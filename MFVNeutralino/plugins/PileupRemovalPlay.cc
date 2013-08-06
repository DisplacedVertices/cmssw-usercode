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
  const edm::InputTag nonpucands_src;
  const edm::InputTag pv_src;
  const edm::InputTag ltmm_src;

  TH1F* h_num;
  TH1F* h_num_null;
  TH1F* h_num_notGeneralTracks;
  TH1F* h_num_withoutLightTrackMatch;
  TH1F* h_num_withLightTrackMatch;
  TH1F* h_ltm_quality;
  TH1F* h_ltm_min_quality;
  TH1F* h_ltm_pt;
  TH1F* h_ltm_eta;
  TH1F* h_ltm_phi;
  TH1F* h_ltm_vx;
  TH1F* h_ltm_vy;
  TH1F* h_ltm_vz;
  TH1F* h_ltm_rho;
  TH1F* h_ltm_r;
  TH1F* h_ltm_gen_pt;
  TH1F* h_ltm_gen_eta;
  TH1F* h_ltm_gen_phi;
  TH1F* h_ltm_num_other_matches;
  TH1F* h_ltm_num_descent_1000021;
  TH1F* h_ltm_num_descent_1000022;
  TH1F* h_ltm_num_only_descent_1000021;
  TH1F* h_ltm_num_only_descent_1000022;
  TH1F* h_noltm_pt;
  TH1F* h_noltm_eta;
  TH1F* h_noltm_phi;
  TH1F* h_noltm_vx;
  TH1F* h_noltm_vy;
  TH1F* h_noltm_vz;
  TH1F* h_noltm_rho;
  TH1F* h_noltm_r;
  TH2F* h_noltm_rho_vz;
  TH2F* h_num_PVsumpt2;
  TH2F* h_num_withoutLightTrackMatch_PVsumpt2;
  TH2F* h_num_withLightTrackMatch_PVsumpt2;
  TH2F* h_num_PVntracks;
  TH2F* h_num_withoutLightTrackMatch_PVntracks;
  TH2F* h_num_withLightTrackMatch_PVntracks;
  TH2F* h_num_numPV;
  TH2F* h_num_withoutLightTrackMatch_numPV;
  TH2F* h_num_withLightTrackMatch_numPV;
  TH2F* h_num_num_withoutLightTrackMatch;
  TH2F* h_num_num_withLightTrackMatch;
  TH2F* h_ltm_num_descent_1000021_ltm_num_descent_1000022;
  TH2F* h_ltm_num_descent_1000021_num_withLightTrackMatch;
  TH1F* h_num_withLightTrackMatch_without_ltm_descent_1000021;
  TH2F* h_ltm_num_descent_1000021_num_nonpucands;
};

PileupRemovalPlay::PileupRemovalPlay(const edm::ParameterSet& cfg)
  : pucands_src(cfg.getParameter<edm::InputTag>("pucands_src")),
    nonpucands_src(cfg.getParameter<edm::InputTag>("nonpucands_src")),
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
  h_ltm_min_quality = fs->make<TH1F>("h_ltm_min_quality", ";min quality;events", 101, 0, 1.01);
  h_ltm_pt = fs->make<TH1F>("h_ltm_pt", ";pt for pucands with lighttrackmatch;number of pucands", 100, 0, 100);
  h_ltm_eta = fs->make<TH1F>("h_ltm_eta", ";eta for pucands with lighttrackmatch;number of pucands", 60, -3, 3);
  h_ltm_phi = fs->make<TH1F>("h_ltm_phi", ";phi for pucands with lighttrackmatch;number of pucands", 63, -3.15, 3.15);
  h_ltm_vx = fs->make<TH1F>("h_ltm_vx", ";vx for pucands with lighttrackmatch;number of pucands", 100, 0, 10);
  h_ltm_vy = fs->make<TH1F>("h_ltm_vy", ";vy for pucands with lighttrackmatch;number of pucands", 100, 0, 10);
  h_ltm_vz = fs->make<TH1F>("h_ltm_vz", ";vz for pucands with lighttrackmatch;number of pucands", 100, 0, 100);
  h_ltm_rho = fs->make<TH1F>("h_ltm_rho", ";rho for pucands with lighttrackmatch;number of pucands", 100, 0, 10);
  h_ltm_r = fs->make<TH1F>("h_ltm_r", ";r for pucands with lighttrackmatch;number of pucands", 100, 0, 100);
  h_ltm_gen_pt = fs->make<TH1F>("h_ltm_gen_pt", ";gen_pt;number of pucands", 100, 0, 100);
  h_ltm_gen_eta = fs->make<TH1F>("h_ltm_gen_eta", ";gen_eta;number of pucands", 60, -3, 3);
  h_ltm_gen_phi = fs->make<TH1F>("h_ltm_gen_phi", ";gen_phi;number of pucands", 63, -3.15, 3.15);
  h_ltm_num_other_matches = fs->make<TH1F>("h_ltm_num_other_matches", ";number of pucands where ltm.other_matches is true;events", 10, 0, 10);
  h_ltm_num_descent_1000021 = fs->make<TH1F>("h_ltm_num_descent_1000021", ";number of pucands where ltm.descent_1000021 is true;events", 100, 0, 200);
  h_ltm_num_descent_1000022 = fs->make<TH1F>("h_ltm_num_descent_1000022", ";number of pucands where ltm.descent_1000022 is true;events", 100, 0, 200);
  h_ltm_num_only_descent_1000021 = fs->make<TH1F>("h_ltm_num_only_descent_1000021", ";number of pucands where only ltm.descent_1000021 is true;events", 100, 0, 200);
  h_ltm_num_only_descent_1000022 = fs->make<TH1F>("h_ltm_num_only_descent_1000022", ";number of pucands where only ltm.descent_1000022 is true;events", 100, 0, 200);
  h_noltm_pt = fs->make<TH1F>("h_noltm_pt", ";pt for pucands without lighttrackmatch;number of pucands", 100, 0, 100);
  h_noltm_eta = fs->make<TH1F>("h_noltm_eta", ";eta for pucands without lighttrackmatch;number of pucands", 60, -3, 3);
  h_noltm_phi = fs->make<TH1F>("h_noltm_phi", ";phi for pucands without lighttrackmatch;number of pucands", 63, -3.15, 3.15);
  h_noltm_vx = fs->make<TH1F>("h_noltm_vx", ";vx for pucands without lighttrackmatch;number of pucands", 100, 0, 10);
  h_noltm_vy = fs->make<TH1F>("h_noltm_vy", ";vy for pucands without lighttrackmatch;number of pucands", 100, 0, 10);
  h_noltm_vz = fs->make<TH1F>("h_noltm_vz", ";vz for pucands without lighttrackmatch;number of pucands", 100, 0, 100);
  h_noltm_rho = fs->make<TH1F>("h_noltm_rho", ";rho for pucands without lighttrackmatch;number of pucands", 100, 0, 10);
  h_noltm_r = fs->make<TH1F>("h_noltm_r", ";r for pucands without lighttrackmatch;number of pucands", 100, 0, 100);
  h_noltm_rho_vz = fs->make<TH2F>("h_noltm_rho_vz", ";vz for pucands without lighttrackmatch;rho for pucands without lighttrackmatch", 100, 0, 100, 100, 0, 10);
  h_num_PVsumpt2 = fs->make<TH2F>("h_num_PVsumpt2", ";sumpt2 of the primary vertex;number of pucands", 100, 0, 2000, 100, 0, 2000);
  h_num_withoutLightTrackMatch_PVsumpt2 = fs->make<TH2F>("h_num_withoutLightTrackMatch_PVsumpt2", ";sumpt2 of the primary vertex;number of pucands without lighttrackmatch", 100, 0, 2000, 100, 0, 2000);
  h_num_withLightTrackMatch_PVsumpt2 = fs->make<TH2F>("h_num_withLightTrackMatch_PVsumpt2", ";sumpt2 of the primary vertex;number of pucands with lighttrackmatch", 100, 0, 2000, 100, 0, 2000);
  h_num_PVntracks = fs->make<TH2F>("h_num_PVntracks", ";number of tracks in the primary vertex;number of pucands", 100, 0, 100, 100, 0, 2000);
  h_num_withoutLightTrackMatch_PVntracks = fs->make<TH2F>("h_num_withoutLightTrackMatch_PVntracks", ";number of tracks in the primary vertex;number of pucands without lighttrackmatch", 100, 0, 100, 100, 0, 2000);
  h_num_withLightTrackMatch_PVntracks = fs->make<TH2F>("h_num_withLightTrackMatch_PVntracks", ";number of tracks in the primary vertex;number of pucands with lighttrackmatch", 100, 0, 100, 100, 0, 2000);
  h_num_numPV = fs->make<TH2F>("h_num_numPV", ";number of primary vertices;number of pucands", 10, 0, 50, 100, 0, 2000);
  h_num_withoutLightTrackMatch_numPV = fs->make<TH2F>("h_num_withoutLightTrackMatch_numPV", ";number of primary vertices;number of pucands without lighttrackmatch", 10, 0, 50, 100, 0, 2000);
  h_num_withLightTrackMatch_numPV = fs->make<TH2F>("h_num_withLightTrackMatch_numPV", ";number of primary vertices;number of pucands with lighttrackmatch", 10, 0, 50, 100, 0, 2000);
  h_num_num_withoutLightTrackMatch = fs->make<TH2F>("h_num_num_withoutLightTrackMatch", ";number of pucands without lighttrackmatch;number of pucands", 100, 0, 2000, 100, 0, 2000);
  h_num_num_withLightTrackMatch = fs->make<TH2F>("h_num_num_withLightTrackMatch", ";number of pucands with lighttrackmatch;number of pucands", 100, 0, 2000, 100, 0, 2000);
  h_ltm_num_descent_1000021_ltm_num_descent_1000022 = fs->make<TH2F>("h_ltm_num_descent_1000021_ltm_num_descent_1000022", ";number of pucands where ltm.descent_1000022 is true;number of pucands where ltm.descent_1000021 is true", 100, 0, 200, 100, 0, 200);
  h_ltm_num_descent_1000021_num_withLightTrackMatch = fs->make<TH2F>("h_ltm_num_descent_1000021_num_withLightTrackMatch", ";number of pucands with lighttrackmatch;number of pucands where ltm.descent_1000021 is true", 100, 0, 2000, 100, 0, 200);
  h_num_withLightTrackMatch_without_ltm_descent_1000021 = fs->make<TH1F>("h_num_withLightTrackMatch_without_ltm_descent_1000021", ";number of pucands with lighttrackmatch and not ltm.descent_1000021;events", 100, 0, 2000);
  h_ltm_num_descent_1000021_num_nonpucands = fs->make<TH2F>("h_ltm_num_descent_1000021_num_nonpucands", ";number of nonpucands;number of pucands where ltm.descent_1000021 is true", 100, 0, 2000, 100, 0, 200);
}

namespace {
  float mag(float x, float y) {
    return sqrt(x*x + y*y); 
  }
  float mag(float x, float y, float z) {
    return sqrt(x*x + y*y + z*z);
  }
} 

void PileupRemovalPlay::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<reco::PFCandidateCollection> pucands;
  event.getByLabel(pucands_src, pucands);

  edm::Handle<reco::PFCandidateCollection> nonpucands;
  event.getByLabel(nonpucands_src, nonpucands);
  const size_t num_nonpucands = nonpucands->size();

  edm::Handle<reco::VertexCollection> pvs;
  event.getByLabel(pv_src, pvs);
  const reco::Vertex& the_pv = pvs->at(0);

  const unsigned pv_ntracks = the_pv.nTracks();
  double pv_sumpt2 = 0;
  auto trkb = the_pv.tracks_begin();
  auto trke = the_pv.tracks_end();
  for (auto trki = trkb; trki != trke; ++trki) {
    if (the_pv.trackWeight(*trki) < 0.5)
      continue;
    double trkpt = (*trki)->pt();
    pv_sumpt2 += trkpt * trkpt;
  }
  const unsigned num_pv = pvs->size();

  edm::Handle<LightTrackMatchMap> ltmm;
  event.getByLabel(ltmm_src, ltmm);

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByLabel("offlineBeamSpot", beamspot);
  const float bsx = beamspot->x0();
  const float bsy = beamspot->y0();
  const float bsz = beamspot->z0();

  int num = 0;
  int num_null = 0;
  int num_notGeneralTracks = 0;
  int num_withoutLightTrackMatch = 0;
  int num_withLightTrackMatch = 0;
  double ltm_min_quality = 1.0;
  int ltm_num_other_matches = 0;
  int ltm_num_descent_1000021 = 0;
  int ltm_num_descent_1000022 = 0;
  int ltm_num_only_descent_1000021 = 0;
  int ltm_num_only_descent_1000022 = 0;
  int num_withLightTrackMatch_without_ltm_descent_1000021 = 0;
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
      h_noltm_pt->Fill(pucand.pt());
      h_noltm_eta->Fill(pucand.eta());
      h_noltm_phi->Fill(pucand.phi());
      h_noltm_vx->Fill(pucand.vx() - bsx);
      h_noltm_vy->Fill(pucand.vy() - bsy);
      h_noltm_vz->Fill(pucand.vz() - bsz);
      h_noltm_rho->Fill(mag(pucand.vx() - bsx, pucand.vy() - bsy));
      h_noltm_r->Fill(mag(pucand.vx() - bsx, pucand.vy() - bsy, pucand.vz() - bsz));
      h_noltm_rho_vz->Fill(pucand.vz() - bsz, mag(pucand.vx() - bsx, pucand.vy() - bsy));
      continue;
    }

    ++num_withLightTrackMatch;
    const LightTrackMatch& ltm = it->second;
    //printf("ltm found quality %f gen_ndx %i other %i lsp %i\n", ltm.quality, ltm.gen_ndx, ltm.other_matches, ltm.descent_1000021 || ltm.descent_1000022);
    h_ltm_quality->Fill(ltm.quality);
    if (ltm.quality < ltm_min_quality) {
      ltm_min_quality = ltm.quality;
    }
    if (ltm.other_matches) {
      ++ltm_num_other_matches;
    }
    if (ltm.descent_1000021) {
      ++ltm_num_descent_1000021;
      if (!ltm.descent_1000022) {
        ++ltm_num_only_descent_1000021;
      }
    } else {
      ++num_withLightTrackMatch_without_ltm_descent_1000021;
    }
    if (ltm.descent_1000022) {
      ++ltm_num_descent_1000022;
      if (!ltm.descent_1000021) {
        ++ltm_num_only_descent_1000022;
      }
    }

    h_ltm_pt->Fill(pucand.pt());
    h_ltm_eta->Fill(pucand.eta());
    h_ltm_phi->Fill(pucand.phi());
    h_ltm_vx->Fill(pucand.vx() - bsx);
    h_ltm_vy->Fill(pucand.vy() - bsy);
    h_ltm_vz->Fill(pucand.vz() - bsz);
    h_ltm_rho->Fill(mag(pucand.vx() - bsx, pucand.vy() - bsy));
    h_ltm_r->Fill(mag(pucand.vx() - bsx, pucand.vy() - bsy, pucand.vz() - bsz));
    h_ltm_gen_pt->Fill(ltm.gen_pt);
    h_ltm_gen_eta->Fill(ltm.gen_eta);
    h_ltm_gen_phi->Fill(ltm.gen_phi);

  }

  h_num->Fill(num);
  h_num_null->Fill(num_null);
  h_num_notGeneralTracks->Fill(num_notGeneralTracks);
  h_num_withoutLightTrackMatch->Fill(num_withoutLightTrackMatch);
  h_num_withLightTrackMatch->Fill(num_withLightTrackMatch);
  h_ltm_min_quality->Fill(ltm_min_quality);
  h_ltm_num_other_matches->Fill(ltm_num_other_matches);
  h_ltm_num_descent_1000021->Fill(ltm_num_descent_1000021);
  h_ltm_num_descent_1000022->Fill(ltm_num_descent_1000022);
  h_ltm_num_only_descent_1000021->Fill(ltm_num_only_descent_1000021);
  h_ltm_num_only_descent_1000022->Fill(ltm_num_only_descent_1000022);
  h_num_PVsumpt2->Fill(pv_sumpt2, num);
  h_num_withoutLightTrackMatch_PVsumpt2->Fill(pv_sumpt2, num_withoutLightTrackMatch);
  h_num_withLightTrackMatch_PVsumpt2->Fill(pv_sumpt2, num_withLightTrackMatch);
  h_num_PVntracks->Fill(pv_ntracks, num);
  h_num_withoutLightTrackMatch_PVntracks->Fill(pv_ntracks, num_withoutLightTrackMatch);
  h_num_withLightTrackMatch_PVntracks->Fill(pv_ntracks, num_withLightTrackMatch);
  h_num_numPV->Fill(num_pv, num);
  h_num_withoutLightTrackMatch_numPV->Fill(num_pv, num_withoutLightTrackMatch);
  h_num_withLightTrackMatch_numPV->Fill(num_pv, num_withLightTrackMatch);
  h_num_num_withoutLightTrackMatch->Fill(num_withoutLightTrackMatch, num);
  h_num_num_withLightTrackMatch->Fill(num_withLightTrackMatch, num);
  h_ltm_num_descent_1000021_ltm_num_descent_1000022->Fill(ltm_num_descent_1000022, ltm_num_descent_1000021);
  h_ltm_num_descent_1000021_num_withLightTrackMatch->Fill(num_withLightTrackMatch, ltm_num_descent_1000021);
  h_num_withLightTrackMatch_without_ltm_descent_1000021->Fill(num_withLightTrackMatch_without_ltm_descent_1000021);
  h_ltm_num_descent_1000021_num_nonpucands->Fill(num_nonpucands, ltm_num_descent_1000021);
}

DEFINE_FWK_MODULE(PileupRemovalPlay);
