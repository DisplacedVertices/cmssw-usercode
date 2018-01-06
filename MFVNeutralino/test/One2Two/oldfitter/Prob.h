#ifndef JMTucker_MFVNeutralino_One2Two_Prob_h
#define JMTucker_MFVNeutralino_One2Two_Prob_h

class TRandom;

namespace jmt {
  struct interval {
    interval() {}
    interval(double l, double u) : lower(l), upper(u) {}
    interval(double v, double l, double u) : value(v), lower(l), upper(u) {}
    bool success;
    double value;
    double lower;
    double upper;
    double error() const { return (upper - lower)/2; }
    double in(double v) const { return v >= lower && v <= upper; }
    void set(double l, double u) { lower = l; upper = u; }
    void set(double v, double l, double u) { value = v; lower = l; upper = u; }
  };

  interval garwood_poisson(const double n, const double alpha=(1-0.6827)/2, const double beta=(1-0.6827)/2);

  interval clopper_pearson_binom(const double n_on, const double n_tot,
                                 const double alpha=1-0.6827, const bool equal_tailed=true);

  interval clopper_pearson_poisson_means_ratio(const double x, const double y,
                                               const double alpha=1-0.6827, const bool equal_tailed=true);

  double lognormal(TRandom* r, double mu, double sig);
}

#endif
