#include "TH1.h"
#include "TFile.h"
#include "TRandom3.h"

#include "Random.h"
#include "ROOTTools.h"

#include "ToyThrower.h"
#include "Templates.h"
#include "ClearedJetsTemplater.h"
#include "PhiShiftTemplater.h"
#include "SimpleClearingTemplater.h"
#include "Fitter.h"

int main() {
  jmt::set_root_style();
  TH1::SetDefaultSumw2();

  jmt::ConfigFromEnv env("mfvo2t");
  const std::string tree_path = env.get_string("tree_path", "trees");
  const std::string out_fn = env.get_string("out_fn", "mfvo2t.root");
  const int seed = env.get_int("seed", 0);
  const int ntoys = env.get_int("ntoys", 1);
  const std::string templates_kind = env.get_string_lower("templates_kind", "clearedjets");
  const bool templates_save_plots = env.get_bool("templates_save_plots", true);
  const bool templates_phishift = templates_kind == "phishift";
  const bool templates_clearedjets = templates_kind == "clearedjets";
  const bool templates_simpleclear = templates_kind == "simpleclear";
  const int sig_from_file_num = env.get_int("sig_from_file_num", 0);
  const std::string sig_from_file_fn = env.get_string("sig_from_file_fn", "bigsigscan.root");
  const bool run_templater = env.get_bool("run_templater", true);
  const bool run_fit = env.get_bool("run_fit", true);
  const std::string data_fn = env.get_string("data_fn", "MultiJetPk2012.root");
  const bool process_data = env.get_bool("process_data", false);

  if (!(templates_phishift || templates_clearedjets || templates_simpleclear))
    jmt::vthrow("templates config must be one of \"phishift\", \"clearedjets\", \"simpleclear\"");

  printf("mfvo2t config:\n");
  printf("trees from %s\n", tree_path.c_str());
  printf("output to %s\n", out_fn.c_str());
  printf("seed: %i\n", seed);
  printf("ntoys: %i\n", ntoys);
  printf("save plots in templater: %i\n", templates_save_plots);
  printf("template kind: %s (phishift? %i clearedjets? %i simpleclear? %i)\n", templates_kind.c_str(), templates_phishift, templates_clearedjets, templates_simpleclear);
  printf("template binning: (%i, %f, %f)\n", mfv::Template::nbins, mfv::Template::min_val, mfv::Template::max_val);
  printf("process data from %s? %s\n", data_fn.c_str(), (process_data ? "YES!" : "no"));

  TFile* out_f = new TFile(out_fn.c_str(), "recreate");
  TRandom3* rand = new TRandom3(jmt::seed_base + seed);

  mfv::ToyThrower* tt = new mfv::ToyThrower("", tree_path, out_f, rand);

  mfv::Templater* ter = 0;
  if (templates_phishift)
    ter = new mfv::PhiShiftTemplater("", out_f, rand);
  else if (templates_clearedjets)
    ter = new mfv::ClearedJetsTemplater("", out_f, rand);
  else if (templates_simpleclear)
    ter = new mfv::SimpleClearingTemplater("", out_f, rand);
  ter->save_plots = templates_save_plots;

  mfv::Fitter* fitter = new mfv::Fitter("", out_f, rand);

  TH1D* h_sig = 0;

  if (0) {
    h_sig = mfv::Template::hist_with_binning("h_sig_template", "");
    int ibin = 1;
    for (double c : { 573.0, 1355.0, 2090.0, 2417.0, 2449.0, 15968.0 })
      h_sig->SetBinContent(ibin++, c);
  }
  else if (sig_from_file_num == 0) {
    h_sig = tt->signal_template("h_sig_template", "");
  }
  else {
    TFile* f_sig = TFile::Open(sig_from_file_fn.c_str());
    if (!f_sig || !f_sig->IsOpen())
      jmt::vthrow("could not open %s\n", sig_from_file_fn.c_str());
    TString h_name = TString::Format("sig%i", sig_from_file_num);
    TH1D* h = (TH1D*)f_sig->Get(h_name);
    if (!h)
      jmt::vthrow("could not get %s from %s\n", h_name.Data(), sig_from_file_fn.c_str());
    h_sig = (TH1D*)h->Clone("h_sig_template");
    h_sig->SetDirectory(0);
    f_sig->Close();
  }

  h_sig->SetDirectory(out_f);

  printf("h_sig: [ ");
  for (int ibin = 1; ibin <= h_sig->GetNbinsX(); ++ibin)
    printf("%.1f ", h_sig->GetBinContent(ibin));
  printf("]  sum: %.1f\n", h_sig->Integral());

  for (int itoy = 0; itoy < ntoys; ++itoy) {
    tt->throw_toy();

    std::vector<double> true_pars = { double(tt->b_sum_sig_2v), double(tt->b_sum_bkg_2v) };

    if (run_templater) {
      ter->process(tt->toy_dataset);
      for (double tp : ter->true_pars())
        true_pars.push_back(tp);

      if (run_fit)
        fitter->fit(itoy, ter, h_sig, tt->toy_2v, true_pars);
    }
  }

  if (process_data) {
    TDirectory* d_data = out_f->mkdir("on_data");
    d_data->cd();
    ter->process(tt->data);

    if (run_fit)
      fitter->fit(-1, ter, h_sig, *tt->data.two_vertices, {0,0});
  }

  out_f->Write();
  out_f->Close();
  delete out_f;
  delete tt;
}
