#ifndef JMTucker_MFVNeutralino_Ntuple_h
#define JMTucker_MFVNeutralino_Ntuple_h

#include "JMTucker/Tools/interface/Ntuple.h"

namespace mfv {
  class GenTruthSubNtuple : public jmt::INtuple {
  public:
    GenTruthSubNtuple();
    virtual void clear();
    virtual void write_to_tree(TTree*);
    virtual void read_from_tree(TTree*);
    virtual void copy_vectors();

    void set(bool valid, float vx, float vy, float vz, bool saw_c, bool saw_b) {
      valid_ = valid;
      vx_ = vx;
      vy_ = vy;
      vz_ = vz;
      saw_c_ = saw_c;
      saw_b_ = saw_b;
    }

    bool valid() const { return valid_; }
    float vx() const { return vx_; }
    float vy() const { return vy_; }
    float vz() const { return vz_; }
    bool saw_c() const { return saw_c_; }
    bool saw_b() const { return saw_b_; }

    TVector3 vertex() const { return TVector3(vx(), vy(), vz()); }
    int flavor_code() const { if (saw_b()) return 2; if (saw_c()) return 1; return 0; }

    void add(int id, float pt, float eta, float phi, float mass, float decay_x, float decay_y, float decay_z) {
      id_.push_back(id);
      pt_.push_back(pt);
      eta_.push_back(eta);
      phi_.push_back(phi);
      mass_.push_back(mass);
      decay_x_.push_back(decay_x);
      decay_y_.push_back(decay_y);
      decay_z_.push_back(decay_z);
    }

    int n() const { return p_size(id_, p_id_); }
    int   id      (int i) const { return p_get(i, id_,       p_id_      ); }
    float pt      (int i) const { return p_get(i, pt_,       p_pt_      ); }
    float eta     (int i) const { return p_get(i, eta_,      p_eta_     ); }
    float phi     (int i) const { return p_get(i, phi_,      p_phi_     ); }
    float mass    (int i) const { return p_get(i, mass_,     p_mass_    ); }
    float decay_x (int i) const { return p_get(i, decay_x_,  p_decay_x_ ); }
    float decay_y (int i) const { return p_get(i, decay_y_,  p_decay_y_ ); }
    float decay_z (int i) const { return p_get(i, decay_z_,  p_decay_z_ ); }

    int ndau() const { return n()-2; }
    TLorentzVector p4(int i) const { return p4_m(pt(i), eta(i), phi(i), mass(i)); }

    TVector3 decay(int i) const { return TVector3(decay_x(i), decay_y(i), decay_z(i)); }
    template <typename BS> TVector3 decay(int i, const BS& bs) const { return TVector3(decay_x(i) - bs.x(decay_z(i)), decay_y(i) - bs.y(decay_z(i)), decay_z(i)); } // JMTBAD BS BS

    float lspdist2() const { return (decay(0) - decay(1)).Perp(); }
    float lspdist3() const { return (decay(0) - decay(1)).Mag(); }
    float lspdistz() const { return std::abs(decay_z(0) - decay_z(1)); }

    void add_bquark(float pt, float eta, float phi) {
      bquark_pt_.push_back(pt);
      bquark_eta_.push_back(eta);
      bquark_phi_.push_back(phi);
    }

    void add_lepton(bool is_el, int q, float pt, float eta, float phi) {
      lepton_is_el_.push_back(is_el);
      lepton_qpt_.push_back(q*pt);
      lepton_eta_.push_back(eta);
      lepton_phi_.push_back(phi);
    }

    int nbquarks() const { return p_size(bquark_pt_, p_bquark_pt_); }
    int nleptons() const { return p_size(lepton_qpt_, p_lepton_qpt_); }
    // JMTBAD

  private:
    bool valid_;
    float vx_;
    float vy_;
    float vz_;
    bool saw_c_;
    bool saw_b_;
    vint   id_;      vint  * p_id_;
    vfloat pt_;      vfloat* p_pt_;
    vfloat eta_;     vfloat* p_eta_;
    vfloat phi_;     vfloat* p_phi_;
    vfloat mass_;    vfloat* p_mass_;
    vfloat decay_x_; vfloat* p_decay_x_;
    vfloat decay_y_; vfloat* p_decay_y_;
    vfloat decay_z_; vfloat* p_decay_z_;
    vfloat bquark_pt_;    vfloat* p_bquark_pt_;
    vfloat bquark_eta_;   vfloat* p_bquark_eta_;
    vfloat bquark_phi_;   vfloat* p_bquark_phi_;
    vbool  lepton_is_el_; vbool * p_lepton_is_el_;
    vfloat lepton_qpt_;   vfloat* p_lepton_qpt_;
    vfloat lepton_eta_;   vfloat* p_lepton_eta_;
    vfloat lepton_phi_;   vfloat* p_lepton_phi_;
  };

  ////

  class VerticesSubNtuple : public jmt::INtuple {
  public:
    VerticesSubNtuple();
    virtual void clear();
    virtual void write_to_tree(TTree*);
    virtual void read_from_tree(TTree*);
    virtual void copy_vectors();

    void add(float x, float y, float z,
             float cxx, float cxy, float cxz, float cyy, float cyz, float czz,
             uchar ntracks, float bs2derr, float geo2ddist, bool genmatch,
             float pt, float eta, float phi, float mass, float tkonlymass) {
      x_.push_back(x);
      y_.push_back(y);
      z_.push_back(z);
      cxx_.push_back(cxx);
      cxy_.push_back(cxy);
      cxz_.push_back(cxz);
      cyy_.push_back(cyy);
      cyz_.push_back(cyz);
      czz_.push_back(czz);
      ntracks_.push_back(ntracks);
      bs2derr_.push_back(bs2derr);
      geo2ddist_.push_back(geo2ddist);
      genmatch_.push_back(genmatch);
      pt_.push_back(pt);
      eta_.push_back(eta);
      phi_.push_back(phi);
      mass_.push_back(mass);
      tkonlymass_.push_back(tkonlymass);
    }

    int n() const { return p_size(x_, p_x_); }
    float x          (int i) const { return p_get(i, x_,          p_x_          ); }
    float y          (int i) const { return p_get(i, y_,          p_y_          ); }
    float z          (int i) const { return p_get(i, z_,          p_z_          ); }
    float cxx        (int i) const { return p_get(i, cxx_,        p_cxx_        ); }
    float cxy        (int i) const { return p_get(i, cxy_,        p_cxy_        ); }
    float cxz        (int i) const { return p_get(i, cxz_,        p_cxz_        ); }
    float cyy        (int i) const { return p_get(i, cyy_,        p_cyy_        ); }
    float cyz        (int i) const { return p_get(i, cyz_,        p_cyz_        ); }
    float czz        (int i) const { return p_get(i, czz_,        p_czz_        ); }
    uchar ntracks    (int i) const { return p_get(i, ntracks_,    p_ntracks_    ); }
    float bs2derr    (int i) const { return p_get(i, bs2derr_,    p_bs2derr_    ); }
    float geo2ddist  (int i) const { return p_get(i, geo2ddist_,  p_geo2ddist_  ); }
    bool  genmatch   (int i) const { return p_get(i, genmatch_,   p_genmatch_   ); }
    float pt         (int i) const { return p_get(i, pt_,         p_pt_         ); }
    float eta        (int i) const { return p_get(i, eta_,        p_eta_        ); }
    float phi        (int i) const { return p_get(i, phi_,        p_phi_        ); }
    float mass       (int i) const { return p_get(i, mass_,       p_mass_       ); }
    float tkonlymass (int i) const { return p_get(i, tkonlymass_, p_tkonlymass_ ); }

    TVector3 pos(int i) const { return TVector3(x(i), y(i), z(i)); }
    float rho(int i) const { return std::hypot(x(i), y(i)); }

  private:
    vfloat x_;           vfloat* p_x_;
    vfloat y_;           vfloat* p_y_;
    vfloat z_;           vfloat* p_z_;
    vfloat cxx_;         vfloat* p_cxx_;
    vfloat cxy_;         vfloat* p_cxy_;
    vfloat cxz_;         vfloat* p_cxz_;
    vfloat cyy_;         vfloat* p_cyy_;
    vfloat cyz_;         vfloat* p_cyz_;
    vfloat czz_;         vfloat* p_czz_;
    vuchar ntracks_;     vuchar* p_ntracks_;
    vfloat bs2derr_;     vfloat* p_bs2derr_;
    vfloat geo2ddist_;   vfloat* p_geo2ddist_;
    vbool  genmatch_;    vbool * p_genmatch_;
    vfloat pt_;          vfloat* p_pt_;
    vfloat eta_;         vfloat* p_eta_;
    vfloat phi_;         vfloat* p_phi_;
    vfloat mass_;        vfloat* p_mass_;
    vfloat tkonlymass_;  vfloat* p_tkonlymass_;
  };

  ////

  class MovedTracksSubNtuple : public jmt::INtuple {
  public:
    MovedTracksSubNtuple();
    virtual void clear();
    virtual void write_to_tree(TTree*);
    virtual void read_from_tree(TTree*);
    virtual void copy_vectors() {}

    void set(ushort nalltracks, uchar nmovedtracks, uchar npreseljets, uchar npreselbjets,
             float move_x, float move_y, float move_z) {
      nalltracks_ = nalltracks;
      nmovedtracks_ = nmovedtracks;
      npreseljets_ = npreseljets;
      npreselbjets_ = npreselbjets;
      move_x_ = move_x;
      move_y_ = move_y;
      move_z_ = move_z;
    }

    ushort nalltracks() const { return nalltracks_; }
    uchar nmovedtracks() const { return nmovedtracks_; }
    uchar npreseljets() const { return npreseljets_; }
    uchar npreselbjets() const { return npreselbjets_; }

    float move_x() const { return move_x_; }
    float move_y() const { return move_y_; }
    float move_z() const { return move_z_; }
    TVector3 move_pos() const { return TVector3(move_x(), move_y(), move_z()); }

  private:
    ushort nalltracks_;
    uchar nmovedtracks_;
    // JMTBAD "presel" on these two really doesn't mean anything other than they have pt > 20 and pass the jet id
    uchar npreseljets_; // JMTBAD this is actually # of jets with bdisc < veto
    uchar npreselbjets_;

    float move_x_;
    float move_y_;
    float move_z_;
  };

  ////

  class MovedTracksNtuple : public jmt::TrackingAndJetsNtuple {
  public:
    MovedTracksNtuple() { clear(); }
    virtual void clear() { jmt::TrackingAndJetsNtuple::clear(); gentruth().clear(); vertices().clear(); tm().clear(); }
    virtual void write_to_tree(TTree* t) { jmt::TrackingAndJetsNtuple::write_to_tree(t); gentruth().write_to_tree(t); vertices().write_to_tree(t); tm().write_to_tree(t); }
    virtual void read_from_tree(TTree* t) { jmt::TrackingAndJetsNtuple::read_from_tree(t); gentruth().read_from_tree(t); vertices().read_from_tree(t); tm().read_from_tree(t); }
    virtual void copy_vectors() { jmt::TrackingAndJetsNtuple::copy_vectors(); gentruth().copy_vectors(); vertices().copy_vectors(); tm().copy_vectors(); }

    GenTruthSubNtuple& gentruth() { return gentruth_; }
    VerticesSubNtuple& vertices() { return vertices_; }
    MovedTracksSubNtuple& tm() { return tm_; }
    const GenTruthSubNtuple& gentruth() const { return gentruth_; }
    const VerticesSubNtuple& vertices() const { return vertices_; }
    const MovedTracksSubNtuple& tm() const { return tm_; }

    static const unsigned b_jet_moved = 0;
    bool jet_moved    (int i) { return test_bit(jets().misc(i), b_jet_moved); }
    void set_jet_moved(int i) { unsigned x = jets().misc(i); set_bit(x, b_jet_moved, 1); jets().set_misc(i,x); }

    static const unsigned b_tk_moved = 0;
    bool tk_moved    (int i) { return test_bit(tracks().misc(i), b_tk_moved); }
    void set_tk_moved(int i) { unsigned x = tracks().misc(i); set_bit(x, b_tk_moved, 1); tracks().set_misc(i,x); }

    TVector3 move_vector() const { return TVector3(tm().move_x() + bs().x(tm().move_z()) - (pvs().x(0) + bs().x(pvs().z(0))),
                                                   tm().move_y() + bs().y(tm().move_z()) - (pvs().y(0) + bs().y(pvs().z(0))),
                                                   tm().move_z() - pvs().z(0)); }
    double move_tau() const { return move_vector().Mag(); }

  private:
    GenTruthSubNtuple gentruth_;
    VerticesSubNtuple vertices_;
    MovedTracksSubNtuple tm_;
  };

  ////

  class K0Ntuple : public jmt::TrackingAndJetsNtuple {
  public:
    K0Ntuple() { clear(); }
    virtual void clear() { jmt::TrackingAndJetsNtuple::clear(); svs().clear(); refit_tks().clear(); }
    virtual void write_to_tree(TTree* t) { jmt::TrackingAndJetsNtuple::write_to_tree(t); svs().write_to_tree(t); refit_tks().write_to_tree(t); }
    virtual void read_from_tree(TTree* t) { jmt::TrackingAndJetsNtuple::read_from_tree(t); svs().read_from_tree(t); refit_tks().read_from_tree(t); }
    virtual void copy_vectors() { jmt::TrackingAndJetsNtuple::copy_vectors(); svs().copy_vectors(); refit_tks().copy_vectors(); }

    jmt::SecondaryVerticesSubNtuple& svs() { return svs_; }
    jmt::RefitTracksSubNtuple& refit_tks() { return refit_tks_; }
    const jmt::SecondaryVerticesSubNtuple& svs() const { return svs_; }
    const jmt::RefitTracksSubNtuple& refit_tks() const { return refit_tks_; }

  private:
    jmt::SecondaryVerticesSubNtuple svs_;
    jmt::RefitTracksSubNtuple refit_tks_;
  };

  ////

  class SplitPVNtuple : public jmt::TrackingAndJetsNtuple {};
}

#endif
