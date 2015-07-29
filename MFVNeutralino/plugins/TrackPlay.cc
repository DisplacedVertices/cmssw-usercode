#include "TH1F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/PairwiseHistos.h"

class MFVTrackPlay : public edm::EDAnalyzer {
 public:
  explicit MFVTrackPlay(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::InputTag track_src;
  const double dxy_cut;
  const int quality_cut;
  const edm::InputTag jet_src;
  const double jet_pt_cut;
  const double delta_r_jet_cut;
  const bool verbose;

  TH1F* h_ntracks;
  TH1F* h_algo;
  PairwiseHistos h_tracks;
};

MFVTrackPlay::MFVTrackPlay(const edm::ParameterSet& cfg)
  : track_src(cfg.getParameter<edm::InputTag>("track_src")),
    dxy_cut(cfg.getParameter<double>("dxy_cut")),
    quality_cut(reco::TrackBase::qualityByName(cfg.getParameter<std::string>("quality_cut"))),
    jet_src(cfg.getParameter<edm::InputTag>("jet_src")),
    jet_pt_cut(cfg.getParameter<double>("jet_pt_cut")),
    delta_r_jet_cut(cfg.getParameter<double>("delta_r_jet_cut")),
    verbose(cfg.getUntrackedParameter<bool>("verbose", false))
{
  edm::Service<TFileService> fs;

  h_ntracks = fs->make<TH1F>("h_ntracks", "", 2000, 0, 2000);

  h_algo = fs->make<TH1F>("h_algo", "", reco::TrackBase::algoSize, 0, reco::TrackBase::algoSize);
  for (int i = 0; i < reco::TrackBase::algoSize; ++i)
    h_algo->GetXaxis()->SetBinLabel(i+1, reco::TrackBase::algoName(reco::TrackBase::TrackAlgorithm(i)).c_str());

  PairwiseHistos::HistoDefs hs;
  hs.add("algo", "", reco::TrackBase::algoSize, 0, reco::TrackBase::algoSize);
  hs.add("tight", "", 2, 0, 2);
  hs.add("highpur", "", 2, 0, 2);
  hs.add("gooditer", "", 2, 0, 2);
  hs.add("q", "", 2, -2, 2);
  hs.add("pt", "", 100, 0, 500);
  hs.add("eta", "", 60, -3, 3);
  hs.add("phi", "", 63, -3.15, 3.15);
  hs.add("dxy", "", 100, -1, 1);
  hs.add("dz", "", 100, -25, 25);
  hs.add("fracsigpt", "", 100, 0, 3);
  hs.add("sigdxy", "", 100, 0, 2);
  hs.add("sigdz", "", 100, 0, 5);
  hs.add("nhits", "", 33, 0, 33);
  hs.add("npxhits", "", 9, 0, 9);
  hs.add("nsthits", "", 28, 0, 28);
  hs.add("npxlayers", "", 5, 0, 5);
  hs.add("nstlayers", "", 15, 0, 15);
  hs.add("nhitsmissinner", "", 15, 0, 15);
  hs.add("nhitsmissouter", "", 15, 0, 15);
  hs.add("min_dr_jet", "", 40, 0, delta_r_jet_cut);
  hs.add("min_dr_jet_pt", "", 100, 0, 500);
  h_tracks.Init("h", hs, true, true);
}

void MFVTrackPlay::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<reco::BeamSpot> beamspot;
  event.getByLabel("offlineBeamSpot", beamspot);

  edm::Handle<reco::TrackCollection> tracks;
  event.getByLabel(track_src, tracks);

  edm::Handle<pat::JetCollection> jets;
  event.getByLabel(jet_src, jets);

  int ntracks = 0;
  for (const reco::Track& track : *tracks) {
    double dxy = track.dxy(beamspot->position());

    if (fabs(dxy) < dxy_cut || (quality_cut != -1 && !track.quality(reco::TrackBase::TrackQuality(quality_cut))))
      continue;

    double min_dr_jet = 1e99;
    double min_dr_jet_pt = -1;
    for (const pat::Jet& jet : *jets) {
      if (jet.pt() > jet_pt_cut) {
        double dr = reco::deltaR(jet, track);
        if (dr < delta_r_jet_cut && dr < min_dr_jet) {
          min_dr_jet = dr;
          min_dr_jet_pt = jet.pt();
        }
      }
    }
    if (min_dr_jet > delta_r_jet_cut)
      continue;

    ++ntracks;

    h_algo->Fill(track.algo());

    const reco::HitPattern& hp = track.hitPattern();

    PairwiseHistos::ValueMap v = {
      {"algo",           track.algo()},
      {"tight",          track.quality(reco::TrackBase::qualityByName("tight"))},
      {"highpur",        track.quality(reco::TrackBase::qualityByName("highPurity"))},
      {"gooditer",       track.quality(reco::TrackBase::qualityByName("goodIterative"))},
      {"q",              track.charge()},
      {"pt",             track.pt()},
      {"eta",            track.eta()},
      {"phi",            track.phi()},
      {"dxy",            dxy},
      {"dz",             track.dz(beamspot->position())},
      {"fracsigpt",      track.ptError()/track.pt()},
      {"sigdxy",         track.dxyError()},
      {"sigdz",          track.dzError()},
      {"nhits",          hp.numberOfValidHits()},
      {"npxhits",        hp.numberOfValidPixelHits()},
      {"nsthits",        hp.numberOfValidStripHits()},
      {"npxlayers",      hp.pixelLayersWithMeasurement()},
      {"nstlayers",      hp.stripLayersWithMeasurement()},
      {"nhitsmissinner", hp.numberOfHits(reco::HitPattern::MISSING_INNER_HITS)},
      {"nhitsmissouter", hp.numberOfHits(reco::HitPattern::MISSING_OUTER_HITS)},
      {"min_dr_jet",     min_dr_jet},
      {"min_dr_jet_pt",  min_dr_jet_pt}
    };

    h_tracks.Fill(v);
  }

  h_ntracks->Fill(ntracks);
}

DEFINE_FWK_MODULE(MFVTrackPlay);
