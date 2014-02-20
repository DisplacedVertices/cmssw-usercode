double xcut = 90;
double ycut = 0.1;

TH1D* compareShapes(char* sampleName, char* histName, char* yname) {
  TH1::SetDefaultSumw2();
  TFile* file = TFile::Open(TString::Format("crab/ABCDHistosV15_3/%s_scaled.root", sampleName));
  TH2F* hist = (TH2F*)abcdHistos->Get(histName);
  char* xname = "tkonlymass01";

  hist->Rebin2D(10,5);

  int xbin = hist->GetXaxis()->FindBin(xcut);
  int ybin = hist->GetYaxis()->FindBin(ycut);

  int nbinsx = hist->GetNbinsX();
  int nbinsy = hist->GetNbinsY();

  TH1D* h_low = hist->ProjectionY(TString::Format("h_%s_low_%s", yname, xname), 0, xbin-1);
  TH1D* h_high = hist->ProjectionY(TString::Format("h_%s_high_%s", yname, xname), xbin, nbinsx+1);

  TCanvas* c1 = new TCanvas();
  c1->Divide(2,2);
  c1->cd(1);
  h_low->Draw();
  c1->cd(3);
  TF1* fexp = new TF1("fexp", "exp([0]*x+[1])", 0.2, 1);
  TH1F* h_high_fit = h_high->Clone();
  h_high_fit->Fit("fexp", "RVWL");
  h_high_fit->Draw();
  c1->cd(2);
  hist->Draw("colz");
  c1->cd(4);
  h_low->SetLineColor(2);
  TH1F* h_low_normalized = h_low->Clone();
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

  c1->SaveAs(TString::Format("plots/ABCD/lifetime_v_mass/%s/%s.pdf", histName, sampleName));
  return h_high;
}

void compareMasses(char* lifetime, char* histName, char* yname) {
  TH1D* h_M0200 = compareShapes(TString::Format("mfv_neutralino_%s_M0200", lifetime), histName, yname);
  TH1D* h_M0300 = compareShapes(TString::Format("mfv_neutralino_%s_M0300", lifetime), histName, yname);
  TH1D* h_M0400 = compareShapes(TString::Format("mfv_neutralino_%s_M0400", lifetime), histName, yname);
  TH1D* h_M0600 = compareShapes(TString::Format("mfv_neutralino_%s_M0600", lifetime), histName, yname);
  TH1D* h_M0800 = compareShapes(TString::Format("mfv_neutralino_%s_M0800", lifetime), histName, yname);
  TH1D* h_M1000 = compareShapes(TString::Format("mfv_neutralino_%s_M1000", lifetime), histName, yname);

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
  c1->SaveAs(TString::Format("plots/ABCD/lifetime_v_mass/%s/%s.pdf", histName, lifetime));
}

void plot_all_samples(char* histName, char* yname) {
  compareMasses("tau0000um", histName, yname);
  compareMasses("tau0010um", histName, yname);
  compareMasses("tau0100um", histName, yname);
  compareMasses("tau0300um", histName, yname);
  compareMasses("tau1000um", histName, yname);
  compareMasses("tau9900um", histName, yname);

  compareShapes("ttbarhadronic", histName, yname);
  compareShapes("ttbarsemilep", histName, yname);
  compareShapes("ttbardilep", histName, yname);
  compareShapes("ttbar", histName, yname);
  compareShapes("qcdht0100", histName, yname);
  compareShapes("qcdht0250", histName, yname);
  compareShapes("qcdht0500", histName, yname);
  compareShapes("qcdht1000", histName, yname);
  compareShapes("qcd", histName, yname);
  compareShapes("background", histName, yname);
}

void lifetime_v_mass() {
  plot_all_samples("h_bs2ddist01_tkonlymass01", "bs2ddist01");
  plot_all_samples("h_pv2ddist01_tkonlymass01", "pv2ddist01");
  plot_all_samples("h_pv3ddist01_tkonlymass01", "pv3ddist01");
  plot_all_samples("h_pv3dtkonlyctau01_tkonlymass01", "pv3dtkonlyctau01");
  plot_all_samples("h_pv3djetsntkctau01_tkonlymass01", "pv3djetsntkctau01");
  plot_all_samples("h_pv3dtksjetsntkctau01_tkonlymass01", "pv3dtksjetsntkctau01");
  plot_all_samples("h_svdist2d_tkonlymass01", "svdist2d");
  plot_all_samples("h_svdist3d_tkonlymass01", "svdist3d");
  plot_all_samples("h_svdist3dcmz_tkonlymass01", "svdist3dcmz");
  plot_all_samples("h_svctau3dcmz_tkonlymass01", "svctau3dcmz");
}
