#include "TH2.h"
#include "JMTucker/MFVNeutralino/interface/Ntuple.h"
#include "JMTucker/Tools/interface/NtupleReader.h"

int main(int argc, char** argv) {
  jmt::NtupleReader<mfv::K0Ntuple> nr;
  nr.init_options("mfvK0s/t");
  if (!nr.parse_options(argc, argv) || !nr.init()) return 1;
  auto& nt = nr.nt();

  ////

  const double mpi = 0.13957;

  auto h_premass = new TH1D("h_premass", ";SV mass before refit (GeV);vertices/5 MeV", 400, 0, 2);
  auto h_mass = new TH1D("h_mass", ";SV mass (GeV);vertices/5 MeV", 400, 0, 2);
  auto h_costh = new TH1D("h_costh", ";costh;vertices/0.001", 2002, -1.001, 1.001);

  auto fcn = [&]() {
    const double w = nr.weight();
    auto fill = [&](auto* h, double x) { h->Fill(x, w); };

    const TVector3 pv = nt.pvs().pos(0);

    for (int isv = 0, isve = nt.svs().n(); isv < isve; ++isv) {
      const TVector3 pos = nt.svs().pos(isv);
      const TVector3 flight = pos - pv;

      const int itk = nt.svs().misc(isv) & 0xFFFF;
      const int jtk = nt.svs().misc(isv) >> 16;
      const int irftk = 2*isv;
      const int jrftk = 2*isv+1;

      const TLorentzVector ip4 = nt.tracks().p4(itk, mpi);
      const TLorentzVector jp4 = nt.tracks().p4(jtk, mpi);
      const TLorentzVector irfp4 = nt.refit_tks().p4(irftk, mpi);
      const TLorentzVector jrfp4 = nt.refit_tks().p4(jrftk, mpi);

      const TLorentzVector prep4 = ip4 + jp4;
      const TLorentzVector p4 = irfp4 + jrfp4;
      const TVector3 momdir = p4.Vect().Unit();

      const double costh = momdir.Dot(flight.Unit());
      const double mass = p4.M();

      fill(h_premass, prep4.M());
      fill(h_mass, mass);
      fill(h_costh, costh);
    }

    return std::make_pair(true, w);
  };

  nr.loop(fcn);
}
