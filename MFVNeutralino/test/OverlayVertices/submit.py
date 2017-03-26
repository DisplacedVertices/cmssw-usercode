#!/usr/bin/env python

import sys, os, shutil
from textwrap import dedent
from JMTucker.Tools.CMSSWTools import make_tarball
from JMTucker.Tools.general import save_git_status
from JMTucker.MFVNeutralino.Year import year

pwd = os.getcwd()

def int_ceil(x,y):
    return (x+y-1)/y

per = 50
max_njobs = dict([(x, (int_ceil(y, per), per if y%per == 0 else y%per)) for x,y in [
            (('ttbar', 3), 17085),
            (('ttbar', 4), 2313),
            (('ttbar', 5), 307),
            (('ttbar_2015', 3), 13399),
            (('ttbar_2015', 4), 1811),
            (('ttbar_2015', 5), 226),
            (('qcdht0700sum', 3), 6442),
            (('qcdht0700sum', 4), 966),
            (('qcdht0700sum', 5), 123),
            (('qcdht1000sum', 3), 63348),
            (('qcdht1000sum', 4), 8907),
            (('qcdht1000sum', 5), 1421),
            (('qcdht1500sum', 3), 93828),
            (('qcdht1500sum', 4), 14576),
            (('qcdht1500sum', 5), 2630),
            (('qcdht2000sum', 3), 60612),
            (('qcdht2000sum', 4), 10444),
            (('qcdht2000sum', 5), 2191),
            (('qcdht0700sum_2015', 3), 4571),
            (('qcdht0700sum_2015', 4), 600),
            (('qcdht0700sum_2015', 5), 84),
            (('qcdht1000sum_2015', 3), 40505),
            (('qcdht1000sum_2015', 4), 5427),
            (('qcdht1000sum_2015', 5), 885),
            (('qcdht1500sum_2015', 3), 59671),
            (('qcdht1500sum_2015', 4), 8930),
            (('qcdht1500sum_2015', 5), 1798),
            (('qcdht2000sum_2015', 3), 41121),
            (('qcdht2000sum_2015', 4), 6835),
            (('qcdht2000sum_2015', 5), 1422),
            ]])

def submit(sample, ntracks, overlay_args, njobs=0, testing=False, batch_name_ex=''):
    if njobs <= 0:
        njobs, per_last = max_njobs[(sample, ntracks)]
    else:
        per_last = per
    njobs_m1 = njobs - 1
    per_m1 = per - 1
    per_last_m1 = per_last - 1

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
    
    batch_dir = '/uscms_data/d2/tucker/OverlayV1_%i/%s/%s' % (year, batch_name, sample)
    
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
    
    scram project CMSSW %(cmssw_version)s 2>&1 > /dev/null
    scramexit=$?
    if [[ $scramexit -ne 0 ]]; then
        echo scram exited with code $scramexit
        exit $scramexit
    fi

    cd %(cmssw_version)s
    tar xf ${workdir}/%(tarball_fn_base)s
    cd src
    eval `scram ru -sh`
    scram b -j 2 2>&1 > /dev/null

    if [[ $job -eq %(njobs_m1)i ]]; then
        nev=%(per_last_m1)i
    else
        nev=%(per_m1)i
    fi

    set -x
    for i in $(seq 0 $nev); do
        cmsRun ${workdir}/%(cmssw_py)s +batch +which-event $((job*50+i)) +sample %(sample)s +ntracks %(ntracks)s %(overlay_args)s 2>&1
        cmsexit=$?
        if [[ $cmsexit -ne 0 ]]; then
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

if year == 2015:
    samples = ['qcdht0700sum_2015', 'qcdht1000sum_2015', 'qcdht1500sum_2015', 'qcdht2000sum_2015', 'ttbar_sum']
elif year == 2016:
    samples = ['qcdht0700sum', 'qcdht1000sum', 'qcdht1500sum', 'qcdht2000sum', 'ttbar']

overlay_argses = ['', '+z-model deltasvgaus', '+rest-of-event', '+rest-of-event +z-model deltasvgaus']
for overlay_args in overlay_argses:
    for sample in samples:
        for ntracks in [3,4,5]:
            submit(sample, ntracks, overlay_args)
            print
