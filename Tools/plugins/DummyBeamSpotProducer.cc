
#include "RecoVertex/BeamSpotProducer/interface/BeamSpotProducer.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"

#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/IOVSyncValue.h"
#include "CondFormats/DataRecord/interface/BeamSpotObjectsRcd.h"
#include "CondFormats/BeamSpotObjects/interface/BeamSpotObjects.h"

#include "DataFormats/Math/interface/Error.h"
#include "DataFormats/Math/interface/Point3D.h"


class dummyBeamSpotProducer : public edm::EDProducer {
public:
  dummyBeamSpotProducer(const edm::ParameterSet&);
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

};

//
// constructors and destructor
//
dummyBeamSpotProducer::dummyBeamSpotProducer(const edm::ParameterSet& cfg)
  : X0(cfg.getParameter<double>("X0")),
    Y0(cfg.getParameter<double>("Y0")),
    Z0(cfg.getParameter<double>("Z0")),
    covariance(cfg.getParameter<std::vector<double>>("covariance")),
    SigmaZ(cfg.getParameter<double>("SigmaZ")),
    dxdz(cfg.getParameter<double>("dxdz")),
    dydz(cfg.getParameter<double>("dydz")),
    BeamWidthX(cfg.getParameter<double>("BeamWidthX")),
    BeamWidthY(cfg.getParameter<double>("BeamWidthY")),
    EmittanceX(cfg.getParameter<double>("EmittanceX")),
    EmittanceY(cfg.getParameter<double>("EmittanceY")),
    BetaStar(cfg.getParameter<double>("BetaStar"))
{
	
	edm::LogInfo("RecoVertex/BeamSpotProducer") 
		<< "Initializing Beam Spot producer " << "\n";
  
	//fVerbose=conf.getUntrackedParameter<bool>("verbose", false);
	
	produces<reco::BeamSpot>();

}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
dummyBeamSpotProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
	
	using namespace edm;

	std::auto_ptr<reco::BeamSpot> result(new reco::BeamSpot);

	reco::BeamSpot aSpot;

	
	//typedef math::XYZPoint Point;
    //enum { dimension = 7 };
    //typedef math::Error<dimension>::type CovarianceMatrix;

	
	//try {
	edm::LogInfo("RecoVertex/BeamSpotProducer") 
	  << "Reconstructing event number: " << iEvent.id() << "\n";

	// translate from BeamSpotObjects to reco::BeamSpot
	reco::BeamSpot::Point apoint( X0, Y0, Z0 );
		
	reco::BeamSpot::CovarianceMatrix matrix;
	int k = 0;
	for ( int i=0; i<7; ++i ) {
	  for ( int j=0; j<7; ++j ) {
	    matrix(i,j) = covariance[k];
	    k++;
	  }
	}
	
	// this assume beam width same in x and y
	aSpot = reco::BeamSpot( apoint,
				SigmaZ,
				dxdz,
				dydz,
				BeamWidthX,
				matrix );
	aSpot.setBeamWidthY( BeamWidthY );
	aSpot.setEmittanceX( EmittanceX );
	aSpot.setEmittanceY( EmittanceY );
	aSpot.setbetaStar( BetaStar );
		
	//}
	//
	//catch (std::exception & err) {
	//	edm::LogInfo("RecoVertex/BeamSpotProducer") 
	//		<< "Exception during event number: " << iEvent.id() 
	//		<< "\n" << err.what() << "\n";
	//}

	*result = aSpot;
	
	iEvent.put(result);
	
}

//define this as a plug-in
DEFINE_FWK_MODULE(dummyBeamSpotProducer);

