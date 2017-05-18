#ifndef JMTucker_MFVNeutralinoFormats_VertexerPairEff_h
#define JMTucker_MFVNeutralinoFormats_VertexerPairEff_h

#include <algorithm>
#include <vector>
#include "DataFormats/VertexReco/interface/Vertex.h"

class VertexerPairEff {
 public:
  enum kind_t { merge=1, erase=2, share=4 };

  VertexerPairEff() : kind_(0) {}

  void set_vertices(const reco::Vertex& v0, const reco::Vertex& v1) {
    point_[0] = v0.position();
    point_[1] = v1.position();
  }

  reco::Vertex::Point point(const int which) const {
    assert(which == 0 || which == 1);
    return point_[which];
  }

  reco::Vertex vertex(const int which) const {
    assert(which == 0 || which == 1);
    return reco::Vertex(point(which), reco::Vertex::Error());
  }

  float d2d() const { return (point(0) - point(1)).rho(); }
  float d3d() const { return (point(0) - point(1)).r();   }

  unsigned kind() const { return kind_; }
  void kind(unsigned k) { kind_ |= k; }

  int ntkmin() const { return int(std::min(tracks_[0].size(), tracks_[1].size())); }
  int ntkmax() const { return int(std::max(tracks_[0].size(), tracks_[1].size())); }

  const std::vector<unsigned char>& tracks(size_t which) const { assert(which == 0 || which == 1); return tracks_[which]; }
  void tracks_push_back(size_t which, unsigned char x) { assert(which == 0 || which == 1); tracks_[which].push_back(x); }

  bool operator==(const VertexerPairEff& o) const {
    return (tracks(0) == o.tracks(0) && tracks(1) == o.tracks(1)) ||
           (tracks(0) == o.tracks(1) && tracks(1) == o.tracks(0));
  }

  bool operator!=(const VertexerPairEff& o) const { return !((*this) == o); }

 private:
  reco::Vertex::Point point_[2];
  unsigned char kind_;
  std::vector<unsigned char> tracks_[2];
};

typedef std::vector<VertexerPairEff> VertexerPairEffs;

#endif
