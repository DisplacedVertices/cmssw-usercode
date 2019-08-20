#include <iostream>
#include "TCanvas.h"
#include "TFile.h"
#include "TH2.h"
#include "TTree.h"
#include "TVector2.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"

const bool prints = false;

TH1D* h_nvtx = 0;
TH1D* h_dbv = 0;

// FIXME probably put all of these into a map
TH1D* h_dbv_all = 0;
TH1D* h_dbv_all_coarse = 0;
TH1D* h_dbv_HT = 0;
TH1D* h_dbv_HT_coarse = 0;
TH1D* h_dbv_Bjet = 0;
TH1D* h_dbv_Bjet_coarse = 0;
TH1D* h_dbv_DisplacedDijet = 0;
TH1D* h_dbv_DisplacedDijet_coarse = 0;
TH1D* h_dbv_passHT_failBjet = 0;
TH1D* h_dbv_passHT_failBjet_coarse = 0;
TH1D* h_dbv_failHT_passBjet = 0;
TH1D* h_dbv_failHT_passBjet_coarse = 0;

TH1D* h_dvv_all = 0;
TH1D* h_dvv_all_coarse = 0;
TH1D* h_dvv_HT = 0;
TH1D* h_dvv_HT_coarse = 0;
TH1D* h_dvv_Bjet = 0;
TH1D* h_dvv_Bjet_coarse = 0;
TH1D* h_dvv_DisplacedDijet = 0;
TH1D* h_dvv_DisplacedDijet_coarse = 0;
TH1D* h_dvv_passHT_failBjet = 0;
TH1D* h_dvv_passHT_failBjet_coarse = 0;
TH1D* h_dvv_failHT_passBjet = 0;
TH1D* h_dvv_failHT_passBjet_coarse = 0;

bool pass_hlt(const mfv::MiniNtuple& nt, size_t i){
  return bool((nt.pass_hlt >> i) & 1);
}

// analyze method is a callback passed to MiniNtuple::loop from main that is called once per tree entry
bool analyze(long long j, long long je, const mfv::MiniNtuple& nt) {
  if (prints) std::cout << "Entry " << j << "\n";

  bool passesHTTrigger = pass_hlt(nt, mfv::b_HLT_PFHT1050);

  bool passesBjetTrigger = pass_hlt(nt, mfv::b_HLT_DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_p33) 
                        || pass_hlt(nt, mfv::b_HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0) 
                        || pass_hlt(nt, mfv::b_HLT_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2) 
                        || pass_hlt(nt, mfv::b_HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2) 
                        || pass_hlt(nt, mfv::b_HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5);

  bool passesDisplacedDijetTrigger = pass_hlt(nt, mfv::b_HLT_HT430_DisplacedDijet40_DisplacedTrack); // ignore the other one with a higher HT threshold for now...

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

  if (dbvs.size() == 1){
    h_dbv->Fill(dbvs[0], w);

    h_dbv_all->Fill(dbvs[0], w);
    h_dbv_all_coarse->Fill(dbvs[0], w);

    // HT trigger
    if(passesHTTrigger && nt.njets >= 4 && nt.ht() > 1200){
      h_dbv_HT->Fill(dbvs[0], w);
      h_dbv_HT_coarse->Fill(dbvs[0], w);
    }
    // Bjet trigger - should think about whether we can be more aggressive with the offline HT threshold
    // e.g. from https://twiki.cern.ch/twiki/pub/CMSPublic/HighLevelTriggerRunIIResults/SUSY2015_trig-Ele15_HT350__var-HT.png
    // it looks like the HT350 leg is 95% efficient already at ~400 GeV
    if(passesBjetTrigger && nt.njets >= 4 && nt.ht() > 600){
      h_dbv_Bjet->Fill(dbvs[0], w);
      h_dbv_Bjet_coarse->Fill(dbvs[0], w);
    }
    // Displaced Dijet trigger
    if(passesDisplacedDijetTrigger && nt.njets >= 4 && nt.ht() > 600){
      h_dbv_DisplacedDijet->Fill(dbvs[0], w);
      h_dbv_DisplacedDijet_coarse->Fill(dbvs[0], w);
    }
    // pass HT trigger fail Bjet trigger (to study the shape differences)
    if(passesHTTrigger && !passesBjetTrigger && nt.njets >= 4 && nt.ht() > 1200){
      h_dbv_passHT_failBjet->Fill(dbvs[0], w);
      h_dbv_passHT_failBjet_coarse->Fill(dbvs[0], w);
    }
    // pass Bjet trigger fail HT trigger (to study the shape differences)
    if(!passesHTTrigger && passesBjetTrigger && nt.njets >= 4 && nt.ht() > 600){
      h_dbv_failHT_passBjet->Fill(dbvs[0], w);
      h_dbv_failHT_passBjet_coarse->Fill(dbvs[0], w);
    }
  }
  else if (dbvs.size() == 2){
    double dvv = hypot(nt.x0 - nt.x1, nt.y0 - nt.y1);
    h_dvv_all->Fill(dvv, w);
    h_dvv_all_coarse->Fill(dvv, w);

    // HT trigger
    if(passesHTTrigger && nt.njets >= 4 && nt.ht() > 1200){
      h_dvv_HT->Fill(dvv, w);
      h_dvv_HT_coarse->Fill(dvv, w);
    }
    // Bjet trigger - should think about whether we can be more aggressive with the offline HT threshold
    // e.g. from https://twiki.cern.ch/twiki/pub/CMSPublic/HighLevelTriggerRunIIResults/SUSY2015_trig-Ele15_HT350__var-HT.png
    // it looks like the HT350 leg is 95% efficient already at ~400 GeV
    if(passesBjetTrigger && nt.njets >= 4 && nt.ht() > 600){
      h_dvv_Bjet->Fill(dvv, w);
      h_dvv_Bjet_coarse->Fill(dvv, w);
    }
    // Displaced Dijet trigger
    if(passesDisplacedDijetTrigger && nt.njets >= 4 && nt.ht() > 600){
      h_dvv_DisplacedDijet->Fill(dvv, w);
      h_dvv_DisplacedDijet_coarse->Fill(dvv, w);
    }
    // pass HT trigger fail Bjet trigger (to study the shape differences)
    if(passesHTTrigger && !passesBjetTrigger && nt.njets >= 4 && nt.ht() > 1200){
      h_dvv_passHT_failBjet->Fill(dvv, w);
      h_dvv_passHT_failBjet_coarse->Fill(dvv, w);
    }
    // pass Bjet trigger fail HT trigger (to study the shape differences)
    if(!passesHTTrigger && passesBjetTrigger && nt.njets >= 4 && nt.ht() > 600){
      h_dvv_failHT_passBjet->Fill(dvv, w);
      h_dvv_failHT_passBjet_coarse->Fill(dvv, w);
    }
  }

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

  // also copy this hist if it is present (in an ntuple rather than a MiniTree)
  if(in_f->GetDirectory("mcStat")){
    out_f.mkdir("mcStat")->cd();
    in_f->Get("mcStat/h_sums")->Clone("h_sums");
    out_f.cd();
  }

  // book hists
  h_nvtx = new TH1D("h_nvtx", ";# of vertices;Events", 10, 0, 10);
  h_dbv = new TH1D("h_dbv", ";d_{BV} (cm);Events/20 #mum", 1250, 0, 2.5);

  h_dbv_all = new TH1D("h_dbv_all", ";d_{BV} (cm);Events/20 #mum", 2500, 0, 5.);
  h_dbv_all_coarse = new TH1D("h_dbv_all_coarse", ";d_{BV} (cm);Events/100 #mum", 40, 0, 0.4);
  h_dbv_HT = new TH1D("h_dbv_HT", ";d_{BV} (cm);Events/20 #mum", 2500, 0, 5.);
  h_dbv_HT_coarse = new TH1D("h_dbv_HT_coarse", ";d_{BV} (cm);Events/100 #mum", 40, 0, 0.4);
  h_dbv_Bjet = new TH1D("h_dbv_Bjet", ";d_{BV} (cm);Events/20 #mum", 2500, 0, 5.);
  h_dbv_Bjet_coarse = new TH1D("h_dbv_Bjet_coarse", ";d_{BV} (cm);Events/100 #mum", 40, 0, 0.4);
  h_dbv_DisplacedDijet = new TH1D("h_dbv_DisplacedDijet", ";d_{BV} (cm);Events/20 #mum", 2500, 0, 5.);
  h_dbv_DisplacedDijet_coarse = new TH1D("h_dbv_DisplacedDijet_coarse", ";d_{BV} (cm);Events/100 #mum", 40, 0, 0.4);
  h_dbv_passHT_failBjet = new TH1D("h_dbv_passHT_failBjet", ";d_{BV} (cm);Events/20 #mum", 2500, 0, 5.);
  h_dbv_passHT_failBjet_coarse = new TH1D("h_dbv_passHT_failBjet_coarse", ";d_{BV} (cm);Events/100 #mum", 40, 0, 0.4);
  h_dbv_failHT_passBjet = new TH1D("h_dbv_failHT_passBjet", ";d_{BV} (cm);Events/20 #mum", 2500, 0, 5.);
  h_dbv_failHT_passBjet_coarse = new TH1D("h_dbv_failHT_passBjet_coarse", ";d_{BV} (cm);Events/100 #mum", 40, 0, 0.4);

  h_dvv_all = new TH1D("h_dvv_all", ";d_{VV} (cm);Events/20 #mum", 2500, 0, 5.);
  h_dvv_all_coarse = new TH1D("h_dvv_all_coarse", ";d_{VV} (cm);Events/100 #mum", 40, 0, 0.4);
  h_dvv_HT = new TH1D("h_dvv_HT", ";d_{VV} (cm);Events/20 #mum", 2500, 0, 5.);
  h_dvv_HT_coarse = new TH1D("h_dvv_HT_coarse", ";d_{VV} (cm);Events/100 #mum", 40, 0, 0.4);
  h_dvv_Bjet = new TH1D("h_dvv_Bjet", ";d_{VV} (cm);Events/20 #mum", 2500, 0, 5.);
  h_dvv_Bjet_coarse = new TH1D("h_dvv_Bjet_coarse", ";d_{VV} (cm);Events/100 #mum", 40, 0, 0.4);
  h_dvv_DisplacedDijet = new TH1D("h_dvv_DisplacedDijet", ";d_{VV} (cm);Events/20 #mum", 2500, 0, 5.);
  h_dvv_DisplacedDijet_coarse = new TH1D("h_dvv_DisplacedDijet_coarse", ";d_{VV} (cm);Events/100 #mum", 40, 0, 0.4);
  h_dvv_passHT_failBjet = new TH1D("h_dvv_passHT_failBjet", ";d_{VV} (cm);Events/20 #mum", 2500, 0, 5.);
  h_dvv_passHT_failBjet_coarse = new TH1D("h_dvv_passHT_failBjet_coarse", ";d_{VV} (cm);Events/100 #mum", 40, 0, 0.4);
  h_dvv_failHT_passBjet = new TH1D("h_dvv_failHT_passBjet", ";d_{VV} (cm);Events/20 #mum", 2500, 0, 5.);
  h_dvv_failHT_passBjet_coarse = new TH1D("h_dvv_failHT_passBjet_coarse", ";d_{VV} (cm);Events/100 #mum", 40, 0, 0.4);

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
