#include <map>
#include <vector>
#include "DataFormats/Common/interface/Association.h"
#include "DataFormats/Common/interface/AssociationMap.h"
#include "DataFormats/Common/interface/Wrapper.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/TriggerFloats.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"

namespace JMTucker_MFVNeutralinoFormats {
  struct dictionary {
    edm::AssociationMap<edm::OneToMany<std::vector<reco::Vertex>,std::vector<pat::Jet>, unsigned int > > dummyAMrVpJ;
    edm::Wrapper<edm::AssociationMap<edm::OneToMany<std::vector<reco::Vertex>,std::vector<pat::Jet>, unsigned int > > > dummyWAMrVpJ;

    edm::helpers::KeyVal<edm::Ref<std::vector<reco::Vertex>,reco::Vertex,edm::refhelper::FindUsingAdvance<std::vector<reco::Vertex>,reco::Vertex> >,edm::RefVector<std::vector<pat::Jet>,pat::Jet,edm::refhelper::FindUsingAdvance<std::vector<pat::Jet>,pat::Jet> > > dummy1;
    edm::helpers::KeyVal<edm::RefProd<std::vector<reco::Vertex> >,edm::RefProd<std::vector<pat::Jet> > > dummy2;
    std::map<unsigned int,edm::helpers::KeyVal<edm::Ref<std::vector<reco::Vertex>,reco::Vertex,edm::refhelper::FindUsingAdvance<std::vector<reco::Vertex>,reco::Vertex> >,edm::RefVector<std::vector<pat::Jet>,pat::Jet,edm::refhelper::FindUsingAdvance<std::vector<pat::Jet>,pat::Jet> > > > dummy3;
    edm::RefProd<std::vector<pat::Jet> > dummy4;

    edm::Wrapper<edm::RefVector<std::vector<reco::Vertex>,reco::Vertex,edm::refhelper::FindUsingAdvance<std::vector<reco::Vertex>,reco::Vertex> > > wvrv;

    edm::Wrapper<MFVEvent> we;
    edm::Wrapper<std::vector<MFVVertexAux> > wvva;

    edm::Wrapper<mfv::TriggerFloats> wtf;
  };
}
