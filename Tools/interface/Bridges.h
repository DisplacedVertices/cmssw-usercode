#ifndef JMTucker_Tools_Bridges_h
#define JMTucker_Tools_Bridges_h

namespace pat { class PackedCandidate; }
#include "DataFormats/TrackReco/interface/TrackFwd.h"

namespace jmt {
  bool hasValidHitInFirstPixelBarrel(const reco::Track&);
  int numberOfAllHits(const reco::HitPattern&, const reco::HitPattern::HitCategory);
  bool packedCandidateHasTrackDetails(const pat::PackedCandidate&);
}

#endif
