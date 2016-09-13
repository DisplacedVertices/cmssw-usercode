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
    const bool load_from_file;
    const std::string load_from_file_fn;
    const std::string load_from_file_path;
    const bool save_templates;
    const bool finalize_templates;
    const int sample_every;
    const int sample_count;
    const bool throw_h_bsd2d;
    const bool throw_dphi_from_2v;
    const bool flat_phis;
    const double phi_from_jet_mu;
    const double phi_from_jet_sigma;
    const bool dphi_from_pdf;
    const double dphi_pdf_c;
    const double dphi_pdf_e;
    const double dphi_pdf_a;
    const int n_scale;
    const bool fixed_clearing;
    const double clearing_mu_start;
    const double d_clearing_mu;
    const int n_clearing_mu;
    const double clearing_sigma_start;
    const double d_clearing_sigma;
    const int n_clearing_sigma;

    ////////////////////////////////////////////////////////////////////////////

    double clearing_mu_fit;
    double clearing_sigma_fit;
    virtual std::vector<double> true_pars() const { return std::vector<double>({clearing_mu_fit, clearing_sigma_fit}); }
    virtual std::vector<TemplatePar> par_info() const;

    ////////////////////////////////////////////////////////////////////////////

    TTree* t_fit_info;

    TF1* f_dphi;

    ////////////////////////////////////////////////////////////////////////////

    ClearedJetsTemplater(const std::string& name_, TFile* f, TRandom* r);

    void book_trees();
    void book_toy_fcns_and_histos();
    bool is_sideband(const VertexSimple&, const VertexSimple&) const;
    double throw_phi(const EventSimple& ev) const;
    void make_templates();
    void process_imp();
  };
}

#endif
