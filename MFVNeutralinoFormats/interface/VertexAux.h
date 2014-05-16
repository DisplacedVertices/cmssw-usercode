#ifndef JMTucker_MFVNeutralinoFormats_interface_VertexAux_h
#define JMTucker_MFVNeutralinoFormats_interface_VertexAux_h

#include <vector>
#include "TLorentzVector.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "JMTucker/MFVNeutralinoFormats/interface/JetVertexAssociation.h"

struct MFVVertexAux {
  typedef unsigned char uchar;
  typedef unsigned short ushort;
  typedef unsigned int uint;

  MFVVertexAux() {
    which = bs2dcompatscss = pv2dcompatscss = pv3dcompatscss = 0;
    x = y = z = cxx = cxy = cxz = cyy = cyz = czz = chi2 = ndof = gen2ddist = gen2derr = gen3ddist = gen3derr = bs2dcompat = bs2ddist = bs2derr = bs3ddist = pv2dcompat = pv2ddist = pv2derr = pv3dcompat = pv3ddist = pv3derr = jetpairdrmin = jetpairdrmax = jetpairdravg = jetpairdrrms = costhtkmomvtxdispmin = costhtkmomvtxdispmax = costhtkmomvtxdispavg = costhtkmomvtxdisprms = costhjetmomvtxdispmin = costhjetmomvtxdispmax = costhjetmomvtxdispavg = costhjetmomvtxdisprms = 0;
    for (int i = 0; i < mfv::NJetsByUse; ++i)
      njets[i] = 0;
    for (int i = 0; i < mfv::NMomenta; ++i)
      pt[i] = eta[i] = phi[i] = mass[i] = costhmombs[i] = costhmompv2d[i] = costhmompv3d[i] = missdistpv[i] = missdistpverr[i] = 0;
  }

  uchar which;
  std::vector<uchar> which_lep; // electrons have 7th bit set

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

  float jetpairdetamin;
  float jetpairdetamax;
  float jetpairdetaavg;
  float jetpairdetarms;

  float jetpairdrmin;
  float jetpairdrmax;
  float jetpairdravg;
  float jetpairdrrms;

  float costhtkmomvtxdispmin;
  float costhtkmomvtxdispmax;
  float costhtkmomvtxdispavg;
  float costhtkmomvtxdisprms;

  float costhjetmomvtxdispmin;
  float costhjetmomvtxdispmax;
  float costhjetmomvtxdispavg;
  float costhjetmomvtxdisprms;

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

  float pvdz() const { return sqrt(pv3ddist*pv3ddist - pv2ddist*pv2ddist); }
  float pvdzerr() const {
    // JMTBAD
    float z = pvdz();
    if (z == 0)
      return -1;
    return sqrt(pv3ddist*pv3ddist*pv3derr*pv3derr + pv2ddist*pv2ddist*pv2derr*pv2derr)/z;
  }
  float pvdzsig() const { return sig(pvdz(), pvdzerr()); }

  float costhmombs  [mfv::NMomenta];
  float costhmompv2d[mfv::NMomenta];
  float costhmompv3d[mfv::NMomenta];

  float missdistpv   [mfv::NMomenta];
  float missdistpverr[mfv::NMomenta];
  float missdistpvsig(int w) const { return sig(missdistpv[w], missdistpverr[w]); }


  std::vector<uchar> track_w;
  static uchar make_track_weight(float weight) { assert(weight >= 0 && weight <= 1); return uchar(weight*255); }
  float track_weight(int i) const { return float(track_w[i])/255.f; }
  std::vector<float> track_qpt;
  float track_q(int i) const { return track_qpt[i] > 0 ? 1 : -1; }
  float track_pt(int i) const { return fabs(track_qpt[i]); }
  std::vector<float> track_eta;
  std::vector<float> track_phi;
  std::vector<float> track_dxy;
  std::vector<float> track_dz;
  std::vector<float> track_pt_err; // relative to pt, rest are absolute values
  std::vector<float> track_eta_err;
  std::vector<float> track_phi_err;
  std::vector<float> track_dxy_err;
  std::vector<float> track_dz_err;
  std::vector<float> track_chi2dof;
  std::vector<ushort> track_hitpattern;
  static ushort make_track_hitpattern(int npx, int nst, int nbehind, int nlost) {
    assert(npx >= 0 && nst >= 0 && nbehind >= 0 && nlost >= 0);
    if (npx > 7) npx = 7;
    if (nst > 31) nst = 31;
    if (nbehind > 15) nbehind = 7;
    if (nlost > 15) nlost = 15;
    return (nlost << 12) | (nbehind << 8) | (nst << 3) | npx;
  }
  int track_npxhits(int i) const { return track_hitpattern[i] & 0x7; }
  int track_nsthits(int i) const { return (track_hitpattern[i] >> 3) & 0x1F; }
  int track_nhitsbehind(int i) const { return (track_hitpattern[i] >> 8) & 0xF; }
  int track_nhitslost(int i) const { return (track_hitpattern[i] >> 12) & 0xF; }
  int track_nhits(int i) const { return track_npxhits(i) + track_nsthits(i); }
  std::vector<bool> track_injet;
  std::vector<short> track_inpv;

  void insert_track() {
    track_w.push_back(0);
    track_qpt.push_back(0);
    track_eta.push_back(0);
    track_phi.push_back(0);
    track_dxy.push_back(0);
    track_dz.push_back(0);
    track_pt_err.push_back(0);
    track_eta_err.push_back(0);
    track_phi_err.push_back(0);
    track_dxy_err.push_back(0);
    track_dz_err.push_back(0);
    track_chi2dof.push_back(0);
    track_hitpattern.push_back(0);
    track_injet.push_back(0);
    track_inpv.push_back(0);
  }

  bool tracks_ok() const {
    const size_t n = ntracks();
    return
      n == track_w.size() &&
      n == track_qpt.size() &&
      n == track_eta.size() &&
      n == track_phi.size() &&
      n == track_dxy.size() &&
      n == track_dz.size() &&
      n == track_pt_err.size() &&
      n == track_eta_err.size() &&
      n == track_phi_err.size() &&
      n == track_dxy_err.size() &&
      n == track_dz_err.size() &&
      n == track_chi2dof.size() &&
      n == track_hitpattern.size() &&
      n == track_injet.size() &&
      n == track_inpv.size();
  }

  TLorentzVector track_p4(int i, float mass=0) const {
    TLorentzVector v;
    v.SetPtEtaPhiM(track_pt(i), track_eta[i], track_phi[i], mass);
    return v;
  }

  int ntracks() const {
    return int(track_w.size());
  }

  int nbadtracks(float thr=0.5) const {
    int c = 0;
    for (size_t i = 0, ie = ntracks(); i < ie; ++i)
      if (track_pt_err[i] > thr)
        ++c;
    return c;
  }

  int ntracksptgt(float thr) const {
    int c = 0;
    for (size_t i = 0, ie = ntracks(); i < ie; ++i)
      if (track_pt(i) > thr)
        ++c;
    return c;
  }

  int trackminnhits() const {
    int m = 255, m2;
    for (size_t i = 0, ie = ntracks(); i < ie; ++i)
      if ((m2 = track_nhits(i)) < m)
        m = m2;
    return m;
  }

  int trackmaxnhits() const {
    int m = 0, m2;
    for (size_t i = 0, ie = ntracks(); i < ie; ++i)
      if ((m2 = track_nhits(i)) > m)
        m = m2;
    return m;
  }

  float sumpt2() const {
    float sum = 0;
    for (size_t i = 0, ie = ntracks(); i < ie; ++i)
      sum += pow(track_pt(i), 2);
    return sum;
  }

  int sumnhitsbehind() const {
    int c = 0;
    for (size_t i = 0, ie = ntracks(); i < ie; ++i)
      c += track_nhitsbehind(i);
    return c;
  }

  int maxnhitsbehind() const {
    int m = 0, m2;
    for (size_t i = 0, ie = ntracks(); i < ie; ++i)
      if ((m2 = track_nhitsbehind(i)) > m)
        m = m2;
    return m;
  }

  int ntrackssharedwpv() const {
    int c = 0;
    for (size_t i = 0, ie = ntracks(); i < ie; ++i)
      if (track_inpv[i] == 0)
        ++c;
    return c;
  }

  int ntrackssharedwpvs() const {
    int c = 0;
    for (size_t i = 0, ie = ntracks(); i < ie; ++i)
      if (track_inpv[i] >= 0)
        ++c;
    return c;
  }

  std::map<int,int> pvswtracksshared() const {
    std::map<int,int> m;
    for (size_t i = 0, ie = ntracks(); i < ie; ++i)
      ++m[track_inpv[i]];
    return m;
  }

  int npvswtracksshared() const {
    std::map<int,int> m = pvswtracksshared();
    int c = int(m.size());
    if (m.find(-1) != m.end())
      --c;
    return c;
  }

  int pvmosttracksshared() const {
    std::map<int,int> m = pvswtracksshared();
    int mi = -1, mc = 0;
    for (std::map<int,int>::const_iterator it = m.begin(), ite = m.end(); it != ite; ++it)
      if (it->second > mc) {
        mc = it->second;
        mi = it->first;
      }
    return mi;
  }

  static float _min(const std::vector<float>& v) { return v.size() ? *std::min_element(v.begin(), v.end()) :  1e99; }
  static float _max(const std::vector<float>& v) { return v.size() ? *std::max_element(v.begin(), v.end()) : -1e99; }
  static float _avg(const std::vector<float>& v) { return v.size() ? std::accumulate(v.begin(), v.end(), 0.f) / v.size() : 0.f; }
  static float _rms(std::vector<float> v) {
    if (v.size() == 0) return 0.f;
    float avg = _avg(v);
    for (size_t i = 0, ie = v.size(); i < ie; ++i)
      v[i] = pow(v[i] - avg, 2);
    return sqrt(std::accumulate(v.begin(), v.end(), 0.f))/v.size();
  }

  struct stats {
    float min, max, avg, rms;
    stats(const std::vector<float>& v) : min(_min(v)), max(_max(v)), avg(_avg(v)), rms(_rms(v)) {}
  };


  std::vector<float> track_pts() const {
    std::vector<float> pts;
    for (size_t i = 0, ie = ntracks(); i < ie; ++i)
      pts.push_back(track_pt(i));
    return pts;
  }

  float mintrackpt() const { return _min(track_pts()); }
  float maxtrackpt() const { return _max(track_pts()); }

  float maxmntrackpt(int n) const {
    int nt = ntracks();
    if (n > nt - 1)
      return mintrackpt();
    std::vector<float> pt = track_pts();
    std::sort(pt.begin(), pt.end());
    return pt[nt-1-n];
  }

  float trackptavg() const { return _avg(track_pts()); }
  float trackptrms() const { return _rms(track_pts()); }

  float trackdxymin() const { return _min(track_dxy); }
  float trackdxymax() const { return _max(track_dxy); }
  float trackdxyavg() const { return _avg(track_dxy); }
  float trackdxyrms() const { return _rms(track_dxy); }

  float trackdzmin() const { return _min(track_dz); }
  float trackdzmax() const { return _max(track_dz); }
  float trackdzavg() const { return _avg(track_dz); }
  float trackdzrms() const { return _rms(track_dz); }

  float trackpterrmin() const { return _min(track_pt_err); }
  float trackpterrmax() const { return _max(track_pt_err); }
  float trackpterravg() const { return _avg(track_pt_err); }
  float trackpterrrms() const { return _rms(track_pt_err); }

  float trackdxyerrmin() const { return _min(track_dxy_err); }
  float trackdxyerrmax() const { return _max(track_dxy_err); }
  float trackdxyerravg() const { return _avg(track_dxy_err); }
  float trackdxyerrrms() const { return _rms(track_dxy_err); }

  float trackdzerrmin() const { return _min(track_dz_err); }
  float trackdzerrmax() const { return _max(track_dz_err); }
  float trackdzerravg() const { return _avg(track_dz_err); }
  float trackdzerrrms() const { return _rms(track_dz_err); }

  std::vector<float> trackpairdetas() const {
    std::vector<float> v;
    size_t n = ntracks();
    if (n >= 2)
      for (size_t i = 0, ie = n-1; i < ie; ++i)
        for (size_t j = i+1, je = n; j < je; ++j)
          v.push_back(fabs(track_eta[i] - track_eta[j]));
    return v;
  }

  float trackpairdetamin() const { return stats(trackpairdetas()).min; }
  float trackpairdetamax() const { return stats(trackpairdetas()).max; }
  float trackpairdetaavg() const { return stats(trackpairdetas()).avg; }
  float trackpairdetarms() const { return stats(trackpairdetas()).rms; }

  std::vector<float> trackpairdphis() const {
    std::vector<float> v;
    size_t n = ntracks();
    if (n >= 2)
      for (size_t i = 0, ie = n-1; i < ie; ++i)
        for (size_t j = i+1, je = n; j < je; ++j)
          v.push_back(reco::deltaPhi(track_phi[i], track_phi[j]));
    return v;
  }

  float trackpairdphimin() const { return stats(trackpairdphis()).min; }
  float trackpairdphimax() const { return stats(trackpairdphis()).max; }
  float trackpairdphiavg() const { return stats(trackpairdphis()).avg; }
  float trackpairdphirms() const { return stats(trackpairdphis()).rms; }

  std::vector<float> trackpairdrs() const {
    std::vector<float> v;
    size_t n = ntracks();
    if (n >= 2)
      for (size_t i = 0, ie = n-1; i < ie; ++i)
        for (size_t j = i+1, je = n; j < je; ++j)
          v.push_back(reco::deltaR(track_eta[i], track_phi[i],
                                   track_eta[j], track_phi[j]));
    return v;
  }

  float trackpairdrmin() const { return stats(trackpairdrs()).min; }
  float trackpairdrmax() const { return stats(trackpairdrs()).max; }
  float trackpairdravg() const { return stats(trackpairdrs()).avg; }
  float trackpairdrrms() const { return stats(trackpairdrs()).rms; }

  float drmin() const { return trackpairdrmin(); }
  float drmax() const { return trackpairdrmax(); }
  float dravg() const { return trackpairdravg(); }
  float drrms() const { return trackpairdrrms(); }

  std::vector<float> trackpairmasses(float mass=0) const {
    std::vector<float> v;
    size_t n = ntracks();
    if (n >= 2)
      for (size_t i = 0, ie = n-1; i < ie; ++i)
        for (size_t j = i+1, je = n; j < je; ++j)
          v.push_back((track_p4(i, mass) + track_p4(j, mass)).M());
    return v;
  }

  float trackpairmassmin() const { return stats(trackpairmasses()).min; }
  float trackpairmassmax() const { return stats(trackpairmasses()).max; }
  float trackpairmassavg() const { return stats(trackpairmasses()).avg; }
  float trackpairmassrms() const { return stats(trackpairmasses()).rms; }

  std::vector<float> tracktripmasses(float mass=0) const {
    std::vector<float> v;
    size_t n = ntracks();
    if (n >= 3)
      for (size_t i = 0, ie = n-2; i < ie; ++i)
        for (size_t j = i+1, je = n-1; j < je; ++j)
          for (size_t k = j+1, ke = n; k < ke; ++k)
            v.push_back((track_p4(i, mass) + track_p4(j, mass) + track_p4(k, mass)).M());
    return v;
  }

  float tracktripmassmin() const { return stats(tracktripmasses()).min; }
  float tracktripmassmax() const { return stats(tracktripmasses()).max; }
  float tracktripmassavg() const { return stats(tracktripmasses()).avg; }
  float tracktripmassrms() const { return stats(tracktripmasses()).rms; }

  std::vector<float> trackquadmasses(float mass=0) const {
    std::vector<float> v;
    size_t n = ntracks();
    if (n >= 4)
      for (size_t i = 0, ie = n-3; i < ie; ++i)
        for (size_t j = i+1, je = n-2; j < je; ++j)
          for (size_t k = j+1, ke = n-1; k < ke; ++k)
            for (size_t l = k+1, le = n; l < le; ++l)
              v.push_back((track_p4(i, mass) + track_p4(j, mass) + track_p4(k, mass) + track_p4(l, mass)).M());
    return v;
  }

  float trackquadmassmin() const { return stats(trackquadmasses()).min; }
  float trackquadmassmax() const { return stats(trackquadmasses()).max; }
  float trackquadmassavg() const { return stats(trackquadmasses()).avg; }
  float trackquadmassrms() const { return stats(trackquadmasses()).rms; }
};

typedef std::vector<MFVVertexAux> MFVVertexAuxCollection;

#endif
