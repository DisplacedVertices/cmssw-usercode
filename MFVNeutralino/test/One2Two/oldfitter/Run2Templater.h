#ifndef JMTucker_MFVNeutralino_One2Two_Run2Templater_h
#define JMTucker_MFVNeutralino_One2Two_Run2Templater_h

#include "ConfigFromEnv.h"
#include "Templater.h"

class TF1;
class TFile;
class TH1D;
class TH2D;
class TRandom;
class TTree;

namespace mfv {
  struct Run2Templater : public Templater {
    jmt::ConfigFromEnv env;

    const double d2d_cut;
    const double dphi_c;
    const double dphi_e;
    const double dphi_a;
    const std::string eff_fn;
    const std::string eff_path;
    const int noversamples;
    const int sample_count;

    TF1* f_dphi;
    TH1D* h_eff;

    ////////////////////////////////////////////////////////////////////////////

    virtual std::vector<double> true_pars() const { return std::vector<double>(); }
    virtual std::vector<TemplatePar> par_info() const;

    ////////////////////////////////////////////////////////////////////////////

    TTree* t_fit_info;
    
    ////////////////////////////////////////////////////////////////////////////

    Run2Templater(const std::string& name_, TFile* f, TRandom* r);

    void book_trees();
    void book_toy_fcns_and_histos();
    bool is_sideband(const VertexSimple&, const VertexSimple&) const;
    void make_templates();
    void process_imp();
  };
}

#endif
