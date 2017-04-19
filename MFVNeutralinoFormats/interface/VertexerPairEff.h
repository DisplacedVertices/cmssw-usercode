#ifndef JMTucker_MFVNeutralinoFormats_VertexerPairEff_h
#define JMTucker_MFVNeutralinoFormats_VertexerPairEff_h

#include <vector>

class VertexerPairEff {
 public:
  enum kind_t { pair, merge, erase };

  VertexerPairEff() {}
  VertexerPairEff(float d2d, int ntkmin, int ntkmax)
    : d2d_(d2d),
      ntkmin_(ntkmin),
      ntkmax_(ntkmax),
      kind_(0)
  {}

  float d2d() const { return d2d_; }
  int ntkmin() const { return ntkmin_; }
  int ntkmax() const { return ntkmax_; }
  int kind() const { return kind_; }
  void kind(int k) { kind_ = k; }

 private:
  float d2d_;
  unsigned char ntkmin_;
  unsigned char ntkmax_;
  unsigned char kind_;
};

typedef std::vector<VertexerPairEff> VertexerPairEffs;

#endif
