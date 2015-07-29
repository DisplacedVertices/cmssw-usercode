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
      run = lumi = 0;
      event = 0;
      sample = 0;
      gen_partons_in_acc = npv = pv_ntracks = nvertices = 0;
      gen_valid = 0;
      for (int i = 0; i < 2; ++i) {
        gen_lsp_pt[i] = gen_lsp_eta[i] = gen_lsp_phi[i] = gen_lsp_mass[i] = 0;
        for (int j = 0; j < 3; ++j)
          gen_lsp_decay[i*3+j] = 0;
        gen_decay_type[i] = 0;
      }
      npu = bsx = bsy = bsz = bsdxdz = bsdydz = bswidthx = bswidthy = pvx = pvy = pvz = pv_sumpt2 = metx = mety = metsig = metdphimin = 0;
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
      vtx_bs2ddist.clear();
      vtx_bs2derr.clear();
      vtx_pv2ddist.clear();
      vtx_pv2derr.clear();
      vtx_pv3ddist.clear();
      vtx_pv3derr.clear();
      vtx_ntracks.clear();
      vtx_nbadtracks.clear();
      vtx_ntracksptgt3.clear();
      vtx_ntracksptgt5.clear();
      vtx_ntracksptgt10.clear();
      vtx_trackminnhits.clear();
      vtx_trackmaxnhits.clear();
      vtx_sumpt2.clear();
      vtx_sumnhitsbehind.clear();
      vtx_maxnhitsbehind.clear();
      vtx_ntrackssharedwpv.clear();
      vtx_ntrackssharedwpvs.clear();
      vtx_npvswtracksshared.clear();
      vtx_pvmosttracksshared.clear();
      vtx_mintrackpt.clear();
      vtx_maxtrackpt.clear();
      vtx_maxm1trackpt.clear();
      vtx_maxm2trackpt.clear();
      vtx_trackpairdrmin.clear();
      vtx_trackpairdrmax.clear();
      vtx_trackpairdravg.clear();
      vtx_trackpairdrrms.clear();
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
    unsigned long long event;
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
    float bsdxdz;
    float bsdydz;
    float bswidthx;
    float bswidthy;

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

    std::vector<float> vtx_bs2ddist;
    std::vector<float> vtx_bs2derr;
    float vtx_bs2dsig(int w) const { return sig(vtx_bs2ddist[w], vtx_bs2derr[w]); }

    std::vector<float> vtx_pv2ddist;
    std::vector<float> vtx_pv2derr;
    float vtx_pv2dsig(int w) const { return sig(vtx_pv2ddist[w], vtx_pv2derr[w]); }

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

    std::vector<uchar> vtx_ntracks;
    std::vector<uchar> vtx_nbadtracks;
    std::vector<uchar> vtx_ntracksptgt3;
    std::vector<uchar> vtx_ntracksptgt5;
    std::vector<uchar> vtx_ntracksptgt10;
    std::vector<uchar> vtx_trackminnhits;
    std::vector<uchar> vtx_trackmaxnhits;
    std::vector<float> vtx_sumpt2;
    std::vector<uchar> vtx_sumnhitsbehind;
    std::vector<uchar> vtx_maxnhitsbehind;
    std::vector<uchar> vtx_ntrackssharedwpv;
    std::vector<uchar> vtx_ntrackssharedwpvs;
    std::vector<uchar> vtx_npvswtracksshared;
    std::vector<char>  vtx_pvmosttracksshared;
    std::vector<float> vtx_mintrackpt;
    std::vector<float> vtx_maxtrackpt;
    std::vector<float> vtx_maxm1trackpt;
    std::vector<float> vtx_maxm2trackpt;
    std::vector<float> vtx_trackpairdrmin;
    std::vector<float> vtx_trackpairdrmax;
    std::vector<float> vtx_trackpairdravg;
    std::vector<float> vtx_trackpairdrrms;
  };

  void write_to_tree(TTree* tree, FlatNtuple& nt);
  void read_from_tree(TTree* tree, FlatNtuple& nt);
}

#endif
