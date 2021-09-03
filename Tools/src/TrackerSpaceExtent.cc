#include "DVCode/Tools/interface/TrackerSpaceExtent.h"

#include "DataFormats/SiPixelDetId/interface/PXBDetId.h"
#include "DataFormats/SiPixelDetId/interface/PXFDetId.h"
#include "DataFormats/SiStripDetId/interface/SiStripDetId.h"
#include "DataFormats/TrackReco/interface/HitPattern.h"
#include "DataFormats/TrackerCommon/interface/TrackerTopology.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "Geometry/CommonDetUnit/interface/GlobalTrackingGeometry.h"
#include "Geometry/Records/interface/GlobalTrackingGeometryRecord.h"
#include "Geometry/Records/interface/TrackerTopologyRcd.h"

void TrackerSpaceExtents::fill(const edm::EventSetup& setup, const GlobalPoint& origin) {
  edm::ESHandle<TrackerTopology> topology;
  setup.get<TrackerTopologyRcd>().get(topology);

  edm::ESHandle<GlobalTrackingGeometry> geometry;
  setup.get<GlobalTrackingGeometryRecord>().get(geometry);
  const TrackingGeometry* tg = geometry->slaveGeometry(PXBDetId(1, 1, 1));
  if (tg == 0)
    throw cms::Exception("TrackerSpaceExtents") << "null slave geometry";
  const TrackerGeometry* tktg = dynamic_cast<const TrackerGeometry*>(tg);
  if (tktg == 0)
    throw cms::Exception("TrackerSpaceExtents") << "couldn't cast tg to tktg";

  // JMTBAD when do PXB/FDetId go away? ttps://twiki.cern.ch/twiki/bin/view/CMS/SiStripLocalReco_notesSiStripSubDetIdToTrackerTopologyMigration#Remaining_PXBDetId_and_PXFDetId
  fill_subdet<PXBDetId>(map, tktg->detsPXB(), [](const PXBDetId& id) { return id.layer(); }, origin);
  fill_subdet<PXFDetId>(map, tktg->detsPXF(), [](const PXFDetId& id) { return id.disk (); }, origin); 
  fill_subdet<SiStripDetId>(map, tktg->detsTIB(), [&](const SiStripDetId& id) { return topology->tibLayer(id); }, origin);
  fill_subdet<SiStripDetId>(map, tktg->detsTOB(), [&](const SiStripDetId& id) { return topology->tobLayer(id); }, origin);
  fill_subdet<SiStripDetId>(map, tktg->detsTID(), [&](const SiStripDetId& id) { return topology->tidWheel(id); }, origin);
  fill_subdet<SiStripDetId>(map, tktg->detsTEC(), [&](const SiStripDetId& id) { return topology->tecWheel(id); }, origin);
  filled_ = true;
}

void TrackerSpaceExtents::print() const {
  for (const auto& extent : map) {
    printf("sub %i  subsub: %i ", extent.first.first, extent.first.second);
    extent.second.print();
    printf("\n");
  }
}

// JMTBAD reduce code duplication

NumExtents TrackerSpaceExtents::numExtentInRAndZ(const reco::HitPattern& hp, int code) const {
  NumExtents ret;
  for (int ihit = 0, ie = hp.numberOfAllHits(reco::HitPattern::TRACK_HITS); ihit < ie; ++ihit) {
    uint32_t hit = hp.getHitPattern(reco::HitPattern::TRACK_HITS, ihit);

    bool is_valid = hp.getHitType(hit) == 0;
    if (!is_valid)
      continue;

    bool is_tk = (hit >> 10) & 0x1;
    if (!is_tk)
      continue;

    uint32_t sub    = reco::HitPattern::getSubStructure   (hit);
    uint32_t subsub = reco::HitPattern::getSubSubStructure(hit);
    
    if (sub != PixelSubdetector::PixelBarrel && sub != PixelSubdetector::PixelEndcap && sub != StripSubdetector::TIB && sub != StripSubdetector::TOB && sub != StripSubdetector::TID && sub != StripSubdetector::TEC)
      throw cms::Exception("TrackerSpaceExtents") << "unknown sub " << sub << " with subsub " << subsub;

    if (code != StripOnly) {
      if (sub == PixelSubdetector::PixelBarrel)
        ret.update_r(subsub);
      else if (sub == PixelSubdetector::PixelEndcap)
        ret.update_z(subsub);
    }
    if (code != PixelOnly) {
      if (sub == StripSubdetector::TIB)
        ret.update_r(4 + subsub);
      else if (sub == StripSubdetector::TOB)
        ret.update_r(8 + subsub);
      else if (sub == StripSubdetector::TID)
        ret.update_z(3 + subsub);
      else if (sub == StripSubdetector::TEC)
        ret.update_z(6 + subsub);
    }
  }

  return ret;
}

SpatialExtents TrackerSpaceExtents::extentInRAndZ(const reco::HitPattern& hp, int code) const {
  if (!filled_) throw cms::Exception("CantEven", "must set up map with fill() before calling extentInRAndZ");

  SpatialExtents ret;

  for (int ihit = 0, ie = hp.numberOfAllHits(reco::HitPattern::TRACK_HITS); ihit < ie; ++ihit) {
    uint32_t hit = hp.getHitPattern(reco::HitPattern::TRACK_HITS, ihit);
        
    bool is_valid = hp.getHitType(hit) == 0;
    if (!is_valid)
      continue;

    bool is_tk = (hit >> 10) & 0x1;
    if (!is_tk)
      continue;

    uint32_t sub    = reco::HitPattern::getSubStructure   (hit);
    uint32_t subsub = reco::HitPattern::getSubSubStructure(hit);
        
    map_t::const_iterator it = map.find(std::make_pair(int(sub), int(subsub)));
    if (it == map.end()) {
      printf("hit %x sub %x subsub %x not found!\n", hit, sub, subsub);
      assert(0);
    }
    const TrackerSpaceExtent& extent = it->second;
    if ((code != StripOnly && sub == PixelSubdetector::PixelBarrel) || (code != PixelOnly && (sub == StripSubdetector::TIB || sub == StripSubdetector::TOB)))
      ret.update_r(extent.avg_r);
    else if ((code != StripOnly && sub == PixelSubdetector::PixelEndcap) || (code != PixelOnly && (sub == StripSubdetector::TID || sub == StripSubdetector::TEC)))
      ret.update_z(extent.avg_z);
  }

  return ret;
}

int TrackerSpaceExtents::numHitsBehind(const reco::HitPattern& hp, const double r, const double z) const {
  if (!filled_) throw cms::Exception("CantEven", "must set up map with fill() before calling numHitsBehind");

  int nhitsbehind = 0;

  for (int ihit = 0, ie = hp.numberOfAllHits(reco::HitPattern::TRACK_HITS); ihit < ie; ++ihit) {
    uint32_t hit = hp.getHitPattern(reco::HitPattern::TRACK_HITS, ihit);
        
    bool is_valid = hp.getHitType(hit) == 0;
    if (!is_valid)
      continue;

    bool is_tk = (hit >> 10) & 0x1;
    if (!is_tk)
      continue;

    uint32_t sub    = reco::HitPattern::getSubStructure   (hit);
    uint32_t subsub = reco::HitPattern::getSubSubStructure(hit);
        
    map_t::const_iterator it = map.find(std::make_pair(int(sub), int(subsub)));
    assert(it != map.end());
    const TrackerSpaceExtent& extent = it->second;
    if (sub == PixelSubdetector::PixelBarrel || sub == StripSubdetector::TIB || sub == StripSubdetector::TOB) {
      if (extent.max_r < r)
        ++nhitsbehind;
    }
    else if (sub == PixelSubdetector::PixelEndcap || sub == StripSubdetector::TID || sub == StripSubdetector::TEC) {
      if (extent.max_z < z)
        ++nhitsbehind;
    }
  }

  return nhitsbehind;
}
