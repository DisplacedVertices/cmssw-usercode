#include "FWCore/Framework/interface/one/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Run.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"

class MCStatProducer : public edm::one::EDProducer<edm::EndRunProducer> {
public:
  explicit MCStatProducer(const edm::ParameterSet&);

private:
  virtual void produce(edm::Event&, const edm::EventSetup&) override;
  virtual void endRunProduce(edm::Run&, const edm::EventSetup&) override;

  const edm::EDGetTokenT<GenEventInfoProduct> gen_info_token;

  int nevents;
  float sumweight;
  float sumweightprod;
};

MCStatProducer::MCStatProducer(const edm::ParameterSet& cfg)
  : gen_info_token(consumes<GenEventInfoProduct>(cfg.getParameter<edm::InputTag>("gen_info_src")))
{
  produces<int,   edm::InRun>("nEvents");
  produces<float, edm::InRun>("sumWeight");
  produces<float, edm::InRun>("sumWeightProd");
}

void MCStatProducer::produce(edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<GenEventInfoProduct> gen_info;
  event.getByToken(gen_info_token, gen_info);

  nevents += 1;
  sumweight += gen_info->weight();
  sumweightprod += gen_info->weightProduct();
}

void MCStatProducer::endRunProduce(edm::Run& run, const edm::EventSetup&) {
  std::unique_ptr<int> pnevents(new int(nevents));
  run.put(std::move(pnevents), "nEvents");

  std::unique_ptr<float> psumweight(new float(sumweight));
  run.put(std::move(psumweight), "sumWeight");

  std::unique_ptr<float> psumweightprod(new float(sumweightprod));
  run.put(std::move(psumweightprod), "sumWeightProd");
}

DEFINE_FWK_MODULE(MCStatProducer);
