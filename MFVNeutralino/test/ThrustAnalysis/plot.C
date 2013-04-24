// root -b plot.C+

#include "TSystem.h"
#include "TStyle.h"
#include "TLorentzVector.h"
#include "TVector3.h"
#include "TVector2.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TTree.h"
#include "TFile.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TRandom3.h"

#include <stdio.h>
#include <iostream>

// return value is hemisphere wrt thrust axis
int fillHSCounts( double cosThrBg, double cosThrS, double cosThrBt,
		  double cosThrWdau0, double cosThrWdau1,
		  TH1F* h_nss, TH1F* h_ws ) ;

void sortByP( const TVector3* vthr,
	      int hsLep, const TLorentzVector* p4,
	      std::vector< const TLorentzVector* >& vHad,
	      std::vector< const TLorentzVector* >& vLep ) ;

void sortByX( const TVector3* vthr,
	      const TVector3* vtx, const TVector3* beamspot,
	      int hsLep, const TLorentzVector* p4,
	      std::vector< const TLorentzVector* >& vHad,
	      std::vector< const TLorentzVector* >& vLep ) ;

void combine( const std::vector< const TLorentzVector* >& vb,
	      const std::vector< const TLorentzVector* >& vq,
	      TH1F* histAll, TH1F* histCand,
	      const TLorentzVector* p4Lep,
	      const TLorentzVector* p4MET,
	      TH1F** diagHists = 0 ) ;

// Use W mass constraint to solve for neutrino pz (up to sign ambiguity).
// Return the neutrino 4-momentum that gives the W the smaller |eta|.
// Returns false if no solution.
bool p4NuCons( const TLorentzVector* p4Lep,
	       const TLorentzVector* p4MET,
	       TLorentzVector& p4Nu,
	       TH1F** diagHists = 0 ) ;

void makeNice( TH1F* h, int color ) ;
void drawSinglet( TH1F* h0, const char* title,
		  TCanvas* canvas, const char* filename ) ;
void drawPair( TH1F* h0, TH1F* h1,
	       const char* title, const char* label0, const char* label1,
	       TCanvas* canvas, const char* filename ) ;
void drawTriplet( TH1F* h0, TH1F* h1, TH1F* h2,
		  TCanvas* canvas, const char* filename ) ;

void plot()
{
  const char* inputFile = "thrust.root";

  gSystem->Load( "./dict_C.so" ) ;

  // Initialize random engine
  TRandom3 rndeng( 0 ) ;

  TFile* f = TFile::Open( inputFile ) ;
  TTree* tree = ( TTree* ) f->Get( "thrustNtuple/tree" ) ;
  cout << tree->GetEntries() << endl ;

  // ~~~~~~~~~~ Set branches ~~~~~~~~~~

  TLorentzVector* p4jBgHad  = new TLorentzVector ;
  tree->SetBranchAddress( "p4jBgHad", &p4jBgHad ) ;
  TLorentzVector* p4jSHad  = new TLorentzVector ;
  tree->SetBranchAddress( "p4jSHad", &p4jSHad ) ;
  TLorentzVector* p4jBtHad  = new TLorentzVector ;
  tree->SetBranchAddress( "p4jBtHad", &p4jBtHad ) ;
  TLorentzVector* p4jQ0  = new TLorentzVector ;
  tree->SetBranchAddress( "p4jQ0", &p4jQ0 ) ;
  TLorentzVector* p4jQ1  = new TLorentzVector ;
  tree->SetBranchAddress( "p4jQ1", &p4jQ1 ) ;
  TLorentzVector* p4jBgLep  = new TLorentzVector ;
  tree->SetBranchAddress( "p4jBgLep", &p4jBgLep ) ;
  TLorentzVector* p4jSLep  = new TLorentzVector ;
  tree->SetBranchAddress( "p4jSLep", &p4jSLep ) ;
  TLorentzVector* p4jBtLep  = new TLorentzVector ;
  tree->SetBranchAddress( "p4jBtLep", &p4jBtLep ) ;
  TLorentzVector* p4Lep  = new TLorentzVector ;
  tree->SetBranchAddress( "p4Lep", &p4Lep ) ;

  TVector3* vtxBgHad  = new TVector3 ;
  tree->SetBranchAddress( "vtxBgHad", &vtxBgHad ) ;
  TVector3* vtxSHad  = new TVector3 ;
  tree->SetBranchAddress( "vtxSHad", &vtxSHad ) ;
  TVector3* vtxBtHad  = new TVector3 ;
  tree->SetBranchAddress( "vtxBtHad", &vtxBtHad ) ;
  TVector3* vtxQ0  = new TVector3 ;
  tree->SetBranchAddress( "vtxQ0", &vtxQ0 ) ;
  TVector3* vtxQ1  = new TVector3 ;
  tree->SetBranchAddress( "vtxQ1", &vtxQ1 ) ;
  TVector3* vtxBgLep  = new TVector3 ;
  tree->SetBranchAddress( "vtxBgLep", &vtxBgLep ) ;
  TVector3* vtxSLep  = new TVector3 ;
  tree->SetBranchAddress( "vtxSLep", &vtxSLep ) ;
  TVector3* vtxBtLep  = new TVector3 ;
  tree->SetBranchAddress( "vtxBtLep", &vtxBtLep ) ;
  TVector3* vtxLep  = new TVector3 ;
  tree->SetBranchAddress( "vtxLep", &vtxLep ) ;

  TLorentzVector* p4MET  = new TLorentzVector ;
  tree->SetBranchAddress( "p4MET", &p4MET ) ;

  std::vector< TLorentzVector >* vp4jQOther =
    new std::vector< TLorentzVector > ;
  tree->SetBranchAddress( "vp4jQOther", &vp4jQOther ) ;
  std::vector< TLorentzVector >* vp4jBOther =
    new std::vector< TLorentzVector > ;
  tree->SetBranchAddress( "vp4jBOther", &vp4jBOther ) ;
  std::vector< TVector3 >* vvtxQOther = new std::vector< TVector3 > ;
  tree->SetBranchAddress( "vvtxQOther", &vvtxQOther ) ;
  std::vector< TVector3 >* vvtxBOther = new std::vector< TVector3 > ;
  tree->SetBranchAddress( "vvtxBOther", &vvtxBOther ) ;

  TVector3* vthr3jAll = new TVector3 ;
  tree->SetBranchAddress( "vthr3jAll", &vthr3jAll ) ;
  Double_t thr3jAll ;
  tree->SetBranchAddress( "thr3jAll", &thr3jAll ) ;
  TVector3* vthr2jAll = new TVector3 ;
  tree->SetBranchAddress( "vthr2jAll", &vthr2jAll ) ;
  Double_t thr2jAll ;
  tree->SetBranchAddress( "thr2jAll", &thr2jAll ) ;

  TVector3* beamspot = new TVector3 ;
  tree->SetBranchAddress( "beamspot", &beamspot ) ;

  // ~~~~~~~~~~ Book histograms ~~~~~~~~~~

  TH1F* h_beamspot = new TH1F( "h_beamspot", "beamspot", 100, 0., 1. ) ;
  TH1F* h_vtxqMatched = new TH1F( "h_vtxqMatched", "vtx q matched", 100, 0., 1. ) ;
  TH1F* h_vtxbMatched = new TH1F( "h_vtxbMatched", "vtx b matched", 100, 0., 1. ) ;
  TH1F* h_vtxqUnmatched = new TH1F( "h_vtxqUnmatched", "vtx q unmatched", 100, 0., 1. ) ;
  TH1F* h_vtxbUnmatched = new TH1F( "h_vtxbUnmatched", "vtx b unmatched", 100, 0., 1. ) ;

  // thrust 3D (GenJets)
  TH1F* h_vthr3jPhi = new TH1F( "h_vthr3jPhi", "thr3j phi",
				50, -TMath::Pi(), TMath::Pi() ) ;
  TH1F* h_vthr3jCosth = new TH1F( "h_vthr3jCosth", "thr3j cosTh", 50, 0., 1. ) ;
  TH2F* h_vthr3jPhiCosth = new TH2F( "h_vthr3jPhiCosth", "thr3j phi v costh",
				     25, -TMath::Pi(), TMath::Pi(),
				     25, 0., 1. ) ;
  TH1F* h_thr3j = new TH1F( "h_thr3j", "thr3j", 50, 0., 1. ) ;
  TH2F* h_thr3jVsPhi = new TH2F( "h_thr3jVsPhi", "thr3j v phi",
				 25, 0.5, 1.,
				 25, -TMath::Pi(), TMath::Pi() ) ;
  TH2F* h_thr3jVsCosth = new TH2F( "h_thr3jVsCosth", "thr3j v costh",
				   25, 0.5, 1.,
				   25, 0., 1. ) ;

  // thrust 2D (GenJets)
  TH1F* h_vthr2jPhi = new TH1F( "h_vthr2jPhi", "thr2j phi",
				50, -TMath::Pi(), TMath::Pi() ) ;
  TH1F* h_vthr2jCosth = new TH1F( "h_vthr2jCosth", "thr2j cosTh", 50, 0., 1. ) ;
  TH2F* h_vthr2jPhiCosth = new TH2F( "h_vthr2jPhiCosth", "thr2j phi v costh",
				     25, -TMath::Pi(), TMath::Pi(),
				     25, 0., 1. ) ;
  TH1F* h_thr2j = new TH1F( "h_thr2j", "thr2j", 50, 0., 1. ) ;
  TH2F* h_thr2jVsPhi = new TH2F( "h_thr2jVsPhi", "thr2j v phi",
				 25, 0.5, 1.,
				 25, -TMath::Pi(), TMath::Pi() ) ;
  TH2F* h_thr2jVsCosth = new TH2F( "h_thr2jVsCosth", "thr2j v costh",
				   25, 0.5, 1.,
				   25, 0., 1. ) ;

  // Diff between 3D and 2D thrust
  TH1F* h_thr32jCosDPhi = new TH1F( "h_thr32jCosDPhi", "thr32jCosDPhi", 50, -1, 1. ) ;

  // # jets
  TH1F* h_nqMatched = new TH1F( "h_nqMatched", "#q matched", 15, -0.5, 14.5 ) ;
  TH1F* h_nbMatched = new TH1F( "h_nbMatched", "#b matched", 15, -0.5, 14.5 ) ;
  TH1F* h_nqUnmatched = new TH1F( "h_nqUnmatched", "#q unmatched", 15, -0.5, 14.5 ) ;
  TH1F* h_nbUnmatched = new TH1F( "h_nbUnmatched", "#b unmatched", 15, -0.5, 14.5 ) ;

  TH1F* h_nqHad3Pj = new TH1F( "h_nqHad3Pj", "#q", 8, -0.5, 7.5 ) ;
  TH1F* h_nqLep3Pj = new TH1F( "h_nqLep3Pj", "#q", 8, -0.5, 7.5 ) ;
  TH1F* h_nbHad3Pj = new TH1F( "h_nbHad3Pj", "#b", 8, -0.5, 7.5 ) ;
  TH1F* h_nbLep3Pj = new TH1F( "h_nbLep3Pj", "#b", 8, -0.5, 7.5 ) ;
  TH1F* h_nqHad3Xj = new TH1F( "h_nqHad3Xj", "#q", 8, -0.5, 7.5 ) ;
  TH1F* h_nqLep3Xj = new TH1F( "h_nqLep3Xj", "#q", 8, -0.5, 7.5 ) ;
  TH1F* h_nbHad3Xj = new TH1F( "h_nbHad3Xj", "#b", 8, -0.5, 7.5 ) ;
  TH1F* h_nbLep3Xj = new TH1F( "h_nbLep3Xj", "#b", 8, -0.5, 7.5 ) ;

  TH2F* h_nqHadLep3Pj = new TH2F( "h_nqHadLep3Pj", "nqHadLep3Pj", 8, -0.5, 7.5,
				  8, -0.5, 7.5 ) ;
  TH2F* h_nbHadLep3Pj = new TH2F( "h_nbHadLep3Pj", "nbHadLep3Pj", 8, -0.5, 7.5,
				  8, -0.5, 7.5 ) ;
  TH2F* h_nqHadLep3Xj = new TH2F( "h_nqHadLep3Xj", "nqHadLep3Xj", 8, -0.5, 7.5,
				  8, -0.5, 7.5 ) ;
  TH2F* h_nbHadLep3Xj = new TH2F( "h_nbHadLep3Xj", "nbHadLep3Xj", 8, -0.5, 7.5,
				  8, -0.5, 7.5 ) ;

  // invariant masses (GenJets)
  TH1F* h_mhadhsThr3jPj = new TH1F( "h_mhadhsThr3jPj", "M(HS) had thr3 by p", 25, 0., 1000. ) ;
  TH1F* h_mlephsThr3jPj = new TH1F( "h_mlephsThr3jPj", "M(HS) lep thr3 by p", 25, 0., 1000. ) ;
  TH1F* h_mhadhsThr3jXj = new TH1F( "h_mhadhsThr3jXj", "M(HS) had thr3 by x", 25, 0., 1000. ) ;
  TH1F* h_mlephsThr3jXj = new TH1F( "h_mlephsThr3jXj", "M(HS) lep thr3 by x", 25, 0., 1000. ) ;
  TH1F* h_mhadThr3jPj = new TH1F( "h_mhadThr3jPj", "M(LSP) had thr3 by p", 25, 0., 1000. ) ;
  TH1F* h_mlepThr3jPj = new TH1F( "h_mlepThr3jPj", "M(LSP) lep thr3 by p", 25, 0., 1000. ) ;
  TH1F* h_mhadThr3jXj = new TH1F( "h_mhadThr3jXj", "M(LSP) had thr3 by x", 25, 0., 1000. ) ;
  TH1F* h_mlepThr3jXj = new TH1F( "h_mlepThr3jXj", "M(LSP) lep thr3 by x", 25, 0., 1000. ) ;
  TH1F* h_mhadhsThr2jPj = new TH1F( "h_mhadhsThr2jPj", "M(HS) had thr2 by p", 25, 0., 1000. ) ;
  TH1F* h_mlephsThr2jPj = new TH1F( "h_mlephsThr2jPj", "M(HS) lep thr2 by p", 25, 0., 1000. ) ;
  TH1F* h_mhadhsThr2jXj = new TH1F( "h_mhadhsThr2jXj", "M(HS) had thr2 by x", 25, 0., 1000. ) ;
  TH1F* h_mlephsThr2jXj = new TH1F( "h_mlephsThr2jXj", "M(HS) lep thr2 by x", 25, 0., 1000. ) ;
  TH1F* h_mhadThr2jPj = new TH1F( "h_mhadThr2jPj", "M(LSP) had thr2 by p", 25, 0., 1000. ) ;
  TH1F* h_mlepThr2jPj = new TH1F( "h_mlepThr2jPj", "M(LSP) lep thr2 by p", 25, 0., 1000. ) ;
  TH1F* h_mhadThr2jXj = new TH1F( "h_mhadThr2jXj", "M(LSP) had thr2 by x", 25, 0., 1000. ) ;
  TH1F* h_mlepThr2jXj = new TH1F( "h_mlepThr2jXj", "M(LSP) lep thr2 by x", 25, 0., 1000. ) ;

  // diagnostic plots
//   TH1F* h_etaWCons = new TH1F( "h_etaWCons", "eta(W), both solutions", 25, -5., 5. ) ;
//   TH1F* h_etaDiffWCons = new TH1F( "h_etaDiffWCons", "|eta(W0)|-|eta(W1)|", 25, -10., 10. ) ;
//   TH1F* h_mtLep = new TH1F( "h_mtLep", "right mt for leptonic G", 25, 0., 750. ) ;
//   TH1F* h_mtDiffLep = new TH1F( "h_mtDiffLep", "delta mt for leptonic G", 25, -500., 500. ) ;
//   TH1F* h_ncombHad = new TH1F( "h_ncombHad", "# combinations had", 25, -0.5, 24.5 ) ;
//   TH1F* h_ncombLep = new TH1F( "h_ncombLep", "# combinations lep", 25, -0.5, 24.5 ) ;

  // ~~~~~~~~~~ Loop over events ~~~~~~~~~~

  double ptCut = 30. ;
  double etaCut = 3. ;
  double vtxqCut = 0.01 ; // cm
  //double vtxqCut = 0.001 ; // cm

  for( int iev = 0 ; iev < tree->GetEntries() ; ++iev )
    {
      tree->GetEntry( iev ) ;

      if( !( p4Lep->Pt() > ptCut &&
	     fabs( p4Lep->Eta() ) < etaCut ) )
	continue ;

      TVector2 v2thr3j( vthr3jAll->X(), vthr3jAll->Y() ) ;
      v2thr3j = v2thr3j.Unit() ;
      TVector2 v2thr2j( vthr2jAll->X(), vthr2jAll->Y() ) ;
      v2thr2j = v2thr2j.Unit() ;

      h_thr32jCosDPhi->Fill( v2thr3j * v2thr2j ) ;

      h_vthr3jPhi->Fill( vthr3jAll->Phi() ) ;
      h_vthr3jCosth->Fill( vthr3jAll->CosTheta() ) ;
      h_vthr3jPhiCosth->Fill( vthr3jAll->Phi(), vthr3jAll->CosTheta() ) ;
      h_thr3j->Fill( thr3jAll ) ;
      h_thr3jVsPhi->Fill( thr3jAll, vthr3jAll->Phi() ) ;
      h_thr3jVsCosth->Fill( thr3jAll, vthr3jAll->CosTheta() ) ;

      h_vthr2jPhi->Fill( vthr2jAll->Phi() ) ;
      h_vthr2jCosth->Fill( vthr2jAll->CosTheta() ) ;
      h_vthr2jPhiCosth->Fill( vthr2jAll->Phi(), vthr2jAll->CosTheta() ) ;
      h_thr2j->Fill( thr2jAll ) ;
      h_thr2jVsPhi->Fill( thr2jAll, vthr2jAll->Phi() ) ;
      h_thr2jVsCosth->Fill( thr2jAll, vthr2jAll->CosTheta() ) ;
	
      double hsLep3Pj = vthr3jAll->X() * p4Lep->X() + vthr3jAll->Y() * p4Lep->Y() > 0. ?
	1 : -1 ;
      double hsLep2Pj = vthr2jAll->X() * p4Lep->X() + vthr2jAll->Y() * p4Lep->Y() > 0. ?
	1 : -1 ;
      double hsLep3Xj = vthr3jAll->X() * ( vtxLep->X() - beamspot->X() ) +
	vthr3jAll->Y() * ( vtxLep->Y() - beamspot->Y() ) > 0. ?	1 : -1 ;
      double hsLep2Xj = vthr2jAll->X() * ( vtxLep->X() - beamspot->X() ) +
	vthr2jAll->Y() * ( vtxLep->Y() - beamspot->Y() ) > 0. ?	1 : -1 ;

      std::vector< const TLorentzVector* > vbHad3Pj, vbLep3Pj, vqHad3Pj, vqLep3Pj ;
      std::vector< const TLorentzVector* > vbHad2Pj, vbLep2Pj, vqHad2Pj, vqLep2Pj ;
      std::vector< const TLorentzVector* > vbHad3Xj, vbLep3Xj, vqHad3Xj, vqLep3Xj ;
      std::vector< const TLorentzVector* > vbHad2Xj, vbLep2Xj, vqHad2Xj, vqLep2Xj ;

      int nq = 0 ;
      int nb = 0 ;

      h_beamspot->Fill( beamspot->Perp() ) ;

      if( p4jBgHad->Pt() > ptCut &&
	  fabs( p4jBgHad->Eta() ) < etaCut )
	{
	  ++nb ;
	  sortByP( vthr3jAll, hsLep3Pj, p4jBgHad, vbHad3Pj, vbLep3Pj ) ;
	  sortByP( vthr2jAll, hsLep2Pj, p4jBgHad, vbHad2Pj, vbLep2Pj ) ;
	  sortByX( vthr3jAll, vtxBgHad, beamspot, hsLep3Xj, p4jBgHad, vbHad3Xj, vbLep3Xj ) ;
	  sortByX( vthr2jAll, vtxBgHad, beamspot, hsLep2Xj, p4jBgHad, vbHad2Xj, vbLep2Xj ) ;
	  h_vtxbMatched->Fill( ( *vtxBgHad - *beamspot ).Perp() ) ;
	}
      if( p4jSHad->Pt() > ptCut &&
          fabs( p4jSHad->Eta() ) < etaCut &&
	  ( *vtxSHad - *beamspot ).Perp() > vtxqCut )
	{
	  ++nq ;
	  sortByP( vthr3jAll, hsLep3Pj, p4jSHad, vqHad3Pj, vqLep3Pj ) ;
	  sortByP( vthr2jAll, hsLep2Pj, p4jSHad, vqHad2Pj, vqLep2Pj ) ;
	  sortByX( vthr3jAll, vtxSHad, beamspot, hsLep3Xj, p4jSHad, vqHad3Xj, vqLep3Xj ) ;
	  sortByX( vthr2jAll, vtxSHad, beamspot, hsLep2Xj, p4jSHad, vqHad2Xj, vqLep2Xj ) ;
	  h_vtxqMatched->Fill( ( *vtxSHad - *beamspot ).Perp() ) ;
	}
      if( p4jBtHad->Pt() > ptCut &&
          fabs( p4jBtHad->Eta() ) < etaCut )
	{
	  ++nb ;
	  sortByP( vthr3jAll, hsLep3Pj, p4jBtHad, vbHad3Pj, vbLep3Pj ) ;
	  sortByP( vthr2jAll, hsLep2Pj, p4jBtHad, vbHad2Pj, vbLep2Pj ) ;
	  sortByX( vthr3jAll, vtxBtHad, beamspot, hsLep3Xj, p4jBtHad, vbHad3Xj, vbLep3Xj ) ;
	  sortByX( vthr2jAll, vtxBtHad, beamspot, hsLep2Xj, p4jBtHad, vbHad2Xj, vbLep2Xj ) ;
	  h_vtxbMatched->Fill( ( *vtxBtHad - *beamspot ).Perp() ) ;
	}
      if( p4jQ0->Pt() > ptCut &&
          fabs( p4jQ0->Eta() ) < etaCut &&
	  ( *vtxQ0 - *beamspot ).Perp() > vtxqCut )
	{
	  ++nq ;
	  sortByP( vthr3jAll, hsLep3Pj, p4jQ0, vqHad3Pj, vqLep3Pj ) ;
	  sortByP( vthr2jAll, hsLep2Pj, p4jQ0, vqHad2Pj, vqLep2Pj ) ;
	  sortByX( vthr3jAll, vtxQ0, beamspot, hsLep3Xj, p4jQ0, vqHad3Xj, vqLep3Xj ) ;
	  sortByX( vthr2jAll, vtxQ0, beamspot, hsLep2Xj, p4jQ0, vqHad2Xj, vqLep2Xj ) ;
	  h_vtxqMatched->Fill( ( *vtxQ0 - *beamspot ).Perp() ) ;
	}
      if( p4jQ1->Pt() > ptCut &&
          fabs( p4jQ1->Eta() ) < etaCut &&
	  ( *vtxQ1 - *beamspot ).Perp() > vtxqCut )
	{
	  ++nq ;
	  sortByP( vthr3jAll, hsLep3Pj, p4jQ1, vqHad3Pj, vqLep3Pj ) ;
	  sortByP( vthr2jAll, hsLep2Pj, p4jQ1, vqHad2Pj, vqLep2Pj ) ;
	  sortByX( vthr3jAll, vtxQ1, beamspot, hsLep3Xj, p4jQ1, vqHad3Xj, vqLep3Xj ) ;
	  sortByX( vthr2jAll, vtxQ1, beamspot, hsLep2Xj, p4jQ1, vqHad2Xj, vqLep2Xj ) ;
	  h_vtxqMatched->Fill( ( *vtxQ1 - *beamspot ).Perp() ) ;
	}
      if( p4jBgLep->Pt() > ptCut &&
	  fabs( p4jBgLep->Eta() ) < etaCut )
	{
	  ++nb ;
	  sortByP( vthr3jAll, hsLep3Pj, p4jBgLep, vbHad3Pj, vbLep3Pj ) ;
	  sortByP( vthr2jAll, hsLep2Pj, p4jBgLep, vbHad2Pj, vbLep2Pj ) ;
	  sortByX( vthr3jAll, vtxBgLep, beamspot, hsLep3Xj, p4jBgLep, vbHad3Xj, vbLep3Xj ) ;
	  sortByX( vthr2jAll, vtxBgLep, beamspot, hsLep2Xj, p4jBgLep, vbHad2Xj, vbLep2Xj ) ;
	  h_vtxbMatched->Fill( ( *vtxBgLep - *beamspot ).Perp() ) ;
	}
      if( p4jSLep->Pt() > ptCut &&
          fabs( p4jSLep->Eta() ) < etaCut &&
	  ( *vtxSLep - *beamspot ).Perp() > vtxqCut )
	{
	  ++nq ;
	  sortByP( vthr3jAll, hsLep3Pj, p4jSLep, vqHad3Pj, vqLep3Pj ) ;
	  sortByP( vthr2jAll, hsLep2Pj, p4jSLep, vqHad2Pj, vqLep2Pj ) ;
	  sortByX( vthr3jAll, vtxSLep, beamspot, hsLep3Xj, p4jSLep, vqHad3Xj, vqLep3Xj ) ;
	  sortByX( vthr2jAll, vtxSLep, beamspot, hsLep2Xj, p4jSLep, vqHad2Xj, vqLep2Xj ) ;
	  h_vtxbMatched->Fill( ( *vtxSLep - *beamspot ).Perp() ) ;
	}
      if( p4jBtLep->Pt() > ptCut &&
	  fabs( p4jBtLep->Eta() ) < etaCut )
	{
	  ++nb ;
	  sortByP( vthr3jAll, hsLep3Pj, p4jBtLep, vbHad3Pj, vbLep3Pj ) ;
	  sortByP( vthr2jAll, hsLep2Pj, p4jBtLep, vbHad2Pj, vbLep2Pj ) ;
	  sortByX( vthr3jAll, vtxBtLep, beamspot, hsLep3Xj, p4jBtLep, vbHad3Xj, vbLep3Xj ) ;
	  sortByX( vthr2jAll, vtxBtLep, beamspot, hsLep2Xj, p4jBtLep, vbHad2Xj, vbLep2Xj ) ;
	  h_vtxbMatched->Fill( ( *vtxBtLep - *beamspot ).Perp() ) ;
	}

      double nbMatched = nb ;
      double nqMatched = nq ;

      for( unsigned int i = 0, n = vp4jQOther->size() ; i < n ; ++i )
	{
	  const TLorentzVector& p4tmp = vp4jQOther->at( i ) ;
	  TVector3 vtxtmp = vvtxQOther->at( i ) ;
	  if( p4tmp.Pt() > ptCut && fabs( p4tmp.Eta() ) < etaCut &&
	    //( vtxtmp - *beamspot ).Perp() > vtxqCut )
	      ( ( vtxtmp - *beamspot ).Perp() > vtxqCut ||
		gRandom->Uniform() < 0.1 ) )
	    // keep 10% at random because all primary quarks will fail the vtx cut
	    {
	      ++nq ;
	      sortByP( vthr3jAll, hsLep3Pj, &p4tmp, vqHad3Pj, vqLep3Pj ) ;
	      sortByP( vthr2jAll, hsLep2Pj, &p4tmp, vqHad2Pj, vqLep2Pj ) ;

	      if( vtxtmp == *beamspot ) // smear this randomly selected jet
		{
		  TVector3 rnd ;
		  rnd.SetPtEtaPhi( vtxqCut,
				   0.,
				   gRandom->Uniform() * TMath::Pi() * 2 ) ;
		  vtxtmp += rnd ;
		}

	      sortByX( vthr3jAll, &vtxtmp, beamspot, hsLep3Xj, &p4tmp, vqHad3Xj, vqLep3Xj ) ;
	      sortByX( vthr2jAll, &vtxtmp, beamspot, hsLep2Xj, &p4tmp, vqHad2Xj, vqLep2Xj ) ;
	      h_vtxqUnmatched->Fill( ( vtxtmp - *beamspot ).Perp() ) ;
	    }
	}

      for( unsigned int i = 0, n = vp4jBOther->size() ; i < n ; ++i )
	{
	  const TLorentzVector& p4tmp = vp4jBOther->at( i ) ;
	  const TVector3& vtxtmp = vvtxBOther->at( i ) ;
	  if( p4tmp.Pt() > ptCut && fabs( p4tmp.Eta() ) < etaCut )
	    {
	      ++nb ;
	      sortByP( vthr3jAll, hsLep3Pj, &p4tmp, vbHad3Pj, vbLep3Pj ) ;
	      sortByP( vthr2jAll, hsLep2Pj, &p4tmp, vbHad2Pj, vbLep2Pj ) ;
	      sortByX( vthr3jAll, &vtxtmp, beamspot, hsLep3Xj, &p4tmp, vbHad3Xj, vbLep3Xj ) ;
	      sortByX( vthr2jAll, &vtxtmp, beamspot, hsLep2Xj, &p4tmp, vbHad2Xj, vbLep2Xj ) ;
	      h_vtxbUnmatched->Fill( ( vtxtmp - *beamspot ).Perp() ) ;
	    }
	}

      h_nqMatched->Fill( nqMatched ) ;
      h_nbMatched->Fill( nbMatched ) ;
      h_nqUnmatched->Fill( nq - nqMatched ) ;
      h_nbUnmatched->Fill( nb - nbMatched ) ;

      //if( nq >= 4 && nb >= 4 )
      //if( nq >= 2 && nb >= 2 )
      if( nq > 2 && nb > 2 )
	{
	  combine( vbHad3Pj, vqHad3Pj, h_mhadhsThr3jPj, h_mhadThr3jPj, 0, 0 ) ;
	  combine( vbLep3Pj, vqLep3Pj, h_mlephsThr3jPj, h_mlepThr3jPj, p4Lep, p4MET ) ;
	  combine( vbHad2Pj, vqHad2Pj, h_mhadhsThr2jPj, h_mhadThr2jPj, 0, 0 ) ;
	  combine( vbLep2Pj, vqLep2Pj, h_mlephsThr2jPj, h_mlepThr2jPj, p4Lep, p4MET ) ;
	  combine( vbHad3Xj, vqHad3Xj, h_mhadhsThr3jXj, h_mhadThr3jXj, 0, 0 ) ;
	  combine( vbLep3Xj, vqLep3Xj, h_mlephsThr3jXj, h_mlepThr3jXj, p4Lep, p4MET ) ;
	  combine( vbHad2Xj, vqHad2Xj, h_mhadhsThr2jXj, h_mhadThr2jXj, 0, 0 ) ;
	  combine( vbLep2Xj, vqLep2Xj, h_mlephsThr2jXj, h_mlepThr2jXj, p4Lep, p4MET ) ;

	  h_nqHad3Pj->Fill( vqHad3Pj.size() ) ;
	  h_nqLep3Pj->Fill( vqLep3Pj.size() ) ;
	  h_nbHad3Pj->Fill( vbHad3Pj.size() ) ;
	  h_nbLep3Pj->Fill( vbLep3Pj.size() ) ;
	  h_nqHad3Xj->Fill( vqHad3Xj.size() ) ;
	  h_nqLep3Xj->Fill( vqLep3Xj.size() ) ;
	  h_nbHad3Xj->Fill( vbHad3Xj.size() ) ;
	  h_nbLep3Xj->Fill( vbLep3Xj.size() ) ;
	  h_nqHadLep3Pj->Fill( vqHad3Pj.size(), vqLep3Pj.size() ) ;
	  h_nbHadLep3Pj->Fill( vbHad3Pj.size(), vbLep3Pj.size() ) ;
	  h_nqHadLep3Xj->Fill( vqHad3Xj.size(), vqLep3Xj.size() ) ;
	  h_nbHadLep3Xj->Fill( vbHad3Xj.size(), vbLep3Xj.size() ) ;
	}
    }

  // draw plots
  gStyle->SetCanvasColor(0);
  gStyle->SetCanvasBorderMode(0);
  gStyle->SetFrameFillColor(0);
  gStyle->SetPadBorderMode(0);
  gStyle->SetPadColor(10);
  gStyle->SetTitleColor(kBlue);
  gStyle->SetStatColor(0);
  gStyle->SetOptStat(111111);

  TCanvas* mycanvas = new TCanvas( "mycanvas", "", 0, 0, 600, 400 ) ;
  mycanvas->SetFillColor( kWhite ) ;
  gStyle->SetCanvasColor( 0 ) ;

  std::string outputFile(inputFile);
  outputFile.erase(outputFile.rfind(string(".root")));
  outputFile.erase(0,outputFile.rfind('/')+1);
  outputFile += ".pdf" ;

  mycanvas->Print( ( outputFile + "[" ).c_str(), "pdf" ) ;

//   drawPair( h_mhadhsThr3jPj, h_mhadThr3jPj,
// 	    "hadronic hemisphere (GenJet, thr3, p)",
// 	    "M(hs)", "M(#tilde{g} cand)",
// 	    mycanvas, outputFile.c_str() ) ;
//   drawPair( h_mlephsThr3jPj, h_mlepThr3jPj,
// 	    "leptonic hemisphere (GenJet, thr3, p)",
// 	    "M(hs)", "M(#tilde{g} cand)",
// 	    mycanvas, outputFile.c_str() ) ;
//   drawPair( h_mhadhsThr2jPj, h_mhadThr2jPj,
// 	    "hadronic hemisphere (GenJet, thr2, p)",
// 	    "M(hs)", "M(#tilde{g} cand)",
// 	    mycanvas, outputFile.c_str() ) ;
//   drawPair( h_mlephsThr2jPj, h_mlepThr2jPj,
// 	    "leptonic hemisphere (GenJet, thr2, p)",
// 	    "M(hs)", "M(#tilde{g} cand)",
// 	    mycanvas, outputFile.c_str() ) ;

  drawPair( h_mhadhsThr3jXj, h_mhadThr3jXj,
	    "hadronic hemisphere (GenJet, thr3, x)",
	    "M(hs)", "M(#tilde{g} cand)",
	    mycanvas, outputFile.c_str() ) ;
  drawPair( h_mlephsThr3jXj, h_mlepThr3jXj,
	    "leptonic hemisphere (GenJet, thr3, x)",
	    "M(hs)", "M(#tilde{g} cand)",
	    mycanvas, outputFile.c_str() ) ;
  drawPair( h_mhadhsThr2jXj, h_mhadThr2jXj,
	    "hadronic hemisphere (GenJet, thr2, x)",
	    "M(hs)", "M(#tilde{g} cand)",
	    mycanvas, outputFile.c_str() ) ;
  drawPair( h_mlephsThr2jXj, h_mlepThr2jXj,
	    "leptonic hemisphere (GenJet, thr2, x)",
	    "M(hs)", "M(#tilde{g} cand)",
	    mycanvas, outputFile.c_str() ) ;

//   drawPair( h_nqHad3Pj, h_nqLep3Pj,
// 	    "#q in hemisphere (GenJet, thr3, p)",
// 	    "had", "lep",
// 	    mycanvas, outputFile.c_str() ) ;
//   drawPair( h_nbHad3Pj, h_nbLep3Pj,
// 	    "#b in hemisphere (GenJet, thr3, p)",
// 	    "had", "lep",
// 	    mycanvas, outputFile.c_str() ) ;
  drawPair( h_nqHad3Xj, h_nqLep3Xj,
	    "#q in hemisphere (GenJet, thr3, x)",
	    "had", "lep",
	    mycanvas, outputFile.c_str() ) ;
  drawPair( h_nbHad3Xj, h_nbLep3Xj,
	    "#b in hemisphere (GenJet, thr3, x)",
	    "had", "lep",
	    mycanvas, outputFile.c_str() ) ;

  mycanvas->Print( ( outputFile + "]" ).c_str(), "pdf" ) ;
}

// return value is hemisphere wrt thrust axis
int fillHSCounts( double cosThrBg, double cosThrS, double cosThrBt,
		  double cosThrWdau0, double cosThrWdau1,
		  TH1F* h_nss, TH1F* h_ws )
{
  int npos = 0 ;
  if( cosThrBg    > 0. ) ++npos ;
  if( cosThrS     > 0. ) ++npos ;
  if( cosThrBt    > 0. ) ++npos ;
  if( cosThrWdau0 > 0. ) ++npos ;
  if( cosThrWdau1 > 0. ) ++npos ;
  int hs = npos >= 3 ? 1 : -1 ; // which hemisphere
  h_nss->Fill( hs > 0 ? npos : 5 - npos ) ;
  // wrong side particles
  if( cosThrBg    * hs < 0. ) h_ws->Fill( 0 ) ;
  if( cosThrS     * hs < 0. ) h_ws->Fill( 1 ) ;
  if( cosThrBt    * hs < 0. ) h_ws->Fill( 2 ) ;
  if( cosThrWdau0 * hs < 0. ) h_ws->Fill( 3 ) ;
  if( cosThrWdau1 * hs < 0. ) h_ws->Fill( 4 ) ;

  return hs ;
}

void sortByP( const TVector3* vthr, int hsLep, const TLorentzVector* p4,
	      std::vector< const TLorentzVector* >& vHad,
	      std::vector< const TLorentzVector* >& vLep )
{
  // we only care about the sign, so no need to normalize.
  double cosThr = vthr->X() * p4->X() + vthr->Y() * p4->Y() ;

  if( cosThr * hsLep < 0. )
    {
      vHad.push_back( p4 ) ;
    }
  else
    {
      vLep.push_back( p4 ) ;
    }
}

void sortByX( const TVector3* vthr, const TVector3* vtx, const TVector3* beamspot,
	      int hsLep, const TLorentzVector* p4,
	      std::vector< const TLorentzVector* >& vHad,
	      std::vector< const TLorentzVector* >& vLep )
{
  // we only care about the sign, so no need to normalize.
  double cosThr = vthr->X() * ( vtx->X() - beamspot->X() ) +
    vthr->Y() * ( vtx->Y() - beamspot->Y() ) ;

  if( cosThr * hsLep < 0. )
    {
      vHad.push_back( p4 ) ;
    }
  else
    {
      vLep.push_back( p4 ) ;
    }
}

void combine( const std::vector< const TLorentzVector* >& vb,
	      const std::vector< const TLorentzVector* >& vq,
	      TH1F* histAll, TH1F* histCand,
	      const TLorentzVector* p4Lep,
	      const TLorentzVector* p4MET,
	      TH1F** diagHists )
{
  double mWmin = 50. ;
  double mWmax = 110. ;
  double mtmin = 125. ;
  double mtmax = 225. ;

  TLorentzVector p4Tot ;

  int nb = vb.size() ;
  for( int ib = 0 ; ib < nb ; ++ib )
    p4Tot += *( vb[ ib ] ) ;

  int nq = vq.size() ;
  for( int iq = 0 ; iq < nq ; ++iq )
    p4Tot += *( vq[ iq ] ) ;

  int ncomb = 0 ;

  if( p4Lep )
    {
      // Solve for neutrino pz
      TLorentzVector p4Nu ;
      if( p4NuCons( p4Lep, p4MET, p4Nu, diagHists ) )
	{
	  p4Tot += *p4Lep ;
	  p4Tot += p4Nu ;

	  // Loop over 3-jet combinations and add lepton + nu 4-vectors
	  // Often, both W-b combinations will be in the top mass window. Count these
	  // combinations only once.
	  for( int ib0 = 0 ; ib0 < nb-1 ; ++ib0 )
	    {
	      TLorentzVector p4t0 = *( vb[ ib0 ] ) + *p4Lep + p4Nu ;
	      double mt0 = p4t0.M() ;

	      for( int ib1 = ib0+1 ; ib1 < nb ; ++ib1 )
		{
		  TLorentzVector p4t1 = *( vb[ ib1 ] ) + *p4Lep + p4Nu ;
		  double mt1 = p4t1.M() ;

		  if( ( mt0 < mtmin || mt0 > mtmax ) &&
		      ( mt1 < mtmin || mt1 > mtmax ) ) continue ;

		  if( diagHists )
		    {
		      diagHists[ 2 ]->Fill( mt0 ) ;
		      diagHists[ 2 ]->Fill( mt1 ) ;
		      diagHists[ 3 ]->Fill( mt0 - mt1 ) ;
		    }

		  for( int iq0 = 0 ; iq0 < nq ; ++iq0 ) // primary s
		    {
		      histCand->Fill( ( *( vb[ ib1 ] ) + *( vq[ iq0 ] ) + p4t0 ).M() ) ;
		      ++ncomb ;
		    }
		}
	    }
	}

      if( diagHists ) diagHists[ 5 ]->Fill( ncomb ) ;
    }
  else
    {
      // Loop over 5-jet combinations and apply mW and mt cuts
      // Count each combination only once.
      for( int iq0 = 0 ; iq0 < nq-2 ; ++iq0 )
	{
	  for( int iq1 = iq0+1 ; iq1 < nq-1 ; ++iq1 )
	    {
	      TLorentzVector p4W01 = *( vq[ iq0 ] ) + *( vq[ iq1 ] ) ;
	      double mW01 = p4W01.M() ;

	      for( int iq2 = iq1+1 ; iq2 < nq ; ++iq2 )
		{
		  TLorentzVector p4W02 = *( vq[ iq0 ] ) + *( vq[ iq2 ] ) ;
		  double mW02 = p4W02.M() ;

		  TLorentzVector p4W12 = *( vq[ iq1 ] ) + *( vq[ iq2 ] ) ;
		  double mW12 = p4W12.M() ;

		  std::vector< TLorentzVector* > goodWs ;
		  if( mW01 > mWmin && mW01 < mWmax ) goodWs.push_back( &p4W01 ) ;
		  if( mW02 > mWmin && mW02 < mWmax ) goodWs.push_back( &p4W02 ) ;
		  if( mW12 > mWmin && mW12 < mWmax ) goodWs.push_back( &p4W12 ) ;

		  for( unsigned int iw = 0 ; iw < goodWs.size() ; ++iw )
		    {
		      TLorentzVector p4q012 = *( vq[ iq2 ] ) + p4W01 ;

		      for( int ib0 = 0 ; ib0 < nb-1 ; ++ib0 )
			{
			  TLorentzVector p4t0 = *( vb[ ib0 ] ) + *( goodWs.at( iw ) ) ;
			  double mt0 = p4t0.M() ;

			  for( int ib1 = ib0+1 ; ib1 < nb ; ++ib1 )
			    {
			      TLorentzVector p4t1 = *( vb[ ib1 ] ) + *( goodWs.at( iw ) ) ;
			      double mt1 = p4t1.M() ;

			      if( ( mt0 < mtmin || mt0 > mtmax ) &&
				  ( mt1 < mtmin || mt1 > mtmax ) ) continue ;

			      histCand->Fill( ( *( vb[ ib0 ] ) + *( vb[ ib1 ] ) + p4q012 ).M() ) ;
			      ++ncomb ;
			    }
			}
		    }
		}
	    }
	}

      if( diagHists ) diagHists[ 4 ]->Fill( ncomb ) ;
    }

  histAll->Fill( p4Tot.M() ) ;
}

// return false if no solution
bool p4NuCons( const TLorentzVector* p4Lep,
	       const TLorentzVector* p4MET,
	       TLorentzVector& p4Nu,
	       TH1F** diagHists )
{
  // recalculate met in case we are given a real neutrino 4-vector
  double met2 = p4MET->Px() * p4MET->Px() + p4MET->Py() * p4MET->Py() ;
  double costhLep = p4Lep->Pz() / p4Lep->Energy() ;
  double sin2thLep = 1. - costhLep * costhLep ;
  double mw = 80.399 ;
  double a = ( mw * mw / 2. +
	       p4Lep->Px() * p4MET->Px() +
	       p4Lep->Py() * p4MET->Py() ) / p4Lep->Energy() ;

  double tmp = a * a - met2 * sin2thLep ;
  if( tmp < 0. )
    return false ;
  else
    tmp = sqrt( tmp ) ;

  double pznu = ( a * costhLep + tmp ) / sin2thLep ;
  TLorentzVector p4Nu0 ;
  p4Nu0.SetXYZT( p4MET->Px(),
		 p4MET->Py(),
		 pznu,
		 sqrt( met2 + pznu * pznu ) ) ;
  pznu = ( a * costhLep - tmp ) / sin2thLep ;
  TLorentzVector p4Nu1 ;
  p4Nu1.SetXYZT( p4MET->Px(),
		 p4MET->Py(),
		 pznu,
		 sqrt( met2 + pznu * pznu ) ) ;

  TLorentzVector p4W0 = p4Nu0 + *p4Lep ;
  TLorentzVector p4W1 = p4Nu1 + *p4Lep ;

  if( diagHists )
    {
      diagHists[ 0 ]->Fill( p4W0.Eta() ) ;
      diagHists[ 0 ]->Fill( p4W1.Eta() ) ;
      diagHists[ 1 ]->Fill( fabs( p4W0.Eta() ) - fabs( p4W1.Eta() ) ) ;
    }
  p4Nu = ( fabs( p4W0.Eta() ) < fabs( p4W1.Eta() ) ) ? p4Nu0 : p4Nu1 ;
  return true ;
}

void drawSinglet( TH1F* h0,
		  const char* title,
		  TCanvas* canvas, const char* filename )
{
  makeNice( h0, kBlue ) ;
  h0->SetTitle( title ) ;
  h0->Draw() ;
  canvas->Print( filename, "pdf" ) ;
}

void drawPair( TH1F* h0, TH1F* h1,
	       const char* title, const char* label0, const char* label1,
	       TCanvas* canvas, const char* filename )
{
  double max = TMath::Max( h0->GetBinContent( h0->GetMaximumBin() ),
			   h1->GetBinContent( h1->GetMaximumBin() ) ) ;

  makeNice( h0, kBlue ) ;
  h0->GetYaxis()->SetRangeUser( 0, max*1.1 ) ;
  makeNice( h1, kRed ) ;
  h1->GetYaxis()->SetRangeUser( 0, max*1.1 ) ;

  h0->SetTitle( title ) ;
  h0->Draw() ;
  h1->Draw( "same" ) ;

  TLegend *leg = new TLegend( 0.78, 0.50, 0.98, 0.65 ) ;
  leg->AddEntry( h0, label0 ) ;
  leg->AddEntry( h1, label1 ) ;
  //Float_t sizeleg = leg->GetTextSize()*1.2;
  //leg->SetTextSize( sizeleg ) ;
  leg->SetFillColor( kWhite ) ;
  leg->Draw();

  canvas->Print( filename, "pdf" ) ;
}

void drawTriplet( TH1F* h0, TH1F* h1, TH1F* h2, TCanvas* canvas, const char* filename )
{
  double max = TMath::Max( TMath::Max( h0->GetBinContent( h0->GetMaximumBin() ),
				       h1->GetBinContent( h1->GetMaximumBin() ) ),
			   h2->GetBinContent( h2->GetMaximumBin() ) ) ;

  makeNice( h0, kBlue ) ;
  h0->GetYaxis()->SetRangeUser( 0, max*1.1 ) ;
  makeNice( h1, kRed ) ;
  h1->GetYaxis()->SetRangeUser( 0, max*1.1 ) ;
  makeNice( h2, kGreen+1 ) ;
  h2->GetYaxis()->SetRangeUser( 0, max*1.1 ) ;

  h0->Draw() ;
  h1->Draw( "same" ) ;
  h2->Draw( "same" ) ;
  canvas->Print( filename, "pdf" ) ;
}

void makeNice( TH1F* h, int color )
{
  h->SetLineColor( color ) ;
  h->SetLineWidth( 3 ) ;
}
