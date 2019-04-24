#include "CommonTools/UtilAlgos/interface/TFileService.h"
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

class MFVK0Treer : public edm::EDAnalyzer {
public:
  explicit MFVK0Treer(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override;

  std::unique_ptr<KalmanVertexFitter> kv_reco;
  const TransientTrackBuilder* tt_builder;
  const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
  jmt::BaseSubNtupleFiller base_filler;
  jmt::BeamspotSubNtupleFiller bs_filler;
  jmt::PrimaryVerticesSubNtupleFiller pvs_filler;
  jmt::JetsSubNtupleFiller jets_filler;
  const bool debug;

  mfv::K0Ntuple nt;
  TTree* tree;

  bool pass(const reco::Track& tk) const { return tk.pt() >= 1 && tk.hitPattern().pixelLayersWithMeasurement() >= 2 && tk.hitPattern().stripLayersWithMeasurement() >= 6 && tk.hitPattern().hasValidHitInPixelLayer(PixelSubdetector::PixelBarrel,1); }
  TLorentzVector p4(const reco::Track& tk) const { TLorentzVector v; v.SetPtEtaPhiM(tk.pt(), tk.eta(), tk.phi(), 0.13957); return v; }
};

MFVK0Treer::MFVK0Treer(const edm::ParameterSet& cfg)
  : kv_reco(new KalmanVertexFitter(cfg.getParameter<edm::ParameterSet>("kvr_params"), cfg.getParameter<edm::ParameterSet>("kvr_params").getParameter<bool>("doSmoothing"))),
    tt_builder(nullptr),
    tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("tracks_src"))),
    base_filler(nt.base(), cfg, consumesCollector()),
    bs_filler(nt.bs(), cfg, consumesCollector()),
    pvs_filler(nt.pvs(), cfg, consumesCollector(), true, true),
    jets_filler(nt.jets(), cfg, consumesCollector()),
    debug(cfg.getUntrackedParameter<bool>("debug", false))
{
  edm::Service<TFileService> fs;
  tree = fs->make<TTree>("t", "");
  nt.write_to_tree(tree);
}

void MFVK0Treer::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  if (debug) printf("\nMFVK0Treer analyze (%u, %u, %llu)\n", event.id().run(), event.luminosityBlock(), event.id().event());

  nt.clear();

  base_filler(event);
  bs_filler(event);
  pvs_filler(event);
  jets_filler(event);

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

  const reco::Vertex& pv = *pvs_filler.pv();

  for (size_t itk = 0; itk < ntracks; ++itk) {
    reco::TrackRef tki(tracks, itk);
    if (!pass(*tki))
      continue;

    for (size_t jtk = itk+1; jtk < ntracks; ++jtk) {
      reco::TrackRef tkj(tracks, jtk);
      if (!pass(*tkj))
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

      TLorentzVector vp4 = p4(tkrefi) + p4(tkrefj);
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

  if (ok)
    tree->Fill();
}

DEFINE_FWK_MODULE(MFVK0Treer);
