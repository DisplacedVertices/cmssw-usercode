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

  MFVVertexAux xform_vertex(const double bsx, const double bsy, const double bsz, const MFVVertexAux&) const;

  const edm::InputTag event_src;
  const std::vector<double> force_bs;
  const edm::InputTag vertex_src;
  const edm::InputTag weight_src;

  TH1F* h_nsv;
  TH1F* h_nsvsel;

  mfv::MiniNtuple nt;
  TTree* tree;
};

MFVMiniTreer::MFVMiniTreer(const edm::ParameterSet& cfg)
  : event_src(cfg.getParameter<edm::InputTag>("event_src")),
    force_bs(cfg.getParameter<std::vector<double> >("force_bs")),
    vertex_src(cfg.getParameter<edm::InputTag>("vertex_src")),
    weight_src(cfg.getParameter<edm::InputTag>("weight_src"))
{
  if (force_bs.size() && force_bs.size() != 3)
    throw cms::Exception("Misconfiguration", "force_bs must be empty or size 3");

  edm::Service<TFileService> fs;

  h_nsv = new TH1F("h_nsv", "", 10, 0, 10);
  h_nsvsel = new TH1F("h_nsvsel", "", 10, 0, 10);

  tree = fs->make<TTree>("t", "");
  mfv::write_to_tree(tree, nt);
}

MFVVertexAux MFVMiniTreer::xform_vertex(const double bsx, const double bsy, const double bsz, const MFVVertexAux& v) const {
  MFVVertexAux v2(v);
  v2.x -= bsx;
  v2.y -= bsy;
  v2.z -= bsz;
  return v2;
}

void MFVMiniTreer::analyze(const edm::Event& event, const edm::EventSetup&) {
  nt.run   = event.id().run();
  nt.lumi  = event.luminosityBlock();
  nt.event = event.id().event();

  edm::Handle<MFVEvent> mevent;
  event.getByLabel(event_src, mevent);

  nt.npu = int(mevent->npu);

  edm::Handle<double> weight;
  event.getByLabel(weight_src, weight);
  nt.weight = *weight;

  nt.njets = mevent->njets();
  if (nt.njets > 50)
    throw cms::Exception("CheckYourPremises") << "too many jets in event: " << nt.njets;

  for (int i = 0; i < mevent->njets(); ++i) {
    nt.jet_pt[i] = mevent->jet_pt[i];
    nt.jet_eta[i] = mevent->jet_eta[i];
    nt.jet_phi[i] = mevent->jet_phi[i];
    nt.jet_energy[i] = mevent->jet_energy[i];
  }

  const double bsx = force_bs.size() ? force_bs[0] : mevent->bsx;
  const double bsy = force_bs.size() ? force_bs[1] : mevent->bsy;
  const double bsz = force_bs.size() ? force_bs[2] : mevent->bsz;

  edm::Handle<MFVVertexAuxCollection> input_vertices;
  event.getByLabel(vertex_src, input_vertices);

  MFVVertexAuxCollection vertices;

  for (const MFVVertexAux& v : *input_vertices)
    vertices.push_back(xform_vertex(bsx, bsy, bsz, v));

  h_nsv->Fill(input_vertices->size());
  h_nsvsel->Fill(vertices.size());
  
  if (vertices.size() == 1) {
    const MFVVertexAux& v0 = vertices[0];
    nt.nvtx = 1;
    nt.ntk0 = v0.ntracks();
    nt.x0 = v0.x;
    nt.y0 = v0.y;
    nt.z0 = v0.z;
    nt.cxx0 = v0.cxx;
    nt.cxy0 = v0.cxy;
    nt.cxz0 = v0.cxz;
    nt.cyy0 = v0.cyy;
    nt.cyz0 = v0.cyz;
    nt.czz0 = v0.czz;
    nt.x1 = nt.y1 = nt.z1 = nt.cxx1 = nt.cxy1 = nt.cxz1 = nt.cyy1 = nt.cyz1 = nt.czz1 = 0;
  }
  else if (vertices.size() >= 2) {
    const MFVVertexAux& v0 = vertices[0];
    const MFVVertexAux& v1 = vertices[1];
    nt.nvtx = 2;
    nt.ntk0 = v0.ntracks();
    nt.ntk1 = v1.ntracks();
    nt.x0 = v0.x; nt.y0 = v0.y; nt.z0 = v0.z; nt.cxx0 = v0.cxx; nt.cxy0 = v0.cxy; nt.cxz0 = v0.cxz; nt.cyy0 = v0.cyy; nt.cyz0 = v0.cyz; nt.czz0 = v0.czz;
    nt.x1 = v1.x; nt.y1 = v1.y; nt.z1 = v1.z; nt.cxx1 = v1.cxx; nt.cxy1 = v1.cxy; nt.cxz1 = v1.cxz; nt.cyy1 = v1.cyy; nt.cyz1 = v1.cyz; nt.czz1 = v1.czz;
  }
  else {
    if (vertices.size() != 0)
      throw cms::Exception("CheckYourPremises") << "more than two vertices (" << vertices.size() << ") in this event";
    return;
  }

  tree->Fill();
}

DEFINE_FWK_MODULE(MFVMiniTreer);
