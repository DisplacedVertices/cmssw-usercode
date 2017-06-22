#ifndef JMTucker_Tools_TrackingTree_h
#define JMTucker_Tools_TrackingTree_h

#include <vector>
#include "TVector3.h"

class TTree;

struct TrackingTree {
  typedef unsigned char uchar;

  unsigned run;
  unsigned lumi;
  unsigned long long event;
  unsigned short npu;

  float bs_x;
  float bs_y;
  float bs_z;
  float bs_sigmaz;
  float bs_dxdz;
  float bs_dydz;
  float bs_width;

  float bs_err_x;
  float bs_err_y;
  float bs_err_z;
  float bs_err_sigmaz;
  float bs_err_dxdz;
  float bs_err_dydz;
  float bs_err_width;

  std::vector<float> pv_x;
  std::vector<float> pv_y;
  std::vector<float> pv_z;
  std::vector<float> pv_sumpt2;
  std::vector<float> pv_ntracks;
  std::vector<float> pv_chi2dof;
  std::vector<float> pv_cxx;
  std::vector<float> pv_cxy;
  std::vector<float> pv_cxz;
  std::vector<float> pv_cyy;
  std::vector<float> pv_cyz;
  std::vector<float> pv_czz;

  std::vector<float> tk_chi2dof;
  std::vector<float> tk_qpt;
  std::vector<float> tk_eta;
  std::vector<float> tk_phi;
  std::vector<float> tk_dxybs;
  std::vector<float> tk_dxypv;
  std::vector<float> tk_dzbs;
  std::vector<float> tk_dzpv;
  std::vector<float> tk_vx;
  std::vector<float> tk_vy;
  std::vector<float> tk_vz;
  std::vector<float> tk_err_qpt;
  std::vector<float> tk_err_eta;
  std::vector<float> tk_err_phi;
  std::vector<float> tk_err_dxy;
  std::vector<float> tk_err_dz;
  std::vector<uchar> tk_nsthit;
  std::vector<uchar> tk_npxhit;
  std::vector<uchar> tk_nstlay;
  std::vector<uchar> tk_npxlay;
  std::vector<uchar> tk_minhit_;
  std::vector<uchar> tk_maxhit_;
  std::vector<uchar> tk_maxpxhit_;
  void tk_minhit(int min_r, int min_z);
  int tk_min_r(int i);
  int tk_min_z(int i);
  void tk_maxhit(int max_r, int max_z);
  int tk_max_r(int i);
  int tk_max_z(int i);
  void tk_maxpxhit(int max_r, int max_z);
  int tk_maxpx_r(int i);
  int tk_maxpx_z(int i);
  int tk_charge(int i);
  TVector3 tk_v3(int i);

  TrackingTree();
  void clear();
  void write_to_tree(TTree* tree);
  void read_from_tree(TTree* tree);
  int npvs() { return int(p_pv_x->size()); }
  int ntks() { return int(p_tk_qpt->size()); }

  // ugh
  std::vector<float>* p_pv_x;
  std::vector<float>* p_pv_y;
  std::vector<float>* p_pv_z;
  std::vector<float>* p_pv_sumpt2;
  std::vector<float>* p_pv_ntracks;
  std::vector<float>* p_pv_chi2dof;
  std::vector<float>* p_pv_cxx;
  std::vector<float>* p_pv_cxy;
  std::vector<float>* p_pv_cxz;
  std::vector<float>* p_pv_cyy;
  std::vector<float>* p_pv_cyz;
  std::vector<float>* p_pv_czz;
  std::vector<float>* p_tk_chi2dof;
  std::vector<float>* p_tk_qpt;
  std::vector<float>* p_tk_eta;
  std::vector<float>* p_tk_phi;
  std::vector<float>* p_tk_dxybs;
  std::vector<float>* p_tk_dxypv;
  std::vector<float>* p_tk_dzbs;
  std::vector<float>* p_tk_dzpv;
  std::vector<float>* p_tk_vx;
  std::vector<float>* p_tk_vy;
  std::vector<float>* p_tk_vz;
  std::vector<float>* p_tk_err_qpt;
  std::vector<float>* p_tk_err_eta;
  std::vector<float>* p_tk_err_phi;
  std::vector<float>* p_tk_err_dxy;
  std::vector<float>* p_tk_err_dz;
  std::vector<uchar>* p_tk_nsthit;
  std::vector<uchar>* p_tk_npxhit;
  std::vector<uchar>* p_tk_nstlay;
  std::vector<uchar>* p_tk_npxlay;
  std::vector<uchar>* p_tk_minhit_;
  std::vector<uchar>* p_tk_maxhit_;
  std::vector<uchar>* p_tk_maxpxhit_;
};

#endif
