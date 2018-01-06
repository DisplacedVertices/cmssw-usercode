// g++ -O2 -Werror -Wall -std=c++0x hogg.cc -o hogg.exe && ./hogg.exe 1.1 1 0 1

// A la Hogg (arXiv:0807.4820)

#include <cstdio>
#include <vector>
#include <cassert>
#include <cmath>

#include "hogg_data.h"

double likfcn(const std::vector<double>& binning, const double alpha) {
  const int nbins = int(binning.size()-1);
  std::vector<int> N(nbins, 0.);

  for (int i = 0; i < Ndd; ++i) {
    const double d = dd[i];
    for (int ibin = 0; ibin < nbins; ++ibin) {
      if (d >= binning[ibin] && d < binning[ibin+1]) {
        ++N[ibin];
        break;
      }
    }
  }

  double L = 0.;
  for (int ibin = 0; ibin < nbins; ++ibin) {
    //printf("%i ", N[ibin]);
    double Delta = binning[ibin+1] - binning[ibin];
    L += N[ibin] * log((N[ibin] + alpha - 1) / Delta / (Ndd + nbins*alpha - 1));
  }
  //printf("\n");

  return L;
}

int main(int argc, char** argv) {
  printf("hello : %f\n", likfcn(std::vector<double>({0.04, 0.0425, 0.045, 0.05, 0.055, 0.06, 0.07, 0.085, 0.1, 0.185, 0.385, 2.5}), 1.1));
  printf("hello : %f\n", likfcn(std::vector<double>({0.04, 0.0425, 0.045, 0.05, 0.055, 0.06, 0.07, 0.085, 0.1, 0.2, 0.4, 2.5}), 1.1));
  printf("hello : %f\n", likfcn(std::vector<double>({0.04, 0.0425, 0.045, 0.05, 0.055, 0.06, 0.07, 0.085, 0.1, 0.2, 0.4, 2.5}), 0.1));

  double alpha;
  int maxdivs, absstepmin, absstepmax;
  assert(argc == 5);
  sscanf(argv[1], "%lf", &alpha);
  sscanf(argv[2], "%i", &maxdivs);
  sscanf(argv[3], "%i", &absstepmin);
  sscanf(argv[4], "%i", &absstepmax);
  printf("i'm testing alpha %f and maxdivs %i in absrange [%i %i)\n", alpha, maxdivs, absstepmin, absstepmax);
  assert(alpha > 0 && maxdivs >= 1 && maxdivs <= 6 && absstepmin <= absstepmax && absstepmin >= 0 && absstepmax >= 1);

  const double lo0 = 0.1;
  const double hi0 = 2.5;
  const double step = 0.005;
#define STARTBINS 0.04, 0.045, 0.05, 0.055, 0.06, 0.07, 0.085, lo0
  const int nsteps = (hi0 - lo0)/step;
  const int laststep = nsteps; //120;
  
  double maxL = 0;
  std::vector<double> binning_atmax;
  double alpha_atmax;

  auto test = [&](const std::vector<double>& binning, const double alpha) { 
    double L = likfcn(binning, alpha);
    if (L > maxL) {
      maxL = L;
      binning_atmax = binning;
      alpha_atmax = alpha;
    }
  };

  // garbage ho!

  {
  //for (int ialpha = 0; ialpha < 12; ++ialpha) {
  //const double alpha = 0.8 + ialpha * 0.05;
    printf("alpha %f\n", alpha);

    for (int i1 = 1; i1 < laststep; ++i1) {
      //printf("i1: %i\n", i1);
      double b1 = lo0 + step * i1;
      if (maxdivs == 1)
        test(std::vector<double>({STARTBINS, b1, hi0}), alpha);
      else {
        for (int i2 = i1+1; i2 < laststep; ++i2) {
          double b2 = lo0 + step * i2;
          if (maxdivs == 2)
            test(std::vector<double>({STARTBINS, b1, b2, hi0}), alpha);
          else {
            for (int i3 = i2+1; i3 < laststep; ++i3) {
              double b3 = lo0 + step * i3;
              if (maxdivs == 3)
                test(std::vector<double>({STARTBINS, b1, b2, b3, hi0}), alpha);
              else {
                for (int i4 = i3+1; i4 < laststep; ++i4) {
                  double b4 = lo0 + step * i4;
                  if (maxdivs == 4)
                    test(std::vector<double>({STARTBINS, b1, b2, b3, b4, hi0}), alpha);
                  else {
                    for (int i5 = i4+1; i5 < laststep; ++i5) {
                      double b5 = lo0 + step * i5;
                      if (maxdivs == 5)
                        test(std::vector<double>({STARTBINS, b1, b2, b3, b4, b5, hi0}), alpha);
                      else {
                        for (int i6 = i5+1; i6 < laststep; ++i6) {
                          double b6 = lo0 + step * i6;
                          if (maxdivs == 6)
                            test(std::vector<double>({STARTBINS, b1, b2, b3, b4, b5, b6, hi0}), alpha);
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }

  printf("max L %f\n", maxL);
  for (double b : binning_atmax)
    printf("%f ", b);
  printf("\nalpha: %f\n", alpha_atmax);
}
