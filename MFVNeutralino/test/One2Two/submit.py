#!/usr/bin/env python

import os, sys
from JMTucker.Tools.general import save_git_status

sample_number_to_name = {}
for line in open('signals.h'):
    num, name = line.strip().replace('samples.push_back({', '').replace(', 0, 0});', '').replace(',', '').replace('"', '').split()
    num = int(num)
    #print num, name
    sample_number_to_name[num] = name
#raise 1

script_template = '''#!/bin/sh
echo mfvo2t script starting at $(date) with args $*
echo wd: $(pwd)

export JOB_NUM=$1

echo ROOTSYS: $ROOTSYS
echo root-config: $(root-config --libdir --version)

echo ls -la
ls -la
echo

export mfvo2t_no_progressbar=1
export mfvo2t_seed=$JOB_NUM
export mfvo2t_ntoys=1
export mfvo2t_templates_save_plots=0
export mfvo2t_fitter_save_plots=0
%(env)s

echo run mfvo2t.exe
set -o pipefail
./mfvo2t.exe | python filtertee.py
ECODE=$?
if [ "$ECODE" -ne "0" ]; then
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  echo @@@@ mfvo2t.exe exited with error code $ECODE
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  exit $ECODE
fi
echo mfvo2t.exe done
echo

cat > FrameworkJobReport.xml << EOF
<FrameworkJobReport>
<ReadBranches>
</ReadBranches>
<PerformanceReport>
  <PerformanceSummary Metric="StorageStatistics">
    <Metric Name="Parameter-untracked-bool-enabled" Value="true"/>
    <Metric Name="Parameter-untracked-bool-stats" Value="true"/>
    <Metric Name="Parameter-untracked-string-cacheHint" Value="application-only"/>
    <Metric Name="Parameter-untracked-string-readHint" Value="auto-detect"/>
    <Metric Name="ROOT-tfile-read-totalMegabytes" Value="0"/>
    <Metric Name="ROOT-tfile-write-totalMegabytes" Value="0"/>
  </PerformanceSummary>
</PerformanceReport>

<GeneratorInfo>
</GeneratorInfo>
</FrameworkJobReport>
EOF
'''

dummy_pset = '''
import FWCore.ParameterSet.Config as cms
process = cms.Process('dummy')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.maxLuminosityBlocks = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.source = cms.Source('EmptySource')
'''

crab_cfg = '''
from CRABClient.UserUtilities import config as Config
config = Config()

config.General.transferLogs = True
config.General.transferOutputs = True
config.General.workArea = '%(batch_root)s'
config.General.requestName = '%(batch_name)s'

config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = '%(dummy_pset_fn)s'
config.JobType.scriptExe = 'runme.sh'
config.JobType.inputFiles = %(files_needed)r
config.JobType.outputFiles = ['mfvo2t.root']

config.Data.outputPrimaryDataset = '%(batch_name)s'
config.Site.storageSite = 'T3_US_FNALLPC'
#config.Site.blacklist = ['T3_GR_IASA', 'T3_IT_Napoli']
config.Data.splitting = 'EventBased'

config.Data.unitsPerJob = 1
config.Data.totalUnits = %(njobs)s
config.Data.publication = False
'''

made = 'nomake' in sys.argv
setuped = False

crab_submit_dir = 'to_submit'
if os.path.isdir(crab_submit_dir):
    sys.exit('move to_submit out of the way')
os.mkdir(crab_submit_dir)
i_submit = 0

def submit(njobs, bkg_scale, signal_sample, template_signal):
    global made
    global setuped
    global i_submit

    if not made:
        if os.system('make clean; make -j 16') != 0:
            raise 'no make'
        raw_input('did the make go OK?')
        made = True

    extra_name = ''
    batch_root = '/uscms_data/d2/tucker/crab_dirs/One2TwoV1'
    for x in sys.argv:
        if x.startswith(batch_root):
            extra_name = x.replace(batch_root + '_', '') + '_'
            batch_root = x
            break

    dummy_pset_fn = os.path.join(batch_root, 'dummy_pset.py')

    if not setuped:
        os.system('mkdir -p %s' % batch_root)
        save_git_status(os.path.join(batch_root, 'gitstatus'))
        open(dummy_pset_fn, 'wt').write(dummy_pset)
        setuped = True

    batch_name = '%sBkgScale%i_SigTmp%s_SigSam%s' % (extra_name, bkg_scale, template_signal, 'no' if signal_sample is None else 'n%ix%i' % signal_sample)
    files_needed = [os.path.abspath(x) for x in ['mfvo2t.exe', 'filtertee.py', 'vpeffs_2016_v15.root', 'throwhists.root']]

    env = [
        'toythrower_template_signal=%i' % template_signal,
        ]

    if bkg_scale != 1:
        env.append('toythrower_scale_2v=%i' % bkg_scale)

    #if template_signal >= -12 or (template_signal <= -101 and template_signal >= -126):
    #    env.append('fitter_sig_limit_step=1')

    if signal_sample is not None:
        sig_samp, sig_scale = signal_sample
        assert sig_samp < 0
        if sig_scale < 0:
            env.append('ntoys=0')
            env.append('process_data=1')
            if sig_scale == -2:
                env.append('seed=1')
                env.append('fitter_i_limit_job=$JOB_NUM')
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

    submit_dir = os.path.join(crab_submit_dir, '%05i' % i_submit)
    os.mkdir(submit_dir)
    open(os.path.join(submit_dir, 'runme.sh'), 'wt').write(script_template % locals())
    open(os.path.join(submit_dir, 'crabConfig.py'), 'wt').write(crab_cfg % locals())

    i_submit += 1

###

if 1:
    sig_first = [-15, -21, -9, -6]
    signals = sig_first + sorted(set(range(-24, 0)) - set(sig_first))

    strengths = (-1, -2, None, 1, 5, 25, 100)
    signals = [-39,-46,-53,-60]

    batches = []

    for bkg_scale in (1, 10):
        for strength in strengths:
            for signal in signals:
                sg = (signal, strength) if strength is not None else None
                njobs = 20 if strength == -1 else 500
                batches.append((njobs, sg, signal))

    for batch in batches:
        #print batch
        submit(*batch)
