#!/usr/bin/env python

import os, sys

script_template = '''#!/bin/sh
echo mfvo2t script starting on `date`
echo mfvo2t script args: $argv
echo wd: `pwd`

export JOB_NUM=$1

echo get trees
xrdcp root://cmseos.fnal.gov//store/user/tucker/all_trees_17879f2d0db8123dbf443e3b6613c4c3c0ba1d2f.tgz all_trees.tgz
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

export mfvo2t_seed=$JOB_NUM
export mfvo2t_ntoys=1
export mfvo2t_toythrower_allow_cap=1
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
return_data=1

[CRAB]
jobtype=cmssw
scheduler=%(scheduler)s
'''

compiled = 'nocompile' in sys.argv
setuped = False

def submit(njobs, min_ntracks, signal_sample, samples):
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
        

    batch_name = 'Ntk%i_SigTmp%s_SigSam%s_Sam%s' % (min_ntracks,
                                                    'def',
                                                    'no' if signal_sample is None else 'n%ix%i' % signal_sample,
                                                    samples)

    env = [
        'toythrower_min_ntracks=%i' % min_ntracks,
        ]

    if signal_sample is not None:
        sig_samp, sig_scale = signal_sample
        assert sig_samp < 0
        env.append('toythrower_injected_signal=%i' % sig_samp)
        env.append('toythrower_injected_signal_scale=%f' % sig_scale)
        env.append('toythrower_template_signal=%i' % sig_samp)

    if type(samples) == int:
        env.append('toythrower_sample_only=%i' % samples)
    elif type(samples) == str and '500' in samples:
        env.append('toythrower_use_qcd500=1')

    env = '\n'.join('export mfvo2t_' + e for e in env)
    open('runme.csh', 'wt').write(script_template % {'env': env})
    open('crab.cfg', 'wt').write(crab_cfg % locals())
    os.system('crab -create -submit all')

batches = []
for min_ntracks in (5,6,7,8):
    for signal_sample in (None, (-9, 1), (-9, 10), (-15, 1), (-15, 10)):
        batches.append((min_ntracks, signal_sample, ''))

raw_input('%i batches = %i jobs?' % (len(batches), len(batches)*200))
for batch in batches[:1]:
    submit(200, *batch)

'''
grep -L 'Normal termination (return value 0)' *.condor
tar --remove-files -czf condor_logs.tgz *.condor


find . -name \*.stderr -size 0
find . -name \*.stderr -size +0
rm *.stderr


less 0.stdout

foreach x (*.stdout)
  sed --in-place -e 's@condor/execute/dir_[0-9]*@@g' $x
end

touch diffstdouts
foreach x (stdout*)
  foreach y (stdout*)
    if ($x != $y) then
      diff $x $y >> diffstdouts
    endif
  end
end
sort -o diffstdouts diffstdouts

tar --remove-files -czf stdouts.tgz stdout.*

hadd.py one2two_all.root *.one2two.root
hadd.py o2tfit_all.root *.o2tfit.root

mkdir in
mv signal_templates.root fit.exe one2two.py lib.tgz py.tgz runme.* in/

mkdir outs
mv *.out.* outs/

mkdir roots
mv *.root roots/


py ~/test/One2Two draw.py roots/one2two_0.root
...
mv plots/one2two plots/one2two_`basename $PWD`
'''
