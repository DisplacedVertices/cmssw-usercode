#include <vector>
#include <string>
#include <iostream>

void MakeWeightPlots(bool Is_bkg, const char* boson, int mg, int ctau, int year)
{
  TString fns;
  //This is for the previous signal samples
  //This is for the new signal samples
  fns.Form("~/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijets_NoPreSelRelaxBSPVetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/%sHToSSTodddd_tau%imm_M%02i_%i.root",boson,ctau/1000,mg,year);
  TString fnb;
  // This is for 10mm->1mm ntuple
  if (Is_bkg)
     fnb.Form("~/nobackup/crabdirs/TrackMoverNoPreSelRelaxBSPNotwJetByJetHistsOnnormdzulv30lepmumv7_20_tau%06ium_noCorrection/background_leptonpresel_%i.root", ctau, year);
  else
     fnb.Form("~/nobackup/crabdirs/TrackMoverNoPreSelRelaxBSPNotwJetByJetHistsOnnormdzulv30lepmumv7_20_tau%06ium_noCorrection/SingleMuon%i.root", ctau, year);
  TFile* fs = TFile::Open(fns, "read");
  TFile* fb = TFile::Open(fnb, "read");
  // This is for 10mm->1mm ntuple after sump weighting
  TString fnout;
  if (Is_bkg)
     fnout.Form("~/nobackup/crabdirs/TM_1D_weight_sim_lepton_histos/reweightnopreselrelaxbspnotwvetomllp_tau%imm_M%02i_%i_1D.root", ctau/1000, mg, year);
  else
     fnout.Form("~/nobackup/crabdirs/TM_1D_weight_dat_lepton_histos/reweightnopreselrelaxbspnotwvetomllp_tau%imm_M%02i_%i_1D.root", ctau/1000, mg, year);
  std::cout << "Getting weights from: " << std::endl;
  std::cout << fns << std::endl;
  std::cout << fnb << std::endl;
  TFile* fout = new TFile(fnout, "recreate");
  
  std::vector<TString> hns_1d = {"nocuts_movedist3_den", "nocuts_movedist2_den"}; //, "nocuts_nseedtracks_den", "nocuts_2logm_den", "nocuts_closeseedtks_den","nocuts_jet_costheta_den","nocuts_jet1_sump_den","nocuts_jet_dr_den"};
  for (const auto& hn : hns_1d){
      std::cout << hn << std::endl;
      TH1D* hb = (TH1D*)fb->Get(hn);
      TH1D* hs = (TH1D*)fs->Get(hn);
      //hb->GetXaxis()->SetRangeUser(0.0,0.45);
      //hs->GetXaxis()->SetRangeUser(0.0,0.45);
      hb->Scale(1./hb->Integral());
      hs->Scale(1./hs->Integral());
      //hb->GetXaxis()->SetRangeUser(0.0,0.5);
      //hs->GetXaxis()->SetRangeUser(0.0,0.5);
      hs->Divide(hb);
      fout->WriteObject(hs,hn);
  }
  fs->Close();
  fb->Close();
  fout->Close();
     
}


void WeightFiles1D()
{
  const char* bosons[1]
          = { "Wplus" };
  std::vector<int> taus = {1000};//,300};
  std::vector<int> mgs = {55};
  //std::vector<int> years = {20161, 20162, 2017, 2018};
  std::vector<int> years = {2017};
  for (int i = 0; i < 1; i++){  
    for (int& year:years){
      for (int& tau:taus){
        for (int& mg:mgs){
          MakeWeightPlots(1,bosons[i],mg,tau,year);
          //MakeWeightPlots(0,bosons[i],mg,tau,year);
        }
      }
    }
  }
}
