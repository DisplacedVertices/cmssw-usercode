#include "JMTucker/MFVNeutralino/interface/VertexAuxSorter.h"

namespace mfv {
  VertexAuxSorter::VertexAuxSorter(const std::string& x) {
    if (x == "mass")
      sort_by = sort_by_mass;
    else if (x == "ntracks")
      sort_by = sort_by_ntracks;
    else if (x == "ntracks_then_mass")
      sort_by = sort_by_ntracks_then_mass;
    else
      throw std::invalid_argument("invalid sort_by");
  }

  void VertexAuxSorter::sort(VertexAuxCollection& v) const {
    if (sort_by == sort_by_mass)
      std::sort(v.begin(), v.end(), by_mass);
    else if (sort_by == sort_by_ntracks)
      std::sort(v.begin(), v.end(), by_ntracks);
    else if (sort_by == sort_by_ntracks_then_mass)
      std::sort(v.begin(), v.end(), by_ntracks_then_mass);
  }
}
