#ifndef JMTucker_Tools_NtupleTrackRescaler_h
#define JMTucker_Tools_NtupleTrackRescaler_h

#define JMT_STANDALONE
#include "JMTucker/Tools/interface/AnalysisEras.h"
#include "JMTucker/Tools/interface/TrackRescaler.h"

namespace jmt {
  class RescaledTracksSubNtupleView : public TracksSubNtuple {
  public:
    RescaledTracksSubNtupleView(TracksSubNtuple& t) : TracksSubNtuple(t) {}
    void setup(const BaseSubNtuple& b, int which=TrackRescaler::w_JetHT) { rescaler_.setup(b.is_mc(), AnalysisEras::pick(b.event()), which); }
    void scaling(bool enable) { rescaler_.enable(enable); }

    float cov_33(int i) const { set(i); return rescaler_.scales().dxycov   (TracksSubNtuple::cov_33(i)); }
    float cov_34(int i) const { set(i); return rescaler_.scales().dxydszcov(TracksSubNtuple::cov_34(i)); }
    float cov_44(int i) const { set(i); return rescaler_.scales().dszcov   (TracksSubNtuple::cov_44(i)); }

  private:
    mutable TrackRescaler rescaler_;
    void set(int i) const { rescaler_.set(pt(i), eta(i)); }
  };
}

#endif
