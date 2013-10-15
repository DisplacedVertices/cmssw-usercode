#!/dev/null

pushd $CMSSW_BASE/src

cvs co -r V04-02-07 RecoLuminosity/LumiDB
cvs co -r V00-00-08 RecoMET/METAnalyzers
cvs co -r V15-02-06 RecoParticleFlow/PFProducer 
cvs co -r V00-00-30-01 -d EGamma/EGammaAnalysisTools UserCode/EGamma/EGammaAnalysisTools
cvs co -r V00-03-04 -d CMGTools/External UserCode/CMG/CMGTools/External
cd EGamma/EGammaAnalysisTools/data
cat download.url | xargs wget
cd -

addpkg CommonTools/ParticleFlow # to satisfy checkdeps
addpkg PhysicsTools/PatAlgos # to have jetTools.py patched in the below

cvs co -r V01-10-02 RecoBTag/SecondaryVertex
addpkg RecoBTag/Configuration
patch -p0 < JMTucker/Tools/patches

scram b -j 8

popd
