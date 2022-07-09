source /cvmfs/cms.cern.ch/cmsset_default.sh
scram project -n mfv_946p1 CMSSW CMSSW_9_4_6_patch1
cd mfv_946p1/src
cmsenv
git cms-init --upstream-only
git clone https://github.com/DisplacedVertices/cmssw-usercode.git JMTucker
cd JMTucker
scram b -j 4
statuscode=$?
source /cvmfs/cms.cern.ch/common/crab-setup.sh

# Check the statuscode, for the purpose of the continuous integration
[ $statuscode == 0 ]
