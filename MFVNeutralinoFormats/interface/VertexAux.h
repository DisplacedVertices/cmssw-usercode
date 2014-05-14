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
    which = ntracks = nbadtracks = ntracksptgt3 = ntracksptgt5 = ntracksptgt10 = trackminnhits = trackmaxnhits = sumnhitsbehind = maxnhitsbehind = ntrackssharedwpv = ntrackssharedwpvs = npvswtracksshared = bs2dcompatscss = pv2dcompatscss = pv3dcompatscss = 0;
    x = y = z = cxx = cxy = cxz = cyy = cyz = czz = chi2 = ndof = sumpt2 = mintrackpt = maxtrackpt = maxm1trackpt = maxm2trackpt = drmin = drmax = dravg = drrms = dravgw = drrmsw = gen2ddist = gen2derr = gen3ddist = gen3derr = bs2dcompat = bs2ddist = bs2derr = bs3ddist = pv2dcompat = pv2ddist = pv2derr = pv3dcompat = pv3ddist = pv3derr = trackptavg = trackptrms = trackdxymin = trackdxymax = trackdxyavg = trackdxyrms = trackdzmin = trackdzmax = trackdzavg = trackdzrms = trackpterrmin = trackpterrmax = trackpterravg = trackpterrrms = trackdxyerrmin = trackdxyerrmax = trackdxyerravg = trackdxyerrrms = trackdzerrmin = trackdzerrmax = trackdzerravg = trackdzerrrms = trackpairmassmin = trackpairmassmax = trackpairmassavg = trackpairmassrms = tracktripmassmin = tracktripmassmax = tracktripmassavg = tracktripmassrms = trackquadmassmin = trackquadmassmax = trackquadmassavg = trackquadmassrms = jetpairdrmin = jetpairdrmax = jetpairdravg = jetpairdrrms = costhtkmomvtxdispmin = costhtkmomvtxdispmax = costhtkmomvtxdispavg = costhtkmomvtxdisprms = costhjetmomvtxdispmin = costhjetmomvtxdispmax = costhjetmomvtxdispavg = costhjetmomvtxdisprms = 0;
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

  uchar ntrackssharedwpv;
  uchar ntrackssharedwpvs;
  uchar npvswtracksshared;
  uchar pvmosttracksshared;

  float mintrackpt;
  float maxtrackpt;
  float maxm1trackpt;
  float maxm2trackpt;

  float trackptavg;
  float trackptrms;

  float trackdxymin;
  float trackdxymax;
  float trackdxyavg;
  float trackdxyrms;

  float trackdzmin;
  float trackdzmax;
  float trackdzavg;
  float trackdzrms;

  float trackpterrmin;
  float trackpterrmax;
  float trackpterravg;
  float trackpterrrms;

  float trackdxyerrmin;
  float trackdxyerrmax;
  float trackdxyerravg;
  float trackdxyerrrms;

  float trackdzerrmin;
  float trackdzerrmax;
  float trackdzerravg;
  float trackdzerrrms;

  float trackpairdetamin;
  float trackpairdetamax;
  float trackpairdetaavg;
  float trackpairdetarms;

  float drmin; // JMTBAD trackpairdrmin
  float drmax;
  float dravg;
  float drrms;
  float dravgw;
  float drrmsw;

  float trackpairmassmin;
  float trackpairmassmax;
  float trackpairmassavg;
  float trackpairmassrms;

  float tracktripmassmin;
  float tracktripmassmax;
  float tracktripmassavg;
  float tracktripmassrms;

  float trackquadmassmin;
  float trackquadmassmax;
  float trackquadmassavg;
  float trackquadmassrms;

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
    const size_t n = ntracks;
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

  int ntracks_() const {
    return int(track_w.size());
  }

  int nbadtracks_(float thr=0.5) const {
    int c = 0;
    for (size_t i = 0, ie = ntracks_(); i < ie; ++i)
      if (track_pt_err[i] > thr)
        ++c;
    return c;
  }

  int ntracksptgt_(float thr) const {
    int c = 0;
    for (size_t i = 0, ie = ntracks_(); i < ie; ++i)
      if (track_pt(i) > thr)
        ++c;
    return c;
  }

  int trackminnhits_() const {
    int m = 255, m2;
    for (size_t i = 0, ie = ntracks_(); i < ie; ++i)
      if ((m2 = track_nhits(i)) < m)
        m = m2;
    return m;
  }

  int trackmaxnhits_() const {
    int m = 0, m2;
    for (size_t i = 0, ie = ntracks_(); i < ie; ++i)
      if ((m2 = track_nhits(i)) > m)
        m = m2;
    return m;
  }

  float sumpt2_() const {
    float sum = 0;
    for (size_t i = 0, ie = ntracks_(); i < ie; ++i)
      sum += pow(track_pt(i), 2);
    return sum;
  }

  int sumnhitsbehind_() const {
    int c = 0;
    for (size_t i = 0, ie = ntracks_(); i < ie; ++i)
      c += track_nhitsbehind(i);
    return c;
  }

  int maxnhitsbehind_() const {
    int m = 0, m2;
    for (size_t i = 0, ie = ntracks_(); i < ie; ++i)
      if ((m2 = track_nhitsbehind(i)) > m)
        m = m2;
    return m;
  }

  int ntrackssharedwpv_() const {
    int c = 0;
    for (size_t i = 0, ie = ntracks_(); i < ie; ++i)
      if (track_inpv[i] == 0)
        ++c;
    return c;
  }

  int ntrackssharedwpvs_() const {
    int c = 0;
    for (size_t i = 0, ie = ntracks_(); i < ie; ++i)
      if (track_inpv[i] >= 0)
        ++c;
    return c;
  }

  std::map<int,int> pvswtracksshared_() const {
    std::map<int,int> m;
    for (size_t i = 0, ie = ntracks_(); i < ie; ++i)
      ++m[track_inpv[i]];
    return m;
  }

  int npvswtracksshared_() const {
    std::map<int,int> m = pvswtracksshared_();
    int c = int(m.size());
    if (m.find(-1) != m.end())
      --c;
    return c;
  }

  int pvmosttracksshared_() const {
    std::map<int,int> m = pvswtracksshared_();
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


  std::vector<float> track_pts_() const {
    std::vector<float> pts;
    for (size_t i = 0, ie = ntracks_(); i < ie; ++i)
      pts.push_back(track_pt(i));
    return pts;
  }

  float mintrackpt_() const { return _min(track_pts_()); }
  float maxtrackpt_() const { return _max(track_pts_()); }

  float maxmntrackpt_(int n) const {
    int nt = ntracks_();
    if (n > nt - 1)
      return mintrackpt_();
    std::vector<float> pt = track_pts_();
    std::sort(pt.begin(), pt.end());
    return pt[nt-1-n];
  }

  float trackptavg_() const { return _avg(track_pts_()); }
  float trackptrms_() const { return _rms(track_pts_()); }

  float trackdxymin_() const { return _min(track_dxy); }
  float trackdxymax_() const { return _max(track_dxy); }
  float trackdxyavg_() const { return _avg(track_dxy); }
  float trackdxyrms_() const { return _rms(track_dxy); }

  float trackdzmin_() const { return _min(track_dz); }
  float trackdzmax_() const { return _max(track_dz); }
  float trackdzavg_() const { return _avg(track_dz); }
  float trackdzrms_() const { return _rms(track_dz); }

  float trackpterrmin_() const { return _min(track_pt_err); }
  float trackpterrmax_() const { return _max(track_pt_err); }
  float trackpterravg_() const { return _avg(track_pt_err); }
  float trackpterrrms_() const { return _rms(track_pt_err); }

  float trackdxyerrmin_() const { return _min(track_dxy_err); }
  float trackdxyerrmax_() const { return _max(track_dxy_err); }
  float trackdxyerravg_() const { return _avg(track_dxy_err); }
  float trackdxyerrrms_() const { return _rms(track_dxy_err); }

  float trackdzerrmin_() const { return _min(track_dz_err); }
  float trackdzerrmax_() const { return _max(track_dz_err); }
  float trackdzerravg_() const { return _avg(track_dz_err); }
  float trackdzerrrms_() const { return _rms(track_dz_err); }

  std::vector<float> trackpairdetas_() const {
    std::vector<float> v;
    size_t n = ntracks_();
    if (n >= 2)
      for (size_t i = 0, ie = n-1; i < ie; ++i)
        for (size_t j = i+1, je = n; j < je; ++j)
          v.push_back(fabs(track_eta[i] - track_eta[j]));
    return v;
  }

  float trackpairdetamin_() const { return stats(trackpairdetas_()).min; }
  float trackpairdetamax_() const { return stats(trackpairdetas_()).max; }
  float trackpairdetaavg_() const { return stats(trackpairdetas_()).avg; }
  float trackpairdetarms_() const { return stats(trackpairdetas_()).rms; }

  std::vector<float> trackpairdphis_() const {
    std::vector<float> v;
    size_t n = ntracks_();
    if (n >= 2)
      for (size_t i = 0, ie = n-1; i < ie; ++i)
        for (size_t j = i+1, je = n; j < je; ++j)
          v.push_back(reco::deltaPhi(track_phi[i], track_phi[j]));
    return v;
  }

  float trackpairdphimin_() const { return stats(trackpairdphis_()).min; }
  float trackpairdphimax_() const { return stats(trackpairdphis_()).max; }
  float trackpairdphiavg_() const { return stats(trackpairdphis_()).avg; }
  float trackpairdphirms_() const { return stats(trackpairdphis_()).rms; }

  std::vector<float> trackpairdrs_() const {
    std::vector<float> v;
    size_t n = ntracks_();
    if (n >= 2)
      for (size_t i = 0, ie = n-1; i < ie; ++i)
        for (size_t j = i+1, je = n; j < je; ++j)
          v.push_back(reco::deltaR(track_eta[i], track_phi[i],
                                   track_eta[j], track_phi[j]));
    return v;
  }

  float trackpairdrmin_() const { return stats(trackpairdrs_()).min; }
  float trackpairdrmax_() const { return stats(trackpairdrs_()).max; }
  float trackpairdravg_() const { return stats(trackpairdrs_()).avg; }
  float trackpairdrrms_() const { return stats(trackpairdrs_()).rms; }

  float drmin_() const { return trackpairdrmin_(); }
  float drmax_() const { return trackpairdrmax_(); }
  float dravg_() const { return trackpairdravg_(); }
  float drrms_() const { return trackpairdrrms_(); }

  std::vector<float> trackpairmasses_(float mass=0) const {
    std::vector<float> v;
    size_t n = ntracks_();
    if (n >= 2)
      for (size_t i = 0, ie = n-1; i < ie; ++i)
        for (size_t j = i+1, je = n; j < je; ++j)
          v.push_back((track_p4(i, mass) + track_p4(j, mass)).M());
    return v;
  }

  float trackpairmassmin_() const { return stats(trackpairmasses_()).min; }
  float trackpairmassmax_() const { return stats(trackpairmasses_()).max; }
  float trackpairmassavg_() const { return stats(trackpairmasses_()).avg; }
  float trackpairmassrms_() const { return stats(trackpairmasses_()).rms; }

  std::vector<float> tracktripmasses_(float mass=0) const {
    std::vector<float> v;
    size_t n = ntracks_();
    if (n >= 3)
      for (size_t i = 0, ie = n-2; i < ie; ++i)
        for (size_t j = i+1, je = n-1; j < je; ++j)
          for (size_t k = j+1, ke = n; k < ke; ++k)
            v.push_back((track_p4(i, mass) + track_p4(j, mass) + track_p4(k, mass)).M());
    return v;
  }

  float tracktripmassmin_() const { return stats(tracktripmasses_()).min; }
  float tracktripmassmax_() const { return stats(tracktripmasses_()).max; }
  float tracktripmassavg_() const { return stats(tracktripmasses_()).avg; }
  float tracktripmassrms_() const { return stats(tracktripmasses_()).rms; }

  std::vector<float> trackquadmasses_(float mass=0) const {
    std::vector<float> v;
    size_t n = ntracks_();
    if (n >= 4)
      for (size_t i = 0, ie = n-3; i < ie; ++i)
        for (size_t j = i+1, je = n-2; j < je; ++j)
          for (size_t k = j+1, ke = n-1; k < ke; ++k)
            for (size_t l = k+1, le = n; l < le; ++l)
              v.push_back((track_p4(i, mass) + track_p4(j, mass) + track_p4(k, mass) + track_p4(l, mass)).M());
    return v;
  }

  float trackquadmassmin_() const { return stats(trackquadmasses_()).min; }
  float trackquadmassmax_() const { return stats(trackquadmasses_()).max; }
  float trackquadmassavg_() const { return stats(trackquadmasses_()).avg; }
  float trackquadmassrms_() const { return stats(trackquadmasses_()).rms; }
};

typedef std::vector<MFVVertexAux> MFVVertexAuxCollection;

#endif
