#!/bin/tcsh

pushd $CMSSW_BASE/src
cvs co -r V00-01-32 GeneratorInterface/Pythia8Interface 
scram b -j 8
popd
