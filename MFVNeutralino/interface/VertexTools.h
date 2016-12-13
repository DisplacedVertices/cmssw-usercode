#ifndef JMTucker_MFVNeutralino_VertexTools_h
#define JMTucker_MFVNeutralino_VertexTools_h

#include "DataFormats/GeometryCommonDetAlgo/interface/Measurement1D.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"

namespace mfv {
  static const double track_vertex_weight_min = 0.5; // JMTBAD unify

  reco::Vertex aux_to_reco(const MFVVertexAux& aux);

  float abs_error(const reco::Vertex& sv, bool use3d);
  Measurement1D gen_dist(const reco::Vertex& sv, const std::vector<double>& gen_verts, const bool use3d);
  std::pair<bool, float> compatibility(const reco::Vertex& x, const reco::Vertex& y, bool use3d);

  Measurement1D miss_dist(const reco::Vertex& v0, const reco::Vertex& v1, const math::XYZTLorentzVector& mom);

  struct vertex_distances {
    std::pair<bool,float> bs2dcompat, pv2dcompat, pv3dcompat;
    Measurement1D gen2ddist, gen3ddist, bs2ddist;
    float pv2ddist_val, pv3ddist_val;
    float pv2ddist_err, pv3ddist_err;
    float pv2ddist_sig, pv3ddist_sig;
    std::vector<float> costhmombs, costhmompv2d, costhmompv3d;
    std::vector<Measurement1D> missdistpv;

    vertex_distances(const reco::Vertex& sv, const std::vector<double>& gen_vertices, const reco::BeamSpot& beamspot, const reco::Vertex* primary_vertex, const std::vector<math::XYZTLorentzVector>& momenta);
  };

  struct track_cluster {
    TLorentzVector p4;
    std::vector<size_t> tracks;
  };

  struct track_clusters {
    double track_mass;
    double R;
    int algo;
    int recomb_scheme;
    std::vector<track_cluster> clusters_;
    size_t size() const { return clusters_.size(); }
    track_cluster& operator[](size_t i) { return clusters_[i]; }
    const track_cluster& operator[](size_t i) const { return clusters_[i]; }
    void resize(size_t i) { clusters_.resize(i); }
  };
}

// JMTBAD mfv::
struct MFVVertexAuxSorter {
  enum sort_by_this { sort_by_mass, sort_by_ntracks, sort_by_ntracks_then_mass };
  sort_by_this sort_by;

  MFVVertexAuxSorter(const std::string& x) {
    if (x == "mass")
      sort_by = sort_by_mass;
    else if (x == "ntracks")
      sort_by = sort_by_ntracks;
    else if (x == "ntracks_then_mass")
      sort_by = sort_by_ntracks_then_mass;
    else
      throw cms::Exception("MFVVertexTools") << "invalid sort_by";
  }

  static bool by_mass(const MFVVertexAux& a, const MFVVertexAux& b) {
    return a.mass[0] > b.mass[0];
  }

  static bool by_ntracks(const MFVVertexAux& a, const MFVVertexAux& b) {
    return a.ntracks() > b.ntracks();
  }

  static bool by_ntracks_then_mass(const MFVVertexAux& a, const MFVVertexAux& b) {
    if (a.ntracks() == b.ntracks())
      return a.mass[0] > b.mass[0];
    return a.ntracks() > b.ntracks();
  }

  void sort(MFVVertexAuxCollection& v) const {
    if (sort_by == sort_by_mass)
      std::sort(v.begin(), v.end(), by_mass);
    else if (sort_by == sort_by_ntracks)
      std::sort(v.begin(), v.end(), by_ntracks);
    else if (sort_by == sort_by_ntracks_then_mass)
      std::sort(v.begin(), v.end(), by_ntracks_then_mass);
  }
};    


#endif
