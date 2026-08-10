#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"

class HalfMCByLumi : public edm::EDFilter {
public:
  explicit HalfMCByLumi(const edm::ParameterSet&);

private:
  virtual bool filter(edm::Event&, const edm::EventSetup&);
  const unsigned n;
  const bool first;
};

HalfMCByLumi::HalfMCByLumi(const edm::ParameterSet& cfg) 
  : n(cfg.getParameter<unsigned>("n")),
    first(cfg.getParameter<bool>("first"))
{
  if (n % 2 != 0) throw cms::Exception("n must be divisible by 2");
  printf("HalfMCByLumi: n: %i first? %i\n", n, first);
}

bool HalfMCByLumi::filter(edm::Event& event, const edm::EventSetup&) {
  return (event.luminosityBlock() % n < n/2) == first;
}

DEFINE_FWK_MODULE(HalfMCByLumi);
