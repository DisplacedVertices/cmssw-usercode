#!/dev/null

pushd $CMSSW_BASE/src

# sigh
mkdir RecoLuminosity
curl https://codeload.github.com/cms-sw/RecoLuminosity-LumiDB/tar.gz/V04-02-10  | tar xzv -C RecoLuminosity
mv RecoLuminosity/RecoLuminosity-LumiDB-* RecoLuminosity/LumiDB
rm -r RecoLuminosity/LumiDB/{plotdata,doc,test}

cvs co -r V00-00-08 RecoMET/METAnalyzers
cvs co -r V15-02-06 RecoParticleFlow/PFProducer 
addpkg CommonTools/ParticleFlow # satisfy checkdeps
cvs co -r V00-00-30-01 -d EGamma/EGammaAnalysisTools UserCode/EGamma/EGammaAnalysisTools
cd EGamma/EGammaAnalysisTools/data
cat download.url | xargs wget
cd -

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

#patch -p0 < JMTucker/Tools/patches

scram b -j 8

popd
