#include "FWCore/Framework/interface/one/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Run.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"

class MCStatProducer : public edm::one::EDProducer<edm::EndLuminosityBlockProducer> {
public:
  explicit MCStatProducer(const edm::ParameterSet&);

private:
  virtual void produce(edm::Event&, const edm::EventSetup&) override;
  virtual void endLuminosityBlockProduce(edm::LuminosityBlock&, const edm::EventSetup&) override;

  const edm::EDGetTokenT<GenEventInfoProduct> gen_info_token;

  int nevents;
  float sumweight;
  float sumweightprod;
};

MCStatProducer::MCStatProducer(const edm::ParameterSet& cfg)
  : gen_info_token(consumes<GenEventInfoProduct>(cfg.getParameter<edm::InputTag>("gen_info_src"))),
    nevents(0),
    sumweight(0),
    sumweightprod(0)
{
  produces<int,   edm::InLumi>("nEvents");
  produces<float, edm::InLumi>("sumWeight");
  produces<float, edm::InLumi>("sumWeightProd");
}

void MCStatProducer::produce(edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<GenEventInfoProduct> gen_info;
  event.getByToken(gen_info_token, gen_info);

  nevents += 1;
  sumweight += gen_info->weight();
  sumweightprod += gen_info->weightProduct();
}

void MCStatProducer::endLuminosityBlockProduce(edm::LuminosityBlock& lumi, const edm::EventSetup&) {
  std::unique_ptr<int> pnevents(new int(nevents));
  lumi.put(std::move(pnevents), "nEvents");

  std::unique_ptr<float> psumweight(new float(sumweight));
  lumi.put(std::move(psumweight), "sumWeight");

  std::unique_ptr<float> psumweightprod(new float(sumweightprod));
  lumi.put(std::move(psumweightprod), "sumWeightProd");

  nevents = 0;
  sumweight = sumweightprod = 0;
}

DEFINE_FWK_MODULE(MCStatProducer);
