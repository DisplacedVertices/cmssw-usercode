// Modified version of SigCalc from Glen Cowan, RHUL Physics

#ifndef SigCalc_fitPar_h
#define SigCalc_fitPar_h

#include <vector>
#include "SigCalc.h"

void fcn(int& n, double* d, double& f, double par[], int flag);
int fitPar(SigCalc* sc, std::vector<bool> freePar, std::vector<double>& parVec);
double psi(double n, double nu);

#endif
