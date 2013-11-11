#ifndef JMTucker_MFVNeutralinoFormats_interface_VertexAux_h
#define JMTucker_MFVNeutralinoFormats_interface_VertexAux_h

#include <algorithm>
#include "TLorentzVector.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "JMTucker/MFVNeutralinoFormats/interface/JetVertexAssociation.h"

struct MFVVertexAux {
  typedef unsigned char uchar;
  typedef unsigned short ushort;
  typedef unsigned int uint;

  uchar which;

  float x;
  float y;
  float z;

  float cxx;
  float cxy;
  float cxz;
  float cyy;
  float cyz;
  float czz;

  float chi2;
  float ndof;

  uchar njets[mfv::NJetsByUse];

  float pt  [mfv::NMomenta];
  float eta [mfv::NMomenta];
  float phi [mfv::NMomenta];
  float mass[mfv::NMomenta];

  TLorentzVector p4(int w=0) const {
    TLorentzVector v;
    v.SetPtEtaPhiM(pt[w], eta[w], phi[w], mass[w]);
    return v;
  }

  uchar ntracks;
  uchar nbadtracks;

  uchar ntracksptgt3;
  uchar ntracksptgt5;
  uchar ntracksptgt10;

  uchar trackminnhits;
  uchar trackmaxnhits;

  float sumpt2;

  uchar sumnhitsbehind;
  uchar maxnhitsbehind;

  float mintrackpt;
  float maxtrackpt;
  float maxm1trackpt;
  float maxm2trackpt;

  float drmin;
  float drmax;
  float dravg;
  float drrms;
  float dravgw;
  float drrmsw;

  float sig(float val, float err) const {
    return err <= 0 ? 0 : val/err;
  }

  float gen2ddist;
  float gen2derr;
  float gen2dsig() const { return sig(gen2ddist, gen2derr); }

  float gen3ddist;
  float gen3derr;
  float gen3dsig() const { return sig(gen3ddist, gen3derr); }

  uchar bs2dcompatscss;
  float bs2dcompat;
  float bs2ddist;
  float bs2derr;
  float bs2dsig() const { return sig(bs2ddist, bs2derr); }

  float bs3ddist;

  uchar pv2dcompatscss;
  float pv2dcompat;
  float pv2ddist;
  float pv2derr;
  float pv2dsig() const { return sig(pv2ddist, pv2derr); }

  uchar pv3dcompatscss;
  float pv3dcompat;
  float pv3ddist;
  float pv3derr;
  float pv3dsig() const { return sig(pv3ddist, pv3derr); }

  float costhmombs  [mfv::NMomenta];
  float costhmompv2d[mfv::NMomenta];
  float costhmompv3d[mfv::NMomenta];

  float missdistpv   [mfv::NMomenta];
  float missdistpverr[mfv::NMomenta];
  float missdistpvsig(int w) const { return sig(missdistpv[w], missdistpverr[w]); }
};

typedef std::vector<MFVVertexAux> MFVVertexAuxCollection;

struct MFVVertexAuxSorter {
  enum sort_by_this { sort_by_mass, sort_by_ntracks, sort_by_ntracks_then_mass };
  sort_by_this sort_by;

  MFVVertexAuxSorter(const std::string& x) {
    if (x == "mass")
      sort_by = sort_by_mass;
    else if (x == "ntracks")
      sort_by = sort_by_ntracks;
    else if (x == "ntracks_then_mass")
      sort_by = sort_by_ntracks_then_mass;
    else
      throw cms::Exception("MFVVertexTools") << "invalid sort_by";
  }

  static bool by_mass(const MFVVertexAux& a, const MFVVertexAux& b) {
    return a.mass > b.mass;
  }

  static bool by_ntracks(const MFVVertexAux& a, const MFVVertexAux& b) {
    return a.ntracks > b.ntracks;
  }

  static bool by_ntracks_then_mass(const MFVVertexAux& a, const MFVVertexAux& b) {
    if (a.ntracks == b.ntracks)
      return a.mass > b.mass;
    return a.ntracks > b.ntracks;
  }

  void sort(MFVVertexAuxCollection& v) const {
    if (sort_by == sort_by_mass)
      std::sort(v.begin(), v.end(), by_mass);
    else if (sort_by == sort_by_ntracks)
      std::sort(v.begin(), v.end(), by_ntracks);
    else if (sort_by == sort_by_ntracks_then_mass)
      std::sort(v.begin(), v.end(), by_ntracks_then_mass);
  }
};    

#endif
