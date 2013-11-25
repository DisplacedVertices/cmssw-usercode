// File:  fitPar.h
// Glen Cowan
// RHUL Physics

#ifndef FITPAR_H
#define FITPAR_H

// TMinuit needs non-member fcn, data global to communicate with fcn
void fcn(int& n, double* d, double& f, double par[], int flag);
int fitPar (SigCalc* sc, vector<bool> freePar,
             vector<double>& parVec);
double psi(double n, double nu);

#endif
