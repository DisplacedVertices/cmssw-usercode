// g++ `root-config --cflags --libs --glibs` -std=c++0x -I/uscms/home/tucker/public/SigCalc -lMinuit ~tucker/public/SigCalc/SigCalc.cc ~tucker/public/SigCalc/fitPar.cc ~tucker/public/SigCalc/getSignificance.cc ssb.C && ./a.out

#include <cmath>
#include <assert.h>
#include <map>
#include <vector>
#include "TMath.h"
#include "TH1.h"
#include "TCanvas.h"
#include "TFile.h"
#include "TLegend.h"
#include "getSignificance.h"

const int niter = 1;
bool printall = 0;
bool plot = 0;

double nsig_total = 19788.362;
double nsig = 1023.41;

double nbkg_total = 211435861768.63;
double nbkg = 174811.73;

void draw_in_order(std::vector<TH1F*> v, const char* cmd="") {
  auto f = [](TH1F* h, TH1F* h2) { return h->GetMaximum() > h2->GetMaximum(); };
  std::sort(v.begin(), v.end(), f);
  std::string ex = cmd;
  for (int i = 0; i < v.size(); ++i) {
    if (i == 0)
      v[i]->Draw(cmd);
    else
      v[i]->Draw(cmd + TString(" same"));
  }
}

void draw_in_order(TH1F* a, TH1F* b, const char* cmd="") {
  std::vector<TH1F*> v = {a,b};
  draw_in_order(v, cmd);
}

void draw_in_order(TH1F* a, TH1F* b, TH1F* c, const char* cmd="") {
  std::vector<TH1F*> v = {a,b,c};
  draw_in_order(v, cmd);
}


struct sigproflik {
  std::vector<std::string> filenames;
  std::vector<double> lumis;
  std::vector<double> taus;
  std::vector<TFile*> files;
  int nfiles;
  std::vector<std::map<std::string, TH1F*> > hists;

  sigproflik(const char** vars, const int nvars, const std::string dir) {
    filenames.push_back(dir + "mfv_neutralino_tau0100um_M0400_mangled.root");
    filenames.push_back(dir + "ttbarhadronic_mangled.root");
    filenames.push_back(dir + "ttbarsemilep_mangled.root");
    filenames.push_back(dir + "ttbardilep_mangled.root");
    //filenames.push_back(dir + "qcdht0100_mangled.root");
    //filenames.push_back(dir + "qcdht0250_mangled.root");
    filenames.push_back(dir + "qcdht0500_mangled.root");
    filenames.push_back(dir + "qcdht1000_mangled.root");

    lumis.push_back(nsig_total/1000/0.199379);
    lumis.push_back(nsig_total/1000/0.386535);
    lumis.push_back(nsig_total/1000/0.153995);
    lumis.push_back(nsig_total/1000/0.077220);
    //lumis.push_back(nsig_total/1000/8210.69);
    //lumis.push_back(nsig_total/1000/403.634);
    lumis.push_back(nsig_total/1000/10.9211);
    lumis.push_back(nsig_total/1000/0.668965);

    nfiles = int(filenames.size());
    assert(nfiles == lumis.size());
    hists.resize(nfiles);

    for (int i = 0; i < nfiles; ++i) {
      files.push_back(new TFile(filenames[i].c_str()));
      for (int j = 0; j < nvars; ++j)
        hists[i][vars[j]] = (TH1F*)files.back()->Get(vars[j]);
    }

    printf("sigproflik setup:\nint lumi 'data': %f/fb\n", lumis[0]);
    for (int i = 1; i < nfiles; ++i) {
      taus.push_back(lumis[i] / lumis[0]);
      printf("bkg: %s   int lumi: %f/fb    tau: %f\n", filenames[i].c_str(), lumis[i], taus.back());
    }
  }

  double sig(const char* var, const int ibin) {
    double s = hists[0][var]->GetBinContent(ibin);
    double n = s;
    std::vector<double> m;
    //printf("   proflik: b/m:");
    for (int i = 1; i < nfiles; ++i) {
      double b = hists[i][var]->GetBinContent(ibin);
      n += b;
      m.push_back(b * taus[i-1]);
      //printf("%f/%f ", b, b*taus[i-1]);
    }
    //printf("   s: %f  n: %f\n", s, n);
    return getSignificance(0, n, s, m, taus);
  }
};

sigproflik* slik = 0;

void maxSSB(TH1F* sigHist, TH1F* bkgHist, const char* var) {
  if (printall) printf("%16s\tcut\t\ts\t\tb\tssb\tssbsb\tproflik\tsig frac\tsig eff\t\tbkg frac\tbkg eff\n", sigHist->GetName());
  int nbins = sigHist->GetNbinsX();
  double xlow = sigHist->GetXaxis()->GetXmin();
  double xup = sigHist->GetXaxis()->GetXmax();
  TH1F* h_ssb = new TH1F("h_ssb", ";cut;ssb", nbins, xlow, xup);
  TH1F* h_sigfrac = new TH1F("h_sigfrac", ";cut;sig frac", nbins, xlow, xup);
  TH1F* h_bkgfrac = new TH1F("h_bkgfrac", ";cut;bkg frac", nbins, xlow, xup);
  TH1F* h_ssbsb = new TH1F("h_ssbsb", ";cut;ssbsb", nbins, xlow, xup);
  TH1F* h_proflik = new TH1F("h_proflik", ";cut;asimov Z", nbins, xlow, xup);

  double value = 0;
  double smax = 0;
  double bmax = 0;
  double ssb = 0;
  for (int i = 1; i <= nbins; i++) {
    double s = sigHist->GetBinContent(i);
    double b = bkgHist->GetBinContent(i);
    double sigb = bkgHist->GetBinError(i);
    double zpl = slik->sig(var, i);
    if (printall) printf("%16s\t%5.1f\t%9.2f\t%9.2f\t%6.2f\t%f\t%f\t%f\t%e\n", "", sigHist->GetBinLowEdge(i), s, b, s/sqrt(b), s/sqrt(b+sigb), zpl, s/nsig, s/nsig_total, b/nbkg, b/nbkg_total);
    h_sigfrac->SetBinContent(i, s/nsig);
    h_bkgfrac->SetBinContent(i, b/nbkg);
    if (b != 0)
      h_ssb->SetBinContent(i, s/sqrt(b));
    if (b+sigb > 0)
      h_ssbsb->SetBinContent(i, s/sqrt(b+sigb));

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

  h_ssbsb->SetLineColor(kRed);
  h_proflik->SetLineColor(kBlue);
  TLegend* leg = new TLegend(0.9,0.9,1,1);
  leg->AddEntry(h_ssb, "s/#sqrt{b}", "L");
  leg->AddEntry(h_ssbsb, "s/#sqrt{b+#sigma_{b}}", "L");
  leg->AddEntry(h_proflik, "Z_{PL}", "L");

  if (plot) {
    for (int logy = 0; logy < 2; ++logy) {
      TCanvas* c1 = new TCanvas();
      c1->Divide(2,2);
      c1->cd(1)->SetLogy(logy);
      sigHist->SetLineColor(kRed);
      sigHist->Draw();
      c1->cd(3)->SetLogy(logy);
      bkgHist->Draw();
      c1->cd(2)->SetLogy(logy);
      draw_in_order(h_ssb, h_ssbsb, h_proflik);
      leg->Draw();
      c1->cd(4)->SetLogy(logy);
      h_sigfrac->SetLineColor(kRed);
      h_bkgfrac->SetLineColor(kBlue);
      draw_in_order(h_sigfrac, h_bkgfrac);
      c1->SaveAs(TString::Format("plots/SSB/iter%d/%s.pdf", niter, sigHist->GetName()));
      delete c1;
    }
  }

  delete h_ssb;
  delete h_ssbsb;
  delete h_proflik;
  delete h_sigfrac;
  delete h_bkgfrac;
  delete leg;
}

int main() {
  const int nvars = 9;
  const char* hnames[nvars] = {"ntracks", "njetssharetks", "maxtrackpt", "drmin", "drmax", "bs2dsig", "ntracks01", "njetssharetks01", "maxtrackpt01"};

  for (int i = 0; i <= niter; i++) {
    printf("iteration %d\n", i);
    slik = new sigproflik(hnames, nvars, TString::Format("crab/CutPlay%d/", i).Data());
    TFile* sigFile = TFile::Open(TString::Format("crab/CutPlay%d/mfv_neutralino_tau0100um_M0400_1pb.root", i));
    TFile* bkgFile = TFile::Open(TString::Format("crab/CutPlay%d/background.root", i));

    if (!printall) printf("variable\t\tcut\t\ts\t\tb\tmax ssb\tsig frac\tsig eff\t\tbkg frac\tbkg eff\n");
    for (int j = 0; j < nvars; j++) {
      TH1F* sigHist = (TH1F*)sigFile->Get(hnames[j]);
      TH1F* bkgHist = (TH1F*)bkgFile->Get(hnames[j]);
      maxSSB(sigHist, bkgHist, hnames[j]);
    }
    printf("\n");
    delete slik;
  }
}
