#!/usr/bin/env python

import os
import shutil
import string
import sys
import time
from copy import deepcopy
from datetime import datetime
from pprint import pprint
from StringIO import StringIO
from CRAB3Tools import Config, crab_global_options, crab_dirs_root, crab_renew_proxy_if_needed, crab_command
from general import mkdirs_if_needed, popen, save_git_status

class CRABSubmitter:
    batch_name_allowed = string.ascii_letters + string.digits + '_'
    get_proxy = True
    aaa_locations = [
        #'T1_US_FNAL',
        'T2_US_Caltech',
        #'T2_US_Florida',
        'T2_US_MIT',
        'T2_US_Nebraska',
        #'T2_US_Purdue',
        'T2_US_UCSD',
        'T2_US_Vanderbilt',
        'T2_US_Wisconsin',
        ]  # T3_US_Brown,T3_US_Colorado,T3_US_NotreDame,T3_US_UMiss

    # JMTBAD missing:
    # create_only mode -- is there --dryrun but no dry run, just make the tarball?
    # skip_common_files
    # storage_catalog_override but not needed anymore right?
    # threaded (proccesssed) submit_all

    def __init__(self,    # JMTBAD check for needed and reorder args
                 batch_name,
                 ex = '',
                 testing = 'testing' in sys.argv or 'cs_testing' in sys.argv,
                 max_threads = 5,
                 cfg_modifier = None,
                 cfg_modifier_strings = [],
                 pset_template_fn = sys.argv[0],
                 pset_modifier = None,
                 input_files = None,
                 script_exe = None,
                 output_files = None,
                 extra_output_files = None,
                 transfer_logs = True,
                 transfer_outputs = True,
                 dataset = 'main',
                 lumi_mask = None,
                 job_control_from_sample = False,
                 storage_site = 'T3_US_FNALLPC',
                 publish_name = '',
                 aaa = False,
                 fnallpc = False,
                 modify_pset_hash = True,
                 **kwargs):

        if aaa and fnallpc:
            raise ValueError('cannot do both aaa and fnallpc options')

        for arg in sys.argv:
            if arg.startswith('cs_name='):
                batch_name = arg.replace('cs_name=', '')
                break

        if not set(self.batch_name_allowed).issuperset(set(batch_name.replace('/', ''))):
            raise ValueError('illegal batch name %s, allowed characters are letters, numbers, and _' % batch_name)

        nslash = batch_name.count('/')
        if nslash > 1:
            raise ValueError('only one slash allowed in batch name %s' % batch_name)
        elif nslash == 1:
            batch_path = os.path.abspath(crab_dirs_root(batch_name))
            batch_root = os.path.dirname(batch_path)
            if os.path.exists(batch_root):
                if not os.path.isdir(batch_root):
                    raise ValueError('slashy mode: batch_root %s exists but is not a dir?' % batch_root)
                for x in os.listdir(batch_root):
                    fx = os.path.join(batch_root, x)
                    if x == 'gitstatus' or x == 'inputs' or x == 'psets' or not os.path.isdir(fx):
                        raise ValueError('bad slashy %s' % batch_path)
            else:
                os.mkdir(batch_root)
                os.mkdir(batch_path)

        self.batch_name = batch_name
        self.batch_dir = crab_dirs_root(batch_name) # JMTBAD rename -- what crab3 calls workArea
        self.existed = False

        if ex:
            ex = str(ex) + '_'
        self.ex_str = 'ex_%s%s' % (ex, str(int(time.time()*1000)))

        self.psets_dir = os.path.join(self.batch_dir, self.ex_str, 'psets')

        # JMTBAD this will never happen now that we allow multiple submits to the same dir
        if os.path.exists(self.psets_dir):  # check psets_dir instead of batch_dir since we might be from metasubmitter
            if 'cs_append' not in sys.argv:
                raise ValueError('batch_dir %s already exists, refusing to clobber ("cs_append" in argv to override)' % self.batch_dir)
            self.existed = True

        if not testing and CRABSubmitter.get_proxy:
            print 'CRABSubmitter init: checking proxies, might ask for password twice (but you can skip it with ^C if you know what you are doing).'
            crab_renew_proxy_if_needed()
            CRABSubmitter.get_proxy = False
      
        self.username = os.environ['USER']
        os.system('mkdir -p /tmp/%s' % self.username)

        self.git_status_dir = os.path.join(self.batch_dir, self.ex_str, 'gitstatus')
        save_git_status(self.git_status_dir)

        self.testing = testing
        self.max_threads = max_threads  # JMTBAD rename -> processes

        self.cfg_modifier = cfg_modifier
        self.cfg_modifier_strings = cfg_modifier_strings
        for k,v in kwargs.iteritems():
            if k.startswith('crab_cfg_'):
                self.cfg_modifier_strings.append((k.replace('crab_', '').replace('__', 'UNDERSCORE').replace('_', '.').replace('UNDERSCORE', '_'), v))

        if '$' in pset_template_fn:
            pset_template_fn =  os.path.expandvars(pset_template_fn)
        if '~' in pset_template_fn:
            pset_template_fn = os.path.expanduser(pset_template_fn)
        self.pset_template_fn = pset_template_fn
        self.pset_modifier = pset_modifier

        self.cfg_template = Config()
        self.cfg_template.General.transferLogs = transfer_logs
        self.cfg_template.General.transferOutputs = transfer_outputs
        self.cfg_template.General.workArea = self.batch_dir
        self.cfg_template.JobType.pluginName = 'Analysis' # JMTBAD PrivateMC -- also needs cfg.Data.primaryDataset, splitting EventBased, unitsPerJob, totalUnits

        if input_files:
            if type(input_files) == str:
                input_files = [input_files]
            self.cfg_template.JobType.inputFiles = input_files

        if script_exe:
            self.cfg_template.JobType.scriptExe = script_exe

        if output_files and extra_output_files:
            raise ValueError("can't have output_files and extra_output_files at the same time")
        elif output_files:
            if type(output_files) == str:
                output_files = [output_files]
            self.cfg_template.JobType.disableAutomaticOutputCollection = True
            self.cfg_template.JobType.outputFiles = output_files
        elif extra_output_files:
            if type(extra_output_files) == str:
                extra_output_files = [extra_output_files]
            self.cfg_template.JobType.outputFiles = extra_output_files

        self.dataset = dataset
        self.cfg_template.Data.inputDataset = 'SETLATER'
        self.cfg_template.Data.inputDBS = 'SETLATER'

        self.cfg_template.General.requestName = 'SETLATER'

        self.cfg_fn_pattern = os.path.join(self.psets_dir, 'crabConfig.%(name)s.py')
        mkdirs_if_needed(self.cfg_fn_pattern)

        self.pset_fn_pattern = os.path.join(self.psets_dir, '%(name)s.py')
        mkdirs_if_needed(self.pset_fn_pattern)
        self.cfg_template.JobType.psetName = 'SETLATER'

        self.job_control_from_sample = job_control_from_sample
        if not self.job_control_from_sample:
            def _get(s):
                x = kwargs.get(s, None)
                if x is None:
                    raise ValueError('job_control_from_sample is False, must provide job splitting parameter %s' % s)
                return x
            self.cfg_template.Data.splitting   = _get('splitting')
            self.cfg_template.Data.unitsPerJob = _get('units_per_job')
            self.cfg_template.Data.totalUnits  = _get('total_units')
            if lumi_mask:
                self.cfg_template.Data.lumiMask = lumi_mask

        if storage_site.lower() == 'cornell':
            self.cfg_template.Site.storageSite = 'T3_US_Cornell'
        elif storage_site.lower() == 'fnal':
            self.cfg_template.Site.storageSite = 'T3_US_FNALLPC'
        else:
            self.cfg_template.Site.storageSite = storage_site

        self.cfg_template.Data.publication = bool(publish_name)
        self.cfg_template.Data.outputDatasetTag = publish_name

        self.aaa = aaa
        if self.aaa:
            self.cfg_template.Data.ignoreLocality = True
            self.cfg_template.Site.whitelist = self.aaa_locations

        if fnallpc:
            self.cfg_template.Site.whitelist = ['T3_US_FNALLPC']
            self.cfg_template.Site.ignoreGlobalBlacklist = True

        self.modify_pset_hash = modify_pset_hash

    def cfg(self, sample):
        cfg = deepcopy(self.cfg_template) # JMTBAD needed?
        
        cfg.General.requestName = self.batch_name.replace('/', '_') + '_' + sample.name # verbose for dashboard, we'll rename the crab directory back to just crab_samplename after submission
        cfg.JobType.psetName = self.pset_fn_pattern % sample
        cfg.Data.inputDataset = sample.dataset
        cfg.Data.inputDBS = sample.dbs_inst

        if self.job_control_from_sample:
            sample.job_control(cfg.Data)

        if sample.aaa:
            cfg.Data.ignoreLocality = True
            cfg.Site.whitelist = sample.aaa

        if self.cfg_modifier is not None:
            self.cfg_modifier(cfg, sample)

        for evl, val in self.cfg_modifier_strings:
            exec '%s = val' % evl

        cfg_fn = self.cfg_fn_pattern % sample
        open(cfg_fn, 'wt').write(cfg.pythonise_()) # JMTBAD this file is just for debugging
        return cfg_fn, cfg

    def pset(self, sample):
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
            if to_add:
                pset += '\n' + '\n'.join(to_add) + '\n'

        pset_fn = self.pset_fn_pattern % sample
        pset_orig_fn = pset_fn.replace('.py', '_orig.py')

        extra = ''
        if self.modify_pset_hash:
            extra += '\nprocess.dummyForPsetHash = cms.PSet(dummy = cms.string(%r))' % (str(datetime.now()) + sample.dataset)
        extra += "\nopen(%r, 'wt').write(process.dumpPython())" % pset_fn
        open(pset_orig_fn, 'wt').write(pset + extra)

        out = popen('python %s' % pset_orig_fn)
        open(pset_orig_fn, 'wt').write(pset)

        return pset_orig_fn, pset_fn, pset

    def submit(self, sample):
        cleanup = [] # not so much to clean up any more

        result = {'stdout': 'Not run'}

        try:
            sample.set_curr_dataset(self.dataset)
        except KeyError:
            print "\033[1m warning: \033[0m sample %s not submitted, doesn't have dataset %s" % (sample.name, self.dataset)
            return result

        cfg_fn, cfg = self.cfg(sample)
        pset_orig_fn, pset_fn, pset = self.pset(sample)

        assert pset_fn.endswith('.py')
        cleanup.append(pset_fn + 'c')

        if not self.testing:
            working_dir = os.path.join(cfg.General.workArea, 'crab_' + cfg.General.requestName)
            new_working_dir = os.path.join(cfg.General.workArea, 'crab_' + sample.name)

            if not os.path.isdir(working_dir) and not os.path.isdir(new_working_dir):
                success, nretries = False, 10
                while not success and nretries:
                    result = crab_command('submit', config = cfg)
                    should_retry = result.get('status', '') == 'HTTPException' and result.has_key('HTTPException')
                    if should_retry:
                        nretries -= 1
                        print sample.name, 'crapped out with HTTPException,', nretries, 'tries left'
                        shutil.rmtree(working_dir)
                    else:
                        open(os.path.join(working_dir, 'cs_ex'), 'wt').write(self.ex_str)
                        success = True

                if success:
                    # The requestName contains the full batch_name so the entries in dashboard
                    # are distinguishable, but once the job is submitted the local directory
                    # name can be changed back to just having the sample name.
                    shutil.move(working_dir, new_working_dir)
                else:
                    print '\033[1m warning: \033[0m sample %s not submitted, nretries exceeded' % (sample.name)
            else:
                print '\033[1m warning: \033[0m sample %s not submitted, directory %s already exists' % (sample.name, working_dir)

            if cleanup:
                os.system('rm -f %s' % ' '.join(cleanup))
        else:
            print 'in testing mode, not submitting anything.'
            diff_out, diff_ret = popen('diff -uN %s %s' % (self.pset_template_fn, pset_orig_fn), return_exit_code=True)
            if diff_ret != 0:
                print '.py diff:\n---------'
                print diff_out
                raw_input('continue?')
                print
            print 'crab.cfg:\n---------'
            print open(cfg_fn).read()
            raw_input('continue?')
            print '\n'

        return result

    def submit_all(self, samples, **kwargs):
        if True or self.testing: # JMTBAD
            if self.testing:
                print 'in testing mode, so only doing one sample at a time.'
            dbg_f = open(os.path.join(os.environ['HOME'], '.jmtct_csdbg'), 'at')
            dbg_f.write(str(datetime.now()) + '\n')
            for sample in samples:
                result = self.submit(sample, **kwargs)
                dbg_f.write('("%s", "%s", %r) + \n' % (self.batch_name, sample.name, result))
                stdout = result['stdout']
                del result['stdout']
                if 'Success' in stdout:
                    print 'submit %s %s' % (self.batch_name, sample.name), '\x1b[92msuccess!\x1b[0m', result['uniquerequestname']
                else:
                    print '================================================='
                    print 'submit %s %s' % (self.batch_name, sample.name)
                    print stdout
                    pprint(result)
                    print '================================================='
            return

        raise NotImplementedError('multithreading -> multiprocessing')

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

        log_fn = os.path.join(self.git_status_dir, 'crabsubmitter.log')
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
