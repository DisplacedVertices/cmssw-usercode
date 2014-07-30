#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"

class MFVPresentFilter : public edm::EDFilter {
public:
  explicit MFVPresentFilter(const edm::ParameterSet&);

private:
  virtual bool filter(edm::Event&, const edm::EventSetup&);
  const edm::InputTag mevent_src;
};

MFVPresentFilter::MFVPresentFilter(const edm::ParameterSet& cfg) 
  : mevent_src(cfg.getParameter<edm::InputTag>("mevent_src"))
{
}

bool MFVPresentFilter::filter(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<MFVEvent> mevent;
  event.getByLabel(mevent_src, mevent);
  return mevent.isValid();
}

DEFINE_FWK_MODULE(MFVPresentFilter);
