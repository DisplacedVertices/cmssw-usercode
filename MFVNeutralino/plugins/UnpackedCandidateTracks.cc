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
};

MFVUnpackedCandidateTracks::MFVUnpackedCandidateTracks(const edm::ParameterSet& cfg)
  : packed_candidates_token(consumes<pat::PackedCandidateCollection>(cfg.getParameter<edm::InputTag>("packed_candidates_src")))
{
  produces<reco::TrackCollection>();
  produces<std::vector<size_t>>(); // map back to which packed candidate
}

void MFVUnpackedCandidateTracks::produce(edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<pat::PackedCandidateCollection> packed_candidates;
  event.getByToken(packed_candidates_token, packed_candidates);

  std::unique_ptr<reco::TrackCollection> tracks(new reco::TrackCollection);
  std::unique_ptr<std::vector<size_t>> which(new std::vector<size_t>);

  for (size_t i = 0, ie = packed_candidates->size(); i < ie; ++i) {
    const pat::PackedCandidate& cand = (*packed_candidates)[i];
    if (cand.charge()) {
      tracks->push_back(cand.pseudoTrack());
      which->push_back(i);
    }
  }

  event.put(std::move(tracks));
  event.put(std::move(which));
}

DEFINE_FWK_MODULE(MFVUnpackedCandidateTracks);
