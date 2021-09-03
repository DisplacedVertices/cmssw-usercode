#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DVCode/Tools/interface/GenUtilities.h"

class JMTGenParticleFilter : public edm::EDFilter {
public:
  explicit JMTGenParticleFilter(const edm::ParameterSet&);

private:
  virtual bool filter(edm::Event&, const edm::EventSetup&);

  const edm::EDGetTokenT<reco::GenParticleCollection> gen_particles_token;

  const double bsx;
  const double bsy;
  const double bsz;
  const double min_pvrho;
  const double max_pvrho;
  const int min_flavor_code;
  const int max_flavor_code;
};

JMTGenParticleFilter::JMTGenParticleFilter(const edm::ParameterSet& cfg)
  : gen_particles_token(consumes<reco::GenParticleCollection>(cfg.getParameter<edm::InputTag>("gen_particles_src"))),
    bsx(cfg.getParameter<double>("bsx")),
    bsy(cfg.getParameter<double>("bsy")),
    bsz(cfg.getParameter<double>("bsz")),
    min_pvrho(cfg.getParameter<double>("min_pvrho")),
    max_pvrho(cfg.getParameter<double>("max_pvrho")),
    min_flavor_code(cfg.getParameter<int>("min_flavor_code")),
    max_flavor_code(cfg.getParameter<int>("max_flavor_code"))
{
  produces<reco::GenParticleCollection>("heavyFlavor");
}

bool JMTGenParticleFilter::filter(edm::Event& event, const edm::EventSetup&) {
  bool keep = true;
  std::unique_ptr<reco::GenParticleCollection> heavy_flavor(new reco::GenParticleCollection);

  if (!event.isRealData()) {
    edm::Handle<reco::GenParticleCollection> gen_particles;
    event.getByToken(gen_particles_token, gen_particles);

    const reco::GenParticle& for_vtx = gen_particles->at(2);
    const int for_vtx_id = abs(for_vtx.pdgId());
    if (for_vtx_id != 21 && !(for_vtx_id >= 1 && for_vtx_id <= 5))
      throw cms::Exception("BadAssumption", "gen_particles[2] is not a gluon or udscb: id=") << for_vtx_id;

    const double pvx = for_vtx.vx();
    const double pvy = for_vtx.vy();
    const double pvrho = hypot(pvx - bsx, pvy - bsy);

    int flavor_code = 0;
    bool saw_c = false;
    for (const reco::GenParticle& gen : *gen_particles) {
      const bool is_b = is_bhadron(&gen);
      const bool is_c = is_chadron(&gen);

      if (is_b)
	flavor_code = 2;
      else if (is_c)
	saw_c = true;

      if ((is_b || is_c) && gen.status() == 2)
        heavy_flavor->push_back(gen);
    }
    if (saw_c && flavor_code == 0)
      flavor_code = 1;

    if (pvrho < min_pvrho || pvrho > max_pvrho)
      keep = false;

    if (flavor_code < min_flavor_code || flavor_code > max_flavor_code)
      keep = false;
  }

  event.put(std::move(heavy_flavor), "heavyFlavor");
  return keep;
}

DEFINE_FWK_MODULE(JMTGenParticleFilter);
