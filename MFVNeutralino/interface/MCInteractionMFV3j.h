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

  const reco::GenParticle* last_tops[2];
  const reco::GenParticle* last_Ws[2];

  int num_leptonic; // 0, 1, or 2 for hadronic, semileptonic, dileptonic ttbar decay
  int decay_type[2]; // for Wplus and Wminus decays (the array index) into e, mu, tau, hadronic (values 0-3)
  int which_is_lepton; // which W daughter is the leptonic decay; only has meaning for num_leptonic = 1

  // "Plain" momentum four-vectors.
  TLorentzVector p4_lsps[2];
  char dummy1;
  TLorentzVector p4_stranges[2];
  char dummy2;
  TLorentzVector p4_bottoms[2];
  char dummy3;
  TLorentzVector p4_tops[2];
  char dummy4;
  TLorentzVector p4_Ws[2];
  char dummy5;
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

  std::vector<const reco::GenParticle*> ElsOrMus();
  bool is_bottom_from_top(int which);
  const reco::Candidate* Ancestor(const reco::Candidate* c, const std::string& type);

  double dvv() const;
};

#endif
