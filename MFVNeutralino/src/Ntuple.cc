#include "JMTucker/MFVNeutralino/interface/Ntuple.h"

namespace mfv {
  GenTruthSubNtuple::GenTruthSubNtuple() {
    clear();
    p_id_ = 0;
    p_pt_ = 0;
    p_eta_ = 0;
    p_phi_ = 0;
    p_mass_ = 0;
    p_decay_x_ = 0;
    p_decay_y_ = 0;
    p_decay_z_ = 0;
    p_bquark_pt_ = 0;
    p_bquark_eta_ = 0;
    p_bquark_phi_ = 0;
    p_lepton_is_el_ = 0;
    p_lepton_qpt_ = 0;
    p_lepton_eta_ = 0;
    p_lepton_phi_ = 0;
  }

  void GenTruthSubNtuple::clear() {
    valid_ = 0;
    vx_ = 0;
    vy_ = 0;
    vz_ = 0;
    saw_c_ = 0;
    saw_b_ = 0;
    id_.clear();
    pt_.clear();
    eta_.clear();
    phi_.clear();
    mass_.clear();
    decay_x_.clear();
    decay_y_.clear();
    decay_z_.clear();
    bquark_pt_.clear();
    bquark_eta_.clear();
    bquark_phi_.clear();
    lepton_is_el_.clear();
    lepton_qpt_.clear();
    lepton_eta_.clear();
    lepton_phi_.clear();
  }

  void GenTruthSubNtuple::write_to_tree(TTree* t) {
    t->Branch("gen_valid", &valid_);
    t->Branch("gen_vx", &vx_);
    t->Branch("gen_vy", &vy_);
    t->Branch("gen_vz", &vz_);
    t->Branch("gen_saw_c", &saw_c_);
    t->Branch("gen_saw_b", &saw_b_);
    t->Branch("gen_id", &id_);
    t->Branch("gen_pt", &pt_);
    t->Branch("gen_eta", &eta_);
    t->Branch("gen_phi", &phi_);
    t->Branch("gen_mass", &mass_);
    t->Branch("gen_decay_x", &decay_x_);
    t->Branch("gen_decay_y", &decay_y_);
    t->Branch("gen_decay_z", &decay_z_);
    t->Branch("gen_bquark_pt", &bquark_pt_);
    t->Branch("gen_bquark_eta", &bquark_eta_);
    t->Branch("gen_bquark_phi", &bquark_phi_);
    t->Branch("gen_lepton_is_el", &lepton_is_el_);
    t->Branch("gen_lepton_qpt", &lepton_qpt_);
    t->Branch("gen_lepton_eta", &lepton_eta_);
    t->Branch("gen_lepton_phi", &lepton_phi_);
  }

  void GenTruthSubNtuple::read_from_tree(TTree* t) {
    t->SetBranchAddress("gen_valid", &valid_);
    t->SetBranchAddress("gen_vx", &vx_);
    t->SetBranchAddress("gen_vy", &vy_);
    t->SetBranchAddress("gen_vz", &vz_);
    t->SetBranchAddress("gen_saw_c", &saw_c_);
    t->SetBranchAddress("gen_saw_b", &saw_b_);
    t->SetBranchAddress("gen_id", &p_id_);
    t->SetBranchAddress("gen_pt", &p_pt_);
    t->SetBranchAddress("gen_eta", &p_eta_);
    t->SetBranchAddress("gen_phi", &p_phi_);
    t->SetBranchAddress("gen_mass", &p_mass_);
    t->SetBranchAddress("gen_decay_x", &p_decay_x_);
    t->SetBranchAddress("gen_decay_y", &p_decay_y_);
    t->SetBranchAddress("gen_decay_z", &p_decay_z_);
    t->SetBranchAddress("gen_bquark_pt", &p_bquark_pt_);
    t->SetBranchAddress("gen_bquark_eta", &p_bquark_eta_);
    t->SetBranchAddress("gen_bquark_phi", &p_bquark_phi_);
    t->SetBranchAddress("gen_lepton_is_el", &p_lepton_is_el_);
    t->SetBranchAddress("gen_lepton_qpt", &p_lepton_qpt_);
    t->SetBranchAddress("gen_lepton_eta", &p_lepton_eta_);
    t->SetBranchAddress("gen_lepton_phi", &p_lepton_phi_);
  }

  void GenTruthSubNtuple::copy_vectors() {
    id_ = *p_id_;
    pt_ = *p_pt_;
    eta_ = *p_eta_;
    phi_ = *p_phi_;
    mass_ = *p_mass_;
    decay_x_ = *p_decay_x_;
    decay_y_ = *p_decay_y_;
    decay_z_ = *p_decay_z_;
    bquark_pt_ = *p_bquark_pt_;
    bquark_eta_ = *p_bquark_eta_;
    bquark_phi_ = *p_bquark_phi_;
    lepton_is_el_ = *p_lepton_is_el_;
    lepton_qpt_ = *p_lepton_qpt_;
    lepton_eta_ = *p_lepton_eta_;
    lepton_phi_ = *p_lepton_phi_;
  }

  ////

  VerticesSubNtuple::VerticesSubNtuple() {
    clear();
    p_x_ = 0;
    p_y_ = 0;
    p_z_ = 0;
    p_cxx_ = 0;
    p_cxy_ = 0;
    p_cxz_ = 0;
    p_cyy_ = 0;
    p_cyz_ = 0;
    p_czz_ = 0;
    p_ntracks_ = 0;
    p_bs2derr_ = 0;
    p_geo2ddist_ = 0;
    p_genmatch_ = 0;
    p_pt_ = 0;
    p_eta_ = 0;
    p_phi_ = 0;
    p_mass_ = 0;
    p_tkonlymass_ = 0;
  }

  void VerticesSubNtuple::clear() {
    x_.clear();
    y_.clear();
    z_.clear();
    cxx_.clear();
    cxy_.clear();
    cxz_.clear();
    cyy_.clear();
    cyz_.clear();
    czz_.clear();
    ntracks_.clear();
    bs2derr_.clear();
    geo2ddist_.clear();
    genmatch_.clear();
    pt_.clear();
    eta_.clear();
    phi_.clear();
    mass_.clear();
    tkonlymass_.clear();
  }

  void VerticesSubNtuple::write_to_tree(TTree* t) {
    t->Branch("v_x", &x_);
    t->Branch("v_y", &y_);
    t->Branch("v_z", &z_);
    t->Branch("v_cxx", &cxx_);
    t->Branch("v_cxy", &cxy_);
    t->Branch("v_cxz", &cxz_);
    t->Branch("v_cyy", &cyy_);
    t->Branch("v_cyz", &cyz_);
    t->Branch("v_czz", &czz_);
    t->Branch("v_ntracks", &ntracks_);
    t->Branch("v_bs2derr", &bs2derr_);
    t->Branch("v_geo2ddist", &geo2ddist_);
    t->Branch("v_genmatch", &genmatch_);
    t->Branch("v_pt", &pt_);
    t->Branch("v_eta", &eta_);
    t->Branch("v_phi", &phi_);
    t->Branch("v_mass", &mass_);
    t->Branch("v_tkonlymass", &tkonlymass_);
  }

  void VerticesSubNtuple::read_from_tree(TTree* t) {
    t->SetBranchAddress("v_x", &p_x_);
    t->SetBranchAddress("v_y", &p_y_);
    t->SetBranchAddress("v_z", &p_z_);
    t->SetBranchAddress("v_cxx", &p_cxx_);
    t->SetBranchAddress("v_cxy", &p_cxy_);
    t->SetBranchAddress("v_cxz", &p_cxz_);
    t->SetBranchAddress("v_cyy", &p_cyy_);
    t->SetBranchAddress("v_cyz", &p_cyz_);
    t->SetBranchAddress("v_czz", &p_czz_);
    t->SetBranchAddress("v_ntracks", &p_ntracks_);
    t->SetBranchAddress("v_bs2derr", &p_bs2derr_);
    t->SetBranchAddress("v_geo2ddist", &p_geo2ddist_);
    t->SetBranchAddress("v_genmatch", &p_genmatch_);
    t->SetBranchAddress("v_pt", &p_pt_);
    t->SetBranchAddress("v_eta", &p_eta_);
    t->SetBranchAddress("v_phi", &p_phi_);
    t->SetBranchAddress("v_mass", &p_mass_);
    t->SetBranchAddress("v_tkonlymass", &p_tkonlymass_);
  }

  void VerticesSubNtuple::copy_vectors() {
    x_ = *p_x_;
    y_ = *p_y_;
    z_ = *p_z_;
    cxx_ = *p_cxx_;
    cxy_ = *p_cxy_;
    cxz_ = *p_cxz_;
    cyy_ = *p_cyy_;
    cyz_ = *p_cyz_;
    czz_ = *p_czz_;
    ntracks_ = *p_ntracks_;
    bs2derr_ = *p_bs2derr_;
    geo2ddist_ = *p_geo2ddist_;
    genmatch_ = *p_genmatch_;
    pt_ = *p_pt_;
    eta_ = *p_eta_;
    phi_ = *p_phi_;
    mass_ = *p_mass_;
    tkonlymass_ = *p_tkonlymass_;
  }

  ////

  MovedTracksSubNtuple::MovedTracksSubNtuple() {
    clear();
  }

  void MovedTracksSubNtuple::clear() {
    nalltracks_ = 0;
    nmovedtracks_ = 0;
    npreseljets_ = 0;
    npreselbjets_ = 0;
    move_x_ = 0;
    move_y_ = 0;
    move_z_ = 0;
  }

  void MovedTracksSubNtuple::write_to_tree(TTree* t) {
    t->Branch("nalltracks", &nalltracks_);
    t->Branch("nmovedtracks", &nmovedtracks_);
    t->Branch("npreseljets", &npreseljets_);
    t->Branch("npreselbjets", &npreselbjets_);
    t->Branch("move_x", &move_x_);
    t->Branch("move_y", &move_y_);
    t->Branch("move_z", &move_z_);
  }

  void MovedTracksSubNtuple::read_from_tree(TTree* t) {
    t->SetBranchAddress("nalltracks", &nalltracks_);
    t->SetBranchAddress("nmovedtracks", &nmovedtracks_);
    t->SetBranchAddress("npreseljets", &npreseljets_);
    t->SetBranchAddress("npreselbjets", &npreselbjets_);
    t->SetBranchAddress("move_x", &move_x_);
    t->SetBranchAddress("move_y", &move_y_);
    t->SetBranchAddress("move_z", &move_z_);
  }
}
