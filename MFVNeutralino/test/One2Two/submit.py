# this script must be run from One2Two/

import sys, os, shutil, time
from JMTucker.Tools.general import save_git_status
from JMTucker.Tools.CondorSubmitter import CondorSubmitter
import ROOT; ROOT.gROOT.SetBatch()
import limitsinput

# The combine tarball is made in a locally checked-out combine
# environment so the worker nodes don't have to git clone, etc.
#
# In this CMSSW environment, run
#   cmsMakeTarball.py --standalone dummyarg > ~/tarball.py
#
# Set up combine *on a SL7 machine* following
# http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/
# Directly for this version:
#
#   export SCRAM_ARCH=slc7_amd64_gcc700
#   cmsrel CMSSW_10_2_13
#   cd CMSSW_10_2_13/src
#   cmsenv
#   git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
#   cd HiggsAnalysis/CombinedLimit
#   patch -p1 < path/to/main/cmssw/src/JMTucker/MFVNeutralino/test/One2Two/patchSetHint
#   git fetch origin
#   git checkout v8.0.1
#   scram b clean; scram b
#
# In that same combine environment, make the tarball with:
#   python ~/tarball.py --include-bin combine.tgz
# Copy the tarball to eos, hopefully with a versioned name,
# and update the url below.

script_template = '''#!/bin/bash
echo combine script starting at $(date) with args $*

REALJOB=$1
mapfile -t JOBMAP < cs_jobmap
export JOB=${JOBMAP[$REALJOB]}
export WHICH=$2
export WD=$(pwd)

source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc700
scram project CMSSW CMSSW_10_2_13 2>&1 >/dev/null
cd CMSSW_10_2_13/src
eval `scram runtime -sh`

cd ..
xrdcp -s root://cmseos.fnal.gov//store/user/tucker/combine_sl7_801_patchSetHint.tgz combine.tgz
if [[ ! -f combine.tgz ]]; then
    >&2 echo could not copy combine tarball
    exit 1
fi
tar xf combine.tgz
scram b 2>&1 >/dev/null
hash -r
which combine

cd $WD

{
    echo "========================================================================="
    echo datacard:
    python datacard.py $WHICH __DATACARDARGS__ > datacard.txt
    awk '{ print "DATACARD: " $0 }' datacard.txt

    hint=$(awk '/hint/ { print $NF }' datacard.txt)
    # don't use -H AsymptoticLimits, at least don't do it for low-efficiency signals, it can lead to way too low limits
    cmd="combine --setTheHint $hint -M MarkovChainMC --noDefaultPrior=0 --tries 20 -b 200 --iteration 100000 datacard.txt"

    if [[ $JOB == 0 ]]; then
        echo "========================================================================="
        echo Observed limit
        eval $cmd
        mv higgsCombine*root observed.root

#       echo "========================================================================="
#       echo Observed limit, no systematics
#       eval $cmd -S0
#       mv higgsCombine*root observed_S0.root
    fi
    # this lets us use cs_status to find missing files later but the _S0,, other extra files that are made by commented out lines aren't taken care of! 
    touch observed_${JOB}.root

    ntoys=100
    seedbase=13068931

    echo "========================================================================="
    echo Expected limits
    eval $cmd --toys $ntoys --saveToys -s $((JOB+seedbase))
    mv higgsCombine*root expected_${JOB}.root

#   echo "========================================================================="
#   echo Expected limits, no systematics
#   eval $cmd -S0 --toys $ntoys --saveToys -s $((JOB+seedbase))
#   mv higgsCombine*root expected_S0_${JOB}.root

########################################################################

#   cmd="combine -M GoodnessOfFit --algo=saturated datacard.txt"
#
#   if [[ $JOB == 0 ]]; then
#       echo "========================================================================="
#       echo GoodnessOfFit observed
#       eval $cmd
#       mv higgsCombine*root gof_observed.root
#
#       echo "========================================================================="
#       echo GoodnessOfFit observed, no systematics
#       eval $cmd -S0
#       combine -S0 -M GoodnessOfFit datacard.txt --algo=saturated
#       mv higgsCombine*root gof_S0_observed.root
#   fi
#
#   echo "========================================================================="
#   echo GoodnessOfFit expected
#   eval $cmd --toys $ntoys -s $((JOB+seedbase))
#   mv higgsCombine*root gof_expected_${JOB}.root
#
#   echo "========================================================================="
#   echo GoodnessOfFit expected, no systematics
#   eval $cmd -S0 --toys ntoys -s $((JOB+seedbase))
#   mv higgsCombine*root gof_S0_expected_${JOB}.root

########################################################################

#   cmd="combine -M Significance datacard.txt"
#
#   if [[ $JOB == 0 ]]; then
#       echo "========================================================================="
#       echo Observed significance
#       eval $cmd
#       mv higgsCombine*root signif_observed.root
#       
#       echo "========================================================================="
#       echo Observed significance, no systematics
#       eval $cmd -S0
#       mv higgsCombine*root signif_observed_S0.root
#   fi
#
#   echo "========================================================================="
#   echo Expected significance
#   eval $cmd --toys $ntoys -saveToys -s $((JOB+seedbase))
#   mv higgsCombine*root signif_expected_${JOB}.root
#
#   echo "========================================================================="
#   echo Expected significances, no systematics
#   eval $cmd -S0 --toys $ntoys -saveToys -s $((JOB+seedbase))
#   mv higgsCombine*root signif_expected_S0_${JOB}.root
} 2>&1 | gzip -c > combine_output_${JOB}.txtgz
'''

if 'save_toys' not in sys.argv:
    script_template = script_template.replace(' --saveToys', '')

datacard_args = []

bkg_correlation = [x for x in ['bkg_fully_correlated', 'bkg_yearwise_correlated', 'bkg_binwise_correlated', 'bkg_mixed_correlated', 'bkg_fully_correlated'] if x in sys.argv]
assert len(bkg_correlation) <= 1
if bkg_correlation:
    datacard_args.append(bkg_correlation[0])

include_2016 = 'include_2016' in sys.argv
if include_2016:
    datacard_args.append('include_2016')

script_template = script_template.replace('__DATACARDARGS__', ' '.join(datacard_args))

njobs = 50

jdl_template = '''universe = vanilla
Executable = run.sh
arguments = $(Process) %(isample)s
Output = stdout.$(Process)
Error = stderr.$(Process)
Log = log.$(Process)
stream_output = true
stream_error  = false
notification  = never
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
transfer_input_files = %(input_files)s,cs_jobmap
+REQUIRED_OS = "rhel7"
+DesiredOS = REQUIRED_OS
Queue %(njobs)s
'''

batch_root = '/home/tucker/crab_dirs/combine_output_%i' % time.time()
if os.path.isdir(batch_root):
    raise IOError('%s exists' % batch_root)
print batch_root
os.mkdir(batch_root)
os.mkdir(os.path.join(batch_root, 'inputs'))

save_git_status(os.path.join(batch_root, 'gitstatus'))

input_files = []
for x in ['signal_efficiency.py', 'datacard.py', 'limitsinput.root']:
    nx = os.path.abspath(os.path.join(batch_root, 'inputs', os.path.basename(x)))
    shutil.copy2(x, nx)
    input_files.append(nx)
input_files = ','.join(input_files)

f = ROOT.TFile('limitsinput.root')

years = ('2016','2017','2018') if include_2016 else ('2017','2018')
samples = limitsinput.sample_iterator(f,
                                      require_years=years,
                                      test='test_batch' in sys.argv,
                                      slices_1d='slices_1d' in sys.argv,
                                      )
names = set(s.name for s in samples)
allowed = [arg for arg in sys.argv if arg in names]

for sample in samples:
    if allowed and sample.name not in allowed:
        continue

    #if sample.isample < -700:
    #    continue

    print sample.isample, sample.name,
    isample = sample.isample # for locals use below

    batch_dir = os.path.join(batch_root, 'signal_%05i' % sample.isample)
    os.mkdir(batch_dir)
    open(os.path.join(batch_dir, 'nice_name'), 'wt').write(sample.name)

    run_fn = os.path.join(batch_dir, 'run.sh')
    open(run_fn, 'wt').write(script_template % locals())

    open(os.path.join(batch_dir, 'cs_dir'), 'wt')
    open(os.path.join(batch_dir, 'cs_jobmap'), 'wt').write('\n'.join(str(i) for i in xrange(njobs)) + '\n')
    open(os.path.join(batch_dir, 'cs_submit.jdl'), 'wt').write(jdl_template % locals())
    open(os.path.join(batch_dir, 'cs_njobs'), 'wt').write(str(njobs))
    open(os.path.join(batch_dir, 'cs_outputfiles'), 'wt').write('observed.root expected.root combine_output.txtgz')

    CondorSubmitter._submit(batch_dir, njobs)

# zcat signal_*/combine_output* | sort | uniq | egrep -v '^median expected limit|^mean   expected limit|^Observed|^Limit: r|^Generate toy|^Done in|random number generator seed is|^   ..% expected band|^DATACARD:' | tee /tmp/duh
