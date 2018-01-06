#include "ClearedJetsTemplater.h"
#include "TFile.h"
#include "TF1.h"
#include "TH1.h"
#include "TKey.h"
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
      load_from_file(env.get_bool("load_from_file", false)),
      load_from_file_fn(env.get_string("load_from_file_fn", "mfvo2t_templates.root")),
      load_from_file_path(env.get_string("load_from_file_path", "ClearedJetsTemplater/seed0000_toy0000/templates")),
      save_templates(env.get_bool("save_templates", false)),
      finalize_templates(env.get_bool("finalize_templates", true)),
      sample_every(env.get_int("sample_every", -1)),
      sample_count(env.get_int("sample_count", -1)),
      throw_h_bsd2d(env.get_bool("throw_h_bsd2d", false)),
      throw_dphi_from_2v(env.get_bool("throw_dphi_from_2v", false)),
      flat_phis(env.get_bool("flat_phis", false)),
      phi_from_jet_mu(env.get_double("phi_from_jet_mu", M_PI_2)),
      phi_from_jet_sigma(env.get_double("phi_from_jet_sigma", 0.4)),
      dphi_from_pdf(env.get_bool("dphi_from_pdf", false)),
      dphi_pdf_c(env.get_double("dphi_pdf_c", 0.)),
      dphi_pdf_e(env.get_double("dphi_pdf_e", 0.)),
      dphi_pdf_a(env.get_double("dphi_pdf_a", 0.)),
      n_scale(env.get_int("n_scale", 1)),
      fixed_clearing(env.get_bool("fixed_clearing", false)),
      clearing_mu_start(env.get_double("clearing_mu_start", 0.)),
      d_clearing_mu(env.get_double("d_clearing_mu", 0.0005 * n_scale)),
      n_clearing_mu(env.get_int("n_clearing_mu", fixed_clearing ? 2 : 180 / n_scale)),
      clearing_sigma_start(env.get_double("clearing_sigma_start", 0.0005)),
      d_clearing_sigma(env.get_double("d_clearing_sigma", 0.0005 * n_scale)),
      n_clearing_sigma(env.get_int("n_clearing_sigma", fixed_clearing ? 2 : 100 / n_scale)),

      clearing_mu_fit(0.028),
      clearing_sigma_fit(0.005),

      t_fit_info(0),
      f_dphi(0)
  {
    printf("ClearedJetsTemplater%s config:\n", name.c_str());
    if (load_from_file)
      printf("loading templates from %s:%s\n", load_from_file_fn.c_str(), load_from_file_path.c_str());
    else {
      printf("d2d_cut: %f\n", d2d_cut);
      printf("sample_count: %i\n", sample_count);
      if (int(throw_dphi_from_2v) + int(flat_phis) + int(dphi_from_pdf) > 1)
        jmt::vthrow("can only pick one phi throwing method");

      if (dphi_from_pdf)
        printf("dphi from pdf: c: %f e: %f a: %f\n", dphi_pdf_c, dphi_pdf_e, dphi_pdf_a);
      else if (throw_dphi_from_2v)
        printf("dphi thrown from 2v hist\n");
      else {
        if (flat_phis)
          printf("phis thrown flat\n");
        else
          printf("phi_from_jet ~ Gaus(%f, %f)\n", phi_from_jet_mu, phi_from_jet_sigma);
      }
    }

    if (fixed_clearing)
      printf("clearing pars fixed around clearing_mu %f and clearing_sigma %f\n", clearing_mu_start, clearing_sigma_start);
    else {
      printf("clearing_mu: %i increments of %f starting from %f\n", n_clearing_mu, d_clearing_mu, clearing_mu_start);
      printf("clearing_sigma: %i increments of %f starting from %f\n", n_clearing_sigma, d_clearing_sigma, clearing_sigma_start);
    }

    fflush(stdout);

    book_trees();

    if (dphi_from_pdf) {
      f_dphi = new TF1("f_dphi", "abs(x - [0])**[1] + [2]", -M_PI, M_PI);
      f_dphi->SetParameters(dphi_pdf_c, dphi_pdf_e, dphi_pdf_a);

      TH1F* h_dphi_test = new TH1F("h_dphi_test", "", 20, -M_PI, M_PI);
      h_dphi_test->FillRandom("f_dphi", 10000);
    }
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

    clear_templates();
    int iglb = 0;

    if (load_from_file) {
      TDirectory* previous_d = gDirectory->GetDirectory(gDirectory->GetPath());

      TFile* f = new TFile(load_from_file_fn.c_str());
      if (!f || !f->IsOpen())
        jmt::vthrow("could not open templates file %s", load_from_file_fn.c_str());
      TDirectory* d = (TDirectory*)f->Get(load_from_file_path.c_str());
      if (!d)
        jmt::vthrow("could not get template directory %s:%s", load_from_file_fn.c_str(), load_from_file_path.c_str());

      int imu = 0;
      TIter it_mu(d->GetListOfKeys());
      TKey* k_mu;
      while ((k_mu = (TKey*)it_mu())) {
        TDirectory* d_mu = (TDirectory*)k_mu->ReadObj();
        TString n_mu = d_mu->GetName();
        n_mu.ReplaceAll("imu_", "");
        const int imu_check = n_mu.Atoi();
        if (imu != imu_check)
          jmt::vthrow("problem reading template directory in %s:%s : %s != imu_%02i", load_from_file_fn.c_str(), load_from_file_path.c_str(), n_mu.Data(), imu);

        int isig = 0;
        TIter it_sig(d_mu->GetListOfKeys());
        TKey* k_sig;
        while ((k_sig = (TKey*)it_sig())) {
          TH1D* h = (TH1D*)k_sig->ReadObj();

          TString n_sig = h->GetName();
          n_sig.ReplaceAll(TString::Format("h_template_imu%03i_isig", imu), "");
          const int isig_check = n_sig.Atoi();
          if (isig != isig_check)
            jmt::vthrow("problem reading template directory in %s:%s : %s != isig_%03i", load_from_file_fn.c_str(), load_from_file_path.c_str(), n_sig.Data(), isig);

          TString title = h->GetTitle();
          TObjArray* arr = title.Tokenize(" ");
          if (arr->GetEntries() != 8)
            jmt::vthrow("cannot parse title %s", title.Data());
          const double mu  = ((TObjString*)arr->At(4))->GetString().Atof();
          const double sig = ((TObjString*)arr->At(7))->GetString().Atof();
          delete arr;

          const double clearing_mu = clearing_mu_start + imu * d_clearing_mu;
          const double clearing_sigma = clearing_sigma_start + isig * d_clearing_sigma;

          if (mu < 0 || mu > 0.1 || sig < 0 || sig > 0.1 || fabs(clearing_mu - mu) > 1e-4 || fabs(clearing_sigma - sig) > 1e-4)
            jmt::vthrow("something wrong with parsing %s into %f and %f", h->GetTitle(), mu, sig);

          TH1D* hh = (TH1D*)h->Clone();
          hh->SetDirectory(0);
          templates.push_back(new ClearedJetsTemplate(iglb++, hh, clearing_mu, clearing_sigma));

          ++isig;
        }

        ++imu;
      }

      f->Close();
      delete f;
      previous_d->cd();
      return;
    }

    const int N1v = sample_count > 0 ? sample_count : int(dataset.events_1v->size());
    printf("ClearedJetsTemplater%s making templates\n", name.c_str()); fflush(stdout);
    jmt::ProgressBar pb(50, N1v / (sample_every > 0 ? sample_every : 1));
    pb.start();

    TDirectory* dtemp = 0;
    if (save_templates) {
      dtemp = dtoy->mkdir("templates");
      dtemp->cd();
    }

    for (int imu = 0; imu < n_clearing_mu; ++imu) {
      const double clearing_mu = clearing_mu_start + imu * d_clearing_mu;

      if (save_templates)
        dtemp->mkdir(TString::Format("imu_%02i", imu))->cd();

      for (int isig = 0; isig < n_clearing_sigma; ++isig) {
        const double clearing_sigma = clearing_sigma_start + isig * d_clearing_sigma;

        TH1D* h = Template::hist_with_binning(TString::Format("h_template_imu%03i_isig%03i", imu, isig),
                                              TString::Format("clearing pars: #mu = %f  #sigma = %f", clearing_mu, clearing_sigma));

        templates.push_back(new ClearedJetsTemplate(iglb++, h, clearing_mu, clearing_sigma));
        if (!save_templates) {
          h->SetDirectory(0);
          templates.back()->h_phi->SetDirectory(0);
        }
      }
    }

    TH1D* h_bsd2d_use = h_bsd2d[vt_1vsingle];
    TH1D* h_bsd2d0_use = h_bsd2d0[vt_1vsingle];
    TH1D* h_bsd2d1_use = h_bsd2d1[vt_1vsingle];
    if (throw_h_bsd2d) {
      h_bsd2d_use = (TH1D*)h_bsd2d_use->Clone("h_bsd2d_use");
      h_bsd2d_use->SetDirectory(0);
      h_bsd2d_use->Reset();
      h_bsd2d_use->FillRandom(h_bsd2d[vt_1vsingle], rand->Poisson(dataset.events_1v->size()));
    }

    int evc = 0;
    for (const EventSimple& ev : *dataset.events_1v) {
      if (sample_every > 0 && evc % sample_every != 0) {
        ++evc;
        continue;
      }

      if (ev.njets > 0) {
        const double bsd2d0 = h_bsd2d0_use->GetRandom();
        const double bsd2d1 = h_bsd2d1_use->GetRandom();

        double dphi = 0;
        if (dphi_from_pdf)
          dphi = f_dphi->GetRandom();
        else if (throw_dphi_from_2v)
          dphi = h_phi[vt_2v]->GetRandom();
        else {
          const double phi0 = throw_phi(ev);
          const double phi1 = throw_phi(ev);
          dphi = TVector2::Phi_mpi_pi(phi0 - phi1);
        }

        const double d2d = sqrt(bsd2d0*bsd2d0 + bsd2d1*bsd2d1 - 2*bsd2d0*bsd2d1*cos(dphi));

        for (Template* t : templates) {
          ClearedJetsTemplate* cjt = dynamic_cast<ClearedJetsTemplate*>(t);
          const double w = std::max(1e-12, 0.5*TMath::Erf((d2d - cjt->clearing_mu)/cjt->clearing_sigma) + 0.5);
          //const double w = 0.5*TMath::Erf((d2d - cjt->clearing_mu)/cjt->clearing_sigma) + 0.5;
          t->h->Fill(d2d, w);
          t->h_phi->Fill(dphi, w);
        }
      }

      ++pb;
      if (++evc == N1v)
        break;
    }

    if (throw_h_bsd2d)
      delete h_bsd2d_use;

    for (Template* t : templates)
      if (t->h->Integral() < 1e-6) {
        t->h->SetBinContent(t->h->GetNbinsX(), 1);
        t->h->SetBinError(t->h->GetNbinsX(), 1);
      }

    if (finalize_templates)
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
