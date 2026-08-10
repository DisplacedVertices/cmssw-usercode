#include <vector>
#include <string>
#include <iostream>


void MakeWeightPlots(bool Is_bkg, const char* boson, int mg, int ctau, const char* etabin, const char* year)
{
  TString fns;
  //This is for the previous signal samples
  //This is for the new signal samples
  if (ctau < 1000)
     fns.Form("~/nobackup/crabdirs/TrackMoverMCTruth_%sEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/%sHToSSTodddd_tau%ium_M%02i_%s.root",etabin, boson,ctau,mg, year);
  else
     fns.Form("~/nobackup/crabdirs/TrackMoverMCTruth_%sEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/%sHToSSTodddd_tau%imm_M%02i_%s.root",etabin, boson,ctau/1000,mg, year);
  TString fnb;
  // This is for 10mm->1mm ntuple
  
  if (ctau < 1000)
     if (Is_bkg)
         fnb.Form("~/nobackup/crabdirs/TrackMover_%sEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHists0p03onnormdzulv30lepmumv8_20_noCorrection/background_leptonpresel_%s.root",etabin, year);
     else
         fnb.Form("~/nobackup/crabdirs/TrackMover_%sEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHists0p03onnormdzulv30lepmumv8_20_noCorrection/SingleMuon%s.root",etabin, year);
  else
     if (Is_bkg)
         fnb.Form("~/nobackup/crabdirs/TrackMover_%sEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_noCorrection/background_leptonpresel_%s.root",etabin, year);
     else
         fnb.Form("~/nobackup/crabdirs/TrackMover_%sEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_noCorrection/SingleMuon%s.root",etabin, year);

  TFile* fs = TFile::Open(fns, "read");
  TFile* fb = TFile::Open(fnb, "read");
  // This is for 10mm->1mm ntuple after sump weighting
  TString fnout;
  
  char *low_etabin = new char[20];
  strcpy(low_etabin, etabin);
  auto it = low_etabin;
  *it = (char) tolower(*it);
  
  if (Is_bkg)
     fnout.Form("~/nobackup/crabdirs/TM_2D_move_weight_sim_lepton_histos/reweight_%seta_move_sim_vetodr_tau%06ium_M%02i_%s_2D.root", low_etabin, ctau, mg, year);
  else 
     fnout.Form("~/nobackup/crabdirs/TM_2D_move_weight_dat_lepton_histos/reweight_%seta_move_dat_vetodr_tau%06ium_M%02i_%s_2D.root", low_etabin, ctau, mg, year);
  std::cout << "Getting weights from: " << std::endl;
  std::cout << fns << std::endl;
  std::cout << fnb << std::endl;
  TFile* fout = new TFile(fnout, "recreate");

  std::vector<TString> hns_2d_md = {"nocuts_movedist3_movedist2_den"};
  for (const auto& hn : hns_2d_md){
      std::cout << hn << std::endl;
      TH2D* hb = (TH2D*)fb->Get(hn);
      TH2D* hs = (TH2D*)fs->Get(hn);
      hb->Scale(1./hb->Integral());
      hs->Scale(1./hs->Integral());
      hs->Divide(hb);
      fout->WriteObject(hs,hn);
  }

  fs->Close();
  fb->Close();
  fout->Close();
}


void WeightFiles2Dfinemove()
{
  const char* bosons[1] = { "V" };
  std::vector<int> taus = {100, 300, 1000, 3000, 10000, 30000};
  std::vector<int> mgs = {15, 40, 55};
  const char* years[2] = { "20161p2", "2017p8" };
  const char* etabins[3] = { "Low","Mix","High" };
  for (int i = 0; i < 1; i++){  
    for (int j = 0; j < 2; j++){
      for (int k = 0; k < 3; k++){
        for (int& tau:taus){
          for (int& mg:mgs){
            MakeWeightPlots(0,bosons[i],mg,tau,etabins[k],years[j]);
            MakeWeightPlots(1,bosons[i],mg,tau,etabins[k],years[j]);
          }
        }
      }
    }
  }
}
