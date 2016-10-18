#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"

namespace mfv {
  void write_to_tree(TTree* tree, MiniNtuple& nt) {
    tree->Branch("run", &nt.run);
    tree->Branch("lumi", &nt.lumi);
    tree->Branch("event", &nt.event);
    tree->Branch("gen_flavor_code", &nt.gen_flavor_code);
    tree->Branch("npv", &nt.npv);
    tree->Branch("pvx", &nt.pvx);
    tree->Branch("pvy", &nt.pvy);
    tree->Branch("pvz", &nt.pvz);
    tree->Branch("npu", &nt.npu);
    tree->Branch("weight", &nt.weight);

    tree->Branch("njets", &nt.njets);
    tree->Branch("jet_pt", nt.jet_pt, "jet_pt[njets]/F");
    tree->Branch("jet_eta", nt.jet_eta, "jet_eta[njets]/F");
    tree->Branch("jet_phi", nt.jet_phi, "jet_phi[njets]/F");
    tree->Branch("jet_energy", nt.jet_energy, "jet_energy[njets]/F");
    tree->Branch("jet_id", nt.jet_id, "jet_id[njets]/b");

    tree->Branch("nvtx", &nt.nvtx);
    tree->Branch("ntk0", &nt.ntk0);
    tree->Branch("tk0_chi2", &nt.tk0_chi2);
    tree->Branch("tk0_ndof", &nt.tk0_ndof);
    tree->Branch("tk0_vx", &nt.tk0_vx);
    tree->Branch("tk0_vy", &nt.tk0_vy);
    tree->Branch("tk0_vz", &nt.tk0_vz);
    tree->Branch("tk0_px", &nt.tk0_px);
    tree->Branch("tk0_py", &nt.tk0_py);
    tree->Branch("tk0_pz", &nt.tk0_pz);
    tree->Branch("tk0_cov", &nt.tk0_cov);
    tree->Branch("x0", &nt.x0);
    tree->Branch("y0", &nt.y0);
    tree->Branch("z0", &nt.z0);
    tree->Branch("ntracksptgt30", &nt.ntracksptgt30);
    tree->Branch("drmin0", &nt.drmin0);
    tree->Branch("drmax0", &nt.drmax0);
    tree->Branch("njetsntks0", &nt.njetsntks0);
    tree->Branch("bs2derr0", &nt.bs2derr0);
    tree->Branch("geo2ddist0", &nt.geo2ddist0);

    tree->Branch("ntk1", &nt.ntk1);
    tree->Branch("tk1_chi2", &nt.tk1_chi2);
    tree->Branch("tk1_ndof", &nt.tk1_ndof);
    tree->Branch("tk1_vx", &nt.tk1_vx);
    tree->Branch("tk1_vy", &nt.tk1_vy);
    tree->Branch("tk1_vz", &nt.tk1_vz);
    tree->Branch("tk1_px", &nt.tk1_px);
    tree->Branch("tk1_py", &nt.tk1_py);
    tree->Branch("tk1_pz", &nt.tk1_pz);
    tree->Branch("tk1_cov", &nt.tk1_cov);
    tree->Branch("x1", &nt.x1);
    tree->Branch("y1", &nt.y1);
    tree->Branch("z1", &nt.z1);
    tree->Branch("ntracksptgt31", &nt.ntracksptgt31);
    tree->Branch("drmin1", &nt.drmin1);
    tree->Branch("drmax1", &nt.drmax1);
    tree->Branch("njetsntks1", &nt.njetsntks1);
    tree->Branch("bs2derr1", &nt.bs2derr1);
    tree->Branch("geo2ddist1", &nt.geo2ddist1);

    tree->SetAlias("dist0", "sqrt(x0**2 + y0**2)");
    tree->SetAlias("dist1", "sqrt(x1**2 + y1**2)");
    tree->SetAlias("phi0",  "atan2(y0,x0)");
    tree->SetAlias("phi1",  "atan2(y1,x1)");
    tree->SetAlias("svdist",  "(nvtx >= 2) * sqrt((x0-x1)**2 + (y0-y1)**2)");
    tree->SetAlias("svdphi",  "(nvtx >= 2) * TVector2::Phi_mpi_pi(atan2(y0,x0)-atan2(y1,x1))");
    tree->SetAlias("svdz",    "(nvtx >= 2) * (z0 - z1)");
  }

  void read_from_tree(TTree* tree, MiniNtuple& nt) {
    nt.p_tk0_chi2 = nt.p_tk0_ndof = nt.p_tk0_vx = nt.p_tk0_vy = nt.p_tk0_vz = nt.p_tk0_px = nt.p_tk0_py = nt.p_tk0_pz = nt.p_tk1_chi2 = nt.p_tk1_ndof = nt.p_tk1_vx = nt.p_tk1_vy = nt.p_tk1_vz = nt.p_tk1_px = nt.p_tk1_py = nt.p_tk1_pz = 0;
    nt.p_tk0_cov = nt.p_tk1_cov = 0;

    tree->SetBranchAddress("run", &nt.run);
    tree->SetBranchAddress("lumi", &nt.lumi);
    tree->SetBranchAddress("event", &nt.event);
    tree->SetBranchAddress("gen_flavor_code", &nt.gen_flavor_code);
    tree->SetBranchAddress("npv", &nt.npv);
    tree->SetBranchAddress("pvx", &nt.pvx);
    tree->SetBranchAddress("pvy", &nt.pvy);
    tree->SetBranchAddress("pvz", &nt.pvz);
    tree->SetBranchAddress("npu", &nt.npu);
    tree->SetBranchAddress("weight", &nt.weight);
    tree->SetBranchAddress("njets", &nt.njets);
    tree->SetBranchAddress("jet_pt", nt.jet_pt);
    tree->SetBranchAddress("jet_eta", nt.jet_eta);
    tree->SetBranchAddress("jet_phi", nt.jet_phi);
    tree->SetBranchAddress("jet_energy", nt.jet_energy);
    tree->SetBranchAddress("jet_id", nt.jet_id);
    tree->SetBranchAddress("nvtx", &nt.nvtx);
    tree->SetBranchAddress("ntk0", &nt.ntk0);
    tree->SetBranchAddress("tk0_chi2", &nt.p_tk0_chi2);
    tree->SetBranchAddress("tk0_ndof", &nt.p_tk0_ndof);
    tree->SetBranchAddress("tk0_vx", &nt.p_tk0_vx);
    tree->SetBranchAddress("tk0_vy", &nt.p_tk0_vy);
    tree->SetBranchAddress("tk0_vz", &nt.p_tk0_vz);
    tree->SetBranchAddress("tk0_px", &nt.p_tk0_px);
    tree->SetBranchAddress("tk0_py", &nt.p_tk0_py);
    tree->SetBranchAddress("tk0_pz", &nt.p_tk0_pz);
    tree->SetBranchAddress("tk0_cov", &nt.p_tk0_cov);
    tree->SetBranchAddress("x0", &nt.x0);
    tree->SetBranchAddress("y0", &nt.y0);
    tree->SetBranchAddress("z0", &nt.z0);
    tree->SetBranchAddress("ntracksptgt30", &nt.ntracksptgt30);
    tree->SetBranchAddress("drmin0", &nt.drmin0);
    tree->SetBranchAddress("drmax0", &nt.drmax0);
    tree->SetBranchAddress("njetsntks0", &nt.njetsntks0);
    tree->SetBranchAddress("bs2derr0", &nt.bs2derr0);
    tree->SetBranchAddress("geo2ddist0", &nt.geo2ddist0);
    tree->SetBranchAddress("ntk1", &nt.ntk1);
    tree->SetBranchAddress("tk1_chi2", &nt.p_tk1_chi2);
    tree->SetBranchAddress("tk1_ndof", &nt.p_tk1_ndof);
    tree->SetBranchAddress("tk1_vx", &nt.p_tk1_vx);
    tree->SetBranchAddress("tk1_vy", &nt.p_tk1_vy);
    tree->SetBranchAddress("tk1_vz", &nt.p_tk1_vz);
    tree->SetBranchAddress("tk1_px", &nt.p_tk1_px);
    tree->SetBranchAddress("tk1_py", &nt.p_tk1_py);
    tree->SetBranchAddress("tk1_pz", &nt.p_tk1_pz);
    tree->SetBranchAddress("tk1_cov", &nt.p_tk1_cov);
    tree->SetBranchAddress("x1", &nt.x1);
    tree->SetBranchAddress("y1", &nt.y1);
    tree->SetBranchAddress("z1", &nt.z1);
    tree->SetBranchAddress("ntracksptgt31", &nt.ntracksptgt31);
    tree->SetBranchAddress("drmin1", &nt.drmin1);
    tree->SetBranchAddress("drmax1", &nt.drmax1);
    tree->SetBranchAddress("njetsntks1", &nt.njetsntks1);
    tree->SetBranchAddress("bs2derr1", &nt.bs2derr1);
    tree->SetBranchAddress("geo2ddist1", &nt.geo2ddist1);
  }
}
