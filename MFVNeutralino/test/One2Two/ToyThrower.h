#ifndef JMTucker_MFVNeutralino_One2Two_ToyThrower_h
#define JMTucker_MFVNeutralino_One2Two_ToyThrower_h

#include <functional>
#include "ConfigFromEnv.h"
#include "SimpleObjects.h"
#include "Samples.h"

class TFile;
class TTree;
class TRandom;

namespace mfv {
  struct ToyThrower {
    const std::string name;
    const std::string uname;
    const std::string path;

    jmt::ConfigFromEnv env;
    const int seed;
    const int min_ntracks;
    const double int_lumi;
    const double scale;
    const bool allow_cap;
    const bool poisson_means;
    const bool use_qcd500;
    const int sample_only;
    const int signal;
    const double signal_scale;

    const Samples samples;
    std::string sample2fn(const Sample& s) { return path + "/" + s.name + ".root"; }

    int ntoys;

    const bool make_trees;
    TFile* fout;
    TDirectory* dout;
    bool own_rand;
    TRandom* rand;

    ////////////////////////////////////////////////////////////////////////////

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

    ////////////////////////////////////////////////////////////////////////////

    TTree* t_config;
    TTree* t_sample_info;
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

    ToyThrower(const std::string& name_, const std::string& path_, TFile* f);
    ~ToyThrower();
    void set_rand(TRandom* r);

    ////////////////////////////////////////////////////////////////////////////

    bool sel_vertex(const VertexSimple& v) const;
    void read_sample(const Sample& sample);
    void loop_over_samples(std::function<void(const Sample&)> fcn);
    void update_poisson_means();
    void book_trees();
    void read_samples();
    void throw_toy();
  };
}

#endif
