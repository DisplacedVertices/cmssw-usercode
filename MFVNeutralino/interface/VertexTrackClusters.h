#ifndef JMTucker_MFVNeutralino_VertexTrackClusters_h
#define JMTucker_MFVNeutralino_VertexTrackClusters_h

#include "TLorentzVector.h"
#include "fastjet/ClusterSequence.hh"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"

namespace mfv {
  struct track_cluster {
    TLorentzVector p4;
    std::vector<size_t> tracks;
    size_t size() const { return tracks.size(); }
  };

  struct track_clusters {
    track_clusters(const MFVVertexAux& v,
                   double R_ = 0.4,
                   fastjet::JetAlgorithm algo_ = fastjet::antikt_algorithm,
                   fastjet::RecombinationScheme recomb_scheme_ = fastjet::E_scheme,
                   double track_mass_ = 0.14);

    const double R;
    const fastjet::JetAlgorithm algo;
    const fastjet::RecombinationScheme recomb_scheme;
    const double track_mass;

    std::vector<track_cluster> clusters;
    std::vector<track_cluster>::iterator begin() { return clusters.begin(); }
    std::vector<track_cluster>::iterator end() { return clusters.end(); }
    std::vector<track_cluster>::const_iterator begin() const { return clusters.begin(); }
    std::vector<track_cluster>::const_iterator end() const { return clusters.end(); }

    size_t size() const { return clusters.size(); }
    size_t nsingle() const;
    size_t ndouble() const;
    double avgnconst() const;
  };
}

#endif
