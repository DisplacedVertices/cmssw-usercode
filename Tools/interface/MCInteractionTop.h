#ifndef JMTucker_Tools_MCInteractionTop_h
#define JMTucker_Tools_MCInteractionTop_h

#include "TLorentzVector.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/JetReco/interface/GenJet.h"

struct MCInteractionTop {
  bool valid() {
    return tops[0] && tops[1];
  }

  const reco::GenParticle* stops[2]; // stop, stopbar
  const reco::GenParticle* tops[2];  //  top,  topbar
  const reco::GenParticle* neutralinos[2]; // from_stop, from_stopbar
  const reco::GenParticle* Ws[2]; // plus, minus
  const reco::GenParticle* bottoms[2]; // b, bbar
  const reco::GenParticle* W_daughters[2][2]; // first index is Wplus, Wminus, second is W daughters in order (d-type, u-type quark) or (charged lepton, neutrino)

  std::vector<const reco::Candidate*> gluons_from_stops[2];
  std::vector<const reco::Candidate*> gluons_from_tops[2];

  // Decays-in-flight: neutrinos and their charged lepton partners.
  struct dif_lepton_pair {
    const reco::GenParticle* charged;
    const reco::GenParticle* neutrino;
    const reco::GenJet* closest_jet;
    const reco::GenJet* mother_jet;
    TLorentzVector p4_charged;
    TLorentzVector p4_neutrino;
    dif_lepton_pair(const reco::Candidate* chg, const reco::Candidate* nu);
  };
  std::vector<dif_lepton_pair> dif_leptons;

  int num_leptonic;
  int decay_type[2]; // for Wplus and Wminus decays (the array index) into e, mu, tau, hadronic (values 0-3)

  // "Plain" momentum four-vectors.
  TLorentzVector p4_stops[2];
  TLorentzVector p4_tops[2];
  TLorentzVector p4_neutralinos[2];
  TLorentzVector p4_Ws[2];
  TLorentzVector p4_bottoms[2];
  TLorentzVector p4_W_daughters[2][2];
  TLorentzVector p4_stopstopbar;
  TLorentzVector p4_toptopbar;
  TLorentzVector p4_neutralinosum;
  TLorentzVector p4_W_neutrinosum;
  TLorentzVector p4_dif_neutrinosum;
  TLorentzVector p4_neutrinosum;
  TLorentzVector p4_missingsum;

  // Convenience aliases.
  const reco::GenParticle*& stop;
  const reco::GenParticle*& stopbar;
  const reco::GenParticle*& top;
  const reco::GenParticle*& topbar;
  const reco::GenParticle*& neutralino_from_stop;
  const reco::GenParticle*& neutralino_from_stopbar;
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
  TLorentzVector& p4_stop;
  TLorentzVector& p4_stopbar;
  TLorentzVector& p4_top;
  TLorentzVector& p4_topbar;
  TLorentzVector& p4_neutralino_from_stop;
  TLorentzVector& p4_neutralino_from_stopbar;
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

  MCInteractionTop() :
    stop(stops[0]),
    stopbar(stops[1]),
    top(tops[0]),
    topbar(tops[1]),
    neutralino_from_stop(neutralinos[0]),
    neutralino_from_stopbar(neutralinos[1]),
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
    p4_stop(p4_stops[0]),
    p4_stopbar(p4_stops[1]),
    p4_top(p4_tops[0]),
    p4_topbar(p4_tops[1]),
    p4_neutralino_from_stop(p4_neutralinos[0]),
    p4_neutralino_from_stopbar(p4_neutralinos[1]),
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
    Clear();
  }

  void Clear() {
    for (int i = 0; i < 2; ++i) {
      stops[i] = tops[i] = neutralinos[i] = Ws[i] = bottoms[i] = 0;
      for (int j = 0; j < 2; ++j)
	W_daughters[i][j] = 0;
      gluons_from_stops[i].clear();
      gluons_from_tops[i].clear();
      decay_type[i] = -1;
    }
    dif_leptons.clear();
    num_leptonic = -1;
  }

  void SetFourVectors();
  void Fill(const reco::GenParticleCollection&);
  void FindDIFJets(const reco::GenJetCollection&);
};

#endif
