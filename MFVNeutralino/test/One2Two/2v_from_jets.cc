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
 *  - For the 2017 MC samples the weights calculated assume an integrated luminosity of 41.53 fb^-1 and the number of events run on for each sample:
samples -i <<EOF
for sample in qcd_samples_2017 + ttbar_samples_2017:
    nevents = sample.nevents('/uscms_data/d2/tucker/crab_dirs/MiniTreeV22m/%s.root' % sample.name)
    print '%20s %6.1f %9d %10.3g' % (sample.name, sample.xsec, nevents, 41530.*sample.xsec/nevents)
EOF
 *  - For the background template only the relative weights are relevant because we only construct the shape; the normalization comes from the fit.
 *  - Todo: MC weights and data samples for 2018.
 *  - If the samples array is modified, ibkg_begin and ibkg_end should also be modified.
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
#include "TRatioPlot.h"
#include "TStyle.h"
#include "TTree.h"
#include "TVector2.h"
#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"

int dvv_nbins = 40;
double dvv_bin_width = 0.01;
std::vector<TString> cb_cbbar_vector = {};

struct ConstructDvvcParameters {
  int ibkg_begin_;
  int ibkg_end_;
  bool is_mc_;
  bool only_10pc_;
  bool inject_signal_;
  std::string year_;
  int ntracks_;
  bool correct_bquarks_;
  int bquarks_;
  int btags_;
  bool vary_dphi_;
  bool clearing_from_eff_;
  bool vary_eff_;
  bool vary_bquarks_;
  int min_npu_;
  int max_npu_;

  ConstructDvvcParameters()
    : ibkg_begin_(-999),
      ibkg_end_(-999),
      is_mc_(true),
      only_10pc_(false),
      inject_signal_(false),
      year_("2017"),
      ntracks_(5),
      correct_bquarks_(true),
      bquarks_(-1),
      btags_(-1),
      vary_dphi_(false),
      clearing_from_eff_(true),
      vary_eff_(false),
      vary_bquarks_(false),
      min_npu_(0),
      max_npu_(255)
  {
  }

  int ibkg_begin() const { return ibkg_begin_; }
  int ibkg_end() const { return ibkg_end_; }
  bool is_mc() const { return is_mc_; }
  bool only_10pc() const { return only_10pc_; }
  bool inject_signal() const { return inject_signal_; }
  std::string year() const { return year_; }
  int ntracks() const { return ntracks_; }
  bool correct_bquarks() const { return correct_bquarks_; }
  int bquarks() const { return bquarks_; }
  int btags() const { return btags_; }
  bool vary_dphi() const { return vary_dphi_; }
  bool clearing_from_eff() const { return clearing_from_eff_; }
  bool vary_eff() const { return vary_eff_; }
  bool vary_bquarks() const { return vary_bquarks_; }
  int min_npu() const { return min_npu_; }
  int max_npu() const { return max_npu_; }

  ConstructDvvcParameters ibkg_begin(bool x)        { ConstructDvvcParameters y(*this); y.ibkg_begin_        = x; return y; }
  ConstructDvvcParameters ibkg_end(bool x)          { ConstructDvvcParameters y(*this); y.ibkg_end_          = x; return y; }
  ConstructDvvcParameters is_mc(bool x)             { ConstructDvvcParameters y(*this); y.is_mc_             = x; return y; }
  ConstructDvvcParameters only_10pc(bool x)         { ConstructDvvcParameters y(*this); y.only_10pc_         = x; return y; }
  ConstructDvvcParameters inject_signal(bool x)     { ConstructDvvcParameters y(*this); y.inject_signal_     = x; return y; }
  ConstructDvvcParameters year(std::string x)       { ConstructDvvcParameters y(*this); y.year_              = x; return y; }
  ConstructDvvcParameters ntracks(int x)            { ConstructDvvcParameters y(*this); y.ntracks_           = x; return y; }
  ConstructDvvcParameters correct_bquarks(bool x)   { ConstructDvvcParameters y(*this); y.correct_bquarks_   = x; return y; }
  ConstructDvvcParameters bquarks(int x)            { ConstructDvvcParameters y(*this); y.bquarks_           = x; return y; }
  ConstructDvvcParameters btags(int x)              { ConstructDvvcParameters y(*this); y.btags_             = x; return y; }
  ConstructDvvcParameters vary_dphi(bool x)         { ConstructDvvcParameters y(*this); y.vary_dphi_         = x; return y; }
  ConstructDvvcParameters clearing_from_eff(bool x) { ConstructDvvcParameters y(*this); y.clearing_from_eff_ = x; return y; }
  ConstructDvvcParameters vary_eff(bool x)          { ConstructDvvcParameters y(*this); y.vary_eff_          = x; return y; }
  ConstructDvvcParameters vary_bquarks(bool x)      { ConstructDvvcParameters y(*this); y.vary_bquarks_      = x; return y; }
  ConstructDvvcParameters min_npu(int x)            { ConstructDvvcParameters y(*this); y.min_npu_           = x; return y; }
  ConstructDvvcParameters max_npu(int x)            { ConstructDvvcParameters y(*this); y.max_npu_           = x; return y; }

  void print() const {
    printf("ibkg_begin-end = %d-%d, is_mc = %d, only_10pc = %d, inject_signal = %d, year = %s, ntracks = %d, correct_bquarks = %d, bquarks = %d, btags = %d, vary_dphi = %d, clearing_from_eff = %d, vary_eff = %d, vary_bquarks = %d, min_npu = %d, max_npu = %d", ibkg_begin(), ibkg_end(), is_mc(), only_10pc(), inject_signal(), year_.c_str(), ntracks(), correct_bquarks(), bquarks(), btags(), vary_dphi(), clearing_from_eff(), vary_eff(), vary_bquarks(), min_npu(), max_npu());
  }
};

void construct_dvvc(ConstructDvvcParameters p, const char* out_fn) {
  p.print(); printf(", out_fn = %s\n", out_fn);

  const char* file_path; //which filepath?
  if (p.only_10pc()) {
    file_path = "/uscms_data/d2/tucker/crab_dirs/MiniTreeV25mv3";
  } else {
    file_path = "/uscms_data/d2/tucker/crab_dirs/MiniTreeV25mv3";
  }

  const int nbkg = 27; //which samples?
  const char* samples[nbkg];
  float       weights[nbkg];
  samples[0]  = "mfv_neu_tau001000um_M0800_2017"; weights[0]  = 0.004153;
  samples[1]  = "qcdht0700_2017";                 weights[1]  = 11.1;
  samples[2]  = "qcdht1000_2017";                 weights[2]  = 5.39;
  samples[3]  = "qcdht1500_2017";                 weights[3]  = 0.709;
  samples[4]  = "qcdht2000_2017";                 weights[4]  = 0.282;
  samples[5]  = "ttbarht0600_2017";               weights[5]  = 0.00185;
  samples[6]  = "ttbarht0800_2017";               weights[6]  = 0.00156;
  samples[7]  = "ttbarht1200_2017";               weights[7]  = 0.000829;
  samples[8]  = "ttbarht2500_2017";               weights[8]  = 2.27e-05;
  samples[9]  = "qcdht0700_2018";                 weights[9]  = 17.5;
  samples[10] = "qcdht1000_2018";                 weights[10] = 8.76;
  samples[11] = "qcdht1500_2018";                 weights[11] = 1.08;
  samples[12] = "qcdht2000_2018";                 weights[12] = 0.44;
  samples[13] = "ttbarht0600_2018";               weights[13] = 0.0153;
  samples[14] = "ttbarht0800_2018";               weights[14] = 0.00866;
  samples[15] = "ttbarht1200_2018";               weights[15] = 0.00564;
  samples[16] = "ttbarht2500_2018";               weights[16] = 0.000116;
  samples[17] = "mfv_neu_tau001000um_M0800_2018"; weights[17] = 1; // FIXME but irrelevant other than for signal contamination
  samples[18] = "JetHT2017B";                     weights[18] = 1;
  samples[19] = "JetHT2017C";                     weights[19] = 1;
  samples[20] = "JetHT2017D";                     weights[20] = 1;
  samples[21] = "JetHT2017E";                     weights[21] = 1;
  samples[22] = "JetHT2017F";                     weights[22] = 1;
  samples[23] = "JetHT2018A";                     weights[23] = 1;
  samples[24] = "JetHT2018B";                     weights[24] = 1;
  samples[25] = "JetHT2018C";                     weights[25] = 1;
  samples[26] = "JetHT2018D";                     weights[26] = 1;

  int ibkg_begin; int ibkg_end;
  if (p.is_mc()) {
    if (p.year() == "2017")         { ibkg_begin =  1; ibkg_end =  8; if (p.inject_signal()) ibkg_begin = 0; }
    else if (p.year() == "2018")    { ibkg_begin =  9; ibkg_end = 16; if (p.inject_signal()) ibkg_end = 17; }
    else if (p.year() == "2017p8")  { ibkg_begin =  1; ibkg_end = 16; if (p.inject_signal()) {ibkg_begin = 0; ibkg_end = 17;} }
    else { fprintf(stderr, "bad year"); exit(1); }
  } else {
    if (p.year() == "2017")         { ibkg_begin = 18; ibkg_end = 22; }
    else if (p.year() == "2018")    { ibkg_begin = 23; ibkg_end = 26; }
    else if (p.year() == "2017p8")  { ibkg_begin = 18; ibkg_end = 26; }
    else if (p.year() == "2017B")   { ibkg_begin = 18; ibkg_end = 18; }
    else if (p.year() == "2017C")   { ibkg_begin = 19; ibkg_end = 19; }
    else if (p.year() == "2017D")   { ibkg_begin = 20; ibkg_end = 20; }
    else if (p.year() == "2017E")   { ibkg_begin = 21; ibkg_end = 21; }
    else if (p.year() == "2017F")   { ibkg_begin = 22; ibkg_end = 22; }
    else if (p.year() == "2018A")   { ibkg_begin = 23; ibkg_end = 23; }
    else if (p.year() == "2018B")   { ibkg_begin = 24; ibkg_end = 24; }
    else if (p.year() == "2018C")   { ibkg_begin = 25; ibkg_end = 25; }
    else if (p.year() == "2018D")   { ibkg_begin = 26; ibkg_end = 26; }
    else { fprintf(stderr, "bad year"); exit(1); }
  }

  if (p.ibkg_begin() != -999) ibkg_begin = p.ibkg_begin();
  if (p.ibkg_end() != -999) ibkg_end = p.ibkg_end();

  const char* tree_path; int min_ntracks0 = 0; int max_ntracks0 = 1000000; int min_ntracks1 = 0; int max_ntracks1 = 1000000; //which ntracks?
  if (p.ntracks() == 3)      { tree_path = "mfvMiniTreeNtk3/t"; }
  else if (p.ntracks() == 4) { tree_path = "mfvMiniTreeNtk4/t"; }
  else if (p.ntracks() == 5) { tree_path = "mfvMiniTree/t"; }
  else if (p.ntracks() == 7) { tree_path = "mfvMiniTreeNtk3or4/t"; min_ntracks0 = 4; max_ntracks0 = 4; min_ntracks1 = 3; max_ntracks1 = 3; }
  else { fprintf(stderr, "bad ntracks"); exit(1); }

  double dphi_pdf_c; double dphi_pdf_e = 2; double dphi_pdf_a; //deltaphi input
  if (p.is_mc()) {
    if (p.year() == "2017")         { dphi_pdf_c = 1.40; dphi_pdf_a = 3.63; }
    else if (p.year() == "2018")    { dphi_pdf_c = 1.44; dphi_pdf_a = 3.57; }
    else if (p.year() == "2017p8")  { dphi_pdf_c = 1.42; dphi_pdf_a = 3.60; }
    else { fprintf(stderr, "bad year"); exit(1); }
  } else if (p.only_10pc()) {
    if (p.year() == "2017")         { dphi_pdf_c = 1.38; dphi_pdf_a = 4.89; }
    else if (p.year() == "2018")    { dphi_pdf_c = 1.35; dphi_pdf_a = 4.71; }
    else if (p.year() == "2017p8")  { dphi_pdf_c = 1.37; dphi_pdf_a = 4.80; }
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
    vpeffs_version = "V25m";
  } else {
    vpeffs_version = "V25m";
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
    if (p.year() == "2018")        { bquark_correction[0] = 0.93; bquark_correction[1] = 1.06; bquark_correction[2] = 1.14; }
    else if (p.year() == "2017p8") { bquark_correction[0] = 0.93; bquark_correction[1] = 1.07; bquark_correction[2] = 1.10; }
    else                           { bquark_correction[0] = 0.94; bquark_correction[1] = 1.07; bquark_correction[2] = 1.06; }
  } else if (p.ntracks() == 4) {
    if (p.year() == "2018")        { bquark_correction[0] = 0.96; bquark_correction[1] = 1.05; bquark_correction[2] = 1.05; }
    else if (p.year() == "2017p8") { bquark_correction[0] = 0.95; bquark_correction[1] = 1.07; bquark_correction[2] = 1.08; }
    else                           { bquark_correction[0] = 0.93; bquark_correction[1] = 1.11; bquark_correction[2] = 1.12; }
  } else if (p.ntracks() == 5) {
    if (p.year() == "2018")        { bquark_correction[0] = 0.93; bquark_correction[1] = 1.02; bquark_correction[2] = 1.19; }
    else if (p.year() == "2017p8") { bquark_correction[0] = 0.94; bquark_correction[1] = 1.01; bquark_correction[2] = 1.23; }
    else                           { bquark_correction[0] = 0.97; bquark_correction[1] = 0.99; bquark_correction[2] = 1.24; }
  } else if (p.ntracks() == 7) {
    if (p.year() == "2018")        { bquark_correction[0] = 0.94; bquark_correction[1] = 1.06; bquark_correction[2] = 1.10; }
    else if (p.year() == "2017p8") { bquark_correction[0] = 0.94; bquark_correction[1] = 1.07; bquark_correction[2] = 1.09; }
    else                           { bquark_correction[0] = 0.94; bquark_correction[1] = 1.08; bquark_correction[2] = 1.08; }
  } else {
    fprintf(stderr, "bad ntracks"); exit(1);
  }

  if (p.vary_bquarks()) {
    if (p.ntracks() == 3) {
      if (p.year() == "2018")        { bquark_correction[0] = 0.87; bquark_correction[1] = 1.11; bquark_correction[2] = 1.22; }
      else if (p.year() == "2017p8") { bquark_correction[0] = 0.88; bquark_correction[1] = 1.13; bquark_correction[2] = 1.15; }
      else                           { bquark_correction[0] = 0.89; bquark_correction[1] = 1.13; bquark_correction[2] = 1.11; }
    } else if (p.ntracks() == 4) {
      if (p.year() == "2018")        { bquark_correction[0] = 0.93; bquark_correction[1] = 1.10; bquark_correction[2] = 1.06; }
      else if (p.year() == "2017p8") { bquark_correction[0] = 0.91; bquark_correction[1] = 1.14; bquark_correction[2] = 1.12; }
      else                           { bquark_correction[0] = 0.88; bquark_correction[1] = 1.19; bquark_correction[2] = 1.18; }
    } else if (p.ntracks() == 5) {
      if (p.year() == "2018")        { bquark_correction[0] = 0.81; bquark_correction[1] = 1.06; bquark_correction[2] = 1.40; }
      else if (p.year() == "2017p8") { bquark_correction[0] = 0.88; bquark_correction[1] = 1.03; bquark_correction[2] = 1.47; }
      else                           { bquark_correction[0] = 0.94; bquark_correction[1] = 0.98; bquark_correction[2] = 1.44; }
    } else if (p.ntracks() == 7) {
      if (p.year() == "2018")        { bquark_correction[0] = 0.90; bquark_correction[1] = 1.10; bquark_correction[2] = 1.17; }
      else if (p.year() == "2017p8") { bquark_correction[0] = 0.89; bquark_correction[1] = 1.13; bquark_correction[2] = 1.14; }
      else                           { bquark_correction[0] = 0.88; bquark_correction[1] = 1.15; bquark_correction[2] = 1.13; }
    } else {
      fprintf(stderr, "bad ntracks"); exit(1);
    }
  }

  if (!p.correct_bquarks()) {
    bquark_correction[0] = 1; bquark_correction[1] = 1; bquark_correction[2] = 1;
  }

  printf("\tdphi_pdf_c = %.2f, dphi_pdf_e = %.2f, dphi_pdf_a = %.2f, eff_file_name = %s, eff_hist = %s, bquark_correction = {%.2f, %.2f, %.2f}\n", dphi_pdf_c, dphi_pdf_e, dphi_pdf_a, eff_file_name.Data(), eff_hist, bquark_correction[0], bquark_correction[1], bquark_correction[2]);

  gRandom->SetSeed(12191982);

  //fill only-one-vertex dBV distribution
  TH1D* h_1v_dbv = new TH1D("h_1v_dbv", "only-one-vertex events;d_{BV} (cm);events", 1250, 0, 2.5);
  TH1D* h_1v_dbv0 = new TH1D("h_1v_dbv0", "only-one-vertex events;d_{BV}^{0} (cm);events", 1250, 0, 2.5);
  TH1D* h_1v_dbv1 = new TH1D("h_1v_dbv1", "only-one-vertex events;d_{BV}^{1} (cm);events", 1250, 0, 2.5);
  TH1F* h_1v_phiv = new TH1F("h_1v_phiv", "only-one-vertex events;vertex #phi;events", 50, -3.15, 3.15);
  TH1D* h_1v_npu = new TH1D("h_1v_npu", "only-one-vertex events;# PU interactions;events", 100, 0, 100);
  TH1F* h_1v_njets = new TH1F("h_1v_njets", "only-one-vertex events;number of jets;events", 20, 0, 20);
  TH1F* h_1v_ht40 = new TH1F("h_1v_ht40", "only-one-vertex events;H_{T} of jets with p_{T} > 40 GeV;events", 200, 0, 5000);
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
    TString fn = TString::Format("%s/%s.root", file_path, samples[i]);
    //std::cout << fn.Data() << "\n";
    TFile* f = TFile::Open(fn);
    if (!f || !f->IsOpen()) { fprintf(stderr, "bad file"); exit(1); }

    TTree* t = (TTree*)f->Get(tree_path);
    if (!t) { fprintf(stderr, "bad tree"); exit(1); }

    // Tight WP of DeepJet
    float bdisc_cut_value = 0;

    if (p.year().find("2017p8") != std::string::npos) {
      if ((i >= 1 && i <= 8) || (i >= 18 && i <= 22)) bdisc_cut_value = 0.7489;
      else if ((i >= 9 && i <= 16) || (i >= 23 && i <= 26)) bdisc_cut_value = 0.7264;
      else {
	std::cerr << "Need to handle this! (" << p.year() << ")" << std::endl;
	abort();
      }
    }
    if (p.year().find("2017") != std::string::npos) {
      bdisc_cut_value = 0.7489;
    }
    else if (p.year().find("2018") != std::string::npos) {
      bdisc_cut_value = 0.7264;
    }
    else{
      std::cerr << "Need to handle this! (" << p.year() << ")" << std::endl;
      abort();
    }

    mfv::read_from_tree(t, nt);
    for (int j = 0, je = t->GetEntries(); j < je; ++j) {
      if (t->LoadTree(j) < 0) break;
      if (t->GetEntry(j) <= 0) continue;
      //if (i == 2 && nt.run == 1 && nt.lumi == 11522 && nt.event == 132003224) continue;
      if ((p.bquarks() == 0 && nt.gen_flavor_code == 2) || (p.bquarks() == 1 && nt.gen_flavor_code != 2)) continue;
      if ((p.btags() == 0 && nt.nbtags(bdisc_cut_value) >= 1) || (p.btags() == 1 && nt.nbtags(bdisc_cut_value) < 1)) continue;
      if (nt.npu < p.min_npu() || nt.npu > p.max_npu()) continue;

      const float w = weights[i] * nt.weight;
      if (nt.nvtx == 1) {
        h_1v_dbv->Fill(sqrt(nt.x0*nt.x0 + nt.y0*nt.y0), w);
        if (nt.ntk0 >= min_ntracks0 && nt.ntk0 <= max_ntracks0) h_1v_dbv0->Fill(sqrt(nt.x0*nt.x0 + nt.y0*nt.y0), w);
        if (nt.ntk0 >= min_ntracks1 && nt.ntk0 <= max_ntracks1) h_1v_dbv1->Fill(sqrt(nt.x0*nt.x0 + nt.y0*nt.y0), w);
        h_1v_phiv->Fill(atan2(nt.y0,nt.x0), w);
        h_1v_npu->Fill(nt.npu, w);
        h_1v_njets->Fill(nt.njets, w);
        h_1v_ht40->Fill(nt.ht(40.), w);
        double dphijvmin = M_PI;
        for (int k = 0; k < nt.njets; ++k) {
          h_1v_phij->Fill(nt.jet_phi[k], w);
          h_1v_dphijv->Fill(TVector2::Phi_mpi_pi(atan2(nt.y0,nt.x0) - nt.jet_phi[k]), w);
          h_1v_dphijvpt->Fill(TVector2::Phi_mpi_pi(atan2(nt.y0,nt.x0) - nt.jet_phi[k]), w * (nt.jet_pt[k]/nt.ht(0.)));
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
        //printf("ibkg %i %s 2v event j %i weight %f * %f = %f dbv %f %f dvv %f npu %i\n", i, samples[i], j, weights[i], nt.weight, w, dbv0, dbv1, dvv, nt.npu);
      }
    }

    f->Close();
    delete f;
  }

  // check for negative bins in dbv histograms that we throw from below--JMTBAD set zero, only wrong ~by a little
  for (TH1* h : { h_1v_dbv0, h_1v_dbv1})
    for (int ibin = 0; ibin <= h->GetNbinsX()+1; ++ibin)
      if (h->GetBinContent(ibin) < 0) {
        printf("\e[1;31mdbv histogram %s has negative content %f in bin %i\e[0m\n", h->GetName(), h->GetBinContent(ibin), ibin);
        h->SetBinContent(ibin, 0);
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

  const int nsamples = 20*int(h_1v_dbv->GetEntries());
  printf("sampling %i times (should be %i)\n", nsamples, 20*int(h_1v_dbv->Integral()));
  double events_after_eff = 0;
  for (int ij = 0; ij < nsamples; ++ij) {
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

    events_after_eff += prob;
  }
  printf("events before efficiency correction = %d, events after efficiency correction = %f, integrated efficiency correction = %f\n", nsamples, events_after_eff, events_after_eff/nsamples);

  TString cb_cbbar = TString::Format("%s, %.3f", out_fn, events_after_eff/nsamples);
  cb_cbbar_vector.push_back(cb_cbbar);

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
  h_1v_ht40->Write();
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
  delete h_1v_ht40;
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
  TH1::SetDefaultSumw2();
  gStyle->SetPadTickX(1);
  gStyle->SetPadTickY(1);

  const bool only_default = argc >= 2 && strcmp(argv[1], "only_default") == 0;
  ConstructDvvcParameters pars;
  if (only_default) {
    const char* outfn  = "2v_from_jets.root";
    const char* drawfn = "2v_from_jets.png";
    const int ntracks  = argc >= 3 ? atoi(argv[2]) : 3;
    const char* year  = argc >= 4 ? argv[3] : "2017";
    const int ibkg  = argc >= 5 ? atoi(argv[4]) : -999;

    ConstructDvvcParameters pars2 = pars.year(year).ntracks(ntracks);
    if (ibkg != -999) pars2 = pars2.ibkg_begin(ibkg).ibkg_end(ibkg);
    construct_dvvc(pars2, outfn);
    TCanvas c("c","",700,900);
    TFile* f = TFile::Open(outfn);
    TH1* h_2v_dvv  = (TH1*)f->Get("h_2v_dvv");
    TH1* h_c1v_dvv = (TH1*)f->Get("h_c1v_dvv");
    h_c1v_dvv->Scale(h_2v_dvv->Integral()/h_c1v_dvv->Integral());
    h_c1v_dvv->SetLineColor(kRed);
    h_2v_dvv->SetLineColor(kBlue);
    for (auto h : {h_c1v_dvv, h_2v_dvv}) {
      h->SetTitle(TString::Format("%i-track, 2-vertex events (%s);d_{VV} (cm);events", ntracks, year));
      h->SetLineWidth(2);
      h->SetStats(0);
    }
    TRatioPlot rat(h_2v_dvv, h_c1v_dvv);
    rat.SetH1DrawOpt("e");
    rat.SetH2DrawOpt("hist");
    rat.Draw();
    c.Update();
    rat.GetLowerPad()->SetLogy();
    double minr = 1e99, maxr = 0;
    for (int ibin = 1; ibin <= std::min(10,h_2v_dvv->GetNbinsX()); ++ibin) {
      const double r = h_2v_dvv->GetBinContent(ibin) / h_c1v_dvv->GetBinContent(ibin);
      minr = std::min(minr, r);
      maxr = std::max(maxr, r);
    }
    rat.GetLowerRefYaxis()->SetRangeUser(minr*0.5,maxr*2);
    rat.GetCalculationOutputGraph()->SetLineWidth(2);
    rat.GetCalculationOutputGraph()->SetLineColor(kBlue);
    rat.SetGridlines(std::vector<double>({1.}));

    c.SaveAs(drawfn);
    return 0;
  }

  // production version
  const char* version = "V25m";

  for (const char* year : {"2017p8"}) {
    for (int ntracks : {3, 4, 5, 7}) {
      ConstructDvvcParameters pars2 = pars.year(year).ntracks(ntracks);
      construct_dvvc(pars2.correct_bquarks(false),              TString::Format("2v_from_jets_%s_%dtrack_bquark_uncorrected_%s.root", year, ntracks, version));
      construct_dvvc(pars2.correct_bquarks(false).bquarks(1),   TString::Format("2v_from_jets_%s_%dtrack_bquarks_%s.root", year, ntracks, version));
      construct_dvvc(pars2.correct_bquarks(false).bquarks(0),   TString::Format("2v_from_jets_%s_%dtrack_nobquarks_%s.root", year, ntracks, version));
      construct_dvvc(pars2.correct_bquarks(false).btags(1),     TString::Format("2v_from_jets_%s_%dtrack_btags_%s.root", year, ntracks, version));
      construct_dvvc(pars2.correct_bquarks(false).btags(0),     TString::Format("2v_from_jets_%s_%dtrack_nobtags_%s.root", year, ntracks, version));
      construct_dvvc(pars2,                                     TString::Format("2v_from_jets_%s_%dtrack_default_%s.root", year, ntracks, version));
      construct_dvvc(pars2.vary_dphi(true),                     TString::Format("2v_from_jets_%s_%dtrack_vary_dphi_%s.root", year, ntracks, version));
      construct_dvvc(pars2.clearing_from_eff(false),            TString::Format("2v_from_jets_%s_%dtrack_noclearing_%s.root", year, ntracks, version));
      construct_dvvc(pars2.vary_eff(true),                      TString::Format("2v_from_jets_%s_%dtrack_vary_eff_%s.root", year, ntracks, version));
      construct_dvvc(pars2.vary_bquarks(true),                  TString::Format("2v_from_jets_%s_%dtrack_vary_bquarks_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.min_npu(0).max_npu(27),              TString::Format("2v_from_jets_%s_%dtrack_npu0to27_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.min_npu(28).max_npu(36),             TString::Format("2v_from_jets_%s_%dtrack_npu28to36_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.min_npu(37).max_npu(255),            TString::Format("2v_from_jets_%s_%dtrack_npu37to255_%s.root", year, ntracks, version));
    }
  }

  //for (const char* year : {"2017", "2018", "2017p8", "2017B", "2017C", "2017D", "2017E", "2017F"}) {
  for (const char* year : {"2017p8"}) {
    //for (int ntracks : {3, 4, 5, 7}) {
    for (int ntracks : {3, 4}) {
      ConstructDvvcParameters pars2 = pars.year(year).ntracks(ntracks).is_mc(false).only_10pc(true);
      const char* version = "v25m";
      construct_dvvc(pars2,                    TString::Format("2v_from_jets_data_%s_%dtrack_default_%s.root", year, ntracks, version));
      construct_dvvc(pars2.correct_bquarks(false).btags(1),     TString::Format("2v_from_jets_data_%s_%dtrack_btags_%s.root", year, ntracks, version));
      construct_dvvc(pars2.correct_bquarks(false).btags(0),     TString::Format("2v_from_jets_data_%s_%dtrack_nobtags_%s.root", year, ntracks, version));
      //construct_dvvc(pars2.vary_dphi(true),    TString::Format("2v_from_jets_data_%s_%dtrack_vary_dphi_%s.root", year, ntracks, version));
      //construct_dvvc(pars2.vary_eff(true),     TString::Format("2v_from_jets_data_%s_%dtrack_vary_eff_%s.root", year, ntracks, version));
      //construct_dvvc(pars2.vary_bquarks(true), TString::Format("2v_from_jets_data_%s_%dtrack_vary_bquarks_%s.root", year, ntracks, version));
    }
  }

  // For use in bquark_fraction.py
  std::cout << "\nIntegrated dVVc efficiency correction values:" << std::endl;
  for(TString cb_cbbar : cb_cbbar_vector){
    if(cb_cbbar.Contains("track_bquarks_") || cb_cbbar.Contains("track_nobquarks_") || cb_cbbar.Contains("track_btags_") || cb_cbbar.Contains("track_nobtags_")){

      cb_cbbar.ReplaceAll("2v_from_jets_","");
      cb_cbbar.ReplaceAll((TString)version+".root","");
      if(cb_cbbar.Contains("_bquarks_") || cb_cbbar.Contains("_btags_")){
        cb_cbbar.ReplaceAll(",",", cb    = ");
      }
      if(cb_cbbar.Contains("_nobquarks_") || cb_cbbar.Contains("_nobtags_")){
        cb_cbbar.ReplaceAll(",",", cbbar = ");
      }

      cb_cbbar.ReplaceAll("_nobquarks_"," bquark method");
      cb_cbbar.ReplaceAll("_bquarks_"," bquark method");
      cb_cbbar.ReplaceAll("_nobtags_"," btag   method");
      cb_cbbar.ReplaceAll("_btags_"," btag   method");

      cb_cbbar.ReplaceAll("_"," ");

      std::cout << cb_cbbar << std::endl;
    }
  }

  /*
  for (const char* year : {"2017p8"}) {
    for (int ntracks : {3, 4, 5, 7}) {
      ConstructDvvcParameters pars2 = pars.year(year).ntracks(ntracks).is_mc(false);
      const char* version = "v22m";
      construct_dvvc(pars2,                    TString::Format("2v_from_jets_data_%s_%dtrack_default_%s.root", year, ntracks, version));
      construct_dvvc(pars2.vary_dphi(true),    TString::Format("2v_from_jets_data_%s_%dtrack_vary_dphi_%s.root", year, ntracks, version));
      //construct_dvvc(pars2.clearing_from_eff(false), TString::Format("2v_from_jets_data_%s_%dtrack_noclearing_%s.root", year, ntracks, version));
      construct_dvvc(pars2.vary_eff(true),     TString::Format("2v_from_jets_data_%s_%dtrack_vary_eff_%s.root", year, ntracks, version));
      construct_dvvc(pars2.vary_bquarks(true), TString::Format("2v_from_jets_data_%s_%dtrack_vary_bquarks_%s.root", year, ntracks, version));
    }
  }
*/
}
