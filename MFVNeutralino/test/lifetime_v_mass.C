int iteration = 30;
double xcut = 90;
double ycut = 0.02;

void compareShapes(char* sampleName) {
  TH1::SetDefaultSumw2();
  TFile* file = TFile::Open(TString::Format("crab/ABCDHistosV13_%db/%s_scaled.root", iteration, sampleName));
  TH2F* hist = (TH2F*)abcdHistos->Get("h_bs2ddist01_tkonlymass01");
  char* xname = "tkonlymass01";
  char* yname = "bs2ddist01";

  hist->Rebin2D(10,100);

  int xbin = hist->GetXaxis()->FindBin(xcut);
  int ybin = hist->GetYaxis()->FindBin(ycut);

  int nbinsx = hist->GetNbinsX();
  double xlow = hist->GetXaxis()->GetXmin();
  double xup = hist->GetXaxis()->GetXmax();
  int nbinsy = hist->GetNbinsY();
  double ylow = hist->GetYaxis()->GetXmin();
  double yup = hist->GetYaxis()->GetXmax();

  TH1D* h_low = hist->ProjectionY(TString::Format("h_%s_low_%s", yname, xname), 0, xbin-1);
  TH1D* h_high = hist->ProjectionY(TString::Format("h_%s_high_%s", yname, xname), xbin, nbinsx+1);

  int bin30 = hist->GetXaxis()->FindBin(30);
  int bin60 = hist->GetXaxis()->FindBin(60);
  int bin90 = hist->GetXaxis()->FindBin(90);
  int bin120 = hist->GetXaxis()->FindBin(120);

  TH1D* h_py_0_30 = hist->ProjectionY("h_py_0_30", 0, bin30-1);
  TH1D* h_py_30_60 = hist->ProjectionY("h_py_30_60", bin30, bin60-1);
  TH1D* h_py_60_90 = hist->ProjectionY("h_py_60_90", bin60, bin90-1);
  TH1D* h_py_90_120 = hist->ProjectionY("h_py_90_120", bin90, bin120-1);
  TH1D* h_py_120_inf = hist->ProjectionY("h_py_120_inf", bin120, nbinsx+1);

  TCanvas* c1 = new TCanvas();
  c1->Divide(2,2);
  c1->cd(1);
  h_low->Draw();
  c1->cd(3);
  h_high->Draw();
  c1->cd(2);
  hist->Draw("colz");

  c1->cd(4);
//  h_py_0_30->SetLineColor(kRed);
//  h_py_0_30->DrawNormalized();
  h_py_30_60->SetLineColor(kRed-7);
  h_py_30_60->SetLineWidth(2);
  h_py_30_60->DrawNormalized();
  h_py_60_90->SetLineColor(kRed);
  h_py_60_90->SetLineWidth(2);
  h_py_60_90->DrawNormalized("sames");
  h_py_90_120->SetLineColor(kRed+3);
  h_py_90_120->SetLineWidth(2);
  h_py_90_120->DrawNormalized("sames");
  h_py_120_inf->SetLineColor(kBlack);
  h_py_120_inf->SetLineWidth(2);
  h_py_120_inf->DrawNormalized("sames");

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

/*
  c1->cd(4);
  int nevents = h_low->Integral();
  double normalization = C/A * nevents;
  h_low->SetLineColor(2);
  if (h_high->GetMaximum() >= C/A * h_low->GetMaximum()) {
    h_high->Draw();
    h_low->DrawNormalized("same", normalization);
  } else {
    h_low->DrawNormalized("", normalization);
    h_high->Draw("same");
  }
*/

//  c1->SaveAs(TString::Format("plots/ABCD/CutPlayV13/iter%d/%d_%d/%s.root", iteration, int(xcut), int(ycut), sampleName));

}

void lifetime_v_mass() {

/*
compareShapes("mfv_neutralino_tau0000um_M0200");
compareShapes("mfv_neutralino_tau0000um_M0300");
compareShapes("mfv_neutralino_tau0000um_M0400");
compareShapes("mfv_neutralino_tau0000um_M0600");
compareShapes("mfv_neutralino_tau0000um_M0800");
compareShapes("mfv_neutralino_tau0010um_M0200");
compareShapes("mfv_neutralino_tau0010um_M0300");
compareShapes("mfv_neutralino_tau0010um_M0400");
compareShapes("mfv_neutralino_tau0010um_M0600");
compareShapes("mfv_neutralino_tau0010um_M0800");
compareShapes("mfv_neutralino_tau0010um_M1000");
compareShapes("mfv_neutralino_tau0100um_M0200");
compareShapes("mfv_neutralino_tau0100um_M0300");
compareShapes("mfv_neutralino_tau0100um_M0400");
compareShapes("mfv_neutralino_tau0100um_M0600");
compareShapes("mfv_neutralino_tau0100um_M0800");
compareShapes("mfv_neutralino_tau0100um_M1000");
compareShapes("mfv_neutralino_tau0300um_M0200");
compareShapes("mfv_neutralino_tau0300um_M0300");
compareShapes("mfv_neutralino_tau0300um_M0400");
compareShapes("mfv_neutralino_tau0300um_M0600");
compareShapes("mfv_neutralino_tau0300um_M0800");
compareShapes("mfv_neutralino_tau0300um_M1000");
compareShapes("mfv_neutralino_tau1000um_M0200");
compareShapes("mfv_neutralino_tau1000um_M0300");
compareShapes("mfv_neutralino_tau1000um_M0400");
compareShapes("mfv_neutralino_tau1000um_M0600");
compareShapes("mfv_neutralino_tau1000um_M0800");
compareShapes("mfv_neutralino_tau1000um_M1000");
compareShapes("mfv_neutralino_tau9900um_M0200");
compareShapes("mfv_neutralino_tau9900um_M0300");
compareShapes("mfv_neutralino_tau9900um_M0400");
compareShapes("mfv_neutralino_tau9900um_M0600");
compareShapes("mfv_neutralino_tau9900um_M0800");
compareShapes("mfv_neutralino_tau9900um_M1000");
printf("\n");
*/

//  compareShapes("mfv_neutralino_tau0100um_M0400");
  compareShapes("mfv_neutralino_tau1000um_M0400");
//  compareShapes("ttbarhadronic");
//  compareShapes("ttbarsemilep");
//  compareShapes("ttbardilep");
//  compareShapes("ttbar");
//  compareShapes("qcdht0100");
//  compareShapes("qcdht0250");
//  compareShapes("qcdht0500");
//  compareShapes("qcdht1000");
//  compareShapes("qcd");
  compareShapes("background");
}
