#ifndef JMTucker_Tools_MCInteraction_h
#define JMTucker_Tools_MCInteraction_h

#include "TLorentzVector.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/METReco/interface/GenMET.h"

struct MCInteraction {
  const reco::GenParticleCollection* gen_particles;
  const reco::GenJetCollection* gen_jets;
  const reco::GenMET* gen_met;

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
  
  std::vector<const reco::Candidate*> immediate_nus;
  std::vector<dif_lepton_pair> dif_leptons;

  TLorentzVector p4_dif_neutrinosum;
  TLorentzVector p4_neutrinosum;
  TLorentzVector p4_missingsum;

  enum Generator { pythia6, pythia8 };
  Generator generator;

  MCInteraction(Generator=pythia6);

  bool FromHardInteraction(const reco::Candidate*) const;

  virtual void Init(const reco::GenParticleCollection&, const reco::GenJetCollection&, const reco::GenMET&);

  virtual void Clear();
  virtual bool Valid();
  virtual void Fill();
  virtual void FindDIFLeptons();
  virtual void FindDIFJets();
  virtual void SetFourVectors();
  virtual void Print(std::ostream&);
};

#endif
