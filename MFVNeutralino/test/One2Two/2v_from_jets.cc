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
 */

#include <cstdlib>
#include <math.h>
#include <iostream>
#include <fstream>
#include <vector>
#include "TCanvas.h"
#include "TF1.h"
#include "TFile.h"
#include "TH2F.h"
#include "TH3F.h"
#include "TLegend.h"
#include "TMath.h"
#include "TRandom3.h"
#include "TRatioPlot.h"
#include "TStyle.h"
#include "TTree.h"
#include "TVector2.h"
#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"

int dvv_nbins = 100;
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
  int bquarks_;
  int btags_;
  bool vary_dphi_;
  bool clearing_from_eff_;
  bool vary_eff_;
  int min_npu_;
  int max_npu_;

  ConstructDvvcParameters()
    : ibkg_begin_(-999),
      ibkg_end_(-999),
      is_mc_(true),
      only_10pc_(false),
      inject_signal_(false),
      year_("2017p8"), //2017p8
      ntracks_(5),
      bquarks_(-1),
      btags_(-1),
      vary_dphi_(false),
      clearing_from_eff_(true),
      //clearing_from_eff_(true),
      vary_eff_(false),
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
  int bquarks() const { return bquarks_; }
  int btags() const { return btags_; }
  bool vary_dphi() const { return vary_dphi_; }
  bool clearing_from_eff() const { return clearing_from_eff_; }
  bool vary_eff() const { return vary_eff_; }
  int min_npu() const { return min_npu_; }
  int max_npu() const { return max_npu_; }

  ConstructDvvcParameters ibkg_begin(bool x)        { ConstructDvvcParameters y(*this); y.ibkg_begin_        = x; return y; }
  ConstructDvvcParameters ibkg_end(bool x)          { ConstructDvvcParameters y(*this); y.ibkg_end_          = x; return y; }
  ConstructDvvcParameters is_mc(bool x)             { ConstructDvvcParameters y(*this); y.is_mc_             = x; return y; }
  ConstructDvvcParameters only_10pc(bool x)         { ConstructDvvcParameters y(*this); y.only_10pc_         = x; return y; }
  ConstructDvvcParameters inject_signal(bool x)     { ConstructDvvcParameters y(*this); y.inject_signal_     = x; return y; }
  ConstructDvvcParameters year(std::string x)       { ConstructDvvcParameters y(*this); y.year_              = x; return y; }
  ConstructDvvcParameters ntracks(int x)            { ConstructDvvcParameters y(*this); y.ntracks_           = x; return y; }
  ConstructDvvcParameters bquarks(int x)            { ConstructDvvcParameters y(*this); y.bquarks_           = x; return y; }
  ConstructDvvcParameters btags(int x)              { ConstructDvvcParameters y(*this); y.btags_             = x; return y; }
  ConstructDvvcParameters vary_dphi(bool x)         { ConstructDvvcParameters y(*this); y.vary_dphi_         = x; return y; }
  ConstructDvvcParameters clearing_from_eff(bool x) { ConstructDvvcParameters y(*this); y.clearing_from_eff_ = x; return y; }
  ConstructDvvcParameters vary_eff(bool x)          { ConstructDvvcParameters y(*this); y.vary_eff_          = x; return y; }
  ConstructDvvcParameters min_npu(int x)            { ConstructDvvcParameters y(*this); y.min_npu_           = x; return y; }
  ConstructDvvcParameters max_npu(int x)            { ConstructDvvcParameters y(*this); y.max_npu_           = x; return y; }

  void print() const {
     printf("ibkg_begin-end = %d-%d, is_mc = %d, only_10pc = %d, inject_signal = %d, year = %s, ntracks = %d, bquarks = %d, btags = %d, vary_dphi = %d, clearing_from_eff = %d, vary_eff = %d, min_npu = %d, max_npu = %d", ibkg_begin(), ibkg_end(), is_mc(), only_10pc(), inject_signal(), year_.c_str(), ntracks(), bquarks(), btags(), vary_dphi(), clearing_from_eff(), vary_eff(), min_npu(), max_npu());
  }

  float extra_eff_2d(float dvv) {
    if (dvv < 0.08) return 0.60;
    if (dvv > 0.20) return 0.84;
    else return (0.213 + 6.00*dvv - 14.4*dvv*dvv);
  }

};

void construct_dvvc(ConstructDvvcParameters p, const char* out_fn) {

  p.print(); printf(", out_fn = %s\n", out_fn);

  const char* file_path; //which filepath?
  if (p.is_mc()) {
    //file_path = "/afs/cern.ch/user/p/pekotamn/crabdirs/MiniTree_FixWP_ULV11Bm";
    file_path = "/afs/cern.ch/user/p/pekotamn/crabdirs/MiniTreeOnnormdzULV30Lepm";
  } else if (p.only_10pc()) {
    //file_path = "/uscms_data/d2/tucker/crab_dirs/MiniTreeV27m";
    file_path = "/afs/cern.ch/user/p/pekotamn/crabdirs/MiniTreeOnnormdzULV30Lepm";
  } else {
    file_path = "/uscms_data/d3/dquach/crab3dirs/MiniTreeV27m_moresidebands";
  }

  std::vector<const char*>  samples;
  std::vector<float>  weights;

  std::cout << "The year is: " << p.year() << std::endl;

  bool use_20161 = p.year() == "20161" or p.year() == "20161"   or p.year() == "run2";
  bool use_20162 = p.year() == "20162" or p.year() == "20162"   or p.year() == "run2";
  bool  use_2017 = p.year() == "2017"  or p.year() == "2017p8" or p.year() == "run2";
  bool  use_2018 = p.year() == "2018"  or p.year() == "2017p8" or p.year() == "run2";
  // FIXME these weights are based off of the number of finished ntuples (which is
  // close to, but not necessarily 100% of ntuples). When it comes time to do the
  // final studies, we'll need to make sure ALL ntuples/minitrees finish, and then
  // update some of the weights
  if (false){
       if (p.is_mc()) {
          if (use_20161) {
	    samples.push_back("qcdht0300_20161");    weights.push_back(140.4);
	    samples.push_back("qcdht0500_20161");    weights.push_back(10.5);
	    samples.push_back("qcdht0700_20161");    weights.push_back(3.13);
	    samples.push_back("qcdht1000_20161");    weights.push_back(1.59);
	    samples.push_back("qcdht1500_20161");    weights.push_back(0.21);
	    samples.push_back("qcdht2000_20161");    weights.push_back(0.09);
	    samples.push_back("ttbar_20161");        weights.push_back(0.16);
	  }

	  if (use_20162) {
	    samples.push_back("qcdht0300_20162");       weights.push_back(117.7);
	    samples.push_back("qcdht0500_20162");       weights.push_back(9.74);
	    samples.push_back("qcdht0700_20162");       weights.push_back(2.52);
	    samples.push_back("qcdht1000_20162");       weights.push_back(1.50);
	    samples.push_back("qcdht1500_20162");       weights.push_back(0.20);
	    samples.push_back("qcdht2000_20162");       weights.push_back(0.08);
	    samples.push_back("ttbar_20162");           weights.push_back(0.14);
	  }

	  if (use_2017) {  
	    samples.push_back("qcdht0300_2017");    weights.push_back(242.0);
	    samples.push_back("qcdht0500_2017");    weights.push_back(20.2);
	    samples.push_back("qcdht0700_2017");    weights.push_back(5.46);
	    samples.push_back("qcdht1000_2017");    weights.push_back(3.21);
	    samples.push_back("qcdht1500_2017");    weights.push_back(0.35);
	    samples.push_back("ttbar_2017");        weights.push_back(0.14);
	  }

	  if (use_2018) {  
	    samples.push_back("qcdht0300_2018");    weights.push_back(335.0);
	    samples.push_back("qcdht0500_2018");    weights.push_back(29.3);
	    samples.push_back("qcdht0700_2018");    weights.push_back(8.01);
	    samples.push_back("qcdht1000_2018");    weights.push_back(4.40);
	    samples.push_back("qcdht1500_2018");    weights.push_back(0.54);
	    samples.push_back("qcdht2000_2018");    weights.push_back(0.23);
	    samples.push_back("ttbar_2018");        weights.push_back(0.32); //weights.push_back(0.16);
	  }
       }
       else {
	    if (use_2017) {
	      samples.push_back("JetHT2017B");                      weights.push_back(1);
	      samples.push_back("JetHT2017C");                      weights.push_back(1);
	      samples.push_back("JetHT2017D");                      weights.push_back(1);
	      samples.push_back("JetHT2017E");                      weights.push_back(1);
	      samples.push_back("JetHT2017F");                      weights.push_back(1);
	    }
	    if (use_2018) {  
	      samples.push_back("JetHT2018A");                      weights.push_back(1);
	      samples.push_back("JetHT2018B");                      weights.push_back(1);
	      samples.push_back("JetHT2018C");                      weights.push_back(1);
	      samples.push_back("JetHT2018D");                      weights.push_back(1);
	    }
        }

  }
  else {
	  if (p.is_mc()) {
	    if (use_2017) { 
	        samples.push_back("ttbar_2017");            weights.push_back(0.15);
                samples.push_back("dyjetstollM10_2017");    weights.push_back(15.45);
		samples.push_back("qcdbctoept170_2017");    weights.push_back(5.57);
		samples.push_back("qcdempt120_2017");       weights.push_back(300.25);
		samples.push_back("qcdpt170mupt5_2017");    weights.push_back(6.18);
		samples.push_back("qcdpt600mupt5_2017");    weights.push_back(0.02);
		samples.push_back("ww_2017");               weights.push_back(0.21);
		samples.push_back("dyjetstollM50_2017");    weights.push_back(2.18);
		samples.push_back("qcdbctoept250_2017");    weights.push_back(1.47);
		samples.push_back("qcdempt170_2017");       weights.push_back(183.50);
		samples.push_back("qcdpt20mupt5_2017");     weights.push_back(1827.01);
		samples.push_back("qcdpt800mupt5_2017");    weights.push_back(0.00);
		samples.push_back("wz_2017");               weights.push_back(0.16);
		samples.push_back("qcdbctoept015_2017");    weights.push_back(589.79);
		samples.push_back("qcdempt020_2017");       weights.push_back(14035.33);
		samples.push_back("qcdempt300_2017");       weights.push_back(20.24);
		samples.push_back("qcdpt300mupt5_2017");    weights.push_back(0.43);
		samples.push_back("qcdpt80mupt5_2017");     weights.push_back(84.36);
		samples.push_back("zz_2017");               weights.push_back(0.18);
		samples.push_back("qcdbctoept020_2017");    weights.push_back(1142.48);
		samples.push_back("qcdempt030_2017");       weights.push_back(29803.79);
		samples.push_back("qcdpt1000mupt5_2017");   weights.push_back(0.00);
		samples.push_back("qcdpt30mupt5_2017");     weights.push_back(1347.09);
		samples.push_back("wjetstolnu_0j_2017");    weights.push_back(12.65);
		samples.push_back("qcdbctoept030_2017");    weights.push_back(1058.97);
		samples.push_back("qcdempt050_2017");       weights.push_back(7906.91);
		samples.push_back("qcdpt120mupt5_2017");    weights.push_back(33.29);
		samples.push_back("qcdpt470mupt5_2017");    weights.push_back(0.06);
		samples.push_back("wjetstolnu_1j_2017");    weights.push_back(2.00);
		samples.push_back("qcdbctoept080_2017");    weights.push_back(101.06);
		samples.push_back("qcdempt080_2017");       weights.push_back(4664.42);
		samples.push_back("qcdpt15mupt5_2017");     weights.push_back(18680.12);
		samples.push_back("qcdpt50mupt5_2017");     weights.push_back(412.17);
		samples.push_back("wjetstolnu_2j_2017");    weights.push_back(1.41);
            }
	    if (use_2018) {
		
		samples.push_back("ttbar_2018");    weights.push_back(0.16);
		samples.push_back("qcdmupt15_2018");    weights.push_back(1089.56);
		samples.push_back("qcdempt015_2018");    weights.push_back(13836.45);
		samples.push_back("qcdempt020_2018");    weights.push_back(20392.99);
		samples.push_back("qcdempt030_2018");    weights.push_back(46444.82);
		samples.push_back("qcdempt050_2018");    weights.push_back(11273.78);
		samples.push_back("qcdempt080_2018");    weights.push_back(2316.50);
		samples.push_back("qcdempt120_2018");    weights.push_back(410.66);
		samples.push_back("qcdempt170_2018");    weights.push_back(267.03);
		samples.push_back("qcdbctoept015_2018");    weights.push_back(671.48);
		samples.push_back("qcdbctoept020_2018");    weights.push_back(1709.18);
		samples.push_back("qcdbctoept030_2018");    weights.push_back(1912.59);
		samples.push_back("qcdbctoept080_2018");    weights.push_back(141.47);
		samples.push_back("qcdbctoept170_2018");    weights.push_back(9.93);
		samples.push_back("qcdbctoept250_2018");    weights.push_back(7.42);
		samples.push_back("qcdempt300_2018");    weights.push_back(29.73);
		samples.push_back("wjetstolnu_0j_2018");    weights.push_back(20.75);
		samples.push_back("wjetstolnu_1j_2018");    weights.push_back(4.62);
		samples.push_back("wjetstolnu_2j_2018");    weights.push_back(2.07);
		samples.push_back("dyjetstollM10_2018");    weights.push_back(11.84);
		samples.push_back("dyjetstollM50_2018");    weights.push_back(3.56);
		samples.push_back("ww_2018");    weights.push_back(0.54);
		samples.push_back("wz_2018");    weights.push_back(1.35);
		samples.push_back("zz_2018");    weights.push_back(0.21);

            }  
          }
	  else {
	    if (use_2017) {
	      samples.push_back("SingleElectron2017B");    weights.push_back(1);
              samples.push_back("SingleElectron2017D");    weights.push_back(1);
              samples.push_back("SingleElectron2017F");    weights.push_back(1);
              samples.push_back("SingleMuon2017D");        weights.push_back(1);
              samples.push_back("SingleMuon2017F");        weights.push_back(1);
              samples.push_back("SingleElectron2017C");    weights.push_back(1);
              samples.push_back("SingleElectron2017E");    weights.push_back(1);
              samples.push_back("SingleMuon2017C");        weights.push_back(1);
              samples.push_back("SingleMuon2017E");        weights.push_back(1);
	    }
          }

  }
  const char* tree_path; int min_ntracks0 = 0; int max_ntracks0 = 1000000; int min_ntracks1 = 0; int max_ntracks1 = 1000000; //which ntracks?
  if (p.ntracks() == 3)      { tree_path = "mfvMiniTreeNtk3/t"; }
  else if (p.ntracks() == 4) { tree_path = "mfvMiniTreeNtk4/t"; }
  else if (p.ntracks() == 5) { tree_path = "mfvMiniTree/t"; }
  else if (p.ntracks() == 7) { tree_path = "mfvMiniTreeNtk3or4/t"; min_ntracks0 = 4; max_ntracks0 = 4; min_ntracks1 = 3; max_ntracks1 = 3; }
  else if (p.ntracks() == 8) { tree_path = "mfvMiniTreeNtk3or5/t"; min_ntracks0 = 5; max_ntracks0 = 5; min_ntracks1 = 3; max_ntracks1 = 3; }
  else if (p.ntracks() == 9) { tree_path = "mfvMiniTreeNtk4or5/t"; min_ntracks0 = 5; max_ntracks0 = 5; min_ntracks1 = 4; max_ntracks1 = 4; }
  else { fprintf(stderr, "bad ntracks"); exit(1); }

  double dphi_pdf_c; double dphi_pdf_e = 2; double dphi_pdf_a; //deltaphi input
  if (p.is_mc()) {
    if      (p.year() == "20161")        { dphi_pdf_c = 1.22; dphi_pdf_a = 2.63; }
    else if (p.year() == "20162")        { dphi_pdf_c = 1.22; dphi_pdf_a = 2.54; }
    else if (p.year() == "20162")         { dphi_pdf_c = 1.22; dphi_pdf_a = 2.73; }
    else if (p.year() == "2017")         { dphi_pdf_c = 1.24; dphi_pdf_a = 4.86; }
    else if (p.year() == "2018")         { dphi_pdf_c = 1.38; dphi_pdf_a = 3.77; }
    else if (p.year() == "2017p8" or p.year() == "run2")  { dphi_pdf_c = 1.23; dphi_pdf_a = 4.18; }
    else { fprintf(stderr, "bad year"); exit(1); }
  } else if (p.only_10pc()) {
    if (p.year() == "2017")         { dphi_pdf_c = 1.34; dphi_pdf_a = 5.44; }
    else if (p.year() == "2018")    { dphi_pdf_c = 1.25; dphi_pdf_a = 6.21; }
    else if (p.year() == "2017p8")  { dphi_pdf_c = 1.30; dphi_pdf_a = 5.78; }
    else if (p.year() == "2017B")   { dphi_pdf_c = 1.29; dphi_pdf_a = 4.84; }
    else if (p.year() == "2017C")   { dphi_pdf_c = 1.29; dphi_pdf_a = 4.84; }
    else if (p.year() == "2017D")   { dphi_pdf_c = 1.29; dphi_pdf_a = 4.84; }
    else if (p.year() == "2017E")   { dphi_pdf_c = 1.29; dphi_pdf_a = 4.84; }
    else if (p.year() == "2017F")   { dphi_pdf_c = 1.29; dphi_pdf_a = 4.84; }
    else { fprintf(stderr, "bad year"); exit(1); }
  } else {
    if (p.year() == "2017")         { dphi_pdf_c = 1.31; dphi_pdf_a = 5.91; }
    else if (p.year() == "2018")    { dphi_pdf_c = 1.30; dphi_pdf_a = 6.01; }
    else if (p.year() == "2017p8")  { dphi_pdf_c = 1.31; dphi_pdf_a = 5.96; }
    else { fprintf(stderr, "bad year"); exit(1); }
  }

  const char* vpeffs_version; //efficiency input
  if (p.only_10pc()) {
    vpeffs_version = "ULV11Bm";
  } else {
    vpeffs_version = "ULV11Bm";
  }
  TString eff_file_name_2d = TString::Format("/afs/cern.ch/user/p/pekotamn/crabdirs/vpeffs%s_%s_%s%s.root", p.is_mc() ? "" : "_data", p.year().c_str(), vpeffs_version, p.vary_eff() ? "_ntkseeds" : "");
  TString jet_angle_fname = TString::Format("background_lw_2017.root");

  const char* eff_hist = "maxtk3";
  if (p.vary_eff()) {
    if (p.ntracks() == 3)      { eff_hist = "maxtk3"; }
    else if (p.ntracks() == 4) { eff_hist = "maxtk4"; }
    else if (p.ntracks() == 5) { eff_hist = "maxtk5"; }
    else                       { eff_hist = "maxtk3"; }
  }


  gRandom->SetSeed(12191982);

  //fill only-one-vertex dBV distribution
  TH1D* h_1v_dbv = new TH1D("h_1v_dbv", "only-one-vertex events;d_{BV} (cm);events", 1250, 0, 2.5);
  TH2D* h_1v_xy  = new TH2D("h_1v_xy", "only-one-vertex events;x0 (cm);y0 (cm)", 250, -1.0, 1.0, 250, -1.0, 1.0);
  TH1D* h_1v_dbv0 = new TH1D("h_1v_dbv0", "only-one-vertex events;d_{BV}^{0} (cm);events", 1000, 0, 2.0);
  TH1D* h_1v_dbv1 = new TH1D("h_1v_dbv1", "only-one-vertex events;d_{BV}^{1} (cm);events", 1000, 0, 2.0);
  TH2D* h_1v_dbv_dz = new TH2D("h_1v_dbv_dz", "only-one-vertex events;d_{BV} (cm); d_{z} (cm)", 1000, 0, 2.0, 1000, 0, 2.0);
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
  TH1F* h_2v_sumdbv = new TH1F("h_2v_sumdbv", "two-vertex events; #Sigma(d_{BV})  (cm);events", 25, 0., 1.);
  TH1F* h_2v_dphivv = new TH1F("h_2v_dphivv", "two-vertex events;#Delta#phi_{VV};events", 10, -3.15, 3.15);
  TH1F* h_2v_absdphivv = new TH1F("h_2v_absdphivv", "two-vertex events;|#Delta#phi_{VV}|;events", 5, 0, 3.15);
  TH1D* h_2v_npu = new TH1D("h_2v_npu", "two-vertex events;# PU interactions;events", 100, 0, 100);

  int ns = (int)samples.size();
  for (int i = 0; i < ns; ++i) {
    mfv::MiniNtuple nt;
    TString fn = TString::Format("%s/%s.root", file_path, samples[i]);
    std::cout << fn.Data() << "\n";
    TFile* f = TFile::Open(fn);
    if (!f || !f->IsOpen()) { fprintf(stderr, "bad file"); exit(1); }

    std::cout << tree_path << std::endl;
    TTree* t = (TTree*)f->Get(tree_path);
    if (!t) { fprintf(stderr, "bad tree"); exit(1); }

    // Tight WP of DeepJet
    float bdisc_cut_value = 0;

    std::string st_name = samples[i];

    // 20161 must come before 2016 in these conditionals
    if (st_name.find("20161") != std::string::npos) {
      bdisc_cut_value = 0.6502;
    } 
    else if (st_name.find("20162") != std::string::npos) {
      bdisc_cut_value = 0.6377;
    } 
    else if (st_name.find("2017") != std::string::npos) {
      bdisc_cut_value = 0.7476;
    } 
    else if (st_name.find("2018") != std::string::npos) {
      bdisc_cut_value = 0.7100;
    } 

    mfv::read_from_tree(t, nt);
    for (int j = 0, je = t->GetEntries(); j < je; ++j) {
      if (t->LoadTree(j) < 0) break;
      if (t->GetEntry(j) <= 0) continue;
      if ((p.bquarks() == 0 && nt.gen_flavor_code == 2) || (p.bquarks() == 1 && nt.gen_flavor_code != 2)) continue;
      if ((p.btags() == 0 && nt.nbtags(bdisc_cut_value) >= 1) || (p.btags() == 1 && nt.nbtags(bdisc_cut_value) < 1)) continue;
      if (nt.npu < p.min_npu() || nt.npu > p.max_npu()) continue;
      const float w = weights[i] * nt.weight;

      if (nt.nvtx == 1) {
        float temp_dbv      = sqrt(nt.x0*nt.x0 + nt.y0*nt.y0);
        //float temp_dbv      = sqrt((nt.x0-nt.bsx)*(nt.x0-nt.bsx) + (nt.y0-nt.bsy)*(nt.y0-nt.bsy));
        float temp_dbv_pv   = sqrt((nt.x0-nt.pvx)*(nt.x0-nt.pvx) + (nt.y0-nt.pvy)*(nt.y0-nt.pvy));

        h_1v_dbv->Fill(temp_dbv, w);
        h_1v_xy->Fill(nt.x0, nt.y0, w);
        
        bool skip_hw = (w > 15.0);
        if (not skip_hw) {
          if (nt.ntk0 >= min_ntracks0 && nt.ntk0 <= max_ntracks0) h_1v_dbv0->Fill(temp_dbv_pv, w);
          if (nt.ntk0 >= min_ntracks1 && nt.ntk0 <= max_ntracks1) h_1v_dbv1->Fill(temp_dbv_pv, w);
          h_1v_phiv->Fill(atan2(nt.y0,nt.x0), w);
          h_1v_npu->Fill(nt.npu, w);
          h_1v_njets->Fill(nt.njets, w);
          h_1v_ht40->Fill(nt.ht(40.), w);
        }
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
        h_2v_sumdbv->Fill(dbv0+dbv1, w);
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
  TH1F* h_c1v_dvv = new TH1F("h_c1v_dvv", "constructed from only-one-vertex events;d_{VV} (cm);events", 100, 0, 1.);
  TH1F* h_c1v_sumdbv = new TH1F("h_c1v_sumdbv", "constructed from only-one-vertex events;#Sigma(d_{BV}) (cm);events", 25, 0, 1.);
  TH1F* h_c1v_absdphivv = new TH1F("h_c1v_absdphivv", "constructed from only-one-vertex events;|#Delta#phi_{VV}|;events", 5, 0, 3.15);
  TH1F* h_c1v_dbv0 = new TH1F("h_c1v_dbv0", "constructed from only-one-vertex events;d_{BV}^{0} (cm);events", 1250, 0, 2.5);
  TH1F* h_c1v_dbv1 = new TH1F("h_c1v_dbv1", "constructed from only-one-vertex events;d_{BV}^{1} (cm);events", 1250, 0, 2.5);
  TH2F* h_c1v_dbv1_dbv0 = new TH2F("h_c1v_dbv1_dbv0", "constructed from only-one-vertex events;d_{BV}^{0} (cm);d_{BV}^{1} (cm)", 1250, 0, 2.5, 1250, 0, 2.5);


  //TF1* f_dphi = new TF1("f_dphi", "(abs(x)-[0])**[1] + [2]", 0, M_PI);
  //f_dphi->SetParameters(dphi_pdf_c, dphi_pdf_e, dphi_pdf_a);
  TF1* f_dphi = new TF1("f_dphi", "[1] + [2] + 1.0/[0]", 0, M_PI);
  dphi_pdf_c = M_PI;
  f_dphi->SetParameters(dphi_pdf_c, 0.0, 0.0);
  
  TF1* i_dphi = 0;
  TF1* i_dphi2 = 0;
  if (p.vary_dphi()) {
    i_dphi = new TF1("i_dphi", "((1/([1]+1))*(x-[0])**([1]+1) + [2]*x - (1/([1]+1))*(-[0])**([1]+1)) / ((1/([1]+1))*(3.14159-[0])**([1]+1) + [2]*3.14159 - (1/([1]+1))*(-[0])**([1]+1))", 0, M_PI);
    i_dphi->SetParameters(dphi_pdf_c, dphi_pdf_e, dphi_pdf_a);
    i_dphi2 = new TF1("i_dphi2", "x/3.14159", 0, M_PI);
  }

  TFile* jet_angle_file = TFile::Open(jet_angle_fname);

  TH1F* h_eff_2d = 0;
  if (p.clearing_from_eff()) {
    TFile* eff_file = TFile::Open(eff_file_name_2d);
    if (!eff_file || !eff_file->IsOpen()) { fprintf(stderr, "bad file"); exit(1); }
    h_eff_2d = (TH1F*)eff_file->Get(eff_hist);
    h_eff_2d->SetBinContent(h_eff_2d->GetNbinsX()+1, h_eff_2d->GetBinContent(h_eff_2d->GetNbinsX()));
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

    double dphi   = f_dphi->GetRandom();

    double dvvc   = sqrt(dbv0*dbv0 + dbv1*dbv1 - 2*dbv0*dbv1*cos(dphi));
    double sumdbv = dbv0 + dbv1;

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

    double prob  = 1;
    if (p.clearing_from_eff()) {
      prob = h_eff_2d->GetBinContent(h_eff_2d->FindBin(dvvc));
      prob *= p.extra_eff_2d(dvvc);
    }

    if (dvvc > dvv_nbins * dvv_bin_width - 0.5*dvv_bin_width) dvvc = dvv_nbins * dvv_bin_width - 0.5*dvv_bin_width;
    h_c1v_dvv->Fill(dvvc, prob);
    h_c1v_sumdbv->Fill(sumdbv, prob);
    h_c1v_absdphivv->Fill(fabs(dphi), prob);
    h_c1v_dbv0->Fill(dbv0, prob);
    h_c1v_dbv1->Fill(dbv1, prob);
    h_c1v_dbv1_dbv0->Fill(dbv0, dbv1, prob);

    events_after_eff += prob;
  }
  printf("events before efficiency correction = %d, events after efficiency correction = %f, integrated efficiency correction = %f\n", nsamples, events_after_eff, events_after_eff/nsamples);

  TString cb_cbbar = TString::Format("%s, %f", out_fn, events_after_eff/nsamples);
  cb_cbbar_vector.push_back(cb_cbbar);

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
  h_1v_xy->Write();
  h_1v_dbv0->Write();
  h_1v_dbv1->Write();
  h_1v_dbv_dz->Write();
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
  h_2v_sumdbv->Write();
  h_2v_dphivv->Write();
  h_2v_absdphivv->Write();
  h_2v_npu->Write();

  h_c1v_dbv->Write();
  //h_c1v_dvv->Scale(1./h_c1v_dvv->Integral());
  h_c1v_dvv->Write();
  //h_c1v_sumdbv->Scale(1./h_c1v_sumdbv->Integral());
  h_c1v_sumdbv->Write();
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

  TCanvas* c_sumdbv = new TCanvas("c_sumdbv", "c_sumdbv", 700, 700);
  TLegend* l_sumdbv = new TLegend(0.35,0.75,0.85,0.85);
  h_2v_sumdbv->SetTitle(";#Sigmad_{BV} (cm);events");
  h_2v_sumdbv->SetLineColor(kBlue);
  h_2v_sumdbv->SetLineWidth(3);
  h_2v_sumdbv->Scale(1./h_2v_sumdbv->Integral());
  h_2v_sumdbv->SetStats(0);
  h_2v_sumdbv->Draw();
  l_sumdbv->AddEntry(h_2v_sumdbv, "two-vertex events");
  h_c1v_sumdbv->SetLineColor(kRed);
  h_c1v_sumdbv->SetLineWidth(3);
  h_c1v_sumdbv->Scale(1./h_c1v_sumdbv->Integral());
  h_c1v_sumdbv->SetStats(0);
  h_c1v_sumdbv->Draw("sames");
  l_sumdbv->AddEntry(h_c1v_sumdbv, "constructed from only-one-vertex events");
  l_sumdbv->SetFillColor(0);
  l_sumdbv->Draw();
  c_sumdbv->SetTickx();
  c_sumdbv->SetTicky();
  c_sumdbv->Write();


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
    h_eff_2d->SetName("h_eff_2d");
    h_eff_2d->Write();
  }
  if (p.vary_dphi()) {
    i_dphi->Write();
    i_dphi2->Write();
  }

  fh->Close();

  delete h_1v_dbv;
  delete h_1v_xy;
  delete h_1v_dbv0;
  delete h_1v_dbv1;
  delete h_1v_dbv_dz;
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
  delete h_2v_sumdbv;
  delete h_2v_dphivv;
  delete h_2v_absdphivv;
  delete h_2v_npu;
  delete c_dvv;
  delete c_sumdbv;
  delete c_absdphivv;
  delete h_c1v_dbv;
  delete h_c1v_dvv;
  delete h_c1v_sumdbv;
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
  const char* version = "ULV30Lepm";
  //const char* version = "ULV11";

 
  // This for loop runs over simulated background 
  
  for (const char* year : {"2017", "2018", "2017p8"}) { //{"20161", "20162", "2017", "2018", "2017p8", "run2"}) {
    for (int ntracks : {3, 4, 5, 7}) {
      ConstructDvvcParameters pars2 = pars.year(year).ntracks(ntracks);

      construct_dvvc(pars2,                                     TString::Format("2v_from_jets_%s_%dtrack_default_%s.root", year, ntracks, version));
      construct_dvvc(pars2.btags(1),     TString::Format("2v_from_jets_%s_%dtrack_btags_%s.root", year, ntracks, version));
      construct_dvvc(pars2.btags(0),     TString::Format("2v_from_jets_%s_%dtrack_nobtags_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.vary_dphi(true),          TString::Format("2v_from_jets_%s_%dtrack_vary_dphi_default_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.btags(1).vary_dphi(true), TString::Format("2v_from_jets_%s_%dtrack_vary_dphi_btags_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.btags(0).vary_dphi(true), TString::Format("2v_from_jets_%s_%dtrack_vary_dphi_nobtags_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.btags(1).vary_eff(true), TString::Format("2v_from_jets_%s_%dtrack_vary_eff_btags_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.btags(0).vary_eff(true), TString::Format("2v_from_jets_%s_%dtrack_vary_eff_nobtags_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.              TString::Format("2v_from_jets_%s_%dtrack_bquark_uncorrected_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.bquarks(1),   TString::Format("2v_from_jets_%s_%dtrack_bquarks_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.bquarks(0),   TString::Format("2v_from_jets_%s_%dtrack_nobquarks_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.btags(1).inject_signal(true),     TString::Format("2v_from_jets_%s_%dtrack_btags_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.btags(0).inject_signal(true),     TString::Format("2v_from_jets_%s_%dtrack_nobtags_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.clearing_from_eff(false),            TString::Format("2v_from_jets_%s_%dtrack_noclearing_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.min_npu(0).max_npu(27),              TString::Format("2v_from_jets_%s_%dtrack_npu0to27_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.min_npu(28).max_npu(36),             TString::Format("2v_from_jets_%s_%dtrack_npu28to36_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.min_npu(37).max_npu(255),            TString::Format("2v_from_jets_%s_%dtrack_npu37to255_%s.root", year, ntracks, version));
    }
  }
    
  // This for loop runs over real data
  /*
  for (const char* year : {"2017",}){ // "2018", "2017p8"}) {
    for (int ntracks : {3, 4, 5, 7,}){ // 8, 9}) {
      ConstructDvvcParameters pars2 = pars.year(year).ntracks(ntracks).is_mc(false);
      construct_dvvc(pars2,                             TString::Format("2v_from_jets_data_%s_%dtrack_default_%s.root", year, ntracks, version));
      construct_dvvc(pars2.btags(1),                    TString::Format("2v_from_jets_data_%s_%dtrack_btags_%s.root", year, ntracks, version));
      construct_dvvc(pars2.btags(0),                    TString::Format("2v_from_jets_data_%s_%dtrack_nobtags_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.btags(1).vary_dphi(true),    TString::Format("2v_from_jets_data_%s_%dtrack_vary_dphi_btags_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.btags(0).vary_dphi(true),    TString::Format("2v_from_jets_data_%s_%dtrack_vary_dphi_nobtags_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.btags(1).vary_eff(true),     TString::Format("2v_from_jets_data_%s_%dtrack_vary_eff_btags_%s.root", year, ntracks, version));
//      construct_dvvc(pars2.btags(0).vary_eff(true),     TString::Format("2v_from_jets_data_%s_%dtrack_vary_eff_nobtags_%s.root", year, ntracks, version));
    }
  }
  */
  // For use in bquark_fraction.py
  std::ofstream outfile;
  outfile.open("cb_vals/cb_vals.csv");
  outfile << "variant,cb_val" << std::endl;;

  for(TString cb_cbbar : cb_cbbar_vector){
    if(cb_cbbar.Contains("_btags_") || cb_cbbar.Contains("_nobtags_")){

      // format for our csv file
      cb_cbbar.ReplaceAll("2v_from_jets_","");
      cb_cbbar.ReplaceAll("_"+(TString)version+".root","");

      cb_cbbar.ReplaceAll("_btags","_cb");
      cb_cbbar.ReplaceAll("_nobtags","_cbbar");
      cb_cbbar.ReplaceAll("track","trk");
      cb_cbbar.ReplaceAll(" ","");
      outfile << cb_cbbar << std::endl;
    }
  }
  outfile.close();
}
