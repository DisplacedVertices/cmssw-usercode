#include "TH2F.h"
#include "TRandom3.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/ExtValue.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralino/interface/EventTools.h"
#include "DataFormats/Math/interface/PtEtaPhiMass.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "TLorentzVector.h"
#include "DataFormats/Math/interface/Point3D.h"

class MFVEventHistos : public edm::EDAnalyzer {
 public:
  explicit MFVEventHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);
  
 private:
  const edm::EDGetTokenT<MFVEvent> mevent_token;
  const edm::EDGetTokenT<double> weight_token;
  const edm::EDGetTokenT<MFVVertexAuxCollection> vertex_token;
  const int max_ntrackplots;
  const bool do_scatterplots;

  TH1F* h_w;
  TH1F* h_nsv;

  TH2F* h_gen_decay;
  TH1F* h_gen_flavor_code;

  TH1F* h_nbquarks;
  TH1F* h_bquark_pt;
  TH1F* h_bquark_eta;
  TH1F* h_bquark_phi;
  TH1F* h_bquark_energy;
  TH1F* h_bquark_pairdphi;
  TH1F* h_bquark_pairdeta;

  //FIXME: ghost-track vertex study
  TH1F* h_n_gen_bvtx;
  TH1F* h_gvtx_nsv;
  TH1F* h_gvtx_sv_ntrack;
  TH1F* h_gvtx_njet;
  TH1F* h_gvtx_sanity_njet;
  TH1F* h_gvtx_nbjet;
  TH1F* h_gvtx_nloosebsvjet;
  TH1F* h_gvtx_nloosebsvplusbtaggedjet;
  TH1F* h_gvtx_njet_bboost_wcut;
  TH1F* h_gvtx_bquark_pT;
  TH1F* h_gvtx_bhad_bquark_dR;
  TH2F* h_2D_gvtx_bhad_bquark_dR_and_b_quark_pT;
  // cut w/ b-quark pT > 25 GeV imposed 
  TH1F* h_gvtx_bhad_bquark_dR_wcut;
  TH1F* h_gvtx_bhad_nonbhad_dR_wcut;
  TH2F* h_2D_gvtx_bhad_bquark_dR_and_b_quark_pT_wcut;
  TH2F* h_2D_gvtx_bhad_nonbhad_dR_and_pT_wcut;
  TH2F* h_2D_gvtx_bhad_nonbhad_dR_and_b_quark_pT_wcut;
  TH1F* h_gvtx_bhad_pT_wcut;
  TH1F* h_gvtx_bquark_pT_wcut;
  TH1F* h_gvtx_bquark_jet_dR_wcut;
  TH1F* h_gvtx_tail_dR_jet_eta_bquark_wcut;
  TH1F* h_gvtx_peak_dR_jet_eta_bquark_wcut;
  TH1F* h_gvtx_tail_dR_jet_pT_bquark_wcut;
  TH1F* h_gvtx_peak_dR_jet_pT_bquark_wcut;
  TH1F* h_gvtx_peak_dR_jet_pT_bjet_wcut;
  TH2F* h_2D_gvtx_bquark_closest_jet_dR_ndau_wcut;
  TH1F* h_gvtx_bquark_closest_dau_to_closest_jet_dR_wcut;
  TH1F* h_gvtx_bquark_closest_jet_dR_wcut;
  TH1F* h_gvtx_bquark_closest_jet_pT_wcut;
  TH1F* h_gvtx_bquark_closest_jet_E_ratio_wcut;
  TH1F* h_gvtx_bhad_closest_jet_dR_wcut;
  TH1F* h_gvtx_bhad_closest_jet_pT_wcut;
  TH1F* h_gvtx_bquark_closest_jet_res_pT_wcut;
  TH1F* h_gvtx_all_ntrack_from_jets_wcut;
  TH1F* h_gvtx_jet_seed_ntrack_per_bjet_wcut;
  TH1F* h_gvtx_jet_seed_ntrack_per_non_bjet_wcut;
  TH1F* h_gvtx_jet_seed_ntrack_per_tight_btag_wcut;
  TH1F* h_gvtx_jet_seed_ntrack_per_non_tight_btag_wcut;
  TH1F* h_gvtx_jet_seed_ntrack_per_medium_btag_wcut;
  TH1F* h_gvtx_jet_seed_ntrack_per_non_medium_btag_wcut;
  TH1F* h_gvtx_jet_seed_ntrack_per_loose_btag_wcut;
  TH1F* h_gvtx_jet_seed_ntrack_per_non_loose_btag_wcut;
  TH1F* h_gvtx_jet_seed_ntrack_per_loose_bsv_jet_wcut;
  TH1F* h_gvtx_jet_seed_ntrack_per_non_loose_bsv_jet_wcut;
  TH1F* h_gvtx_jet_seed_ntrack_per_loose_bsv_plus_btagged_jet_wcut;
  TH1F* h_gvtx_jet_seed_ntrack_per_non_loose_bsv_plus_btagged_jet_wcut;
  TH1F* h_gvtx_jet_seed_track_pT_from_jets_wcut;
  TH1F* h_gvtx_jet_seed_track_sigmadxybs_from_jets_wcut;
  TH1F* h_gvtx_jet_seed_track_npxlayers_from_jets_wcut;
  TH1F* h_gvtx_jet_seed_track_nstlayers_from_jets_wcut;
  TH1F* h_gvtx_jet_seed_track_rmin_from_jets_wcut;
  TH1F* h_gvtx_seed_track_pT_from_jets_wcut;
  TH1F* h_gvtx_seed_track_sigmadxybs_from_jets_wcut;
  TH1F* h_gvtx_seed_track_npxlayers_from_jets_wcut;
  TH1F* h_gvtx_seed_track_nstlayers_from_jets_wcut;
  TH1F* h_gvtx_seed_track_rmin_from_jets_wcut;
  TH1F* h_gvtx_sum_pT_all_tracks_from_jets_wcut;

  TH1F* h_gvtx_shared_bjet_or_not_wcut;
  
  //sv investigation 
  TH1F* h_gvtx_sv_trkonly_mom_jet_mom_dR_wcut;
  TH1F* h_gvtx_sv_jetbytrk_mom_jet_mom_dR_wcut;
  
  TH1F* h_gvtx_sv_trkplusjetbytrk_mom_jet_mom_dR_wcut;
  TH1F* h_gvtx_sv_displ_vec_jet_mom_dR_wcut;

  TH1F* h_gvtx_sv_trkonly_mom_bquark_mom_dR_wcut;
  TH1F* h_gvtx_sv_jetbytrk_mom_bquark_mom_dR_wcut;
  TH1F* h_gvtx_sv_trkplusjetbytrk_mom_bquark_mom_dR_wcut;
  TH1F* h_gvtx_sv_displ_vec_bquark_mom_dR_wcut;

  TH1F* h_gvtx_sv_bquark_closest_dist3d_wcut;

  //how to match SVs to a b-decay ? 
  TH1F* h_gvtx_nbsv_by_nsv_wcut;
  TH1F* h_gvtx_match_pT_wcut;
  TH1F* h_gvtx_match_pT_etacut_wcut;
  TH1F* h_gvtx_match_pT_phicut_wcut;
  TH1F* h_gvtx_match_eta_wcut;
  TH1F* h_gvtx_match_eta_pTcut_wcut;
  TH1F* h_gvtx_match_eta_phicut_wcut;
  TH1F* h_gvtx_match_phi_wcut;
  TH1F* h_gvtx_match_phi_etacut_wcut;
  TH1F* h_gvtx_match_phi_pTcut_wcut;
  TH2F* h_2D_gvtx_numerator_nbsv_bjets_wcut;
  TH2F* h_2D_gvtx_numerator_tight_trkmatch_nbsv_bjets_wcut;
  TH2F* h_2D_gvtx_denominator_nbsv_bjets_wcut;
  TH1F* h_gvtx_bsv_dBV_wcut;
  TH1F* h_gvtx_numerator_nbsv_wcut;
  TH1F* h_gvtx_numerator_tight_trkmatch_nbsv_wcut;
  TH1F* h_gvtx_tight_trkmatch_nbsv_per_bjet_wcut;
  TH1F* h_gvtx_tight_trkmatch_nbsv_per_non_bjet_wcut;
  TH1F* h_gvtx_tight_trkmatch_nbsv_per_tight_btag_jet_wcut;
  TH1F* h_gvtx_tight_trkmatch_nbsv_per_non_tight_btag_jet_wcut;
  TH1F* h_gvtx_tight_trkmatch_nbsv_per_medium_btag_jet_wcut;
  TH1F* h_gvtx_tight_trkmatch_nbsv_per_non_medium_btag_jet_wcut;
  TH1F* h_gvtx_tight_trkmatch_nbsv_per_loose_btag_jet_wcut;
  TH1F* h_gvtx_tight_trkmatch_nbsv_per_non_loose_btag_jet_wcut;
  TH1F* h_gvtx_tight_trkmatch_nbsv_per_loose_bsv_jet_wcut;
  TH1F* h_gvtx_tight_trkmatch_nbsv_per_non_loose_bsv_jet_wcut;
  TH1F* h_gvtx_tight_trkmatch_nbsv_per_loose_bsv_plus_btagged_jet_wcut;
  TH1F* h_gvtx_tight_trkmatch_nbsv_per_non_loose_bsv_plus_btagged_jet_wcut;
  TH1F* h_gvtx_has_bSV_per_bjet_or_not_wcut;
  TH1F* h_gvtx_has_bSV_per_non_bjet_or_not_wcut;
  TH1F* h_gvtx_is_tight_btag_per_bjet_or_not_wcut;
  TH1F* h_gvtx_is_tight_btag_per_non_bjet_or_not_wcut;
  TH1F* h_gvtx_is_medium_btag_per_bjet_or_not_wcut;
  TH1F* h_gvtx_is_medium_btag_per_non_bjet_or_not_wcut;
  TH1F* h_gvtx_is_loose_btag_per_bjet_or_not_wcut;
  // investigate a GEN b-jet with either no loose b-tagged (a-type jet) or has loose b-tagged (b-type jet)
  TH1F* h_gvtx_a_type_diff_pT_bquark_jet_wcut;
  TH1F* h_gvtx_a_type_pT_jet_wcut;
  TH1F* h_gvtx_a_type_eta_bquark_jet_wcut;
  TH1F* h_gvtx_a_type_dR_bquark_wcut;
  TH1F* h_gvtx_a_type_nbsv_wcut;
  TH1F* h_gvtx_a_type_seed_ntrack_wcut;
  TH1F* h_gvtx_a_type_all_ntrack_wcut;
  TH1F* h_gvtx_a_type_all_tracks_pt_wcut;
  TH1F* h_gvtx_a_type_all_tracks_sigmadxybs_wcut;
  TH1F* h_gvtx_b_type_diff_pT_bquark_jet_wcut;
  TH1F* h_gvtx_b_type_dR_bquark_wcut;
  TH1F* h_gvtx_b_type_nbsv_wcut;
  TH1F* h_gvtx_b_type_seed_ntrack_wcut;
  TH1F* h_gvtx_b_type_all_ntrack_wcut;
  TH1F* h_gvtx_b_type_all_tracks_pt_wcut;
  TH1F* h_gvtx_b_type_all_tracks_sigmadxybs_wcut;
  TH1F* h_gvtx_is_loose_btag_per_non_bjet_or_not_wcut;
  // investigate a non GEN b-jet with either no loose b-tagged (c-type jet) or has loose b-tagged (d-type jet)
  TH1F* h_gvtx_c_type_dR_closest_lowpT_bquark_wcut;
  TH1F* h_gvtx_sub_c_type_pT_bquark_wcut;
  TH1F* h_gvtx_sub_c_type_pT_jet_wcut;
  TH1F* h_gvtx_sub_c_type_eta_bquark_jet_wcut;
  TH1F* h_gvtx_sub_c_type_nbsv_wcut;
  TH1F* h_gvtx_sub_c_type_all_ntrack_wcut;
  TH1F* h_gvtx_sub_c_type_seed_ntrack_wcut;
  TH1F* h_gvtx_sub_c_type_all_tracks_pt_wcut;
  TH1F* h_gvtx_sub_c_type_all_tracks_sigmadxybs_wcut;
  TH1F* h_gvtx_sub_c_type_diff_pT_bquark_jet_wcut;
  TH1F* h_gvtx_sub_c_type_dR_jets_close_bquark_wcut;
  TH1F* h_gvtx_sub_c_type_E_ratio_close_bquark_wcut;
  TH1F* h_gvtx_sub_c_type_pT_bquark_close_bquark_wcut;
  TH1F* h_gvtx_sub_c_type_pT_jet_close_bquark_wcut;
  TH1F* h_gvtx_fake_c_type_pT_bquark_wcut;
  TH1F* h_gvtx_fake_c_type_pT_jet_wcut;
  TH1F* h_gvtx_fake_c_type_eta_bquark_jet_wcut;
  TH1F* h_gvtx_fake_c_type_nbsv_wcut;
  TH1F* h_gvtx_fake_c_type_all_ntrack_wcut;
  TH1F* h_gvtx_fake_c_type_seed_ntrack_wcut;
  TH1F* h_gvtx_fake_c_type_all_tracks_pt_wcut;
  TH1F* h_gvtx_fake_c_type_all_tracks_sigmadxybs_wcut;
  TH1F* h_gvtx_fake_c_type_diff_pT_bquark_jet_wcut;
  TH1F* h_gvtx_c_type_nbsv_wcut;
  TH1F* h_gvtx_c_type_seed_ntrack_wcut;
  TH1F* h_gvtx_c_type_all_ntrack_wcut;
  TH1F* h_gvtx_c_type_all_tracks_pt_wcut;
  TH1F* h_gvtx_c_type_all_tracks_sigmadxybs_wcut;
  TH1F* h_gvtx_d_type_dR_closest_lowpT_bquark_wcut;
  TH1F* h_gvtx_sub_d_type_pT_bquark_wcut;
  TH1F* h_gvtx_sub_d_type_nbsv_wcut;
  TH1F* h_gvtx_sub_d_type_seed_ntrack_wcut;
  TH1F* h_gvtx_sub_d_type_all_tracks_pt_wcut;
  TH1F* h_gvtx_sub_d_type_all_tracks_sigmadxybs_wcut;
  TH1F* h_gvtx_sub_d_type_diff_pT_bquark_jet_wcut;
  TH1F* h_gvtx_d_type_nbsv_wcut;
  TH1F* h_gvtx_d_type_seed_ntrack_wcut;
  TH1F* h_gvtx_d_type_all_ntrack_wcut;
  TH1F* h_gvtx_d_type_all_tracks_pt_wcut;
  TH1F* h_gvtx_d_type_all_tracks_sigmadxybs_wcut;
  TH1F* h_gvtx_denominator_nsv_wcut;
  TH2F* h_2D_gvtx_ntrack_bsv_and_jet_seed_ntrack_from_bsv_wcut;
  TH2F* h_2D_gvtx_ntrack_bsv_and_jet_seed_ntrack_from_tight_trkmatch_bsv_wcut;
  TH1F* h_gvtx_sv_bquark_dist3d_wcut;
 
  //track investigation 
  TH1F* h_gvtx_seed_ntrack_bsvs_from_jets_wcut;
  TH1F* h_gvtx_seed_ntrack_per_bsv_from_jets_wcut;
  TH1F* h_gvtx_all_track_pt_from_jets_wcut;
  TH1F* h_gvtx_all_track_sigmadxybs_from_jets_wcut;
  TH1F* h_gvtx_all_track_npxhits_from_jets_wcut;
  TH1F* h_gvtx_all_track_nsthits_from_jets_wcut;
  TH1F* h_gvtx_all_track_npxlayers_from_jets_wcut;
  TH1F* h_gvtx_all_track_nstlayers_from_jets_wcut;
  TH1F* h_gvtx_all_track_rmin_from_jets_wcut;
  TH1F* h_gvtx_jet_seed_nm1_pt_from_jets_wcut;
  TH1F* h_gvtx_jet_seed_nm1_npxlayers_from_jets_wcut;
  TH1F* h_gvtx_jet_seed_nm1_nstlayers_from_jets_wcut;
  TH1F* h_gvtx_jet_seed_nm1_rmin_from_jets_wcut;
  TH1F* h_gvtx_jet_seed_nm1_sigmadxybs_from_jets_wcut;

  // (1) nstlayers
  TH1F* h_gvtx_one_cut_ntrack_from_jets_wcut;
  TH1F* h_gvtx_one_cut_track_pT_from_jets_wcut;
  TH1F* h_gvtx_one_cut_track_sigmadxybs_from_jets_wcut;
  TH1F* h_gvtx_one_cut_track_npxlayers_from_jets_wcut;
  TH1F* h_gvtx_one_cut_track_nstlayers_from_jets_wcut;
  TH1F* h_gvtx_one_cut_track_rmin_from_jets_wcut;
  // (1) nstlayers + (2) npxlayers
  TH1F* h_gvtx_two_cut_ntrack_from_jets_wcut;
  TH1F* h_gvtx_two_cut_track_pT_from_jets_wcut;
  TH1F* h_gvtx_two_cut_track_sigmadxybs_from_jets_wcut;
  TH1F* h_gvtx_two_cut_track_npxlayers_from_jets_wcut;
  TH1F* h_gvtx_two_cut_track_nstlayers_from_jets_wcut;
  TH1F* h_gvtx_two_cut_track_rmin_from_jets_wcut;
  // (1) nstlayers + (2) npxlayers  + (3) rmin 
  TH1F* h_gvtx_three_cut_ntrack_from_jets_wcut;
  TH1F* h_gvtx_three_cut_track_pT_from_jets_wcut;
  TH1F* h_gvtx_three_cut_track_sigmadxybs_from_jets_wcut;
  TH1F* h_gvtx_three_cut_track_npxlayers_from_jets_wcut;
  TH1F* h_gvtx_three_cut_track_nstlayers_from_jets_wcut;
  TH1F* h_gvtx_three_cut_track_rmin_from_jets_wcut;
  // (1) nstlayers + (2) npxlayers + (3) rmin  + (4) pT
  TH1F* h_gvtx_four_cut_ntrack_from_jets_wcut;
  TH1F* h_gvtx_four_cut_track_pT_from_jets_wcut;
  TH1F* h_gvtx_four_cut_track_sigmadxybs_from_jets_wcut;
  TH1F* h_gvtx_four_cut_track_npxlayers_from_jets_wcut;
  TH1F* h_gvtx_four_cut_track_nstlayers_from_jets_wcut;
  TH1F* h_gvtx_four_cut_track_rmin_from_jets_wcut;
  



 

  //////////////////////////////////////// 

  TH1F* h_minlspdist2d;
  TH1F* h_lspdist2d;
  TH1F* h_lspdist3d;

  TH1F* h_hlt_bits;
  TH1F* h_l1_bits;
  TH1F* h_filter_bits;

  TH1F* h_npu;

  TH1F* h_bsx;
  TH1F* h_bsy;
  TH1F* h_bsz;
  TH1F* h_bsphi;

  TH1F* h_npv;
  TH1F* h_pvx;
  TH1F* h_pvy;
  TH1F* h_pvxwide;
  TH1F* h_pvywide;
  TH1F* h_pvz;
  TH1F* h_pvcxx;
  TH1F* h_pvcxy;
  TH1F* h_pvcxz;
  TH1F* h_pvcyy;
  TH1F* h_pvcyz;
  TH1F* h_pvczz;
  TH1F* h_pvrho;
  TH1F* h_pvrhowide;
  TH1F* h_pvphi;
  TH1F* h_pvntracks;
  TH1F* h_pvscore;
  TH1F* h_pvsx;
  TH1F* h_pvsy;
  TH1F* h_pvsxwide;
  TH1F* h_pvsywide;
  TH1F* h_pvsz;
  TH1F* h_pvsrho;
  TH1F* h_pvsrhowide;
  TH1F* h_pvsphi;
  TH1F* h_pvsscore;
  TH1F* h_pvsdz;
  TH1F* h_pvsmindz;
  TH1F* h_pvsmaxdz;
  TH1F* h_pvsmindz_minscore;
  TH1F* h_pvsmaxdz_minscore;

  TH1F* h_njets;
  TH1F* h_njets20;
  static const int MAX_NJETS = 10;
  TH1F* h_jet_pt[MAX_NJETS+1];
  TH1F* h_jet_eta[MAX_NJETS+1];
  TH1F* h_jet_phi[MAX_NJETS+1];
  TH1F* h_jet_energy;
  TH1F* h_jet_ht;
  TH1F* h_jet_ht_40;

  TH1F* h_jet_pairdphi;
  TH1F* h_jet_pairdeta;
  TH1F* h_jet_pairdr;

  TH1F* h_met;
  TH1F* h_metphi;

  TH1F* h_nbtags[3];
  TH2F* h_nbtags_v_bquark_code[3];
  TH1F* h_jet_bdisc;
  TH2F* h_jet_bdisc_v_bquark_code;
  TH1F* h_bjet_pt;
  TH1F* h_bjet_eta;
  TH1F* h_bjet_phi;
  TH1F* h_bjet_energy;
  TH1F* h_bjet_pairdphi;
  TH1F* h_bjet_pairdeta;

  TH1F* h_nmuons[2];
  TH1F* h_nelectrons[2];
  TH1F* h_nleptons[2];

  TH1F* h_leptons_pt[2][2];
  TH1F* h_leptons_eta[2][2];
  TH1F* h_leptons_phi[2][2];
  TH1F* h_leptons_dxy[2][2];
  TH1F* h_leptons_dxybs[2][2];
  TH1F* h_leptons_dz[2][2];
  TH1F* h_leptons_iso[2][2];

  TH1F* h_n_vertex_seed_tracks;
  TH1F* h_vertex_seed_track_chi2dof;
  TH1F* h_vertex_seed_track_q;
  TH1F* h_vertex_seed_track_pt;
  TH1F* h_vertex_seed_track_eta;
  TH1F* h_vertex_seed_track_phi;
  TH2F* h_vertex_seed_track_phi_v_eta;
  TH1F* h_vertex_seed_track_dxy;
  TH1F* h_vertex_seed_track_dz;
  TH1F* h_vertex_seed_track_err_pt;
  TH1F* h_vertex_seed_track_err_eta;
  TH1F* h_vertex_seed_track_err_phi;
  TH1F* h_vertex_seed_track_err_dxy;
  TH1F* h_vertex_seed_track_err_dz;
  TH1F* h_vertex_seed_track_npxhits;
  TH1F* h_vertex_seed_track_nsthits;
  TH1F* h_vertex_seed_track_nhits;
  TH1F* h_vertex_seed_track_npxlayers;
  TH1F* h_vertex_seed_track_nstlayers;
  TH1F* h_vertex_seed_track_nlayers;
};

MFVEventHistos::MFVEventHistos(const edm::ParameterSet& cfg)
  : mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
	weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
	vertex_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertex_src"))),
	max_ntrackplots(cfg.getParameter<int>("max_ntrackplots")),
	do_scatterplots(cfg.getParameter<bool>("do_scatterplots"))
{

  edm::Service<TFileService> fs;

  h_w = fs->make<TH1F>("h_w", ";event weight;events/0.1", 100, 0, 10);
  h_nsv = fs->make<TH1F>("h_nsv", ";# of (loose) secondary vertices;arb. units", 40, 0, 40);

  h_gen_decay = fs->make<TH2F>("h_gen_decay", "0-2=e,mu,tau, 3=h;decay code #0;decay code #1", 4, 0, 4, 4, 0, 4);
  h_gen_flavor_code = fs->make<TH1F>("h_gen_flavor_code", ";quark flavor composition;events", 3, 0, 3);

  h_nbquarks = fs->make<TH1F>("h_nbquarks", ";# of bquarks;events", 20, 0, 20);
  h_bquark_pt = fs->make<TH1F>("h_bquark_pt", ";bquarks p_{T} (GeV);bquarks/10 GeV", 100, 0, 1000);
  h_bquark_eta = fs->make<TH1F>("h_bquark_eta", ";bquarks #eta (rad);bquarks/.08", 100, -4, 4);
  h_bquark_phi = fs->make<TH1F>("h_bquark_phi", ";bquarks #phi (rad);bquarks/.063", 100, -3.1416, 3.1416);
  h_bquark_energy = fs->make<TH1F>("h_bquark_energy", ";bquarks energy (GeV);bquarks/10 GeV", 100, 0, 1000);
  h_bquark_pairdphi = fs->make<TH1F>("h_bquark_pairdphi", ";bquark pair #Delta#phi (rad);bquark pairs/.063", 100, -3.1416, 3.1416);
  h_bquark_pairdeta = fs->make<TH1F>("h_bquark_pairdeta", ";bquark pair #Delta#eta (rad);bquark pairs/.1", 100, -5.0, 5.0);

  // overview
  h_gvtx_nsv = fs->make<TH1F>("h_gvtx_nsv", ";# of secondary vertices; events/1", 40, 0, 40);
  h_gvtx_sv_ntrack = fs->make<TH1F>("h_gvtx_sv_ntrack", ";# of tracks / SV; svs/1", 10, 0, 10);
  h_gvtx_njet_bboost_wcut = fs->make<TH1F>("h_gvtx_njet_bboost_wcut", "all four b-decays w/ b-quark pT > 20 GeV ;# of jets;events/1", 20, 0, 20);
  h_gvtx_bquark_pT = fs->make<TH1F>("h_gvtx_bquark_pT", ";GEN b-quark p_{T} (GeV);arb. units", 100, 0, 200);
  h_gvtx_bhad_bquark_dR = fs->make<TH1F>("h_gvtx_bhad_bquark_dR", ";#Delta R between mom. of a GEN b-quark and GEN b-had; arb. units", 70, 0, 2.0);
  h_2D_gvtx_bhad_bquark_dR_and_b_quark_pT = fs->make<TH2F>("h_2D_gvtx_bhad_bquark_dR_and_b_quark_pT", ";#Delta R between mom. of a GEN b-quark and GEN b-had; GEN b-quark p_{T} (GeV); arb. units", 70, 0, 2.0, 200, 0, 200);
  h_n_gen_bvtx = fs->make<TH1F>("h_n_gen_bvtx", ";# of GEN b-vertices (from non-b hadrons); events/1", 40, 0, 40);
  h_gvtx_njet = fs->make<TH1F>("h_gvtx_njet", ";# of jets;events/1", 10, 0, 10);
  h_gvtx_sanity_njet = fs->make<TH1F>("h_gvtx_sanity_njet", ";# of jets;events/1", 10, 0, 10);
  h_gvtx_nbjet = fs->make<TH1F>("h_gvtx_nbjet", ";# of b-jets;events/1", 10, 0, 10);
  h_gvtx_nloosebsvjet = fs->make<TH1F>("h_gvtx_nloosebsvjet", ";# of loose-sv bjets;events/1", 10, 0, 10);
  h_gvtx_nloosebsvplusbtaggedjet = fs->make<TH1F>("h_gvtx_nloosebsvplusbtaggedjet", ";# of loose-sv-btagged bjets;events/1", 10, 0, 10);
  

  h_gvtx_bhad_bquark_dR_wcut = fs->make<TH1F>("h_gvtx_bhad_bquark_dR_wcut", "b-quark pT > 20 GeV;#Delta R between mom. of a GEN b-quark and GEN b-had; arb. units", 70, 0, 2.0);
  h_gvtx_bhad_nonbhad_dR_wcut = fs->make<TH1F>("h_gvtx_bhad_nonbhad_dR_wcut", "b-quark pT > 20 GeV;#Delta R between mom. of a GEN non-b hadron and GEN b-had; arb. units", 70, 0, 2.0);
  h_2D_gvtx_bhad_nonbhad_dR_and_pT_wcut = fs->make<TH2F>("h_2D_gvtx_bhad_nonbhad_dR_and_pT_wcut", "b-quark pT > 20 GeV;#Delta R between mom. of a GEN non-b hadron and GEN b-had; GEN non-b hadron p_{T} (GeV); arb. units", 70, 0, 2.0, 100, 0, 50);
  h_2D_gvtx_bhad_nonbhad_dR_and_b_quark_pT_wcut = fs->make<TH2F>("h_2D_gvtx_bhad_nonbhad_dR_and_b_quark_pT_wcut", "b-quark pT > 20 GeV;#Delta R between mom. of a GEN non-b hadron and GEN b-had; GEN b-quark p_{T} (GeV); arb. units", 70, 0, 2.0, 200, 0, 200);
  h_2D_gvtx_bhad_bquark_dR_and_b_quark_pT_wcut = fs->make<TH2F>("h_2D_gvtx_bhad_bquark_dR_and_b_quark_pT_wcut", "b-quark pT > 20 GeV;#Delta R between mom. of a GEN b-quark and GEN b-had; GEN b-quark p_{T} (GeV); arb. units", 70, 0, 2.0, 200, 0, 200);
  h_gvtx_bhad_pT_wcut = fs->make<TH1F>("h_gvtx_bhad_pT_wcut", "b-quark pT > 20 GeV;GEN b-hadron p_{T} (GeV);arb. units", 20, 0, 200);
  h_gvtx_bquark_pT_wcut = fs->make<TH1F>("h_gvtx_bquark_pT_wcut", "b-quark pT > 20 GeV;GEN b-quark p_{T} (GeV);arb. units", 20, 0, 200);
  h_gvtx_bquark_jet_dR_wcut = fs->make<TH1F>("h_gvtx_bquark_jet_dR_wcut", "b-quark pT > 20 GeV;#Delta R between mom. of a closest RECO jet and a GEN b-quark; arb. units", 100, 0, 0.8);
  h_gvtx_tail_dR_jet_eta_bquark_wcut = fs->make<TH1F>("h_gvtx_tail_dR_jet_eta_bquark_wcut", "b-quark pT > 20 GeV && #Delta R (closest matched-jet, b-quark) > 0.2; |#eta| of a GEN b-quark; arb. units", 100, 0, 3.0);
  h_gvtx_peak_dR_jet_eta_bquark_wcut = fs->make<TH1F>("h_gvtx_peak_dR_jet_eta_bquark_wcut", "b-quark pT > 20 GeV && #Delta R (closest matched-jet, b-quark) < 0.2; |#eta| of a GEN b-quark; arb. units", 100, 0, 3.0);
  h_gvtx_tail_dR_jet_pT_bquark_wcut = fs->make<TH1F>("h_gvtx_tail_dR_jet_pT_bquark_wcut", "b-quark pT > 20 GeV && #Delta R (closest matched-jet, b-quark) > 0.2; p_{T} of a GEN b-quark (GeV); arb. units", 200, 0, 200);
  h_gvtx_peak_dR_jet_pT_bquark_wcut = fs->make<TH1F>("h_gvtx_peak_dR_jet_pT_bquark_wcut", "b-quark pT > 20 GeV && #Delta R (closest matched-jet, b-quark) < 0.2; p_{T} of a GEN b-quark (GeV); arb. units", 200, 0, 200);
  h_gvtx_peak_dR_jet_pT_bjet_wcut = fs->make<TH1F>("h_gvtx_peak_dR_jet_pT_bjet_wcut", "b-quark pT > 20 GeV && #Delta R (closest matched-jet, b-quark) < 0.2; p_{T} of a b-jet (GeV); arb. units", 200, 0, 200);
  h_gvtx_bquark_closest_jet_pT_wcut = fs->make<TH1F>("h_gvtx_bquark_closest_jet_pT_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;p_{T} a closest RECO jet w.r.t GEN b-quark; arb. units", 100, 0, 200);
  h_gvtx_bquark_closest_jet_dR_wcut = fs->make<TH1F>("h_gvtx_bquark_closest_jet_dR_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;#Delta R between mom. of a closest RECO jet and a GEN b-quark; arb. units", 50, 0, 0.4);
  h_gvtx_bquark_closest_jet_E_ratio_wcut = fs->make<TH1F>("h_gvtx_bquark_closest_jet_E_ratio_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;#frac{macthed jet energy}{b-quark energy}; arb. units", 60, 0.0, 3.0);
  h_gvtx_bhad_closest_jet_dR_wcut = fs->make<TH1F>("h_gvtx_bhad_closest_jet_dR_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;#Delta R between mom. of a closest RECO jet and a GEN b-hadron; arb. units", 50, 0, 0.4);
  h_gvtx_bhad_closest_jet_pT_wcut = fs->make<TH1F>("h_gvtx_bhad_closest_jet_pT_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;p_{T} a closest RECO jet w.r.t GEN b-hadron; arb. units", 100, 0, 200);
  h_gvtx_bquark_closest_jet_res_pT_wcut = fs->make<TH1F>("h_gvtx_bquark_closest_jet_res_pT_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;sum track p_{T} of a closest RECO jet - p_{T} of a GEN b-quark; arb. units", 60, -30.0, 30.0);
  h_2D_gvtx_bquark_closest_jet_dR_ndau_wcut = fs->make<TH2F>("h_2D_gvtx_bquark_closest_jet_dR_ndau_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;#Delta R between mom. of a closest RECO jet and a GEN b-quark; # of b-had daughters; arb. units", 70, 0, 7.0, 20, 0, 20);
  h_gvtx_bquark_closest_dau_to_closest_jet_dR_wcut = fs->make<TH1F>("h_gvtx_bquark_closest_dau_to_closest_jet_dR_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;#Delta R between mom. of a closest RECO jet and its closest b-had dau; arb. units", 70, 0, 7.0);
  h_gvtx_all_ntrack_from_jets_wcut = fs->make<TH1F>("h_gvtx_all_ntrack_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;# of tracks per a matched jet;", 50, 0, 50);
  h_gvtx_jet_seed_ntrack_per_bjet_wcut = fs->make<TH1F>("h_gvtx_jet_seed_ntrack_per_bjet_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;# of seed tracks per a b-jet;", 50, 0, 50);
  h_gvtx_jet_seed_ntrack_per_non_bjet_wcut = fs->make<TH1F>("h_gvtx_jet_seed_ntrack_per_non_bjet_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;# of seed tracks per a non b-jet;", 50, 0, 50);
  h_gvtx_jet_seed_ntrack_per_tight_btag_wcut = fs->make<TH1F>("h_gvtx_jet_seed_ntrack_per_tight_btag_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;# of seed tracks per a tight-btagged jet;", 50, 0, 50);
  h_gvtx_jet_seed_ntrack_per_non_tight_btag_wcut = fs->make<TH1F>("h_gvtx_jet_seed_ntrack_per_non_tight_btag_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;# of seed tracks per a non tight-btagged jet;", 50, 0, 50);
  h_gvtx_jet_seed_ntrack_per_medium_btag_wcut = fs->make<TH1F>("h_gvtx_jet_seed_ntrack_per_medium_btag_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;# of seed tracks per a medium-btagged jet;", 50, 0, 50);
  h_gvtx_jet_seed_ntrack_per_non_medium_btag_wcut = fs->make<TH1F>("h_gvtx_jet_seed_ntrack_per_non_medium_btag_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;# of seed tracks per a non medium-btagged jet;", 50, 0, 50);
  h_gvtx_jet_seed_ntrack_per_loose_btag_wcut = fs->make<TH1F>("h_gvtx_jet_seed_ntrack_per_loose_btag_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;# of seed tracks per a loose-btagged jet;", 50, 0, 50);
  h_gvtx_jet_seed_ntrack_per_non_loose_btag_wcut = fs->make<TH1F>("h_gvtx_jet_seed_ntrack_per_non_loose_btag_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;# of seed tracks per a non loose-btagged jet;", 50, 0, 50);
  h_gvtx_jet_seed_ntrack_per_loose_bsv_jet_wcut = fs->make<TH1F>("h_gvtx_jet_seed_ntrack_per_loose_bsv_jet_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;# of seed tracks per a loose-bsv jet;", 50, 0, 50);
  h_gvtx_jet_seed_ntrack_per_non_loose_bsv_jet_wcut = fs->make<TH1F>("h_gvtx_jet_seed_ntrack_per_non_loose_bsv_jet_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;# of seed tracks per a non loose-bsv jet;", 50, 0, 50);
  h_gvtx_jet_seed_ntrack_per_loose_bsv_plus_btagged_jet_wcut = fs->make<TH1F>("h_gvtx_jet_seed_ntrack_per_loose_bsv_plus_btagged_jet_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;# of seed tracks per a loose-bsv-plus-btagged jet;", 50, 0, 50);
  h_gvtx_jet_seed_ntrack_per_non_loose_bsv_plus_btagged_jet_wcut = fs->make<TH1F>("h_gvtx_jet_seed_ntrack_per_non_loose_bsv_plus_btagged_jet_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;# of seed tracks per a non loose-bsv-plus-btagged jet;", 50, 0, 50);

  h_gvtx_jet_seed_track_pT_from_jets_wcut = fs->make<TH1F>("h_gvtx_jet_seed_track_pT_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;p_{T} of a seed track in a matched jet;", 20, 0, 10);
  h_gvtx_jet_seed_track_sigmadxybs_from_jets_wcut = fs->make<TH1F>("h_gvtx_jet_seed_track_sigmadxybs_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;#sigma_{dxy} of a seed track in a matched jet;", 40, -10, 10);
  h_gvtx_jet_seed_track_npxlayers_from_jets_wcut = fs->make<TH1F>("h_gvtx_jet_seed_track_npxlayers_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;npxlayers of a seed track in a matched jet;", 12, 0, 12);
  h_gvtx_jet_seed_track_nstlayers_from_jets_wcut = fs->make<TH1F>("h_gvtx_jet_seed_track_nstlayers_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;nstlayers of a seed track in a matched jet;", 28, 0, 28);
  h_gvtx_jet_seed_track_rmin_from_jets_wcut = fs->make<TH1F>("h_gvtx_jet_seed_track_rmin_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;r_{min} of a seed track in a matched jet;", 5, 0, 5);
  h_gvtx_seed_track_pT_from_jets_wcut = fs->make<TH1F>("h_gvtx_seed_track_pT_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;p_{T} of a seed track from SVs in a matched jet;", 20, 0, 10);
  h_gvtx_seed_track_sigmadxybs_from_jets_wcut = fs->make<TH1F>("h_gvtx_seed_track_sigmadxybs_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;#sigma_{dxy} of a seed track from SVs in a matched jet;", 40, -10, 10);
  h_gvtx_seed_track_npxlayers_from_jets_wcut = fs->make<TH1F>("h_gvtx_seed_track_npxlayers_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;npxlayers of a seed track from SVs in a matched jet ;", 12, 0, 12);
  h_gvtx_seed_track_nstlayers_from_jets_wcut = fs->make<TH1F>("h_gvtx_seed_track_nstlayers_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;nstlayers of a seed track from SVs in a matched jet;", 28, 0, 28);
  h_gvtx_seed_track_rmin_from_jets_wcut = fs->make<TH1F>("h_gvtx_seed_track_rmin_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;r_{min} of a seed track from SVs in a matched jet;", 5, 0, 5);

  h_gvtx_seed_ntrack_bsvs_from_jets_wcut = fs->make<TH1F>("h_gvtx_seed_ntrack_bsvs_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;# of seed tracks from SVs per a matched jet;", 50, 0, 50);
  h_gvtx_seed_ntrack_per_bsv_from_jets_wcut = fs->make<TH1F>("h_gvtx_seed_ntrack_per_bsv_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;# of seed tracks per SV in a matched jet;", 10, 0, 10);
  h_gvtx_sum_pT_all_tracks_from_jets_wcut = fs->make<TH1F>("h_gvtx_sum_pT_all_tracks_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; sum p_{T} of matched-jet tracks;", 25, 0, 200);
  
  h_gvtx_shared_bjet_or_not_wcut = fs->make<TH1F>("h_gvtx_shared_bjet_or_not_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; shared b-jets ?; arb. units", 3, 0, 3);

  //sv investigation 
  h_gvtx_sv_trkonly_mom_jet_mom_dR_wcut = fs->make<TH1F>("h_gvtx_sv_trkonly_mom_jet_mom_dR_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;#Delta R between mom. of a closest RECO jet and most-matched SV by tracks only; arb. units", 120, 0, 3);
  h_gvtx_sv_jetbytrk_mom_jet_mom_dR_wcut = fs->make<TH1F>("h_gvtx_sv_jetbytrk_mom_jet_mom_dR_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;#Delta R between mom. of a closest RECO jet and most-matched SV by jet's ntrack; arb. units", 120, 0, 3);
  h_gvtx_sv_trkplusjetbytrk_mom_jet_mom_dR_wcut = fs->make<TH1F>("h_gvtx_sv_trkplusjetbytrk_mom_jet_mom_dR_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;#Delta R between mom. of a closest RECO jet and most-matched SV by tracks + jet's ntrack; arb. units", 120, 0, 3);
  h_gvtx_sv_displ_vec_jet_mom_dR_wcut = fs->make<TH1F>("h_gvtx_sv_displ_vec_jet_mom_dR_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;#Delta R between mom. of a closest RECO jet and most-matched SV by its displacement; arb. units", 120, 0, 3);

  /*
  h_2D_gvtx_sv_jetbytrk_mom_jet_mom_dR_jntrack_wtightcut = fs->make<TH2F>("h_2D_gvtx_sv_jetbytrk_mom_jet_mom_dR_jntrack_wtightcut", "b-quark pT > 25 GeV w/ 1-1 matched jet to b-decay && Is jet of most-matched SV;#Delta R between mom. of a closest RECO jet and most-matched SV by jet's ntrack; ntrack in a jet from most-matched SV; arb. units", 120, 0, 3.0, 20, 0, 20);
  h_2D_gvtx_sv_jetbytrk_mom_jet_mom_dR_ngdau_wcut = fs->make<TH2F>("h_2D_gvtx_sv_jetbytrk_mom_jet_mom_dR_ngdau_wcut", "b-quark pT > 25 GeV w/ 1-1 matched jet to b-decay;#Delta R between mom. of a closest RECO jet and most-matched SV by jet's ntrack; # of b-quark daughters; arb. units", 120, 0, 3.0, 20, 0, 20);
  h_gvtx_sv_jntrack_wtightcut = fs->make<TH1F>("h_gvtx_sv_jntrack_wtightcut", "b-quark pT > 25 GeV w/ 1-1 matched jet to b-decay && Is jet of most-matched SV; ntrack in a jet from most-matched SV; arb. units", 20, 0, 20);
  h_gvtx_jntrack_wtightcut = fs->make<TH1F>("h_gvtx_jntrack_wtightcut", "b-quark pT > 25 GeV w/ 1-1 matched jet to b-decay && Is jet of most-matched SV; # of all tracks per a matched jet; arb. units", 50, 0, 50);
  h_gvtx_seed_jntrack_wtightcut = fs->make<TH1F>("h_gvtx_seed_jntrack_wtightcut", "b-quark pT > 25 GeV w/ 1-1 matched jet to b-decay && Is jet of most-matched SV; # of seed tracks per a matched jet; arb. units", 50, 0, 50);
  h_gvtx_sv_ngdau_wtightcut = fs->make<TH1F>("h_gvtx_sv_ngdau_wtightcut", "b-quark pT > 25 GeV w/ 1-1 matched jet to b-decay && Is jet of most-matched SV; # of b-quark daughters; arb. units", 20, 0, 20);
  h_gvtx_sv_jetbytrk_mom_jet_mom_dR_wtightcut = fs->make<TH1F>("h_gvtx_sv_jetbytrk_mom_jet_mom_dR_wtightcut", "b-quark pT > 25 GeV w/ 1-1 matched jet to b-decay && Is jet of most-matched SV;#Delta R between mom. of a closest RECO jet and most-matched SV by jet's ntrack; arb. units", 120, 0, 3.0);
  h_gvtx_sv_ngdau_miss_wtightcut = fs->make<TH1F>("h_gvtx_sv_ngdau_miss_wtightcut", "b-quark pT > 25 GeV w/ 1-1 matched jet to b-decay && Is *NOT* jet of most-matched SV; # of b-quark daughters; arb. units", 20, 0, 20);
  h_2D_gvtx_sv_jetbytrk_mom_jet_mom_dR_ngdau_wtightcut = fs->make<TH2F>("h_2D_gvtx_sv_jetbytrk_mom_jet_mom_dR_ngdau_wtightcut", "b-quark pT > 25 GeV w/ 1-1 matched jet to b-decay && Is jet of most-matched SV;#Delta R between mom. of a closest RECO jet and most-matched SV by jet's ntrack; # of b-quark daughters; arb. units", 120, 0, 3.0, 20, 0, 20);
  */

  h_gvtx_sv_trkonly_mom_bquark_mom_dR_wcut = fs->make<TH1F>("h_gvtx_sv_trkonly_mom_bquark_mom_dR_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;#Delta R between mom. of a GEN b-quark and most-matched SV by tracks only; arb. units", 120, 0, 3);
  h_gvtx_sv_jetbytrk_mom_bquark_mom_dR_wcut = fs->make<TH1F>("h_gvtx_sv_jetbytrk_mom_bquark_mom_dR_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;#Delta R between mom. of a GEN b-quark and most-matched SV by jet's ntrack; arb. units", 120, 0, 3);
  h_gvtx_sv_trkplusjetbytrk_mom_bquark_mom_dR_wcut = fs->make<TH1F>("h_gvtx_sv_trkplusjetbytrk_mom_bquark_mom_dR_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;#Delta R between mom. of a GEN b-quark and most-matched SV by tracks + jet's ntrack; arb. units", 120, 0, 3);
  h_gvtx_sv_displ_vec_bquark_mom_dR_wcut = fs->make<TH1F>("h_gvtx_sv_displ_vec_bquark_mom_dR_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;#Delta R between mom. of a GEN b-quark and most-matched SV by its displacement; arb. units", 120, 0, 3);

  h_gvtx_sv_bquark_closest_dist3d_wcut = fs->make<TH1F>("h_gvtx_sv_bquark_closest_dist3d_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;dist3d b/w a GEN b-quark and most-matched SV (cm); arb. units", 120, 0, 3);
  //match SVs with jet by sv_jetbytrk_mom_jet_mom_dR < 0.02
  //h_gvtx_sv_inv_mass_wcut = fs->make<TH1F>("h_gvtx_sv_inv_mass_wcut", "b-quark pT > 25 GeV w/ 1-1 matched jet to b-decay;invariant mass of a matched SV; SVs/1", 80, 0, 8);
  h_gvtx_sv_bquark_dist3d_wcut = fs->make<TH1F>("h_gvtx_sv_bquark_dist3d_wcut", "b-quark pT > 20 GeV;dist3d b/w a GEN b-quark decay vtx and its closest SV (cm); arb. units", 120, 0, 3);
  h_gvtx_bsv_dBV_wcut = fs->make<TH1F>("h_gvtx_bsv_dBV_wcut", "b-quark pT > 20 GeV; bs2dist (cm.); arb. units", 300, 0, 3);
  h_gvtx_match_pT_wcut = fs->make<TH1F>("h_gvtx_match_pT_wcut", "b-quark pT > 20 GeV; |track #pT_{SV} - track #pT_{jet}| (GeV); arb. units", 100, 0, 0.005);
  h_gvtx_match_pT_phicut_wcut = fs->make<TH1F>("h_gvtx_match_pT_phicut_wcut", "b-quark pT > 20 GeV && |track #phi_{SV} - track #phi_{jet}| < 0.0001; |track #pT_{SV} - track #pT_{jet}| (GeV); arb. units", 100, 0, 0.005);
  h_gvtx_match_pT_etacut_wcut = fs->make<TH1F>("h_gvtx_match_pT_etacut_wcut", "b-quark pT > 20 GeV && |track #eta_{SV} - track #eta_{jet}| < 0.0001; |track #pT_{SV} - track #pT_{jet}| (GeV); arb. units", 100, 0, 0.005);
  h_gvtx_match_eta_wcut = fs->make<TH1F>("h_gvtx_match_eta_wcut", "b-quark pT > 20 GeV; |track #eta_{SV} - track #eta_{jet}|; arb. units", 100, 0, 0.005);
  h_gvtx_match_eta_phicut_wcut = fs->make<TH1F>("h_gvtx_match_eta_phicut_wcut", "b-quark pT > 20 GeV && |track #phi_{SV} - track #phi_{jet}| < 0.0001; |track #eta_{SV} - track #eta_{jet}| (GeV); arb. units", 100, 0, 0.005);
  h_gvtx_match_eta_pTcut_wcut = fs->make<TH1F>("h_gvtx_match_eta_pTcut_wcut", "b-quark pT > 20 GeV && |track #pT_{SV} - track #pT_{jet}| < 0.0001; |track #eta_{SV} - track #eta_{jet}| (GeV); arb. units", 100, 0, 0.005);
  h_gvtx_match_phi_wcut = fs->make<TH1F>("h_gvtx_match_phi_wcut", "b-quark pT > 20 GeV; |track #phi_{SV} - track #phi_{jet}|; arb. units", 100, 0, 0.005);
  h_gvtx_match_phi_etacut_wcut = fs->make<TH1F>("h_gvtx_match_phi_etacut_wcut", "b-quark pT > 20 GeV && |track #eta_{SV} - track #eta_{jet}| < 0.0001; |track #phi_{SV} - track #phi_{jet}| (GeV); arb. units", 100, 0, 0.005);
  h_gvtx_match_phi_pTcut_wcut = fs->make<TH1F>("h_gvtx_match_phi_pTcut_wcut", "b-quark pT > 20 GeV && |track #pT_{SV} - track #pT_{jet}| < 0.0001; |track #phi_{SV} - track #phi_{jet}| (GeV); arb. units", 100, 0, 0.005);
  h_2D_gvtx_numerator_nbsv_bjets_wcut = fs->make<TH2F>("h_2D_gvtx_numerator_nbsv_bjets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of SVs matched with the b-jets; # bjets; arb. units", 20, 0, 20, 20, 0, 20);
  h_2D_gvtx_numerator_tight_trkmatch_nbsv_bjets_wcut = fs->make<TH2F>("h_2D_gvtx_numerator_tight_trkmatch_nbsv_bjets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of bSVs; # bjets; events/1", 20, 0, 20, 20, 0, 20);
  h_2D_gvtx_denominator_nbsv_bjets_wcut = fs->make<TH2F>("h_2D_gvtx_denominator_nbsv_bjets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of total SVs; # bjets; arb. units", 20, 0, 20, 20, 0, 20);
  h_gvtx_nbsv_by_nsv_wcut = fs->make<TH1F>("h_gvtx_nbsv_by_nsv_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; #frac{# of SVs matched with the b-jets}{# of total SVs}; arb. units", 4, 0.0, 2.0);
  h_gvtx_numerator_nbsv_wcut = fs->make<TH1F>("h_gvtx_numerator_nbsv_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of SVs matched with the b-jets; arb. units", 10, 0, 10);
  h_gvtx_numerator_tight_trkmatch_nbsv_wcut = fs->make<TH1F>("h_gvtx_numerator_tight_trkmatch_nbsv_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of bSVs; arb. units", 10, 0, 10);
  h_gvtx_tight_trkmatch_nbsv_per_bjet_wcut = fs->make<TH1F>("h_gvtx_tight_trkmatch_nbsv_per_bjet_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of bSVs per a b-jet; arb. units", 10, 0, 10);
  h_gvtx_tight_trkmatch_nbsv_per_non_bjet_wcut = fs->make<TH1F>("h_gvtx_tight_trkmatch_nbsv_per_non_bjet_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of bSVs per a non b-jet; arb. units", 10, 0, 10);
  h_gvtx_tight_trkmatch_nbsv_per_tight_btag_jet_wcut = fs->make<TH1F>("h_gvtx_tight_trkmatch_nbsv_per_tight_btag_jet_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of bSVs per a tight b-tagged jet; arb. units", 10, 0, 10);
  h_gvtx_tight_trkmatch_nbsv_per_non_tight_btag_jet_wcut = fs->make<TH1F>("h_gvtx_tight_trkmatch_nbsv_per_non_tight_btag_jet_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of bSVs per a non tight b-tagged jet; arb. units", 10, 0, 10);
  h_gvtx_tight_trkmatch_nbsv_per_medium_btag_jet_wcut = fs->make<TH1F>("h_gvtx_tight_trkmatch_nbsv_per_medium_btag_jet_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of bSVs per a medium b-tagged jet; arb. units", 10, 0, 10);
  h_gvtx_tight_trkmatch_nbsv_per_non_medium_btag_jet_wcut = fs->make<TH1F>("h_gvtx_tight_trkmatch_nbsv_per_non_medium_btag_jet_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of bSVs per a non medium b-tagged jet; arb. units", 10, 0, 10);
  h_gvtx_tight_trkmatch_nbsv_per_loose_btag_jet_wcut = fs->make<TH1F>("h_gvtx_tight_trkmatch_nbsv_per_loose_btag_jet_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of bSVs per a loose b-tagged jet; arb. units", 10, 0, 10);
  h_gvtx_tight_trkmatch_nbsv_per_non_loose_btag_jet_wcut = fs->make<TH1F>("h_gvtx_tight_trkmatch_nbsv_per_non_loose_btag_jet_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of bSVs per a non loose b-tagged jet; arb. units", 10, 0, 10);
  h_gvtx_tight_trkmatch_nbsv_per_loose_bsv_jet_wcut = fs->make<TH1F>("h_gvtx_tight_trkmatch_nbsv_per_loose_bsv_jet_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of bSVs per a loose-bsv jet; arb. units", 10, 0, 10);
  h_gvtx_tight_trkmatch_nbsv_per_non_loose_bsv_jet_wcut = fs->make<TH1F>("h_gvtx_tight_trkmatch_nbsv_per_non_loose_bsv_jet_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of bSVs per a non loose-bsv jet; arb. units", 10, 0, 10);
  h_gvtx_tight_trkmatch_nbsv_per_loose_bsv_plus_btagged_jet_wcut = fs->make<TH1F>("h_gvtx_tight_trkmatch_nbsv_per_loose_bsv_plus_btagged_jet_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of bSVs per a loose-bsv-plus-btagged jet; arb. units", 10, 0, 10);
  h_gvtx_tight_trkmatch_nbsv_per_non_loose_bsv_plus_btagged_jet_wcut = fs->make<TH1F>("h_gvtx_tight_trkmatch_nbsv_per_non_loose_bsv_plus_btagged_jet_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of bSVs per a non loose-bsv-plus_btagged jet; arb. units", 10, 0, 10);

  h_gvtx_has_bSV_per_bjet_or_not_wcut = fs->make<TH1F>("h_gvtx_has_bSV_per_bjet_or_not_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; has at least one bSV per a b-jet or not ?; arb. units", 3, 0, 3);
  h_gvtx_has_bSV_per_non_bjet_or_not_wcut = fs->make<TH1F>("h_gvtx_has_bSV_per_non_bjet_or_not_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; has at least one bSV per a non b-jet or not ?; arb. units", 3, 0, 3);
  h_gvtx_is_tight_btag_per_bjet_or_not_wcut = fs->make<TH1F>("h_gvtx_is_tight_btag_per_bjet_or_not_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; is this b-jet also tight b-tagged ?; arb. units", 3, 0, 3);
  h_gvtx_is_tight_btag_per_non_bjet_or_not_wcut = fs->make<TH1F>("h_gvtx_is_tight_btag_per_non_bjet_or_not_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; is this non b-jet also tight b-tagged ?; arb. units", 3, 0, 3);
  h_gvtx_is_medium_btag_per_bjet_or_not_wcut = fs->make<TH1F>("h_gvtx_is_medium_btag_per_bjet_or_not_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; is this b-jet also medium b-tagged ?; arb. units", 3, 0, 3);
  h_gvtx_is_medium_btag_per_non_bjet_or_not_wcut = fs->make<TH1F>("h_gvtx_is_medium_btag_per_non_bjet_or_not_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; is this non b-jet also medium b-tagged ?; arb. units", 3, 0, 3);
  h_gvtx_is_loose_btag_per_bjet_or_not_wcut = fs->make<TH1F>("h_gvtx_is_loose_btag_per_bjet_or_not_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; is this b-jet also loose b-tagged ?; arb. units", 3, 0, 3);
  h_gvtx_a_type_diff_pT_bquark_jet_wcut = fs->make<TH1F>("h_gvtx_a_type_diff_pT_bquark_jet_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;p_{T} of a type-a jet - p_{T} of a GEN b-quark; arb. units", 60, -30.0, 30.0);
  h_gvtx_a_type_pT_jet_wcut = fs->make<TH1F>("h_gvtx_a_type_pT_jet_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;a type-a jet p_{T} (GeV);arb. units", 100, 0, 200);
  h_gvtx_a_type_eta_bquark_jet_wcut = fs->make<TH1F>("h_gvtx_a_type_eta_bquark_jet_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; |#eta| of a GEN b-quark; arb. units", 100, 0, 3.0);
  h_gvtx_a_type_dR_bquark_wcut = fs->make<TH1F>("h_gvtx_a_type_dR_bquark_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;#Delta R between mom. of a type-a jet and a GEN b-quark; arb. units", 50, 0, 0.4);
  h_gvtx_a_type_nbsv_wcut = fs->make<TH1F>("h_gvtx_a_type_nbsv_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of bSVs in a type-a jets; arb. units", 10, 0, 10);
  h_gvtx_a_type_seed_ntrack_wcut = fs->make<TH1F>("h_gvtx_a_type_seed_ntrack_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of seed tracks in a type-a jets; arb. units", 10, 0, 10);
  h_gvtx_a_type_all_ntrack_wcut = fs->make<TH1F>("h_gvtx_a_type_all_ntrack_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of all tracks in a type-a jets; arb. units", 10, 0, 10);
  h_gvtx_a_type_all_tracks_pt_wcut = fs->make<TH1F>("h_gvtx_a_type_all_tracks_pt_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;p_{T} of a track in a type-a jet;", 40, 0, 10);
  h_gvtx_a_type_all_tracks_sigmadxybs_wcut = fs->make<TH1F>("h_gvtx_a_type_all_tracks_sigmadxybs_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;#sigma_{dxy} of a track in a type-a jet;", 40, -10, 10);
  h_gvtx_b_type_diff_pT_bquark_jet_wcut = fs->make<TH1F>("h_gvtx_b_type_diff_pT_bquark_jet_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;p_{T} of a type-b jet - p_{T} of a GEN b-quark; arb. units", 60, -30.0, 30.0);
  h_gvtx_b_type_dR_bquark_wcut = fs->make<TH1F>("h_gvtx_b_type_dR_bquark_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;#Delta R between mom. of a type-b jet and a GEN b-quark; arb. units", 50, 0, 0.4);
  h_gvtx_b_type_nbsv_wcut = fs->make<TH1F>("h_gvtx_b_type_nbsv_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of bSVs in a type-b jets; arb. units", 10, 0, 10);
  h_gvtx_b_type_seed_ntrack_wcut = fs->make<TH1F>("h_gvtx_b_type_seed_ntrack_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of seed tracks in a type-b jets; arb. units", 10, 0, 10);
  h_gvtx_b_type_all_ntrack_wcut = fs->make<TH1F>("h_gvtx_b_type_all_ntrack_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of all tracks in a type-b jets; arb. units", 10, 0, 10);
  h_gvtx_b_type_all_tracks_pt_wcut = fs->make<TH1F>("h_gvtx_b_type_all_tracks_pt_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;p_{T} of a track in a type-b jet;", 40, 0, 10);
  h_gvtx_b_type_all_tracks_sigmadxybs_wcut = fs->make<TH1F>("h_gvtx_b_type_all_tracks_sigmadxybs_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;#sigma_{dxy} of a track in a type-b jet;", 40, -10, 10);
  h_gvtx_is_loose_btag_per_non_bjet_or_not_wcut = fs->make<TH1F>("h_gvtx_is_loose_btag_per_non_bjet_or_not_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; is this non b-jet also loose b-tagged ?; arb. units", 3, 0, 3);
  h_gvtx_c_type_dR_closest_lowpT_bquark_wcut = fs->make<TH1F>("h_gvtx_c_type_dR_closest_lowpT_bquark_wcut", "b-quark pT < 20 GeV;#Delta R between mom. of a type-c jet and a lowpT GEN b-quark; arb. units", 50, 0, 4.0);
  h_gvtx_sub_c_type_eta_bquark_jet_wcut = fs->make<TH1F>("h_gvtx_sub_c_type_eta_bquark_jet_wcut", "b-quark pT > 20 GeV w/ 1-1 matched type-c jet to b-decay; |#eta| of a GEN b-quark; arb. units", 100, 0, 3.0);
  h_gvtx_sub_c_type_pT_bquark_wcut = fs->make<TH1F>("h_gvtx_sub_c_type_pT_bquark_wcut", "b-quark pT < 20 GeV w/ 1-1 matched type-c jet to b-decay;GEN b-quark p_{T} (GeV);arb. units", 50, 0, 25);
  h_gvtx_sub_c_type_pT_jet_wcut = fs->make<TH1F>("h_gvtx_sub_c_type_pT_jet_wcut", "b-quark pT < 20 GeV w/ 1-1 matched type-c jet to b-decay;a type-c jet p_{T} (GeV);arb. units", 100, 0, 200);
  h_gvtx_sub_c_type_nbsv_wcut = fs->make<TH1F>("h_gvtx_sub_c_type_nbsv_wcut", "b-quark pT < 20 GeV w/ 1-1 matched type-c jet to b-decay; # of bSVs in a type-c jets; arb. units", 10, 0, 10);
  h_gvtx_sub_c_type_all_ntrack_wcut = fs->make<TH1F>("h_gvtx_sub_c_type_all_ntrack_wcut", "b-quark pT < 20 GeV w/ 1-1 matched type-c jet to b-decay; # of all tracks in a type-c jet; arb. units", 10, 0, 10);
  h_gvtx_sub_c_type_seed_ntrack_wcut = fs->make<TH1F>("h_gvtx_sub_c_type_seed_ntrack_wcut", "b-quark pT < 20 GeV w/ 1-1 matched type-c jet to b-decay; # of seed tracks in a type-c jet; arb. units", 10, 0, 10);
  h_gvtx_sub_c_type_all_tracks_pt_wcut = fs->make<TH1F>("h_gvtx_sub_c_type_all_tracks_pt_wcut", "b-quark pT < 20 GeV w/ 1-1 matched type-c jet to b-decay;p_{T} of a track in a type-c jet;", 40, 0, 10);
  h_gvtx_sub_c_type_all_tracks_sigmadxybs_wcut = fs->make<TH1F>("h_gvtx_sub_c_type_all_tracks_sigmadxybs_wcut", "b-quark pT < 20 GeV w/ 1-1 matched type-c jet to b-decay;#sigma_{dxy} of a track in a type-c jet;", 40, -10, 10);
  h_gvtx_sub_c_type_diff_pT_bquark_jet_wcut = fs->make<TH1F>("h_gvtx_sub_c_type_diff_pT_bquark_jet_wcut", "b-quark pT < 20 GeV w/ 1-1 matched type-c jet to b-decay;p_{T} of a type-c jet - p_{T} of a lowpT GEN b-quark; arb. units", 60, -30.0, 30.0);
  h_gvtx_sub_c_type_dR_jets_close_bquark_wcut = fs->make<TH1F>("h_gvtx_sub_c_type_dR_jets_close_bquark_wcut", "b-quark pT < 20 GeV w/ dR-0.4 b-quarks && w/ 1-1 matched type-c jet to b-decay;#Delta R between mom. of a type-c jet and a type-a jet w/ dR-0.4 b-quarks; arb. units", 50, 0, 4.0);
  h_gvtx_sub_c_type_E_ratio_close_bquark_wcut = fs->make<TH1F>("h_gvtx_sub_c_type_E_ratio_close_bquark_wcut", "b-quark pT < 20 GeV w/ dR-0.4 b-quarks && w/ 1-1 matched type-c jet to b-decay;#frac{jet-pair energy}{b-quark pair energy}; arb. units", 60, 0.0, 3.0);
  h_gvtx_sub_c_type_pT_bquark_close_bquark_wcut = fs->make<TH1F>("h_gvtx_sub_c_type_pT_bquark_close_bquark_wcut", "b-quark pT < 20 GeV w/ dR-0.4 b-quarks && w/ 1-1 matched type-c jet to b-decay;GEN b-quark p_{T} (GeV);arb. units", 50, 0, 25);
  h_gvtx_sub_c_type_pT_jet_close_bquark_wcut = fs->make<TH1F>("h_gvtx_sub_c_type_pT_jet_close_bquark_wcut", "b-quark pT < 20 GeV w/ dR-0.4 b-quarks && w/ 1-1 matched type-c jet to b-decay; type-c jet p_{T} (GeV);arb. units", 100, 0, 200);
  h_gvtx_fake_c_type_eta_bquark_jet_wcut = fs->make<TH1F>("h_gvtx_fake_c_type_eta_bquark_jet_wcut", "b-quark pT > 20 GeV w/ 1-1 matched fake type-c jet to b-decay; |#eta| of a GEN b-quark; arb. units", 100, 0, 3.0);
  h_gvtx_fake_c_type_pT_bquark_wcut = fs->make<TH1F>("h_gvtx_fake_c_type_pT_bquark_wcut", "b-quark pT < 20 GeV w/ 1-1 matched fake type-c jet to b-decay;GEN b-quark p_{T} (GeV);arb. units", 50, 0, 25);
  h_gvtx_fake_c_type_pT_jet_wcut = fs->make<TH1F>("h_gvtx_fake_c_type_pT_jet_wcut", "b-quark pT < 20 GeV w/ 1-1 matched fake type-c jet to b-decay; a fake type-c jet p_{T} (GeV);arb. units", 100, 0, 200);
  h_gvtx_fake_c_type_nbsv_wcut = fs->make<TH1F>("h_gvtx_fake_c_type_nbsv_wcut", "b-quark pT < 20 GeV w/ 1-1 matched fake type-c jet to b-decay; # of bSVs in a fake type-c jet; arb. units", 10, 0, 10);
  h_gvtx_fake_c_type_all_ntrack_wcut = fs->make<TH1F>("h_gvtx_fake_c_type_all_ntrack_wcut", "b-quark pT < 20 GeV w/ 1-1 matched fake type-c jet to b-decay; # of all tracks in a fake type-c jet; arb. units", 10, 0, 10);
  h_gvtx_fake_c_type_seed_ntrack_wcut = fs->make<TH1F>("h_gvtx_fake_c_type_seed_ntrack_wcut", "b-quark pT < 20 GeV w/ 1-1 matched fake type-c jet to b-decay; # of seed tracks in a fake type-c jet; arb. units", 10, 0, 10);
  h_gvtx_fake_c_type_all_tracks_pt_wcut = fs->make<TH1F>("h_gvtx_fake_c_type_all_tracks_pt_wcut", "b-quark pT < 20 GeV w/ 1-1 matched fake type-c jet to b-decay;p_{T} of a track in a fake type-c jet;", 40, 0, 10);
  h_gvtx_fake_c_type_all_tracks_sigmadxybs_wcut = fs->make<TH1F>("h_gvtx_fake_c_type_all_tracks_sigmadxybs_wcut", "b-quark pT < 20 GeV w/ 1-1 matched fake type-c jet to b-decay;#sigma_{dxy} of a track in a fake type-c jet;", 40, -10, 10);
  h_gvtx_fake_c_type_diff_pT_bquark_jet_wcut = fs->make<TH1F>("h_gvtx_fake_c_type_diff_pT_bquark_jet_wcut", "b-quark pT < 20 GeV w/ 1-1 matched fake type-c jet to b-decay;p_{T} of a fake type-c jet - p_{T} of a lowpT GEN b-quark; arb. units", 60, -30.0, 30.0);
  h_gvtx_c_type_nbsv_wcut = fs->make<TH1F>("h_gvtx_c_type_nbsv_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of bSVs in a type-c jets; arb. units", 10, 0, 10);
  h_gvtx_c_type_seed_ntrack_wcut = fs->make<TH1F>("h_gvtx_c_type_seed_ntrack_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of seed tracks in a type-c jet; arb. units", 10, 0, 10);
  h_gvtx_c_type_all_ntrack_wcut = fs->make<TH1F>("h_gvtx_c_type_all_ntrack_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of all tracks in a type-c jet; arb. units", 10, 0, 10);
  h_gvtx_c_type_all_tracks_pt_wcut = fs->make<TH1F>("h_gvtx_c_type_all_tracks_pt_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;p_{T} of a track in a type-c jet;", 40, 0, 10);
  h_gvtx_c_type_all_tracks_sigmadxybs_wcut = fs->make<TH1F>("h_gvtx_c_type_all_tracks_sigmadxybs_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;#sigma_{dxy} of a track in a type-c jet;", 40, -10, 10);
  h_gvtx_d_type_dR_closest_lowpT_bquark_wcut = fs->make<TH1F>("h_gvtx_d_type_dR_closest_lowpT_bquark_wcut", "b-quark pT < 20 GeV w/ 1-1 matched type-d jet to b-decay;#Delta R between mom. of a type-d jet and a lowpT GEN b-quark; arb. units", 50, 0, 4.0);
  h_gvtx_sub_d_type_pT_bquark_wcut = fs->make<TH1F>("h_gvtx_sub_d_type_pT_bquark_wcut", "b-quark pT < 20 GeV w/ 1-1 matched type-d jet to b-decay ;GEN b-quark p_{T}(GeV);arb. units", 50, 0, 25);
  h_gvtx_sub_d_type_nbsv_wcut = fs->make<TH1F>("h_gvtx_sub_d_type_nbsv_wcut", "b-quark pT < 20 GeV w/ 1-1 matched type-d jet to b-decay; # of bSVs in a type-d jets; arb. units", 10, 0, 10);
  h_gvtx_sub_d_type_seed_ntrack_wcut = fs->make<TH1F>("h_gvtx_sub_d_type_seed_ntrack_wcut", "b-quark pT < 20 GeV w/ 1-1 matched type-d jet to b-decay; # of seed tracks in a type-d jets; arb. units", 10, 0, 10);
  h_gvtx_sub_d_type_all_tracks_pt_wcut = fs->make<TH1F>("h_gvtx_sub_d_type_all_tracks_pt_wcut", "b-quark pT < 20 GeV w/ 1-1 matched type-d jet to b-decay;p_{T} of a track in a type-d jet;", 40, 0, 10);
  h_gvtx_sub_d_type_all_tracks_sigmadxybs_wcut = fs->make<TH1F>("h_gvtx_sub_d_type_all_tracks_sigmadxybs_wcut", "b-quark pT < 20 GeV w/ 1-1 matched type-d jet to b-decay;#sigma_{dxy} of a track in a type-d jet;", 40, -10, 10);
  h_gvtx_sub_d_type_diff_pT_bquark_jet_wcut = fs->make<TH1F>("h_gvtx_sub_d_type_diff_pT_bquark_jet_wcut", "b-quark pT < 20 GeV;p_{T} of a type-d jet - p_{T} of a lowpT GEN b-quark; arb. units", 60, -30.0, 30.0);
  h_gvtx_d_type_nbsv_wcut = fs->make<TH1F>("h_gvtx_d_type_nbsv_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of bSVs in a type-d jets; arb. units", 10, 0, 10);
  h_gvtx_d_type_seed_ntrack_wcut = fs->make<TH1F>("h_gvtx_d_type_seed_ntrack_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of seed tracks in a type-d jets; arb. units", 10, 0, 10);
  h_gvtx_d_type_all_ntrack_wcut = fs->make<TH1F>("h_gvtx_d_type_all_ntrack_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of all tracks in a type-d jets; arb. units", 10, 0, 10);
  h_gvtx_d_type_all_tracks_pt_wcut = fs->make<TH1F>("h_gvtx_d_type_all_tracks_pt_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;p_{T} of a track in a type-d jet;", 40, 0, 10);
  h_gvtx_d_type_all_tracks_sigmadxybs_wcut = fs->make<TH1F>("h_gvtx_d_type_all_tracks_sigmadxybs_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;#sigma_{dxy} of a track in a type-d jet;", 40, -10, 10);

  h_gvtx_denominator_nsv_wcut = fs->make<TH1F>("h_gvtx_denominator_nsv_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of total SVs; arb. units", 10, 0, 10);
  h_2D_gvtx_ntrack_bsv_and_jet_seed_ntrack_from_bsv_wcut = fs->make<TH2F>("h_2D_gvtx_ntrack_bsv_and_jet_seed_ntrack_from_bsv_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of total tracks of this SV; # of seed tracks in the b-jet from this SV; arb. units", 20, 0, 20, 20, 0, 20);
  h_2D_gvtx_ntrack_bsv_and_jet_seed_ntrack_from_tight_trkmatch_bsv_wcut = fs->make<TH2F>("h_2D_gvtx_ntrack_bsv_and_jet_seed_ntrack_from_tight_trkmatch_bsv_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; # of total seed tracks/bSV; # of seed tracks in the b-jet from this bSV; arb. units", 20, 0, 20, 20, 0, 20);
  

  //track investigation 
  h_gvtx_all_track_pt_from_jets_wcut = fs->make<TH1F>("h_gvtx_all_track_pt_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; track p_{T} (GeV)", 20, 0, 10);
  h_gvtx_all_track_sigmadxybs_from_jets_wcut = fs->make<TH1F>("h_gvtx_all_track_sigmadxybs_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; #sigma_{dxy}", 40, -10, 10);
  h_gvtx_all_track_npxhits_from_jets_wcut = fs->make<TH1F>("h_gvtx_all_track_npxhits_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; npxhits", 12, 0, 12);
  h_gvtx_all_track_nsthits_from_jets_wcut = fs->make<TH1F>("h_gvtx_all_track_nsthits_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; nsthits", 28, 0, 28);
  h_gvtx_all_track_npxlayers_from_jets_wcut = fs->make<TH1F>("h_gvtx_all_track_npxlayers_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; npxlayers", 12, 0, 12);
  h_gvtx_all_track_nstlayers_from_jets_wcut = fs->make<TH1F>("h_gvtx_all_track_nstlayers_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; nstlayers", 28, 0, 28);
  h_gvtx_all_track_rmin_from_jets_wcut = fs->make<TH1F>("h_gvtx_all_track_rmin_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;r_{min};", 5, 0, 5);

  h_gvtx_jet_seed_nm1_pt_from_jets_wcut = fs->make<TH1F>("h_gvtx_jet_seed_nm1_pt_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; track p_{T} (GeV) w/ n-1 cuts applied", 20, 0, 10);
  h_gvtx_jet_seed_nm1_npxlayers_from_jets_wcut = fs->make<TH1F>("h_gvtx_jet_seed_nm1_npxlayers_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; npxlayers w/ n-1 cuts applied", 12, 0, 12);
  h_gvtx_jet_seed_nm1_nstlayers_from_jets_wcut = fs->make<TH1F>("h_gvtx_jet_seed_nm1_nstlayers_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; nstlayers w/ n-1 cuts applied", 28, 0, 28);
  h_gvtx_jet_seed_nm1_rmin_from_jets_wcut = fs->make<TH1F>("h_gvtx_jet_seed_nm1_rmin_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; rmin w/ n-1 cuts applied", 5, 0, 5);
  h_gvtx_jet_seed_nm1_sigmadxybs_from_jets_wcut = fs->make<TH1F>("h_gvtx_jet_seed_nm1_sigmadxybs_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay; #sigma_{dxy} w/ n-1 cuts applied", 40, -10, 10);

  h_gvtx_one_cut_ntrack_from_jets_wcut = fs->make<TH1F>("h_gvtx_one_cut_ntrack_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;# of 1-cut seed tracks per a matched jet;", 50, 0, 50);
  h_gvtx_one_cut_track_pT_from_jets_wcut = fs->make<TH1F>("h_gvtx_one_cut_track_pT_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;p_{T} of a 1-cut seed track in a matched jet;", 20, 0, 10);
  h_gvtx_one_cut_track_sigmadxybs_from_jets_wcut = fs->make<TH1F>("h_gvtx_one_cut_track_sigmadxybs_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;#sigma_{dxy} of a 1-cut seed track in a matched jet;", 40, -10, 10);
  h_gvtx_one_cut_track_npxlayers_from_jets_wcut = fs->make<TH1F>("h_gvtx_one_cut_track_npxlayers_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;npxlayers of a 1-cut seed track in a matched jet;", 12, 0, 12);
  h_gvtx_one_cut_track_nstlayers_from_jets_wcut = fs->make<TH1F>("h_gvtx_one_cut_track_nstlayers_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;nstlayers of a 1-cut seed track in a matched jet;", 28, 0, 28);
  h_gvtx_one_cut_track_rmin_from_jets_wcut = fs->make<TH1F>("h_gvtx_one_cut_track_rmin_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;r_{min} of a 1-cut seed track in a matched jet;", 5, 0, 5);

  h_gvtx_two_cut_ntrack_from_jets_wcut = fs->make<TH1F>("h_gvtx_two_cut_ntrack_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;# of 2-cut seed tracks per a matched jet;", 50, 0, 50);
  h_gvtx_two_cut_track_pT_from_jets_wcut = fs->make<TH1F>("h_gvtx_two_cut_track_pT_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;p_{T} of a 2-cut seed track in a matched jet;", 20, 0, 10);
  h_gvtx_two_cut_track_sigmadxybs_from_jets_wcut = fs->make<TH1F>("h_gvtx_two_cut_track_sigmadxybs_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;#sigma_{dxy} of a 2-cut seed track in a matched jet;", 40, -10, 10);
  h_gvtx_two_cut_track_npxlayers_from_jets_wcut = fs->make<TH1F>("h_gvtx_two_cut_track_npxlayers_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;npxlayers of a 2-cut seed track in a matched jet;", 12, 0, 12);
  h_gvtx_two_cut_track_nstlayers_from_jets_wcut = fs->make<TH1F>("h_gvtx_two_cut_track_nstlayers_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;nstlayers of a 2-cut seed track in a matched jet;", 28, 0, 28);
  h_gvtx_two_cut_track_rmin_from_jets_wcut = fs->make<TH1F>("h_gvtx_two_cut_track_rmin_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;r_{min} of a 2-cut seed track in a matched jet;", 5, 0, 5);

  h_gvtx_three_cut_ntrack_from_jets_wcut = fs->make<TH1F>("h_gvtx_three_cut_ntrack_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;# of 3-cut seed tracks per a matched jet;", 50, 0, 50);
  h_gvtx_three_cut_track_pT_from_jets_wcut = fs->make<TH1F>("h_gvtx_three_cut_track_pT_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;p_{T} of a 3-cut seed track in a matched jet;", 20, 0, 10);
  h_gvtx_three_cut_track_sigmadxybs_from_jets_wcut = fs->make<TH1F>("h_gvtx_three_cut_track_sigmadxybs_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;#sigma_{dxy} of a 3-cut seed track in a matched jet;", 40, -10, 10);
  h_gvtx_three_cut_track_npxlayers_from_jets_wcut = fs->make<TH1F>("h_gvtx_three_cut_track_npxlayers_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;npxlayers of a 3-cut seed track in a matched jet;", 12, 0, 12);
  h_gvtx_three_cut_track_nstlayers_from_jets_wcut = fs->make<TH1F>("h_gvtx_three_cut_track_nstlayers_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;nstlayers of a 3-cut seed track in a matched jet;", 28, 0, 28);
  h_gvtx_three_cut_track_rmin_from_jets_wcut = fs->make<TH1F>("h_gvtx_three_cut_track_rmin_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;r_{min} of a 3-cut seed track in a matched jet;", 5, 0, 5);

  h_gvtx_four_cut_ntrack_from_jets_wcut = fs->make<TH1F>("h_gvtx_four_cut_ntrack_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;# of 4-cut seed tracks per a matched jet;", 50, 0, 50);
  h_gvtx_four_cut_track_pT_from_jets_wcut = fs->make<TH1F>("h_gvtx_four_cut_track_pT_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;p_{T} of a 4-cut seed track in a matched jet;", 20, 0, 10);
  h_gvtx_four_cut_track_sigmadxybs_from_jets_wcut = fs->make<TH1F>("h_gvtx_four_cut_track_sigmadxybs_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;#sigma_{dxy} of a 4-cut seed track in a matched jet;", 40, -10, 10);
  h_gvtx_four_cut_track_npxlayers_from_jets_wcut = fs->make<TH1F>("h_gvtx_four_cut_track_npxlayers_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;npxlayers of a 4-cut seed track in a matched jet;", 12, 0, 12);
  h_gvtx_four_cut_track_nstlayers_from_jets_wcut = fs->make<TH1F>("h_gvtx_four_cut_track_nstlayers_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;nstlayers of a 4-cut seed track in a matched jet;", 28, 0, 28);
  h_gvtx_four_cut_track_rmin_from_jets_wcut = fs->make<TH1F>("h_gvtx_four_cut_track_rmin_from_jets_wcut", "b-quark pT > 20 GeV w/ 1-1 matched jet to b-decay;r_{min} of a 4-cut seed track in a matched jet;", 5, 0, 5);

  
 

  h_minlspdist2d = fs->make<TH1F>("h_minlspdist2d", ";min dist2d(gen vtx #i) (cm);events/0.1 mm", 200, 0, 2);
  h_lspdist2d = fs->make<TH1F>("h_lspdist2d", ";dist2d(gen vtx #0, #1) (cm);events/0.1 mm", 200, 0, 2);
  h_lspdist3d = fs->make<TH1F>("h_lspdist3d", ";dist3d(gen vtx #0, #1) (cm);events/0.1 mm", 200, 0, 2);

  h_hlt_bits = fs->make<TH1F>("h_hlt_bits", ";;events", 2*mfv::n_hlt_paths+1, 0, 2*mfv::n_hlt_paths+1);
  h_l1_bits  = fs->make<TH1F>("h_l1_bits",  ";;events", 2*mfv::n_l1_paths +1, 0, 2*mfv::n_l1_paths +1);
  //h_filter_bits  = fs->make<TH1F>("h_filter_bits",  ";;events", 2*mfv::n_filter_paths +1, 0, 2*mfv::n_filter_paths +1);
  h_filter_bits  = fs->make<TH1F>("h_filter_bits",  ";;events", mfv::n_filter_paths +1, 0, mfv::n_filter_paths +1);

  h_hlt_bits->GetXaxis()->SetBinLabel(1, "nevents");
  for (int i = 0; i < mfv::n_hlt_paths; ++i) {
    h_hlt_bits->GetXaxis()->SetBinLabel(1+2*i+1, TString::Format("found %s", mfv::hlt_paths[i]));
    h_hlt_bits->GetXaxis()->SetBinLabel(1+2*i+2, TString::Format(" pass %s", mfv::hlt_paths[i]));
  }
  h_l1_bits->GetXaxis()->SetBinLabel(1, "nevents");
  for (int i = 0; i < mfv::n_l1_paths; ++i) {
    h_l1_bits->GetXaxis()->SetBinLabel(1+2*i+1, TString::Format("found %s", mfv::l1_paths[i]));
    h_l1_bits->GetXaxis()->SetBinLabel(1+2*i+2, TString::Format(" pass %s", mfv::l1_paths[i]));
  }

  h_filter_bits->GetXaxis()->SetBinLabel(1, "nevents");
  for (int i = 0; i < mfv::n_filter_paths; ++i) {
    h_filter_bits->GetXaxis()->SetBinLabel(i+2, TString::Format(" pass %s", mfv::filter_paths[i]));
  }

  h_npu = fs->make<TH1F>("h_npu", ";true nPU;events", 120, 0, 120);

  h_bsx = fs->make<TH1F>("h_bsx", ";beamspot x (cm);events/10 #mum", 200, -0.1, 0.1);
  h_bsy = fs->make<TH1F>("h_bsy", ";beamspot y (cm);events/10 #mum", 200, -0.1, 0.1);
  h_bsz = fs->make<TH1F>("h_bsz", ";beamspot z (cm);events/400 #mum", 200, -4, 4);
  h_bsphi = fs->make<TH1F>("h_bsphi", ";beamspot #phi (rad);events/.063", 100, -3.1416, 3.1416);

  h_npv = fs->make<TH1F>("h_npv", ";# of primary vertices;events", 120, 0, 120);
  h_pvx = fs->make<TH1F>("h_pvx", ";primary vertex x (cm);events/2 #mum", 200, -0.02, 0.02);
  h_pvy = fs->make<TH1F>("h_pvy", ";primary vertex y (cm);events/2 #mum", 200, -0.02, 0.02);
  h_pvxwide = fs->make<TH1F>("h_pvxwide", ";primary vertex x (cm);events/40 #mum", 50, -0.1, 0.1);
  h_pvywide = fs->make<TH1F>("h_pvywide", ";primary vertex y (cm);events/40 #mum", 50, -0.1, 0.1);
  h_pvz = fs->make<TH1F>("h_pvz", ";primary vertex z (cm);events/3.6 mm", 100, -18, 18);
  h_pvcxx = fs->make<TH1F>("h_pvcxx", ";primary vertex cxx;events", 100, 0, 5e-6);
  h_pvcyy = fs->make<TH1F>("h_pvcyy", ";primary vertex cyy;events", 100, 0, 5e-6);
  h_pvczz = fs->make<TH1F>("h_pvczz", ";primary vertex czz;events", 100, 0, 1e-5);
  h_pvcxy = fs->make<TH1F>("h_pvcxy", ";primary vertex cxy;events", 100, -1e-6, 1e-6);
  h_pvcxz = fs->make<TH1F>("h_pvcxz", ";primary vertex cxz;events", 100, -1e-6, 1e-6);
  h_pvcyz = fs->make<TH1F>("h_pvcyz", ";primary vertex cyz;events", 100, -1e-6, 1e-6);
  h_pvrho = fs->make<TH1F>("h_pvrho", ";primary vertex rho (cm);events/5 #mum", 40, 0, 0.02);
  h_pvrhowide = fs->make<TH1F>("h_pvrhowide", ";primary vertex rho (cm);events/10 #mum", 100, 0, 0.1);
  h_pvphi = fs->make<TH1F>("h_pvphi", ";primary vertex #phi (rad);events/.063", 100, -3.1416, 3.1416);
  h_pvntracks = fs->make<TH1F>("h_pvntracks", ";# of tracks in primary vertex;events/3", 100, 0, 300);
  h_pvscore = fs->make<TH1F>("h_pvscore", ";primary vertex #Sigma p_{T}^{2} (GeV^{2});events/10000 GeV^{2}", 100, 0, 1e6);
  h_pvsx = fs->make<TH1F>("h_pvsx", ";primary vertices x (cm);events/2 #mum", 200, -0.02, 0.02);
  h_pvsy = fs->make<TH1F>("h_pvsy", ";primary vertices y (cm);events/2 #mum", 200, -0.02, 0.02);
  h_pvsxwide = fs->make<TH1F>("h_pvsxwide", ";primary vertices x (cm);events/40 #mum", 50, -0.1, 0.1);
  h_pvsywide = fs->make<TH1F>("h_pvsywide", ";primary vertices y (cm);events/40 #mum", 50, -0.1, 0.1);
  h_pvsz = fs->make<TH1F>("h_pvsz", ";primary vertices z (cm);events/3.6 mm", 100, -18, 18);
  h_pvsrho = fs->make<TH1F>("h_pvsrho", ";primary vertices rho (cm);events/5 #mum", 40, 0, 0.02);
  h_pvsrhowide = fs->make<TH1F>("h_pvsrhowide", ";primary vertices rho (cm);events/10 #mum", 100, 0, 0.1);
  h_pvsphi = fs->make<TH1F>("h_pvsphi", ";primary vertices #phi (rad);events/.063", 100, -3.1416, 3.1416);
  h_pvsscore = fs->make<TH1F>("h_pvsscore", ";primary vertices #Sigma p_{T}^{2} (GeV^{2});events/10000 GeV^{2}", 100, 0, 1e6);
  h_pvsdz = fs->make<TH1F>("h_pvsdz", ";primary vertices pairs #delta z (cm);events/2 mm", 100, 0, 20);
  h_pvsmindz = fs->make<TH1F>("h_pvsmindz", ";min primary vertices pairs #delta z (cm);events/0.5 mm", 100, 0, 5);
  h_pvsmaxdz = fs->make<TH1F>("h_pvmaxdz", ";max primary vertices pairs #delta z (cm);events/2 mm", 100, 0, 20);
  h_pvsmindz_minscore = fs->make<TH1F>("h_pvmindz_minscore", ";min primary vertices pairs (with score req) #delta z (cm);events/1 mm", 100, 0, 10);
  h_pvsmaxdz_minscore = fs->make<TH1F>("h_pvmaxdz_minscore", ";max primary vertices pairs (with score req) #delta z (cm);events/1 mm", 100, 0, 10);

  h_njets = fs->make<TH1F>("h_njets", ";# of jets;events", 30, 0, 30);
  h_njets20 = fs->make<TH1F>("h_njets20", ";# of jets w. p_{T} > 20 GeV;events", 20, 0, 20);
  for (int i = 0; i < MAX_NJETS+1; ++i) {
    TString ijet = i == MAX_NJETS ? TString("all") : TString::Format("%i", i);
    h_jet_pt[i] = fs->make<TH1F>(TString::Format("h_jet_pt_%s", ijet.Data()), TString::Format(";p_{T} of jet #%s (GeV);events/10 GeV", ijet.Data()), 200, 0, 2000);
    h_jet_eta[i] = fs->make<TH1F>(TString::Format("h_jet_eta_%s", ijet.Data()), TString::Format(";#eta of jet #%s (GeV);events/0.05", ijet.Data()), 120, -3, 3);
    h_jet_phi[i] = fs->make<TH1F>(TString::Format("h_jet_phi_%s", ijet.Data()), TString::Format(";#phi of jet #%s (GeV);events/0.063", ijet.Data()), 100, -3.1416, 3.1416);
  }
  h_jet_energy = fs->make<TH1F>("h_jet_energy", ";jets energy (GeV);jets/10 GeV", 200, 0, 2000);
  h_jet_ht = fs->make<TH1F>("h_jet_ht", ";H_{T} of jets (GeV);events/25 GeV", 200, 0, 5000);
  h_jet_ht_40 = fs->make<TH1F>("h_jet_ht_40", ";H_{T} of jets with p_{T} > 40 GeV;events/25 GeV", 200, 0, 5000);

  h_jet_pairdphi = fs->make<TH1F>("h_jet_pairdphi", ";jet pair #Delta#phi (rad);jet pairs/.063", 100, -3.1416, 3.1416);
  h_jet_pairdeta = fs->make<TH1F>("h_jet_pairdeta", ";jet pair #Delta#eta ;jet pairs/.1", 100, -5.0, 5.0);
  h_jet_pairdr = fs->make<TH1F>("h_jet_pairdr", ";jet pair #DeltaR (rad);jet pairs/.063", 100, 0, 6.3);

  h_n_vertex_seed_tracks = fs->make<TH1F>("h_n_vertex_seed_tracks", ";# vertex seed tracks;events", 100, 0, 100);
  h_vertex_seed_track_chi2dof = fs->make<TH1F>("h_vertex_seed_track_chi2dof", ";vertex seed track #chi^{2}/dof;tracks/1", 10, 0, 10);
  h_vertex_seed_track_q = fs->make<TH1F>("h_vertex_seed_track_q", ";vertex seed track charge;tracks", 3, -1, 2);
  h_vertex_seed_track_pt = fs->make<TH1F>("h_vertex_seed_track_pt", ";vertex seed track p_{T} (GeV);tracks/GeV", 300, 0, 300);
  h_vertex_seed_track_eta = fs->make<TH1F>("h_vertex_seed_track_eta", ";vertex seed track #eta;tracks/0.052", 100, -2.6, 2.6);
  h_vertex_seed_track_phi = fs->make<TH1F>("h_vertex_seed_track_phi", ";vertex seed track #phi;tracks/0.063", 100, -3.15, 3.15);
  h_vertex_seed_track_phi_v_eta = fs->make<TH2F>("h_vertex_seed_track_phi_v_eta", ";vertex seed track #eta;vertex seed track #phi", 26, -2.6, 2.6, 24, -M_PI, M_PI);
  h_vertex_seed_track_dxy = fs->make<TH1F>("h_vertex_seed_track_dxy", ";vertex seed track dxy (cm);tracks/10 #mum", 200, -0.1, 0.1);
  h_vertex_seed_track_dz = fs->make<TH1F>("h_vertex_seed_track_dz", ";vertex seed track dz (cm);tracks/10 #mum", 200, -0.1, 0.1);
  h_vertex_seed_track_err_pt = fs->make<TH1F>("h_vertex_seed_track_err_pt", ";vertex seed track #sigma(p_{T})/p_{T} (GeV);tracks/0.005", 100, 0, 0.5);
  h_vertex_seed_track_err_eta = fs->make<TH1F>("h_vertex_seed_track_err_eta", ";vertex seed track #sigma(#eta);tracks/5e-5", 100, 0, 0.005);
  h_vertex_seed_track_err_phi = fs->make<TH1F>("h_vertex_seed_track_err_phi", ";vertex seed track #sigma(#phi);tracks/5e-5", 100, 0, 0.005);
  h_vertex_seed_track_err_dxy = fs->make<TH1F>("h_vertex_seed_track_err_dxy", ";vertex seed track #sigma(dxy) (cm);tracks/3 #mum", 100, 0, 0.03);
  h_vertex_seed_track_err_dz = fs->make<TH1F>("h_vertex_seed_track_err_dz", ";vertex seed track #sigma(dz) (cm);tracks/15 #mum", 100, 0, 0.15);
  h_vertex_seed_track_npxhits = fs->make<TH1F>("h_vertex_seed_track_npxhits", ";vertex seed track # pixel hits;tracks", 10, 0, 10);
  h_vertex_seed_track_nsthits = fs->make<TH1F>("h_vertex_seed_track_nsthits", ";vertex seed track # strip hits;tracks", 50, 0, 50);
  h_vertex_seed_track_nhits = fs->make<TH1F>("h_vertex_seed_track_nhits", ";vertex seed track # hits;tracks", 60, 0, 60);
  h_vertex_seed_track_npxlayers = fs->make<TH1F>("h_vertex_seed_track_npxlayers", ";vertex seed track # pixel layers;tracks", 10, 0, 10);
  h_vertex_seed_track_nstlayers = fs->make<TH1F>("h_vertex_seed_track_nstlayers", ";vertex seed track # strip layers;tracks", 20, 0, 20);
  h_vertex_seed_track_nlayers = fs->make<TH1F>("h_vertex_seed_track_nlayers", ";vertex seed track # layers;tracks", 30, 0, 30);

  h_met = fs->make<TH1F>("h_met", ";MET (GeV);events/5 GeV", 100, 0, 500);
  h_metphi = fs->make<TH1F>("h_metphi", ";MET #phi (rad);events/.063", 100, -3.1416, 3.1416);

  const char* lmt_ex[3] = {"loose", "medium", "tight"};
  const char* lep_kind[2] = {"muon", "electron"};
  for (int i = 0; i < 3; ++i) {
    h_nbtags[i] = fs->make<TH1F>(TString::Format("h_nbtags_%i", i), TString::Format(";# of %s b tags;events", lmt_ex[i]), 10, 0, 10);
    h_nbtags_v_bquark_code[i] = fs->make<TH2F>(TString::Format("h_nbtags_v_bquark_code_%i", i), TString::Format(";bquark code;# of %s b tags", lmt_ex[i]), 3, 0, 3, 3, 0, 3);
  }
  h_jet_bdisc = fs->make<TH1F>("h_jet_bdisc", ";jets' b discriminator;jets/0.02", 51, 0, 1.02);
  h_jet_bdisc_v_bquark_code = fs->make<TH2F>("h_jet_bdisc_v_bquark_code", ";b quark code;jets' b discriminator", 3, 0, 3, 51, 0, 1.02);
  h_bjet_pt = fs->make<TH1F>("h_bjet_pt", ";bjets p_{T} (GeV);bjets/10 GeV", 150, 0, 1500);
  h_bjet_eta = fs->make<TH1F>("h_bjet_eta", ";bjets #eta (rad);bjets/.05", 120, -3, 3);
  h_bjet_phi = fs->make<TH1F>("h_bjet_phi", ";bjets #phi (rad);bjets/.063", 100, -3.1416, 3.1416);
  h_bjet_energy = fs->make<TH1F>("h_bjet_energy", ";bjets E (GeV);bjets/10 GeV", 150, 0, 1500);
  h_bjet_pairdphi = fs->make<TH1F>("h_bjet_pairdphi", ";bjet pair #Delta#phi (rad);bjet pairs/.063", 100, -3.1416, 3.1416);
  h_bjet_pairdeta = fs->make<TH1F>("h_bjet_pairdeta", ";bjet pair #Delta#eta;bjet pairs/.1", 100, -5.0, 5.0);

  const char* lep_ex[2] = {"any", "selected"};
  for (int i = 0; i < 2; ++i) {
    h_nmuons[i] = fs->make<TH1F>(TString::Format("h_nmuons_%s", lep_ex[i]), TString::Format(";# of %s muons;events", lep_ex[i]), 5, 0, 5);
    h_nelectrons[i] = fs->make<TH1F>(TString::Format("h_nelectrons_%s", lep_ex[i]), TString::Format(";# of %s electrons;events", lep_ex[i]), 5, 0, 5);
    h_nleptons[i] = fs->make<TH1F>(TString::Format("h_nleptons_%s", lep_ex[i]), TString::Format(";# of %s leptons;events", lep_ex[i]), 5, 0, 5);
    for (int j = 0; j < 2; ++j) {
      h_leptons_pt   [j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_pt",    lep_kind[j], lep_ex[i]), TString::Format(";%s %s p_{T} (GeV);%ss/5 GeV",     lep_ex[i], lep_kind[j], lep_kind[j]), 40, 0, 200);
      h_leptons_eta  [j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_eta",   lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #eta (rad);%ss/.104",      lep_ex[i], lep_kind[j], lep_kind[j]), 50, -2.6, 2.6);
      h_leptons_phi  [j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_phi",   lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #phi (rad);%ss/.126",      lep_ex[i], lep_kind[j], lep_kind[j]), 50, -3.1416, 3.1416);
      h_leptons_dxy  [j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_dxy",   lep_kind[j], lep_ex[i]), TString::Format(";%s %ss dxy(PV) (cm);%ss/50 #mum", lep_ex[i], lep_kind[j], lep_kind[j]), 200, -0.5, 0.5);
      h_leptons_dxybs[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_dxybs", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss dxy(BS) (cm);%ss/50 #mum", lep_ex[i], lep_kind[j], lep_kind[j]), 200, -0.5, 0.5);
      h_leptons_dz   [j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_dz",   lep_kind[j], lep_ex[i]), TString::Format(";%s %ss dz (cm);%ss/50 #mum",       lep_ex[i], lep_kind[j], lep_kind[j]), 200, -0.5, 0.5);
      h_leptons_iso  [j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso",   lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%ss/.04",       lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    }
  }
}

void MFVEventHistos::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<MFVEvent> mevent;
  event.getByToken(mevent_token, mevent);

  edm::Handle<MFVVertexAuxCollection> auxes;
  event.getByToken(vertex_token, auxes);

  
  const int nsv = int(auxes->size());

  edm::Handle<double> weight;
  event.getByToken(weight_token, weight);
  const double w = *weight;
  h_w->Fill(w);

  h_nsv->Fill(nsv, w);
  //////////////////////////////////////////////////////////////////////////////

  h_gen_decay->Fill(mevent->gen_decay_type[0], mevent->gen_decay_type[1], w);
  h_gen_flavor_code->Fill(mevent->gen_flavor_code, w);

  const size_t nbquarks = mevent->gen_bquarks.size();
  h_nbquarks->Fill(nbquarks, w);
  for (size_t i = 0; i < nbquarks; ++i) {
    h_bquark_pt->Fill(mevent->gen_bquarks[i].Pt(), w);
    h_bquark_eta->Fill(mevent->gen_bquarks[i].Eta(), w);
    h_bquark_phi->Fill(mevent->gen_bquarks[i].Phi(), w);
    h_bquark_energy->Fill(mevent->gen_bquarks[i].E(), w);
    for (size_t j = i+1; j < nbquarks; ++j) {
      h_bquark_pairdphi->Fill(reco::deltaPhi(mevent->gen_bquarks[i].Phi(), mevent->gen_bquarks[j].Phi()), w);
      h_bquark_pairdeta->Fill(std::max(mevent->gen_bquarks[i].Eta(), mevent->gen_bquarks[j].Eta()) - std::min(mevent->gen_bquarks[i].Eta(),  mevent->gen_bquarks[j].Eta()), w);
    }
  }

  // overview before studies 
  h_n_gen_bvtx->Fill(int((mevent->gen_b_llp0_decay.size()+ mevent->gen_b_llp1_decay.size())/3), w);
  
  
  
	  
  if (mevent->gen_bchain_nonb_had_eta.size() == 4) {

	  for (int isv = 0; isv < nsv; ++isv) {

		  const MFVVertexAux& aux = auxes->at(isv);
		  h_gvtx_sv_ntrack->Fill(aux.ntracks(), w);
	  }

	  if (nsv > 0) {
		  h_gvtx_nsv->Fill(nsv, w);
		  h_gvtx_njet->Fill(mevent->njets(20), w);
		  h_gvtx_sanity_njet->Fill(mevent->jet_id.size(), w);
		  for (int i = 0; i < 3; ++i) {
			  h_nbtags[i]->Fill(mevent->nbtags(i), w);
			  h_nbtags_v_bquark_code[i]->Fill(mevent->gen_flavor_code, mevent->nbtags(i), w);
		  }


		  size_t shared_bjet = 0;
		  bool match_jet_event = false;
		  bool all_bboost = true;
		  std::vector<size_t> vec_lowpT_bquark = {};
		  std::vector<size_t> vec_ibjet = {};
		  std::vector<int> vec_ibsv = {};
		  std::vector<int> vec_tight_trk_ibsv = {};
		  size_t sum_nbsv_by_bjet = 0;
		  std::vector<size_t> vec_bquark_jet = {};
		  std::vector<size_t> vec_bquark = {};

		  size_t nloosebsvjet = 0;
		  size_t nloosebsvplusbtaggedjet = 0;

		  
		  for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
			  if (mevent->jet_pt[ijet] < 0.0)  // Jets have a cut at 20 GeV
				  continue;
			  
			  std::vector<size_t> vec_bsvjet_isv = {};
			  size_t jet_seed_ntrack_in_bsvjet = 0;
			  for (size_t j = 0; j < mevent->jet_track_which_jet.size(); ++j) {
				  if (ijet == mevent->jet_track_which_jet[j]) {
					  if (mevent->jet_track_npxlayers(j) > 1 && mevent->jet_track_nstlayers(j) > 5 && mevent->jet_track_pt(j) > 1 && fabs(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j]) > 4 && mevent->jet_track_hp_rmin[j] == 1) {
						  jet_seed_ntrack_in_bsvjet++;
						  for (int isv = 0; isv < nsv; ++isv) {

							  const MFVVertexAux& aux = auxes->at(isv);

							  for (int itk = 0; itk < aux.ntracks(); ++itk) {


								  if (fabs(aux.track_pt(itk) - fabs(mevent->jet_track_qpt[j])) < 0.0001 &&
									  fabs(aux.track_eta[itk] - mevent->jet_track_eta[j]) < 0.0001 &&
									  fabs(aux.track_phi[itk] - mevent->jet_track_phi[j]) < 0.0001) {
									  vec_bsvjet_isv.push_back(isv);
								  }
							  }

						  }
					  }


				  }
			  }

			  int nbsv_by_bsvjet_jet = 0;
			  
			  for (int isv = 0; isv < nsv; ++isv) {
				  int jet_seed_ntrack_from_tight_trk_bsv = std::count(vec_bsvjet_isv.begin(), vec_bsvjet_isv.end(), isv);
				  if (jet_seed_ntrack_from_tight_trk_bsv >= 2) {
					  nbsv_by_bsvjet_jet++;
				  }

			  }
			  if (nbsv_by_bsvjet_jet >= 1) {
				  nloosebsvjet++;
				  if (jet_seed_ntrack_in_bsvjet > 0)
					  h_gvtx_jet_seed_ntrack_per_loose_bsv_jet_wcut->Fill(jet_seed_ntrack_in_bsvjet, w);
				  h_gvtx_tight_trkmatch_nbsv_per_loose_bsv_jet_wcut->Fill(nbsv_by_bsvjet_jet, w);
			  }
			  else {
				  if (jet_seed_ntrack_in_bsvjet > 0)
					  h_gvtx_jet_seed_ntrack_per_non_loose_bsv_jet_wcut->Fill(jet_seed_ntrack_in_bsvjet, w);
				  h_gvtx_tight_trkmatch_nbsv_per_non_loose_bsv_jet_wcut->Fill(nbsv_by_bsvjet_jet, w);
			  }

			  if (nbsv_by_bsvjet_jet >= 1 || mevent->is_btagged(ijet, 0)) {
				  nloosebsvplusbtaggedjet++;
				  if (jet_seed_ntrack_in_bsvjet > 0)
					  h_gvtx_jet_seed_ntrack_per_loose_bsv_plus_btagged_jet_wcut->Fill(jet_seed_ntrack_in_bsvjet, w);
				  h_gvtx_tight_trkmatch_nbsv_per_loose_bsv_plus_btagged_jet_wcut->Fill(nbsv_by_bsvjet_jet, w);
			  }
			  else {
				  if (jet_seed_ntrack_in_bsvjet > 0)
					  h_gvtx_jet_seed_ntrack_per_non_loose_bsv_plus_btagged_jet_wcut->Fill(jet_seed_ntrack_in_bsvjet, w);
				  h_gvtx_tight_trkmatch_nbsv_per_non_loose_bsv_plus_btagged_jet_wcut->Fill(nbsv_by_bsvjet_jet, w);
			  }


			  if (mevent->is_btagged(ijet, 0)) {
				  std::vector<size_t> vec_btag0_isv = {};

				  size_t jet_seed_ntrack = 0;
				  for (size_t j = 0; j < mevent->jet_track_which_jet.size(); ++j) {
					  if (ijet == mevent->jet_track_which_jet[j]) {
						  if (mevent->jet_track_npxlayers(j) > 1 && mevent->jet_track_nstlayers(j) > 5 && mevent->jet_track_pt(j) > 1 && fabs(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j]) > 4 && mevent->jet_track_hp_rmin[j] == 1) {
							  jet_seed_ntrack++; 
							  for (int isv = 0; isv < nsv; ++isv) {

								  const MFVVertexAux& aux = auxes->at(isv);

								  for (int itk = 0; itk < aux.ntracks(); ++itk) {


									  if (fabs(aux.track_pt(itk) - fabs(mevent->jet_track_qpt[j])) < 0.0001 &&
										  fabs(aux.track_eta[itk] - mevent->jet_track_eta[j]) < 0.0001 &&
										  fabs(aux.track_phi[itk] - mevent->jet_track_phi[j]) < 0.0001) {
										  vec_btag0_isv.push_back(isv);
									  }
								  }

							  }
						  }


					  }
				  }


				  int nbsv_by_btag0_jet = 0;
				  
				  for (int isv = 0; isv < nsv; ++isv) {
					  const MFVVertexAux& aux = auxes->at(isv);
					  int jet_seed_ntrack_from_tight_trk_bsv = std::count(vec_btag0_isv.begin(), vec_btag0_isv.end(), isv);
					  if (jet_seed_ntrack_from_tight_trk_bsv == aux.ntracks()) {
						  nbsv_by_btag0_jet++;
					  }
					  else
						  continue;

				  }
				  if (jet_seed_ntrack > 0)
						h_gvtx_jet_seed_ntrack_per_loose_btag_wcut->Fill(jet_seed_ntrack, w);
				  h_gvtx_tight_trkmatch_nbsv_per_loose_btag_jet_wcut->Fill(nbsv_by_btag0_jet, w);
			  }
			  else {
				  
				  std::vector<size_t> vec_non_btag0_isv = {};
				  size_t jet_seed_ntrack = 0;
				  for (size_t j = 0; j < mevent->jet_track_which_jet.size(); ++j) {
					  if (ijet == mevent->jet_track_which_jet[j]) {
						  if (mevent->jet_track_npxlayers(j) > 1 && mevent->jet_track_nstlayers(j) > 5 && mevent->jet_track_pt(j) > 1 && fabs(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j]) > 4 && mevent->jet_track_hp_rmin[j] == 1) {
							  jet_seed_ntrack ++;
							  for (int isv = 0; isv < nsv; ++isv) {

								  const MFVVertexAux& aux = auxes->at(isv);

								  for (int itk = 0; itk < aux.ntracks(); ++itk) {


									  if (fabs(aux.track_pt(itk) - fabs(mevent->jet_track_qpt[j])) < 0.0001 &&
										  fabs(aux.track_eta[itk] - mevent->jet_track_eta[j]) < 0.0001 &&
										  fabs(aux.track_phi[itk] - mevent->jet_track_phi[j]) < 0.0001) {
										  vec_non_btag0_isv.push_back(isv);
									  }
								  }

							  }
						  }


					  }
				  }


				  int nbsv_by_non_btag0_jet = 0;
				  for (int isv = 0; isv < nsv; ++isv) {
					  const MFVVertexAux& aux = auxes->at(isv);
					  int jet_seed_ntrack_from_tight_trk_bsv = std::count(vec_non_btag0_isv.begin(), vec_non_btag0_isv.end(), isv);
					  if (jet_seed_ntrack_from_tight_trk_bsv == aux.ntracks()) {
						  nbsv_by_non_btag0_jet++;
					  }
					  else
						  continue;

				  }
				  if (jet_seed_ntrack > 0)
						h_gvtx_jet_seed_ntrack_per_non_loose_btag_wcut->Fill(jet_seed_ntrack, w);
				  h_gvtx_tight_trkmatch_nbsv_per_non_loose_btag_jet_wcut->Fill(nbsv_by_non_btag0_jet, w);
			  }

			  if (mevent->is_btagged(ijet, 1)) {
				  std::vector<size_t> vec_btag1_isv = {};
				  size_t jet_seed_ntrack = 0;
				  for (size_t j = 0; j < mevent->jet_track_which_jet.size(); ++j) {
					  if (ijet == mevent->jet_track_which_jet[j]) {
						  if (mevent->jet_track_npxlayers(j) > 1 && mevent->jet_track_nstlayers(j) > 5 && mevent->jet_track_pt(j) > 1 && fabs(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j]) > 4 && mevent->jet_track_hp_rmin[j] == 1) {
							  jet_seed_ntrack++;
							  for (int isv = 0; isv < nsv; ++isv) {

								  const MFVVertexAux& aux = auxes->at(isv);

								  for (int itk = 0; itk < aux.ntracks(); ++itk) {


									  if (fabs(aux.track_pt(itk) - fabs(mevent->jet_track_qpt[j])) < 0.0001 &&
										  fabs(aux.track_eta[itk] - mevent->jet_track_eta[j]) < 0.0001 &&
										  fabs(aux.track_phi[itk] - mevent->jet_track_phi[j]) < 0.0001) {
										  vec_btag1_isv.push_back(isv);
									  }
								  }

							  }
						  }


					  }
				  }


				  int nbsv_by_btag1_jet = 0;
				  for (int isv = 0; isv < nsv; ++isv) {
					  const MFVVertexAux& aux = auxes->at(isv);
					  int jet_seed_ntrack_from_tight_trk_bsv = std::count(vec_btag1_isv.begin(), vec_btag1_isv.end(), isv);
					  if (jet_seed_ntrack_from_tight_trk_bsv == aux.ntracks()) {
						  nbsv_by_btag1_jet++;
					  }
					  else
						  continue;

				  }
				  if (jet_seed_ntrack > 0)
						h_gvtx_jet_seed_ntrack_per_medium_btag_wcut->Fill(jet_seed_ntrack, w);
				  h_gvtx_tight_trkmatch_nbsv_per_medium_btag_jet_wcut->Fill(nbsv_by_btag1_jet, w);
			  }
			  else {

				  std::vector<size_t> vec_non_btag1_isv = {};
				  size_t jet_seed_ntrack = 0;
				  for (size_t j = 0; j < mevent->jet_track_which_jet.size(); ++j) {
					  if (ijet == mevent->jet_track_which_jet[j]) {
						  if (mevent->jet_track_npxlayers(j) > 1 && mevent->jet_track_nstlayers(j) > 5 && mevent->jet_track_pt(j) > 1 && fabs(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j]) > 4 && mevent->jet_track_hp_rmin[j] == 1) {
							  jet_seed_ntrack ++;
							  for (int isv = 0; isv < nsv; ++isv) {

								  const MFVVertexAux& aux = auxes->at(isv);

								  for (int itk = 0; itk < aux.ntracks(); ++itk) {


									  if (fabs(aux.track_pt(itk) - fabs(mevent->jet_track_qpt[j])) < 0.0001 &&
										  fabs(aux.track_eta[itk] - mevent->jet_track_eta[j]) < 0.0001 &&
										  fabs(aux.track_phi[itk] - mevent->jet_track_phi[j]) < 0.0001) {
										  vec_non_btag1_isv.push_back(isv);
									  }
								  }

							  }
						  }


					  }
				  }


				  int nbsv_by_non_btag1_jet = 0;
				  for (int isv = 0; isv < nsv; ++isv) {
					  const MFVVertexAux& aux = auxes->at(isv);
					  int jet_seed_ntrack_from_tight_trk_bsv = std::count(vec_non_btag1_isv.begin(), vec_non_btag1_isv.end(), isv);
					  if (jet_seed_ntrack_from_tight_trk_bsv == aux.ntracks()) {
						  nbsv_by_non_btag1_jet++;
					  }
					  else
						  continue;

				  }
				  if (jet_seed_ntrack > 0)
						h_gvtx_jet_seed_ntrack_per_non_medium_btag_wcut->Fill(jet_seed_ntrack, w);
				  h_gvtx_tight_trkmatch_nbsv_per_non_medium_btag_jet_wcut->Fill(nbsv_by_non_btag1_jet, w);
			  }

			  if (mevent->is_btagged(ijet, 2)) {
				  std::vector<size_t> vec_btag2_isv = {};
				  size_t jet_seed_ntrack = 0;
				  for (size_t j = 0; j < mevent->jet_track_which_jet.size(); ++j) {
					  if (ijet == mevent->jet_track_which_jet[j]) {
						  if (mevent->jet_track_npxlayers(j) > 1 && mevent->jet_track_nstlayers(j) > 5 && mevent->jet_track_pt(j) > 1 && fabs(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j]) > 4 && mevent->jet_track_hp_rmin[j] == 1) {
							  jet_seed_ntrack ++;
							  for (int isv = 0; isv < nsv; ++isv) {

								  const MFVVertexAux& aux = auxes->at(isv);

								  for (int itk = 0; itk < aux.ntracks(); ++itk) {


									  if (fabs(aux.track_pt(itk) - fabs(mevent->jet_track_qpt[j])) < 0.0001 &&
										  fabs(aux.track_eta[itk] - mevent->jet_track_eta[j]) < 0.0001 &&
										  fabs(aux.track_phi[itk] - mevent->jet_track_phi[j]) < 0.0001) {
										  vec_btag2_isv.push_back(isv);
									  }
								  }

							  }
						  }


					  }
				  }


				  int nbsv_by_btag2_jet = 0;
				  for (int isv = 0; isv < nsv; ++isv) {
					  const MFVVertexAux& aux = auxes->at(isv);
					  int jet_seed_ntrack_from_tight_trk_bsv = std::count(vec_btag2_isv.begin(), vec_btag2_isv.end(), isv);
					  if (jet_seed_ntrack_from_tight_trk_bsv == aux.ntracks()) {
						  nbsv_by_btag2_jet++;
					  }
					  else
						  continue;

				  }
				  if (jet_seed_ntrack > 0)
						h_gvtx_jet_seed_ntrack_per_tight_btag_wcut->Fill(jet_seed_ntrack, w);
				  h_gvtx_tight_trkmatch_nbsv_per_tight_btag_jet_wcut->Fill(nbsv_by_btag2_jet, w);
			  }
			  else {

				  std::vector<size_t> vec_non_btag2_isv = {};
				  size_t jet_seed_ntrack = 0;
				  for (size_t j = 0; j < mevent->jet_track_which_jet.size(); ++j) {
					  if (ijet == mevent->jet_track_which_jet[j]) {
						  if (mevent->jet_track_npxlayers(j) > 1 && mevent->jet_track_nstlayers(j) > 5 && mevent->jet_track_pt(j) > 1 && fabs(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j]) > 4 && mevent->jet_track_hp_rmin[j] == 1) {
							  jet_seed_ntrack ++;
							  for (int isv = 0; isv < nsv; ++isv) {

								  const MFVVertexAux& aux = auxes->at(isv);

								  for (int itk = 0; itk < aux.ntracks(); ++itk) {


									  if (fabs(aux.track_pt(itk) - fabs(mevent->jet_track_qpt[j])) < 0.0001 &&
										  fabs(aux.track_eta[itk] - mevent->jet_track_eta[j]) < 0.0001 &&
										  fabs(aux.track_phi[itk] - mevent->jet_track_phi[j]) < 0.0001) {
										  vec_non_btag2_isv.push_back(isv);
									  }
								  }

							  }
						  }


					  }
				  }


				  int nbsv_by_non_btag2_jet = 0;
				  for (int isv = 0; isv < nsv; ++isv) {
					  const MFVVertexAux& aux = auxes->at(isv);
					  int jet_seed_ntrack_from_tight_trk_bsv = std::count(vec_non_btag2_isv.begin(), vec_non_btag2_isv.end(), isv);
					  if (jet_seed_ntrack_from_tight_trk_bsv == aux.ntracks()) {
						  nbsv_by_non_btag2_jet++;
					  }
					  else
						  continue;

				  }
				  if (jet_seed_ntrack > 0)
						h_gvtx_jet_seed_ntrack_per_non_tight_btag_wcut->Fill(jet_seed_ntrack, w);
				  h_gvtx_tight_trkmatch_nbsv_per_non_tight_btag_jet_wcut->Fill(nbsv_by_non_btag2_jet, w);
			  }

			  

		  }

		  h_gvtx_nloosebsvjet->Fill(nloosebsvjet, w);
		  h_gvtx_nloosebsvplusbtaggedjet->Fill(nloosebsvplusbtaggedjet, w);

		  for (size_t i = 0; i < 4; ++i) {
			  

			  h_gvtx_bquark_pT->Fill(mevent->gen_daughters[i].Pt(), w);
			  double dR_bquark = reco::deltaR(mevent->gen_daughters[i].Eta(), mevent->gen_daughters[i].Phi(), mevent->gen_bchain_b_had_eta[i], mevent->gen_bchain_b_had_phi[i]);

			  h_gvtx_bhad_bquark_dR->Fill(dR_bquark, w);
			  h_2D_gvtx_bhad_bquark_dR_and_b_quark_pT->Fill(dR_bquark, mevent->gen_daughters[i].Pt(), w);
			  if (mevent->gen_daughters[i].Pt() < 20) {
				  all_bboost = false;
				  vec_lowpT_bquark.push_back(i);
				  continue;
			  }

			  h_gvtx_bhad_bquark_dR_wcut->Fill(dR_bquark, w);
			  h_gvtx_bhad_pT_wcut->Fill(mevent->gen_bchain_b_had_pt[i], w);
			  h_gvtx_bquark_pT_wcut->Fill(mevent->gen_daughters[i].Pt(), w);
			  for (size_t j = 0; j < mevent->gen_bchain_nonb_had_eta[i].size(); ++j) {
				  double dR_nonb = reco::deltaR(mevent->gen_bchain_nonb_had_eta[i][j], mevent->gen_bchain_nonb_had_phi[i][j], mevent->gen_bchain_b_had_eta[i], mevent->gen_bchain_b_had_phi[i]);
				  h_gvtx_bhad_nonbhad_dR_wcut->Fill(dR_nonb, w);
				  h_2D_gvtx_bhad_nonbhad_dR_and_pT_wcut->Fill(dR_nonb, mevent->gen_bchain_nonb_had_pt[i][j], w);
				  h_2D_gvtx_bhad_nonbhad_dR_and_b_quark_pT_wcut->Fill(dR_nonb, mevent->gen_daughters[i].Pt(), w);
			  }
			  h_2D_gvtx_bhad_bquark_dR_and_b_quark_pT_wcut->Fill(dR_bquark, mevent->gen_daughters[i].Pt(), w);

			  double mindR_bhad = 0.4;
			  size_t bhad_jet = 0;
			  double mindR_bquark = 4.0;
			  size_t bquark_jet = 0;
			  for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
				  if (mevent->jet_pt[ijet] < 0.0)  // Jets have a cut at 20 GeV
					  continue;
				  if (reco::deltaR(mevent->jet_eta[ijet], mevent->jet_phi[ijet], mevent->gen_bchain_b_had_eta[i], mevent->gen_bchain_b_had_phi[i]) < mindR_bhad) {
					  mindR_bhad = reco::deltaR(mevent->jet_eta[ijet], mevent->jet_phi[ijet], mevent->gen_bchain_b_had_eta[i], mevent->gen_bchain_b_had_phi[i]);
					  bhad_jet = ijet;
				  }

				  if (reco::deltaR(mevent->jet_eta[ijet], mevent->jet_phi[ijet], mevent->gen_daughters[i].Eta(), mevent->gen_daughters[i].Phi()) < mindR_bquark) {
					  mindR_bquark = reco::deltaR(mevent->jet_eta[ijet], mevent->jet_phi[ijet], mevent->gen_daughters[i].Eta(), mevent->gen_daughters[i].Phi());
					  bquark_jet = ijet;
				  }

				 
			  }

			  if (mindR_bhad < 0.4) {
				  h_gvtx_bhad_closest_jet_pT_wcut->Fill(mevent->jet_pt[bhad_jet], w);
				  h_gvtx_bhad_closest_jet_dR_wcut->Fill(mindR_bhad, w);
			  }
			  h_gvtx_bquark_jet_dR_wcut->Fill(mindR_bquark, w);
			  if (mindR_bquark < 0.4) {

				  h_gvtx_peak_dR_jet_eta_bquark_wcut->Fill(fabs(mevent->gen_daughters[i].Eta()), w);
				  h_gvtx_peak_dR_jet_pT_bquark_wcut->Fill(mevent->gen_daughters[i].Pt(), w);
				  h_gvtx_peak_dR_jet_pT_bjet_wcut->Fill(mevent->jet_pt[bquark_jet], w);
				  
				  vec_ibjet.push_back(bquark_jet);
				  match_jet_event = true;
				  std::vector<size_t> vec_isv = {};
				  std::vector<size_t> vec_tight_trk_isv = {};

				  vec_bquark_jet.push_back(bquark_jet);
				  vec_bquark.push_back(i);
				  if (std::count(vec_bquark_jet.begin(), vec_bquark_jet.end(), vec_bquark_jet[i]) > 1)
					  shared_bjet = 1;

				  h_gvtx_bquark_closest_jet_pT_wcut->Fill(mevent->jet_pt[bquark_jet], w);
				  h_gvtx_bquark_closest_jet_dR_wcut->Fill(mindR_bquark, w);
				  h_gvtx_bquark_closest_jet_E_ratio_wcut->Fill(mevent->jet_energy[bquark_jet] / mevent->gen_daughters[i].Energy(), w);
				  h_2D_gvtx_bquark_closest_jet_dR_ndau_wcut->Fill(mindR_bquark, mevent->gen_bchain_nonb_had_eta[i].size(), w);

				  double mindR_dau = 0.4;
				  for (size_t j = 0; j < mevent->gen_bchain_nonb_had_eta[i].size(); ++j) {
					  double dR_dau = reco::deltaR(mevent->gen_bchain_nonb_had_eta[i][j], mevent->gen_bchain_nonb_had_phi[i][j], mevent->jet_eta[bquark_jet], mevent->jet_phi[bquark_jet]);
					  if (dR_dau < mindR_dau) {
						  mindR_dau = dR_dau;
					  }
				  }
				  h_gvtx_bquark_closest_dau_to_closest_jet_dR_wcut->Fill(mindR_dau, w);
				  size_t jet_ntrack = 0;
				  size_t jet_onect_ntrack = 0;
				  size_t jet_twoct_ntrack = 0;
				  size_t jet_threect_ntrack = 0;
				  size_t jet_fourct_ntrack = 0;
				  size_t jet_seed_ntrack = 0;
				  double sum_track_pT = 0;
				  for (size_t j = 0; j < mevent->jet_track_which_jet.size(); ++j) {
					  if (bquark_jet == mevent->jet_track_which_jet[j]) {
						  jet_ntrack++;
						  sum_track_pT += mevent->jet_track_pt(j);
						  h_gvtx_all_track_pt_from_jets_wcut->Fill(mevent->jet_track_pt(j), w);
						  h_gvtx_all_track_sigmadxybs_from_jets_wcut->Fill(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j], w);
						  h_gvtx_all_track_npxhits_from_jets_wcut->Fill(mevent->jet_track_npxhits(j), w);
						  h_gvtx_all_track_nsthits_from_jets_wcut->Fill(mevent->jet_track_nsthits(j), w);
						  h_gvtx_all_track_npxlayers_from_jets_wcut->Fill(mevent->jet_track_npxlayers(j), w);
						  h_gvtx_all_track_nstlayers_from_jets_wcut->Fill(mevent->jet_track_nstlayers(j), w);
						  h_gvtx_all_track_rmin_from_jets_wcut->Fill(mevent->jet_track_hp_rmin[j], w);
						  if (mevent->is_btagged(bquark_jet, 0)) {
							  h_gvtx_a_type_all_tracks_pt_wcut->Fill(mevent->jet_track_pt(j), w);
							  h_gvtx_a_type_all_tracks_sigmadxybs_wcut->Fill(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j], w);
						  }
						  else {
							  h_gvtx_b_type_all_tracks_pt_wcut->Fill(mevent->jet_track_pt(j), w);
							  h_gvtx_b_type_all_tracks_sigmadxybs_wcut->Fill(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j], w);
						  }
						  if (mevent->jet_track_npxlayers(j) > 1 && mevent->jet_track_nstlayers(j) > 5 && fabs(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j]) > 4 && mevent->jet_track_hp_rmin[j] == 1)
							  h_gvtx_jet_seed_nm1_pt_from_jets_wcut->Fill(mevent->jet_track_pt(j), w);
						  if (mevent->jet_track_nstlayers(j) > 5 && fabs(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j]) > 4 && mevent->jet_track_pt(j) > 1 && mevent->jet_track_hp_rmin[j] == 1)
							  h_gvtx_jet_seed_nm1_npxlayers_from_jets_wcut->Fill(mevent->jet_track_npxlayers(j), w);
						  if (mevent->jet_track_npxlayers(j) > 1 && fabs(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j]) > 4 && mevent->jet_track_pt(j) > 1 && mevent->jet_track_hp_rmin[j] == 1)
							  h_gvtx_jet_seed_nm1_nstlayers_from_jets_wcut->Fill(mevent->jet_track_nstlayers(j), w);
						  if (mevent->jet_track_npxlayers(j) > 1 && mevent->jet_track_nstlayers(j) > 5 && mevent->jet_track_pt(j) > 1 && mevent->jet_track_hp_rmin[j] == 1)
							  h_gvtx_jet_seed_nm1_sigmadxybs_from_jets_wcut->Fill(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j], w);

						  if (mevent->jet_track_npxlayers(j) > 1 && mevent->jet_track_nstlayers(j) > 5 && mevent->jet_track_pt(j) > 1 && fabs(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j]) > 4)
							  h_gvtx_jet_seed_nm1_rmin_from_jets_wcut->Fill(mevent->jet_track_hp_rmin[j], w);

						  if (mevent->jet_track_nstlayers(j) > 5) {
							  jet_onect_ntrack++;
							  h_gvtx_one_cut_track_pT_from_jets_wcut->Fill(mevent->jet_track_pt(j), w);
							  h_gvtx_one_cut_track_sigmadxybs_from_jets_wcut->Fill(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j], w);
							  h_gvtx_one_cut_track_npxlayers_from_jets_wcut->Fill(mevent->jet_track_npxlayers(j), w);
							  h_gvtx_one_cut_track_nstlayers_from_jets_wcut->Fill(mevent->jet_track_nstlayers(j), w);
							  h_gvtx_one_cut_track_rmin_from_jets_wcut->Fill(mevent->jet_track_hp_rmin[j], w);

							  if (mevent->jet_track_npxlayers(j) > 1) {
								  jet_twoct_ntrack++;
								  h_gvtx_two_cut_track_pT_from_jets_wcut->Fill(mevent->jet_track_pt(j), w);
								  h_gvtx_two_cut_track_sigmadxybs_from_jets_wcut->Fill(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j], w);
								  h_gvtx_two_cut_track_npxlayers_from_jets_wcut->Fill(mevent->jet_track_npxlayers(j), w);
								  h_gvtx_two_cut_track_nstlayers_from_jets_wcut->Fill(mevent->jet_track_nstlayers(j), w);
								  h_gvtx_two_cut_track_rmin_from_jets_wcut->Fill(mevent->jet_track_hp_rmin[j], w);

								  if (mevent->jet_track_hp_rmin[j] == 1) {
									  jet_threect_ntrack++;
									  h_gvtx_three_cut_track_pT_from_jets_wcut->Fill(mevent->jet_track_pt(j), w);
									  h_gvtx_three_cut_track_sigmadxybs_from_jets_wcut->Fill(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j], w);
									  h_gvtx_three_cut_track_npxlayers_from_jets_wcut->Fill(mevent->jet_track_npxlayers(j), w);
									  h_gvtx_three_cut_track_nstlayers_from_jets_wcut->Fill(mevent->jet_track_nstlayers(j), w);
									  h_gvtx_three_cut_track_rmin_from_jets_wcut->Fill(mevent->jet_track_hp_rmin[j], w);

									  if (mevent->jet_track_pt(j) > 1) {
										  jet_fourct_ntrack++;
										  h_gvtx_four_cut_track_pT_from_jets_wcut->Fill(mevent->jet_track_pt(j), w);
										  h_gvtx_four_cut_track_sigmadxybs_from_jets_wcut->Fill(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j], w);
										  h_gvtx_four_cut_track_npxlayers_from_jets_wcut->Fill(mevent->jet_track_npxlayers(j), w);
										  h_gvtx_four_cut_track_nstlayers_from_jets_wcut->Fill(mevent->jet_track_nstlayers(j), w);
										  h_gvtx_four_cut_track_rmin_from_jets_wcut->Fill(mevent->jet_track_hp_rmin[j], w);

										  if (fabs(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j]) > 4) {
											  jet_seed_ntrack++;
											  h_gvtx_jet_seed_track_pT_from_jets_wcut->Fill(mevent->jet_track_pt(j), w);
											  h_gvtx_jet_seed_track_sigmadxybs_from_jets_wcut->Fill(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j], w);
											  h_gvtx_jet_seed_track_npxlayers_from_jets_wcut->Fill(mevent->jet_track_npxlayers(j), w);
											  h_gvtx_jet_seed_track_nstlayers_from_jets_wcut->Fill(mevent->jet_track_nstlayers(j), w);
											  h_gvtx_jet_seed_track_rmin_from_jets_wcut->Fill(mevent->jet_track_hp_rmin[j], w);

											  for (int isv = 0; isv < nsv; ++isv) {

												  const MFVVertexAux& aux = auxes->at(isv);

												  for (int itk = 0; itk < aux.ntracks(); ++itk) {
													  double match_threshold = 1.1;

													  double a = fabs(aux.track_pt(itk) - fabs(mevent->jet_track_qpt[j])) + 1;
													  double b = fabs(aux.track_eta[itk] - mevent->jet_track_eta[j]) + 1;
													  double c = fabs(aux.track_phi[itk] - mevent->jet_track_phi[j]) + 1;
													  h_gvtx_match_pT_wcut->Fill(fabs(aux.track_pt(itk) - fabs(mevent->jet_track_qpt[j])), w);
													  h_gvtx_match_eta_wcut->Fill(fabs(aux.track_eta[itk] - mevent->jet_track_eta[j]), w);
													  h_gvtx_match_phi_wcut->Fill(fabs(aux.track_phi[itk] - mevent->jet_track_phi[j]), w);

													  if (fabs(aux.track_phi[itk] - mevent->jet_track_phi[j]) < 0.0001) {
														  h_gvtx_match_pT_phicut_wcut->Fill(fabs(aux.track_pt(itk) - fabs(mevent->jet_track_qpt[j])), w);
														  h_gvtx_match_eta_phicut_wcut->Fill(fabs(aux.track_eta[itk] - mevent->jet_track_eta[j]), w);
													  }
													  if (fabs(aux.track_eta[itk] - mevent->jet_track_eta[j]) < 0.0001) {
														  h_gvtx_match_pT_etacut_wcut->Fill(fabs(aux.track_pt(itk) - fabs(mevent->jet_track_qpt[j])), w);
														  h_gvtx_match_phi_etacut_wcut->Fill(fabs(aux.track_phi[itk] - mevent->jet_track_phi[j]), w);
													  }
													  if (fabs(aux.track_pt(itk) - fabs(mevent->jet_track_qpt[j])) < 0.0001) {
														  h_gvtx_match_eta_pTcut_wcut->Fill(fabs(aux.track_eta[itk] - mevent->jet_track_eta[j]), w);
														  h_gvtx_match_phi_pTcut_wcut->Fill(fabs(aux.track_phi[itk] - mevent->jet_track_phi[j]), w);
													  }



													  if (a * b * c < match_threshold) {
														  vec_isv.push_back(isv);
													  }

													  if (fabs(aux.track_pt(itk) - fabs(mevent->jet_track_qpt[j])) < 0.0001 &&
														  fabs(aux.track_eta[itk] - mevent->jet_track_eta[j]) < 0.0001 &&
														  fabs(aux.track_phi[itk] - mevent->jet_track_phi[j]) < 0.0001) {
														  vec_tight_trk_isv.push_back(isv);
													  }
												  }

											  }


										  }
									  }
								  }
							  }
						  }

					  }
				  }

				  size_t bsv_seed_ntrack = 0;
				  size_t count_bsv = 0;

				  double mindR_sv_trk = 3.0;
				  double mindR_sv_jet = 3.0;
				  double mindR_sv = 3.0;
				  double mindR_sv_displ = 3.0;
				  double mindR_b_sv_trk = 3.0;
				  double mindR_b_sv_jet = 3.0;
				  double mindR_b_sv = 3.0;
				  double mindR_b_sv_displ = 3.0;
				  double mindR_b_sv_dist3d = 3.0;


				  for (int isv = 0; isv < nsv; ++isv) {
					  const MFVVertexAux& aux = auxes->at(isv);
					  double sv_trk_eta = aux.eta[mfv::PTracksOnly];
					  double sv_trk_phi = aux.phi[mfv::PTracksOnly];
					  double sv_jet_eta = aux.eta[mfv::PJetsByNtracks];
					  double sv_jet_phi = aux.phi[mfv::PJetsByNtracks];
					  double sv_eta = aux.eta[mfv::PTracksPlusJetsByNtracks];
					  double sv_phi = aux.phi[mfv::PTracksPlusJetsByNtracks];

					  TVector3 gen_sv_flight = TVector3(aux.x - mevent->pvx, aux.y - mevent->pvy, aux.z - mevent->pvz);



					  double dR_sv_trk = reco::deltaR(sv_trk_eta, sv_trk_phi, mevent->jet_eta[bquark_jet], mevent->jet_phi[bquark_jet]);
					  if (dR_sv_trk < mindR_sv_trk)
						  mindR_sv_trk = dR_sv_trk;
					  double dR_sv_jet = reco::deltaR(sv_jet_eta, sv_jet_phi, mevent->jet_eta[bquark_jet], mevent->jet_phi[bquark_jet]);
					  if (dR_sv_jet < mindR_sv_jet)
						  mindR_sv_jet = dR_sv_jet;
					  double dR_sv = reco::deltaR(sv_eta, sv_phi, mevent->jet_eta[bquark_jet], mevent->jet_phi[bquark_jet]);
					  if (dR_sv < mindR_sv)
						  mindR_sv = dR_sv;
					  double dR_sv_displ = reco::deltaR(gen_sv_flight.Eta(), gen_sv_flight.Phi(), mevent->jet_eta[bquark_jet], mevent->jet_phi[bquark_jet]);
					  if (dR_sv_displ < mindR_sv_displ)
						  mindR_sv_displ = dR_sv_displ;

					  double dR_b_sv_trk = reco::deltaR(sv_trk_eta, sv_trk_phi, mevent->gen_daughters[i].Eta(), mevent->gen_daughters[i].Phi());
					  if (dR_b_sv_trk < mindR_b_sv_trk)
						  mindR_b_sv_trk = dR_b_sv_trk;
					  double dR_b_sv_jet = reco::deltaR(sv_jet_eta, sv_jet_phi, mevent->gen_daughters[i].Eta(), mevent->gen_daughters[i].Phi());
					  if (dR_b_sv_jet < mindR_b_sv_jet)
						  mindR_b_sv_jet = dR_b_sv_jet;
					  double dR_b_sv = reco::deltaR(sv_eta, sv_phi, mevent->gen_daughters[i].Eta(), mevent->gen_daughters[i].Phi());
					  if (dR_b_sv < mindR_b_sv)
						  mindR_b_sv = dR_b_sv;
					  double dR_b_sv_displ = reco::deltaR(gen_sv_flight.Eta(), gen_sv_flight.Phi(), mevent->gen_daughters[i].Eta(), mevent->gen_daughters[i].Phi());
					  if (dR_b_sv_displ < mindR_b_sv_displ)
						  mindR_b_sv_displ = dR_b_sv_displ;

					  double dR_b_sv_dist3d = 0.0;
					  if (i == 0) {
						  dR_b_sv_dist3d = sqrt(pow(mevent->gen_b_llp0_decay[0] - aux.x, 2) + pow(mevent->gen_b_llp0_decay[1] - aux.y, 2) + pow(mevent->gen_b_llp0_decay[2] - aux.z, 2));
					  }
					  else if (i == 1) {
						  dR_b_sv_dist3d = sqrt(pow(mevent->gen_b_llp0_decay[3] - aux.x, 2) + pow(mevent->gen_b_llp0_decay[4] - aux.y, 2) + pow(mevent->gen_b_llp0_decay[5] - aux.z, 2));
					  }
					  else if (i == 2) {
						  dR_b_sv_dist3d = sqrt(pow(mevent->gen_b_llp1_decay[0] - aux.x, 2) + pow(mevent->gen_b_llp1_decay[1] - aux.y, 2) + pow(mevent->gen_b_llp1_decay[2] - aux.z, 2));
					  }
					  else {
						  dR_b_sv_dist3d = sqrt(pow(mevent->gen_b_llp1_decay[3] - aux.x, 2) + pow(mevent->gen_b_llp1_decay[4] - aux.y, 2) + pow(mevent->gen_b_llp1_decay[5] - aux.z, 2));
					  }



					  if (dR_b_sv_dist3d < mindR_b_sv_dist3d)
						  mindR_b_sv_dist3d = dR_b_sv_dist3d;


					  if (reco::deltaR(sv_jet_eta, sv_jet_phi, mevent->jet_eta[bquark_jet], mevent->jet_phi[bquark_jet]) < 0.01) {
						  count_bsv++;
						  if (count_bsv > 0) {
							  bsv_seed_ntrack += aux.ntracks();
							  h_gvtx_seed_ntrack_per_bsv_from_jets_wcut->Fill(aux.ntracks(), w);
							  for (int itk = 0; itk < aux.ntracks(); ++itk) {
								  h_gvtx_seed_track_pT_from_jets_wcut->Fill(mevent->vertex_seed_track_pt(itk), w);
								  h_gvtx_seed_track_sigmadxybs_from_jets_wcut->Fill(mevent->vertex_seed_track_dxy[itk] / mevent->vertex_seed_track_err_dxy[itk], w);
								  h_gvtx_seed_track_npxlayers_from_jets_wcut->Fill(mevent->vertex_seed_track_npxlayers(itk), w);
								  h_gvtx_seed_track_nstlayers_from_jets_wcut->Fill(mevent->vertex_seed_track_nstlayers(itk), w);
								  h_gvtx_seed_track_rmin_from_jets_wcut->Fill(mevent->vertex_seed_track_hp_rmin[itk], w);

							  }
						  }
					  }

				  }
				  if (mindR_sv_trk < 3)
					  h_gvtx_sv_trkonly_mom_jet_mom_dR_wcut->Fill(mindR_sv_trk, w);
				  if (mindR_sv_jet < 3)
					  h_gvtx_sv_jetbytrk_mom_jet_mom_dR_wcut->Fill(mindR_sv_jet, w);
				  if (mindR_sv < 3)
					  h_gvtx_sv_trkplusjetbytrk_mom_jet_mom_dR_wcut->Fill(mindR_sv, w);
				  if (mindR_sv_displ < 3)
					  h_gvtx_sv_displ_vec_jet_mom_dR_wcut->Fill(mindR_sv_displ, w);

				  if (mindR_b_sv_trk < 3)
					  h_gvtx_sv_trkonly_mom_bquark_mom_dR_wcut->Fill(mindR_b_sv_trk, w);
				  if (mindR_b_sv_jet < 3)
					  h_gvtx_sv_jetbytrk_mom_bquark_mom_dR_wcut->Fill(mindR_b_sv_jet, w);
				  if (mindR_b_sv < 3)
					  h_gvtx_sv_trkplusjetbytrk_mom_bquark_mom_dR_wcut->Fill(mindR_b_sv, w);
				  if (mindR_b_sv_displ < 3)
					  h_gvtx_sv_displ_vec_bquark_mom_dR_wcut->Fill(mindR_b_sv_displ, w);

				  if (mindR_b_sv_dist3d < 3)
					  h_gvtx_sv_bquark_closest_dist3d_wcut->Fill(mindR_b_sv_dist3d, w);

				  if (count_bsv > 0) {
					  h_gvtx_seed_ntrack_bsvs_from_jets_wcut->Fill(bsv_seed_ntrack, w);
				  }

				  for (int isv = 0; isv < nsv; ++isv) {
					  const MFVVertexAux& aux = auxes->at(isv);
					  size_t jet_seed_ntrack_from_bsv = std::count(vec_isv.begin(), vec_isv.end(), isv);
					  if (jet_seed_ntrack_from_bsv > 0 && std::count(vec_ibsv.begin(), vec_ibsv.end(), isv) == 0)
						  vec_ibsv.push_back(isv);
					  else
						  continue;
					  h_gvtx_bsv_dBV_wcut->Fill(mag(aux.x - mevent->bsx_at_z(aux.z), aux.y - mevent->bsy_at_z(aux.z)), w);
					  h_2D_gvtx_ntrack_bsv_and_jet_seed_ntrack_from_bsv_wcut->Fill(aux.ntracks(), jet_seed_ntrack_from_bsv, w);
				  }

				  int nbsv_by_bjet = 0;
				  for (int isv = 0; isv < nsv; ++isv) {
					  const MFVVertexAux& aux = auxes->at(isv);
					  int jet_seed_ntrack_from_tight_trk_bsv = std::count(vec_tight_trk_isv.begin(), vec_tight_trk_isv.end(), isv);
					  if (jet_seed_ntrack_from_tight_trk_bsv == aux.ntracks() && std::count(vec_tight_trk_ibsv.begin(), vec_tight_trk_ibsv.end(), isv) == 0) {
						  vec_tight_trk_ibsv.push_back(isv);
						  nbsv_by_bjet++;
					  }
					  else
						  continue;
					  h_2D_gvtx_ntrack_bsv_and_jet_seed_ntrack_from_tight_trkmatch_bsv_wcut->Fill(aux.ntracks(), jet_seed_ntrack_from_tight_trk_bsv, w);
				  }

				  h_gvtx_tight_trkmatch_nbsv_per_bjet_wcut->Fill(nbsv_by_bjet, w);
				  if (nbsv_by_bjet > 0)
					  h_gvtx_has_bSV_per_bjet_or_not_wcut->Fill(1.0, w);
				  else
					  h_gvtx_has_bSV_per_bjet_or_not_wcut->Fill(0.0, w);


				  h_gvtx_is_tight_btag_per_bjet_or_not_wcut->Fill(mevent->is_btagged(bquark_jet, 2), w);
				  h_gvtx_is_medium_btag_per_bjet_or_not_wcut->Fill(mevent->is_btagged(bquark_jet, 1), w);
				  h_gvtx_is_loose_btag_per_bjet_or_not_wcut->Fill(mevent->is_btagged(bquark_jet, 0), w);


				  if (mevent->is_btagged(bquark_jet, 0)) {
					  h_gvtx_a_type_diff_pT_bquark_jet_wcut->Fill(mevent->jet_pt[bquark_jet] - mevent->gen_daughters[i].Pt(), w);
					  h_gvtx_a_type_dR_bquark_wcut->Fill(mindR_bquark, w);
					  h_gvtx_a_type_nbsv_wcut->Fill(nbsv_by_bjet, w);
					  h_gvtx_a_type_seed_ntrack_wcut->Fill(jet_seed_ntrack, w);
					  h_gvtx_a_type_all_ntrack_wcut->Fill(jet_ntrack, w);
					  h_gvtx_a_type_eta_bquark_jet_wcut->Fill(fabs(mevent->gen_daughters[i].Eta()), w);
					  h_gvtx_a_type_pT_jet_wcut->Fill(mevent->jet_pt[bquark_jet], w);
				  }
				  else {
					  h_gvtx_b_type_diff_pT_bquark_jet_wcut->Fill(mevent->jet_pt[bquark_jet] - mevent->gen_daughters[i].Pt(), w);
					  h_gvtx_b_type_dR_bquark_wcut->Fill(mindR_bquark, w);
					  h_gvtx_b_type_nbsv_wcut->Fill(nbsv_by_bjet, w);
					  h_gvtx_b_type_seed_ntrack_wcut->Fill(jet_seed_ntrack, w);
					  h_gvtx_b_type_all_ntrack_wcut->Fill(jet_ntrack, w);
				  }

				  sum_nbsv_by_bjet += nbsv_by_bjet;

				  if (jet_onect_ntrack > 0)
					  h_gvtx_one_cut_ntrack_from_jets_wcut->Fill(jet_onect_ntrack, w);
				  if (jet_twoct_ntrack > 0)
					  h_gvtx_two_cut_ntrack_from_jets_wcut->Fill(jet_twoct_ntrack, w);
				  if (jet_threect_ntrack > 0)
					  h_gvtx_three_cut_ntrack_from_jets_wcut->Fill(jet_threect_ntrack, w);
				  if (jet_fourct_ntrack > 0)
					  h_gvtx_four_cut_ntrack_from_jets_wcut->Fill(jet_fourct_ntrack, w);
				  if (jet_seed_ntrack > 0)
					  h_gvtx_jet_seed_ntrack_per_bjet_wcut->Fill(jet_seed_ntrack, w);
				  if (jet_ntrack > 0)
					  h_gvtx_all_ntrack_from_jets_wcut->Fill(jet_ntrack, w);
				  h_gvtx_sum_pT_all_tracks_from_jets_wcut->Fill(sum_track_pT, w);
				  h_gvtx_bquark_closest_jet_res_pT_wcut->Fill(sum_track_pT - mevent->gen_daughters[i].Pt(), w);
			  }
			  else {
			        h_gvtx_tail_dR_jet_eta_bquark_wcut->Fill(fabs(mevent->gen_daughters[i].Eta()), w);
					h_gvtx_tail_dR_jet_pT_bquark_wcut->Fill(mevent->gen_daughters[i].Pt(), w);
              }

			  double min_sv_dist3d_bvtx = 100;
			  for (int isv = 0; isv < nsv; ++isv) {
				  const MFVVertexAux& aux = auxes->at(isv);

				  double dR_b_sv_dist3d = 0.0;
				  if (i == 0) {
					  dR_b_sv_dist3d = sqrt(pow(mevent->gen_b_llp0_decay[0] - aux.x, 2) + pow(mevent->gen_b_llp0_decay[1] - aux.y, 2) + pow(mevent->gen_b_llp0_decay[2] - aux.z, 2));
				  }
				  else if (i == 1) {
					  dR_b_sv_dist3d = sqrt(pow(mevent->gen_b_llp0_decay[3] - aux.x, 2) + pow(mevent->gen_b_llp0_decay[4] - aux.y, 2) + pow(mevent->gen_b_llp0_decay[5] - aux.z, 2));
				  }
				  else if (i == 2) {
					  dR_b_sv_dist3d = sqrt(pow(mevent->gen_b_llp1_decay[0] - aux.x, 2) + pow(mevent->gen_b_llp1_decay[1] - aux.y, 2) + pow(mevent->gen_b_llp1_decay[2] - aux.z, 2));
				  }
				  else {
					  dR_b_sv_dist3d = sqrt(pow(mevent->gen_b_llp1_decay[3] - aux.x, 2) + pow(mevent->gen_b_llp1_decay[4] - aux.y, 2) + pow(mevent->gen_b_llp1_decay[5] - aux.z, 2));
				  }

				  if (min_sv_dist3d_bvtx > dR_b_sv_dist3d) {
					  min_sv_dist3d_bvtx = dR_b_sv_dist3d;
				  }
			  }

			  h_gvtx_sv_bquark_dist3d_wcut->Fill(min_sv_dist3d_bvtx, w);


		  }


		  int nbsv = vec_ibsv.size();
		  size_t nbjet = vec_ibjet.size();

		  
		  vec_tight_trk_ibsv = {};

		  for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
				  
				  if (std::count(vec_ibjet.begin(), vec_ibjet.end(), ijet) > 0)  // this is a b-jet 
					  continue;

				  double mindR_bquark = 4.0;
				  size_t ibquark = 0;
				  for (size_t k = 0; k < vec_lowpT_bquark.size(); ++k) {
					  double dR_bquark = reco::deltaR(mevent->jet_eta[ijet], mevent->jet_phi[ijet], mevent->gen_daughters[vec_lowpT_bquark[k]].Eta(), mevent->gen_daughters[vec_lowpT_bquark[k]].Phi());
					  if (dR_bquark < mindR_bquark) {
						  mindR_bquark = dR_bquark;
						  ibquark = vec_lowpT_bquark[k];
					  }
				  }

				  std::vector<size_t> vec_tight_trk_isv = {};
				  size_t jet_seed_ntrack = 0;
				  size_t jet_ntrack = 0;
				  for (size_t j = 0; j < mevent->jet_track_which_jet.size(); ++j) {
					  if (ijet == mevent->jet_track_which_jet[j]) {
						  jet_ntrack++;
						  if (mevent->is_btagged(ijet, 0)) {
							  h_gvtx_c_type_all_tracks_pt_wcut->Fill(mevent->jet_track_pt(j), w);
							  h_gvtx_c_type_all_tracks_sigmadxybs_wcut->Fill(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j], w);
							  if (mindR_bquark < 0.4) {
								  h_gvtx_sub_c_type_all_tracks_pt_wcut->Fill(mevent->jet_track_pt(j), w);
								  h_gvtx_sub_c_type_all_tracks_sigmadxybs_wcut->Fill(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j], w);
							  }
							  else {
								  h_gvtx_fake_c_type_all_tracks_pt_wcut->Fill(mevent->jet_track_pt(j), w);
								  h_gvtx_fake_c_type_all_tracks_sigmadxybs_wcut->Fill(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j], w);

							  }
						  }
						  else {
							  h_gvtx_d_type_all_tracks_pt_wcut->Fill(mevent->jet_track_pt(j), w);
							  h_gvtx_d_type_all_tracks_sigmadxybs_wcut->Fill(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j], w);
							  if (mindR_bquark < 0.4) {
								  h_gvtx_sub_d_type_all_tracks_pt_wcut->Fill(mevent->jet_track_pt(j), w);
								  h_gvtx_sub_d_type_all_tracks_sigmadxybs_wcut->Fill(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j], w);
							  }
							  
						  }
						  if (mevent->jet_track_npxlayers(j) > 1 && mevent->jet_track_nstlayers(j) > 5 && mevent->jet_track_pt(j) > 1 && fabs(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j]) > 4 && mevent->jet_track_hp_rmin[j] == 1) {
							  jet_seed_ntrack ++;
							  for (int isv = 0; isv < nsv; ++isv) {

								  const MFVVertexAux& aux = auxes->at(isv);

								  for (int itk = 0; itk < aux.ntracks(); ++itk) {


									  if (fabs(aux.track_pt(itk) - fabs(mevent->jet_track_qpt[j])) < 0.0001 &&
										  fabs(aux.track_eta[itk] - mevent->jet_track_eta[j]) < 0.0001 &&
										  fabs(aux.track_phi[itk] - mevent->jet_track_phi[j]) < 0.0001) {
										  vec_tight_trk_isv.push_back(isv);
									  }
								  }

							  }
						  }


					  }
				  }

				  int nbsv_by_non_bjet = 0;
				  for (int isv = 0; isv < nsv; ++isv) {
					  const MFVVertexAux& aux = auxes->at(isv);
					  int jet_seed_ntrack_from_tight_trk_bsv = std::count(vec_tight_trk_isv.begin(), vec_tight_trk_isv.end(), isv);
					  if (jet_seed_ntrack_from_tight_trk_bsv == aux.ntracks() && std::count(vec_tight_trk_ibsv.begin(), vec_tight_trk_ibsv.end(), isv) == 0) {
						  vec_tight_trk_ibsv.push_back(isv);
						  nbsv_by_non_bjet++;
					  }
					  else
						  continue;

				  }

				  if (jet_seed_ntrack > 0)
					  h_gvtx_jet_seed_ntrack_per_non_bjet_wcut->Fill(jet_seed_ntrack, w);

				  h_gvtx_tight_trkmatch_nbsv_per_non_bjet_wcut->Fill(nbsv_by_non_bjet, w);

				  if (nbsv_by_non_bjet > 0)
					  h_gvtx_has_bSV_per_non_bjet_or_not_wcut->Fill(1.0, w);
				  else
					  h_gvtx_has_bSV_per_non_bjet_or_not_wcut->Fill(0.0, w);


				  h_gvtx_is_tight_btag_per_non_bjet_or_not_wcut->Fill(mevent->is_btagged(ijet, 2), w);
				  h_gvtx_is_medium_btag_per_non_bjet_or_not_wcut->Fill(mevent->is_btagged(ijet, 1), w);
				  h_gvtx_is_loose_btag_per_non_bjet_or_not_wcut->Fill(mevent->is_btagged(ijet, 0), w);

				  

				  if (mevent->is_btagged(ijet, 0)) {
					  h_gvtx_c_type_nbsv_wcut->Fill(nbsv_by_non_bjet, w);
					  h_gvtx_c_type_seed_ntrack_wcut->Fill(jet_seed_ntrack, w);
					  h_gvtx_c_type_all_ntrack_wcut->Fill(jet_ntrack, w);
					  if (vec_lowpT_bquark.size() > 0) {
						  h_gvtx_c_type_dR_closest_lowpT_bquark_wcut->Fill(mindR_bquark,w);
						  if (mindR_bquark < 0.4) {
							  h_gvtx_sub_c_type_pT_bquark_wcut->Fill(mevent->gen_daughters[ibquark].Pt(), w);
							  h_gvtx_sub_c_type_diff_pT_bquark_jet_wcut->Fill(mevent->jet_pt[ijet] - mevent->gen_daughters[ibquark].Pt(), w);
							  h_gvtx_sub_c_type_nbsv_wcut->Fill(nbsv_by_non_bjet, w);
							  h_gvtx_sub_c_type_seed_ntrack_wcut->Fill(jet_seed_ntrack, w);
							  h_gvtx_sub_c_type_all_ntrack_wcut->Fill(jet_ntrack, w);
							  h_gvtx_sub_c_type_eta_bquark_jet_wcut->Fill(fabs(mevent->gen_daughters[ibquark].Eta()), w);
							  h_gvtx_sub_c_type_pT_jet_wcut->Fill(mevent->jet_pt[ijet], w);
							  double min_pair_bquark = 4.0;
							  size_t jjet = 0;
							  size_t jbquark = 0;
                              for (size_t k = 0; k < vec_bquark_jet.size(); ++k) {
								  double pair_bquark = reco::deltaR(mevent->gen_daughters[vec_bquark[k]].Eta(), mevent->gen_daughters[vec_bquark[k]].Phi(), mevent->gen_daughters[ibquark].Eta(), mevent->gen_daughters[ibquark].Phi());
								  if (pair_bquark < min_pair_bquark) {
									  min_pair_bquark = pair_bquark;
									  jjet = vec_bquark_jet[k];
									  jbquark = vec_bquark[k];
								  }

							  }
							  if (min_pair_bquark < 0.4) {
								  h_gvtx_sub_c_type_dR_jets_close_bquark_wcut->Fill(reco::deltaR(mevent->jet_eta[jjet], mevent->jet_phi[jjet], mevent->jet_eta[ijet], mevent->jet_phi[ijet]), w);
								  h_gvtx_sub_c_type_E_ratio_close_bquark_wcut->Fill((mevent->jet_energy[jjet] + mevent->jet_energy[ijet]) / (mevent->gen_daughters[ibquark].Energy() + mevent->gen_daughters[jbquark].Energy()), w);
								  h_gvtx_sub_c_type_pT_bquark_close_bquark_wcut->Fill(mevent->gen_daughters[jbquark].Pt(), w);
								  h_gvtx_sub_c_type_pT_jet_close_bquark_wcut->Fill(mevent->jet_pt[jjet], w);
							  }
						  }
						  else {
							  h_gvtx_fake_c_type_pT_bquark_wcut->Fill(mevent->gen_daughters[ibquark].Pt(), w);
							  h_gvtx_fake_c_type_diff_pT_bquark_jet_wcut->Fill(mevent->jet_pt[ijet] - mevent->gen_daughters[ibquark].Pt(), w);
							  h_gvtx_fake_c_type_nbsv_wcut->Fill(nbsv_by_non_bjet, w);
							  h_gvtx_fake_c_type_seed_ntrack_wcut->Fill(jet_seed_ntrack, w);
							  h_gvtx_fake_c_type_all_ntrack_wcut->Fill(jet_ntrack, w);
							  h_gvtx_fake_c_type_eta_bquark_jet_wcut->Fill(fabs(mevent->gen_daughters[ibquark].Eta()), w);
							  h_gvtx_fake_c_type_pT_jet_wcut->Fill(mevent->jet_pt[ijet], w);
						  }
					  }

				  }
				  else {
					  h_gvtx_d_type_nbsv_wcut->Fill(nbsv_by_non_bjet, w);
					  h_gvtx_d_type_seed_ntrack_wcut->Fill(jet_seed_ntrack, w);
					  h_gvtx_d_type_all_ntrack_wcut->Fill(jet_ntrack, w);
					  if (vec_lowpT_bquark.size() > 0) {
						  h_gvtx_d_type_dR_closest_lowpT_bquark_wcut->Fill(mindR_bquark, w);
						  if (mindR_bquark < 0.4) {
							  h_gvtx_sub_d_type_pT_bquark_wcut->Fill(mevent->gen_daughters[ibquark].Pt(), w);
							  h_gvtx_sub_d_type_diff_pT_bquark_jet_wcut->Fill(mevent->jet_pt[ijet] - mevent->gen_daughters[ibquark].Pt(), w);
							  h_gvtx_sub_d_type_nbsv_wcut->Fill(nbsv_by_non_bjet, w);
							  h_gvtx_sub_d_type_seed_ntrack_wcut->Fill(jet_seed_ntrack, w);
						  }
					  }
				  }


		  }
		  


		  h_gvtx_nbsv_by_nsv_wcut->Fill(nbsv / nsv, w);
		  h_gvtx_numerator_nbsv_wcut->Fill(nbsv, w);
		  h_gvtx_numerator_tight_trkmatch_nbsv_wcut->Fill(vec_tight_trk_ibsv.size(), w);
		  h_gvtx_denominator_nsv_wcut->Fill(nsv, w);
		  h_2D_gvtx_numerator_nbsv_bjets_wcut->Fill(nbsv, nbjet, w);
		  h_2D_gvtx_numerator_tight_trkmatch_nbsv_bjets_wcut->Fill(vec_tight_trk_ibsv.size(), nbjet, w);
		  h_2D_gvtx_denominator_nbsv_bjets_wcut->Fill(nsv, nbjet, w);
		  h_gvtx_nbjet->Fill(nbjet, w);
		  if (match_jet_event == true)
			  h_gvtx_shared_bjet_or_not_wcut->Fill(shared_bjet, w);
		  if (all_bboost == true)
			  h_gvtx_njet_bboost_wcut->Fill(mevent->njets(20), w);

	  }
  }
	  
  
  h_minlspdist2d->Fill(mevent->minlspdist2d(), w);
  h_lspdist2d->Fill(mevent->lspdist2d(), w);
  h_lspdist3d->Fill(mevent->lspdist3d(), w);

  //////////////////////////////////////////////////////////////////////////////

  h_hlt_bits->Fill(0., w);
  h_l1_bits->Fill(0., w);
  h_filter_bits->Fill(0., w);
  for (int i = 0; i < mfv::n_hlt_paths; ++i) {
    if (mevent->found_hlt(i)) h_hlt_bits->Fill(1+2*i,   w);
    if (mevent->pass_hlt (i)) h_hlt_bits->Fill(1+2*i+1, w);
  }
  for (int i = 0; i < mfv::n_l1_paths; ++i) {
    if (mevent->found_l1(i)) h_l1_bits->Fill(1+2*i,   w);
    if (mevent->pass_l1 (i)) h_l1_bits->Fill(1+2*i+1, w);
  }
  for (int i = 0; i < mfv::n_filter_paths; ++i) {
    if (mevent->pass_filter (i)) h_filter_bits->Fill(i+1, w);
  }

  //////////////////////////////////////////////////////////////////////////////

  h_npu->Fill(mevent->npu, w);

  h_bsx->Fill(mevent->bsx, w);
  h_bsy->Fill(mevent->bsy, w);
  h_bsz->Fill(mevent->bsz, w);
  h_bsphi->Fill(atan2(mevent->bsy, mevent->bsx), w);

  h_npv->Fill(mevent->npv, w);
  for (auto h : { h_pvx, h_pvxwide }) h->Fill(mevent->pvx - mevent->bsx_at_z(mevent->pvz), w);
  for (auto h : { h_pvy, h_pvywide }) h->Fill(mevent->pvy - mevent->bsy_at_z(mevent->pvz), w);
  h_pvz->Fill(mevent->pvz - mevent->bsz, w);
  h_pvcxx->Fill(mevent->pvcxx, w);
  h_pvcxy->Fill(mevent->pvcxy, w);
  h_pvcxz->Fill(mevent->pvcxz, w);
  h_pvcyy->Fill(mevent->pvcyy, w);
  h_pvcyz->Fill(mevent->pvcyz, w);
  h_pvczz->Fill(mevent->pvczz, w);
  h_pvphi->Fill(atan2(mevent->pvy - mevent->bsy_at_z(mevent->pvz), mevent->pvx - mevent->bsx_at_z(mevent->pvz)), w);
  h_pvntracks->Fill(mevent->pv_ntracks, w);
  h_pvscore->Fill(mevent->pv_score, w);
  h_pvrho->Fill(mevent->pv_rho(), w);
  for (auto h : { h_pvrho, h_pvrhowide }) h->Fill(mevent->pv_rho(), w);
  for (size_t i = 0; i < mevent->npv; ++i) {
    const float z = mevent->pv_z(i);
    const float x = mevent->pv_x(i) - mevent->bsx_at_z(z);
    const float y = mevent->pv_y(i) - mevent->bsy_at_z(z);
    for (auto h : { h_pvsx, h_pvsxwide }) h->Fill(x, w);
    for (auto h : { h_pvsy, h_pvsywide }) h->Fill(y, w);
    h_pvsz->Fill(z, w);
    for (auto h : { h_pvsrho, h_pvsrhowide }) h->Fill(hypot(x,y), w);
    h_pvsphi->Fill(atan2(y,x), w);
    h_pvsscore->Fill(mevent->pv_score_(i), w);

    jmt::MinValue mindz, mindz_minscore;
    jmt::MaxValue maxdz, maxdz_minscore;
    for (size_t j = i+1; j < mevent->npv; ++j) {
      const float z2 = mevent->pv_z(j);
      //const float x2 = mevent->pv_x(j) - mevent->bsx_at_z(z);
      //const float y2 = mevent->pv_y(j) - mevent->bsy_at_z(z);
      const float dz = fabs(z-z2);
      h_pvsdz->Fill(dz, w);
      mindz(dz), maxdz(dz);
      if (mevent->pv_score_(i) > 50e3 && mevent->pv_score_(j) > 50e3)
        mindz_minscore(dz), maxdz_minscore(dz);
    }
    h_pvsmindz->Fill(mindz, w);
    h_pvsmaxdz->Fill(maxdz, w);
    h_pvsmindz_minscore->Fill(mindz_minscore, w);
    h_pvsmaxdz_minscore->Fill(maxdz_minscore, w);
  }

  h_njets->Fill(mevent->njets(), w);
  h_njets20->Fill(mevent->njets(20), w);

  for (int i = 0; i < MAX_NJETS; ++i) {
    h_jet_pt[i]->Fill(mevent->nth_jet_pt(i), w);
    h_jet_eta[i]->Fill(mevent->nth_jet_eta(i), w);
    h_jet_phi[i]->Fill(mevent->nth_jet_phi(i), w);
  }
  h_jet_ht->Fill(mevent->jet_ht(mfv::min_jet_pt), w);
  h_jet_ht_40->Fill(mevent->jet_ht(40), w);

  for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
    if (mevent->jet_pt[ijet] < mfv::min_jet_pt)
      continue;
    h_jet_pt[MAX_NJETS]->Fill(mevent->jet_pt[ijet], w);
    h_jet_eta[MAX_NJETS]->Fill(mevent->jet_eta[ijet], w);
    h_jet_phi[MAX_NJETS]->Fill(mevent->jet_phi[ijet], w);
    h_jet_energy->Fill(mevent->jet_energy[ijet], w);
    for (size_t jjet = ijet+1; jjet < mevent->jet_id.size(); ++jjet) {
      if (mevent->jet_pt[jjet] < mfv::min_jet_pt)
        continue;
      h_jet_pairdphi->Fill(reco::deltaPhi(mevent->jet_phi[ijet], mevent->jet_phi[jjet]), w);
      h_jet_pairdeta->Fill(std::max(mevent->jet_eta[ijet], mevent->jet_eta[jjet]) - std::min(mevent->jet_eta[ijet], mevent->jet_eta[jjet]), w);
      h_jet_pairdr->Fill(reco::deltaR(mevent->jet_eta[ijet], mevent->jet_phi[ijet], mevent->jet_eta[jjet], mevent->jet_phi[jjet]), w);
    }
  }

  for (int i = 0; i < 2; ++i) {
    h_nmuons[i]->Fill(mevent->nmu(i), w);
    h_nelectrons[i]->Fill(mevent->nel(i), w);
    h_nleptons[i]->Fill(mevent->nlep(i), w);
  }

  for (size_t ilep = 0; ilep < mevent->nlep(); ++ilep) {
    const size_t j = mevent->is_electron(ilep);
    for (size_t i = 0; i < 2; ++i)
      if (i == 0 || mevent->pass_lep_sel(ilep)) {
        h_leptons_pt[j][i]->Fill(mevent->lep_pt(ilep), w);
        h_leptons_eta[j][i]->Fill(mevent->lep_eta[ilep], w);
        h_leptons_phi[j][i]->Fill(mevent->lep_phi[ilep], w);
        h_leptons_dxy[j][i]->Fill(mevent->lep_dxy[ilep], w);
        h_leptons_dxybs[j][i]->Fill(mevent->lep_dxybs[ilep], w);
        h_leptons_dz[j][i]->Fill(mevent->lep_dz[ilep], w);
        h_leptons_iso[j][i]->Fill(mevent->lep_iso[ilep], w);
      }
  }

  h_met->Fill(mevent->met(), w);
  h_metphi->Fill(mevent->metphi(), w);
  /*
  for (int i = 0; i < 3; ++i) {
    h_nbtags[i]->Fill(mevent->nbtags(i), w);
    h_nbtags_v_bquark_code[i]->Fill(mevent->gen_flavor_code, mevent->nbtags(i), w);
  }
  */
  const int ibtag = 2; // tight only
  for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
    if (mevent->jet_pt[ijet] < mfv::min_jet_pt)
      continue;
    h_jet_bdisc->Fill(mevent->jet_bdisc[ijet], w);
    h_jet_bdisc_v_bquark_code->Fill(mevent->gen_flavor_code, mevent->jet_bdisc[ijet], w);
    if (mevent->is_btagged(ijet, ibtag)) {
      h_bjet_pt->Fill(mevent->jet_pt[ijet], w);
      h_bjet_eta->Fill(mevent->jet_eta[ijet], w);
      h_bjet_phi->Fill(mevent->jet_phi[ijet], w);
      h_bjet_energy->Fill(mevent->jet_energy[ijet], w);
      for (size_t jjet = ijet+1; jjet < mevent->jet_id.size(); ++jjet) {
        if (mevent->jet_pt[jjet] < mfv::min_jet_pt)
          continue;
        if (mevent->is_btagged(jjet, ibtag)) {
          h_bjet_pairdphi->Fill(reco::deltaPhi(mevent->jet_phi[ijet], mevent->jet_phi[jjet]), w);
          h_bjet_pairdeta->Fill(std::max(mevent->jet_eta[ijet], mevent->jet_eta[jjet]) - std::min(mevent->jet_eta[ijet], mevent->jet_eta[jjet]), w);
        }
      }
    }
  }

  //////////////////////////////////////////////////////////////////////////////

  const size_t n_vertex_seed_tracks = mevent->n_vertex_seed_tracks();
  h_n_vertex_seed_tracks->Fill(n_vertex_seed_tracks, w);
  for (size_t i = 0; i < n_vertex_seed_tracks; ++i) {
    h_vertex_seed_track_chi2dof->Fill(mevent->vertex_seed_track_chi2dof[i], w);
    h_vertex_seed_track_q->Fill(mevent->vertex_seed_track_q(i), w);
    h_vertex_seed_track_pt->Fill(mevent->vertex_seed_track_pt(i), w);
    h_vertex_seed_track_eta->Fill(mevent->vertex_seed_track_eta[i], w);
    h_vertex_seed_track_phi->Fill(mevent->vertex_seed_track_phi[i], w);
    h_vertex_seed_track_phi_v_eta->Fill(mevent->vertex_seed_track_eta[i], mevent->vertex_seed_track_phi[i], w);
    h_vertex_seed_track_dxy->Fill(mevent->vertex_seed_track_dxy[i], w);
    h_vertex_seed_track_dz->Fill(mevent->vertex_seed_track_dz[i], w);
    h_vertex_seed_track_err_pt->Fill(mevent->vertex_seed_track_err_pt[i] / mevent->vertex_seed_track_pt(i), w);
    h_vertex_seed_track_err_eta->Fill(mevent->vertex_seed_track_err_eta[i], w);
    h_vertex_seed_track_err_phi->Fill(mevent->vertex_seed_track_err_phi[i], w);
    h_vertex_seed_track_err_dxy->Fill(mevent->vertex_seed_track_err_dxy[i], w);
    h_vertex_seed_track_err_dz->Fill(mevent->vertex_seed_track_err_dz[i], w);
    h_vertex_seed_track_npxhits->Fill(mevent->vertex_seed_track_npxhits(i), w);
    h_vertex_seed_track_nsthits->Fill(mevent->vertex_seed_track_nsthits(i), w);
    h_vertex_seed_track_nhits->Fill(mevent->vertex_seed_track_nhits(i), w);
    h_vertex_seed_track_npxlayers->Fill(mevent->vertex_seed_track_npxlayers(i), w);
    h_vertex_seed_track_nstlayers->Fill(mevent->vertex_seed_track_nstlayers(i), w);
    h_vertex_seed_track_nlayers->Fill(mevent->vertex_seed_track_nlayers(i), w);
  }
}

DEFINE_FWK_MODULE(MFVEventHistos);
