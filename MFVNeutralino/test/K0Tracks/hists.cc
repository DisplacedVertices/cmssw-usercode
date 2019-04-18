#include "TH2.h"
#include "JMTucker/MFVNeutralino/interface/Ntuple.h"
#include "JMTucker/Tools/interface/NtupleReader.h"

int main(int argc, char** argv) {
  jmt::NtupleReader<mfv::K0Ntuple> nr;
  nr.init_options("mfvK0s/t");
  if (!nr.parse_options(argc, argv) || !nr.init()) return 1;
  auto& nt = nr.nt();
  auto& ntt = nt.tracks();

  ////

  const double mpion = 0.13957;

  enum { mass_all, mass_lo, mass_hi, mass_on, max_mass_type };
  const char* mass_names[max_mass_type] = {"massall", "masslo", "masshi", "masson"};

  TH1D* h_nvtx[max_mass_type];
  TH1D* h_premass[max_mass_type];
  TH1D* h_mass[max_mass_type];
  TH1D* h_pt[max_mass_type];
  TH1D* h_eta[max_mass_type];
  TH1D* h_phi[max_mass_type];
  TH1D* h_costh[max_mass_type];
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

  for (int i = 0; i < max_mass_type; ++i) {
    TDirectory* d = nr.f_out().mkdir(mass_names[i]);
    d->cd();

    h_nvtx[i] = new TH1D("h_nvtx", ";# of K0 candidates;events", 30, 0, 30);
    h_premass[i] = new TH1D("h_premass", ";K0 candidate pre-fit mass (GeV);cands/5 MeV", 400, 0, 2);
    h_mass[i] = new TH1D("h_mass", ";K0 candidate mass (GeV);cands/5 MeV", 400, 0, 2);
    h_pt[i] = new TH1D("h_pt", ";K0 candidate p_{T} (GeV);cands/5 GeV", 100, 0, 500);
    h_eta[i] = new TH1D("h_eta", ";K0 candidate #eta;cands/0.05", 100, -2.5, 2.5);
    h_phi[i] = new TH1D("h_phi", ";K0 candidate #phi;cands/0.063", 100, -M_PI, M_PI);
    h_costh[i] = new TH1D("h_costh", ";K0 candidate cos(angle{flight,momentum});cands/0.01", 202, -1.01, 1.01);
    h_ct[i] = new TH1D("h_ct", ";K0 candidate ct (cm);cands/0.01", 100, 0, 10);
    h_ctau[i] = new TH1D("h_ctau", ";K0 candidate c#tau (cm);cands/0.01", 100, 0, 10);
    h_rho[i] = new TH1D("h_rho", ";K0 candidate #rho (cm);cands/0.01", 100, 0, 10);
    h_tracks_pt[i] = new TH1D("h_tracks_pt", ";tracks pt;arb. units", 2000, 0, 200);
    h_tracks_eta[i] = new TH1D("h_tracks_eta", ";tracks eta;arb. units", 50, -4, 4);
    h_tracks_phi[i] = new TH1D("h_tracks_phi", ";tracks phi;arb. units", 315, -3.15, 3.15);
    h_tracks_dxy[i] = new TH1D("h_tracks_dxy", ";tracks dxy to beamspot;arb. units", 400, -0.2, 0.2);
    h_tracks_absdxy[i] = new TH1D("h_tracks_absdxy", ";tracks |dxy| to beamspot;arb. units", 200, 0, 0.2);
    h_tracks_dz[i] = new TH1D("h_tracks_dz", ";tracks dz to BS;arb. units", 400, -20, 20);
    h_tracks_dzpv[i] = new TH1D("h_tracks_dzpv", ";tracks dz to PV;arb. units", 400, -20, 20);
    h_tracks_nhits[i] = new TH1D("h_tracks_nhits", ";tracks nhits;arb. units", 40, 0, 40);
    h_tracks_npxhits[i] = new TH1D("h_tracks_npxhits", ";tracks npxhits;arb. units", 40, 0, 40);
    h_tracks_nsthits[i] = new TH1D("h_tracks_nsthits", ";tracks nsthits;arb. units", 40, 0, 40);
    h_tracks_min_r[i] = new TH1D("h_tracks_min_r", ";tracks min_r;arb. units", 20, 0, 20);
    h_tracks_npxlayers[i] = new TH1D("h_tracks_npxlayers", ";tracks npxlayers;arb. units", 20, 0, 20);
    h_tracks_nstlayers[i] = new TH1D("h_tracks_nstlayers", ";tracks nstlayers;arb. units", 20, 0, 20);
    h_tracks_nsigmadxy[i] = new TH1D("h_tracks_nsigmadxy", ";tracks nsigmadxy;arb. units", 400, 0, 40);
    h_tracks_dxyerr[i] = new TH1D("h_tracks_dxyerr", ";tracks dxyerr;arb. units", 2000, 0, 0.2);
    h_tracks_dzerr[i] = new TH1D("h_tracks_dzerr", ";tracks dzerr;arb. units", 2000, 0, 0.2);
    h_tracks_dszerr[i] = new TH1D("h_tracks_dszerr", ";tracks dszerr;arb. units", 2000, 0, 0.2);
    h_tracks_lambdaerr[i] = new TH1D("h_tracks_lambdaerr", ";tracks lambdaerr;arb. units", 2000, 0, 0.2);
    h_tracks_pterr[i] = new TH1D("h_tracks_pterr", ";tracks pterr;arb. units", 200, 0, 0.2);
    h_tracks_phierr[i] = new TH1D("h_tracks_phierr", ";tracks phierr;arb. units", 200, 0, 0.2);
    h_tracks_etaerr[i] = new TH1D("h_tracks_etaerr", ";tracks etaerr;arb. units", 200, 0, 0.2);
  }

  nr.f_out().cd();

  auto fcn = [&]() {
    const double w = nr.weight();
    auto fill = [&](auto* h, double x) { h->Fill(x, w); };

    const TVector3 pv = nt.pvs().pos(0);

    int nvtx[max_mass_type] = {0};

    for (int isv = 0, isve = nt.svs().n(); isv < isve; ++isv) {
      const TVector3 pos = nt.svs().pos(isv);
      const TVector3 flight = pos - pv;
      const double rho = flight.Perp();

      if (rho > 2.)
        continue;

      const int itk = nt.svs().misc(isv) & 0xFFFF;
      const int jtk = nt.svs().misc(isv) >> 16;

      if (!ntt.pass_sel(itk) || !ntt.pass_sel(jtk))
        continue;

      const int irftk = 2*isv;
      const int jrftk = 2*isv+1;

      const TLorentzVector ip4 = ntt.p4(itk, mpion);
      const TLorentzVector jp4 = ntt.p4(jtk, mpion);
      const TLorentzVector prep4 = ip4 + jp4;

      const TLorentzVector irfp4 = nt.refit_tks().p4(irftk, mpion);
      const TLorentzVector jrfp4 = nt.refit_tks().p4(jrftk, mpion);
      const TLorentzVector p4 = irfp4 + jrfp4;

      const double mass = p4.M();
      const double costh = p4.Vect().Unit().Dot(flight.Unit());
      const double ct = flight.Mag();
      const double ctau = ct / p4.Beta() / p4.Gamma();

      int imass2 = mass_on;
      if      (mass < 0.490) imass2 = mass_lo;
      else if (mass > 0.505) imass2 = mass_hi;

      for (int ii : {0,1}) {
        const int imass = ii == 0 ? mass_all : imass2;

        fill(h_premass[imass], prep4.M());
        fill(h_mass[imass], mass);
        fill(h_pt[imass], p4.Pt());
        fill(h_eta[imass], p4.Eta());
        fill(h_phi[imass], p4.Phi());
        fill(h_costh[imass], costh);
        fill(h_ct[imass], ct);
        fill(h_ctau[imass], ctau);
        fill(h_rho[imass], rho);

        for (int tki : {itk, jtk}) {
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
        }

        ++nvtx[imass];
      }
    }

    for (int i = 0; i < max_mass_type; ++i)
      fill(h_nvtx[i], nvtx[i]);

    return std::make_pair(true, w);
  };

  nr.loop(fcn);
}
