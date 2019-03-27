#ifndef trackmover_utils_h
#define trackmover_utils_h

#include <map>
#include <string>
#include "TH2.h"
#include "TRandom3.h"
#include "JMTucker/MFVNeutralino/interface/Ntuple.h"
#include "JMTucker/Tools/interface/NtupleReader.h"
#include "JMTucker/Tools/interface/Prob.h"
#include "JMTucker/Tools/interface/ROOTTools.h"

struct numden {
  numden() : num(0), den(0) {}
  numden(const char* name, const char* title, int nbins, double xlo, double xhi)
  : num(new TH1D(TString::Format("%s_num", name), title, nbins, xlo, xhi)),
    den(new TH1D(TString::Format("%s_den", name), title, nbins, xlo, xhi))
  {}
  numden(const char* name, const char* title, int nbins, double xlo, double xhi, int nbinsy, double ylo, double yhi)
  : num(new TH2D(TString::Format("%s_num", name), title, nbins, xlo, xhi, nbinsy, ylo, yhi)),
    den(new TH2D(TString::Format("%s_den", name), title, nbins, xlo, xhi, nbinsy, ylo, yhi))
  {}
  // no ownership, the TFile owns the histos
  TH1* num;
  TH1* den;
};

struct numdens {
  numdens(const char* c) : common(c + std::string("_")) {}
  void book(int key, const char* name, const char* title, int nbins, double xlo, double xhi) { m.insert(std::make_pair(key, numden((common + name).c_str(), title, nbins, xlo, xhi))); }
  void book(int key, const char* name, const char* title, int nbins, double xlo, double xhi, int nbinsy, double ylo, double yhi) { m.insert(std::make_pair(key, numden((common + name).c_str(), title, nbins, xlo, xhi, nbinsy, ylo, yhi))); }
  numden& operator()(int k) { return m[k]; }

  std::string common;
  std::map<int, numden> m;
};

#endif
