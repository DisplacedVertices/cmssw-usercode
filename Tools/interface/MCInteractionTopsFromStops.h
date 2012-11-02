#ifndef JMTucker_Tools_MCInteractionTopsFromStops_h
#define JMTucker_Tools_MCInteractionTopsFromStops_h

#include "JMTucker/Tools/interface/MCInteractionTops.h"

struct MCInteractionTopsFromStops : public MCInteractionTops { 
  const reco::GenParticle* stops[2]; // stop, stopbar
  const reco::GenParticle* neutralinos[2]; // from_stop, from_stopbar
  std::vector<const reco::Candidate*> gluons_from_stops[2];

  // "Plain" momentum four-vectors.
  TLorentzVector p4_stops[2];
  TLorentzVector p4_neutralinos[2];
  TLorentzVector p4_stopstopbar;
  TLorentzVector p4_neutralinosum;

  // Convenience aliases.
  const reco::GenParticle*& stop;
  const reco::GenParticle*& stopbar;
  const reco::GenParticle*& neutralino_from_stop;
  const reco::GenParticle*& neutralino_from_stopbar;
  TLorentzVector& p4_stop;
  TLorentzVector& p4_stopbar;
  TLorentzVector& p4_neutralino_from_stop;
  TLorentzVector& p4_neutralino_from_stopbar;

  MCInteractionTopsFromStops() :
    MCInteractionTops(),
    stop(stops[0]),
    stopbar(stops[1]),
    neutralino_from_stop(neutralinos[0]),
    neutralino_from_stopbar(neutralinos[1]),
    p4_stop(p4_stops[0]),
    p4_stopbar(p4_stops[1]),
    p4_neutralino_from_stop(p4_neutralinos[0]),
    p4_neutralino_from_stopbar(p4_neutralinos[1])
  {
  }

  virtual void Clear();
  virtual bool Valid();
  virtual void Fill();
  virtual void SetFourVectors();
  virtual void Print(std::ostream&);
};

#endif
