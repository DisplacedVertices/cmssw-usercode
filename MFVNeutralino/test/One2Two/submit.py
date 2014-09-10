#!/usr/bin/env python

import os, sys

script_template = '''#!/bin/sh
echo mfvo2t script starting on `date`
echo mfvo2t script args: $argv
echo wd: `pwd`

export JOB_NUM=$1

echo get trees
xrdcp root://cmseos.fnal.gov//store/user/tucker/all_trees_3c359678f94253163d849d8f53e4e5e65dddd79c.tgz all_trees.tgz
ECODE=$?
if [ "$ECODE" -ne "0" ]; then
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  echo @@@@ xrdcp of trees failed
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  exit $ECODE
fi
echo

echo untar trees
tar zxvf all_trees.tgz
ECODE=$?
if [ "$ECODE" -ne "0" ]; then
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  echo @@@@ untar failed
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  exit $ECODE
fi
echo

echo ROOTSYS: $ROOTSYS
echo root-config: `root-config --libdir --version`

echo pwd `pwd`
echo ls -la
ls -la
echo

export mfvo2t_no_progressbar=1
export mfvo2t_seed=$JOB_NUM
export mfvo2t_ntoys=1
export mfvo2t_toythrower_allow_cap=1
export mfvo2t_phishift_find_f_dz=0
%(env)s

echo run mfvo2t.exe
./mfvo2t.exe
ECODE=$?
if [ "$ECODE" -ne "0" ]; then
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  echo @@@@ mfvo2t.exe exited with error code $ECODE
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  exit $ECODE
fi
echo mfvo2t.exe done
echo

cat > $RUNTIME_AREA/crab_fjr_${JOB_NUM}.xml << EOF
<FrameworkJobReport>
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
process = cms.Process('One2Two')
process.source = cms.Source('EmptySource')
'''

crab_cfg = '''
[CMSSW]
events_per_job=1
number_of_jobs=%(njobs)s
pset=%(dummy_pset_fn)s
datasetpath=None
output_file=mfvo2t.root

[USER]
script_exe=runme.csh
ui_working_dir=%(batch_root)s/crab_%(batch_name)s
ssh_control_persist=no
additional_input_files=mfvo2t.exe
copy_data=1
publish_data_name=mfvo2t_%(batch_name)s
publish_data=1
dbs_url_for_publication=phys03
storage_element=T3_US_Cornell

[CRAB]
jobtype=cmssw
scheduler=%(scheduler)s
'''

compiled = 'nocompile' in sys.argv
setuped = False

def submit(njobs, template_type, min_ntracks, signal_sample, template_signal, samples):
    global compiled
    global setuped

    if not compiled:
        if os.system('./compile -O2') != 0:
            raise 'no compile'
        raw_input('did the compile go OK?')
        compiled = True

    scheduler = 'condor' if 'condor' in sys.argv else 'remoteGlidein'
    batch_root = 'crab/One2Two'
    if scheduler == 'condor':
        batch_root += '_condor'
    dummy_pset_fn = os.path.join(batch_root, 'dummy_pset.py')

    if not setuped:
        os.system('mkdir -p %s' % batch_root)
        open(dummy_pset_fn, 'wt').write(dummy_pset)
        setuped = True
        

    batch_name = 'Tmp%s_Ntk%i_SigTmp%s_SigSam%s_Sam%s' % (template_type,
                                                          min_ntracks,
                                                          template_signal,
                                                          'no' if signal_sample is None else 'n%ix%i' % signal_sample,
                                                          samples)

    env = [
        'toythrower_min_ntracks=%i' % min_ntracks,
        'toythrower_template_signal=%i' % template_signal,
        ]

    if template_type == 'PS':
        env.append('templates_kind=phishift')
        env.append('fitter_start_nuis0=2')
        env.append('fitter_start_nuis1=0.003')
    elif template_type == 'SC':
        env.append('templates_kind=simpleclear')
        env.append('fitter_fix_nuis1=1')
        env.append('fitter_start_nuis0=10')
        env.append('fitter_start_nuis1=0')

    if signal_sample is not None:
        sig_samp, sig_scale = signal_sample
        assert sig_samp < 0
        env.append('toythrower_injected_signal=%i' % sig_samp)
        env.append('toythrower_injected_signal_scale=%f' % sig_scale)

    if type(samples) == int:
        env.append('toythrower_sample_only=%i' % samples)
    elif type(samples) == str and '500' in samples:
        env.append('toythrower_use_qcd500=1')

    env = '\n'.join('export mfvo2t_' + e for e in env)
    open('runme.csh', 'wt').write(script_template % {'env': env})
    open('crab.cfg', 'wt').write(crab_cfg % locals())
    os.system('crab -create -submit all')


batches = []
for template_type in ('CJ',):
    for min_ntracks in (5,): #6): #,7,8):
        for signal in xrange(-24, 0):
            for strength in (None, 1, 5, 10):
                sg = (signal, strength) if strength is not None else None
                batches.append((template_type, min_ntracks, sg, signal, ''))
            
nj = 500
raw_input('%i batches = %i jobs?' % (len(batches), len(batches)*nj))
for batch in batches:
    submit(nj, *batch)
