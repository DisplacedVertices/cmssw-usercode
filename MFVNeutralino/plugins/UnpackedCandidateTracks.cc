#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "JMTucker/MFVNeutralinoFormats/interface/TracksMap.h"

class MFVUnpackedCandidateTracks : public edm::EDProducer {
public:
  explicit MFVUnpackedCandidateTracks(const edm::ParameterSet&);
  virtual void produce(edm::Event&, const edm::EventSetup&);
private:
  const edm::EDGetTokenT<pat::PackedCandidateCollection> packed_candidates_token;
  const bool add_lost_candidates;
  const edm::EDGetTokenT<pat::PackedCandidateCollection> lost_candidates_token;
  const bool debug;

  void debug_cand(const pat::PackedCandidate& cand, const char* tag, const size_t i) const {
    std::cout << tag << " cand #" << i << " id " << cand.pdgId() << " pt " << cand.pt() << " eta " << cand.eta() << " charge " << cand.charge() << " hasTrackDetails? " << cand.hasTrackDetails() << " ";
  }

  void debug_tk(const reco::Track& tk, const char* tag, const size_t i) const {
    std::cout << "-> " << tag << " track #" << i << " pt " << tk.pt() << " eta " << tk.eta() << " min_r? " << tk.hitPattern().hasValidHitInPixelLayer(PixelSubdetector::PixelBarrel,1)
              << " npxlayers " << tk.hitPattern().pixelLayersWithMeasurement() << " nstlayers " << tk.hitPattern().stripLayersWithMeasurement() << " dxy " << tk.dxy() << " +- " << tk.dxyError() << " pass? " << pass_tk(tk);
  };

  bool pass_cand(const pat::PackedCandidate& cand) const {
    return cand.charge() && cand.hasTrackDetails();
  }

  bool pass_tk(const reco::Track& tk) const {
    return
      tk.hitPattern().hasValidHitInPixelLayer(PixelSubdetector::PixelBarrel,1) &&
      tk.hitPattern().pixelLayersWithMeasurement() >= 2 &&
      tk.hitPattern().stripLayersWithMeasurement() >= 6 &&
      fabs(tk.dxy() / tk.dxyError()) > 4;
  }
};

MFVUnpackedCandidateTracks::MFVUnpackedCandidateTracks(const edm::ParameterSet& cfg)
  : packed_candidates_token(consumes<pat::PackedCandidateCollection>(cfg.getParameter<edm::InputTag>("packed_candidates_src"))),
    add_lost_candidates(cfg.getParameter<bool>("add_lost_candidates")),
    lost_candidates_token(consumes<pat::PackedCandidateCollection>(cfg.getParameter<edm::InputTag>("lost_candidates_src"))),
    debug(cfg.getUntrackedParameter<bool>("debug", false))
{
  produces<reco::TrackCollection>();
  produces<reco::TrackCollection>("lost");
  produces<mfv::UnpackedCandidateTracksMap>();
}

void MFVUnpackedCandidateTracks::produce(edm::Event& event, const edm::EventSetup& setup) {
  if (debug) std::cout << "MFVUnpackedCandidateTracks::produce: run " << event.id().run() << " lumi " << event.luminosityBlock() << " event " << event.id().event() << "\n";

  edm::Handle<pat::PackedCandidateCollection> packed_candidates;
  event.getByToken(packed_candidates_token, packed_candidates);

  std::unique_ptr<reco::TrackCollection> tracks(new reco::TrackCollection);
  std::unique_ptr<reco::TrackCollection> lost_tracks(new reco::TrackCollection);
  std::unique_ptr<mfv::UnpackedCandidateTracksMap> tracks_map(new mfv::UnpackedCandidateTracksMap);

  reco::TrackRefProd h_tracks = event.getRefBeforePut<reco::TrackCollection>();

  int ntkpass = 0, nlosttkpass = 0;

  for (size_t i = 0, ie = packed_candidates->size(); i < ie; ++i) {
    const pat::PackedCandidate& cand = (*packed_candidates)[i];
    if (debug) debug_cand(cand, "", i);

    if (pass_cand(cand)) {
      const reco::Track& tk = cand.pseudoTrack();

      if (debug) {
        debug_tk(tk, "", tracks->size());
        if (pass_tk(tk)) ++ntkpass;
      }

      tracks->push_back(tk);
      tracks_map->insert(reco::CandidatePtr(packed_candidates, i), reco::TrackRef(h_tracks, tracks->size() - 1));
    }

    if (debug) std::cout << "\n";
  }

  edm::Handle<pat::PackedCandidateCollection> lost_candidates;
  event.getByToken(lost_candidates_token, lost_candidates);

  for (size_t i = 0, ie = lost_candidates->size(); i < ie; ++i) {
    const pat::PackedCandidate& cand = (*lost_candidates)[i];
    if (debug) debug_cand(cand, "lost", i);

    if (pass_cand(cand)) {
      const reco::Track& tk = cand.pseudoTrack();

      if (debug) {
        debug_tk(tk, "lost", lost_tracks->size());
        if (pass_tk(tk)) ++nlosttkpass;
      }

      if (add_lost_candidates) {
        tracks->push_back(tk);
        tracks_map->insert(reco::CandidatePtr(lost_candidates, i), reco::TrackRef(h_tracks, tracks->size() - 1));
      }

      lost_tracks->push_back(tk);
    }

    if (debug) std::cout << "\n";
  }

  if (debug) std::cout << "MFVUnpackedCandidateTracks::produce: npass/ntk = " << ntkpass << " / " << tracks->size() << " npass/nlost = " << nlosttkpass << " / " << lost_tracks->size() << "\n";

  event.put(std::move(tracks));
  event.put(std::move(lost_tracks), "lost");
  event.put(std::move(tracks_map));
}

DEFINE_FWK_MODULE(MFVUnpackedCandidateTracks);
