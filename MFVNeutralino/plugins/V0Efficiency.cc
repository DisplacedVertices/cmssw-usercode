#include "TH2.h"
#include "TLorentzVector.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "RecoVertex/VertexTools/interface/VertexDistanceXY.h"
#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "JMTucker/MFVNeutralino/interface/V0Hypotheses.h"
#include "JMTucker/Tools/interface/TrackerSpaceExtent.h"

class MFVV0Efficiency : public edm::EDAnalyzer {
public:
  explicit MFVV0Efficiency(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  const edm::EDGetTokenT<reco::VertexCollection> vertices_token;
  const edm::EDGetTokenT<std::vector<PileupSummaryInfo>> pileup_token;
  const std::vector<double> pileup_weights;
  const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
  const edm::EDGetTokenT<reco::VertexCollection> primary_vertex_token;
  const edm::EDGetTokenT<int> n_good_primary_vertices_token;
  const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
  const bool limit_set;
  const double min_track_pt;
  const double min_track_nsigmadxybs;
  const int min_track_npxlayers;
  const int max_track_npxlayers;
  const int min_track_nstlayers;
  const int max_track_nstlayers;
  const int min_track_nstlayersstereo;
  const int max_track_nstlayersstereo;
  const double max_chi2ndf;
  const double min_p;
  const double max_p;
  const double min_eta;
  const double max_eta;
  const bool abs_eta_cut;
  const double mass_window_lo;
  const double mass_window_hi;
  const double min_costh2;
  const double min_costh3;
  const double max_geo2ddist;
  const bool debug;

  TrackerSpaceExtents tracker_extents;

  double w;

  TH1D* h_npu;
  TH1D* h_bsx;
  TH1D* h_bsy;
  TH1D* h_bsz;
  TH1D* h_npv;
  TH1D* h_pvx;
  TH1D* h_pvy;
  TH1D* h_pvz;
  TH1D* h_pvbsx;
  TH1D* h_pvbsy;
  TH1D* h_pvbsz;
  TH1D* h_pvntracks;

  enum { nhyp = 1 }; //mfv::n_V0_hyp };

  TH1D* h_ntracks[nhyp+1];
  TH1D* h_max_track_multiplicity[nhyp+1];
  TH1D* h_track_charge[nhyp+1];
  TH1D* h_track_pt[nhyp+1];
  TH1D* h_track_eta[nhyp+1];
  TH1D* h_track_phi[nhyp+1];
  TH1D* h_track_npxhits[nhyp+1];
  TH1D* h_track_nsthits[nhyp+1];
  TH1D* h_track_npxlayers[nhyp+1];
  TH1D* h_track_nstlayers[nhyp+1];
  TH1D* h_track_nstlayersmono[nhyp+1];
  TH1D* h_track_nstlayersstereo[nhyp+1];
  TH1D* h_track_maxpxlayer[nhyp+1];
  TH1D* h_track_minstlayer[nhyp+1];
  TH1D* h_track_deltapxlayers[nhyp+1];
  TH1D* h_track_deltastlayers[nhyp+1];
  TH1D* h_track_deltastlayers1stereo[nhyp+1];
  TH1D* h_track_deltastlayers2stereo[nhyp+1];
  TH1D* h_track_dxybs[nhyp+1];
  TH1D* h_track_dxypv[nhyp+1];
  TH1D* h_track_dzbs[nhyp+1];
  TH1D* h_track_dzpv[nhyp+1];
  TH1D* h_track_sigmadxy[nhyp+1];
  TH1D* h_track_nsigmadxybs[nhyp+1];
  TH1D* h_track_nsigmadxypv[nhyp+1];

  TH1D* h_nvtx;

  TH1D* h_prefit_p[nhyp];
  TH1D* h_prefit_mass[nhyp];
  TH1D* h_vtx_chi2ndf[nhyp];
  TH2D* h_vtx_2d[nhyp];
  TH1D* h_vtx_x[nhyp];
  TH1D* h_vtx_y[nhyp];
  TH1D* h_vtx_z[nhyp];
  TH1D* h_vtx_r[nhyp];
  TH1D* h_vtx_rho[nhyp];
  TH1D* h_vtx_nsigrho[nhyp];
  TH2D* h_vtx_rho_vs_p[nhyp];
  TH2D* h_vtx_rho_vs_mass[nhyp];
  TH1D* h_vtx_angle[nhyp];
  TH2D* h_vtx_angle_vs_p[nhyp];
  TH2D* h_vtx_angle_vs_mass[nhyp];
  TH2D* h_vtx_track_pt_0v1[nhyp];
  TH2D* h_vtx_track_eta_0v1[nhyp];
  TH2D* h_vtx_track_phi_0v1[nhyp];
  TH2D* h_vtx_track_dxybs_0v1[nhyp];
  TH2D* h_vtx_track_dxybs_0v1_zoom[nhyp];
  TH1D* h_vtx_p[nhyp];
  TH1D* h_vtx_costh3[nhyp];
  TH1D* h_vtx_costh2[nhyp];
  TH1D* h_vtx_mass[nhyp];

  void fill(TH1* h, double x) {
    if (h == 0) {
      assert(limit_set);
      return;
    }
    h->Fill(x, w);
  }

  void fill(TH2* h, double x, double y) {
    if (h == 0) {
      assert(limit_set);
      return;
    }
    h->Fill(x, y, w);
  }
};

MFVV0Efficiency::MFVV0Efficiency(const edm::ParameterSet& cfg)
  : vertices_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("vertices_src"))),
    pileup_token(consumes<std::vector<PileupSummaryInfo>>(edm::InputTag("slimmedAddPileupInfo"))),
    pileup_weights(cfg.getParameter<std::vector<double>>("pileup_weights")),
    beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot_src"))),
    primary_vertex_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("primary_vertex_src"))),
    n_good_primary_vertices_token(consumes<int>(edm::InputTag(cfg.getParameter<edm::InputTag>("primary_vertex_src").label(), "nGood"))),
    tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("tracks_src"))),
    limit_set(cfg.getParameter<bool>("limit_set")),
    min_track_pt(cfg.getParameter<double>("min_track_pt")),
    min_track_nsigmadxybs(cfg.getParameter<double>("min_track_nsigmadxybs")),
    min_track_npxlayers(cfg.getParameter<int>("min_track_npxlayers")),
    max_track_npxlayers(cfg.getParameter<int>("max_track_npxlayers")),
    min_track_nstlayers(cfg.getParameter<int>("min_track_nstlayers")),
    max_track_nstlayers(cfg.getParameter<int>("max_track_nstlayers")),
    min_track_nstlayersstereo(cfg.getParameter<int>("min_track_nstlayersstereo")),
    max_track_nstlayersstereo(cfg.getParameter<int>("max_track_nstlayersstereo")),
    max_chi2ndf(cfg.getParameter<double>("max_chi2ndf")),
    min_p(cfg.getParameter<double>("min_p")),
    max_p(cfg.getParameter<double>("max_p")),
    min_eta(cfg.getParameter<double>("min_eta")),
    max_eta(cfg.getParameter<double>("max_eta")),
    abs_eta_cut(cfg.getParameter<bool>("abs_eta_cut")),
    mass_window_lo(cfg.getParameter<double>("mass_window_lo")),
    mass_window_hi(cfg.getParameter<double>("mass_window_hi")),
    min_costh2(cfg.getParameter<double>("min_costh2")),
    min_costh3(cfg.getParameter<double>("min_costh3")),
    max_geo2ddist(cfg.getParameter<double>("max_geo2ddist")),
    debug(cfg.getUntrackedParameter<bool>("debug", false))
{
  edm::Service<TFileService> fs;
  TH1::SetDefaultSumw2();

  h_npu = h_bsx = h_bsy = h_bsz = h_npv = h_pvx = h_pvy = h_pvz = h_pvbsx = h_pvbsy = h_pvbsz = h_pvntracks = h_nvtx = 0;
  for (size_t i = 0; i < nhyp+1; ++i)
    h_ntracks[i] = h_max_track_multiplicity[i] = h_track_charge[i] = h_track_pt[i] = h_track_eta[i] = h_track_phi[i] = h_track_npxhits[i] = h_track_nsthits[i] = h_track_npxlayers[i] = h_track_nstlayers[i] =  h_track_nstlayersmono[i] = h_track_nstlayersstereo[i] = h_track_maxpxlayer[i] = h_track_minstlayer[i] = h_track_deltapxlayers[i] = h_track_deltastlayers[i] = h_track_deltastlayers1stereo[i] = h_track_deltastlayers2stereo[i] = h_track_dxybs[i] = h_track_dxypv[i] = h_track_dzbs[i] = h_track_dzpv[i] = h_track_sigmadxy[i] = h_track_nsigmadxybs[i] = h_track_nsigmadxypv[i] = 0;

  for (size_t i = 0; i < nhyp; ++i) {
    h_prefit_p[i] = h_prefit_mass[i] = h_vtx_chi2ndf[i] = h_vtx_x[i] = h_vtx_y[i] = h_vtx_z[i] = h_vtx_r[i] = h_vtx_rho[i] = h_vtx_nsigrho[i] = h_vtx_angle[i] = h_vtx_p[i] = h_vtx_costh3[i] = h_vtx_costh2[i] = h_vtx_mass[i] = 0;
    h_vtx_2d[i] = h_vtx_rho_vs_p[i] = h_vtx_rho_vs_mass[i] = h_vtx_angle_vs_p[i] = h_vtx_angle_vs_mass[i] = h_vtx_track_pt_0v1[i] = h_vtx_track_eta_0v1[i] = h_vtx_track_phi_0v1[i] = h_vtx_track_dxybs_0v1[i] = h_vtx_track_dxybs_0v1_zoom[i] = 0;
  }

  if (!limit_set) {
    h_npu = fs->make<TH1D>("h_npu", ";true npu", 100, 0, 100);
    h_bsx = fs->make<TH1D>("h_bsx", ";beamspot x", 4000, -2, 2);
    h_bsy = fs->make<TH1D>("h_bsy", ";beamspot y", 4000, -2, 2);
    h_bsz = fs->make<TH1D>("h_bsz", ";beamspot z", 4000, -20, 20);
    h_npv = fs->make<TH1D>("h_npv", ";number of primary vertices", 100, 0, 100);
    h_pvx = fs->make<TH1D>("h_pvx", ";primary vertex x (cm)", 4000, -2, 2);
    h_pvy = fs->make<TH1D>("h_pvy", ";primary vertex y (cm)", 4000, -2, 2);
    h_pvz = fs->make<TH1D>("h_pvz", ";primary vertex z (cm)", 4000, -20, 20);
    h_pvbsx = fs->make<TH1D>("h_pvbsx", ";primary vertex x - beam spot x (cm)", 4000, -2, 2);
    h_pvbsy = fs->make<TH1D>("h_pvbsy", ";primary vertex y - beam spot y (cm)", 4000, -2, 2);
    h_pvbsz = fs->make<TH1D>("h_pvbsz", ";primary vertex z - beam spot z (cm)", 4000, -20, 20);
    h_pvntracks = fs->make<TH1D>("h_pvntracks", ";# tracks in primary vertex;events/5", 100, 0, 500);
  }

  auto booktracks = [&](TFileDirectory& d, int i) {
    if (limit_set && i == nhyp)
      return;
    h_ntracks[i] = d.make<TH1D>("h_ntracks", ";# of selected tracks;events/1", 100, 0, 100);
    h_max_track_multiplicity[i] = d.make<TH1D>("h_max_track_multiplicity", ";max multiplicity of any track in vertices;events/1", 10, 0, 10);
    h_track_charge[i] = d.make<TH1D>("h_track_charge", ";track charge;tracks/1", 3, -1, 2);
    h_track_pt[i] = d.make<TH1D>("h_track_pt", ";track p_{T} (GeV);tracks/100 MeV", 1000, 0, 100);
    h_track_eta[i] = d.make<TH1D>("h_track_eta", ";track #eta;tracks/0.01", 520, -2.6, 2.6);
    h_track_phi[i] = d.make<TH1D>("h_track_phi", ";track #eta;tracks/0.01", 630, -M_PI, M_PI);
    h_track_npxhits[i] = d.make<TH1D>("h_track_npxhits", ";track # pixel hits;tracks/1", 15, 0, 15);
    h_track_nsthits[i] = d.make<TH1D>("h_track_nsthits", ";track # strip hits;tracks/1", 40, 0, 40);
    h_track_npxlayers[i] = d.make<TH1D>("h_track_npxlayers", ";track # pixel layers;tracks/1", 7, 0, 7);
    h_track_nstlayers[i] = d.make<TH1D>("h_track_nstlayers", ";track # strip layers;tracks/1", 20, 0, 20);
    h_track_nstlayersmono[i] = d.make<TH1D>("h_track_nstlayersmono", ";track # mono strip layers;tracks/1", 20, 0, 20);
    h_track_nstlayersstereo[i] = d.make<TH1D>("h_track_nstlayersstereo", ";track # stereo strip layers;tracks/1", 20, 0, 20);
    h_track_maxpxlayer[i] = d.make<TH1D>("h_track_maxpxlayer", ";track max pixel layer;tracks/1", 7, 0, 7);
    h_track_minstlayer[i] = d.make<TH1D>("h_track_minstlayer", ";track min strip layer;tracks/1", 20, 0, 20);
    h_track_deltapxlayers[i] = d.make<TH1D>("h_track_deltapxlayers", ";track delta pixel layers;tracks/1", 7, 0, 7);
    h_track_deltastlayers[i] = d.make<TH1D>("h_track_deltastlayers", ";track delta strip layers;tracks/1", 20, 0, 20);
    h_track_deltastlayers1stereo[i] = d.make<TH1D>("h_track_deltastlayers1stereo", ";track delta strip layers (one stereo);tracks/1", 20, 0, 20);
    h_track_deltastlayers2stereo[i] = d.make<TH1D>("h_track_deltastlayers2stereo", ";track delta strip layers (both stereo);tracks/1", 20, 0, 20);
    h_track_dxybs[i] = d.make<TH1D>("h_track_dxybs", ";track dxy to BS (cm);tracks/10 #mum", 4000, -2, 2);
    h_track_dxypv[i] = d.make<TH1D>("h_track_dxypv", ";track dxy to PV (cm);tracks/10 #mum", 4000, -2, 2);
    h_track_dzbs[i] = d.make<TH1D>("h_track_dzbs", ";track dz to BS (cm);tracks/100 #mum", 4000, -20, 20);
    h_track_dzpv[i] = d.make<TH1D>("h_track_dzpv", ";track dz to PV (cm);tracks/100 #mum", 4000, -20, 20);
    h_track_sigmadxy[i] = d.make<TH1D>("h_track_sigmadxy", ";track #sigma(dxy) (cm);tracks/5 #mum", 200, 0, 0.1);
    h_track_nsigmadxybs[i] = d.make<TH1D>("h_track_nsigmadxybs", ";track N#sigma(dxy) to BS (cm);tracks/0.1", 1000, 0, 100);
    h_track_nsigmadxypv[i] = d.make<TH1D>("h_track_nsigmadxypv", ";track N#sigma(dxy) to PV (cm);tracks/0.1", 1000, 0, 100);
  };

  booktracks(fs->tFileDirectory(), nhyp);

  if (!limit_set) h_nvtx = fs->make<TH1D>("h_nvtx", ";# of vertices;events/1", 50, 0, 50);

  for (int ihyp = 0; ihyp < nhyp; ++ihyp) {
    TFileDirectory d = fs->mkdir(mfv::V0_hypotheses[ihyp].name);

    booktracks(d, ihyp);

    if (!limit_set) {
      h_prefit_p[ihyp] = d.make<TH1D>("h_prefit_p", ";pre-fit candidate momentum (GeV);candidates/100 MeV", 5000, 0, 500);
      h_prefit_mass[ihyp] = d.make<TH1D>("h_prefit_mass", ";pre-fit candidate invariant mass (GeV);candidates/1 MeV", 5000, 0, 5);

      h_vtx_chi2ndf[ihyp] = d.make<TH1D>("h_vtx_chi2ndf", ";candidate vertex #chi^{2}/ndf;candidates/0.05", 200, 0, 10);
      h_vtx_2d[ihyp] = d.make<TH2D>("h_vtx_2d", ";candidate vertex x (cm);candidate veretx y (cm)", 800, -4,4, 800, -4, 4);
      h_vtx_x[ihyp] = d.make<TH1D>("h_vtx_x", ";candidate vertex x - pv x (cm);candidates/40 #mum", 2000, -4,4);
      h_vtx_y[ihyp] = d.make<TH1D>("h_vtx_y", ";candidate vertex y - pv y (cm);candidates/40 #mum", 2000, -4,4);
      h_vtx_z[ihyp] = d.make<TH1D>("h_vtx_z", ";candidate vertex z - pv z (cm);candidates/40 #mum", 2000, -4,4);
      h_vtx_r[ihyp] = d.make<TH1D>("h_vtx_r", ";candidate vertex - pv (cm);candidates/40 #mum", 2000, 0, 8);
    }

    h_vtx_rho[ihyp] = d.make<TH1D>("h_vtx_rho", ";candidate vertex - pv (2D) (cm);candidates/10 #mum", 2000, 0, 8);

    if (!limit_set) {
      h_vtx_nsigrho[ihyp] = d.make<TH1D>("h_vtx_nsigrho", ";N#sigma(candidate vertex - pv (2D));candidates/0.01", 10000, 0, 100);
      h_vtx_rho_vs_p[ihyp] = d.make<TH2D>("h_vtx_rho_vs_p", ";candidate p (GeV);candidate vertex - pv (2D) (cm)", 400,0,100, 400, 0, 4);
      h_vtx_rho_vs_mass[ihyp] = d.make<TH2D>("h_vtx_rho_vs_mass", ";candidate mass (GeV);candidate vertex - pv (2D) (cm)", 220, 0.380,0.600, 400, 0, 4);

      h_vtx_angle[ihyp] = d.make<TH1D>("h_vtx_angle", ";candidate vertex opening angle (rad);candidates/0.0315", 100, 0, M_PI);
      h_vtx_angle_vs_p[ihyp] = d.make<TH2D>("h_vtx_angle_vs_p", ";candidate vertex momentum (GeV);candidate vertex opening angle (rad)", 400,0,100, 100, 0, M_PI);
      h_vtx_angle_vs_mass[ihyp] = d.make<TH2D>("h_vtx_angle_vs_mass", ";candidate vertex mass (GeV);candidate vertex opening angle (rad)", 220, 0.380,0.600, 100, 0, M_PI);

      h_vtx_track_pt_0v1[ihyp] = d.make<TH2D>("h_vtx_track_pt_0v1", ";+ve track p_{T} (GeV);-ve track p_{T} (GeV)", 200, 0, 20, 200, 0, 20);
      h_vtx_track_eta_0v1[ihyp] = d.make<TH2D>("h_vtx_track_eta_0v1", ";+ve track #eta;-ve track #eta", 200, -3, 3, 200, -3, 3);
      h_vtx_track_phi_0v1[ihyp] = d.make<TH2D>("h_vtx_track_phi_0v1", ";+ve track #phi;-ve track #phi", 200, -M_PI, M_PI, 200, -M_PI, M_PI);
      h_vtx_track_dxybs_0v1[ihyp] = d.make<TH2D>("h_vtx_track_dxybs_0v1", ";+ve track dxy(BS) (cm);-ve track dxy(BS) (cm)", 400, -0.1, 0.1, 400, -0.1, 0.1);
      h_vtx_track_dxybs_0v1_zoom[ihyp] = d.make<TH2D>("h_vtx_track_dxybs_0v1_zoom", ";+ve track dxy(BS) (cm);-ve track dxy(BS) (cm)", 400, -2, 2, 400, -2, 2);

      h_vtx_costh3[ihyp] = d.make<TH1D>("h_vtx_costh3", ";post-fit candidate cos(angle between displacement and flight dir);candidates/0.001", 2001, -1, 1.01);
      h_vtx_costh2[ihyp] = d.make<TH1D>("h_vtx_costh2", ";post-fit candidate cos(angle between displacement and flight dir (2D));candidates/0.001", 2001, -1, 1.01);
    }
    h_vtx_p[ihyp] = d.make<TH1D>("h_vtx_p", ";post-fit candidate momentum (GeV);candidates/1 GeV", 400, 0, 100);
    h_vtx_mass[ihyp] = d.make<TH1D>("h_vtx_mass", ";post-fit candidate invariant mass (GeV);candidates/1 MeV", 5000, 0, 5);
  }
}

void MFVV0Efficiency::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  const bool is_mc = !event.isRealData();
  w = 1;

  if (is_mc) {
    edm::Handle<std::vector<PileupSummaryInfo> > pileup;
    event.getByToken(pileup_token, pileup);

    int npu = -1;
    for (std::vector<PileupSummaryInfo>::const_iterator psi = pileup->begin(), end = pileup->end(); psi != end; ++psi)
      if (psi->getBunchCrossing() == 0)
        npu = psi->getTrueNumInteractions();

    assert(npu >= 0);
    fill(h_npu, npu); // w is still 1
    if (npu >= int(pileup_weights.size()))
      w *= pileup_weights.back();
    else
      w *= pileup_weights[npu];
  }

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByToken(beamspot_token, beamspot);

  const double bsx = beamspot->x0();
  const double bsy = beamspot->y0();
  const double bsz = beamspot->z0();

  fill(h_bsx, bsx);
  fill(h_bsy, bsy);
  fill(h_bsz, bsz);

  edm::Handle<reco::VertexCollection> primary_vertex;
  event.getByToken(primary_vertex_token, primary_vertex);
  edm::Handle<int> n_good_primary_vertices;
  event.getByToken(n_good_primary_vertices_token, n_good_primary_vertices);

  const reco::Vertex& pv = (*primary_vertex)[0];
  const int npv = *n_good_primary_vertices;
  fill(h_npv, npv);

  const double pvx = pv.x();
  const double pvy = pv.y();
  const double pvz = pv.z();
  const int pvntracks = -1; // pv.nTracks();

  fill(h_pvx, pvx);
  fill(h_pvy, pvy);
  fill(h_pvz, pvz);
  fill(h_pvbsx, pvx - bsx);
  fill(h_pvbsy, pvy - bsy);
  fill(h_pvbsz, pvz - bsz);
  fill(h_pvntracks, pvntracks);
  
  if (debug) printf("\nEVENT (%u, %u, %llu) npv %i weight %f\n", event.id().run(), event.luminosityBlock(), event.id().event(), npv, w);

  edm::Handle<reco::TrackCollection> tracks;
  event.getByToken(tracks_token, tracks);
  const size_t ntracks = tracks->size();
  fill(h_ntracks[nhyp], ntracks);

  auto filltrack = [&](const int i, const reco::Track& tk) {
    const reco::HitPattern& p = tk.hitPattern();

    fill(h_track_charge[i], tk.charge());
    fill(h_track_pt[i], tk.pt());
    fill(h_track_eta[i], tk.eta());
    fill(h_track_phi[i], tk.phi());
    fill(h_track_npxhits[i], p.numberOfValidPixelHits());
    fill(h_track_nsthits[i], p.numberOfValidStripHits());
    fill(h_track_npxlayers[i], p.pixelLayersWithMeasurement());
    fill(h_track_nstlayers[i], p.stripLayersWithMeasurement());
    fill(h_track_dxybs[i], tk.dxy(*beamspot));
    fill(h_track_dxypv[i], tk.dxy(pv.position()));
    fill(h_track_dzbs[i], tk.dz(beamspot->position()));
    fill(h_track_dzpv[i], tk.dz(pv.position()));
    fill(h_track_sigmadxy[i], tk.dxyError());
    fill(h_track_nsigmadxybs[i], tk.dxy(*beamspot) / tk.dxyError());
    fill(h_track_nsigmadxypv[i], tk.dxy(pv.position()) / tk.dxyError());

    NumExtents pixel = tracker_extents.numExtentInRAndZ(p, TrackerSpaceExtents::PixelOnly);
    NumExtents strip = tracker_extents.numExtentInRAndZ(p, TrackerSpaceExtents::StripOnly);
    fill(h_track_nstlayersmono[i], p.stripLayersWithMeasurement() - p.numberOfValidStripLayersWithMonoAndStereo());
    fill(h_track_nstlayersstereo[i], p.numberOfValidStripLayersWithMonoAndStereo());
    fill(h_track_maxpxlayer[i], pixel.max_r);
    fill(h_track_minstlayer[i], strip.min_r);
    fill(h_track_deltapxlayers[i], pixel.max_r - pixel.min_r);
    fill(h_track_deltastlayers[i], strip.max_r - strip.min_r);
  };

  for (size_t itk = 0; itk < ntracks; ++itk)
    filltrack(nhyp, (*tracks)[itk]);

  edm::Handle<reco::VertexCollection> vertices;
  event.getByToken(vertices_token, vertices);
  const size_t nvtx = vertices->size();
  fill(h_nvtx, nvtx);

  std::vector<std::multiset<reco::TrackRef>> tracks_used(nhyp);

  for (size_t ivtx = 0; ivtx < nvtx; ++ivtx) {
    const reco::Vertex& v = (*vertices)[ivtx];
    const double chi2ndf = v.normalizedChi2();
    if (chi2ndf > max_chi2ndf)
      continue;

    const size_t ndaughters = v.tracksSize();
    if (debug) std::cout << "ivtx " << ivtx << " chi2 " << chi2ndf << " ntracks " << ndaughters << " has refits? " << v.hasRefittedTracks() << std::endl;
    std::vector<int> charges(ndaughters, 0);
    std::vector<TVector3> v3s(ndaughters);
    std::vector<reco::TrackRef> refs(ndaughters);
    bool tracks_ok = true;

    int itk = 0;
    for (auto it = v.tracks_begin(), ite = v.tracks_end(); it != ite; ++it, ++itk) {
      const reco::Track& tk = **it;
      const double nsigmadxybs = fabs(tk.dxy(*beamspot) / tk.dxyError());
      const int npxlayers = tk.hitPattern().pixelLayersWithMeasurement();
      const int nstlayers = tk.hitPattern().stripLayersWithMeasurement();
      const int nstlayersstereo = tk.hitPattern().numberOfValidStripLayersWithMonoAndStereo();
      if (tk.pt() < min_track_pt ||
          nsigmadxybs < min_track_nsigmadxybs ||
          npxlayers < min_track_npxlayers ||
          npxlayers > max_track_npxlayers ||
          nstlayers < min_track_nstlayers ||
          nstlayers > max_track_nstlayers ||
          nstlayersstereo < min_track_nstlayersstereo ||
          nstlayersstereo > max_track_nstlayersstereo
          ) {
        tracks_ok = false;
        break;
      }

      charges[itk] = tk.charge();
      v3s[itk].SetPtEtaPhi(tk.pt(), tk.eta(), tk.phi());
      refs[itk] = it->castTo<reco::TrackRef>();
    }

    if (!tracks_ok)
      continue;
        
    for (size_t ihyp = 0; ihyp < nhyp; ++ihyp) {
      const auto& hyp = mfv::V0_hypotheses[ihyp];
      if (debug) printf("hypothesis %s:\n", hyp.name);
      if (ndaughters != hyp.ndaughters())
        continue;

      std::vector<double> test(hyp.charges_and_masses);

      do {
        if (debug) {
          printf("permutation:");
          for (size_t idau = 0; idau < ndaughters; ++idau)
            printf(" %10.4f", test[idau]);
          printf("\n");
        }

        bool all_same = true, all_opp = true;
        for (size_t idau = 0; idau < ndaughters; ++idau) {
          const int x = charges[idau] * (test[idau] > 0 ? 1 : -1);
          if (x > 0) all_opp = false;
          if (x < 0) all_same = false;
        }
        if (debug) printf("all same? %i opp? %i\n", all_same, all_opp);

        if (!all_same && !all_opp)
          continue;

        TLorentzVector sum_prefit, p4;
        for (size_t idau = 0; idau < ndaughters; ++idau) {
          const double mass = fabs(test[idau]);
          p4.SetVectM(v3s[idau], mass);
          sum_prefit += p4;
        }

        if (debug) printf(" pre-fit 4-vector: p = %10.4f y = %10.4f eta = %10.4f phi = %10.4f M = %10.4f>\n", sum_prefit.P(), sum_prefit.Rapidity(), sum_prefit.Eta(), sum_prefit.Phi(), sum_prefit.M());

        const double x = v.x();
        const double y = v.y();
        const double z = v.z();
        const double nsigrho = VertexDistanceXY().distance(v, pv).significance();

        const TVector3 flight(x - pv.x(), y - pv.y(), z - pv.z());
        const TVector3 flight_dir(flight.Unit());
        const TVector2 flight_dir_2(flight_dir.X(), flight_dir.Y());

        TLorentzVector sum;
        for (size_t idau = 0; idau < ndaughters; ++idau) {
          const reco::Track refit_tk = v.refittedTrack(refs[idau]);
          const double mass = fabs(test[idau]); 
          p4.SetXYZM(refit_tk.px(), refit_tk.py(), refit_tk.pz(), mass);
          sum += p4;
        }

        auto get_angle = [&](const reco::Track& tk0, const reco::Track& tk1) { return acos((tk0.px() * tk1.px() + tk0.py() * tk1.py() + tk0.pz() * tk1.pz()) / tk0.p() / tk1.p()); };
        const double angle = ndaughters == 2 ? get_angle(v.refittedTrack(refs[0]), v.refittedTrack(refs[1])) : -1;
        const double mass = sum.M();
        const double p = sum.P();
        const double eta = sum.Eta();
        const double eta_cut = abs_eta_cut ? fabs(eta) : eta;
        const double costh3 = sum.Vect().Unit().Dot(flight_dir);
        const double costh2 = cos(sum.Vect().Unit().XYvector().DeltaPhi(flight_dir_2)); // wtf
        const double geo2ddist = hypot(x, y);
        const double mass_lo = mass_window_lo < 0 ? -mass_window_lo : hyp.mass - mass_window_lo;
        const double mass_hi = mass_window_hi < 0 ? -mass_window_hi : hyp.mass + mass_window_hi;
        const bool use =
          p >= min_p &&
          p < max_p && // < and not <= for disjoint bins
          eta_cut >= min_eta &&
          eta_cut < max_eta &&
          mass >= mass_lo &&
          mass <= mass_hi &&
          costh2 >= min_costh2 &&
          costh3 >= min_costh3 &&
          geo2ddist < max_geo2ddist;

        if (debug) {
          printf("vertex chi2: %10.4f (%.1f dof)  position: <%10.4f %10.4f %10.4f>  err: <%10.4f %10.4f %10.4f / %10.4f %10.4f / %10.4f>\n",
                 chi2ndf, v.ndof(), x, y, z, v.covariance(0,0), v.covariance(0,1), v.covariance(0,2), v.covariance(1,1), v.covariance(1,2), v.covariance(2,2));
          printf("post-fit 4-vector: p = %10.4f y = %10.4f eta = %10.4f phi = %10.4f M = %10.4f>\n", p, sum.Rapidity(), sum.Eta(), sum.Phi(), mass);
          printf("use? %i\n", use);
        }

        if (!use)
          continue;

        tracks_used[ihyp].insert(refs.begin(), refs.end());

        fill(h_vtx_chi2ndf[ihyp], chi2ndf);
        fill(h_vtx_2d[ihyp], x, y);
        fill(h_vtx_x[ihyp], flight.X());
        fill(h_vtx_y[ihyp], flight.Y());
        fill(h_vtx_z[ihyp], flight.Z());
        fill(h_vtx_r[ihyp], flight.Mag());
        fill(h_vtx_rho[ihyp], flight.Perp());
        fill(h_vtx_rho_vs_p[ihyp], sum.P(), flight.Perp());
        fill(h_vtx_rho_vs_mass[ihyp], mass, flight.Perp());
        fill(h_vtx_nsigrho[ihyp], nsigrho);

        fill(h_vtx_angle[ihyp], angle);
        fill(h_vtx_angle_vs_p[ihyp], p, angle);
        fill(h_vtx_angle_vs_mass[ihyp], mass, angle);

        fill(h_vtx_p[ihyp], p);
        fill(h_vtx_costh3[ihyp], costh3);
        fill(h_vtx_costh2[ihyp], costh2);
        fill(h_vtx_mass[ihyp], mass);

        fill(h_prefit_p[ihyp], sum_prefit.P());
        fill(h_prefit_mass[ihyp], sum_prefit.M());

        if (ndaughters == 2) {
          const bool neg_first = v.refittedTrack(refs[0]).charge() < 0;
          const reco::Track& tkpos = v.refittedTrack(refs[ neg_first]);
          const reco::Track& tkneg = v.refittedTrack(refs[!neg_first]);
          fill(h_vtx_track_pt_0v1[ihyp], tkpos.pt(), tkneg.pt());
          fill(h_vtx_track_eta_0v1[ihyp], tkpos.eta(), tkneg.eta());
          fill(h_vtx_track_phi_0v1[ihyp], tkpos.phi(), tkneg.phi());
          fill(h_vtx_track_dxybs_0v1[ihyp], tkpos.dxy(*beamspot), tkneg.dxy(*beamspot));
          fill(h_vtx_track_dxybs_0v1_zoom[ihyp], tkpos.dxy(*beamspot), tkneg.dxy(*beamspot));
        }
      }
      while (std::next_permutation(test.begin(), test.end()));
    }
  }

  for (size_t ihyp = 0; ihyp < nhyp; ++ihyp) {
    int max_mult = 0;
    for (auto r : tracks_used[ihyp]) {
      const int mult = tracks_used[ihyp].count(r);
      if (mult > max_mult)
        max_mult = mult;
    }
    fill(h_max_track_multiplicity[ihyp], max_mult);

    int ntracks = 0;
    for (auto tkref : tracks_used[ihyp]) {
      ++ntracks;
      filltrack(ihyp, *tkref);
    }
    fill(h_ntracks[ihyp], ntracks);
  }
}

DEFINE_FWK_MODULE(MFVV0Efficiency);
