#ifndef JMTucker_MFVNeutralinoFormats_VertexerPairEff_h
#define JMTucker_MFVNeutralinoFormats_VertexerPairEff_h

#include <algorithm>
#include <vector>

class VertexerPairEff {
 public:
  enum kind_t { merge=1, erase=2, share=4 };

  VertexerPairEff() {}
  VertexerPairEff(float d2d, float d3d, int ntkmin, int ntkmax)
    : d2d_(d2d),
      d3d_(d3d),
      kind_(0)
  {}

  float d2d() const { return d2d_; }
  float d3d() const { return d3d_; }
  void d2d(float x) { d2d_ = x; }
  void d3d(float x) { d3d_ = x; }

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
  float d2d_;
  float d3d_;
  unsigned char kind_;
  std::vector<unsigned char> tracks_[2];
};

typedef std::vector<VertexerPairEff> VertexerPairEffs;

#endif
