#!/dev/null

pushd $CMSSW_BASE/src

cvs co -r V04-02-07 RecoLuminosity/LumiDB
cvs co -r V00-00-08 RecoMET/METAnalyzers
cvs co -r V15-02-06 RecoParticleFlow/PFProducer 
cvs co -r V00-00-30-01 -d EGamma/EGammaAnalysisTools UserCode/EGamma/EGammaAnalysisTools
cd EGamma/EGammaAnalysisTools/data
cat download.url | xargs wget
cd -

addpkg CommonTools/ParticleFlow # to satisfy checkdeps
addpkg PhysicsTools/PatAlgos # to have jetTools.py patched in the below

cvs co -r V00-03-04 -d CMGTools/External UserCode/CMG/CMGTools/External
cd CMGTools/External/data
rm Jec12_V7.db
rm START52_V9::All_L2L3Residual_AK5PF.txt
rm Summer12_V1_DATA.db
rm Summer12_V1_MC.db
rm TMVAClassificationCategory_JetID_53X_Dec2012.weights.xml
rm TMVAClassificationCategory_JetID_MET_53X_Dec2012.weights.xml
rm TMVAClassification_5x_BDT_chsFullPlusRMS.weights.xml
rm TMVAClassification_5x_BDT_chsSimpleNoVtxCat.weights.xml
rm TMVAClassification_5x_BDT_fullPlusRMS.weights.xml
rm TMVAClassification_5x_BDT_simpleNoVtxCat.weights.xml
rm TMVAClassification_PuJetIdMinMVA.weights.xml
rm TMVAClassification_PuJetIdOptMVA.weights.xml
rm mva_JetID.weights.xml
rm mva_JetID_v1.weights.xml
cd -

cvs co -r V01-10-02 RecoBTag/SecondaryVertex
addpkg RecoBTag/Configuration
patch -p0 < JMTucker/Tools/patches

scram b -j 8

popd
