#include "ToyThrower.h"
#include "TFile.h"
#include "TH1.h"
#include "TRandom3.h"
#include "TTree.h"
#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"
#include "JMTucker/MFVNeutralino/interface/AnalysisConstants.h"
#include "Random.h"
#include "Templates.h"

namespace mfv {
  ToyThrower::ToyThrower(const std::string& name_, const std::string& path_, TFile* f, TRandom* r)
    : name (name_.size() ? " " + name_ : ""),
      uname(name_.size() ? "_" + name_ : ""),
      path(path_),

      env("mfvo2t_toythrower" + uname),
      min_ntracks(env.get_int("min_ntracks", 5)),
      min_ntracks0(env.get_int("min_ntracks0", 0)),
      max_ntracks0(env.get_int("max_ntracks0", 1000000)),
      min_ntracks1(env.get_int("min_ntracks1", 0)),
      max_ntracks1(env.get_int("max_ntracks1", 1000000)),
      int_lumi(env.get_double("int_lumi", mfv::AnalysisConstants::int_lumi_2016 * mfv::AnalysisConstants::scale_factor_2016)),
      scale_1v(env.get_double("scale_1v", 1.)),
      scale_2v(env.get_double("scale_2v", 1.)),
      allow_cap(env.get_bool("allow_cap", false)),
      poisson_means(env.get_bool("poisson_means", true)),
      throw_2v_from_histogram(env.get_bool("throw_2v_from_histogram", false)),
      n2v_from_histogram(env.get_int("n2v_from_histogram", 0)),
      use_qcd700(env.get_bool("use_qcd700", false)),
      use_bkgsyst(env.get_bool("use_bkgsyst", false)),
      use_only_data_sample(env.get_bool("use_only_data_sample", false)),
      sample_only(env.get_int("sample_only", 0)),
      injected_signal(env.get_int("injected_signal", 0)),
      injected_signal_scale(env.get_double("injected_signal_scale", 1.)),
      template_signal(env.get_int("template_signal", -10)),

      ntoys(-1),

      fout(f),
      dout(0),
      rand(r),
      seed(r->GetSeed() - jmt::seed_base)
  {
    printf("ToyThrower%s config:\n", name.c_str());
    printf("(read ntuples from %s)\n", path.c_str());
    printf("seed: %i\n", seed);
    printf("min_ntracks: %i\n", min_ntracks);
    printf("min_ntracks0: %i\n", min_ntracks0);
    printf("max_ntracks0: %i\n", max_ntracks0);
    printf("min_ntracks1: %i\n", min_ntracks1);
    printf("max_ntracks1: %i\n", max_ntracks1);
    printf("int_lumi: %f\n", int_lumi);
    printf("scale: %f 1v  %f 2v\n", scale_1v, scale_2v);
    printf("poisson_means: %i\n", poisson_means);
    printf("throw_2v_from_histogram: %i\n", throw_2v_from_histogram);
    printf("n2v_from_histogram: %i\n", n2v_from_histogram);
    printf("use_qcd700: %i\n", use_qcd700);
    printf("use_only_data_sample: %i\n", use_only_data_sample);
    printf("sample_only: %i (%s)\n", sample_only, samples.get(sample_only).name.c_str());
    printf("injected_signal: %i (%s)\n", injected_signal, samples.get(injected_signal).name.c_str());
    printf("injected_signal_scale: %g\n", injected_signal_scale);
    printf("template_signal: %i (%s)\n", template_signal, samples.get(template_signal).name.c_str());
    fflush(stdout);

    toy_dataset.toy = ntoys;
    toy_dataset.events_1v = &toy_events_1v;
    toy_dataset.events_2v = &toy_events_2v;
    toy_dataset.one_vertices = &toy_1v;
    toy_dataset.two_vertices = &toy_2v;

    book_hists();
    read_samples();

    const TString directory_name = TString::Format("ToyThrower%s", uname.c_str());
    dout = (TDirectory*)fout->Get(directory_name);
    if (!dout)
      dout = f->mkdir(directory_name);
    else
      jmt::vthrow("only one ToyThrower per file allowed");

    book_and_fill_some_trees();
  }

  void ToyThrower::book_hists() {
    h_dbv = new TH1D("h_dbv", "", 995, 0.01, 2.);
    h_dvv = new TH1D("h_dvv", "", Template::nbins, Template::min_val, Template::max_val);
  }

  bool ToyThrower::sel_vertex(const VertexSimple& v) const {
    return v.ntracks >= min_ntracks;
  }

  void ToyThrower::read_sample(const Sample& sample) {
    printf("ToyThrower::read_sample: %s\n", sample.name.c_str());

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

      //if (sample.is_data() && j == 20000)
      //  break;

      EventSimple e(nt);
      e.sample = sample.key;
      e.nvtx_sel = 0;

      const double w = sample.weight(int_lumi);
      if (nt.nvtx == 1) {
        VertexSimple v0(nt, 0, sample.is_sig());
        if (sel_vertex(v0)) {
          all_1v[sample.key].push_back(v0);
          e.nvtx_sel = 1;
          if (!sample.is_sig()) h_dbv->Fill(v0.d2d(), w);
        }
      }
      else if (nt.nvtx == 2) {
        VertexSimple v0(nt, 0, sample.is_sig());
        VertexSimple v1(nt, 1, sample.is_sig());
        const bool sel0 = sel_vertex(v0);
        const bool sel1 = sel_vertex(v1);
        if (sel0 && sel1) {
          if (v0.ntracks >= min_ntracks0 && v0.ntracks <= max_ntracks0 && v1.ntracks >= min_ntracks1 && v1.ntracks <= max_ntracks1) {
            all_2v[sample.key].push_back(VertexPair(v0, v1));
            e.nvtx_sel = 2;
            if (!sample.is_sig()) h_dvv->Fill(v0.d2d(v1), w);
          }
        }
        else if (sel0 || sel1) {
          all_1v[sample.key].push_back(sel0 ? v0 : v1);
          e.nvtx_sel = 1;
          if (!sample.is_sig()) h_dbv->Fill(sel0 ? v0.d2d() : v1.d2d(), w);
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
    if (use_only_data_sample) {
      fcn(samples.get(0));
    }
    else if (sample_only) {
      fcn(samples.get(sample_only));
      if (injected_signal != 0)
        fcn(samples.get(injected_signal));
      if (template_signal != 0 && template_signal != injected_signal)
        fcn(samples.get(template_signal));
    }
    else {
      for (const Sample& sample : samples.samples)
        //if (sample.name != "qcdht0100" && sample.name != "qcdht0250" && 
        if ((!sample.is_sig() || sample.key == injected_signal || sample.key == template_signal) && (use_qcd700 || sample.name != "qcdht0700") && (use_bkgsyst || sample.name != "bkgsyst"))
          fcn(sample);
    }
  }

  void ToyThrower::update_poisson_means() {
    printf("ToyThrower(%s)::sample info (without any scaling):\n", name.c_str());
    auto f = [this](const Sample& sample) {
      if (sample.is_data())
        return;
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

    data.toy = -1;
    data.events_1v = &events_1v[0];
    data.events_2v = &events_2v[0];
    data.one_vertices = &all_1v[0];
    data.two_vertices = &all_2v[0];
  }

  void ToyThrower::book_and_fill_some_trees() {
    dout->cd();

    TTree* t_config = new TTree("t_config", "");
    t_config->SetAlias("name", name.c_str());
    t_config->SetAlias("path", path.c_str());
    t_config->Branch("seed", const_cast<int*>(&seed), "seed/I");
    t_config->Branch("min_ntracks", const_cast<int*>(&min_ntracks), "min_ntracks/I");
    t_config->Branch("int_lumi", const_cast<double*>(&int_lumi), "int_lumi/D");
    t_config->Branch("scale_1v", const_cast<double*>(&scale_1v), "scale_1v/D");
    t_config->Branch("scale_2v", const_cast<double*>(&scale_2v), "scale_2v/D");
    t_config->Branch("poisson_means", const_cast<bool*>(&poisson_means), "poisson_means/O");
    t_config->Branch("use_qcd700", const_cast<bool*>(&use_qcd700), "use_qcd700/O");
    t_config->Branch("sample_only", const_cast<int*>(&sample_only), "sample_only/I");
    t_config->Branch("injected_signal", const_cast<int*>(&injected_signal), "injected_signal/I");
    t_config->Branch("injected_signal_scale", const_cast<double*>(&injected_signal_scale), "injected_signal_scale/D");
    t_config->Fill();

    TTree* t_sample_info = new TTree("t_sample_info", "");
    int b_sample_info_key;
    double b_sample_info_weight;
    int b_sample_info_N1v;
    int b_sample_info_N2v;
    t_sample_info->Branch("key", &b_sample_info_key, "key/I");
    t_sample_info->Branch("weight", &b_sample_info_weight, "weight/D");
    t_sample_info->Branch("N1v", &b_sample_info_N1v, "N1v/I");
    t_sample_info->Branch("N2v", &b_sample_info_N2v, "N2v/I");
    loop_over_samples([&](const Sample& sample) {
                        if (sample.is_data())
                          return;
                        t_sample_info->SetAlias(sample.name.c_str(), TString::Format("%i", sample.key));
                        b_sample_info_key = sample.key;
                        b_sample_info_weight = sample.weight(int_lumi);
                        b_sample_info_N1v = int(all_1v[sample.key].size());
                        b_sample_info_N2v = int(all_2v[sample.key].size());
                        t_sample_info->Fill();
                      });


    t_sample_usage_1v = new TTree("t_sample_usage_1v", "");
    t_sample_usage_1v->Branch("key", &b_sample_usage_1v_key, "key/I");
    t_sample_usage_1v->Branch("ndx", &b_sample_usage_1v_ndx, "ndx/I");

    t_sample_usage_2v = new TTree("t_sample_usage_2v", "");
    t_sample_usage_2v->Branch("key", &b_sample_usage_2v_key, "key/I");
    t_sample_usage_2v->Branch("ndx", &b_sample_usage_2v_ndx, "ndx/I");


    t_toy_stats_1v = new TTree("t_toy_stats_1v", "");
    t_toy_stats_2v = new TTree("t_toy_stats_2v", "");

    loop_over_samples([this](const Sample& sample) {
                        if (sample.is_data())
                          return;
                        b_toy_stats_1v[sample.key] = 0;
                        b_toy_stats_2v[sample.key] = 0;
                        t_toy_stats_1v->Branch(sample.name.c_str(), &(b_toy_stats_1v.find(sample.key)->second), TString::Format("%s/I", sample.name.c_str()));
                        t_toy_stats_2v->Branch(sample.name.c_str(), &(b_toy_stats_2v.find(sample.key)->second), TString::Format("%s/I", sample.name.c_str()));
                      });

    t_toy_stats_1v->Branch("sum_1v", &b_sum_1v, "sum_1v/I");
    t_toy_stats_2v->Branch("sum_2v", &b_sum_2v, "sum_2v/I");
    t_toy_stats_1v->Branch("sum_bkg_1v", &b_sum_bkg_1v, "sum_bkg_1v/I");
    t_toy_stats_2v->Branch("sum_bkg_2v", &b_sum_bkg_2v, "sum_bkg_2v/I");
    t_toy_stats_1v->Branch("sum_sig_1v", &b_sum_sig_1v, "sum_sig_1v/I");
    t_toy_stats_2v->Branch("sum_sig_2v", &b_sum_sig_2v, "sum_sig_2v/I");
  }

  void ToyThrower::throw_toy() {
    toy_dataset.toy = ++ntoys;
    printf("ToyThrower%s throwing toy #%i:\n", name.c_str(), ntoys);

    toy_events_1v.clear();
    toy_events_2v.clear();
    toy_1v.clear();
    toy_2v.clear();

    b_sum_bkg_1v = 0;
    b_sum_bkg_2v = 0;

    auto f = [this](const Sample& sample) {
      if (sample.is_data() || (sample.is_sig() && sample.key != injected_signal))
        return;

      const double sc1v = sample.is_sig() ? injected_signal_scale : scale_1v;
      const double sc2v = sample.is_sig() ? injected_signal_scale : scale_2v;

      const int N1v = int(all_1v[sample.key].size());
      const double n1v_d = lambda_1v[sample.key] * sc1v;
      const int n1v_i = poisson_means ? rand->Poisson(n1v_d) : int(n1v_d) + 1;
      const int n1v = allow_cap ? std::min(n1v_i, N1v) : n1v_i;
      b_sum_1v += n1v;
      if (!sample.is_sig()) b_sum_bkg_1v += n1v;

      const int N2v = int(all_2v[sample.key].size());
      const double n2v_d = lambda_2v[sample.key] * sc2v;
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

    if (throw_2v_from_histogram) {
      b_sum_bkg_2v = n2v_from_histogram > 0 ? n2v_from_histogram : b_sum_bkg_2v;
      toy_2v.clear();
      for (int i = 0; i < b_sum_bkg_2v; ++i) {
        double dvv = 0;
        const double r = rand->Rndm();
        if      (r < 0.77)      dvv = 0.02;
        else if (r < 0.77+0.20) dvv = 0.055;
        else                    dvv = 0.1;
        toy_2v.push_back(VertexPair(VertexSimple(0, 0), VertexSimple(dvv, 0)));
      }
    }

    b_sum_1v = toy_1v.size();
    b_sum_2v = toy_2v.size();
    b_sum_sig_1v = b_sum_1v - b_sum_bkg_1v;
    b_sum_sig_2v = b_sum_2v - b_sum_bkg_2v;

    printf("  1v sum: %i (%i bkg, %i sig)   2v sum: %i (%i bkg, %i sig)\n", b_sum_1v, b_sum_bkg_1v, b_sum_sig_1v, b_sum_2v, b_sum_bkg_2v, b_sum_sig_2v);

    t_toy_stats_1v->Fill();
    t_toy_stats_2v->Fill();
  }

  TH1D* ToyThrower::hist_with_template_binning(const char* name_, const char* title, const VertexPairs& v2v) const {
    TH1D* h_temp = Template::hist_with_binning(name_, title);
    h_temp->SetDirectory(0);
    for (const VertexPair& p : v2v)
      h_temp->Fill(p.d2d());
    TH1D* h = Template::finalize_binning(h_temp);
    h->SetDirectory(0);
    delete h_temp;
    return h;
  }

  TH1D* ToyThrower::signal_template(const char* name_, const char* title) const {
    std::map<int, VertexPairs>::const_iterator it = all_2v.find(template_signal);
    if (it == all_2v.end())
      jmt::vthrow("can't read signal sample to make template");
    return hist_with_template_binning(name_, title, it->second);
  }
}
