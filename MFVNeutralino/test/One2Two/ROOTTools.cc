#include "ROOTTools.h"
#include <cassert>
#include <cmath>
#include "TColor.h"
#include "TGraphAsymmErrors.h"
#include "TH1.h"
#include "TPaveStats.h"
#include "TROOT.h"
#include "TStyle.h"
#include "Prob.h"

namespace jmt {
  void cumulate(TH1D* h, const bool do_overflow) {
    const int nbins = h->GetNbinsX();
    int last = do_overflow ? nbins + 1 : nbins;
    for (int ibin = 1; ibin <= last; ++ibin) {
      const double valm1 = h->GetBinContent(ibin-1);
      const double errm1 = h->GetBinError  (ibin-1);
      const double val = h->GetBinContent(ibin);
      const double err = h->GetBinError  (ibin);
      h->SetBinContent(ibin, val + valm1);
      h->SetBinError  (ibin, sqrt(err*err + errm1*errm1));
    }
  }

  void deoverflow(TH1D* h) {
    const int nb = h->GetNbinsX();
    const double l  = h->GetBinContent(nb);
    const double le = h->GetBinError  (nb);
    const double o  = h->GetBinContent(nb+1);
    const double oe = h->GetBinError  (nb+1);
    h->SetBinContent(nb, l + o);
    h->SetBinError  (nb, sqrt(le*le + oe*oe));
    h->SetBinContent(nb+1, 0);
    h->SetBinError  (nb+1, 0);
  }

  void deunderflow(TH1D* h) {
    const double f  = h->GetBinContent(1);
    const double fe = h->GetBinError  (1);
    const double u  = h->GetBinContent(0);
    const double ue = h->GetBinError  (0);
    h->SetBinContent(1, f + u);
    h->SetBinError  (1, sqrt(fe*fe + ue*ue));
    h->SetBinContent(0, 0);
    h->SetBinError  (0, 0);
  }

  void divide_by_bin_width(TH1D* h) {
    const int nbins = h->GetNbinsX();
    for (int ibin = 1; ibin <= nbins; ++ibin) {
      const double width = h->GetBinWidth(ibin);
      const double val = h->GetBinContent(ibin);
      const double err = h->GetBinError  (ibin);
      h->SetBinContent(ibin, val/width);
      h->SetBinError  (ibin, err/width);
    }
  }

  double integral(const TH1* h) {
    return h->Integral(0, h->GetNbinsX()+1);
  }

  TPaveStats* move_stat_box(TPaveStats* s, double dx, double dy) {
    // Move the stat box s by (dx, dy), preserving width. (Remember
    // to call TCanvas::Update first.)

    s->SetX1NDC(s->GetX1NDC() + dx);
    s->SetY1NDC(s->GetY1NDC() + dy);
    s->SetX2NDC(s->GetX2NDC() + dx);
    s->SetY2NDC(s->GetY2NDC() + dy);
    
    return s;
  }

  TPaveStats* move_stat_box(TH1* h, double dx, double dy) {
    return move_stat_box((TPaveStats*)h->FindObject("stats"), dx, dy);
  }

  TPaveStats* move_stat_box(TPaveStats* s, double x1, double y1, double x2, double y2) {
    // Move the stat box s to the NDC coords (x1, y1, x2, y2)
    // specified. (Remember to call TCanvas::Update first.)

    s->SetX1NDC(x1);
    s->SetY1NDC(y1);
    s->SetX2NDC(x2);
    s->SetY2NDC(y2);

    return s;
  }

  TPaveStats* move_stat_box(TH1* h, double x0, double y0, double x1, double y1) {
    return move_stat_box((TPaveStats*)h->FindObject("stats"), x0, y0, x1, y1);
  }

  TGraphAsymmErrors* poisson_intervalize(const TH1D* h, const bool zero_x, const bool include_zero_bins) {
    std::vector<int> bins;
    for (int ibin = 1; ibin <= h->GetNbinsX(); ++ibin)
      if (include_zero_bins || h->GetBinContent(ibin) > 0)
        bins.push_back(ibin);

    TGraphAsymmErrors* h2 = new TGraphAsymmErrors(bins.size());
    int np = 0; // TGraphs count from 0
    for (int ibin : bins) {
      const double xl = h->GetBinLowEdge(ibin);
      const double xh = h->GetBinLowEdge(ibin+1);
      const double x = (xl + xh)/2;
      const double y = h->GetBinContent(ibin);
      const interval i = garwood_poisson(y);
      h2->SetPoint(np, x, y);

      if (zero_x) {
        h2->SetPointEXlow (np, 0);
        h2->SetPointEXhigh(np, 0);
      }
      else {
        h2->SetPointEXlow (np, x - xl);
        h2->SetPointEXhigh(np, xh - x);
      }

      h2->SetPointEYlow (np, y - i.lower);
      h2->SetPointEYhigh(np, i.upper - y);

      ++np;
    }

    return h2;
  }
  
  void set_root_style() {
    gStyle->SetPalette(1);
    gStyle->SetOptStat(1222222);
    gStyle->SetOptFit(2222);
    gStyle->SetStatX(0.85);
    gStyle->SetStatY(0.85);
    gStyle->SetStatW(0.2);
    gStyle->SetStatH(0.05); 
    gStyle->SetPadTickX(1);
    gStyle->SetPadTickY(1);
    gStyle->SetGridStyle(3);
    gROOT->ProcessLine("gErrorIgnoreLevel = kWarning;");
    double palinfo[4][5] = {{0,0,0,1,1},{0,1,1,1,0},{1,1,0,0,0},{0,0.25,0.5,0.75,1}};
    TColor::CreateGradientColorTable(5, palinfo[3], palinfo[0], palinfo[1], palinfo[2], 500);
    gStyle->SetNumberContours(500);
  }

  TH1D* shift_hist(const TH1D* h, const int shift) {
    assert(shift >= 0);
    assert(h->GetBinContent(0) == 0.);

    const int nbins = h->GetNbinsX();
    TH1D* hshift = (TH1D*)h->Clone(TString::Format("%s_shift%i", h->GetName(), shift));
    if (shift == 0)
      return hshift;

    for (int ibin = 1; ibin <= nbins+1; ++ibin) {
      const int ifrom = ibin - shift;
      double val = 0, err = 0;
      if (ifrom >= 1) { // don't shift in from underflow, shouldn't be any with svdist = positive quantity anyway
        val = h->GetBinContent(ifrom);
        err = h->GetBinError  (ifrom);
      }
      if (ibin == nbins+1) {
        double var = err*err;
        for (int irest = ifrom+1; irest <= nbins+1; ++irest) {
          val += h->GetBinContent(irest);
          var += pow(h->GetBinError(irest), 2);
        }
        err = sqrt(var);
      }

      hshift->SetBinContent(ibin, val);
      hshift->SetBinError  (ibin, err);
    }

    return hshift;
  }
}
