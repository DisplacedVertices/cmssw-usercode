#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include "TFile.h"
#include "TH1.h"
#include "TTree.h"
#include "TVector2.h"
#include "JMTucker/Tools/interface/TrackingTree.h"
#include "utils.h"

int main(int argc, char** argv) {
  if (argc < 3) {
    fprintf(stderr, "usage: hists.exe files_in.txt out.root\n");
    return 1;
  }

  const char* files_in_fn = argv[1];
  const char* out_fn = argv[2];

  root_setup();

  std::vector<std::string> fns;
  std::ifstream files_in(files_in_fn);
  std::string fn_tmp;
  while (files_in >> fn_tmp)
    fns.push_back(fn_tmp);
  printf("will read %lu files:\n", fns.size());
  
  TFile* f_out = new TFile(out_fn, "recreate");

  TH1F* h_norm = new TH1F("h_norm", "", 1, 0, 1);
  TH1F* h_npu = new TH1F("h_npu", "", 50, 0, 50);

  for (const std::string& fn : fns) {
    std::cout << fn << std::endl;
    file_and_tree fat(fn.c_str());
    TrackingTree& nt = fat.nt;

    h_norm->Fill(0.5, ((TH1F*)fat.f->Get("mcStat/h_sums"))->GetBinContent(1));

    long j = 0, je = fat.t->GetEntries();
    for (; j < je; ++j) {
      if (fat.t->LoadTree(j) < 0) break;
      if (fat.t->GetEntry(j) <= 0) continue;
      if (j % 2000 == 0) {
        printf("\r%li/%li", j, je);
        fflush(stdout);
      }

      h_npu->Fill(nt.npu);
    }

    printf("\r%li/%li\n", j, je);
  }

  f_out->Write();
  f_out->Close();
  delete f_out;
}
