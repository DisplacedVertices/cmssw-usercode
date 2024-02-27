#!/usr/bin/env python

import platform, sys, os, string, shutil, time, base64, zlib, imp, cPickle as pickle
from datetime import datetime, timedelta
from JMTucker.Tools.CMSSWTools import make_tarball, find_output_files
from JMTucker.Tools.CRAB3ToolsBase import crab_dirs_root, crab_renew_proxy_if_needed
from JMTucker.Tools.CondorTools import cs_timestamp
from JMTucker.Tools.general import mkdirs_if_needed, popen, save_git_status, int_ceil, touch

if not os.environ.has_key('SCRAM_ARCH') or not os.environ.has_key('CMSSW_VERSION'):
    raise EnvironmentError('CMSSW environment not set?')

class CondorSubmitter:
    sh_template = '''#!/bin/bash

workdir=$(pwd)
realjob=$1
mapfile -t jobmap < cs_jobmap
job=${jobmap[$realjob]}

echo realjob $realjob job $job start at $(date)

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

mkdir $workdir/subworkdir
cd $workdir/subworkdir

cp $workdir/{cs_njobs,cs.json,cs_filelist.py,cs_cmsrun_args,cs_primaryds,cs_samplename,cs_timestamp__INPUT_BNS__} .
echo $job > cs_job

echo meat start at $(date)
__MEAT__
echo meat end at $(date)
echo meat exited with code $meatexit
if [[ $meatexit -ne 0 ]]; then
    exit $meatexit
fi

__OUTPUT_SNIPPET__
''' \
.replace('__SCRAM_ARCH__',    os.environ['SCRAM_ARCH']) \
.replace('__CMSSW_VERSION__', os.environ['CMSSW_VERSION'])

    cmsRun_meat = '''
cmsRun -j ${workdir}/fjr_${job}.xml ${workdir}/cs_pset.py $(<cs_cmsrun_args) 2>&1
meatexit=$?
'''

    output_template = '''
for x in __OUTPUT_BNS__; do
    xext="${x##*.}"
    xname="${x%.*}"
    xwjob=${xname}_${job}.${xext}
    mv $x ${workdir}/${xwjob}
done
'''
    stageout_template = '''
xrdcp_problem=0
touch publish
for x in __STAGEOUT_BNS__; do
    xext="${x##*.}"
    xname="${x%.*}"
    xwjob=${xname}_${job}.${xext}
    dest=__STAGEOUT_PATH__/${xwjob}
    xrdcp -s $x $dest
    if [[ $? -ne 0 ]]; then
        echo xrdcp problem with ${xwjob}
        xrdcp_problem=1
    else
        echo $dest >> publish
    fi
done

mv publish ${workdir}/publish_${job}.txt

if [[ $xrdcp_problem -ne 0 ]]; then
    exit 60307
fi
''' # 60307 will show up as unix code 147

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
transfer_input_files = __TARBALL_FN__,cs_jobmap,cs_njobs,cs_pset.py,cs_filelist.py,cs.json,cs_cmsrun_args,cs_primaryds,cs_samplename,cs_timestamp__INPUT_FNS__
x509userproxy = $ENV(X509_USER_PROXY)
__EXTRAS__
Queue __NJOBS__
'''

    pset_end_template = '''
####

import os

cs_job = int(open('cs_job').read())
assert cs_job >= 0

cs_fail = __FAIL_LIST__
assert cs_job not in cs_fail

import cs_filelist
if __SPLIT_BY_EVENTS__:
    if process.source.type_() != 'EmptySource':
        process.source.fileNames = [__PFN_PREFIX__ + x for x in cs_filelist.get(0)]
        process.source.skipEvents = cms.untracked.uint32(cs_job * __EVENTS_PER__)
    process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(__MAX_EVENTS__ if __MAX_EVENTS__ != -1 else __EVENTS_PER__))
else:
    if process.source.type_() != 'EmptySource':
        process.source.fileNames = [__PFN_PREFIX__ + x for x in cs_filelist.get(cs_job)]
    process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(__MAX_EVENTS__))

process.maxLuminosityBlocks = cms.untracked.PSet(input = cms.untracked.int32(-1))

if os.stat('cs.json').st_size > 0:
    from FWCore.PythonUtilities.LumiList import LumiList
    process.source.lumisToProcess = LumiList('cs.json').getVLuminosityBlockRange()
'''

    filelist_py_template = '''
import zlib, base64, cPickle as pickle
_l = pickle.loads(zlib.decompress(base64.b64decode('__FILELIST__')))
def get(i): return _l[i]
'''

    submit_host = platform.node()
    get_proxy = True
    batch_name_allowed = string.ascii_letters + string.digits + '_'
    if submit_host == 'login.uscms.org':
        links_dir = None
    else:
        links_dir = os.path.abspath(crab_dirs_root('cs_links'))
    schedds = []

    if links_dir:
        if not os.path.isdir(links_dir):
            os.mkdir(links_dir)

        if submit_host.endswith('fnal.gov'):
            schedds = ['lpcschedd%i.fnal.gov' % i for i in 1,2,3,4,5,6]
            for schedd in schedds:
                schedd_d = os.path.join(links_dir, schedd)
                if not os.path.isdir(schedd_d):
                    os.mkdir(schedd_d)

    def __init__(self,
                 batch_name,
                 ex = '',
                 testing = 'testing' in sys.argv or 'cs_testing' in sys.argv,
                 meat = cmsRun_meat,
                 pset_template_fn = sys.argv[0],
                 pset_modifier = None,
                 input_files = [],
                 output_files = [],
                 skip_output_files = [],
                 stageout_files = [], # can be "all" or "pool"
                 stageout_path = '', # if / in it, does not try to generate
                 publish_name = '',
                 dataset = 'main',
                 jdl_extras = '',
                 _events = -1,
                 _njobs = None,
                 _fail = [],
                 ):

        self.nsubmits = -1

        self.testing = testing

        if type(meat) == file:
            meat = meat.read()
        elif type(meat) == str and os.path.isfile(meat):
            meat = open(meat).read()
        if 'meatexit=' not in meat:
            raise ValueError('meatexit not set in meat?')
        self.meat = meat
        self.is_cmsRun = meat == self.cmsRun_meat

        if '$' in pset_template_fn:
            pset_template_fn =  os.path.expandvars(pset_template_fn)
        if '~' in pset_template_fn:
            pset_template_fn = os.path.expanduser(pset_template_fn)
        self.pset_template_fn = pset_template_fn
        self.pset_modifier = pset_modifier
        self.dataset = dataset
        self._njobs = _njobs

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

        if ex:
            ex = str(ex) + '_'
        self.ex_str = 'ex_%s%s' % (ex, str(int(time.time()*1000)))

        self.batch_name = batch_name
        self.batch_dir = os.path.abspath(crab_dirs_root(batch_name))
        self.inputs_dir = os.path.join(self.batch_dir, self.ex_str, 'inputs')
        if os.path.exists(self.inputs_dir): # check inputs_dir instead of batch_dir since we might be from metasubmitter
            raise ValueError('batch_dir %s already exists, refusing to clobber' % self.batch_dir)

        if not testing and self.get_proxy:
            #print 'CondorSubmitter init: checking proxies, might ask for password twice (but you can skip it with ^C if you know what you are doing).'
            crab_renew_proxy_if_needed()
            self.get_proxy = False

        username = os.environ['USER']
        self.timestamp = datetime.now()
        #os.system('mkdir -p /tmp/%s' % username)

        #print 'CondorSubmitter init: saving git status'
        save_git_status(os.path.join(self.batch_dir, self.ex_str, 'gitstatus'))

        os.mkdir(self.inputs_dir)

        self.filelist_fn_pattern = os.path.join(self.inputs_dir, '%(name)s.sh')
        self.jdl_fn_pattern = os.path.join(self.inputs_dir, '%(name)s.jdl')
        self.pset_fn_pattern = os.path.join(self.inputs_dir, '%(name)s.py')

        tarball_fn = os.path.join(self.inputs_dir, 'input.tgz')
        #print 'CondorSubmitter init: making cmssw tarball'
        make_tarball(tarball_fn, include_python=True, include_interface=True)

        sh_fn = os.path.join(self.inputs_dir, 'run.sh')

        if input_files:
            input_bns = []
            input_fns = []
            for x in input_files:
                bn = os.path.basename(x)
                fn = os.path.abspath(os.path.join(self.inputs_dir, bn))
                input_bns.append(bn)
                input_fns.append(fn)
                shutil.copy(x, fn)
            input_bns = ',' + ','.join(input_bns)
            input_fns = ',' + ','.join(input_fns)
        else:
            input_bns = ''
            input_fns = ''

        # JMTBAD if pset_modifier or cmsrun_args modifies the output filenames, we won't catch them
        #print 'CondorSubmitter init: importing pset_template fn %s to get output filenames' % pset_template_fn
        module_output_files = {}
        if self.pset_template_fn:
            module = imp.load_source('dummy', self.pset_template_fn)
            module_output_files = find_output_files(module.process)
            for l in module_output_files.itervalues():
                for x in l:
                    if x not in skip_output_files:
                        output_files.append(x)

        if type(stageout_files) == str:
            stageout_which = stageout_files
            if stageout_which == 'all':
                stageout_files = output_files
            elif stageout_which == 'pool':
                stageout_files = [x for x in module_output_files.get('PoolOutputModule', []) if x not in skip_output_files]
            else:
                raise ValueError("don't understand stageout_files = %s" % stageout_which)
        output_files = [x for x in output_files if x not in stageout_files]

        for x in output_files + stageout_files:
            if os.path.basename(x) != x:
                raise ValueError('output file must have no slashes: %r' % x)
        self.output_files   = output_files   = ' '.join(output_files)
        self.stageout_files = stageout_files = ' '.join(stageout_files)

        output_snippet = ''

        if output_files:
            #print 'CondorSubmitter init: output files are', output_files
            output_snippet += self.output_template.replace('__OUTPUT_BNS__', output_files)

        if stageout_files:
            if '/' not in stageout_path:
                stageout_user = username # JMTBAD use getUsernameFromSiteDB?
                if stageout_path:
                    stageout_path = '/' + stageout_path
                stageout_path = 'root://cmseos.fnal.gov//store/user/' + stageout_user + stageout_path
                if not publish_name:
                    publish_name = batch_name.replace('/', '_')
                stageout_path += '/$(<cs_primaryds)/' + publish_name + '/$(<cs_timestamp)/$(printf "%04i" $(($job/1000)) )'

            #print 'CondorSubmitter init: stageout files are', stageout_files
            #print 'CondorSubmitter init: stageout path is', stageout_path

            output_snippet += self.stageout_template \
                .replace('__STAGEOUT_BNS__',  stageout_files) \
                .replace('__STAGEOUT_PATH__', stageout_path)

        self.sh_template = self.sh_template \
            .replace('__INPUT_BNS__',  input_bns) \
            .replace('__MEAT__', self.meat) \
            .replace('__OUTPUT_SNIPPET__', output_snippet)

        self.jdl_template = self.jdl_template \
            .replace('__SH_FN__',      sh_fn) \
            .replace('__TARBALL_FN__', tarball_fn) \
            .replace('__INPUT_FNS__',  input_fns) \
            .replace('__EXTRAS__',     jdl_extras)

        self.pset_end_template = self.pset_end_template \
            .replace('__MAX_EVENTS__', str(_events)) \
            .replace('__FAIL_LIST__', repr(_fail))

        open(sh_fn, 'wt').write(self.sh_template)

    def normalize_fns(self, fns):
        # JMTBAD fall back to global redirector
        return ['root://cmseos.fnal.gov/' + x for x in fns if x.startswith('/store')]

    def filelist(self, sample, working_dir):
        # JMTBAD are there performance problems by not matching the json to the files per job?
        json_fn = os.path.join(working_dir, 'cs.json')
        if hasattr(sample, 'json') and sample.json:
            shutil.copy2(sample.json, json_fn)
        else:
            touch(json_fn)

        filenames = sample.filenames
        if not self.is_cmsRun:
            filenames = self.normalize_fns(filenames)

        if sample.split_by == 'events':
            per = sample.events_per
            assert sample.nevents_orig > 0 or sample.total_events > 0
            nevents = sample.total_events if sample.total_events > 0 else sample.nevents_orig
            njobs = int_ceil(nevents, per)
            fn_groups = [filenames]
        else:
            use_njobs = sample.files_per < 0
            per = abs(sample.files_per)
            if sample.total_files > 0:
                filenames = filenames[:sample.total_files]
            njobs = getattr(sample, 'njobs', int_ceil(len(filenames), per))
            fn_groups = [x for x in (filenames[i*per:(i+1)*per] for i in xrange(njobs)) if x]
            if not use_njobs:
                njobs = len(fn_groups) # let it fail downward
        if self._njobs is not None:
            assert self._njobs <= njobs
            njobs = self._njobs

        encoded_filelist = base64.b64encode(zlib.compress(pickle.dumps(fn_groups, -1)))

        files_to_write = [
            ('cs_outputfiles',   self.output_files),
            ('cs_stageoutfiles', self.stageout_files),
            ('cs_filelist.py',   self.filelist_py_template.replace('__FILELIST__', encoded_filelist)),
            ('cs_njobs',         str(njobs)),
            ('cs_jobmap',        '\n'.join(str(i) for i in xrange(njobs)) + '\n'), # will be more complicated for resubmits
            ('cs_primaryds',     sample.primary_dataset),
            ('cs_samplename',    sample.name),
            ('cs_timestamp',     (self.timestamp + timedelta(seconds=self.nsubmits)).strftime('%y%m%d_%H%M%S')),
            ]

        for fn, content in files_to_write:
            open(os.path.join(working_dir, fn), 'wt').write(content)

        return njobs

    def pset(self, sample, working_dir):
        cmsrun_args_fn = os.path.join(working_dir, 'cs_cmsrun_args')
        cmsrun_args = sample.cmsrun_args if hasattr(sample, 'cmsrun_args') else ''
        if type(cmsrun_args) == list:
            cmsrun_args = ' '.join(cmsrun_args)
        open(cmsrun_args_fn, 'wt').write(cmsrun_args)

        pset = ''
        if self.pset_template_fn:
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

        pset_end_template = self.pset_end_template \
            .replace('__PFN_PREFIX__', repr(sample.xrootd_url)) \
            .replace('__EVENTS_PER__', str(sample.events_per)) \
            .replace('__SPLIT_BY_EVENTS__', str(sample.split_by == 'events'))

        pset += pset_end_template
        pset_fn = os.path.join(working_dir, 'cs_pset.py')
        open(pset_fn, 'wt').write(pset)
        return pset_fn

    @classmethod
    def _submit(cls, working_dir, njobs):
        cwd = os.getcwd()
        os.chdir(working_dir)
        try:
            submit_out, submit_ret = popen('condor_submit < cs_submit.jdl', return_exit_code=True)
            ok = False
            cluster = None
            schedd = None
            if cls.schedds:
                for line in submit_out.split('\n'):
                    if line.startswith('Attempting to submit jobs to '):
                        schedd = line.strip().replace('Attempting to submit jobs to ', '')
                        assert schedd in cls.schedds
            for line in submit_out.split('\n'):
                if 'job(s) submitted to cluster' in line:
                    ok = True
                    line = line.split()
                    try:
                        njobs_sub = int(line[0])
                        assert line[-1][-1] == '.'
                        cluster = int(line[-1][:-1])
                        open('njobs', 'wt').write(str(njobs_sub))
                        open('cluster', 'wt').write('%i %s' % (cluster, schedd) if schedd else str(cluster))
                        if njobs_sub != njobs:
                            ok = False
                    except ValueError:
                        ok = False
            if ok and not cluster:
                print '\033[1m problem, ok but no cluster? \033[0m'
            if not ok:
                print '\033[1m problem! \033[0m'
                print submit_out
            else:
                if schedd:
                    cluster_s = '%s:%s' % (schedd, cluster)
                    if cls.links_dir:
                        cluster_link = os.path.join(cls.links_dir, schedd, str(cluster))
                else:
                    cluster_s = cluster
                    if cls.links_dir:
                        cluster_link = os.path.join(cls.links_dir, str(cluster))
                print '\x1b[92msuccess!\x1b[0m %s' % cluster_s
                if cls.links_dir:
                    if os.path.islink(cluster_link):
                        print 'warning: clobbering old link:', os.readlink(cluster_link)
                        os.unlink(cluster_link)
                    os.symlink(os.path.abspath(working_dir), cluster_link)
        finally:
            os.chdir(cwd)

    def submit(self, sample):
        self.nsubmits += 1
        print 'submit', self.batch_name, sample.name,

        if self.dataset:
            try:
                sample.set_curr_dataset(self.dataset)
            except KeyError:
                print "\033[1m warning: \033[0m sample %s not submitted, doesn't have dataset %s" % (sample.name, self.dataset)
                return

        if sample.split_by == 'events' and not sample.is_mc:
            print "\033[1m warning: \033[0m sample %s not submitted because can't split by events on data sample"
            return

        working_dir = os.path.join(self.batch_dir, 'condor_%s' % sample.name)
        if os.path.exists(working_dir):
            print "\033[1m warning: \033[0m sample %s not submitted, working dir %s already exists" % (sample.name, working_dir)
            return

        os.mkdir(working_dir)
        touch(os.path.join(working_dir, 'cs_dir'))
        open(os.path.join(working_dir, 'cs_ex'), 'wt').write(self.ex_str)

        njobs = self.filelist(sample, working_dir)
        pset_fn = self.pset(sample, working_dir)

        jdl_fn = os.path.join(working_dir, 'cs_submit.jdl')
        open(jdl_fn, 'wt').write(self.jdl_template.replace('__NJOBS__', str(njobs)))

        if not self.testing:
            self._submit(working_dir, njobs)
        else:
            print 'in testing mode, not submitting anything.'
            if pset_fn:
                diff_out, diff_ret = popen('diff -uN %s %s' % (self.pset_template_fn, pset_fn), return_exit_code=True)
                if diff_ret != 0:
                    print '.py diff:\n---------'
                    print diff_out
                    raw_input('continue?')
                    print

    def submit_all(self, samples):
        for sample in samples:
            self.submit(sample)

def NtupleReader_submit(batch_name, dataset, samples, exe_fn='hists.exe', exe_args='', output_fn='hists.root', split_default=1, split={}):
    meat = '''
job=$(<cs_job)
njobs=$(<cs_njobs)
nfns=$(python -c 'from cs_filelist import _l; print len(_l)')
split=$((njobs/nfns))
fnum=$((job/split))
fn=$(python -c 'from cs_filelist import get; print get('$fnum')[0]')

cmd="./__EXE_FN__ -i $fn -o __OUTPUT_FN__ -n $split -w $((job%split)) __EXE_ARGS__"
if false; then
  echo $cmd
  meatexit=0
  touch __OUTPUT_FN__
else
  $cmd 2>&1
  meatexit=$?
fi
'''\
.replace('__EXE_FN__', exe_fn) \
.replace('__EXE_ARGS__', exe_args) \
.replace('__OUTPUT_FN__', output_fn)

    for sample in samples:
        sample.set_curr_dataset(dataset)
        sample.files_per = -1
        sample.njobs = len(sample.filenames) * getattr(sample, 'nr_split', split.get(sample.name, split_default))

    cs = CondorSubmitter(batch_name=batch_name, dataset=dataset, meat=meat, pset_template_fn='', input_files=[exe_fn], output_files=[output_fn])
    cs.submit_all(samples)
