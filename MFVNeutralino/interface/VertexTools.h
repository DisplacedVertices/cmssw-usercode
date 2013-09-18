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
    double maxtrackpt; // JMTBAD

    vertex_tracks_distance(const reco::Vertex& sv, const double track_vertex_weight_min);
  };

  struct vertex_distances {
    std::pair<bool,float> bs2dcompat, pv2dcompat, pv3dcompat;
    Measurement1D gen2ddist, gen3ddist, bs2ddist;
    float bs3ddist;
    float pv2ddist_val, pv3ddist_val;
    float pv2ddist_err, pv3ddist_err;
    float pv2ddist_sig, pv3ddist_sig;
    float costhmombs, costhmompv2d, costhmompv3d;

    vertex_distances(const reco::Vertex& sv, const std::vector<double>& gen_vertices, const reco::BeamSpot& beamspot, const reco::Vertex* primary_vertex);
  };
}

#endif
