#ifndef JMTucker_MFVNeutralino_JetTrackRefGetter_h
#define JMTucker_MFVNeutralino_JetTrackRefGetter_h

#include "FWCore/Framework/interface/ConsumesCollector.h"

namespace mfv {
  class JetTrackRefGetter {
  private:
    const bool input_is_miniaod;
    const edm::EDGetTokenT<reco::TrackCollection> unpacked_tracks_token;
    const edm::EDGetTokenT<std::vector<size_t>> unpacking_map_token;

    edm::Event::CacheIdentifier_t last_cacheIdentifier;
    edm::Handle<reco::TrackCollection> unpacked_tracks;
    edm::Handle<std::vector<size_t>> unpacking_map;
    std::map<size_t, size_t> inverse_unpacking_map;

    void setup_event(const edm::Event& event) {
      if (!input_is_miniaod)
        return;

      if (event.cacheIdentifier() == last_cacheIdentifier)
        return;

      last_cacheIdentifier = event.cacheIdentifier();
      event.getByToken(unpacked_tracks_token, unpacked_tracks);
      event.getByToken(unpacking_map_token, unpacking_map);
      inverse_unpacking_map.clear();
      for (size_t itrk = 0, itrke = unpacking_map->size(); itrk < itrke; ++itrk) {
        const size_t ipack = (*unpacking_map)[itrk];
        inverse_unpacking_map[ipack] = itrk;
      }
    }

  public:
    JetTrackRefGetter(const edm::ParameterSet& cfg, edm::ConsumesCollector&& cc)
      : input_is_miniaod(cfg.getParameter<bool>("input_is_miniaod")),
        unpacked_tracks_token(cc.consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("unpacked_tracks_src"))),
        unpacking_map_token(cc.consumes<std::vector<size_t>>(cfg.getParameter<edm::InputTag>("unpacking_map_src"))),
        last_cacheIdentifier(0)
    {
    }

    std::vector<reco::TrackRef> tracks(const edm::Event& event, const pat::Jet& jet) {
      setup_event(event);

      std::vector<reco::TrackRef> r;

      if (input_is_miniaod) {
        for (const reco::CandidatePtr& p : jet.daughterPtrVector()) {
          const size_t ipack = p.key();
          auto it = inverse_unpacking_map.find(ipack);
          if (it != inverse_unpacking_map.end())
            r.push_back(reco::TrackRef(unpacked_tracks, it->second));
        }
      }
      else {
        for (const reco::PFCandidatePtr& pfcand : jet.getPFConstituents()) {
          const reco::TrackRef& tk = pfcand->trackRef();
          if (tk.isNonnull())
            r.push_back(tk);
        }
      }

      return r;
    }
  };
}

#endif
