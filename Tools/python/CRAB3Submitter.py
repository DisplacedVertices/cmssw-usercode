#!/usr/bin/env python

import os
import sys
import time
from copy import deepcopy
from pprint import pprint
from StringIO import StringIO
from CRAB3Tools import Config, crab_global_options, crab_dirs_root, crab_renew_proxy_if_needed, crab_command
from general import popen, save_git_status

def mkdirs_if_needed(path):
    dn = os.path.dirname(path)
    if dn:
        os.system('mkdir -p %s' % dn)

class CRABSubmitter:
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
                 testing = 'testing' in sys.argv or 'cs_testing' in sys.argv,
                 max_threads = 5,
                 cfg_modifier = None,
                 pset_template_fn = sys.argv[0],
                 pset_modifier = None,
                 transfer_logs = True,
                 transfer_outputs = True,
                 dataset = 'main',
                 job_control_from_sample = False,
                 storage_site = 'T3_US_FNALLPC',
                 publish_name = '',
                 aaa = False,
                 modify_pset_hash = True,
                 **kwargs):

        for arg in sys.argv:
            if arg.startswith('cs_name='):
                batch_name = arg.replace('cs_name=', '')
                break

        if '/' in batch_name:
            raise ValueError('/ not allowed in batch name')
        self.batch_name = batch_name
        self.batch_dir = crab_dirs_root(batch_name) # JMTBAD rename -- what crab3 calls workArea
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
        os.system('mkdir -p /tmp/%s' % self.username)

        self.git_status_dir = os.path.join(self.batch_dir, 'gitstatus')
        save_git_status(self.git_status_dir)

        self.testing = testing
        self.max_threads = max_threads  # JMTBAD rename -> processes

        self.cfg_modifier = cfg_modifier

        self.pset_template_fn = pset_template_fn
        self.pset_modifier = pset_modifier

        self.cfg_template = Config()
        self.cfg_template.General.transferLogs = transfer_logs
        self.cfg_template.General.transferOutputs = transfer_outputs
        self.cfg_template.General.workArea = self.batch_dir
        self.cfg_template.JobType.pluginName = 'Analysis'
        # JMTBAD PrivateMC -- also needs cfg.Data.primaryDataset, splitting EventBased, unitsPerJob, totalUnits

        self.dataset = dataset
        self.cfg_template.Data.inputDataset = 'SETLATER'
        self.cfg_template.Data.inputDBS = 'SETLATER'

        self.working_dir_pattern = '%(name)s'
        self.cfg_template.General.requestName = 'SETLATER'

        self.cfg_fn_pattern = os.path.join(self.batch_dir, 'psets/crabConfig.%(name)s.py')
        mkdirs_if_needed(self.cfg_fn_pattern)

        self.pset_fn_pattern = os.path.join(self.batch_dir, 'psets/%(name)s.py')
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

        if storage_site.lower() == 'cornell':
            self.cfg_template.Site.storageSite = 'T3_US_Cornell'
        elif storage_site.lower() == 'fnal':
            self.cfg_template.Site.storageSite = 'T3_US_FNALLPC'
        else:
            self.cfg_template.Site.storageSite = storage_site

        self.cfg_template.Data.publication = bool(publish_name)
        self.cfg_template.Data.publishDataName = publish_name

        if aaa:
            self.cfg_template.Data.ignoreLocality = True
            self.cfg_template.Site.whitelist = self.aaa_locations

        self.modify_pset_hash = modify_pset_hash
        if modify_pset_hash:
            self.modify_pset_hash = str(time.time()) # to avoid multiple tasks publishing into the same dataset

    def cfg(self, sample):
        cfg = deepcopy(self.cfg_template) # JMTBAD needed?
        
        sample.set_curr_dataset(self.dataset) # JMTBAD should this be done in the loop instead?

        cfg.General.requestName = self.batch_name + '_' + self.working_dir_pattern % sample
        cfg.JobType.psetName = self.pset_fn_pattern % sample
        cfg.Data.inputDataset = sample.dataset
        cfg.Data.inputDBS = sample.dbs_inst

        if self.job_control_from_sample:
            sample.job_control(cfg.Data)

        if self.cfg_modifier is not None:
            self.cfg_modifier(cfg, sample)

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
            extra += '\nprocess.dummyForPsetHash = cms.PSet(dummy = cms.string(%r))' % self.modify_pset_hash
        extra += "\nopen(%r, 'wt').write(process.dumpPython())" % pset_fn
        open(pset_orig_fn, 'wt').write(pset + extra)

        out = popen('python %s' % pset_orig_fn)
        open(pset_orig_fn, 'wt').write(pset)

        return pset_orig_fn, pset_fn, pset

    def submit(self, sample):
        print 'batch %s, submit sample %s' % (self.batch_name, sample.name)

        cleanup = [] # not so much to clean up any more

        cfg_fn, cfg = self.cfg(sample)
        pset_orig_fn, pset_fn, pset = self.pset(sample)

        assert pset_fn.endswith('.py')
        cleanup.append(pset_fn + 'c')

        result = {'stdout': 'Not run'}

        if not self.testing:
            working_dir = os.path.join(cfg.General.workArea, 'crab_' + cfg.General.requestName)

            if not os.path.isdir(working_dir):
                result = crab_command('submit', config = cfg)
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
            for sample in samples:
                result = self.submit(sample, **kwargs)
                stdout = result['stdout']
                del result['stdout']
                print stdout,
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
