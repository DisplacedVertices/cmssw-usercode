#include <vector>
#include <string>
#include <iostream>
#include "TMath.h"

void MakeWeightPlots(bool Is_bkg, int mg, int ctau, const char* etabin, const char* year)
{
  TString fns;
  
  //This is for the previous signal samples
  //This is for the new signal samples
  
  if (ctau < 1000){
     //fns.Form("~/nobackup/crabdirs/TrackMoverMCTruth_%sEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/VHToSSTodddd_tau%ium_M%02i_%s.root",etabin,ctau,mg,year);
     //fns.Form("~/nobackup/crabdirs/TrackMoverMCTruth_%sEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30bmpreselv6/mfv_stopbbarbbar_tau%06ium_M%04i_%s.root",etabin,ctau,mg, year);
     fns.Form("~/nobackup/crabdirs/TrackMoverMCTruth_%sEta_HighdVV0p36_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30bmpreselhighptv6/mfv_stopdbardbar_tau%06ium_M%04i_%s.root",etabin,ctau,mg, year);
     //fns.Form("~/nobackup/crabdirs/TrackMoverMCTruth_%sEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30bmpreselv6/ggHToSSTodddd_tau%ium_M%02i_%s.root",etabin,ctau,mg,year);
  }
  else{
     //fns.Form("~/nobackup/crabdirs/TrackMoverMCTruth_%sEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/VHToSSTodddd_tau%imm_M%02i_%s.root",etabin,ctau/1000,mg, year);
     //fns.Form("~/nobackup/crabdirs/TrackMoverMCTruth_%sEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30bmpreselv6/mfv_stopbbarbbar_tau%06ium_M%04i_%s.root",etabin,ctau,mg, year);
     fns.Form("~/nobackup/crabdirs/TrackMoverMCTruth_%sEta_HighdVV0p36_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30bmpreselhighptv6/mfv_stopdbardbar_tau%06ium_M%04i_%s.root",etabin,ctau,mg, year);
     //fns.Form("~/nobackup/crabdirs/TrackMoverMCTruth_%sEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30bmpreselv6/ggHToSSTodddd_tau%imm_M%02i_%s.root",etabin,ctau/1000,mg,year);
  }
  
  TString fnb;
  // This is for 10mm->1mm ntuple
  
  if (Is_bkg){
      //fnb.Form("~/nobackup/crabdirs/TrackMover_%sEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_noCorrection/background_leptonpresel_%s.root",etabin, year);
      fnb.Form("~/nobackup/crabdirs/TrackMover_%sEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30bmofftosspreselhighptv8_20_noCorrection/background_btagpresel_%s.root", etabin, year);
      //fnb.Form("~/nobackup/crabdirs/TrackMover_%sEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30bmofftosspreselv8_20_noCorrection/background_btagpresel_%s.root",etabin, year);
  }
  else{
      //fnb.Form("~/nobackup/crabdirs/TrackMover_%sEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_noCorrection/SingleMuon%s.root",etabin, year);
      fnb.Form("~/nobackup/crabdirs/TrackMover_%sEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30bmofftosspreselhighptv8_20_noCorrection/BTagDispl%s.root", etabin, year);
      //fnb.Form("~/nobackup/crabdirs/TrackMover_%sEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30bmofftosspreselv8_20_noCorrection/BTagDispl%s.root",etabin, year);
  }

  TFile* fs = TFile::Open(fns, "read");
  TFile* fb = TFile::Open(fnb, "read");
  // This is for 10mm->1mm ntuple after sump weighting
  TString fnout;
  
  char *low_etabin = new char[20];
  strcpy(low_etabin, etabin);
  auto it = low_etabin;
  *it = (char) tolower(*it);
  
  if (Is_bkg){
     //fnout.Form("~/nobackup/crabdirs/TM_2D_move_weight_sim_lepton_histos/reweight_%seta_move_sim_vetodr_tau%06ium_M%02i_%s_2D.root", low_etabin, ctau, mg, year);
     //fnout.Form("~/nobackup/crabdirs/TM_2D_move_weight_sim_stopb_histos/reweight_%seta_move_sim_vetodr_tau%06ium_M%04i_%s_2D.root", low_etabin, ctau, mg, year);
     fnout.Form("~/nobackup/crabdirs/TM_2D_move_weight_sim_stopd_histos/reweight_%seta_move_sim_vetodr_tau%06ium_M%04i_%s_2D.root", low_etabin, ctau, mg, year);
     //fnout.Form("~/nobackup/crabdirs/TM_2D_move_weight_sim_ggh_histos/reweight_%seta_move_sim_vetodr_tau%06ium_M%02i_%s_2D.root", low_etabin, ctau, mg, year);
  }
  else { 
     //fnout.Form("~/nobackup/crabdirs/TM_2D_move_weight_dat_lepton_histos/reweight_%seta_move_dat_vetodr_tau%06ium_M%02i_%s_2D.root", low_etabin, ctau, mg, year);
     //fnout.Form("~/nobackup/crabdirs/TM_2D_move_weight_dat_stopb_histos/reweight_%seta_move_dat_vetodr_tau%06ium_M%04i_%s_2D.root", low_etabin, ctau, mg, year);
     fnout.Form("~/nobackup/crabdirs/TM_2D_move_weight_dat_stopd_histos/reweight_%seta_move_dat_vetodr_tau%06ium_M%04i_%s_2D.root", low_etabin, ctau, mg, year);
     //fnout.Form("~/nobackup/crabdirs/TM_2D_move_weight_dat_ggh_histos/reweight_%seta_move_dat_vetodr_tau%06ium_M%02i_%s_2D.root", low_etabin, ctau, mg, year);
  }
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
      
      std::vector<double> b_Int_idx = {}; 
      std::vector<double> b_error_Int_idx = {}; 
      std::vector<double> s_Int_idx = {}; 
      std::vector<double> s_error_Int_idx = {}; 
      std::vector<int> b_x = {16, 18, 20, 22, 24, 26, 30, 38, 50};  
      std::vector<int> b_y = {0, 10, 14, 16, 17, 18, 19, 20, 22, 26, 34, 50}; 
      
      for (int i = 0; i < b_x.size()-1; ++i){
         for (int j = 5-i; j < 8+i; ++j){
            if (j < 0)
              j = 0;
            double b_error_Int = 0, s_error_Int = 0;
            double b_Int = hb->IntegralAndError(b_x[i]+1,b_x[i+1],b_y[j]+1,b_y[j+1],b_error_Int, "");
            b_Int_idx.push_back(b_Int);
            b_error_Int_idx.push_back(b_error_Int);

            double s_Int = hs->IntegralAndError(b_x[i]+1,b_x[i+1],b_y[j]+1,b_y[j+1],s_error_Int, "");
            s_Int_idx.push_back(s_Int);
            s_error_Int_idx.push_back(s_error_Int);
         }
      }

      int ij = 0;
      for (int i = 0; i < b_x.size()-1; ++i){
        for (int j = 5-i; j < 8+i; ++j){
           if (j < 0) 
             j = 0;
           double exp_Int_idx = 0.0;
           for (int bx = 1; bx < hs->GetNbinsX()+1; bx++){
               for (int by = 1; by < hs->GetNbinsY()+1; by++){
                  if ( hs->GetBinContent(bx, by) != 0 && b_x[i] < bx && bx < b_x[i+1]+1 && b_y[j] < by && by < b_y[j+1]+1) {
                     exp_Int_idx +=  hs->GetBinContent(bx, by);
                     if (fabs(s_Int_idx[ij]/b_Int_idx[ij]) > 20.0){
                       if (fabs(s_Int_idx[ij-1]/b_Int_idx[ij-1]) < 20.0){
                         hb->SetBinContent(bx, by, b_Int_idx[ij-1]);
                         hb->SetBinError(bx, by, b_error_Int_idx[ij-1]);
                         hs->SetBinContent(bx, by, s_Int_idx[ij-1]);
                         hs->SetBinError(bx, by, s_error_Int_idx[ij-1]);
                       }
                       else{
                         hb->SetBinContent(bx, by, b_Int_idx[ij+1]);
                         hb->SetBinError(bx, by, b_error_Int_idx[ij+1]);
                         hs->SetBinContent(bx, by, s_Int_idx[ij+1]);
                         hs->SetBinError(bx, by, s_error_Int_idx[ij+1]);
                       }
                     }
                     else{
                       hb->SetBinContent(bx, by, b_Int_idx[ij]);
                       hb->SetBinError(bx, by, b_error_Int_idx[ij]);
                       hs->SetBinContent(bx, by, s_Int_idx[ij]);
                       hs->SetBinError(bx, by, s_error_Int_idx[ij]);
                     }
                  }
                  else{
                     if (fabs(hs->GetBinContent(bx, by)/hb->GetBinContent(bx, by)) > 15.0 || hs->GetBinContent(bx, by)/hb->GetBinContent(bx, by) < 0.0){
                       if (fabs(hs->GetBinContent(bx-1, by)/hb->GetBinContent(bx-1, by)) < 15.0 && hs->GetBinContent(bx-1, by)/hb->GetBinContent(bx-1, by) > 0.0){
                         hb->SetBinContent(bx, by, hb->GetBinContent(bx-1, by));
                         hb->SetBinError(bx, by, hb->GetBinError(bx-1, by));
                         hs->SetBinContent(bx, by, hs->GetBinContent(bx-1, by));
                         hs->SetBinError(bx, by, hs->GetBinError(bx-1, by));
                       }
                       else if (fabs(hs->GetBinContent(bx+1, by)/hb->GetBinContent(bx+1, by)) < 15.0 && hs->GetBinContent(bx+1, by)/hb->GetBinContent(bx+1, by) > 0.0){
                         hb->SetBinContent(bx, by, hb->GetBinContent(bx+1, by));
                         hb->SetBinError(bx, by, hb->GetBinError(bx+1, by));
                         hs->SetBinContent(bx, by, hs->GetBinContent(bx+1, by));
                         hs->SetBinError(bx, by, hs->GetBinError(bx+1, by));
                       }
                       else if (fabs(hs->GetBinContent(bx, by-1)/hb->GetBinContent(bx, by-1)) < 15.0 && hs->GetBinContent(bx, by-1)/hb->GetBinContent(bx, by-1) > 0.0){
                         hb->SetBinContent(bx, by, hb->GetBinContent(bx, by-1));
                         hb->SetBinError(bx, by, hb->GetBinError(bx, by-1));
                         hs->SetBinContent(bx, by, hs->GetBinContent(bx, by-1));
                         hs->SetBinError(bx, by, hs->GetBinError(bx, by-1));
                       }
                       else{
                         hb->SetBinContent(bx, by, hb->GetBinContent(bx, by+1));
                         hb->SetBinError(bx, by, hb->GetBinError(bx, by+1));
                         hs->SetBinContent(bx, by, hs->GetBinContent(bx, by+1));
                         hs->SetBinError(bx, by, hs->GetBinError(bx, by+1));
                       }
                     }
                  }
                     
               }
           }
           ij++;
         }
      }
         
      hs->Divide(hb);
      fout->WriteObject(hs,hn);
  }

  fs->Close();
  fb->Close();
  fout->Close();
}


void WeightFiles2Dmove()
{
  std::vector<int> taus = {1000}; //100, 300, 1000, 3000, 10000, 30000}; // 10000};
  std::vector<int> mgs = {400}; //15, 40, 55};
  const char* years[1] = {"2017p8"}; //20161p2
  const char* etabins[1] = {"Low",}; // "Mix", "High"};
  for (int j = 0; j < 1; j++){
     for (int k = 0; k < 1; k++){
       for (int& tau:taus){
        for (int& mg:mgs){
          MakeWeightPlots(0,mg,tau,etabins[k],years[j]); //data
          MakeWeightPlots(1,mg,tau,etabins[k],years[j]);  //sim
        }
       }
     }
  }
}
