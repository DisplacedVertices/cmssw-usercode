#include "utils.h"

int main(int argc, char** argv) {
  double min_lspdist3 = 0.02;

  jmt::NtupleReader<mfv::MovedTracksNtuple> nr;
  namespace po = boost::program_options;
  nr.init_options("mfvMovedTreeMCTruth/t")
    ("min-lspdist3", po::value<double>(&min_lspdist3)->default_value(0.02), "min distance between LSP decays to use event")
    ;

  if (!nr.parse_options(argc, argv)) return 1;
  std::cout << " min_lspdist3: " << min_lspdist3 << "\n";

  if (!nr.init()) return 1;
  auto& nt = nr.nt();

  ////

  const int num_numdens = 3;

  numdens nds[num_numdens] = {
    numdens("nocuts"),
    numdens("ntracks"),
    numdens("all")
  };

  enum { k_decay_x, k_decay_y, k_decay_z, k_lspdist2, k_lspdist3, k_lspdistz, k_movedist2, k_movedist3, k_lspeta, k_npv, k_pvz, k_pvrho, k_pvntracks, k_pvscore, k_ht, k_jet_asymm, k_angle0, k_angle1, k_pt0, k_pt1, k_ntks_j0, k_ntks_j1, k_angle0_angle1, k_eta0_eta1, k_pt0_pt1, k_pt_angle0, k_pt_angle1, k_eta_angle0, k_eta_angle1 };
  for (numdens& nd : nds) {
    nd.book(k_decay_x,  "decay_x" , ";SV Decay X-pos [cm]; arb. units", 100, -4, 4);
    nd.book(k_decay_y,  "decay_y" , ";SV Decay Y-pos [cm]; arb. units", 100, -4, 4);
    nd.book(k_decay_z,  "decay_z" , ";SV Decay Z-pos [cm]; arb. units", 100, -20, 20);
    nd.book(k_lspdist2, "lspdist2", ";2-dist between gen verts;events/0.01 cm", 200, 0, 2);
    nd.book(k_lspdist3, "lspdist3", ";3-dist between gen verts;events/0.01 cm", 200, 0, 2);
    nd.book(k_lspdistz, "lspdistz", ";z-dist between gen verts;events/0.01 cm", 200, 0, 2);
    nd.book(k_movedist2, "movedist2", ";movement 2-dist;events/0.01 cm", 200, 0, 2);
    nd.book(k_movedist3, "movedist3", ";movement 3-dist;events/0.01 cm", 200, 0, 2);
    nd.book(k_lspeta,    "movevectoreta"   , ";move vector eta;events/0.08 cm", 100, -4, 4);
    nd.book(k_npv, "npv", ";# PV;events/1", 100, 0, 100);
    nd.book(k_pvz, "pvz", ";PV z (cm);events/0.24 cm", 200, -24, 24);
    nd.book(k_pvrho, "pvrho", ";PV #rho (cm);events/1 #mum", 200, 0, 0.02);
    nd.book(k_pvntracks, "pvntracks", ";PV # tracks;events/2", 200, 0, 400);
    nd.book(k_pvscore, "pvscore", ";PV #Sigma p_{T}^{2} (GeV^{2});events/200 GeV^{2}", 200, 0, 40000);
    nd.book(k_ht, "ht", ";#Sigma H_{T} (GeV);events/50 GeV", 50, 0, 2500);
    nd.book(k_jet_asymm, "jet_asymm", ";Jet asymmetry A_{J}; arb. units", 25, 0, 1);
    nd.book(k_angle0, "jetmovea3d0", ";Angle between jet0 and SV;arb. units", 63, 0, M_PI);
    nd.book(k_angle1, "jetmovea3d1", ";Angle between jet1 and SV;arb. units", 63, 0, M_PI);
    nd.book(k_pt0,     "pt0",     ";Pt of jet0 [GeV]", 50, 0, 2500);
    nd.book(k_pt1,     "pt1",     ";Pt of jet1 [GeV]", 50, 0, 2500);
    nd.book(k_ntks_j0,"ntks_j0",";Ntks in jet0", 50, 0, 50);
    nd.book(k_ntks_j1,"ntks_j1",";Ntks in jet1", 50, 0, 50);

    nd.book(k_angle0_angle1, "angle0_angle1", ";Angle between jet0 and SV;Angle between jet1 and SV", 63, 0, M_PI, 63, 0, M_PI);
    nd.book(k_eta0_eta1,     "eta0_eta1"    , ";Eta of jet0; Eta of jet1"                   , 60, -5, 5, 60, -5, 5);
    nd.book(k_pt0_pt1,       "pt0_pt1"        , ";Pt of jet0 [GeV]; Pt of jet1 [GeV]"           , 50, 0, 2500, 50, 0, 2500);
    nd.book(k_pt_angle0,     "pt_angle0"    , ";Pt of jet0 [GeV]; Angle between jet0 and SV", 50, 0, 2500, 63, 0, M_PI);
    nd.book(k_pt_angle1,     "pt_angle1"    , ";Pt of jet1 [GeV]; Angle between jet1 and SV", 50, 0, 2500, 63, 0, M_PI);
    nd.book(k_eta_angle0,    "eta_angle0"  , ";Eta of SV decay vector; Angle between jet0 and SV", 60, -5, 5, 63, 0, M_PI);
    nd.book(k_eta_angle1,    "eta_angle1"  , ";Eta of SV decay vector; Angle between jet1 and SV", 60, -5, 5, 63, 0, M_PI);
  }

  TH1D* h_vtxntracks[num_numdens] = {0};
  TH1D* h_vtxbs2derr[num_numdens] = {0};
  TH1D* h_vtxtkonlymass[num_numdens] = {0};
  TH1D* h_vtxs_mass[num_numdens] = {0};

  for (int i = 0; i < num_numdens; ++i) {
    h_vtxntracks[i] = new TH1D(TString::Format("h_%i_vtxntracks",      i), ";# tracks in largest vertex;events/1", 40, 0, 40);
    h_vtxbs2derr[i] = new TH1D(TString::Format("h_%i_vtxbs2derr",      i), ";#sigma(d_{BV}) of largest vertex (cm);events/2 #mum", 50, 0, 0.01);
    h_vtxtkonlymass[i] = new TH1D(TString::Format("h_%i_vtxtkonlymass", i), ";track-only mass of largest vertex (GeV);events/1 GeV", 500, 0, 500);
    h_vtxs_mass[i] = new TH1D(TString::Format("h_%i_vtxs_mass", i), ";track+jets mass of largest vertex (GeV);vertices/50 GeV", 100, 0, 5000);
  }

  double den = 0;
  std::map<std::string, double> nums;

  auto fcn = [&]() {
    double w = nr.weight();
    if (!nt.gentruth().valid() || nt.jets().ht() < 1200 || nt.jets().nminpt() < 4 || nt.gentruth().lspdist3() < min_lspdist3)
      return std::make_pair(true, w);

    auto F1 = [&w](TH1* h, double v)            { h                    ->Fill(v,     w); };
    auto F2 = [&w](TH1* h, double v, double v2) { dynamic_cast<TH2*>(h)->Fill(v, v2, w); };

    const size_t nvtx = nt.vertices().n();
    const double lspdist2 = nt.gentruth().lspdist2();
    const double lspdist3 = nt.gentruth().lspdist3();
    const double lspdistz = nt.gentruth().lspdistz();

    // Loop over each LSP
    for (int ilsp = 0; ilsp < 2; ++ilsp) {
      const TVector3 lspdecay = nt.gentruth().decay(ilsp, nt.bs());  // JMTBAD BS BS
      const double movedist2 = lspdecay.Perp();
      const double movedist3 = lspdecay.Mag();


      // Match decay daughters to the closest (by dR) jet
      std::vector<int> closest_jets;
      std::vector<int> quark_assoc;
      for (int i=0, iend = nt.gentruth().n(); i < iend; i++) {
          if (nt.gentruth().id(ilsp) == 1000006 && nt.gentruth().id(i) != -1) continue;
          if (nt.gentruth().id(ilsp) == -1000006 && nt.gentruth().id(i) != 1) continue;
          int i_closest_jet = -1;
          double closest_jet_dr = 0.4;
          for (int j=0, jend = nt.jets().n(); j < jend; j++) {
              if (nt.gentruth().p4(i).DeltaR(nt.jets().p4(j)) < closest_jet_dr) {
                  closest_jet_dr = nt.gentruth().p4(i).DeltaR(nt.jets().p4(j));  //dR between dbar and jet
                  i_closest_jet = j;
              }
          }
        closest_jets.push_back(i_closest_jet);
        quark_assoc.push_back(i);
      }

      // If, for some reason, a daughter doesn't match to a jet, continue. Also, if both daughters match
      // to the same jet, continue.
      if (closest_jets[0] == -1 || closest_jets[1] == -1 || closest_jets[0] == closest_jets[1]) continue;
      
      // Calculate some relevant jet variables
      double jet0_lsp_angle = nt.jets().p4(closest_jets[0]).Angle(nt.gentruth().p4(ilsp).Vect());
      double jet1_lsp_angle = nt.jets().p4(closest_jets[1]).Angle(nt.gentruth().p4(ilsp).Vect());
      const TLorentzVector jet_tot_p4 = nt.jets().p4(closest_jets[0])+nt.jets().p4(closest_jets[1]);
      const double jet_tot_mass = jet_tot_p4.M();
      
      // If the jets don't have an invariant mass within 80% of the LSP, continue.
      if (jet_tot_mass > 1.2*nt.gentruth().mass(ilsp) || jet_tot_mass < 0.8*nt.gentruth().mass(ilsp)) continue;


      // Make sure that jet0 corresponds to the higher-momentum daughter
      if (nt.gentruth().p4(quark_assoc[0]).Pt() < nt.gentruth().p4(quark_assoc[1]).Pt()) {
        int hold_jetIndex = closest_jets[0];
        int hold_qrkIndex = quark_assoc[0];
        double hold_angle = jet0_lsp_angle;

        closest_jets[0] = closest_jets[1];
        closest_jets[1] = hold_jetIndex;

        quark_assoc[0] = quark_assoc[1];
        quark_assoc[1] = hold_qrkIndex;

        jet0_lsp_angle = jet1_lsp_angle;
        jet1_lsp_angle = hold_angle;
      }

      const float jet_aj = (nt.jets().p4(closest_jets[0]).Pt() - nt.jets().p4(closest_jets[1]).Pt()) / (nt.jets().p4(closest_jets[0]).Pt() + nt.jets().p4(closest_jets[1]).Pt());

      if (movedist2 > 2.0 ||
          movedist2 < 0.01)
        continue;

      for (numdens& nd : nds) {
        F1(nd(k_decay_x)  .den, lspdecay.x());
        F1(nd(k_decay_y)  .den, lspdecay.y());
        F1(nd(k_decay_z)  .den, lspdecay.z());
        F1(nd(k_lspdist2) .den, lspdist2);
        F1(nd(k_lspdist3) .den, lspdist3);
        F1(nd(k_lspdistz) .den, lspdistz);
        F1(nd(k_movedist2).den, movedist2);
        F1(nd(k_movedist3).den, movedist3);
        F1(nd(k_lspeta)   .den, nt.gentruth().p4(ilsp).Eta());
        F1(nd(k_npv)      .den, nt.pvs().n());
        F1(nd(k_pvz)      .den, nt.pvs().z(0));
        F1(nd(k_pvrho)    .den, nt.pvs().rho(0));
        F1(nd(k_pvntracks).den, nt.pvs().ntracks(0));
        F1(nd(k_pvscore)  .den, nt.pvs().score(0));
        F1(nd(k_ht)       .den, nt.jets().ht());
        F1(nd(k_jet_asymm).den, jet_aj);
        F1(nd(k_angle0)   .den, jet0_lsp_angle);
        F1(nd(k_angle1)   .den, jet1_lsp_angle);
        F1(nd(k_pt0)       .den, nt.jets().p4(closest_jets[0]).Pt());
        F1(nd(k_pt1)       .den, nt.jets().p4(closest_jets[1]).Pt());
        F1(nd(k_ntks_j0)  .den, (int)nt.jets().ntracks(closest_jets[0]));
        F1(nd(k_ntks_j1)  .den, (int)nt.jets().ntracks(closest_jets[1]));

        F2(nd(k_angle0_angle1)   .den, jet0_lsp_angle, jet1_lsp_angle);
        F2(nd(k_eta0_eta1)       .den, nt.jets().p4(closest_jets[0]).Eta(), nt.jets().p4(closest_jets[1]).Eta());
        F2(nd(k_pt0_pt1)         .den, nt.jets().p4(closest_jets[0]).Pt(), nt.jets().p4(closest_jets[1]).Pt());
        F2(nd(k_pt_angle0)       .den, nt.jets().p4(closest_jets[0]).Pt(), jet0_lsp_angle);
        F2(nd(k_pt_angle1)       .den, nt.jets().p4(closest_jets[1]).Pt(), jet1_lsp_angle);
        F2(nd(k_eta_angle0)      .den, nt.gentruth().p4(ilsp).Eta(), jet0_lsp_angle);
        F2(nd(k_eta_angle1)      .den, nt.gentruth().p4(ilsp).Eta(), jet1_lsp_angle);
      }

      den += w;

      int n_pass_nocuts = 0;
      int n_pass_ntracks = 0;
      int n_pass_all = 0;

      std::vector<int> first_vtx_to_pass(num_numdens, -1);
      auto set_it_if_first = [](int& to_set, int to_set_to) { if (to_set == -1) to_set = to_set_to; };

      for (size_t i = 0; i < nvtx; ++i) {
        const double dist2move = (lspdecay - nt.vertices().pos(i)).Mag();
        if (dist2move > 0.0084)
          continue;

        const bool pass_ntracks = nt.vertices().ntracks(i) >= 5;
        const bool pass_bs2derr = nt.vertices().bs2derr(i) < 0.0025;

        if (1)                             { set_it_if_first(first_vtx_to_pass[0], i); ++n_pass_nocuts;  }
        if (pass_ntracks)                  { set_it_if_first(first_vtx_to_pass[1], i); ++n_pass_ntracks; }
        if (pass_ntracks && pass_bs2derr)  { set_it_if_first(first_vtx_to_pass[2], i); ++n_pass_all;     }
      }

      for (int in = 0; in < num_numdens; ++in) {
        const int iv = first_vtx_to_pass[in];
        if (iv != -1) {
          h_vtxntracks   [in]->Fill(nt.vertices().ntracks(iv));
          h_vtxbs2derr   [in]->Fill(nt.vertices().bs2derr(iv));
	  h_vtxtkonlymass[in]->Fill(nt.vertices().tkonlymass(iv));
	  h_vtxs_mass    [in]->Fill(nt.vertices().mass(iv));
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
        F1(nd(k_decay_x)  .num, lspdecay.x());
        F1(nd(k_decay_y)  .num, lspdecay.y());
        F1(nd(k_decay_z)  .num, lspdecay.z());
        F1(nd(k_lspdist2) .num, lspdist2);
        F1(nd(k_lspdist3) .num, lspdist3);
        F1(nd(k_lspdistz) .num, lspdistz);
        F1(nd(k_movedist2).num, movedist2);
        F1(nd(k_movedist3).num, movedist3);
        F1(nd(k_lspeta)   .num, nt.gentruth().p4(ilsp).Eta());
        F1(nd(k_npv)      .num, nt.pvs().n());
        F1(nd(k_pvz)      .num, nt.pvs().z(0));
        F1(nd(k_pvrho)    .num, nt.pvs().rho(0));
        F1(nd(k_pvntracks).num, nt.pvs().ntracks(0));
        F1(nd(k_pvscore)  .num, nt.pvs().score(0));
        F1(nd(k_ht)       .num, nt.jets().ht());
        F1(nd(k_jet_asymm).num, jet_aj);
        F1(nd(k_angle0)   .num, jet0_lsp_angle);
        F1(nd(k_angle1)   .num, jet1_lsp_angle);
        F1(nd(k_pt0)       .num, nt.jets().p4(closest_jets[0]).Pt());
        F1(nd(k_pt1)       .num, nt.jets().p4(closest_jets[1]).Pt());
        F1(nd(k_ntks_j0)  .num, (int)nt.jets().ntracks(closest_jets[0]));
        F1(nd(k_ntks_j1)  .num, (int)nt.jets().ntracks(closest_jets[1]));

        F2(nd(k_angle0_angle1)   .num, jet0_lsp_angle, jet1_lsp_angle);
        F2(nd(k_eta0_eta1)       .num, nt.jets().p4(closest_jets[0]).Eta(), nt.jets().p4(closest_jets[1]).Eta());
        F2(nd(k_pt0_pt1)         .num, nt.jets().p4(closest_jets[0]).Pt(), nt.jets().p4(closest_jets[1]).Pt());
        F2(nd(k_pt_angle0)       .num, nt.jets().p4(closest_jets[0]).Pt(), jet0_lsp_angle);
        F2(nd(k_pt_angle1)       .num, nt.jets().p4(closest_jets[1]).Pt(), jet1_lsp_angle);
        F2(nd(k_eta_angle0)      .num, nt.gentruth().p4(ilsp).Eta(), jet0_lsp_angle);
        F2(nd(k_eta_angle1)      .num, nt.gentruth().p4(ilsp).Eta(), jet1_lsp_angle);
      }
    }

    return std::make_pair(true, w);
  };

  nr.loop(fcn);

  printf("%12.1f", den);
  for (const std::string& c : {"nocuts", "ntracks", "all"}) {
    const jmt::interval i = jmt::clopper_pearson_binom(nums[c], den);
    printf("    %6.4f +- %6.4f", i.value, i.error());
  }
  printf("\n");
}
