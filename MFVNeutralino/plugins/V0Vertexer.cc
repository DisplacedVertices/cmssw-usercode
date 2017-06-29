#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "JMTucker/MFVNeutralino/interface/V0Hypotheses.h"

class MFVV0Vertexer : public edm::EDFilter {
public:
  explicit MFVV0Vertexer(const edm::ParameterSet&);

private:
  virtual bool filter(edm::Event&, const edm::EventSetup&) override;

  std::auto_ptr<KalmanVertexFitter> kv_reco;
  const TransientTrackBuilder* tt_builder;
  const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
  const double max_chi2ndf;
  const bool cut;
  const bool debug;

  void do_hyps(const std::vector<reco::TrackRef>,
               std::unique_ptr<reco::VertexCollection>&, std::unique_ptr<mfv::V0VertexAuxCollection>&);
};

MFVV0Vertexer::MFVV0Vertexer(const edm::ParameterSet& cfg)
  : kv_reco(new KalmanVertexFitter(cfg.getParameter<edm::ParameterSet>("kvr_params"), cfg.getParameter<edm::ParameterSet>("kvr_params").getParameter<bool>("doSmoothing"))),
    tt_builder(nullptr),
    tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("tracks_src"))),
    max_chi2ndf(cfg.getParameter<double>("max_chi2ndf")),
    cut(cfg.getParameter<bool>("cut")),
    debug(cfg.getUntrackedParameter<bool>("debug", false))
{
  produces<reco::VertexCollection>();
  produces<mfv::V0VertexAuxCollection>(); 
}

bool MFVV0Vertexer::filter(edm::Event& event, const edm::EventSetup& setup) {
  std::unique_ptr<reco::VertexCollection> vertices(new reco::VertexCollection);
  std::unique_ptr<mfv::V0VertexAuxCollection> codes(new std::vector<int>);

  if (debug) printf("\nEVENT (%u, %u, %llu)\n", event.id().run(), event.luminosityBlock(), event.id().event());

  edm::Handle<reco::TrackCollection> tracks;
  event.getByToken(tracks_token, tracks);
  const size_t ntracks = tracks->size();

  edm::ESHandle<TransientTrackBuilder> tt_builder_;
  setup.get<TransientTrackRecord>().get("TransientTrackBuilder", tt_builder_);
  tt_builder = &*tt_builder_;

  if (debug) printf("# selected tracks: %lu\n", ntracks);

  for (size_t itk = 0; itk < ntracks; ++itk) {
    reco::TrackRef tki(tracks, itk);
    for (size_t jtk = itk+1; jtk < ntracks; ++jtk) {
      reco::TrackRef tkj(tracks, jtk);
      do_hyps({tki, tkj}, vertices, codes);
      for (size_t ktk = jtk+1; ktk < ntracks; ++ktk) {
        reco::TrackRef tkk(tracks, ktk);
        do_hyps({tki, tkj, tkk}, vertices, codes);
      }
    }
  }

  const size_t nvertices = vertices->size();
  event.put(std::move(vertices));
  event.put(std::move(codes));
  return !cut || nvertices;
}

void MFVV0Vertexer::do_hyps(const std::vector<reco::TrackRef> tracks,
                            std::unique_ptr<reco::VertexCollection>& vertices, std::unique_ptr<mfv::V0VertexAuxCollection>& codes) {

  const size_t ndaughters = tracks.size();
  std::vector<reco::TransientTrack> ttks(ndaughters);
  bool v_tried = false;
  TransientVertex v;
  const int daughters_charge = std::accumulate(tracks.begin(), tracks.end(), 0, [](const int a, const reco::TrackRef& tk) { return a + tk->charge(); });

  if (debug) {
    printf("track set:\n");
    for (size_t idau = 0; idau < ndaughters; ++idau) {
      const reco::TrackRef& tk = tracks[idau];
      printf("  %4u: %s <%10.4f %10.4f %10.4f>\n", tk.key(), tk->charge() > 0 ? "+" : "-", tk->pt(), tk->eta(), tk->phi());
    }
  }

  for (const auto& hyp : mfv::V0_hypotheses) {
    if (debug) printf("hypothesis #%i %s:\n", hyp.type, hyp.name);

    if (hyp.ndaughters() != ndaughters || hyp.charge() != daughters_charge) {
      if (debug) printf("failed # or total charge check\n");
      continue;
    }
            
    if (!v_tried) {
      for (size_t idau = 0; idau < ndaughters; ++idau)
        ttks[idau] = tt_builder->build(tracks[idau]);
      const std::vector<TransientVertex> vv(1, kv_reco->vertex(ttks));
      v = vv[0];
      v_tried = true;
    }

    const bool valid = v.isValid();
    if (debug) printf("vertex valid? %i chi2/ndf %f\n", valid, (valid ? v.normalisedChiSquared() : -1));
    if (valid && v.normalisedChiSquared() < max_chi2ndf) {
      vertices->push_back(reco::Vertex(v));
      codes->push_back(hyp.type);
    }
    else if (debug)
      printf("vertex is invalid!\n");
  }
}

DEFINE_FWK_MODULE(MFVV0Vertexer);
