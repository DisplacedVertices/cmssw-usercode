#include "TTree.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"

class BeamSpotTreeProducer : public edm::EDAnalyzer {
public:
  explicit BeamSpotTreeProducer(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  const edm::InputTag event_src;

  struct tree_t {
    unsigned run;
    unsigned lumi;
    unsigned event;
    float bsx;
    float bsy;
    float bsz;
    float pvx;
    float pvy;
    float pvz;

    tree_t() { clear(); }

    void clear() {
      run = lumi = event = bsx = bsy = bsz = pvx = pvy = pvz = 0;
    }
  };

  TTree* tree;
  tree_t nt;
};

BeamSpotTreeProducer::BeamSpotTreeProducer(const edm::ParameterSet& cfg)
  : event_src(cfg.getParameter<edm::InputTag>("event_src"))
{
  edm::Service<TFileService> fs;
  tree = fs->make<TTree>("t", "");
  tree->Branch("run", &nt.run, "run/i");
  tree->Branch("lumi", &nt.lumi, "lumi/i");
  tree->Branch("event", &nt.event, "event/i");
  tree->Branch("bsx", &nt.bsx, "bsx/F");
  tree->Branch("bsy", &nt.bsy, "bsy/F");
  tree->Branch("bsz", &nt.bsz, "bsz/F");
}

void BeamSpotTreeProducer::analyze(const edm::Event& event, const edm::EventSetup&) {
  nt.clear();
  nt.run = event.id().run();
  nt.lumi = event.luminosityBlock();
  nt.event = event.id().event();

  edm::Handle<MFVEvent> mevent;
  event.getByLabel(event_src, mevent);

  nt.bsx = mevent->bsx;
  nt.bsy = mevent->bsy;
  nt.bsz = mevent->bsz;
  nt.pvx = mevent->pvx;
  nt.pvy = mevent->pvy;
  nt.pvz = mevent->pvz;

  tree->Fill();
}

DEFINE_FWK_MODULE(BeamSpotTreeProducer);
