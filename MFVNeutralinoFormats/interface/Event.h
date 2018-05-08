#ifndef JMTucker_MFVNeutralinoFormats_interface_Event_h
#define JMTucker_MFVNeutralinoFormats_interface_Event_h

#include <cassert>
#include <numeric>
#include "TLorentzVector.h"

namespace mfv {
  // JMTBAD hope you keep these in sync with Event.cc
  static const int n_clean_paths = 7;
  enum {
    b_HLT_PFHT1050, n_hlt_paths,
    b_L1_HTT120er=0, b_L1_HTT160er, b_L1_HTT200er, b_L1_HTT220er, b_L1_HTT240er, b_L1_HTT255er, b_L1_HTT270er, b_L1_HTT280er, b_L1_HTT300er, b_L1_HTT320er, b_L1_HTT340er, b_L1_HTT380er, b_L1_HTT400er, b_L1_HTT450er, b_L1_HTT500er, b_L1_HTT250er_QuadJet_70_55_40_35_er2p5, b_L1_HTT280er_QuadJet_70_55_40_35_er2p5, b_L1_HTT300er_QuadJet_70_55_40_35_er2p5, n_l1_paths
  };

  extern const char* hlt_paths[n_hlt_paths];
  extern const char* l1_paths[n_l1_paths];
  extern const char* clean_paths[n_clean_paths];
}

struct MFVEvent {
  typedef unsigned char uchar;
  typedef unsigned short ushort;
  typedef unsigned int uint;

  static bool test_bit(uint64_t v, size_t i) { return bool((v >> i) & 1); }
  static void set_bit(uint64_t& v, size_t i, bool x) { v ^= (-uint64_t(x) ^ v) & (1ULL << i); }

  MFVEvent() {
    gen_valid = 0;
    npv = pv_ntracks = 0;
    gen_flavor_code = 0;
    gen_weight = gen_weightprod = l1_htt = l1_myhtt = l1_myhttwbug = hlt_ht = hlt_ht4mc = npu = bsx = bsy = bsz = bsdxdz = bsdydz = bswidthx = bswidthy = pvx = pvy = pvz = pvcxx = pvcxy = pvcxz = pvcyy = pvcyz = pvczz = pv_sumpt2 = metx = mety = 0;
    for (int i = 0; i < 2; ++i) {
      gen_lsp_pt[i] = gen_lsp_eta[i] = gen_lsp_phi[i] = gen_lsp_mass[i] = 0;
      gen_decay_type[i] = 0;
      for (int j = 0; j < 3; ++j)
        gen_lsp_decay[i*3+j] = 0;
    }
    for (int i = 0; i < 3; ++i) {
      gen_pv[i] = 0;
    }
    pass_ = 0;
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

  float gen_weight;
  float gen_weightprod;
  uchar gen_flavor_code;
  float gen_pv[3];
  std::vector<TLorentzVector> gen_bquarks;
  std::vector<TLorentzVector> gen_leptons;
  std::vector<TLorentzVector> gen_jets;

  int gen_lepton_id(int which) { // same convention as reco lep_id below, el=1, mu=0
    double mass = gen_leptons[which].M();
    if (fabs(mass - 0.000511) < 1e-4)
      return 1; 
    else if (fabs(mass - 0.1057) < 1e-2)
      return 0;
    else {
      assert(0);
      return 999;
    }
  }

  double gen_jet_ht(double min_jet_pt=0.) const {
    double r(0);
    for (auto j : gen_jets)
      if (j.Pt() > min_jet_pt)
        r += j.Pt();
    return r;
  }

  bool gen_valid; // only refers to the next block, not the weights above
  float gen_lsp_pt[2];
  float gen_lsp_eta[2];
  float gen_lsp_phi[2];
  float gen_lsp_mass[2];
  float gen_lsp_decay[2*3];
  uchar gen_decay_type[2];
  std::vector<TLorentzVector> gen_daughters;
  std::vector<int> gen_daughter_id;

  TLorentzVector gen_lsp_p4(int w) const {
    return p4(gen_lsp_pt[w], gen_lsp_eta[w], gen_lsp_phi[w], gen_lsp_mass[w]);
  }

  TVector3 gen_lsp_flight(int w) const {
    return TVector3(gen_lsp_decay[w*3+0] - gen_pv[0],
                    gen_lsp_decay[w*3+1] - gen_pv[1],
                    gen_lsp_decay[w*3+2] - gen_pv[2]);
  }

  TLorentzVector gen_lsp_p4_vis(int w) const {
    const size_t n = gen_daughters.size();
    assert(n % 2 == 0);
    assert(w == 0 || w == 1);
    TLorentzVector r;
    for (size_t i = n/2 * w; i < n/2*(w+1); ++i) {
      int id = gen_daughter_id[i];
      if (id == 11 || id == 13 || id == 15 || (id >= 1 && id <= 5))
        r += gen_daughters[i];
    }
    return r;
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

  float l1_htt;
  float l1_myhtt;
  float l1_myhttwbug;
  float hlt_ht;
  float hlt_ht4mc;

  uint64_t pass_;
  bool pass_hlt(size_t i)           const { assert(i < mfv::n_hlt_paths);                                                return test_bit(pass_, i   ); }
  void pass_hlt(size_t i, bool x)         { assert(i < mfv::n_hlt_paths);                                                        set_bit(pass_, i, x); }
  bool found_hlt(size_t i)          const { assert(i < mfv::n_hlt_paths);   i += mfv::n_hlt_paths;                       return test_bit(pass_, i   ); }
  void found_hlt(size_t i, bool x)        { assert(i < mfv::n_hlt_paths);   i += mfv::n_hlt_paths;                               set_bit(pass_, i, x); }
  bool pass_l1(size_t i)            const { assert(i < mfv::n_l1_paths);    i += 2*mfv::n_hlt_paths;                     return test_bit(pass_, i   ); }
  void pass_l1(size_t i, bool x)          { assert(i < mfv::n_l1_paths);    i += 2*mfv::n_hlt_paths;                             set_bit(pass_, i, x); }
  bool found_l1(size_t i)           const { assert(i < mfv::n_l1_paths);    i += 2*mfv::n_hlt_paths + mfv::n_l1_paths;   return test_bit(pass_, i   ); }
  void found_l1(size_t i, bool x)         { assert(i < mfv::n_l1_paths);    i += 2*mfv::n_hlt_paths + mfv::n_l1_paths;           set_bit(pass_, i, x); }

  float npu;

  float bsx;
  float bsy;
  float bsz;
  float bsdxdz;
  float bsdydz;
  float bswidthx;
  float bswidthy;

  float bsx_at_z(float z) const { return bsx + bsdxdz * (z - bsz); }
  float bsy_at_z(float z) const { return bsy + bsdydz * (z - bsz); }
  float bs2ddist(float x, float y, float z) const { return mag(x - bsx_at_z(z), y - bsy_at_z(z)); }
  template <typename T> float bs2ddist(const T& t) const { return bs2ddist(t.x, t.y, t.z); }

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
  float pv_rho() const { return mag(pvx - bsx_at_z(pvz), pvy - bsy_at_z(pvz)); }

  std::vector<uchar> jet_id;
  std::vector<float> jet_bdisc; // JMTBAD jet_id currently redundant with this
  std::vector<float> jet_pudisc; // to be removed and put into _id when working points defined
  std::vector<float> jet_pt;
  std::vector<float> jet_raw_pt;
  std::vector<float> jet_eta;
  std::vector<float> jet_phi;
  std::vector<float> jet_energy;

  TLorentzVector jet_p4(int w) const {
    TLorentzVector v;
    v.SetPtEtaPhiE(jet_pt[w], jet_eta[w], jet_phi[w], jet_energy[w]);
    return v;
  }
    
  int njets() const { return int(jet_id.size()); }
  float jetpt4() const { return njets() >= 4 ? jet_pt[3] : 0.f; }
  float jetpt5() const { return njets() >= 5 ? jet_pt[4] : 0.f; }
  float jetpt6() const { return njets() >= 6 ? jet_pt[5] : 0.f; }
  float jet_ht(float min_jet_pt=0.f) const { return std::accumulate(jet_pt.begin(), jet_pt.end(), 0.f,
                                                                    [min_jet_pt](float init, float b) { if (b > min_jet_pt) init += b; return init; }); }

  float jet_ST_sum() const {
    double sum = 0;
    for (size_t ijet = 0; ijet < jet_id.size(); ++ijet) {
      const double px_i = jet_pt[ijet] * cos(jet_phi[ijet]);
      const double py_i = jet_pt[ijet] * sin(jet_phi[ijet]);
      for (size_t jjet = 0; jjet < jet_id.size(); ++jjet) {
        const double px_j = jet_pt[jjet] * cos(jet_phi[jjet]);
        const double py_j = jet_pt[jjet] * sin(jet_phi[jjet]);
        sum += (px_i*px_i * py_j*py_j - px_i*py_i * px_j*py_j) / (jet_pt[ijet] * jet_pt[jjet]);
      }
    }
    return sum;
  }

  float jet_ST() const {
    return 1 - sqrt(1 - 4 * jet_ST_sum() / pow(jet_ht(), 2));
  }

  static uchar encode_jet_id(int pu_level, int bdisc_level, int hadron_flavor) {
    assert(pu_level == 0); assert(pu_level >= 0 && pu_level <= 3);
    assert(hadron_flavor == 0 || hadron_flavor == 4 || hadron_flavor == 5);
    assert(bdisc_level >= 0 && bdisc_level <= 3);

    if      (hadron_flavor == 4) hadron_flavor = 1;
    else if (hadron_flavor == 5) hadron_flavor = 2;

    return (hadron_flavor << 4) | (bdisc_level << 2) | pu_level;
  }

  bool pass_nopu(int w, int level) const {
    return false;
    return (jet_id[w] & 3) >= level + 1;
  }
  
  int njetsnopu(int level) const {
    return -1;
    int c = 0;
    for (int i = 0, ie = njets(); i < ie; ++i)
      if (pass_nopu(i, level))
        ++c;
    return c;
  }

  int jet_hadron_flavor(int w) const {
    const int f = (jet_id[w] >> 4) & 3;
    if (f == 1) return 4;
    if (f == 2) return 5;
    return 0;
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

  float metx;
  float mety;
  float met() const { return mag(metx, mety); }
  float metphi() const { return atan2(mety, metx); }

  enum { lep_mu, lep_el };
  enum { mu_veto = 1, mu_semilep = 2, mu_dilep = 4, max_mu_sel = 8 };
  enum { el_veto = 1, el_semilep = 2, el_dilep = 4, el_ctf = 8, max_el_sel = 16 };
  std::vector<uchar> lep_id; // bit field: bit 7 (msb): 0 = mu, 1 = el, remaining seven bits are el or mu id in order from lsb to msb according to the enums above
  std::vector<float> lep_pt;
  std::vector<float> lep_eta;
  std::vector<float> lep_phi;
  std::vector<float> lep_dxy;
  std::vector<float> lep_dxybs;
  std::vector<float> lep_dz;
  std::vector<float> lep_iso;

  size_t nlep() const { return lep_id.size(); }

  static uchar encode_mu_id(uchar sel) {
    assert(sel < max_mu_sel);
    return sel;
  }

  static uchar encode_el_id(uchar sel) {
    assert(sel < max_el_sel);
    return sel | 0x80;
  }

  bool is_electron(size_t w) const { return lep_id[w] & 0x80; }
  bool is_muon    (size_t w) const { return !is_electron(w); }
  bool pass_lep_sel_bit(size_t w, uchar sel) const { return lep_id[w] & sel; }
  bool pass_lep_sel(size_t w, uchar el_sel, uchar mu_sel) const { 
    return
      (is_electron(w) && (lep_id[w] & el_sel)) || 
      (is_muon    (w) && (lep_id[w] & mu_sel));
  }

  TLorentzVector lep_p4(size_t w) const {
    const float mass = is_electron(w) ? 0.000511 : 0.106;
    return p4(lep_pt[w], lep_eta[w], lep_phi[w], mass);
  }

  int nlep(int type, uchar sel) const {
    int n = 0;
    for (size_t i = 0, ie = nlep(); i < ie; ++i)
      if (((lep_id[i] & 0x80) >> 7) == type && (lep_id[i] & sel))
        ++n;
    return n;
  }

  int nmu (uchar sel) const { return nlep(lep_mu, sel); }
  int nel (uchar sel) const { return nlep(lep_el, sel); }
  int nlep(uchar sel) const { return nmu(sel) + nel(sel); }

  float jetlep_ST(uchar el_sel, uchar mu_sel) const {
    double sum = jet_ST_sum();
    double sum_lep_pt = 0;

    for (size_t ilep = 0; ilep < nlep(); ++ilep) {
      if (pass_lep_sel(ilep, el_sel, mu_sel)) {
        sum_lep_pt += lep_pt[ilep];

        const double px_i = lep_pt[ilep] * cos(lep_phi[ilep]);
        const double py_i = lep_pt[ilep] * sin(lep_phi[ilep]);
        for (size_t jlep = 0; jlep < nlep(); ++jlep) {
          const double px_j = lep_pt[jlep] * cos(lep_phi[jlep]);
          const double py_j = lep_pt[jlep] * sin(lep_phi[jlep]);
          sum += (px_i*px_i * py_j*py_j - px_i*py_i * px_j*py_j) / (lep_pt[ilep] * lep_pt[jlep]);
        }
      }
    }

    return 1 - sqrt(1 - 4 * sum / pow(jet_ht() + sum_lep_pt, 2));
  }

  static ushort make_track_hitpattern(int npxh, int nsth, int npxl, int nstl) {
    assert(npxh >= 0 && nsth >= 0 && npxl >= 0 && nstl >= 0);
    if (npxh > 7) npxh = 7;
    if (nsth > 31) nsth = 31;
    if (npxl > 7) npxl = 7;
    if (nstl > 31) nstl = 31;
    return (nstl << 11) | (npxl << 8) | (nsth << 3) | npxh;
  }

  std::vector<float> vertex_seed_track_chi2dof;
  std::vector<float> vertex_seed_track_qpt;
  int vertex_seed_track_q(int i) const { return vertex_seed_track_qpt[i] > 0 ? 1 : -1; }
  float vertex_seed_track_pt(int i) const { return fabs(vertex_seed_track_qpt[i]); }
  std::vector<float> vertex_seed_track_eta;
  std::vector<float> vertex_seed_track_phi;
  std::vector<float> vertex_seed_track_dxy;
  std::vector<float> vertex_seed_track_dz;
  std::vector<ushort> vertex_seed_track_hp_;
  size_t n_vertex_seed_tracks() const { return vertex_seed_track_chi2dof.size(); }
  int vertex_seed_track_npxhits(int i) const { return vertex_seed_track_hp_[i] & 0x7; }
  int vertex_seed_track_nsthits(int i) const { return (vertex_seed_track_hp_[i] >> 3) & 0x1F; }
  int vertex_seed_track_nhits(int i) const { return vertex_seed_track_npxhits(i) + vertex_seed_track_nsthits(i); }
  int vertex_seed_track_npxlayers(int i) const { return (vertex_seed_track_hp_[i] >> 8) & 0x7; }
  int vertex_seed_track_nstlayers(int i) const { return (vertex_seed_track_hp_[i] >> 11) & 0x1F; }
  int vertex_seed_track_nlayers(int i) const { return vertex_seed_track_npxlayers(i) + vertex_seed_track_nstlayers(i); }

  std::vector<uchar> jet_track_which_jet;
  size_t n_jet_tracks() const { return jet_track_which_jet.size(); }
  std::vector<float> jet_track_chi2dof;
  std::vector<float> jet_track_qpt;
  int jet_track_q(int i) const { return jet_track_qpt[i] > 0 ? 1 : -1; }
  float jet_track_pt(int i) const { return fabs(jet_track_qpt[i]); }
  std::vector<float> jet_track_eta;
  std::vector<float> jet_track_phi;
  std::vector<float> jet_track_dxy;
  std::vector<float> jet_track_dz;
  std::vector<float> jet_track_pt_err;
  std::vector<float> jet_track_eta_err;
  std::vector<float> jet_track_phi_err;
  std::vector<float> jet_track_dxy_err;
  std::vector<float> jet_track_dz_err;
  std::vector<ushort> jet_track_hp_;
  int jet_track_npxhits(int i) const { return jet_track_hp_[i] & 0x7; }
  int jet_track_nsthits(int i) const { return (jet_track_hp_[i] >> 3) & 0x1F; }
  int jet_track_nhits(int i) const { return jet_track_npxhits(i) + jet_track_nsthits(i); }
  int jet_track_npxlayers(int i) const { return (jet_track_hp_[i] >> 8) & 0x7; }
  int jet_track_nstlayers(int i) const { return (jet_track_hp_[i] >> 11) & 0x1F; }
  int jet_track_nlayers(int i) const { return jet_track_npxlayers(i) + jet_track_nstlayers(i); }
};

#endif
