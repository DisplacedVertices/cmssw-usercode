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
  TH1F* h_ntrack_sv;
  TH1F* h_sum_ntrack_sv;
  TH1F* h_sum_noutseedtrack; 
  

  TH2F* h_2D_ntrk0_ntrk1; 
  // for a cross-check 
  TH1F* h_signal_evt_min_dau_dxy;
  TH1F* h_signal_evt_gendist3d_vtx0;
  TH2F* h_2D_signal_evt_llp0_daudxy;
  TH1F* h_signal_evt_llp0_min_dau_dxy;
  TH1F* h_signal_evt_vtx0_outseedtrk_trkdist;
  TH1F* h_signal_evt_vtx0_outseedtrk_trkdistsig;
  TH2F* h_2D_signal_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_trkdistsig;
  TH2F* h_2D_signal_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_trkdist;
  TH1F* h_signal_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_nsigmadxybs;
  TH1F* h_signal_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_trkdistsig;
  TH1F* h_signal_evt_llp01_gendist3d;
  TH1F* h_signal_evt_vtx01_dist3d;
  TH1F* h_signal_evt_vtx01_dist3dsig;
  TH1F* h_signal_evt_vtx0_outseedtrk_nsigmadxybs;
  TH1F* h_signal_evt_vtx0_outseedtrk_dxybs;
  TH1F* h_signal_evt_vtx0_seedtrk_dxybs;
  TH1F* h_signal_evt_vtx0_seedtrk_nsigmadxybs;
  TH1F* h_signal_evt_vtx0_seedtrk_trkdist;
  TH1F* h_signal_evt_vtx0_seedtrk_trkdistsig;
  TH1F* h_signal_evt_vtx0_mass;
  TH1F* h_signal_evt_vtx0_pT;
  TH1F* h_signal_evt_vtx0_bs2derr;
  TH1F* h_signal_evt_vtx0_dbv;
  TH1F* h_signal_evt_n2trksv;
  TH1F* h_signal_evt_gendist3dresllp0_2trksv;
  TH2F* h_2D_signal_evt_gendist3dresllp0_n2trksv;
  TH1F* h_signal_evt_gendist3dresllp0_400um_2trksv_dbv;
  TH1F* h_signal_evt_gendist3dresllp0_400um_2trksv_absdphivtx0;
  TH1F* h_signal_evt_gendist3dresllp0_400um_2trksv_absdphillp0;
  TH1F* h_signal_evt_gendist3dresllp0_400um_2trksv_3ddistvtx0;

  // for improvement of signal eff. 
  TH1F* h_potential_evt_min_dau_dxy;
  TH1F* h_potential_evt_gendist3d_vtx0;
  TH2F* h_2D_potential_evt_llp0_daudxy;
  TH1F* h_potential_evt_llp0_min_dau_dxy;
  TH1F* h_potential_evt_gendist3d_vtx1;
  TH1F* h_potential_evt_gendist3d_3trk_vtx1;
  TH2F* h_2D_potential_evt_llp1_daudxy;
  TH1F* h_potential_evt_llp1_min_dau_dxy;
  TH1F* h_potential_evt_vtx0_outseedtrk_trkdist;
  TH1F* h_potential_evt_vtx0_outseedtrk_trkdistsig;
  TH2F* h_2D_potential_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_trkdistsig;
  TH2F* h_2D_potential_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_trkdist;
  TH1F* h_potential_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_nsigmadxybs;
  TH1F* h_potential_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_trkdistsig;
  TH1F* h_potential_evt_vtx1_outseedtrk_trkdist;
  TH1F* h_potential_evt_vtx1_outseedtrk_trkdistsig;
  TH2F* h_2D_potential_evt_vtx1_max_outseedtrk_dxy_by_min_daudxy_trkdistsig;
  TH2F* h_2D_potential_evt_vtx1_max_outseedtrk_dxy_by_min_daudxy_trkdist;
  TH2F* h_2D_potential_evt_3trk_vtx1_max_outseedtrk_dxy_by_min_daudxy_trkdistsig;
  TH2F* h_2D_potential_evt_3trk_vtx1_max_outseedtrk_dxy_by_min_daudxy_trkdist;
  TH1F* h_potential_evt_vtx1_max_outseedtrk_dxy_by_min_daudxy_nsigmadxybs;
  TH1F* h_potential_evt_vtx1_max_outseedtrk_dxy_by_min_daudxy_trkdistsig;
  TH1F* h_potential_evt_3trk_vtx1_max_outseedtrk_dxy_by_min_daudxy_nsigmadxybs;
  TH1F* h_potential_evt_3trk_vtx1_max_outseedtrk_dxy_by_min_daudxy_trkdistsig;
  TH1F* h_potential_evt_llp01_gendist3d;
  TH1F* h_potential_evt_vtx01_dist3d;
  TH1F* h_potential_evt_vtx01_dist3dsig;
  TH1F* h_potential_evt_vtx0_seedtrk_dxybs;
  TH1F* h_potential_evt_vtx0_seedtrk_nsigmadxybs;
  TH1F* h_potential_evt_vtx0_seedtrk_trkdist;
  TH1F* h_potential_evt_vtx0_seedtrk_trkdistsig;
  TH1F* h_potential_evt_vtx0_outseedtrk_nsigmadxybs;
  TH1F* h_potential_evt_vtx0_outseedtrk_dxybs;
  TH1F* h_potential_evt_vtx1_seedtrk_dxybs;
  TH1F* h_potential_evt_vtx1_seedtrk_nsigmadxybs;
  TH1F* h_potential_evt_vtx1_seedtrk_trkdist;
  TH1F* h_potential_evt_vtx1_seedtrk_trkdistsig;
  TH1F* h_potential_evt_3trk_vtx1_seedtrk_dxybs;
  TH1F* h_potential_evt_3trk_vtx1_seedtrk_nsigmadxybs;
  TH1F* h_potential_evt_3trk_vtx1_seedtrk_trkdist;
  TH1F* h_potential_evt_3trk_vtx1_seedtrk_trkdistsig;
  TH2F* h_2D_potential_evt_vtx0_seedtrk_trkdist_other_trkdist;
  TH2F* h_2D_potential_evt_vtx0_seedtrk_trkdistsig_other_trkdistsig;
  TH1F* h_potential_evt_vtx0_mass;
  TH1F* h_potential_evt_vtx0_pT;
  TH1F* h_potential_evt_vtx0_bs2derr;
  TH1F* h_potential_evt_vtx0_dbv;
  TH1F* h_potential_evt_vtx1_mass;
  TH1F* h_potential_evt_vtx1_pT;
  TH1F* h_potential_evt_vtx1_bs2derr;
  TH1F* h_potential_evt_vtx1_dbv;
  TH1F* h_potential_evt_3trk_vtx1_mass;
  TH1F* h_potential_evt_3trk_vtx1_pT;
  TH1F* h_potential_evt_3trk_vtx1_bs2derr;
  TH1F* h_potential_evt_3trk_vtx1_dbv;
  TH1F* h_potential_evt_n2trksv;
  TH1F* h_potential_evt_gendist3dresllp0_2trksv;
  TH1F* h_potential_evt_gendist3dresllp1_2trksv;
  TH2F* h_2D_potential_evt_gendist3dresllp0_n2trksv;
  TH2F* h_2D_potential_evt_gendist3dresllp1_n2trksv;
  TH2F* h_2D_potential_evt_gendist3dres3trkllp1_n2trksv;
  TH1F* h_potential_evt_gendist3dresllp0_400um_2trksv_dbv;
  TH1F* h_potential_evt_gendist3dresllp0_400um_2trksv_absdphivtx0;
  TH1F* h_potential_evt_gendist3dresllp0_400um_2trksv_absdphillp0;
  TH1F* h_potential_evt_gendist3dresllp0_400um_2trksv_3ddistvtx0;
  TH1F* h_potential_evt_gendist3dresllp1_400um_2trksv_dbv;
  TH1F* h_potential_evt_gendist3dresllp1_400um_2trksv_absdphivtx1;
  TH1F* h_potential_evt_gendist3dresllp1_400um_2trksv_absdphillp1;
  TH1F* h_potential_evt_gendist3dresllp1_400um_2trksv_3ddistvtx1;
  TH1F* h_potential_evt_gendist3dres3trkllp1_400um_2trksv_dbv;
  TH1F* h_potential_evt_gendist3dres3trkllp1_400um_2trksv_absdphivtx1;
  TH1F* h_potential_evt_gendist3dres3trkllp1_400um_2trksv_absdphillp1;
  TH1F* h_potential_evt_gendist3dres3trkllp1_400um_2trksv_3ddistvtx1;

  TH2F* h_gen_decay;
  TH1F* h_gen_flavor_code;

  TH1F* h_nbquarks;
  TH1F* h_bquark_pt;
  TH1F* h_bquark_eta;
  TH1F* h_bquark_phi;
  TH1F* h_bquark_energy;
  TH1F* h_bquark_pairdphi;
  TH1F* h_bquark_pairdeta;

  TH1F* h_llp_r3d;
  TH1F* h_llp_ctau;
  TH1F* h_llp_gammabeta;
  

  

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
  h_nsv = fs->make<TH1F>("h_nsv", ";# of raw secondary vertices;arb. units", 20, 0, 20);
  h_ntrack_sv = fs->make<TH1F>("h_ntrack_sv", ";ntrack/ raw secondary vertices;arb. units", 20, 0, 20);
  h_sum_ntrack_sv = fs->make<TH1F>("h_sum_ntrack_sv", ";sum of all in-vertex seed tracks;arb. units", 50, 0, 50);
  h_sum_noutseedtrack = fs->make<TH1F>("h_sum_noutseedtrack", ";sum of all out-vertex seed tracks;arb. units", 50, 0, 50);
  h_2D_ntrk0_ntrk1 = fs->make<TH2F>("h_2D_ntrk0_ntrk1", ";# of tracks per vtx0; # of tracks per vtx1;arb. units", 20, 0, 20, 20, 0, 20);

  // for a cross-check 
  h_signal_evt_min_dau_dxy = fs->make<TH1F>("h_signal_evt_min_dau_dxy", "signal-like events;min(|dau's dxy|) (cm.)", 50, 0, 0.2);
  h_signal_evt_gendist3d_vtx0 = fs->make<TH1F>("h_signal_evt_gendist3d_vtx0", "signal-like events; gendist3d(closest llp-vtx, vtx0) (cm.)", 50, 0, 0.2);
  h_2D_signal_evt_llp0_daudxy = fs->make<TH2F>("h_2D_signal_evt_llp0_daudxy", "signal-like events;llp0's |dau0's dxy| (cm.); llp0's |dau1's dxy| (cm.);arb. units", 20, 0, 0.2, 20, 0, 0.2);
  h_signal_evt_llp0_min_dau_dxy = fs->make<TH1F>("h_signal_evt_llp0_min_dau_dxy", "signal-like events;llp0's min(|dau's dxy|) (cm.);arb. units", 50, 0, 0.05);
  h_signal_evt_vtx0_outseedtrk_trkdist = fs->make<TH1F>("h_signal_evt_vtx0_outseedtrk_trkdist", "signal-like events; outside seed track's missdist_{vtx0} (cm.)", 50, 0, 0.2);
  h_signal_evt_vtx0_outseedtrk_trkdistsig = fs->make<TH1F>("h_signal_evt_vtx0_outseedtrk_trkdistsig", "signal-like events; outside seed track's n#sigma missdist_{vtx0}", 80, 0, 10.0);
  h_2D_signal_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_trkdistsig = fs->make<TH2F>("h_2D_signal_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_trkdistsig", "signal-like events; max(outside seed track's dxybs(< min(vtx0 |daudxy|)) cm. ; its vtx0's n#sigma missdist_{vtx0}", 20, 0.0, 0.2, 50, 0, 10.0);
  h_2D_signal_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_trkdist = fs->make<TH2F>("h_2D_signal_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_trkdist", "signal-like events; max(outside seed track's dxybs(< min(vtx0 |daudxy|)) cm. ; its vtx0's missdist_{vtx0} (cm.)", 20, 0.0, 0.2, 50, 0, 0.2);
  h_signal_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_nsigmadxybs = fs->make<TH1F>("h_signal_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_nsigmadxybs", "signal-like events;mindxydau-vtx0 outside seed track's n#sigma missdist_{bsp} ; arb. units", 20, 0.0, 10.0);
  h_signal_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_trkdistsig = fs->make<TH1F>("h_signal_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_trkdistsig", "signal-like events;mindxydau-vtx0 outside seed track's n#sigma missdist_{vtx0} ; arb. units", 20, 0.0, 10.0);
  h_signal_evt_llp01_gendist3d = fs->make<TH1F>("h_signal_evt_llp01_gendist3d", "signal-like events; gendist3d(llp0, llp1) (cm.)", 50, 0, 0.2);
  h_signal_evt_vtx01_dist3d = fs->make<TH1F>("h_signal_evt_vtx01_dist3d", "signal-like events; dist3d(vtx0, vtx1) (cm.)", 50, 0, 0.2);
  h_signal_evt_vtx01_dist3dsig = fs->make<TH1F>("h_signal_evt_vtx01_dist3dsig", "signal-like events; n#sigma dist3d(vtx0, vtx1) ", 80, 0, 10.0);
  h_signal_evt_vtx0_outseedtrk_nsigmadxybs = fs->make<TH1F>("h_signal_evt_vtx0_outseedtrk_nsigmadxybs", "signal-like events;outside seed track's n#sigma missdist_{bsp} ; arb. units", 20, 0.0, 10.0);
  h_signal_evt_vtx0_outseedtrk_dxybs = fs->make<TH1F>("h_signal_evt_vtx0_outseedtrk_dxybs", "signal-like events;outside seed track's dxybs (cm.)", 100, 0.0, 0.2);
  h_signal_evt_vtx0_seedtrk_dxybs = fs->make<TH1F>("h_signal_evt_vtx0_seedtrk_dxybs", "signal-like events;vtx0 seed track's dxybs (cm.)", 100, 0.0, 0.2);
  h_signal_evt_vtx0_seedtrk_nsigmadxybs = fs->make<TH1F>("h_signal_evt_vtx0_seedtrk_nsigmadxybs", "signal-like events;vtx0 seed track's n#sigma missdist_{bsp} ; arb. units", 20, 0.0, 10.0);
  h_signal_evt_vtx0_seedtrk_trkdist = fs->make<TH1F>("h_signal_evt_vtx0_seedtrk_trkdist", "signal-like events;vtx0 seed track's missdist_{vtx0} (cm.)", 50, 0, 0.2);
  h_signal_evt_vtx0_seedtrk_trkdistsig = fs->make<TH1F>("h_signal_evt_vtx0_seedtrk_trkdistsig", "signal-like events;vtx0 seed track's n#sigma missdist_{vtx0}", 80, 0, 10.0);
  h_signal_evt_vtx0_mass = fs->make<TH1F>("h_signal_evt_vtx0_mass", "signal-like events;vtx0 tracks-plus-jets-by-ntracks mass (GeV); ", 100, 0, 80);
  h_signal_evt_vtx0_pT = fs->make<TH1F>("h_signal_evt_vtx0_pT", "signal-like events;vtx0 tracks-plus-jets-by-ntracks p_{T} (GeV); ", 100, 0, 80);
  h_signal_evt_vtx0_dbv = fs->make<TH1F>("h_signal_evt_vtx0_dbv", "signal-like events;dBV/vtx0 (cm.); ", 30, 0, 0.3);
  h_signal_evt_vtx0_bs2derr = fs->make<TH1F>("h_signal_evt_vtx0_bs2derr", "signal-like events;bs2derr/vtx0(cm.); ", 50, 0, 0.05);
  h_signal_evt_n2trksv = fs->make<TH1F>("h_signal_evt_n2trksv", "signal-like events;# of 2-trk vertices (exclude top two);arb. units", 20, 0, 20);
  h_signal_evt_gendist3dresllp0_2trksv = fs->make<TH1F>("h_signal_evt_gendist3dresllp0_2trksv", "signal-like events;gendist3dllp0 to 2-trk vertices (exclude top two) cm.", 100, 0.0, 0.1);
  h_2D_signal_evt_gendist3dresllp0_n2trksv = fs->make<TH2F>("h_2D_signal_evt_gendist3dresllp0_n2trksv", "signal-like events;resolution cutoff of gendist3dllp0 cm.; # of 2-trk vertices within a cutoff", 10, 0.0, 0.04, 20, 0, 20);
  h_signal_evt_gendist3dresllp0_400um_2trksv_dbv = fs->make<TH1F>("h_signal_evt_gendist3dresllp0_400um_2trksv_dbv", "signal-like events;dBV/2trk-vtx2+ w/ 400um-genllp0 (cm.); ", 50, 0, 0.1);
  h_signal_evt_gendist3dresllp0_400um_2trksv_absdphivtx0 = fs->make<TH1F>("h_signal_evt_gendist3dresllp0_400um_2trksv_absdphivtx0", "signal-like events;|#Delta(phi_{2trk-vtx2+}, phi_{vtx0})| w/ 400um-genllp0 ; ", 315, 0, 3.15);
  h_signal_evt_gendist3dresllp0_400um_2trksv_absdphillp0 = fs->make<TH1F>("h_signal_evt_gendist3dresllp0_400um_2trksv_absdphillp0", "signal-like events;|#Delta(phi_{2trk-vtx2+}, phi_{llp0})| w/ 400um-genllp0 ; ", 315, 0, 3.15);
  h_signal_evt_gendist3dresllp0_400um_2trksv_3ddistvtx0 = fs->make<TH1F>("h_signal_evt_gendist3dresllp0_400um_2trksv_3ddistvtx0", "signal-like events;dist3d(vtx0, 2trk-vtx2+ w/ 400um-genllp0) (cm.); ", 50, 0, 0.2);


  // for improvement of signal eff. 
  h_potential_evt_min_dau_dxy = fs->make<TH1F>("h_potential_evt_min_dau_dxy", "potentially-recover events;min(|dau's dxy|) (cm.)", 50, 0, 0.2);
  h_potential_evt_gendist3d_vtx0 = fs->make<TH1F>("h_potential_evt_gendist3d_vtx0", "potentially-recover events; gendist3d(closest llp-vtx, vtx0) (cm.)", 50, 0, 0.2);
  h_2D_potential_evt_llp0_daudxy = fs->make<TH2F>("h_2D_potential_evt_llp0_daudxy", "potentially-recover events;llp0's |dau0's dxy| (cm.); llp0's |dau1's dxy| (cm.);arb. units", 20, 0, 0.2, 20, 0, 0.2);
  h_potential_evt_llp0_min_dau_dxy = fs->make<TH1F>("h_potential_evt_llp0_min_dau_dxy", "potentially-recover events;llp0's min(|dau's dxy|) (cm.);arb. units", 50, 0, 0.05);
  h_2D_potential_evt_llp1_daudxy = fs->make<TH2F>("h_2D_potential_evt_llp1_daudxy", "potentially-recover events;llp1's |dau2's dxy| (cm.); llp1's |dau3's dxy| (cm.);arb. units", 20, 0, 0.2, 20, 0, 0.2);
  h_potential_evt_llp1_min_dau_dxy = fs->make<TH1F>("h_potential_evt_llp1_min_dau_dxy", "potentially-recover events;llp1's min(|dau's dxy|) (cm.);arb. units", 50, 0, 0.05);
  h_potential_evt_gendist3d_vtx1 = fs->make<TH1F>("h_potential_evt_gendist3d_vtx1", "potentially-recover events; gendist3d(closest llp-vtx, vtx1) (cm.)", 50, 0, 0.2);
  h_potential_evt_gendist3d_3trk_vtx1 = fs->make<TH1F>("h_potential_evt_gendist3d_3trk_vtx1", "potentially-recover events; gendist3d(closest llp-vtx, >=3trk vtx1) (cm.)", 50, 0, 0.2);
  h_potential_evt_vtx0_outseedtrk_trkdist = fs->make<TH1F>("h_potential_evt_vtx0_outseedtrk_trkdist", "potentially-recover events; outside seed track's missdist_{vtx0} (cm.)", 50, 0, 0.2);
  h_potential_evt_vtx0_outseedtrk_trkdistsig = fs->make<TH1F>("h_potential_evt_vtx0_outseedtrk_trkdistsig", "potentially-recover events; outside seed track's n#sigma missdist_{vtx0}", 80, 0, 10.0);
  h_2D_potential_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_trkdistsig = fs->make<TH2F>("h_2D_potential_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_trkdistsig", "potentially-recover events; max(outside seed track's dxybs(< min(vtx0 |daudxy|)) cm. ; its n#sigma missdist_{vtx0}", 20, 0.0, 0.2, 50, 0, 10.0);
  h_2D_potential_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_trkdist = fs->make<TH2F>("h_2D_potential_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_trkdist", "potentially-recover events; max(outside seed track's dxybs(< min(vtx0 |daudxy|)) cm. ; its missdist_{vtx0} (cm.)", 20, 0.0, 0.2, 50, 0, 0.2);
  h_potential_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_nsigmadxybs = fs->make<TH1F>("h_potential_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_nsigmadxybs", "potentially-recover events;mindxydau-vtx0 outside seed track's n#sigma missdist_{bsp} ; arb. units", 20, 0.0, 10.0);
  h_potential_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_trkdistsig = fs->make<TH1F>("h_potential_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_trkdistsig", "potentially-recover events;mindxydau-vtx0 outside seed track's n#sigma missdist_{vtx0} ; arb. units", 20, 0.0, 10.0);
  h_potential_evt_vtx1_outseedtrk_trkdist = fs->make<TH1F>("h_potential_evt_vtx1_outseedtrk_trkdist", "potentially-recover events; vtx1 outside seed track's missdist_{vtx1} (cm.)", 50, 0, 0.2);
  h_potential_evt_vtx1_outseedtrk_trkdistsig = fs->make<TH1F>("h_potential_evt_vtx1_outseedtrk_trkdistsig", "potentially-recover events; vtx1 outside seed track's n#sigma missdist_{vtx1}", 80, 0, 10.0);
  h_2D_potential_evt_vtx1_max_outseedtrk_dxy_by_min_daudxy_trkdistsig = fs->make<TH2F>("h_2D_potential_evt_vtx1_max_outseedtrk_dxy_by_min_daudxy_trkdistsig", "potentially-recover events; max(outside seed track's dxybs(< min(vtx1 |daudxy|)) cm. ; its n#sigma missdist_{vtx1}", 20, 0.0, 0.2, 50, 0, 10.0);
  h_2D_potential_evt_3trk_vtx1_max_outseedtrk_dxy_by_min_daudxy_trkdistsig = fs->make<TH2F>("h_2D_potential_evt_3trk_vtx1_max_outseedtrk_dxy_by_min_daudxy_trkdistsig", "potentially-recover events; max(outside seed track's dxybs(< min(vtx1 |daudxy|)) cm. ; its n#sigma missdist_{>=3trk-vtx1}", 20, 0.0, 0.2, 50, 0, 10.0);
  h_2D_potential_evt_vtx1_max_outseedtrk_dxy_by_min_daudxy_trkdist = fs->make<TH2F>("h_2D_potential_evt_vtx1_max_outseedtrk_dxy_by_min_daudxy_trkdist", "potentially-recover events; max(outside seed track's dxybs(< min(vtx1 |daudxy|)) cm. ; its missdist_{vtx1} (cm.)", 20, 0.0, 0.2, 50, 0, 0.2);
  h_2D_potential_evt_3trk_vtx1_max_outseedtrk_dxy_by_min_daudxy_trkdist = fs->make<TH2F>("h_2D_potential_evt_3trk_vtx1_max_outseedtrk_dxy_by_min_daudxy_trkdist", "potentially-recover events; max(outside seed track's dxybs(< min(vtx1 |daudxy|)) cm. ; its missdist_{>=3trk-vtx1} (cm.)", 20, 0.0, 0.2, 50, 0, 0.2);
  h_potential_evt_vtx1_max_outseedtrk_dxy_by_min_daudxy_nsigmadxybs = fs->make<TH1F>("h_potential_evt_vtx1_max_outseedtrk_dxy_by_min_daudxy_nsigmadxybs", "potentially-recover events;mindxydau-vtx1 outside seed track's n#sigma missdist_{bsp} ; arb. units", 20, 0.0, 10.0);
  h_potential_evt_vtx1_max_outseedtrk_dxy_by_min_daudxy_trkdistsig = fs->make<TH1F>("h_potential_evt_vtx1_max_outseedtrk_dxy_by_min_daudxy_trkdistsig", "potentially-recover events;mindxydau-vtx1 outside seed track's n#sigma missdist_{vtx1} ; arb. units", 20, 0.0, 10.0);
  h_potential_evt_3trk_vtx1_max_outseedtrk_dxy_by_min_daudxy_nsigmadxybs = fs->make<TH1F>("h_potential_evt_3trk_vtx1_max_outseedtrk_dxy_by_min_daudxy_nsigmadxybs", "potentially-recover events;mindxydau->=3trk-vtx1 outside seed track's n#sigma missdist_{bsp} ; arb. units", 20, 0.0, 10.0);
  h_potential_evt_3trk_vtx1_max_outseedtrk_dxy_by_min_daudxy_trkdistsig = fs->make<TH1F>("h_potential_evt_3trk_vtx1_max_outseedtrk_dxy_by_min_daudxy_trkdistsig", "potentially-recover events;mindxydau->=3trk-vtx1 outside seed track's n#sigma missdist_{>=3trk-vtx1} ; arb. units", 20, 0.0, 10.0);
  h_potential_evt_llp01_gendist3d = fs->make<TH1F>("h_potential_evt_llp01_gendist3d", "potentially-recover events; gendist3d(llp0, llp1) (cm.)", 50, 0, 0.2);
  h_potential_evt_vtx01_dist3d = fs->make<TH1F>("h_potential_evt_vtx01_dist3d", "potentially-recover events; dist3d(vtx0, vtx1) (cm.)", 50, 0, 0.2);
  h_potential_evt_vtx01_dist3dsig = fs->make<TH1F>("h_potential_evt_vtx01_dist3dsig", "potentially-recover events; n#sigma dist3d(vtx0, vtx1) ", 80, 0, 10.0);
  h_potential_evt_vtx0_seedtrk_dxybs = fs->make<TH1F>("h_potential_evt_vtx0_seedtrk_dxybs", "potentially-recover events;vtx0 seed track's dxybs (cm.)", 100, 0.0, 0.2);
  h_potential_evt_vtx0_seedtrk_nsigmadxybs = fs->make<TH1F>("h_potential_evt_vtx0_seedtrk_nsigmadxybs", "potentially-recover events;vtx0 seed track's n#sigma missdist_{bsp} ; arb. units", 20, 0.0, 10.0);
  h_potential_evt_vtx0_seedtrk_trkdist = fs->make<TH1F>("h_potential_evt_vtx0_seedtrk_trkdist", "potentially-recover events;vtx0 seed track's missdist_{vtx0} (cm.)", 50, 0, 0.2);
  h_potential_evt_vtx0_seedtrk_trkdistsig = fs->make<TH1F>("h_potential_evt_vtx0_seedtrk_trkdistsig", "potentially-recover events;vtx0 seed track's n#sigma missdist_{vtx0}", 80, 0, 10.0);
  h_potential_evt_vtx0_outseedtrk_nsigmadxybs = fs->make<TH1F>("h_potential_evt_vtx0_outseedtrk_nsigmadxybs", "potentially-recover events;outside seed track's n#sigma missdist_{bsp} ; arb. units", 20, 0.0, 10.0);
  h_potential_evt_vtx0_outseedtrk_dxybs = fs->make<TH1F>("h_potential_evt_vtx0_outseedtrk_dxybs", "potentially-recover events;outside seed track's dxybs (cm.)", 100, 0.0, 0.2);
  h_potential_evt_vtx1_seedtrk_nsigmadxybs = fs->make<TH1F>("h_potential_evt_vtx1_seedtrk_nsigmadxybs", "potentially-recover events;vtx1 seed track's n#sigma missdist_{bsp} ; arb. units", 20, 0.0, 10.0);
  h_potential_evt_vtx1_seedtrk_dxybs = fs->make<TH1F>("h_potential_evt_vtx1_seedtrk_dxybs", "potentially-recover events;vtx1 seed track's dxybs (cm.)", 100, 0.0, 0.2);
  h_potential_evt_vtx1_seedtrk_trkdist = fs->make<TH1F>("h_potential_evt_vtx1_seedtrk_trkdist", "potentially-recover events;vtx1 seed track's missdist_{vtx1} (cm.)", 50, 0, 0.2);
  h_potential_evt_vtx1_seedtrk_trkdistsig = fs->make<TH1F>("h_potential_evt_vtx1_seedtrk_trkdistsig", "potentially-recover events;vtx1 seed track's n#sigma missdist_{vtx1}", 80, 0, 10.0);
  h_potential_evt_3trk_vtx1_seedtrk_nsigmadxybs = fs->make<TH1F>("h_potential_evt_3trk_vtx1_seedtrk_nsigmadxybs", "potentially-recover events;>=3trk-vtx1 seed track's n#sigma missdist_{bsp} ; arb. units", 20, 0.0, 10.0);
  h_potential_evt_3trk_vtx1_seedtrk_dxybs = fs->make<TH1F>("h_potential_evt_3trk_vtx1_seedtrk_dxybs", "potentially-recover events;>=3trk-vtx1 seed track's dxybs (cm.)", 100, 0.0, 0.2);
  h_potential_evt_3trk_vtx1_seedtrk_trkdist = fs->make<TH1F>("h_potential_evt_3trk_vtx1_seedtrk_trkdist", "potentially-recover events;>=3trk-vtx1 seed track's missdist_{vtx1} (cm.)", 50, 0, 0.2);
  h_potential_evt_3trk_vtx1_seedtrk_trkdistsig = fs->make<TH1F>("h_potential_evt_3trk_vtx1_seedtrk_trkdistsig", "potentially-recover events;>=3trk-vtx1 seed track's n#sigma missdist_{vtx1}", 80, 0, 10.0);
  h_2D_potential_evt_vtx0_seedtrk_trkdist_other_trkdist = fs->make<TH2F>("h_2D_potential_evt_vtx0_seedtrk_trkdist_other_trkdist", ";vtx0 seed track's missdist_{vtx0} (cm.); vtx0 seed track's missdist_{vtx1} (cm.);arb. units", 20, 0, 0.2, 20, 0, 0.2);
  h_2D_potential_evt_vtx0_seedtrk_trkdistsig_other_trkdistsig = fs->make<TH2F>("h_2D_potential_evt_vtx0_seedtrk_trkdistsig_other_trkdistsig", ";vtx0 seed track's n#sigma missdist_{vtx0}; vtx0 seed track's n#sigma missdist_{vtx1};arb. units", 30, 0, 10.0, 30, 0, 10.0);
  h_potential_evt_vtx0_mass = fs->make<TH1F>("h_potential_evt_vtx0_mass", "potentially-recover events;vtx0 tracks-plus-jets-by-ntracks mass (GeV); ", 100, 0, 80);
  h_potential_evt_vtx0_pT = fs->make<TH1F>("h_potential_evt_vtx0_pT", "potentially-recover events;vtx0 tracks-plus-jets-by-ntracks p_{T} (GeV); ", 100, 0, 80);
  h_potential_evt_vtx0_dbv = fs->make<TH1F>("h_potential_evt_vtx0_dbv", "potentially-recover events;dBV/vtx0 (cm.); ", 30, 0, 0.3);
  h_potential_evt_vtx0_bs2derr = fs->make<TH1F>("h_potential_evt_vtx0_bs2derr", "potentially-recover events;bs2derr/vtx0 (cm.); ", 50, 0, 0.05);
  h_potential_evt_vtx1_mass = fs->make<TH1F>("h_potential_evt_vtx1_mass", "potentially-recover events;vtx1 tracks-plus-jets-by-ntracks mass (GeV); ", 100, 0, 80);
  h_potential_evt_vtx1_pT = fs->make<TH1F>("h_potential_evt_vtx1_pT", "potentially-recover events;vtx1 tracks-plus-jets-by-ntracks p_{T} (GeV); ", 100, 0, 80);
  h_potential_evt_vtx1_dbv = fs->make<TH1F>("h_potential_evt_vtx1_dbv", "potentially-recover events;dBV/vtx1 (cm.); ", 30, 0, 0.3);
  h_potential_evt_vtx1_bs2derr = fs->make<TH1F>("h_potential_evt_vtx1_bs2derr", "potentially-recover events;bs2derr/vtx1 (cm.); ", 50, 0, 0.05);
  h_potential_evt_3trk_vtx1_mass = fs->make<TH1F>("h_potential_evt_3trk_vtx1_mass", "potentially-recover events;>=3trk vtx1 tracks-plus-jets-by-ntracks mass (GeV); ", 100, 0, 80);
  h_potential_evt_3trk_vtx1_pT = fs->make<TH1F>("h_potential_evt_3trk_vtx1_pT", "potentially-recover events;>=3trk vtx1 tracks-plus-jets-by-ntracks p_{T} (GeV); ", 100, 0, 80);
  h_potential_evt_3trk_vtx1_dbv = fs->make<TH1F>("h_potential_evt_3trk_vtx1_dbv", "potentially-recover events;dBV/>=3trk vtx1 (cm.); ", 30, 0, 0.3);
  h_potential_evt_3trk_vtx1_bs2derr = fs->make<TH1F>("h_potential_evt_3trk_vtx1_bs2derr", "potentially-recover events;bs2derr/>=3trk vtx1 (cm.); ", 50, 0, 0.05);
  h_potential_evt_n2trksv = fs->make<TH1F>("h_potential_evt_n2trksv", "potentially-recover events;# of 2-trk vertices (exclude top two);arb. units", 20, 0, 20);
  h_potential_evt_gendist3dresllp0_2trksv = fs->make<TH1F>("h_potential_evt_gendist3dresllp0_2trksv", "potentially-recover events;gendist3dllp0 to 2-trk vertices (exclude top two) cm.", 100, 0.0, 0.1);
  h_potential_evt_gendist3dresllp1_2trksv = fs->make<TH1F>("h_potential_evt_gendist3dresllp1_2trksv", "potentially-recover events;gendist3dllp1 to 2-trk vertices (exclude top two) cm.", 100, 0.0, 0.1);
  h_2D_potential_evt_gendist3dresllp0_n2trksv = fs->make<TH2F>("h_2D_potential_evt_gendist3dresllp0_n2trksv", "potentially-recover events;resolution cutoff of gendist3dllp0 cm.; # of 2-trk vertices within a cutoff", 10, 0.0, 0.04, 20, 0, 20);
  h_2D_potential_evt_gendist3dresllp1_n2trksv = fs->make<TH2F>("h_2D_potential_evt_gendist3dresllp1_n2trksv", "potentially-recover events;resolution cutoff of gendist3dllp1 cm.; # of 2-trk vertices within a cutoff", 10, 0.0, 0.04, 20, 0, 20);
  h_2D_potential_evt_gendist3dres3trkllp1_n2trksv = fs->make<TH2F>("h_2D_potential_evt_gendist3dres3trkllp1_n2trksv", "potentially-recover events;resolution cutoff of gendist3dllp1 w/ >=3-trk vtx1 cm.; # of 2-trk vertices within a cutoff", 10, 0.0, 0.04, 20, 0, 20);
  h_potential_evt_gendist3dresllp0_400um_2trksv_dbv = fs->make<TH1F>("h_potential_evt_gendist3dresllp0_400um_2trksv_dbv", "potentially-recover events;dBV/2trk-vtx2+ w/ 400um-genllp0 (cm.); ", 50, 0, 0.1);
  h_potential_evt_gendist3dresllp0_400um_2trksv_absdphivtx0 = fs->make<TH1F>("h_potential_evt_gendist3dresllp0_400um_2trksv_absdphivtx0", "potentially-recover events;|#Delta(phi_{2trk-vtx2+}, phi_{vtx0})| w/ 400um-genllp0 ; ", 315, 0, 3.15);
  h_potential_evt_gendist3dresllp0_400um_2trksv_absdphillp0 = fs->make<TH1F>("h_potential_evt_gendist3dresllp0_400um_2trksv_absdphivtx0", "potentially-recover events;|#Delta(phi_{2trk-vtx2+}, phi_{llp0})| w/ 400um-genllp0 ; ", 315, 0, 3.15);
  h_potential_evt_gendist3dresllp0_400um_2trksv_3ddistvtx0 = fs->make<TH1F>("h_potential_evt_gendist3dresllp0_400um_2trksv_3ddistvtx0", "potentially-recover events;dist3d(vtx0, 2trk-vtx2+ w/ 400um-genllp0) (cm.); ", 50, 0, 0.2);
  h_potential_evt_gendist3dresllp1_400um_2trksv_dbv = fs->make<TH1F>("h_potential_evt_gendist3dresllp1_400um_2trksv_dbv", "potentially-recover events;dBV/2trk-vtx2+ w/ 400um-genllp1 (cm.); ", 50, 0, 0.1);
  h_potential_evt_gendist3dresllp1_400um_2trksv_absdphivtx1 = fs->make<TH1F>("h_potential_evt_gendist3dresllp1_400um_2trksv_absdphivtx1", "potentially-recover events;|#Delta(phi_{2trk-vtx2+}, phi_{vtx1})| w/ 400um-genllp1 ; ", 315, 0, 3.15);
  h_potential_evt_gendist3dresllp1_400um_2trksv_absdphillp1 = fs->make<TH1F>("h_potential_evt_gendist3dresllp1_400um_2trksv_absdphillp1", "potentially-recover events;|#Delta(phi_{2trk-vtx2+}, phi_{llp1})| w/ 400um-genllp1 ; ", 315, 0, 3.15);
  h_potential_evt_gendist3dresllp1_400um_2trksv_3ddistvtx1 = fs->make<TH1F>("h_potential_evt_gendist3dresllp1_400um_2trksv_3ddistvtx1", "potentially-recover events;dist3d(vtx1, 2trk-vtx2+ w/ 400um-genllp1) (cm.); ", 50, 0, 0.2);
  h_potential_evt_gendist3dres3trkllp1_400um_2trksv_dbv = fs->make<TH1F>("h_potential_evt_gendist3dres3trkllp1_400um_2trksv_dbv", "potentially-recover events;dBV/2trk-vtx2+ w/ 400um-genllp1-match>=3trkvtx1 (cm.); ", 50, 0, 0.1);
  h_potential_evt_gendist3dres3trkllp1_400um_2trksv_absdphivtx1 = fs->make<TH1F>("h_potential_evt_gendist3dres3trkllp1_400um_2trksv_absdphivtx1", "potentially-recover events;|#Delta(phi_{2trk-vtx2+}, phi_{vtx1})| w/ 400um-genllp1-match>=3trkvtx1 ; ", 315, 0, 3.15);
  h_potential_evt_gendist3dres3trkllp1_400um_2trksv_absdphillp1 = fs->make<TH1F>("h_potential_evt_gendist3dres3trkllp1_400um_2trksv_absdphillp1", "potentially-recover events;|#Delta(phi_{2trk-vtx2+}, phi_{llp1})| w/ 400um-genllp1-match>=3trkvtx1 ; ", 315, 0, 3.15);
  h_potential_evt_gendist3dres3trkllp1_400um_2trksv_3ddistvtx1 = fs->make<TH1F>("h_potential_evt_gendist3dres3trkllp1_400um_2trksv_3ddistvtx1", "potentially-recover events;dist3d(vtx1, 2trk-vtx2+ w/ 400um-genllp1-match>=3trkvtx1) (cm.); ", 50, 0, 0.2);


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
  h_llp_r3d = fs->make<TH1F>("h_llp_r3d", ";dist3d(PV, GEN-llp decay point) (cm);events/0.1 mm", 200, 0, 2);
  h_llp_ctau = fs->make<TH1F>("h_llp_ctau", ";llp's ctau (cm);events/0.1 mm", 200, 0, 2);
  h_llp_gammabeta = fs->make<TH1F>("h_llp_gammabeta", ";llp's gammabeta;events/0.1 mm", 100, 0, 20);
  
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
  //std::cout << "MFVEventHistos "  << " run " << event.id().run() << " lumi " << event.luminosityBlock() << " event " << event.id().event() << "\n"; 
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
  /*
  const double r3d0 = 0.0;//mag(mevent->gen_lsp_decay[0] - mevent->gen_pv[0], mevent->gen_lsp_decay[1] - mevent->gen_pv[1], mevent->gen_lsp_decay[2] - mevent->gen_pv[2]);
  const double lspbeta0 = 0.0;//mevent->gen_lsps[0].P() / mevent->gen_lsps[0].Energy();
  const double lspbetagamma0 = 0.0;//lspbeta0 / sqrt(1 - lspbeta0 * lspbeta0);
  //const double ctau0 = r3d0 / lspbetagamma0;

  const double r3d1 = 0.0;//mag(mevent->gen_lsp_decay[3] - mevent->gen_pv[0], mevent->gen_lsp_decay[4] - mevent->gen_pv[1], mevent->gen_lsp_decay[5] - mevent->gen_pv[2]);
  const double lspbeta1 = 0.0;//mevent->gen_lsps[1].P() / mevent->gen_lsps[1].Energy();
  const double lspbetagamma1 = 0.0;//lspbeta1 / sqrt(1 - lspbeta1 * lspbeta1);
  //const double ctau1 = r3d1 / lspbetagamma1;

  //std::cout << "*** START GEN-level information ***" << std::endl; 
  double min_dist3d_genlsp0sv = 5.0;
  int isv_llp0 = -99;
  //int gensv0_ntrack = 0;
  double min_dist3d_genlsp1sv = 5.0;
  int isv_llp1 = -99;
  //int gensv1_ntrack = 0;
  double gendist3dvtx0 = 5.0;
  double gendist3dvtx1 = 5.0;
  double dau0_dxy = 99.0;
  double dau1_dxy = 99.0;
  double dau2_dxy = 99.0;
  double dau3_dxy = 99.0;
  int sum_ntrack = 0.0;
  std::vector<double> vec_exact_outsed_track_nsigmadxy = {};
  std::vector<int> vec_i2trksv = {};
  std::vector<double> vec_2trksv_gendist3dllpvtx0 = {};
  std::vector<double> vec_2trksv_gendist3dllpvtx1 = {};
  std::vector<double> vec_2trksv_absdphiauxllp0 = {};
  std::vector<double> vec_2trksv_absdphiauxllp1 = {};
  bool Isllp0vtx0 = true; 

  for (int isv = 0; isv < nsv; ++isv) {
	  const MFVVertexAux& aux = auxes->at(isv);
	  h_ntrack_sv->Fill(aux.ntracks(), w);
	  sum_ntrack += aux.ntracks(); 
	  double genlsp0_dist3d = 0.0; //mag(mevent->gen_lsp_decay[0] - aux.x, mevent->gen_lsp_decay[1] - aux.y, mevent->gen_lsp_decay[2] - aux.z);
	  double genlsp1_dist3d = 0.0; // mag(mevent->gen_lsp_decay[3] - aux.x, mevent->gen_lsp_decay[4] - aux.y, mevent->gen_lsp_decay[5] - aux.z);
	  if (genlsp0_dist3d < min_dist3d_genlsp0sv) {
		  isv_llp0 = isv; 
		  min_dist3d_genlsp0sv = genlsp0_dist3d;
          //gensv0_ntrack = aux.ntracks();
	  }
	  if (genlsp1_dist3d < min_dist3d_genlsp1sv) {
		  isv_llp1 = isv;
		  min_dist3d_genlsp1sv = genlsp1_dist3d;
          //gensv1_ntrack = aux.ntracks();
	  }

	  
	  if (isv == 0 && nsv >= 2) {
		  const MFVVertexAux& aux1 = auxes->at(1);

		  if (genlsp0_dist3d < genlsp1_dist3d) {
			  gendist3dvtx0 = genlsp0_dist3d;
			  gendist3dvtx1 = 0.0;// mag(mevent->gen_lsp_decay[3] - aux1.x, mevent->gen_lsp_decay[4] - aux1.y, mevent->gen_lsp_decay[5] - aux1.z);
			  dau0_dxy = 0.0;// fabs(mag(mevent->gen_lsp_decay[0] - mevent->gen_pv[0], mevent->gen_lsp_decay[1] - mevent->gen_pv[1]) * sin(mevent->gen_daughters[0].Phi() - atan2(mevent->gen_lsp_decay[1] - mevent->gen_pv[1], mevent->gen_lsp_decay[0] - mevent->gen_pv[0])));
			  dau1_dxy = 0.0;// fabs(mag(mevent->gen_lsp_decay[0] - mevent->gen_pv[0], mevent->gen_lsp_decay[1] - mevent->gen_pv[1]) * sin(mevent->gen_daughters[1].Phi() - atan2(mevent->gen_lsp_decay[1] - mevent->gen_pv[1], mevent->gen_lsp_decay[0] - mevent->gen_pv[0])));
			  dau2_dxy = 0.0;// fabs(mag(mevent->gen_lsp_decay[3] - mevent->gen_pv[0], mevent->gen_lsp_decay[4] - mevent->gen_pv[1]) * sin(mevent->gen_daughters[2].Phi() - atan2(mevent->gen_lsp_decay[4] - mevent->gen_pv[1], mevent->gen_lsp_decay[3] - mevent->gen_pv[0])));
			  dau3_dxy = 0.0;// fabs(mag(mevent->gen_lsp_decay[3] - mevent->gen_pv[0], mevent->gen_lsp_decay[4] - mevent->gen_pv[1]) * sin(mevent->gen_daughters[3].Phi() - atan2(mevent->gen_lsp_decay[4] - mevent->gen_pv[1], mevent->gen_lsp_decay[3] - mevent->gen_pv[0])));
			  
			  
		  }
		  else {
			  Isllp0vtx0 = false; 
			  gendist3dvtx0 = genlsp1_dist3d;
			  gendist3dvtx1 = 0.0;//mag(mevent->gen_lsp_decay[0] - aux1.x, mevent->gen_lsp_decay[1] - aux1.y, mevent->gen_lsp_decay[2] - aux1.z);
			  dau2_dxy = 0.0;//fabs(mag(mevent->gen_lsp_decay[0] - mevent->gen_pv[0], mevent->gen_lsp_decay[1] - mevent->gen_pv[1]) * sin(mevent->gen_daughters[0].Phi() - atan2(mevent->gen_lsp_decay[1] - mevent->gen_pv[1], mevent->gen_lsp_decay[0] - mevent->gen_pv[0])));
			  dau3_dxy = 0.0;//fabs(mag(mevent->gen_lsp_decay[0] - mevent->gen_pv[0], mevent->gen_lsp_decay[1] - mevent->gen_pv[1]) * sin(mevent->gen_daughters[1].Phi() - atan2(mevent->gen_lsp_decay[1] - mevent->gen_pv[1], mevent->gen_lsp_decay[0] - mevent->gen_pv[0])));
			  dau0_dxy = 0.0;//fabs(mag(mevent->gen_lsp_decay[3] - mevent->gen_pv[0], mevent->gen_lsp_decay[4] - mevent->gen_pv[1]) * sin(mevent->gen_daughters[2].Phi() - atan2(mevent->gen_lsp_decay[4] - mevent->gen_pv[1], mevent->gen_lsp_decay[3] - mevent->gen_pv[0])));
			  dau1_dxy = 0.0;//fabs(mag(mevent->gen_lsp_decay[3] - mevent->gen_pv[0], mevent->gen_lsp_decay[4] - mevent->gen_pv[1]) * sin(mevent->gen_daughters[3].Phi() - atan2(mevent->gen_lsp_decay[4] - mevent->gen_pv[1], mevent->gen_lsp_decay[3] - mevent->gen_pv[0])));
			  
		  }
	  }

	  if (aux.ntracks() == 2) {
		  if (isv >= 2) {
			  vec_i2trksv.push_back(isv);
			  if (Isllp0vtx0) {
				  //vec_2trksv_gendist3dllpvtx0.push_back(mag(mevent->gen_lsp_decay[0] - aux.x, mevent->gen_lsp_decay[1] - aux.y, mevent->gen_lsp_decay[2] - aux.z));
				  //vec_2trksv_gendist3dllpvtx1.push_back(mag(mevent->gen_lsp_decay[3] - aux.x, mevent->gen_lsp_decay[4] - aux.y, mevent->gen_lsp_decay[5] - aux.z));
				  TVector3 aux_flight = TVector3(aux.x - mevent->bsx_at_z(aux.z), aux.y - mevent->bsy_at_z(aux.z), aux.z - mevent->bsz);
				  double absdphiauxllp0 = 0.0;//fabs(mevent->gen_lsp_p4(0).Vect().DeltaPhi(aux_flight));
				  vec_2trksv_absdphiauxllp0.push_back(absdphiauxllp0);
				  double absdphiauxllp1 = 0.0;//fabs(mevent->gen_lsp_p4(1).Vect().DeltaPhi(aux_flight));
				  vec_2trksv_absdphiauxllp1.push_back(absdphiauxllp1);
			  }
			  else {
				  //vec_2trksv_gendist3dllpvtx0.push_back(mag(mevent->gen_lsp_decay[3] - aux.x, mevent->gen_lsp_decay[4] - aux.y, mevent->gen_lsp_decay[5] - aux.z));
				  //vec_2trksv_gendist3dllpvtx1.push_back(mag(mevent->gen_lsp_decay[0] - aux.x, mevent->gen_lsp_decay[1] - aux.y, mevent->gen_lsp_decay[2] - aux.z));
				  TVector3 aux_flight = TVector3(aux.x - mevent->bsx_at_z(aux.z), aux.y - mevent->bsy_at_z(aux.z), aux.z - mevent->bsz);
				  double absdphiauxllp0 = 0.0;//fabs(mevent->gen_lsp_p4(1).Vect().DeltaPhi(aux_flight));
				  vec_2trksv_absdphiauxllp0.push_back(absdphiauxllp0);
				  double absdphiauxllp1 = 0.0;//fabs(mevent->gen_lsp_p4(0).Vect().DeltaPhi(aux_flight));
				  vec_2trksv_absdphiauxllp1.push_back(absdphiauxllp1);
			  }
		  }
	  }

	  for (size_t i = 0; i < aux.outsed_track_nsigmadxy.size(); ++i) {
		  if (std::count(aux.track_tkdist_val.begin(), aux.track_tkdist_val.end(), aux.outsed_track_tkdist_val[i]) > 0
			  || std::count(vec_exact_outsed_track_nsigmadxy.begin(), vec_exact_outsed_track_nsigmadxy.end(), aux.outsed_track_tkdist_val[i]) > 0)
			  continue;
		  vec_exact_outsed_track_nsigmadxy.push_back(aux.outsed_track_tkdist_val[i]);
		  
	  }
  }

  h_sum_ntrack_sv->Fill(sum_ntrack, w);
  h_sum_noutseedtrack->Fill(vec_exact_outsed_track_nsigmadxy.size(), w);
 
  if (nsv > 1) {
	  const MFVVertexAux& aux0 = auxes->at(0);
	  const MFVVertexAux& aux1 = auxes->at(1);
	  h_2D_ntrk0_ntrk1->Fill(aux0.ntracks(), aux1.ntracks());
	  
	  double min_dau_dxy = 99.0;
	  for (int i = 0; i < 2; ++i) {  //an index of GEN llps 
		  for (int j = i*2; j < i*2 + 2; ++j) {
			  double d_dxy = 0.0;//mag(mevent->gen_lsp_decay[i*3 + 0] - mevent->gen_pv[0], mevent->gen_lsp_decay[i*3 + 1] - mevent->gen_pv[1]) * sin(mevent->gen_daughters[j].Phi() - atan2(mevent->gen_lsp_decay[i * 3 + 1] - mevent->gen_pv[1], mevent->gen_lsp_decay[i * 3 + 0] - mevent->gen_pv[0]));
			  //std::cout << " d-quark #" <<  j << " dxy(cm): " << d_dxy << " pT (GeV): " << mevent->gen_daughters[j].Pt() << std::endl;
			  if (fabs(d_dxy) < min_dau_dxy)
				  min_dau_dxy = fabs(d_dxy);
		  }
		  
	  }
	  double genllpdist3d = 0.0;//mag(mevent->gen_lsp_decay[0] - mevent->gen_lsp_decay[3], mevent->gen_lsp_decay[1] - mevent->gen_lsp_decay[4], mevent->gen_lsp_decay[2] - mevent->gen_lsp_decay[5]);
	  //std::cout << " dist3d llp01 (cm) " << genllpdist3d << std::endl;

	  if (aux0.ntracks() >= 5 && aux1.ntracks() >= 5) {
			  h_signal_evt_min_dau_dxy->Fill(min_dau_dxy, w);
			  h_signal_evt_gendist3d_vtx0->Fill(gendist3dvtx0, w);
			  h_2D_signal_evt_llp0_daudxy->Fill(dau0_dxy, dau1_dxy, w);
			  if (dau0_dxy < dau1_dxy)
				  h_signal_evt_llp0_min_dau_dxy->Fill(dau0_dxy, w);
			  else
				  h_signal_evt_llp0_min_dau_dxy->Fill(dau1_dxy, w);
			  h_signal_evt_llp01_gendist3d->Fill(genllpdist3d, w);
			  h_signal_evt_vtx01_dist3d->Fill(aux1.missdistsv0[mfv::PTracksPlusJetsByNtracks], w);
			  h_signal_evt_vtx01_dist3dsig->Fill(aux1.missdistsv0sig(mfv::PTracksPlusJetsByNtracks), w);
			  h_signal_evt_vtx0_mass->Fill(aux0.mass[mfv::PTracksPlusJetsByNtracks], w);
			  h_signal_evt_vtx0_pT->Fill(aux0.pt[mfv::PTracksPlusJetsByNtracks], w);
			  h_signal_evt_vtx0_dbv->Fill(mag(aux0.x - mevent->bsx_at_z(aux0.z), aux0.y - mevent->bsy_at_z(aux0.z)), w);
			  h_signal_evt_vtx0_bs2derr->Fill(aux0.rescale_bs2derr, w);
			  for (int i = 0; i < aux0.ntracks(); ++i) {
				  h_signal_evt_vtx0_seedtrk_dxybs->Fill(aux0.track_dxy[i], w);
				  h_signal_evt_vtx0_seedtrk_nsigmadxybs->Fill(fabs(aux0.track_dxy[i] / aux0.track_dxy_err(i)), w);
				  h_signal_evt_vtx0_seedtrk_trkdist->Fill(aux0.track_tkdist_val[i], w);
				  h_signal_evt_vtx0_seedtrk_trkdistsig->Fill(aux0.track_tkdist_sig[i], w);
			  }
			  size_t imax_vtx0_outsed_mindaudxy = 9999;
			  double max_vtx0_outsed_mindaudxy = 0.0;
			  for (size_t i = 0; i < aux0.outsed_track_nsigmadxy.size(); ++i) {
				  if (std::count(aux0.track_tkdist_val.begin(), aux0.track_tkdist_val.end(), aux0.outsed_track_tkdist_val[i]) > 0)
					  continue;
				  
				  h_signal_evt_vtx0_outseedtrk_dxybs->Fill(aux0.outsed_track_dxy[i], w);
				  h_signal_evt_vtx0_outseedtrk_nsigmadxybs->Fill(fabs(aux0.outsed_track_nsigmadxy[i]), w);
				  h_signal_evt_vtx0_outseedtrk_trkdist->Fill(aux0.outsed_track_tkdist_val[i], w);
				  h_signal_evt_vtx0_outseedtrk_trkdistsig->Fill(aux0.outsed_track_tkdist_sig[i], w);
				  if ((dau0_dxy * (dau0_dxy < dau1_dxy) + dau1_dxy * (dau0_dxy > dau1_dxy)) < aux0.outsed_track_dxy[i])
					  continue;
				  
				  if (max_vtx0_outsed_mindaudxy < aux0.outsed_track_dxy[i]) {
					  max_vtx0_outsed_mindaudxy = aux0.outsed_track_dxy[i];
					  imax_vtx0_outsed_mindaudxy = i;
					  
				  }
				  
			  }
			  if (imax_vtx0_outsed_mindaudxy != 9999) {
				  h_2D_signal_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_trkdistsig->Fill(aux0.outsed_track_dxy[imax_vtx0_outsed_mindaudxy], aux0.outsed_track_tkdist_sig[imax_vtx0_outsed_mindaudxy], w);
				  h_2D_signal_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_trkdist->Fill(aux0.outsed_track_dxy[imax_vtx0_outsed_mindaudxy], aux0.outsed_track_tkdist_val[imax_vtx0_outsed_mindaudxy], w);
				  h_signal_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_nsigmadxybs->Fill(fabs(aux0.outsed_track_nsigmadxy[imax_vtx0_outsed_mindaudxy]),w);
				  h_signal_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_trkdistsig->Fill(aux0.outsed_track_tkdist_sig[imax_vtx0_outsed_mindaudxy], w);

			  }

			  h_signal_evt_n2trksv->Fill(vec_i2trksv.size(), w);

			  for (size_t ibin = 0; ibin < 10; ++ibin) {
				  double gendist3dllp0_cutoff = ibin * (0.04 / 10);
				  int count_n2trksv_cutoff = 0;
				  for (size_t i = 0; i < vec_2trksv_gendist3dllpvtx0.size(); ++i) {
					  if (vec_2trksv_gendist3dllpvtx0[i] < gendist3dllp0_cutoff) {
						  count_n2trksv_cutoff++;
						  if (ibin == 9) {
							  const MFVVertexAux& aux2trk = auxes->at(vec_i2trksv[i]);
							  double phi2trk = atan2(aux2trk.y - mevent->bsy_at_z(aux2trk.z), aux2trk.x - mevent->bsx_at_z(aux2trk.z));
							  double phi0 = atan2(aux0.y - mevent->bsy_at_z(aux2trk.z), aux0.x - mevent->bsx_at_z(aux2trk.z));
							  h_signal_evt_gendist3dresllp0_400um_2trksv_dbv->Fill(mag(aux2trk.x - mevent->bsx_at_z(aux2trk.z), aux2trk.y - mevent->bsy_at_z(aux2trk.z)), w);
							  h_signal_evt_gendist3dresllp0_400um_2trksv_absdphivtx0->Fill(fabs(reco::deltaPhi(phi0, phi2trk)), w);
							  h_signal_evt_gendist3dresllp0_400um_2trksv_absdphillp0->Fill(vec_2trksv_absdphiauxllp0[i], w);
							  h_signal_evt_gendist3dresllp0_400um_2trksv_3ddistvtx0->Fill(mag(aux0.x - aux2trk.x, aux0.y - aux2trk.y, aux0.z - aux2trk.z), w);
							  
						  }
					  }
					  if (ibin == 0)
						  h_signal_evt_gendist3dresllp0_2trksv->Fill(vec_2trksv_gendist3dllpvtx0[i], w);
					  
				  }
				  h_2D_signal_evt_gendist3dresllp0_n2trksv->Fill(gendist3dllp0_cutoff, count_n2trksv_cutoff, w);

			  }
			  
	  }
	  else if (aux0.ntracks() >= 5 && aux1.ntracks() < 5) {
			  h_potential_evt_min_dau_dxy->Fill(min_dau_dxy, w);
			  h_potential_evt_gendist3d_vtx0->Fill(gendist3dvtx0, w);
			  h_2D_potential_evt_llp0_daudxy->Fill(dau0_dxy, dau1_dxy, w);
			  if (dau0_dxy < dau1_dxy)
				  h_potential_evt_llp0_min_dau_dxy->Fill(dau0_dxy, w);
			  else
				  h_potential_evt_llp0_min_dau_dxy->Fill(dau1_dxy, w);
			  h_potential_evt_gendist3d_vtx1->Fill(gendist3dvtx1, w);
			  if (aux1.ntracks() >= 3) {
				  h_potential_evt_gendist3d_3trk_vtx1->Fill(gendist3dvtx1, w);
				  h_potential_evt_3trk_vtx1_mass->Fill(aux1.mass[mfv::PTracksPlusJetsByNtracks], w);
				  h_potential_evt_3trk_vtx1_pT->Fill(aux1.pt[mfv::PTracksPlusJetsByNtracks], w);
				  h_potential_evt_3trk_vtx1_dbv->Fill(mag(aux1.x - mevent->bsx_at_z(aux1.z), aux1.y - mevent->bsy_at_z(aux1.z)), w);
				  h_potential_evt_3trk_vtx1_bs2derr->Fill(aux1.rescale_bs2derr, w);
			  }
			  h_2D_potential_evt_llp1_daudxy->Fill(dau2_dxy, dau3_dxy, w);
			  if (dau2_dxy < dau3_dxy)
				  h_potential_evt_llp1_min_dau_dxy->Fill(dau2_dxy, w);
			  else
				  h_potential_evt_llp1_min_dau_dxy->Fill(dau3_dxy, w);
			  h_potential_evt_llp01_gendist3d->Fill(genllpdist3d, w);
			  h_potential_evt_vtx01_dist3d->Fill(aux1.missdistsv0[mfv::PTracksPlusJetsByNtracks], w);
			  h_potential_evt_vtx01_dist3dsig->Fill(aux1.missdistsv0sig(mfv::PTracksPlusJetsByNtracks), w);
			  h_potential_evt_vtx0_mass->Fill(aux0.mass[mfv::PTracksPlusJetsByNtracks], w);
			  h_potential_evt_vtx0_pT->Fill(aux0.pt[mfv::PTracksPlusJetsByNtracks], w);
			  h_potential_evt_vtx0_dbv->Fill(mag(aux0.x - mevent->bsx_at_z(aux0.z), aux0.y - mevent->bsy_at_z(aux0.z)), w);
			  h_potential_evt_vtx0_bs2derr->Fill(aux0.rescale_bs2derr, w);
			  h_potential_evt_vtx1_mass->Fill(aux1.mass[mfv::PTracksPlusJetsByNtracks], w);
			  h_potential_evt_vtx1_pT->Fill(aux1.pt[mfv::PTracksPlusJetsByNtracks], w);
			  h_potential_evt_vtx1_dbv->Fill(mag(aux1.x - mevent->bsx_at_z(aux1.z), aux1.y - mevent->bsy_at_z(aux1.z)), w);
			  h_potential_evt_vtx1_bs2derr->Fill(aux1.rescale_bs2derr, w);
			  for (int i = 0; i < aux0.ntracks(); ++i) {
				  h_potential_evt_vtx0_seedtrk_dxybs->Fill(aux0.track_dxy[i], w);
				  h_potential_evt_vtx0_seedtrk_nsigmadxybs->Fill(fabs(aux0.track_dxy[i] / aux0.track_dxy_err(i)), w);
				  h_potential_evt_vtx0_seedtrk_trkdist->Fill(aux0.track_tkdist_val[i], w);
				  h_potential_evt_vtx0_seedtrk_trkdistsig->Fill(aux0.track_tkdist_sig[i], w);
				  h_2D_potential_evt_vtx0_seedtrk_trkdist_other_trkdist->Fill(aux0.track_tkdist_val[i], aux0.track_tkdisttosv1_val[i], w);
				  h_2D_potential_evt_vtx0_seedtrk_trkdistsig_other_trkdistsig->Fill(aux0.track_tkdist_sig[i], aux0.track_tkdisttosv1_sig[i], w);

			  }
			  for (int i = 0; i < aux1.ntracks(); ++i) {
				  h_potential_evt_vtx1_seedtrk_dxybs->Fill(aux1.track_dxy[i], w);
				  h_potential_evt_vtx1_seedtrk_nsigmadxybs->Fill(fabs(aux1.track_dxy[i] / aux1.track_dxy_err(i)), w);
				  h_potential_evt_vtx1_seedtrk_trkdist->Fill(aux1.track_tkdist_val[i], w);
				  h_potential_evt_vtx1_seedtrk_trkdistsig->Fill(aux1.track_tkdist_sig[i], w);
                  
				  if (aux1.ntracks() >= 3) {
					  h_potential_evt_3trk_vtx1_seedtrk_dxybs->Fill(aux1.track_dxy[i], w);
					  h_potential_evt_3trk_vtx1_seedtrk_nsigmadxybs->Fill(fabs(aux1.track_dxy[i] / aux1.track_dxy_err(i)), w);
					  h_potential_evt_3trk_vtx1_seedtrk_trkdist->Fill(aux1.track_tkdist_val[i], w);
					  h_potential_evt_3trk_vtx1_seedtrk_trkdistsig->Fill(aux1.track_tkdist_sig[i], w);
				  }

			  }
			  size_t imax_vtx0_outsed_mindaudxy = 9999;
			  double max_vtx0_outsed_mindaudxy = 0.0;
			  for (size_t i = 0; i < aux0.outsed_track_nsigmadxy.size(); ++i) {
				  if (std::count(aux0.track_tkdist_val.begin(), aux0.track_tkdist_val.end(), aux0.outsed_track_tkdist_val[i]) > 0)
					  continue;
				  h_potential_evt_vtx0_outseedtrk_dxybs->Fill(aux0.outsed_track_dxy[i], w);
				  h_potential_evt_vtx0_outseedtrk_nsigmadxybs->Fill(fabs(aux0.outsed_track_nsigmadxy[i]), w);
				  h_potential_evt_vtx0_outseedtrk_trkdist->Fill(aux0.outsed_track_tkdist_val[i], w);
				  h_potential_evt_vtx0_outseedtrk_trkdistsig->Fill(aux0.outsed_track_tkdist_sig[i], w);

				  
				  if ((dau0_dxy * (dau0_dxy < dau1_dxy) + dau1_dxy * (dau0_dxy > dau1_dxy)) < aux0.outsed_track_dxy[i])
					  continue;
				  if (max_vtx0_outsed_mindaudxy < aux0.outsed_track_dxy[i]) {
					  max_vtx0_outsed_mindaudxy = aux0.outsed_track_dxy[i];
					  imax_vtx0_outsed_mindaudxy = i;
				  }

			  }

			  if (imax_vtx0_outsed_mindaudxy != 9999) {
				  h_2D_potential_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_trkdistsig->Fill(aux0.outsed_track_dxy[imax_vtx0_outsed_mindaudxy], aux0.outsed_track_tkdist_sig[imax_vtx0_outsed_mindaudxy], w);
				  h_2D_potential_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_trkdist->Fill(aux0.outsed_track_dxy[imax_vtx0_outsed_mindaudxy], aux0.outsed_track_tkdist_val[imax_vtx0_outsed_mindaudxy], w);
				  h_potential_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_nsigmadxybs->Fill(fabs(aux0.outsed_track_nsigmadxy[imax_vtx0_outsed_mindaudxy]), w);
				  h_potential_evt_vtx0_max_outseedtrk_dxy_by_min_daudxy_trkdistsig->Fill(aux0.outsed_track_tkdist_sig[imax_vtx0_outsed_mindaudxy], w);

			  }
			  size_t imax_vtx1_outsed_mindaudxy = 9999;
			  double max_vtx1_outsed_mindaudxy = 0.0;
			  for (size_t i = 0; i < aux1.outsed_track_tkdist_val.size(); ++i) {
				  if (std::count(aux1.track_tkdist_val.begin(), aux1.track_tkdist_val.end(), aux1.outsed_track_tkdist_val[i]) > 0)
					  continue;
				  h_potential_evt_vtx1_outseedtrk_trkdist->Fill(aux1.outsed_track_tkdist_val[i], w);
				  h_potential_evt_vtx1_outseedtrk_trkdistsig->Fill(aux1.outsed_track_tkdist_sig[i], w);

				  if ((dau2_dxy * (dau2_dxy < dau3_dxy) + dau3_dxy * (dau2_dxy > dau3_dxy)) < aux0.outsed_track_dxy[i])
					  continue;
				  if (max_vtx1_outsed_mindaudxy < aux0.outsed_track_dxy[i]) {
					  max_vtx1_outsed_mindaudxy = aux0.outsed_track_dxy[i];
					  imax_vtx1_outsed_mindaudxy = i;
				  }

			  }
			  if (imax_vtx1_outsed_mindaudxy != 9999) {
				  h_2D_potential_evt_vtx1_max_outseedtrk_dxy_by_min_daudxy_trkdistsig->Fill(aux0.outsed_track_dxy[imax_vtx1_outsed_mindaudxy], aux1.outsed_track_tkdist_sig[imax_vtx1_outsed_mindaudxy], w);
				  h_2D_potential_evt_vtx1_max_outseedtrk_dxy_by_min_daudxy_trkdist->Fill(aux0.outsed_track_dxy[imax_vtx1_outsed_mindaudxy], aux1.outsed_track_tkdist_val[imax_vtx1_outsed_mindaudxy], w);
				  h_potential_evt_vtx1_max_outseedtrk_dxy_by_min_daudxy_nsigmadxybs->Fill(fabs(aux0.outsed_track_nsigmadxy[imax_vtx1_outsed_mindaudxy]), w);
				  h_potential_evt_vtx1_max_outseedtrk_dxy_by_min_daudxy_trkdistsig->Fill(aux1.outsed_track_tkdist_sig[imax_vtx1_outsed_mindaudxy], w);

				  if (aux1.ntracks() >= 3) {
					  h_2D_potential_evt_3trk_vtx1_max_outseedtrk_dxy_by_min_daudxy_trkdistsig->Fill(aux0.outsed_track_dxy[imax_vtx1_outsed_mindaudxy], aux1.outsed_track_tkdist_sig[imax_vtx1_outsed_mindaudxy], w);
					  h_2D_potential_evt_3trk_vtx1_max_outseedtrk_dxy_by_min_daudxy_trkdist->Fill(aux0.outsed_track_dxy[imax_vtx1_outsed_mindaudxy], aux1.outsed_track_tkdist_val[imax_vtx1_outsed_mindaudxy], w);
					  h_potential_evt_3trk_vtx1_max_outseedtrk_dxy_by_min_daudxy_nsigmadxybs->Fill(fabs(aux0.outsed_track_nsigmadxy[imax_vtx1_outsed_mindaudxy]), w);
					  h_potential_evt_3trk_vtx1_max_outseedtrk_dxy_by_min_daudxy_trkdistsig->Fill(aux1.outsed_track_tkdist_sig[imax_vtx1_outsed_mindaudxy], w);

				  }
			  }

			  h_potential_evt_n2trksv->Fill(vec_i2trksv.size(), w);

			  for (size_t ibin = 0; ibin < 10; ++ibin) {
				  double gendist3dllp0_cutoff = ibin * (0.04 / 10);
				  int count_n2trksv_cutoff0 = 0;
				  double gendist3dllp1_cutoff = ibin * (0.04 / 10);
				  int count_n2trksv_cutoff1 = 0;
				  for (size_t i = 0; i < vec_2trksv_gendist3dllpvtx0.size(); ++i) {
					  if (vec_2trksv_gendist3dllpvtx0[i] < gendist3dllp0_cutoff) {
						  count_n2trksv_cutoff0++;
						  if (ibin == 9) {
							  const MFVVertexAux& aux2trk = auxes->at(vec_i2trksv[i]);
							  double phi2trk = atan2(aux2trk.y - mevent->bsy_at_z(aux2trk.z), aux2trk.x - mevent->bsx_at_z(aux2trk.z));
							  double phi0 = atan2(aux0.y - mevent->bsy_at_z(aux2trk.z), aux0.x - mevent->bsx_at_z(aux2trk.z));
							  h_potential_evt_gendist3dresllp0_400um_2trksv_dbv->Fill(mag(aux2trk.x - mevent->bsx_at_z(aux2trk.z), aux2trk.y - mevent->bsy_at_z(aux2trk.z)), w);
							  h_potential_evt_gendist3dresllp0_400um_2trksv_absdphivtx0->Fill(fabs(reco::deltaPhi(phi0, phi2trk)), w);
							  h_potential_evt_gendist3dresllp0_400um_2trksv_absdphillp0->Fill(vec_2trksv_absdphiauxllp0[i], w);
							  h_potential_evt_gendist3dresllp0_400um_2trksv_3ddistvtx0->Fill(mag(aux0.x - aux2trk.x, aux0.y - aux2trk.y, aux0.z - aux2trk.z), w);

						  }
					  }
					  if (ibin == 0)
						  h_potential_evt_gendist3dresllp0_2trksv->Fill(vec_2trksv_gendist3dllpvtx0[i], w);
				  }
				  h_2D_potential_evt_gendist3dresllp0_n2trksv->Fill(gendist3dllp0_cutoff, count_n2trksv_cutoff0, w);

				  for (size_t i = 0; i < vec_2trksv_gendist3dllpvtx1.size(); ++i) {
					  if (vec_2trksv_gendist3dllpvtx1[i] < gendist3dllp1_cutoff) {
						  count_n2trksv_cutoff1++;
						  if (ibin == 9) {
							  const MFVVertexAux& aux2trk = auxes->at(vec_i2trksv[i]);
							  double phi2trk = atan2(aux2trk.y - mevent->bsy_at_z(aux2trk.z), aux2trk.x - mevent->bsx_at_z(aux2trk.z));
							  double phi1 = atan2(aux1.y - mevent->bsy_at_z(aux2trk.z), aux1.x - mevent->bsx_at_z(aux2trk.z));
							  h_potential_evt_gendist3dresllp1_400um_2trksv_dbv->Fill(mag(aux2trk.x - mevent->bsx_at_z(aux2trk.z), aux2trk.y - mevent->bsy_at_z(aux2trk.z)), w);
							  h_potential_evt_gendist3dresllp1_400um_2trksv_absdphivtx1->Fill(fabs(reco::deltaPhi(phi1, phi2trk)), w);
							  h_potential_evt_gendist3dresllp1_400um_2trksv_absdphillp1->Fill(vec_2trksv_absdphiauxllp1[i], w);
							  h_potential_evt_gendist3dresllp1_400um_2trksv_3ddistvtx1->Fill(mag(aux1.x - aux2trk.x, aux1.y - aux2trk.y, aux1.z - aux2trk.z), w);
							  if (aux1.ntracks() >= 3) {
								  h_potential_evt_gendist3dres3trkllp1_400um_2trksv_dbv->Fill(mag(aux2trk.x - mevent->bsx_at_z(aux2trk.z), aux2trk.y - mevent->bsy_at_z(aux2trk.z)), w);
								  h_potential_evt_gendist3dres3trkllp1_400um_2trksv_absdphivtx1->Fill(fabs(reco::deltaPhi(phi1, phi2trk)), w);
								  h_potential_evt_gendist3dres3trkllp1_400um_2trksv_absdphillp1->Fill(vec_2trksv_absdphiauxllp1[i], w);
								  h_potential_evt_gendist3dres3trkllp1_400um_2trksv_3ddistvtx1->Fill(mag(aux1.x - aux2trk.x, aux1.y - aux2trk.y, aux1.z - aux2trk.z), w);

							  }
						  }
					  }
					  if (ibin == 0)
						  h_potential_evt_gendist3dresllp1_2trksv->Fill(vec_2trksv_gendist3dllpvtx1[i], w);
				  }
				  h_2D_potential_evt_gendist3dresllp1_n2trksv->Fill(gendist3dllp1_cutoff, count_n2trksv_cutoff1, w);
				  if (aux1.ntracks() >= 3)
					  h_2D_potential_evt_gendist3dres3trkllp1_n2trksv->Fill(gendist3dllp1_cutoff, count_n2trksv_cutoff1, w);
			  }
			  
			  
	  }
	  
  }
  */

  std::vector<std::vector<int> > sv_track_which_jet;
  std::vector<std::vector<int> > sv_track_which_track;
  for (int isv = 0; isv < nsv; ++isv) { 
	  const MFVVertexAux& aux = auxes->at(isv);
	  const int ntracks = aux.ntracks();
	  std::vector<int> track_which_jet;
          std::vector<int> track_which_track;
	  for (int i = 0; i < ntracks; ++i) { 
		  //double match_threshold = 1.3;
	      int jet_index = 255;
	      for (unsigned j = 0; j < mevent->jet_track_which_jet.size(); ++j) { 
			  //double a = fabs(aux.track_pt(i) - fabs(mevent->jet_track_qpt[j])) + 1;
			  //double b = fabs(aux.track_eta[i] - mevent->jet_track_eta[j]) + 1;
			  //double c = fabs(aux.track_phi[i] - mevent->jet_track_phi[j]) + 1;
			  if (fabs(aux.track_pt(i) - fabs(mevent->jet_track_qpt[j])) < 0.0001 
				  && fabs(aux.track_eta[i] - mevent->jet_track_eta[j]) < 0.0001 
				  && fabs(aux.track_phi[i] - mevent->jet_track_phi[j]) < 0.0001) {
				  jet_index = mevent->jet_track_which_jet[j];
			  } 
	      }
	      if (jet_index != 255) { 
		  track_which_jet.push_back((int)jet_index);
                  track_which_track.push_back(i);

	      } 
	  }
	  sv_track_which_jet.push_back(track_which_jet);
          sv_track_which_track.push_back(track_which_track);
  }

  /*
  double llp0_flight_mom_phi = 0.0;//mevent->gen_lsp_p4(0).Vect().DeltaPhi(mevent->gen_lsp_flight(0));
  //std::cout << "llp0 : energy (GeV) = " << mevent->gen_lsps[0].Energy() << " betagamma = " << lspbetagamma0 << " r3d (cm) " << r3d0 << " dphi(GEN mom, GEN flight) " << llp0_flight_mom_phi << std::endl;
  if (isv_llp0 != -99) {
	  const MFVVertexAux& aux = auxes->at(isv_llp0);
          TVector3 vtx_flight = TVector3(aux.x - mevent->bsx_at_z(aux.z), aux.y - mevent->bsy_at_z(aux.z), aux.z - mevent->bsz);
          double vtx_flight_mom_phi = aux.p4(mfv::PTracksOnly).Vect().DeltaPhi(vtx_flight); 
          //std::cout << "     :  found closest sv! " << "idx = " << isv_llp0 << " ntrack = " << gensv0_ntrack << " dist3d (cm) = " << min_dist3d_genlsp0sv << " dphi(vtx mom, vtx flight) " << vtx_flight_mom_phi << std::endl;
          for (size_t i = 0; i < sv_track_which_jet[isv_llp0].size(); ++i) {
                  int ijet = sv_track_which_jet[isv_llp0][i];
                  int itrack = sv_track_which_track[isv_llp0][i];
                  //std::cout << "     :  track's dxy : " <<  aux.track_dxy[itrack]; 
		  //std::cout << "     :  jet's idx : "  << ijet << " jet's pT : " << mevent->jet_pt[ijet] << " jet's eta : " << mevent->jet_eta[ijet] << " jet's phi : " << mevent->jet_phi[ijet] << std::endl;
		  //std::cout << "     :  loose-btagged jet? : " << mevent->is_btagged(ijet, 0) << std::endl;
	  }
  }
  double llp1_flight_mom_phi = 0.0;//mevent->gen_lsp_p4(1).Vect().DeltaPhi(mevent->gen_lsp_flight(1));
  //std::cout << "llp1 : energy (GeV) = " << mevent->gen_lsps[1].Energy() << " betagamma = " << lspbetagamma1 << " r3d (cm) " << r3d1 << " dphi(GEN mom, GEN flight) " << llp1_flight_mom_phi << std::endl;
  if (isv_llp1 != -99) {
          const MFVVertexAux& aux = auxes->at(isv_llp1); 
          TVector3 vtx_flight = TVector3(aux.x - mevent->bsx_at_z(aux.z), aux.y - mevent->bsy_at_z(aux.z), aux.z - mevent->bsz);
          double vtx_flight_mom_phi = aux.p4(mfv::PTracksOnly).Vect().DeltaPhi(vtx_flight);
          //std::cout << "     :  found closest sv! " << "idx = " << isv_llp1 << " ntrack = " << gensv1_ntrack << " dist3d (cm) = " << min_dist3d_genlsp1sv << " dphi(vtx mom, vtx flight) " << vtx_flight_mom_phi << std::endl;
          for (size_t i = 0; i < sv_track_which_jet[isv_llp1].size(); ++i) {
                  int ijet = sv_track_which_jet[isv_llp1][i];
                  int itrack = sv_track_which_track[isv_llp1][i];
           //std::cout << "     :  track's dxy : " <<  aux.track_dxy[itrack]; 
		  //std::cout << "     :  jet's idx : " << ijet << " jet's pT : " << mevent->jet_pt[ijet] << " jet's eta : " << mevent->jet_eta[ijet] << " jet's phi : " << mevent->jet_phi[ijet] << std::endl;
		  //std::cout << "     :  loose-btagged jet? : " << mevent->is_btagged(ijet, 0) << std::endl;
	  }
  }
  //std::cout << "*** END GEN-level information ***" << std::endl;
  */
	
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
