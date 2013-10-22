#!/dev/null

pushd $CMSSW_BASE/src

cvs co -r version18 -d JMTucker/Tools UserCode/JMTucker/Tools

source JMTucker/Tools/setup.csh

# this only works at cmslpc, obviously
scram tool remove pythia8
cat > pythia8.xml <<EOF
<tool name="pythia8" version="165-cms">
  <lib name="pythia8"/>
  <lib name="hepmcinterface"/>
  <client>
    <environment name="PYTHIA8_BASE" default="/uscmst1/prod/sw/cms/slc5_amd64_gcc462/external/pythia8/165-cms"/>
    <environment name="LIBDIR" default="/uscmst1/prod/sw/cms/slc5_amd64_gcc462/external/pythia8/165-cms/lib"/>
    <environment name="INCLUDE" default="/uscmst1/prod/sw/cms/slc5_amd64_gcc462/external/pythia8/165-cms/include"/>
  </client>
  <runtime name="PYTHIA8DATA" value="/uscmst1/prod/sw/cms/slc5_amd64_gcc462/external/pythia8/165-cms/xmldoc"/>
  <use name="cxxcompiler"/>
  <use name="hepmc"/>
  <use name="pythia6"/>
  <use name="clhep"/>
  <use name="lhapdf"/>
</tool>
EOF
mv pythia8.xml $CMSSW_BASE/config/toolbox/slc5_amd64_gcc462/tools/selected/pythia8.xml
scram setup pythia8

cmsenv # must do again after the setup above, even if user has already cmsenv'ed

cvs co -r V00-01-32 GeneratorInterface/Pythia8Interface 

scram b -j 8

popd
