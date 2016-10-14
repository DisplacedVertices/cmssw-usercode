#ifndef JMTucker_MFVNeutralino_One2Two_Fitter_h
#define JMTucker_MFVNeutralino_One2Two_Fitter_h

#include <string>
#include <vector>

#include "ConfigFromEnv.h"
#include "SimpleObjects.h"
#include "Templates.h"

class TDirectory;
class TFile;
class TRandom;
class TString;
class TTree;
class TH1F;

namespace mfv {
  class Templater;

  struct Fitter {
    const std::string name;
    const std::string uname;

    jmt::ConfigFromEnv env;
    int print_level;
    const bool save_plots;
    const int inject_in_last_bin;
    const bool bkg_gaussians;
    const bool bkg_gaussians_all;
    const bool barlow_beeston;
    const bool bend_bkg;
    const bool allow_negative_mu_sig;
    const bool run_mnseek;
    const bool run_minos;
    const bool draw_bkg_templates;
    const bool fix_nuis0;
    const bool fix_nuis1;
    const double start_nuis0;
    const double start_nuis1;
    const bool fluctuate_toys_shapes;
    const int n_toy_signif;
    const bool print_toys;
    const bool print_subtoys;
    const bool save_toys;
    const bool do_signif;
    const bool do_limit;
    const bool only_fit;
    const int n_toy_cls;
    const bool do_cls;
    const int i_limit_job;
    const int n_toy_limit;
    const double sig_limit_start;
    const double sig_limit_stop;
    const double sig_limit_step;
    const double sig_eff;
    const double sig_eff_uncert;
    const bool bracket_limit;

    TFile* fout;
    TDirectory* dout;
    TDirectory* dtoy;
    TRandom* rand;
    const int seed;

    static const int npars;

    ////////////////////////////////////////////////////////////////////////////

    struct min_lik_t {
      bool ok;
      int istat;
      double maxtwolnL;
      double mu_sig;
      double err_mu_sig;
      double eplus_mu_sig;
      double eminus_mu_sig;
      double mu_bkg;
      double err_mu_bkg;
      double eplus_mu_bkg;
      double eminus_mu_bkg;
      bool all_ok;
      double nuis0;
      double err_nuis0;
      double eplus_nuis0;
      double eminus_nuis0;
      double nuis1;
      double err_nuis1;
      double eplus_nuis1;
      double eminus_nuis1;
      double correlation_nuis;
      std::vector<double> A_sig;
      std::vector<double> A_bkg;
      std::vector<double> A_sig_rel;
      std::vector<double> A_bkg_rel;
      double A_sig_sum;
      double A_bkg_sum;

      min_lik_t() : ok(true), maxtwolnL(-1e300), mu_sig(-1), err_mu_sig(-1), mu_bkg(-1), err_mu_bkg(-1), all_ok(true) {}

      double sig_yield_in_bin(const size_t i) const { return mu_sig * A_sig[i]; }
      double bkg_yield_in_bin(const size_t i) const { return mu_bkg * A_bkg[i]; }
      double yield_in_bin(const size_t i) const { return sig_yield_in_bin(i) + bkg_yield_in_bin(i); }

      std::vector<double> nuis_pars() const { return std::vector<double>({nuis0, nuis1}); }
      std::string nuis_title() const;
      std::string mu_title() const;
      std::string title() const;
      void print(const char* header, const char* indent="  ") const;
    };

    struct test_stat_t {
      min_lik_t h1;
      min_lik_t h0;
      double t;
      bool ok() const { return h1.ok && h0.ok; }

      void print(const char* header, const int i=-1, const char* indent="  ") const;
    };

    struct fit_stat_t {
      double chi2;
      double ndof;
      double prob;
      double ks;
    };

    ////////////////////////////////////////////////////////////////////////////

    int toy;
    Templates* bkg_templates;

    std::vector<double> true_pars;

    test_stat_t t_obs_0;
    fit_stat_t fit_stat;
    double pval_signif;
    double pval_cls;
    std::vector<double> sig_limits;
    std::vector<double> pval_limits;
    std::vector<double> pval_limit_errs;
    double sig_limit;
    double sig_limit_err;
    int    sig_limit_fit_n;
    double sig_limit_fit_a;
    double sig_limit_fit_b;
    double sig_limit_fit_a_err;
    double sig_limit_fit_b_err;
    double sig_limit_fit_prob;

    ////////////////////////////////////////////////////////////////////////////

    TTree* t_fit_info;
    std::vector<TH1F*> h_signif_toy;
    std::vector<TH1F*> h_limit_toy;
    
    ////////////////////////////////////////////////////////////////////////////

    Fitter(const std::string& name_, TFile* f, TRandom* r);

    void book_trees();
    void book_toy_fcns_and_histos();
    void fit_globals_ok();
    void draw_likelihood(const test_stat_t& t, const char* ex=0);
    TH1D* make_h_bkg(const char* n, const std::vector<double>& nuis_pars, const std::vector<double>& A_bkg);
    void scan_template_chi2(const test_stat_t& t);
    fit_stat_t draw_fit(const test_stat_t& t);
    min_lik_t min_likelihood(double mu_sig_start, bool fix_mu_sig);
    test_stat_t calc_test_stat(double fix_mu_sig_val);
    void make_toy_data(int i_toy_signif, int i_toy_limit, int i_toy_expect, int n_sig, int n_bkg, TH1D* h_bkg);
    void fit(int toy_, Templater* bkg_templater, TH1D* sig_template, const VertexPairs& v2v, const std::vector<double>& true_pars_);
  };
}

#endif
