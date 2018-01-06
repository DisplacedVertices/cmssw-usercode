#ifndef JMTucker_MFVNeutralino_One2Two_Templater_h
#define JMTucker_MFVNeutralino_One2Two_Templater_h

#include "ConfigFromEnv.h"
#include "SimpleObjects.h"
#include "Templates.h"

class TH1D;
class TH2D;
class TFile;
class TRandom;

namespace mfv {
  struct Templater {
    const std::string dname;
    const std::string name;
    const std::string uname;

    jmt::ConfigFromEnv env;
    const int min_ntracks0;
    const int max_ntracks0;
    const int min_ntracks1;
    const int max_ntracks1;

    TFile* fout;
    TDirectory* dout;
    TDirectory* dtoy;
    TRandom* rand;
    const int seed;
    bool save_plots;

    ////////////////////////////////////////////////////////////////////////////

    Dataset dataset;

    Templates templates;
    Templates* get_templates() { return &templates; }

    virtual std::vector<double> true_pars() const = 0;
    virtual std::vector<TemplatePar> par_info() const = 0;

    enum { vt_2v, vt_2vbkg, vt_2vsig, vt_2vsb, vt_2vsbbkg, vt_2vsbsig,  n_vt_2v, vt_1v = n_vt_2v, vt_1vsb,  n_vt_pairs, vt_1vsingle = n_vt_pairs, n_vt };
    static const char* vt_names[n_vt];

    TH1D* h_issig[n_vt];
    TH1D* h_issig_0[n_vt];
    TH1D* h_issig_1[n_vt];
    TH2D* h_xy[n_vt];
    TH1D* h_bsd2d[n_vt];
    TH1D* h_bsd2d0[n_vt];
    TH1D* h_bsd2d1[n_vt];
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

    Templater(const std::string& dname_, const std::string& name_, TFile* f, TRandom* r);
    ~Templater();

    virtual bool is_sideband(const VertexSimple&, const VertexSimple&) const = 0;

    virtual void book_hists();
    virtual void fill_2v(const int ih, const double w, const VertexSimple& v0, const VertexSimple& v1);
    virtual void dataset_ok();
    virtual void fill_2v_histos();
    virtual void clear_templates();
    virtual void process(const Dataset&);
    virtual void process_imp() = 0;
  };
}

#endif
