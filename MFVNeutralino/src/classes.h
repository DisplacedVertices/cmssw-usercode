#include <map>
#include <vector>
#include "DataFormats/Common/interface/Association.h"
#include "DataFormats/Common/interface/AssociationMap.h"
#include "DataFormats/Common/interface/Wrapper.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "JMTucker/MFVNeutralino/interface/LightTrackMatch.h"
#include "JMTucker/MFVNeutralino/interface/Event.h"
#include "JMTucker/MFVNeutralino/interface/VertexAux.h"

namespace {
  namespace {
    edm::Wrapper<LightTrackMatch> ltm;
    std::map<int, LightTrackMatch> dummymiltm;
    edm::Wrapper<std::map<int, LightTrackMatch> > dummyWmiltm;

    edm::Association<std::vector<reco::Vertex> > dummyAvV;
    edm::Wrapper<edm::Association<std::vector<reco::Vertex> > > dummyWAvV;

    edm::AssociationMap<edm::OneToMany<std::vector<reco::Vertex>,std::vector<pat::Jet>, unsigned int > > dummyAMrVpJ;
    edm::Wrapper<edm::AssociationMap<edm::OneToMany<std::vector<reco::Vertex>,std::vector<pat::Jet>, unsigned int > > > dummyWAMrVpJ;

    edm::Wrapper<edm::RefVector<std::vector<reco::Vertex>,reco::Vertex,edm::refhelper::FindUsingAdvance<std::vector<reco::Vertex>,reco::Vertex> > > wvrv;

    edm::Wrapper<MFVEvent> we;
    edm::Wrapper<std::vector<MFVVertexAux> > wvva;
  }
}
