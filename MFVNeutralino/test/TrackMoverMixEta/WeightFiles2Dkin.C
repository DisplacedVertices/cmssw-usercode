#include <vector>
#include <string>
#include <iostream>
#include "TMath.h"

void MakeWeightPlots(bool Is_bkg, const char* boson, int mg, int ctau, const char* etabin, const char* year)
{
  TString fns;
  //This is for the previous signal samples
  //This is for the new signal samples
  if (ctau < 1000)
     //fns.Form("~/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijetsV2p4_%sEta_NoQrkEtaCut_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkVetoOdVVJetByMiniJetHistsOnnormdzUlv30lepmumv6/%sHToSSTodddd_tau%ium_M%02i_%s.root",etabin,boson,ctau,mg,year);
     fns.Form("~/nobackup/crabdirs/%sHToSSTodddd_tau%ium_M%02i_alleta.root",boson,ctau,mg);
  else
     //fns.Form("~/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijetsV2p4_%sEta_NoQrkEtaCut_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkVetoOdVVJetByMiniJetHistsOnnormdzUlv30lepmumv6/%sHToSSTodddd_tau%imm_M%02i_%s.root",etabin,boson,ctau/1000,mg,year);
     fns.Form("~/nobackup/crabdirs/%sHToSSTodddd_tau%imm_M%02i_alleta.root",boson,ctau/1000,mg);
  TString fnb;
  // This is for 10mm->1mm ntuple
  if (Is_bkg)
     //fnb.Form("~/nobackup/crabdirs/TrackMover_StudyV2p4_%sEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau%06ium_noCorrection/background_leptonpresel_%s.root", etabin, ctau, year);
     fnb.Form("~/nobackup/crabdirs/background_leptonpresel_alleta.root");
  //else
  //   fnb.Form("~/nobackup/crabdirs/TrackMover_StudyV2p4_%sEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau%06ium_noCorrection/SingleMuon%s.root", etabin, ctau, year);
  TFile* fs = TFile::Open(fns, "read");
  TFile* fb = TFile::Open(fnb, "read");
  // This is for 10mm->1mm ntuple after sump weighting
  TString fnout;
  char *low_etabin = new char[20];
  strcpy(low_etabin, etabin);
  auto it = low_etabin;
  *it = (char) tolower(*it);

  if (Is_bkg)
     fnout.Form("~/nobackup/crabdirs/TM_2D_kin_weight_sim_lepton_histos/reweight_v2p4_alletasoftup_kin_sim_vetodr_tau%06ium_M%02i_2D.root", ctau, mg);
  else
     fnout.Form("~/nobackup/crabdirs/TM_2D_kin_weight_dat_lepton_histos/reweight_v2p4_alletasoftup_kin_dat_vetodr_tau%06ium_M%02i_2D.root", ctau, mg);
  std::cout << "Getting weights from: " << std::endl;
  std::cout << fns << std::endl;
  std::cout << fnb << std::endl;
  TFile* fout = new TFile(fnout, "recreate");


  //std::vector<TString> hns_2d = {"nocuts_llp_sump_jetdr_den", "nocuts_llp_sump_jetdphi_den", "nocuts_nmovedseedtks0_jet0_sump_den", "nocuts_nmovedseedtks1_jet1_sump_den","nocuts_jet0_sump_jetdr_den","nocuts_jet1_sump_jetdr_den","nocuts_nmovedtks_jet_dr_den","nocuts_2logm_jetdr_den", "nocuts_jet0_sump_qrk0_dxybs_den", "nocuts_jet1_sump_qrk1_dxybs_den"}; //"nocuts_jetdr_qrk0_dxybs_den","nocuts_jetdr_qrk1_dxybs_den"};
  std::vector<TString> hns_2d = {"nocuts_llp_sump_jetdr_den",}; // "nocuts_llp_sump_jetdphi_den",};
  for (const auto& hn : hns_2d){
      std::cout << hn << std::endl;
      TH2D* hb = (TH2D*)fb->Get(hn);
      TH2D* hs = (TH2D*)fs->Get(hn);
      int hs_entries = hs->Integral();
      int hb_entries = hb->Integral();
      //hb->RebinX(10);
      //hs->RebinX(10);
      //hb->RebinY(3);
      //hs->RebinY(3);
      hb->RebinX(60);  //60
      hs->RebinX(60); //60
      hb->RebinY(3);
      hs->RebinY(3);
      hb->Scale(1./hb->Integral());
      TH2D* nhb = (TH2D*)hb->Clone("nocuts_llp_sump_jetdr_den");
      hs->Scale(1./hs->Integral());
      TH2D* nhs = (TH2D*)hs->Clone("nocuts_llp_sump_jetdr_den");
      hs->Divide(hb);
      double intl_nhs = 0;
      double intl_nhb = 0;
      for (int bx = 1; bx < hs->GetNbinsX()+1; bx++){
         for (int by = 1; by < hs->GetNbinsY()+1; by++){
             
             int sint = 0;
             double fr = 0;
             if (bx == 1){
                fr = 0.35;
                sint = TMath::Nint(fr) - 1;
                fr -= sint;
             }
             else if ( bx == 2 || bx == 3) {
                fr = 0.35;
                sint = TMath::Nint(fr) - 1;
                fr -= sint;
             }
             else{
                fr = 0.0;
                sint = TMath::Nint(fr) - 1;
                fr -= sint;
             }
             double new_bincontent_nhs = (1-fr)*nhs->GetBinContent(bx, by-sint) + (fr)*nhs->GetBinContent(bx, by-1-sint); 
             double new_bincontent_nhs_err = TMath::Sqrt(new_bincontent_nhs*(1-new_bincontent_nhs)/hs_entries);
             double new_bincontent_nhs_preverr = TMath::Hypot((1-fr)*nhs->GetBinError(bx, by-sint), (fr)*nhs->GetBinError(bx, by-1-sint));
             if (new_bincontent_nhs < 0.0) new_bincontent_nhs_err = nhs->GetBinError(bx, by-sint);
            
             //std::cout << " bin " << bx << ", " << by << " content of signal : " << new_bincontent_nhs << std::endl;  
             //std::cout << " bin " << bx << ", " << by << " err of signal : " << new_bincontent_nhs_err << " or by previous err : " << new_bincontent_nhs_preverr << std::endl; 
             double new_bincontent_nhb = (1-fr)*nhb->GetBinContent(bx, by-sint) + (fr)*nhb->GetBinContent(bx, by-1-sint); 
             double new_bincontent_nhb_err = TMath::Sqrt(new_bincontent_nhb*(1-new_bincontent_nhb)/hb_entries);
             double new_bincontent_nhb_preverr = TMath::Hypot((1-fr)*nhb->GetBinError(bx, by-sint), (fr)*nhb->GetBinError(bx, by-1-sint));
             if (new_bincontent_nhb < 0.0) new_bincontent_nhb_err = nhb->GetBinError(bx, by-sint);  
             //std::cout << " bin " << bx << ", " << by << "content of TMMC : " << new_bincontent_nhb << std::endl;  
             //std::cout << " bin " << bx << ", " << by << " err of TMMC : " << new_bincontent_nhb_err << " or by previous err : " << new_bincontent_nhb_preverr << std::endl; 
             double new_bincontent = new_bincontent_nhs / new_bincontent_nhb;
             intl_nhs += new_bincontent_nhs; 
             intl_nhb += new_bincontent_nhb; 
             if (new_bincontent_nhb == 0) new_bincontent = 0;
             std::cout << " bin " << bx << ", " << by << " old content of map : " << hs->GetBinContent(bx, by) << " new content of map : " << new_bincontent << std::endl;  
             hs->SetBinContent(bx, by, new_bincontent);
             double new_bincontent_err = new_bincontent*TMath::Hypot(new_bincontent_nhs_err/new_bincontent_nhs,new_bincontent_nhb_err/new_bincontent_nhb); 
             if (new_bincontent == 0) new_bincontent_err = 0;
             //std::cout << " bin " << bx << ", " << by << " signal/TMMC ratio : " << new_bincontent << " and error : " << new_bincontent_err  << " or by previous error : " << TMath::Hypot(fr*hs->GetBinError(bx, by+sint), (1-fr)*hs->GetBinError(bx, by+1+sint)) <<  std::endl; 
             hs->SetBinError(bx, by, new_bincontent_err);
             //hs->SetBinError(bx, TMath::Hypot(fr*hs->GetBinError(bx, by+sint), (1-fr)*hs->GetBinError(bx, by+1+sint)));

         }
      }
      std::cout << " sum new hns bins : " << intl_nhs << std::endl; 
      std::cout << " sum new hnb bins : " << intl_nhb << std::endl; 
      fout->WriteObject(hs,hn);
  }
  fs->Close();
  fb->Close();
  fout->Close();
}


void WeightFiles2Dkin()
{
  const char* bosons[1] = { "V" };
  std::vector<int> taus = {1000,};//{100, 300, 1000, 3000, 30000};
  std::vector<int> mgs = {55,};
  const char* years[1] = { "20161p2"}; //, "2017p8",};
  const char* etabins[1] = { "High" };
  for (int i = 0; i < 1; i++){  
    for (int j = 0; j < 1; j++){
      for (int k = 0; k < 1; k++){
        for (int& tau:taus){
          for (int& mg:mgs){
            if (tau==100 && mg==40)
              continue;
            //MakeWeightPlots(0,bosons[i],mg,tau,etabins[k],years[j]);
            MakeWeightPlots(1,bosons[i],mg,tau,etabins[k],years[j]);
          }
        }
      }
    }
  }
}
