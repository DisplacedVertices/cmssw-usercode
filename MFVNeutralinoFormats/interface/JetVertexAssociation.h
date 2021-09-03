#ifndef DVCode_MFVNeutralinoFormats_JetVertexAssociation_h
#define DVCode_MFVNeutralinoFormats_JetVertexAssociation_h

#include "DataFormats/Common/interface/AssociationMap.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
 
namespace mfv {
  typedef edm::AssociationMap<edm::OneToMany<reco::VertexCollection, pat::JetCollection> > JetVertexAssociation;

  enum { JByNtracks, NJetsByUse, JByNtracksPtmin=NJetsByUse, JByMissDist, JByCombination, JByCombinationPtmin, NJetsBy };
  static const char* jetsby_names[NJetsBy] __attribute__((used)) =
    { "ByNtracks", "ByNtracksPtmin", "ByMissDist", "ByCombination", "ByCombinationPtmin" };

  enum { PTracksOnly, PJetsByNtracks, PTracksPlusJetsByNtracks, NMomenta }; // JMTBAD keep in sync
}

#endif
