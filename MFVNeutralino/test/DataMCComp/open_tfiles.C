
void open_mc_dat_tfiles(TFile*& f_dat, vector<TFile*>& tfiles, const string& yr, const string& dat_prefix, const string& dat_suffix, const string& mc_prefix, const string& mc_suffix, const vector<string>& samplenames, const bool debug) {
  /*
  Inputs:
  f_dat: data TFile
  tfiles: vector of MC TFiles
  */

  // const bool debug = true;

  int nbkg = samplenames.size();
  tfiles.resize(nbkg);


  // Make names
  vector<string> fn_mc(nbkg);
  const string fn_dat = dat_prefix + yr + dat_suffix;
  cout << fn_dat << endl;
  for (int i=0; i<nbkg; i++) {
    fn_mc[i] = mc_prefix + samplenames[i] + "_" + yr + mc_suffix;
  }
  
  // Data
  f_dat = TFile::Open(fn_dat.c_str(), "READ");
  if (debug) {cout << fn_dat << endl;};

  // MC
  for (int i=0; i<nbkg; i++) {
    tfiles[i] = TFile::Open(fn_mc[i].c_str(), "READ");
    if (debug) {cout << fn_mc[i] << endl;};
  }


}






void open_sig_tfiles(vector<vector<vector<TFile*>>>& fs_sig, const string& yr, const string& sig_prefix, const string& sig_suffix, const vector<vector<string>>& signames, const bool debug) {

  const map<string, vector<string>> year_divs = {
    {"2016", {"20161", "20162"}},
    {"2017", {"2017"}},
    {"2018", {"2018"}},
    {"run2", {"20161", "20162", "2017", "2018"}},
  };
  const vector<string> yrs = year_divs.at(yr);
  int nsig = signames.size();


  fs_sig.resize(nsig);

  for (int i=0; i<nsig; i++) {
    fs_sig[i].resize(signames[i].size());
    for (int j=0; j<signames[i].size(); j++) {
      fs_sig[i][j].resize(yrs.size());
      for (int k=0; k<yrs.size(); k++) {
        string fn_sig = sig_prefix + signames[i][j] + yrs[k] + sig_suffix;
        if (debug) {cout << fn_sig << endl;};
        fs_sig[i][j][k] = TFile::Open(fn_sig.c_str(), "READ");
      }
    }
  }

}



void get_sig_norms() {
  /*
  Returns (xsec*lumi/sumw)
  Currently NOT called
  */

  const vector<vector<float>> sigxsecs = {{ // in pb
    3*(9.426e-02), // WplusH
    3*(5.983e-02), // WminusH
    3*(2.568e-02), // ZH
    3*(4.14e-03), // ggZH
  }};

  const map<string,float> lumis = { // in pb^{-1}
    {"20161", 19502},
    {"20162", 16812},
    {"2017", 42068},
    {"2018", 59561},
  };

}







