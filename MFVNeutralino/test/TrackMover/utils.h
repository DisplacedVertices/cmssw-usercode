#ifndef trackmover_utils_h
#define trackmover_utils_h

#include <cmath>
#include <map>
#include <string>
#include "JMTucker/MFVNeutralino/interface/MovedTracksNtuple.h"

class TH1D;
class TFile;
class TTree;

template <typename T>
T mag(T x, T y, T z=0) {
  return sqrt(x*x + y*y + z*z);
}

struct interval {
  bool success;
  double value;
  double lower;
  double upper;
  double error() const { return (upper - lower)/2; }
  double in(double v) const { return v >= lower && v <= upper; }
};

interval clopper_pearson_binom(const double n_on, const double n_tot,
                               const double alpha=1-0.6827, const bool equal_tailed=true);

struct numden {
  numden() : num(0), den(0) {}
  numden(const char* name, const char* title, int nbins, double xlo, double xhi);
  // no ownership, the TFile owns the histos
  TH1D* num;
  TH1D* den;
};

struct numdens {
  numdens(const char* c);
  void book(int key, const char* name, const char* title, int nbins, double xlo, double xhi);
  numden& operator()(int);

  std::string common;
  std::map<int, numden> m;
};

void root_setup();

struct file_and_tree {
  TFile* f;
  TTree* t;
  mfv::MovedTracksNtuple nt;
  TFile* f_out;

  file_and_tree(const char* in_fn, const char* out_fn, int njets, int nbjets);
  ~file_and_tree();
};

#endif
