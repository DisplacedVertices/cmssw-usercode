source /cvmfs/cms.cern.ch/cmsset_default.sh
scram project -n mfv_10648 CMSSW CMSSW_10_6_48
cd mfv_10648/src
cmsenv
git cms-init --upstream-only
#git clone https://github.com/DisplacedVertices/cmssw-usercode.git JMTucker # we can pull via https but not push. Leaving this here in case someone doesn't have ssh keys set up...
git clone git@github.com:DisplacedVertices/cmssw-usercode.git JMTucker

# dependencies for Rochester corrections
git clone ssh://git@gitlab.cern.ch:7999/akhukhun/roccor.git RoccoR

# from EgammaPostRecoTools scales/smearings from 
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammaUL2016To2018#Recipe_for_running_scales_and_sm
git cms-addpkg RecoEgamma/EgammaTools  ### essentially just checkout the package from CMSSW
git clone git@github.com:cms-egamma/EgammaPostRecoTools.git
mv EgammaPostRecoTools/python/EgammaPostRecoTools.py RecoEgamma/EgammaTools/python/.
git clone -b ULSSfiles_correctScaleSysMC git@github.com:jainshilpi/EgammaAnalysis-ElectronTools.git EgammaAnalysis/ElectronTools/data/
git cms-addpkg EgammaAnalysis/ElectronTools


cd JMTucker
git checkout UL_Lepton

cd ..
scram b -j 4
statuscode=$?
source /cvmfs/cms.cern.ch/common/crab-setup.sh

# Check the statuscode, for the purpose of the continuous integration
[ $statuscode == 0 ]
