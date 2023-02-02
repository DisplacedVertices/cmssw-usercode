#ifndef JMTucker_Tools_Ntuple_h
#define JMTucker_Tools_Ntuple_h

#include <cassert>
#include <numeric>
#include <vector>
#include "TLorentzVector.h"
#include "TTree.h"
#include "TVector3.h"
#define SMATRIX_USE_CONSTEXPR
#include "Math/SVector.h"
#include "Math/SMatrix.h"

namespace jmt {
  class INtuple {
  public:
    virtual ~INtuple() {};

    const char* pfx() const { return pfx_; }
    void set_pfx(const char* p) { pfx_ = p; }

    virtual int n() const { return 0; } // to be implemented in classes that are indexed, e.g. tracks, vertices, etc.
    std::vector<int> iota() const { std::vector<int> i(n()); std::iota(i.begin(), i.end(), 0); return i; }

  protected:
    typedef unsigned char uchar;
    typedef unsigned short ushort;
    typedef std::vector<bool> vbool;
    typedef std::vector<float> vfloat;
    typedef std::vector<uchar> vuchar;
    typedef std::vector<ushort> vushort;
    typedef std::vector<unsigned> vunsigned;
    typedef std::vector<int> vint;

    typedef ROOT::Math::SVector<double,3> Vec3;
    typedef ROOT::Math::SMatrix<double,3,3,ROOT::Math::MatRepSym<double,3> > SymMat33;

    template <typename T> static int p_size(const std::vector<T>& v, const std::vector<T>* p) { return int(p ? p->size() : v.size()); }
    template <typename T> static T p_get(int i, const std::vector<T>& v, const std::vector<T>* p) { return p ? p->at(i) : v.at(i); }

    template <typename T> static bool test_bit(T v, size_t i) { return bool((v >> i) & 1); }
    template <typename T> static void set_bit(T& v, size_t i, bool x) { v ^= (-T(x) ^ v) & (T(1) << i); }

    static TVector3 p3_(double pt, double eta, double phi) { TVector3 v; v.SetPtEtaPhi(pt, eta, phi); return v; }
    static TLorentzVector p4_e(double pt, double eta, double phi, double e) { TLorentzVector v; v.SetPtEtaPhiE(pt, eta, phi, e); return v; }
    static TLorentzVector p4_m(double pt, double eta, double phi, double m) { TLorentzVector v; v.SetPtEtaPhiM(pt, eta, phi, m); return v; }

    const char* pfx_;

  public:
    virtual void clear() = 0;
    virtual void write_to_tree(TTree*) = 0;
    virtual void read_from_tree(TTree*) = 0;
    virtual void copy_vectors() = 0;
  };

  ////

  class BaseSubNtuple : public INtuple {
  public:
    BaseSubNtuple();
    virtual void clear();
    virtual void write_to_tree(TTree*);
    virtual void read_from_tree(TTree*);
    virtual void copy_vectors() {}

    void set_weight(float x) { weight_ = x; }
    float weight() const { return weight_; }
    void set_event(unsigned r, unsigned l, unsigned long long e) { run_ = r; lumi_ = l; event_ = e; }
    unsigned run() const { return run_; }
    unsigned lumi() const { return lumi_; }
    unsigned long long event() const { return event_; }
    void set_pass(uchar x) { pass_ = x; }
    uchar pass() const { return pass_; }
    void set_npu(uchar x) { npu_ = x; }
    uchar npu() const { return npu_; }
    void set_rho(float x) { rho_ = x; }
    float rho() const { return rho_; }
    void set_nallpv(uchar x) { nallpv_ = x; }
    uchar nallpv() const { return nallpv_; }

    bool is_mc() const { return run() == 1; }

  private:
    float weight_;
    unsigned run_;
    unsigned lumi_;
    unsigned long long event_;
    uchar pass_;
    uchar npu_;
    float rho_;
    uchar nallpv_;
  };

  ////

  class BeamspotSubNtuple : public INtuple {
  public:
    BeamspotSubNtuple();
    virtual void clear();
    virtual void write_to_tree(TTree* tree);
    virtual void read_from_tree(TTree* tree);
    virtual void copy_vectors() {}

    void set(float x, float y, float z, float sigmaz, float dxdz, float dydz, float width,
             float err_x, float err_y, float err_z, float err_sigmaz, float err_dxdz, float err_dydz, float err_width) {
      x_ = x;
      y_ = y;
      z_ = z;
      sigmaz_ = sigmaz;
      dxdz_ = dxdz;
      dydz_ = dydz;
      width_ = width;
      err_x_ = err_x;
      err_y_ = err_y;
      err_z_ = err_z;
      err_sigmaz_ = err_sigmaz;
      err_dxdz_ = err_dxdz;
      err_dydz_ = err_dydz;
      err_width_ = err_width;
    }

    float x() const { return x_; }
    float y() const { return y_; }
    float z() const { return z_; }
    float sigmaz() const { return sigmaz_; }
    float dxdz() const { return dxdz_; }
    float dydz() const { return dydz_; }
    float width() const { return width_; }
    float err_x() const { return err_x_; }
    float err_y() const { return err_y_; }
    float err_z() const { return err_z_; }
    float err_sigmaz() const { return err_sigmaz_; }
    float err_dxdz() const { return err_dxdz_; }
    float err_dydz() const { return err_dydz_; }
    float err_width() const { return err_width_; }
    float cxx() const { return std::pow(err_x(), 2); }
    float cyy() const { return std::pow(err_y(), 2); }
    float czz() const { return std::pow(err_z(), 2); }
    float cxy() const { return 0; }
    float cxz() const { return 0; }
    float cyz() const { return 0; }
    float phi() const { return std::atan2(y(), x()); }
    float x(float zp) const { return x() + dxdz() * (zp - z()); }
    float y(float zp) const { return y() + dydz() * (zp - z()); }

    TVector3 pos() const { return TVector3(x(), y(), z()); }
    SymMat33 cov() const { SymMat33 c; c(0,0) = cxx(), c(1,1) = cyy(), c(2,2) = czz(); return c; }

    float rho(float xx, float yy, float zz) const { return std::hypot(xx - x(zz), yy - y(zz)); }
    float erho(float xx, float yy, float /*zz*/, float exx, float exy, float eyy) const {
      float dx = xx - x(), dy = yy - y(); // JMTBAD we never used the slope-corrected version
      if (dx == 0 && dy == 0) return std::numeric_limits<float>::infinity();
      float Cxx = exx + cxx(), Cxy = exy + cxy(), Cyy = eyy + cyy();
      return sqrt((Cxx*dx*dx + Cyy*dy*dy + 2*Cxy*dx*dy) / (dx*dx + dy*dy));
    }
    template <typename T> float rho (const T& v) const { return rho (v.x(), v.y(), v.z()); }
    template <typename T> float erho(const T& v) const { return erho(v.x(), v.y(), v.z(), v.covariance(0,0), v.covariance(0,1), v.covariance(1,1)); }

  protected:
    Vec3 pos_() const { return Vec3(x(), y(), z()); }

  private:
    float x_;
    float y_;
    float z_;
    float sigmaz_;
    float dxdz_;
    float dydz_;
    float width_;
    float err_x_;
    float err_y_;
    float err_z_;
    float err_sigmaz_;
    float err_dxdz_;
    float err_dydz_;
    float err_width_;
  };

  ////

  class VerticesSubNtuple : public INtuple {
  public:
    VerticesSubNtuple();
    virtual void clear();
    virtual void write_to_tree(TTree* tree);
    virtual void read_from_tree(TTree* tree);
    virtual void copy_vectors();

    void add(float xx, float yy, float zz, float chi2, float ndof, uchar ntracks, float score,
             float cxx, float cxy, float cxz, float cyy, float cyz, float czz,
             unsigned misc) {
      x_.push_back(xx);
      y_.push_back(yy);
      z_.push_back(zz);
      chi2_.push_back(chi2);
      ndof_.push_back(ndof);
      ntracks_.push_back(ntracks);
      score_.push_back(score);
      cxx_.push_back(cxx);
      cxy_.push_back(cxy);
      cxz_.push_back(cxz);
      cyy_.push_back(cyy);
      cyz_.push_back(cyz);
      czz_.push_back(czz);
      misc_.push_back(misc);
    }

    virtual int n() const { return p_size(x_, p_x_); }
    float x      (int i) const { return p_get(i, x_,       p_x_       ); }
    float y      (int i) const { return p_get(i, y_,       p_y_       ); }
    float z      (int i) const { return p_get(i, z_,       p_z_       ); }
    float chi2   (int i) const { return p_get(i, chi2_,    p_chi2_    ); }
    float ndof   (int i) const { return p_get(i, ndof_,    p_ndof_    ); }
    uchar ntracks(int i) const { return p_get(i, ntracks_, p_ntracks_ ); }
    float score  (int i) const { return p_get(i, score_,   p_score_   ); }
    float cxx    (int i) const { return p_get(i, cxx_,     p_cxx_     ); }
    float cxy    (int i) const { return p_get(i, cxy_,     p_cxy_     ); }
    float cxz    (int i) const { return p_get(i, cxz_,     p_cxz_     ); }
    float cyy    (int i) const { return p_get(i, cyy_,     p_cyy_     ); }
    float cyz    (int i) const { return p_get(i, cyz_,     p_cyz_     ); }
    float czz    (int i) const { return p_get(i, czz_,     p_czz_     ); }
    unsigned misc(int i) const { return p_get(i, misc_,    p_misc_    ); }

    void set_misc(int i, unsigned m) { assert(0 == p_misc_); misc_[i] = m; }

    TVector3 pos(int i) const { return TVector3(x(i), y(i), z(i)); }
    SymMat33 cov(int i) const { SymMat33 c; c(0,0) = cxx(i), c(0,1) = cxy(i), c(0,2) = cxz(i),
                                                             c(1,1) = cyy(i), c(1,2) = cyz(i),
                                                                              c(2,2) = czz(i); return c; }

    float phi(int i) const { return std::atan2(y(i), x(i)); }
    float rho(int i) const { return std::hypot(x(i), y(i)); }
    template <typename BS> float xraw(int i, const BS& bs) const { return x(i) + bs.x(z(i)); }
    template <typename BS> float yraw(int i, const BS& bs) const { return y(i) + bs.y(z(i)); }
    template <typename BS> float phiraw(int i, const BS& bs) const { return std::atan2(y(i, bs), x(i, bs)); }
    template <typename BS> float rhoraw(int i, const BS& bs) const { return std::hypot(x(i, bs), y(i, bs)); }
    template <typename BS> TVector3 posraw(int i, const BS& bs) const { return TVector3(xraw(i, bs), yraw(i, bs), z(i, bs)); }
    float chi2dof(int i) const { return chi2(i) / ndof(i); }

  protected:
    Vec3 pos_(int i) const { return Vec3(x(i), y(i), z(i)); }

  private:
    vfloat x_;           vfloat* p_x_;
    vfloat y_;           vfloat* p_y_;
    vfloat z_;           vfloat* p_z_;
    vfloat chi2_;        vfloat* p_chi2_;
    vfloat ndof_;        vfloat* p_ndof_;
    vuchar ntracks_;     vuchar* p_ntracks_;
    vfloat score_;       vfloat* p_score_;
    vfloat cxx_;         vfloat* p_cxx_;
    vfloat cxy_;         vfloat* p_cxy_;
    vfloat cxz_;         vfloat* p_cxz_;
    vfloat cyy_;         vfloat* p_cyy_;
    vfloat cyz_;         vfloat* p_cyz_;
    vfloat czz_;         vfloat* p_czz_;
    vunsigned misc_;     vunsigned* p_misc_;
  };

  class PrimaryVerticesSubNtuple   : public VerticesSubNtuple { public: PrimaryVerticesSubNtuple  () { set_pfx("pv"); }};
  class SecondaryVerticesSubNtuple : public VerticesSubNtuple { public: SecondaryVerticesSubNtuple() { set_pfx("sv"); }};

  ////

  class TracksSubNtuple : public INtuple {
  public:
    TracksSubNtuple();
    virtual void clear();
    virtual void write_to_tree(TTree* tree);
    virtual void read_from_tree(TTree* tree);
    virtual void copy_vectors();

    //will be storing the boolean value if the track is a lepton or not true == 1 false == 0;
    void add(int q, float pt, float eta, float phi, float vx, float vy, float vz,
             float cov_00, float cov_11, float cov_14, float cov_22, float cov_23, float cov_33, float cov_34, float cov_44,
             float chi2dof,
             int npxh, int nsth, int npxl, int nstl,
             int minhit_r, int minhit_z, int maxhit_r, int maxhit_z, int maxpxhit_r, int maxpxhit_z,
             int which_jet, int which_pv, bool ismu, bool isel, bool isgoodmu, bool isgoodel,
	     int which_sv,
             unsigned misc) {
      qpt_.push_back(q*pt);
      eta_.push_back(eta);
      phi_.push_back(phi);
      vx_.push_back(vx);
      vy_.push_back(vy);
      vz_.push_back(vz);
      cov_00_.push_back(cov_00);
      cov_11_.push_back(cov_11);
      cov_14_.push_back(cov_14);
      cov_22_.push_back(cov_22);
      cov_23_.push_back(cov_23);
      cov_33_.push_back(cov_33);
      cov_34_.push_back(cov_34);
      cov_44_.push_back(cov_44);
      chi2dof_.push_back(chi2dof);

      assert(npxh >= 0 && nsth >= 0 && npxl >= 0 && nstl >= 0);
      if (npxh > 15) npxh = 15;
      if (nsth > 31) nsth = 31;
      if (npxl > 15) npxl = 15;
      if (nstl > 31) nstl = 31;
      hp_.push_back((nstl << 13) | (npxl << 9) | (nsth << 4) | npxh);
      assert(minhit_r >= 0 && minhit_r <= 15);
      assert(minhit_z >= 0 && minhit_z <= 15);
      minhit_.push_back((uchar(minhit_z) << 4) | uchar(minhit_r));
      assert(maxhit_r >= 0 && maxhit_r <= 15);
      assert(maxhit_z >= 0 && maxhit_z <= 15);
      maxhit_.push_back((uchar(maxhit_z) << 4) | uchar(maxhit_r));
      assert(maxpxhit_r >= 0 && maxpxhit_r <= 15);
      assert(maxpxhit_z >= 0 && maxpxhit_z <= 15);
      maxpxhit_.push_back((uchar(maxpxhit_z) << 4) | uchar(maxpxhit_r));

      which_jet_.push_back(which_jet < 0 || which_jet > 255 ? 255 : which_jet);
      which_pv_.push_back(which_pv < 0 || which_pv > 255 ? 255 : which_pv);
      which_sv_.push_back(which_sv < 0 || which_sv > 255 ? 255 : which_sv);
      ismu_.push_back(ismu);
      isel_.push_back(isel);
      isgoodmu_.push_back(isgoodmu);
      isgoodel_.push_back(isgoodel);
      misc_.push_back(misc);
    }

    virtual int n() const { return p_size(qpt_, p_qpt_); }
    float    qpt      (int i) const { return p_get(i, qpt_,       p_qpt_       ); }
    float    eta      (int i) const { return p_get(i, eta_,       p_eta_       ); }
    float    phi      (int i) const { return p_get(i, phi_,       p_phi_       ); }
    float    vx       (int i) const { return p_get(i, vx_,        p_vx_        ); }
    float    vy       (int i) const { return p_get(i, vy_,        p_vy_        ); }
    float    vz       (int i) const { return p_get(i, vz_,        p_vz_        ); }
    float    cov_00   (int i) const { return p_get(i, cov_00_,    p_cov_00_    ); }
    float    cov_11   (int i) const { return p_get(i, cov_11_,    p_cov_11_    ); }
    float    cov_14   (int i) const { return p_get(i, cov_14_,    p_cov_14_    ); }
    float    cov_22   (int i) const { return p_get(i, cov_22_,    p_cov_22_    ); }
    float    cov_23   (int i) const { return p_get(i, cov_23_,    p_cov_23_    ); }
    virtual float cov_33 (int i) const { return p_get(i, cov_33_, p_cov_33_ ); }
    virtual float cov_34 (int i) const { return p_get(i, cov_34_, p_cov_34_ ); }
    virtual float cov_44 (int i) const { return p_get(i, cov_44_, p_cov_44_ ); }
    float    chi2dof  (int i) const { return p_get(i, chi2dof_,   p_chi2dof_   ); }
    unsigned hp       (int i) const { return p_get(i, hp_,        p_hp_        ); }
    uchar    minhit   (int i) const { return p_get(i, minhit_,    p_minhit_    ); }
    uchar    maxhit   (int i) const { return p_get(i, maxhit_,    p_maxhit_    ); }
    uchar    maxpxhit (int i) const { return p_get(i, maxpxhit_,  p_maxpxhit_  ); }
    uchar    which_jet(int i) const { return p_get(i, which_jet_, p_which_jet_ ); }
    uchar    which_pv (int i) const { return p_get(i, which_pv_,  p_which_pv_  ); }
    uchar    which_sv (int i) const { return p_get(i, which_sv_,  p_which_sv_  ); }
    bool     ismu     (int i) const { return p_get(i, ismu_,      p_ismu_      ); }
    bool     isel     (int i) const { return p_get(i, isel_,      p_isel_      ); }
    bool     isgoodmu     (int i) const { return p_get(i, isgoodmu_,      p_isgoodmu_      ); }
    bool     isgoodel     (int i) const { return p_get(i, isgoodel_,      p_isgoodel_      ); }
    
    unsigned misc     (int i) const { return p_get(i, misc_,      p_misc_      ); }

    void set_which_jet(int i, uchar x) { assert(0 == p_which_jet_); which_jet_[i] = x; }
    void set_which_pv(int i, uchar x) { assert(0 == p_which_pv_); which_pv_[i] = x; }
    void set_which_sv(int i, uchar x) { assert(0 == p_which_sv_); which_sv_[i] = x; }
    // void set_ismu(int i, uchar x) {assert(0 == p_ismu_); ismu_[i] = x; }
    // void set_isel(int i, uchar x) {assert(0 == p_isel_); isel_[i] = x; }
    
    void set_misc(int i, unsigned x) { assert(0 == p_misc_); misc_[i] = x; }

    int q(int i) const { return qpt(i) > 0 ? 1 : -1; }
    float pt(int i) const { return std::abs(qpt(i)); }
    float px(int i) const { return p3(i).X(); }
    float py(int i) const { return p3(i).Y(); }
    float pz(int i) const { return p3(i).Z(); }
    float p(int i) const { return p3(i).Mag(); }
    float p2(int i) const { return p3(i).Mag2(); }
    TVector3 v(int i) const { return TVector3(vx(i), vy(i), vz(i)); }
    float dxy(int i, float x=0, float y=0) const { return ((vy(i) - y) * px(i) - (vx(i) - x) * py(i)) / pt(i); }
    template <typename BS> float dxybs(int i, const BS& bs) const { return dxy(i, bs.x(vz(i)), bs.y(vz(i))); }
    template <typename BS> float nsigmadxybs(int i, const BS& bs) const { return std::abs(dxybs(i, bs) / err_dxy(i)); }
    template <typename PV> float dxypv(int i, const PV& pv, int j=0) const { return dxy(i, pv.x(j), pv.y(j)); }
    float dz(int i, float x=0, float y=0, float z=0) const { return (vz(i) - z) - ((vx(i) - x) * px(i) + (vy(i) - y) * py(i)) / pt(i) * pz(i) / pt(i); }
    template <typename PV> float dzpv(int i, const PV& pv, int j=0) const { return dz(i, pv.x(j), pv.y(j), pv.z(j)); }
    float dsz(int i, float x=0, float y=0, float z=0) const { return (vz(i) - z) * pt(i) / p(i) - ((vx(i) - x) * px(i) + (vy(i) - y) * py(i)) / pt(i) * pz(i) / p(i); }
    float cov(int i, int j, int k) const {
      if (j > k) { j = j^k; k = j^k; j = j^k; }
      switch (j*10 + k) {
      case 00: return cov_00(i);
      case 11: return cov_11(i);
      case 14: return cov_14(i);
      case 22: return cov_22(i);
      case 23: return cov_23(i);
      case 33: return cov_33(i);
      case 34: return cov_34(i);
      case 44: return cov_44(i);
      default: return 0.f;
      }
    }
    float err_pt(int i) const { return sqrt(cov_00(i) * pt(i) * pt(i) * p2(i) / q(i) / q(i) + cov_11(i) * pz(i) * pz(i)); } // + cov(i,0,1) * 2 * pt(i) * p(i) / q(i) * pz(i)); }
    float err_pt_rel(int i) const { return err_pt(i) / pt(i); }
    float err_eta(int i) const { return sqrt(cov_11(i) * p2(i)) / pt(i); }
    float err_phi(int i) const { return sqrt(cov_22(i)); }
    float err_dxy(int i) const { return sqrt(cov_33(i)); }
    float err_dz(int i) const { return sqrt(cov_44(i) * p2(i)) / pt(i); }
    float err_dsz(int i) const { return sqrt(cov_44(i)); }
    float err_lambda(int i) const { return sqrt(cov_11(i)); }
    int npxhits(int i) const { return hp(i) & 0xf; }
    int nsthits(int i) const { return (hp(i) >> 4) & 0x1f; }
    int npxlayers(int i) const { return (hp(i) >> 9) & 0xf; }
    int nstlayers(int i) const { return (hp(i) >> 13) & 0x1f; }
    int nhits(int i) const { return npxhits(i) + nsthits(i); }
    int nlayers(int i) const { return npxlayers(i) + nstlayers(i); }
    int min_r(int i) const { return minhit(i) & 0xF; }
    int min_z(int i) const { return minhit(i) >> 4; }
    int max_r(int i) const { return maxhit(i) & 0xF; }
    int max_z(int i) const { return maxhit(i) >> 4; }
    int maxpx_r(int i) const { return maxpxhit(i) & 0xF; }
    int maxpx_z(int i) const { return maxpxhit(i) >> 4; }
    TVector3 p3(int i) const { return p3_(pt(i), eta(i), phi(i)); }
    TLorentzVector p4(int i, double m=0) const { return p4_m(pt(i), eta(i), phi(i), m); }
    bool pass_sel(int i) const { return pt(i) > 1 && min_r(i) <= 1 && npxlayers(i) >= 2 && nstlayers(i) >= 6; }
    template <typename BS> bool pass_seed(int i, const BS& bs, float ns=4) const { return pass_sel(i) && nsigmadxybs(i,bs) > ns; }
    int nsel() const { int c = 0; for (int i = 0, ie = n(); i < ie; ++i) if (pass_sel(i)) ++c; return c; }
    template <typename BS> int nseed(const BS& bs) const { int c = 0; for (int i = 0, ie = n(); i < ie; ++i) if (pass_seed(i, bs)) ++c; return c; }

    std::vector<int> tks_for_jet(uchar i) const { return tks_for_x_(0, i); }
    std::vector<int> tks_for_pv (uchar i) const { return tks_for_x_(1, i); }
    std::vector<int> tks_for_sv (uchar i) const { return tks_for_x_(2, i); }
         
  private:
    std::vector<int> tks_for_x_(int wi, uchar i) const {
      std::vector<int> v;
      for (int j = 0, je = n(); j < je; ++j)
        if ((wi == 0 && which_jet(j) == i) ||
            (wi == 1 && which_pv (j) == i) || 
	    (wi == 2 && which_sv (j) == i))
	  
	  v.push_back(j);
      return v;
    }

    vfloat qpt_;         vfloat* p_qpt_;
    vfloat eta_;         vfloat* p_eta_;
    vfloat phi_;         vfloat* p_phi_;
    vfloat vx_;          vfloat* p_vx_;
    vfloat vy_;          vfloat* p_vy_;
    vfloat vz_;          vfloat* p_vz_;
    vfloat cov_00_;      vfloat* p_cov_00_;
    vfloat cov_11_;      vfloat* p_cov_11_;
    vfloat cov_14_;      vfloat* p_cov_14_;
    vfloat cov_22_;      vfloat* p_cov_22_;
    vfloat cov_23_;      vfloat* p_cov_23_;
    vfloat cov_33_;      vfloat* p_cov_33_;
    vfloat cov_34_;      vfloat* p_cov_34_;
    vfloat cov_44_;      vfloat* p_cov_44_;
    vfloat chi2dof_;     vfloat* p_chi2dof_;
    vunsigned hp_;       vunsigned* p_hp_;
    vuchar minhit_;      vuchar* p_minhit_;
    vuchar maxhit_;      vuchar* p_maxhit_;
    vuchar maxpxhit_;    vuchar* p_maxpxhit_;
    vuchar which_jet_;   vuchar* p_which_jet_;
    vuchar which_pv_;    vuchar* p_which_pv_;
    vuchar which_sv_;    vuchar* p_which_sv_;
    vbool  ismu_;        vbool* p_ismu_;
    vbool  isel_;        vbool* p_isel_;
    vbool  isgoodmu_;        vbool* p_isgoodmu_;
    vbool  isgoodel_;        vbool* p_isgoodel_;
    vunsigned misc_;     vunsigned* p_misc_;
  };

  class RefitTracksSubNtuple : public TracksSubNtuple { public: RefitTracksSubNtuple  () { set_pfx("rftk"); }};

  ////

  class JetsSubNtuple : public INtuple {
  public:
    JetsSubNtuple();
    virtual void clear();
    virtual void write_to_tree(TTree*);
    virtual void read_from_tree(TTree*);
    virtual void copy_vectors();

    void add(float pt, float eta, float phi, float energy, float uncorr, uchar ntracks, float bdisc, uchar genflavor, unsigned misc) {
      pt_.push_back(pt);
      eta_.push_back(eta);
      phi_.push_back(phi);
      energy_.push_back(energy);
      uncorr_.push_back(uncorr);
      ntracks_.push_back(ntracks);
      bdisc_.push_back(bdisc);
      genflavor_.push_back(genflavor);
      misc_.push_back(misc);
    }

    virtual int n() const { return p_size(pt_, p_pt_); }
    float pt        (int i) const { return p_get(i, pt_,        p_pt_);        }
    float eta       (int i) const { return p_get(i, eta_,       p_eta_);       }
    float phi       (int i) const { return p_get(i, phi_,       p_phi_);       }
    float energy    (int i) const { return p_get(i, energy_,    p_energy_);    }
    float uncorr    (int i) const { return p_get(i, uncorr_,    p_uncorr_);    }
    uchar ntracks   (int i) const { return p_get(i, ntracks_,   p_ntracks_);   }
    float bdisc     (int i) const { return p_get(i, bdisc_,     p_bdisc_);     }
    uchar genflavor (int i) const { return p_get(i, genflavor_, p_genflavor_); }
    unsigned misc   (int i) const { return p_get(i, misc_,      p_misc_);      }

    void set_misc(int i, unsigned x) { assert(0 == p_misc_); misc_[i] = x; }

    vfloat::const_iterator pt_begin() const { return p_pt_ ? p_pt_->begin() : pt_.begin(); }
    vfloat::const_iterator pt_end()   const { return p_pt_ ? p_pt_->end()   : pt_.end();   }
    int nminpt(float minpt=20.f) const { return std::count_if(pt_begin(), pt_end(), [minpt](float pt) { return pt > minpt; }); }
    float ht(float minpt=40.f) const { return std::accumulate(pt_begin(), pt_end(), 0.f, [minpt](float init, float pt) { if (pt > minpt) init += pt; return init; }); }
    TVector3 p3(int i) const { return p3_(pt(i), eta(i), phi(i)); }
    TLorentzVector p4(int i) const { return p4_e(pt(i), eta(i), phi(i), energy(i)); }
    std::vector<bool> btagged(float d) const {
      std::vector<bool> r(n(), false);
      for (int i = 0, ie = n(); i < ie; ++i)
        if (bdisc(i) > d)
          r[i] = true;
      return r;
    }
    int nbtags(float d) const {
      int c = 0;
      for (int i = 0, ie = n(); i < ie; ++i)
        if (bdisc(i) > d)
          ++c;
      return c;
    }

  private:
    vfloat pt_;          vfloat* p_pt_;
    vfloat eta_;         vfloat* p_eta_;
    vfloat phi_;         vfloat* p_phi_;
    vfloat energy_;      vfloat* p_energy_;
    vfloat uncorr_;      vfloat* p_uncorr_;
    vuchar ntracks_;     vuchar* p_ntracks_;
    vfloat bdisc_;       vfloat* p_bdisc_;
    vuchar genflavor_;   vuchar* p_genflavor_;
    vunsigned misc_;     vunsigned* p_misc_;
  };

  ////

  class PFSubNtuple : public INtuple {
  public:
    PFSubNtuple();
    virtual void clear();
    virtual void write_to_tree(TTree*);
    virtual void read_from_tree(TTree*);
    virtual void copy_vectors() {}

    void set(float met_x, float met_y) {
      met_x_ = met_x;
      met_y_ = met_y;
    }

    float met_x() const { return met_x_; }
    float met_y() const { return met_y_; }

    float met_phi() const { return std::atan2(met_y(), met_x()); }
    float met()     const { return std::hypot(met_y(), met_x()); }

  private:
    float met_x_;
    float met_y_;
  };

  class MuonsSubNtuple : public INtuple {
  public:
    MuonsSubNtuple();
    virtual void clear();
    virtual void write_to_tree(TTree*);
    virtual void read_from_tree(TTree*);
    virtual void copy_vectors();

 
    void add(int q, float pt, float eta, float phi, bool isLoose, bool isMed, bool isTight, float iso,
	     float vx, float vy, float vz,
             float cov_00, float cov_11, float cov_14, float cov_22, float cov_23, float cov_33, float cov_34, float cov_44,
             float chi2dof,
	     int npxh, int nsth, int npxl, int nstl,
             int minhit_r, int minhit_z, int maxhit_r, int maxhit_z, int maxpxhit_r, int maxpxhit_z) {
      qpt_.push_back(q*pt);
      eta_.push_back(eta);
      phi_.push_back(phi);
      isLoose_.push_back(isLoose);
      isMed_.push_back(isMed);
      isTight_.push_back(isTight);
      iso_.push_back(iso);
      vx_.push_back(vx);
      vy_.push_back(vy);
      vz_.push_back(vz);
      cov_00_.push_back(cov_00);
      cov_11_.push_back(cov_11);
      cov_14_.push_back(cov_14);
      cov_22_.push_back(cov_22);
      cov_23_.push_back(cov_23);
      cov_33_.push_back(cov_33);
      cov_34_.push_back(cov_34);
      cov_44_.push_back(cov_44);
      chi2dof_.push_back(chi2dof);

      assert(npxh >= 0 && nsth >= 0 && npxl >= 0 && nstl >= 0);
      if (npxh > 15) npxh = 15;
      if (nsth > 31) nsth = 31;
      if (npxl > 15) npxl = 15;
      if (nstl > 31) nstl = 31;
      hp_.push_back((nstl << 13) | (npxl << 9) | (nsth << 4) | npxh);
      assert(minhit_r >= 0 && minhit_r <= 15);
      assert(minhit_z >= 0 && minhit_z <= 15);
      minhit_.push_back((uchar(minhit_z) << 4) | uchar(minhit_r));
      assert(maxhit_r >= 0 && maxhit_r <= 15);
      assert(maxhit_z >= 0 && maxhit_z <= 15);
      maxhit_.push_back((uchar(maxhit_z) << 4) | uchar(maxhit_r));
      assert(maxpxhit_r >= 0 && maxpxhit_r <= 15);
      assert(maxpxhit_z >= 0 && maxpxhit_z <= 15);
      maxpxhit_.push_back((uchar(maxpxhit_z) << 4) | uchar(maxpxhit_r));
    }
    
    virtual int n() const { return p_size(qpt_, p_qpt_); }
    float    qpt      (int i) const { return p_get(i, qpt_,       p_qpt_       ); }
    float    eta      (int i) const { return p_get(i, eta_,       p_eta_       ); }
    float    phi      (int i) const { return p_get(i, phi_,       p_phi_       ); }
    bool     isLoose  (int i) const { return p_get(i, isLoose_,   p_isLoose_   ); }
    bool     isMed    (int i) const { return p_get(i, isMed_,     p_isMed_     ); }
    bool     isTight  (int i) const { return p_get(i, isTight_,   p_isTight_   ); }
    float    iso      (int i) const { return p_get(i, iso_,       p_iso_       ); }
    float    vx       (int i) const { return p_get(i, vx_,        p_vx_        ); }
    float    vy       (int i) const { return p_get(i, vy_,        p_vy_        ); }
    float    vz       (int i) const { return p_get(i, vz_,        p_vz_        ); }
    float    cov_00   (int i) const { return p_get(i, cov_00_,    p_cov_00_    ); }
    float    cov_11   (int i) const { return p_get(i, cov_11_,    p_cov_11_    ); }
    float    cov_14   (int i) const { return p_get(i, cov_14_,    p_cov_14_    ); }
    float    cov_22   (int i) const { return p_get(i, cov_22_,    p_cov_22_    ); }
    float    cov_23   (int i) const { return p_get(i, cov_23_,    p_cov_23_    ); }
    virtual float cov_33 (int i) const { return p_get(i, cov_33_, p_cov_33_ ); }
    virtual float cov_34 (int i) const { return p_get(i, cov_34_, p_cov_34_ ); }
    virtual float cov_44 (int i) const { return p_get(i, cov_44_, p_cov_44_ ); }
    float    chi2dof  (int i) const { return p_get(i, chi2dof_,   p_chi2dof_   ); }
    unsigned hp       (int i) const { return p_get(i, hp_,        p_hp_        ); }
    uchar    minhit   (int i) const { return p_get(i, minhit_,    p_minhit_    ); }
    uchar    maxhit   (int i) const { return p_get(i, maxhit_,    p_maxhit_    ); }
    uchar    maxpxhit (int i) const { return p_get(i, maxpxhit_,  p_maxpxhit_  ); }

    int q(int i) const { return qpt(i) > 0 ? 1 : -1; }
    float pt(int i) const { return std::abs(qpt(i)); }
    float px(int i) const { return p3(i).X(); }
    float py(int i) const { return p3(i).Y(); }
    float pz(int i) const { return p3(i).Z(); }
    float p(int i) const { return p3(i).Mag(); }
    float p2(int i) const { return p3(i).Mag2(); }
    TVector3 v(int i) const { return TVector3(vx(i), vy(i), vz(i)); }
    float dxy(int i, float x=0, float y=0) const { return ((vy(i) - y) * px(i) - (vx(i) - x) * py(i)) / pt(i); }
    template <typename BS> float dxybs(int i, const BS& bs) const { return dxy(i, bs.x(vz(i)), bs.y(vz(i))); }
    template <typename BS> float nsigmadxybs(int i, const BS& bs) const { return std::abs(dxybs(i, bs) / err_dxy(i)); }
    float cov(int i, int j, int k) const {
      if (j > k) { j = j^k; k = j^k; j = j^k; }
      switch (j*10 + k) {
      case 00: return cov_00(i);
      case 11: return cov_11(i);
      case 14: return cov_14(i);
      case 22: return cov_22(i);
      case 23: return cov_23(i);
      case 33: return cov_33(i);
      case 34: return cov_34(i);
      case 44: return cov_44(i);
      default: return 0.f;
      }
    }
    float err_pt(int i) const { return sqrt(cov_00(i) * pt(i) * pt(i) * p2(i) / q(i) / q(i) + cov_11(i) * pz(i) * pz(i)); } // + cov(i,0,1) * 2 * pt(i) * p(i) / q(i) * pz(i)); }
    float err_pt_rel(int i) const { return err_pt(i) / pt(i); }
    float err_eta(int i) const { return sqrt(cov_11(i) * p2(i)) / pt(i); }
    float err_phi(int i) const { return sqrt(cov_22(i)); }
    float err_dxy(int i) const { return sqrt(cov_33(i)); }
    float err_dz(int i) const { return sqrt(cov_44(i) * p2(i)) / pt(i); }
    float err_dsz(int i) const { return sqrt(cov_44(i)); }
    float err_lambda(int i) const { return sqrt(cov_11(i)); }
    int npxhits(int i) const { return hp(i) & 0xf; }
    int nsthits(int i) const { return (hp(i) >> 4) & 0x1f; }
    int npxlayers(int i) const { return (hp(i) >> 9) & 0xf; }
    int nstlayers(int i) const { return (hp(i) >> 13) & 0x1f; }
    int nhits(int i) const { return npxhits(i) + nsthits(i); }
    int nlayers(int i) const { return npxlayers(i) + nstlayers(i); }
    int min_r(int i) const { return minhit(i) & 0xF; }
    int min_z(int i) const { return minhit(i) >> 4; }
    int max_r(int i) const { return maxhit(i) & 0xF; }
    int max_z(int i) const { return maxhit(i) >> 4; }
    int maxpx_r(int i) const { return maxpxhit(i) & 0xF; }
    int maxpx_z(int i) const { return maxpxhit(i) >> 4; }
    TVector3 p3(int i) const { return p3_(pt(i), eta(i), phi(i)); }
    TLorentzVector p4(int i, double m=0) const { return p4_m(pt(i), eta(i), phi(i), m); }
    bool pass_sel(int i) const { return pt(i) > 1 && min_r(i) <= 1 && npxlayers(i) >= 2 && nstlayers(i) >= 6; }
    
  private:
    vfloat qpt_;         vfloat* p_qpt_;
    vfloat eta_;         vfloat* p_eta_;
    vfloat phi_;         vfloat* p_phi_;
    vbool  isLoose_;     vbool* p_isLoose_;
    vbool  isMed_;       vbool* p_isMed_;
    vbool  isTight_;     vbool* p_isTight_;
    vfloat iso_;         vfloat* p_iso_;
    vfloat vx_;          vfloat* p_vx_;
    vfloat vy_;          vfloat* p_vy_;
    vfloat vz_;          vfloat* p_vz_;
    vfloat cov_00_;      vfloat* p_cov_00_;
    vfloat cov_11_;      vfloat* p_cov_11_;
    vfloat cov_14_;      vfloat* p_cov_14_;
    vfloat cov_22_;      vfloat* p_cov_22_;
    vfloat cov_23_;      vfloat* p_cov_23_;
    vfloat cov_33_;      vfloat* p_cov_33_;
    vfloat cov_34_;      vfloat* p_cov_34_;
    vfloat cov_44_;      vfloat* p_cov_44_;
    vfloat chi2dof_;     vfloat* p_chi2dof_;
    vunsigned hp_;       vunsigned* p_hp_;
    vuchar minhit_;      vuchar* p_minhit_;
    vuchar maxhit_;      vuchar* p_maxhit_;
    vuchar maxpxhit_;    vuchar* p_maxpxhit_;
  };
  
  class ElectronsSubNtuple : public INtuple {
  public:
    ElectronsSubNtuple();
    virtual void clear();
    virtual void write_to_tree(TTree*);
    virtual void read_from_tree(TTree*);
    virtual void copy_vectors();
    
    void add(int q, float pt, float eta, float phi, bool isVeto, bool isLoose, bool isMed, bool isTight, float iso, bool passveto,
	     float vx, float vy, float vz,
             float cov_00, float cov_11, float cov_14, float cov_22, float cov_23, float cov_33, float cov_34, float cov_44,
             float chi2dof,
	     int npxh, int nsth, int npxl, int nstl,
             int minhit_r, int minhit_z, int maxhit_r, int maxhit_z, int maxpxhit_r, int maxpxhit_z) {
      qpt_.push_back(q*pt);
      eta_.push_back(eta);
      phi_.push_back(phi);
      isVeto_.push_back(isVeto);
      isLoose_.push_back(isLoose);
      isMed_.push_back(isMed);
      isTight_.push_back(isTight);
      iso_.push_back(iso);
      passveto_.push_back(passveto);
      vx_.push_back(vx);
      vy_.push_back(vy);
      vz_.push_back(vz);
      cov_00_.push_back(cov_00);
      cov_11_.push_back(cov_11);
      cov_14_.push_back(cov_14);
      cov_22_.push_back(cov_22);
      cov_23_.push_back(cov_23);
      cov_33_.push_back(cov_33);
      cov_34_.push_back(cov_34);
      cov_44_.push_back(cov_44);
      chi2dof_.push_back(chi2dof);

      assert(npxh >= 0 && nsth >= 0 && npxl >= 0 && nstl >= 0);
      if (npxh > 15) npxh = 15;
      if (nsth > 31) nsth = 31;
      if (npxl > 15) npxl = 15;
      if (nstl > 31) nstl = 31;
      hp_.push_back((nstl << 13) | (npxl << 9) | (nsth << 4) | npxh);
      assert(minhit_r >= 0 && minhit_r <= 15);
      assert(minhit_z >= 0 && minhit_z <= 15);
      minhit_.push_back((uchar(minhit_z) << 4) | uchar(minhit_r));
      assert(maxhit_r >= 0 && maxhit_r <= 15);
      assert(maxhit_z >= 0 && maxhit_z <= 15);
      maxhit_.push_back((uchar(maxhit_z) << 4) | uchar(maxhit_r));
      assert(maxpxhit_r >= 0 && maxpxhit_r <= 15);
      assert(maxpxhit_z >= 0 && maxpxhit_z <= 15);
      maxpxhit_.push_back((uchar(maxpxhit_z) << 4) | uchar(maxpxhit_r));
    }
    
    virtual int n() const { return p_size(qpt_, p_qpt_); }
    float    qpt      (int i) const { return p_get(i, qpt_,       p_qpt_       ); }
    float    eta      (int i) const { return p_get(i, eta_,       p_eta_       ); }
    float    phi      (int i) const { return p_get(i, phi_,       p_phi_       ); }
    bool     isVeto   (int i) const { return p_get(i, isVeto_,    p_isVeto_    ); }
    bool     isLoose  (int i) const { return p_get(i, isLoose_,   p_isLoose_   ); }
    bool     isMed    (int i) const { return p_get(i, isMed_,     p_isMed_     ); }
    bool     isTight  (int i) const { return p_get(i, isTight_,   p_isTight_   ); }
    float    iso      (int i) const { return p_get(i, iso_,       p_iso_       ); }
    bool     passveto (int i) const { return p_get(i, passveto_,  p_passveto_  ); }
    float    vx       (int i) const { return p_get(i, vx_,        p_vx_        ); }
    float    vy       (int i) const { return p_get(i, vy_,        p_vy_        ); }
    float    vz       (int i) const { return p_get(i, vz_,        p_vz_        ); }
    float    cov_00   (int i) const { return p_get(i, cov_00_,    p_cov_00_    ); }
    float    cov_11   (int i) const { return p_get(i, cov_11_,    p_cov_11_    ); }
    float    cov_14   (int i) const { return p_get(i, cov_14_,    p_cov_14_    ); }
    float    cov_22   (int i) const { return p_get(i, cov_22_,    p_cov_22_    ); }
    float    cov_23   (int i) const { return p_get(i, cov_23_,    p_cov_23_    ); }
    virtual float cov_33 (int i) const { return p_get(i, cov_33_, p_cov_33_ ); }
    virtual float cov_34 (int i) const { return p_get(i, cov_34_, p_cov_34_ ); }
    virtual float cov_44 (int i) const { return p_get(i, cov_44_, p_cov_44_ ); }
    float    chi2dof  (int i) const { return p_get(i, chi2dof_,   p_chi2dof_   ); }
    unsigned hp       (int i) const { return p_get(i, hp_,        p_hp_        ); }
    uchar    minhit   (int i) const { return p_get(i, minhit_,    p_minhit_    ); }
    uchar    maxhit   (int i) const { return p_get(i, maxhit_,    p_maxhit_    ); }
    uchar    maxpxhit (int i) const { return p_get(i, maxpxhit_,  p_maxpxhit_  ); }

    int q(int i) const { return qpt(i) > 0 ? 1 : -1; }
    float pt(int i) const { return std::abs(qpt(i)); }
    float px(int i) const { return p3(i).X(); }
    float py(int i) const { return p3(i).Y(); }
    float pz(int i) const { return p3(i).Z(); }
    float p(int i) const { return p3(i).Mag(); }
    float p2(int i) const { return p3(i).Mag2(); }
    TVector3 v(int i) const { return TVector3(vx(i), vy(i), vz(i)); }
    float dxy(int i, float x=0, float y=0) const { return ((vy(i) - y) * px(i) - (vx(i) - x) * py(i)) / pt(i); }
    template <typename BS> float dxybs(int i, const BS& bs) const { return dxy(i, bs.x(vz(i)), bs.y(vz(i))); }
    template <typename BS> float nsigmadxybs(int i, const BS& bs) const { return std::abs(dxybs(i, bs) / err_dxy(i)); }
    float cov(int i, int j, int k) const {
      if (j > k) { j = j^k; k = j^k; j = j^k; }
      switch (j*10 + k) {
      case 00: return cov_00(i);
      case 11: return cov_11(i);
      case 14: return cov_14(i);
      case 22: return cov_22(i);
      case 23: return cov_23(i);
      case 33: return cov_33(i);
      case 34: return cov_34(i);
      case 44: return cov_44(i);
      default: return 0.f;
      }
    }
    float err_pt(int i) const { return sqrt(cov_00(i) * pt(i) * pt(i) * p2(i) / q(i) / q(i) + cov_11(i) * pz(i) * pz(i)); } // + cov(i,0,1) * 2 * pt(i) * p(i) / q(i) * pz(i)); }
    float err_pt_rel(int i) const { return err_pt(i) / pt(i); }
    float err_eta(int i) const { return sqrt(cov_11(i) * p2(i)) / pt(i); }
    float err_phi(int i) const { return sqrt(cov_22(i)); }
    float err_dxy(int i) const { return sqrt(cov_33(i)); }
    float err_dz(int i) const { return sqrt(cov_44(i) * p2(i)) / pt(i); }
    float err_dsz(int i) const { return sqrt(cov_44(i)); }
    float err_lambda(int i) const { return sqrt(cov_11(i)); }
    int npxhits(int i) const { return hp(i) & 0xf; }
    int nsthits(int i) const { return (hp(i) >> 4) & 0x1f; }
    int npxlayers(int i) const { return (hp(i) >> 9) & 0xf; }
    int nstlayers(int i) const { return (hp(i) >> 13) & 0x1f; }
    int nhits(int i) const { return npxhits(i) + nsthits(i); }
    int nlayers(int i) const { return npxlayers(i) + nstlayers(i); }
    int min_r(int i) const { return minhit(i) & 0xF; }
    int min_z(int i) const { return minhit(i) >> 4; }
    int max_r(int i) const { return maxhit(i) & 0xF; }
    int max_z(int i) const { return maxhit(i) >> 4; }
    int maxpx_r(int i) const { return maxpxhit(i) & 0xF; }
    int maxpx_z(int i) const { return maxpxhit(i) >> 4; }
    TVector3 p3(int i) const { return p3_(pt(i), eta(i), phi(i)); }
    TLorentzVector p4(int i, double m=0) const { return p4_m(pt(i), eta(i), phi(i), m); }
    bool pass_sel(int i) const { return pt(i) > 1 && min_r(i) <= 1 && npxlayers(i) >= 2 && nstlayers(i) >= 6; }
    
  private:
    vfloat qpt_;         vfloat* p_qpt_;
    vfloat eta_;         vfloat* p_eta_;
    vfloat phi_;         vfloat* p_phi_;
    vbool isVeto_;       vbool* p_isVeto_;
    vbool isLoose_;      vbool* p_isLoose_;
    vbool isMed_;        vbool* p_isMed_;
    vbool isTight_;      vbool* p_isTight_;
    vfloat iso_;         vfloat* p_iso_;
    vbool passveto_;     vbool* p_passveto_;
    vfloat vx_;          vfloat* p_vx_;
    vfloat vy_;          vfloat* p_vy_;
    vfloat vz_;          vfloat* p_vz_;
    vfloat cov_00_;      vfloat* p_cov_00_;
    vfloat cov_11_;      vfloat* p_cov_11_;
    vfloat cov_14_;      vfloat* p_cov_14_;
    vfloat cov_22_;      vfloat* p_cov_22_;
    vfloat cov_23_;      vfloat* p_cov_23_;
    vfloat cov_33_;      vfloat* p_cov_33_;
    vfloat cov_34_;      vfloat* p_cov_34_;
    vfloat cov_44_;      vfloat* p_cov_44_;
    vfloat chi2dof_;     vfloat* p_chi2dof_;
    vunsigned hp_;       vunsigned* p_hp_;
    vuchar minhit_;      vuchar* p_minhit_;
    vuchar maxhit_;      vuchar* p_maxhit_;
    vuchar maxpxhit_;    vuchar* p_maxpxhit_;
    
  };


  class TrackingNtuple : public INtuple {
  public:
    TrackingNtuple() { clear(); }

    virtual void clear() {
      base().clear();
      bs().clear();
      pvs().clear();
      tracks().clear();
    }

    virtual void write_to_tree(TTree* t) {
      base().write_to_tree(t);
      bs().write_to_tree(t);
      pvs().write_to_tree(t);
      tracks().write_to_tree(t);
    }

    virtual void read_from_tree(TTree* t) {
      base().read_from_tree(t);
      bs().read_from_tree(t);
      pvs().read_from_tree(t);
      tracks().read_from_tree(t);
    }

    virtual void copy_vectors() {
      base().copy_vectors();
      bs().copy_vectors();
      pvs().copy_vectors();
      tracks().copy_vectors();
    }

    BaseSubNtuple& base() { return base_; }
    BeamspotSubNtuple& bs() { return bs_; }
    PrimaryVerticesSubNtuple& pvs() { return pvs_; }
    TracksSubNtuple& tracks() { return tracks_; }
    const BaseSubNtuple& base() const { return base_; }
    const BeamspotSubNtuple& bs() const { return bs_; }
    const PrimaryVerticesSubNtuple& pvs() const { return pvs_; }
    const TracksSubNtuple& tracks() const { return tracks_; }

  private:
    BaseSubNtuple base_;
    BeamspotSubNtuple bs_;
    PrimaryVerticesSubNtuple pvs_;
    TracksSubNtuple tracks_;
  };


  class TrackingAndJetsNtuple : public TrackingNtuple {
  public:
    TrackingAndJetsNtuple() { clear(); }

    virtual void clear() {
      TrackingNtuple::clear();
      jets().clear();
      pf().clear();
      muons().clear();
      electrons().clear();
    }

    virtual void write_to_tree(TTree* t) {
      TrackingNtuple::write_to_tree(t);
      jets().write_to_tree(t);
      pf().write_to_tree(t);
      muons().write_to_tree(t);
      electrons().write_to_tree(t);
    }

    virtual void read_from_tree(TTree* t) {
      TrackingNtuple::read_from_tree(t);
      jets().read_from_tree(t);
      pf().read_from_tree(t);
      muons().read_from_tree(t);
      electrons().read_from_tree(t);
    }

    virtual void copy_vectors() {
      TrackingNtuple::copy_vectors();
      jets().copy_vectors();
      pf().copy_vectors();
      muons().copy_vectors();
      electrons().copy_vectors();
	
    }

    JetsSubNtuple& jets() { return jets_; }
    PFSubNtuple& pf() { return pf_; }
    MuonsSubNtuple& muons() { return muons_; }
    ElectronsSubNtuple& electrons() { return electrons_; }
    const JetsSubNtuple& jets() const { return jets_; }
    const PFSubNtuple& pf() const { return pf_; }
    const MuonsSubNtuple& muons() const { return muons_; }
    const ElectronsSubNtuple& electrons() const { return electrons_; }

  private:
    JetsSubNtuple jets_;
    PFSubNtuple pf_;
    MuonsSubNtuple muons_;
    ElectronsSubNtuple electrons_;
  };
}

#endif
