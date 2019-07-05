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


struct distrib_calculator {
  // ith value of these are the corresponding stat with the ith value
  // of the n-length input removed, value n is the stat with no input
  // values removed
  const size_t n;
  const bool rmscorr;
  std::vector<double> min; 
  std::vector<double> max;
  std::vector<double> med;
  std::vector<double> sum;
  std::vector<double> avg;
  std::vector<double> rms;
  std::vector<double> mad;

  void calc(std::vector<double> v, double& min, double& max, double& med, double& sum, double& avg, double& rms, double& mad) {
    const size_t m = v.size();
    if (m == 0) return;

    std::sort(v.begin(), v.end());
    min = v.front();
    max = v.back();
 
    if (m % 2 == 0)
      med = (v[m/2] + v[m/2-1])/2;
    else
      med = v[m/2];

    sum = avg = rms = 0;
    std::vector<double> v2(m);
    for (size_t i = 0; i < m; ++i) {
      sum += v[i];
      v2[i] = fabs(v[i] - med);
    }
    avg = sum/m;

    std::sort(v2.begin(), v2.end());
    if (m % 2 == 0)
      mad = (v2[m/2] + v2[m/2-1])/2;
    else
      mad = v2[m/2];

    for (auto a : v)
      rms += pow(a - avg, 2);
    rms = sqrt(rms/(rmscorr ? m-1 : m)); //m-1
  }

  distrib_calculator(const std::vector<double>& v, bool rmscorr_=false) : n(v.size()), rmscorr(rmscorr_) {
    min.assign(n+1, 0);
    max.assign(n+1, 0);
    med.assign(n+1, 0);
    sum.assign(n+1, 0);
    avg.assign(n+1, 0);
    rms.assign(n+1, 0);
    mad.assign(n+1, 0);
    if (n == 0)
      return;

    calc(v, min[n], max[n], med[n], sum[n], avg[n], rms[n], mad[n]);

    for (size_t i = 0; i < n; ++i) {
      std::vector<double> v2(v);
      v2.erase(v2.begin()+i);
      calc(v2, min[i], max[i], med[i], sum[i], avg[i], rms[i], mad[i]);
    }
  }
};

const reco::Track* jetDaughterTrack(const pat::Jet&, size_t idau);

#endif
