#include "JMTucker/MFVNeutralino/interface/MovedTracksNtuple.h"

#include "TTree.h"
#include "TVector3.h"

namespace mfv {
  TVector3 MovedTracksNtuple::move_vector() const {
    return TVector3(move_x + bsx_at_z(move_z) - (pvx + bsx_at_z(pvz)),
                    move_y + bsy_at_z(move_z) - (pvy + bsy_at_z(pvz)),
                    move_z - pvz);
  }

  double MovedTracksNtuple::move_tau() const { return move_vector().Mag(); }

  std::vector<int> MovedTracksNtuple::vtxs_tracks(int i) const {
    std::vector<int> r;
    for (size_t j = 0, je = ntks(); j < je; ++j)
      if ((p_tks_vtx ? (*p_tks_vtx)[j] : tks_vtx[j]) == i)
        r.push_back(j);
    assert(r.size() == (p_vtxs_ntracks ? (*p_vtxs_ntracks)[i] : vtxs_ntracks[i]));
    return r;
  }

  MovedTracksNtuple::MovedTracksNtuple() {
    clear();
    p_alljets_pt = p_alljets_eta = p_alljets_phi = p_alljets_energy = p_alljets_bdisc = p_vtxs_x = p_vtxs_y = p_vtxs_z = p_vtxs_pt = p_vtxs_theta = p_vtxs_phi = p_vtxs_mass = p_vtxs_tkonlymass = p_vtxs_bs2derr = p_tks_qpt = p_tks_eta = p_tks_phi = p_tks_dxy = p_tks_dz = p_tks_err_pt = p_tks_err_eta = p_tks_err_phi = p_tks_err_dxy = p_tks_err_dz = 0;
    p_tks_hp_ = 0;
    p_alljets_ntracks = p_alljets_hadronflavor = p_vtxs_ntracks = p_tks_vtx = 0;
    p_alljets_moved = p_tks_moved = 0;
  }

  void MovedTracksNtuple::clear() {
    run = lumi = 0;
    event = 0;
    weight = bsx = bsy = bsz = bsdxdz = bsdydz = pvx = pvy = pvz = pvsumpt2 = jetht = move_x = move_y = move_z = 0;
    gen_valid = 0;
    pass_hlt = npu = npv = nmovedtracks = npreseljets = npreselbjets = 0;
    pvntracks = ntracks = 0;
    for (int i = 0; i < 2; ++i) {
      gen_lsp_pt[i] = gen_lsp_eta[i] = gen_lsp_phi[i] = gen_lsp_mass[i] = 0;
      gen_decay_type[i] = 0;
      for (int j = 0; j < 3; ++j)
        gen_lsp_decay[i*3+j] = 0;
    }

    alljets_pt.clear();
    alljets_eta.clear();
    alljets_phi.clear();
    alljets_energy.clear();
    alljets_ntracks.clear();
    alljets_bdisc.clear();
    alljets_hadronflavor.clear();
    alljets_moved.clear();
    vtxs_x.clear();
    vtxs_y.clear();
    vtxs_z.clear();
    vtxs_pt.clear();
    vtxs_theta.clear();
    vtxs_phi.clear();
    vtxs_mass.clear();
    vtxs_tkonlymass.clear();
    vtxs_ntracks.clear();
    vtxs_bs2derr.clear();
    tks_qpt.clear();
    tks_eta.clear();
    tks_phi.clear();
    tks_dxy.clear();
    tks_dz.clear();
    tks_err_pt.clear();
    tks_err_eta.clear();
    tks_err_phi.clear();
    tks_err_dxy.clear();
    tks_err_dz.clear();
    tks_hp_.clear();
    tks_moved.clear();
    tks_vtx.clear();
  }

  void MovedTracksNtuple::write_to_tree(TTree* tree) {
    tree->Branch("run", &run);
    tree->Branch("lumi", &lumi);
    tree->Branch("event", &event);
    tree->Branch("weight", &weight);
    tree->Branch("gen_valid", &gen_valid, "gen_valid/O");
    tree->Branch("gen_lsp_pt", gen_lsp_pt, "gen_lsp_pt[2]/F");
    tree->Branch("gen_lsp_eta", gen_lsp_eta, "gen_lsp_eta[2]/F");
    tree->Branch("gen_lsp_phi", gen_lsp_phi, "gen_lsp_phi[2]/F");
    tree->Branch("gen_lsp_mass", gen_lsp_mass, "gen_lsp_mass[2]/F");
    tree->Branch("gen_lsp_decay", gen_lsp_decay, "gen_lsp_decay[6]/F");
    tree->Branch("gen_decay_type", gen_decay_type, "gen_decay_type[2]/b");
    tree->Branch("pass_hlt", &pass_hlt);
    tree->Branch("bsx", &bsx);
    tree->Branch("bsy", &bsy);
    tree->Branch("bsz", &bsz);
    tree->Branch("bsdxdz", &bsdxdz);
    tree->Branch("bsdydz", &bsdydz);
    tree->Branch("npu", &npu);
    tree->Branch("npv", &npv);
    tree->Branch("pvx", &pvx);
    tree->Branch("pvy", &pvy);
    tree->Branch("pvz", &pvz);
    tree->Branch("pvntracks", &pvntracks);
    tree->Branch("pvsumpt2", &pvsumpt2);
    tree->Branch("jetht", &jetht);
    tree->Branch("ntracks", &ntracks);
    tree->Branch("nmovedtracks", &nmovedtracks);
    tree->Branch("npreseljets", &npreseljets);
    tree->Branch("npreselbjets", &npreselbjets);
    tree->Branch("alljets_pt", &alljets_pt);
    tree->Branch("alljets_eta", &alljets_eta);
    tree->Branch("alljets_phi", &alljets_phi);
    tree->Branch("alljets_energy", &alljets_energy);
    tree->Branch("alljets_ntracks", &alljets_ntracks);
    tree->Branch("alljets_bdisc", &alljets_bdisc);
    tree->Branch("alljets_hadronflavor", &alljets_hadronflavor);
    tree->Branch("alljets_moved", &alljets_moved);
    tree->Branch("move_x", &move_x);
    tree->Branch("move_y", &move_y);
    tree->Branch("move_z", &move_z);
    tree->Branch("vtxs_x", &vtxs_x);
    tree->Branch("vtxs_y", &vtxs_y);
    tree->Branch("vtxs_z", &vtxs_z);
    tree->Branch("vtxs_pt", &vtxs_pt);
    tree->Branch("vtxs_theta", &vtxs_theta);
    tree->Branch("vtxs_phi", &vtxs_phi);
    tree->Branch("vtxs_mass", &vtxs_mass);
    tree->Branch("vtxs_tkonlymass", &vtxs_tkonlymass);
    tree->Branch("vtxs_ntracks", &vtxs_ntracks);
    tree->Branch("vtxs_bs2derr", &vtxs_bs2derr);
    tree->Branch("tks_qpt", &tks_qpt);
    tree->Branch("tks_eta", &tks_eta);
    tree->Branch("tks_phi", &tks_phi);
    tree->Branch("tks_dxy", &tks_dxy);
    tree->Branch("tks_dz", &tks_dz);
    tree->Branch("tks_err_pt", &tks_err_pt);
    tree->Branch("tks_err_eta", &tks_err_eta);
    tree->Branch("tks_err_phi", &tks_err_phi);
    tree->Branch("tks_err_dxy", &tks_err_dxy);
    tree->Branch("tks_err_dz", &tks_err_dz);
    tree->Branch("tks_hp_", &tks_hp_);
    tree->Branch("tks_moved", &tks_moved);
    tree->Branch("tks_vtx", &tks_vtx);
  }

  void MovedTracksNtuple::read_from_tree(TTree* tree) {
    tree->SetBranchAddress("run", &run);
    tree->SetBranchAddress("lumi", &lumi);
    tree->SetBranchAddress("event", &event);
    tree->SetBranchAddress("weight", &weight);
    tree->SetBranchAddress("gen_valid", &gen_valid);
    tree->SetBranchAddress("gen_lsp_pt", gen_lsp_pt);
    tree->SetBranchAddress("gen_lsp_eta", gen_lsp_eta);
    tree->SetBranchAddress("gen_lsp_phi", gen_lsp_phi);
    tree->SetBranchAddress("gen_lsp_mass", gen_lsp_mass);
    tree->SetBranchAddress("gen_lsp_decay", gen_lsp_decay);
    tree->SetBranchAddress("gen_decay_type", gen_decay_type);
    tree->SetBranchAddress("pass_hlt", &pass_hlt);
    tree->SetBranchAddress("bsx", &bsx);
    tree->SetBranchAddress("bsy", &bsy);
    tree->SetBranchAddress("bsz", &bsz);
    tree->SetBranchAddress("bsdxdz", &bsdxdz);
    tree->SetBranchAddress("bsdydz", &bsdydz);
    tree->SetBranchAddress("npu", &npu);
    tree->SetBranchAddress("npv", &npv);
    tree->SetBranchAddress("pvx", &pvx);
    tree->SetBranchAddress("pvy", &pvy);
    tree->SetBranchAddress("pvz", &pvz);
    tree->SetBranchAddress("pvntracks", &pvntracks);
    tree->SetBranchAddress("pvsumpt2", &pvsumpt2);
    tree->SetBranchAddress("jetht", &jetht);
    tree->SetBranchAddress("ntracks", &ntracks);
    tree->SetBranchAddress("nmovedtracks", &nmovedtracks);
    tree->SetBranchAddress("npreseljets", &npreseljets);
    tree->SetBranchAddress("npreselbjets", &npreselbjets);
    tree->SetBranchAddress("alljets_pt", &p_alljets_pt);
    tree->SetBranchAddress("alljets_eta", &p_alljets_eta);
    tree->SetBranchAddress("alljets_phi", &p_alljets_phi);
    tree->SetBranchAddress("alljets_energy", &p_alljets_energy);
    tree->SetBranchAddress("alljets_ntracks", &p_alljets_ntracks);
    tree->SetBranchAddress("alljets_bdisc", &p_alljets_bdisc);
    tree->SetBranchAddress("alljets_hadronflavor", &p_alljets_hadronflavor);
    tree->SetBranchAddress("alljets_moved", &p_alljets_moved);
    tree->SetBranchAddress("move_x", &move_x);
    tree->SetBranchAddress("move_y", &move_y);
    tree->SetBranchAddress("move_z", &move_z);
    tree->SetBranchAddress("vtxs_x", &p_vtxs_x);
    tree->SetBranchAddress("vtxs_y", &p_vtxs_y);
    tree->SetBranchAddress("vtxs_z", &p_vtxs_z);
    tree->SetBranchAddress("vtxs_pt", &p_vtxs_pt);
    tree->SetBranchAddress("vtxs_theta", &p_vtxs_theta);
    tree->SetBranchAddress("vtxs_phi", &p_vtxs_phi);
    tree->SetBranchAddress("vtxs_mass", &p_vtxs_mass);
    tree->SetBranchAddress("vtxs_tkonlymass", &p_vtxs_tkonlymass);
    tree->SetBranchAddress("vtxs_ntracks", &p_vtxs_ntracks);
    tree->SetBranchAddress("vtxs_bs2derr", &p_vtxs_bs2derr);
    tree->SetBranchAddress("tks_qpt", &p_tks_qpt);
    tree->SetBranchAddress("tks_eta", &p_tks_eta);
    tree->SetBranchAddress("tks_phi", &p_tks_phi);
    tree->SetBranchAddress("tks_dxy", &p_tks_dxy);
    tree->SetBranchAddress("tks_dz", &p_tks_dz);
    tree->SetBranchAddress("tks_err_pt", &p_tks_err_pt);
    tree->SetBranchAddress("tks_err_eta", &p_tks_err_eta);
    tree->SetBranchAddress("tks_err_phi", &p_tks_err_phi);
    tree->SetBranchAddress("tks_err_dxy", &p_tks_err_dxy);
    tree->SetBranchAddress("tks_err_dz", &p_tks_err_dz);
    tree->SetBranchAddress("tks_hp_", &p_tks_hp_);
    tree->SetBranchAddress("tks_moved", &p_tks_moved);
    tree->SetBranchAddress("tks_vtx", &p_tks_vtx);
  }
}
