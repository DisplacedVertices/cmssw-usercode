#include "TH2.h"
#include "JMTucker/MFVNeutralino/interface/Ntuple.h"
#include "JMTucker/Tools/interface/Geometry.h"
#include "JMTucker/Tools/interface/NtupleReader.h"

int main(int argc, char** argv) {
  jmt::NtupleReader<mfv::K0Ntuple> nr;
  nr.init_options("mfvK0s/t");
  if (!nr.parse_options(argc, argv) || !nr.init()) return 1;
  auto& nt = nr.nt();
  auto& ntt = nt.tracks();
  auto& bs = nt.bs(); //Alec added from here
  auto& pvs = nt.pvs();
  //auto& jets = nt.jets();
  auto& muons = nt.muons();
  //auto& electrons = nt.electrons();
  //auto& vs = nt.vertices();  //Alec to here

  TH1::SetDefaultSumw2();

  ////

  enum { mass_all, mass_lo, mass_hi, mass_on, max_mass_type };
  const char* mass_names[max_mass_type] = {"massall", "masslo", "masshi", "masson"};

  enum { pt_gt2lt2p2, pt_gt2p2lt2p5, pt_gt2p5lt3, pt_gt3lt4, pt_gt4, max_pt_type };                         //Alec added from here
  const char* pt_names[max_pt_type] = {"pt_gt2lt2p2", "pt_gt2p2lt2p5", "pt_gt2p5lt3", "pt_gt3lt4", "pt_gt4"};

  enum { dxy_ltp03, dxy_gtp03ltp06, dxy_gtp06ltp09, dxy_gtp09ltp13, dxy_gtp13ltp17, dxy_gtp17ltp23, dxy_gtp23ltp3, dxy_gtp3, max_dxy_type };
  const char* dxy_names[max_dxy_type] = {"dxy_ltp03", "dxy_gtp03ltp06", "dxy_gtp06ltp09", "dxy_gtp09ltp13", "dxy_gtp13ltp17", "dxy_gtp17ltp23", "dxy_gtp23ltp3", "dxy_gtp3"};

/*
  enum { pt_lt0p25, pt_gt0p25lt0p45, pt_gt0p45lt0p7, pt_gt0p7, max_pt_type };
  const char* pt_names[max_pt_type] = {"pt_lt0p25", "pt_gt0p25lt0p45", "pt_gt0p45lt0p7", "pt_gt0p7"};

  enum { dxy_ltp03, dxy_gtp03ltp06, dxy_gtp06ltp09, dxy_gtp09ltp13, dxy_gtp13ltp17, dxy_gtp17ltp23, dxy_gtp23ltp3, dxy_gtp3, max_dxy_type };
  const char* dxy_names[max_dxy_type] = {"dxy_ltp03", "dxy_gtp03ltp06", "dxy_gtp06ltp09", "dxy_gtp09ltp13", "dxy_gtp13ltp17", "dxy_gtp17ltp23", "dxy_gtp23ltp3", "dxy_gtp3"};
*/
/*
  enum { p_lt2p2, p_gt2p2lt2p5, p_gt2p5lt3, p_gt3lt4, p_gt4, max_p_type };
  const char* p_names[max_p_type] = {"p_lt2p2", "p_gt2p2lt2p5", "p_gt2p5lt3", "p_gt3lt4", "p_gt4"};

  enum { dxy_ltp03, dxy_gtp03ltp06, dxy_gtp06ltp09, dxy_gtp09ltp13, dxy_gtp13ltp17, dxy_gtp17ltp23, dxy_gtp23ltp3, dxy_gtp3, max_dxy_type };
  const char* dxy_names[max_dxy_type] = {"dxy_ltp03", "dxy_gtp03ltp06", "dxy_gtp06ltp09", "dxy_gtp09ltp13", "dxy_gtp13ltp17", "dxy_gtp17ltp23", "dxy_gtp23ltp3", "dxy_gtp3"};
*/

  enum { dbv_gtp2ltp4, dbv_gtp4ltp6, dbv_gtp6ltp8, dbv_gtp8lt1, dbv_gt1lt1p2, dbv_gt1p2lt1p4, dbv_gt1p4lt1p6, dbv_gt1p6lt1p9, max_dbv_type };
  const char* dbv_names[max_dbv_type] = {"dbv_gtp2ltp4", "dbv_gtp4ltp6", "dbv_gtp6ltp8", "dbv_gtp8lt1", "dbv_gt1lt1p2", "dbv_gt1p2lt1p4", "dbv_gt1p4lt1p6", "dbv_gt1p6lt1p9"};

  enum { abseta_lt1, abseta_gt1lt1p9, abseta_gt1p9, max_abseta_type };
  const char* abseta_names[max_abseta_type] = {"abseta_lt1", "abseta_gt1lt1p9", "abseta_gt1p9"};
  //Alec added to here  

  TH1D* h_nvtx[max_mass_type];
  TH1D* h_chi2dof[max_mass_type];
  TH1D* h_premass[max_mass_type];
  TH1D* h_mass[max_mass_type];  //Alec commented
  /*TH1D* h_mass_ptlt2_dxyltp02_pimintrack[max_mass_type];       //Alec added from here to here
  TH1D* h_mass_ptgt2lt5_dxyltp02_pimintrack[max_mass_type];
  TH1D* h_mass_ptgt5_dxyltp02_pimintrack[max_mass_type];
  TH1D* h_mass_ptlt2_dxygtp02ltp1_pimintrack[max_mass_type];    //These were added back when I was comparing max vs. min of the two track impact parameters, no difference
  TH1D* h_mass_ptlt2_dxygtp1_pimintrack[max_mass_type];
  TH1D* h_mass_ptgt2lt5_dxygtp02ltp1_pimintrack[max_mass_type];*/
  //TH1D* h_mass_bin[max_mass_type][max_pt_type][max_dxy_type];
  TH1D* h_mass_bin[max_mass_type][max_abseta_type][max_pt_type][max_dxy_type];
  TH1D* h_mass_dbvbin[max_mass_type][max_abseta_type][max_pt_type][max_dbv_type];
  TH1D* h_p[max_mass_type];
  TH1D* h_pt[max_mass_type];
  TH1D* h_dbv[max_mass_type]; //Alec added
  TH1D* h_eta[max_mass_type];
  TH1D* h_phi[max_mass_type];
  TH1D* h_deltazpv[max_mass_type];
  TH1D* h_costh3[max_mass_type];
  TH1D* h_costh2[max_mass_type];
  TH1D* h_trackdeltaeta[max_mass_type];
  TH1D* h_trackdeltaphi[max_mass_type];
  TH1D* h_trackdeltaz[max_mass_type];
  TH1D* h_ct[max_mass_type];
  TH1D* h_ctau[max_mass_type];
  TH1D* h_rho[max_mass_type];
  TH1D* h_tracks_pt[max_mass_type];
  TH1D* h_tracks_eta[max_mass_type];
  TH1D* h_tracks_phi[max_mass_type];
  TH1D* h_tracks_dxy[max_mass_type];
  TH1D* h_tracks_absdxy[max_mass_type];
  TH1D* h_tracks_dz[max_mass_type];
  TH1D* h_tracks_dzpv[max_mass_type];
  TH1D* h_tracks_nhits[max_mass_type];
  TH1D* h_tracks_npxhits[max_mass_type];
  TH1D* h_tracks_nsthits[max_mass_type];
  TH1D* h_tracks_min_r[max_mass_type];
  TH1D* h_tracks_npxlayers[max_mass_type];
  TH1D* h_tracks_nstlayers[max_mass_type];
  TH1D* h_tracks_nsigmadxy[max_mass_type];
  TH1D* h_tracks_dxyerr[max_mass_type];
  TH1D* h_tracks_dzerr[max_mass_type];
  TH1D* h_tracks_dszerr[max_mass_type];
  TH1D* h_tracks_lambdaerr[max_mass_type];
  TH1D* h_tracks_pterr[max_mass_type];
  TH1D* h_tracks_phierr[max_mass_type];
  TH1D* h_tracks_etaerr[max_mass_type];
  TH2D* h_tracks_dxyerr_v_pt[max_mass_type];
  TH2D* h_tracks_dszerr_v_pt[max_mass_type];
  TH2D* h_dbv_v_pt[max_mass_type]; //Alec added from here
  TH2D* h_tracks_absdxy_v_pt[max_mass_type];
  TH2D* h_tracks_absdxy_v_alphapt[max_mass_type];
  /*TH2D* h_ptlt2_dxyltp02_mintracks_absdxy_v_alphapt[max_mass_type];
  TH2D* h_ptgt2lt5_dxyltp02_mintracks_absdxy_v_alphapt[max_mass_type];
  TH2D* h_ptgt5_dxyltp02_mintracks_absdxy_v_alphapt[max_mass_type];
  TH2D* h_ptlt2_dxygtp02ltp1_mintracks_absdxy_v_alphapt[max_mass_type];
  TH2D* h_ptlt2_dxygtp1_mintracks_absdxy_v_alphapt[max_mass_type];
  TH2D* h_ptgt2lt5_dxygtp02ltp1_mintracks_absdxy_v_alphapt[max_mass_type];
  TH2D* h_ptlt2_dxyltp02_maxtracks_absdxy_v_alphapt[max_mass_type];
  TH2D* h_ptgt2lt5_dxyltp02_maxtracks_absdxy_v_alphapt[max_mass_type];
  TH2D* h_ptgt5_dxyltp02_maxtracks_absdxy_v_alphapt[max_mass_type];
  TH2D* h_ptlt2_dxygtp02ltp1_maxtracks_absdxy_v_alphapt[max_mass_type];
  TH2D* h_ptlt2_dxygtp1_maxtracks_absdxy_v_alphapt[max_mass_type];
  TH2D* h_ptgt2lt5_dxygtp02ltp1_maxtracks_absdxy_v_alphapt[max_mass_type];*/
  //Alec added to here

  for (int i = 0; i < max_mass_type; ++i) {
    TDirectory* d = nr.f_out().mkdir(mass_names[i]);
    d->cd();

    h_nvtx[i] = new TH1D("h_nvtx", ";# of K0 candidates;events", 30, 0, 30);
    h_chi2dof[i] = new TH1D("h_chi2dof", ";K0 candidate #chi^{2}/dof;cands/0.1", 70, 0, 7);
    h_premass[i] = new TH1D("h_premass", ";K0 candidate pre-fit mass (GeV);cands/5 MeV", 400, 0, 2);
    h_mass[i] = new TH1D("h_mass", ";K0 candidate mass (GeV);cands/5 MeV", 400, 0, 2); //Alec commented
    /*h_mass_ptlt2_dxyltp02_pimintrack[i] = new TH1D("h_mass_ptlt2_dxyltp02_pimintrack", ";K0 candidate mass (GeV);cands/5 MeV", 400, 0, 2); //Alec added from here
    h_mass_ptgt2lt5_dxyltp02_pimintrack[i] = new TH1D("h_mass_ptgt2lt5_dxyltp02_pimintrack", ";K0 candidate mass (GeV);cands/5 MeV", 400, 0, 2);
    h_mass_ptgt5_dxyltp02_pimintrack[i] = new TH1D("h_mass_ptgt5_dxyltp02_pimintrack", ";K0 candidate mass (GeV);cands/5 MeV", 400, 0, 2);
    h_mass_ptlt2_dxygtp02ltp1_pimintrack[i] = new TH1D("h_mass_ptlt2_dxygtp02ltp1_pimintrack", ";K0 candidate mass (GeV);cands/5 MeV", 400, 0, 2);
    h_mass_ptlt2_dxygtp1_pimintrack[i] = new TH1D("h_mass_ptlt2_dxygtp1_pimintrack", ";K0 candidate mass (GeV);cands/5 MeV", 400, 0, 2);
    h_mass_ptgt2lt5_dxygtp02ltp1_pimintrack[i] = new TH1D("h_mass_ptgt2lt5_dxygtp02ltp1_pimintrack", ";K0 candidate mass (GeV);cands/5 MeV", 400, 0, 2);
    h_mass_ptlt2_dxyltp02_pimaxtrack[i] = new TH1D("h_mass_ptlt2_dxyltp02_pimaxtrack", ";K0 candidate mass (GeV);cands/5 MeV", 400, 0, 2);
    h_mass_ptgt2lt5_dxyltp02_pimaxtrack[i] = new TH1D("h_mass_ptgt2lt5_dxyltp02_pimaxtrack", ";K0 candidate mass (GeV);cands/5 MeV", 400, 0, 2);
    h_mass_ptgt5_dxyltp02_pimaxtrack[i] = new TH1D("h_mass_ptgt5_dxyltp02_pimaxtrack", ";K0 candidate mass (GeV);cands/5 MeV", 400, 0, 2);
    h_mass_ptlt2_dxygtp02ltp1_pimaxtrack[i] = new TH1D("h_mass_ptlt2_dxygtp02ltp1_pimaxtrack", ";K0 candidate mass (GeV);cands/5 MeV", 400, 0, 2);
    h_mass_ptlt2_dxygtp1_pimaxtrack[i] = new TH1D("h_mass_ptlt2_dxygtp1_pimaxtrack", ";K0 candidate mass (GeV);cands/5 MeV", 400, 0, 2);
    h_mass_ptgt2lt5_dxygtp02ltp1_pimaxtrack[i] = new TH1D("h_mass_ptgt2lt5_dxygtp02ltp1_pimaxtrack", ";K0 candidate mass (GeV);cands/5 MeV", 400, 0, 2);*/ //Alec added to here
    h_p[i] = new TH1D("h_p", ";K0 candidate p (GeV);cands/1 GeV", 200, 0, 200);
    h_pt[i] = new TH1D("h_pt", ";K0 candidate p_{T} (GeV);cands/1 GeV", 200, 0, 200);
    h_dbv[i] = new TH1D("h_dbv", ";K0 candidate 2D distance from BS (cm);cands/0.005 cm", 400, 0, 2);
    h_eta[i] = new TH1D("h_eta", ";K0 candidate #eta;cands/0.05", 100, -2.5, 2.5);
    h_phi[i] = new TH1D("h_phi", ";K0 candidate #phi;cands/0.063", 100, -M_PI, M_PI);
    h_deltazpv[i] = new TH1D("h_deltazpv", ";K0 candidate |#Delta z to PV| (cm);cands/0.1 cm", 200, 0, 20);
    h_costh3[i] = new TH1D("h_costh3", ";K0 candidate cos(angle3{flight,momentum});cands/0.00025", 202, 0.95, 1.001);
    h_costh2[i] = new TH1D("h_costh2", ";K0 candidate cos(angle2{flight,momentum});cands/0.00025", 202, 0.95, 1.001);
    h_trackdeltaeta[i] = new TH1D("h_trackdeltaeta", ";K0 candidate track #Delta #eta;cands/0.025", 100, 0, 2.5);
    h_trackdeltaphi[i] = new TH1D("h_trackdeltaphi", ";K0 candidate track #Delta #phi;cands/0.063", 100, -M_PI, M_PI);
    h_trackdeltaz[i] = new TH1D("h_trackdeltaz", ";K0 candidate |#Delta track z| (cm);cands/0.03 cm", 100, 0, 3);
    h_ct[i] = new TH1D("h_ct", ";K0 candidate ct (cm);cands/0.005 cm", 400, 0, 2);
    h_ctau[i] = new TH1D("h_ctau", ";K0 candidate c#tau (cm);cands/0.005 cm", 400, 0, 2);
    h_rho[i] = new TH1D("h_rho", ";K0 candidate #rho (cm);cands/0.005 cm", 400, 0, 2);
    h_tracks_pt[i] = new TH1D("h_tracks_pt", ";tracks pt;arb. units", 200, 0, 200);
    h_tracks_eta[i] = new TH1D("h_tracks_eta", ";tracks eta;arb. units", 50, -4, 4);
    h_tracks_phi[i] = new TH1D("h_tracks_phi", ";tracks phi;arb. units", 32, -3.15, 3.15);
    h_tracks_dxy[i] = new TH1D("h_tracks_dxy", ";tracks dxy to beamspot (cm);arb. units", 2000, -1, 1);  //Alec changed +-.2 to +-1 and 400 to 2000
    h_tracks_absdxy[i] = new TH1D("h_tracks_absdxy", ";tracks |dxy| to beamspot (cm);arb. units", 1000, 0, 1); //Alec changed 0.2 to 1 and 200 to 1000
    h_tracks_dz[i] = new TH1D("h_tracks_dz", ";tracks dz to BS;arb. units", 400, -20, 20);
    h_tracks_dzpv[i] = new TH1D("h_tracks_dzpv", ";tracks dz to PV;arb. units", 400, -20, 20);
    h_tracks_nhits[i] = new TH1D("h_tracks_nhits", ";tracks nhits;arb. units", 40, 0, 40);
    h_tracks_npxhits[i] = new TH1D("h_tracks_npxhits", ";tracks npxhits;arb. units", 40, 0, 40);
    h_tracks_nsthits[i] = new TH1D("h_tracks_nsthits", ";tracks nsthits;arb. units", 40, 0, 40);
    h_tracks_min_r[i] = new TH1D("h_tracks_min_r", ";tracks min_r;arb. units", 20, 0, 20);
    h_tracks_npxlayers[i] = new TH1D("h_tracks_npxlayers", ";tracks npxlayers;arb. units", 20, 0, 20);
    h_tracks_nstlayers[i] = new TH1D("h_tracks_nstlayers", ";tracks nstlayers;arb. units", 20, 0, 20);
    h_tracks_nsigmadxy[i] = new TH1D("h_tracks_nsigmadxy", ";tracks nsigmadxy;arb. units", 400, 0, 40);
    h_tracks_dxyerr[i] = new TH1D("h_tracks_dxyerr", ";tracks dxyerr;arb. units", 400, 0, 0.04);
    h_tracks_dzerr[i] = new TH1D("h_tracks_dzerr", ";tracks dzerr;arb. units", 400, 0, 0.04);
    h_tracks_dszerr[i] = new TH1D("h_tracks_dszerr", ";tracks dszerr;arb. units", 400, 0, 0.04);
    h_tracks_lambdaerr[i] = new TH1D("h_tracks_lambdaerr", ";tracks lambdaerr;arb. units", 2000, 0, 0.2);
    h_tracks_pterr[i] = new TH1D("h_tracks_pterr", ";tracks pterr;arb. units", 200, 0, 0.2);
    h_tracks_phierr[i] = new TH1D("h_tracks_phierr", ";tracks phierr;arb. units", 200, 0, 0.2);
    h_tracks_etaerr[i] = new TH1D("h_tracks_etaerr", ";tracks etaerr;arb. units", 200, 0, 0.2);
    h_tracks_dxyerr_v_pt[i] = new TH2D("h_tracks_dxyerr_v_pt", ";p_{T} (GeV);dxyerr (cm)", 2000, 0, 200, 2000, 0, 0.2);
    h_tracks_dszerr_v_pt[i] = new TH2D("h_tracks_dszerr_v_pt", ";p_{T} (GeV);dszerr (cm)", 2000, 0, 200, 2000, 0, 0.2);
    h_dbv_v_pt[i] = new TH2D("h_dbv_v_pt", ";K0 candidate p_{T} (GeV);K0 candidate 2D distance from BS (cm)", 200, 0, 200, 400, 0, 2); //Alec added from here
    h_tracks_absdxy_v_pt[i] = new TH2D("h_tracks_absdxy_v_pt", ";pion track p_{T} (GeV);tracks |dxy| to beamspot (cm)", 200, 0, 200, 1000, 0, 1);
    h_tracks_absdxy_v_alphapt[i] = new TH2D("h_tracks_absdxy_v_alphapt", ";pion track p_{T} * abs sine of 2D angle between K0 and pion track (GeV);tracks |dxy| to beamspot (cm)", 200, 0, 200, 1000, 0, 1);
    /*h_ptlt2_dxyltp02_mintracks_absdxy_v_alphapt[i] = new TH2D("h_ptlt2_dxyltp02_mintracks_absdxy_v_alphapt", ";pion mindxy track p_{T} * abs sine of 2D angle between K0 and pion track (GeV);tracks |dxy| to beamspot (cm)", 10, 0, 2, 20, 0, .02);
    h_ptgt2lt5_dxyltp02_mintracks_absdxy_v_alphapt[i] = new TH2D("h_ptgt2lt5_dxyltp02_mintracks_absdxy_v_alphapt", ";pion mindxy track p_{T} * abs sine of 2D angle between K0 and pion track (GeV);tracks |dxy| to beamspot (cm)", 10, 2, 5, 20, 0, .02);
    h_ptgt5_dxyltp02_mintracks_absdxy_v_alphapt[i] = new TH2D("h_ptgt5_dxyltp02_mintracks_absdxy_v_alphapt", ";pion mindxy track p_{T} * abs sine of 2D angle between K0 and pion track (GeV);tracks |dxy| to beamspot (cm)", 10, 5, 200, 20, 0, .02);
    h_ptlt2_dxygtp02ltp1_mintracks_absdxy_v_alphapt[i] = new TH2D("h_ptlt2_dxygtp02ltp1_mintracks_absdxy_v_alphapt", ";pion mindxy track p_{T} * abs sine of 2D angle between K0 and pion track (GeV);tracks |dxy| to beamspot (cm)", 10, 0, 2, 80, .02, .1);
    h_ptlt2_dxygtp1_mintracks_absdxy_v_alphapt[i] = new TH2D("h_ptlt2_dxygtp1_mintracks_absdxy_v_alphapt", ";pion mindxy track p_{T} * abs sine of 2D angle between K0 and pion track (GeV);tracks |dxy| to beamspot (cm)", 10, 0, 2, 900, .1, 1);
    h_ptgt2lt5_dxygtp02ltp1_mintracks_absdxy_v_alphapt[i] = new TH2D("h_ptgt2lt5_dxygtp02ltp1_mintracks_absdxy_v_alphapt", ";pion mindxy track p_{T} * abs sine of 2D angle between K0 and pion track (GeV);tracks |dxy| to beamspot (cm)", 10, 2, 5, 80, .02, .1);
    h_ptlt2_dxyltp02_maxtracks_absdxy_v_alphapt[i] = new TH2D("h_ptlt2_dxyltp02_maxtracks_absdxy_v_alphapt", ";pion maxdxy track p_{T} * abs sine of 2D angle between K0 and pion track (GeV);tracks |dxy| to beamspot (cm)", 10, 0, 2, 20, 0, .02);
    h_ptgt2lt5_dxyltp02_maxtracks_absdxy_v_alphapt[i] = new TH2D("h_ptgt2lt5_dxyltp02_maxtracks_absdxy_v_alphapt", ";pion maxdxy track p_{T} * abs sine of 2D angle between K0 and pion track (GeV);tracks |dxy| to beamspot (cm)", 10, 2, 5, 20, 0, .02);
    h_ptgt5_dxyltp02_maxtracks_absdxy_v_alphapt[i] = new TH2D("h_ptgt5_dxyltp02_maxtracks_absdxy_v_alphapt", ";pion maxdxy track p_{T} * abs sine of 2D angle between K0 and pion track (GeV);tracks |dxy| to beamspot (cm)", 10, 5, 200, 20, 0, .02);
    h_ptlt2_dxygtp02ltp1_maxtracks_absdxy_v_alphapt[i] = new TH2D("h_ptlt2_dxygtp02ltp1_maxtracks_absdxy_v_alphapt", ";pion maxdxy track p_{T} * abs sine of 2D angle between K0 and pion track (GeV);tracks |dxy| to beamspot (cm)", 10, 0, 2, 80, .02, .1);
    h_ptlt2_dxygtp1_maxtracks_absdxy_v_alphapt[i] = new TH2D("h_ptlt2_dxygtp1_maxtracks_absdxy_v_alphapt", ";pion maxdxy track p_{T} * abs sine of 2D angle between K0 and pion track (GeV);tracks |dxy| to beamspot (cm)", 10, 0, 2, 900, .1, 1);
    h_ptgt2lt5_dxygtp02ltp1_maxtracks_absdxy_v_alphapt[i] = new TH2D("h_ptgt2lt5_dxygtp02ltp1_maxtracks_absdxy_v_alphapt", ";pion maxdxy track p_{T} * abs sine of 2D angle between K0 and pion track (GeV);tracks |dxy| to beamspot (cm)", 10, 2, 5, 80, .02, .1);
//Alec added to here */
  
    for (int l = 0; l < max_abseta_type; ++l) {
      TDirectory* dmakeeta = d->mkdir(abseta_names[l]);
      dmakeeta->cd();

      for (int j = 0; j < max_pt_type; ++j) {        //remember to change this when switching between binning in p or pt
        TDirectory* dmakept = dmakeeta->mkdir(pt_names[j]);
        dmakept->cd();

        for (int k = 0; k < max_dxy_type; ++k) {
          TDirectory* dmakedxy = dmakept->mkdir(dxy_names[k]);
          dmakedxy->cd();

          h_mass_bin[i][l][j][k] = new TH1D("h_mass_bin", ";K0 candidate mass (GeV);cands/5 MeV", 400, 0, 2);
        }

        for (int k = 0; k < max_dbv_type; ++k) {
          TDirectory* dmakedbv = dmakept->mkdir(dbv_names[k]);
          dmakedbv->cd();

          h_mass_dbvbin[i][l][j][k] = new TH1D("h_mass_dbvbin", ";K0 candidate mass (GeV);cands/5 MeV", 400, 0, 2);
        }
      }
    }

    //for (int j = 0; j < max_pt_type; ++j) {
      //TDirectory* dmakept = d->mkdir(pt_names[j]);
      //dmakept->cd();

      //for (int k = 0; k < max_dbv_type; ++k) {
        //TDirectory* dmakedbv = dmakept->mkdir(dbv_names[k]);
        //dmakedbv->cd();

        //h_mass_dbvbin[i][j][k] = new TH1D("h_mass_dbvbin", ";K0 candidate mass (GeV);cands/5 MeV", 400, 0, 2);
      //}
    //}
  }

  nr.f_out().cd();

  const double mpion = 0.13957;
  const double min_nsigmadxybs = 0.;

  auto fcn = [&]() {
    const double w = nr.weight();  //Alec added absolute value to the weights here to see what would happen, CHANGE THIS BACK!

    int nselmuons = 0;  //Alec added this TrackerMapper block from here
    //double muon_pT = -99;
    double muon_p = -99;
    double muon_q = -99;
    double muon_px = -99;
    double muon_py = -99;
    double muon_pz = -99;
    //double muon_abseta = -99; 
    //double muon_iso = 99;
    //double muon_absdxybs = -99;
    //double muon_absdz = -99;
    //double muon_nsigmadxybs = -99;
    TLorentzVector muon_p4;
    TLorentzVector tmpz_p4;
    TLorentzVector zmumu_p4;
    TLorentzVector zee_p4;
    bool has_Zmumuboson = false;
    //bool has_Zeeboson = false;
    //bool has_Wboson = false;
    
    for (int i = 0, ie = muons.n(); i < ie; ++i) {
      //FIXME cut on IPs in addition to IDs 
      double tmp_muon_absdxybs = abs(muons.dxybs(i, bs));
      double tmp_muon_absdz = muons.dzpv(i, pvs);
      //abs((muons.vz(i) - pvs.z(0)) - ((muons.vx(i) - pvs.x(0)) * muons.px(i) + (muons.vy(i) - pvs.y(0)) * muons.py(i)) / muons.pt(i) * muons.pz(i) / muons.pt(i));
      bool muon_IP_cut = tmp_muon_absdxybs < 0.02 && tmp_muon_absdz < 0.5;
      if (muon_IP_cut && muons.pt(i) > 29.0 && abs(muons.eta(i)) < 2.4 && muons.isMed(i) && muons.iso(i) < 0.15) {
	nselmuons += 1;
	if (nselmuons == 1) {
	  //muon_pT = muons.pt(i);
	  muon_p = muons.p(i);
	  muon_px = muons.px(i);
	  muon_py = muons.py(i);
	  muon_pz = muons.pz(i);
	  muon_p4.SetPxPyPzE(muon_px, muon_py, muon_pz, muon_p);
	  muon_q = muons.q(i);
	  //muon_abseta = abs(muons.eta(i));
	  //muon_absdxybs = abs(muons.dxybs(i, bs));
	  //muon_absdz =  muons.dzpv(i, pvs);
	  //abs((muons.vz(i) - pvs.z(0)) - ((muons.vx(i) - pvs.x(0)) * muons.px(i) + (muons.vy(i) - pvs.y(0)) * muons.py(i)) / muons.pt(i) * muons.pz(i) / muons.pt(i));
	  //muon_iso = muons.iso(i);
	  //muon_nsigmadxybs = muons.nsigmadxybs(i, bs);
	  tmpz_p4 += muon_p4;

	}
	if (nselmuons == 2 && muon_q * muons.q(i) == -1) {
	  TLorentzVector antimuon_p4;
	  antimuon_p4.SetPxPyPzE(muons.px(i), muons.py(i), muons.pz(i), muons.p(i));
	  tmpz_p4 += antimuon_p4;
	  //has_Zmumuboson = true;
          if (tmpz_p4.M() > 80 && tmpz_p4.M() < 100) {has_Zmumuboson = true;} //Alec added this line and commented above line so invariant mass consistent with Z boson
	}
      }
    }

    //double z_m = -99;
    //double zmumu_m = -99; 
    //double z_pT = -99;
    //double zmumu_pT = -99;
    if (has_Zmumuboson) {
      //zmumu_m = tmpz_p4.M();
      //zmumu_pT = tmpz_p4.Pt();
      zmumu_p4 = tmpz_p4;
    }

    /*int nseleles = 0;
    //double ele_pT = -99;
    double ele_p = -99;
    double ele_q = -99;
    double ele_px = -99;
    double ele_py = -99;
    double ele_pz = -99;
    //double ele_abseta = -99;
    //double ele_iso = 99;
    //double ele_absdxybs = -99;
    //double ele_absdz = -99;
    //double ele_nsigmadxybs = -99;
    TLorentzVector ele_p4;
    tmpz_p4.SetPxPyPzE(0.0, 0.0, 0.0, 0.0);

    for (int i = 0, ie = electrons.n(); i < ie; ++i) {
      double tmp_ele_abseta = abs(electrons.eta(i));
      double tmp_ele_absdxybs = abs(electrons.dxybs(i, bs));
      double tmp_ele_absdz = electrons.dzpv(i, pvs);  
      //abs((electrons.vz(i) - pvs.z(0)) - ((electrons.vx(i) - pvs.x(0)) * electrons.px(i) + (electrons.vy(i) - pvs.y(0)) * electrons.py(i)) / electrons.pt(i) * electrons.pz(i) / electrons.pt(i));
      bool ele_IP_cut = tmp_ele_abseta < 1.48 ? tmp_ele_absdxybs < 0.05 && tmp_ele_absdz < 0.1 : tmp_ele_absdxybs < 0.1 && tmp_ele_absdz < 0.2;
      if (ele_IP_cut && electrons.pt(i) > 20.0 && abs(electrons.eta(i)) < 2.4 && electrons.isTight(i) && electrons.passveto(i) && electrons.iso(i) < 0.1) {
	nseleles += 1;
	if (nseleles == 1) {
	  //ele_pT = electrons.pt(i);
	  ele_p = electrons.p(i);
	  ele_px = electrons.px(i);
	  ele_py = electrons.py(i);
	  ele_pz = electrons.pz(i);
	  //ele_abseta = abs(electrons.eta(i));
	  //ele_absdxybs = abs(electrons.dxybs(i, bs));
	  //ele_absdz = electrons.dzpv(i, pvs);
	  //abs((electrons.vz(i) - pvs.z(0)) - ((electrons.vx(i) - pvs.x(0)) * electrons.px(i) + (electrons.vy(i) - pvs.y(0)) * electrons.py(i)) / electrons.pt(i) * electrons.pz(i) / electrons.pt(i));
	  ele_p4.SetPxPyPzE(ele_px, ele_py, ele_pz, ele_p);
	  ele_q = electrons.q(i);
	  //ele_iso = electrons.iso(i);
	  //ele_nsigmadxybs = electrons.nsigmadxybs(i, bs);
	  tmpz_p4 += ele_p4;

	}
	
	if (nseleles > 0 && ele_q * electrons.q(i) == -1) {
	  TLorentzVector antiele_p4;
	  antiele_p4.SetPxPyPzE(electrons.px(i), electrons.py(i), electrons.pz(i), electrons.p(i));
	  tmpz_p4 += antiele_p4;
	  //has_Zeeboson = true;
	}
      }
    }*/  //Alec to this line

    auto fill  = [&](TH1* h, double x)           { h->Fill(x,    w); };
    auto fill2 = [&](TH2* h, double x, double y) { h->Fill(x, y, w); };

    const TVector3 pv = nt.pvs().pos(0);

    int nvtx[max_mass_type] = {0};

    for (int isv = 0, isve = nt.svs().n(); isv < isve; ++isv) {
      const TVector3 pos = nt.svs().pos(isv);
      if (!jmt::Geometry::inside_beampipe(nr.is_mc(), pos.X(), pos.Y()))
        continue;

      const TVector3 flight = pos - pv;
      const TVector3 flight2(flight.X(), flight.Y(), 0);
      const double rho = flight.Perp();
      const double deltazpv = flight.Z();

      //if (rho < 0.268) continue;  //got rid of this cut to try to eliminate drop off in events at low dxy in past analysis

      const int itk = nt.svs().misc(isv) & 0xFFFF;
      const int jtk = nt.svs().misc(isv) >> 16;
      const double trackdeltaz = fabs(ntt.vz(itk) - ntt.vz(jtk));
      const double trackdeltaeta = fabs(ntt.eta(itk) - ntt.eta(jtk));
      const double trackdeltaphi = TVector2::Phi_mpi_pi(ntt.phi(itk) - ntt.phi(jtk));

      if (!ntt.pass_seed(itk, nt.bs(), min_nsigmadxybs) ||
          !ntt.pass_seed(jtk, nt.bs(), min_nsigmadxybs))
        continue;

      const int irftk = 2*isv;
      const int jrftk = 2*isv+1;

      const TLorentzVector ip4 = ntt.p4(itk, mpion);
      const TLorentzVector jp4 = ntt.p4(jtk, mpion);
      const TLorentzVector prep4 = ip4 + jp4;

      const TLorentzVector irfp4 = nt.refit_tks().p4(irftk, mpion); //
      const TLorentzVector jrfp4 = nt.refit_tks().p4(jrftk, mpion); //
      const TLorentzVector p4 = irfp4 + jrfp4;
      const TVector3 pperp(p4.X(), p4.Y(), 0);

      //const float alpha_i = p4.DeltaPhi(irfp4); //Alec added
      //const float alpha_j = p4.DeltaPhi(jrfp4); //Alec added

      const double mass = p4.M();
      const double pt = p4.Pt(); //Alec added
      //const double p = p4.P(); //Alec added
      const double costh3 = p4.Vect().Unit().Dot(flight.Unit());
      const double costh2 = pperp.Unit().Dot(flight2.Unit());

      const double ct = flight.Mag();
      const double ctau = ct / p4.Beta() / p4.Gamma();

      const double x = pos.X();
      const double y = pos.Y();
      const double dbv = std::hypot(x-bs.x(), y-bs.y());  //Alec added

      if (dbv > 1.9) continue; //Alec added
      if (dbv < .2) continue; //Alec added, this cut appears to be in place without this to ensure displaced vertices, but just to be safe
      if (p4.Pt() < 2) continue;

      int iabseta = abseta_lt1;
      if      (fabs(p4.Eta()) > 1 && fabs(p4.Eta()) < 1.9) iabseta = abseta_gt1lt1p9;
      else if (fabs(p4.Eta()) > 1.9)                       iabseta = abseta_gt1p9;

      int ipt = pt_gt2lt2p2;  //Alec added
      if      (pt > 2.2 && pt < 2.5) ipt = pt_gt2p2lt2p5;
      if      (pt > 2.5 && pt < 3)   ipt = pt_gt2p5lt3;
      if      (pt > 3 && pt < 4)     ipt = pt_gt3lt4;
      else if (pt > 4)               ipt = pt_gt4;

      int idbv = dbv_gtp2ltp4; //Alec added
      if      (dbv > .4 && dbv < .6)   idbv = dbv_gtp4ltp6;
      if      (dbv > .6 && dbv < .8)   idbv = dbv_gtp6ltp8;
      if      (dbv > .8 && dbv < 1)    idbv = dbv_gtp8lt1;
      if      (dbv > 1 && dbv < 1.2)   idbv = dbv_gt1lt1p2;
      if      (dbv > 1.2 && dbv < 1.4) idbv = dbv_gt1p2lt1p4;
      if      (dbv > 1.4 && dbv < 1.6) idbv = dbv_gt1p4lt1p6;
      if      (dbv > 1.6 && dbv < 1.9) idbv = dbv_gt1p6lt1p9;

      //track dxy ntt.dxybs(tki, nt.bs()) 

      if (costh2 < 0.99975) continue;
      if (ctau < 0.0268) continue; //got rid of this cut to try to eliminate drop off in events at low dxy in past analysis, no noticable effect
      //if (fabs(p4.Eta()) > 0.5) continue;  //added this cut to ensure better agreement between data and MC when plotting wrt Kaon p

      int imass2 = mass_on;
      //if      (mass < 0.490) imass2 = mass_lo; //widened the range of mass_on to completely eliminate signal events from lo and hi, now those should be pure background
      //else if (mass > 0.505) imass2 = mass_hi;
      if      (mass < 0.475) imass2 = mass_lo;
      else if (mass > 0.525) imass2 = mass_hi;

      for (int ii : {0,1}) {
        const int imass = ii == 0 ? mass_all : imass2;

        fill(h_chi2dof[imass], nt.svs().chi2dof(isv));
        fill(h_premass[imass], prep4.M());
        fill(h_mass[imass], mass);
        fill(h_p[imass], p4.P());
        fill(h_pt[imass], p4.Pt());
        fill(h_dbv[imass], dbv); //Alec added
        fill(h_eta[imass], p4.Eta());
        fill(h_phi[imass], p4.Phi());
        fill(h_deltazpv[imass], deltazpv);
        fill(h_costh3[imass], costh3);
        fill(h_costh2[imass], costh2);
        fill(h_trackdeltaeta[imass], trackdeltaeta);
        fill(h_trackdeltaphi[imass], trackdeltaphi);
        fill(h_trackdeltaz[imass], trackdeltaz);
        fill(h_ct[imass], ct);
        fill(h_ctau[imass], ctau);
        fill(h_rho[imass], rho);
        fill(h_mass_dbvbin[imass][iabseta][ipt][idbv], mass); //Alec added
        fill2(h_dbv_v_pt[imass], p4.Pt(), dbv); //Alec added

        for (int tki : {itk, jtk}) {
          //if (fabs(ntt.dxybs(tki, nt.bs())) > .02) continue; //Alec added to see if we can find bias in dxy distribution between data and bkg
          const float alpha = p4.DeltaPhi(ntt.p4(tki, mpion)); //Alec added
          fill(h_tracks_pt[imass], ntt.pt(tki));
          fill(h_tracks_eta[imass], ntt.eta(tki));
          fill(h_tracks_phi[imass], ntt.phi(tki));
          fill(h_tracks_dxy[imass], ntt.dxybs(tki, nt.bs()));
          fill(h_tracks_absdxy[imass], fabs(ntt.dxybs(tki, nt.bs())));
          fill(h_tracks_dz[imass], ntt.dz(tki));
          fill(h_tracks_dzpv[imass], ntt.dzpv(tki, nt.pvs()));
          fill(h_tracks_nhits[imass], ntt.nhits(tki));
          fill(h_tracks_npxhits[imass], ntt.npxhits(tki));
          fill(h_tracks_nsthits[imass], ntt.nsthits(tki));
          fill(h_tracks_min_r[imass], ntt.min_r(tki));
          fill(h_tracks_npxlayers[imass], ntt.npxlayers(tki));
          fill(h_tracks_nstlayers[imass], ntt.nstlayers(tki));
          fill(h_tracks_nsigmadxy[imass], ntt.nsigmadxybs(tki, nt.bs()));
          fill(h_tracks_dxyerr[imass], ntt.err_dxy(tki));
          fill(h_tracks_dzerr[imass], ntt.err_dz(tki));
          fill(h_tracks_dszerr[imass], ntt.err_dsz(tki));
          fill(h_tracks_lambdaerr[imass], ntt.err_lambda(tki));
          fill(h_tracks_pterr[imass], ntt.err_pt(tki));
          fill(h_tracks_phierr[imass], ntt.err_phi(tki));
          fill(h_tracks_etaerr[imass], ntt.err_eta(tki));
          fill2(h_tracks_dxyerr_v_pt[imass], ntt.pt(tki), ntt.err_dxy(tki));
          fill2(h_tracks_dszerr_v_pt[imass], ntt.pt(tki), ntt.err_dsz(tki));
          //fill2(h_tracks_absdxy_v_pt[imass], ntt.pt(tki), fabs(ntt.dxybs(tki, nt.bs()))); //Alec added from here
          //fill2(h_tracks_absdxy_v_alphapt[imass], ntt.pt(tki)*fabs(alpha), fabs(ntt.dxybs(tki, nt.bs())));
	  fill2(h_tracks_absdxy_v_pt[imass], p4.Pt(), fabs(ntt.dxybs(tki, nt.bs())));
          fill2(h_tracks_absdxy_v_alphapt[imass], p4.Pt()*fabs(std::sin(alpha)), fabs(ntt.dxybs(tki, nt.bs())));
          /*if (fabs(ntt.dxybs(tki, nt.bs()))<.02 && p4.Pt()<2) fill2(h_ptlt2_dxyltp02_tracks_absdxy_v_alphapt[imass], p4.Pt()*fabs(std::sin(alpha)), fabs(ntt.dxybs(tki, nt.bs())));
          if (fabs(ntt.dxybs(tki, nt.bs()))<.02 && p4.Pt()>2 && p4.Pt()<5) fill2(h_ptgt2lt5_dxyltp02_tracks_absdxy_v_alphapt[imass], p4.Pt()*fabs(std::sin(alpha)), fabs(ntt.dxybs(tki, nt.bs())));
          if (fabs(ntt.dxybs(tki, nt.bs()))<.02 && p4.Pt()>5) fill2(h_ptgt5_dxyltp02_tracks_absdxy_v_alphapt[imass], p4.Pt()*fabs(std::sin(alpha)), fabs(ntt.dxybs(tki, nt.bs())));
          if (fabs(ntt.dxybs(tki, nt.bs()))>.02 && fabs(ntt.dxybs(tki, nt.bs()))<.1 && p4.Pt()<2) fill2(h_ptlt2_dxygtp02ltp1_tracks_absdxy_v_alphapt[imass], p4.Pt()*fabs(std::sin(alpha)), fabs(ntt.dxybs(tki, nt.bs())));
          if (fabs(ntt.dxybs(tki, nt.bs()))>.1 && p4.Pt()<2) fill2(h_ptlt2_dxygtp1_tracks_absdxy_v_alphapt[imass], p4.Pt()*fabs(std::sin(alpha)), fabs(ntt.dxybs(tki, nt.bs())));
          if (fabs(ntt.dxybs(tki, nt.bs()))>.02 && fabs(ntt.dxybs(tki, nt.bs()))<.1 && p4.Pt()>2 && p4.Pt()<5) fill2(h_ptgt2lt5_dxygtp02ltp1_tracks_absdxy_v_alphapt[imass], p4.Pt()*fabs(std::sin(alpha)), fabs(ntt.dxybs(tki, nt.bs())));*/
          //Alec to here
        }

        //int mintk;
        int maxtk;
        //float minalpha;
        //float maxalpha;

        if (ntt.dxybs(itk, nt.bs()) < ntt.dxybs(jtk, nt.bs())) {
          //mintk = itk;
          maxtk = jtk;
          //minalpha = p4.DeltaPhi(ntt.p4(mintk, mpion));
          //maxalpha = p4.DeltaPhi(ntt.p4(maxtk, mpion));
        }
        else {
          //mintk = jtk;
          maxtk = itk;
          //minalpha = p4.DeltaPhi(ntt.p4(mintk, mpion));
	  //maxalpha = p4.DeltaPhi(ntt.p4(maxtk, mpion));
        }

	int idxy = dxy_ltp03;  //Alec added from here
	if      (fabs(ntt.dxybs(maxtk, nt.bs()))>.03 && fabs(ntt.dxybs(maxtk, nt.bs()))<.06) idxy = dxy_gtp03ltp06;
	else if (fabs(ntt.dxybs(maxtk, nt.bs()))>.06 && fabs(ntt.dxybs(maxtk, nt.bs()))<.09) idxy = dxy_gtp06ltp09;
	else if (fabs(ntt.dxybs(maxtk, nt.bs()))>.09 && fabs(ntt.dxybs(maxtk, nt.bs()))<.13) idxy = dxy_gtp09ltp13;
        else if (fabs(ntt.dxybs(maxtk, nt.bs()))>.13 && fabs(ntt.dxybs(maxtk, nt.bs()))<.17) idxy = dxy_gtp13ltp17;
        else if (fabs(ntt.dxybs(maxtk, nt.bs()))>.17 && fabs(ntt.dxybs(maxtk, nt.bs()))<.23) idxy = dxy_gtp17ltp23;
        else if (fabs(ntt.dxybs(maxtk, nt.bs()))>.23 && fabs(ntt.dxybs(maxtk, nt.bs()))<.3)  idxy = dxy_gtp23ltp3;
        else if (fabs(ntt.dxybs(maxtk, nt.bs()))>.3)                                        idxy = dxy_gtp3;

        fill(h_mass_bin[imass][iabseta][ipt][idxy], mass);

        /*const float max_alpha = p4.DeltaPhi(ntt.p4(maxtk, mpion));  //add this back in when want to bin in pt*sin(alpha)
        const float pt_sinalpha = pt*fabs(std::sin(max_alpha));
        int ipt = pt_lt0p25;
	if      (pt_sinalpha > 0.25 && pt_sinalpha < 0.45) ipt = pt_gt0p25lt0p45;
	if      (pt_sinalpha > 0.45 && pt_sinalpha < 0.7)  ipt = pt_gt0p45lt0p7;
	else if (pt_sinalpha > 0.7)                        ipt = pt_gt0p7;
        
        fill(h_mass_bin[imass][ipt][idxy], mass);*/

        /*if (fabs(ntt.dxybs(mintk, nt.bs()))<.02 && p4.Pt()<2) fill(h_mass_ptlt2_dxyltp02_pimintrack[imass], mass); //Alec added from here
        if (fabs(ntt.dxybs(mintk, nt.bs()))<.02 && p4.Pt()>2 && p4.Pt()<5) fill(h_mass_ptgt2lt5_dxyltp02_pimintrack[imass], mass);
	if (fabs(ntt.dxybs(mintk, nt.bs()))<.02 && p4.Pt()>5) fill(h_mass_ptgt5_dxyltp02_pimintrack[imass], mass);
        if (fabs(ntt.dxybs(mintk, nt.bs()))>.02 && fabs(ntt.dxybs(mintk, nt.bs()))<.1 && p4.Pt()<2) fill(h_mass_ptlt2_dxygtp02ltp1_pimintrack[imass], mass);
        if (fabs(ntt.dxybs(mintk, nt.bs()))>.1 && p4.Pt()<2) fill(h_mass_ptlt2_dxygtp1_pimintrack[imass], mass);
        if (fabs(ntt.dxybs(mintk, nt.bs()))>.02 && fabs(ntt.dxybs(mintk, nt.bs()))<.1 && p4.Pt()>2 && p4.Pt()<5) fill(h_mass_ptgt2lt5_dxygtp02ltp1_pimintrack[imass], mass);
        if (fabs(ntt.dxybs(maxtk, nt.bs()))<.02 && p4.Pt()<2) fill(h_mass_ptlt2_dxyltp02_pimaxtrack[imass], mass);
        if (fabs(ntt.dxybs(maxtk, nt.bs()))<.02 && p4.Pt()>2 && p4.Pt()<5) fill(h_mass_ptgt2lt5_dxyltp02_pimaxtrack[imass], mass);
        if (fabs(ntt.dxybs(maxtk, nt.bs()))<.02 && p4.Pt()>5) fill(h_mass_ptgt5_dxyltp02_pimaxtrack[imass], mass);
	if (fabs(ntt.dxybs(maxtk, nt.bs()))>.02 && fabs(ntt.dxybs(maxtk, nt.bs()))<.1 && p4.Pt()<2) fill(h_mass_ptlt2_dxygtp02ltp1_pimaxtrack[imass], mass);
        if (fabs(ntt.dxybs(maxtk, nt.bs()))>.1 && p4.Pt()<2) fill(h_mass_ptlt2_dxygtp1_pimaxtrack[imass], mass);
        if (fabs(ntt.dxybs(maxtk, nt.bs()))>.02 && fabs(ntt.dxybs(maxtk, nt.bs()))<.1 && p4.Pt()>2 && p4.Pt()<5) fill(h_mass_ptgt2lt5_dxygtp02ltp1_pimaxtrack[imass], mass);*/

        /*if (fabs(ntt.dxybs(mintk, nt.bs()))<.02 && p4.Pt()<2) fill2(h_ptlt2_dxyltp02_mintracks_absdxy_v_alphapt[imass], p4.Pt()*fabs(std::sin(minalpha)), fabs(ntt.dxybs(mintk, nt.bs())));
	if (fabs(ntt.dxybs(mintk, nt.bs()))<.02 && p4.Pt()>2 && p4.Pt()<5) fill2(h_ptgt2lt5_dxyltp02_mintracks_absdxy_v_alphapt[imass], p4.Pt()*fabs(std::sin(minalpha)), fabs(ntt.dxybs(mintk, nt.bs())));
	if (fabs(ntt.dxybs(mintk, nt.bs()))<.02 && p4.Pt()>5) fill2(h_ptgt5_dxyltp02_mintracks_absdxy_v_alphapt[imass], p4.Pt()*fabs(std::sin(minalpha)), fabs(ntt.dxybs(mintk, nt.bs())));
	if (fabs(ntt.dxybs(mintk, nt.bs()))>.02 && fabs(ntt.dxybs(mintk, nt.bs()))<.1 && p4.Pt()<2) fill2(h_ptlt2_dxygtp02ltp1_mintracks_absdxy_v_alphapt[imass], p4.Pt()*fabs(std::sin(minalpha)), fabs(ntt.dxybs(mintk, nt.bs())));
	if (fabs(ntt.dxybs(mintk, nt.bs()))>.1 && p4.Pt()<2) fill2(h_ptlt2_dxygtp1_mintracks_absdxy_v_alphapt[imass], p4.Pt()*fabs(std::sin(minalpha)), fabs(ntt.dxybs(mintk, nt.bs())));
	if (fabs(ntt.dxybs(mintk, nt.bs()))>.02 && fabs(ntt.dxybs(mintk, nt.bs()))<.1 && p4.Pt()>2 && p4.Pt()<5) fill2(h_ptgt2lt5_dxygtp02ltp1_mintracks_absdxy_v_alphapt[imass], p4.Pt()*fabs(std::sin(minalpha)), fabs(ntt.dxybs(mintk, nt.bs())));
        if (fabs(ntt.dxybs(maxtk, nt.bs()))<.02 && p4.Pt()<2) fill2(h_ptlt2_dxyltp02_maxtracks_absdxy_v_alphapt[imass], p4.Pt()*fabs(std::sin(maxalpha)), fabs(ntt.dxybs(maxtk, nt.bs())));
        if (fabs(ntt.dxybs(maxtk, nt.bs()))<.02 && p4.Pt()>2 && p4.Pt()<5) fill2(h_ptgt2lt5_dxyltp02_maxtracks_absdxy_v_alphapt[imass], p4.Pt()*fabs(std::sin(maxalpha)), fabs(ntt.dxybs(maxtk, nt.bs())));
        if (fabs(ntt.dxybs(maxtk, nt.bs()))<.02 && p4.Pt()>5) fill2(h_ptgt5_dxyltp02_maxtracks_absdxy_v_alphapt[imass], p4.Pt()*fabs(std::sin(maxalpha)), fabs(ntt.dxybs(maxtk, nt.bs())));
        if (fabs(ntt.dxybs(maxtk, nt.bs()))>.02 && fabs(ntt.dxybs(maxtk, nt.bs()))<.1 && p4.Pt()<2) fill2(h_ptlt2_dxygtp02ltp1_maxtracks_absdxy_v_alphapt[imass], p4.Pt()*fabs(std::sin(maxalpha)), fabs(ntt.dxybs(maxtk, nt.bs())));
        if (fabs(ntt.dxybs(maxtk, nt.bs()))>.1 && p4.Pt()<2) fill2(h_ptlt2_dxygtp1_maxtracks_absdxy_v_alphapt[imass], p4.Pt()*fabs(std::sin(maxalpha)), fabs(ntt.dxybs(maxtk, nt.bs())));
        if (fabs(ntt.dxybs(maxtk, nt.bs()))>.02 && fabs(ntt.dxybs(maxtk, nt.bs()))<.1 && p4.Pt()>2 && p4.Pt()<5) fill2(h_ptgt2lt5_dxygtp02ltp1_maxtracks_absdxy_v_alphapt[imass], p4.Pt()*fabs(std::sin(maxalpha)), fabs(ntt.dxybs(maxtk, nt.bs())));*/
        //Alec added to here

        ++nvtx[imass];
      }
    }

    for (int i = 0; i < max_mass_type; ++i)
      fill(h_nvtx[i], nvtx[i]);

    return std::make_pair(true, w);
  };

  nr.loop(fcn);
}
