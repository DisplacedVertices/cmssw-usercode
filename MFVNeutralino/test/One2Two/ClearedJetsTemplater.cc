#include "ClearedJetsTemplater.h"
#include "TFile.h"
#include "TH1.h"
#include "TMath.h"
#include "TRandom3.h"
#include "TTree.h"
#include "ProgressBar.h"

namespace mfv {
  std::vector<TemplatePar> ClearedJetsTemplater::par_info() const {
    return std::vector<TemplatePar>({
        { n_clearing_mu, clearing_mu_start, d_clearing_mu },
        { n_clearing_sigma, clearing_sigma_start, d_clearing_sigma }
      });
  }

  ClearedJetsTemplater::ClearedJetsTemplater(const std::string& name_, TFile* f, TRandom* r)
    : Templater("ClearedJets", name_, f, r),

      env("mfvo2t_clearedjets" + uname),
      d2d_cut(env.get_double("d2d_cut", 0.05)),
      save_templates(env.get_bool("save_templates", false)),
      sample_count(env.get_int("sample_count", -1)),
      flat_phis(env.get_bool("flat_phis", false)),
      phi_from_jet_mu(env.get_double("phi_from_jet_mu", M_PI_2)),
      phi_from_jet_sigma(env.get_double("phi_from_jet_sigma", 0.4)),
      clearing_mu_start(env.get_double("clearing_mu_start", 0.)),
      d_clearing_mu(env.get_double("d_clearing_mu", 0.0005)),
      n_clearing_mu(env.get_int("n_clearing_mu", 180)),
      clearing_sigma_start(env.get_double("clearing_sigma_start", 0.0005)),
      d_clearing_sigma(env.get_double("d_clearing_sigma", 0.0005)),
      n_clearing_sigma(env.get_int("n_clearing_sigma", 100)),

      clearing_mu_fit(0.028),
      clearing_sigma_fit(0.005)
  {
    printf("ClearedJetsTemplater%s config:\n", name.c_str());
    printf("d2d_cut: %f\n", d2d_cut);
    printf("sample_count: %i\n", sample_count);
    if (flat_phis)
      printf("phis thrown flat\n");
    else
      printf("phi_from_jet ~ Gaus(%f, %f)\n", phi_from_jet_mu, phi_from_jet_sigma);
    printf("clearing_mu: %i increments of %f starting from %f\n", n_clearing_mu, d_clearing_mu, clearing_mu_start);
    printf("clearing_sigma: %i increments of %f starting from %f\n", n_clearing_sigma, d_clearing_sigma, clearing_sigma_start);

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

  double ClearedJetsTemplater::throw_phi(const EventSimple& ev) const {
    if (flat_phis)
      return rand->Uniform(-M_PI, M_PI);

    double sumpt = 0;
    for (unsigned short j = 0; j < ev.njets; ++j)
      sumpt += ev.jet_pt[j];

    const double r = rand->Rndm();
    double rjetphi = 0;
    double cumpt = 0;
    for (unsigned short j = 0; j < ev.njets; ++j) {
      cumpt += ev.jet_pt[j];
      if (r < cumpt/sumpt) {
        rjetphi = ev.jet_phi[j];
        break;
      }
    }

    const double rdphi = rand->Gaus(phi_from_jet_mu, phi_from_jet_sigma);
    const int pm = rand->Rndm() < 0.5 ? -1 : 1;
    return TVector2::Phi_mpi_pi(rjetphi + pm * rdphi);
  }

  void ClearedJetsTemplater::make_templates() {
    dataset_ok();

    printf("ClearedJetsTemplater%s making templates\n", name.c_str()); fflush(stdout);
    jmt::ProgressBar pb(50, dataset.events_1v->size());
    pb.start();

    clear_templates();

    TDirectory* dtemp = 0;
    if (save_templates) {
      dtemp = dtoy->mkdir("templates");
      dtemp->cd();
    }

    int iglb = 0;
    for (int imu = 0; imu < n_clearing_mu; ++imu) {
      const double clearing_mu = clearing_mu_start + imu * d_clearing_mu;

      if (save_templates)
        dtemp->mkdir(TString::Format("imu_%02i", imu))->cd();

      for (int isig = 0; isig < n_clearing_sigma; ++isig) {
        const double clearing_sigma = clearing_sigma_start + isig * d_clearing_sigma;

        TH1D* h = Template::hist_with_binning(TString::Format("h_template_imu%03i_isig%03i", imu, isig),
                                              TString::Format("clearing pars: #mu = %f  #sigma = %f", clearing_mu, clearing_sigma));
        if (!save_templates)
          h->SetDirectory(0);

        templates.push_back(new ClearedJetsTemplate(iglb++, h, clearing_mu, clearing_sigma));
      }
    }

    for (const EventSimple& ev : *dataset.events_1v) {
      if (ev.njets > 0) {
        const double bsd2d0 = h_bsd2d[vt_1vsingle]->GetRandom();
        const double bsd2d1 = h_bsd2d[vt_1vsingle]->GetRandom();

        const double phi0 = throw_phi(ev);
        const double phi1 = throw_phi(ev);

        const double d2d = sqrt(bsd2d0*bsd2d0 + bsd2d1*bsd2d1 - 2*bsd2d0*bsd2d1*cos(TVector2::Phi_mpi_pi(phi0 - phi1)));

        for (Template* t : templates) {
          ClearedJetsTemplate* cjt = dynamic_cast<ClearedJetsTemplate*>(t);
          //const double w = std::max(1e-12, 0.5*TMath::Erf((d2d - cjt->clearing_mu)/cjt->clearing_sigma) + 0.5);
          const double w = 0.5*TMath::Erf((d2d - cjt->clearing_mu)/cjt->clearing_sigma) + 0.5;
          t->h->Fill(d2d, w);
        }
      }

      ++pb;
    }

    for (Template* t : templates)
      Template::finalize_template_in_place(t->h);

    printf("\n");
  }

  void ClearedJetsTemplater::process_imp() {
    printf("ClearedJetsTemplater%s: run toy #%i\n", name.c_str(), dataset.toy);
    const int N1v = int(dataset.one_vertices->size());
    printf("  # 1v input: %i  2v input: %lu\n", N1v, dataset.two_vertices->size());

    book_toy_fcns_and_histos();
    fill_2v_histos();

    for (int iv = 0; iv < N1v; ++iv) {
      const VertexSimple& v0 = dataset.one_vertices->at(iv);
      fill_2v(vt_1vsingle, 1, v0, v0);
    }

    make_templates();

    t_fit_info->Fill();
  }
}
