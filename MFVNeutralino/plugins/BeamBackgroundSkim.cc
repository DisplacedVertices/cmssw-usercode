#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"

class BeamBackgroundSkim : public edm::EDFilter {
public:
  explicit BeamBackgroundSkim(const edm::ParameterSet&);

private:
  virtual bool filter(edm::Event&, const edm::EventSetup&);

  const edm::InputTag beamspot_src;
  const edm::InputTag tracks_src;
  const double min_pt;
  const double min_dxy;
};

BeamBackgroundSkim::BeamBackgroundSkim(const edm::ParameterSet& cfg) 
  : beamspot_src(cfg.getParameter<edm::InputTag>("beamspot_src")),
    tracks_src(cfg.getParameter<edm::InputTag>("tracks_src")),
    min_pt(cfg.getParameter<double>("min_pt")),
    min_dxy(cfg.getParameter<double>("min_dxy"))
{
}

bool BeamBackgroundSkim::filter(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<reco::BeamSpot> beamspot;
  event.getByLabel(beamspot_src, beamspot);

  edm::Handle<reco::TrackCollection> tracks;
  event.getByLabel(tracks_src, tracks);

  for (const reco::Track& track : *tracks)
    if (track.pt() > min_pt && track.dxy(*beamspot) > min_dxy)
      return true;

  return false;
}

DEFINE_FWK_MODULE(BeamBackgroundSkim);
