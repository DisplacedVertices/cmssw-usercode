#ifndef JMTucker_MFVNeutralino_interface_FlatNtuple_h
#define JMTucker_MFVNeutralino_interface_FlatNtuple_h

#include <numeric>
#include <vector>
#include "TLorentzVector.h"
#include "TTree.h"

namespace mfv {
  struct FlatNtuple {
    typedef unsigned char uchar;
    typedef unsigned short ushort;
    typedef unsigned int uint;

    FlatNtuple() {
      clear();
    }

    void clear() {
      run = lumi = event = 0;
      sample = gen_partons_in_acc = npv = pv_ntracks = nvertices = 0;
      gen_valid = 0;
      for (int i = 0; i < 2; ++i) {
        gen_lsp_pt[i] = gen_lsp_eta[i] = gen_lsp_phi[i] = gen_lsp_mass[i] = 0;
        for (int j = 0; j < 3; ++j)
          gen_lsp_decay[i*3+j] = 0;
        gen_decay_type[i] = 0;
      }
      npu = bsx = bsy = bsz = pvx = pvy = pvz = pv_sumpt2 = metx = mety = metsig = metdphimin = 0;
      jet_id.clear();
      jet_pt.clear();
      jet_eta.clear();
      jet_phi.clear();
      jet_energy.clear();
      lep_id.clear();
      lep_pt.clear();
      lep_eta.clear();
      lep_phi.clear();
      lep_dxy.clear();
      lep_dz.clear();
      lep_iso.clear();
      lep_mva.clear();
      vtx_nmu.clear();
      vtx_nel.clear();
      vtx_x.clear();
      vtx_y.clear();
      vtx_z.clear();
      vtx_cxx.clear();
      vtx_cxy.clear();
      vtx_cxz.clear();
      vtx_cyy.clear();
      vtx_cyz.clear();
      vtx_czz.clear();
      vtx_chi2.clear();
      vtx_ndof.clear();
      vtx_njets.clear();
      vtx_tks_pt.clear();
      vtx_tks_eta.clear();
      vtx_tks_phi.clear();
      vtx_tks_mass.clear();
      vtx_jets_pt.clear();
      vtx_jets_eta.clear();
      vtx_jets_phi.clear();
      vtx_jets_mass.clear();
      vtx_tksjets_pt.clear();
      vtx_tksjets_eta.clear();
      vtx_tksjets_phi.clear();
      vtx_tksjets_mass.clear();
      vtx_jetpairdetamin.clear();
      vtx_jetpairdetamax.clear();
      vtx_jetpairdetaavg.clear();
      vtx_jetpairdetarms.clear();
      vtx_jetpairdrmin.clear();
      vtx_jetpairdrmax.clear();
      vtx_jetpairdravg.clear();
      vtx_jetpairdrrms.clear();
      vtx_costhtkmomvtxdispmin.clear();
      vtx_costhtkmomvtxdispmax.clear();
      vtx_costhtkmomvtxdispavg.clear();
      vtx_costhtkmomvtxdisprms.clear();
      vtx_costhjetmomvtxdispmin.clear();
      vtx_costhjetmomvtxdispmax.clear();
      vtx_costhjetmomvtxdispavg.clear();
      vtx_costhjetmomvtxdisprms.clear();
      vtx_gen2ddist.clear();
      vtx_gen2derr.clear();
      vtx_gen3ddist.clear();
      vtx_gen3derr.clear();
      vtx_bs2dcompatscss.clear();
      vtx_bs2dcompat.clear();
      vtx_bs2ddist.clear();
      vtx_bs2derr.clear();
      vtx_pv2dcompatscss.clear();
      vtx_pv2dcompat.clear();
      vtx_pv2ddist.clear();
      vtx_pv2derr.clear();
      vtx_pv3dcompatscss.clear();
      vtx_pv3dcompat.clear();
      vtx_pv3ddist.clear();
      vtx_pv3derr.clear();
    }

    static TLorentzVector p4(float pt, float eta, float phi, float mass) {
      TLorentzVector v;
      v.SetPtEtaPhiM(pt, eta, phi, mass);
      return v;
    }

    static float min(float x, float y) {
      return x < y ? x : y;
    }

    static float mag(float x, float y) {
      return sqrt(x*x + y*y);
    }

    static float mag(float x, float y, float z) {
      return sqrt(x*x + y*y + z*z);
    }
    
    static float sig(float val, float err) {
      return err <= 0 ? 0 : val/err;
    }

    ////////////////////////////////////////////////////////////////////

    uint run;
    uint lumi;
    uint event;
    uchar sample;

    ////////////////////////////////////////////////////////////////////

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

    ////////////////////////////////////////////////////////////////////

    float npu;

    float bsx;
    float bsy;
    float bsz;

    uchar npv;
    float pvx;
    float pvy;
    float pvz;
    uchar pv_ntracks;
    float pv_sumpt2;
    float pv_rho() const { return mag(pvx - bsx, pvy - bsy); }

    ////////////////////////////////////////////////////////////////////

    std::vector<uchar> jet_id;
    std::vector<float> jet_pt;
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
    float jet_sum_ht() const { return std::accumulate(jet_pt.begin(), jet_pt.end(), 0.f); }

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

    ////////////////////////////////////////////////////////////////////

    float metx;
    float mety;
    float metsig;
    float met() const { return mag(metx, mety); }
    float metphi() const { return atan2(mety, metx); }
    float metdphimin;

    ////////////////////////////////////////////////////////////////////

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

    ////////////////////////////////////////////////////////////////////

    uchar nvertices;

    std::vector<uchar> vtx_nmu;
    std::vector<uchar> vtx_nel;

    std::vector<float> vtx_x;
    std::vector<float> vtx_y;
    std::vector<float> vtx_z;

    std::vector<float> vtx_cxx;
    std::vector<float> vtx_cxy;
    std::vector<float> vtx_cxz;
    std::vector<float> vtx_cyy;
    std::vector<float> vtx_cyz;
    std::vector<float> vtx_czz;

    std::vector<float> vtx_chi2;
    std::vector<float> vtx_ndof;

    std::vector<uchar> vtx_njets;

    std::vector<float> vtx_tks_pt;
    std::vector<float> vtx_tks_eta;
    std::vector<float> vtx_tks_phi;
    std::vector<float> vtx_tks_mass;

    std::vector<float> vtx_jets_pt;
    std::vector<float> vtx_jets_eta;
    std::vector<float> vtx_jets_phi;
    std::vector<float> vtx_jets_mass;

    std::vector<float> vtx_tksjets_pt;
    std::vector<float> vtx_tksjets_eta;
    std::vector<float> vtx_tksjets_phi;
    std::vector<float> vtx_tksjets_mass;

    TLorentzVector vtx_p4(int w, int wmom=0) const {
      if (wmom == 0)
        return p4(vtx_tks_pt[wmom], vtx_tks_eta[wmom], vtx_tks_phi[wmom], vtx_tks_mass[wmom]);
      else if (wmom == 1)
        return p4(vtx_jets_pt[wmom], vtx_jets_eta[wmom], vtx_jets_phi[wmom], vtx_jets_mass[wmom]);
      else if (wmom == 2)
        return p4(vtx_tksjets_pt[wmom], vtx_tksjets_eta[wmom], vtx_tksjets_phi[wmom], vtx_tksjets_mass[wmom]);
    }

    double vtx_betagamma(int w, int wmom=0) const {
      TLorentzVector v = vtx_p4(w, wmom);
      return v.Beta() * v.Gamma();
    }

    std::vector<float> vtx_jetpairdetamin;
    std::vector<float> vtx_jetpairdetamax;
    std::vector<float> vtx_jetpairdetaavg;
    std::vector<float> vtx_jetpairdetarms;

    std::vector<float> vtx_jetpairdrmin;
    std::vector<float> vtx_jetpairdrmax;
    std::vector<float> vtx_jetpairdravg;
    std::vector<float> vtx_jetpairdrrms;

    std::vector<float> vtx_costhtkmomvtxdispmin;
    std::vector<float> vtx_costhtkmomvtxdispmax;
    std::vector<float> vtx_costhtkmomvtxdispavg;
    std::vector<float> vtx_costhtkmomvtxdisprms;

    std::vector<float> vtx_costhjetmomvtxdispmin;
    std::vector<float> vtx_costhjetmomvtxdispmax;
    std::vector<float> vtx_costhjetmomvtxdispavg;
    std::vector<float> vtx_costhjetmomvtxdisprms;

    std::vector<float> vtx_gen2ddist;
    std::vector<float> vtx_gen2derr;
    float vtx_gen2dsig(int w) const { return sig(vtx_gen2ddist[w], vtx_gen2derr[w]); }

    std::vector<float> vtx_gen3ddist;
    std::vector<float> vtx_gen3derr;
    float vtx_gen3dsig(int w) const { return sig(vtx_gen3ddist[w], vtx_gen3derr[w]); }

    std::vector<uchar> vtx_bs2dcompatscss;
    std::vector<float> vtx_bs2dcompat;
    std::vector<float> vtx_bs2ddist;
    std::vector<float> vtx_bs2derr;
    float vtx_bs2dsig(int w) const { return sig(vtx_bs2ddist[w], vtx_bs2derr[w]); }

    std::vector<uchar> vtx_pv2dcompatscss;
    std::vector<float> vtx_pv2dcompat;
    std::vector<float> vtx_pv2ddist;
    std::vector<float> vtx_pv2derr;
    float vtx_pv2dsig(int w) const { return sig(vtx_pv2ddist[w], vtx_pv2derr[w]); }

    std::vector<uchar> vtx_pv3dcompatscss;
    std::vector<float> vtx_pv3dcompat;
    std::vector<float> vtx_pv3ddist;
    std::vector<float> vtx_pv3derr;
    float vtx_pv3dsig(int w) const { return sig(vtx_pv3ddist[w], vtx_pv3derr[w]); }

    float vtx_pvdz(int w) const { return sqrt(vtx_pv3ddist[w]*vtx_pv3ddist[w] - vtx_pv2ddist[w]*vtx_pv2ddist[w]); }
    float vtx_pvdzerr(int w) const {
      // JMTBAD
      float z = vtx_pvdz(w);
      if (z == 0)
        return -1;
      return sqrt(vtx_pv3ddist[w]*vtx_pv3ddist[w]*vtx_pv3derr[w]*vtx_pv3derr[w] + vtx_pv2ddist[w]*vtx_pv2ddist[w]*vtx_pv2derr[w]*vtx_pv2derr[w])/z;
    }
    float vtx_pvdzsig(int w) const { return sig(vtx_pvdz(w), vtx_pvdzerr(w)); }

#if 0
    ////////////////

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
      const size_t n = ntracks();
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

    int ntracks() const {
      return int(track_w.size());
    }

    bool use_track(size_t i) const {
      static const float pt_err_thr = 0.5;
      return track_pt_err[i] / track_pt(i) <= pt_err_thr;
    }

    int nbadtracks() const {
      int c = 0;
      for (size_t i = 0, ie = ntracks(); i < ie; ++i)
        if (!use_track(i))
          ++c;
      return c;
    }

    int ngoodtracks() const {
      return ntracks() - nbadtracks();
    }

    int ntracksptgt(float thr) const {
      int c = 0;
      for (size_t i = 0, ie = ntracks(); i < ie; ++i)
        if (use_track(i) && track_pt(i) > thr)
          ++c;
      return c;
    }

    int trackminnhits() const {
      int m = 255, m2;
      for (size_t i = 0, ie = ntracks(); i < ie; ++i)
        if (use_track(i) && (m2 = track_nhits(i)) < m)
          m = m2;
      return m;
    }

    int trackmaxnhits() const {
      int m = 0, m2;
      for (size_t i = 0, ie = ntracks(); i < ie; ++i)
        if (use_track(i) && (m2 = track_nhits(i)) > m)
          m = m2;
      return m;
    }

    float sumpt2() const {
      float sum = 0;
      for (size_t i = 0, ie = ntracks(); i < ie; ++i)
        if (use_track(i))
          sum += pow(track_pt(i), 2);
      return sum;
    }

    int sumnhitsbehind() const {
      int c = 0;
      for (size_t i = 0, ie = ntracks(); i < ie; ++i)
        if (use_track(i))
          c += track_nhitsbehind(i);
      return c;
    }

    int maxnhitsbehind() const {
      int m = 0, m2;
      for (size_t i = 0, ie = ntracks(); i < ie; ++i)
        if (use_track(i) && (m2 = track_nhitsbehind(i)) > m)
          m = m2;
      return m;
    }

    int ntrackssharedwpv() const {
      int c = 0;
      for (size_t i = 0, ie = ntracks(); i < ie; ++i)
        if (use_track(i) && track_inpv[i] == 0)
          ++c;
      return c;
    }

    int ntrackssharedwpvs() const {
      int c = 0;
      for (size_t i = 0, ie = ntracks(); i < ie; ++i)
        if (use_track(i) && track_inpv[i] >= 0)
          ++c;
      return c;
    }

    std::map<int,int> pvswtracksshared() const {
      std::map<int,int> m;
      for (size_t i = 0, ie = ntracks(); i < ie; ++i)
        if (use_track(i))
          ++m[track_inpv[i]];
      return m;
    }

    int npvswtracksshared() const {
      std::map<int,int> m = pvswtracksshared();
      int c = int(m.size());
      if (m.find(-1) != m.end())
        --c;
      return c;
    }

    int pvmosttracksshared() const {
      std::map<int,int> m = pvswtracksshared();
      int mi = -1, mc = 0;
      for (std::map<int,int>::const_iterator it = m.begin(), ite = m.end(); it != ite; ++it)
        if (it->first != -1 && it->second > mc) {
          mc = it->second;
          mi = it->first;
        }
      return mi;
    }

    float _min(const std::vector<float>& v, const bool filter=true) const {
      float m = 1e99;
      for (size_t i = 0, ie = v.size(); i < ie; ++i)
        if (!filter || use_track(i))
          if (v[i] < m)
            m = v[i];
      return m;
    }

    float _max(const std::vector<float>& v, const bool filter=true) const {
      float m = -1e99;
      for (size_t i = 0, ie = v.size(); i < ie; ++i)
        if (!filter || use_track(i))
          if (v[i] > m)
            m = v[i];
      return m;
    }

    float _avg(const std::vector<float>& v, const bool filter=true) const {
      float a = 0.f;
      int c = 0;
      for (size_t i = 0, ie = v.size(); i < ie; ++i)
        if (!filter || use_track(i)) {
          a += v[i];
          ++c;
        }
      return a / c;
    }

    float _rms(const std::vector<float>& v, const bool filter=true) const {
      if (v.size() == 0) return 0.f;
      float avg = _avg(v, filter);
      std::vector<float> v2;
      for (size_t i = 0, ie = v.size(); i < ie; ++i)
        if (!filter || use_track(i))
          v2.push_back(pow(v[i] - avg, 2));
      return sqrt(std::accumulate(v2.begin(), v2.end(), 0.f)/v2.size());
    }

    struct stats {
      float min, max, avg, rms;
      stats(const MFVVertexAux* a, const std::vector<float>& v, const bool filter=false)
        : min(a->_min(v, filter)),
          max(a->_max(v, filter)),
          avg(a->_avg(v, filter)),
          rms(a->_rms(v, filter))
      {}
    };


    std::vector<float> track_pts() const {
      std::vector<float> pts;
      for (size_t i = 0, ie = ntracks(); i < ie; ++i)
        if (use_track(i))
          pts.push_back(track_pt(i));
      return pts;
    }

    float mintrackpt() const { return _min(track_pts(), false); } // already filtered
    float maxtrackpt() const { return _max(track_pts(), false); }

    float maxmntrackpt(int n) const {
      std::vector<float> pt = track_pts();
      int nt = int(pt.size());
      if (n > nt - 1)
        return -1;
      std::sort(pt.begin(), pt.end());
      return pt[nt-1-n];
    }

    float trackptavg() const { return _avg(track_pts(), false); }
    float trackptrms() const { return _rms(track_pts(), false); }

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

    std::vector<float> trackpairdetas() const {
      std::vector<float> v;
      size_t n = ntracks();
      if (n >= 2)
        for (size_t i = 0, ie = n-1; i < ie; ++i)
          if (use_track(i))
            for (size_t j = i+1, je = n; j < je; ++j)
              if (use_track(j))
                v.push_back(fabs(track_eta[i] - track_eta[j]));
      return v;
    }

    float trackpairdetamin() const { return stats(this, trackpairdetas()).min; }
    float trackpairdetamax() const { return stats(this, trackpairdetas()).max; }
    float trackpairdetaavg() const { return stats(this, trackpairdetas()).avg; }
    float trackpairdetarms() const { return stats(this, trackpairdetas()).rms; }

    std::vector<float> trackpairdphis() const {
      std::vector<float> v;
      size_t n = ntracks();
      if (n >= 2)
        for (size_t i = 0, ie = n-1; i < ie; ++i)
          if (use_track(i))
            for (size_t j = i+1, je = n; j < je; ++j)
              if (use_track(j))
                v.push_back(reco::deltaPhi(track_phi[i], track_phi[j]));
      return v;
    }

    float trackpairdphimin() const { return stats(this, trackpairdphis()).min; }
    float trackpairdphimax() const { return stats(this, trackpairdphis()).max; }
    float trackpairdphiavg() const { return stats(this, trackpairdphis()).avg; }
    float trackpairdphirms() const { return stats(this, trackpairdphis()).rms; }

    std::vector<float> trackpairdrs() const {
      std::vector<float> v;
      size_t n = ntracks();
      if (n >= 2)
        for (size_t i = 0, ie = n-1; i < ie; ++i)
          if (use_track(i))
            for (size_t j = i+1, je = n; j < je; ++j)
              if (use_track(j))
                v.push_back(reco::deltaR(track_eta[i], track_phi[i],
                                         track_eta[j], track_phi[j]));
      return v;
    }

    float trackpairdrmin() const { return stats(this, trackpairdrs()).min; }
    float trackpairdrmax() const { return stats(this, trackpairdrs()).max; }
    float trackpairdravg() const { return stats(this, trackpairdrs()).avg; }
    float trackpairdrrms() const { return stats(this, trackpairdrs()).rms; }

    float drmin() const { return trackpairdrmin(); }
    float drmax() const { return trackpairdrmax(); }
    float dravg() const { return trackpairdravg(); }
    float drrms() const { return trackpairdrrms(); }

    std::vector<float> trackpairmasses(float mass=0) const {
      std::vector<float> v;
      size_t n = ntracks();
      if (n >= 2)
        for (size_t i = 0, ie = n-1; i < ie; ++i)
          if (use_track(i))
            for (size_t j = i+1, je = n; j < je; ++j)
              if (use_track(j))
                v.push_back((track_p4(i, mass) + track_p4(j, mass)).M());
      return v;
    }

    float trackpairmassmin() const { return stats(this, trackpairmasses()).min; }
    float trackpairmassmax() const { return stats(this, trackpairmasses()).max; }
    float trackpairmassavg() const { return stats(this, trackpairmasses()).avg; }
    float trackpairmassrms() const { return stats(this, trackpairmasses()).rms; }

    std::vector<float> tracktripmasses(float mass=0) const {
      std::vector<float> v;
      size_t n = ntracks();
      if (n >= 3)
        for (size_t i = 0, ie = n-2; i < ie; ++i)
          if (use_track(i))
            for (size_t j = i+1, je = n-1; j < je; ++j)
              if (use_track(j))
                for (size_t k = j+1, ke = n; k < ke; ++k)
                  if (use_track(k))
                    v.push_back((track_p4(i, mass) + track_p4(j, mass) + track_p4(k, mass)).M());
      return v;
    }

    float tracktripmassmin() const { return stats(this, tracktripmasses()).min; }
    float tracktripmassmax() const { return stats(this, tracktripmasses()).max; }
    float tracktripmassavg() const { return stats(this, tracktripmasses()).avg; }
    float tracktripmassrms() const { return stats(this, tracktripmasses()).rms; }

    std::vector<float> trackquadmasses(float mass=0) const {
      std::vector<float> v;
      size_t n = ntracks();
      if (n >= 4)
        for (size_t i = 0, ie = n-3; i < ie; ++i)
          if (use_track(i))
            for (size_t j = i+1, je = n-2; j < je; ++j)
              if (use_track(j))
                for (size_t k = j+1, ke = n-1; k < ke; ++k)
                  if (use_track(k))
                    for (size_t l = k+1, le = n; l < le; ++l)
                      if (use_track(l))
                        v.push_back((track_p4(i, mass) + track_p4(j, mass) + track_p4(k, mass) + track_p4(l, mass)).M());
      return v;
    }

    float trackquadmassmin() const { return stats(this, trackquadmasses()).min; }
    float trackquadmassmax() const { return stats(this, trackquadmasses()).max; }
    float trackquadmassavg() const { return stats(this, trackquadmasses()).avg; }
    float trackquadmassrms() const { return stats(this, trackquadmasses()).rms; }
#endif    
  };

  void write_to_tree(TTree* tree, FlatNtuple& nt);
  void read_from_tree(TTree* tree, FlatNtuple& nt);
}

#endif
