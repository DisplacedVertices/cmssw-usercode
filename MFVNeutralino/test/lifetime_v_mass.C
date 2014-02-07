double xcut = 90;
double ycut = 0.1;

void compareShapes(char* sampleName, char* histName, char* yname) {
  TH1::SetDefaultSumw2();
  TFile* file = TFile::Open(TString::Format("crab/ABCDHistosV13_30f/%s_scaled.root", sampleName));
  TH2F* hist = (TH2F*)abcdHistos->Get(histName);
  char* xname = "tkonlymass01";

  hist->Rebin2D(10,10);

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
  h_high->Draw();
  c1->cd(2);
  hist->Draw("colz");
  c1->cd(4);
  h_low->SetLineColor(2);
  h_low->DrawNormalized();
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

//  c1->SaveAs(TString::Format("plots/ABCD/lifetime_v_mass/%s/%s.pdf", histName, sampleName));
//  c1->SaveAs(TString::Format("plots/ABCD/lifetime_v_mass/%s/%s.root", histName, sampleName));

}

void plot_all_samples(char* histName, char* yname) {
  compareShapes("mfv_neutralino_tau0000um_M0200", histName, yname);
  compareShapes("mfv_neutralino_tau0000um_M0300", histName, yname);
  compareShapes("mfv_neutralino_tau0000um_M0400", histName, yname);
  compareShapes("mfv_neutralino_tau0000um_M0600", histName, yname);
  compareShapes("mfv_neutralino_tau0000um_M0800", histName, yname);
  compareShapes("mfv_neutralino_tau0010um_M0200", histName, yname);
  compareShapes("mfv_neutralino_tau0010um_M0300", histName, yname);
  compareShapes("mfv_neutralino_tau0010um_M0400", histName, yname);
  compareShapes("mfv_neutralino_tau0010um_M0600", histName, yname);
  compareShapes("mfv_neutralino_tau0010um_M0800", histName, yname);
  compareShapes("mfv_neutralino_tau0010um_M1000", histName, yname);
  compareShapes("mfv_neutralino_tau0100um_M0200", histName, yname);
  compareShapes("mfv_neutralino_tau0100um_M0300", histName, yname);
  compareShapes("mfv_neutralino_tau0100um_M0400", histName, yname);
  compareShapes("mfv_neutralino_tau0100um_M0600", histName, yname);
  compareShapes("mfv_neutralino_tau0100um_M0800", histName, yname);
  compareShapes("mfv_neutralino_tau0100um_M1000", histName, yname);
  compareShapes("mfv_neutralino_tau0300um_M0200", histName, yname);
  compareShapes("mfv_neutralino_tau0300um_M0300", histName, yname);
  compareShapes("mfv_neutralino_tau0300um_M0400", histName, yname);
  compareShapes("mfv_neutralino_tau0300um_M0600", histName, yname);
  compareShapes("mfv_neutralino_tau0300um_M0800", histName, yname);
  compareShapes("mfv_neutralino_tau0300um_M1000", histName, yname);
  compareShapes("mfv_neutralino_tau1000um_M0200", histName, yname);
  compareShapes("mfv_neutralino_tau1000um_M0300", histName, yname);
  compareShapes("mfv_neutralino_tau1000um_M0400", histName, yname);
  compareShapes("mfv_neutralino_tau1000um_M0600", histName, yname);
  compareShapes("mfv_neutralino_tau1000um_M0800", histName, yname);
  compareShapes("mfv_neutralino_tau1000um_M1000", histName, yname);
  compareShapes("mfv_neutralino_tau9900um_M0200", histName, yname);
  compareShapes("mfv_neutralino_tau9900um_M0300", histName, yname);
  compareShapes("mfv_neutralino_tau9900um_M0400", histName, yname);
  compareShapes("mfv_neutralino_tau9900um_M0600", histName, yname);
  compareShapes("mfv_neutralino_tau9900um_M0800", histName, yname);
  compareShapes("mfv_neutralino_tau9900um_M1000", histName, yname);
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
}
