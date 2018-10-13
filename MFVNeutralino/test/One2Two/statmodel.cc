/*
 * This program is used to compute the fractional statistical uncertainty in the yield in each bin of the dVVC template.
 * To run interactively: compile with the Makefile (make statmodel.exe); execute (./statmodel.exe).
 * To run all configurations of n1v: submit to condor (condor_submit statmodel.jdl).
 *
 * Here is an example of the end of the printout (in the .log files if run by condor):
 *   2v bins means:
 *   bin                     bin mean                   scaled true                          diff                           rms
 *     1       0.7337 +-       0.0002        0.7349 +-       0.0009       -0.0012 +-       0.0009        0.0183 +-       0.0001
 *     2       0.2063 +-       0.0001        0.2053 +-       0.0005        0.0010 +-       0.0005        0.0133 +-       0.0001
 *     3       0.0600 +-       0.0001        0.0598 +-       0.0002        0.0002 +-       0.0003        0.0127 +-       0.0001
 *
 * The statistical uncertainty is taken as the root-mean-square of yields in an ensemble of simulated pseudo-data sets.
 * To compute the fractional statistical uncertainty, divide rms/true for each bin.
 * For example, in this case the fractional statistical uncertainties are: bin1 0.0183/0.7349 = 0.0249; bin2 0.0133/0.2053 = 0.0648; bin3 0.0127/0.0598 = 0.2124.
 *
 * The fractional statistical uncertainties depend primarily on the number of entries in the parent dBV distribution (n1v).
 * So by default, the set of configurations run when submitted to condor are different in n1v but use the same values of phi_c, phi_a, eff_fn, etc.
 * There is one job for each n1v[samples_index][year_index][ntracks]:
 *  - samples_index: 0 = n1v in MC scaled to integrated luminosity, 1 = effective n1v in MC, 2 = n1v in 10% data, 3 = n1v in 100% data
 *  - year_index: 0 = 2017, 1 = 2018, 2 = 2017+2018
 *  - ntracks: 3, 4, 5
 *
 * Run treesprint.py to get the values of n1v in MC scaled to integrated luminosity.
 * Calculate the effective n1v in MC: "n1v" = (n1v/en1v)^2.
 * For example, if n1v = 826.11 +/- 61.39, then "n1v" = (826.11 / 61.39)**2 = 181.
 *
 *
 * How statmodel.cc works:
 *  - Model the dBV distribution with a function:
 *      f(rho) = p0 + p1 * expl(-p2 * rho) + p3 * expl(-p4 * rho^0.5) + rho_tail_norm * p5 * expl(-p6 * rho_tail_slope * rho^0.15)
 *      {p0, p1, p2, p3, p4, p5, p6} depends on ntracks
 *  - Generate the true dVV distribution using the dBV function (and the deltaphi function and efficiency curve).
 *  - Throw ntoys.  For each toy:
 *     - Randomly sample i1v from Poisson(n1v)
 *     - Make a histogram of dBV by randomly sampling from the dBV function i1v times
 *     - Construct dVVC
 *  - Calculate the RMS of the dVVC yields in each bin.
 *
 * These configurables can be set on the command line (e.g. env sm_ntracks=5 ./statmodel.exe):
 *   inst, seed, ntoys, out_fn, samples_index, year_index, ntracks, n1v, n2v, true_fn, true_from_file,
 *   ntrue_1v, ntrue_2v, oversample, rho_tail_norm, rho_tail_slope, phi_c, phi_e, phi_a, eff_fn, eff_path
 *
 * These should be modified in the code:
 *   nbins_1v, bins_1v, nbins_2v, bins_2v, func_rho, rho_min, rho_max, default_n1v, default_n2v
 */

#include <cassert>
#include <experimental/filesystem>
#include <memory>
template <typename T> using uptr = std::unique_ptr<T>;
#include "TCanvas.h"
#include "TError.h"
#include "TF1.h"
#include "TFile.h"
#include "TGraph.h"
#include "TH1.h"
#include "TLatex.h"
#include "TLine.h"
#include "TMath.h"
#include "TRandom3.h"
#include "TRatioPlot.h"
#include "TStyle.h"
#include "TVector2.h"
#include "ConfigFromEnv.h"
#include "Prob.h"
#include "ROOTTools.h"
#include "Utility.h"

// Helper classes for vertices and pairs of vertices (simplified version of those used in the fitter)

struct Vertex {
  double r, p;
  double x, y;

  Vertex() : r(0), p(0), x(0), y(0) {}
  Vertex(double rho_, double phi_)
    : r(rho_),
      p(phi_),
      x(rho_ * cos(phi_)),
      y(rho_ * sin(phi_))
    {}

  double rho() const { return r; }
  double phi() const { return p; }

  double rho(const Vertex& o) const { return jmt::mag(x - o.x, y - o.y);          }
  double phi(const Vertex& o) const { return TVector2::Phi_mpi_pi(phi() - o.phi()); }
 };

struct VertexPair {
  Vertex first;
  Vertex second;

  VertexPair() {}
  VertexPair(const Vertex& f, const Vertex& s) : first(f), second(s) {}
    
  double rho() const { return first.rho(second); }
  double phi() const { return first.phi(second); }
};

// Globals: parameters for the throwing fcns and the fcns themselves, and the binning for 1v/2v hists

int ntracks;
long double rho_tail_norm;
long double rho_tail_slope;
double phi_c;
double phi_e;
double phi_a;

const int nbins_1v = 995;
const double bins_1v[nbins_1v+1] = {
  0.010, 0.012, 0.014, 0.016, 0.018, 0.020, 0.022, 0.024, 0.026, 0.028, 0.030, 0.032, 0.034, 0.036, 0.038,
  0.040, 0.042, 0.044, 0.046, 0.048, 0.050, 0.052, 0.054, 0.056, 0.058, 0.060, 0.062, 0.064, 0.066, 0.068,
  0.070, 0.072, 0.074, 0.076, 0.078, 0.080, 0.082, 0.084, 0.086, 0.088, 0.090, 0.092, 0.094, 0.096, 0.098,
  0.100, 0.102, 0.104, 0.106, 0.108, 0.110, 0.112, 0.114, 0.116, 0.118, 0.120, 0.122, 0.124, 0.126, 0.128,
  0.130, 0.132, 0.134, 0.136, 0.138, 0.140, 0.142, 0.144, 0.146, 0.148, 0.150, 0.152, 0.154, 0.156, 0.158,
  0.160, 0.162, 0.164, 0.166, 0.168, 0.170, 0.172, 0.174, 0.176, 0.178, 0.180, 0.182, 0.184, 0.186, 0.188,
  0.190, 0.192, 0.194, 0.196, 0.198, 0.200, 0.202, 0.204, 0.206, 0.208, 0.210, 0.212, 0.214, 0.216, 0.218,
  0.220, 0.222, 0.224, 0.226, 0.228, 0.230, 0.232, 0.234, 0.236, 0.238, 0.240, 0.242, 0.244, 0.246, 0.248,
  0.250, 0.252, 0.254, 0.256, 0.258, 0.260, 0.262, 0.264, 0.266, 0.268, 0.270, 0.272, 0.274, 0.276, 0.278,
  0.280, 0.282, 0.284, 0.286, 0.288, 0.290, 0.292, 0.294, 0.296, 0.298, 0.300, 0.302, 0.304, 0.306, 0.308,
  0.310, 0.312, 0.314, 0.316, 0.318, 0.320, 0.322, 0.324, 0.326, 0.328, 0.330, 0.332, 0.334, 0.336, 0.338,
  0.340, 0.342, 0.344, 0.346, 0.348, 0.350, 0.352, 0.354, 0.356, 0.358, 0.360, 0.362, 0.364, 0.366, 0.368,
  0.370, 0.372, 0.374, 0.376, 0.378, 0.380, 0.382, 0.384, 0.386, 0.388, 0.390, 0.392, 0.394, 0.396, 0.398,
  0.400, 0.402, 0.404, 0.406, 0.408, 0.410, 0.412, 0.414, 0.416, 0.418, 0.420, 0.422, 0.424, 0.426, 0.428,
  0.430, 0.432, 0.434, 0.436, 0.438, 0.440, 0.442, 0.444, 0.446, 0.448, 0.450, 0.452, 0.454, 0.456, 0.458,
  0.460, 0.462, 0.464, 0.466, 0.468, 0.470, 0.472, 0.474, 0.476, 0.478, 0.480, 0.482, 0.484, 0.486, 0.488,
  0.490, 0.492, 0.494, 0.496, 0.498, 0.500, 0.502, 0.504, 0.506, 0.508, 0.510, 0.512, 0.514, 0.516, 0.518,
  0.520, 0.522, 0.524, 0.526, 0.528, 0.530, 0.532, 0.534, 0.536, 0.538, 0.540, 0.542, 0.544, 0.546, 0.548,
  0.550, 0.552, 0.554, 0.556, 0.558, 0.560, 0.562, 0.564, 0.566, 0.568, 0.570, 0.572, 0.574, 0.576, 0.578,
  0.580, 0.582, 0.584, 0.586, 0.588, 0.590, 0.592, 0.594, 0.596, 0.598, 0.600, 0.602, 0.604, 0.606, 0.608,
  0.610, 0.612, 0.614, 0.616, 0.618, 0.620, 0.622, 0.624, 0.626, 0.628, 0.630, 0.632, 0.634, 0.636, 0.638,
  0.640, 0.642, 0.644, 0.646, 0.648, 0.650, 0.652, 0.654, 0.656, 0.658, 0.660, 0.662, 0.664, 0.666, 0.668,
  0.670, 0.672, 0.674, 0.676, 0.678, 0.680, 0.682, 0.684, 0.686, 0.688, 0.690, 0.692, 0.694, 0.696, 0.698,
  0.700, 0.702, 0.704, 0.706, 0.708, 0.710, 0.712, 0.714, 0.716, 0.718, 0.720, 0.722, 0.724, 0.726, 0.728,
  0.730, 0.732, 0.734, 0.736, 0.738, 0.740, 0.742, 0.744, 0.746, 0.748, 0.750, 0.752, 0.754, 0.756, 0.758,
  0.760, 0.762, 0.764, 0.766, 0.768, 0.770, 0.772, 0.774, 0.776, 0.778, 0.780, 0.782, 0.784, 0.786, 0.788,
  0.790, 0.792, 0.794, 0.796, 0.798, 0.800, 0.802, 0.804, 0.806, 0.808, 0.810, 0.812, 0.814, 0.816, 0.818,
  0.820, 0.822, 0.824, 0.826, 0.828, 0.830, 0.832, 0.834, 0.836, 0.838, 0.840, 0.842, 0.844, 0.846, 0.848,
  0.850, 0.852, 0.854, 0.856, 0.858, 0.860, 0.862, 0.864, 0.866, 0.868, 0.870, 0.872, 0.874, 0.876, 0.878,
  0.880, 0.882, 0.884, 0.886, 0.888, 0.890, 0.892, 0.894, 0.896, 0.898, 0.900, 0.902, 0.904, 0.906, 0.908,
  0.910, 0.912, 0.914, 0.916, 0.918, 0.920, 0.922, 0.924, 0.926, 0.928, 0.930, 0.932, 0.934, 0.936, 0.938,
  0.940, 0.942, 0.944, 0.946, 0.948, 0.950, 0.952, 0.954, 0.956, 0.958, 0.960, 0.962, 0.964, 0.966, 0.968,
  0.970, 0.972, 0.974, 0.976, 0.978, 0.980, 0.982, 0.984, 0.986, 0.988, 0.990, 0.992, 0.994, 0.996, 0.998,
  1.000, 1.002, 1.004, 1.006, 1.008, 1.010, 1.012, 1.014, 1.016, 1.018, 1.020, 1.022, 1.024, 1.026, 1.028,
  1.030, 1.032, 1.034, 1.036, 1.038, 1.040, 1.042, 1.044, 1.046, 1.048, 1.050, 1.052, 1.054, 1.056, 1.058,
  1.060, 1.062, 1.064, 1.066, 1.068, 1.070, 1.072, 1.074, 1.076, 1.078, 1.080, 1.082, 1.084, 1.086, 1.088,
  1.090, 1.092, 1.094, 1.096, 1.098, 1.100, 1.102, 1.104, 1.106, 1.108, 1.110, 1.112, 1.114, 1.116, 1.118,
  1.120, 1.122, 1.124, 1.126, 1.128, 1.130, 1.132, 1.134, 1.136, 1.138, 1.140, 1.142, 1.144, 1.146, 1.148,
  1.150, 1.152, 1.154, 1.156, 1.158, 1.160, 1.162, 1.164, 1.166, 1.168, 1.170, 1.172, 1.174, 1.176, 1.178,
  1.180, 1.182, 1.184, 1.186, 1.188, 1.190, 1.192, 1.194, 1.196, 1.198, 1.200, 1.202, 1.204, 1.206, 1.208,
  1.210, 1.212, 1.214, 1.216, 1.218, 1.220, 1.222, 1.224, 1.226, 1.228, 1.230, 1.232, 1.234, 1.236, 1.238,
  1.240, 1.242, 1.244, 1.246, 1.248, 1.250, 1.252, 1.254, 1.256, 1.258, 1.260, 1.262, 1.264, 1.266, 1.268,
  1.270, 1.272, 1.274, 1.276, 1.278, 1.280, 1.282, 1.284, 1.286, 1.288, 1.290, 1.292, 1.294, 1.296, 1.298,
  1.300, 1.302, 1.304, 1.306, 1.308, 1.310, 1.312, 1.314, 1.316, 1.318, 1.320, 1.322, 1.324, 1.326, 1.328,
  1.330, 1.332, 1.334, 1.336, 1.338, 1.340, 1.342, 1.344, 1.346, 1.348, 1.350, 1.352, 1.354, 1.356, 1.358,
  1.360, 1.362, 1.364, 1.366, 1.368, 1.370, 1.372, 1.374, 1.376, 1.378, 1.380, 1.382, 1.384, 1.386, 1.388,
  1.390, 1.392, 1.394, 1.396, 1.398, 1.400, 1.402, 1.404, 1.406, 1.408, 1.410, 1.412, 1.414, 1.416, 1.418,
  1.420, 1.422, 1.424, 1.426, 1.428, 1.430, 1.432, 1.434, 1.436, 1.438, 1.440, 1.442, 1.444, 1.446, 1.448,
  1.450, 1.452, 1.454, 1.456, 1.458, 1.460, 1.462, 1.464, 1.466, 1.468, 1.470, 1.472, 1.474, 1.476, 1.478,
  1.480, 1.482, 1.484, 1.486, 1.488, 1.490, 1.492, 1.494, 1.496, 1.498, 1.500, 1.502, 1.504, 1.506, 1.508,
  1.510, 1.512, 1.514, 1.516, 1.518, 1.520, 1.522, 1.524, 1.526, 1.528, 1.530, 1.532, 1.534, 1.536, 1.538,
  1.540, 1.542, 1.544, 1.546, 1.548, 1.550, 1.552, 1.554, 1.556, 1.558, 1.560, 1.562, 1.564, 1.566, 1.568,
  1.570, 1.572, 1.574, 1.576, 1.578, 1.580, 1.582, 1.584, 1.586, 1.588, 1.590, 1.592, 1.594, 1.596, 1.598,
  1.600, 1.602, 1.604, 1.606, 1.608, 1.610, 1.612, 1.614, 1.616, 1.618, 1.620, 1.622, 1.624, 1.626, 1.628,
  1.630, 1.632, 1.634, 1.636, 1.638, 1.640, 1.642, 1.644, 1.646, 1.648, 1.650, 1.652, 1.654, 1.656, 1.658,
  1.660, 1.662, 1.664, 1.666, 1.668, 1.670, 1.672, 1.674, 1.676, 1.678, 1.680, 1.682, 1.684, 1.686, 1.688,
  1.690, 1.692, 1.694, 1.696, 1.698, 1.700, 1.702, 1.704, 1.706, 1.708, 1.710, 1.712, 1.714, 1.716, 1.718,
  1.720, 1.722, 1.724, 1.726, 1.728, 1.730, 1.732, 1.734, 1.736, 1.738, 1.740, 1.742, 1.744, 1.746, 1.748,
  1.750, 1.752, 1.754, 1.756, 1.758, 1.760, 1.762, 1.764, 1.766, 1.768, 1.770, 1.772, 1.774, 1.776, 1.778,
  1.780, 1.782, 1.784, 1.786, 1.788, 1.790, 1.792, 1.794, 1.796, 1.798, 1.800, 1.802, 1.804, 1.806, 1.808,
  1.810, 1.812, 1.814, 1.816, 1.818, 1.820, 1.822, 1.824, 1.826, 1.828, 1.830, 1.832, 1.834, 1.836, 1.838,
  1.840, 1.842, 1.844, 1.846, 1.848, 1.850, 1.852, 1.854, 1.856, 1.858, 1.860, 1.862, 1.864, 1.866, 1.868,
  1.870, 1.872, 1.874, 1.876, 1.878, 1.880, 1.882, 1.884, 1.886, 1.888, 1.890, 1.892, 1.894, 1.896, 1.898,
  1.900, 1.902, 1.904, 1.906, 1.908, 1.910, 1.912, 1.914, 1.916, 1.918, 1.920, 1.922, 1.924, 1.926, 1.928,
  1.930, 1.932, 1.934, 1.936, 1.938, 1.940, 1.942, 1.944, 1.946, 1.948, 1.950, 1.952, 1.954, 1.956, 1.958,
  1.960, 1.962, 1.964, 1.966, 1.968, 1.970, 1.972, 1.974, 1.976, 1.978, 1.980, 1.982, 1.984, 1.986, 1.988,
  1.990, 1.992, 1.994, 1.996, 1.998, 2.000
};

//const int nbins_2v = 11;
//const double bins_2v[nbins_2v+1] = { 0., 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.2 };
const int nbins_2v = 3;
const double bins_2v[nbins_2v+1] = { 0., 0.04, 0.07, 0.11 };

//#define USE_H_DBV
TH1D* h_func_rho = 0;
TF1* f_func_rho = 0;
TF1* f_func_dphi = 0;
TH1F* h_eff = 0;

double func_rho(double* x, double*) {
  const long double rho(fabs(x[0]));
  long double f = 1e-6;
  const long double p[3][10] = {
    { 2.87190e-04L, 3.35391e-08L, 3.56126e+02L, 6.74967e+02L, 2.19970e+01L, 1.07814e+06L, 5.97512e+01L },
    { 6.72207e-10L, 8.71486e-03L, 2.50698e+00L, 1.30699e+03L, 2.63253e+01L, 2.84286e+04L, 3.09081e+01L },
    { 8.91883e-04L, 2.12659e-01L, 1.32012e+01L, 5.11276e+03L, 3.63974e+01L, 3.30855e+06L, 4.13659e+02L }
  };

  const size_t i = ntracks - 3;
  f = p[i][0] + p[i][1] * expl(-p[i][2] * rho) + p[i][3] * expl(-p[i][4] * powl(rho, 0.5L)) + rho_tail_norm * p[i][5] * expl(-p[i][6] * rho_tail_slope * powl(rho, 0.15L));

  return double(f);
}

double func_rho_norm(double* x, double* p) {
  return p[0] * func_rho(x,0);
}

double func_dphi(double* x, double*) {
  return pow(x[0] - phi_c, phi_e) + phi_a;
}

double throw_rho() {
  //return gRandom->Rndm();
#ifdef USE_H_DBV
  return h_func_rho->GetRandom();
#else
  return f_func_rho->GetRandom();
#endif
}

double throw_dphi() {
  double dphi = f_func_dphi->GetRandom();
  if (gRandom->Rndm() > 0.5) dphi *= -1;
  return dphi;
}

Vertex throw_1v(const double phi=-1e99) {
  if (phi < -1e98)
    return Vertex(throw_rho(), gRandom->Rndm()*2*M_PI - M_PI);
  else
    return Vertex(throw_rho(), phi);
}

double get_eff(double rho) {
  if (h_eff)
    return h_eff->GetBinContent(h_eff->FindBin(rho));
  return 1;
}

VertexPair throw_2v() {
  VertexPair p;
  while (1) {
    p.first = throw_1v();
    const double dphi = throw_dphi();
    p.second = throw_1v(TVector2::Phi_mpi_pi(p.first.phi() + dphi));
    const double eff = get_eff(p.rho());
    const double u = gRandom->Rndm();
    if (u < eff)
      break;
  }
  return p;
}

TH1D* book_1v(const char* name) { return new TH1D(name, "", nbins_1v, bins_1v); }
TH1D* book_2v(const char* name) { return new TH1D(name, "", nbins_2v, bins_2v); }

int main(int, char**) {
  // Defaults and command-line configurables.

  jmt::ConfigFromEnv env("sm", true);

                                       // 2017                                2018                     2017+2018
  const double default_n1v[4][3][6] = {{{ -1, -1, -1, 104166, 10097, 826 }, { -1, -1, -1, 1, 1, 1 }, { -1, -1, -1, 104166, 10097,  826 }},  //MC scaled to int. lumi.
                                       {{ -1, -1, -1,  22501,  2245, 181 }, { -1, -1, -1, 1, 1, 1 }, { -1, -1, -1,  22501,  2245,  181 }},  //MC effective
                                       {{ -1, -1, -1,      1,     1,   1 }, { -1, -1, -1, 1, 1, 1 }, { -1, -1, -1,      1,     1,    1 }},  //data 10%
                                       {{ -1, -1, -1,      1,     1,   1 }, { -1, -1, -1, 1, 1, 1 }, { -1, -1, -1,      1,     1,    1 }}}; //data 100%

  const double default_n2v[4][3][6] = {{{ -1, -1, -1,    773,     5,   1 }, { -1, -1, -1, 1, 1, 1 }, { -1, -1, -1,    773,     5,    1 }},
                                       {{ -1, -1, -1,    184,     8,   1 }, { -1, -1, -1, 1, 1, 1 }, { -1, -1, -1,    184,     8,    1 }},
                                       {{ -1, -1, -1,      1,     1,   1 }, { -1, -1, -1, 1, 1, 1 }, { -1, -1, -1,      1,     1,    1 }},
                                       {{ -1, -1, -1,      1,     1,   1 }, { -1, -1, -1, 1, 1, 1 }, { -1, -1, -1,      1,     1,    1 }}};

  const int inst = env.get_int("inst", 0);
  const int seed = env.get_int("seed", 12919135 + inst);
  const int ntoys = env.get_int("ntoys", 10000);
  const std::string out_fn = env.get_string("out_fn", "statmodel");
  const int samples_index = env.get_int("samples_index", 0);
  assert(samples_index >= 0 && samples_index <= 3);
  const int year_index = env.get_int("year_index", 0);
  assert(year_index >= 0 && year_index <= 2);
  ntracks = env.get_int("ntracks", 5);
  assert(ntracks >= 3 && ntracks <= 5);
  const double n1v = env.get_double("n1v", default_n1v[samples_index][year_index][ntracks]);
  const double n2v = env.get_double("n2v", default_n2v[samples_index][year_index][ntracks]);
  const std::string true_fn = env.get_string("true_fn", "");
  const bool true_from_file = true_fn != "";
  const long ntrue_1v = env.get_long("ntrue_1v", 10000000L);
  const long ntrue_2v = env.get_long("ntrue_2v", 1000000L);
  const double oversample = env.get_double("oversample", 20);
  const std::string rho_compare_fn = env.get_string("rho_compare_fn", "/uscms_data/d2/tucker/crab_dirs/HistosV20mp1/background_2017.root");
  rho_tail_norm = env.get_long_double("rho_tail_norm", 1L);
  rho_tail_slope = env.get_long_double("rho_tail_slope", 1L);
  phi_c = env.get_double("phi_c", 1.42);
  phi_e = env.get_double("phi_e", 2);
  phi_a = env.get_double("phi_a", 3.46);
  const std::string eff_fn = env.get_string("eff_fn", "vpeffs_2017_v20m.root");
  const std::string eff_path = env.get_string("eff_path", "maxtk3");

  /////////////////////////////////////////////

  // Set up ROOT and globals (mainly the fcns from which we throw)

  jmt::set_root_style();
  TH1::SetDefaultSumw2();
  TH1::AddDirectory(0);

  gRandom->SetSeed(seed);

  uptr<TFile> out_f(new TFile((out_fn + ".root").c_str(), "recreate"));

#ifdef USE_H_DBV
  uptr<TFile> fh(new TFile("h.root"));
  h_func_rho = (TH1D*)fh->Get("c1")->FindObject("h")->Clone();
  h_func_rho->SetDirectory(0);
  fh->Close();
  printf("entries in h: %f\n", h_func_rho->GetEntries());
#endif

  const double rho_min = 0.01;
  const double rho_max = 2.;
  f_func_rho = new TF1("func_rho", func_rho, rho_min, rho_max);
  f_func_rho->SetNpx(25000); // need lots of points when you want to sample a fcn with such a big y range

  f_func_dphi = new TF1("func_dphi", func_dphi, 0, M_PI);
  f_func_dphi->SetNpx(1000);

  if (eff_fn != "") {
    uptr<TFile> eff_f(new TFile(eff_fn.c_str()));
    h_eff = (TH1F*)eff_f->Get(eff_path.c_str())->Clone("h_eff");
    eff_f->Close();
  }

  uptr<TCanvas> c(new TCanvas("c", "", 1972, 1000));
  TVirtualPad* pd = 0;
  TString pdf_fn = (out_fn + ".pdf").c_str();
  c->Print(pdf_fn + "[");
  auto p = [&] () { c->cd(); c->Print(pdf_fn); };
  //auto lp   = [&] () { c->SetLogy(1); c->Print(pdf_fn); c->SetLogy(0); };
  //auto lxp  = [&] () { c->SetLogx(1); c->Print(pdf_fn); c->SetLogx(0); };
  //auto lxyp = [&] () { c->SetLogx(1); c->SetLogy(1); c->Print(pdf_fn); c->SetLogx(0); c->SetLogy(0); };

  /////////////////////////////////////////////

  // 1st page of output: show the rho fcn itself lin/log

  const double func_rho_max   = f_func_rho->GetMaximum();
  const double func_rho_max_x = f_func_rho->GetMaximumX();
  printf("max of 1v fcn %f at %f\n", func_rho_max, func_rho_max_x);
  c->Divide(2,1);
  c->cd(1)->SetLogy();
  f_func_rho->SetRange(0., 0.2);
  f_func_rho->DrawCopy();
  c->cd(2)->SetLogy();
  f_func_rho->SetRange(rho_min, rho_max);
  f_func_rho->Draw();
  p();
  c->Clear();

  // 2nd page: compare rho to MC background distributions.

  if (std::experimental::filesystem::exists(rho_compare_fn)) {
    TF1* f_func_rho_norm = new TF1("func_rho_norm", func_rho_norm, rho_min, rho_max, 1);
    f_func_rho_norm->SetNpx(25000);
    f_func_rho_norm->SetParameter(1,1);
    uptr<TFile> fin(TFile::Open(rho_compare_fn.c_str()));
    TH1* h_rho_compare = 0;
    if      (ntracks == 5) h_rho_compare = (TH1*)fin->Get(    "mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist");
    else if (ntracks == 3) h_rho_compare = (TH1*)fin->Get("Ntk3mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist");
    else if (ntracks == 4) h_rho_compare = (TH1*)fin->Get("Ntk4mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist");
    h_rho_compare->SetStats(0);
    h_rho_compare->Fit(f_func_rho_norm, "WL Q R");
    h_rho_compare->GetXaxis()->SetRangeUser(0,0.5);
    //  h_rho_compare->GetYaxis()->SetRangeUser(3e-2,500);
    c->SetLogy();
    uptr<TRatioPlot> rho_compare(new TRatioPlot(h_rho_compare));
    rho_compare->SetGraphDrawOpt("P");
    rho_compare->Draw();
    c->Update();
    rho_compare->GetLowerRefYaxis()->SetRangeUser(-7,7);
    p();
  }
  else {
    TText tt(0.1, 0.75, TString::Format("no file %s", rho_compare_fn.c_str()));
    tt.Draw();
    p();
  }
  c->Clear();

  // Generate the true 1v & 2v distributions from func_rho and
  // func_dphi. Takes a while, so if true_fn is set on cmd line, will
  // take these + the rng state from that file.

  uptr<TH1D> h_true_1v_rho(book_1v("h_true_1v_rho"));
  uptr<TH1D> h_true_1v_phi(new TH1D("h_true_1v_phi", "", 20, -M_PI, M_PI));

  uptr<TH1D> h_true_2v_rho(book_1v("h_true_2v_rho"));
  uptr<TH1D> h_true_2v_phi(new TH1D("h_true_2v_phi", "", 20, -M_PI, M_PI));

  uptr<TH1D> h_true_2v_dvv(book_2v("h_true_2v_dvv"));
  uptr<TH1D> h_true_2v_dphi(new TH1D("h_true_2v_dphi", "", 10, 0, M_PI));

  if (true_from_file) {
    gRandom->ReadRandom(true_fn.c_str());

    printf("reading 1 and 2v true hists from file\n");
    uptr<TFile> true_f(new TFile(true_fn.c_str()));
    if (!true_f->IsOpen()) {
      fprintf(stderr, "can't open %s\n", true_fn.c_str());
      return 1;
    }

    for (auto* h : {h_true_1v_rho.get(), h_true_1v_phi.get(), h_true_2v_rho.get(), h_true_2v_phi.get(), h_true_2v_dvv.get(), h_true_2v_dphi.get()})
      h->Add((TH1D*)true_f->Get(h->GetName()));
  }
  else {
    printf("1v true: ");
    for (long i = 0; i < ntrue_1v; ++i) {
      if (i % (ntrue_1v/10) == 0) {
        printf("%li", i/(ntrue_1v/10));
        fflush(stdout);
      }
      Vertex v = throw_1v();
      h_true_1v_rho->Fill(v.rho());
      h_true_1v_phi->Fill(v.phi());
    }
    printf(" %li\n", ntrue_1v);

    printf("2v true: ");
    for (long i = 0; i < ntrue_2v; ++i) {
      if (i % (ntrue_2v/10) == 0) {
        printf("%li", i/(ntrue_2v/10));
        fflush(stdout);
      }
      VertexPair vp = throw_2v();
      h_true_2v_rho->Fill(vp.first .rho());
      h_true_2v_rho->Fill(vp.second.rho());
      h_true_2v_phi->Fill(vp.first .phi());
      h_true_2v_phi->Fill(vp.second.phi());
      h_true_2v_dvv->Fill(vp.rho());
      h_true_2v_dphi->Fill(fabs(vp.phi()));
    }
    printf(" %li\n", ntrue_2v);

    gRandom->Write();
  }

  assert(h_true_1v_rho->GetBinContent(h_true_1v_rho->GetNbinsX()+1) < 1e-12);
  //jmt::deoverflow(h_true_1v_rho.get());
  jmt::deoverflow(h_true_2v_dvv.get());

  // 3rd-8th pages of output: the true_1v histogram + comparison to
  // fcn (for debugging),

  uptr<TH1D> h_true_1v_rho_unzoom    ((TH1D*)h_true_1v_rho->Clone("h_true_1v_rho_unzoom"));
  uptr<TH1D> h_true_1v_rho_norm      ((TH1D*)h_true_1v_rho->Clone("h_true_1v_rho_norm"));
  uptr<TH1D> h_true_1v_rho_norm_one  ((TH1D*)h_true_1v_rho->Clone("h_true_1v_rho_norm_one"));
  uptr<TH1D> h_true_1v_rho_norm_width((TH1D*)h_true_1v_rho->Clone("h_true_1v_rho_norm_width"));
  h_true_1v_rho_norm      ->Scale(n1v/h_true_1v_rho->Integral());
  h_true_1v_rho_norm_one  ->Scale( 1./h_true_1v_rho->Integral());
  h_true_1v_rho_norm_width->Scale(n1v/h_true_1v_rho->Integral(), "width");

  printf("1v err/bin check:\n");
  for (auto* h : {h_true_1v_rho.get(), h_true_1v_rho_norm.get(), h_true_1v_rho_norm_one.get(), h_true_1v_rho_norm_width.get()})
    printf("%40s: %10.4f/%10.4f = %0.3f\n", h->GetName(), h->GetBinError(nbins_1v), h->GetBinContent(nbins_1v), h->GetBinError(nbins_1v)/h->GetBinContent(nbins_1v));

  uptr<TH1D> h_true_2v_rho_unzoom    ((TH1D*)h_true_2v_rho->Clone("h_true_2v_rho_unzoom"));
  uptr<TH1D> h_true_2v_rho_norm      ((TH1D*)h_true_2v_rho->Clone("h_true_2v_rho_norm"));
  uptr<TH1D> h_true_2v_rho_norm_width((TH1D*)h_true_2v_rho->Clone("h_true_2v_rho_norm_width"));
  h_true_2v_rho_norm      ->Scale(n2v/h_true_2v_rho->Integral());
  h_true_2v_rho_norm_width->Scale(n2v/h_true_2v_rho->Integral(), "width");

  c->Divide(2,2);
  c->cd(1)->SetLogy();
  h_true_1v_rho_unzoom->SetTitle("true 1v, raw counts, unzoomed;#rho (cm);counts");
  h_true_1v_rho_unzoom->Draw("histe");
  c->cd(2)->SetLogy();
  h_true_1v_rho->GetXaxis()->SetRangeUser(0,0.4);
  h_true_1v_rho->SetTitle("true 1v, raw counts;#rho (cm);counts");
  h_true_1v_rho->Draw("histe");
  c->cd(3)->SetLogy();
  h_true_1v_rho_norm->SetTitle(TString::Format("true 1v, scaled to %.1f events;#rho (cm);events", n1v));
  h_true_1v_rho_norm->GetXaxis()->SetRangeUser(0,0.4);
  h_true_1v_rho_norm->Draw("histe");
  c->cd(4)->SetLogy();
  h_true_1v_rho_norm_width->SetTitle(TString::Format("true 1v, scaled to %.1f events, bin width;#rho (cm);events/cm", n1v));
  h_true_1v_rho_norm_width->GetXaxis()->SetRangeUser(0,0.4);
  h_true_1v_rho_norm_width->Draw("histe");
  p();
  c->Clear();

  uptr<TH1D> h_true_1v_rho_integ     (book_1v("h_true_1v_rho_integ"));
  uptr<TH1D> h_true_1v_rho_integ_diff(book_1v("h_true_1v_rho_integ_diff"));

  h_true_1v_rho_integ->SetTitle("integral of fcn;#rho (cm);fraction");
  h_true_1v_rho_integ_diff->SetTitle("abs. diff. in integral and thrown hist;#rho (cm)");
  
  for (int i = 0; i < nbins_1v; ++i)
    h_true_1v_rho_integ->SetBinContent(i+1, f_func_rho->Integral(bins_1v[i], bins_1v[i+1]));
  h_true_1v_rho_integ->Scale(1./h_true_1v_rho_integ->Integral());

  for (int ibin = 1; ibin <= nbins_1v; ++ibin) {
    const double integ = h_true_1v_rho_integ   ->GetBinContent(ibin);
    const double hist  = h_true_1v_rho_norm_one->GetBinContent(ibin);
    const double histe = h_true_1v_rho_norm_one->GetBinError  (ibin);
    h_true_1v_rho_integ_diff->SetBinContent(ibin, hist - integ);
    h_true_1v_rho_integ_diff->SetBinError  (ibin, histe);
  }

  c->Divide(2,1);
  pd = c->cd(1); pd->SetLogx(); pd->SetLogy();
  h_true_1v_rho_integ->Draw("hist");
  c->cd(2)->SetLogx();
  h_true_1v_rho_integ_diff->SetStats(0);
  h_true_1v_rho_integ_diff->Draw("e");
  p();
  c->Clear();

  c->Divide(2,2);
  c->cd(1)->SetLogy();
  h_true_2v_rho_unzoom->SetTitle("true 2v, raw counts, unzoomed;#rho (cm);counts");
  h_true_2v_rho_unzoom->Draw("histe");
  c->cd(2)->SetLogy();
  h_true_2v_rho->GetXaxis()->SetRangeUser(0,0.4);
  h_true_2v_rho->SetTitle("true 2v, raw counts;#rho (cm);counts");
  h_true_2v_rho->Draw("histe");
  c->cd(3)->SetLogy();
  h_true_2v_rho_norm->SetTitle(TString::Format("true 2v, scaled to %.1f events;#rho (cm);events", n2v));
  h_true_2v_rho_norm->GetXaxis()->SetRangeUser(0,0.4);
  h_true_2v_rho_norm->Draw("histe");
  c->cd(4)->SetLogy();
  h_true_2v_rho_norm_width->SetTitle(TString::Format("true 2v, scaled to %.1f events, bin width;#rho (cm);events/cm", n2v));
  h_true_2v_rho_norm_width->GetXaxis()->SetRangeUser(0,0.4);
  h_true_2v_rho_norm_width->Draw("histe");
  p();
  c->Clear();

  c->Divide(2,1);
  c->cd(1);
  h_true_1v_phi->SetMinimum(0);
  h_true_1v_phi->SetTitle("true 1v;#phi;counts");
  h_true_1v_phi->Draw("histe");
  c->cd(1)->Update();
  jmt::move_stat_box(h_true_1v_phi.get(), 0., -0.15);
  c->cd(2);
  h_true_2v_phi->SetMinimum(0);
  h_true_2v_phi->SetTitle("true 2v;#phi;counts");
  h_true_2v_phi->Draw("histe");
  c->cd(2)->Update();
  jmt::move_stat_box(h_true_2v_phi.get(), 0., -0.15);
  p();
  c->Clear();

  uptr<TH1D> h_true_2v_dvv_norm((TH1D*)h_true_2v_dvv->Clone("h_true_2v_dvv_norm"));
  h_true_2v_dvv_norm->Scale(n2v/h_true_2v_dvv->Integral());
  uptr<TH1D> h_true_2v_dphi_norm((TH1D*)h_true_2v_dphi->Clone("h_true_2v_dphi_norm"));
  h_true_2v_dphi_norm->Scale(n2v/h_true_2v_dphi->Integral());
  
  printf("2v err/bin check:\n");
  for (auto* h : {h_true_2v_dvv.get(), h_true_2v_dvv_norm.get()})
    printf("%40s: %10.4f/%10.4f = %0.3f\n", h->GetName(), h->GetBinError(nbins_2v), h->GetBinContent(nbins_2v), h->GetBinError(nbins_2v)/h->GetBinContent(nbins_2v));

  c->Divide(2,1);
  c->cd(1)->SetLogy();
  h_true_2v_dvv->SetTitle("true, raw counts;d_{VV} (cm);counts");
  h_true_2v_dvv->Draw("histe");
  c->cd(2)->SetLogy();
  h_true_2v_dvv_norm->SetTitle(TString::Format("true, scaled to %.1f events;d_{VV} (cm);events", n2v));
  h_true_2v_dvv_norm->Draw("histe");
  p();
  c->Clear();

  c->Divide(2,1);
  c->cd(1);
  h_true_2v_dphi->SetMinimum(0);
  h_true_2v_dphi->SetTitle("true, raw counts;#Delta #phi_{VV};counts");
  h_true_2v_dphi->Draw("histe");
  c->cd(1)->Update();
  jmt::move_stat_box(h_true_2v_dphi.get(), -0.5, 0);
  c->cd(2);
  h_true_2v_dphi_norm->SetMinimum(0);
  h_true_2v_dphi_norm->SetTitle(TString::Format("true, scaled to %.1f events;#Delta #phi_{VV};events", n2v));
  h_true_2v_dphi_norm->Draw("histe");
  c->cd(2)->Update();
  jmt::move_stat_box(h_true_2v_dphi_norm.get(), -0.5, 0);
  p();
  c->Clear();

  /////////////////////////////////////////////

  // Output pg 9-XX: distribution in toys of total n1v, n1v in each
  // dbv bin, and n2v in each dvv bin, each compared to truth from
  // fcn.

  uptr<TH1D> h_n1v(new TH1D("h_n1v", "", 20, n1v - 5*sqrt(n1v), n1v + 5*sqrt(n1v)));
  std::vector<uptr<TH1D>> h_1v_rho_bins;
  std::vector<uptr<TH1D>> h_2v_dvvc_bins;

  for (int ibin = 1; ibin <= nbins_1v; ++ibin) {
    const double tru = h_true_1v_rho_norm->GetBinContent(ibin);
    const double pb = 2.87e-7;
    jmt::interval iv = jmt::garwood_poisson(tru, pb, pb);
    if (iv.lower < 1) iv.lower = 0;
    h_1v_rho_bins.emplace_back(new TH1D(TString::Format("h_1v_rho_bins_%i", ibin), TString::Format("#rho bin %i", ibin), 25, iv.lower, iv.upper));
  }

  for (int ibin = 1; ibin <= nbins_2v; ++ibin) {
    const double tru = h_true_2v_dvv_norm->GetBinContent(ibin);
    const double pb = 1.35e-3;
    jmt::interval iv = jmt::garwood_poisson(tru, pb, pb);
    if (iv.lower < 1) iv.lower = 0;
    h_2v_dvvc_bins.emplace_back(new TH1D(TString::Format("h_2v_dvvc_bins_%i", ibin), TString::Format("d_{VV}^{C} bin %i", ibin), 200, iv.lower, iv.upper));
  }

  // Throw the toys and fill the above hists.
  // First throw the one vertex sample, then construct dvvc from it.
  // The toy is saved in the h_1v/2v*bins vectors.

  printf("toys: ");
  for (int itoy = 0; itoy < ntoys; ++itoy) {
    // make the toy dataset
    uptr<TH1D> h_1v_rho(book_1v("h_1v_rho"));
    const int i1v = gRandom->Poisson(n1v);
    h_n1v->Fill(i1v);

    for (int i = 0; i < i1v; ++i) {
      Vertex v = throw_1v();
      h_1v_rho->Fill(v.rho());
    }

    for (int ibin = 1; ibin <= nbins_1v; ++ibin)
      h_1v_rho_bins[ibin-1]->Fill(h_1v_rho->GetBinContent(ibin));

    // The construction
    uptr<TH1D> h_2v_dvvc(book_2v("h_2v_dvvc"));

    for (int i = 0, ie = int(i1v * oversample); i < ie; ++i) {
      const double rho0 = h_1v_rho->GetRandom();
      const double rho1 = h_1v_rho->GetRandom();
      const double dphi = throw_dphi();
      const double dvvc = sqrt(rho0*rho0 + rho1*rho1 - 2*rho0*rho1*cos(dphi));
      const double w = get_eff(dvvc);
      h_2v_dvvc->Fill(dvvc, w);
    }

    jmt::deoverflow(h_2v_dvvc.get());
    h_2v_dvvc->Scale(n2v/h_2v_dvvc->Integral());
    
    for (int ibin = 1; ibin <= nbins_2v; ++ibin)
      h_2v_dvvc_bins[ibin-1]->Fill(h_2v_dvvc->GetBinContent(ibin));

    if (ntoys > 10 && itoy % (ntoys/10) == 0) {
      printf("%i", itoy/(ntoys/10));
      fflush(stdout);
    }
  }
  printf(" %i\n", ntoys);

  h_n1v->Draw("hist");
  p();
  c->Clear();

  TLatex tl;
  tl.SetTextFont(42);

  /////////////////////////////////////////////

  // Output pg XX: display and compare the mean and rms to the true
  // distributions. The right plot on output pg-1, "2v bin-by-bin
  // rms/true" gives the fractional uncertainties in each bin due to
  // the statistics of the 1v distribution, and the last page shows
  // the closure of the construction procedure.

  uptr<TH1D> h_1v_rho_bins_means      (book_1v("h_1v_rho_bins_means"));
  uptr<TH1D> h_1v_rho_bins_rmses      (book_1v("h_1v_rho_bins_rmses"));
  uptr<TH1D> h_1v_rho_bins_rmses_norm (book_1v("h_1v_rho_bins_rmses_norm"));
  uptr<TH1D> h_1v_rho_bins_diffs      (book_1v("h_1v_rho_bins_diffs"));
  uptr<TH1D> h_1v_rho_bins_diffs_norm (book_1v("h_1v_rho_bins_diffs_norm"));

  uptr<TH1D> h_2v_dvvc_bins_means     (book_2v("h_2v_dvvc_bins_means"));
  uptr<TH1D> h_2v_dvvc_bins_rmses     (book_2v("h_2v_dvvc_bins_rmses"));
  uptr<TH1D> h_2v_dvvc_bins_rmses_norm(book_2v("h_2v_dvvc_bins_rmses_norm"));
  uptr<TH1D> h_2v_dvvc_bins_diffs     (book_2v("h_2v_dvvc_bins_diffs"));
  uptr<TH1D> h_2v_dvvc_bins_diffs_norm(book_2v("h_2v_dvvc_bins_diffs_norm"));

  printf("1v bins means:\n");
  printf("%3s %28s  %28s  %28s\n", "bin", "bin mean", "scaled true", "diff");
  for (int i_base = 0; i_base < nbins_1v; i_base += 4) {
    c->Divide(2,2);
    for (int i = i_base; i < std::min(i_base + 4, nbins_1v); ++i) {
      c->cd(i%4+1);
      h_1v_rho_bins[i]->Draw("hist");
      const double b  = h_1v_rho_bins[i]->GetMean();
      const double be = h_1v_rho_bins[i]->GetMeanError();
      const double r  = h_1v_rho_bins[i]->GetRMS();
      const double re = h_1v_rho_bins[i]->GetRMSError();
      const double t  = h_true_1v_rho_norm->GetBinContent(i+1);
      const double te = h_true_1v_rho_norm->GetBinError  (i+1);
      const double d  = b - t;
      const double de = sqrt(be*be + te*te);
      printf("%3i %12.4f +- %12.4f  %12.4f +- %12.4f  %12.4f +- %12.4f\n", i+1, b, be, t, te, d, de);
      if (d > 2*de)
        tl.SetTextColor(kRed);
      else if (d > de)
        tl.SetTextColor(kOrange+2);
      else
        tl.SetTextColor(kBlack);
      tl.DrawLatexNDC(0.6, 0.4, TString::Format("#splitline{true: %.3f #pm %.3f}{diff: %.3f #pm %.3f}", t, te, d, de));

      h_1v_rho_bins_means->SetBinContent(i+1, b);
      h_1v_rho_bins_means->SetBinError  (i+1, be);

      h_1v_rho_bins_rmses->SetBinContent(i+1, r);
      h_1v_rho_bins_rmses->SetBinError  (i+1, re);

      h_1v_rho_bins_rmses_norm->SetBinContent(i+1, r/t);
      h_1v_rho_bins_rmses_norm->SetBinError  (i+1, sqrt(re*re/r/r + te*te/t/t)); // JMTBAD

      h_1v_rho_bins_diffs->SetBinContent(i+1, d);
      h_1v_rho_bins_diffs->SetBinError  (i+1, de);

      h_1v_rho_bins_diffs_norm->SetBinContent(i+1, d/t);
      h_1v_rho_bins_diffs_norm->SetBinError  (i+1, sqrt(be*be/b/b + te*te/t/t)); // JMTBAD
    }
    p();
    c->Clear();
  }

  printf("2v bins means:\n");
  printf("%3s %28s  %28s  %28s  %28s\n", "bin", "bin mean", "scaled true", "diff", "rms");
  for (int i_base = 0; i_base < nbins_2v; i_base += 4) {
    c->Divide(2,2);
    for (int i = i_base; i < std::min(i_base + 4, nbins_2v); ++i) {
      c->cd(i%4+1);
      h_2v_dvvc_bins[i]->Draw("hist");
      const double b  = h_2v_dvvc_bins[i]->GetMean();
      const double be = h_2v_dvvc_bins[i]->GetMeanError();
      const double r  = h_2v_dvvc_bins[i]->GetRMS();
      const double re = h_2v_dvvc_bins[i]->GetRMSError();
      const double t  = h_true_2v_dvv_norm->GetBinContent(i+1);
      const double te = h_true_2v_dvv_norm->GetBinError  (i+1);
      const double d  = b - t;
      const double de = sqrt(be*be + te*te);
      printf("%3i %12.4f +- %12.4f  %12.4f +- %12.4f  %12.4f +- %12.4f  %12.4f +- %12.4f\n", i+1, b, be, t, te, b-t, sqrt(be*be + te*te), r, re);
      if (d > 2*de)
        tl.SetTextColor(kRed);
      else if (d > de)
        tl.SetTextColor(kOrange+2);
      else
        tl.SetTextColor(kBlack);
      tl.DrawLatexNDC(0.6, 0.4, TString::Format("#splitline{true: %.3f #pm %.3f}{diff: %.3f #pm %.3f}", t, te, d, de));

      h_2v_dvvc_bins_means->SetBinContent(i+1, b);
      h_2v_dvvc_bins_means->SetBinError  (i+1, be);

      h_2v_dvvc_bins_rmses->SetBinContent(i+1, r);
      h_2v_dvvc_bins_rmses->SetBinError  (i+1, re);

      h_2v_dvvc_bins_rmses_norm->SetBinContent(i+1, r/t);
      h_2v_dvvc_bins_rmses_norm->SetBinError  (i+1, sqrt(re*re/r/r + te*te/t/t)); // JMTBAD

      h_2v_dvvc_bins_diffs->SetBinContent(i+1, d);
      h_2v_dvvc_bins_diffs->SetBinError  (i+1, de);

      h_2v_dvvc_bins_diffs_norm->SetBinContent(i+1, d/t);
      h_2v_dvvc_bins_diffs_norm->SetBinError  (i+1, sqrt(be*be/b/b + te*te/t/t)); // JMTBAD
    }
    p();
    c->Clear();
  }

  TLine l1;
  l1.SetLineStyle(2);

  c->Divide(2,1);
  pd = c->cd(1); pd->SetLogx(); pd->SetLogy();
  h_1v_rho_bins_means->SetStats(0);
  h_1v_rho_bins_means->SetTitle("1v bin-by-bin mean;#rho (cm)");
  h_1v_rho_bins_means->Draw("histe");
  c->cd(2)->SetLogx();
  h_1v_rho_bins_diffs->SetStats(0);
  h_1v_rho_bins_diffs->SetTitle("1v bin-by-bin mean/true - 1;#rho (cm)");
  h_1v_rho_bins_diffs->Draw("e");
  l1.DrawLine(0,0,2.0,0);
  p();
  c->Clear();

  c->Divide(2,1);
  c->cd(1)->SetLogy();
  h_2v_dvvc_bins_means->SetStats(0);
  h_2v_dvvc_bins_means->SetTitle("2v bin-by-bin mean;d_{VV}^{C} (cm)");
  h_2v_dvvc_bins_means->Draw("histe");
  c->cd(2);
  //h_2v_dvvc_bins_rmses->GetYaxis()->SetRangeUser(0,0.6);
  h_2v_dvvc_bins_rmses->SetStats(0);
  h_2v_dvvc_bins_rmses->SetTitle("2v bin-by-bin rms;d_{VV}^{C} (cm)");
  h_2v_dvvc_bins_rmses->Draw("histe");
  p();
  c->Clear();

  c->Divide(2,1);
  c->cd(1);
  h_2v_dvvc_bins_rmses->SetStats(0);
  h_2v_dvvc_bins_rmses->SetTitle("2v bin-by-bin rms;d_{VV}^{C} (cm)");
  h_2v_dvvc_bins_rmses->Draw("histe");
  c->cd(2);
  h_2v_dvvc_bins_rmses_norm->SetStats(0);
  h_2v_dvvc_bins_rmses_norm->SetTitle("2v bin-by-bin rms/true;d_{VV}^{C} (cm)");
  h_2v_dvvc_bins_rmses_norm->Draw("histe");
  p();
  c->Clear();

  c->Divide(2,1);
  c->cd(1);
  h_2v_dvvc_bins_diffs->SetStats(0);
  h_2v_dvvc_bins_diffs->SetTitle("2v bin-by-bin mean - true;d_{VV} (cm)");
  h_2v_dvvc_bins_diffs->Draw("e");
  l1.DrawLine(0,0,0.2,0);
  c->cd(2);
  h_2v_dvvc_bins_diffs_norm->SetStats(0);
  h_2v_dvvc_bins_diffs_norm->SetTitle("2v bin-by-bin mean/true - 1;d_{VV} (cm)");
  h_2v_dvvc_bins_diffs_norm->Draw("e");
  l1.DrawLine(0,0,0.2,0);
  p();
  c->Clear();

  c->Print(pdf_fn + "]");

  out_f->cd();
  for (auto* h : {h_true_1v_rho.get(), h_true_1v_phi.get(), h_true_2v_rho.get(), h_true_2v_phi.get(), h_true_2v_dvv.get(), h_true_2v_dphi.get()})
    h->Write();

  // making these unique_ptrs causes segfault at end?
  delete h_func_rho;
  delete f_func_rho;
  delete f_func_dphi;
  delete h_eff;
}
