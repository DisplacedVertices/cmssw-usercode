#!/bin/bash

if [[ ! -z $CMSSW_BASE ]]; then
    echo must NOT cmsenv first
    exit 1
fi

WD=$(pwd)

if [[ ! -e .SCRAM/Environment ]] || ! grep -q 'SCRAM_PROJECTVERSION=CMSSW_10_2_6' .SCRAM/Environment; then
    echo this only works with the 2018 version and current working dir must be that
    exit 1
fi

cd config/toolbox/slc6_amd64_gcc700/tools/available

scram tool remove pythia8
cat > pythia8.xml <<EOF
<tool name="pythia8" version="240">
  <lib name="pythia8"/>
  <client>
    <environment name="PYTHIA8_BASE" default="/cvmfs/cms.cern.ch/slc6_amd64_gcc700/external/pythia8/240"/>
    <environment name="LIBDIR" default="\$PYTHIA8_BASE/lib"/>
    <environment name="INCLUDE" default="\$PYTHIA8_BASE/include"/>
  </client>
  <runtime name="PYTHIA8DATA" value="\$PYTHIA8_BASE/share/Pythia8/xmldoc"/>
  <runtime name="ROOT_INCLUDE_PATH" value="\$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="cxxcompiler"/>
  <use name="hepmc"/>
  <use name="lhapdf"/>
</tool>
EOF

scram tool remove dire
cat > dire.xml <<EOF
<tool name="dire" version="2.003">
  <lib name="dire"/>
  <client>
    <environment name="DIRE_BASE" default="/cvmfs/cms.cern.ch/slc6_amd64_gcc700/external/dire/2.003"/>
    <environment name="LIBDIR" default="\$DIRE_BASE/lib"/>
    <environment name="INCLUDE" default="\$DIRE_BASE/include"/>
    <environment name="BINDIR" default="\$DIRE_BASE/bin"/>
  </client>
  <runtime name="PATH" default="\$BINDIR" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="pythia8"/>
</tool>
EOF

scram tool remove vincia
cat > vincia.xml <<EOF
<tool name="vincia" version="2.2.04">
  <lib name="vincia"/>
  <lib name="VinciaMG4"/>
  <lib name="VinciaMG5"/>
  <client>
    <environment name="VINCIA_BASE" default="/cvmfs/cms.cern.ch/slc6_amd64_gcc700/external/vincia/2.2.04"/>
    <environment name="LIBDIR" default="\$VINCIA_BASE/lib"/>
    <environment name="INCLUDE" default="\$VINCIA_BASE/include"/>
  </client>
  <runtime name="VINCIADATA" value="\$VINCIA_BASE/share/Vincia/xmldoc"/>
  <use name="root_cxxdefaults"/>
  <use name="pythia8"/>
</tool>
EOF

for x in pythia8 dire vincia; do
    scram setup $x
done

cd $WD
tarfn=pythia8240-GeneratorInterface.tgz
curl -s https://home.fnal.gov/~tucker/$tarfn -o $tarfn
tar xf $tarfn

eval $(scram runtime -sh)

exit 0



# need to do this to remake the tarball
export CMSSW_GIT_REFERENCE=/cvmfs/cms.cern.ch/cmssw.git.daily
git cms-addpkg GeneratorInterface/Pythia8Interface || exit 1

patch -p1 <<EOF
diff --git a/GeneratorInterface/Pythia8Interface/interface/MultiUserHook.h b/GeneratorInterface/Pythia8Interface/interface/MultiUserHook.h
index f53d32df75e..58b70da4afd 100644
--- a/GeneratorInterface/Pythia8Interface/interface/MultiUserHook.h
+++ b/GeneratorInterface/Pythia8Interface/interface/MultiUserHook.h
@@ -439,19 +439,19 @@ public:
   // Do change fragmentation parameters.
   // Input: flavPtr, zPtr, pTPtr, idEnd, m2Had, iParton.
   bool doChangeFragPar( Pythia8::StringFlav* flavPtr, Pythia8::StringZ* zPtr, Pythia8::StringPT* pTPtr, int idEnd,
-    double m2Had, std::vector<int> iParton) override {
+    double m2Had, std::vector<int> iParton, const Pythia8::StringEnd* sEnd) override {
       bool test = true;
       for (Pythia8::UserHooks *hook : hooks_) {
-        if (hook->canChangeFragPar()) test &= hook->doChangeFragPar(flavPtr, zPtr, pTPtr, idEnd, m2Had, iParton);
+        if (hook->canChangeFragPar()) test &= hook->doChangeFragPar(flavPtr, zPtr, pTPtr, idEnd, m2Had, iParton, sEnd);
       }
       return test;
   }
 
  // Do a veto on a hadron just before it is added to the final state.
-  bool doVetoFragmentation( Pythia8::Particle part) override {
+  bool doVetoFragmentation( Pythia8::Particle part, const Pythia8::StringEnd* sEnd) override {
     bool test = false;
     for (Pythia8::UserHooks *hook : hooks_) {
-      if (hook->canChangeFragPar()) test |= hook->doVetoFragmentation(part);
+      if (hook->canChangeFragPar()) test |= hook->doVetoFragmentation(part, sEnd);
     }
     return test;
   }
EOF

scram b
