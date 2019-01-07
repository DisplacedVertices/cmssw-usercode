#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "JMTucker/MFVNeutralino/interface/JetTrackRefGetter.h"

namespace mfv {
  void JetTrackRefGetter::setup_event(const edm::Event& event) {
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

  JetTrackRefGetter::JetTrackRefGetter(const edm::ParameterSet& cfg, edm::ConsumesCollector&& cc)
    : input_is_miniaod(cfg.getParameter<bool>("input_is_miniaod")),
      unpacked_tracks_token(cc.consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("unpacked_tracks_src"))),
      unpacking_map_token(cc.consumes<std::vector<size_t>>(cfg.getParameter<edm::InputTag>("unpacking_map_src"))),
      verbose(cfg.getUntrackedParameter<bool>("jtrg_verbose", false)),
      module_label(cfg.getParameter<std::string>("@module_label")),
      last_cacheIdentifier(0)
  {
  }

  std::vector<reco::TrackRef> JetTrackRefGetter::tracks(const edm::Event& event, const pat::Jet& jet) {
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

    if (verbose)
      for (auto tk : r)
        printf("JetTrackRefGetter %s: jet %f,%f,%f,%f got track %f,%f,%f,%f,%f\n",
               module_label.c_str(), jet.pt(), jet.eta(), jet.phi(), jet.energy(),
               tk->charge()*tk->pt(), tk->eta(), tk->phi(), tk->dxy(), tk->dz());

    return r;
  }
}
