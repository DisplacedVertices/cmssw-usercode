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

  TH1F* h_num;
  TH1F* h_num_null;
  TH1F* h_num_notGeneralTracks;
  TH1F* h_num_withoutLightTrackMatch;
  TH1F* h_num_withLightTrackMatch;
  TH1F* h_ltm_quality;
  TH1F* h_min_quality;
  TH1F* h_num_other_matches;
  TH1F* h_num_descent_1000021;
  TH1F* h_num_descent_1000022;
  TH1F* h_num_only_descent_1000021;
  TH1F* h_num_only_descent_1000022;
};

PileupRemovalPlay::PileupRemovalPlay(const edm::ParameterSet& cfg)
  : pucands_src(cfg.getParameter<edm::InputTag>("pucands_src")),
    pv_src(cfg.getParameter<edm::InputTag>("pv_src")),
    ltmm_src(cfg.getParameter<edm::InputTag>("ltmm_src"))
{
  edm::Service<TFileService> fs;
  h_num = fs->make<TH1F>("h_num", ";number of pucands;events", 100, 0, 2000);
  h_num_null = fs->make<TH1F>("h_num_null", ";number of pucands with null track ref;events", 10, 0, 10);
  h_num_notGeneralTracks = fs->make<TH1F>("h_num_notGeneralTracks", ";number of pucands with module not generalTracks;events", 10, 0, 10);
  h_num_withoutLightTrackMatch = fs->make<TH1F>("h_num_withoutLightTrackMatch", ";number of pucands without lighttrackmatch;events", 100, 0, 2000);
  h_num_withLightTrackMatch = fs->make<TH1F>("h_num_withLightTrackMatch", ";number of pucands with lighttrackmatch;events", 100, 0, 2000);
  h_ltm_quality = fs->make<TH1F>("h_ltm_quality", ";lighttrackmatch quality;number of pucands", 101, 0, 1.01);
  h_min_quality = fs->make<TH1F>("h_min_quality", ";min quality;events", 101, 0, 1.01);
  h_num_other_matches = fs->make<TH1F>("h_num_other_matches", ";number of pucands where ltm.other_matches is true;events", 10, 0, 10);
  h_num_descent_1000021 = fs->make<TH1F>("h_num_descent_1000021", ";number of pucands where ltm.descent_1000021 is true;events", 100, 0, 200);
  h_num_descent_1000022 = fs->make<TH1F>("h_num_descent_1000022", ";number of pucands where ltm.descent_1000022 is true;events", 100, 0, 200);
  h_num_only_descent_1000021 = fs->make<TH1F>("h_num_only_descent_1000021", ";number of pucands where only ltm.descent_1000021 is true;events", 100, 0, 200);
  h_num_only_descent_1000022 = fs->make<TH1F>("h_num_only_descent_1000022", ";number of pucands where only ltm.descent_1000022 is true;events", 100, 0, 200);
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

  int num = 0;
  int num_null = 0;
  int num_notGeneralTracks = 0;
  int num_withoutLightTrackMatch = 0;
  int num_withLightTrackMatch = 0;
  double min_quality = 1.0;
  int num_other_matches = 0;
  int num_descent_1000021 = 0;
  int num_descent_1000022 = 0;
  int num_only_descent_1000021 = 0;
  int num_only_descent_1000022 = 0;
  for (const reco::PFCandidate& pucand : *pucands) {
    ++num;

    reco::TrackRef tkref = pucand.trackRef();
    if (tkref.isNull()) {
      ++num_null;
      continue;
    }

    edm::Provenance prov = event.getProvenance(tkref.id());
    if (prov.moduleLabel() != "generalTracks") {
      ++num_notGeneralTracks;
      continue;
    }

    LightTrackMatchMap::const_iterator it = ltmm->find(tkref.index());
    if (it == ltmm->end()) {
      ++num_withoutLightTrackMatch;
      continue;
    }

    ++num_withLightTrackMatch;
    const LightTrackMatch& ltm = it->second;
    //printf("ltm found quality %f gen_ndx %i other %i lsp %i\n", ltm.quality, ltm.gen_ndx, ltm.other_matches, ltm.descent_1000021 || ltm.descent_1000022);
    h_ltm_quality->Fill(ltm.quality);
    if (ltm.quality < min_quality) {
      min_quality = ltm.quality;
    }
    if (ltm.other_matches) {
      ++num_other_matches;
    }
    if (ltm.descent_1000021) {
      ++num_descent_1000021;
      if (!ltm.descent_1000022) {
        ++num_only_descent_1000021;
      }
    }
    if (ltm.descent_1000022) {
      ++num_descent_1000022;
      if (!ltm.descent_1000021) {
        ++num_only_descent_1000022;
      }
    }
  }

  h_num->Fill(num);
  h_num_null->Fill(num_null);
  h_num_notGeneralTracks->Fill(num_notGeneralTracks);
  h_num_withoutLightTrackMatch->Fill(num_withoutLightTrackMatch);
  h_num_withLightTrackMatch->Fill(num_withLightTrackMatch);
  h_min_quality->Fill(min_quality);
  h_num_other_matches->Fill(num_other_matches);
  h_num_descent_1000021->Fill(num_descent_1000021);
  h_num_descent_1000022->Fill(num_descent_1000022);
  h_num_only_descent_1000021->Fill(num_only_descent_1000021);
  h_num_only_descent_1000022->Fill(num_only_descent_1000022);
}

DEFINE_FWK_MODULE(PileupRemovalPlay);
