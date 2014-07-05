#include "ROOTTools.h"
#include "TH1.h"
#include "TROOT.h"
#include "TStyle.h"

namespace jmt {
  void SetROOTStyle() {
    TH1::SetDefaultSumw2();
  }
}
