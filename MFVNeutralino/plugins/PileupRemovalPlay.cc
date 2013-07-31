#include "TH2F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralino/interface/LightTrackMatch.h"

class PileupRemovalPlay : public edm::EDAnalyzer {
 public:
  explicit PileupRemovalPlay(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  typedef std::map<int, LightTrackMatch> LightTrackMatchMap;
  const edm::InputTag pucands_src;
  const edm::InputTag pv_src;
  const edm::InputTag ltmm_src;
};

PileupRemovalPlay::PileupRemovalPlay(const edm::ParameterSet& cfg)
  : pucands_src(cfg.getParameter<edm::InputTag>("pucands_src")),
    pv_src(cfg.getParameter<edm::InputTag>("pv_src")),
    ltmm_src(cfg.getParameter<edm::InputTag>("ltmm_src"))
{
  edm::Service<TFileService> fs;
}

void PileupRemovalPlay::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<reco::PFCandidateCollection> pucands;
  event.getByLabel(pucands_src, pucands);

  edm::Handle<reco::VertexCollection> pvs;
  event.getByLabel(pv_src, pvs);
  const reco::Vertex& the_pv = pvs->at(0);

  //const unsigned pv_ntracks = the_pv.nTracks();
  double pv_sumpt2 = 0;
  auto trkb = the_pv.tracks_begin();
  auto trke = the_pv.tracks_end();
  for (auto trki = trkb; trki != trke; ++trki) {
    if (the_pv.trackWeight(*trki) < 0.5)
      continue;
    double trkpt = (*trki)->pt();
    pv_sumpt2 += trkpt * trkpt;
  }

  edm::Handle<LightTrackMatchMap> ltmm;
  event.getByLabel(ltmm_src, ltmm);

  int num_null = 0;
  for (const reco::PFCandidate& pucand : *pucands) {
    reco::TrackRef tkref = pucand.trackRef();
    if (tkref.isNull()) {
      ++num_null;
      continue;
    }

    edm::Provenance prov = event.getProvenance(tkref.id());
    if (prov.moduleLabel() != "generalTracks") {
      continue;
    }

    LightTrackMatchMap::const_iterator it = ltmm->find(tkref.index());
    if (it == ltmm->end()) {
      continue;
    }

    const LightTrackMatch& ltm = it->second;
    printf("ltm found quality %f gen_ndx %i other %i lsp %i\n", ltm.quality, ltm.gen_ndx, ltm.other_matches, ltm.descent_1000021 || ltm.descent_1000022);
  }

  //  h_num_null->Fill(num_null);
}

DEFINE_FWK_MODULE(PileupRemovalPlay);
