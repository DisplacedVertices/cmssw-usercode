source /cvmfs/cms.cern.ch/cmsset_default.sh
scram project -n mfv_10627 CMSSW CMSSW_10_6_27
cd mfv_10627/src
cmsenv
git cms-init --upstream-only
#git clone https://github.com/DisplacedVertices/cmssw-usercode.git JMTucker # we can pull via https but not push. Leaving this here in case someone doesn't have ssh keys set up...
git clone git@github.com:DisplacedVertices/cmssw-usercode.git JMTucker
cd JMTucker
scram b -j 4
statuscode=$?
source /cvmfs/cms.cern.ch/common/crab-setup.sh

# Check the statuscode, for the purpose of the continuous integration
[ $statuscode == 0 ]
