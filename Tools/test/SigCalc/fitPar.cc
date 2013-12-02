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
      bool isa = i - sc->numBck() > 0;
      snprintf(buf, 128, "%s%i", (isa ? "a" : "b"), i-1 - isa*sc->numBck());
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
  for (int i = 0; i < npar; ++i) {
    double fitpar, err;
    minuit->GetParameter(i, fitpar, err);
    pars.push_back(fitpar);
  }

  delete minuit;
  return status; // 0 = normal completion, 4 = MIGRAD not converged
}

// fcn must be non-member function, uses global SigCalc object scGlobal.
void fcn(int& npar, double* deriv, double& f, double par[], int flag) {
  double mu = par[0];
  std::vector<double> b, a;
  for (int i = 0; i < scGlobal->numBck(); ++i)
    b.push_back(par[i+1]);
  if (scGlobal->systFrac() > 0)
    for (int j = 0; j < scGlobal->numa(); ++j)
      a.push_back(par[scGlobal->numBck()+1+j]);

  f = -2.*scGlobal->lnL(mu, b, a);

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
  static const double logeps = log(epsilon);
  if (n <= epsilon && nu <= epsilon)
    return 0;
  else if (n > epsilon && nu <= epsilon)
    return n * logeps;
  else
    return n*log(nu) - nu;
}
