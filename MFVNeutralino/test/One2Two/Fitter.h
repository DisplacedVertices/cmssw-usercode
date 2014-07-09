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

    TFile* fout;
    TDirectory* dout;
    TDirectory* dtoy;
    TRandom* rand;
    const int seed;

    static const int npars;

    ////////////////////////////////////////////////////////////////////////////

    int toy;
    Templates* bkg_templates;

    std::vector<double> true_pars;

    double glb_scan_maxtwolnL;
    std::vector<double> glb_scan_max_pars;
    std::vector<double> glb_scan_max_pars_errs;

    double glb_scanmin_sb_maxtwolnL;
    std::vector<double> glb_scanmin_sb_max_pars;
    std::vector<double> glb_scanmin_sb_max_pars_errs;
    Template* glb_scanmin_sb_template;
    double glb_scanmin_b_maxtwolnL;
    std::vector<double> glb_scanmin_b_max_pars;
    std::vector<double> glb_scanmin_b_max_pars_errs;
    Template* glb_scanmin_b_template;

    ////////////////////////////////////////////////////////////////////////////

    TTree* t_fit_info;
    
    ////////////////////////////////////////////////////////////////////////////

    Fitter(const std::string& name_, TFile* f, TRandom* r);
    //    ~Fitter();

    void book_trees();
    std::vector<double> binning() const;
    TH1D* hist_with_binning(const TString& name, const TString& title);
    TH1D* finalize_binning(TH1D* h);
    TH1D* finalize_template(TH1D* h);
    void book_toy_fcns_and_histos();
    void fit_globals_ok();
    bool scan_likelihood();
    bool scanmin_likelihood(bool bkg_only);
    void fit(int toy_, Templates* bkg_templates, TH1D* sig_template, const VertexPairs& v2v, const std::vector<double>& true_pars_);
  };
}

#endif
