// -*- C++ -*-
//
// Package:    MFVGenAnlzr
// Class:      MFVGenAnlzr
// 
/**\class MFVGenAnlzr MFVGenAnlzr.cc MFVAnal/MFVGenAnlzr/src/MFVGenAnlzr.cc

Description: [one line class summary]

Implementation:
[Notes on implementation]
*/
//
// Original Author:  Werner Sun
//         Created:  Thu Jan 31 12:20:09 CST 2013
// $Id$
//
//


// system include files
#include <memory>

// root
#include "TTree.h"
#include "TSystem.h"

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/METReco/interface/GenMET.h"
#include "DataFormats/METReco/interface/GenMETCollection.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "JMTucker/Tools/interface/MCInteractionMFV3j.h"
#include "JMTucker/Tools/interface/GenUtilities.h"
#include "PhysicsTools/CandUtils/interface/Thrust.h"
#include "PhysicsTools/CandUtils/interface/Thrust2D.h"

//
// class declaration
//

class MFVGenAnlzr : public edm::EDAnalyzer {
public:
  explicit MFVGenAnlzr(const edm::ParameterSet&);
  ~MFVGenAnlzr();

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  virtual void beginJob() ;
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;

  virtual void beginRun(edm::Run const&, edm::EventSetup const&);
  virtual void endRun(edm::Run const&, edm::EventSetup const&);
  virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
  virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

  void fillVecs( const reco::Candidate* genp, // initial candidate
		 TLorentzVector* p4,
		 TVector3* vtx,
		 const reco::Candidate* genpFinal = 0 ) ; // final candidate (used for b's)

  void fillGenParticleVec( std::vector< reco::GenParticle >& vec,
 			   const reco::GenParticle* genp,
			   bool ptNotP = false ) ;

  const reco::GenJet* matchedGenJet( const reco::GenParticle* genp,
				     const reco::GenJetCollection& genJets ) ;

  void fillGenJetVec( std::vector< reco::GenJet >& vec,
		      const reco::GenJet* genj,
		      bool ptNotP = false ) ;

  // ----------member data ---------------------------
  TTree * m_tree;

  TLorentzVector* m_p4GHad ;
  TLorentzVector* m_p4BgHad ;
  TLorentzVector* m_p4SHad ;
  TLorentzVector* m_p4THad ;
  TLorentzVector* m_p4BtHad ;
  TLorentzVector* m_p4Q0 ;
  TLorentzVector* m_p4Q1 ;
  TLorentzVector* m_p4GLep ;
  TLorentzVector* m_p4BgLep ;
  TLorentzVector* m_p4SLep ;
  TLorentzVector* m_p4TLep ;
  TLorentzVector* m_p4BtLep ;
  TLorentzVector* m_p4Lep ;
  TLorentzVector* m_p4Nu ;

  TVector3* m_vtxGHad ;
  TVector3* m_vtxBgHad ;
  TVector3* m_vtxSHad ;
  TVector3* m_vtxTHad ;
  TVector3* m_vtxBtHad ;
  TVector3* m_vtxQ0 ;
  TVector3* m_vtxQ1 ;
  TVector3* m_vtxGLep ;
  TVector3* m_vtxBgLep ;
  TVector3* m_vtxSLep ;
  TVector3* m_vtxTLep ;
  TVector3* m_vtxBtLep ;
  TVector3* m_vtxLep ;
  TVector3* m_vtxNu ;

  TVector3* m_vthr3 ;
  Double_t m_thr3 ;
  TVector3* m_vthr2 ;
  Double_t m_thr2 ;

  TLorentzVector* m_p4jBgHad ;
  TLorentzVector* m_p4jSHad ;
  TLorentzVector* m_p4jBtHad ;
  TLorentzVector* m_p4jQ0 ;
  TLorentzVector* m_p4jQ1 ;
  TLorentzVector* m_p4jBgLep ;
  TLorentzVector* m_p4jSLep ;
  TLorentzVector* m_p4jBtLep ;
  TLorentzVector* m_p4MET ;

  TVector3* m_vthr3j ;
  Double_t m_thr3j ;
  TVector3* m_vthr2j ;
  Double_t m_thr2j ;

  std::vector< TLorentzVector >* m_vp4jQOther ;
  std::vector< TLorentzVector >* m_vp4jBOther ;
  std::vector< TVector3 >* m_vvtxQOther ;
  std::vector< TVector3 >* m_vvtxBOther ;

  TVector3* m_vthr3jAll ;
  Double_t m_thr3jAll ;
  TVector3* m_vthr2jAll ;
  Double_t m_thr2jAll ;

  TVector3* m_beamspot ;
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
MFVGenAnlzr::MFVGenAnlzr(const edm::ParameterSet& iConfig)

{
  //now do what ever initialization is needed

}


MFVGenAnlzr::~MFVGenAnlzr()
{
 
  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
MFVGenAnlzr::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;
  double ptCut = 30. ;
  double etaCut = 3. ;
//   double loosePtCut = 20. ;
//   double looseEtaCut = 3.5 ;
  double loosePtCut = 30. ;
  double looseEtaCut = 3. ;

  *m_p4GHad = TLorentzVector() ;
  *m_p4BgHad = TLorentzVector() ;
  *m_p4SHad = TLorentzVector() ;
  *m_p4THad = TLorentzVector() ;
  *m_p4BtHad = TLorentzVector() ;
  *m_p4Q0 = TLorentzVector() ;
  *m_p4Q1 = TLorentzVector() ;
  *m_p4GLep = TLorentzVector() ;
  *m_p4BgLep = TLorentzVector() ;
  *m_p4SLep = TLorentzVector() ;
  *m_p4TLep = TLorentzVector() ;
  *m_p4BtLep = TLorentzVector() ;
  *m_p4Lep = TLorentzVector() ;
  *m_p4Nu = TLorentzVector() ;

  *m_vtxGHad = TVector3() ;
  *m_vtxBgHad = TVector3() ;
  *m_vtxSHad = TVector3() ;
  *m_vtxTHad = TVector3() ;
  *m_vtxBtHad = TVector3() ;
  *m_vtxQ0 = TVector3() ;
  *m_vtxQ1 = TVector3() ;
  *m_vtxGLep = TVector3() ;
  *m_vtxBgLep = TVector3() ;
  *m_vtxSLep = TVector3() ;
  *m_vtxTLep = TVector3() ;
  *m_vtxBtLep = TVector3() ;
  *m_vtxLep = TVector3() ;
  *m_vtxNu = TVector3() ;

  *m_vthr3 = TVector3() ;
  m_thr3 = 0. ;
  *m_vthr2 = TVector3() ;
  m_thr2 = 0. ;

  *m_p4jBgHad = TLorentzVector() ;
  *m_p4jSHad = TLorentzVector() ;
  *m_p4jBtHad = TLorentzVector() ;
  *m_p4jQ0 = TLorentzVector() ;
  *m_p4jQ1 = TLorentzVector() ;
  *m_p4jBgLep = TLorentzVector() ;
  *m_p4jSLep = TLorentzVector() ;
  *m_p4jBtLep = TLorentzVector() ;
  *m_p4MET = TLorentzVector() ;

  *m_vthr3j = TVector3() ;
  m_thr3j = 0. ;
  *m_vthr2j = TVector3() ;
  m_thr2j = 0. ;

  m_vp4jQOther->clear() ;
  m_vp4jBOther->clear() ;
  m_vvtxQOther->clear() ;
  m_vvtxBOther->clear() ;

  *m_vthr3jAll = TVector3() ;
  m_thr3jAll = 0. ;
  *m_vthr2jAll = TVector3() ;
  m_thr2jAll = 0. ;

  Handle< reco::GenParticleCollection > genpHandle ;
  iEvent.getByLabel( "genParticles", genpHandle ) ; 
  Handle< reco::GenJetCollection > genJetHandle ;
  iEvent.getByLabel( "ak5GenJets", genJetHandle ) ;
  Handle< reco::GenMETCollection > genMetHandle ;
  iEvent.getByLabel( "genMetTrue", genMetHandle ) ;
  const reco::GenMET& genMet = genMetHandle->at( 0 ) ;

  std::vector< reco::GenParticle > thr3Cands ;
  std::vector< reco::GenJet > thr3jCands ;
  const reco::GenJet* jBgHad = 0 ;
  const reco::GenJet* jSHad = 0 ;
  const reco::GenJet* jBtHad = 0 ;
  const reco::GenJet* jQ0 = 0 ;
  const reco::GenJet* jQ1 = 0 ;
  const reco::GenJet* jBgLep = 0 ;
  const reco::GenJet* jSLep = 0 ;
  const reco::GenJet* jBtLep = 0 ;

  *m_beamspot = TVector3() ;

  // ~~~~~~~~~~ GenParticle ~~~~~~~~~~

  MCInteractionMFV3j mci ;
  mci.Init( *genpHandle, *genJetHandle, genMet ) ;
  if( mci.Valid() )
    {
      int ihad = ( mci.decay_type[ 0 ] == 3 ) ? 0 : 1 ;
      int ilep = 1 - ihad ;

      fillVecs( mci.lsps[ ihad ], m_p4GHad, m_vtxGHad ) ;
      fillVecs( mci.bottoms_init[ ihad ], m_p4BgHad, m_vtxBgHad, mci.bottoms[ ihad ] ) ;
      fillVecs( mci.stranges_init[ ihad ], m_p4SHad, m_vtxSHad ) ;
      fillVecs( mci.tops_init[ ihad ], m_p4THad, m_vtxTHad ) ;
      fillVecs( mci.bottoms_from_tops_init[ ihad ], m_p4BtHad, m_vtxBtHad,
		mci.bottoms_from_tops[ ihad ] ) ;
      fillVecs( mci.W_daughters_init[ ihad ][ 0 ], m_p4Q0, m_vtxQ0 ) ;
      fillVecs( mci.W_daughters_init[ ihad ][ 1 ], m_p4Q1, m_vtxQ1 ) ;
      fillVecs( mci.lsps[ ilep ], m_p4GLep, m_vtxGLep ) ;
      fillVecs( mci.bottoms_init[ ilep ], m_p4BgLep, m_vtxBgLep, mci.bottoms[ ilep ] ) ;
      fillVecs( mci.stranges_init[ ilep ], m_p4SLep, m_vtxSLep ) ;
      fillVecs( mci.tops_init[ ilep ], m_p4TLep, m_vtxTLep ) ;
      fillVecs( mci.bottoms_from_tops_init[ ilep ], m_p4BtLep, m_vtxBtLep,
		mci.bottoms_from_tops[ ilep ] ) ;
      fillVecs( mci.W_daughters_init[ ilep ][ 0 ], m_p4Lep, m_vtxLep ) ;
      fillVecs( mci.W_daughters_init[ ilep ][ 1 ], m_p4Nu, m_vtxNu ) ;

//       std::cout << "GHad " << mci.lsps[ ihad ]->vertex() << std::endl
// 		<< "BgHad " << mci.bottoms_init[ ihad ]->vertex() << std::endl
//  		<< "SHad " << mci.stranges_init[ ihad ]->vertex() << std::endl
// 		<< "THad " << mci.tops_init[ ihad ]->vertex() << std::endl
// 		<< "BtHad " << mci.bottoms_from_tops[ ihad ]->vertex() << std::endl
// 		<< "Q0 " << mci.W_daughters_init[ ihad ][ 0 ]->vertex() << std::endl
// 		<< "Q1 " << mci.W_daughters_init[ ihad ][ 1 ]->vertex() << std::endl
// 		<< "GLep " << mci.lsps[ ilep ]->vertex() << std::endl
// 		<< "BgLep " << mci.bottoms_init[ ilep ]->vertex() << std::endl
// 		<< "SLep " << mci.stranges_init[ ilep ]->vertex() << std::endl
// 		<< "TLep " << mci.tops_init[ ilep ]->vertex() << std::endl
// 		<< "BtLep " << mci.bottoms_from_tops[ ilep ]->vertex() << std::endl
// 		<< "Lep " << mci.W_daughters_init[ ilep ][ 0 ]->vertex() << std::endl
// 		<< "Nu " << mci.W_daughters_init[ ilep ][ 1 ]->vertex() << std::endl ;

      *m_beamspot = *m_vtxGHad ;

      fillGenParticleVec( thr3Cands, mci.bottoms_init[ ihad ] ) ;
      fillGenParticleVec( thr3Cands, mci.stranges_init[ ihad ] ) ;
      fillGenParticleVec( thr3Cands, mci.bottoms_from_tops_init[ ihad ] ) ;
      fillGenParticleVec( thr3Cands, mci.W_daughters_init[ ihad ][ 0 ] ) ;
      fillGenParticleVec( thr3Cands, mci.W_daughters_init[ ihad ][ 1 ] ) ;
      fillGenParticleVec( thr3Cands, mci.bottoms_init[ ilep ] ) ;
      fillGenParticleVec( thr3Cands, mci.stranges_init[ ilep ] ) ;
      fillGenParticleVec( thr3Cands, mci.bottoms_from_tops_init[ ilep ] ) ;
      fillGenParticleVec( thr3Cands, mci.W_daughters_init[ ilep ][ 0 ] ) ; // omit neutrino

      Thrust thr3Calc( thr3Cands.begin(), thr3Cands.end() ) ;
      Thrust::Vector vthr3 = thr3Calc.axis() ;
      m_vthr3->SetXYZ( vthr3.x(), vthr3.y(), vthr3.z() ) ;
      m_thr3 = thr3Calc.thrust() ;

      Thrust2D thr2Calc( thr3Cands.begin(), thr3Cands.end() ) ;
      Thrust::Vector vthr2 = thr2Calc.axis() ;
      m_vthr2->SetXYZ( vthr2.x(), vthr2.y(), vthr2.z() ) ;
      m_thr2 = thr2Calc.thrust() ;

      // ~~~~~~~~~~ Matched GenJets ~~~~~~~~~~

      // Find matching GenJets
      jBgHad = matchedGenJet( mci.bottoms_init[ ihad ], *genJetHandle ) ;
      jSHad = matchedGenJet( mci.stranges_init[ ihad ], *genJetHandle ) ;
      jBtHad = matchedGenJet( mci.bottoms_from_tops_init[ ihad ], *genJetHandle ) ;
      jQ0 = matchedGenJet( mci.W_daughters_init[ ihad ][ 0 ], *genJetHandle ) ;
      jQ1 = matchedGenJet( mci.W_daughters_init[ ihad ][ 1 ], *genJetHandle ) ;
      jBgLep = matchedGenJet( mci.bottoms_init[ ilep ], *genJetHandle ) ;
      jSLep = matchedGenJet( mci.stranges_init[ ilep ], *genJetHandle ) ;
      jBtLep = matchedGenJet( mci.bottoms_from_tops_init[ ilep ], *genJetHandle ) ;

      TVector3 vtxTmp ;
      fillVecs( jBgHad, m_p4jBgHad, &vtxTmp ) ;
      fillVecs( jSHad, m_p4jSHad, &vtxTmp ) ;
      fillVecs( jBtHad, m_p4jBtHad, &vtxTmp ) ;
      fillVecs( jQ0, m_p4jQ0, &vtxTmp ) ;
      fillVecs( jQ1, m_p4jQ1, &vtxTmp ) ;
      fillVecs( jBgLep, m_p4jBgLep, &vtxTmp ) ;
      fillVecs( jSLep, m_p4jSLep, &vtxTmp ) ;
      fillVecs( jBtLep, m_p4jBtLep, &vtxTmp ) ;

      m_p4MET->SetXYZT( genMet.px(),
			genMet.py(),
			0., // the met object has pz = px
			genMet.energy() ) ;

      fillGenJetVec( thr3jCands, jBgHad ) ;
      fillGenJetVec( thr3jCands, jSHad ) ;
      fillGenJetVec( thr3jCands, jBtHad ) ;
      fillGenJetVec( thr3jCands, jQ0 ) ;
      fillGenJetVec( thr3jCands, jQ1 ) ;
      fillGenJetVec( thr3jCands, jBgLep ) ;
      fillGenJetVec( thr3jCands, jSLep ) ;
      fillGenJetVec( thr3jCands, jBtLep ) ;

      // don't forget the lepton
      if( mci.W_daughters_init[ ilep ][ 0 ] )
	{
	  thr3jCands.push_back( reco::GenJet( mci.W_daughters_init[ ilep ][ 0 ]->p4(),
					      mci.W_daughters_init[ ilep ][ 0 ]->vertex(),
					      reco::GenJet::Specific(),
					      reco::Jet::Constituents() ) ) ;
	}

      Thrust thr3jCalc( thr3jCands.begin(), thr3jCands.end() ) ;
      Thrust::Vector vthr3j = thr3jCalc.axis() ;
      m_vthr3j->SetXYZ( vthr3j.x(), vthr3j.y(), vthr3j.z() ) ;
      m_thr3j = thr3jCalc.thrust() ;

      Thrust2D thr2jCalc( thr3jCands.begin(), thr3jCands.end() ) ;
      Thrust::Vector vthr2j = thr2jCalc.axis() ;
      m_vthr2j->SetXYZ( vthr2j.x(), vthr2j.y(), vthr2j.z() ) ;
      m_thr2j = thr2jCalc.thrust() ;
    }
  else
    {
      // Require one and only one lepton passing pt and eta cuts
      for( int i = 0, n = genpHandle->size() ; i < n ; ++i )
	{
	  const reco::GenParticle* genp = &genpHandle->at( i ) ;

	  if( fabs( genp->pdgId() ) == 6 ) // if not mfv signal sample, assume ttbar
	    {
	      m_beamspot->SetXYZ( genp->vx(),
				  genp->vy(),
				  genp->vz() ) ;
	    }
	  else if( is_lepton( genp ) &&
		   !is_neutrino( genp ) &&
		   genp->mother() &&
		   fabs( genp->mother()->pdgId() ) == 24 && // to get first copy of lepton
		   genp->pt() > ptCut &&
		   fabs( genp->eta() ) < etaCut )
	    {
	      if( thr3jCands.size() )
		{
		  // > 1 lepton, so discard event
		  return ;
		}
	      else
		{
		  fillVecs( genp, m_p4Lep, m_vtxLep ) ;
		  thr3jCands.push_back( reco::GenJet( genp->p4(),
						      genp->vertex(),
						      reco::GenJet::Specific(),
						      reco::Jet::Constituents() ) ) ;
		}
	    }
	}

      if( !thr3jCands.size() ) return ;
    }

  // ~~~~~~~~~~ All GenJets ~~~~~~~~~~

  // Find GenJets (passing pt and eta cuts) matched to generated
  // b quarks not from gluino decay
  std::vector< const reco::GenJet* > vbjOther ;
  std::vector< reco::GenJet > thr3jAllCands ;
  const reco::GenParticleCollection& vgenp = *genpHandle ;
  for( unsigned int i = 0, n = vgenp.size() ; i < n ; ++i )
    {
      if( fabs( vgenp[ i ].pdgId() ) == 5 &&
	  vgenp[ i ].mother() &&
	  fabs( vgenp[ i ].mother()->pdgId() ) != 5 &&
	  &( vgenp[ i ] ) != mci.bottoms_init[ 0 ] &&
	  &( vgenp[ i ] ) != mci.bottoms_init[ 1 ] &&
	  &( vgenp[ i ] ) != mci.bottoms_from_tops_init[ 0 ] &&
	  &( vgenp[ i ] ) != mci.bottoms_from_tops_init[ 1 ] )
	{
	  const reco::GenJet* match = matchedGenJet( &( vgenp[ i ] ),
						     *genJetHandle ) ;
	  if( match &&
	      match != jBgHad &&
	      match != jSHad &&
	      match != jBtHad &&
	      match != jQ0 &&
	      match != jQ1 &&
	      match != jBgLep &&
	      match != jSLep &&
	      match != jBtLep &&
	      match->pt() > loosePtCut &&
	      fabs( match->eta() ) < looseEtaCut )
	    {	   
	      vbjOther.push_back( match ) ;
	      fillGenJetVec( thr3jAllCands, match ) ;

	      TLorentzVector p4tmp ;
	      TVector3 vtxtmp ;
	      fillVecs( match, &p4tmp, &vtxtmp,
			final_candidate( match, 3 ) ) ;
	      m_vp4jBOther->push_back( p4tmp ) ;
	      m_vvtxBOther->push_back( vtxtmp ) ;
	    }
	}
    }

  // get the unmatched GenJets passing pt and eta cuts
  const reco::GenJetCollection& genJets = *genJetHandle ;
  for( unsigned int i = 0, n = genJets.size() ; i < n ; ++i )
    {
      const reco::GenJet* genJet = &( genJets[ i ] ) ;

      if( genJet != jBgHad &&
	  genJet != jSHad &&
	  genJet != jBtHad &&
	  genJet != jQ0 &&
	  genJet != jQ1 &&
	  genJet != jBgLep &&
	  genJet != jSLep &&
	  genJet != jBtLep &&
	  genJet->pt() > loosePtCut &&
	  fabs( genJet->eta() ) < looseEtaCut &&
	  find( vbjOther.begin(), vbjOther.end(), genJet ) == vbjOther.end() )
	{
	  fillGenJetVec( thr3jAllCands, genJet ) ;

	  TLorentzVector p4tmp ;
	  TVector3 vtxtmp ;
	  fillVecs( genJet, &p4tmp, &vtxtmp ) ;
	  m_vp4jQOther->push_back( p4tmp ) ;
	  //m_vvtxQOther->push_back( vtxtmp ) ; // always at origin
	  m_vvtxQOther->push_back( *m_beamspot ) ;
	}
    }

  // Calculate thrusts with all jets + lepton with pt and eta cuts
  for( int i = 0, n = thr3jCands.size() ; i < n ; ++i )
    {
      if( thr3jCands[ i ].pt() > ptCut &&
	  fabs( thr3jCands[ i ].eta() ) < etaCut )
	thr3jAllCands.push_back( thr3jCands[ i ] ) ;
    }

  // Add other jets to thrust calculations
  Thrust thr3jAllCalc( thr3jAllCands.begin(), thr3jAllCands.end() ) ;
  Thrust::Vector vthr3jAll = thr3jAllCalc.axis() ;
  m_vthr3jAll->SetXYZ( vthr3jAll.x(), vthr3jAll.y(), vthr3jAll.z() ) ;
  m_thr3jAll = thr3jAllCalc.thrust() ;

  Thrust2D thr2jAllCalc( thr3jAllCands.begin(), thr3jAllCands.end() ) ;
  Thrust::Vector vthr2jAll = thr2jAllCalc.axis() ;
  m_vthr2jAll->SetXYZ( vthr2jAll.x(), vthr2jAll.y(), vthr2jAll.z() ) ;
  m_thr2jAll = thr2jAllCalc.thrust() ;

//   m_beamspot->Print() ;
//   m_vtxSHad->Print() ;

  if( mci.Valid() ||
      ( m_vp4jQOther->size() > 2 && m_vp4jBOther->size() > 2 ) )
    m_tree->Fill() ;
}

void
MFVGenAnlzr::fillGenParticleVec( std::vector< reco::GenParticle >& vec,
				 const reco::GenParticle* genp,
				 bool ptNotP )
{
  if( !genp ) return ;
  reco::GenParticle tmp = *genp ;
  if( ptNotP ) tmp.setPz( 0. ) ;
  vec.push_back( tmp ) ;
}

void
MFVGenAnlzr::fillVecs( const reco::Candidate* genp, // initial
		       TLorentzVector* p4,
		       TVector3* vtx,
		       const reco::Candidate* genpFinal ) // for b's
{
  if( genp )
    {
      p4->SetXYZT( genp->px(),
		   genp->py(),
		   genp->pz(),
		   genp->energy() ) ;
      if( genpFinal )
	{
	  // get position of first non-b daughter
	  int ndau = genpFinal->numberOfDaughters() ;
	  for( int i = 0 ; i < ndau ; ++i )
	    {
	      const reco::Candidate* dau = genpFinal->daughter( i ) ;
	      int dauId = abs( dau->pdgId() ) ;

	      if( dauId != 5 )
		{
		  // If dau is a B hadron, get its first daughter
		  if( dauId > 10000 ) dauId = dauId % 10000 ;

		  while( ( dauId < 1000 && ( int ) ( dauId / 100 ) == 5 ) ||
			 ( dauId > 1000 && ( int ) ( dauId / 1000 ) == 5 ) )
		    {
		      dau = final_candidate( dau, 3 ) ;
		      int ndau2 = dau->numberOfDaughters() ;
		      for( int j = 0 ; j < ndau2 ; ++j )
			{
			  const reco::Candidate* dau2 = dau->daughter( i ) ;
			  if( abs( dau2->pdgId() ) != dauId )
			    {
			      dau = dau2 ;
			      dauId = abs( dau->pdgId() ) ;
			      if( dauId > 10000 ) dauId = dauId % 10000 ;
			      break ;
			    }
			}
		    }

		  vtx->SetXYZ( dau->vx(),
			       dau->vy(),
			       dau->vz() ) ;
		  break ;
		}
	    }
	}
      else
	{
	  vtx->SetXYZ( genp->vx(),
		       genp->vy(),
		       genp->vz() ) ;
	}
    }
  else
    {
      *p4 = TLorentzVector() ;
      *vtx = TVector3() ;
    }
}

// Find closest GenJet
const reco::GenJet*
MFVGenAnlzr::matchedGenJet( const reco::GenParticle* genp,
			    const reco::GenJetCollection& genJets )
{
  const reco::GenJet* matchedGenJet = 0 ;

  if( genp )
    {
      // Find closest GenJet with dR < 0.4
      double bestDR = 999. ;
      for( unsigned int i = 0 ; i < genJets.size() ; ++i )
	{
	  double dR = deltaR( genp->p4(), genJets[ i ].p4() ) ;
	  if( dR < 0.4 && dR < bestDR )
	    {
	      matchedGenJet = &( genJets[ i ] ) ;
	      bestDR = dR ;
	    }
	}
    }

  return matchedGenJet ;
}

void
MFVGenAnlzr::fillGenJetVec( std::vector< reco::GenJet >& vec,
			    const reco::GenJet* genj,
			    bool ptNotP )
{
  if( !genj ) return ;
  reco::GenJet tmp = *genj ;
  if( ptNotP ) tmp.setPz( 0. ) ;
  vec.push_back( tmp ) ;
}

// ------------ method called once each job just before starting event loop  ------------
void 
MFVGenAnlzr::beginJob()
{
  gSystem->Load( "./dict_C.so" ) ;

  edm::Service< TFileService > fs ;
  m_tree = fs->make< TTree >( "tree", "thetree" ) ;

  m_p4GHad = new TLorentzVector ;
  m_p4BgHad = new TLorentzVector ;
  m_p4SHad = new TLorentzVector ;
  m_p4THad = new TLorentzVector ;
  m_p4BtHad = new TLorentzVector ;
  m_p4Q0 = new TLorentzVector ;
  m_p4Q1 = new TLorentzVector ;
  m_p4GLep = new TLorentzVector ;
  m_p4BgLep = new TLorentzVector ;
  m_p4SLep = new TLorentzVector ;
  m_p4TLep = new TLorentzVector ;
  m_p4BtLep = new TLorentzVector ;
  m_p4Lep = new TLorentzVector ;
  m_p4Nu = new TLorentzVector ;

  m_vtxGHad = new TVector3 ;
  m_vtxBgHad = new TVector3 ;
  m_vtxSHad = new TVector3 ;
  m_vtxTHad = new TVector3 ;
  m_vtxBtHad = new TVector3 ;
  m_vtxQ0 = new TVector3 ;
  m_vtxQ1 = new TVector3 ;
  m_vtxGLep = new TVector3 ;
  m_vtxBgLep = new TVector3 ;
  m_vtxSLep = new TVector3 ;
  m_vtxTLep = new TVector3 ;
  m_vtxBtLep = new TVector3 ;
  m_vtxLep = new TVector3 ;
  m_vtxNu = new TVector3 ;

  m_vthr3 = new TVector3 ;
  m_vthr2 = new TVector3 ;

  m_p4jBgHad = new TLorentzVector ;
  m_p4jSHad = new TLorentzVector ;
  m_p4jBtHad = new TLorentzVector ;
  m_p4jQ0 = new TLorentzVector ;
  m_p4jQ1 = new TLorentzVector ;
  m_p4jBgLep = new TLorentzVector ;
  m_p4jSLep = new TLorentzVector ;
  m_p4jBtLep = new TLorentzVector ;
  m_p4MET = new TLorentzVector ;

  m_vthr3j = new TVector3 ;
  m_vthr2j = new TVector3 ;

  m_vp4jQOther = new std::vector< TLorentzVector > ;
  m_vp4jBOther = new std::vector< TLorentzVector > ;
  m_vvtxQOther = new std::vector< TVector3 > ;
  m_vvtxBOther = new std::vector< TVector3 > ;

  m_vthr3jAll = new TVector3 ;
  m_vthr2jAll = new TVector3 ;

  m_beamspot = new TVector3 ;

  m_tree->Branch( "p4GHad", &m_p4GHad ) ;
  m_tree->Branch( "p4BgHad", &m_p4BgHad ) ;
  m_tree->Branch( "p4SHad", &m_p4SHad ) ;
  m_tree->Branch( "p4THad", &m_p4THad ) ;
  m_tree->Branch( "p4BtHad", &m_p4BtHad ) ;
  m_tree->Branch( "p4Q0", &m_p4Q0 ) ;
  m_tree->Branch( "p4Q1", &m_p4Q1 ) ;
  m_tree->Branch( "p4GLep", &m_p4GLep ) ;
  m_tree->Branch( "p4BgLep", &m_p4BgLep ) ;
  m_tree->Branch( "p4SLep", &m_p4SLep ) ;
  m_tree->Branch( "p4TLep", &m_p4TLep ) ;
  m_tree->Branch( "p4BtLep", &m_p4BtLep ) ;
  m_tree->Branch( "p4Lep", &m_p4Lep ) ;
  m_tree->Branch( "p4Nu", &m_p4Nu ) ;

  m_tree->Branch( "vtxGHad", &m_vtxGHad ) ;
  m_tree->Branch( "vtxBgHad", &m_vtxBgHad ) ;
  m_tree->Branch( "vtxSHad", &m_vtxSHad ) ;
  m_tree->Branch( "vtxTHad", &m_vtxTHad ) ;
  m_tree->Branch( "vtxBtHad", &m_vtxBtHad ) ;
  m_tree->Branch( "vtxQ0", &m_vtxQ0 ) ;
  m_tree->Branch( "vtxQ1", &m_vtxQ1 ) ;
  m_tree->Branch( "vtxGLep", &m_vtxGLep ) ;
  m_tree->Branch( "vtxBgLep", &m_vtxBgLep ) ;
  m_tree->Branch( "vtxSLep", &m_vtxSLep ) ;
  m_tree->Branch( "vtxTLep", &m_vtxTLep ) ;
  m_tree->Branch( "vtxBtLep", &m_vtxBtLep ) ;
  m_tree->Branch( "vtxLep", &m_vtxLep ) ;
  m_tree->Branch( "vtxNu", &m_vtxNu ) ;

  m_tree->Branch( "vthr3", &m_vthr3 ) ;
  m_tree->Branch( "thr3", &m_thr3, "thr3/D" ) ;
  m_tree->Branch( "vthr2", &m_vthr2 ) ;
  m_tree->Branch( "thr2", &m_thr2, "thr2/D" ) ;

  m_tree->Branch( "p4jBgHad", &m_p4jBgHad ) ;
  m_tree->Branch( "p4jSHad", &m_p4jSHad ) ;
  m_tree->Branch( "p4jBtHad", &m_p4jBtHad ) ;
  m_tree->Branch( "p4jQ0", &m_p4jQ0 ) ;
  m_tree->Branch( "p4jQ1", &m_p4jQ1 ) ;
  m_tree->Branch( "p4jBgLep", &m_p4jBgLep ) ;
  m_tree->Branch( "p4jSLep", &m_p4jSLep ) ;
  m_tree->Branch( "p4jBtLep", &m_p4jBtLep ) ;
  m_tree->Branch( "p4MET", &m_p4MET ) ;

  m_tree->Branch( "vthr3j", &m_vthr3j ) ;
  m_tree->Branch( "thr3j", &m_thr3j, "thr3j/D" ) ;
  m_tree->Branch( "vthr2j", &m_vthr2j ) ;
  m_tree->Branch( "thr2j", &m_thr2j, "thr2j/D" ) ;

  m_tree->Branch( "vp4jQOther", &m_vp4jQOther, 32000, 0 ) ;
  m_tree->Branch( "vp4jBOther", &m_vp4jBOther, 32000, 0 ) ;
  m_tree->Branch( "vvtxQOther", &m_vvtxQOther, 32000, 0 ) ;
  m_tree->Branch( "vvtxBOther", &m_vvtxBOther, 32000, 0 ) ;

  m_tree->Branch( "vthr3jAll", &m_vthr3jAll ) ;
  m_tree->Branch( "thr3jAll", &m_thr3jAll, "thr3jAll/D" ) ;
  m_tree->Branch( "vthr2jAll", &m_vthr2jAll ) ;
  m_tree->Branch( "thr2jAll", &m_thr2jAll, "thr2jAll/D" ) ;

  m_tree->Branch( "beamspot", &m_beamspot ) ;
}

// ------------ method called once each job just after ending the event loop  ------------
void 
MFVGenAnlzr::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
void 
MFVGenAnlzr::beginRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
MFVGenAnlzr::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
MFVGenAnlzr::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
MFVGenAnlzr::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
MFVGenAnlzr::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(MFVGenAnlzr);
