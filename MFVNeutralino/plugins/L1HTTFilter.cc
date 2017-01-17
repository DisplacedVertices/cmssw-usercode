#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DataFormats/L1Trigger/interface/L1EtMissParticle.h"
#include "DataFormats/L1Trigger/interface/L1EtMissParticleFwd.h"

class MFVL1HTTFilter : public edm::EDFilter {
public:
  explicit MFVL1HTTFilter(const edm::ParameterSet&);

private:
  virtual bool filter(edm::Event&, const edm::EventSetup&);

  const edm::EDGetTokenT<l1extra::L1EtMissParticleCollection> l1_htt_token;
  const double threshold;
};

MFVL1HTTFilter::MFVL1HTTFilter(const edm::ParameterSet& cfg)
  : l1_htt_token(consumes<l1extra::L1EtMissParticleCollection>(edm::InputTag("l1extraParticles", "MHT"))),
    threshold(cfg.getParameter<double>("threshold"))
{
}

bool MFVL1HTTFilter::filter(edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<l1extra::L1EtMissParticleCollection> l1_htts;
  event.getByToken(l1_htt_token, l1_htts);
  if (l1_htts->size() != 1)
    throw cms::Exception("BadAssumption", "not exactly one L1 MHT object");
  const l1extra::L1EtMissParticle& l1_htt = l1_htts->at(0);
  if (l1_htt.type() != 1)
    throw cms::Exception("BadAssumption", "L1 MHT object in collection not right type");
  //printf("l1_htt.etTotal() %f\n", l1_htt.etTotal());
  return l1_htt.etTotal() >= threshold;
}

DEFINE_FWK_MODULE(MFVL1HTTFilter);
