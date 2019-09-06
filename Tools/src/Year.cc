#include "JMTucker/Tools/interface/BTagging.h"
#include "JMTucker/Tools/interface/Year.h"

namespace jmt {
  void assert_year(int year) {
    bool ok = false;
    for (int y : MFVNEUTRALINO_YEARS)
      if (y == year)
        ok = true;
    assert(ok);
  }

  void set_year(int y, bool check=true) {
    if (check) assert_year(y);
    jmt::BTagging::set_year(y);
  }

  yearcode::yearcode(double cc)
    : year_(-1), nfiles_(-1)
  {
    double ip; assert(std::modf(cc, &ip) == 0.);
    const int c(cc);
    for (int y : MFVNEUTRALINO_YEARS) {
      const int cd = y * MFVNEUTRALINO_YEARCODE_MULT;
      if (c % cd == 0) {
        set_year(y, false);
        year_ = y;
        nfiles_ = c / cd;
        break;
      }
    }
  }
}
