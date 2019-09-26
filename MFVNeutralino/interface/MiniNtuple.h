#ifndef JMTucker_MFVNeutralino_interface_MiniNtuple_h
#define JMTucker_MFVNeutralino_interface_MiniNtuple_h

#include "Math/SMatrix.h"
#include "TLorentzVector.h"
#include "TTree.h"

#define JMT_STANDALONE_BTAGGING
#include "JMTucker/Tools/interface/BTagging.h"

namespace mfv {
  typedef ROOT::Math::SMatrix<double, 5, 5, ROOT::Math::MatRepSym<double, 5> >  TrackCovarianceMatrix;

  struct MiniNtuple {
    MiniNtuple();
    void clear();

    unsigned run;
    unsigned lumi;
    unsigned long long event;
    unsigned char gen_flavor_code;
    unsigned int pass_hlt;
    float l1_htt;
    float l1_myhtt;
    float l1_myhttwbug;
    float hlt_ht;
    float bsx;
    float bsy;
    float bsz;
    float bsdxdz;
    float bsdydz;
    float bsx_at_z(float z) const { return bsx + bsdxdz * (z - bsz); }
    float bsy_at_z(float z) const { return bsy + bsdydz * (z - bsz); }
    unsigned char npv;
    float pvx;
    float pvy;
    float pvz;
    unsigned char npu;
    float weight;
    unsigned char njets;
    float jet_pt[50];
    float jet_eta[50];
    float jet_phi[50];
    float jet_energy[50];
    unsigned char jet_id[50];
    float jet_bdisc_old[50];
    float jet_bdisc[50];
    float jet_hlt_pt[50];
    float jet_hlt_eta[50];
    float jet_hlt_phi[50];
    float jet_hlt_energy[50];
    bool jet_hlt_match(int i, float min_jet_pt=20.) const {
      // an offline jet with a successful HLT match will have a nonzero jet_hlt_pt;
      // all others have the default value of 0
      return jet_hlt_pt[i] > min_jet_pt;
    }
    float displaced_jet_hlt_pt[50];
    float displaced_jet_hlt_eta[50];
    float displaced_jet_hlt_phi[50];
    float displaced_jet_hlt_energy[50];
    bool displaced_jet_hlt_match(int i, float min_jet_pt=20.) const {
      // an offline jet with a successful HLT match will have a nonzero displaced_jet_hlt_pt;
      // all others have the default value of 0
      return displaced_jet_hlt_pt[i] > min_jet_pt;
    }
    float ht(float min_jet_pt=40.) const;
    bool is_btagged(int i, float min_bdisc=jmt::BTagging::discriminator_min(jmt::BTagging::tight)) const;
    int nbtags(std::vector<int> indices) const;
    int nbtags_(float min_bdisc, bool old) const;
    int nbtags_old(float min_bdisc) const { return nbtags_(min_bdisc, true); }
    int nbtags(float min_bdisc) const { return nbtags_(min_bdisc, false); }
    float gen_x[2];
    float gen_y[2];
    float gen_z[2];
    float gen_lsp_pt[2];
    float gen_lsp_eta[2];
    float gen_lsp_phi[2];
    float gen_lsp_mass[2];
    std::vector<TLorentzVector> gen_daughters;
    std::vector<int> gen_daughter_id;
    std::vector<TLorentzVector> gen_bquarks;
    std::vector<TLorentzVector> gen_leptons;
    float gen_jet_ht;
    float gen_jet_ht40;
    std::vector<TLorentzVector>* p_gen_daughters;
    std::vector<int>* p_gen_daughter_id;
    std::vector<TLorentzVector>* p_gen_bquarks;
    std::vector<TLorentzVector>* p_gen_leptons;

    unsigned char nvtx;
    unsigned char ntk0;
    std::vector<double> tk0_qchi2;
    std::vector<double> tk0_ndof;
    std::vector<double> tk0_vx;
    std::vector<double> tk0_vy;
    std::vector<double> tk0_vz;
    std::vector<double> tk0_px;
    std::vector<double> tk0_py;
    std::vector<double> tk0_pz;
    std::vector<short>  tk0_inpv;
    std::vector<TrackCovarianceMatrix> tk0_cov;
    std::vector<double>* p_tk0_qchi2;
    std::vector<double>* p_tk0_ndof;
    std::vector<double>* p_tk0_vx;
    std::vector<double>* p_tk0_vy;
    std::vector<double>* p_tk0_vz;
    std::vector<double>* p_tk0_px;
    std::vector<double>* p_tk0_py;
    std::vector<double>* p_tk0_pz;
    std::vector<short>*  p_tk0_inpv;
    std::vector<TrackCovarianceMatrix>* p_tk0_cov;
    bool genmatch0;
    float x0;
    float y0;
    float z0;
    float bs2derr0;
    float rescale_bs2derr0;

    unsigned char ntk1;
    std::vector<double> tk1_qchi2;
    std::vector<double> tk1_ndof;
    std::vector<double> tk1_vx;
    std::vector<double> tk1_vy;
    std::vector<double> tk1_vz;
    std::vector<double> tk1_px;
    std::vector<double> tk1_py;
    std::vector<double> tk1_pz;
    std::vector<short>  tk1_inpv;
    std::vector<TrackCovarianceMatrix> tk1_cov;
    std::vector<double>* p_tk1_qchi2;
    std::vector<double>* p_tk1_ndof;
    std::vector<double>* p_tk1_vx;
    std::vector<double>* p_tk1_vy;
    std::vector<double>* p_tk1_vz;
    std::vector<double>* p_tk1_px;
    std::vector<double>* p_tk1_py;
    std::vector<double>* p_tk1_pz;
    std::vector<short>*  p_tk1_inpv;
    std::vector<TrackCovarianceMatrix>* p_tk1_cov;
    bool genmatch1;
    float x1;
    float y1;
    float z1;
    float bs2derr1;
    float rescale_bs2derr1;

    bool satisfiesTrigger(size_t trig) const;
    bool satisfiesTriggerAndOffline(size_t trig) const;
    bool satisfiesHTOrBjetOrDisplacedDijetTrigger() const;
    bool satisfiesHTOrBjetOrDisplacedDijetTriggerAndOffline() const;
  };

  void write_to_tree(TTree* tree, MiniNtuple& nt);
  void read_from_tree(TTree* tree, MiniNtuple& nt);
  MiniNtuple* clone(const MiniNtuple& nt);
  long long loop(const char* fn, const char* tree_path, bool (*)(long long, long long, const mfv::MiniNtuple&));
}

#endif
