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

namespace mfv {
  struct Fitter {
    const std::string name;
    const std::string uname;

    jmt::ConfigFromEnv env;
    const int print_level;
    const int n_toy_signif;
    const int n_toy_limit;
    const bool print_toys;
    const bool save_toys;
    const bool do_limits;
    const double mu_sig_limit_step;

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
      double mu_bkg;
      double err_mu_bkg;
      bool all_ok;
      Template* nuis;
      std::vector<std::pair<double, Template*> > nuis_region;

      min_lik_t() : ok(true), maxtwolnL(-1e300), mu_sig(-1), err_mu_sig(-1), mu_bkg(-1), err_mu_bkg(-1), all_ok(true) {}

      std::pair<std::vector<double>, std::vector<double> > get_template_par_ranges(const double up) const;
      void print(const char* header, const char* indent="  ") const;
    };

    struct test_stat_t {
      min_lik_t h1;
      min_lik_t h0;
      double t;
      bool ok() const { return h1.ok && h0.ok; }

      void print(const char* header, const char* indent="  ") const;
    };

    ////////////////////////////////////////////////////////////////////////////

    int toy;
    Templates* bkg_templates;

    std::vector<double> true_pars;

    double glb_scan_maxtwolnL;
    std::vector<double> glb_scan_max_pars;
    std::vector<double> glb_scan_max_pars_errs;

    test_stat_t t_obs_0;
    double pval_signif;
    std::vector<double> pval_limits;
    std::vector<double> mu_sig_limits;
    test_stat_t t_obs_limit;
    double pval_limit;
    double mu_sig_limit;

    ////////////////////////////////////////////////////////////////////////////

    TTree* t_fit_info;
    
    ////////////////////////////////////////////////////////////////////////////

    Fitter(const std::string& name_, TFile* f, TRandom* r);
    //    ~Fitter();

    void book_trees();
    void book_toy_fcns_and_histos();
    void fit_globals_ok();
    //    bool scan_likelihood();
    void draw_likelihood(const test_stat_t& t);
    void draw_fit(const test_stat_t& t);
    min_lik_t scanmin_likelihood(double mu_sig, bool fix_mu_sig);
    test_stat_t calc_test_stat(double fix_mu_sig_val);
    void make_toy_data(int i_toy_signif, int i_toy_limit, int n_sig, int n_bkg);
    void fit(int toy_, Templates* bkg_templates, TH1D* sig_template, const VertexPairs& v2v, const std::vector<double>& true_pars_);
  };
}

#endif
