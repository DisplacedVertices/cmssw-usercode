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
#include "JMTucker/MFVNeutralino/interface/LightTrackMatch.h"
#include "JMTucker/Tools/interface/GenUtilities.h"

class MFVTrackMatcherLight : public edm::EDProducer {
public:
  explicit MFVTrackMatcherLight(const edm::ParameterSet&);

private:
  virtual void produce(edm::Event&, const edm::EventSetup&);

  const edm::InputTag gen_particles_src;
  const edm::InputTag tracking_particles_src;
  const edm::InputTag tracks_src;

  typedef std::map<int, LightTrackMatch> OutputType;
};

MFVTrackMatcherLight::MFVTrackMatcherLight(const edm::ParameterSet& cfg) 
  : gen_particles_src(cfg.getParameter<edm::InputTag>("gen_particles_src")),
    tracking_particles_src(cfg.getParameter<edm::InputTag>("tracking_particles_src")),
    tracks_src(cfg.getParameter<edm::InputTag>("tracks_src"))
{
  produces<OutputType>();
}

void MFVTrackMatcherLight::produce(edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<reco::GenParticleCollection> gen_particles;
  edm::Handle<std::vector<int> > gen_particles_barcodes;
  event.getByLabel(gen_particles_src, gen_particles);
  event.getByLabel(gen_particles_src, gen_particles_barcodes);

  // JMTBAD instead of checking this, just use the barcodes
  int ibc = 0;
  for (const auto& bc : *gen_particles_barcodes) {
    assert(bc - ibc == 1);
    ++ibc;
  }

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

  std::auto_ptr<OutputType> output(new OutputType);
    
  for (size_t i = 0, ie = tracks->size(); i < ie; ++i) {
    edm::RefToBase<reco::Track> track_ref(tracks, i);
    std::vector<std::pair<TrackingParticleRef, double> > matches;
    try {
      matches = reco_to_sim[track_ref];
    }
    catch (const edm::Exception& e) {
    }
    const size_t nmatch = matches.size();
#if 0
    if (nmatch > 1) {
      std::ostringstream out;
      for (const auto& match : matches)
	out << "match with quality " << match.second << ": id " << match.first->pdgId() << " q: " << match.first->charge() << " pt: " << match.first->pt() << " eta: " << match.first->eta() << " phi: " << match.first->phi() << " vtx: " << match.first->vx() << "," << match.first->vy() << "," << match.first->vz() << "\n";
      throw cms::Exception("MFVTrackMatcherLight") << "more than one tracking particle match for track #" << i << ": track pt: " << track_ref->pt() << " eta: " << track_ref->eta() << " phi: " << track_ref->phi() << " dxy: " << track_ref->dxy() << " dz: " << track_ref->dz() << "\n" << out.str();
    }
#endif
    if (nmatch > 0) {
      const auto& match = matches[0];
      const TrackingParticleRef tp = match.first;
      const double quality = match.second;
      const size_t ngen = tp->genParticle().size();
      if (ngen > 1)
	throw cms::Exception("MFVTrackMatcherLight") << "more than one gen particle match for track #" << i;
      else if (ngen == 1) {
	const auto& hepmc = tp->genParticle()[0];
	if (hepmc->barcode() <= 0)
	  throw cms::Exception("MFVTrackMatcherLight") << "hepmc barcode <= 0 (=" << hepmc->barcode() << ") for track #" << i;
	int gen_ndx = hepmc->barcode()-1; // JMTBAD
	const reco::GenParticle& gen = gen_particles->at(gen_ndx);
	(*output)[int(i)] = LightTrackMatch(quality,
					    gen.pt(), gen.eta(), gen.phi(),
					    gen_ndx,
					    nmatch > 1,
					    has_any_ancestor_with_id(&gen, 1000021) || has_any_ancestor_with_id(&gen, 1000022));
      }
    }
  }
    
  event.put(output);
}

DEFINE_FWK_MODULE(MFVTrackMatcherLight);
