#include <cassert>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <boost/program_options.hpp>
#include "TFile.h"
#include "TH2.h"
#include "TTree.h"
#include "TVector2.h"
#include "JMTucker/Tools/interface/LumiList.h"
#include "JMTucker/Tools/interface/TrackingTree.h"
#include "utils.h"

// be sure to change these if you target a different sample, e.g. 2018
// JMTBAD standardize pileup weight access
// 2017 pileup
const double pileup_weights[96] = { 0.184739, 3.87862, 3.43873, 2.55711, 1.66222, 1.50921, 1.28595, 1.25693, 0.615431, 1.45522, 1.4954, 1.48321, 1.33156, 1.16429, 1.07819, 1.05333, 1.08185, 1.1281, 1.16611, 1.18882, 1.2123, 1.23819, 1.26049, 1.27054, 1.27151, 1.27133, 1.27212, 1.26675, 1.27518, 1.25199, 1.22257, 1.16871, 1.10992, 1.03781, 0.968667, 0.911656, 0.867131, 0.834894, 0.787916, 0.750576, 0.758612, 0.79302, 0.859323, 0.959067, 1.09514, 1.25685, 1.41972, 1.49691, 1.52938, 1.46324, 1.33617, 1.15483, 0.950685, 0.749146, 0.569927, 0.411027, 0.28984, 0.198626, 0.13758, 0.0964932, 0.0693175, 0.0508504, 0.038385, 0.0299888, 0.0240799, 0.0170695, 0.0124844, 0.0107651, 0.00962124, 0.00879133, 0.00826726, 0.00803058, 0.00783523, 0.00781574, 0.00631688, 0.00535918, 0.00553274, 0.00551791, 0.00589565, 0.00594138, 0.00625883, 0.00628165, 0.00635429, 0.00491238, 0.00435898, 0.00445464, 0.00438023, 0.00456194, 0.00393917, 0.00424369, 0.00310455, 0.00284123, 0.00176242, 0.00148484, 0.00316881, 0.00199287 };

// 2018 pileup
#if 0
const double pileup_weights[100] = { 0, 11.5, 54.0978, 19.7888, 11.885, 9.25087, 6.26469, 4.80745, 3.49009, 2.64713, 2.15361, 1.82647, 1.63217, 1.50981, 1.44394, 1.40782, 1.39506, 1.40397, 1.42026, 1.42592, 1.43044, 1.41223, 1.38412, 1.3443, 1.29754, 1.24851, 1.20549, 1.16808, 1.13849, 1.11615, 1.09923, 1.09091, 1.08221, 1.07757, 1.07385, 1.06817, 1.0623, 1.05207, 1.03581, 1.01343, 0.982392, 0.940151, 0.892928, 0.837689, 0.773924, 0.707478, 0.639465, 0.570935, 0.504203, 0.442841, 0.385688, 0.333489, 0.288532, 0.249292, 0.215335, 0.187414, 0.162552, 0.142601, 0.1254, 0.110664, 0.0981898, 0.0867282, 0.0774977, 0.0687965, 0.060932, 0.05364, 0.0470512, 0.0413551, 0.0361235, 0.0315523, 0.027532, 0.0240214, 0.0210999, 0.0181469, 0.0153926, 0.013164, 0.0108045, 0.00947701, 0.0078069, 0.00700868, 0.00572437, 0.00443263, 0.0044066, 0.00291622, 0.0024858, 0.00209414, 0.00224626, 0.000990174, 0.000590135, 0.000335204, 0.000293124, 0.0004019, 0.00013152, 0.000127091, 9.06419e-05, 1.41345e-05, 1.95143e-05, 8.83322e-06, 1.96614e-06, 1.72141e-06 };
#endif

int main(int argc, char** argv) {
  std::string in_fn;
  std::string out_fn("hists.root");
  std::string json;
  float nevents_frac;

  {
    namespace po = boost::program_options;
    po::options_description desc("Allowed options");
    desc.add_options()
      ("help,h", "this help message")
      ("input-file,i",   po::value<std::string>(&in_fn),                                             "the input file (required)")
      ("output-file,o",  po::value<std::string>(&out_fn)        ->default_value("hists.root"),       "the output file")
      ("json,j",         po::value<std::string>(&json),                                              "lumi mask json file for data")
      ("nevents-frac,n", po::value<float>(&nevents_frac)        ->default_value(1.f),                "only run on this fraction of events in the tree")
      ;

    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, desc), vm);
    po::notify(vm);

    if (vm.count("help")) {
      std::cout << desc << "\n";
      return 1;
    }

    if (in_fn == "") {
      std::cout << "value for --input-file is required\n" << desc << "\n";
      return 1;
    }
  }

  std::cout << argv[0] << " with options:"
            << " in_fn: " << in_fn
            << " out_fn: " << out_fn
            << " json: " << (json != "" ? json : "none")
            << " nevents_frac: " << nevents_frac
            << "\n";

  root_setup();

  file_and_tree fat(in_fn.c_str(), out_fn.c_str());
  TrackingTree& nt = fat.nt;
  fat.t->GetEntry(0);

  const bool is_mc = nt.run() == 1;

  fat.f_out->mkdir("mfvWeight")->cd();
  TH1D* h_sums = (TH1D*)fat.f->Get("mcStat/h_sums")->Clone();
  if (is_mc && nevents_frac < 1) {
    h_sums->SetBinContent(1, h_sums->GetBinContent(1) * nevents_frac);
    for (int i = 2, ie = h_sums->GetNbinsX(); i <= ie; ++i) // invalidate other entries since we can't just assume equal weights in them
      h_sums->SetBinContent(i, -1e9);
  }
  fat.f_out->cd();

  std::unique_ptr<jmt::LumiList> good_ll;
  if (!is_mc && json != "") good_ll.reset(new jmt::LumiList(json));

  TH1D* h_norm = new TH1D("h_norm", "", 1, 0, 1);
  if (is_mc)
    h_norm->Fill(0.5, h_sums->GetBinContent(1));

  TH1D* h_npu = new TH1D("h_npu", ";true npu", 100, 0, 100);
  TH1D* h_npv = new TH1D("h_npv", ";number of primary vertices", 50, 0, 50);
  TH1D* h_bsx = new TH1D("h_bsx", ";beamspot x", 400, -0.15, 0.15);
  TH1D* h_bsy = new TH1D("h_bsy", ";beamspot y", 400, -0.15, 0.15);
  TH1D* h_bsz = new TH1D("h_bsz", ";beamspot z", 800, -5, 5);
  TH1D* h_bsdxdz = new TH1D("h_bsdxdz", ";beamspot dx/dz", 100, -1e-4, 5e-4);
  TH1D* h_bsdydz = new TH1D("h_bsdydz", ";beamspot dy/dz", 100, -1e-4, 1e-4);
  TH1D* h_pvbsx = new TH1D("h_pvbsx", ";pvx - bsx", 400, -0.05, 0.05);
  TH1D* h_pvbsy = new TH1D("h_pvbsy", ";pvy - bsy", 400, -0.05, 0.05); 
  TH1D* h_pvbsz = new TH1D("h_pvbsz", ";pvz - bsz", 500, -15, 15);
  TH2D* h_bsy_v_bsx = new TH2D("h_bsy_v_bsx", ";beamspot x;beamspot y", 4000, -1, 1, 4000, -1, 1);
  TH2D* h_pvy_v_pvx = new TH2D("h_pvy_v_pvx", ";pvx;pvy", 400, -1, 1, 400, -1, 1);

  enum { tk_all, tk_sel, tk_seed,  max_tk_type };

  TH1D* h_ntracks[max_tk_type];
  TH1D* h_tracks_pt[max_tk_type];
  TH1D* h_tracks_eta[max_tk_type];
  TH1D* h_tracks_phi[max_tk_type];
  TH1D* h_tracks_dxy[max_tk_type];

  TH1D* h_tracks_absdxy[max_tk_type];
  TH1D* h_tracks_dz[max_tk_type];
  TH1D* h_tracks_dzpv[max_tk_type];
  TH1D* h_tracks_nhits[max_tk_type];
  TH1D* h_tracks_npxhits[max_tk_type];
  TH1D* h_tracks_nsthits[max_tk_type];
  TH1D* h_tracks_min_r[max_tk_type];
  TH1D* h_tracks_npxlayers[max_tk_type];
  TH1D* h_tracks_nstlayers[max_tk_type];
  TH1D* h_tracks_nsigmadxy[max_tk_type];

  TH1D* h_tracks_dxyerr[max_tk_type];
  TH1D* h_tracks_dzerr[max_tk_type];
  TH1D* h_tracks_pterr[max_tk_type];
  TH1D* h_tracks_phierr[max_tk_type];
  TH1D* h_tracks_etaerr[max_tk_type];

  TH2D* h_tracks_nstlayers_v_eta[max_tk_type];
  TH2D* h_tracks_dxy_v_eta[max_tk_type];
  TH2D* h_tracks_dxy_v_phi[max_tk_type];
  TH2D* h_tracks_dxy_v_nstlayers[max_tk_type];
  TH2D* h_tracks_nstlayers_v_phi[max_tk_type];
  TH2D* h_tracks_npxlayers_v_phi[max_tk_type];
  TH2D* h_tracks_nhits_v_phi[max_tk_type];
  TH2D* h_tracks_npxhits_v_phi[max_tk_type];
  TH2D* h_tracks_nsthits_v_phi[max_tk_type];

  TH2D* h_tracks_nsigmadxy_v_eta[max_tk_type];
  TH2D* h_tracks_nsigmadxy_v_nstlayers[max_tk_type];
  TH2D* h_tracks_nsigmadxy_v_dxy[max_tk_type];
  TH2D* h_tracks_nsigmadxy_v_dxyerr[max_tk_type];

  TH2D* h_tracks_dxyerr_v_pt[max_tk_type];
  TH2D* h_tracks_dxyerr_v_eta[max_tk_type];
  TH2D* h_tracks_dxyerr_v_phi[max_tk_type];
  TH2D* h_tracks_dxyerr_v_dxy[max_tk_type];
  TH2D* h_tracks_dxyerr_v_dz[max_tk_type];
  TH2D* h_tracks_dxyerr_v_npxlayers[max_tk_type];
  TH2D* h_tracks_dxyerr_v_nstlayers[max_tk_type];

  TH2D* h_tracks_eta_v_phi[max_tk_type];

  const char* ex[max_tk_type] = {"all", "sel", "seed"};
  for (int i = 0; i < max_tk_type; ++i) {
    h_ntracks[i] = new TH1D(TString::Format("h_%s_ntracks", ex[i]), TString::Format(";number of %s tracks;events", ex[i]), 2000, 0, 2000);
    h_tracks_pt[i] = new TH1D(TString::Format("h_%s_tracks_pt", ex[i]), TString::Format("%s tracks;tracks pt;arb. units", ex[i]), 2000, 0, 200);
    h_tracks_eta[i] = new TH1D(TString::Format("h_%s_tracks_eta", ex[i]), TString::Format("%s tracks;tracks eta;arb. units", ex[i]), 50, -4, 4);
    h_tracks_phi[i] = new TH1D(TString::Format("h_%s_tracks_phi", ex[i]), TString::Format("%s tracks;tracks phi;arb. units", ex[i]), 315, -3.15, 3.15);
    h_tracks_dxy[i] = new TH1D(TString::Format("h_%s_tracks_dxy", ex[i]), TString::Format("%s tracks;tracks dxy to beamspot;arb. units", ex[i]), 400, -0.2, 0.2);
    h_tracks_absdxy[i] = new TH1D(TString::Format("h_%s_tracks_absdxy", ex[i]), TString::Format("%s tracks;tracks |dxy| to beamspot;arb. units", ex[i]), 200, 0, 0.2);
    h_tracks_dz[i] = new TH1D(TString::Format("h_%s_tracks_dz", ex[i]), TString::Format("%s tracks;tracks dz to BS;arb. units", ex[i]), 400, -20, 20);
    h_tracks_dzpv[i] = new TH1D(TString::Format("h_%s_tracks_dzpv", ex[i]), TString::Format("%s tracks;tracks dz to PV;arb. units", ex[i]), 400, -20, 20);
    h_tracks_nhits[i] = new TH1D(TString::Format("h_%s_tracks_nhits", ex[i]), TString::Format("%s tracks;tracks nhits;arb. units", ex[i]), 40, 0, 40);
    h_tracks_npxhits[i] = new TH1D(TString::Format("h_%s_tracks_npxhits", ex[i]), TString::Format("%s tracks;tracks npxhits;arb. units", ex[i]), 40, 0, 40);
    h_tracks_nsthits[i] = new TH1D(TString::Format("h_%s_tracks_nsthits", ex[i]), TString::Format("%s tracks;tracks nsthits;arb. units", ex[i]), 40, 0, 40);

    h_tracks_min_r[i] = new TH1D(TString::Format("h_%s_tracks_min_r", ex[i]), TString::Format("%s tracks;tracks min_r;arb. units", ex[i]), 20, 0, 20);
    h_tracks_npxlayers[i] = new TH1D(TString::Format("h_%s_tracks_npxlayers", ex[i]), TString::Format("%s tracks;tracks npxlayers;arb. units", ex[i]), 20, 0, 20);
    h_tracks_nstlayers[i] = new TH1D(TString::Format("h_%s_tracks_nstlayers", ex[i]), TString::Format("%s tracks;tracks nstlayers;arb. units", ex[i]), 20, 0, 20);
    h_tracks_nsigmadxy[i] = new TH1D(TString::Format("h_%s_tracks_nsigmadxy", ex[i]), TString::Format("%s tracks;tracks nsigmadxy;arb. units", ex[i]), 400, 0, 40);
    
    h_tracks_dxyerr[i] = new TH1D(TString::Format("h_%s_tracks_dxyerr", ex[i]), TString::Format("%s tracks;tracks dxyerr;arb. units", ex[i]), 2000, 0, 0.2);
    h_tracks_dzerr[i] = new TH1D(TString::Format("h_%s_tracks_dzerr", ex[i]), TString::Format("%s tracks;tracks dzerr;arb. units", ex[i]), 200, 0, 2);
    h_tracks_pterr[i] = new TH1D(TString::Format("h_%s_tracks_pterr", ex[i]), TString::Format("%s tracks;tracks pterr;arb. units", ex[i]), 200, 0, 0.2);
    h_tracks_phierr[i] = new TH1D(TString::Format("h_%s_tracks_phierr", ex[i]), TString::Format("%s tracks;tracks phierr;arb. units", ex[i]), 200, 0, 0.2);
    h_tracks_etaerr[i] = new TH1D(TString::Format("h_%s_tracks_etaerr", ex[i]), TString::Format("%s tracks;tracks etaerr;arb. units", ex[i]), 200, 0, 0.2);

    h_tracks_nstlayers_v_eta[i] = new TH2D(TString::Format("h_%s_tracks_nstlayers_v_eta", ex[i]), TString::Format("%s tracks;tracks eta;tracks nstlayers", ex[i]), 80, -4, 4, 20, 0, 20);
    h_tracks_dxy_v_eta[i] = new TH2D(TString::Format("h_%s_tracks_dxy_v_eta", ex[i]), TString::Format("%s tracks;tracks eta;tracks dxy to beamspot", ex[i]), 80, -4, 4, 400, -0.2, 0.2);
    h_tracks_dxy_v_nstlayers[i] = new TH2D(TString::Format("h_%s_tracks_dxy_v_nstlayers", ex[i]), TString::Format("%s tracks;tracks nstlayers;tracks dxy to beamspot", ex[i]), 20, 0, 20, 400, -0.2, 0.2);
    h_tracks_nsigmadxy_v_eta[i] = new TH2D(TString::Format("h_%s_tracks_nsigmadxy_v_eta", ex[i]), TString::Format("%s tracks;tracks eta;tracks nsigmadxy", ex[i]), 80, -4, 4, 200, 0, 20);
    h_tracks_nsigmadxy_v_nstlayers[i] = new TH2D(TString::Format("h_%s_tracks_nsigmadxy_v_nstlayers", ex[i]), TString::Format("%s tracks;tracks nstlayers;tracks nsigmadxy", ex[i]), 20, 0, 20, 200, 0, 20);
    h_tracks_nsigmadxy_v_dxy[i] = new TH2D(TString::Format("h_%s_tracks_nsigmadxy_v_dxy", ex[i]), TString::Format("%s tracks;tracks dxy to beamspot;tracks nsigmadxy", ex[i]), 400, -0.2, 0.2, 200, 0, 20);
    h_tracks_nsigmadxy_v_dxyerr[i] = new TH2D(TString::Format("h_%s_tracks_nsigmadxy_v_dxyerr", ex[i]), TString::Format("%s tracks;tracks dxyerr;tracks nsigmadxy", ex[i]), 200, 0, 0.2, 200, 0, 20);
    h_tracks_dxy_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_dxy_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks dxy to beamspot", ex[i]), 315, -3.15, 3.15, 400, -0.2, 0.2);
    h_tracks_nstlayers_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_nstlayers_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks nstlayers", ex[i]), 315, -3.15, 3.15, 20, 0, 20);
    h_tracks_npxlayers_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_npxlayers_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks npxlayers", ex[i]), 315, -3.15, 3.15, 10, 0, 10);
    h_tracks_nhits_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_nhits_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks nhits", ex[i]), 315, -3.15, 3.15, 40, 0, 40);
    h_tracks_npxhits_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_npxhits_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks npxhits", ex[i]), 315, -3.15, 3.15, 40, 0, 40);
    h_tracks_nsthits_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_nsthits_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks nsthits", ex[i]), 315, -3.15, 3.15, 40, 0, 40);

    h_tracks_dxyerr_v_pt[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_pt", ex[i]), TString::Format("%s tracks;tracks pt;tracks dxyerr", ex[i]), 2000, 0, 200, 2000, 0, 0.2);
    h_tracks_dxyerr_v_eta[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_eta", ex[i]), TString::Format("%s tracks;tracks eta;tracks dxyerr", ex[i]), 80, -4, 4, 2000, 0, 0.2);
    h_tracks_dxyerr_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks dxyerr", ex[i]), 126, -3.15, 3.15, 200, 0, 0.2);
    h_tracks_dxyerr_v_dxy[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_dxy", ex[i]), TString::Format("%s tracks;tracks dxy to beamspot;tracks dxyerr", ex[i]), 400, -0.2, 0.2, 200, 0, 0.2);
    h_tracks_dxyerr_v_dz[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_dz", ex[i]), TString::Format("%s tracks;tracks dz to beamspot;tracks dxyerr", ex[i]), 400, -20, 20, 200, 0, 0.2);
    h_tracks_dxyerr_v_npxlayers[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_npxlayers", ex[i]), TString::Format("%s tracks;tracks npxlayers;tracks dxyerr", ex[i]), 10, 0, 10, 200, 0, 0.2);
    h_tracks_dxyerr_v_nstlayers[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_nstlayers", ex[i]), TString::Format("%s tracks;tracks nstlayers;tracks dxyerr", ex[i]), 20, 0, 20, 200, 0, 0.2);

    h_tracks_eta_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_eta_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks eta", ex[i]), 126, -3.15, 3.15, 80, -4, 4);
  }

  unsigned long long jj = 0;
  const unsigned long long jje = fat.t->GetEntries();
  const unsigned long long jjmax = nevents_frac < 1 ? nevents_frac * jje : jje;
  for (; jj < jjmax; ++jj) {
    if (fat.t->LoadTree(jj) < 0) break;
    if (fat.t->GetEntry(jj) <= 0) continue;
    if (jj % 2000 == 0) {
      if (jjmax != jje) printf("\r%llu/%llu(/%llu)", jj, jjmax, jje);
      else              printf("\r%llu/%llu",        jj, jjmax);
      fflush(stdout);
    }

    if (!is_mc && good_ll.get() && !good_ll->contains(nt.run(), nt.lumi()))
      continue;

    double w = 1;

    if (is_mc) {
      const int npu = int(nt.npu());
      h_npu->Fill(npu);
      assert(npu >= 0);
      const double pileup_weight = pileup_weights[npu >= 96 ? 95 : npu];
      w *= pileup_weight;
    }

    h_npv->Fill(nt.npvs(), w);

    const double bsx = nt.bs_x();
    const double bsy = nt.bs_y();
    const double bsz = nt.bs_z();

    h_bsx->Fill(bsx, w);
    h_bsy->Fill(bsy, w);
    h_bsz->Fill(bsz, w);
    h_bsdxdz->Fill(nt.bs_dxdz(), w);
    h_bsdydz->Fill(nt.bs_dydz(), w);
    h_bsy_v_bsx->Fill(bsx, bsy, w);

    const double pvbsx = nt.pv_x(0) - bsx;
    const double pvbsy = nt.pv_y(0) - bsy;
    const double pvbsz = nt.pv_z(0) - bsz;
    h_pvbsx->Fill(pvbsx, w);
    h_pvbsy->Fill(pvbsy, w);
    h_pvbsz->Fill(pvbsz, w);

    h_pvy_v_pvx->Fill(nt.pv_x(0), nt.pv_y(0), w);

    int ntracks[max_tk_type] = {0};

    for (int itk = 0, itke = nt.ntks(); itk < itke; ++itk) {
      const double pt = nt.tk_pt(itk);
      const int min_r = nt.tk_min_r(itk);
      const int npxlayers = nt.tk_npxlayers(itk);
      const int nstlayers = nt.tk_nstlayers(itk);
      const double nsigmadxy = fabs(nt.tk_dxybs(itk)) / nt.tk_err_dxy(itk);

      const bool nm1[5] = {
	pt > 1,
	min_r <= 1,
	npxlayers >= 2,
	nstlayers >= 6,
	nsigmadxy > 4
      };

      const bool sel = nm1[0] && nm1[1] && nm1[2] && nm1[3];
      const bool seed = sel && nm1[4];
      const bool tk_ok[max_tk_type] = { true, sel, seed };

      //const bool high_purity = npxlayers == 4 && fabs(nt.tk_eta(itk)) < 0.8 && fabs(nt.tk_dzpv(itk) - pvbsz) < 10;
      //const bool etalt1p5 = fabs(nt.tk_eta(itk)) < 1.5;

      for (int i = 0; i < max_tk_type; ++i) {
	if (!tk_ok[i]) continue;
	++ntracks[i];

	h_tracks_pt[i]->Fill(pt, w);
	h_tracks_eta[i]->Fill(nt.tk_eta(itk), w);
	h_tracks_phi[i]->Fill(nt.tk_phi(itk), w);
	h_tracks_dxy[i]->Fill(nt.tk_dxybs(itk), w);
	h_tracks_absdxy[i]->Fill(fabs(nt.tk_dxybs(itk)), w);
	h_tracks_dz[i]->Fill(nt.tk_dzpv(itk) - pvbsz, w);
	h_tracks_dzpv[i]->Fill(nt.tk_dzpv(itk), w);
	h_tracks_nhits[i]->Fill(nt.tk_nhits(itk), w);
	h_tracks_npxhits[i]->Fill(nt.tk_npxhits(itk), w);
	h_tracks_nsthits[i]->Fill(nt.tk_nsthits(itk), w);
	h_tracks_min_r[i]->Fill(min_r, w);
	h_tracks_npxlayers[i]->Fill(npxlayers, w);
	h_tracks_nstlayers[i]->Fill(nstlayers, w);
	h_tracks_nsigmadxy[i]->Fill(nsigmadxy, w);

	h_tracks_dxyerr[i]->Fill(nt.tk_err_dxy(itk), w);
	h_tracks_dzerr[i]->Fill(nt.tk_err_dz(itk), w);
	h_tracks_pterr[i]->Fill(nt.tk_err_pt(itk), w);
	h_tracks_phierr[i]->Fill(nt.tk_err_phi(itk), w);
	h_tracks_etaerr[i]->Fill(nt.tk_err_eta(itk), w);

	h_tracks_nstlayers_v_eta[i]->Fill(nt.tk_eta(itk), nstlayers, w);
	h_tracks_dxy_v_eta[i]->Fill(nt.tk_eta(itk), nt.tk_dxybs(itk), w);
	h_tracks_dxy_v_phi[i]->Fill(nt.tk_phi(itk), nt.tk_dxybs(itk), w);
	h_tracks_dxy_v_nstlayers[i]->Fill(nstlayers, nt.tk_dxybs(itk), w);
	h_tracks_nstlayers_v_phi[i]->Fill(nt.tk_phi(itk), nstlayers, w);
	h_tracks_npxlayers_v_phi[i]->Fill(nt.tk_phi(itk), npxlayers, w);
	h_tracks_nhits_v_phi[i]->Fill(nt.tk_phi(itk), nt.tk_nhits(itk), w);
	h_tracks_npxhits_v_phi[i]->Fill(nt.tk_phi(itk), nt.tk_npxhits(itk), w);
	h_tracks_nsthits_v_phi[i]->Fill(nt.tk_phi(itk), nt.tk_nsthits(itk), w);

	h_tracks_nsigmadxy_v_eta[i]->Fill(nt.tk_eta(itk), nsigmadxy, w);
	h_tracks_nsigmadxy_v_nstlayers[i]->Fill(nstlayers, nsigmadxy, w);
	h_tracks_nsigmadxy_v_dxy[i]->Fill(nt.tk_dxybs(itk), nsigmadxy, w);
	h_tracks_nsigmadxy_v_dxyerr[i]->Fill(nt.tk_err_dxy(itk), nsigmadxy, w);

	h_tracks_dxyerr_v_pt[i]->Fill(pt, nt.tk_err_dxy(itk), w);
	h_tracks_dxyerr_v_eta[i]->Fill(nt.tk_eta(itk), nt.tk_err_dxy(itk), w);
	h_tracks_dxyerr_v_phi[i]->Fill(nt.tk_phi(itk), nt.tk_err_dxy(itk), w);
	h_tracks_dxyerr_v_dxy[i]->Fill(nt.tk_dxybs(itk), nt.tk_err_dxy(itk), w);
	h_tracks_dxyerr_v_dz[i]->Fill(nt.tk_dzpv(itk) - pvbsz, nt.tk_err_dxy(itk), w);
	h_tracks_dxyerr_v_npxlayers[i]->Fill(npxlayers, nt.tk_err_dxy(itk), w);
	h_tracks_dxyerr_v_nstlayers[i]->Fill(nstlayers, nt.tk_err_dxy(itk), w);

	h_tracks_eta_v_phi[i]->Fill(nt.tk_phi(itk), nt.tk_eta(itk), w);
      }
    }
    for (int i = 0; i < max_tk_type; ++i) {
      h_ntracks[i]->Fill(ntracks[i], w);
    }
  }

  if (jjmax != jje) printf("\rdone with %llu events (out of %llu)\n", jjmax, jje);
  else              printf("\rdone with %llu events\n",               jjmax);
}
