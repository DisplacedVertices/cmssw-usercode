#include "TH2.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/TrackerSpaceExtent.h"

class CheckMinRCalc : public edm::EDAnalyzer {
 public:
  explicit CheckMinRCalc(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);
 private:
  const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
  const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
  TrackerSpaceExtents tracker_extents;
  TH2D* ok;
};

CheckMinRCalc::CheckMinRCalc(const edm::ParameterSet&)
  : beamspot_token(consumes<reco::BeamSpot>(edm::InputTag("offlineBeamSpot"))),
    tracks_token(consumes<reco::TrackCollection>(edm::InputTag("generalTracks")))
{
  edm::Service<TFileService> fs;
  ok = fs->make<TH2D>("ok", "", 2, 0, 2, 2, 0, 2);
}

void CheckMinRCalc::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<reco::BeamSpot> beamspot;
  event.getByToken(beamspot_token, beamspot);
  const double bs_x = beamspot->position().x();
  const double bs_y = beamspot->position().y();
  const double bs_z = beamspot->position().z();
  
  if (!tracker_extents.filled())
    tracker_extents.fill(setup, GlobalPoint(bs_x, bs_y, bs_z));

  edm::Handle<reco::TrackCollection> tracks;
  event.getByToken(tracks_token, tracks);
  for (const reco::Track& tk : *tracks) {
    NumExtents ne = tracker_extents.numExtentInRAndZ(tk.hitPattern(), false);
    ok->Fill(ne.min_r == 1, tk.hitPattern().hasValidHitInFirstPixelBarrel());
  }
}

DEFINE_FWK_MODULE(CheckMinRCalc);
