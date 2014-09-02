#include "TH2.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/CSCRecHit/interface/CSCRecHit2DCollection.h"
#include "DataFormats/CSCRecHit/interface/CSCSegmentCollection.h"
#include "DataFormats/DTRecHit/interface/DTRecHitCollection.h"
#include "DataFormats/DTRecHit/interface/DTRecSegment4DCollection.h"
#include "DataFormats/RPCRecHit/interface/RPCRecHitCollection.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/TrajectorySeed/interface/TrajectorySeedCollection.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "Geometry/CommonDetUnit/interface/GeomDet.h"
#include "Geometry/CommonDetUnit/interface/GlobalTrackingGeometry.h"
#include "Geometry/Records/interface/GlobalTrackingGeometryRecord.h"

class MFVCosmicActivity : public edm::EDAnalyzer {
public:
  explicit MFVCosmicActivity(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

  std::map<std::string, TH1F*> h_n;

  std::string tag2string(const edm::InputTag& tag) const {
    return tag.label();
  }
    
  template <typename T>
  void fill(const edm::Event& event, const edm::InputTag tag) {
    edm::Handle<T> objs;
    event.getByLabel(tag, objs);
    h_n[tag2string(tag)]->Fill(objs->size());
  }

  TH2F* h_seg_dt;
  TH2F* h_seg_dt_upper;
  TH2F* h_seg_csc;
  TH2F* h_seg_csc_upper;

  TH1F* h_trigs_found;
  TH1F* h_trigs_pass;
};

MFVCosmicActivity::MFVCosmicActivity(const edm::ParameterSet&) {
  edm::Service<TFileService> fs;

  const std::vector<std::string> tags = {
    "dt1DRecHits",
    "dt4DSegments",
    "dt1DCosmicRecHits",
    "dt4DCosmicSegments",
    "csc2DRecHits",
    "cscSegments",
    "rpcRecHits",
    "ancientMuonSeed",
    "standAloneMuons",
    "CosmicMuonSeed",
    "cosmicMuons",
    "cosmicMuons1Leg",

    "dt4DCosmicSegments_stat34",
    "dt4DCosmicSegments_stat34upper",
    "cscSegments_notME11or2",
    "cscSegments_notME11or2upper",
    "muSegments_outer",
    "muSegments_outerupper"
  };

  for (const edm::InputTag& tag : tags) {
    const std::string& stag = tag2string(tag);
    h_n[stag] = fs->make<TH1F>(TString::Format("h_n_%s", stag.c_str()), TString::Format(";# of %s;events", stag.c_str()), 100, 0, 100);
  }

  h_seg_dt        = fs->make<TH2F>("h_seg_dt",        ";wheel;station", 5, -2, 3, 4, 1, 5);
  h_seg_dt_upper  = fs->make<TH2F>("h_seg_dt_upper",  ";wheel;station", 5, -2, 3, 4, 1, 5);
  h_seg_csc       = fs->make<TH2F>("h_seg_csc",       ";station;ring", 9, -4, 5, 3, 1, 4);
  h_seg_csc_upper = fs->make<TH2F>("h_seg_csc_upper", ";station;ring", 9, -4, 5, 3, 1, 4);

  h_trigs_found = fs->make<TH1F>("h_trigs_found", "", 3, 0, 3);
  h_trigs_pass = fs->make<TH1F>("h_trigs_pass", "", 3, 0, 3);
}

const GeomDet* geom_det(const edm::EventSetup& setup, const DetId& id) {
  edm::ESHandle<GlobalTrackingGeometry> geometry;
  setup.get<GlobalTrackingGeometryRecord>().get(geometry);
  return geometry->idToDet(id);
}

void MFVCosmicActivity::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  fill<DTRecHitCollection>       (event, edm::InputTag("dt1DRecHits"));
  fill<DTRecSegment4DCollection> (event, edm::InputTag("dt4DSegments"));
  fill<DTRecHitCollection>       (event, edm::InputTag("dt1DCosmicRecHits"));
  fill<DTRecSegment4DCollection> (event, edm::InputTag("dt4DCosmicSegments"));
  fill<CSCRecHit2DCollection>    (event, edm::InputTag("csc2DRecHits"));
  fill<CSCSegmentCollection>     (event, edm::InputTag("cscSegments"));
  fill<RPCRecHitCollection>      (event, edm::InputTag("rpcRecHits"));
  fill<TrajectorySeedCollection> (event, edm::InputTag("ancientMuonSeed"));
  fill<reco::TrackCollection>    (event, edm::InputTag("standAloneMuons"));
  fill<TrajectorySeedCollection> (event, edm::InputTag("CosmicMuonSeed"));
  fill<reco::TrackCollection>    (event, edm::InputTag("cosmicMuons"));
  fill<reco::TrackCollection>    (event, edm::InputTag("cosmicMuons1Leg"));

  edm::Handle<DTRecSegment4DCollection> dt_segments;
  event.getByLabel("dt4DCosmicSegments", dt_segments);
  edm::Handle<CSCSegmentCollection> csc_segments;
  event.getByLabel("cscSegments", csc_segments);

  int dt_seg_stat34 = 0;
  int dt_seg_stat34upper = 0;
  int csc_seg_notME11or2 = 0;
  int csc_seg_notME11or2upper = 0;

  for (const auto& seg : *dt_segments) {
    const DTChamberId& id = seg.chamberId();
    const bool upper = geom_det(setup, id)->toGlobal(seg.localPosition()).y() > 0;

    h_seg_dt->Fill(id.wheel(), id.station());
    if (upper)
      h_seg_dt_upper->Fill(id.wheel(), id.station());

    if (id.station() >= 3) {
      ++dt_seg_stat34;
      if (upper)
        ++dt_seg_stat34upper;
    }
  }
      
  for (const auto& seg : *csc_segments) {
    const CSCDetId& id = seg.cscDetId();
    const int stat = (id.endcap() == 2 ? -1 : 1) * id.station();
    const bool upper = geom_det(setup, id)->toGlobal(seg.localPosition()).y() > 0;

    h_seg_csc->Fill(stat, id.ring());
    if (upper)
      h_seg_csc_upper->Fill(stat, id.ring());

    if (id.station() > 1 || (id.station() == 1 && id.ring() == 3)) {
      ++csc_seg_notME11or2;
      if (upper);
        ++csc_seg_notME11or2upper;
    }
  }

  h_n["dt4DCosmicSegments_stat34"]     ->Fill(dt_seg_stat34);
  h_n["dt4DCosmicSegments_stat34upper"]->Fill(dt_seg_stat34upper);
  h_n["cscSegments_notME11or2"]        ->Fill(csc_seg_notME11or2);
  h_n["cscSegments_notME11or2upper"]   ->Fill(csc_seg_notME11or2upper);
  h_n["muSegments_outer"]              ->Fill(dt_seg_stat34 + csc_seg_notME11or2);
  h_n["muSegments_outerupper"]         ->Fill(dt_seg_stat34upper + csc_seg_notME11or2upper);


  edm::Handle<edm::TriggerResults> hlt_results;
  event.getByLabel(edm::InputTag("TriggerResults", "", "HLT"), hlt_results);
  const edm::TriggerNames& hlt_names = event.triggerNames(*hlt_results);
  const size_t npaths = hlt_names.size();

  const char* paths[3] = { "HLT_BeamHalo", "HLT_L1SingleMuOpen_AntiBPTX", "HLT_L1TrackerCosmics" };
  bool found[3] = {0};
  bool pass[3] = {0};
  for (int i = 0; i < 3; ++i) {
    for (int v = 0; v < 100; ++v) {
      char path[1024];
      snprintf(path, 1024, "%s_v%i", paths[i], v);
      const size_t ipath = hlt_names.triggerIndex(path);
      if (ipath >= npaths)
        continue;
      found[i] = true;
      pass[i] = hlt_results->accept(ipath);
      break;
    }

    if (found[i]) h_trigs_found->Fill(i);
    if (pass [i]) h_trigs_pass ->Fill(i);
  }
}

DEFINE_FWK_MODULE(MFVCosmicActivity);
