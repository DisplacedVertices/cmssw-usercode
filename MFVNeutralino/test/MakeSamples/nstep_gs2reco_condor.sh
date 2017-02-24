#!/bin/bash

#exec 2>&1

for fn in rawhlt.py reco.py; do
    if [[ -e $fn ]]; then
        ./todoify.sh $fn > temp
        mv temp $fn
    fi
done

WD=$(pwd)
JOBNUM=$1
OUTPUTDIR=$2
TODOS="$3 $4 $5 $6 $7 $8 $9"

echo WD: $WD
echo JOBNUM: $JOBNUM
echo OUTPUTDIR: $OUTPUTDIR
echo TODOS: $TODOS

################################################################################

echo START RAWHLT

(
scram project -n RAWHLT CMSSW CMSSW_8_0_21
cd RAWHLT/src
eval $(scram runtime -sh)
cp $WD/{inputfns.txt,*.py,*.pkl} .

echo cmsRun
cmsRun -j fjr.xml rawhlt.py ${TODOS} 2>&1

EXITCODE=${PIPESTATUS[0]}
if [ $EXITCODE -eq 0 ]; then
    echo RAWHLT ls -l
    ls -l
    gzip RandomEngineState.xml
    mv RandomEngineState.xml.gz $WD/RandomEngineState_RAWHLT_${JOBNUM}.xml.gz
    gzip fjr.xml
    mv fjr.xml.gz $WD/fjr_RAWHLT_${JOBNUM}.xml.gz
    mv hlt.root $WD/
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

(
scram project -n RECO CMSSW CMSSW_8_0_21
cd RECO/src
eval $(scram runtime -sh)
cp $WD/{reco.py,modify.py} .
mv $WD/hlt.root .

echo cmsRun
cmsRun -j fjr.xml reco.py 2>&1

EXITCODE=${PIPESTATUS[0]}
if [ $EXITCODE -eq 0 ]; then
    echo RECO ls -l
    ls -l
    gzip fjr.xml
    mv fjr.xml.gz $WD/fjr_RECO_${JOBNUM}.xml.gz
    xrdcp -s reco.root root://cmseos.fnal.gov//store/user/tucker/${OUTPUTDIR}/reco_${JOBNUM}.root 2>&1
    XRDCP_EXITCODE=${PIPESTATUS[0]}
    if [ $XRDCP_EXITCODE -ne 0 ]; then
        echo problem with xrdcp!
        EXITCODE=XRDCP_EXITCODE
    fi
fi

exit $EXITCODE
)

if [ $EXITCODE -ne 0 ]; then
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  echo @@@@ cmsRun exited RECO step with error code $EXITCODE
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  exit $EXITCODE
fi

echo END RECO
