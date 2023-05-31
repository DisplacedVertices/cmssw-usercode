#include "utils.h"

int main(int argc, char** argv) {
  double min_lspdist3 = 0.02;

  jmt::NtupleReader<mfv::MovedTracksNtuple> nr;
  namespace po = boost::program_options;
  nr.init_options("mfvMovedTreeMCTruth/t", "TrackMoverMCTruthHistsUlv30lepmv2", "trackmovermctruthulv30lepmv2", "all_signal = True")
    ("min-lspdist3", po::value<double>(&min_lspdist3)->default_value(0.02), "min distance between LSP decays to use event")
    ;

  if (!nr.parse_options(argc, argv)) return 1;
  std::cout << " min_lspdist3: " << min_lspdist3 << "\n";

  if (!nr.init()) return 1;
  auto& nt = nr.nt();
  auto& bs = nt.bs();
  auto& pvs = nt.pvs();
  auto& jets = nt.jets();
  //auto& tks = nt.tracks();
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

  enum { k_decay_x, k_decay_y, k_decay_z, k_decay_xy, k_lspdist2, k_lspdist3, k_lspdistz, k_movedist2, k_movedist3, k_lspeta,k_lsppt, k_npv, k_pvz, k_pvrho, k_pvntracks, k_pvscore, k_ht, k_jet_asymm, k_vtx_unc, k_jet_dr, k_jet_deta, k_jet_dphi, k_jet_dind, k_pt0, k_pt1, k_ntks_j0, k_ntks_j1, k_nmovedtracks, k_dphi_sum_j_mv, k_deta_sum_j_mv, k_dphi_sum_q_mv, k_jetpt0_asymm, k_jetpt1_asymm, k_jeteta0_asymm, k_jeteta1_asymm, k_jetdr_asymm, k_jetdravg, k_angle0, k_angle1, k_dphi_j0_mv, k_dphi_j1_mv, k_deta_j0_mv, k_deta_j1_mv, k_dphi_q0_mv, k_dphi_q1_mv, k_jetdphimax, k_jetdetamax, k_qrkdphimax, k_jetdphi_mveta, k_jetmovea3d01, k_jeteta01, k_jetpt01, k_pt_angle0, k_pt_angle1, k_eta_angle0, k_eta_angle1};

  for (numdens& nd : nds) {
    nd.book(k_decay_x,  "decay_x" , ";SV Decay X-pos [cm]; arb. units", 100, -4, 4);
    nd.book(k_decay_y,  "decay_y" , ";SV Decay Y-pos [cm]; arb. units", 100, -4, 4);
    nd.book(k_decay_z,  "decay_z" , ";SV Decay Z-pos [cm]; arb. units", 100, -20, 20);
    nd.book(k_decay_xy, "decay_xy" , ";SV Decay X-pos [cm]; SV Decay Y-pos [cm]", 100, -10, 10, 100, -10, 10);
    nd.book(k_lspdist2, "lspdist2", ";2-dist between gen verts;events/0.01 cm", 200, 0, 2);
    nd.book(k_lspdist3, "lspdist3", ";3-dist between gen verts;events/0.01 cm", 200, 0, 2);
    nd.book(k_lspdistz, "lspdistz", ";z-dist between gen verts;events/0.01 cm", 200, 0, 2);
    nd.book(k_movedist2, "movedist2", ";movement 2-dist;events/0.01 cm", 200, 0, 2);
    nd.book(k_movedist3, "movedist3", ";movement 3-dist;events/0.01 cm", 200, 0, 2);
    nd.book(k_lspeta,    "movevectoreta"   , ";move vector eta;events/0.08 cm", 100, -4, 4);
    nd.book(k_lsppt,     "lsppt"    , ";Pt of LSP [GeV];events/bin", 50, 0, 1000);
    nd.book(k_npv, "npv", ";# PV;events/1", 100, 0, 100);
    nd.book(k_pvz, "pvz", ";PV z (cm);events/0.24 cm", 200, -24, 24);
    nd.book(k_pvrho, "pvrho", ";PV #rho (cm);events/1 #mum", 200, 0, 0.02);
    nd.book(k_pvntracks, "pvntracks", ";PV # tracks;events/2", 200, 0, 400);
    nd.book(k_pvscore, "pvscore", ";PV #Sigma p_{T}^{2} (GeV^{2});events/200 GeV^{2}", 200, 0, 40000);
    nd.book(k_ht, "ht", ";#Sigma H_{T} (GeV);events/50 GeV", 50, 0, 2500);
    nd.book(k_jet_asymm, "jet_asymm", ";Jet asymmetry A_{J}; arb. units", 25, 0, 1);
	nd.book(k_vtx_unc, "vtx_unc", ";dist3d(move vector, vtx); arb. units", 100, 0, 0.1);
	nd.book(k_jet_dr, "jet_dr", ";jets #DeltaR; arb. units", 70, 0, 7);
	nd.book(k_jet_deta, "jet_deta", ";jets #DeltaEta; arb. units", 70, 0, 7);
	nd.book(k_jet_dphi, "jet_dphi", ";jets #DeltaPhi; arb. units", 70, 0, 7);
	nd.book(k_jet_dind, "jet_dind", ";jets #DeltaIndex; arb. units", 20, 0, 20);
	nd.book(k_pt0, "pt0", ";Pt of jet0 [GeV]", 50, 0, 1000);
	nd.book(k_pt1, "pt1", ";Pt of jet1 [GeV]", 50, 0, 1000);
	nd.book(k_ntks_j0, "ntks_j0", ";Ntks in jet0", 50, 0, 50);
	nd.book(k_ntks_j1, "ntks_j1", ";Ntks in jet1", 50, 0, 50);
	nd.book(k_nmovedtracks, "nmovedtracks", ";# moved tracks;events/2", 120, 0, 120);
	nd.book(k_dphi_sum_j_mv, "dphi_sum_j_mv", ";abs #Delta #phi between jet0+jet1 and move vec;events/bin", 63, 0, M_PI);
	nd.book(k_deta_sum_j_mv, "deta_sum_j_mv", ";abs #Delta #eta between jet0+jet1 and move vec;events/bin", 25, 0, 4);
	nd.book(k_dphi_sum_q_mv, "dphi_sum_q_mv", ";abs #Delta #phi between jet0+jet1 and move vec;events/bin", 63, 0, M_PI);

    nd.book(k_jetpt0_asymm, "jetpt0_asymm", ";jet p_{T} 0; jet asymm. A_{J}", 50, 0, 1000, 25, 0, 1);
    nd.book(k_jetpt1_asymm, "jetpt1_asymm", ";jet p_{T} 1; jet asymm. A_{J}", 50, 0, 1000, 25, 0, 1);
    nd.book(k_jeteta0_asymm, "jeteta0_asymm", ";jet #eta 0; jet asymm. A_{J}", 100, -4, 4, 25, 0, 1);
    nd.book(k_jeteta1_asymm, "jeteta1_asymm", ";jet #eta 1; jet asymm. A_{J}", 100, -4, 4, 25, 0, 1);
    nd.book(k_jetdr_asymm, "jetdr_asymm", ";jets #DeltaR; jet asymm. A_{J}", 70, 0, 7, 25, 0, 1);
    nd.book(k_jetdravg, "jetdravg", ";avg jet #Delta R;events/0.1", 70, 0, 7);
    nd.book(k_angle0, "jetmovea3d0", ";Angle between jet0 and SV;arb. units", 63, 0, M_PI);
    nd.book(k_angle1, "jetmovea3d1", ";Angle between jet1 and SV;arb. units", 63, 0, M_PI);
    nd.book(k_dphi_j0_mv, "dphi_j0_mv", ";abs #Delta #phi between jet0 and move vec;events/bin", 63, 0, M_PI);
    nd.book(k_dphi_j1_mv, "dphi_j1_mv", ";abs #Delta #phi between jet1 and move vec;events/bin", 63, 0, M_PI);
    nd.book(k_deta_j0_mv, "deta_j0_mv", ";abs #Delta #eta between jet0 and move vec;events/bin", 25, 0, 4);
    nd.book(k_deta_j1_mv, "deta_j1_mv", ";abs #Delta #eta between jet1 and move vec;events/bin", 25, 0, 4);
    nd.book(k_dphi_q0_mv, "dphi_q0_mv", ";abs #Delta #phi between qrk0 and move vec;events/bin", 63, 0, M_PI);
    nd.book(k_dphi_q1_mv, "dphi_q1_mv", ";abs #Delta #phi between qrk1 and move vec;events/bin", 63, 0, M_PI);
    nd.book(k_jetdphimax, "jetdphimax", ";max jet #Delta #phi; events", 32, -M_PI, M_PI);
    nd.book(k_jetdetamax, "jetdetamax", ";max jet #Delta #eta; events", 200, -5, 5);
    nd.book(k_qrkdphimax, "qrkdphimax", ";abs. max qrk #Delta #phi; events", 63, 0, M_PI);
    nd.book(k_jetdphi_mveta, "jetdphi_mveta", ";abs(max jet #Delta #phi);abs( #eta of disp. vector)", 32, 0, M_PI, 40, 0, 4);
    
    nd.book(k_jetmovea3d01, "jetmovea3d", ";3D angle between jet 0 and move vector;3D angle between jet 1 and move vector", 63, 0, M_PI, 63, 0, M_PI);
    nd.book(k_jeteta01, "jeteta01", ";jet #eta 0 (GeV);jet #eta 1 (GeV)", 100, -4, 4, 100, -4, 4);
    nd.book(k_jetpt01, "jetpt01", ";jet p_{T} 0 (GeV);jet p_{T} 1 (GeV)", 50, 0, 1000, 50, 0, 1000);
    nd.book(k_pt_angle0,     "pt_angle0"    , ";Pt of jet0 [GeV]; Angle between jet0 and SV", 50, 0, 2500, 63, 0, M_PI);
    nd.book(k_pt_angle1,     "pt_angle1"    , ";Pt of jet1 [GeV]; Angle between jet1 and SV", 50, 0, 2500, 63, 0, M_PI);
    nd.book(k_eta_angle0,    "eta_angle0"  , ";Eta of SV decay vector; Angle between jet0 and SV", 60, -5, 5, 63, 0, M_PI);
    nd.book(k_eta_angle1,    "eta_angle1"  , ";Eta of SV decay vector; Angle between jet1 and SV", 60, -5, 5, 63, 0, M_PI);
  }

  TH1D* h_vtxntracks[num_numdens] = {0};
  TH1D* h_vtxbs2derr[num_numdens] = {0};
  //TH1D* h_vtxtkonlymass[num_numdens] = {0}; // JMTBAD interface for vertex_tracks common to Mini2 and MovedTracks ntuples
  TH1D* h_vtxs_mass[num_numdens] = {0};

  for (int i = 0; i < num_numdens; ++i) {
    h_vtxntracks[i] = new TH1D(TString::Format("h_%i_vtxntracks",      i), ";# tracks in largest vertex;events/1", 40, 0, 40);
    h_vtxbs2derr[i] = new TH1D(TString::Format("h_%i_vtxbs2derr",      i), ";#sigma(d_{BV}) of largest vertex (cm);events/2 #mum", 50, 0, 0.01);
    //h_vtxtkonlymass[i] = new TH1D(TString::Format("h_%i_vtxtkonlymass", i), ";track-only mass of largest vertex (GeV);events/1 GeV", 500, 0, 500);
    h_vtxs_mass[i] = new TH1D(TString::Format("h_%i_vtxs_mass", i), ";track+jets mass of largest vertex (GeV);vertices/50 GeV", 100, 0, 5000);
  }

  double den = 0;
  std::map<std::string, double> nums;

  auto fcn = [&]() {
    const double w = nr.weight();

    // First part of the preselection: our offline jet requirements
    // plus require the lsps to be far enough apart that they don't
    // interfere with each other in reconstruction
    if (!gen.valid() || gen.lspdist3() < min_lspdist3) //FIXME 
      NR_loop_cont(w);

    for (numdens& nd : nds)
      nd.setw(w);

    const size_t nvtx = vs.n();
    const double lspdist2 = gen.lspdist2();
    const double lspdist3 = gen.lspdist3();
    const double lspdistz = gen.lspdistz();

    // Instantiate some jet & quark variables to be filled later
    float   jet_aj = -9.9, jet_dr = -9.9, jet_deta = -9.9, jet_dphi = -9.9, jet_dind = -9.9, jet_pt_0 = -9.9, jet_pt_1 = -9.9;
    float   jet_eta_0 = -9.9, jet_eta_1 = -9.9;
    double  jet0_lsp_angle = -9.9, jet1_lsp_angle = -9.9;
    double  jet_mv_dphi_0  = 0.0, jet_mv_dphi_1 = 0.0, jet_mv_dphi_sum = 0.0;
    double  jet_mv_deta_0  = 0.0, jet_mv_deta_1 = 0.0, jet_mv_deta_sum = 0.0;
    double  qrk_mv_dphi_0  = 0.0, qrk_mv_dphi_1 = 0.0, qrk_mv_dphi_sum = 0.0;
    double  jet_dphi_max = 0.0;
    double  jet_deta_max = 0.0;
    double  qrk_dphi_max = 0.0;
    int     jet_ntks_0 = -10, jet_ntks_1 = -10;

    // Loop over each LSP
    for (int ilsp = 0; ilsp < 2; ++ilsp) {
      const TVector3 lspdecay = gen.decay(ilsp, bs);  // JMTBAD BS BS
      const double movedist2 = lspdecay.Perp();
      const double movedist3 = lspdecay.Mag();
      const TLorentzVector lsp_p4 = gen.p4(ilsp);

      // Second part of preselection: only look at move vectors
      // ~inside the beampipe // JMTBAD the 2.0 cm requirement isn't
      // exact
      if (movedist2 < 0.01 || movedist2 > 2.0)
        continue;

      if (dijet) {
        //assert(abs(gen.id(ilsp)) == 1000006); // stop pair production

        // Match decay daughters to the closest (by dR) reconstructed jet
        std::vector<int> closest_jets(2,-1), quark_assoc(2,-1);
        int s = 2+ilsp*2, swapem = gen.pt(s) < gen.pt(s+1); // toward making the jet assoc'd to the higher (lower) pT quark be "jet0" ("jet1")
        for (int i = 0; i < 2; ++i) {
          const int iq = s + (swapem ? !i : i);
          //assert(gen.id(iq) == -1000006 / gen.id(ilsp)); // stop -> dbar dbar + c.c.

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
          
        jet0_lsp_angle = jet_p4_0.Angle(lsp_p4.Vect());	 //smearing angle
        jet1_lsp_angle = jet_p4_1.Angle(lsp_p4.Vect());  //smearing angle

        jet_pt_0  = jet_p4_0.Pt();
        jet_pt_1  = jet_p4_1.Pt();
        jet_dr        = jet_p4_0.DeltaR(jet_p4_1);
		jet_dphi = jet_p4_0.DeltaPhi(jet_p4_1);
		jet_deta = fabs(jet_eta_0 - jet_eta_1);
		jet_dind = fabs(closest_jets[1] - closest_jets[0]);
        jet_aj    = (jet_pt_0 - jet_pt_1) / (jet_pt_0 + jet_pt_1);
        jet_eta_0 = jets.eta(closest_jets[0]);
        jet_eta_1 = jets.eta(closest_jets[1]);
        jet_dphi_max = jet_p4_0.DeltaPhi(jet_p4_1);
        jet_deta_max = jet_eta_0 - jet_eta_1; // JMTBAD fabs?
        qrk_dphi_max = quark_p4_0.DeltaPhi(quark_p4_1);
        jet_ntks_0 = jets.ntracks(closest_jets[0]);
        jet_ntks_1 = jets.ntracks(closest_jets[1]);
        jet_mv_dphi_0  = lsp_p4.DeltaPhi(jet_p4_0);
        jet_mv_dphi_1  = lsp_p4.DeltaPhi(jet_p4_1);
		jet_mv_dphi_sum = lsp_p4.DeltaPhi(jet_p4_0 + jet_p4_1);
        qrk_mv_dphi_0  = lsp_p4.DeltaPhi(quark_p4_0);
        qrk_mv_dphi_1  = lsp_p4.DeltaPhi(quark_p4_1);
		qrk_mv_dphi_sum = lsp_p4.DeltaPhi(quark_p4_0 + quark_p4_1);
        jet_mv_deta_0  = fabs(jet_eta_0 - lsp_p4.Eta());
        jet_mv_deta_1  = fabs(jet_eta_1 - lsp_p4.Eta());
		jet_mv_deta_sum = fabs((jet_p4_0 + jet_p4_1).Eta() - lsp_p4.Eta());
      }

	  int n_pass_nocuts = 0;
	  int n_pass_ntracks = 0;
	  int n_pass_all = 0;
	  double  dist2move = -9.9;

	  std::vector<int> first_vtx_to_pass(num_numdens, -1);
	  auto set_it_if_first = [](int& to_set, int to_set_to) { if (to_set == -1) to_set = to_set_to; };

	  for (size_t i = 0; i < nvtx; ++i) {
		  dist2move = (lspdecay - vs.pos(i)).Mag();
		  //if (dist2move > 0.0084) //FIXME
			//continue;

		  const bool pass_ntracks = vs.ntracks(i) >= 5;
		  const bool pass_bs2derr = vs.bs2derr(i) < 0.0050; // JMTBAD rescale_bs2derr // FIXME

		  if (1) { set_it_if_first(first_vtx_to_pass[0], i); ++n_pass_nocuts; }
		  if (pass_ntracks) { set_it_if_first(first_vtx_to_pass[1], i); ++n_pass_ntracks; }
		  if (pass_ntracks && pass_bs2derr) { set_it_if_first(first_vtx_to_pass[2], i); ++n_pass_all; }
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
        nd.den(k_lspeta, lsp_p4.Eta());
        nd.den(k_lsppt, lsp_p4.Pt());
        nd.den(k_npv, pvs.n());
        nd.den(k_pvz, pvs.z(0));
        nd.den(k_pvrho, pvs.rho(0));
        nd.den(k_pvntracks, pvs.ntracks(0));
        nd.den(k_pvscore, pvs.score(0));
        nd.den(k_ht, jets.ht());
        nd.den(k_jet_asymm, jet_aj);
		nd.den(k_vtx_unc, dist2move);
		nd.den(k_jet_dr, jet_dr);
		nd.den(k_jet_deta, jet_deta);
		nd.den(k_jet_dphi, jet_dphi);
		nd.den(k_jet_dind, jet_dind);
		nd.den(k_pt0, jet_pt_0);
		nd.den(k_pt1, jet_pt_1);
		nd.den(k_ntks_j0, jet_ntks_0);
		nd.den(k_ntks_j1, jet_ntks_1);
		nd.den(k_nmovedtracks, jet_ntks_0 + jet_ntks_1);
		nd.den(k_dphi_sum_j_mv, fabs(jet_mv_dphi_sum));
		nd.den(k_deta_sum_j_mv, jet_mv_deta_sum);
		nd.den(k_dphi_sum_q_mv, fabs(qrk_mv_dphi_sum));
        nd.den(k_jetpt0_asymm, jet_pt_0, jet_aj);
        nd.den(k_jetpt1_asymm, jet_pt_1, jet_aj);
        nd.den(k_jeteta0_asymm, jet_eta_0, jet_aj);
        nd.den(k_jeteta1_asymm, jet_eta_1, jet_aj);
        nd.den(k_jetdr_asymm, jet_dr, jet_aj);
        nd.den(k_angle0, jet0_lsp_angle);
        nd.den(k_angle1, jet1_lsp_angle);
        nd.den(k_jetdravg, jet_dr);
        nd.den(k_dphi_j0_mv, fabs(jet_mv_dphi_0));
        nd.den(k_dphi_j1_mv, fabs(jet_mv_dphi_1));
        nd.den(k_deta_j0_mv, jet_mv_deta_0);
        nd.den(k_deta_j1_mv, jet_mv_deta_1);
        nd.den(k_dphi_q0_mv, fabs(qrk_mv_dphi_0));
        nd.den(k_dphi_q1_mv, fabs(qrk_mv_dphi_1));
        nd.den(k_jetdphimax, jet_dphi_max);
        nd.den(k_jetdetamax, jet_deta_max);
        nd.den(k_qrkdphimax, fabs(qrk_dphi_max));
        nd.den(k_jetdphi_mveta, fabs(jet_dphi_max), fabs(lsp_p4.Eta()));
        nd.den(k_jetmovea3d01, jet0_lsp_angle, jet1_lsp_angle);
        nd.den(k_jeteta01,  jet_eta_0, jet_eta_1);
        nd.den(k_jetpt01, jet_pt_0, jet_pt_1);
        nd.den(k_pt_angle0, jet_pt_0, jet0_lsp_angle);
        nd.den(k_pt_angle1, jet_pt_1, jet1_lsp_angle);
        nd.den(k_eta_angle0, lsp_p4.Eta(), jet0_lsp_angle);
        nd.den(k_eta_angle1, lsp_p4.Eta(), jet1_lsp_angle);
      }

      for (int in = 0; in < num_numdens; ++in) {
        const int iv = first_vtx_to_pass[in];
        if (iv != -1) {
          h_vtxntracks   [in]->Fill(vs.ntracks(iv));
          h_vtxbs2derr   [in]->Fill(vs.bs2derr(iv));
          //h_vtxtkonlymass[in]->Fill(vs.tkonlymass(iv));
          h_vtxs_mass    [in]->Fill(vs.mass(iv));
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
        nd.num(k_lspeta, lsp_p4.Eta());
        nd.num(k_lsppt, lsp_p4.Pt());
        nd.num(k_npv, pvs.n());
        nd.num(k_pvz, pvs.z(0));
        nd.num(k_pvrho, pvs.rho(0));
        nd.num(k_pvntracks, pvs.ntracks(0));
        nd.num(k_pvscore, pvs.score(0));
        nd.num(k_ht, jets.ht());
        nd.num(k_jet_asymm, jet_aj);
		nd.num(k_vtx_unc, dist2move);
		nd.num(k_jet_dr, jet_dr);
		nd.num(k_jet_deta, jet_deta);
		nd.num(k_jet_dphi, jet_dphi);
		nd.num(k_jet_dind, jet_dind);
		nd.num(k_pt0, jet_pt_0);
		nd.num(k_pt1, jet_pt_1);
		nd.num(k_ntks_j0, jet_ntks_0);
		nd.num(k_ntks_j1, jet_ntks_1);
		nd.num(k_nmovedtracks, jet_ntks_0 + jet_ntks_1);
		nd.num(k_dphi_sum_j_mv, fabs(jet_mv_dphi_sum));
		nd.num(k_deta_sum_j_mv, jet_mv_deta_sum);
		nd.num(k_dphi_sum_q_mv, fabs(qrk_mv_dphi_sum));
        nd.num(k_jetpt0_asymm, jet_pt_0, jet_aj);
        nd.num(k_jetpt1_asymm, jet_pt_1, jet_aj);
        nd.num(k_jeteta0_asymm, jet_eta_0, jet_aj);
        nd.num(k_jeteta1_asymm, jet_eta_1, jet_aj);
        nd.num(k_jetdr_asymm, jet_dr, jet_aj);
        nd.num(k_jetdravg, jet_dr);
        nd.num(k_angle0, jet0_lsp_angle);
        nd.num(k_angle1, jet1_lsp_angle);
        nd.num(k_dphi_j0_mv, fabs(jet_mv_dphi_0));
        nd.num(k_dphi_j1_mv, fabs(jet_mv_dphi_1));
        nd.num(k_deta_j0_mv, jet_mv_deta_0);
        nd.num(k_deta_j1_mv, jet_mv_deta_1);
        nd.num(k_dphi_q0_mv, fabs(qrk_mv_dphi_0));
        nd.num(k_dphi_q1_mv, fabs(qrk_mv_dphi_1));
        nd.num(k_jetdphimax, jet_dphi_max);
        nd.num(k_jetdetamax, jet_deta_max);
        nd.num(k_qrkdphimax, fabs(qrk_dphi_max));
        nd.num(k_jetdphi_mveta, fabs(jet_dphi_max), fabs(lsp_p4.Eta()));
        nd.num(k_jetmovea3d01, jet0_lsp_angle, jet1_lsp_angle);
        nd.num(k_jeteta01,  jet_eta_0, jet_eta_1);
        nd.num(k_jetpt01, jet_pt_0, jet_pt_1);
        nd.num(k_pt_angle0, jet_pt_0, jet0_lsp_angle);
        nd.num(k_pt_angle1, jet_pt_1, jet1_lsp_angle);
        nd.num(k_eta_angle0, lsp_p4.Eta(), jet0_lsp_angle);
        nd.num(k_eta_angle1, lsp_p4.Eta(), jet1_lsp_angle);
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
