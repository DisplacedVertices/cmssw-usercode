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
  typedef std::set<reco::TrackRef> track_set;
  struct share_info {
    void set(int s, int t0, int t1) {
      shared = s;
      totals[0] = t0;
      totals[1] = t1;
      total = t0+t1;
      fracs[0] = t0 > 0 ? double(s)/t0 : -1;
      fracs[1] = t1 > 0 ? double(s)/t1 : -1;
    }

    void set(int s) {
      set(s, totals[0], totals[1]);
    }

    share_info() {
      set(0,0,0);
    }

    int shared;
    int totals[2];
    int total;
    double fracs[2];
    track_set tracks;
  };

  track_set vertexTrackSet(const reco::Vertex&, double min_weight=0, bool extra_debug=false) const;
  share_info computeSharedTracks(const reco::Vertex&, const reco::Vertex&) const;

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

MFVVertexMergerSharedTracks::track_set MFVVertexMergerSharedTracks::vertexTrackSet(const reco::Vertex& v, double min_weight, bool extra_debug) const {
  std::set<reco::TrackRef> result;
  for (auto it = v.tracks_begin(), ite = v.tracks_end(); it != ite; ++it) {
    double w = v.trackWeight(*it);
    bool use = w >= min_weight;
    if (debug && extra_debug) printf("trk #%2i pt %6.3f eta %6.3f phi %6.3f dxy %6.3f dz %6.3f w %5.3f  use? %i\n", int(it-v.tracks_begin()), (*it)->pt(), (*it)->eta(), (*it)->phi(), (*it)->dxy(), (*it)->dz(), w, use);
    if (use)
      result.insert(it->castTo<reco::TrackRef>());
  }

  if (debug) {
    printf("track set: ");
    for (auto r : result)
      printf("(%i,%u) ", r.id().id(), r.key());
    printf("\n");
  }

  return result;
}

MFVVertexMergerSharedTracks::share_info MFVVertexMergerSharedTracks::computeSharedTracks(const reco::Vertex& sv0, const reco::Vertex& sv1) const {
  share_info result;

  for (int i = 0; i < 2; ++i) {
    const reco::Vertex& sv = i == 0 ? sv0 : sv1;
    if (debug) printf("computeSharedtracks sv #%i\n", i);
    track_set tracks = vertexTrackSet(sv, min_track_weight, true);
    result.totals[i] += tracks.size();
    result.tracks.insert(tracks.begin(), tracks.end());
  }
  
  int shared = result.totals[0] + result.totals[1] - result.tracks.size();
  result.set(shared);
  return result;
}

void MFVVertexMergerSharedTracks::produce(edm::Event& event, const edm::EventSetup& setup) {
  edm::ESHandle<TransientTrackBuilder> tt_builder;
  setup.get<TransientTrackRecord>().get("TransientTrackBuilder", tt_builder);

  edm::Handle<reco::VertexCollection> vertices;
  event.getByLabel(vertex_src, vertices);

  std::auto_ptr<reco::VertexCollection> new_vertices(new reco::VertexCollection);
  for (const reco::Vertex& sv : *vertices)
    new_vertices->push_back(sv);

  if (debug) printf("run: %u lumi: %u event: %u  # input vertices: %i\n", event.id().run(), event.luminosityBlock(), event.id().event(), int(vertices->size()));

  int num_duplicate = 0;
  int num_shared = 0;

  // First, look for duplicates and remove them.
  if (debug) printf("looking for duplicates:\n");
  for (std::vector<reco::Vertex>::iterator sv0 = new_vertices->begin(); sv0 != new_vertices->end(); ++sv0) {
    if (debug) printf("sv0 #%i ", int(sv0-new_vertices->begin()));
    track_set tks0 = vertexTrackSet(*sv0);

    for (std::vector<reco::Vertex>::iterator sv1 = sv0+1; sv1 != new_vertices->end(); ++sv1) {
      if (debug) printf("sv1 #%i ", int(sv1-new_vertices->begin()));
      track_set tks1 = vertexTrackSet(*sv1);

      if (tks1 == tks0) {
        ++num_duplicate;
        sv1 = new_vertices->erase(sv1)-1;
        if (debug) printf("duplicate!\n");
      }
    }
  }

  if (debug) printf("# duplicates removed: %i  # vertices left: %i\n", num_duplicate, int(new_vertices->size()));

  for (std::vector<reco::Vertex>::iterator sv = new_vertices->begin(), sve = new_vertices->end(); sv != sve; ++sv) {
    bool shared = false;
    share_info sharing;
    std::vector<reco::Vertex>::iterator other_sv;

    for (std::vector<reco::Vertex>::iterator sv2 = sv+1, sv2e = new_vertices->end(); sv2 != sv2e; ++sv2) {
      Measurement1D dist = vertex_dist.distance(*sv, *sv2);
      double sig = dist.significance();
      if (sig > min_sig)
        continue;

      if (debug) printf("computeShared for sv %i and %i, with dist %6.3f +/- %6.3f: sig %6.3f\n", int(sv-new_vertices->begin()), int(sv2-new_vertices->begin()), dist.value(), dist.error(), sig);
      sharing = computeSharedTracks(*sv2, *sv);

      if (debug) printf("sv0 #%i sv1 #%i: total0 %i total1 %i total %i shared %i frac0 %f frac1 %f \n", int(sv-new_vertices->begin()), int(sv2-new_vertices->begin()), sharing.totals[0], sharing.totals[1], sharing.total, sharing.shared, sharing.fracs[0], sharing.fracs[1]);

      if (sharing.fracs[0] > max_frac && sharing.fracs[0] >= sharing.fracs[1]) {
        if (debug) printf("SHARED!\n");
        other_sv = sv2;
        shared = true;
        break;
      }
    }

    if (shared) {
      ++num_shared;

      std::vector<reco::TransientTrack> ttks;
      for (const reco::TrackRef& tk : sharing.tracks)
        ttks.push_back(tt_builder->build(tk));
      
      if (debug) printf("in shared merge: tracks in sv: %i/%i tracks in sv2: %i/%i; num total with weight > min and remove shared: %i\n", sharing.totals[0], int(sv->tracks_end() - sv->tracks_begin()), sharing.totals[1], int(other_sv->tracks_end() - other_sv->tracks_begin()), int(ttks.size()));

      std::vector<TransientVertex> vertices = vertex_reco->vertices(ttks);
      if (debug) printf("in shared: num verts found: %i\n", int(vertices.size()));

      new_vertices->erase(other_sv); // erase other_sv first since it comes after sv
      new_vertices->erase(sv);

      for (std::vector<TransientVertex>::const_iterator v = vertices.begin(), ve = vertices.end(); v != ve; ++v)
        if (v->normalisedChiSquared() < max_new_chi2dof)
          new_vertices->push_back(reco::Vertex(*v));

      // start over completely
      sv  = new_vertices->begin()-1; // -1 because about to ++sv
      sve = new_vertices->end();
    }
  }

  event.put(new_vertices);
}

DEFINE_FWK_MODULE(MFVVertexMergerSharedTracks);
