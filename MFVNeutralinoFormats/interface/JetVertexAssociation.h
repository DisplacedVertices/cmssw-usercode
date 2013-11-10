#ifndef JMTucker_MFVNeutralinoFormats_JetVertexAssociation_h
#define JMTucker_MFVNeutralinoFormats_JetVertexAssociation_h

#include "DataFormats/Common/interface/AssociationMap.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
 
namespace mfv {
  typedef edm::AssociationMap<edm::OneToMany<reco::VertexCollection, pat::JetCollection> > JetVertexAssociation;

  enum { JByNtracks, JByCombination, NJetsByUse, JByNtracksPtmin=NJetsByUse, JByMissDist, JByCombinationPtmin, NJetsBy };
  static const char* jetsby_names[NJetsBy] =
    { "ByNtracks", "ByCombination", "ByNtracksPtmin", "ByMissDist", "ByCombinationPtmin" };

  enum { PTracksOnly, PJetsByNtracks, PJetsByCombination, PTracksPlusJetsByNtracks, PTracksPlusJetsByCombination, NMomenta }; // JMTBAD keep in sync
}

#endif
