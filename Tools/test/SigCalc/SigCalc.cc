// File:  SigCalc.cc
// Glen Cowan
// RHUL Physics

// Implementation of SigCalc class

#include <iostream>
#include <string>
#include <vector>
#include <cmath>
#include "SigCalc.h"
#include "fitPar.h"

SigCalc::SigCalc(double n, double s, vector<double> mVec,  
                 vector<double> tauVec, int option){
  m_n = n;
  m_s = s;
  m_m = mVec;
  m_tau = tauVec;
  m_numBck = mVec.size();
  m_option = option;
}

double SigCalc::lnL(double mu, vector<double> bVec){

// The log-likelihood function.
// mu = global strength parameter
// here bVec is the vector of adjustable background values (not
// to be confused with the m values in the SigCalc object,
// which are estimates based on MC or sidebands.

  double btot = 0;
  for (int i=0; i<bVec.size(); i++){
    btot += bVec[i];
  }  
  double logL = psi(this->n(), mu*this->s() + btot);
  for (int i=0; i<this->numBck(); i++){
    logL += psi( this->m(i), this->tau(i)*bVec[i] );
  }
  return logL;

}

double SigCalc::qmu(double mu){

// Returns qmu = - 2 ln lambda(mu), where lambda = profile likelihood ratio.
// For this version the only argument is mu.  If you
// need access to muHat, bHat, bHatHat, use the version of qmu below.

  double muHat;
  vector<double> bHat;
  vector<double> bHatHat;
  double q = this->qmu(mu, muHat, bHat, bHatHat);
  return q;

}

double SigCalc::qmu(double mu, double& muHat, vector<double>& bHat,
                     vector<double>& bHatHat){

// This version of qmu passes back muHat, bHat, bHatHat.

  int numBck = this->numBck();

// Fix mu to input value and fit b (gives bHatHat)

  vector<double> parVec;
  vector<bool> freePar;
  parVec.push_back(mu);
  freePar.push_back(false);
  for (int i=0; i<numBck; i++){
    parVec.push_back(this->m(i)/this->tau(i));   // m/tau as starting values
    freePar.push_back(true);
  }
  int status = fitPar(this, freePar, parVec);

  bHatHat.clear();
  for (int i=0; i<numBck; i++){
    bHatHat.push_back(parVec[i+1]);
  }
  double lnLmubHatHat = this->lnL(mu, bHatHat);

// Fit mu and b (gives muHat and bHat)

  double muStart = 0.5;
  parVec.clear();
  freePar.clear();
  parVec.push_back(muStart);
  freePar.push_back(true);
   for (int i=0; i<numBck; i++){
   parVec.push_back(this->m(i)/this->tau(i));   // m/tau as starting values
    freePar.push_back(true);
  }
  status = fitPar(this, freePar, parVec);
  
  // if ( status != 0 ) {
  //   cout << "status, muHat = " << status << "  " << parVec[0] << endl;
  //   for (int i=1; i<numBck; i++){
  //     cout << parVec[i] << "  " << this->n(i) << "  " << this->m(i) << endl;
  //   }
  //   cout << endl;
  // }

  muHat = parVec[0];
  bHat.clear();
  for (int p=0; p<numBck; p++){
    bHat.push_back(parVec[p+1]);
  }
  double lnLmuHatbHat = this->lnL(muHat, bHat);

  double qVal = 2.*(lnLmuHatbHat - lnLmubHatHat);
  return qVal;

}
