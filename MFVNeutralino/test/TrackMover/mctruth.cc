#include "utils.h"
#include <cmath>

int main(int argc, char** argv) {
  double min_lspdist3 = 0.02;

  jmt::NtupleReader<mfv::MovedTracksNtuple> nr;
  namespace po = boost::program_options;
  nr.init_options("mfvMovedTreeMCTruth/t", "TrackMoverMCTruthVetoPUPVetoTrkOffdzJetByMiniJetHistsUlv30lepmumv4", "trackmovermctruthoffdzulv30lepmumv4", "all_signal = True")
    ("min-lspdist3", po::value<double>(&min_lspdist3)->default_value(0.00), "min distance between LSP decays to use event") //FIXME 0.02
    ;

  if (!nr.parse_options(argc, argv)) return 1;
  std::cout << " min_lspdist3: " << min_lspdist3 << "\n";

  if (!nr.init()) return 1;
  auto& nt = nr.nt();
  auto& bs = nt.bs();
  auto& pvs = nt.pvs();
  auto& jets = nt.jets();
  auto& muons = nt.muons();
  auto& electrons = nt.electrons();
  auto& pf = nt.pf();
  auto& tks = nt.tracks();
  auto& gen = nt.gentruth();
  auto& vs = nt.vertices();

  ////

  const int num_numdens = 3;
  const bool dijet      = true;
  numdens nds[num_numdens] = {
    numdens("nocuts"),
    numdens("ntracks"),
    numdens("all")
  };

  enum { k_decay_x, k_decay_y, k_decay_z, k_decay_xy, k_lspdist2, k_lspdist3, k_lspdistz, k_movedist2, k_movedist3, k_lspeta,k_lsppt, k_lspgammabeta, k_lspctau, k_npv, k_pvz, k_dist2dpvbs, k_pvrho, k_pvntracks, k_pvscore, k_ht, k_njets, k_nmuons, k_muon_pT, k_muon_abseta, k_muon_iso, k_muon_absdxybs, k_muon_absdz, k_muon_nsigmadxybs, k_neles, k_ele_pT, k_ele_abseta, k_ele_iso, k_ele_absdxybs, k_ele_absdz, k_ele_nsigmadxybs, k_met_pT, k_w_pT, k_w_mT, k_z_pT, k_z_m, k_lnu_absphi, k_ljet_absdr, k_ljet0_absdr, k_ljet1_absdr, k_nujet0_absphi, k_nujet1_absphi, k_wjet_dphi, k_zjet_dphi, k_jet_asymm, k_jet0_eta, k_jet1_eta, k_llp_category, k_jet_dr, k_jet_costheta, k_jet_asymsump, k_jet_deta, k_jet_dphi, k_jet_dind, k_pt0, k_pt1, k_ntks_j0, k_ntks_j1, k_jet_dr_minj0_q0, k_jet_dr_minj1_q1, k_ntk0_ntk1, k_boost0_boost1, k_jet0_trk_pt, k_jet1_trk_pt, k_jet0_trk_p, k_jet1_trk_p, k_jet0_trk_dr, k_jet1_trk_dr, k_jet0_trk_dz, k_jet1_trk_dz, k_jet0_trk_vtxdxy, k_jet1_trk_vtxdxy, k_jet0_trk_vtxdz, k_jet1_trk_vtxdz, k_jet0_trk_nsigmavtxdz, k_jet1_trk_nsigmavtxdz, k_jet0_trk_nsigmavtxdxy, k_jet1_trk_nsigmavtxdxy, k_jet0_trk_nsigmavtx, k_jet1_trk_nsigmavtx, k_jet0_trk_dzerr, k_jet1_trk_dzerr, k_jet0_trk_dxyerr, k_jet1_trk_dxyerr, k_jet0_trk_eta, k_jet1_trk_eta, k_jet0_sump, k_jet1_sump, k_jet0_sump_jetdr, k_jet1_sump_jetdr, k_movedist3_jetdr, k_movedist3_tightcloseseedtks, k_jet_costheta_tightcloseseedtks, k_jet_dr_tightcloseseedtks, k_movedist3_closeseedtks, k_jet_costheta_closeseedtks, k_jet_dr_closeseedtks, k_jet1_sump_jetdphi, k_jet1_ntks_jetdphi, k_jet0_maxeta_jet1_maxeta, k_jet0_sumeta_jet1_sumeta, k_jet0_sump_jet1_sump, k_qrktosump_j0, k_qrktosump_j1, k_qrktosump_sumpj0, k_qrktosump_sumpj1, k_2p0p1_1mgencos, k_2sump0sump1_1mcos, k_1mcosto1mgencos, k_2genlogm, k_2logm, k_asymjet_jetdr,k_closeseed_trk_gendz, k_closeseed_trk_genmissdist, k_closeseed_trk_gennsigmadz, k_jet0_trk_gennsigma, k_jet1_trk_gennsigma, k_jet0_trk_gennsigmamissdist, k_jet1_trk_gennsigmamissdist, k_jet0_trk_genmissdist, k_jet1_trk_genmissdist, k_jet0_trk_gennsigmadz, k_jet1_trk_gennsigmadz, k_jet0_trk_gendz, k_jet1_trk_gendz, k_jet0_trk_whichpv, k_jet1_trk_whichpv, k_jet0_trk_dsz, k_jet1_trk_dsz, k_jet0_trk_dxy, k_jet1_trk_dxy, k_jet0_trk_nsigmadxy, k_jet1_trk_nsigmadxy, k_nmovedtracks, k_dphi_sum_j_mv, k_deta_sum_j_mv, k_dphi_sum_q_mv, k_jetpt0_asymm, k_jetpt1_asymm, k_jeteta0_asymm, k_jeteta1_asymm, k_jetdr_asymm, k_jetdravg, k_angle0, k_angle1, k_dphi_j0_mv, k_dphi_j1_mv, k_deta_j0_mv, k_deta_j1_mv, k_dphi_q0_mv, k_dphi_q1_mv, k_nseedtracks, k_miscseedtracks, k_closeseedtks, k_tightcloseseedtks, k_movedseedtks, k_movedcloseseedtks, k_movedvtxseedtks, k_rat_moved_to_closetks, k_rat_moved_to_vtxtks, k_jetdphimax, k_jetdetamax, k_qrkdphimax, k_jetdphi_mveta, k_jetmovea3d01, k_jeteta01, k_jetpt01, k_pt_angle0, k_pt_angle1, k_eta_angle0, k_eta_angle1, k_nvtx, k_vtxbs2derr, k_vtxunc, k_vtxeta, k_vtxz, k_vtxdbv, k_vtx3dbv, k_vtxntk};

  for (numdens& nd : nds) {
    nd.book(k_decay_x,  "decay_x" , ";SV Decay X-pos [cm]; arb. units", 100, -4, 4);
    nd.book(k_decay_y,  "decay_y" , ";SV Decay Y-pos [cm]; arb. units", 100, -4, 4);
    nd.book(k_decay_z,  "decay_z" , ";SV Decay Z-pos [cm]; arb. units", 100, -20, 20);
    nd.book(k_decay_xy, "decay_xy" , ";SV Decay X-pos [cm]; SV Decay Y-pos [cm]", 100, -10, 10, 100, -10, 10);
    nd.book(k_lspdist2, "lspdist2", ";2-dist between gen verts;events/0.01 cm", 200, 0, 2);
    nd.book(k_lspdist3, "lspdist3", ";3-dist between gen verts;events/0.01 cm", 200, 0, 2);
    nd.book(k_lspdistz, "lspdistz", ";z-dist between gen verts;events/0.01 cm", 200, 0, 2);
    nd.book(k_movedist2, "movedist2", ";movement 2-dist;events/0.01 cm", 200, 0, 2);
    nd.book(k_movedist3, "movedist3", ";movement 3-dist;events/0.01 cm", 200, 0, 2);
    nd.book(k_lspeta,    "movevectoreta"   , ";move vector eta;events/0.08 cm", 100, -4, 4);
    nd.book(k_lsppt,     "lsppt"    , ";Pt of LSP [GeV];events/bin", 50, 0, 1000);
    nd.book(k_lspgammabeta,     "lspgammabeta"    , ";#gamma#beta of LSP ;events/bin", 100, 0, 20);
    nd.book(k_lspctau,     "lspctau"    , ";c#tau of LSP ;events/bin", 100, 0, 2);
    nd.book(k_npv, "npv", ";# PV;events/1", 100, 0, 100);
    nd.book(k_pvz, "pvz", ";PV z (cm);events/0.24 cm", 200, -24, 24);
    nd.book(k_dist2dpvbs, "dist2dpvbs", ";dist2d(pvs,bs) (cm);events/0.24 cm", 100, -0.1, 0.1);
    nd.book(k_pvrho, "pvrho", ";PV #rho (cm);events/1 #mum", 200, 0, 0.02);
    nd.book(k_pvntracks, "pvntracks", ";PV # tracks;events/2", 200, 0, 400);
    nd.book(k_pvscore, "pvscore", ";PV #Sigma p_{T}^{2} (GeV^{2});events/200 GeV^{2}", 200, 0, 40000);
    nd.book(k_ht, "ht", ";#Sigma H_{T} (GeV);events/50 GeV", 20, 0, 1000);
    nd.book(k_njets, "njets", ";# jets;events/1", 20, 0, 20);
    nd.book(k_nmuons, "nmuons", ";# passed offline-sel muons;events/1", 10, 0, 10);
    nd.book(k_muon_pT, "muon_pT", ";muons p_{T} (GeV);events/1", 50, 0, 200);
    nd.book(k_muon_abseta, "muon_abseta", ";muons |#eta|; arb. units", 70, 0, 3.5);
    nd.book(k_muon_iso, "muon_iso", ";muons iso;events/1", 200, 0, 0.15);
    nd.book(k_muon_absdxybs, "muon_absdxybs", ";muons |dxy| cm; arb. units", 80, 0, 0.2);
    nd.book(k_muon_absdz, "muon_absdz", ";muons |dz| cm; arb. units", 80, 0, 1.0);
    nd.book(k_muon_nsigmadxybs, "muon_nsigmadxybs", ";muons n#sigma dxybs ; arb. units", 80, 0, 6.0);
    nd.book(k_neles, "neles", ";# passed offline-sel electrons;events/1", 10, 0, 10);
    nd.book(k_ele_pT, "ele_pT", ";electrons p_{T} (GeV);events/1", 50, 0, 200);
    nd.book(k_ele_abseta, "ele_abseta", ";electrons |#eta|; arb. units", 70, 0, 3.5);
    nd.book(k_ele_iso, "ele_iso", ";electrons iso;events/1", 200, 0, 0.15);
    nd.book(k_ele_absdxybs, "ele_absdxybs", ";electrons |dxy| cm; arb. units", 80, 0, 0.2);
    nd.book(k_ele_absdz, "ele_absdz", ";electrons |dz| cm; arb. units", 80, 0, 1.0);
    nd.book(k_ele_nsigmadxybs, "ele_nsigmadxybs", ";electrons n#sigma dxybs ; arb. units", 80, 0, 6.0);
    nd.book(k_met_pT, "met_pT", ";missing p_{T} (GeV);events/1", 50, 0, 200);
    nd.book(k_w_pT, "w_pT", ";RECO W(Z) boson's p_{T} (GeV);events/1", 50, 0, 200);
    nd.book(k_w_mT, "w_mT", ";RECO W boson's mass_{T} (GeV);events/1", 50, 0, 150);
    nd.book(k_z_pT, "z_pT", ";RECO Z boson's p_{T} (GeV);events/1", 50, 0, 200);
    nd.book(k_z_m, "z_m", ";RECO Z boson's inv. mass (GeV);events/1", 50, 0, 150);
    nd.book(k_lnu_absphi, "lnu_absphi", ";lepton-#nu |#DeltaPhi|; arb. units", 70, 0.0, 3.5);
    nd.book(k_ljet_absdr, "ljet_absdr", ";lepton-closest-jet |#DeltaPhi|; arb. units", 70, 0.0, 3.5);
    nd.book(k_ljet0_absdr, "ljet0_absdr", ";lepton-jet0 |#DeltaR|; arb. units", 70, 0.0, 3.5);
    nd.book(k_ljet1_absdr, "ljet1_absdr", ";lepton-jet1 |#DeltaR|; arb. units", 70, 0.0, 3.5);
    nd.book(k_nujet0_absphi, "nujet0_absphi", ";MET-jet0 |#DeltaPhi|; arb. units", 70, 0.0, 3.5);
    nd.book(k_nujet1_absphi, "nujet1_absphi", ";MET-jet0 |#DeltaPhi|; arb. units", 70, 0.0, 3.5);
    nd.book(k_wjet_dphi, "wjet_dphi", ";W(Z)-jet |#DeltaPhi|; arb. units", 70, 0.0, 3.5);
    nd.book(k_zjet_dphi, "zjet_dphi", ";Z-jet |#DeltaPhi|; arb. units", 70, 0.0, 3.5);
    nd.book(k_jet_asymm, "jet_asymm", ";jet pT asymmetry A_{J}; arb. units", 25, 0, 1);
    nd.book(k_jet0_eta, "jet0_eta", ";jet0's Eta; arb. units", 60, -3, 3);
    nd.book(k_jet1_eta, "jet1_eta", ";jet1's Eta; arb. units", 60, -3, 3);
    nd.book(k_llp_category, "llp_category", ";category 1-4 of llp decays", 5, 0, 5);
    nd.book(k_jet_dr, "jet_dr", ";jets' #DeltaR; arb. units", 70, 0, 7);
    nd.book(k_jet_costheta, "jet_costheta", ";jets' cos(#theta); arb. units", 80, -1, 1);
    nd.book(k_jet_asymsump, "jet_asymsump", ";jet's quality tracks sum mom. asymm. A_{J}", 20, -1, 1);
    nd.book(k_jet_deta, "jet_deta", ";jets' #DeltaEta; arb. units", 70, 0, 7);
    nd.book(k_jet_dphi, "jet_dphi", ";jets' #DeltaPhi; arb. units", 70, -3.5, 3.5);
    nd.book(k_jet_dind, "jet_dind", ";jets' #DeltaIndex; arb. units", 20, 0, 20);
    nd.book(k_pt0, "pt0", ";RECO jet0 pT [GeV]", 50, 0, 150);
    nd.book(k_pt1, "pt1", ";RECO jet1 pT [GeV]", 50, 0, 150);
    nd.book(k_ntks_j0, "ntks_j0", ";Ntks in jet0", 25, 0, 25);
    nd.book(k_ntks_j1, "ntks_j1", ";Ntks in jet1", 25, 0, 25);
    nd.book(k_jet_dr_minj0_q0, "jet_dr_minj0_q0", ";#DeltaR(minij0,quark0)", 70, 0, 7);
    nd.book(k_jet_dr_minj1_q1, "jet_dr_minj1_q1", ";#DeltaR(minij1,quark1)", 70, 0, 7);
    nd.book(k_ntk0_ntk1, "ntk0_ntk1", ";Ntks in jet0; Ntks in jet1; arb. units", 25, 0.0, 25, 25, 0.0, 25);
    nd.book(k_boost0_boost1, "boost0_boost1", ";#gamma#beta of quark0; #gamma#beta of quark1; arb. units", 50, 0.0, 200, 50, 0.0, 200);
    nd.book(k_jet0_trk_pt, "jet0_trk_pt", "; jet0-movedseed-track's pT; arb. units", 45, 0, 15);
    nd.book(k_jet1_trk_pt, "jet1_trk_pt", "; jet1-movedseed-track's pT; arb. units", 45, 0, 15);
    nd.book(k_jet0_trk_p, "jet0_trk_p", "; jet0-movedseed-track's p; arb. units", 45, 0, 15);
    nd.book(k_jet1_trk_p, "jet1_trk_p", "; jet1-movedseed-track's p; arb. units", 45, 0, 15);
    nd.book(k_jet0_sump, "jet0_sump", "; jet0-movedseed-track's sum p; arb. units", 80, 0, 80);
    nd.book(k_jet1_sump, "jet1_sump", "; jet1-movedseed-track's sum p; arb. units", 80, 0, 80);
    nd.book(k_jet0_sump_jetdr, "jet0_sump_jetdr", "; jet0-movedseed-track's sum p;jets #DeltaR", 80, 0, 80, 50, 0, 3.5);
    nd.book(k_jet1_sump_jetdr, "jet1_sump_jetdr", "; jet1-movedseed-track's sum p;jets #DeltaR", 80, 0, 80, 50, 0, 3.5);
    nd.book(k_movedist3_jetdr, "movedist3_jetdr", "; movement 3-dist;jets #DeltaR", 100, 0, 2, 50, 0, 3.5);
    nd.book(k_movedist3_tightcloseseedtks, "movedist3_tightcloseseedtks", ";movement 3-dist ;# tracks 2#sigma-close to artificial vtx", 100, 0, 2, 25, 0, 25);
    nd.book(k_jet_costheta_tightcloseseedtks, "jet_costheta_tightcloseseedtks", "; jets' cos(#theta);# tracks 2#sigma-close to artificial vtx", 80, -1, 1, 25, 0, 25);
    nd.book(k_jet_dr_tightcloseseedtks, "jet_dr_tightcloseseedtks", "; jets' #DeltaR;# tracks 2#sigma-close to artificial vtx", 70, 0, 7, 25, 0, 25);
    nd.book(k_movedist3_closeseedtks, "movedist3_closeseedtks", ";movement 3-dist ;# tracks close to artificial vtx", 100, 0, 2, 25, 0, 25);
    nd.book(k_jet_costheta_closeseedtks, "jet_costheta_closeseedtks", "; jets' cos(#theta);# tracks close to artificial vtx", 80, -1, 1, 25, 0, 25);
    nd.book(k_jet_dr_closeseedtks, "jet_dr_closeseedtks", "; jets' #DeltaR;# tracks close to artificial vtx", 70, 0, 7, 25, 0, 25);
    nd.book(k_jet1_sump_jetdphi, "jet1_sump_jetdphi", "; jet1-movedseed-track's sum p;jets #DeltaPhi", 80, 0, 80, 70, -3.5, 3.5);
    nd.book(k_jet1_ntks_jetdphi, "jet1_ntks_jetdphi", "; Ntks in jet1;jets #DeltaPhi", 25, 0, 25, 70, -3.5, 3.5);
    nd.book(k_jet0_maxeta_jet1_maxeta, "jet0_maxeta_jet1_maxeta", "; max(jet0-movedseed-track's Eta); max(jet1-movedseed-track's Eta)", 60, -3, 3, 60, -3, 3); 
    nd.book(k_jet0_sumeta_jet1_sumeta, "jet0_sumeta_jet1_sumeta", "; jet0-movedseed-track's sum |Eta|; jet1-movedseed-track's sum |Eta|", 100, 0, 25, 100, 0, 25); 
    nd.book(k_jet0_sump_jet1_sump, "jet0_sump_jet1_sump", "; jet0-movedseed-track's sum p; jet1-movedseed-track's sum p", 80, 0, 80, 80, 0, 80); 
    nd.book(k_qrktosump_j0, "qrktosump_j0", "; #frac{jet0-movedseed-track's sum p}{quark0's p}; arb. units", 50, 0, 1);
    nd.book(k_qrktosump_j1, "qrktosump_j1", "; #frac{jet1-movedseed-track's sum p}{quark1's p}; arb. units", 50, 0, 1);
    nd.book(k_qrktosump_sumpj0, "qrktosump_sumpj0", "; jet0-movedseed-track's sum p; #frac{jet0-movedseed-track's sum p}{quark0's p}; arb. units", 50, 0, 50, 50, 0, 1);
    nd.book(k_qrktosump_sumpj1, "qrktosump_sumpj1", "; jet1-movedseed-track's sum p; #frac{jet1-movedseed-track's sum p}{quark1's p}; arb. units", 50, 0, 50, 50, 0, 1);
    nd.book(k_2p0p1_1mgencos, "2p0p1_1mgencos", "; log(2*p_{quark0}*p_{quark1}); log(1-cos(#Delta#Theta))", 70, 0, 7, 20, -2, 0);
    nd.book(k_2sump0sump1_1mcos, "2sump0sump1_1mcos", "; log(2*sump_{tk0}*sump_{tk1}); log(1-cos(#Delta#Theta))", 70, 0, 7, 20, -2, 0);
    nd.book(k_1mcosto1mgencos, "1mcosto1mgencos", "; #frac{1-cos(#Delta#Theta)_{minijet}}{1-cos(#Delta#Theta)_{GEN}}", 20, 0, 1);
    nd.book(k_2logm, "2logm", "; log(2*sump_{tk0}*sump_{tk1}) + log(1-cos(#Delta#Theta))", 70, 0, 7);
    nd.book(k_2genlogm, "2genlogm", "; log(2*p_{quark0}*p_{quark1}) + log(1-cos(#Delta#Theta))", 70, 0, 7);
    nd.book(k_asymjet_jetdr, "asymjet_jetdr", ";jet's quality tracks sum mom. asymm. A_{J}; jets's movedseed-track p4 #DeltaR ", 20, -1, 1, 50, 0, 3.5);
    nd.book(k_jet0_trk_dr, "jet0_trk_dr", "; jet0-movedseed-track's DeltaR-to-jet; arb. units", 45, 0, 0.5);
    nd.book(k_jet1_trk_dr, "jet1_trk_dr", "; jet1-movedseed-track's DeltaR-to-jet; arb. units", 45, 0, 0.5);
    nd.book(k_jet0_trk_dz, "jet0_trk_dz", "; jet0-movedseed-track's dz; arb. units", 50, -1.0, 1.0);
    nd.book(k_jet1_trk_dz, "jet1_trk_dz", "; jet1-movedseed-track's dz; arb. units", 50, -1.0, 1.0);
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
    nd.book(k_closeseed_trk_genmissdist, "closeseed_trk_genmissdist", "; close-seed-track's missdist to LLP; arb. units", 50, -0.05, 0.05);
    nd.book(k_closeseed_trk_gendz, "closeseed_trk_gendz", "; close-seed-track's dz to LLP; arb. units", 50, -0.05, 0.05);
    nd.book(k_closeseed_trk_gennsigmadz, "closeseed_trk_gennsigmadz", "; close-seed-track's gennsigmadz; arb. units", 80, -10, 10);
    nd.book(k_jet0_trk_gennsigma, "jet0_trk_gennsigma", "; jet0-movedseed-track's n#sigma to LLP; arb. units", 80, -10, 10);
    nd.book(k_jet1_trk_gennsigma, "jet1_trk_gennsigma", "; jet1-movedseed-track's n#sigma to LLP; arb. units", 80, -10, 10);
    nd.book(k_jet0_trk_gennsigmamissdist, "jet0_trk_gennsigmamissdist", "; jet0-movedseed-track's n#sigma missdist to LLP; arb. units", 80, -10, 10);
    nd.book(k_jet1_trk_gennsigmamissdist, "jet1_trk_gennsigmamissdist", "; jet1-movedseed-track's n#sigma missdist to LLP; arb. units", 80, -10, 10);
    nd.book(k_jet0_trk_genmissdist, "jet0_trk_genmissdist", "; jet0-movedseed-track's missdist to LLP; arb. units", 50, -0.05, 0.05);
    nd.book(k_jet1_trk_genmissdist, "jet1_trk_genmissdist", "; jet1-movedseed-track's missdist to LLP; arb. units", 50, -0.05, 0.05);
    nd.book(k_jet0_trk_gennsigmadz, "jet0_trk_gennsigmadz", "; jet0-movedseed-track's n#sigma dz to LLP; arb. units", 80, -10, 10);
    nd.book(k_jet1_trk_gennsigmadz, "jet1_trk_gennsigmadz", "; jet1-movedseed-track's n#sigma dz to LLP; arb. units", 80, -10, 10);
    nd.book(k_jet0_trk_gendz, "jet0_trk_gendz", "; jet0-movedseed-track's dz to LLP; arb. units", 50, -0.05, 0.05);
    nd.book(k_jet1_trk_gendz, "jet1_trk_gendz", "; jet1-movedseed-track's dz to LLP; arb. units", 50, -0.05, 0.05);
    nd.book(k_jet0_trk_whichpv, "jet0_trk_whichpv", "; jet1-movedseed-track's which_pv; arb. units", 260, 0.0, 260);
    nd.book(k_jet1_trk_whichpv, "jet1_trk_whichpv", "; jet1-movedseed-track's which_pv; arb. units", 260, 0.0, 260);
    nd.book(k_jet0_trk_dsz, "jet0_trk_dsz", "; jet0-movedseed-track's dsz; arb. units", 50, -1.0, 1.0);
    nd.book(k_jet1_trk_dsz, "jet1_trk_dsz", "; jet1-movedseed-track's dsz; arb. units", 50, -1.0, 1.0);
    nd.book(k_jet0_trk_dxy, "jet0_trk_dxy", "; jet0-movedseed-track's dxybs; arb. units", 50, -0.5, 0.5);
    nd.book(k_jet1_trk_dxy, "jet1_trk_dxy", "; jet1-movedseed-track's dxybs; arb. units", 50, -0.5, 0.5);
    nd.book(k_jet0_trk_nsigmadxy, "jet0_trk_nsigmadxy", "; jet0-movedseed-track's nsigmadxybs; arb. units", 80, -10, 10);
    nd.book(k_jet1_trk_nsigmadxy, "jet1_trk_nsigmadxy", "; jet1-movedseed-track's nsigmadxybs; arb. units", 80, -10, 10);
    nd.book(k_nmovedtracks, "nmovedtracks", ";# moved tracks;events/2", 120, 0, 120);
    nd.book(k_dphi_sum_j_mv, "dphi_sum_j_mv", ";abs #Delta #phi between jet0+jet1 and move vec;events/bin", 63, 0, M_PI);
    nd.book(k_deta_sum_j_mv, "deta_sum_j_mv", ";abs #Delta #eta between jet0+jet1 and move vec;events/bin", 25, 0, 4);
    nd.book(k_dphi_sum_q_mv, "dphi_sum_q_mv", ";abs #Delta #phi between jet0+jet1 and move vec;events/bin", 63, 0, M_PI);

    nd.book(k_jetpt0_asymm, "jetpt0_asymm", ";jet p_{T} 0; jet asymm. A_{J}", 50, 0, 1000, 25, 0, 1);
    nd.book(k_jetpt1_asymm, "jetpt1_asymm", ";jet p_{T} 1; jet asymm. A_{J}", 50, 0, 1000, 25, 0, 1);
    nd.book(k_jeteta0_asymm, "jeteta0_asymm", ";jet #eta 0; jet asymm. A_{J}", 100, -4, 4, 25, 0, 1);
    nd.book(k_jeteta1_asymm, "jeteta1_asymm", ";jet #eta 1; jet asymm. A_{J}", 100, -4, 4, 25, 0, 1);
    nd.book(k_jetdr_asymm, "jetdr_asymm", ";jets #DeltaR; jet asymm. A_{J}", 70, 0, 7, 25, 0, 1);
    nd.book(k_jetdravg, "jetdravg", ";avg jet #Delta R;events/0.1", 70, 0, 7);
    nd.book(k_angle0, "jetmovea3d0", ";Angle between jet0 and SV;arb. units", 63, 0, M_PI);
    nd.book(k_angle1, "jetmovea3d1", ";Angle between jet1 and SV;arb. units", 63, 0, M_PI);
    nd.book(k_dphi_j0_mv, "dphi_j0_mv", ";abs #Delta #phi between jet0 and move vec;events/bin", 63, 0, M_PI);
    nd.book(k_dphi_j1_mv, "dphi_j1_mv", ";abs #Delta #phi between jet1 and move vec;events/bin", 63, 0, M_PI);
    nd.book(k_deta_j0_mv, "deta_j0_mv", ";abs #Delta #eta between jet0 and move vec;events/bin", 25, 0, 4);
    nd.book(k_deta_j1_mv, "deta_j1_mv", ";abs #Delta #eta between jet1 and move vec;events/bin", 25, 0, 4);
    nd.book(k_dphi_q0_mv, "dphi_q0_mv", ";abs #Delta #phi between qrk0 and move vec;events/bin", 63, 0, M_PI);
    nd.book(k_dphi_q1_mv, "dphi_q1_mv", ";abs #Delta #phi between qrk1 and move vec;events/bin", 63, 0, M_PI);
    nd.book(k_nseedtracks, "nseedtracks", ";# seed tracks;events", 80, 0, 80);
    nd.book(k_miscseedtracks, "miscseedtracks", ";#Sigma seed tks not from moved jets;count", 80, 0, 80);
    nd.book(k_closeseedtks,  "closeseedtks", ";# tracks close to artificial vtx.;count", 80, 0, 80);
    nd.book(k_tightcloseseedtks,  "tightcloseseedtks", ";# tracks 2#sigma-close to artificial vtx.;count", 25, 0, 25);
    nd.book(k_movedseedtks,  "movedseedtks", ";# moved seed tracks;count", 30, 0, 30);
    nd.book(k_movedvtxseedtks,  "movedvtxseedtks", ";# moved seed tracks in vtx;count", 30, 0, 30);
    nd.book(k_movedcloseseedtks,  "movedcloseseedtks", ";# moved seed tracks 5#sigma to LLP;count", 30, 0, 30);
    nd.book(k_rat_moved_to_closetks, "rat_moved_to_closetks", ";#frac{# moved seed tracks 5#sigma to LLP}{# seed tracks 5#sigma to LLP};count", 50, 0, 1);
    nd.book(k_rat_moved_to_vtxtks, "rat_moved_to_vtxtks", ";#frac{# moved seed tracks in vtx}{# vtx ntrack};count", 50, 0, 1);
    nd.book(k_jetdphimax, "jetdphimax", ";max jet #Delta #phi; events", 32, -M_PI, M_PI);
    nd.book(k_jetdetamax, "jetdetamax", ";max jet #Delta #eta; events", 200, -5, 5);
    nd.book(k_qrkdphimax, "qrkdphimax", ";abs. max qrk #Delta #phi; events", 75, -3.5, 3.5);
    nd.book(k_jetdphi_mveta, "jetdphi_mveta", ";abs(max jet #Delta #phi);abs( #eta of disp. vector)", 32, 0, M_PI, 40, 0, 4);

    nd.book(k_jetmovea3d01, "jetmovea3d", ";3D angle between jet 0 and move vector;3D angle between jet 1 and move vector", 63, 0, M_PI, 63, 0, M_PI);
    nd.book(k_jeteta01, "jeteta01", ";jet #eta 0 (GeV);jet #eta 1 (GeV)", 100, -4, 4, 100, -4, 4);
    nd.book(k_jetpt01, "jetpt01", ";jet p_{T} 0 (GeV);jet p_{T} 1 (GeV)", 50, 0, 1000, 50, 0, 1000);
    nd.book(k_pt_angle0,     "pt_angle0"    , ";Pt of jet0 [GeV]; Angle between jet0 and SV", 50, 0, 2500, 63, 0, M_PI);
    nd.book(k_pt_angle1,     "pt_angle1"    , ";Pt of jet1 [GeV]; Angle between jet1 and SV", 50, 0, 2500, 63, 0, M_PI);
    nd.book(k_eta_angle0,    "eta_angle0"  , ";Eta of SV decay vector; Angle between jet0 and SV", 60, -5, 5, 63, 0, M_PI);
    nd.book(k_eta_angle1,    "eta_angle1"  , ";Eta of SV decay vector; Angle between jet1 and SV", 60, -5, 5, 63, 0, M_PI);
    nd.book(k_nvtx, "nvtx", ";number of vertices;events/1", 8, 0, 8);
    nd.book(k_vtxbs2derr, "vtxbs2derr", ";bs2derr of vertex;events", 500, 0, 0.05);
    nd.book(k_vtxunc, "vtxunc", ";dist3d(move vector, vtx) cm; arb. units", 200, 0, 0.2);
    nd.book(k_vtxeta, "vtxeta", ";eta of vertex;events", 100, -4, 4);
    nd.book(k_vtxz, "vtxz", ";z pos of vertex;events", 100, -10, 10);
    nd.book(k_vtxdbv, "vtxdbv", ";2D displacement of vertex to a beamspot;events", 50, 0, 2);
    nd.book(k_vtx3dbv, "vtx3dbv", ";3D displacement of vertex to a beamspot;events", 50, 0, 2);
    nd.book(k_vtxntk, "vtxntk", ";ntrack of vertex;events", 20, 0, 20);
  }

  TH1D* h_vtxntracks[num_numdens] = {0};
  TH1D* h_vtxbs2derr[num_numdens] = {0};
  //TH1D* h_vtxtkonlymass[num_numdens] = {0}; // JMTBAD interface for vertex_tracks common to Mini2 and MovedTracks ntuples
  TH1D* h_vtxs_mass[num_numdens] = {0};

  for (int i = 0; i < num_numdens; ++i) {
    h_vtxntracks[i] = new TH1D(TString::Format("h_%i_vtxntracks",      i), ";# tracks in largest vertex;events/1", 40, 0, 40);
    h_vtxbs2derr[i] = new TH1D(TString::Format("h_%i_vtxbs2derr",      i), ";#sigma(d_{BV}) of largest vertex (cm);events/2 #mum", 50, 0, 0.01);
    //h_vtxtkonlymass[i] = new TH1D(TString::Format("h_%i_vtxtkonlymass", i), ";track-only mass of largest vertex (GeV);events/1 GeV", 500, 0, 500);
    h_vtxs_mass[i] = new TH1D(TString::Format("h_%i_vtxs_mass", i), ";track+jets mass of largest vertex (GeV);vertices/50 GeV", 100, 0, 5000);
  }

  double den = 0;
  std::map<std::string, double> nums;

  auto fcn = [&]() {
    const double w = nr.weight();

    // First part of the preselection: our offline jet requirements
    // plus require the lsps to be far enough apart that they don't
    // interfere with each other in reconstruction
    if (!gen.valid() || gen.lspdist3() < min_lspdist3) //FIXME 
      NR_loop_cont(w);

    for (numdens& nd : nds)
      nd.setw(w);


    const size_t nvtx = vs.n();
    const double lspdist2 = gen.lspdist2();
    const double lspdist3 = gen.lspdist3();
    const double lspdistz = gen.lspdistz();

    const float  close_criteria = 5.0;  // How close must a seed track pass near an SV to be considered 'close?'
    const float  tight_close_criteria = 2.0;  // How close must a seed track pass near an SV to be considered 'close?'
    std::vector<int> tks_in_lspjets;

    int n_miscseedtracks = 0;
    int n_movedseedtks = 0;
    
    // Instantiate some jet, leptons & quark variables to be filled later
    int nselmuons = 0, nseleles = 0;
    TLorentzVector muon_p4;
    TLorentzVector ele_p4;
    TLorentzVector tmpz_p4;
    TLorentzVector zee_p4;
    TLorentzVector zmumu_p4;
    bool has_Zmumuboson = false;
    bool has_Zeeboson = false;
    bool has_Wboson = false;
    double z_m = -99, zmumu_m = -99, zee_m = -99;
    double z_pT = -99, zmumu_pT = -99, zee_pT = -99;

    double muon_pT = -99, ele_pT = -99;
    double muon_px = -99, ele_px = -99;
    double muon_py = -99, ele_py = -99;
    double muon_pz = -99, ele_pz = -99;
    double muon_q = -99, ele_q = -99;
    double muon_abseta = -99, ele_abseta = -99;
    double muon_iso = 99, ele_iso = 99;
    double muon_absdxybs = -99, ele_absdxybs = -99;
    double muon_nsigmadxybs = -99, ele_nsigmadxybs = -99;
    double muon_absdz = -99, ele_absdz = -99;
    double met_pT = std::hypot(pf.met_x(), pf.met_y());
    double lnu_absphi = -99, ljet_absdr = -99, ljet0_absdr = -99,  ljet1_absdr = -99, nujet0_absphi = -99, nujet1_absphi = -99;
    double w_mT = -99;
    double w_pT = -99;

    float   jet_aj = -9.9, jet_dr = -9.9, jet_deta = -9.9, jet_dphi = -9.9, jet_dind = -9.9, jet_pt_0 = -9.9, jet_pt_1 = -9.9;
    float   jet_dr_minjq0 = -9.9, jet_dr_minjq1 = -9.9;
    float   jet_eta_0 = -100.0, jet_eta_1 = -100.0;
    double  jet0_lsp_angle = -9.9, jet1_lsp_angle = -9.9;
    double  jet_mv_dphi_0  = 0.0, jet_mv_dphi_1 = 0.0, jet_mv_dphi_sum = 0.0;
    double  jet_mv_deta_0  = 0.0, jet_mv_deta_1 = 0.0, jet_mv_deta_sum = 0.0;
    double  qrk_mv_dphi_0  = 0.0, qrk_mv_dphi_1 = 0.0, qrk_mv_dphi_sum = 0.0;
    double  jet_dphi_max = 0.0;
    double  jet_deta_max = 0.0;
    double  qrk_dphi_max = 0.0;
    int     jet_ntks_0 = -10, jet_ntks_1 = -10;
    double  boost0 = -10, boost1 = -10;
    int n_closeseedtks = 0;
    int n_movedcloseseedtks = 0;
    int n_tightcloseseedtks = 0;
    int n_movedvtxseedtks = 0;
    const int nseedtracks = tks.nseed(bs);
    double sump_0 = 0;
    double sump_1 = 0;
    double maxeta_0 = 0.0;
    double maxeta_1 = 0.0;
    double sumeta_0 = 0.0;
    double sumeta_1 = 0.0;
    double qrkp_0 = -9.9;
    double qrkp_1 = -9.9;
    double qrk_costheta = -9.9;
    double jet_costheta = -9.9;
    int llp_category = -99;
    std::vector<int> closeseedtrk_idx;
    std::vector<int> jet0trk_idx;
    std::vector<int> jet1trk_idx;
    double  wjet_dphi = 99, zjet_dphi = 99;

    TLorentzVector minijet_p4_0;
    TLorentzVector minijet_p4_1;

    // Loop over each LSP
    for (int ilsp = 0; ilsp < 2; ++ilsp) {
      const TVector3 lspdecay(gen.decay(ilsp,bs).x() -pvs.x(0), gen.decay(ilsp,bs).y() -pvs.y(0), gen.decay(ilsp,bs).z()-pvs.z(0));  // JMTBAD BS BS
      const double movedist2 = lspdecay.Perp();
      const double movedist3 = lspdecay.Mag();
      const TLorentzVector lsp_p4 = gen.p4(ilsp);

      // Second part of preselection: only look at move vectors
      // ~inside the beampipe // JMTBAD the 2.0 cm requirement isn't
      // exact
      if (movedist2 < 0.01 || movedist2 > 2.0) //FIXME
        continue;

      if (dijet) {
        //assert(abs(gen.id(ilsp)) == 1000006); // stop pair production


        for (int i = 0, ie = muons.n(); i < ie; ++i) {
          if (muons.pt(i) > 20.0 && abs(muons.eta(i)) < 2.4 && muons.isMed(i) && muons.iso(i) < 0.15) {
            double tmp_muon_absdxybs = abs(muons.dxybs(i, bs));
            double tmp_muon_absdz = muons.dzpv(i, pvs); 
            bool muon_IP_cut = tmp_muon_absdxybs < 0.02 && tmp_muon_absdz < 0.5;
            if (muon_IP_cut && muons.pt(i) > 29.0 && abs(muons.eta(i)) < 2.4 && muons.isMed(i) && muons.iso(i) < 0.15) {
              nselmuons += 1;
              if (nselmuons == 1) {
                muon_pT = muons.pt(i);
                muon_px = muons.px(i);
                muon_py = muons.py(i);
                muon_pz = muons.pz(i);
                muon_p4.SetPxPyPzE(muon_px, muon_py, muon_pz, muon_pT);
                muon_q = muons.q(i);
                muon_abseta = abs(muons.eta(i));
                muon_iso = muons.iso(i);
                muon_absdxybs = abs(muons.dxybs(i, bs));
                muon_absdz = muons.dzpv(i, pvs); 
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
        }

        if (has_Zmumuboson) {
          zmumu_m = tmpz_p4.M();
          zmumu_pT = tmpz_p4.Pt();
          zmumu_p4 = tmpz_p4;
        }
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
              ele_px = electrons.px(i);
              ele_py = electrons.py(i);
              ele_pz = electrons.pz(i);
              ele_p4.SetPxPyPzE(ele_px, ele_py, ele_pz, ele_pT);
              ele_abseta = abs(electrons.eta(i));
              ele_q = electrons.q(i);
              ele_iso = electrons.iso(i);
              ele_absdxybs = abs(electrons.dxybs(i, bs));
              ele_absdz = electrons.dzpv(i, pvs); 
              ele_nsigmadxybs = electrons.nsigmadxybs(i, bs);
              tmpz_p4 += ele_p4;

            }

            if (has_Zeeboson == false && nseleles > 0 && ele_q * electrons.q(i) == -1) {
              TLorentzVector antiele_p4;
              antiele_p4.SetPxPyPzE(electrons.px(i), electrons.py(i), electrons.pz(i), electrons.p(i));
              tmpz_p4 += antiele_p4;
              has_Zeeboson = true;
            }
          }
        }

        TLorentzVector met_p4;
        met_p4.SetPtEtaPhiM(met_pT, 0, pf.met_phi(), 0);
        TLorentzVector w_p4;

        if (met_p4.Pt() > 25) {
          if (nselmuons > 0) {
            has_Wboson = true;
            w_p4 = met_p4 + muon_p4;
            w_pT = w_p4.Pt();
            lnu_absphi = abs(muon_p4.DeltaPhi(met_p4));
            w_mT = w_p4.Mt();
          }
          else if (nseleles > 0 && nselmuons == 0) {
            has_Wboson = true;
            w_p4 = met_p4 + ele_p4;
            w_pT = w_p4.Pt();
            lnu_absphi = abs(ele_p4.DeltaPhi(met_p4));
            w_mT = w_p4.Mt();
          }
        }
        if (has_Zeeboson) {
          zee_m = tmpz_p4.M();
          zee_pT = tmpz_p4.Pt();
          zee_p4 = tmpz_p4;
        }

        // Match decay daughters to the closest (by dR) reconstructed jet
        std::vector<int> closest_jets(2,-1), quark_assoc(2,-1);
        int s = 2+ilsp*2, swapem = gen.pt(s) < gen.pt(s+1); // toward making the jet assoc'd to the higher (lower) pT quark be "jet0" ("jet1")
        for (int i = 0; i < 2; ++i) {
          const int iq = s + (swapem ? !i : i);
          //assert(gen.id(iq) == -1000006 / gen.id(ilsp)); // stop -> dbar dbar + c.c.

          jmt::MinValue m(0.4);
          for (int j = 0, je = jets.n(); j < je; ++j)
            m(j, gen.p4(iq).DeltaR(jets.p4(j)));

          closest_jets[i] = m.i();
          quark_assoc[i] = iq;
        }

        closeseedtrk_idx = {};
        n_closeseedtks = 0;
        n_movedcloseseedtks = 0;
        n_tightcloseseedtks = 0;
        n_movedvtxseedtks = 0;
        n_miscseedtracks = 0;
        // Start calculating significances of closest approach and count # of close seed tracks
        for (int it=0, ite = tks.n(); it < ite; it++) {
          if (tks.pass_seed(it, bs)) {

            n_miscseedtracks++; // Count up all seed tracks. Will subtract out the matching tracks later.

            std::vector<double> sigs_quad;

            for (int il = 0; il < 2; il++) {
              const double temp_sigdxy = tks.dxy(it, gen.decay_x(il), gen.decay_y(il))/tks.err_dxy(it);
              const double temp_sigdz  = tks.dz(it, gen.decay_x(il), gen.decay_y(il), gen.decay_z(il))/tks.err_dz(it);
              const double sum_sq_sig = hypot(temp_sigdxy, temp_sigdz);
              sigs_quad.push_back(sum_sq_sig);
            }      


            // Count how many 'close' seed tracks there are
            if ( sigs_quad[ilsp] < close_criteria){
              n_closeseedtks++;
              closeseedtrk_idx.push_back(it);
              auto it0 = std::find(jet0trk_idx.begin(), jet0trk_idx.end(), it);
              auto it1 = std::find(jet1trk_idx.begin(), jet1trk_idx.end(), it);
              if (it0 != jet0trk_idx.end() || it1 != jet1trk_idx.end()) n_movedcloseseedtks++;
            }

            if ( sigs_quad[ilsp] < tight_close_criteria){
              n_tightcloseseedtks++;
            }

            if (((sigs_quad[0] < close_criteria) or  (sigs_quad[1] < close_criteria)) )
              n_miscseedtracks--;

          }

        }


        // Last hidden part of the preselection: skip events where
        // daughter doesn't match to a jet or both match to the same
        // jet // JMTBAD how many are we skipping?
        TLorentzVector jet_p4_0;
        TLorentzVector jet_p4_1;
        const TLorentzVector quark_p4_0 = gen.p4(quark_assoc[0]);
        const TLorentzVector quark_p4_1 = gen.p4(quark_assoc[1]);


        if (closest_jets[0] == -1 || closest_jets[1] == -1){
          llp_category = 1;
          if (closest_jets[0] != -1) {
            llp_category = 2;
          }
          if (closest_jets[1] != -1) {
            llp_category = 3;
          }
        }
        else {
          llp_category = 4;
        }



        int minijet_ntk_0 = 0;
        int minijet_ntk_1 = 0;
        n_movedseedtks = 0;
        sump_0 = 0;
        sump_1 = 0;
        maxeta_0 = 0;
        maxeta_1 = 0;
        sumeta_0 = 0;
        sumeta_1 = 0;
        minijet_p4_0.SetPxPyPzE(0, 0, 0, 0);
        minijet_p4_1.SetPxPyPzE(0, 0, 0, 0);
        jet0trk_idx = {};
        jet1trk_idx = {};
        for (int j = 0; j < tks.n(); ++j) {
          const TLorentzVector jp4 = tks.p4(j);
          if ( tks.pass_sel(j) && (tks.which_pv(j) == 0 || tks.which_pv(j) == 255) && jp4.DeltaR(quark_p4_0) < 0.4 ){ //FIXME apply which_pv            
          //if ( jp4.DeltaR(quark_p4_0) < 0.4 ){ //FIXME apply which_pv            
          //auto it0 = std::find(jet0_tracks.begin(), jet0_tracks.end(), j);
          //if (tks.pass_sel(j) && it0 != jet0_tracks.end()){
            minijet_p4_0 += tks.p4(j);
            minijet_ntk_0 += 1;
            if (tks.pass_seed(j, bs)) jet0trk_idx.push_back(j);
            sump_0 += tks.p(j);
            sumeta_0 += fabs(tks.eta(j));
            if (fabs(tks.eta(j)) > fabs(maxeta_0)) maxeta_0 = tks.eta(j);
            if (tks.pass_seed(j, bs)) n_movedseedtks++;
          }
          if ( tks.pass_sel(j) && (tks.which_pv(j) == 0 || tks.which_pv(j) == 255) && jp4.DeltaR(quark_p4_1) < 0.4 ){ //FIXME apply which_pv
          //if ( jp4.DeltaR(quark_p4_1) < 0.4 ){ //FIXME apply which_pv
          //auto it1 = std::find(jet1_tracks.begin(), jet1_tracks.end(), j);
          //if ( tks.pass_sel(j) && it1 != jet1_tracks.end()){
            auto it1 = std::find(jet0trk_idx.begin(), jet0trk_idx.end(), j);
            if (it1 != jet0trk_idx.end()) continue;
            minijet_p4_1 += tks.p4(j);
            minijet_ntk_1 += 1;
            if (tks.pass_seed(j, bs)) jet1trk_idx.push_back(j);
            sump_1 += tks.p(j);
            sumeta_1 += fabs(tks.eta(j));
            if (fabs(tks.eta(j)) > fabs(maxeta_1)) maxeta_1 = tks.eta(j);
            if (tks.pass_seed(j, bs)) n_movedseedtks++;
          }

        }


        jet_p4_0 = minijet_p4_0;
        jet_p4_1 = minijet_p4_1;
        jet_eta_0 = minijet_p4_0.Eta();
        jet_eta_1 = minijet_p4_1.Eta();
        jet_ntks_0 = minijet_ntk_0;
        jet_ntks_1 = minijet_ntk_1;

        //apply presel cuts
        if (minijet_ntk_0 < 1 || minijet_ntk_1 < 1 || minijet_ntk_0 + minijet_ntk_1 < 5)
          continue;
        //FIXME
        //if (n_movedseedtks < 10)
        //  continue;
        int j = ilsp;   
        int slsp = 2+j*2, swapemm = gen.pt(slsp) < gen.pt(slsp+1); // toward making the jet assoc'd to the higher (lower) pT quark be "jet0" ("jet1")
        int iqlsp0 = slsp + (swapemm ? !0 : 0);
        int iqlsp1 = slsp + (swapemm ? !1 : 1);
        boost0 =  gen.p4(iqlsp0).Beta()*gen.p4(iqlsp0).Gamma(); 
        boost1 = gen.p4(iqlsp1).Beta()*gen.p4(iqlsp1).Gamma(); 
        
        const TLorentzVector jet_tot_p4 = jet_p4_0 + jet_p4_1;

        jet0_lsp_angle = jet_p4_0.Angle(lsp_p4.Vect());	 //smearing angle
        jet1_lsp_angle = jet_p4_1.Angle(lsp_p4.Vect());  //smearing angle

        jet_pt_0  = jet_p4_0.Pt();
        jet_pt_1  = jet_p4_1.Pt();
        jet_dr_minjq0 = jet_p4_0.DeltaR(quark_p4_0);
        jet_dr_minjq1 = jet_p4_1.DeltaR(quark_p4_1);
        jet_dr        = jet_p4_0.DeltaR(jet_p4_1);
        jet_costheta = ((jet_p4_0.X()*jet_p4_1.X()) + (jet_p4_0.Y()*jet_p4_1.Y()) + (jet_p4_0.Z()*jet_p4_1.Z()))/(jet_p4_0.P()*jet_p4_1.P()); 
        jet_dphi = jet_p4_0.DeltaPhi(jet_p4_1);
        jet_aj    = (jet_pt_0 - jet_pt_1) / (jet_pt_0 + jet_pt_1);
        jet_deta = fabs(jet_eta_0 - jet_eta_1);
        jet_dphi_max = jet_p4_0.DeltaPhi(jet_p4_1);
        jet_deta_max = jet_eta_0 - jet_eta_1; // JMTBAD fabs?
        qrk_dphi_max = quark_p4_0.DeltaPhi(quark_p4_1);
        jet_mv_dphi_0  = lsp_p4.DeltaPhi(jet_p4_0);
        jet_mv_dphi_1  = lsp_p4.DeltaPhi(jet_p4_1);
        jet_mv_dphi_sum = lsp_p4.DeltaPhi(jet_p4_0 + jet_p4_1);
        qrk_mv_dphi_0  = lsp_p4.DeltaPhi(quark_p4_0);
        qrk_mv_dphi_1  = lsp_p4.DeltaPhi(quark_p4_1);
        qrk_mv_dphi_sum = lsp_p4.DeltaPhi(quark_p4_0 + quark_p4_1);
        qrkp_0 = quark_p4_0.P();
        qrkp_1 = quark_p4_1.P();
        qrk_costheta = ((quark_p4_0.X()*quark_p4_1.X()) + (quark_p4_0.Y()*quark_p4_1.Y()) + (quark_p4_0.Z()*quark_p4_1.Z()))/(quark_p4_0.P()*quark_p4_1.P()); 
        jet_mv_deta_0  = fabs(jet_eta_0 - lsp_p4.Eta());
        jet_mv_deta_1  = fabs(jet_eta_1 - lsp_p4.Eta());
        jet_mv_deta_sum = fabs((jet_p4_0 + jet_p4_1).Eta() - lsp_p4.Eta());
        if (has_Wboson) wjet_dphi = w_p4.DeltaPhi(jet_p4_0 + jet_p4_1);
        if (has_Zmumuboson) {
          zjet_dphi = zmumu_p4.DeltaPhi(jet_p4_0 + jet_p4_1);
          z_m = zmumu_m;
          z_pT = zmumu_pT;
        }
        else if (has_Zeeboson) {
          zjet_dphi = zee_p4.DeltaPhi(jet_p4_0 + jet_p4_1);
          z_m = zee_m;
          z_pT = zee_pT;
        }
        if (met_p4.Pt() > 25) {
          if (nselmuons > 0) {
            ljet_absdr = abs(muon_p4.DeltaR(jet_p4_0)) < abs(muon_p4.DeltaR(jet_p4_1)) ? abs(muon_p4.DeltaR(jet_p4_0)) : abs(muon_p4.DeltaR(jet_p4_1));
            ljet0_absdr = abs(muon_p4.DeltaR(jet_p4_0));
            ljet1_absdr = abs(muon_p4.DeltaR(jet_p4_1));
          }
          else if (nseleles > 0 && nselmuons == 0) {
            ljet_absdr = abs(ele_p4.DeltaR(jet_p4_0)) < abs(ele_p4.DeltaR(jet_p4_1)) ? abs(ele_p4.DeltaR(jet_p4_0)) : abs(ele_p4.DeltaR(jet_p4_1));		
            ljet0_absdr = abs(ele_p4.DeltaR(jet_p4_0));
            ljet1_absdr = abs(ele_p4.DeltaR(jet_p4_1));
          }
          nujet0_absphi = abs(met_p4.DeltaPhi(jet_p4_0));
          nujet1_absphi = abs(met_p4.DeltaPhi(jet_p4_1));

        }
      }


      int n_pass_nocuts = 0;
      int n_pass_ntracks = 0;
      int n_pass_all = 0;
      double  dist2move = -9.9;
      jmt::MinValue dist2min(100);
      std::vector<int> first_vtx_to_pass(num_numdens, -1);
      double vtx_bs2derr = -9.9, vtx_eta = -9.9, vtx_z = -999.9, vtx_dbv = -999.9, vtx_3dbv = -999.9, vtx_ntk = -9; // JMTBAD ??? these end up with what???
      auto set_it_if_first = [](int& to_set, int to_set_to) { if (to_set == -1) to_set = to_set_to; };
      for (size_t i = 0; i < nvtx; ++i) {
        dist2move = (gen.decay(ilsp, bs) - vs.pos(i)).Mag();
        dist2min(i, dist2move);
        if (dist2move > 0.0200) //FIXME
          continue;
      
        vtx_bs2derr = vs.bs2derr(i); // JMTBAD ???
        vtx_eta     = vs.eta(i);
        vtx_z       = vs.z(i);
        vtx_dbv     = vs.pos(i).Perp();
        vtx_3dbv    = vs.pos(i).Mag();
        vtx_ntk     = vs.ntracks(i);

        const bool pass_ntracks = vs.ntracks(i) >= 5;
        const bool pass_bs2derr = vs.bs2derr(i) < 0.0050; // JMTBAD rescale_bs2derr // FIXME

        if (1) { set_it_if_first(first_vtx_to_pass[0], i); ++n_pass_nocuts; }
        if (pass_ntracks) { set_it_if_first(first_vtx_to_pass[1], i); ++n_pass_ntracks; }
        if (pass_ntracks && pass_bs2derr) { set_it_if_first(first_vtx_to_pass[2], i); ++n_pass_all; }
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
      
      den += w;

      for (numdens& nd : nds) {
        nd.den(k_decay_x, lspdecay.x());
        nd.den(k_decay_y, lspdecay.y());
        nd.den(k_decay_z, lspdecay.z());
        nd.den(k_decay_xy, lspdecay.x(), lspdecay.y());
        nd.den(k_lspdist2, lspdist2);
        nd.den(k_lspdist3, lspdist3);
        nd.den(k_lspdistz, lspdistz);
        nd.den(k_movedist2, movedist2);
        nd.den(k_movedist3, movedist3);
        nd.den(k_lspeta, lsp_p4.Eta());
        nd.den(k_lsppt, lsp_p4.Pt());
        nd.den(k_lspgammabeta, lsp_p4.Beta()*lsp_p4.Gamma());
        nd.den(k_lspctau, movedist3/(lsp_p4.Beta()*lsp_p4.Gamma()));
        nd.den(k_npv, pvs.n());
        nd.den(k_pvz, pvs.z(0));
        nd.den(k_dist2dpvbs, sqrt((pvs.x(0)-bs.x(pvs.z(0)))*(pvs.x(0)-bs.x(pvs.z(0))) + (pvs.y(0)-bs.y(pvs.z(0)))*(pvs.y(0)-bs.y(pvs.z(0)))));
        nd.den(k_pvrho, pvs.rho(0));
        nd.den(k_pvntracks, pvs.ntracks(0));
        nd.den(k_pvscore, pvs.score(0));
        nd.den(k_ht, jets.ht());
        nd.den(k_njets, jets.n());
        nd.den(k_nmuons, nselmuons);
        nd.den(k_muon_pT, muon_pT);
        nd.den(k_muon_abseta, muon_abseta);
        nd.den(k_muon_iso, muon_iso);
        nd.den(k_muon_absdxybs, muon_absdxybs);
        nd.den(k_muon_absdz, muon_absdz);
        nd.den(k_muon_nsigmadxybs, muon_nsigmadxybs);
        nd.den(k_neles, nseleles);
        nd.den(k_ele_pT, ele_pT);
        nd.den(k_ele_abseta, ele_abseta);
        nd.den(k_ele_iso, ele_iso);
        nd.den(k_ele_absdxybs, ele_absdxybs);
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
        nd.den(k_jet_asymm, jet_aj);
        nd.den(k_jet0_eta, jet_eta_0);
        nd.den(k_jet1_eta, jet_eta_1);
        nd.den(k_llp_category, llp_category);
        nd.den(k_jet_dr, jet_dr);
        nd.den(k_jet_costheta, jet_costheta);
        nd.den(k_jet_deta, jet_deta);
        nd.den(k_jet_dphi, jet_dphi);
        nd.den(k_jet_dind, jet_dind);
        nd.den(k_pt0, jet_pt_0);
        nd.den(k_pt1, jet_pt_1);
        nd.den(k_ntks_j0, jet_ntks_0);
        nd.den(k_ntks_j1, jet_ntks_1);
        nd.den(k_jet_dr_minj0_q0, jet_dr_minjq0);
        nd.den(k_jet_dr_minj1_q1, jet_dr_minjq1);
        nd.den(k_ntk0_ntk1, jet_ntks_0, jet_ntks_1);
        nd.den(k_boost0_boost1, boost0, boost1);
        for (size_t j = 0; j < closeseedtrk_idx.size(); ++j){
          nd.den(k_closeseed_trk_genmissdist, tks.dxy(closeseedtrk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp)));
          nd.den(k_closeseed_trk_gendz, tks.dz(closeseedtrk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp)));
          nd.den(k_closeseed_trk_gennsigmadz, tks.dz(closeseedtrk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp))/tks.err_dz(closeseedtrk_idx[j]));
        }
        for (size_t j = 0; j < jet0trk_idx.size(); ++j){
          const TLorentzVector jp4 = tks.p4(jet0trk_idx[j]);
          nd.den(k_jet0_trk_dr, jp4.DeltaR(minijet_p4_0));
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
          const double jet0_gennsigmadz = tks.dz(jet0trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp))/tks.err_dz(jet0trk_idx[j]);
          const double jet0_gennsigmamissdist = tks.dxy(jet0trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp))/tks.err_dxy(jet0trk_idx[j]);  
          nd.den(k_jet0_trk_gennsigma, sqrt((jet0_gennsigmamissdist*jet0_gennsigmamissdist) + (jet0_gennsigmadz*jet0_gennsigmadz)));
          nd.den(k_jet0_trk_gennsigmamissdist, jet0_gennsigmamissdist);
          nd.den(k_jet0_trk_genmissdist, tks.dxy(jet0trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp)));
          nd.den(k_jet0_trk_gennsigmadz, jet0_gennsigmadz);
          nd.den(k_jet0_trk_gendz, tks.dz(jet0trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp)));
          nd.den(k_jet0_trk_whichpv, tks.which_pv(jet0trk_idx[j]));
          nd.den(k_jet0_trk_dsz, tks.dsz(jet0trk_idx[j], pvs.x(0) + bs.x(pvs.z(0)), pvs.y(0) + bs.y(pvs.z(0)), pvs.z(0)));
          nd.den(k_jet0_trk_dxy, tks.dxybs(jet0trk_idx[j], bs));
          nd.den(k_jet0_trk_nsigmadxy, tks.dxybs(jet0trk_idx[j], bs)/tks.err_dxy(jet0trk_idx[j]));
          nd.den(k_jet0_trk_dxyerr, tks.err_dxy(jet0trk_idx[j]));
        }
        nd.den(k_jet0_sump, sump_0);
        nd.den(k_jet0_sump_jetdr, sump_0, jet_dr);
        nd.den(k_movedist3_jetdr, movedist3, jet_dr);
        nd.den(k_movedist3_tightcloseseedtks, movedist3, n_tightcloseseedtks);
        nd.den(k_jet_costheta_tightcloseseedtks, jet_costheta, n_tightcloseseedtks);
        nd.den(k_jet_dr_tightcloseseedtks, jet_dr, n_tightcloseseedtks);
        nd.den(k_movedist3_closeseedtks, movedist3, n_closeseedtks);
        nd.den(k_jet_costheta_closeseedtks, jet_costheta, n_closeseedtks);
        nd.den(k_jet_dr_closeseedtks, jet_dr, n_closeseedtks);
        for (size_t j = 0; j < jet1trk_idx.size(); ++j){
          const TLorentzVector jp4 = tks.p4(jet1trk_idx[j]);
          nd.den(k_jet1_trk_dr, jp4.DeltaR(minijet_p4_1));
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
          const double jet1_gennsigmadz = tks.dz(jet1trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp))/tks.err_dz(jet1trk_idx[j]);
          const double jet1_gennsigmamissdist = tks.dxy(jet1trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp))/tks.err_dxy(jet1trk_idx[j]);  
          nd.den(k_jet1_trk_gennsigma, sqrt((jet1_gennsigmamissdist*jet1_gennsigmamissdist) + (jet1_gennsigmadz*jet1_gennsigmadz)));
          nd.den(k_jet1_trk_gennsigmamissdist, jet1_gennsigmamissdist);
          nd.den(k_jet1_trk_genmissdist, tks.dxy(jet1trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp)));
          nd.den(k_jet1_trk_gennsigmadz, jet1_gennsigmadz);
          nd.den(k_jet1_trk_gendz, tks.dz(jet1trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp)));
          nd.den(k_jet1_trk_whichpv, tks.which_pv(jet1trk_idx[j]));
          nd.den(k_jet1_trk_dsz, tks.dsz(jet1trk_idx[j], pvs.x(0) + bs.x(pvs.z(0)), pvs.y(0) + bs.y(pvs.z(0)), pvs.z(0)));
          nd.den(k_jet1_trk_dxy, tks.dxybs(jet1trk_idx[j], bs));
          nd.den(k_jet1_trk_nsigmadxy, tks.dxybs(jet1trk_idx[j], bs)/tks.err_dxy(jet1trk_idx[j]));
          nd.den(k_jet1_trk_dxyerr, tks.err_dxy(jet1trk_idx[j]));
        }
        
        nd.den(k_jet1_sump, sump_1);
        nd.den(k_jet1_sump_jetdr, sump_1, jet_dr);
        nd.den(k_jet1_sump_jetdphi, sump_1, jet_dphi);
        nd.den(k_jet1_ntks_jetdphi, jet_ntks_1, jet_dphi);
        nd.den(k_asymjet_jetdr, (sump_0 - sump_1)/(sump_0 + sump_1), jet_dr);
        nd.den(k_jet_asymsump, (sump_0 - sump_1)/(sump_0 + sump_1));
        nd.den(k_jet0_maxeta_jet1_maxeta, maxeta_0, maxeta_1);
        nd.den(k_jet0_sumeta_jet1_sumeta, sumeta_0, sumeta_1);
        nd.den(k_jet0_sump_jet1_sump, sump_0, sump_1);
        nd.den(k_qrktosump_j0, sump_0/qrkp_0);
        nd.den(k_qrktosump_j1, sump_1/qrkp_1);
        nd.den(k_qrktosump_sumpj0, sump_0, sump_0/qrkp_0);
        nd.den(k_qrktosump_sumpj1, sump_1, sump_1/qrkp_1);
        nd.den(k_2p0p1_1mgencos, log10(2*qrkp_0*qrkp_1), log10(1-qrk_costheta));
        nd.den(k_2sump0sump1_1mcos, log10(2*sump_0*sump_1), log10(1-jet_costheta));
        nd.den(k_1mcosto1mgencos, (1-jet_costheta)/(1-qrk_costheta));
        nd.den(k_2logm, log10(2*sump_0*sump_1) + log10(1-jet_costheta));
        nd.den(k_2genlogm, log10(2*qrkp_0*qrkp_1) + log10(1-qrk_costheta));
        nd.den(k_nmovedtracks, jet_ntks_0 + jet_ntks_1);
        nd.den(k_dphi_sum_j_mv, jet_mv_dphi_sum);
        nd.den(k_deta_sum_j_mv, jet_mv_deta_sum);
        nd.den(k_dphi_sum_q_mv, fabs(qrk_mv_dphi_sum));
        nd.den(k_jetpt0_asymm, jet_pt_0, jet_aj);
        nd.den(k_jetpt1_asymm, jet_pt_1, jet_aj);
        nd.den(k_jeteta0_asymm, jet_eta_0, jet_aj);
        nd.den(k_jeteta1_asymm, jet_eta_1, jet_aj);
        nd.den(k_jetdr_asymm, jet_dr, jet_aj);
        nd.den(k_angle0, jet0_lsp_angle);
        nd.den(k_angle1, jet1_lsp_angle);
        nd.den(k_jetdravg, jet_dr);
        nd.den(k_dphi_j0_mv, fabs(jet_mv_dphi_0));
        nd.den(k_dphi_j1_mv, fabs(jet_mv_dphi_1));
        nd.den(k_deta_j0_mv, jet_mv_deta_0);
        nd.den(k_deta_j1_mv, jet_mv_deta_1);
        nd.den(k_dphi_q0_mv, fabs(qrk_mv_dphi_0));
        nd.den(k_dphi_q1_mv, fabs(qrk_mv_dphi_1));
        nd.den(k_nseedtracks, nseedtracks);
        nd.den(k_miscseedtracks, n_miscseedtracks); 
        nd.den(k_closeseedtks, n_closeseedtks);
        nd.den(k_tightcloseseedtks, n_tightcloseseedtks);
        nd.den(k_movedseedtks, n_movedseedtks);
        nd.den(k_movedvtxseedtks, n_movedvtxseedtks);
        nd.den(k_movedcloseseedtks, n_movedcloseseedtks);
        nd.den(k_rat_moved_to_closetks, n_movedcloseseedtks/n_closeseedtks); 
        nd.den(k_rat_moved_to_vtxtks, n_movedvtxseedtks/vtx_ntk); 
        nd.den(k_jetdphimax, jet_dphi_max);
        nd.den(k_jetdetamax, jet_deta_max);
        nd.den(k_qrkdphimax, qrk_dphi_max);
        nd.den(k_jetdphi_mveta, fabs(jet_dphi_max), fabs(lsp_p4.Eta()));
        nd.den(k_jetmovea3d01, jet0_lsp_angle, jet1_lsp_angle);
        nd.den(k_jeteta01,  jet_eta_0, jet_eta_1);
        nd.den(k_jetpt01, jet_pt_0, jet_pt_1);
        nd.den(k_pt_angle0, jet_pt_0, jet0_lsp_angle);
        nd.den(k_pt_angle1, jet_pt_1, jet1_lsp_angle);
        nd.den(k_eta_angle0, lsp_p4.Eta(), jet0_lsp_angle);
        nd.den(k_eta_angle1, lsp_p4.Eta(), jet1_lsp_angle);
        nd.den(k_nvtx, nvtx);
        nd.den(k_vtxunc, dist2move);
        nd.den(k_vtxbs2derr, vtx_bs2derr);
        nd.den(k_vtxeta, vtx_eta);
        nd.den(k_vtxz, vtx_z);
        nd.den(k_vtxdbv, vtx_dbv);
        nd.den(k_vtx3dbv, vtx_3dbv);
        nd.den(k_vtxntk, vtx_ntk);
      }

      for (int in = 0; in < num_numdens; ++in) {
        int iv = first_vtx_to_pass[in];
        if (iv != -1) {
          h_vtxntracks   [in]->Fill(vs.ntracks(iv));
          h_vtxbs2derr   [in]->Fill(vs.bs2derr(iv));
          //h_vtxtkonlymass[in]->Fill(vs.tkonlymass(iv));
          h_vtxs_mass    [in]->Fill(vs.mass(iv));
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

      for (int in = 0; in < num_numdens; ++in) {
        if (!npasses[in])
          continue;
        numdens& nd = nds[in];
        nd.num(k_decay_x, lspdecay.x());
        nd.num(k_decay_y, lspdecay.y());
        nd.num(k_decay_z, lspdecay.z());
        nd.num(k_decay_xy, lspdecay.x(), lspdecay.y());
        nd.num(k_lspdist2, lspdist2);
        nd.num(k_lspdist3, lspdist3);
        nd.num(k_lspdistz, lspdistz);
        nd.num(k_movedist2, movedist2);
        nd.num(k_movedist3, movedist3);
        nd.num(k_lspeta, lsp_p4.Eta());
        nd.num(k_lsppt, lsp_p4.Pt());
        nd.num(k_lspgammabeta, lsp_p4.Beta()*lsp_p4.Gamma());
        nd.num(k_lspctau, movedist3/(lsp_p4.Beta()*lsp_p4.Gamma()));
        nd.num(k_npv, pvs.n());
        nd.num(k_pvz, pvs.z(0) + bs.z());
        nd.num(k_dist2dpvbs, sqrt((pvs.x(0)-bs.x(pvs.z(0)))*(pvs.x(0)-bs.x(pvs.z(0))) + (pvs.y(0)-bs.y(pvs.z(0)))*(pvs.y(0)-bs.y(pvs.z(0)))));
        nd.num(k_pvrho, pvs.rho(0));
        nd.num(k_pvntracks, pvs.ntracks(0));
        nd.num(k_pvscore, pvs.score(0));
        nd.num(k_ht, jets.ht());
        nd.num(k_njets, jets.n());
        nd.num(k_nmuons, nselmuons);
        nd.num(k_muon_pT, muon_pT);
        nd.num(k_muon_abseta, muon_abseta);
        nd.num(k_muon_iso, muon_iso);
        nd.num(k_muon_absdxybs, muon_absdxybs);
        nd.num(k_muon_absdz, muon_absdz);
        nd.num(k_muon_nsigmadxybs, muon_nsigmadxybs);
        nd.num(k_neles, nseleles);
        nd.num(k_ele_pT, ele_pT);
        nd.num(k_ele_abseta, ele_abseta);
        nd.num(k_ele_iso, ele_iso);
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
        nd.num(k_jet_asymm, jet_aj);
        nd.num(k_jet0_eta, jet_eta_0);
        nd.num(k_jet1_eta, jet_eta_1);
        nd.num(k_llp_category, llp_category);
        nd.num(k_jet_dr, jet_dr);
        nd.num(k_jet_costheta, jet_costheta);
        nd.num(k_jet_deta, jet_deta);
        nd.num(k_jet_dphi, jet_dphi);
        nd.num(k_jet_dind, jet_dind);
        nd.num(k_pt0, jet_pt_0);
        nd.num(k_pt1, jet_pt_1);
        nd.num(k_ntks_j0, jet_ntks_0);
        nd.num(k_ntks_j1, jet_ntks_1);
        nd.num(k_jet_dr_minj0_q0, jet_dr_minjq0);
        nd.num(k_jet_dr_minj1_q1, jet_dr_minjq1);
        nd.num(k_ntk0_ntk1, jet_ntks_0, jet_ntks_1);
        nd.num(k_boost0_boost1, boost0, boost1);
        for (size_t j = 0; j < closeseedtrk_idx.size(); ++j){
          nd.num(k_closeseed_trk_genmissdist, tks.dxy(closeseedtrk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp)));
          nd.num(k_closeseed_trk_gendz, tks.dz(closeseedtrk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp)));
          nd.num(k_closeseed_trk_gennsigmadz, tks.dz(closeseedtrk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp))/tks.err_dz(closeseedtrk_idx[j]));
        }
        for (size_t j = 0; j < jet0trk_idx.size(); ++j){
          const TLorentzVector jp4 = tks.p4(jet0trk_idx[j]);
          nd.num(k_jet0_trk_dr, jp4.DeltaR(minijet_p4_0));
          nd.num(k_jet0_trk_pt, tks.pt(jet0trk_idx[j]));
          nd.num(k_jet0_trk_eta, tks.eta(jet0trk_idx[j]));
          nd.num(k_jet0_trk_p, tks.p(jet0trk_idx[j]));
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
          const double jet0_gennsigmadz = tks.dz(jet0trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp))/tks.err_dz(jet0trk_idx[j]);
          const double jet0_gennsigmamissdist = tks.dxy(jet0trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp))/tks.err_dxy(jet0trk_idx[j]);  
          nd.num(k_jet0_trk_gennsigma, sqrt((jet0_gennsigmamissdist*jet0_gennsigmamissdist) + (jet0_gennsigmadz*jet0_gennsigmadz)));
          nd.num(k_jet0_trk_gennsigmamissdist, jet0_gennsigmamissdist);
          nd.num(k_jet0_trk_genmissdist, tks.dxy(jet0trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp)));
          nd.num(k_jet0_trk_gennsigmadz, jet0_gennsigmadz);
          nd.num(k_jet0_trk_gendz, tks.dz(jet0trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp)));
          nd.num(k_jet0_trk_whichpv, tks.which_pv(jet0trk_idx[j]));
          nd.num(k_jet0_trk_dsz, tks.dsz(jet0trk_idx[j], pvs.x(0) + bs.x(pvs.z(0)), pvs.y(0) + bs.y(pvs.z(0)), pvs.z(0)));
          nd.num(k_jet0_trk_dxy, tks.dxybs(jet0trk_idx[j], bs));
          nd.num(k_jet0_trk_nsigmadxy, tks.dxybs(jet0trk_idx[j], bs)/tks.err_dxy(jet0trk_idx[j]));
          nd.num(k_jet0_trk_dxyerr, tks.err_dxy(jet0trk_idx[j]));
        }
        nd.num(k_jet0_sump, sump_0);
        nd.num(k_jet0_sump_jetdr, sump_0, jet_dr);
        nd.num(k_movedist3_jetdr, movedist3, jet_dr);
        nd.num(k_movedist3_tightcloseseedtks, movedist3, n_tightcloseseedtks);
        nd.num(k_jet_costheta_tightcloseseedtks, jet_costheta, n_tightcloseseedtks);
        nd.num(k_jet_dr_tightcloseseedtks, jet_dr, n_tightcloseseedtks);
        nd.num(k_movedist3_closeseedtks, movedist3, n_closeseedtks);
        nd.num(k_jet_costheta_closeseedtks, jet_costheta, n_closeseedtks);
        nd.num(k_jet_dr_closeseedtks, jet_dr, n_closeseedtks);
        for (size_t j = 0; j < jet1trk_idx.size(); ++j){
          const TLorentzVector jp4 = tks.p4(jet1trk_idx[j]);
          nd.num(k_jet1_trk_dr, jp4.DeltaR(minijet_p4_1));
          nd.num(k_jet1_trk_pt, tks.pt(jet1trk_idx[j]));
          nd.num(k_jet1_trk_eta, tks.eta(jet1trk_idx[j]));
          nd.num(k_jet1_trk_p, tks.p(jet1trk_idx[j]));
          nd.num(k_jet1_trk_dz, tks.dzpv(jet1trk_idx[j], pvs));
          if (mindist2move_iv != -1) {
            const double jet1_vtxdz = tks.dz(jet1trk_idx[j], vs.x(mindist2move_iv) + bs.x(vs.z(mindist2move_iv)),vs.y(mindist2move_iv) + bs.y(vs.z(mindist2move_iv)),vs.z(mindist2move_iv)); 
            const double jet1_vtxdxy = tks.dxy(jet1trk_idx[j], vs.x(mindist2move_iv) + bs.x(vs.z(mindist2move_iv)), vs.y(mindist2move_iv) + bs.y(vs.z(mindist2move_iv)));
            nd.num(k_jet1_trk_vtxdxy, jet1_vtxdxy);
            nd.num(k_jet1_trk_vtxdz, jet1_vtxdz);
            nd.num(k_jet1_trk_nsigmavtxdz, jet1_vtxdz/tks.err_dz(jet1trk_idx[j]));
            nd.num(k_jet1_trk_nsigmavtxdxy, jet1_vtxdxy/tks.err_dxy(jet1trk_idx[j]));
            nd.num(k_jet1_trk_nsigmavtx, sqrt((jet1_vtxdxy/tks.err_dxy(jet1trk_idx[j]))*(jet1_vtxdxy/tks.err_dxy(jet1trk_idx[j])) + (jet1_vtxdz/tks.err_dz(jet1trk_idx[j]))*(jet1_vtxdz/tks.err_dz(jet1trk_idx[j]))));
          }
          nd.num(k_jet1_trk_dzerr, tks.err_dz(jet1trk_idx[j]));
          const double jet1_gennsigmadz = tks.dz(jet1trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp))/tks.err_dz(jet1trk_idx[j]);
          const double jet1_gennsigmamissdist = tks.dxy(jet1trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp))/tks.err_dxy(jet1trk_idx[j]);  
          nd.num(k_jet1_trk_gennsigma, sqrt((jet1_gennsigmamissdist*jet1_gennsigmamissdist) + (jet1_gennsigmadz*jet1_gennsigmadz)));
          nd.num(k_jet1_trk_gennsigmamissdist, jet1_gennsigmamissdist);
          nd.num(k_jet1_trk_genmissdist, tks.dxy(jet1trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp)));
          nd.num(k_jet1_trk_gennsigmadz, jet1_gennsigmadz);
          nd.num(k_jet1_trk_gendz, tks.dz(jet1trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp)));
          nd.num(k_jet1_trk_whichpv, tks.which_pv(jet1trk_idx[j]));
          nd.num(k_jet1_trk_dsz, tks.dsz(jet1trk_idx[j], pvs.x(0) + bs.x(pvs.z(0)), pvs.y(0) + bs.y(pvs.z(0)), pvs.z(0)));
          nd.num(k_jet1_trk_dxy, tks.dxybs(jet1trk_idx[j], bs));
          nd.num(k_jet1_trk_nsigmadxy, tks.dxybs(jet1trk_idx[j], bs)/tks.err_dxy(jet1trk_idx[j]));
          nd.num(k_jet1_trk_dxyerr, tks.err_dxy(jet1trk_idx[j]));
        }
        nd.num(k_jet1_sump, sump_1);
        nd.num(k_jet1_sump_jetdr, sump_1, jet_dr);
        nd.num(k_jet1_sump_jetdphi, sump_1, jet_dphi);
        nd.num(k_jet1_ntks_jetdphi, jet_ntks_1, jet_dphi);
        nd.num(k_asymjet_jetdr, (sump_0 - sump_1)/(sump_0 + sump_1), jet_dr);
        nd.num(k_jet_asymsump, (sump_0 - sump_1)/(sump_0 + sump_1));
        nd.num(k_jet0_maxeta_jet1_maxeta, maxeta_0, maxeta_1);
        nd.num(k_jet0_sumeta_jet1_sumeta, sumeta_0, sumeta_1);
        nd.num(k_jet0_sump_jet1_sump, sump_0, sump_1);
        nd.num(k_qrktosump_j0, sump_0/qrkp_0);
        nd.num(k_qrktosump_j1, sump_1/qrkp_1);
        nd.num(k_qrktosump_sumpj0, sump_0, sump_0/qrkp_0);
        nd.num(k_qrktosump_sumpj1, sump_1, sump_1/qrkp_1);
        nd.num(k_2p0p1_1mgencos, log10(2*qrkp_0*qrkp_1), log10(1-qrk_costheta));
        nd.num(k_2sump0sump1_1mcos, log10(2*sump_0*sump_1), log10(1-jet_costheta));
        nd.num(k_1mcosto1mgencos, (1-jet_costheta)/(1-qrk_costheta));
        nd.num(k_2logm, log10(2*sump_0*sump_1) + log10(1-jet_costheta));
        nd.num(k_2genlogm, log10(2*qrkp_0*qrkp_1) + log10(1-qrk_costheta));
        nd.num(k_nmovedtracks, jet_ntks_0 + jet_ntks_1);
        nd.num(k_dphi_sum_j_mv, fabs(jet_mv_dphi_sum));
        nd.num(k_deta_sum_j_mv, jet_mv_deta_sum);
        nd.num(k_dphi_sum_q_mv, fabs(qrk_mv_dphi_sum));
        nd.num(k_jetpt0_asymm, jet_pt_0, jet_aj);
        nd.num(k_jetpt1_asymm, jet_pt_1, jet_aj);
        nd.num(k_jeteta0_asymm, jet_eta_0, jet_aj);
        nd.num(k_jeteta1_asymm, jet_eta_1, jet_aj);
        nd.num(k_jetdr_asymm, jet_dr, jet_aj);
        nd.num(k_jetdravg, jet_dr);
        nd.num(k_angle0, jet0_lsp_angle);
        nd.num(k_angle1, jet1_lsp_angle);
        nd.num(k_dphi_j0_mv, fabs(jet_mv_dphi_0));
        nd.num(k_dphi_j1_mv, fabs(jet_mv_dphi_1));
        nd.num(k_deta_j0_mv, jet_mv_deta_0);
        nd.num(k_deta_j1_mv, jet_mv_deta_1);
        nd.num(k_dphi_q0_mv, fabs(qrk_mv_dphi_0));
        nd.num(k_dphi_q1_mv, fabs(qrk_mv_dphi_1));
        nd.num(k_nseedtracks, nseedtracks);
        nd.num(k_miscseedtracks, n_miscseedtracks); 
        nd.num(k_closeseedtks, n_closeseedtks);
        nd.num(k_tightcloseseedtks, n_tightcloseseedtks);
        nd.num(k_movedseedtks, n_movedseedtks);
        nd.num(k_movedvtxseedtks, n_movedvtxseedtks);
        nd.num(k_movedcloseseedtks, n_movedcloseseedtks);
        nd.num(k_rat_moved_to_closetks, n_movedcloseseedtks/n_closeseedtks); 
        nd.num(k_rat_moved_to_vtxtks, n_movedvtxseedtks/vtx_ntk); 
        nd.num(k_jetdphimax, jet_dphi_max);
        nd.num(k_jetdetamax, jet_deta_max);
        nd.num(k_qrkdphimax, qrk_dphi_max);
        nd.num(k_jetdphi_mveta, fabs(jet_dphi_max), fabs(lsp_p4.Eta()));
        nd.num(k_jetmovea3d01, jet0_lsp_angle, jet1_lsp_angle);
        nd.num(k_jeteta01,  jet_eta_0, jet_eta_1);
        nd.num(k_jetpt01, jet_pt_0, jet_pt_1);
        nd.num(k_pt_angle0, jet_pt_0, jet0_lsp_angle);
        nd.num(k_pt_angle1, jet_pt_1, jet1_lsp_angle);
        nd.num(k_eta_angle0, lsp_p4.Eta(), jet0_lsp_angle);
        nd.num(k_eta_angle1, lsp_p4.Eta(), jet1_lsp_angle);
        nd.num(k_nvtx, npasses[in]);
        nd.num(k_vtxunc, dist2move);
        nd.num(k_vtxbs2derr, vtx_bs2derr);
        nd.num(k_vtxeta, vtx_eta);
        nd.num(k_vtxz, vtx_z);
        nd.num(k_vtxdbv, vtx_dbv);
        nd.num(k_vtx3dbv, vtx_3dbv);
        nd.num(k_vtxntk, vtx_ntk);
      }
    }

    NR_loop_cont(w);
  };

  nr.loop(fcn);

  printf("%12.1f", den);
  for (const std::string& c : {"nocuts", "ntracks", "all"}) {
    const jmt::interval i = jmt::clopper_pearson_binom(nums[c], den);
    printf("    %6.4f +- %6.4f", i.value, i.error());
  }
  printf("\n");
}
