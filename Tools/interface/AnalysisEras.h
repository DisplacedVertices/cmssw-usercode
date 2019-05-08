#ifndef JMTucker_Tools_Eras_h
#define JMTucker_Tools_Eras_h

#include <random>
#include <vector>
#include "JMTucker/Tools/interface/Framework.h"

namespace jmt {
  class AnalysisEras {
  public:
    enum { e_2017B, e_2017C, e_2017D, e_2017E, e_2017F, e_2018A, e_2018B, e_2018C, e_2018D, e_max };

    static const double int_lumi(int e) { return int_lumi_[e]; }
    static double cumu_int_lumi(int e) { return std::accumulate(std::begin(int_lumi_), std::begin(int_lumi_) + e + 1, 0.); }
    static double total_int_lumi() { return cumu_int_lumi(e_max); }

    static int pick(unsigned long long event) {
      std::mt19937_64 g(event);
      std::discrete_distribution<> d(std::begin(int_lumi_), std::end(int_lumi_));
      return d(g);
    }

    template <typename T>
    static int pick(const edm::Event& event, const T& consumer) {
      const int which = jmt::getProcessModuleParameter<int>(event, consumer, "jmtAnalysisEras", "which");
      return which == -1 ? pick(event.id().event()) : which;
    }

  private:
    static const double int_lumi_[e_max];
  };
}

#endif
