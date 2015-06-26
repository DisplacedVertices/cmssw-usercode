#ifndef JMTucker_Tools_MCInteraction_h
#define JMTucker_Tools_MCInteraction_h

#include "TLorentzVector.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

struct MCInteraction {
  const reco::GenParticleCollection* gen_particles;

  enum Generator { pythia6, pythia8 };
  Generator generator;

  MCInteraction(Generator=pythia6);

  bool FromHardInteraction(const reco::Candidate*) const;

  virtual void Init(const reco::GenParticleCollection&);

  virtual void Clear() { gen_particles = 0; }
  virtual bool Valid() { return true; }
  virtual void Fill() {}
  virtual void SetFourVectors() {}
  virtual void Print(std::ostream&) {}
};

#endif
