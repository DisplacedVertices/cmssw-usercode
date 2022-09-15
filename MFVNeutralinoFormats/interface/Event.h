#ifndef JMTucker_MFVNeutralinoFormats_interface_Event_h
#define JMTucker_MFVNeutralinoFormats_interface_Event_h

#include <cassert>
#include <numeric>
#include "TLorentzVector.h"
#include "DataFormats/Math/interface/Point3D.h"
#include "JMTucker/MFVNeutralinoFormats/interface/HitPattern.h"
#include "JMTucker/MFVNeutralinoFormats/interface/TriggerEnum.h"
#include "JMTucker/MFVNeutralinoFormats/interface/MCInteractions.h"

#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"

namespace reco { class Track; class Candidate; }

namespace mfv {
  static const float min_jet_pt = 20; // JMTBAD take away once it's back at ntuple level
}

struct MFVEvent {
  typedef unsigned char uchar;
  typedef unsigned short ushort;
  typedef unsigned int uint;

  static bool test_bit(uint64_t v, size_t i) { return bool((v >> i) & 1); }
  static void set_bit(uint64_t& v, size_t i, bool x) { v ^= (-uint64_t(x) ^ v) & (1ULL << i); }

  MFVEvent() {
    gen_valid = 0;
    npv = pv_ntracks = pv_ntracksloose = 0;
    gen_flavor_code = 0;
    gen_weight = l1_htt = l1_myhtt = l1_myhttwbug = hlt_ht = npu = bsx = bsy = bsz = bsdxdz = bsdydz = bswidthx = bswidthy = pvx = pvy = pvz = pvcxx = pvcxy = pvcxz = pvcyy = pvcyz = pvczz = pv_score = metx = mety = metNoMux = metNoMuy = met_calo = 0;
    pass_metfilters = false;
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

  template <typename T>
  static T mag2(T x, T y, T z) {
    return x*x + y*y + z*z;
  }

  float gen_weight;
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

  int lspmatches(const float x, const float y, const float z, const float dist2=0.0084*0.0084) const {
    for (int i = 0; i < 2; ++i)
      if (mag2(x - gen_lsp_decay[i*3+0],
               y - gen_lsp_decay[i*3+1],
               z - gen_lsp_decay[i*3+2]) < dist2)
        return i;
    return -1;
  }
  template <typename T> int lspmatches(const T& v, const float dist2=0.0084*0.0084) const { return lspmatches(v.x, v.y, v.z, dist2); }

  float l1_htt;
  float l1_myhtt;
  float l1_myhttwbug;
  float hlt_ht;

  

  uint64_t pass_;
  uint64_t pass_hlt_bits() const { return pass_ & ((1UL << mfv::n_hlt_paths) - 1UL); }
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
  float pv_score;
  uchar pv_ntracks;
  uchar pv_ntracksloose;
  float pv_rho() const { return mag(pvx - bsx_at_z(pvz), pvy - bsy_at_z(pvz)); }

  std::vector<float> pvsx;
  std::vector<float> pvsy;
  std::vector<float> pvsz;
  std::vector<uchar> pvsscores;

  float pv_x(size_t i) const { return i == 0 ? pvx : pvsx[i-1]; } // these whole classes need cleaning with fire
  float pv_y(size_t i) const { return i == 0 ? pvy : pvsy[i-1]; }
  float pv_z(size_t i) const { return i == 0 ? pvz : pvsz[i-1]; }
  float pv_score_(size_t i) const { return i == 0 ? pv_score : pvsscores[i-1]; } // JMTBAD oops, didn't bin in Producer

  std::vector<uchar> jet_id; // see encode_jet_id for definition
  std::vector<float> jet_bdisc_old; // JMTBAD CSV for backward compatibility, to be removed
  std::vector<float> jet_bdisc;
  std::vector<float> jet_pudisc; // to be removed and put into _id when working points defined
  std::vector<float> jet_pt;
  std::vector<float> jet_raw_pt;
  std::vector<float> jet_eta;
  std::vector<float> jet_phi;
  std::vector<float> jet_energy;
  std::vector<float> jet_gen_energy;

  TLorentzVector jet_p4(int w) const {
    TLorentzVector v;
    v.SetPtEtaPhiE(jet_pt[w], jet_eta[w], jet_phi[w], jet_energy[w]);
    return v;
  }

  int njets() const { return int(jet_id.size()); }
  int njets(float min_jet_pt) const { return std::count_if(jet_pt.begin(), jet_pt.end(),
                                                           [min_jet_pt](float b) { return b > min_jet_pt; }); }

  float nth_jet_pt (int w) const { return njets() > w ? jet_pt [w] :   -1.f; }
  float nth_jet_eta(int w) const { return njets() > w ? jet_eta[w] : -999.f; }
  float nth_jet_phi(int w) const { return njets() > w ? jet_phi[w] : -999.f; }

  std::vector<float> jet_hlt_pt;
  std::vector<float> jet_hlt_eta;
  std::vector<float> jet_hlt_phi;
  std::vector<float> jet_hlt_energy;
  std::vector<float> displaced_jet_hlt_pt;
  std::vector<float> displaced_jet_hlt_eta;
  std::vector<float> displaced_jet_hlt_phi;
  std::vector<float> displaced_jet_hlt_energy;
  void jet_hlt_push_back(const reco::Candidate& jet, const std::vector<TLorentzVector>& hltjets, bool is_displaced_calojets);

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

  bool pass_metfilters;

  float metx;
  float mety;
  float met() const { return mag(metx, mety); }
  float metphi() const { return atan2(mety, metx); }
  float met_calo;

  float metNoMux;
  float metNoMuy;
  float metNoMu() const { return mag(metNoMux, metNoMuy); }
  float metNoMuphi() const { return atan2(metNoMuy, metNoMux); }

 // leptons 
  std::vector<float> muon_pt;
  std::vector<float> muon_eta;
  std::vector<float> muon_phi;
  std::vector<float> muon_pt_err;
  std::vector<float> muon_eta_err;
  std::vector<float> muon_phi_err;
  std::vector<float> muon_x;
  std::vector<float> muon_y;
  std::vector<float> muon_z;
  std::vector<float> muon_lxy;
  std::vector<float> muon_l;
  std::vector<float> muon_iso;
  std::vector<float> muon_dxy;
  std::vector<float> muon_dz;
  std::vector<float> muon_dxybs;
  std::vector<float> muon_dxyerr;
  std::vector<float> muon_dzerr;
  std::vector<float> muon_chi2dof;

  std::vector<float> electron_pt;
  std::vector<float> electron_eta;
  std::vector<float> electron_phi;
  std::vector<float> electron_pt_err;
  std::vector<float> electron_eta_err;
  std::vector<float> electron_phi_err;
  std::vector<float> electron_x;
  std::vector<float> electron_y;
  std::vector<float> electron_z;
  std::vector<float> electron_lxy;
  std::vector<float> electron_l;
  std::vector<float> electron_dxy;
  std::vector<float> electron_dz;
  std::vector<float> electron_dxybs;
  std::vector<float> electron_dxyerr;
  std::vector<float> electron_dzerr;
  std::vector<float> electron_chi2dof;


  std::vector<float> electron_isEB;
  std::vector<float> electron_isEE;
  std::vector<float> electron_sigmaIetaIeta5x5;
  std::vector<float> electron_dEtaAtVtx;
  std::vector<float> electron_dPhiAtVtx;
  std::vector<float> electron_HE;
  std::vector<float> electron_ooEmooP;
  std::vector<float> electron_expectedMissingInnerHits;
  std::vector<float> electron_passveto;
  std::vector<float> electron_iso;

  //isolation variables
  std::vector<float> electron_had_iso;
  std::vector<float> electron_neutral_iso;
  std::vector<float> electron_photon_iso;
  std::vector<float> electron_corr;
  std::vector<float> muon_had_iso;
  std::vector<float> muon_neutral_iso;
  std::vector<float> muon_photon_iso;
  std::vector<float> muon_PU_corr;

  std::vector<std::vector<int>> electron_ID;
  std::vector<std::vector<int>> muon_ID;
  
  
  void muon_push_back(const reco::Muon& muon,
		      const reco::Track& trk,
		      const float iso,
		      const math::XYZPoint& beamspot,
		      const math::XYZPoint& primary_vertex);

  void electron_push_back(const reco::GsfElectron& electron,
			  const reco::Track& trk,
			  const float iso,
			  const math::XYZPoint& beamspot,
			  const math::XYZPoint& primary_vertex);

  void muon_pfiso_push_back(const float muhad_iso,
			    const float muneut_iso,
			    const float muphoton_iso,
			    const float PU_corr);

  void electron_pfiso_push_back(const float elhad_iso,
				const float elneut_iso,
				const float elphoton_iso,
				const float elcorr);

  void ele_ID_push_back(const reco::GsfElectron& electron,
			const bool h_Escaled,
			const float ooEmooP,
			const int expectedMissingInnerHits,
			const float iso,
			const bool passveto);
  
  std::vector<mfv::HitPattern::value_t> muon_hp_;
  mfv::HitPattern muon_hp(int i) const { return mfv::HitPattern(muon_hp_[i]); }
  void muon_hp_push_back(int npxh, int nsth, int npxl, int nstl) { muon_hp_.push_back(mfv::HitPattern(npxh, nsth, npxl, nstl).value); }
  int muon_npxhits(int i) const { return muon_hp(i).npxhits(); }
  int muon_nsthits(int i) const { return muon_hp(i).nsthits(); }
  int muon_nhits(int i) const { return muon_hp(i).nhits(); }
  int muon_npxlayers(int i) const { return muon_hp(i).npxlayers(); }
  int muon_nstlayers(int i) const { return muon_hp(i).nstlayers(); }
  int muon_nlayers(int i) const { return muon_hp(i).nlayers(); }


  std::vector<mfv::HitPattern::value_t> electron_hp_;
  mfv::HitPattern electron_hp(int i) const { return mfv::HitPattern(electron_hp_[i]); }
  void electron_hp_push_back(int npxh, int nsth, int npxl, int nstl) { electron_hp_.push_back(mfv::HitPattern(npxh, nsth, npxl, nstl).value); }
  int electron_npxhits(int i) const { return electron_hp(i).npxhits(); }
  int electron_nsthits(int i) const { return electron_hp(i).nsthits(); }
  int electron_nhits(int i) const { return electron_hp(i).nhits(); }
  int electron_npxlayers(int i) const { return electron_hp(i).npxlayers(); }
  int electron_nstlayers(int i) const { return electron_hp(i).nstlayers(); }
  int electron_nlayers(int i) const { return electron_hp(i).nlayers(); }

  int nmuons() const { return int(muon_pt.size()); }
  int nelectrons() const { return int(electron_pt.size()); }
  int nlep() const { return nmuons() + nelectrons(); }

  int nmuons(float min_muon_pt) const { return std::count_if(muon_pt.begin(), muon_pt.end(),
                                                           [min_muon_pt](float c) { return c > min_muon_pt; }); }
  int nelectrons(float min_electron_pt) const { return std::count_if(electron_pt.begin(), electron_pt.end(),
                                                           [min_electron_pt](float d) { return d > min_electron_pt; }); }

  /////////////////////////////////////////////////////

  size_t n_vertex_seed_tracks() const { return vertex_seed_track_chi2dof.size(); }
  std::vector<float> vertex_seed_track_chi2dof;
  std::vector<float> vertex_seed_track_qpt;
  int vertex_seed_track_q(int i) const { return vertex_seed_track_qpt[i] > 0 ? 1 : -1; }
  float vertex_seed_track_pt(int i) const { return fabs(vertex_seed_track_qpt[i]); }
  std::vector<float> vertex_seed_track_eta;
  std::vector<float> vertex_seed_track_phi;
  std::vector<float> vertex_seed_track_dxy;
  std::vector<float> vertex_seed_track_dz;
  std::vector<float> vertex_seed_track_err_pt;
  std::vector<float> vertex_seed_track_err_eta;
  std::vector<float> vertex_seed_track_err_phi;
  std::vector<float> vertex_seed_track_err_dxy;
  std::vector<float> vertex_seed_track_err_dz;
  std::vector<mfv::HitPattern::value_t> vertex_seed_track_hp_;
  mfv::HitPattern vertex_seed_track_hp(int i) const { return mfv::HitPattern(vertex_seed_track_hp_[i]); }
  void vertex_seed_track_hp_push_back(int npxh, int nsth, int npxl, int nstl) { vertex_seed_track_hp_.push_back(mfv::HitPattern(npxh, nsth, npxl, nstl).value); }
  int vertex_seed_track_npxhits(int i) const { return vertex_seed_track_hp(i).npxhits(); }
  int vertex_seed_track_nsthits(int i) const { return vertex_seed_track_hp(i).nsthits(); }
  int vertex_seed_track_nhits(int i) const { return vertex_seed_track_hp(i).nhits(); }
  int vertex_seed_track_npxlayers(int i) const { return vertex_seed_track_hp(i).npxlayers(); }
  int vertex_seed_track_nstlayers(int i) const { return vertex_seed_track_hp(i).nstlayers(); }
  int vertex_seed_track_nlayers(int i) const { return vertex_seed_track_hp(i).nlayers(); }

  size_t n_jet_tracks_all() const { return jet_track_which_jet.size(); }
  std::vector<uchar> jet_track_which_jet;
  size_t n_jet_tracks(const size_t i) const { return std::count(jet_track_which_jet.begin(), jet_track_which_jet.end(), i); }
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
  std::vector<mfv::HitPattern::value_t> jet_track_hp_;
  mfv::HitPattern jet_track_hp(int i) const { return mfv::HitPattern(jet_track_hp_[i]); }
  void jet_track_hp_push_back(int npxh, int nsth, int npxl, int nstl) { jet_track_hp_.push_back(mfv::HitPattern(npxh, nsth, npxl, nstl).value); }
  int jet_track_npxhits(int i) const { return jet_track_hp(i).npxhits(); }
  int jet_track_nsthits(int i) const { return jet_track_hp(i).nsthits(); }
  int jet_track_nhits(int i) const { return jet_track_hp(i).nhits(); }
  int jet_track_npxlayers(int i) const { return jet_track_hp(i).npxlayers(); }
  int jet_track_nstlayers(int i) const { return jet_track_hp(i).nstlayers(); }
  int jet_track_nlayers(int i) const { return jet_track_hp(i).nlayers(); }

  // stuff we aren't sure should be permanently in ntuple; the meaning of the entries is version-dependent
  std::vector<float> misc;

  // scale uncertainty weights
  double ren_weight_up;
  double ren_weight_dn;
  double fac_weight_up;
  double fac_weight_dn;
};

#endif
