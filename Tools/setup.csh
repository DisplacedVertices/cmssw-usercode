#!/dev/null

pushd $CMSSW_BASE/src

cvs co -r V04-02-02    RecoLuminosity/LumiDB
cvs co -r V06-05-06-07 DataFormats/PatCandidates
cvs co -r V08-09-52    PhysicsTools/PatAlgos
cvs co -r V03-09-28    PhysicsTools/PatUtils
cvs co -r V00-02-14    DataFormats/StdDictionaries
cvs co -r V00-00-08    RecoMET/METAnalyzers
cvs co -r V00-00-13    RecoMET/METFilters
cvs co -r V03-03-12-02 RecoMET/METProducers
cvs co -r V15-02-06    RecoParticleFlow/PFProducer 
cvs co -r V00-00-30-01 -d EGamma/EGammaAnalysisTools UserCode/EGamma/EGammaAnalysisTools
cd EGamma/EGammaAnalysisTools/data
cat download.url | xargs wget
cd -

addpkg CommonTools/ParticleFlow
addpkg CommonTools/Utils
addpkg PhysicsTools/SelectorUtils
addpkg PhysicsTools/UtilAlgos

cvs co -r V01-10-02 RecoBTag/SecondaryVertex
addpkg RecoBTag/Configuration

patch -p0 < JMTucker/Tools/patches

scram b -j 24

popd

echo
echo XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
echo
echo checkdeps would also suggest these packages, mostly TQAF:
echo not getting them, so beware if you use them!
echo
echo AnalysisDataFormats/TopObjects
echo ElectroWeakAnalysis/Skimming
echo ElectroWeakAnalysis/WENu
echo ElectroWeakAnalysis/ZEE
echo ElectroWeakAnalysis/ZMuMu
echo MuonAnalysis/MomentumScaleCalibration
echo MuonAnalysis/MuonAssociators
echo PhysicsTools/FWLite
echo PhysicsTools/PatExamples
echo PhysicsTools/TagAndProbe
echo TopQuarkAnalysis/Examples
echo TopQuarkAnalysis/TopEventProducers
echo TopQuarkAnalysis/TopEventSelection
echo TopQuarkAnalysis/TopHitFit
echo TopQuarkAnalysis/TopJetCombination
echo TopQuarkAnalysis/TopKinFitter
echo TopQuarkAnalysis/TopObjectResolutions
echo
echo XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
echo
