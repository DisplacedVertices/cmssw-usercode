#include "TFile.h"
#include "TRandom3.h"
#include "Random.h"
#include "ROOTTools.h"
#include "One2TwoPhiShift.h"
#include "ToyThrower.h"

int main() {
  jmt::set_root_style();

  jmt::ConfigFromEnv env("mfvo2t");
  const std::string out_fn = env.get_string("out_fn", "mfvo2t.root");
  const std::string tree_path = env.get_string("tree_path", "crab/MiniTreeV18_Njets");
  const int seed = env.get_int("seed", 0);
  const int ntoys = env.get_int("ntoys", 1);
  const std::string templates = env.get_string("templates", "phishift");
  const bool templates_phishift = templates == "phishift";
  const bool templates_clearedjets = templates == "clearedjets";
  if (!(templates_phishift || templates_clearedjets))
    jmt::vthrow("templates config must be one of \"phishift\", \"clearedjets\"");

  TFile* out_f = new TFile(out_fn.c_str(), "recreate");
  TRandom3* rand = new TRandom3(jmt::seed_base + seed);
  mfv::ToyThrower* tt = new mfv::ToyThrower("", tree_path, out_f, rand);
  mfv::One2TwoPhiShift* o_phishift = new mfv::One2TwoPhiShift("", out_f, rand);
  mfv::Fitter* fitter = new mfv::Fitter("", out_f, rand);

  for (int itoy = 0; itoy < ntoys; ++itoy) {
    tt->throw_toy();

    const Templates* templates = 0;
    if (templates_phishift) {
      o_phishift->process(itoy, &tt->toy_1v, &tt->toy_2v);
      templates = o_phishift->templates;
    }
    else if (templates_clearedjets) {
      jmt::vthrow("templates_clearedjets not implemented");
    }

    fitter->fit(itoy, templates, &tt->toy_2v);
  }

  out_f->Write();
  out_f->Close();
  delete out_f;
  delete tt;
}
