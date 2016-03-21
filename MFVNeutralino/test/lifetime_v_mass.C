#include <utility>

double xcut;
double ycut;
const char* crab_path = "crab/ABCDHistosV17_16";
const char* hist_path = "mfvAbcdHistosTrksJets";
bool plot = 0;
const char* plot_path = "plots/ABCD/lifetime_v_mass/version17/NoSig_bs2derr0p0025";
const double ymax = 50;
bool no_y_overflow = 0;
double ylow = 0.000;

std::pair<TH1D*,TH1D*> compareShapes(const char* sampleName, const char* histName) {
  TH1::SetDefaultSumw2();
  TFile* file = TFile::Open(TString::Format("%s/%s_scaled.root", crab_path, sampleName));
  TH2F* hist = (TH2F*)file->Get(TString::Format("%s/%s", hist_path, histName));

  int ybinlow = hist->GetYaxis()->FindBin(ylow);
  TH2F* cutHist = new TH2F("cutHist", TString::Format("y > %4.3f", ylow), hist->GetNbinsX(), hist->GetXaxis()->GetXmin(), hist->GetXaxis()->GetXmax(),
                                                                          hist->GetNbinsY(), hist->GetYaxis()->GetXmin(), hist->GetYaxis()->GetXmax());
  for (int i = 0; i <= hist->GetNbinsX() + 1; ++i) {
    for (int j = ybinlow; j <= hist->GetNbinsY() + 1; ++j) {
      cutHist->SetBinContent(i, j, hist->GetBinContent(i,j));
      cutHist->SetBinError(i, j, hist->GetBinError(i,j));
    }
  }

  int xbin = hist->GetXaxis()->FindBin(xcut);
  int ybin = hist->GetYaxis()->FindBin(ycut);
  printf("ylow = %f, ybinlow = %3d, ybinlow low edge = %f\n", ylow, ybinlow, hist->GetYaxis()->GetBinLowEdge(ybinlow));
  printf("ycut = %f, ybin-1  = %3d, ybin    low edge = %f\n", ycut, ybin-1, hist->GetYaxis()->GetBinLowEdge(ybin));

  int nbinsx = hist->GetNbinsX();
  int nbinsy = hist->GetNbinsY();

  double errA, errB, errC, errD;
  double A = hist->IntegralAndError(0, xbin-1, ybinlow, ybin-1, errA);
  double B = hist->IntegralAndError(0, xbin-1, ybin, nbinsy+1, errB);
  double C = hist->IntegralAndError(xbin, nbinsx+1, ybinlow, ybin-1, errC);
  double D = hist->IntegralAndError(xbin, nbinsx+1, ybin, nbinsy+1, errD);

  if (no_y_overflow) {
    A = hist->IntegralAndError(0, xbin-1, ybinlow, ybin-1, errA);
    B = hist->IntegralAndError(0, xbin-1, ybin, nbinsy, errB);
    C = hist->IntegralAndError(xbin, nbinsx+1, ybinlow, ybin-1, errC);
    D = hist->IntegralAndError(xbin, nbinsx+1, ybin, nbinsy, errD);
  }

  double Dpred = B/A*C;
  double errPred = Dpred * sqrt(errA/A * errA/A + errB/B * errB/B + errC/C * errC/C);

  printf("%35s A = %9.2f +/- %9.2f, B = %7.2f +/- %7.2f, C = %8.2f +/- %8.2f, D = %6.2f +/- %6.2f, B/A*C = %7.2f +/- %7.2f, C.F.= %5.2f\n", sampleName, A, errA, B, errB, C, errC, D, errD, Dpred, errPred, cutHist->GetCorrelationFactor());

  TH1D* h_low = hist->ProjectionY(TString::Format("%s_low_%s", histName, sampleName), 0, xbin-1);
  TH1D* h_high = hist->ProjectionY(TString::Format("%s_high_%s", histName, sampleName), xbin, nbinsx+1);

  if (plot) {
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
    c1->SaveAs(TString::Format("%s/%s_%d/%s.pdf", plot_path, histName, int(xcut), sampleName));
    c1->cd(1)->SetLogy();
    c1->cd(3)->SetLogy();
    h_low_normalized->GetYaxis()->SetRangeUser(0.00001,1);
    c1->cd(4)->SetLogy();
    c1->SaveAs(TString::Format("%s/%s_%d/%s_logy.pdf", plot_path, histName, int(xcut), sampleName));
  }

  h_high->SetDirectory(0);
  h_low->SetDirectory(0);
  file->Close();
  return std::make_pair(h_high, h_low);
}

void compareMasses(const char* lifetime, double xmax, const char* histName) {
  std::pair<TH1D*,TH1D*> h_pair_M0300 = compareShapes(TString::Format("mfv_neutralino_%s_M0300_1fb", lifetime), histName);
  std::pair<TH1D*,TH1D*> h_pair_M0400 = compareShapes(TString::Format("mfv_neutralino_%s_M0400_1fb", lifetime), histName);
  std::pair<TH1D*,TH1D*> h_pair_M0600 = compareShapes(TString::Format("mfv_neutralino_%s_M0600_1fb", lifetime), histName);
  std::pair<TH1D*,TH1D*> h_pair_M1000 = compareShapes(TString::Format("mfv_neutralino_%s_M1000_1fb", lifetime), histName);
  std::pair<TH1D*,TH1D*> h_pair_ttbar = compareShapes("ttbar", histName);
  std::pair<TH1D*,TH1D*> h_pair_background_nobigw = compareShapes("background_nobigw", histName);
  std::pair<TH1D*,TH1D*> h_pair_ttbar_sq_qcdht1000 = compareShapes("ttbar_sq_qcdht1000", histName);
  std::pair<TH1D*,TH1D*> h_pair_sb_ttbar_qcdht1000 = compareShapes("sb_ttbar_qcdht1000", histName);
  std::pair<TH1D*,TH1D*> h_pair_background = compareShapes("background", histName);

  TH1D* h_M0300 = h_pair_M0300.first;
  TH1D* h_M0400 = h_pair_M0400.first;
  TH1D* h_M0600 = h_pair_M0600.first;
  TH1D* h_M1000 = h_pair_M1000.first;
  TH1D* h_ttbar = h_pair_ttbar.first;
  TH1D* h_background_nobigw = h_pair_background_nobigw.first;
  TH1D* h_ttbar_sq_qcdht1000 = h_pair_ttbar_sq_qcdht1000.first;
  TH1D* h_sb_ttbar_qcdht1000 = h_pair_sb_ttbar_qcdht1000.first;
  TH1D* h_background = h_pair_background.first;

  if (plot) {
    TFile* file = TFile::Open(TString::Format("%s/%s_%d/%s.root", plot_path, histName, int(xcut), lifetime), "RECREATE");
    h_M0300->Write();
    h_M0400->Write();
    h_M0600->Write();
    h_M1000->Write();
    h_ttbar->Write();
    h_background_nobigw->Write();
    h_ttbar_sq_qcdht1000->Write();
    h_sb_ttbar_qcdht1000->Write();
    h_background->Write();

    h_pair_M0300.second->Write();
    h_pair_M0400.second->Write();
    h_pair_M0600.second->Write();
    h_pair_M1000.second->Write();
    h_pair_ttbar.second->Write();
    h_pair_background_nobigw.second->Write();
    h_pair_ttbar_sq_qcdht1000.second->Write();
    h_pair_sb_ttbar_qcdht1000.second->Write();
    h_pair_background.second->Write();
    file->Close();
  }

  TCanvas* c1 = new TCanvas();
  h_background->GetXaxis()->SetRangeUser(0,xmax);
  h_background->GetYaxis()->SetRangeUser(0,ymax);
  h_background->SetMarkerStyle(21);
  h_background->SetMarkerColor(9);
  h_background->SetLineColor(9)
  h_background->Draw();
  h_ttbar->SetMarkerStyle(21);
  h_ttbar->SetMarkerColor(2);
  h_ttbar->SetLineColor(2);
  h_ttbar->Draw("same");
  h_background_nobigw->SetMarkerStyle(21);
  h_background_nobigw->SetMarkerColor(3);
  h_background_nobigw->SetLineColor(3);
  h_background_nobigw->Draw("same");
  h_ttbar_sq_qcdht1000->SetMarkerStyle(21);
  h_ttbar_sq_qcdht1000->SetMarkerColor(4);
  h_ttbar_sq_qcdht1000->SetLineColor(4);
  h_ttbar_sq_qcdht1000->Draw("same");
  h_sb_ttbar_qcdht1000->SetMarkerStyle(21);
  h_sb_ttbar_qcdht1000->SetMarkerColor(6);
  h_sb_ttbar_qcdht1000->SetLineColor(6);
  h_sb_ttbar_qcdht1000->Draw("same");

  h_M0300->SetLineColor(14);
  h_M0300->Draw("same");
  h_M0400->SetLineColor(13);
  h_M0400->Draw("same");
  h_M0600->SetLineColor(12);
  h_M0600->Draw("same");
  h_M1000->SetLineColor(1);
  h_M1000->Draw("same");

  TLegend* legend = new TLegend(0.5,0.75,0.75,1.0);
  legend->AddEntry(h_background, "background", "LPE");
  legend->AddEntry(h_ttbar, "ttbar", "LPE");
  legend->AddEntry(h_background_nobigw, "ttbar+qcdht1000", "LPE");
  legend->AddEntry(h_ttbar_sq_qcdht1000, "ttbar+sq*qcdht1000", "LPE");
  legend->AddEntry(h_sb_ttbar_qcdht1000, "sb*(ttbar+qcdht1000)", "LPE");
  legend->AddEntry(h_M0300, "M0300", "LPE");
  legend->AddEntry(h_M0400, "M0400", "LPE");
  legend->AddEntry(h_M0600, "M0600", "LPE");
  legend->AddEntry(h_M1000, "M1000", "LPE");
  legend->SetFillColor(0);
  legend->Draw();

  if (plot) {
    c1->SaveAs(TString::Format("%s/%s_%d/%s.pdf", plot_path, histName, int(xcut), lifetime));
    h_background->GetYaxis()->SetRangeUser(0.0001,ymax);
    c1->SetLogy();
    c1->SaveAs(TString::Format("%s/%s_%d/%s_logy.pdf", plot_path, histName, int(xcut), lifetime));
  }

  TCanvas* c2 = new TCanvas();
  h_M1000->DrawNormalized();
  h_M0300->DrawNormalized("same");
  h_M0400->DrawNormalized("same");
  h_M0600->DrawNormalized("same");
  legend->Draw();
  if (plot) {
    c2->SaveAs(TString::Format("%s/%s_%d/%s_nobkg_normalized.pdf", plot_path, histName, int(xcut), lifetime));
    c2->SetLogy();
    c2->SaveAs(TString::Format("%s/%s_%d/%s_nobkg_normalized_logy.pdf", plot_path, histName, int(xcut), lifetime));
  }

  TCanvas* c3 = new TCanvas();
  TH1F* h_background_normalized = (TH1F*)h_background->Clone();
  h_background_normalized->Scale(1./h_background->Integral());
  h_background_normalized->GetYaxis()->SetRangeUser(0,1);
  h_background_normalized->Draw();
  h_ttbar->DrawNormalized("same");
  h_background_nobigw->DrawNormalized("same");
  h_ttbar_sq_qcdht1000->DrawNormalized("same");
  h_sb_ttbar_qcdht1000->DrawNormalized("same");
  h_M0300->DrawNormalized("same");
  h_M0400->DrawNormalized("same");
  h_M0600->DrawNormalized("same");
  h_M1000->DrawNormalized("same");
  legend->Draw();
  if (plot) {
    c3->SaveAs(TString::Format("%s/%s_%d/%s_normalized.pdf", plot_path, histName, int(xcut), lifetime));
    h_background_normalized->GetYaxis()->SetRangeUser(0.00001,1);
    c3->SetLogy();
    c3->SaveAs(TString::Format("%s/%s_%d/%s_normalized_logy.pdf", plot_path, histName, int(xcut), lifetime));
  }
}

void plot_all_samples(const char* histName) {
  printf("%s, xcut = %f, ycut = %f\n", histName, xcut, ycut);

  if (plot) {
    const char* cmd = TString::Format("mkdir %s/%s_%d", plot_path, histName, int(xcut));
    system(cmd);
//    compareMasses("tau0100um", 0.2, histName);
//    compareMasses("tau0300um", 0.3, histName);
//    compareMasses("tau1000um", 0.4, histName);
//    compareMasses("tau9900um", 1.0, histName);
  }

  compareShapes("mfv_neutralino_tau0300um_M0400_1fb", histName);
  compareShapes("mfv_neutralino_tau1000um_M0400_1fb", histName);
  compareShapes("ttbarhadronic", histName);
  compareShapes("ttbarsemilep", histName);
  compareShapes("ttbardilep", histName);
  compareShapes("ttbar", histName);
  compareShapes("qcdht0100", histName);
  compareShapes("qcdht0250", histName);
  compareShapes("qcdht0500", histName);
  compareShapes("qcdht1000", histName);
  compareShapes("qcd", histName);
//  compareShapes("ttbar_sq_qcdht1000", histName);
//  compareShapes("sb_ttbar_qcdht1000", histName);
//  compareShapes("background_nobigw", histName);
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
  ycut = 0.04;
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

void ht() {
  xcut = 600;
  ycut = 0.1;
//  plot_all_samples("h_bs2ddist01_ht");
//  plot_all_samples("h_pv2ddist01_ht");
//  plot_all_samples("h_pv3ddist01_ht");
//  plot_all_samples("h_pv3dctau01_ht");
  plot_all_samples("h_svdist2d_ht");
  plot_all_samples("h_svdist3d_ht");
//  plot_all_samples("h_svdist2dcmz_ht");
  plot_all_samples("h_svdist3dcmz_ht");
  plot_all_samples("h_svctau2dcmz_ht");
  plot_all_samples("h_svctau3dcmz_ht");
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
//  ntracks();
//  ht();
//  njets();
//  ycut = 0.1;
//  xcut = 40;  plot_all_samples("h_svctau3dcmz_maxtrackpt01");
//  xcut = 17;  plot_all_samples("h_svctau3dcmz_maxm1trackpt01");
//  xcut = 8;   plot_all_samples("h_svctau3dcmz_ntracksptgt301");
//  xcut = 700; plot_all_samples("h_svctau3dcmz_msptm01");

//  xcut = 16; ycut = 0.05; plot_all_samples("h_svdist2d_ntracks01");
  xcut =  8; ycut = 0.05; plot_all_samples("h_sv_best0_bs2ddist_ntracks");
}
