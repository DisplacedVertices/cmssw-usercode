#ifndef JMTucker_Tools_TrackTools_h
#define JMTucker_Tools_TrackTools_h

namespace reco {
  class BeamSpot;
  class Track;
}

namespace jmt {
  bool pass_track(const reco::Track&, const int level, const reco::BeamSpot* =0);
}

#endif
