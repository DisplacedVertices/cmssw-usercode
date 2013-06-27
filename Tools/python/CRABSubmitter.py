#!/usr/bin/env python

import sys, os, threading, time, ConfigParser, StringIO
from StringIO import StringIO
from CRABTools import crab_popen
    
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
    
    def __init__(self,
                 batch_name,
                 pset_template_fn = sys.argv[0],
                 pset_modifier = None,
                 working_dir_pattern = '%BATCH/crab_%(name)s',
                 pset_fn_pattern = '%BATCH/%(name)s',
                 job_control_from_sample = False,
                 job_splitting = (),
                 data_retrieval = 'return',
                 publish_data_name = '',
                 use_ana_dataset = False,
                 get_edm_output = False,
                 use_parent = False,
                 other_cfg_lines = (),
                 testing = 'testing' in sys.argv,
                 max_threads = 5,
                 ssh_control_persist = False,
                 **kwargs):

        if not testing and CRABSubmitter.get_proxy:
            print 'CRABSubmitter init: mandatory proxy get.'
            os.system('voms-proxy-init -voms cms -valid 192:00')
            CRABSubmitter.get_proxy = False

        self.batch_name = batch_name
        self.testing = testing
        self.max_threads = max_threads

        self.pset_template_fn = pset_template_fn
        self.pset_modifier = pset_modifier

        cfg = ConfigParserEx()
        cfg.set('CRAB', 'jobtype', 'cmssw')
        cfg.set('CRAB', 'scheduler', '%(scheduler)s')
        if not ssh_control_persist:
            cfg.set('USER', 'ssh_control_persist', 'no')

        if working_dir_pattern.startswith('%BATCH/'):
            working_dir_pattern = working_dir_pattern.replace('%BATCH', 'crab/%s' % batch_name)
        self.working_dir_pattern = working_dir_pattern
        cfg.set('USER', 'ui_working_dir', working_dir_pattern)
        mkdirs_if_needed(working_dir_pattern)

        if not pset_fn_pattern.endswith('.py'):
            pset_fn_pattern = pset_fn_pattern + '.py'
        if pset_fn_pattern.startswith('%BATCH/'):
            pset_fn_pattern = pset_fn_pattern.replace('%BATCH', 'crab/psets/%s' % batch_name)
        self.pset_fn_pattern = pset_fn_pattern
        cfg.set('CMSSW', 'pset', pset_fn_pattern)
        mkdirs_if_needed(pset_fn_pattern)

        def get_two_max(s):
            l = []
            for opt in s.split():
                val = kwargs.get(opt, None)
                if val is not None:
                    l.append((opt, val))
            if len(l) > 2:
                raise ValueError('can only set two of %s' % s)
            return l

        self.job_control_from_sample = job_control_from_sample
        if not job_control_from_sample:
            self.job_control_from_sample = False
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
            if data_retrieval == 'fnal':
                cfg.set('USER', 'storage_element', 'T3_US_FNALLPC')
                cfg.set('USER', 'check_user_remote_dir', 0)
            elif data_retrieval == 'cornell':
                cfg.set('USER', 'storage_element', 'T3_US_Cornell')
            if publish_data_name:
                cfg.set('USER', 'publish_data', 1)
                cfg.set('USER', 'publish_data_name', publish_data_name)
                cfg.set('USER', 'dbs_url_for_publication', 'https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet')

        self.use_ana_dataset = use_ana_dataset
        cfg.set('CMSSW', 'datasetpath', '%(ana_dataset)s' if use_ana_dataset else '%(dataset)s')

        if get_edm_output:
            cfg.set('CMSSW', 'get_edm_output', 1)

        if len(other_cfg_lines) % 3 != 0:
            raise ValueError('other_cfg_lines must be flat sequence of (section, option, value, ...) triplets')
        for i in xrange(0, len(other_cfg_lines), 3):
            cfg.set(*other_cfg_lines[i:i+3])
        for opt, val in kwargs.iteritems():
            for section in cfg.sections():
                shib = section + '_'
                if opt.startswith(shib):
                    cfg.set(section, opt.replace(shib, ''), val)

        self.crab_cfg_template = StringIO()
        cfg.write(self.crab_cfg_template)
        self.crab_cfg_template = self.crab_cfg_template.getvalue()

    def crab_cfg(self, sample):
        cfg = ConfigParserEx()
        cfg.readfp(StringIO(self.crab_cfg_template))
        cfg.interpolate(sample)
        dbs_url = sample.ana_dbs_url if self.use_ana_dataset else sample.dbs_url
        if dbs_url:
            cfg.set('CMSSW', 'dbs_url', dbs_url.replace('dbs_url = ', ''))
        if self.job_control_from_sample:
            for cmd in sample.job_control_commands:
                cfg.set('CMSSW', *cmd)
        crab_cfg_fn = 'crab.%s.%s.cfg' % (self.batch_name, sample.name)
        cfg.write(open(crab_cfg_fn, 'wt'))
        return crab_cfg_fn, open(crab_cfg_fn, 'rt').read()

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
            pset += '\n' + '\n'.join(to_add) + '\n'
        pset_fn = self.pset_fn_pattern % sample
        open(pset_fn, 'wt').write(pset)
        return pset_fn, pset

    def submit(self, sample, cleanup_crab_cfg=True, cleanup_pset=False, cleanup_pset_pyc=True, create_only=False):
        print 'batch %s, submit sample %s' % (self.batch_name, sample.name)

        cleanup = []

        crab_cfg_fn, crab_cfg = self.crab_cfg(sample)
        if cleanup_crab_cfg:
            cleanup.append(crab_cfg_fn)

        pset_fn, pset = self.pset(sample)
        if cleanup_pset:
            cleanup.append(pset_fn)
        if cleanup_pset_pyc:
            assert pset_fn.endswith('.py')
            cleanup.append(pset_fn + 'c')

        crab_output = None
        if not self.testing:
            cmd = 'crab -cfg %s -create' % crab_cfg_fn
            if not create_only:
                cmd += ' -submit'
            crab_output = crab_popen(cmd)
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

        os.system('mkdir -p /tmp/%s' % os.environ['USER'])
        log = open('/tmp/%s/CRABSubmitter_%s.log' % (os.environ['USER'], self.batch_name), 'wt')
        for name in sorted(results.keys()):
            log.write('*' * 250)
            log.write('\n\n%s\n' % name)
            log.write(results[name])
            log.write('\n\n')

if __name__ == '__main__':
    cs = CRABSubmitter('abalone')
    from JMTucker.Tools.Samples import ttbarincl, mfv_neutralino_tau1000um_M0400
    print
    print cs.crab_cfg(ttbarincl)
    print
    print cs.crab_cfg(mfv_neutralino_tau1000um_M0400)
