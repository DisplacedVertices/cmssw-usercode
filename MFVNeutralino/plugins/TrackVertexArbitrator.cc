#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "RecoVertex/AdaptiveVertexFit/interface/AdaptiveVertexFitter.h"
#include "RecoVertex/ConfigurableVertexReco/interface/ConfigurableVertexReconstructor.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexUpdator.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexTrackCompatibilityEstimator.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexSmoother.h"
#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "TrackingTools/IPTools/interface/IPTools.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"

#include "JMTucker/MFVNeutralino/plugins/TrackVertexArbitratration.h"

class MFVTrackVertexArbitrator : public edm::EDProducer {
public:
  MFVTrackVertexArbitrator(const edm::ParameterSet&);
  ~MFVTrackVertexArbitrator();

  virtual void produce(edm::Event&, const edm::EventSetup&);

private:
  bool trackFilter(const reco::TrackRef&) const;

  edm::InputTag primaryVertexCollection;
  edm::InputTag secondaryVertexCollection;
  edm::InputTag trackCollection;
  edm::InputTag beamSpotCollection;
  MFVTrackVertexArbitration* theArbitrator;
};

MFVTrackVertexArbitrator::MFVTrackVertexArbitrator(const edm::ParameterSet& cfg)
  : primaryVertexCollection  (cfg.getParameter<edm::InputTag>("primaryVertices")),
    secondaryVertexCollection(cfg.getParameter<edm::InputTag>("secondaryVertices")),
    trackCollection          (cfg.getParameter<edm::InputTag>("tracks")),
    beamSpotCollection       (cfg.getParameter<edm::InputTag>("beamSpot"))
{
  produces<reco::VertexCollection>();
  theArbitrator = new MFVTrackVertexArbitration(cfg);
}

MFVTrackVertexArbitrator::~MFVTrackVertexArbitrator() {
  delete theArbitrator;
}

void MFVTrackVertexArbitrator::produce(edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<reco::VertexCollection> primaryVertices;
  event.getByLabel(primaryVertexCollection, primaryVertices);

  std::auto_ptr<reco::VertexCollection> recoVertices(new reco::VertexCollection);

  if (primaryVertices->size() > 0) {
    const reco::Vertex &pv = primaryVertices->at(0);

    edm::Handle<reco::BeamSpot> beamSpot;
    event.getByLabel(beamSpotCollection, beamSpot);

    edm::Handle<reco::TrackCollection> tracks;
    event.getByLabel(trackCollection, tracks);

    edm::Handle<reco::VertexCollection> secondaryVertices;
    event.getByLabel(secondaryVertexCollection, secondaryVertices);
    
    edm::ESHandle<TransientTrackBuilder> trackBuilder;
    setup.get<TransientTrackRecord>().get("TransientTrackBuilder", trackBuilder);

    reco::TrackRefVector selectedTracks;
    for (size_t i = 0, ie = tracks->size(); i < ie; ++i)
      selectedTracks.push_back(reco::TrackRef(tracks, i));
    
    reco::VertexCollection theRecoVertices = theArbitrator->trackVertexArbitrator(beamSpot, pv, trackBuilder, selectedTracks, *secondaryVertices);
    for (const reco::Vertex& v : theRecoVertices)
      recoVertices->push_back(v);
  }	

  event.put(recoVertices);
}

DEFINE_FWK_MODULE(MFVTrackVertexArbitrator);
