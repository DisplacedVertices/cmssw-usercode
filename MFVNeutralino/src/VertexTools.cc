#include "TVector3.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "RecoVertex/VertexTools/interface/VertexDistanceXY.h"
#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "JMTucker/MFVNeutralino/interface/VertexTools.h"
#include "JMTucker/Tools/interface/Year.h"

namespace {
  template <typename T>
  T mag(T x, T y) {
    return sqrt(x*x + y*y);
  }

  template <typename T>
  T mag(T x, T y, T z) {
    return sqrt(x*x + y*y + z*z);
  }

  template <typename T, typename T2>
  double dot2(const T& a, const T2& b) {
    return a.x() * b.x() + a.y() * b.y();
  }

  template <typename T, typename T2>
  double dot3(const T& a, const T2& b) {
    return a.x() * b.x() + a.y() * b.y() + a.z() * b.z();
  }

  template <typename T, typename T2>
  double costh2(const T& a, const T2& b) {
    return dot2(a,b) / mag(a.x(), a.y()) / mag(b.x(), b.y());
  }

  template <typename T, typename T2>
  double costh3(const T& a, const T2& b) {
    return dot3(a,b) / mag(a.x(), a.y(), a.z()) / mag(b.x(), b.y(), b.z());
  }
}

namespace mfv {
  bool inside_beampipe(bool is_mc, double x, double y) {
    double cx = 0, cy = 0;
    if (!is_mc) {
#ifdef MFVNEUTRALINO_2017
      cx =  0.113;
      cy = -0.180;
#elif defined(MFVNEUTRALINO_2018)
      cx =  0.171;
      cy = -0.175;
#else
#error bad year
#endif
    }

    const double r = 2.09;
    return hypot(x - cx, y - cy) < r;
  }

  float abs_error(const reco::Vertex& sv, bool use3d) {
    const double x = sv.x();
    const double y = sv.y();
    const double z = use3d ? sv.z() : 0;
    AlgebraicVector3 v(x,y,z);
    AlgebraicSymMatrix33 cov = sv.covariance();
    double dist = mag(x,y,z);
    double err2 = ROOT::Math::Similarity(v, cov);
    return dist != 0 ? sqrt(err2)/dist : 0;
  }

  Measurement1D gen_dist(const reco::Vertex& sv, const std::vector<double>& gen_verts, const bool use3d) {
    float dist = 1e99;
    for (int i = 0; i < 2; ++i) {
      float dist_;
      if (use3d)
        dist_ = mag(sv.x() - gen_verts[i*3], sv.y() - gen_verts[i*3+1], sv.z() - gen_verts[i*3+2]);
      else
        dist_ = mag(sv.x() - gen_verts[i*3], sv.y() - gen_verts[i*3+1]);
      if (dist_ < dist) dist = dist_;
    }

    return Measurement1D(dist, abs_error(sv, use3d));
  }

  std::pair<bool, float> compatibility(const reco::Vertex& x, const reco::Vertex& y, bool use3d) {
    bool success = false;
    float compat = 0;
    try {
      if (use3d)
        compat = VertexDistance3D().compatibility(x, y);
      else
        compat = VertexDistanceXY().compatibility(x, y);
      success = true;
    }
    catch (cms::Exception& e) {
      if (e.category().find("matrix inversion problem") == std::string::npos)
        throw;
    }
    return std::make_pair(success, compat);
  }

  Measurement1D miss_dist(const reco::Vertex& v0, const reco::Vertex& v1, const math::XYZTLorentzVector& mom) {
    // miss distance is magnitude of (jet direction (= n) cross (tv - sv) ( = d))
    // to calculate uncertainty, use |n X d|^2 = (|n||d|)^2 - (n . d)^2
    // JMTBAD vector/matrix types
    const TVector3 n = TVector3(mom.x(), mom.y(), mom.z()).Unit();
    const TVector3 d(v1.x() - v0.x(),
                     v1.y() - v0.y(),
                     v1.z() - v0.z());
    const double n_dot_d = n.Dot(d);
    const TVector3 n_cross_d = n.Cross(d);
    const double miss_dist_value = n_cross_d.Mag();

    typedef math::VectorD<3>::type vec_t;
    typedef math::ErrorD<3>::type mat_t;
    const vec_t jacobian(2*d.x() - 2*n_dot_d*n.x(),
                         2*d.y() - 2*n_dot_d*n.y(),
                         2*d.z() - 2*n_dot_d*n.z());
    const mat_t v0_to_v1_cov_matrix = v0.covariance() + v1.covariance();
    const double sigma_f2 = sqrt(ROOT::Math::Similarity(jacobian, v0_to_v1_cov_matrix));

    const double miss_dist_err = sigma_f2 / 2 / miss_dist_value;
    return Measurement1D(miss_dist_value, miss_dist_err);
  }

  vertex_distances::vertex_distances(const reco::Vertex& sv, const std::vector<double>& gen_vertices, const reco::BeamSpot& beamspot, const reco::Vertex* primary_vertex, const std::vector<math::XYZTLorentzVector>& momenta) {
    VertexDistanceXY distcalc_2d;
    VertexDistance3D distcalc_3d;

    gen2ddist = gen_dist(sv, gen_vertices, false);
    gen3ddist = gen_dist(sv, gen_vertices, true);

    const reco::Vertex fake_bs_vtx(beamspot.position(), beamspot.covariance3D());
    bs2dcompat = compatibility(sv, fake_bs_vtx, false);
    bs2ddist = distcalc_2d.distance(sv, fake_bs_vtx);
    const math::XYZVector bs2sv = sv.position() - beamspot.position();

    pv2dcompat = pv3dcompat = std::make_pair(false, -1.f);
    pv2ddist_val = pv3ddist_val = pv2ddist_err = pv3ddist_err = pv2ddist_sig = pv3ddist_sig = -1;

    if (primary_vertex != 0) {
      pv2dcompat = compatibility(sv, *primary_vertex, false);
      Measurement1D pv2ddist = distcalc_2d.distance(sv, *primary_vertex);
      pv2ddist_val = pv2ddist.value();
      pv2ddist_err = pv2ddist.error();
      pv2ddist_sig = pv2ddist.significance();

      pv3dcompat = compatibility(sv, *primary_vertex, true);
      Measurement1D pv3ddist = distcalc_3d.distance(sv, *primary_vertex);
      pv3ddist_val = pv3ddist.value();
      pv3ddist_err = pv3ddist.error();
      pv3ddist_sig = pv3ddist.significance();
    }

    math::XYZVector pv2sv;
    if (primary_vertex != 0)
      pv2sv = sv.position() - primary_vertex->position();

    for (const math::XYZTLorentzVector& mom : momenta) {
      if (mom.pt() > 0) {
        costhmombs.push_back(costh2(mom, bs2sv));
        if (primary_vertex != 0) {
          costhmompv2d.push_back(costh2(mom, pv2sv));
          costhmompv3d.push_back(costh3(mom, pv2sv));
          missdistpv.push_back(miss_dist(*primary_vertex, sv, mom));
        }
        else {
          costhmompv2d.push_back(-2);
          costhmompv3d.push_back(-2);
          missdistpv.push_back(Measurement1D(1e9,-1));
        }
      }
      else {
        costhmombs.push_back(-2);
        costhmompv2d.push_back(-2);
        costhmompv3d.push_back(-2);
        missdistpv.push_back(Measurement1D(1e9,-1));
      }
    }
  }
}
