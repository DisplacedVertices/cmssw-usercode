#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/Math/interface/Error.h"
#include "DataFormats/Math/interface/Point3D.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"

class DummyBeamSpotProducer : public edm::EDProducer {
public:
  DummyBeamSpotProducer(const edm::ParameterSet&);
  virtual void produce(edm::Event&, const edm::EventSetup&);

private:
  const double X0;
  const double Y0;
  const double Z0;
  const std::vector<double> covariance;
  const double SigmaZ;
  const double dxdz;
  const double dydz;
  const double BeamWidthX;
  const double BeamWidthY;
  const double EmittanceX;
  const double EmittanceY;
  const double BetaStar;

  reco::BeamSpot spot;
};

DummyBeamSpotProducer::DummyBeamSpotProducer(const edm::ParameterSet& cfg)
  : X0(cfg.getParameter<double>("X0")),
    Y0(cfg.getParameter<double>("Y0")),
    Z0(cfg.getParameter<double>("Z0")),
    covariance(cfg.getParameter<std::vector<double> >("covariance")),
    SigmaZ(cfg.getParameter<double>("SigmaZ")),
    dxdz(cfg.getParameter<double>("dxdz")),
    dydz(cfg.getParameter<double>("dydz")),
    BeamWidthX(cfg.getParameter<double>("BeamWidthX")),
    BeamWidthY(cfg.getParameter<double>("BeamWidthY")),
    EmittanceX(cfg.getParameter<double>("EmittanceX")),
    EmittanceY(cfg.getParameter<double>("EmittanceY")),
    BetaStar(cfg.getParameter<double>("BetaStar"))
{
  const reco::BeamSpot::Point pos(X0, Y0, Z0);
  const reco::BeamSpot::CovarianceMatrix cov(covariance.begin(), covariance.end(), true, false);

  spot = reco::BeamSpot(pos, SigmaZ, dxdz, dydz, BeamWidthX, cov);
  spot.setBeamWidthY(BeamWidthY);
  spot.setEmittanceX(EmittanceX);
  spot.setEmittanceY(EmittanceY);
  spot.setbetaStar(BetaStar);

  produces<reco::BeamSpot>();
}

void DummyBeamSpotProducer::produce(edm::Event& event, const edm::EventSetup&) {
  event.put(std::unique_ptr<reco::BeamSpot>(new reco::BeamSpot(spot)));
}

DEFINE_FWK_MODULE(DummyBeamSpotProducer);
