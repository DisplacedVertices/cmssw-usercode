#include "utils.h"
#include <cassert>
#include "TColor.h"
#include "TFile.h"
#include "TH2.h"
#include "TROOT.h"
#include "TString.h"
#include "TStyle.h"
#include "TTree.h"
#include "Math/QuantFuncMathCore.h"

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

  t = (TTree*)f->Get("mfvK0s/t");
  if (!t) {
    fprintf(stderr, "could not get tree from %s\n", in_fn);
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
