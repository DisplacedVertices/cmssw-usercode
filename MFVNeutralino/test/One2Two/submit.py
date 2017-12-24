#!/usr/bin/env python

import os, sys, shutil
from JMTucker.Tools.general import save_git_status

class submitter:
    batch_root = '/uscms_data/d2/tucker/crab_dirs/One2TwoV1p1'
    files_needed = ['mfvo2t.exe', 'filtertee.py', 'vpeffs_2016_v15.root', 'limitsinput.root']
    script_template = '''#!/bin/bash
echo mfvo2t script starting at $(date) with args $*
export JOB=$1
export WD=$(pwd)
echo JOB: $JOB
echo WD: $WD

source /cvmfs/cms.cern.ch/cmsset_default.sh
scram project CMSSW CMSSW_8_0_25 2>&1 >/dev/null
cd CMSSW_8_0_25/src
eval `scram runtime -sh`
cd ../..
echo ROOTSYS: $ROOTSYS

export mfvo2t_no_progressbar=1
export mfvo2t_seed=$JOB
export mfvo2t_ntoys=1
export mfvo2t_templates_save_plots=0
export mfvo2t_fitter_save_plots=0
__ENV__

echo mfvo2t.exe begin at $(date)
set -o pipefail
./mfvo2t.exe | python filtertee.py
EXITCODE=$?
echo mfvo2t.exe exitcode $EXITCODE at $(date)
mv mfvo2t.root mfvo2t_${JOB}.root
exit $EXITCODE
'''

    jdl_template = '''universe = vanilla
Executable = run.sh
arguments = $(Process)
Output = stdout.$(Process)
Error = stderr.$(Process)
Log = log.$(Process)
stream_output = false
stream_error = false
notification = never
transfer_input_files = __INPUT_FILES__
should_transfer_files   = YES
when_to_transfer_output = ON_EXIT
Queue __NJOBS__
'''

    def __init__(self):
        if not os.environ.has_key('ROOTSYS'):
            raise RuntimeError('$ROOTSYS not set?')

        if os.path.isdir(self.batch_root):
            raise IOError('%s exists' % self.batch_root)
        os.mkdir(self.batch_root)

        if not 'nomake' in sys.argv:
            if os.system('make clean; make -j 16') != 0:
                raise RuntimeError('make failed')
            raw_input('did the make go OK?')

        save_git_status(os.path.join(self.batch_root, 'gitstatus'))

        self.inputs_dir = os.path.join(self.batch_root, 'inputs')
        os.mkdir(self.inputs_dir)
        for x in self.files_needed:
            shutil.copy2(x, os.path.join(self.inputs_dir, x))

        self.i_submit = -1

    def submit(self, njobs, bkg_scale, signal_sample, template_signal):
        self.i_submit += 1

        ###

        env = ['toythrower_template_signal=%i' % template_signal]

        if bkg_scale != 1:
            env.append('toythrower_scale_2v=%i' % bkg_scale)

        #if template_signal >= -12 or (template_signal <= -101 and template_signal >= -126):
        #    env.append('fitter_sig_limit_step=1')

        if signal_sample is not None:
            assert type(signal_sample) == tuple
            sig_samp, sig_scale = signal_sample
            assert sig_samp < 0
            if sig_scale < 0: # two special values for running on data.
                env.append('ntoys=0')
                env.append('process_data=1')
                if sig_scale == -2:
                    env.append('seed=1')
                    env.append('fitter_i_limit_job=$JOB')
                    env.append('fitter_do_signif=0')
                else:
                    assert njobs <= 20
            else:
                env.append('fitter_do_limit=0')
                env.append('toythrower_injected_signal=%i' % sig_samp)
                env.append('toythrower_injected_signal_scale=%f' % sig_scale)
        else:
            pass #env.append('fitter_do_limit=0')

        env = '\n'.join('export mfvo2t_' + e for e in env)

        input_files = [os.path.abspath(os.path.join(self.inputs_dir, x)) for x in self.files_needed]
        input_files = ','.join(input_files)

        ###

        batch_name = 'BkgScale%i_SigTmp%s_SigSam%s' % (bkg_scale,
                                                       template_signal,
                                                       'no' if signal_sample is None else 'n%ix%i' % signal_sample)
        batch_dir = os.path.join(self.batch_root, '%05i_%s' % (self.i_submit, batch_name))
        os.mkdir(batch_dir)

        script = self.script_template
        script = script.replace('__ENV__', env)
        script = script.replace('__ROOTSYS__', os.environ['ROOTSYS'])
        script_fn = os.path.join(batch_dir, 'run.sh')
        open(script_fn, 'wt').write(script)

        jdl = self.jdl_template
        jdl = jdl.replace('__INPUT_FILES__', input_files)
        jdl = jdl.replace('__NJOBS__', str(njobs))
        open(os.path.join(batch_dir, 'submit.jdl'), 'wt').write(jdl)

        open(os.path.join(batch_dir, 'cs_dir'), 'wt')
        open(os.path.join(batch_dir, 'njobs'), 'wt').write(str(njobs))

        pwd = os.getcwd()
        os.chdir(batch_dir)
        os.system('condor_submit submit.jdl')
        os.chdir(pwd)

###

if 1:
    sig_first = [-15, -21, -9, -6]
    signals = sig_first + sorted(set(range(-24, 0)) - set(sig_first))

    strengths = (-1, -2, None, 1, 5, 25, 100)
    strengths = (None, 1, 5, 25, 100)
    signals = [-39,-46,-53,-60]

    batches = []

    for bkg_scale in (1, 10):
        for strength in strengths:
            for signal in signals:
                sg = (signal, strength) if strength is not None else None
                njobs = 20 if strength == -1 else 500
                batches.append((njobs, bkg_scale, sg, signal))

    s = submitter()
    for batch in batches:
        #print batch
        s.submit(*batch)
