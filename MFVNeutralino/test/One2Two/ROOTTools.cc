#include "ROOTTools.h"
#include <cassert>
#include <cmath>
#include "TColor.h"
#include "TH1.h"
#include "TROOT.h"
#include "TStyle.h"

namespace jmt {
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

  void set_root_style() {
    gROOT->SetStyle("Plain");
    gStyle->SetPalette(1);
    gStyle->SetFillColor(0);
    gStyle->SetOptDate(0);
    gStyle->SetOptStat(1222222);
    gStyle->SetOptFit(2222);
    gStyle->SetPadTickX(1);
    gStyle->SetPadTickY(1);
    gStyle->SetMarkerSize(.1);
    gStyle->SetMarkerStyle(8);
    gStyle->SetGridStyle(3);
    gROOT->ProcessLine("gErrorIgnoreLevel = 1001;");
    double palinfo[4][5] = {{0,0,0,1,1},{0,1,1,1,0},{1,1,0,0,0},{0,0.25,0.5,0.75,1}};
    TColor::CreateGradientColorTable(5, palinfo[3], palinfo[0], palinfo[1], palinfo[2], 500);
    gStyle->SetNumberContours(500);
    TH1::SetDefaultSumw2();
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
