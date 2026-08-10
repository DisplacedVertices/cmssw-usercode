#include "DataFormats/PatCandidates/interface/Jet.h"
#include "JMTucker/Tools/interface/AnalysisEras.h"
#include "JMTucker/Tools/interface/Geometry.h"
#include "JMTucker/Tools/interface/Year.h"

namespace jmt {
  namespace Geometry {
    bool inside_beampipe(bool is_mc, double x, double y) {
      int idx = (jmt::Year::get() == 20161 || jmt::Year::get() == 20162) ? 0 : jmt::Year::get() == 2017 ? 1 : 2;
      const double r = (idx == 0) ? 2.00 : 2.09;
      const double c[4][2] = { {0.124, 0.07}, {0.113, -0.180}, {0.171, -0.175}, {0,0} };
      const int i = is_mc ? 3 : idx;
      return std::hypot(x - c[i][0], y - c[i][1]) < r;
    }

    bool inside_beampipe(double x, double y) {
      return inside_beampipe(jmt::AnalysisEras::is_mc(), x, y);
    }
  }
}
