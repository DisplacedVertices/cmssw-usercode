void sum_signal_hists(TH1F*& h_sig, vector<vector<TFile*>>& fs_sig, const vector<float>& sigxsecs, const float sigBR, const string& yr, const string& hloc) {
  
  const map<string,float> lumis = { // in pb^{-1}
    {"20161", 19502}, // This is NOT correct for bjet (differs by a few %), change if non-rescaled signal is ever needed
    {"20162", 16812},
    {"2017", 42068},
    {"2018", 59561},
  };
  
  const map<string, vector<string>> year_divs = {
    {"2016", {"20161", "20162"}},
    {"2017", {"2017"}},
    {"2018", {"2018"}},
    {"run2", {"20161", "20162", "2017", "2018"}},
  };
  const vector<string> yrs = year_divs.at(yr);


  for (int i=0; i<sigxsecs.size(); i++) {
    for (int j=0; j<yrs.size(); j++) {
      TFile* fsig = fs_sig[i][j];
      TH1F* h_subsig = (TH1F*)fsig->Get(hloc.c_str())->Clone();


      // Get sumw
      TH1* h_sumw = (TH1F*)fsig->Get("mfvWeight/h_sums")->Clone();
      Int_t binNum = h_sumw->GetXaxis()->FindBin("sum_gen_weight_total");
      Double_t sumw = h_sumw->GetBinContent(binNum);
      //cout << "Sumw:" << sumw << " ";
      
      h_subsig->Scale(lumis.at(yrs[j]) * sigxsecs[i] / sumw);
      //cout << "Scale factor:" << lumis.at(yrs[j]) * sigxsecs[i] / sumw << endl;

      if (i==0 && j==0) {
        h_sig = (TH1F*)h_subsig->Clone();
        h_sig->SetDirectory(0); // Apparently this prevents a memory storage crash, idk why
      } else {
        h_sig->Add(h_subsig);
      }
      delete h_subsig;
      delete h_sumw;
    }
  }

  h_sig->Scale(sigBR);

}


