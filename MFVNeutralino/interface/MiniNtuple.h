#ifndef JMTucker_MFVNeutralino_interface_MiniNtuple_h
#define JMTucker_MFVNeutralino_interface_MiniNtuple_h

#include "Math/SMatrix.h"
#include "TTree.h"

namespace mfv {
  typedef ROOT::Math::SMatrix<double, 5, 5, ROOT::Math::MatRepSym<double, 5> >  TrackCovarianceMatrix;

  struct MiniNtuple {
    MiniNtuple();
    void clear();

    unsigned run;
    unsigned lumi;
    unsigned long long event;
    unsigned char gen_flavor_code;
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
    std::vector<TrackCovarianceMatrix> tk0_cov;
    std::vector<double>* p_tk0_qchi2;
    std::vector<double>* p_tk0_ndof;
    std::vector<double>* p_tk0_vx;
    std::vector<double>* p_tk0_vy;
    std::vector<double>* p_tk0_vz;
    std::vector<double>* p_tk0_px;
    std::vector<double>* p_tk0_py;
    std::vector<double>* p_tk0_pz;
    std::vector<TrackCovarianceMatrix>* p_tk0_cov;
    float x0;
    float y0;
    float z0;
    unsigned char ntracksptgt30;
    float drmin0;
    float drmax0;
    unsigned char njetsntks0;
    float bs2derr0;
    float geo2ddist0;

    unsigned char ntk1;
    std::vector<double> tk1_qchi2;
    std::vector<double> tk1_ndof;
    std::vector<double> tk1_vx;
    std::vector<double> tk1_vy;
    std::vector<double> tk1_vz;
    std::vector<double> tk1_px;
    std::vector<double> tk1_py;
    std::vector<double> tk1_pz;
    std::vector<TrackCovarianceMatrix> tk1_cov;
    std::vector<double>* p_tk1_qchi2;
    std::vector<double>* p_tk1_ndof;
    std::vector<double>* p_tk1_vx;
    std::vector<double>* p_tk1_vy;
    std::vector<double>* p_tk1_vz;
    std::vector<double>* p_tk1_px;
    std::vector<double>* p_tk1_py;
    std::vector<double>* p_tk1_pz;
    std::vector<TrackCovarianceMatrix>* p_tk1_cov;
    float x1;
    float y1;
    float z1;
    unsigned char ntracksptgt31;
    float drmin1;
    float drmax1;
    unsigned char njetsntks1;
    float bs2derr1;
    float geo2ddist1;
  };

  void write_to_tree(TTree* tree, MiniNtuple& nt);
  void read_from_tree(TTree* tree, MiniNtuple& nt);
  MiniNtuple* clone(const MiniNtuple& nt);
  long long loop(const char* fn, const char* tree_path, bool (*)(long long, long long, const mfv::MiniNtuple&));
}

#endif
