#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/METReco/interface/GenMET.h"
#include "DataFormats/METReco/interface/GenMETCollection.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "JMTucker/Tools/interface/GenUtilities.h"
#include "JMTucker/Tools/interface/MCInteractionMFV3j.h"

class MFVGenParticles : public edm::EDProducer {
public:
  explicit MFVGenParticles(const edm::ParameterSet&);

private:
  virtual void produce(edm::Event&, const edm::EventSetup&);

  const edm::InputTag gen_src;
  const edm::InputTag gen_jet_src;
  const edm::InputTag gen_met_src;
  const bool print_info;
};

MFVGenParticles::MFVGenParticles(const edm::ParameterSet& cfg) 
  : gen_src(cfg.getParameter<edm::InputTag>("gen_src")),
    gen_jet_src(cfg.getParameter<edm::InputTag>("gen_jet_src")),
    gen_met_src(cfg.getParameter<edm::InputTag>("gen_met_src")),
    print_info(cfg.getParameter<bool>("print_info"))
{
  produces<reco::GenParticleCollection>("All");
  produces<reco::GenParticleCollection>("Visible");
  produces<reco::GenParticleCollection>("Bottoms");
}

void MFVGenParticles::produce(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<reco::GenParticleCollection> gen_particles;
  event.getByLabel(gen_src, gen_particles);
  edm::Handle<reco::GenJetCollection> gen_jets;
  event.getByLabel(gen_jet_src, gen_jets);
  edm::Handle<reco::GenMETCollection> gen_mets;
  event.getByLabel(gen_met_src, gen_mets);
  const reco::GenMET& gen_met = gen_mets->at(0);

  MCInteractionMFV3j mci;
  mci.Init(*gen_particles, *gen_jets, gen_met);

  std::auto_ptr<reco::GenParticleCollection> all(new reco::GenParticleCollection);
  reco::GenParticleRefProd ref_prod = event.getRefBeforePut<reco::GenParticleCollection>("All");

  std::auto_ptr<reco::GenParticleCollection> visible(new reco::GenParticleCollection);
  std::auto_ptr<reco::GenParticleCollection> bottoms(new reco::GenParticleCollection);

  if (mci.Valid()) {
    if (print_info)
      mci.Print(std::cout);

    const int n = 8;

    for (int i = 0; i < 2; ++i) {
      const reco::GenParticle old_gen[n] = {
	*mci.lsps             [i],
	*mci.stranges         [i],
	*mci.bottoms          [i],
	*mci.tops             [i],
	*mci.Ws               [i],
	*mci.bottoms_from_tops[i],
	*mci.W_daughters      [i][0],
	*mci.W_daughters      [i][1],
      };

      visible->push_back(reco::GenParticle(*mci.stranges[i]));
      visible->push_back(reco::GenParticle(*mci.bottoms[i]));
      visible->push_back(reco::GenParticle(*mci.bottoms_from_tops[i]));
      for (int k = 0; k < 2; ++k)
	if (!is_neutrino(mci.W_daughters[i][k]))
	  visible->push_back(reco::GenParticle(*mci.W_daughters[i][k]));

      bottoms->push_back(reco::GenParticle(*mci.bottoms[i]));
      bottoms->push_back(reco::GenParticle(*mci.bottoms_from_tops[i]));

      for (int j = 0; j < n; ++j) {
	all->push_back(reco::GenParticle(old_gen[j]));
	all->back().clearMothers();
	all->back().clearDaughters();
      }

      reco::GenParticle&             lsp(all->at(i*n + 0));
      reco::GenParticle&         strange(all->at(i*n + 1));
      reco::GenParticle&          bottom(all->at(i*n + 2));
      reco::GenParticle&             top(all->at(i*n + 3));
      reco::GenParticle&               W(all->at(i*n + 4));
      reco::GenParticle& bottom_from_top(all->at(i*n + 5));
      reco::GenParticle&    W_daughter_0(all->at(i*n + 6));
      reco::GenParticle&    W_daughter_1(all->at(i*n + 7));

      reco::GenParticleRef             lsp_ref(ref_prod, i*n + 0);
      reco::GenParticleRef         strange_ref(ref_prod, i*n + 1);
      reco::GenParticleRef          bottom_ref(ref_prod, i*n + 2);
      reco::GenParticleRef             top_ref(ref_prod, i*n + 3);
      reco::GenParticleRef               W_ref(ref_prod, i*n + 4);
      reco::GenParticleRef bottom_from_top_ref(ref_prod, i*n + 5);
      reco::GenParticleRef    W_daughter_0_ref(ref_prod, i*n + 6);
      reco::GenParticleRef    W_daughter_1_ref(ref_prod, i*n + 7);

      lsp.addDaughter(strange_ref);
      lsp.addDaughter( bottom_ref);
      lsp.addDaughter(    top_ref);

      strange.addMother(lsp_ref);
      bottom .addMother(lsp_ref);
      top    .addMother(lsp_ref);

      top.addDaughter(              W_ref);
      top.addDaughter(bottom_from_top_ref);

      W              .addMother(top_ref);
      bottom_from_top.addMother(top_ref);

      W.addDaughter(W_daughter_0_ref);
      W.addDaughter(W_daughter_1_ref);
      
      W_daughter_0.addMother(W_ref);
      W_daughter_1.addMother(W_ref);
    }
  }
  else
    edm::LogWarning("MFVGenParticles") << "MCInteractionMFV3j invalid! putting empty collections in event";

  event.put(all,     "All");
  event.put(visible, "Visible");
  event.put(bottoms, "Bottoms");
}

DEFINE_FWK_MODULE(MFVGenParticles);
