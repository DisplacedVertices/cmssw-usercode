#include "TFile.h"
#include "TTree.h"
#include "JMTucker/MFVNeutralino/interface/MiniNtuple.h"

namespace mfv {
  MiniNtuple::MiniNtuple() {
    clear();
    p_tk0_qchi2 = p_tk0_ndof = p_tk0_vx = p_tk0_vy = p_tk0_vz = p_tk0_px = p_tk0_py = p_tk0_pz = p_tk1_qchi2 = p_tk1_ndof = p_tk1_vx = p_tk1_vy = p_tk1_vz = p_tk1_px = p_tk1_py = p_tk1_pz = 0;
    p_tk0_inpv = p_tk1_inpv = 0;
    p_tk0_cov = p_tk1_cov = 0;
  }

  void MiniNtuple::clear() {
    run = lumi = 0;
    event = 0;
    gen_flavor_code = npv = npu = njets = nvtx = ntk0 = ntracksptgt30 = njetsntks0 = ntk1 = ntracksptgt31 = njetsntks1 = 0;
    pvx = pvy = pvz = weight = x0 = y0 = z0 = drmin0 = drmax0 = bs2derr0 = geo2ddist0 = x1 = y1 = z1 = drmin1 = drmax1 = bs2derr1 = geo2ddist1 = 0;
    for (int i = 0; i < 50; ++i) {
      jet_pt[i] = jet_eta[i] = jet_phi[i] = jet_energy[i] = 0;
      jet_id[i] = 0;
    }
    tk0_qchi2.clear();
    tk0_ndof.clear();
    tk0_vx.clear();
    tk0_vy.clear();
    tk0_vz.clear();
    tk0_px.clear();
    tk0_py.clear();
    tk0_pz.clear();
    tk0_inpv.clear();
    tk0_cov.clear();
    tk1_qchi2.clear();
    tk1_ndof.clear();
    tk1_vx.clear();
    tk1_vy.clear();
    tk1_vz.clear();
    tk1_px.clear();
    tk1_py.clear();
    tk1_pz.clear();
    tk1_inpv.clear();
    tk1_cov.clear();
  }

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
    tree->Branch("tk0_qchi2", &nt.tk0_qchi2);
    tree->Branch("tk0_ndof", &nt.tk0_ndof);
    tree->Branch("tk0_vx", &nt.tk0_vx);
    tree->Branch("tk0_vy", &nt.tk0_vy);
    tree->Branch("tk0_vz", &nt.tk0_vz);
    tree->Branch("tk0_px", &nt.tk0_px);
    tree->Branch("tk0_py", &nt.tk0_py);
    tree->Branch("tk0_pz", &nt.tk0_pz);
    tree->Branch("tk0_inpv", &nt.tk0_inpv);
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
    tree->Branch("tk1_qchi2", &nt.tk1_qchi2);
    tree->Branch("tk1_ndof", &nt.tk1_ndof);
    tree->Branch("tk1_vx", &nt.tk1_vx);
    tree->Branch("tk1_vy", &nt.tk1_vy);
    tree->Branch("tk1_vz", &nt.tk1_vz);
    tree->Branch("tk1_px", &nt.tk1_px);
    tree->Branch("tk1_py", &nt.tk1_py);
    tree->Branch("tk1_pz", &nt.tk1_pz);
    tree->Branch("tk1_inpv", &nt.tk1_inpv);
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

    tree->SetAlias("jetht", "Sum$((jet_pt>40)*jet_pt)");
    tree->SetAlias("dist0", "sqrt(x0**2 + y0**2)");
    tree->SetAlias("dist1", "sqrt(x1**2 + y1**2)");
    tree->SetAlias("phi0",  "atan2(y0,x0)");
    tree->SetAlias("phi1",  "atan2(y1,x1)");
    tree->SetAlias("svdist",  "(nvtx >= 2) * sqrt((x0-x1)**2 + (y0-y1)**2)");
    tree->SetAlias("svdphi",  "(nvtx >= 2) * TVector2::Phi_mpi_pi(atan2(y0,x0)-atan2(y1,x1))");
    tree->SetAlias("svdz",    "(nvtx >= 2) * (z0 - z1)");
  }

  void read_from_tree(TTree* tree, MiniNtuple& nt) {
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
    tree->SetBranchAddress("tk0_qchi2", &nt.p_tk0_qchi2);
    tree->SetBranchAddress("tk0_ndof", &nt.p_tk0_ndof);
    tree->SetBranchAddress("tk0_vx", &nt.p_tk0_vx);
    tree->SetBranchAddress("tk0_vy", &nt.p_tk0_vy);
    tree->SetBranchAddress("tk0_vz", &nt.p_tk0_vz);
    tree->SetBranchAddress("tk0_px", &nt.p_tk0_px);
    tree->SetBranchAddress("tk0_py", &nt.p_tk0_py);
    tree->SetBranchAddress("tk0_pz", &nt.p_tk0_pz);
    tree->SetBranchAddress("tk0_inpv", &nt.p_tk0_inpv);
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
    tree->SetBranchAddress("tk1_qchi2", &nt.p_tk1_qchi2);
    tree->SetBranchAddress("tk1_ndof", &nt.p_tk1_ndof);
    tree->SetBranchAddress("tk1_vx", &nt.p_tk1_vx);
    tree->SetBranchAddress("tk1_vy", &nt.p_tk1_vy);
    tree->SetBranchAddress("tk1_vz", &nt.p_tk1_vz);
    tree->SetBranchAddress("tk1_px", &nt.p_tk1_px);
    tree->SetBranchAddress("tk1_py", &nt.p_tk1_py);
    tree->SetBranchAddress("tk1_pz", &nt.p_tk1_pz);
    tree->SetBranchAddress("tk1_inpv", &nt.p_tk1_inpv);
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

  MiniNtuple* clone(const MiniNtuple& nt) {
    MiniNtuple* nnt = new MiniNtuple(nt);

    if (nt.p_tk0_qchi2) nnt->tk0_qchi2 = *nt.p_tk0_qchi2;
    if (nt.p_tk0_ndof ) nnt->tk0_ndof  = *nt.p_tk0_ndof;
    if (nt.p_tk0_vx   ) nnt->tk0_vx    = *nt.p_tk0_vx;
    if (nt.p_tk0_vy   ) nnt->tk0_vy    = *nt.p_tk0_vy;
    if (nt.p_tk0_vz   ) nnt->tk0_vz    = *nt.p_tk0_vz;
    if (nt.p_tk0_px   ) nnt->tk0_px    = *nt.p_tk0_px;
    if (nt.p_tk0_py   ) nnt->tk0_py    = *nt.p_tk0_py;
    if (nt.p_tk0_pz   ) nnt->tk0_pz    = *nt.p_tk0_pz;
    if (nt.p_tk0_inpv ) nnt->tk0_inpv  = *nt.p_tk0_inpv;
    if (nt.p_tk0_cov  ) nnt->tk0_cov   = *nt.p_tk0_cov;

    if (nt.p_tk1_qchi2) nnt->tk1_qchi2 = *nt.p_tk1_qchi2;
    if (nt.p_tk1_ndof ) nnt->tk1_ndof  = *nt.p_tk1_ndof;
    if (nt.p_tk1_vx   ) nnt->tk1_vx    = *nt.p_tk1_vx;
    if (nt.p_tk1_vy   ) nnt->tk1_vy    = *nt.p_tk1_vy;
    if (nt.p_tk1_vz   ) nnt->tk1_vz    = *nt.p_tk1_vz;
    if (nt.p_tk1_px   ) nnt->tk1_px    = *nt.p_tk1_px;
    if (nt.p_tk1_py   ) nnt->tk1_py    = *nt.p_tk1_py;
    if (nt.p_tk1_pz   ) nnt->tk1_pz    = *nt.p_tk1_pz;
    if (nt.p_tk1_inpv ) nnt->tk1_inpv  = *nt.p_tk1_inpv;
    if (nt.p_tk1_cov  ) nnt->tk1_cov   = *nt.p_tk1_cov;

    nnt->p_tk0_qchi2 = nnt->p_tk0_ndof = nnt->p_tk0_vx = nnt->p_tk0_vy = nnt->p_tk0_vz = nnt->p_tk0_px = nnt->p_tk0_py = nnt->p_tk0_pz = nnt->p_tk1_qchi2 = nnt->p_tk1_ndof = nnt->p_tk1_vx = nnt->p_tk1_vy = nnt->p_tk1_vz = nnt->p_tk1_px = nnt->p_tk1_py = nnt->p_tk1_pz = 0;
    nnt->p_tk0_inpv = nnt->p_tk1_inpv = 0;
    nnt->p_tk0_cov = nnt->p_tk1_cov = 0;

    return nnt;
  }

  long long loop(const char* fn, const char* tree_path, bool (*fcn)(long long, long long, const mfv::MiniNtuple&)) {
    TFile* f = TFile::Open(fn);
    assert(f);

    TTree* tree = (TTree*)f->Get(tree_path);
    assert(tree);

    mfv::MiniNtuple nt;
    mfv::read_from_tree(tree, nt);

    long long j = 0, je = tree->GetEntriesFast();
    for (; j < je; ++j) {
      if (tree->LoadTree(j) < 0) break;
      if (tree->GetEntry(j) <= 0) continue;
      if (!fcn(j, je, nt)) break;
    }

    f->Close();
    delete f;

    return j;
  }
}
