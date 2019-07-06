#include "TH2.h"
#include "JMTucker/MFVNeutralino/interface/Ntuple.h"
#include "JMTucker/Tools/interface/NtupleReader.h"

int main(int argc, char** argv) {
  jmt::NtupleReader<mfv::MiniNtuple2> nr;
  nr.init_options("mfvMiniTree2/t");
  if (!nr.parse_options(argc, argv) || !nr.init()) return 1;
  auto& nt = nr.nt();

  bool ok = true;

  nr.loop([&]() {
      for (int iv = 0, ive = nt.vertices().n(); iv < ive; ++iv) {
        int c = 0;
        for (int itk = 0, itke = nt.tracks().n(); itk < itke; ++itk)
          if (nt.tracks().which_sv(itk) == iv)
            ++c;
        if (c != nt.vertices().ntracks(iv)) {
          ok = false;
          printf("ntk %i c %i\n", nt.vertices().ntracks(iv), c);
        }
      }

      return std::make_pair(true, nr.weight());
    });

  if (!ok) {
    std::cerr << "not OK!\n";
    return 1;
  }
}
