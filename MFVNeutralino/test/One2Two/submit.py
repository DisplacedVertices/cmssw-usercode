#!/usr/bin/env python

import os, sys

batch_root = 'crab/One2Two'
dummy_pset_fn = os.path.join(batch_root, 'dummy_pset.py')
os.system('mkdir -p %s' % batch_root)

script_template = '''#!/bin/sh
echo script starting on `date`
echo script args: $argv
echo wd: `pwd`

setenv JMT_WD `pwd`
setenv JOB_NUM $1

echo get trees
xrdcp root://cmseos.fnal.gov//store/user/tucker/all_trees.tgz .

echo untar trees
tar zxvf all_trees.tgz
echo

echo ROOTSYS: $ROOTSYS
echo root-config: `root-config --libdir --version`

echo pwd `pwd`
echo ls -la
ls -la
echo

export mfvo2t_seed=$JOB_NUM
export mfvo2t_ntoys=1
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

gunzip crab_fjr.gz
mv crab_fjr $RUNTIME_AREA/crab_fjr_${JOB_NUM}.xml

#mv mfvo2t.root mfvo2t_${JOB_NUM}.root
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
additional_input_files=mfvo2t.exe,signal_templates.root,crab_fjr.gz
return_data=1

[CRAB]
jobtype=cmssw
scheduler=remoteGlidein
'''

compiled = 'nocompile' in sys.argv
def compile():
    global compiled
    if not compiled:
        if os.system('./compile') != 0:
            raise 'no compile'
        raw_input('did the compile go OK?')
        compiled = True

def submit(njobs, min_ntracks, signal_sample, samples):
    compile()

    batch_root = 'crab/One2Two'
    dummy_pset_fn = os.path.join(batch_root, 'dummy_pset.py')
    open(dummy_pset_fn, 'wt').write(dummy_pset)

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
        env.append('toythrower_signal=%i' % sig_samp)
        env.append('toythrower_signal_scale=%f' % sig_scale)

    if type(samples) == int:
        env.append('toythrower_sample_only=%i' % samples)
    elif type(samples) == str and '500' in samples:
        env.append('toythrower_use_qcd500=1')

    env = '\n'.join('export mfvo2t_' + e for e in env)
    open('runme.csh', 'wt').write(script_template % {'env': env})
    open('crab.cfg', 'wt').write(crab_cfg % locals())
    os.system('crab -create -submit all')

batches = []
for min_ntracks in (5,6,7):
    for signal_sample in (None, (-9, 1), (-9, 10)):
        batches.append((min_ntracks, signal_sample, ''))

raw_input('%i batches = %i jobs?' % (len(batches), len(batches)*200))
for batch in batches[:1]:
    submit(20, *batch)

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
