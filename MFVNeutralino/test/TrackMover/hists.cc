#include <cmath>
#include "TColor.h"
#include "TFile.h"
#include "TH1.h"
#include "TROOT.h"
#include "TStyle.h"
#include "TTree.h"
#include "JMTucker/MFVNeutralino/interface/MovedTracksNtuple.h"

template <typename T>
T mag(T x, T y, T z=0) {
  return sqrt(x*x + y*y + z*z);
}

int main(int argc, char** argv) {
  if (argc < 3) {
    fprintf(stderr, "usage: hists.exe in.root out.root\n");
    return 1;
  }

  const char* in_fn  = argv[1];
  const char* out_fn = argv[2];
  const int njets_req = 2;
  const int nbjets_req = 1;

  gROOT->SetStyle("Plain");
  gStyle->SetPalette(1);
  gStyle->SetFillColor(0);
  gStyle->SetOptDate(0);
  gStyle->SetOptStat(1222222);
  gStyle->SetOptFit(2222);
  gStyle->SetPadTickX(1);
  gStyle->SetPadTickY(1);
  gStyle->SetMarkerSize(.1);
  gStyle->SetMarkerStyle(8);
  gStyle->SetGridStyle(3);
  gROOT->ProcessLine("gErrorIgnoreLevel = 1001;");
  double palinfo[4][5] = {{0,0,0,1,1},{0,1,1,1,0},{1,1,0,0,0},{0,0.25,0.5,0.75,1}};
  TColor::CreateGradientColorTable(5, palinfo[3], palinfo[0], palinfo[1], palinfo[2], 500);
  gStyle->SetNumberContours(500);
  TH1::SetDefaultSumw2();

  TFile* f = new TFile(in_fn);
  if (!f || !f->IsOpen()) {
    fprintf(stderr, "could not open %s\n", in_fn);
    return 1;
  }

  const char* tree_path = "mfvMovedTree/t";
  TTree* t = (TTree*)f->Get(tree_path);
  if (!t) {
    fprintf(stderr, "could not get tree %s from %s\n", tree_path, in_fn);
    return 1;
  }

  mfv::MovedTracksNtuple nt;
  nt.read_from_tree(t);

  TFile* f_out = new TFile(out_fn, "recreate");

  //TH1F* h_ = new TH1F("h_", ";;events/", );
  TH1F* h_weight = new TH1F("h_weight", ";weight;events/0.01", 200, 0, 2);
  TH1F* h_npu = new TH1F("h_npu", ";# PU;events/1", 100, 0, 100);
  TH1F* h_npv = new TH1F("h_npv", ";# PV;events/1", 100, 0, 100);
  TH1F* h_pvx = new TH1F("h_pvx", ";PV x (cm);events/1.5 #mum", 200, -0.015, 0.015);
  TH1F* h_pvy = new TH1F("h_pvy", ";PV y (cm);events/1.5 #mum", 200, -0.015, 0.015);
  TH1F* h_pvz = new TH1F("h_pvz", ";PV z (cm);events/0.24 cm", 200, -24, 24);
  TH1F* h_pvdist2 = new TH1F("h_pvdist2", ";movement 2-dist;events/0.01 cm", 200, 0, 2);
  TH1F* h_pvdist3 = new TH1F("h_pvdist3", ";movement 3-dist;events/0.01 cm", 200, 0, 2);

  for (int j = 0, je = t->GetEntries(); j < je; ++j) {
    if (t->LoadTree(j) < 0) break;
    if (t->GetEntry(j) <= 0) continue;
    if (j % 250000 == 0) {
      printf("\r%i/%i", j, je);
      fflush(stdout);
    }

    if (nt.npreseljets < njets_req || nt.npreselbjets < nbjets_req)
      continue;

    const float w = nt.weight;

    h_weight->Fill(w);
    h_npu->Fill(nt.npu, w);
    h_npv->Fill(nt.npv, w);
    h_pvx->Fill(nt.pvx, w);
    h_pvy->Fill(nt.pvy, w);
    h_pvz->Fill(nt.pvz, w);

    const double pvdist2 = mag(nt.move_x - nt.pvx,
                               nt.move_y - nt.pvy);
    const double pvdist3 = mag(nt.move_x - nt.pvx,
                               nt.move_y - nt.pvy,
                               nt.move_z - nt.pvz);

    h_pvdist2->Fill(pvdist2, w);
    h_pvdist3->Fill(pvdist3, w);
  }

  printf("\r                                \n");

  f_out->Write();
  f_out->Close();
  f->Close();

  delete f;
  delete f_out;
}
