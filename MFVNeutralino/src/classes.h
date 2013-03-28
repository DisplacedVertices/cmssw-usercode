#include <map>
#include "DataFormats/Common/interface/Wrapper.h"
#include "JMTucker/MFVNeutralino/interface/LightTrackMatch.h"

namespace {
  namespace {
    edm::Wrapper<LightTrackMatch> ltm;
    std::map<int, LightTrackMatch> dummymiltm;
    edm::Wrapper<std::map<int, LightTrackMatch> > dummymiltmW;
  }
}
