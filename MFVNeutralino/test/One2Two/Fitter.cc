#include "Fitter.h"

#include <cassert>
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
#include "Templater.h"

namespace mfv {
  namespace fit {
    int n_bins = -1;

    std::vector<double> a_bkg;
    TemplateInterpolator* interp;

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
      interp->interpolate(par0, par1);

      double lnL = 0;
      for (int i = 1; i <= n_bins; ++i) {
        const double nu_sum = mu_sig * a_sig[i] + mu_bkg * a_bkg[i];
        if (nu_sum > 1e-12)
          lnL += -nu_sum + a_data[i] * log(nu_sum);
        else
          lnL -= 1e-12 + a_data[i] * 27.6310211159285473;
        //printf("i: %i   mu_sig, mu_bkg (%f, %f)   nu_bkg: %f  nu_sig: %f  nu: %f  n: %f    dlnL: %f   lnL: %f\n",
        //       i, mu_sig, mu_bkg, mu_bkg * a_bkg[i], mu_sig * a_sig[i], mu_bkg * a_bkg[i] + mu_sig * a_sig[i], a_data[i], -nu_sum + a_data[i] * (nu_sum > 1e-12 ? log(nu_sum) : -27.6310211159285473), lnL);
      }
      return 2*lnL;
    }

    void minfcn(int&, double*, double& f, double* par, int) {
      f = -twolnL(par[0], par[1], par[2], par[3]);
    }
  }

  //////////////////////////////////////////////////////////////////////////////

  std::string Fitter::min_lik_t::nuis_title() const {
    std::string s = "nuis. pars:";
    char buf[128];
    for (size_t i = 0, ie = nuis_pars.size(); i < ie; ++i) {
      snprintf(buf, 128, "  %f #pm %f", nuis_pars[i], nuis_par_errs[i]);
      s += buf;
    }
    return s;
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
    for (size_t ipar = 0; ipar < nuis_pars.size(); ++ipar)
      printf("  nuis%lu = %7.3f +- %7.3f", ipar, nuis_pars[ipar], nuis_par_errs[ipar]);
    printf("\n");
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

    struct scan_t {
      int n;
      double min;
      double max;
      double d() const { return (max - min)/n; }
      double v(int i) const { return min + d() * i; }
    };

    scan_t mu_scan[2] = {
      { 200, 0, 200 },
      { 200, 0, 200 }
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

    scan_t nuis_scan[2] = {
      { 200, mins[0], maxs[0] },
      { 200, mins[1], maxs[1] }
    };

    for (int sb = 1; sb >= 0; --sb) {
      const char* sb_or_b = sb ? "sb" : "b";
      printf("%s ", sb_or_b); fflush(stdout);
      const char* sb_or_b_nice = sb ? "sig + bkg" : "b only";
      const min_lik_t& ml = sb ? t.h1 : t.h0;

      TH2F* h1 = new TH2F(TString::Format("h_likelihood_%s_scannuis", sb_or_b),
                          TString::Format("Best %s fit: %s;nuis. par 0;nuis. par 1", sb_or_b_nice, ml.title().c_str()),
                          nuis_scan[0].n, nuis_scan[0].min, nuis_scan[0].max,
                          nuis_scan[1].n, nuis_scan[1].min, nuis_scan[1].max
                          );

      for (int i0 = 1; i0 < nuis_scan[0].n; ++i0) {
        const double nuispar0 = nuis_scan[0].v(i0);
        for (int i1 = 1; i1 < nuis_scan[1].n; ++i1) {
          const double nuispar1 = nuis_scan[1].v(i1);
          h1->SetBinContent(i0, i1, fit::twolnL(ml.mu_sig, ml.mu_bkg, nuispar0, nuispar1));
        }
      }

      TH2F* h2 = new TH2F(TString::Format("h_likelihood_%s_scanmus", sb_or_b),
                          TString::Format("Best %s fit: %s;#mu_{sig};#mu_{bkg}", sb_or_b_nice, ml.title().c_str()),
                          mu_scan[0].n, mu_scan[0].min, mu_scan[0].max,
                          mu_scan[1].n, mu_scan[1].min, mu_scan[1].max
                          );

      for (int i0 = 1; i0 < mu_scan[0].n; ++i0) {
        const double mu_sig = mu_scan[0].v(i0);
        for (int i1 = 1; i1 < mu_scan[1].n; ++i1) {
          const double mu_bkg = mu_scan[1].v(i1);
          h2->SetBinContent(i0, i1, fit::twolnL(mu_sig, mu_bkg, ml.nuis_pars[0], ml.nuis_pars[1]));
        }
      }
    }

    printf("\n");
  }

  TH1D* Fitter::make_h_bkg(const char* n, const std::vector<double>& nuis_pars) {
    std::vector<double> a(fit::n_bins+2, 0.);
    TH1D* h = (TH1D*)fit::interp->get_Q(nuis_pars)->h->Clone(n);
    fit::interp->interpolate(nuis_pars, &a);
    for (int ibin = 0; ibin <= fit::n_bins+1; ++ibin)
      h->SetBinContent(ibin, a[ibin]);
    return h;
  }

  void Fitter::draw_fit(const test_stat_t& t) {
    for (int sb = 1; sb >= 0; --sb) {
      const char* sb_or_b = sb ? "sb" : "b";
      const char* sb_or_b_nice = sb ? "sig + bkg" : "b only";
      const min_lik_t& ml = sb ? t.h1 : t.h0;
      TCanvas* c = new TCanvas(TString::Format("c_%s_fit", sb_or_b));

      TH1D* h_bkg_fit = make_h_bkg(TString::Format("h_bkg_%s_fit",  sb_or_b), ml.nuis_pars);
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
        h->SetTitle(TString::Format("best %s fit: %s;svdist2d (cm);events/bin width", sb_or_b_nice, ml.title().c_str()));

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

  Fitter::min_lik_t Fitter::min_likelihood(double mu_sig_start, bool fix_mu_sig) {
    fit::globals_ok();

    min_lik_t ret;

    TMinuit* m = new TMinuit(4);
    m->SetPrintLevel(print_level);
    m->SetFCN(fit::minfcn);
    int ierr;
    m->mnparm(0, "mu_sig", (mu_sig_start > 0 ? mu_sig_start : 0), 0.1, 0, (mu_sig_start > 0 ? mu_sig_start : 5000), ierr);
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
      double start = (maxs[ipar] + mins[ipar])/2;
      double delta = (maxs[ipar] - mins[ipar])/20;
      m->mnparm(2+ipar, nuis_par_names[ipar], start, delta, mins[ipar], maxs[ipar], ierr);
    }

    if (fix_mu_sig)
      m->FixParameter(0);

    m->Migrad();
    //      m->mnmnos();
    double fmin, fedm, errdef;
    int npari, nparx, istat;
    m->mnstat(fmin, fedm, errdef, npari, nparx, istat);

    ret.maxtwolnL = -fmin;
    m->GetParameter(0, ret.mu_sig, ret.err_mu_sig);
    m->GetParameter(1, ret.mu_bkg, ret.err_mu_bkg);
    ret.nuis_pars.resize(npars);
    ret.nuis_par_errs.resize(npars);
    for (size_t ipar = 0; ipar < npars; ++ipar)
      m->GetParameter(2+ipar, ret.nuis_pars[ipar], ret.nuis_par_errs[ipar]);
    ret.ok = istat == 3;
    ret.istat = istat;

    //printf("min_likelihood: %s  istat: %i   maxtwolnL: %e   mu_sig: %f +- %f  mu_bkg: %f +- %f\n", bkg_template->title().c_str(), istat, maxtwolnL, mu_sig, err_mu_sig, mu_bkg, err_mu_bkg);
    delete m;
    return ret;
  }

  Fitter::test_stat_t Fitter::calc_test_stat(double fix_mu_sig_val) {
    test_stat_t t;
    t.h1 = min_likelihood(fix_mu_sig_val, false);
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
  }

  void Fitter::fit(int toy_, Templater* bkg_templater, TH1D* sig_template, const VertexPairs& v2v, const std::vector<double>& true_pars_) {
    toy = toy_;
    true_pars = true_pars_;

    dtoy = dout->mkdir(TString::Format("seed%02i_toy%02i", seed, toy));

    ////

    dtoy->mkdir("finalized_templates")->cd();

    fit::set_sig(Template::finalize_template(sig_template));

    bkg_templates = bkg_templater->get_templates();
    fit::interp = new TemplateInterpolator(bkg_templates, fit::n_bins, bkg_templater->par_info(), fit::a_bkg);

    std::map<int, int> template_index_deltas;
    for (int i = 0, ie = bkg_templates->size(); i < ie; ++i) {
      //printf("bkg template #%5i: %s\n", i, bkg_templates->at(i)->title().c_str());
      const int delta = abs(i - fit::interp->i_Q(bkg_templates->at(i)->pars));
      template_index_deltas[delta] += 1;
    }
    //jmt::vthrow("something wrong with templates");

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

    pval_signif = 1;
    pval_limits.clear();
    mu_sig_limits.clear();
    t_obs_limit = test_stat_t();
    mu_sig_limit = 1e-6;
    pval_limit = 1;

    draw_likelihood(t_obs_0);
    draw_fit(t_obs_0);


    printf("throwing %i significance toys:\n", n_toy_signif);
    jmt::ProgressBar pb_signif(50, n_toy_signif);
    if (!print_toys)
      pb_signif.start();

    TH1D* h_bkg_obs_0 = make_h_bkg("h_bkg_obs_0", t_obs_0.h0.nuis_pars);
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

    if (do_limits) {
      mu_sig_limit = 1e-6;
      pval_limit = 1;
      std::vector<test_stat_t> t_obs_limits;
      const double limit_alpha = 0.05;
      const double mu_sig_limit_stop = n_data;

      printf("scanning for %.1f%% upper limit:\n", 100*(1-limit_alpha));
      jmt::ProgressBar pb_limits(50, mu_sig_limit_stop / mu_sig_limit_step);
      if (!print_toys)
        pb_limits.start();

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

          make_toy_data(-1, i_toy_limit, n_sig_limit, n_bkg_limit, h_bkg_obs_0);
      
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

    delete fit::interp;
  }
}
