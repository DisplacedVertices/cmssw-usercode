#include <map>
#include <vector>
#include "DataFormats/Common/interface/Association.h"
#include "DataFormats/Common/interface/Wrapper.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "JMTucker/MFVNeutralino/interface/LightTrackMatch.h"

namespace {
  namespace {
    edm::Wrapper<LightTrackMatch> ltm;
    std::map<int, LightTrackMatch> dummymiltm;
    edm::Wrapper<std::map<int, LightTrackMatch> > dummyWmiltm;

    std::vector<reco::Vertex> vrv;
    edm::Association<std::vector<reco::Vertex> > dummyAvV;
    edm::Wrapper<edm::Association<std::vector<reco::Vertex> > > dummyWAvV;
  }
}
