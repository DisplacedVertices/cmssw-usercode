#include <iostream>
#include "TCanvas.h"
#include "TFile.h"
#include "TH2.h"
#include "TTree.h"
#include "TVector2.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"

const int NVTX = 2;
const char* vtx_names[NVTX] = {"one-vertex", "two-vertex"};

const int NBTAGS = 2;
const int nbtag_mins[NBTAGS] = {1, 2};

const int NBDISC = 3;
const char* bdisc_names[NBDISC] = {"loose", "medium", "tight"};
const double bdisc_mins[NBDISC] = {0.5803, 0.8838, 0.9693};

const int NDBV = 3;
const char* dbv_names[NDBV] = {"all", "longer", "shorter"};

TH1F* h_bquark_flavor_code[NVTX] = {0};
TH1F* h_njets[NVTX] = {0};
TH1F* h_jet_bdisc[NVTX] = {0};
TH1F* h_jet_bdisc_bquarks[NVTX] = {0};
TH1F* h_jet_bdisc_nobquarks[NVTX] = {0};

TH1F* h_nbtags[NVTX][NBDISC] = {{0}};
TH2F* h_nbtags_vs_bquark_flavor_code[NVTX][NBDISC] = {{0}};
TH1F* h_btag_flavor_code[NVTX][NBTAGS][NBDISC] = {{{0}}};
TH2F* h_btag_flavor_code_vs_bquark_flavor_code[NVTX][NBTAGS][NBDISC] = {{{0}}};
TH1F* h_btag_flavor_code_bquarks[NVTX][NBTAGS][NBDISC] = {{{0}}};
TH1F* h_btag_flavor_code_nobquarks[NVTX][NBTAGS][NBDISC] = {{{0}}};
TH1F* h_bquark_flavor_code_btag[NVTX][NBTAGS][NBDISC] = {{{0}}};
TH1F* h_bquark_flavor_code_nobtag[NVTX][NBTAGS][NBDISC] = {{{0}}};

TH1F* h_dbv[NVTX][NDBV] = {{0}};
TH1F* h_dbv_bquarks[NVTX][NDBV] = {{0}};
TH1F* h_dbv_nobquarks[NVTX][NDBV] = {{0}};
TH1F* h_dbv_btag[NVTX][NBTAGS][NBDISC][NDBV] = {{{{0}}}};
TH1F* h_dbv_btag_bquarks[NVTX][NBTAGS][NBDISC][NDBV] = {{{{0}}}};
TH1F* h_dbv_btag_nobquarks[NVTX][NBTAGS][NBDISC][NDBV] = {{{{0}}}};
TH1F* h_dbv_nobtag[NVTX][NBTAGS][NBDISC][NDBV] = {{{{0}}}};
TH1F* h_dbv_nobtag_bquarks[NVTX][NBTAGS][NBDISC][NDBV] = {{{{0}}}};
TH1F* h_dbv_nobtag_nobquarks[NVTX][NBTAGS][NBDISC][NDBV] = {{{{0}}}};

void book_hists(int ntk) {
  for (int k = 0; k < NVTX; ++k) {
    h_bquark_flavor_code[k] = new TH1F(TString::Format("h_%dv_bquark_flavor_code", k+1), TString::Format("%d-track %s events;bquark_flavor_code;Events", ntk, vtx_names[k]), 2, 0, 2);
    h_njets[k] = new TH1F(TString::Format("h_%dv_njets", k+1), TString::Format("%d-track %s events;number of jets;Events", ntk, vtx_names[k]), 40, 0, 40);
    h_jet_bdisc[k] = new TH1F(TString::Format("h_%dv_jet_bdisc", k+1), TString::Format("%d-track %s events;jet bdisc;Number of jets", ntk, vtx_names[k]), 100, 0, 1);
    h_jet_bdisc_bquarks[k] = new TH1F(TString::Format("h_%dv_jet_bdisc_bquarks", k+1), TString::Format("%d-track %s events with b quarks;jet bdisc;Number of jets", ntk, vtx_names[k]), 100, 0, 1);
    h_jet_bdisc_nobquarks[k] = new TH1F(TString::Format("h_%dv_jet_bdisc_nobquarks", k+1), TString::Format("%d-track %s events without b quarks;jet bdisc;Number of jets", ntk, vtx_names[k]), 100, 0, 1);

    for (int i = 0; i < NBDISC; ++i) {
      h_nbtags[k][i] = new TH1F(TString::Format("h_%dv_nbtags_%s", k+1, bdisc_names[i]), TString::Format("%d-track %s events;number of %s btags;Events", ntk, vtx_names[k], bdisc_names[i]), 20, 0, 20);
      h_nbtags_vs_bquark_flavor_code[k][i] = new TH2F(TString::Format("h_%dv_nbtags_%s_vs_bquark_flavor_code", k+1, bdisc_names[i]), TString::Format("%d-track %s events;bquark_flavor_code;number of %s btags", ntk, vtx_names[k], bdisc_names[i]), 2, 0, 2, 20, 0, 20);
      for (int j = 0; j < NBTAGS; ++j) {
        h_btag_flavor_code[k][j][i] = new TH1F(TString::Format("h_%dv_%d%s_btag_flavor_code", k+1, nbtag_mins[j], bdisc_names[i]), TString::Format("%d-track %s events;%d%s_btag_flavor_code;Events", ntk, vtx_names[k], nbtag_mins[j], bdisc_names[i]), 2, 0, 2);
        h_btag_flavor_code_vs_bquark_flavor_code[k][j][i] = new TH2F(TString::Format("h_%dv_%d%s_btag_flavor_code_vs_bquark_flavor_code", k+1, nbtag_mins[j], bdisc_names[i]), TString::Format("%d-track %s events;bquark_flavor_code;%d%s_btag_flavor_code", ntk, vtx_names[k], nbtag_mins[j], bdisc_names[i]), 2, 0, 2, 2, 0, 2);
        h_btag_flavor_code_bquarks[k][j][i] = new TH1F(TString::Format("h_%dv_%d%s_btag_flavor_code_bquarks", k+1, nbtag_mins[j], bdisc_names[i]), TString::Format("%d-track %s events with b quarks;%d%s_btag_flavor_code;Events", ntk, vtx_names[k], nbtag_mins[j], bdisc_names[i]), 2, 0, 2);
        h_btag_flavor_code_nobquarks[k][j][i] = new TH1F(TString::Format("h_%dv_%d%s_btag_flavor_code_nobquarks", k+1, nbtag_mins[j], bdisc_names[i]), TString::Format("%d-track %s events without b quarks;%d%s_btag_flavor_code;Events", ntk, vtx_names[k], nbtag_mins[j], bdisc_names[i]), 2, 0, 2);
        h_bquark_flavor_code_btag[k][j][i] = new TH1F(TString::Format("h_%dv_bquark_flavor_code_%d%s_btag", k+1, nbtag_mins[j], bdisc_names[i]), TString::Format("%d-track %s events with #geq%d %s btag;bquark_flavor_code;Events", ntk, vtx_names[k], nbtag_mins[j], bdisc_names[i]), 2, 0, 2);
        h_bquark_flavor_code_nobtag[k][j][i] = new TH1F(TString::Format("h_%dv_bquark_flavor_code_%d%s_nobtag", k+1, nbtag_mins[j], bdisc_names[i]), TString::Format("%d-track %s events without #geq%d %s btag;bquark_flavor_code;Events", ntk, vtx_names[k], nbtag_mins[j], bdisc_names[i]), 2, 0, 2);
      }
    }
  }

  for (int k = 0; k < NVTX; ++k) {
    for (int l = 0; l < NDBV; ++l) {
      if (k == 0 && l != 0) continue;
      h_dbv[k][l] = new TH1F(TString::Format("h_%dv_%s_dbv", k+1, dbv_names[l]), TString::Format("%d-track %s events;d_{BV} (cm);Events", ntk, vtx_names[k]), 40, 0, 0.2);
      h_dbv_bquarks[k][l] = new TH1F(TString::Format("h_%dv_%s_dbv_bquarks", k+1, dbv_names[l]), TString::Format("%d-track %s events with b quarks;d_{BV} (cm);Events", ntk, vtx_names[k]), 40, 0, 0.2);
      h_dbv_nobquarks[k][l] = new TH1F(TString::Format("h_%dv_%s_dbv_nobquarks", k+1, dbv_names[l]), TString::Format("%d-track %s events without b quarks;d_{BV} (cm);Events", ntk, vtx_names[k]), 40, 0, 0.2);
      for (int i = 0; i < NBDISC; ++i) {
        for (int j = 0; j < NBTAGS; ++j) {
          h_dbv_btag[k][j][i][l] = new TH1F(TString::Format("h_%dv_%s_dbv_%d%s_btag", k+1, dbv_names[l], nbtag_mins[j], bdisc_names[i]), TString::Format("%d-track %s events with #geq%d %s btag;d_{BV} (cm);Events", ntk, vtx_names[k], nbtag_mins[j], bdisc_names[i]), 40, 0, 0.2);
          h_dbv_btag_bquarks[k][j][i][l] = new TH1F(TString::Format("h_%dv_%s_dbv_%d%s_btag_bquarks", k+1, dbv_names[l], nbtag_mins[j], bdisc_names[i]), TString::Format("%d-track %s events with b quarks and with #geq%d %s btag;d_{BV} (cm);Events", ntk, vtx_names[k], nbtag_mins[j], bdisc_names[i]), 40, 0, 0.2);
          h_dbv_btag_nobquarks[k][j][i][l] = new TH1F(TString::Format("h_%dv_%s_dbv_%d%s_btag_nobquarks", k+1, dbv_names[l], nbtag_mins[j], bdisc_names[i]), TString::Format("%d-track %s events without b quarks and with #geq%d %s btag;d_{BV} (cm);Events", ntk, vtx_names[k], nbtag_mins[j], bdisc_names[i]), 40, 0, 0.2);
          h_dbv_nobtag[k][j][i][l] = new TH1F(TString::Format("h_%dv_%s_dbv_%d%s_nobtag", k+1, dbv_names[l], nbtag_mins[j], bdisc_names[i]), TString::Format("%d-track %s events without #geq%d %s btag;d_{BV} (cm);Events", ntk, vtx_names[k], nbtag_mins[j], bdisc_names[i]), 40, 0, 0.2);
          h_dbv_nobtag_bquarks[k][j][i][l] = new TH1F(TString::Format("h_%dv_%s_dbv_%d%s_nobtag_bquarks", k+1, dbv_names[l], nbtag_mins[j], bdisc_names[i]), TString::Format("%d-track %s events with b quarks and without #geq%d %s btag;d_{BV} (cm);Events", ntk, vtx_names[k], nbtag_mins[j], bdisc_names[i]), 40, 0, 0.2);
          h_dbv_nobtag_nobquarks[k][j][i][l] = new TH1F(TString::Format("h_%dv_%s_dbv_%d%s_nobtag_nobquarks", k+1, dbv_names[l], nbtag_mins[j], bdisc_names[i]), TString::Format("%d-track %s events without b quarks and without #geq%d %s btag;d_{BV} (cm);Events", ntk, vtx_names[k], nbtag_mins[j], bdisc_names[i]), 40, 0, 0.2);
        }
      }
    }
  }
}

bool analyze(long long j, long long je, const mfv::MiniNtuple& nt) {
  double w = nt.weight;

  if (nt.nvtx >= 1) {
    int k = nt.nvtx > NVTX ? NVTX-1 : nt.nvtx-1;

    int bquark_flavor_code = nt.gen_flavor_code == 2 ? 1 : 0;
    h_bquark_flavor_code[k]->Fill(bquark_flavor_code, w);
    h_njets[k]->Fill(nt.njets, w);

    double dbv0 = hypot(nt.x0, nt.y0);
    h_dbv[k][0]->Fill(dbv0, w);
    if (bquark_flavor_code) h_dbv_bquarks[k][0]->Fill(dbv0, w);
    if (!bquark_flavor_code) h_dbv_nobquarks[k][0]->Fill(dbv0, w);

    double dbv1 = hypot(nt.x1, nt.y1);
    const double dbv[NDBV] = {dbv1, dbv0 >= dbv1 ? dbv0 : dbv1, dbv0 >= dbv1 ? dbv1 : dbv0};
    if (nt.nvtx >= 2) {
      for (int l = 0; l < NDBV; ++l) {
        h_dbv[k][l]->Fill(dbv[l], w);
        if (bquark_flavor_code) h_dbv_bquarks[k][l]->Fill(dbv[l], w);
        if (!bquark_flavor_code) h_dbv_nobquarks[k][l]->Fill(dbv[l], w);
      }
    }

    int nbtags[NBDISC] = {0};
    for (int ijet = 0; ijet < nt.njets; ++ijet) {
      double bdisc = nt.jet_bdisc[ijet];
      h_jet_bdisc[k]->Fill(bdisc, w);
      if (bquark_flavor_code) h_jet_bdisc_bquarks[k]->Fill(bdisc, w);
      if (!bquark_flavor_code) h_jet_bdisc_nobquarks[k]->Fill(bdisc, w);
      for (int i = 0; i < NBDISC; ++i) {
        if (bdisc >= bdisc_mins[i]) {
          ++nbtags[i];
        }
      }
    }

    for (int i = 0; i < NBDISC; ++i) {
      h_nbtags[k][i]->Fill(nbtags[i], w);
      h_nbtags_vs_bquark_flavor_code[k][i]->Fill(bquark_flavor_code, nbtags[i], w);

      for (int j = 0; j < NBTAGS; ++j) {
        int btag_flavor_code = nbtags[i] >= nbtag_mins[j] ? 1 : 0;
        h_btag_flavor_code[k][j][i]->Fill(btag_flavor_code, w);
        h_btag_flavor_code_vs_bquark_flavor_code[k][j][i]->Fill(bquark_flavor_code, btag_flavor_code, w);
        if (bquark_flavor_code) h_btag_flavor_code_bquarks[k][j][i]->Fill(btag_flavor_code, w);
        if (!bquark_flavor_code) h_btag_flavor_code_nobquarks[k][j][i]->Fill(btag_flavor_code, w);
        if (btag_flavor_code) h_bquark_flavor_code_btag[k][j][i]->Fill(bquark_flavor_code, w);
        if (!btag_flavor_code) h_bquark_flavor_code_nobtag[k][j][i]->Fill(bquark_flavor_code, w);

        if (btag_flavor_code) h_dbv_btag[k][j][i][0]->Fill(dbv0, w);
        if (btag_flavor_code && bquark_flavor_code) h_dbv_btag_bquarks[k][j][i][0]->Fill(dbv0, w);
        if (btag_flavor_code && !bquark_flavor_code) h_dbv_btag_nobquarks[k][j][i][0]->Fill(dbv0, w);
        if (!btag_flavor_code) h_dbv_nobtag[k][j][i][0]->Fill(dbv0, w);
        if (!btag_flavor_code && bquark_flavor_code) h_dbv_nobtag_bquarks[k][j][i][0]->Fill(dbv0, w);
        if (!btag_flavor_code && !bquark_flavor_code) h_dbv_nobtag_nobquarks[k][j][i][0]->Fill(dbv0, w);

        if (nt.nvtx >= 2) {
          for (int l = 0; l < NDBV; ++l) {
            if (btag_flavor_code) h_dbv_btag[k][j][i][l]->Fill(dbv[l], w);
            if (btag_flavor_code && bquark_flavor_code) h_dbv_btag_bquarks[k][j][i][l]->Fill(dbv[l], w);
            if (btag_flavor_code && !bquark_flavor_code) h_dbv_btag_nobquarks[k][j][i][l]->Fill(dbv[l], w);
            if (!btag_flavor_code) h_dbv_nobtag[k][j][i][l]->Fill(dbv[l], w);
            if (!btag_flavor_code && bquark_flavor_code) h_dbv_nobtag_bquarks[k][j][i][l]->Fill(dbv[l], w);
            if (!btag_flavor_code && !bquark_flavor_code) h_dbv_nobtag_nobquarks[k][j][i][l]->Fill(dbv[l], w);
          }
        }
      }
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
