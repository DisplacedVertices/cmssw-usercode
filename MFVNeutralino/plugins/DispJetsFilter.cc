#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "JMTucker/Tools/interface/Utilities.h"

class MFVDispJetsFilter : public edm::EDFilter {
public:
  explicit MFVDispJetsFilter(const edm::ParameterSet&);
  bool filter(edm::Event&, const edm::EventSetup&);
  const int a;
  const int b;
};

MFVDispJetsFilter::MFVDispJetsFilter(const edm::ParameterSet& cfg)
  : a(cfg.getParameter<int>("a")),
    b(cfg.getParameter<int>("b"))
{
}

bool MFVDispJetsFilter::filter(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<reco::GenParticleCollection> gen_particles;
  event.getByLabel("genParticles", gen_particles);

  std::vector<int> part_ids;

  for (int i = 0, ie = int(gen_particles->size()); i < ie; ++i) {
    const reco::GenParticle& g = gen_particles->at(i);
    if (g.status() != 3)
      continue;

    int id = g.pdgId();
    id -= 6000000;
    if (id < 0 || id > 10000)
      continue;

    part_ids.push_back(id);
  }

  die_if_not(part_ids.size() == 2, "parts found != 2: %i\n", int(part_ids.size()));

  if (b == 0) {
    die_if_not(a >= 1 && b <= 3, "a must be 1-3 if b == 0");
    return part_ids[0] % 10 == 4 && part_ids[1] % 10 == 4 && part_ids[0] / 1000 % 10 == a;
  }
  return a == std::min(part_ids[0], part_ids[1]) && b == std::max(part_ids[0], part_ids[1]);
}

DEFINE_FWK_MODULE(MFVDispJetsFilter);
