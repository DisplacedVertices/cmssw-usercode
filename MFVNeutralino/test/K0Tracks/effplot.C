void effplot()
{
  gROOT->SetBatch(kTRUE);
  gStyle->SetOptStat(0);
  TString year = "2017";
  //TString file_dir = "/uscms/home/joeyr/crabdirs/hists_k0ntupleulv1bmv2_summer20ul_miniaodv2/";
  TString file_dir = "./K0NtupleULV1Bmv2_Summer20UL_MiniAODv2/";
  TString out_dir = "/uscms/home/joeyr/publicweb/plots/K0study_2017/";
  TString fnmc = "background_btagpresel_"+year+".root";
  TString fndata = "BTagCSV"+year+".root";
  int rebin = 60;
  int nbins = 10;
  Double_t bins[] = {0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.9,2.0};
  TString plot_name = "h_dbv/hsig";
  std::cout << file_dir+fnmc << std::endl;
  TFile* fmc = TFile::Open(file_dir+fnmc);
  TFile* fdata = TFile::Open(file_dir+fndata);
  TH1D* h_mc = (TH1D*)fmc->Get(plot_name);
  TH1D* h_data = (TH1D*)fdata->Get(plot_name);

  h_mc->Scale(h_data->Integral(h_data->FindBin(0.4),h_data->FindBin(0.6))/h_mc->Integral(h_mc->FindBin(0.4),h_mc->FindBin(0.6)));

  //h_mc->Rebin(rebin);
  //h_data->Rebin(rebin);
  TH1D* h_data_new = (TH1D*)h_data->Rebin(nbins,"h_data_new", bins);
  TH1D* h_mc_new = (TH1D*)h_mc->Rebin(nbins,"h_mc_new", bins);
  h_data_new->SetMaximum(2*h_data_new->GetMaximum());
  h_mc_new->SetLineColor(kBlue);
  h_data_new->SetLineColor(kRed);
  TCanvas *c = new TCanvas("c","c",800,800);
  h_data_new->Draw();
  h_mc_new->Draw("same");
  TLegend* l = new TLegend(0.6,0.75,0.9,0.95);
  l->AddEntry(h_data_new, "data");
  l->AddEntry(h_mc_new, "background MC");

  TRatioPlot * rp = new TRatioPlot(h_data_new, h_mc_new);
  
  std::vector<double> lines = {};
  lines.push_back(1);
  rp->SetGridlines(lines);
  rp->SetH1DrawOpt("e");
  rp->SetH2DrawOpt("e");
  
  rp->Draw();
  rp->GetLowerRefGraph()->SetLineColor(kBlue);
  rp->GetLowerRefGraph()->SetMinimum(0.85);
  rp->GetLowerRefGraph()->SetMaximum(1.15);
  rp->GetLowerRefYaxis()->SetTitle("data/MC");
  //rp->GetUpperPad().SetLogy();
  rp->GetLowYaxis()->SetNdivisions(505);

  l->Draw();

  c->SaveAs(out_dir+"K0rho_"+year+".pdf");
}
