#include "utils.h"

#include "TColor.h"
#include "TFile.h"
#include "TH1.h"
#include "TROOT.h"
#include "TStyle.h"
#include "TTree.h"

void root_setup() {
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
}

file_and_tree::file_and_tree(const char* in_fn) {
  f = TFile::Open(in_fn);
  if (!f || !f->IsOpen()) {
    fprintf(stderr, "could not open %s\n", in_fn);
    exit(1);
  }

  const char* tree_path = "tt/t";
  t = (TTree*)f->Get(tree_path);
  if (!t) {
    fprintf(stderr, "could not get tree %s from %s\n", tree_path, in_fn);
    exit(1);
  }

  nt.read_from_tree(t);
}

file_and_tree::~file_and_tree() {
  f->Close();
  delete f;
}
