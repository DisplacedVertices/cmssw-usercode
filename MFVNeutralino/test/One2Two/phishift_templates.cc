#include "TFile.h"
#include "One2TwoPhiShift.h"
#include "ROOTTools.h"
#include "ToyThrower.h"

int main() {
  jmt::SetROOTStyle();

  jmt::ConfigFromEnv env("mfvo2t");
  const std::string out_fn = env.get_string("out_fn", "mfvo2t.root");
  const std::string tree_path = env.get_string("tree_path", "crab/MiniTreeV18_Njets");
  const int seed = env.get_int("seed", 0);
  const int ntoys = env.get_int("ntoys", 1);

  TFile* out_f = new TFile(out_fn.c_str(), "recreate");
  TRandom3* rand = new TRandom3(12191982 + seed);
  mfv::ToyThrower* tt = new mfv::ToyThrower("", tree_path, out_f, rand);

  for (int i = 0; i < ntoys; ++i) {
    tt->throw_toy();
    mfv::One2TwoPhiShift* o = new mfv::One2TwoPhiShift("", f, tt->rand, tt->seed, tt->ntoys, &tt->toy_1v, &tt->toy_2v);
    o->make_templates();
    delete o;
  }

  out_f->Write();
  out_f->Close();
  delete out_f;
  delete tt;
}
