#include "TH2.h"
#include "JMTucker/MFVNeutralino/interface/Ntuple.h"
#include "JMTucker/Tools/interface/NtupleReader.h"


int main(int argc, char** argv) {
  jmt::NtupleReader<jmt::TrackingAndJetsNtuple> nr;
  // nr.init_options("tt/t", "TrackingTreerHistsV23mv3", "nr_trackingtreerv23mv3", "ttbar=False, all_signal=False");
  //nr.init_options("tt/t", "TrackingTreerULV1_Lepm_cut0_etalt1p5_2017scaled", "trackingtreerulv1_lepm_cut0", "ttbar=False, leptonic=True, all_signal=False, qcd_lep=True, met=True, diboson=True, Lepton_data=False ");
  nr.init_options("tt/t", "TrackingTreerULV1_Lepm_cut0_etalt1p5_2017_wsellep", "trackingtreerulv1_lepm_wsellep", "ttbar=False, leptonic=True, all_signal=False, qcd_lep=False, met=False, diboson=False, Lepton_data=True ");
  if (!nr.parse_options(argc, argv) || !nr.init()) return 1;
  auto& nt = nr.nt();
  auto& ntt = nt.tracks();
  auto& ntm = nt.muons();
  auto& nte = nt.electrons();

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

  // enum { muon, ele, pass_muon, pass_ele };
  enum { muon, ele, pass_muon, pass_ele, nm1_mu, nm1_ele, max_lep_type };
  
  TH1D* h_leptracks_pt[max_lep_type];
  // TH1D* h_leptracks_eta[2];
  // TH1D* h_leptracks_phi[2];
  //TH1D* h_leptracks_dxy[2];
  // TH1D* h_leptracks_absdxy[2];
  // TH1D* h_leptracks_dsz[2];
  // TH1D* h_leptracks_dz[2];
  // TH1D* h_leptracks_nsigmadxy[2];
  // TH1D* h_leptracks_nsigmadsz[2];
  TH1D* h_leptracks_dxyerr[max_lep_type];
  // TH1D* h_leptracks_dxydszcov[2];
  // TH1D* h_leptracks_absdxydszcov[2];
  // TH1D* h_leptracks_dzerr[2];
  TH1D* h_leptracks_dszerr[max_lep_type];
  // TH1D* h_leptracks_pterr[2];
  // TH1D* h_leptracks_phierr[2];
  // TH1D* h_leptracks_etaerr[2];
  TH2D* h_leptracks_dxyerr_v_pt[max_lep_type];
  // TH2D* h_leptracks_dxyerr_v_eta[2];
  // TH2D* h_leptracks_dxyerr_v_phi[2];
  TH2D* h_leptracks_dszerr_v_pt[max_lep_type];
  // TH2D* h_leptracks_dszerr_v_eta[2];
  // TH2D* h_leptracks_dszerr_v_phi[2];


  //make new sel tracks : tk_nolep_sel tk_onlylep_sel
  // enum { tk_all, tk_sel, tk_sel_nolep, tk_sel_nomu, tk_sel_noel, tk_seed, max_tk_type };
  enum { tk_all, tk_sel, tk_seed, max_tk_type };

  TH1D* h_ntracks[max_tk_type];
  TH1D* h_tracks_pt[max_tk_type];
  TH1D* h_tracks_eta[max_tk_type];
  TH1D* h_tracks_phi[max_tk_type];
  TH1D* h_tracks_dxy[max_tk_type];
  TH1D* h_tracks_absdxy[max_tk_type];
  TH1D* h_tracks_dsz[max_tk_type];
  TH1D* h_tracks_dz[max_tk_type];
  // TH1D* h_tracks_dzpv[max_tk_type];
  // TH1D* h_tracks_nhits[max_tk_type];
  // TH1D* h_tracks_npxhits[max_tk_type];
  // TH1D* h_tracks_nsthits[max_tk_type];
  // TH1D* h_tracks_min_r[max_tk_type];
  // TH1D* h_tracks_npxlayers[max_tk_type];
  // TH1D* h_tracks_nstlayers[max_tk_type];
  //TH1D* h_tracks_absnsigmadxy[max_tk_type];
  TH1D* h_tracks_nsigmadxy[max_tk_type];
  TH1D* h_tracks_nsigmadsz[max_tk_type];

  TH1D* h_tracks_dxyerr[max_tk_type];
  TH1D* h_tracks_dxydszcov[max_tk_type];
  TH1D* h_tracks_absdxydszcov[max_tk_type];
  TH1D* h_tracks_dzerr[max_tk_type];
  TH1D* h_tracks_dszerr[max_tk_type];
  //TH1D* h_tracks_lambdaerr[max_tk_type];
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

  // TH2D* h_tracks_lambdaerr_v_pt[max_tk_type];
  // TH2D* h_tracks_lambdaerr_v_eta[max_tk_type];
  // TH2D* h_tracks_lambdaerr_v_phi[max_tk_type];
  // TH2D* h_tracks_lambdaerr_v_dxy[max_tk_type];
  // TH2D* h_tracks_lambdaerr_v_dz[max_tk_type];
  // TH2D* h_tracks_lambdaerr_v_npxlayers[max_tk_type];
  // TH2D* h_tracks_lambdaerr_v_nstlayers[max_tk_type];

  TH2D* h_tracks_eta_v_phi[max_tk_type];
  
  // enum { B, C, D, E, F, max_era };
  
  // TH1D* h_era_tracks_absnsigmadxy[max_era];
  // TH1D* h_era_tracks_nsigmadxy[max_era];
  // TH1D* h_era_tracks_nsigmadsz[max_era];
  // TH1D* h_era_tracks_dxyerr[max_era];
  // TH1D* h_era_tracks_dxydszcov[max_era];
  // TH1D* h_era_tracks_absdxydszcov[max_era];
  // TH1D* h_era_tracks_dszerr[max_era];
  // TH2D* h_era_tracks_dxyerr_v_pt[max_era];
  // TH2D* h_era_tracks_dxyerr_v_eta[max_era];
  // TH2D* h_era_tracks_dxyerr_v_phi[max_era];
  // TH2D* h_era_tracks_dszerr_v_pt[max_era];
  // TH2D* h_era_tracks_dszerr_v_eta[max_era];
  // TH2D* h_era_tracks_dszerr_v_phi[max_era];
  
  //const char* ex[max_tk_type] = {"all", "sel", "sel_nolep", "sel_nomu", "sel_noel", "seed"};
  const char* ex[max_tk_type] = {"all", "sel", "seed"};
  for (int i = 0; i < max_tk_type; ++i) {
    h_ntracks[i] = new TH1D(TString::Format("h_%s_ntracks", ex[i]), TString::Format(";number of %s tracks;events", ex[i]), 2000, 0, 2000);
    h_tracks_pt[i] = new TH1D(TString::Format("h_%s_tracks_pt", ex[i]), TString::Format("%s tracks;tracks pt (GeV);arb. units", ex[i]), 2000, 0, 200);
    h_tracks_eta[i] = new TH1D(TString::Format("h_%s_tracks_eta", ex[i]), TString::Format("%s tracks;tracks eta;arb. units", ex[i]), 50, -4, 4);
    h_tracks_phi[i] = new TH1D(TString::Format("h_%s_tracks_phi", ex[i]), TString::Format("%s tracks;tracks phi;arb. units", ex[i]), 315, -3.15, 3.15);
    h_tracks_dxy[i] = new TH1D(TString::Format("h_%s_tracks_dxy", ex[i]), TString::Format("%s tracks;tracks dxy to beamspot (cm);arb. units", ex[i]), 400, -0.2, 0.2);
    h_tracks_absdxy[i] = new TH1D(TString::Format("h_%s_tracks_absdxy", ex[i]), TString::Format("%s tracks;tracks |dxy| to beamspot (cm);arb. units", ex[i]), 200, 0, 0.2);
    h_tracks_dsz[i] = new TH1D(TString::Format("h_%s_tracks_dsz", ex[i]), TString::Format("%s tracks;tracks dsz (cm);arb. units", ex[i]), 400, -20, 20);
    h_tracks_dz[i] = new TH1D(TString::Format("h_%s_tracks_dz", ex[i]), TString::Format("%s tracks;tracks dz (cm);arb. units", ex[i]), 400, -20, 20);
    // h_tracks_dzpv[i] = new TH1D(TString::Format("h_%s_tracks_dzpv", ex[i]), TString::Format("%s tracks;tracks dz to PV (cm);arb. units", ex[i]), 400, -20, 20);
    // h_tracks_nhits[i] = new TH1D(TString::Format("h_%s_tracks_nhits", ex[i]), TString::Format("%s tracks;tracks nhits;arb. units", ex[i]), 40, 0, 40);
    // h_tracks_npxhits[i] = new TH1D(TString::Format("h_%s_tracks_npxhits", ex[i]), TString::Format("%s tracks;tracks npxhits;arb. units", ex[i]), 40, 0, 40);
    // h_tracks_nsthits[i] = new TH1D(TString::Format("h_%s_tracks_nsthits", ex[i]), TString::Format("%s tracks;tracks nsthits;arb. units", ex[i]), 40, 0, 40);

    // h_tracks_min_r[i] = new TH1D(TString::Format("h_%s_tracks_min_r", ex[i]), TString::Format("%s tracks;tracks min_r;arb. units", ex[i]), 20, 0, 20);
    // h_tracks_npxlayers[i] = new TH1D(TString::Format("h_%s_tracks_npxlayers", ex[i]), TString::Format("%s tracks;tracks npxlayers;arb. units", ex[i]), 20, 0, 20);
    // h_tracks_nstlayers[i] = new TH1D(TString::Format("h_%s_tracks_nstlayers", ex[i]), TString::Format("%s tracks;tracks nstlayers;arb. units", ex[i]), 20, 0, 20);
    //h_tracks_absnsigmadxy[i] = new TH1D(TString::Format("h_%s_tracks_absnsigmadxy", ex[i]), TString::Format("%s tracks;tracks abs nsigmadxy;arb. units", ex[i]), 400, 0, 40);
    h_tracks_nsigmadxy[i] = new TH1D(TString::Format("h_%s_tracks_nsigmadxy", ex[i]), TString::Format("%s tracks;tracks nsigmadxy;arb. units", ex[i]), 2000, -20, 20);
    h_tracks_nsigmadsz[i] = new TH1D(TString::Format("h_%s_tracks_nsigmadsz", ex[i]), TString::Format("%s tracks;tracks nsigmadsz;arb. units", ex[i]), 2000, -20, 20);
    
    h_tracks_dxyerr[i] = new TH1D(TString::Format("h_%s_tracks_dxyerr", ex[i]), TString::Format("%s tracks;tracks dxyerr;arb. units", ex[i]), 2000, 0, 0.2);
    h_tracks_dxydszcov[i] = new TH1D(TString::Format("h_%s_tracks_dxydszcov", ex[i]), TString::Format("%s tracks;tracks dxy-dsz covariance;arb. units", ex[i]), 2000, -0.00002, 0.00002);
    h_tracks_absdxydszcov[i] = new TH1D(TString::Format("h_%s_tracks_absdxydszcov", ex[i]), TString::Format("%s tracks;tracks dxy-dsz covariance;arb. units", ex[i]), 2000, 0, 0.00002);
    h_tracks_dzerr[i] = new TH1D(TString::Format("h_%s_tracks_dzerr", ex[i]), TString::Format("%s tracks;tracks dzerr;arb. units", ex[i]), 2000, 0, 0.2);
    h_tracks_dszerr[i] = new TH1D(TString::Format("h_%s_tracks_dszerr", ex[i]), TString::Format("%s tracks;tracks dszerr;arb. units", ex[i]), 2000, 0, 0.2);
    //  h_tracks_lambdaerr[i] = new TH1D(TString::Format("h_%s_tracks_lambdaerr", ex[i]), TString::Format("%s tracks;tracks lambdaerr;arb. units", ex[i]), 2000, 0, 0.2);
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

    // h_tracks_lambdaerr_v_pt[i] = new TH2D(TString::Format("h_%s_tracks_lambdaerr_v_pt", ex[i]), TString::Format("%s tracks;tracks pt;tracks lambdaerr", ex[i]), 2000, 0, 200, 2000, 0, 0.2);
    // h_tracks_lambdaerr_v_eta[i] = new TH2D(TString::Format("h_%s_tracks_lambdaerr_v_eta", ex[i]), TString::Format("%s tracks;tracks eta;tracks lambdaerr", ex[i]), 80, -4, 4, 2000, 0, 0.2);
    // h_tracks_lambdaerr_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_lambdaerr_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks lambdaerr", ex[i]), 126, -3.15, 3.15, 200, 0, 0.2);
    // h_tracks_lambdaerr_v_dxy[i] = new TH2D(TString::Format("h_%s_tracks_lambdaerr_v_dxy", ex[i]), TString::Format("%s tracks;tracks dxy to beamspot;tracks lambdaerr", ex[i]), 400, -0.2, 0.2, 200, 0, 0.2);
    // h_tracks_lambdaerr_v_dz[i] = new TH2D(TString::Format("h_%s_tracks_lambdaerr_v_dz", ex[i]), TString::Format("%s tracks;tracks dz to beamspot;tracks lambdaerr", ex[i]), 400, -20, 20, 200, 0, 0.2);
    // h_tracks_lambdaerr_v_npxlayers[i] = new TH2D(TString::Format("h_%s_tracks_lambdaerr_v_npxlayers", ex[i]), TString::Format("%s tracks;tracks npxlayers;tracks lambdaerr", ex[i]), 10, 0, 10, 200, 0, 0.2);
    // h_tracks_lambdaerr_v_nstlayers[i] = new TH2D(TString::Format("h_%s_tracks_lambdaerr_v_nstlayers", ex[i]), TString::Format("%s tracks;tracks nstlayers;tracks lambdaerr", ex[i]), 20, 0, 20, 200, 0, 0.2);

    h_tracks_eta_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_eta_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks eta", ex[i]), 126, -3.15, 3.15, 80, -4, 4);
  }

  //this is only for selected tracks
  // const char* eex[max_era] = {"B", "C", "D", "E", "F"};
  // for (int i = 0; i < max_era; ++i) {

  //   h_era_tracks_absnsigmadxy[i] = new TH1D(TString::Format("h_%s_tracks_absnsigmadxy", eex[i]), TString::Format("%s tracks;tracks abs nsigmadxy;arb. units", eex[i]), 400, 0, 40);
  //   h_era_tracks_nsigmadxy[i] = new TH1D(TString::Format("h_%s_tracks_nsigmadxy", eex[i]), TString::Format("%s tracks;tracks nsigmadxy;arb. units", eex[i]), 2000, -20, 20);
  //   h_era_tracks_nsigmadsz[i] = new TH1D(TString::Format("h_%s_tracks_nsigmadsz", eex[i]), TString::Format("%s tracks;tracks nsigmadsz;arb. units", eex[i]), 2000, -20, 20);
  //   h_era_tracks_dxyerr[i] = new TH1D(TString::Format("h_%s_tracks_dxyerr", eex[i]), TString::Format("%s tracks;tracks dxyerr;arb. units", eex[i]), 2000, 0, 0.2);
  //   h_era_tracks_dxydszcov[i] = new TH1D(TString::Format("h_%s_tracks_dxydszcov", eex[i]), TString::Format("%s tracks;tracks dxy-dsz covariance;arb. units", eex[i]), 2000, -0.00002, 0.00002);
  //   h_era_tracks_absdxydszcov[i] = new TH1D(TString::Format("h_%s_tracks_absdxydszcov", eex[i]), TString::Format("%s tracks;tracks dxy-dsz covariance;arb. units", eex[i]), 2000, 0, 0.00002);
  //   h_era_tracks_dszerr[i] = new TH1D(TString::Format("h_%s_tracks_dszerr", eex[i]), TString::Format("%s tracks;tracks dszerr;arb. units", eex[i]), 2000, 0, 0.2);
  //   h_era_tracks_dxyerr_v_pt[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_pt", eex[i]), TString::Format("%s tracks;tracks pt;tracks dxyerr", eex[i]), 2000, 0, 200, 2000, 0, 0.2);
  //   h_era_tracks_dxyerr_v_eta[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_eta", eex[i]), TString::Format("%s tracks;tracks eta;tracks dxyerr", eex[i]), 80, -4, 4, 2000, 0, 0.2);
  //   h_era_tracks_dxyerr_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_phi", eex[i]), TString::Format("%s tracks;tracks phi;tracks dxyerr", eex[i]), 126, -3.15, 3.15, 200, 0, 0.2);
  //   h_era_tracks_dszerr_v_pt[i] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_pt", eex[i]), TString::Format("%s tracks;tracks pt;tracks dszerr", eex[i]), 2000, 0, 200, 2000, 0, 0.2);
  //   h_era_tracks_dszerr_v_eta[i] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_eta", eex[i]), TString::Format("%s tracks;tracks eta;tracks dszerr", eex[i]), 80, -4, 4, 2000, 0, 0.2);
  //   h_era_tracks_dszerr_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_phi", eex[i]), TString::Format("%s tracks;tracks phi;tracks dszerr", eex[i]), 126, -3.15, 3.15, 200, 0, 0.2);
  // }

  const char* lepex[max_lep_type] = {"muon", "electron", "pass_muon", "pass_ele", "nm1pt_mu", "nm1pt_ele"};
  for (int j = 0; j < max_lep_type; ++j) {
  // const char* lepex[2] = {"muon", "electron"};
  // for (int j = 0; j < 2; ++j) {
    h_leptracks_pt[j] = new TH1D(TString::Format("h_%s_tracks_pt", lepex[j]), TString::Format("%s tracks;tracks pt (GeV);arb. units", lepex[j]), 2000, 0, 200);
    // h_leptracks_eta[j] = new TH1D(TString::Format("h_%s_tracks_eta", ex[j]), TString::Format("%s tracks;tracks eta;arb. units", ex[j]), 50, -4, 4);
    // h_leptracks_phi[j] = new TH1D(TString::Format("h_%s_tracks_phi", ex[j]), TString::Format("%s tracks;tracks phi;arb. units", ex[j]), 315, -3.15, 3.15);
    // h_leptracks_dxy[j] = new TH1D(TString::Format("h_%s_tracks_dxy", ex[j]), TString::Format("%s tracks;tracks dxy to beamspot (cm);arb. units", ex[j]), 400, -0.2, 0.2);
    // h_leptracks_absdxy[j] = new TH1D(TString::Format("h_%s_tracks_absdxy", ex[j]), TString::Format("%s tracks;tracks |dxy| to beamspot (cm);arb. units", ex[j]), 200, 0, 0.2);
    // h_leptracks_dsz[j] = new TH1D(TString::Format("h_%s_tracks_dsz", ex[j]), TString::Format("%s tracks;tracks dsz (cm);arb. units", ex[j]), 400, -20, 20);
    // h_leptracks_dz[j] = new TH1D(TString::Format("h_%s_tracks_dz", ex[j]), TString::Format("%s tracks;tracks dz (cm);arb. units", ex[j]), 400, -20, 20);
    // h_leptracks_nsigmadxy[j] = new TH1D(TString::Format("h_%s_tracks_nsigmadxy", ex[j]), TString::Format("%s tracks;tracks nsigmadxy;arb. units", ex[j]), 2000, -20, 20);
    // h_leptracks_nsigmadsz[j] = new TH1D(TString::Format("h_%s_tracks_nsigmadsz", ex[j]), TString::Format("%s tracks;tracks nsigmadsz;arb. units", ex[j]), 2000, -20, 20);
    h_leptracks_dxyerr[j] = new TH1D(TString::Format("h_%s_tracks_dxyerr", lepex[j]), TString::Format("%s tracks;tracks dxyerr;arb. units", lepex[j]), 2000, 0, 0.2);
    // h_leptracks_dxydszcov[j] = new TH1D(TString::Format("h_%s_tracks_dxydszcov", ex[j]), TString::Format("%s tracks;tracks dxy-dsz covariance;arb. units", ex[j]), 2000, -0.00002, 0.00002);
    // h_leptracks_absdxydszcov[j] = new TH1D(TString::Format("h_%s_tracks_absdxydszcov", ex[j]), TString::Format("%s tracks;tracks dxy-dsz covariance;arb. units", ex[j]), 2000, 0, 0.00002);
    // h_leptracks_dzerr[j] = new TH1D(TString::Format("h_%s_tracks_dzerr", ex[j]), TString::Format("%s tracks;tracks dzerr;arb. units", ex[j]), 2000, 0, 0.2);
    h_leptracks_dszerr[j] = new TH1D(TString::Format("h_%s_tracks_dszerr", lepex[j]), TString::Format("%s tracks;tracks dszerr;arb. units", lepex[j]), 2000, 0, 0.2);
    // h_leptracks_pterr[j] = new TH1D(TString::Format("h_%s_tracks_pterr", ex[j]), TString::Format("%s tracks;tracks pterr;arb. units", ex[j]), 200, 0, 0.2);
    // h_leptracks_phierr[j] = new TH1D(TString::Format("h_%s_tracks_phierr", ex[j]), TString::Format("%s tracks;tracks phierr;arb. units", ex[j]), 200, 0, 0.2);
    // h_leptracks_etaerr[j] = new TH1D(TString::Format("h_%s_tracks_etaerr", ex[j]), TString::Format("%s tracks;tracks etaerr;arb. units", ex[j]), 200, 0, 0.2);
    h_leptracks_dxyerr_v_pt[j] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_pt", lepex[j]), TString::Format("%s tracks;tracks pt;tracks dxyerr", lepex[j]), 2000, 0, 200, 2000, 0, 0.2);
    // h_leptracks_dxyerr_v_eta[j] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_eta", ex[j]), TString::Format("%s tracks;tracks eta;tracks dxyerr", ex[j]), 80, -4, 4, 2000, 0, 0.2);
    // h_leptracks_dxyerr_v_phi[j] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_phi", ex[j]), TString::Format("%s tracks;tracks phi;tracks dxyerr", ex[j]), 126, -3.15, 3.15, 200, 0, 0.2);
    h_leptracks_dszerr_v_pt[j] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_pt", lepex[j]), TString::Format("%s tracks;tracks pt;tracks dszerr", lepex[j]), 2000, 0, 200, 2000, 0, 0.2);
    // h_leptracks_dszerr_v_eta[j] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_eta", ex[j]), TString::Format("%s tracks;tracks eta;tracks dszerr", ex[j]), 80, -4, 4, 2000, 0, 0.2);
    // h_leptracks_dszerr_v_phi[j] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_phi", ex[j]), TString::Format("%s tracks;tracks phi;tracks dszerr", ex[j]), 126, -3.15, 3.15, 200, 0, 0.2);
    // h_leptracks_eta_v_phi[j] = new TH2D(TString::Format("h_%s_tracks_eta_v_phi", ex[j]), TString::Format("%s tracks;tracks phi;tracks eta", ex[j]), 126, -3.15, 3.15, 80, -4, 4);
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

    // at the very least, we must create the dxyerr vs pt plot 
    for (int ie = 0, iee = nte.n(); ie < iee; ++ie) {
      const double pt = nte.pt(ie);
      const int min_r = nte.min_r(ie);
      const int npxlayers = nte.npxlayers(ie);
      const int nstlayers = nte.nstlayers(ie);
      //const double dxybs = nte.dxybs(ie, nt.bs());
      //const double nsigmadxy = nte.nsigmadxybs(ie, nt.bs());

      const bool eef[5] = {
      			   pt > 38,
      			   nte.eta(ie) < 2.4,
      			   nte.iso(ie) < 0.10,
      			   nte.passveto(ie),
      			   nte.isTight(ie)
			   
      };
      
      const bool pass_ele = eef[0] && eef[1] && eef[2] && eef[3] && eef[4];
      const bool pass_nm1ef = eef[1] && eef[2] && eef[3] && eef[4];
      
      const bool etagt1p5 = false;
      bool etarange =false;
      if (etagt1p5)
        etarange = fabs(nte.eta(ie)) > 1.5;
      else
        etarange = fabs(nte.eta(ie)) < 1.5;
      
      if (pt > 1 && etarange && min_r <=1 && npxlayers >=2 && nstlayers >=6) {
      	h_leptracks_pt[1]->Fill(pt, w);
	h_leptracks_dxyerr[1]->Fill(nte.err_dxy(ie), w);
	h_leptracks_dszerr[1]->Fill(nte.err_dsz(ie), w);
	h_leptracks_dszerr_v_pt[1]->Fill(pt, ntt.err_dsz(ie), w);
	h_leptracks_dxyerr_v_pt[1]->Fill(pt, ntt.err_dxy(ie), w);

	if (pass_ele) {
      	  h_leptracks_pt[3]->Fill(pt, w);
      	  h_leptracks_dxyerr[3]->Fill(nte.err_dxy(ie), w);
      	  h_leptracks_dszerr[3]->Fill(nte.err_dsz(ie), w);
      	  h_leptracks_dszerr_v_pt[3]->Fill(pt, ntt.err_dsz(ie), w);
      	  h_leptracks_dxyerr_v_pt[3]->Fill(pt, ntt.err_dxy(ie), w);
	}
	if (pass_nm1ef) {
      	  h_leptracks_pt[5]->Fill(pt, w);
      	  h_leptracks_dxyerr[5]->Fill(nte.err_dxy(ie), w);
      	  h_leptracks_dszerr[5]->Fill(nte.err_dsz(ie), w);
      	  h_leptracks_dszerr_v_pt[5]->Fill(pt, ntt.err_dsz(ie), w);
      	  h_leptracks_dxyerr_v_pt[5]->Fill(pt, ntt.err_dxy(ie), w);
	}
      }
    }

    for (int im = 0, ime = ntm.n(); im < ime; ++im) {
      const double pt = ntm.pt(im);
      const int min_r = ntm.min_r(im);
      const int npxlayers = ntm.npxlayers(im);
      const int nstlayers = ntm.nstlayers(im);
      // const double dxybs = ntm.dxybs(im, nt.bs());
      //const double nsigmadxy = ntm.nsigmadxybs(im, nt.bs());
      
      const bool mef[4] = {
      			   pt > 29,
      			   ntm.eta(im) < 2.4,
      			   ntm.iso(im) < 0.15,
      			   ntm.isMed(im)
			   
      };
      
      const bool pass_mu = mef[0] && mef[1] && mef[2] && mef[3];
      const bool pass_nm1mf = mef[1] && mef[2] && mef[3];

      const bool etagt1p5 = false;
      bool etarange =false;
      if (etagt1p5)
        etarange = fabs(ntm.eta(im)) > 1.5;
      else
        etarange = fabs(ntm.eta(im)) < 1.5;
      
      if (pt > 1 && etarange && min_r <=1 && npxlayers >=2 && nstlayers >=6) {
	h_leptracks_pt[0]->Fill(pt, w);
	h_leptracks_dxyerr[0]->Fill(ntm.err_dxy(im), w);
	h_leptracks_dszerr[0]->Fill(ntm.err_dsz(im), w);
	h_leptracks_dszerr_v_pt[0]->Fill(pt, ntm.err_dsz(im), w);
	h_leptracks_dxyerr_v_pt[0]->Fill(pt, ntm.err_dxy(im), w);

	if (pass_mu) {
	  h_leptracks_pt[2]->Fill(pt, w);
	  h_leptracks_dxyerr[2]->Fill(ntm.err_dxy(im), w);
	  h_leptracks_dszerr[2]->Fill(ntm.err_dsz(im), w);
	  h_leptracks_dszerr_v_pt[2]->Fill(pt, ntm.err_dsz(im), w);
	  h_leptracks_dxyerr_v_pt[2]->Fill(pt, ntm.err_dxy(im), w);
	}
	if (pass_nm1mf) {
	  h_leptracks_pt[4]->Fill(pt, w);
	  h_leptracks_dxyerr[4]->Fill(ntm.err_dxy(im), w);
	  h_leptracks_dszerr[4]->Fill(ntm.err_dsz(im), w);
	  h_leptracks_dszerr_v_pt[4]->Fill(pt, ntm.err_dsz(im), w);
	  h_leptracks_dxyerr_v_pt[4]->Fill(pt, ntm.err_dxy(im), w);
	}
      }
    }
    
    for (int itk = 0, itke = ntt.n(); itk < itke; ++itk) {
      const double pt = ntt.pt(itk);
      const int min_r = ntt.min_r(itk);
      const int npxlayers = ntt.npxlayers(itk);
      const int nstlayers = ntt.nstlayers(itk);
      const double dxybs = ntt.dxybs(itk, nt.bs());
      const double nsigmadxy = ntt.nsigmadxybs(itk, nt.bs());

      //const bool high_purity = npxlayers == 4 && fabs(ntt.eta(itk)) < 0.8 && fabs(ntt.dz(itk)) < 10;
      const bool etagt1p5 = false;
      bool etarange =false;
      if (etagt1p5)
        etarange = fabs(ntt.eta(itk)) > 1.5;
      else
        etarange = fabs(ntt.eta(itk)) < 1.5;
      //const bool etagt1p5 = fabs(ntt.eta(itk)) > 1.5;
      //const bool etalt1p5 = fabs(ntt.eta(itk)) < 1.5;

      std::vector<double> dxyerr_scale(5, 1.);
      std::vector<double> dszerr_scale(5, 1.);

      
      std::vector<double> rescaled_dxyerr(5, ntt.err_dxy(itk));
      std::vector<double> rescaled_dszerr(5, ntt.err_dsz(itk));
      std::vector<double> rescaled_dxydszcov(5, ntt.cov_34(itk));
      //std::vector<double> nsigmadxy(5, 1.);
      
      // for (int j = 0; j < max_era; ++j) {
	  
      // 	double dxyerr_scale[j] = 1.;
      // 	double dszerr_scale[j] = 1.;

      // 	double rescaled_dxyerr[j] = ntt.err_dxy(itk);
      // 	double rescaled_dszerr[j] = ntt.err_dsz(itk);
      // 	double rescaled_dxydszcov[j] = ntt.cov_34(itk);
      // }
      
      const bool rescale_tracks = false;
      if (rescale_tracks) {
	
        if (fabs(ntt.eta(itk)) < 1.5) {
          const double x = pt;

	  //2017 B
	  const double pb_dxy[7] = {0.957546103651918, 0.10115878425485272, -0.011415063464127082, 1.1934581803990052, 0.0012915340460863236, 1.185865599289828, 0.000607061956079625};
	  const double pb_dsz[7] = {1.0357759074456505, 0.11094532031998264, -0.01757285947949813, 1.2149304609505513, -0.001958128601506479, 1.1698461729720642, -0.000196959171373087};

	  dxyerr_scale[0] = (x<=5)*(pb_dxy[0]+pb_dxy[1]*x+pb_dxy[2]*pow(x,2))+(x>5&&x<=30)*(pb_dxy[3]+pb_dxy[4]*x)+(x>30&&x<=200)*(pb_dxy[5]+pb_dxy[6]*x);
	  dszerr_scale[0] = (x<=4)*(pb_dsz[0]+pb_dsz[1]*x+pb_dsz[2]*pow(x,2))+(x>4&&x<=20)*(pb_dsz[3]+pb_dsz[4]*x)+(x>20&&x<=200)*(pb_dsz[5]+pb_dsz[6]*x);
	  
	  //2017 C
	  const double pc_dxy[9] = {0.949676160349007, 0.13006314908140257, -0.015545193778351262, 1.2307660528799549, 0.0007043590265264279, 1.1974355098321214, 0.001303434548335857, 1.2845380934953352, -4.1194985043423856e-05};
	  const double pc_dsz[7] = {1.0883367053628183, 0.13580757264364524, -0.02146022561478638, 1.3039228956514926, -0.0010821273053523515, 1.2828707957617664, -0.00023290743618047344};

	  dxyerr_scale[1] = (x<=5)*(pc_dxy[0]+pc_dxy[1]*x+pc_dxy[2]*pow(x,2))+(x>5&&x<=30)*(pc_dxy[3]+pc_dxy[4]*x)+(x>30&&x<=80)*(pc_dxy[5]+pc_dxy[6]*x)+(x>80&&x<=200)*(pc_dxy[7]+pc_dxy[8]*x);
	  dszerr_scale[1] = (x<=4)*(pc_dsz[0]+pc_dsz[1]*x+pc_dsz[2]*pow(x,2))+(x>4&&x<=15)*(pc_dsz[3]+pc_dsz[4]*x)+(x>15&&x<=200)*(pc_dsz[5]+pc_dsz[6]*x);
	  
	  //2017 D
	  const double pd_dxy[9] = {0.9577719736881636, 0.1012729478986804, -0.011645689941694258, 1.191456590220749, 0.0002789772758379746, 1.168832789258199, 0.00051441822997604, 1.2053682671761432, -2.8139149141985162e-05};
	  const double pd_dsz[7] = {1.0203375909717907, 0.10445499613314517, -0.014942701685989336, 1.1986997604058922, 0.0025980812171631958, 1.2303173640430805, -0.00017485187473597667};

	  dxyerr_scale[2] = (x<=5)*(pd_dxy[0]+pd_dxy[1]*x+pd_dxy[2]*pow(x,2))+(x>5&&x<=30)*(pd_dxy[3]+pd_dxy[4]*x)+(x>30&&x<=90)*(pd_dxy[5]+pd_dxy[6]*x)+(x>90&&x<=200)*(pd_dxy[7]+pd_dxy[8]*x);
	  dszerr_scale[2] = (x<=4)*(pd_dsz[0]+pd_dsz[1]*x+pd_dsz[2]*pow(x,2))+(x>4&&x<=15)*(pd_dsz[3]+pd_dsz[4]*x)+(x>15&&x<=200)*(pd_dsz[5]+pd_dsz[6]*x);
	  
	  //2017 E
	  const double pe_dxy[9] = {0.9609066946505194, 0.07663369798178354, -0.009422264919897885, 1.1246768990561118, -0.0002987520720562679, 1.0583032806360884, 0.0010200888371873482, 1.1226200924748864, 0.0001835054219603248};
	  const double pe_dsz[7] = {0.9990802669750953, 0.06518129275719037, -0.009627937529330442, 1.1085401855037689, 0.0006640497021907683, 1.1091645815160394, -0.00014297752964789441};

	  dxyerr_scale[3] = (x<=5)*(pe_dxy[0]+pe_dxy[1]*x+pe_dxy[2]*pow(x,2))+(x>5&&x<=30)*(pe_dxy[3]+pe_dxy[4]*x)+(x>30&&x<=90)*(pe_dxy[5]+pe_dxy[6]*x)+(x>90&&x<=200)*(pe_dxy[7]+pe_dxy[8]*x);
	  dszerr_scale[3] = (x<=4)*(pe_dsz[0]+pe_dsz[1]*x+pe_dsz[2]*pow(x,2))+(x>4&&x<=15)*(pe_dsz[3]+pe_dsz[4]*x)+(x>15&&x<=200)*(pe_dsz[5]+pe_dsz[6]*x);
	  
	  //2017 F
	  const double pf_dxy[9] = {0.9690582612477836, 0.09955409099034848, -0.012049508044364693, 1.1856663695362375, 0.0005866641676978286, 1.127022409099426, 0.0009620529197614539, 1.1618427996565703, 0.0004971487441196317};
	  const double pf_dsz[7] = {1.0050229806632387, 0.07904914957873413, -0.01142767161059791, 1.1374380527723271, 0.0022223102094448134, 1.1615536560491244, 6.860278421417444e-06};
	  
	  dxyerr_scale[4] = (x<=5)*(pf_dxy[0]+pf_dxy[1]*x+pf_dxy[2]*pow(x,2))+(x>5&&x<=30)*(pf_dxy[3]+pf_dxy[4]*x)+(x>30&&x<=90)*(pf_dxy[5]+pf_dxy[6]*x)+(x>90&&x<=200)*(pf_dxy[7]+pf_dxy[8]*x);
	  dszerr_scale[4] = (x<=4)*(pf_dsz[0]+pf_dsz[1]*x+pf_dsz[2]*pow(x,2))+(x>4&&x<=15)*(pf_dsz[3]+pf_dsz[4]*x)+(x>15&&x<=200)*(pf_dsz[5]+pf_dsz[6]*x);
	  
      	}
      	else {
      	  const double x = pt;

	  
	  //2017 B
	  const double pb_dxy[8] = {0.9588820714692646, 0.061982058366554654, 1.1162960765884076, 0.021041745021068897, 1.2889698501830753, -0.001425344425817686, 1.1405582300661157, -0.00020372129500620135};
	  const double pb_dsz[8] = {0.980245295260894, 0.029988240038579007, -0.0015257397418379712, 1.0515459828015872, 0.010146274556091055, -0.00032769698400819555, 1.1062508695433444, 2.5782684526297375e-05};

	  dxyerr_scale[0] = (x<=4)*(pb_dxy[0]+pb_dxy[1]*x)+(x>4&&x<=8)*(pb_dxy[2]+pb_dxy[3]*x)+(x>8&&x<=35)*(pb_dxy[4]+pb_dxy[5]*x)+(x>35&&x<=200)*(pb_dxy[6]+pb_dxy[7]*x);
	  dszerr_scale[0] = (x<=5)*(pb_dsz[0]+pb_dsz[1]*x+pb_dsz[2]*pow(x,2))+(x>5&&x<=20)*(pb_dsz[3]+pb_dsz[4]*x+pb_dsz[5]*pow(x,2))+(x>20&&x<=200)*(pb_dsz[6]+pb_dsz[7]*x);
	  
	  //2017 C
	  const double pc_dxy[8] = {0.9501917257978219, 0.0772696113851621, 1.1619170077121224, 0.020847624349959647, 1.313087954945408, 0.00029437856768493647, 1.2578412122477818, -0.00032702675277679707};
	  const double pc_dsz[8] = {0.940905897160002, 0.08583498729021975, -0.006478303914057582, 1.133017936366856, 0.0193398044794409, -0.0005942927263893404, 1.2809198711252718, 0.00026104650679676544};

	  dxyerr_scale[1] = (x<=4)*(pc_dxy[0]+pc_dxy[1]*x)+(x>4&&x<=8)*(pc_dxy[2]+pc_dxy[3]*x)+(x>8&&x<=40)*(pc_dxy[4]+pc_dxy[5]*x)+(x>40&&x<=200)*(pc_dxy[6]+pc_dxy[7]*x);
	  dszerr_scale[1] = (x<=5)*(pc_dsz[0]+pc_dsz[1]*x+pc_dsz[2]*pow(x,2))+(x>5&&x<=21)*(pc_dsz[3]+pc_dsz[4]*x+pc_dsz[5]*pow(x,2))+(x>21&&x<=200)*(pc_dsz[6]+pc_dsz[7]*x);
	  
	  //2017 D
	  const double pd_dxy[8] = {0.9580879554830931, 0.062299229775116774, 1.1259869242568172, 0.018177261592246995, 1.2549486089179482, 0.0006126257142669289, 1.2125648270839353, -0.00045873051921530884};
	  const double pd_dsz[8] = {0.974001785855261, 0.03487080218767103, -0.001860419720174829, 1.0487411366278545, 0.012928918333158035, -0.0003829906150617834, 1.1738461500391797, -0.00010567461379826843};

	  dxyerr_scale[2] = (x<=4)*(pd_dxy[0]+pd_dxy[1]*x)+(x>4&&x<=8)*(pd_dxy[2]+pd_dxy[3]*x)+(x>8&&x<=40)*(pd_dxy[4]+pd_dxy[5]*x)+(x>40&&x<=200)*(pd_dxy[6]+pd_dxy[7]*x);
	  dszerr_scale[2] = (x<=5)*(pd_dsz[0]+pd_dsz[1]*x+pd_dsz[2]*pow(x,2))+(x>5&&x<=18)*(pd_dsz[3]+pd_dsz[4]*x+pd_dsz[5]*pow(x,2))+(x>18&&x<=200)*(pd_dsz[6]+pd_dsz[7]*x);
	  
	  //2017 E
	  const double pe_dxy[8] = {0.961763549000799, 0.04729252429670964, 1.0687039873406823, 0.0198106914340693, 1.2375222489011366, -0.0007098052119063909, 1.1231195453325953, 0.0002227216425638378};
	  const double pe_dsz[10] = {0.9892972282625031, 0.008892894952452693, 1.596342754638314e-06, 1.0116851606420791, 0.0050550104751535966, -9.610032864576431e-05, 1.053730943982757, -5.374955151630109e-06, 1.0163239503986545, 0.0005379551847026874};

	  dxyerr_scale[3] = (x<=4)*(pe_dxy[0]+pe_dxy[1]*x)+(x>4&&x<=8)*(pe_dxy[2]+pe_dxy[3]*x)+(x>8&&x<=40)*(pe_dxy[4]+pe_dxy[5]*x)+(x>40&&x<=200)*(pe_dxy[6]+pe_dxy[7]*x);
	  dszerr_scale[3] = (x<=5)*(pe_dsz[0]+pe_dsz[1]*x+pe_dsz[2]*pow(x,2))+(x>5&&x<=20)*(pe_dsz[3]+pe_dsz[4]*x+pe_dsz[5]*pow(x,2))+(x>20&&x<=80)*(pe_dsz[6]+pe_dsz[7]*x)+(x>80&&x<=200)*(pe_dsz[8]+pe_dsz[9]*x);
	  
	  //2017 F
	  const double pf_dxy[9] = {0.9632406813200427, 0.05622873191000643, 1.002334039671506, 0.05345613714980831, -0.0023364984222545467, 1.3586160288262277, -0.0036480551019057073, 1.0892897635140877, 0.0009724468173780977};
	  const double pf_dsz[10] = {0.956793222542059, 0.07830129712754953, -0.004986750813002189, 1.0782049901540949, 0.03516919473607397, -0.0009714964267480747, 1.4796997655458373, -0.003229301671130096, 1.2888999031352133, 0.0016483979439785338};

	 
	  dxyerr_scale[4] = (x<=4)*(pf_dxy[0]+pf_dxy[1]*x)+(x>4&&x<=10)*(pf_dxy[2]+pf_dxy[3]*x+pf_dxy[4]*pow(x,2))+(x>10&&x<=40)*(pf_dxy[5]+pf_dxy[6]*x)+(x>40&&x<=200)*(pf_dxy[7]+pf_dxy[8]*x);
	  dszerr_scale[4] = (x<=5)*(pf_dsz[0]+pf_dsz[1]*x+pf_dsz[2]*pow(x,2))+(x>5&&x<=16)*(pf_dsz[3]+pf_dsz[4]*x+pf_dsz[5]*pow(x,2))+(x>16&&x<=40)*(pf_dsz[6]+pf_dsz[7]*x)+(x>40&&x<=200)*(pf_dsz[8]+pf_dsz[9]*x);
	  
      	}
	// for (int k =0; k < max_era; ++k) {
	//   rescaled_dxyerr[k] *= dxyerr_scale[k];
	//   rescaled_dxydszcov[k] *= sqrt(dxyerr_scale[k]);
	//   rescaled_dszerr[k] *= dszerr_scale[k];
	//   rescaled_dxydszcov[k] *= sqrt(dszerr_scale[k]);
	//   // nsigmadxy[k] *= dxybs / rescaled_dxyerr[k]; 

	// }
      }


      const bool nm1[5] = {
	pt > 1,
	min_r <= 1,
	npxlayers >= 2,
	nstlayers >= 6,
	nsigmadxy > 4
	// nsigmadxy[0] > 4,
	// nsigmadxy[1] > 4,
	// nsigmadxy[2] > 4,
	// nsigmadxy[3] > 4,
	// nsigmadxy[4] > 4,
	
      };

      const bool sel = nm1[0] && nm1[1] && nm1[2] && nm1[3];
      // std::vector<bool> v_seed = {nm1[4], nm1[5], nm1[6], nm1[7], nm1[8]};
      // const bool seed[5] = {sel && nm1[4], sel && nm1[5], sel && 

      
      const bool seed = sel && nm1[4];
      //const bool sel_nolep = sel && !ntt.ismu(itk) && !ntt.isel(itk);
      //const bool sel_nomu = sel && !ntt.ismu(itk);
      //const bool sel_noel = sel && !ntt.isel(itk);
      // const bool tk_ok[max_tk_type] = { true, sel, sel_nolep, sel_nomu, sel_noel, seed };
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
	h_tracks_absdxy[i]->Fill(fabs(dxybs), w);
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
	h_tracks_nsigmadxy[i]->Fill(dxybs / ntt.err_dxy(itk), w);
	h_tracks_nsigmadsz[i]->Fill(ntt.dsz(itk) / ntt.err_dsz(itk), w);

	h_tracks_dxyerr[i]->Fill(ntt.err_dxy(itk), w);
	h_tracks_dxydszcov[i]->Fill(ntt.cov_34(itk), w);
	h_tracks_absdxydszcov[i]->Fill(fabs(ntt.cov_34(itk)), w);
	h_tracks_dzerr[i]->Fill(ntt.err_dz(itk), w);
	h_tracks_dszerr[i]->Fill(ntt.err_dsz(itk), w);
	//	h_tracks_lambdaerr[i]->Fill(ntt.err_lambda(itk), w);
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

	h_tracks_dxyerr_v_pt[i]->Fill(pt, ntt.err_dxy(itk), w);
	h_tracks_dxyerr_v_eta[i]->Fill(ntt.eta(itk), ntt.err_dxy(itk), w);
	h_tracks_dxyerr_v_phi[i]->Fill(ntt.phi(itk), ntt.err_dxy(itk), w);
	// h_tracks_dxyerr_v_dxy[i]->Fill(dxybs, ntt.err_dxy(itk), w);
	// h_tracks_dxyerr_v_dzpv[i]->Fill(ntt.dzpv(itk, nt.pvs()), ntt.err_dxy(itk), w);
	// h_tracks_dxyerr_v_npxlayers[i]->Fill(npxlayers, ntt.err_dxy(itk), w);
	// h_tracks_dxyerr_v_nstlayers[i]->Fill(nstlayers, ntt.err_dxy(itk), w);

	h_tracks_dszerr_v_pt[i]->Fill(pt, ntt.err_dsz(itk), w);
	h_tracks_dszerr_v_eta[i]->Fill(ntt.eta(itk), ntt.err_dsz(itk), w);
	h_tracks_dszerr_v_phi[i]->Fill(ntt.phi(itk), ntt.err_dsz(itk), w);
	// h_tracks_dszerr_v_dxy[i]->Fill(dxybs, ntt.err_dsz(itk), w);
	// h_tracks_dszerr_v_dz[i]->Fill(ntt.dz(itk), ntt.err_dsz(itk), w);
	// h_tracks_dszerr_v_npxlayers[i]->Fill(npxlayers, ntt.err_dsz(itk), w);
	// h_tracks_dszerr_v_nstlayers[i]->Fill(nstlayers, ntt.err_dsz(itk), w);

	// h_tracks_lambdaerr_v_pt[i]->Fill(pt, ntt.err_lambda(itk), w);
	// h_tracks_lambdaerr_v_eta[i]->Fill(ntt.eta(itk), ntt.err_lambda(itk), w);
	// h_tracks_lambdaerr_v_phi[i]->Fill(ntt.phi(itk), ntt.err_lambda(itk), w);
	// h_tracks_lambdaerr_v_dxy[i]->Fill(dxybs, ntt.err_lambda(itk), w);
	// h_tracks_lambdaerr_v_dz[i]->Fill(ntt.dz(itk), ntt.err_lambda(itk), w);
	// h_tracks_lambdaerr_v_npxlayers[i]->Fill(npxlayers, ntt.err_lambda(itk), w);
	// h_tracks_lambdaerr_v_nstlayers[i]->Fill(nstlayers, ntt.err_lambda(itk), w);

	h_tracks_eta_v_phi[i]->Fill(ntt.phi(itk), ntt.eta(itk), w);

	// now only considering sel tracks to fill the rescaled-by-era plots 
	// if (i == 1) {
	//   for (int j = 0; j < max_era; ++j) {
	//     h_era_tracks_absnsigmadxy[j]->Fill(nsigmadxy[j], w);
	//     h_era_tracks_nsigmadxy[j]->Fill(dxybs / rescaled_dxyerr[j], w);
	//     h_era_tracks_nsigmadsz[j]->Fill(ntt.dsz(itk) / rescaled_dszerr[j], w);
	//     h_era_tracks_dxyerr[j]->Fill(rescaled_dxyerr[j], w);
	//     h_era_tracks_dxydszcov[j]->Fill(rescaled_dxydszcov[j], w);
	//     h_era_tracks_absdxydszcov[j]->Fill(fabs(rescaled_dxydszcov[j]), w);
	//     h_era_tracks_dszerr[j]->Fill(rescaled_dszerr[j], w);
	//     h_era_tracks_dxyerr_v_pt[i]->Fill(pt, rescaled_dxyerr[j], w);
	//     h_era_tracks_dxyerr_v_eta[i]->Fill(ntt.eta(itk), rescaled_dxyerr[j], w);
	//     h_era_tracks_dxyerr_v_phi[i]->Fill(ntt.phi(itk), rescaled_dxyerr[j], w);
	//     h_era_tracks_dszerr_v_pt[i]->Fill(pt, rescaled_dszerr[j], w);
	//     h_era_tracks_dszerr_v_eta[i]->Fill(ntt.eta(itk), rescaled_dszerr[j], w);
	//     h_era_tracks_dszerr_v_phi[i]->Fill(ntt.phi(itk), rescaled_dszerr[j], w);
	//   }
	// }
      }
    }

    

    for (int i = 0; i < max_tk_type; ++i)
      h_ntracks[i]->Fill(ntracks[i], w);

    return std::make_pair(true, w);
  };

  nr.loop(fcn);
}
