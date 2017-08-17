#include "utils.h"
#include <cassert>
#include "TColor.h"
#include "TFile.h"
#include "TH1.h"
#include "TROOT.h"
#include "TString.h"
#include "TStyle.h"
#include "TTree.h"
#include "Math/QuantFuncMathCore.h"

interval clopper_pearson_binom(const double n_on, const double n_tot, const double alpha, const bool equal_tailed) {
  const double alpha_min = equal_tailed ? alpha/2 : alpha;

  interval i;
  i.success = !(n_on == 0 && n_tot == 0);
  i.value = n_on / n_tot;
  i.lower = 0;
  i.upper = 1;

  if (n_on > 0)         i.lower = ROOT::Math::beta_quantile  (alpha_min, n_on,     n_tot - n_on + 1);
  if (n_tot - n_on > 0) i.upper = ROOT::Math::beta_quantile_c(alpha_min, n_on + 1, n_tot - n_on);

  return i;
}

numden::numden(const char* name, const char* title, int nbins, double xlo, double xhi)
  : num(new TH1D(TString::Format("%s_num", name), title, nbins, xlo, xhi)),
    den(new TH1D(TString::Format("%s_den", name), title, nbins, xlo, xhi))
{}

numdens::numdens(const char* c)
  : common(c + std::string("_"))
{}

void numdens::book(int key, const char* name, const char* title, int nbins, double xlo, double xhi) {
  m.insert(std::make_pair(key, numden((common + name).c_str(), title, nbins, xlo, xhi)));
}

numden& numdens::operator()(int k) {
  return m[k];
}

void root_setup() {
  TH1::SetDefaultSumw2();
  gStyle->SetOptStat(1222222);
  gStyle->SetOptFit(2222);
  gStyle->SetPadTickX(1);
  gStyle->SetPadTickY(1);
  gROOT->ProcessLine("gErrorIgnoreLevel = 1001;");
}

file_and_tree::file_and_tree(const char* in_fn, const char* out_fn, int njets, int nbjets) {
  f = TFile::Open(in_fn);
  if (!f || !f->IsOpen()) {
    fprintf(stderr, "could not open %s\n", in_fn);
    exit(1);
  }

  char tree_path[128] = "mfvMovedTree/t";
  if (njets != -1)
    snprintf(tree_path, 128, "mfvMovedTree%i%i/t", njets, nbjets);
  t = (TTree*)f->Get(tree_path);
  if (!t) {
    fprintf(stderr, "could not get tree %s from %s\n", tree_path, in_fn);
    exit(1);
  }

  nt.read_from_tree(t);

  f_out = new TFile(out_fn, "recreate");
}

file_and_tree::~file_and_tree() {
  f_out->Write();
  f_out->Close();
  f->Close();

  delete f;
  delete f_out;
}
