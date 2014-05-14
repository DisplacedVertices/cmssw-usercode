#ifndef JMTucker_MFVNeutralinoFormats_interface_VertexAux_h
#define JMTucker_MFVNeutralinoFormats_interface_VertexAux_h

#include <vector>
#include "TLorentzVector.h"
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
};

typedef std::vector<MFVVertexAux> MFVVertexAuxCollection;

#endif
