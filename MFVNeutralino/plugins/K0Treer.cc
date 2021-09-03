#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "DVCode/Tools/interface/TrackTools.h"
#include "DVCode/MFVNeutralino/interface/NtupleFiller.h"

class MFVK0Treer : public edm::EDAnalyzer {
public:
  explicit MFVK0Treer(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override;

  mfv::K0Ntuple nt;
  jmt::TrackingAndJetsNtupleFiller nt_filler;

  std::unique_ptr<KalmanVertexFitter> kv_reco;
  const TransientTrackBuilder* tt_builder;
  const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
  const bool debug;
};

MFVK0Treer::MFVK0Treer(const edm::ParameterSet& cfg)
  : nt_filler(nt, cfg, NF_CC_TrackingAndJets_v,
              jmt::TrackingAndJetsNtupleFillerParams()
                .pvs_first_only(true)
                .fill_tracks(false)),
    kv_reco(new KalmanVertexFitter(cfg.getParameter<edm::ParameterSet>("kvr_params"), cfg.getParameter<edm::ParameterSet>("kvr_params").getParameter<bool>("doSmoothing"))),
    tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("tracks_src"))),
    debug(cfg.getUntrackedParameter<bool>("debug", false))
{}

void MFVK0Treer::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  if (debug) printf("\nMFVK0Treer analyze (%u, %u, %llu)\n", event.id().run(), event.luminosityBlock(), event.id().event());

  nt_filler.fill(event);

  edm::Handle<reco::TrackCollection> tracks;
  event.getByToken(tracks_token, tracks);
  const size_t ntracks = tracks->size();

  edm::ESHandle<TransientTrackBuilder> tt_builder_;
  setup.get<TransientTrackRecord>().get("TransientTrackBuilder", tt_builder_);
  tt_builder = &*tt_builder_;

  if (debug) printf("# selected tracks: %lu\n", ntracks);

  std::map<size_t, size_t> tkind;
  auto nt_add_tk = [&](const reco::TrackRef& tk) {
    auto it = tkind.find(tk.key());
    if (it != tkind.end())
      return it->second;
    jmt::NtupleAdd(nt.tracks(), *tk);
    size_t r = nt.tracks().n() - 1;
    tkind[tk.key()] = r;
    assert(r < (1<<16));
    return r;
  };

  bool ok = false;

  const reco::Vertex& pv = *nt_filler.pv();

  for (size_t itk = 0; itk < ntracks; ++itk) {
    reco::TrackRef tki(tracks, itk);
    if (!jmt::pass_track(*tki, 1))
      continue;

    for (size_t jtk = itk+1; jtk < ntracks; ++jtk) {
      reco::TrackRef tkj(tracks, jtk);
      if (!jmt::pass_track(*tkj, 1))
        continue;

      if (tki->charge() + tkj->charge() != 0)
        continue;
        
      if (debug) {
        printf("track set:\n");
        for (auto tk : {tki,tkj})
          printf("  %4u: %s <%12.6f %12.6f %12.6f %12.6f %12.6f>\n", tk.key(), tk->charge() > 0 ? "+" : "-", tk->pt(), tk->eta(), tk->phi(), tk->dxy(), tk->dz());
      }

      TransientVertex tv;
      try { tv = kv_reco->vertex({tt_builder->build(tki), tt_builder->build(tkj)}); } catch (...) {}
      const bool vok = tv.isValid() && tv.normalisedChiSquared() < 7;
      if (debug) printf("vertex valid? %i chi2/ndf %f ok? %i\n", tv.isValid(), (tv.isValid() ? tv.normalisedChiSquared() : -1), vok);
      if (!vok)
        continue;

      reco::Vertex v(tv);
      const reco::Track& tkrefi = v.refittedTrack(tki);
      const reco::Track& tkrefj = v.refittedTrack(tkj);

      if (debug) {
        printf("  pos %f %f %f ntracks %u hasRefitted? %i refit tracks:\n", v.x(), v.y(), v.z(), v.nTracks(), v.hasRefittedTracks());
        for (const reco::Track& tk : {tkrefi, tkrefj})
          printf("        %s <%12.6f %12.6f %12.6f %12.6f %12.6f>\n", tk.charge() > 0 ? "+" : "-", tk.pt(), tk.eta(), tk.phi(), tk.dxy(), tk.dz());
      }

      TLorentzVector vp4 = jmt::track_p4(tkrefi) + jmt::track_p4(tkrefj);
      const double mass = vp4.M();
      if (debug) printf("  p: %f m: %f\n", vp4.P(), mass);
      if (mass < 0.42 || mass > 0.58)
        continue;

      const TVector3 vp42(vp4.X(), vp4.Y(), 0);
      const TVector3 flight2(v.x() - pv.x(), v.y() - pv.y(), 0);
      const double costh2 = vp42.Unit().Dot(flight2.Unit());
      if (costh2 < 0.95)
        continue;

      const size_t itk_nt = nt_add_tk(tki);
      const size_t jtk_nt = nt_add_tk(tkj);
      
      nt.svs().add(v.x(), v.y(), v.z(), v.chi2(), v.ndof(), 2, mass,
                   v.covariance(0,0), v.covariance(0,1), v.covariance(0,2),
                                      v.covariance(1,1), v.covariance(1,2),
                                                         v.covariance(2,2),
                   (jtk_nt << 16) | itk_nt);

      for (const reco::Track& tk : {tkrefi, tkrefj})
        jmt::NtupleAdd(nt.refit_tks(), tk);

      ok = true;
    }
  }

  if (ok) nt_filler.finalize();
}

DEFINE_FWK_MODULE(MFVK0Treer);
