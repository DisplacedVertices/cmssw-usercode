#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "JMTucker/Tools/interface/GenUtilities.h"
#include "JMTucker/MFVNeutralino/interface/MCInteractionMFV3j.h"

class MFVGenParticles : public edm::EDProducer {
public:
  explicit MFVGenParticles(const edm::ParameterSet&);

private:
  virtual void produce(edm::Event&, const edm::EventSetup&);

  const edm::EDGetTokenT<reco::GenParticleCollection> gen_particles_token;
  const bool print_info;
};

MFVGenParticles::MFVGenParticles(const edm::ParameterSet& cfg) 
  : gen_particles_token(consumes<reco::GenParticleCollection>(cfg.getParameter<edm::InputTag>("gen_particles_src"))),
    print_info(cfg.getParameter<bool>("print_info"))
{
  produces<reco::GenParticleCollection>("All");
  produces<reco::GenParticleCollection>("Visible");
  produces<reco::GenParticleCollection>("Bottoms");
  produces<reco::GenParticleCollection>("Status1");
  produces<reco::GenParticleCollection>("Status1FromTBS");
}

namespace {
  template <typename T>
  T mag(const T& x, const T& y) {
    return sqrt(x*x + y*y);
  }
}

void MFVGenParticles::produce(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<reco::GenParticleCollection> gen_particles;
  event.getByToken(gen_particles_token, gen_particles);

  MCInteractionMFV3j mci;
  mci.Init(*gen_particles);

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


  std::auto_ptr<reco::GenParticleCollection> status1   (new reco::GenParticleCollection);
  std::auto_ptr<reco::GenParticleCollection> status1tbs(new reco::GenParticleCollection);

  for (const auto& gen : *gen_particles) {
    if (gen.status() == 1 && gen.charge() != 0 && mag(gen.vx(), gen.vy()) < 120 && abs(gen.vz()) < 300) {
      if (has_any_ancestor_with_id(&gen, 1000021))
        status1->push_back(gen);
      if (mci.Ancestor(&gen, "quark"))
        status1tbs->push_back(gen);
    }
  }

  event.put(status1,    "Status1");
  event.put(status1tbs, "Status1FromTBS");
}

DEFINE_FWK_MODULE(MFVGenParticles);
