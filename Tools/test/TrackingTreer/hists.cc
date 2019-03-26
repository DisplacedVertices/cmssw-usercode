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
#include "JMTucker/Tools/interface/PileupWeights.h"
#include "JMTucker/Tools/interface/Ntuple.h"
#include "utils.h"

int main(int argc, char** argv) {
  std::string in_fn;
  std::string out_fn("hists.root");
  std::string json;
  float nevents_frac;
  std::string pu_weights;

  {
    namespace po = boost::program_options;
    po::options_description desc("Allowed options");
    desc.add_options()
      ("help,h", "this help message")
      ("input-file,i",   po::value<std::string>(&in_fn),                                             "the input file (required)")
      ("output-file,o",  po::value<std::string>(&out_fn)        ->default_value("hists.root"),       "the output file")
      ("json,j",         po::value<std::string>(&json),                                              "lumi mask json file for data")
      ("nevents-frac,n", po::value<float>(&nevents_frac)        ->default_value(1.f),                "only run on this fraction of events in the tree")
      ("pu-weights",     po::value<std::string>(&pu_weights)    ->default_value("2017"),             "pileup weights to use")
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
            << " pu_weights: " << pu_weights
            << "\n";

  root_setup();

  jmt::PileupWeights puwhelper(pu_weights);

  file_and_tree fat(in_fn.c_str(), out_fn.c_str());
  fat.t->GetEntry(0);
  const jmt::TrackingNtuple& nt = fat.nt;
  const jmt::TracksSubNtuple& ntt = nt.tracks();

  const bool is_mc = nt.base().run() == 1;

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

    if (!is_mc && good_ll.get() && !good_ll->contains(nt.base()))
      continue;

    double w = 1;

    h_npu->Fill(nt.base().npu());

    if (is_mc && puwhelper.valid())
      w *= puwhelper.w(nt.base().npu());

    h_npv->Fill(nt.pvs().n(), w);

    h_bsx->Fill(nt.bs().x(), w);
    h_bsy->Fill(nt.bs().y(), w);
    h_bsz->Fill(nt.bs().z(), w);
    h_bsdxdz->Fill(nt.bs().dxdz(), w);
    h_bsdydz->Fill(nt.bs().dydz(), w);
    h_bsy_v_bsx->Fill(nt.bs().x(), nt.bs().y(), w);

    h_pvbsx->Fill(nt.pvs().x(0) - nt.bs().x(nt.pvs().z(0)), w);
    h_pvbsy->Fill(nt.pvs().y(0) - nt.bs().y(nt.pvs().z(0)), w);
    h_pvbsz->Fill(nt.pvs().z(0) - nt.bs().z(),              w);

    h_pvy_v_pvx->Fill(nt.pvs().x(0), nt.pvs().y(0), w);

    int ntracks[max_tk_type] = {0};

    for (int itk = 0, itke = ntt.n(); itk < itke; ++itk) {
      const double pt = ntt.pt(itk);
      const int min_r = ntt.min_r(itk);
      const int npxlayers = ntt.npxlayers(itk);
      const int nstlayers = ntt.nstlayers(itk);
      const double nsigmadxy = ntt.nsigmadxybs(itk);

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

      //const bool high_purity = npxlayers == 4 && fabs(ntt.eta(itk)) < 0.8 && fabs(ntt.dz(itk)) < 10;
      //const bool etalt1p5 = fabs(ntt.eta(itk)) < 1.5;

      for (int i = 0; i < max_tk_type; ++i) {
	if (!tk_ok[i]) continue;
	++ntracks[i];

        // JMTBAD separate plots for dxy, dxybs, dxypv, dz, dzpv

	h_tracks_pt[i]->Fill(pt, w);
	h_tracks_eta[i]->Fill(ntt.eta(itk), w);
	h_tracks_phi[i]->Fill(ntt.phi(itk), w);
	h_tracks_dxy[i]->Fill(ntt.dxybs(itk), w);
	h_tracks_absdxy[i]->Fill(fabs(ntt.dxybs(itk)), w);
	h_tracks_dz[i]->Fill(ntt.dz(itk), w);
	h_tracks_dzpv[i]->Fill(ntt.dzpv(itk), w);
	h_tracks_nhits[i]->Fill(ntt.nhits(itk), w);
	h_tracks_npxhits[i]->Fill(ntt.npxhits(itk), w);
	h_tracks_nsthits[i]->Fill(ntt.nsthits(itk), w);
	h_tracks_min_r[i]->Fill(min_r, w);
	h_tracks_npxlayers[i]->Fill(npxlayers, w);
	h_tracks_nstlayers[i]->Fill(nstlayers, w);
	h_tracks_nsigmadxy[i]->Fill(nsigmadxy, w);

	h_tracks_dxyerr[i]->Fill(ntt.err_dxy(itk), w);
	h_tracks_dzerr[i]->Fill(ntt.err_dz(itk), w);
	h_tracks_pterr[i]->Fill(ntt.err_pt(itk), w);
	h_tracks_phierr[i]->Fill(ntt.err_phi(itk), w);
	h_tracks_etaerr[i]->Fill(ntt.err_eta(itk), w);

	h_tracks_nstlayers_v_eta[i]->Fill(ntt.eta(itk), nstlayers, w);
	h_tracks_dxy_v_eta[i]->Fill(ntt.eta(itk), ntt.dxybs(itk), w);
	h_tracks_dxy_v_phi[i]->Fill(ntt.phi(itk), ntt.dxybs(itk), w);
	h_tracks_dxy_v_nstlayers[i]->Fill(nstlayers, ntt.dxybs(itk), w);
	h_tracks_nstlayers_v_phi[i]->Fill(ntt.phi(itk), nstlayers, w);
	h_tracks_npxlayers_v_phi[i]->Fill(ntt.phi(itk), npxlayers, w);
	h_tracks_nhits_v_phi[i]->Fill(ntt.phi(itk), ntt.nhits(itk), w);
	h_tracks_npxhits_v_phi[i]->Fill(ntt.phi(itk), ntt.npxhits(itk), w);
	h_tracks_nsthits_v_phi[i]->Fill(ntt.phi(itk), ntt.nsthits(itk), w);

	h_tracks_nsigmadxy_v_eta[i]->Fill(ntt.eta(itk), nsigmadxy, w);
	h_tracks_nsigmadxy_v_nstlayers[i]->Fill(nstlayers, nsigmadxy, w);
	h_tracks_nsigmadxy_v_dxy[i]->Fill(ntt.dxybs(itk), nsigmadxy, w);
	h_tracks_nsigmadxy_v_dxyerr[i]->Fill(ntt.err_dxy(itk), nsigmadxy, w);

	h_tracks_dxyerr_v_pt[i]->Fill(pt, ntt.err_dxy(itk), w);
	h_tracks_dxyerr_v_eta[i]->Fill(ntt.eta(itk), ntt.err_dxy(itk), w);
	h_tracks_dxyerr_v_phi[i]->Fill(ntt.phi(itk), ntt.err_dxy(itk), w);
	h_tracks_dxyerr_v_dxy[i]->Fill(ntt.dxybs(itk), ntt.err_dxy(itk), w);
	h_tracks_dxyerr_v_dz[i]->Fill(ntt.dz(itk), ntt.err_dxy(itk), w);
	h_tracks_dxyerr_v_npxlayers[i]->Fill(npxlayers, ntt.err_dxy(itk), w);
	h_tracks_dxyerr_v_nstlayers[i]->Fill(nstlayers, ntt.err_dxy(itk), w);

	h_tracks_eta_v_phi[i]->Fill(ntt.phi(itk), ntt.eta(itk), w);
      }
    }
    for (int i = 0; i < max_tk_type; ++i) {
      h_ntracks[i]->Fill(ntracks[i], w);
    }
  }

  if (jjmax != jje) printf("\rdone with %llu events (out of %llu)\n", jjmax, jje);
  else              printf("\rdone with %llu events\n",               jjmax);
}
