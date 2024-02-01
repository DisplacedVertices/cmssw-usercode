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
  bool jet_decay_weights = false;
  std::string w_fn = "reweight.root";
  jmt::NtupleReader<mfv::MovedTracksNtuple> nr;

  namespace po = boost::program_options;
  nr.init_options("mfvMovedTree20/t", "TrackMoverHistsV27m", "nr_trackmoverv27mv1")
    ("tau",           po::value<int>   (&itau)          ->default_value(10000),   "tau in microns, for reweighting")
    ("btagsf",        po::value<bool>  (&btagsf_weights)->default_value(false),   "whether to use b-tag SF weights")
    ("ntks-weights",  po::value<bool>  (&ntks_weights)  ->default_value(false),   "whether to use ntracks weights")
    ("jet-decayweights",po::value<bool>  (&jet_decay_weights)->default_value(true),   "whether to use jet decay weights")
    ("w_fn",       po::value<std::string>  (&w_fn)          ->default_value("reweight.root"),  "file name of weights")
    ;

  if (!nr.parse_options(argc, argv)) return 1;

  TString w_fn_(w_fn);

  if (!nr.init()) return 1;
  auto& nt = nr.nt();
  auto& bs = nt.bs();
  auto& pvs = nt.pvs();
  auto& jets = nt.jets();	
  auto& muons = nt.muons();
  auto& electrons = nt.electrons();
  auto& pf = nt.pf();
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

  const std::vector<std::string> weight_hists_1d = {
    //"nocuts_2logm_den",
    //"nocuts_movedist3_den",
    "nocuts_jet_costheta_den",
  };
  const std::vector<std::string> jet_2d_weights_hists = {
    //"nocuts_jet0_sump_jet1_sump_den",
    //"nocuts_jet1_sump_jetdphi_den", 
    //"nocuts_jet1_sump_jetdr_den",
    "nocuts_jet_costheta_tightcloseseedtks_den",
    
  };
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
  if (jet_decay_weights) std::cout << "using extra weights from " << w_fn_ << std::endl;

  TH1D* h_tau = new TH1D("h_tau", ";tau (cm);events/10 #mum", 10000, 0,10);
  TH2D* h_tau_tw = new TH2D("h_tau_tw", ";tau (cm); weight from ctau=10mm", 25, 0, 10, 50, 0, 10);
  TH1D* h_btagsfweight = new TH1D("h_btagsfweight", ";weight;events/0.01", 200, 0, 2);

  const int num_numdens = 3;
  numdens nds[num_numdens] = { // JMTBAD why multiple dens here?
    numdens("nocuts"),
    numdens("ntracks"),
    numdens("all")
  };
  enum { k_movedist2, k_movedist3, k_movevectoreta, k_npv, k_pvx, k_pvy, k_pvz, k_pvrho, k_pvntracks, k_pvscore, k_ht, k_njets, k_nmuons, k_muon_pT, k_muon_abseta, k_muon_iso, k_muon_zoom_iso, k_muon_absdxybs, k_muon_absdz, k_muon_nsigmadxybs, k_neles, k_ele_pT, k_ele_abseta, k_ele_iso, k_ele_zoom_iso, k_ele_absdxybs, k_ele_absdz, k_ele_nsigmadxybs, k_met_pT, k_w_pT, k_w_mT, k_z_pT, k_z_m, k_lnu_absphi, k_ljet_absdr,k_ljet0_absdr, k_ljet1_absdr, k_nujet0_absphi, k_nujet1_absphi, k_wjet_dphi, k_zjet_dphi, k_w_ntk_j0, k_z_ntk_j0, k_jet_asymm, k_jet0_eta, k_jet1_eta, k_jet_dr, k_jet_costheta, k_jet_deta, k_jet_dphi, k_jet_dind, k_pt0, k_pt1, k_ntks_j0, k_ntks_j1, k_jet0_trk_pt, k_jet1_trk_pt, k_jet0_trk_p, k_jet1_trk_p,k_jet0_sump, k_jet1_sump, k_jet0_maxeta_jet1_maxeta, k_jet0_sumeta_jet1_sumeta, k_jet0_sump_jet1_sump, k_jet1_sump_jetdr, k_closeseed_trk_gendz, k_closeseed_trk_genmissdist, k_closeseed_trk_gennsigmadz, k_movedist3_jetdr, k_movedist3_tightcloseseedtks, k_jet_costheta_tightcloseseedtks, k_jet_dr_tightcloseseedtks, k_movedist3_closeseedtks, k_jet_costheta_closeseedtks, k_jet_dr_closeseedtks, k_jet1_sump_jetdphi, k_jet1_ntks_jetdphi,  k_2sump0sump1_1mcos, k_2logm, k_jet0_trk_dz, k_jet1_trk_dz, k_jet0_trk_vtxdxy, k_jet1_trk_vtxdxy, k_jet0_trk_vtxdz, k_jet1_trk_vtxdz, k_jet0_trk_nsigmavtxdz, k_jet1_trk_nsigmavtxdz, k_jet0_trk_nsigmavtxdxy, k_jet1_trk_nsigmavtxdxy, k_jet0_trk_nsigmavtx, k_jet1_trk_nsigmavtx, k_jet0_trk_dzerr, k_jet1_trk_dzerr, k_jet0_trk_dxyerr, k_jet1_trk_dxyerr, k_jet0_trk_eta, k_jet1_trk_eta, k_jet0_trk_gennsigma, k_jet1_trk_gennsigma, k_jet0_trk_gennsigmamissdist, k_jet1_trk_gennsigmamissdist, k_jet0_trk_genmissdist, k_jet1_trk_genmissdist, k_jet0_trk_gennsigmadz, k_jet1_trk_gennsigmadz, k_jet0_trk_gendz, k_jet1_trk_gendz, k_jet0_trk_whichpv, k_jet1_trk_whichpv, k_jet0_trk_dsz, k_jet1_trk_dsz, k_jet0_trk_dxy, k_jet1_trk_dxy, k_jet0_trk_nsigmadxy, k_jet1_trk_nsigmadxy, k_nmovedtracks, k_dphi_sum_j_mv, k_deta_sum_j_mv, k_jetpt0_asymm, k_jetpt1_asymm, k_jeteta0_asymm, k_jeteta1_asymm, k_jetdr_asymm, k_nalltracks, k_nseedtracks, k_seedtracks_jetdr, k_seedtracks_2logm, k_npreseljets, k_npreselbjets, k_jeti01, k_jetp01, k_jetpt01, k_jeteta01, k_jetphi01, k_jetsume, k_jetdrmax, k_jetdravg, k_jetdetamax, k_jetdetaavg, k_jetdphimax, k_jetdphiavg, k_jet0_tkdrmax, k_jet1_tkdrmax, k_jet0_tkdravg, k_jet1_tkdravg, k_jet_dphi_deta_avg, k_jdphi_nmovedtks, k_jdeta_nmovedtks, k_jdr_nmovedtks, k_jtheta0_nmovedtks, k_jetmovea3d01, k_jetmovea3d_v_jetp, k_jetmovea3d0_v_movevectoreta, k_jetmovea3d1_v_movevectoreta, k_jeta3dmax, k_angle0, k_angle1, k_dphi_j0_mv, k_dphi_j1_mv, k_deta_j0_mv, k_deta_j1_mv, k_dphi_j0_mv_jdeta, k_jetsumntracks, k_jetsumseedtracks, k_miscseedtracks, k_closeseedtks, k_tightcloseseedtks, k_movedseedtks, k_movedseedtks_jetdr, k_movedcloseseedtks, k_movedvtxseedtks, k_rat_moved_to_closetks, k_rat_moved_to_vtxtks, k_jetntracks01, k_jetntracks_v_jetp, k_jetnseedtracks01, k_nvtx, k_vtxbs2derr, k_vtxbs2derr_avgtkdr, k_vtxbs2derr_jdeta, k_vtxbs2derr_dphi_j0_mv, k_vtxbs2derr_jdr, k_vtxunc, k_vtxeta, k_vtxz, k_vtxdbv, k_vtx3dbv, k_vtxntk};
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
    nd.book(k_muon_zoom_iso, "muon_zoom_iso", ";muons zoomed iso;events/1", 200, 0, 0.15);
    nd.book(k_muon_absdxybs, "muon_absdxybs", ";muons |dxybs| cm; arb. units", 80, 0, 0.2);
    nd.book(k_muon_absdz, "muon_absdz", ";muons |dz| cm; arb. units", 80, 0, 1.0);
    nd.book(k_muon_nsigmadxybs, "muon_nsigmadxybs", ";muons n#sigma dxybs ; arb. units", 80, 0, 6.0);
    nd.book(k_neles, "neles", ";# passed offline-sel electrons;events/1", 10, 0, 10);
    nd.book(k_ele_pT, "ele_pT", ";electrons p_{T} (GeV);events/1", 50, 0, 200);
    nd.book(k_ele_abseta, "ele_abseta", ";electrons |#eta|; arb. units", 70, 0, 3.5);
    nd.book(k_ele_iso, "ele_iso", ";electrons iso;events/1", 200, 0, 0.15);
    nd.book(k_ele_zoom_iso, "ele_zoom_iso", ";electrons zoomed iso;events/1", 200, 0, 0.15);
    nd.book(k_ele_absdxybs, "ele_absdxybs", ";electrons |dxybs| cm; arb. units", 80, 0, 0.2);
    nd.book(k_ele_absdz, "ele_absdz", ";electrons |dz| cm; arb. units", 80, 0, 1.0);
    nd.book(k_ele_nsigmadxybs, "ele_nsigmadxybs", ";electrons n#sigma dxybs ; arb. units", 80, 0, 6.0);
    nd.book(k_met_pT, "met_pT", ";missing p_{T} (GeV);events/1", 50, 0, 200);
    nd.book(k_w_pT, "w_pT", ";RECO W boson's p_{T} (GeV);events/1", 50, 0, 200);
    nd.book(k_w_mT, "w_mT", ";RECO W boson's mass_{T} (GeV);events/1", 50, 0, 150);
    nd.book(k_z_pT, "z_pT", ";RECO Z boson's p_{T} (GeV);events/1", 50, 0, 200);
    nd.book(k_z_m, "z_m", ";RECO Z boson's inv. mass (GeV);events/1", 50, 0, 150);
    nd.book(k_lnu_absphi, "lnu_absphi", ";lepton-#nu |#DeltaPhi|; arb. units", 70, 0.0, 3.5);
    nd.book(k_ljet_absdr, "ljet_absdr", ";lepton-closest-jet |#DeltaR|; arb. units", 70, 0.0, 3.5);
    nd.book(k_ljet0_absdr, "ljet0_absdr", ";lepton-jet0 |#DeltaR|; arb. units", 70, 0.0, 3.5);
    nd.book(k_ljet1_absdr, "ljet1_absdr", ";lepton-jet1 |#DeltaR|; arb. units", 70, 0.0, 3.5);
    nd.book(k_nujet0_absphi, "nujet0_absphi", ";MET-jet0 |#DeltaPhi|; arb. units", 70, 0.0, 3.5);
    nd.book(k_nujet1_absphi, "nujet1_absphi", ";MET-jet1 |#DeltaPhi|; arb. units", 70, 0.0, 3.5);
    nd.book(k_wjet_dphi, "wjet_dphi", ";W-jet |#DeltaPhi|; arb. units", 70, 0.0, 3.5);
    nd.book(k_zjet_dphi, "zjet_dphi", ";Z-jet |#DeltaPhi|; arb. units", 70, 0.0, 3.5);
    nd.book(k_w_ntk_j0, "w_ntk_j0", ";Ntks in jet0 in single-muon events; arb. units", 25, 0.0, 25);
    nd.book(k_z_ntk_j0, "z_ntk_j0", ";Ntks in jet0 in di-muon events; arb. units", 25, 0.0, 25);
    nd.book(k_jet_asymm, "jet_asymm", ";jet pT asymmetry A_{J}; arb. units", 25, 0, 1);
    nd.book(k_jet0_eta, "jet0_eta", ";jet0's Eta; arb. units", 60, -3, 3);
    nd.book(k_jet1_eta, "jet1_eta", ";jet1's Eta; arb. units", 60, -3, 3);
    nd.book(k_jet_dr, "jet_dr", ";jets' #DeltaR; arb. units", 70, 0, 7);
    nd.book(k_jet_costheta, "jet_costheta", ";jets' cos(#theta); arb. units", 80, -1, 1);
    nd.book(k_jet_deta, "jet_deta", ";jets' #DeltaEta; arb. units", 70, 0, 7);
    nd.book(k_jet_dphi, "jet_dphi", ";jets' #DeltaPhi; arb. units", 70, -3.5, 3.5);
    nd.book(k_jet_dind, "jet_dind", ";jets' #DeltaIndex; arb. units", 20, 0, 20);
    nd.book(k_pt0, "pt0", ";RECO jet0 pT [GeV]", 50, 0, 150);
    nd.book(k_pt1, "pt1", ";RECO jet1 pT [GeV]", 50, 0, 150);
    nd.book(k_ntks_j0, "ntks_j0", ";Ntks in jet0", 25, 0, 25);
    nd.book(k_ntks_j1, "ntks_j1", ";Ntks in jet1", 25, 0, 25);
    nd.book(k_jet0_trk_pt, "jet0_trk_pt", "; jet0-movedseed-track's pT; arb. units", 45, 0, 15);
    nd.book(k_jet1_trk_pt, "jet1_trk_pt", "; jet1-movedseed-track's pT; arb. units", 45, 0, 15);
    nd.book(k_jet0_trk_p, "jet0_trk_p", "; jet0-movedseed-track's p; arb. units", 45, 0, 15);
    nd.book(k_jet1_trk_p, "jet1_trk_p", "; jet1-movedseed-track's p; arb. units", 45, 0, 15);
    nd.book(k_jet0_sump, "jet0_sump", "; jet0-movedseed-track's sum p; arb. units", 80, 0, 80);
    nd.book(k_jet1_sump, "jet1_sump", "; jet1-movedseed-track's sum p; arb. units", 80, 0, 80);
    nd.book(k_jet0_maxeta_jet1_maxeta, "jet0_maxeta_jet1_maxeta", "; max(jet0-movedseed-track's Eta); max(jet1-movedseed-track's Eta)", 60, -3, 3, 60, -3, 3); 
    nd.book(k_jet0_sumeta_jet1_sumeta, "jet0_sumeta_jet1_sumeta", "; jet0-movedseed-track's sum |Eta|; jet1-movedseed-track's sum |Eta|", 100, 0, 25, 100, 0, 25); 
    nd.book(k_jet0_sump_jet1_sump, "jet0_sump_jet1_sump", "; jet0-movedseed-track's sum p; jet1-movedseed-track's sum p", 80, 0, 80, 80, 0, 80);
    nd.book(k_jet1_sump_jetdr, "jet1_sump_jetdr", "; jet1-movedseed-track's sum p;jets #DeltaR", 80, 0, 80, 50, 0, 3.5);
    nd.book(k_closeseed_trk_genmissdist, "closeseed_trk_genmissdist", "; close-seed-track's missdist to LLP; arb. units", 50, -0.05, 0.05);
    nd.book(k_closeseed_trk_gendz, "closeseed_trk_gendz", "; close-seed-track's dz to LLP; arb. units", 50, -0.05, 0.05);
    nd.book(k_closeseed_trk_gennsigmadz, "closeseed_trk_gennsigmadz", "; close-seed-track's gennsigmadz; arb. units", 80, -10, 10);
    nd.book(k_movedist3_jetdr, "movedist3_jetdr", "; movement 3-dist;jets #DeltaR", 100, 0, 2, 50, 0, 3.5);
    nd.book(k_movedist3_tightcloseseedtks, "movedist3_tightcloseseedtks", ";movement 3-dist ;# tracks 2#sigma-close to artificial vtx", 100, 0, 2, 25, 0, 25);
    nd.book(k_jet_costheta_tightcloseseedtks, "jet_costheta_tightcloseseedtks", "; jets' cos(#theta);# tracks 2#sigma-close to artificial vtx", 80, -1, 1, 25, 0, 25);
    nd.book(k_jet_dr_tightcloseseedtks, "jet_dr_tightcloseseedtks", "; jets' #DeltaR;# tracks 2#sigma-close to artificial vtx", 70, 0, 7, 25, 0, 25);
    nd.book(k_movedist3_closeseedtks, "movedist3_closeseedtks", ";movement 3-dist ;# tracks close to artificial vtx", 100, 0, 2, 25, 0, 25);
    nd.book(k_jet_costheta_closeseedtks, "jet_costheta_closeseedtks", "; jets' cos(#theta);# tracks close to artificial vtx", 80, -1, 1, 25, 0, 25);
    nd.book(k_jet_dr_closeseedtks, "jet_dr_closeseedtks", "; jets' #DeltaR;# tracks close to artificial vtx", 70, 0, 7, 25, 0, 25);
    nd.book(k_jet1_sump_jetdphi, "jet1_sump_jetdphi", "; jet1-movedseed-track's sum p;jets #DeltaPhi", 80, 0, 80, 70, -3.5, 3.5);
    nd.book(k_jet1_ntks_jetdphi, "jet1_ntks_jetdphi", "; Ntks in jet1;jets #DeltaPhi", 25, 0, 25, 70, -3.5, 3.5);
    nd.book(k_2sump0sump1_1mcos, "2sump0sump1_1mcos", "; log(2*sump_{tk0}*sump_{tk1}); log(1-cos(#Delta#Theta))", 70, 0, 7, 20, -2, 0);
    nd.book(k_2logm, "2logm", "; log(2*sump_{tk0}*sump_{tk1}) + log(1-cos(#Delta#Theta))", 70, 0, 7);
    nd.book(k_jet0_trk_dz, "jet0_trk_dz", "; jet0-movedseed-track's dzpv; arb. units", 50, -1.0, 1.0);
    nd.book(k_jet1_trk_dz, "jet1_trk_dz", "; jet1-movedseed-track's dzpv; arb. units", 50, -1.0, 1.0);
    nd.book(k_jet0_trk_vtxdxy, "jet0_trk_vtxdxy", "; jet0-movedseed-track's dxy to vtx; arb. units", 50, -1.0, 1.0);
    nd.book(k_jet1_trk_vtxdxy, "jet1_trk_vtxdxy", "; jet1-movedseed-track's dxy to vtx; arb. units", 50, -1.0, 1.0);
    nd.book(k_jet0_trk_vtxdz, "jet0_trk_vtxdz", "; jet0-movedseed-track's dz to vtx; arb. units", 50, -1.0, 1.0);
    nd.book(k_jet1_trk_vtxdz, "jet1_trk_vtxdz", "; jet1-movedseed-track's dz to vtx; arb. units", 50, -1.0, 1.0);
    nd.book(k_jet0_trk_nsigmavtxdz, "jet0_trk_nsigmavtxdz", "; jet0-movedseed-track's nsigmavtxdz; arb. units", 80, -10, 10);
    nd.book(k_jet1_trk_nsigmavtxdz, "jet1_trk_nsigmavtxdz", "; jet1-movedseed-track's nsigmavtxdz; arb. units", 80, -10, 10);
    nd.book(k_jet0_trk_nsigmavtxdxy, "jet0_trk_nsigmavtxdxy", "; jet0-movedseed-track's nsigmavtxdxy; arb. units", 80, -10, 10);
    nd.book(k_jet1_trk_nsigmavtxdxy, "jet1_trk_nsigmavtxdxy", "; jet1-movedseed-track's nsigmavtxdxy; arb. units", 80, -10, 10);
    nd.book(k_jet0_trk_nsigmavtx, "jet0_trk_nsigmavtx", "; jet0-movedseed-track's nsigmavtx; arb. units", 80, -10, 10);
    nd.book(k_jet1_trk_nsigmavtx, "jet1_trk_nsigmavtx", "; jet1-movedseed-track's nsigmavtx; arb. units", 80, -10, 10);
    nd.book(k_jet0_trk_dzerr, "jet0_trk_dzerr", "; jet0-movedseed-track's dz err; arb. units", 100, 0.0, 0.05);
    nd.book(k_jet1_trk_dzerr, "jet1_trk_dzerr", "; jet1-movedseed-track's dz err; arb. units", 100, 0.0, 0.05);
    nd.book(k_jet0_trk_dxyerr, "jet0_trk_dxyerr", "; jet0-movedseed-track's dxy err; arb. units", 100, 0.0, 0.05);
    nd.book(k_jet1_trk_dxyerr, "jet1_trk_dxyerr", "; jet1-movedseed-track's dxy err; arb. units", 100, 0.0, 0.05);
    nd.book(k_jet0_trk_eta, "jet0_trk_eta", "; jet0-movedseed-track's eta; arb. units", 70, -3.5, 3.5);
    nd.book(k_jet1_trk_eta, "jet1_trk_eta", "; jet1-movedseed-track's eta; arb. units", 70, -3.5, 3.5);
    nd.book(k_jet0_trk_gennsigma, "jet0_trk_gennsigma", "; jet0-movedseed-track's n#sigma to LLP; arb. units", 80, -10, 10);
    nd.book(k_jet1_trk_gennsigma, "jet1_trk_gennsigma", "; jet1-movedseed-track's n#sigma to LLP; arb. units", 80, -10, 10);
    nd.book(k_jet0_trk_gennsigmamissdist, "jet0_trk_gennsigmamissdist", "; jet0-movedseed-track's n#sigma missdist to LLP; arb. units", 80, -10, 10);
    nd.book(k_jet1_trk_gennsigmamissdist, "jet1_trk_gennsigmamissdist", "; jet1-movedseed-track's n#sigma missdist to LLP; arb. units", 80, -10, 10);
    nd.book(k_jet0_trk_genmissdist, "jet0_trk_genmissdist", "; jet0-movedseed-track's missdist to LLP; arb. units", 50, -0.05, 0.05);
    nd.book(k_jet1_trk_genmissdist, "jet1_trk_genmissdist", "; jet1-movedseed-track's missdist to LLP; arb. units", 50, -0.05, 0.05);
    nd.book(k_jet0_trk_gendz, "jet0_trk_gendz", "; jet0-movedseed-track's dz to LLP; arb. units", 50, -0.05, 0.05);
    nd.book(k_jet1_trk_gendz, "jet1_trk_gendz", "; jet1-movedseed-track's dz to LLP; arb. units", 50, -0.05, 0.05);
    nd.book(k_jet0_trk_gennsigmadz, "jet0_trk_gennsigmadz", "; jet0-movedseed-track's n#sigma dz to LLP; arb. units", 80, -10, 10);
    nd.book(k_jet1_trk_gennsigmadz, "jet1_trk_gennsigmadz", "; jet1-movedseed-track's n#sigma dz to LLP; arb. units", 80, -10, 10);
    nd.book(k_jet0_trk_whichpv, "jet0_trk_whichpv", "; jet0-movedseed-track's which_pv; arb. units", 40, 0.0, 40);
    nd.book(k_jet1_trk_whichpv, "jet1_trk_whichpv", "; jet1-movedseed-track's which_pv; arb. units", 40, 0.0, 40);
    nd.book(k_jet0_trk_dsz, "jet0_trk_dsz", "; jet0-movedseed-track's dsz; arb. units", 50, -1.0, 1.0);
    nd.book(k_jet1_trk_dsz, "jet1_trk_dsz", "; jet1-movedseed-track's dsz; arb. units", 50, -1.0, 1.0);
    nd.book(k_jet0_trk_dxy, "jet0_trk_dxy", "; jet0-movedseed-track's dxybs; arb. units", 50, -0.5, 0.5);
    nd.book(k_jet1_trk_dxy, "jet1_trk_dxy", "; jet1-movedseed-track's dxybs; arb. units", 50, -0.5, 0.5);
    nd.book(k_jet0_trk_nsigmadxy, "jet0_trk_nsigmadxy", "; jet0-movedseed-track's nsigmadxybs; arb. units", 80, -10, 10);
    nd.book(k_jet1_trk_nsigmadxy, "jet1_trk_nsigmadxy", "; jet1-movedseed-track's nsigmadxybs; arb. units", 80, -10, 10);
    nd.book(k_nmovedtracks, "nmovedtracks", ";# moved tracks;events/2", 30, 0, 30);
    nd.book(k_dphi_sum_j_mv, "dphi_sum_j_mv", ";#Delta #phi between jet0+jet1 and move vec;events/bin", 70, -3.5, 3.5);
    nd.book(k_deta_sum_j_mv, "deta_sum_j_mv", ";abs #Delta #eta between jet0+jet1 and move vec;events/bin", 25, 0, 4);

    nd.book(k_jetpt0_asymm, "jetpt0_asymm", ";jet p_{T} 0; jet asymm. A_{J}", 50, 0, 1000, 25, 0, 1);
    nd.book(k_jetpt1_asymm, "jetpt1_asymm", ";jet p_{T} 1; jet asymm. A_{J}", 50, 0, 1000, 25, 0, 1);
    nd.book(k_jeteta0_asymm, "jeteta0_asymm", ";jet #eta 0; jet asymm. A_{J}", 100, -4, 4, 25, 0, 1);
    nd.book(k_jeteta1_asymm, "jeteta1_asymm", ";jet #eta 1; jet asymm. A_{J}", 100, -4, 4, 25, 0, 1);
    nd.book(k_jetdr_asymm, "jetdr_asymm", ";jets #DeltaR; jet asymm. A_{J}", 70, 0, 7, 25, 0, 1);
    nd.book(k_nalltracks, "nalltracks", ";# all tracks;events/10", 200, 0, 2000);
    nd.book(k_nseedtracks, "nseedtracks", ";# seed tracks;events", 80, 0, 80);
    nd.book(k_seedtracks_jetdr, "seedtracks_jetdr", "; # seed tracks; jets #DeltaR", 20, 0, 20, 70, 0, 7);
    nd.book(k_seedtracks_2logm, "seedtracks_2logm", "; # seed tracks; log(2*sump_{tk0}*sump_{tk1}) + log(1-cos(#Delta#Theta))", 20, 0, 20, 70, 0, 7);
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
    nd.book(k_jetsumseedtracks, "jetsumseedtracks", ";#Sigma jet # seed tracks;events/5", 200, 0, 1000);    
    nd.book(k_miscseedtracks, "miscseedtracks", ";#Sigma seed tks not from moved jets;count", 30, 0, 30);
    nd.book(k_closeseedtks,  "closeseedtks", ";# tracks close to artificial vtx.;count", 80, 0, 80);
    nd.book(k_tightcloseseedtks,  "tightcloseseedtks", ";# tracks 2#sigma-close to artificial vtx.;count", 25, 0, 25);
    nd.book(k_movedseedtks,  "movedseedtks", ";# moved seed tracks;count", 30, 0, 30);
    nd.book(k_movedseedtks_jetdr, "movedseedtks_jetdr", ";# moved seed tracks; jets #DeltaR", 30, 0, 30, 70, 0, 7);
    nd.book(k_movedvtxseedtks,  "movedvtxseedtks", ";# moved seed tracks in vtx;count", 30, 0, 30);
    nd.book(k_movedcloseseedtks,  "movedcloseseedtks", ";# moved seed tracks 5#sigma to LLP;count", 30, 0, 30);
    nd.book(k_rat_moved_to_closetks, "rat_moved_to_closetks", ";#frac{# moved seed tracks 5#sigma to LLP}{# seed tracks 5#sigma to LLP};count", 50, 0, 1);
    nd.book(k_rat_moved_to_vtxtks, "rat_moved_to_vtxtks", ";#frac{# moved seed tracks in vtx}{# vtx ntrack};count", 50, 0, 1);
    nd.book(k_jetntracks01, "jetntracks01", ";jet # tracks 0;jet # tracks 1", 50, 0, 50, 50, 0, 50);
    nd.book(k_jetntracks_v_jetp, "jetntracks_v_jetp01", ";jet momentum (GeV);jet # tracks", 200, 0, 2000, 50, 0, 50);
    nd.book(k_jetnseedtracks01, "jetnseedtracks01", ";jet # sel tracks 0;jet # sel tracks 1", 50, 0, 50, 50, 0, 50);
    nd.book(k_nvtx, "nvtx", ";number of vertices;events/1", 8, 0, 8);
    nd.book(k_vtxbs2derr, "vtxbs2derr", ";bs2derr of vertex;events", 500, 0, 0.05);
    nd.book(k_vtxbs2derr_avgtkdr, "vtxbs2derr_avgtkdr", ";bs2derr of vertex; avg tk #Delta R", 100, 0, 0.025, 31, 0, M_PI);
    nd.book(k_vtxbs2derr_jdeta, "vtxbs2derr_jdeta", ";bs2derr of vertex; jet #Delta #eta", 100, 0, 0.025, 25, 0, 4);
    nd.book(k_vtxbs2derr_dphi_j0_mv, "vtxbs2derr_dphi_j0_mv", ";bs2derr of vertex;  #Delta #phi btwn j0 and MV", 100, 0, 0.025, 63, 0, M_PI);
    nd.book(k_vtxbs2derr_jdr, "vtxbs2derr_jdr", ";bs2derr of vertex; jet #Delta R", 100, 0, 0.025, 30, 0, 6);
    nd.book(k_vtxunc, "vtxunc", ";dist3d(move vector, vtx) cm; arb. units", 200, 0, 0.2);
    nd.book(k_vtxeta, "vtxeta", ";eta of vertex;events", 100, -4, 4);
    nd.book(k_vtxz, "vtxz", ";z pos of vertex;events", 100, -10, 10);
    nd.book(k_vtxdbv, "vtxdbv", ";2D displacement of vertex to a beamspot;events", 50, 0, 2);
    nd.book(k_vtx3dbv, "vtx3dbv", ";3D displacement of vertex to a beamspot;events", 50, 0, 2);
    nd.book(k_vtxntk, "vtxntk", ";ntrack of vertex;events", 20, 0, 20);
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
    int n_movedseedtks = 0;
    int n_closeseedtks = 0;
    int n_tightcloseseedtks = 0;
    int n_movedcloseseedtks = 0;
    int n_movedvtxseedtks = 0;
    const float  close_criteria = 5.0;  // How close must a seed track pass near an SV to be considered 'close?'
    const float  tight_close_criteria = 2.0;  // How close must a seed track pass near an SV to be considered 'close?'
    // First part of the preselection: our offline jet requirements
    // (mostly applied in ntupling step) plus only look at move
    // vectors ~inside the beampipe // JMTBAD the 2.0 cm requirement isn't exact
    if (movedist2 < 0.01 || movedist2 > 2.0) //FIXME
      NR_loop_cont(w);

    int nselmuons = 0;
    double muon_pT = -99;
    double muon_p = -99;
    double muon_q = -99;
    double muon_px = -99;
    double muon_py = -99;
    double muon_pz = -99;
    double muon_abseta = -99;	 
    double muon_iso = 99;
    double muon_absdxybs = -99;
    double muon_absdz = -99;
    double muon_nsigmadxybs = -99;
    TLorentzVector muon_p4;
    TLorentzVector tmpz_p4;
    TLorentzVector zmumu_p4;
    TLorentzVector zee_p4;
    bool has_Zmumuboson = false;
    bool has_Zeeboson = false;
    bool has_Wboson = false;


    for (int i = 0, ie = muons.n(); i < ie; ++i) {
      double tmp_muon_absdxybs = abs(muons.dxybs(i, bs));
      double tmp_muon_absdz = muons.dzpv(i, pvs);
      bool muon_IP_cut = tmp_muon_absdxybs < 0.02 && tmp_muon_absdz < 0.5;
      if (muon_IP_cut && muons.pt(i) > 29.0 && abs(muons.eta(i)) < 2.4 && muons.isMed(i) && muons.iso(i) < 0.15) {
        nselmuons += 1;
        if (nselmuons == 1) {
          muon_pT = muons.pt(i);
          muon_p = muons.p(i);
          muon_px = muons.px(i);
          muon_py = muons.py(i);
          muon_pz = muons.pz(i);
          muon_p4.SetPxPyPzE(muon_px, muon_py, muon_pz, muon_p);
          muon_q = muons.q(i);
          muon_abseta = abs(muons.eta(i));
          muon_absdxybs = abs(muons.dxybs(i, bs));
          muon_absdz =  muons.dzpv(i, pvs);
          muon_iso = muons.iso(i);
          muon_nsigmadxybs = muons.nsigmadxybs(i, bs);
          tmpz_p4 += muon_p4;

        }
        if (has_Zmumuboson == false && nselmuons > 0 && muon_q * muons.q(i) == -1) {
          TLorentzVector antimuon_p4;
          antimuon_p4.SetPxPyPzE(muons.px(i), muons.py(i), muons.pz(i), muons.p(i));
          tmpz_p4 += antimuon_p4;
          has_Zmumuboson = true; 
        }
      }
    }

    double z_m = -99, zmumu_m = -99; 
    double z_pT = -99, zmumu_pT = -99;
    if (has_Zmumuboson) {
      zmumu_m = tmpz_p4.M();
      zmumu_pT = tmpz_p4.Pt();
      zmumu_p4 = tmpz_p4;
    }

    int nseleles = 0;
    double ele_pT = -99;
    double ele_p = -99;
    double ele_q = -99;
    double ele_px = -99;
    double ele_py = -99;
    double ele_pz = -99;
    double ele_abseta = -99;
    double ele_iso = 99;
    double ele_absdxybs = -99;
    double ele_absdz = -99;
    double ele_nsigmadxybs = -99;
    TLorentzVector ele_p4;
    tmpz_p4.SetPxPyPzE(0.0, 0.0, 0.0, 0.0);

    for (int i = 0, ie = electrons.n(); i < ie; ++i) {
      double tmp_ele_abseta = abs(electrons.eta(i));
      double tmp_ele_absdxybs = abs(electrons.dxybs(i, bs));
      double tmp_ele_absdz = electrons.dzpv(i, pvs);  
      bool ele_IP_cut = tmp_ele_abseta < 1.48 ? tmp_ele_absdxybs < 0.05 && tmp_ele_absdz < 0.1 : tmp_ele_absdxybs < 0.1 && tmp_ele_absdz < 0.2;
      if (ele_IP_cut && electrons.pt(i) > 20.0 && abs(electrons.eta(i)) < 2.4 && electrons.isTight(i) && electrons.passveto(i) && electrons.iso(i) < 0.1) {
        nseleles += 1;
        if (nseleles == 1) {
          ele_pT = electrons.pt(i);
          ele_p = electrons.p(i);
          ele_px = electrons.px(i);
          ele_py = electrons.py(i);
          ele_pz = electrons.pz(i);
          ele_abseta = abs(electrons.eta(i));
          ele_absdxybs = abs(electrons.dxybs(i, bs));
          ele_absdz = electrons.dzpv(i, pvs);
          ele_p4.SetPxPyPzE(ele_px, ele_py, ele_pz, ele_p);
          ele_q = electrons.q(i);
          ele_iso = electrons.iso(i);
          ele_nsigmadxybs = electrons.nsigmadxybs(i, bs);
          tmpz_p4 += ele_p4;

        }

        if ( has_Zeeboson == false && nseleles > 0 && ele_q * electrons.q(i) == -1) {
          TLorentzVector antiele_p4;
          antiele_p4.SetPxPyPzE(electrons.px(i), electrons.py(i), electrons.pz(i), electrons.p(i));
          tmpz_p4 += antiele_p4;
          has_Zeeboson = true;
        }
      }
    }

    double met_pT = std::hypot(pf.met_x(), pf.met_y());
    TLorentzVector met_p4;
    met_p4.SetPtEtaPhiM(met_pT, 0, pf.met_phi(), 0);
    double lnu_absphi = -99, ljet_absdr = -99, ljet0_absdr = -99, ljet1_absdr = -99, nujet0_absphi = -99, nujet1_absphi = -99;
    double w_mT = -99, zee_m = -99;
    double w_pT = -99, zee_pT = -99;
    TLorentzVector w_p4;

    if (met_p4.Pt() > 25) {
      if (nselmuons && !has_Zmumuboson) {
        has_Wboson = true;
        w_p4 = met_p4 + muon_p4;
        w_pT = w_p4.Pt();
        lnu_absphi = abs(muon_p4.DeltaPhi(met_p4));
        w_mT = sqrt(2 * muon_pT * met_pT * (1 - cos(muon_p4.DeltaPhi(met_p4))));
      }
      else if (nseleles > 0 && nselmuons == 0 && !has_Zeeboson) {
        has_Wboson = true;
        w_p4 = met_p4 + ele_p4;
        w_pT = w_p4.Pt();
        lnu_absphi = abs(ele_p4.DeltaPhi(met_p4));
        w_mT = sqrt(2 * muon_pT * met_pT * (1 - cos(muon_p4.DeltaPhi(met_p4))));
      }
    }
    if (has_Zeeboson) {
      zee_m = tmpz_p4.M();
      zee_pT = tmpz_p4.Pt();
      zee_p4 = tmpz_p4;
    }

    auto nps = [&](const int k) { return tks.pass_seed(k, bs); };
    int nmovedjets = 0, jet_sumntracks = 0;
    int jet_sumseedtracks = 0;
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

      const std::vector<int> jet_tk_list = tks.tks_for_jet(i);
      jet_sumseedtracks += std::count_if(jet_tk_list.begin(), jet_tk_list.end(), nps);

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


    const std::vector<int> jet0_tracks = tks.tks_for_jet(jet_i[0]);
    const std::vector<int> jet1_tracks = tks.tks_for_jet(jet_i[1]);
    std::vector<int> closeseedtrk_idx;
    std::vector<int> jet0trk_idx;
    std::vector<int> jet1trk_idx;
    int jet_ntk_0 = 0;
    int jet_ntk_1 = 0;
    double sump_0 = 0;
    double sump_1 = 0;
    double maxeta_0 = 0.0;
    double maxeta_1 = 0.0;
    double sumeta_0 = 0.0;
    double sumeta_1 = 0.0;
    
    for (int j = 0; j < tks.n(); ++j) {
      const TLorentzVector jp4 = tks.p4(j);
      auto it0 = std::find(jet0_tracks.begin(), jet0_tracks.end(), j);
      if (it0 != jet0_tracks.end() && tks.pass_sel(j)){
        jet_p4[0] += tks.p4(j);
        jet_ntk_0 += 1;
        if (tks.pass_seed(j, bs) && nt.tk_moved(j)) jet0trk_idx.push_back(j);
        sump_0+=tks.p(j);
        sumeta_0 += fabs(tks.eta(j));
        if (fabs(tks.eta(j)) > fabs(maxeta_0)) maxeta_0 = tks.eta(j);
        //std::cout << "is also moved?" << (bool)nt.tk_moved(j) << std::endl;
      }
      auto it1 = std::find(jet1_tracks.begin(), jet1_tracks.end(), j);
      if (it1 != jet1_tracks.end() && tks.pass_sel(j)){
        jet_p4[1] += tks.p4(j);
        jet_ntk_1 += 1;
        if (tks.pass_seed(j, bs) && nt.tk_moved(j)) jet1trk_idx.push_back(j);
        sump_1+=tks.p(j);
        sumeta_1 += fabs(tks.eta(j));
        if (fabs(tks.eta(j)) > fabs(maxeta_1)) maxeta_1 = tks.eta(j);
        //std::cout << "is also moved?" << (bool)nt.tk_moved(j) << std::endl;
      }
    }
 
    for (int j = 0; j < tks.n(); ++j){
        if (tks.pass_seed(j, bs) && nt.tk_moved(j)) n_movedseedtks++;
        if (tks.pass_seed(j,bs)){
            
            const double temp_sigdxy = tks.dxy(j, nt.tm().move_x() + bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()))/tks.err_dxy(j);
            const double temp_sigdz  = tks.dz(j, nt.tm().move_x() + bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()), nt.tm().move_z())/tks.err_dz(j);
            const double sum_sq_sig = hypot(temp_sigdxy, temp_sigdz);
            const double sigs_quad = sum_sq_sig;


            // Count how many 'close' seed tracks there are
            if ( sigs_quad < close_criteria){
              n_closeseedtks++;
              closeseedtrk_idx.push_back(j);
              auto it0 = std::find(jet0trk_idx.begin(), jet0trk_idx.end(), j);
              auto it1 = std::find(jet1trk_idx.begin(), jet1trk_idx.end(), j);
              if (it0 != jet0trk_idx.end() || it1 != jet1trk_idx.end()) n_movedcloseseedtks++;
            }
            if ( sigs_quad < tight_close_criteria){
              n_tightcloseseedtks++;
            }
        }
    }
    //for (size_t j = 0; j < jet1trk_idx.size(); ++j)
    //    if (tks.pass_seed(jet1trk_idx[j], bs) && nt.tk_moved(jet1trk_idx[j])) n_movedseedtks++;


    const double jet_asymm = (jet_p4[0].Pt() - jet_p4[1].Pt()) / (jet_p4[0].Pt() + jet_p4[1].Pt());
    const double jet_dr = jet_p4[0].DeltaR(jet_p4[1]); 
    const double jet_costheta = ((jet_p4[0].X()*jet_p4[1].X()) + (jet_p4[0].Y()*jet_p4[1].Y()) + (jet_p4[0].Z()*jet_p4[1].Z()))/(jet_p4[0].P()*jet_p4[1].P()); 
    const double jet_dphi = jet_p4[0].DeltaPhi(jet_p4[1]); 
    const double jet_deta = fabs(jet_p4[0].Eta() - jet_p4[1].Eta()); 
    const double jet_dind = fabs(jet_i[1] - jet_i[0]);
    const double jet_mv_dphi_sum = move_vector.DeltaPhi((jet_p4[0] + jet_p4[1]).Vect());
    const double jet_mv_deta_sum = fabs((jet_p4[0] + jet_p4[1]).Eta() - move_vector.Eta());
    double wjet_dphi = w_p4.DeltaPhi(jet_p4[0] + jet_p4[1]);
    if (!has_Wboson) wjet_dphi = 99;
    double zjet_dphi = 99;
    if (has_Zmumuboson){
      zjet_dphi = zmumu_p4.DeltaPhi(jet_p4[0] + jet_p4[1]);
      z_m = zmumu_m;
      z_pT = zmumu_pT;
    }
    else if (has_Zeeboson){
      zjet_dphi = zee_p4.DeltaPhi(jet_p4[0] + jet_p4[1]);
      z_m = zee_m;
      z_pT = zee_pT;
    }
    if (met_p4.Pt() > 25){
      if (nselmuons > 0) {
        ljet_absdr = abs(muon_p4.DeltaR(jet_p4[0])) < abs(muon_p4.DeltaR(jet_p4[1])) ? abs(muon_p4.DeltaR(jet_p4[0])) : abs(muon_p4.DeltaR(jet_p4[1]));
        ljet0_absdr = abs(muon_p4.DeltaR(jet_p4[0]));
        ljet1_absdr = abs(muon_p4.DeltaR(jet_p4[1]));
      }
      else if ( nseleles > 0 && nselmuons == 0) {
        ljet_absdr = abs(ele_p4.DeltaR(jet_p4[0])) < abs(ele_p4.DeltaR(jet_p4[1])) ? abs(ele_p4.DeltaR(jet_p4[0])) : abs(ele_p4.DeltaR(jet_p4[1]));
        ljet0_absdr = abs(ele_p4.DeltaR(jet_p4[0]));
        ljet1_absdr = abs(ele_p4.DeltaR(jet_p4[1]));
      }
      nujet0_absphi = abs(met_p4.DeltaPhi(jet_p4[0]));
      nujet1_absphi = abs(met_p4.DeltaPhi(jet_p4[1]));
    }



    const double jet_nseedtracks_max = std::max(jet_nseedtracks[0], jet_nseedtracks[1]);
    const double jet_nseedtracks_min = std::min(jet_nseedtracks[0], jet_nseedtracks[1]);
    const double jet_pt_max = std::max(jet_pt[0], jet_pt[1]);
    const double jet_pt_min = std::min(jet_pt[0], jet_pt[1]);

    //presel cuts
    if (jet_ntk_0 < 1 || jet_ntk_1 < 1 || jet_ntk_0 + jet_ntk_1 < 5)
      NR_loop_cont(w);

    //if (n_movedseedtks < 10)
    //  NR_loop_cont(w);
   
    //if ( fabs(jet_p4[0].Eta()) > 1.0 || fabs(jet_p4[1].Eta()) > 1.0 )
    //  NR_loop_cont(w);

    if (jet_decay_weights) {
      TFile* jet_weights = TFile::Open(w_fn_);

      /* 
         for (const auto& name : weight_hists_1d) {
         double v = -1e99;
         if (name == "nocuts_2logm_den"){
         v = log10(2*sump_0*sump_1) + log10(1-jet_costheta);
         }
         TH1D* hw = (TH1D*)jet_weights->Get(name.c_str());
         assert(hw);
         const int bin = hw->FindBin(v);
         if (bin >= 1 && bin <= hw->GetNbinsX())
         w *= hw->GetBinContent(bin);
         }
      */
      /*
      for (const auto& name : weight_hists_1d) {
        double v = -1e99;
        if (name == "nocuts_jet_costheta_den"){
          v = jet_costheta;
        }
        TH1D* hw = (TH1D*)jet_weights->Get(name.c_str());
        assert(hw);
        const int bin = hw->FindBin(v);
        if (bin >= 1 && bin <= hw->GetNbinsX())
          w *= hw->GetBinContent(bin);
      }
      */
      for (const auto& name : jet_2d_weights_hists) {
         double vx = -1e99;
         double vy = -1e99;
         if (name == "nocuts_jet_costheta_tightcloseseedtks_den"){
         //if (name == "nocuts_jet_dr_tightcloseseedtks_den"){
         //if (name == "nocuts_movedist3_tightcloseseedtks_den"){
         vx = jet_costheta;
         vy = n_tightcloseseedtks;
         }
         TH2D* hw = (TH2D*)jet_weights->Get(name.c_str());
         assert(hw);
         const int bin = hw->FindBin(vx, vy);
         if (bin >= 1 && bin <= hw->GetNcells()){
         w *= hw->GetBinContent(bin);
         }
      }
      /*
      for (const auto& name : jet_2d_weights_hists) {
         double vx = -1e99;
         double vy = -1e99;
         if (name == "nocuts_jet1_sump_jetdr_den"){
         vx = sump_1;
         vy = jet_dr;
         }
         TH2D* hw = (TH2D*)jet_weights->Get(name.c_str());
         assert(hw);
         const int bin = hw->FindBin(vx, vy);
         if (bin >= 1 && bin <= hw->GetNcells()){
         w *= hw->GetBinContent(bin);
         }    
       }
      */
      jet_weights->Close();
      
    }
    
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
    jmt::MinValue dist2min(100);
    double vtx_bs2derr = -9.9, vtx_eta = -9.9, vtx_z = -999.9, vtx_dbv = -999.9, vtx_3dbv = -999.9, vtx_ntk = -9; // JMTBAD ??? these end up with what???
    std::vector<int> first_vtx_to_pass(num_numdens, -1);
    auto set_it_if_first = [](int& to_set, int to_set_to) { if (to_set == -1) to_set = to_set_to; };

    for (int ivtx = 0; ivtx < nvtx; ++ivtx) {
      dist2move = (vs.pos(ivtx) - nt.tm().move_pos()).Mag();
      dist2min(ivtx, dist2move);
      if (dist2move > 0.0200) //FIXME 
        continue;

      vtx_bs2derr = vs.bs2derr(ivtx); // JMTBAD ???
      vtx_eta     = vs.eta(ivtx);
      vtx_z       = vs.z(ivtx);
      vtx_dbv     = vs.pos(ivtx).Perp();
      vtx_3dbv    = vs.pos(ivtx).Mag();
      vtx_ntk     = vs.ntracks(ivtx);
      
      const bool pass_ntracks = vs.ntracks(ivtx) >= 5;
      const bool pass_bs2derr = vs.bs2derr(ivtx) < 0.0050; // JMTBAD use rescale_bs2derr and in plots below //FIXME 

      if (1)                            { set_it_if_first(first_vtx_to_pass[0], ivtx); ++n_pass_nocuts;  }
      if (pass_ntracks)                 { set_it_if_first(first_vtx_to_pass[1], ivtx); ++n_pass_ntracks; }
      if (pass_ntracks && pass_bs2derr) { set_it_if_first(first_vtx_to_pass[2], ivtx); ++n_pass_all;     }

      if (pass_ntracks && pass_bs2derr && nr.is_mc() && nr.use_weights() && ntks_weights)
        w *= ntks_weight(vs.ntracks(ivtx));
    }
    dist2move = dist2min.v();
    double mindist2move_iv = dist2min.i();
    if (mindist2move_iv != -1){
      vtx_bs2derr = vs.bs2derr(mindist2move_iv); // JMTBAD ???
      vtx_eta     = vs.eta(mindist2move_iv);
      vtx_z       = vs.z(mindist2move_iv);
      vtx_dbv     = vs.pos(mindist2move_iv).Perp();
      vtx_3dbv    = vs.pos(mindist2move_iv).Mag();
      vtx_ntk     = vs.ntracks(mindist2move_iv);
      const std::vector<int> its = tks.tks_for_sv(mindist2move_iv);
      for (int it : its){
        auto it0 = std::find(jet0trk_idx.begin(), jet0trk_idx.end(), it);
        auto it1 = std::find(jet1trk_idx.begin(), jet1trk_idx.end(), it);
        if (it0 != jet0trk_idx.end() || it1 != jet1trk_idx.end()) n_movedvtxseedtks++;
      }
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
      if (muon_iso != 0.0) nd.den(k_muon_zoom_iso, muon_iso);
      nd.den(k_muon_absdxybs, muon_absdxybs);
      nd.den(k_muon_absdz, muon_absdz);
      nd.den(k_muon_nsigmadxybs, muon_nsigmadxybs);
      nd.den(k_neles, nseleles);
      nd.den(k_ele_pT, ele_pT);
      nd.den(k_ele_abseta, ele_abseta);
      nd.den(k_ele_iso, ele_iso);
      if (ele_iso != 0.0) nd.den(k_ele_zoom_iso, ele_iso);
      nd.den(k_ele_absdxybs, ele_absdxybs);
      nd.den(k_ele_absdz, ele_absdz);
      nd.den(k_ele_nsigmadxybs, ele_nsigmadxybs);
      nd.den(k_met_pT, met_pT);
      nd.den(k_w_pT, w_pT);
      nd.den(k_w_mT, w_mT);
      nd.den(k_z_pT, z_pT);
      nd.den(k_z_m, z_m);
      nd.den(k_lnu_absphi, lnu_absphi);
      nd.den(k_ljet_absdr, ljet_absdr);
      nd.den(k_ljet0_absdr, ljet0_absdr);
      nd.den(k_ljet1_absdr, ljet1_absdr);
      nd.den(k_nujet0_absphi, nujet0_absphi);
      nd.den(k_nujet1_absphi, nujet1_absphi);
      nd.den(k_wjet_dphi, fabs(wjet_dphi));
      nd.den(k_zjet_dphi, fabs(zjet_dphi));
      nd.den(k_jet_asymm, jet_asymm);
      nd.den(k_jet0_eta, jet_eta[0]);
      nd.den(k_jet1_eta, jet_eta[1]);
      nd.den(k_jet_dr, jet_dr);
      nd.den(k_jet_costheta, jet_costheta);
      nd.den(k_jet_deta, jet_deta);
      nd.den(k_jet_dphi, jet_dphi);
      nd.den(k_jet_dind, jet_dind);
      nd.den(k_pt0, jet_pt[0]);
      nd.den(k_pt1, jet_pt[1]);
      nd.den(k_ntks_j0, jet_ntk_0);
      nd.den(k_ntks_j1, jet_ntk_1);
      for (size_t j = 0; j < jet0trk_idx.size(); ++j){
        nd.den(k_jet0_trk_pt, tks.pt(jet0trk_idx[j]));
        nd.den(k_jet0_trk_p, tks.p(jet0trk_idx[j]));
        nd.den(k_jet0_trk_eta, tks.eta(jet0trk_idx[j]));
        nd.den(k_jet0_trk_dz, tks.dzpv(jet0trk_idx[j], pvs));
        if (mindist2move_iv != -1) {
          const double jet0_vtxdz = tks.dz(jet0trk_idx[j], vs.x(mindist2move_iv) + bs.x(vs.z(mindist2move_iv)),vs.y(mindist2move_iv) + bs.y(vs.z(mindist2move_iv)),vs.z(mindist2move_iv)); 
          const double jet0_vtxdxy = tks.dxy(jet0trk_idx[j], vs.x(mindist2move_iv) + bs.x(vs.z(mindist2move_iv)), vs.y(mindist2move_iv) + bs.y(vs.z(mindist2move_iv)));
          nd.den(k_jet0_trk_vtxdxy, jet0_vtxdxy);
          nd.den(k_jet0_trk_vtxdz, jet0_vtxdz);
          nd.den(k_jet0_trk_nsigmavtxdz, jet0_vtxdz/tks.err_dz(jet0trk_idx[j]));
          nd.den(k_jet0_trk_nsigmavtxdxy, jet0_vtxdxy/tks.err_dxy(jet0trk_idx[j]));
          nd.den(k_jet0_trk_nsigmavtx, sqrt((jet0_vtxdxy/tks.err_dxy(jet0trk_idx[j]))*(jet0_vtxdxy/tks.err_dxy(jet0trk_idx[j])) + (jet0_vtxdz/tks.err_dz(jet0trk_idx[j]))*(jet0_vtxdz/tks.err_dz(jet0trk_idx[j]))));
        }
        nd.den(k_jet0_trk_dzerr, tks.err_dz(jet0trk_idx[j]));
        const double jet0_gennsigmadz = tks.dz(jet0trk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()), nt.tm().move_z())/tks.err_dz(jet0trk_idx[j]);
        const double jet0_gennsigmamissdist = tks.dxy(jet0trk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y()+ bs.y(nt.tm().move_z()))/tks.err_dxy(jet0trk_idx[j]);  
        nd.den(k_jet0_trk_gennsigma, sqrt((jet0_gennsigmamissdist*jet0_gennsigmamissdist) + (jet0_gennsigmadz*jet0_gennsigmadz)));
        nd.den(k_jet0_trk_gennsigmamissdist, jet0_gennsigmamissdist);
        nd.den(k_jet0_trk_genmissdist, tks.dxy(jet0trk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y()+ bs.y(nt.tm().move_z())));
        nd.den(k_jet0_trk_gennsigmadz, jet0_gennsigmadz);
        nd.den(k_jet0_trk_gendz, tks.dz(jet0trk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()), nt.tm().move_z()));
        nd.den(k_jet0_trk_whichpv, tks.which_pv(jet0trk_idx[j]));
        nd.den(k_jet0_trk_dsz, tks.dsz(jet0trk_idx[j], pvs.x(0) + bs.x(pvs.z(0)), pvs.y(0) + bs.y(pvs.z(0)), pvs.z(0)));
        nd.den(k_jet0_trk_dxy, tks.dxybs(jet0trk_idx[j], bs));
        nd.den(k_jet0_trk_nsigmadxy, tks.dxybs(jet0trk_idx[j], bs)/tks.err_dxy(jet0trk_idx[j]));
        nd.den(k_jet0_trk_dxyerr, tks.err_dxy(jet0trk_idx[j]));
      }
      nd.den(k_jet0_sump, sump_0);
      for (size_t j = 0; j < jet1trk_idx.size(); ++j){
        nd.den(k_jet1_trk_pt, tks.pt(jet1trk_idx[j]));
        nd.den(k_jet1_trk_p, tks.p(jet1trk_idx[j]));
        nd.den(k_jet1_trk_eta, tks.eta(jet1trk_idx[j]));
        nd.den(k_jet1_trk_dz, tks.dzpv(jet1trk_idx[j], pvs));
        if (mindist2move_iv != -1) {
          const double jet1_vtxdz = tks.dz(jet1trk_idx[j],vs.x(mindist2move_iv) + bs.x(vs.z(mindist2move_iv)),vs.y(mindist2move_iv) + bs.y(vs.z(mindist2move_iv)),vs.z(mindist2move_iv)); 
          const double jet1_vtxdxy = tks.dxy(jet1trk_idx[j], vs.x(mindist2move_iv) + bs.x(vs.z(mindist2move_iv)), vs.y(mindist2move_iv) + bs.y(vs.z(mindist2move_iv)));
          nd.den(k_jet1_trk_vtxdxy, jet1_vtxdxy);
          nd.den(k_jet1_trk_vtxdz, jet1_vtxdz);
          nd.den(k_jet1_trk_nsigmavtxdz, jet1_vtxdz/tks.err_dz(jet1trk_idx[j]));
          nd.den(k_jet1_trk_nsigmavtxdxy, jet1_vtxdxy/tks.err_dxy(jet1trk_idx[j]));
          nd.den(k_jet1_trk_nsigmavtx, sqrt((jet1_vtxdxy/tks.err_dxy(jet1trk_idx[j]))*(jet1_vtxdxy/tks.err_dxy(jet1trk_idx[j])) + (jet1_vtxdz/tks.err_dz(jet1trk_idx[j]))*(jet1_vtxdz/tks.err_dz(jet1trk_idx[j]))));
        }
        nd.den(k_jet1_trk_dzerr, tks.err_dz(jet1trk_idx[j]));
        const double jet1_gennsigmadz = tks.dz(jet1trk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()), nt.tm().move_z())/tks.err_dz(jet1trk_idx[j]);
        const double jet1_gennsigmamissdist = tks.dxy(jet1trk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y()+ bs.y(nt.tm().move_z()))/tks.err_dxy(jet1trk_idx[j]);  
        nd.den(k_jet1_trk_gennsigma, sqrt((jet1_gennsigmamissdist*jet1_gennsigmamissdist) + (jet1_gennsigmadz*jet1_gennsigmadz)));
        nd.den(k_jet1_trk_gennsigmamissdist, jet1_gennsigmamissdist);
        nd.den(k_jet1_trk_genmissdist, tks.dxy(jet1trk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y()+ bs.y(nt.tm().move_z())));
        nd.den(k_jet1_trk_gennsigmadz, jet1_gennsigmadz);
        nd.den(k_jet1_trk_gendz, tks.dz(jet1trk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()), nt.tm().move_z()));
        nd.den(k_jet1_trk_whichpv, tks.which_pv(jet1trk_idx[j]));
        nd.den(k_jet1_trk_dsz, tks.dsz(jet1trk_idx[j], pvs.x(0) + bs.x(pvs.z(0)), pvs.y(0) + bs.y(pvs.z(0)), pvs.z(0)));
        nd.den(k_jet1_trk_dxy, tks.dxybs(jet1trk_idx[j], bs));
        nd.den(k_jet1_trk_nsigmadxy, tks.dxybs(jet1trk_idx[j], bs)/tks.err_dxy(jet1trk_idx[j]));
        nd.den(k_jet1_trk_dxyerr, tks.err_dxy(jet1trk_idx[j]));
      }
      for (size_t j = 0; j < closeseedtrk_idx.size(); ++j){
        nd.den(k_closeseed_trk_genmissdist, tks.dxy(closeseedtrk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y()+ bs.y(nt.tm().move_z())));
        nd.den(k_closeseed_trk_gendz, tks.dz(closeseedtrk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()), nt.tm().move_z()));
        nd.den(k_closeseed_trk_gennsigmadz, tks.dz(closeseedtrk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()), nt.tm().move_z())/tks.err_dz(closeseedtrk_idx[j]));
      }
      nd.den(k_jet1_sump, sump_1);
      nd.den(k_jet1_sump_jetdr, sump_1, jet_dr);
      nd.den(k_movedist3_jetdr, movedist3, jet_dr);
      nd.den(k_movedist3_tightcloseseedtks, movedist3, n_tightcloseseedtks);
      nd.den(k_jet_costheta_tightcloseseedtks, jet_costheta, n_tightcloseseedtks);
      nd.den(k_jet_dr_tightcloseseedtks, jet_dr, n_tightcloseseedtks);
      nd.den(k_movedist3_closeseedtks, movedist3, n_closeseedtks);
      nd.den(k_jet_costheta_closeseedtks, jet_costheta, n_closeseedtks);
      nd.den(k_jet_dr_closeseedtks, jet_dr, n_closeseedtks);
      nd.den(k_jet1_sump_jetdphi, sump_1, jet_dphi);
      nd.den(k_jet1_ntks_jetdphi, jet_ntk_1, jet_dphi);
      nd.den(k_jet0_sump_jet1_sump, sump_0, sump_1);
      nd.den(k_jet0_maxeta_jet1_maxeta, maxeta_0, maxeta_1);
      nd.den(k_jet0_sumeta_jet1_sumeta, sumeta_0, sumeta_1);
      nd.den(k_2sump0sump1_1mcos, log10(2*sump_0*sump_1), log10(1-jet_costheta));
      nd.den(k_2logm, log10(2*sump_0*sump_1) + log10(1-jet_costheta));
      nd.den(k_nmovedtracks, nt.tm().nmovedtracks());
      nd.den(k_dphi_sum_j_mv, jet_mv_dphi_sum);
      nd.den(k_deta_sum_j_mv, jet_mv_deta_sum);
      nd.den(k_jetpt0_asymm, jet_pt_max, jet_asymm);
      nd.den(k_jetpt1_asymm, jet_pt_min, jet_asymm);
      nd.den(k_jeteta0_asymm, jet_p4[0].Eta(), jet_asymm);
      nd.den(k_jeteta1_asymm, jet_p4[1].Eta(), jet_asymm);
      nd.den(k_jetdr_asymm, jet_dr, jet_asymm);
      nd.den(k_nalltracks, nt.tm().nalltracks());
      nd.den(k_nseedtracks, nseedtracks);
      nd.den(k_seedtracks_jetdr, nseedtracks, jet_dr);
      nd.den(k_seedtracks_2logm, nseedtracks, log10(2*sump_0*sump_1) + log10(1-jet_costheta));
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
      nd.den(k_jetsumseedtracks, jet_sumseedtracks);
      nd.den(k_miscseedtracks, nseedtracks - jet_sumseedtracks); 
      nd.den(k_closeseedtks, n_closeseedtks);
      nd.den(k_tightcloseseedtks, n_tightcloseseedtks);
      nd.den(k_movedseedtks_jetdr, n_movedseedtks, jet_dr);
      nd.den(k_movedseedtks, n_movedseedtks);
      nd.den(k_movedvtxseedtks, n_movedvtxseedtks);
      nd.den(k_movedcloseseedtks, n_movedcloseseedtks);
      nd.den(k_rat_moved_to_closetks, n_movedcloseseedtks/n_closeseedtks); 
      nd.den(k_rat_moved_to_vtxtks, n_movedvtxseedtks/vtx_ntk); 
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
      nd.den(k_vtxunc, dist2move);
      nd.den(k_vtxeta, vtx_eta);
      nd.den(k_vtxz, vtx_z);
      nd.den(k_vtxdbv, vtx_dbv);
      nd.den(k_vtx3dbv, vtx_3dbv);
      nd.den(k_vtxntk, vtx_ntk);
    }

    for (int in = 0; in < num_numdens; ++in) {
      int iv = first_vtx_to_pass[in];
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
      if (muon_iso != 0.0) nd.num(k_muon_zoom_iso, muon_iso);
      nd.num(k_muon_absdxybs, muon_absdxybs);
      nd.num(k_muon_absdz, muon_absdz);
      nd.num(k_muon_nsigmadxybs, muon_nsigmadxybs);
      nd.num(k_neles, nseleles);
      nd.num(k_ele_pT, ele_pT);
      nd.num(k_ele_abseta, ele_abseta);
      nd.num(k_ele_iso, ele_iso);
      if (ele_iso != 0.0) nd.num(k_ele_zoom_iso, ele_iso);
      nd.num(k_ele_absdxybs, ele_absdxybs);
      nd.num(k_ele_absdz, ele_absdz);
      nd.num(k_ele_nsigmadxybs, ele_nsigmadxybs);
      nd.num(k_met_pT, met_pT);
      nd.num(k_w_pT, w_pT);
      nd.num(k_w_mT, w_mT);
      nd.num(k_z_pT, z_pT);
      nd.num(k_z_m, z_m);
      nd.num(k_lnu_absphi, lnu_absphi);
      nd.num(k_ljet_absdr, ljet_absdr);
      nd.num(k_ljet0_absdr, ljet0_absdr);
      nd.num(k_ljet1_absdr, ljet1_absdr);
      nd.num(k_nujet0_absphi, nujet0_absphi);
      nd.num(k_nujet1_absphi, nujet1_absphi);
      nd.num(k_wjet_dphi, fabs(wjet_dphi));
      nd.num(k_zjet_dphi, fabs(zjet_dphi));
      nd.num(k_jet_asymm, jet_asymm);
      nd.num(k_jet0_eta, jet_eta[0]);
      nd.num(k_jet1_eta, jet_eta[1]);
      nd.num(k_jet_dr, jet_dr);
      nd.num(k_jet_costheta, jet_costheta);
      nd.num(k_jet_deta, jet_deta);
      nd.num(k_jet_dphi, jet_dphi);
      nd.num(k_jet_dind, jet_dind);
      nd.num(k_pt0, jet_pt[0]);
      nd.num(k_pt1, jet_pt[1]);
      nd.num(k_ntks_j0, jet_ntk_0);
      nd.num(k_ntks_j1, jet_ntk_1);
      for (size_t j = 0; j < jet0trk_idx.size(); ++j){
        nd.num(k_jet0_trk_pt, tks.pt(jet0trk_idx[j]));
        nd.num(k_jet0_trk_p, tks.p(jet0trk_idx[j]));
        nd.num(k_jet0_trk_eta, tks.eta(jet0trk_idx[j]));
        nd.num(k_jet0_trk_dz, tks.dzpv(jet0trk_idx[j], pvs));
        if (mindist2move_iv != -1) {
          const double jet0_vtxdz = tks.dz(jet0trk_idx[j], vs.x(mindist2move_iv) + bs.x(vs.z(mindist2move_iv)),vs.y(mindist2move_iv) + bs.y(vs.z(mindist2move_iv)),vs.z(mindist2move_iv)); 
          const double jet0_vtxdxy = tks.dxy(jet0trk_idx[j], vs.x(mindist2move_iv) + bs.x(vs.z(mindist2move_iv)), vs.y(mindist2move_iv) + bs.y(vs.z(mindist2move_iv)));
          nd.num(k_jet0_trk_vtxdxy, jet0_vtxdxy);
          nd.num(k_jet0_trk_vtxdz, jet0_vtxdz);
          nd.num(k_jet0_trk_nsigmavtxdz, jet0_vtxdz/tks.err_dz(jet0trk_idx[j]));
          nd.num(k_jet0_trk_nsigmavtxdxy, jet0_vtxdxy/tks.err_dxy(jet0trk_idx[j]));
          nd.num(k_jet0_trk_nsigmavtx, sqrt((jet0_vtxdxy/tks.err_dxy(jet0trk_idx[j]))*(jet0_vtxdxy/tks.err_dxy(jet0trk_idx[j])) + (jet0_vtxdz/tks.err_dz(jet0trk_idx[j]))*(jet0_vtxdz/tks.err_dz(jet0trk_idx[j]))));
        }
        nd.num(k_jet0_trk_dzerr, tks.err_dz(jet0trk_idx[j]));
        const double jet0_gennsigmadz = tks.dz(jet0trk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()), nt.tm().move_z())/tks.err_dz(jet0trk_idx[j]);
        const double jet0_gennsigmamissdist = tks.dxy(jet0trk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y()+ bs.y(nt.tm().move_z()))/tks.err_dxy(jet0trk_idx[j]);  
        nd.num(k_jet0_trk_gennsigma, sqrt((jet0_gennsigmamissdist*jet0_gennsigmamissdist) + (jet0_gennsigmadz*jet0_gennsigmadz)));
        nd.num(k_jet0_trk_gennsigmamissdist, jet0_gennsigmamissdist);
        nd.num(k_jet0_trk_genmissdist, tks.dxy(jet0trk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y()+ bs.y(nt.tm().move_z())));
        nd.num(k_jet0_trk_gennsigmadz, jet0_gennsigmadz);
        nd.num(k_jet0_trk_gendz, tks.dz(jet0trk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()), nt.tm().move_z()));
        nd.num(k_jet0_trk_whichpv, tks.which_pv(jet0trk_idx[j]));
        nd.num(k_jet0_trk_dsz, tks.dsz(jet0trk_idx[j], pvs.x(0) + bs.x(pvs.z(0)), pvs.y(0) + bs.y(pvs.z(0)), pvs.z(0)));
        nd.num(k_jet0_trk_dxy, tks.dxybs(jet0trk_idx[j], bs));
        nd.num(k_jet0_trk_nsigmadxy, tks.dxybs(jet0trk_idx[j], bs)/tks.err_dxy(jet0trk_idx[j]));
        nd.num(k_jet0_trk_dxyerr, tks.err_dxy(jet0trk_idx[j]));
      }
      nd.num(k_jet0_sump, sump_0);
      for (size_t j = 0; j < jet1trk_idx.size(); ++j){
        nd.num(k_jet1_trk_pt, tks.pt(jet1trk_idx[j]));
        nd.num(k_jet1_trk_p, tks.p(jet1trk_idx[j]));
        nd.num(k_jet1_trk_eta, tks.eta(jet1trk_idx[j]));
        nd.num(k_jet1_trk_dz, tks.dzpv(jet1trk_idx[j], pvs));
        if (mindist2move_iv != -1) {
          const double jet1_vtxdz = tks.dz(jet1trk_idx[j],vs.x(mindist2move_iv) + bs.x(vs.z(mindist2move_iv)),vs.y(mindist2move_iv) + bs.y(vs.z(mindist2move_iv)),vs.z(mindist2move_iv)); 
          const double jet1_vtxdxy = tks.dxy(jet1trk_idx[j], vs.x(mindist2move_iv) + bs.x(vs.z(mindist2move_iv)), vs.y(mindist2move_iv) + bs.y(vs.z(mindist2move_iv)));
          nd.num(k_jet1_trk_vtxdxy, jet1_vtxdxy);
          nd.num(k_jet1_trk_vtxdz, jet1_vtxdz);
          nd.num(k_jet1_trk_nsigmavtxdz, jet1_vtxdz/tks.err_dz(jet1trk_idx[j]));
          nd.num(k_jet1_trk_nsigmavtxdxy, jet1_vtxdxy/tks.err_dxy(jet1trk_idx[j]));
          nd.num(k_jet1_trk_nsigmavtx, sqrt((jet1_vtxdxy/tks.err_dxy(jet1trk_idx[j]))*(jet1_vtxdxy/tks.err_dxy(jet1trk_idx[j])) + (jet1_vtxdz/tks.err_dz(jet1trk_idx[j]))*(jet1_vtxdz/tks.err_dz(jet1trk_idx[j]))));
        }
        nd.num(k_jet1_trk_dzerr, tks.err_dz(jet1trk_idx[j]));
        const double jet1_gennsigmadz = tks.dz(jet1trk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()), nt.tm().move_z())/tks.err_dz(jet1trk_idx[j]);
        const double jet1_gennsigmamissdist = tks.dxy(jet1trk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y()+ bs.y(nt.tm().move_z()))/tks.err_dxy(jet1trk_idx[j]);  
        nd.num(k_jet1_trk_gennsigma, sqrt((jet1_gennsigmamissdist*jet1_gennsigmamissdist) + (jet1_gennsigmadz*jet1_gennsigmadz)));
        nd.num(k_jet1_trk_gennsigmamissdist, jet1_gennsigmamissdist);
        nd.num(k_jet1_trk_genmissdist, tks.dxy(jet1trk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y()+ bs.y(nt.tm().move_z())));
        nd.num(k_jet1_trk_gennsigmadz, jet1_gennsigmadz);
        nd.num(k_jet1_trk_gendz, tks.dz(jet1trk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()), nt.tm().move_z()));
        nd.num(k_jet1_trk_whichpv, tks.which_pv(jet1trk_idx[j]));
        nd.num(k_jet1_trk_dsz, tks.dsz(jet1trk_idx[j], pvs.x(0) + bs.x(pvs.z(0)), pvs.y(0) + bs.y(pvs.z(0)), pvs.z(0)));
        nd.num(k_jet1_trk_dxy, tks.dxybs(jet1trk_idx[j], bs));
        nd.num(k_jet1_trk_nsigmadxy, tks.dxybs(jet1trk_idx[j], bs)/tks.err_dxy(jet1trk_idx[j]));
        nd.num(k_jet1_trk_dxyerr, tks.err_dxy(jet1trk_idx[j]));
      }
      for (size_t j = 0; j < closeseedtrk_idx.size(); ++j){
        nd.num(k_closeseed_trk_genmissdist, tks.dxy(closeseedtrk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y()+ bs.y(nt.tm().move_z())));
        nd.num(k_closeseed_trk_gendz, tks.dz(closeseedtrk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()), nt.tm().move_z()));
        nd.num(k_closeseed_trk_gennsigmadz, tks.dz(closeseedtrk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()), nt.tm().move_z())/tks.err_dz(closeseedtrk_idx[j]));
      }
      nd.num(k_jet1_sump, sump_1);
      nd.num(k_jet1_sump_jetdr, sump_1, jet_dr);
      nd.num(k_movedist3_jetdr, movedist3, jet_dr);
      nd.num(k_movedist3_tightcloseseedtks, movedist3, n_tightcloseseedtks);
      nd.num(k_jet_costheta_tightcloseseedtks, jet_costheta, n_tightcloseseedtks);
      nd.num(k_jet_dr_tightcloseseedtks, jet_dr, n_tightcloseseedtks);
      nd.num(k_movedist3_closeseedtks, movedist3, n_closeseedtks);
      nd.num(k_jet_costheta_closeseedtks, jet_costheta, n_closeseedtks);
      nd.num(k_jet_dr_closeseedtks, jet_dr, n_closeseedtks);
      nd.num(k_jet1_sump_jetdphi, sump_1, jet_dphi);
      nd.num(k_jet1_ntks_jetdphi, jet_ntk_1, jet_dphi);
      nd.num(k_jet0_sump_jet1_sump, sump_0, sump_1);
      nd.num(k_jet0_maxeta_jet1_maxeta, maxeta_0, maxeta_1);
      nd.num(k_jet0_sumeta_jet1_sumeta, sumeta_0, sumeta_1);
      nd.num(k_2sump0sump1_1mcos, log10(2*sump_0*sump_1), log10(1-jet_costheta));
      nd.num(k_2logm, log10(2*sump_0*sump_1) + log10(1-jet_costheta));
      nd.num(k_nmovedtracks, nt.tm().nmovedtracks());
      nd.num(k_dphi_sum_j_mv, jet_mv_dphi_sum);
      nd.num(k_deta_sum_j_mv, jet_mv_deta_sum);
      nd.num(k_jetpt0_asymm, jet_p4[0].Pt(), jet_asymm);
      nd.num(k_jetpt1_asymm, jet_p4[1].Pt(), jet_asymm);
      nd.num(k_jeteta0_asymm, jet_p4[0].Eta(), jet_asymm);
      nd.num(k_jeteta1_asymm, jet_p4[1].Eta(), jet_asymm);
      nd.num(k_jetdr_asymm, jet_dr, jet_asymm);
      nd.num(k_nalltracks, nt.tm().nalltracks());
      nd.num(k_nseedtracks, nseedtracks);
      nd.num(k_seedtracks_jetdr, nseedtracks, jet_dr);
      nd.num(k_seedtracks_2logm, nseedtracks, log10(2*sump_0*sump_1) + log10(1-jet_costheta));
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
      nd.num(k_angle0, jet_mv_a3d[0]);
      nd.num(k_angle1, jet_mv_a3d[1]);
      nd.num(k_dphi_j0_mv, fabs(jet_mv_dphi[0]));
      nd.num(k_dphi_j1_mv, fabs(jet_mv_dphi[1]));
      nd.num(k_deta_j0_mv, fabs(jet_mv_deta[0]));
      nd.num(k_deta_j1_mv, fabs(jet_mv_deta[1]));
      nd.num(k_dphi_j0_mv_jdeta, fabs(jet_mv_dphi[0]), fabs(jet_detaavg));
      nd.num(k_jetsumntracks, jet_sumntracks);
      nd.num(k_jetsumseedtracks, jet_sumseedtracks);
      nd.num(k_miscseedtracks, nseedtracks - jet_sumseedtracks); 
      nd.num(k_closeseedtks, n_closeseedtks);
      nd.num(k_tightcloseseedtks, n_tightcloseseedtks);
      nd.num(k_movedseedtks_jetdr, n_movedseedtks, jet_dr);
      nd.num(k_movedseedtks, n_movedseedtks);
      nd.num(k_movedvtxseedtks, n_movedvtxseedtks);
      nd.num(k_movedcloseseedtks, n_movedcloseseedtks);
      nd.num(k_rat_moved_to_closetks, n_movedcloseseedtks/n_closeseedtks); 
      nd.num(k_rat_moved_to_vtxtks, n_movedvtxseedtks/vtx_ntk); 
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
      nd.num(k_vtxunc, dist2move);
      nd.num(k_vtxeta, vtx_eta);
      nd.num(k_vtxz, vtx_z);
      nd.num(k_vtxdbv, vtx_dbv);
      nd.num(k_vtx3dbv, vtx_3dbv);
      nd.num(k_vtxntk, vtx_ntk);
      
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
