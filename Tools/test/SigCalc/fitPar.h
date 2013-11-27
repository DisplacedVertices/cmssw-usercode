// Modified version of SigCalc from Glen Cowan, RHUL Physics

#ifndef SigCalc_fitPar_h
#define SigCalc_fitPar_h

#include <vector>
#include "SigCalc.h"

int fitPar(const SigCalc* sc, const std::vector<bool>& freePar, std::vector<double>& parVec);
void fcn(int& n, double* d, double& f, double par[], int flag);
double psi(double n, double nu);

#endif
