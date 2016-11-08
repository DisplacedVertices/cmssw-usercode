#!/usr/bin/env python

import sys, os, shutil, gzip
from textwrap import dedent
from JMTucker.Tools.CMSSWTools import make_tarball
from JMTucker.Tools.general import save_git_status

pwd = os.getcwd()

def int_ceil(x,y):
    return (x+y-1)/y

def submit(sample, testing=False):
    per = 10
    batch_name = sample
    file_list_fn = os.path.abspath('filelist.%s.gz' % sample)
    event_list_fn = os.path.abspath('vetolist.%s.gz' % sample)
    nfiles = sum(1 for line in gzip.open(file_list_fn))
    njobs = int_ceil(nfiles, per)

    if testing:
        batch_name += '_TEST'
        njobs = 1

    print batch_name

    cmssw_py = 'pick_by_veto.py'

    root_name = 'pick1vtx'
    batch_root = os.path.join('/uscms_data/d2/tucker/condor_batch', root_name)
    batch_dir = os.path.abspath(os.path.join(batch_root, batch_name))
    
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

    out_xrd = 'root://cmseos.fnal.gov/'
    out_path = '/store/user/tucker/pick1vtx/%s' % sample
    if os.system('eos %s mkdir -p %s' % (out_xrd, out_path)) != 0:
        raise IOError('problem making %s' % out_path)

    if any(os.system('eos %s ls %s/pick_%i.root 2>&1 > /dev/null' % (out_xrd, out_path, i)) == 0 for i in xrange(njobs)):
        raise IOError('one or more output files already exist')

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
    cd $workdir
    
    cmsRun %(cmssw_py)s +job $job +per %(per)s +sample %(sample)s 2>&1
    cmsexit=$?
    if [[ $cmsexit -ne 0 ]]; then
        echo cmsRun exited with code $cmsexit
        exit $cmsexit
    fi

    new_fn=${out_xrd}${out_path}/pick_${job}.root
    echo xrdcp to $new_fn
    xrdcp pick.root $new_fn
    xrdcpexit=$?
    if [[ $xrdcpexit -ne 0 ]]; then
        echo xrdcp exited with code $xrdcpexit
        exit $xrdcpexit
    fi
    ''' % locals())
    
    open(sh_fn, 'wt').write(sh)
    os.chmod(sh_fn, 0755)
    
    jdl = dedent('''
    universe = vanilla
    Executable = %(sh_fn)s
    arguments = $(Process)
    Output = %(root_name)s_%(batch_name)s_$(Cluster)_$(Process).stdout
    Error = %(root_name)s_%(batch_name)s_$(Cluster)_$(Process).stderr
    Log = %(root_name)s_%(batch_name)s_$(Cluster)_$(Process).log
    stream_output = false
    stream_error  = false
    notification  = never
    should_transfer_files   = YES
    when_to_transfer_output = ON_EXIT
    transfer_input_files = %(tarball_fn)s,%(cmssw_py_fn)s,%(file_list_fn)s,%(event_list_fn)s
    Queue %(njobs)s
    ''' % locals())
    
    open(jdl_fn, 'wt').write(jdl)

    if not testing or testing == 'run':
        os.chdir(outputs_dir)
        os.system('condor_submit < ' + jdl_fn)
        os.chdir(pwd)

samples = ['qcdht1000', 'qcdht2000'] # , 'qcdht1500']
for sample in samples:
    submit(sample, testing='run')
