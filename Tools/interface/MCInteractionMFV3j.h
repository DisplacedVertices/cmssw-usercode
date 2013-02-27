#ifndef JMTucker_Tools_MCInteractionMFV3j_h
#define JMTucker_Tools_MCInteractionMFV3j_h

#include "JMTucker/Tools/interface/MCInteraction.h"

struct MCInteractionMFV3j : public MCInteraction { 
  const reco::GenParticle* lsps[2];
  const reco::GenParticle* stranges[2];
  const reco::GenParticle* bottoms[2];
  const reco::GenParticle* tops[2];
  const reco::GenParticle* Ws[2];
  const reco::GenParticle* bottoms_from_tops[2];
  const reco::GenParticle* W_daughters[2][2]; // first index is same as above, second is W daughters in order (d-type, u-type quark) or (charged lepton, neutrino)

  int num_leptonic;
  int decay_type[2]; // for Wplus and Wminus decays (the array index) into e, mu, tau, hadronic (values 0-3)

  // "Plain" momentum four-vectors.
  TLorentzVector p4_lsps[2];
  TLorentzVector p4_stranges[2];
  TLorentzVector p4_bottoms[2];
  TLorentzVector p4_tops[2];
  TLorentzVector p4_Ws[2];
  TLorentzVector p4_bottoms_from_tops[2];
  TLorentzVector p4_W_daughters[2][2];
  TLorentzVector p4_W_neutrinosum;

  MCInteractionMFV3j()
    : MCInteraction(MCInteraction::pythia8)
  {
    Clear();
  }

  virtual void Clear();
  virtual bool Valid();
  virtual void Fill();
  virtual void SetFourVectors();
  virtual void Print(std::ostream&);

  const reco::Candidate* Ancestor(const reco::Candidate* c, const std::string& type);
};

#endif
