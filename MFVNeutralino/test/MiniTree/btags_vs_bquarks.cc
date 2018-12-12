#include <iostream>
#include "TCanvas.h"
#include "TFile.h"
#include "TH2.h"
#include "TTree.h"
#include "TVector2.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"

const int NBTAGS = 2;
const int NBDISC = 3;

TH1F* h_1v_bquark_flavor_code = 0;
TH1F* h_1v_njets = 0;
TH1F* h_1v_jet_bdisc = 0;
TH1F* h_1v_jet_bdisc_bquarks = 0;
TH1F* h_1v_jet_bdisc_nobquarks = 0;

const char* b_discriminator_wps[NBDISC] = {"loose", "medium", "tight"};
const double b_discriminator_mins[NBDISC] = {0.5803, 0.8838, 0.9693};
TH1F* h_1v_nbtags[NBDISC] = {0};
TH2F* h_1v_nbtags_vs_bquark_flavor_code[NBDISC] = {0};
TH1F* h_1v_btag_flavor_code[NBTAGS][NBDISC] = {{0}};
TH2F* h_1v_btag_flavor_code_vs_bquark_flavor_code[NBTAGS][NBDISC] = {{0}};
TH1F* h_1v_btag_flavor_code_bquarks[NBTAGS][NBDISC] = {{0}};
TH1F* h_1v_btag_flavor_code_nobquarks[NBTAGS][NBDISC] = {{0}};
TH1F* h_1v_bquark_flavor_code_btag[NBTAGS][NBDISC] = {{0}};
TH1F* h_1v_bquark_flavor_code_nobtag[NBTAGS][NBDISC] = {{0}};

TH1F* h_1v_dbv = 0;
TH1F* h_1v_dbv_bquarks = 0;
TH1F* h_1v_dbv_nobquarks = 0;
TH1F* h_1v_dbv_btag[NBTAGS][NBDISC] = {{0}};
TH1F* h_1v_dbv_btag_bquarks[NBTAGS][NBDISC] = {{0}};
TH1F* h_1v_dbv_btag_nobquarks[NBTAGS][NBDISC] = {{0}};
TH1F* h_1v_dbv_nobtag[NBTAGS][NBDISC] = {{0}};
TH1F* h_1v_dbv_nobtag_bquarks[NBTAGS][NBDISC] = {{0}};
TH1F* h_1v_dbv_nobtag_nobquarks[NBTAGS][NBDISC] = {{0}};

void book_hists(int ntk) {
  h_1v_bquark_flavor_code = new TH1F("h_1v_bquark_flavor_code", TString::Format("%d-track one-vertex events;bquark_flavor_code;Events", ntk), 2, 0, 2);
  h_1v_njets = new TH1F("h_1v_njets", TString::Format("%d-track one-vertex events;number of jets;Events", ntk), 40, 0, 40);
  h_1v_jet_bdisc = new TH1F("h_1v_jet_bdisc", TString::Format("%d-track one-vertex events;jet bdisc;Number of jets", ntk), 100, 0, 1);
  h_1v_jet_bdisc_bquarks = new TH1F("h_1v_jet_bdisc_bquarks", TString::Format("%d-track one-vertex events with b quarks;jet bdisc;Number of jets", ntk), 100, 0, 1);
  h_1v_jet_bdisc_nobquarks = new TH1F("h_1v_jet_bdisc_nobquarks", TString::Format("%d-track one-vertex events without b quarks;jet bdisc;Number of jets", ntk), 100, 0, 1);

  for (int i = 0; i < NBDISC; ++i) {
    h_1v_nbtags[i] = new TH1F(TString::Format("h_1v_nbtags_%s", b_discriminator_wps[i]), TString::Format("%d-track one-vertex events;number of %s btags;Events", ntk, b_discriminator_wps[i]), 20, 0, 20);
    h_1v_nbtags_vs_bquark_flavor_code[i] = new TH2F(TString::Format("h_1v_nbtags_%s_vs_bquark_flavor_code", b_discriminator_wps[i]), TString::Format("%d-track one-vertex events;bquark_flavor_code;number of %s btags", ntk, b_discriminator_wps[i]), 2, 0, 2, 20, 0, 20);
    for (int j = 0; j < NBTAGS; ++j) {
      h_1v_btag_flavor_code[j][i] = new TH1F(TString::Format("h_1v_%d%s_btag_flavor_code", j+1, b_discriminator_wps[i]), TString::Format("%d-track one-vertex events;%d%s_btag_flavor_code;Events", ntk, j+1, b_discriminator_wps[i]), 2, 0, 2);
      h_1v_btag_flavor_code_vs_bquark_flavor_code[j][i] = new TH2F(TString::Format("h_1v_%d%s_btag_flavor_code_vs_bquark_flavor_code", j+1, b_discriminator_wps[i]), TString::Format("%d-track one-vertex events;bquark_flavor_code;%d%s_btag_flavor_code", ntk, j+1, b_discriminator_wps[i]), 2, 0, 2, 2, 0, 2);
      h_1v_btag_flavor_code_bquarks[j][i] = new TH1F(TString::Format("h_1v_%d%s_btag_flavor_code_bquarks", j+1, b_discriminator_wps[i]), TString::Format("%d-track one-vertex events with b quarks;%d%s_btag_flavor_code;Events", ntk, j+1, b_discriminator_wps[i]), 2, 0, 2);
      h_1v_btag_flavor_code_nobquarks[j][i] = new TH1F(TString::Format("h_1v_%d%s_btag_flavor_code_nobquarks", j+1, b_discriminator_wps[i]), TString::Format("%d-track one-vertex events without b quarks;%d%s_btag_flavor_code;Events", ntk, j+1, b_discriminator_wps[i]), 2, 0, 2);
      h_1v_bquark_flavor_code_btag[j][i] = new TH1F(TString::Format("h_1v_bquark_flavor_code_%d%s_btag", j+1, b_discriminator_wps[i]), TString::Format("%d-track one-vertex events with #geq%d %s btag;bquark_flavor_code;Events", ntk, j+1, b_discriminator_wps[i]), 2, 0, 2);
      h_1v_bquark_flavor_code_nobtag[j][i] = new TH1F(TString::Format("h_1v_bquark_flavor_code_%d%s_nobtag", j+1, b_discriminator_wps[i]), TString::Format("%d-track one-vertex events without #geq%d %s btag;bquark_flavor_code;Events", ntk, j+1, b_discriminator_wps[i]), 2, 0, 2);
    }
  }

  h_1v_dbv = new TH1F("h_1v_dbv", TString::Format("%d-track one-vertex events;d_{BV} (cm);Events", ntk), 40, 0, 0.2);
  h_1v_dbv_bquarks = new TH1F("h_1v_dbv_bquarks", TString::Format("%d-track one-vertex events with b quarks;d_{BV} (cm);Events", ntk), 40, 0, 0.2);
  h_1v_dbv_nobquarks = new TH1F("h_1v_dbv_nobquarks", TString::Format("%d-track one-vertex events without b quarks;d_{BV} (cm);Events", ntk), 40, 0, 0.2);
  for (int i = 0; i < NBDISC; ++i) {
    for (int j = 0; j < NBTAGS; ++j) {
      h_1v_dbv_btag[j][i] = new TH1F(TString::Format("h_1v_dbv_%d%s_btag", j+1, b_discriminator_wps[i]), TString::Format("%d-track one-vertex events with #geq%d %s btag;d_{BV} (cm);Events", ntk, j+1, b_discriminator_wps[i]), 40, 0, 0.2);
      h_1v_dbv_btag_bquarks[j][i] = new TH1F(TString::Format("h_1v_dbv_%d%s_btag_bquarks", j+1, b_discriminator_wps[i]), TString::Format("%d-track one-vertex events with b quarks and with #geq%d %s btag;d_{BV} (cm);Events", ntk, j+1, b_discriminator_wps[i]), 40, 0, 0.2);
      h_1v_dbv_btag_nobquarks[j][i] = new TH1F(TString::Format("h_1v_dbv_%d%s_btag_nobquarks", j+1, b_discriminator_wps[i]), TString::Format("%d-track one-vertex events without b quarks and with #geq%d %s btag;d_{BV} (cm);Events", ntk, j+1, b_discriminator_wps[i]), 40, 0, 0.2);
      h_1v_dbv_nobtag[j][i] = new TH1F(TString::Format("h_1v_dbv_%d%s_nobtag", j+1, b_discriminator_wps[i]), TString::Format("%d-track one-vertex events without #geq%d %s btag;d_{BV} (cm);Events", ntk, j+1, b_discriminator_wps[i]), 40, 0, 0.2);
      h_1v_dbv_nobtag_bquarks[j][i] = new TH1F(TString::Format("h_1v_dbv_%d%s_nobtag_bquarks", j+1, b_discriminator_wps[i]), TString::Format("%d-track one-vertex events with b quarks and without #geq%d %s btag;d_{BV} (cm);Events", ntk, j+1, b_discriminator_wps[i]), 40, 0, 0.2);
      h_1v_dbv_nobtag_nobquarks[j][i] = new TH1F(TString::Format("h_1v_dbv_%d%s_nobtag_nobquarks", j+1, b_discriminator_wps[i]), TString::Format("%d-track one-vertex events without b quarks and without #geq%d %s btag;d_{BV} (cm);Events", ntk, j+1, b_discriminator_wps[i]), 40, 0, 0.2);
    }
  }
}

bool analyze(long long j, long long je, const mfv::MiniNtuple& nt) {
  double w = nt.weight;

  if (nt.nvtx == 1) {
    int bquark_flavor_code = nt.gen_flavor_code == 2 ? 1 : 0;
    h_1v_bquark_flavor_code->Fill(bquark_flavor_code, w);
    h_1v_njets->Fill(nt.njets, w);

    double dbv = hypot(nt.x0, nt.y0);
    h_1v_dbv->Fill(dbv, w);
    if (bquark_flavor_code) h_1v_dbv_bquarks->Fill(dbv, w);
    if (!bquark_flavor_code) h_1v_dbv_nobquarks->Fill(dbv, w);

    int nbtags[NBDISC] = {0};
    for (int ijet = 0; ijet < nt.njets; ++ijet) {
      double bdisc = nt.jet_bdisc[ijet];
      h_1v_jet_bdisc->Fill(bdisc, w);
      if (bquark_flavor_code) h_1v_jet_bdisc_bquarks->Fill(bdisc, w);
      if (!bquark_flavor_code) h_1v_jet_bdisc_nobquarks->Fill(bdisc, w);
      for (int i = 0; i < NBDISC; ++i) {
        if (bdisc >= b_discriminator_mins[i]) {
          ++nbtags[i];
        }
      }
    }

    for (int i = 0; i < NBDISC; ++i) {
      h_1v_nbtags[i]->Fill(nbtags[i], w);
      h_1v_nbtags_vs_bquark_flavor_code[i]->Fill(bquark_flavor_code, nbtags[i], w);

      for (int j = 0; j < NBTAGS; ++j) {
        int btag_flavor_code = nbtags[i] >= j+1 ? 1 : 0;
        h_1v_btag_flavor_code[j][i]->Fill(btag_flavor_code, w);
        h_1v_btag_flavor_code_vs_bquark_flavor_code[j][i]->Fill(bquark_flavor_code, btag_flavor_code, w);
        if (bquark_flavor_code) h_1v_btag_flavor_code_bquarks[j][i]->Fill(btag_flavor_code, w);
        if (!bquark_flavor_code) h_1v_btag_flavor_code_nobquarks[j][i]->Fill(btag_flavor_code, w);
        if (btag_flavor_code) h_1v_bquark_flavor_code_btag[j][i]->Fill(bquark_flavor_code, w);
        if (!btag_flavor_code) h_1v_bquark_flavor_code_nobtag[j][i]->Fill(bquark_flavor_code, w);

        if (btag_flavor_code) h_1v_dbv_btag[j][i]->Fill(dbv, w);
        if (btag_flavor_code && bquark_flavor_code) h_1v_dbv_btag_bquarks[j][i]->Fill(dbv, w);
        if (btag_flavor_code && !bquark_flavor_code) h_1v_dbv_btag_nobquarks[j][i]->Fill(dbv, w);
        if (!btag_flavor_code) h_1v_dbv_nobtag[j][i]->Fill(dbv, w);
        if (!btag_flavor_code && bquark_flavor_code) h_1v_dbv_nobtag_bquarks[j][i]->Fill(dbv, w);
        if (!btag_flavor_code && !bquark_flavor_code) h_1v_dbv_nobtag_nobquarks[j][i]->Fill(dbv, w);
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
