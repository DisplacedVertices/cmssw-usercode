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
#include "JMTucker/Tools/interface/Utilities.h"

class MFVMiniTreer : public edm::EDAnalyzer {
public:
  explicit MFVMiniTreer(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

  MFVVertexAux xform_vertex(const MFVEvent&, const MFVVertexAux&) const;

  const edm::EDGetTokenT<MFVEvent> event_token;
  const edm::EDGetTokenT<MFVVertexAuxCollection> vertex_token;
  const edm::EDGetTokenT<double> weight_token;

  const bool save_tracks;

  TH1F* h_nsv;
  TH1F* h_nsvsel;

  mfv::MiniNtuple nt;
  TTree* tree;
};

MFVMiniTreer::MFVMiniTreer(const edm::ParameterSet& cfg)
  : event_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("event_src"))),
    vertex_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertex_src"))),
    weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
    save_tracks(cfg.getParameter<bool>("save_tracks"))
{
  edm::Service<TFileService> fs;

  h_nsv = fs->make<TH1F>("h_nsv", "", 10, 0, 10);
  h_nsvsel = fs->make<TH1F>("h_nsvsel", "", 10, 0, 10);

  tree = fs->make<TTree>("t", "");
  mfv::write_to_tree(tree, nt);
}

MFVVertexAux MFVMiniTreer::xform_vertex(const MFVEvent& mevent, const MFVVertexAux& v) const {
  MFVVertexAux v2(v);
  v2.x -= mevent.bsx_at_z(v.z);
  v2.y -= mevent.bsy_at_z(v.z);
  v2.z -= mevent.bsz;
  return v2;
}

void MFVMiniTreer::analyze(const edm::Event& event, const edm::EventSetup&) {
  nt.run   = event.id().run();
  nt.lumi  = event.luminosityBlock();
  nt.event = event.id().event();

  edm::Handle<MFVEvent> mevent;
  event.getByToken(event_token, mevent);

  nt.gen_flavor_code = mevent->gen_flavor_code;
  nt.npv = int2uchar(mevent->npv);
  nt.pvx = mevent->pvx - mevent->bsx_at_z(mevent->pvz);
  nt.pvy = mevent->pvy - mevent->bsy_at_z(mevent->pvz);
  nt.pvz = mevent->pvz - mevent->bsz;
  nt.npu = int2uchar(mevent->npu);

  edm::Handle<double> weight;
  event.getByToken(weight_token, weight);
  nt.weight = *weight;

  nt.njets = int2uchar(mevent->njets());
  if (nt.njets > 50)
    throw cms::Exception("CheckYourPremises") << "too many jets in event: " << nt.njets;

  for (int i = 0; i < mevent->njets(); ++i) {
    nt.jet_pt[i] = mevent->jet_pt[i];
    nt.jet_eta[i] = mevent->jet_eta[i];
    nt.jet_phi[i] = mevent->jet_phi[i];
    nt.jet_energy[i] = mevent->jet_energy[i];
    nt.jet_id[i] = mevent->jet_id[i];
  }

  edm::Handle<MFVVertexAuxCollection> input_vertices;
  event.getByToken(vertex_token, input_vertices);

  MFVVertexAuxCollection vertices;

  for (const MFVVertexAux& v : *input_vertices)
    vertices.push_back(xform_vertex(*mevent, v));

  h_nsv->Fill(input_vertices->size());
  h_nsvsel->Fill(vertices.size());

  if (vertices.size() == 1) {
    const MFVVertexAux& v0 = vertices[0];
    nt.nvtx = 1;
    nt.ntk0 = int2uchar(v0.ntracks());
    if (save_tracks)
      for (int i = 0, ie = v0.ntracks(); i < ie; ++i) {
        nt.tk0_chi2.push_back(v0.track_chi2[i]);
        nt.tk0_ndof.push_back(v0.track_ndof[i]);
        nt.tk0_vx.push_back(v0.track_vx[i]);
        nt.tk0_vy.push_back(v0.track_vy[i]);
        nt.tk0_vz.push_back(v0.track_vz[i]);
        nt.tk0_px.push_back(v0.track_px[i]);
        nt.tk0_py.push_back(v0.track_py[i]);
        nt.tk0_pz.push_back(v0.track_pz[i]);
        nt.tk0_cov.push_back(v0.track_cov[i]);
      }      
    nt.x0 = v0.x;
    nt.y0 = v0.y;
    nt.z0 = v0.z;
    nt.ntracksptgt30 = int2uchar(v0.ntracksptgt(3));
    nt.drmin0 = v0.drmin();
    nt.drmax0 = v0.drmax();
    nt.njetsntks0 = int2uchar(v0.njets[mfv::JByNtracks]);
    nt.bs2derr0 = v0.bs2derr;
    nt.geo2ddist0 = v0.geo2ddist();
    nt.x1 = nt.y1 = nt.z1 = nt.drmin1 = nt.drmax1 = nt.bs2derr1 = nt.geo2ddist1 = 0;
    nt.ntracksptgt31 = nt.njetsntks1 = 0;
  }
  else if (vertices.size() >= 2) {
    const MFVVertexAux& v0 = vertices[0];
    const MFVVertexAux& v1 = vertices[1];
    nt.nvtx = int2uchar(int(vertices.size()));
    nt.ntk0 = int2uchar(v0.ntracks());
    nt.ntk1 = int2uchar(v1.ntracks());
    if (save_tracks) {
      for (int i = 0, ie = v0.ntracks(); i < ie; ++i) {
        nt.tk0_chi2.push_back(v0.track_chi2[i]);
        nt.tk0_ndof.push_back(v0.track_ndof[i]);
        nt.tk0_vx.push_back(v0.track_vx[i]);
        nt.tk0_vy.push_back(v0.track_vy[i]);
        nt.tk0_vz.push_back(v0.track_vz[i]);
        nt.tk0_px.push_back(v0.track_px[i]);
        nt.tk0_py.push_back(v0.track_py[i]);
        nt.tk0_pz.push_back(v0.track_pz[i]);
        nt.tk0_cov.push_back(v0.track_cov[i]);
      }      
      for (int i = 0, ie = v1.ntracks(); i < ie; ++i) {
        nt.tk1_chi2.push_back(v1.track_chi2[i]);
        nt.tk1_ndof.push_back(v1.track_ndof[i]);
        nt.tk1_vx.push_back(v1.track_vx[i]);
        nt.tk1_vy.push_back(v1.track_vy[i]);
        nt.tk1_vz.push_back(v1.track_vz[i]);
        nt.tk1_px.push_back(v1.track_px[i]);
        nt.tk1_py.push_back(v1.track_py[i]);
        nt.tk1_pz.push_back(v1.track_pz[i]);
        nt.tk1_cov.push_back(v1.track_cov[i]);
      }      
    }
    nt.x0 = v0.x; nt.y0 = v0.y; nt.z0 = v0.z;
    nt.x1 = v1.x; nt.y1 = v1.y; nt.z1 = v1.z;
    nt.ntracksptgt30 = int2uchar(v0.ntracksptgt(3));
    nt.drmin0 = v0.drmin();
    nt.drmax0 = v0.drmax();
    nt.njetsntks0 = int2uchar(v0.njets[mfv::JByNtracks]);
    nt.bs2derr0 = v0.bs2derr;
    nt.geo2ddist0 = v0.geo2ddist();
    nt.ntracksptgt31 = int2uchar(v1.ntracksptgt(3));
    nt.drmin1 = v1.drmin();
    nt.drmax1 = v1.drmax();
    nt.njetsntks1 = int2uchar(v1.njets[mfv::JByNtracks]);
    nt.bs2derr1 = v1.bs2derr;
    nt.geo2ddist1 = v1.geo2ddist();
  }
  else
    return;

  tree->Fill();
}

DEFINE_FWK_MODULE(MFVMiniTreer);
