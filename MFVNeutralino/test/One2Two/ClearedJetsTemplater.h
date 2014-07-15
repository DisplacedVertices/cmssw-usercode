#ifndef JMTucker_MFVNeutralino_One2Two_ClearedJetsTemplater_h
#define JMTucker_MFVNeutralino_One2Two_ClearedJetsTemplater_h

#include "ConfigFromEnv.h"
#include "Templater.h"

class TF1;
class TFile;
class TH1D;
class TH2D;
class TRandom;
class TTree;

namespace mfv {
  struct ClearedJetsTemplater : public Templater {
    jmt::ConfigFromEnv env;

    const double d2d_cut;
    const int sample_count;
    const double angle_from_jet_mu;
    const double angle_from_jet_sigma;
    const double clearing_mu;
    const double clearing_sigma;

    ////////////////////////////////////////////////////////////////////////////

    double clearing_mu_fit;
    double clearing_sigma_fit;
    virtual std::vector<double> true_pars() const { return std::vector<double>({clearing_mu_fit, clearing_sigma_fit}); }
    virtual std::vector<TemplatePar> par_info() const { return std::vector<TemplatePar>(2); }

    ////////////////////////////////////////////////////////////////////////////

    TTree* t_fit_info;
    
    ////////////////////////////////////////////////////////////////////////////

    ClearedJetsTemplater(const std::string& name_, TFile* f, TRandom* r);

    void book_trees();
    void book_toy_fcns_and_histos();
    void make_templates();
    bool is_sideband(const VertexSimple&, const VertexSimple&) const;
    void process_imp();
  };
}

#endif
