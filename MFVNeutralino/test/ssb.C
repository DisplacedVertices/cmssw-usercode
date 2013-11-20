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
#include "TError.h"
#include "TStyle.h"

const int niter = 1;
bool printall = 0;
bool plot = 0;

double nsig_total = 19788.362;
double nsig[niter+1] = {1023.41, 794.72};
//double nsig[niter+1] = {1023.41, 7342.61};

double nbkg_total = 211435861768.63;
double nbkg[niter+1] = {174811.73, 28369.66};

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

void draw_in_order(TH1F* a, TH1F* b, const char* cmd="") {
  std::vector<TH1F*> v = {a,b};
  draw_in_order(v, cmd);
}

void draw_in_order(TH1F* a, TH1F* b, TH1F* c, const char* cmd="") {
  std::vector<TH1F*> v = {a,b,c};
  draw_in_order(v, cmd);
}

void draw_in_order(TH1F* a, TH1F* b, TH1F* c, TH1F* d, const char* cmd="") {
  std::vector<TH1F*> v = {a,b,c,d};
  draw_in_order(v, cmd);
}

struct sigproflik {
  std::vector<std::string> filenames;
  std::vector<double> lumis;
  std::vector<double> taus;
  std::vector<TFile*> files;
  int nfiles;
  std::vector<std::map<std::string, TH1F*> > hists;

  sigproflik(const char** vars, const int nvars, const std::string dir, const bool bigw) {
    filenames.push_back(dir + "mfv_neutralino_tau0100um_M0400_mangled.root");
    filenames.push_back(dir + "ttbarhadronic_mangled.root");
    filenames.push_back(dir + "ttbarsemilep_mangled.root");
    filenames.push_back(dir + "ttbardilep_mangled.root");
    if (bigw) {
      filenames.push_back(dir + "qcdht0100_mangled.root");
      filenames.push_back(dir + "qcdht0250_mangled.root");
    }
    filenames.push_back(dir + "qcdht0500_mangled.root");
    filenames.push_back(dir + "qcdht1000_mangled.root");

    lumis.push_back(nsig_total/1000/0.199379);
    lumis.push_back(nsig_total/1000/0.386535);
    lumis.push_back(nsig_total/1000/0.153995);
    lumis.push_back(nsig_total/1000/0.077220);
    if (bigw) {
      lumis.push_back(nsig_total/1000/8210.69);
      lumis.push_back(nsig_total/1000/403.634);
    }
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

sigproflik* slik_nobigw = 0;
sigproflik* slik = 0;

void maxSSB(TH1F* sigHist, TH1F* bkgHist, const char* var) {
  if (printall) printf("%16s\tcut\t\ts\t\tb\tsigb\t\tssb\tssbsb\tproflik\tnobigw\tsig frac\tsig eff\t\tbkg frac\tbkg eff\n", sigHist->GetName());
  int nbins = sigHist->GetNbinsX();
  double xlow = sigHist->GetXaxis()->GetXmin();
  double xup = sigHist->GetXaxis()->GetXmax();
  TH1F* h_ssb = new TH1F("h_ssb", ";cut;ssb", nbins, xlow, xup);
  TH1F* h_sigfrac = new TH1F("h_sigfrac", ";cut;sig frac", nbins, xlow, xup);
  TH1F* h_bkgfrac = new TH1F("h_bkgfrac", ";cut;bkg frac", nbins, xlow, xup);
  TH1F* h_ssbsb = new TH1F("h_ssbsb", ";cut;ssbsb", nbins, xlow, xup);
  TH1F* h_proflik = new TH1F("h_proflik", ";cut;asimov Z", nbins, xlow, xup);
  TH1F* h_proflik_nobigw = new TH1F("h_proflik_nobigw", ";cut;asimov Z", nbins, xlow, xup);

  double value = 0;
  double smax = 0;
  double bmax = 0;
  double ssb = 0;
  for (int i = 1; i <= nbins; i++) {
    double s = sigHist->GetBinContent(i);
    double b = bkgHist->GetBinContent(i);
    double sigb = bkgHist->GetBinError(i);
    double zpl = slik->sig(var, i);
    double zpl_nobigw = slik_nobigw->sig(var, i);
    if (printall) printf("%16s\t%5.1f\t%9.2f\t%9.2f\t%9.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%f\t%f\t%f\t%e\n", "", sigHist->GetBinLowEdge(i), s, b, sigb, s/sqrt(b), s/sqrt(b+sigb), zpl, zpl_nobigw, s/nsig[niter], s/nsig_total, b/nbkg[niter], b/nbkg_total);
    h_sigfrac->SetBinContent(i, s/nsig[niter]);
    h_bkgfrac->SetBinContent(i, b/nbkg[niter]);
    if (b != 0)
      h_ssb->SetBinContent(i, s/sqrt(b));
    if (b+sigb > 0)
      h_ssbsb->SetBinContent(i, s/sqrt(b+sigb));
    if (!TMath::IsNaN(zpl))
      h_proflik->SetBinContent(i, zpl);
    if (!TMath::IsNaN(zpl_nobigw))
      h_proflik_nobigw->SetBinContent(i, zpl_nobigw);

    if (zpl_nobigw > ssb) {
      value = sigHist->GetBinLowEdge(i);
      smax = s;
      bmax = b;
      ssb = zpl_nobigw;
    }
  }
  if (printall) {
    printf("\n%16s\t%6.2f\t%9.2f\t%9.2f\t%6.2f\t\t\t%f\t%f\t%f\t%e\n\n\n", "max ssb", value, smax, bmax, ssb, smax/nsig[niter], smax/nsig_total, bmax/nbkg[niter], bmax/nbkg_total);
  } else {
    printf("%16s\t%6.2f\t%9.2f\t%9.2f\t%6.2f\t%f\t%f\t%f\t%e\n", sigHist->GetName(), value, smax, bmax, ssb, smax/nsig[niter], smax/nsig_total, bmax/nbkg[niter], bmax/nbkg_total);
  }

  h_ssbsb->SetLineColor(kRed);
  h_proflik_nobigw->SetLineColor(kBlue);
  h_proflik->SetLineColor(kOrange+2);
  TLegend* leg = new TLegend(0.8,0.8,1,1);
  leg->AddEntry(h_ssb, "s/#sqrt{b}", "L");
  leg->AddEntry(h_ssbsb, "s/#sqrt{b+#sigma_{b}}", "L");
  leg->AddEntry(h_proflik, "Z_{PL}", "L");
  leg->AddEntry(h_proflik_nobigw, "Z_{PL} (no big weights)", "L");

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
      draw_in_order(h_ssb, h_ssbsb, h_proflik, h_proflik_nobigw);
      leg->Draw();
      c1->cd(4)->SetLogy(logy);
      h_sigfrac->SetLineColor(kRed);
      h_bkgfrac->SetLineColor(kBlue);
      draw_in_order(h_sigfrac, h_bkgfrac);
      c1->SaveAs(TString::Format("plots/SSB/iter%d_tau0100um/%s%s.pdf", niter, sigHist->GetName(), (logy ? "_log" : "")));
      delete c1;
    }
  }

  delete h_ssb;
  delete h_ssbsb;
  delete h_proflik;
  delete h_proflik_nobigw;
  delete h_sigfrac;
  delete h_bkgfrac;
  delete leg;
}

int main() {
  gErrorIgnoreLevel = 1001;
  gStyle->SetPadTickX(1);
  gStyle->SetPadTickY(1);

  const int nvars = 17;
  const char* hnames[nvars] = {"ntracks", "njetssharetks", "maxtrackpt", "drmin", "drmax", "bs2dsig", "ntracks01", "njetssharetks01", "maxtrackpt01", "costhmombs", "mass", "jetsmassntks", "mass01", "jetsmassntks01", "pt", "ntracksptgt3", "sumpt2"};

  printf("iteration %d\n", niter);
  slik = new sigproflik(hnames, nvars, TString::Format("crab/CutPlay%d/", niter).Data(), true);
  slik_nobigw = new sigproflik(hnames, nvars, TString::Format("crab/CutPlay%d/", niter).Data(), false);
  TFile* sigFile = TFile::Open(TString::Format("crab/CutPlay%d/mfv_neutralino_tau0100um_M0400_1pb.root", niter));
  TFile* bkgFile = TFile::Open(TString::Format("crab/CutPlay%d/background.root", niter));

  if (!printall) printf("variable\t\tcut\t\ts\t\tb\tmax ssb\tsig frac\tsig eff\t\tbkg frac\tbkg eff\n");
  for (int i = 0; i < nvars; i++) {
    TH1F* sigHist = (TH1F*)sigFile->Get(hnames[i]);
    TH1F* bkgHist = (TH1F*)bkgFile->Get(hnames[i]);
    maxSSB(sigHist, bkgHist, hnames[i]);
  }
  delete slik;
  delete slik_nobigw;
}
