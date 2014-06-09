#include "TTree.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"

class MFVMiniTreer : public edm::EDAnalyzer {
public:
  explicit MFVMiniTreer(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

  MFVVertexAux xform_vertex(const MFVEvent&, const MFVVertexAux&) const;

  const edm::InputTag event_src;
  const edm::InputTag vertex_src;

  TH1F* h_nsv;
  TH1F* h_nsvsel;

  mfv::MiniNtuple nt;
  TTree* tree;
};

MFVMiniTreer::MFVMiniTreer(const edm::ParameterSet& cfg)
  : event_src(cfg.getParameter<edm::InputTag>("event_src")),
    vertex_src(cfg.getParameter<edm::InputTag>("vertex_src"))
{
  edm::Service<TFileService> fs;

  h_nsv = new TH1F("h_nsv", "", 10, 0, 10);
  h_nsvsel = new TH1F("h_nsvsel", "", 10, 0, 10);

  tree = fs->make<TTree>("t", "");
  mfv::write_to_tree(tree, nt);
}

MFVVertexAux MFVMiniTreer::xform_vertex(const MFVEvent& mevent, const MFVVertexAux& v) const {
  MFVVertexAux v2(v);
  v2.x -= mevent.bsx;
  v2.y -= mevent.bsy;
  v2.z -= mevent.bsz;
  return v2;
}

void MFVMiniTreer::analyze(const edm::Event& event, const edm::EventSetup&) {
  nt.run   = event.id().run();
  nt.lumi  = event.luminosityBlock();
  nt.event = event.id().event();

  edm::Handle<MFVEvent> mevent;
  event.getByLabel(event_src, mevent);

  edm::Handle<MFVVertexAuxCollection> input_vertices;
  event.getByLabel(vertex_src, input_vertices);

  MFVVertexAuxCollection vertices;

  for (const MFVVertexAux& v : *input_vertices)
    vertices.push_back(xform_vertex(*mevent, v));

  h_nsv->Fill(input_vertices->size());
  h_nsvsel->Fill(vertices.size());
  
  if (vertices.size() == 1) {
    const MFVVertexAux& v0 = vertices[0];
    nt.nvtx = 1;
    nt.ntk0 = v0.ntracks();
    nt.x0 = v0.x;
    nt.y0 = v0.y;
    nt.z0 = v0.z;
  }
  else if (vertices.size() >= 2) {
    const MFVVertexAux& v0 = vertices[0];
    const MFVVertexAux& v1 = vertices[1];
    nt.nvtx = 2;
    nt.ntk0 = v0.ntracks();
    nt.ntk1 = v1.ntracks();
    nt.x0 = v0.x; nt.y0 = v0.y; nt.z0 = v0.z;
    nt.x1 = v1.x; nt.y1 = v1.y; nt.z1 = v1.z;
  }
  else {
    if (vertices.size() != 0)
      throw cms::Exception("CheckYourPremises") << "more than two vertices (" << vertices.size() << ") in this event";
    return;
  }

  tree->Fill();
}

DEFINE_FWK_MODULE(MFVMiniTreer);
