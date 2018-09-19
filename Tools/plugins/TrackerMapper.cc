#include "TH2D.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "JMTucker/Tools/interface/TrackerSpaceExtent.h"
#include "JMTucker/Tools/interface/Utilities.h"

class TrackerMapper : public edm::EDAnalyzer {
 public:
  explicit TrackerMapper(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);
 
 private:
  const edm::EDGetTokenT<reco::TrackCollection> track_token;
  const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
  const edm::EDGetTokenT<reco::VertexCollection> primary_vertex_token;
  const edm::EDGetTokenT<std::vector<PileupSummaryInfo> > pileup_info_token;

  const std::vector<double> pileup_weights;
  double pileup_weight(int mc_npu) const;

  const int use_duplicateMerge;
  const bool old_stlayers_cut;

  TH1D* h_npu;
  TH1D* h_w;

  TH1D* h_bsx;
  TH1D* h_bsy;
  TH1D* h_bsz;

  TH1D* h_npv;
  TH1D* h_pvx[2];
  TH1D* h_pvy[2];
  TH1D* h_pvz[2];
  TH1D* h_pvrho[2];
  TH1D* h_pvntracks[2];
  TH1D* h_pvsumpt2[2];

  TH1D* h_ntracks[3];
  TH1D* h_ntracks_quality[3][reco::TrackBase::qualitySize];
  TH1D* h_tracks_algo[3];
  TH1D* h_tracks_original_algo[3];
  TH1D* h_tracks_pt[3];
  TH1D* h_tracks_eta[3];
  TH1D* h_tracks_phi[3];
  TH1D* h_tracks_vx[3];
  TH1D* h_tracks_vy[3];
  TH1D* h_tracks_vz[3];
  TH1D* h_tracks_vphi[3];
  TH1D* h_tracks_dxy[3];
  TH1D* h_tracks_absdxy[3];
  TH1D* h_tracks_dz[3];
  TH1D* h_tracks_dzpv[3];
  TH1D* h_tracks_dxyerr[3];
  TH1D* h_tracks_dzerr[3];
  TH1D* h_tracks_nhits[3];
  TH1D* h_tracks_npxhits[3];
  TH1D* h_tracks_nsthits[3];

  TH1D* h_tracks_qp_dxy[3];
  TH1D* h_tracks_qm_dxy[3];
  TH1D* h_tracks_dxy_zslices[3][6];

  TH1D* h_tracks_min_r[3];
  TH1D* h_tracks_npxlayers[3];
  TH1D* h_tracks_nstlayers[3];
  TH1D* h_tracks_nstlayers_etalt2[3];
  TH1D* h_tracks_nstlayers_etagt2[3];
  TH1D* h_tracks_nsigmadxy[3];
  TH1D* h_tracks_nsigmadxy_acc[3];
  TH1D* h_tracks_nsigmadxy_deltaacc[3];

  TH2D* h_tracks_nstlayers_v_eta[3];
  TH2D* h_tracks_dxy_v_eta[3];
  TH2D* h_tracks_dxy_v_nstlayers[3];
  TH2D* h_tracks_dxyerr_v_eta[3];
  TH2D* h_tracks_dxyerr_v_nstlayers[3];
  TH2D* h_tracks_dxyerr_v_dxy[3];
  TH2D* h_tracks_nsigmadxy_v_eta[3];
  TH2D* h_tracks_nsigmadxy_v_nstlayers[3];
  TH2D* h_tracks_nsigmadxy_v_dxy[3];
  TH2D* h_tracks_nsigmadxy_v_dxyerr[3];
  TH2D* h_tracks_dxyerr_v_dxy_ptslices[3][6];

  TH1D* h_nm1_tracks_pt[2];
  TH1D* h_nm1_tracks_min_r[2];
  TH1D* h_nm1_tracks_npxlayers[2];
  TH1D* h_nm1_tracks_nstlayers[2];
  TH2D* h_nm1_tracks_nstlayers_v_eta[2];
  TH1D* h_nm1_tracks_nstlayers_etalt2[2];
  TH1D* h_nm1_tracks_nstlayers_etagt2[2];
  TH1D* h_nm1_tracks_nsigmadxy[2];
  TH2D* h_nm1_tracks_dxy_v_pt[2];
  TH2D* h_nm1_tracks_dxy_v_nstlayers[2];
  TH2D* h_nm1_tracks_dxy_v_npxlayers[2];
  TH2D* h_nm1_tracks_dxy_v_min_r[2];
  TH2D* h_nm1_tracks_dxyerr_v_pt[2];
  TH2D* h_nm1_tracks_dxyerr_v_npxlayers[2];
  TH2D* h_nm1_tracks_dxyerr_v_nstlayers[2];
  TH2D* h_nm1_tracks_dxyerr_v_min_r[2];

  TH2D* h_dxyerr_v_ptcut[2];
  TH2D* h_dxyerr_v_npxlayerscut[2];
  TH2D* h_dxyerr_v_nstlayerscut[2];
  TH1D* h_tracks_ptcut[2];
  TH1D* h_tracks_npxlayerscut[2];
  TH1D* h_tracks_nstlayerscut[2];

  TH2D* h_dxyerr_v_npxlayerscut_etaslices[2][4];
  TH2D* h_dxyerr_v_nstlayerscut_etaslices[2][4];
};

TrackerMapper::TrackerMapper(const edm::ParameterSet& cfg)
  : track_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("track_src"))),
    beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot_src"))),
    primary_vertex_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("primary_vertex_src"))),
    pileup_info_token(consumes<std::vector<PileupSummaryInfo> >(cfg.getParameter<edm::InputTag>("pileup_info_src"))),
    pileup_weights(cfg.getParameter<std::vector<double> >("pileup_weights")),
    use_duplicateMerge(cfg.getParameter<int>("use_duplicateMerge")),
    old_stlayers_cut(cfg.getParameter<bool>("old_stlayers_cut"))
{
  edm::Service<TFileService> fs;
  TH1::SetDefaultSumw2();

  h_npu = fs->make<TH1D>("h_npu", ";number of pileup interactions;events", 100, 0, 100);
  h_w = fs->make<TH1D>("h_w", ";event weight;events", 20, 0, 10);

  h_bsx = fs->make<TH1D>("h_bsx", ";beamspot x (cm);events/100 #mum", 200, -1, 1);
  h_bsy = fs->make<TH1D>("h_bsy", ";beamspot y (cm);events/100 #mum", 200, -1, 1);
  h_bsz = fs->make<TH1D>("h_bsz", ";beamspot z (cm);events/100 #mum", 200, -1, 1);

  h_npv = fs->make<TH1D>("h_npv", ";number of primary vertices;events", 100, 0, 100);
  for (int i = 0; i < 2; ++i) {
    const char* ex = i == 0 ? "the" : "all";
    h_pvx[i] = fs->make<TH1D>(TString::Format("h_pvx_%i", i), TString::Format(";%s pv x (cm);events/10 #mum", ex), 2000, -1, 1);
    h_pvy[i] = fs->make<TH1D>(TString::Format("h_pvy_%i", i), TString::Format(";%s pv y (cm);events/10 #mum", ex), 2000, -1, 1);
    h_pvz[i] = fs->make<TH1D>(TString::Format("h_pvz_%i", i), TString::Format(";%s pv z (cm);events/1 mm", ex), 4000, -20, 20);
    h_pvrho[i] = fs->make<TH1D>(TString::Format("h_pvrho_%i", i), TString::Format(";%s pv #rho x (cm);events/10 #mum", ex), 1000, 0, 1);
    h_pvntracks[i] = fs->make<TH1D>(TString::Format("h_pvntracks_%i", i), TString::Format(";%s pv # tracks;events/1", ex), 200, 0, 200);
    h_pvsumpt2[i] = fs->make<TH1D>(TString::Format("h_pvsumpt2_%i", i), TString::Format(";%s pv #Sigma p_{T}^{2} (GeV^{2});events/200 GeV^{2}", ex), 500, 0, 100000);
  }

  const char* ex[3] = {"all", "sel", "seed"};
  for (int i = 0; i < 3; ++i) {
    h_ntracks[i] = fs->make<TH1D>(TString::Format("h_%s_ntracks", ex[i]), TString::Format(";number of %s tracks;events", ex[i]), 2000, 0, 2000);
    for (int j = 0; j < reco::TrackBase::qualitySize; ++j)
      h_ntracks_quality[i][j] = fs->make<TH1D>(TString::Format("h_%s_ntracks_quality%i", ex[i], j), TString::Format(";number of %s tracks quality %s;events", ex[i], reco::TrackBase::qualityNames[j].c_str()), 2000, 0, 2000);
    h_tracks_algo[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_algo", ex[i]), TString::Format(";%s tracks algo;events", ex[i]), 50, 0, 50);
    h_tracks_original_algo[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_original_algo", ex[i]), TString::Format(";%s tracks original algo;events", ex[i]), 50, 0, 50);
    h_tracks_pt[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_pt", ex[i]), TString::Format("%s tracks;tracks pt;arb. units", ex[i]), 200, 0, 20);
    h_tracks_phi[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_phi", ex[i]), TString::Format("%s tracks;tracks phi;arb. units", ex[i]), 50, -3.15, 3.15);
    h_tracks_eta[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_eta", ex[i]), TString::Format("%s tracks;tracks eta;arb. units", ex[i]), 50, -4, 4);
    h_tracks_vx[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_vx", ex[i]), TString::Format("%s tracks;tracks vx - beamspot x;arb. units", ex[i]), 400, -0.2, 0.2);
    h_tracks_vy[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_vy", ex[i]), TString::Format("%s tracks;tracks vy - beamspot y;arb. units", ex[i]), 400, -0.2, 0.2);
    h_tracks_vz[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_vz", ex[i]), TString::Format("%s tracks;tracks vz - beamspot z;arb. units", ex[i]), 400, -20, 20);
    h_tracks_vphi[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_vphi", ex[i]), TString::Format("%s tracks;tracks vphi w.r.t. beamspot;arb. units", ex[i]), 50, -3.15, 3.15);
    h_tracks_dxy[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_dxy", ex[i]), TString::Format("%s tracks;tracks dxy to beamspot;arb. units", ex[i]), 400, -0.2, 0.2);
    h_tracks_absdxy[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_absdxy", ex[i]), TString::Format("%s tracks;tracks |dxy| to beamspot;arb. units", ex[i]), 200, 0, 0.2);
    h_tracks_dz[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_dz", ex[i]), TString::Format("%s tracks;tracks dz to beamspot;arb. units", ex[i]), 400, -20, 20);
    h_tracks_dzpv[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_dzpv", ex[i]), TString::Format("%s tracks;tracks dz to PV;arb. units", ex[i]), 400, -20, 20);
    h_tracks_dxyerr[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_dxyerr", ex[i]), TString::Format("%s tracks;tracks dxyerr;arb. units", ex[i]), 200, 0, 0.2);
    h_tracks_dzerr[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_dzerr", ex[i]), TString::Format("%s tracks;tracks dzerr;arb. units", ex[i]), 200, 0, 2);
    h_tracks_nhits[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_nhits", ex[i]), TString::Format("%s tracks;tracks nhits;arb. units", ex[i]), 40, 0, 40);
    h_tracks_npxhits[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_npxhits", ex[i]), TString::Format("%s tracks;tracks npxhits;arb. units", ex[i]), 40, 0, 40);
    h_tracks_nsthits[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_nsthits", ex[i]), TString::Format("%s tracks;tracks nsthits;arb. units", ex[i]), 40, 0, 40);

    h_tracks_qp_dxy[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_qp_dxy", ex[i]), TString::Format("%s tracks;q=+1 tracks dxy to beamspot;arb. units", ex[i]), 400, -0.2, 0.2);
    h_tracks_qm_dxy[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_qm_dxy", ex[i]), TString::Format("%s tracks;q=-1 tracks dxy to beamspot;arb. units", ex[i]), 400, -0.2, 0.2);
    for (int j = 0; j < 6; ++j) {
      h_tracks_dxy_zslices[i][j] = fs->make<TH1D>(TString::Format("h_%s_tracks_dxy_z%d", ex[i], j), TString::Format("%s tracks z%d;tracks dxy to beamspot;arb. units", ex[i], j), 400, -0.2, 0.2);
    }

    h_tracks_min_r[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_min_r", ex[i]), TString::Format("%s tracks;tracks min_r;arb. units", ex[i]), 20, 0, 20);
    h_tracks_npxlayers[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_npxlayers", ex[i]), TString::Format("%s tracks;tracks npxlayers;arb. units", ex[i]), 20, 0, 20);
    h_tracks_nstlayers[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_nstlayers", ex[i]), TString::Format("%s tracks;tracks nstlayers;arb. units", ex[i]), 20, 0, 20);
    h_tracks_nstlayers_etalt2[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_nstlayers_etalt2", ex[i]), TString::Format("%s tracks;|#eta| < 2 tracks nstlayers;arb. units", ex[i]), 20, 0, 20);
    h_tracks_nstlayers_etagt2[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_nstlayers_etagt2", ex[i]), TString::Format("%s tracks;|#eta| #geq 2 tracks nstlayers;arb. units", ex[i]), 20, 0, 20);
    h_tracks_nsigmadxy[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_nsigmadxy", ex[i]), TString::Format("%s tracks;tracks nsigmadxy;arb. units", ex[i]), 400, 0, 40);
    h_tracks_nsigmadxy_acc[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_nsigmadxy_acc", ex[i]), TString::Format("%s tracks;tracks nsigmadxy_acc;arb. units", ex[i]), 400, 0, 40);
    h_tracks_nsigmadxy_deltaacc[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_nsigmadxy_deltaacc", ex[i]), TString::Format("%s tracks;tracks nsigmadxy - nsigmadxy_acc;arb. units", ex[i]), 400, -10, 10);

    h_tracks_nstlayers_v_eta[i] = fs->make<TH2D>(TString::Format("h_%s_tracks_nstlayers_v_eta", ex[i]), TString::Format("%s tracks;tracks eta;tracks nstlayers", ex[i]), 80, -4, 4, 20, 0, 20);
    h_tracks_dxy_v_eta[i] = fs->make<TH2D>(TString::Format("h_%s_tracks_dxy_v_eta", ex[i]), TString::Format("%s tracks;tracks eta;tracks dxy to beamspot", ex[i]), 80, -4, 4, 400, -0.2, 0.2);
    h_tracks_dxy_v_nstlayers[i] = fs->make<TH2D>(TString::Format("h_%s_tracks_dxy_v_nstlayers", ex[i]), TString::Format("%s tracks;tracks nstlayers;tracks dxy to beamspot", ex[i]), 20, 0, 20, 400, -0.2, 0.2);
    h_tracks_dxyerr_v_eta[i] = fs->make<TH2D>(TString::Format("h_%s_tracks_dxyerr_v_eta", ex[i]), TString::Format("%s tracks;tracks eta;tracks dxyerr", ex[i]), 80, -4, 4, 200, 0, 0.2);
    h_tracks_dxyerr_v_nstlayers[i] = fs->make<TH2D>(TString::Format("h_%s_tracks_dxyerr_v_nstlayers", ex[i]), TString::Format("%s tracks;tracks nstlayers;tracks dxyerr", ex[i]), 20, 0, 20, 200, 0, 0.2);
    h_tracks_dxyerr_v_dxy[i] = fs->make<TH2D>(TString::Format("h_%s_tracks_dxyerr_v_dxy", ex[i]), TString::Format("%s tracks;tracks dxy to beamspot;tracks dxyerr", ex[i]), 400, -0.2, 0.2, 200, 0, 0.2);
    h_tracks_nsigmadxy_v_eta[i] = fs->make<TH2D>(TString::Format("h_%s_tracks_nsigmadxy_v_eta", ex[i]), TString::Format("%s tracks;tracks eta;tracks nsigmadxy", ex[i]), 80, -4, 4, 200, 0, 20);
    h_tracks_nsigmadxy_v_nstlayers[i] = fs->make<TH2D>(TString::Format("h_%s_tracks_nsigmadxy_v_nstlayers", ex[i]), TString::Format("%s tracks;tracks nstlayers;tracks nsigmadxy", ex[i]), 20, 0, 20, 200, 0, 20);
    h_tracks_nsigmadxy_v_dxy[i] = fs->make<TH2D>(TString::Format("h_%s_tracks_nsigmadxy_v_dxy", ex[i]), TString::Format("%s tracks;tracks dxy to beamspot;tracks nsigmadxy", ex[i]), 400, -0.2, 0.2, 200, 0, 20);
    h_tracks_nsigmadxy_v_dxyerr[i] = fs->make<TH2D>(TString::Format("h_%s_tracks_nsigmadxy_v_dxyerr", ex[i]), TString::Format("%s tracks;tracks dxyerr;tracks nsigmadxy", ex[i]), 200, 0, 0.2, 200, 0, 20);
    for (int j = 0; j < 6; ++j) {
      h_tracks_dxyerr_v_dxy_ptslices[i][j] = fs->make<TH2D>(TString::Format("h_%s_tracks_dxyerr_v_dxy_pt%d", ex[i], j), TString::Format("%s tracks pt%d;tracks dxy to beamspot;tracks dxyerr", ex[i], j), 400, -0.2, 0.2, 200, 0, 0.2);
    }
  }

  const char* ex3[2] = {"sel", "seed"};
  for (int i = 0; i < 2; ++i) {
    h_nm1_tracks_pt[i] = fs->make<TH1D>(TString::Format("h_nm1_%s_tracks_pt", ex3[i]), TString::Format("nm1 %s tracks;tracks pt;arb. units", ex3[i]), 200, 0, 20);
    h_nm1_tracks_min_r[i] = fs->make<TH1D>(TString::Format("h_nm1_%s_tracks_min_r", ex3[i]), TString::Format("nm1 %s tracks;tracks min_r;arb. units", ex3[i]), 20, 0, 20);
    h_nm1_tracks_npxlayers[i] = fs->make<TH1D>(TString::Format("h_nm1_%s_tracks_npxlayers", ex3[i]), TString::Format("nm1 %s tracks;tracks npxlayers;arb. units", ex3[i]), 20, 0, 20);
    h_nm1_tracks_nstlayers[i] = fs->make<TH1D>(TString::Format("h_nm1_%s_tracks_nstlayers", ex3[i]), TString::Format("nm1 %s tracks;tracks nstlayers;arb. units", ex3[i]), 20, 0, 20);
    h_nm1_tracks_nstlayers_v_eta[i] = fs->make<TH2D>(TString::Format("h_nm1_%s_tracks_nstlayers_v_eta", ex3[i]), TString::Format("nm1 %s tracks;tracks #eta;tracks number of strip layers", ex3[i]), 80, -4, 4, 20, 0, 20);
    h_nm1_tracks_nstlayers_etalt2[i] = fs->make<TH1D>(TString::Format("h_nm1_%s_tracks_nstlayers_etalt2", ex3[i]), TString::Format("nm1 %s tracks;|#eta| < 2 tracks nstlayers;arb. units", ex3[i]), 20, 0, 20);
    h_nm1_tracks_nstlayers_etagt2[i] = fs->make<TH1D>(TString::Format("h_nm1_%s_tracks_nstlayers_etagt2", ex3[i]), TString::Format("nm1 %s tracks;|#eta| #geq 2 tracks nstlayers;arb. units", ex3[i]), 20, 0, 20);
    h_nm1_tracks_nsigmadxy[i] = fs->make<TH1D>(TString::Format("h_nm1_%s_tracks_nsigmadxy", ex3[i]), TString::Format("nm1 %s tracks;tracks nsigmadxy;arb. units", ex3[i]), 200, 0, 20);
    h_nm1_tracks_dxy_v_pt[i] = fs->make<TH2D>(TString::Format("h_nm1_%s_tracks_dxy_v_pt", ex3[i]), TString::Format("nm1 %s tracks;tracks pt;tracks dxyerr", ex3[i]), 200, 0, 20, 400, -0.2, 0.2);
    h_nm1_tracks_dxy_v_nstlayers[i] = fs->make<TH2D>(TString::Format("h_nm1_%s_tracks_dxy_v_nstlayers", ex3[i]), TString::Format("nm1 %s tracks;tracks nstlayers;tracks dxyerr", ex3[i]), 20, 0, 20, 400, -0.2, 0.2);
    h_nm1_tracks_dxy_v_npxlayers[i] = fs->make<TH2D>(TString::Format("h_nm1_%s_tracks_dxy_v_npxlayers", ex3[i]), TString::Format("nm1 %s tracks;tracks npxlayers;tracks dxyerr", ex3[i]), 20, 0, 20, 400, -0.2, 0.2);
    h_nm1_tracks_dxy_v_min_r[i] = fs->make<TH2D>(TString::Format("h_nm1_%s_tracks_dxy_v_min_r", ex3[i]), TString::Format("nm1 %s tracks;tracks min_r;tracks dxyerr", ex3[i]), 20, 0, 20, 400, -0.2, 0.2);
    h_nm1_tracks_dxyerr_v_pt[i] = fs->make<TH2D>(TString::Format("h_nm1_%s_tracks_dxyerr_v_pt", ex3[i]), TString::Format("nm1 %s tracks;tracks pt;tracks dxyerr", ex3[i]), 200, 0, 20, 200, 0, 0.2);
    h_nm1_tracks_dxyerr_v_npxlayers[i] = fs->make<TH2D>(TString::Format("h_nm1_%s_tracks_dxyerr_v_npxlayers", ex3[i]), TString::Format("nm1 %s tracks;tracks npxlayers;tracks dxyerr", ex3[i]), 20, 0, 20, 200, 0, 0.2);
    h_nm1_tracks_dxyerr_v_nstlayers[i] = fs->make<TH2D>(TString::Format("h_nm1_%s_tracks_dxyerr_v_nstlayers", ex3[i]), TString::Format("nm1 %s tracks;tracks nstlayers;tracks dxyerr", ex3[i]), 20, 0, 20, 200, 0, 0.2);
    h_nm1_tracks_dxyerr_v_min_r[i] = fs->make<TH2D>(TString::Format("h_nm1_%s_tracks_dxyerr_v_min_r", ex3[i]), TString::Format("nm1 %s tracks;tracks min_r;tracks dxyerr", ex3[i]), 20, 0, 20, 200, 0, 0.2);
  }

  const char* ex2[2] = {"all", "nm1"};
  for (int i = 0; i < 2; ++i) {
    h_dxyerr_v_ptcut[i] = fs->make<TH2D>(TString::Format("h_%s_dxyerr_v_ptcut", ex2[i]), "", 40, 0, 20, 100, 0, 0.2);
    h_dxyerr_v_npxlayerscut[i] = fs->make<TH2D>(TString::Format("h_%s_dxyerr_v_npxlayerscut", ex2[i]), "", 5, 0, 5, 100, 0, 0.2);
    h_dxyerr_v_nstlayerscut[i] = fs->make<TH2D>(TString::Format("h_%s_dxyerr_v_nstlayerscut", ex2[i]), "", 15, 0, 15, 100, 0, 0.2);
    h_tracks_ptcut[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_ptcut", ex2[i]), "", 40, 0, 20);
    h_tracks_npxlayerscut[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_npxlayerscut", ex2[i]), "", 5, 0, 5);
    h_tracks_nstlayerscut[i] = fs->make<TH1D>(TString::Format("h_%s_tracks_nstlayerscut", ex2[i]), "", 15, 0, 15);
    for (int j = 0; j < 4; ++j) {
      h_dxyerr_v_npxlayerscut_etaslices[i][j] = fs->make<TH2D>(TString::Format("h_%s_dxyerr_v_npxlayerscut_eta%d", ex2[i], j), "", 5, 0, 5, 100, 0, 0.2);
      h_dxyerr_v_nstlayerscut_etaslices[i][j] = fs->make<TH2D>(TString::Format("h_%s_dxyerr_v_nstlayerscut_eta%d", ex2[i], j), "", 15, 0, 15, 100, 0, 0.2);
    }
  }
}

double TrackerMapper::pileup_weight(int mc_npu) const {
  if (mc_npu < 0 || mc_npu >= int(pileup_weights.size()))
    return 0;
  else
    return pileup_weights[mc_npu];
}

void TrackerMapper::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  double w = 1;
  int npu = -1;

  if (!event.isRealData()) {
    edm::Handle<std::vector<PileupSummaryInfo> > pileup_info;
    event.getByToken(pileup_info_token, pileup_info);

    for (std::vector<PileupSummaryInfo>::const_iterator psi = pileup_info->begin(), end = pileup_info->end(); psi != end; ++psi)
      if (psi->getBunchCrossing() == 0)
        npu = psi->getTrueNumInteractions();

    h_npu->Fill(npu);
    w *= pileup_weight(npu);
  }

  h_w->Fill(w);

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByToken(beamspot_token, beamspot);

  const float bsx = beamspot->x0();
  const float bsy = beamspot->y0();
  const float bsz = beamspot->z0();

  h_bsx->Fill(bsx);
  h_bsy->Fill(bsy);
  h_bsz->Fill(bsz);

  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByToken(primary_vertex_token, primary_vertices);

  h_npv->Fill(int(primary_vertices->size()), w);

  for (int j = 0; j < 2; ++j) {
    for (size_t i = 0, ie = j == 0 ? 1 : primary_vertices->size(); i < ie; ++i) {
      const reco::Vertex& pv = (*primary_vertices)[i];
      h_pvx[j]->Fill(pv.x() - bsx, w);
      h_pvy[j]->Fill(pv.y() - bsy, w);
      h_pvz[j]->Fill(pv.z() - bsz, w);
      h_pvrho[j]->Fill(mag(pv.x() - bsx, pv.y() - bsy), w);
      h_pvntracks[j]->Fill(pv.nTracks(), w);
      double pvsumpt2 = 0;
      for (auto trki = pv.tracks_begin(), trke = pv.tracks_end(); trki != trke; ++trki) {
        const double trkpt = (*trki)->pt();
        pvsumpt2 += trkpt * trkpt;
      }
      h_pvsumpt2[j]->Fill(pvsumpt2, w);
    }
  }

  const reco::Vertex* pv = primary_vertices->size() ? &primary_vertices->at(0) : 0;

  edm::Handle<reco::TrackCollection> tracks;
  event.getByToken(track_token, tracks);

  edm::ESHandle<TransientTrackBuilder> tt_builder;
  setup.get<TransientTrackRecord>().get("TransientTrackBuilder", tt_builder);

  int ntracks[3] = {0};
  int ntracks_quality[3][reco::TrackBase::qualitySize] = {{0}};
  for (const reco::Track& tk : *tracks) {
    if (use_duplicateMerge != -1 && (tk.algo() == 2) != use_duplicateMerge) // reco::TrackBase::duplicateMerge
      continue;

    reco::TransientTrack ttk(tt_builder->build(tk));

    TrackerSpaceExtents tracker_extents;
    const double pt = tk.pt();
    const double min_r = tracker_extents.numExtentInRAndZ(tk.hitPattern(), TrackerSpaceExtents::AllowAll).min_r;
    const double npxlayers = tk.hitPattern().pixelLayersWithMeasurement();
    const double nstlayers = tk.hitPattern().stripLayersWithMeasurement();
    const double abseta = fabs(tk.eta());
    const double dxy = tk.dxy(*beamspot);
    const double nsigmadxy = fabs(dxy / tk.dxyError());
    const double nsigmadxy_acc = fabs(ttk.stateAtBeamLine().transverseImpactParameter().significance());

    const bool nm1[5] = {
      pt > 1,
      min_r <= 1,
      npxlayers >= 2,
      nstlayers >= (old_stlayers_cut ? 3 : 6),
      nsigmadxy > 4
    };

    const bool sel = nm1[0] && nm1[1] && nm1[2] && nm1[3];
    const bool seed = sel && nm1[4];

    const bool pt_nm1_sel = nm1[1] && nm1[2] && nm1[3];
    const bool min_r_nm1_sel = nm1[0] && nm1[2] && nm1[3];
    const bool npxlay_nm1_sel = nm1[0] && nm1[1] && nm1[3];
    const bool nstlay_nm1_sel = nm1[0] && nm1[1] && nm1[2];

    for (int i = 0; i < 2; ++i) {
      if (i == 1 && !nm1[4]) continue;

      if (pt_nm1_sel) {
	h_nm1_tracks_pt[i]->Fill(pt, w);
	h_nm1_tracks_dxy_v_pt[i]->Fill(pt, dxy, w);
	h_nm1_tracks_dxyerr_v_pt[i]->Fill(pt, tk.dxyError(), w);
      }
      if (min_r_nm1_sel) {
	h_nm1_tracks_min_r[i]->Fill(min_r, w);
	h_nm1_tracks_dxy_v_min_r[i]->Fill(min_r, dxy, w);
	h_nm1_tracks_dxyerr_v_min_r[i]->Fill(min_r, tk.dxyError(), w);
      }
      if (npxlay_nm1_sel) {
	h_nm1_tracks_npxlayers[i]->Fill(npxlayers, w);
	h_nm1_tracks_dxy_v_npxlayers[i]->Fill(npxlayers, dxy, w);
	h_nm1_tracks_dxyerr_v_npxlayers[i]->Fill(npxlayers, tk.dxyError(), w);
      }
      if (nstlay_nm1_sel) {
	h_nm1_tracks_nstlayers[i]->Fill(nstlayers, w);
	h_nm1_tracks_nstlayers_v_eta[i]->Fill(tk.eta(), nstlayers, w);
	h_nm1_tracks_dxy_v_nstlayers[i]->Fill(nstlayers, dxy, w);
	h_nm1_tracks_dxyerr_v_nstlayers[i]->Fill(nstlayers, tk.dxyError(), w);
      }
      if (nstlay_nm1_sel && abseta <  2.0) h_nm1_tracks_nstlayers_etalt2[i]->Fill(nstlayers, w);
      if (nstlay_nm1_sel && abseta >= 2.0) h_nm1_tracks_nstlayers_etagt2[i]->Fill(nstlayers, w);
      if (sel) h_nm1_tracks_nsigmadxy[i]->Fill(nsigmadxy, w);
    }

    const bool nm1_sel[3] = {
      pt_nm1_sel,
      npxlay_nm1_sel,
      nstlay_nm1_sel
    };
    const double nm1_v[3] = { pt, npxlayers, nstlayers };

    for (int i = 0; i < 2; ++i) {
      TH2D* nm1_h[3] = { h_dxyerr_v_ptcut[i], h_dxyerr_v_npxlayerscut[i], h_dxyerr_v_nstlayerscut[i] };
      TH1D* nm1_h_tracks[3] = { h_tracks_ptcut[i], h_tracks_npxlayerscut[i], h_tracks_nstlayerscut[i] };
      for (int j = 0; j < 3; ++j) {
	if (i == 0 || (i == 1 && nm1_sel[j])) {
	  for (int ibin = 1; ibin <= nm1_h[j]->GetNbinsX(); ++ibin) {
	    const double cut = nm1_h[j]->GetXaxis()->GetBinLowEdge(ibin);
	    if (nm1_v[j] >= cut) nm1_h[j]->Fill(cut, tk.dxyError(), w);
	  }
	  for (int ibin = 1; ibin <= nm1_h_tracks[j]->GetNbinsX(); ++ibin) {
	    const double cut = nm1_h_tracks[j]->GetXaxis()->GetBinLowEdge(ibin);
	    if (nm1_v[j] >= cut) nm1_h_tracks[j]->Fill(cut, w);
	  }
	}
      }

      for (int k = 0; k < 4; ++k) {
	TH2D* nm1_h2[2] = { h_dxyerr_v_npxlayerscut_etaslices[i][k], h_dxyerr_v_nstlayerscut_etaslices[i][k] };
	for (int j = 0; j < 2; ++j) {
	  if (i == 0 || (i == 1 && nm1_sel[j+1])) {
	    for (int ibin = 1; ibin <= nm1_h2[j]->GetNbinsX(); ++ibin) {
	      const double cut = nm1_h2[j]->GetXaxis()->GetBinLowEdge(ibin);
	      if (abseta < 1 && k == 0) {
		if (nm1_v[j+1] >= cut) nm1_h2[j]->Fill(cut, tk.dxyError(), w);
	      }
	      if (abseta < 1.5 && abseta > 1 && k == 1) {
		if (nm1_v[j+1] >= cut) nm1_h2[j]->Fill(cut, tk.dxyError(), w);
	      }
	      if (abseta < 2.5 && abseta > 1.5 && k == 2) {
		if (nm1_v[j+1] >= cut) nm1_h2[j]->Fill(cut, tk.dxyError(), w);
	      }
	      if (abseta > 2.5 && k == 3) {
		if (nm1_v[j+1] >= cut) nm1_h2[j]->Fill(cut, tk.dxyError(), w);
	      }
	    }
	  }
	}
      }
    }

    for (int i = 0; i < 3; ++i) {
      if (i==1 && !sel) continue;
      if (i==2 && !seed) continue;

      ++ntracks[i];

      for (int j = 0; j < reco::TrackBase::qualitySize; ++j)
        if (tk.quality(reco::TrackBase::TrackQuality(j)))
          ++ntracks_quality[i][j];

      h_tracks_algo[i]->Fill(int(tk.algo()), w);
      h_tracks_original_algo[i]->Fill(int(tk.originalAlgo()), w);
      h_tracks_pt[i]->Fill(tk.pt(), w);
      h_tracks_eta[i]->Fill(tk.eta(), w);
      h_tracks_phi[i]->Fill(tk.phi(), w);
      h_tracks_vx[i]->Fill(tk.vx() - bsx, w);
      h_tracks_vy[i]->Fill(tk.vy() - bsy, w);
      h_tracks_vz[i]->Fill(tk.vz() - bsz, w);
      h_tracks_vphi[i]->Fill(atan2(tk.vy() - bsy, tk.vx() - bsx), w);
      h_tracks_dxy[i]->Fill(tk.dxy(*beamspot), w);
      h_tracks_dz[i]->Fill(tk.dz(beamspot->position()), w);
      if (pv) h_tracks_dzpv[i]->Fill(tk.dz(pv->position()), w);
      h_tracks_dxyerr[i]->Fill(tk.dxyError(), w);
      h_tracks_dzerr[i]->Fill(tk.dzError(), w);
      h_tracks_nhits[i]->Fill(tk.hitPattern().numberOfValidHits(), w);
      h_tracks_npxhits[i]->Fill(tk.hitPattern().numberOfValidPixelHits(), w);
      h_tracks_nsthits[i]->Fill(tk.hitPattern().numberOfValidStripHits(), w);

      if (tk.charge() > 0) h_tracks_qp_dxy[i]->Fill(dxy, w);
      if (tk.charge() < 0) h_tracks_qm_dxy[i]->Fill(dxy, w);

      const double z = tk.vz();
      if (z<-5)         h_tracks_dxy_zslices[i][0]->Fill(dxy, w);
      if (z>-5 && z<-2) h_tracks_dxy_zslices[i][1]->Fill(dxy, w);
      if (z>-2 && z<0)  h_tracks_dxy_zslices[i][2]->Fill(dxy, w);
      if (z>0 && z<2)   h_tracks_dxy_zslices[i][3]->Fill(dxy, w);
      if (z>2 && z<5)   h_tracks_dxy_zslices[i][4]->Fill(dxy, w);
      if (z>5)          h_tracks_dxy_zslices[i][5]->Fill(dxy, w);

      h_tracks_min_r[i]->Fill(min_r, w);
      h_tracks_npxlayers[i]->Fill(npxlayers, w);
      h_tracks_nstlayers[i]->Fill(nstlayers, w);
      if (abseta <  2.0) h_tracks_nstlayers_etalt2[i]->Fill(nstlayers, w);
      if (abseta >= 2.0) h_tracks_nstlayers_etagt2[i]->Fill(nstlayers, w);
      h_tracks_nsigmadxy[i]->Fill(nsigmadxy, w);
      h_tracks_nsigmadxy_acc[i]->Fill(nsigmadxy_acc, w);
      h_tracks_nsigmadxy_deltaacc[i]->Fill(nsigmadxy - nsigmadxy_acc, w);

      h_tracks_absdxy[i]->Fill(fabs(dxy), w);

      h_tracks_nstlayers_v_eta[i]->Fill(tk.eta(), nstlayers, w);
      h_tracks_dxy_v_eta[i]->Fill(tk.eta(), dxy, w);
      h_tracks_dxy_v_nstlayers[i]->Fill(nstlayers, dxy, w);
      h_tracks_dxyerr_v_eta[i]->Fill(tk.eta(), tk.dxyError(), w);
      h_tracks_dxyerr_v_nstlayers[i]->Fill(nstlayers, tk.dxyError(), w);
      h_tracks_dxyerr_v_dxy[i]->Fill(dxy, tk.dxyError(), w);
      h_tracks_nsigmadxy_v_eta[i]->Fill(tk.eta(), nsigmadxy, w);
      h_tracks_nsigmadxy_v_nstlayers[i]->Fill(nstlayers, nsigmadxy, w);
      h_tracks_nsigmadxy_v_dxy[i]->Fill(dxy, nsigmadxy, w);
      h_tracks_nsigmadxy_v_dxyerr[i]->Fill(tk.dxyError(), nsigmadxy, w);

      int ipt = pt > 5 ? 5 : int(pt);
      h_tracks_dxyerr_v_dxy_ptslices[i][ipt]->Fill(dxy, tk.dxyError(), w);
    }
  }

  for (int i = 0; i < 3; ++i) {
    h_ntracks[i]->Fill(ntracks[i], w);
    for (int j = 0; j < reco::TrackBase::qualitySize; ++j)
      h_ntracks_quality[i][j]->Fill(ntracks_quality[i][j], w);
  }
}

DEFINE_FWK_MODULE(TrackerMapper);
