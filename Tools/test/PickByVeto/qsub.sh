#$ -S /bin/sh

export X509_USER_PROXY=/home/uscms213/x509up_u819

JOBNUM=${PBS_ARRAYID}
JOBNAME=$(echo ${PBS_JOBNAME} | sed "s/-${JOBNUM}$//")
JOBID=$(echo ${PBS_JOBID} | tr -s '[]' '_.')

echo JOBNAME: $JOBNAME
echo JOBNUM: $JOBNUM
echo JOBID: $JOBID

startdate=$(date +"%s")

source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /home/uscms213/CMSSW_7_6_3_patch2/src/JMTucker/Tools/test/PickByVeto
eval `scram runtime -sh`

set -x
cmsRun pick_by_veto.py +job $JOBNUM +sample $JOBNAME +per 10 +out-fn ${JOBNAME}_${JOBNUM}.root
cmsrunexit=$?
set +x

echo cmsRun exited with code $cmsrunexit

enddate=$(date +"%s")
echo startdate $startdate enddate $startdate deltat $((enddate-startdate))
