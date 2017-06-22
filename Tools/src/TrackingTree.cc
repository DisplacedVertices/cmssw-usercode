#include "JMTucker/Tools/interface/TrackingTree.h"
#include <cassert>
#include "TTree.h"

TrackingTree::TrackingTree() {
  clear();
  p_pv_x = p_pv_y = p_pv_z = p_pv_sumpt2 = p_pv_ntracks = p_pv_chi2dof = p_pv_cxx = p_pv_cxy = p_pv_cxz = p_pv_cyy = p_pv_cyz = p_pv_czz = p_tk_chi2dof = p_tk_qpt = p_tk_eta = p_tk_phi = p_tk_dxybs = p_tk_dxypv = p_tk_dzbs = p_tk_dzpv = p_tk_vx = p_tk_vy = p_tk_vz = p_tk_err_qpt = p_tk_err_eta = p_tk_err_phi = p_tk_err_dxy = p_tk_err_dz = 0;
  p_tk_nsthit = p_tk_npxhit = p_tk_nstlay = p_tk_npxlay = p_tk_minhit_ = p_tk_maxhit_ = p_tk_maxpxhit_ = 0;
}

void TrackingTree::clear() {
  run = lumi = 0;
  event = 0;
  npu = 0;
  bs_x = bs_y = bs_z = bs_sigmaz = bs_dxdz = bs_dydz = bs_width = 0;
  bs_err_x = bs_err_y = bs_err_z = bs_err_sigmaz = bs_err_dxdz = bs_err_dydz = bs_err_width = 0;

  pv_x.clear();
  pv_y.clear();
  pv_z.clear();
  pv_sumpt2.clear();
  pv_ntracks.clear();
  pv_chi2dof.clear();
  pv_cxx.clear();
  pv_cxy.clear();
  pv_cxz.clear();
  pv_cyy.clear();
  pv_cyz.clear();
  pv_czz.clear();

  tk_chi2dof.clear();
  tk_qpt.clear();
  tk_eta.clear();
  tk_phi.clear();
  tk_dxybs.clear();
  tk_dxypv.clear();
  tk_dzbs.clear();
  tk_dzpv.clear();
  tk_vx.clear();
  tk_vy.clear();
  tk_vz.clear();
  tk_err_qpt.clear();
  tk_err_eta.clear();
  tk_err_phi.clear();
  tk_err_dxy.clear();
  tk_err_dz.clear();
  tk_nsthit.clear();
  tk_npxhit.clear();
  tk_nstlay.clear();
  tk_npxlay.clear();
  tk_minhit_.clear();
  tk_maxhit_.clear();
  tk_maxpxhit_.clear();
}

void TrackingTree::tk_minhit(int min_r, int min_z) {
  assert(min_r >= 0 && min_r <= 15);
  assert(min_z >= 0 && min_z <= 15);
  tk_minhit_.push_back((uchar(min_z) << 4) | uchar(min_r));
}

int TrackingTree::tk_min_r(int i) {
  return (*p_tk_minhit_)[i] & 0xF;
}

int TrackingTree::tk_min_z(int i) {
  return (*p_tk_minhit_)[i] >> 4;
}

void TrackingTree::tk_maxhit(int max_r, int max_z) {
  assert(max_r >= 0 && max_r <= 15);
  assert(max_z >= 0 && max_z <= 15);
  tk_maxhit_.push_back((uchar(max_z) << 4) | uchar(max_r));
}

int TrackingTree::tk_max_r(int i) {
  return (*p_tk_maxhit_)[i] & 0xF;
}

int TrackingTree::tk_max_z(int i) {
  return (*p_tk_maxhit_)[i] >> 4;
}

void TrackingTree::tk_maxpxhit(int max_r, int max_z) {
  assert(max_r >= 0 && max_r <= 15);
  assert(max_z >= 0 && max_z <= 15);
  tk_maxpxhit_.push_back((uchar(max_z) << 4) | uchar(max_r));
}

int TrackingTree::tk_maxpx_r(int i) {
  return (*p_tk_maxpxhit_)[i] & 0xF;
}

int TrackingTree::tk_maxpx_z(int i) {
  return (*p_tk_maxpxhit_)[i] >> 4;
}

int TrackingTree::tk_charge(int i) {
  return (*p_tk_qpt)[i] > 0 ? 1 : -1;
}

TVector3 TrackingTree::tk_v3(int i) {
  TVector3 v;
  v.SetPtEtaPhi(fabs((*p_tk_qpt)[i]), (*p_tk_eta)[i], (*p_tk_phi)[i]);
  return v;
}

void TrackingTree::write_to_tree(TTree* tree) {
  tree->SetAlias("npvs", "pv_x@.size()");
  tree->SetAlias("ntks", "tk_qpt@.size()");

  tree->Branch("run", &run, "run/i");
  tree->Branch("lumi", &lumi, "lumi/i");
  tree->Branch("event", &event);
  tree->Branch("npu", &npu);
  tree->Branch("bs_x", &bs_x, "bs_x/F");
  tree->Branch("bs_y", &bs_y, "bs_y/F");
  tree->Branch("bs_z", &bs_z, "bs_z/F");
  tree->Branch("bs_sigmaz", &bs_sigmaz, "bs_sigmaz/F");
  tree->Branch("bs_dxdz", &bs_dxdz, "bs_dxdz/F");
  tree->Branch("bs_dydz", &bs_dydz, "bs_dydz/F");
  tree->Branch("bs_width", &bs_width, "bs_width/F");
  tree->Branch("bs_err_x", &bs_err_x, "bs_err_x/F");
  tree->Branch("bs_err_y", &bs_err_y, "bs_err_y/F");
  tree->Branch("bs_err_z", &bs_err_z, "bs_err_z/F");
  tree->Branch("bs_err_sigmaz", &bs_err_sigmaz, "bs_err_sigmaz/F");
  tree->Branch("bs_err_dxdz", &bs_err_dxdz, "bs_err_dxdz/F");
  tree->Branch("bs_err_dydz", &bs_err_dydz, "bs_err_dydz/F");
  tree->Branch("bs_err_width", &bs_err_width, "bs_err_width/F");
  tree->Branch("pv_x", &pv_x);
  tree->Branch("pv_y", &pv_y);
  tree->Branch("pv_z", &pv_z);
  tree->Branch("pv_sumpt2", &pv_sumpt2);
  tree->Branch("pv_ntracks", &pv_ntracks);
  tree->Branch("pv_chi2dof", &pv_chi2dof);
  tree->Branch("pv_cxx", &pv_cxx);
  tree->Branch("pv_cxy", &pv_cxy);
  tree->Branch("pv_cxz", &pv_cxz);
  tree->Branch("pv_cyy", &pv_cyy);
  tree->Branch("pv_cyz", &pv_cyz);
  tree->Branch("pv_czz", &pv_czz);
  tree->Branch("tk_chi2dof", &tk_chi2dof);
  tree->Branch("tk_qpt", &tk_qpt);
  tree->Branch("tk_eta", &tk_eta);
  tree->Branch("tk_phi", &tk_phi);
  tree->Branch("tk_dxybs", &tk_dxybs);
  tree->Branch("tk_dxypv", &tk_dxypv);
  tree->Branch("tk_dzbs", &tk_dzbs);
  tree->Branch("tk_dzpv", &tk_dzpv);
  tree->Branch("tk_vx", &tk_vx);
  tree->Branch("tk_vy", &tk_vy);
  tree->Branch("tk_vz", &tk_vz);
  tree->Branch("tk_err_qpt", &tk_err_qpt);
  tree->Branch("tk_err_eta", &tk_err_eta);
  tree->Branch("tk_err_phi", &tk_err_phi);
  tree->Branch("tk_err_dxy", &tk_err_dxy);
  tree->Branch("tk_err_dz", &tk_err_dz);
  tree->Branch("tk_nsthit", &tk_nsthit);
  tree->Branch("tk_npxhit", &tk_npxhit);
  tree->Branch("tk_nstlay", &tk_nstlay);
  tree->Branch("tk_npxlay", &tk_npxlay);
  tree->Branch("tk_minhit", &tk_minhit_);
  tree->Branch("tk_maxhit", &tk_maxhit_);
  tree->Branch("tk_maxpxhit", &tk_maxpxhit_);
}

void TrackingTree::read_from_tree(TTree* tree) {
  tree->SetBranchAddress("run", &run);
  tree->SetBranchAddress("lumi", &lumi);
  tree->SetBranchAddress("event", &event);
  tree->SetBranchAddress("npu", &npu);
  tree->SetBranchAddress("bs_x", &bs_x);
  tree->SetBranchAddress("bs_y", &bs_y);
  tree->SetBranchAddress("bs_z", &bs_z);
  tree->SetBranchAddress("bs_sigmaz", &bs_sigmaz);
  tree->SetBranchAddress("bs_dxdz", &bs_dxdz);
  tree->SetBranchAddress("bs_dydz", &bs_dydz);
  tree->SetBranchAddress("bs_width", &bs_width);
  tree->SetBranchAddress("bs_err_x", &bs_err_x);
  tree->SetBranchAddress("bs_err_y", &bs_err_y);
  tree->SetBranchAddress("bs_err_z", &bs_err_z);
  tree->SetBranchAddress("bs_err_sigmaz", &bs_err_sigmaz);
  tree->SetBranchAddress("bs_err_dxdz", &bs_err_dxdz);
  tree->SetBranchAddress("bs_err_dydz", &bs_err_dydz);
  tree->SetBranchAddress("bs_err_width", &bs_err_width);
  tree->SetBranchAddress("pv_x", &p_pv_x);
  tree->SetBranchAddress("pv_y", &p_pv_y);
  tree->SetBranchAddress("pv_z", &p_pv_z);
  tree->SetBranchAddress("pv_sumpt2", &p_pv_sumpt2);
  tree->SetBranchAddress("pv_ntracks", &p_pv_ntracks);
  tree->SetBranchAddress("pv_chi2dof", &p_pv_chi2dof);
  tree->SetBranchAddress("pv_cxx", &p_pv_cxx);
  tree->SetBranchAddress("pv_cxy", &p_pv_cxy);
  tree->SetBranchAddress("pv_cxz", &p_pv_cxz);
  tree->SetBranchAddress("pv_cyy", &p_pv_cyy);
  tree->SetBranchAddress("pv_cyz", &p_pv_cyz);
  tree->SetBranchAddress("pv_czz", &p_pv_czz);
  tree->SetBranchAddress("tk_chi2dof", &p_tk_chi2dof);
  tree->SetBranchAddress("tk_qpt", &p_tk_qpt);
  tree->SetBranchAddress("tk_eta", &p_tk_eta);
  tree->SetBranchAddress("tk_phi", &p_tk_phi);
  tree->SetBranchAddress("tk_dxybs", &p_tk_dxybs);
  tree->SetBranchAddress("tk_dxypv", &p_tk_dxypv);
  tree->SetBranchAddress("tk_dzbs", &p_tk_dzbs);
  tree->SetBranchAddress("tk_dzpv", &p_tk_dzpv);
  tree->SetBranchAddress("tk_vx", &p_tk_vx);
  tree->SetBranchAddress("tk_vy", &p_tk_vy);
  tree->SetBranchAddress("tk_vz", &p_tk_vz);
  tree->SetBranchAddress("tk_err_qpt", &p_tk_err_qpt);
  tree->SetBranchAddress("tk_err_eta", &p_tk_err_eta);
  tree->SetBranchAddress("tk_err_phi", &p_tk_err_phi);
  tree->SetBranchAddress("tk_err_dxy", &p_tk_err_dxy);
  tree->SetBranchAddress("tk_err_dz", &p_tk_err_dz);
  tree->SetBranchAddress("tk_nsthit", &p_tk_nsthit);
  tree->SetBranchAddress("tk_npxhit", &p_tk_npxhit);
  tree->SetBranchAddress("tk_nstlay", &p_tk_nstlay);
  tree->SetBranchAddress("tk_npxlay", &p_tk_npxlay);
  tree->SetBranchAddress("tk_minhit", &p_tk_minhit_);
  tree->SetBranchAddress("tk_maxhit", &p_tk_maxhit_);
  tree->SetBranchAddress("tk_maxpxhit", &p_tk_maxpxhit_);
}
