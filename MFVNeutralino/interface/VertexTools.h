#ifndef JMTucker_MFVNeutralino_VertexTools_h
#define JMTucker_MFVNeutralino_VertexTools_h

#include "DataFormats/GeometryCommonDetAlgo/interface/Measurement1D.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "JMTucker/MFVNeutralino/interface/JetVertexAssociation.h"

namespace mfv {
  static const double track_vertex_weight_min = 0.5; // JMTBAD unify
  enum Momenta { PTracksOnly, PJetsByNtracks, PJetsByCombination, PTracksPlusJetsByNtracks, PTracksPlusJetsByCombination, NMomenta }; // JMTBAD keep in sync

  float abs_error(const reco::Vertex& sv, bool use3d);
  Measurement1D gen_dist(const reco::Vertex& sv, const std::vector<double>& gen_verts, const bool use3d);
  std::pair<bool, float> compatibility(const reco::Vertex& x, const reco::Vertex& y, bool use3d);

  Measurement1D miss_dist(const reco::Vertex& v0, const reco::Vertex& v1, const math::XYZTLorentzVector& mom);

  struct vertex_tracks_distance {
    double drmin, drmax;
    double dravg, dravgw, dravgvw;
    double drrms, drrmsw, drrmsvw;

    vertex_tracks_distance(const reco::Vertex& sv);
  };

  struct vertex_distances {
    std::pair<bool,float> bs2dcompat, pv2dcompat, pv3dcompat;
    Measurement1D gen2ddist, gen3ddist, bs2ddist;
    float bs3ddist;
    float pv2ddist_val, pv3ddist_val;
    float pv2ddist_err, pv3ddist_err;
    float pv2ddist_sig, pv3ddist_sig;
    std::vector<float> costhmombs, costhmompv2d, costhmompv3d;
    std::vector<Measurement1D> missdistpv;

    vertex_distances(const reco::Vertex& sv, const std::vector<double>& gen_vertices, const reco::BeamSpot& beamspot, const reco::Vertex* primary_vertex, const std::vector<math::XYZTLorentzVector>& momenta);
  };
}

#endif
