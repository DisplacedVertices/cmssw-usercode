#include "TTree.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/MFVNeutralino/interface/FlatNtuple.h"

class MFVFlatTreer : public edm::EDAnalyzer {
public:
  explicit MFVFlatTreer(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

  const edm::InputTag event_src;
  const edm::InputTag vertex_src;
  const int sample;

  mfv::FlatNtuple nt;
  TTree* tree;
};

MFVFlatTreer::MFVFlatTreer(const edm::ParameterSet& cfg)
  : event_src(cfg.getParameter<edm::InputTag>("event_src")),
    vertex_src(cfg.getParameter<edm::InputTag>("vertex_src")),
    sample(cfg.getParameter<int>("sample"))
{
  assert(sample <= 255);
  edm::Service<TFileService> fs;
  tree = fs->make<TTree>("t", "");
  mfv::write_to_tree(tree, nt);
}

void MFVFlatTreer::analyze(const edm::Event& event, const edm::EventSetup&) {
  nt.clear();

  nt.run   = event.id().run();
  nt.lumi  = event.luminosityBlock();
  nt.event = event.id().event();
  nt.sample = sample;

  edm::Handle<MFVEvent> mevent;
  event.getByLabel(event_src, mevent);

  nt.gen_valid = mevent->gen_valid;
  for (int i = 0; i < 2; ++i) {
    nt.gen_lsp_pt[i] = mevent->gen_lsp_pt[i];
    nt.gen_lsp_eta[i] = mevent->gen_lsp_eta[i];
    nt.gen_lsp_phi[i] = mevent->gen_lsp_phi[i];
    nt.gen_lsp_mass[i] = mevent->gen_lsp_mass[i];
    nt.gen_decay_type[i] = mevent->gen_decay_type[i];
  }
  for (int i = 0; i < 6; ++i)
    nt.gen_lsp_decay[i] = mevent->gen_lsp_decay[i];
  nt.gen_partons_in_acc = mevent->gen_partons_in_acc;
  nt.npu = mevent->npu;
  nt.bsx = mevent->bsx;
  nt.bsy = mevent->bsy;
  nt.bsz = mevent->bsz;
  nt.bsdxdz = mevent->bsdxdz;
  nt.bsdydz = mevent->bsdydz;
  nt.bswidthx = mevent->bswidthx;
  nt.bswidthy = mevent->bswidthy;
  nt.npv = mevent->npv;
  nt.pvx = mevent->pvx;
  nt.pvy = mevent->pvy;
  nt.pvz = mevent->pvz;
  nt.pv_ntracks = mevent->pv_ntracks;
  nt.pv_sumpt2 = mevent->pv_sumpt2;
  nt.jet_id = mevent->jet_id;
  nt.jet_pt = mevent->jet_pt;
  nt.jet_eta = mevent->jet_eta;
  nt.jet_phi = mevent->jet_phi;
  nt.jet_energy = mevent->jet_energy;
  nt.metx = mevent->metx;
  nt.mety = mevent->mety;
  nt.metsig = mevent->metsig;
  nt.metdphimin = mevent->metdphimin;
  nt.lep_id = mevent->lep_id;
  nt.lep_pt = mevent->lep_pt;
  nt.lep_eta = mevent->lep_eta;
  nt.lep_phi = mevent->lep_phi;
  nt.lep_dxy = mevent->lep_dxy;
  nt.lep_dz = mevent->lep_dz;
  nt.lep_iso = mevent->lep_iso;
  nt.lep_mva = mevent->lep_mva;
  
  edm::Handle<MFVVertexAuxCollection> vertices;
  event.getByLabel(vertex_src, vertices);

  nt.nvertices = vertices->size();

  for (const MFVVertexAux& v : *vertices) {
    unsigned char nmu = 0, nel = 0;
    for (unsigned char w : v.which_lep) {
      if (w & (1<<7))
        ++nel;
      else
        ++nmu;
    }
    nt.vtx_nmu.push_back(nmu);
    nt.vtx_nel.push_back(nel);
    nt.vtx_x.push_back(v.x);
    nt.vtx_y.push_back(v.y);
    nt.vtx_z.push_back(v.z);
    nt.vtx_cxx.push_back(v.cxx);
    nt.vtx_cxy.push_back(v.cxy);
    nt.vtx_cxz.push_back(v.cxz);
    nt.vtx_cyy.push_back(v.cyy);
    nt.vtx_cyz.push_back(v.cyz);
    nt.vtx_czz.push_back(v.czz);
    nt.vtx_chi2.push_back(v.chi2);
    nt.vtx_ndof.push_back(v.ndof);
    nt.vtx_njets.push_back(v.njets[0]);
    nt.vtx_tks_pt.push_back(v.pt[0]);
    nt.vtx_tks_eta.push_back(v.eta[0]);
    nt.vtx_tks_phi.push_back(v.phi[0]);
    nt.vtx_tks_mass.push_back(v.mass[0]);
    nt.vtx_jets_pt.push_back(v.pt[1]);
    nt.vtx_jets_eta.push_back(v.eta[1]);
    nt.vtx_jets_phi.push_back(v.phi[1]);
    nt.vtx_jets_mass.push_back(v.mass[1]);
    nt.vtx_tksjets_pt.push_back(v.pt[2]);
    nt.vtx_tksjets_eta.push_back(v.eta[2]);
    nt.vtx_tksjets_phi.push_back(v.phi[2]);
    nt.vtx_tksjets_mass.push_back(v.mass[2]);
    nt.vtx_jetpairdetamin.push_back(v.jetpairdetamin);
    nt.vtx_jetpairdetamax.push_back(v.jetpairdetamax);
    nt.vtx_jetpairdetaavg.push_back(v.jetpairdetaavg);
    nt.vtx_jetpairdetarms.push_back(v.jetpairdetarms);
    nt.vtx_jetpairdrmin.push_back(v.jetpairdrmin);
    nt.vtx_jetpairdrmax.push_back(v.jetpairdrmax);
    nt.vtx_jetpairdravg.push_back(v.jetpairdravg);
    nt.vtx_jetpairdrrms.push_back(v.jetpairdrrms);
    nt.vtx_costhtkmomvtxdispmin.push_back(v.costhtkmomvtxdispmin);
    nt.vtx_costhtkmomvtxdispmax.push_back(v.costhtkmomvtxdispmax);
    nt.vtx_costhtkmomvtxdispavg.push_back(v.costhtkmomvtxdispavg);
    nt.vtx_costhtkmomvtxdisprms.push_back(v.costhtkmomvtxdisprms);
    nt.vtx_costhjetmomvtxdispmin.push_back(v.costhjetmomvtxdispmin);
    nt.vtx_costhjetmomvtxdispmax.push_back(v.costhjetmomvtxdispmax);
    nt.vtx_costhjetmomvtxdispavg.push_back(v.costhjetmomvtxdispavg);
    nt.vtx_costhjetmomvtxdisprms.push_back(v.costhjetmomvtxdisprms);
    nt.vtx_gen2ddist.push_back(v.gen2ddist);
    nt.vtx_gen2derr.push_back(v.gen2derr);
    nt.vtx_gen3ddist.push_back(v.gen3ddist);
    nt.vtx_gen3derr.push_back(v.gen3derr);
    nt.vtx_bs2ddist.push_back(v.bs2ddist);
    nt.vtx_bs2derr.push_back(v.bs2derr);
    nt.vtx_pv2ddist.push_back(v.pv2ddist);
    nt.vtx_pv2derr.push_back(v.pv2derr);
    nt.vtx_pv3ddist.push_back(v.pv3ddist);
    nt.vtx_pv3derr.push_back(v.pv3derr);
    nt.vtx_ntracks.push_back(v.ntracks());
    nt.vtx_nbadtracks.push_back(v.nbadtracks());
    nt.vtx_ntracksptgt3.push_back(v.ntracksptgt(3));
    nt.vtx_ntracksptgt5.push_back(v.ntracksptgt(5));
    nt.vtx_ntracksptgt10.push_back(v.ntracksptgt(10));
    nt.vtx_trackminnhits.push_back(v.trackminnhits());
    nt.vtx_trackmaxnhits.push_back(v.trackmaxnhits());
    nt.vtx_sumpt2.push_back(v.sumpt2());
    nt.vtx_sumnhitsbehind.push_back(v.sumnhitsbehind());
    nt.vtx_maxnhitsbehind.push_back(v.maxnhitsbehind());
    nt.vtx_ntrackssharedwpv.push_back(v.ntrackssharedwpv());
    nt.vtx_ntrackssharedwpvs.push_back(v.ntrackssharedwpvs());
    nt.vtx_npvswtracksshared.push_back(v.npvswtracksshared());
    nt.vtx_pvmosttracksshared.push_back(v.pvmosttracksshared());
    nt.vtx_mintrackpt.push_back(v.mintrackpt());
    nt.vtx_maxtrackpt.push_back(v.maxtrackpt());
    nt.vtx_maxm1trackpt.push_back(v.maxmntrackpt(1));
    nt.vtx_maxm2trackpt.push_back(v.maxmntrackpt(2));
    nt.vtx_trackpairdrmin.push_back(v.trackpairdrmin());
    nt.vtx_trackpairdrmax.push_back(v.trackpairdrmax());
    nt.vtx_trackpairdravg.push_back(v.trackpairdravg());
    nt.vtx_trackpairdrrms.push_back(v.trackpairdrrms());
  }

  tree->Fill();
}

DEFINE_FWK_MODULE(MFVFlatTreer);
