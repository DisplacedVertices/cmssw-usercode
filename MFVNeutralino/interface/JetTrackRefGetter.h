#ifndef JMTucker_MFVNeutralino_JetTrackRefGetter_h
#define JMTucker_MFVNeutralino_JetTrackRefGetter_h

#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"

namespace pat {
  class Jet;
}

namespace mfv {
  class UnpackedCandidateTracksMap;

  class JetTrackRefGetter {
  private:
    const bool input_is_miniaod;
    const edm::EDGetTokenT<mfv::UnpackedCandidateTracksMap> unpacked_candidate_tracks_map_token;
    const bool verbose;
    const std::string module_label;

    edm::Event::CacheIdentifier_t last_cacheIdentifier;
    edm::Handle<mfv::UnpackedCandidateTracksMap> unpacked_candidate_tracks_map;

    void setup_event(const edm::Event&);

  public:
    JetTrackRefGetter(const edm::ParameterSet&, edm::ConsumesCollector&&);
    std::vector<reco::TrackRef> tracks(const edm::Event&, const pat::Jet&);
  };
}

#endif
