#include "Phi.h"
#include "TH1.h"

#include <cmath>

namespace mfv {
  const bool Phi::use_abs = false;
  const int Phi::nbins = 8;
  const double Phi::min = Phi::use_abs ? 0 : -M_PI;
  const double Phi::max = M_PI;

  TH1D* Phi::new_1d_hist(const char* name, const char* title) {
    return new TH1D(name, title, nbins, min, max);
  }
}
