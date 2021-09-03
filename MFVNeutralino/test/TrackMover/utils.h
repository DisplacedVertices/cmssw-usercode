#ifndef trackmover_utils_h
#define trackmover_utils_h

#include <map>
#include "DVCode/MFVNeutralino/interface/Ntuple.h"
#include "DVCode/Tools/interface/NtupleReader.h"

struct numden {
  numden() : w(1), num(0), den(0) {}

  numden(const char* name, const char* title, int nbins, double xlo, double xhi)
  : w(1),
    num(new TH1D(TString::Format("%s_num", name), title, nbins, xlo, xhi)),
    den(new TH1D(TString::Format("%s_den", name), title, nbins, xlo, xhi))
  {}

  numden(const char* name, const char* title, int nbins, double xlo, double xhi, int nbinsy, double ylo, double yhi)
  : w(1),
    num(new TH2D(TString::Format("%s_num", name), title, nbins, xlo, xhi, nbinsy, ylo, yhi)),
    den(new TH2D(TString::Format("%s_den", name), title, nbins, xlo, xhi, nbinsy, ylo, yhi))
  {}

  void fill(bool usenum, double x) {
    if (usenum) num->Fill(x,w);
    else        den->Fill(x,w);
  }

  void fill(bool usenum, double x, double y) {
    TH2* h = dynamic_cast<TH2*>(usenum ? num : den);
    assert(h != 0);
    h->Fill(x,y,w);
  }

  double w;
  // no ownership, the TFile owns the histos
  TH1* num;
  TH1* den;
};

struct numdens {
  numdens(const char* c) : common(c + std::string("_")) {}
  void book(int key, const char* name, const char* title, int nbins, double xlo, double xhi) { m.insert(std::make_pair(key, numden((common + name).c_str(), title, nbins, xlo, xhi))); }
  void book(int key, const char* name, const char* title, int nbins, double xlo, double xhi, int nbinsy, double ylo, double yhi) { m.insert(std::make_pair(key, numden((common + name).c_str(), title, nbins, xlo, xhi, nbinsy, ylo, yhi))); }
  numden& operator()(int key) { return m[key]; }
  void setw(double w) { for (auto& p : m) p.second.w = w; }
  void fill(int key, bool usenum, double x)           { (*this)(key).fill(usenum, x); }
  void fill(int key, bool usenum, double x, double y) { (*this)(key).fill(usenum, x, y); }
  void den(int key, double x)            { fill(key, false, x); }
  void den(int key, double x, double y ) { fill(key, false, x, y); }
  void num(int key, double x)            { fill(key, true,  x); }
  void num(int key, double x, double y ) { fill(key, true,  x, y); }
  std::string common;
  std::map<int, numden> m;
};

#endif
