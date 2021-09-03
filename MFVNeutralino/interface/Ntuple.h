#ifndef DVCode_MFVNeutralino_Ntuple_h
#define DVCode_MFVNeutralino_Ntuple_h

#include "DVCode/Tools/interface/Geometry.h"
#include "DVCode/Tools/interface/Ntuple.h"

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

    virtual int n() const { return p_size(id_, p_id_); }
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

    float minlspdist2() const { return valid() ? std::min(decay(0).Perp(), decay(1).Perp()) : -1; }
    float lspdist2() const { return valid() ? (decay(0) - decay(1)).Perp() : -1; }
    float lspdist3() const { return valid() ? (decay(0) - decay(1)).Mag() : -1; }
    float lspdistz() const { return valid() ? std::abs(decay_z(0) - decay_z(1)) : -1; }

    int lspmatch(double x, double y, double z, double d3d=0.0084) {
      if (valid())
        for (int i = 0, ie = std::min(n(), 2); i < ie; ++i)
          if ((decay(i) - TVector3(x,y,z)).Mag2() < d3d*d3d)
            return i;
      return -1;
    }
    template <typename T> int lspmatch(const T& v, double d3d=0.0084) { return lspmatch(v.x, v.y, v.z, d3d); }

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
    float bquark_pt (int i) const { return p_get(i, bquark_pt_,  p_bquark_pt_ ); }
    float bquark_eta(int i) const { return p_get(i, bquark_eta_, p_bquark_eta_); }
    float bquark_phi(int i) const { return p_get(i, bquark_phi_, p_bquark_phi_); }
    int nleptons() const { return p_size(lepton_qpt_, p_lepton_qpt_); }
    // JMTBAD

    TLorentzVector bquark_p4(int i) const { return p4_m(bquark_pt(i), bquark_eta(i), bquark_phi(i), 4.18); }

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

  namespace VertexNm1s {
    enum { nm1_none, nm1_dbv, nm1_edbv, nm1_beampipe, nm1_all, max_nm1 }; // none = regular cuts applied, all = drop all cuts
  }

  class VerticesSubNtuple : public jmt::VerticesSubNtuple {
  public:
    VerticesSubNtuple();
    virtual void clear();
    virtual void write_to_tree(TTree*);
    virtual void read_from_tree(TTree*);
    virtual void copy_vectors();

    void add(float chi2, float x, float y, float z, float cxx, float cxy, float cxz, float cyy, float cyz, float czz,
             float rescale_chi2, float rescale_x, float rescale_y, float rescale_z, float rescale_cxx, float rescale_cxy, float rescale_cxz, float rescale_cyy, float rescale_cyz, float rescale_czz,
             uchar ntracks, uchar njets, float bbs2derr, float rescale_bs2derr, bool genmatch,
             float pt, float eta, float phi, float mass) {
      jmt::VerticesSubNtuple::add(x,y,z, chi2, 2*ntracks-3, ntracks, -1, cxx,cxy,cxz,cyy,cyz,czz, 0);
      rescale_chi2_.push_back(rescale_chi2);
      rescale_x_.push_back(rescale_x);
      rescale_y_.push_back(rescale_y);
      rescale_z_.push_back(rescale_z);
      rescale_cxx_.push_back(rescale_cxx);
      rescale_cxy_.push_back(rescale_cxy);
      rescale_cxz_.push_back(rescale_cxz);
      rescale_cyy_.push_back(rescale_cyy);
      rescale_cyz_.push_back(rescale_cyz);
      rescale_czz_.push_back(rescale_czz);
      njets_.push_back(njets);
      bs2derr_.push_back(bbs2derr);
      rescale_bs2derr_.push_back(rescale_bs2derr);
      genmatch_.push_back(genmatch);
      pt_.push_back(pt);
      eta_.push_back(eta);
      phi_.push_back(phi);
      mass_.push_back(mass);
    }

    float rescale_chi2   (int i) const { return p_get(i, rescale_chi2_, p_rescale_chi2_); }
    float rescale_x      (int i) const { return p_get(i, rescale_x_,    p_rescale_x_   ); }
    float rescale_y      (int i) const { return p_get(i, rescale_y_,    p_rescale_y_   ); }
    float rescale_z      (int i) const { return p_get(i, rescale_z_,    p_rescale_z_   ); }
    float rescale_cxx    (int i) const { return p_get(i, rescale_cxx_,  p_rescale_cxx_ ); }
    float rescale_cxy    (int i) const { return p_get(i, rescale_cxy_,  p_rescale_cxy_ ); }
    float rescale_cxz    (int i) const { return p_get(i, rescale_cxz_,  p_rescale_cxz_ ); }
    float rescale_cyy    (int i) const { return p_get(i, rescale_cyy_,  p_rescale_cyy_ ); }
    float rescale_cyz    (int i) const { return p_get(i, rescale_cyz_,  p_rescale_cyz_ ); }
    float rescale_czz    (int i) const { return p_get(i, rescale_czz_,  p_rescale_czz_ ); }
    uchar njets          (int i) const { return p_get(i, njets_,        p_njets_       ); }
    float bs2derr        (int i) const { return p_get(i, bs2derr_,      p_bs2derr_     ); } // DELME
    float rescale_bs2derr(int i) const { return p_get(i, rescale_bs2derr_, p_rescale_bs2derr_); } // DELME
    bool  genmatch       (int i) const { return p_get(i, genmatch_,     p_genmatch_    ); }
    float pt             (int i) const { return p_get(i, pt_,           p_pt_          ); } // DELME
    float eta            (int i) const { return p_get(i, eta_,          p_eta_         ); } // DELME
    float phi            (int i) const { return p_get(i, phi_,          p_phi_         ); } // DELME
    float mass           (int i) const { return p_get(i, mass_,         p_mass_        ); } // DELME

    template <typename BS> float bs2derr(int i, const BS& bs, bool rescale=false) const {
      float dx = -bs.x(), dy = -bs.y(); // JMTBAD we never used the slope-corrected version
      if (rescale) dx += rescale_x(i), dy += rescale_y(i);
      else         dx +=         x(i), dy +=         y(i);
      if (dx == 0 && dy == 0) return std::numeric_limits<float>::infinity();
      float xx = bs.cxx(), yy = bs.cyy(), xy = bs.cxy();
      if (rescale) xx += rescale_cxx(i), yy += rescale_cyy(i), xy += rescale_cxy(i);
      else         xx +=         cxx(i), yy +=         cyy(i), xy +=         cxy(i);
      return sqrt((xx*dx*dx + yy*dy*dy + 2*xy*dx*dy)/(dx*dx + dy*dy));
    }

    template <typename BS> float dbv(int i, const BS& bs) const { return bs.rho(x(i), y(i), z(i)); }
    float edbv(int i) const { return rescale_bs2derr(i); } // JMTBAD

    template <typename BS> bool pass(int i, const BS& bs, const int min_ntracks=-1, const int max_ntracks=-1,
                                     int nm1=VertexNm1s::nm1_none, const double min_dbv=0.01, const double max_edbv=0.0025) const {
      return
        (min_ntracks < 0 || ntracks(i) >= min_ntracks) &&
        (max_ntracks < 0 || ntracks(i) <= max_ntracks) &&
        (nm1 == VertexNm1s::nm1_all || nm1 == VertexNm1s::nm1_dbv      || dbv(i, bs) > min_dbv) &&
        (nm1 == VertexNm1s::nm1_all || nm1 == VertexNm1s::nm1_edbv     || edbv(i) < max_edbv) &&
        (nm1 == VertexNm1s::nm1_all || nm1 == VertexNm1s::nm1_beampipe || jmt::Geometry::inside_beampipe(x(i), y(i)));
    }

    template <typename BS> std::vector<int> pass(const BS& bs, const int min_ntracks=-1, const int max_ntracks=-1,
                                                 int nm1=VertexNm1s::nm1_none, const double min_dbv=0.01, const double max_edbv=0.0025) const {
      std::vector<int> r;
      for (int i = 0, ie = n(); i < ie; ++i)
        if (pass(i, bs, min_ntracks, max_ntracks, nm1, min_dbv, max_edbv))
          r.push_back(i);
      return r;
    }

    template <typename BS> std::vector<int> npass(const BS& bs, const int min_ntracks=-1, const int max_ntracks=-1,
                                                  int nm1=VertexNm1s::nm1_none, const double min_dbv=0.01, const double max_edbv=0.0025) const {
      return pass(bs, min_ntracks, max_ntracks, nm1, min_dbv, max_edbv).size();
    }

  private:
    vfloat rescale_chi2_;vfloat* p_rescale_chi2_;
    vfloat rescale_x_;   vfloat* p_rescale_x_;
    vfloat rescale_y_;   vfloat* p_rescale_y_;
    vfloat rescale_z_;   vfloat* p_rescale_z_;
    vfloat rescale_cxx_; vfloat* p_rescale_cxx_;
    vfloat rescale_cxy_; vfloat* p_rescale_cxy_;
    vfloat rescale_cxz_; vfloat* p_rescale_cxz_;
    vfloat rescale_cyy_; vfloat* p_rescale_cyy_;
    vfloat rescale_cyz_; vfloat* p_rescale_cyz_;
    vfloat rescale_czz_; vfloat* p_rescale_czz_;
    vuchar njets_;       vuchar* p_njets_;
    vfloat bs2derr_;     vfloat* p_bs2derr_; // drop these two after confirming recalculation
    vfloat rescale_bs2derr_; vfloat* p_rescale_bs2derr_;
    vbool  genmatch_;    vbool * p_genmatch_;
    vfloat pt_;          vfloat* p_pt_; // drop after jet match saved
    vfloat eta_;         vfloat* p_eta_;
    vfloat phi_;         vfloat* p_phi_;
    vfloat mass_;        vfloat* p_mass_;
  };

  ////

  class MiniNtuple2SubNtuple : public jmt::INtuple {
  public:
    MiniNtuple2SubNtuple();
    virtual void clear();
    virtual void write_to_tree(TTree*);
    virtual void read_from_tree(TTree*);
    virtual void copy_vectors() {}

    void set(uchar vcode) {
      vcode_ = vcode;
    }

    uchar vcode() const { return vcode_; }

    static uchar vcode(int n3, int n7, int n4, int n5)  {
      uchar code = 0;
      if (n3 == 1) code |= 0x01;
      if (n3 >= 2) code |= 0x02;
      if (n7 == 1) code |= 0x04;
      if (n7 >= 2) code |= 0x08;
      if (n4 == 1) code |= 0x10;
      if (n4 >= 2) code |= 0x20;
      if (n5 == 1) code |= 0x40;
      if (n5 >= 2) code |= 0x80;
      return code;
    }

  private:
    uchar vcode_;
    // missing: trig bits and floats; leptons (should be a Tools-level SubNtuple)
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

  //////////////////////////////////////////////////////////////////////

  class MiniNtuple2 : public jmt::TrackingAndJetsNtuple {
  public:
    MiniNtuple2() { clear(); }
    virtual void clear() { jmt::TrackingAndJetsNtuple::clear(); gentruth().clear(); vertices().clear(); event().clear(); }
    virtual void write_to_tree(TTree* t) { jmt::TrackingAndJetsNtuple::write_to_tree(t); gentruth().write_to_tree(t); vertices().write_to_tree(t); event().write_to_tree(t); }
    virtual void read_from_tree(TTree* t) { jmt::TrackingAndJetsNtuple::read_from_tree(t); gentruth().read_from_tree(t); vertices().read_from_tree(t); event().read_from_tree(t); }
    virtual void copy_vectors() { jmt::TrackingAndJetsNtuple::copy_vectors(); gentruth().copy_vectors(); vertices().copy_vectors(); event().copy_vectors(); }

    GenTruthSubNtuple& gentruth() { return gentruth_; }
    VerticesSubNtuple& vertices() { return vertices_; }
    MiniNtuple2SubNtuple& event() { return event_; }
    const GenTruthSubNtuple& gentruth() const { return gentruth_; }
    const VerticesSubNtuple& vertices() const { return vertices_; }
    const MiniNtuple2SubNtuple& event() const { return event_; }

    std::vector<int> vertex_tracks(int iv) const {
      const size_t n = vertices().ntracks(iv);
      std::vector<int> t(n, -1);
      size_t z = 0;
      for (int itk = 0, itke = tracks().n(); itk < itke; ++itk)
        if (tracks().which_sv(itk) == iv)
          t[z++] = itk;
      assert(z == n);
      return t;
    }

    std::vector<std::pair<int,int>> vertex_track_pairs(int iv) const {
      std::vector<int> t = vertex_tracks(iv);
      const size_t n = t.size();
      std::vector<std::pair<int,int>> t2(n*(n-1)/2);
      size_t z = 0;
      for (size_t i = 0; i < n-1; ++i)
        for (size_t j = i+1; j < n; ++j)
          t2[z++] = std::make_pair(t[i], t[j]);
      return t2;
    }

    TLorentzVector vertex_tracks_p4(int iv, float mtk=0.13957) const {
      TLorentzVector p4;
      for (int j : vertex_tracks(iv))
        p4 += tracks().p4(j, mtk);
      return p4;
    }

    std::vector<std::pair<int,int>> vertex_tracks_jets(int iv) const {
      std::vector<std::pair<int,int>> r;
      for (int it : vertex_tracks(iv))
        r.push_back(std::make_pair(it, tracks().which_jet(it)));
      return r;
    }

    std::set<int> vertex_jets_raw(int iv) const { // no arbitration of jets to vertices
      std::set<int> r;
      for (std::pair<int,int> p : vertex_tracks_jets(iv))
        if (p.second >= 0 && p.second < 255)
          r.insert(p.second);
      return r;
    }

    std::vector<std::set<int>> vertices_jets() const { // arbitration: assign a jet to the vertex with which it shares the most tracks
      int nv = vertices().n(), nj = jets().n();
      std::vector<int> ntracks(nv * nj, 0);
      for (int iv = 0; iv < nv; ++iv) {
        if (vertices().ntracks(iv) < 3) // JMTBAD
          continue;
        for (auto tj : vertex_tracks_jets(iv))
          if (tj.second >= 0 && tj.second < 255)
            ++ntracks[nv*tj.second + iv];
      }

      std::vector<std::set<int>> r(nv);
      for (int ij = 0; ij < nj; ++ij) {
        int mx = 0, wv = -1;
        for (int iv = 0; iv < nv; ++iv) {
          int ntk = ntracks[nv*ij + iv];
          if (ntk > mx) mx = ntk, wv = iv;
        }
        if (wv != -1) r[wv].insert(ij);
      }

      return r;
    }

    std::set<int> vertex_jets(int iv) const { return vertices_jets()[iv]; }

    TLorentzVector vertex_jets_p4(int iv) const {
      TLorentzVector p4;
      for (int j : vertex_jets(iv))
        p4 += jets().p4(j);
      return p4;
    }

    TLorentzVector vertex_tracks_jets_p4(int iv, const float mtk=0.13957) const {
      TLorentzVector p4;
      std::set<int> js = vertex_jets(iv);
      for (int ij : js)
        p4 += jets().p4(ij);
      for (std::pair<int,int> p : vertex_tracks_jets(iv))
        if (p.second >= 0 && p.second < 255 && js.count(p.second) == 0)
          p4 += tracks().p4(p.first, mtk);
      return p4;
    }

  private:
    GenTruthSubNtuple gentruth_;
    VerticesSubNtuple vertices_;
    MiniNtuple2SubNtuple event_;
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
