#include "Fitter.h"

#include <cmath>

#include "TCanvas.h"
#include "TFile.h"
#include "TH2.h"
#include "TMinuit.h"
#include "TRandom3.h"
#include "TTree.h"

#include "ROOTTools.h"
#include "Random.h"

namespace mfv {
  namespace fit {
    int n_bins = -1;
    TH1D* h_data_real = 0;
    TH1D* h_data_sig = 0;
    TH1D* h_data_bkg = 0;
    TH1D* h_data = 0;
    Template* curr_bkg_template = 0;
    TH1D* h_sig = 0;

    double twolnL(double mu_sig, double mu_bkg) {
      const TH1D* h_bkg = curr_bkg_template->h_final;
      double lnL = 0;
      for (int i = 1; i <= n_bins; ++i) {
        const double nu_sig = mu_sig * h_sig->GetBinContent(i);
        const double nu_bkg = mu_bkg * h_bkg->GetBinContent(i);
        const double nu_sum = nu_sig + nu_bkg;
        const double nu = nu_sum > 1e-12 ? nu_sum : 1e-12;
        const double n = h_data->GetBinContent(i);
        //if (n > 0 && nu_sum == 0)
        //  jmt::vthrow("in twolnL, n = %f and nu = 0 for bin i = %i", n, i);
        const double dlnL = -nu + n * log(nu);
        lnL += dlnL;
        //        printf("i: %i   mu_sig, mu_bkg (%f, %f)   nu_bkg: %f  nu_sig: %f  nu: %f  n: %f    dlnL: %f   lnL: %f\n",
        //               i, mu_sig, mu_bkg, nu_bkg, nu_sig, nu, n, dlnL, lnL);
      }
      return 2*lnL;
    }

    void minfcn(int&, double*, double& f, double* par, int) {
      f = -twolnL(par[0], par[1]); // + curr_bkg_template->chi2();
    }
  }

  const int Fitter::npars = 2 + Template::max_npars;

  void Fitter::min_lik_t::print(const char* header, const char* indent) const {
    printf("%s%s  istat = %i  max_value = %10.4e  mu_sig = %7.3f +- %7.3f  mu_bkg = %7.3f +- %7.3f\n", indent, header, istat, maxtwolnL, mu_sig, err_mu_sig, mu_bkg, err_mu_bkg);
  }

  void Fitter::test_stat_t::print(const char* header, const char* indent) const {
    printf("%s:  ok? %i  t = %f\n", header, ok(), t);
    h1.print("h1", indent);
    h0.print("h0", indent);
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
      n_toy_limit(env.get_int("n_toy_limit", 5000)),
      print_toys(env.get_bool("print_toys", false)),
      save_toys(env.get_bool("save_toys", false)),
      do_limits(env.get_bool("do_limits", true)),
      mu_sig_limit_step(env.get_double("mu_sig_limit_step", 0.05)),

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

  std::vector<double> Fitter::binning() const {
    std::vector<double> bins;
    for (int i = 0; i < 20; ++i)
      bins.push_back(i * 0.01);
    bins.push_back(0.2);
    bins.push_back(0.4);
    bins.push_back(0.6);
    bins.push_back(1);
    bins.push_back(3);
    if (fit::n_bins < 0)
      fit::n_bins = bins.size() - 1;
    return bins;
  }

  TH1D* Fitter::hist_with_binning(const TString& name_, const TString& title) {
    std::vector<double> bins = binning();
    return new TH1D(name_, title, bins.size()-1, &bins[0]);
  }

  TH1D* Fitter::finalize_binning(TH1D* h) {
    std::vector<double> bins = binning();
    TH1D* hh = (TH1D*)h->Rebin(bins.size()-1, TString::Format("%s_rebinned", h->GetName()), &bins[0]);
    const int nb = hh->GetNbinsX();
    const double l  = hh->GetBinContent(nb);
    const double le = hh->GetBinError  (nb);
    const double o  = hh->GetBinContent(nb+1);
    const double oe = hh->GetBinError  (nb+1);
    hh->SetBinContent(nb, l + o);
    hh->SetBinError  (nb, sqrt(le*le + oe*oe));
    hh->SetBinContent(nb+1, 0);
    hh->SetBinError  (nb+1, 0);
    return hh;
  }

  TH1D* Fitter::finalize_template(TH1D* h) {
    TH1D* hh = finalize_binning(h);
    hh->Scale(1./hh->Integral());
    return hh;
  }

  void Fitter::fit_globals_ok() {
    if (fit::n_bins < 0 || fit::h_data == 0 || fit::curr_bkg_template == 0 || fit::h_sig == 0)
      jmt::vthrow("fit globals not set up properly: n_bins: %i  h_data: %p  curr_bkg_template: %p  h_sig: %p",
                  fit::n_bins, fit::h_data, fit::curr_bkg_template, fit::h_sig);
  }

#if 0
  bool Fitter::scan_likelihood() {
    fit_globals_ok();

    const double mu_sig_min = 0;
    const double mu_sig_max = 100;
    const double mu_bkg_min = 0;
    const double mu_bkg_max = 100;
    const int mu_sig_steps = 200;
    const int mu_bkg_steps = 200;
    const double d_mu_sig = (mu_sig_max - mu_sig_min) / mu_sig_steps;
    const double d_mu_bkg = (mu_bkg_max - mu_bkg_min) / mu_bkg_steps;

    printf("scanning likelihood mu_sig (%f, %f) in %i steps and mu_bkg (%f, %f) in %i steps, with %i templates:\n", mu_sig_min, mu_sig_max, mu_sig_steps, mu_bkg_min, mu_bkg_max, mu_bkg_steps, int(bkg_templates->size()));

    glb_scan_maxtwolnL = -1e300;
    glb_scan_max_pars.assign(5, -1);
    glb_scan_max_pars_errs.assign(5, -1);

    TDirectory* d = dtoy->mkdir("scan_likelihood");
    d->cd();

    for (size_t i_template = 0, i_template_e = bkg_templates->size(); i_template < i_template_e; ++i_template) {
      Template* bkg_template = bkg_templates->at(i_template);
      fit::curr_bkg_template = bkg_template;

      TH2F* h = new TH2F(TString::Format("h_likelihood_template%s", bkg_template->name().c_str()),
                         TString::Format("%s;#mu_{sig};#mu_{bkg}", bkg_template->title().c_str()),
                         mu_sig_steps, mu_sig_min, mu_sig_max,
                         mu_bkg_steps, mu_bkg_min, mu_bkg_max);

      double maxtwolnL = -1e300;
      std::vector<double> max_pars(npars);
      max_pars[0] = max_pars[1] = -1;
      for (int ipar = 2; ipar < npars; ++ipar)
        max_pars[ipar] = bkg_template->par(ipar-2);

      for (int i_mu_sig = 0; i_mu_sig < mu_sig_steps; ++i_mu_sig) {
        const double mu_sig = mu_sig_min + i_mu_sig * d_mu_sig;
        for (int i_mu_bkg = 0; i_mu_bkg < mu_bkg_steps; ++i_mu_bkg) {
          const double mu_bkg = mu_bkg_min + i_mu_bkg * d_mu_bkg;
          if (mu_sig < 1 || mu_bkg < 1)
            continue;

          const double twolnL_ = fit::twolnL(mu_sig, mu_bkg);
          h->SetBinContent(i_mu_sig+1, i_mu_bkg+1, twolnL_);

          if (twolnL_ > maxtwolnL) {
            maxtwolnL = twolnL_;
            max_pars[0] = mu_sig;
            max_pars[1] = mu_bkg;
          }
        }
      }

      printf("%s (%s) max 2lnL = %f  for  mu_sig = %f  mu_bkg = %f\n", h->GetName(), h->GetTitle(), maxtwolnL, max_pars[0], max_pars[1]);
      if (maxtwolnL > glb_scan_maxtwolnL) {
        printf("  ^ new global max!\n");
        glb_scan_maxtwolnL = maxtwolnL;
        for (int ipar = 0; ipar < npars; ++ipar)
          glb_scan_max_pars[ipar] = max_pars[ipar];
      }
    }

    return glb_scan_maxtwolnL > -1e300;
  }
#endif

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
        Template* bkg_template = fit::curr_bkg_template = bkg_templates->at(i_template);
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

      fit::curr_bkg_template = ml.nuis;

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

      TH1D* h_bkg_fit  = (TH1D*)ml.nuis->h_final->Clone(TString::Format("h_bkg_%s_fit",  sb_or_b));
      TH1D* h_sig_fit  = (TH1D*)fit::h_sig      ->Clone(TString::Format("h_sig_%s_fit",  sb_or_b));
      TH1D* h_data_fit = (TH1D*)fit::h_data     ->Clone(TString::Format("h_data_%s_fit", sb_or_b));

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
    fit_globals_ok();

    min_lik_t ret;

    //printf("scanminning (mu_sig_start = %f, fix? %i):\n", mu_sig_start, fix_mu_sig);

    //TDirectory* d = dtoy->mkdir(TString::Format("scanmin_likelihood_%s", bkg_only ? "b" : "sb"));
    //d->cd();

    for (size_t i_template = 0, i_template_e = bkg_templates->size(); i_template < i_template_e; ++i_template) {
      Template* bkg_template = bkg_templates->at(i_template);
      fit::curr_bkg_template = bkg_template;

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
    char s[128], s2[128];
    if (i_toy_signif < 0 && i_toy_limit < 0)
      snprintf(s, 128, "h_%%s_seed%02i_toy%02i", seed, toy);
    else if (i_toy_limit < 0)
      snprintf(s, 128, "h_%%s_seed%02i_toy%02i_signif%02i", seed, toy, i_toy_signif);
    else if (i_toy_signif < 0)
      snprintf(s, 128, "h_%%s_seed%02i_toy%02i_limit%02i", seed, toy, i_toy_limit);

    snprintf(s2, 128, s, "data_sig"); fit::h_data_sig = hist_with_binning(s2, "");
    snprintf(s2, 128, s, "data_bkg"); fit::h_data_bkg = hist_with_binning(s2, "");
    snprintf(s2, 128, s, "data");     fit::h_data     = hist_with_binning(s2, "");

    bool save = i_toy_signif < 0 && i_toy_limit < 0;
    for (TH1D* h : {fit::h_data_sig, fit::h_data_bkg, fit::h_data}) {
      h->SetLineWidth(2);
      if (!save)
        h->SetDirectory(0);
    }
  
    fit::h_data_sig->FillRandom(fit::h_sig, n_sig);
    fit::h_data_bkg->FillRandom(fit::curr_bkg_template->h_final, n_bkg);

    fit::h_data->Add(fit::h_data_sig);
    fit::h_data->Add(fit::h_data_bkg);
  }

  void Fitter::fit(int toy_, Templates* bkg_templates_, TH1D* sig_template, const VertexPairs& v2v, const std::vector<double>& true_pars_) {
    toy = toy_;
    true_pars = true_pars_;

    dtoy = dout->mkdir(TString::Format("seed%02i_toy%02i", seed, toy));

    ////

    dtoy->mkdir("finalized_templates")->cd();

    bkg_templates = bkg_templates_;
    for (Template* t : *bkg_templates)
      t->h_final = finalize_template(t->h);

    fit::curr_bkg_template = (*bkg_templates)[0];
    fit::h_sig = finalize_template(sig_template);

    fit::h_data_real = fit::h_data = hist_with_binning("h_data", TString::Format("toy %i", toy));
    for (const VertexPair& p : v2v)
      fit::h_data->Fill(p.d2d());
    const int n_data = fit::h_data->Integral();

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

    printf("throwing %i significance toys: ", n_toy_signif);

    int n_toys_per_dot = n_toy_signif / 50;
    int n_toy_signif_t_ge_obs = 0;
    for (int i_toy_signif = 0; i_toy_signif < n_toy_signif; ++i_toy_signif) {
      if (i_toy_signif % n_toys_per_dot == 0) {
        printf("."); fflush(stdout);
      }

      const int n_sig_signif = 0;
      const int n_bkg_signif = rand->Poisson(n_data);
      make_toy_data(i_toy_signif, -1, n_sig_signif, n_bkg_signif);
      
      const test_stat_t t = calc_test_stat(0);
      if (t.t >= t_obs_0.t)
        ++n_toy_signif_t_ge_obs;

      if (print_toys) {
        t.print("t_signif toy %i");
      }

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
      const int n_i_mu_per_dot = mu_sig_limit_stop / mu_sig_limit_step / 50;
      int i_mu_sig_limit = 0;

      printf("scanning for %.1f%% upper limit: ", 100*(1-limit_alpha));
      while (mu_sig_limit < mu_sig_limit_stop) {
        if (i_mu_sig_limit++ % n_i_mu_per_dot == 0) {
          printf("."); fflush(stdout);
        }

        fit::h_data = fit::h_data_real;
        const test_stat_t t_obs_limit_ = calc_test_stat(mu_sig_limit);

        if (print_toys) {
          printf("mu_sig_limit: %f  ", mu_sig_limit);
          t_obs_limit_.print("t_obs_limit");
        }

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
