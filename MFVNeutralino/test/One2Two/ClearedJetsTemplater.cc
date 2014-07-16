#include "ClearedJetsTemplater.h"
#include "TF1.h"
#include "TFile.h"
#include "TFitResult.h"
#include "TH2D.h"
#include "TRandom3.h"
#include "TTree.h"
#include "Phi.h"
#include "Prob.h"
#include "ROOTTools.h"
#include "Random.h"
#include "Templates.h"

namespace mfv {
  ClearedJetsTemplater::ClearedJetsTemplater(const std::string& name_, TFile* f, TRandom* r)
    : Templater("ClearedJets", name_, f, r),

      env("mfvo2t_clearedjets" + uname),
      d2d_cut(env.get_double("d2d_cut", 0.05)),
      sample_count(env.get_int("sample_count", -1)),
      flat_phis(env.get_bool("flat_phis", false)),
      phi_from_jet_mu(env.get_double("phi_from_jet_mu", M_PI_2)),
      phi_from_jet_sigma(env.get_double("phi_from_jet_sigma", 0.4)),
      clearing_mu(env.get_double("clearing_mu", 0.028)),
      clearing_sigma(env.get_double("clearing_sigma", 0.005))
  {
    printf("ClearedJetsTemplater%s config:\n", name.c_str());
    printf("d2d_cut: %f\n", d2d_cut);
    printf("sample_count: %i\n", sample_count);
    if (flat_phis)
      printf("phis thrown flat\n");
    else
      printf("phi_from_jet ~ Gaus(%f, %f)\n", phi_from_jet_mu, phi_from_jet_sigma);
    printf("clearing ~ Erf(%f, %f)\n", clearing_mu, clearing_sigma);
    fflush(stdout);

    book_trees();
  }

  void ClearedJetsTemplater::book_trees() {
    dout->cd();

    TTree* t_config = new TTree("t_config", "");
    t_config->Branch("seed", const_cast<int*>(&seed), "seed/I");
    t_config->Branch("d2d_cut", const_cast<double*>(&d2d_cut), "d2d_cut/D");
    t_config->Branch("sample_count", const_cast<int*>(&sample_count), "sample_count/I");
    t_config->Fill();


    t_fit_info = new TTree("t_fit_info", "");
    t_fit_info->Branch("seed", const_cast<int*>(&seed), "seed/I");
    t_fit_info->Branch("toy", &dataset.toy, "toy/I");
  }    

  void ClearedJetsTemplater::book_toy_fcns_and_histos() {
    Templater::book_hists();

  }

  bool ClearedJetsTemplater::is_sideband(const VertexSimple& v0, const VertexSimple& v1) const {
    return v0.d2d(v1) < d2d_cut;
  }

  void ClearedJetsTemplater::make_templates() {
    printf("ClearedJetsTemplater%s making templates: fill me in\n", name.c_str()); fflush(stdout);

    clear_templates();

    TDirectory* dtemp = dtoy->mkdir("templates");
    dtemp->cd();

    jmt::vthrow("ClearedJetsTemplater::make_templates not implemented");
  }

  void ClearedJetsTemplater::process_imp() {
    printf("ClearedJetsTemplater%s: run toy #%i\n", name.c_str(), dataset.toy);
    const int N1v = int(dataset.one_vertices->size());
    printf("  # 1v input: %i  2v input: %lu\n", N1v, dataset.two_vertices->size());

    book_toy_fcns_and_histos();
    fill_2v_histos();

    make_templates();

    t_fit_info->Fill();
  }
}
