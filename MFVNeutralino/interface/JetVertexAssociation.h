#ifndef JMTucker_MFVNeutralino_JetVertexAssociation_h
#define JMTucker_MFVNeutralino_JetVertexAssociation_h

#include "DataFormats/Common/interface/AssociationMap.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
 
struct MFVJetVertexAssociation {
  typedef edm::AssociationMap<edm::OneToMany<reco::VertexCollection, pat::JetCollection> > type;

  enum { ByNtracks, ByCombination, NByUse, ByNtracksPtmin=NByUse, ByMissDist, ByCombinationPtmin, NBy }; // JMTBAD keep in sync with mfv::Momenta
  static const char* names[NBy];
};

#endif
