#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

class MFVL1HTTFilter : public edm::EDFilter {
public:
  explicit MFVL1HTTFilter(const edm::ParameterSet&);

private:
  virtual bool filter(edm::Event&, const edm::EventSetup&);

  const edm::EDGetTokenT<float> l1htt_token;
  const double threshold;
};

MFVL1HTTFilter::MFVL1HTTFilter(const edm::ParameterSet& cfg)
  : l1htt_token(consumes<float>(edm::InputTag("mfvTriggerFloats", "l1htt"))),
    threshold(cfg.getParameter<double>("threshold"))
{
}

bool MFVL1HTTFilter::filter(edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<float> l1htt;
  event.getByToken(l1htt_token, l1htt);
  return *l1htt >= threshold;
}

DEFINE_FWK_MODULE(MFVL1HTTFilter);
