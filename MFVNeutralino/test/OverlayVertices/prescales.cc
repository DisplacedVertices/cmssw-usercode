#include <iostream>
#include "TCanvas.h"
#include "TFile.h"
#include "TH1.h"
#include "TTree.h"
#include "DVCode/MFVNeutralino/interface/MiniNtuple.h"

template <typename T> T mag (T x, T y) { return sqrt(x*x + y*y); }

int ntracks = 3;
const int target = 10000;
const int nbins = 400;

struct point {
  point(double a, double b) : x(a), y(b) {};
  double x, y;
  double d(const point& o) const { return mag(x - o.x, y - o.y); }
};
std::vector<point> vs;
// P = permutations = N(N-1), C = combinations N(N-1)/2
TH1D* h_P_dvvc = 0;
TH1D* h_P_prescales = 0;
TH1D* h_P_prescaled = 0;
TH1D* h_C_dvvc = 0;
TH1D* h_C_prescales = 0;
TH1D* h_C_prescaled = 0;

bool analyze(long long j, long long je, const mfv::MiniNtuple& nt) {
  if (j == 0)
    vs.clear();

  if (j % 1000 == 0)
    printf("\rtree event %lli/%lli", j, je);

  if (nt.nvtx == 1 && ((ntracks == 3 || ntracks == 4) && nt.ntk0 == ntracks) || (ntracks == 5 && nt.ntk0 >= ntracks))
    vs.push_back(point(nt.x0, nt.y0));

  const long long maxevents = -1;
  if (j == maxevents || j == je-1) {
    const size_t nv = vs.size();
    printf("\rtree done with %lli entries, %lu passed. double loop on passed:", je, nv);
    for (size_t i = 0; i < nv; ++i) {
      if (i % 10000 == 0) { printf(" %lu", i); fflush(stdout); }
      point a = vs[i];
      for (size_t j = 0; j < nv; ++j) {
        if (i == j) continue;
        point b = vs[j];

        if (i < j)
          h_C_dvvc->Fill(a.d(b));
        h_P_dvvc->Fill(a.d(b));
      }
    }
    printf(" %lu done\n", nv);

    for (int ibin = 1; ibin <= nbins; ++ibin) {
      const double c_P = h_P_dvvc->GetBinContent(ibin);
      const double c_C = h_C_dvvc->GetBinContent(ibin);
      h_P_prescales->SetBinContent(ibin, std::max(c_P / target, 1.));
      h_C_prescales->SetBinContent(ibin, std::max(c_C / target, 1.));
    }

    h_P_prescaled->Divide(h_P_dvvc, h_P_prescales);
    h_C_prescaled->Divide(h_C_dvvc, h_C_prescales);
    printf("integrals P: before prescale %15.f after %10.f\n", h_P_dvvc->Integral(), h_P_prescaled->Integral());
    printf("integrals C: before prescale %15.f after %10.f\n", h_C_dvvc->Integral(), h_C_prescaled->Integral());
    
    if (j == maxevents) return false;
  }

  return true;
}

int main() {
  const char* samples[] = {
    "qcdht0500sum", "qcdht0700sum", "qcdht1000sum", "qcdht1500sum", "qcdht2000sum", "ttbar", "background_noweight",
    "qcdht0500sum_2015", "qcdht0700sum_2015", "qcdht1000sum_2015", "qcdht1500sum_2015", "qcdht2000sum_2015", "ttbar_2015", "background_noweight_2015",
    "JetHT2015C", "JetHT2015D", "JetHT2015",
    "JetHT2016B3", "JetHT2016C", "JetHT2016D", "JetHT2016E", "JetHT2016F", "JetHT2016G", "JetHT2016H",
    "JetHT2016", "JetHT2016BthruG", "JetHT2016BCD", "JetHT2016EF",
  };

  const char* fn_path = "root://cmseos.fnal.gov//store/user/tucker/MiniTreeV14_forpick/%s.root";
  TFile out_f("prescales.root", "new");

  for (ntracks = 3; ntracks <= 5; ++ntracks) {
    printf("ntracks = %i:\n", ntracks);
    const char* tree_path =
      ntracks == 3 ? "mfvMiniTreeNtk3/t" :
      ntracks == 4 ? "mfvMiniTreeNtk4/t" :
      "mfvMiniTree/t";

    TDirectory* d = out_f.mkdir(TString::Format("ntk%i", ntracks));

    for (auto sample : samples) {
      printf("%s\n", sample);
      h_P_dvvc      = new TH1D(TString::Format("%s-P_dvvc",      sample), "", nbins, 0, 4);
      h_P_prescales = new TH1D(TString::Format("%s-P_prescales", sample), "", nbins, 0, 4);
      h_P_prescaled = new TH1D(TString::Format("%s-P_prescaled", sample), "", nbins, 0, 4);
      h_C_dvvc      = new TH1D(TString::Format("%s-C_dvvc",      sample), "", nbins, 0, 4);
      h_C_prescales = new TH1D(TString::Format("%s-C_prescales", sample), "", nbins, 0, 4);
      h_C_prescaled = new TH1D(TString::Format("%s-C_prescaled", sample), "", nbins, 0, 4);
      mfv::loop(TString::Format(fn_path, sample), tree_path, analyze);
      printf("\n");

      for (auto h : {h_P_dvvc, h_P_prescales, h_P_prescaled, h_C_dvvc, h_C_prescales, h_C_prescaled}) {
        d->cd();
        h->Write();
      }
    }
  }

  out_f.Close();
}
