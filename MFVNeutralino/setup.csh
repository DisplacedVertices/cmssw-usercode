#!/bin/tcsh

pushd $CMSSW_BASE/src

cvs co -d JMTucker/Tools UserCode/JMTucker/Tools

source JMTucker/Tools/setup.csh

cvs co -r V00-01-32 GeneratorInterface/Pythia8Interface 
patch -p0 < JMTucker/MFVNeutralino/patches

scram b -j 8
popd
