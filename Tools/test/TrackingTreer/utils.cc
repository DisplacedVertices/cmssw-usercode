#include "utils.h"

#include "TColor.h"
#include "TFile.h"
#include "TH1.h"
#include "TROOT.h"
#include "TStyle.h"
#include "TTree.h"

void root_setup() {
  TH1::SetDefaultSumw2();
  gStyle->SetOptStat(1222222);
  gStyle->SetOptFit(2222);
  gStyle->SetPadTickX(1);
  gStyle->SetPadTickY(1);
  gROOT->ProcessLine("gErrorIgnoreLevel = 1001;");
}

file_and_tree::file_and_tree(const char* in_fn, const char* out_fn) {
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

  if (strncmp(out_fn, "n/a", 3) == 0)
    f_out = 0;
  else
    f_out = new TFile(out_fn, "recreate");
}

file_and_tree::~file_and_tree() {
  if (f_out) {
    f_out->Write();
    f_out->Close();
  }
  f->Close();

  delete f;
  delete f_out;
}
