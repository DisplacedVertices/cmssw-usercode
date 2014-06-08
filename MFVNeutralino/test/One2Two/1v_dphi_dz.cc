// rootg++ -I../../../.. ../../src/MiniNtuple.cc 1v_dphi_dz.cc -o 1v_dphi_dz.exe && ./1v_dphi_dz.exe && cp 1v_dphi_dz.root ~/asdf/

#include <cmath>
#include <cstdlib>
#include "TCanvas.h"
#include "TError.h"
#include "TFile.h"
#include "TH1.h"
#include "TPaveStats.h"
#include "TRandom3.h"
#include "TStyle.h"
#include "TTree.h"
#include "TVector2.h"
#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"

int nbins_phi = 8;
int min_ntracks = 5;

struct V {
  double phi;
  double z;

  V() : phi(0), z(0) {}
  V(double a, double b) : phi(a), z(b) {}

  V(const V& a, const V& b)
    : phi(TVector2::Phi_mpi_pi(a.phi - b.phi)),
      z(a.z - b.z)
  {}
};

int main() {
  gStyle->SetOptStat(2222222);
  gStyle->SetOptFit(2222);
  gStyle->SetPadTickX(1);
  gStyle->SetPadTickY(1);
  gErrorIgnoreLevel = 1001;

  TFile* fout = new TFile("1v_dphi_dz.root", "recreate");
  TH1F* h_1v_phi     = new TH1F("h_1v_phi",     TString::Format("1v events (# tracks #geq %i);#phi;vertices/%.2f",               min_ntracks, 2*M_PI/nbins_phi), nbins_phi, -M_PI, M_PI);
  TH1F* h_1v_dphi    = new TH1F("h_1v_dphi",    TString::Format("pairs of 1v events (# tracks #geq %i);#Delta#phi;pairs/%.2f",   min_ntracks, 2*M_PI/nbins_phi), nbins_phi, -M_PI, M_PI);
  TH1F* h_1v_absdphi = new TH1F("h_1v_absdphi", TString::Format("pairs of 1v events (# tracks #geq %i);|#Delta#phi|;pairs/%.2f", min_ntracks, 2*M_PI/nbins_phi), nbins_phi,     0, M_PI);
  TH1F* h_1v_z  = new TH1F("h_1v_z",  TString::Format("1v events (# tracks #geq %i);z (cm);vertices/%.1f",    min_ntracks, 80./200), 200, -40, 40);
  TH1F* h_1v_dz = new TH1F("h_1v_dz", TString::Format("1v events (# tracks #geq %i);#Deltaz (cm);pairs/%.1f", min_ntracks, 80./400), 400, -40, 40);

  mfv::MiniNtuple nt;
  TFile* f = TFile::Open("crab/MiniTreeV18/qcdht1000.root");
  TTree* t = (TTree*)f->Get("mfvMiniTree/t");
  
  mfv::read_from_tree(t, nt);
 
  std::vector<V> v1v;

  for (int j = 0, je = t->GetEntries(); j < je; ++j) {
    if (t->LoadTree(j) < 0) break;
    if (t->GetEntry(j) <= 0) continue;

    // Also add the 2v events where one vertex fails
    // min_ntracks. Don't need to do the other combination since ntk0
    // >= ntk1 by construction.
    if ((nt.nvtx == 1 && nt.ntk0 >= min_ntracks) || (nt.nvtx == 2 && nt.ntk0 >= min_ntracks && nt.ntk1 < min_ntracks)) {
      V v;

      v.phi = atan2(nt.y0, nt.x0);
      h_1v_phi->Fill(v.phi);

      v.z = nt.z0;
      h_1v_z->Fill(v.z);

      v1v.push_back(v);
    }
  }

  const int n = int(v1v.size());
  printf("%i v1vs.\n", n);

  const int npairs = 100000;
  if (npairs > 0) {
    for (int ii = 0; ii < npairs; ++ii) {
      const int i = gRandom->Integer(n);
      const int j = gRandom->Integer(n);

      V d(v1v[i], v1v[j]);
      h_1v_dphi->Fill(d.phi);
      h_1v_absdphi->Fill(fabs(d.phi));
      h_1v_dz->Fill(d.z);
    }
  }
  else {
    int i = 0;
    for (; i < n; ++i) {
      if (i % 1000 == 0) {
        printf("\ri: %i", i);
        fflush(stdout);
      }

      for (int j = i+1; j < n; ++j) {
        V d(v1v[i], v1v[j]);
        h_1v_dphi->Fill(d.phi);
        h_1v_absdphi->Fill(fabs(d.phi));
        h_1v_dz->Fill(d.z);
      }
    }

    printf("\r                       \ri: %i\npairs: %i\n", i, int(h_1v_dphi->GetEntries()));
  }

  const TString path("/uscms/home/tucker/asdf/plots/1v_dphi_dz");
  system(("mkdir -p " + path).Data());

  TCanvas* c = new TCanvas("c", "", 600, 600);

  FILE* fhtml = fopen((path + "/index.html").Data(), "wt");
  if (!fhtml) {
    fprintf(stderr, "can't open html file?\n");
    return 1;
  }

  TH1F* hphis[3] = { h_1v_phi, h_1v_dphi, h_1v_absdphi };
  for (int i = 0; i < 3; ++i) {
    TH1F* h = hphis[i];
    double x, m = 0;
    for (int ib = 0; ib < h->GetNbinsX(); ++ib)
      if ((x = h->GetBinContent(ib)) > m)
        m = x;
    h->GetYaxis()->SetRangeUser(0, m*1.05);
    h->Fit("pol0", "Q");
    c->Update();
    TPaveStats* s = (TPaveStats*)h->FindObject("stats");
    s->SetX1NDC(0.471);
    s->SetY1NDC(0.133);
    s->SetX2NDC(0.864);
    s->SetY2NDC(0.509);
    TString n = h->GetName();
    n.Remove(0, 2);
    const char* nn = n.Data();
    c->SaveAs(TString::Format("%s/%i_%s.root", path.Data(), i, nn));
    c->SaveAs(TString::Format("%s/%i_%s.png",  path.Data(), i, nn));
    fprintf(fhtml, "<h4>%i_%s</h4>:<br><a href=\"%i_%s.root\"><img src=\"%i_%s.png\"></a>\n<br>\n", i, nn, i, nn, i, nn);
  }


  TH1F* hzs[2] = { h_1v_z, h_1v_dz };
  for (int i = 0; i < 2; ++i) {
    TH1F* h = hzs[i];
    h->Fit("gaus", "Q");
    c->Update();
    TPaveStats* s = (TPaveStats*)h->FindObject("stats");
    s->SetX1NDC(0.604);
    s->SetY1NDC(0.484);
    s->SetX2NDC(0.997);
    s->SetY2NDC(0.860);
    TString n = h->GetName();
    n.Remove(0, 2);
    const char* nn = n.Data();
    const int j = 3+i;
    c->SaveAs(TString::Format("%s/%i_%s.root", path.Data(), j, nn));
    c->SaveAs(TString::Format("%s/%i_%s.png",  path.Data(), j, nn));
    c->SetLogy();
    c->SaveAs(TString::Format("%s/%i_%s_log.png",  path.Data(), i, nn));
    c->SetLogy(0);
    fprintf(fhtml, "<h4>%i_%s</h4>:<br><a href=\"%i_%s.root\"><img src=\"%i_%s.png\"></a><a href=\"%i_%s.root\"><img src=\"%i_%s_log.png\"></a>\n<br>\n", j, nn, j, nn, j, nn, j, nn, j, nn);
  }

  fclose(fhtml);

  fout->Write();
  fout->Close();
  delete fout;
  f->Close();
  delete f;
}
