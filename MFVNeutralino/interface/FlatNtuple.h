#ifndef JMTucker_MFVNeutralino_interface_FlatNtuple_h
#define JMTucker_MFVNeutralino_interface_FlatNtuple_h

#include <cassert>
#include <numeric>
#include <vector>
#include "TLorentzVector.h"
#include "TTree.h"
#include "TVector2.h"

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
      sample = 0;
      gen_partons_in_acc = npv = pv_ntracks = nvertices = 0;
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
      track_w.clear();
      track_qpt.clear();
      track_eta.clear();
      track_phi.clear();
      track_dxy.clear();
      track_dz.clear();
      track_pt_err.clear();
      track_eta_err.clear();
      track_phi_err.clear();
      track_dxy_err.clear();
      track_dz_err.clear();
      track_chi2dof.clear();
      track_hitpattern.clear();
      track_injet.clear();
      track_inpv.clear();
    }

    void reserve_tracks(const int ntk) {
      track_w.push_back(std::vector<ushort>(ntk, 0));
      track_qpt.push_back(std::vector<float>(ntk, 0));
      track_eta.push_back(std::vector<float>(ntk, 0));
      track_phi.push_back(std::vector<float>(ntk, 0));
      track_dxy.push_back(std::vector<float>(ntk, 0));
      track_dz.push_back(std::vector<float>(ntk, 0));
      track_pt_err.push_back(std::vector<float>(ntk, 0));
      track_eta_err.push_back(std::vector<float>(ntk, 0));
      track_phi_err.push_back(std::vector<float>(ntk, 0));
      track_dxy_err.push_back(std::vector<float>(ntk, 0));
      track_dz_err.push_back(std::vector<float>(ntk, 0));
      track_chi2dof.push_back(std::vector<float>(ntk, 0));
      track_hitpattern.push_back(std::vector<ushort>(ntk, 0));
      track_injet.push_back(std::vector<ushort>(ntk, 0));
      track_inpv.push_back(std::vector<short>(ntk, 0));
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
    char sample;

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

    ////////////////

    std::vector<std::vector<ushort> > track_w;
    static uchar make_track_weight(float weight) { assert(weight >= 0 && weight <= 1); return uchar(weight*255); }
    float track_weight(int w, int i) const { return float(track_w[w][i])/255.f; }
    std::vector<std::vector<float> > track_qpt;
    float track_q(int w, int i) const { return track_qpt[w][i] > 0 ? 1 : -1; }
    float track_pt(int w, int i) const { return fabs(track_qpt[w][i]); }
    std::vector<std::vector<float> > track_eta;
    std::vector<std::vector<float> > track_phi;
    std::vector<std::vector<float> > track_dxy;
    std::vector<std::vector<float> > track_dz;
    std::vector<std::vector<float> > track_pt_err;
    std::vector<std::vector<float> > track_eta_err;
    std::vector<std::vector<float> > track_phi_err;
    std::vector<std::vector<float> > track_dxy_err;
    std::vector<std::vector<float> > track_dz_err;
    std::vector<std::vector<float> > track_chi2dof;
    std::vector<std::vector<ushort> > track_hitpattern;
    static ushort make_track_hitpattern(int npx, int nst, int nbehind, int nlost) {
      assert(npx >= 0 && nst >= 0 && nbehind >= 0 && nlost >= 0);
      if (npx > 7) npx = 7;
      if (nst > 31) nst = 31;
      if (nbehind > 15) nbehind = 7;
      if (nlost > 15) nlost = 15;
      return (nlost << 12) | (nbehind << 8) | (nst << 3) | npx;
    }
    int track_npxhits(int w, int i) const { return track_hitpattern[w][i] & 0x7; }
    int track_nsthits(int w, int i) const { return (track_hitpattern[w][i] >> 3) & 0x1F; }
    int track_nhitsbehind(int w, int i) const { return (track_hitpattern[w][i] >> 8) & 0xF; }
    int track_nhitslost(int w, int i) const { return (track_hitpattern[w][i] >> 12) & 0xF; }
    int track_nhits(int w, int i) const { return track_npxhits(w,i) + track_nsthits(w,i); }
    std::vector<std::vector<ushort> > track_injet;
    std::vector<std::vector<short> > track_inpv;

    TLorentzVector track_p4(int w, int i, float mass=0) const {
      TLorentzVector v;
      v.SetPtEtaPhiM(track_pt(w,i), track_eta[w][i], track_phi[w][i], mass);
      return v;
    }

    int ntracks(int w) const {
      return int(track_w[w].size());
    }

    bool use_track(int w, size_t i) const {
      static const float pt_err_thr = 0.5;
      return track_pt_err[w][i] / track_pt(w,i) <= pt_err_thr;
    }

    int nbadtracks(int w) const {
      int c = 0;
      for (size_t i = 0, ie = ntracks(w); i < ie; ++i)
        if (!use_track(w, i))
          ++c;
      return c;
    }

    int ngoodtracks(int w) const {
      return ntracks(w) - nbadtracks(w);
    }

    int ntracksptgt(int w, float thr) const {
      int c = 0;
      for (size_t i = 0, ie = ntracks(w); i < ie; ++i)
        if (use_track(w,i) && track_pt(w,i) > thr)
          ++c;
      return c;
    }

    int trackminnhits(int w) const {
      int m = 255, m2;
      for (size_t i = 0, ie = ntracks(w); i < ie; ++i)
        if (use_track(w,i) && (m2 = track_nhits(w,i)) < m)
          m = m2;
      return m;
    }

    int trackmaxnhits(int w) const {
      int m = 0, m2;
      for (size_t i = 0, ie = ntracks(w); i < ie; ++i)
        if (use_track(w,i) && (m2 = track_nhits(w,i)) > m)
          m = m2;
      return m;
    }

    float sumpt2(int w) const {
      float sum = 0;
      for (size_t i = 0, ie = ntracks(w); i < ie; ++i)
        if (use_track(w,i))
          sum += pow(track_pt(w,i), 2);
      return sum;
    }

    int sumnhitsbehind(int w) const {
      int c = 0;
      for (size_t i = 0, ie = ntracks(w); i < ie; ++i)
        if (use_track(w,i))
          c += track_nhitsbehind(w,i);
      return c;
    }

    int maxnhitsbehind(int w) const {
      int m = 0, m2;
      for (size_t i = 0, ie = ntracks(w); i < ie; ++i)
        if (use_track(w,i) && (m2 = track_nhitsbehind(w,i)) > m)
          m = m2;
      return m;
    }

    int ntrackssharedwpv(int w) const {
      int c = 0;
      for (size_t i = 0, ie = ntracks(w); i < ie; ++i)
        if (use_track(w,i) && track_inpv[w][i] == 0)
          ++c;
      return c;
    }

    int ntrackssharedwpvs(int w) const {
      int c = 0;
      for (size_t i = 0, ie = ntracks(w); i < ie; ++i)
        if (use_track(w,i) && track_inpv[w][i] >= 0)
          ++c;
      return c;
    }

    std::map<int,int> pvswtracksshared(int w) const {
      std::map<int,int> m;
      for (size_t i = 0, ie = ntracks(w); i < ie; ++i)
        if (use_track(w,i))
          ++m[track_inpv[w][i]];
      return m;
    }

    int npvswtracksshared(int w) const {
      std::map<int,int> m = pvswtracksshared(w);
      int c = int(m.size());
      if (m.find(-1) != m.end())
        --c;
      return c;
    }

    int pvmosttracksshared(int w) const {
      std::map<int,int> m = pvswtracksshared(w);
      int mi = -1, mc = 0;
      for (std::map<int,int>::const_iterator it = m.begin(), ite = m.end(); it != ite; ++it)
        if (it->first != -1 && it->second > mc) {
          mc = it->second;
          mi = it->first;
        }
      return mi;
    }

    std::vector<float> track_pts(int w) const {
      std::vector<float> pts;
      for (size_t i = 0, ie = ntracks(w); i < ie; ++i)
        if (use_track(w,i))
          pts.push_back(track_pt(w,i));
      return pts;
    }

    static float _min(const std::vector<float>& v) {
      float m = 1e99;
      for (size_t i = 0, ie = v.size(); i < ie; ++i)
        if (v[i] < m)
          m = v[i];
      return m;
    }

    static float _max(const std::vector<float>& v) {
      float m = -1e99;
      for (size_t i = 0, ie = v.size(); i < ie; ++i)
        if (v[i] > m)
          m = v[i];
      return m;
    }

    static float _avg(const std::vector<float>& v) {
      float a = 0.f;
      int c = 0;
      for (size_t i = 0, ie = v.size(); i < ie; ++i) {
        a += v[i];
        ++c;
      }
      return a / c;
    }

    static float _rms(const std::vector<float>& v) {
      if (v.size() == 0) return 0.f;
      float avg = _avg(v);
      std::vector<float> v2;
      for (size_t i = 0, ie = v.size(); i < ie; ++i)
        v2.push_back(pow(v[i] - avg, 2));
      return sqrt(std::accumulate(v2.begin(), v2.end(), 0.f)/v2.size());
    }
    
    float mintrackpt(int w) const { return _min(track_pts(w)); }
    float maxtrackpt(int w) const { return _max(track_pts(w)); }

    float maxmntrackpt(int w, int n) const {
      std::vector<float> pt = track_pts(w);
      int nt = int(pt.size());
      if (n > nt - 1)
        return -1;
      std::sort(pt.begin(), pt.end());
      return pt[nt-1-n];
    }

    std::vector<float> trackpairdrs(int w) const {
      std::vector<float> v;
      size_t n = ntracks(w);
      if (n >= 2)
        for (size_t i = 0, ie = n-1; i < ie; ++i)
          if (use_track(w,i))
            for (size_t j = i+1, je = n; j < je; ++j)
              if (use_track(w,j))
                v.push_back(sqrt(pow(track_eta[w][i] - track_eta[w][j], 2) + pow(TVector2::Phi_mpi_pi(track_phi[w][i] - track_phi[w][j]), 2)));
      return v;
    }

    float trackpairdrmin(int w) const { return _min(trackpairdrs(w)); }
    float trackpairdrmax(int w) const { return _max(trackpairdrs(w)); }
    float trackpairdravg(int w) const { return _avg(trackpairdrs(w)); }
    float trackpairdrrms(int w) const { return _rms(trackpairdrs(w)); }
  };

  void write_to_tree(TTree* tree, FlatNtuple& nt);
  void read_from_tree(TTree* tree, FlatNtuple& nt);
}

#endif
