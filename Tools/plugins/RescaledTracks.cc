#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "JMTucker/Formats/interface/TracksMap.h"
#include "JMTucker/Tools/interface/AnalysisEras.h"
#include "JMTucker/Tools/interface/TrackRescaler.h"

class JMTRescaledTracks : public edm::EDProducer {
public:
  explicit JMTRescaledTracks(const edm::ParameterSet&);

private:
  virtual void produce(edm::Event&, const edm::EventSetup&) override;

  const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
  const int which;

  jmt::TrackRescaler rescaler;
};

JMTRescaledTracks::JMTRescaledTracks(const edm::ParameterSet& cfg) 
  : tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("tracks_src"))),
    which(cfg.getParameter<int>("which"))
{
  if (which < -1 || which >= jmt::TrackRescaler::w_max) throw cms::Exception("Configuration", "bad which ") << which;

  produces<reco::TrackCollection>();
  produces<jmt::TracksMap>();
}

void JMTRescaledTracks::produce(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<reco::TrackCollection> tracks;
  event.getByToken(tracks_token, tracks);

  auto output_tracks = std::make_unique<reco::TrackCollection>();
  auto output_tracks_map = std::make_unique<jmt::TracksMap>();

  reco::TrackRefProd h_output_tracks = event.getRefBeforePut<reco::TrackCollection>();
  rescaler.setup(!event.isRealData() && which != -1,
                 jmt::AnalysisEras::pick(event.id().event()),
                 //jmt::AnalysisEras::pick(event, this),
                 which);

  for (size_t i = 0, ie = tracks->size(); i < ie; ++i) {
    reco::TrackRef tk(tracks, i);
    output_tracks->push_back(rescaler.scale(*tk).rescaled_tk);
    output_tracks_map->insert(tk, reco::TrackRef(h_output_tracks, output_tracks->size() - 1));
  }

  event.put(std::move(output_tracks));
  event.put(std::move(output_tracks_map));
}

DEFINE_FWK_MODULE(JMTRescaledTracks);
