#ifndef JMTucker_Tools_MCInteractionTops_h
#define JMTucker_Tools_MCInteractionTops_h

#include "JMTucker/Tools/interface/MCInteraction.h"

struct MCInteractionTops : public MCInteraction { 
  const reco::GenParticle* tops[2];  //  top,  topbar
  const reco::GenParticle* Ws[2]; // plus, minus
  const reco::GenParticle* bottoms[2]; // b, bbar
  const reco::GenParticle* W_daughters[2][2]; // first index is Wplus, Wminus, second is W daughters in order (d-type, u-type quark) or (charged lepton, neutrino)

  std::vector<const reco::Candidate*> gluons_from_tops[2];

  int num_leptonic;
  int decay_type[2]; // for Wplus and Wminus decays (the array index) into e, mu, tau, hadronic (values 0-3)

  // "Plain" momentum four-vectors.
  TLorentzVector p4_tops[2];
  TLorentzVector p4_Ws[2];
  TLorentzVector p4_bottoms[2];
  TLorentzVector p4_W_daughters[2][2];
  TLorentzVector p4_toptopbar;
  TLorentzVector p4_W_neutrinosum;

  // Convenience aliases.
  const reco::GenParticle*& top;
  const reco::GenParticle*& topbar;
  const reco::GenParticle*& Wplus;
  const reco::GenParticle*& Wminus;
  const reco::GenParticle*& bottom;
  const reco::GenParticle*& bottombar;
  const reco::GenParticle*& Wplus_dquark;
  const reco::GenParticle*& Wplus_uquark;
  const reco::GenParticle*& Wminus_dquark;
  const reco::GenParticle*& Wminus_uquark;
  const reco::GenParticle*& Wplus_charged_lepton;
  const reco::GenParticle*& Wplus_neutrino;
  const reco::GenParticle*& Wminus_charged_lepton;
  const reco::GenParticle*& Wminus_neutrino;
  TLorentzVector& p4_top;
  TLorentzVector& p4_topbar;
  TLorentzVector& p4_Wplus;
  TLorentzVector& p4_Wminus;
  TLorentzVector& p4_bottom;
  TLorentzVector& p4_bottombar;
  TLorentzVector& p4_Wplus_dquark;
  TLorentzVector& p4_Wplus_uquark;
  TLorentzVector& p4_Wminus_dquark;
  TLorentzVector& p4_Wminus_uquark;
  TLorentzVector& p4_Wplus_charged_lepton;
  TLorentzVector& p4_Wplus_neutrino;
  TLorentzVector& p4_Wminus_charged_lepton;
  TLorentzVector& p4_Wminus_neutrino;
  int& decay_plus;
  int& decay_minus;

  MCInteractionTops()
    : MCInteraction(),
      top(tops[0]),
      topbar(tops[1]),
      Wplus(Ws[0]),
      Wminus(Ws[1]),
      bottom(bottoms[0]),
      bottombar(bottoms[1]),
      Wplus_dquark(W_daughters[0][0]),
      Wplus_uquark(W_daughters[0][1]),
      Wminus_dquark(W_daughters[1][0]),
      Wminus_uquark(W_daughters[1][1]),
      Wplus_charged_lepton(W_daughters[0][0]),
      Wplus_neutrino(W_daughters[0][1]),
      Wminus_charged_lepton(W_daughters[1][0]),
      Wminus_neutrino(W_daughters[1][1]),
      p4_top(p4_tops[0]),
      p4_topbar(p4_tops[1]),
      p4_Wplus(p4_Ws[0]),
      p4_Wminus(p4_Ws[1]),
      p4_bottom(p4_bottoms[0]),
      p4_bottombar(p4_bottoms[1]),
      p4_Wplus_dquark(p4_W_daughters[0][0]),
      p4_Wplus_uquark(p4_W_daughters[0][1]),
      p4_Wminus_dquark(p4_W_daughters[1][0]),
      p4_Wminus_uquark(p4_W_daughters[1][1]),
      p4_Wplus_charged_lepton(p4_W_daughters[0][0]),
      p4_Wplus_neutrino(p4_W_daughters[0][1]),
      p4_Wminus_charged_lepton(p4_W_daughters[1][0]),
      p4_Wminus_neutrino(p4_W_daughters[1][1]),
      decay_plus(decay_type[0]),
      decay_minus(decay_type[1])
  {
  }

  virtual void Clear();
  virtual bool Valid();
  virtual void Fill();
  virtual void SetFourVectors();
  virtual void Print(std::ostream&);
};

#endif
