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
  // only find 4 b-quarks 
  TH1F* h_4bvtx_nsv;
  TH1F* h_gvtx_nsv;
  TH1F* h_gvtx_llp_pairdphi;
  TH1F* h_gvtx_llp_pairdist2d;
  TH1F* h_gvtx_llp_pairdist3d;
  TH1F* h_gvtx_bquark_betagamma;
  TH1F* h_gvtx_nonbquark_r3d;
  // BEGIN NEW
  TH1F* h_gvtx_bhad_nonbhad_dR;
  TH2F* h_2D_gvtx_bhad_nonbhad_dR_and_pT;
  TH1F* h_gvtx_bhad_closest_jet_dR;
  TH1F* h_gvtx_bhad_jet_mindR_nonbhad_dR;
  TH1F* h_gvtx_bhad_nonbhad_jet_dR;
  // cut at dR(a jet, b-had) < 0.4 
  TH1F* h_gvtx_njet;
  TH1F* h_gvtx_ntrack_from_jets;
  TH1F* h_gvtx_nsv_from_jets;
  TH1F* h_gvtx_sum_pT_all_tracks;
  TH1F* h_gvtx_sum_pT_tracks_leading_jet;
  TH1F* h_gvtx_pT_all_tracks;
  // END NEW
  // match a pair of b-quarks and LLP
  TH1F* h_gvtx_diff_pT_bpair_llp0;
  TH1F* h_gvtx_diff_pT_bpair_llp1;
  TH1F* h_gvtx_diff_phi_bquark_bvtx;
  TH1F* h_gvtx_diff_eta_bquark_bvtx;
  // GEN-level info of bquark matching with tracks from jets 
  TH1F* h_gvtx_bquark_before_match_dR_jets;
  TH1F* h_gvtx_bquark_match_njet;
  TH1F* h_gvtx_bquark_match_nbjet;
  TH1F* h_gvtx_bquark_match_jet_ntrack;
  TH1F* h_gvtx_bquark_match_bjet_ntrack;
  TH1F* h_gvtx_bquark_before_match_dR_svs;
  TH1F* h_gvtx_bquark_match_nsv;
  TH1F* h_gvtx_bquark_match_sv_ntrack;
  TH1F* h_gvtx_msv_ntrack;
  TH1F* h_gvtx_dist3d_msv_bquark;
  TH1F* h_gvtx_dPhi_msv_bquark;
  TH1F* h_gvtx_msv_bs2derr;
  TH1F* h_gvtx_msv_dBV;
  TH1F* h_gvtx_msv_nchi2;
  TH1F* h_gvtx_msv_gen3ddist;

  // END
  TH1F* h_gvtx_bquark_pairdphi0;
  TH1F* h_gvtx_nonbquark_pairdphi0;
  TH1F* h_gvtx_nonbquark_pairdist3d0;
  TH1F* h_gvtx_nonbquark_pairdist2d0;
  TH1F* h_gvtx_bquark_pairdphi1;
  TH1F* h_gvtx_nonbquark_pairdphi1;
  TH1F* h_gvtx_nonbquark_pairdist3d1;
  TH1F* h_gvtx_nonbquark_pairdist2d1;
  TH1F* h_gvtx_diff_pT_bsvpair_llp0;
  TH1F* h_gvtx_diff_pT_bsvpair_llp1;
  TH1F* h_gvtx_bsv_pairdphi0;
  TH1F* h_gvtx_bsv_pairdphi1;
  TH1F* h_gvtx_bsv_ntrack;
  TH1F* h_gvtx_bsv_bs2derr;
  TH1F* h_gvtx_bsv_dBV;
  TH1F* h_gvtx_bsv_nchi2;
  TH1F* h_gvtx_bsv_gen3ddist;
  //TH1F* h_gvtx_ghost_pairdphi;
  //TH1F* h_gvtx_bquark_pairdist2d0;
  //TH1F* h_gvtx_bquark_pairdist2d1;
  TH1F* h_gvtx_all_dR_tracks_bsv_llp0;
  TH1F* h_gvtx_all_dR_tracks_bsv_llp1;

  TH1F* h_gvtx_dist3d_bsv_bquark;
  TH1F* h_gvtx_dPhi_bsv_bquark;
  TH1F* h_gvtx_all_dR_tracks_bquark_llp0;
  TH1F* h_gvtx_all_dR_tracks_bquark_llp1;

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
  h_n_gen_bvtx = fs->make<TH1F>("h_n_gen_bvtx", ";# of GEN b-vertices (from non-b hadrons); events/1", 40, 0, 40);
  h_4bvtx_nsv = fs->make<TH1F>("h_4bvtx_nsv", "req. exact 4 GEN b-vertices;# of (loose) secondary vertices; events/1", 40, 0, 40);
  // only find 4 b-vertices and at least 4 loose SVs  
  h_gvtx_nsv = fs->make<TH1F>("h_gvtx_nsv", "req. exact 4 GEN b-vertices && nsv>=4 ;# of (loose) secondary vertices; events/1", 40, 0, 40);
  h_gvtx_llp_pairdphi = fs->make<TH1F>("h_gvtx_llp_pairdphi", ";LLP pair |#Delta#phi| (rad);events/.031", 100, 0, 3.1416);
  h_gvtx_llp_pairdist2d = fs->make<TH1F>("h_gvtx_llp_pairdist2d", ";dist2d(gen vtx #0, #1) (cm);events/.01 mm", 1000, 0, 10);
  h_gvtx_llp_pairdist3d = fs->make<TH1F>("h_gvtx_llp_pairdist3d", ";dist3d(gen vtx #0, #1) (cm);events/.01 mm", 1000, 0, 10);
  h_gvtx_bquark_betagamma = fs->make<TH1F>("h_gvtx_bquark_betagamma", "; b-quark #beta#gamma; 4 x events / 0.1", 100, 0, 100);
  h_gvtx_nonbquark_r3d = fs->make<TH1F>("h_gvtx_nonbquark_r3d", ";dist3d(GEN b-vtx, LLP) (cm);events/.01 mm", 1000, 0, 10);
  // BEGIN NEW
  h_gvtx_bhad_nonbhad_dR = fs->make<TH1F>("h_gvtx_bhad_nonbhad_dR", ";#Delta R between mom. of a GEN non-b hadron and GEN b-had; arb. units", 140, 0, 7.0);
  h_2D_gvtx_bhad_nonbhad_dR_and_pT = fs->make<TH2F>("h_2D_gvtx_bhad_nonbhad_dR_and_pT", ";#Delta R between mom. of a GEN non-b hadron and GEN b-had; non-b hadron p_{T} (GeV); arb. units", 70, 0, 7.0, 50, 0, 100);
  h_gvtx_bhad_closest_jet_dR = fs->make<TH1F>("h_gvtx_bhad_closest_jet_dR", ";#Delta R between mom. of a closest RECO jet and a GEN b-had; arb. units", 140, 0, 7.0);
  h_gvtx_bhad_jet_mindR_nonbhad_dR = fs->make<TH1F>("h_gvtx_bhad_jet_mindR_nonbhad_dR", ";#Delta R between mom. of a closest RECO jet and a GEN non-b had; arb. units", 140, 0, 7.0);
  h_gvtx_bhad_nonbhad_jet_dR = fs->make<TH1F>("h_gvtx_bhad_nonbhad_jet_dR", ";#Delta R between mom. of a closest RECO jet to a GEN non-b had and GEN b had; arb. units", 140, 0, 7.0);
  // END NEW

  // match a pair of b-quarks and LLP
  h_gvtx_diff_pT_bpair_llp0 = fs->make<TH1F>("h_gvtx_diff_pT_bpair_llp0", "; b-quark pair p_{T} - LLP0 p_{T}(GeV);events/1 GeV", 100, -50, 50);
  h_gvtx_diff_pT_bpair_llp1 = fs->make<TH1F>("h_gvtx_diff_pT_bpair_llp1", "; b-quark pair p_{T} - LLP1 p_{T}(GeV);events/1 GeV", 100, -50, 50);
  h_gvtx_diff_phi_bquark_bvtx = fs->make<TH1F>("h_gvtx_diff_phi_bquark_bvtx", ";#phi(b-quark) - #phi(b-vtx)  (rad);4 x events/.031", 200, -3.1416, 3.1416);
  h_gvtx_diff_eta_bquark_bvtx = fs->make<TH1F>("h_gvtx_diff_eta_bquark_bvtx", ";#eta(b-quark) - #eta(b-vtx)  (rad);4 x events/.031", 200, -3.1416, 3.1416);
  // GEN-level info of bquark matching with tracks from jets 
  h_gvtx_bquark_before_match_dR_jets = fs->make<TH1F>("h_gvtx_bquark_before_match_dR_jets", "Before req. dR < 0.5;dR(GEN b-quark,a match-jet);arb. units", 200, 0.0, 3.1416);
  h_gvtx_bquark_match_njet = fs->make<TH1F>("h_gvtx_bquark_match_njet", ";# of jets within dR < 0.5; 4 x events/1", 40, 0, 40);
  h_gvtx_bquark_match_nbjet = fs->make<TH1F>("h_gvtx_bquark_match_nbjet", ";# of loose b-jets within dR < 0.5; 4 x events/1", 40, 0, 40);
  h_gvtx_bquark_match_jet_ntrack = fs->make<TH1F>("h_gvtx_bquark_match_jet_ntrack", ";# of tracks from match-jets within dR < 0.5; 4 x events/1", 80, 0, 80);
  h_gvtx_bquark_match_bjet_ntrack = fs->make<TH1F>("h_gvtx_bquark_match_bjet_ntrack", ";# of tracks from match-bjets within dR < 0.5; 4 x events/1", 80, 0, 80);
  h_gvtx_bquark_before_match_dR_svs = fs->make<TH1F>("h_gvtx_bquark_before_match_dR_svs", "Before req. dR < 0.5;dR(GEN b-quark,a match-sv);arb. units", 200, 0.0, 3.1416);
  h_gvtx_bquark_match_nsv = fs->make<TH1F>("h_gvtx_bquark_match_nsv", ";# of SVs within dR < 0.5 ; 4 x events/1", 40, 0, 40);
  h_gvtx_bquark_match_sv_ntrack = fs->make<TH1F>("h_gvtx_bquark_match_sv_ntrack", ";# of tracks from match-SVs within dR < 0.5; 4 x events/1", 40, 0, 40);
  h_gvtx_dist3d_msv_bquark = fs->make<TH1F>("h_gvtx_dist3d_msv_bquark", ";dist3d(GEN b-vtx,match-sv) (cm)", 200, 0, 0.6);
  h_gvtx_dPhi_msv_bquark = fs->make<TH1F>("h_gvtx_dPhi_msv_bquark", ";|dPhi(GEN b-vtx,match-sv)|", 200, 0, 3.15);
  h_gvtx_msv_ntrack = fs->make<TH1F>("h_gvtx_msv_ntrack", ";# of tracks per match-sv;", 50, 0, 50);
  h_gvtx_msv_bs2derr = fs->make<TH1F>("h_gvtx_msv_bs2derr", ";match-sv's bs2derr(cm)", 200, 0, 0.02);
  h_gvtx_msv_dBV = fs->make<TH1F>("h_gvtx_msv_dBV", ";match-sv's dBV(cm)", 200, 0, 3.0);
  h_gvtx_msv_gen3ddist = fs->make<TH1F>("h_gvtx_msv_gen3ddist", "; dist3d(match-sv, closest gen LLP-vtx) (cm)", 200, 0, 0.6);
  h_gvtx_msv_nchi2 = fs->make<TH1F>("h_gvtx_msv_nchi2", ";match-sv #chi^{2}/dof;", 10, 0, 10);



  // END
  h_gvtx_bquark_pairdphi0 = fs->make<TH1F>("h_gvtx_bquark_pairdphi0", ";|#Delta#phi| (rad) of b-quark pair per LLP0 ;events/.031", 100, 0, 3.1416);
  h_gvtx_nonbquark_pairdphi0 = fs->make<TH1F>("h_gvtx_nonbquark_pairdphi0", "; |#Delta#phi| (rad) of GEN b-vertex pair per LLP0 ;events/.031", 100, 0, 3.1416);
  h_gvtx_nonbquark_pairdist2d0 = fs->make<TH1F>("h_gvtx_nonbquark_pairdist2d0", ";dist2d(gen b-vtx #0, #1) (cm);events/.01 mm", 1000, 0, 10);
  h_gvtx_nonbquark_pairdist3d0 = fs->make<TH1F>("h_gvtx_nonbquark_pairdist3d0", ";dist3d(gen b-vtx #0, #1) (cm);events/.01 mm", 1000, 0, 10);
  h_gvtx_bquark_pairdphi1 = fs->make<TH1F>("h_gvtx_bquark_pairdphi1", ";|#Delta#phi| (rad) of b-quark pair per LLP1 ;events/.031", 100, 0, 3.1416);
  h_gvtx_nonbquark_pairdphi1 = fs->make<TH1F>("h_gvtx_nonbquark_pairdphi1", "; |#Delta#phi| (rad) of GEN b-vertex pair per LLP1 ;events/.031", 100, 0, 3.1416);
  h_gvtx_nonbquark_pairdist2d1 = fs->make<TH1F>("h_gvtx_nonbquark_pairdist2d1", ";dist2d(gen b-vtx #2, #3) (cm);events/.01 mm", 1000, 0, 10);
  h_gvtx_nonbquark_pairdist3d1 = fs->make<TH1F>("h_gvtx_nonbquark_pairdist3d1", ";dist3d(gen b-vtx #2, #3) (cm);events/.01 mm", 1000, 0, 10);
  h_gvtx_diff_pT_bsvpair_llp0 = fs->make<TH1F>("h_gvtx_diff_pT_bsvpair_llp0", "; b-sv pair p_{T} - LLP0 p_{T}(GeV);events/1 GeV", 100, -50, 50);
  h_gvtx_diff_pT_bsvpair_llp1 = fs->make<TH1F>("h_gvtx_diff_pT_bsvpair_llp1", "; b-sv pair p_{T} - LLP1 p_{T}(GeV);events/1 GeV", 100, -50, 50);
  h_gvtx_bsv_pairdphi0 = fs->make<TH1F>("h_gvtx_bsv_pairdphi0", ";|#Delta#phi| (rad) of b-sv pair per LLP0;events/.031", 100, 0, 3.1416);
  h_gvtx_bsv_pairdphi1 = fs->make<TH1F>("h_gvtx_bsv_pairdphi1", ";|#Delta#phi| (rad) of b-sv pair per LLP1 ;events/.031", 100, 0, 3.1416);
  h_gvtx_bsv_ntrack = fs->make<TH1F>("h_gvtx_bsv_ntrack", ";# of tracks per b-sv;", 50, 0, 50);
  h_gvtx_bsv_bs2derr = fs->make<TH1F>("h_gvtx_bsv_bs2derr", ";b-sv's bs2derr(cm)", 200, 0, 0.02);
  h_gvtx_bsv_dBV = fs->make<TH1F>("h_gvtx_bsv_dBV", ";b-sv's dBV(cm)", 200, 0, 3.0);
  h_gvtx_bsv_gen3ddist = fs->make<TH1F>("h_gvtx_bsv_gen3ddist", "is a b-sv actually an LLP-sv?; dist3d(b-sv, closest gen LLP-vtx) (cm)", 200, 0, 0.6);
  h_gvtx_bsv_nchi2 = fs->make<TH1F>("h_gvtx_bsv_nchi2", ";b-sv #chi^{2}/dof;", 10, 0, 10);

  h_gvtx_dist3d_bsv_bquark = fs->make<TH1F>("h_gvtx_dist3d_bsv_bquark", ";matched dist3d(gen b-vtx,b-sv) (cm)", 200, 0, 0.6);
  h_gvtx_dPhi_bsv_bquark = fs->make<TH1F>("h_gvtx_dPhi_bsv_bquark", ";matched |dPhi(gen b-vtx,b-sv)|", 200, 0, 3.15);

  h_gvtx_all_dR_tracks_bquark_llp0 = fs->make<TH1F>("h_gvtx_all_dR_tracks_bquark_llp0", ";dR(gen b-vtx,b-sv track) per LLP0", 200, 0, 3.15);
  h_gvtx_all_dR_tracks_bquark_llp1 = fs->make<TH1F>("h_gvtx_all_dR_tracks_bquark_llp1", ";dR(gen b-vtx,b-sv track) per LLP1", 200, 0, 3.15);

  h_gvtx_all_dR_tracks_bsv_llp0 = fs->make<TH1F>("h_gvtx_all_dR_tracks_bsv_llp0", ";dR(b-sv,b-sv track) per LLP0", 200, 0, 3.15);
  h_gvtx_all_dR_tracks_bsv_llp1 = fs->make<TH1F>("h_gvtx_all_dR_tracks_bsv_llp1", ";dR(b-sv,b-sv track) per LLP1", 200, 0, 3.15);

  //h_gvtx_ghost_pairdphi;
  //h_gvtx_bquark_pairdist2d0 = fs->make<TH1F>("h_gvtx_bquark_pairdist2d0", "found 4 b-quarks and matched with LLP;dist2d(b-quak pair) per LLP0 (cm);events/.01 mm", 300, 0, 3);
  //h_gvtx_bquark_pairdist2d1 = = fs->make<TH1F>("h_gvtx_bquark_pairdist2d1", "found 4 b-quarks and matched with LLP;dist2d(b-quak pair) per LLP1 (cm);events/.01 mm", 300, 0, 3);


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
  // only 4 b-vertices and >=4 loose-SVs per event 
  //
  
  
	  
  if (mevent->gen_bchain_nonb_had_eta.size() == 4) {
		  h_4bvtx_nsv->Fill(nsv, w);
		  for (size_t i = 0; i < 4; ++i) {
			  for (size_t j = 0; j < mevent->gen_bchain_nonb_had_eta[i].size(); ++j) {
				  double dR = reco::deltaR(mevent->gen_bchain_nonb_had_eta[i][j], mevent->gen_bchain_nonb_had_phi[i][j], mevent->gen_bchain_b_had_eta[i], mevent->gen_bchain_b_had_phi[i]);
				  h_gvtx_bhad_nonbhad_dR->Fill(dR, w);
				  h_2D_gvtx_bhad_nonbhad_dR_and_pT->Fill(dR, mevent->gen_bchain_nonb_had_pt[i][j], w);
			  }

			  double mindR = 400;
			  for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
			      if (mevent->jet_pt[ijet] < mfv::min_jet_pt)
					continue;
				  if (reco::deltaR(mevent->jet_eta[ijet], mevent->jet_phi[ijet], mevent->gen_bchain_b_had_eta[i], mevent->gen_bchain_b_had_phi[i]) < mindR)
					mindR = reco::deltaR(mevent->jet_eta[ijet], mevent->jet_phi[ijet], mevent->gen_bchain_b_had_eta[i], mevent->gen_bchain_b_had_phi[i]);
			  }
			  if (mindR != 400)
				h_gvtx_bhad_closest_jet_dR->Fill(mindR, w);
			  //h_gvtx_bhad_jet_mindR_nonbhad_dR->Fill(mindR_nonb, w);
		      //h_gvtx_bhad_nonbhad_jet_dR->Fill(reco::deltaR(mevent->jet_eta[matchnonb_ijet], mevent->jet_phi[matchnonb_ijet], mevent->gen_bchain_nonb_had_eta[i], mevent->gen_bchain_nonb_had_phi[i]), w);
			  
		  }

		  if (nsv >= 4) {
			  h_gvtx_nsv->Fill(nsv, w);
			  h_gvtx_llp_pairdphi->Fill(fabs(reco::deltaPhi(mevent->gen_lsp_phi[0], mevent->gen_lsp_phi[1])), w);
			  h_gvtx_llp_pairdist2d->Fill(mevent->lspdist2d(), w);
			  h_gvtx_llp_pairdist3d->Fill(mevent->lspdist3d(), w);

			  for (size_t k = 0; k < 2; ++k) {
				  if (k == 0) {
					  double genllp_pT = mevent->gen_lsp_pt[k];
					  double bpair_pT = mevent->gen_daughters[0].Pt() + mevent->gen_daughters[1].Pt();
					  double diff_pT = bpair_pT - genllp_pT;
					  double pairdphi = fabs(reco::deltaPhi(mevent->gen_daughters[0].Phi(), mevent->gen_daughters[1].Phi()));
					  double pairdphi_nonb = fabs(reco::deltaPhi(mevent->gen_b_llp0_flight(0).Phi(), mevent->gen_b_llp0_flight(1).Phi()));
					  double pairdist3d0 = sqrt(pow(mevent->gen_b_llp0_decay[0] - mevent->gen_b_llp0_decay[3], 2) + pow(mevent->gen_b_llp0_decay[1] - mevent->gen_b_llp0_decay[4], 2) + pow(mevent->gen_b_llp0_decay[2] - mevent->gen_b_llp0_decay[5], 2));
					  double pairdist2d0 = sqrt(pow(mevent->gen_b_llp0_decay[0] - mevent->gen_b_llp0_decay[3], 2) + pow(mevent->gen_b_llp0_decay[1] - mevent->gen_b_llp0_decay[4], 2));

					  h_gvtx_diff_pT_bpair_llp0->Fill(diff_pT, w);
					  h_gvtx_diff_phi_bquark_bvtx->Fill(reco::deltaPhi(mevent->gen_daughters[0].Phi(), mevent->gen_b_llp0_flight(0).Phi()), w);
					  h_gvtx_diff_phi_bquark_bvtx->Fill(reco::deltaPhi(mevent->gen_daughters[1].Phi(), mevent->gen_b_llp0_flight(1).Phi()), w);
					  h_gvtx_diff_eta_bquark_bvtx->Fill(etaFromXYZ(mevent->gen_lsp_decay[0] - mevent->gen_b_llp0_decay[0], mevent->gen_lsp_decay[1] - mevent->gen_b_llp0_decay[1], mevent->gen_lsp_decay[2] - mevent->gen_b_llp0_decay[2]), w);
					  h_gvtx_diff_eta_bquark_bvtx->Fill(etaFromXYZ(mevent->gen_lsp_decay[0] - mevent->gen_b_llp0_decay[3], mevent->gen_lsp_decay[1] - mevent->gen_b_llp0_decay[4], mevent->gen_lsp_decay[2] - mevent->gen_b_llp0_decay[5]), w);
					  double b0beta = mevent->gen_daughters[0].P() / mevent->gen_daughters[0].Energy();
					  double b0betagamma = b0beta / sqrt(1 - b0beta * b0beta);
					  h_gvtx_bquark_betagamma->Fill(b0betagamma, w);
					  double b1beta = mevent->gen_daughters[1].P() / mevent->gen_daughters[1].Energy();
					  double b1betagamma = b1beta / sqrt(1 - b1beta * b1beta);
					  h_gvtx_bquark_betagamma->Fill(b1betagamma, w);
					  h_gvtx_nonbquark_r3d->Fill(mag(mevent->gen_b_llp0_decay[0] - mevent->gen_lsp_decay[0], mevent->gen_b_llp0_decay[1] - mevent->gen_lsp_decay[1], mevent->gen_b_llp0_decay[2] - mevent->gen_lsp_decay[2]), w);
					  h_gvtx_nonbquark_r3d->Fill(mag(mevent->gen_b_llp0_decay[3] - mevent->gen_lsp_decay[0], mevent->gen_b_llp0_decay[4] - mevent->gen_lsp_decay[1], mevent->gen_b_llp0_decay[5] - mevent->gen_lsp_decay[2]), w);
					  h_gvtx_bquark_pairdphi0->Fill(pairdphi, w);
					  h_gvtx_nonbquark_pairdphi0->Fill(pairdphi_nonb, w);
					  h_gvtx_nonbquark_pairdist3d0->Fill(pairdist3d0, w);
					  h_gvtx_nonbquark_pairdist2d0->Fill(pairdist2d0, w);

				  }
				  else {
					  double genllp_pT = mevent->gen_lsp_pt[k];
					  double bpair_pT = mevent->gen_daughters[2].Pt() + mevent->gen_daughters[3].Pt();
					  double diff_pT = bpair_pT - genllp_pT;
					  double pairdphi = fabs(reco::deltaPhi(mevent->gen_daughters[2].Phi(), mevent->gen_daughters[3].Phi()));
					  double pairdphi_nonb = fabs(reco::deltaPhi(mevent->gen_b_llp1_flight(0).Phi(), mevent->gen_b_llp1_flight(1).Phi()));
					  double pairdist3d1 = sqrt(pow(mevent->gen_b_llp1_decay[0] - mevent->gen_b_llp1_decay[3], 2) + pow(mevent->gen_b_llp1_decay[1] - mevent->gen_b_llp1_decay[4], 2) + pow(mevent->gen_b_llp1_decay[2] - mevent->gen_b_llp1_decay[5], 2));
					  double pairdist2d1 = sqrt(pow(mevent->gen_b_llp1_decay[0] - mevent->gen_b_llp1_decay[3], 2) + pow(mevent->gen_b_llp1_decay[1] - mevent->gen_b_llp1_decay[4], 2));

					  h_gvtx_diff_pT_bpair_llp1->Fill(diff_pT, w);
					  h_gvtx_diff_phi_bquark_bvtx->Fill(reco::deltaPhi(mevent->gen_daughters[2].Phi(), mevent->gen_b_llp1_flight(0).Phi()), w);
					  h_gvtx_diff_phi_bquark_bvtx->Fill(reco::deltaPhi(mevent->gen_daughters[3].Phi(), mevent->gen_b_llp1_flight(1).Phi()), w);
					  h_gvtx_diff_eta_bquark_bvtx->Fill(etaFromXYZ(mevent->gen_lsp_decay[3] - mevent->gen_b_llp1_decay[0], mevent->gen_lsp_decay[4] - mevent->gen_b_llp1_decay[1], mevent->gen_lsp_decay[5] - mevent->gen_b_llp1_decay[2]), w);
					  h_gvtx_diff_eta_bquark_bvtx->Fill(etaFromXYZ(mevent->gen_lsp_decay[3] - mevent->gen_b_llp1_decay[3], mevent->gen_lsp_decay[4] - mevent->gen_b_llp1_decay[4], mevent->gen_lsp_decay[5] - mevent->gen_b_llp1_decay[5]), w);
					  double b2beta = mevent->gen_daughters[2].P() / mevent->gen_daughters[2].Energy();
					  double b2betagamma = b2beta / sqrt(1 - b2beta * b2beta);
					  h_gvtx_bquark_betagamma->Fill(b2betagamma, w);
					  double b3beta = mevent->gen_daughters[3].P() / mevent->gen_daughters[3].Energy();
					  double b3betagamma = b3beta / sqrt(1 - b3beta * b3beta);
					  h_gvtx_bquark_betagamma->Fill(b3betagamma, w);
					  h_gvtx_nonbquark_r3d->Fill(mag(mevent->gen_b_llp1_decay[0] - mevent->gen_lsp_decay[3], mevent->gen_b_llp1_decay[1] - mevent->gen_lsp_decay[4], mevent->gen_b_llp1_decay[2] - mevent->gen_lsp_decay[5]), w);
					  h_gvtx_nonbquark_r3d->Fill(mag(mevent->gen_b_llp1_decay[3] - mevent->gen_lsp_decay[3], mevent->gen_b_llp1_decay[4] - mevent->gen_lsp_decay[4], mevent->gen_b_llp1_decay[5] - mevent->gen_lsp_decay[5]), w);
					  h_gvtx_bquark_pairdphi1->Fill(pairdphi, w);
					  h_gvtx_nonbquark_pairdphi1->Fill(pairdphi_nonb, w);
					  h_gvtx_nonbquark_pairdist3d1->Fill(pairdist3d1, w);
					  h_gvtx_nonbquark_pairdist2d1->Fill(pairdist2d1, w);
				  }

				  double match_dR_threshold = 0.5;
				  for (size_t dau = 0; dau < 2; ++dau) {
					  int match_njets = 0;
					  int match_nbjets = 0;
					  int match_jet_ntrack = 0;
					  int match_bjet_ntrack = 0;
					  for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
						  if (mevent->jet_pt[ijet] < mfv::min_jet_pt)
							  continue;
						  h_gvtx_bquark_before_match_dR_jets->Fill(reco::deltaR(mevent->jet_eta[ijet], mevent->jet_phi[ijet], mevent->gen_daughters[k * 2 + dau].Eta(), mevent->gen_daughters[k * 2 + dau].Phi()), w);
						  if (match_dR_threshold > reco::deltaR(mevent->jet_eta[ijet], mevent->jet_phi[ijet], mevent->gen_daughters[k * 2 + dau].Eta(), mevent->gen_daughters[k * 2 + dau].Phi())) {
							  match_njets++;
							  int jet_ntrack = 0;
							  for (unsigned j = 0; j < mevent->jet_track_which_jet.size(); ++j) {
								  if (ijet == mevent->jet_track_which_jet[j]) {
									  jet_ntrack++;
								  }
							  }
							  match_jet_ntrack += jet_ntrack;
							  if (mevent->is_btagged(ijet, 0)) {		   // loose b-tag
								  match_nbjets++;
								  match_bjet_ntrack += jet_ntrack;
							  }
						  }


					  }
					  h_gvtx_bquark_match_njet->Fill(match_njets, w);
					  h_gvtx_bquark_match_nbjet->Fill(match_nbjets, w);
					  h_gvtx_bquark_match_jet_ntrack->Fill(match_jet_ntrack, w);
					  h_gvtx_bquark_match_bjet_ntrack->Fill(match_bjet_ntrack, w);

					  int match_nsv = 0;
					  int match_sv_ntrack = 0;
					  for (int isv = 0; isv < nsv; ++isv) {
						  const MFVVertexAux& maux = auxes->at(isv);
						  double msv_phi = atan2(maux.y - mevent->pvy, maux.x - mevent->pvx);
						  double msv_eta = etaFromXYZ(maux.x - mevent->pvx, maux.y - mevent->pvy, maux.z - mevent->pvz);
						  h_gvtx_bquark_before_match_dR_svs->Fill(reco::deltaR(msv_eta, msv_phi, mevent->gen_daughters[k * 2 + dau].Eta(), mevent->gen_daughters[k * 2 + dau].Phi()), w);
						  if (match_dR_threshold > reco::deltaR(msv_eta, msv_phi, mevent->gen_daughters[k * 2 + dau].Eta(), mevent->gen_daughters[k * 2 + dau].Phi())) {
							  match_nsv++;
							  match_sv_ntrack += maux.ntracks();
							  double msv_dist3d = 0;
							  if (k == 0) {
								  msv_dist3d = sqrt(pow(maux.x - mevent->gen_b_llp0_decay[dau * 3 + 0], 2) + pow(maux.y - mevent->gen_b_llp0_decay[dau * 3 + 1], 2) + pow(maux.z - mevent->gen_b_llp0_decay[dau * 3 + 2], 2));
								  h_gvtx_dPhi_msv_bquark->Fill(fabs(reco::deltaPhi(msv_phi, mevent->gen_b_llp0_flight(dau).Phi())), w);
							  }
							  else {
								  msv_dist3d = sqrt(pow(maux.x - mevent->gen_b_llp1_decay[dau * 3 + 0], 2) + pow(maux.y - mevent->gen_b_llp1_decay[dau * 3 + 1], 2) + pow(maux.z - mevent->gen_b_llp1_decay[dau * 3 + 2], 2));
								  h_gvtx_dPhi_msv_bquark->Fill(fabs(reco::deltaPhi(msv_phi, mevent->gen_b_llp1_flight(dau).Phi())), w);
							  }
							  h_gvtx_dist3d_msv_bquark->Fill(msv_dist3d, w);
							  h_gvtx_msv_ntrack->Fill(maux.ntracks(), w);
							  h_gvtx_msv_bs2derr->Fill(maux.bs2derr, w);
							  h_gvtx_msv_dBV->Fill(mevent->bs2ddist(maux), w);
							  h_gvtx_msv_gen3ddist->Fill(maux.gen3ddist, w);
							  h_gvtx_msv_nchi2->Fill(maux.chi2dof(), w);
						  }
					  }
					  h_gvtx_bquark_match_nsv->Fill(match_nsv, w);
					  h_gvtx_bquark_match_sv_ntrack->Fill(match_sv_ntrack, w);
				  }
			  }





			  std::vector<size_t> vec_bvtx_match = {};
			  double bsvpair0_pT = 0;
			  double bsvpair1_pT = 0;
			  for (int k = 0; k < 2; ++k) {

				  double diff_sv_dist3d = 200;
				  double isv_b = 0;
				  for (int isv = 0; isv < nsv; ++isv) {
					  const MFVVertexAux& aux = auxes->at(isv);
					  if (std::count(vec_bvtx_match.begin(), vec_bvtx_match.end(), isv))
						  continue;

					  double temp_diff_sv_dist3d = sqrt(pow(aux.x - mevent->gen_b_llp0_decay[k * 3 + 0], 2) + pow(aux.y - mevent->gen_b_llp0_decay[k * 3 + 1], 2) + pow(aux.z - mevent->gen_b_llp0_decay[k * 3 + 2], 2));
					  if (temp_diff_sv_dist3d < diff_sv_dist3d) {
						  diff_sv_dist3d = temp_diff_sv_dist3d;
						  isv_b = isv;
					  }
				  }

				  vec_bvtx_match.push_back(isv_b);
				  const MFVVertexAux& baux = auxes->at(vec_bvtx_match[k]);
				  if (baux.gen3ddist > 0.0150 && baux.bs2derr > 0.0050) {
					  double bsv_phi = atan2(baux.y - mevent->pvy, baux.x - mevent->pvx);
					  double bsv_eta = etaFromXYZ(baux.x - mevent->pvx, baux.y - mevent->pvy, baux.z - mevent->pvz);
					  double bsv_dist3d = sqrt(pow(baux.x - mevent->gen_b_llp0_decay[k * 3 + 0], 2) + pow(baux.y - mevent->gen_b_llp0_decay[k * 3 + 1], 2) + pow(baux.z - mevent->gen_b_llp0_decay[k * 3 + 2], 2));
					  h_gvtx_dist3d_bsv_bquark->Fill(bsv_dist3d, w);
					  h_gvtx_dPhi_bsv_bquark->Fill(fabs(reco::deltaPhi(bsv_phi, mevent->gen_b_llp0_flight(k).Phi())), w);

					  h_gvtx_bsv_ntrack->Fill(baux.ntracks(), w);
					  h_gvtx_bsv_bs2derr->Fill(baux.bs2derr, w);
					  h_gvtx_bsv_dBV->Fill(mevent->bs2ddist(baux), w);
					  h_gvtx_bsv_gen3ddist->Fill(baux.gen3ddist, w);
					  h_gvtx_bsv_nchi2->Fill(baux.chi2dof(), w);

					  for (int j = 0; j < baux.ntracks(); ++j) {
						  bsvpair0_pT += baux.track_pt(j);
						  h_gvtx_all_dR_tracks_bsv_llp0->Fill(reco::deltaR(bsv_eta, bsv_phi, baux.track_eta[j], baux.track_phi[j]), w);
						  h_gvtx_all_dR_tracks_bquark_llp0->Fill(reco::deltaR(mevent->gen_b_llp0_flight(k).Eta(), mevent->gen_b_llp0_flight(k).Phi(), baux.track_eta[j], baux.track_phi[j]), w);
					  }
				  }

			  }

			  if (vec_bvtx_match.size() == 2) {
				  double genllp_pT = mevent->gen_lsp_pt[0];
				  double diff_sv_pT = bsvpair0_pT - genllp_pT;
				  const MFVVertexAux& b0aux = auxes->at(vec_bvtx_match[0]);
				  const MFVVertexAux& b1aux = auxes->at(vec_bvtx_match[1]);
				  double bsv0_phi = atan2(b0aux.y - mevent->pvy, b0aux.x - mevent->pvx);
				  double bsv1_phi = atan2(b1aux.y - mevent->pvy, b1aux.x - mevent->pvx);
				  double svpairdphi = fabs(reco::deltaPhi(bsv0_phi, bsv1_phi));
				  h_gvtx_diff_pT_bsvpair_llp0->Fill(diff_sv_pT, w);
				  h_gvtx_bsv_pairdphi0->Fill(svpairdphi, w);
			  }

			  for (int k = 0; k < 2; ++k) {

				  double diff_sv_dist3d = 200;
				  double isv_b = 0;
				  for (int isv = 0; isv < nsv; ++isv) {
					  const MFVVertexAux& aux = auxes->at(isv);
					  if (std::count(vec_bvtx_match.begin(), vec_bvtx_match.end(), isv))
						  continue;

					  double temp_diff_sv_dist3d = sqrt(pow(aux.x - mevent->gen_b_llp1_decay[k * 3 + 0], 2) + pow(aux.y - mevent->gen_b_llp1_decay[k * 3 + 1], 2) + pow(aux.z - mevent->gen_b_llp1_decay[k * 3 + 2], 2));
					  if (temp_diff_sv_dist3d < diff_sv_dist3d) {
						  diff_sv_dist3d = temp_diff_sv_dist3d;
						  isv_b = isv;
					  }
				  }

				  vec_bvtx_match.push_back(isv_b);
				  const MFVVertexAux& baux = auxes->at(vec_bvtx_match[k + 2]);
				  if (baux.gen3ddist > 0.0150 && baux.bs2derr > 0.0050) {
					  double bsv_phi = atan2(baux.y - mevent->pvy, baux.x - mevent->pvx);
					  double bsv_eta = etaFromXYZ(baux.x - mevent->pvx, baux.y - mevent->pvy, baux.z - mevent->pvz);
					  double bsv_dist3d = sqrt(pow(baux.x - mevent->gen_b_llp1_decay[k * 3 + 0], 2) + pow(baux.y - mevent->gen_b_llp1_decay[k * 3 + 1], 2) + pow(baux.z - mevent->gen_b_llp1_decay[k * 3 + 2], 2));
					  h_gvtx_dist3d_bsv_bquark->Fill(bsv_dist3d, w);
					  h_gvtx_dPhi_bsv_bquark->Fill(fabs(reco::deltaPhi(bsv_phi, mevent->gen_b_llp1_flight(k).Phi())), w);

					  h_gvtx_bsv_ntrack->Fill(baux.ntracks(), w);
					  h_gvtx_bsv_bs2derr->Fill(baux.bs2derr, w);
					  h_gvtx_bsv_dBV->Fill(mevent->bs2ddist(baux), w);
					  h_gvtx_bsv_gen3ddist->Fill(baux.gen3ddist, w);
					  h_gvtx_bsv_nchi2->Fill(baux.chi2dof(), w);

					  for (int j = 0; j < baux.ntracks(); ++j) {
						  bsvpair1_pT += baux.track_pt(j);
						  h_gvtx_all_dR_tracks_bsv_llp1->Fill(reco::deltaR(bsv_eta, bsv_phi, baux.track_eta[j], baux.track_phi[j]), w);
						  h_gvtx_all_dR_tracks_bquark_llp1->Fill(reco::deltaR(mevent->gen_b_llp1_flight(k).Eta(), mevent->gen_b_llp1_flight(k).Phi(), baux.track_eta[j], baux.track_phi[j]), w);
					  }
				  }

			  }

			  if (vec_bvtx_match.size() == 4) {
				  double genllp_pT = mevent->gen_lsp_pt[1];
				  double diff_sv_pT = bsvpair1_pT - genllp_pT;
				  const MFVVertexAux& b2aux = auxes->at(vec_bvtx_match[2]);
				  const MFVVertexAux& b3aux = auxes->at(vec_bvtx_match[3]);
				  double bsv2_phi = atan2(b2aux.y - mevent->pvy, b2aux.x - mevent->pvx);
				  double bsv3_phi = atan2(b3aux.y - mevent->pvy, b3aux.x - mevent->pvx);
				  double svpairdphi = fabs(reco::deltaPhi(bsv2_phi, bsv3_phi));
				  h_gvtx_diff_pT_bsvpair_llp1->Fill(diff_sv_pT, w);
				  h_gvtx_bsv_pairdphi1->Fill(svpairdphi, w);
			  }

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

  for (int i = 0; i < 3; ++i) {
    h_nbtags[i]->Fill(mevent->nbtags(i), w);
    h_nbtags_v_bquark_code[i]->Fill(mevent->gen_flavor_code, mevent->nbtags(i), w);
  }
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
