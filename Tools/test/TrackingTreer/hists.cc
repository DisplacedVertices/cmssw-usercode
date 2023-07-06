#include "TH2.h"
#include "JMTucker/MFVNeutralino/interface/Ntuple.h"
#include "JMTucker/Tools/interface/NtupleReader.h"


int main(int argc, char** argv) {
  jmt::NtupleReader<jmt::TrackingAndJetsNtuple> nr;
  // nr.init_options("tt/t", "TrackingTreerHistsV23mv3", "nr_trackingtreerv23mv3", "ttbar=False, all_signal=False");
  //need to include scale type 
  nr.init_options("tt/t", "TrackingTreerULV2_Lepm_cut0_etalt1p5_2018_wsellep", "trackingtreerulv2_lepm", "ttbar=False, leptonic=False, all_signal=False, qcd_lep=False, met=False, diboson=False, Lepton_data=False ");
  //nr.init_options("tt/t", "TrackingTreerULV1_Lepm_etagt1p5_eraF_2017", "trackingtreerulv1_lepm_wsellep", "ttbar=False, leptonic=True, all_signal=False, qcd_lep=True, met=True, diboson=True, Lepton_data=False ");
  if (!nr.parse_options(argc, argv) || !nr.init()) return 1;
  auto& nt = nr.nt();
  auto& ntt = nt.tracks();
  //try : mu_tracks() & ele_tracks()
  auto& ntm = nt.mu_tracks();
  auto& nte = nt.ele_tracks();

  TH1D* h_npv = new TH1D("h_npv", ";number of primary vertices", 50, 0, 50);
  TH1D* h_bsx = new TH1D("h_bsx", ";beamspot x", 400, -0.15, 0.15);
  TH1D* h_bsy = new TH1D("h_bsy", ";beamspot y", 400, -0.15, 0.15);
  TH1D* h_bsz = new TH1D("h_bsz", ";beamspot z", 800, -5, 5);
  TH1D* h_bsdxdz = new TH1D("h_bsdxdz", ";beamspot dx/dz", 100, -1e-4, 5e-4);
  TH1D* h_bsdydz = new TH1D("h_bsdydz", ";beamspot dy/dz", 100, -1e-4, 1e-4);
  TH1D* h_pvbsx = new TH1D("h_pvbsx", ";pvx - bsx", 400, -0.05, 0.05);
  TH1D* h_pvbsy = new TH1D("h_pvbsy", ";pvy - bsy", 400, -0.05, 0.05); 
  TH1D* h_pvbsz = new TH1D("h_pvbsz", ";pvz - bsz", 500, -15, 15);
  TH2D* h_bsy_v_bsx = new TH2D("h_bsy_v_bsx", ";beamspot x;beamspot y", 4000, -1, 1, 4000, -1, 1);
  TH2D* h_pvy_v_pvx = new TH2D("h_pvy_v_pvx", ";pvx;pvy", 400, -1, 1, 400, -1, 1);

  //going to first try with no extra selections; just the track selection
  enum { ele_all, ele_sel, ele_seed, max_ele_type };
  TH1D* h_eletracks_pt[max_ele_type];
  TH1D* h_eletracks_eta[max_ele_type];
  TH1D* h_eletracks_phi[max_ele_type];
  TH1D* h_eletracks_dxy[max_ele_type];
  //TH1D* h_eletracks_absdxy[max_ele_type];
  TH1D* h_eletracks_dsz[max_ele_type];
  TH1D* h_eletracks_dz[max_ele_type];
  TH1D* h_eletracks_absnsigmadxy[max_ele_type];
  TH1D* h_eletracks_nsigmadxy[max_ele_type];
  TH1D* h_eletracks_nsigmadsz[max_ele_type];
  TH1D* h_eletracks_dxyerr[max_ele_type];
  //TH1D* h_eletracks_dxyerr_pt[max_ele_type][max_ptslice];
  TH1D* h_eletracks_dxydszcov[max_ele_type];
  TH1D* h_eletracks_absdxydszcov[max_ele_type];
  TH1D* h_eletracks_dzerr[max_ele_type];
  TH1D* h_eletracks_dszerr[max_ele_type];
  TH1D* h_eletracks_lambdaerr[max_ele_type];
  TH1D* h_eletracks_pterr[max_ele_type];
  TH1D* h_eletracks_phierr[max_ele_type];
  TH1D* h_eletracks_etaerr[max_ele_type];
  TH2D* h_eletracks_dxyerr_v_pt[max_ele_type];
  TH2D* h_eletracks_dxyerr_v_minr[max_ele_type];
  TH2D* h_eletracks_dxyerr_v_eta[max_ele_type];
  TH2D* h_eletracks_dxyerr_v_phi[max_ele_type];
  TH2D* h_eletracks_dszerr_v_pt[max_ele_type];
  TH2D* h_eletracks_dszerr_v_eta[max_ele_type];
  TH2D* h_eletracks_dszerr_v_phi[max_ele_type];

  TH2D* h_eletracks_dxydszcov_v_pt[max_ele_type];
  TH2D* h_eletracks_dxydszcov_v_eta[max_ele_type];
  TH2D* h_eletracks_dxydszcov_v_phi[max_ele_type];
  TH2D* h_eletracks_absdxydszcov_v_pt[max_ele_type];
  TH2D* h_eletracks_absdxydszcov_v_eta[max_ele_type];
  TH2D* h_eletracks_absdxydszcov_v_phi[max_ele_type];
  TH2D* h_eletracks_eta_v_phi[max_ele_type];


  enum { mu_all, mu_sel, mu_seed, max_mu_type };
  TH1D* h_mutracks_pt[max_mu_type];
  TH1D* h_mutracks_eta[max_mu_type];
  TH1D* h_mutracks_phi[max_mu_type];
  TH1D* h_mutracks_dxy[max_mu_type];
  //TH1D* h_mutracks_absdxy[max_mu_type];
  TH1D* h_mutracks_dsz[max_mu_type];
  TH1D* h_mutracks_dz[max_mu_type];
  TH1D* h_mutracks_absnsigmadxy[max_mu_type];
  TH1D* h_mutracks_nsigmadxy[max_mu_type];
  TH1D* h_mutracks_nsigmadsz[max_mu_type];
  TH1D* h_mutracks_dxyerr[max_mu_type];
  //TH1D* h_mutracks_dxyerr_pt[max_mu_type][max_ptslice];
  TH1D* h_mutracks_dxydszcov[max_mu_type];
  TH1D* h_mutracks_absdxydszcov[max_mu_type];
  TH1D* h_mutracks_dzerr[max_mu_type];
  TH1D* h_mutracks_dszerr[max_mu_type];
  TH1D* h_mutracks_lambdaerr[max_mu_type];
  TH1D* h_mutracks_pterr[max_mu_type];
  TH1D* h_mutracks_phierr[max_mu_type];
  TH1D* h_mutracks_etaerr[max_mu_type];
  TH2D* h_mutracks_dxyerr_v_pt[max_mu_type];
  TH2D* h_mutracks_dxyerr_v_minr[max_mu_type];
  TH2D* h_mutracks_dxyerr_v_eta[max_mu_type];
  TH2D* h_mutracks_dxyerr_v_phi[max_mu_type];
  TH2D* h_mutracks_dszerr_v_pt[max_mu_type];
  TH2D* h_mutracks_dszerr_v_eta[max_mu_type];
  TH2D* h_mutracks_dszerr_v_phi[max_mu_type];

  TH2D* h_mutracks_dxydszcov_v_pt[max_mu_type];
  TH2D* h_mutracks_dxydszcov_v_eta[max_mu_type];
  TH2D* h_mutracks_dxydszcov_v_phi[max_mu_type];
  TH2D* h_mutracks_absdxydszcov_v_pt[max_mu_type];
  TH2D* h_mutracks_absdxydszcov_v_eta[max_mu_type];
  TH2D* h_mutracks_absdxydszcov_v_phi[max_mu_type];
  TH2D* h_mutracks_eta_v_phi[max_mu_type];


  //the no lep corresponds to no GOOD lepton with pt > 20
  // new : these now by default do not have leptons with pt ≥ 20 GeV
  enum { tk_all, tk_sel, tk_seed, max_tk_type };
  TH1D* h_ntracks[max_tk_type];
  TH1D* h_tracks_pt[max_tk_type];
  TH1D* h_tracks_eta[max_tk_type];
  TH1D* h_tracks_phi[max_tk_type];
  TH1D* h_tracks_dxy[max_tk_type];
  //TH1D* h_tracks_absdxy[max_tk_type];
  TH1D* h_tracks_dsz[max_tk_type];
  TH1D* h_tracks_dz[max_tk_type];
  // TH1D* h_tracks_dzpv[max_tk_type];
  // TH1D* h_tracks_nhits[max_tk_type];
  // TH1D* h_tracks_npxhits[max_tk_type];
  // TH1D* h_tracks_nsthits[max_tk_type];
  // TH1D* h_tracks_min_r[max_tk_type];
  // TH1D* h_tracks_npxlayers[max_tk_type];
  // TH1D* h_tracks_nstlayers[max_tk_type];
  TH1D* h_tracks_absnsigmadxy[max_tk_type];
  TH1D* h_tracks_nsigmadxy[max_tk_type];
  TH1D* h_tracks_nsigmadsz[max_tk_type];

  TH1D* h_tracks_dxyerr[max_tk_type];
  //TH1D* h_tracks_dxyerr_pt[max_tk_type][max_ptslice];
  TH1D* h_tracks_dxydszcov[max_tk_type];
  TH1D* h_tracks_absdxydszcov[max_tk_type];
  TH1D* h_tracks_dzerr[max_tk_type];
  TH1D* h_tracks_dszerr[max_tk_type];
  TH1D* h_tracks_lambdaerr[max_tk_type];
  TH1D* h_tracks_pterr[max_tk_type];
  TH1D* h_tracks_phierr[max_tk_type];
  TH1D* h_tracks_etaerr[max_tk_type];

  // TH2D* h_tracks_nstlayers_v_eta[max_tk_type];
  // TH2D* h_tracks_dxy_v_eta[max_tk_type];
  // TH2D* h_tracks_dxy_v_phi[max_tk_type];
  // TH2D* h_tracks_dxy_v_nstlayers[max_tk_type];
  // TH2D* h_tracks_nstlayers_v_phi[max_tk_type];
  // TH2D* h_tracks_npxlayers_v_phi[max_tk_type];
  // TH2D* h_tracks_nhits_v_phi[max_tk_type];
  // TH2D* h_tracks_npxhits_v_phi[max_tk_type];
  // TH2D* h_tracks_nsthits_v_phi[max_tk_type];

  // TH2D* h_tracks_nsigmadxy_v_eta[max_tk_type];
  // TH2D* h_tracks_nsigmadxy_v_nstlayers[max_tk_type];
  // TH2D* h_tracks_nsigmadxy_v_dxy[max_tk_type];
  // TH2D* h_tracks_nsigmadxy_v_dxyerr[max_tk_type];

  TH2D* h_tracks_dxyerr_v_pt[max_tk_type];
  TH2D* h_tracks_dxyerr_v_eta[max_tk_type];
  TH2D* h_tracks_dxyerr_v_phi[max_tk_type];
  TH2D* h_tracks_dxyerr_v_minr[max_tk_type];
  // TH2D* h_tracks_dxyerr_v_dxy[max_tk_type];
  // TH2D* h_tracks_dxyerr_v_dzpv[max_tk_type];
  // TH2D* h_tracks_dxyerr_v_npxlayers[max_tk_type];
  // TH2D* h_tracks_dxyerr_v_nstlayers[max_tk_type];

  TH2D* h_tracks_dszerr_v_pt[max_tk_type];
  TH2D* h_tracks_dszerr_v_eta[max_tk_type];
  TH2D* h_tracks_dszerr_v_phi[max_tk_type];
  // TH2D* h_tracks_dszerr_v_dxy[max_tk_type];
  // TH2D* h_tracks_dszerr_v_dz[max_tk_type];
  // TH2D* h_tracks_dszerr_v_npxlayers[max_tk_type];
  // TH2D* h_tracks_dszerr_v_nstlayers[max_tk_type];

  TH2D* h_tracks_dxydszcov_v_pt[max_tk_type];
  TH2D* h_tracks_dxydszcov_v_eta[max_tk_type];
  TH2D* h_tracks_dxydszcov_v_phi[max_tk_type];
  TH2D* h_tracks_absdxydszcov_v_pt[max_tk_type];
  TH2D* h_tracks_absdxydszcov_v_eta[max_tk_type];
  TH2D* h_tracks_absdxydszcov_v_phi[max_tk_type];
  // TH2D* h_tracks_lambdaerr_v_pt[max_tk_type];
  // TH2D* h_tracks_lambdaerr_v_eta[max_tk_type];
  // TH2D* h_tracks_lambdaerr_v_phi[max_tk_type];
  // TH2D* h_tracks_lambdaerr_v_dxy[max_tk_type];
  // TH2D* h_tracks_lambdaerr_v_dz[max_tk_type];
  // TH2D* h_tracks_lambdaerr_v_npxlayers[max_tk_type];
  // TH2D* h_tracks_lambdaerr_v_nstlayers[max_tk_type];

  TH2D* h_tracks_eta_v_phi[max_tk_type];
  
  const char* ex[max_tk_type] = {"all", "sel", "seed"};
  for (int i = 0; i < max_tk_type; ++i) {
    h_ntracks[i] = new TH1D(TString::Format("h_%s_ntracks", ex[i]), TString::Format(";number of %s tracks;events", ex[i]), 2000, 0, 2000);
    h_tracks_pt[i] = new TH1D(TString::Format("h_%s_tracks_pt", ex[i]), TString::Format("%s tracks;tracks pt (GeV);arb. units", ex[i]), 2000, 0, 200);
    h_tracks_eta[i] = new TH1D(TString::Format("h_%s_tracks_eta", ex[i]), TString::Format("%s tracks;tracks eta;arb. units", ex[i]), 50, -4, 4);
    h_tracks_phi[i] = new TH1D(TString::Format("h_%s_tracks_phi", ex[i]), TString::Format("%s tracks;tracks phi;arb. units", ex[i]), 315, -3.15, 3.15);
    h_tracks_dxy[i] = new TH1D(TString::Format("h_%s_tracks_dxy", ex[i]), TString::Format("%s tracks;tracks dxy to beamspot (cm);arb. units", ex[i]), 400, -0.2, 0.2);
    //h_tracks_absdxy[i] = new TH1D(TString::Format("h_%s_tracks_absdxy", ex[i]), TString::Format("%s tracks;tracks |dxy| to beamspot (cm);arb. units", ex[i]), 200, 0, 0.2);
    h_tracks_dsz[i] = new TH1D(TString::Format("h_%s_tracks_dsz", ex[i]), TString::Format("%s tracks;tracks dsz (cm);arb. units", ex[i]), 400, -20, 20);
    h_tracks_dz[i] = new TH1D(TString::Format("h_%s_tracks_dz", ex[i]), TString::Format("%s tracks;tracks dz (cm);arb. units", ex[i]), 400, -20, 20);
    // h_tracks_dzpv[i] = new TH1D(TString::Format("h_%s_tracks_dzpv", ex[i]), TString::Format("%s tracks;tracks dz to PV (cm);arb. units", ex[i]), 400, -20, 20);
    // h_tracks_nhits[i] = new TH1D(TString::Format("h_%s_tracks_nhits", ex[i]), TString::Format("%s tracks;tracks nhits;arb. units", ex[i]), 40, 0, 40);
    // h_tracks_npxhits[i] = new TH1D(TString::Format("h_%s_tracks_npxhits", ex[i]), TString::Format("%s tracks;tracks npxhits;arb. units", ex[i]), 40, 0, 40);
    // h_tracks_nsthits[i] = new TH1D(TString::Format("h_%s_tracks_nsthits", ex[i]), TString::Format("%s tracks;tracks nsthits;arb. units", ex[i]), 40, 0, 40);

    // h_tracks_min_r[i] = new TH1D(TString::Format("h_%s_tracks_min_r", ex[i]), TString::Format("%s tracks;tracks min_r;arb. units", ex[i]), 20, 0, 20);
    // h_tracks_npxlayers[i] = new TH1D(TString::Format("h_%s_tracks_npxlayers", ex[i]), TString::Format("%s tracks;tracks npxlayers;arb. units", ex[i]), 20, 0, 20);
    // h_tracks_nstlayers[i] = new TH1D(TString::Format("h_%s_tracks_nstlayers", ex[i]), TString::Format("%s tracks;tracks nstlayers;arb. units", ex[i]), 20, 0, 20);
    h_tracks_absnsigmadxy[i] = new TH1D(TString::Format("h_%s_tracks_absnsigmadxy", ex[i]), TString::Format("%s tracks;tracks abs nsigmadxy;arb. units", ex[i]), 400, 0, 40);
    h_tracks_nsigmadxy[i] = new TH1D(TString::Format("h_%s_tracks_nsigmadxy", ex[i]), TString::Format("%s tracks;tracks nsigmadxy;arb. units", ex[i]), 2000, -20, 20);
    h_tracks_nsigmadsz[i] = new TH1D(TString::Format("h_%s_tracks_nsigmadsz", ex[i]), TString::Format("%s tracks;tracks nsigmadsz;arb. units", ex[i]), 2000, -20, 20);
    
    h_tracks_dxyerr[i] = new TH1D(TString::Format("h_%s_tracks_dxyerr", ex[i]), TString::Format("%s tracks;tracks dxyerr;arb. units", ex[i]), 2000, 0, 0.2);
    h_tracks_dxydszcov[i] = new TH1D(TString::Format("h_%s_tracks_dxydszcov", ex[i]), TString::Format("%s tracks;tracks dxy-dsz covariance;arb. units", ex[i]), 2000, -0.00002, 0.00002);
    h_tracks_absdxydszcov[i] = new TH1D(TString::Format("h_%s_tracks_absdxydszcov", ex[i]), TString::Format("%s tracks;tracks dxy-dsz covariance;arb. units", ex[i]), 2000, 0, 0.00002);
    h_tracks_dzerr[i] = new TH1D(TString::Format("h_%s_tracks_dzerr", ex[i]), TString::Format("%s tracks;tracks dzerr;arb. units", ex[i]), 2000, 0, 0.2);
    h_tracks_dszerr[i] = new TH1D(TString::Format("h_%s_tracks_dszerr", ex[i]), TString::Format("%s tracks;tracks dszerr;arb. units", ex[i]), 2000, 0, 0.2);
    h_tracks_lambdaerr[i] = new TH1D(TString::Format("h_%s_tracks_lambdaerr", ex[i]), TString::Format("%s tracks;tracks lambdaerr;arb. units", ex[i]), 2000, 0, 0.2);
    h_tracks_pterr[i] = new TH1D(TString::Format("h_%s_tracks_pterr", ex[i]), TString::Format("%s tracks;tracks pterr;arb. units", ex[i]), 200, 0, 0.2);
    h_tracks_phierr[i] = new TH1D(TString::Format("h_%s_tracks_phierr", ex[i]), TString::Format("%s tracks;tracks phierr;arb. units", ex[i]), 200, 0, 0.2);
    h_tracks_etaerr[i] = new TH1D(TString::Format("h_%s_tracks_etaerr", ex[i]), TString::Format("%s tracks;tracks etaerr;arb. units", ex[i]), 200, 0, 0.2);

    // h_tracks_nstlayers_v_eta[i] = new TH2D(TString::Format("h_%s_tracks_nstlayers_v_eta", ex[i]), TString::Format("%s tracks;tracks eta;tracks nstlayers", ex[i]), 80, -4, 4, 20, 0, 20);
    // h_tracks_dxy_v_eta[i] = new TH2D(TString::Format("h_%s_tracks_dxy_v_eta", ex[i]), TString::Format("%s tracks;tracks eta;tracks dxy to beamspot", ex[i]), 80, -4, 4, 400, -0.2, 0.2);
    // h_tracks_dxy_v_nstlayers[i] = new TH2D(TString::Format("h_%s_tracks_dxy_v_nstlayers", ex[i]), TString::Format("%s tracks;tracks nstlayers;tracks dxy to beamspot", ex[i]), 20, 0, 20, 400, -0.2, 0.2);
    // h_tracks_nsigmadxy_v_eta[i] = new TH2D(TString::Format("h_%s_tracks_nsigmadxy_v_eta", ex[i]), TString::Format("%s tracks;tracks eta;tracks nsigmadxy", ex[i]), 80, -4, 4, 200, 0, 20);
    // h_tracks_nsigmadxy_v_nstlayers[i] = new TH2D(TString::Format("h_%s_tracks_nsigmadxy_v_nstlayers", ex[i]), TString::Format("%s tracks;tracks nstlayers;tracks nsigmadxy", ex[i]), 20, 0, 20, 200, 0, 20);
    // h_tracks_nsigmadxy_v_dxy[i] = new TH2D(TString::Format("h_%s_tracks_nsigmadxy_v_dxy", ex[i]), TString::Format("%s tracks;tracks dxy to beamspot;tracks nsigmadxy", ex[i]), 400, -0.2, 0.2, 200, 0, 20);
    // h_tracks_nsigmadxy_v_dxyerr[i] = new TH2D(TString::Format("h_%s_tracks_nsigmadxy_v_dxyerr", ex[i]), TString::Format("%s tracks;tracks dxyerr;tracks nsigmadxy", ex[i]), 200, 0, 0.2, 200, 0, 20);
    // h_tracks_dxy_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_dxy_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks dxy to beamspot", ex[i]), 315, -3.15, 3.15, 400, -0.2, 0.2);
    // h_tracks_nstlayers_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_nstlayers_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks nstlayers", ex[i]), 315, -3.15, 3.15, 20, 0, 20);
    // h_tracks_npxlayers_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_npxlayers_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks npxlayers", ex[i]), 315, -3.15, 3.15, 10, 0, 10);
    // h_tracks_nhits_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_nhits_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks nhits", ex[i]), 315, -3.15, 3.15, 40, 0, 40);
    // h_tracks_npxhits_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_npxhits_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks npxhits", ex[i]), 315, -3.15, 3.15, 40, 0, 40);
    // h_tracks_nsthits_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_nsthits_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks nsthits", ex[i]), 315, -3.15, 3.15, 40, 0, 40);

    h_tracks_dxyerr_v_pt[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_pt", ex[i]), TString::Format("%s tracks;tracks pt;tracks dxyerr", ex[i]), 2000, 0, 200, 2000, 0, 0.2);
    h_tracks_dxyerr_v_eta[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_eta", ex[i]), TString::Format("%s tracks;tracks eta;tracks dxyerr", ex[i]), 80, -4, 4, 2000, 0, 0.2);
    h_tracks_dxyerr_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks dxyerr", ex[i]), 126, -3.15, 3.15, 200, 0, 0.2);
    h_tracks_dxyerr_v_minr[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_minr", ex[i]), TString::Format("%s tracks;tracks minr;tracks dxyerrr", ex[i]), 10, 0, 10, 200, 0, 0.2);
    // h_tracks_dxyerr_v_dxy[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_dxy", ex[i]), TString::Format("%s tracks;tracks dxy to beamspot;tracks dxyerr", ex[i]), 400, -0.2, 0.2, 200, 0, 0.2);
    // h_tracks_dxyerr_v_dzpv[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_dzpv", ex[i]), TString::Format("%s tracks;tracks dz to PV;tracks dxyerr", ex[i]), 400, -20, 20, 200, 0, 0.2);
    // h_tracks_dxyerr_v_npxlayers[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_npxlayers", ex[i]), TString::Format("%s tracks;tracks npxlayers;tracks dxyerr", ex[i]), 10, 0, 10, 200, 0, 0.2);
    // h_tracks_dxyerr_v_nstlayers[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_nstlayers", ex[i]), TString::Format("%s tracks;tracks nstlayers;tracks dxyerr", ex[i]), 20, 0, 20, 200, 0, 0.2);

    h_tracks_dszerr_v_pt[i] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_pt", ex[i]), TString::Format("%s tracks;tracks pt;tracks dszerr", ex[i]), 2000, 0, 200, 2000, 0, 0.2);
    h_tracks_dszerr_v_eta[i] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_eta", ex[i]), TString::Format("%s tracks;tracks eta;tracks dszerr", ex[i]), 80, -4, 4, 2000, 0, 0.2);
    h_tracks_dszerr_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks dszerr", ex[i]), 126, -3.15, 3.15, 200, 0, 0.2);
    // h_tracks_dszerr_v_dxy[i] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_dxy", ex[i]), TString::Format("%s tracks;tracks dxy to beamspot;tracks dszerr", ex[i]), 400, -0.2, 0.2, 200, 0, 0.2);
    // h_tracks_dszerr_v_dz[i] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_dz", ex[i]), TString::Format("%s tracks;tracks dz to beamspot;tracks dszerr", ex[i]), 400, -20, 20, 200, 0, 0.2);
    // h_tracks_dszerr_v_npxlayers[i] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_npxlayers", ex[i]), TString::Format("%s tracks;tracks npxlayers;tracks dszerr", ex[i]), 10, 0, 10, 200, 0, 0.2);
    // h_tracks_dszerr_v_nstlayers[i] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_nstlayers", ex[i]), TString::Format("%s tracks;tracks nstlayers;tracks dszerr", ex[i]), 20, 0, 20, 200, 0, 0.2);

    h_tracks_dxydszcov_v_pt[i] = new TH2D(TString::Format("h_%s_tracks_dxydszcov_v_pt", ex[i]), TString::Format("%s tracks;tracks pt;tracks dxydszcov", ex[i]), 2000, 0, 200, 2000, -0.00002, 0.00002);
    h_tracks_dxydszcov_v_eta[i] = new TH2D(TString::Format("h_%s_tracks_dxydszcov_v_eta", ex[i]), TString::Format("%s tracks;tracks eta;tracks dxydszcov", ex[i]), 80, -4, 4, 2000, -0.00002, 0.00002);
    h_tracks_dxydszcov_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_dxydszcov_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks dxydszcov", ex[i]), 126, -3.15, 3.15, 200, -0.00002, 0.00002);
    h_tracks_absdxydszcov_v_pt[i] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_pt", ex[i]), TString::Format("%s tracks;tracks pt;tracks dxydszcov", ex[i]), 2000, 0, 200, 2000, 0, 0.00002);
    h_tracks_absdxydszcov_v_eta[i] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_eta", ex[i]), TString::Format("%s tracks;tracks eta;tracks dxydszcov", ex[i]), 80, -4, 4, 2000, 0, 0.00002);
    h_tracks_absdxydszcov_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks dxydszcov", ex[i]), 126, -3.15, 3.15, 2000, 0, 0.00002);

    // h_tracks_lambdaerr_v_pt[i] = new TH2D(TString::Format("h_%s_tracks_lambdaerr_v_pt", ex[i]), TString::Format("%s tracks;tracks pt;tracks lambdaerr", ex[i]), 2000, 0, 200, 2000, 0, 0.2);
    // h_tracks_lambdaerr_v_eta[i] = new TH2D(TString::Format("h_%s_tracks_lambdaerr_v_eta", ex[i]), TString::Format("%s tracks;tracks eta;tracks lambdaerr", ex[i]), 80, -4, 4, 2000, 0, 0.2);
    // h_tracks_lambdaerr_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_lambdaerr_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks lambdaerr", ex[i]), 126, -3.15, 3.15, 200, 0, 0.2);
    // h_tracks_lambdaerr_v_dxy[i] = new TH2D(TString::Format("h_%s_tracks_lambdaerr_v_dxy", ex[i]), TString::Format("%s tracks;tracks dxy to beamspot;tracks lambdaerr", ex[i]), 400, -0.2, 0.2, 200, 0, 0.2);
    // h_tracks_lambdaerr_v_dz[i] = new TH2D(TString::Format("h_%s_tracks_lambdaerr_v_dz", ex[i]), TString::Format("%s tracks;tracks dz to beamspot;tracks lambdaerr", ex[i]), 400, -20, 20, 200, 0, 0.2);
    // h_tracks_lambdaerr_v_npxlayers[i] = new TH2D(TString::Format("h_%s_tracks_lambdaerr_v_npxlayers", ex[i]), TString::Format("%s tracks;tracks npxlayers;tracks lambdaerr", ex[i]), 10, 0, 10, 200, 0, 0.2);
    // h_tracks_lambdaerr_v_nstlayers[i] = new TH2D(TString::Format("h_%s_tracks_lambdaerr_v_nstlayers", ex[i]), TString::Format("%s tracks;tracks nstlayers;tracks lambdaerr", ex[i]), 20, 0, 20, 200, 0, 0.2);

    h_tracks_eta_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_eta_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks eta", ex[i]), 126, -3.15, 3.15, 80, -4, 4);
  }

  //the pass mu and pass el is pt >= 20 
  const char* eleex[max_ele_type] = {"all_ele", "sel_ele", "seed_ele"};
  for (int j = 0; j < max_ele_type; ++j) {
    h_eletracks_pt[j] = new TH1D(TString::Format("h_%s_tracks_pt", eleex[j]), TString::Format("%s tracks;tracks pt (GeV);arb. units", eleex[j]), 2000, 0, 200);
    h_eletracks_eta[j] = new TH1D(TString::Format("h_%s_tracks_eta", eleex[j]), TString::Format("%s tracks;tracks eta;arb. units", eleex[j]), 50, -4, 4);
    h_eletracks_phi[j] = new TH1D(TString::Format("h_%s_tracks_phi", eleex[j]), TString::Format("%s tracks;tracks phi;arb. units", eleex[j]), 315, -3.15, 3.15);
    h_eletracks_dxy[j] = new TH1D(TString::Format("h_%s_tracks_dxy", eleex[j]), TString::Format("%s tracks;tracks dxy to beamspot (cm);arb. units", eleex[j]), 400, -0.2, 0.2);
    //h_eletracks_absdxy[j] = new TH1D(TString::Format("h_%s_tracks_absdxy", eleex[j]), TString::Format("%s tracks;tracks |dxy| to beamspot (cm);arb. units", eleex[j]), 200, 0, 0.2);
    h_eletracks_dsz[j] = new TH1D(TString::Format("h_%s_tracks_dsz", eleex[j]), TString::Format("%s tracks;tracks dsz (cm);arb. units", eleex[j]), 400, -20, 20);
    h_eletracks_dz[j] = new TH1D(TString::Format("h_%s_tracks_dz", eleex[j]), TString::Format("%s tracks;tracks dz (cm);arb. units", eleex[j]), 400, -20, 20);
    h_eletracks_absnsigmadxy[j] = new TH1D(TString::Format("h_%s_tracks_absnsigmadxy", eleex[j]), TString::Format("%s tracks;tracks abs nsigmadxy;arb. units", eleex[j]), 400, 0, 40);
    h_eletracks_nsigmadxy[j] = new TH1D(TString::Format("h_%s_tracks_nsigmadxy", eleex[j]), TString::Format("%s tracks;tracks nsigmadxy;arb. units", eleex[j]), 2000, -20, 20);
    h_eletracks_nsigmadsz[j] = new TH1D(TString::Format("h_%s_tracks_nsigmadsz", eleex[j]), TString::Format("%s tracks;tracks nsigmadsz;arb. units", eleex[j]), 2000, -20, 20);
    h_eletracks_dxyerr[j] = new TH1D(TString::Format("h_%s_tracks_dxyerr", eleex[j]), TString::Format("%s tracks;tracks dxyerr;arb. units", eleex[j]), 2000, 0, 0.2);
    h_eletracks_dxydszcov[j] = new TH1D(TString::Format("h_%s_tracks_dxydszcov", eleex[j]), TString::Format("%s tracks;tracks dxy-dsz covariance;arb. units", eleex[j]), 2000, -0.00002, 0.00002);
    h_eletracks_absdxydszcov[j] = new TH1D(TString::Format("h_%s_tracks_absdxydszcov", eleex[j]), TString::Format("%s tracks;tracks dxy-dsz covariance;arb. units", eleex[j]), 2000, 0, 0.00002);
    h_eletracks_dzerr[j] = new TH1D(TString::Format("h_%s_tracks_dzerr", eleex[j]), TString::Format("%s tracks;tracks dzerr;arb. units", eleex[j]), 2000, 0, 0.2);
    h_eletracks_dszerr[j] = new TH1D(TString::Format("h_%s_tracks_dszerr", eleex[j]), TString::Format("%s tracks;tracks dszerr;arb. units", eleex[j]), 2000, 0, 0.2);
    h_eletracks_lambdaerr[j] = new TH1D(TString::Format("h_%s_tracks_lambdaerr", eleex[j]), TString::Format("%s tracks;tracks lambdaerr;arb. units", eleex[j]), 2000, 0, 0.2);
    h_eletracks_pterr[j] = new TH1D(TString::Format("h_%s_tracks_pterr", eleex[j]), TString::Format("%s tracks;tracks pterr;arb. units", eleex[j]), 200, 0, 0.2);
    h_eletracks_phierr[j] = new TH1D(TString::Format("h_%s_tracks_phierr", eleex[j]), TString::Format("%s tracks;tracks phierr;arb. units", eleex[j]), 200, 0, 0.2);
    h_eletracks_etaerr[j] = new TH1D(TString::Format("h_%s_tracks_etaerr", eleex[j]), TString::Format("%s tracks;tracks etaerr;arb. units", eleex[j]), 200, 0, 0.2);
    h_eletracks_dxyerr_v_pt[j] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_pt", eleex[j]), TString::Format("%s tracks;tracks pt;tracks dxyerr", eleex[j]), 2000, 0, 400, 2000, 0, 0.2);
    h_eletracks_dxyerr_v_eta[j] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_eta", eleex[j]), TString::Format("%s tracks;tracks eta;tracks dxyerr", eleex[j]), 80, -4, 4, 2000, 0, 0.2);
    h_eletracks_dxyerr_v_phi[j] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_phi", eleex[j]), TString::Format("%s tracks;tracks phi;tracks dxyerr", eleex[j]), 126, -3.15, 3.15, 200, 0, 0.2);
    h_eletracks_dxyerr_v_minr[j] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_minr", eleex[j]), TString::Format("%s tracks;tracks minr;tracks dxyerrr", eleex[j]), 10, 0, 10, 200, 0, 0.2);
    h_eletracks_dszerr_v_pt[j] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_pt", eleex[j]), TString::Format("%s tracks;tracks pt;tracks dszerr", eleex[j]), 2000, 0, 400, 2000, 0, 0.2);
    h_eletracks_dszerr_v_eta[j] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_eta", eleex[j]), TString::Format("%s tracks;tracks eta;tracks dszerr", eleex[j]), 80, -4, 4, 2000, 0, 0.2);
    h_eletracks_dszerr_v_phi[j] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_phi", eleex[j]), TString::Format("%s tracks;tracks phi;tracks dszerr", eleex[j]), 126, -3.15, 3.15, 200, 0, 0.2);
    
    h_eletracks_dxydszcov_v_pt[j] = new TH2D(TString::Format("h_%s_tracks_dxydszcov_v_pt", eleex[j]), TString::Format("%s tracks;tracks pt;tracks dxydszcov", eleex[j]), 2000, 0, 200, 2000, -0.00002, 0.00002);
    h_eletracks_dxydszcov_v_eta[j] = new TH2D(TString::Format("h_%s_tracks_dxydszcov_v_eta", eleex[j]), TString::Format("%s tracks;tracks eta;tracks dxydszcov", eleex[j]), 80, -4, 4, 2000, -0.00002, 0.00002);
    h_eletracks_dxydszcov_v_phi[j] = new TH2D(TString::Format("h_%s_tracks_dxydszcov_v_phi", eleex[j]), TString::Format("%s tracks;tracks phi;tracks dxydszcov", eleex[j]), 126, -3.15, 3.15, 200, -0.00002, 0.00002);
    h_eletracks_absdxydszcov_v_pt[j] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_pt", eleex[j]), TString::Format("%s tracks;tracks pt;tracks dxydszcov", eleex[j]), 2000, 0, 200, 2000, 0, 0.00002);
    h_eletracks_absdxydszcov_v_eta[j] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_eta", eleex[j]), TString::Format("%s tracks;tracks eta;tracks dxydszcov", eleex[j]), 80, -4, 4, 2000, 0, 0.00002);
    h_eletracks_absdxydszcov_v_phi[j] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_phi", eleex[j]), TString::Format("%s tracks;tracks phi;tracks dxydszcov", eleex[j]), 126, -3.15, 3.15, 2000, 0, 0.00002);
    h_eletracks_eta_v_phi[j] = new TH2D(TString::Format("h_%s_tracks_eta_v_phi", eleex[j]), TString::Format("%s tracks;tracks phi;tracks eta", eleex[j]), 126, -3.15, 3.15, 80, -4, 4);

  }

  const char* muex[max_mu_type] = {"all_mu", "sel_mu", "seed_mu"};
  for (int j = 0; j < max_mu_type; ++j) {
    h_mutracks_pt[j] = new TH1D(TString::Format("h_%s_tracks_pt", muex[j]), TString::Format("%s tracks;tracks pt (GeV);arb. units", muex[j]), 2000, 0, 200);
    h_mutracks_eta[j] = new TH1D(TString::Format("h_%s_tracks_eta", muex[j]), TString::Format("%s tracks;tracks eta;arb. units", muex[j]), 50, -4, 4);
    h_mutracks_phi[j] = new TH1D(TString::Format("h_%s_tracks_phi", muex[j]), TString::Format("%s tracks;tracks phi;arb. units", muex[j]), 315, -3.15, 3.15);
    h_mutracks_dxy[j] = new TH1D(TString::Format("h_%s_tracks_dxy", muex[j]), TString::Format("%s tracks;tracks dxy to beamspot (cm);arb. units", muex[j]), 400, -0.2, 0.2);
   // h_mutracks_absdxy[j] = new TH1D(TString::Format("h_%s_tracks_absdxy", muex[j]), TString::Format("%s tracks;tracks |dxy| to beamspot (cm);arb. units", muex[j]), 200, 0, 0.2);
    h_mutracks_dsz[j] = new TH1D(TString::Format("h_%s_tracks_dsz", muex[j]), TString::Format("%s tracks;tracks dsz (cm);arb. units", muex[j]), 400, -20, 20);
    h_mutracks_dz[j] = new TH1D(TString::Format("h_%s_tracks_dz", muex[j]), TString::Format("%s tracks;tracks dz (cm);arb. units", muex[j]), 400, -20, 20);
    h_mutracks_absnsigmadxy[j] = new TH1D(TString::Format("h_%s_tracks_absnsigmadxy", muex[j]), TString::Format("%s tracks;tracks abs nsigmadxy;arb. units", muex[j]), 400, 0, 40);
    h_mutracks_nsigmadxy[j] = new TH1D(TString::Format("h_%s_tracks_nsigmadxy", muex[j]), TString::Format("%s tracks;tracks nsigmadxy;arb. units", muex[j]), 2000, -20, 20);
    h_mutracks_nsigmadsz[j] = new TH1D(TString::Format("h_%s_tracks_nsigmadsz", muex[j]), TString::Format("%s tracks;tracks nsigmadsz;arb. units", muex[j]), 2000, -20, 20);
    h_mutracks_dxyerr[j] = new TH1D(TString::Format("h_%s_tracks_dxyerr", muex[j]), TString::Format("%s tracks;tracks dxyerr;arb. units", muex[j]), 2000, 0, 0.2);
    h_mutracks_dxydszcov[j] = new TH1D(TString::Format("h_%s_tracks_dxydszcov", muex[j]), TString::Format("%s tracks;tracks dxy-dsz covariance;arb. units", muex[j]), 2000, -0.00002, 0.00002);
    h_mutracks_absdxydszcov[j] = new TH1D(TString::Format("h_%s_tracks_absdxydszcov", muex[j]), TString::Format("%s tracks;tracks dxy-dsz covariance;arb. units", muex[j]), 2000, 0, 0.00002);
    h_mutracks_dzerr[j] = new TH1D(TString::Format("h_%s_tracks_dzerr", muex[j]), TString::Format("%s tracks;tracks dzerr;arb. units", muex[j]), 2000, 0, 0.2);
    h_mutracks_dszerr[j] = new TH1D(TString::Format("h_%s_tracks_dszerr", muex[j]), TString::Format("%s tracks;tracks dszerr;arb. units", muex[j]), 2000, 0, 0.2);
    h_mutracks_lambdaerr[j] = new TH1D(TString::Format("h_%s_tracks_lambdaerr", muex[j]), TString::Format("%s tracks;tracks lambdaerr;arb. units", muex[j]), 2000, 0, 0.2);
    h_mutracks_pterr[j] = new TH1D(TString::Format("h_%s_tracks_pterr", muex[j]), TString::Format("%s tracks;tracks pterr;arb. units", muex[j]), 200, 0, 0.2);
    h_mutracks_phierr[j] = new TH1D(TString::Format("h_%s_tracks_phierr", muex[j]), TString::Format("%s tracks;tracks phierr;arb. units", muex[j]), 200, 0, 0.2);
    h_mutracks_etaerr[j] = new TH1D(TString::Format("h_%s_tracks_etaerr", muex[j]), TString::Format("%s tracks;tracks etaerr;arb. units", muex[j]), 200, 0, 0.2);
    h_mutracks_dxyerr_v_pt[j] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_pt", muex[j]), TString::Format("%s tracks;tracks pt;tracks dxyerr", muex[j]), 2000, 0, 400, 2000, 0, 0.2);
    h_mutracks_dxyerr_v_eta[j] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_eta", muex[j]), TString::Format("%s tracks;tracks eta;tracks dxyerr", muex[j]), 80, -4, 4, 2000, 0, 0.2);
    h_mutracks_dxyerr_v_phi[j] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_phi", muex[j]), TString::Format("%s tracks;tracks phi;tracks dxyerr", muex[j]), 126, -3.15, 3.15, 200, 0, 0.2);
    h_mutracks_dxyerr_v_minr[j] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_minr", muex[j]), TString::Format("%s tracks;tracks minr;tracks dxyerrr", muex[j]), 10, 0, 10, 200, 0, 0.2);
    h_mutracks_dszerr_v_pt[j] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_pt", muex[j]), TString::Format("%s tracks;tracks pt;tracks dszerr", muex[j]), 2000, 0, 400, 2000, 0, 0.2);
    h_mutracks_dszerr_v_eta[j] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_eta", muex[j]), TString::Format("%s tracks;tracks eta;tracks dszerr", muex[j]), 80, -4, 4, 2000, 0, 0.2);
    h_mutracks_dszerr_v_phi[j] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_phi", muex[j]), TString::Format("%s tracks;tracks phi;tracks dszerr", muex[j]), 126, -3.15, 3.15, 200, 0, 0.2);
    
    h_mutracks_dxydszcov_v_pt[j] = new TH2D(TString::Format("h_%s_tracks_dxydszcov_v_pt", muex[j]), TString::Format("%s tracks;tracks pt;tracks dxydszcov", muex[j]), 2000, 0, 200, 2000, -0.00002, 0.00002);
    h_mutracks_dxydszcov_v_eta[j] = new TH2D(TString::Format("h_%s_tracks_dxydszcov_v_eta", muex[j]), TString::Format("%s tracks;tracks eta;tracks dxydszcov", muex[j]), 80, -4, 4, 2000, -0.00002, 0.00002);
    h_mutracks_dxydszcov_v_phi[j] = new TH2D(TString::Format("h_%s_tracks_dxydszcov_v_phi", muex[j]), TString::Format("%s tracks;tracks phi;tracks dxydszcov", muex[j]), 126, -3.15, 3.15, 200, -0.00002, 0.00002);
    h_mutracks_absdxydszcov_v_pt[j] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_pt", muex[j]), TString::Format("%s tracks;tracks pt;tracks dxydszcov", muex[j]), 2000, 0, 200, 2000, 0, 0.00002);
    h_mutracks_absdxydszcov_v_eta[j] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_eta", muex[j]), TString::Format("%s tracks;tracks eta;tracks dxydszcov", muex[j]), 80, -4, 4, 2000, 0, 0.00002);
    h_mutracks_absdxydszcov_v_phi[j] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_phi", muex[j]), TString::Format("%s tracks;tracks phi;tracks dxydszcov", muex[j]), 126, -3.15, 3.15, 2000, 0, 0.00002);
    h_mutracks_eta_v_phi[j] = new TH2D(TString::Format("h_%s_tracks_eta_v_phi", muex[j]), TString::Format("%s tracks;tracks phi;tracks eta", muex[j]), 126, -3.15, 3.15, 80, -4, 4);

  }



  auto fcn = [&]() {
    const double w = nr.weight();
    if (nt.pvs().n() == 0)
      return std::make_pair(true, w);

    h_npv->Fill(nt.pvs().n(), w);

    h_bsx->Fill(nt.bs().x(), w);
    h_bsy->Fill(nt.bs().y(), w);
    h_bsz->Fill(nt.bs().z(), w);
    h_bsdxdz->Fill(nt.bs().dxdz(), w);
    h_bsdydz->Fill(nt.bs().dydz(), w);
    h_bsy_v_bsx->Fill(nt.bs().x(), nt.bs().y(), w);

    h_pvbsx->Fill(nt.pvs().x(0) - nt.bs().x(nt.pvs().z(0)), w);
    h_pvbsy->Fill(nt.pvs().y(0) - nt.bs().y(nt.pvs().z(0)), w);
    h_pvbsz->Fill(nt.pvs().z(0) - nt.bs().z(),              w);

    h_pvy_v_pvx->Fill(nt.pvs().x(0), nt.pvs().y(0), w);

    int ntracks[max_tk_type] = {0};
    int neletracks[max_ele_type] = {0};
    int nmutracks[max_mu_type] = {0};

    //////////////////////////////////////////////
    ///                                        ///
    /// old way to work with electrons & muons ///
    ///                                        ///
    //////////////////////////////////////////////


    // for (int ie = 0, iee = nte.n(); ie < iee; ++ie) {
    //   const double pt = nte.pt(ie);
    //   const double dxybs = nte.dxybs(ie, nt.bs());
    //   const float dsz = (nte.vz(ie)) * pt / nte.p(ie) - ((nte.vx(ie)) * nte.px(ie) + (nte.vy(ie)) * nte.py(ie)) / pt * nte.pz(ie) / nte.p(ie);
    //   const float dz = nte.vz(ie) - (nte.vx(ie) * nte.px(ie) + nte.vy(ie) * nte.py(ie)) / pt * nte.pz(ie) / pt;
    //   const int min_r = nte.min_r(ie);
    //   const int npxlayers = nte.npxlayers(ie);
    //   const int nstlayers = nte.nstlayers(ie);
    //   //const double nsigmadxy = nte.nsigmadxybs(ie, nt.bs());

    //   const bool eef[5] = {
		// 	  pt >= 20,
    //   	nte.eta(ie) < 2.4,
    //   	nte.iso(ie) < 0.10,
    //   	nte.passveto(ie),
    //   	nte.isTight(ie)
    //   };
      
    //   const bool pass_ele = eef[0] && eef[1] && eef[2] && eef[3] && eef[4];
    //   //const bool pass_nm1ef = eef[1] && eef[2] && eef[3] && eef[4];
      
    //   const bool etagt1p5 = false;
    //   bool etarange =false;
    //   if (etagt1p5)
    //     etarange = fabs(nte.eta(ie)) > 1.5;
    //   else
    //     etarange = fabs(nte.eta(ie)) < 1.5;

    //   double rescaled_dxyerr_el = nte.err_dxy(ie);
    //   double rescaled_dszerr_el = nte.err_dsz(ie);
    //   double rescaled_dxydszcov_el = nte.cov_34(ie);

    //   const bool rescale_tracks = false;
    //   if (rescale_tracks) {
    //     double dxyerr_scale_el = 1.;
    //     double dszerr_scale_el = 1.;
	
    //     if (fabs(nte.eta(ie)) < 1.5) {
    //       const double x = pt;

	  //        //2017 B
	  //       //electron 
	  //       // const double e_dxy[2] = {1.2519894918062238, 0.00007487187197916488};
	  //       // const double e_dsz[2] = {1.1378345538232282, 0.000015006579023894503}; 

	  //       // dxyerr_scale_el = (x>=20&&x<=200)*(e_dxy[0]+e_dxy[1]*x);
	  //       // dszerr_scale_el = (x>=20&&x<=200)*(e_dsz[0]+e_dsz[1]*x);
          
    //       // //2017 C
    //       // //electron 
    //       // const double e_dxy[2] = {1.2813251299194244, 0.0000980634546644231};
    //       // const double e_dsz[2] = {1.2396626500193402, 0.0001031872972430143}; 

    //       // dxyerr_scale_el = (x>=20&&x<=200)*(e_dxy[0]+e_dxy[1]*x);
    //       // dszerr_scale_el = (x>=20&&x<=200)*(e_dsz[0]+e_dsz[1]*x);

    //       // //2017 D
    //       // //electron 
    //       // const double e_dxy[2] = {1.2175109728215536, 0.00015468622838992613};
    //       // const double e_dsz[2] = {1.193086410468232, 0.00009273527660223248}; 

    //       // dxyerr_scale_el = (x>=20&&x<=200)*(e_dxy[0]+e_dxy[1]*x);
    //       // dszerr_scale_el = (x>=20&&x<=200)*(e_dsz[0]+e_dsz[1]*x);
          
    //       // //2017 E
    //       // //electron 
    //       // const double e_dxy[2] = {1.1391061605726946, 0.000101181227594822};
    //       // const double e_dsz[2] = {1.0759837837776636, 0.00012897972750002158}; 

    //       // dxyerr_scale_el = (x>=20&&x<=200)*(e_dxy[0]+e_dxy[1]*x);
    //       // dszerr_scale_el = (x>=20&&x<=200)*(e_dsz[0]+e_dsz[1]*x);
         
    //       // //2017 F
    //       // //electron 
    //       const double e_dxy[2] = {1.2163661067927056, 0.0001401403672766123};
    //       const double e_dsz[2] = {1.1387132063959098, 0.00017118239591405043}; 

    //       dxyerr_scale_el = (x>=20&&x<=200)*(e_dxy[0]+e_dxy[1]*x);
    //       dszerr_scale_el = (x>=20&&x<=200)*(e_dsz[0]+e_dsz[1]*x);
    //   	}
    //   	else {
    //   	  const double x = pt;
	  
    //       //2017 B
    //       //electron 
    //       // const double e_dxy[2] = {1.170410154026039, -0.00015029075777466504};
    //       // const double e_dsz[2] = {1.1099677806775403, 0.00043288105494967803}; 

    //       // dxyerr_scale_el = (x>=20&&x<=200)*(e_dxy[0]+e_dxy[1]*x);
    //       // dszerr_scale_el = (x>=20&&x<=200)*(e_dsz[0]+e_dsz[1]*x);
          
    //       // //2017 C
    //       // //electron 
    //       // const double e_dxy[2] = {1.2057194508431224, 0.00012593984775844357};
    //       // const double e_dsz[2] = {1.2565529221655773, 0.00039439387574306123}; 

    //       // dxyerr_scale_el = (x>=20&&x<=200)*(e_dxy[0]+e_dxy[1]*x);
    //       // dszerr_scale_el = (x>=20&&x<=200)*(e_dsz[0]+e_dsz[1]*x);
      
    //       // //2017 D
    //       // //electron 
    //       // const double e_dxy[2] = {1.1761188847482749, 0.0001398415228549936};
    //       // const double e_dsz[2] = {1.116270698700518, 0.00061093509987282}; 

    //       // dxyerr_scale_el = (x>=20&&x<=200)*(e_dxy[0]+e_dxy[1]*x);
    //       // dszerr_scale_el = (x>=20&&x<=200)*(e_dsz[0]+e_dsz[1]*x);
          
    //       // //2017 E
    //       // //electron 
    //       // const double e_dxy[2] = {1.1648523225295881, 0.00010905658578916344};
    //       // const double e_dsz[2] = {1.078683273620775, 0.0007123812217371458}; 

    //       // dxyerr_scale_el = (x>=20&&x<=200)*(e_dxy[0]+e_dxy[1]*x);
    //       // dszerr_scale_el = (x>=20&&x<=200)*(e_dsz[0]+e_dsz[1]*x);
                
    //       // //2017 F
    //       // //electron 
    //       const double e_dxy[2] = {1.3092795940264987, -0.00023650767360119604};
    //       const double e_dsz[2] = {1.477456468774621, 0.00039462740911918627}; 

    //       dxyerr_scale_el = (x>=20&&x<=200)*(e_dxy[0]+e_dxy[1]*x);
    //       dszerr_scale_el = (x>=20&&x<=200)*(e_dsz[0]+e_dsz[1]*x);
    //     }
    //     //for electrons 
    //     rescaled_dxyerr_el *= dxyerr_scale_el;
    //     rescaled_dxydszcov_el *= sqrt(dxyerr_scale_el);
    //     rescaled_dszerr_el *= dszerr_scale_el;
    //     rescaled_dxydszcov_el *= sqrt(dszerr_scale_el);
       
    //   }
    //   const double nsigmadxy_el = dxybs / rescaled_dxyerr_el;
    //   if (pt > 1 && etarange && min_r <=1 && npxlayers >=2 && nstlayers >=6) {

	  //     if (pass_ele) {
    //       h_eletracks_pt[1]->Fill(pt, w);
    //       h_eletracks_eta[1]->Fill(nte.eta(ie), w);
    //       h_eletracks_phi[1]->Fill(nte.phi(ie), w);
    //       h_eletracks_dxy[1]->Fill(dxybs, w);
    //       h_eletracks_absdxy[1]->Fill(fabs(dxybs), w);
    //       h_eletracks_dsz[1]->Fill(dsz, w);
    //       h_eletracks_dz[1]->Fill(dz, w);
    //       h_eletracks_dxyerr[1]->Fill(rescaled_dxyerr_el, w);

    //       // if (pt<=20)             h_eletracks_dxyerr_pt[1][0]->Fill(nte.err_dxy(ie), w);
    //       // if (pt>20 && pt<=40)    h_eletracks_dxyerr_pt[1][1]->Fill(nte.err_dxy(ie), w);
    //       // if (pt>40 && pt<=60)    h_eletracks_dxyerr_pt[1][2]->Fill(nte.err_dxy(ie), w);
    //       // if (pt>60 && pt<=90)    h_eletracks_dxyerr_pt[1][3]->Fill(nte.err_dxy(ie), w);
    //       // if (pt>90 && pt<=130)   h_eletracks_dxyerr_pt[1][4]->Fill(nte.err_dxy(ie), w);
    //       // if (pt>130 && pt<=200)  h_eletracks_dxyerr_pt[1][5]->Fill(nte.err_dxy(ie), w);
    //       h_eletracks_absnsigmadxy[1]->Fill(nsigmadxy_el, w);
    //       h_eletracks_nsigmadxy[1]->Fill(dxybs / rescaled_dxyerr_el, w);
    //       h_eletracks_nsigmadsz[1]->Fill(dsz / rescaled_dszerr_el, w);
    //       h_eletracks_dxydszcov[1]->Fill(rescaled_dxydszcov_el, w);
    //       h_eletracks_absdxydszcov[1]->Fill(fabs(rescaled_dxydszcov_el), w);
    //       h_eletracks_dzerr[1]->Fill(nte.err_dz(ie), w);
    //       h_eletracks_dszerr[1]->Fill(rescaled_dszerr_el, w);
    //       h_eletracks_lambdaerr[1]->Fill(nte.err_lambda(ie), w);
    //       h_eletracks_pterr[1]->Fill(nte.err_pt(ie), w);
    //       h_eletracks_phierr[1]->Fill(nte.err_phi(ie), w);
    //       h_eletracks_etaerr[1]->Fill(nte.err_eta(ie), w);
    //       // h_eletracks_dszerr_v_pt[1]->Fill(pt, nte.err_dsz(ie), w);
    //       // h_eletracks_dxyerr_v_pt[1]->Fill(pt, nte.err_dxy(ie), w);
    //       // h_eletracks_dxyerr_v_eta[1]->Fill(nte.eta(ie), nte.err_dxy(ie), w);
    //       // h_eletracks_dxyerr_v_phi[1]->Fill(nte.phi(ie), nte.err_dxy(ie), w);
    //       // h_eletracks_dszerr_v_eta[1]->Fill(nte.eta(ie), nte.err_dxy(ie), w);
    //       // h_eletracks_dszerr_v_phi[1]->Fill(nte.phi(ie), nte.err_dxy(ie), w);

    //       h_eletracks_dxyerr_v_pt[1]->Fill(pt, rescaled_dxyerr_el, w);
    //       h_eletracks_dxyerr_v_eta[1]->Fill(nte.eta(ie), rescaled_dxyerr_el, w);
    //       h_eletracks_dxyerr_v_phi[1]->Fill(nte.phi(ie), rescaled_dxyerr_el, w);
    //       h_eletracks_dxyerr_v_minr[1]->Fill(nte.min_r(ie), rescaled_dxyerr_el, w);
    //       h_eletracks_dszerr_v_pt[1]->Fill(pt, rescaled_dszerr_el, w);
    //       h_eletracks_dszerr_v_eta[1]->Fill(nte.eta(ie), rescaled_dszerr_el, w);
    //       h_eletracks_dszerr_v_phi[1]->Fill(nte.phi(ie), rescaled_dszerr_el, w);
        
    //       h_eletracks_dxydszcov_v_pt[1]->Fill(pt, rescaled_dxydszcov_el, w);
    //       h_eletracks_dxydszcov_v_eta[1]->Fill(nte.eta(ie), rescaled_dxydszcov_el, w);
    //       h_eletracks_dxydszcov_v_phi[1]->Fill(nte.phi(ie), rescaled_dxydszcov_el, w);
    //       h_eletracks_absdxydszcov_v_pt[1]->Fill(pt, fabs(rescaled_dxydszcov_el), w);
    //       h_eletracks_absdxydszcov_v_eta[1]->Fill(nte.eta(ie), fabs(rescaled_dxydszcov_el), w);
    //       h_eletracks_absdxydszcov_v_phi[1]->Fill(nte.phi(ie), fabs(rescaled_dxydszcov_el), w);
	  //     } 
    //   }
    // }
    // for (int im = 0, ime = ntm.n(); im < ime; ++im) {
    //   const double pt = ntm.pt(im);
    //   const double dxybs = ntm.dxybs(im, nt.bs());
    //   const float dsz = (ntm.vz(im)) * pt / ntm.p(im) - ((ntm.vx(im)) * ntm.px(im) + (ntm.vy(im)) * ntm.py(im)) / pt * ntm.pz(im) / ntm.p(im);
    //   const float dz = ntm.vz(im) - (ntm.vx(im) * ntm.px(im) + ntm.vy(im) * ntm.py(im)) / pt * ntm.pz(im) / pt;
    //   const int min_r = ntm.min_r(im);
    //   const int npxlayers = ntm.npxlayers(im);
    //   const int nstlayers = ntm.nstlayers(im);
      
    //   const bool mef[4] = {
    //     pt >= 20,
    //   	ntm.eta(im) < 2.4,
    //   	ntm.iso(im) < 0.15,
    //   	ntm.isMed(im)
    //   };
      
    //   const bool pass_mu = mef[0] && mef[1] && mef[2] && mef[3];
    //   //const bool pass_nm1mf = mef[1] && mef[2] && mef[3];

    //   const bool etagt1p5 = false;
    //   bool etarange =false;
    //   if (etagt1p5)
    //     etarange = fabs(ntm.eta(im)) > 1.5;
    //   else
    //     etarange = fabs(ntm.eta(im)) < 1.5;

    //   double rescaled_dxyerr_mu = ntm.err_dxy(im);
    //   double rescaled_dszerr_mu = ntm.err_dsz(im);
    //   double rescaled_dxydszcov_mu = ntm.cov_34(im);

    //   const bool rescale_tracks = false;
    //   if (rescale_tracks) {
    //     double dxyerr_scale_mu = 1.;
    //     double dszerr_scale_mu = 1.;
	
    //     if (fabs(ntm.eta(im)) < 1.5) {
    //       const double x = pt;

	  //        //2017 B
	  //       //muon
	  //       // const double m_dxy[2] = {1.2148062639351913, 0.00012377341911564733};
	  //       // const double m_dsz[2] = {1.1730021966468054, -0.000149736302669597}; 

	  //       // dxyerr_scale_mu = (x>=20&&x<=200)*(m_dxy[0]+m_dxy[1]*x);
	  //       // dszerr_scale_mu = (x>=20&&x<=200)*(m_dsz[0]+m_dsz[1]*x);
	 
    //       // //2017 C
    //       // //muon
    //       // const double m_dxy[2] = {1.2369182541723913, 0.00006638107717464939};
    //       // const double m_dsz[2] = {1.2875566271184316, -0.00015059072827484053}; 

    //       // dxyerr_scale_mu = (x>=20&&x<=200)*(m_dxy[0]+m_dxy[1]*x);
    //       // dszerr_scale_mu = (x>=20&&x<=200)*(m_dsz[0]+m_dsz[1]*x);
        
    //       // //2017 D
    //       // //muon
    //       // const double m_dxy[2] = {1.2014547625589436, -0.0003230230107513707};
    //       // const double m_dsz[2] = {1.2362920471954792, -0.0001124554074662925}; 

    //       // dxyerr_scale_mu = (x>=20&&x<=200)*(m_dxy[0]+m_dxy[1]*x);
    //       // dszerr_scale_mu = (x>=20&&x<=200)*(m_dsz[0]+m_dsz[1]*x);
        
    //       // //2017 E
    //       // //muon
    //       // const double m_dxy[2] = {1.1073581182642487, -0.0002688182632471052};
    //       // const double m_dsz[2] = {1.1124654017857332, -0.00006862041740876568}; 

    //       // dxyerr_scale_mu = (x>=20&&x<=200)*(m_dxy[0]+m_dxy[1]*x);
    //       // dszerr_scale_mu = (x>=20&&x<=200)*(m_dsz[0]+m_dsz[1]*x);
         
    //       // //2017 F
    //       // //muon
    //       const double m_dxy[2] = {1.1855136718401231, -0.00008035979201444395};
    //       const double m_dsz[2] = {1.1709976385402432, -0.00013193247852357447}; 

    //       dxyerr_scale_mu = (x>=20&&x<=200)*(m_dxy[0]+m_dxy[1]*x);
    //       dszerr_scale_mu = (x>=20&&x<=200)*(m_dsz[0]+m_dsz[1]*x);
    //   	}
    //   	else {
    //   	  const double x = pt;
	  
    //       //2017 B
    //       //muon
    //       // const double m_dxy[2] = {1.2881888374900963, -0.0006996192395661432};
    //       // const double m_dsz[2] = {1.0975750359065857, -0.00021900979665942163}; 

    //       // dxyerr_scale_mu = (x>=20&&x<=200)*(m_dxy[0]+m_dxy[1]*x);
    //       // dszerr_scale_mu = (x>=20&&x<=200)*(m_dsz[0]+m_dsz[1]*x);
        
    //       // //2017 C
    //       // //muon
    //       // const double m_dxy[2] = {1.3142661391870103, -0.0008179089771729025};
    //       // const double m_dsz[2] = {1.2290616916291792, -0.00019044437771609073}; 

    //       // dxyerr_scale_mu = (x>=20&&x<=200)*(m_dxy[0]+m_dxy[1]*x);
    //       // dszerr_scale_mu = (x>=20&&x<=200)*(m_dsz[0]+m_dsz[1]*x);
	 
    //       // //2017 D
    //       // //muon
    //       // const double m_dxy[2] = {1.28569782063072, -0.0007018332128769147};
    //       // const double m_dsz[2] = {1.1359875496520355, -0.00009653597906441966}; 

    //       // dxyerr_scale_mu = (x>=20&&x<=200)*(m_dxy[0]+m_dxy[1]*x);
    //       // dszerr_scale_mu = (x>=20&&x<=200)*(m_dsz[0]+m_dsz[1]*x);
        
    //       // //2017 E
    //       // //muon
    //       // const double m_dxy[2] = {1.241991737450876, -0.0005439955810617094};
    //       // const double m_dsz[2] = {1.0999736323133213, -0.00014218890677155684}; 

    //       // dxyerr_scale_mu = (x>=20&&x<=200)*(m_dxy[0]+m_dxy[1]*x);
    //       // dszerr_scale_mu = (x>=20&&x<=200)*(m_dsz[0]+m_dsz[1]*x);
        
    //       // //2017 F
    //       // //muon
    //       const double m_dxy[2] = {1.3276007175478752, -0.0005551829741863527};
    //       const double m_dsz[2] = {1.5071250531650895, -0.00033371136752079894}; 

    //       dxyerr_scale_mu = (x>=20&&x<=200)*(m_dxy[0]+m_dxy[1]*x);
    //       dszerr_scale_mu = (x>=20&&x<=200)*(m_dsz[0]+m_dsz[1]*x);
    //     }
    //     //for muons 
    //     rescaled_dxyerr_mu *= dxyerr_scale_mu;
    //     rescaled_dxydszcov_mu *= sqrt(dxyerr_scale_mu);
    //     rescaled_dszerr_mu *= dszerr_scale_mu;
    //     rescaled_dxydszcov_mu *= sqrt(dszerr_scale_mu);
    //   }
    //   const double nsigmadxy_mu = dxybs / rescaled_dxyerr_mu;
      
    //   if (pt > 1 && etarange && min_r <=1 && npxlayers >=2 && nstlayers >=6) {
	
	  //     if (pass_mu) {
    //       h_eletracks_pt[0]->Fill(pt, w);
    //       h_eletracks_eta[0]->Fill(ntm.eta(im), w);
    //       h_eletracks_phi[0]->Fill(ntm.phi(im), w);
    //       h_eletracks_dxy[0]->Fill(dxybs, w);
    //       h_tracks_absdxy[0]->Fill(fabs(dxybs), w);
    //       h_eletracks_dz[0]->Fill(dz, w);
    //       h_eletracks_dsz[0]->Fill(dsz, w);

    //       h_eletracks_dxyerr[0]->Fill(rescaled_dxyerr_mu, w);
    //       h_eletracks_dxydszcov[0]->Fill(rescaled_dxydszcov_mu, w);
    //       h_eletracks_absdxydszcov[0]->Fill(fabs(rescaled_dxydszcov_mu), w);
    //       // if (pt<=20)             h_eletracks_dxyerr_pt[0][0]->Fill(ntm.err_dxy(im), w);
    //       // if (pt>20 && pt<=40)    h_eletracks_dxyerr_pt[0][1]->Fill(ntm.err_dxy(im), w);
    //       // if (pt>40 && pt<=60)    h_eletracks_dxyerr_pt[0][2]->Fill(ntm.err_dxy(im), w);
    //       // if (pt>60 && pt<=90)    h_eletracks_dxyerr_pt[0][3]->Fill(ntm.err_dxy(im), w);
    //       // if (pt>90 && pt<=130)   h_eletracks_dxyerr_pt[0][4]->Fill(ntm.err_dxy(im), w);
    //       // if (pt>130 && pt<=200)  h_eletracks_dxyerr_pt[0][5]->Fill(ntm.err_dxy(im), w);
    //       h_eletracks_absnsigmadxy[0]->Fill(nsigmadxy_mu, w);
    //       h_eletracks_nsigmadxy[0]->Fill(dxybs / rescaled_dxyerr_mu, w);
    //       h_eletracks_nsigmadsz[0]->Fill(dsz / rescaled_dszerr_mu, w);
    //       h_eletracks_dszerr[0]->Fill(rescaled_dszerr_mu, w);
    //       h_eletracks_lambdaerr[0]->Fill(ntm.err_lambda(im), w);
    //       h_eletracks_pterr[0]->Fill(ntm.err_pt(im), w);
    //       h_eletracks_phierr[0]->Fill(ntm.err_phi(im), w);
    //       h_eletracks_etaerr[0]->Fill(ntm.err_eta(im), w);
    //       // h_eletracks_dszerr_v_pt[0]->Fill(pt, ntm.err_dsz(im), w);
    //       // h_eletracks_dxyerr_v_pt[0]->Fill(pt, ntm.err_dxy(im), w);
    //       // h_eletracks_dxyerr_v_eta[0]->Fill(ntm.eta(im), ntm.err_dxy(im), w);
    //       // h_eletracks_dxyerr_v_phi[0]->Fill(ntm.phi(im), ntm.err_dxy(im), w);
    //       // h_eletracks_dszerr_v_eta[0]->Fill(ntm.eta(im), ntm.err_dxy(im), w);
    //       // h_eletracks_dszerr_v_phi[0]->Fill(ntm.phi(im), ntm.err_dxy(im), w);

          
    //       h_eletracks_dxyerr_v_pt[0]->Fill(pt, rescaled_dxyerr_mu, w);
    //       h_eletracks_dxyerr_v_eta[0]->Fill(ntm.eta(im), rescaled_dxyerr_mu, w);
    //       h_eletracks_dxyerr_v_phi[0]->Fill(ntm.phi(im), rescaled_dxyerr_mu, w);
    //       h_eletracks_dxyerr_v_minr[0]->Fill(ntm.min_r(im), rescaled_dxyerr_mu, w);

    //       h_eletracks_dszerr_v_pt[0]->Fill(pt, rescaled_dszerr_mu, w);
    //       h_eletracks_dszerr_v_eta[0]->Fill(ntm.eta(im), rescaled_dszerr_mu, w);
    //       h_eletracks_dszerr_v_phi[0]->Fill(ntm.phi(im), rescaled_dszerr_mu, w);
        
    //       h_eletracks_dxydszcov_v_pt[0]->Fill(pt, rescaled_dxydszcov_mu, w);
    //       h_eletracks_dxydszcov_v_eta[0]->Fill(ntm.eta(im), rescaled_dxydszcov_mu, w);
    //       h_eletracks_dxydszcov_v_phi[0]->Fill(ntm.phi(im), rescaled_dxydszcov_mu, w);
    //       h_eletracks_absdxydszcov_v_pt[0]->Fill(pt, fabs(rescaled_dxydszcov_mu), w);
    //       h_eletracks_absdxydszcov_v_eta[0]->Fill(ntm.eta(im), fabs(rescaled_dxydszcov_mu), w);
    //       h_eletracks_absdxydszcov_v_phi[0]->Fill(ntm.phi(im), fabs(rescaled_dxydszcov_mu), w);
    //   	} 
    //   }
    // }

    //////////////////////////////////////////////
    ///                                        ///
    /// new way to work with electrons & muons ///
    ///  try 1 : no selections on lep tracks   ///
    ///     besides usual track & pt ≥ 20      ///
    //////////////////////////////////////////////

    for (int ie = 0, iee = nte.n(); ie < iee; ++ie) {
      const double pt = nte.pt(ie);
      const int min_r = nte.min_r(ie);
      const int losthits = nte.losthit(ie);
      const int npxlayers = nte.npxlayers(ie);
      const int nstlayers = nte.nstlayers(ie);
      const double dxybs = nte.dxybs(ie, nt.bs());
      //const double nsigmadxy = ntt.nsigmadxybs(itk, nt.bs());
      
      const bool etagt1p5 = false;
      bool etarange =false;
      if (etagt1p5)
        etarange = fabs(nte.eta(ie)) > 1.5;
      else
        etarange = fabs(nte.eta(ie)) < 1.5;

      double rescaled_dxyerr_el = nte.err_dxy(ie);
      double rescaled_dszerr_el = nte.err_dsz(ie);
      double rescaled_dxydszcov_el = nte.cov_34(ie);
      
      const bool rescale_tracks = false;
      if (rescale_tracks) {
        double dxyerr_scale_el = 1.;
        double dszerr_scale_el = 1.;
	
        if (fabs(nte.eta(ie)) < 1.5) {
         const double x = pt;
          //2017 B
	        //electron 
	        // const double e_dxy[2] = {1.2519894918062238, 0.00007487187197916488};
	        // const double e_dsz[2] = {1.1378345538232282, 0.000015006579023894503}; 

	        // dxyerr_scale_el = (x>=20&&x<=200)*(e_dxy[0]+e_dxy[1]*x);
	        // dszerr_scale_el = (x>=20&&x<=200)*(e_dsz[0]+e_dsz[1]*x);
          
          // //2017 C
          // //electron 
          // const double e_dxy[2] = {1.2813251299194244, 0.0000980634546644231};
          // const double e_dsz[2] = {1.2396626500193402, 0.0001031872972430143}; 

          // dxyerr_scale_el = (x>=20&&x<=200)*(e_dxy[0]+e_dxy[1]*x);
          // dszerr_scale_el = (x>=20&&x<=200)*(e_dsz[0]+e_dsz[1]*x);

          // //2017 D
          // //electron 
          // const double e_dxy[2] = {1.2175109728215536, 0.00015468622838992613};
          // const double e_dsz[2] = {1.193086410468232, 0.00009273527660223248}; 

          // dxyerr_scale_el = (x>=20&&x<=200)*(e_dxy[0]+e_dxy[1]*x);
          // dszerr_scale_el = (x>=20&&x<=200)*(e_dsz[0]+e_dsz[1]*x);
          
          // //2017 E
          // //electron 
          // const double e_dxy[2] = {1.1391061605726946, 0.000101181227594822};
          // const double e_dsz[2] = {1.0759837837776636, 0.00012897972750002158}; 

          // dxyerr_scale_el = (x>=20&&x<=200)*(e_dxy[0]+e_dxy[1]*x);
          // dszerr_scale_el = (x>=20&&x<=200)*(e_dsz[0]+e_dsz[1]*x);
         
          // //2017 F
          //electron 
        const double e_dxy[2] = {1.2163661067927056, 0.0001401403672766123};
        const double e_dsz[2] = {1.1387132063959098, 0.00017118239591405043}; 

         dxyerr_scale_el = (x>=20&&x<=200)*(e_dxy[0]+e_dxy[1]*x);
         dszerr_scale_el = (x>=20&&x<=200)*(e_dsz[0]+e_dsz[1]*x);

      	}
      	else {
      	  const double x = pt;
          //2017 B
          //electron 
          // const double e_dxy[2] = {1.170410154026039, -0.00015029075777466504};
          // const double e_dsz[2] = {1.1099677806775403, 0.00043288105494967803}; 

          // dxyerr_scale_el = (x>=20&&x<=200)*(e_dxy[0]+e_dxy[1]*x);
          // dszerr_scale_el = (x>=20&&x<=200)*(e_dsz[0]+e_dsz[1]*x);
          
          //2017 C
          //electron 
          // const double e_dxy[2] = {1.2057194508431224, 0.00012593984775844357};
          // const double e_dsz[2] = {1.2565529221655773, 0.00039439387574306123}; 

          // dxyerr_scale_el = (x>=20&&x<=200)*(e_dxy[0]+e_dxy[1]*x);
          // dszerr_scale_el = (x>=20&&x<=200)*(e_dsz[0]+e_dsz[1]*x);
      
          //2017 D
          //electron 
          // const double e_dxy[2] = {1.1761188847482749, 0.0001398415228549936};
          // const double e_dsz[2] = {1.116270698700518, 0.00061093509987282}; 

          // dxyerr_scale_el = (x>=20&&x<=200)*(e_dxy[0]+e_dxy[1]*x);
          // dszerr_scale_el = (x>=20&&x<=200)*(e_dsz[0]+e_dsz[1]*x);
          
          //2017 E
          //electron 
          // const double e_dxy[2] = {1.1648523225295881, 0.00010905658578916344};
          // const double e_dsz[2] = {1.078683273620775, 0.0007123812217371458}; 

          // dxyerr_scale_el = (x>=20&&x<=200)*(e_dxy[0]+e_dxy[1]*x);
          // dszerr_scale_el = (x>=20&&x<=200)*(e_dsz[0]+e_dsz[1]*x);
                
        //2017 F
        //electron 
        const double e_dxy[2] = {1.3092795940264987, -0.00023650767360119604};
        const double e_dsz[2] = {1.477456468774621, 0.00039462740911918627}; 

        dxyerr_scale_el = (x>=20&&x<=200)*(e_dxy[0]+e_dxy[1]*x);
        dszerr_scale_el = (x>=20&&x<=200)*(e_dsz[0]+e_dsz[1]*x);

        }
        rescaled_dxyerr_el *= dxyerr_scale_el;
        rescaled_dxydszcov_el *= sqrt(dxyerr_scale_el);
        rescaled_dszerr_el *= dszerr_scale_el;
        rescaled_dxydszcov_el *= sqrt(dszerr_scale_el);
      }
      const double nsigmadxy_el = dxybs / rescaled_dxyerr_el;

      // the pt cut should already be in place ... we will see 
      const bool nm1[5] = {
        pt > 1,
        min_r <= 1 || (min_r == 2 && losthits == 0),
        npxlayers >= 2,
        nstlayers >= 6,
        nsigmadxy_el > 3
  
      };

      const bool sel = nm1[0] && nm1[1] && nm1[2] && nm1[3];
      const bool seed = sel && nm1[4];

      const bool tk_ok[max_ele_type] = { true, sel, seed };

      for (int i = 0; i < max_ele_type; ++i) {
	      if (!tk_ok[i] || !etarange) continue;
        ++neletracks[i];

        h_eletracks_pt[i]->Fill(pt, w);
        h_eletracks_eta[i]->Fill(nte.eta(ie), w);
        h_eletracks_phi[i]->Fill(nte.phi(ie), w);
        h_eletracks_dxy[i]->Fill(dxybs, w);
        h_eletracks_dsz[i]->Fill(nte.dsz(ie), w);
        h_eletracks_dz[i]->Fill(nte.dz(ie), w);

        h_eletracks_absnsigmadxy[i]->Fill(nsigmadxy_el, w);
        h_eletracks_nsigmadxy[i]->Fill(dxybs / rescaled_dxyerr_el, w);
        h_eletracks_nsigmadsz[i]->Fill(nte.dsz(ie) / rescaled_dszerr_el, w);
        
        h_eletracks_dxyerr[i]->Fill(rescaled_dxyerr_el, w);
        h_eletracks_dxydszcov[i]->Fill(rescaled_dxydszcov_el, w);
        h_eletracks_absdxydszcov[i]->Fill(fabs(rescaled_dxydszcov_el), w);
        h_eletracks_dzerr[i]->Fill(nte.err_dz(ie), w);
        h_eletracks_dszerr[i]->Fill(rescaled_dszerr_el, w);
        h_eletracks_lambdaerr[i]->Fill(nte.err_lambda(ie), w);
        h_eletracks_pterr[i]->Fill(nte.err_pt(ie), w);
        h_eletracks_phierr[i]->Fill(nte.err_phi(ie), w);
        h_eletracks_etaerr[i]->Fill(nte.err_eta(ie), w);

        h_eletracks_dxyerr_v_pt[i]->Fill(pt, rescaled_dxyerr_el, w);
        h_eletracks_dxyerr_v_eta[i]->Fill(nte.eta(ie), rescaled_dxyerr_el, w);
        h_eletracks_dxyerr_v_phi[i]->Fill(nte.phi(ie), rescaled_dxyerr_el, w);
        h_eletracks_dxyerr_v_minr[i]->Fill(nte.min_r(ie), rescaled_dxyerr_el, w);

        h_eletracks_dszerr_v_pt[i]->Fill(pt, rescaled_dszerr_el, w);
        h_eletracks_dszerr_v_eta[i]->Fill(nte.eta(ie), rescaled_dszerr_el, w);
        h_eletracks_dszerr_v_phi[i]->Fill(nte.phi(ie), rescaled_dszerr_el, w);
        
        h_eletracks_dxydszcov_v_pt[i]->Fill(pt, rescaled_dxydszcov_el, w);
        h_eletracks_dxydszcov_v_eta[i]->Fill(nte.eta(ie), rescaled_dxydszcov_el, w);
        h_eletracks_dxydszcov_v_phi[i]->Fill(nte.phi(ie), rescaled_dxydszcov_el, w);
        h_eletracks_absdxydszcov_v_pt[i]->Fill(pt, fabs(rescaled_dxydszcov_el), w);
        h_eletracks_absdxydszcov_v_eta[i]->Fill(nte.eta(ie), fabs(rescaled_dxydszcov_el), w);
        h_eletracks_absdxydszcov_v_phi[i]->Fill(nte.phi(ie), fabs(rescaled_dxydszcov_el), w);
        h_eletracks_eta_v_phi[i]->Fill(nte.phi(ie), nte.eta(ie), w);
      }
    }

    for (int im = 0, imm = ntm.n(); im < imm; ++im) {
      const double pt = ntm.pt(im);
      const int min_r = ntm.min_r(im);
      const int losthits = ntm.losthit(im);
      const int npxlayers = ntm.npxlayers(im);
      const int nstlayers = ntm.nstlayers(im);
      const double dxybs = ntm.dxybs(im, nt.bs());
      //const double nsigmadxy = ntt.nsigmadxybs(itk, nt.bs());
      
      const bool etagt1p5 = false;
      bool etarange =false;
      if (etagt1p5)
        etarange = fabs(ntm.eta(im)) > 1.5;
      else
        etarange = fabs(ntm.eta(im)) < 1.5;

      double rescaled_dxyerr_mu = ntm.err_dxy(im);
      double rescaled_dszerr_mu = ntm.err_dsz(im);
      double rescaled_dxydszcov_mu = ntm.cov_34(im);
      
      const bool rescale_tracks = false;
      if (rescale_tracks) {
        double dxyerr_scale_mu = 1.;
        double dszerr_scale_mu = 1.;
	
        if (fabs(ntm.eta(im)) < 1.5) {
          const double x = pt;
	        //2017 B
	        //muon
	        // const double m_dxy[2] = {1.2148062639351913, 0.00012377341911564733};
	        // const double m_dsz[2] = {1.1730021966468054, -0.000149736302669597}; 

	        // dxyerr_scale_mu = (x>=20&&x<=200)*(m_dxy[0]+m_dxy[1]*x);
	        // dszerr_scale_mu = (x>=20&&x<=200)*(m_dsz[0]+m_dsz[1]*x);
	 
          // //2017 C
          // //muon
          // const double m_dxy[2] = {1.2369182541723913, 0.00006638107717464939};
          // const double m_dsz[2] = {1.2875566271184316, -0.00015059072827484053}; 

          // dxyerr_scale_mu = (x>=20&&x<=200)*(m_dxy[0]+m_dxy[1]*x);
          // dszerr_scale_mu = (x>=20&&x<=200)*(m_dsz[0]+m_dsz[1]*x);
        
          // //2017 D
          // //muon
          // const double m_dxy[2] = {1.2014547625589436, -0.0003230230107513707};
          // const double m_dsz[2] = {1.2362920471954792, -0.0001124554074662925}; 

          // dxyerr_scale_mu = (x>=20&&x<=200)*(m_dxy[0]+m_dxy[1]*x);
          // dszerr_scale_mu = (x>=20&&x<=200)*(m_dsz[0]+m_dsz[1]*x);
        
          // //2017 E
          // //muon
          // const double m_dxy[2] = {1.1073581182642487, -0.0002688182632471052};
          // const double m_dsz[2] = {1.1124654017857332, -0.00006862041740876568}; 

          // dxyerr_scale_mu = (x>=20&&x<=200)*(m_dxy[0]+m_dxy[1]*x);
          // dszerr_scale_mu = (x>=20&&x<=200)*(m_dsz[0]+m_dsz[1]*x);
         
          //2017 F
          //muon
          const double m_dxy[2] = {1.1855136718401231, -0.00008035979201444395};
          const double m_dsz[2] = {1.1709976385402432, -0.00013193247852357447}; 

          dxyerr_scale_mu = (x>=20&&x<=200)*(m_dxy[0]+m_dxy[1]*x);
          dszerr_scale_mu = (x>=20&&x<=200)*(m_dsz[0]+m_dsz[1]*x);
        }
        else {
      	  const double x = pt;
          //2017 B
          //muon
          // const double m_dxy[2] = {1.2881888374900963, -0.0006996192395661432};
          // const double m_dsz[2] = {1.0975750359065857, -0.00021900979665942163}; 

          // dxyerr_scale_mu = (x>=20&&x<=200)*(m_dxy[0]+m_dxy[1]*x);
          // dszerr_scale_mu = (x>=20&&x<=200)*(m_dsz[0]+m_dsz[1]*x);
        
          //2017 C
          //muon
          // const double m_dxy[2] = {1.3142661391870103, -0.0008179089771729025};
          // const double m_dsz[2] = {1.2290616916291792, -0.00019044437771609073}; 

          // dxyerr_scale_mu = (x>=20&&x<=200)*(m_dxy[0]+m_dxy[1]*x);
          // dszerr_scale_mu = (x>=20&&x<=200)*(m_dsz[0]+m_dsz[1]*x);
	 
          //2017 D
          //muon
          // const double m_dxy[2] = {1.28569782063072, -0.0007018332128769147};
          // const double m_dsz[2] = {1.1359875496520355, -0.00009653597906441966}; 

          // dxyerr_scale_mu = (x>=20&&x<=200)*(m_dxy[0]+m_dxy[1]*x);
          // dszerr_scale_mu = (x>=20&&x<=200)*(m_dsz[0]+m_dsz[1]*x);
        
          // //2017 E
          // //muon
          // const double m_dxy[2] = {1.241991737450876, -0.0005439955810617094};
          // const double m_dsz[2] = {1.0999736323133213, -0.00014218890677155684}; 

          // dxyerr_scale_mu = (x>=20&&x<=200)*(m_dxy[0]+m_dxy[1]*x);
          // dszerr_scale_mu = (x>=20&&x<=200)*(m_dsz[0]+m_dsz[1]*x);
        
          //2017 F
          //muon
          const double m_dxy[2] = {1.3276007175478752, -0.0005551829741863527};
          const double m_dsz[2] = {1.5071250531650895, -0.00033371136752079894}; 

          dxyerr_scale_mu = (x>=20&&x<=200)*(m_dxy[0]+m_dxy[1]*x);
          dszerr_scale_mu = (x>=20&&x<=200)*(m_dsz[0]+m_dsz[1]*x);
        }
        rescaled_dxyerr_mu *= dxyerr_scale_mu;
        rescaled_dxydszcov_mu *= sqrt(dxyerr_scale_mu);
        rescaled_dszerr_mu *= dszerr_scale_mu;
        rescaled_dxydszcov_mu *= sqrt(dszerr_scale_mu);
      }
      const double nsigmadxy_mu = dxybs / rescaled_dxyerr_mu;

      // the pt cut should already be in place ... we will see 
      const bool nm1[5] = {
	      pt > 1,
	      min_r <= 1 || (min_r == 2 && losthits == 0),
	      npxlayers >= 2,
	      nstlayers >= 6,
	      nsigmadxy_mu > 3
	
      };

      const bool sel = nm1[0] && nm1[1] && nm1[2] && nm1[3];
      const bool seed = sel && nm1[4];

      const bool tk_ok[max_mu_type] = { true, sel, seed };

      for (int i = 0; i < max_mu_type; ++i) {
	      if (!tk_ok[i] || !etarange) continue;
        ++nmutracks[i];

        h_mutracks_pt[i]->Fill(pt, w);
        h_mutracks_eta[i]->Fill(ntm.eta(im), w);
        h_mutracks_phi[i]->Fill(ntm.phi(im), w);
        h_mutracks_dxy[i]->Fill(dxybs, w);
        h_mutracks_dsz[i]->Fill(ntm.dsz(im), w);
        h_mutracks_dz[i]->Fill(ntm.dz(im), w);

        h_mutracks_absnsigmadxy[i]->Fill(nsigmadxy_mu, w);
        h_mutracks_nsigmadxy[i]->Fill(dxybs / rescaled_dxyerr_mu, w);
        h_mutracks_nsigmadsz[i]->Fill(ntm.dsz(im) / rescaled_dszerr_mu, w);
        
        h_mutracks_dxyerr[i]->Fill(rescaled_dxyerr_mu, w);
        h_mutracks_dxydszcov[i]->Fill(rescaled_dxydszcov_mu, w);
        h_mutracks_absdxydszcov[i]->Fill(fabs(rescaled_dxydszcov_mu), w);
        h_mutracks_dzerr[i]->Fill(ntm.err_dz(im), w);
        h_mutracks_dszerr[i]->Fill(rescaled_dszerr_mu, w);
        h_mutracks_lambdaerr[i]->Fill(ntm.err_lambda(im), w);
        h_mutracks_pterr[i]->Fill(ntm.err_pt(im), w);
        h_mutracks_phierr[i]->Fill(ntm.err_phi(im), w);
        h_mutracks_etaerr[i]->Fill(ntm.err_eta(im), w);

        h_mutracks_dxyerr_v_pt[i]->Fill(pt, rescaled_dxyerr_mu, w);
        h_mutracks_dxyerr_v_eta[i]->Fill(ntm.eta(im), rescaled_dxyerr_mu, w);
        h_mutracks_dxyerr_v_phi[i]->Fill(ntm.phi(im), rescaled_dxyerr_mu, w);
        h_mutracks_dxyerr_v_minr[i]->Fill(ntm.min_r(im), rescaled_dxyerr_mu, w);

        h_mutracks_dszerr_v_pt[i]->Fill(pt, rescaled_dszerr_mu, w);
        h_mutracks_dszerr_v_eta[i]->Fill(ntm.eta(im), rescaled_dszerr_mu, w);
        h_mutracks_dszerr_v_phi[i]->Fill(ntm.phi(im), rescaled_dszerr_mu, w);
        
        h_mutracks_dxydszcov_v_pt[i]->Fill(pt, rescaled_dxydszcov_mu, w);
        h_mutracks_dxydszcov_v_eta[i]->Fill(ntm.eta(im), rescaled_dxydszcov_mu, w);
        h_mutracks_dxydszcov_v_phi[i]->Fill(ntm.phi(im), rescaled_dxydszcov_mu, w);
        h_mutracks_absdxydszcov_v_pt[i]->Fill(pt, fabs(rescaled_dxydszcov_mu), w);
        h_mutracks_absdxydszcov_v_eta[i]->Fill(ntm.eta(im), fabs(rescaled_dxydszcov_mu), w);
        h_mutracks_absdxydszcov_v_phi[i]->Fill(ntm.phi(im), fabs(rescaled_dxydszcov_mu), w);
        h_mutracks_eta_v_phi[i]->Fill(ntm.phi(im), ntm.eta(im), w);
      }
    }

    for (int itk = 0, itke = ntt.n(); itk < itke; ++itk) {
      const double pt = ntt.pt(itk);
      const int min_r = ntt.min_r(itk);
      const int npxlayers = ntt.npxlayers(itk);
      const int nstlayers = ntt.nstlayers(itk);
      const double dxybs = ntt.dxybs(itk, nt.bs());
      //const double nsigmadxy = ntt.nsigmadxybs(itk, nt.bs());
      
      //const bool high_purity = npxlayers == 4 && fabs(ntt.eta(itk)) < 0.8 && fabs(ntt.dz(itk)) < 10;
      const bool etagt1p5 = false;
      bool etarange =false;
      if (etagt1p5)
        etarange = fabs(ntt.eta(itk)) > 1.5;
      else
        etarange = fabs(ntt.eta(itk)) < 1.5;
      //const bool etagt1p5 = fabs(ntt.eta(itk)) > 1.5;
      //const bool etalt1p5 = fabs(ntt.eta(itk)) < 1.5;


      double rescaled_dxyerr = ntt.err_dxy(itk);
      double rescaled_dszerr = ntt.err_dsz(itk);
      double rescaled_dxydszcov = ntt.cov_34(itk);
      
      const bool rescale_tracks = false;
      if (rescale_tracks) {
        double dxyerr_scale = 1.;
        double dszerr_scale = 1.;
	
        if (fabs(ntt.eta(itk)) < 1.5) {
          const double x = pt;

	         //2017 B
          //lepton
          // const double p_dxy[7] = {1.0453400796831038, 0.0405096809208158, -0.002355288529547607, 1.2026299518900068, 0.0006884209860798037, 1.1628183104698713, 0.0012484679591100844};
          // const double p_dsz[7] = {1.1267638191956668, 0.04071139378352154, -0.004993679429027863, 1.2112382112431304, -0.0015965199500326682, 1.1820719170949545, -0.00023804650024970408}; 

          // dxyerr_scale = (x<=5)*(p_dxy[0]+p_dxy[1]*x+p_dxy[2]*pow(x,2))+(x>5&&x<=40)*(p_dxy[3]+p_dxy[4]*x)+(x>40&&x<=200)*(p_dxy[5]+p_dxy[6]*x);
          // dszerr_scale = (x<=5)*(p_dsz[0]+p_dsz[1]*x+p_dsz[2]*pow(x,2))+(x>5&&x<=20)*(p_dsz[3]+p_dsz[4]*x)+(x>20&&x<=200)*(p_dsz[5]+p_dsz[6]*x);
        
          // //2017 C
          // //lepton
          // const double p_dxy[6] = {1.059467179971021, 0.05379668254313902, -0.004041508581226136, 1.236348174338712, 0.000029641768229563253};
          // const double p_dsz[6] = {1.1991893761328978, 0.0487907633770176, -0.005827340581446815, 1.2971150890882188, -0.0005085699959177701}; 

          // dxyerr_scale = (x<=5)*(p_dxy[0]+p_dxy[1]*x+p_dxy[2]*pow(x,2))+(x>5&&x<=200)*(p_dxy[3]+p_dxy[4]*x);
          // dszerr_scale = (x<=5)*(p_dsz[0]+p_dsz[1]*x+p_dsz[2]*pow(x,2))+(x>5&&x<=200)*(p_dsz[3]+p_dsz[4]*x);
        
          // //2017 D
          // //lepton
          // const double p_dxy[5] = {1.0449551839136935, 0.041012710596001575, -0.0026308302035657934, 1.198510897027289, -0.00033693441739767035};
          // const double p_dsz[5] = {1.1097319617887849, 0.03692688935936872, -0.003343063431853366, 1.2226326293269942, -0.0001534036404185527}; 

          // dxyerr_scale = (x<=5)*(p_dxy[0]+p_dxy[1]*x+p_dxy[2]*pow(x,2))+(x>5&&x<=200)*(p_dxy[3]+p_dxy[4]*x);
          // dszerr_scale = (x<=5)*(p_dsz[0]+p_dsz[1]*x+p_dsz[2]*pow(x,2))+(x>5&&x<=200)*(p_dsz[3]+p_dsz[4]*x);
        
          // //2017 E
          // //lepton
          // const double p_dxy[7] = {1.0244332073862856, 0.03290524947424986, -0.0027323784897288084, 1.132001139436433, -0.0011119189151882758, 1.076278362109507, 0.0008572563517515314};
          // const double p_dsz[5] = {1.0537415747052477, 0.023983701628267545, -0.002460002718732854, 1.115437064592664, -0.00016771260788939852}; 

          // dxyerr_scale = (x<=5)*(p_dxy[0]+p_dxy[1]*x+p_dxy[2]*pow(x,2))+(x>5&&x<=25)*(p_dxy[3]+p_dxy[4]*x)+(x>25&&x<=200)*(p_dxy[5]+p_dxy[6]*x);
          // dszerr_scale = (x<=5)*(p_dsz[0]+p_dsz[1]*x+p_dsz[2]*pow(x,2))+(x>5&&x<=200)*(p_dsz[3]+p_dsz[4]*x);
        
          // //2017 F
          // //lepton
          const double p_dxy[5] = {1.0524177910998205, 0.041848772694468656, -0.003202316378398979, 1.187595864155141, 0.0006212914420966572};
          const double p_dsz[5] = {1.0723413122235423, 0.028069492349497793, -0.0025749250844388782, 1.1533497764875236, 0.00034982398555030627}; 

          dxyerr_scale = (x<=5)*(p_dxy[0]+p_dxy[1]*x+p_dxy[2]*pow(x,2))+(x>5&&x<=200)*(p_dxy[3]+p_dxy[4]*x);
          dszerr_scale = (x<=5)*(p_dsz[0]+p_dsz[1]*x+p_dsz[2]*pow(x,2))+(x>5&&x<=200)*(p_dsz[3]+p_dsz[4]*x);
        
      	}
      	else {
      	  const double x = pt;
	  
          //2017 B
          //lepton
          // const double p_dxy[10] = {1.0237963390144942, 0.025228551972129153, 0.002678260834765862, 1.0024003215617026, 0.05820706865079255, -0.003059743296013568, 1.327761185835826, -0.004335253393028475, 1.0754178383446944, 0.001335524261476772};
          // const double p_dsz[8] = {1.0130027293863002, 0.0072976252782243275, 0.001480929736347815, 1.0396274262965146, 0.013492728301925772, -0.0005486830311880401, 1.1158679644319554, 0.0005931286288834794}; 

          // dxyerr_scale = (x<=5)*(p_dxy[0]+p_dxy[1]*x+p_dxy[2]*pow(x,2))+(x>5&&x<=12)*(p_dxy[3]+p_dxy[4]*x+p_dxy[5]*pow(x,2))+(x>12&&x<=45)*(p_dxy[6]+p_dxy[7]*x)+(x>45&&x<=200)*(p_dxy[8]+p_dxy[9]*x);
          // dszerr_scale = (x<=5)*(p_dsz[0]+p_dsz[1]*x+p_dsz[2]*pow(x,2))+(x>5&&x<=15)*(p_dsz[3]+p_dsz[4]*x+p_dsz[5]*pow(x,2))+(x>15&&x<=200)*(p_dsz[6]+p_dsz[7]*x);
        
          // //2017 C
          // //lepton
          // const double p_dxy[10] = {1.0269757035384641, 0.03652092356271204, 0.0020506537577015, 1.0432846046584063, 0.06011209970321533, -0.003280163804422833, 1.3560590024477523, -0.0038667217262399536, 1.165308017858451, 0.0005497225128418062};
          // const double p_dsz[8] = {1.0267146227720167, 0.02592057099522661, 0.0017276417069966553, 1.108720183105023, 0.025694759947995006, -0.0010160634465168203, 1.2791039778843831, 0.0007467751701414265}; 

          // dxyerr_scale = (x<=5)*(p_dxy[0]+p_dxy[1]*x+p_dxy[2]*pow(x,2))+(x>5&&x<=10)*(p_dxy[3]+p_dxy[4]*x+p_dxy[5]*pow(x,2))+(x>10&&x<=45)*(p_dxy[6]+p_dxy[7]*x)+(x>45&&x<=200)*(p_dxy[8]+p_dxy[9]*x);
          // dszerr_scale = (x<=5)*(p_dsz[0]+p_dsz[1]*x+p_dsz[2]*pow(x,2))+(x>5&&x<=15)*(p_dsz[3]+p_dsz[4]*x+p_dsz[5]*pow(x,2))+(x>15&&x<=200)*(p_dsz[6]+p_dsz[7]*x);
        
          // //2017 D
          // //lepton
          // const double p_dxy[10] = {1.0217037283723767, 0.027483929818230807, 0.0021419428588488904, 1.0003174841213076, 0.05766924225842008, -0.0031461181804122596, 1.3031772486704725, -0.0038288864747483553, 1.1233917025819669, 0.0004739342947480858};
          // const double p_dsz[8] = {1.012088873572254, 0.008336848087783084, 0.001691285765957144, 1.0325662890433136, 0.01722447955856797, -0.0006509039305293584, 1.1560569363426048, 0.00017076396669853553}; 

          // dxyerr_scale = (x<=5)*(p_dxy[0]+p_dxy[1]*x+p_dxy[2]*pow(x,2))+(x>5&&x<=10)*(p_dxy[3]+p_dxy[4]*x+p_dxy[5]*pow(x,2))+(x>10&&x<=45)*(p_dxy[6]+p_dxy[7]*x)+(x>45&&x<=200)*(p_dxy[8]+p_dxy[9]*x);
          // dszerr_scale = (x<=5)*(p_dsz[0]+p_dsz[1]*x+p_dsz[2]*pow(x,2))+(x>5&&x<=15)*(p_dsz[3]+p_dsz[4]*x+p_dsz[5]*pow(x,2))+(x>15&&x<=200)*(p_dsz[6]+p_dsz[7]*x);
        
          // //2017 E
          // //lepton
          // const double p_dxy[8] = {1.0131078880048845, 0.016881644273644948, 0.0026536813154402917, 0.9493278264805254, 0.05575099689223152, -0.002745102778758904, 1.22424188270028, 0.00015307624597829593};
          // const double p_dsz[8] = {1.0006397264018454, 0.0010299855043318616, 0.000998070579694292, 1.023785575140348, 0.0027468144983222795, 0.0, 1.0500309207395546, 0.0010914692028304316}; 

          // dxyerr_scale = (x<=5)*(p_dxy[0]+p_dxy[1]*x+p_dxy[2]*pow(x,2))+(x>5&&x<=12)*(p_dxy[3]+p_dxy[4]*x+p_dxy[5]*pow(x,2))+(x>12&&x<=200)*(p_dxy[6]+p_dxy[7]*x);
          // dszerr_scale = (x<=5)*(p_dsz[0]+p_dsz[1]*x+p_dsz[2]*pow(x,2))+(x>5&&x<=15)*(p_dsz[3]+p_dsz[4]*x)+(x>15&&x<=200)*(p_dsz[6]+p_dsz[7]*x);
                
          // //2017 F
          // //lepton
          const double p_dxy[8] = {1.0242311478224801, 0.02002218518358078, 0.0031725460344452835, 0.976662905809667, 0.05847108376325353, -0.0025611401238447747, 1.304497561215741, 0.0007840770479622023};
          const double p_dsz[8] = {1.0385965273089381, 0.021607205529097562, 0.002831404794454864, 1.1244072523508986, 0.02502229771767877, -0.0004540140341128252, 1.3683973708701243, 0.003896809834472007}; 

          dxyerr_scale = (x<=5)*(p_dxy[0]+p_dxy[1]*x+p_dxy[2]*pow(x,2))+(x>5&&x<=11)*(p_dxy[3]+p_dxy[4]*x+p_dxy[5]*pow(x,2))+(x>11&&x<=200)*(p_dxy[6]+p_dxy[7]*x);
          dszerr_scale = (x<=5)*(p_dsz[0]+p_dsz[1]*x+p_dsz[2]*pow(x,2))+(x>5&&x<=19)*(p_dsz[3]+p_dsz[4]*x+p_dsz[5]*pow(x,2))+(x>19&&x<=200)*(p_dsz[6]+p_dsz[7]*x);
        
        }
        // for leptons 
        rescaled_dxyerr *= dxyerr_scale;
        rescaled_dxydszcov *= sqrt(dxyerr_scale);
        rescaled_dszerr *= dszerr_scale;
        rescaled_dxydszcov *= sqrt(dszerr_scale);
      }
      const double nsigmadxy = dxybs / rescaled_dxyerr;


      const bool nm1[5] = {
	      pt > 1,
	      min_r <= 1,
	      npxlayers >= 2,
	      nstlayers >= 6,
	      nsigmadxy > 4
	
      };

      const bool sel = nm1[0] && nm1[1] && nm1[2] && nm1[3];
      const bool seed = sel && nm1[4];
      //const bool goodmu = ntt.isgoodmu(itk) && pt > 20;
      //const bool goodel = ntt.isgoodel(itk) && pt > 20;
      //const bool sel_nolep = sel && !goodmu && !goodel;
						    
      //const bool sel_nomu = sel && !ntt.ismu(itk);
      //const bool sel_noel = sel && !ntt.isel(itk);
      //      const bool tk_ok[max_tk_type] = { true, sel, sel_nolep, sel_nomu, sel_noel, seed };
      const bool tk_ok[max_tk_type] = { true, sel, seed };

      //const bool high_purity = npxlayers == 4 && fabs(ntt.eta(itk)) < 0.8 && fabs(ntt.dz(itk)) < 10;
      //const bool etalt1p5 = fabs(ntt.eta(itk)) < 1.5;

      for (int i = 0; i < max_tk_type; ++i) {
	      if (!tk_ok[i] || !etarange) continue;
        ++ntracks[i];

      // JMTBAD separate plots for dxy, dxybs, dxypv, dz, dzpv
        h_tracks_pt[i]->Fill(pt, w);
        h_tracks_eta[i]->Fill(ntt.eta(itk), w);
        h_tracks_phi[i]->Fill(ntt.phi(itk), w);
        h_tracks_dxy[i]->Fill(dxybs, w);
        //	h_tracks_absdxy[i]->Fill(fabs(dxybs), w);
        h_tracks_dsz[i]->Fill(ntt.dsz(itk), w);
        h_tracks_dz[i]->Fill(ntt.dz(itk), w);

        // h_tracks_dzpv[i]->Fill(ntt.dzpv(itk, nt.pvs()), w);
        // h_tracks_nhits[i]->Fill(ntt.nhits(itk), w);
        // h_tracks_npxhits[i]->Fill(ntt.npxhits(itk), w);
        // h_tracks_nsthits[i]->Fill(ntt.nsthits(itk), w);
        // h_tracks_min_r[i]->Fill(min_r, w);
        // h_tracks_npxlayers[i]->Fill(npxlayers, w);
        // h_tracks_nstlayers[i]->Fill(nstlayers, w);
        //h_tracks_absnsigmadxy[i]->Fill(nsigmadxy, w);
        //h_tracks_nsigmadxy[i]->Fill(dxybs / ntt.err_dxy(itk), w);
        //	h_tracks_nsigmadsz[i]->Fill(ntt.dsz(itk) / ntt.err_dsz(itk), w);

        //h_tracks_dxyerr[i]->Fill(ntt.err_dxy(itk), w);
        //	h_tracks_dxydszcov[i]->Fill(ntt.cov_34(itk), w);
        //	h_tracks_absdxydszcov[i]->Fill(fabs(ntt.cov_34(itk)), w);
        //h_tracks_dzerr[i]->Fill(ntt.err_dz(itk), w);
       // h_tracks_dszerr[i]->Fill(ntt.err_dsz(itk), w);
        //	h_tracks_lambdaerr[i]->Fill(ntt.err_lambda(itk), w);
        //h_tracks_pterr[i]->Fill(ntt.err_pt(itk), w);
        //h_tracks_phierr[i]->Fill(ntt.err_phi(itk), w);
        //h_tracks_etaerr[i]->Fill(ntt.err_eta(itk), w);
        h_tracks_absnsigmadxy[i]->Fill(nsigmadxy, w);
        h_tracks_nsigmadxy[i]->Fill(dxybs / rescaled_dxyerr, w);
        h_tracks_nsigmadsz[i]->Fill(ntt.dsz(itk) / rescaled_dszerr, w);
        
        h_tracks_dxyerr[i]->Fill(rescaled_dxyerr, w);
        h_tracks_dxydszcov[i]->Fill(rescaled_dxydszcov, w);
        h_tracks_absdxydszcov[i]->Fill(fabs(rescaled_dxydszcov), w);
        h_tracks_dzerr[i]->Fill(ntt.err_dz(itk), w);
        h_tracks_dszerr[i]->Fill(rescaled_dszerr, w);
        h_tracks_lambdaerr[i]->Fill(ntt.err_lambda(itk), w);
        h_tracks_pterr[i]->Fill(ntt.err_pt(itk), w);
        h_tracks_phierr[i]->Fill(ntt.err_phi(itk), w);
        h_tracks_etaerr[i]->Fill(ntt.err_eta(itk), w);


        // h_tracks_nstlayers_v_eta[i]->Fill(ntt.eta(itk), nstlayers, w);
        // h_tracks_dxy_v_eta[i]->Fill(ntt.eta(itk), dxybs, w);
        // h_tracks_dxy_v_phi[i]->Fill(ntt.phi(itk), dxybs, w);
        // h_tracks_dxy_v_nstlayers[i]->Fill(nstlayers, dxybs, w);
        // h_tracks_nstlayers_v_phi[i]->Fill(ntt.phi(itk), nstlayers, w);
        // h_tracks_npxlayers_v_phi[i]->Fill(ntt.phi(itk), npxlayers, w);
        // h_tracks_nhits_v_phi[i]->Fill(ntt.phi(itk), ntt.nhits(itk), w);
        // h_tracks_npxhits_v_phi[i]->Fill(ntt.phi(itk), ntt.npxhits(itk), w);
        // h_tracks_nsthits_v_phi[i]->Fill(ntt.phi(itk), ntt.nsthits(itk), w);

        // h_tracks_nsigmadxy_v_eta[i]->Fill(ntt.eta(itk), nsigmadxy, w);
        // h_tracks_nsigmadxy_v_nstlayers[i]->Fill(nstlayers, nsigmadxy, w);
        // h_tracks_nsigmadxy_v_dxy[i]->Fill(dxybs, nsigmadxy, w);
        // h_tracks_nsigmadxy_v_dxyerr[i]->Fill(ntt.err_dxy(itk), nsigmadxy, w);

        //h_tracks_dxyerr_v_pt[i]->Fill(pt, ntt.err_dxy(itk), w);
        //h_tracks_dxyerr_v_eta[i]->Fill(ntt.eta(itk), ntt.err_dxy(itk), w);
        //h_tracks_dxyerr_v_phi[i]->Fill(ntt.phi(itk), ntt.err_dxy(itk), w);
        // h_tracks_dxyerr_v_dxy[i]->Fill(dxybs, ntt.err_dxy(itk), w);
        // h_tracks_dxyerr_v_dzpv[i]->Fill(ntt.dzpv(itk, nt.pvs()), ntt.err_dxy(itk), w);
        // h_tracks_dxyerr_v_npxlayers[i]->Fill(npxlayers, ntt.err_dxy(itk), w);
        // h_tracks_dxyerr_v_nstlayers[i]->Fill(nstlayers, ntt.err_dxy(itk), w);

        //h_tracks_dszerr_v_pt[i]->Fill(pt, ntt.err_dsz(itk), w);
        //h_tracks_dszerr_v_eta[i]->Fill(ntt.eta(itk), ntt.err_dsz(itk), w);
        //h_tracks_dszerr_v_phi[i]->Fill(ntt.phi(itk), ntt.err_dsz(itk), w);
        // h_tracks_dszerr_v_dxy[i]->Fill(dxybs, ntt.err_dsz(itk), w);
        // h_tracks_dszerr_v_dz[i]->Fill(ntt.dz(itk), ntt.err_dsz(itk), w);
        // h_tracks_dszerr_v_npxlayers[i]->Fill(npxlayers, ntt.err_dsz(itk), w);
        // h_tracks_dszerr_v_nstlayers[i]->Fill(nstlayers, ntt.err_dsz(itk), w);

        h_tracks_dxyerr_v_pt[i]->Fill(pt, rescaled_dxyerr, w);
        h_tracks_dxyerr_v_eta[i]->Fill(ntt.eta(itk), rescaled_dxyerr, w);
        h_tracks_dxyerr_v_phi[i]->Fill(ntt.phi(itk), rescaled_dxyerr, w);
        h_tracks_dxyerr_v_minr[i]->Fill(ntt.min_r(itk), rescaled_dxyerr, w);

        h_tracks_dszerr_v_pt[i]->Fill(pt, rescaled_dszerr, w);
        h_tracks_dszerr_v_eta[i]->Fill(ntt.eta(itk), rescaled_dszerr, w);
        h_tracks_dszerr_v_phi[i]->Fill(ntt.phi(itk), rescaled_dszerr, w);
        
        h_tracks_dxydszcov_v_pt[i]->Fill(pt, rescaled_dxydszcov, w);
        h_tracks_dxydszcov_v_eta[i]->Fill(ntt.eta(itk), rescaled_dxydszcov, w);
        h_tracks_dxydszcov_v_phi[i]->Fill(ntt.phi(itk), rescaled_dxydszcov, w);
        h_tracks_absdxydszcov_v_pt[i]->Fill(pt, fabs(rescaled_dxydszcov), w);
        h_tracks_absdxydszcov_v_eta[i]->Fill(ntt.eta(itk), fabs(rescaled_dxydszcov), w);
        h_tracks_absdxydszcov_v_phi[i]->Fill(ntt.phi(itk), fabs(rescaled_dxydszcov), w);

        // h_tracks_lambdaerr_v_pt[i]->Fill(pt, ntt.err_lambda(itk), w);
        // h_tracks_lambdaerr_v_eta[i]->Fill(ntt.eta(itk), ntt.err_lambda(itk), w);
        // h_tracks_lambdaerr_v_phi[i]->Fill(ntt.phi(itk), ntt.err_lambda(itk), w);
        // h_tracks_lambdaerr_v_dxy[i]->Fill(dxybs, ntt.err_lambda(itk), w);
        // h_tracks_lambdaerr_v_dz[i]->Fill(ntt.dz(itk), ntt.err_lambda(itk), w);
        // h_tracks_lambdaerr_v_npxlayers[i]->Fill(npxlayers, ntt.err_lambda(itk), w);
        // h_tracks_lambdaerr_v_nstlayers[i]->Fill(nstlayers, ntt.err_lambda(itk), w);

        h_tracks_eta_v_phi[i]->Fill(ntt.phi(itk), ntt.eta(itk), w);
      }
    }

    for (int i = 0; i < max_tk_type; ++i) {
      h_ntracks[i]->Fill(ntracks[i], w);
    }
    return std::make_pair(true, w);
  };

  nr.loop(fcn);
}
