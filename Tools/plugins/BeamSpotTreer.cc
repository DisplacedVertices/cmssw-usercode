#include "TTree.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

class BeamSpotTreer : public edm::EDAnalyzer {
public:
  explicit BeamSpotTreer(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  const edm::InputTag beamspot_src;
  const edm::InputTag primary_vertex_src;

  struct tree_t {
    unsigned run;
    unsigned lumi;
    unsigned event;
    float bsx;
    float bsy;
    float bsz;
    float bsdxdz;
    float bsdydz;
    float bssigmaz;
    std::vector<float> pvx;
    std::vector<float> pvy;
    std::vector<float> pvz;
    std::vector<float> pvntracks;
    std::vector<float> pvchi2;
    std::vector<float> pvndof;

    tree_t() { clear(); }

    void clear() {
      run = lumi = event = 0;
      bsx = bsy = bsz = bsdxdz = bsdydz = bssigmaz = 0;
      pvx.clear();
      pvy.clear();
      pvz.clear();
      pvntracks.clear();
      pvchi2.clear();
      pvndof.clear();
    }
  };

  TTree* tree;
  tree_t nt;
};

BeamSpotTreer::BeamSpotTreer(const edm::ParameterSet& cfg)
  : beamspot_src(cfg.getParameter<edm::InputTag>("beamspot_src")),
    primary_vertex_src(cfg.getParameter<edm::InputTag>("primary_vertex_src"))
{
  edm::Service<TFileService> fs;
  tree = fs->make<TTree>("t", "");
  tree->Branch("run", &nt.run, "run/i");
  tree->Branch("lumi", &nt.lumi, "lumi/i");
  tree->Branch("event", &nt.event, "event/i");
  tree->Branch("bsx", &nt.bsx, "bsx/F");
  tree->Branch("bsy", &nt.bsy, "bsy/F");
  tree->Branch("bsz", &nt.bsz, "bsz/F");
  tree->Branch("bsdxdz", &nt.bsdxdz, "bsdxdz/F");
  tree->Branch("bsdydz", &nt.bsdydz, "bsdydz/F");
  tree->Branch("bssigmaz", &nt.bssigmaz, "bssigmaz/F");
  tree->Branch("pvx", &nt.pvx);
  tree->Branch("pvy", &nt.pvy);
  tree->Branch("pvz", &nt.pvz);
  tree->Branch("pvntracks", &nt.pvntracks);
  tree->Branch("pvchi2", &nt.pvchi2);
  tree->Branch("pvndof", &nt.pvndof);
}

void BeamSpotTreer::analyze(const edm::Event& event, const edm::EventSetup&) {
  nt.clear();
  nt.run = event.id().run();
  nt.lumi = event.luminosityBlock();
  nt.event = event.id().event();

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByLabel(beamspot_src, beamspot);
  nt.bsx = beamspot->x0();
  nt.bsy = beamspot->y0();
  nt.bsz = beamspot->z0();
  nt.bsdxdz = beamspot->dxdz();
  nt.bsdydz = beamspot->dydz();
  nt.bssigmaz = beamspot->sigmaZ();

  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByLabel(primary_vertex_src, primary_vertices);
  for (const reco::Vertex& pv : *primary_vertices) {
    nt.pvx.push_back(pv.x());
    nt.pvy.push_back(pv.y());
    nt.pvz.push_back(pv.z());
    nt.pvntracks.push_back(pv.nTracks());
    nt.pvchi2.push_back(pv.chi2());
    nt.pvndof.push_back(pv.ndof());
  }

  tree->Fill();
}

DEFINE_FWK_MODULE(BeamSpotTreer);
