#ifndef JMTucker_Tools_MCInteractionLQ_h
#define JMTucker_Tools_MCInteractionLQ_h

#include "JMTucker/Tools/interface/MCInteraction.h"

struct MCInteractionLQ : public MCInteraction { 
  const reco::GenParticle* lqs[2]; // lq then lqbar
  const reco::GenParticle* daus[2][2]; // [lq then lqbar][q then l]
  int decay_id[2]; // generation 1-3

  // "Plain" momentum four-vectors.
  TLorentzVector p4_lqs[2];
  char dummy2;
  TLorentzVector p4_daus[2][2];

  MCInteractionLQ()
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
