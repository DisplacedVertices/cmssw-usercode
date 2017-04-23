#!/usr/bin/env python

import sys, os, shutil
from textwrap import dedent
from JMTucker.Tools.CMSSWTools import make_tarball
from JMTucker.Tools.general import save_git_status, popen, touch
from JMTucker.MFVNeutralino.Year import year

pwd = os.getcwd()

def int_ceil(x,y):
    return (x+y-1)/y

per = 50
max_njobs = dict([(x, (int_ceil(y, per), per if y%per == 0 else y%per)) for x,y in [
            (('JetHT2016B3', 3), 19521),
            (('JetHT2016B3', 4), 2125),
            (('JetHT2016C', 3), 8559),
            (('JetHT2016C', 4), 945),
            (('JetHT2016D', 3), 14478),
            (('JetHT2016D', 4), 1659),
            (('JetHT2016E', 3), 8128),
            (('JetHT2016E', 4), 819),
            (('JetHT2016F', 3), 6480),
            (('JetHT2016F', 4), 687),
            (('JetHT2016G', 3), 22317),
            (('JetHT2016G', 4), 2427),
            (('JetHT2016H2', 3), 23550),
            (('JetHT2016H2', 4), 2572),
            (('JetHT2016H3', 3), 643),
            (('JetHT2016H3', 4), 66),
            (('JetHT2015C', 3), 46),
            (('JetHT2015C', 4), 8),
            (('JetHT2015D', 3), 5376),
            (('JetHT2015D', 4), 615),
            (('ttbar', 3), 12257),
            (('ttbar', 4), 1488),
            (('ttbar', 5), 184),
            (('ttbar_2015', 3), 9630),
            (('ttbar_2015', 4), 1156),
            (('ttbar_2015', 5), 122),
            (('qcdht0500sum', 3), 16),
            (('qcdht0500sum', 4), 0),
            (('qcdht0500sum', 5), 0),
            (('qcdht0700sum', 3), 4325),
            (('qcdht0700sum', 4), 531),
            (('qcdht0700sum', 5), 74),
            (('qcdht1000sum', 3), 40603),
            (('qcdht1000sum', 4), 5098),
            (('qcdht1000sum', 5), 789),
            (('qcdht1500sum', 3), 60851),
            (('qcdht1500sum', 4), 8551),
            (('qcdht1500sum', 5), 1552),
            (('qcdht2000sum', 3), 40015),
            (('qcdht2000sum', 4), 6340),
            (('qcdht2000sum', 5), 1337),
            (('qcdht0500sum_2015', 3), 15),
            (('qcdht0500sum_2015', 4), 2),
            (('qcdht0500sum_2015', 5), 0),
            (('qcdht0700sum_2015', 3), 2850),
            (('qcdht0700sum_2015', 4), 325),
            (('qcdht0700sum_2015', 5), 38),
            (('qcdht1000sum_2015', 3), 25123),
            (('qcdht1000sum_2015', 4), 2923),
            (('qcdht1000sum_2015', 5), 470),
            (('qcdht1500sum_2015', 3), 36943),
            (('qcdht1500sum_2015', 4), 5099),
            (('qcdht1500sum_2015', 5), 1040),
            (('qcdht2000sum_2015', 3), 25954),
            (('qcdht2000sum_2015', 4), 3972),
            (('qcdht2000sum_2015', 5), 888),
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
    if 'deltasv' in overlay_args:
        batch_name += '_deltasv'
    if 'no-rest-of-event' in overlay_args:
        batch_name += '_woevent'
    batch_name += batch_name_ex
    if testing:
        batch_name += '_TEST'

    print batch_name, sample

    cmssw_py = 'overlay.py'
    
    batch_dir = '/uscms_data/d2/tucker/OverlayV3_%i/%s/%s' % (year, batch_name, sample)
    
    inputs_dir = os.path.join(batch_dir, 'inputs')
    os.makedirs(inputs_dir)
    
    save_git_status(os.path.join(batch_dir, 'gitstatus'))
    
    tarball_fn_base = 'input.tgz'
    tarball_fn = os.path.join(inputs_dir, tarball_fn_base)
    make_tarball(tarball_fn, include_python=True, include_interface=True)
    
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
        cmsRun ${workdir}/%(cmssw_py)s +which-event $((job*50+i)) +sample %(sample)s +ntracks %(ntracks)s %(overlay_args)s 2>&1
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
    Output = stdout.$(Process)
    Error = stderr.$(Process)
    Log = log.$(Process)
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
        os.chdir(batch_dir)
        submit_out, submit_ret = popen('condor_submit < ' + jdl_fn, return_exit_code=True)
        ok = False
        for line in submit_out.split('\n'):
            if 'job(s) submitted to cluster' in line:
                ok = True
                line = line.split()
                try:
                    njobs_sub = int(line[0])
                    cluster = int(line[-1][:-1])
                    touch(os.path.join(batch_dir, 'cs_dir'))
                    open(os.path.join(batch_dir, 'njobs'), 'wt').write(str(njobs_sub))
                    open(os.path.join(batch_dir, 'cluster'), 'wt').write(str(cluster))
                    if njobs_sub != njobs:
                        ok = False
                except ValueError:
                    ok = False
        if not ok:
            print '\033[1m problem! \033[0m'
            print submit_out
        else:
            print 'success! cluster', cluster
        os.chdir(pwd)

if year == 2015:
    samples = ['qcdht0700sum_2015', 'qcdht1000sum_2015', 'qcdht1500sum_2015', 'qcdht2000sum_2015', 'ttbar_2015']
elif year == 2016:
    samples = ['qcdht0700sum', 'qcdht1000sum', 'qcdht1500sum', 'qcdht2000sum', 'ttbar']

samples = ['qcdht1500sum']

overlay_argses = [''] #['+rest-of-event +z-model deltasvgaus']
for overlay_args in overlay_argses:
    for sample in samples:
        for ntracks in [3,4,5]:
            submit(sample, ntracks, overlay_args)
            print
