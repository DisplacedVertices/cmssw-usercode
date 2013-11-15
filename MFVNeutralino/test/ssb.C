const int niter = 1;
bool printall = 0;
bool plot = 0;

double nsig_total = 19788.362;
double nsig = 1023.41;

double nbkg_total = 211435861768.63;
double nbkg = 174811.73;

void maxSSB(TH1F* sigHist, TH1F* bkgHist) {
  if (printall) printf("%16s\tcut\t\ts\t\tb\tssb\tsig frac\tsig eff\t\tbkg frac\tbkg eff\n", sigHist->GetName());
  int nbins = sigHist->GetNbinsX();
  double xlow = sigHist->GetXaxis()->GetXmin();
  double xup = sigHist->GetXaxis()->GetXmax();
  TH1F* h_ssb = new TH1F("h_ssb", ";cut;ssb", nbins, xlow, xup);
  TH1F* h_sigfrac = new TH1F("h_sigfrac", ";cut;sig frac", nbins, xlow, xup);
  TH1F* h_bkgfrac = new TH1F("h_bkgfrac", ";cut;bkg frac", nbins, xlow, xup);
//  TH1F* h_ssbsb = new TH1F("h_ssbsb", ";cut;ssbsb", nbins, xlow, xup);

  double value = 0;
  double smax = 0;
  double bmax = 0;
  double ssb = 0;
  for (int i = 1; i <= nbins; i++) {
    double s = sigHist->GetBinContent(i);
    double b = bkgHist->GetBinContent(i);
//    double sigb = bkgHist->GetBinError(i);
    if (printall) printf("%16s\t%5.1f\t%9.2f\t%9.2f\t%6.2f\t%f\t%f\t%f\t%e\n", "", sigHist->GetBinLowEdge(i), s, b, s/sqrt(b), s/nsig, s/nsig_total, b/nbkg, b/nbkg_total);
    h_sigfrac->SetBinContent(i, s/nsig);
    h_bkgfrac->SetBinContent(i, b/nbkg);
    if (b != 0) {
      h_ssb->SetBinContent(i, s/sqrt(b));
    }
//    if (b+sigb > 0) {
//      h_ssbsb->SetBinContent(i, s/sqrt(b+sigb));
//    }

    if (s/sqrt(b) > ssb) {
      value = sigHist->GetBinLowEdge(i);
      smax = s;
      bmax = b;
      ssb = s/sqrt(b);
    }
  }
  if (printall) {
    printf("\n%16s\t%5.1f\t%9.2f\t%9.2f\t%6.2f\t%f\t%f\t%f\t%e\n\n\n", "max ssb", value, smax, bmax, ssb, smax/nsig, smax/nsig_total, bmax/nbkg, bmax/nbkg_total);
  } else {
    printf("%16s\t%5.1f\t%9.2f\t%9.2f\t%6.2f\t%f\t%f\t%f\t%e\n", sigHist->GetName(), value, smax, bmax, ssb, smax/nsig, smax/nsig_total, bmax/nbkg, bmax/nbkg_total);
  }

  if (plot) {
    TCanvas* c1 = new TCanvas();
    c1->Divide(2,2);
    c1->cd(1);
    sigHist->SetLineColor(kRed);
    sigHist->Draw();
    c1->cd(3);
    bkgHist->Draw();
    c1->cd(2);
    h_ssb->Draw();
//    h_ssbsb->Draw("same");
    c1->cd(4);
    h_sigfrac->SetLineColor(kRed);
    h_bkgfrac->SetLineColor(kBlue);
    if (h_sigfrac->GetMaximum() >= h_bkgfrac->GetMaximum()) {
      h_sigfrac->Draw();
      h_bkgfrac->Draw("same");
    } else {
      h_bkgfrac->Draw();
      h_sigfrac->Draw("same");
    }
    c1->SaveAs(TString::Format("plots/SSB/iter%d/%s.pdf", niter, sigHist->GetName()));
    TCanvas* c2 = new TCanvas();
    c2->Divide(2,2);
    c2->cd(1)->SetLogy();
    sigHist->SetLineColor(kRed);
    sigHist->Draw();
    c2->cd(3)->SetLogy();
    bkgHist->Draw();
    c2->cd(2)->SetLogy();
    h_ssb->Draw();
//    h_ssbsb->Draw("same");
    c2->cd(4)->SetLogy();
    h_sigfrac->SetLineColor(kRed);
    h_bkgfrac->SetLineColor(kBlue);
    if (h_sigfrac->GetMaximum() >= h_bkgfrac->GetMaximum()) {
      h_sigfrac->Draw();
      h_bkgfrac->Draw("same");
    } else {
      h_bkgfrac->Draw();
      h_sigfrac->Draw("same");
    }
    c2->SaveAs(TString::Format("plots/SSB/iter%d/%s_log.pdf", niter, sigHist->GetName()));
  }

  delete h_ssb;
//  delete h_ssbsb;
  delete h_sigfrac;
  delete h_bkgfrac;
}

void ssb() {
  const int nvars = 9;
  const char* hnames[nvars] = {"ntracks", "njetssharetks", "maxtrackpt", "drmin", "drmax", "bs2dsig", "ntracks01", "njetssharetks01", "maxtrackpt01"};

  for (int i = 0; i <= niter; i++) {
    printf("iteration %d\n", i);
    TFile* sigFile = TFile::Open(TString::Format("crab/CutPlay%d/mfv_neutralino_tau0100um_M0400_1pb.root", i));
    TFile* bkgFile = TFile::Open(TString::Format("crab/CutPlay%d/background.root", i));

    if (!printall) printf("variable\t\tcut\t\ts\t\tb\tmax ssb\tsig frac\tsig eff\t\tbkg frac\tbkg eff\n");
    for (int j = 0; j < nvars; j++) {
      TH1F* sigHist = (TH1F*)sigFile->Get(hnames[j]);
      TH1F* bkgHist = (TH1F*)bkgFile->Get(hnames[j]);
      maxSSB(sigHist, bkgHist);
    }
    printf("\n");
  }
}
