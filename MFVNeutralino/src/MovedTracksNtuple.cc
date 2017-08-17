#include "JMTucker/MFVNeutralino/interface/MovedTracksNtuple.h"

#include "TTree.h"

namespace mfv {
  MovedTracksNtuple::MovedTracksNtuple() {
    clear();
    p_jets_pt = p_jets_eta = p_jets_phi = p_jets_energy = p_vtxs_x = p_vtxs_y = p_vtxs_z = p_vtxs_pt = p_vtxs_theta = p_vtxs_phi = p_vtxs_mass = p_vtxs_tkonlymass = p_vtxs_anglemin = p_vtxs_anglemax = p_vtxs_bs2derr = 0;
    p_jets_ntracks = p_vtxs_ntracks = 0;
  }

  void MovedTracksNtuple::clear() {
    run = lumi = 0;
    event = 0;
    weight = pvx = pvy = pvz = pvsumpt2 = jetht = move_x = move_y = move_z = 0;
    for (int i = 0; i < 2; ++i) {
      gen_lsp_pt[i] = gen_lsp_eta[i] = gen_lsp_phi[i] = gen_lsp_mass[i] = 0;
      gen_decay_type[i] = 0;
      for (int j = 0; j < 3; ++j)
        gen_lsp_decay[i*3+j] = 0;
    }
    gen_partons_in_acc = pass_hlt = npu = npv = nseltracks = nalljets = npreseljets = npreselbjets = nlightjets = 0;
    pvntracks = ntracks = 0;
    jets_pt.clear();
    jets_eta.clear();
    jets_phi.clear();
    jets_energy.clear();
    jets_ntracks.clear();
    vtxs_x.clear();
    vtxs_y.clear();
    vtxs_z.clear();
    vtxs_pt.clear();
    vtxs_theta.clear();
    vtxs_phi.clear();
    vtxs_mass.clear();
    vtxs_tkonlymass.clear();
    vtxs_ntracks.clear();
    vtxs_anglemin.clear();
    vtxs_anglemax.clear();
    vtxs_bs2derr.clear();
  }

  void MovedTracksNtuple::write_to_tree(TTree* tree) {
    tree->SetAlias("njets", "jets_pt@.size()");
    tree->SetAlias("nvtxs", "vtxs_x@.size()");

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
    tree->Branch("gen_decay_type", gen_decay_type, "gen_decay_type[2]/s"); // JMTBAD
    tree->Branch("gen_partons_in_acc", &gen_partons_in_acc);
    tree->Branch("pass_hlt", &pass_hlt);
    tree->Branch("npu", &npu);
    tree->Branch("npv", &npv);
    tree->Branch("pvx", &pvx);
    tree->Branch("pvy", &pvy);
    tree->Branch("pvz", &pvz);
    tree->Branch("pvntracks", &pvntracks);
    tree->Branch("pvsumpt2", &pvsumpt2);
    tree->Branch("jetht", &jetht);
    tree->Branch("ntracks", &ntracks);
    tree->Branch("nseltracks", &nseltracks);
    tree->Branch("nalljets", &nalljets);
    tree->Branch("npreseljets", &npreseljets);
    tree->Branch("npreselbjets", &npreselbjets);
    tree->Branch("nlightjets", &nlightjets);
    tree->Branch("jets_pt", &jets_pt);
    tree->Branch("jets_eta", &jets_eta);
    tree->Branch("jets_phi", &jets_phi);
    tree->Branch("jets_energy", &jets_energy);
    tree->Branch("jets_ntracks", &jets_ntracks);
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
    tree->Branch("vtxs_anglemin", &vtxs_anglemin);
    tree->Branch("vtxs_anglemax", &vtxs_anglemax);
    tree->Branch("vtxs_bs2derr", &vtxs_bs2derr);
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
    tree->SetBranchAddress("gen_partons_in_acc", &gen_partons_in_acc);
    tree->SetBranchAddress("pass_hlt", &pass_hlt);
    tree->SetBranchAddress("npu", &npu);
    tree->SetBranchAddress("npv", &npv);
    tree->SetBranchAddress("pvx", &pvx);
    tree->SetBranchAddress("pvy", &pvy);
    tree->SetBranchAddress("pvz", &pvz);
    tree->SetBranchAddress("pvntracks", &pvntracks);
    tree->SetBranchAddress("pvsumpt2", &pvsumpt2);
    tree->SetBranchAddress("jetht", &jetht);
    tree->SetBranchAddress("ntracks", &ntracks);
    tree->SetBranchAddress("nseltracks", &nseltracks);
    tree->SetBranchAddress("nalljets", &nalljets);
    tree->SetBranchAddress("npreseljets", &npreseljets);
    tree->SetBranchAddress("npreselbjets", &npreselbjets);
    tree->SetBranchAddress("nlightjets", &nlightjets);
    tree->SetBranchAddress("jets_pt", &p_jets_pt);
    tree->SetBranchAddress("jets_eta", &p_jets_eta);
    tree->SetBranchAddress("jets_phi", &p_jets_phi);
    tree->SetBranchAddress("jets_energy", &p_jets_energy);
    tree->SetBranchAddress("jets_ntracks", &p_jets_ntracks);
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
    tree->SetBranchAddress("vtxs_anglemin", &p_vtxs_anglemin);
    tree->SetBranchAddress("vtxs_anglemax", &p_vtxs_anglemax);
    tree->SetBranchAddress("vtxs_bs2derr", &p_vtxs_bs2derr);
  }
}
