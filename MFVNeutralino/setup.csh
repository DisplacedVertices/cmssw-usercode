#!/bin/tcsh

pushd $CMSSW_BASE/src

cvs co -r version3 -d JMTucker/Tools UserCode/JMTucker/Tools

source JMTucker/Tools/setup.csh

# this only works at cmslpc, obviously
cat > pythia8.xml <<EOF
<tool name="pythia8" version="165-cms">
  <lib name="pythia8"/>
  <lib name="hepmcinterface"/>
  <client>
    <environment name="PYTHIA8_BASE" default="/uscmst1/prod/sw/cms/slc5_amd64_gcc462/external/pythia8/165-cms"/>
    <environment name="LIBDIR" default="$PYTHIA8_BASE/lib"/>
    <environment name="INCLUDE" default="$PYTHIA8_BASE/include"/>
  </client>
  <runtime name="PYTHIA8DATA" value="$PYTHIA8_BASE/xmldoc"/>
  <use name="cxxcompiler"/>
  <use name="hepmc"/>
  <use name="pythia6"/>
  <use name="clhep"/>
  <use name="lhapdf"/>
</tool>
EOF
mv pythia8.xml $CMSSW_BASE/config/toolbox/slc5_amd64_gcc462/tools/selected/pythia8.xml
scram setup pythia8

cvs co -r V00-01-32 GeneratorInterface/Pythia8Interface 
#patch -p0 < JMTucker/MFVNeutralino/patches

scram b -j 8
popd
