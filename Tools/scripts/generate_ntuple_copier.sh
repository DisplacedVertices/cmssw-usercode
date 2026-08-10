cat >copier.cc <<EOF
#include "JMTucker/MFVNeutralino/interface/Ntuple.h"
#include "JMTucker/Tools/interface/Ntuple.h"
#include "JMTucker/Tools/interface/NtupleReader.h"

int main(int argc, char** argv) {
  return jmt::copy<$1>(argc, argv, "$2");
}
EOF
