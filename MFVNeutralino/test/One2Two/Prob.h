#ifndef JMTucker_MFVNeutralino_One2Two_Prob_h
#define JMTucker_MFVNeutralino_One2Two_Prob_h

namespace jmt {
  struct interval {
    bool success;
    double value;
    double lower;
    double upper;
    double error() const { return (upper - lower)/2; }
  };

  interval clopper_pearson_binom(const double n_on, const double n_tot,
                                 const double alpha=1-0.6827, const bool equal_tailed=true);

  interval clopper_pearson_poisson_means_ratio(const double x, const double y,
                                               const double alpha=1-0.6827, const bool equal_tailed=true);

  class TRandom;
  double lognormal(TRandom* r, double mu, double sig);
}

#endif
