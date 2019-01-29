#include <iostream>
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Run.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "SimDataFormats/GeneratorProducts/interface/LHERunInfoProduct.h"

class LHEVersions : public edm::EDAnalyzer {
public:
  explicit LHEVersions(const edm::ParameterSet&);
private:
  virtual void endRun(const edm::Run&, const edm::EventSetup&) override;
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override {}

  edm::EDGetTokenT<LHERunInfoProduct> token;
  const std::string sep;
};

LHEVersions::LHEVersions(const edm::ParameterSet& cfg)
  : token(consumes<LHERunInfoProduct, edm::InRun>(edm::InputTag("externalLHEProducer"))),
    sep("\n================================================================================\n")
{}

void LHEVersions::endRun(const edm::Run& run, edm::EventSetup const&) {
  std::cout << "LHEVersions::beginRun run " << run.id().run() << "\n";

  edm::Handle<LHERunInfoProduct> product;
  run.getByToken(token, product);

  int count = 0;
  for (LHERunInfoProduct::headers_const_iterator it = product->headers_begin(); it != product->headers_end(); ++it, ++count) {
    std::cout << sep << "LHE header #" << count << " tag " << it->tag() << " lines:\n";
    for (auto line : it->lines())
      std::cout << line;
  }

  if (product->comments_size()) {
    count = 0;
    for (LHERunInfoProduct::comments_const_iterator it = product->comments_begin(); it != product->comments_end(); ++it, ++count)
      std::cout << sep << "LHE comment #" << count << " " << *it;
  }
  else
    std::cout << sep << "LHE comments empty\n";
}

DEFINE_FWK_MODULE(LHEVersions);
