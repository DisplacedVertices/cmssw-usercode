#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"

class NoOP : public edm::EDAnalyzer {
public:
  explicit NoOP(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
};

NoOP::NoOP(const edm::ParameterSet& cfg) 
{
}

void NoOP::analyze(const edm::Event& event, const edm::EventSetup&) {
}

DEFINE_FWK_MODULE(NoOP);
