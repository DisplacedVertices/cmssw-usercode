#include "TFile.h"
#include "TH1.h"
#include "TTree.h"
#include "JMTucker/MFVNeutralino/interface/MovedTracksNtuple.h"
#include "utils.h"
#include <iostream>

int main(int argc, char** argv) {
  if (argc < 6) {
    fprintf(stderr, "usage: checknjets.exe in.root out.root tree/path njets_req nbjets_req\n");
    return 1;
  }

  const char* in_fn  = argv[1];
  const char* out_fn  = argv[2];
  const char* tree_path = argv[3];
  const int njets_req = atoi(argv[4]);
  const int nbjets_req = atoi(argv[5]);

  file_and_tree fat(in_fn, out_fn, tree_path);
  TTree* t = fat.t;
  mfv::MovedTracksNtuple& nt = fat.nt;
  bool ok = true;

  fat.f_out->cd();
  TH1D* h_tau = new TH1D("h_tau", "", 10000, 0, 10);

  for (int j = 0, je = t->GetEntries(); j < je; ++j) {
    //if (j == 100000) break;
    if (t->LoadTree(j) < 0) break;
    if (t->GetEntry(j) <= 0) continue;
    if (j % 250000 == 0) {
      printf("\r%i/%i", j, je);
      fflush(stdout);
    }

    if (nt.npreseljets < njets_req || nt.npreselbjets < nbjets_req) {
      ok = false;
      std::cout << "bad event with " << +nt.npreseljets << "," << +nt.npreselbjets << ": " << nt.run << "," << nt.lumi << "," << nt.event << "\n";
    }

    h_tau->Fill(nt.move_tau());
  }

  printf(ok ? "\nkein problem\n" : "\nscheisse\n");
  return !ok;
}
