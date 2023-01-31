#ifndef JMTucker_MFVNeutralinoFormats_LeptonVertexAssociation_h
#define JMTucker_MFVNeutralinoFormats_LeptonVertexAssociation_h

#include "DataFormats/Common/interface/AssociationMap.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "TrackingTools/IPTools/interface/IPTools.h"
namespace mfv {
  typedef edm::AssociationMap<edm::OneToMany<reco::VertexCollection, pat::MuonCollection> > MuonVertexAssociation;

  enum { NMuonsByUse, MByDr=NMuonsByUse, NMuonsBy };
  static const char* muonsby_name __attribute__((used)) = "MByDr";

  typedef edm::AssociationMap<edm::OneToMany<reco::VertexCollection, pat::ElectronCollection> > ElectronVertexAssociation;

  enum { NEleByUse, EByDr=NEleByUse, NEleBy };
  static const char* electronsby_name __attribute__((used)) = "EByDr";

}

#endif