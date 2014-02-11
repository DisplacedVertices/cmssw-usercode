#include <cmath>
#include <cassert>
#include <map>
#include <memory>
#include <vector>
#include <getopt.h>
#include "Math/QuantFuncMathCore.h"
#include "TCanvas.h"
#include "TError.h"
#include "TFile.h"
#include "TGraphAsymmErrors.h"
#include "TH1.h"
#include "THStack.h"
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
  double int_lumi; // in /fb
  std::string signal_name;
  double signal_xsec; // in fb
  bool bigw;
  double syst_frac;
  std::string file_path;
  std::string signal_file_suffix() const { return TString::Format("%ifb", int(signal_xsec)).Data(); }
  std::string signal_path() const { return file_path + "/" + signal_name + "_" + signal_file_suffix() + ".root"; }
  
  option_driver()
    : weightfiles(0),
      printall(0),
      moreprints(0),
      saveplots(0),
      plot_path("plots/SSB"),
      int_lumi(20.),
      signal_name("mfv_neutralino_tau0100um_M0400"),
      signal_xsec(20.),
      bigw(false),
      syst_frac(-1)
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

    int c;
    while (!help && (c = getopt(argc, argv, "hpmsz:l:n:x:bf:")) != -1) {
      switch (c) {
      case 'h':
        help = true;
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
        bigw = true;
	break;
      case 'f':
        if (!one_double('f', &syst_frac))
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
      fprintf(stderr, "  -p                      turn on (some) prints (default: off)\n");
      fprintf(stderr, "  -m                      turn on (all) prints (default: off)\n");
      fprintf(stderr, "  -s                      turn on saving of plots (default: off)\n");
      fprintf(stderr, "  -z plot_path            path to save plots to (implies -s, default: plots/SSB/signal_name/)\n");
      fprintf(stderr, "  -l int_lumi             integrated luminosity to scale to, in fb^-1 (default: 20)\n");
      fprintf(stderr, "  -n signal_name          signal name (default: mfv_neutralino_tau0100um_M0400)\n");
      fprintf(stderr, "  -x signal_xsec          signal cross section, in fb (default: 20)\n");
      fprintf(stderr, "  -b                      use big-weights samples (default: off)\n");
      fprintf(stderr, "  -f syst_frac            fraction systematic uncertainty to use in PL calculation (default: -1)\n");
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

void draw_in_order(std::vector<TH1F*> v) {
  auto f = [](TH1F* h, TH1F* h2) { return h->GetMaximum() > h2->GetMaximum(); };
  std::sort(v.begin(), v.end(), f);
  for (size_t i = 0; i < v.size(); ++i) {
    if (i == 0) {
      v[i]->SetMinimum(0.01);
      v[i]->Draw();
    } else {
      v[i]->Draw("same");
    }
  }
}



struct intvl {
  double lower;
  double upper;
  double hat;

  intvl() : lower(0), upper(1) {}
};

intvl clopper_pearson(double n_on, double n_tot, const double alpha=1-0.6827, const bool equal_tailed=true) {
  const double alpha_min = equal_tailed ? alpha/2 : alpha;
    
  intvl v;

  if (n_on > 0)
    v.lower = ROOT::Math::beta_quantile(alpha_min, n_on, n_tot - n_on + 1);
  if (n_tot - n_on > 0)
    v.upper = ROOT::Math::beta_quantile_c(alpha_min, n_on + 1, n_tot - n_on);
  
  if (n_on == 0 && n_tot == 0)
    v.hat = 0;
  else
    v.hat = n_on/n_tot;

  return v;
}

intvl clopper_pearson_poisson(double x, double y) {
  intvl vbi = clopper_pearson(x, x+y);
  intvl v;
  v.lower = vbi.lower/(1 - vbi.lower);
  if (y == 0 || fabs(vbi.upper - 1) < 1e-9) {
    v.hat = v.upper = -1;
    return v;
  }
  v.hat = vbi.hat/(1-vbi.hat);
  v.upper = vbi.upper/(1-vbi.upper);
  return v;
}

struct z_calculator {
  struct sample {
    std::string name;
    std::string filename;
    bool is_signal;
    double xsec; // in fb
    int color;
    std::unique_ptr<TFile> file;
    double nevents;
    double nm1;

    double partial_weight() const { assert(nevents > 0); return xsec / nevents; }
    double lumi() const { assert(xsec > 0); return nevents / xsec; };
    double weight() const { assert(nevents > 0); return xsec * options.int_lumi / nevents; }
    bool use() const { return is_signal || options.bigw || partial_weight() < 5e-2; }
    double tau() const { return lumi() / options.int_lumi; }

    std::map<std::string, TH1F*> hists;

    const TH1F* hist(const std::string& var) const {
      auto it = hists.find(var);
      assert(it != hists.end());
      return it->second;
    }

    static double ana_filter_eff(const std::string& name) {
      // JMTBAD keep in sync with Samples.py
      if (name == "mfv_neutralino_tau0000um_M0200") return 4.7518e-01;  //    47447 /    99850
      else if (name == "mfv_neutralino_tau0000um_M0400") return 9.6890e-01;  //    96890 /   100000
      else if (name == "mfv_neutralino_tau0000um_M0600") return 9.9495e-01;  //    99495 /   100000
      else if (name == "mfv_neutralino_tau0000um_M0800") return 9.9796e-01;  //    99696 /    99900
      else if (name == "mfv_neutralino_tau0000um_M1000") return 9.9866e-01;  //    99862 /    99996
      else if (name == "mfv_neutralino_tau0010um_M0200") return 4.7647e-01;  //    47647 /   100000
      else if (name == "mfv_neutralino_tau0010um_M0400") return 9.6750e-01;  //    96750 /   100000
      else if (name == "mfv_neutralino_tau0010um_M0600") return 9.9530e-01;  //    99231 /    99700
      else if (name == "mfv_neutralino_tau0010um_M0800") return 9.9795e-01;  //    99745 /    99950
      else if (name == "mfv_neutralino_tau0010um_M1000") return 9.9892e-01;  //    99791 /    99899
      else if (name == "mfv_neutralino_tau0100um_M0200") return 4.7951e-01;  //    47807 /    99700
      else if (name == "mfv_neutralino_tau0100um_M0400") return 9.6769e-01;  //    96043 /    99250
      else if (name == "mfv_neutralino_tau0100um_M0600") return 9.9554e-01;  //    99206 /    99650
      else if (name == "mfv_neutralino_tau0100um_M0800") return 9.9795e-01;  //    99795 /   100000
      else if (name == "mfv_neutralino_tau0100um_M1000") return 9.9890e-01;  //    99639 /    99749
      else if (name == "mfv_neutralino_tau1000um_M0200") return 4.7873e-01;  //    47754 /    99752
      else if (name == "mfv_neutralino_tau1000um_M0400") return 9.6798e-01;  //    96653 /    99850
      else if (name == "mfv_neutralino_tau1000um_M0600") return 9.9508e-01;  //    99360 /    99851
      else if (name == "mfv_neutralino_tau1000um_M0800") return 9.9825e-01;  //    99774 /    99949
      else if (name == "mfv_neutralino_tau1000um_M1000") return 9.9866e-01;  //    99866 /   100000
      else if (name == "mfv_neutralino_tau9900um_M0200") return 4.7714e-01;  //    47690 /    99950
      else if (name == "mfv_neutralino_tau9900um_M0400") return 9.6734e-01;  //    96734 /   100000
      else if (name == "mfv_neutralino_tau9900um_M0600") return 9.9511e-01;  //    99461 /    99950
      else if (name == "mfv_neutralino_tau9900um_M0800") return 9.9818e-01;  //    99718 /    99900
      else if (name == "mfv_neutralino_tau9900um_M1000") return 9.9904e-01;  //    99803 /    99899
      else if (name == "dyjetstollM10") return 4.3913e-04;  //     3132 /  7132223
      else if (name == "dyjetstollM50") return 2.8337e-03;  //    86313 / 30459503
      else if (name == "qcdht0100") return 7.4784e-04;  //    37489 / 50129518
      else if (name == "qcdht0250") return 6.0783e-02;  //  1644907 / 27062078
      else if (name == "qcdht0500") return 3.1108e-01;  //  9518716 / 30599292
      else if (name == "qcdht1000") return 4.4614e-01;  //  6176270 / 13843863
      else if (name == "singletop_s") return 7.3030e-02;  //    18985 /   259961
      else if (name == "singletop_s_tbar") return 6.7548e-02;  //     9455 /   139974
      else if (name == "singletop_t") return 5.4126e-02;  //   203416 /  3758227
      else if (name == "singletop_tW") return 1.8520e-01;  //    92167 /   497658
      else if (name == "singletop_tW_tbar") return 1.8475e-01;  //    91167 /   493460
      else if (name == "singletop_t_tbar") return 5.3102e-02;  //   102756 /  1935072
      else if (name == "ttbardilep") return 1.3153e-01;  //  1577210 / 11991069
      else if (name == "ttbarhadronic") return 4.7515e-01;  //  4823997 / 10152516
      else if (name == "ttbarsemilep") return 2.7453e-01;  //  6979960 / 25424818
      else if (name == "ttgjets") return 5.0128e-01;  //   862177 /  1719954
      else if (name == "ttwjets") return 6.0494e-01;  //   118596 /   196046
      else if (name == "ttzjets") return 6.3787e-01;  //   134054 /   210160
      else if (name == "wjetstolnu") return 6.6758e-04;  //    38526 / 57709905
      else if (name == "ww") return 2.2439e-02;  //   224401 / 10000431
      else if (name == "wz") return 2.8131e-02;  //   281321 / 10000283
      else if (name == "zz") return 2.9762e-02;  //   291664 /  9799908
      else return 0;
    }

    sample(const std::string& name_, const double xsec_, const int color_, const std::vector<std::string>& vars)
      : name(name_),
        filename(options.file_path + "/" + name_ + "_mangled.root"),
        is_signal(name == options.signal_name),
        xsec(xsec_),
        color(color_),
        file(TFile::Open(filename.c_str()))
    {
      assert(file->IsOpen());

      double filter_eff = ana_filter_eff(name);

      TH1F* hnevents = (TH1F*)file->Get("ntot");
      nevents = hnevents->GetBinContent(1) / filter_eff;

      TH1F* hnm1 = (TH1F*)file->Get("nm1");
      nm1 = hnm1->GetBinContent(1);

      for (const std::string& var : vars)
        hists[var] = (TH1F*)file->Get(var.c_str());
    }
  };

  static bool bannered;
  std::vector<sample> samples;
  std::map<std::string, const sample*> samples_by_name;
  double nsig_nm1;
  double nbkg_nm1;
  double nsig_tot;
  double nbkg_tot;

  z_calculator(const std::vector<std::string>& vars)
    : nsig_nm1(0),
      nbkg_nm1(0),
      nsig_tot(0),
      nbkg_tot(0)
  {
    samples.push_back(sample(options.signal_name, options.signal_xsec, kRed,       vars));
    samples.push_back(sample("ttbarhadronic",     225.2e3 * 0.457,     kBlue,      vars));
    samples.push_back(sample("ttbarsemilep",      225.2e3 * 0.438,     kBlue + 1,  vars));
    samples.push_back(sample("ttbardilep",        225.2e3 * 0.105,     kBlue + 2,  vars));
    samples.push_back(sample("qcdht0100",         1.04e10,             kGreen,     vars));
    samples.push_back(sample("qcdht0250",         2.76e8,              kGreen + 1, vars));
    samples.push_back(sample("qcdht0500",         8.43e6,              kGreen + 2, vars));
    samples.push_back(sample("qcdht1000",         2.04e5,              kGreen + 3, vars));

    for (std::vector<sample>::iterator s = samples.begin(); s != samples.end(); ) {
      if (!s->use())
        s = samples.erase(s);
      else
        ++s;
    }

    int n_sig_samples = 0;
    for (const sample& s : samples) {
      samples_by_name[s.name] = &s;

      if (s.is_signal) {
        ++n_sig_samples;
        nsig_nm1 = s.weight() * s.nm1;
        nsig_tot = s.weight() * s.nevents;
      }
      else {
        nbkg_nm1 += s.weight() * s.nm1;
        nbkg_tot += s.weight() * s.nevents;
      }
    }

    assert(n_sig_samples == 1);

    if (!bannered) {
      bannered = true;
      printf("nsig_nm1 = %f, nbkg_nm1 = %f\n", nsig_nm1, nbkg_nm1);
      printf("z_calculator setup:\nint lumi 'data': %f/fb\n", options.int_lumi);
      for (const sample& s : samples)
        if (!s.is_signal)
          printf("bkg: %20s   int lumi: %.3e/fb    tau: %.3e\n", s.name.c_str(), s.lumi(), s.tau());
    }
  }

  typedef std::pair<double, double> val_w_err;

  val_w_err raw_count(const sample& s, const std::string& var, const int ibin) const {
    const TH1F* h = s.hist(var);
    return std::make_pair(h->GetBinContent(ibin), h->GetBinError(ibin));
  }

  val_w_err weighted_count(const sample& s, const std::string& var, const int ibin) const {
    val_w_err r = raw_count(s, var, ibin);
    double w = s.weight();
    return std::make_pair(w * r.first, w * r.second);
  }

  val_w_err total_count(const std::string& var, const int ibin, const bool signal, const bool weighted) const {
    double totb = 0, totvarb = 0;
    for (const sample& s : samples) {
      if (s.is_signal == signal) {
        val_w_err b;
        if (weighted)
          b = weighted_count(s, var, ibin);
        else
          b = raw_count(s, var, ibin);

        totb += b.first;
        totvarb += b.second*b.second;
      }
    }

    return std::make_pair(totb, sqrt(totvarb));
  }

  THStack* total_hist(const std::string& var, const bool signal, const bool weighted) const {
    THStack* hs = new THStack(TString::Format("stack_%s", var.c_str()), TString::Format(";%s cut value;events passing", var.c_str()));

    for (const sample& s : samples) {
      if (s.is_signal == signal) {
        double w = s.weight();

        TH1F* h = (TH1F*)s.hist(var)->Clone(TString::Format("total_%s", var.c_str()));
        h->Sumw2();
        h->SetFillColor(s.color);
        h->SetLineColor(s.color);

        if (weighted) {
          for (int i = 0; i < h->GetNbinsX()+2; ++i) {
            h->SetBinContent(i, w * h->GetBinContent(i));
            h->SetBinError  (i, w * h->GetBinError  (i));
          }
        }

        hs->Add(h);
      }
    }

    return hs;
  }

  double get_zpl(const std::string& var, const int ibin) const {
    double s = total_count(var, ibin, true, true).first;
    double n = s;
    std::vector<double> ms, taus;
    if (options.moreprints) printf("   PL: b/m:");
    for (const sample& s : samples) {
      if (s.is_signal)
        continue;

      double m = raw_count(s, var, ibin).first;
      double tau = s.tau();
      n += m/tau;

      ms.push_back(m);
      taus.push_back(tau);

      if (options.moreprints)
        printf("    %s %i/%i\n", s.name.c_str(), int(m), int(s.nevents));
    }

    if (options.moreprints) printf("   s: %f  n: %f\n", s, n);
    return getSignificance(0, n, s, ms, taus, options.syst_frac);
  }

  void max_z(const std::string& var) const {
    THStack* sigHist = total_hist(var, true, true);
    THStack* bkgHist = total_hist(var, false, true);
    TAxis* xax = ((TH1F*)sigHist->GetHists()->First())->GetXaxis();

    if (options.printall)
      printf("%16s%6s%9s%9s%9s%9s%9s%9s%9s%9s %9s %9s %9s %9s\n", var.c_str(), "cut", "s", "b", "sigb", "ssb", "ssb20", "ssbsb", "ssbsb20", "zpl", "sig frac", "sig eff", "bkg frac", "bkg eff");

    const int nbins = xax->GetNbins();
    const double xlow = xax->GetXmin();
    const double xup = xax->GetXmax();
    TH1F* h_sigfrac = new TH1F("h_sigfrac", ";cut;sig frac", nbins, xlow, xup);
    TH1F* h_bkgfrac = new TH1F("h_bkgfrac", ";cut;bkg frac", nbins, xlow, xup);
    double bkgpl_x[nbins], bkgpl_y[nbins], bkgpl_exl[nbins], bkgpl_exh[nbins], bkgpl_eyl[nbins], bkgpl_eyh[nbins];
    TH1F* h_zssb = new TH1F("h_zssb", ";cut;ssb", nbins, xlow, xup);
    TH1F* h_zssb20 = new TH1F("h_zssb20", ";cut;ssb20", nbins, xlow, xup);
    TH1F* h_zssbsb = new TH1F("h_zssbsb", ";cut;ssbsb", nbins, xlow, xup);
    TH1F* h_zssbsb20 = new TH1F("h_zssbsb20", ";cut;ssbsb20", nbins, xlow, xup);
    TH1F* h_zpl = new TH1F("h_zpl", ";cut;asimov Z", nbins, xlow, xup);

    double cut = 0;
    double smax = 0;
    double bmax = 0;
    double zmax = 0;

    for (int i = 1; i <= nbins; i++) {
      const double s = total_count(var, i, true, true).first;
      const val_w_err bve = total_count(var, i, false, true);
      const double b = bve.first;
      const double sigb = bve.second;

      const double zssb = s/sqrt(b);
      const double zssb20 = s/sqrt(b + 0.04*b*b);
      const double zssbsb = s/sqrt(b + sigb*sigb);
      const double zssbsb20 = s/sqrt(b + sigb*sigb + 0.04*b*b);
      const double zpl = get_zpl(var, i);

      const double z = zssb20;

      bkgpl_x[i-1] = xax->GetBinCenter(i);
      bkgpl_exl[i-1] = bkgpl_exh[i-1] = xax->GetBinWidth(i)/2;
      //intvl bkgpl_v = slik_syst20->bkgfrac(var, i);
      bkgpl_y[i-1] = 0; //bkgpl_v.hat;
      bkgpl_eyl[i-1] = 0; //bkgpl_v.hat - bkgpl_v.lower;
      bkgpl_eyh[i-1] = 0; //bkgpl_v.upper - bkgpl_v.hat;

      if (options.printall)
        printf("%16s%6.2f%9.2f%9.2f%9.2f%9.2f%9.2f%9.2f%9.2f%9.2f %9.2e %9.2e %9.2e %9.2e\n", "", xax->GetBinLowEdge(i), s, b, sigb, zssb, zssb20, zssbsb, zssbsb20, zpl, s/nsig_nm1, s/nsig_tot, b/nbkg_nm1, b/nbkg_tot);

      h_sigfrac->SetBinContent(i, s/nsig_nm1);
      h_bkgfrac->SetBinContent(i, b/nbkg_nm1);

      if (b > 0) {
        h_zssb->SetBinContent(i, zssb);
        h_zssb20->SetBinContent(i, zssb20);
      }
      if (b + sigb*sigb > 0) {
        h_zssbsb->SetBinContent(i, zssbsb);
        h_zssbsb20->SetBinContent(i, zssbsb20);
      }
      if (!TMath::IsNaN(zpl))
        h_zpl->SetBinContent(i, zpl);

      if (z > zmax && s >= 5) {
        cut = xax->GetBinLowEdge(i);
        smax = s;
        bmax = b;
        zmax = z;
      }
    }

    if (options.printall)
      printf("\n%16s\t%6.2f\t%9.2f\t%9.2f\t%6.2f\t\t\t%f\t%f\t%f\t%e\n\n\n", "max ssb", cut, smax, bmax, zmax, smax/nsig_nm1, smax/nsig_tot, bmax/nbkg_nm1, bmax/nbkg_tot);
    else
      printf("%16s\t%6.2f\t%9.2f\t%9.2f\t%6.2f\t%f\t%f\t%f\t%e\n", var.c_str(),  cut, smax, bmax, zmax, smax/nsig_nm1, smax/nsig_tot, bmax/nbkg_nm1, bmax/nbkg_tot);

    std::vector<TH1F*> zs = {h_zssb, h_zssb20, h_zssbsb, h_zssbsb20, h_zpl};
    for (TH1F* h : zs)
      h->SetLineWidth(2);
    h_zssb20->SetLineColor(kCyan);
    h_zssbsb->SetLineColor(kRed);
    h_zssbsb20->SetLineColor(6);
    h_zpl->SetLineColor(kOrange+2);
    h_sigfrac->SetLineColor(kRed);
    h_bkgfrac->SetLineColor(kBlue);

    TGraphAsymmErrors* g_bkgpl = new TGraphAsymmErrors(nbins, bkgpl_x, bkgpl_y, bkgpl_exl, bkgpl_exh, bkgpl_eyl, bkgpl_eyh);
    g_bkgpl->SetLineColor(kCyan);
    g_bkgpl->SetMarkerColor(kCyan);
    g_bkgpl->SetMarkerStyle(20);
    g_bkgpl->SetMarkerSize(1);

    TLegend* leg = new TLegend(0.8,0.8,1,1);
    leg->AddEntry(h_zssb, "s/#sqrt{b}", "L");
    leg->AddEntry(h_zssb20, "s/#sqrt{b+(0.2b)^{2}}", "L");
    leg->AddEntry(h_zssbsb, "s/#sqrt{b+#sigma_{b}^{2}}", "L");
    leg->AddEntry(h_zssbsb20, "s/#sqrt{b+#sigma_{b}^{2}+(0.2b)^{2}}", "L");
    leg->AddEntry(h_zpl, TString::Format("Z_{PL} w/ %i syst", int(options.syst_frac * 100)), "L");

    if (options.saveplots) {
      for (int logy = 0; logy < 2; ++logy) {
        TCanvas* c1 = new TCanvas("c1", "", 1110, 1020);
        c1->Divide(2,2);
        c1->cd(1)->SetLogy(logy);
        sigHist->Draw();
        c1->cd(3)->SetLogy(logy);
        bkgHist->Draw();
        c1->cd(2)->SetLogy(logy);
        draw_in_order(zs);
        leg->Draw();
        c1->cd(4)->SetLogy(logy);
        draw_in_order(std::vector<TH1F*>({h_sigfrac, h_bkgfrac}));
        g_bkgpl->Draw("ZP");
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
    delete h_zssb20;
    delete h_zssbsb;
    delete h_zssbsb20;
    delete h_zpl;
    delete h_sigfrac;
    delete h_bkgfrac;
    delete leg;
    delete sigHist;
    delete bkgHist;
  }
};

bool z_calculator::bannered = false;

int main(int argc, char** argv) {
  int r;
  if ((r = options.parse_args(argc, argv)))
    return r;

  gErrorIgnoreLevel = 1001;
  gStyle->SetPadTickX(1);
  gStyle->SetPadTickY(1);

  std::vector<std::string> vars = {"ntracks", "ntracksptgt3", "ntracksptgt5", "ntracksptgt10", "njetsntks", "tkonlypt", "abstkonlyeta", "tkonlymass", "jetsntkpt", "absjetsntketa", "jetsntkmass", "tksjetsntkpt", "abstksjetsntketa", "tksjetsntkmass", "costhtkonlymombs", "costhjetsntkmombs", "costhtksjetsntkmombs", "missdisttksjetsntkpvsig", "sumpt2", "maxtrackpt", "maxm1trackpt", "trackdxyerrmin", "trackdzerrmin", "drmin", "drmax", "jetpairdrmin", "jetpairdrmax", "bs2ddist", "bs2derr", "bs2dsig", "sumht", "nsemilepmuons", "nleptons", "nsemileptons", "ntracks01", "maxtrackpt01", "njetsntks01", "tkonlymass01", "jetsntkmass01", "tksjetsntkmass01", "absdeltaphi01"};

  z_calculator z_calc(vars);

  if (!options.printall) printf("variable\t\tcut\t\ts\t\tb\tmax ssb\tsig frac\tsig eff\t\tbkg frac\tbkg eff\n");

  for (const std::string& var : vars)
    z_calc.max_z(var);
}
