#ifndef JMTucker_MFVNeutralino_One2Two_PhiShiftTemplater_h
#define JMTucker_MFVNeutralino_One2Two_PhiShiftTemplater_h

#include <functional>
#include "ConfigFromEnv.h"
#include "Templater.h"

class TF1;
class TFile;
class TH1D;
class TH2D;
class TRandom;
class TTree;

namespace mfv {
  struct PhiShiftTemplater : public Templater {
    jmt::ConfigFromEnv env;
    const double d2d_cut;
    const int sampling_type;
    const int sample_count;
    const int n_phi_exp;
    const double phi_exp_min;
    const double d_phi_exp;
    const int n_phi_interp;
    const double d_phi_interp;
    const int n_phi_total;
    const int n_shift;
    const bool find_g_phi;
    const bool find_g_dz;
    const bool find_f_phi;
    const bool find_f_dz;
    const bool find_f_phi_bkgonly;
    const bool find_f_dz_bkgonly;

    ////////////////////////////////////////////////////////////////////////////

    double phi_exp_bkgonly;
    double shift_means;
    virtual std::vector<double> true_pars() const { return std::vector<double>({phi_exp_bkgonly, shift_means}); }
    virtual std::vector<TemplatePar> par_info() const;

    TH1D* h_1v_g_phi;
    TH1D* h_1v_g_dz;
    TF1* g_phi;
    TF1* g_dz;
    TH1D* h_fcn_g_phi;
    TH1D* h_fcn_g_dz;

    TF1* f_phi;
    TF1* f_dz;
    std::vector<TH1D*> h_fcn_f_phis;
    TH1D* h_fcn_f_phi;
    TH1D* h_fcn_f_dz;

    double Mdp;
    double Mdz;

    ////////////////////////////////////////////////////////////////////////////

    TTree* t_fit_info;
    float b_g_phi_mean;
    float b_g_phi_mean_err;
    float b_g_phi_rms;
    float b_g_phi_rms_err;
    float b_g_phi_fit_offset;
    float b_g_phi_fit_offset_err;
    float b_g_phi_fit_slope;
    float b_g_phi_fit_slope_err;
    float b_g_phi_fit_chi2;
    float b_g_phi_fit_ndf;
    float b_g_dz_mean;
    float b_g_dz_mean_err;
    float b_g_dz_rms;
    float b_g_dz_rms_err;
    float b_g_dz_fit_sigma;
    float b_g_dz_fit_sigma_err;
    float b_g_dz_fit_mu;
    float b_g_dz_fit_mu_err;
    float b_g_dz_fit_chi2;
    float b_g_dz_fit_ndf;
    float b_f_phi_mean;
    float b_f_phi_mean_err;
    float b_f_phi_rms;
    float b_f_phi_rms_err;
    float b_f_phi_asym;
    float b_f_phi_asym_err;
    float b_f_phi_fit_exp;
    float b_f_phi_fit_exp_err;
    float b_f_phi_fit_offset;
    float b_f_phi_fit_offset_err;
    float b_f_phi_fit_chi2;
    float b_f_phi_fit_ndf;
    float b_f_dz_mean;
    float b_f_dz_mean_err;
    float b_f_dz_rms;
    float b_f_dz_rms_err;
    float b_f_dz_fit_sigma;
    float b_f_dz_fit_sigma_err;
    float b_f_dz_fit_mu;
    float b_f_dz_fit_mu_err;
    float b_f_dz_fit_chi2;
    float b_f_dz_fit_ndf;
    
    ////////////////////////////////////////////////////////////////////////////

    PhiShiftTemplater(const std::string& name_, TFile* f, TRandom* r);

    void book_trees();
    void book_toy_fcns_and_histos();
    bool is_sideband(const VertexSimple&, const VertexSimple&) const;
    void fit_envelopes();
    void fit_fs_in_sideband();
    void update_f_weighting_pars();
    void set_phi_exp(double);
    double prob_1v_pair(const VertexSimple&, const VertexSimple&) const;
    void loop_over_1v_pairs(std::function<void(const VertexPair&)>);
    void fill_1v_histos();
    void make_templates();
    virtual void process_imp();
  };
}

#endif
