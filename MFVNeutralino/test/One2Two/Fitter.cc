#include "Fitter.h"

#include <cassert>
#include <cmath>

#include "TCanvas.h"
#include "TFile.h"
#include "TFitResult.h"
#include "TGraphErrors.h"
#include "TH2.h"
#include "TMath.h"
#include "TMinuit.h"
#include "TRandom3.h"
#include "TTree.h"

#include "Prob.h"
#include "ProgressBar.h"
#include "ROOTTools.h"
#include "Random.h"
#include "Templater.h"

namespace mfv {
  namespace fit {
    int extra_prints = 0;

    int n_bins = -1;

    std::vector<double> a_bkg;
    TemplateInterpolator* interp;

    double n_sig_orig = -1;
    TH1D* h_sig = 0;
    const double* a_sig = 0;

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
      if (n_bins < 0 || h_data == 0 || h_sig == 0 || h_data_real == 0 || interp == 0)
        jmt::vthrow("fit globals not set up properly: n_bins: %i  h_data: %p  h_sig: %p  h_data_real: %p  interp: %p", n_bins, h_data, h_sig, h_data_real, interp);
    }

    double twolnL(double mu_sig, double mu_bkg, double par0, double par1) {
      if (TMath::IsNaN(mu_sig) || TMath::IsNaN(mu_bkg) || TMath::IsNaN(par0) || TMath::IsNaN(par1))
        jmt::vthrow("NaN in twolnL(%f, %f, %f, %f)", mu_sig, mu_bkg, par0, par1);

      interp->interpolate(par0, par1);
      for (int i = 1; i < n_bins; ++i)
        if (TMath::IsNaN(a_bkg[i]))
          jmt::vthrow("NaN in interpolation (%f, %f) in bin %i", par0, par1, i);

      if (mu_sig < 1e-12)
        mu_sig = 1e-12;

      if (extra_prints)
        printf("\n----\nmu_sig: %f  mu_bkg: %f\npar0: %f  par1: %f\n", mu_sig, mu_bkg, par0, par1);

      std::vector<double> A_sig(n_bins+2, 0.);
      std::vector<double> A_bkg(n_bins+2, 0.);

      //static const double eta_bkg[7] = { -1, 0.001, 0.001, 0.01, 0.35, 1.5, 1.5 };
      static const double eta_bkg[7] = { -1, 1e-9, 1e-9, 1e-9, 1e-9, 1e-9, 1e-9 };

      const double eps = 1e-7;
      const int maxit = 1000;

      for (int i = 1; i <= n_bins; ++i) {
        double t = 1;

        if (a_data[i] > eps) {
          double t_lo = -1./std::max(mu_sig, mu_bkg) + 1e-12;
          double t_hi = 1;
          bool found = false;

          if (extra_prints)
            printf("find t: bin %i  d: %5.1f  a_bkg: %10.6f  a_sig: %10.6f\n", i, a_data[i], a_bkg[i], a_sig[i]);

          for (int it = 0; it < maxit; ++it) {
            t = 0.5*(t_lo + t_hi);

            const double y = a_data[i] / (1 - t) - mu_bkg * a_bkg[i] / (1 + mu_bkg * t) - mu_sig * a_sig[i] / (1 + mu_sig * t);

            if (y > 0)
              t_hi = t;
            else if (y < 0)
              t_lo = t;

            if (extra_prints)
              printf("  #%3i:  t: %11.6e  y: %11.6f  new t: [%11.6e %11.6e]\n", it, t, y, t_lo, t_hi);

            if (fabs(y) < eps || t_hi - t_lo < eps) {
              found = true;
              break;
            }
          }

          if (!found)
            jmt::vthrow("zero finding failed");
        }
        else if (extra_prints)
          printf("find t: bin %i  d: 0 -> t = 1\n", i);

        A_sig[i] = a_sig[i] / (t * mu_sig / n_sig_orig + 1);
        A_bkg[i] = a_bkg[i] - t * mu_bkg * a_bkg[i] * a_bkg[i] * eta_bkg[i] * eta_bkg[i];
      }

      if (extra_prints) {
        printf("   %10s %10s %10s %10s %10s %10s\n", "a_bkg", "A_bkg", "dlt_bkg", "a_sig", "A_sig", "dlt_sig");
        for (int i = 1; i <= n_bins; ++i)
          printf("%2i %10f %10f %10f %10f %10f %10f\n", i, a_bkg[i], A_bkg[i], A_bkg[i] - a_bkg[i], a_sig[i], A_sig[i], A_sig[i] - a_sig[i]);
      }

      double lnL = 0;

      for (int i = 1; i <= n_bins; ++i) {
        const double dlnL_bb_bkg = -0.5 * pow((a_bkg[i] - A_bkg[i])/a_bkg[i]/eta_bkg[i], 2);
        const double dlnL_bb_sig = n_sig_orig * a_sig[i] * log(n_sig_orig * A_sig[i]) - n_sig_orig * A_sig[i]; 

        const double nu_sig = mu_sig * A_sig[i];
        const double nu_bkg = mu_bkg * A_bkg[i];
        const double nu_sum = nu_sig + nu_bkg;
        const double dlnL = -nu_sum + a_data[i] * log(nu_sum);

        lnL += dlnL + dlnL_bb_bkg + dlnL_bb_sig;

        if (extra_prints)
          printf("i: %2i  nu_bkg: %7.3f  nu_sig: %7.3f  nu: %7.3f  n: %6.1f    dlnL: %10.6f + %10.6f + %10.6f  lnL: %10.6f\n", i, nu_bkg, nu_sig, nu_sum, a_data[i], dlnL, dlnL_bb_bkg, dlnL_bb_sig, lnL);
      }

      return 2*lnL;
    }

    void minfcn(int&, double*, double& f, double* par, int) {
      f = -twolnL(par[0], par[1], par[2], par[3]);
    }
  }

  //////////////////////////////////////////////////////////////////////////////

  std::string Fitter::min_lik_t::nuis_title() const {
    char buf[128];
    snprintf(buf, 128, "nuis 0:  %f #pm %f  nuis1: %f #pm %f", nuis0, err_nuis0, nuis1, err_nuis1);
    return std::string(buf);
  }

  std::string Fitter::min_lik_t::mu_title() const {
    char buf[256];
    snprintf(buf, 128, "#mu_{sig} = %f #pm %f, #mu_{bkg} = %f #pm %f", mu_sig, err_mu_sig, mu_bkg, err_mu_bkg);
    return std::string(buf);
  }

  std::string Fitter::min_lik_t::title() const {
    return mu_title() + "  " + nuis_title();
  }


  void Fitter::min_lik_t::print(const char* header, const char* indent) const {
    printf("%s%s  istat = %i  maxtwolnL = %10.4e  mu_sig = %7.3f +- %7.3f  mu_bkg = %7.3f +- %7.3f", indent, header, istat, maxtwolnL, mu_sig, err_mu_sig, mu_bkg, err_mu_bkg);
    printf("  nuis0 = %7.3f +- %7.3f  nuis1 = %7.3f +- %7.3f\n", nuis0, err_nuis0, nuis1, err_nuis1);
  }

  void Fitter::test_stat_t::print(const char* header, const char* indent) const {
    printf("%s:  ok? %i  t = %f\n", header, ok(), t);
    h1.print("h1", indent);
    h0.print("h0", indent);
  }

  //////////////////////////////////////////////////////////////////////////////

  Fitter::Fitter(const std::string& name_, TFile* f, TRandom* r)
    : name (name_.size() ? " " + name_ : ""),
      uname(name_.size() ? "_" + name_ : ""),

      env("mfvo2t_fitter" + uname),
      print_level(env.get_int("print_level", -1)),
      allow_negative_mu_sig(env.get_bool("allow_negative_mu_sig", false)),
      run_minos(env.get_bool("run_minos", true)),
      draw_bkg_templates(env.get_bool("draw_bkg_templates", 0)),
      fix_nuis1(env.get_bool("fix_nuis1", 0)),
      start_nuis0(env.get_double("start_nuis0", 0.025)),
      start_nuis1(env.get_double("start_nuis1", 0.008)),
      n_toy_signif(env.get_int("n_toy_signif", 100000)),
      print_toys(env.get_bool("print_toys", false)),
      save_toys(env.get_bool("save_toys", false)),
      do_signif(env.get_bool("do_signif", true)),
      do_limits(env.get_bool("do_limits", true)),
      only_fit(env.get_bool("only_fit", false)),
      n_toy_limit(env.get_int("n_toy_limit", 20000)),
      sig_limit_step(env.get_double("sig_limit_step", 0.1)),
      sig_eff(env.get_double("sig_eff", 1.)),
      sig_eff_uncert(env.get_double("sig_eff_uncert", 0.)),

      fout(f),
      dout(f->mkdir(TString::Format("Fitter%s", uname.c_str()))),
      dtoy(0),
      rand(r),
      seed(r->GetSeed() - jmt::seed_base)
  {
    printf("Fitter%s config:\n", name.c_str());
    printf("print_level: %i\n", print_level);
    printf("draw_bkg_templates: %i\n", draw_bkg_templates);
    printf("fix_nuis1: %i\n", fix_nuis1);
    printf("start_nuis: %f, %f\n", start_nuis0, start_nuis1);
    printf("n_toy_signif: %i\n", n_toy_signif);
    printf("print_toys? %i\n", print_toys);
    printf("save_toys? %i\n", save_toys);
    printf("do_signif? %i\n", do_signif);
    printf("do_limits? %i\n", do_limits);
    printf("only_fit? %i\n", only_fit);
    printf("n_toy_limit: %i (~%f uncert @ 0.05)\n", n_toy_limit, sqrt(0.05*0.95/n_toy_limit));
    printf("sig_limit_step: %f\n", sig_limit_step);
    printf("sig_eff: %f +- %f\n", sig_eff, sig_eff_uncert);

    fflush(stdout);

    book_trees();
  }

  void Fitter::book_trees() {
    dout->cd();

    TTree* t_config = new TTree("t_config", "");
    t_config->Branch("seed", const_cast<int*>(&seed), "seed/I");
    t_config->Branch("allow_negative_mu_sig", const_cast<bool*>(&allow_negative_mu_sig));
    t_config->Branch("run_minos", const_cast<bool*>(&run_minos));
    t_config->Branch("fix_nuis1", const_cast<bool*>(&fix_nuis1));
    t_config->Branch("start_nuis0", const_cast<double*>(&start_nuis0));
    t_config->Branch("start_nuis1", const_cast<double*>(&start_nuis1));
    t_config->Branch("n_toy_signif", const_cast<int*>(&n_toy_signif));
    t_config->Branch("n_toy_limit", const_cast<int*>(&n_toy_limit));
    t_config->Branch("sig_limit_step", const_cast<double*>(&sig_limit_step));
    t_config->Branch("sig_eff", const_cast<double*>(&sig_eff));
    t_config->Branch("sig_eff_uncert", const_cast<double*>(&sig_eff_uncert));
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
    t_fit_info->Branch("t_obs_0__h1_nuis0", &t_obs_0.h1.nuis0, "t_obs_0__h1_nuis0/D");
    t_fit_info->Branch("t_obs_0__h1_err_nuis0", &t_obs_0.h1.err_nuis0, "t_obs_0__h1_err_nuis0/D");
    t_fit_info->Branch("t_obs_0__h1_nuis1", &t_obs_0.h1.nuis1, "t_obs_0__h1_nuis1/D");
    t_fit_info->Branch("t_obs_0__h1_err_nuis1", &t_obs_0.h1.err_nuis1, "t_obs_0__h1_err_nuis1/D");
    t_fit_info->Branch("t_obs_0__h0_istat", &t_obs_0.h0.istat, "t_obs_0__h0_istat/I");
    t_fit_info->Branch("t_obs_0__h0_maxtwolnL", &t_obs_0.h0.maxtwolnL, "t_obs_0__h0_maxtwolnL/D");
    t_fit_info->Branch("t_obs_0__h0_mu_sig", &t_obs_0.h0.mu_sig, "t_obs_0__h0_mu_sig/D");
    t_fit_info->Branch("t_obs_0__h0_err_mu_sig", &t_obs_0.h0.err_mu_sig, "t_obs_0__h0_err_mu_sig/D");
    t_fit_info->Branch("t_obs_0__h0_mu_bkg", &t_obs_0.h0.mu_bkg, "t_obs_0__h0_mu_bkg/D");
    t_fit_info->Branch("t_obs_0__h0_err_mu_bkg", &t_obs_0.h0.err_mu_bkg, "t_obs_0__h0_err_mu_bkg/D");
    t_fit_info->Branch("t_obs_0__h0_nuis0", &t_obs_0.h0.nuis0, "t_obs_0__h0_nuis0/D");
    t_fit_info->Branch("t_obs_0__h0_err_nuis0", &t_obs_0.h0.err_nuis0, "t_obs_0__h0_err_nuis0/D");
    t_fit_info->Branch("t_obs_0__h0_nuis1", &t_obs_0.h0.nuis1, "t_obs_0__h0_nuis1/D");
    t_fit_info->Branch("t_obs_0__h0_err_nuis1", &t_obs_0.h0.err_nuis1, "t_obs_0__h0_err_nuis1/D");
    t_fit_info->Branch("t_obs_0__t", &t_obs_0.t, "t_obs_0__t/D");
    t_fit_info->Branch("fs_chi2", &fit_stat.chi2);
    t_fit_info->Branch("fs_ndof", &fit_stat.ndof);
    t_fit_info->Branch("fs_prob", &fit_stat.prob);
    t_fit_info->Branch("fs_ks", &fit_stat.ks);
    t_fit_info->Branch("pval_signif", &pval_signif);
    t_fit_info->Branch("sig_limit", &sig_limit);
    t_fit_info->Branch("sig_limit_err", &sig_limit_err);
    t_fit_info->Branch("sig_limit_fit_n", &sig_limit_fit_n);
    t_fit_info->Branch("sig_limit_fit_a", &sig_limit_fit_a);
    t_fit_info->Branch("sig_limit_fit_b", &sig_limit_fit_b);
    t_fit_info->Branch("sig_limit_fit_a_err", &sig_limit_fit_a_err);
    t_fit_info->Branch("sig_limit_fit_b_err", &sig_limit_fit_b_err);
    t_fit_info->Branch("sig_limit_fit_prob", &sig_limit_fit_prob);

    t_fit_info->SetAlias("s_true", "true_pars[0]");
    t_fit_info->SetAlias("b_true", "true_pars[1]");
  }    

  void Fitter::draw_likelihood(const test_stat_t& t) {
    printf("draw_likelihood: ");

    struct scan_t {
      int n;
      double min;
      double max;
      double d() const { return (max - min)/n; }
      double v(int i) const { return min + d() * i; }
    };

    scan_t mu_scan[2] = {
      { 200, 0, 200 },
      { 400, 0, 400 }
    };

    const size_t npars = bkg_templates->at(0)->npars();
    std::vector<double> mins(npars,  1e99);
    std::vector<double> maxs(npars, -1e99);
    for (Template* tp : *bkg_templates)
      for (size_t ipar = 0; ipar < npars; ++ipar) {
        double t_par = tp->par(ipar);
        if (t_par > maxs[ipar])
          maxs[ipar] = t_par;
        if (t_par < mins[ipar])
          mins[ipar] = t_par;
      }
    int n_nuis[2] = {200, 200};
    if (maxs[1] <= mins[1]) {
      maxs[1] = mins[1] + 1;
      n_nuis[1] = 3;
    }

    scan_t nuis_scan[2] = {
      { n_nuis[0], mins[0], maxs[0] },
      { n_nuis[1], mins[1], maxs[1] }
    };

    TDirectory* cwd = gDirectory;

    for (int sb = 1; sb >= 0; --sb) {
      const char* sb_or_b = sb ? "sb" : "b";
      printf("%s: ", sb_or_b); fflush(stdout);
      const char* sb_or_b_nice = sb ? "sig + bkg" : "b only";
      const min_lik_t& ml = sb ? t.h1 : t.h0;

      TDirectory* subdir = 0;
      if (draw_bkg_templates)
        subdir = cwd->mkdir(TString::Format("bkg_template_scan_nuis_%s", sb_or_b));

      jmt::ProgressBar pb(50, nuis_scan[0].n * nuis_scan[1].n + mu_scan[0].n * mu_scan[1].n);
      pb.start();


      if (draw_bkg_templates)
        cwd->cd();

      TH2F* h1 = new TH2F(TString::Format("h_likelihood_%s_scannuis", sb_or_b),
                          TString::Format("Best %s fit: %s;nuis. par 0;nuis. par 1", sb_or_b_nice, ml.title().c_str()),
                          nuis_scan[0].n, nuis_scan[0].min, nuis_scan[0].max,
                          nuis_scan[1].n, nuis_scan[1].min, nuis_scan[1].max
                          );

      for (int i0 = 1; i0 < nuis_scan[0].n; ++i0) {
        const double nuispar0 = nuis_scan[0].v(i0);

        if (draw_bkg_templates)
          subdir->mkdir(TString::Format("nuis0_%03i", i0))->cd();

        for (int i1 = 1; i1 < nuis_scan[1].n; ++i1, ++pb) {
          //fit::extra_prints = i0 == 186 && i1 == 1;
          //fit::interp->extra_prints = i0 == 186 && i1 == 1;

          const double nuispar1 = nuis_scan[1].v(i1);
          const double twolnL = fit::twolnL(ml.mu_sig, ml.mu_bkg, nuispar0, nuispar1);

          if (draw_bkg_templates)
            make_h_bkg(TString::Format("h_bkg_template_scan_%s_nuis0_%03i_nuis1_%03i", sb_or_b, i0, i1), std::vector<double>({nuispar0, nuispar1}));

          //printf("i0: %i %f  i1: %i %f  %f\n", i0, nuispar0, i1, nuispar1, twolnL);
          h1->SetBinContent(i0, i1, twolnL);
        }
      }

      if (draw_bkg_templates)
        cwd->cd();

      TH2F* h2 = new TH2F(TString::Format("h_likelihood_%s_scanmus", sb_or_b),
                          TString::Format("Best %s fit: %s;#mu_{sig};#mu_{bkg}", sb_or_b_nice, ml.title().c_str()),
                          mu_scan[0].n, mu_scan[0].min, mu_scan[0].max,
                          mu_scan[1].n, mu_scan[1].min, mu_scan[1].max
                          );

      for (int i0 = 1; i0 < mu_scan[0].n; ++i0) {
        const double mu_sig = mu_scan[0].v(i0);
        for (int i1 = 1; i1 < mu_scan[1].n; ++i1, ++pb) {
          const double mu_bkg = mu_scan[1].v(i1);
          h2->SetBinContent(i0, i1, fit::twolnL(mu_sig, mu_bkg, ml.nuis0, ml.nuis1));
        }
      }

      printf("\n");
    }
  }

  TH1D* Fitter::make_h_bkg(const char* n, const std::vector<double>& nuis_pars) {
    std::vector<double> a(fit::n_bins+2, 0.);
    TH1D* h = (TH1D*)fit::interp->get_Q(nuis_pars)->h->Clone(n);
    fit::interp->interpolate(nuis_pars, &a);
    for (int ibin = 0; ibin <= fit::n_bins+1; ++ibin)
      h->SetBinContent(ibin, a[ibin]);
    return h;
  }

  Fitter::fit_stat_t Fitter::draw_fit(const test_stat_t& t) {
    fit_stat_t ret;

    for (int div = 0; div <= 1; ++div) {
      for (int sb = 1; sb >= 0; --sb) {
        const char* div_or_no = div ? "div" : "nodiv";
        const char* div_or_no_nice = div ? "/bin width" : "";
        const char* sb_or_b = sb ? "sb" : "b";
        const char* sb_or_b_nice = sb ? "sig + bkg" : "b only";
        const min_lik_t& ml = sb ? t.h1 : t.h0;
        TCanvas* c = new TCanvas(TString::Format("c_%s_fit_%s", sb_or_b, div_or_no));

        TH1D* h_bkg_fit = make_h_bkg(TString::Format("h_bkg_%s_fit_%s",  sb_or_b, div_or_no), ml.nuis_pars());
        TH1D* h_sig_fit  = (TH1D*)fit::h_sig ->Clone(TString::Format("h_sig_%s_fit_%s",  sb_or_b, div_or_no));
        TH1D* h_data_fit = (TH1D*)fit::h_data->Clone(TString::Format("h_data_%s_fit_%s", sb_or_b, div_or_no));

        for (TH1D** ph : {&h_bkg_fit, &h_sig_fit, &h_data_fit}) {
          TH1D* h = *ph;
          std::vector<double> bins = Template::binning(true);
          TH1D* h_short = (TH1D*)h->Rebin(bins.size()-1, TString::Format("%s_shortened", h->GetName()), &bins[0]);
          // Splitting the last bin puts its contents in the overflow -- move back into last bin.
          int n = h_short->GetNbinsX();
          double v = h_short->GetBinContent(n+1);
          double e = h_short->GetBinError(n+1);
          h_short->SetBinContent(n+1, 0);
          h_short->SetBinError  (n+1, 0);
          h_short->SetBinContent(n, v);
          h_short->SetBinError  (n, e);
          *ph = h_short;
        }

        for (TH1D* h : {h_bkg_fit, h_sig_fit, h_data_fit}) {
          h->SetLineWidth(2);
          if (div)
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

        TH1D* h_sum_fit = (TH1D*)h_sig_fit->Clone(TString::Format("h_sum_%s_fit_%s", sb_or_b, div_or_no));
        h_sum_fit->SetLineColor(kMagenta);
        h_sum_fit->Add(h_bkg_fit);
        for (TH1D* h : {h_sum_fit, h_data_fit})
          h->SetTitle(TString::Format("best %s fit: %s;svdist2d (cm);events%s", sb_or_b_nice, ml.title().c_str(), div_or_no_nice));

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

        if (!div) {
          TH1D* h_sum_cumul = (TH1D*)h_sum_fit->Clone(TString::Format("h_sum_%s_cumul_%s", sb_or_b, div_or_no));
          TH1D* h_data_cumul = (TH1D*)h_data_fit->Clone(TString::Format("h_data_%s_cumul_%s", sb_or_b, div_or_no));
          h_sum_cumul->Scale(1/h_sum_cumul->Integral());
          h_data_cumul->Scale(1/h_data_cumul->Integral());

          for (TH1D* h : {h_sum_cumul, h_data_cumul})
            jmt::cumulate(h, false);

          TCanvas* c2 = new TCanvas(TString::Format("c_%s_cumul_%s", sb_or_b, div_or_no));
          h_sum_cumul->Draw();
          h_data_cumul->Draw("same e");
          c2->Write();
          delete c2;

          ret.chi2 = 0;
          ret.ndof = h_data_fit->GetNbinsX() - 2;
          ret.ks = 0;
          for (int ibin = 1; ibin <= h_data_fit->GetNbinsX(); ++ibin) {
            if (h_sum_fit->GetBinContent(ibin) > 0)
              ret.chi2 += pow(h_data_fit->GetBinContent(ibin) - h_sum_fit->GetBinContent(ibin), 2) / h_sum_fit->GetBinContent(ibin);

            double ksd = fabs(h_sum_cumul->GetBinContent(ibin) - h_data_cumul->GetBinContent(ibin));
            if (ksd > ret.ks)
              ret.ks = ksd;
          }
          ret.prob = TMath::Prob(ret.chi2, ret.ndof);
        }
      }
    }

    return ret;
  }

  Fitter::min_lik_t Fitter::min_likelihood(double mu_sig_start, bool fix_mu_sig) {
    fit::globals_ok();

    min_lik_t ret;

    TMinuit* m = new TMinuit(4);
    m->SetPrintLevel(print_level);
    m->SetFCN(fit::minfcn);
    int ierr;
    m->mnparm(0, "mu_sig", (mu_sig_start > 0 ? mu_sig_start : 0), 0.1, 0, (mu_sig_start > 0 ? mu_sig_start : (allow_negative_mu_sig ? 0 : 5000)), ierr);
    m->mnparm(1, "mu_bkg", 50, 0.1, 0, 5000, ierr);

    const size_t npars = bkg_templates->at(0)->npars();
    std::vector<double> mins(npars,  1e99);
    std::vector<double> maxs(npars, -1e99);
    for (Template* t : *bkg_templates)
      for (size_t ipar = 0; ipar < npars; ++ipar) {
        double t_par = t->par(ipar);
        if (t_par > maxs[ipar])
          maxs[ipar] = t_par;
        if (t_par < mins[ipar])
          mins[ipar] = t_par;
      }

    static const char* nuis_par_names[2] = { "nuis0", "nuis1" };
    for (size_t ipar = 0; ipar < npars; ++ipar) {
      const double start = ipar == 0 ? start_nuis0 : start_nuis1;
      m->mnparm(2+ipar, nuis_par_names[ipar], start, start/100., mins[ipar], maxs[ipar], ierr);
    }

    if (fix_mu_sig)
      m->FixParameter(0);

    if (fix_nuis1)
      m->FixParameter(3);

    m->Migrad();
    //    m->mnsimp();
    //    m->Migrad();
    //    m->mnimpr();
    m->Migrad();
    if (run_minos)
      m->mnmnos();
    double fmin, fedm, errdef;
    int npari, nparx, istat;
    m->mnstat(fmin, fedm, errdef, npari, nparx, istat);

    ret.maxtwolnL = -fmin;
    m->GetParameter(0, ret.mu_sig, ret.err_mu_sig);
    m->GetParameter(1, ret.mu_bkg, ret.err_mu_bkg);
    m->GetParameter(2, ret.nuis0, ret.err_nuis0);
    m->GetParameter(3, ret.nuis1, ret.err_nuis1);
    ret.ok = istat == 3;
    ret.istat = istat;

    //printf("min_likelihood: %s  istat: %i   maxtwolnL: %e   mu_sig: %f +- %f  mu_bkg: %f +- %f\n", bkg_template->title().c_str(), istat, maxtwolnL, mu_sig, err_mu_sig, mu_bkg, err_mu_bkg);
    delete m;
    return ret;
  }

  Fitter::test_stat_t Fitter::calc_test_stat(double fix_mu_sig_val) {
    test_stat_t t;
    if (print_level > 0)
      printf("calc_test_stat: H1\n");
    t.h1 = min_likelihood(fix_mu_sig_val, false);
    if (print_level > 0)
      printf("calc_test_stat: H0 (mu_sig fixed to %f)\n", fix_mu_sig_val);
    t.h0 = min_likelihood(fix_mu_sig_val, true);
    t.t = t.h1.maxtwolnL - t.h0.maxtwolnL;
    return t;
  }

  void Fitter::make_toy_data(int i_toy_signif, int i_toy_limit, int n_sig, int n_bkg, TH1D* h_bkg) {
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
    fit::h_data_toy_bkg->FillRandom(h_bkg, n_bkg);

    fit::h_data_toy->Add(fit::h_data_toy_sig);
    fit::h_data_toy->Add(fit::h_data_toy_bkg);
    fit::set_data_no_check(fit::h_data_toy);

    if (print_level > 1) {
      printf("make_toy_data: i_signif: %i i_limit: %i n_sig: %i n_bkg: %i\n", i_toy_signif, i_toy_limit, n_sig, n_bkg);
      printf("toy_sig: ");
      for (int i = 0; i <= fit::n_bins+1; ++i)
        printf("%10.6f ", fit::h_data_toy_sig->GetBinContent(i));
      printf("\ntoy_bkg: ");
      for (int i = 0; i <= fit::n_bins+1; ++i)
        printf("%10.6f ", fit::h_data_toy_bkg->GetBinContent(i));
      printf("\ntoy: ");
      for (int i = 0; i <= fit::n_bins+1; ++i)
        printf("%10.6f ", fit::h_data_toy->GetBinContent(i));
      printf("\n");
    }
  }

  void Fitter::fit(int toy_, Templater* bkg_templater, TH1D* sig_template, const VertexPairs& v2v, const std::vector<double>& true_pars_) {
    toy = toy_;
    true_pars = true_pars_;

    dtoy = dout->mkdir(TString::Format("seed%02i_toy%02i", seed, toy));

    ////

    dtoy->mkdir("finalized_templates")->cd();

    if (!fit::extra_prints && print_level > 1)
      fit::extra_prints = 1;

    fit::n_sig_orig = sig_template->Integral(1,100000);
    fit::set_sig(Template::finalize_template(sig_template));

    bkg_templates = bkg_templater->get_templates();
    fit::interp = new TemplateInterpolator(bkg_templates, fit::n_bins, bkg_templater->par_info(), fit::a_bkg);

    std::map<int, int> template_index_deltas;
    bool any_nan = false;
    for (int i = 0, ie = bkg_templates->size(); i < ie; ++i) {
      //printf("bkg template #%5i: %s\n", i, bkg_templates->at(i)->title().c_str());
      const TH1D* ht = bkg_templates->at(i)->h;
      for (int ibin = 0; ibin <= ht->GetNbinsX()+1; ++ibin)
        if (TMath::IsNaN(ht->GetBinContent(ibin)) || TMath::IsNaN(ht->GetBinError(ibin))) {
          printf("NaN in template %i (%s) bin %i\n", i, bkg_templates->at(i)->title().c_str(), ibin);
          any_nan = true;
        }
      const int delta = abs(i - fit::interp->i_Q(bkg_templates->at(i)->pars));
      template_index_deltas[delta] += 1;
    }
    if (any_nan)
      jmt::vthrow("something wrong with templates");

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
    printf("  # bkg templates: %lu  template_index_deltas seen:\n", bkg_templates->size());
    for (const auto& p : template_index_deltas)
      printf("%i: %i times\n", p.first, p.second);

    t_obs_0 = calc_test_stat(0);
    t_obs_0.print("t_obs_0");
    TH1D* h_bkg_obs_0 = make_h_bkg("h_bkg_obs_0", t_obs_0.h0.nuis_pars());

    pval_signif = 1;

    draw_likelihood(t_obs_0);
    fit_stat = draw_fit(t_obs_0);

    if (!only_fit && do_signif) {
      printf("throwing %i significance toys:\n", n_toy_signif);
      jmt::ProgressBar pb_signif(50, n_toy_signif);
      if (!print_toys)
        pb_signif.start();

      int n_toy_signif_t_ge_obs = 0;

      for (int i_toy_signif = 0; i_toy_signif < n_toy_signif; ++i_toy_signif) {
        const int n_sig_signif = 0;
        const int n_bkg_signif = rand->Poisson(n_data);
        make_toy_data(i_toy_signif, -1, n_sig_signif, n_bkg_signif, h_bkg_obs_0);
      
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
    }

    if (!only_fit && do_limits) {
      const double limit_alpha = 0.05;

      const double sig_limit_lo = std::max(0., t_obs_0.h1.mu_sig / sig_eff); // units of fb
      const double sig_limit_hi = 1000;
      const int n_sigma_away = 5;

      printf("scanning for %.1f%% upper limit:\n", 100*(1-limit_alpha));
      jmt::ProgressBar pb_limit(50, (sig_limit_hi - sig_limit_lo)/sig_limit_step);
      if (!print_toys)
        pb_limit.start();

      sig_limit = sig_limit_lo;

      std::vector<double> bracket_sig_limit;
      std::vector<double> bracket_pval_limit;
      std::vector<double> bracket_pval_limit_err;

      while (sig_limit < sig_limit_hi) {
        const double mu_sig_limit = sig_eff * sig_limit;

        fit::set_data_real();
        const test_stat_t t_obs_limit_ = calc_test_stat(mu_sig_limit);

        if (print_toys) {
          printf("sig_limit: %f  mu_sig_limit: %f ", sig_limit, mu_sig_limit);
          t_obs_limit_.print("t_obs_limit");
        }
        else
          ++pb_limit;

        if (save_toys) {
          jmt::vthrow("save limit toys not implemented");
        }

        int n_toy_limit_t_ge_obs = 0;

        jmt::ProgressBar pb_limit_toys(50, n_toy_limit);
        if (print_toys)
          pb_limit_toys.start();

        for (int i_toy_limit = 0; i_toy_limit < n_toy_limit; ++i_toy_limit) {
          const double mu_sig_limit_toy = mu_sig_limit * (sig_eff_uncert > 0 ? jmt::lognormal(rand, 0, sig_eff_uncert) : 1);
          if (mu_sig_limit_toy >= n_data) {
            --i_toy_limit;
            continue;
          }
          const int n_sig_limit = rand->Poisson(mu_sig_limit_toy);
          const int n_bkg_limit = rand->Poisson(n_data - mu_sig_limit_toy);

          make_toy_data(-1, i_toy_limit, n_sig_limit, n_bkg_limit, h_bkg_obs_0);
      
          const test_stat_t t = calc_test_stat(mu_sig_limit);
          if (t.t > t_obs_limit_.t)
            ++n_toy_limit_t_ge_obs;

          if (print_toys) {
            //printf("limit toy %i nsig %i nbkg %i n'data' %i\n", i_toy_limit, n_sig_limit, n_bkg_limit, n_data);
            //t.print("t_limit");
            ++pb_limit_toys;
          }

          if (save_toys) {
            jmt::vthrow("save toys for limits not implemented");
          }
        }
        if (print_toys)
          printf("\n");

        const double T = 1./n_toy_limit;
        const double p_hat = double(n_toy_limit_t_ge_obs) / n_toy_limit;
        const double pval_limit = (p_hat + T/2)/(1 + T);
        const double pval_limit_err = sqrt(p_hat * (1 - p_hat) * T + T*T/4)/(1 + T);
        const double pval_limit_sglo = pval_limit - n_sigma_away * pval_limit_err;
        const double pval_limit_sghi = pval_limit + n_sigma_away * pval_limit_err;

        if (print_toys) {
          printf("  p_hat = %f -> %f +- %f  %is: [%f, %f]\n", p_hat, pval_limit, pval_limit_err, n_sigma_away, pval_limit_sglo, pval_limit_sghi);
          fflush(stdout);
        }

        if (pval_limit_sglo <= limit_alpha) {
          if (print_toys)
            printf("  ** include in bracket\n");
          bracket_sig_limit.push_back(sig_limit);
          bracket_pval_limit.push_back(pval_limit);
          bracket_pval_limit_err.push_back(pval_limit_err);
        }

        if (pval_limit_sghi <= limit_alpha)
          break;

        sig_limit += sig_limit_step;
      }

      std::vector<double> bracket_sig_limit_err(bracket_pval_limit.size(), 0.);
      TGraphErrors* g = new TGraphErrors(bracket_sig_limit.size(), &bracket_sig_limit[0], &bracket_pval_limit[0], &bracket_sig_limit_err[0], &bracket_pval_limit_err[0]);
      g->SetMarkerStyle(5);
      TFitResultPtr res = g->Fit("pol1", "S");
      const double a = sig_limit_fit_a = res->Parameter(0);
      const double b = sig_limit_fit_b = res->Parameter(1);
      const double ea = sig_limit_fit_a_err = res->ParError(0);
      const double eb = sig_limit_fit_b_err = res->ParError(1);
      sig_limit = (limit_alpha - a)/b;
      sig_limit_err = sig_limit * sqrt(pow(ea/a, 2) + pow(eb/b, 2));
      sig_limit_fit_n = bracket_sig_limit.size();
      sig_limit_fit_prob = res->Prob();
      g->SetName("g_limit_bracket_fit");
      g->Write();

      // need to set pval_limit, sig_limit, t_obs_limit, or whatever in tree.

      printf("  *** done bracketing (%lu points), y = %.2f at %f +- %f (prob: %f)\n", bracket_sig_limit.size(), limit_alpha, sig_limit, sig_limit_err, sig_limit_fit_prob);
    }

    t_fit_info->Fill();

    delete fit::interp;
  }
}
