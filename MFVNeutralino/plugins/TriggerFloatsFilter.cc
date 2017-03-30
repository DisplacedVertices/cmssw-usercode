#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "JMTucker/MFVNeutralinoFormats/interface/TriggerFloats.h"

class MFVTriggerFloatsFilter : public edm::EDFilter {
public:
  explicit MFVTriggerFloatsFilter(const edm::ParameterSet&);

private:
  virtual bool filter(edm::Event&, const edm::EventSetup&);

  const edm::EDGetTokenT<mfv::TriggerFloats> triggerfloats_token;

  const double hltht_cut;
};

MFVTriggerFloatsFilter::MFVTriggerFloatsFilter(const edm::ParameterSet& cfg) 
  : triggerfloats_token(consumes<mfv::TriggerFloats>(edm::InputTag("mfvTriggerFloats"))),
    hltht_cut(cfg.getParameter<double>("hltht_cut"))
{
}

bool MFVTriggerFloatsFilter::filter(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<mfv::TriggerFloats> triggerfloats;
  event.getByToken(triggerfloats_token, triggerfloats);

  if (hltht_cut > 0 && triggerfloats->hltht < hltht_cut)
    return false;

  return true;
}

DEFINE_FWK_MODULE(MFVTriggerFloatsFilter);
