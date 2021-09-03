#ifndef DVCode_Tools_StatCalculator_h
#define DVCode_Tools_StatCalculator_h

#include <vector>

namespace jmt {
  template <typename T>
  struct IStatCalculator {
    // ith value of these are the corresponding stat with the ith value
    // of the n-length input removed, value n is the stat with no input
    // values removed
    const size_t n;
    const bool rmscorr;
    std::vector<T> min;
    std::vector<T> max;
    std::vector<T> med;
    std::vector<T> sum;
    std::vector<T> avg;
    std::vector<T> rms;
    std::vector<T> mad;

    void calc(std::vector<T> v, T& min_, T& max_, T& med_, T& sum_, T& avg_, T& rms_, T& mad_) {
      const size_t m = v.size();
      if (m == 0) return;

      std::sort(v.begin(), v.end());
      min_ = v.front();
      max_ = v.back();

      if (m % 2 == 0)
        med_ = (v[m/2] + v[m/2-1])/2;
      else
        med_ = v[m/2];

      sum_ = avg_ = rms_ = 0;
      std::vector<T> v2(m);
      for (size_t i = 0; i < m; ++i) {
        sum_ += v[i];
        v2[i] = fabs(v[i] - med_);
      }
      avg_ = sum_/m;

      std::sort(v2.begin(), v2.end());
      if (m % 2 == 0)
        mad_ = (v2[m/2] + v2[m/2-1])/2;
      else
        mad_ = v2[m/2];

      for (auto a : v)
        rms_ += pow(a - avg_, 2);
      rms_ = sqrt(rms_/(rmscorr ? m-1 : m)); //m-1
    }

  IStatCalculator(const std::vector<T>& v, bool rmscorr_=false) : n(v.size()), rmscorr(rmscorr_) {
      min.assign(n+1, 0);
      max.assign(n+1, 0);
      med.assign(n+1, 0);
      sum.assign(n+1, 0);
      avg.assign(n+1, 0);
      rms.assign(n+1, 0);
      mad.assign(n+1, 0);
      if (n == 0)
        return;

      calc(v, min[n], max[n], med[n], sum[n], avg[n], rms[n], mad[n]);

      for (size_t i = 0; i < n; ++i) {
        std::vector<T> v2(v);
        v2.erase(v2.begin()+i);
        calc(v2, min[i], max[i], med[i], sum[i], avg[i], rms[i], mad[i]);
      }
    }
  };

  typedef IStatCalculator<float> FloatStatCalculator;
  typedef IStatCalculator<double> StatCalculator;
}

#endif
