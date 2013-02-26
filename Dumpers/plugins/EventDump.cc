#include "DataFormats/Common/interface/DetSet.h"
#include "DataFormats/Common/interface/DetSetVector.h"
#include "DataFormats/CSCRecHit/interface/CSCSegmentCollection.h"
#include "DataFormats/DTRecHit/interface/DTRecHitCollection.h"
#include "DataFormats/DTRecHit/interface/DTRecSegment4DCollection.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/RPCRecHit/interface/RPCRecHitCollection.h"
#include "DataFormats/SiStripDigi/interface/SiStripDigi.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/TrackReco/interface/TrackToTrackMap.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "SimDataFormats/Track/interface/SimTrackContainer.h"
#include "SimDataFormats/TrackingAnalysis/interface/TrackingParticleFwd.h"
#include "SimDataFormats/TrackingHit/interface/PSimHitContainer.h"
#include "SimDataFormats/Vertex/interface/SimVertexContainer.h"
#include "JMTucker/Dumpers/interface/Dumpers.h"

class JMTEventDump : public edm::EDAnalyzer {
public:
  explicit JMTEventDump(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  typedef std::vector<edm::InputTag> VInputTag;
  VInputTag genparticle_labels;
  VInputTag simhit_labels;
  VInputTag trackingparticle_labels;
  VInputTag rpchit_labels;
  VInputTag cscsegment_labels;
  VInputTag dt1dhit_labels;
  VInputTag dt4dsegment_labels;
  VInputTag track_labels;
  VInputTag muon_labels;
  VInputTag t2tmap_labels;
  VInputTag strip_digi_labels;
  VInputTag points_labels;
  VInputTag errors_labels;
  VInputTag beamspot_labels;
  VInputTag trajectoryseed_labels;
  VInputTag compositecandidate_labels;

  bool use_cout;
};

////////////////////////////////////////////////////////////////////////////////

JMTEventDump::JMTEventDump(const edm::ParameterSet& cfg) {
  if (cfg.exists("genparticle_labels"))
    genparticle_labels = cfg.getUntrackedParameter<VInputTag>("genparticle_labels");
  if (cfg.exists("simhit_labels"))
    simhit_labels = cfg.getUntrackedParameter<VInputTag>("simhit_labels");
  if (cfg.exists("trackingparticle_labels"))
    trackingparticle_labels = cfg.getUntrackedParameter<VInputTag>("trackingparticle_labels");
  if (cfg.exists("rpchit_labels"))
    rpchit_labels = cfg.getUntrackedParameter<VInputTag>("rpchit_labels");
  if (cfg.exists("cscsegment_labels"))
    cscsegment_labels = cfg.getUntrackedParameter<VInputTag>("cscsegment_labels");
  if (cfg.exists("dt1dhit_labels"))
    dt1dhit_labels = cfg.getUntrackedParameter<VInputTag>("dt1dhit_labels");
  if (cfg.exists("dt4dsegment_labels"))
    dt4dsegment_labels = cfg.getUntrackedParameter<VInputTag>("dt4dsegment_labels");
  if (cfg.exists("track_labels"))
    track_labels = cfg.getUntrackedParameter<VInputTag>("track_labels");
  if (cfg.exists("muon_labels"))
    muon_labels = cfg.getUntrackedParameter<VInputTag>("muon_labels");
  if (cfg.exists("t2tmap_labels"))
    t2tmap_labels = cfg.getUntrackedParameter<VInputTag>("t2tmap_labels");
  if (cfg.exists("strip_digi_labels"))
    strip_digi_labels = cfg.getUntrackedParameter<VInputTag>("strip_digi_labels");
  if (cfg.exists("points_labels"))
    points_labels = cfg.getUntrackedParameter<VInputTag>("points_labels");
  if (cfg.exists("errors_labels"))
    errors_labels = cfg.getUntrackedParameter<VInputTag>("errors_labels");
  if (cfg.exists("beamspot_labels"))
    beamspot_labels = cfg.getUntrackedParameter<VInputTag>("beamspot_labels");
  if (cfg.exists("trajectoryseed_labels"))
    trajectoryseed_labels = cfg.getUntrackedParameter<VInputTag>("trajectoryseed_labels");
  if (cfg.exists("compositecandidate_labels"))
    compositecandidate_labels = cfg.getUntrackedParameter<VInputTag>("compositecandidate_labels");

  use_cout = cfg.getUntrackedParameter<bool>("use_cout", false);
}

void JMTEventDump::analyze(const edm::Event& event, const edm::EventSetup& event_setup) {
  std::ostringstream out;
  
  JMTDumper::set(event, event_setup);
  out << event;

  JMTDumper::dump_all<reco::GenParticleCollection>(out, "GenParticles", genparticle_labels);
  JMTDumper::dump_all<edm::PSimHitContainer>(out, "SimHits", simhit_labels);
  JMTDumper::dump_all<TrackingParticleCollection>(out, "TrackingParticles", trackingparticle_labels);
  JMTDumper::dump_all<RPCRecHitCollection>(out, "RPCHits", rpchit_labels);
  JMTDumper::dump_all<CSCSegmentCollection>(out, "CSCSegments", cscsegment_labels);
  JMTDumper::dump_all<DTRecHitCollection>(out, "DTRecHitPairs", dt1dhit_labels);
  JMTDumper::dump_all<DTRecSegment4DCollection>(out, "DTSegments", dt4dsegment_labels);
  JMTDumper::dump_all<reco::TrackCollection>(out, "Tracks", track_labels);
  JMTDumper::dump_all<reco::MuonCollection>(out, "Muons", muon_labels);
  JMTDumper::dump_all<std::vector<LocalPoint> >(out, "LocalPoints", points_labels);
  JMTDumper::dump_all<std::vector<LocalError> >(out, "LocalErrors", errors_labels);
  JMTDumper::dump_all<std::vector<TrajectorySeed> >(out, "TrajectorySeeds", trajectoryseed_labels);
  JMTDumper::dump_all<pat::CompositeCandidateCollection>(out, "pat::CompositeCandidates", compositecandidate_labels);

  JMTDumper::dump_each<reco::TrackToTrackMap>(out, "TrackToTrackMaps", t2tmap_labels);
  JMTDumper::dump_each<reco::BeamSpot>(out, "BeamSpots", beamspot_labels);

  typedef edm::DetSetVector<SiStripDigi> SiStripDigis;
  for (const edm::InputTag& strip_digi_label : strip_digi_labels) {
    edm::Handle<edm::DetSetVector<SiStripDigi> > strip_digi_sets;
    event.getByLabel(strip_digi_label, strip_digi_sets);
    
    SiStripDigis::const_iterator set = strip_digi_sets->begin(), sete = strip_digi_sets->end();
    for ( ; set != sete; ++set) {
      DetId d(set->id);
      out << "Strip digis in " << d << "\n";
      int i = 0;
      edm::DetSet<SiStripDigi>::const_iterator digi = set->data.begin(), digie = set->data.end();
      for ( ; digi != digie; ++digi, ++i)
	out << "#" << i << ": adc: " << digi->adc() << " channel: " << digi->channel() << " strip: " << digi->strip() << std::endl;
    }
  }

  if (use_cout)
    std::cout << out.str();
  else
    edm::LogInfo("JMTEventDump") << out.str();
}

DEFINE_FWK_MODULE(JMTEventDump);
