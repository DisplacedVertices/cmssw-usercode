#ifndef JMTucker_Tools_Bridges_h
#define JMTucker_Tools_Bridges_h

#include "DataFormats/TrackReco/interface/TrackFwd.h"

namespace jmt {
  bool hasValidHitInFirstPixelBarrel(const reco::Track& tk);
}

#endif
