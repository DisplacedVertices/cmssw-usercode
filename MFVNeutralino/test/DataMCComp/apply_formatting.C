
void format_h_dat(TH1F*& h_dat) {
  h_dat->SetMarkerStyle(20);
  h_dat->SetMarkerSize(0.6);
  h_dat->SetLineColor(kBlack);
  h_dat->SetLineWidth(2);
}


// format_h_mc() not implemented



void format_mc_stat(TH1*& h_mc_stat) {
  h_mc_stat->SetFillStyle(3144);
  h_mc_stat->SetFillColorAlpha(kBlack, 0.6);
  h_mc_stat->SetMarkerSize(0);
}



void format_h_sig(TH1F* hsig) {
  hsig->SetFillStyle(3008);
  hsig->SetLineWidth(0); // Does nothing
  hsig->SetMarkerSize(-1);
}



void format_legend(TLegend*& legend) {
  legend->SetFillColorAlpha(kWhite, 0.60);
  legend->SetBorderSize(0);
  legend->SetTextSize(0.033);
}



void format_tlx(TLatex*& tlx) {
  tlx->SetNDC();
  tlx->SetTextAlign(13);
  tlx->SetTextFont(42);
  tlx->SetTextSize(0.032);
  tlx->SetLineWidth(2);
}



void format_qt_ln(TLine*& qt_ln, const EColor lncol, const bool is_mn=true) {
  if (is_mn) {
    qt_ln->SetLineColorAlpha(lncol, 0.5);
    qt_ln->SetLineStyle(1);
    qt_ln->SetLineWidth(3);
  } else {
    qt_ln->SetLineColorAlpha(lncol, 0.4);
    qt_ln->SetLineStyle(2);
    qt_ln->SetLineWidth(2);
  }
}



void format_rat(TH1F*& h_rat, const TH1F* h_dat, const EColor ratcol, const float ratio_font_scale) {
  h_rat->SetLineColor(ratcol);
  h_rat->SetMarkerColor(ratcol);
  h_rat->SetMarkerSize(0);

  h_rat->GetXaxis()->SetTitleSize(h_dat->GetXaxis()->GetTitleSize()*ratio_font_scale);
  h_rat->GetYaxis()->SetTitleSize(h_dat->GetYaxis()->GetTitleSize()*ratio_font_scale);
  h_rat->GetXaxis()->SetLabelSize(h_dat->GetXaxis()->GetLabelSize()*ratio_font_scale);
  h_rat->GetYaxis()->SetLabelSize(h_dat->GetYaxis()->GetLabelSize()*ratio_font_scale);
  h_rat->GetXaxis()->SetTitle("");
  h_rat->GetYaxis()->SetTitle("Data to MC Ratio");
}



void format_rat_ln(TLine*& rat_ln) {
  rat_ln->SetLineColorAlpha(kRed+2, 0.7);
  rat_ln->SetLineStyle(2);
  rat_ln->SetLineWidth(4);
}



