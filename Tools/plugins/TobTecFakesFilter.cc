// -*- C++ -*-
//
// Class:      TobTecFakesFilter
//
// Original Author:  Kevin Stenson
//
//

// system include files
#include <memory>
#include <string>
#include <vector>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"

//
// class declaration
//

class TobTecFakesFilter : public edm::EDFilter {
   public:
      explicit TobTecFakesFilter(const edm::ParameterSet&);
      ~TobTecFakesFilter();

   private:
      virtual void beginJob() ;
      virtual bool filter(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      // ----------member data ---------------------------

  edm::InputTag m_trackCollection;
  const double m_minEta; // define the transition region where problems occur
  const double m_maxEta; // as above
  const double m_phiWindow; // size in phi to look for "jet" of tracks
  const bool m_filter; // apply filter or not
  const double m_ratioAllCut; // cut on ratio of TOBTEC/Pixel tracks
  const double m_ratioJetCut; // cut on ratio of TOBTEC/Pixel tracks in "jet"
  const double m_absJetCut; // cut on TOBTEC tracks in "jet"

};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
TobTecFakesFilter::TobTecFakesFilter(const edm::ParameterSet& iConfig):
  m_trackCollection(iConfig.getParameter<edm::InputTag>("trackCollection")),
  m_minEta(iConfig.getParameter<double>("minEta")),
  m_maxEta(iConfig.getParameter<double>("maxEta")),
  m_phiWindow(iConfig.getParameter<double>("phiWindow")),
  m_filter(iConfig.getParameter<bool>("filter")),
  m_ratioAllCut(iConfig.getParameter<double>("ratioAllCut")),
  m_ratioJetCut(iConfig.getParameter<double>("ratioJetCut")),
  m_absJetCut(iConfig.getParameter<double>("absJetCut"))
{
   //now do what ever initialization is needed
}

TobTecFakesFilter::~TobTecFakesFilter()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called on each new Event  ------------
bool
TobTecFakesFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;
  
  bool selected = true;
  const double piconst = 3.141592653589793;
  const double twopiconst = 2.0*piconst;
  const int phibins = 100;
  const double phibinsize = twopiconst/static_cast<double>(phibins);
  Handle<reco::TrackCollection> trks;
  iEvent.getByLabel(m_trackCollection,trks);
  
  int pxlmin = 4; // iteration 0 (InitialStep)
  int pxlmax = 6; // iteration 2 (PixelPairStep)
  int itertobtec = 10; // iteration 6 (TobTecStep)

  int phiIterPixelTrks[phibins][2] = { {0} };
  int phiIterTobTecTrks[phibins][2] = { {0} };
  double n_iterPixelTrks = 0;
  double n_iterTobTecTrks = 0;

  int i_trkphi;
  double trkabseta;
  int trkalgo;

  // Count up pixel seeded tracks (n_iterPixelTrks) and TOBTEC seeded tracks (n_iterTobTecTrks)
  // Also count up pixel seeded and TOBTEC seeded tracks in bins of phi in the transition region
  for (reco::TrackCollection::const_iterator trk=trks->begin(); trk!=trks->end(); ++trk){
    trkalgo = trk->algo();
    if (trkalgo >= pxlmin && trkalgo <= pxlmax) ++n_iterPixelTrks;
    if (trkalgo == itertobtec) ++n_iterTobTecTrks;
    trkabseta = fabs(trk->eta());
    int zside = 0;
    if (trk->eta() > 0) zside = 1;
    if (trkabseta < m_maxEta && trkabseta > m_minEta) {
      i_trkphi = std::max(0,std::min(phibins-1,(int) ((trk->phi()+piconst)/phibinsize)));
      if (trkalgo >= pxlmin && trkalgo <= pxlmax) ++phiIterPixelTrks[i_trkphi][zside];
      if (trkalgo == itertobtec) ++phiIterTobTecTrks[i_trkphi][zside];
    }
  }
  if (n_iterPixelTrks < 0.5) n_iterPixelTrks = 1.0; // avoid divide by zero
  double ritertobtec = n_iterTobTecTrks / n_iterPixelTrks; // ratio of TOBTEC seeded to pixel seeded tracks

  // Simple jet finder for TOBTEC seeded tracks.  Find the value of phi that maximizes
  // the number of tracks inside a phi window of windowRange (only for tracks in the 
  // transition region.
  int windowRange = std::max(1,static_cast<int>(m_phiWindow/phibinsize+0.5));
  int runPhiIterTobTec[phibins][2] = { {0} };
  int lowindx;
  int maxIterTobTecPhiTrks = -1;
  int maxIterTobTecPhiTrksBin = -1;
  int maxIterTobTecPhiTrksZBin = -1;
  for (int zside = 0; zside < 2; ++zside) {
    for (int iphi = phibins-windowRange+1; iphi < phibins; ++iphi) {
      runPhiIterTobTec[0][zside] += phiIterTobTecTrks[iphi][zside];
    }
    runPhiIterTobTec[0][zside] += phiIterTobTecTrks[0][zside];
    for (int iphi = 1; iphi < phibins; ++iphi) {
      lowindx = iphi-windowRange;
      if (lowindx < 0) lowindx += phibins;
      runPhiIterTobTec[iphi][zside] = runPhiIterTobTec[iphi-1][zside] + phiIterTobTecTrks[iphi][zside] - phiIterTobTecTrks[lowindx][zside];
      if (runPhiIterTobTec[iphi][zside] > maxIterTobTecPhiTrks) {
	maxIterTobTecPhiTrks = runPhiIterTobTec[iphi][zside];
	maxIterTobTecPhiTrksBin = iphi;
	maxIterTobTecPhiTrksZBin = zside;
      }
    }
  }
  double n_iterTobTecTrksInIterTobTecJet = static_cast<double>(maxIterTobTecPhiTrks);
  double n_iterPixelTrksInIterTobTecJet = 0.0;

  // Find the number of pixel seeded tracks in the same region that maximizes the number
  // of TOBTEC seeded tracks.
  int indx;
  for (int iphi = maxIterTobTecPhiTrksBin-windowRange+1; iphi < maxIterTobTecPhiTrksBin+1; ++iphi) {
    indx = iphi < 0 ? phibins+iphi : iphi;
    n_iterPixelTrksInIterTobTecJet += phiIterPixelTrks[indx][maxIterTobTecPhiTrksZBin];
  }
  if (n_iterPixelTrksInIterTobTecJet < 0.5) n_iterPixelTrksInIterTobTecJet = 1.0; // avoid divide by zero

//  std::cout << "Counting gives " << n_iterTobTecTrksInIterTobTecJet << " / " << n_iterPixelTrksInIterTobTecJet
//	      << " and " << n_iterTobTecTrks << " / " << n_iterPixelTrks << std::endl;

  // Calculate ratio of TOBTEC seeded tracks in "jet" to pixel seeded tracks in same region
  double ritertobtecjet = n_iterTobTecTrksInIterTobTecJet / n_iterPixelTrksInIterTobTecJet;

  if(m_filter) selected = ritertobtec > m_ratioAllCut && 
		 n_iterTobTecTrksInIterTobTecJet > m_absJetCut && 
		 ritertobtecjet > m_ratioJetCut;

  return selected;
}

// ------------ method called once each job just before starting event loop  ------------
void 
TobTecFakesFilter::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
TobTecFakesFilter::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(TobTecFakesFilter);
