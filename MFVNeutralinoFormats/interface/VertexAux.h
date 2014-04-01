#ifndef JMTucker_MFVNeutralinoFormats_interface_VertexAux_h
#define JMTucker_MFVNeutralinoFormats_interface_VertexAux_h

#include <numeric>
#include <vector>
#include "Math/SMatrix.h"
#include "Math/SVector.h"
#include "TLorentzVector.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "JMTucker/MFVNeutralinoFormats/interface/JetVertexAssociation.h"

struct MFVVertexAux {
  typedef unsigned char uchar;
  typedef unsigned short ushort;
  typedef unsigned int uint;
  typedef ROOT::Math::SVector<double,2> vec2;
  typedef ROOT::Math::SMatrix<double,2,2,ROOT::Math::MatRepSym<double,2> > symmat2;
  typedef ROOT::Math::SVector<double,3> vec3;
  typedef ROOT::Math::SMatrix<double,3,3,ROOT::Math::MatRepSym<double,3> > symmat3;
  typedef ROOT::Math::SVector<double,6> vec6;

  MFVVertexAux() {
    which = 0;
    x = y = z = cxx = cxy = cxz = cyy = cyz = czz = chi2 = ndof = 0;
    bs_x = bs_y = bs_z = bs_cxx = bs_cxy = bs_cxz = bs_cyy = bs_cyz = bs_czz = 0;
    pv_x = pv_y = pv_z = pv_cxx = pv_cxy = pv_cxz = pv_cyy = pv_cyz = pv_czz = 0;
    for (int i = 0; i < mfv::NMomenta; ++i)
      missdistpv[i] = missdistpverr[i] = 0;
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

  vec3 pos() const { return vec3(x,y,z); }
  symmat3 cov() const { return symmat3(vec6(cxx, cxy, cxz, cyy, cyz, czz)); }

  float chi2;
  float ndof;

  std::vector<uchar> track_w;
  static uchar make_track_weight(float weight) { return uchar(weight*255); }
  float track_weight(int i) const { return float(track_w[i])/255.f; }
  std::vector<bool> track_chg;
  static bool make_track_q(int q) { return q == 1; }
  int track_q(int i) const { return track_chg[i] ? 1 : -1; }
  std::vector<float> track_pt;
  std::vector<float> track_eta;
  std::vector<float> track_phi;
  std::vector<float> track_dxy;
  std::vector<float> track_dz;
  std::vector<float> track_pt_err; // relative to pt, rest are absolute values
  std::vector<float> track_dxy_err;
  std::vector<float> track_dz_err;
  std::vector<float> track_chi2dof;
  std::vector<ushort> track_hitpattern;
  static ushort make_track_hitpattern(int npx, int nst, int nbehind) {
    if (npx > 7) npx = 7;
    if (nst > 31) nst = 31;
    if (nbehind > 15) nbehind = 15;
    return (nbehind << 8) | (nst << 3) | npx;
  }
  int track_npxhits(int i) const { return track_hitpattern[i] & 0x7; }
  int track_nsthits(int i) const { return (track_hitpattern[i] >> 3) & 0x1F; }
  int track_nhitsbehind(int i) const { return (track_hitpattern[i] >> 8) & 0xF; }
  int track_nhits(int i) const { return track_npxhits(i) + track_nsthits(i); }
  std::vector<bool> track_injet;

  void insert_track() {
    track_w.push_back(0);
    track_chg.push_back(0);
    track_pt.push_back(0);
    track_eta.push_back(0);
    track_phi.push_back(0);
    track_dxy.push_back(0);
    track_dz.push_back(0);
    track_pt_err.push_back(0);
    track_dxy_err.push_back(0);
    track_dz_err.push_back(0);
    track_chi2dof.push_back(0);
    track_hitpattern.push_back(0);
    track_injet.push_back(0);
  }

  bool tracks_ok() const {
    const size_t n = ntracks();
    return 
      n == track_w.size() &&
      n == track_chg.size() &&
      n == track_eta.size() &&
      n == track_phi.size() &&
      n == track_dxy.size() &&
      n == track_dz.size() &&
      n == track_pt_err.size() &&
      n == track_dxy_err.size() &&
      n == track_dz_err.size() &&
      n == track_chi2dof.size() &&
      n == track_hitpattern.size() &&
      n == track_injet.size();
  }

  int ntracks() const { return int(track_pt.size()); }

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
      if (track_pt[i] > thr)
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
      sum += track_pt[i]*track_pt[i];
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

  static float _min(const std::vector<float>& v) { return v.size() ? *std::min_element(v.begin(), v.end()) : 1e99; }
  static float _max(const std::vector<float>& v) { return v.size() ? *std::max_element(v.begin(), v.end()) : -1e99; }
  static float _avg(const std::vector<float>& v) { return v.size() ? std::accumulate(v.begin(), v.end(), 0) / v.size() : 0; }
  static float _rms(std::vector<float> v) {
    if (v.size() == 0) return 0;
    float avg = _avg(v);
    for (size_t i = 0, ie = v.size(); i < ie; ++i)
      v[i] = pow(v[i] - avg, 2);
    return sqrt(std::accumulate(v.begin(), v.end(), 0))/v.size();
  }

  float mintrackpt() const { return _min(track_pt); }
  float maxtrackpt() const { return _max(track_pt); }

  float maxmntrackpt(int n) const {
    int nt = ntracks();
    if (n > nt - 1)
      return mintrackpt();
    std::vector<float> pt = track_pt;
    std::sort(pt.begin(), pt.end());
    return pt[nt-1-n];
  }

  float trackptavg() const { return _avg(track_pt); }
  float trackptrms() const { return _rms(track_pt); }

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

  struct stats {
    float min, max, avg, rms;
    stats(const std::vector<float>& v) : min(_min(v)), max(_max(v)), avg(_avg(v)), rms(_rms(v)) {}
  };

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
  
  std::vector<float> jet_pt;
  std::vector<float> jet_eta;
  std::vector<float> jet_phi;
  std::vector<float> jet_energy;
  bool jets_ok() const {
    const size_t n = njets();
    return n == jet_eta.size() && n == jet_phi.size() && n == jet_energy.size();
  }

  int njets(int w=0) const { assert(w == 0); return int(jet_pt.size()); }

  std::vector<float> jetpairdetas() const {
    std::vector<float> v;
    size_t n = njets();
    if (n >= 2)
      for (size_t i = 0, ie = n-1; i < ie; ++i)
        for (size_t j = i+1, je = n; j < je; ++j)
          v.push_back(fabs(jet_eta[i] - jet_eta[j]));
    return v;
  }

  float jetpairdetamin() const { return stats(jetpairdetas()).min; }
  float jetpairdetamax() const { return stats(jetpairdetas()).max; }
  float jetpairdetaavg() const { return stats(jetpairdetas()).avg; }
  float jetpairdetarms() const { return stats(jetpairdetas()).rms; }

  std::vector<float> jetpairdphis() const {
    std::vector<float> v;
    size_t n = njets();
    if (n >= 2)
      for (size_t i = 0, ie = n-1; i < ie; ++i)
        for (size_t j = i+1, je = n; j < je; ++j)
          v.push_back(reco::deltaPhi(jet_phi[i], jet_phi[j]));
    return v;
  }

  float jetpairdphimin() const { return stats(jetpairdphis()).min; }
  float jetpairdphimax() const { return stats(jetpairdphis()).max; }
  float jetpairdphiavg() const { return stats(jetpairdphis()).avg; }
  float jetpairdphirms() const { return stats(jetpairdphis()).rms; }

  std::vector<float> jetpairdrs() const {
    std::vector<float> v;
    size_t n = njets();
    if (n >= 2)
      for (size_t i = 0, ie = n-1; i < ie; ++i)
        for (size_t j = i+1, je = n; j < je; ++j)
          v.push_back(reco::deltaR(jet_eta[i], jet_phi[i],
                                   jet_eta[j], jet_phi[j]));
    return v;
  }

  float jetpairdrmin() const { return stats(jetpairdrs()).min; }
  float jetpairdrmax() const { return stats(jetpairdrs()).max; }
  float jetpairdravg() const { return stats(jetpairdrs()).avg; }
  float jetpairdrrms() const { return stats(jetpairdrs()).rms; }

  TLorentzVector track_p4(int i, float mass=0) const {
    TLorentzVector v;
    v.SetPtEtaPhiM(track_pt[i], track_eta[i], track_phi[i], mass);
    return v;
  }

  TLorentzVector jet_p4(int i) const {
    TLorentzVector v;
    v.SetPtEtaPhiE(jet_pt[i], jet_eta[i], jet_phi[i], jet_energy[i]);
    return v;
  }

  TLorentzVector p4(int w=0, float track_mass=0) const {
    TLorentzVector v;

    if (w != mfv::PJetsByNtracks)
      for (size_t i = 0, ie = ntracks(); i < ie; ++i) {
        if (w == mfv::PTracksPlusJetsByNtracks && track_injet[i])
          continue;
        v += track_p4(i, track_mass);
      }
    
    if (w != mfv::PTracksOnly)
      for (size_t i = 0, ie = njets(); i < ie; ++i)
        v+= jet_p4(i);

    return v;
  }

  float pt  (int w=0) const { return p4(w).Pt();  }
  float eta (int w=0) const { return pt(w) > 0 ? p4(w).Eta() : 0; }
  float phi (int w=0) const { return p4(w).Phi(); }
  float mass(int w=0) const { return p4(w).M();   }


  // The BS and PV info is event-level but we duplicate it here for
  // ease of use. (It also might save 13*4 bytes/aux to recalc related
  // stuff rather than save.)

  float bs_x;
  float bs_y;
  float bs_z;

  float bs_cxx;
  float bs_cxy;
  float bs_cxz;
  float bs_cyy;
  float bs_cyz;
  float bs_czz;

  vec3 bs_pos() const { return vec3(bs_x, bs_y, bs_z); }
  symmat3 bs_cov() const { return symmat3(vec6(bs_cxx, bs_cxy, bs_cxz, bs_cyy, bs_cyz, bs_czz)); }

  float pv_x;
  float pv_y;
  float pv_z;

  float pv_cxx;
  float pv_cxy;
  float pv_cxz;
  float pv_cyy;
  float pv_cyz;
  float pv_czz;

  vec3 pv_pos() const { return vec3(pv_x, pv_y, pv_z); }
  symmat3 pv_cov() const { return symmat3(vec6(pv_cxx, pv_cxy, pv_cxz, pv_cyy, pv_cyz, pv_czz)); }


  static float _sig(float val, float err) { return err <= 0 ? 0 : val/err; }
  static float _mag(float x, float y) { return sqrt(x*x + y*y); }
  static float _mag(float x, float y, float z) { return sqrt(x*x + y*y + z*z); }

  static std::pair<bool, float> _compat2(const vec3& a, const symmat3& ca, const vec3& b, const symmat3& cb) {
    symmat2 err;
    err[0][0] = ca[0][0] + cb[0][0];
    err[0][1] = ca[0][1] + cb[0][1];
    err[1][1] = ca[1][1] + cb[1][1];
    vec2 d;
    d[0] = b[0] - a[0];
    d[1] = b[1] - a[1];
    if (err == symmat2() || !err.Invert())
      return std::make_pair(false, FLT_MAX);
    return std::make_pair(true, ROOT::Math::Similarity(err, d));
  }
 
  static std::pair<bool, float> _compat3(const vec3& a, const symmat3& ca, const vec3& b, const symmat3& cb) {
    symmat3 err = ca + cb;
    if (err == symmat3() || !err.InvertChol())
      return std::make_pair(false, FLT_MAX);
    return std::make_pair(true, ROOT::Math::Similarity(err, b - a));
  }

 static std::pair<float, float> _dist(const vec3& a, const symmat3& ca, const vec3& b, const symmat3& cb, bool twod=true) {
    vec3 d = a - b;
    if (twod) d[2] = 0;
    float dist = _mag(d[0], d[1], d[2]);
    double err = 0;
    if (dist > 0) err = sqrt(ROOT::Math::Similarity(ca + cb, d))/dist;
    return std::make_pair(dist, err);
  }

  // JMTBAD finish these too
  float gen2ddist;
  float gen2derr;
  float gen2dsig() const { return _sig(gen2ddist, gen2derr); }

  float gen3ddist;
  float gen3derr;
  float gen3dsig() const { return _sig(gen3ddist, gen3derr); }

  bool bs2dcompatscss() const { return _compat2(pos(), cov(), bs_pos(), bs_cov()).first; }
  float bs2dcompat() const { return _compat2(pos(), cov(), bs_pos(), bs_cov()).second; }
  float bs2ddist() const { return _mag(x - bs_x, y - bs_y); }
  float bs2derr() const { return _dist(pos(), cov(), bs_pos(), bs_cov()).second; }
  float bs2dsig() const { std::pair<float, float> d = _dist(pos(), cov(), bs_pos(), bs_cov()); return _sig(d.first, d.second); }

  bool pv2dcompatscss() const { return _compat2(pos(), cov(), pv_pos(), pv_cov()).first; }
  float pv2dcompat() const { return _compat2(pos(), cov(), pv_pos(), pv_cov()).second; }
  float pv2ddist() const { return _mag(x - pv_x, y - pv_y); }
  float pv2derr() const { return _dist(pos(), cov(), pv_pos(), pv_cov()).second; }
  float pv2dsig() const { std::pair<float, float> d = _dist(pos(), cov(), pv_pos(), pv_cov()); return _sig(d.first, d.second); }

  bool pv3dcompatscss() const { return _compat3(pos(), cov(), pv_pos(), pv_cov()).first; }
  float pv3dcompat() const { return _compat3(pos(), cov(), pv_pos(), pv_cov()).second; }
  float pv3ddist() const { return _mag(x - pv_x, y - pv_y, z - pv_z); }
  float pv3derr() const { return _dist(pos(), cov(), pv_pos(), pv_cov(), false).second; }
  float pv3dsig() const { std::pair<float, float> d = _dist(pos(), cov(), pv_pos(), pv_cov(), false); return _sig(d.first, d.second); }

  float pvdz() const { return fabs(z - pv_z); }
  float pvdzerr() const { return _mag(czz, pv_czz); } // JMTBAD
  float pvdzsig() const { return _sig(pvdz(), pvdzerr()); }

  // JMTBAD finish up
  float costhtkmomvtxdispmin;
  float costhtkmomvtxdispmax;
  float costhtkmomvtxdispavg;
  float costhtkmomvtxdisprms;

  float costhjetmomvtxdispmin;
  float costhjetmomvtxdispmax;
  float costhjetmomvtxdispavg;
  float costhjetmomvtxdisprms;

  float costhmombs  [mfv::NMomenta];
  float costhmompv2d[mfv::NMomenta];
  float costhmompv3d[mfv::NMomenta];

  float missdistpv   [mfv::NMomenta];
  float missdistpverr[mfv::NMomenta];
  float missdistpvsig(int w) const { return _sig(missdistpv[w], missdistpverr[w]); }
};

typedef std::vector<MFVVertexAux> MFVVertexAuxCollection;

#endif
