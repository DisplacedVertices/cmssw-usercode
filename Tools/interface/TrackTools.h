#ifndef JMTucker_Tools_TrackTools_h
#define JMTucker_Tools_TrackTools_h

namespace reco {
  class BeamSpot;
  class Track;
}

namespace edm {
  class Event;
}

namespace jmt {
  // use_rescaled <0 means pass if either the plain or rescaled track passes, 0 = use plain, >0 = use rescaled
  bool pass_track(const reco::Track&, const int level, const int use_rescaled=0, const edm::Event* =0, const reco::BeamSpot* =0);
}

#endif
