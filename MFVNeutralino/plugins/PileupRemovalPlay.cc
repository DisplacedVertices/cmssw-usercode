#include "TH2F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
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
  const edm::InputTag ltmm_src;
};

PileupRemovalPlay::PileupRemovalPlay(const edm::ParameterSet& cfg)
  : pucands_src(cfg.getParameter<edm::InputTag>("pucands_src")),
    ltmm_src(cfg.getParameter<edm::InputTag>("ltmm_src"))
{
  edm::Service<TFileService> fs;
}

void PileupRemovalPlay::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<reco::PFCandidateCollection> pucands;
  event.getByLabel(pucands_src, pucands);

  edm::Handle<LightTrackMatchMap> ltmm;
  event.getByLabel(ltmm_src, ltmm);

  for (const reco::PFCandidate& pucand : *pucands) {
    reco::TrackRef tkref = pucand.trackRef();
    if (tkref.isNull()) {
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
}

DEFINE_FWK_MODULE(PileupRemovalPlay);
