#!/bin/bash

#exec 2>&1

JOBNUM=$1
MAXEVENTS=$2
TODO=$3
OUTDIR=$4

WORKDIR=$(pwd)
TMPDIR=${WORKDIR}/tmp
mkdir $TMPDIR
tar -xf input.tgz -C ${TMPDIR}

source /cvmfs/cms.cern.ch/cmsset_default.sh

echo WORKDIR: ${WORKDIR}
echo TMPDIR: ${TMPDIR}
echo JOBNUM: ${JOBNUM}
echo MAXEVENTS: ${MAXEVENTS}
echo TODO: ${TODO}
echo OUTDIR: ${OUTDIR}
echo ls -l
ls -l $WORKDIR $TMPDIR

################################################################################

echo
echo START GENSIM

(
scram project -n GENSIM CMSSW CMSSW_7_1_21_patch2
cd GENSIM/src
eval $(scram runtime -sh)

for x in gensim.py modify.py; do
    ln -s ${TMPDIR}/$x
done

echo cmsRun
cmsRun gensim.py maxevents=${MAXEVENTS} todo=${TODO} 2>&1 | gzip > ${WORKDIR}/log_GENSIM_${JOBNUM}.gz

EXITCODE=$?
if [ $EXITCODE -eq 0 ]; then
    gzip RandomEngineState.xml
    mv RandomEngineState.xml.gz ${WORKDIR}/RandomEngineState_GENSIM_${JOBNUM}.xml.gz
    mv gensim.root $TMPDIR
fi

echo TMPDIR:
ls -l ${TMPDIR}

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

for x in rawhlt.py modify.py minbias.py minbias_files.py minbias_files.pkl gensim.root; do
    ln -s ${TMPDIR}/$x
done

echo cmsRun
cmsRun rawhlt.py 2>&1 | gzip > ${WORKDIR}/log_RAWHLT_${JOBNUM}.gz

EXITCODE=$?
if [ $EXITCODE -eq 0 ]; then
    gzip RandomEngineState.xml
    mv RandomEngineState.xml.gz ${WORKDIR}/RandomEngineState_RAWHLT_${JOBNUM}.xml.gz
    mv hlt.root $TMPDIR
fi

echo TMPDIR:
ls -l ${TMPDIR}

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
scram project -n RECO CMSSW CMSSW_7_6_1
cd RECO/src
eval $(scram runtime -sh)

for x in /reco.py modify.py hlt.root; do
    ln -s ${TMPDIR}/$x
done

echo RECO cmsRun
cmsRun reco.py 2>&1 | gzip > ${WORKDIR}/log_RECO_${JOBNUM}.gz

EXITCODE=$?
if [ $EXITCODE -eq 0 ]; then
    mv reco.root $TMPDIR
fi

echo TMPDIR:
ls -l ${TMPDIR}

exit $EXITCODE
)

EXITCODE=$?
if [ $EXITCODE -ne 0 ]; then
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  echo @@@@ cmsRun exited RECO step with error code $EXITCODE
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  exit $EXITCODE
fi

echo END RECO

################################################################################

echo COPY:
echo xrdcp ${TMPDIR}/reco.root ${OUTDIR}/reco_${JOBNUM}.root
xrdcp ${TMPDIR}/reco.root ${OUTDIR}/reco_${JOBNUM}.root

echo DONE
