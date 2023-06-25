#include "BTagSFHelper.h"
#include "utils.h"

double ntks_weight(int i) {
  const int N = 60;
  if (i < 0 || i >= N) return 0;
  // from h_2_vtxntracks so only apply there?
  const double ws[N] = { 0., 0., 0., 0., 0., 0., 1.674196, 1.550810, 1.459271, 1.284317, 1.187709, 1.231090, 1.242313, 1.145012, 1.182134, 1.114840, 1.093479, 0.964026, 1.039401, 0.940219, 0.907171, 0.976593, 0.918716, 0.904142, 0.867394, 0.777177, 0.814517, 0.799371, 0.829022, 0.834422, 0.609130, 0.599720, 0.726436, 0.570779, 0.677044, 0.590878, 0.540080, 0.490107, 0.561173, 0.464503, 0.537223, 0.414802, 0.426949, 0.173858, 0.267836, 0.725926, 0.237331, 0.201321, 0.121923, 0.311854, 0.193843, 0.995309, 0., 0., 0., 0.559031, 0.810189, 0., 0., 0. };
  return ws[i];
}

int main(int argc, char** argv) {
  int itau = 10000;
  bool btagsf_weights = false;
  bool ntks_weights = false;

  jmt::NtupleReader<mfv::MovedTracksNtuple> nr;

  namespace po = boost::program_options;
  nr.init_options("mfvMovedTree20/t", "TrackMoverHistsV27m", "nr_trackmoverv27mv1")
    ("tau",           po::value<int>   (&itau)          ->default_value(10000),   "tau in microns, for reweighting")
    ("btagsf",        po::value<bool>  (&btagsf_weights)->default_value(false),   "whether to use b-tag SF weights")
    ("ntks-weights",  po::value<bool>  (&ntks_weights)  ->default_value(false),   "whether to use ntracks weights")
    ;

  if (!nr.parse_options(argc, argv)) return 1;
  std::cout << " tau: " << itau << " btagsf: " << btagsf_weights << " ntks_weights: " << ntks_weights << "\n";

  if (!nr.init()) return 1;
  auto& nt = nr.nt();
  auto& bs = nt.bs();
  auto& pvs = nt.pvs();
  auto& jets = nt.jets();	
  auto& muons = nt.muons();
  auto& electrons = nt.electrons();
  auto& tks = nt.tracks();
  auto& vs = nt.vertices();

  ////

  const int itau_original = 10000; // JMTBAD keep in sync with value in ntuple.py
  if (itau != itau_original)
    std::cout << "reweighting tau distribution from " << itau_original << " um to " << itau << " um\n";
  const double o_tau_from = 10000./itau_original;
  const double o_tau_to = 10000./itau;
  auto tau_weight = [&](double tau) { return o_tau_to/o_tau_from * exp((o_tau_from - o_tau_to) * tau); };

  std::unique_ptr<BTagSFHelper> btagsfhelper;
  if (btagsf_weights) btagsfhelper.reset(new BTagSFHelper);

  const std::vector<std::string> extra_weights_hists = {
    //"nocuts_npv_den",
    //"nocuts_pvz_den",
    //"nocuts_pvx_den",
    //"nocuts_pvy_den",
    //"nocuts_ntracks_den",
    //"nocuts_npv_den_redo"
    //"nocuts_ht_den",
    //"nocuts_pvntracks_den",
  };
  TFile* extra_weights = extra_weights_hists.size() > 0 ? TFile::Open("reweight.root") : 0;
  const bool use_extra_weights = extra_weights != 0 && extra_weights->IsOpen();
  if (use_extra_weights) printf("using extra weights from reweight.root\n");

  TH1D* h_tau = new TH1D("h_tau", ";tau (cm);events/10 #mum", 10000, 0,10);
  TH2D* h_tau_tw = new TH2D("h_tau_tw", ";tau (cm); weight from ctau=10mm", 25, 0, 10, 50, 0, 10);
  TH1D* h_btagsfweight = new TH1D("h_btagsfweight", ";weight;events/0.01", 200, 0, 2);

  const int num_numdens = 3;
  numdens nds[num_numdens] = { // JMTBAD why multiple dens here?
    numdens("nocuts"),
    numdens("ntracks"),
    numdens("all")
  };

  enum { k_movedist2, k_movedist3, k_movevectoreta, k_npv, k_pvx, k_pvy, k_pvz, k_pvrho, k_pvntracks, k_pvscore, k_ht, k_njets, k_nmuons, k_muon_pT, k_muon_abseta, k_muon_iso, k_muon_absdxy, k_neles, k_ele_pT, k_ele_abseta, k_ele_iso, k_ele_absdxy, k_jet_asymm, k_vtx_unc, k_jet_dr, k_jet_deta, k_jet_dphi, k_jet_dind, k_pt0, k_pt1, k_ntks_j0, k_ntks_j1, k_nmovedtracks, k_dphi_sum_j_mv, k_deta_sum_j_mv, k_jetpt0_asymm, k_jetpt1_asymm, k_jeteta0_asymm, k_jeteta1_asymm, k_jetdr_asymm, k_nalltracks, k_nseedtracks, k_npreseljets, k_npreselbjets, k_jeti01, k_jetp01, k_jetpt01, k_jeteta01, k_jetphi01, k_jetsume, k_jetdrmax, k_jetdravg, k_jetdetamax, k_jetdetaavg, k_jetdphimax, k_jetdphiavg, k_jet0_tkdrmax, k_jet1_tkdrmax, k_jet0_tkdravg, k_jet1_tkdravg, k_jet_dphi_deta_avg, k_jdphi_nmovedtks, k_jdeta_nmovedtks, k_jdr_nmovedtks, k_jtheta0_nmovedtks, k_jetmovea3d01, k_jetmovea3d_v_jetp, k_jetmovea3d0_v_movevectoreta, k_jetmovea3d1_v_movevectoreta, k_jeta3dmax, k_angle0, k_angle1, k_dphi_j0_mv, k_dphi_j1_mv, k_deta_j0_mv, k_deta_j1_mv, k_dphi_j0_mv_jdeta, k_jetsumntracks, k_jetntracks01, k_jetntracks_v_jetp, k_jetnseedtracks01, k_nvtx, k_vtxbs2derr, k_vtxbs2derr_avgtkdr, k_vtxbs2derr_jdeta, k_vtxbs2derr_dphi_j0_mv, k_vtxbs2derr_jdr, k_vtxeta, k_vtxz };

  for (numdens& nd : nds) {
    nd.book(k_movedist2, "movedist2", ";movement 2-dist;events/0.01 cm", 200, 0, 2);
    nd.book(k_movedist3, "movedist3", ";movement 3-dist;events/0.01 cm", 200, 0, 2);
    nd.book(k_movevectoreta, "movevectoreta", ";move vector eta;events/0.08 cm", 100, -4, 4);
    nd.book(k_npv, "npv", ";# PV;events/1", 100, 0, 100);
    nd.book(k_pvx, "pvx", ";PV x (cm);events/1.5 #mum", 200, -0.015, 0.015);
    nd.book(k_pvy, "pvy", ";PV y (cm);events/1.5 #mum", 200, -0.015, 0.015);
    nd.book(k_pvz, "pvz", ";PV z (cm);events/0.24 cm", 200, -24, 24);
    nd.book(k_pvrho, "pvrho", ";PV #rho (cm);events/1 #mum", 200, 0, 0.02);
    nd.book(k_pvntracks, "pvntracks", ";PV # tracks;events/2", 200, 0, 400);
    nd.book(k_pvscore, "pvscore", ";PV #Sigma p_{T}^{2} (GeV^{2});events/200 GeV^{2}", 200, 0, 40000);
    nd.book(k_ht, "ht", ";H_{T} (GeV);events/50 GeV", 20, 0, 1000);
	nd.book(k_njets, "njets", ";# jets;events/1", 20, 0, 20);
	nd.book(k_nmuons, "nmuons", ";# passed offline-sel muons;events/1", 10, 0, 10);
	nd.book(k_muon_pT, "muon_pT", ";muons p_{T} (GeV);events/1", 50, 0, 200);
	nd.book(k_muon_abseta, "muon_abseta", ";muons |#eta|; arb. units", 70, 0, 3.5);
	nd.book(k_muon_iso, "muon_iso", ";muons iso;events/1", 200, 0, 0.15);
	nd.book(k_muon_absdxy, "muon_absdxy", ";muons |dxy| cm; arb. units", 80, 0, 0.2);
	nd.book(k_neles, "neles", ";# passed offline-sel electrons;events/1", 10, 0, 10);
	nd.book(k_ele_pT, "ele_pT", ";electrons p_{T} (GeV);events/1", 50, 0, 200);
	nd.book(k_ele_abseta, "ele_abseta", ";electrons |#eta|; arb. units", 70, 0, 3.5);
	nd.book(k_ele_iso, "ele_iso", ";electrons iso;events/1", 200, 0, 0.15);
	nd.book(k_ele_absdxy, "ele_absdxy", ";electrons |dxy| cm; arb. units", 80, 0, 0.2);
	nd.book(k_jet_asymm, "jet_asymm", ";Jet asymmetry A_{J}; arb. units", 25, 0, 1);
	nd.book(k_vtx_unc, "vtx_unc", ";dist3d(move vector, vtx) cm; arb. units", 100, 0, 0.1);
	nd.book(k_jet_dr, "jet_dr", ";jets #DeltaR; arb. units", 70, 0, 7);
	nd.book(k_jet_deta, "jet_deta", ";jets #DeltaEta; arb. units", 70, 0, 7);
	nd.book(k_jet_dphi, "jet_dphi", ";jets #DeltaPhi; arb. units", 70, -3.5, 3.5);
	nd.book(k_jet_dind, "jet_dind", ";jets #DeltaIndex; arb. units", 20, 0, 20);
	nd.book(k_pt0, "pt0", ";Pt of jet0 [GeV]", 25, 0, 500);
	nd.book(k_pt1, "pt1", ";Pt of jet1 [GeV]", 25, 0, 500);
	nd.book(k_ntks_j0, "ntks_j0", ";Ntks in jet0", 25, 0, 25);
	nd.book(k_ntks_j1, "ntks_j1", ";Ntks in jet1", 25, 0, 25);
	nd.book(k_nmovedtracks, "nmovedtracks", ";# moved tracks;events/2", 120, 0, 120);
	nd.book(k_dphi_sum_j_mv, "dphi_sum_j_mv", ";abs #Delta #phi between jet0+jet1 and move vec;events/bin", 63, 0, M_PI);
	nd.book(k_deta_sum_j_mv, "deta_sum_j_mv", ";abs #Delta #eta between jet0+jet1 and move vec;events/bin", 25, 0, 4);
	
	nd.book(k_jetpt0_asymm, "jetpt0_asymm", ";jet p_{T} 0; jet asymm. A_{J}", 50, 0, 1000, 25, 0, 1);
    nd.book(k_jetpt1_asymm, "jetpt1_asymm", ";jet p_{T} 1; jet asymm. A_{J}", 50, 0, 1000, 25, 0, 1);
    nd.book(k_jeteta0_asymm, "jeteta0_asymm", ";jet #eta 0; jet asymm. A_{J}", 100, -4, 4, 25, 0, 1);
    nd.book(k_jeteta1_asymm, "jeteta1_asymm", ";jet #eta 1; jet asymm. A_{J}", 100, -4, 4, 25, 0, 1);
    nd.book(k_jetdr_asymm, "jetdr_asymm", ";jets #DeltaR; jet asymm. A_{J}", 70, 0, 7, 25, 0, 1);
    nd.book(k_nalltracks, "nalltracks", ";# all tracks;events/10", 200, 0, 2000);
    nd.book(k_nseedtracks, "nseedtracks", ";# selected tracks;events", 80, 0, 80);
    nd.book(k_npreseljets, "npreseljets", ";# preselected jets;events/1", 20, 0, 20);
    nd.book(k_npreselbjets, "npreselbjets", ";# preselected b jets;events/1", 20, 0, 20);
    nd.book(k_jeti01, "jeti01", ";jet i 0 (GeV);jet i 1 (GeV);events", 15, 0, 15, 15, 0, 15);
    nd.book(k_jetp01, "jetp01", ";jet 0 momentum (GeV);jet 1 momentum (GeV)", 200, 0, 2000, 200, 0, 2000);
    nd.book(k_jetpt01, "jetpt01", ";jet p_{T} 0 (GeV);jet p_{T} 1 (GeV)", 50, 0, 1000, 50, 0, 1000);
    nd.book(k_jeteta01, "jeteta01", ";jet #eta 0 (GeV);jet #eta 1 (GeV)", 100, -4, 4, 100, -4, 4);
    nd.book(k_jetphi01, "jetphi01", ";jet #phi 0 (GeV);jet #phi 1 (GeV)", 126, -M_PI, M_PI, 126, -M_PI, M_PI);
    nd.book(k_jetsume, "jetsume", ";#Sigma jet energy (GeV);events/5 GeV", 200, 0, 1000);
    nd.book(k_jetdrmax, "jetdrmax", ";max jet #Delta R;events/0.1", 70, 0, 7);
    nd.book(k_jetdravg, "jetdravg", ";avg jet #Delta R;events/0.1", 70, 0, 7);
    nd.book(k_jetdetamax, "jetdetamax", ";max jet #Delta #eta; events", 200, -5, 5);
    nd.book(k_jetdetaavg, "jetdetaavg", ";avg jet #Delta #eta; events", 200, -5, 5);
    nd.book(k_jetdphimax, "jetdphimax", ";max jet #Delta #phi; events", 32, -M_PI, M_PI);
    nd.book(k_jetdphiavg, "jetdphiavg", ";avg jet #Delta #phi; events", 32, -M_PI, M_PI);
    nd.book(k_jet0_tkdrmax, "jet0_tkdrmax", ";max track #Delta R in jet0; events", 63, 0, M_PI);
    nd.book(k_jet1_tkdrmax, "jet1_tkdrmax", ";max track #Delta R in jet1; events", 63, 0, M_PI);
    nd.book(k_jet0_tkdravg, "jet0_tkdravg", ";avg track #Delta R in jet0; events", 63, 0, M_PI);
    nd.book(k_jet1_tkdravg, "jet1_tkdravg", ";avg track #Delta R in jet1; events", 63, 0, M_PI);
    nd.book(k_jet_dphi_deta_avg, "jet_dphi_deta_avg", ";avg jet #Delta #phi; avg jet #Delta #eta", 31, -M_PI, M_PI, 50, -4, 4); 
    nd.book(k_jdphi_nmovedtks, "jdphi_nmovedtracks", ";abs. avg. jet #Delta #phi; no. moved tracks", 31, 0, M_PI, 60, 0, 120);
    nd.book(k_jdeta_nmovedtks, "jdeta_nmovedtracks", ";abs. avg. jet #Delta #eta; no. moved tracks", 25, 0, 4, 60, 0, 120);
    nd.book(k_jdr_nmovedtks, "jdr_nmovedtracks", ";avg. jet #Delta R; no. moved tracks", 30, 0, 6, 60, 0, 120);
    nd.book(k_jtheta0_nmovedtks, "jtheta0_nmovedtracks", ";3D angle btwn moved jet and move vector; no. moved tracks", 31, 0, M_PI, 60, 0, 120);
    nd.book(k_jetmovea3d01, "jetmovea3d", ";3D angle between jet 0 and move vector;3D angle between jet 1 and move vector", 63, 0, M_PI, 63, 0, M_PI);
    nd.book(k_jetmovea3d_v_jetp, "jetmovea3d_v_jetp", ";jet momentum p (GeV);3D angle between moved jet and move vector", 200, 0, 2000, 63, 0, M_PI);
    nd.book(k_jetmovea3d0_v_movevectoreta, "jetmovea3d0_v_movevectoreta", ";move vector eta;3D angle between moved jet and move vector", 100, -4, 4, 63, 0, M_PI);
    nd.book(k_jetmovea3d1_v_movevectoreta, "jetmovea3d1_v_movevectoreta", ";move vector eta;3D angle between moved jet and move vector", 100, -4, 4, 63, 0, M_PI);
    nd.book(k_jeta3dmax, "jeta3dmax", ";max 3D angle between moved jets;events/0.05", 63, 0, M_PI);
    nd.book(k_angle0, "jetmovea3d0", ";Angle between jet0 and SV;arb. units", 63, 0, M_PI);
    nd.book(k_angle1, "jetmovea3d1", ";Angle between jet1 and SV;arb. units", 63, 0, M_PI);
    nd.book(k_dphi_j0_mv, "dphi_j0_mv", ";abs #Delta #phi between jet0 and move vec;events/bin", 63, 0, M_PI);
    nd.book(k_dphi_j1_mv, "dphi_j1_mv", ";abs #Delta #phi between jet1 and move vec;events/bin", 63, 0, M_PI);
    nd.book(k_deta_j0_mv, "deta_j0_mv", ";abs #Delta #eta between jet0 and move vec;events/bin", 25, 0, 4);
    nd.book(k_deta_j1_mv, "deta_j1_mv", ";abs #Delta #eta between jet1 and move vec;events/bin", 25, 0, 4);
    nd.book(k_dphi_j0_mv_jdeta, "dphi_j0_mv_jdeta", ";abs #Delta #phi btwn jet0 and move vec; abs #Delta #eta btwn jets", 63, 0, M_PI, 50, 0, 5);
    nd.book(k_jetsumntracks, "jetsumntracks", ";#Sigma jet # tracks;events/5", 200, 0, 1000);
    nd.book(k_jetntracks01, "jetntracks01", ";jet # tracks 0;jet # tracks 1", 50, 0, 50, 50, 0, 50);
    nd.book(k_jetntracks_v_jetp, "jetntracks_v_jetp01", ";jet momentum (GeV);jet # tracks", 200, 0, 2000, 50, 0, 50);
    nd.book(k_jetnseedtracks01, "jetnseedtracks01", ";jet # sel tracks 0;jet # sel tracks 1", 50, 0, 50, 50, 0, 50);
    nd.book(k_nvtx, "nvtx", ";number of vertices;events/1", 8, 0, 8);
    nd.book(k_vtxbs2derr, "vtxbs2derr", ";bs2derr of vertex;events", 500, 0, 0.05);
    nd.book(k_vtxbs2derr_avgtkdr, "vtxbs2derr_avgtkdr", ";bs2derr of vertex; avg tk #Delta R", 100, 0, 0.025, 31, 0, M_PI);
    nd.book(k_vtxbs2derr_jdeta, "vtxbs2derr_jdeta", ";bs2derr of vertex; jet #Delta #eta", 100, 0, 0.025, 25, 0, 4);
    nd.book(k_vtxbs2derr_dphi_j0_mv, "vtxbs2derr_dphi_j0_mv", ";bs2derr of vertex;  #Delta #phi btwn j0 and MV", 100, 0, 0.025, 63, 0, M_PI);
    nd.book(k_vtxbs2derr_jdr, "vtxbs2derr_jdr", ";bs2derr of vertex; jet #Delta R", 100, 0, 0.025, 30, 0, 6);
    nd.book(k_vtxeta, "vtxeta", ";eta of vertex;events", 100, -4, 4);
    nd.book(k_vtxz, "vtxz", ";z pos of vertex;events", 100, -15, 15);
  }

  // JMTBAD some (all?) of these should be numdens
  TH1D* h_vtxdbv[num_numdens] = {0};
  TH1D* h_vtxntracks[num_numdens] = {0};
  TH1D* h_vtxbs2derr[num_numdens] = {0};
  //  TH1D* h_vtxtkonlymass[num_numdens] = {0};  // JMTBAD interface for vertex_tracks common to Mini2 and MovedTracks ntuples
  TH1D* h_vtxmass[num_numdens] = {0};
  TH1D* h_vtxanglemax[num_numdens] = {0};
  TH1D* h_vtxphi[num_numdens] = {0};
  TH1D* h_vtxeta[num_numdens] = {0};
  TH1D* h_vtxpt[num_numdens] = {0};
  TH2D* h_vtxbs2derr_v_vtxntracks[num_numdens] = {0};
  //  TH2D* h_vtxbs2derr_v_vtxtkonlymass[num_numdens] = {0};
  TH2D* h_vtxbs2derr_v_vtxanglemax[num_numdens] = {0};
  TH2D* h_vtxbs2derr_v_vtxphi[num_numdens] = {0};
  TH2D* h_vtxbs2derr_v_vtxeta[num_numdens] = {0};
  TH2D* h_vtxbs2derr_v_vtxpt[num_numdens] = {0};
  TH2D* h_vtxbs2derr_v_vtxdbv[num_numdens] = {0};
  TH2D* h_vtxbs2derr_v_etamovevec[num_numdens] = {0};
  TH2D* h_vtxbs2derr_v_maxtkerrdxy[num_numdens] = {0};

  TH1D* h_tks_pt[num_numdens] = {0};
  TH1D* h_tks_eta[num_numdens] = {0};
  TH1D* h_tks_phi[num_numdens] = {0};
  TH1D* h_tks_dxy[num_numdens] = {0};
  TH1D* h_tks_dz[num_numdens] = {0};
  TH1D* h_tks_err_pt[num_numdens] = {0};
  TH1D* h_tks_err_eta[num_numdens] = {0};
  TH1D* h_tks_err_phi[num_numdens] = {0};
  TH1D* h_tks_err_dxy[num_numdens] = {0};
  TH1D* h_tks_err_dz[num_numdens] = {0};
  TH1D* h_tks_nsigmadxy[num_numdens] = {0};
  TH1D* h_tks_npxlayers[num_numdens] = {0};
  TH1D* h_tks_nstlayers[num_numdens] = {0};

  TH1D* h_vtx_tks_pt[num_numdens] = {0};
  TH1D* h_vtx_tks_eta[num_numdens] = {0};
  TH1D* h_vtx_tks_phi[num_numdens] = {0};
  TH1D* h_vtx_tks_dxy[num_numdens] = {0};
  TH1D* h_vtx_tks_dz[num_numdens] = {0};
  TH1D* h_vtx_tks_err_pt[num_numdens] = {0};
  TH1D* h_vtx_tks_err_eta[num_numdens] = {0};
  TH1D* h_vtx_tks_err_phi[num_numdens] = {0};
  TH1D* h_vtx_tks_err_dxy[num_numdens] = {0};
  TH1D* h_vtx_tks_err_dz[num_numdens] = {0};
  TH1D* h_vtx_tks_nsigmadxy[num_numdens] = {0};
  TH1D* h_vtx_tks_npxlayers[num_numdens] = {0};
  TH1D* h_vtx_tks_nstlayers[num_numdens] = {0};

  TH1D* h_vtx_tks_nomove_pt[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_eta[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_phi[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_dxy[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_dz[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_err_pt[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_err_eta[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_err_phi[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_err_dxy[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_err_dz[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_nsigmadxy[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_npxlayers[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_nstlayers[num_numdens] = {0};
  
  TH1D* h_moved_tks_pt[num_numdens] = {0};
  TH1D* h_moved_tks_eta[num_numdens] = {0};
  TH1D* h_moved_tks_phi[num_numdens] = {0};
  TH1D* h_moved_tks_dxy[num_numdens] = {0};
  TH1D* h_moved_tks_dz[num_numdens] = {0};
  TH1D* h_moved_tks_err_pt[num_numdens] = {0};
  TH1D* h_moved_tks_err_eta[num_numdens] = {0};
  TH1D* h_moved_tks_err_phi[num_numdens] = {0};
  TH1D* h_moved_tks_err_dxy[num_numdens] = {0};
  TH1D* h_moved_tks_err_dz[num_numdens] = {0};
  TH1D* h_moved_tks_nsigmadxy[num_numdens] = {0};
  TH1D* h_moved_tks_npxlayers[num_numdens] = {0};
  TH1D* h_moved_tks_nstlayers[num_numdens] = {0};

  TH1D* h_moved_nosel_tks_pt[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_eta[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_phi[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_dxy[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_dz[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_err_pt[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_err_eta[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_err_phi[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_err_dxy[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_err_dz[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_nsigmadxy[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_npxlayers[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_nstlayers[num_numdens] = {0};

  for (int i = 0; i < num_numdens; ++i) {
    h_vtxdbv[i] = new TH1D(TString::Format("h_%i_vtxdbv", i), ";d_{BV} of largest vertex (cm);events/50 #mum", 400, 0, 2);
    h_vtxntracks[i] = new TH1D(TString::Format("h_%i_vtxntracks", i), ";# tracks in largest vertex;events/1", 60, 0, 60);
    h_vtxbs2derr[i] = new TH1D(TString::Format("h_%i_vtxbs2derr", i), ";#sigma(d_{BV}) of largest vertex (cm);events/1 #mum", 500, 0, 0.05);
    //    h_vtxtkonlymass[i] = new TH1D(TString::Format("h_%i_vtxtkonlymass", i), ";track-only mass of largest vertex (GeV);events/1 GeV", 50, 0, 500);
    h_vtxmass[i] = new TH1D(TString::Format("h_%i_vtxmass", i), ";track+jets mass of largest vertex (GeV);events/1 GeV", 100, 0, 5000);
    h_vtxanglemax[i] = new TH1D(TString::Format("h_%i_vtxanglemax", i), ";biggest angle between pairs of tracks in vertex;events/0.03", 100, 0, M_PI);
    h_vtxphi[i] = new TH1D(TString::Format("h_%i_vtxphi", i), ";tracks-plus-jets-by-ntracks #phi of largest vertex;events/0.06", 100, -M_PI, M_PI);
    h_vtxeta[i] = new TH1D(TString::Format("h_%i_vtxeta", i), ";tracks-plus-jets-by-ntracks #eta of largest vertex; events/0.03", 100, -4, 4);
    h_vtxpt[i] = new TH1D(TString::Format("h_%i_vtxpt", i), ";tracks-plus-jets-by-ntracks p_{T} of largest vertex (GeV);events/1", 500, 0, 500);

    h_vtxbs2derr_v_vtxntracks[i] = new TH2D(TString::Format("h_%i_vtxbs2derr_v_vtxntracks", i), ";# tracks in largest vertex;#sigma(d_{BV}) of largest vertex (cm)", 60, 0, 60, 500, 0, 0.05);
    //    h_vtxbs2derr_v_vtxtkonlymass[i] = new TH2D(TString::Format("h_%i_vtxbs2derr_v_vtxtkonlymass", i), ";track-only mass of largest vertex (GeV);#sigma(d_{BV}) of largest vertex (cm)", 500, 0, 500, 500, 0, 0.05);
    h_vtxbs2derr_v_vtxanglemax[i] = new TH2D(TString::Format("h_%i_vtxbs2derr_v_vtxanglemax", i), ";biggest angle between pairs of tracks in vertex;#sigma(d_{BV}) of largest vertex (cm)", 100, 0, M_PI, 500, 0, 0.05);
    h_vtxbs2derr_v_vtxphi[i] = new TH2D(TString::Format("h_%i_vtxbs2derr_v_vtxphi", i), ";tracks-plus-jets-by-ntracks #phi of largest vertex;#sigma(d_{BV}) of largest vertex (cm)", 100, -M_PI, M_PI, 500, 0, 0.05);
    h_vtxbs2derr_v_vtxeta[i] = new TH2D(TString::Format("h_%i_vtxbs2derr_v_vtxeta", i), ";tracks-plus-jets-by-ntracks #theta of largest vertex;#sigma(d_{BV}) of largest vertex (cm)", 100, 0, M_PI, 500, 0, 0.05);
    h_vtxbs2derr_v_vtxpt[i] = new TH2D(TString::Format("h_%i_vtxbs2derr_v_vtxpt", i), ";tracks-plus-jets-by-ntracks p_{T} of largest vertex (GeV);#sigma(d_{BV}) of largest vertex (cm)", 500, 0, 500, 500, 0, 0.05);
    h_vtxbs2derr_v_vtxdbv[i] = new TH2D(TString::Format("h_%i_vtxbs2derr_v_vtxdbv", i), ";d_{BV} of largest vertex (cm);#sigma(d_{BV}) of largest vertex (cm)", 400, 0, 2, 500, 0, 0.05);
    h_vtxbs2derr_v_etamovevec[i] = new TH2D(TString::Format("h_%i_vtxbs2derr_v_etamovevec", i), ";eta of move vector;#sigma(d_{BV}) of largest vertex (cm)", 100, -4, 4, 500, 0, 0.05);
    h_vtxbs2derr_v_maxtkerrdxy[i] = new TH2D(TString::Format("h_%i_vtxbs2derr_v_maxtkerrdxy", i), ";largest track #sigma(dxy) in largest vertex (cm);#sigma(d_{BV}) of largest vertex (cm)", 100, 0, 0.1, 500, 0, 0.05);

    h_tks_pt[i] = new TH1D(TString::Format("h_%i_tks_pt", i), ";moved and selected track p_{T} (GeV);tracks/1 GeV", 200, 0, 200);
    h_tks_eta[i] = new TH1D(TString::Format("h_%i_tks_eta", i), ";moved and selected track #eta;tracks/0.16", 50, -4, 4);
    h_tks_phi[i] = new TH1D(TString::Format("h_%i_tks_phi", i), ";moved and selected track #phi;tracks/0.13", 50, -M_PI, M_PI);
    h_tks_dxy[i] = new TH1D(TString::Format("h_%i_tks_dxy", i), ";moved and selected track dxy;tracks/40 #mum", 200, -0.8, 0.8);
    h_tks_dz[i] = new TH1D(TString::Format("h_%i_tks_dz", i), ";moved and selected track dz;tracks/100 #mum", 200, -1, 1);
    h_tks_err_pt[i] = new TH1D(TString::Format("h_%i_tks_err_pt", i), ";moved and selected track #sigma(p_{T});tracks/0.01", 200, 0, 2);
    h_tks_err_eta[i] = new TH1D(TString::Format("h_%i_tks_err_eta", i), ";moved and selected track #sigma(#eta);tracks/0.0001", 200, 0, 0.02);
    h_tks_err_phi[i] = new TH1D(TString::Format("h_%i_tks_err_phi", i), ";moved and selected track #sigma(#phi);tracks/0.0001", 200, 0, 0.02);
    h_tks_err_dxy[i] = new TH1D(TString::Format("h_%i_tks_err_dxy", i), ";moved and selected track #sigma(dxy) (cm);tracks/0.001 cm", 100, 0, 0.1);
    h_tks_err_dz[i] = new TH1D(TString::Format("h_%i_tks_err_dz", i), ";moved and selected track #sigma(dz) (cm);tracks/0.001 cm", 100, 0, 0.1);
    h_tks_nsigmadxy[i] = new TH1D(TString::Format("h_%i_tks_nsigmadxy", i), ";moved and selected track n#sigma(dxy);tracks/0.1", 200, 0, 20);
    h_tks_npxlayers[i] = new TH1D(TString::Format("h_%i_tks_npxlayers", i), ";moved and selected track npxlayers;tracks/1", 20, 0, 20);
    h_tks_nstlayers[i] = new TH1D(TString::Format("h_%i_tks_nstlayers", i), ";moved and selected track nstlayers;tracks/1", 20, 0, 20);

    h_vtx_tks_pt[i] = new TH1D(TString::Format("h_%i_vtx_tks_pt", i), ";track p_{T} in largest vertex (GeV);tracks/1 GeV", 200, 0, 200);
    h_vtx_tks_eta[i] = new TH1D(TString::Format("h_%i_vtx_tks_eta", i), ";track #eta in largest vertex;tracks/0.16", 50, -4, 4);
    h_vtx_tks_phi[i] = new TH1D(TString::Format("h_%i_vtx_tks_phi", i), ";track #phi in largest vertex;tracks/0.13", 50, -M_PI, M_PI);
    h_vtx_tks_dxy[i] = new TH1D(TString::Format("h_%i_vtx_tks_dxy", i), ";track dxy in largest vertex;tracks/40 #mum", 200, -0.8, 0.8);
    h_vtx_tks_dz[i] = new TH1D(TString::Format("h_%i_vtx_tks_dz", i), ";track dz in largest vertex;tracks/100 #mum", 200, -1, 1);
    h_vtx_tks_err_pt[i] = new TH1D(TString::Format("h_%i_vtx_tks_err_pt", i), ";track #sigma(p_{T}) in largest vertex;tracks/0.01", 200, 0, 2);
    h_vtx_tks_err_eta[i] = new TH1D(TString::Format("h_%i_vtx_tks_err_eta", i), ";track #sigma(#eta) in largest vertex;tracks/0.0001", 200, 0, 0.02);
    h_vtx_tks_err_phi[i] = new TH1D(TString::Format("h_%i_vtx_tks_err_phi", i), ";track #sigma(#phi) in largest vertex;tracks/0.0001", 200, 0, 0.02);
    h_vtx_tks_err_dxy[i] = new TH1D(TString::Format("h_%i_vtx_tks_err_dxy", i), ";track #sigma(dxy) (cm) in largest vertex;tracks/0.001 cm", 100, 0, 0.1);
    h_vtx_tks_err_dz[i] = new TH1D(TString::Format("h_%i_vtx_tks_err_dz", i), ";track #sigma(dz) (cm) in largest vertex;tracks/0.001 cm", 100, 0, 0.1);
    h_vtx_tks_nsigmadxy[i] = new TH1D(TString::Format("h_%i_vtx_tks_nsigmadxy", i), ";track n#sigma(dxy) in largest vertex;tracks/0.1", 200, 0, 20);
    h_vtx_tks_npxlayers[i] = new TH1D(TString::Format("h_%i_vtx_tks_npxlayers", i), ";track npxlayers in largest vertex;tracks/1", 20, 0, 20);
    h_vtx_tks_nstlayers[i] = new TH1D(TString::Format("h_%i_vtx_tks_nstlayers", i), ";track nstlayers in largest vertex;tracks/1", 20, 0, 20);

    h_vtx_tks_nomove_pt[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_pt", i), ";track p_{T} in largest vertex but not moved (GeV);tracks/1 GeV", 200, 0, 200);
    h_vtx_tks_nomove_eta[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_eta", i), ";track #eta in largest vertex but not moved;tracks/0.16", 50, -4, 4);
    h_vtx_tks_nomove_phi[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_phi", i), ";track #phi in largest vertex but not moved;tracks/0.13", 50, -M_PI, M_PI);
    h_vtx_tks_nomove_dxy[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_dxy", i), ";track dxy in largest vertex but not moved;tracks/40 #mum", 200, -0.4, 0.4);
    h_vtx_tks_nomove_dz[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_dz", i), ";track dz in largest vertex but not moved;tracks/100 #mum", 200, -1, 1);
    h_vtx_tks_nomove_err_pt[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_err_pt", i), ";track #sigma(p_{T}) in largest vertex but not moved;tracks/0.01", 200, 0, 2);
    h_vtx_tks_nomove_err_eta[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_err_eta", i), ";track #sigma(#eta) in largest vertex but not moved;tracks/0.0001", 200, 0, 0.02);
    h_vtx_tks_nomove_err_phi[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_err_phi", i), ";track #sigma(#phi) in largest vertex but not moved;tracks/0.0001", 200, 0, 0.02);
    h_vtx_tks_nomove_err_dxy[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_err_dxy", i), ";track #sigma(dxy) (cm) in largest vertex but not moved;tracks/0.001 cm", 100, 0, 0.1);
    h_vtx_tks_nomove_err_dz[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_err_dz", i), ";track #sigma(dz) (cm) in largest vertex but not moved;tracks/0.001 cm", 100, 0, 0.1);
    h_vtx_tks_nomove_nsigmadxy[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_nsigmadxy", i), ";track n#sigma(dxy) in largest vertex but not moved;tracks/0.1", 200, 0, 20);
    h_vtx_tks_nomove_npxlayers[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_npxlayers", i), ";track npxlayers in largest vertex but not moved;tracks/1", 20, 0, 20);
    h_vtx_tks_nomove_nstlayers[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_nstlayers", i), ";track nstlayers in largest vertex but not moved;tracks/1", 20, 0, 20);

    h_moved_tks_pt[i] = new TH1D(TString::Format("h_%i_moved_tks_pt", i), ";moved track p_{T} (GeV);tracks/1 GeV", 200, 0, 200);
    h_moved_tks_eta[i] = new TH1D(TString::Format("h_%i_moved_tks_eta", i), ";moved track #eta;tracks/0.16", 50, -4, 4);
    h_moved_tks_phi[i] = new TH1D(TString::Format("h_%i_moved_tks_phi", i), ";moved track #phi;tracks/0.13", 50, -M_PI, M_PI);
    h_moved_tks_dxy[i] = new TH1D(TString::Format("h_%i_moved_tks_dxy", i), ";moved track dxy;tracks/40 #mum", 200, -0.8, 0.8);
    h_moved_tks_dz[i] = new TH1D(TString::Format("h_%i_moved_tks_dz", i), ";moved track dz;tracks/100 #mum", 200, -1, 1);
    h_moved_tks_err_pt[i] = new TH1D(TString::Format("h_%i_moved_tks_err_pt", i), ";moved track #sigma(p_{T});tracks/0.01", 200, 0, 2);
    h_moved_tks_err_eta[i] = new TH1D(TString::Format("h_%i_moved_tks_err_eta", i), ";moved track #sigma(#eta);tracks/0.0001", 200, 0, 0.02);
    h_moved_tks_err_phi[i] = new TH1D(TString::Format("h_%i_moved_tks_err_phi", i), ";moved track #sigma(#phi);tracks/0.0001", 200, 0, 0.02);
    h_moved_tks_err_dxy[i] = new TH1D(TString::Format("h_%i_moved_tks_err_dxy", i), ";moved track #sigma(dxy) (cm);tracks/0.001 cm", 100, 0, 0.1);
    h_moved_tks_err_dz[i] = new TH1D(TString::Format("h_%i_moved_tks_err_dz", i), ";moved track #sigma(dz) (cm);tracks/0.001 cm", 100, 0, 0.1);
    h_moved_tks_nsigmadxy[i] = new TH1D(TString::Format("h_%i_moved_tks_nsigmadxy", i), ";moved track n#sigma(dxy);tracks/0.1", 200, 0, 20);
    h_moved_tks_npxlayers[i] = new TH1D(TString::Format("h_%i_moved_tks_npxlayers", i), ";moved track npxlayers;tracks/1", 20, 0, 20);
    h_moved_tks_nstlayers[i] = new TH1D(TString::Format("h_%i_moved_tks_nstlayers", i), ";moved track nstlayers;tracks/1", 20, 0, 20);

    h_moved_nosel_tks_pt[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_pt", i), ";moved but not selected track p_{T} (GeV);tracks/1 GeV", 200, 0, 200);
    h_moved_nosel_tks_eta[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_eta", i), ";moved but not selected track #eta;tracks/0.16", 50, -4, 4);
    h_moved_nosel_tks_phi[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_phi", i), ";moved but not selected track #phi;tracks/0.13", 50, -M_PI, M_PI);
    h_moved_nosel_tks_dxy[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_dxy", i), ";moved but not selected track dxy;tracks/40 #mum", 200, -0.8, 0.8);
    h_moved_nosel_tks_dz[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_dz", i), ";moved but not selected track dz;tracks/100 #mum", 200, -1, 1);
    h_moved_nosel_tks_err_pt[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_err_pt", i), ";moved but not selected track #sigma(p_{T});tracks/0.01", 200, 0, 2);
    h_moved_nosel_tks_err_eta[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_err_eta", i), ";moved but not selected track #sigma(#eta);tracks/0.0001", 200, 0, 0.02);
    h_moved_nosel_tks_err_phi[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_err_phi", i), ";moved but not selected track #sigma(#phi);tracks/0.0001", 200, 0, 0.02);
    h_moved_nosel_tks_err_dxy[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_err_dxy", i), ";moved but not selected track #sigma(dxy) (cm);tracks/0.001 cm", 100, 0, 0.1);
    h_moved_nosel_tks_err_dz[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_err_dz", i), ";moved but not selected track #sigma(dz) (cm);tracks/0.001 cm", 100, 0, 0.1);
    h_moved_nosel_tks_nsigmadxy[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_nsigmadxy", i), ";moved but not selected track n#sigma(dxy);tracks/0.1", 200, 0, 20);
    h_moved_nosel_tks_npxlayers[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_npxlayers", i), ";moved but not selected track npxlayers;tracks/1", 20, 0, 20);
    h_moved_nosel_tks_nstlayers[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_nstlayers", i), ";moved but not selected track nstlayers;tracks/1", 20, 0, 20);
  }


  std::map<std::string, double> nums;
  unsigned long long nden = 0, nnegden = 0;
  double den = 0, negden = 0;

  auto fcn = [&]() {
    double w = nr.weight();

    if (itau != 10000) {
      const double tau = nt.move_tau();
      const double tw = tau_weight(tau);
      h_tau->Fill(tau, tw);
      h_tau_tw->Fill(tau, tw, 1.0);
      w *= tw;
    }

    if (nr.use_weights()) {
      if (nr.is_mc() && btagsf_weights) {
        assert(0); // JMTBAD update for 2017+8, probably just the discriminator
        double p_mc = 1, p_data = 1;

        for (size_t i = 0, ie = jets.n(); i < ie; ++i) {
          const double pt = jets.pt(i);
          const double eta = jets.eta(i);
          const bool is_tagged = jets.bdisc(i) > 0.935;
          const int hf = jets.genflavor(i);

          const double sf = btagsfhelper->scale_factor(BTagSFHelper::BH, BTagSFHelper::tight, hf, eta, pt).v;
          const double e = btagsfhelper->efficiency(hf, eta, pt).v;
          assert(e > 0 && e <= 1);

          if (is_tagged) {
            p_mc   *= e;
            p_data *= e*sf;
          }
          else {
            p_mc   *= 1-e;
            p_data *= 1-e*sf;
          }
        }

        const double btagsfw = p_data / p_mc;
        h_btagsfweight->Fill(btagsfw);
        w *= btagsfw;
      }

      if (nr.is_mc() && use_extra_weights) {
        for (const auto& name : extra_weights_hists) {
          TH1D* hw = (TH1D*)extra_weights->Get(name.c_str());
          assert(hw);
          const double v =
            name == "nocuts_npv_den" ? pvs.n() :
            name == "nocuts_pvz_den" ? pvs.z(0) :
            name == "nocuts_pvx_den" ? pvs.x(0) :
            name == "nocuts_pvy_den" ? pvs.y(0) :
            name == "nocuts_nalltracks_den" ? nt.tm().nalltracks() :
            name == "nocuts_npv_den_redo" ? pvs.n() :
            name == "nocuts_ht_den" ? jets.ht() :
            name == "nocuts_pvndof_den" ? pvs.ndof(0) :
            -1e99;
          assert(v > -1e98);
          const int bin = hw->FindBin(v);
          if (bin >= 1 && bin <= hw->GetNbinsX())  
            w *= hw->GetBinContent(bin);
        }
      }
    }

    const TVector3& move_vector = nt.move_vector();
    const double movedist2 = move_vector.Perp();
    const double movedist3 = move_vector.Mag();
    const double movevectoreta = move_vector.Eta();
    const int nseedtracks = tks.nseed(bs);

    // First part of the preselection: our offline jet requirements
    // (mostly applied in ntupling step) plus only look at move
    // vectors ~inside the beampipe // JMTBAD the 2.0 cm requirement isn't exact
    if (movedist2 < 0.01 || movedist2 > 2.0) //FIXME
      NR_loop_cont(w);

	int nselmuons = 0;
	double muon_pT = -99;	     //muons.pt(i)
	double muon_abseta = -99;	 //abs(muons.eta(i))
	double muon_iso = 99;		 //muon.iso(i)
	double muon_absdxy = -99;	 //abs(muon.dxy(i))

	for (int i = 0, ie = muons.n(); i < ie; ++i) {
		if (muons.pt(i) > 29.0 && abs(muons.eta(i)) < 2.4 && muons.isMed(i) && muons.iso(i) < 0.15) {
			nselmuons += 1;
			muon_pT = muons.pt(i);
			muon_abseta = abs(muons.eta(i));
			muon_iso = muons.iso(i);
			muon_absdxy = abs(muons.dxy(i));
		}
	}

	int nseleles = 0;
	double ele_pT = -99;
	double ele_abseta = -99;
	double ele_iso = 99;
	double ele_absdxy = -99;

	for (int i = 0, ie = electrons.n(); i < ie; ++i) {
		if (electrons.pt(i) > 38.0 && abs(electrons.eta(i)) < 2.4 && electrons.isTight(i) && electrons.passveto(i) && electrons.iso(i) < 0.1) {
			nseleles += 1;
			ele_pT = electrons.pt(i);
			ele_abseta = abs(electrons.eta(i));
			ele_iso = electrons.iso(i);
			ele_absdxy = abs(electrons.dxy(i));
		}
	}


    int nmovedjets = 0, jet_sumntracks = 0;
    double jet_sume = 0;
    double jet_dravg = 0, jet_detaavg = 0, jet_dphiavg = 0;
    double jet_drmax = 0, jet_detamax = 0, jet_dphimax = 0;
    double jet_a3dmax = 0;
    int jet_i[2] = {-1,-1}; // keep track of the pair of jets with largest 3D angle // JMTBAD should this be largest phi?

    for (int i = 0, ie = jets.n(); i < ie; ++i) {
      if (!nt.jet_moved(i)) continue;
      const auto i_p4 = jets.p4(i);

      ++nmovedjets;
      jet_sume += jets.energy(i);
      jet_sumntracks += jets.ntracks(i);

      for (int j = i+1; j < ie; ++j) {
        if (!nt.jet_moved(j)) continue;
        const auto j_p4 = jets.p4(j);

        const double dr = i_p4.DeltaR(j_p4);
        const double deta = i_p4.Eta() - j_p4.Eta();
        const double dphi = i_p4.DeltaPhi(j_p4);
        jet_dravg += dr;
        jet_detaavg += deta; // JMTBAD should these be fabs'd
        jet_dphiavg += dphi;
        if (dr > jet_drmax)
          jet_drmax = dr;
        if (fabs(deta) > fabs(jet_detamax))
          jet_detamax = deta;
        if (fabs(dphi) > fabs(jet_dphimax))
          jet_dphimax = dphi;

        const double a3d = i_p4.Angle(j_p4.Vect());
        if (a3d > jet_a3dmax) {
          jet_a3dmax = a3d;
          jet_i[0] = i;
          jet_i[1] = j;
        }
      }
    }

    const int nmovedpairs = nmovedjets*(nmovedjets-1)/2;
    jet_detaavg /= nmovedpairs;
    jet_dphiavg /= nmovedpairs;
    jet_dravg /= nmovedpairs;

    std::vector<int> jet_tracks[2];
    int jet_ntracks[2] = {0};
    auto nps = [&](const int k) { return tks.pass_seed(k, bs); };
    int jet_nseedtracks[2] = {0};
    TLorentzVector jet_p4[2];
    double jet_max_trackpair_dr[2] = {0};
    double jet_avg_trackpair_dr[2] = {0};
    double jet_pt[2] = {0};
    double jet_eta[2] = {0};
    double jet_phi[2] = {0};
    double jet_p[2] = {0};
    double jet_mv_deta[2] = {0};
    double jet_mv_dphi[2] = {0};
    double jet_mv_a3d[2] = {0};

    for (int ii = 0; ii < 2; ++ii) {
      const int i = jet_i[ii];
      jet_tracks[ii] = tks.tks_for_jet(i);
      jet_ntracks[ii] = jets.ntracks(i);
      jet_nseedtracks[ii] = std::count_if(jet_tracks[ii].begin(), jet_tracks[ii].end(), nps);
      jet_pt[ii] = jets.pt(i);
      jet_eta[ii] = jets.eta(i);
      jet_phi[ii] = jets.phi(i);
      auto p4 = jet_p4[ii] = jets.p4(i);
      jet_p[ii] = jet_p4[ii].P();
      jet_mv_deta[ii] = fabs(move_vector.Eta() - p4.Eta());
      jet_mv_dphi[ii] = move_vector.DeltaPhi(p4.Vect());
      jet_mv_a3d[ii] = move_vector.Angle(p4.Vect());

      const int ntk = jet_tracks[ii].size();
      for (int j = 0; j < ntk; ++j)
        for (int k = j+1; k < ntk; ++k) {
          const double dr = tks.p3(jet_tracks[ii][j]).DeltaR(tks.p3(jet_tracks[ii][k]));
          jet_avg_trackpair_dr[ii] += dr;
          if (dr > jet_max_trackpair_dr[i])
            jet_max_trackpair_dr[ii] = dr;
        }
      jet_avg_trackpair_dr[ii] /= ntk*(ntk-1)/2;
    }

    const double jet_asymm = (jet_pt[0] - jet_pt[1]) / (jet_pt[0] + jet_pt[1]);
    const double jet_dr = jet_p4[0].DeltaR(jet_p4[1]);
	const double jet_dphi = jet_p4[0].DeltaPhi(jet_p4[1]);
	const double jet_deta = fabs(jet_p4[0].Eta() - jet_p4[1].Eta());
	const double jet_dind = fabs(jet_i[1] - jet_i[0]);
	const double jet_mv_dphi_sum = move_vector.DeltaPhi((jet_p4[0] + jet_p4[1]).Vect());
	const double jet_mv_deta_sum = fabs((jet_p4[0] + jet_p4[1]).Eta() - move_vector.Eta());

    const double jet_nseedtracks_max = std::max(jet_nseedtracks[0], jet_nseedtracks[1]);
    const double jet_nseedtracks_min = std::min(jet_nseedtracks[0], jet_nseedtracks[1]);
    const double jet_pt_max = std::max(jet_pt[0], jet_pt[1]);
    const double jet_pt_min = std::min(jet_pt[0], jet_pt[1]);

    // The rest of the preselection: signal-mocking cuts (only implemented for dijet truth case)
    //if ((jet_i[1] - jet_i[0]) > 3 || jet_pt[1] < 125 || jet_dr < 1.0) //FIXME
    //  NR_loop_cont(w);

    const int nvtx = vs.n();
    std::vector<double> vtxs_anglemax(nvtx, 0);

    for (int i = 0; i < nvtx; ++i) {
      const std::vector<int> tracks = tks.tks_for_sv(i);
      const int ntracks = int(tracks.size());
      assert(vs.ntracks(i) == ntracks);

      for (int j = 0; j < ntracks; ++j) {
        const TVector3 jp = tks.p3(tracks[j]);
        for (int k = j+1; k < ntracks; ++k) {
          const TVector3 kp = tks.p3(tracks[k]);
          const double angle = jp.Angle(kp); // JMTBAD probably should tighten cuts on tracks used for this
          if (angle > vtxs_anglemax[i])
            vtxs_anglemax[i] = angle;
        }
      }
    }

    int n_pass_nocuts = 0;
    int n_pass_ntracks = 0;
    int n_pass_all = 0;
	double dist2move = -9.9;

    double vtx_bs2derr = 0, vtx_eta = 0, vtx_z = 0; // JMTBAD ??? these end up with what???
    std::vector<int> first_vtx_to_pass(num_numdens, -1);
    auto set_it_if_first = [](int& to_set, int to_set_to) { if (to_set == -1) to_set = to_set_to; };

    for (int ivtx = 0; ivtx < nvtx; ++ivtx) {
      dist2move = (vs.pos(ivtx) - nt.tm().move_pos()).Mag();
      //if (dist2move > 0.0084) //FIXME 
        //continue;

      vtx_bs2derr = vs.bs2derr(ivtx); // JMTBAD ???
      vtx_eta     = vs.eta(ivtx);
      vtx_z       = vs.z(ivtx);

      const bool pass_ntracks = vs.ntracks(ivtx) >= 5;
      const bool pass_bs2derr = vs.bs2derr(ivtx) < 0.0050; // JMTBAD use rescale_bs2derr and in plots below //FIXME 

      if (1)                            { set_it_if_first(first_vtx_to_pass[0], ivtx); ++n_pass_nocuts;  }
      if (pass_ntracks)                 { set_it_if_first(first_vtx_to_pass[1], ivtx); ++n_pass_ntracks; }
      if (pass_ntracks && pass_bs2derr) { set_it_if_first(first_vtx_to_pass[2], ivtx); ++n_pass_all;     }

      if (pass_ntracks && pass_bs2derr && nr.is_mc() && nr.use_weights() && ntks_weights)
        w *= ntks_weight(vs.ntracks(ivtx));
    }

    // w now final and can count event toward denominator
    for (numdens& nd : nds)
      nd.setw(w);
    ++nden;
    den += w;
    if (w < 0) { ++nnegden; negden += w; }

    for (numdens& nd : nds) {
      nd.den(k_movedist2, movedist2);
      nd.den(k_movedist3, movedist3);
      nd.den(k_movevectoreta, movevectoreta);
      nd.den(k_npv, pvs.n());
      nd.den(k_pvx, pvs.x(0));
      nd.den(k_pvy, pvs.y(0));
      nd.den(k_pvz, pvs.z(0));
      nd.den(k_pvrho, pvs.rho(0));
      nd.den(k_pvntracks, pvs.ntracks(0));
      nd.den(k_pvscore, pvs.score(0));
      nd.den(k_ht, jets.ht());
	  nd.den(k_njets, jets.n());
	  nd.den(k_nmuons, nselmuons);
	  nd.den(k_muon_pT, muon_pT);
	  nd.den(k_muon_abseta, muon_abseta);
	  nd.den(k_muon_iso, muon_iso);
	  nd.den(k_muon_absdxy, muon_absdxy);
	  nd.den(k_neles, nseleles);
	  nd.den(k_ele_pT, ele_pT);
	  nd.den(k_ele_abseta, ele_abseta);
	  nd.den(k_ele_iso, ele_iso);
	  nd.den(k_ele_absdxy, ele_absdxy);
      nd.den(k_jet_asymm, jet_asymm);
	  nd.den(k_vtx_unc, dist2move);
	  nd.den(k_jet_dr, jet_dr);
	  nd.den(k_jet_deta, jet_deta);
	  nd.den(k_jet_dphi, jet_dphi);
	  nd.den(k_jet_dind, jet_dind);
	  nd.den(k_pt0, jet_pt[0]);
	  nd.den(k_pt1, jet_pt[1]);
	  nd.den(k_ntks_j0, jet_ntracks[0]);
	  nd.den(k_ntks_j1, jet_ntracks[1]);
	  nd.den(k_nmovedtracks, nt.tm().nmovedtracks());
	  nd.den(k_dphi_sum_j_mv, fabs(jet_mv_dphi_sum));
	  nd.den(k_deta_sum_j_mv, jet_mv_deta_sum);
	  nd.den(k_jetpt0_asymm, jet_pt_max, jet_asymm);
      nd.den(k_jetpt1_asymm, jet_pt_min, jet_asymm);
      nd.den(k_jeteta0_asymm, jet_eta[0], jet_asymm);
      nd.den(k_jeteta1_asymm, jet_eta[1], jet_asymm);
      nd.den(k_jetdr_asymm, jet_dr, jet_asymm);
      nd.den(k_nalltracks, nt.tm().nalltracks());
      nd.den(k_nseedtracks, nseedtracks);
      nd.den(k_npreseljets, nt.tm().npreseljets());
      nd.den(k_npreselbjets, nt.tm().npreselbjets());
      nd.den(k_jeti01, jet_i[0], jet_i[1]);
      nd.den(k_jetp01, jet_p[0], jet_p[1]);
      nd.den(k_jetpt01, jet_pt[0], jet_pt[1]);
      nd.den(k_jeteta01, jet_eta[0], jet_eta[1]);
      nd.den(k_jetphi01, jet_phi[0], jet_phi[1]);
      nd.den(k_jetsume, jet_sume);
      nd.den(k_jetdrmax, jet_drmax);
      nd.den(k_jetdravg, jet_dravg);
      nd.den(k_jetdetamax, jet_detamax);
      nd.den(k_jetdetaavg, jet_detaavg);
      nd.den(k_jetdphimax, jet_dphimax);
      nd.den(k_jetdphiavg, jet_dphiavg);
      nd.den(k_jet0_tkdrmax, jet_max_trackpair_dr[0]);
      nd.den(k_jet1_tkdrmax, jet_max_trackpair_dr[1]);
      nd.den(k_jet0_tkdravg, jet_avg_trackpair_dr[0]);
      nd.den(k_jet1_tkdravg, jet_avg_trackpair_dr[1]);
      nd.den(k_jet_dphi_deta_avg, jet_dphiavg, jet_detaavg);
      nd.den(k_jdphi_nmovedtks, fabs(jet_dphiavg), nt.tm().nmovedtracks());
      nd.den(k_jdeta_nmovedtks, fabs(jet_detaavg), nt.tm().nmovedtracks());
      nd.den(k_jdr_nmovedtks, jet_dravg,        nt.tm().nmovedtracks());
      nd.den(k_jtheta0_nmovedtks, jet_mv_a3d[0],  nt.tm().nmovedtracks());
      nd.den(k_jetmovea3d01, jet_mv_a3d[0], jet_mv_a3d[1]);
      nd.den(k_jetmovea3d_v_jetp, jet_p[0], jet_mv_a3d[0]);
      nd.den(k_jetmovea3d_v_jetp, jet_p[1], jet_mv_a3d[1]);
      nd.den(k_jetmovea3d0_v_movevectoreta, movevectoreta, jet_mv_a3d[0]);
      nd.den(k_jetmovea3d1_v_movevectoreta, movevectoreta, jet_mv_a3d[1]);
      nd.den(k_jeta3dmax, jet_a3dmax);
      nd.den(k_angle0, jet_mv_a3d[0]);
      nd.den(k_angle1, jet_mv_a3d[1]);
      nd.den(k_dphi_j0_mv, fabs(jet_mv_dphi[0]));
      nd.den(k_dphi_j1_mv, fabs(jet_mv_dphi[1]));
      nd.den(k_deta_j0_mv, fabs(jet_mv_deta[0]));
      nd.den(k_deta_j1_mv, fabs(jet_mv_deta[1]));
      nd.den(k_dphi_j0_mv_jdeta, fabs(jet_mv_dphi[0]), fabs(jet_detaavg));
      nd.den(k_jetsumntracks, jet_sumntracks);
      nd.den(k_jetntracks01, jet_ntracks[0], jet_ntracks[1]);
      nd.den(k_jetntracks_v_jetp, jet_p[0], jet_ntracks[0]);
      nd.den(k_jetntracks_v_jetp, jet_p[1], jet_ntracks[1]);
      nd.den(k_jetnseedtracks01, jet_nseedtracks_max, jet_nseedtracks_min);
      nd.den(k_nvtx, nvtx);
      nd.den(k_vtxbs2derr, vtx_bs2derr);
      nd.den(k_vtxbs2derr_avgtkdr, vtx_bs2derr, jet_avg_trackpair_dr[0]);
      nd.den(k_vtxbs2derr_jdeta, vtx_bs2derr, jet_detaavg);
      nd.den(k_vtxbs2derr_dphi_j0_mv, vtx_bs2derr, jet_mv_dphi[0]);
      nd.den(k_vtxbs2derr_jdr, vtx_bs2derr, jet_dravg);
      nd.den(k_vtxeta, vtx_eta);
      nd.den(k_vtxz, vtx_z);
    }

    for (int in = 0; in < num_numdens; ++in) {
      const int iv = first_vtx_to_pass[in];
      if (iv == -1)
        continue;

      const std::vector<int> its = tks.tks_for_sv(iv);
      jmt::MaxValue max_tk_err_dxy;
      for (int it : its) max_tk_err_dxy(tks.err_dxy(it));

      h_vtxdbv[in]->Fill(vs.rho(iv), w);
      h_vtxntracks[in]->Fill(vs.ntracks(iv), w);
      h_vtxbs2derr[in]->Fill(vs.bs2derr(iv), w);
      h_vtxanglemax[in]->Fill(vtxs_anglemax[iv], w);
      //      h_vtxtkonlymass[in]->Fill(vs.tkonlymass(iv), w);
      h_vtxmass[in]->Fill(vs.mass(iv), w);
      h_vtxphi[in]->Fill(vs.phi(iv), w);
      h_vtxeta[in]->Fill(vs.eta(iv), w);
      h_vtxpt[in]->Fill(vs.pt(iv), w);
      h_vtxbs2derr_v_vtxntracks[in]->Fill(vs.ntracks(iv), vs.bs2derr(iv), w);
      //      h_vtxbs2derr_v_vtxtkonlymass[in]->Fill(vs.tkonlymass(iv), vs.bs2derr(iv), w);
      h_vtxbs2derr_v_vtxanglemax[in]->Fill(vtxs_anglemax[iv], vs.bs2derr(iv), w);
      h_vtxbs2derr_v_vtxphi[in]->Fill(vs.phi(iv), vs.bs2derr(iv), w);
      h_vtxbs2derr_v_vtxeta[in]->Fill(vs.eta(iv), vs.bs2derr(iv), w);
      h_vtxbs2derr_v_vtxpt[in]->Fill(vs.pt(iv), vs.bs2derr(iv), w);
      h_vtxbs2derr_v_vtxdbv[in]->Fill(vs.rho(iv), vs.bs2derr(iv), w);
      h_vtxbs2derr_v_etamovevec[in]->Fill(move_vector.Eta(), vs.bs2derr(iv), w);

      h_vtxbs2derr_v_maxtkerrdxy[in]->Fill(max_tk_err_dxy, vs.bs2derr(iv), w);

      for (const int it : its) {
        h_vtx_tks_pt[in]->Fill(tks.pt(it), w);
        h_vtx_tks_eta[in]->Fill(tks.eta(it), w);
        h_vtx_tks_phi[in]->Fill(tks.phi(it), w);
        h_vtx_tks_dxy[in]->Fill(tks.dxybs(it, bs), w);
        h_vtx_tks_dz[in]->Fill(tks.dzpv(it, pvs), w);
        h_vtx_tks_err_pt[in]->Fill(tks.err_pt(it), w);
        h_vtx_tks_err_eta[in]->Fill(tks.err_eta(it), w);
        h_vtx_tks_err_phi[in]->Fill(tks.err_phi(it), w);
        h_vtx_tks_err_dxy[in]->Fill(tks.err_dxy(it), w); // JMTBAD this stored value is not the rescaled one
        h_vtx_tks_err_dz[in]->Fill(tks.err_dz(it), w);
        h_vtx_tks_nsigmadxy[in]->Fill(tks.nsigmadxybs(it, bs), w);
        h_vtx_tks_npxlayers[in]->Fill(tks.npxlayers(it), w);
        h_vtx_tks_nstlayers[in]->Fill(tks.nstlayers(it), w);

        if (!nt.tk_moved(it)) {
          h_vtx_tks_nomove_pt[in]->Fill(tks.pt(it), w);
          h_vtx_tks_nomove_eta[in]->Fill(tks.eta(it), w);
          h_vtx_tks_nomove_phi[in]->Fill(tks.phi(it), w);
          h_vtx_tks_nomove_dxy[in]->Fill(tks.dxybs(it, bs), w);
          h_vtx_tks_nomove_dz[in]->Fill(tks.dzpv(it, pvs), w);
          h_vtx_tks_nomove_err_pt[in]->Fill(tks.err_pt(it), w);
          h_vtx_tks_nomove_err_eta[in]->Fill(tks.err_eta(it), w);
          h_vtx_tks_nomove_err_phi[in]->Fill(tks.err_phi(it), w);
          h_vtx_tks_nomove_err_dxy[in]->Fill(tks.err_dxy(it), w);
          h_vtx_tks_nomove_err_dz[in]->Fill(tks.err_dz(it), w);
          h_vtx_tks_nomove_nsigmadxy[in]->Fill(tks.nsigmadxybs(it, bs), w);
          h_vtx_tks_nomove_npxlayers[in]->Fill(tks.npxlayers(it), w);
          h_vtx_tks_nomove_nstlayers[in]->Fill(tks.nstlayers(it), w);
        }
      }
    }

    if (n_pass_nocuts)  nums["nocuts"]  += w;
    if (n_pass_ntracks) nums["ntracks"] += w;
    if (n_pass_all)     nums["all"]     += w;

    const int npasses[num_numdens] = {
      n_pass_nocuts,
      n_pass_ntracks,
      n_pass_all
    };

    for (int i = 0; i < num_numdens; ++i) {
      if (!npasses[i]) continue;
      numdens& nd = nds[i];

      nd.num(k_movedist2, movedist2);
      nd.num(k_movedist3, movedist3);
      nd.num(k_movevectoreta, movevectoreta);
      nd.num(k_npv, pvs.n());
      nd.num(k_pvx, pvs.x(0));
      nd.num(k_pvy, pvs.y(0));
      nd.num(k_pvz, pvs.z(0));
      nd.num(k_pvrho, pvs.rho(0));
      nd.num(k_pvntracks, pvs.ntracks(0));
      nd.num(k_pvscore, pvs.score(0));
      nd.num(k_ht, jets.ht());
	  nd.num(k_njets, jets.n());
	  nd.num(k_nmuons, nselmuons);
	  nd.num(k_muon_pT, muon_pT);
	  nd.num(k_muon_abseta, muon_abseta);
	  nd.num(k_muon_iso, muon_iso);
	  nd.num(k_muon_absdxy, muon_absdxy);
	  nd.num(k_neles, nseleles);
	  nd.num(k_ele_pT, ele_pT);
	  nd.num(k_ele_abseta, ele_abseta);
	  nd.num(k_ele_iso, ele_iso);
	  nd.num(k_ele_absdxy, ele_absdxy);
      nd.num(k_jet_asymm, jet_asymm);
	  nd.num(k_vtx_unc, dist2move);
	  nd.num(k_jet_dr, jet_dr);
	  nd.num(k_jet_deta, jet_deta);
	  nd.num(k_jet_dphi, jet_dphi);
	  nd.num(k_jet_dind, jet_dind);
	  nd.num(k_pt0, jet_pt[0]);
	  nd.num(k_pt1, jet_pt[1]);
	  nd.num(k_ntks_j0, jet_ntracks[0]);
	  nd.num(k_ntks_j1, jet_ntracks[1]);
	  nd.num(k_nmovedtracks, nt.tm().nmovedtracks());
	  nd.num(k_dphi_sum_j_mv, fabs(jet_mv_dphi_sum));
	  nd.num(k_deta_sum_j_mv, jet_mv_deta_sum);
	  nd.num(k_jetpt0_asymm, jet_pt[0], jet_asymm);
      nd.num(k_jetpt1_asymm, jet_pt[1], jet_asymm);
      nd.num(k_jeteta0_asymm, jet_eta[0], jet_asymm);
      nd.num(k_jeteta1_asymm, jet_eta[1], jet_asymm);
      nd.num(k_jetdr_asymm, jet_dr, jet_asymm);
      nd.num(k_nalltracks, nt.tm().nalltracks());
      nd.num(k_nseedtracks, nseedtracks);
      nd.num(k_npreseljets, nt.tm().npreseljets());
      nd.num(k_npreselbjets, nt.tm().npreselbjets());
      nd.num(k_jeti01, jet_i[0], jet_i[1]);
      nd.num(k_jetp01, jet_p[0], jet_p[1]);
      nd.num(k_jetpt01, jet_pt[0], jet_pt[1]);
      nd.num(k_jeteta01, jet_eta[0], jet_eta[1]);
      nd.num(k_jetphi01, jet_phi[0], jet_phi[1]);
      nd.num(k_jetsume, jet_sume);
      nd.num(k_jetdrmax, jet_drmax);
      nd.num(k_jetdravg, jet_dravg);
      nd.num(k_jetdetamax, jet_detamax);
      nd.num(k_jetdetaavg, jet_detaavg);
      nd.num(k_jetdphimax, jet_dphimax);
      nd.num(k_jetdphiavg, jet_dphiavg);
      nd.num(k_jet0_tkdrmax, jet_max_trackpair_dr[0]);
      nd.num(k_jet1_tkdrmax, jet_max_trackpair_dr[1]);
      nd.num(k_jet0_tkdravg, jet_avg_trackpair_dr[0]);
      nd.num(k_jet1_tkdravg, jet_avg_trackpair_dr[1]);
      nd.num(k_jet_dphi_deta_avg, jet_dphiavg, jet_detaavg);
      nd.num(k_jdphi_nmovedtks, fabs(jet_dphiavg), nt.tm().nmovedtracks());
      nd.num(k_jdeta_nmovedtks, fabs(jet_detaavg), nt.tm().nmovedtracks());
      nd.num(k_jdr_nmovedtks, jet_dravg,        nt.tm().nmovedtracks());
      nd.num(k_jtheta0_nmovedtks, jet_mv_a3d[0],  nt.tm().nmovedtracks());
      nd.num(k_jetmovea3d01, jet_mv_a3d[0], jet_mv_a3d[1]);
      nd.num(k_jetmovea3d_v_jetp, jet_p[0], jet_mv_a3d[0]);
      nd.num(k_jetmovea3d_v_jetp, jet_p[1], jet_mv_a3d[1]);
      nd.num(k_jetmovea3d0_v_movevectoreta, movevectoreta, jet_mv_a3d[0]);
      nd.num(k_jetmovea3d1_v_movevectoreta, movevectoreta, jet_mv_a3d[1]);
      nd.num(k_jeta3dmax, jet_a3dmax);
      nd.num(k_angle0, jet_mv_a3d[0]);
      nd.num(k_angle1, jet_mv_a3d[1]);
      nd.num(k_dphi_j0_mv, fabs(jet_mv_dphi[0]));
      nd.num(k_dphi_j1_mv, fabs(jet_mv_dphi[1]));
      nd.num(k_deta_j0_mv, fabs(jet_mv_deta[0]));
      nd.num(k_deta_j1_mv, fabs(jet_mv_deta[1]));
      nd.num(k_dphi_j0_mv_jdeta, fabs(jet_mv_dphi[0]), fabs(jet_detaavg));
      nd.num(k_jetsumntracks, jet_sumntracks);
      nd.num(k_jetntracks01, jet_ntracks[0], jet_ntracks[1]);
      nd.num(k_jetntracks_v_jetp, jet_p[0], jet_ntracks[0]);
      nd.num(k_jetntracks_v_jetp, jet_p[1], jet_ntracks[1]);
      nd.num(k_jetnseedtracks01, jet_nseedtracks_max, jet_nseedtracks_min);
      nd.num(k_nvtx, npasses[i]);
      nd.num(k_vtxbs2derr, vtx_bs2derr);
      nd.num(k_vtxbs2derr_avgtkdr, vtx_bs2derr, jet_avg_trackpair_dr[0]);
      nd.num(k_vtxbs2derr_jdeta, vtx_bs2derr, jet_detaavg);
      nd.num(k_vtxbs2derr_dphi_j0_mv, vtx_bs2derr, jet_mv_dphi[0]);
      nd.num(k_vtxbs2derr_jdr, vtx_bs2derr, jet_dravg);
      nd.num(k_vtxeta, vtx_eta);
      nd.num(k_vtxz, vtx_z);

      for (size_t it = 0, ite = tks.n(); it < ite; ++it) {
        h_tks_pt[i]->Fill(tks.pt(it), w);
        h_tks_eta[i]->Fill(tks.eta(it), w);
        h_tks_phi[i]->Fill(tks.phi(it), w);
        h_tks_dxy[i]->Fill(tks.dxybs(it, bs), w);
        h_tks_dz[i]->Fill(tks.dzpv(it, pvs), w);
        h_tks_err_pt[i]->Fill(tks.err_pt(it), w);
        h_tks_err_eta[i]->Fill(tks.err_eta(it), w);
        h_tks_err_phi[i]->Fill(tks.err_phi(it), w);
        h_tks_err_dxy[i]->Fill(tks.err_dxy(it), w);
        h_tks_err_dz[i]->Fill(tks.err_dz(it), w);
        h_tks_nsigmadxy[i]->Fill(tks.nsigmadxybs(it, bs), w);
        h_tks_npxlayers[i]->Fill(tks.npxlayers(it), w);
        h_tks_nstlayers[i]->Fill(tks.nstlayers(it), w);

        if (nt.tk_moved(it)) {
          h_moved_tks_pt[i]->Fill(tks.pt(it), w);
          h_moved_tks_eta[i]->Fill(tks.eta(it), w);
          h_moved_tks_phi[i]->Fill(tks.phi(it), w);
          h_moved_tks_dxy[i]->Fill(tks.dxybs(it, bs), w);
          h_moved_tks_dz[i]->Fill(tks.dzpv(it, pvs), w);
          h_moved_tks_err_pt[i]->Fill(tks.err_pt(it), w);
          h_moved_tks_err_eta[i]->Fill(tks.err_eta(it), w);
          h_moved_tks_err_phi[i]->Fill(tks.err_phi(it), w);
          h_moved_tks_err_dxy[i]->Fill(tks.err_dxy(it), w);
          h_moved_tks_err_dz[i]->Fill(tks.err_dz(it), w);
          h_moved_tks_nsigmadxy[i]->Fill(tks.nsigmadxybs(it, bs), w);
          h_moved_tks_npxlayers[i]->Fill(tks.npxlayers(it), w);
          h_moved_tks_nstlayers[i]->Fill(tks.nstlayers(it), w);

          if (!tks.pass_seed(it, bs)) {
            h_moved_nosel_tks_pt[i]->Fill(tks.pt(it), w);
            h_moved_nosel_tks_eta[i]->Fill(tks.eta(it), w);
            h_moved_nosel_tks_phi[i]->Fill(tks.phi(it), w);
            h_moved_nosel_tks_dxy[i]->Fill(tks.dxybs(it, bs), w);
            h_moved_nosel_tks_dz[i]->Fill(tks.dzpv(it, pvs), w);
            h_moved_nosel_tks_err_pt[i]->Fill(tks.err_pt(it), w);
            h_moved_nosel_tks_err_eta[i]->Fill(tks.err_eta(it), w);
            h_moved_nosel_tks_err_phi[i]->Fill(tks.err_phi(it), w);
            h_moved_nosel_tks_err_dxy[i]->Fill(tks.err_dxy(it), w);
            h_moved_nosel_tks_err_dz[i]->Fill(tks.err_dz(it), w);
            h_moved_nosel_tks_nsigmadxy[i]->Fill(tks.nsigmadxybs(it, bs), w);
            h_moved_nosel_tks_npxlayers[i]->Fill(tks.npxlayers(it), w);
            h_moved_nosel_tks_nstlayers[i]->Fill(tks.nstlayers(it), w);
          }
        }
      }
    }

    NR_loop_cont(w);
  };

  nr.loop(fcn);

  printf("%llu/%llu = %.1f/%.1f denominator events with negative weights\n", nnegden, nden, negden, den);
  printf("%20s  %12s  %12s  %10s [%10s, %10s] +%10s -%10s\n", "name", "num", "den", "eff", "lo", "hi", "+", "-");
  for (const auto& p : nums) {
    const jmt::interval i = jmt::clopper_pearson_binom(p.second, den);
    printf("%20s  %12.1f  %12.1f  %10.4f [%10.4f, %10.4f] +%10.4f -%10.4f\n", p.first.c_str(), p.second, den, i.value, i.lower, i.upper, i.upper - i.value, i.value - i.lower);
  }
}
