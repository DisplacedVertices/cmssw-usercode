#include "utils.h"

int main(int argc, char** argv) {
  int njets, nbjets;

  jmt::NtupleReader<mfv::MovedTracksNtuple> nr;
  namespace po = boost::program_options;
  nr.init_options("mfvMovedTree20/t")
    ("njets",  po::value<int>(&njets) ->default_value(2), "njets")
    ("nbjets", po::value<int>(&nbjets)->default_value(0), "nbjets")
    ;

  if (!nr.parse_options(argc, argv)) return 1;
  std::cout << " njets: " << njets << " nbjets: " << nbjets << "\n";

  if (!nr.init()) return 1;
  auto& nt = nr.nt();

  bool ok = true;

  auto fcn = [&]() {
    if (nt.tm().npreseljets() < njets || nt.tm().npreselbjets() < nbjets) {
      ok = false;
      std::cout << "bad event with " << +nt.tm().npreseljets() << "," << +nt.tm().npreselbjets() << ": " << nt.base().run() << "," << nt.base().lumi() << "," << nt.base().event() << "\n";
    }

    return std::make_pair(true, nr.weight());
  };

  nr.loop(fcn);

  printf(ok ? "\nkein problem\n" : "\nscheisse\n");
  return !ok;
}
