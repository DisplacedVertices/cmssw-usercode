#include "TH1.h"
#include "TTree.h"
#include "TVector2.h"
#include "JMTucker/MFVNeutralino/interface/MovedTracksNtuple.h"
#include "utils.h"

int main(int argc, char** argv) {
  if (argc < 3) {
    fprintf(stderr, "usage: hists.exe in.root out.root\n");
    return 1;
  }

  const char* in_fn  = argv[1];
  const char* out_fn = argv[2];
  const bool apply_weight = true;

  root_setup();

  file_and_tree fat(in_fn, out_fn);
  TTree* t = fat.t;
  mfv::MovedTracksNtuple& nt = fat.nt;

  TH1F* h_weight = new TH1F("h_weight", ";weight;events/0.01", 200, 0, 2);
  TH1F* h_npu = new TH1F("h_npu", ";# PU;events/1", 100, 0, 100);

  const int num_numdens = 6;

  numdens nds[num_numdens] = {
    numdens("nocuts"),
    numdens("ntracks"),
    numdens("ntracksPptgt3"),
    numdens("ntracksPptgt3Pdr"),
    numdens("ntracksPptgt3Pbs2d"),
    numdens("all")
  };

  for (numdens& nd : nds) {
    nd.book("movedist2", ";movement 2-dist;events/0.01 cm", 200, 0, 2);
    nd.book("movedist3", ";movement 3-dist;events/0.01 cm", 200, 0, 2);
    nd.book("npv", ";# PV;events/1", 100, 0, 100);
    nd.book("pvz", ";PV z (cm);events/0.24 cm", 200, -24, 24);
    nd.book("pvrho", ";PV #rho (cm);events/1 #mum", 200, 0, 0.02);
    nd.book("pvntracks", ";PV # tracks;events/2", 200, 0, 400);
    nd.book("pvsumpt2", ";PV #Sigma p_{T}^{2} (GeV^{2});events/200 GeV^{2}", 200, 0, 40000);
    nd.book("sumht", ";#Sigma H_{T} (GeV);events/50 GeV", 50, 0, 2500);
  }

  double den = 0;
  std::map<std::string, double> nums;

  for (int j = 0, je = t->GetEntries(); j < je; ++j) {
    if (t->LoadTree(j) < 0) break;
    if (t->GetEntry(j) <= 0) continue;
    if (j % 250000 == 0) {
      printf("\r%i/%i", j, je);
      fflush(stdout);
    }

    const double w = apply_weight ? nt.weight : 1.;

    const size_t n_raw_vtx = nt.p_vtxs_x->size();

    if (nt.jetsumht < 500 ||
        nt.jetpt4 < 60)
//        movedist2 < 0.03 ||
//        movedist2 > 2.5 ||
//        jet_drmax > 4)
      continue;

    h_weight->Fill(w);
    h_npu->Fill(nt.npu, w);

    auto Fill = [&w](TH1F* h, double v) { h->Fill(v, w); };

    for (numdens& nd : nds) {
      Fill(nd("movedist2")    .den, movedist2);
      Fill(nd("movedist3")    .den, movedist3);
      Fill(nd("npv")          .den, nt.npv);
      Fill(nd("pvz")          .den, nt.pvz);
      Fill(nd("pvrho")        .den, mag(nt.pvx, nt.pvy));
      Fill(nd("pvntracks")    .den, nt.pvntracks);
      Fill(nd("pvsumpt2")     .den, nt.pvsumpt2);
      Fill(nd("sumht")        .den, nt.jetsumht);
    }

    den += w;

    int n_pass_nocuts = 0;
    int n_pass_ntracks = 0;
    int n_pass_ntracksPptgt3 = 0;
    int n_pass_ntracksPptgt3Pdr = 0;
    int n_pass_ntracksPptgt3Pbs2d = 0;
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
      const bool pass_ntracksptgt3 = nt.p_vtxs_ntracksptgt3->at(ivtx) >= 3;
      const bool pass_drmin        = nt.p_vtxs_drmin       ->at(ivtx) < 0.4;
      const bool pass_drmax        = nt.p_vtxs_drmax       ->at(ivtx) < 4;
      const bool pass_mindrmax     = nt.p_vtxs_drmax       ->at(ivtx) > 1.2;
      const bool pass_bs2derr      = nt.p_vtxs_bs2derr     ->at(ivtx) < 0.0025;
      const bool pass_drcuts = pass_drmin && pass_drmax && pass_mindrmax;

      if (1)                                                                 { set_it_if_first(first_vtx_to_pass[0], ivtx); ++n_pass_nocuts;             }
      if (pass_ntracks)                                                      { set_it_if_first(first_vtx_to_pass[1], ivtx); ++n_pass_ntracks;            }
      if (pass_ntracks && pass_ntracksptgt3)                                 { set_it_if_first(first_vtx_to_pass[2], ivtx); ++n_pass_ntracksPptgt3;      }
      if (pass_ntracks && pass_ntracksptgt3 && pass_drcuts)                  { set_it_if_first(first_vtx_to_pass[3], ivtx); ++n_pass_ntracksPptgt3Pdr;   }
      if (pass_ntracks && pass_ntracksptgt3 &&                pass_bs2derr)  { set_it_if_first(first_vtx_to_pass[4], ivtx); ++n_pass_ntracksPptgt3Pbs2d; }
      if (pass_ntracks && pass_ntracksptgt3 && pass_drcuts && pass_bs2derr)  { set_it_if_first(first_vtx_to_pass[5], ivtx); ++n_pass_all;                }
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
    if (n_pass_ntracksPptgt3)      nums["ntracksPptgt3"]      += w;
    if (n_pass_ntracksPptgt3Pdr)   nums["ntracksPptgt3Pdr"]   += w;
    if (n_pass_ntracksPptgt3Pbs2d) nums["ntracksPptgt3Pbs2d"] += w;
    if (n_pass_all)                nums["all"]                += w;

    const int passes[num_numdens] = {
      n_pass_nocuts,
      n_pass_ntracks,
      n_pass_ntracksPptgt3,
      n_pass_ntracksPptgt3Pdr,
      n_pass_ntracksPptgt3Pbs2d,
      n_pass_all
    };

    for (int i = 0; i < num_numdens; ++i) {
      if (passes[i]) {
        numdens& nd = nds[i];
        Fill(nd("movedist2")    .num, movedist2);
        Fill(nd("movedist3")    .num, movedist3);
        Fill(nd("npv")          .num, nt.npv);
        Fill(nd("pvz")          .num, nt.pvz);
        Fill(nd("pvrho")        .num, mag(nt.pvx, nt.pvy));
        Fill(nd("pvntracks")    .num, nt.pvntracks);
        Fill(nd("pvsumpt2")     .num, nt.pvsumpt2);
        Fill(nd("sumht")        .num, nt.jetsumht);
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
