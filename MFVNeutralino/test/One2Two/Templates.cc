#include "Templates.h"

#include "TH1D.h"

namespace mfv {
  const int Template::max_npars = 3;

  //////////////////////////////////////////////////////////////////////////////

  PhiShiftTemplate::PhiShiftTemplate(int i_, TH1D* h_, const double phi_exp_, const double shift_)
    : Template(i_, h_),
      phi_exp(phi_exp_),
      shift(shift_)
  {
  }

  double PhiShiftTemplate::chi2() const {
    return 0; // pow(phi_exp - 1.7, 2)/0.7
  }

  std::string PhiShiftTemplate::name() const {
    char buf[128];
    snprintf(buf, 128, "phishift%04i", i);
    return std::string(buf);
  }

  std::string PhiShiftTemplate::title() const {
    char buf[128];
    snprintf(buf, 128, "phi_exp = %f, shift = %g", phi_exp, shift);
    return std::string(buf);
  }

  double PhiShiftTemplate::par(size_t w) const {
    if (w == 0)
      return phi_exp;
    else if (w == 1)
      return shift;
    else
      return 0.;
  }

  //////////////////////////////////////////////////////////////////////////////

  ClearedJetsTemplate::ClearedJetsTemplate(int i_, TH1D* h_)
    : Template(i_, h_)
  {
  }
}
