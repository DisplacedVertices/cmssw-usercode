#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "JMTucker/MFVNeutralino/interface/MCInteractionMFV3j.h"
#include "JMTucker/Tools/interface/GenUtilities.h"

class MFVGenParticleFilter : public edm::EDFilter {
public:
  explicit MFVGenParticleFilter(const edm::ParameterSet&);

private:
  virtual bool filter(edm::Event&, const edm::EventSetup&);

  const edm::InputTag gen_src;
  const bool cut_invalid;
  const double min_rho0;
  const double max_rho0;
  const double min_rho1;
  const double max_rho1;
};

MFVGenParticleFilter::MFVGenParticleFilter(const edm::ParameterSet& cfg) 
  : gen_src(cfg.getParameter<edm::InputTag>("gen_src")),
    cut_invalid(cfg.getParameter<bool>("cut_invalid")),
    min_rho0(cfg.getParameter<double>("min_rho0")),
    max_rho0(cfg.getParameter<double>("max_rho0")),
    min_rho1(cfg.getParameter<double>("min_rho1")),
    max_rho1(cfg.getParameter<double>("max_rho1"))
{
}

namespace {
  template <typename T>
  T mag(T x, T y) {
    return sqrt(x*x + y*y);
  }
}

bool MFVGenParticleFilter::filter(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<reco::GenParticleCollection> gen_particles;
  event.getByLabel(gen_src, gen_particles);

  MCInteractionMFV3j mci;
  mci.Init(*gen_particles);

  if (cut_invalid && !mci.Valid())
    return false;

  const double rho0 = mag(mci.stranges[0]->vx() - mci.lsps[0]->vx(), mci.stranges[0]->vy() - mci.lsps[0]->vy());
  const double rho1 = mag(mci.stranges[1]->vx() - mci.lsps[1]->vx(), mci.stranges[1]->vy() - mci.lsps[1]->vy());

  if (min_rho0 > 0 && rho0 < min_rho0)
    return false;
  if (max_rho0 > 0 && rho0 > max_rho0)
    return false;
  if (min_rho1 > 0 && rho1 < min_rho1)
    return false;
  if (max_rho1 > 0 && rho1 > max_rho1)
    return false;

  return true;
}

DEFINE_FWK_MODULE(MFVGenParticleFilter);
