#include "TH1.h"
#include "TFile.h"
#include "TRandom3.h"

#include "Random.h"
#include "ROOTTools.h"

#include "ToyThrower.h"
#include "Templates.h"
#include "One2TwoPhiShift.h"
#include "Fitter.h"

int main() {
  jmt::set_root_style();

  jmt::ConfigFromEnv env("mfvo2t");
  const std::string tree_path = env.get_string("tree_path", "crab/MiniTreeV18_Njets");
  const std::string out_fn = env.get_string("out_fn", "mfvo2t.root");
  const int seed = env.get_int("seed", 0);
  const int ntoys = env.get_int("ntoys", 1);
  const std::string templates_kind = env.get_string_lower("templates_kind", "phishift");
  const bool templates_phishift = templates_kind == "phishift";
  const bool templates_clearedjets = templates_kind == "clearedjets";
  if (!(templates_phishift || templates_clearedjets))
    jmt::vthrow("templates config must be one of \"phishift\", \"clearedjets\"");

  printf("mfvo2t config:\n");
  printf("trees from %s\n", tree_path.c_str());
  printf("output to %s\n", out_fn.c_str());
  printf("seed: %i\n", seed);
  printf("ntoys: %i\n", ntoys);
  printf("template kind: %s (phishift? %i clearedjets? %i)\n", templates_kind.c_str(), templates_phishift, templates_clearedjets);

  TFile* out_f = new TFile(out_fn.c_str(), "recreate");
  TRandom3* rand = new TRandom3(jmt::seed_base + seed);
  mfv::ToyThrower* tt = new mfv::ToyThrower("", tree_path, out_f, rand);
  mfv::One2TwoPhiShift* o_phishift = new mfv::One2TwoPhiShift("", out_f, rand);
  mfv::Fitter* fitter = new mfv::Fitter("", out_f, rand);

  TH1D* h_empty_sig_template = new TH1D("h_empty_sig_template", "", 20000, 0, 10);
  h_empty_sig_template->SetDirectory(0);

  TFile f_sig("signal_templates.root");

  TH1D* h_sig = (TH1D*)f_sig.Get(TString::Format("h_sig_ntk%i_%s", tt->min_ntracks, tt->samples.get(tt->signal).name.c_str()))->Clone("h_sig_FIXME");
  h_sig->SetDirectory(out_f);

  for (int itoy = 0; itoy < ntoys; ++itoy) {
    tt->throw_toy();

    mfv::Templates* templates = 0;
    if (templates_phishift) {
      o_phishift->process(itoy, &tt->toy_1v, &tt->toy_2v);
      templates = &o_phishift->templates;
    }
    else if (templates_clearedjets) {
      jmt::vthrow("templates_clearedjets not implemented");
    }

    fitter->fit(itoy, templates, h_sig, tt->toy_2v);
  }

  delete h_empty_sig_template;

  out_f->Write();
  out_f->Close();
  delete out_f;
  delete tt;
}
