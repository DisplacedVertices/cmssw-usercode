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
  nr.init_options("mfvMovedTree20/t")
    ("tau",           po::value<int>   (&itau)          ->default_value(10000),   "tau in microns, for reweighting")
    ("btagsf",        po::value<bool>  (&btagsf_weights)->default_value(false),   "whether to use b-tag SF weights")
    ("ntks-weights",  po::value<bool>  (&ntks_weights)  ->default_value(false),   "whether to use ntracks weights")
    ;

  if (!nr.parse_options(argc, argv)) return 1;
  std::cout << " tau: " << itau << " btagsf: " << btagsf_weights << " ntks_weights: " << ntks_weights << "\n";

  if (!nr.init()) return 1;
  auto& nt = nr.nt();

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
  TH1D* h_btagsfweight = new TH1D("h_btagsfweight", ";weight;events/0.01", 200, 0, 2);

  const int num_numdens = 3;
  numdens nds[num_numdens] = {
    numdens("nocuts"),
    numdens("ntracks"),
    numdens("all")
  };

  enum { k_movedist2, k_movedist3, k_movevectoreta, k_npv, k_pvx, k_pvy, k_pvz, k_pvrho, k_pvntracks, k_pvscore, k_ht, k_jet_asymm, k_jetpt0_asymm, k_jetpt1_asymm, k_jeteta0_asymm, k_jeteta1_asymm, k_jetdr_asymm, k_nalltracks, k_nmovedtracks, k_nseedtracks, k_npreseljets, k_npreselbjets, k_jeti01, k_jetp01, k_pt0, k_pt1, k_jetpt01, k_jeteta01, k_jetphi01, k_jetsume, k_jetdrmax, k_jetdravg, k_jetdetamax, k_jetdetaavg, k_jetdphimax, k_jetdphiavg, k_jet0_tkdrmax, k_jet1_tkdrmax, k_jet0_tkdravg, k_jet1_tkdravg, k_jet_dphi_deta_avg, k_jdphi_nmovedtks, k_jdeta_nmovedtks, k_jdr_nmovedtks, k_jtheta0_nmovedtks, k_jetmovea3d01, k_jetmovea3d_v_jetp, k_jetmovea3d0_v_movevectoreta, k_jetmovea3d1_v_movevectoreta, k_jeta3dmax, k_angle0, k_angle1, k_dphi_j0_mv, k_dphi_j1_mv, k_deta_j0_mv, k_deta_j1_mv, k_dphi_j0_mv_jdeta, k_jetsumntracks, k_jetntracks01, k_jetntracks_v_jetp, k_jetnseedtracks01, k_nvtx, k_vtxbs2derr, k_vtxbs2derr_avgtkdr, k_vtxbs2derr_jdeta, k_vtxbs2derr_dphi_j0_mv, k_vtxbs2derr_jdr, k_vtxeta, k_vtxz };

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
    nd.book(k_ht, "ht", ";H_{T} (GeV);events/50 GeV", 50, 0, 2500);
    nd.book(k_jet_asymm, "jet_asymm", ";Jet asymmetry A_{J}; arb. units", 25, 0, 1);

    nd.book(k_jetpt0_asymm, "jetpt0_asymm", ";jet p_{T} 0; jet asymm. A_{J}", 50, 0, 1000, 25, 0, 1);
    nd.book(k_jetpt1_asymm, "jetpt1_asymm", ";jet p_{T} 1; jet asymm. A_{J}", 50, 0, 1000, 25, 0, 1);
    nd.book(k_jeteta0_asymm, "jeteta0_asymm", ";jet #eta 0; jet asymm. A_{J}", 100, -4, 4, 25, 0, 1);
    nd.book(k_jeteta1_asymm, "jeteta1_asymm", ";jet #eta 1; jet asymm. A_{J}", 100, -4, 4, 25, 0, 1);
    nd.book(k_jetdr_asymm, "jetdr_asymm", ";jets #DeltaR; jet asymm. A_{J}", 70, 0, 7, 25, 0, 1);
    nd.book(k_nalltracks, "nalltracks", ";# all tracks;events/10", 200, 0, 2000);
    nd.book(k_nmovedtracks, "nmovedtracks", ";# moved tracks;events/2", 120, 0, 120);
    nd.book(k_nseedtracks, "nseedtracks", ";# selected tracks;events", 80, 0, 80);
    nd.book(k_npreseljets, "npreseljets", ";# preselected jets;events/1", 20, 0, 20);
    nd.book(k_npreselbjets, "npreselbjets", ";# preselected b jets;events/1", 20, 0, 20);
    nd.book(k_jeti01, "jeti01", ";jet i 0 (GeV);jet i 1 (GeV);events", 15, 0, 15, 15, 0, 15);
    nd.book(k_jetp01, "jetp01", ";jet 0 momentum (GeV);jet 1 momentum (GeV)", 200, 0, 2000, 200, 0, 2000);
    nd.book(k_jetpt01, "jetpt01", ";jet p_{T} 0 (GeV);jet p_{T} 1 (GeV)", 50, 0, 1000, 50, 0, 1000);
    nd.book(k_pt0,     "pt0",     ";Pt of jet0 [GeV]", 50, 0, 1000);
    nd.book(k_pt1,     "pt1",     ";Pt of jet1 [GeV]", 50, 0, 1000);
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
      w *= tw;
    }

    if (nr.use_weights()) {
      if (nr.is_mc() && btagsf_weights) {
        double p_mc = 1, p_data = 1;

        for (size_t i = 0, ie = nt.jets().n(); i < ie; ++i) {
          const double pt = nt.jets().pt(i);
          const double eta = nt.jets().eta(i);
          const bool is_tagged = nt.jets().bdisc(i) > 0.935; // what ever
          const int hf = nt.jets().genflavor(i);

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
            name == "nocuts_npv_den" ? nt.pvs().n() :
            name == "nocuts_pvz_den" ? nt.pvs().z(0) :
            name == "nocuts_pvx_den" ? nt.pvs().x(0) :
            name == "nocuts_pvy_den" ? nt.pvs().y(0) :
            name == "nocuts_nalltracks_den" ? nt.tm().nalltracks() :
            name == "nocuts_npv_den_redo" ? nt.pvs().n() :
            name == "nocuts_ht_den" ? nt.jets().ht() :
            name == "nocuts_pvndof_den" ? nt.pvs().ndof(0) :
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

    if (nt.jets().ht() < 1200 || 
        nt.jets().nminpt() < 4 ||
        movedist2 < 0.01 ||
        movedist2 > 2.0) {
      return std::make_pair(true, w);
    }

    double jet_sume = 0;
    double jet_drmax = 0;
    double jet_dravg = 0;
    double jet_detamax = 0;
    double jet_detaavg = 0;
    double jet_dphimax = 0;
    double jet_dphiavg = 0;
    double max_dr_0 = 0.0, max_dr_1 = 0.0;
    double avg_dr_0 = 0.0, avg_dr_1 = 0.0;
    double jet_a3dmax = 0;
    double jet_sumntracks = 0;
    int jet_i_0 = -1, jet_i_1 = -1;
    double jet_p_0 = 0, jet_p_1 = 0;
    double jet_pt_0 = 0, jet_pt_1 = 0;
    double jet_eta_0 = 0, jet_eta_1 = 0;
    double jet_phi_0 = 0, jet_phi_1 = 0;
    double jet_asymm = 0;
    double jet_dr = 0;
    double jet_move_a3d_0 = 0, jet_move_a3d_1 = 0;
    double jet_mv_dphi_0  = 0.0, jet_mv_dphi_1 = 0.0;
    double jet_mv_deta_0  = 0.0, jet_mv_deta_1 = 0.0;
    int jet_ntracks_0 = 0, jet_ntracks_1 = 0;
    int jet_nseedtracks_0 = 0, jet_nseedtracks_1 = 0;
    size_t nmovedjets = 0;
    double vtx_bs2derr = 0.0, vtx_eta = 0.0, vtx_z = 0.0;


    for (int i = 0, ie = nt.jets().n(); i < ie; ++i) {
      if (!nt.jet_moved(i))
        continue;


      const auto i_p4 = nt.jets().p4(i);
      const auto i_tracks = nt.tracks().tks_for_jet(i);

      ++nmovedjets;
      jet_sume += nt.jets().energy(i);
      jet_sumntracks += nt.jets().ntracks(i);


      for (int j = i+1; j < ie; ++j) {
        if (!nt.jet_moved(j))
          continue;

        const auto j_p4 = nt.jets().p4(j);

        const double dr = i_p4.DeltaR(j_p4);
        const double dphi = i_p4.DeltaPhi(j_p4);
        const double deta = i_p4.Eta() - j_p4.Eta();

        const double a3d = i_p4.Angle(j_p4.Vect());

        jet_dravg += dr;
        jet_detaavg += deta;
        jet_dphiavg += dphi;


        if (dr > jet_drmax)
          jet_drmax = dr;
        if (abs(deta) > abs(jet_detamax))
          jet_detamax = deta;
        if (abs(dphi) > abs(jet_dphimax))
          jet_dphimax = dphi;

        if (a3d > jet_a3dmax) {
          const auto j_tracks = nt.tracks().tks_for_jet(j);

          for (int k=0, ke=i_tracks.size()-1; k < ke; k++) {
             for (int l=0, le=i_tracks.size(); l < le; l++) {
                double eta_k = nt.tracks().eta(i_tracks[k]), eta_l = nt.tracks().eta(i_tracks[l]);
                double phi_k = nt.tracks().phi(i_tracks[k]), phi_l = nt.tracks().phi(i_tracks[l]);
                double dR = hypot(eta_k - eta_l, phi_k - phi_l);
                avg_dr_0 += dR;
                if (dR > max_dr_0) max_dr_0 = dR;
             }
          }
          avg_dr_0 /= ((i_tracks.size()-1)*i_tracks.size());

          for (int k=0, ke=j_tracks.size()-1; k < ke; k++) {
             for (int l=0, le=j_tracks.size(); l < le; l++) {
                double eta_k = nt.tracks().eta(j_tracks[k]), eta_l = nt.tracks().eta(j_tracks[l]);
                double phi_k = nt.tracks().phi(j_tracks[k]), phi_l = nt.tracks().phi(j_tracks[l]);
                double dR = hypot(eta_k - eta_l, phi_k - phi_l);
                avg_dr_1 += dR;
                if (dR > max_dr_1) max_dr_1 = dR;
             }
          }
          avg_dr_1 /= ((j_tracks.size()-1)*j_tracks.size());

          auto nps = [&nt](const int k) { return nt.tracks().pass_seed(k, nt.bs()); };
          const int i_nseedtracks = std::count_if(i_tracks.begin(), i_tracks.end(), nps);
          const int j_nseedtracks = std::count_if(j_tracks.begin(), j_tracks.end(), nps);


          jet_a3dmax = a3d;
          jet_i_0 = i;
          jet_i_1 = j;
          jet_pt_0 = std::max(nt.jets().pt(i), nt.jets().pt(j));
          jet_pt_1 = std::min(nt.jets().pt(i), nt.jets().pt(j));
          jet_nseedtracks_0 = std::max(i_nseedtracks, j_nseedtracks);
          jet_nseedtracks_1 = std::min(i_nseedtracks, j_nseedtracks);
          jet_p_0 = i_p4.P();
          jet_p_1 = j_p4.P();
          jet_asymm = (jet_pt_0 - jet_pt_1) / (jet_pt_0 + jet_pt_1);
          jet_dr    = dr;
          jet_ntracks_0 = nt.jets().ntracks(i);
          jet_ntracks_1 = nt.jets().ntracks(j);
	      jet_move_a3d_0 = move_vector.Angle(i_p4.Vect());
	      jet_move_a3d_1 = move_vector.Angle(j_p4.Vect());
          jet_mv_dphi_0  = move_vector.DeltaPhi(i_p4.Vect());
          jet_mv_dphi_1  = move_vector.DeltaPhi(j_p4.Vect());
          jet_mv_deta_0  = abs(move_vector.Eta() - i_p4.Eta());
          jet_mv_deta_1  = abs(move_vector.Eta() - j_p4.Eta());
          jet_eta_0 = i_p4.Eta();
          jet_eta_1 = j_p4.Eta();
          jet_phi_0 = i_p4.Phi();
          jet_phi_1 = j_p4.Phi();


        }
      }
    }
    jet_dravg /= nmovedjets * (nmovedjets - 1) / 2.;
    jet_detaavg /= nmovedjets * (nmovedjets - 1) / 2.;
    jet_dphiavg /= nmovedjets * (nmovedjets - 1) / 2.;

    int nseedtracks = 0;
    for (int i = 0, ie = nt.tracks().n(); i < ie; ++i)
      if (nt.tracks().pass_seed(i, nt.bs()))
        ++nseedtracks;


    const int nvtx = nt.vertices().n();
    std::vector<double> vtxs_anglemax(nvtx, 0);

    for (int i = 0; i < nvtx; ++i) {
      const std::vector<int> tracks = nt.tracks().tks_for_sv(i);
      const int ntracks = int(tracks.size());
      assert(nt.vertices().ntracks(i) == ntracks);

      for (int j = 0; j < ntracks; ++j) {
        const TVector3 jp = nt.tracks().p3(tracks[j]);
        for (int k = j+1; k < ntracks; ++k) {
          const TVector3 kp = nt.tracks().p3(tracks[k]);
          const double angle = jp.Angle(kp); // JMTBAD probably should tighten cuts on tracks used for this
          if (angle > vtxs_anglemax[i])
            vtxs_anglemax[i] = angle;
        }
      }
    }

    int n_pass_nocuts = 0;
    int n_pass_ntracks = 0;
    int n_pass_all = 0;

    std::vector<int> first_vtx_to_pass(num_numdens, -1);
    auto set_it_if_first = [](int& to_set, int to_set_to) { if (to_set == -1) to_set = to_set_to; };

    for (int ivtx = 0; ivtx < nvtx; ++ivtx) {
      const double dist2move = (nt.vertices().pos(ivtx) - nt.tm().move_pos()).Mag();
      if (dist2move > 0.0084)
        continue;

      //Signal-mocking cuts
      if ((jet_i_1 - jet_i_0) > 3) continue;
      if (jet_pt_1 < 125) continue;
      if (jet_dr < 1.0) continue;
       
      vtx_bs2derr = nt.vertices().bs2derr(ivtx);
      vtx_eta     = nt.vertices().eta(ivtx);
      vtx_z       = nt.vertices().z(ivtx);

      const bool pass_ntracks = nt.vertices().ntracks(ivtx) >= 5;
      const bool pass_bs2derr = nt.vertices().bs2derr(ivtx) < 0.0025;

      if (1)                            { set_it_if_first(first_vtx_to_pass[0], ivtx); ++n_pass_nocuts;  }
      if (pass_ntracks)                 { set_it_if_first(first_vtx_to_pass[1], ivtx); ++n_pass_ntracks; }
      if (pass_ntracks && pass_bs2derr) { set_it_if_first(first_vtx_to_pass[2], ivtx); ++n_pass_all;     }

      if (pass_ntracks && pass_bs2derr && nr.is_mc() && nr.use_weights() && ntks_weights)
        w *= ntks_weight(nt.vertices().ntracks(ivtx));
    }

    auto F1 = [&w](TH1* h, double v)            { h                    ->Fill(v,     w); };
    auto F2 = [&w](TH1* h, double v, double v2) { dynamic_cast<TH2*>(h)->Fill(v, v2, w); };


    // JMTBAD why multiple dens?
    for (numdens& nd : nds) {

      //Signal-mocking cuts
      if ((jet_i_1 - jet_i_0) > 3) continue;
      if (jet_pt_1 < 125) continue;
      if (jet_dr < 1.0) continue;

      F1(nd(k_movedist2)        .den, movedist2);
      F1(nd(k_movedist3)        .den, movedist3);
      F1(nd(k_movevectoreta)    .den, movevectoreta);
      F1(nd(k_npv)              .den, nt.pvs().n());
      F1(nd(k_pvx)              .den, nt.pvs().x(0));
      F1(nd(k_pvy)              .den, nt.pvs().y(0));
      F1(nd(k_pvz)              .den, nt.pvs().z(0));
      F1(nd(k_pvrho)            .den, nt.pvs().rho(0));
      F1(nd(k_pvntracks)        .den, nt.pvs().ntracks(0));
      F1(nd(k_pvscore)          .den, nt.pvs().score(0));
      F1(nd(k_ht)               .den, nt.jets().ht());
      F1(nd(k_jet_asymm)        .den, jet_asymm);
      F2(nd(k_jetpt0_asymm)     .den, jet_pt_0, jet_asymm);
      F2(nd(k_jetpt1_asymm)     .den, jet_pt_1, jet_asymm);
      F2(nd(k_jeteta0_asymm)    .den, jet_eta_0, jet_asymm);
      F2(nd(k_jeteta1_asymm)    .den, jet_eta_1, jet_asymm);
      F2(nd(k_jetdr_asymm)      .den, jet_dr, jet_asymm);
      F1(nd(k_nalltracks)       .den, nt.tm().nalltracks());
      F1(nd(k_nmovedtracks)     .den, nt.tm().nmovedtracks());
      F1(nd(k_nseedtracks)      .den, nseedtracks);
      F1(nd(k_npreseljets)      .den, nt.tm().npreseljets());
      F1(nd(k_npreselbjets)     .den, nt.tm().npreselbjets());
      F2(nd(k_jeti01)           .den, jet_i_0, jet_i_1);
      F2(nd(k_jetp01)           .den, jet_p_0, jet_p_1);
      F2(nd(k_jetpt01)          .den, jet_pt_0, jet_pt_1);
      F1(nd(k_pt0)              .den, jet_pt_0);
      F1(nd(k_pt1)              .den, jet_pt_1);
      F2(nd(k_jeteta01)         .den, jet_eta_0, jet_eta_1);
      F2(nd(k_jetphi01)         .den, jet_phi_0, jet_phi_1);
      F1(nd(k_jetsume)          .den, jet_sume);
      F1(nd(k_jetdrmax)         .den, jet_drmax);
      F1(nd(k_jetdravg)         .den, jet_dravg);
      F1(nd(k_jetdetamax)       .den, jet_detamax);
      F1(nd(k_jetdetaavg)       .den, jet_detaavg);
      F1(nd(k_jetdphimax)       .den, jet_dphimax);
      F1(nd(k_jetdphiavg)       .den, jet_dphiavg);
      F1(nd(k_jet0_tkdrmax)     .den, max_dr_0);
      F1(nd(k_jet1_tkdrmax)     .den, max_dr_1);
      F1(nd(k_jet0_tkdravg)     .den, avg_dr_0);
      F1(nd(k_jet1_tkdravg)     .den, avg_dr_1);
      F2(nd(k_jet_dphi_deta_avg).den, jet_dphiavg, jet_detaavg);
      F2(nd(k_jdphi_nmovedtks)  .den, abs(jet_dphiavg), nt.tm().nmovedtracks());
      F2(nd(k_jdeta_nmovedtks)  .den, abs(jet_detaavg), nt.tm().nmovedtracks());
      F2(nd(k_jdr_nmovedtks)    .den, jet_dravg,        nt.tm().nmovedtracks());
      F2(nd(k_jtheta0_nmovedtks).den, jet_move_a3d_0,  nt.tm().nmovedtracks());
      F2(nd(k_jetmovea3d01)     .den, jet_move_a3d_0, jet_move_a3d_1);
      F2(nd(k_jetmovea3d_v_jetp).den, jet_p_0, jet_move_a3d_0);
      F2(nd(k_jetmovea3d_v_jetp).den, jet_p_1, jet_move_a3d_1);
      F2(nd(k_jetmovea3d0_v_movevectoreta).den, movevectoreta, jet_move_a3d_0);
      F2(nd(k_jetmovea3d1_v_movevectoreta).den, movevectoreta, jet_move_a3d_1);
      F1(nd(k_jeta3dmax)        .den, jet_a3dmax);
      F1(nd(k_angle0)           .den, jet_move_a3d_0);
      F1(nd(k_angle1)           .den, jet_move_a3d_1);
      F1(nd(k_dphi_j0_mv)       .den, abs(jet_mv_dphi_0));
      F1(nd(k_dphi_j1_mv)       .den, abs(jet_mv_dphi_1));
      F1(nd(k_deta_j0_mv)       .den, abs(jet_mv_deta_0));
      F1(nd(k_deta_j1_mv)       .den, abs(jet_mv_deta_1));
      F2(nd(k_dphi_j0_mv_jdeta) .den, abs(jet_mv_dphi_0), abs(jet_detaavg));
      F1(nd(k_jetsumntracks)    .den, jet_sumntracks);
      F2(nd(k_jetntracks01)     .den, jet_ntracks_0, jet_ntracks_1);
      F2(nd(k_jetntracks_v_jetp).den, jet_p_0, jet_ntracks_0);
      F2(nd(k_jetntracks_v_jetp).den, jet_p_1, jet_ntracks_1);
      F2(nd(k_jetnseedtracks01) .den, jet_nseedtracks_0, jet_nseedtracks_1);
      F1(nd(k_nvtx)             .den, nvtx);
      F1(nd(k_vtxbs2derr)       .den, vtx_bs2derr);
      F2(nd(k_vtxbs2derr_avgtkdr)    .den, vtx_bs2derr, avg_dr_0);
      F2(nd(k_vtxbs2derr_jdeta)      .den, vtx_bs2derr, jet_detaavg);
      F2(nd(k_vtxbs2derr_dphi_j0_mv) .den, vtx_bs2derr, jet_mv_dphi_0);
      F2(nd(k_vtxbs2derr_jdr)        .den, vtx_bs2derr, jet_dravg);
      F1(nd(k_vtxeta)           .den, vtx_eta);
      F1(nd(k_vtxz)             .den, vtx_z);
    }

    ++nden;
    den += w;
    if (w < 0) { ++nnegden; negden += w; }

    for (int in = 0; in < num_numdens; ++in) {
      const int iv = first_vtx_to_pass[in];
      if (iv == -1)
        continue;

      const std::vector<int> its = nt.tracks().tks_for_sv(iv);
      const float max_tk_err_dxy = nt.tracks().err_dxy(*std::max_element(its.begin(), its.end(), [&nt](const int ia, const int ib) { return nt.tracks().err_dxy(ia) < nt.tracks().err_dxy(ib); }));

      h_vtxdbv[in]->Fill(nt.vertices().rho(iv), w);
      h_vtxntracks[in]->Fill(nt.vertices().ntracks(iv), w);
      h_vtxbs2derr[in]->Fill(nt.vertices().bs2derr(iv), w);
      h_vtxanglemax[in]->Fill(vtxs_anglemax[iv], w);
      //      h_vtxtkonlymass[in]->Fill(nt.vertices().tkonlymass(iv), w);
      h_vtxmass[in]->Fill(nt.vertices().mass(iv), w);
      h_vtxphi[in]->Fill(nt.vertices().phi(iv), w);
      h_vtxeta[in]->Fill(nt.vertices().eta(iv), w);
      h_vtxpt[in]->Fill(nt.vertices().pt(iv), w);
      h_vtxbs2derr_v_vtxntracks[in]->Fill(nt.vertices().ntracks(iv), nt.vertices().bs2derr(iv), w);
      //      h_vtxbs2derr_v_vtxtkonlymass[in]->Fill(nt.vertices().tkonlymass(iv), nt.vertices().bs2derr(iv), w);
      h_vtxbs2derr_v_vtxanglemax[in]->Fill(vtxs_anglemax[iv], nt.vertices().bs2derr(iv), w);
      h_vtxbs2derr_v_vtxphi[in]->Fill(nt.vertices().phi(iv), nt.vertices().bs2derr(iv), w);
      h_vtxbs2derr_v_vtxeta[in]->Fill(nt.vertices().eta(iv), nt.vertices().bs2derr(iv), w);
      h_vtxbs2derr_v_vtxpt[in]->Fill(nt.vertices().pt(iv), nt.vertices().bs2derr(iv), w);
      h_vtxbs2derr_v_vtxdbv[in]->Fill(nt.vertices().rho(iv), nt.vertices().bs2derr(iv), w);
      h_vtxbs2derr_v_etamovevec[in]->Fill(move_vector.Eta(), nt.vertices().bs2derr(iv), w);

      h_vtxbs2derr_v_maxtkerrdxy[in]->Fill(max_tk_err_dxy, nt.vertices().bs2derr(iv), w);

      for (const int it : its) {
        h_vtx_tks_pt[in]->Fill(nt.tracks().pt(it), w);
        h_vtx_tks_eta[in]->Fill(nt.tracks().eta(it), w);
        h_vtx_tks_phi[in]->Fill(nt.tracks().phi(it), w);
        h_vtx_tks_dxy[in]->Fill(nt.tracks().dxybs(it, nt.bs()), w);
        h_vtx_tks_dz[in]->Fill(nt.tracks().dzpv(it, nt.pvs()), w);
        h_vtx_tks_err_pt[in]->Fill(nt.tracks().err_pt(it), w);
        h_vtx_tks_err_eta[in]->Fill(nt.tracks().err_eta(it), w);
        h_vtx_tks_err_phi[in]->Fill(nt.tracks().err_phi(it), w);
        h_vtx_tks_err_dxy[in]->Fill(nt.tracks().err_dxy(it), w);
        h_vtx_tks_err_dz[in]->Fill(nt.tracks().err_dz(it), w);
        h_vtx_tks_nsigmadxy[in]->Fill(nt.tracks().nsigmadxybs(it, nt.bs()), w);
        h_vtx_tks_npxlayers[in]->Fill(nt.tracks().npxlayers(it), w);
        h_vtx_tks_nstlayers[in]->Fill(nt.tracks().nstlayers(it), w);

        if (!nt.tk_moved(it)) {
          h_vtx_tks_nomove_pt[in]->Fill(nt.tracks().pt(it), w);
          h_vtx_tks_nomove_eta[in]->Fill(nt.tracks().eta(it), w);
          h_vtx_tks_nomove_phi[in]->Fill(nt.tracks().phi(it), w);
          h_vtx_tks_nomove_dxy[in]->Fill(nt.tracks().dxybs(it, nt.bs()), w);
          h_vtx_tks_nomove_dz[in]->Fill(nt.tracks().dzpv(it, nt.pvs()), w);
          h_vtx_tks_nomove_err_pt[in]->Fill(nt.tracks().err_pt(it), w);
          h_vtx_tks_nomove_err_eta[in]->Fill(nt.tracks().err_eta(it), w);
          h_vtx_tks_nomove_err_phi[in]->Fill(nt.tracks().err_phi(it), w);
          h_vtx_tks_nomove_err_dxy[in]->Fill(nt.tracks().err_dxy(it), w);
          h_vtx_tks_nomove_err_dz[in]->Fill(nt.tracks().err_dz(it), w);
          h_vtx_tks_nomove_nsigmadxy[in]->Fill(nt.tracks().nsigmadxybs(it, nt.bs()), w);
          h_vtx_tks_nomove_npxlayers[in]->Fill(nt.tracks().npxlayers(it), w);
          h_vtx_tks_nomove_nstlayers[in]->Fill(nt.tracks().nstlayers(it), w);
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
      if (!npasses[i])
        continue;

      numdens& nd = nds[i];
      F1(nd(k_movedist2)        .num, movedist2);
      F1(nd(k_movedist3)        .num, movedist3);
      F1(nd(k_movevectoreta)    .num, movevectoreta);
      F1(nd(k_npv)              .num, nt.pvs().n());
      F1(nd(k_pvx)              .num, nt.pvs().x(0));
      F1(nd(k_pvy)              .num, nt.pvs().y(0));
      F1(nd(k_pvz)              .num, nt.pvs().z(0));
      F1(nd(k_pvrho)            .num, nt.pvs().rho(0));
      F1(nd(k_pvntracks)        .num, nt.pvs().ntracks(0));
      F1(nd(k_pvscore)          .num, nt.pvs().score(0));
      F1(nd(k_ht)               .num, nt.jets().ht());
      F1(nd(k_jet_asymm)        .num, jet_asymm);
      F2(nd(k_jetpt0_asymm)     .num, jet_pt_0, jet_asymm);
      F2(nd(k_jetpt1_asymm)     .num, jet_pt_1, jet_asymm);
      F2(nd(k_jeteta0_asymm)    .num, jet_eta_0, jet_asymm);
      F2(nd(k_jeteta1_asymm)    .num, jet_eta_1, jet_asymm);
      F2(nd(k_jetdr_asymm)      .num, jet_dr, jet_asymm);
      F1(nd(k_nalltracks)       .num, nt.tm().nalltracks());
      F1(nd(k_nmovedtracks)     .num, nt.tm().nmovedtracks());
      F1(nd(k_nseedtracks)      .num, nseedtracks);
      F1(nd(k_npreseljets)      .num, nt.tm().npreseljets());
      F1(nd(k_npreselbjets)     .num, nt.tm().npreselbjets());
      F2(nd(k_jeti01)           .num, jet_i_0, jet_i_1);
      F2(nd(k_jetp01)           .num, jet_p_0, jet_p_1);
      F2(nd(k_jetpt01)          .num, jet_pt_0, jet_pt_1);
      F1(nd(k_pt0)              .num, jet_pt_0);
      F1(nd(k_pt1)              .num, jet_pt_1);
      F2(nd(k_jeteta01)         .num, jet_eta_0, jet_eta_1);
      F2(nd(k_jetphi01)         .num, jet_phi_0, jet_phi_1);
      F1(nd(k_jetsume)          .num, jet_sume);
      F1(nd(k_jetdrmax)         .num, jet_drmax);
      F1(nd(k_jetdravg)         .num, jet_dravg);
      F1(nd(k_jetdetamax)       .num, jet_detamax);
      F1(nd(k_jetdetaavg)       .num, jet_detaavg);
      F1(nd(k_jetdphimax)       .num, jet_dphimax);
      F1(nd(k_jetdphiavg)       .num, jet_dphiavg);
      F1(nd(k_jet0_tkdrmax)     .num, max_dr_0);
      F1(nd(k_jet1_tkdrmax)     .num, max_dr_1);
      F1(nd(k_jet0_tkdravg)     .num, avg_dr_0);
      F1(nd(k_jet1_tkdravg)     .num, avg_dr_1);
      F2(nd(k_jet_dphi_deta_avg).num, jet_dphiavg, jet_detaavg);
      F2(nd(k_jdphi_nmovedtks)  .num, abs(jet_dphiavg), nt.tm().nmovedtracks());
      F2(nd(k_jdeta_nmovedtks)  .num, abs(jet_detaavg), nt.tm().nmovedtracks());
      F2(nd(k_jdr_nmovedtks)    .num, jet_dravg,        nt.tm().nmovedtracks());
      F2(nd(k_jtheta0_nmovedtks).num, jet_move_a3d_0,  nt.tm().nmovedtracks());
      F2(nd(k_jetmovea3d01)     .num, jet_move_a3d_0, jet_move_a3d_1);
      F2(nd(k_jetmovea3d_v_jetp).num, jet_p_0, jet_move_a3d_0);
      F2(nd(k_jetmovea3d_v_jetp).num, jet_p_1, jet_move_a3d_1);
      F2(nd(k_jetmovea3d0_v_movevectoreta).num, movevectoreta, jet_move_a3d_0);
      F2(nd(k_jetmovea3d1_v_movevectoreta).num, movevectoreta, jet_move_a3d_1);
      F1(nd(k_jeta3dmax)        .num, jet_a3dmax);
      F1(nd(k_angle0)           .num, jet_move_a3d_0);
      F1(nd(k_angle1)           .num, jet_move_a3d_1);
      F1(nd(k_dphi_j0_mv)       .num, abs(jet_mv_dphi_0));
      F1(nd(k_dphi_j1_mv)       .num, abs(jet_mv_dphi_1));
      F1(nd(k_deta_j0_mv)       .num, abs(jet_mv_deta_0));
      F1(nd(k_deta_j1_mv)       .num, abs(jet_mv_deta_1));
      F2(nd(k_dphi_j0_mv_jdeta) .num, abs(jet_mv_dphi_0), abs(jet_detaavg));
      F1(nd(k_jetsumntracks)    .num, jet_sumntracks);
      F2(nd(k_jetntracks01)     .num, jet_ntracks_0, jet_ntracks_1);
      F2(nd(k_jetntracks_v_jetp).num, jet_p_0, jet_ntracks_0);
      F2(nd(k_jetntracks_v_jetp).num, jet_p_1, jet_ntracks_1);
      F2(nd(k_jetnseedtracks01) .num, jet_nseedtracks_0, jet_nseedtracks_1);
      F1(nd(k_nvtx)             .num, npasses[i]);
      F1(nd(k_vtxbs2derr)       .num, vtx_bs2derr);
      F2(nd(k_vtxbs2derr_avgtkdr)    .num, vtx_bs2derr, avg_dr_0);
      F2(nd(k_vtxbs2derr_jdeta)      .num, vtx_bs2derr, jet_detaavg);
      F2(nd(k_vtxbs2derr_dphi_j0_mv) .num, vtx_bs2derr, jet_mv_dphi_0);
      F2(nd(k_vtxbs2derr_jdr)        .num, vtx_bs2derr, jet_dravg);
      F1(nd(k_vtxeta)           .num, vtx_eta);
      F1(nd(k_vtxz)             .num, vtx_z);

      for (size_t it = 0, ite = nt.tracks().n(); it < ite; ++it) {
        h_tks_pt[i]->Fill(nt.tracks().pt(it), w);
        h_tks_eta[i]->Fill(nt.tracks().eta(it), w);
        h_tks_phi[i]->Fill(nt.tracks().phi(it), w);
        h_tks_dxy[i]->Fill(nt.tracks().dxybs(it, nt.bs()), w);
        h_tks_dz[i]->Fill(nt.tracks().dzpv(it, nt.pvs()), w);
        h_tks_err_pt[i]->Fill(nt.tracks().err_pt(it), w);
        h_tks_err_eta[i]->Fill(nt.tracks().err_eta(it), w);
        h_tks_err_phi[i]->Fill(nt.tracks().err_phi(it), w);
        h_tks_err_dxy[i]->Fill(nt.tracks().err_dxy(it), w);
        h_tks_err_dz[i]->Fill(nt.tracks().err_dz(it), w);
        h_tks_nsigmadxy[i]->Fill(nt.tracks().nsigmadxybs(it, nt.bs()), w);
        h_tks_npxlayers[i]->Fill(nt.tracks().npxlayers(it), w);
        h_tks_nstlayers[i]->Fill(nt.tracks().nstlayers(it), w);

        if (nt.tk_moved(it)) {
          h_moved_tks_pt[i]->Fill(nt.tracks().pt(it), w);
          h_moved_tks_eta[i]->Fill(nt.tracks().eta(it), w);
          h_moved_tks_phi[i]->Fill(nt.tracks().phi(it), w);
          h_moved_tks_dxy[i]->Fill(nt.tracks().dxybs(it, nt.bs()), w);
          h_moved_tks_dz[i]->Fill(nt.tracks().dzpv(it, nt.pvs()), w);
          h_moved_tks_err_pt[i]->Fill(nt.tracks().err_pt(it), w);
          h_moved_tks_err_eta[i]->Fill(nt.tracks().err_eta(it), w);
          h_moved_tks_err_phi[i]->Fill(nt.tracks().err_phi(it), w);
          h_moved_tks_err_dxy[i]->Fill(nt.tracks().err_dxy(it), w);
          h_moved_tks_err_dz[i]->Fill(nt.tracks().err_dz(it), w);
          h_moved_tks_nsigmadxy[i]->Fill(nt.tracks().nsigmadxybs(it, nt.bs()), w);
          h_moved_tks_npxlayers[i]->Fill(nt.tracks().npxlayers(it), w);
          h_moved_tks_nstlayers[i]->Fill(nt.tracks().nstlayers(it), w);

          if (!nt.tracks().pass_seed(it, nt.bs())) {
            h_moved_nosel_tks_pt[i]->Fill(nt.tracks().pt(it), w);
            h_moved_nosel_tks_eta[i]->Fill(nt.tracks().eta(it), w);
            h_moved_nosel_tks_phi[i]->Fill(nt.tracks().phi(it), w);
            h_moved_nosel_tks_dxy[i]->Fill(nt.tracks().dxybs(it, nt.bs()), w);
            h_moved_nosel_tks_dz[i]->Fill(nt.tracks().dzpv(it, nt.pvs()), w);
            h_moved_nosel_tks_err_pt[i]->Fill(nt.tracks().err_pt(it), w);
            h_moved_nosel_tks_err_eta[i]->Fill(nt.tracks().err_eta(it), w);
            h_moved_nosel_tks_err_phi[i]->Fill(nt.tracks().err_phi(it), w);
            h_moved_nosel_tks_err_dxy[i]->Fill(nt.tracks().err_dxy(it), w);
            h_moved_nosel_tks_err_dz[i]->Fill(nt.tracks().err_dz(it), w);
            h_moved_nosel_tks_nsigmadxy[i]->Fill(nt.tracks().nsigmadxybs(it, nt.bs()), w);
            h_moved_nosel_tks_npxlayers[i]->Fill(nt.tracks().npxlayers(it), w);
            h_moved_nosel_tks_nstlayers[i]->Fill(nt.tracks().nstlayers(it), w);
          }
        }
      }
    }

    return std::make_pair(true, w);
  };

  nr.loop(fcn);

  printf("%llu/%llu = %.1f/%.1f denominator events with negative weights\n", nnegden, nden, negden, den);
  printf("%20s  %12s  %12s  %10s [%10s, %10s] +%10s -%10s\n", "name", "num", "den", "eff", "lo", "hi", "+", "-");
  for (const auto& p : nums) {
    const jmt::interval i = jmt::clopper_pearson_binom(p.second, den);
    printf("%20s  %12.1f  %12.1f  %10.4f [%10.4f, %10.4f] +%10.4f -%10.4f\n", p.first.c_str(), p.second, den, i.value, i.lower, i.upper, i.upper - i.value, i.value - i.lower);
  }
}
