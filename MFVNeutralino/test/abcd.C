int iteration = 0;
double xcut = 15;
double ycut = 15;

void compareShapes(char* sampleName) {
  TH1::SetDefaultSumw2();
  TFile* file = TFile::Open(TString::Format("crab/ABCDHistosV13_%d/%s_scaled.root", iteration, sampleName));
  TH2F* hist = (TH2F*)abcdHistos->Get("h_ntracks01_maxtrackpt01");
  char* xname = "maxtrackpt01";
  char* yname = "ntracks01";

  int xbin = hist->GetXaxis()->FindBin(xcut);
  int ybin = hist->GetYaxis()->FindBin(ycut);

  int nbinsx = hist->GetNbinsX();
  double xlow = hist->GetXaxis()->GetXmin();
  double xup = hist->GetXaxis()->GetXmax();
  int nbinsy = hist->GetNbinsY();
  double ylow = hist->GetYaxis()->GetXmin();
  double yup = hist->GetYaxis()->GetXmax();

  TH1F* h_low = new TH1F(TString::Format("h_sv_%s_low_%s", yname, xname), TString::Format("low %s;%s;events", xname, yname), nbinsy, ylow, yup);
  TH1F* h_high = new TH1F(TString::Format("h_sv_%s_high_%s", yname, xname), TString::Format("high %s;%s;events", xname, yname), nbinsy, ylow, yup);
  for (int i = 0; i <= nbinsy+1; ++i) {
    h_low->SetBinContent(i, hist->Integral(0, xbin-1, i, i));
    h_high->SetBinContent(i, hist->Integral(xbin, nbinsx+1, i, i));
  }

  TCanvas* c1 = new TCanvas();
  c1->Divide(2,2);
  c1->cd(1);
  h_low->Draw();
  c1->cd(3);
  h_high->Draw();
  c1->cd(2);
  hist->Draw("colz");

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

//  c1->SaveAs(TString::Format("plots/ABCD/CutPlayV13/iter%d/%d_%d/%s.pdf", iteration, int(xcut), int(ycut), sampleName));

}

void abcd() {
  compareShapes("mfv_neutralino_tau0100um_M0400");
  compareShapes("mfv_neutralino_tau1000um_M0400");
  compareShapes("ttbarhadronic");
  compareShapes("ttbarsemilep");
  compareShapes("ttbardilep");
  compareShapes("ttbar");
  compareShapes("qcdht0100");
  compareShapes("qcdht0250");
  compareShapes("qcdht0500");
  compareShapes("qcdht1000");
  compareShapes("qcd");
  compareShapes("background");
}
