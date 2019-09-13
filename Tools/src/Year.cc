#include "JMTucker/Tools/interface/Year.h"
#include <cmath>
#include <initializer_list>
#include <stdexcept>

namespace jmt {
  int Year::year_ = MFVNEUTRALINO_YEAR;

  void Year::check(int y) {
    bool ok = false;
    for (int y2 : MFVNEUTRALINO_YEARS)
      if (y == y2)
        ok = true;
    if (!ok)
      throw std::invalid_argument("bad year");
  }

  yearcode::yearcode(double cc)
    : year_(-1), nfiles_(-1)
  {
    double ip; if (std::modf(cc, &ip) != 0.) throw std::invalid_argument("bad double yearcode");
    const int c(cc);
    for (int y : MFVNEUTRALINO_YEARS) {
      const int cd = y * MFVNEUTRALINO_YEARCODE_MULT;
      if (c % cd == 0) {
        Year::set(year_ = y, false);
        nfiles_ = c / cd;
        break;
      }
    }
  }
}
