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
  const double max_chi2dof;
  const double max_err2d;
  const double max_err3d;
  const double min_mass;
  const double min_drmin;
  const double max_drmin;
  const double min_drmax;
  const double max_drmax;
  const double min_gen3dsig;
  const double max_gen3dsig;
  const double min_maxtrackpt;
  const double max_bs2derr;
  const int min_njetssharetks;
  const int max_njetssharetks;
};

MFVVertexSelector::MFVVertexSelector(const edm::ParameterSet& cfg) 
  : vertex_aux_src(cfg.getParameter<edm::InputTag>("vertex_aux_src")),
    produce_refs(cfg.getParameter<bool>("produce_refs")),
    sorter(cfg.getParameter<std::string>("sort_by")),
    min_ntracks(cfg.getParameter<int>("min_ntracks")),
    max_chi2dof(cfg.getParameter<double>("max_chi2dof")),
    max_err2d(cfg.getParameter<double>("max_err2d")),
    max_err3d(cfg.getParameter<double>("max_err3d")),
    min_mass(cfg.getParameter<double>("min_mass")),
    min_drmin(cfg.getParameter<double>("min_drmin")),
    max_drmin(cfg.getParameter<double>("max_drmin")),
    min_drmax(cfg.getParameter<double>("min_drmax")),
    max_drmax(cfg.getParameter<double>("max_drmax")),
    min_gen3dsig(cfg.getParameter<double>("min_gen3dsig")),
    max_gen3dsig(cfg.getParameter<double>("max_gen3dsig")),
    min_maxtrackpt(cfg.getParameter<double>("min_maxtrackpt")),
    max_bs2derr(cfg.getParameter<double>("max_bs2derr")),
    min_njetssharetks(cfg.getParameter<int>("min_njetssharetks")),
    max_njetssharetks(cfg.getParameter<int>("max_njetssharetks"))
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
    vtx.chi2/vtx.ndof < max_chi2dof &&
    vtx.gen2derr < max_err2d &&
    vtx.gen3derr < max_err3d &&
    vtx.mass >= min_mass && 
    vtx.drmin >= min_drmin &&
    vtx.drmin <  max_drmin &&
    vtx.drmax >= min_drmax &&
    vtx.drmax <  max_drmax &&
    vtx.gen3dsig() >= min_gen3dsig &&
    vtx.gen3dsig() <  max_gen3dsig &&
    vtx.maxtrackpt >= min_maxtrackpt &&
    vtx.bs2derr < max_bs2derr &&
    vtx.njets[0] >= min_njetssharetks;
    vtx.njets[0] <= max_njetssharetks;
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
