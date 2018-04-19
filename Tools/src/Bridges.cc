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

}
