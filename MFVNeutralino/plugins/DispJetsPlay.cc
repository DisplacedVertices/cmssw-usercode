#include "TH1F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/GenUtilities.h"
#include "JMTucker/Tools/interface/Utilities.h"

class MFVDispJetsPlay : public edm::EDProducer {
public:
  explicit MFVDispJetsPlay(const edm::ParameterSet&);
  void produce(edm::Event&, const edm::EventSetup&);

private:
  bool debug;
  TH1F* h_nthing1s;
  TH1F* h_mass;
  TH1F* h_beta;
  TH1F* h_betagamma;
  TH1F* h_r;
  TH1F* h_tau;
  TH1F* h_dauid;
};

MFVDispJetsPlay::MFVDispJetsPlay(const edm::ParameterSet& cfg)
  : debug(cfg.getUntrackedParameter<bool>("debug", false))
{
  edm::Service<TFileService> fs;
  h_nthing1s = fs->make<TH1F>("h_nthing1s", "", 20, 0, 20);
  h_mass = fs->make<TH1F>("h_mass", "", 2000, 0, 2000);
  h_beta = fs->make<TH1F>("h_beta", "", 2000, 0, 1);
  h_betagamma = fs->make<TH1F>("h_betagamma", "", 2000, 0, 100);
  h_r = fs->make<TH1F>("h_r", "", 2000, 0, 1000);
  h_tau = fs->make<TH1F>("h_tau", "", 2000, 0, 1000);
  h_dauid = fs->make<TH1F>("h_dauid", "", 39, -19, 20);
}

namespace {
  float mag(float x, float y, float z) {
    return sqrt(x*x + y*y + z*z);
  }
}

void MFVDispJetsPlay::produce(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<reco::GenParticleCollection> gen_particles;
  event.getByLabel("genParticles", gen_particles);

  std::vector<int> thing1_ids;
  int thing1s_found = 0;
  for (int i = 0, ie = int(gen_particles->size()); i < ie; ++i) {
    const reco::GenParticle& g = gen_particles->at(i);
    if (g.status() != 3)
      continue;

    int id = g.pdgId();
    id -= 6000000;
    if (id < 0 || id > 10000)
      continue;

    thing1_ids.push_back(id);
    ++thing1s_found;
      
    die_if_not(g.numberOfDaughters() == 3, "thing1 particle at %i has not 3 daughters: %i", i, g.numberOfDaughters());
    h_mass->Fill(g.mass());

    double beta = g.p()/g.energy();
    double betagamma = beta/sqrt(1-beta*beta);

    h_beta->Fill(beta);
    h_betagamma->Fill(betagamma);

    int thing2s_found = 0;

    for (int j = 0, je = g.numberOfDaughters(); j < je; ++j) {
      const reco::Candidate* gd = g.daughter(j);
      if (gd->status() == 3) {
        //die_if_not(gd->numberOfDaughters() == 1, "thing2 particle at %i has more than one dau", original_index(gd, *gen_particles));
        die_if_not(is_quark(gd) || is_lepton(gd), "thing2 is not q or l");
        ++thing2s_found;

        const reco::Candidate* gdd = gd->daughter(0);
        //die_if_not(gdd->pdgId() == gd->pdgId(), "thing2 daughter is not thing2's type");
        die_if_not(gdd->status() == 1 || gdd->status() == 2, "thing2 daughter at line %i is not status-1", original_index(gdd, *gen_particles));

        h_dauid->Fill(gdd->pdgId());

        double r = mag(gdd->vx() - g.vx(),
                       gdd->vy() - g.vy(),
                       gdd->vz() - g.vz());
        double tau = r / betagamma;

        h_r->Fill(r);
        h_tau->Fill(tau);

        if (debug)
          printf("thing1 #%i at %i: mass: %f    beta: %f    betagamma: %f    r %f   tau: %f\n", thing1s_found, i, g.mass(), beta, betagamma, r, tau);

        if (thing2s_found)
          break;
      }
    }
  }

  die_if_not(thing1s_found == 2, "thing1s found != 2: %i\n", thing1s_found);
  printf("SORTED: %i %i\n", std::min(thing1_ids[0], thing1_ids[1]), std::max(thing1_ids[0], thing1_ids[1]));
  printf("THING1S: %i %i\n", thing1_ids[0], thing1_ids[1]);
  h_nthing1s->Fill(thing1s_found);
}

DEFINE_FWK_MODULE(MFVDispJetsPlay);
