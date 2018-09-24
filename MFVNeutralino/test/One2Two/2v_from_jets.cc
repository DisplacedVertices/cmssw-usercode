/*
 * This program constructs the background template from one-vertex events.
 * Set the input parameters at the top of the method construct_dvvc().
 * Set which combinations of input parameters to run in main().
 * To run: compile with the Makefile (make); execute (./2v_from_jets.exe); delete the .exe (make clean).
 *
 * Here are details on each of the input parameters:
 * which filepath?
 *  - Provide the filepath to the MiniTree directory.
 *
 * which samples?
 *  - The MC and data samples and weights are set in static arrays; edit nbkg if necessary.
 *  - For the 2017 MC samples the weights calculated assume an integrated luminosity of 41.53 fb^-1 and the original number of events for each sample:
 *      python -i ../../../Tools/python/Samples.py
 *      >>> for sample in qcd_samples_2017 + ttbar_samples_2017:
 *      ...     print '%14s %7.1f %6.1f %9d %7.5f' % (sample.name, 41530., sample.xsec, sample.nevents_orig, 41530.*sample.xsec/sample.nevents_orig)
 *  - For the background template only the relative weights are relevant because we only construct the shape; the normalization comes from the fit.
 *  - Todo: MC weights and data samples for 2018.
 *  - If the sample arrays is modified, ibkg_begin and ibkg_end should also be modified.
 *
 * which ntracks?
 *  - This sets the treepath and shouldn't need to be modified.  (For Ntk3or4 two-vertex event is considered to be 4-track x 3-track if ntk0==4 and ntk1==3.)
 *
 * deltaphi input
 *  - Run fit_jetpairdphi.py to get the values of dphi_pdf_c, dphi_pdf_a.
 *  - Todo: update for 2017 (the current values are from 2015+2016 data).
 *
 * efficiency input
 *  - Run vertexer_eff.py to get the .root file with the efficiency curve.
 *  - vpeffs_version refers to the version of VertexerPairEffs.
 *
 * bquark input
 *  - Derive the b quark corrections; here is the procedure.
 *  - Run 2v_from_jets.cc with correct_bquarks = false, bquarks = 1 (with b quarks).
 *  - Run 2v_from_jets.cc with correct_bquarks = false, bquarks = 0 (without b quarks).
 *  - In MFVNeutralino/test: python utilities.py merge_bquarks_nobquarks
 *  - Run bquark_correction.py to get the values of the b quark corrections.
 *  - Todo: update for 2017 (the current values are from 2015+2016 MC).
 */

#include <cstdlib>
#include <math.h>
#include "TCanvas.h"
#include "TF1.h"
#include "TFile.h"
#include "TH2F.h"
#include "TLegend.h"
#include "TMath.h"
#include "TRandom3.h"
#include "TTree.h"
#include "TVector2.h"
#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"

int dvv_nbins = 40;
double dvv_bin_width = 0.01;

float ht(int njets, float* jet_pt) {
  double sum = 0;
  for (int i = 0; i < njets; ++i) {
    sum += jet_pt[i];
  }
  return sum;
}

struct ConstructDvvcParameters {
  bool is_mc_;
  bool only_10pc_;
  bool inject_signal_;
  std::string year_;
  int ntracks_;
  bool correct_bquarks_;
  int bquarks_;
  bool vary_dphi_;
  bool clearing_from_eff_;
  bool vary_eff_;
  bool vary_bquarks_;
  int min_npu_;
  int max_npu_;

  ConstructDvvcParameters()
    : is_mc_(true),
      only_10pc_(false),
      inject_signal_(false),
      year_("2017"),
      ntracks_(5),
      correct_bquarks_(true),
      bquarks_(-1),
      vary_dphi_(false),
      clearing_from_eff_(true),
      vary_eff_(false),
      vary_bquarks_(false),
      min_npu_(0),
      max_npu_(255)
  {
  }

  bool is_mc() const { return is_mc_; }
  bool only_10pc() const { return only_10pc_; }
  bool inject_signal() const { return inject_signal_; }
  std::string year() const { return year_; }
  int ntracks() const { return ntracks_; }
  bool correct_bquarks() const { return correct_bquarks_; }
  int bquarks() const { return bquarks_; }
  bool vary_dphi() const { return vary_dphi_; }
  bool clearing_from_eff() const { return clearing_from_eff_; }
  bool vary_eff() const { return vary_eff_; }
  bool vary_bquarks() const { return vary_bquarks_; }
  int min_npu() const { return min_npu_; }
  int max_npu() const { return max_npu_; }

  ConstructDvvcParameters is_mc(bool x)             { ConstructDvvcParameters y(*this); y.is_mc_             = x; return y; }
  ConstructDvvcParameters only_10pc(bool x)         { ConstructDvvcParameters y(*this); y.only_10pc_         = x; return y; }
  ConstructDvvcParameters inject_signal(bool x)     { ConstructDvvcParameters y(*this); y.inject_signal_     = x; return y; }
  ConstructDvvcParameters year(std::string x)       { ConstructDvvcParameters y(*this); y.year_              = x; return y; }
  ConstructDvvcParameters ntracks(int x)            { ConstructDvvcParameters y(*this); y.ntracks_           = x; return y; }
  ConstructDvvcParameters correct_bquarks(bool x)   { ConstructDvvcParameters y(*this); y.correct_bquarks_   = x; return y; }
  ConstructDvvcParameters bquarks(int x)            { ConstructDvvcParameters y(*this); y.bquarks_           = x; return y; }
  ConstructDvvcParameters vary_dphi(bool x)         { ConstructDvvcParameters y(*this); y.vary_dphi_         = x; return y; }
  ConstructDvvcParameters clearing_from_eff(bool x) { ConstructDvvcParameters y(*this); y.clearing_from_eff_ = x; return y; }
  ConstructDvvcParameters vary_eff(bool x)          { ConstructDvvcParameters y(*this); y.vary_eff_          = x; return y; }
  ConstructDvvcParameters vary_bquarks(bool x)      { ConstructDvvcParameters y(*this); y.vary_bquarks_      = x; return y; }
  ConstructDvvcParameters min_npu(int x)            { ConstructDvvcParameters y(*this); y.min_npu_           = x; return y; }
  ConstructDvvcParameters max_npu(int x)            { ConstructDvvcParameters y(*this); y.max_npu_           = x; return y; }

  void print() const {
    printf("is_mc = %d, only_10pc = %d, inject_signal = %d, year = %s, ntracks = %d, correct_bquarks = %d, bquarks = %d, vary_dphi = %d, clearing_from_eff = %d, vary_eff = %d, vary_bquarks = %d", is_mc(), only_10pc(), inject_signal(), year_.c_str(), ntracks(), correct_bquarks(), bquarks(), vary_dphi(), clearing_from_eff(), vary_eff(), vary_bquarks());
  }
};

void construct_dvvc(ConstructDvvcParameters p, const char* out_fn) {
  p.print(); printf(", out_fn = %s\n", out_fn);

  const char* file_path; //which filepath?
  if (p.only_10pc()) {
    file_path = "/uscms_data/d2/tucker/crab_dirs/MiniTreeV20mp2";
  } else {
    file_path = "/uscms_data/d2/tucker/crab_dirs/MiniTreeV20mp2";
  }

  const int nbkg = 18; //which samples?
  const char* samples[nbkg];
  float       weights[nbkg];
  samples[0]  = "mfv_neu_tau001000um_M0800_2017"; weights[0]  = 0.004153;
  samples[1]  = "qcdht0700_2017";                 weights[1]  = 5.87992;
  samples[2]  = "qcdht1000_2017";                 weights[2]  = 3.01370;
  samples[3]  = "qcdht1500_2017";                 weights[3]  = 0.44013;
  samples[4]  = "qcdht2000_2017";                 weights[4]  = 0.19212;
  samples[5]  = "ttbar_2017";                     weights[5]  = 0.22485;
  samples[6]  = "qcdht0700_2018";                 weights[6]  = 1;
  samples[7]  = "qcdht1000_2018";                 weights[7]  = 1;
  samples[8]  = "qcdht1500_2018";                 weights[8]  = 1;
  samples[9]  = "qcdht2000_2018";                 weights[9]  = 1;
  samples[10] = "ttbar_2018";                     weights[10] = 1;
  samples[11] = "mfv_neu_tau001000um_M0800_2018"; weights[11] = 1;
  samples[12] = "JetHT2017B";                     weights[12] = 1;
  samples[13] = "JetHT2017C";                     weights[13] = 1;
  samples[14] = "JetHT2017D";                     weights[14] = 1;
  samples[15] = "JetHT2017E";                     weights[15] = 1;
  samples[16] = "JetHT2017F";                     weights[16] = 1;
  samples[17] = "JetHT2018";                      weights[17] = 1;

  int ibkg_begin; int ibkg_end;
  if (p.is_mc()) {
    if (p.year() == "2017")         { ibkg_begin =  1; ibkg_end =  5; if (p.inject_signal()) ibkg_begin = 0; }
    else if (p.year() == "2018")    { ibkg_begin =  6; ibkg_end = 10; if (p.inject_signal()) ibkg_end = 11; }
    else if (p.year() == "2017p8")  { ibkg_begin =  1; ibkg_end = 10; if (p.inject_signal()) {ibkg_begin = 0; ibkg_end = 11;} }
    else { fprintf(stderr, "bad year"); exit(1); }
  } else {
    if (p.year() == "2017")         { ibkg_begin = 12; ibkg_end = 16; }
    else if (p.year() == "2018")    { ibkg_begin = 17; ibkg_end = 17; }
    else if (p.year() == "2017p8")  { ibkg_begin = 12; ibkg_end = 17; }
    else if (p.year() == "2017B")   { ibkg_begin = 12; ibkg_end = 12; }
    else if (p.year() == "2017C")   { ibkg_begin = 13; ibkg_end = 13; }
    else if (p.year() == "2017D")   { ibkg_begin = 14; ibkg_end = 14; }
    else if (p.year() == "2017E")   { ibkg_begin = 15; ibkg_end = 15; }
    else if (p.year() == "2017F")   { ibkg_begin = 16; ibkg_end = 16; }
    else { fprintf(stderr, "bad year"); exit(1); }
  }

  const char* tree_path; int min_ntracks0 = 0; int max_ntracks0 = 1000000; int min_ntracks1 = 0; int max_ntracks1 = 1000000; //which ntracks?
  if (p.ntracks() == 3)      { tree_path = "mfvMiniTreeNtk3/t"; }
  else if (p.ntracks() == 4) { tree_path = "mfvMiniTreeNtk4/t"; }
  else if (p.ntracks() == 5) { tree_path = "mfvMiniTree/t"; }
  else if (p.ntracks() == 7) { tree_path = "mfvMiniTreeNtk3or4/t"; min_ntracks0 = 4; max_ntracks0 = 4; min_ntracks1 = 3; max_ntracks1 = 3; }
  else { fprintf(stderr, "bad ntracks"); exit(1); }

  double dphi_pdf_c; double dphi_pdf_e = 2; double dphi_pdf_a; //deltaphi input
  if (p.is_mc()) {
    if (p.year() == "2017")         { dphi_pdf_c = 1.29; dphi_pdf_a = 4.84; }
    else if (p.year() == "2018")    { dphi_pdf_c = 1.29; dphi_pdf_a = 4.84; }
    else if (p.year() == "2017p8")  { dphi_pdf_c = 1.29; dphi_pdf_a = 4.84; }
    else { fprintf(stderr, "bad year"); exit(1); }
  } else if (p.only_10pc()) {
    if (p.year() == "2017")         { dphi_pdf_c = 1.29; dphi_pdf_a = 4.84; }
    else if (p.year() == "2018")    { dphi_pdf_c = 1.29; dphi_pdf_a = 4.84; }
    else if (p.year() == "2017p8")  { dphi_pdf_c = 1.29; dphi_pdf_a = 4.84; }
    else if (p.year() == "2017B")   { dphi_pdf_c = 1.29; dphi_pdf_a = 4.84; }
    else if (p.year() == "2017C")   { dphi_pdf_c = 1.29; dphi_pdf_a = 4.84; }
    else if (p.year() == "2017D")   { dphi_pdf_c = 1.29; dphi_pdf_a = 4.84; }
    else if (p.year() == "2017E")   { dphi_pdf_c = 1.29; dphi_pdf_a = 4.84; }
    else if (p.year() == "2017F")   { dphi_pdf_c = 1.29; dphi_pdf_a = 4.84; }
    else { fprintf(stderr, "bad year"); exit(1); }
  } else {
    if (p.year() == "2017p8")       { dphi_pdf_c = 1.29; dphi_pdf_a = 4.84; }
    else { fprintf(stderr, "bad year"); exit(1); }
  }

  const char* vpeffs_version; //efficiency input
  if (p.only_10pc()) {
    vpeffs_version = "v20m";
  } else {
    vpeffs_version = "v20m";
  }
  TString eff_file_name = TString::Format("vpeffs%s_%s_%s%s.root", p.is_mc() ? "" : "_data", p.year().c_str(), vpeffs_version, p.vary_eff() ? "_ntkseeds" : "");

  const char* eff_hist = "maxtk3";
  if (p.vary_eff()) {
    if (p.ntracks() == 3)      { eff_hist = "maxtk3"; }
    else if (p.ntracks() == 4) { eff_hist = "maxtk4"; }
    else if (p.ntracks() == 5) { eff_hist = "maxtk5"; }
    else if (p.ntracks() == 7) { eff_hist = "maxtk3"; }
  }

  double bquark_correction[3] = {1,1,1}; //bquark input
  if (p.ntracks() == 3) {
    if (p.year() == "2018")        { bquark_correction[0] = 0.93; bquark_correction[1] = 1.07; bquark_correction[2] = 1.10; }
    else if (p.year() == "2017p8") { bquark_correction[0] = 0.93; bquark_correction[1] = 1.07; bquark_correction[2] = 1.10; }
    else                           { bquark_correction[0] = 0.93; bquark_correction[1] = 1.07; bquark_correction[2] = 1.10; }
  } else if (p.ntracks() == 4) {
    if (p.year() == "2018")        { bquark_correction[0] = 0.93; bquark_correction[1] = 1.11; bquark_correction[2] = 1.20; }
    else if (p.year() == "2017p8") { bquark_correction[0] = 0.93; bquark_correction[1] = 1.11; bquark_correction[2] = 1.20; }
    else                           { bquark_correction[0] = 0.93; bquark_correction[1] = 1.11; bquark_correction[2] = 1.20; }
  } else if (p.ntracks() == 5) {
    if (p.year() == "2018")        { bquark_correction[0] = 0.92; bquark_correction[1] = 1.25; bquark_correction[2] = 1.57; }
    else if (p.year() == "2017p8") { bquark_correction[0] = 0.92; bquark_correction[1] = 1.25; bquark_correction[2] = 1.57; }
    else                           { bquark_correction[0] = 0.92; bquark_correction[1] = 1.25; bquark_correction[2] = 1.57; }
  } else if (p.ntracks() == 7) {
    if (p.year() == "2018")        { bquark_correction[0] = 0.93; bquark_correction[1] = 1.09; bquark_correction[2] = 1.14; }
    else if (p.year() == "2017p8") { bquark_correction[0] = 0.93; bquark_correction[1] = 1.09; bquark_correction[2] = 1.14; }
    else                           { bquark_correction[0] = 0.93; bquark_correction[1] = 1.09; bquark_correction[2] = 1.14; }
  } else {
    fprintf(stderr, "bad ntracks"); exit(1);
  }

  if (p.vary_bquarks()) {
    if (p.ntracks() == 3) {
      if (p.year() == "2018")        { bquark_correction[0] = 0.87; bquark_correction[1] = 1.14; bquark_correction[2] = 1.18; }
      else if (p.year() == "2017p8") { bquark_correction[0] = 0.87; bquark_correction[1] = 1.14; bquark_correction[2] = 1.18; }
      else                           { bquark_correction[0] = 0.87; bquark_correction[1] = 1.14; bquark_correction[2] = 1.18; }
    } else if (p.ntracks() == 4) {
      if (p.year() == "2018")        { bquark_correction[0] = 0.87; bquark_correction[1] = 1.21; bquark_correction[2] = 1.35; }
      else if (p.year() == "2017p8") { bquark_correction[0] = 0.87; bquark_correction[1] = 1.21; bquark_correction[2] = 1.35; }
      else                           { bquark_correction[0] = 0.87; bquark_correction[1] = 1.21; bquark_correction[2] = 1.35; }
    } else if (p.ntracks() == 5) {
      if (p.year() == "2018")        { bquark_correction[0] = 0.86; bquark_correction[1] = 1.43; bquark_correction[2] = 1.95; }
      else if (p.year() == "2017p8") { bquark_correction[0] = 0.86; bquark_correction[1] = 1.43; bquark_correction[2] = 1.95; }
      else                           { bquark_correction[0] = 0.86; bquark_correction[1] = 1.43; bquark_correction[2] = 1.95; }
    } else if (p.ntracks() == 7) {
      if (p.year() == "2018")        { bquark_correction[0] = 0.87; bquark_correction[1] = 1.17; bquark_correction[2] = 1.24; }
      else if (p.year() == "2017p8") { bquark_correction[0] = 0.87; bquark_correction[1] = 1.17; bquark_correction[2] = 1.24; }
      else                           { bquark_correction[0] = 0.87; bquark_correction[1] = 1.17; bquark_correction[2] = 1.24; }
    } else {
      fprintf(stderr, "bad ntracks"); exit(1);
    }
  }

  if (!p.correct_bquarks()) {
    bquark_correction[0] = 1; bquark_correction[1] = 1; bquark_correction[2] = 1;
  }

  printf("\tdphi_pdf_c = %.2f, dphi_pdf_e = %.2f, dphi_pdf_a = %.2f, eff_file_name = %s, eff_hist = %s, bquark_correction = {%.2f, %.2f, %.2f}\n", dphi_pdf_c, dphi_pdf_e, dphi_pdf_a, eff_file_name.Data(), eff_hist, bquark_correction[0], bquark_correction[1], bquark_correction[2]);

  TH1::SetDefaultSumw2();
  gRandom->SetSeed(12191982);

  //fill only-one-vertex dBV distribution
  TH1D* h_1v_dbv = new TH1D("h_1v_dbv", "only-one-vertex events;d_{BV} (cm);events", 1250, 0, 2.5);
  TH1D* h_1v_dbv0 = new TH1D("h_1v_dbv0", "only-one-vertex events;d_{BV}^{0} (cm);events", 1250, 0, 2.5);
  TH1D* h_1v_dbv1 = new TH1D("h_1v_dbv1", "only-one-vertex events;d_{BV}^{1} (cm);events", 1250, 0, 2.5);
  TH1F* h_1v_phiv = new TH1F("h_1v_phiv", "only-one-vertex events;vertex #phi;events", 50, -3.15, 3.15);
  TH1D* h_1v_npu = new TH1D("h_1v_npu", "only-one-vertex events;# PU interactions;events", 100, 0, 100);
  TH1F* h_1v_njets = new TH1F("h_1v_njets", "only-one-vertex events;number of jets;events", 20, 0, 20);
  TH1F* h_1v_ht = new TH1F("h_1v_ht", "only-one-vertex events;#Sigma H_{T} of jets (GeV);events", 200, 0, 5000);
  TH1F* h_1v_phij = new TH1F("h_1v_phij", "only-one-vertex events;jets #phi;jets", 50, -3.15, 3.15);
  TH1F* h_1v_dphijj = new TH1F("h_1v_dphijj", "only-one-vertex events;#Delta#phi_{JJ};jet pairs", 100, -3.1416, 3.1416);
  TH1F* h_1v_dphijv = new TH1F("h_1v_dphijv", "only-one-vertex events;#Delta#phi_{JV};jet-vertex pairs", 100, -3.1416, 3.1416);
  TH1F* h_1v_dphijvpt = new TH1F("h_1v_dphijvpt", "only-one-vertex events;p_{T}-weighted #Delta#phi_{JV};jet-vertex pairs", 100, -3.1416, 3.1416);
  TH1F* h_1v_dphijvmin = new TH1F("h_1v_dphijvmin", "only-one-vertex events;#Delta#phi_{JV}^{min};events", 50, 0, 3.1416);
  TH1F* h_2v_dbv = new TH1F("h_2v_dbv", "two-vertex events;d_{BV} (cm);vertices", 1250, 0, 2.5);
  TH2F* h_2v_dbv1_dbv0 = new TH2F("h_2v_dbv1_dbv0", "two-vertex events;d_{BV}^{0} (cm);d_{BV}^{1} (cm)", 1250, 0, 2.5, 1250, 0, 2.5);
  TH1F* h_2v_dvv = new TH1F("h_2v_dvv", "two-vertex events;d_{VV} (cm);events", dvv_nbins, 0, dvv_nbins * dvv_bin_width);
  TH1F* h_2v_dphivv = new TH1F("h_2v_dphivv", "two-vertex events;#Delta#phi_{VV};events", 10, -3.15, 3.15);
  TH1F* h_2v_absdphivv = new TH1F("h_2v_absdphivv", "two-vertex events;|#Delta#phi_{VV}|;events", 5, 0, 3.15);
  TH1D* h_2v_npu = new TH1D("h_2v_npu", "two-vertex events;# PU interactions;events", 100, 0, 100);

  for (int i = ibkg_begin; i <= ibkg_end; ++i) {
    mfv::MiniNtuple nt;
    TFile* f = TFile::Open(TString::Format("%s/%s.root", file_path, samples[i]));
    if (!f || !f->IsOpen()) { fprintf(stderr, "bad file"); exit(1); }

    TTree* t = (TTree*)f->Get(tree_path);
    if (!t) { fprintf(stderr, "bad tree"); exit(1); }

    mfv::read_from_tree(t, nt);
    for (int j = 0, je = t->GetEntries(); j < je; ++j) {
      if (t->LoadTree(j) < 0) break;
      if (t->GetEntry(j) <= 0) continue;

      if ((p.bquarks() == 0 && nt.gen_flavor_code == 2) || (p.bquarks() == 1 && nt.gen_flavor_code != 2)) continue;
      if (nt.npu < p.min_npu() || nt.npu > p.max_npu()) continue;

      const float w = weights[i] * nt.weight;
      if (nt.nvtx == 1) {
        h_1v_dbv->Fill(sqrt(nt.x0*nt.x0 + nt.y0*nt.y0), w);
        if (nt.ntk0 >= min_ntracks0 && nt.ntk0 <= max_ntracks0) h_1v_dbv0->Fill(sqrt(nt.x0*nt.x0 + nt.y0*nt.y0), w);
        if (nt.ntk0 >= min_ntracks1 && nt.ntk0 <= max_ntracks1) h_1v_dbv1->Fill(sqrt(nt.x0*nt.x0 + nt.y0*nt.y0), w);
        h_1v_phiv->Fill(atan2(nt.y0,nt.x0), w);
        h_1v_npu->Fill(nt.npu, w);
        h_1v_njets->Fill(nt.njets, w);
        h_1v_ht->Fill(ht(nt.njets, nt.jet_pt), w);
        double dphijvmin = M_PI;
        for (int k = 0; k < nt.njets; ++k) {
          h_1v_phij->Fill(nt.jet_phi[k], w);
          h_1v_dphijv->Fill(TVector2::Phi_mpi_pi(atan2(nt.y0,nt.x0) - nt.jet_phi[k]), w);
          h_1v_dphijvpt->Fill(TVector2::Phi_mpi_pi(atan2(nt.y0,nt.x0) - nt.jet_phi[k]), w * (nt.jet_pt[k]/ht(nt.njets, nt.jet_pt)));
          if (fabs(TVector2::Phi_mpi_pi(atan2(nt.y0,nt.x0) - nt.jet_phi[k])) < dphijvmin) dphijvmin = fabs(TVector2::Phi_mpi_pi(atan2(nt.y0,nt.x0) - nt.jet_phi[k]));
          for (int l = k+1; l < nt.njets; ++l) {
            h_1v_dphijj->Fill(TVector2::Phi_mpi_pi(nt.jet_phi[k] - nt.jet_phi[l]), w);
          }
        }
        h_1v_dphijvmin->Fill(dphijvmin, w);
      }

      if (nt.nvtx >= 2 && nt.ntk0 >= min_ntracks0 && nt.ntk0 <= max_ntracks0 && nt.ntk1 >= min_ntracks1 && nt.ntk1 <= max_ntracks1) {
        double dbv0 = sqrt(nt.x0*nt.x0 + nt.y0*nt.y0);
        double dbv1 = sqrt(nt.x1*nt.x1 + nt.y1*nt.y1);
        h_2v_dbv->Fill(dbv0, w);
        h_2v_dbv->Fill(dbv1, w);
        h_2v_dbv1_dbv0->Fill(dbv0, dbv1, w);
        double dvv = sqrt((nt.x0-nt.x1)*(nt.x0-nt.x1) + (nt.y0-nt.y1)*(nt.y0-nt.y1));
        if (dvv > dvv_nbins * dvv_bin_width - 0.5*dvv_bin_width) dvv = dvv_nbins * dvv_bin_width - 0.5*dvv_bin_width;
        h_2v_dvv->Fill(dvv, w);
        double dphi = TVector2::Phi_mpi_pi(atan2(nt.y0,nt.x0)-atan2(nt.y1,nt.x1));
        h_2v_dphivv->Fill(dphi, w);
        h_2v_absdphivv->Fill(fabs(dphi), w);
        h_2v_npu->Fill(nt.npu, w);
      }
    }

    f->Close();
    delete f;
  }

  //construct dvvc
  TH1F* h_c1v_dbv = new TH1F("h_c1v_dbv", "constructed from only-one-vertex events;d_{BV} (cm);vertices", 1250, 0, 2.5);
  TH1F* h_c1v_dvv = new TH1F("h_c1v_dvv", "constructed from only-one-vertex events;d_{VV} (cm);events", dvv_nbins, 0, dvv_nbins * dvv_bin_width);
  TH1F* h_c1v_absdphivv = new TH1F("h_c1v_absdphivv", "constructed from only-one-vertex events;|#Delta#phi_{VV}|;events", 5, 0, 3.15);
  TH1F* h_c1v_dbv0 = new TH1F("h_c1v_dbv0", "constructed from only-one-vertex events;d_{BV}^{0} (cm);events", 1250, 0, 2.5);
  TH1F* h_c1v_dbv1 = new TH1F("h_c1v_dbv1", "constructed from only-one-vertex events;d_{BV}^{1} (cm);events", 1250, 0, 2.5);
  TH2F* h_c1v_dbv1_dbv0 = new TH2F("h_c1v_dbv1_dbv0", "constructed from only-one-vertex events;d_{BV}^{0} (cm);d_{BV}^{1} (cm)", 1250, 0, 2.5, 1250, 0, 2.5);

  TF1* f_dphi = new TF1("f_dphi", "(abs(x)-[0])**[1] + [2]", 0, M_PI);
  f_dphi->SetParameters(dphi_pdf_c, dphi_pdf_e, dphi_pdf_a);

  TF1* i_dphi = 0;
  TF1* i_dphi2 = 0;
  if (p.vary_dphi()) {
    i_dphi = new TF1("i_dphi", "((1/([1]+1))*(x-[0])**([1]+1) + [2]*x - (1/([1]+1))*(-[0])**([1]+1)) / ((1/([1]+1))*(3.14159-[0])**([1]+1) + [2]*3.14159 - (1/([1]+1))*(-[0])**([1]+1))", 0, M_PI);
    i_dphi->SetParameters(dphi_pdf_c, dphi_pdf_e, dphi_pdf_a);
    i_dphi2 = new TF1("i_dphi2", "x/3.14159", 0, M_PI);
  }

  TH1F* h_eff = 0;
  if (p.clearing_from_eff()) {
    TFile* eff_file = TFile::Open(eff_file_name);
    if (!eff_file || !eff_file->IsOpen()) { fprintf(stderr, "bad file"); exit(1); }
    h_eff = (TH1F*)eff_file->Get(eff_hist);
    h_eff->SetBinContent(h_eff->GetNbinsX()+1, h_eff->GetBinContent(h_eff->GetNbinsX()));
  }

  int bin1 = 0;
  int bin2 = 0;
  int bin3 = 0;
  int intobin1 = 0;
  int intobin2 = 0;
  int intobin3 = 0;
  int outofbin1 = 0;
  int outofbin2 = 0;
  int outofbin3 = 0;

  for (int i = 0; i < 20; ++i) {
    for (int j = 0; j < int(h_1v_dbv->GetEntries()); ++j) {
      double dbv0 = h_1v_dbv0->GetRandom();
      double dbv1 = h_1v_dbv1->GetRandom();
      h_c1v_dbv->Fill(dbv0);
      h_c1v_dbv->Fill(dbv1);

      double dphi = f_dphi->GetRandom();

      double dvvc = sqrt(dbv0*dbv0 + dbv1*dbv1 - 2*dbv0*dbv1*cos(dphi));

      if (p.vary_dphi()) {
        double dphi2 = i_dphi2->GetX(i_dphi->Eval(dphi), 0, M_PI);
        double dvvc2 = sqrt(dbv0*dbv0 + dbv1*dbv1 - 2*dbv0*dbv1*cos(dphi2));
        if (dvvc < 0.04) ++bin1;
        if (dvvc >= 0.04 && dvvc < 0.07) ++bin2;
        if (dvvc >= 0.07) ++bin3;
        if (!(dvvc < 0.04) && (dvvc2 < 0.04)) ++intobin1;
        if (!(dvvc >= 0.04 && dvvc < 0.07) && (dvvc2 >= 0.04 && dvvc2 < 0.07)) ++intobin2;
        if (!(dvvc >= 0.07) && (dvvc2 >= 0.07)) ++intobin3;
        if ((dvvc < 0.04) && !(dvvc2 < 0.04)) ++outofbin1;
        if ((dvvc >= 0.04 && dvvc < 0.07) && !(dvvc2 >= 0.04 && dvvc2 < 0.07)) ++outofbin2;
        if ((dvvc >= 0.07) && !(dvvc2 >= 0.07)) ++outofbin3;
        dphi = dphi2;
        dvvc = dvvc2;
      }

      double prob = 1;
      if (p.clearing_from_eff()) {
        prob = h_eff->GetBinContent(h_eff->FindBin(dvvc));
      }

      if (dvvc > dvv_nbins * dvv_bin_width - 0.5*dvv_bin_width) dvvc = dvv_nbins * dvv_bin_width - 0.5*dvv_bin_width;
      h_c1v_dvv->Fill(dvvc, prob);
      h_c1v_absdphivv->Fill(fabs(dphi), prob);
      h_c1v_dbv0->Fill(dbv0, prob);
      h_c1v_dbv1->Fill(dbv1, prob);
      h_c1v_dbv1_dbv0->Fill(dbv0, dbv1, prob);
    }
  }

  for (int i = 1; i <= h_c1v_dvv->GetNbinsX(); ++i) {
    if (h_c1v_dvv->GetBinLowEdge(i) < 0.04) {
      h_c1v_dvv->SetBinContent(i, h_c1v_dvv->GetBinContent(i) * bquark_correction[0]);
    } else if (h_c1v_dvv->GetBinLowEdge(i) < 0.07) {
      h_c1v_dvv->SetBinContent(i, h_c1v_dvv->GetBinContent(i) * bquark_correction[1]);
    } else {
      h_c1v_dvv->SetBinContent(i, h_c1v_dvv->GetBinContent(i) * bquark_correction[2]);
    }
  }

  if (p.vary_dphi()) {
    printf("bin1 = %d, bin2 = %d, bin3 = %d, intobin1 = %d, intobin2 = %d, intobin3 = %d, outofbin1 = %d, outofbin2 = %d, outofbin3 = %d\n", bin1, bin2, bin3, intobin1, intobin2, intobin3, outofbin1, outofbin2, outofbin3);
    printf("uncorrelated variation / default (bin 1): %f +/- %f\n", 1 + (intobin1 - outofbin1) / (1.*bin1), sqrt(bin1 + bin1 + intobin1 - outofbin1) / bin1);
    printf("  correlated variation / default (bin 1): %f +/- %f\n", 1 + (intobin1 - outofbin1) / (1.*bin1), sqrt(intobin1 + outofbin1) / bin1);
    printf("uncertainty correlated / uncorrelated (bin 1): %f\n", sqrt(intobin1 + outofbin1) / sqrt(bin1 + bin1 + intobin1 - outofbin1));
    printf("uncorrelated variation / default (bin 2): %f +/- %f\n", 1 + (intobin2 - outofbin2) / (1.*bin2), sqrt(bin2 + bin2 + intobin2 - outofbin2) / bin2);
    printf("  correlated variation / default (bin 2): %f +/- %f\n", 1 + (intobin2 - outofbin2) / (1.*bin2), sqrt(intobin2 + outofbin2) / bin2);
    printf("uncertainty correlated / uncorrelated (bin 2): %f\n", sqrt(intobin2 + outofbin2) / sqrt(bin2 + bin2 + intobin2 - outofbin2));
    printf("uncorrelated variation / default (bin 3): %f +/- %f\n", 1 + (intobin3 - outofbin3) / (1.*bin3), sqrt(bin3 + bin3 + intobin3 - outofbin3) / bin3);
    printf("  correlated variation / default (bin 3): %f +/- %f\n", 1 + (intobin3 - outofbin3) / (1.*bin3), sqrt(intobin3 + outofbin3) / bin3);
    printf("uncertainty correlated / uncorrelated (bin 3): %f\n", sqrt(intobin3 + outofbin3) / sqrt(bin3 + bin3 + intobin3 - outofbin3));
  }

  TFile* fh = TFile::Open(out_fn, "recreate");

  h_1v_dbv->Write();
  h_1v_dbv0->Write();
  h_1v_dbv1->Write();
  h_1v_phiv->Write();
  h_1v_npu->Write();
  h_1v_njets->Write();
  h_1v_ht->Write();
  h_1v_phij->Write();
  h_1v_dphijj->Write();
  h_1v_dphijv->Write();
  h_1v_dphijvpt->Write();
  h_1v_dphijvmin->Write();
  h_2v_dbv->Write();
  h_2v_dbv1_dbv0->Write();
  h_2v_dvv->Write();
  h_2v_dphivv->Write();
  h_2v_absdphivv->Write();
  h_2v_npu->Write();

  h_c1v_dbv->Write();
  h_c1v_dvv->Scale(1./h_c1v_dvv->Integral());
  h_c1v_dvv->Write();
  h_c1v_absdphivv->Write();
  h_c1v_dbv0->Write();
  h_c1v_dbv1->Write();
  h_c1v_dbv1_dbv0->Write();

  TCanvas* c_dvv = new TCanvas("c_dvv", "c_dvv", 700, 700);
  TLegend* l_dvv = new TLegend(0.35,0.75,0.85,0.85);
  h_2v_dvv->SetTitle(";d_{VV} (cm);events");
  h_2v_dvv->SetLineColor(kBlue);
  h_2v_dvv->SetLineWidth(3);
  h_2v_dvv->Scale(1./h_2v_dvv->Integral());
  h_2v_dvv->SetStats(0);
  h_2v_dvv->Draw();
  l_dvv->AddEntry(h_2v_dvv, "two-vertex events");
  h_c1v_dvv->SetLineColor(kRed);
  h_c1v_dvv->SetLineWidth(3);
  h_c1v_dvv->Scale(1./h_c1v_dvv->Integral());
  h_c1v_dvv->SetStats(0);
  h_c1v_dvv->Draw("sames");
  l_dvv->AddEntry(h_c1v_dvv, "constructed from only-one-vertex events");
  l_dvv->SetFillColor(0);
  l_dvv->Draw();
  c_dvv->SetTickx();
  c_dvv->SetTicky();
  c_dvv->Write();

  TCanvas* c_absdphivv = new TCanvas("c_absdphivv", "c_absdphivv", 700, 700);
  TLegend* l_absdphivv = new TLegend(0.25,0.75,0.75,0.85);
  h_2v_absdphivv->SetTitle(";|#Delta#phi_{VV}|;events");
  h_2v_absdphivv->SetLineColor(kBlue);
  h_2v_absdphivv->SetLineWidth(3);
  h_2v_absdphivv->Scale(1./h_2v_absdphivv->Integral());
  h_2v_absdphivv->SetStats(0);
  h_2v_absdphivv->Draw();
  l_absdphivv->AddEntry(h_2v_absdphivv, "two-vertex events");
  h_c1v_absdphivv->SetLineColor(kRed);
  h_c1v_absdphivv->SetLineWidth(3);
  h_c1v_absdphivv->Scale(1./h_c1v_absdphivv->Integral());
  h_c1v_absdphivv->SetStats(0);
  h_c1v_absdphivv->Draw("sames");
  l_absdphivv->AddEntry(h_c1v_absdphivv, "constructed from only-one-vertex events");
  l_absdphivv->SetFillColor(0);
  l_absdphivv->Draw();
  c_absdphivv->SetTickx();
  c_absdphivv->SetTicky();
  c_absdphivv->Write();

  f_dphi->Write();
  if (p.clearing_from_eff()) {
    h_eff->SetName("h_eff");
    h_eff->Write();
  }
  if (p.vary_dphi()) {
    i_dphi->Write();
    i_dphi2->Write();
  }

  fh->Close();

  delete h_1v_dbv;
  delete h_1v_dbv0;
  delete h_1v_dbv1;
  delete h_1v_phiv;
  delete h_1v_npu;
  delete h_1v_njets;
  delete h_1v_ht;
  delete h_1v_phij;
  delete h_1v_dphijj;
  delete h_1v_dphijv;
  delete h_1v_dphijvpt;
  delete h_1v_dphijvmin;
  delete h_2v_dbv;
  delete h_2v_dbv1_dbv0;
  delete h_2v_dvv;
  delete h_2v_dphivv;
  delete h_2v_absdphivv;
  delete h_2v_npu;
  delete c_dvv;
  delete c_absdphivv;
  delete h_c1v_dbv;
  delete h_c1v_dvv;
  delete h_c1v_absdphivv;
  delete h_c1v_dbv0;
  delete h_c1v_dbv1;
  delete h_c1v_dbv1_dbv0;
}

int main(int argc, const char* argv[]) {
  const bool only_default = strcmp(getenv("USER"), "tucker") == 0 || (argc >= 2 && strcmp(argv[1], "only_default"));
  ConstructDvvcParameters pars;
  if (only_default) {
    construct_dvvc(pars, "2v_from_jets_2017_5track_default_v20mp2.root");
    return 0;
  }

  construct_dvvc(pars, "2v_from_jets_2017_5track_default_v20mp2.root");
/*
  for (const char* year : {"2017", "2018", "2017p8"}) {
    for (int ntracks : {3, 4, 5, 7}) {
      ConstructDvvcParameters pars2 = pars.year(year).ntracks(ntracks);
      const char* version = "v20mp2";
      construct_dvvc(pars2.correct_bquarks(false),              TString::Format("2v_from_jets_%s_%dtrack_bquark_uncorrected_%s.root", year, ntracks, version));
      construct_dvvc(pars2.correct_bquarks(false).bquarks(1),   TString::Format("2v_from_jets_%s_%dtrack_bquarks_%s.root", year, ntracks, version));
      construct_dvvc(pars2.correct_bquarks(false).bquarks(0),   TString::Format("2v_from_jets_%s_%dtrack_nobquarks_%s.root", year, ntracks, version));
      construct_dvvc(pars2,                                     TString::Format("2v_from_jets_%s_%dtrack_default_%s.root", year, ntracks, version));
      construct_dvvc(pars2.vary_dphi(true),                     TString::Format("2v_from_jets_%s_%dtrack_vary_dphi_%s.root", year, ntracks, version));
      construct_dvvc(pars2.clearing_from_eff(false),            TString::Format("2v_from_jets_%s_%dtrack_noclearing_%s.root", year, ntracks, version));
      construct_dvvc(pars2.vary_eff(true),                      TString::Format("2v_from_jets_%s_%dtrack_vary_eff_%s.root", year, ntracks, version));
      construct_dvvc(pars2.vary_bquarks(true),                  TString::Format("2v_from_jets_%s_%dtrack_vary_bquarks_%s.root", year, ntracks, version));
    }
  }
  for (const char* year : {"2017", "2018", "2017p8", "2017B", "2017C", "2017D", "2017E", "2017F"}) {
    for (int ntracks : {3, 4, 5, 7}) {
      ConstructDvvcParameters pars2 = pars.year(year).ntracks(ntracks).is_mc(false).only_10pc(true);
      const char* version = "v20mp2";
      //construct_dvvc(pars2,                    TString::Format("2v_from_jets_data_%s_%dtrack_default_%s.root", year, ntracks, version));
      //construct_dvvc(pars2.vary_dphi(true),    TString::Format("2v_from_jets_data_%s_%dtrack_vary_dphi_%s.root", year, ntracks, version));
      //construct_dvvc(pars2.vary_eff(true),     TString::Format("2v_from_jets_data_%s_%dtrack_vary_eff_%s.root", year, ntracks, version));
      //construct_dvvc(pars2.vary_bquarks(true), TString::Format("2v_from_jets_data_%s_%dtrack_vary_bquarks_%s.root", year, ntracks, version));
    }
  }
  for (const char* year : {"2017p8"}) {
    for (int ntracks : {3, 4, 5, 7}) {
      ConstructDvvcParameters pars2 = pars.year(year).ntracks(ntracks).is_mc(false);
      const char* version = "v20mp2";
      construct_dvvc(pars2,                    TString::Format("2v_from_jets_data_%s_%dtrack_default_%s.root", year, ntracks, version));
      construct_dvvc(pars2.vary_dphi(true),    TString::Format("2v_from_jets_data_%s_%dtrack_vary_dphi_%s.root", year, ntracks, version));
      //construct_dvvc(pars2.clearing_from_eff(false), TString::Format("2v_from_jets_data_%s_%dtrack_noclearing_%s.root", year, ntracks, version));
      construct_dvvc(pars2.vary_eff(true),     TString::Format("2v_from_jets_data_%s_%dtrack_vary_eff_%s.root", year, ntracks, version));
      construct_dvvc(pars2.vary_bquarks(true), TString::Format("2v_from_jets_data_%s_%dtrack_vary_bquarks_%s.root", year, ntracks, version));
    }
  }
*/
}
