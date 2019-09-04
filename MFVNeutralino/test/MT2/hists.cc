#include "TH2.h"
#include "JMTucker/MFVNeutralino/interface/Ntuple.h"
#include "JMTucker/Tools/interface/ExtValue.h"
#include "JMTucker/Tools/interface/Math.h"
#include "JMTucker/Tools/interface/NtupleReader.h"
#include "JMTucker/Tools/interface/NtupleViews.h"

int main(int argc, char** argv) {
  jmt::NtupleReader<mfv::MiniNtuple2> nr;
  nr.init_options("mfvMiniTree2/t", "HistsV27mm", "nr_ntuplev27mm");
  if (!nr.parse_options(argc, argv) || !nr.init()) return 1;
  auto& nt = nr.nt();
  auto& bs = nt.bs();
  auto& pvs = nt.pvs();
  auto& jets = nt.jets();
  auto& tks = nt.tracks();
  jmt::RescaledTracksSubNtupleView rtks(tks);
  auto& gen = nt.gentruth();
  //  auto& vs = nt.vertices();

  //////////////////////////////////////////////////////////////////////

  nr.f_out().mkdir("mfvEventHistosNoCuts")->cd();
  
  //  auto h_gen_decay = new TH2F("h_gen_decay", "0-2=e,mu,tau, 3=h;decay code #0;decay code #1", 4, 0, 4, 4, 0, 4);
  auto h_gen_flavor_code = new TH1F("h_gen_flavor_code", ";quark flavor composition;events", 3, 0, 3);

  auto h_nbquarks = new TH1F("h_nbquarks", ";# of bquarks;events", 20, 0, 20);
  auto h_bquark_pt = new TH1F("h_bquark_pt", ";bquarks p_{T} (GeV);bquarks/10 GeV", 100, 0, 1000);
  auto h_bquark_eta = new TH1F("h_bquark_eta", ";bquarks #eta (rad);bquarks/.08", 100, -4, 4);
  auto h_bquark_phi = new TH1F("h_bquark_phi", ";bquarks #phi (rad);bquarks/.063", 100, -3.1416, 3.1416);
  auto h_bquark_energy = new TH1F("h_bquark_energy", ";bquarks energy (GeV);bquarks/10 GeV", 100, 0, 1000);
  auto h_bquark_pairdphi = new TH1F("h_bquark_pairdphi", ";bquark pair #Delta#phi (rad);bquark pairs/.063", 100, -3.1416, 3.1416);

  auto h_minlspdist2d = new TH1F("h_minlspdist2d", ";min dist2d(gen vtx #i) (cm);events/0.1 mm", 200, 0, 2);
  auto h_lspdist2d = new TH1F("h_lspdist2d", ";dist2d(gen vtx #0, #1) (cm);events/0.1 mm", 200, 0, 2);
  auto h_lspdist3d = new TH1F("h_lspdist3d", ";dist3d(gen vtx #0, #1) (cm);events/0.1 mm", 200, 0, 2);

  /*
  auto h_hlt_bits = new TH1F("h_hlt_bits", ";;events", 2*mfv::n_hlt_paths+1, 0, 2*mfv::n_hlt_paths+1);
  auto h_l1_bits  = new TH1F("h_l1_bits",  ";;events", 2*mfv::n_l1_paths +1, 0, 2*mfv::n_l1_paths +1);

  h_hlt_bits->GetXaxis()->SetBinLabel(1, "nevents");
  for (int i = 0; i < mfv::n_hlt_paths; ++i) {
    h_hlt_bits->GetXaxis()->SetBinLabel(1+2*i+1, TString::Format("found %s", mfv::hlt_paths[i]));
    h_hlt_bits->GetXaxis()->SetBinLabel(1+2*i+2, TString::Format(" pass %s", mfv::hlt_paths[i]));
  }
  h_l1_bits->GetXaxis()->SetBinLabel(1, "nevents");
  for (int i = 0; i < mfv::n_l1_paths; ++i) {
    h_l1_bits->GetXaxis()->SetBinLabel(1+2*i+1, TString::Format("found %s", mfv::l1_paths[i]));
    h_l1_bits->GetXaxis()->SetBinLabel(1+2*i+2, TString::Format(" pass %s", mfv::l1_paths[i]));
  }
  */

  auto h_bsx = new TH1F("h_bsx", ";beamspot x (cm);events/10 #mum", 200, -0.1, 0.1);
  auto h_bsy = new TH1F("h_bsy", ";beamspot y (cm);events/10 #mum", 200, -0.1, 0.1);
  auto h_bsz = new TH1F("h_bsz", ";beamspot z (cm);events/400 #mum", 200, -4, 4);
  auto h_bsphi = new TH1F("h_bsphi", ";beamspot #phi (rad);events/.063", 100, -3.1416, 3.1416);

  auto h_npv = new TH1F("h_npv", ";# of primary vertices;events", 120, 0, 120);
  TH1F* h_pvx[2];
  TH1F* h_pvy[2];
  TH1F* h_pvz[2];
  TH1F* h_pvxwide[2];
  TH1F* h_pvywide[2];
  TH1F* h_pvrho[2];
  TH1F* h_pvrhowide[2];
  TH1F* h_pvphi[2];
  TH1F* h_pvcxx[2];
  TH1F* h_pvcyy[2];
  TH1F* h_pvczz[2];
  TH1F* h_pvcxy[2];
  TH1F* h_pvcxz[2];
  TH1F* h_pvcyz[2];
  TH1F* h_pvntracks[2];
  TH1F* h_pvscore[2];
  for (int i = 0; i < 2; ++i) {
    TString ex  = i == 1 ? "s" : "";
    TString ex2 = i == 1 ? "ices" : "ex";
    h_pvx[i] = new TH1F("h_pv" + ex + "x", ";primary vert" + ex2 + " x, beamspot-subtracted (cm);events/2 #mum", 200, -0.02, 0.02);
    h_pvy[i] = new TH1F("h_pv" + ex + "y", ";primary vert" + ex2 + " y, beamspot-subtracted (cm);events/2 #mum", 200, -0.02, 0.02);
    h_pvz[i] = new TH1F("h_pv" + ex + "z", ";primary vert" + ex2 + " z, beamspot-subtracted (cm);events/3.6 mm", 200, -18, 18);
    h_pvxwide[i] = new TH1F("h_pv" + ex + "xwide", ";primary vert" + ex2 + " x, beamspot-subtracted (cm);events/40 #mum", 50, -0.1, 0.1);
    h_pvywide[i] = new TH1F("h_pv" + ex + "ywide", ";primary vert" + ex2 + " y, beamspot-subtracted (cm);events/40 #mum", 50, -0.1, 0.1);
    h_pvrho[i] = new TH1F("h_pv" + ex + "rho", ";primary vert" + ex2 + " rho (cm);events/5 #mum", 40, 0, 0.02);
    h_pvrhowide[i] = new TH1F("h_pv" + ex + "rhowide", ";primary vert" + ex2 + " rho (cm);events/10 #mum", 100, 0, 0.1);
    h_pvphi[i] = new TH1F("h_pv" + ex + "phi", ";primary vert" + ex2 + " #phi, beamspot-subtracted (rad);events/.063", 100, -3.1416, 3.1416);
    h_pvcxx[i] = new TH1F("h_pv" + ex + "cxx", ";primary vert" + ex2 + " cxx;events", 100, 0, 5e-6);
    h_pvcyy[i] = new TH1F("h_pv" + ex + "cyy", ";primary vert" + ex2 + " cyy;events", 100, 0, 5e-6);
    h_pvczz[i] = new TH1F("h_pv" + ex + "czz", ";primary vert" + ex2 + " czz;events", 100, 0, 1e-5);
    h_pvcxy[i] = new TH1F("h_pv" + ex + "cxy", ";primary vert" + ex2 + " cxy;events", 100, -1e-6, 1e-6);
    h_pvcxz[i] = new TH1F("h_pv" + ex + "cxz", ";primary vert" + ex2 + " cxz;events", 100, -1e-6, 1e-6);
    h_pvcyz[i] = new TH1F("h_pv" + ex + "cyz", ";primary vert" + ex2 + " cyz;events", 100, -1e-6, 1e-6);
    h_pvntracks[i] = new TH1F("h_pv" + ex + "ntracks", ";# of tracks in primary vert" + ex2 + ";events/3", 100, 0, 300);
    h_pvscore[i] = new TH1F("h_pv" + ex + "score", ";primary vert" + ex2 + " #Sigma p_{T}^{2} (GeV^{2});events/10000 GeV^{2}", 100, 0, 1e6);
  }
  auto h_pvsdz = new TH1F("h_pvsdz", ";primary vertices pairs #delta z (cm);events/2 mm", 100, 0, 20);
  auto h_pvsdz_minscore = new TH1F("h_pvsdz_minscore", ";primary vertices pairs (with score req) #delta z (cm);events/2 mm", 100, 0, 20);
  auto h_pvsmindz = new TH1F("h_pvsmindz", ";min primary vertices pairs #delta z (cm);events/0.5 mm", 100, 0, 5);
  auto h_pvsmaxdz = new TH1F("h_pvmaxdz", ";max primary vertices pairs #delta z (cm);events/2 mm", 100, 0, 20);
  auto h_pvsmindz_minscore = new TH1F("h_pvmindz_minscore", ";min primary vertices pairs (with score req) #delta z (cm);events/1 mm", 100, 0, 10);
  auto h_pvsmaxdz_minscore = new TH1F("h_pvmaxdz_minscore", ";max primary vertices pairs (with score req) #delta z (cm);events/1 mm", 100, 0, 10);

  auto h_njets = new TH1F("h_njets", ";# of jets;events", 30, 0, 30);
  auto h_njets20 = new TH1F("h_njets20", ";# of jets w. p_{T}  20 GeV;events", 20, 0, 20);
  const int max_njets = 10;
  TH1F* h_jet_pt[max_njets+1];
  TH1F* h_jet_eta[max_njets+1];
  TH1F* h_jet_phi[max_njets+1];
  TH1F* h_jet_energy[max_njets+1];
  for (int i = 0; i < max_njets+1; ++i) {
    TString ex = i == max_njets ? TString("all") : TString::Format("%i", i);
    h_jet_pt [i] = new TH1F("h_jet_pt_"  + ex, ";p_{T} of jet " + ex + " (GeV);events/10 GeV", 200, 0, 2000);
    h_jet_eta[i] = new TH1F("h_jet_eta_" + ex, ";#eta of jet "  + ex + " (GeV);events/0.05", 120, -3, 3);
    h_jet_phi[i] = new TH1F("h_jet_phi_" + ex, ";#phi of jet "  + ex + " (GeV);events/0.063", 100, -3.1416, 3.1416);
    h_jet_energy[i] = new TH1F("h_jet_energy_" + ex, ";jets energy (GeV);jets/10 GeV", 200, 0, 2000);
  }
  auto h_jet_ht = new TH1F("h_jet_ht", ";H_{T} of jets (GeV);events/25 GeV", 200, 0, 5000);
  auto h_jet_ht_40 = new TH1F("h_jet_ht_40", ";H_{T} of jets with p_{T}  40 GeV;events/25 GeV", 200, 0, 5000);

  auto h_jet_pairdphi = new TH1F("h_jet_pairdphi", ";jet pair #Delta#phi (rad);jet pairs/.063", 100, -3.1416, 3.1416);
  auto h_jet_pairdr = new TH1F("h_jet_pairdr", ";jet pair #DeltaR (rad);jet pairs/.063", 100, 0, 6.3);

  TH1F* h_n_vertex_seed_tracks[2];
  TH1F* h_vertex_seed_track_chi2dof[2];
  TH1F* h_vertex_seed_track_q[2];
  TH1F* h_vertex_seed_track_pt[2];
  TH1F* h_vertex_seed_track_eta[2];
  TH1F* h_vertex_seed_track_phi[2];
  TH2F* h_vertex_seed_track_phi_v_eta[2];
  TH1F* h_vertex_seed_track_dxy[2];
  TH1F* h_vertex_seed_track_dxybs[2];
  TH1F* h_vertex_seed_track_dxypv[2];
  TH1F* h_vertex_seed_track_dz[2];
  TH1F* h_vertex_seed_track_dzpv[2];
  TH1F* h_vertex_seed_track_err_pt[2];
  TH1F* h_vertex_seed_track_err_eta[2];
  TH1F* h_vertex_seed_track_err_phi[2];
  TH1F* h_vertex_seed_track_err_dxy[2];
  TH1F* h_vertex_seed_track_err_dz[2];
  TH1F* h_vertex_seed_track_npxhits[2];
  TH1F* h_vertex_seed_track_nsthits[2];
  TH1F* h_vertex_seed_track_nhits[2];
  TH1F* h_vertex_seed_track_npxlayers[2];
  TH1F* h_vertex_seed_track_nstlayers[2];
  TH1F* h_vertex_seed_track_nlayers[2];

  for (int i = 0; i < 2; ++i) {
    TString ex  = i == 1 ? "_rescale" : "";
    TString ex2 = i == 1 ? " (rescaled)" : "";
    h_n_vertex_seed_tracks[i] = new TH1F("h_n_vertex_seed_tracks" + ex, ";# vertex seed tracks" + ex2 + ";events", 100, 0, 100);
    h_vertex_seed_track_chi2dof[i] = new TH1F("h_vertex_seed_track_chi2dof" + ex, ";vertex seed track" + ex2 + " #chi^{2}/dof;tracks/1", 10, 0, 10);
    h_vertex_seed_track_q[i] = new TH1F("h_vertex_seed_track_q" + ex, ";vertex seed track" + ex2 + " charge;tracks", 3, -1, 2);
    h_vertex_seed_track_pt[i] = new TH1F("h_vertex_seed_track_pt" + ex, ";vertex seed track" + ex2 + " p_{T} (GeV);tracks/GeV", 300, 0, 300);
    h_vertex_seed_track_eta[i] = new TH1F("h_vertex_seed_track_eta" + ex, ";vertex seed track" + ex2 + " #eta;tracks/0.052", 100, -2.6, 2.6);
    h_vertex_seed_track_phi[i] = new TH1F("h_vertex_seed_track_phi" + ex, ";vertex seed track" + ex2 + " #phi;tracks/0.063", 100, -3.15, 3.15);
    h_vertex_seed_track_phi_v_eta[i] = new TH2F("h_vertex_seed_track_phi_v_eta" + ex, ";vertex seed track" + ex2 + " #eta;vertex seed track" + ex2 + " #phi", 26, -2.6, 2.6, 24, -M_PI, M_PI);
    h_vertex_seed_track_dxy[i] = new TH1F("h_vertex_seed_track_dxy" + ex, ";vertex seed track" + ex2 + " dxy (cm);tracks/10 #mum", 200, -0.1, 0.1);
    h_vertex_seed_track_dxybs[i] = new TH1F("h_vertex_seed_track_dxybs" + ex, ";vertex seed track" + ex2 + " dxy wrt BS (cm);tracks/10 #mum", 200, -0.1, 0.1);
    h_vertex_seed_track_dxypv[i] = new TH1F("h_vertex_seed_track_dxypv" + ex, ";vertex seed track" + ex2 + " dxy wrt PV (cm);tracks/10 #mum", 200, -0.1, 0.1);
    h_vertex_seed_track_dz[i] = new TH1F("h_vertex_seed_track_dz" + ex, ";vertex seed track" + ex2 + " dz (cm);tracks/10 #mum", 200, -0.1, 0.1);
    h_vertex_seed_track_dzpv[i] = new TH1F("h_vertex_seed_track_dzpv" + ex, ";vertex seed track" + ex2 + " dz wrt PV (cm);tracks/10 #mum", 200, -0.1, 0.1);
    h_vertex_seed_track_err_pt[i] = new TH1F("h_vertex_seed_track_err_pt" + ex, ";vertex seed track" + ex2 + " #sigma(p_{T})/p_{T} (GeV);tracks/0.005", 100, 0, 0.5);
    h_vertex_seed_track_err_eta[i] = new TH1F("h_vertex_seed_track_err_eta" + ex, ";vertex seed track" + ex2 + " #sigma(#eta);tracks/5e-5", 100, 0, 0.005);
    h_vertex_seed_track_err_phi[i] = new TH1F("h_vertex_seed_track_err_phi" + ex, ";vertex seed track" + ex2 + " #sigma(#phi);tracks/5e-5", 100, 0, 0.005);
    h_vertex_seed_track_err_dxy[i] = new TH1F("h_vertex_seed_track_err_dxy" + ex, ";vertex seed track" + ex2 + " #sigma(dxy) (cm);tracks/3 #mum", 100, 0, 0.03);
    h_vertex_seed_track_err_dz[i] = new TH1F("h_vertex_seed_track_err_dz" + ex, ";vertex seed track" + ex2 + " #sigma(dz) (cm);tracks/15 #mum", 100, 0, 0.15);
    h_vertex_seed_track_npxhits[i] = new TH1F("h_vertex_seed_track_npxhits" + ex, ";vertex seed track" + ex2 + " # pixel hits;tracks", 10, 0, 10);
    h_vertex_seed_track_nsthits[i] = new TH1F("h_vertex_seed_track_nsthits" + ex, ";vertex seed track" + ex2 + " # strip hits;tracks", 50, 0, 50);
    h_vertex_seed_track_nhits[i] = new TH1F("h_vertex_seed_track_nhits" + ex, ";vertex seed track" + ex2 + " # hits;tracks", 60, 0, 60);
    h_vertex_seed_track_npxlayers[i] = new TH1F("h_vertex_seed_track_npxlayers" + ex, ";vertex seed track" + ex2 + " # pixel layers;tracks", 10, 0, 10);
    h_vertex_seed_track_nstlayers[i] = new TH1F("h_vertex_seed_track_nstlayers" + ex, ";vertex seed track" + ex2 + " # strip layers;tracks", 20, 0, 20);
    h_vertex_seed_track_nlayers[i] = new TH1F("h_vertex_seed_track_nlayers" + ex, ";vertex seed track" + ex2 + " # layers;tracks", 30, 0, 30);
  }

  /* auto h_met = new TH1F("h_met", ";MET (GeV);events/5 GeV", 100, 0, 500);
  auto h_metphi = new TH1F("h_metphi", ";MET #phi (rad);events/.063", 100, -3.1416, 3.1416);

  const char* lmt_ex[3] = {"loose", "medium", "tight"};
  TH1F* h_nbtags[3];
  TH2F* h_nbtags_v_bquark_code[3];
  for (int i = 0; i < 3; ++i) {
    h_nbtags[i] = new TH1F(TString::Format("h_nbtags_%i", i), TString::Format(";# of %s b tags;events", lmt_ex[i]), 10, 0, 10);
    h_nbtags_v_bquark_code[i] = new TH2F(TString::Format("h_nbtags_v_bquark_code_%i", i), TString::Format(";bquark code;# of %s b tags", lmt_ex[i]), 3, 0, 3, 3, 0, 3);
  }
  auto h_jet_bdisc = new TH1F("h_jet_bdisc", ";jets' b discriminator;jets/0.02", 51, 0, 1.02);
  auto h_jet_bdisc_v_bquark_code = new TH2F("h_jet_bdisc_v_bquark_code", ";b quark code;jets' b discriminator", 3, 0, 3, 51, 0, 1.02);
  auto h_bjet_pt = new TH1F("h_bjet_pt", ";bjets p_{T} (GeV);bjets/10 GeV", 150, 0, 1500);
  auto h_bjet_eta = new TH1F("h_bjet_eta", ";bjets #eta (rad);bjets/.05", 120, -3, 3);
  auto h_bjet_phi = new TH1F("h_bjet_phi", ";bjets #phi (rad);bjets/.063", 100, -3.1416, 3.1416);
  auto h_bjet_energy = new TH1F("h_bjet_energy", ";bjets E (GeV);bjets/10 GeV", 150, 0, 1500);
  auto h_bjet_pairdphi = new TH1F("h_bjet_pairdphi", ";bjet pair #Delta#phi (rad);bjet pairs/.063", 100, -3.1416, 3.1416);

  const char* lep_ex[2] = {"any", "selected"};
  const char* lep_kind[2] = {"muon", "electron"};
  TH1F* h_nmuons[2];
  TH1F* h_nelectrons[2];
  TH1F* h_nleptons[2];
  TH1F* h_leptons_pt[2][2];
  TH1F* h_leptons_eta[2][2];
  TH1F* h_leptons_phi[2][2];
  TH1F* h_leptons_dxy[2][2];
  TH1F* h_leptons_dxybs[2][2];
  TH1F* h_leptons_dz[2][2];
  TH1F* h_leptons_iso[2][2];
  for (int i = 0; i < 2; ++i) {
    h_nmuons[i] = new TH1F(TString::Format("h_nmuons_%s", lep_ex[i]), TString::Format(";# of %s muons;events", lep_ex[i]), 5, 0, 5);
    h_nelectrons[i] = new TH1F(TString::Format("h_nelectrons_%s", lep_ex[i]), TString::Format(";# of %s electrons;events", lep_ex[i]), 5, 0, 5);
    h_nleptons[i] = new TH1F(TString::Format("h_nleptons_%s", lep_ex[i]), TString::Format(";# of %s leptons;events", lep_ex[i]), 5, 0, 5);
    for (int j = 0; j < 2; ++j) {
      h_leptons_pt   [j][i] = new TH1F(TString::Format("h_%s_%s_pt",    lep_kind[j], lep_ex[i]), TString::Format(";%s %s p_{T} (GeV);%ss/5 GeV",     lep_ex[i], lep_kind[j], lep_kind[j]), 40, 0, 200);
      h_leptons_eta  [j][i] = new TH1F(TString::Format("h_%s_%s_eta",   lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #eta (rad);%ss/.104",      lep_ex[i], lep_kind[j], lep_kind[j]), 50, -2.6, 2.6);
      h_leptons_phi  [j][i] = new TH1F(TString::Format("h_%s_%s_phi",   lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #phi (rad);%ss/.126",      lep_ex[i], lep_kind[j], lep_kind[j]), 50, -3.1416, 3.1416);
      h_leptons_dxy  [j][i] = new TH1F(TString::Format("h_%s_%s_dxy",   lep_kind[j], lep_ex[i]), TString::Format(";%s %ss dxy(PV) (cm);%ss/50 #mum", lep_ex[i], lep_kind[j], lep_kind[j]), 200, -0.5, 0.5);
      h_leptons_dxybs[j][i] = new TH1F(TString::Format("h_%s_%s_dxybs", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss dxy(BS) (cm);%ss/50 #mum", lep_ex[i], lep_kind[j], lep_kind[j]), 200, -0.5, 0.5);
      h_leptons_dz   [j][i] = new TH1F(TString::Format("h_%s_%s_dz",   lep_kind[j], lep_ex[i]), TString::Format(";%s %ss dz (cm);%ss/50 #mum",       lep_ex[i], lep_kind[j], lep_kind[j]), 200, -0.5, 0.5);
      h_leptons_iso  [j][i] = new TH1F(TString::Format("h_%s_%s_iso",   lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%ss/.04",       lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    }
  } */

  //////////////////////////////////////////////////////////////////////

  nr.loop([&]() {
      rtks.setup(nt.base());

      //h_gen_decay->Fill(mevent->gen_decay_type[0], mevent->gen_decay_type[1], w);
      nr.fill(h_gen_flavor_code, gen.flavor_code());
      nr.fill(h_nbquarks, gen.nbquarks());
      for (int i = 0, ie = gen.nbquarks(); i < ie; ++i) {
        nr.fill(h_bquark_pt, gen.bquark_pt(i));
        nr.fill(h_bquark_eta, gen.bquark_eta(i));
        nr.fill(h_bquark_phi, gen.bquark_phi(i));
        nr.fill(h_bquark_energy, gen.bquark_p4(i).E());
        for (int j = i+1, je = gen.nbquarks(); j < je; ++j) {
          nr.fill(h_bquark_pairdphi, jmt::dphi(gen.bquark_phi(i), gen.bquark_phi(j)));
        }
      }
      nr.fill(h_minlspdist2d, gen.minlspdist2());
      nr.fill(h_lspdist2d, gen.lspdist2());
      nr.fill(h_lspdist3d, gen.lspdist3());

      ////

      /*nr.fill(h_hlt_bits, 0);
      nr.fill(h_l1_bits, 0);
      for (int i = 0; i < mfv::n_hlt_paths; ++i) {
        if (found_hlt(i)) nr.fill(h_hlt_bits, 1+2*i);
        if (pass_hlt (i)) nr.fill(h_hlt_bits, 1+2*i+1);
      }
      for (int i = 0; i < mfv::n_l1_paths; ++i) {
        if (found_l1(i)) nr.fill(h_l1_bits, 1+2*i);
        if (pass_l1 (i)) nr.fill(h_l1_bits, 1+2*i+1);
      } */

      ////

      nr.fill(h_bsx, bs.x());
      nr.fill(h_bsy, bs.y());
      nr.fill(h_bsz, bs.z());
      nr.fill(h_bsphi, bs.phi());

      nr.fill(h_npv, pvs.n());

      jmt::MinValue minpvdz, minpvdz_minscore;
      jmt::MaxValue maxpvdz, maxpvdz_minscore;
      for (int i = 0, ie = pvs.n(); i < ie; ++i) {
        for (int j : {0,1}) {
          if (j == 0 && i > 0) continue;
          for (auto h : { h_pvx[j], h_pvxwide[j] }) nr.fill(h, pvs.x(i));
          for (auto h : { h_pvy[j], h_pvywide[j] }) nr.fill(h, pvs.y(i));
          nr.fill(h_pvz[j], pvs.z(i));
          for (auto h : { h_pvrho[j], h_pvrhowide[j] }) nr.fill(h, pvs.rho(i));
          nr.fill(h_pvphi[j], pvs.phi(i));
          nr.fill(h_pvcxx[j], pvs.cxx(i));
          nr.fill(h_pvcxy[j], pvs.cxy(i));
          nr.fill(h_pvcxz[j], pvs.cxz(i));
          nr.fill(h_pvcyy[j], pvs.cyy(i));
          nr.fill(h_pvcyz[j], pvs.cyz(i));
          nr.fill(h_pvczz[j], pvs.czz(i));
          nr.fill(h_pvntracks[j], pvs.ntracks(i));
          nr.fill(h_pvscore[j], pvs.score(i));
        }

        for (int j = i+1, je = pvs.n(); j < je; ++j) {
          const float dz = fabs(pvs.z(i) - pvs.z(j));
          nr.fill(h_pvsdz, dz);
          minpvdz(dz), maxpvdz(dz);
          if (pvs.score(i) > 50e3 && pvs.score(j) > 50e3) {
            nr.fill(h_pvsdz_minscore, dz);
            minpvdz_minscore(dz), maxpvdz_minscore(dz);
          }
        }
      }
      nr.fill(h_pvsmindz, minpvdz);
      nr.fill(h_pvsmaxdz, maxpvdz);
      nr.fill(h_pvsmindz_minscore, minpvdz_minscore);
      nr.fill(h_pvsmaxdz_minscore, maxpvdz_minscore);

      ////

      nr.fill(h_njets, jets.n());
      nr.fill(h_njets20, jets.nminpt(20));
      for (int i = 0, ie = std::min(max_njets, jets.n()); i < ie; ++i) {
        for (int j : {i, max_njets}) {
          nr.fill(h_jet_pt[j], jets.pt(i));
          nr.fill(h_jet_eta[j], jets.eta(i));
          nr.fill(h_jet_phi[j], jets.phi(i));
          nr.fill(h_jet_energy[j], jets.energy(i));
        }
      }
      nr.fill(h_jet_ht, jets.ht(20));
      nr.fill(h_jet_ht_40, jets.ht(40));

      for (int i = 0, ie = jets.n(); i < ie; ++i) {
        for (int j = i+1, je = jets.n(); j < je; ++j) {
          nr.fill(h_jet_pairdphi, jmt::dphi(jets.phi(i), jets.phi(j)));
          nr.fill(h_jet_pairdr, jmt::dR(jets.eta(i), jets.phi(i), jets.eta(j), jets.phi(j)));
        }
      }

      ////

      for (int j : {0,1}) {
        int n_vertex_seed_tracks = 0;
        rtks.scaling(j == 1);
        for (int i = 0, ie = tks.n(); i < ie; ++i) {
          if (!rtks.pass_seed(i, bs))
            continue;

          ++n_vertex_seed_tracks;
          nr.fill(h_vertex_seed_track_chi2dof[j], rtks.chi2dof(i));
          nr.fill(h_vertex_seed_track_q[j], rtks.q(i));
          nr.fill(h_vertex_seed_track_pt[j], rtks.pt(i));
          nr.fill(h_vertex_seed_track_eta[j], rtks.eta(i));
          nr.fill(h_vertex_seed_track_phi[j], rtks.phi(i));
          nr.fill(h_vertex_seed_track_phi_v_eta[j], rtks.eta(i), rtks.phi(i));
          nr.fill(h_vertex_seed_track_dxy[j], rtks.dxy(i));
          nr.fill(h_vertex_seed_track_dxybs[j], rtks.dxybs(i, bs));
          nr.fill(h_vertex_seed_track_dxypv[j], rtks.dxypv(i, pvs));
          nr.fill(h_vertex_seed_track_dz[j], rtks.dz(i));
          nr.fill(h_vertex_seed_track_dzpv[j], rtks.dzpv(i, pvs));
          nr.fill(h_vertex_seed_track_err_pt[j], rtks.err_pt_rel(i));
          nr.fill(h_vertex_seed_track_err_eta[j], rtks.err_eta(i));
          nr.fill(h_vertex_seed_track_err_phi[j], rtks.err_phi(i));
          nr.fill(h_vertex_seed_track_err_dxy[j], rtks.err_dxy(i));
          nr.fill(h_vertex_seed_track_err_dz[j], rtks.err_dz(i));
          nr.fill(h_vertex_seed_track_npxhits[j], rtks.npxhits(i));
          nr.fill(h_vertex_seed_track_nsthits[j], rtks.nsthits(i));
          nr.fill(h_vertex_seed_track_nhits[j], rtks.nhits(i));
          nr.fill(h_vertex_seed_track_npxlayers[j], rtks.npxlayers(i));
          nr.fill(h_vertex_seed_track_nstlayers[j], rtks.nstlayers(i));
          nr.fill(h_vertex_seed_track_nlayers[j], rtks.nlayers(i));
        }
        nr.fill(h_n_vertex_seed_tracks[j], n_vertex_seed_tracks);
      }

      ////
      /*
      for (int i = 0; i < 2; ++i) {
        nr.fill(h_nmuons[i], nmu(i));
        nr.fill(h_nelectrons[i], nel(i));
        nr.fill(h_nleptons[i], nlep(i));
      }

      for (size_t ilep = 0; ilep < nlep(); ++ilep) {
        const size_t j = is_electron(ilep);
        for (size_t i = 0; i < 2; ++i)
          if (i == 0 || pass_lep_sel(ilep)) {
            nr.fill(h_leptons_pt[j][i], lep_pt(ilep));
            nr.fill(h_leptons_eta[j][i], lep_eta[ilep]);
            nr.fill(h_leptons_phi[j][i], lep_phi[ilep]);
            nr.fill(h_leptons_dxy[j][i], lep_dxy[ilep]);
            nr.fill(h_leptons_dxybs[j][i], lep_dxybs[ilep]);
            nr.fill(h_leptons_dz[j][i], lep_dz[ilep]);
            nr.fill(h_leptons_iso[j][i], lep_iso[ilep]);
          }
      }

      nr.fill(h_met, met());
      nr.fill(h_metphi, metphi());

      for (int i = 0; i < 3; ++i) {
        nr.fill(h_nbtags[i], nbtags(i));
        nr.fill(h_nbtags_v_bquark_code[i], gen_flavor_code, nbtags(i));
      }
      const int ibtag = 2; // tight only
      for (size_t ijet = 0; ijet < jet_id.size(); ++ijet) {
        if (jet_pt[ijet] < mfv::min_jet_pt)
          continue;
        nr.fill(h_jet_bdisc, jet_bdisc[ijet]);
        nr.fill(h_jet_bdisc_v_bquark_code, gen_flavor_code, jet_bdisc[ijet]);
        if (is_btagged(ijet, ibtag)) {
          nr.fill(h_bjet_pt, jet_pt[ijet]);
          nr.fill(h_bjet_eta, jet_eta[ijet]);
          nr.fill(h_bjet_phi, jet_phi[ijet]);
          nr.fill(h_bjet_energy, jet_energy[ijet]);
          for (size_t jjet = ijet+1; jjet < jet_id.size(); ++jjet) {
            if (jet_pt[jjet] < mfv::min_jet_pt)
              continue;
            if (is_btagged(jjet, ibtag)) {
              nr.fill(h_bjet_pairdphi, reco::deltaPhi(jet_phi[ijet], jet_phi[jjet]));
            }
          }
        }
      }

      //////////////////////////////////////////////////////////////////////////////
      */

      NR_loop_continue;
    });
}
