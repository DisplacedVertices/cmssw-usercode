#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "JMTucker/MFVNeutralino/interface/VertexTools.h"
#include "RecoVertex/VertexTools/interface/VertexDistanceXY.h"
#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"

namespace {
  template <typename T>
  T mag(T x, T y) {
    return sqrt(x*x + y*y);
  }

  template <typename T>
  T mag(T x, T y, T z) {
    return sqrt(x*x + y*y + z*z);
  }
}

namespace mfv {
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

  vertex_tracks_distance::vertex_tracks_distance(const reco::Vertex& sv, const double track_vertex_weight_min) {
    drmin = 1e99;
    drmax = dravg = dravgw = drrms = drrmsw = 0;
    std::vector<double> drs;
    std::vector<double> ws;
    std::vector<double> vws;
    double sumw = 0, sumvw = 0;

    auto trkb = sv.tracks_begin();
    auto trke = sv.tracks_end();
    for (auto trki = trkb; trki != trke; ++trki) {
      if (sv.trackWeight(*trki) < track_vertex_weight_min)
        continue;

      for (auto trkj = trki + 1; trkj != trke; ++trkj) {
        if (sv.trackWeight(*trkj) < track_vertex_weight_min)
          continue;

        double dr = reco::deltaR(**trki, **trkj);
        drs.push_back(dr);

        double w  = 0.5*((*trki)->pt() + (*trkj)->pt());
        double vw = 0.5*(sv.trackWeight(*trki) + sv.trackWeight(*trkj));

        sumw  += w;
        sumvw += vw;
        ws .push_back(w);
        vws.push_back(vw);

        dravg   += dr;
        dravgw  += dr * w;
        dravgvw += dr * vw;

        if (dr < drmin)
          drmin = dr;
        if (dr > drmax)
          drmax = dr;
      }
    }

    dravg   /= drs.size();
    dravgw  /= sumw;
    dravgvw /= sumvw;

    for (int i = 0, ie = int(drs.size()); i < ie; ++i) {
      double dr = drs[i];
      drrms   += pow(dr - dravg,   2);
      drrmsw  += pow(dr - dravgw,  2) * ws [i];
      drrmsvw += pow(dr - dravgvw, 2) * vws[i];
    }

    drrms   = sqrt(drrms  /drs.size());
    drrmsw  = sqrt(drrmsw /sumw);
    drrmsvw = sqrt(drrmsvw/sumvw);
  }
}
