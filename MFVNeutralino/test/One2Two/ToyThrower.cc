#include "ToyThrower.h"
#include "TFile.h"
#include "TH1.h"
#include "TRandom3.h"
#include "TTree.h"
#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"
#include "JMTucker/MFVNeutralino/interface/AnalysisConstants.h"
#include "ROOTTools.h"
#include "Random.h"
#include "Templates.h"

namespace mfv {
  ToyThrower::ToyThrower(const std::string& name_, const std::string& path_, TFile* f, TRandom* r)
    : name (name_.size() ? " " + name_ : ""),
      uname(name_.size() ? "_" + name_ : ""),
      path(path_),

      env("mfvo2t_toythrower" + uname),
      from_histograms(env.get_bool("from_histograms", true)),
      from_histograms_fn(env.get_string("from_histograms_fn", "throwhists.root")),
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
      use_bkgsyst(env.get_bool("use_bkgsyst", false)),
      use_only_data_sample(env.get_bool("use_only_data_sample", false)),
      sample_only(env.get_int("sample_only", 0)),
      injected_signal(env.get_int("injected_signal", 0)),
      injected_signal_scale(env.get_double("injected_signal_scale", 1.)),
      template_signal(env.get_int("template_signal", -53)),

      ntoys(-1),

      fout(f),
      dout(0),
      rand(r),
      seed(r->GetSeed() - jmt::seed_base),

      h_bkg_dbv(0),
      h_bkg_dvv(0),
      h_bkg_dphi(0),
      h_injected_signal_dbv(0),
      h_injected_signal_dvv(0),
      h_injected_signal_dphi(0),
      h_injected_signal_norm(0),
      h_template_signal_dvv(0),

      h_dbv(0),
      h_dvv(0)
  {
    printf("ToyThrower%s config:\n", name.c_str());
    printf("(read ntuples from %s)\n", path.c_str());
    printf("seed: %i\n", seed);
    printf("from_histograms: %i  fn: %s\n", from_histograms, from_histograms_fn.c_str());
    printf("min_ntracks: %i\n", min_ntracks);
    printf("min_ntracks0: %i\n", min_ntracks0);
    printf("max_ntracks0: %i\n", max_ntracks0);
    printf("min_ntracks1: %i\n", min_ntracks1);
    printf("max_ntracks1: %i\n", max_ntracks1);
    printf("int_lumi: %f\n", int_lumi);
    printf("scale: %f 1v  %f 2v\n", scale_1v, scale_2v);
    printf("poisson_means: %i\n", poisson_means);
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

    const TString directory_name = TString::Format("ToyThrower%s", uname.c_str());
    dout = (TDirectory*)fout->Get(directory_name);
    if (!dout)
      dout = f->mkdir(directory_name);
    else
      jmt::vthrow("only one ToyThrower per file allowed");

    book_hists();
    if (from_histograms)
      read_histograms();
    else
      read_samples();

    book_and_fill_some_trees();
  }

  void ToyThrower::book_hists() {
    h_dbv = new TH1D("h_dbv", "", 995, 0.01, 2.);
    h_dvv = new TH1D("h_dvv", "", Template::nbins, Template::min_val, Template::max_val);
  }

  bool ToyThrower::sel_vertex(const VertexSimple& v) const {
    return v.ntracks >= min_ntracks;
  }

  void ToyThrower::read_histograms() {
    TFile* f = TFile::Open(from_histograms_fn.c_str());
    if (!f || !f->IsOpen())
      jmt::vthrow("could not read file %s", from_histograms_fn.c_str());

    auto checkedget = [&](const char* nm, const char* new_nm) {
      TH1D* h = (TH1D*)f->Get(nm);
      //printf("zzz %s -> %s  ptr %p\n", nm, new_nm, (void*)h);
      if (!h) jmt::vthrow("file %s didn't have hist %s", from_histograms_fn.c_str(), name);
      TH1D* hnew = (TH1D*)h->Clone(new_nm == 0 ? nm : new_nm);
      hnew->SetDirectory(dout);
      return hnew;
    };

    dout->cd();

    // background hists should be normalized to the expected yield
    h_bkg_dbv  = checkedget("h_bkg_dbv",  0);
    h_bkg_dvv  = checkedget("h_bkg_dvv",  0);
    h_bkg_dphi = checkedget("h_bkg_dphi", 0);

    using jmt::integral;

    lambda_1v[1] = integral(h_bkg_dbv);
    lambda_2v[1] = integral(h_bkg_dvv);
    if (fabs(lambda_2v[1] - integral(h_bkg_dphi)) > 1e-6)
      jmt::vthrow("2v bkg histograms have different normalizations dvv %f dphi %f", lambda_2v[1], integral(h_bkg_dphi));

    if (injected_signal != 0) {
      h_injected_signal_dbv  = checkedget(TString::Format("h_signal_%i_dbv",  injected_signal), "h_injected_signal_dbv");
      h_injected_signal_dvv  = checkedget(TString::Format("h_signal_%i_dvv",  injected_signal), "h_injected_signal_dvv");
      h_injected_signal_dphi = checkedget(TString::Format("h_signal_%i_dphi", injected_signal), "h_injected_signal_dphi");
      if (fabs(integral(h_injected_signal_dvv) - integral(h_injected_signal_dphi)) > 1e-6)
        jmt::vthrow("2v injected signal histograms have different normalizations dvv %f dphi %f", integral(h_injected_signal_dvv), integral(h_injected_signal_dphi));

      // signal hists have just the raw MC events to do the stats right -- normalization comes separately
      h_injected_signal_norm = checkedget(TString::Format("h_signal_%i_norm", injected_signal), "h_injected_signal_norm");

      lambda_1v[injected_signal] = h_injected_signal_norm->GetBinContent(1) * int_lumi;
      lambda_2v[injected_signal] = h_injected_signal_norm->GetBinContent(2) * int_lumi;
    }

    h_template_signal_dvv  = checkedget(TString::Format("h_signal_%i_dvv",  template_signal), "h_template_signal_dvv");

    printf("read_histograms: # 1v bkg = %f 2v = %f  sig eff injected 1v %f 2v %f template 2v %f\n",
           lambda_1v[1], lambda_2v[1], lambda_1v[injected_signal], lambda_2v[injected_signal], integral(h_template_signal_dvv));
  }

  void ToyThrower::read_sample(const Sample& sample) {
    printf("ToyThrower::read_sample: %s\n", sample.name.c_str());

    std::string fn  = sample2fn(sample);

    TFile* f = TFile::Open(fn.c_str());
    if (!f || !f->IsOpen())
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
        if ((!sample.is_sig() || sample.key == injected_signal || sample.key == template_signal) && (use_bkgsyst || sample.name != "bkgsyst"))
          fcn(sample);
    }
  }

  void ToyThrower::read_samples() {
    printf("ToyThrower(%s)::sample info (without any scaling):\n", name.c_str());
    loop_over_samples([this](const Sample& s) {
        read_sample(s);
        if (s.is_data())
          return;
        const double w = s.weight(int_lumi);
        const int N1v = int(all_1v[s.key].size());
        const int N2v = int(all_2v[s.key].size());
        const double W1v = lambda_1v[s.key] = w * N1v;
        const double W2v = lambda_2v[s.key] = w * N2v;
        printf("%-30s (%3i), weight %8.4g: %10i (%10.2f) 1v events,  %5i (%10.2f) 2v events\n", s.name.c_str(), s.key, w, N1v, W1v, N2v, W2v);
      });

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
    t_config->Branch("sample_only", const_cast<int*>(&sample_only), "sample_only/I");
    t_config->Branch("injected_signal", const_cast<int*>(&injected_signal), "injected_signal/I");
    t_config->Branch("injected_signal_scale", const_cast<double*>(&injected_signal_scale), "injected_signal_scale/D");
    t_config->Branch("template_signal", const_cast<int*>(&template_signal), "template_signal/I");
    t_config->Fill();

    t_toy_stats_1v = new TTree("t_toy_stats_1v", "");
    t_toy_stats_2v = new TTree("t_toy_stats_2v", "");

    if (from_histograms) {
      // JMTBAD anything?
    }
    else {
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

      loop_over_samples([this](const Sample& sample) {
          if (sample.is_data())
            return;
          b_toy_stats_1v[sample.key] = 0;
          b_toy_stats_2v[sample.key] = 0;
          t_toy_stats_1v->Branch(sample.name.c_str(), &(b_toy_stats_1v.find(sample.key)->second), TString::Format("%s/I", sample.name.c_str()));
          t_toy_stats_2v->Branch(sample.name.c_str(), &(b_toy_stats_2v.find(sample.key)->second), TString::Format("%s/I", sample.name.c_str()));
        });
    }

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

    b_sum_1v = 0;
    b_sum_2v = 0;
    b_sum_bkg_1v = 0;
    b_sum_bkg_2v = 0;

    if (from_histograms) {
      for (int bs : {1, injected_signal}) {
        if (bs == 0) // i.e. no injected_signal
          continue;
        const bool bkg = bs == 1;

        const double n1v_d = lambda_1v[bs] * (bkg ? scale_1v : injected_signal_scale);
        const int n1v = poisson_means ? rand->Poisson(n1v_d) : int(n1v_d) + 1;
        if (bkg) b_sum_bkg_1v += n1v;

        const double n2v_d = lambda_2v[bs] * (bkg ? scale_2v : injected_signal_scale);
        const int n2v = poisson_means ? rand->Poisson(n2v_d) : int(n2v_d) + 1;
        if (bkg) b_sum_bkg_2v += n2v;

        // do we need toy_events*? depends on the
        // templater. Run2Templater shouldn't. at least keep the vector
        // lengths in sync for now
        for (int i = 0; i < n1v; ++i) {
          toy_events_1v.push_back(EventSimple());
          toy_1v.push_back(VertexSimple((bkg ? h_bkg_dbv : h_injected_signal_dbv)->GetRandom(), rand->Uniform(-M_PI, M_PI)));
        }

        for (int i = 0; i < n2v; ++i) {
          toy_events_2v.push_back(EventSimple());
          const double phi0 = rand->Uniform(-M_PI, M_PI);
          const double dphi = (bkg ? h_bkg_dphi : h_injected_signal_dphi)->GetRandom();
          toy_2v.push_back(VertexPair(VertexSimple(0, phi0),
                                      VertexSimple((bkg ? h_bkg_dvv : h_injected_signal_dvv)->GetRandom(), phi0 + dphi)));
        }
      }
    }
    else {
      auto f = [this](const Sample& sample) {
        if (sample.is_data() || (sample.is_sig() && sample.key != injected_signal))
          return;

        const double sc1v = sample.is_sig() ? injected_signal_scale : scale_1v;
        const double sc2v = sample.is_sig() ? injected_signal_scale : scale_2v;

        const int N1v = int(all_1v[sample.key].size());
        const double n1v_d = lambda_1v[sample.key] * sc1v;
        const int n1v_i = poisson_means ? rand->Poisson(n1v_d) : int(n1v_d) + 1;
        const int n1v = allow_cap ? std::min(n1v_i, N1v) : n1v_i;
        if (!sample.is_sig()) b_sum_bkg_1v += n1v;

        const int N2v = int(all_2v[sample.key].size());
        const double n2v_d = lambda_2v[sample.key] * sc2v;
        const int n2v_i = poisson_means ? rand->Poisson(n2v_d) : int(n2v_d) + 1;
        const int n2v = allow_cap ? std::min(n2v_i, N2v) : n2v_i;
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
    if (from_histograms)
      return Template::finalize_binning(h_template_signal_dvv);
    else {
      std::map<int, VertexPairs>::const_iterator it = all_2v.find(template_signal);
      if (it == all_2v.end())
        jmt::vthrow("can't read signal sample to make template");
      return hist_with_template_binning(name_, title, it->second);
    }
  }
}
