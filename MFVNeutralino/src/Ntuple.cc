#include "DVCode/MFVNeutralino/interface/Ntuple.h"

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
    set_pfx("v");
    clear();
    p_rescale_chi2_ = 0;
    p_rescale_x_ = 0;
    p_rescale_y_ = 0;
    p_rescale_z_ = 0;
    p_rescale_cxx_ = 0;
    p_rescale_cxy_ = 0;
    p_rescale_cxz_ = 0;
    p_rescale_cyy_ = 0;
    p_rescale_cyz_ = 0;
    p_rescale_czz_ = 0;
    p_njets_ = 0;
    p_bs2derr_ = 0;
    p_rescale_bs2derr_ = 0;
    p_genmatch_ = 0;
    p_pt_ = 0;
    p_eta_ = 0;
    p_phi_ = 0;
    p_mass_ = 0;
  }

  void VerticesSubNtuple::clear() {
    jmt::VerticesSubNtuple::clear();
    rescale_chi2_.clear();
    rescale_x_.clear();
    rescale_y_.clear();
    rescale_z_.clear();
    rescale_cxx_.clear();
    rescale_cxy_.clear();
    rescale_cxz_.clear();
    rescale_cyy_.clear();
    rescale_cyz_.clear();
    rescale_czz_.clear();
    njets_.clear();
    bs2derr_.clear();
    rescale_bs2derr_.clear();
    genmatch_.clear();
    pt_.clear();
    eta_.clear();
    phi_.clear();
    mass_.clear();
  }

  void VerticesSubNtuple::write_to_tree(TTree* t) {
    jmt::VerticesSubNtuple::write_to_tree(t);
    t->Branch(TString::Format("%s_rescale_chi2", pfx()), &rescale_chi2_);
    t->Branch(TString::Format("%s_rescale_x", pfx()), &rescale_x_);
    t->Branch(TString::Format("%s_rescale_y", pfx()), &rescale_y_);
    t->Branch(TString::Format("%s_rescale_z", pfx()), &rescale_z_);
    t->Branch(TString::Format("%s_rescale_cxx", pfx()), &rescale_cxx_);
    t->Branch(TString::Format("%s_rescale_cxy", pfx()), &rescale_cxy_);
    t->Branch(TString::Format("%s_rescale_cxz", pfx()), &rescale_cxz_);
    t->Branch(TString::Format("%s_rescale_cyy", pfx()), &rescale_cyy_);
    t->Branch(TString::Format("%s_rescale_cyz", pfx()), &rescale_cyz_);
    t->Branch(TString::Format("%s_rescale_czz", pfx()), &rescale_czz_);
    t->Branch(TString::Format("%s_njets", pfx()), &njets_);
    t->Branch(TString::Format("%s_bs2derr", pfx()), &bs2derr_);
    t->Branch(TString::Format("%s_rescale_bs2derr", pfx()), &rescale_bs2derr_);
    t->Branch(TString::Format("%s_genmatch", pfx()), &genmatch_);
    t->Branch(TString::Format("%s_pt", pfx()), &pt_);
    t->Branch(TString::Format("%s_eta", pfx()), &eta_);
    t->Branch(TString::Format("%s_phi", pfx()), &phi_);
    t->Branch(TString::Format("%s_mass", pfx()), &mass_);
  }

  void VerticesSubNtuple::read_from_tree(TTree* t) {
    jmt::VerticesSubNtuple::read_from_tree(t);
    t->SetBranchAddress(TString::Format("%s_rescale_chi2", pfx()), &p_rescale_chi2_);
    t->SetBranchAddress(TString::Format("%s_rescale_x", pfx()), &p_rescale_x_);
    t->SetBranchAddress(TString::Format("%s_rescale_y", pfx()), &p_rescale_y_);
    t->SetBranchAddress(TString::Format("%s_rescale_z", pfx()), &p_rescale_z_);
    t->SetBranchAddress(TString::Format("%s_rescale_cxx", pfx()), &p_rescale_cxx_);
    t->SetBranchAddress(TString::Format("%s_rescale_cxy", pfx()), &p_rescale_cxy_);
    t->SetBranchAddress(TString::Format("%s_rescale_cxz", pfx()), &p_rescale_cxz_);
    t->SetBranchAddress(TString::Format("%s_rescale_cyy", pfx()), &p_rescale_cyy_);
    t->SetBranchAddress(TString::Format("%s_rescale_cyz", pfx()), &p_rescale_cyz_);
    t->SetBranchAddress(TString::Format("%s_rescale_czz", pfx()), &p_rescale_czz_);
    t->SetBranchAddress(TString::Format("%s_njets", pfx()), &p_njets_);
    t->SetBranchAddress(TString::Format("%s_bs2derr", pfx()), &p_bs2derr_);
    t->SetBranchAddress(TString::Format("%s_rescale_bs2derr", pfx()), &p_rescale_bs2derr_);
    t->SetBranchAddress(TString::Format("%s_genmatch", pfx()), &p_genmatch_);
    t->SetBranchAddress(TString::Format("%s_pt", pfx()), &p_pt_);
    t->SetBranchAddress(TString::Format("%s_eta", pfx()), &p_eta_);
    t->SetBranchAddress(TString::Format("%s_phi", pfx()), &p_phi_);
    t->SetBranchAddress(TString::Format("%s_mass", pfx()), &p_mass_);
  }

  void VerticesSubNtuple::copy_vectors() {
    jmt::VerticesSubNtuple::copy_vectors();
    rescale_chi2_ = *p_rescale_chi2_;
    rescale_x_ = *p_rescale_x_;
    rescale_y_ = *p_rescale_y_;
    rescale_z_ = *p_rescale_z_;
    rescale_cxx_ = *p_rescale_cxx_;
    rescale_cxy_ = *p_rescale_cxy_;
    rescale_cxz_ = *p_rescale_cxz_;
    rescale_cyy_ = *p_rescale_cyy_;
    rescale_cyz_ = *p_rescale_cyz_;
    rescale_czz_ = *p_rescale_czz_;
    njets_ = *p_njets_;
    bs2derr_ = *p_bs2derr_;
    rescale_bs2derr_ = *p_rescale_bs2derr_;
    genmatch_ = *p_genmatch_;
    pt_ = *p_pt_;
    eta_ = *p_eta_;
    phi_ = *p_phi_;
    mass_ = *p_mass_;
  }

  ////

  MiniNtuple2SubNtuple::MiniNtuple2SubNtuple() {
    clear();
  }

  void MiniNtuple2SubNtuple::clear() {
    vcode_ = 0;
  }

  void MiniNtuple2SubNtuple::write_to_tree(TTree* t) {
    t->Branch("vcode", &vcode_);
  }

  void MiniNtuple2SubNtuple::read_from_tree(TTree* t) {
    t->SetBranchAddress("vcode", &vcode_);
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
