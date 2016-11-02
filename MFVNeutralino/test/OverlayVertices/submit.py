#!/usr/bin/env python

import sys, os
from JMTucker.Tools.CMSSWTools import make_tarball

pwd = os.getcwd()

working_dir = os.path.abspath('/uscms_data/d2/tucker/overlay/ttbar_temp')

inputs_dir = os.path.join(working_dir, 'inputs')
outputs_dir = os.path.join(working_dir, 'outputs')
os.makedirs(inputs_dir)
os.makedirs(outputs_dir)

tarball_fn_base = 'input.tgz'
tarball_fn = os.path.join(inputs_dir, tarball_fn_base)
make_tarball(tarball_fn, include_python=True)

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

cmsRun ${workdir}/overlay.py $job 2>&1
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
transfer_input_files = %(tarball_fn)s,%(pwd)s/overlay.py
Queue 1000
''' % locals()

open(jdl_fn, 'wt').write(jdl)

os.chdir(outputs_dir)
os.system('condor_submit < ' + jdl_fn)
os.chdir(pwd)
