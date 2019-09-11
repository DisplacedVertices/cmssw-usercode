#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "JMTucker/MFVNeutralino/interface/Ntuple.h"
#include "JMTucker/MFVNeutralino/interface/NtupleFiller.h"

class MFVSplitPV : public edm::EDAnalyzer {
public:
  explicit MFVSplitPV(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override;

  mfv::SplitPVNtuple nt;
  jmt::TrackingAndJetsNtupleFiller nt_filler;

  std::unique_ptr<KalmanVertexFitter> kv_reco;
  const bool debug;
};

MFVSplitPV::MFVSplitPV(const edm::ParameterSet& cfg)
  : nt_filler(nt, cfg, NF_CC_TrackingAndJets_v,
              jmt::TrackingAndJetsNtupleFillerParams()
                .pvs_first_only(true)
                .fill_tracks(false)),
    kv_reco(new KalmanVertexFitter(cfg.getParameter<edm::ParameterSet>("kvr_params"), cfg.getParameter<edm::ParameterSet>("kvr_params").getParameter<bool>("doSmoothing"))),
    debug(cfg.getUntrackedParameter<bool>("debug", false))
{}

void MFVSplitPV::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  if (debug) printf("MFVSplitPV analyze (%u, %u, %llu)\n", event.id().run(), event.luminosityBlock(), event.id().event());

  nt_filler.fill(event);

  auto doit = [&](const std::vector<std::pair<reco::TransientTrack, unsigned>>& tps, unsigned which, unsigned ex=0) {
    TransientVertex tv;
    std::vector<reco::TransientTrack> ts(tps.size());
    for (size_t i = 0, ie = tps.size(); i < ie; ++i) ts[i] = tps[i].first;
    try { tv = kv_reco->vertex(ts); } catch (...) {}
    if (tv.isValid()) {
      reco::Vertex v(tv);
      nt.pvs().add(v.x(), v.y(), v.z(), v.chi2(), v.ndof(), v.nTracks(), 0,
                   v.covariance(0,0), v.covariance(0,1), v.covariance(0,2),
                   v.covariance(1,1), v.covariance(1,2),
                   v.covariance(2,2),
                   (ex << 16) | which);
    }
  };

  std::vector<std::pair<reco::TransientTrack,unsigned>> ttks, ttks_loose;

  edm::ESHandle<TransientTrackBuilder> tt_builder;
  setup.get<TransientTrackRecord>().get("TransientTrackBuilder", tt_builder);

  if (debug) printf("ipv %i, cands:", nt_filler.pvs_filler().ipv());

  for (const pat::PackedCandidate& c : nt_filler.pvs_filler().cands(event))
    if (c.charge() && c.hasTrackDetails()) {
      const int k = int(c.vertexRef().key());
      const int q = c.pvAssociationQuality();
      if (debug) printf(" %i-%i", k, q);
      if (k == nt_filler.pvs_filler().ipv()) {
        if (q == pat::PackedCandidate::UsedInFitLoose || q == pat::PackedCandidate::UsedInFitTight) {
          auto ttk = std::make_pair(tt_builder->build(c.pseudoTrack()), 0U);
          ttks_loose.push_back(ttk);
          if (q == pat::PackedCandidate::UsedInFitTight)
            ttks.push_back(ttk);
        }
      }
    }

  const size_t n = ttks.size();
  if (debug) printf("\nPV ndof %f ntracks %i n %lu\n", nt.pvs().ndof(0), nt.pvs().ntracks(0), n);

  if (n >= 2) {
    doit(ttks, 1, n);
    doit(ttks, 2, ttks_loose.size());

    if (n >= 4) {
      std::vector<std::pair<reco::TransientTrack, unsigned>> ttksa(n/2+n%2), ttksb(n/2);

      for (int k : {0,1}) {
        if (k == 0) std::sort(ttks.begin(), ttks.end(), [](auto a, auto b) { return a.first.track().pt() > b.first.track().pt(); });
        else        std::sort(ttks.begin(), ttks.end(), [](auto a, auto b) { return a.first.track().dxyError() < b.first.track().dxyError(); });

        for (size_t i = 0; i < n; ++i) {
          const int which = i % 2 == 0;
          ttks[i].second |= which << k;
          (which ? ttksa : ttksb)[i/2] = ttks[i];
        }

        doit(ttksa, 2*k+3);
        doit(ttksb, 2*k+4);
      }
    }
  
    for (auto tp : ttks)
      jmt::NtupleAdd(nt.tracks(), tp.first.track(), -1, tp.second);

    nt_filler.finalize();
  }
}

DEFINE_FWK_MODULE(MFVSplitPV);
