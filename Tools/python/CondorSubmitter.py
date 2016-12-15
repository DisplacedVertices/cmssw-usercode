#!/usr/bin/env python

import sys, os, string, shutil, base64, zlib, cPickle as pickle
from JMTucker.Tools.CMSSWTools import make_tarball
from JMTucker.Tools.CRAB3ToolsBase import crab_dirs_root, crab_renew_proxy_if_needed
from JMTucker.Tools.general import mkdirs_if_needed, popen, save_git_status, int_ceil, touch

if not os.environ.has_key('SCRAM_ARCH') or not os.environ.has_key('CMSSW_VERSION'):
    raise EnvironmentError('CMSSW environment not set?')

class CondorSubmitter:
    sh_template = '''#!/bin/bash

workdir=$(pwd)
job=$1

echo job $job start at $(date)

export SCRAM_ARCH=__SCRAM_ARCH__
source /cvmfs/cms.cern.ch/cmsset_default.sh

scram project CMSSW __CMSSW_VERSION__ 2>&1 > /dev/null
scramexit=$?
if [[ $scramexit -ne 0 ]]; then
    echo scram exited with code $scramexit
    exit $scramexit
fi

cd __CMSSW_VERSION__
tar xf ${workdir}/input.tgz
cd src
eval `scram ru -sh`
scram b -j 2 2>&1 > /dev/null

echo cmsRun start at $(date)
cp $workdir/{cs.json,cs_filelist.py} .
echo $job > cs_job
cmsRun -j ${workdir}/fjr_${job}.xml ${workdir}/cs_pset.py 2>&1
cmsexit=$?
echo cmsRun end at $(date)
echo cmsRun exited with code $cmsexit
if [[ $cmsexit -ne 0 ]]; then
    exit $cmsexit
fi

for x in *.root; do
    mv $x ${workdir}/$(basename $x .root)_${job}.root
done
''' \
.replace('__SCRAM_ARCH__',    os.environ['SCRAM_ARCH']) \
.replace('__CMSSW_VERSION__', os.environ['CMSSW_VERSION'])

    jdl_template = '''
universe = vanilla
Executable = __SH_FN__
arguments = $(Process)
Output = stdout.$(Process)
Error = stderr.$(Process)
Log = log.$(Process)
stream_output = false
stream_error = false
notification = never
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
transfer_input_files = __TARBALL_FN__,cs_pset.py,cs_filelist.py,cs.json
Queue __NJOBS__
'''

    pset_end_template = '''
####

import os
from JMTucker.Tools.general import typed_from_argv

cs_job = int(open('cs_job').read())
assert cs_job >= 0

import cs_filelist
process.source.fileNames = [__PFN_PREFIX__ + x for x in cs_filelist.get(cs_job)]

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.maxLuminosityBlocks = cms.untracked.PSet(input = cms.untracked.int32(-1))

if os.stat('cs.json').st_size > 0:
    from FWCore.PythonUtilities.LumiList import LumiList
    process.source.lumisToProcess = LumiList('cs.json').getVLuminosityBlockRange()
'''

    get_proxy = True

    batch_name_allowed = string.ascii_letters + string.digits + '_'

    def __init__(self,
                 batch_name,
                 testing = 'testing' in sys.argv or 'cs_testing' in sys.argv,
                 pset_template_fn = sys.argv[0],
                 pset_modifier = None,
                 input_files = None,
                 output_files = None,
                 pfn_prefix = 'root://cmseos.fnal.gov/',
                 dataset = 'main',
                 **kwargs):

        for arg in sys.argv:
            if arg.startswith('cs_name='):
                batch_name = arg.replace('cs_name=', '')
                break

        if not set(self.batch_name_allowed).issuperset(set(batch_name)):
            raise ValueError('illegal batch name %s, allowed characters are letters, numbers, and _' % batch_name)

        self.batch_name = batch_name
        self.batch_dir = os.path.abspath(crab_dirs_root(batch_name))
        if os.path.exists(self.batch_dir):
            raise ValueError('batch_dir %s already exists, refusing to clobber' % self.batch_dir)

        if not testing and self.get_proxy:
            print 'CondorSubmitter init: checking proxies, might ask for password twice (but you can skip it with ^C if you know what you are doing).'
            crab_renew_proxy_if_needed()
            self.get_proxy = False

        #self.username = os.environ['USER']
        #os.system('mkdir -p /tmp/%s' % self.username)

        save_git_status(os.path.join(self.batch_dir, 'gitstatus'))

        self.inputs_dir = os.path.join(self.batch_dir, 'inputs')
        os.mkdir(self.inputs_dir)

        self.filelist_fn_pattern = os.path.join(self.inputs_dir, '%(name)s.sh')
        self.jdl_fn_pattern = os.path.join(self.inputs_dir, '%(name)s.jdl')
        self.pset_fn_pattern = os.path.join(self.inputs_dir, '%(name)s.py')

        tarball_fn = os.path.join(self.inputs_dir, 'input.tgz')
        make_tarball(tarball_fn, include_python=True)

        sh_fn = os.path.join(self.inputs_dir, 'run.sh')
        open(sh_fn, 'wt').write(self.sh_template)

        self.jdl_template = self.jdl_template \
            .replace('__TARBALL_FN__', tarball_fn) \
            .replace('__SH_FN__',      sh_fn) \

        self.pset_end_template = self.pset_end_template \
            .replace('__PFN_PREFIX__', repr(pfn_prefix))

        self.testing = testing

        # JMTBAD handle later
        assert input_files is None
        assert output_files is None

        self.dataset = dataset

        self.pset_template_fn = pset_template_fn
        self.pset_modifier = pset_modifier

    def filelist(self, sample, working_dir):
        # JMTBAD are there performance problems by not matching the json to the files per job?
        json_fn = os.path.join(working_dir, 'cs.json')
        if hasattr(sample, 'json'):
            shutil.copy2(sample.json, json_fn)
        else:
            touch(json_fn)
        per = sample.files_per
        nfns = len(sample.filenames)
        njobs = sample.njobs if hasattr(sample, 'njobs') else int_ceil(nfns, per)
        fn_groups = [sample.filenames[i*per:(i+1)*per] for i in xrange(njobs)]
        fn_groups = [x for x in fn_groups if x]
        njobs = len(fn_groups)
        xxx = base64.b64encode(zlib.compress(pickle.dumps(fn_groups, -1)))
        with open(os.path.join(working_dir, 'cs_filelist.py'), 'wt') as f:
            f.write('import zlib, base64, cPickle as pickle\n')
            f.write('_l = pickle.loads(zlib.decompress(base64.b64decode(%r)))\n' % xxx)
            f.write('def get(i):\n    return _l[i]\n\n')
        return njobs

    def pset(self, sample, working_dir):
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

        pset += self.pset_end_template
        pset_fn = os.path.join(working_dir, 'cs_pset.py')
        open(pset_fn, 'wt').write(pset)
        return pset_fn

    def submit(self, sample):
        print 'batch', self.batch_name, 'sample', sample.name, 

        try:
            sample.set_curr_dataset(self.dataset)
        except KeyError:
            print "\033[1m warning: \033[0m sample %s not submitted, doesn't have dataset %s" % (sample.name, self.dataset)
            return result

        working_dir = os.path.join(self.batch_dir, 'condor_%s' % sample.name)
        os.mkdir(working_dir)
        touch(os.path.join(working_dir, 'cs_dir'))

        njobs = self.filelist(sample, working_dir)
        pset_fn = self.pset(sample, working_dir)

        jdl_fn = os.path.join(working_dir, 'cs_submit.jdl')
        open(jdl_fn, 'wt').write(self.jdl_template.replace('__NJOBS__', str(njobs)))

        cwd = os.getcwd()
        
        if not self.testing:
            os.chdir(working_dir)
            try:
                submit_out, submit_ret = popen('condor_submit < cs_submit.jdl', return_exit_code=True)
                ok = False
                for line in submit_out.split('\n'):
                    if 'job(s) submitted to cluster' in line:
                        ok = True
                        line = line.split()
                        try:
                            njobs_sub = int(line[0])
                            cluster = int(line[-1][:-1])
                            open(os.path.join(working_dir, 'njobs'), 'wt').write(str(njobs_sub))
                            open(os.path.join(working_dir, 'cluster'), 'wt').write(str(cluster))
                            if njobs_sub != njobs:
                                ok = False
                        except ValueError:
                            ok = False
                if not ok:
                    print '\033[1m problem! \033[0m'
                    print submit_out
                else:
                    print 'success! cluster', cluster
            finally:
                os.chdir(cwd)
        else:
            print 'in testing mode, not submitting anything.'
            diff_out, diff_ret = popen('diff -uN %s %s' % (self.pset_template_fn, pset_fn), return_exit_code=True)
            if diff_ret != 0:
                print '.py diff:\n---------'
                print diff_out
                raw_input('continue?')
                print

    def submit_all(self, samples):
        for sample in samples:
            self.submit(sample)
