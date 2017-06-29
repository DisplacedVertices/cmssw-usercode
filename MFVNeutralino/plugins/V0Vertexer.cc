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

  void do_hyps(const std::vector<reco::TrackRef>, std::unique_ptr<reco::VertexCollection>&);
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
}

bool MFVV0Vertexer::filter(edm::Event& event, const edm::EventSetup& setup) {
  std::unique_ptr<reco::VertexCollection> vertices(new reco::VertexCollection);

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
      do_hyps({tki, tkj}, vertices);
      for (size_t ktk = jtk+1; ktk < ntracks; ++ktk) {
        reco::TrackRef tkk(tracks, ktk);
        do_hyps({tki, tkj, tkk}, vertices);
      }
    }
  }

  const size_t nvertices = vertices->size();

  if (debug) {
    printf("got these vertices:\n");
    for (const auto &v : *vertices) {
      printf("chi2 %f pos %f %f %f ntracks %u hasRefitted? %i\ntracks:\n", v.normalizedChi2(), v.x(), v.y(), v.z(), v.nTracks(), v.hasRefittedTracks());
      for (auto it = v.tracks_begin(), ite = v.tracks_end(); it != ite; ++it) {
        const reco::Track& tk = **it;
        printf("  tk pt %f eta %f phi %f\n  ", tk.pt(), tk.eta(), tk.phi());
      }
    }
  }

  event.put(std::move(vertices));
  return !cut || nvertices;
}

void MFVV0Vertexer::do_hyps(const std::vector<reco::TrackRef> tracks, std::unique_ptr<reco::VertexCollection>& vertices) {
  const size_t ntracks = tracks.size();
  const int tracks_charge = std::accumulate(tracks.begin(), tracks.end(), 0, [](const int a, const reco::TrackRef& tk) { return a + tk->charge(); });

  if (debug) {
    printf("track set:\n");
    for (size_t i = 0; i < ntracks; ++i) {
      const reco::TrackRef& tk = tracks[i];
      printf("  %4u: %s <%10.4f %10.4f %10.4f>\n", tk.key(), tk->charge() > 0 ? "+" : "-", tk->pt(), tk->eta(), tk->phi());
    }
  }

  bool one_hyp_ok = false;
  for (const auto& hyp : mfv::V0_hypotheses) {
    if (debug) printf("hypothesis code %i = %s ndau %lu charge %i:\n", hyp.type, hyp.name, hyp.ndaughters(), hyp.charge());
    if (hyp.ndaughters() == ntracks && abs(hyp.charge()) == abs(tracks_charge)) {
      if (debug) printf("  matches #tracks %lu and charge %i\n", ntracks, tracks_charge);
      one_hyp_ok = true;
      break;
    }
  }

  if (one_hyp_ok) {
    std::vector<reco::TransientTrack> ttks(ntracks);
    for (size_t i = 0; i < ntracks; ++i)
      ttks[i] = tt_builder->build(tracks[i]);
    TransientVertex v = kv_reco->vertex(ttks);
    const bool valid = v.isValid();
    const bool keep = valid && v.normalisedChiSquared() < max_chi2ndf;
    if (debug) printf("vertex valid? %i chi2/ndf %f keep? %i\n", valid, (valid ? v.normalisedChiSquared() : -1), keep);
    if (keep)
      vertices->push_back(reco::Vertex(v));
  }
  else if (debug) printf("no hyps ok\n");
}

DEFINE_FWK_MODULE(MFVV0Vertexer);
