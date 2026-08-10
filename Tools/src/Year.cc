#include "JMTucker/Tools/interface/Year.h"
#include <cmath>
#include <initializer_list>
#include <limits>
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
    typedef unsigned long long ull;
    double ip;
    if (cc < 0 || cc > std::numeric_limits<ull>::max() ||
        std::modf(cc, &ip) != 0.)
      throw std::invalid_argument("bad double yearcode");
    const ull c(cc);
    for (int y : MFVNEUTRALINO_YEARS) {
      const ull cd = y * MFVNEUTRALINO_YEARCODE_MULT;
      if (c % cd == 0) {
        Year::set(year_ = y, false);
        const ull nf = c / cd;
        if (nf > std::numeric_limits<int>::max()) throw std::overflow_error("nfiles overflow");
        nfiles_ = nf;
        break;
      }
    }
  }
}
