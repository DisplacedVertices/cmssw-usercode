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
                 pset_adder = None,
                 working_dir_pattern = '%BATCH/crab_%(name)s',
                 pset_fn_pattern = '%BATCH/%(name)s',
                 job_splitting = ('total_number_of_events', -1, 'events_per_job', 1000),
                 data_retrieval = 'return',
                 publish_data_name = '',
                 use_ana_dataset = False,
                 get_edm_output = False,
                 use_parent = False,
                 other_cfg_lines = [],
                 argv = sys.argv,
                 crab_cfg_fn = 'crab.cfg',
                 max_threads = 5,
                 ):

        if CRABSubmitter.get_proxy:
            os.system('voms-proxy-init -voms cms')
            CRABSubmitter.get_proxy = False

        self.batch_name = batch_name
        self.testing = 'testing' in argv
        self.max_threads = max_threads

        self.pset_template_fn = pset_template_fn
        self.pset_adder = pset_adder

        cfg = ConfigParserEx()
        cfg.set('CRAB', 'jobtype', 'cmssw')
        cfg.set('CRAB', 'scheduler', '%(scheduler)s')
        self.crab_cfg_fn = crab_cfg_fn

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

        if len(job_splitting) % 2 != 0:
            raise ValueError('job_splitting must be flat sequence of (name, value, ...) pairs')
        for i in xrange(0, len(job_splitting), 2):
            cfg.set('CMSSW', *job_splitting[i:i+2])

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
        cfg.write(open(self.crab_cfg_fn, 'wt'))
        return self.crab_cfg_fn, open(self.crab_cfg_fn, 'rt').read()

    def pset(self, sample):
        pset = open(self.pset_template_fn).read()
        if self.pset_adder is not None:
            to_add = self.pset_adder(sample) 
            pset += '\n' + '\n'.join(to_add) + '\n'
        pset_fn = self.pset_fn_pattern % sample
        open(pset_fn, 'wt').write(pset)
        return pset_fn, pset

    def submit(self, sample, cleanup_crab_cfg=True, cleanup_pset=False, cleanup_pset_pyc=True):
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
            crab_output = crab_popen('crab -cfg %s -create -submit' % crab_cfg_fn)
            os.system('rm -f %s' % ' '.join(cleanup))
        else:
            print 'in testing mode, not submitting anything.'
            print '.py diff:\n---------'
            os.system('diff -uN %s %s' % (self.pset_template_fn, pset_fn))
            raw_input('continue?')
            print '\ncrab.cfg:\n---------'
            os.system('cat crab.cfg')
            raw_input('continue?')
            print '\n'

        return crab_output

    def submit_all(self, samples):
        results = {}
        threads = []
        print 'launching threads...'
        def threadable_fcn(s):
            print 'submitting', s.name
            results[s.name] = self.submit(s)
        for sample in samples:
            while threading.active_count() - 1 >= self.max_threads:
                time.sleep(0.1)
            thread = threading.Thread(target=threadable_fcn, args=(s,))
            threads.append((sample,thread))
            thread.start()
        sleep_count = 0
        while threading.active_count() > 1:
            if sleep_count % 150 == 3:
                print 'waiting for these threads:', ' '.join(s.name for s,t in threads if t.is_alive())
            sleep_count += 1
            time.sleep(0.1)
        print 'done waiting for threads!'
        
if __name__ == '__main__':
    cs = CRABSubmitter('abalone')
    from JMTucker.Tools.Samples import ttbarincl, mfv_neutralino_tau1000um_M0400
    print
    print cs.crab_cfg(ttbarincl)
    print
    print cs.crab_cfg(mfv_neutralino_tau1000um_M0400)
