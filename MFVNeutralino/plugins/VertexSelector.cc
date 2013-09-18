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

  bool use_vertex(const reco::Vertex& vtx, const reco::BeamSpot& beamspot, const reco::Vertex* primary_vertex) const;

  const edm::InputTag vertex_src;
  const edm::InputTag primary_vertex_src;
  const edm::InputTag gen_vertices_src;
  const double track_vertex_weight_min;
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

  enum sort_by_this { sort_by_mass, sort_by_ntracks };
  sort_by_this sort_by;

  bool gen_valid;
  std::vector<double> gen_verts;
};

MFVVertexSelector::MFVVertexSelector(const edm::ParameterSet& cfg) 
  : vertex_src(cfg.getParameter<edm::InputTag>("vertex_src")),
    primary_vertex_src(cfg.getParameter<edm::InputTag>("primary_vertex_src")),
    gen_vertices_src(cfg.getParameter<edm::InputTag>("gen_vertices_src")),
    track_vertex_weight_min(cfg.getParameter<double>("track_vertex_weight_min")),
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
    min_njetssharetks(cfg.getParameter<int>("min_njetssharetks"))
{
  produces<reco::VertexCollection>();

  std::string x = cfg.getParameter<std::string>("sort_by");
  if (x == "mass")
    sort_by = sort_by_mass;
  else if (x == "ntracks")
    sort_by = sort_by_ntracks;
  else
    throw cms::Exception("MFVVertexSelector") << "invalid sort_by";
}

bool MFVVertexSelector::use_vertex(const reco::Vertex& vtx, const reco::BeamSpot& beamspot, const reco::Vertex* primary_vertex) const {
  bool use =
    int(vtx.tracksSize()) >= min_ntracks && // JMTBAD use nTracks(0.5)
    vtx.normalizedChi2() < max_chi2dof   &&
    vtx.p4().mass() >= min_mass;

  if (!use) return false;

  if (max_err2d < 1e6)
    use = use && mfv::abs_error(vtx, false) < max_err2d;

  if (!use) return false;

  if (max_err3d < 1e6)
    use = use && mfv::abs_error(vtx, true) < max_err3d;

  if (!use) return false;

  if (min_drmin > 0 || min_drmax > 0 || max_drmin < 1e6 || max_drmax < 1e6 || min_maxtrackpt > 0) {
    mfv::vertex_tracks_distance tks(vtx, track_vertex_weight_min);
    use = use && tks.drmin >= min_drmin && tks.drmin < max_drmin
              && tks.drmax >= min_drmax && tks.drmax < max_drmax
              && tks.maxtrackpt >= min_maxtrackpt;
  }

  if (!use) return false;
  
  if (gen_valid) {
    const float gd3sg = mfv::gen_dist(vtx, gen_verts, true).significance();
    use = use && gd3sg >= min_gen3dsig && gd3sg < max_gen3dsig;
  }

  if (!use) return false;

  if (max_bs2derr < 1e6) {
    mfv::vertex_distances dst(vtx, gen_verts, beamspot, primary_vertex);
    use = use && dst.bs2ddist.error() < max_bs2derr;
  }

  return use;
}

void MFVVertexSelector::produce(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<std::vector<double> > gen_vertices;
  event.getByLabel(gen_vertices_src, gen_vertices);
  gen_valid = gen_vertices->size() == 6;
  if (gen_valid)
    gen_verts = *gen_vertices;

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByLabel("offlineBeamSpot", beamspot);

  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByLabel(primary_vertex_src, primary_vertices);
  const reco::Vertex* primary_vertex = 0;
  if (primary_vertices->size())
    primary_vertex = &primary_vertices->at(0);

  edm::Handle<reco::VertexCollection> vertices;
  event.getByLabel(vertex_src, vertices);

  std::auto_ptr<reco::VertexCollection> selected_vertices(new reco::VertexCollection);

  for (const reco::Vertex& v : *vertices)
    if (use_vertex(v, *beamspot, primary_vertex))
      selected_vertices->push_back(v);

  if (sort_by == sort_by_mass)
    std::sort(selected_vertices->begin(), selected_vertices->end(), [](const reco::Vertex& a, const reco::Vertex& b) { return a.p4().mass() > b.p4().mass(); });
  else if (sort_by == sort_by_ntracks)
    std::sort(selected_vertices->begin(), selected_vertices->end(), [](const reco::Vertex& a, const reco::Vertex& b) { return a.nTracks() > b.nTracks(); });

  event.put(selected_vertices);
}

DEFINE_FWK_MODULE(MFVVertexSelector);
