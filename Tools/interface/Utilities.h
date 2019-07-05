#ifndef JMTucker_Tools_Utilities_h
#define JMTucker_Tools_Utilities_h

// JMTBAD some/most of this stuff should go over to ROOTTools

#include "TAxis.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TLorentzVector.h"

namespace reco {
  class Candidate;
  class Track;
}

namespace pat {
  class Jet;
}

double cos_angle(const TVector3& v1, const TVector3& v2);
double cos_angle(const TLorentzVector& v1, const TLorentzVector& v2);
double cos_angle_in_rest(const TLorentzVector& rest_frame, const TLorentzVector& v1, const TLorentzVector& v2);
void die_if_not(bool condition, const char* msg, ...);
TLorentzVector lorentz_boost(const TLorentzVector& boost_frame, const TLorentzVector& to_be_boosted);
TLorentzVector make_tlv(const reco::Candidate& c);
TLorentzVector make_tlv(const reco::Candidate* c);
double pt_proj(const TLorentzVector& a, const TLorentzVector& b);
void set_bin_labels(TAxis* xax, const char** labels);
void fill_by_label(TH1F* h, const std::string& label);
void fill_by_label(TH2F* h, const std::string& label_x, const std::string& label_y);

template <typename T>
int sgn(T x) {
  return x >= 0 ? 1 : -1;
}

template <typename T>
T min(T x, T y) {
  return x < y ? x : y;
}

template <typename T>
T mag(T x, T y) {
  return sqrt(x*x + y*y);
}

template <typename T>
T mag(T x, T y, T z) {
  return sqrt(x*x + y*y + z*z);
}

template <typename T, typename T2>
T2 mag(const T& v) {
  return mag<T2>(v.x(), v.y(), v.z());
}

template <typename T>
T signed_mag(T x, T y) {
  T m = mag(x,y);
  if (y < 0) return -m;
  return m;
}

typedef unsigned char uchar;
uchar int2uchar(int x);
uchar int2uchar_clamp(int x);
uchar uint2uchar_clamp(unsigned x);
void inc_uchar(uchar& x);
void inc_uchar_clamp(uchar& x);

const reco::Track* jetDaughterTrack(const pat::Jet&, size_t idau);

#endif
