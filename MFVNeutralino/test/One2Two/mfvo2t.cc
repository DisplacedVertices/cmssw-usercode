#include "TH1.h"
#include "TFile.h"
#include "TRandom3.h"

#include "Random.h"
#include "ROOTTools.h"

#include "ToyThrower.h"
#include "Templates.h"
#include "ClearedJetsTemplater.h"
#include "PhiShiftTemplater.h"
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
  printf("template binning: (%i, %f, %f)\n", mfv::Template::nbins, mfv::Template::min_val, mfv::Template::max_val);

  TFile* out_f = new TFile(out_fn.c_str(), "recreate");
  TRandom3* rand = new TRandom3(jmt::seed_base + seed);
  mfv::ToyThrower* tt = new mfv::ToyThrower("", tree_path, out_f, rand);
  mfv::Templater* ter = 0;
  if (templates_phishift)
    ter = new mfv::PhiShiftTemplater("", out_f, rand);
  else if (templates_clearedjets)
    ter = new mfv::ClearedJetsTemplater("", out_f, rand);
    
  mfv::Fitter* fitter = new mfv::Fitter("", out_f, rand);

  TFile f_sig("signal_templates.root");
  printf("\n\n\n\n\n\n\n*** signal template is fixed to h_sig_ntk5_mfv_neutralino_tau1000um_M0400 ***\n\n\n\n\n\n\n");
  TH1D* h_sig = (TH1D*)f_sig.Get("h_sig_ntk5_mfv_neutralino_tau1000um_M0400"); //TString::Format("h_sig_ntk%i_%s", tt->min_ntracks, tt->samples.get(tt->signal).name.c_str()))->Clone("h_sig_FIXME");
  h_sig->SetDirectory(out_f);

  for (int itoy = 0; itoy < ntoys; ++itoy) {
    tt->throw_toy();

    std::vector<double> true_pars = { double(tt->b_sum_sig_2v), double(tt->b_sum_bkg_2v) };
    ter->process(itoy, &tt->toy_1v, &tt->toy_2v);
    for (double tp : ter->true_pars())
      true_pars.push_back(tp);

    fitter->fit(itoy, &ter->templates, h_sig, tt->toy_2v, true_pars);
  }

  out_f->Write();
  out_f->Close();
  delete out_f;
  delete tt;
}
