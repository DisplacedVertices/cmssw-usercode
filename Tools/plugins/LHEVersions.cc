#include <iostream>
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Run.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "SimDataFormats/GeneratorProducts/interface/LHERunInfoProduct.h"

class LHEVersions : public edm::EDAnalyzer {
public:
  explicit LHEVersions(const edm::ParameterSet&);

private:
  const bool endls;

  virtual void beginRun(const edm::Run&, const edm::EventSetup&);
  virtual void analyze(const edm::Event&, const edm::EventSetup&) {}
};

LHEVersions::LHEVersions(const edm::ParameterSet& cfg)
  : endls(cfg.getUntrackedParameter<bool>("endls", false))
{
}

void LHEVersions::beginRun(const edm::Run& run, edm::EventSetup const&) {
  edm::Handle<LHERunInfoProduct> product;
  run.getByLabel("source", product);

  int count = 0;
  for (LHERunInfoProduct::headers_const_iterator it = product->headers_begin(); it != product->headers_end(); ++it, ++count) {
    std::cout << "HEADER " << count << std::endl;
    for (std::vector<std::string>::const_iterator it2 = it->begin(); it2 != it->end(); ++it2)
      std::cout << *it2;
  }
}

DEFINE_FWK_MODULE(LHEVersions);
