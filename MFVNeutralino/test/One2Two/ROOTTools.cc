#include "ROOTTools.h"
#include "TH1.h"
#include "TROOT.h"
#include "TStyle.h"

namespace jmt {
  void SetROOTStyle() {
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
}
