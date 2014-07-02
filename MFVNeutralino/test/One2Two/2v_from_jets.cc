// g++ -I $CMSSW_BASE/src -g -Wall `root-config --cflags --libs --glibs` ../../src/MiniNtuple.cc 2v_from_jets.cc -o 2v_from_jets.exe && ./2v_from_jets.exe

#include <cstdlib>
#include "TFile.h"
#include "TTree.h"
#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"

int main() {
  mfv::MiniNtuple nt;
  TFile* f = TFile::Open(TString::Format("minitree.root"));
  if (!f || !f->IsOpen()) {
    fprintf(stderr, "bad file");
    exit(1);
  }

  TTree* t = (TTree*)f->Get("mfvMiniTree/t");
  if (!t) {
    fprintf(stderr, "bad tree");
    exit(1);
  }
  
  mfv::read_from_tree(t, nt);
 
  for (int j = 0, je = t->GetEntries(); j < je; ++j) {
    if (t->LoadTree(j) < 0) break;
    if (t->GetEntry(j) <= 0) continue;

    printf("njets %i\n", nt.njets);
    for (int i = 0; i < nt.njets; ++i) {
      printf("jet #%i pt %f\n", i, nt.jet_pt[i]);
    }
  }
}
