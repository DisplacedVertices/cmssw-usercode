#ifndef JMTucker_Tools_Utilities_h
#define JMTucker_Tools_Utilities_h

#include "TAxis.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TLorentzVector.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"

double cos_angle(const TVector3& v1, const TVector3& v2);
double cos_angle(const TLorentzVector& v1, const TLorentzVector& v2);
double cos_angle_in_rest(const TLorentzVector& rest_frame, const TLorentzVector& v1, const TLorentzVector& v2);
void die_if_not(bool condition, const char* msg, ...);
TLorentzVector lorentz_boost(const TLorentzVector& boost_frame, const TLorentzVector& to_be_boosted);
TLorentzVector make_tlv(const reco::Candidate::LorentzVector& lv);
TLorentzVector make_tlv(const reco::Candidate& c);
TLorentzVector make_tlv(const reco::Candidate* c);
TLorentzVector make_tlv(const reco::GenParticleRef& c);
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

template <typename V>
double coord(const V& v, const int i) {
  if      (i == 0) return v.x();
  else if (i == 1) return v.y();
  else if (i == 2) return v.z();
  else
    throw cms::Exception("coord") << "no such coordinate " << i;
}

typedef unsigned char uchar;
uchar int2uchar(int x);
uchar int2uchar_clamp(int x);
void inc_uchar(uchar& x);

struct weight_fill {
  double weight;
  weight_fill(double w) : weight(w) {}
  void operator()(TH1F* h, double x) const {
    h->Fill(x, weight);
  }
  void operator()(TH2F* h, double x, double y) const {
    h->Fill(x, y, weight);
  }
};

struct distrib_calculator {
  double min, max, sum, wsum, avg, rms, sumw, avgw, rmsw;

  distrib_calculator(const std::vector<double>& v, const std::vector<double>& w)
    : min(1e99), max(-1e99), sum(0), wsum(0), avg(0), rms(0), sumw(0), avgw(0), rmsw(0)
  {
    int n;
    if ((n = int(v.size())) == 0)
      return;

    bool usew = w.size() > 0;
    if (usew && int(w.size()) != n)
      throw cms::Exception("distrib_calculator") << "v.size = " << n << " != w.size = " << w.size();

    for (int i = 0; i < n; ++i) {
      if (v[i] < min) min = v[i];
      if (v[i] > max) max = v[i];
      sum += v[i];
      if (usew) {
        sumw += w[i];
        wsum += v[i] * w[i];
      }
    }

    avg = sum / n;
    if (usew)
      avgw = wsum / sumw;

    for (int i = 0; i < n; ++i) {
      rms += pow(v[i] - avg, 2);
      if (usew)
        rmsw += pow(v[i] - avg, 2) * w[i];
    }

    rms = sqrt(rms/n);
    if (usew)
      rmsw = sqrt(rmsw/sumw);
  }
};

#endif
