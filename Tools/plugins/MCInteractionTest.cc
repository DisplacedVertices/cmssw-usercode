#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/METReco/interface/GenMETCollection.h"

#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "JMTucker/Tools/interface/MCInteraction.h"
#include "JMTucker/Tools/interface/MCInteractionTops.h"
#include "JMTucker/Tools/interface/MCInteractionTopsFromStops.h"

class MCInteractionTest : public edm::EDAnalyzer {
public:
  explicit MCInteractionTest(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  bool pythia8;
};

MCInteractionTest::MCInteractionTest(const edm::ParameterSet& cfg)
  : pythia8(cfg.existsAs<bool>("pythia8") ? cfg.getParameter<bool>("pythia8") : false)
{
}

void MCInteractionTest::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<reco::GenParticleCollection> gen_particles;
  event.getByLabel("genParticles", gen_particles);
  edm::Handle<reco::GenJetCollection> gen_jets;
  event.getByLabel("ak5GenJets", gen_jets);
  edm::Handle<reco::GenMETCollection> gen_mets;
  event.getByLabel("genMetTrue", gen_mets);

  const MCInteraction::Generator g = pythia8 ? MCInteraction::pythia8 : MCInteraction::pythia6;
  MCInteraction              mci    (g);
  MCInteractionTops          mci_top(g);
  MCInteractionTopsFromStops mci_tfs(g);

  printf("inits: mci\n"); fflush(stdout);
  mci.Init    (*gen_particles, *gen_jets, gen_mets->at(0));
  printf("inits: mci_top\n"); fflush(stdout);
  mci_top.Init(*gen_particles, *gen_jets, gen_mets->at(0));
  printf("inits: mci_tfs\n"); fflush(stdout);
  mci_tfs.Init(*gen_particles, *gen_jets, gen_mets->at(0));
  printf("inits: done\n"); fflush(stdout);

  printf("\nMCInteraction:\n");
  mci.Print(std::cout);
  printf("\nMCInteractionTops:\n");
  mci_top.Print(std::cout);
  printf("\nMCInteractionTopsFromStops:\n");
  mci_tfs.Print(std::cout);
}

DEFINE_FWK_MODULE(MCInteractionTest);
