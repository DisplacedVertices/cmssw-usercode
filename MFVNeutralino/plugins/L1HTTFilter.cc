#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DVCode/MFVNeutralinoFormats/interface/TriggerFloats.h"

class MFVL1HTTFilter : public edm::EDFilter {
public:
  explicit MFVL1HTTFilter(const edm::ParameterSet&);

private:
  virtual bool filter(edm::Event&, const edm::EventSetup&);

  const edm::EDGetTokenT<mfv::TriggerFloats> triggerfloats_token;
  const double threshold;
};

MFVL1HTTFilter::MFVL1HTTFilter(const edm::ParameterSet& cfg)
  : triggerfloats_token(consumes<mfv::TriggerFloats>(edm::InputTag("mfvTriggerFloats"))),
    threshold(cfg.getParameter<double>("threshold"))
{
}

bool MFVL1HTTFilter::filter(edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<mfv::TriggerFloats> triggerfloats;
  event.getByToken(triggerfloats_token, triggerfloats);
  return triggerfloats->l1htt >= threshold;
}

DEFINE_FWK_MODULE(MFVL1HTTFilter);
