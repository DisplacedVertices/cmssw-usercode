#ifndef JMTucker_Tools_MCInteractionXX4j_h
#define JMTucker_Tools_MCInteractionXX4j_h

#include "JMTucker/Tools/interface/MCInteraction.h"

struct MCInteractionXX4j : public MCInteraction { 
  const reco::GenParticle* hs[2]; // a then h
  const reco::GenParticle* qs[2][2]; // [a then h][q then qbar]
  int decay_id[2]; // must be 1-5

  // "Plain" momentum four-vectors.
  TLorentzVector p4_hs[2];
  char dummy2;
  TLorentzVector p4_qs[2][2];

  MCInteractionXX4j()
    : MCInteraction(MCInteraction::pythia8)
  {
    Clear();
  }

  virtual void Clear();
  virtual bool Valid();
  virtual void Fill();
  virtual void SetFourVectors();
  virtual void Print(std::ostream&);
};

#endif
