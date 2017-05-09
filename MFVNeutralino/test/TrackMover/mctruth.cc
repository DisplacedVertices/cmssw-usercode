#include "TH1.h"
#include "TTree.h"
#include "TVector2.h"
#include "JMTucker/MFVNeutralino/interface/MovedTracksNtuple.h"
#include "utils.h"

int main(int argc, char** argv) {
  if (argc < 4) {
    fprintf(stderr, "usage: mctruth.exe in.root out.root min_lspdist3\n");
    return 1;
  }

  const char* in_fn  = argv[1];
  const char* out_fn = argv[2];
  const double min_lspdist3 = atof(argv[3]);
  const bool apply_weight = true;
  if (!apply_weight)
    printf("******************************\nno pileup weight applied\n******************************\n");

  root_setup();

  file_and_tree fat(in_fn, out_fn);
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

  for (numdens& nd : nds) {
    nd.book("lspdist2", ";2-dist between gen verts;events/0.01 cm", 200, 0, 2);
    nd.book("lspdist3", ";3-dist between gen verts;events/0.01 cm", 200, 0, 2);
    nd.book("lspdistz", ";z-dist between gen verts;events/0.01 cm", 200, 0, 2);
    nd.book("movedist2", ";movement 2-dist;events/0.01 cm", 200, 0, 2);
    nd.book("movedist3", ";movement 3-dist;events/0.01 cm", 200, 0, 2);
    nd.book("npv", ";# PV;events/1", 100, 0, 100);
    nd.book("pvz", ";PV z (cm);events/0.24 cm", 200, -24, 24);
    nd.book("pvrho", ";PV #rho (cm);events/1 #mum", 200, 0, 0.02);
    nd.book("pvntracks", ";PV # tracks;events/2", 200, 0, 400);
    nd.book("pvsumpt2", ";PV #Sigma p_{T}^{2} (GeV^{2});events/200 GeV^{2}", 200, 0, 40000);
    nd.book("ht", ";#Sigma H_{T} (GeV);events/50 GeV", 50, 0, 2500);
  }

  double den = 0;
  std::map<std::string, double> nums;

  printf("\n*********************************\nafter fixing gen z bug in ntuple, redo moved tracks treer and fix the min_lspdist3 and movedist cut in vtx loop below\n*********************************\n");

  for (int j = 0, je = t->GetEntries(); j < je; ++j) {
    if (t->LoadTree(j) < 0) break;
    if (t->GetEntry(j) <= 0) continue;
    if (j % 250000 == 0) {
      printf("\r%i/%i", j, je);
      fflush(stdout);
    }

    const bool pass_800 = bool(nt.pass_hlt & 0x2);
    const bool pass_900_450_AK450 = bool(nt.pass_hlt & 0x1C);
    const bool H_scheme = false; // could throw random number?

    if (nt.jetht < 1000 ||
        !(pass_800 || (H_scheme && pass_900_450_AK450)))
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

    if (lspdist2 < 0 ||
        lspdist2 < min_lspdist3 || // JMTBAD put back to lspdist3 after fixing
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
          movedist2 > 2.5)
        continue;

      for (numdens& nd : nds) {
        Fill(nd("lspdist2")     .den, lspdist2);
        Fill(nd("lspdist3")     .den, lspdist3);
        Fill(nd("lspdistz")     .den, lspdistz);
        Fill(nd("movedist2")    .den, movedist2);
        Fill(nd("movedist3")    .den, movedist3);
        Fill(nd("npv")          .den, nt.npv);
        Fill(nd("pvz")          .den, nt.pvz);
        Fill(nd("pvrho")        .den, mag(nt.pvx, nt.pvy));
        Fill(nd("pvntracks")    .den, nt.pvntracks);
        Fill(nd("pvsumpt2")     .den, nt.pvsumpt2);
        Fill(nd("ht")        .den, nt.jetht);
      }

      den += w;

      int n_pass_nocuts = 0;
      int n_pass_ntracks = 0;
      int n_pass_all = 0;

      std::vector<int> first_vtx_to_pass(num_numdens, -1);
      auto set_it_if_first = [](int& to_set, int to_set_to) { if (to_set == -1) to_set = to_set_to; };

      for (size_t ivtx = 0; ivtx < n_raw_vtx; ++ivtx) {
        const double dist2move = mag(gen_vx - nt.p_vtxs_x->at(ivtx),
                                     gen_vy - nt.p_vtxs_y->at(ivtx));
                                     //                                     gen_vz - nt.p_vtxs_z->at(ivtx));  // JMTBAD maybe put back to 3D
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

      //for (int i = 0; i < num_numdens; ++i) {
      //  int ivtx = first_vtx_to_pass[i];
      //  if (ivtx != -1) {
      //    h_vtxntracks      [i]->Fill(nt.p_vtxs_ntracks     ->at(ivtx));
      //    h_vtxntracksptgt3 [i]->Fill(nt.p_vtxs_ntracksptgt3->at(ivtx));
      //    h_vtxdrmin        [i]->Fill(nt.p_vtxs_drmin       ->at(ivtx));
      //    h_vtxdrmax        [i]->Fill(nt.p_vtxs_drmax       ->at(ivtx));
      //    h_vtxbs2derr      [i]->Fill(nt.p_vtxs_bs2derr     ->at(ivtx));
      //  }
      //}

      if (n_pass_nocuts)       nums["nocuts"]       += w;
      if (n_pass_ntracks)      nums["ntracks"]      += w;
      if (n_pass_all)          nums["all"]          += w;

      const int passes[num_numdens] = {
        n_pass_nocuts,
        n_pass_ntracks,
        n_pass_all
      };

      for (int i = 0; i < num_numdens; ++i) {
        if (passes[i]) {
          numdens& nd = nds[i];
          Fill(nd("lspdist2")     .num, lspdist2);
          Fill(nd("lspdist3")     .num, lspdist3);
          Fill(nd("lspdistz")     .num, lspdistz);
          Fill(nd("movedist2")    .num, movedist2);
          Fill(nd("movedist3")    .num, movedist3);
          Fill(nd("npv")          .num, nt.npv);
          Fill(nd("pvz")          .num, nt.pvz);
          Fill(nd("pvrho")        .num, mag(nt.pvx, nt.pvy));
          Fill(nd("pvntracks")    .num, nt.pvntracks);
          Fill(nd("pvsumpt2")     .num, nt.pvsumpt2);
          Fill(nd("ht")        .num, nt.jetht);
        }
      }
    }
  }

  printf("\r                                \n");
  printf("%f events in denominator\n", den);
  printf("%20s  %12s  %10s +- %10s\n", "name", "num", "eff", "seff");
  for (const auto& p : nums) {
    const interval i = clopper_pearson_binom(p.second, den);
    printf("%20s  %12.2f  %10.4f +- %10.4f\n", p.first.c_str(), p.second, i.value, (i.upper - i.lower)/2);
  }
}
