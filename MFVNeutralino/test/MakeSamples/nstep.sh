#!/bin/bash

#exec 2>&1

for fn in gensim.py rawhlt.py reco.py ntuple.py minitree.py; do
    if [[ -e $fn ]]; then
        ./todoify.sh $fn > temp
        mv temp $fn
    fi
done

JOBNUM=$1
MAXEVENTS=$2
export DUMMYFORHASH=$(echo $3 | cut -d = -f 2) # crab scriptArgs requires a =
MINITREES=$(echo $4 | cut -d = -f 2)
TODO=$5
TODO2=$6

INDIR=$(pwd)
OUTDIR=$(pwd)

eval $(scram unsetenv -sh)

echo JOBNUM: ${JOBNUM}
echo MAXEVENTS: ${MAXEVENTS}
echo DUMMYFORHASH: ${DUMMYFORHASH}
echo MINITREES: ${MINITREES}
echo TODO: ${TODO}
echo TODO2: ${TODO2}

################################################################################

echo
echo START GENSIM

(
scram project -n GENSIM CMSSW CMSSW_7_1_21_patch2
cd GENSIM/src
eval $(scram runtime -sh)
cd ../..

echo cmsRun
cmsRun gensim.py \
    jobnum=${JOBNUM} \
    ${MAXEVENTS} \
    ${TODO} \
    2>&1

EXITCODE=${PIPESTATUS[0]}
if [ $EXITCODE -eq 0 ]; then
    gzip RandomEngineState.xml
    mv RandomEngineState.xml.gz RandomEngineState_GENSIM.xml.gz
    echo GENSIM ls -l
    ls -l
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

################################################################################

echo START RAWHLT

(
scram project -n RAWHLT CMSSW CMSSW_7_6_1
cd RAWHLT/src
eval $(scram runtime -sh)
cd ../..

echo cmsRun
cmsRun rawhlt.py ${TODO2} 2>&1

EXITCODE=${PIPESTATUS[0]}
if [ $EXITCODE -eq 0 ]; then
    gzip RandomEngineState.xml
    mv RandomEngineState.xml.gz RandomEngineState_RAWHLT.xml.gz
    echo RAWHLT ls -l
    ls -l
fi

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
cd CMSSW_7_6_3_patch2/src
eval $(scram runtime -sh)
cd ../..

echo cmsRun
cmsRun -j tempfjr.xml reco.py ${TODO2} 2>&1

EXITCODE=${PIPESTATUS[0]}
if [ $EXITCODE -eq 0 ]; then
    echo RECO ls -l
    ls -l
fi

python fixfjr.py

if [ $EXITCODE -ne 0 ]; then
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  echo @@@@ cmsRun exited RECO step with error code $EXITCODE
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  exit $EXITCODE
fi

echo END RECO

################################################################################

if [[ $MINITREES -eq 1 ]]; then
    echo START NTUPLE+MINITREE

    echo "process.source.fileNames = ['file:reco.root']" >> ntuple.py
    echo "process.maxEvents.input = -1" >> ntuple.py
    echo cmsRun ntuple.py
    cmsRun ntuple.py ${TODO2} 2>&1

    EXITCODE=${PIPESTATUS[0]}
    if [ $EXITCODE -eq 0 ]; then
        echo NTUPLE ls -l
        ls -l

        echo "process.source.fileNames = ['file:ntuple.root']" >> minitree.py
        echo "process.maxEvents.input = -1" >> minitree.py
        echo cmsRun minitree.py
        cmsRun -j tempfjr.xml minitree.py ${TODO2} 2>&1
        EXITCODE=${PIPESTATUS[0]}
        python fixfjr.py
        if [ $EXITCODE -eq 0 ]; then
            echo MINITREE ls -l
            ls -l
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
