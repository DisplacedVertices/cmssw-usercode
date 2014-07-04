#include "TFile.h"
#include "ToyThrower.h"

int main() {
  TFile f("throw_toys.root", "recreate");
  mfv::ToyThrower tt("", "crab/MiniTreeV18_Njets", &f);
  tt.throw_toy();
  tt.throw_toy();
  f.Write();
  f.Close();
}
