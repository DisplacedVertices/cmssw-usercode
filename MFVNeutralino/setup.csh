#!/bin/tcsh

pushd $CMSSW_BASE/src

cvs co -r V00-01-32 GeneratorInterface/Pythia8Interface 

patch -p0 < MFVNeutralino/MFVNeutralino/patches

scram b -j 8
popd
