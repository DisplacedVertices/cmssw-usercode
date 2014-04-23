double xcut;
double ycut;
const char* crab_path = "crab/ABCDHistosV17_1";
const char* hist_path = "abcdHistosTrksJets";
const char* plot_path = "plots/ABCD/lifetime_v_mass/version17/TrksJets";

TH1D* compareShapes(const char* sampleName, const char* histName) {
  TH1::SetDefaultSumw2();
  TFile* file = TFile::Open(TString::Format("%s/%s_scaled.root", crab_path, sampleName));
  TH2F* hist = (TH2F*)file->Get(TString::Format("%s/%s", hist_path, histName));

  int xbin = hist->GetXaxis()->FindBin(xcut);
  int ybin = hist->GetYaxis()->FindBin(ycut);

  int nbinsx = hist->GetNbinsX();
  int nbinsy = hist->GetNbinsY();

  TH1D* h_low = hist->ProjectionY(TString::Format("%s_low_%s", histName, sampleName), 0, xbin-1);
  TH1D* h_high = hist->ProjectionY(TString::Format("%s_high_%s", histName, sampleName), xbin, nbinsx+1);

  TCanvas* c1 = new TCanvas();
  c1->Divide(2,2);
  h_low->SetLineColor(2);
  TF1* fexp = new TF1("fexp", "exp([0]*x+[1])", 0.2, 1);
  c1->cd(1);
  TH1F* h_low_fit = (TH1F*)h_low->Clone();
  h_low_fit->Fit("fexp", "IRVWL");
  h_low_fit->Draw();
  double errAB;
  double AB = h_low->IntegralAndError(0, nbinsy+1, errAB);
  TLatex* text_low = new TLatex(0.6, 0.5, TString::Format("%.1f #pm %.1f", AB, errAB));
  text_low->SetNDC();
  text_low->Draw();
  c1->cd(3);
  TH1F* h_high_fit = (TH1F*)h_high->Clone();
  h_high_fit->Fit("fexp", "IRVWL");
  h_high_fit->Draw();
  double errCD;
  double CD = h_high->IntegralAndError(0, nbinsy+1, errCD);
  TLatex* text_high = new TLatex(0.6, 0.5, TString::Format("%.1f #pm %.1f", CD, errCD));
  text_high->SetNDC();
  text_high->Draw();
  c1->cd(2);
  hist->Draw("colz");
  TLine* line = new TLine(xcut, 0, xcut, hist->GetYaxis()->GetXmax());
  line->SetLineStyle(2);
  line->Draw();
  c1->cd(4);
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

  printf("%30s\tA = %5.2f +/- %5.2f, B = %5.2f +/- %5.2f, C = %5.2f +/- %5.2f, D = %5.2f +/- %5.2f\n", sampleName, A, errA, B, errB, C, errC, D, errD);
  printf("%30s\tD = %5.2f +/- %5.2f, B/A*C = %5.2f +/- %5.2f, correlation factor = %5.2f\n", "", D, errD, Dpred, errPred, hist->GetCorrelationFactor());

  c1->SaveAs(TString::Format("%s/%s/%s.pdf", plot_path, histName, sampleName));
/*
  c1->cd(1)->SetLogy();
  c1->cd(3)->SetLogy();
  h_low_normalized->GetYaxis()->SetRangeUser(0.00001,1);
  c1->cd(4)->SetLogy();
  c1->SaveAs(TString::Format("%s/%s/%s_logy.pdf", plot_path, histName, sampleName));
*/
  h_high->SetDirectory(0);
  file->Close();
  return h_high;
}

void compareMasses(const char* lifetime, double xmax, const char* histName) {
  TH1D* h_M0200 = compareShapes(TString::Format("mfv_neutralino_%s_M0200", lifetime), histName);
  TH1D* h_M0300 = compareShapes(TString::Format("mfv_neutralino_%s_M0300", lifetime), histName);
  TH1D* h_M0400 = compareShapes(TString::Format("mfv_neutralino_%s_M0400", lifetime), histName);
  TH1D* h_M0600 = compareShapes(TString::Format("mfv_neutralino_%s_M0600", lifetime), histName);
  TH1D* h_M0800 = compareShapes(TString::Format("mfv_neutralino_%s_M0800", lifetime), histName);
  TH1D* h_M1000 = compareShapes(TString::Format("mfv_neutralino_%s_M1000", lifetime), histName);

  TH1D* h_ttbar = compareShapes("ttbar", histName);
  TH1D* h_background_nobigw = compareShapes("background_nobigw", histName);
  TH1D* h_background_qcdht1000 = compareShapes("background_qcdht1000", histName);
  TH1D* h_background_noqcdht0500 = compareShapes("background_noqcdht0500", histName);
  TH1D* h_background = compareShapes("background", histName);

  TCanvas* c1 = new TCanvas();
  h_background->GetXaxis()->SetRangeUser(0,xmax);
  h_background->GetYaxis()->SetRangeUser(0,50);
  h_background->SetMarkerStyle(21);
  h_background->Draw();
  h_ttbar->SetMarkerStyle(21);
  h_ttbar->SetMarkerColor(2);
  h_ttbar->Draw("same");
  h_background_nobigw->SetMarkerStyle(21);
  h_background_nobigw->SetMarkerColor(3);
  h_background_nobigw->Draw("same");
  h_background_qcdht1000->SetMarkerStyle(21);
  h_background_qcdht1000->SetMarkerColor(4);
  h_background_qcdht1000->Draw("same");
  h_background_noqcdht0500->SetMarkerStyle(21);
  h_background_noqcdht0500->SetMarkerColor(6);
  h_background_noqcdht0500->Draw("same");

  h_M0200->SetLineColor(1);
  h_M0200->Draw("same");
  h_M0300->SetLineColor(2);
  h_M0300->Draw("same");
  h_M0400->SetLineColor(3);
  h_M0400->Draw("same");
  h_M0600->SetLineColor(4);
  h_M0600->Draw("same");
  h_M0800->SetLineColor(6);
  h_M0800->Draw("same");
  h_M1000->SetLineColor(7);
  h_M1000->Draw("same");

  TLegend* legend = new TLegend(0.5,0.75,0.75,1.0);
  legend->AddEntry(h_background, "background", "LPE");
  legend->AddEntry(h_ttbar, "ttbar", "LPE");
  legend->AddEntry(h_background_nobigw, "background_nobigw", "LPE");
  legend->AddEntry(h_background_qcdht1000, "background_qcdht1000", "LPE");
  legend->AddEntry(h_background_noqcdht0500, "background_noqcdht0500", "LPE");
  legend->AddEntry(h_M0200, "M0200", "LPE");
  legend->AddEntry(h_M0300, "M0300", "LPE");
  legend->AddEntry(h_M0400, "M0400", "LPE");
  legend->AddEntry(h_M0600, "M0600", "LPE");
  legend->AddEntry(h_M0800, "M0800", "LPE");
  legend->AddEntry(h_M1000, "M1000", "LPE");
  legend->SetFillColor(0);
  legend->Draw();

  c1->SaveAs(TString::Format("%s/%s/%s.pdf", plot_path, histName, lifetime));
  h_background->GetYaxis()->SetRangeUser(0.0001,50);
  c1->SetLogy();
  c1->SaveAs(TString::Format("%s/%s/%s_logy.pdf", plot_path, histName, lifetime));

  TCanvas* c2 = new TCanvas();
  h_background->DrawNormalized();
  h_ttbar->DrawNormalized("same");
  h_background_nobigw->DrawNormalized("same");
  h_background_qcdht1000->DrawNormalized("same");
  h_background_noqcdht0500->DrawNormalized("same");
  h_M0200->DrawNormalized("same");
  h_M0300->DrawNormalized("same");
  h_M0400->DrawNormalized("same");
  h_M0600->DrawNormalized("same");
  h_M0800->DrawNormalized("same");
  h_M1000->DrawNormalized("same");
  legend->Draw();

  c2->SaveAs(TString::Format("%s/%s/%s_normalized.pdf", plot_path, histName, lifetime));
  c2->SetLogy();
  c2->SaveAs(TString::Format("%s/%s/%s_normalized_logy.pdf", plot_path, histName, lifetime));
}

void plot_all_samples(const char* histName) {
  printf("%s\n", histName);
  const char* cmd = TString::Format("mkdir %s/%s", plot_path, histName);
  system(cmd);

  compareMasses("tau0100um", 0.2, histName);
  compareMasses("tau0300um", 0.3, histName);
  compareMasses("tau1000um", 0.4, histName);
  compareMasses("tau9900um", 1.0, histName);

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

  printf("\n");
}

void mass() {
  xcut = 250;
  ycut = 0.1;
//  plot_all_samples("h_bs2ddist01_mass01");
//  plot_all_samples("h_pv2ddist01_mass01");
//  plot_all_samples("h_pv3ddist01_mass01");
//  plot_all_samples("h_pv3dctau01_mass01");
  plot_all_samples("h_svdist2d_mass01");
  plot_all_samples("h_svdist3d_mass01");
//  plot_all_samples("h_svdist2dcmz_mass01");
  plot_all_samples("h_svdist3dcmz_mass01");
  plot_all_samples("h_svctau2dcmz_mass01");
  plot_all_samples("h_svctau3dcmz_mass01");

/*
  xcut = 45;
  ycut = 0.05;
  plot_all_samples("h_bs2ddist0_mass0");
  plot_all_samples("h_pv2ddist0_mass0");
  plot_all_samples("h_pv3ddist0_mass0");
  plot_all_samples("h_pv3dctau0_mass0");
*/
}

void ntracks() {
  xcut = 12;
  ycut = 0.05;
//  plot_all_samples("h_bs2ddist01_ntracks01");
//  plot_all_samples("h_pv2ddist01_ntracks01");
//  plot_all_samples("h_pv3ddist01_ntracks01");
//  plot_all_samples("h_pv3dctau01_ntracks01");
  plot_all_samples("h_svdist2d_ntracks01");
  plot_all_samples("h_svdist3d_ntracks01");
//  plot_all_samples("h_svdist2dcmz_ntracks01");
  plot_all_samples("h_svdist3dcmz_ntracks01");
  plot_all_samples("h_svctau2dcmz_ntracks01");
  plot_all_samples("h_svctau3dcmz_ntracks01");

/*
  xcut = 12;
  ycut = 0.05;
  plot_all_samples("h_bs2ddist0_ntracks01");
  plot_all_samples("h_pv2ddist0_ntracks01");
  plot_all_samples("h_pv3ddist0_ntracks01");
  plot_all_samples("h_pv3dctau0_ntracks01");

  xcut = 7;
  ycut = 0.05;
  plot_all_samples("h_bs2ddist0_ntracks0");
  plot_all_samples("h_pv2ddist0_ntracks0");
  plot_all_samples("h_pv3ddist0_ntracks0");
  plot_all_samples("h_pv3dctau0_ntracks0");
*/
}

void sumht() {
  xcut = 600;
  ycut = 0.1;
//  plot_all_samples("h_bs2ddist01_sumht");
//  plot_all_samples("h_pv2ddist01_sumht");
//  plot_all_samples("h_pv3ddist01_sumht");
//  plot_all_samples("h_pv3dctau01_sumht");
  plot_all_samples("h_svdist2d_sumht");
  plot_all_samples("h_svdist3d_sumht");
//  plot_all_samples("h_svdist2dcmz_sumht");
  plot_all_samples("h_svdist3dcmz_sumht");
  plot_all_samples("h_svctau2dcmz_sumht");
  plot_all_samples("h_svctau3dcmz_sumht");
}

void njets() {
  xcut = 5;
  ycut = 0.1;
  plot_all_samples("h_bs2ddist01_njets");
  plot_all_samples("h_pv2ddist01_njets");
  plot_all_samples("h_pv3ddist01_njets");
  plot_all_samples("h_pv3dctau01_njets");
  plot_all_samples("h_svdist2d_njets");
  plot_all_samples("h_svdist3d_njets");
  plot_all_samples("h_svdist2dcmz_njets");
  plot_all_samples("h_svdist3dcmz_njets");
  plot_all_samples("h_svctau2dcmz_njets");
  plot_all_samples("h_svctau3dcmz_njets");
}

void lifetime_v_mass() {
//  mass();
  ntracks();
//  sumht();
//  njets();
//  ycut = 0.1;
//  xcut = 40;  plot_all_samples("h_svctau3dcmz_maxtrackpt01");
//  xcut = 17;  plot_all_samples("h_svctau3dcmz_maxm1trackpt01");
//  xcut = 8;   plot_all_samples("h_svctau3dcmz_ntracksptgt301");
//  xcut = 700; plot_all_samples("h_svctau3dcmz_msptm01");
}
