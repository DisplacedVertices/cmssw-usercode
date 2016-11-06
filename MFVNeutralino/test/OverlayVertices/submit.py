#!/usr/bin/env python

import sys, os, shutil
from JMTucker.Tools.CMSSWTools import make_tarball
from JMTucker.Tools.general import save_git_status

pwd = os.getcwd()

batch_name = ''
njobs = 1000

cmssw_py = 'overlay.py'

working_dir = os.path.abspath('/uscms_data/d2/tucker/overlay/' + batch_name)
save_git_status(os.path.join(working_dir, 'gitstatus'))

inputs_dir = os.path.join(working_dir, 'inputs')
outputs_dir = os.path.join(working_dir, 'outputs')
os.makedirs(inputs_dir)
os.makedirs(outputs_dir)

tarball_fn_base = 'input.tgz'
tarball_fn = os.path.join(inputs_dir, tarball_fn_base)
make_tarball(tarball_fn, include_python=True)

cmssw_py_fn = os.path.join(inputs_dir, cmssw_py)
shutil.copy2(cmssw_py, cmssw_py_fn)

sh_fn = os.path.join(inputs_dir, 'run.sh')
jdl_fn = os.path.join(inputs_dir, 'submit.jdl')

scram_arch = os.environ['SCRAM_ARCH']
cmssw_version = os.environ['CMSSW_VERSION']

sh = '''
#!/bin/bash

workdir=$(pwd)
job=$1

echo date: $(date)
echo job: $job
echo pwd: $workdir

export SCRAM_ARCH=%(scram_arch)s
source /cvmfs/cms.cern.ch/cmsset_default.sh

scram project CMSSW %(cmssw_version)s
cd %(cmssw_version)s
tar xvf ${workdir}/%(tarball_fn_base)s
cd src
eval `scram ru -sh`
scram b -j 2

cmsRun ${workdir}/%(cmssw_py)s $job 2>&1
mv overlay*.root $workdir

''' % locals()

open(sh_fn, 'wt').write(sh)
os.chmod(sh_fn, 0755)

jdl = '''
universe = vanilla
Executable = %(sh_fn)s
arguments = $(Process)
Output = overlay_$(Cluster)_$(Process).stdout
Error = overlay_$(Cluster)_$(Process).stderr
Log = overlay_$(Cluster)_$(Process).log
stream_output = false
stream_error  = false
notification  = never
should_transfer_files   = YES
when_to_transfer_output = ON_EXIT
transfer_input_files = %(tarball_fn)s,%(cmssw_py_fn)s
Queue %(njobs)s
''' % locals()

open(jdl_fn, 'wt').write(jdl)

os.chdir(outputs_dir)
os.system('condor_submit < ' + jdl_fn)
os.chdir(pwd)
