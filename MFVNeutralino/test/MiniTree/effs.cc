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

TH1D* h_num_1v = 0;
TH1D* h_den_1v = 0;
TH1D* h_num_2v = 0;
TH1D* h_den_2v = 0;

TH1D* h_eff_1v = 0;
TH1D* h_eff_2v = 0;

bool pass_hlt(const mfv::MiniNtuple& nt, size_t i){
  return bool((nt.pass_hlt >> i) & 1);
}

void formatHist(TH1& h){
  h.SetStats(0);
  h.GetXaxis()->SetLabelSize(0.035);
  h.GetXaxis()->SetBinLabel(1, "PFHT1050");
  h.GetXaxis()->SetBinLabel(2, "DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_p33");
  h.GetXaxis()->SetBinLabel(3, "PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0");
  h.GetXaxis()->SetBinLabel(4, "PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2");
  h.GetXaxis()->SetBinLabel(5, "PFHT380_SixPFJet32_DoublePFBTagCSV_2p2");
  h.GetXaxis()->SetBinLabel(6, "PFHT430_SixPFJet40_PFBTagCSV_1p5");
  h.GetXaxis()->SetBinLabel(7, "HT430_DisplacedDijet40_DisplacedTrack");
  h.GetXaxis()->SetBinLabel(8, "OR of first two bjet triggers");
  h.GetXaxis()->SetBinLabel(9, "OR of all bjet triggers");
  h.GetXaxis()->SetBinLabel(10,"OR of all triggers");
}

// analyze method is a callback passed to MiniNtuple::loop from main that is called once per tree entry
bool analyze(long long j, long long je, const mfv::MiniNtuple& nt) {
  if (prints) std::cout << "Entry " << j << "\n";

  // count nbjets for the bjet triggers
  int nbjets = 0;
  for(int ijet = 0; ijet < nt.njets; ++ijet){
    double bdisc = nt.jet_bdisc[ijet];
    
    // Tight WP, 2017
    if(bdisc >= 0.7489) ++nbjets;
  }

  // at least four jets
  if(nt.njets < 4) return true;

  bool path0 = pass_hlt(nt, mfv::b_HLT_PFHT1050) && nt.ht() > 1200;

  // pt requirements: go 40 GeV above threshold based on https://twiki.cern.ch/twiki/bin/view/CMSPublic/HLTplots2018DataJets
  // HT requirements: go 150 GeV above threshold based on what we've done with the HT1050 trigger
  //
  // should think about whether we can be more aggressive with the offline HT threshold
  // e.g. from https://twiki.cern.ch/twiki/pub/CMSPublic/HighLevelTriggerRunIIResults/SUSY2015_trig-Ele15_HT350__var-HT.png
  // it looks like the HT350 leg is 95% efficient already at ~400 GeV
  bool path1 = (pass_hlt(nt, mfv::b_HLT_DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_p33) && nt.njets >= 2 && nbjets >= 2);
      
  bool path1_passed_kinematics = false;
  for(int ijet = 0; ijet < nt.njets; ++ijet){
    for(int jjet = ijet+1; jjet < nt.njets; ++jjet){
      if(nt.jet_pt[ijet] > 140 && nt.jet_pt[jjet] > 140 && fabs(nt.jet_eta[ijet] - nt.jet_eta[jjet]) < 1.6){
        path1_passed_kinematics = true;
      }
    }
  }

  path1 = path1 && path1_passed_kinematics;

  bool path2 = (pass_hlt(nt, mfv::b_HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0) && nt.ht(30) > 450 && nt.njets >= 4 && nt.jet_pt[0] > 115 && nt.jet_pt[1] > 100 && nt.jet_pt[2] > 85 && nt.jet_pt[3] > 80 && nbjets >= 3);
  bool path3 = (pass_hlt(nt, mfv::b_HLT_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2) && nt.ht() > 530 && nt.njets >= 6 && nt.jet_pt[0] > 72 && nt.jet_pt[1] > 72 && nt.jet_pt[2] > 72 && nt.jet_pt[3] > 72 && nt.jet_pt[4] > 72 && nt.jet_pt[5] > 72 && nbjets >= 2);
  bool path4 = (pass_hlt(nt, mfv::b_HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2)     && nt.ht() > 530 && nt.njets >= 6 && nt.jet_pt[0] > 72 && nt.jet_pt[1] > 72 && nt.jet_pt[2] > 72 && nt.jet_pt[3] > 72 && nt.jet_pt[4] > 72 && nt.jet_pt[5] > 72 && nbjets >= 2);
  bool path5 = (pass_hlt(nt, mfv::b_HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5) && nt.ht() > 580 && nt.njets >= 6 && nt.jet_pt[0] > 80 && nt.jet_pt[1] > 80 && nt.jet_pt[2] > 80 && nt.jet_pt[3] > 80 && nt.jet_pt[4] > 80 && nt.jet_pt[5] > 80 && nbjets >= 1);

  bool path6 = pass_hlt(nt, mfv::b_HLT_HT430_DisplacedDijet40_DisplacedTrack) && nt.njets >= 2 && nt.jet_pt[0] > 80 && nt.jet_pt[1] > 80 && nt.ht() > 580; // ignore the other one with a higher HT threshold for now...

  bool path7 = path1 || path2;
  bool path8 = path1 || path2 || path3 || path4 || path5;
  bool path9 = path0 || path1 || path2 || path3 || path4 || path5 || path6;

  // for efficiencies orthogonal with the HT trigger
  //path1 = path1 && !path0;
  //path2 = path2 && !path0;
  //path3 = path3 && !path0;
  //path4 = path4 && !path0;
  //path5 = path5 && !path0;
  //path6 = path6 && !path0;
  //path7 = path7 && !path0;
  //path8 = path8 && !path0;

  // paths to pass the trigger
  std::vector<bool> paths = {path0, path1, path2, path3, path4, path5, path6, path7, path8, path9};

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

  if (dbvs.size() == 1){
    for(int ipath = 0; ipath < paths.size(); ++ipath){
      h_den_1v->Fill(ipath,w);

      if(paths[ipath]){
        h_num_1v->Fill(ipath,w);
      }

    }
  }
  else if (dbvs.size() == 2){
    for(int ipath = 0; ipath < paths.size(); ++ipath){
      h_den_2v->Fill(ipath,w);

      if(paths[ipath]){
        h_num_2v->Fill(ipath,w);
      }

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
  h_num_1v = new TH1D("h_num_1v", ";;Events", 10, 0, 10);
  h_den_1v = new TH1D("h_den_1v", ";;Events", 10, 0, 10);
  h_num_2v = new TH1D("h_num_2v", ";;Events", 10, 0, 10);
  h_den_2v = new TH1D("h_den_2v", ";;Events", 10, 0, 10);

  formatHist(*h_num_1v);
  formatHist(*h_num_2v);
  formatHist(*h_den_1v);
  formatHist(*h_den_2v);

  const char* tree_path =
    ntk == 3 ? "mfvMiniTreeNtk3/t" :
    ntk == 4 ? "mfvMiniTreeNtk4/t" :
    ntk == 7 ? "mfvMiniTreeNtk3or4/t" :
    ntk == 5 ? "mfvMiniTree/t" : 0;
  if (prints) printf("fn %s out_fn %s ntk %i path %s\n", tree_path);

  mfv::loop(fn, tree_path, analyze);

  out_f.cd();

  h_eff_1v = new TH1D("h_eff_1v", ";;Efficiency", 10, 0, 10);
  h_eff_2v = new TH1D("h_eff_2v", ";;Efficiency", 10, 0, 10);
  formatHist(*h_eff_1v);
  formatHist(*h_eff_2v);

  h_eff_1v->Divide(h_num_1v, h_den_1v, 1, 1, "B");
  h_eff_2v->Divide(h_num_2v, h_den_2v, 1, 1, "B");

  float max_val1 = 0;
  float max_val2 = 0;

  TString max_trig1 = "";
  TString max_trig2 = "";

  // ibin = 1 is the HT trigger
  // ibin = 7 is the last trigger that isn't an OR
  for(int ibin = 1; ibin < 8; ++ibin){
    float bin_val = h_eff_2v->GetBinContent(ibin);
    if(bin_val > max_val1){

      max_val2 = max_val1;
      max_trig2 = max_trig1;

      max_val1 = bin_val;
      max_trig1 = h_eff_2v->GetXaxis()->GetBinLabel(ibin);
    }
    else if(bin_val > max_val2){
      max_val2 = bin_val;
      max_trig2 = h_eff_2v->GetXaxis()->GetBinLabel(ibin);
    }
  }

  std::cout << "max_trig1: " << max_trig1 << ", eff = " << max_val1 << std::endl;
  std::cout << "max_trig2: " << max_trig2 << ", eff = " << max_val2 << std::endl;

  TCanvas* can = new TCanvas();
  can->SetBottomMargin(0.25);
  TString pdf_file = out_fn;
  pdf_file.ReplaceAll(".root",".pdf");
  h_eff_2v->Draw();
  can->Print(pdf_file);

  out_f.Write();
  out_f.Close();
}
