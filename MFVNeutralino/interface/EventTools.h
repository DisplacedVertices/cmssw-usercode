#ifndef DVCode_MFVNeutralino_interface_EventTools_h
#define DVCode_MFVNeutralino_interface_EventTools_h

#include "LHAPDF/LHAPDF.h"
#include "LHAPDF/Info.h"
#include <stdexcept>

namespace mfv {

  LHAPDF::PDF* setupLHAPDF();
  double alphas(double q2);

  double renormalization_weight(double q, int up_or_dn);
  double factorization_weight(LHAPDF::PDF* pdf, double id1, double id2, double x1, double x2, double q, int up_or_dn);
}

#endif
