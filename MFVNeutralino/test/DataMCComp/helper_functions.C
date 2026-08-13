
void move_over_under_flows(TH1* h) {
  const int nb = h->GetNbinsX();

  const double b0_err = h->GetBinError(0);
  const double b1_err = h->GetBinError(1);
  h->SetBinContent(1, h->GetBinContent(1) + h->GetBinContent(0));
  h->SetBinError(1, sqrt(b1_err*b1_err + b0_err*b0_err));

  const double bN1_err = h->GetBinError(nb+1);
  const double bN_err = h->GetBinError(nb);
  h->SetBinContent(nb, h->GetBinContent(nb) + h->GetBinContent(nb+1));
  h->SetBinError(nb, sqrt(bN_err*bN_err + bN1_err*bN1_err));

  h->SetBinContent(0, 0);
  h->SetBinError(0, 0);
  h->SetBinContent(nb+1, 0);
  h->SetBinError(nb+1, 0);
}




