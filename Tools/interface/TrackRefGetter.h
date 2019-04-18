#ifndef JMTucker_Tools_TrackRefGetter_h
#define JMTucker_Tools_TrackRefGetter_h

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "JMTucker/Formats/interface/TracksMap.h"

namespace jmt {
  class TrackRefGetter {
  private:
    const bool input_is_miniaod;
    const edm::EDGetTokenT<jmt::UnpackedCandidateTracksMap> unpacked_candidate_tracks_map_token;
    std::vector<edm::EDGetTokenT<jmt::TracksMap>> tracks_maps_tokens;
    const bool verbose;
    const std::string module_label;

    edm::Event::CacheIdentifier_t last_cacheIdentifier;
    edm::Handle<jmt::UnpackedCandidateTracksMap> unpacked_candidate_tracks_map;
    std::vector<edm::Handle<jmt::TracksMap>> tracks_maps;

    void setup_event(const edm::Event&);

  public:
    TrackRefGetter(const std::string& label, const edm::ParameterSet&, edm::ConsumesCollector&&);
    std::vector<reco::TrackRef> tracks(const edm::Event&, const pat::Jet&);
    std::vector<std::pair<reco::TrackRef,int>> tracks(const edm::Event&, const reco::VertexRef&);

    bool has_track(const edm::Event&, const pat::Jet&, const reco::TrackRef&);
    int  has_track(const edm::Event&, const reco::VertexRef&, const reco::TrackRef&);
  };
}

#endif
