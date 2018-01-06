#ifndef JMTucker_MFVNeutralino_One2Two_SimpleClearingTemplater_h
#define JMTucker_MFVNeutralino_One2Two_SimpleClearingTemplater_h

#include "ConfigFromEnv.h"
#include "Templater.h"

class TF1;
class TFile;
class TH1D;
class TH2D;
class TRandom;
class TTree;

namespace mfv {
  struct SimpleClearingTemplater : public Templater {
    jmt::ConfigFromEnv env;

    const double d2d_cut;
    const int sample_count;
    const double clearing_sigma_start;
    const double d_clearing_sigma;
    const int n_clearing_sigma;

    ////////////////////////////////////////////////////////////////////////////

    double clearing_sigma_fit;
    virtual std::vector<double> true_pars() const { return std::vector<double>({clearing_sigma_fit, 0}); }
    virtual std::vector<TemplatePar> par_info() const;

    ////////////////////////////////////////////////////////////////////////////

    TTree* t_fit_info;
    
    ////////////////////////////////////////////////////////////////////////////

    SimpleClearingTemplater(const std::string& name_, TFile* f, TRandom* r);

    void book_trees();
    void book_toy_fcns_and_histos();
    bool is_sideband(const VertexSimple&, const VertexSimple&) const;
    void make_templates();
    void process_imp();
  };
}

#endif
