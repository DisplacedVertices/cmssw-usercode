// https://twiki.cern.ch/twiki/bin/viewauth/CMS/L1ECALPrefiringWeightRecipe
// from git cms-merge-topic lathomas:L1Prefiring_9_4_9 at 18-12-18 9:35:19
// convert root file to included chunk with this script:
/*
import os
from DVCode.Tools.ROOTTools import *
z = []
for _,_,f in tdirectory_walk(ROOT.TFile.Open('L1PrefiringMaps_new.root')):
    for x in f:
        fn = x.GetName() + '.C'
        assert not os.path.exists(fn)
        z.append((x.GetName(), fn))
        x.SaveAs(fn)
newfn = os.environ['CMSSW_BASE'] + '/src/DVCode/Tools/plugins/L1ECALPrefiringWeightMaps.h'
f = open(newfn, 'wt')
for hn,fn in z:
   f.write('std::unique_ptr<TH2F> %s;\n' % hn)
f.write('\n')
for i, (hn, fn) in enumerate(z):
    c = open(fn).read()
    assert ('TH2F *%s__%i = new TH2F' % (hn, i+1))  in c
    a,b =c.rsplit('}',1)
    f.write(a + '\n')
    f.write('%s.reset(%s__%i);\n' % (hn, hn, i+1))
    f.write('}\n' + b + '\n')
    os.remove(fn)
*/


// -*- C++ -*-
//
// Package:    ProdTutorial/L1ECALPrefiringWeightProducer
// Class:      L1ECALPrefiringWeightProducer
// 
/**\class L1ECALPrefiringWeightProducer L1ECALPrefiringWeightProducer.cc ProdTutorial/L1ECALPrefiringWeightProducer/plugins/L1ECALPrefiringWeightProducer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  localusers user
//         Created:  Thu, 08 Nov 2018 16:16:00 GMT
//
//


// system include files
#include <memory>

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "TH2.h"

#include <iostream>
enum fluctuations{central=0, up, down};

class L1ECALPrefiringWeightProducer : public edm::stream::EDProducer<> {
public:
  explicit L1ECALPrefiringWeightProducer(const edm::ParameterSet&);
  ~L1ECALPrefiringWeightProducer();
  
  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
  
private:
  virtual void beginStream(edm::StreamID) override;
  virtual void produce(edm::Event&, const edm::EventSetup&) override;
  //  virtual void beginJob();
  //virtual void endJob(void);
  virtual void endStream() override;
  virtual double GetPrefiringRate( double eta, double pt, TH2F * h_prefmap,/*std::string object, std::string dataera, */ int fluctuation);
  
  edm::InputTag srcPhotons_;
  edm::EDGetTokenT<std::vector< pat::Photon> >  photons_token_; 
  
  edm::InputTag srcJets_;
  edm::EDGetTokenT<std::vector< pat::Jet> > jets_token_;
  

  std::unique_ptr<TH2F> h_prefmap_photon; 
  std::unique_ptr<TH2F> h_prefmap_jet;
  std::string dataera_;
  bool useEMpt_;
  double prefiringRateSystUnc_;
};


L1ECALPrefiringWeightProducer::L1ECALPrefiringWeightProducer(const edm::ParameterSet& iConfig)
{
  photons_token_  = consumes<std::vector<pat::Photon> >(  iConfig.getParameter<edm::InputTag>( "ThePhotons" )  );
  jets_token_  = consumes<std::vector<pat::Jet> >(  iConfig.getParameter<edm::InputTag>( "TheJets" )  );

  dataera_ =  iConfig.getParameter<std::string>( "DataEra" ) ;
  useEMpt_  =  iConfig.getParameter<bool>( "UseJetEMPt" ) ; 
  prefiringRateSystUnc_ =  iConfig.getParameter<double>( "PrefiringRateSystematicUncty" ) ;


  //TFile *  file_prefiringmaps_;
  //std::string fname =  iConfig.getParameter<std::string>( "L1Maps" );
  //file_prefiringmaps_ = new TFile(  fname.c_str(),"read" );
  //TString mapphotonfullname= "L1prefiring_photonptvseta_"+ dataera_; 
  //h_prefmap_photon =(TH2F*) file_prefiringmaps_->Get(mapphotonfullname);
  //TString mapjetfullname= (useEMpt_) ? "L1prefiring_jetemptvseta_"+ dataera_  :  "L1prefiring_jetptvseta_"+ dataera_ ; 
  //h_prefmap_jet =(TH2F*) file_prefiringmaps_->Get(mapjetfullname);
  //file_prefiringmaps_->Close();

#include "L1ECALPrefiringWeightMaps.h"
  assert(dataera_ == "2017BtoF" or dataera_ == "2016BtoH");
  if (dataera_ == "2017BtoF") {
    h_prefmap_jet.reset(useEMpt_ ? L1prefiring_jetemptvseta_2017BtoF.release() : L1prefiring_jetptvseta_2017BtoF.release());
    h_prefmap_photon.reset(L1prefiring_photonptvseta_2017BtoF.release());
  }
  else {
    h_prefmap_jet.reset(useEMpt_ ? L1prefiring_jetemptvseta_2016BtoH.release() : L1prefiring_jetptvseta_2016BtoH.release());
    h_prefmap_photon.reset(L1prefiring_photonptvseta_2016BtoH.release());
  }

  produces<double>( "NonPrefiringProb" ).setBranchAlias( "NonPrefiringProb");
  produces<double>( "NonPrefiringProbUp" ).setBranchAlias( "NonPrefiringProbUp");
  produces<double>( "NonPrefiringProbDown" ).setBranchAlias( "NonPrefiringProbDown");

  

}


L1ECALPrefiringWeightProducer::~L1ECALPrefiringWeightProducer()
{
}



void
L1ECALPrefiringWeightProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;

   //Photons
   edm::Handle< std::vector<pat::Photon> > thePhotons;
   iEvent.getByToken(photons_token_,thePhotons);
   
   //Jets
   edm::Handle< std::vector< pat::Jet> > theJets;
   iEvent.getByToken(jets_token_,theJets );
   
   //Probability for the event NOT to prefire, computed with the prefiring maps per object. 
   //Up and down values correspond to the resulting value when shifting up/down all prefiring rates in prefiring maps. 
   double NonPrefiringProba[3]={1.,1.,1.};//0: central, 1: up, 2: down
   
   for(int fluct = 0; fluct<3;fluct++) {
     //Start by applying the prefiring maps to photons in the affected regions. 
     std::vector < pat::Photon > affectedphotons; 
     for( std::vector<pat::Photon>::const_iterator photon = (*thePhotons).begin(); photon != (*thePhotons).end(); photon++ ) {
       double pt_gam= (&*photon)->pt();
       double eta_gam=  (&*photon)->eta();
       if( pt_gam < 20.) continue;
       if( fabs(eta_gam) <2.) continue;
       if( fabs(eta_gam) >3.) continue;
       affectedphotons.push_back((*photon));
       double prefiringprob_gam=  GetPrefiringRate( eta_gam, pt_gam, h_prefmap_photon.get(), fluct);  
       NonPrefiringProba[fluct] *= (1.-prefiringprob_gam);
     }
     
     //Now applying the prefiring maps to jets in the affected regions. 
     for( std::vector<pat::Jet>::const_iterator jet = (*theJets).begin(); jet != (*theJets).end(); jet++ ) {
       
       double pt_jet= (&*jet)->pt();
       double eta_jet=  (&*jet)->eta();
       double phi_jet=  (&*jet)->phi();
       if( pt_jet < 20.) continue;
       if( fabs(eta_jet) <2.) continue;
       if( fabs(eta_jet) >3.) continue;

       //Loop over photons to remove overlap
       double nonprefiringprobfromoverlappingphotons =1.;
       for( std::vector<pat::Photon>::const_iterator photon = affectedphotons.begin(); photon != affectedphotons.end(); photon++ ) {
	 double pt_gam= (&*photon)->pt();
	 double eta_gam=  (&*photon)->eta();
	 double phi_gam=  (&*photon)->phi();
	 double dR = reco::deltaR( eta_jet,phi_jet,eta_gam,phi_gam );
	 if(dR>0.4)continue;
	 double prefiringprob_gam =  GetPrefiringRate( eta_gam, pt_gam, h_prefmap_photon.get() , fluct);
	 nonprefiringprobfromoverlappingphotons  *= (1.-prefiringprob_gam) ;
       }
       
       
       double ptem_jet =  pt_jet*(jet->neutralEmEnergyFraction()+jet->chargedEmEnergyFraction());
       double prefiringprob_jet = (useEMpt_) ? GetPrefiringRate( eta_jet, ptem_jet, h_prefmap_jet.get() , fluct) : GetPrefiringRate( eta_jet, pt_jet , h_prefmap_jet.get() , fluct);
       //useEMpt =true if one wants to use maps parametrized vs Jet EM pt instead of pt.
       double nonprefiringprobfromoverlappingjet =(1.-prefiringprob_jet);
       //If there are no overlapping photons, just multiply by the jet non prefiring rate
       if(nonprefiringprobfromoverlappingphotons ==1.)    NonPrefiringProba[fluct]*= (1.-prefiringprob_jet);
       //If overlapping photons have a non prefiring rate larger than the jet, then replace these weights by the jet one
       else if(nonprefiringprobfromoverlappingphotons > nonprefiringprobfromoverlappingjet ) {
	 if(nonprefiringprobfromoverlappingphotons !=0.)NonPrefiringProba[fluct]*= nonprefiringprobfromoverlappingjet /nonprefiringprobfromoverlappingphotons;
	 else NonPrefiringProba[fluct]=0.;
	 
	 
       }
       //If overlapping photons have a non prefiring rate smaller than the jet, don't consider the jet in the event weight
       else if(nonprefiringprobfromoverlappingphotons < nonprefiringprobfromoverlappingjet ) NonPrefiringProba[fluct]*=1.;
     
     }
   }
   
   //   std::cout << NonPrefiringProba[0]<<", "<< NonPrefiringProba[1]<<", "<< NonPrefiringProba[2]<<", "<<std::endl;
   auto NonPrefiringProb =std::make_unique <double> ( NonPrefiringProba[0]);
   auto NonPrefiringProbUp =std::make_unique <double> ( NonPrefiringProba[1]);
   auto NonPrefiringProbDown =std::make_unique <double> ( NonPrefiringProba[2]);
   iEvent.put( std::move(NonPrefiringProb), "NonPrefiringProb" );        
   iEvent.put( std::move(NonPrefiringProbUp), "NonPrefiringProbUp" );        
   iEvent.put( std::move(NonPrefiringProbDown), "NonPrefiringProbDown" );    
    
}


double L1ECALPrefiringWeightProducer::GetPrefiringRate( double eta, double pt, TH2F * h_prefmap /*std::string object, std::string dataera*/ , int fluctuation){

  if(h_prefmap==0) return 0.;
  //Check pt is not above map overflow
  int nbinsy = h_prefmap->GetNbinsY();
  double maxy= h_prefmap->GetYaxis()->GetBinLowEdge(nbinsy+1);
  if(pt>=maxy) pt = maxy-0.01;
  int thebin= h_prefmap->FindBin(eta,pt);
  
  double prefrate =  h_prefmap->GetBinContent(thebin);
  
  if(fluctuation == up) prefrate = TMath::Min(TMath::Max(prefrate +  h_prefmap->GetBinError(thebin), (1.+prefiringRateSystUnc_)*prefrate),1.);
  if(fluctuation == down) prefrate = TMath::Max(TMath::Min(prefrate -  h_prefmap->GetBinError(thebin), (1.-prefiringRateSystUnc_)*prefrate),0.);    
  
  return prefrate;
  
  
}


// ------------ method called once each stream before processing any runs, lumis or events  ------------
void
L1ECALPrefiringWeightProducer::beginStream(edm::StreamID)
{
}

// ------------ method called once each stream after processing all runs, lumis and events  ------------
void
L1ECALPrefiringWeightProducer::endStream() {
}

// ------------ method called when starting to processes a run  ------------
/*
void
L1ECALPrefiringWeightProducer::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when ending the processing of a run  ------------
/*
void
L1ECALPrefiringWeightProducer::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when starting to processes a luminosity block  ------------
/*
void
L1ECALPrefiringWeightProducer::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when ending the processing of a luminosity block  ------------
/*
void
L1ECALPrefiringWeightProducer::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
L1ECALPrefiringWeightProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  
  desc.add<edm::InputTag>("ThePhotons", edm::InputTag("slimmedPhotons"));
  desc.add<edm::InputTag>("TheJets", edm::InputTag("slimmedJets"));
  desc.add<std::string>("L1Maps", "L1PrefiringMaps_new.root");
  desc.add<std::string>("DataEra", "2017BtoF");
  desc.add<bool>("UseJetEMPt", true);
  desc.add<double>("PrefiringRateSystematicUncty",0.2);

  descriptions.add("l1ECALPrefiringWeightProducer",desc);
  //descriptions.addDefault(desc);


}





//define this as a plug-in
DEFINE_FWK_MODULE(L1ECALPrefiringWeightProducer);

