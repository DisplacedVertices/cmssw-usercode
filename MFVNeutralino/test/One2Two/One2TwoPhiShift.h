#ifndef JMTucker_MFVNeutralino_One2Two_One2TwoPhiShift_h
#define JMTucker_MFVNeutralino_One2Two_One2TwoPhiShift_h

#include <functional>
#include "ConfigFromEnv.h"
#include "SimpleObjects.h"
#include "Templates.h"

class TF1;
class TFile;
class TH1D;
class TH2D;
class TRandom;
class TTree;

namespace mfv {
  struct One2TwoPhiShift {
    const std::string name;
    const std::string uname;

    jmt::ConfigFromEnv env;
    const double d2d_cut;
    const int sampling_type;
    const int sample_count;
    const double phi_exp_min;
    const double phi_exp_max;
    const double d_phi_exp;
    const int n_phi_interp;
    const int n_shift;
    const bool use_abs_phi;
    const int template_nbins;
    const double template_min;
    const double template_max;
    const bool find_g_phi;
    const bool find_g_dz;
    const bool find_f_phi;
    const bool find_f_dz;
    const bool find_f_phi_bkgonly;
    const bool find_f_dz_bkgonly;

    TFile* fout;
    TDirectory* dout;
    TDirectory* dtoy;
    TRandom* rand;
    const int seed;

    ////////////////////////////////////////////////////////////////////////////

    int toy;
    const VertexSimples* one_vertices;
    const VertexPairs* two_vertices;

    Templates templates;

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

    double gdpmax;
    double fdpmax;
    double Mdp;
    double gdzmax;
    double fdzmax;
    double Mdz;

    enum { vt_2v, vt_2vbkg, vt_2vsig, vt_2vsb, vt_2vsbbkg, vt_2vsbsig,  n_vt_2v, vt_1v = n_vt_2v, vt_1vsb,  n_vt_pairs, vt_1vsingle = n_vt_pairs, n_vt };
    static const char* vt_names[n_vt];

    TH1D* h_issig[n_vt];
    TH1D* h_issig_0[n_vt];
    TH1D* h_issig_1[n_vt];
    TH2D* h_xy[n_vt];
    TH1D* h_bsd2d[n_vt];
    TH2D* h_bsd2d_v_bsdz[n_vt];
    TH1D* h_bsdz[n_vt];
    TH1D* h_bsd2d_0[n_vt];
    TH2D* h_bsd2d_v_bsdz_0[n_vt];
    TH1D* h_bsdz_0[n_vt];
    TH1D* h_bsd2d_1[n_vt];
    TH2D* h_bsd2d_v_bsdz_1[n_vt];
    TH1D* h_bsdz_1[n_vt];
    TH2D* h_ntracks[n_vt];
    TH1D* h_ntracks01[n_vt];
    TH1D* h_d2d[n_vt];
    TH1D* h_phi[n_vt];
    TH1D* h_dz[n_vt];

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

    One2TwoPhiShift(const std::string& name_, TFile* f, TRandom* r);
    ~One2TwoPhiShift();

    void book_trees();
    void book_toy_fcns_and_histos();
    bool is_sideband(const VertexSimple&, const VertexSimple&) const;
    void fill_2v(const int ih, const double w, const VertexSimple&, const VertexSimple&);
    void fill_2v_histos();
    void fit_envelopes();
    void fit_fs_in_sideband();
    void update_f_weighting_pars();
    void set_phi_exp(double);
    double prob_1v_pair(const VertexSimple&, const VertexSimple&) const;
    void loop_over_1v_pairs(std::function<void(const VertexPair&)>);
    void fill_1v_histos();
    void clear_templates();
    void make_templates();
    void process(int toy, const VertexSimples*, const VertexPairs*);
  };
}

#endif
