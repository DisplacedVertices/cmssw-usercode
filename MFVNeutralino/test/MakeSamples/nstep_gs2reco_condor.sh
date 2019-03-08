#!/bin/bash

#exec 2>&1

for fn in rawhlt.py reco.py miniaod.py; do
    if [[ -e $fn ]]; then
        ./todoify.sh $fn > temp
        mv temp $fn
    fi
done

WD=$(pwd)
JOBNUM=$1
OUTPUTDIR=$2
TODOS="$3 $4 $5 $6 $7 $8 $9"
TODOS2="$4 $5 $6 $7 $8 $9"

echo WD: $WD
echo JOBNUM: $JOBNUM
echo OUTPUTDIR: $OUTPUTDIR
echo TODOS: $TODOS
echo TODOS2: $TODOS2

source /cvmfs/cms.cern.ch/cmsset_default.sh

################################################################################

echo START RAWHLT

(
scram project -n RAWHLT CMSSW CMSSW_9_4_0_patch1 2>&1
cd RAWHLT/src
eval $(scram runtime -sh)
cp $WD/{inputfns.txt,year.txt,*.py,*.txt.gz} .

echo cmsRun
cmsRun -j fjr.xml rawhlt.py ${TODOS} 2>&1

EXITCODE=${PIPESTATUS[0]}
if [ $EXITCODE -eq 0 ]; then
    gzip fjr.xml
    mv fjr.xml.gz $WD/fjr_RAWHLT_${JOBNUM}.xml.gz
    mv rawhlt.root $WD/
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
scram project -n RECO CMSSW CMSSW_9_4_0_patch1 2>&1
cd RECO/src
eval $(scram runtime -sh)
cp $WD/{year.txt,*.py} .
mv $WD/rawhlt.root .

echo cmsRun
cmsRun -j fjr.xml reco.py ${TODOS2} 2>&1

EXITCODE=${PIPESTATUS[0]}
if [ $EXITCODE -eq 0 ]; then
    gzip fjr.xml
    mv fjr.xml.gz $WD/fjr_RECO_${JOBNUM}.xml.gz
    xrdcp -s reco.root root://cmseos.fnal.gov//store/user/tucker/${OUTPUTDIR}/reco_${JOBNUM}.root 2>&1
    XRDCP_EXITCODE=${PIPESTATUS[0]}
    if [ $XRDCP_EXITCODE -ne 0 ]; then
        echo problem with xrdcp!
        EXITCODE=XRDCP_EXITCODE
    fi
    mv reco.root $WD/
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

################################################################################

echo START MINIAOD

(
scram project -n MINIAOD CMSSW CMSSW_9_4_6_patch1 2>&1
cd MINIAOD/src
eval $(scram runtime -sh)
cp $WD/{year.txt,*.py} .
mv $WD/reco.root .

echo cmsRun
cmsRun -j fjr.xml miniaod.py ${TODOS2} 2>&1

EXITCODE=${PIPESTATUS[0]}
if [ $EXITCODE -eq 0 ]; then
    gzip fjr.xml
    mv fjr.xml.gz $WD/fjr_MINIAOD_${JOBNUM}.xml.gz
    xrdcp -s miniaod.root root://cmseos.fnal.gov//store/user/tucker/${OUTPUTDIR}/miniaod_${JOBNUM}.root 2>&1
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
  echo @@@@ cmsRun exited MINIAOD step with error code $EXITCODE
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  exit $EXITCODE
fi

echo END MINIAOD
