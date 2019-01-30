#include "TH1.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"

class JMTNegativeWeights : public edm::EDAnalyzer {
public:
  explicit JMTNegativeWeights(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override;

  const edm::EDGetTokenT<GenEventInfoProduct> gen_info_token;

  TH1D* h_nweights;
  TH1D* h_weight_eq_product;
  TH1D* h_weight_sign;
};

JMTNegativeWeights::JMTNegativeWeights(const edm::ParameterSet& cfg)
  : gen_info_token(consumes<GenEventInfoProduct>(cfg.getParameter<edm::InputTag>("gen_info_src")))
{
  edm::Service<TFileService> fs;
  TH1::SetDefaultSumw2();

  h_nweights = fs->make<TH1D>("h_nweights", "", 100, 0, 100);
  h_weight_eq_product = fs->make<TH1D>("h_weight_eq_product", "", 2, 0, 2);
  h_weight_sign = fs->make<TH1D>("h_weight_sign", "", 2, 0, 2);
}

void JMTNegativeWeights::analyze(const edm::Event& event, const edm::EventSetup&) {
  if (event.isRealData())
    return;

  edm::Handle<GenEventInfoProduct> gen_info;
  event.getByToken(gen_info_token, gen_info);

  h_nweights->Fill(gen_info->weights().size());
  h_weight_eq_product->Fill(fabs(gen_info->weight() - gen_info->weightProduct()) / gen_info->weight() < 1e-3);
  h_weight_sign->Fill(gen_info->weight() > 0);
}

DEFINE_FWK_MODULE(JMTNegativeWeights);
