#!/bin/bash

for fn in lhe.py gensim.py rawhlt.py reco.py ntuple.py minitree.py; do
    if [[ -e $fn ]]; then
        ./todoify.sh $fn > temp
        mv temp $fn
    fi
done

JOBNUM=$1
MAXEVENTS=$2
SALT=$3
FROMLHE=$(echo $4 | cut -d = -f 2)
export DUMMYFORHASH=$(echo $5 | cut -d = -f 2) # crab scriptArgs requires a =
OUTPUTLEVEL=$(echo $6 | cut -d = -f 2)
TODO=$7
TODO2=$8

INDIR=$(pwd)
OUTDIR=$(pwd)

echo JOBNUM: ${JOBNUM}
echo MAXEVENTS: ${MAXEVENTS}
echo SALT: ${SALT}
echo FROMLHE: ${FROMLHE}
echo DUMMYFORHASH: ${DUMMYFORHASH}
echo OUTPUTLEVEL: ${OUTPUTLEVEL}
echo TODO: ${TODO}
echo TODO2: ${TODO2}

################################################################################

eval $(scram unsetenv -sh)

################################################################################

if [[ $FROMLHE -eq 1 ]]; then
    echo
    echo START LHE

    (
    scram project -n LHE CMSSW CMSSW_7_1_16_patch1
    cd LHE/src
    eval $(scram runtime -sh)
    cd ../..

    echo cmsRun
    cmsRun lhe.py \
        salt=${SALT} \
        jobnum=${JOBNUM} \
        ${MAXEVENTS} \
        ${TODO} \
        2>&1

    EXITCODE=${PIPESTATUS[0]}
    exit $EXITCODE
    )

    EXITCODE=$?
    if [ $EXITCODE -ne 0 ]; then
      echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      echo @@@@ cmsRun exited LHE step with error code $EXITCODE
      echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      exit $EXITCODE
    fi

    echo END LHE
fi

################################################################################

echo
echo START GENSIM

(
scram project -n GENSIM CMSSW CMSSW_7_1_21_patch2
cd GENSIM/src
eval $(scram runtime -sh)
cd ../..

echo cmsRun
cmsRun -j tempfjr.xml gensim.py \
    fromlhe=${FROMLHE} \
    salt=${SALT} \
    jobnum=${JOBNUM} \
    ${MAXEVENTS} \
    ${TODO} \
    2>&1

EXITCODE=${PIPESTATUS[0]}

if [[ $FROMLHE -eq 1 ]]; then
    python fixfjr.py
fi

exit $EXITCODE
)

EXITCODE=$?
if [ $EXITCODE -ne 0 ]; then
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  echo @@@@ cmsRun exited GENSIM step with error code $EXITCODE
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  exit $EXITCODE
fi

echo END GENSIM

if [[ $OUTPUTLEVEL == "gensim" ]]; then
    echo OUTPUTLEVEL told me to exit
    exit 0
fi

################################################################################

echo START RAWHLT

(
scram project -n RAWHLT CMSSW CMSSW_8_0_21
cd RAWHLT/src
eval $(scram runtime -sh)
cd ../..

echo cmsRun
cmsRun rawhlt.py \
    salt=${SALT} \
    jobnum=${JOBNUM} \
    ${TODO2} \
    2>&1

EXITCODE=${PIPESTATUS[0]}
exit $EXITCODE
)

EXITCODE=$?
if [ $EXITCODE -ne 0 ]; then
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  echo @@@@ cmsRun exited RAWHLT step with error code $EXITCODE
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  exit $EXITCODE
fi

echo END RAWHLT

################################################################################

echo START RECO
cd CMSSW_8_0_25/src
eval $(scram runtime -sh)
cd ../..

echo cmsRun
cmsRun -j tempfjr.xml reco.py ${TODO2} 2>&1

EXITCODE=${PIPESTATUS[0]}

python fixfjr.py

if [ $EXITCODE -ne 0 ]; then
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  echo @@@@ cmsRun exited RECO step with error code $EXITCODE
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  exit $EXITCODE
fi

echo END RECO

################################################################################

if [[ $OUTPUTLEVEL == "minitree" ]]; then
    echo START NTUPLE+MINITREE

    echo "process.source.fileNames = ['file:reco.root']" >> ntuple.py
    echo "process.maxEvents.input = -1" >> ntuple.py
    echo cmsRun ntuple.py
    cmsRun ntuple.py ${TODO2} 2>&1

    EXITCODE=${PIPESTATUS[0]}
    if [ $EXITCODE -eq 0 ]; then
        echo NTUPLE nevents $(edmEventSize -v ntuple.root | grep Events)

        echo "process.source.fileNames = ['file:ntuple.root']" >> minitree.py
        echo "process.maxEvents.input = -1" >> minitree.py
        echo cmsRun minitree.py
        cmsRun -j tempfjr.xml minitree.py ${TODO2} 2>&1
        EXITCODE=${PIPESTATUS[0]}
        python fixfjr.py
        if [ $EXITCODE -eq 0 ]; then
            echo MINITREE nevents $(python -c "import sys; sys.argv.append('-b'); import ROOT; f=ROOT.TFile('minitree.root'); print f.Get('tre33/t').GetEntries(), f.Get('tre44/t').GetEntries(), f.Get('mfvMiniTree/t').GetEntries()")
        fi
    fi

    if [ $EXITCODE -ne 0 ]; then
      echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      echo @@@@ cmsRun exited NTUPLE+MINITREE step with error code $EXITCODE
      echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      exit $EXITCODE
    fi

    echo END NTUPLE+MINITREE
fi
