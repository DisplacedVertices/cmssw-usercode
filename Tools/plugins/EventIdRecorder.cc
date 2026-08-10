#include "TTree.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
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

  edm::EDGetTokenT<reco::GenParticleCollection> gen_particles_token;

  const bool check_gen_particles;
  const bool prints;
  unsigned run;
  unsigned lumi;
  unsigned long long evt;
  float first_parton_pz;
  TTree* tree;
};

EventIdRecorder::EventIdRecorder(const edm::ParameterSet& cfg) 
  : check_gen_particles(cfg.existsAs<bool>("check_gen_particles") && cfg.getParameter<bool>("check_gen_particles")),
    prints(cfg.getUntrackedParameter<bool>("prints", false)),
    run(0), lumi(0), evt(0), first_parton_pz(0)
{
  if (check_gen_particles)
    gen_particles_token = consumes<reco::GenParticleCollection>(edm::InputTag("genParticles"));

  edm::Service<TFileService> fs;

  tree = fs->make<TTree>("t", "");
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
    event.getByToken(gen_particles_token, gens);
    first_parton_pz = gens->at(2).pz();
  }

  tree->Fill();

  if (prints) {
    const edm::EventAuxiliary& a = event.eventAuxiliary();
    std::cout << "run " << run << " lumi " << lumi << " event " << evt << " 1stpartonpz " << first_parton_pz << " id " << a.id() << " guid " << a.processGUID() << " time " << a.time().value() << " isreal " << a.isRealData() << " expt type " << a.experimentType() << " bx " << a.bunchCrossing() << " store " << a.storeNumber() << std::endl;
  }
}

DEFINE_FWK_MODULE(EventIdRecorder);
