// Modified version of SigCalc from Glen Cowan, RHUL Physics

#include <cmath>
#include <stdio.h>
#include "SigCalc.h"
#include "fitPar.h"

int SigCalc::debugLevel = 0;

SigCalc::SigCalc(double n, double s, const std::vector<double>& m, const std::vector<double>& tau) {
  m_n = n;
  m_s = s;
  m_m = m;
  m_tau = tau;
  m_numBck = m.size();
}

// The log-likelihood function.
// mu is the signal strength parameter.
// b is the vector of adjustable background values. This is not to be
// confused with the m values in the SigCalc object, which are
// estimates based on MC or sidebands.

double SigCalc::lnL(double mu, const std::vector<double>& b) const {
  const int nbkg = int(b.size());

  double btot = 0;
  for (int i = 0; i < nbkg; ++i)
    btot += b[i];

  double logL = psi(n(), mu * s() + btot);

  for (int i = 0; i < nbkg; ++i)
    logL += psi(m(i), tau(i) * b[i]);

  return logL;
}

// Returns qmu = - 2 ln lambda(mu), where lambda = profile likelihood
// ratio.
double SigCalc::qmu(double mu, double& muHat, std::vector<double>& bHat, std::vector<double>& bHatHat) const {
  const int nbkg = numBck();

  // Fix mu to input value and fit for (HatHat) nuisance parameters.

  std::vector<double> parVec; // mu is first, then the b, then the a
  std::vector<bool> freePar; // same order as parVec
  parVec.push_back(mu);
  freePar.push_back(false);

  for (int i = 0; i < nbkg; ++i) {
    parVec.push_back(m(i)/tau(i));   // m/tau as starting values
    freePar.push_back(true);
  }

  int status = fitPar(this, freePar, parVec);

  bHatHat.clear();
  for (int i = 0; i < nbkg; ++i)
    bHatHat.push_back(parVec[i+1]);

  if (status != 0 || debugLevel >= 2) {
    printf("qmu, fitting nuisance parameters only for mu=%.4f: status=%i\n", mu, status);
    printf("  bHatHat: ");
    for (int i = 1; i < nbkg; ++i)
      printf("%e ", bHatHat[i-1]);
    printf("\n");
  }

  // Fit all parameters.

  parVec.clear();
  freePar.clear();
  parVec.push_back(0.5);
  freePar.push_back(true);

  for (int i = 0; i < nbkg; ++i) {
    parVec.push_back(m(i)/tau(i));
    freePar.push_back(true);
  }

  status = fitPar(this, freePar, parVec);
  
  muHat = parVec[0];
  bHat.clear();
  for (int i=0; i < nbkg; ++i)
    bHat.push_back(parVec[i+1]);

  if (status != 0 || debugLevel >= 2) {
    printf("qmu, fitting all parameters: status=%i, muHat = %.4f\n", status, muHat);
    printf("  bHat: ");
    for (int i = 1; i < nbkg; ++i)
      printf("%e ", bHat[i-1]);
    printf("\n");
  }

  const double lnLmu_bHatHat = lnL(mu, bHatHat);
  const double lnLmuHat_bHat = lnL(muHat, bHat);
  const double q = 2.*(lnLmuHat_bHat - lnLmu_bHatHat);
  if (q < 0 || debugLevel >= 2)
    printf("lnLmuHat_bHat: %e  lnLmu_bHatHat: %e  q: %e\n", lnLmuHat_bHat, lnLmu_bHatHat, q);
  return q;
}

// Returns significance Z with which hypothesized value of mu is rejected;
// Z = Phi^-1(1 - p), p = p-value of mu, Phi^-1 = quantile of standard
// Gaussian.
// 
// Inputs:     
// mu    signal strength parameter (0 = background only, 1 = nominal).
// n     number of events seen in data, e.g. generate from Poisson(mu*s+b)
// s     expected number of signal events
// m     std::vector of numbers of events seen in subsidiary measurements.
// tau   defined by m_i ~ Poisson(tau_i*b_i), e.g., ratio of MC lumonisity
//        to that of data sample.
// systFrac
//       if positive, include a systematic uncertainty modelled as a Gaussian
//       multiplicative factor in the likelihood. This results in an extra
//       nuisance parameter a ~ N(1, systFrac) that scales the b values.

double getSignificance(double mu, double n, double s, const std::vector<double>& m, const std::vector<double>& tau, double systFrac) {
  SigCalc* sc = new SigCalc (n, s, m, tau);
  sc->setSystFrac(systFrac);
  double qmu = sc->qmu(mu);
  double Z = sqrt(qmu);

  delete sc;
  return Z;
}
