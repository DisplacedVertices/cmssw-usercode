#include "ToyThrower.h"
#include "TFile.h"
#include "TRandom3.h"
#include "TTree.h"
#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"
#include "Random.h"

namespace mfv {
  ToyThrower::ToyThrower(const std::string& name_, const std::string& path_, TFile* f)
    : name(name_),
      path(path_),

      env(name.size() ? "mfvo2t_toythrower_" + name : "mfvo2t_toythrower"),
      seed(env.get_int("seed", 0)),
      min_ntracks(env.get_int("min_ntracks", 5)),
      int_lumi(env.get_double("int_lumi", 18.2e3)),
      scale(env.get_double("scale", 1.)),
      allow_cap(env.get_bool("allow_cap", false)),
      poisson_means(env.get_bool("poisson_means", true)),
      use_qcd500(env.get_bool("use_qcd500", false)),
      sample_only(env.get_int("sample_only", 0)),
      signal(env.get_int("signal", 0)),
      signal_scale(env.get_double("signal_scale", 1.)),

      ntoys(0),

      make_trees(f != 0),
      fout(f),
      dout(make_trees ? f->mkdir(TString::Format("ToyThrower_%s_seed%i", name.c_str(), seed)) : 0),
      own_rand(true),
      rand(new TRandom3(12191982 + seed))
  {
    printf("ToyThrower %s config:\n", name.c_str());
    printf("(read ntuples from %s)\n", path.c_str());
    printf("seed: %i\n", seed);
    printf("min_ntracks: %i\n", min_ntracks);
    printf("int_lumi: %f\n", int_lumi);
    printf("scale: %f\n", scale);
    printf("poisson_means: %i\n", poisson_means);
    printf("use_qcd500: %i\n", use_qcd500);
    printf("sample_only: %i (%s)\n", sample_only, samples.get(sample_only).name.c_str());
    printf("signal: %i (%s)\n", signal, samples.get(signal).name.c_str());
    printf("signal_scale: %g\n", signal_scale);

    read_samples();
    book_trees();
  }

  ToyThrower::~ToyThrower() {
    if (own_rand)
      delete rand;
  }

  void ToyThrower::set_rand(TRandom* r) {
    if (rand)
      delete rand;
    own_rand = false;
    rand = r;
  }

  bool ToyThrower::sel_vertex(const VertexSimple& v) const {
    return v.ntracks >= min_ntracks;
  }

  void ToyThrower::read_sample(const Sample& sample) {
    std::string fn  = sample2fn(sample);

    TFile* f = TFile::Open(fn.c_str());
    if (!f)
      jmt::vthrow("could not read file %s", fn.c_str());

    const std::string tree_path = "mfvMiniTree/t";
    TTree* tree = (TTree*)f->Get(tree_path.c_str());
    if (!tree)
      jmt::vthrow("could not get %s from file %s", tree_path.c_str(), fn.c_str());

    MiniNtuple nt;
    read_from_tree(tree, nt);

    for (int j = 0, je = tree->GetEntries(); j < je; ++j) {
      if (tree->LoadTree(j) < 0) break;
      if (tree->GetEntry(j) <= 0) continue;

      EventSimple e(nt);
      e.sample = sample.key;
      e.nvtx_sel = 0;

      if (nt.nvtx == 1) {
        VertexSimple v0(nt, 0, sample.is_sig());
        if (sel_vertex(v0)) {
          all_1v[sample.key].push_back(v0);
          e.nvtx_sel = 1;
        }
      }
      else if (nt.nvtx == 2) {
        VertexSimple v0(nt, 0, sample.is_sig());
        VertexSimple v1(nt, 1, sample.is_sig());
        const bool sel0 = sel_vertex(v0);
        const bool sel1 = sel_vertex(v1);
        if (sel0 && sel1) {
          all_2v[sample.key].push_back(VertexPair(v0, v1));
          e.nvtx_sel = 2;
        }
        else if (sel0 || sel1) {
          all_1v[sample.key].push_back(sel0 ? v0 : v1);
          e.nvtx_sel = 1;
        }
      }

      events[sample.key].push_back(e);
      if (e.nvtx_sel == 1)
        events_1v[sample.key].push_back(e);
      else if (e.nvtx_sel == 2)
        events_2v[sample.key].push_back(e);
    }
  }

  void ToyThrower::loop_over_samples(std::function<void(const Sample&)> fcn) {
    if (sample_only)
      fcn(samples.get(sample_only));
    else {
      for (const Sample& sample : samples.samples)
        //if (sample.name != "qcdht0100" && sample.name != "qcdht0250" && 
        if ((!sample.is_sig() || sample.key == signal) && (use_qcd500 || sample.name != "qcdht0500"))
          fcn(sample);
    }
  }

  void ToyThrower::update_poisson_means() {
    printf("ToyThrower(%s)::sample info (without any scaling):\n", name.c_str());
    auto f = [this](const Sample& sample) {
      const double w = sample.weight(int_lumi);
      const int N1v = int(all_1v[sample.key].size());
      const int N2v = int(all_2v[sample.key].size());
      const double W1v = lambda_1v[sample.key] = w * N1v;
      const double W2v = lambda_2v[sample.key] = w * N2v;
      printf("%-30s (%3i), weight %8.4g: %10i (%10.2f) 1v events,  %5i (%10.2f) 2v events\n", sample.name.c_str(), sample.key, w, N1v, W1v, N2v, W2v);
    };

    loop_over_samples(f);
  }

  void ToyThrower::read_samples() {
    loop_over_samples([this](const Sample& s) { read_sample(s); });
    update_poisson_means();
  }

  void ToyThrower::book_trees() {
    if (!make_trees)
      return;

    TDirectory* d = dout ? dout : fout;


    t_config = new TTree("t_config", "");
    t_config->SetDirectory(d);
    t_config->SetAlias("name", name.c_str());
    t_config->SetAlias("path", path.c_str());
    t_config->Branch("seed", const_cast<int*>(&seed), "seed/I");
    t_config->Branch("min_ntracks", const_cast<int*>(&min_ntracks), "min_ntracks/I");
    t_config->Branch("int_lumi", const_cast<double*>(&int_lumi), "int_lumi/D");
    t_config->Branch("scale", const_cast<double*>(&scale), "scale/D");
    t_config->Branch("poisson_means", const_cast<bool*>(&poisson_means), "poisson_means/O");
    t_config->Branch("use_qcd500", const_cast<bool*>(&use_qcd500), "use_qcd500/O");
    t_config->Branch("sample_only", const_cast<int*>(&sample_only), "sample_only/I");
    t_config->Branch("signal", const_cast<int*>(&signal), "signal/I");
    t_config->Branch("signal_scale", const_cast<double*>(&signal_scale), "signal_scale/D");
    t_config->Fill();

    {
      t_sample_info = new TTree("t_sample_info", "");
      t_sample_info->SetDirectory(d);
      int b_sample_info_key;
      double b_sample_info_weight;
      int b_sample_info_N1v;
      int b_sample_info_N2v;
      t_sample_info->Branch("key", &b_sample_info_key, "key/I");
      t_sample_info->Branch("weight", &b_sample_info_weight, "weight/D");
      t_sample_info->Branch("N1v", &b_sample_info_N1v, "N1v/I");
      t_sample_info->Branch("N2v", &b_sample_info_N2v, "N2v/I");

      auto f = [this, &b_sample_info_key, &b_sample_info_weight, &b_sample_info_N1v, &b_sample_info_N2v](const Sample& sample) {
        t_sample_info->SetAlias(sample.name.c_str(), TString::Format("%i", sample.key));
        b_sample_info_key = sample.key;
        b_sample_info_weight = sample.weight(int_lumi);
        b_sample_info_N1v = int(all_1v[sample.key].size());
        b_sample_info_N2v = int(all_2v[sample.key].size());
        t_sample_info->Fill();
      };

      loop_over_samples(f);
    }

    t_sample_usage_1v = new TTree("t_sample_usage_1v", "");
    t_sample_usage_1v->SetDirectory(d);
    t_sample_usage_1v->Branch("key", &b_sample_usage_1v_key, "key/I");
    t_sample_usage_1v->Branch("ndx", &b_sample_usage_1v_ndx, "ndx/I");

    t_sample_usage_2v = new TTree("t_sample_usage_2v", "");
    t_sample_usage_2v->SetDirectory(d);
    t_sample_usage_2v->Branch("key", &b_sample_usage_2v_key, "key/I");
    t_sample_usage_2v->Branch("ndx", &b_sample_usage_2v_ndx, "ndx/I");

    {
      t_toy_stats_1v = new TTree("t_toy_stats_1v", "");
      t_toy_stats_2v = new TTree("t_toy_stats_2v", "");
      t_toy_stats_1v->SetDirectory(d);
      t_toy_stats_2v->SetDirectory(d);

      auto f = [this](const Sample& sample) {
        b_toy_stats_1v[sample.key] = 0;
        b_toy_stats_2v[sample.key] = 0;
        t_toy_stats_1v->Branch(sample.name.c_str(), &(b_toy_stats_1v.find(sample.key)->second), TString::Format("%s/I", sample.name.c_str()));
        t_toy_stats_2v->Branch(sample.name.c_str(), &(b_toy_stats_2v.find(sample.key)->second), TString::Format("%s/I", sample.name.c_str()));
      };

      loop_over_samples(f);

      t_toy_stats_1v->Branch("sum_1v", &b_sum_1v, "sum_1v/I");
      t_toy_stats_2v->Branch("sum_2v", &b_sum_2v, "sum_2v/I");
      t_toy_stats_1v->Branch("sum_bkg_1v", &b_sum_bkg_1v, "sum_bkg_1v/I");
      t_toy_stats_2v->Branch("sum_bkg_2v", &b_sum_bkg_2v, "sum_bkg_2v/I");
      t_toy_stats_1v->Branch("sum_sig_1v", &b_sum_sig_1v, "sum_sig_1v/I");
      t_toy_stats_2v->Branch("sum_sig_2v", &b_sum_sig_2v, "sum_sig_2v/I");
    }
  }

  void ToyThrower::throw_toy() {
    toy_events_1v.clear();
    toy_events_2v.clear();
    toy_1v.clear();
    toy_2v.clear();

    printf("toy #%i:\n", ntoys);

    b_sum_bkg_1v = 0;
    b_sum_bkg_2v = 0;

    auto f = [this](const Sample& sample) {
      const double sc = sample.is_sig() ? signal_scale : scale;

      const int N1v = int(all_1v[sample.key].size());
      const double n1v_d = lambda_1v[sample.key] * sc;
      const int n1v_i = poisson_means ? rand->Poisson(n1v_d) : int(n1v_d) + 1;
      const int n1v = allow_cap ? std::min(n1v_i, N1v) : n1v_i;
      b_sum_1v += n1v;
      if (!sample.is_sig()) b_sum_bkg_1v += n1v;

      const int N2v = int(all_2v[sample.key].size());
      const double n2v_d = lambda_2v[sample.key] * sc;
      const int n2v_i = poisson_means ? rand->Poisson(n2v_d) : int(n2v_d) + 1;
      const int n2v = allow_cap ? std::min(n2v_i, N2v) : n2v_i;
      b_sum_2v += n2v;
      if (!sample.is_sig()) b_sum_bkg_2v += n2v;

      printf("  %-30s (%3i)  1v: lambda = %10.2f -> %10i events / %10i total\n", sample.name.c_str(), sample.key, n1v_d, n1v, N1v);
      printf("  %-30s        2v: lambda = %10.2f -> %10i events / %10i total\n", "",                              n2v_d, n2v, N2v);

      for (int i1v : jmt::knuth_choose_wo_replacement(rand, N1v, n1v)) {
        toy_events_1v.push_back(events_1v[sample.key][i1v]);
        toy_1v.push_back(all_1v[sample.key][i1v]);

        b_sample_usage_1v_key = sample.key;
        b_sample_usage_1v_ndx = i1v;
        t_sample_usage_1v->Fill();
      }

      for (int i2v : jmt::knuth_choose_wo_replacement(rand, N2v, n2v)) {
        toy_events_2v.push_back(events_2v[sample.key][i2v]);
        toy_2v.push_back(all_2v[sample.key][i2v]);

        b_sample_usage_2v_key = sample.key;
        b_sample_usage_2v_ndx = i2v;
        t_sample_usage_2v->Fill();
      }

      b_toy_stats_1v[sample.key] = n1v;
      b_toy_stats_2v[sample.key] = n2v;
    };

    loop_over_samples(f);

    b_sum_1v = toy_1v.size();
    b_sum_2v = toy_2v.size();
    b_sum_sig_1v = b_sum_1v - b_sum_bkg_1v;
    b_sum_sig_2v = b_sum_2v - b_sum_bkg_2v;

    printf("  1v sum: %i (%i bkg, %i sig)   2v sum: %i (%i bkg, %i sig)\n", b_sum_1v, b_sum_bkg_1v, b_sum_sig_1v, b_sum_2v, b_sum_bkg_2v, b_sum_sig_2v);

    t_toy_stats_1v->Fill();
    t_toy_stats_2v->Fill();

    ++ntoys;
  }      
}
