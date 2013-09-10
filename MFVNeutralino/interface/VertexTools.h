#ifndef JMTucker_MFVNeutralino_VertexTools_h
#define JMTucker_MFVNeutralino_VertexTools_h

#include "DataFormats/GeometryCommonDetAlgo/interface/Measurement1D.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

namespace mfv {
  float abs_error(const reco::Vertex& sv, bool use3d);
  Measurement1D gen_dist(const reco::Vertex& sv, const std::vector<double>& gen_verts, const bool use3d);
  std::pair<bool, float> compatibility(const reco::Vertex& x, const reco::Vertex& y, bool use3d);

  struct vertex_tracks_distance {
    double drmin, drmax;
    double dravg, dravgw, dravgvw;
    double drrms, drrmsw, drrmsvw;

    vertex_tracks_distance(const reco::Vertex& sv, const double track_vertex_weight_min);
  };
}

#endif
