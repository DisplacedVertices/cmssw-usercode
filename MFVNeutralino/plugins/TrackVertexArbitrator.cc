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

class MFVTrackVertexArbitrator : public edm::EDProducer {
public:
  MFVTrackVertexArbitrator(const edm::ParameterSet&);

  virtual void produce(edm::Event&, const edm::EventSetup&);

private:
  bool trackFilter(const reco::TrackRef&) const;

  const edm::InputTag primaryVertexCollection;
  const edm::InputTag secondaryVertexCollection;
  const edm::InputTag trackCollection;
  const edm::InputTag beamSpotCollection;
  const double dRCut;
  const double distCut;
  const double sigCut;
  const double dLenFraction;

  VertexDistance3D vdist;
};

MFVTrackVertexArbitrator::MFVTrackVertexArbitrator(const edm::ParameterSet& cfg)
  : primaryVertexCollection  (cfg.getParameter<edm::InputTag>("primaryVertices")),
    secondaryVertexCollection(cfg.getParameter<edm::InputTag>("secondaryVertices")),
    trackCollection          (cfg.getParameter<edm::InputTag>("tracks")),
    beamSpotCollection       (cfg.getParameter<edm::InputTag>("beamSpot")),
    dRCut       (cfg.getParameter<double>("dRCut")),
    distCut     (cfg.getParameter<double>("distCut")),
    sigCut      (cfg.getParameter<double>("sigCut")),
    dLenFraction(cfg.getParameter<double>("dLenFraction"))
{
  produces<reco::VertexCollection>();
}

bool MFVTrackVertexArbitrator::trackFilter(const reco::TrackRef& track) const {
  return
    track->hitPattern().trackerLayersWithMeasurement() >= 4 &&
    track->hitPattern().numberOfValidPixelHits() >= 1 &&
    track->pt() > 0.4;
}

void MFVTrackVertexArbitrator::produce(edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<reco::VertexCollection> primaryVertices;
  event.getByLabel(primaryVertexCollection, primaryVertices);

  std::auto_ptr<reco::VertexCollection> recoVertices(new reco::VertexCollection);

  if (primaryVertices->size() > 0) {
    const reco::Vertex& pv = primaryVertices->at(0);

    edm::Handle<reco::BeamSpot> beamSpot;
    event.getByLabel(beamSpotCollection, beamSpot);

    edm::Handle<reco::TrackCollection> tracks;
    event.getByLabel(trackCollection, tracks);

    edm::Handle<reco::VertexCollection> secondaryVertices;
    event.getByLabel(secondaryVertexCollection, secondaryVertices);
    
    edm::ESHandle<TransientTrackBuilder> trackBuilder;
    setup.get<TransientTrackRecord>().get("TransientTrackBuilder", trackBuilder);

    const double annealing_sigmacut = 3.0;
    const double annealing_Tini     = 256.;
    const double annealing_ratio    = 0.25;
    AdaptiveVertexFitter theAdaptiveFitter(GeometricAnnealing(annealing_sigmacut, annealing_Tini, annealing_ratio),
                                           DefaultLinearizationPointFinder(),
                                           KalmanVertexUpdator<5>(),
                                           KalmanVertexTrackCompatibilityEstimator<5>(),
                                           KalmanVertexSmoother());

    reco::TrackRefVector selectedTracks;
    for (size_t i = 0, ie = tracks->size(); i < ie; ++i) {
      reco::TrackRef tk(tracks, i);
      if (trackFilter(tk))
        selectedTracks.push_back(tk);
    }
    
    for (std::vector<reco::Vertex>::const_iterator sv = secondaryVertices->begin(); sv != secondaryVertices->end(); ++sv) {
      GlobalPoint ppv(pv .position().x(), pv .position().y(), pv .position().z());
      GlobalPoint ssv(sv->position().x(), sv->position().y(), sv->position().z());
      GlobalVector flightDir = ssv - ppv;

      Measurement1D dlen = vdist.distance(pv, *sv);
      std::vector<reco::TransientTrack> selTracks;

      for (unsigned int itrack = 0; itrack < selectedTracks.size(); itrack++) {
        reco::TrackRef tkref = selectedTracks[itrack];

        reco::TransientTrack tt = trackBuilder->build(tkref);
        tt.setBeamSpot(*beamSpot);
        float w = sv->trackWeight(tkref);
        std::pair<bool,Measurement1D> ipv  = IPTools::absoluteImpactParameter3D(tt, pv);
        std::pair<bool,Measurement1D> isv  = IPTools::absoluteImpactParameter3D(tt, *sv);
        //        std::pair<bool,Measurement1D> itpv = IPTools::absoluteTransverseImpactParameter(tt, pv);
        float dR = reco::deltaR(flightDir, tt.track());

        if (w > 0 || (isv.second.significance() < sigCut && isv.second.value() < distCut && isv.second.value() < dlen.value() * dLenFraction)) {
          if (isv.second.value() < ipv.second.value() && isv.second.value() < distCut && isv.second.value() < dlen.value()*dLenFraction && dR < dRCut)
            selTracks.push_back(tt);
          // add also the tracks used in previous fitting that are still closer to Sv than Pv 
          else if (w > 0.5 && isv.second.value() <= ipv.second.value() && dR < dRCut)
            selTracks.push_back(tt);
        }
      }

      if (selTracks.size() >= 2) { 
        TransientVertex singleFitVertex = theAdaptiveFitter.vertex(selTracks,ssv);
        if (singleFitVertex.isValid())
          recoVertices->push_back(reco::Vertex(singleFitVertex));
      } 
    }
  }	

  event.put(recoVertices);
}

DEFINE_FWK_MODULE(MFVTrackVertexArbitrator);
