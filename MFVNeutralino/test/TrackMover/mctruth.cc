#include "utils.h"

int main(int argc, char** argv) {
  double min_lspdist3 = 0.02;

  jmt::NtupleReader<mfv::MovedTracksNtuple> nr;
  namespace po = boost::program_options;
  nr.init_options("mfvMovedTreeMCTruth/t", "TrackMoverMCTruthHistsV27_GenFSmv2", "nr_trackmovermctruthv27_genfsmv2")
    ("min-lspdist3", po::value<double>(&min_lspdist3)->default_value(0.02), "min distance between LSP decays to use event")
    ;

  if (!nr.parse_options(argc, argv)) return 1;
  std::cout << " min_lspdist3: " << min_lspdist3 << "\n";

  if (!nr.init()) return 1;
  auto& nt = nr.nt();
  auto& bs = nt.bs();
  auto& pvs = nt.pvs();
  auto& jets = nt.jets();
  auto& tks = nt.tracks();
  auto& gen = nt.gentruth();
  auto& vs = nt.vertices();

  ////

  const int num_numdens = 3;
  const bool dijet      = true;

  numdens nds[num_numdens] = {
    numdens("nocuts"),
    numdens("ntracks"),
    numdens("all")
  };

  enum { k_decay_x, k_decay_y, k_decay_z, k_decay_xy, k_lspdist2, k_lspdist3, k_lspdistz, k_movedist2, k_movedist3, k_lspeta,k_lsppt, k_npv, k_pvz, k_pvrho, k_pvntracks, k_pvscore, k_ht, k_jet_asymm, k_jetpt0_asymm, k_jetpt1_asymm, k_jeteta0_asymm, k_jeteta1_asymm, k_jetdr_asymm, k_jetdrmax, k_jetdravg, k_angle0, k_angle1, k_angle2, k_dphi_j0_mv, k_dphi_j1_mv, k_dphi_j2_mv, k_deta_j0_mv, k_deta_j1_mv, k_deta_j2_mv, k_dphi_q0_mv, k_dphi_q1_mv, k_dphi_q2_mv, k_jetdphimax, k_jetdphiavg, k_jetdetamax, k_jetdetaavg,  k_qrkdphimax, k_qrkdphiavg, k_jetdphi_mveta, k_pt0, k_pt1, k_pt2, k_ntks_j0, k_ntks_j1, k_ntks_j2, k_ip_seedtk_dxysig, k_ip_seedtk_dzsig, k_ip_seedtk_sigs, k_ip_seedtk_2D_sumsigs, k_ip_seedtk_2D_dxysigs, k_ip_seedtk_2D_dzsigs, k_ip_seedtk_1D_sumsig, k_closeseedtks, k_miscseedtks, k_closeseedtks_dbv};

  for (numdens& nd : nds) {
    nd.book(k_decay_x,  "decay_x" , ";SV Decay X-pos [cm]; arb. units", 100, -4, 4);
    nd.book(k_decay_y,  "decay_y" , ";SV Decay Y-pos [cm]; arb. units", 100, -4, 4);
    nd.book(k_decay_z,  "decay_z" , ";SV Decay Z-pos [cm]; arb. units", 100, -20, 20);
    nd.book(k_decay_xy, "decay_xy" , ";SV Decay X-pos [cm]; SV Decay Y-pos [cm]", 100, -10, 10, 100, -10, 10);
    nd.book(k_lspdist2, "lspdist2", ";2-dist between gen verts;events/0.01 cm", 200, 0, 2);
    nd.book(k_lspdist3, "lspdist3", ";3-dist between gen verts;events/0.01 cm", 200, 0, 2);
    nd.book(k_lspdistz, "lspdistz", ";z-dist between gen verts;events/0.01 cm", 200, 0, 2);
    nd.book(k_movedist2, "movedist2", ";movement 2-dist;events/bin", 200, 0, 2);
    nd.book(k_movedist3, "movedist3", ";movement 3-dist;events/bin", 200, 0, 2);
    nd.book(k_lspeta,    "movevectoreta"   , ";abs. move vector eta;events/bin", 50, 0, 4);
    nd.book(k_lsppt,     "lsppt"    , ";Pt of LSP [GeV];events/bin", 50, 0, 1000);
    nd.book(k_npv, "npv", ";# PV;events/bin", 50, 0, 100);
    nd.book(k_pvz, "pvz", ";PV z (cm);events/0.24 cm", 200, -24, 24);
    nd.book(k_pvrho, "pvrho", ";PV #rho (cm);events/bin", 50, 0, 0.02);
    nd.book(k_pvntracks, "pvntracks", ";PV # tracks;events/bin", 50, 0, 400);
    nd.book(k_pvscore, "pvscore", ";PV #Sigma p_{T}^{2} (GeV^{2});events/bin", 50, 0, 40000);
    nd.book(k_ht, "ht", ";#Sigma H_{T} (GeV);events/50 GeV", 50, 0, 2500);
    nd.book(k_jet_asymm, "jet_asymm", ";Jet asymmetry A_{J}; arb. units", 25, 0, 1);
    nd.book(k_jetpt0_asymm, "jetpt0_asymm", ";jet p_{T} 0; jet asymm. A_{J}", 50, 0, 1000, 25, 0, 1);
    nd.book(k_jetpt1_asymm, "jetpt1_asymm", ";jet p_{T} 1; jet asymm. A_{J}", 50, 0, 1000, 25, 0, 1);
    nd.book(k_jeteta0_asymm, "jeteta0_asymm", ";jet #eta 0; jet asymm. A_{J}", 100, -4, 4, 25, 0, 1);
    nd.book(k_jeteta1_asymm, "jeteta1_asymm", ";jet #eta 1; jet asymm. A_{J}", 100, -4, 4, 25, 0, 1);
    nd.book(k_jetdr_asymm, "jetdr_asymm", ";jets #DeltaR; jet asymm. A_{J}", 70, 0, 7, 25, 0, 1);
    nd.book(k_jetdrmax, "jetdrmax", ";max jet #Delta R;events/0.1", 35, 0, 7);
    nd.book(k_jetdravg, "jetdravg", ";avg jet #Delta R;events/0.1", 35, 0, 7);
    nd.book(k_angle0, "jetmovea3d0", ";Angle between jet0 and SV;arb. units", 63, 0, M_PI);
    nd.book(k_angle1, "jetmovea3d1", ";Angle between jet1 and SV;arb. units", 63, 0, M_PI);
    nd.book(k_angle2, "jetmovea3d2", ";Angle between jet1 and SV;arb. units", 63, 0, M_PI);
    nd.book(k_dphi_j0_mv, "dphi_j0_mv", ";abs #Delta #phi between jet0 and move vec;events/bin", 63, 0, M_PI);
    nd.book(k_dphi_j1_mv, "dphi_j1_mv", ";abs #Delta #phi between jet1 and move vec;events/bin", 63, 0, M_PI);
    nd.book(k_dphi_j2_mv, "dphi_j2_mv", ";abs #Delta #phi between jet2 and move vec;events/bin", 63, 0, M_PI);
    nd.book(k_deta_j0_mv, "deta_j0_mv", ";abs #Delta #eta between jet0 and move vec;events/bin", 25, 0, 4);
    nd.book(k_deta_j1_mv, "deta_j1_mv", ";abs #Delta #eta between jet1 and move vec;events/bin", 25, 0, 4);
    nd.book(k_deta_j2_mv, "deta_j2_mv", ";abs #Delta #eta between jet2 and move vec;events/bin", 25, 0, 4);
    nd.book(k_dphi_q0_mv, "dphi_q0_mv", ";abs #Delta #phi between qrk0 and move vec;events/bin", 63, 0, M_PI);
    nd.book(k_dphi_q1_mv, "dphi_q1_mv", ";abs #Delta #phi between qrk1 and move vec;events/bin", 63, 0, M_PI);
    nd.book(k_dphi_q2_mv, "dphi_q2_mv", ";abs #Delta #phi between qrk2 and move vec;events/bin", 63, 0, M_PI);
    nd.book(k_jetdphimax, "jetdphimax", ";max jet #Delta #phi; events", 31, 0, M_PI);
    nd.book(k_jetdphiavg, "jetdphiavg", ";avg jet #Delta #phi; events", 31, 0, M_PI);
    nd.book(k_jetdetamax, "jetdetamax", ";max jet #Delta #eta; events", 80, 0, 5);
    nd.book(k_jetdetaavg, "jetdetaavg", ";avg jet #Delta #eta; events", 80, 0, 5);
    nd.book(k_qrkdphimax, "qrkdphimax", ";max qrk #Delta #phi; events", 31, 0, M_PI);
    nd.book(k_qrkdphiavg, "qrkdphiavg", ";avg qrk #Delta #phi; events", 31, 0, M_PI);
    nd.book(k_jetdphi_mveta, "jetdphi_mveta", ";abs(max jet #Delta #phi);abs( #eta of disp. vector)", 32, 0, M_PI, 40, 0, 4);
    nd.book(k_pt0,     "pt0",     ";Pt of jet0 [GeV]", 50, 0, 1000);
    nd.book(k_pt1,     "pt1",     ";Pt of jet1 [GeV]", 50, 0, 1000);
    nd.book(k_pt2,     "pt2",     ";Pt of jet2 [GeV]", 50, 0, 1000);
    nd.book(k_ntks_j0,"ntks_j0",";Ntks in jet0", 50, 0, 50);
    nd.book(k_ntks_j1,"ntks_j1",";Ntks in jet1", 50, 0, 50);
    nd.book(k_ntks_j2,"ntks_j2",";Ntks in jet2", 50, 0, 50);
    nd.book(k_ip_seedtk_dxysig, "ip_seedtk_dxysig", ";significance of dxy(seedtk, lsp); count", 80, -40, 40);
    nd.book(k_ip_seedtk_dzsig, "ip_seedtk_dzsig", ";significance of dz(seedtk, lsp); count", 80, -40, 40);
    nd.book(k_ip_seedtk_sigs,  "ip_seedtk_sigs", ";significance of dxy(seedtk, lsp); sig. of dz(seedtk, lsp)", 100, -20, 20, 100, -20, 20);
    nd.book(k_ip_seedtk_2D_sumsigs, "ip_seedtk_2D_sumsigs", ";significances to LSP0 summed in quad.; significances to LSP1 summed in quad", 500, 0, 500, 500, 0, 500);
    nd.book(k_ip_seedtk_2D_dxysigs, "ip_seedtk_2D_dxysigs", ";nsigmadxy w.r.t. LSP0; nsigmadxy w.r.t. LSP1", 150, 0, 150, 150, 0, 150);
    nd.book(k_ip_seedtk_2D_dzsigs, "ip_seedtk_2D_dzsigs", ";nsigmadz w.r.t. LSP0; nsigmadz w.r.t. LSP1", 150, 0, 150, 150, 0, 150);
    nd.book(k_ip_seedtk_1D_sumsig,   "ip_seedtk_sumsig", ";summed significance for dists of closest approach btwn seedtk/SV; count", 100, 0, 100);
    nd.book(k_closeseedtks,  "closeseedtks", ";# tracks close to artificial vtx.;count", 80, 0, 80);
    nd.book(k_miscseedtks,  "miscseedtks", ";# of misc seed tracks ;count", 30, 0, 30);
    nd.book(k_closeseedtks_dbv,  "closeseedtks_dbv", ";# tracks close to artificial vtx.;movedist2", 80, 0, 80, 200, 0, 2);
  }

  TH1D* h_vtxntracks[num_numdens] = {0};
  TH1D* h_vtxbs2derr[num_numdens] = {0};
  //TH1D* h_vtxtkonlymass[num_numdens] = {0}; // JMTBAD interface for vertex_tracks common to Mini2 and MovedTracks ntuples
  TH1D* h_vtxs_mass[num_numdens] = {0};
  TH1D* h_vtx_tks_nsigmadxy[num_numdens] = {0};

  for (int i = 0; i < num_numdens; ++i) {
    h_vtxntracks[i] = new TH1D(TString::Format("h_%i_vtxntracks",      i), ";# tracks in largest vertex;events/1", 40, 0, 40);
    h_vtxbs2derr[i] = new TH1D(TString::Format("h_%i_vtxbs2derr",      i), ";#sigma(d_{BV}) of largest vertex (cm);events/2 #mum", 50, 0, 0.01);
    //h_vtxtkonlymass[i] = new TH1D(TString::Format("h_%i_vtxtkonlymass", i), ";track-only mass of largest vertex (GeV);events/1 GeV", 500, 0, 500);
    h_vtxs_mass[i] = new TH1D(TString::Format("h_%i_vtxs_mass", i), ";track+jets mass of largest vertex (GeV);vertices/50 GeV", 100, 0, 5000);
    h_vtx_tks_nsigmadxy[i] = new TH1D(TString::Format("h_%i_vtx_tks_nsigmadxy", i), ";moved and selected track n#sigma(dxy);tracks/0.1", 200, 0, 20);
  }

  double den = 0;

  std::map<std::string, double> nums;

  auto fcn = [&]() {
    const double w = nr.weight();

    // First part of the preselection: our offline jet requirements
    // plus require the lsps to be far enough apart that they don't
    // interfere with each other in reconstruction
    if (!gen.valid() || jets.ht() < 1200 || jets.nminpt() < 4 || gen.lspdist3() < min_lspdist3)
      NR_loop_cont(w);

    for (numdens& nd : nds)
      nd.setw(w);

    const size_t nvtx = vs.n();
    const double lspdist2 = gen.lspdist2();
    const double lspdist3 = gen.lspdist3();
    const double lspdistz = gen.lspdistz();

    const float  close_criteria = 5.0;  // How close must a seed track pass near an SV to be considered 'close?'

    std::vector<int> tks_in_lspjets;

    int n_miscseedtracks = 0;

    // Loop over each LSP
    for (int ilsp = 0; ilsp < 2; ++ilsp) {
      const TVector3 lspdecay = gen.decay(ilsp, bs);  // JMTBAD BS BS
      const double movedist2 = lspdecay.Perp();
      const double movedist3 = lspdecay.Mag();
      const TLorentzVector lsp_p4 = gen.p4(ilsp);

      // Instantiate some jet & quark variables to be filled later
      float   jet_aj = -9.9, jet_pt_0 = -9.9, jet_pt_1 = -9.9, jet_pt_2 = -9.9;
      float   jet_eta_0 = -9.9, jet_eta_1 = -9.9, jet_eta_2 = -9.9;
      double  jet0_lsp_angle = -9.9, jet1_lsp_angle = -9.9, jet2_lsp_angle = -9.9;
      double  jet_mv_dphi_0  = -9.9, jet_mv_dphi_1 = -9.9, jet_mv_dphi_2 = -9.9;
      double  jet_mv_deta_0  = -9.9, jet_mv_deta_1 = -9.9, jet_mv_deta_2 = -9.9;
      double  qrk_mv_dphi_0  = -9.9, qrk_mv_dphi_1 = -9.9, qrk_mv_dphi_2 = -9.9;
      double  jet_dr_max = -9.9, jet_dr_avg = 0.0;
      double  jet_dphi_max = -9.9, jet_dphi_avg = 0.0;
      double  jet_deta_max = -9.9, jet_deta_avg = 0.0;
      double  qrk_dphi_max = -9.9, qrk_dphi_avg = 0.0;
      int     jet_ntks_0 = -10, jet_ntks_1 = -10, jet_ntks_2 = -10;
      int     n_closeseedtks = 0;

      // Stuff for jet-level and quark-level histograms
      std::vector<double> reco_gen_match_dR;
      std::vector<double> gen_which_jetmatch;
      std::vector<double> part_rE_over_gE;
      std::vector<double> seedtk_lsp_dxy;
      std::vector<double> nonsvtk_lsp_dxy;
      std::vector<double> seedtk_lsp_nsigdxy;
      std::vector<double> nonsvtk_lsp_nsigdxy;
      std::vector<double> seedtk_lsp_sumsig;
      std::vector<double> seedtk_lsp_dxysig, seedtk_lsp_dzsig;
      std::vector<double> seedtk_lsp_dxysig0, seedtk_lsp_dzsig0;
      std::vector<double> seedtk_lsp_dxysig1, seedtk_lsp_dzsig1;
      std::vector<double> seedtk_lsp_sumsig0, seedtk_lsp_sumsig1;


      // Second part of preselection: only look at move vectors
      // ~inside the beampipe // JMTBAD the 2.0 cm requirement isn't
      // exact
      if (movedist2 < 0.01 || movedist2 > 2.0)
        continue;
    

      if (dijet) {

        // Match decay daughters to the closest (by dR) reconstructed jet
        std::vector<int> closest_jets(2,-1), quark_assoc(2,-1);
        int s = 2+ilsp*2, swapem = gen.pt(s) < gen.pt(s+1); // toward making the jet assoc'd to the higher (lower) pT quark be "jet0" ("jet1")
        for (int i = 0; i < 2; ++i) {
          const int iq = s + (swapem ? !i : i);

          jmt::MinValue m(0.4);
          for (int j = 0, je = jets.n(); j < je; ++j)
            m(j, gen.p4(iq).DeltaR(jets.p4(j)));
  
          closest_jets[i] = m.i();
          quark_assoc[i] = iq;
        }

        // Last hidden part of the preselection: skip events where
        // daughter doesn't match to a jet or both match to the same
        // jet // JMTBAD how many are we skipping?
        if (closest_jets[0] == -1 || closest_jets[1] == -1 || closest_jets[0] == closest_jets[1])
          continue;

        const TLorentzVector jet_p4_0   = jets.p4(closest_jets[0]);
        const TLorentzVector jet_p4_1   = jets.p4(closest_jets[1]);
        const TLorentzVector quark_p4_0 = gen.p4(quark_assoc[0]);
        const TLorentzVector quark_p4_1 = gen.p4(quark_assoc[1]);
        const TLorentzVector jet_tot_p4 = jet_p4_0 + jet_p4_1;
          
        jet0_lsp_angle = jet_p4_0.Angle(lsp_p4.Vect());
        jet1_lsp_angle = jet_p4_1.Angle(lsp_p4.Vect());

        jet_pt_0  = jet_p4_0.Pt();
        jet_pt_1  = jet_p4_1.Pt();
        jet_dr_max        = jet_p4_0.DeltaR(jet_p4_1);
        jet_aj    = (jet_pt_0 - jet_pt_1) / (jet_pt_0 + jet_pt_1);
        jet_eta_0 = jets.eta(closest_jets[0]);
        jet_eta_1 = jets.eta(closest_jets[1]);
        jet_dphi_max = fabs(jet_p4_0.DeltaPhi(jet_p4_1));
        jet_deta_max = fabs(jet_eta_0 - jet_eta_1); // JMTBAD fabs?
        qrk_dphi_max = fabs(quark_p4_0.DeltaPhi(quark_p4_1));
        jet_ntks_0 = jets.ntracks(closest_jets[0]);
        jet_ntks_1 = jets.ntracks(closest_jets[1]);
        jet_mv_dphi_0  = lsp_p4.DeltaPhi(jet_p4_0);
        jet_mv_dphi_1  = lsp_p4.DeltaPhi(jet_p4_1);
        qrk_mv_dphi_0  = lsp_p4.DeltaPhi(quark_p4_0);
        qrk_mv_dphi_1  = lsp_p4.DeltaPhi(quark_p4_1);
        jet_mv_deta_0  = fabs(jet_eta_0 - lsp_p4.Eta());
        jet_mv_deta_1  = fabs(jet_eta_1 - lsp_p4.Eta());

        if (fabs(jet_dphi_max) > 2.7) continue;
        
      }

      if (!dijet) {

        // Match decay daughters to the closest (by dR) reconstructed jet
        std::vector<int> closest_jets(3,-1), quark_assoc(3,-1);
        TLorentzVector lsp_jets_sump4;

        int s = 2+ilsp*7;
        int swap_01 = gen.pt(s) < gen.pt(s+1), swap_12 = gen.pt(s+1) < gen.pt(s+2), swap_02 = gen.pt(s) < gen.pt(s+2);

        if (swap_01 and swap_12) {quark_assoc[0] = s+2; quark_assoc[1] = s+1; quark_assoc[2] = s;}
        else if (!swap_01 and !swap_12) {quark_assoc[0] = s; quark_assoc[1] = s+1; quark_assoc[2] = s+2;}
        else if (!swap_01 and swap_12) {quark_assoc[0] = s+2*swap_02; quark_assoc[1] = s+2*(!swap_02); quark_assoc[2] = s+1;}
        else {quark_assoc[0] = s+1; quark_assoc[1] = s+2*swap_02; quark_assoc[2] = s+2*(!swap_02);}
        

        for (int k = 0; k < 3; ++k) {
          jmt::MinValue m(0.4);
          for (int j = 0, je = jets.n(); j < je; ++j)
            m(j, gen.p4(quark_assoc[k]).DeltaR(jets.p4(j)));
  
          closest_jets[k] = m.i();
        }
        
        // Start calculating significances of closest approach and count # of close seed tracks
        for (int it=0, ite = tks.n(); it < ite; it++) {
            if (tks.pass_seed(it, bs)) {

                    if (ilsp == 1)
                        n_miscseedtracks++; // Count up all seed tracks. Will subtract out the matching tracks later.

                    std::vector<double> sigs_quad;

                    for (int il = 0; il < 2; il++) {
                        const double temp_sigdxy = tks.dxy(it, gen.decay_x(il), gen.decay_y(il))/tks.err_dxy(it);
                        const double temp_sigdz  = tks.dz(it, gen.decay_x(il), gen.decay_y(il), gen.decay_z(il))/tks.err_dz(it);
                        const double sum_sq_sig = hypot(temp_sigdxy, temp_sigdz);
                        sigs_quad.push_back(sum_sq_sig);
                        if (il == 0) {
                            seedtk_lsp_sumsig0.push_back(sum_sq_sig);
                            seedtk_lsp_dxysig0.push_back(fabs(temp_sigdxy));
                            seedtk_lsp_dzsig0.push_back(fabs(temp_sigdz));
                        }
                        if (il == 1) {
                            seedtk_lsp_sumsig1.push_back(sum_sq_sig);
                            seedtk_lsp_dxysig1.push_back(fabs(temp_sigdxy));
                            seedtk_lsp_dzsig1.push_back(fabs(temp_sigdz));
                        }
                    }      

                  seedtk_lsp_dxysig.push_back(tks.dxy(it, gen.decay_x(ilsp), gen.decay_y(ilsp))/tks.err_dxy(it));
                  seedtk_lsp_dzsig.push_back(tks.dz(it, gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp))/tks.err_dz(it));

              // Count how many 'close' seed tracks there are
                    if ( sigs_quad[ilsp] < close_criteria)
                        n_closeseedtks++;

                    if ( (ilsp == 1) and ((sigs_quad[0] < close_criteria) or  (sigs_quad[1] < close_criteria)) )
                        n_miscseedtracks--;

            }

        }

        // Last hidden part of the preselection: skip events where
        // daughter doesn't match to a jet
        if (closest_jets[0] == -1 || closest_jets[1] == -1 || closest_jets[2] == -1)
          continue;

        const TLorentzVector jet_p4_0   = jets.p4(closest_jets[0]);
        const TLorentzVector jet_p4_1   = jets.p4(closest_jets[1]);
        const TLorentzVector jet_p4_2   = jets.p4(closest_jets[2]);
        const TLorentzVector quark_p4_0 = gen.p4(quark_assoc[0]);
        const TLorentzVector quark_p4_1 = gen.p4(quark_assoc[1]);
        const TLorentzVector quark_p4_2 = gen.p4(quark_assoc[2]);
        const TLorentzVector jet_tot_p4 = jet_p4_0 + jet_p4_1 + jet_p4_2;

        jmt::MaxValue max_jdphi, max_jdeta, max_jdr, max_qdphi;
        for (int j = 0; j < 2; j++) {


            for (int k = j+1; k < 3; k++) {

                // Find the largest vals of jet_dphi, jet_deta, etc...
                max_jdphi(fabs(jets.p4(closest_jets[j]).DeltaPhi(jets.p4(closest_jets[k]))));
                max_jdeta(fabs((jets.p4(closest_jets[j]).Eta()-jets.p4(closest_jets[k]).Eta())));
                max_jdr(jets.p4(closest_jets[j]).DeltaR(jets.p4(closest_jets[k])));
                max_qdphi(fabs(gen.p4(quark_assoc[j]).DeltaPhi(gen.p4(quark_assoc[k]))));

                // Sum up each jet_dphi, jet_deta, etc...
                jet_dphi_avg += fabs(jets.p4(closest_jets[j]).DeltaPhi(jets.p4(closest_jets[k])));
                jet_deta_avg += fabs((jets.p4(closest_jets[j]).Eta()-jets.p4(closest_jets[k]).Eta()));
                jet_dr_avg   += jets.p4(closest_jets[j]).DeltaR(jets.p4(closest_jets[k]));
                qrk_dphi_avg += fabs(gen.p4(quark_assoc[j]).DeltaPhi(gen.p4(quark_assoc[k])));
            }
        }

        // Calculate averages. The '3' comes from (3 nCr 2 =  number of jet pairs)
        jet_dphi_avg /= 3;
        jet_deta_avg /= 3;
        jet_dr_avg   /= 3;
        qrk_dphi_avg /= 3;
          
        jet0_lsp_angle = jet_p4_0.Angle(lsp_p4.Vect());
        jet1_lsp_angle = jet_p4_1.Angle(lsp_p4.Vect());
        jet2_lsp_angle = jet_p4_2.Angle(lsp_p4.Vect());

        jet_pt_0  = jet_p4_0.Pt();
        jet_pt_1  = jet_p4_1.Pt();
        jet_pt_2  = jet_p4_2.Pt();
        jet_aj    = (jet_pt_0 - jet_pt_2) / (jet_pt_0 + jet_pt_2);  // Shaun Is this a good def'n?
        jet_eta_0 = jets.eta(closest_jets[0]);
        jet_eta_1 = jets.eta(closest_jets[1]);
        jet_eta_2 = jets.eta(closest_jets[2]);
        jet_dr_max   = max_jdr;  // FIX THIS
        jet_dphi_max = max_jdphi;
        jet_deta_max = max_jdeta;
        qrk_dphi_max = max_qdphi;
        jet_ntks_1 = jets.ntracks(closest_jets[1]);
        jet_ntks_2 = jets.ntracks(closest_jets[2]);
        jet_mv_dphi_0  = lsp_p4.DeltaPhi(jet_p4_0);
        jet_mv_dphi_1  = lsp_p4.DeltaPhi(jet_p4_1);
        jet_mv_dphi_2  = lsp_p4.DeltaPhi(jet_p4_2);
        qrk_mv_dphi_0  = lsp_p4.DeltaPhi(quark_p4_0);
        qrk_mv_dphi_1  = lsp_p4.DeltaPhi(quark_p4_1);
        qrk_mv_dphi_2  = lsp_p4.DeltaPhi(quark_p4_2);
        jet_mv_deta_0  = fabs(jet_eta_0 - lsp_p4.Eta());
        jet_mv_deta_1  = fabs(jet_eta_1 - lsp_p4.Eta());
        jet_mv_deta_2  = fabs(jet_eta_2 - lsp_p4.Eta());
        
      }

      den += w;

      for (numdens& nd : nds) {
        nd.den(k_decay_x, lspdecay.x());
        nd.den(k_decay_y, lspdecay.y());
        nd.den(k_decay_z, lspdecay.z());
        nd.den(k_decay_xy, lspdecay.x(), lspdecay.y());
        nd.den(k_lspdist2, lspdist2);
        nd.den(k_lspdist3, lspdist3);
        nd.den(k_lspdistz, lspdistz);
        nd.den(k_movedist2, movedist2);
        nd.den(k_movedist3, movedist3);
        nd.den(k_lspeta, fabs(lsp_p4.Eta()));
        nd.den(k_lsppt, lsp_p4.Pt());
        nd.den(k_npv, pvs.n());
        nd.den(k_pvz, pvs.z(0));
        nd.den(k_pvrho, pvs.rho(0));
        nd.den(k_pvntracks, pvs.ntracks(0));
        nd.den(k_pvscore, pvs.score(0));
        nd.den(k_ht, jets.ht());
        nd.den(k_jet_asymm, jet_aj);
        nd.den(k_jetpt0_asymm, jet_pt_0, jet_aj);
        nd.den(k_jetpt1_asymm, jet_pt_1, jet_aj);
        nd.den(k_jeteta0_asymm, jet_eta_0, jet_aj);
        nd.den(k_jeteta1_asymm, jet_eta_1, jet_aj);
        nd.den(k_jetdr_asymm, jet_dr_max, jet_aj);
        nd.den(k_angle0, jet0_lsp_angle);
        nd.den(k_angle1, jet1_lsp_angle);
        nd.den(k_angle2, jet2_lsp_angle);
        nd.den(k_jetdrmax, jet_dr_max);
        nd.den(k_jetdravg, jet_dr_avg);
        nd.den(k_dphi_j0_mv, fabs(jet_mv_dphi_0));
        nd.den(k_dphi_j1_mv, fabs(jet_mv_dphi_1));
        nd.den(k_dphi_j2_mv, fabs(jet_mv_dphi_2));
        nd.den(k_deta_j0_mv, jet_mv_deta_0);
        nd.den(k_deta_j1_mv, jet_mv_deta_1);
        nd.den(k_deta_j2_mv, jet_mv_deta_2);
        nd.den(k_dphi_q0_mv, fabs(qrk_mv_dphi_0));
        nd.den(k_dphi_q1_mv, fabs(qrk_mv_dphi_1));
        nd.den(k_dphi_q2_mv, fabs(qrk_mv_dphi_2));
        nd.den(k_jetdphimax, jet_dphi_max);
        nd.den(k_jetdphiavg, jet_dphi_avg);
        nd.den(k_jetdetamax, jet_deta_max);
        nd.den(k_jetdetaavg, jet_deta_avg);
        nd.den(k_qrkdphimax, fabs(qrk_dphi_max));
        nd.den(k_qrkdphiavg, fabs(qrk_dphi_avg));
        nd.den(k_jetdphi_mveta, fabs(jet_dphi_max), fabs(lsp_p4.Eta()));
        nd.den(k_pt0, jet_pt_0);
        nd.den(k_pt1, jet_pt_1);
        nd.den(k_pt2, jet_pt_2);
        nd.den(k_ntks_j0, jet_ntks_0);
        nd.den(k_ntks_j1, jet_ntks_1);
        nd.den(k_ntks_j2, jet_ntks_2);
        nd.den(k_ip_seedtk_dxysig, seedtk_lsp_dxysig);
        nd.den(k_ip_seedtk_dzsig, seedtk_lsp_dzsig);
        nd.den(k_ip_seedtk_sigs, seedtk_lsp_dxysig, seedtk_lsp_dzsig);
        if (ilsp == 0) {
            nd.den(k_ip_seedtk_2D_sumsigs, seedtk_lsp_sumsig0, seedtk_lsp_sumsig1);
            nd.den(k_ip_seedtk_2D_dxysigs, seedtk_lsp_dxysig0, seedtk_lsp_dxysig1);
            nd.den(k_ip_seedtk_2D_dzsigs, seedtk_lsp_dzsig0, seedtk_lsp_dzsig1);
        }
        nd.den(k_ip_seedtk_1D_sumsig, seedtk_lsp_sumsig);
        nd.den(k_closeseedtks, n_closeseedtks);
        nd.den(k_closeseedtks_dbv, n_closeseedtks, movedist2);
        if (ilsp == 1) {
            nd.den(k_miscseedtks, n_miscseedtracks);
        }
            
      }

      int n_pass_nocuts = 0;
      int n_pass_ntracks = 0;
      int n_pass_all = 0;

      seedtk_lsp_dxysig.clear();
      seedtk_lsp_dzsig.clear();
      seedtk_lsp_dxysig0.clear(); seedtk_lsp_dxysig1.clear(); 
      seedtk_lsp_dzsig0.clear(); seedtk_lsp_dzsig1.clear();
      seedtk_lsp_sumsig0.clear(); seedtk_lsp_sumsig1.clear();

      std::vector<int> first_vtx_to_pass(num_numdens, -1);
      auto set_it_if_first = [](int& to_set, int to_set_to) { if (to_set == -1) to_set = to_set_to; };

      for (size_t i = 0; i < nvtx; ++i) {
        const double dist2move = (lspdecay - vs.pos(i)).Mag();
        if (dist2move > 0.0084)
          continue;

        const bool pass_ntracks = vs.ntracks(i) >= 5;
        const bool pass_bs2derr = vs.bs2derr(i) < 0.0025; // JMTBAD rescale_bs2derr

        if (1)                             { set_it_if_first(first_vtx_to_pass[0], i); ++n_pass_nocuts;  }
        if (pass_ntracks)                  { set_it_if_first(first_vtx_to_pass[1], i); ++n_pass_ntracks; }
        if (pass_ntracks && pass_bs2derr)  { set_it_if_first(first_vtx_to_pass[2], i); ++n_pass_all;     }
      }

      for (int in = 0; in < num_numdens; ++in) {
        const int iv = first_vtx_to_pass[in];
        if (iv != -1) {
          h_vtxntracks   [in]->Fill(vs.ntracks(iv));
          h_vtxbs2derr   [in]->Fill(vs.bs2derr(iv));
          //h_vtxtkonlymass[in]->Fill(vs.tkonlymass(iv));
          h_vtxs_mass    [in]->Fill(vs.mass(iv));


          // This block of code is used to plot the dxy(SV,tk) distribution for tracks in an SV and tracks not in an SV
          std::vector<int> tks_in_sv = tks.tks_for_sv(iv);

          for (const int it : tks_in_sv) {
            h_vtx_tks_nsigmadxy[in]->Fill(tks.nsigmadxybs(it, bs), w);
          }

          if (in == 2) {
            for (int it=0, ite=tks.n() ; it < ite ; it++) {


                // Tracks that do associate to the SV
                if (std::find(tks_in_sv.begin(), tks_in_sv.end(), it) != tks_in_sv.end()) {

                // The chunk of code sees which terms in sigma d_xyz are dominant
                    const double this_dxy = tks.dxy(it, gen.decay_x(ilsp), gen.decay_y(ilsp));
                    const double tk_sumsig = hypot(this_dxy/tks.err_dxy(it), tks.dz(it, gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp))/tks.err_dz(it));

                    const double dxy_sig0 = tks.dxy(it, gen.decay_x(0), gen.decay_y(0))/tks.err_dxy(it);
                    const double dxy_sig1 = tks.dxy(it, gen.decay_x(1), gen.decay_y(1))/tks.err_dxy(it);
                    const double dz_sig0  = tks.dz(it, gen.decay_x(0), gen.decay_y(0), gen.decay_z(0))/tks.err_dz(it);
                    const double dz_sig1  = tks.dz(it, gen.decay_x(1), gen.decay_y(1), gen.decay_z(1))/tks.err_dz(it);

                    seedtk_lsp_sumsig.push_back(tk_sumsig); 
                    seedtk_lsp_dxy.push_back(fabs(tks.dxy(it, gen.decay_x(ilsp), gen.decay_y(ilsp))));
                    seedtk_lsp_nsigdxy.push_back(fabs(tks.dxy(it, gen.decay_x(ilsp), gen.decay_y(ilsp))/tks.err_dxy(it)));
                    seedtk_lsp_dxysig.push_back(tks.dxy(it, gen.decay_x(ilsp), gen.decay_y(ilsp))/tks.err_dxy(it));
                    seedtk_lsp_dzsig.push_back(tks.dz(it, gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp))/tks.err_dz(it));

                    seedtk_lsp_dxysig0.push_back(dxy_sig0);
                    seedtk_lsp_dxysig1.push_back(dxy_sig1);

                    seedtk_lsp_dzsig0.push_back(dz_sig0);
                    seedtk_lsp_dzsig1.push_back(dz_sig1);

                    seedtk_lsp_sumsig0.push_back(hypot(dxy_sig0, dz_sig0));
                    seedtk_lsp_sumsig1.push_back(hypot(dxy_sig1, dz_sig1));
                }

                // Tracks that don't associate to the given SV
                else {
                    nonsvtk_lsp_dxy.push_back(fabs(tks.dxy(it, gen.decay_x(ilsp), gen.decay_y(ilsp))));
                    nonsvtk_lsp_nsigdxy.push_back(fabs(tks.dxy(it, gen.decay_x(ilsp), gen.decay_y(ilsp))/tks.err_dxy(it)));
                }
            }

          }
          
        }
      }

      if (n_pass_nocuts)  nums["nocuts"]  += w;
      if (n_pass_ntracks) nums["ntracks"] += w;
      if (n_pass_all)     nums["all"]     += w;

      const int npasses[num_numdens] = {
        n_pass_nocuts,
        n_pass_ntracks,
        n_pass_all
      };

      for (int in = 0; in < num_numdens; ++in) {
        if (!npasses[in])
          continue;

        numdens& nd = nds[in];
        nd.num(k_decay_x, lspdecay.x());
        nd.num(k_decay_y, lspdecay.y());
        nd.num(k_decay_z, lspdecay.z());
        nd.num(k_decay_xy, lspdecay.x(), lspdecay.y());
        nd.num(k_lspdist2, lspdist2);
        nd.num(k_lspdist3, lspdist3);
        nd.num(k_lspdistz, lspdistz);
        nd.num(k_movedist2, movedist2);
        nd.num(k_movedist3, movedist3);
        nd.num(k_lspeta, fabs(lsp_p4.Eta()));
        nd.num(k_lsppt, lsp_p4.Pt());
        nd.num(k_npv, pvs.n());
        nd.num(k_pvz, pvs.z(0));
        nd.num(k_pvrho, pvs.rho(0));
        nd.num(k_pvntracks, pvs.ntracks(0));
        nd.num(k_pvscore, pvs.score(0));
        nd.num(k_ht, jets.ht());
        nd.num(k_jet_asymm, jet_aj);
        nd.num(k_jetpt0_asymm, jet_pt_0, jet_aj);
        nd.num(k_jetpt1_asymm, jet_pt_1, jet_aj);
        nd.num(k_jeteta0_asymm, jet_eta_0, jet_aj);
        nd.num(k_jeteta1_asymm, jet_eta_1, jet_aj);
        nd.num(k_jetdr_asymm, jet_dr_max, jet_aj);
        nd.num(k_angle0, jet0_lsp_angle);
        nd.num(k_angle1, jet1_lsp_angle);
        nd.num(k_angle2, jet2_lsp_angle);
        nd.num(k_jetdrmax, jet_dr_max);
        nd.num(k_jetdravg, jet_dr_avg);
        nd.num(k_dphi_j0_mv, fabs(jet_mv_dphi_0));
        nd.num(k_dphi_j1_mv, fabs(jet_mv_dphi_1));
        nd.num(k_dphi_j2_mv, fabs(jet_mv_dphi_2));
        nd.num(k_deta_j0_mv, jet_mv_deta_0);
        nd.num(k_deta_j1_mv, jet_mv_deta_1);
        nd.num(k_deta_j2_mv, jet_mv_deta_2);
        nd.num(k_dphi_q0_mv, fabs(qrk_mv_dphi_0));
        nd.num(k_dphi_q1_mv, fabs(qrk_mv_dphi_1));
        nd.num(k_dphi_q2_mv, fabs(qrk_mv_dphi_2));
        nd.num(k_jetdphimax, jet_dphi_max);
        nd.num(k_jetdphiavg, jet_dphi_avg);
        nd.num(k_jetdetamax, jet_deta_max);
        nd.num(k_jetdetaavg, jet_deta_avg);
        nd.num(k_qrkdphimax, fabs(qrk_dphi_max));
        nd.num(k_qrkdphiavg, fabs(qrk_dphi_avg));
        nd.num(k_jetdphi_mveta, fabs(jet_dphi_max), fabs(lsp_p4.Eta()));
        nd.num(k_pt0, jet_pt_0);
        nd.num(k_pt1, jet_pt_1);
        nd.num(k_pt2, jet_pt_2);
        nd.num(k_ntks_j0, jet_ntks_0);
        nd.num(k_ntks_j1, jet_ntks_1);
        nd.num(k_ntks_j2, jet_ntks_2);
        nd.num(k_ip_seedtk_dxysig, seedtk_lsp_dxysig);
        nd.num(k_ip_seedtk_dzsig, seedtk_lsp_dzsig);
        nd.num(k_ip_seedtk_sigs, seedtk_lsp_dxysig, seedtk_lsp_dzsig);
        nd.num(k_ip_seedtk_2D_sumsigs, seedtk_lsp_sumsig0, seedtk_lsp_sumsig1);
        nd.num(k_ip_seedtk_2D_dxysigs, seedtk_lsp_dxysig0, seedtk_lsp_dxysig1);
        nd.num(k_ip_seedtk_2D_dzsigs, seedtk_lsp_dzsig0, seedtk_lsp_dzsig1);
        nd.num(k_ip_seedtk_1D_sumsig, seedtk_lsp_sumsig);
        nd.num(k_closeseedtks, n_closeseedtks);
        nd.num(k_closeseedtks_dbv, n_closeseedtks, movedist2);
        if (ilsp == 1)
            nd.num(k_miscseedtks, n_miscseedtracks);
      }
    }

    NR_loop_cont(w);
  };

  nr.loop(fcn);


  printf("%12.1f", den);
  for (const std::string& c : {"nocuts", "ntracks", "all"}) {
    const jmt::interval i = jmt::clopper_pearson_binom(nums[c], den);
    printf("    %6.4f +- %6.4f", i.value, i.error());
  }
  printf("\n");
}
