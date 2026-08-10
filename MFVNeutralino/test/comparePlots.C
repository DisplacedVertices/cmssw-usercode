void comparePlots()
{
  gStyle->SetOptStat(0);
  //TString fn_MET = "MET_study/output_studyNewTriggers_ntk5_2017/mfv_splitSUSY_tau000001000um_M2000_1800_2017.root";
  //TString fn_HT = "HT_study/output_studyNewTriggers_ntk5_2017/mfv_splitSUSY_tau000001000um_M2000_1800_2017.root";
  TString plot = "Ntk3mfvVertexHistosFullSel/h_svdist2d";
  int rb = 10;
  TString fn_MET = "/uscms_data/d3/ali/LLP/crabdir/HistosV36METm_noHTveto/background_metpresel_2017.root";
  TString fn_HT = "/uscms_data/d2/tucker/crab_dirs/HistosV27m/background_2017.root";

  //TString fn_MET = "MET_study/output_studyNewTriggers_ntk3_2017/background.root";
  //TString fn_HT = "HT_study/output_studyNewTriggers_ntk3_2017/background.root";
  TFile *f_MET = new TFile(fn_MET);
  TFile *f_HT = new TFile(fn_HT);
  TH1F* h_MET = (TH1F*)f_MET->Get(plot);
  TH1F* h_HT = (TH1F*)f_HT->Get(plot);
  TCanvas* c = new TCanvas("c", "c", 600, 600);
  c->cd();
  h_MET->SetLineColor(kBlue);
  h_HT->SetLineColor(kRed);
  h_MET->Scale(1.0/(h_MET->Integral()));
  h_HT->Scale(1.0/(h_HT->Integral()));
  h_MET->Rebin(rb);
  h_HT->Rebin(rb);
  h_MET->SetTitle("MET");
  //h_MET->GetYaxis()->SetRangeUser(0, 0.2);
  h_MET->Draw();
  h_HT->Draw("same");
  TLegend *l = new TLegend(0.6,0.7,0.9,0.9);
  l->AddEntry(h_MET,"MET trigger");
  l->AddEntry(h_HT,"HT trigger");
  l->Draw();

}
