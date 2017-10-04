import sys, os, shutil, time
from JMTucker.Tools.general import save_git_status
from JMTucker.Tools.CondorSubmitter import CondorSubmitter
import smallsigscan

# the combine tarball is made in a locally checked-out combine environment so the worker nodes don't have to git clone, etc.
# take JMTucker/Tools/scripts/cmsMakeTarball.py, insert make_tarball in it so it can run standalone, then *in the combine environment* do
#   ./cmsMakeTarball.py --include-bin combine.tz

script_template = '''#!/bin/bash
echo combine script starting at $(date) with args $*

export JOB=$1
export WHICH=$2
export WD=$(pwd)

source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc530
scram project CMSSW CMSSW_8_1_0 2>&1 >/dev/null
cd CMSSW_8_1_0/src
eval `scram runtime -sh`

cd ..
xrdcp -s root://cmseos.fnal.gov//store/user/tucker/combine_810.tgz combine.tgz
tar xf combine.tgz
scram b 2>&1 >/dev/null
hash -r
which combine

cd $WD

{
    echo "========================================================================="
    echo datacard:
    python datacard.py $WHICH | tee datacard.txt

    echo "========================================================================="
    echo GoodnessOfFit observed
    combine -M GoodnessOfFit datacard.txt --algo=saturated
    mv higgsCombine*root gof_observed.root

    echo "========================================================================="
    echo GoodnessOfFit expected
    combine -M GoodnessOfFit datacard.txt --algo=saturated --toys 100
    mv higgsCombine*root gof_expected.root

    echo "========================================================================="
    echo GoodnessOfFit observed, no systematics
    combine -S0 -M GoodnessOfFit datacard.txt --algo=saturated
    mv higgsCombine*root gof_S0_observed.root

    echo "========================================================================="
    echo GoodnessOfFit expected, no systematics
    combine -S0 -M GoodnessOfFit datacard.txt --algo=saturated --toys 100
    mv higgsCombine*root gof_S0_expected.root

    echo "========================================================================="
    echo Observed limit
    combine -M BayesianToyMC datacard.txt
    mv higgsCombine*root observed.root

    echo "========================================================================="
    echo Expected limits
    combine -M BayesianToyMC datacard.txt --toys 100
    mv higgsCombine*root expected.root

    echo "========================================================================="
    echo Observed limit, no systematics
    combine -S0 -M BayesianToyMC datacard.txt
    mv higgsCombine*root observed_S0.root

    echo "========================================================================="
    echo Expected limits, no systematics
    combine -S0 -M BayesianToyMC datacard.txt --toys 100
    mv higgsCombine*root expected_S0.root

    echo "========================================================================="
    echo Observed significance
    combine -M Significance datacard.txt
    mv higgsCombine*root signif_observed.root

    echo "========================================================================="
    echo Expected limits
    combine -M Significance datacard.txt --toys 100
    mv higgsCombine*root signif_expected.root

    echo "========================================================================="
    echo Observed limit, no systematics
    combine -S0 -M Significance datacard.txt
    mv higgsCombine*root signif_observed_S0.root

    echo "========================================================================="
    echo Expected limits, no systematics
    combine -S0 -M Significance datacard.txt --toys 100
    mv higgsCombine*root signif_expected_S0.root
} 2>&1 | gzip -c > combine_output.txt.gz
'''

jdl_template = '''universe = vanilla
Executable = run.sh
arguments = $(Process) %(sample_num)s
Output = stdout.$(Process)
Error = stderr.$(Process)
Log = log.$(Process)
stream_output = true
stream_error  = false
notification  = never
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
transfer_input_files = %(input_files)s
Queue 1
'''

batch_root = '/uscms_data/d2/tucker/crab_dirs/combine_output_%i' % time.time()
if os.path.isdir(batch_root):
    raise IOError('%s exists' % batch_root)
os.mkdir(batch_root)
os.mkdir(os.path.join(batch_root, 'inputs'))

save_git_status(os.path.join(batch_root, 'gitstatus'))

input_files = []
for x in ['combine/datacard.py', 'limits_input.root']:
    nx = os.path.abspath(os.path.join(batch_root, 'inputs', os.path.basename(x)))
    shutil.copy2(x, nx)
    input_files.append(nx)
input_files = ','.join(input_files)

for sample_num in smallsigscan.sample_nums:
    nice = smallsigscan.num2name[sample_num]
    print sample_num, nice,

    batch_dir = os.path.join(batch_root, 'signal_%05i' % sample_num)
    os.mkdir(batch_dir)
    open(os.path.join(batch_dir, 'nice_name'), 'wt').write(nice)

    run_fn = os.path.join(batch_dir, 'run.sh')
    open(run_fn, 'wt').write(script_template % locals())

    open(os.path.join(batch_dir, 'cs_dir'), 'wt')
    open(os.path.join(batch_dir, 'cs_submit.jdl'), 'wt').write(jdl_template % locals())

    CondorSubmitter._submit(batch_dir, 1)
