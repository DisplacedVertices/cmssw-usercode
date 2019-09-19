#include "JMTucker/MFVNeutralino/interface/Ntuple.h"
#include "JMTucker/Tools/interface/NtupleReader.h"

int main(int argc, char** argv) {
  jmt::NtupleReader<mfv::MiniNtuple2> nr;
  nr.init_options("mfvMiniTree2/t", "CountV27mm", "nr_ntuplev27mm");
  if (!nr.parse_options(argc, argv) || !nr.init()) return 1;
  auto& nt = nr.nt();
  auto& bs = nt.bs();
  auto& vs = nt.vertices();

  auto h_dbs2derr = new TH1F("h_dbs2derr","",200,-0.01,0.01);
  auto h_bs2derr = new TH2F("h_bs2derr","",200,0,0.05,200,0,0.05);
  auto h_dntracks = new TH1F("h_dntracks", "", 100,-50,50);
  auto h_ntracks = new TH2F("h_ntracks", "", 100,0,100,100,0,100);
  auto h_dnjets = new TH1F("h_dnjets", "", 20,-10,10);
  auto h_njets = new TH2F("h_njets", "", 20,0,20,20,0,20);
  auto h_dpt = new TH1F("h_dpt","",200,-1,1);
  auto h_pt = new TH2F("h_pt","",200,0,2000,0,2000);
  auto h_deta = new TH1F("h_deta","",200,-0.1,0.1);
  auto h_eta = new TH2F("h_eta","",200,-2.6,2.6,200,-2.6,2.6);
  auto h_dphi = new TH1F("h_dphi","",200,-0.1,0.1);
  auto h_phi = new TH2F("h_phi","",200,-M_PI,M_PI,200,-M_PI,M_PI);
  auto h_dm = new TH1F("h_dm","",200,-1,1);
  auto h_m = new TH2F("h_m","",200,0,2000,200,0,2000);

  bool ok = true;

  nr.loop([&]() {
      for (int i = 0; i < vs.n(); ++i) {
        const float bs2derr = vs.bs2derr(i,bs);
        if (fabs(bs2derr - vs.bs2derr(i)) > 1e-4) { nr.print_event(false); printf(" calc bs2derr %g != stored %g\n", bs2derr, vs.bs2derr(i)); ok = false; }
        h_dbs2derr->Fill(bs2derr - vs.bs2derr(i));
        h_bs2derr->Fill(bs2derr, vs.bs2derr(i));

        const int ntracks = nt.vertex_tracks(i).size();
        if (ntracks != vs.ntracks(i)) { nr.print_event(false); printf(" found ntracks %i != stored %i\n", ntracks, vs.ntracks(i)); ok = false; }
        h_dntracks->Fill(ntracks - vs.ntracks(i));
        h_ntracks->Fill(ntracks, vs.ntracks(i));

        const int njets = nt.vertex_jets(i).size();
        if (njets != vs.njets(i)) { nr.print_event(false); printf(" found njets %i != stored %i\n", njets, vs.njets(i)); ok = false; }
        h_dnjets->Fill(njets - vs.njets(i));
        h_njets->Fill(njets, vs.njets(i));

        auto p4 = nt.vertex_tracks_jets_p4(i);
        h_dpt->Fill(p4.Pt() - vs.pt(i));
        h_pt->Fill(p4.Pt(), vs.pt(i));
        h_deta->Fill(p4.Eta() - vs.eta(i));
        h_eta->Fill(p4.Eta(), vs.eta(i));
        h_dphi->Fill(p4.Phi() - vs.phi(i));
        h_phi->Fill(p4.Phi(), vs.phi(i));
        h_dm->Fill(p4.M() - vs.mass(i));
        h_m->Fill(p4.M(), vs.mass(i));
      }

      NR_loop_continue;
    });

  if (!ok) {
    std::cerr << "not OK!\n";
    return 1;
  }
}
