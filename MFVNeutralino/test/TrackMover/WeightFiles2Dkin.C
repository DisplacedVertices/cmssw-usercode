#include <vector>
#include <string>
#include <iostream>
#include "TMath.h"

void MakeWeightPlots(int mg, int ctau, const char* etabin, const char* year)
{
  TString fns;
  //This is for the previous signal samples
  //This is for the new signal samples
  if (ctau < 1000){
     //fns.Form("~/nobackup/crabdirs/TrackMoverMCTruth_AllEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/VHToSSTodddd_tau%ium_M%02i_all.root",ctau,mg);
     //fns.Form("~/nobackup/crabdirs/TrackMoverMCTruth_AllEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30bmpreselv6/mfv_stopbbarbbar_tau%06ium_M%04i_all.root",ctau,mg);
     fns.Form("~/nobackup/crabdirs/TrackMoverMCTruth_AllEta_HighdVV0p36_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30bmpreselhighptv6/mfv_stopdbardbar_tau%06ium_M%04i_all.root",ctau,mg);
     //fns.Form("~/nobackup/crabdirs/TrackMoverMCTruth_AllEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30bmpreselv6/ggHToSSTodddd_tau%ium_M%02i_all.root",ctau,mg);
  }
  else{
     //fns.Form("~/nobackup/crabdirs/TrackMoverMCTruth_AllEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/VHToSSTodddd_tau%imm_M%02i_all.root",ctau/1000,mg);
     //fns.Form("~/nobackup/crabdirs/TrackMoverMCTruth_AllEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30bmpreselv6/mfv_stopbbarbbar_tau%06ium_M%04i_all.root",ctau,mg);
     fns.Form("~/nobackup/crabdirs/TrackMoverMCTruth_AllEta_HighdVV0p36_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30bmpreselhighptv6/mfv_stopdbardbar_tau%06ium_M%04i_all.root",ctau,mg);
     //fns.Form("~/nobackup/crabdirs/TrackMoverMCTruth_AllEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30bmpreselv6/ggHToSSTodddd_tau%imm_M%02i_all.root",ctau/1000,mg);
  }
  TString fnb;
  // This is for 10mm->1mm ntuple
  
  //fnb.Form("~/nobackup/crabdirs/TrackMover_AllEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_noCorrection/background_leptonpresel_all.root");
  //fnb.Form("~/nobackup/crabdirs/TrackMover_AllEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30bmofftosspreselv8_20_noCorrection/background_btagpresel_all.root");
  fnb.Form("~/nobackup/crabdirs/TrackMover_AllEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30bmofftosspreselhighptv8_20_noCorrection/background_btagpresel_all.root");
  TFile* fs = TFile::Open(fns, "read");
  TFile* fb = TFile::Open(fnb, "read");
  // This is for 10mm->1mm ntuple after sump weighting
  TString fnout;
  char *low_etabin = new char[20];
  strcpy(low_etabin, etabin);
  auto it = low_etabin;
  *it = (char) tolower(*it);

  //fnout.Form("~/nobackup/crabdirs/TM_2D_kin_weight_sim_lepton_histos/reweight_all_kin_sim_vetodr_tau%06ium_M%02i_2D.root", ctau, mg);
  //fnout.Form("~/nobackup/crabdirs/TM_2D_kin_weight_sim_stopb_histos/reweight_all_kin_sim_vetodr_tau%06ium_M%04i_2D.root", ctau, mg);
  fnout.Form("~/nobackup/crabdirs/TM_2D_kin_weight_sim_stopd_histos/reweight_all_kin_sim_vetodr_tau%06ium_M%04i_2D.root", ctau, mg);
  //fnout.Form("~/nobackup/crabdirs/TM_2D_kin_weight_sim_ggh_histos/reweight_all_kin_sim_vetodr_tau%06ium_M%02i_2D.root", ctau, mg);
  std::cout << "Getting weights from: " << std::endl;
  std::cout << fns << std::endl;
  std::cout << fnb << std::endl;
  TFile* fout = new TFile(fnout, "recreate");


  std::vector<TString> hns_2d = {"nocuts_llp_sump_jetdr_den",}; // "nocuts_llp_sump_jetdphi_den",};
  for (const auto& hn : hns_2d){
      std::cout << hn << std::endl;
      TH2D* hb = (TH2D*)fb->Get(hn);
      TH2D* hs = (TH2D*)fs->Get(hn);
      int hs_entries = hs->Integral();
      int hb_entries = hb->Integral();
      hb->Scale(1./hb->Integral());
      hs->Scale(1./hs->Integral());
      
      hb->RebinX(60);  //60
      hs->RebinX(60); //60
      hb->RebinY(3);  //3
      hs->RebinY(3);  //3
      
      hs->Divide(hb);
      hs->GetXaxis()->SetRangeUser(0.0,800.0);
      fout->WriteObject(hs,hn);
  }
  fs->Close();
  fb->Close();
  fout->Close();
}


void WeightFiles2Dkin()
{
  std::vector<int> taus = {100, 300, 1000, 10000, 30000};
  std::vector<int> mgs = {200,400,800};
  const char* years[1] = {"2017p8"}; //, "2017p8",};
  const char* etabins[1] = { "All"}; //"Low", "Mix", "High" };
  for (int j = 0; j < 1; j++){
    for (int k = 0; k < 1; k++){
       for (int& tau:taus){
         for (int& mg:mgs){
           MakeWeightPlots(mg,tau,etabins[k],years[j]);
         }
       }
    }
  }
}
