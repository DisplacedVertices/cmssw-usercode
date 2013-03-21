#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "JMTucker/Tools/interface/GenUtilities.h"
#include "JMTucker/Tools/interface/MCInteractionMFV3j.h"

class MFVGenParticleFilter : public edm::EDFilter {
public:
  explicit MFVGenParticleFilter(const edm::ParameterSet&);

private:
  virtual bool filter(edm::Event&, const edm::EventSetup&);

  const edm::InputTag gen_src;
  const edm::InputTag gen_jet_src;
  const edm::InputTag gen_met_src;
  const bool cut_invalid;
  const double min_rho;
  const double max_rho;
};

MFVGenParticleFilter::MFVGenParticleFilter(const edm::ParameterSet& cfg) 
  : gen_src(cfg.getParameter<edm::InputTag>("gen_src")),
    gen_jet_src(cfg.getParameter<edm::InputTag>("gen_jet_src")),
    gen_met_src(cfg.getParameter<edm::InputTag>("gen_met_src")),
    cut_invalid(cfg.getUntrackedParameter<bool>("cut_invalid", false)),
    min_rho(cfg.getUntrackedParameter<double>("min_rho", -1)),
    max_rho(cfg.getUntrackedParameter<double>("max_rho", -1))
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

  const double rho = mag(mci.stranges[0]->vx(), mci.stranges[0]->vy());
  if (min_rho > 0 && rho < min_rho)
    return false;
  if (max_rho > 0 && rho > max_rho)
    return false;

  return true;
}

DEFINE_FWK_MODULE(MFVGenParticleFilter);
