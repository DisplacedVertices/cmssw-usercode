#include <iostream>
#include "TCanvas.h"
#include "TFile.h"
#include "TH2.h"
#include "TTree.h"
#include "TVector2.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"

const int NBQUARKS = 3;
const char* bquarks_hist_names[NBQUARKS] = {"", "_bquarks", "_nobquarks"};
const char* bquarks_nice_names[NBQUARKS] = {"", " with b quarks", " without b quarks"};

const int NVTX = 2;
const char* vtx_hist_names[NVTX] = {"1v", "2v"};
const char* vtx_nice_names[NVTX] = {"one-vertex", "two-vertex"};

const int NBDISC = 3;
const char* bdisc_names[NBDISC] = {"loose", "medium", "tight"};
const double bdisc_mins[NBDISC] = {0.5803, 0.8838, 0.9693};

const int NBTAGS = 2;
const int nbtag_mins[NBTAGS] = {1, 2};

const int NDBV = 3;
const char* dbv_names[NDBV] = {"all", "longer", "shorter"};

TH1F* h_bquark_flavor_code[NBQUARKS][NVTX] = {{0}};
TH1F* h_njets[NBQUARKS][NVTX] = {{0}};
TH1F* h_jet_bdisc[NBQUARKS][NVTX] = {{0}};

TH1F* h_nbtags[NBQUARKS][NVTX][NBDISC] = {{{0}}};
TH1F* h_btag_flavor_code[NBQUARKS][NVTX][NBDISC][NBTAGS] = {{{0}}};
TH2F* h_btag_flavor_code_vs_bquark_flavor_code[NBQUARKS][NVTX][NBDISC][NBTAGS] = {{{{0}}}};

TH1F* h_dbv[NBQUARKS][NVTX][NDBV] = {{{0}}};
TH1F* h_dbv_btag[NBQUARKS][NVTX][NDBV][NBDISC][NBTAGS] = {{{{{0}}}}};
TH1F* h_dbv_nobtag[NBQUARKS][NVTX][NDBV][NBDISC][NBTAGS] = {{{{{0}}}}};

TH1F* h_nbquarks[NBQUARKS][NVTX] = {{0}};
TH1F* h_drmin_tkp_bquark[NBQUARKS][NVTX] = {{0}};
TH1F* h_ntk_bquark[NBQUARKS][NVTX] = {{0}};

void book_hists(int ntk) {
  for (int i_nbquarks = 0; i_nbquarks < NBQUARKS; ++i_nbquarks) {
    for (int i_nvtx = 0; i_nvtx < NVTX; ++i_nvtx) {
      h_bquark_flavor_code[i_nbquarks][i_nvtx] = new TH1F(TString::Format("h%s_%s_bquark_flavor_code", bquarks_hist_names[i_nbquarks], vtx_hist_names[i_nvtx]), TString::Format("%d-track %s events%s;bquark_flavor_code;Events", ntk, vtx_nice_names[i_nvtx], bquarks_nice_names[i_nbquarks]), 2, 0, 2);
      h_njets[i_nbquarks][i_nvtx] = new TH1F(TString::Format("h%s_%s_njets", bquarks_hist_names[i_nbquarks], vtx_hist_names[i_nvtx]), TString::Format("%d-track %s events%s;number of jets;Events", ntk, vtx_nice_names[i_nvtx], bquarks_nice_names[i_nbquarks]), 40, 0, 40);
      h_jet_bdisc[i_nbquarks][i_nvtx] = new TH1F(TString::Format("h%s_%s_jet_bdisc", bquarks_hist_names[i_nbquarks], vtx_hist_names[i_nvtx]), TString::Format("%d-track %s events%s;jet bdisc;Number of jets", ntk, vtx_nice_names[i_nvtx], bquarks_nice_names[i_nbquarks]), 100, 0, 1);

      for (int i_nbdisc = 0; i_nbdisc < NBDISC; ++i_nbdisc) {
        h_nbtags[i_nbquarks][i_nvtx][i_nbdisc] = new TH1F(TString::Format("h%s_%s_nbtags_%s", bquarks_hist_names[i_nbquarks], vtx_hist_names[i_nvtx], bdisc_names[i_nbdisc]), TString::Format("%d-track %s events%s;number of %s btags;Events", ntk, vtx_nice_names[i_nvtx], bquarks_nice_names[i_nbquarks], bdisc_names[i_nbdisc]), 20, 0, 20);

        for (int i_nbtags = 0; i_nbtags < NBTAGS; ++i_nbtags) {
          h_btag_flavor_code[i_nbquarks][i_nvtx][i_nbdisc][i_nbtags] = new TH1F(TString::Format("h%s_%s_%d%s_btag_flavor_code", bquarks_hist_names[i_nbquarks], vtx_hist_names[i_nvtx], nbtag_mins[i_nbtags], bdisc_names[i_nbdisc]), TString::Format("%d-track %s events%s;%d%s_btag_flavor_code;Events", ntk, vtx_nice_names[i_nvtx], bquarks_nice_names[i_nbquarks], nbtag_mins[i_nbtags], bdisc_names[i_nbdisc]), 2, 0, 2);
          h_btag_flavor_code_vs_bquark_flavor_code[i_nbquarks][i_nvtx][i_nbdisc][i_nbtags] = new TH2F(TString::Format("h%s_%s_%d%s_btag_flavor_code_vs_bquark_flavor_code", bquarks_hist_names[i_nbquarks], vtx_hist_names[i_nvtx], nbtag_mins[i_nbtags], bdisc_names[i_nbdisc]), TString::Format("%d-track %s events%s;bquark_flavor_code;%d%s_btag_flavor_code", ntk, vtx_nice_names[i_nvtx], bquarks_nice_names[i_nbquarks], nbtag_mins[i_nbtags], bdisc_names[i_nbdisc]), 2, 0, 2, 2, 0, 2);
        }
      }
    }
  }

  for (int i_nbquarks = 0; i_nbquarks < NBQUARKS; ++i_nbquarks) {
    for (int i_nvtx = 0; i_nvtx < NVTX; ++i_nvtx) {
      for (int i_ndbv = 0; i_ndbv < NDBV; ++i_ndbv) {
        if (i_nvtx == 0 && i_ndbv != 0) continue;
        h_dbv[i_nbquarks][i_nvtx][i_ndbv] = new TH1F(TString::Format("h%s_%s_%s_dbv", bquarks_hist_names[i_nbquarks], vtx_hist_names[i_nvtx], dbv_names[i_ndbv]), TString::Format("%d-track %s events%s;d_{BV} (cm);Events", ntk, vtx_nice_names[i_nvtx], bquarks_nice_names[i_nbquarks]), 40, 0, 0.2);

        for (int i_nbdisc = 0; i_nbdisc < NBDISC; ++i_nbdisc) {
          for (int i_nbtags = 0; i_nbtags < NBTAGS; ++i_nbtags) {
            h_dbv_btag[i_nbquarks][i_nvtx][i_ndbv][i_nbdisc][i_nbtags] = new TH1F(TString::Format("h%s_%s_%s_dbv_%d%s_btag", bquarks_hist_names[i_nbquarks], vtx_hist_names[i_nvtx], dbv_names[i_ndbv], nbtag_mins[i_nbtags], bdisc_names[i_nbdisc]), TString::Format("%d-track %s events%s with #geq%d %s btag;d_{BV} (cm);Events", ntk, vtx_nice_names[i_nvtx], bquarks_nice_names[i_nbquarks], nbtag_mins[i_nbtags], bdisc_names[i_nbdisc]), 40, 0, 0.2);
            h_dbv_nobtag[i_nbquarks][i_nvtx][i_ndbv][i_nbdisc][i_nbtags] = new TH1F(TString::Format("h%s_%s_%s_dbv_%d%s_nobtag", bquarks_hist_names[i_nbquarks], vtx_hist_names[i_nvtx], dbv_names[i_ndbv], nbtag_mins[i_nbtags], bdisc_names[i_nbdisc]), TString::Format("%d-track %s events%s without #geq%d %s btag;d_{BV} (cm);Events", ntk, vtx_nice_names[i_nvtx], bquarks_nice_names[i_nbquarks], nbtag_mins[i_nbtags], bdisc_names[i_nbdisc]), 40, 0, 0.2);
          }
        }
      }
    }
  }

  for (int i_nbquarks = 0; i_nbquarks < NBQUARKS; ++i_nbquarks) {
    for (int i_nvtx = 0; i_nvtx < NVTX; ++i_nvtx) {
      h_nbquarks[i_nbquarks][i_nvtx] = new TH1F(TString::Format("h%s_%s_nbquarks", bquarks_hist_names[i_nbquarks], vtx_hist_names[i_nvtx]), TString::Format("%d-track %s events%s;number of b quarks;Events", ntk, vtx_nice_names[i_nvtx], bquarks_nice_names[i_nbquarks]), 20, 0, 20);
      h_drmin_tkp_bquark[i_nbquarks][i_nvtx] = new TH1F(TString::Format("h%s_%s_drmin_tkp_bquark", bquarks_hist_names[i_nbquarks], vtx_hist_names[i_nvtx]), TString::Format("%d-track %s events%s;#DeltaR(track momentum, closest b quark);Number of tracks", ntk, vtx_nice_names[i_nvtx], bquarks_nice_names[i_nbquarks]), 100, 0, 10);
      h_ntk_bquark[i_nbquarks][i_nvtx] = new TH1F(TString::Format("h%s_%s_ntk_bquark", bquarks_hist_names[i_nbquarks], vtx_hist_names[i_nvtx]), TString::Format("%d-track %s events%s;number of tracks with #DeltaR(track momentum, closest b quark) < 0.4;Vertices", ntk, vtx_nice_names[i_nvtx], bquarks_nice_names[i_nbquarks]), 40, 0, 40);
    }
  }
}

bool analyze(long long j, long long je, const mfv::MiniNtuple& nt) {
  double w = nt.weight;

  int bquark_flavor_code = nt.gen_flavor_code == 2 ? 1 : 0;
  int i_nbquarks[2] = {0, 2-bquark_flavor_code};

  int i_nvtx = nt.nvtx > NVTX ? NVTX-1 : nt.nvtx-1;
  assert(i_nvtx == 0 || i_nvtx == 1);

  for (int i = 0; i < 2; ++i) {
    h_bquark_flavor_code[i_nbquarks[i]][i_nvtx]->Fill(bquark_flavor_code, w);
    h_njets[i_nbquarks[i]][i_nvtx]->Fill(nt.njets, w);

    double dbv0 = hypot(nt.x0, nt.y0);
    double dbv1 = hypot(nt.x1, nt.y1);
    double dbv[NDBV] = {dbv1, dbv0 >= dbv1 ? dbv0 : dbv1, dbv0 >= dbv1 ? dbv1 : dbv0};

    h_dbv[i_nbquarks[i]][i_nvtx][0]->Fill(dbv0, w);
    if (i_nvtx == 1) {
      for (int i_ndbv = 0; i_ndbv < NDBV; ++i_ndbv) {
        h_dbv[i_nbquarks[i]][i_nvtx][i_ndbv]->Fill(dbv[i_ndbv], w);
      }
    }

    int nbtags[NBDISC] = {0};
    for (int ijet = 0; ijet < nt.njets; ++ijet) {
      double bdisc = nt.jet_bdisc[ijet];
      h_jet_bdisc[i_nbquarks[i]][i_nvtx]->Fill(bdisc, w);
      for (int i_nbdisc = 0; i_nbdisc < NBDISC; ++i_nbdisc) {
        if (bdisc >= bdisc_mins[i_nbdisc]) {
          ++nbtags[i_nbdisc];
        }
      }
    }

    for (int i_nbdisc = 0; i_nbdisc < NBDISC; ++i_nbdisc) {
      h_nbtags[i_nbquarks[i]][i_nvtx][i_nbdisc]->Fill(nbtags[i], w);

      for (int i_nbtags = 0; i_nbtags < NBTAGS; ++i_nbtags) {
        int btag_flavor_code = nbtags[i_nbdisc] >= nbtag_mins[i_nbtags] ? 1 : 0;
        h_btag_flavor_code[i_nbquarks[i]][i_nvtx][i_nbdisc][i_nbtags]->Fill(btag_flavor_code, w);
        h_btag_flavor_code_vs_bquark_flavor_code[i_nbquarks[i]][i_nvtx][i_nbdisc][i_nbtags]->Fill(bquark_flavor_code, btag_flavor_code, w);

        if (btag_flavor_code) {
          h_dbv_btag[i_nbquarks[i]][i_nvtx][0][i_nbdisc][i_nbtags]->Fill(dbv0, w);
        } else {
          h_dbv_nobtag[i_nbquarks[i]][i_nvtx][0][i_nbdisc][i_nbtags]->Fill(dbv0, w);
        }

        if (i_nvtx == 1) {
          for (int i_ndbv = 0; i_ndbv < NDBV; ++i_ndbv) {
            if (btag_flavor_code) {
              h_dbv_btag[i_nbquarks[i]][i_nvtx][i_ndbv][i_nbdisc][i_nbtags]->Fill(dbv[i_ndbv], w);
            } else {
              h_dbv_nobtag[i_nbquarks[i]][i_nvtx][i_ndbv][i_nbdisc][i_nbtags]->Fill(dbv[i_ndbv], w);
            }
          }
        }
      }
    }

    int nbquarks = nt.p_gen_bquarks->size();
    h_nbquarks[i_nbquarks[i]][i_nvtx]->Fill(nbquarks, w);

    for (int ivtx = 0; ivtx < 2; ++ivtx) {
      if (nt.nvtx == 1 && ivtx != 0) continue;

      int ntk_vtx = ivtx == 0 ? nt.ntk0 : nt.ntk1;
      int ntk_bquark = 0;
      for (int itk = 0; itk < ntk_vtx; ++itk) {
        TVector3 tkp = ivtx == 0 ? TVector3(nt.p_tk0_px->at(itk), nt.p_tk0_py->at(itk), nt.p_tk0_pz->at(itk))
                                 : TVector3(nt.p_tk1_px->at(itk), nt.p_tk1_py->at(itk), nt.p_tk1_pz->at(itk));
        double drmin = 1e9;
        for (int ibquark = 0; ibquark < nbquarks; ++ibquark) {
          double dr = reco::deltaR(tkp.Eta(), tkp.Phi(), nt.p_gen_bquarks->at(ibquark).Eta(), nt.p_gen_bquarks->at(ibquark).Phi());
          if (dr < drmin) {
            drmin = dr;
          }
        }
        h_drmin_tkp_bquark[i_nbquarks[i]][i_nvtx]->Fill(drmin, w);
        if (drmin < 0.4) {
          ++ntk_bquark;
        }
      }
      h_ntk_bquark[i_nbquarks[i]][i_nvtx]->Fill(ntk_bquark, w);
    }
  }

  return true;
}

int main(int argc, char** argv) {
  if (argc < 4) {
    fprintf(stderr, "usage: %s in_fn out_fn ntk\n", argv[0]);
    return 1;
  }

  const char* fn = argv[1];
  const char* out_fn = argv[2];
  const int ntk = atoi(argv[3]);

  if (!(ntk == 3 || ntk == 4 || ntk == 7 || ntk == 5)) {
    fprintf(stderr, "ntk must be one of 3,4,7,5\n");
    return 1;
  }

  TFile* in_f = TFile::Open(fn);
  TFile out_f(out_fn, "recreate");

  TH1::SetDefaultSumw2();

  out_f.mkdir("mfvWeight")->cd();
  in_f->Get("mfvWeight/h_sums")->Clone("h_sums");
  out_f.cd();

  book_hists(ntk);

  const char* tree_path =
    ntk == 3 ? "mfvMiniTreeNtk3/t" :
    ntk == 4 ? "mfvMiniTreeNtk4/t" :
    ntk == 7 ? "mfvMiniTreeNtk3or4/t" :
    ntk == 5 ? "mfvMiniTree/t" : 0;

  mfv::loop(fn, tree_path, analyze);

  out_f.cd();
  out_f.Write();
  out_f.Close();
}
