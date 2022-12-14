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
  TH1F* h_gvtx_nbquarkjet_wcut;
  TH1F* h_gvtx_nloosebtaggedjet_wcut;
  TH1F* h_gvtx_nloosebtaggedjet_bboost_wcut;
  TH1F* h_gvtx_shared_loosebtaggedjet_or_not_bboost_wcut;
  
  // cut w/ b-quark pT > 25 GeV imposed 
  TH1F* h_gvtx_all_ntrack_from_jets_wcut;
  
  TH1F* h_gvtx_jet_seed_track_pT_from_jets_wcut;
  TH1F* h_gvtx_jet_seed_track_sigmadxybs_from_jets_wcut;
  TH1F* h_gvtx_jet_seed_track_npxlayers_from_jets_wcut;
  TH1F* h_gvtx_jet_seed_track_nstlayers_from_jets_wcut;
  TH1F* h_gvtx_jet_seed_track_rmin_from_jets_wcut;
  
  TH1F* h_gvtx_shared_bjet_or_not;
  TH1F* h_gvtx_shared_loosebtaggedjet_or_not;

  TH1F* h_gvtx_count_bquarks_match_to_loosebtaggedjet_wcut;
  TH1F* h_gvtx_shared_loosebtaggedjet_nm1_bquarkjet_or_not;
  TH1F* h_gvtx_no_shared_loosebtaggedjet_nm1_bquarkjet_or_not;
  TH1F* h_gvtx_no_matched_loosebtaggedjet_nm1_bquarkjet_or_not;
  TH1F* h_gvtx_shared_loosebtaggedjet_nm1_nbsv;
  TH1F* h_gvtx_no_shared_loosebtaggedjet_nm1_nbsv;
  TH1F* h_gvtx_no_matched_loosebtaggedjet_nm1_nbsv;
  TH1F* h_gvtx_shared_loosebtaggedjet_nm1_nloosebsv;
  TH1F* h_gvtx_no_shared_loosebtaggedjet_nm1_nloosebsv;
  TH1F* h_gvtx_no_matched_loosebtaggedjet_nm1_nloosebsv;
  TH2F* h_2D_gvtx_shared_loosebtaggedjet_nm1_ntrack_loosebsv;
  TH2F* h_2D_gvtx_no_shared_loosebtaggedjet_nm1_ntrack_loosebsv;
  TH2F* h_2D_gvtx_no_matched_loosebtaggedjet_nm1_ntrack_loosebsv;
  TH1F* h_gvtx_shared_loosebtaggedjet_nm1_genbvtxdist3d_loosebsv;  //expects two b-vertices 
  TH1F* h_gvtx_no_shared_loosebtaggedjet_nm1_genbvtxdist3d_loosebsv;  //expects one b-vertex 
  TH2F* h_2D_gvtx_shared_loosebtaggedjet_nm1_genbvtxdist3d_ntrack_loosebsv;  //expects two b-vertices 
  TH2F* h_2D_gvtx_no_shared_loosebtaggedjet_nm1_genbvtxdist3d_ntrack_loosebsv;  //expects one b-vertex 
  TH1F* h_gvtx_shared_loosebtaggedjet_nm1_pT_ratio_loosebsv;
  TH1F* h_gvtx_no_shared_loosebtaggedjet_nm1_pT_ratio_loosebsv;
  TH1F* h_gvtx_shared_loosebtaggedjet_nm1_jet_pT;
  TH1F* h_gvtx_shared_loosebtaggedjet_nm1_dist3d_bpair;
  TH1F* h_gvtx_shared_loosebtaggedjet_nm1_bigdist3d_bpair;
  TH1F* h_gvtx_no_shared_loosebtaggedjet_nm1_jet_pT;
  TH1F* h_gvtx_no_matched_loosebtaggedjet_nm1_jet_pT;

  TH1F* h_gvtx_nm1_nsigmadxy_seed_tracks_per_no_shared_jet;
  TH1F* h_gvtx_nm1_nsigmadxy_seed_tracks_per_no_matched_jet;
  TH1F* h_gvtx_nm1_nsigmadxy_seed_tracks_per_shared_jet;

  TH1F* h_gvtx_seed_tracks_per_no_shared_jet;
  TH1F* h_gvtx_seed_tracks_per_no_matched_jet;
  TH1F* h_gvtx_seed_tracks_per_shared_jet;

  TH1F* h_gvtx_nm1_pT_seed_tracks_per_no_shared_jet;
  TH1F* h_gvtx_nm1_pT_seed_tracks_per_no_matched_jet;
  TH1F* h_gvtx_nm1_pT_seed_tracks_per_shared_jet;

  
  TH1F* h_gvtx_is_tight_btag_per_bjet_or_not_wcut;
  TH1F* h_gvtx_is_medium_btag_per_bjet_or_not_wcut;
  TH1F* h_gvtx_is_loose_btag_per_bjet_or_not_wcut;
  
  TH1F* h_gvtx_sv_bquark_dist3d_wcut;
 
  //track investigation 
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
  h_gvtx_nloosebtaggedjet_bboost_wcut = fs->make<TH1F>("h_gvtx_nloosebtaggedjet_bboost_wcut", "all four b-decays;# of loose-btagged jets;events/1", 20, 0, 20);
  h_gvtx_shared_loosebtaggedjet_or_not_bboost_wcut = fs->make<TH1F>("h_gvtx_shared_loosebtaggedjet_or_not_bboost_wcut", "all four b-decays; shared loose-btagged-jets ?; arb. units", 3, 0, 3);
  h_n_gen_bvtx = fs->make<TH1F>("h_n_gen_bvtx", ";# of GEN b-vertices (from non-b hadrons); events/1", 40, 0, 40);
  h_gvtx_njet = fs->make<TH1F>("h_gvtx_njet", ";# of jets;events/1", 10, 0, 10);
  h_gvtx_nbquarkjet_wcut = fs->make<TH1F>("h_gvtx_nbquarkjet_wcut", "1-1 matched jet to b-decay;# of b-quark jets;events/1", 10, 0, 10);
  h_gvtx_nloosebtaggedjet_wcut = fs->make<TH1F>("h_gvtx_nloosebtaggedjet_wcut", "1-1 matched jet to b-decay;# of loose-btagged jets;events/1", 10, 0, 10);

  h_gvtx_all_ntrack_from_jets_wcut = fs->make<TH1F>("h_gvtx_all_ntrack_from_jets_wcut", "1-1 matched jet to b-decay;# of tracks per a matched jet;", 50, 0, 50);
  
  h_gvtx_jet_seed_track_pT_from_jets_wcut = fs->make<TH1F>("h_gvtx_jet_seed_track_pT_from_jets_wcut", "1-1 matched jet to b-decay;p_{T} of a seed track in a matched jet;", 20, 0, 10);
  h_gvtx_jet_seed_track_sigmadxybs_from_jets_wcut = fs->make<TH1F>("h_gvtx_jet_seed_track_sigmadxybs_from_jets_wcut", "1-1 matched jet to b-decay;#sigma_{dxy} of a seed track in a matched jet;", 40, -10, 10);
  h_gvtx_jet_seed_track_npxlayers_from_jets_wcut = fs->make<TH1F>("h_gvtx_jet_seed_track_npxlayers_from_jets_wcut", "1-1 matched jet to b-decay;npxlayers of a seed track in a matched jet;", 12, 0, 12);
  h_gvtx_jet_seed_track_nstlayers_from_jets_wcut = fs->make<TH1F>("h_gvtx_jet_seed_track_nstlayers_from_jets_wcut", "1-1 matched jet to b-decay;nstlayers of a seed track in a matched jet;", 28, 0, 28);
  h_gvtx_jet_seed_track_rmin_from_jets_wcut = fs->make<TH1F>("h_gvtx_jet_seed_track_rmin_from_jets_wcut", "1-1 matched jet to b-decay;r_{min} of a seed track in a matched jet;", 5, 0, 5);
  
  h_gvtx_shared_bjet_or_not = fs->make<TH1F>("h_gvtx_shared_bjet_or_not", "; shared b-jets ?; arb. units", 3, 0, 3);
  h_gvtx_shared_loosebtaggedjet_or_not = fs->make<TH1F>("h_gvtx_shared_loosebtaggedjet_or_not", "; shared loose-btagged-jets ?; arb. units", 3, 0, 3);
  h_gvtx_count_bquarks_match_to_loosebtaggedjet_wcut = fs->make<TH1F>("h_gvtx_count_bquarks_match_to_loosebtaggedjet_wcut", "; # of b-quarks matched to a loose-btagged jet; arb. units", 6, 0, 6);

  h_gvtx_shared_loosebtaggedjet_nm1_bquarkjet_or_not = fs->make<TH1F>("h_gvtx_shared_loosebtaggedjet_nm1_bquarkjet_or_not", "a loose-btagged jet is matched by at least two b-quarks; also the closest jet to a b-quark?; arb. units", 3, 0, 3);
  h_gvtx_no_shared_loosebtaggedjet_nm1_bquarkjet_or_not = fs->make<TH1F>("h_gvtx_no_shared_loosebtaggedjet_nm1_bquarkjet_or_not", "a loose-btagged jet is matched by only one b-quark; also the closest jet to a b-quark?; arb. units", 3, 0, 3);
  h_gvtx_no_matched_loosebtaggedjet_nm1_bquarkjet_or_not = fs->make<TH1F>("h_gvtx_no_matched_loosebtaggedjet_nm1_bquarkjet_or_not", "a loose-btagged jet is not matched by any b-quarks; also the closest jet to a b-quark?; arb. units", 3, 0, 3);
  h_gvtx_shared_loosebtaggedjet_nm1_nbsv = fs->make<TH1F>("h_gvtx_shared_loosebtaggedjet_nm1_nbsv", "a loose-btagged jet is matched by at least two b-quarks; # of SVs with all tracks in a loose-btagged jet (bSVs); arb. units", 10, 0, 10);
  h_gvtx_no_shared_loosebtaggedjet_nm1_nbsv = fs->make<TH1F>("h_gvtx_no_shared_loosebtaggedjet_nm1_nbsv", "a loose-btagged jet is matched by only one b-quark; # of SVs with all tracks in a loose-btagged jet (bSVs); arb. units", 10, 0, 10);
  h_gvtx_no_matched_loosebtaggedjet_nm1_nbsv = fs->make<TH1F>("h_gvtx_no_matched_loosebtaggedjet_nm1_nbsv", "a loose-btagged jet is not matched by any b-quarks; # of SVs with all tracks in a loose-btagged jet (bSVs); arb. units", 10, 0, 10);
  h_gvtx_shared_loosebtaggedjet_nm1_nloosebsv = fs->make<TH1F>("h_gvtx_shared_loosebtaggedjet_nm1_nloosebsv", "a loose-btagged jet is matched by at least two b-quarks; # of SVs with some tracks in a loose-btagged jet (loose-bSVs); arb. units", 10, 0, 10);
  h_gvtx_no_shared_loosebtaggedjet_nm1_nloosebsv = fs->make<TH1F>("h_gvtx_no_shared_loosebtaggedjet_nm1_nloosebsv", "a loose-btagged jet is matched by only one b-quark; # of SVs with some tracks in a loose-btagged jet (loose-bSVs); arb. units", 10, 0, 10);
  h_gvtx_no_matched_loosebtaggedjet_nm1_nloosebsv = fs->make<TH1F>("h_gvtx_no_matched_loosebtaggedjet_nm1_nloosebsv", "a loose-btagged jet is not matched by any b-quarks; # of SVs with some tracks in a loose-btagged jet (loose-bSVs); arb. units", 10, 0, 10);
  h_2D_gvtx_shared_loosebtaggedjet_nm1_ntrack_loosebsv = fs->make<TH2F>("h_2D_gvtx_shared_loosebtaggedjet_nm1_ntrack_loosebsv", "a loose-btagged jet is matched by at least two b-quarks; # of seed tracks / a loose-bSV; # of a loose-bSV's seed tracks in a loose-btagged jet; arb. units", 50, 0, 50, 50, 0, 50);
  h_2D_gvtx_no_shared_loosebtaggedjet_nm1_ntrack_loosebsv = fs->make<TH2F>("h_2D_gvtx_no_shared_loosebtaggedjet_nm1_ntrack_loosebsv", "a loose-btagged jet is matched by only one b-quark; # of seed tracks / a loose-bSV; # of a loose-bSV's seed tracks in a loose-btagged jet; arb. units", 50, 0, 50, 50, 0, 50);
  h_2D_gvtx_no_matched_loosebtaggedjet_nm1_ntrack_loosebsv = fs->make<TH2F>("h_2D_gvtx_no_matched_loosebtaggedjet_nm1_ntrack_loosebsv", "a loose-btagged jet is not matched by any b-quarks; # of seed tracks / a loose-bSV; # of a loose-bSV's seed tracks in a loose-btagged jet; arb. units", 50, 0, 50, 50, 0, 50);
  h_gvtx_shared_loosebtaggedjet_nm1_genbvtxdist3d_loosebsv = fs->make<TH1F>("h_gvtx_shared_loosebtaggedjet_nm1_genbvtxdist3d_loosebsv", "a loose-btagged jet is matched by at least two b-quarks; closest dist3d to a GEN b-vtx and a loose-bSV (cm.); arb. units", 120, 0, 3);
  h_gvtx_no_shared_loosebtaggedjet_nm1_genbvtxdist3d_loosebsv = fs->make<TH1F>("h_gvtx_no_shared_loosebtaggedjet_nm1_genbvtxdist3d_loosebsv", "a loose-btagged jet is matched by only one b-quark; closest dist3d to a GEN b-vtx and a loose-bSV (cm.); arb. units", 120, 0, 3);
  h_2D_gvtx_shared_loosebtaggedjet_nm1_genbvtxdist3d_ntrack_loosebsv = fs->make<TH2F>("h_2D_gvtx_shared_loosebtaggedjet_nm1_genbvtxdist3d_ntrack_loosebsv", "a loose-btagged jet is matched by at least two b-quarks; closest dist3d to a GEN b-vtx and a loose-bSV (cm.); # of a loose-bSV's seed tracks; arb. units", 120, 0, 3, 50, 0, 50);
  h_2D_gvtx_no_shared_loosebtaggedjet_nm1_genbvtxdist3d_ntrack_loosebsv = fs->make<TH2F>("h_2D_gvtx_no_shared_loosebtaggedjet_nm1_genbvtxdist3d_ntrack_loosebsv", "a loose-btagged jet is matched by only one b-quark; closest dist3d to a GEN b-vtx and a loose-bSV (cm.); # of a loose-bSV's seed tracks; arb. units", 120, 0, 3, 50, 0, 50);
  h_gvtx_shared_loosebtaggedjet_nm1_pT_ratio_loosebsv = fs->make<TH1F>("h_gvtx_shared_loosebtaggedjet_nm1_pT_ratio_loosebsv", "a loose-btagged jet is matched by at least two b-quarks; #frac{a b-jet pT}{sum of >=2 b-quarks pT}; arb. units", 120, 0, 2);
  h_gvtx_no_shared_loosebtaggedjet_nm1_pT_ratio_loosebsv = fs->make<TH1F>("h_gvtx_no_shared_loosebtaggedjet_nm1_pT_ratio", "a loose-btagged jet is matched by only one b-quark; #frac{a b-jet pT}{sum of a b-quark pT}; arb. units", 120, 0, 2);
  h_gvtx_shared_loosebtaggedjet_nm1_jet_pT = fs->make<TH1F>("h_gvtx_shared_loosebtaggedjet_nm1_jet_pT", "a loose-btagged jet is matched by at least two b-quarks; a b-jet pT; arb. units", 75, 0, 150);
  h_gvtx_shared_loosebtaggedjet_nm1_dist3d_bpair = fs->make<TH1F>("h_gvtx_shared_loosebtaggedjet_nm1_dist3d_bpair", "a loose-btagged jet is matched by at least two b-quarks; a dist3d between b-quarks from the same llp; arb. units", 120, 0, 3.0);
  h_gvtx_shared_loosebtaggedjet_nm1_bigdist3d_bpair = fs->make<TH1F>("h_gvtx_shared_loosebtaggedjet_nm1_bigdist3d_bpair", "a loose-btagged jet is matched by at least two b-quarks; a dist3d between b-quarks from the same llp; arb. units", 100, 0, 0.5);
  h_gvtx_no_shared_loosebtaggedjet_nm1_jet_pT = fs->make<TH1F>("h_gvtx_no_shared_loosebtaggedjet_nm1_jet_pT", "a loose-btagged jet is matched by only one b-quark; a b-jet pT; arb. units", 75, 0, 150);
  h_gvtx_no_matched_loosebtaggedjet_nm1_jet_pT = fs->make<TH1F>("h_gvtx_no_matched_loosebtaggedjet_nm1_jet_pT", "a loose-btagged jet is not matched by any b-quark; a b-jet pT; arb. units", 75, 0, 150);

  
  h_gvtx_nm1_nsigmadxy_seed_tracks_per_no_shared_jet = fs->make<TH1F>("h_gvtx_nm1_nsigmadxy_seed_tracks_per_no_shared_jet", ";# of n-nsigmadxy seed tracks per a loose-btagged jet matched w/ a b-quark;", 50, 0, 50);
  h_gvtx_nm1_nsigmadxy_seed_tracks_per_no_matched_jet = fs->make<TH1F>("h_gvtx_nm1_nsigmadxy_seed_tracks_per_no_matched_jet", ";# of n-nsigmadxy seed tracks per a loose-btagged w/ no matched b-quark;", 50, 0, 50);
  h_gvtx_nm1_nsigmadxy_seed_tracks_per_shared_jet = fs->make<TH1F>("h_gvtx_nm1_nsigmadxy_seed_tracks_per_shared_jet", ";# of n-nsigmadxy seed tracks per a loose-btagged jet matched w/ >=2 b-quarks;", 50, 0, 50);
  h_gvtx_seed_tracks_per_no_shared_jet = fs->make<TH1F>("h_gvtx_seed_tracks_per_no_shared_jet", ";# of seed tracks per a loose-btagged jet matched w/ a b-quark;", 50, 0, 50);
  h_gvtx_seed_tracks_per_no_matched_jet = fs->make<TH1F>("h_gvtx_seed_tracks_per_no_matched_jet", ";# of seed tracks per a loose-btagged jet w/ no matched b-quark;", 50, 0, 50);
  h_gvtx_seed_tracks_per_shared_jet = fs->make<TH1F>("h_gvtx_seed_tracks_per_shared_jet", ";# of seed tracks per a loose-btagged jet matched w/ >= 2 b-quarks;", 50, 0, 50);
  h_gvtx_nm1_pT_seed_tracks_per_no_shared_jet = fs->make<TH1F>("h_gvtx_nm1_pT_seed_tracks_per_no_shared_jet", ";# of n-pT seed tracks per a loose-btagged jet matched w/ a b-quark;", 50, 0, 50);
  h_gvtx_nm1_pT_seed_tracks_per_no_matched_jet = fs->make<TH1F>("h_gvtx_nm1_pT_seed_tracks_per_no_matched_jet", ";# of n-pT seed tracks per a loose-btagged jet matched w/ no matched b-quark;", 50, 0, 50);
  h_gvtx_nm1_pT_seed_tracks_per_shared_jet = fs->make<TH1F>("h_gvtx_nm1_pT_seed_tracks_per_shared_jet", ";# of n-pT seed tracks per a loose-btagged jet matched w/ >=2 b-quarks;", 50, 0, 50);
  
  h_gvtx_sv_bquark_dist3d_wcut = fs->make<TH1F>("h_gvtx_sv_bquark_dist3d_wcut", ";dist3d b/w a GEN b-quark decay vtx and its closest >=3trk SV (cm); arb. units", 50, 0, 0.1);
  h_gvtx_is_tight_btag_per_bjet_or_not_wcut = fs->make<TH1F>("h_gvtx_is_tight_btag_per_bjet_or_not_wcut", "1-1 matched jet to b-decay; is this b-jet also tight b-tagged ?; arb. units", 3, 0, 3);
  h_gvtx_is_medium_btag_per_bjet_or_not_wcut = fs->make<TH1F>("h_gvtx_is_medium_btag_per_bjet_or_not_wcut", "1-1 matched jet to b-decay; is this b-jet also medium b-tagged ?; arb. units", 3, 0, 3);
  h_gvtx_is_loose_btag_per_bjet_or_not_wcut = fs->make<TH1F>("h_gvtx_is_loose_btag_per_bjet_or_not_wcut", "1-1 matched jet to b-decay; is this b-jet also loose b-tagged ?; arb. units", 3, 0, 3);
  
  //track investigation 
  h_gvtx_all_track_pt_from_jets_wcut = fs->make<TH1F>("h_gvtx_all_track_pt_from_jets_wcut", "1-1 matched jet to b-decay; track p_{T} (GeV)", 20, 0, 10);
  h_gvtx_all_track_sigmadxybs_from_jets_wcut = fs->make<TH1F>("h_gvtx_all_track_sigmadxybs_from_jets_wcut", "1-1 matched jet to b-decay; #sigma_{dxy}", 40, -10, 10);
  h_gvtx_all_track_npxhits_from_jets_wcut = fs->make<TH1F>("h_gvtx_all_track_npxhits_from_jets_wcut", "1-1 matched jet to b-decay; npxhits", 12, 0, 12);
  h_gvtx_all_track_nsthits_from_jets_wcut = fs->make<TH1F>("h_gvtx_all_track_nsthits_from_jets_wcut", "1-1 matched jet to b-decay; nsthits", 28, 0, 28);
  h_gvtx_all_track_npxlayers_from_jets_wcut = fs->make<TH1F>("h_gvtx_all_track_npxlayers_from_jets_wcut", "1-1 matched jet to b-decay; npxlayers", 12, 0, 12);
  h_gvtx_all_track_nstlayers_from_jets_wcut = fs->make<TH1F>("h_gvtx_all_track_nstlayers_from_jets_wcut", "1-1 matched jet to b-decay; nstlayers", 28, 0, 28);
  h_gvtx_all_track_rmin_from_jets_wcut = fs->make<TH1F>("h_gvtx_all_track_rmin_from_jets_wcut", "1-1 matched jet to b-decay;r_{min};", 5, 0, 5);

  h_gvtx_jet_seed_nm1_pt_from_jets_wcut = fs->make<TH1F>("h_gvtx_jet_seed_nm1_pt_from_jets_wcut", "1-1 matched jet to b-decay; track p_{T} (GeV) w/ n-1 cuts applied", 20, 0, 10);
  h_gvtx_jet_seed_nm1_npxlayers_from_jets_wcut = fs->make<TH1F>("h_gvtx_jet_seed_nm1_npxlayers_from_jets_wcut", "1-1 matched jet to b-decay; npxlayers w/ n-1 cuts applied", 12, 0, 12);
  h_gvtx_jet_seed_nm1_nstlayers_from_jets_wcut = fs->make<TH1F>("h_gvtx_jet_seed_nm1_nstlayers_from_jets_wcut", "1-1 matched jet to b-decay; nstlayers w/ n-1 cuts applied", 28, 0, 28);
  h_gvtx_jet_seed_nm1_rmin_from_jets_wcut = fs->make<TH1F>("h_gvtx_jet_seed_nm1_rmin_from_jets_wcut", "1-1 matched jet to b-decay; rmin w/ n-1 cuts applied", 5, 0, 5);
  h_gvtx_jet_seed_nm1_sigmadxybs_from_jets_wcut = fs->make<TH1F>("h_gvtx_jet_seed_nm1_sigmadxybs_from_jets_wcut", "1-1 matched jet to b-decay; #sigma_{dxy} w/ n-1 cuts applied", 40, -10, 10);


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
	  h_gvtx_nsv->Fill(nsv, w);
	  if (nsv > 0) {
		  h_gvtx_njet->Fill(mevent->njets(20), w);
		  for (int i = 0; i < 3; ++i) {
			  h_nbtags[i]->Fill(mevent->nbtags(i), w);
			  h_nbtags_v_bquark_code[i]->Fill(mevent->gen_flavor_code, mevent->nbtags(i), w);
		  }


		  size_t shared_bjet = 0;
		  size_t shared_loosebtaggedjet = 0;
		  
		  bool all_bboost = true;
		  std::vector<size_t> vec_lowpT_bquark = {};
		  
		  std::vector<size_t> vec_bquark_jet = {};
		  std::vector<size_t> vec_bquark_jet_no_duplicate = {};
		  std::vector<size_t> vec_loosebtagged_jet_no_duplicate = {};
		  
		  std::vector<size_t> vec_no_shared_loosebtaggedjet_nm1_dxy_or_not = {};
		  std::vector<size_t> vec_shared_loosebtaggedjet_nm1_dxy_or_not = {};

		  std::vector<size_t> vec_no_shared_loosebtaggedjet_nm1_pT_or_not = {};
		  std::vector<size_t> vec_shared_loosebtaggedjet_nm1_pT_or_not = {};
		  
		  std::vector<size_t> vec_bquark_idx_bsv = {};
		  
		  for (size_t i = 0; i < 4; ++i) {
              if (mevent->gen_daughters[i].Pt() < 0) {
				  all_bboost = false;
				  vec_lowpT_bquark.push_back(i);
				  continue;
			  }

			  double mindR_bquark = 4.0;
			  size_t bquark_jet = 0;
			  for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
				  if (mevent->jet_pt[ijet] < 20.0)  // Jets have a cut at 20 GeV
					  continue;
				  
				  if (reco::deltaR(mevent->jet_eta[ijet], mevent->jet_phi[ijet], mevent->gen_daughters[i].Eta(), mevent->gen_daughters[i].Phi()) < mindR_bquark) {
					  mindR_bquark = reco::deltaR(mevent->jet_eta[ijet], mevent->jet_phi[ijet], mevent->gen_daughters[i].Eta(), mevent->gen_daughters[i].Phi());
					  bquark_jet = ijet;
				  }


			  }

			  // condition we have found a GEN bjet matching with a b-quark 
			  if (mindR_bquark < 0.4) {

				  
				  vec_bquark_jet.push_back(bquark_jet);
				  vec_bquark_jet_no_duplicate.push_back(bquark_jet);
				  if (std::count(vec_bquark_jet.begin(), vec_bquark_jet.end(), bquark_jet) == 2) {
					  shared_bjet = 1;
					  vec_bquark_jet_no_duplicate.pop_back();
				  }

				 
				  double mindR_dau = 0.4;
				  for (size_t j = 0; j < mevent->gen_bchain_nonb_had_eta[i].size(); ++j) {
					  double dR_dau = reco::deltaR(mevent->gen_bchain_nonb_had_eta[i][j], mevent->gen_bchain_nonb_had_phi[i][j], mevent->jet_eta[bquark_jet], mevent->jet_phi[bquark_jet]);
					  if (dR_dau < mindR_dau) {
						  mindR_dau = dR_dau;
					  }
				  }

				  
				  size_t jet_all_ntrack = 0;
				  size_t jet_seed_ntrack = 0;
				  
				  for (size_t j = 0; j < mevent->jet_track_which_jet.size(); ++j) {
					  if (bquark_jet == mevent->jet_track_which_jet[j]) {
						  jet_all_ntrack++;
						  h_gvtx_all_track_pt_from_jets_wcut->Fill(mevent->jet_track_pt(j), w);
						  h_gvtx_all_track_sigmadxybs_from_jets_wcut->Fill(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j], w);
						  h_gvtx_all_track_npxhits_from_jets_wcut->Fill(mevent->jet_track_npxhits(j), w);
						  h_gvtx_all_track_nsthits_from_jets_wcut->Fill(mevent->jet_track_nsthits(j), w);
						  h_gvtx_all_track_npxlayers_from_jets_wcut->Fill(mevent->jet_track_npxlayers(j), w);
						  h_gvtx_all_track_nstlayers_from_jets_wcut->Fill(mevent->jet_track_nstlayers(j), w);
						  h_gvtx_all_track_rmin_from_jets_wcut->Fill(mevent->jet_track_hp_rmin[j], w);
						  
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

						  
										  
						  if (fabs(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j]) > 4) {
							  jet_seed_ntrack++;
							  h_gvtx_jet_seed_track_pT_from_jets_wcut->Fill(mevent->jet_track_pt(j), w);
							  h_gvtx_jet_seed_track_sigmadxybs_from_jets_wcut->Fill(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j], w);
							  h_gvtx_jet_seed_track_npxlayers_from_jets_wcut->Fill(mevent->jet_track_npxlayers(j), w);
						      h_gvtx_jet_seed_track_nstlayers_from_jets_wcut->Fill(mevent->jet_track_nstlayers(j), w);
							  h_gvtx_jet_seed_track_rmin_from_jets_wcut->Fill(mevent->jet_track_hp_rmin[j], w);			  
						  }
									  
								  
							  
						  

					  }
				  }

				  
				  h_gvtx_is_tight_btag_per_bjet_or_not_wcut->Fill(mevent->is_btagged(bquark_jet, 2), w);
				  h_gvtx_is_medium_btag_per_bjet_or_not_wcut->Fill(mevent->is_btagged(bquark_jet, 1), w);
				  h_gvtx_is_loose_btag_per_bjet_or_not_wcut->Fill(mevent->is_btagged(bquark_jet, 0), w);


				  if (jet_all_ntrack > 0)
					  h_gvtx_all_ntrack_from_jets_wcut->Fill(jet_all_ntrack, w);
				  
			  }
			  
			  // trying to get a resolution of 3d distance b/w GEN b-decay vertex and reconstructed vertex 
			  double min_sv_dist3d_bvtx = 0.3;
			  //size_t idx_bsv = 99;
			  for (int isv = 0; isv < nsv; ++isv) {
				  //if (std::count(vec_bquark_idx_bsv.begin(), vec_bquark_idx_bsv.end(), isv) == 1)
				  //	  continue;
				  const MFVVertexAux& aux = auxes->at(isv);
				  if (aux.ntracks() >= 3) {
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
						  //idx_bsv = isv;
						  min_sv_dist3d_bvtx = dR_b_sv_dist3d;
					  }
				  }
			  }
			  
			  //vec_bquark_idx_bsv.push_back(idx_bsv);
			  if (min_sv_dist3d_bvtx < 0.3)
			      h_gvtx_sv_bquark_dist3d_wcut->Fill(min_sv_dist3d_bvtx, w);
			  


		  }

		  h_gvtx_nbquarkjet_wcut->Fill(vec_bquark_jet_no_duplicate.size(), w);
		  
		  // no cuts on GEN-level are applied, looking at all loose-btagged jets  
		  for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
			  if (mevent->jet_pt[ijet] < 20.0)  // Jets have a cut at 20 GeV
				  continue;


			  if (mevent->is_btagged(ijet, 0)) {

				  std::vector<size_t> vec_isv_btag0_jet = {};
				  size_t jet_seed_ntrack = 0;
				  size_t jet_nm1_nsigmadxy_seed_ntrack = 0;
				  size_t jet_nm1_pT_seed_ntrack = 0;
				  for (size_t j = 0; j < mevent->jet_track_which_jet.size(); ++j) {
					  if (ijet == mevent->jet_track_which_jet[j]) {
						  if (mevent->jet_track_npxlayers(j) > 1 && mevent->jet_track_nstlayers(j) > 5 && mevent->jet_track_pt(j) > 1 && mevent->jet_track_hp_rmin[j] == 1) {
							  jet_nm1_nsigmadxy_seed_ntrack++;
							  if (fabs(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j]) > 4) {
								  jet_seed_ntrack++;

								  for (int isv = 0; isv < nsv; ++isv) {

									  const MFVVertexAux& aux = auxes->at(isv);

									  for (int itk = 0; itk < aux.ntracks(); ++itk) {


										  if (fabs(aux.track_pt(itk) - fabs(mevent->jet_track_qpt[j])) < 0.0001 &&
											  fabs(aux.track_eta[itk] - mevent->jet_track_eta[j]) < 0.0001 &&
											  fabs(aux.track_phi[itk] - mevent->jet_track_phi[j]) < 0.0001) {
											  vec_isv_btag0_jet.push_back(isv);
										  }
									  }

								  }

							  }
						  }

						  if (mevent->jet_track_npxlayers(j) > 1 && mevent->jet_track_nstlayers(j) > 5 && mevent->jet_track_pt(j) > 0.5 && fabs(mevent->jet_track_dxy[j] / mevent->jet_track_dxy_err[j]) > 4 && mevent->jet_track_hp_rmin[j] == 1) {
							  jet_nm1_pT_seed_ntrack++;
						  }


					  }
				  }

				  int nbsv_by_btag0_jet = 0;
				  int nloosebsv_by_btag0_jet = 0;
				  std::vector<int> vec_ntrack_loosebsv = {};
				  std::vector<size_t> vec_jet_seedtrack_loosebsv = {};
				  std::vector<size_t> vec_jet_idx_loosebsv = {};
				  std::vector<size_t> vec_jet_idx_matched_genbvtx = {};

				  for (int isv = 0; isv < nsv; ++isv) {
					  const MFVVertexAux& aux = auxes->at(isv);
					  int jet_seed_ntrack_from_trk_bsv = std::count(vec_isv_btag0_jet.begin(), vec_isv_btag0_jet.end(), isv);
					  if (jet_seed_ntrack_from_trk_bsv == aux.ntracks()) {
						  nbsv_by_btag0_jet++;
					  }
					  if (jet_seed_ntrack_from_trk_bsv >= 1) {
						  nloosebsv_by_btag0_jet++;
						  vec_ntrack_loosebsv.push_back(aux.ntracks());
						  vec_jet_seedtrack_loosebsv.push_back(jet_seed_ntrack_from_trk_bsv);
						  vec_jet_idx_loosebsv.push_back(isv);
					  }
					  

				  }

				  // ***with nonzero # of relaxed seed tracks by nsigmadxy cut
				  if (jet_nm1_nsigmadxy_seed_ntrack > 1) {

					  bool is_two_b_decay_jet = false;
					  double sum_b_quark_pT = 0.0;
					  std::vector<double> vec_b_pair_dist3d = {};
					  int count_bquark_match = 0;
					  size_t i = 0;
					  for (size_t llp = 0; llp < 2; ++llp) {
					     int count_match = 0;
					     for (size_t b = 0; b < 2; ++b) {

						    if (reco::deltaR(mevent->jet_eta[ijet], mevent->jet_phi[ijet], mevent->gen_daughters[i].Eta(), mevent->gen_daughters[i].Phi()) < 0.4) {
							  count_match++;
							  count_bquark_match++;
							  sum_b_quark_pT += mevent->gen_daughters[i].Pt();
							  vec_jet_idx_matched_genbvtx.push_back(i);
							  if (std::count(vec_loosebtagged_jet_no_duplicate.begin(), vec_loosebtagged_jet_no_duplicate.end(), ijet) == 0) {
								  vec_loosebtagged_jet_no_duplicate.push_back(ijet);
							  }

						    }
						    i++;
                         }
						 if (count_match == 2) {  // a jet considered as a two-b-decay jet has exactly two b-quarks matched
							 is_two_b_decay_jet = true;
							 if (llp == 0) {
								 h_gvtx_shared_loosebtaggedjet_nm1_dist3d_bpair->Fill(sqrt(pow(mevent->gen_b_llp0_decay[0] - mevent->gen_b_llp0_decay[3], 2) + pow(mevent->gen_b_llp0_decay[1] - mevent->gen_b_llp0_decay[4], 2) + pow(mevent->gen_b_llp0_decay[2] - mevent->gen_b_llp0_decay[5], 2)));
								 h_gvtx_shared_loosebtaggedjet_nm1_bigdist3d_bpair->Fill(sqrt(pow(mevent->gen_b_llp0_decay[0] - mevent->gen_b_llp0_decay[3], 2) + pow(mevent->gen_b_llp0_decay[1] - mevent->gen_b_llp0_decay[4], 2) + pow(mevent->gen_b_llp0_decay[2] - mevent->gen_b_llp0_decay[5], 2)));
							 }
							 else {
								 h_gvtx_shared_loosebtaggedjet_nm1_dist3d_bpair->Fill(sqrt(pow(mevent->gen_b_llp1_decay[0] - mevent->gen_b_llp1_decay[3], 2) + pow(mevent->gen_b_llp1_decay[1] - mevent->gen_b_llp1_decay[4], 2) + pow(mevent->gen_b_llp1_decay[2] - mevent->gen_b_llp1_decay[5], 2)));
								 h_gvtx_shared_loosebtaggedjet_nm1_bigdist3d_bpair->Fill(sqrt(pow(mevent->gen_b_llp1_decay[0] - mevent->gen_b_llp1_decay[3], 2) + pow(mevent->gen_b_llp1_decay[1] - mevent->gen_b_llp1_decay[4], 2) + pow(mevent->gen_b_llp1_decay[2] - mevent->gen_b_llp1_decay[5], 2)));
							 }
						 }
					  }
				  
					  h_gvtx_count_bquarks_match_to_loosebtaggedjet_wcut->Fill(count_bquark_match);

					  
					  
					  if (is_two_b_decay_jet) {
						  shared_loosebtaggedjet = 1;
						  h_gvtx_seed_tracks_per_shared_jet->Fill(jet_seed_ntrack, w);
						  h_gvtx_nm1_nsigmadxy_seed_tracks_per_shared_jet->Fill(jet_nm1_nsigmadxy_seed_ntrack, w);
						  h_gvtx_nm1_pT_seed_tracks_per_shared_jet->Fill(jet_nm1_pT_seed_ntrack, w);

						  if (jet_nm1_nsigmadxy_seed_ntrack >= 5) {
							  vec_shared_loosebtaggedjet_nm1_dxy_or_not.push_back(0);
						  }

						  if (jet_nm1_pT_seed_ntrack >= 5) {
							  vec_shared_loosebtaggedjet_nm1_pT_or_not.push_back(0);
						  }

						  if (jet_seed_ntrack >= 5) {
							  vec_shared_loosebtaggedjet_nm1_dxy_or_not.push_back(1);
						  }

						  h_gvtx_shared_loosebtaggedjet_nm1_nbsv->Fill(nbsv_by_btag0_jet, w);
						  h_gvtx_shared_loosebtaggedjet_nm1_nloosebsv->Fill(nloosebsv_by_btag0_jet, w);
						  h_gvtx_shared_loosebtaggedjet_nm1_pT_ratio_loosebsv->Fill(mevent->jet_pt[ijet] / sum_b_quark_pT, w);
						  h_gvtx_shared_loosebtaggedjet_nm1_jet_pT->Fill(mevent->jet_pt[ijet], w);

						  for (size_t i = 0; i < vec_ntrack_loosebsv.size(); ++i) {
							  h_2D_gvtx_shared_loosebtaggedjet_nm1_ntrack_loosebsv->Fill(vec_ntrack_loosebsv[i], vec_jet_seedtrack_loosebsv[i], w);
							  double min_genbvtxdist3d = 5.0;
							  size_t isv = vec_jet_idx_loosebsv[i];
							  const MFVVertexAux& aux = auxes->at(isv);
							  
							  for (size_t j = 0; j < vec_jet_idx_matched_genbvtx.size(); ++j) {
								  double genbvtxdist3d = 0.0;
								  if (vec_jet_idx_matched_genbvtx[j] == 0) {
									  genbvtxdist3d = sqrt(pow(mevent->gen_b_llp0_decay[0] - aux.x, 2) + pow(mevent->gen_b_llp0_decay[1] - aux.y, 2) + pow(mevent->gen_b_llp0_decay[2] - aux.z, 2));
								  }
								  else if (vec_jet_idx_matched_genbvtx[j] == 1) {
									  genbvtxdist3d = sqrt(pow(mevent->gen_b_llp0_decay[3] - aux.x, 2) + pow(mevent->gen_b_llp0_decay[4] - aux.y, 2) + pow(mevent->gen_b_llp0_decay[5] - aux.z, 2));
								  }
								  else if (vec_jet_idx_matched_genbvtx[j] == 2) {
									  genbvtxdist3d = sqrt(pow(mevent->gen_b_llp1_decay[0] - aux.x, 2) + pow(mevent->gen_b_llp1_decay[1] - aux.y, 2) + pow(mevent->gen_b_llp1_decay[2] - aux.z, 2));
								  }
								  else {
									  genbvtxdist3d = sqrt(pow(mevent->gen_b_llp1_decay[3] - aux.x, 2) + pow(mevent->gen_b_llp1_decay[4] - aux.y, 2) + pow(mevent->gen_b_llp1_decay[5] - aux.z, 2));
								  }
								  if (min_genbvtxdist3d > genbvtxdist3d)
									  min_genbvtxdist3d = genbvtxdist3d;
							  }
							  h_gvtx_shared_loosebtaggedjet_nm1_genbvtxdist3d_loosebsv->Fill(min_genbvtxdist3d, w);
							  h_2D_gvtx_shared_loosebtaggedjet_nm1_genbvtxdist3d_ntrack_loosebsv->Fill(min_genbvtxdist3d, vec_ntrack_loosebsv[i], w);
						  }

						  if (std::count(vec_bquark_jet_no_duplicate.begin(), vec_bquark_jet_no_duplicate.end(), ijet) == 1)
							  h_gvtx_shared_loosebtaggedjet_nm1_bquarkjet_or_not->Fill(1.0, w);
						  else
							  h_gvtx_shared_loosebtaggedjet_nm1_bquarkjet_or_not->Fill(0.0, w);

					  }
					  else {

						  if (count_bquark_match >= 1) {
							  h_gvtx_seed_tracks_per_no_shared_jet->Fill(jet_seed_ntrack, w);
							  h_gvtx_nm1_nsigmadxy_seed_tracks_per_no_shared_jet->Fill(jet_nm1_nsigmadxy_seed_ntrack, w);
							  h_gvtx_nm1_pT_seed_tracks_per_no_shared_jet->Fill(jet_nm1_pT_seed_ntrack, w);

							  if (jet_nm1_nsigmadxy_seed_ntrack >= 3) {
								  vec_no_shared_loosebtaggedjet_nm1_dxy_or_not.push_back(0);
							  }

							  if (jet_nm1_pT_seed_ntrack >= 3) {
								  vec_no_shared_loosebtaggedjet_nm1_pT_or_not.push_back(0);
							  }

							  if (jet_seed_ntrack >= 3) {
								  vec_no_shared_loosebtaggedjet_nm1_dxy_or_not.push_back(1);
							  }

							  h_gvtx_no_shared_loosebtaggedjet_nm1_nbsv->Fill(nbsv_by_btag0_jet, w);
							  h_gvtx_no_shared_loosebtaggedjet_nm1_nloosebsv->Fill(nloosebsv_by_btag0_jet, w);
							  h_gvtx_no_shared_loosebtaggedjet_nm1_pT_ratio_loosebsv->Fill(mevent->jet_pt[ijet] / sum_b_quark_pT, w);
							  h_gvtx_no_shared_loosebtaggedjet_nm1_jet_pT->Fill(mevent->jet_pt[ijet], w);

							  for (size_t i = 0; i < vec_ntrack_loosebsv.size(); ++i) {
								  h_2D_gvtx_no_shared_loosebtaggedjet_nm1_ntrack_loosebsv->Fill(vec_ntrack_loosebsv[i], vec_jet_seedtrack_loosebsv[i], w);
								  double min_genbvtxdist3d = 5.0;
								  size_t isv = vec_jet_idx_loosebsv[i];
								  const MFVVertexAux& aux = auxes->at(isv);

								  for (size_t j = 0; j < vec_jet_idx_matched_genbvtx.size(); ++j) {
									  double genbvtxdist3d = 0.0;
									  if (vec_jet_idx_matched_genbvtx[j] == 0) {
										  genbvtxdist3d = sqrt(pow(mevent->gen_b_llp0_decay[0] - aux.x, 2) + pow(mevent->gen_b_llp0_decay[1] - aux.y, 2) + pow(mevent->gen_b_llp0_decay[2] - aux.z, 2));
									  }
									  else if (vec_jet_idx_matched_genbvtx[j] == 1) {
										  genbvtxdist3d = sqrt(pow(mevent->gen_b_llp0_decay[3] - aux.x, 2) + pow(mevent->gen_b_llp0_decay[4] - aux.y, 2) + pow(mevent->gen_b_llp0_decay[5] - aux.z, 2));
									  }
									  else if (vec_jet_idx_matched_genbvtx[j] == 2) {
										  genbvtxdist3d = sqrt(pow(mevent->gen_b_llp1_decay[0] - aux.x, 2) + pow(mevent->gen_b_llp1_decay[1] - aux.y, 2) + pow(mevent->gen_b_llp1_decay[2] - aux.z, 2));
									  }
									  else {
										  genbvtxdist3d = sqrt(pow(mevent->gen_b_llp1_decay[3] - aux.x, 2) + pow(mevent->gen_b_llp1_decay[4] - aux.y, 2) + pow(mevent->gen_b_llp1_decay[5] - aux.z, 2));
									  }
									  if (min_genbvtxdist3d > genbvtxdist3d)
										  min_genbvtxdist3d = genbvtxdist3d;
								  }
								  h_gvtx_no_shared_loosebtaggedjet_nm1_genbvtxdist3d_loosebsv->Fill(min_genbvtxdist3d, w);
								  h_2D_gvtx_no_shared_loosebtaggedjet_nm1_genbvtxdist3d_ntrack_loosebsv->Fill(min_genbvtxdist3d, vec_ntrack_loosebsv[i], w);
							  }

							  if (std::count(vec_bquark_jet_no_duplicate.begin(), vec_bquark_jet_no_duplicate.end(), ijet) == 1)
								  h_gvtx_no_shared_loosebtaggedjet_nm1_bquarkjet_or_not->Fill(1.0, w);
							  else
								  h_gvtx_no_shared_loosebtaggedjet_nm1_bquarkjet_or_not->Fill(0.0, w);
						  }

						  else {

							  h_gvtx_seed_tracks_per_no_matched_jet->Fill(jet_seed_ntrack, w);
							  h_gvtx_nm1_nsigmadxy_seed_tracks_per_no_matched_jet->Fill(jet_nm1_nsigmadxy_seed_ntrack, w);
							  h_gvtx_nm1_pT_seed_tracks_per_no_matched_jet->Fill(jet_nm1_pT_seed_ntrack, w);
							  h_gvtx_no_matched_loosebtaggedjet_nm1_jet_pT->Fill(mevent->jet_pt[ijet], w);

							  if (jet_nm1_nsigmadxy_seed_ntrack >= 3) {
								  vec_no_shared_loosebtaggedjet_nm1_dxy_or_not.push_back(0);
							  }

							  if (jet_nm1_pT_seed_ntrack >= 3) {
								  vec_no_shared_loosebtaggedjet_nm1_pT_or_not.push_back(0);
							  }

							  if (jet_seed_ntrack >= 3) {
								  vec_no_shared_loosebtaggedjet_nm1_dxy_or_not.push_back(1);
							  }

							  h_gvtx_no_matched_loosebtaggedjet_nm1_nbsv->Fill(nbsv_by_btag0_jet, w);
							  h_gvtx_no_matched_loosebtaggedjet_nm1_nloosebsv->Fill(nloosebsv_by_btag0_jet, w);

							  for (size_t i = 0; i < vec_ntrack_loosebsv.size(); ++i) {
								  h_2D_gvtx_no_matched_loosebtaggedjet_nm1_ntrack_loosebsv->Fill(vec_ntrack_loosebsv[i], vec_jet_seedtrack_loosebsv[i], w);
							  }

							  if (std::count(vec_bquark_jet_no_duplicate.begin(), vec_bquark_jet_no_duplicate.end(), ijet) == 1)
								  h_gvtx_no_matched_loosebtaggedjet_nm1_bquarkjet_or_not->Fill(1.0, w);
							  else
								  h_gvtx_no_matched_loosebtaggedjet_nm1_bquarkjet_or_not->Fill(0.0, w);

						  }
					  }

				  }
			  }

		  }

		  h_gvtx_nloosebtaggedjet_wcut->Fill(vec_loosebtagged_jet_no_duplicate.size(), w);

		  if (all_bboost == true) {
			  h_gvtx_nloosebtaggedjet_bboost_wcut->Fill(mevent->nbtags(0), w);
			  h_gvtx_shared_loosebtaggedjet_or_not_bboost_wcut->Fill(shared_loosebtaggedjet, w);
		  }
		  h_gvtx_shared_bjet_or_not->Fill(shared_bjet, w);
		  h_gvtx_shared_loosebtaggedjet_or_not->Fill(shared_loosebtaggedjet, w);

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
