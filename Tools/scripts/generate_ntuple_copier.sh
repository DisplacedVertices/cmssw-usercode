cat >copier.cc <<EOF
#include "DVCode/MFVNeutralino/interface/Ntuple.h"
#include "DVCode/Tools/interface/Ntuple.h"
#include "DVCode/Tools/interface/NtupleReader.h"

int main(int argc, char** argv) {
  return jmt::copy<$1>(argc, argv, "$2");
}
EOF
