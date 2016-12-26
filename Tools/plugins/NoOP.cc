#include "CLHEP/Random/RandomEngine.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/RandomNumberGenerator.h"

class NoOP : public edm::EDAnalyzer {
public:
  explicit NoOP(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  const double exception_chance;
};

NoOP::NoOP(const edm::ParameterSet& cfg)
  : exception_chance(cfg.getUntrackedParameter<double>("exception_chance", -1))
{
  edm::Service<edm::RandomNumberGenerator> rng;
  if (exception_chance > 0 && !rng.isAvailable())
    throw cms::Exception("NoOP", "RandomNumberGeneratorService not available");
}

void NoOP::analyze(const edm::Event& event, const edm::EventSetup&) {
  if (exception_chance > 0) {
    edm::Service<edm::RandomNumberGenerator> rng;
    if (rng->getEngine(event.streamID()).flat() < exception_chance)
      throw cms::Exception("NoOP", "pop goes the weasel");
  }
}

DEFINE_FWK_MODULE(NoOP);
