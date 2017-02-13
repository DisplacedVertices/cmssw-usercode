#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "TTree.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

class EventIdRecorder : public edm::EDAnalyzer {
public:
  explicit EventIdRecorder(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  const bool check_gen_particles;
  unsigned run;
  unsigned lumi;
  unsigned long long evt;
  float first_parton_pz;
  TTree* tree;
};

EventIdRecorder::EventIdRecorder(const edm::ParameterSet& cfg) 
  : check_gen_particles(cfg.existsAs<bool>("check_gen_particles") && cfg.getParameter<bool>("check_gen_particles"))
{
  edm::Service<TFileService> fs;

  tree = fs->make<TTree>("event_ids", "");
  tree->Branch("run",   &run,   "run/i");
  tree->Branch("lumi",  &lumi,  "lumi/i");
  tree->Branch("event", &evt,   "event/l");

  if (check_gen_particles)
    tree->Branch("first_parton_pz", &first_parton_pz, "first_parton_pz/F");

  if (cfg.existsAs<std::string>("notes"))
    tree->SetAlias("notes", cfg.getParameter<std::string>("notes").c_str());
}

void EventIdRecorder::analyze(const edm::Event& event, const edm::EventSetup&) {
  run  = event.id().run();
  lumi = event.luminosityBlock();
  evt  = event.id().event();

  if (check_gen_particles) {
    edm::Handle<reco::GenParticleCollection> gens;
    event.getByLabel("genParticles", gens);
    first_parton_pz = gens->at(2).pz();
  }

  tree->Fill();
}

DEFINE_FWK_MODULE(EventIdRecorder);
