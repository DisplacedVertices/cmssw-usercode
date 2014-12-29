#include <cassert>
#include <cmath>
#include "Math/QuantFuncMathCore.h"
#include "TColor.h"
#include "TFile.h"
#include "TH1.h"
#include "TROOT.h"
#include "TStyle.h"
#include "TTree.h"
#include "TVector2.h"
#include "JMTucker/MFVNeutralino/interface/MovedTracksNtuple.h"

template <typename T>
T mag(T x, T y, T z=0) {
  return sqrt(x*x + y*y + z*z);
}

struct interval {
  bool success;
  double value;
  double lower;
  double upper;
  double error() const { return (upper - lower)/2; }
  double in(double v) const { return v >= lower && v <= upper; }
};

interval clopper_pearson_binom(const double n_on, const double n_tot,
                               const double alpha=1-0.6827, const bool equal_tailed=true) {
  const double alpha_min = equal_tailed ? alpha/2 : alpha;

  interval i;
  i.success = !(n_on == 0 && n_tot == 0);
  i.value = n_on / n_tot;
  i.lower = 0;
  i.upper = 1;

  if (n_on > 0)         i.lower = ROOT::Math::beta_quantile  (alpha_min, n_on,     n_tot - n_on + 1);
  if (n_tot - n_on > 0) i.upper = ROOT::Math::beta_quantile_c(alpha_min, n_on + 1, n_tot - n_on);

  return i;
}

struct numden {
  numden(const char* name, const char* title, int nbins, double xlo, double xhi)
    : num(new TH1F(TString::Format("%s_num", name), title, nbins, xlo, xhi)),
      den(new TH1F(TString::Format("%s_den", name), title, nbins, xlo, xhi))
  {}
  // no ownership, the TFile owns the histos
  TH1F* num;
  TH1F* den;
};

struct numdens {
  numdens(const char* c) : common(c) {}
  void book(const char* name, const char* title, int nbins, double xlo, double xhi) {
    m.insert(std::make_pair(std::string(name), numden((common + name).c_str(), title, nbins, xlo, xhi)));
  }
  numden& operator()(const std::string& w) {
    auto it = m.find(w);
    assert(it != m.end());
    return it->second;
  }
  std::string common;
  std::map<std::string, numden> m;
};

int main(int argc, char** argv) {
  if (argc < 3) {
    fprintf(stderr, "usage: hists.exe in.root out.root\n");
    return 1;
  }

  const char* in_fn  = argv[1];
  const char* out_fn = argv[2];
  const int njets_req = 2;
  const int nbjets_req = 1;
  const bool apply_weight = true;

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

  TFile* f = new TFile(in_fn);
  if (!f || !f->IsOpen()) {
    fprintf(stderr, "could not open %s\n", in_fn);
    return 1;
  }

  const char* tree_path = "mfvMovedTree/t";
  TTree* t = (TTree*)f->Get(tree_path);
  if (!t) {
    fprintf(stderr, "could not get tree %s from %s\n", tree_path, in_fn);
    return 1;
  }

  mfv::MovedTracksNtuple nt;
  nt.read_from_tree(t);

  TFile* f_out = new TFile(out_fn, "recreate");

  TH1F* h_weight = new TH1F("h_weight", ";weight;events/0.01", 200, 0, 2);
  TH1F* h_npu = new TH1F("h_npu", ";# PU;events/1", 100, 0, 100);

  numdens nds[6] = {
    numdens("nocuts"),
    numdens("ntracks"),
    numdens("ntracksPptgt3"),
    numdens("ntracksPptgt3Pdr"),
    numdens("ntracksPptgt3Pbs2d"),
    numdens("all")
  };

  for (numdens& nd : nds) {
    nd.book("movedist2", ";movement 2-dist;events/0.01 cm", 200, 0, 2);
    nd.book("movedist3", ";movement 3-dist;events/0.01 cm", 200, 0, 2);
    nd.book("npv", ";# PV;events/1", 100, 0, 100);
    nd.book("pvx", ";PV x (cm);events/1.5 #mum", 200, -0.015, 0.015);
    nd.book("pvy", ";PV y (cm);events/1.5 #mum", 200, -0.015, 0.015);
    nd.book("pvz", ";PV z (cm);events/0.24 cm", 200, -24, 24);
    nd.book("pvrho", ";PV #rho (cm);events/1 #mum", 200, 0, 0.02);
    nd.book("pvntracks", ";PV # tracks;events/2", 200, 0, 400);
    nd.book("pvsumpt2", ";PV #Sigma p_{T}^{2} (GeV^{2});events/200 GeV^{2}", 200, 0, 40000);
    nd.book("ntracks", ";# tracks;events/10", 200, 0, 2000);
    nd.book("nseltracks", ";# selected tracks;events/2", 200, 0, 400);
    nd.book("npreseljets", ";# preselected jets;events/1", 20, 0, 20);
    nd.book("npreselbjets", ";# preselected b jets;events/1", 20, 0, 20);
    nd.book("jetsume", ";#Sigma jet energy (GeV);events/5 GeV", 200, 0, 1000);
    nd.book("jetdrmax", ";max jet #Delta R;events/0.1", 70, 0, 7);
    nd.book("jetdravg", ";avg jet #Delta R;events/0.1", 70, 0, 7);
    nd.book("jetsumntracks", ";#Sigma jet # tracks;events/2", 200, 0, 400);
  }

  double den = 0;
  std::map<std::string, double> nums;

  for (int j = 0, je = t->GetEntries(); j < je; ++j) {
    if (t->LoadTree(j) < 0) break;
    if (t->GetEntry(j) <= 0) continue;
    if (j % 250000 == 0) {
      printf("\r%i/%i", j, je);
      fflush(stdout);
    }

    const double w = apply_weight ? nt.weight : 1.;

    const double movedist2 = mag(nt.move_x - nt.pvx,
                                 nt.move_y - nt.pvy);
    const double movedist3 = mag(nt.move_x - nt.pvx,
                                 nt.move_y - nt.pvy,
                                 nt.move_z - nt.pvz);

    const size_t n_raw_vtx = nt.p_vtxs_x->size();

    double jet_sume = 0;
    double jet_drmax = 0;
    double jet_dravg = 0;
    double jet_sumntracks;
    const size_t n_jets = nt.p_jets_pt->size();
    for (size_t ijet = 0; ijet < n_jets; ++ijet) {
      jet_sume += nt.p_jets_energy->at(ijet);
      jet_sumntracks += nt.p_jets_ntracks->at(ijet);

      for (size_t jjet = ijet+1; jjet < n_jets; ++jjet) {
        const double dr = mag(double(nt.p_jets_eta->at(ijet) - nt.p_jets_eta->at(jjet)),
                              TVector2::Phi_mpi_pi(nt.p_jets_phi->at(ijet) - nt.p_jets_phi->at(jjet)));
        jet_dravg += dr;
        if (dr > jet_drmax)
          jet_drmax = dr;
      }
    }
    jet_dravg /= n_jets * (n_jets - 1) / 2.;
    
    if (nt.npreseljets < njets_req || 
        nt.npreselbjets < nbjets_req ||
        movedist2 < 0.03 ||
        movedist2 > 2.5 ||
        jet_drmax > 4)
      continue;

    h_weight->Fill(w);
    h_npu->Fill(nt.npu, w);

    auto Fill = [&w](TH1F* h, double v) { h->Fill(v, w); };

    for (numdens& nd : nds) {
      Fill(nd("movedist2")    .den, movedist2);
      Fill(nd("movedist3")    .den, movedist3);
      Fill(nd("npv")          .den, nt.npv);
      Fill(nd("pvx")          .den, nt.pvx);
      Fill(nd("pvy")          .den, nt.pvy);
      Fill(nd("pvz")          .den, nt.pvz);
      Fill(nd("pvrho")        .den, mag(nt.pvx, nt.pvy));
      Fill(nd("pvntracks")    .den, nt.pvntracks);
      Fill(nd("pvsumpt2")     .den, nt.pvsumpt2);
      Fill(nd("ntracks")      .den, nt.ntracks);
      Fill(nd("nseltracks")   .den, nt.nseltracks);
      Fill(nd("npreseljets")  .den, nt.npreseljets);
      Fill(nd("npreselbjets") .den, nt.npreselbjets);
      Fill(nd("jetsume")      .den, jet_sume);
      Fill(nd("jetdrmax")     .den, jet_drmax);
      Fill(nd("jetdravg")     .den, jet_dravg);
      Fill(nd("jetsumntracks").den, jet_sumntracks);
    }

    den += w;

    int wvtx = -1;
    if (n_raw_vtx > 2)
      {}
    if (n_raw_vtx == 1)
      wvtx = 0;
    else if (n_raw_vtx >= 2) {
      for (size_t ivtx = 0; ivtx < n_raw_vtx; ++ivtx) {
        if (mag(nt.move_x - nt.p_vtxs_x->at(ivtx),
                nt.move_y - nt.p_vtxs_y->at(ivtx)) < 0.005)
          wvtx = int(ivtx);
      }
    }

    if (wvtx < 0)
      continue;

    const bool pass_ntracks      = nt.p_vtxs_ntracks     ->at(wvtx) >= 5;
    const bool pass_ntracksptgt3 = nt.p_vtxs_ntracksptgt3->at(wvtx) >= 3;
    const bool pass_drmin        = nt.p_vtxs_drmin       ->at(wvtx) < 0.4;
    const bool pass_drmax        = nt.p_vtxs_drmax       ->at(wvtx) < 4;
    const bool pass_mindrmax     = nt.p_vtxs_drmax       ->at(wvtx) > 1.2;
    const bool pass_bs2derr      = nt.p_vtxs_bs2derr     ->at(wvtx) < 0.0025;

    const bool pass_ntrackscuts = pass_ntracks && pass_ntracksptgt3;
    const bool pass_drcuts = pass_drmin && pass_drmax && pass_mindrmax;

                                                         nums["nocuts"]             += w;
    if (pass_ntracks)                                    nums["ntracks"]            += w;
    if (pass_ntrackscuts)                                nums["ntracksPptgt3"]      += w;
    if (pass_ntrackscuts && pass_drcuts)                 nums["ntracksPptgt3Pdr"]   += w;
    if (pass_ntrackscuts && pass_drcuts && pass_bs2derr) nums["all"]                += w;
    if (pass_ntrackscuts                && pass_bs2derr) nums["ntracksPptgt3Pbs2d"] += w;

    const bool passes[6] = {
      true,
      pass_ntracks,
      pass_ntrackscuts,
      pass_ntrackscuts && pass_drcuts,
      pass_ntrackscuts                && pass_bs2derr,
      pass_ntrackscuts && pass_drcuts && pass_bs2derr
    };

    for (int i = 0; i < 6; ++i) {
      if (passes[i]) {
        numdens& nd = nds[i];
        Fill(nd("movedist2")    .num, movedist2);
        Fill(nd("movedist3")    .num, movedist3);
        Fill(nd("npv")          .num, nt.npv);
        Fill(nd("pvx")          .num, nt.pvx);
        Fill(nd("pvy")          .num, nt.pvy);
        Fill(nd("pvz")          .num, nt.pvz);
        Fill(nd("pvrho")        .num, mag(nt.pvx, nt.pvy));
        Fill(nd("pvntracks")    .num, nt.pvntracks);
        Fill(nd("pvsumpt2")     .num, nt.pvsumpt2);
        Fill(nd("ntracks")      .num, nt.ntracks);
        Fill(nd("nseltracks")   .num, nt.nseltracks);
        Fill(nd("npreseljets")  .num, nt.npreseljets);
        Fill(nd("npreselbjets") .num, nt.npreselbjets);
        Fill(nd("jetsume")      .num, jet_sume);
        Fill(nd("jetdrmax")     .num, jet_drmax);
        Fill(nd("jetdravg")     .num, jet_dravg);
        Fill(nd("jetsumntracks").num, jet_sumntracks);
      }
    }
  }

  printf("\r                                \n");
  printf("%f events in denominator\n", den);
  printf("%30s  %12s  %12s   %10s [%10s, %10s] +%10s -%10s\n", "name", "num", "den", "eff", "lo", "hi", "+", "-");
  for (const auto& p : nums) {
    const interval i = clopper_pearson_binom(p.second, den);
    printf("%30s  %12f  %12f  %10f [%10f, %10f] +%10f -%10f\n", p.first.c_str(), p.second, den, i.value, i.lower, i.upper, i.upper - i.value, i.value - i.lower);
  }

  f_out->Write();
  f_out->Close();
  f->Close();

  delete f;
  delete f_out;
}
