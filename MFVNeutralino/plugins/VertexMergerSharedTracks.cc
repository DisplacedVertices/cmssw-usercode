#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "RecoVertex/ConfigurableVertexReco/interface/ConfigurableVertexReconstructor.h"
#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"

class MFVVertexMergerSharedTracks : public edm::EDProducer {
public:
  MFVVertexMergerSharedTracks(const edm::ParameterSet&);

  virtual void produce(edm::Event&, const edm::EventSetup&);

private:
  std::pair<double,double> computeSharedTracks(const reco::Vertex&, const reco::Vertex&) const;

  VertexDistance3D vertex_dist;
  std::auto_ptr<VertexReconstructor> vertex_reco;

  const edm::InputTag vertex_src;
  const double min_track_weight;
  const double max_frac;
  const double min_sig;
  const double max_new_chi2dof;
  const bool debug;
};

MFVVertexMergerSharedTracks::MFVVertexMergerSharedTracks(const edm::ParameterSet& cfg)
  : vertex_reco(new ConfigurableVertexReconstructor(cfg.getParameter<edm::ParameterSet>("vertex_reco"))),
    vertex_src(cfg.getParameter<edm::InputTag>("secondaryVertices")),
    min_track_weight(cfg.getParameter<double>("min_track_weight")),
    max_frac(cfg.getParameter<double>("max_frac")),
    min_sig(cfg.getParameter<double>("min_sig")),
    max_new_chi2dof(cfg.getParameter<double>("max_new_chi2dof")),
    debug(cfg.getUntrackedParameter<bool>("debug", false))
{
  produces<reco::VertexCollection>();
}

std::pair<double,double> MFVVertexMergerSharedTracks::computeSharedTracks(const reco::Vertex& sv0, const reco::Vertex& sv1) const {
  std::set<reco::TrackRef> tracks;
  int totals[2] = {0};
  for (int i = 0; i < 2; ++i) {
    const reco::Vertex& sv = i == 0 ? sv0 : sv1;
    for (auto it = sv.tracks_begin(), ite = sv.tracks_end(); it != ite; ++it)
      if (sv.trackWeight(*it) >= min_track_weight) {
        ++totals[i];
        tracks.insert(it->castTo<reco::TrackRef>());
      }
  }
  
  double shared = totals[0] + totals[1] - tracks.size();
  return std::make_pair(shared/totals[0], shared/totals[1]);
}

void MFVVertexMergerSharedTracks::produce(edm::Event& event, const edm::EventSetup& setup) {
  static const bool debug = true;

  edm::ESHandle<TransientTrackBuilder> tt_builder;
  setup.get<TransientTrackRecord>().get("TransientTrackBuilder", tt_builder);

  edm::Handle<reco::VertexCollection> vertices;
  event.getByLabel(vertex_src, vertices);

  std::auto_ptr<reco::VertexCollection> new_vertices(new reco::VertexCollection);
  for (const reco::Vertex& sv : *vertices)
    new_vertices->push_back(sv);

  for (std::vector<reco::Vertex>::iterator sv = new_vertices->begin(), sve = new_vertices->end(); sv != sve; ++sv) {
    bool shared = false;
    std::vector<reco::Vertex>::iterator other_sv;

    for (std::vector<reco::Vertex>::iterator sv2 = new_vertices->begin(), sv2e = new_vertices->end(); sv2 != sv2e; ++sv2) {
      if (sv == sv2)
        continue;

      std::pair<double,double> shared_fracs = computeSharedTracks(*sv2, *sv);
      double sig = vertex_dist.distance(*sv, *sv2).significance();
      if (debug) printf("sv %i sv2 %i fr %f fr2 %f sig %f\n", int(sv-new_vertices->begin()), int(sv2-new_vertices->begin()), shared_fracs.first, shared_fracs.second, sig);

      if (shared_fracs.first > max_frac && sig < min_sig && shared_fracs.first >= shared_fracs.second) {
        if (debug) printf("SHARED!\n");
        other_sv = sv2;
        shared = true;
        break;
      }
    }

    if (shared) {
      std::set<reco::TrackRef> tracks_seen;
      std::vector<reco::TransientTrack> ttks;
      int totals[2] = {0};
      for (int i = 0; i < 2; ++i) {
        const reco::Vertex& v = i == 0 ? *sv : *other_sv;
        for (std::vector<reco::TrackBaseRef>::const_iterator it = v.tracks_begin(), ite = v.tracks_end(); it != ite; ++it) {
          if (v.trackWeight(*it) >= min_track_weight) {
            ++totals[i];
            reco::TrackRef tk = it->castTo<reco::TrackRef>();
            if (tracks_seen.count(tk) < 1) {
              tracks_seen.insert(tk);
              ttks.push_back(tt_builder->build(tk));
            }
          }
        }
      }

      if (debug) printf("in shared merge: tracks in sv: %i/%i tracks in sv2: %i/%i; num total with weight > min and remove shared %i\n", totals[0], int(sv->tracks_end() - sv->tracks_begin()), totals[1], int(other_sv->tracks_end() - other_sv->tracks_begin()), int(ttks.size()));

      std::vector<TransientVertex> vertices = vertex_reco->vertices(ttks);
      if (debug) printf("in shared: num verts found: %i\n", int(vertices.size()));

      new_vertices->erase(other_sv);
      new_vertices->erase(sv);
      sv = new_vertices->begin(); // start over completely

      for (std::vector<TransientVertex>::const_iterator v = vertices.begin(), ve = vertices.end(); v != ve; ++v)
        if (v->normalisedChiSquared() < max_new_chi2dof)
          new_vertices->push_back(reco::Vertex(*v));
    }
  }

  event.put(new_vertices);
}

DEFINE_FWK_MODULE(MFVVertexMergerSharedTracks);
