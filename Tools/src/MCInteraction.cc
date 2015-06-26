#include "JMTucker/Tools/interface/MCInteraction.h"
#include "JMTucker/Tools/interface/GenUtilities.h"
#include "JMTucker/Tools/interface/Utilities.h"

MCInteraction::MCInteraction(MCInteraction::Generator g)
  : generator(g)
{
  Clear();
}

bool MCInteraction::FromHardInteraction(const reco::Candidate* p) const {
  switch (generator) {
  case pythia6: return p->status() == 3;
  case pythia8: return p->status() >= 21 && p->status() <= 29;
  default: return false;
  }
}

void MCInteraction::Init(const reco::GenParticleCollection& gen_particles_) {
  Clear();
  
  gen_particles = &gen_particles_;
  
  Fill();
  if (!Valid())
    return;
  
  SetFourVectors();
}
