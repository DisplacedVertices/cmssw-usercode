#include <iostream>
#include "TCanvas.h"
#include "TFile.h"
#include "TH2.h"
#include "TTree.h"
#include "TVector2.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"

const bool prints = false;

TH1D* h_nvtx = 0;
TH1D* h_dbv = 0;
TH1D* h_dvv = 0;

// analyze method is a callback passed to MiniNtuple::loop from main that is called once per tree entry
bool analyze(long long j, long long je, const mfv::MiniNtuple& nt) {
  if (prints) std::cout << "Entry " << j << "\n";

  double w = nt.weight; // modify as needed before filling hists

  // minitree is stupid and doesn't store past the first two vertices
  // can tighten cuts, but you won't ever be able to pull out the vertices past 2 in 3-vertex events
  // on background this should be negliglble, but this attempts to handle it as best as we can at this point

  std::vector<double> dbvs;
  const int ivtxe = std::min(int(nt.nvtx), 2);
  
  for (int ivtx = 0; ivtx < ivtxe; ++ivtx) {
    int ntracks = 0;
    bool genmatch = false;
    double dbv = 0;

    if (ivtx == 0) {
      ntracks = nt.ntk0;
      genmatch = nt.genmatch0;
      dbv = hypot(nt.x0, nt.y0);
    }
    else {
      ntracks = nt.ntk1;
      genmatch = nt.genmatch1;
      dbv = hypot(nt.x1, nt.y1);
    }

    if (dbv > 0.01) dbvs.push_back(dbv);
  }

  int nvtx = dbvs.size();
  if (nt.nvtx > 2) // deal with the aforementioned stupidity
    nvtx += int(nt.nvtx) - 2;
  h_nvtx->Fill(nvtx, w);

  if (dbvs.size() == 1)
    h_dbv->Fill(dbvs[0], w);
  else if (dbvs.size() == 2)
    h_dvv->Fill(hypot(nt.x0 - nt.x1, nt.y0 - nt.y1), w);

  return true;
}

int main(int argc, char** argv) {
  if (argc < 4) {
    fprintf(stderr, "usage: %s in_fn out_fn ntk\n", argv[0]);
    return 1;
  }

  // get args, can add any options you want

  const char* fn = argv[1];
  const char* out_fn = argv[2];
  const int ntk = atoi(argv[3]);

  if (!(ntk == 3 || ntk == 4 || ntk == 7 || ntk == 5)) {
    fprintf(stderr, "ntk must be one of 3,4,7,5\n");
    return 1;
  }

  TFile* in_f = TFile::Open(fn);
  TFile out_f(out_fn, "recreate");

  // setup root
  TH1::SetDefaultSumw2();

  // copy the normalization hist--if you don't read the whole tree by returning false in analyze above, you're screwed
  out_f.mkdir("mfvWeight")->cd();
  in_f->Get("mfvWeight/h_sums")->Clone("h_sums");
  out_f.cd();

  // book hists
  h_nvtx = new TH1D("h_nvtx", ";# of vertices;Events", 10, 0, 10);
  h_dbv = new TH1D("h_dbv", ";d_{BV} (cm);Events/20 #mum", 1250, 0, 2.5);
  h_dvv = new TH1D("h_dvv", ";d_{VV} (cm);Events/20 #mum", 2500, 0, 5.);

  const char* tree_path =
    ntk == 3 ? "mfvMiniTreeNtk3/t" :
    ntk == 4 ? "mfvMiniTreeNtk4/t" :
    ntk == 7 ? "mfvMiniTreeNtk3or4/t" :
    ntk == 5 ? "mfvMiniTree/t" : 0;
  if (prints) printf("fn %s out_fn %s ntk %i path %s\n", tree_path);

  mfv::loop(fn, tree_path, analyze);

  out_f.cd();

  // can do post loop processing of hists here

  out_f.Write();
  out_f.Close();
}
