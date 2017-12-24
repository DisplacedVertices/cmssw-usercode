#include <cassert>
#include <iostream>
#include "TH1.h"
#include "TH2.h"
#include "TFile.h"
#include "TTree.h"
#include "TVector2.h"
#include "TVector3.h"
#include "JMTucker/MFVNeutralino/interface/MovedTracksNtuple.h"
#include "BTagSFHelper.h"
#include "utils.h"

int main(int argc, char** argv) {
  if (argc < 5) {
    fprintf(stderr, "usage: hists.exe in.root out.root tree_path tau[int:microns] [btagsf_weights]-\n");
    return 1;
  }

  const char* in_fn  = argv[1];
  const char* out_fn = argv[2];
  const char* tree_path = argv[3];
  const int itau = atoi(argv[4]);

  const int itau_original = 10000; // JMTBAD if you change this in ntuple.py, change it here
  if (itau != itau_original)
    printf("reweighting tau distribution from 10000 um to %i um\n", itau);
  const double o_tau_from = 10000./itau_original;
  const double o_tau_to = 10000./itau;

  bool apply_weights = true;
  bool btagsf_weights = false;
  for (int argi = 5; argi < argc; ++argi) {
    if      (strcmp(argv[argi], "btagsf_weights") == 0) { btagsf_weights = true; printf("btagsf_weights -> true\n"); }
    else if (strcmp(argv[argi], "no_weights"    ) == 0) { apply_weights = false; printf("apply_weights -> false\n"); }
  }

  std::unique_ptr<BTagSFHelper> btagsfhelper;
  if (btagsf_weights) btagsfhelper.reset(new BTagSFHelper);

  root_setup();

  file_and_tree fat(in_fn, out_fn, tree_path);
  TTree* t = fat.t;
  mfv::MovedTracksNtuple& nt = fat.nt;
  t->GetEntry(0);

  const bool is_mc = nt.run == 1;
  TH1F* h_sums = is_mc ? ((TH1F*)fat.f->Get("mcStat/h_sums")) : 0;

  fat.f_out->mkdir("mfvWeight")->cd();
  fat.f->Get("mcStat/h_sums")->Clone("h_sums");
  fat.f_out->cd();

  TH1F* h_norm = new TH1F("h_norm", "", 1, 0, 1);
  if (is_mc)
    h_norm->Fill(0.5, h_sums->GetBinContent(1));

  TH1D* h_weight = new TH1D("h_weight", ";weight;events/0.01", 200, 0, 2);
  TH1D* h_btagsfweight = new TH1D("h_btagsfweight", ";weight;events/0.01", 200, 0, 2);
  TH1D* h_tau = new TH1D("h_tau", ";tau (cm);events/10 #mum", 10000, 0,10);
  TH1D* h_npu = new TH1D("h_npu", ";# PU;events/1", 100, 0, 100);

  const int num_numdens = 3;

  numdens nds[num_numdens] = {
    numdens("nocuts"),
    numdens("ntracks"),
    numdens("all")
  };

  enum { k_movedist2, k_movedist3, k_npv, k_pvx, k_pvy, k_pvz, k_pvrho, k_pvntracks, k_pvsumpt2, k_ht, k_ntracks, k_nseltracks, k_npreseljets, k_npreselbjets, k_jetsume, k_jetdrmax, k_jetdravg, k_jetsumntracks };
  for (numdens& nd : nds) {
    nd.book(k_movedist2, "movedist2", ";movement 2-dist;events/0.01 cm", 200, 0, 2);
    nd.book(k_movedist3, "movedist3", ";movement 3-dist;events/0.01 cm", 200, 0, 2);
    nd.book(k_npv, "npv", ";# PV;events/1", 100, 0, 100);
    nd.book(k_pvx, "pvx", ";PV x (cm);events/1.5 #mum", 200, -0.015, 0.015);
    nd.book(k_pvy, "pvy", ";PV y (cm);events/1.5 #mum", 200, -0.015, 0.015);
    nd.book(k_pvz, "pvz", ";PV z (cm);events/0.24 cm", 200, -24, 24);
    nd.book(k_pvrho, "pvrho", ";PV #rho (cm);events/1 #mum", 200, 0, 0.02);
    nd.book(k_pvntracks, "pvntracks", ";PV # tracks;events/2", 200, 0, 400);
    nd.book(k_pvsumpt2, "pvsumpt2", ";PV #Sigma p_{T}^{2} (GeV^{2});events/200 GeV^{2}", 200, 0, 40000);
    nd.book(k_ht, "ht", ";H_{T} (GeV);events/50 GeV", 50, 0, 2500);
    nd.book(k_ntracks, "ntracks", ";# tracks;events/10", 200, 0, 2000);
    nd.book(k_nseltracks, "nseltracks", ";# selected tracks;events/2", 200, 0, 400);
    nd.book(k_npreseljets, "npreseljets", ";# preselected jets;events/1", 20, 0, 20);
    nd.book(k_npreselbjets, "npreselbjets", ";# preselected b jets;events/1", 20, 0, 20);
    nd.book(k_jetsume, "jetsume", ";#Sigma jet energy (GeV);events/5 GeV", 200, 0, 1000);
    nd.book(k_jetdrmax, "jetdrmax", ";max jet #Delta R;events/0.1", 70, 0, 7);
    nd.book(k_jetdravg, "jetdravg", ";avg jet #Delta R;events/0.1", 70, 0, 7);
    nd.book(k_jetsumntracks, "jetsumntracks", ";#Sigma jet # tracks;events/5", 200, 0, 1000);
  }

  TH1D* h_vtxdbv[num_numdens] = {0};
  TH1D* h_vtxntracks[num_numdens] = {0};
  TH1D* h_vtxbs2derr[num_numdens] = {0};
  TH1D* h_vtxtkonlymass[num_numdens] = {0};
  TH1D* h_vtxanglemax[num_numdens] = {0};

  for (int i = 0; i < num_numdens; ++i) {
    h_vtxdbv[i] = new TH1D(TString::Format("h_%i_vtxdbv", i), ";d_{BV} of largest vertex (cm);events/50 #mum", 400, 0, 2);
    h_vtxntracks[i] = new TH1D(TString::Format("h_%i_vtxntracks", i), ";# tracks in largest vertex;events/1", 60, 0, 60);
    h_vtxbs2derr[i] = new TH1D(TString::Format("h_%i_vtxbs2derr", i), ";#sigma(d_{BV}) of largest vertex (cm);events/1 #mum", 500, 0, 0.05);
    h_vtxtkonlymass[i] = new TH1D(TString::Format("h_%i_vtxtkonlymass", i), ";track-only mass of largest vertex (GeV);events/1 GeV", 500, 0, 500);
    h_vtxanglemax[i] = new TH1D(TString::Format("h_%i_vtxanglemax", i), ";biggest angle between track in vertex and move vector;events/0.03", 100, 0, M_PI);
  }

  double den = 0;
  std::map<std::string, double> nums;

  const std::vector<std::string> extra_weights_hists = {
    //"nocuts_npv_den",
    //"nocuts_pvz_den",
    //"nocuts_pvx_den",
    //"nocuts_pvy_den",
    //"nocuts_ntracks_den",
    //"nocuts_npv_den_redo"
    //"nocuts_ht_den",
    //"nocuts_pvntracks_den",
  };
  TFile* extra_weights = extra_weights_hists.size() > 0 ? TFile::Open("reweight.root") : 0;
  const bool use_extra_weights = extra_weights != 0 && extra_weights->IsOpen();
  printf("using extra weights from reweight.root? %i\n", use_extra_weights);

  for (int j = 0, je = t->GetEntries(); j < je; ++j) {
    //if (j == 100000) break;
    if (t->LoadTree(j) < 0) break;
    if (t->GetEntry(j) <= 0) continue;
    if (j % 250000 == 0) {
      printf("\r%i/%i", j, je);
      fflush(stdout);
    }

    double w = 1;

    if (itau != 10000) {
      const double tau = nt.move_tau();
      const double tau_weight = o_tau_to/o_tau_from * exp((o_tau_from - o_tau_to) * tau);
      h_tau->Fill(tau, tau_weight);
      w *= tau_weight;
    }

    if (is_mc && apply_weights) {
      w *= nt.weight;

      if (btagsf_weights) {
        double p_mc = 1, p_data = 1;

        for (size_t i = 0, ie = nt.nalljets(); i < ie; ++i) {
          const double pt = (*nt.p_alljets_pt)[i];
          const double eta = (*nt.p_alljets_eta)[i];
          const bool is_tagged = (*nt.p_alljets_bdisc)[i] > 0.935; // what ever
          const int hf = (*nt.p_alljets_hadronflavor)[i];

          const double sf = btagsfhelper->scale_factor(BTagSFHelper::BH, BTagSFHelper::tight, hf, eta, pt).v;
          const double e = btagsfhelper->efficiency(hf, eta, pt).v;
          assert(e > 0 && e <= 1);

          if (is_tagged) {
            p_mc   *= e;
            p_data *= e*sf;
          }
          else {
            p_mc   *= 1-e;
            p_data *= 1-e*sf;
          }
        }

        const double btagsfw = p_data / p_mc;
        h_btagsfweight->Fill(btagsfw);
        w *= btagsfw;
      }

      if (use_extra_weights) {
        for (const auto& name : extra_weights_hists) {
          TH1D* hw = (TH1D*)extra_weights->Get(name.c_str());
          assert(hw);
          const double v =
            name == "nocuts_npv_den" ? nt.npv :
            name == "nocuts_pvz_den" ? nt.pvz :
            name == "nocuts_pvx_den" ? nt.pvx :
            name == "nocuts_pvy_den" ? nt.pvy :
            name == "nocuts_ntracks_den" ? nt.ntracks :
            name == "nocuts_npv_den_redo" ? nt.npv :
            name == "nocuts_ht_den" ? nt.jetht :
            name == "nocuts_pvntracks_den" ? nt.pvntracks :
            -1e99;
          assert(v > -1e98);
          const int bin = hw->FindBin(v);
          if (bin >= 1 && bin <= hw->GetNbinsX())  
            w *= hw->GetBinContent(bin);
        }
      }
    }

    const TVector3 move_vector = nt.move_vector();
    const double movedist2 = move_vector.Perp();
    const double movedist3 = move_vector.Mag();

    const size_t n_raw_vtx = nt.p_vtxs_x->size();

    const bool pass_800 = bool(nt.pass_hlt & 0x2);
    const bool pass_900_450_AK450 = bool(nt.pass_hlt & 0x1C);
    const bool is_H = nt.run > 281000;
    const bool pass_trig = pass_800 || (is_H && pass_900_450_AK450);

    double jet_sume = 0;
    double jet_drmax = 0;
    double jet_dravg = 0;
    double jet_sumntracks = 0;
    const size_t n_jets = nt.p_jets_pt->size();
    for (size_t ijet = 0; ijet < n_jets; ++ijet) {
      jet_sume += nt.p_jets_energy->at(ijet);
      jet_sumntracks += nt.p_jets_ntracks->at(ijet);

      for (size_t jjet = ijet+1; jjet < n_jets; ++jjet) {
        const double dr = mag(double(nt.p_jets_eta->at(ijet) - nt.p_jets_eta->at(jjet)),
                              TVector2::Phi_mpi_pi(nt.p_jets_phi->at(ijet) - nt.p_jets_phi->at(jjet)));
        jet_dravg += dr;
        if (dr > jet_drmax)
          jet_drmax = dr;
      }
    }
    jet_dravg /= n_jets * (n_jets - 1) / 2.;

    if (nt.jetht < 1000 ||
        nt.nalljets() < 4 ||
	!pass_trig || 
        movedist2 < 0.03 ||
        movedist2 > 2.0) {
      continue;
    }

    h_weight->Fill(w);
    h_npu->Fill(nt.npu, w);

    auto Fill = [&w](TH1D* h, double v) { h->Fill(v, w); };

    for (numdens& nd : nds) {
      Fill(nd(k_movedist2)    .den, movedist2);
      Fill(nd(k_movedist3)    .den, movedist3);
      Fill(nd(k_npv)          .den, nt.npv);
      Fill(nd(k_pvx)          .den, nt.pvx);
      Fill(nd(k_pvy)          .den, nt.pvy);
      Fill(nd(k_pvz)          .den, nt.pvz);
      Fill(nd(k_pvrho)        .den, mag(nt.pvx, nt.pvy));
      Fill(nd(k_pvntracks)    .den, nt.pvntracks);
      Fill(nd(k_pvsumpt2)     .den, nt.pvsumpt2);
      Fill(nd(k_ht)           .den, nt.jetht);
      Fill(nd(k_ntracks)      .den, nt.ntracks);
      Fill(nd(k_nseltracks)   .den, nt.nseltracks);
      Fill(nd(k_npreseljets)  .den, nt.npreseljets);
      Fill(nd(k_npreselbjets) .den, nt.npreselbjets);
      Fill(nd(k_jetsume)      .den, jet_sume);
      Fill(nd(k_jetdrmax)     .den, jet_drmax);
      Fill(nd(k_jetdravg)     .den, jet_dravg);
      Fill(nd(k_jetsumntracks).den, jet_sumntracks);
    }

    den += w;

    int n_pass_nocuts = 0;
    int n_pass_ntracks = 0;
    int n_pass_all = 0;

    std::vector<int> first_vtx_to_pass(num_numdens, -1);
    auto set_it_if_first = [](int& to_set, int to_set_to) { if (to_set == -1) to_set = to_set_to; };

    for (size_t ivtx = 0; ivtx < n_raw_vtx; ++ivtx) {
      const double dist2move = mag(nt.move_x - nt.p_vtxs_x->at(ivtx),
                                   nt.move_y - nt.p_vtxs_y->at(ivtx),
                                   nt.move_z - nt.p_vtxs_z->at(ivtx));
      if (dist2move > 0.0084)
        continue;

      const bool pass_ntracks = nt.p_vtxs_ntracks->at(ivtx) >= 5;
      const bool pass_bs2derr = nt.p_vtxs_bs2derr->at(ivtx) < 0.0025;

      if (1)                            { set_it_if_first(first_vtx_to_pass[0], ivtx); ++n_pass_nocuts;  }
      if (pass_ntracks)                 { set_it_if_first(first_vtx_to_pass[1], ivtx); ++n_pass_ntracks; }
      if (pass_ntracks && pass_bs2derr) { set_it_if_first(first_vtx_to_pass[2], ivtx); ++n_pass_all;     }
    }

    for (int i = 0; i < num_numdens; ++i) {
      int ivtx = first_vtx_to_pass[i];
      if (ivtx != -1) {
        h_vtxdbv[i]->Fill(mag(nt.p_vtxs_x->at(ivtx),
                              nt.p_vtxs_y->at(ivtx)));
        h_vtxntracks[i]->Fill(nt.p_vtxs_ntracks->at(ivtx), w);
        h_vtxbs2derr[i]->Fill(nt.p_vtxs_bs2derr->at(ivtx), w);
        h_vtxanglemax[i]->Fill(nt.p_vtxs_anglemax->at(ivtx), w);
        h_vtxtkonlymass[i]->Fill(nt.p_vtxs_tkonlymass->at(ivtx), w);
      }
    }

    if (n_pass_nocuts)  nums["nocuts"]  += w;
    if (n_pass_ntracks) nums["ntracks"] += w;
    if (n_pass_all)     nums["all"]     += w;

    const int passes[num_numdens] = {
      n_pass_nocuts,
      n_pass_ntracks,
      n_pass_all
    };

    for (int i = 0; i < num_numdens; ++i) {
      if (passes[i]) {
        numdens& nd = nds[i];
        Fill(nd(k_movedist2)    .num, movedist2);
        Fill(nd(k_movedist3)    .num, movedist3);
        Fill(nd(k_npv)          .num, nt.npv);
        Fill(nd(k_pvx)          .num, nt.pvx);
        Fill(nd(k_pvy)          .num, nt.pvy);
        Fill(nd(k_pvz)          .num, nt.pvz);
        Fill(nd(k_pvrho)        .num, mag(nt.pvx, nt.pvy));
        Fill(nd(k_pvntracks)    .num, nt.pvntracks);
        Fill(nd(k_pvsumpt2)     .num, nt.pvsumpt2);
        Fill(nd(k_ht)           .num, nt.jetht);
        Fill(nd(k_ntracks)      .num, nt.ntracks);
        Fill(nd(k_nseltracks)   .num, nt.nseltracks);
        Fill(nd(k_npreseljets)  .num, nt.npreseljets);
        Fill(nd(k_npreselbjets) .num, nt.npreselbjets);
        Fill(nd(k_jetsume)      .num, jet_sume);
        Fill(nd(k_jetdrmax)     .num, jet_drmax);
        Fill(nd(k_jetdravg)     .num, jet_dravg);
        Fill(nd(k_jetsumntracks).num, jet_sumntracks);
      }
    }
  }

  printf("\r                                \n");
  printf("%f events in denominator\n", den);
  printf("%30s  %12s  %12s  %10s [%10s, %10s] +%10s -%10s\n", "name", "num", "den", "eff", "lo", "hi", "+", "-");
  for (const auto& p : nums) {
    const interval i = clopper_pearson_binom(p.second, den);
    printf("%30s  %12f  %12f  %10f [%10f, %10f] +%10f -%10f\n", p.first.c_str(), p.second, den, i.value, i.lower, i.upper, i.upper - i.value, i.value - i.lower);
  }
}
