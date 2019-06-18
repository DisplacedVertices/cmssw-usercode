#include "JMTucker/MFVNeutralino/interface/VertexTrackClusters.h"

namespace {
  template <typename T>
  T mag(T x, T y, T z, T t) {
    return sqrt(x*x + y*y + z*z + t*t);
  }
}

namespace mfv {
  track_clusters::track_clusters(const MFVVertexAux& v,
                                 double R_,
                                 fastjet::JetAlgorithm algo_,
                                 fastjet::RecombinationScheme recomb_scheme_,
                                 double track_mass_)
    : R(R_),
      algo(algo_),
      recomb_scheme(recomb_scheme_),
      track_mass(track_mass_)
  {
    std::vector<fastjet::PseudoJet> particles;
    for (size_t i = 0, ie = v.ntracks(); i < ie; ++i) {
      particles.push_back(fastjet::PseudoJet(v.track_px[i],
                                             v.track_py[i],
                                             v.track_pz[i],
                                             mag(v.track_px[i],
                                                 v.track_py[i],
                                                 v.track_pz[i],
                                                 track_mass)));
      particles.back().set_user_index(i);
    }

    fastjet::ClusterSequence cs(particles, fastjet::JetDefinition(algo, R, recomb_scheme));
    std::vector<fastjet::PseudoJet> cs_clusters = fastjet::sorted_by_pt(cs.inclusive_jets());

    // have to repack because can't keep the fastjet PseudoJets around
    // without the ClusterSequence, and it doesn't seem to work to
    // pass the latter back too...
    const size_t nc = cs_clusters.size();
    clusters.resize(nc);
    for (size_t i = 0; i < nc; ++i) {
      const fastjet::PseudoJet& c = cs_clusters[i];
      clusters[i].p4.SetPtEtaPhiM(c.pt(), c.eta(), c.phi_std(), c.m());
      for (const fastjet::PseudoJet& d : c.constituents())
        clusters[i].tracks.push_back(d.user_index());
    }
  }

  size_t track_clusters::nsingle() const {
    return std::count_if(clusters.begin(), clusters.end(), [](const track_cluster& c) { return c.size() == 1; });
  }

  size_t track_clusters::ndouble() const {
    return std::count_if(clusters.begin(), clusters.end(), [](const track_cluster& c) { return c.size() == 2; });
  }

  double track_clusters::avgnconst() const {
    return std::accumulate(clusters.begin(), clusters.end(), 0., [](const double& sum, const track_cluster& c) { return sum + c.size(); }) / clusters.size();
  }
}
