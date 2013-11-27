// Modified version of SigCalc from Glen Cowan, RHUL Physics

// Uses Minuit to fit the MLEs muHat, bHat and conditional MLEs bHatHat
// used in profile likelihood ratio.

#include <cmath>
#include <string>
#include "TMinuit.h"
#include "fitPar.h"

const SigCalc* scGlobal; // needs to be global to communicate with fcn (below)

int fitPar(const SigCalc* sc, const std::vector<bool>& freePar, std::vector<double>& pars) {
  // Set up start values, step sizes, etc. for fit.

  scGlobal = sc; // communicate to fcn via global
  const int npar = pars.size();

  double par[npar];
  std::string parName[npar];
  double stepSize[npar];
  double minVal[npar];
  double maxVal[npar];

  parName[0] = "mu";

  for (int i = 0; i < npar; i++) {
    par[i] = pars[i];
    stepSize[i] = par[i] != 0 ? std::abs(par[i])*0.1 : 0.1;
    minVal[i] = 0.;
    maxVal[i] = 1000000.;

    if (i > 0) {
      char buf[128];
      snprintf(buf, 128, "b%i", i-1);
      parName[i] = buf;
    }
  }

  // Create the TMinuit object and define parameters.
  TMinuit* minuit = new TMinuit(npar);
  int ierr = 0;
  minuit->SetPrintLevel(SigCalc::debugLevel >= 2 ? 1 : -1);
  if (SigCalc::debugLevel < 1)
    minuit->mnexcm("SET NOWarnings", 0, 0, ierr);

  minuit->SetFCN(fcn);
  for (int i = 0; i < npar; i++) {
    minuit->DefineParameter(i, parName[i].c_str(), par[i], stepSize[i], minVal[i], maxVal[i]);
    if (!freePar[i])
      minuit->FixParameter(i);
  }

  // Do the fit and extract results.
  int status = minuit->Command("MIGRAD");
  if (status != 0) {
    status = minuit->Command("SIMPLEX");
    status = minuit->Command("MIGRAD");
  }

  pars.clear();
  const int nFreePar = minuit->GetNumFreePars();
  double fitpar[nFreePar], err[nFreePar];
  for (int i = 0; i < npar; ++i) {
    minuit->GetParameter(i, fitpar[i], err[i]);
    pars.push_back(fitpar[i]);
  }

  delete minuit;
  return status; // 0 = normal completion, 4 = MIGRAD not converged
}

// fcn must be non-member function, uses global SigCalc object scGlobal.
void fcn(int& npar, double* deriv, double& f, double par[], int flag) {
  const int numBck = scGlobal->numBck();
  double mu = par[0];
  std::vector<double> b;
  for (int i = 0; i < numBck; ++i)
    b.push_back(par[i+1]);

  f = -2.*scGlobal->lnL(mu, b);

  //  if ( SigCalc::debugLevel >= 3 ) {
  //    for (int i=0; i<npar; i++) {
  //      cout << "i, par = " << i << "  " << par[i] << endl;
  //    }
  //    cout << "f = " << f << endl;
  //    cout << endl;
  //  }
}

// psi returns log of Poisson probability nu^n exp(-nu) (the n! term
// is dropped). For nu -> 0 and n = 0 the probability is 1, i.e., psi
// returns zero. The function avoids evaluating log(nu) for nu <=
// epsilon.
double psi(double n, double nu) {
  static const double epsilon = 1e-6;
  static const double logOfSmallValue = -100; // JMTBAD should correspond to epsilon...
  double val;
  if (n <= epsilon && nu <= epsilon)
    return 0;
  else if (n > epsilon && nu <= epsilon)
    return -n * logOfSmallValue;  // JMTBAD two negatives here? 
  else
    return n*log(nu) - nu;
}
