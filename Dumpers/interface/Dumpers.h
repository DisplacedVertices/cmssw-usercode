#ifndef JMTucker_Dumpers_interface_Dumpers_h
#define JMTucker_Dumpers_interface_Dumpers_h

#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/CSCRecHit/interface/CSCSegment.h"
#include "DataFormats/DTRecHit/interface/DTRecHit1D.h"
#include "DataFormats/DTRecHit/interface/DTRecHit1DPair.h"
#include "DataFormats/DTRecHit/interface/DTRecSegment4D.h"
#include "DataFormats/EcalDetId/interface/EcalSubdetector.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/MuonDetId/interface/CSCDetId.h"
#include "DataFormats/MuonDetId/interface/DTWireId.h"
#include "DataFormats/MuonDetId/interface/RPCDetId.h"
#include "DataFormats/MuonDetId/interface/MuonSubdetId.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/CompositeCandidate.h"
#include "DataFormats/RPCRecHit/interface/RPCRecHit.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackToTrackMap.h"
#include "DataFormats/TrajectorySeed/interface/TrajectorySeed.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "Geometry/CommonDetUnit/interface/GeomDet.h"
#include "SimDataFormats/EncodedEventId/interface/EncodedEventId.h"
#include "SimDataFormats/Track/interface/SimTrack.h"
#include "SimDataFormats/TrackingAnalysis/interface/TrackingParticle.h"
#include "SimDataFormats/TrackingHit/interface/PSimHit.h"
#include "SimDataFormats/Vertex/interface/SimVertex.h"

std::ostream& operator<<(std::ostream&, const edm::Event&);
std::ostream& operator<<(std::ostream&, const EncodedEventId&);
std::ostream& operator<<(std::ostream&, const DetId&);
std::ostream& operator<<(std::ostream&, const DTRecHit1D&);
std::ostream& operator<<(std::ostream&, const DTRecHit1DPair&);
std::ostream& operator<<(std::ostream&, const DTRecSegment4D&);
std::ostream& operator<<(std::ostream&, const CSCSegment&);
std::ostream& operator<<(std::ostream&, const RPCRecHit&);
std::ostream& operator<<(std::ostream&, const reco::HitPattern&);
std::ostream& operator<<(std::ostream&, const reco::Track&);
std::ostream& operator<<(std::ostream&, const reco::Muon&);
std::ostream& operator<<(std::ostream&, const TrackingRecHit&);
std::ostream& operator<<(std::ostream&, const TrajectorySeed&);
std::ostream& operator<<(std::ostream&, const reco::TrackToTrackMap&);
std::ostream& operator<<(std::ostream&, const reco::BeamSpot&);
std::ostream& operator<<(std::ostream&, const reco::GenParticle&);
std::ostream& operator<<(std::ostream&, const PSimHit&);
std::ostream& operator<<(std::ostream&, const SimVertex&);
std::ostream& operator<<(std::ostream&, const SimTrack&);
std::ostream& operator<<(std::ostream&, const TrackingParticle&);
std::ostream& operator<<(std::ostream&, const pat::CompositeCandidate&);

struct JMTDumper {
  static bool warn;
  static const edm::Event* event;
  static const edm::EventSetup* event_setup;

  static void set(const edm::Event& e, const edm::EventSetup& es) {
    event = &e;
    event_setup = &es;
  }

  static const GeomDet* geom_det(const DetId& raw_id);

  template <typename T>
  static void dump_ref(std::ostream& out, const edm::Ref<T>& ref) {
    out << "ref with product id " << ref.id().id();
    if (ref.id().id() == 0) {
      out << "\n";
      return;
    }
    if (event) {
      edm::Provenance prov = event->getProvenance(ref.id());
      out << ", branch " << prov.branchName() << " (id " << prov.branchID().id() << "),";
    }
    out << " with index " << ref.index() << "\n";
  }

  template <typename T>
  static void dump_object(std::ostream& out, const edm::InputTag& tag) {
    edm::Handle<T> handle;
    event->getByLabel(tag, handle);
      
    if (!handle.failedToGet()) {
      out << "item tagged " << tag.encode() << ":\n";
      ::operator<<(out, *handle);
    }
    else
      out << "item tagged " << tag.encode() << " not found in event!\n";
  }

  template <typename T>
  static void dump_each(std::ostream& out, const char* name, const std::vector<edm::InputTag>& tags) {
    if (tags.size() > 0) {
      out << name << ":\n";
      for (const edm::InputTag& tag : tags) {
	dump_object<T>(out, tag);
	out << "\n";
      }
    }
  }    

  template <typename T>
  static void dump_collection(std::ostream& out, const edm::InputTag& tag) {
    edm::Handle<T> handle;
    event->getByLabel(tag, handle);
      
    if (!handle.failedToGet()) {
      out << "item tagged " << tag.encode() << " (size: " << handle->size() << ")\n";
      for (const auto& item : *handle)
	out << item;
    }
    else
      out << "item tagged " << tag.encode() << " not found in event!\n";
  }

  template <typename T>
  static void dump_all(std::ostream& out, const char* name, const std::vector<edm::InputTag>& tags) {
    if (tags.size() > 0) {
      out << name << ":\n";
      for (const edm::InputTag& tag : tags) {
	dump_collection<T>(out, tag);
	out << "\n";
      }
    }
  }    
};

#endif
