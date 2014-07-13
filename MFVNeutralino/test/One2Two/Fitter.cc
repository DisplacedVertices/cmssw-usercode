#include "Fitter.h"

#include <cmath>

#include "TCanvas.h"
#include "TFile.h"
#include "TH2.h"
#include "TMinuit.h"
#include "TRandom3.h"
#include "TTree.h"

#include "ProgressBar.h"
#include "ROOTTools.h"
#include "Random.h"

namespace mfv {
  namespace fit {
    int n_bins = -1;

    TH1D* h_sig = 0;
    const double* a_sig = 0;

    Template* curr_bkg_template = 0;
    TH1D* h_bkg = 0;
    const double* a_bkg = 0;

    TH1D* h_data_real = 0;
    TH1D* h_data_toy_sig = 0;
    TH1D* h_data_toy_bkg = 0;
    TH1D* h_data_toy = 0;
    TH1D* h_data = 0;
    const double* a_data = 0;

    void set_or_check_n_bins(TH1D* h) {
      if (n_bins < 0)
        n_bins = h->GetNbinsX();
      else if (h->GetNbinsX() != n_bins)
        jmt::vthrow("%s binning bad: n_bins = %i, h # bins: %i", h->GetName(), n_bins, h->GetNbinsX());
    }

    void set_sig(TH1D* h) {
      set_or_check_n_bins(h);
      h_sig = h;
      a_sig = h->GetArray();
    }

    void set_bkg_no_check(Template* t) {
      curr_bkg_template = t;
      h_bkg = t->h;
      a_bkg = t->h->GetArray();
    }

    void set_bkg(Template* t) {
      set_or_check_n_bins(t->h);
      set_bkg_no_check(t);
    }

    void set_data_no_check(TH1D* h) {
      h_data = h;
      a_data = h->GetArray();
    }

    void set_data_real() {
      set_data_no_check(h_data_real);
    }

    void set_data(TH1D* h) {
      set_or_check_n_bins(h);
      set_data_no_check(h);
    }

    void globals_ok() {
      if (n_bins < 0 || h_data == 0 || curr_bkg_template == 0 || h_sig == 0 || h_data_real == 0)
        jmt::vthrow("fit globals not set up properly: n_bins: %i  h_data: %p  curr_bkg_template: %p  h_sig: %p  h_data_real: %p",
                    n_bins, h_data, curr_bkg_template, h_sig, h_data_real);
    }

    double twolnL(double mu_sig, double mu_bkg) {
      double lnL = 0; //-(mu_sig + mu_bkg);
      for (int i = 1; i <= n_bins; ++i) {
        const double nu_sum = mu_sig * a_sig[i] + mu_bkg * a_bkg[i];
        if (nu_sum > 1e-12)
          lnL += -nu_sum + a_data[i] * log(nu_sum);
        else
          lnL -= 1e-12 + a_data[i] * 27.6310211159285473;
        //printf("i: %i   mu_sig, mu_bkg (%f, %f)   nu_bkg: %f  nu_sig: %f  nu: %f  n: %f    dlnL: %f   lnL: %f\n",
        //     i, mu_sig, mu_bkg, mu_bkg * a_bkg[i], mu_sig * a_sig[i], mu_bkg * a_bkg[i] + mu_sig * a_sig[i], a_data[i], -nu_sum + a_data[i] * (nu_sum > 1e-12 ? log(nu_sum) : -27.6310211159285473), lnL);
      }
      return 2*lnL;
    }

    void minfcn(int&, double*, double& f, double* par, int) {
      f = -twolnL(par[0], par[1]); // + curr_bkg_template->chi2();
    }
  }

  const int Fitter::npars = 2 + Template::max_npars;

  void Fitter::min_lik_t::print(const char* header, const char* indent) const {
    printf("%s%s  istat = %i  maxtwolnL = %10.4e  mu_sig = %7.3f +- %7.3f  mu_bkg = %7.3f +- %7.3f\n", indent, header, istat, maxtwolnL, mu_sig, err_mu_sig, mu_bkg, err_mu_bkg);
  }

  void Fitter::test_stat_t::print(const char* header, const char* indent) const {
    printf("%s:  ok? %i  t = %f\n", header, ok(), t);
    h1.print("h1", indent);
    printf("%s  ^ nuis: %s\n", indent, h1.nuis->title().c_str());
    h0.print("h0", indent);
    printf("%s  ^ nuis: %s\n", indent, h0.nuis->title().c_str());
  }

  std::pair<std::vector<double>, std::vector<double> > Fitter::min_lik_t::get_template_par_ranges(const double up) const {
    std::pair<std::vector<double>, std::vector<double> > ret;
    jmt::vthrow("implement get_template_par_ranges %f", up);
    return ret;
  }

  Fitter::Fitter(const std::string& name_, TFile* f, TRandom* r)
    : name (name_.size() ? " " + name_ : ""),
      uname(name_.size() ? "_" + name_ : ""),

      env("mfvo2t_fitter" + uname),
      print_level(env.get_int("print_level", -1)),
      n_toy_signif(env.get_int("n_toy_signif", 10000)),
      n_toy_limit(env.get_int("n_toy_limit", 1000)),
      print_toys(env.get_bool("print_toys", false)),
      save_toys(env.get_bool("save_toys", false)),
      do_limits(env.get_bool("do_limits", true)),
      mu_sig_limit_step(env.get_double("mu_sig_limit_step", 0.2)),

      fout(f),
      dout(f->mkdir(TString::Format("Fitter%s", uname.c_str()))),
      dtoy(0),
      rand(r),
      seed(r->GetSeed() - jmt::seed_base)
  {
    printf("Fitter%s config:\n", name.c_str());
    printf("print_level: %i\n", print_level);
    printf("n_toy_signif: %i\n", n_toy_signif);
    printf("n_toy_limit: %i\n", n_toy_limit);
    printf("print_toys? %i\n", print_toys);
    printf("save_toys? %i\n", save_toys);
    printf("do_limits? %i\n", do_limits);
    printf("mu_sig_limit_step: %f\n", mu_sig_limit_step);
    fflush(stdout);

    book_trees();
  }

  void Fitter::book_trees() {
    dout->cd();

    TTree* t_config = new TTree("t_config", "");
    t_config->Branch("seed", const_cast<int*>(&seed), "seed/I");
    t_config->Fill();


    t_fit_info = new TTree("t_fit_info", "");
    t_fit_info->Branch("seed", const_cast<int*>(&seed), "seed/I");
    t_fit_info->Branch("toy", &toy, "toy/I");
    t_fit_info->Branch("true_pars", &true_pars);
    t_fit_info->Branch("t_obs_0__h1_istat", &t_obs_0.h1.istat, "t_obs_0__h1_istat/I");
    t_fit_info->Branch("t_obs_0__h1_maxtwolnL", &t_obs_0.h1.maxtwolnL, "t_obs_0__h1_maxtwolnL/D");
    t_fit_info->Branch("t_obs_0__h1_mu_sig", &t_obs_0.h1.mu_sig, "t_obs_0__h1_mu_sig/D");
    t_fit_info->Branch("t_obs_0__h1_err_mu_sig", &t_obs_0.h1.err_mu_sig, "t_obs_0__h1_err_mu_sig/D");
    t_fit_info->Branch("t_obs_0__h1_mu_bkg", &t_obs_0.h1.mu_bkg, "t_obs_0__h1_mu_bkg/D");
    t_fit_info->Branch("t_obs_0__h1_err_mu_bkg", &t_obs_0.h1.err_mu_bkg, "t_obs_0__h1_err_mu_bkg/D");
    t_fit_info->Branch("t_obs_0__h0_istat", &t_obs_0.h0.istat, "t_obs_0__h0_istat/I");
    t_fit_info->Branch("t_obs_0__h0_maxtwolnL", &t_obs_0.h0.maxtwolnL, "t_obs_0__h0_maxtwolnL/D");
    t_fit_info->Branch("t_obs_0__h0_mu_sig", &t_obs_0.h0.mu_sig, "t_obs_0__h0_mu_sig/D");
    t_fit_info->Branch("t_obs_0__h0_err_mu_sig", &t_obs_0.h0.err_mu_sig, "t_obs_0__h0_err_mu_sig/D");
    t_fit_info->Branch("t_obs_0__h0_mu_bkg", &t_obs_0.h0.mu_bkg, "t_obs_0__h0_mu_bkg/D");
    t_fit_info->Branch("t_obs_0__h0_err_mu_bkg", &t_obs_0.h0.err_mu_bkg, "t_obs_0__h0_err_mu_bkg/D");
    t_fit_info->Branch("t_obs_0__t", &t_obs_0.t, "t_obs_0__t/D");
    t_fit_info->Branch("pval_signif", &pval_signif, "pval_signif/D");
    t_fit_info->Branch("t_obs_limit__h1_istat", &t_obs_limit.h1.istat, "t_obs_limit__h1_istat/I");
    t_fit_info->Branch("t_obs_limit__h1_maxtwolnL", &t_obs_limit.h1.maxtwolnL, "t_obs_limit__h1_maxtwolnL/D");
    t_fit_info->Branch("t_obs_limit__h1_mu_sig", &t_obs_limit.h1.mu_sig, "t_obs_limit__h1_mu_sig/D");
    t_fit_info->Branch("t_obs_limit__h1_err_mu_sig", &t_obs_limit.h1.err_mu_sig, "t_obs_limit__h1_err_mu_sig/D");
    t_fit_info->Branch("t_obs_limit__h1_mu_bkg", &t_obs_limit.h1.mu_bkg, "t_obs_limit__h1_mu_bkg/D");
    t_fit_info->Branch("t_obs_limit__h1_err_mu_bkg", &t_obs_limit.h1.err_mu_bkg, "t_obs_limit__h1_err_mu_bkg/D");
    t_fit_info->Branch("t_obs_limit__h0_istat", &t_obs_limit.h0.istat, "t_obs_limit__h0_istat/I");
    t_fit_info->Branch("t_obs_limit__h0_maxtwolnL", &t_obs_limit.h0.maxtwolnL, "t_obs_limit__h0_maxtwolnL/D");
    t_fit_info->Branch("t_obs_limit__h0_mu_sig", &t_obs_limit.h0.mu_sig, "t_obs_limit__h0_mu_sig/D");
    t_fit_info->Branch("t_obs_limit__h0_err_mu_sig", &t_obs_limit.h0.err_mu_sig, "t_obs_limit__h0_err_mu_sig/D");
    t_fit_info->Branch("t_obs_limit__h0_mu_bkg", &t_obs_limit.h0.mu_bkg, "t_obs_limit__h0_mu_bkg/D");
    t_fit_info->Branch("t_obs_limit__h0_err_mu_bkg", &t_obs_limit.h0.err_mu_bkg, "t_obs_limit__h0_err_mu_bkg/D");
    t_fit_info->Branch("t_obs_limit__t", &t_obs_limit.t, "t_obs_limit__t/D");
    t_fit_info->Branch("pval_limits", &pval_limits);
    t_fit_info->Branch("mu_sig_limits", &mu_sig_limits);
    t_fit_info->Branch("pval_limit", &pval_limit, "pval_limit/D");
    t_fit_info->Branch("mu_sig_limit", &mu_sig_limit, "mu_sig_limit/D");
  }    

  void Fitter::draw_likelihood(const test_stat_t& t) {
    printf("draw_likelihood: ");

    const int n_mu_sig = 200;
    const int n_mu_bkg = 200;
    const double mu_sig_min = 0;
    const double mu_sig_max = 200;
    const double mu_bkg_min = 0;
    const double mu_bkg_max = 200;
    const double d_mu_sig = (mu_sig_max - mu_sig_min)/n_mu_sig;
    const double d_mu_bkg = (mu_bkg_max - mu_bkg_min)/n_mu_bkg;

    for (int sb = 1; sb >= 0; --sb) {
      const char* sb_or_b = sb ? "sb" : "b";
      printf("%s ", sb_or_b); fflush(stdout);
      const char* sb_or_b_nice = sb ? "sig + bkg" : "b only";
      const min_lik_t& ml = sb ? t.h1 : t.h0;
      TH1F* h = new TH1F(TString::Format("h_likelihood_%s_scannuis", sb_or_b),
                         TString::Format("Best %s fit: #hat{#mu_{sig}} = %.3f  #hat{#mu_{bkg}} = %.3f  #hat{nuis}: %s", sb_or_b_nice, ml.mu_sig, ml.mu_bkg, ml.nuis->title().c_str()),
                         bkg_templates->size(), 0, bkg_templates->size() );

      for (size_t i_template = 0, i_template_e = bkg_templates->size(); i_template < i_template_e; ++i_template) {
        Template* bkg_template =  bkg_templates->at(i_template);
        fit::set_bkg(bkg_template);
        const int ibin = int(i_template + 1);

        h->SetBinContent(ibin, fit::twolnL(ml.mu_sig, ml.mu_bkg));
        h->GetXaxis()->SetBinLabel(ibin, bkg_template->title().c_str());
      }

      h->GetXaxis()->LabelsOption("v");

      TH2F* h2 = new TH2F(TString::Format("h_likelihood_%s_scanmus", sb_or_b),
                          TString::Format("Best %s fit: %s;#mu_{sig};#mu_{bkg}", sb_or_b_nice, ml.nuis->title().c_str()),
                          n_mu_sig, mu_sig_min, mu_sig_max,
                          n_mu_bkg, mu_bkg_min, mu_bkg_max
                          );

      fit::set_bkg(ml.nuis);

      for (int i_mu_sig = 1; i_mu_sig < n_mu_sig; ++i_mu_sig) {
        const double mu_sig = mu_sig_min + i_mu_sig * d_mu_sig;
        for (int i_mu_bkg = 1; i_mu_bkg < n_mu_bkg; ++i_mu_bkg) {
          const double mu_bkg = mu_bkg_min + i_mu_bkg * d_mu_bkg;
          h2->SetBinContent(i_mu_sig, i_mu_bkg, fit::twolnL(mu_sig, mu_bkg));
        }
      }
    }

    printf("\n");
  }

  void Fitter::draw_fit(const test_stat_t& t) {
    for (int sb = 1; sb >= 0; --sb) {
      const char* sb_or_b = sb ? "sb" : "b";
      const char* sb_or_b_nice = sb ? "sig + bkg" : "b only";
      const min_lik_t& ml = sb ? t.h1 : t.h0;
      TCanvas* c = new TCanvas(TString::Format("c_%s_fit", sb_or_b));

      TH1D* h_bkg_fit  = (TH1D*)ml.nuis->h ->Clone(TString::Format("h_bkg_%s_fit",  sb_or_b));
      TH1D* h_sig_fit  = (TH1D*)fit::h_sig ->Clone(TString::Format("h_sig_%s_fit",  sb_or_b));
      TH1D* h_data_fit = (TH1D*)fit::h_data->Clone(TString::Format("h_data_%s_fit", sb_or_b));

      for (TH1D* h : {h_bkg_fit, h_sig_fit, h_data_fit}) {
        h->SetLineWidth(2);
        jmt::divide_by_bin_width(h);
      }

      h_sig_fit->SetLineColor(kRed);
      h_sig_fit->SetFillColor(kRed);
      h_sig_fit->SetFillStyle(3004);
      h_bkg_fit->SetLineColor(kBlue);
      h_bkg_fit->SetFillColor(kBlue);
      h_bkg_fit->SetFillStyle(3005);

      h_sig_fit->Scale(ml.mu_sig);
      h_bkg_fit->Scale(ml.mu_bkg);

      TH1D* h_sum_fit = (TH1D*)h_sig_fit->Clone(TString::Format("h_sum_%s_fit", sb_or_b));
      h_sum_fit->SetLineColor(kMagenta);
      h_sum_fit->Add(h_bkg_fit);
      for (TH1D* h : {h_sum_fit, h_data_fit})
        h->SetTitle(TString::Format("best %s fit with #mu_{sig} = %.2f #pm %.2f, #mu_{bkg} = %.2f #pm %.2f, %s;svdist2d (cm);events/bin width", sb_or_b_nice, ml.mu_sig, ml.err_mu_sig, ml.mu_bkg, ml.err_mu_bkg, ml.nuis->title().c_str()));

      if (h_data_fit->GetMaximum() > h_sum_fit->GetMaximum()) {
        h_data_fit->Draw("e");
        h_sum_fit->Draw("hist same");
      }
      else {
        h_sum_fit->Draw("hist");
        h_data_fit->Draw("same e");
      }
      h_sig_fit->Draw("same hist");
      h_bkg_fit->Draw("same hist");
      c->Write();
      delete c;
    }
  }

  Fitter::min_lik_t Fitter::scanmin_likelihood(double mu_sig_start, bool fix_mu_sig) {
    fit::globals_ok();

    min_lik_t ret;

    //printf("scanminning (mu_sig_start = %f, fix? %i):\n", mu_sig_start, fix_mu_sig);

    //TDirectory* d = dtoy->mkdir(TString::Format("scanmin_likelihood_%s", bkg_only ? "b" : "sb"));
    //d->cd();

    for (size_t i_template = 0, i_template_e = bkg_templates->size(); i_template < i_template_e; ++i_template) {
      Template* bkg_template = bkg_templates->at(i_template);
      fit::set_bkg(bkg_template);

      TMinuit* m = new TMinuit(2);
      m->SetPrintLevel(print_level);
      m->SetFCN(fit::minfcn);
      int ierr;
      m->mnparm(0, "mu_sig", (mu_sig_start > 0 ? mu_sig_start : 0), 0.1, 0, (mu_sig_start > 0 ? mu_sig_start : 5000), ierr);
      m->mnparm(1, "mu_bkg", 50, 0.1, 0, 5000, ierr);

      if (fix_mu_sig)
        m->FixParameter(0);

      m->Migrad();
      //      m->mnmnos();
      double fmin, fedm, errdef;
      int npari, nparx, istat;
      m->mnstat(fmin, fedm, errdef, npari, nparx, istat);

      const double maxtwolnL = -fmin;
      double mu_sig, err_mu_sig, mu_bkg, err_mu_bkg;
      m->GetParameter(0, mu_sig, err_mu_sig);
      m->GetParameter(1, mu_bkg, err_mu_bkg);

      //printf("scanmin_likelihood: %s  istat: %i   maxtwolnL: %e   mu_sig: %f +- %f  mu_bkg: %f +- %f\n", bkg_template->title().c_str(), istat, maxtwolnL, mu_sig, err_mu_sig, mu_bkg, err_mu_bkg);

      if (maxtwolnL > ret.maxtwolnL) {
        ret.ok = istat == 3;
        ret.istat = istat;
        ret.maxtwolnL = maxtwolnL;
        ret.mu_sig = mu_sig;
        ret.mu_bkg = mu_bkg;
        ret.err_mu_sig = err_mu_sig;
        ret.err_mu_bkg = err_mu_bkg;
        ret.nuis = bkg_template;
      }

      if (istat != 3)
        ret.all_ok = false;

      ret.nuis_region.push_back(std::make_pair(maxtwolnL, bkg_template));

      delete m;
    }

    return ret;
  }

  Fitter::test_stat_t Fitter::calc_test_stat(double fix_mu_sig_val) {
    test_stat_t t;
    t.h1 = scanmin_likelihood(fix_mu_sig_val, false);
    t.h0 = scanmin_likelihood(fix_mu_sig_val, true);
    t.t = t.h1.maxtwolnL - t.h0.maxtwolnL;
    return t;
  }

  void Fitter::make_toy_data(int i_toy_signif, int i_toy_limit, int n_sig, int n_bkg) {
    delete fit::h_data_toy_sig;
    delete fit::h_data_toy_bkg;
    delete fit::h_data_toy;

    char s[128], s2[128];
    if (i_toy_signif < 0 && i_toy_limit < 0)
      snprintf(s, 128, "h_%%s_seed%02i_toy%02i", seed, toy);
    else if (i_toy_limit < 0)
      snprintf(s, 128, "h_%%s_seed%02i_toy%02i_signif%02i", seed, toy, i_toy_signif);
    else if (i_toy_signif < 0)
      snprintf(s, 128, "h_%%s_seed%02i_toy%02i_limit%02i", seed, toy, i_toy_limit);

    snprintf(s2, 128, s, "data_toy_sig"); fit::h_data_toy_sig = Template::hist_with_binning(s2, "");
    snprintf(s2, 128, s, "data_toy_bkg"); fit::h_data_toy_bkg = Template::hist_with_binning(s2, "");
    snprintf(s2, 128, s, "data_toy");     fit::h_data_toy     = Template::hist_with_binning(s2, "");

    for (TH1D* h : {fit::h_data_toy_sig, fit::h_data_toy_bkg, fit::h_data_toy}) {
      h->SetLineWidth(2);
      h->SetDirectory(0);
    }
  
    fit::h_data_toy_sig->FillRandom(fit::h_sig, n_sig);
    fit::h_data_toy_bkg->FillRandom(fit::curr_bkg_template->h, n_bkg);

    fit::h_data_toy->Add(fit::h_data_toy_sig);
    fit::h_data_toy->Add(fit::h_data_toy_bkg);
    fit::set_data_no_check(fit::h_data_toy);
  }

  void Fitter::fit(int toy_, Templates* bkg_templates_, TH1D* sig_template, const VertexPairs& v2v, const std::vector<double>& true_pars_) {
    toy = toy_;
    true_pars = true_pars_;

    dtoy = dout->mkdir(TString::Format("seed%02i_toy%02i", seed, toy));

    ////

    dtoy->mkdir("finalized_templates")->cd();

    fit::set_sig(Template::finalize_template(sig_template));

    bkg_templates = bkg_templates_;
    fit::set_bkg((*bkg_templates)[0]);

    TH1D* h_data_temp = Template::hist_with_binning("h_data", TString::Format("toy %i", toy));
    for (const VertexPair& p : v2v)
      h_data_temp->Fill(p.d2d());
    fit::h_data_real = Template::finalize_binning(h_data_temp);
    fit::set_data_real();
    const int n_data = fit::h_data_real->Integral();
    delete h_data_temp;

    ////

    dtoy->mkdir("fit_results")->cd();

    printf("Fitter: toy: %i  n_sig_true: %f  n_bkg_true: %f  true_pars:", toy, true_pars[0], true_pars[1]);
    for (double tp : true_pars)
      printf(" %f", tp);
    printf("\n");

    t_obs_0 = calc_test_stat(0);
    t_obs_0.print("t_obs_0");

    pval_signif = 1;
    pval_limits.clear();
    mu_sig_limits.clear();
    t_obs_limit = test_stat_t();
    mu_sig_limit = 1e-6;
    pval_limit = 1;

    //scan_likelihood();
    draw_likelihood(t_obs_0);
    draw_fit(t_obs_0);

    printf("throwing %i significance toys:\n", n_toy_signif);
    jmt::ProgressBar pb_signif(50, n_toy_signif);
    if (!print_toys)
      pb_signif.start();

    int n_toy_signif_t_ge_obs = 0;

    for (int i_toy_signif = 0; i_toy_signif < n_toy_signif; ++i_toy_signif) {
      const int n_sig_signif = 0;
      const int n_bkg_signif = rand->Poisson(n_data);
      make_toy_data(i_toy_signif, -1, n_sig_signif, n_bkg_signif);
      
      const test_stat_t t = calc_test_stat(0);
      if (t.t >= t_obs_0.t)
        ++n_toy_signif_t_ge_obs;

      if (print_toys) {
        t.print("t_signif toy %i");
      }
      else
        ++pb_signif;

      if (save_toys) {
        jmt::vthrow("save signif toys not implemented");
      }
    }

    pval_signif = double(n_toy_signif_t_ge_obs) / n_toy_signif;
    printf("\npval_signif: %e\n", pval_signif); fflush(stdout);

    if (do_limits) {
      mu_sig_limit = 1e-6;
      pval_limit = 1;
      std::vector<test_stat_t> t_obs_limits;
      const double limit_alpha = 0.05;
      const double mu_sig_limit_stop = n_data;

      jmt::ProgressBar pb_limits(50, mu_sig_limit_stop / mu_sig_limit_step);
      if (!print_toys)
        pb_limits.start();

      printf("scanning for %.1f%% upper limit: ", 100*(1-limit_alpha));
      while (mu_sig_limit < mu_sig_limit_stop) {
        fit::set_data_real();
        const test_stat_t t_obs_limit_ = calc_test_stat(mu_sig_limit);

        if (print_toys) {
          printf("mu_sig_limit: %f  ", mu_sig_limit);
          t_obs_limit_.print("t_obs_limit");
        }
        else
          ++pb_limits;

        if (save_toys) {
          jmt::vthrow("save limit toys not implemented");
        }

        int n_toy_limit_t_ge_obs = 0;
        for (int i_toy_limit = 0; i_toy_limit < n_toy_limit; ++i_toy_limit) {
          const int n_sig_limit = rand->Poisson(mu_sig_limit);
          const int n_bkg_limit = rand->Poisson(n_data - mu_sig_limit);

          make_toy_data(-1, i_toy_limit, n_sig_limit, n_bkg_limit);
      
          const test_stat_t t = calc_test_stat(mu_sig_limit);
          if (t.t > t_obs_limit_.t)
            ++n_toy_limit_t_ge_obs;

          if (print_toys) {
            printf("limit toy %i nsig %i nbkg %i n'data' %i\n", i_toy_limit, n_sig_limit, n_bkg_limit, n_data);
            t.print("t_limit");
          }

          if (save_toys) {
            jmt::vthrow("save toys for limits not implemented");
          }
        }

        pval_limit = double(n_toy_limit_t_ge_obs) / n_toy_limit;

        pval_limits.push_back(pval_limit);
        mu_sig_limits.push_back(mu_sig_limit);
        t_obs_limits.push_back(t_obs_limit_);

        mu_sig_limit += mu_sig_limit_step;
      }
      printf("\n");

      int i;
      for (i = int(pval_limits.size())-1; i >= 0; --i)
        if (pval_limits[i] > limit_alpha)
          break;
      pval_limit = pval_limits[i+1];
      mu_sig_limit = mu_sig_limits[i+1];
      t_obs_limit = t_obs_limits[i+1];


      printf("pval_limit: %e  mu_sig_limit: %f\n", pval_limit, mu_sig_limit);
    }

    t_fit_info->Fill();
  }
}
