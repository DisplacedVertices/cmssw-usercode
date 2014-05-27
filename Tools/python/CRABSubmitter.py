#!/usr/bin/env python

import sys, os, glob, threading, time, ConfigParser, StringIO
from StringIO import StringIO
from CRABTools import crab_popen, crab_submit_in_batches, crab_renew_proxy_if_needed
    
class ConfigParserEx(ConfigParser.ConfigParser):
    def set(self, section, option, value):
        if not self.has_section(section):
            self.add_section(section)
        return ConfigParser.ConfigParser.set(self, section, option, value)

    def interpolate(self, vars):
        for section in self.sections():
            for option in self.options(section):
                self.set(section, option, self.get(section, option, raw=True) % vars)

def mkdirs_if_needed(path):
    dn = os.path.dirname(path)
    if dn:
        os.system('mkdir -p %s' % dn)

class CRABSubmitter:
    get_proxy = True
    aaa_locations = 'T1_US_FNAL,T2_US_Florida,T2_US_MIT,T2_US_Nebraska,T2_US_Purdue,T2_US_UCSD,T2_US_Wisconsin,T2_US_Vanderbilt,T3_US_Brown,T3_US_Colorado,T3_US_NotreDame,T3_US_UMiss'
    half_mc_path = '/uscms/home/tucker/mfvrecipe/HalfMCLists/%s.txt.gz'
    
    def __init__(self,
                 batch_name,
                 pset_template_fn = sys.argv[0],
                 pset_modifier = None,
                 working_dir_pattern = '%BATCH/crab_%(name)s',
                 pset_fn_pattern = '%BATCH/%(name)s',
                 scheduler = None,
                 job_control_from_sample = False,
                 job_splitting = (),
                 data_retrieval = 'return',
                 publish_data_name = '',
                 use_ana_dataset = False,
                 use_parent_dataset = False,
                 get_edm_output = False,
                 use_parent = False,
                 other_cfg_lines = (),
                 testing = 'testing' in sys.argv or 'cs_testing' in sys.argv,
                 max_threads = 5,
                 ssh_control_persist = False,
                 crab_cfg_modifier = None,
                 aaa = False,
                 manual_datasets = None,
                 run_half_mc = False,
                 **kwargs):

        if '/' in batch_name:
            raise ValueError('/ not allowed in batch name')
        self.batch_name = batch_name
        self.batch_dir = 'crab/%s' % batch_name
        self.existed = False
        if os.path.exists(self.batch_dir):
            if 'cs_append' not in sys.argv:
                raise ValueError('batch_dir %s already exists, refusing to clobber ("cs_append" in argv to override)' % self.batch_dir)
            self.existed = True

        if not testing and CRABSubmitter.get_proxy:
            print 'CRABSubmitter init: checking proxies, might ask for password twice (but you can skip it with ^C if you know what you are doing).'
            crab_renew_proxy_if_needed()
            CRABSubmitter.get_proxy = False

        self.username = os.environ['USER']

        self.git_status_dir = self.batch_dir + '/gitstatus/'
        mkdirs_if_needed(self.git_status_dir)
        if self.existed:
            files = glob.glob(os.path.join(self.git_status_dir, '*'))
            if files:
                replaced_git_status_dir = os.path.join(self.git_status_dir, str(int(time.time())))
                os.mkdir(replaced_git_status_dir)
                for f in files:
                    os.rename(f, os.path.join(replaced_git_status_dir, os.path.basename(f)))
        os.system("git log --pretty=format:'%%H' -n 1 > %shash" % self.git_status_dir)
        os.system("git status --untracked-files=all --ignored | grep -v pyc > %sstatus" % self.git_status_dir)
        self.git_untracked_tmp_fn = '/tmp/%s/untracked.tgz' % self.username
        git_untracked_file_list_cmd = "git status --porcelain | grep '^??' | sed 's/??//'"
        git_untracked_file_list = crab_popen(git_untracked_file_list_cmd)
        if git_untracked_file_list:
            git_tar_ret = os.system("tar czf %s -C `git rev-parse --show-toplevel` `%s`" % (self.git_untracked_tmp_fn, git_untracked_file_list_cmd))
            if git_tar_ret != 0:
                print '\033[36;7m warning: \033[m git-untracked tar returned non-zero exit code'
            elif os.stat(self.git_untracked_tmp_fn).st_size > 100*1024**2:
                print '\033[36;7m warning: \033[m git-untracked tarball is bigger than 100M, leaving in %s' % self.git_untracked_tmp_fn
            else:
                os.system('mv %s %s' % (self.git_untracked_tmp_fn, self.git_status_dir))
        os.system('git diff > %sdiff' % self.git_status_dir)
        
        self.testing = testing
        self.max_threads = max_threads

        self.crab_cfg_modifier = crab_cfg_modifier

        self.pset_template_fn = pset_template_fn
        self.pset_modifier = pset_modifier

        cfg = ConfigParserEx()
        cfg.set('CRAB', 'jobtype', 'cmssw')
        cfg.set('CRAB', 'scheduler', scheduler if scheduler else ('%(scheduler)s' if not use_ana_dataset else '%(ana_scheduler)s'))
        if not ssh_control_persist:
            cfg.set('USER', 'ssh_control_persist', 'no')

        if working_dir_pattern.startswith('%BATCH/'):
            working_dir_pattern = working_dir_pattern.replace('%BATCH', self.batch_dir)
        self.working_dir_pattern = working_dir_pattern
        cfg.set('USER', 'ui_working_dir', working_dir_pattern)
        mkdirs_if_needed(working_dir_pattern)

        if not pset_fn_pattern.endswith('.py'):
            pset_fn_pattern = pset_fn_pattern + '.py'
        if pset_fn_pattern.startswith('%BATCH/'):
            pset_fn_pattern = pset_fn_pattern.replace('%BATCH', self.batch_dir + '/psets')
        self.pset_fn_pattern = pset_fn_pattern
        cfg.set('CMSSW', 'pset', pset_fn_pattern)
        mkdirs_if_needed(pset_fn_pattern)

        self.manual_datasets = manual_datasets
        if manual_datasets is not None:
            if run_half_mc:
                raise ValueError('run_half_mc is not for manual_datasets mode')
            if not job_control_from_sample:
                for opt in 'total_number_of_events events_per_job'.split():
                    if not kwargs.has_key(opt):
                        raise ValueError('must specify %s in manual_datasets mode' % opt)
                    setattr(self, 'manual_%s' % opt, kwargs[opt])
                    del kwargs[opt]

            cfg.set('CMSSW', 'datasetpath', 'None')
            cfg.set('CRAB', 'scheduler', 'condor')
            # crab_cfg below has to set out CMSSW.number_of_jobs

        self.run_half_mc = run_half_mc

        def get_two_max(s):
            l = []
            for opt in s.split():
                val = kwargs.get(opt, None)
                if val is not None:
                    l.append((opt, int(val)))
            if len(l) > 2:
                raise ValueError('can only set two of %s' % s)
            return l

        self.job_control_from_sample = job_control_from_sample
        if not job_control_from_sample and manual_datasets is None:
            if len(job_splitting) < 2:
                job_splitting = get_two_max('total_number_of_events events_per_job number_of_jobs')
            if len(job_splitting) < 2:
                job_splitting = get_two_max('total_number_of_lumis lumis_per_job number_of_jobs')
            if len(job_splitting) < 2:
                raise ValueError('must provide job splitting')

            if type(job_splitting[0]) == str:
                if len(job_splitting) % 2 != 0:
                    raise ValueError('job_splitting must be flat sequence of (name, value, ...) pairs')
                for i in xrange(0, len(job_splitting), 2):
                    cfg.set('CMSSW', *job_splitting[i:i+2])
            else:
                for opt, val in job_splitting:
                    if kwargs.has_key(opt):
                        del kwargs[opt]
                    cfg.set('CMSSW', opt, val)

        data_retrieval = data_retrieval.lower()
        if data_retrieval == 'return':
            cfg.set('USER', 'return_data', 1)
        else:
            cfg.set('USER', 'copy_data', 1)
            publish_ok = True
            if data_retrieval == 'fnal':
                cfg.set('USER', 'storage_element', 'T3_US_FNALLPC')
            elif data_retrieval == 'cornell':
                cfg.set('USER', 'storage_element', 'T3_US_Cornell')

            if publish_data_name:
                if not publish_ok:
                    raise ValueError('refusing to set up publishing')
                cfg.set('USER', 'publish_data', 1)
                cfg.set('USER', 'publish_data_name', publish_data_name)
                cfg.set('USER', 'dbs_url_for_publication', 'phys03')
                cfg.set('CMSSW', 'use_dbs3', '1')

        self.use_ana_dataset = use_ana_dataset
        if not self.manual_datasets:
            self.use_parent_dataset = use_parent_dataset
            datasetpath = '%(dataset)s'
            if use_ana_dataset:
                datasetpath = '%(ana_dataset)s'
            elif use_parent_dataset:
                datasetpath = '%(parent_dataset)s'
            cfg.set('CMSSW', 'datasetpath', datasetpath)

            if use_parent:
                cfg.set('CMSSW', 'use_parent', 1)

        if get_edm_output:
            cfg.set('CMSSW', 'get_edm_output', 1)

        if aaa:
            cfg.set('CRAB', 'scheduler', 'remoteGlidein')
            cfg.set('GRID', 'data_location_override', self.aaa_locations)
            cfg.set('GRID', 'remove_default_blacklist', 1)

        if len(other_cfg_lines) % 3 != 0:
            raise ValueError('other_cfg_lines must be flat sequence of (section, option, value, ...) triplets')
        for i in xrange(0, len(other_cfg_lines), 3):
            cfg.set(*other_cfg_lines[i:i+3])
        for opt, val in kwargs.iteritems():
            for section in ('CMSSW', 'USER', 'CRAB', 'GRID'):
                shib = section + '_'
                if opt.startswith(shib):
                    cfg.set(section, opt.replace(shib, ''), val)

        self.crab_cfg_template = StringIO()
        cfg.write(self.crab_cfg_template)
        self.crab_cfg_template = self.crab_cfg_template.getvalue()

    def half_mc_fn(self, sample):
        half_mc_fn = self.half_mc_path % sample.name
        return half_mc_fn if os.path.isfile(half_mc_fn) else ''

    def crab_cfg(self, sample):
        cfg = ConfigParserEx()
        cfg.readfp(StringIO(self.crab_cfg_template))
        cfg.interpolate(sample)

        if not self.manual_datasets:
            dbs_url = sample.ana_dbs_url if self.use_ana_dataset else sample.dbs_url # assume if use_parent_dataset the dbs_url is the same
            cfg.set('CMSSW', 'use_dbs3', '1')
            if dbs_url:
                cfg.set('CMSSW', 'dbs_url', dbs_url.replace('dbs_url = ', ''))
            if self.job_control_from_sample:
                for cmd in sample.job_control_commands(ana=self.use_ana_dataset):
                    if cmd:
                        cfg.set('CMSSW', *cmd)
        else:
            cfg.set('USER', 'script_exe', sample.manual_script_fn)
            cfg.set('CMSSW', 'number_of_jobs', sample.manual_script_njobs)
            cfg.set('CMSSW', 'events_per_job', '-1') # totally fake, will be re-written at batch job run time

        if self.crab_cfg_modifier is not None:
            ret = self.crab_cfg_modifier(sample)
            for entry in ret:
                cfg.set(*entry)

        if self.run_half_mc:
            half_mc_fn = self.half_mc_fn(sample)
            if half_mc_fn:
                try:
                    aif = cfg.get('USER', 'additional_input_files') + ',' + half_mc_fn
                except ConfigParser.NoOptionError:
                    aif = half_mc_fn
                cfg.set('USER', 'additional_input_files', aif)

        crab_cfg_fn = 'crab.%s.%s.cfg' % (self.batch_name, sample.name)
        cfg.write(open(crab_cfg_fn, 'wt'))
        return crab_cfg_fn, open(crab_cfg_fn, 'rt').read(), cfg

    def pset(self, sample, tmp_fn=None):
        pset = open(self.pset_template_fn).read()
        if self.pset_modifier is not None:
            ret = self.pset_modifier(sample)
            if type(ret) != tuple:
                to_add = ret
                to_replace = []
            else:
                to_add, to_replace = ret
            for a,b,err in to_replace:
                if pset.find(a) < 0:
                    raise ValueError(err)
                pset = pset.replace(a,b)
            pset += '\n' + '\n'.join(to_add) + '\n'
        pset_fn = self.pset_fn_pattern % sample if tmp_fn is None else tmp_fn

        if self.run_half_mc:
            if not self.half_mc_fn(sample):
                print '\033[1m warning: \033[0m half_mc not available for sample %s' % (sample.name)
            else:
                # This must be the last modification because we will
                # modify all the paths and they must be finalized.
                pset += '''
process.runHalfMCVeto = cms.EDFilter('EventIdVeto',
                                     list_fn = cms.string('%s.txt.gz'),
                                     use_run = cms.bool(False))
for p in process.paths.keys():
    getattr(process, p).insert(0, ~process.runHalfMCVeto)
''' % sample.name

        open(pset_fn, 'wt').write(pset)
        return pset_fn, pset

    def manual_splits(self, sample, filenevs):
        splits = []
        files = []
        skipsum = 0
        totevsum = 0
        evsum = 0
        curr = 0

        if self.job_control_from_sample:
            jcc = dict(sample.job_control_commands(ana=self.use_ana_dataset))
            try:
                total_number_of_events = jcc['total_number_of_events']
                events_per_job = jcc['events_per_job']
            except KeyError:
                print '\033[36;7m warning: \033[m manual_splits: no total_number_of_events, events_per_job for %s' % sample.name
                total_number_of_events = jcc.get('total_number_of_events', -1)
                events_per_job = jcc.get('events_per_job', 100000)
        else:
            total_number_of_events = self.manual_total_number_of_events
            events_per_job = self.manual_events_per_job

        while curr < len(filenevs):
            if len(filenevs[curr]) < 3:
                fn, nevents = filenevs[curr]
                skip = 0
            else:
                fn, nevents, skip = filenevs[curr]

            files.append(fn)
            skipsum += skip
            evsum += nevents - skip

            advance = True

            if evsum >= events_per_job:
                breakmax = False

                nevinjob = events_per_job
                if total_number_of_events >= 0 and totevsum + nevinjob >= total_number_of_events:
                    breakmax = True
                    nevinjob = total_number_of_events - totevsum

                splits += [(files, nevinjob, skipsum)]
                totevsum += nevinjob

                if breakmax:
                    break

                if evsum > events_per_job:
                    filenevs[curr] = (fn, nevents, nevents - (evsum - events_per_job))
                    advance = False

                files, skipsum, evsum = [], 0, 0

            if advance:
                curr += 1

        if files and (total_number_of_events < 0 or evsum < events_per_job):
            splits += [(files, events_per_job, skipsum)]

        return splits
    
    def manual_script(self, sample, splits):
        script = '''#!/bin/sh

NJob=$1

SPLITTING_DETAILS

echo Messing with pset.py
cat >> pset.py <<EOF
process.source.fileNames = "${FileNames[$NJob]}".split(',')
process.maxEvents.input = ${NEvents[$NJob]}
process.source.skipEvents = ${SkipEvents[$NJob]}
del process.source.firstLuminosityBlock
EOF

cmsRun -j $RUNTIME_AREA/crab_fjr_$NJob.xml -p pset.py
ECODE=$?
echo manual exit code was $ECODE, done!
exit $ECODE
'''

        splitting_details = []
        for i, (files, maxev, skipev) in enumerate(splits):
            njob = i+1
            splitting_details.append('FileNames[%i]=%s' % (njob, ','.join(files)))
            splitting_details.append('NEvents[%i]=%i' % (njob, maxev))
            splitting_details.append('SkipEvents[%i]=%i' % (njob, skipev))
        splitting_details.sort()

        script_fn = 'crabsubmitter.%s.%s.sh' % (self.batch_name, sample.name)
        script = script.replace('SPLITTING_DETAILS', '\n'.join(splitting_details))
        open(script_fn, 'wt').write(script)
        return script_fn, script

    def submit(self, sample, cleanup_crab_cfg=True, cleanup_pset=False, cleanup_pset_pyc=True, cleanup_manual_script=True, create_only=False):
        print 'batch %s, submit sample %s' % (self.batch_name, sample.name)

        cleanup = []

        if self.manual_datasets:
            filenevs = self.manual_datasets[sample.name]
            splits = self.manual_splits(sample, filenevs)
            manual_script_fn, manual_script = self.manual_script(sample, splits)
            sample.manual_script_njobs = len(splits)  # to communicate with crab_cfg
            sample.manual_script_fn = manual_script_fn # ditto
            if cleanup_manual_script:
                cleanup.append(manual_script_fn)
                    
        crab_cfg_fn, crab_cfg, crab_cfg_obj = self.crab_cfg(sample)
        if cleanup_crab_cfg:
            cleanup.append(crab_cfg_fn)

        pset_fn, pset = self.pset(sample)
        if cleanup_pset:
            cleanup.append(pset_fn)
        if cleanup_pset_pyc:
            assert pset_fn.endswith('.py')
            cleanup.append(pset_fn + 'c')

        crab_output = 'Not run'
        if not self.testing:
            working_dir = crab_cfg_obj.get('USER', 'ui_working_dir')
            if not os.path.isdir(working_dir):
                cmd = 'crab -cfg %s -create' % crab_cfg_fn
                if not create_only:
                    cmd += ' -submit'
                crab_output = crab_popen(cmd)
                ok = False
                suball = False
                for line in crab_output.split('\n'):
                    if 'Total of' in line and ('jobs created' if create_only else 'jobs submitted') in line:
                        ok = True
                    if not create_only and 'The CRAB client will not submit task with more than 500 jobs.' in line:
                        suball = True
                if not ok:
                    if suball:
                        print '%s needs to sub in groups of 500, doing now (and not checking for errors!)' % sample.name
                        crab_submit_in_batches(working_dir)
                    else:
                        print '\033[36;7m warning: \033[m sample %s might have had problem(s) submitting, check the log in /tmp' % sample.name
            else:
                print '\033[1m warning: \033[0m sample %s not submitted, directory %s already exists' % (sample.name, working_dir)
            os.system('rm -f %s' % ' '.join(cleanup))
        else:
            print 'in testing mode, not submitting anything.'
            diff_out, diff_ret = crab_popen('diff -uN %s %s' % (self.pset_template_fn, pset_fn), return_exit_code=True)
            if diff_ret != 0:
                print '.py diff:\n---------'
                print diff_out
                raw_input('continue?')
                print
            print 'crab.cfg:\n---------'
            print crab_cfg
            raw_input('continue?')
            if self.manual_datasets:
                print 'manual script:\n---------'
                print manual_script
                raw_input('continue?')
            print '\n'

        return crab_output

    def submit_all(self, samples, **kwargs):
        if self.testing:
            print 'in testing mode, so only doing one sample at a time.'
            for sample in samples:
                self.submit(sample, **kwargs)
            return
            
        results = {}
        threads = []
        print 'launching threads (max %s)...' % self.max_threads
        def threadable_fcn(sample):
            results[sample.name] = self.submit(sample, **kwargs)
        for sample in samples:
            while threading.active_count() - 1 >= self.max_threads:
                time.sleep(0.1)
            thread = threading.Thread(target=threadable_fcn, args=(sample,))
            threads.append((sample,thread))
            thread.start()
        sleep_count = 0
        while threading.active_count() > 1:
            if sleep_count % 150 == 3:
                print 'waiting for these threads:', ' '.join(s.name for s,t in threads if t.is_alive())
            sleep_count += 1
            time.sleep(0.1)
        print 'done waiting for threads!'

        os.system('mkdir -p /tmp/%s' % self.username)
        log_fn = '/tmp/%s/CRABSubmitter_%s.log' % (self.username, self.batch_name)
        log = open(log_fn, 'wt')
        for name in sorted(results.keys()):
            log.write('*' * 250)
            log.write('\n\n%s\n' % name)
            log.write(results[name])
            log.write('\n\n')
        print 'log fn is', log_fn

if __name__ == '__main__':
    cs = CRABSubmitter('abalone')
    from JMTucker.Tools.Samples import ttbarincl, mfv_neutralino_tau1000um_M0400
    print
    print cs.crab_cfg(ttbarincl)
    print
    print cs.crab_cfg(mfv_neutralino_tau1000um_M0400)
