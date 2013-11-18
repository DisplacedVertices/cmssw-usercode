#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "JMTucker/MFVNeutralino/interface/VertexAux.h"
#include "JMTucker/MFVNeutralino/interface/VertexTools.h"

class MFVVertexSelector : public edm::EDProducer {
public:
  explicit MFVVertexSelector(const edm::ParameterSet&);

private:
  virtual void produce(edm::Event&, const edm::EventSetup&);

  bool use_vertex(const MFVVertexAux& vtx) const;

  const edm::InputTag vertex_aux_src;
  const bool produce_refs;
  const MFVVertexAuxSorter sorter;

  const int min_ntracks;
  const int min_ntracksptgt3;
  const int min_ntracksptgt5;
  const int min_ntracksptgt10;
  const int min_njetssharetks;
  const double min_jetsmassntks;
  const double max_chi2dof;
  const double min_p;
  const double min_pt;
  const double max_abs_eta;
  const double max_abs_rapidity;
  const double min_mass;
  const double min_costhmombs;
  const double min_costhjetntkmombs;
  const double min_sumpt2;
  const double min_maxtrackpt;
  const double min_maxm1trackpt;
  const double min_maxm2trackpt;
  const double min_drmin;
  const double max_drmin;
  const double min_drmax;
  const double max_drmax;
  const double max_err2d;
  const double max_err3d;
  const double min_gen3dsig;
  const double max_gen3dsig;
  const double min_bs2ddist;
  const double max_bs2derr;
  const double min_bs2dsig;
  const double min_bs3ddist;
};

MFVVertexSelector::MFVVertexSelector(const edm::ParameterSet& cfg) 
  : vertex_aux_src(cfg.getParameter<edm::InputTag>("vertex_aux_src")),
    produce_refs(cfg.getParameter<bool>("produce_refs")),
    sorter(cfg.getParameter<std::string>("sort_by")),
    min_ntracks(cfg.getParameter<int>("min_ntracks")),
    min_ntracksptgt3(cfg.getParameter<int>("min_ntracksptgt3")),
    min_ntracksptgt5(cfg.getParameter<int>("min_ntracksptgt5")),
    min_ntracksptgt10(cfg.getParameter<int>("min_ntracksptgt10")),
    min_njetssharetks(cfg.getParameter<int>("min_njetssharetks")),
    min_jetsmassntks(cfg.getParameter<double>("min_jetsmassntks")),
    max_chi2dof(cfg.getParameter<double>("max_chi2dof")),
    min_p(cfg.getParameter<double>("min_p")),
    min_pt(cfg.getParameter<double>("min_pt")),
    max_abs_eta(cfg.getParameter<double>("max_abs_eta")),
    max_abs_rapidity(cfg.getParameter<double>("max_abs_rapidity")),
    min_mass(cfg.getParameter<double>("min_mass")),
    min_costhmombs(cfg.getParameter<double>("min_costhmombs")),
    min_costhjetntkmombs(cfg.getParameter<double>("min_costhjetntkmombs")),
    min_sumpt2(cfg.getParameter<double>("min_sumpt2")),
    min_maxtrackpt(cfg.getParameter<double>("min_maxtrackpt")),
    min_maxm1trackpt(cfg.getParameter<double>("min_maxm1trackpt")),
    min_maxm2trackpt(cfg.getParameter<double>("min_maxm2trackpt")),
    min_drmin(cfg.getParameter<double>("min_drmin")),
    max_drmin(cfg.getParameter<double>("max_drmin")),
    min_drmax(cfg.getParameter<double>("min_drmax")),
    max_drmax(cfg.getParameter<double>("max_drmax")),
    max_err2d(cfg.getParameter<double>("max_err2d")),
    max_err3d(cfg.getParameter<double>("max_err3d")),
    min_gen3dsig(cfg.getParameter<double>("min_gen3dsig")),
    max_gen3dsig(cfg.getParameter<double>("max_gen3dsig")),
    min_bs2ddist(cfg.getParameter<double>("min_bs2ddist")),
    max_bs2derr(cfg.getParameter<double>("max_bs2derr")),
    min_bs2dsig(cfg.getParameter<double>("min_bs2dsig")),
    min_bs3ddist(cfg.getParameter<double>("min_bs3ddist"))
{
  if (produce_refs)
    produces<reco::VertexRefVector>();
  else
    produces<reco::VertexCollection>();
  produces<MFVVertexAuxCollection>();
}

bool MFVVertexSelector::use_vertex(const MFVVertexAux& vtx) const {
  return 
    vtx.ntracks >= min_ntracks &&
    vtx.ntracksptgt3 >= min_ntracksptgt3 &&
    vtx.ntracksptgt5 >= min_ntracksptgt5 &&
    vtx.ntracksptgt10 >= min_ntracksptgt10 &&
    vtx.njets[0] >= min_njetssharetks &&
    vtx.jetsmass[0] >= min_jetsmassntks &&
    vtx.chi2/vtx.ndof < max_chi2dof &&
    vtx.p4().P() >= min_p &&
    vtx.pt >= min_pt &&
    fabs(vtx.eta) < max_abs_eta &&
    fabs(vtx.p4().Rapidity()) < max_abs_rapidity &&
    vtx.mass >= min_mass && 
    vtx.costhmombs[0] >= min_costhmombs &&
    vtx.costhmombs[1] >= min_costhjetntkmombs;
    vtx.sumpt2 >= min_sumpt2 &&
    vtx.maxtrackpt >= min_maxtrackpt &&
    vtx.maxm1trackpt >= min_maxm1trackpt &&
    vtx.maxm2trackpt >= min_maxm2trackpt &&
    vtx.drmin >= min_drmin &&
    vtx.drmin <  max_drmin &&
    vtx.drmax >= min_drmax &&
    vtx.drmax <  max_drmax &&
    vtx.gen2derr < max_err2d &&
    vtx.gen3derr < max_err3d &&
    vtx.gen3dsig() >= min_gen3dsig &&
    vtx.gen3dsig() <  max_gen3dsig &&
    vtx.bs2ddist >= min_bs2ddist &&
    vtx.bs2derr < max_bs2derr &&
    vtx.bs2dsig() >= min_bs2dsig &&
    vtx.bs3ddist >= min_bs3ddist;
}

void MFVVertexSelector::produce(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<MFVVertexAuxCollection> auxes;
  event.getByLabel(vertex_aux_src, auxes);

  std::auto_ptr<MFVVertexAuxCollection> selected(new MFVVertexAuxCollection);
  std::auto_ptr<reco::VertexRefVector>  selected_vertex_refs(new reco::VertexRefVector);

  for (const MFVVertexAux& aux : *auxes) {
    if (use_vertex(aux)) {
      MFVVertexAux sel(aux);
      sel.selected = true;
      selected->push_back(sel);
      selected_vertex_refs->push_back(aux.ref);
    }
  }

  sorter.sort(*selected);

  if (!produce_refs) {
    std::auto_ptr<reco::VertexCollection> selected_vertices(new reco::VertexCollection);
    for (const reco::VertexRef& v : *selected_vertex_refs)
      selected_vertices->push_back(*v);
    event.put(selected_vertices);
  }
  else
    event.put(selected_vertex_refs);

  event.put(selected);
}

DEFINE_FWK_MODULE(MFVVertexSelector);
