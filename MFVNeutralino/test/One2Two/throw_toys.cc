#include "TFile.h"
#include "ToyThrower.h"

int main(int argc, char** argv) {
  SetROOTStyle();

  int ntoys = argc > 1 ? atoi(argv[1]) : 1;

  TFile f("throw_toys.root", "recreate");
  mfv::ToyThrower tt("", "crab/MiniTreeV18_Njets", &f);

  for (int i = 0; i < ntoys; ++i)
    tt.throw_toy();

  f.Write();
  f.Close();
}
