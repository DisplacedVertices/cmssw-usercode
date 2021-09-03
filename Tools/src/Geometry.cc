#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DVCode/Tools/interface/AnalysisEras.h"
#include "DVCode/Tools/interface/Geometry.h"
#include "DVCode/Tools/interface/Year.h"

namespace jmt {
  namespace Geometry {
    bool inside_beampipe(bool is_mc, double x, double y) {
      const double r = 2.09;
      const double c[3][2] = { {0.113, -0.180}, {0.171, -0.175}, {0,0} };
      const int i = is_mc ? 2 : jmt::Year::get()-2017;
      return std::hypot(x - c[i][0], y - c[i][1]) < r;
    }

    bool inside_beampipe(double x, double y) {
      return inside_beampipe(jmt::AnalysisEras::is_mc(), x, y);
    }
  }
}
