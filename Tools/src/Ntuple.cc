#include "JMTucker/Tools/interface/Ntuple.h"

namespace jmt {
  BaseSubNtuple::BaseSubNtuple() {
    set_pfx("");
    clear();
  }

  void BaseSubNtuple::clear() {
    weight_ = 1;
    run_ = 0;
    lumi_ = 0;
    event_ = 0;
    pass_ = 0;
    npu_ = 0;
    rho_ = 0;
    nallpv_ = 0;
  }

  void BaseSubNtuple::write_to_tree(TTree* t) {
    t->Branch("weight", &weight_);
    t->Branch("run", &run_);
    t->Branch("lumi", &lumi_);
    t->Branch("event", &event_);
    t->Branch("pass", &pass_);
    t->Branch("npu", &npu_);
    t->Branch("rho", &rho_);
    t->Branch("nallpv", &nallpv_);
  }

  void BaseSubNtuple::read_from_tree(TTree* t) {
    t->SetBranchAddress("weight", &weight_);
    t->SetBranchAddress("run", &run_);
    t->SetBranchAddress("lumi", &lumi_);
    t->SetBranchAddress("event", &event_);
    t->SetBranchAddress("pass", &pass_);
    t->SetBranchAddress("npu", &npu_);
    t->SetBranchAddress("rho", &rho_);
    t->SetBranchAddress("nallpv", &nallpv_);
  }

  ////

  BeamspotSubNtuple::BeamspotSubNtuple() {
    set_pfx("bs");
    clear();
  }

  void BeamspotSubNtuple::clear() {
    x_ = 0;
    y_ = 0;
    z_ = 0;
    sigmaz_ = 0;
    dxdz_ = 0;
    dydz_ = 0;
    width_ = 0;
    err_x_ = 0;
    err_y_ = 0;
    err_z_ = 0;
    err_sigmaz_ = 0;
    err_dxdz_ = 0;
    err_dydz_ = 0;
    err_width_ = 0;
  }

  void BeamspotSubNtuple::write_to_tree(TTree* t) {
    t->Branch(TString::Format("%s_x", pfx()), &x_);
    t->Branch(TString::Format("%s_y", pfx()), &y_);
    t->Branch(TString::Format("%s_z", pfx()), &z_);
    t->Branch(TString::Format("%s_sigmaz", pfx()), &sigmaz_);
    t->Branch(TString::Format("%s_dxdz", pfx()), &dxdz_);
    t->Branch(TString::Format("%s_dydz", pfx()), &dydz_);
    t->Branch(TString::Format("%s_width", pfx()), &width_);
    t->Branch(TString::Format("%s_err_x", pfx()), &err_x_);
    t->Branch(TString::Format("%s_err_y", pfx()), &err_y_);
    t->Branch(TString::Format("%s_err_z", pfx()), &err_z_);
    t->Branch(TString::Format("%s_err_sigmaz", pfx()), &err_sigmaz_);
    t->Branch(TString::Format("%s_err_dxdz", pfx()), &err_dxdz_);
    t->Branch(TString::Format("%s_err_dydz", pfx()), &err_dydz_);
    t->Branch(TString::Format("%s_err_width", pfx()), &err_width_);
  }

  void BeamspotSubNtuple::read_from_tree(TTree* t) {
    t->SetBranchAddress(TString::Format("%s_x", pfx()), &x_);
    t->SetBranchAddress(TString::Format("%s_y", pfx()), &y_);
    t->SetBranchAddress(TString::Format("%s_z", pfx()), &z_);
    t->SetBranchAddress(TString::Format("%s_sigmaz", pfx()), &sigmaz_);
    t->SetBranchAddress(TString::Format("%s_dxdz", pfx()), &dxdz_);
    t->SetBranchAddress(TString::Format("%s_dydz", pfx()), &dydz_);
    t->SetBranchAddress(TString::Format("%s_width", pfx()), &width_);
    t->SetBranchAddress(TString::Format("%s_err_x", pfx()), &err_x_);
    t->SetBranchAddress(TString::Format("%s_err_y", pfx()), &err_y_);
    t->SetBranchAddress(TString::Format("%s_err_z", pfx()), &err_z_);
    t->SetBranchAddress(TString::Format("%s_err_sigmaz", pfx()), &err_sigmaz_);
    t->SetBranchAddress(TString::Format("%s_err_dxdz", pfx()), &err_dxdz_);
    t->SetBranchAddress(TString::Format("%s_err_dydz", pfx()), &err_dydz_);
    t->SetBranchAddress(TString::Format("%s_err_width", pfx()), &err_width_);
  }

  ////

  VerticesSubNtuple::VerticesSubNtuple() {
    set_pfx("v");
    clear();
    p_x_ = 0;
    p_y_ = 0;
    p_z_ = 0;
    p_chi2_ = 0;
    p_ndof_ = 0;
    p_ntracks_ = 0;
    p_score_ = 0;
    p_cxx_ = 0;
    p_cxy_ = 0;
    p_cxz_ = 0;
    p_cyy_ = 0;
    p_cyz_ = 0;
    p_czz_ = 0;
    p_misc_ = 0;
  }

  void VerticesSubNtuple::clear() {
    x_.clear();
    y_.clear();
    z_.clear();
    chi2_.clear();
    ndof_.clear();
    ntracks_.clear();
    score_.clear();
    cxx_.clear();
    cxy_.clear();
    cxz_.clear();
    cyy_.clear();
    cyz_.clear();
    czz_.clear();
    misc_.clear();
  }

  void VerticesSubNtuple::write_to_tree(TTree* t) {
    t->Branch(TString::Format("%s_x", pfx()), &x_);
    t->Branch(TString::Format("%s_y", pfx()), &y_);
    t->Branch(TString::Format("%s_z", pfx()), &z_);
    t->Branch(TString::Format("%s_chi2", pfx()), &chi2_);
    t->Branch(TString::Format("%s_ndof", pfx()), &ndof_);
    t->Branch(TString::Format("%s_ntracks", pfx()), &ntracks_);
    t->Branch(TString::Format("%s_score", pfx()), &score_);
    t->Branch(TString::Format("%s_cxx", pfx()), &cxx_);
    t->Branch(TString::Format("%s_cxy", pfx()), &cxy_);
    t->Branch(TString::Format("%s_cxz", pfx()), &cxz_);
    t->Branch(TString::Format("%s_cyy", pfx()), &cyy_);
    t->Branch(TString::Format("%s_cyz", pfx()), &cyz_);
    t->Branch(TString::Format("%s_czz", pfx()), &czz_);
    t->Branch(TString::Format("%s_misc", pfx()), &misc_);
    t->SetAlias(TString::Format("n%ss", pfx()), TString::Format("%s_x@.size()", pfx()));
  }

  void VerticesSubNtuple::read_from_tree(TTree* t) {
    t->SetBranchAddress(TString::Format("%s_x", pfx()), &p_x_);
    t->SetBranchAddress(TString::Format("%s_y", pfx()), &p_y_);
    t->SetBranchAddress(TString::Format("%s_z", pfx()), &p_z_);
    t->SetBranchAddress(TString::Format("%s_chi2", pfx()), &p_chi2_);
    t->SetBranchAddress(TString::Format("%s_ndof", pfx()), &p_ndof_);
    t->SetBranchAddress(TString::Format("%s_ntracks", pfx()), &p_ntracks_);
    t->SetBranchAddress(TString::Format("%s_score", pfx()), &p_score_);
    t->SetBranchAddress(TString::Format("%s_cxx", pfx()), &p_cxx_);
    t->SetBranchAddress(TString::Format("%s_cxy", pfx()), &p_cxy_);
    t->SetBranchAddress(TString::Format("%s_cxz", pfx()), &p_cxz_);
    t->SetBranchAddress(TString::Format("%s_cyy", pfx()), &p_cyy_);
    t->SetBranchAddress(TString::Format("%s_cyz", pfx()), &p_cyz_);
    t->SetBranchAddress(TString::Format("%s_czz", pfx()), &p_czz_);
    t->SetBranchAddress(TString::Format("%s_misc", pfx()), &p_misc_);
  }

  void VerticesSubNtuple::copy_vectors() {
    x_ = *p_x_;
    y_ = *p_y_;
    z_ = *p_z_;
    chi2_ = *p_chi2_;
    ndof_ = *p_ndof_;
    ntracks_ = *p_ntracks_;
    score_ = *p_score_;
    cxx_ = *p_cxx_;
    cxy_ = *p_cxy_;
    cxz_ = *p_cxz_;
    cyy_ = *p_cyy_;
    cyz_ = *p_cyz_;
    czz_ = *p_czz_;
    misc_ = *p_misc_;
  }

  ////

  TracksSubNtuple::TracksSubNtuple() {
    set_pfx("tk");
    clear();
    p_qpt_ = 0;
    p_eta_ = 0;
    p_phi_ = 0;
    p_vx_ = 0;
    p_vy_ = 0;
    p_vz_ = 0;
    p_cov_00_ = 0;
    p_cov_11_ = 0;
    p_cov_14_ = 0;
    p_cov_22_ = 0;
    p_cov_23_ = 0;
    p_cov_33_ = 0;
    p_cov_34_ = 0;
    p_cov_44_ = 0;
    p_chi2dof_ = 0;
    p_hp_ = 0;
    p_minhit_ = 0;
    p_maxhit_ = 0;
    p_maxpxhit_ = 0;
    p_which_jet_ = 0;
    p_which_pv_ = 0;
    p_misc_ = 0;
  }

  void TracksSubNtuple::clear() {
    qpt_.clear();
    eta_.clear();
    phi_.clear();
    vx_.clear();
    vy_.clear();
    vz_.clear();
    cov_00_.clear();
    cov_11_.clear();
    cov_14_.clear();
    cov_22_.clear();
    cov_23_.clear();
    cov_33_.clear();
    cov_34_.clear();
    cov_44_.clear();
    chi2dof_.clear();
    hp_.clear();
    minhit_.clear();
    maxhit_.clear();
    maxpxhit_.clear();
    which_jet_.clear();
    which_pv_.clear();
    misc_.clear();
  }

  void TracksSubNtuple::write_to_tree(TTree* t) {
    t->Branch(TString::Format("%s_qpt", pfx()), &qpt_);
    t->Branch(TString::Format("%s_eta", pfx()), &eta_);
    t->Branch(TString::Format("%s_phi", pfx()), &phi_);
    t->Branch(TString::Format("%s_vx", pfx()), &vx_);
    t->Branch(TString::Format("%s_vy", pfx()), &vy_);
    t->Branch(TString::Format("%s_vz", pfx()), &vz_);
    t->Branch(TString::Format("%s_cov_00", pfx()), &cov_00_);
    t->Branch(TString::Format("%s_cov_11", pfx()), &cov_11_);
    t->Branch(TString::Format("%s_cov_14", pfx()), &cov_14_);
    t->Branch(TString::Format("%s_cov_22", pfx()), &cov_22_);
    t->Branch(TString::Format("%s_cov_23", pfx()), &cov_23_);
    t->Branch(TString::Format("%s_cov_33", pfx()), &cov_33_);
    t->Branch(TString::Format("%s_cov_34", pfx()), &cov_34_);
    t->Branch(TString::Format("%s_cov_44", pfx()), &cov_44_);
    t->Branch(TString::Format("%s_chi2dof", pfx()), &chi2dof_);
    t->Branch(TString::Format("%s_hp", pfx()), &hp_);
    t->Branch(TString::Format("%s_minhit", pfx()), &minhit_);
    t->Branch(TString::Format("%s_maxhit", pfx()), &maxhit_);
    t->Branch(TString::Format("%s_maxpxhit", pfx()), &maxpxhit_);
    t->Branch(TString::Format("%s_which_jet", pfx()), &which_jet_);
    t->Branch(TString::Format("%s_which_pv", pfx()), &which_pv_);
    t->Branch(TString::Format("%s_misc", pfx()), &misc_);

    t->SetAlias(TString::Format("n%ss", pfx()), TString::Format("%s_qpt@.size()", pfx()));
    t->SetAlias(TString::Format("%s_q", pfx_), TString::Format("%s_qpt > 0 ? 1 : -1", pfx()));
    t->SetAlias(TString::Format("%s_pt", pfx_), TString::Format("abs(%s_qpt)", pfx()));
    t->SetAlias(TString::Format("%s_npxhits", pfx_), TString::Format("%s_hp & 0x7", pfx()));
    t->SetAlias(TString::Format("%s_nsthits", pfx_), TString::Format("(%s_hp >> 3) & 0x1f", pfx()));
    t->SetAlias(TString::Format("%s_npxlayers", pfx_), TString::Format("(%s_hp >> 8) & 0x7", pfx()));
    t->SetAlias(TString::Format("%s_nstlayers", pfx_), TString::Format("(%s_hp >> 11) & 0x1f", pfx()));
    t->SetAlias(TString::Format("%s_nhits", pfx_), TString::Format("%s_npxhits + %s_nsthits", pfx(), pfx()));
    t->SetAlias(TString::Format("%s_nlayers", pfx_), TString::Format("%s_npxlayers + %s_nstlayers", pfx(), pfx()));
    t->SetAlias(TString::Format("%s_min_r", pfx_), TString::Format("%s_minhit & 0xf", pfx()));
    t->SetAlias(TString::Format("%s_min_z", pfx_), TString::Format("%s_minhit >> 4", pfx()));
    t->SetAlias(TString::Format("%s_max_r", pfx_), TString::Format("%s_maxhit & 0xf", pfx()));
    t->SetAlias(TString::Format("%s_max_z", pfx_), TString::Format("%s_maxhit >> 4", pfx()));
    t->SetAlias(TString::Format("%s_maxpx_r", pfx_), TString::Format("%s_maxpxhit & 0xf", pfx()));
    t->SetAlias(TString::Format("%s_maxpx_z", pfx_), TString::Format("%s_maxpxhit >> 4", pfx()));
  }

  void TracksSubNtuple::read_from_tree(TTree* t) {
    t->SetBranchAddress(TString::Format("%s_qpt", pfx()), &p_qpt_);
    t->SetBranchAddress(TString::Format("%s_eta", pfx()), &p_eta_);
    t->SetBranchAddress(TString::Format("%s_phi", pfx()), &p_phi_);
    t->SetBranchAddress(TString::Format("%s_vx", pfx()), &p_vx_);
    t->SetBranchAddress(TString::Format("%s_vy", pfx()), &p_vy_);
    t->SetBranchAddress(TString::Format("%s_vz", pfx()), &p_vz_);
    t->SetBranchAddress(TString::Format("%s_cov_00", pfx()), &p_cov_00_);
    t->SetBranchAddress(TString::Format("%s_cov_11", pfx()), &p_cov_11_);
    t->SetBranchAddress(TString::Format("%s_cov_14", pfx()), &p_cov_14_);
    t->SetBranchAddress(TString::Format("%s_cov_22", pfx()), &p_cov_22_);
    t->SetBranchAddress(TString::Format("%s_cov_23", pfx()), &p_cov_23_);
    t->SetBranchAddress(TString::Format("%s_cov_33", pfx()), &p_cov_33_);
    t->SetBranchAddress(TString::Format("%s_cov_34", pfx()), &p_cov_34_);
    t->SetBranchAddress(TString::Format("%s_cov_44", pfx()), &p_cov_44_);
    t->SetBranchAddress(TString::Format("%s_chi2dof", pfx()), &p_chi2dof_);
    t->SetBranchAddress(TString::Format("%s_hp", pfx()), &p_hp_);
    t->SetBranchAddress(TString::Format("%s_minhit", pfx()), &p_minhit_);
    t->SetBranchAddress(TString::Format("%s_maxhit", pfx()), &p_maxhit_);
    t->SetBranchAddress(TString::Format("%s_maxpxhit", pfx()), &p_maxpxhit_);
    t->SetBranchAddress(TString::Format("%s_which_jet", pfx()), &p_which_jet_);
    t->SetBranchAddress(TString::Format("%s_which_pv", pfx()), &p_which_pv_);
    t->SetBranchAddress(TString::Format("%s_misc", pfx()), &p_misc_);
  }

  void TracksSubNtuple::copy_vectors() {
    qpt_ = *p_qpt_;
    eta_ = *p_eta_;
    phi_ = *p_phi_;
    vx_ = *p_vx_;
    vy_ = *p_vy_;
    vz_ = *p_vz_;
    cov_00_ = *p_cov_00_;
    cov_11_ = *p_cov_11_;
    cov_14_ = *p_cov_14_;
    cov_22_ = *p_cov_22_;
    cov_23_ = *p_cov_23_;
    cov_33_ = *p_cov_33_;
    cov_34_ = *p_cov_34_;
    cov_44_ = *p_cov_44_;
    chi2dof_ = *p_chi2dof_;
    hp_ = *p_hp_;
    minhit_ = *p_minhit_;
    maxhit_ = *p_maxhit_;
    maxpxhit_ = *p_maxpxhit_;
    which_jet_ = *p_which_jet_;
    which_pv_ = *p_which_pv_;
    misc_ = *p_misc_;
  }

  ////

  JetsSubNtuple::JetsSubNtuple() {
    set_pfx("jet");
    clear();
    p_pt_ = 0;
    p_eta_ = 0;
    p_phi_ = 0;
    p_energy_ = 0;
    p_uncorr_ = 0;
    p_ntracks_ = 0;
    p_bdisc_ = 0;
    p_genflavor_ = 0;
    p_misc_ = 0;
  }

  void JetsSubNtuple::clear() {
    pt_.clear();
    eta_.clear();
    phi_.clear();
    energy_.clear();
    uncorr_.clear();
    ntracks_.clear();
    bdisc_.clear();
    genflavor_.clear();
    misc_.clear();
  }

  void JetsSubNtuple::write_to_tree(TTree* t) {
    t->Branch(TString::Format("%s_pt", pfx()), &pt_);
    t->Branch(TString::Format("%s_eta", pfx()), &eta_);
    t->Branch(TString::Format("%s_phi", pfx()), &phi_);
    t->Branch(TString::Format("%s_energy", pfx()), &energy_);
    t->Branch(TString::Format("%s_uncorr", pfx()), &uncorr_);
    t->Branch(TString::Format("%s_ntracks", pfx()), &ntracks_);
    t->Branch(TString::Format("%s_bdisc", pfx()), &bdisc_);
    t->Branch(TString::Format("%s_genflavor", pfx()), &genflavor_);
    t->Branch(TString::Format("%s_misc", pfx()), &misc_);
  }

  void JetsSubNtuple::read_from_tree(TTree* t) {
    t->SetBranchAddress(TString::Format("%s_pt", pfx()), &p_pt_);
    t->SetBranchAddress(TString::Format("%s_eta", pfx()), &p_eta_);
    t->SetBranchAddress(TString::Format("%s_phi", pfx()), &p_phi_);
    t->SetBranchAddress(TString::Format("%s_energy", pfx()), &p_energy_);
    t->SetBranchAddress(TString::Format("%s_uncorr", pfx()), &p_uncorr_);
    t->SetBranchAddress(TString::Format("%s_ntracks", pfx()), &p_ntracks_);
    t->SetBranchAddress(TString::Format("%s_bdisc", pfx()), &p_bdisc_);
    t->SetBranchAddress(TString::Format("%s_genflavor", pfx()), &p_genflavor_);
    t->SetBranchAddress(TString::Format("%s_misc", pfx()), &p_misc_);
  }

  void JetsSubNtuple::copy_vectors() {
    pt_ = *p_pt_;
    eta_ = *p_eta_;
    phi_ = *p_phi_;
    energy_ = *p_energy_;
    uncorr_ = *p_uncorr_;
    ntracks_ = *p_ntracks_;
    bdisc_ = *p_bdisc_;
    genflavor_ = *p_genflavor_;
    misc_ = *p_misc_;
  }


  PFSubNtuple::PFSubNtuple() {
    set_pfx("pf");
    clear();
  }

  void PFSubNtuple::clear() {
    met_x_ = 0;
    met_y_ = 0;
  }

  void PFSubNtuple::write_to_tree(TTree* t) {
    t->Branch(TString::Format("%s_met_x", pfx()), &met_x_);
    t->Branch(TString::Format("%s_met_y", pfx()), &met_y_);
  }

  void PFSubNtuple::read_from_tree(TTree* t) {
    t->SetBranchAddress(TString::Format("%s_met_x", pfx()), &met_x_);
    t->SetBranchAddress(TString::Format("%s_met_y", pfx()), &met_y_);
  }

  //////
  MuTracksSubNtuple::MuTracksSubNtuple() {
    set_pfx("muons");
    clear();
    p_qpt_ = 0;
    p_eta_ = 0;
    p_phi_ = 0;
    p_vx_ = 0;
    p_vy_ = 0;
    p_vz_ = 0;
    p_cov_00_ = 0;
    p_cov_11_ = 0;
    p_cov_14_ = 0;
    p_cov_22_ = 0;
    p_cov_23_ = 0;
    p_cov_33_ = 0;
    p_cov_34_ = 0;
    p_cov_44_ = 0;
    p_chi2dof_ = 0;
    p_hp_ = 0;
    p_minhit_ = 0;
    p_maxhit_ = 0;
    p_maxpxhit_ = 0;
    p_losthit_ = 0;
  }

  void MuTracksSubNtuple::clear() {
    qpt_.clear();
    eta_.clear();
    phi_.clear();
    vx_.clear();
    vy_.clear();
    vz_.clear();
    cov_00_.clear();
    cov_11_.clear();
    cov_14_.clear();
    cov_22_.clear();
    cov_23_.clear();
    cov_33_.clear();
    cov_34_.clear();
    cov_44_.clear();
    chi2dof_.clear();
    hp_.clear();
    minhit_.clear();
    maxhit_.clear();
    maxpxhit_.clear();
    losthit_.clear();
  }

  void MuTracksSubNtuple::write_to_tree(TTree* t) {
    t->Branch(TString::Format("%s_qpt", pfx()), &qpt_);
    t->Branch(TString::Format("%s_eta", pfx()), &eta_);
    t->Branch(TString::Format("%s_phi", pfx()), &phi_);
    t->Branch(TString::Format("%s_vx", pfx()), &vx_);
    t->Branch(TString::Format("%s_vy", pfx()), &vy_);
    t->Branch(TString::Format("%s_vz", pfx()), &vz_);
    t->Branch(TString::Format("%s_cov_00", pfx()), &cov_00_);
    t->Branch(TString::Format("%s_cov_11", pfx()), &cov_11_);
    t->Branch(TString::Format("%s_cov_14", pfx()), &cov_14_);
    t->Branch(TString::Format("%s_cov_22", pfx()), &cov_22_);
    t->Branch(TString::Format("%s_cov_23", pfx()), &cov_23_);
    t->Branch(TString::Format("%s_cov_33", pfx()), &cov_33_);
    t->Branch(TString::Format("%s_cov_34", pfx()), &cov_34_);
    t->Branch(TString::Format("%s_cov_44", pfx()), &cov_44_);
    t->Branch(TString::Format("%s_chi2dof", pfx()), &chi2dof_);
    t->Branch(TString::Format("%s_hp", pfx()), &hp_);
    t->Branch(TString::Format("%s_minhit", pfx()), &minhit_);
    t->Branch(TString::Format("%s_maxhit", pfx()), &maxhit_);
    t->Branch(TString::Format("%s_maxpxhit", pfx()), &maxpxhit_);
    t->Branch(TString::Format("%s_losthit", pfx()), &losthit_);

    t->SetAlias(TString::Format("%s_q", pfx_), TString::Format("%s_qpt > 0 ? 1 : -1", pfx()));
    t->SetAlias(TString::Format("%s_pt", pfx_), TString::Format("abs(%s_qpt)", pfx()));
    t->SetAlias(TString::Format("%s_npxhits", pfx_), TString::Format("%s_hp & 0x7", pfx()));
    t->SetAlias(TString::Format("%s_nsthits", pfx_), TString::Format("(%s_hp >> 3) & 0x1f", pfx()));
    t->SetAlias(TString::Format("%s_npxlayers", pfx_), TString::Format("(%s_hp >> 8) & 0x7", pfx()));
    t->SetAlias(TString::Format("%s_nstlayers", pfx_), TString::Format("(%s_hp >> 11) & 0x1f", pfx()));
    t->SetAlias(TString::Format("%s_nhits", pfx_), TString::Format("%s_npxhits + %s_nsthits", pfx(), pfx()));
    t->SetAlias(TString::Format("%s_nlayers", pfx_), TString::Format("%s_npxlayers + %s_nstlayers", pfx(), pfx()));
    t->SetAlias(TString::Format("%s_min_r", pfx_), TString::Format("%s_minhit & 0xf", pfx()));
    t->SetAlias(TString::Format("%s_min_z", pfx_), TString::Format("%s_minhit >> 4", pfx()));
    t->SetAlias(TString::Format("%s_max_r", pfx_), TString::Format("%s_maxhit & 0xf", pfx()));
    t->SetAlias(TString::Format("%s_max_z", pfx_), TString::Format("%s_maxhit >> 4", pfx()));
    t->SetAlias(TString::Format("%s_maxpx_r", pfx_), TString::Format("%s_maxpxhit & 0xf", pfx()));
    t->SetAlias(TString::Format("%s_maxpx_z", pfx_), TString::Format("%s_maxpxhit >> 4", pfx()));
    
  }

  void MuTracksSubNtuple::read_from_tree(TTree* t) {
    t->SetBranchAddress(TString::Format("%s_qpt", pfx()), &p_qpt_);
    t->SetBranchAddress(TString::Format("%s_eta", pfx()), &p_eta_);
    t->SetBranchAddress(TString::Format("%s_phi", pfx()), &p_phi_);
    t->SetBranchAddress(TString::Format("%s_vx", pfx()), &p_vx_);
    t->SetBranchAddress(TString::Format("%s_vy", pfx()), &p_vy_);
    t->SetBranchAddress(TString::Format("%s_vz", pfx()), &p_vz_);
    t->SetBranchAddress(TString::Format("%s_cov_00", pfx()), &p_cov_00_);
    t->SetBranchAddress(TString::Format("%s_cov_11", pfx()), &p_cov_11_);
    t->SetBranchAddress(TString::Format("%s_cov_14", pfx()), &p_cov_14_);
    t->SetBranchAddress(TString::Format("%s_cov_22", pfx()), &p_cov_22_);
    t->SetBranchAddress(TString::Format("%s_cov_23", pfx()), &p_cov_23_);
    t->SetBranchAddress(TString::Format("%s_cov_33", pfx()), &p_cov_33_);
    t->SetBranchAddress(TString::Format("%s_cov_34", pfx()), &p_cov_34_);
    t->SetBranchAddress(TString::Format("%s_cov_44", pfx()), &p_cov_44_);
    t->SetBranchAddress(TString::Format("%s_chi2dof", pfx()), &p_chi2dof_);
    t->SetBranchAddress(TString::Format("%s_hp", pfx()), &p_hp_);
    t->SetBranchAddress(TString::Format("%s_minhit", pfx()), &p_minhit_);
    t->SetBranchAddress(TString::Format("%s_maxhit", pfx()), &p_maxhit_);
    t->SetBranchAddress(TString::Format("%s_maxpxhit", pfx()), &p_maxpxhit_);
    t->SetBranchAddress(TString::Format("%s_losthit", pfx()), &p_losthit_);

  }
  
  void MuTracksSubNtuple::copy_vectors() {
    qpt_ = *p_qpt_;
    eta_ = *p_eta_;
    phi_ = *p_phi_;
    vx_ = *p_vx_;
    vy_ = *p_vy_;
    vz_ = *p_vz_;
    cov_00_ = *p_cov_00_;
    cov_11_ = *p_cov_11_;
    cov_14_ = *p_cov_14_;
    cov_22_ = *p_cov_22_;
    cov_23_ = *p_cov_23_;
    cov_33_ = *p_cov_33_;
    cov_34_ = *p_cov_34_;
    cov_44_ = *p_cov_44_;
    chi2dof_ = *p_chi2dof_;
    hp_ = *p_hp_;
    minhit_ = *p_minhit_;
    maxhit_ = *p_maxhit_;
    maxpxhit_ = *p_maxpxhit_;
    losthit_ = *p_losthit_;
  }
    

  ////
  EleTracksSubNtuple::EleTracksSubNtuple() {
    set_pfx("electrons");
    clear();
    p_qpt_ = 0;
    p_eta_ = 0;
    p_phi_ = 0;
    p_vx_ = 0;
    p_vy_ = 0;
    p_vz_ = 0;
    p_cov_00_ = 0;
    p_cov_11_ = 0;
    p_cov_14_ = 0;
    p_cov_22_ = 0;
    p_cov_23_ = 0;
    p_cov_33_ = 0;
    p_cov_34_ = 0;
    p_cov_44_ = 0;
    p_chi2dof_ = 0;
    p_hp_ = 0;
    p_minhit_ = 0;
    p_maxhit_ = 0;
    p_maxpxhit_ = 0;
    p_losthit_ = 0;
  }
  
  void EleTracksSubNtuple::clear() {
    qpt_.clear();
    eta_.clear();
    phi_.clear();
    vx_.clear();
    vy_.clear();
    vz_.clear();
    cov_00_.clear();
    cov_11_.clear();
    cov_14_.clear();
    cov_22_.clear();
    cov_23_.clear();
    cov_33_.clear();
    cov_34_.clear();
    cov_44_.clear();
    chi2dof_.clear();
    hp_.clear();
    minhit_.clear();
    maxhit_.clear();
    maxpxhit_.clear();
    losthit_.clear();
  }

  void EleTracksSubNtuple::write_to_tree(TTree* t) {
    t->Branch(TString::Format("%s_qpt", pfx()), &qpt_);
    t->Branch(TString::Format("%s_eta", pfx()), &eta_);
    t->Branch(TString::Format("%s_phi", pfx()), &phi_);
    t->Branch(TString::Format("%s_vx", pfx()), &vx_);
    t->Branch(TString::Format("%s_vy", pfx()), &vy_);
    t->Branch(TString::Format("%s_vz", pfx()), &vz_);
    t->Branch(TString::Format("%s_cov_00", pfx()), &cov_00_);
    t->Branch(TString::Format("%s_cov_11", pfx()), &cov_11_);
    t->Branch(TString::Format("%s_cov_14", pfx()), &cov_14_);
    t->Branch(TString::Format("%s_cov_22", pfx()), &cov_22_);
    t->Branch(TString::Format("%s_cov_23", pfx()), &cov_23_);
    t->Branch(TString::Format("%s_cov_33", pfx()), &cov_33_);
    t->Branch(TString::Format("%s_cov_34", pfx()), &cov_34_);
    t->Branch(TString::Format("%s_cov_44", pfx()), &cov_44_);
    t->Branch(TString::Format("%s_chi2dof", pfx()), &chi2dof_);
    t->Branch(TString::Format("%s_hp", pfx()), &hp_);
    t->Branch(TString::Format("%s_minhit", pfx()), &minhit_);
    t->Branch(TString::Format("%s_maxhit", pfx()), &maxhit_);
    t->Branch(TString::Format("%s_maxpxhit", pfx()), &maxpxhit_);
    t->Branch(TString::Format("%s_losthit", pfx()), &losthit_);

    t->SetAlias(TString::Format("n%ss", pfx()), TString::Format("%s_qpt@.size()", pfx()));
    t->SetAlias(TString::Format("%s_q", pfx_), TString::Format("%s_qpt > 0 ? 1 : -1", pfx()));
    t->SetAlias(TString::Format("%s_pt", pfx_), TString::Format("abs(%s_qpt)", pfx()));
    t->SetAlias(TString::Format("%s_npxhits", pfx_), TString::Format("%s_hp & 0x7", pfx()));
    t->SetAlias(TString::Format("%s_nsthits", pfx_), TString::Format("(%s_hp >> 3) & 0x1f", pfx()));
    t->SetAlias(TString::Format("%s_npxlayers", pfx_), TString::Format("(%s_hp >> 8) & 0x7", pfx()));
    t->SetAlias(TString::Format("%s_nstlayers", pfx_), TString::Format("(%s_hp >> 11) & 0x1f", pfx()));
    t->SetAlias(TString::Format("%s_nhits", pfx_), TString::Format("%s_npxhits + %s_nsthits", pfx(), pfx()));
    t->SetAlias(TString::Format("%s_nlayers", pfx_), TString::Format("%s_npxlayers + %s_nstlayers", pfx(), pfx()));
    t->SetAlias(TString::Format("%s_min_r", pfx_), TString::Format("%s_minhit & 0xf", pfx()));
    t->SetAlias(TString::Format("%s_min_z", pfx_), TString::Format("%s_minhit >> 4", pfx()));
    t->SetAlias(TString::Format("%s_max_r", pfx_), TString::Format("%s_maxhit & 0xf", pfx()));
    t->SetAlias(TString::Format("%s_max_z", pfx_), TString::Format("%s_maxhit >> 4", pfx()));
    t->SetAlias(TString::Format("%s_maxpx_r", pfx_), TString::Format("%s_maxpxhit & 0xf", pfx()));
    t->SetAlias(TString::Format("%s_maxpx_z", pfx_), TString::Format("%s_maxpxhit >> 4", pfx()));
    
  }

  void EleTracksSubNtuple::read_from_tree(TTree* t) {
    t->SetBranchAddress(TString::Format("%s_qpt", pfx()), &p_qpt_);
    t->SetBranchAddress(TString::Format("%s_eta", pfx()), &p_eta_);
    t->SetBranchAddress(TString::Format("%s_phi", pfx()), &p_phi_);
    t->SetBranchAddress(TString::Format("%s_vx", pfx()), &p_vx_);
    t->SetBranchAddress(TString::Format("%s_vy", pfx()), &p_vy_);
    t->SetBranchAddress(TString::Format("%s_vz", pfx()), &p_vz_);
    t->SetBranchAddress(TString::Format("%s_cov_00", pfx()), &p_cov_00_);
    t->SetBranchAddress(TString::Format("%s_cov_11", pfx()), &p_cov_11_);
    t->SetBranchAddress(TString::Format("%s_cov_14", pfx()), &p_cov_14_);
    t->SetBranchAddress(TString::Format("%s_cov_22", pfx()), &p_cov_22_);
    t->SetBranchAddress(TString::Format("%s_cov_23", pfx()), &p_cov_23_);
    t->SetBranchAddress(TString::Format("%s_cov_33", pfx()), &p_cov_33_);
    t->SetBranchAddress(TString::Format("%s_cov_34", pfx()), &p_cov_34_);
    t->SetBranchAddress(TString::Format("%s_cov_44", pfx()), &p_cov_44_);
    t->SetBranchAddress(TString::Format("%s_chi2dof", pfx()), &p_chi2dof_);
    t->SetBranchAddress(TString::Format("%s_hp", pfx()), &p_hp_);
    t->SetBranchAddress(TString::Format("%s_minhit", pfx()), &p_minhit_);
    t->SetBranchAddress(TString::Format("%s_maxhit", pfx()), &p_maxhit_);
    t->SetBranchAddress(TString::Format("%s_maxpxhit", pfx()), &p_maxpxhit_);
    t->SetBranchAddress(TString::Format("%s_losthit", pfx()), &p_losthit_);
    
  }
  void EleTracksSubNtuple::copy_vectors() {
    qpt_ = *p_qpt_;
    eta_ = *p_eta_;
    phi_ = *p_phi_;
    vx_ = *p_vx_;
    vy_ = *p_vy_;
    vz_ = *p_vz_;
    cov_00_ = *p_cov_00_;
    cov_11_ = *p_cov_11_;
    cov_14_ = *p_cov_14_;
    cov_22_ = *p_cov_22_;
    cov_23_ = *p_cov_23_;
    cov_33_ = *p_cov_33_;
    cov_34_ = *p_cov_34_;
    cov_44_ = *p_cov_44_;
    chi2dof_ = *p_chi2dof_;
    hp_ = *p_hp_;
    minhit_ = *p_minhit_;
    maxhit_ = *p_maxhit_;
    maxpxhit_ = *p_maxpxhit_;
    losthit_ = *p_losthit_;
  }

}
