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
  const bool skip_weirdos;
  const bool debug;

  void debug_cand(const pat::PackedCandidate& cand, const char* tag, const size_t i) const {
    std::cout << tag << " cand #" << i << " id " << cand.pdgId() << " pt " << cand.pt() << " eta " << cand.eta() << " charge " << cand.charge() << " hasTrackDetails? " << cand.hasTrackDetails() << " ";
  }

  void debug_tk(const reco::Track& tk, const char* tag, const size_t i) const {
    std::cout << "-> " << tag << " track #" << i << " pt " << tk.pt() << " eta " << tk.eta() << " min_r? " << tk.hitPattern().hasValidHitInPixelLayer(PixelSubdetector::PixelBarrel,1)
              << " npxlayers " << tk.hitPattern().pixelLayersWithMeasurement() << " nstlayers " << tk.hitPattern().stripLayersWithMeasurement() << " dxy " << tk.dxy() << " +- " << tk.dxyError() << " pass? " << pass_tk(tk);
  };

  bool pass_cand(const pat::PackedCandidate& cand) const {
    if (cand.charge() && cand.hasTrackDetails()) {
      if (skip_weirdos || debug) {
        const reco::Track& tk = cand.pseudoTrack();
        union U { float f; int i; } u;
        u.f = tk.dxyError();
        const bool weirdo =
          u.i == 0x3b8c70c2 ||  // 0.0042859027
          u.i == 0x3c060959 ||  // 0.0081809396
          u.i == 0x3cd24697 ||  // 0.0256684255
          u.i == 0x3dfc7c28 ||  // 0.1232836843
          u.i == 0x3e948f67;    // 0.2901565731
        if (debug && pass_tk(tk,false,false)) printf("(weirdo check %i %i %i 0x%08x %.10g) ", weirdo, pass_tk(tk,true,false), pass_tk(tk,true,true), u.i, u.f);
        if (skip_weirdos) return false;
      }
      return true;
    }
    return false;
  }

  bool pass_tk(const reco::Track& tk, bool req_min_r=true, bool req_nsigmadxy=true) const {
    return
      tk.pt() > 1 &&
      tk.hitPattern().pixelLayersWithMeasurement() >= 2 &&
      tk.hitPattern().stripLayersWithMeasurement() >= 6 &&
      (!req_min_r || tk.hitPattern().hasValidHitInPixelLayer(PixelSubdetector::PixelBarrel,1)) &&
      (!req_nsigmadxy || fabs(tk.dxy() / tk.dxyError()) > 4);
  }
};

MFVUnpackedCandidateTracks::MFVUnpackedCandidateTracks(const edm::ParameterSet& cfg)
  : packed_candidates_token(consumes<pat::PackedCandidateCollection>(cfg.getParameter<edm::InputTag>("packed_candidates_src"))),
    add_lost_candidates(cfg.getParameter<bool>("add_lost_candidates")),
    lost_candidates_token(consumes<pat::PackedCandidateCollection>(cfg.getParameter<edm::InputTag>("lost_candidates_src"))),
    skip_weirdos(cfg.getParameter<bool>("skip_weirdos")),
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

  reco::TrackRefProd h_output_tracks = event.getRefBeforePut<reco::TrackCollection>();

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
      tracks_map->insert(reco::CandidatePtr(packed_candidates, i), reco::TrackRef(h_output_tracks, tracks->size() - 1));
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
        tracks_map->insert(reco::CandidatePtr(lost_candidates, i), reco::TrackRef(h_output_tracks, tracks->size() - 1));
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
