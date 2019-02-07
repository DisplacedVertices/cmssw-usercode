#include "TTree.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "JMTucker/Tools/interface/TrackingTree.h"
#include "JMTucker/Tools/interface/TrackerSpaceExtent.h"

class TrackingTreer : public edm::EDAnalyzer {
public:
  explicit TrackingTreer(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  const bool input_is_miniaod;
  const edm::EDGetTokenT<std::vector<PileupSummaryInfo>> pileup_token;
  const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
  const edm::EDGetTokenT<reco::VertexCollection> primary_vertices_token;
  const edm::EDGetTokenT<edm::ValueMap<float>> primary_vertex_scores_token;
  const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
  const bool assert_diag_cov;
  const bool track_sel;

  TTree* tree;
  TrackingTree nt;
};

TrackingTreer::TrackingTreer(const edm::ParameterSet& cfg)
  : input_is_miniaod(cfg.getParameter<bool>("input_is_miniaod")),
    pileup_token(consumes<std::vector<PileupSummaryInfo>>(cfg.getParameter<edm::InputTag>("pileup_info_src"))),
    beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot_src"))),
    primary_vertices_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("primary_vertices_src"))),
    primary_vertex_scores_token(consumes<edm::ValueMap<float>>(cfg.getParameter<edm::InputTag>("primary_vertices_src"))),
    tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("tracks_src"))),
    assert_diag_cov(cfg.getParameter<bool>("assert_diag_cov")),
    track_sel(cfg.getParameter<bool>("track_sel"))
{
  edm::Service<TFileService> fs;
  tree = fs->make<TTree>("t", "");
  nt.write_to_tree(tree);
}

void TrackingTreer::analyze(const edm::Event& event, const edm::EventSetup&) {
  nt.clear();
  nt.set_event(event.id().run(), event.luminosityBlock(), event.id().event());

  if (!event.isRealData()) {
    edm::Handle<std::vector<PileupSummaryInfo> > pileup;
    event.getByToken(pileup_token, pileup);

    for (std::vector<PileupSummaryInfo>::const_iterator psi = pileup->begin(), end = pileup->end(); psi != end; ++psi)
      if (psi->getBunchCrossing() == 0)
        nt.set_npu(psi->getTrueNumInteractions());
  }

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByToken(beamspot_token, beamspot);

  nt.set_bs(beamspot->x0(), beamspot->y0(), beamspot->z0(),
            beamspot->sigmaZ(), beamspot->dxdz(), beamspot->dydz(), beamspot->BeamWidthX(), // set equal to Y
            beamspot->x0Error(), beamspot->y0Error(), beamspot->z0Error(),
            beamspot->sigmaZ0Error(), beamspot->dxdzError(), beamspot->dydzError(), beamspot->BeamWidthXError());

  if (assert_diag_cov)
    for (int i = 0; i < 7; ++i)
      for (int j = i+1; j < 7; ++j)
        if (beamspot->covariance(i,j) > 1e-8)
          throw cms::Exception("BadAssumption", "non-zero cov matrix") << "beamspot cov(" << i << "," << j << ") = " << beamspot->covariance(i,j) << std::endl;

  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByToken(primary_vertices_token, primary_vertices);
  const reco::Vertex* the_pv = primary_vertices->size() ? &(*primary_vertices)[0] : 0;
  edm::Handle<edm::ValueMap<float>> primary_vertex_scores;
  if (input_is_miniaod)
      event.getByToken(primary_vertex_scores_token, primary_vertex_scores);

  for (size_t i = 0, ie = primary_vertices->size(); i < ie; ++i) {
    const reco::Vertex& pv = (*primary_vertices)[i];
    if (pv.isFake() || pv.ndof() < 4 || fabs(pv.z()) > 24 || fabs(pv.position().Rho()) > 2)
      continue;

    float score = 0;
    if (input_is_miniaod)
      score = (*primary_vertex_scores)[reco::VertexRef(primary_vertices, i)];
    else
      for (auto it = pv.tracks_begin(); it != pv.tracks_end(); ++it)
        score += pow((**it).pt(), 2);

    nt.add_pv(pv.x(), pv.y(), pv.z(), pv.normalizedChi2(), pv.ndof(), score,
              pv.covariance(0,0), pv.covariance(0,1), pv.covariance(0,2),
                                  pv.covariance(1,1), pv.covariance(1,2),
                                                      pv.covariance(2,2));
  }

  edm::Handle<reco::TrackCollection> tracks;
  event.getByToken(tracks_token, tracks);

  TrackerSpaceExtents tracker_extents;

  for (const reco::Track& tk : *tracks) {
    if (track_sel && (tk.pt() < 1 || tk.hitPattern().pixelLayersWithMeasurement() < 2 || tk.hitPattern().stripLayersWithMeasurement() < 6))
      continue;

    const reco::HitPattern& hp = tk.hitPattern();
    NumExtents ex    = tracker_extents.numExtentInRAndZ(tk.hitPattern(), TrackerSpaceExtents::AllowAll);
    NumExtents ex_px = tracker_extents.numExtentInRAndZ(tk.hitPattern(), TrackerSpaceExtents::PixelOnly);

    nt.add_tk(tk.charge(), tk.pt(), tk.eta(), tk.phi(),
              tk.dxy(*beamspot),
              the_pv ? tk.dxy(the_pv->position()) : 1e99,
              the_pv ? tk.dz (the_pv->position()) : 1e99,
              tk.vx(), tk.vy(), tk.vz(),
              tk.ptError(), tk.etaError(), tk.phiError(), tk.dxyError(), tk.dzError(), tk.normalizedChi2(),
              hp.numberOfValidPixelHits(),
              hp.numberOfValidStripHits(),
              hp.pixelLayersWithMeasurement(),
              hp.stripLayersWithMeasurement(),
              ex.min_r < 2e9 ? ex.min_r : 0,
              ex.min_z < 2e9 ? ex.min_z : 0,
              ex.max_r > -2e9 ? ex.max_r : 0,
              ex.max_z > -2e9 ? ex.max_z : 0,
              ex_px.max_r > -2e9 ? ex_px.max_r : 0,
              ex_px.max_z > -2e9 ? ex_px.max_z : 0);
  }

  tree->Fill();
}

DEFINE_FWK_MODULE(TrackingTreer);
