#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "JMTucker/Tools/interface/MCInteraction.h"
#include "JMTucker/Tools/interface/GenUtilities.h"
#include "JMTucker/Tools/interface/Utilities.h"

MCInteraction::dif_lepton_pair::dif_lepton_pair(const reco::Candidate* chg, const reco::Candidate* nu) :
  charged (dynamic_cast<const reco::GenParticle*>(chg)),
  neutrino(dynamic_cast<const reco::GenParticle*>(nu)),
  closest_jet(0),
  mother_jet(0),
  p4_charged (make_tlv(charged)),
  p4_neutrino(make_tlv(neutrino))
{
}

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
  FindDIFLeptons();
  
  SetFourVectors();
}

void MCInteraction::Init(const reco::GenParticleCollection& gen_particles_,
			 const reco::GenJetCollection& gen_jets_,
			 const reco::GenMET& gen_met_) {
  Clear();
  
  gen_particles = &gen_particles_;
  gen_jets = &gen_jets_;
  gen_met = &gen_met_;
  
  Fill();
  FindDIFLeptons();
  FindDIFJets();
  
  SetFourVectors();
}

void MCInteraction::Clear() {
  gen_particles = 0;
  gen_jets = 0;
  gen_met = 0;
  warned_no_dif_jets = false;
  immediate_nus.clear();
  dif_leptons.clear();
}

bool MCInteraction::Valid() {
  return true;
}

void MCInteraction::Fill() {
}

void MCInteraction::FindDIFLeptons() {
  // Find neutrinos and their charged lepton partners from
  // decays-in-flight. Don't include any "immediate" neutrinos,
  // e.g. from leptonic top decays, as specified in
  // immediate_nus. Fill() in derived classes is responsible for
  // setting this!
  
  static const bool debug = false;

  for (int i = 0, ie = int(gen_particles->size()); i < ie; ++i) {
    const reco::GenParticle& gen = gen_particles->at(i);
    if (gen.status() != 1 || !is_neutrino(&gen))
      continue;

    if (debug) printf("neutrino found at index %i with pdgId %i and status %i. number of mothers %i\n", i, gen.pdgId(), gen.status(), int(gen.numberOfMothers()));

    const reco::Candidate* nu = &gen;
    die_if_not(nu->numberOfMothers() == 1, "neutrino at index %i with # mothers = %i", i, nu->numberOfMothers());
    const reco::Candidate* nu_mom = nu->mother();
    if (nu_mom->pdgId() == nu->pdgId())
      while (!FromHardInteraction(nu_mom))
	nu_mom = nu_mom->mother();
    
    if (debug) {
      printf("status-3 neutrino mother (& = %p) found with pdgId %i and status %i. number of daughters %i\n", (void*)nu_mom, nu_mom->pdgId(), nu_mom->status(), int(nu_mom->numberOfDaughters()));
      printf("immediate_nus: ");
      for (const reco::Candidate* p : immediate_nus) 
	printf("%p ", (void*)p);
      printf("\n");
    }

    if (std::find(immediate_nus.begin(), immediate_nus.end(), nu_mom) != immediate_nus.end())
      continue;

    // We're looking for nus with mothers such as B0, where PYTHIA
    // sets the B0 daughters to be the neutrino and the charged lepton.
    // Skip "immediate" nus that aren't found by the previous test.
    if (nu_mom->numberOfDaughters() == 1 && nu_mom->pdgId() == nu->pdgId()) 
      continue;

    // Find the charged lepton partner. Should be the "sister" of the
    // nu, i.e. -11 for nu.id = 12. If nu is a nu_tau not from the
    // leptonic top decay, it won't have a sister, but rather a tau
    // mother that may or may not be from the leptonic top decay. In
    // either case, keep that tau.
    const reco::Candidate* chg = 0;
    for (size_t j = 0; j < nu_mom->numberOfDaughters(); ++j) {
      const reco::Candidate* dau = nu_mom->daughter(j);
      if (dau->pdgId() * nu->pdgId() < 0 && abs(nu->pdgId()) - abs(dau->pdgId()) == 1) {
	die_if_not(chg == 0, "found more than one sister charged lepton for nu");
	chg = dau; // don't break because we want to see if there's other possibilities
      }
    }

    if (chg == 0) {
      die_if_not(abs(nu->pdgId()) == 16, "did not find any sister charged lepton for nu (e or mu) at index %i", i);
      die_if_not(abs(nu_mom->pdgId()) == 15, "mother of nu_tau at index %i is not a tau", i);
      chg = nu_mom;
    }

    dif_leptons.push_back(dif_lepton_pair(chg, nu));
  }
}

void MCInteraction::FindDIFJets() {
  if (gen_jets == 0) {
    if (!warned_no_dif_jets)
      edm::LogWarning("MCInteraction") << "in, FindDIFJets, gen_jets pointer is null: not setting up closest/mother jets for decay-in-flight leptons.";
    warned_no_dif_jets = true;
    return;
  }

  for (int i = 0, ie = int(dif_leptons.size()); i < ie; ++i) {
    MCInteraction::dif_lepton_pair& dif = dif_leptons[i];
    
    double dR, closest_dR = 1e99;
    for (int j = 0, je = int(gen_jets->size()); j < je; ++j) {
      const reco::GenJet& gen_jet = gen_jets->at(j);

      // Look for a closest GenJet (in deltaR) to the charged
      // lepton. Only consider GenJets with p more than the lepton.
      if (gen_jet.pt() > dif.charged->pt() && (dR = reco::deltaR(gen_jet, *dif.charged)) < closest_dR) {
	closest_dR = dR;
	dif.closest_jet = &gen_jet;
      }

      // See if this GenJet has the charged lepton or neutrino as its
      // mother (should probably check for both), recording it if
      // so. Ensure that two GenJets don't wind up being associated to
      // the DIF in this way. JMTBAD need to revisit because of taus
      const std::vector<const reco::GenParticle*>& constituents = gen_jet.getGenConstituents();
      for (int k = 0, ke = int(constituents.size()); k < ke; ++k) {
	if ((abs(dif.charged->pdgId()) == 15 && constituents[k]->mother() == dif.charged) || constituents[k] == dif.charged) { // || constituents[k] == dif.neutrino) {
	  dif.mother_jet = &gen_jet;
	  break;
	}
      }
    }
  }
}

void MCInteraction::SetFourVectors() {
  p4_dif_neutrinosum = TLorentzVector();
  for (const auto& dif : dif_leptons)
    p4_dif_neutrinosum += dif.p4_neutrino;
  
  p4_neutrinosum = p4_dif_neutrinosum;
  p4_missingsum = p4_neutrinosum;
}

void MCInteraction::Print(std::ostream& out) {
  if (!dif_leptons.empty())
    printf("charged leptons/neutrinos from decays-in-flight:\n");
  for (int i = 0, ie = int(dif_leptons.size()); i < ie; ++i) {
    print_gen_and_daus(dif_leptons[i].charged,     TString::Format("chg #%i", i), *gen_particles);
    print_gen_and_daus(dif_leptons[i].neutrino,    TString::Format("nu  #%i", i), *gen_particles);
    print_gen_and_daus(dif_leptons[i].closest_jet, TString::Format("closest jet #%i", i), *gen_particles, false);
    print_gen_and_daus(dif_leptons[i].mother_jet,  TString::Format("mother  jet #%i", i), *gen_particles, false);
  }
  printf("p4_missingsum ex: %.2f  ey: %.2f    et: %.2f  phi: %.3f\n", p4_missingsum.Px(), p4_missingsum.Py(), p4_missingsum.Pt(), p4_missingsum.Phi());
}
