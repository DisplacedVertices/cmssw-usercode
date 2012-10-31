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

cvs co -r V01-10-02 RecoBTag/SecondaryVertex
addpkg RecoBTag/Configuration

patch -p0 < JMTucker/Tools/patches

scram b -j 8
popd

echo
echo XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
echo
echo checkdeps would also suggest these packages, mostly TQAF:
echo not getting them, so beware if you use them!
echo
echo AnalysisDataFormats/TopObjects
echo ElectroWeakAnalysis/WENu
echo ElectroWeakAnalysis/ZEE
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
