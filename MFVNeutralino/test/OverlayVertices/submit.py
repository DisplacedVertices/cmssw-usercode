#!/usr/bin/env python

import sys, os, shutil
from textwrap import dedent
from JMTucker.Tools.CMSSWTools import make_tarball
from JMTucker.Tools.general import save_git_status

pwd = os.getcwd()

def int_ceil(x,y):
    return (x+y-1)/y

max_njobs = dict([(x, int_ceil(y, 10)) for x,y in [
            (('qcdht1000', 3), 13371),
            (('qcdht1000', 4), 1841),
            (('qcdht1000', 5), 237),
            (('qcdht1500', 3), 20009),
            (('qcdht1500', 4), 2936),
            (('qcdht1500', 5), 454),
            (('qcdht2000', 3), 13656),
            (('qcdht2000', 4), 2310),
            (('qcdht2000', 5), 335),
            (('ttbar', 3), 13398),
            (('ttbar', 4), 1811),
            (('ttbar', 5), 194),
            ]])

def submit(sample, ntracks, overlay_args, njobs=1000, testing=False, batch_name_ex=''):
    njobs = min(max_njobs[(sample, ntracks)], njobs)

    batch_name = 'ntk%i' % ntracks
    if 'deltasvgaus' in overlay_args:
        batch_name += '_deltasvgaus'
    if 'rest-of-event' in overlay_args:
        batch_name += '_wevent'
    batch_name += batch_name_ex
    if testing:
        batch_name += '_TEST'

    print batch_name, sample

    cmssw_py = 'overlay.py'
    
    batch_dir = '/uscms_data/d2/tucker/overlay/%s/%s' % (batch_name, sample)
    
    inputs_dir = os.path.join(batch_dir, 'inputs')
    outputs_dir = os.path.join(batch_dir, 'outputs')
    os.makedirs(inputs_dir)
    os.makedirs(outputs_dir)
    
    save_git_status(os.path.join(batch_dir, 'gitstatus'))
    
    tarball_fn_base = 'input.tgz'
    tarball_fn = os.path.join(inputs_dir, tarball_fn_base)
    make_tarball(tarball_fn, include_python=True)
    
    cmssw_py_fn = os.path.join(inputs_dir, cmssw_py)
    shutil.copy2(cmssw_py, cmssw_py_fn)
    
    sh_fn = os.path.join(inputs_dir, 'run.sh')
    jdl_fn = os.path.join(inputs_dir, 'submit.jdl')
    
    scram_arch = os.environ['SCRAM_ARCH']
    cmssw_version = os.environ['CMSSW_VERSION']
    
    sh = dedent('''
    #!/bin/bash
    
    workdir=$(pwd)
    job=$1
    
    echo date: $(date)
    echo job: $job
    echo pwd: $workdir
    
    export SCRAM_ARCH=%(scram_arch)s
    source /cvmfs/cms.cern.ch/cmsset_default.sh
    
    scram project CMSSW %(cmssw_version)s 2>&1
    cd %(cmssw_version)s
    tar xvf ${workdir}/%(tarball_fn_base)s
    cd src
    eval `scram ru -sh`
    scram b -j 2

    set -x
    for i in {0..9}; do
        cmsRun ${workdir}/%(cmssw_py)s +which-event $((job*10+i)) +sample %(sample)s +ntracks %(ntracks)s %(overlay_args)s 2>&1
        cmsexit=$?
        if [[ $cmsexit -eq 65 ]]; then
            echo looks like we are out of events
            break
        elif [[ $cmsexit -ne 0 ]]; then
            echo cmsRun exited with code $cmsexit
            exit $cmsexit
        fi
    done
    set +x
    hadd overlay.root overlay_*.root 2>&1
    haddexit=$?
    if [[ $haddexit -ne 0 ]]; then
        echo hadd exited with code $haddexit
        exit $haddexit
    fi
    mv overlay.root $workdir/overlay_${job}.root
    ''' % locals())

    open(sh_fn, 'wt').write(sh)
    os.chmod(sh_fn, 0755)
    
    jdl = dedent('''
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
    ''' % locals())
    
    open(jdl_fn, 'wt').write(jdl)

    if not testing:
        os.chdir(outputs_dir)
        os.system('condor_submit < ' + jdl_fn)
        os.chdir(pwd)

for sample in ['qcdht1000', 'qcdht1500', 'qcdht2000', 'ttbar']:
    for ntracks in [3,4,5]:
        overlay_args = '+rest-of-event'
        overlay_args = '+rest-of-event +z-model deltasvgaus'
        overlay_args = '+z-model deltasvgaus'
        overlay_args = ''
        submit(sample, ntracks, overlay_args, njobs=3000)
