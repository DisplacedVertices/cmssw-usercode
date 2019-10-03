#include "JMTucker/MFVNeutralino/interface/Ntuple.h"
#include "JMTucker/Tools/interface/NtupleReader.h"

int main(int argc, char** argv) {
  jmt::NtupleReader<mfv::MiniNtuple2> nr;
  nr.init_options("mfvMiniTree2/t");
  if (!nr.parse_options(argc, argv) || !nr.init()) return 1;
  auto& nt = nr.nt();
  auto& gen = nt.gentruth();
  auto& bs = nt.bs();
  auto& jets = nt.jets();
  auto& vs = nt.vertices();

  nr.loop([&]() {
      nr.print_event();
      printf("gen truth: valid? %i  pp vtx: %f %f %f  saw c? %i b? %i\n", gen.valid(), gen.vx(), gen.vy(), gen.vz(), gen.saw_c(), gen.saw_b());
      if (gen.valid()) {
        printf("  lspdist2: %10.4f  3: %10.4f  %i truth particles:\n", gen.lspdist2(), gen.lspdist3(), gen.n());
        printf("    %3s %10s %10s %10s %10s %10s %10s %10s %10s\n","i", "id","pt","eta","phi","mass","decay x", "y", "z");
        for (int i = 0; i < gen.n(); ++i)
          printf("    %3i %10i %10.4f %10.4f %10.4f %10.4f %10.4f %10.4f %10.4f\n",
                 i, gen.id(i), gen.pt(i), gen.eta(i), gen.phi(i), gen.mass(i), gen.decay_x(i), gen.decay_y(i), gen.decay_z(i));
      }

      printf("beamspot: %f %f %f dxdz %g dydz %g   njets %2i ht: %10.2f\n",
             bs.x(), bs.y(), bs.z(), bs.dxdz(), bs.dydz(), jets.n(), jets.ht());

      auto vclasses = nt.classify_vertices(jmt::AnalysisEras::is_mc());

      printf("%i raw vertices:\n", vs.n());
      printf("    %3s %5s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %5s %5s\n", "i", "ntks", "x", "y", "z", "cxx","cxy","cxz","cyy","cyz","czz", "dbv", "edbv", "inbp", "pass");
      for (int i = 0, ie = vs.n(); i < ie; ++i)
        printf("    %3i %5i %10.4f %10.4f %10.4f %10.3g %10.3g %10.3g %10.3g %10.3g %10.3g %10.4f %10.4f %5i %5i\n",
               i, vs.ntracks(i),
               vs.x(i), vs.y(i), vs.z(i), vs.cxx(i), vs.cxy(i), vs.cxz(i), vs.cyy(i), vs.cyz(i), vs.czz(i),
               vs.dbv(i, bs), vs.edbv(i), vs.inside_beampipe(i), vs.pass(i,bs));

      for (int ntk : {7,3,4,5}) {
        const int n = vclasses[ntk].size();
        printf("  n%i: %2i", ntk, n);
        if (n >= 2) {
          const int i0 = vclasses[ntk][0];
          const int i1 = vclasses[ntk][1];
          printf(" dvv %i-%i: %10.4f", i0, i1, nt.dvv(i0, i1));
        }
        printf("\n");
      }

      NR_loop_continue;
    });
}
