#include "TTree.h"
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

  std::unique_ptr<KalmanVertexFitter> kv_reco;
  jmt::BaseSubNtupleFiller base_filler;
  jmt::BeamspotSubNtupleFiller bs_filler;
  jmt::PrimaryVerticesSubNtupleFiller pvs_filler;
  jmt::JetsSubNtupleFiller jets_filler;
  const bool debug;

  mfv::SplitPVNtuple nt;
  TTree* tree;
};

MFVSplitPV::MFVSplitPV(const edm::ParameterSet& cfg)
  : kv_reco(new KalmanVertexFitter(cfg.getParameter<edm::ParameterSet>("kvr_params"), cfg.getParameter<edm::ParameterSet>("kvr_params").getParameter<bool>("doSmoothing"))),
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

void MFVSplitPV::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  if (debug) printf("MFVSplitPV analyze (%u, %u, %llu)\n", event.id().run(), event.luminosityBlock(), event.id().event());

  nt.clear();

  base_filler(event);
  bs_filler(event);
  pvs_filler(event);
  jets_filler(event);

  auto doit = [&](const std::vector<reco::TransientTrack>& ts, unsigned which, unsigned ex=0) {
    TransientVertex tv;
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

  std::vector<reco::TransientTrack> ttks;

  edm::ESHandle<TransientTrackBuilder> tt_builder;
  setup.get<TransientTrackRecord>().get("TransientTrackBuilder", tt_builder);

  if (debug) printf("ipv %i, cands:", pvs_filler.ipv());

  for (const pat::PackedCandidate& c : pvs_filler.cands(event))
    if (c.charge() && c.hasTrackDetails()) {
      int k = int(c.vertexRef().key());
      if (debug) printf(" %i", k);
      if (k == pvs_filler.ipv())
        ttks.push_back(tt_builder->build(c.pseudoTrack()));
    }

  const size_t n = ttks.size();
  if (debug) printf("\nPV ndof %f ntracks %i n %lu\n", nt.pvs().ndof(0), nt.pvs().ntracks(0), n);

  if (n < 2)
    return;

  doit(ttks, 1, n);

  if (n < 4)
    return;

  std::vector<reco::TransientTrack> ttksa(n/2+n%2), ttksb(n/2);

  for (int k : {0,1}) {
    if (k == 0) std::sort(ttks.begin(), ttks.end(), [](auto a, auto b) { return a.track().pt() > b.track().pt(); });
    else        std::sort(ttks.begin(), ttks.end(), [](auto a, auto b) { return a.track().dxyError() < b.track().dxyError(); });
  
    for (size_t i = 0; i < n; ++i)
      (i % 2 == 0 ? ttksa : ttksb)[i/2] = ttks[i];

    doit(ttksa, 2*k+2);
    doit(ttksb, 2*k+3);
  }

  tree->Fill();
}

DEFINE_FWK_MODULE(MFVSplitPV);
