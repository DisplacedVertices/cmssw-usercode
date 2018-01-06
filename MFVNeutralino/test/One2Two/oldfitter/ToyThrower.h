#ifndef JMTucker_MFVNeutralino_One2Two_ToyThrower_h
#define JMTucker_MFVNeutralino_One2Two_ToyThrower_h

#include <functional>
#include "ConfigFromEnv.h"
#include "SimpleObjects.h"
#include "Samples.h"

class TH1D;
class TFile;
class TTree;
class TRandom;

namespace mfv {
  struct ToyThrower {
    const std::string name;
    const std::string uname;
    const std::string path;

    jmt::ConfigFromEnv env;
    const bool from_histograms;
    const std::string from_histograms_fn;
    const int min_ntracks;
    const int min_ntracks0;
    const int max_ntracks0;
    const int min_ntracks1;
    const int max_ntracks1;
    const double int_lumi;
    const double scale_1v;
    const double scale_2v;
    const bool allow_cap;
    const bool poisson_means;
    const bool use_bkgsyst;
    const bool use_only_data_sample;
    const int sample_only;
    const int injected_signal;
    const double injected_signal_scale;
    const int template_signal;

    const Samples samples;
    std::string sample2fn(const Sample& s) { return path + "/" + s.name + ".root"; }

    int ntoys;

    TFile* fout;
    TDirectory* dout;
    TRandom* rand;
    const int seed;

    ////////////////////////////////////////////////////////////////////////////

    TH1D* h_bkg_dbv;
    TH1D* h_bkg_dvv;
    TH1D* h_bkg_dphi;
    TH1D* h_injected_signal_dbv;
    TH1D* h_injected_signal_dvv;
    TH1D* h_injected_signal_dphi;
    TH1D* h_injected_signal_norm;
    TH1D* h_template_signal_dvv;

    std::map<int, VertexSimples> all_1v;
    std::map<int, VertexPairs>   all_2v;

    std::map<int, EventSimples> events;
    std::map<int, EventSimples> events_1v;
    std::map<int, EventSimples> events_2v;

    std::map<int, double> lambda_1v;
    std::map<int, double> lambda_2v;

    EventSimples toy_events_1v;
    EventSimples toy_events_2v;
    VertexSimples toy_1v;
    VertexPairs toy_2v;
    Dataset toy_dataset;

    Dataset data;

    TH1D* h_dbv;
    TH1D* h_dvv;
    
    ////////////////////////////////////////////////////////////////////////////

    TTree* t_sample_usage_1v;
    int b_sample_usage_1v_key;
    int b_sample_usage_1v_ndx;
    TTree* t_sample_usage_2v;
    int b_sample_usage_2v_key;
    int b_sample_usage_2v_ndx;
    TTree* t_toy_stats_1v;
    std::map<int, int> b_toy_stats_1v;
    int b_sum_1v;
    int b_sum_bkg_1v;
    int b_sum_sig_1v;
    TTree* t_toy_stats_2v;
    std::map<int, int> b_toy_stats_2v;
    int b_sum_2v;
    int b_sum_bkg_2v;
    int b_sum_sig_2v;
    
    ////////////////////////////////////////////////////////////////////////////

    ToyThrower(const std::string& name_, const std::string& path_, TFile* f, TRandom* r);

    void book_hists();
    bool sel_vertex(const VertexSimple& v) const;
    void read_histograms();
    void read_sample(const Sample& sample);
    void loop_over_samples(std::function<void(const Sample&)> fcn);
    void update_poisson_means();
    void read_samples();
    void book_and_fill_some_trees();
    void throw_toy();
    TH1D* hist_with_template_binning(const char* name, const char* title, const VertexPairs& v2v) const;
    TH1D* signal_template(const char* name, const char* title) const;
  };
}

#endif
