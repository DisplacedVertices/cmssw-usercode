#include "TH1.h"
#include "TRandom3.h"
#include "TTree.h"
#include "TVector2.h"
#include "JMTucker/MFVNeutralino/interface/MovedTracksNtuple.h"
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

    const bool pass_trig = nt.pass_hlt & 1;

    if (nt.jetht < 1200 ||
        nt.nalljets() < 4 ||
        !pass_trig)
      continue;

    const double w = apply_weight ? nt.weight : 1.;
    h_weight->Fill(w);
    h_npu->Fill(nt.npu, w);
    auto Fill = [&w](TH1D* h, double v) { h->Fill(v, w); };

    const size_t n_raw_vtx = nt.p_vtxs_x->size();

    const double lspdist2 = mag(nt.gen_lsp_decay[0] - nt.gen_lsp_decay[3],
                                nt.gen_lsp_decay[1] - nt.gen_lsp_decay[4]);
    const double lspdist3 = mag(nt.gen_lsp_decay[0] - nt.gen_lsp_decay[3],
                                nt.gen_lsp_decay[1] - nt.gen_lsp_decay[4],
                                nt.gen_lsp_decay[2] - nt.gen_lsp_decay[5]);
    const double lspdistz = fabs(nt.gen_lsp_decay[2] - nt.gen_lsp_decay[5]);

    //printf("lspdist2 %f dist3 %f distz %f n_raw_vtx %lu  weight %f\n", lspdist2, lspdist3, lspdistz, n_raw_vtx, w);

    if (lspdist3 < min_lspdist3 ||
        lspdistz < 0)
      continue;

    for (int ilsp = 0; ilsp < 2; ++ilsp) {
      const double gen_vx = nt.gen_lsp_decay[ilsp*3 + 0];
      const double gen_vy = nt.gen_lsp_decay[ilsp*3 + 1]; 
      const double gen_vz = nt.gen_lsp_decay[ilsp*3 + 2];
      const double movedist2 = mag(gen_vx, gen_vy);
      const double movedist3 = mag(gen_vx, gen_vy, gen_vz);

      //printf("ilsp %i movedist2 %f dist3 %f\n", ilsp, movedist2, movedist3);

      if (movedist2 < 0.03 ||
          movedist2 > 2.0)
        continue;

      for (numdens& nd : nds) {
        Fill(nd(k_lspdist2) .den, lspdist2);
        Fill(nd(k_lspdist3) .den, lspdist3);
        Fill(nd(k_lspdistz) .den, lspdistz);
        Fill(nd(k_movedist2).den, movedist2);
        Fill(nd(k_movedist3).den, movedist3);
        Fill(nd(k_npv)      .den, nt.npv);
        Fill(nd(k_pvz)      .den, nt.pvz);
        Fill(nd(k_pvrho)    .den, mag(nt.pvx, nt.pvy));
        Fill(nd(k_pvntracks).den, nt.pvntracks);
        Fill(nd(k_pvscore)  .den, nt.pvscore);
        Fill(nd(k_ht)       .den, nt.jetht);
      }

      den += w;

      int n_pass_nocuts = 0;
      int n_pass_ntracks = 0;
      int n_pass_all = 0;

      std::vector<int> first_vtx_to_pass(num_numdens, -1);
      auto set_it_if_first = [](int& to_set, int to_set_to) { if (to_set == -1) to_set = to_set_to; };

      for (size_t ivtx = 0; ivtx < n_raw_vtx; ++ivtx) {
        const double dist2move = mag(gen_vx - nt.p_vtxs_x->at(ivtx),
                                     gen_vy - nt.p_vtxs_y->at(ivtx),
                                     gen_vz - nt.p_vtxs_z->at(ivtx));
        //printf("ivtx %lu dist2move %f\n", ivtx, dist2move);
        if (dist2move > 0.0084)
          continue;

        const bool pass_ntracks = nt.p_vtxs_ntracks->at(ivtx) >= 5;
        const bool pass_bs2derr = nt.p_vtxs_bs2derr->at(ivtx) < 0.0025;

        //printf("  ntracks %i pass? %i  bs2derr %f pass? %i\n", nt.p_vtxs_ntracks->at(ivtx), pass_ntracks, nt.p_vtxs_bs2derr->at(ivtx), pass_bs2derr);

        if (1)                             { set_it_if_first(first_vtx_to_pass[0], ivtx); ++n_pass_nocuts;       }
        if (pass_ntracks)                  { set_it_if_first(first_vtx_to_pass[1], ivtx); ++n_pass_ntracks;      }
        if (pass_ntracks && pass_bs2derr)  { set_it_if_first(first_vtx_to_pass[2], ivtx); ++n_pass_all; }
      }

      for (int i = 0; i < num_numdens; ++i) {
        int ivtx = first_vtx_to_pass[i];
        if (ivtx != -1) {
          h_vtxntracks      [i]->Fill(nt.p_vtxs_ntracks->at(ivtx));
          h_vtxbs2derr      [i]->Fill(nt.p_vtxs_bs2derr->at(ivtx));
	  h_vtxtkonlymass[i]->Fill(nt.p_vtxs_tkonlymass->at(ivtx));
	  h_vtxs_mass[i]->Fill(nt.p_vtxs_mass->at(ivtx));
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
          Fill(nd(k_lspdist2) .num, lspdist2);
          Fill(nd(k_lspdist3) .num, lspdist3);
          Fill(nd(k_lspdistz) .num, lspdistz);
          Fill(nd(k_movedist2).num, movedist2);
          Fill(nd(k_movedist3).num, movedist3);
          Fill(nd(k_npv)      .num, nt.npv);
          Fill(nd(k_pvz)      .num, nt.pvz);
          Fill(nd(k_pvrho)    .num, mag(nt.pvx, nt.pvy));
          Fill(nd(k_pvntracks).num, nt.pvntracks);
          Fill(nd(k_pvscore)  .num, nt.pvscore);
          Fill(nd(k_ht)       .num, nt.jetht);
        }
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
