#include "TH2.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "RecoVertex/ConfigurableVertexReco/interface/ConfigurableVertexReconstructor.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"

class MFVVertexRefitter : public edm::EDProducer {
public:
  MFVVertexRefitter(const edm::ParameterSet&);
  virtual void produce(edm::Event&, const edm::EventSetup&);

private:
  std::unique_ptr<KalmanVertexFitter> kv_reco;

  static const int max_n_input_vertices;

  std::string vertex_collection_name(int i) const {
    char buf[128];
    snprintf(buf, 128, "refitVertices%i", i);
    return std::string(buf);
  }

  const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
  const edm::EDGetTokenT<reco::VertexCollection> vertex_token;
  const unsigned n_tracks_to_drop;
  const bool histos;
  const bool verbose;

  enum SortTracksBy { SortTracksByDxyErr, SortTracksByPt };
  SortTracksBy sort_tracks_by;

#if 0
  VertexDistanceXY vertex_dist_2d;

  TH1F* h_n_vertices;
  TH1F* h_vertex_track_weights;
  TH1F* h_vertex_chi2;
  TH1F* h_vertex_ndof;
  TH1F* h_vertex_x;
  TH1F* h_vertex_y;
  TH1F* h_vertex_rho;
  TH1F* h_vertex_phi;
  TH1F* h_vertex_z;
  TH1F* h_vertex_r;
#endif
};

const int MFVVertexRefitter::max_n_input_vertices = 5;

MFVVertexRefitter::MFVVertexRefitter(const edm::ParameterSet& cfg)
  : kv_reco(new KalmanVertexFitter(cfg.getParameter<edm::ParameterSet>("kvr_params"), cfg.getParameter<edm::ParameterSet>("kvr_params").getParameter<bool>("doSmoothing"))),
    beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot_src"))),
    vertex_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("vertex_src"))),
    n_tracks_to_drop(cfg.getParameter<unsigned>("n_tracks_to_drop")),
    histos(cfg.getUntrackedParameter<bool>("histos", false)),
    verbose(cfg.getUntrackedParameter<bool>("verbose", false))
{
  const std::string& sort_tracks_by_str = cfg.getParameter<std::string>("sort_tracks_by");
  if (sort_tracks_by_str == "dxyerr")
    sort_tracks_by = SortTracksByDxyErr;
  else if (sort_tracks_by_str == "pt")
    sort_tracks_by = SortTracksByPt;
  else
    throw cms::Exception("MFVVertexRefitter") << "sort_tracks_by " << sort_tracks_by_str << " unrecognized";

  for (int i = 0; i < max_n_input_vertices; ++i)
    produces<reco::VertexCollection>(vertex_collection_name(i));

#if 0    
  if (histos) {
    edm::Service<TFileService> fs;
    h_n_vertices                = fs->make<TH1F>("h_n_vertices",                "", 200,   0,    400);
    h_vertex_track_weights      = fs->make<TH1F>("h_vertex_track_weights",      "",  64,   0,      1);
    h_vertex_chi2               = fs->make<TH1F>("h_vertex_chi2",               "", 100,   0,     10);
    h_vertex_ndof               = fs->make<TH1F>("h_vertex_ndof",               "", 100,   0,     20);
    h_vertex_x                  = fs->make<TH1F>("h_vertex_x",                  "", 200,  -1,      1);
    h_vertex_y                  = fs->make<TH1F>("h_vertex_y",                  "", 200,  -1,      1);
    h_vertex_rho                = fs->make<TH1F>("h_vertex_rho",                "", 200,   0,      2);
    h_vertex_phi                = fs->make<TH1F>("h_vertex_phi",                "", 200,  -3.15,   3.15);
    h_vertex_z                  = fs->make<TH1F>("h_vertex_z",                  "", 200, -20,     20);
    h_vertex_r                  = fs->make<TH1F>("h_vertex_r",                  "", 200,   0,      2);
  }
#endif
}

namespace {
  bool sort_by_dxyerr(const reco::TrackRef& a, const reco::TrackRef& b) {
    return a->dxyError() < b->dxyError();
  }

  bool sort_by_pt(const reco::TrackRef& a, const reco::TrackRef& b) {
    return a->pt() < b->pt();
  }
}

void MFVVertexRefitter::produce(edm::Event& event, const edm::EventSetup& setup) {
  if (verbose) {
    printf("------------------------------------------------------------------------\n");
    printf("MFVVertexRefitter::produce: run %u, lumi %u, event ", event.id().run(), event.luminosityBlock());
    std::cout << event.id().event() << "\n";
  }

#if 0
  edm::Handle<reco::BeamSpot> beamspot;
  event.getByToken(beamspot_token, beamspot);
  const double bs_x = beamspot->position().x();
  const double bs_y = beamspot->position().y();
  const double bs_z = beamspot->position().z();
#endif

  edm::ESHandle<TransientTrackBuilder> tt_builder;
  setup.get<TransientTrackRecord>().get("TransientTrackBuilder", tt_builder);

  edm::Handle<reco::VertexCollection> input_vertices;
  event.getByToken(vertex_token, input_vertices);

  int iiv = -1;
  for (const reco::Vertex& iv : *input_vertices) {
    if (++iiv >= max_n_input_vertices)
      break;

    std::unique_ptr<reco::VertexCollection> vertices(new reco::VertexCollection);

    std::vector<reco::TrackRef> input_tracks;
    for (auto tk = iv.tracks_begin(), tke = iv.tracks_end(); tk != tke; ++tk)
      input_tracks.push_back(tk->castTo<reco::TrackRef>());

    const size_t n_tracks = input_tracks.size();
    if (n_tracks_to_drop < n_tracks - 1) {
      if (sort_tracks_by == SortTracksByDxyErr)
        std::sort(input_tracks.begin(), input_tracks.end(), sort_by_dxyerr);
      else if (sort_tracks_by == SortTracksByPt)
        std::sort(input_tracks.begin(), input_tracks.end(), sort_by_pt);
      else
        throw cms::Exception("MFVVertexRefitter") << "sort_tracks_by " << sort_tracks_by << " not implemented";

      std::vector<int> drop(n_tracks, 0);
      for (size_t i = n_tracks - 1, ie = n_tracks - n_tracks_to_drop - 1; i > ie; --i)
        drop[i] = 1;

      do {
        std::vector<reco::TransientTrack> ttks;
        for (size_t i = 0; i < n_tracks; ++i)
          if (!drop[i])
            ttks.push_back(tt_builder->build(input_tracks[i]));

        vertices->push_back(reco::Vertex(TransientVertex(kv_reco->vertex(ttks))));
      }
      while (std::next_permutation(drop.begin(), drop.end()));
    }

    event.put(std::move(vertices), vertex_collection_name(iiv));
  }

#if 0
  if (histos || verbose) {
    for (size_t i = 0, ie = vertices->size(); i < ie; ++i) {
      const reco::Vertex& v = vertices->at(i);
      const int ntracks = v.nTracks();
      const double vchi2 = v.normalizedChi2();
      const double vndof = v.ndof();
      const double vx = v.position().x() - bs_x;
      const double vy = v.position().y() - bs_y;
      const double vz = v.position().z() - bs_z;
      const double rho = mag(vx, vy);
      const double phi = atan2(vy, vx);
      const double r = mag(vx, vy, vz);

      if (verbose)
        printf("no-share vertex #%3lu: ntracks: %i chi2/dof: %7.3f dof: %7.3f pos: <%7.3f, %7.3f, %7.3f>  rho: %7.3f  phi: %7.3f  r: %7.3f\n", i, ntracks, vchi2, vndof, vx, vy, vz, rho, phi, r);

      if (histos) {
        h_vertex_ntracks->Fill(ntracks);
        for (auto it = v.tracks_begin(), ite = v.tracks_end(); it != ite; ++it)
          h_vertex_track_weights->Fill(v.trackWeight(*it));
        h_vertex_chi2->Fill(vchi2);
        h_vertex_ndof->Fill(vndof);
        h_vertex_x->Fill(vx);
        h_vertex_y->Fill(vy);
        h_vertex_rho->Fill(rho);
        h_vertex_phi->Fill(phi);
        h_vertex_z->Fill(vz);
        h_vertex_r->Fill(r);
      }
    }
  }

  if (verbose)
    printf("n_vertices: %lu\n", vertices->size());
  if (histos)
    h_n_vertices->Fill(vertices->size());
#endif
}

DEFINE_FWK_MODULE(MFVVertexRefitter);
