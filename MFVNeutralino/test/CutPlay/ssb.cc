#include <cmath>
#include <cassert>
#include <map>
#include <vector>
#include <getopt.h>
#include "TCanvas.h"
#include "TError.h"
#include "TFile.h"
#include "TH1.h"
#include "TLegend.h"
#include "TMath.h"
#include "TStyle.h"
#include "SigCalc.h"

struct option_driver {
  bool weightfiles;
  bool printall;
  bool moreprints;
  bool saveplots;
  std::string plot_path;
  double int_lumi;
  std::string signal_name;
  double signal_xsec;
  double nsig_total() { return int_lumi * signal_xsec; }
  double nbkg_total;
  std::string file_path;
  std::string signal_file_suffix() { return TString::Format("%ipb", int(signal_xsec)).Data(); }
  std::string background_file_name;
  std::string signal_path() { return file_path + "/" + signal_name + "_" + signal_file_suffix() + ".root"; }
  std::string background_path() { return file_path + "/background.root"; }
  
  option_driver()
    : weightfiles(0),
      printall(0),
      moreprints(0),
      saveplots(0),
      plot_path("plots/SSB"),
      signal_name("mfv_neutralino_tau0100um_M0400"),
      int_lumi(20000.),
      signal_xsec(1.),
      nbkg_total(211435861768.63),
      background_file_name("background.root")
  {}

  bool one_double(char sw, double* d) {
    int n = sscanf(optarg, "%lf", d);
    if (n != 1) {
      fprintf(stderr, "error: -%c argument takes a double value\n", sw);
      return false;
    }
    return true;
  }

  bool one_string(char sw, std::string* s) {
    if (optarg && optarg[0] == '\0') {
      fprintf(stderr, "error: -%c argument takes a string\n", sw);
      return false;
    }
    *s = optarg;
    return true;
  }
    
  int parse_args(int argc, char** argv) {
    bool help = false;

    int c, n;
    while (!help && (c = getopt(argc, argv, "hwpmsz:l:n:x:b:u:k:")) != -1) {
      switch (c) {
      case 'h':
        help = true;
        break;
      case 'w':
        weightfiles = true;
        break;
      case 'p':
        printall = true;
        break;
      case 'm':
        moreprints = true;
        break;
      case 's':
        saveplots = true;
        break;
      case 'z':
        saveplots = true;
        if (!one_string('z', &plot_path))
          return 1;
        break;
      case 'l':
        if (!one_double('l', &int_lumi))
	  return 1;
	break;
      case 'n':
        if (!one_string('n', &signal_name))
          return 1;
        break;
      case 'x':
        if (!one_double('x', &signal_xsec))
          return 1;
	break;
      case 'b':
        if (!one_double('b', &nbkg_total))
          return 1;
	break;
      case 'k':
        if (!one_string('k', &background_file_name))
          return 1;
        break;
        
      case '?':
        if (strchr("", optopt))
          fprintf(stderr, "error: option -%c requires an argument\n", optopt);
        else if (isprint(optopt))
          fprintf(stderr, "error: unknown option -%c\n", optopt);
        else
          fprintf(stderr, "error: unknown option character `\\x%x'\n", optopt);
        return 1;
      }
    }

    int nargs = argc - optind;

    if (help || nargs < 1) {
      fprintf(stderr, "usage: %s path [switch options]\n", argv[0]);
      fprintf(stderr, "  path             path containing input root files\n");
      fprintf(stderr, "available switch options:\n");
      fprintf(stderr, "  -h                      produce this help message and quit\n");
      fprintf(stderr, "  -w                      produce weighted files and quit\n");
      fprintf(stderr, "  -p                      turn on (some) prints (default: off)\n");
      fprintf(stderr, "  -m                      turn on (all) prints (default: off)\n");
      fprintf(stderr, "  -s                      turn on saving of plots (default: off\n");
      fprintf(stderr, "  -z plot_path            path to save plots to (implies -s, default: plots/SSB/signal_name/)\n");
      fprintf(stderr, "  -l int_lumi             integrated luminosity to scale to, in pb^-1 (default: 20000)\n");
      fprintf(stderr, "  -n signal_name          signal name (default: mfv_neutralino_tau0100um_M0400)\n");
      fprintf(stderr, "  -x signal_xsec          signal cross section, in pb (default: 1)\n");
      fprintf(stderr, "  -b nbkg_total           number to scale background efficiency by (default: something big)\n");
      fprintf(stderr, "  -k bkg_file_name        filename for weighted, added backgrounds (default: background.root)\n");
      return 1;
    }

    file_path = argv[optind];
    if (strcmp(argv[optind], "") == 0) {
      fprintf(stderr, "error: path must be supplied\n");
      return 1;
    }

    return 0;
  }
};

option_driver options;

void draw_in_order(std::vector<TH1F*> v, const char* cmd="") {
  auto f = [](TH1F* h, TH1F* h2) { return h->GetMaximum() > h2->GetMaximum(); };
  std::sort(v.begin(), v.end(), f);
  std::string ex = cmd;
  for (int i = 0; i < v.size(); ++i) {
    if (i == 0) {
      v[i]->SetMinimum(0.01);
      v[i]->Draw(cmd);
    } else {
      //v[i]->Draw(TString::Format("%s same", cmd));
      v[i]->Draw("same");
    }
  }
}

struct sample {
  std::string name;
  double xsec; // in pb
  double nevents;

  double partial_weight() const { return xsec / nevents; }
  double weight() const { return xsec * options.int_lumi / nevents; }
};

const int nsamples = 8;
sample samples[nsamples] = {
  {options.signal_name, options.signal_xsec,    100000 },
  {"ttbarhadronic",     225.2 * 0.457,         5268722 },
  {"ttbarsemilep",      225.2 * 0.438,        12674909 },
  {"ttbardilep",        225.2 * 0.105,         6059506 },
  {"qcdht0100",         1.04e7,               25064759 },           
  {"qcdht0250",         2.76e5,               13531039 },           
  {"qcdht0500",         8.43e3,               15274646 },           
  {"qcdht1000",         2.04e2,                6034431 }
};

bool weight_files() {
  std::string cmd = "mergeTFileServiceHistograms -w ";
  cmd += TString::Format("%e", samples[0].weight()).Data();
  cmd += " -i " + options.file_path + "/" + samples[0].name + "_mangled.root -o " + options.file_path + "/" + samples[0].name + "_" + options.signal_file_suffix() + ".root";
  printf("%s\n", cmd.c_str());
  if (system(cmd.c_str()))
    return false;

  cmd = "mergeTFileServiceHistograms -w ";
  
  for (int i = 1; i < nsamples; ++i)
    cmd += TString::Format("%e%s", samples[i].weight(), (i < nsamples-1 ? "," : ""));
  cmd += " -i ";
  for (int i = 1; i < nsamples; ++i)
    cmd += options.file_path + "/" + samples[i].name + "_mangled.root ";
  cmd += " -o " + options.file_path + "/" + options.background_file_name;
  printf("%s\n", cmd.c_str());
  if (system(cmd.c_str()))
    return false;

  return true;
}

struct sigproflik {
  static bool bannered;
  std::vector<std::string> filenames;
  std::vector<TFile*> files;
  std::vector<double> taus;
  std::vector<std::map<std::string, TH1F*> > hists;
  double syst_frac;

  sigproflik(const char** vars, const int nvars, const bool bigw, const double syst) {
    syst_frac = syst;

    std::vector<double> lumis;
  
    for (const sample& s : samples) {
      if (s.name != options.signal_name && !bigw && s.partial_weight() > 1e-3)
        continue;
      filenames.push_back(options.file_path + "/" + s.name + "_mangled.root");
      lumis.push_back(1e-3/s.partial_weight()); // 1e-3 is go to fb^-1 from the xsecs in pb
    }

    for (int i = 1; i < filenames.size(); ++i)
      taus.push_back(lumis[i] / lumis[0]);
        
    hists.resize(filenames.size());

    for (int i = 0; i < filenames.size(); ++i) {
      files.push_back(new TFile(filenames[i].c_str()));
      for (int j = 0; j < nvars; ++j)
        hists[i][vars[j]] = (TH1F*)files.back()->Get(vars[j]);
    }

    if (!bannered) {
      bannered = true;
      printf("sigproflik setup:\nint lumi 'data': %f/fb\n", lumis[0]);
      for (int i = 1; i < filenames.size(); ++i)
        printf("bkg: %s   int lumi: %f/fb    tau: %f\n", filenames[i].c_str(), lumis[i], taus[i-1]);
    }
  }

  double sig(const char* var, const int ibin) {
    double s = hists[0][var]->GetBinContent(ibin);
    double n = s;
    std::vector<double> ms;
    if (options.moreprints) printf("   proflik: b/m:");
    for (int i = 1; i < filenames.size(); ++i) {
      double m = hists[i][var]->GetBinContent(ibin);
      if (options.moreprints)
        printf("    %s %i/%i\n", filenames[i].c_str(), int(m), samples[i].nevents);
      n += m/taus[i-1];
      ms.push_back(m);
    }
    if (options.moreprints) printf("   s: %f  n: %f\n", s, n);
    return getSignificance(0, n, s, ms, taus, syst_frac);
  }
};

bool sigproflik::bannered = false;
sigproflik* slik = 0;
sigproflik* slik_nobigw = 0;
sigproflik* slik_syst20 = 0;

void maxSSB(TH1F* sigHist, double nsig_nm1, TH1F* bkgHist, double nbkg_nm1, const char* var) {
  if (options.printall)
    printf("%16s%6s%9s%9s%9s%9s%9s%9s%9s%9s%9s %9s %9s %9s %9s\n", sigHist->GetName(), "cut", "s", "b", "sigb", "ssb", "ssbsb", "ssbsb20", "zplnobigw", "zpl", "zplsyst20", "sig frac", "sig eff", "bkg frac", "bkg eff");
  const int nbins = sigHist->GetNbinsX();
  const double xlow = sigHist->GetXaxis()->GetXmin();
  const double xup = sigHist->GetXaxis()->GetXmax();
  TH1F* h_sigfrac = new TH1F("h_sigfrac", ";cut;sig frac", nbins, xlow, xup);
  TH1F* h_bkgfrac = new TH1F("h_bkgfrac", ";cut;bkg frac", nbins, xlow, xup);
  TH1F* h_zssb = new TH1F("h_zssb", ";cut;ssb", nbins, xlow, xup);
  TH1F* h_zssbsb = new TH1F("h_zssbsb", ";cut;ssbsb", nbins, xlow, xup);
  TH1F* h_zssbsb20 = new TH1F("h_zssbsb20", ";cut;ssbsb20", nbins, xlow, xup);
  TH1F* h_zpl_nobigw = new TH1F("h_zpl_nobigw", ";cut;asimov Z", nbins, xlow, xup);
  TH1F* h_zpl = new TH1F("h_zpl", ";cut;asimov Z", nbins, xlow, xup);
  TH1F* h_zpl_syst20 = new TH1F("h_zpl_syst20", ";cut;asimov Z", nbins, xlow, xup);

  double cut = 0;
  double smax = 0;
  double bmax = 0;
  double zmax = 0;

  for (int i = 1; i <= nbins; i++) {
    const double s = sigHist->GetBinContent(i);
    const double b = bkgHist->GetBinContent(i);
    const double sigb = bkgHist->GetBinError(i);

    const double zssb = s/sqrt(b);
    const double zssbsb = s/sqrt(b + sigb*sigb);
    const double zssbsb20 = s/sqrt(b + sigb*sigb + 0.04*b*b);
    const double zpl_nobigw = -1; //slik_nobigw->sig(var, i);
    const double zpl = slik->sig(var, i);
    const double zpl_syst20 = -1; //slik_syst20->sig(var, i);

    if (options.printall)
      printf("%16s%6.2f%9.2f%9.2f%9.2f%9.2f%9.2f%9.2f%9.2f%9.2f%9.2f %9.2e %9.2e %9.2e %9.2e\n", "", sigHist->GetBinLowEdge(i), s, b, sigb, zssb, zssbsb, zssbsb20, zpl_nobigw, zpl, zpl_syst20, s/nsig_nm1, s/options.nsig_total(), b/nbkg_nm1, b/options.nbkg_total);

    h_sigfrac->SetBinContent(i, s/nsig_nm1);
    h_bkgfrac->SetBinContent(i, b/nbkg_nm1);

    if (b != 0)
      h_zssb->SetBinContent(i, zssb);
    if (b + sigb*sigb > 0)
      h_zssbsb->SetBinContent(i, zssbsb);
    if (b > 0)
      h_zssbsb20->SetBinContent(i, zssbsb20);
    if (!TMath::IsNaN(zpl_nobigw))
      h_zpl_nobigw->SetBinContent(i, zpl_nobigw);
    if (!TMath::IsNaN(zpl))
      h_zpl->SetBinContent(i, zpl);
    if (!TMath::IsNaN(zpl_syst20))
      h_zpl_syst20->SetBinContent(i, zpl_syst20);

    if (zpl > zmax) {
      cut = sigHist->GetBinLowEdge(i);
      smax = s;
      bmax = b;
      zmax = zpl;
    }
  }

  if (options.printall)
    printf("\n%16s\t%6.2f\t%9.2f\t%9.2f\t%6.2f\t\t\t%f\t%f\t%f\t%e\n\n\n", "max ssb", cut, smax, bmax, zmax, smax/nsig_nm1, smax/options.nsig_total(), bmax/nbkg_nm1, bmax/options.nbkg_total);
  else
    printf("%16s\t%6.2f\t%9.2f\t%9.2f\t%6.2f\t%f\t%f\t%f\t%e\n", sigHist->GetName(),  cut, smax, bmax, zmax, smax/nsig_nm1, smax/options.nsig_total(), bmax/nbkg_nm1, bmax/options.nbkg_total);

  std::vector<TH1F*> zs = {h_zssb, h_zssbsb, h_zssbsb20, h_zpl_nobigw, h_zpl, h_zpl_syst20};
  for (TH1F* h : zs)
    h->SetLineWidth(2);
  h_zssbsb->SetLineColor(kRed);
  h_zssbsb20->SetLineColor(6);
  h_zpl_nobigw->SetLineColor(kBlue);
  h_zpl->SetLineColor(kOrange+2);
  h_zpl_syst20->SetLineColor(kGreen+2);
  h_sigfrac->SetLineColor(kRed);
  h_bkgfrac->SetLineColor(kBlue);

  TLegend* leg = new TLegend(0.8,0.8,1,1);
  leg->AddEntry(h_zssb, "s/#sqrt{b}", "L");
  leg->AddEntry(h_zssbsb, "s/#sqrt{b+#sigma_{b}^{2}}", "L");
  leg->AddEntry(h_zssbsb20, "s/#sqrt{b+#sigma_{b}^{2}+(0.2b)^{2}}", "L");
  leg->AddEntry(h_zpl_nobigw, "Z_{PL} (no big weights)", "L");
  leg->AddEntry(h_zpl, "Z_{PL}", "L");
  leg->AddEntry(h_zpl_syst20, "Z_{PL} inc. 20% syst. unc.", "L");

  if (options.saveplots) {
    for (int logy = 0; logy < 2; ++logy) {
      TCanvas* c1 = new TCanvas("c1", "", 1200, 675);
      c1->Divide(2,2);
      c1->cd(1)->SetLogy(logy);
      sigHist->SetLineColor(kRed);
      sigHist->Draw();
      c1->cd(3)->SetLogy(logy);
      bkgHist->Draw();
      c1->cd(2)->SetLogy(logy);
      draw_in_order(zs);
      leg->Draw();
      c1->cd(4)->SetLogy(logy);
      draw_in_order(std::vector<TH1F*>({h_sigfrac, h_bkgfrac}));
      std::string p = options.plot_path + "/" + options.signal_name + "/";
      p += var;
      if (logy)
        p += "_log";
      c1->SaveAs((p + ".pdf").c_str());
      c1->SaveAs((p + ".png").c_str());
      if (!logy) c1->SaveAs((p + ".root").c_str());
      delete c1;
    }
  }

  delete h_zssb;
  delete h_zssbsb;
  delete h_zssbsb20;
  delete h_zpl;
  delete h_zpl_nobigw;
  delete h_zpl_syst20;
  delete h_sigfrac;
  delete h_bkgfrac;
  delete leg;
}


int main(int argc, char** argv) {
  int r;
  if ((r = options.parse_args(argc, argv)))
    return r;

  if (options.weightfiles) {
    weight_files();
    return 0;
  }

  gErrorIgnoreLevel = 1001;
  gStyle->SetPadTickX(1);
  gStyle->SetPadTickY(1);

  const int nvars = 17;
  const char* hnames[nvars] = {"ntracks", "njetssharetks", "maxtrackpt", "drmin", "drmax", "bs2dsig", "ntracks01", "njetssharetks01", "maxtrackpt01", "costhmombs", "mass", "jetsmassntks", "mass01", "jetsmassntks01", "pt", "ntracksptgt3", "sumpt2"};

  slik = new sigproflik(hnames, nvars, true, -1);
  slik_nobigw = new sigproflik(hnames, nvars, false, -1);
  slik_syst20 = new sigproflik(hnames, nvars, true, 0.2);

  TFile* sigFile = TFile::Open(options.signal_path().c_str());
  TFile* bkgFile = TFile::Open(options.background_path().c_str());

  double nsig_nm1 = ((TH1F*)sigFile->Get("nm1"))->GetBinContent(1);
  double nbkg_nm1 = ((TH1F*)bkgFile->Get("nm1"))->GetBinContent(1);
  printf("nsig_nm1 = %f, nbkg_nm1 = %f\n", nsig_nm1, nbkg_nm1);

  if (!options.printall) printf("variable\t\tcut\t\ts\t\tb\tmax ssb\tsig frac\tsig eff\t\tbkg frac\tbkg eff\n");

  for (int i = 0; i < nvars; i++) {
    TH1F* sigHist = (TH1F*)sigFile->Get(hnames[i]);
    TH1F* bkgHist = (TH1F*)bkgFile->Get(hnames[i]);
    maxSSB(sigHist, nsig_nm1, bkgHist, nbkg_nm1, hnames[i]);
  }

  delete slik;
  delete slik_nobigw;
  delete slik_syst20;
}
