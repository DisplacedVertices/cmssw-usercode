#include "TH1.h"
#include "TFile.h"
#include "TTree.h"
#include "TVector2.h"
#include "JMTucker/MFVNeutralino/interface/MovedTracksNtuple.h"
#include "utils.h"
#include <iostream>

// #error need to support picking hlt bit and final ht cut

int main(int argc, char** argv) {
  if (argc < 5) {
    fprintf(stderr, "usage: hists.exe in.root out.root njets_req nbjets_req\n");
    return 1;
  }

  const char* in_fn  = argv[1];
  const char* out_fn = argv[2];
  const int njets_req = atoi(argv[3]);
  const int nbjets_req = atoi(argv[4]);
  const bool apply_weight = true;

  root_setup();

  file_and_tree fat(in_fn, out_fn);
  TTree* t = fat.t;
  mfv::MovedTracksNtuple& nt = fat.nt;

  TH1F* h_sums = ((TH1F*)fat.f->Get("mcStat/h_sums"));
  bool is_mc = h_sums != 0;

  fat.f_out->mkdir("mfvWeight")->cd();
  fat.f->Get("mcStat/h_sums")->Clone("h_sums");
  fat.f_out->cd();

  TH1F* h_norm = new TH1F("h_norm", "", 1, 0, 1);
  if (is_mc)
    h_norm->Fill(0.5, h_sums->GetBinContent(1));

  TH1D* h_weight = new TH1D("h_weight", ";weight;events/0.01", 200, 0, 2);
  TH1D* h_npu = new TH1D("h_npu", ";# PU;events/1", 100, 0, 100);

  const int num_numdens = 3;

  TH1D* h_vtxntracks     [num_numdens] = {0};
  TH1D* h_vtxntracksptgt3[num_numdens] = {0};
  TH1D* h_vtxdrmin       [num_numdens] = {0};
  TH1D* h_vtxdrmax       [num_numdens] = {0};
  TH1D* h_vtxbs2derr     [num_numdens] = {0};

  for (int i = 0; i < num_numdens; ++i) {
    h_vtxntracks     [i] = new TH1D(TString::Format("h_%i_vtxntracks",      i), ";# tracks in largest vertex;events/1", 40, 0, 40);
    h_vtxntracksptgt3[i] = new TH1D(TString::Format("h_%i_vtxntracksptgt3", i), ";# tracks w/ p_{T} > 3 GeV in largest vertex;events/1", 40, 0, 40);
    h_vtxdrmin       [i] = new TH1D(TString::Format("h_%i_vtxdrmin",        i), ";min #Delta R_{ij} of tracks in largest vertex;events/0.05", 10, 0, 0.5);
    h_vtxdrmax       [i] = new TH1D(TString::Format("h_%i_vtxdrmax",        i), ";max #Delta R_{ij} of tracks in largest vertex;events/0.5", 14, 0, 7);
    h_vtxbs2derr     [i] = new TH1D(TString::Format("h_%i_vtxbs2derr",      i), ";#sigma(d_{BV}) of largest vertex (cm);events/2 #mum", 50, 0, 0.01);
  }

  numdens nds[num_numdens] = {
    numdens("nocuts"),
    numdens("ntracks"),
    numdens("all")
  };

  for (numdens& nd : nds) {
    nd.book("movedist2", ";movement 2-dist;events/0.01 cm", 200, 0, 2);
    nd.book("movedist3", ";movement 3-dist;events/0.01 cm", 200, 0, 2);
    nd.book("npv", ";# PV;events/1", 100, 0, 100);
    nd.book("pvx", ";PV x (cm);events/1.5 #mum", 200, -0.015, 0.015);
    nd.book("pvy", ";PV y (cm);events/1.5 #mum", 200, -0.015, 0.015);
    nd.book("pvz", ";PV z (cm);events/0.24 cm", 200, -24, 24);
    nd.book("pvrho", ";PV #rho (cm);events/1 #mum", 200, 0, 0.02);
    nd.book("pvntracks", ";PV # tracks;events/2", 200, 0, 400);
    nd.book("pvsumpt2", ";PV #Sigma p_{T}^{2} (GeV^{2});events/200 GeV^{2}", 200, 0, 40000);
    nd.book("ht", ";#Sigma H_{T} (GeV);events/50 GeV", 50, 0, 2500);
    nd.book("met", ";MET (GeV);events/20 GeV", 25, 0, 500);
    nd.book("nlep", ";# leptons;events", 5, 0, 5);
    nd.book("ntracks", ";# tracks;events/10", 200, 0, 2000);
    nd.book("nseltracks", ";# selected tracks;events/2", 200, 0, 400);
    nd.book("npreseljets", ";# preselected jets;events/1", 20, 0, 20);
    nd.book("npreselbjets", ";# preselected b jets;events/1", 20, 0, 20);
    nd.book("jetsume", ";#Sigma jet energy (GeV);events/5 GeV", 200, 0, 1000);
    nd.book("jetdrmax", ";max jet #Delta R;events/0.1", 70, 0, 7);
    nd.book("jetdravg", ";avg jet #Delta R;events/0.1", 70, 0, 7);
    nd.book("jetsumntracks", ";#Sigma jet # tracks;events/5", 200, 0, 1000);
  }

  double den = 0;
  std::map<std::string, double> nums;

  //TFile* f_pvzweights = TFile::Open("../pvzweights.root");
  //TH1D* h_pvzweights = (TH1D*)f_pvzweights->Get("rat");

  for (int j = 0, je = t->GetEntries(); j < je; ++j) {
    //if (j == 100000) break;
    if (t->LoadTree(j) < 0) break;
    if (t->GetEntry(j) <= 0) continue;
    if (j % 250000 == 0) {
      printf("\r%i/%i", j, je);
      fflush(stdout);
    }

    const double w = apply_weight ? nt.weight : 1.;
    //if (0) {
    //  int bin = h_pvzweights->FindBin(nt.pvz);
    //  if (bin >= 1 && bin <= h_pvzweights->GetNbinsX())
    //    w *= h_pvzweights->GetBinContent(bin);
    //}

    const double movedist2 = mag(nt.move_x - nt.pvx,
                                 nt.move_y - nt.pvy);
    const double movedist3 = mag(nt.move_x - nt.pvx,
                                 nt.move_y - nt.pvy,
                                 nt.move_z - nt.pvz);

    const size_t n_raw_vtx = nt.p_vtxs_x->size();

    const bool pass_800 = bool(nt.pass_hlt & 0x2);
    const bool pass_900_450_AK450 = bool(nt.pass_hlt & 0x1C);
    const bool H_data = nt.run > 281000;

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
    if (nt.npreseljets < njets_req || 
        nt.npreselbjets < nbjets_req ||
        nt.jetht < 1000 ||
        movedist2 < 0.03 ||
	!(pass_800 || (H_data && pass_900_450_AK450)) ||
        movedist2 > 2.5) {
      continue;
    }

    h_weight->Fill(w);
    h_npu->Fill(nt.npu, w);

    auto Fill = [&w](TH1D* h, double v) { h->Fill(v, w); };

    for (numdens& nd : nds) {
      Fill(nd("movedist2")    .den, movedist2);
      Fill(nd("movedist3")    .den, movedist3);
      Fill(nd("npv")          .den, nt.npv);
      Fill(nd("pvx")          .den, nt.pvx);
      Fill(nd("pvy")          .den, nt.pvy);
      Fill(nd("pvz")          .den, nt.pvz);
      Fill(nd("pvrho")        .den, mag(nt.pvx, nt.pvy));
      Fill(nd("pvntracks")    .den, nt.pvntracks);
      Fill(nd("pvsumpt2")     .den, nt.pvsumpt2);
      Fill(nd("ht")           .den, nt.jetht);
      Fill(nd("met")          .den, nt.met);
      Fill(nd("nlep")         .den, nt.nlep);
      Fill(nd("ntracks")      .den, nt.ntracks);
      Fill(nd("nseltracks")   .den, nt.nseltracks);
      Fill(nd("npreseljets")  .den, nt.npreseljets);
      Fill(nd("npreselbjets") .den, nt.npreselbjets);
      Fill(nd("jetsume")      .den, jet_sume);
      Fill(nd("jetdrmax")     .den, jet_drmax);
      Fill(nd("jetdravg")     .den, jet_dravg);
      Fill(nd("jetsumntracks").den, jet_sumntracks);
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
      if (dist2move > 0.005)
        continue;

      const bool pass_ntracks      = nt.p_vtxs_ntracks     ->at(ivtx) >= 5;
      const bool pass_bs2derr      = nt.p_vtxs_bs2derr     ->at(ivtx) < 0.0025;

      if (1)                                           { set_it_if_first(first_vtx_to_pass[0], ivtx); ++n_pass_nocuts;        }
      if (pass_ntracks)                                { set_it_if_first(first_vtx_to_pass[1], ivtx); ++n_pass_ntracks;       }
      if (pass_ntracks && pass_bs2derr)  { set_it_if_first(first_vtx_to_pass[2], ivtx); ++n_pass_all;           }
    }

    for (int i = 0; i < num_numdens; ++i) {
      int ivtx = first_vtx_to_pass[i];
      if (ivtx != -1) {
        h_vtxntracks      [i]->Fill(nt.p_vtxs_ntracks     ->at(ivtx));
        h_vtxntracksptgt3 [i]->Fill(nt.p_vtxs_ntracksptgt3->at(ivtx));
        h_vtxdrmin        [i]->Fill(nt.p_vtxs_drmin       ->at(ivtx));
        h_vtxdrmax        [i]->Fill(nt.p_vtxs_drmax       ->at(ivtx));
        h_vtxbs2derr      [i]->Fill(nt.p_vtxs_bs2derr     ->at(ivtx));
      }
    }

    if (n_pass_nocuts)             nums["nocuts"]             += w;
    if (n_pass_ntracks)            nums["ntracks"]            += w;
    if (n_pass_all)                nums["all"]                += w;

    const int passes[num_numdens] = {
      n_pass_nocuts,
      n_pass_ntracks,
      n_pass_all
    };

    for (int i = 0; i < num_numdens; ++i) {
      if (passes[i]) {
        numdens& nd = nds[i];
        Fill(nd("movedist2")    .num, movedist2);
        Fill(nd("movedist3")    .num, movedist3);
        Fill(nd("npv")          .num, nt.npv);
        Fill(nd("pvx")          .num, nt.pvx);
        Fill(nd("pvy")          .num, nt.pvy);
        Fill(nd("pvz")          .num, nt.pvz);
        Fill(nd("pvrho")        .num, mag(nt.pvx, nt.pvy));
        Fill(nd("pvntracks")    .num, nt.pvntracks);
        Fill(nd("pvsumpt2")     .num, nt.pvsumpt2);
        Fill(nd("ht")           .num, nt.jetht);
        Fill(nd("met")          .num, nt.met);
        Fill(nd("nlep")         .num, nt.nlep);
        Fill(nd("ntracks")      .num, nt.ntracks);
        Fill(nd("nseltracks")   .num, nt.nseltracks);
        Fill(nd("npreseljets")  .num, nt.npreseljets);
        Fill(nd("npreselbjets") .num, nt.npreselbjets);
        Fill(nd("jetsume")      .num, jet_sume);
        Fill(nd("jetdrmax")     .num, jet_drmax);
        Fill(nd("jetdravg")     .num, jet_dravg);
        Fill(nd("jetsumntracks").num, jet_sumntracks);
      }
    }
  }

  printf("\r                                \n");
  printf("%f events in denominator\n", den);
  printf("%30s  %12s  %12s   %10s [%10s, %10s] +%10s -%10s\n", "name", "num", "den", "eff", "lo", "hi", "+", "-");
  for (const auto& p : nums) {
    const interval i = clopper_pearson_binom(p.second, den);
    printf("%30s  %12f  %12f  %10f [%10f, %10f] +%10f -%10f\n", p.first.c_str(), p.second, den, i.value, i.lower, i.upper, i.upper - i.value, i.value - i.lower);
  }
}
