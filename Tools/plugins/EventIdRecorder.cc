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

  unsigned run;
  unsigned lumi;
  unsigned evt;
  TTree* tree;
};

EventIdRecorder::EventIdRecorder(const edm::ParameterSet& cfg) {
  edm::Service<TFileService> fs;

  tree = fs->make<TTree>("event_ids", "");
  tree->Branch("run",   &run,   "run/i");
  tree->Branch("lumi",  &lumi,  "lumi/i");
  tree->Branch("event", &evt,   "event/i");

  if (cfg.existsAs<std::string>("notes"))
    tree->SetAlias("notes", cfg.getParameter<std::string>("notes").c_str());
}

void EventIdRecorder::analyze(const edm::Event& event, const edm::EventSetup&) {
  run  = event.id().run();
  lumi = event.luminosityBlock();
  evt  = event.id().event();
  tree->Fill();
}

DEFINE_FWK_MODULE(EventIdRecorder);
