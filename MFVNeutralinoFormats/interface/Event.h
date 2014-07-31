#ifndef JMTucker_MFVNeutralinoFormats_interface_Event_h
#define JMTucker_MFVNeutralinoFormats_interface_Event_h

#include <numeric>
#include "TLorentzVector.h"

namespace mfv {
  static const int n_trigger_paths = 5;
  static const int n_clean_paths = 19+1;
}

struct MFVEvent {
  typedef unsigned char uchar;
  typedef unsigned short ushort;
  typedef unsigned int uint;

  MFVEvent() {
    gen_valid = 0;
    gen_partons_in_acc = npfjets = npv = pv_ntracks = 0;
    pfjetpt4 = pfjetpt5 = pfjetpt6 = npu = bsx = bsy = bsz = pvx = pvy = pvz = pvcxx = pvcxy = pvcxz = pvcyy = pvcyz = pvczz = pv_sumpt2 = metx = mety = metsig = metdphimin = 0;
    for (int i = 0; i < 2; ++i) {
      gen_lsp_pt[i] = gen_lsp_eta[i] = gen_lsp_phi[i] = gen_lsp_mass[i] = 0;
      gen_decay_type[i] = 0;
      for (int j = 0; j < 3; ++j)
        gen_lsp_decay[i*3+j] = 0;
    }
    for (int i = 0; i < mfv::n_trigger_paths; ++i)
      pass_trigger[i] = 0;
    for (int i = 0; i < 9; ++i) {
      l1_prescale[i] = 0;
      l1_pass[i] = 0;
    }
    hlt_prescale = 0;
    for (int i = 0; i < mfv::n_clean_paths; ++i)
      pass_clean[i] = 0;
  }

  static TLorentzVector p4(float pt, float eta, float phi, float mass) {
    TLorentzVector v;
    v.SetPtEtaPhiM(pt, eta, phi, mass);
    return v;
  }

  template <typename T>
  static T min(T x, T y) {
    return x < y ? x : y;
  }

  template <typename T>
  static T mag(T x, T y) {
    return sqrt(x*x + y*y);
  }

  template <typename T>
  static T mag(T x, T y, T z) {
    return sqrt(x*x + y*y + z*z);
  }

  bool gen_valid;
  float gen_lsp_pt[2];
  float gen_lsp_eta[2];
  float gen_lsp_phi[2];
  float gen_lsp_mass[2];
  float gen_lsp_decay[2*3];
  uchar gen_decay_type[2];
  uchar gen_partons_in_acc;

  TLorentzVector gen_lsp_p4(int w) const {
    return p4(gen_lsp_pt[w], gen_lsp_eta[w], gen_lsp_phi[w], gen_lsp_mass[w]);
  }

  float minlspdist2d() const {
    return min(mag(gen_lsp_decay[0*3+0] - bsx, gen_lsp_decay[0*3+1] - bsy),
               mag(gen_lsp_decay[1*3+0] - bsx, gen_lsp_decay[1*3+1] - bsy));
  }

  float lspdist2d() const {
    return mag(gen_lsp_decay[0*3+0] - gen_lsp_decay[1*3+0],
               gen_lsp_decay[0*3+1] - gen_lsp_decay[1*3+1]);
  }

  float lspdist3d() const {
    return mag(gen_lsp_decay[0*3+0] - gen_lsp_decay[1*3+0],
               gen_lsp_decay[0*3+1] - gen_lsp_decay[1*3+1],
               gen_lsp_decay[0*3+2] - gen_lsp_decay[1*3+2]);
  }

  bool pass_trigger[mfv::n_trigger_paths];
  ushort l1_prescale[9];
  bool l1_pass[9];
  ushort hlt_prescale;
  bool pass_clean[mfv::n_clean_paths]; // JMTBAD

  uchar npfjets;
  float pfjetpt4;
  float pfjetpt5;
  float pfjetpt6;

  float npu;

  float bsx;
  float bsy;
  float bsz;

  uchar npv;
  float pvx;
  float pvy;
  float pvz;
  float pvcxx;
  float pvcxy;
  float pvcxz;
  float pvcyy;
  float pvcyz;
  float pvczz;
  uchar pv_ntracks;
  float pv_sumpt2;
  float pv_rho() const { return mag(pvx - bsx, pvy - bsy); }

  std::vector<uchar> calojet_id;
  std::vector<float> calojet_pt;
  std::vector<float> calojet_eta;
  std::vector<float> calojet_phi;
  std::vector<float> calojet_energy;

  int ncalojets() const { return int(calojet_pt.size()); }
  float calojetpt4() const { return ncalojets() >= 4 ? calojet_pt[3] : 0.f; }
  float calojet_sum_ht() const { return std::accumulate(calojet_pt.begin(), calojet_pt.end(), 0.f); }

  std::vector<uchar> jet_id;
  std::vector<float> jet_pt;
  std::vector<float> jet_eta;
  std::vector<float> jet_phi;
  std::vector<float> jet_energy;
  std::vector<char> jet_svnvertices;
  std::vector<uchar> jet_svntracks;
  std::vector<float> jet_svsumpt2;
  std::vector<float> jet_svx;
  std::vector<float> jet_svy;
  std::vector<float> jet_svz;
  std::vector<float> jet_svcxx;
  std::vector<float> jet_svcxy;
  std::vector<float> jet_svcxz;
  std::vector<float> jet_svcyy;
  std::vector<float> jet_svcyz;
  std::vector<float> jet_svczz;

  TLorentzVector jet_p4(int w) const {
    TLorentzVector v;
    v.SetPtEtaPhiE(jet_pt[w], jet_eta[w], jet_phi[w], jet_energy[w]);
    return v;
  }
    
  int njets() const { return int(jet_id.size()); }
  float jetpt4() const { return njets() >= 4 ? jet_pt[3] : 0.f; }
  float jetpt5() const { return njets() >= 5 ? jet_pt[4] : 0.f; }
  float jetpt6() const { return njets() >= 6 ? jet_pt[5] : 0.f; }
  float jet_sum_ht() const { return std::accumulate(jet_pt.begin(), jet_pt.end(), 0.f); }

  static uchar encode_jet_id(int pu_level, int bdisc_level) {
    uchar id = 0;
    assert(pu_level >= 0 && pu_level <= 3);
    assert(bdisc_level >= 0 && bdisc_level <= 3);
    id = (bdisc_level << 2) | pu_level;
    return id;
  }

  bool pass_nopu(int w, int level) const {
    return (jet_id[w] & 3) >= level + 1;
  }
  
  int njetsnopu(int level) const {
    int c = 0;
    for (int i = 0, ie = njets(); i < ie; ++i)
      if (pass_nopu(i, level))
        ++c;
    return c;
  }

  bool is_btagged(int w, int level) const {
    return ((jet_id[w] >> 2) & 3) >= level + 1;
  }

  int nbtags(int level) const {
    int c = 0;
    for (int i = 0, ie = njets(); i < ie; ++i)
      if (is_btagged(i, level))
        ++c;
    return c;
  }

  float jet_svpv2ddist(int w) const {
    return mag(jet_svx[w] - pvx,
               jet_svy[w] - pvy);
  }

  float jet_svpv2derr(int w) const {
    const float d = jet_svpv2ddist(w);
    const float dx = (jet_svx[w] - pvx)/d;
    const float dy = (jet_svy[w] - pvy)/d;
    return sqrt((pvcxx + jet_svcxx[w])*dx*dx +
                (pvcyy + jet_svcyy[w])*dy*dy +
                2*(pvcxy + jet_svcxy[w])*dx*dy);
  }

  float jet_svpv2dsig(int w) const {
    return jet_svpv2ddist(w) / jet_svpv2derr(w);
  }

  float metx;
  float mety;
  float metsig;
  float met() const { return mag(metx, mety); }
  float metphi() const { return atan2(mety, metx); }
  float metdphimin;

  std::vector<uchar> lep_id; // bit field: bit 0 (lsb) = mu, 1 = el, bit 1 = loosest (veto) id (always 1 for now), bit 2 = semilep id, bit 3 = dilep id, bit4 = 1 if electron and closestCtfTrack is not null
  std::vector<float> lep_pt;
  std::vector<float> lep_eta;
  std::vector<float> lep_phi;
  std::vector<float> lep_dxy;
  std::vector<float> lep_dz;
  std::vector<float> lep_iso;
  std::vector<float> lep_mva; // only filled for electrons

  TLorentzVector lep_p4(int w) const {
    float mass = (lep_id[w] & 1) ? 0.000511 : 0.106;
    return p4(lep_pt[w], lep_eta[w], lep_phi[w], mass);
  }

  int nlep(int type, int id) const {
    int n = 0;
    for (size_t i = 0, ie = lep_id.size(); i < ie; ++i)
      if ((lep_id[i] & 1) == type &&
          (lep_id[i] & (1 << (id+1))))
        ++n;
    return n;
  }

  int nmu(int which) const { return nlep(0, which); }
  int nel(int which) const { return nlep(1, which); }
  int nlep(int which) const { return nmu(which) + nel(which); }
};

#endif
