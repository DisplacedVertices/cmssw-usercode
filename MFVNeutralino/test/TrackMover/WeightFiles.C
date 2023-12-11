#include <vector>

void MakeWeightPlots(bool Is_bkg, int mg, int ctau, int year, bool doangle, double weight_limit=-1)
{
  TString fns;
  //This is for the previous signal samples
  //This is for the new signal samples
  fns.Form("root://cmseos.fnal.gov//store/user/pekotamn/TM_signals_histos/WplusHToSSTodddd_tau%imm_M%02i_%i.root",ctau,mg,year);
  TString fnb;
  // This is for 10mm->1mm ntuple
  if (Is_bkg)
     fnb.Form("root://cmseos.fnal.gov//store/user/pekotamn/TM_bkg_histos/background_leptonpresel_%i.root",year);
  else
     fnb.Form("root://cmseos.fnal.gov//store/user/pekotamn/TM_data_histos/SingleMuon%i.root",year);
  TFile* fs = TFile::Open(fns, "read");
  TFile* fb = TFile::Open(fnb, "read");
  // This is for 10mm->1mm ntuple after sump weighting
  TString fnout;
  fnout.Form("reweight_tau%imm_M%02i_%i.root", ctau, mg, year);
  std::cout << "Getting weights from: " << std::endl;
  std::cout << fns << std::endl;
  std::cout << fnb << std::endl;
  TFile* fout = new TFile(fnout, "recreate");

  /*
  std::vector<TString> hns_1d = {"nocuts_jet_dr_den"};
  for (const auto& hn : hns_1d){
      std::cout << hn << std::endl;
      TH1D* hb = (TH1D*)fb->Get(hn);
      TH1D* hs = (TH1D*)fs->Get(hn);
      //hb->Rebin(2);
      hb->Scale(1./hb->Integral());
      hs->Scale(1./hs->Integral());
      hs->Divide(hb);
      fout->WriteObject(hs,hn);
  }
  fs->Close();
  fb->Close();
  fout->Close();
  */

  std::vector<TString> hns_2d = {"nocuts_jet1_sump_jetdr_den"};
  for (const auto& hn : hns_2d){
      std::cout << hn << std::endl;
      TH2D* hb = (TH2D*)fb->Get(hn);
      TH2D* hs = (TH2D*)fs->Get(hn);
      hb->Scale(1./hb->Integral());
      hs->Scale(1./hs->Integral());
      hs->Divide(hb);
      if ((weight_limit>0) && (hn!="nocuts_detadphi_js_mv_den")){
        for(int i=0; i<hs->GetNcells(); ++i){
          if (hs->GetBinContent(i)>weight_limit)
            hs->SetBinContent(i,weight_limit);
          else if (hs->GetBinContent(i)<(-1)*weight_limit)
            hs->SetBinContent(i,(-1)*weight_limit);
        }
      }
      fout->WriteObject(hs,hn);
  }
  fs->Close();
  fb->Close();
  fout->Close();
}


void WeightFiles()
{
  std::vector<int> taus = {1};
  std::vector<int> mgs = {55};
  //std::vector<int> years = {20161, 20162, 2017, 2018};
  std::vector<int> years = {2017};
  for (int& year:years){
    for (int& tau:taus){
      for (int& mg:mgs){
        MakeWeightPlots(1,mg,tau,year,false,30);
        //MakeWeightPlots(0,mg,tau,year,false,30);
      }
    }
  }
}
