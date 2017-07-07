#ifndef JMTucker_Tools_TrackerSpaceExtent_h
#define JMTucker_Tools_TrackerSpaceExtent_h

//#include <map>
#include "Geometry/CommonDetUnit/interface/GeomDet.h"
#include "Geometry/TrackerGeometryBuilder/interface/TrackerGeometry.h"

namespace edm {
  class EventSetup;
}

namespace reco {
  class HitPattern;
}

struct TrackerSpaceExtent {
  double min_r;
  double max_r;
  double avg_r;
  int nr;
  double min_z;
  double max_z;
  double avg_z;
  int nz;
  TrackerSpaceExtent() : min_r(1e99), max_r(0), avg_r(0), nr(0), min_z(1e99), max_z(0), avg_z(0), nz(0) {}

  void add(double r, double z) {
    if (r < min_r)
      min_r = r;
    if (r > max_r)
      max_r = r;
    avg_r = (nr*avg_r + r)/(nr+1);
    ++nr;

    if (z < min_z)
      min_z = z;
    if (z > max_z)
      max_z = z;
    avg_z = (nz*avg_z + z)/(nz+1);
    ++nz;
  }

  void print() const {
    printf("r stats: %7.3f-%7.3f (avg %7.3f)   z stats: %7.3f-%7.3f (avg %7.3f)", min_r, max_r, avg_r, min_z, max_z, avg_z);
  }
};

template <typename T>
struct Extents {
  T min_r;
  T max_r;
  T min_z;
  T max_z;

  Extents() : min_r(2e9), max_r(-2e9), min_z(2e9), max_z(-2e9) {}

  void update_r(T r) {
    if (r > max_r) max_r = r;
    if (r < min_r) min_r = r;
  }

  void update_z(T z) {
    if (z > max_z) max_z = z;
    if (z < min_z) min_z = z;
  }
};

typedef Extents<double> SpatialExtents;
typedef Extents<int> NumExtents;

class TrackerSpaceExtents {
public:
  TrackerSpaceExtents() : filled_(false) {}
  bool filled() const { return filled_; }
  typedef std::map<std::pair<int, int>, TrackerSpaceExtent> map_t;
  map_t map;

  void fill(const edm::EventSetup&, const GlobalPoint& origin);
  void print() const;
  enum { AllowAll, PixelOnly, StripOnly };
  NumExtents numExtentInRAndZ(const reco::HitPattern&, int code) const;
  SpatialExtents extentInRAndZ(const reco::HitPattern&, int code) const;
  int numHitsBehind(const reco::HitPattern&, const double r, const double z) const;

private:
  bool filled_;

  template <typename Id, typename SubFunc>
  void fill_subdet(map_t& extents, const TrackingGeometry::DetContainer& dets, SubFunc substructure, const GlobalPoint& origin) {
    for (const GeomDet* geom : dets) {
      const GlobalPoint pos = geom->toGlobal(LocalPoint());
      const double dx = pos.x() - origin.x();
      const double dy = pos.y() - origin.y();
      const double r = sqrt(dx*dx + dy*dy);
      const double z = fabs(pos.z() - origin.z());
      
      Id id(geom->geographicalId());
      std::pair<int, int> which_element = std::make_pair(id.subdetId(), substructure(id));
      if (extents.find(which_element) == extents.end())
        extents[which_element] = TrackerSpaceExtent();
      extents[which_element].add(r, z);
    }
  }
};

#endif
