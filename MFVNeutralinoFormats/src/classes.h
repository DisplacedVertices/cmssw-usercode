#include <map>
#include <vector>
#include "DataFormats/Common/interface/Association.h"
#include "DataFormats/Common/interface/AssociationMap.h"
#include "DataFormats/Common/interface/Wrapper.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/MCInteractions.h"
#include "JMTucker/MFVNeutralinoFormats/interface/TriggerFloats.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexerPairEff.h"

namespace JMTucker_MFVNeutralinoFormats {
  struct dictionary {
    edm::AssociationMap<edm::OneToMany<std::vector<reco::Vertex>,std::vector<pat::Jet>, unsigned int > > dummyAMrVpJ;
    edm::Wrapper<edm::AssociationMap<edm::OneToMany<std::vector<reco::Vertex>,std::vector<pat::Jet>, unsigned int > > > dummyWAMrVpJ;

    edm::AssociationMap<edm::OneToMany<std::vector<reco::Vertex>,std::vector<pat::Electron>,unsigned int> > dummyAMrVpE;
    edm::Wrapper<edm::AssociationMap<edm::OneToMany<std::vector<reco::Vertex>,std::vector<pat::Electron>,unsigned int> > > dummyWAMrVpE;

    edm::AssociationMap<edm::OneToMany<std::vector<reco::Vertex>,std::vector<pat::Muon>,unsigned int> > dummyAMrVpM;
    edm::Wrapper<edm::AssociationMap<edm::OneToMany<std::vector<reco::Vertex>,std::vector<pat::Muon>,unsigned int> > > dummyWAMrVpM;

    edm::helpers::KeyVal<edm::Ref<std::vector<reco::Vertex>,reco::Vertex,edm::refhelper::FindUsingAdvance<std::vector<reco::Vertex>,reco::Vertex> >,edm::RefVector<std::vector<pat::Jet>,pat::Jet,edm::refhelper::FindUsingAdvance<std::vector<pat::Jet>,pat::Jet> > > dummy1;
    edm::helpers::KeyVal<edm::RefProd<std::vector<reco::Vertex> >,edm::RefProd<std::vector<pat::Jet> > > dummy2;
    std::map<unsigned int,edm::helpers::KeyVal<edm::Ref<std::vector<reco::Vertex>,reco::Vertex,edm::refhelper::FindUsingAdvance<std::vector<reco::Vertex>,reco::Vertex> >,edm::RefVector<std::vector<pat::Jet>,pat::Jet,edm::refhelper::FindUsingAdvance<std::vector<pat::Jet>,pat::Jet> > > > dummy3;
    edm::RefProd<std::vector<pat::Jet> > dummy4;

    edm::helpers::KeyVal<edm::RefProd<vector<reco::Vertex> >,edm::RefProd<vector<pat::Electron> > > dummye2;
    edm::RefProd<vector<pat::Electron> > dummye4;

    edm::helpers::KeyVal<edm::RefProd<vector<reco::Vertex> >,edm::RefProd<vector<pat::Muon> > > dummym2;
    edm::RefProd<vector<pat::Muon> > dummym4;

    edm::Wrapper<edm::RefVector<std::vector<reco::Vertex>,reco::Vertex,edm::refhelper::FindUsingAdvance<std::vector<reco::Vertex>,reco::Vertex> > > wvrv;

    std::vector<TLorentzVector> vtlv;
    edm::Wrapper<std::vector<TLorentzVector> > wvtlv;

    edm::Wrapper<MFVEvent> we;
    edm::Wrapper<std::vector<MFVVertexAux> > wvva;

    edm::Wrapper<mfv::MCInteraction> wmci;
    edm::Wrapper<mfv::TriggerFloats> wtf;
    edm::Wrapper<std::vector<VertexerPairEff> > wvvpe;

    edm::Wrapper<std::vector<edm::Ref<std::vector<reco::Track>,reco::Track,edm::refhelper::FindUsingAdvance<std::vector<reco::Track>,reco::Track> > > > wvtr;
  };
}
