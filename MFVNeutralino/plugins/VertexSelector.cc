#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "JMTucker/MFVNeutralino/interface/VertexTools.h"

class MFVVertexSelector : public edm::EDProducer {
public:
  explicit MFVVertexSelector(const edm::ParameterSet&);

private:
  virtual void produce(edm::Event&, const edm::EventSetup&);

  bool use_vertex(const reco::Vertex&) const;

  const edm::InputTag vertex_src;
  const edm::InputTag gen_vertices_src;
  const double track_vertex_weight_min;
  const int min_ntracks;
  const double max_chi2dof;
  const double max_err2d;
  const double max_err3d;
  const double min_mass;
  const double min_drmax;
  const double min_gen3dsig;
  const double max_gen3dsig;

  bool gen_valid;
  std::vector<double> gen_verts;
};

MFVVertexSelector::MFVVertexSelector(const edm::ParameterSet& cfg) 
  : vertex_src(cfg.getParameter<edm::InputTag>("vertex_src")),
    gen_vertices_src(cfg.getParameter<edm::InputTag>("gen_vertices_src")),
    track_vertex_weight_min(cfg.getParameter<double>("track_vertex_weight_min")),
    min_ntracks(cfg.getParameter<int>("min_ntracks")),
    max_chi2dof(cfg.getParameter<double>("max_chi2dof")),
    max_err2d(cfg.getParameter<double>("max_err2d")),
    max_err3d(cfg.getParameter<double>("max_err3d")),
    min_mass(cfg.getParameter<double>("min_mass")),
    min_drmax(cfg.getParameter<double>("min_drmax")),
    min_gen3dsig(cfg.getParameter<double>("min_gen3dsig")),
    max_gen3dsig(cfg.getParameter<double>("max_gen3dsig"))
{
  produces<reco::VertexCollection>();
}

bool MFVVertexSelector::use_vertex(const reco::Vertex& vtx) const {
  const bool use =
    int(vtx.tracksSize()) >= min_ntracks && // JMTBAD use nTracks(0.5)
    vtx.normalizedChi2() < max_chi2dof   &&
    vtx.p4().mass() >= min_mass          &&
    mfv::abs_error(vtx, false) < max_err2d    &&
    mfv::abs_error(vtx, true ) < max_err3d    &&
    (min_drmax == 0 || mfv::vertex_tracks_distance(vtx, track_vertex_weight_min).drmax >= min_drmax);

  if (!use)
    return false;

  const float gd3sg = mfv::gen_dist(vtx, gen_verts, true).significance();
  return use && (!gen_valid || (gd3sg >= min_gen3dsig && gd3sg < max_gen3dsig));
}

void MFVVertexSelector::produce(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<std::vector<double> > gen_vertices;
  event.getByLabel(gen_vertices_src, gen_vertices);
  gen_valid = gen_vertices->size() == 6;
  if (gen_valid)
    gen_verts = *gen_vertices;

  edm::Handle<reco::VertexCollection> vertices;
  event.getByLabel(vertex_src, vertices);

  std::auto_ptr<reco::VertexCollection> selected_vertices(new reco::VertexCollection);

  for (const reco::Vertex& v : *vertices)
    if (use_vertex(v))
      selected_vertices->push_back(v);

  std::sort(selected_vertices->begin(), selected_vertices->end(),
            [](const reco::Vertex& a, const reco::Vertex& b) { return a.p4().mass() > b.p4().mass(); });

  event.put(selected_vertices);
}

DEFINE_FWK_MODULE(MFVVertexSelector);
