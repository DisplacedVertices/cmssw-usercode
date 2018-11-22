#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"

class MFVUnpackedCandidateTracks : public edm::EDProducer {
public:
  explicit MFVUnpackedCandidateTracks(const edm::ParameterSet&);
  virtual void produce(edm::Event&, const edm::EventSetup&);
private:
  const edm::EDGetTokenT<pat::PackedCandidateCollection> packed_candidates_token;
  const bool debug;
};

MFVUnpackedCandidateTracks::MFVUnpackedCandidateTracks(const edm::ParameterSet& cfg)
  : packed_candidates_token(consumes<pat::PackedCandidateCollection>(cfg.getParameter<edm::InputTag>("packed_candidates_src"))),
    debug(cfg.getUntrackedParameter<bool>("debug", false))
{
  produces<reco::TrackCollection>();
  produces<std::vector<size_t>>(); // map back to which packed candidate
}

void MFVUnpackedCandidateTracks::produce(edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<pat::PackedCandidateCollection> packed_candidates;
  event.getByToken(packed_candidates_token, packed_candidates);

  std::unique_ptr<reco::TrackCollection> tracks(new reco::TrackCollection);
  std::unique_ptr<std::vector<size_t>> which(new std::vector<size_t>);

  int itk = 0;
  for (size_t i = 0, ie = packed_candidates->size(); i < ie; ++i) {
    const pat::PackedCandidate& cand = (*packed_candidates)[i];
    if (debug) std::cout << "cand #" << i << " id " << cand.pdgId() << " pt " << cand.pt() << " eta " << cand.eta() << " charge " << cand.charge() << " hasTrackDetails? " << cand.hasTrackDetails() << " ";
    if (cand.charge() && cand.hasTrackDetails()) {
      if (debug) std::cout << "-> track #" << itk << " pt " << cand.pseudoTrack().pt() << " eta " << cand.pseudoTrack().eta() << " min_r? " << cand.pseudoTrack().hitPattern().hasValidHitInPixelLayer(PixelSubdetector::PixelBarrel,1) << " npxlayers " << cand.pseudoTrack().hitPattern().pixelLayersWithMeasurement() << " nstlayers " << cand.pseudoTrack().hitPattern().stripLayersWithMeasurement() << " dxy " << cand.pseudoTrack().dxy() << " +- " << cand.pseudoTrack().dxyError();
      tracks->push_back(cand.pseudoTrack());
      which->push_back(i);
      ++itk;
    }
    if (debug) std::cout << "\n";
  }

  event.put(std::move(tracks));
  event.put(std::move(which));
}

DEFINE_FWK_MODULE(MFVUnpackedCandidateTracks);
