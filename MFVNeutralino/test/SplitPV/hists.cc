#include "TH2.h"
#include "DVCode/MFVNeutralino/interface/Ntuple.h"
#include "DVCode/Tools/interface/NtupleReader.h"

int main(int argc, char** argv) {
  jmt::NtupleReader<mfv::SplitPVNtuple> nr;
  nr.init_options("mfvSplitPVs/t");
  if (!nr.parse_options(argc, argv) || !nr.init()) return 1;
  auto& nt = nr.nt();
  auto& pvs = nt.pvs();

  ////

  auto h_refit_dx = new TH1D("h_refit_dx", "", 1000, -1, 1);
  auto h_refit_dy = new TH1D("h_refit_dy", "", 1000, -1, 1);
  auto h_refit_dz = new TH1D("h_refit_dz", "", 1000, -1, 1);

  auto h_dx = new TH1D("h_dx", "", 1000, -1, 1);
  auto h_dy = new TH1D("h_dy", "", 1000, -1, 1);
  auto h_dz = new TH1D("h_dz", "", 1000, -1, 1);

  auto fcn = [&]() {
    const double w = nr.weight();
    auto fill = [&](auto* h, double x) { h->Fill(x, w); };

    int io = 0, ir = -1, __attribute__((unused)) il = -1, ia = -1, ib = -1;

    for (int i = 1, ie = pvs.n(); i < ie; ++i) {
      unsigned which = pvs.misc(i) & 0xFFFF;
      if      (which == 0) io = i;
      else if (which == 1) ir = i;
      else if (which == 2) il = i;
      else if (which == 3) ia = i;
      else if (which == 4) ib = i;
      //else printf("which is %u\n", which);
    }

    //printf("io %i ir %i il %i ia %i ib %i\n", io, ir, il, ia, ib);

    if (io != -1 && ir != -1) {
      fill(h_refit_dx, pvs.x(ir) - pvs.x(io));
      fill(h_refit_dy, pvs.y(ir) - pvs.y(io));
      fill(h_refit_dz, pvs.z(ir) - pvs.z(io));
    }

    if (ia != -1 && ib != -1) {
      fill(h_dx, pvs.x(ia) - pvs.x(ib));
      fill(h_dy, pvs.y(ia) - pvs.y(ib));
      fill(h_dz, pvs.z(ia) - pvs.z(ib));
    }

    return std::make_pair(true, w);
  };

  nr.loop(fcn);
}
