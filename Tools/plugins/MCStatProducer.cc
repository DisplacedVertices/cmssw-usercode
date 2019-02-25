#include <iostream>
#include "TH1.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/one/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Run.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
//#include "DataFormats/NanoAOD/interface/MergeableCounterTable.h" // not until CMSSW 9?
#include "JMTucker/Formats/interface/MergeablePOD.h"

class MCStatProducer : public edm::one::EDProducer<edm::EndLuminosityBlockProducer> {
public:
  explicit MCStatProducer(const edm::ParameterSet&);

private:
  virtual void produce(edm::Event&, const edm::EventSetup&) override;
  virtual void endLuminosityBlockProduce(edm::LuminosityBlock&, const edm::EventSetup&) override;

  const edm::EDGetTokenT<GenEventInfoProduct> gen_info_token;
  const int debug;

  int nevents;
  float sumweight;

  enum { sum_nevents_total, sum_gen_weight_total, n_sums };
  TH1D* h_sums;
};

MCStatProducer::MCStatProducer(const edm::ParameterSet& cfg)
  : gen_info_token(consumes<GenEventInfoProduct>(cfg.getParameter<edm::InputTag>("gen_info_src"))),
    debug(cfg.getUntrackedParameter<int>("debug", 0)),
    nevents(0),
    sumweight(0),
    h_sums(0)
{
  produces<jmt::MergeableInt,   edm::Transition::EndLuminosityBlock>("nEvents");
  produces<jmt::MergeableFloat, edm::Transition::EndLuminosityBlock>("sumWeight");

  edm::Service<TFileService> fs;
  if (fs) {
    TH1::SetDefaultSumw2();
    h_sums = fs->make<TH1D>("h_sums", "", n_sums, 0, n_sums);
    int ibin = 1;
    for (const char* x : { "sum_nevents_total", "sum_gen_weight_total" })
      h_sums->GetXaxis()->SetBinLabel(ibin++, x);
  }
}

void MCStatProducer::produce(edm::Event& event, const edm::EventSetup& setup) {
  nevents += 1;

  if (!event.isRealData()) {
    edm::Handle<GenEventInfoProduct> gen_info;
    event.getByToken(gen_info_token, gen_info);
    sumweight += gen_info->weight();
  }

  if (debug >= 2)
    std::cout << "after event " << event.id().run() << "," << event.luminosityBlock() << "," << event.id().event() << ": nevents = " << nevents << ", sumweight = " << sumweight << "\n";
}

void MCStatProducer::endLuminosityBlockProduce(edm::LuminosityBlock& lumi, const edm::EventSetup&) {
  if (h_sums) {
    h_sums->Fill(sum_nevents_total, nevents);
    h_sums->Fill(sum_gen_weight_total, sumweight);
  }

  if (debug >= 1)
    std::cout << "endLumiBlock lumi = " << lumi.id().run() << "," << lumi.luminosityBlock() << ": nevents = " << nevents << ", sumweight = " << sumweight << "\n";

  std::unique_ptr<jmt::MergeableInt> pnevents(new jmt::MergeableInt(nevents));
  lumi.put(std::move(pnevents), "nEvents");

  std::unique_ptr<jmt::MergeableFloat> psumweight(new jmt::MergeableFloat(sumweight));
  lumi.put(std::move(psumweight), "sumWeight");

  nevents = 0;
  sumweight = 0;
}

DEFINE_FWK_MODULE(MCStatProducer);
