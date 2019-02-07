#ifndef JMTucker_Tools_TrackingTree_h
#define JMTucker_Tools_TrackingTree_h

#include <cassert>
#include <vector>
#include "TVector3.h"
#include "TLorentzVector.h"

class TTree;

class TrackingTree {
  typedef unsigned char uchar;
  typedef unsigned short ushort;
  typedef std::vector<float> vfloat;
  typedef std::vector<uchar> vuchar;
  typedef std::vector<ushort> vushort;
  typedef std::vector<unsigned> vunsigned;

 public:
  void set_event(unsigned r, unsigned l, unsigned long long e) { run_ = r; lumi_ = l; event_ = e; }
  unsigned run() const { return run_; }
  unsigned lumi() const { return lumi_; }
  unsigned long long event() const { return event_; }
  void set_npu(ushort n) { npu_ = n; }
  ushort npu() const { return npu_; }

  void set_bs(float x, float y, float z, float sigmaz, float dxdz, float dydz, float width,
              float err_x, float err_y, float err_z, float err_sigmaz, float err_dxdz, float err_dydz, float err_width) {
    bs_x_ = x;
    bs_y_ = y;
    bs_z_ = z;
    bs_sigmaz_ = sigmaz;
    bs_dxdz_ = dxdz;
    bs_dydz_ = dydz;
    bs_width_ = width;
    bs_err_x_ = err_x;
    bs_err_y_ = err_y;
    bs_err_z_ = err_z;
    bs_err_sigmaz_ = err_sigmaz;
    bs_err_dxdz_ = err_dxdz;
    bs_err_dydz_ = err_dydz;
    bs_err_width_ = err_width;
  }

  float bs_x() const { return bs_x_; }
  float bs_x(float z) const { return bs_x() + bs_dxdz() * (z - bs_z()); }
  float bs_y() const { return bs_y_; }
  float bs_y(float z) const { return bs_y() + bs_dydz() * (z - bs_z()); }
  float bs_z() const { return bs_z_; }
  float bs_sigmaz() const { return bs_sigmaz_; }
  float bs_dxdz() const { return bs_dxdz_; }
  float bs_dydz() const { return bs_dydz_; }
  float bs_width() const { return bs_width_; }
  float bs_err_x() const { return bs_err_x_; }
  float bs_err_y() const { return bs_err_y_; }
  float bs_err_z() const { return bs_err_z_; }
  float bs_err_sigmaz() const { return bs_err_sigmaz_; }
  float bs_err_dxdz() const { return bs_err_dxdz_; }
  float bs_err_dydz() const { return bs_err_dydz_; }
  float bs_err_width() const { return bs_err_width_; }

  void add_pv(float x, float y, float z, float chi2dof, float ndof, float score,
              float cxx, float cxy, float cxz, float cyy, float cyz, float czz) {
    pv_x_.push_back(x);
    pv_y_.push_back(y);
    pv_z_.push_back(z);
    pv_chi2dof_.push_back(chi2dof);
    pv_ndof_.push_back(ndof);
    pv_score_.push_back(score);
    pv_cxx_.push_back(cxx);
    pv_cxy_.push_back(cxy);
    pv_cxz_.push_back(cxz);
    pv_cyy_.push_back(cyy);
    pv_cyz_.push_back(cyz);
    pv_czz_.push_back(czz);
  }

  int npvs() const { return p_pv_x_ ? int(p_pv_x_->size()) : int(pv_x_.size()); }
  float pv_x(int i) const { return p_pv_x_ ? (*p_pv_x_)[i] : pv_x_[i]; }
  float pv_y(int i) const { return p_pv_y_ ? (*p_pv_y_)[i] : pv_y_[i]; }
  float pv_z(int i) const { return p_pv_z_ ? (*p_pv_z_)[i] : pv_z_[i]; }
  float pv_chi2dof(int i) const { return p_pv_chi2dof_ ? (*p_pv_chi2dof_)[i] : pv_chi2dof_[i]; }
  float pv_ndof(int i) const { return p_pv_ndof_ ? (*p_pv_ndof_)[i] : pv_ndof_[i]; }
  float pv_score(int i) const { return p_pv_score_ ? (*p_pv_score_)[i] : pv_score_[i]; }
  float pv_cxx(int i) const { return p_pv_cxx_ ? (*p_pv_cxx_)[i] : pv_cxx_[i]; }
  float pv_cxy(int i) const { return p_pv_cxy_ ? (*p_pv_cxy_)[i] : pv_cxy_[i]; }
  float pv_cxz(int i) const { return p_pv_cxz_ ? (*p_pv_cxz_)[i] : pv_cxz_[i]; }
  float pv_cyy(int i) const { return p_pv_cyy_ ? (*p_pv_cyy_)[i] : pv_cyy_[i]; }
  float pv_cyz(int i) const { return p_pv_cyz_ ? (*p_pv_cyz_)[i] : pv_cyz_[i]; }
  float pv_czz(int i) const { return p_pv_czz_ ? (*p_pv_czz_)[i] : pv_czz_[i]; }

  void add_tk(int q, float pt, float eta, float phi, float dxybs, float dxypv, float dzpv, float vx, float vy, float vz,
              float err_pt, float err_eta, float err_phi, float err_dxy, float err_dz, float chi2dof,
              int npxh, int nsth, int npxl, int nstl,
              int minhit_r, int minhit_z, int maxhit_r, int maxhit_z, int maxpxhit_r, int maxpxhit_z) {
    tk_qpt_.push_back(q*pt);
    tk_eta_.push_back(eta);
    tk_phi_.push_back(phi);
    tk_dxybs_.push_back(dxybs);
    tk_dxypv_.push_back(dxypv);
    tk_dzpv_.push_back(dzpv);
    tk_vx_.push_back(vx);
    tk_vy_.push_back(vy);
    tk_vz_.push_back(vz);
    tk_err_pt_.push_back(err_pt);
    tk_err_eta_.push_back(err_eta);
    tk_err_phi_.push_back(err_phi);
    tk_err_dxy_.push_back(err_dxy);
    tk_err_dz_.push_back(err_dz);
    tk_chi2dof_.push_back(chi2dof);

    assert(npxh >= 0 && nsth >= 0 && npxl >= 0 && nstl >= 0);
    if (npxh > 15) npxh = 15;
    if (nsth > 31) nsth = 31;
    if (npxl > 15) npxl = 15;
    if (nstl > 31) nstl = 31;
    tk_hp_.push_back((nstl << 13) | (npxl << 9) | (nsth << 4) | npxh);
    assert(minhit_r >= 0 && minhit_r <= 15);
    assert(minhit_z >= 0 && minhit_z <= 15);
    tk_minhit_.push_back((uchar(minhit_z) << 4) | uchar(minhit_r));
    assert(maxhit_r >= 0 && maxhit_r <= 15);
    assert(maxhit_z >= 0 && maxhit_z <= 15);
    tk_maxhit_.push_back((uchar(maxhit_z) << 4) | uchar(maxhit_r));
    assert(maxpxhit_r >= 0 && maxpxhit_r <= 15);
    assert(maxpxhit_z >= 0 && maxpxhit_z <= 15);
    tk_maxpxhit_.push_back((uchar(maxpxhit_z) << 4) | uchar(maxpxhit_r));
  }

  int ntks() const { return p_tk_qpt_ ? int(p_tk_qpt_->size()) : int(tk_qpt_.size()); }
  float tk_qpt(int i) const { return p_tk_qpt_ ? (*p_tk_qpt_)[i] : tk_qpt_[i]; }
  int tk_q(int i) const { return tk_qpt(i) > 0 ? 1 : -1; }
  float tk_pt(int i) const { return fabs(tk_qpt(i)); }
  float tk_eta(int i) const { return p_tk_eta_ ? (*p_tk_eta_)[i] : tk_eta_[i]; }
  float tk_phi(int i) const { return p_tk_phi_ ? (*p_tk_phi_)[i] : tk_phi_[i]; }
  float tk_dxybs(int i) const { return p_tk_dxybs_ ? (*p_tk_dxybs_)[i] : tk_dxybs_[i]; }
  float tk_dxypv(int i) const { return p_tk_dxypv_ ? (*p_tk_dxypv_)[i] : tk_dxypv_[i]; }
  float tk_dzpv(int i) const { return p_tk_dzpv_ ? (*p_tk_dzpv_)[i] : tk_dzpv_[i]; }
  float tk_vx(int i) const { return p_tk_vx_ ? (*p_tk_vx_)[i] : tk_vx_[i]; }
  float tk_vy(int i) const { return p_tk_vy_ ? (*p_tk_vy_)[i] : tk_vy_[i]; }
  float tk_vz(int i) const { return p_tk_vz_ ? (*p_tk_vz_)[i] : tk_vz_[i]; }
  float tk_err_pt(int i) const { return p_tk_err_pt_ ? (*p_tk_err_pt_)[i] : tk_err_pt_[i]; }
  float tk_err_eta(int i) const { return p_tk_err_eta_ ? (*p_tk_err_eta_)[i] : tk_err_eta_[i]; }
  float tk_err_phi(int i) const { return p_tk_err_phi_ ? (*p_tk_err_phi_)[i] : tk_err_phi_[i]; }
  float tk_err_dxy(int i) const { return p_tk_err_dxy_ ? (*p_tk_err_dxy_)[i] : tk_err_dxy_[i]; }
  float tk_err_dz(int i) const { return p_tk_err_dz_ ? (*p_tk_err_dz_)[i] : tk_err_dz_[i]; }
  float tk_chi2dof(int i) const { return p_tk_chi2dof_ ? (*p_tk_chi2dof_)[i] : tk_chi2dof_[i]; }
  unsigned tk_hp(int i) const { return p_tk_hp_ ? (*p_tk_hp_)[i] : tk_hp_[i]; }
  int tk_npxhits(int i) const { return tk_hp(i) & 0xf; }
  int tk_nsthits(int i) const { return (tk_hp(i) >> 4) & 0x1f; }
  int tk_npxlayers(int i) const { return (tk_hp(i) >> 9) & 0xf; }
  int tk_nstlayers(int i) const { return (tk_hp(i) >> 13) & 0x1f; }
  int tk_nhits(int i) const { return tk_npxhits(i) + tk_nsthits(i); }
  int tk_nlayers(int i) const { return tk_npxlayers(i) + tk_nstlayers(i); }
  uchar tk_minhit(int i) const { return p_tk_minhit_ ? (*p_tk_minhit_)[i] : tk_minhit_[i]; }
  int tk_min_r(int i) const { return tk_minhit(i) & 0xF; }
  int tk_min_z(int i) const { return tk_minhit(i) >> 4; }
  uchar tk_maxhit(int i) const { return p_tk_maxhit_ ? (*p_tk_maxhit_)[i] : tk_maxhit_[i]; }
  int tk_max_r(int i) const { return tk_maxhit(i) & 0xF; }
  int tk_max_z(int i) const { return tk_maxhit(i) >> 4; }
  uchar tk_maxpxhit(int i) const { return p_tk_maxpxhit_ ? (*p_tk_maxpxhit_)[i] : tk_maxpxhit_[i]; }
  int tk_maxpx_r(int i) const { return tk_maxpxhit(i) & 0xF; }
  int tk_maxpx_z(int i) const { return tk_maxpxhit(i) >> 4; }
  TVector3 tk_momentum(int i) const { TVector3 v; v.SetPtEtaPhi(tk_pt(i), tk_eta(i), tk_phi(i)); return v; }
  TLorentzVector tk_p4(int i, double m=0) const { TLorentzVector v; v.SetPtEtaPhiM(tk_pt(i), tk_eta(i), tk_phi(i), m); return v; }

  TrackingTree();
  void clear();
  void write_to_tree(TTree* tree);
  void read_from_tree(TTree* tree);

 private:
  unsigned run_;
  unsigned lumi_;
  unsigned long long event_;
  ushort npu_;

  float bs_x_;
  float bs_y_;
  float bs_z_;
  float bs_sigmaz_;
  float bs_dxdz_;
  float bs_dydz_;
  float bs_width_;
  float bs_err_x_;
  float bs_err_y_;
  float bs_err_z_;
  float bs_err_sigmaz_;
  float bs_err_dxdz_;
  float bs_err_dydz_;
  float bs_err_width_;

  vfloat pv_x_;           vfloat* p_pv_x_;
  vfloat pv_y_;           vfloat* p_pv_y_;
  vfloat pv_z_;           vfloat* p_pv_z_;
  vfloat pv_chi2dof_;     vfloat* p_pv_chi2dof_;
  vfloat pv_ndof_;        vfloat* p_pv_ndof_;
  vfloat pv_score_;       vfloat* p_pv_score_;
  vfloat pv_cxx_;         vfloat* p_pv_cxx_;
  vfloat pv_cxy_;         vfloat* p_pv_cxy_;
  vfloat pv_cxz_;         vfloat* p_pv_cxz_;
  vfloat pv_cyy_;         vfloat* p_pv_cyy_;
  vfloat pv_cyz_;         vfloat* p_pv_cyz_;
  vfloat pv_czz_;         vfloat* p_pv_czz_;

  vfloat tk_qpt_;         vfloat* p_tk_qpt_;
  vfloat tk_eta_;         vfloat* p_tk_eta_;
  vfloat tk_phi_;         vfloat* p_tk_phi_;
  vfloat tk_dxybs_;       vfloat* p_tk_dxybs_;
  vfloat tk_dxypv_;       vfloat* p_tk_dxypv_;
  vfloat tk_dzpv_;        vfloat* p_tk_dzpv_;
  vfloat tk_vx_;          vfloat* p_tk_vx_;
  vfloat tk_vy_;          vfloat* p_tk_vy_;
  vfloat tk_vz_;          vfloat* p_tk_vz_;
  vfloat tk_err_pt_;      vfloat* p_tk_err_pt_;
  vfloat tk_err_eta_;     vfloat* p_tk_err_eta_;
  vfloat tk_err_phi_;     vfloat* p_tk_err_phi_;
  vfloat tk_err_dxy_;     vfloat* p_tk_err_dxy_;
  vfloat tk_err_dz_;      vfloat* p_tk_err_dz_;
  vfloat tk_chi2dof_;     vfloat* p_tk_chi2dof_;
  vunsigned tk_hp_;       vunsigned* p_tk_hp_;
  vuchar tk_minhit_;      vuchar* p_tk_minhit_;
  vuchar tk_maxhit_;      vuchar* p_tk_maxhit_;
  vuchar tk_maxpxhit_;    vuchar* p_tk_maxpxhit_;
};

#endif
