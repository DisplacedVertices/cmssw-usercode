#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectronFwd.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"
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
  const edm::EDGetTokenT<reco::TrackCollection> mu_tracks_token;
  const edm::EDGetTokenT<reco::TrackCollection> ele_tracks_token;
  const bool add_separated_leptons;
  const int which;

  jmt::TrackRescaler rescaler;
};

JMTRescaledTracks::JMTRescaledTracks(const edm::ParameterSet& cfg) 
  : tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("tracks_src"))),
    mu_tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("muons_src"))),
    ele_tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("electrons_src"))),
    add_separated_leptons(cfg.getParameter<bool>("add_separated_leptons")),
    which(cfg.getParameter<int>("which"))
{
  if (which < -1 || which >= jmt::TrackRescaler::w_max) throw cms::Exception("Configuration", "bad which ") << which;

  produces<reco::TrackCollection>();
  produces<reco::TrackCollection>("electrons");
  produces<reco::TrackCollection>("muons");
  produces<jmt::TracksMap>();
  produces<jmt::TracksMap>("elemap");
  produces<jmt::TracksMap>("mumap");
}

void JMTRescaledTracks::produce(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<reco::TrackCollection> tracks;
  event.getByToken(tracks_token, tracks);

  edm::Handle<reco::TrackCollection> ele_tracks;
  event.getByToken(ele_tracks_token, ele_tracks);

  edm::Handle<reco::TrackCollection> mu_tracks;
  event.getByToken(mu_tracks_token, mu_tracks);

  auto output_tracks = std::make_unique<reco::TrackCollection>();
  auto output_tracks_map = std::make_unique<jmt::TracksMap>();

  auto output_ele_tracks = std::make_unique<reco::TrackCollection>();
  auto output_ele_tracks_map = std::make_unique<jmt::TracksMap>();
  auto output_mu_tracks = std::make_unique<reco::TrackCollection>();
  auto output_mu_tracks_map = std::make_unique<jmt::TracksMap>();

  

  reco::TrackRefProd h_output_tracks = event.getRefBeforePut<reco::TrackCollection>();
  reco::TrackRefProd h_output_mu_tracks = event.getRefBeforePut<reco::TrackCollection>();
  reco::TrackRefProd h_output_ele_tracks = event.getRefBeforePut<reco::TrackCollection>();

  rescaler.setup(!event.isRealData() && which != -1,
                 jmt::AnalysisEras::pick(event, this),
                 which);

  for (size_t i = 0, ie = tracks->size(); i < ie; ++i) {
    reco::TrackRef tk(tracks, i);
    output_tracks->push_back(rescaler.scale(*tk).rescaled_tk);
    output_tracks_map->insert(tk, reco::TrackRef(h_output_tracks, output_tracks->size() - 1));
  }

  event.put(std::move(output_tracks));
  event.put(std::move(output_tracks_map));


  if (add_separated_leptons) {

    //rescaled will need to be changed slightly in the future
    for (size_t i = 0, ie = mu_tracks->size(); i < ie; ++i) {
      reco::TrackRef mtk(mu_tracks, i);
      output_mu_tracks->push_back(rescaler.scale(*mtk).rescaled_tk);
      output_mu_tracks_map->insert(mtk, reco::TrackRef(h_output_mu_tracks, output_mu_tracks->size() - 1));
    }

    for (size_t i = 0, ie = ele_tracks->size(); i < ie; ++i) {
      reco::TrackRef etk(ele_tracks, i);
      output_ele_tracks->push_back(rescaler.scale(*etk).rescaled_tk);
      output_ele_tracks_map->insert(etk, reco::TrackRef(h_output_ele_tracks, output_ele_tracks->size() - 1));
    }

    event.put(std::move(output_mu_tracks), "muons");
    event.put(std::move(output_mu_tracks_map), "mumap");
    event.put(std::move(output_ele_tracks), "electrons");
    event.put(std::move(output_ele_tracks_map), "elemap");
  }

}

DEFINE_FWK_MODULE(JMTRescaledTracks);
