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
  m_useSystFrac = false;
}

// The log-likelihood function.
// mu is the signal strength parameter.
// b is the vector of adjustable background values. This is not to be
// confused with the m values in the SigCalc object, which are
// estimates based on MC or sidebands.

double SigCalc::lnL(double mu, const std::vector<double>& b, const std::vector<double>& a) const {
  double btot = 0;
  for (int i = 0; i < numBck(); ++i) {
    if (useSystFrac())
      btot += b[i] * a[bitoaj(i)];
    else
      btot += b[i];
  }

  double logL = psi(n(), mu * s() + btot);

  for (int i = 0; i < numBck(); ++i) {
    if (useSystFrac()) {
      int j = bitoaj(i);
      double loga = log(a[j]);
      logL += psi(m(i), tau(i) * b[i] * a[j]) - loga - loga*loga/2/systFrac(j)/systFrac(j);
    }
    else
      logL += psi(m(i), tau(i) * b[i]);
  }

  return logL;
}

// Returns qmu = - 2 ln lambda(mu), where lambda = profile likelihood
// ratio.
double SigCalc::qmu(double mu, double& muHat, std::vector<double>& bHat, std::vector<double>& bHatHat) const {
  // Fix mu to input value and fit for (HatHat) nuisance parameters.

  std::vector<double> parVec; // mu is first, then the b, then the a
  std::vector<bool> freePar; // same order as parVec
  parVec.push_back(mu);
  freePar.push_back(false);

  for (int i = 0; i < numBck(); ++i) {
    parVec.push_back(m(i)/tau(i));   // m/tau as starting values
    freePar.push_back(true);
  }
  
  if (useSystFrac()) {
    for (int j = 0; j < numa(); ++j) {
      parVec.push_back(1);
      freePar.push_back(true);
    }
  }

  int status = fitPar(this, freePar, parVec);

  std::vector<double> aHatHat, aHat;

  bHatHat.clear();
  for (int i = 0; i < numBck(); ++i)
    bHatHat.push_back(parVec[i+1]);
  aHatHat.clear();
  for (int j = 0; j < numa(); ++j)
    aHatHat.push_back(parVec[numBck()+1+j]);

  if (status != 0 || debugLevel >= 2) {
    printf("\n");
    printf("qmu, fitting nuisance parameters only for mu=%.4f: status=%i\n", mu, status);
    printf("  bHatHat: ");
    for (int i = 0; i < numBck(); ++i)
      printf("%e ", bHatHat[i]);
    printf("\n  aHatHat: ");
    for (int j = 0; j < numa(); ++j)
      printf("%e ", aHatHat[j]);
    printf("\n\n");
  }

  // Fit all parameters.

  parVec.clear();
  freePar.clear();
  parVec.push_back(0.5);
  freePar.push_back(true);

  for (int i = 0; i < numBck(); ++i) {
    parVec.push_back(m(i)/tau(i));
    freePar.push_back(true);
  }

  if (useSystFrac()) {
    for (int j = 0; j < numa(); ++j) {
      parVec.push_back(1);
      freePar.push_back(true);
    }
  }

  status = fitPar(this, freePar, parVec);
  
  muHat = parVec[0];
  bHat.clear();
  for (int i = 0; i < numBck(); ++i)
    bHat.push_back(parVec[i+1]);
  aHat.clear();
  for (int j = 0; j < numa(); ++j)
    aHatHat.push_back(parVec[numBck()+1+j]);

  if (status != 0 || debugLevel >= 2) {
    printf("\n");
    printf("qmu, fitting all parameters: status=%i, muHat = %.4f\n", status, muHat);
    printf("  bHat: ");
    for (int i = 0; i < numBck(); ++i)
      printf("%e ", bHat[i]);
    printf("\n  aHat: ");
    for (int j = 0; j < numa(); ++j)
      printf("%e ", aHat[j]);
    printf("\n\n");
  }

  const double lnLmu_xHatHat = lnL(mu, bHatHat, aHatHat);
  const double lnLmuHat_xHat = lnL(muHat, bHat, aHat);
  const double q = 2.*(lnLmuHat_xHat - lnLmu_xHatHat);
  if (q < 0 || debugLevel >= 2)
    printf("lnLmuHat_xHat: %e  lnLmu_xHatHat: %e  q: %e\n", lnLmuHat_xHat, lnLmu_xHatHat, q);
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
  if (systFrac > 0) {
    sc->systFrac(std::vector<double>({systFrac}));
    sc->bitoaj(std::vector<int>(m.size(), 0));
  }
  double qmu = sc->qmu(mu);
  double Z = sqrt(qmu);

  delete sc;
  return Z;
}
