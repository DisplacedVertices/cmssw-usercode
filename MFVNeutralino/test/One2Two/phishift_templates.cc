#include "TFile.h"
#include "One2TwoPhiShift.h"
#include "ROOTTools.h"
#include "ToyThrower.h"

int main(int argc, char** argv) {
  jmt::SetROOTStyle();

  int ntoys = argc > 1 ? atoi(argv[1]) : 1;

  TFile* f = new TFile("phishift_templates.root", "recreate");
  mfv::ToyThrower* tt = new mfv::ToyThrower("", "crab/MiniTreeV18_Njets", f);

  for (int i = 0; i < ntoys; ++i) {
    tt->throw_toy();
    mfv::One2TwoPhiShift* o = 
      new mfv::One2TwoPhiShift("", f, tt->rand, tt->seed, tt->ntoys,
                               &tt->toy_1v, &tt->toy_2v);
    o->make_templates();
    delete o;
  }

  f->Write();
  f->Close();
  delete f;
  delete tt;
}
