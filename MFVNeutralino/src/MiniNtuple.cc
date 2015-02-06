#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"

namespace mfv {
  void write_to_tree(TTree* tree, MiniNtuple& nt) {
    tree->Branch("run", &nt.run, "run/i");
    tree->Branch("lumi", &nt.lumi, "lumi/i");
    tree->Branch("event", &nt.event);
    tree->Branch("npv", &nt.npv, "npv/s");
    tree->Branch("pvx", &nt.pvx, "pvx/F");
    tree->Branch("pvy", &nt.pvy, "pvy/F");
    tree->Branch("pvz", &nt.pvz, "pvz/F");
    tree->Branch("npu", &nt.npu, "npu/s");
    tree->Branch("weight", &nt.weight, "weight/F");

    tree->Branch("njets", &nt.njets, "njets/s");
    tree->Branch("jet_pt", nt.jet_pt, "jet_pt[njets]/F");
    tree->Branch("jet_eta", nt.jet_eta, "jet_eta[njets]/F");
    tree->Branch("jet_phi", nt.jet_phi, "jet_phi[njets]/F");
    tree->Branch("jet_energy", nt.jet_energy, "jet_energy[njets]/F");

    tree->Branch("nvtx", &nt.nvtx, "nvtx/s");
    tree->Branch("ntk0", &nt.ntk0, "ntk0/s");
    tree->Branch("x0", &nt.x0, "x0/F");
    tree->Branch("y0", &nt.y0, "y0/F");
    tree->Branch("z0", &nt.z0, "z0/F");
    tree->Branch("cxx0", &nt.cxx0, "cxx0/F");
    tree->Branch("cxy0", &nt.cxy0, "cxy0/F");
    tree->Branch("cxz0", &nt.cxz0, "cxz0/F");
    tree->Branch("cyy0", &nt.cyy0, "cyy0/F");
    tree->Branch("cyz0", &nt.cyz0, "cyz0/F");
    tree->Branch("czz0", &nt.czz0, "czz0/F");
    tree->Branch("ntk1", &nt.ntk1, "ntk1/s");
    tree->Branch("x1", &nt.x1, "x1/F");
    tree->Branch("y1", &nt.y1, "y1/F");
    tree->Branch("z1", &nt.z1, "z1/F");
    tree->Branch("cxx1", &nt.cxx1, "cxx1/F");
    tree->Branch("cxy1", &nt.cxy1, "cxy1/F");
    tree->Branch("cxz1", &nt.cxz1, "cxz1/F");
    tree->Branch("cyy1", &nt.cyy1, "cyy1/F");
    tree->Branch("cyz1", &nt.cyz1, "cyz1/F");
    tree->Branch("czz1", &nt.czz1, "czz1/F");

    tree->SetAlias("dist0", "sqrt(x0**2 + y0**2)");
    tree->SetAlias("dist1", "sqrt(x1**2 + y1**2)");
    tree->SetAlias("phi0",  "atan2(y0,x0)");
    tree->SetAlias("phi1",  "atan2(y1,x1)");
    tree->SetAlias("svdist",  "(nvtx == 2) * sqrt((x0-x1)**2 + (y0-y1)**2)");
    tree->SetAlias("svdphi",  "(nvtx == 2) * TVector2::Phi_mpi_pi(atan2(y0,x0)-atan2(y1,x1))");
    tree->SetAlias("svdz",    "(nvtx == 2) * (z0 - z1)");
  }

  void read_from_tree(TTree* tree, MiniNtuple& nt) {
    tree->SetBranchAddress("run", &nt.run);
    tree->SetBranchAddress("lumi", &nt.lumi);
    tree->SetBranchAddress("event", &nt.event);
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
    tree->SetBranchAddress("nvtx", &nt.nvtx);
    tree->SetBranchAddress("ntk0", &nt.ntk0);
    tree->SetBranchAddress("x0", &nt.x0);
    tree->SetBranchAddress("y0", &nt.y0);
    tree->SetBranchAddress("z0", &nt.z0);
    tree->SetBranchAddress("cxx0", &nt.cxx0);
    tree->SetBranchAddress("cxy0", &nt.cxy0);
    tree->SetBranchAddress("cxz0", &nt.cxz0);
    tree->SetBranchAddress("cyy0", &nt.cyy0);
    tree->SetBranchAddress("cyz0", &nt.cyz0);
    tree->SetBranchAddress("czz0", &nt.czz0);
    tree->SetBranchAddress("ntk1", &nt.ntk1);
    tree->SetBranchAddress("x1", &nt.x1);
    tree->SetBranchAddress("y1", &nt.y1);
    tree->SetBranchAddress("z1", &nt.z1);
    tree->SetBranchAddress("cxx1", &nt.cxx1);
    tree->SetBranchAddress("cxy1", &nt.cxy1);
    tree->SetBranchAddress("cxz1", &nt.cxz1);
    tree->SetBranchAddress("cyy1", &nt.cyy1);
    tree->SetBranchAddress("cyz1", &nt.cyz1);
    tree->SetBranchAddress("czz1", &nt.czz1);
  }
}
