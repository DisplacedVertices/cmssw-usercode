#include "TH2.h"
#include "TRandom3.h"
#include "TTree.h"
#include "TVector2.h"
#include "JMTucker/MFVNeutralino/interface/Ntuple.h"
#include "utils.h"

int main(int argc, char** argv) {
  if (argc < 4) {
    fprintf(stderr, "usage: mctruth.exe in.root out.root min_lspdist3\n");
    return 1;
  }

  gRandom->SetSeed(4916823);

  const char* in_fn  = argv[1];
  const char* out_fn = argv[2];
  const double min_lspdist3 = atof(argv[3]);
  const bool apply_weight = true;
  if (!apply_weight)
    printf("******************************\nno pileup weight applied\n******************************\n");

  root_setup();

  file_and_tree fat(in_fn, out_fn, "mfvMovedTree/t");
  TTree* t = fat.t;
  mfv::MovedTracksNtuple& nt = fat.nt;

  TH1D* h_weight = new TH1D("h_weight", ";weight;events/0.01", 200, 0, 2);
  TH1D* h_npu = new TH1D("h_npu", ";# PU;events/1", 100, 0, 100);

  const int num_numdens = 3;

  numdens nds[num_numdens] = {
    numdens("nocuts"),
    numdens("ntracks"),
    numdens("all")
  };

  enum { k_lspdist2, k_lspdist3, k_lspdistz, k_movedist2, k_movedist3, k_npv, k_pvz, k_pvrho, k_pvntracks, k_pvscore, k_ht };
  for (numdens& nd : nds) {
    nd.book(k_lspdist2, "lspdist2", ";2-dist between gen verts;events/0.01 cm", 200, 0, 2);
    nd.book(k_lspdist3, "lspdist3", ";3-dist between gen verts;events/0.01 cm", 200, 0, 2);
    nd.book(k_lspdistz, "lspdistz", ";z-dist between gen verts;events/0.01 cm", 200, 0, 2);
    nd.book(k_movedist2, "movedist2", ";movement 2-dist;events/0.01 cm", 200, 0, 2);
    nd.book(k_movedist3, "movedist3", ";movement 3-dist;events/0.01 cm", 200, 0, 2);
    nd.book(k_npv, "npv", ";# PV;events/1", 100, 0, 100);
    nd.book(k_pvz, "pvz", ";PV z (cm);events/0.24 cm", 200, -24, 24);
    nd.book(k_pvrho, "pvrho", ";PV #rho (cm);events/1 #mum", 200, 0, 0.02);
    nd.book(k_pvntracks, "pvntracks", ";PV # tracks;events/2", 200, 0, 400);
    nd.book(k_pvscore, "pvscore", ";PV #Sigma p_{T}^{2} (GeV^{2});events/200 GeV^{2}", 200, 0, 40000);
    nd.book(k_ht, "ht", ";#Sigma H_{T} (GeV);events/50 GeV", 50, 0, 2500);
  }

  TH1D* h_vtxntracks[num_numdens] = {0};
  TH1D* h_vtxbs2derr[num_numdens] = {0};
  TH1D* h_vtxtkonlymass[num_numdens] = {0};
  TH1D* h_vtxs_mass[num_numdens] = {0};

  for (int i = 0; i < num_numdens; ++i) {
    h_vtxntracks[i] = new TH1D(TString::Format("h_%i_vtxntracks",      i), ";# tracks in largest vertex;events/1", 40, 0, 40);
    h_vtxbs2derr[i] = new TH1D(TString::Format("h_%i_vtxbs2derr",      i), ";#sigma(d_{BV}) of largest vertex (cm);events/2 #mum", 50, 0, 0.01);
    h_vtxtkonlymass[i] = new TH1D(TString::Format("h_%i_vtxtkonlymass", i), ";track-only mass of largest vertex (GeV);events/1 GeV", 500, 0, 500);
    h_vtxs_mass[i] = new TH1D(TString::Format("h_%i_vtxs_mass", i), ";track+jets mass of largest vertex (GeV);vertices/50 GeV", 100, 0, 5000);
  }

  double den = 0;
  std::map<std::string, double> nums;

  for (int j = 0, je = t->GetEntries(); j < je; ++j) {
    if (t->LoadTree(j) < 0) break;
    if (t->GetEntry(j) <= 0) continue;

    if (nt.jets().ht() < 1200 ||
        nt.jets().nminpt() < 4)
      continue;

    const double w = apply_weight ? nt.base().weight() : 1.;
    h_weight->Fill(w);
    h_npu->Fill(nt.base().npu(), w);
    auto F1 = [&w](TH1* h, double v)            { h                    ->Fill(v,     w); };
    //auto F2 = [&w](TH1* h, double v, double v2) { dynamic_cast<TH2*>(h)->Fill(v, v2, w); };

    const double lspdist3 = nt.gentruth().lspdist3();

    if (lspdist3 < min_lspdist3)
      continue;

    const size_t nvtx = nt.vertices().n();
    const double lspdist2 = nt.gentruth().lspdist2();
    const double lspdistz = nt.gentruth().lspdistz();

    for (int ilsp = 0; ilsp < 2; ++ilsp) {
      const TVector3 lspdecay = nt.gentruth().decay(ilsp);
      const double movedist2 = lspdecay.Perp();
      const double movedist3 = lspdecay.Mag();

      if (movedist2 < 0.03 ||
          movedist2 > 2.0)
        continue;

      for (numdens& nd : nds) {
        F1(nd(k_lspdist2) .den, lspdist2);
        F1(nd(k_lspdist3) .den, lspdist3);
        F1(nd(k_lspdistz) .den, lspdistz);
        F1(nd(k_movedist2).den, movedist2);
        F1(nd(k_movedist3).den, movedist3);
        F1(nd(k_npv)      .den, nt.pvs().n());
        F1(nd(k_pvz)      .den, nt.pvs().z(0));
        F1(nd(k_pvrho)    .den, nt.pvs().rho(0));
        F1(nd(k_pvntracks).den, nt.pvs().ntracks(0));
        F1(nd(k_pvscore)  .den, nt.pvs().score(0));
        F1(nd(k_ht)       .den, nt.jets().ht());
      }

      den += w;

      int n_pass_nocuts = 0;
      int n_pass_ntracks = 0;
      int n_pass_all = 0;

      std::vector<int> first_vtx_to_pass(num_numdens, -1);
      auto set_it_if_first = [](int& to_set, int to_set_to) { if (to_set == -1) to_set = to_set_to; };

      for (size_t i = 0; i < nvtx; ++i) {
        const double dist2move = (lspdecay - nt.vertices().pos(i)).Mag();
        if (dist2move > 0.0084)
          continue;

        const bool pass_ntracks = nt.vertices().ntracks(i) >= 5;
        const bool pass_bs2derr = nt.vertices().bs2derr(i) < 0.0025;

        if (1)                             { set_it_if_first(first_vtx_to_pass[0], i); ++n_pass_nocuts;  }
        if (pass_ntracks)                  { set_it_if_first(first_vtx_to_pass[1], i); ++n_pass_ntracks; }
        if (pass_ntracks && pass_bs2derr)  { set_it_if_first(first_vtx_to_pass[2], i); ++n_pass_all;     }
      }

      for (int in = 0; in < num_numdens; ++in) {
        const int iv = first_vtx_to_pass[in];
        if (iv != -1) {
          h_vtxntracks   [in]->Fill(nt.vertices().ntracks(iv));
          h_vtxbs2derr   [in]->Fill(nt.vertices().bs2derr(iv));
	  h_vtxtkonlymass[in]->Fill(nt.vertices().tkonlymass(iv));
	  h_vtxs_mass    [in]->Fill(nt.vertices().mass(iv));
        }
      }

      if (n_pass_nocuts)  nums["nocuts"]  += w;
      if (n_pass_ntracks) nums["ntracks"] += w;
      if (n_pass_all)     nums["all"]     += w;

      const int npasses[num_numdens] = {
        n_pass_nocuts,
        n_pass_ntracks,
        n_pass_all
      };

      for (int in = 0; in < num_numdens; ++in) {
        if (!npasses[in])
          continue;

        numdens& nd = nds[in];
        F1(nd(k_lspdist2) .num, lspdist2);
        F1(nd(k_lspdist3) .num, lspdist3);
        F1(nd(k_lspdistz) .num, lspdistz);
        F1(nd(k_movedist2).num, movedist2);
        F1(nd(k_movedist3).num, movedist3);
        F1(nd(k_npv)      .num, nt.pvs().n());
        F1(nd(k_pvz)      .num, nt.pvs().z(0));
        F1(nd(k_pvrho)    .num, nt.pvs().rho(0));
        F1(nd(k_pvntracks).num, nt.pvs().ntracks(0));
        F1(nd(k_pvscore)  .num, nt.pvs().score(0));
        F1(nd(k_ht)       .num, nt.jets().ht());
      }
    }
  }

  printf("%12.1f", den);
  for (const std::string& c : {"nocuts", "ntracks", "all"}) {
    const interval i = clopper_pearson_binom(nums[c], den);
    printf("    %6.4f +- %6.4f", i.value, i.error());
  }
  printf("\n");
}
