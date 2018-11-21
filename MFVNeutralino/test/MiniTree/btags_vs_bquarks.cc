#include <iostream>
#include "TCanvas.h"
#include "TFile.h"
#include "TH2.h"
#include "TTree.h"
#include "TVector2.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"

TH1F* h_1v_bquark_flavor_code = 0;
TH1F* h_1v_njets = 0;
TH1F* h_1v_jet_bdisc = 0;
const char* b_discriminator_wps[3] = {"loose", "medium", "tight"};
const double b_discriminator_mins[3] = {0.5803, 0.8838, 0.9693};
TH1F* h_1v_nbtags[3] = {0,0,0};
TH2F* h_1v_nbtags_vs_bquark_flavor_code[3] = {0,0,0};
TH1F* h_1v_btag1_flavor_code[3] = {0,0,0};
TH2F* h_1v_btag1_flavor_code_vs_bquark_flavor_code[3] = {0,0,0};
TH1F* h_1v_btag1_flavor_code_bquarks[3] = {0,0,0};
TH1F* h_1v_btag1_flavor_code_nobquarks[3] = {0,0,0};
TH1F* h_1v_bquark_flavor_code_btag1[3] = {0,0,0};
TH1F* h_1v_bquark_flavor_code_nobtag1[3] = {0,0,0};
TH1F* h_1v_btag2_flavor_code[3] = {0,0,0};
TH2F* h_1v_btag2_flavor_code_vs_bquark_flavor_code[3] = {0,0,0};
TH1F* h_1v_btag2_flavor_code_bquarks[3] = {0,0,0};
TH1F* h_1v_btag2_flavor_code_nobquarks[3] = {0,0,0};
TH1F* h_1v_bquark_flavor_code_btag2[3] = {0,0,0};
TH1F* h_1v_bquark_flavor_code_nobtag2[3] = {0,0,0};

TH1F* h_1v_dbv = 0;
TH1F* h_1v_dbv_bquarks = 0;
TH1F* h_1v_dbv_nobquarks = 0;
TH1F* h_1v_dbv_btag1[3] = {0,0,0};
TH1F* h_1v_dbv_nobtag1[3] = {0,0,0};
TH1F* h_1v_dbv_btag2[3] = {0,0,0};
TH1F* h_1v_dbv_nobtag2[3] = {0,0,0};

void book_hists(int ntk) {
  h_1v_bquark_flavor_code = new TH1F("h_1v_bquark_flavor_code", TString::Format("%d-track one-vertex events;bquark_flavor_code;Events", ntk), 2, 0, 2);
  h_1v_njets = new TH1F("h_1v_njets", TString::Format("%d-track one-vertex events;number of jets;Events", ntk), 40, 0, 40);
  h_1v_jet_bdisc = new TH1F("h_1v_jet_bdisc", TString::Format("%d-track one-vertex events;jet bdisc;Number of jets", ntk), 100, 0, 1);
  for (int i = 0; i < 3; ++i) {
    h_1v_nbtags[i] = new TH1F(TString::Format("h_1v_nbtags_%s", b_discriminator_wps[i]), TString::Format("%d-track one-vertex events;number of %s btags;Events", ntk, b_discriminator_wps[i]), 20, 0, 20);
    h_1v_nbtags_vs_bquark_flavor_code[i] = new TH2F(TString::Format("h_1v_nbtags_%s_vs_bquark_flavor_code", b_discriminator_wps[i]), TString::Format("%d-track one-vertex events;bquark_flavor_code;number of %s btags", ntk, b_discriminator_wps[i]), 2, 0, 2, 20, 0, 20);
    h_1v_btag1_flavor_code[i] = new TH1F(TString::Format("h_1v_%s_btag1_flavor_code", b_discriminator_wps[i]), TString::Format("%d-track one-vertex events;%s_btag1_flavor_code;Events", ntk, b_discriminator_wps[i]), 2, 0, 2);
    h_1v_btag1_flavor_code_vs_bquark_flavor_code[i] = new TH2F(TString::Format("h_1v_%s_btag1_flavor_code_vs_bquark_flavor_code", b_discriminator_wps[i]), TString::Format("%d-track one-vertex events;bquark_flavor_code;%s_btag1_flavor_code", ntk, b_discriminator_wps[i]), 2, 0, 2, 2, 0, 2);
    h_1v_btag1_flavor_code_bquarks[i] = new TH1F(TString::Format("h_1v_%s_btag1_flavor_code_bquarks", b_discriminator_wps[i]), TString::Format("%d-track one-vertex events with b quarks;%s_btag1_flavor_code;Events", ntk, b_discriminator_wps[i]), 2, 0, 2);
    h_1v_btag1_flavor_code_nobquarks[i] = new TH1F(TString::Format("h_1v_%s_btag1_flavor_code_nobquarks", b_discriminator_wps[i]), TString::Format("%d-track one-vertex events without b quarks;%s_btag1_flavor_code;Events", ntk, b_discriminator_wps[i]), 2, 0, 2);
    h_1v_bquark_flavor_code_btag1[i] = new TH1F(TString::Format("h_1v_bquark_flavor_code_%s_btag1", b_discriminator_wps[i]), TString::Format("%d-track one-vertex events with #geq1 %s btag;bquark_flavor_code;Events", ntk, b_discriminator_wps[i]), 2, 0, 2);
    h_1v_bquark_flavor_code_nobtag1[i] = new TH1F(TString::Format("h_1v_bquark_flavor_code_%s_nobtag1", b_discriminator_wps[i]), TString::Format("%d-track one-vertex events without #geq1 %s btag;bquark_flavor_code;Events", ntk, b_discriminator_wps[i]), 2, 0, 2);
    h_1v_btag2_flavor_code[i] = new TH1F(TString::Format("h_1v_%s_btag2_flavor_code", b_discriminator_wps[i]), TString::Format("%d-track one-vertex events;%s_btag2_flavor_code;Events", ntk, b_discriminator_wps[i]), 2, 0, 2);
    h_1v_btag2_flavor_code_vs_bquark_flavor_code[i] = new TH2F(TString::Format("h_1v_%s_btag2_flavor_code_vs_bquark_flavor_code", b_discriminator_wps[i]), TString::Format("%d-track one-vertex events;bquark_flavor_code;%s_btag2_flavor_code", ntk, b_discriminator_wps[i]), 2, 0, 2, 2, 0, 2);
    h_1v_btag2_flavor_code_bquarks[i] = new TH1F(TString::Format("h_1v_%s_btag2_flavor_code_bquarks", b_discriminator_wps[i]), TString::Format("%d-track one-vertex events with b quarks;%s_btag2_flavor_code;Events", ntk, b_discriminator_wps[i]), 2, 0, 2);
    h_1v_btag2_flavor_code_nobquarks[i] = new TH1F(TString::Format("h_1v_%s_btag2_flavor_code_nobquarks", b_discriminator_wps[i]), TString::Format("%d-track one-vertex events without b quarks;%s_btag2_flavor_code;Events", ntk, b_discriminator_wps[i]), 2, 0, 2);
    h_1v_bquark_flavor_code_btag2[i] = new TH1F(TString::Format("h_1v_bquark_flavor_code_%s_btag2", b_discriminator_wps[i]), TString::Format("%d-track one-vertex events with #geq2 %s btags;bquark_flavor_code;Events", ntk, b_discriminator_wps[i]), 2, 0, 2);
    h_1v_bquark_flavor_code_nobtag2[i] = new TH1F(TString::Format("h_1v_bquark_flavor_code_%s_nobtag2", b_discriminator_wps[i]), TString::Format("%d-track one-vertex events without #geq2 %s btags;bquark_flavor_code;Events", ntk, b_discriminator_wps[i]), 2, 0, 2);
  }

  h_1v_dbv = new TH1F("h_1v_dbv", TString::Format("%d-track one-vertex events;d_{BV} (cm);Events", ntk), 40, 0, 0.2);
  h_1v_dbv_bquarks = new TH1F("h_1v_dbv_bquarks", TString::Format("%d-track one-vertex events with b quarks;d_{BV} (cm);Events", ntk), 40, 0, 0.2);
  h_1v_dbv_nobquarks = new TH1F("h_1v_dbv_nobquarks", TString::Format("%d-track one-vertex events without b quarks;d_{BV} (cm);Events", ntk), 40, 0, 0.2);
  for (int i = 0; i < 3; ++i) {
    h_1v_dbv_btag1[i] = new TH1F(TString::Format("h_1v_dbv_%s_btag1", b_discriminator_wps[i]), TString::Format("%d-track one-vertex events with #geq1 %s btag;d_{BV} (cm);Events", ntk, b_discriminator_wps[i]), 40, 0, 0.2);
    h_1v_dbv_nobtag1[i] = new TH1F(TString::Format("h_1v_dbv_%s_nobtag1", b_discriminator_wps[i]), TString::Format("%d-track one-vertex events without #geq1 %s btag;d_{BV} (cm);Events", ntk, b_discriminator_wps[i]), 40, 0, 0.2);
    h_1v_dbv_btag2[i] = new TH1F(TString::Format("h_1v_dbv_%s_btag2", b_discriminator_wps[i]), TString::Format("%d-track one-vertex events with #geq2 %s btags;d_{BV} (cm);Events", ntk, b_discriminator_wps[i]), 40, 0, 0.2);
    h_1v_dbv_nobtag2[i] = new TH1F(TString::Format("h_1v_dbv_%s_nobtag2", b_discriminator_wps[i]), TString::Format("%d-track one-vertex events without #geq2 %s btags;d_{BV} (cm);Events", ntk, b_discriminator_wps[i]), 40, 0, 0.2);
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

    int nbtags[3] = {0,0,0};
    for (int ijet = 0; ijet < nt.njets; ++ijet) {
      double bdisc = nt.jet_bdisc[ijet];
      h_1v_jet_bdisc->Fill(bdisc, w);
      for (int i = 0; i < 3; ++i) {
        if (bdisc >= b_discriminator_mins[i]) {
          ++nbtags[i];
        }
      }
    }

    for (int i = 0; i < 3; ++i) {
      h_1v_nbtags[i]->Fill(nbtags[i], w);
      h_1v_nbtags_vs_bquark_flavor_code[i]->Fill(bquark_flavor_code, nbtags[i], w);

      int btag1_flavor_code = nbtags[i] >= 1 ? 1 : 0;
      h_1v_btag1_flavor_code[i]->Fill(btag1_flavor_code, w);
      h_1v_btag1_flavor_code_vs_bquark_flavor_code[i]->Fill(bquark_flavor_code, btag1_flavor_code, w);
      if (bquark_flavor_code) h_1v_btag1_flavor_code_bquarks[i]->Fill(btag1_flavor_code, w);
      if (!bquark_flavor_code) h_1v_btag1_flavor_code_nobquarks[i]->Fill(btag1_flavor_code, w);
      if (btag1_flavor_code) h_1v_bquark_flavor_code_btag1[i]->Fill(bquark_flavor_code, w);
      if (!btag1_flavor_code) h_1v_bquark_flavor_code_nobtag1[i]->Fill(bquark_flavor_code, w);

      int btag2_flavor_code = nbtags[i] >= 2 ? 1 : 0;
      h_1v_btag2_flavor_code[i]->Fill(btag2_flavor_code, w);
      h_1v_btag2_flavor_code_vs_bquark_flavor_code[i]->Fill(bquark_flavor_code, btag2_flavor_code, w);
      if (bquark_flavor_code) h_1v_btag2_flavor_code_bquarks[i]->Fill(btag2_flavor_code, w);
      if (!bquark_flavor_code) h_1v_btag2_flavor_code_nobquarks[i]->Fill(btag2_flavor_code, w);
      if (btag2_flavor_code) h_1v_bquark_flavor_code_btag2[i]->Fill(bquark_flavor_code, w);
      if (!btag2_flavor_code) h_1v_bquark_flavor_code_nobtag2[i]->Fill(bquark_flavor_code, w);

      if (btag1_flavor_code) h_1v_dbv_btag1[i]->Fill(dbv, w);
      if (!btag1_flavor_code) h_1v_dbv_nobtag1[i]->Fill(dbv, w);
      if (btag2_flavor_code) h_1v_dbv_btag2[i]->Fill(dbv, w);
      if (!btag2_flavor_code) h_1v_dbv_nobtag2[i]->Fill(dbv, w);
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
