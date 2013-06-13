#include "TH1F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
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
  const edm::InputTag tracks_src;
  const double dxy_cut;
  const int quality_cut;
  const bool verbose;

  TH1F* h_ntracks;
  TH1F* h_algo;
  PairwiseHistos h_tracks;
};

MFVTrackPlay::MFVTrackPlay(const edm::ParameterSet& cfg)
  : tracks_src(cfg.getParameter<edm::InputTag>("tracks_src")),
    dxy_cut(cfg.getParameter<double>("dxy_cut")),
    quality_cut(reco::TrackBase::qualityByName(cfg.getParameter<std::string>("quality_cut"))),
    verbose(cfg.getUntrackedParameter<bool>("verbose", false))
{
  edm::Service<TFileService> fs;

  h_ntracks = fs->make<TH1F>("h_ntracks", "", 2000, 0, 2000);

  h_algo = fs->make<TH1F>("h_algo", "", reco::TrackBase::algoSize, 0, reco::TrackBase::algoSize);
  for (int i = 0; i < reco::TrackBase::algoSize; ++i)
    h_algo->GetXaxis()->SetBinLabel(i+1, reco::TrackBase::algoName(reco::TrackBase::TrackAlgorithm(i)).c_str());

  PairwiseHistos::HistoDefs hs;
  hs.add("algo", "", reco::TrackBase::algoSize, 0, reco::TrackBase::algoSize);
  hs.add("q", "", 2, -2, 2);
  hs.add("pt", "", 100, 0, 500);
  hs.add("eta", "", 60, -3, 3);
  hs.add("phi", "", 63, -3.15, 3.15);
  hs.add("dxy", "", 100, -1, 1);
  hs.add("dz", "", 100, -25, 25);
  hs.add("nhits", "", 33, 0, 33);
  hs.add("npxhits", "", 9, 0, 9);
  hs.add("nsthits", "", 28, 0, 28);
  hs.add("npxlayers", "", 5, 0, 5);
  hs.add("nstlayers", "", 15, 0, 15);
  hs.add("nhitsmissinner", "", 15, 0, 15);
  hs.add("nhitsmissouter", "", 15, 0, 15);
  h_tracks.Init("h_tracks", hs, true, true);
}

void MFVTrackPlay::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<reco::BeamSpot> beamspot;
  event.getByLabel("offlineBeamSpot", beamspot);

  edm::Handle<reco::TrackCollection> tracks;
  event.getByLabel(tracks_src, tracks);

  int ntracks = 0;
  for (const reco::Track& t : *tracks) {
    double dxy = t.dxy(beamspot->position());

    if (fabs(dxy) < dxy_cut || (quality_cut != -1 && !t.quality(reco::TrackBase::TrackQuality(quality_cut))))
      continue;

    ++ntracks;

    h_algo->Fill(t.algo());

    const reco::HitPattern& hp = t.hitPattern();

    PairwiseHistos::ValueMap v = {
      {"algo",           t.algo()},
      {"q",              t.charge()},
      {"pt",             t.pt()},
      {"eta",            t.eta()},
      {"phi",            t.phi()},
      {"dxy",            dxy},
      {"dz",             t.dz(beamspot->position())},
      {"nhits",          hp.numberOfValidHits()},
      {"npxhits",        hp.numberOfValidPixelHits()},
      {"nsthits",        hp.numberOfValidStripHits()},
      {"npxlayers",      hp.pixelLayersWithMeasurement()},
      {"nstlayers",      hp.stripLayersWithMeasurement()},
      {"nhitsmissinner", t.trackerExpectedHitsInner().numberOfHits()},
      {"nhitsmissouter", t.trackerExpectedHitsOuter().numberOfHits()},
    };

    h_tracks.Fill(v);
  }

  h_ntracks->Fill(ntracks);
}

DEFINE_FWK_MODULE(MFVTrackPlay);
