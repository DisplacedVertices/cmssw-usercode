#include "TH2F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DataFormats/BTauReco/interface/JetTag.h"
#include "JMTucker/Tools/interface/TriggerHelper.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/Tools/interface/GenUtilities.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralino/interface/EventTools.h"


class MinBiasHistos : public edm::EDAnalyzer {
 public:
  explicit MinBiasHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::InputTag jet_src;
  const edm::InputTag btag_src;
  const edm::InputTag gen_particle_src;
  const double jet_pt_min;
  const double bdisc_min;

  TH1F* h_jet_pt;
  TH1F* h_jet_eta;
  TH1F* h_jet_phi;
  TH1F* h_ndisc;
  TH1F* h_njets;
  TH1F* h_nbjets;
  TH1F* h_nbquarks;
  TH1F* h_nconstituents;
  TH1F* h_Energy;
  TH1F* h_emEnergy;
  TH1F* h_hadEnergy;
  TH1F* h_mass;

};


MinBiasHistos::MinBiasHistos(const edm::ParameterSet& cfg)
  :jet_src(cfg.getParameter<edm::InputTag>("jet_src")),
   btag_src(cfg.getParameter<edm::InputTag>("btag_src")),
   gen_particle_src(cfg.getParameter<edm::InputTag>("gen_particle_src")),
   jet_pt_min(cfg.getParameter<double>("jet_pt_min")),
   bdisc_min(cfg.getParameter<double>("bdisc_min"))
{
  edm::Service<TFileService> fs;

  h_jet_pt = fs->make<TH1F>("h_jet_pt", "MinBias Jet pt", 100,0,1000);
  h_jet_eta = fs->make<TH1F>("h_jet_eta", "MinBias Jet eta", 100,-3,3);
  h_jet_phi = fs->make<TH1F>("h_jet_phi", "MinBias Jet phi", 100,-3.15,3.15);
  h_ndisc = fs->make<TH1F>("h_ndisc", "Btag disc", 100,-1,2);
  h_njets = fs->make<TH1F>("h_njets", "Numb jets", 10,0,10);
  h_nbjets = fs->make<TH1F>("h_nbjets", "Numb b jets", 10,0,10);
  h_nbquarks = fs->make<TH1F>("h_nbquarks", "Numb b quarks", 10,0,10);
  h_nconstituents = fs->make<TH1F>("h_nconstituents", "Numb constituents", 10,0,20);
  h_Energy = fs->make<TH1F>("h_Energy", "MinBias Jet Energy", 100,0,1000);
  h_emEnergy = fs->make<TH1F>("h_emEnergy", "MinBias Jet EM Energy", 100,0,1000);
  h_hadEnergy = fs->make<TH1F>("h_hadEnergy", "MinBias Jet HAD Energy", 100,0,1000);
  h_mass = fs->make<TH1F>("h_mass", "MinBias Jet Mass", 100,0,1000);

}

void MinBiasHistos::analyze(const edm::Event& event, const edm::EventSetup&) {

  edm::Handle<reco::GenJetCollection> jets;
  event.getByLabel(jet_src, jets);
  
  edm::Handle<reco::GenParticleCollection> gen_particles;
  event.getByLabel(gen_particle_src, gen_particles);

  int nbquarks=0;
  for (const auto& gen_p : *gen_particles)
    if (abs(gen_p.pdgId())==5 && gen_p.status() == 2)
      nbquarks++;
  h_nbquarks->Fill(nbquarks);

  int njets = 0;
  int nbjets = 0;
  for (const auto& jet : *jets) {
    if (jet.pt() > jet_pt_min &&
	fabs(jet.eta()) < 2.5 &&
	jet.numberOfDaughters() > 1 
	//&& (fabs(jet.eta()) >= 2.4 || (jet.chargedEmEnergyFraction() < 0.99 && jet.chargedHadronEnergyFraction() > 0. && jet.chargedMultiplicity() > 0)) &&
	//jet.neutralHadronEnergyFraction() < 0.90 &&
	//jet.neutralEmEnergyFraction() < 0.90
	) 
      {
	njets++;
	if (gen_jet_id(jet) == 5)
	  nbjets++;
	h_jet_pt->Fill(jet.pt());
	h_jet_eta->Fill(jet.eta());
	h_jet_phi->Fill(jet.phi());
	h_nconstituents->Fill(jet.nConstituents());
	h_Energy->Fill(jet.energy());
	h_emEnergy->Fill(jet.emEnergy());
	h_hadEnergy->Fill(jet.hadEnergy());
	h_mass->Fill(jet.mass());
       
      }    
  }  
  if (nbjets==1)
    std::cout<<"Run="<<event.id().run()<<" Event="<<event.id().event()<<std::endl;
    
  h_njets->Fill(njets);
  h_nbjets->Fill(nbjets);
}

DEFINE_FWK_MODULE(MinBiasHistos);
