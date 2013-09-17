// alias rootg++ 'g++ `root-config --cflags --libs --glibs`'
// rootg++ -I../../plugins -std=c++0x CLASS.C && ./a.out

#include <assert.h>
#include <TCanvas.h>
#include <TFile.h>
#include <TH2.h>
#include <TROOT.h>
#include <TStyle.h>
#include <TTree.h>
#include "VertexNtuple.h"

void die_if_not(bool condition, const char* msg, ...) {
  if (condition)
    return;
  va_list args;
  va_start(args, msg);
  vfprintf(stderr, msg, args);
  va_end(args);
  assert(0);
}

struct Sample {
  static const char* file_dir;
  static const char* root_dir;
  const char* fn;
  int nevents;
  double xsec;
};

struct NtupleReader {
  Sample sample;
  TFile* file;
  TTree* tree;
  VertexNtuple nt;

  NtupleReader(const Sample& s)
    : sample(s)
  {
    file = new TFile(TString(s.file_dir) + s.fn);
    die_if_not(file && file->IsOpen(), "couldn't open file %s\n", s.fn);
    
    TDirectory* dir = (TDirectory*)file->Get(s.root_dir);
    die_if_not(dir, "couldn't get dir %s from %s\n", s.root_dir, s.fn);
    
    dir->GetObject("tree", tree);
    die_if_not(tree, "couldn't get tree \"tree\" from %s/%s\n", s.fn, s.root_dir);
    
    tree->SetMakeClass(1);
    nt.read(tree);
  }

  ~NtupleReader() {
    file->Close();
    delete file;
  }
};
