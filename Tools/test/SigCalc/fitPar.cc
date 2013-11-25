// Modified version of SigCalc from Glen Cowan, RHUL Physics

// Uses TMinuit to fit the MLEs muHat, bHat and conditional MLEs bHatHat
// used in profile likelihood ratio.
// Inputs:     
// mu    signal strength parameter (0 = background only, 1 = nominal).
// n     number of events seen in data, e.g. generate from Poisson(mu*s+b)
// s     expected number of signal events
// m     vector of numbers of events seen in subsidiary measurements.
// tau   defined by m_i ~ Poisson(tau_i*b_i), e.g., ratio of MC lumonisity
//       to that of data sample.

#include <cmath>
#include <string>
#include "TMinuit.h"
#include "fitPar.h"

SigCalc* scGlobal;   // needs to be global to communicate with fcn (below)
bool debug;

int fitPar(SigCalc* sc, std::vector<bool> freePar, std::vector<double>& parVec) {
  
// set up start values, step sizes, etc. for fit

  scGlobal = sc;                  // communicate to fcn via global
  int npar = parVec.size();

  const int maxpar = 100;
  double par[maxpar];
  std::string parName[maxpar];
  double stepSize[maxpar];
  double minVal[maxpar];
  double maxVal[maxpar];

  for (int i=0; i<npar; i++) {
    par[i] = parVec[i];
  }

  for (int i=0; i<npar; i++) {    // some of these overridden below
    stepSize[i] = 0.1;
    minVal[i] = 0.;
    maxVal[i] = 1000000.;
  }  

  parName[0] = "mu";
  for (int i=1; i<npar; i++) {
    char buf[128];
    snprintf(buf, 128, "b%i", i);
    parName[i] = buf;
  }

  for (int i=0; i<npar; i++) {
    if ( par[i] != 0 ) {
      stepSize[i] = std::abs( par[i] ) * 0.1;
    }
    else {
      stepSize[i] = 0.1;
    }
  }

// Create the TMinuit object and define parameters

  TMinuit* minuit = new TMinuit(npar);

  minuit->SetPrintLevel(-1);
  int ierr = 0;
  minuit->mnexcm("SET NOWarnings",0,0,ierr);

  minuit->SetFCN(fcn);
  for (int i=0; i<npar; i++) {
    minuit->DefineParameter(i, parName[i].c_str(), 
    par[i], stepSize[i], minVal[i], maxVal[i]);
  }

  for (int i=0; i<npar; i++) {
    if ( !freePar[i] ) {
      minuit->FixParameter(i);
    }
  }

// do the fit and extract results

  int status = minuit->Command("MIGRAD");
  if ( status != 0 ) {
    debug = true;
    status = minuit->Command("SIMPLEX");
    status = minuit->Command("MIGRAD");
    debug = false;
  }

  parVec.clear();
  int nFreePar = minuit->GetNumFreePars();
  double fitpar[nFreePar], err[nFreePar];
  for (int i=0; i<npar; i++) {
    minuit->GetParameter(i, fitpar[i], err[i]);
    parVec.push_back(fitpar[i]);
  }

  delete minuit;
  return status;     // 0 = normal completion, 4 = MIGRAD not converged

}

// fcn must be non-member function, uses global SigCalc object scGlobal

void fcn(int& npar, double* deriv, double& f, double par[], int flag) {

  int numBck = scGlobal->numBck();
  double mu = par[0];
  std::vector<double> bVec;
  for (int i=0; i<numBck; i++) {
    bVec.push_back(par[i+1]);
  }
  f = -2.*scGlobal->lnL(mu, bVec);

  //  if ( debug ) {
  //    for (int i=0; i<npar; i++) {
  //      cout << "i, par = " << i << "  " << par[i] << endl;
  //    }
  //    cout << "f = " << f << endl;
  //    cout << endl;
  //  }

}

// The function psi returns log of Poisson probability nu^n exp(-nu)
// (the n! term is dropped).  For nu -> 0 and n = 0 the probability is 1,
// i.e., psi returns zero.  The function avoids evaluating log(nu) for 
// nu <= epsilon.

double psi(double n, double nu) {
  const double epsilon = 1.e-6;
  const double logOfSmallValue = -100.;
  double val;
  if ( n <= epsilon && nu <= epsilon ) {
    val = 0.;
  }
  else if ( n > epsilon && nu <= epsilon ) {
    val = - n * logOfSmallValue; 
  }
  else {
    val = n*log(nu) - nu;
  }
  return val;
}
