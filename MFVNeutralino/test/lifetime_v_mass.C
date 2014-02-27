#include "TH2.h"
#include "TFile.h"
#include "TString.h"
#include "TCanvas.h"
#include "TF1.h"

double xcut;
double ycut;

TH1D* compareShapes(const char* sampleName, const char* histName) {
  TH1::SetDefaultSumw2();
  TFile* file = TFile::Open(TString::Format("crab/ABCDHistosV15_6/%s_scaled.root", sampleName));
  TH2F* hist = (TH2F*)file->Get(TString::Format("abcdHistosTrksJets/%s", histName));

  hist->Rebin2D(10,5);

  int xbin = hist->GetXaxis()->FindBin(xcut);
  int ybin = hist->GetYaxis()->FindBin(ycut);

  int nbinsx = hist->GetNbinsX();
  int nbinsy = hist->GetNbinsY();

  TH1D* h_low = hist->ProjectionY(TString::Format("%s_low_%s", histName, sampleName), 0, xbin-1);
  TH1D* h_high = hist->ProjectionY(TString::Format("%s_high_%s", histName, sampleName), xbin, nbinsx+1);

  TCanvas* c1 = new TCanvas();
  c1->Divide(2,2);
  c1->cd(1);
  h_low->Draw();
  c1->cd(3);
  TF1* fexp = new TF1("fexp", "exp([0]*x+[1])", 0.2, 1);
  TH1F* h_high_fit = (TH1F*)h_high->Clone();
  h_high_fit->Fit("fexp", "RVWL");
  h_high_fit->Draw();
  c1->cd(2);
  hist->Draw("colz");
  c1->cd(4);
  h_low->SetLineColor(2);
  TH1F* h_low_normalized = (TH1F*)h_low->Clone();
  h_low_normalized->Scale(1./h_low->Integral());
  h_low_normalized->GetYaxis()->SetRangeUser(0,1);
  h_low_normalized->Draw();
  h_high->DrawNormalized("same");

  double errA, errB, errC, errD;
  double A = hist->IntegralAndError(0, xbin-1, 0, ybin-1, errA);
  double B = hist->IntegralAndError(0, xbin-1, ybin, nbinsy+1, errB);
  double C = hist->IntegralAndError(xbin, nbinsx+1, 0, ybin-1, errC);
  double D = hist->IntegralAndError(xbin, nbinsx+1, ybin, nbinsy+1, errD);

  double Dpred = B/A*C;
  double errPred = Dpred * sqrt(errA/A * errA/A + errB/B * errB/B + errC/C * errC/C);

  printf("%s\n", sampleName);
  printf("\tA = %5.2f +/- %5.2f, B = %5.2f +/- %5.2f, C = %5.2f +/- %5.2f, D = %5.2f +/- %5.2f\n", A, errA, B, errB, C, errC, D, errD);
  printf("\tD = %5.2f +/- %5.2f, B/A*C = %5.2f +/- %5.2f, correlation factor = %5.2f\n", D, errD, Dpred, errPred, hist->GetCorrelationFactor());

  c1->SaveAs(TString::Format("plots/ABCD/lifetime_v_mass/TrksJets/%s/%s.pdf", histName, sampleName));
  c1->SaveAs(TString::Format("plots/ABCD/lifetime_v_mass/TrksJets/%s/%s.root", histName, sampleName));
  return h_high;
}

void compareMasses(const char* lifetime, const char* histName) {
  TH1D* h_M0200 = compareShapes(TString::Format("mfv_neutralino_%s_M0200", lifetime), histName);
  TH1D* h_M0300 = compareShapes(TString::Format("mfv_neutralino_%s_M0300", lifetime), histName);
  TH1D* h_M0400 = compareShapes(TString::Format("mfv_neutralino_%s_M0400", lifetime), histName);
  TH1D* h_M0600 = compareShapes(TString::Format("mfv_neutralino_%s_M0600", lifetime), histName);
  TH1D* h_M0800 = compareShapes(TString::Format("mfv_neutralino_%s_M0800", lifetime), histName);
  TH1D* h_M1000 = compareShapes(TString::Format("mfv_neutralino_%s_M1000", lifetime), histName);

  TCanvas* c1 = new TCanvas();
  c1->SetLogy(1);
  h_M1000->SetLineColor(1);
  h_M1000->Draw();
  h_M0800->SetLineColor(2);
  h_M0800->Draw("same");
  h_M0600->SetLineColor(3);
  h_M0600->Draw("same");
  h_M0400->SetLineColor(4);
  h_M0400->Draw("same");
  h_M0300->SetLineColor(7);
  h_M0300->Draw("same");
  h_M0200->SetLineColor(6);
  h_M0200->Draw("same");
  c1->SaveAs(TString::Format("plots/ABCD/lifetime_v_mass/TrksJets/%s/%s.pdf", histName, lifetime));
}

void plot_all_samples(const char* histName) {
  compareMasses("tau0000um", histName);
  compareMasses("tau0010um", histName);
  compareMasses("tau0100um", histName);
  compareMasses("tau0300um", histName);
  compareMasses("tau1000um", histName);
  compareMasses("tau9900um", histName);

  compareShapes("ttbarhadronic", histName);
  compareShapes("ttbarsemilep", histName);
  compareShapes("ttbardilep", histName);
  compareShapes("ttbar", histName);
  compareShapes("qcdht0100", histName);
  compareShapes("qcdht0250", histName);
  compareShapes("qcdht0500", histName);
  compareShapes("qcdht1000", histName);
  compareShapes("qcd", histName);
  compareShapes("background", histName);
}

void lifetime_v_mass() {
  xcut = 90;
  ycut = 0.1;
  plot_all_samples("h_bs2ddist01_mass01");
  plot_all_samples("h_pv2ddist01_mass01");
  plot_all_samples("h_pv3ddist01_mass01");
  plot_all_samples("h_pv3dctau01_mass01");
  plot_all_samples("h_svdist2d_mass01");
  plot_all_samples("h_svdist3d_mass01");
  plot_all_samples("h_svdist2dcmz_mass01");
  plot_all_samples("h_svdist3dcmz_mass01");
  plot_all_samples("h_svctau2dcmz_mass01");
  plot_all_samples("h_svctau3dcmz_mass01");

  xcut = 45;
  ycut = 0.05;
  plot_all_samples("h_bs2ddist0_mass0");
  plot_all_samples("h_pv2ddist0_mass0");
  plot_all_samples("h_pv3ddist0_mass0");
  plot_all_samples("h_pv3dctau0_mass0");
}
