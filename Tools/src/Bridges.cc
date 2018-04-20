#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "JMTucker/Tools/interface/Year.h"

namespace jmt {
  bool hasValidHitInFirstPixelBarrel(const reco::Track& tk) {
#if defined(MFVNEUTRALINO_2017)
    return tk.hitPattern().hasValidHitInPixelLayer(PixelSubdetector::PixelBarrel,1);
#else
    return tk.hitPattern().hasValidHitInFirstPixelBarrel();
#endif
  }

  int numberOfAllHits(const reco::HitPattern& hp, const reco::HitPattern::HitCategory category) {
#if defined(MFVNEUTRALINO_2017)
    return hp.numberOfAllHits(category);
#else
    return hp.numberOfHits(category);
#endif
  }

  bool packedCandidateHasTrackDetails(const pat::PackedCandidate& cand) {
#if defined(MFVNEUTRALINO_2017)
    return cand.charge() && cand.hasTrackDetails(); //cand.charge() && cand.pt() > 0.5 && fabs(cand.eta()) < 2.5;
#else
    return cand.charge(); // JMTBAD why didn't we need to do the rest of the above with 2016 miniaod packed candidates?
#endif
  }
}
