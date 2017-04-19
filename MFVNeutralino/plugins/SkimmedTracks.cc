#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"

class MFVSkimmedTracks : public edm::EDProducer {
public:
  explicit MFVSkimmedTracks(const edm::ParameterSet&);
private:
  virtual void produce(edm::Event&, const edm::EventSetup&);
  const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
};

MFVSkimmedTracks::MFVSkimmedTracks(const edm::ParameterSet& cfg)
  : tracks_token(consumes<reco::TrackCollection>(edm::InputTag("generalTracks")))
{
  produces<reco::TrackCollection>();
}

void MFVSkimmedTracks::produce(edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<reco::TrackCollection> tracks;
  event.getByToken(tracks_token, tracks);
  
  std::auto_ptr<reco::TrackCollection> output_tracks(new reco::TrackCollection);

  for (const reco::Track& tk : *tracks) {
    const double pt = tk.pt();
    const int npxlayers = tk.hitPattern().pixelLayersWithMeasurement();
    const int nstlayers = tk.hitPattern().stripLayersWithMeasurement();
    const bool min_r = tk.hitPattern().hasValidHitInFirstPixelBarrel();
    if (pt > 1. && min_r && npxlayers >= 2 && nstlayers >= 3)
      output_tracks->push_back(tk);
  }

  event.put(output_tracks);
}

DEFINE_FWK_MODULE(MFVSkimmedTracks);
