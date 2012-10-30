#!/bin/tcsh

pushd $CMSSW_BASE/src

cvs co -r V06-05-06-03 DataFormats/PatCandidates
cvs co -r V08-09-43 PhysicsTools/PatAlgos
cvs co -r V15-02-06 RecoParticleFlow/PFProducer 
cvs co -r V00-00-08 RecoMET/METAnalyzers
cvs co -r V00-00-16 -d EGamma/EGammaAnalysisTools UserCode/EGamma/EGammaAnalysisTools
cd EGamma/EGammaAnalysisTools/data
cat download.url | xargs wget
cd -

addpkg CommonTools/ParticleFlow
addpkg PhysicsTools/PatUtils
addpkg PhysicsTools/SelectorUtils
addpkg PhysicsTools/TagAndProbe

scram b -j 8
popd
