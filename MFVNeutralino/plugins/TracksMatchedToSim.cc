#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"
#include "MagneticField/Engine/interface/MagneticField.h"
#include "SimDataFormats/TrackingAnalysis/interface/TrackingParticle.h"
#include "SimTracker/Records/interface/TrackAssociatorRecord.h"
#include "SimTracker/TrackAssociation/interface/TrackAssociatorBase.h"
#include "JMTucker/Tools/interface/GenUtilities.h"

class MFVTracksMatchedToSim : public edm::EDProducer {
public:
  explicit MFVTracksMatchedToSim(const edm::ParameterSet&);

private:
  virtual void produce(edm::Event&, const edm::EventSetup&);

  const edm::InputTag gen_particles_src;
  const edm::InputTag tracking_particles_src;
  const edm::InputTag tracks_src;
  const bool produce_nonmatched;
  const double min_match_quality;
  const double min_track_pt;
};

MFVTracksMatchedToSim::MFVTracksMatchedToSim(const edm::ParameterSet& cfg) 
  : gen_particles_src(cfg.getParameter<edm::InputTag>("gen_particles_src")),
    tracking_particles_src(cfg.getParameter<edm::InputTag>("tracking_particles_src")),
    tracks_src(cfg.getParameter<edm::InputTag>("tracks_src")),
    produce_nonmatched(cfg.getParameter<bool>("produce_nonmatched")),
    min_match_quality(cfg.getParameter<double>("min_match_quality")),
    min_track_pt(cfg.getParameter<double>("min_track_pt"))
{
  produces<reco::TrackCollection>();
  if (produce_nonmatched)
    produces<reco::TrackCollection>("nonmatched");
}

void MFVTracksMatchedToSim::produce(edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<reco::GenParticleCollection> gen_particles;
  event.getByLabel(gen_particles_src, gen_particles);

  edm::Handle<TrackingParticleCollection> tracking_particles;
  event.getByLabel(tracking_particles_src, tracking_particles);

  // magnetic_field is not used below, but if you don't have the
  // record defined in the cfg then the TrackAssociatorByHits
  // record-getting will fail without telling you that it's missing
  // the magnetic field record.
  edm::ESHandle<MagneticField> magnetic_field; 
  setup.get<IdealMagneticFieldRecord>().get(magnetic_field);

  edm::Handle<edm::View<reco::Track> > tracks;
  event.getByLabel(tracks_src, tracks);

  edm::ESHandle<TrackAssociatorBase> associator_handle;
  setup.get<TrackAssociatorRecord>().get("TrackAssociatorByHits", associator_handle);
  TrackAssociatorBase* associator = (TrackAssociatorBase*) associator_handle.product();
  reco::RecoToSimCollection reco_to_sim = associator->associateRecoToSim(tracks, tracking_particles, &event);

  std::auto_ptr<reco::TrackCollection> output(new reco::TrackCollection);
  std::auto_ptr<reco::TrackCollection> output_nonmatched(new reco::TrackCollection);
    
  for (size_t i = 0, ie = tracks->size(); i < ie; ++i) {
    bool put = false;
    edm::RefToBase<reco::Track> track_ref(tracks, i);
    std::vector<std::pair<TrackingParticleRef, double> > matches;
    try {
      matches = reco_to_sim[track_ref];
    }
    catch (const edm::Exception& e) {
    }
    const size_t nmatch = matches.size();
    if (nmatch > 1)
      throw cms::Exception("MFVTracksMatchedToSim") << "more than one tracking particle match for track #" << i;
    else if (nmatch == 1) {
      const auto& match = matches[0];
      const TrackingParticleRef tp = match.first;
      const double quality = match.second;
      if (quality >= min_match_quality) {
	const size_t ngen = tp->genParticle().size();
	if (ngen > 1)
	  throw cms::Exception("MFVTracksMatchedToSim") << "more than one gen particle match for track #" << i;
	else if (ngen == 1) {
	  const auto& hepmc = tp->genParticle()[0];
	  if (hepmc->barcode() <= 0)
	    throw cms::Exception("MFVTracksMatchedToSim") << "hepmc barcode <= 0 (=" << hepmc->barcode() << ") for track #" << i;
	  const reco::GenParticle& gen = gen_particles->at(hepmc->barcode()-1);
	  if (has_any_ancestor_with_id(&gen, 1000021) && track_ref->pt() > min_track_pt) {
	    put = true;
	    output->push_back(*track_ref);
	  }
	}
      }
    }
    
    if (!put && produce_nonmatched)
      output_nonmatched->push_back(*track_ref);
  }

  event.put(output);
  event.put(output_nonmatched, "nonmatched");
}

DEFINE_FWK_MODULE(MFVTracksMatchedToSim);
