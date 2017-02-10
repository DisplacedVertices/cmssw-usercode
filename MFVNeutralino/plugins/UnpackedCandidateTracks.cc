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
  : packed_candidates_token(consumes<pat::PackedCandidateCollection>(edm::InputTag("packedPFCandidates")))
{
  produces<reco::TrackCollection>();
}

void MFVUnpackedCandidateTracks::produce(edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<pat::PackedCandidateCollection> packed_candidates;
  event.getByToken(packed_candidates_token, packed_candidates);

  std::auto_ptr<reco::TrackCollection> output_tracks(new reco::TrackCollection);

  for (const pat::PackedCandidate& cand : *packed_candidates)
    if (cand.charge())
      output_tracks->push_back(cand.pseudoTrack());

  event.put(output_tracks);
}

DEFINE_FWK_MODULE(MFVUnpackedCandidateTracks);
