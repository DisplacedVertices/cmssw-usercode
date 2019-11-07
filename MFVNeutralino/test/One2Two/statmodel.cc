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
 * The statistical uncertainty is taken as the root-mean-square of yields in an ensemble of simulated pseudodata sets.
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
 * When the jobs are completed, calculate the fractional statistical uncertainties and put the resulting values in statmodel.py.
 *
 *
 * How statmodel.cc works:
 *  - Model the dBV distribution with a function depending on ntracks
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
 * These can be modified in the code:
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
#include "JMTucker/Tools/interface/ConfigFromEnv.h"
#include "JMTucker/Tools/interface/Prob.h"
#include "JMTucker/Tools/interface/ROOTTools.h"
#include "JMTucker/Tools/interface/Utilities.h"

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

  double rho(const Vertex& o) const { return mag(x - o.x, y - o.y);          }
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

int sample_is_mc = 1;
int year_index = 0;
int ntracks = 3;
int ntracks_index = ntracks - 3;
double phi_c = 1.3;
double phi_e = 2;
double phi_a = 6;

const int nbins_1v = 995;
double bins_1v[nbins_1v+1] = {0};

const int nbins_2v = 3;
double bins_2v[nbins_2v+1] = {0};

//#define USE_H_DBV
TH1D* h_func_rho = 0;
TF1* f_func_rho = 0;
TF1* f_func_dphi = 0;
TH1F* h_eff = 0;

const int fr_max_kn = 7;
const double fr_kn[3][fr_max_kn] = {
  { 0.01, 0.02, 0.03, 0.06, 0.1, 0.2, 2 },
  { 0.01, 0.02, 0.05, 0.1, 2,     -1,-1 },
  { 0.01, 0.06, 2,          -1,-1,-1,-1 },
};

#ifdef FITTING_DBV
const int fr_ic = FR_IC; // e.g.   i=6; rm statmodel.exe ; make SMFLAGS="-DFITTING_DBV -DFR_IC=${i}" statmodel.exe && env sm_year_index=0 sm_rho_compare_only=1 sm_samples_index=2 sm_ntracks=3 sm_rho_compare_xmax=0.5 ./statmodel.exe
#endif
double fr_c[2][3][3][fr_max_kn] = { // is_mc, year, ntracks indices
  { // data (5tk are from 10%) are same for 2017/8--fit to 2017p8 but 2017 and 2018 look very similar in shape
    { // 2017
      { 9.80903, 9.66801, 8.36952, 5.86700, 3.2111, 0.05319, -10.3479 }, // 3track
      { 8.45312, 8.23969, 4.68509, 0.79881, -22.0859,           -1,-1 }, // 4track
      { 4.64386, 0.049497, -100,                          -1,-1,-1,-1 }, // 5track
    },
    { // 2018
      { 9.80903, 9.66801, 8.36952, 5.86700, 3.2111, 0.05319, -10.3479 },
      { 8.45312, 8.23969, 4.68509, 0.79881, -22.0859,           -1,-1 },
      { 4.64386, 0.049497, -100,                          -1,-1,-1,-1 },
    },
    { // 2017p8
      { 9.80903, 9.66801, 8.36952, 5.86700, 3.2111, 0.05319, -10.3479 },
      { 8.45312, 8.23969, 4.68509, 0.79881, -22.0859,           -1,-1 },
      { 4.64386, 0.049497, -100,                          -1,-1,-1,-1 },
    },
  },
  { // mc
    { // 2017
      { 8.27872, 8.13094, 6.9383, 4.87983, 2.33309, -0.733174, -8.93311 },
      { 6.4729, 6.27879, 3.31899, -0.18999, -26.6506,             -1,-1 },
      { 4.58488, -0.352759, -57.9401,                       -1,-1,-1,-1 },
    },
    { // 2018
      { 7.76261, 7.96822, 7.01993, 4.46392, 2.13192, -2.76241, -7.21428 },
      { 5.96357, 6.35436, 3.4712, -2.60817, -9.14066,             -1,-1 },
      { 4.39865, 1.26948, -223.883,                         -1,-1,-1,-1 },
    },
    { // 2017p8
      { 8.74394, 8.74316, 7.67281, 5.37591, 2.93877, -0.750633, -7.55426 },
      { 6.93565, 7.00247, 4.09944, -0.399182, -15.6391,            -1,-1 },
      { 5.15881, 1.33783, -114.868,                          -1,-1,-1,-1 },
    },
  },
};

double func_rho(double* _x, double* p) {
  const double x = fabs(_x[0]);

  int k = 1;
  for (; k < fr_max_kn; ++k)
    if (fr_kn[ntracks_index][k] < 0 || (fr_kn[ntracks_index][k-1] <= x && x < fr_kn[ntracks_index][k]))
      break;

#ifdef FITTING_DBV
  fr_c[sample_is_mc][year_index][ntracks_index][fr_ic] = p[0];
  if (fr_ic == 0)
    fr_c[sample_is_mc][year_index][ntracks_index][1] = p[1];
#endif

  const double xa = fr_kn[ntracks_index][k-1];
  const double xb = fr_kn[ntracks_index][k];
  const double ya = fr_c[sample_is_mc][year_index][ntracks_index][k-1];
  const double yb = fr_c[sample_is_mc][year_index][ntracks_index][k];
  const double m = (yb - ya) / (xb - xa);
  const double y = m * (x - xb) + yb;
  return exp(y);
}

double func_rho_norm(double* x, double* p) {
#ifdef FITTING_DBV
  return func_rho(x,p);
#else
  return p[0] * func_rho(x,0);
#endif
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

  for (int i = 0; i <= nbins_1v; ++i)
    bins_1v[i] = 0.0100 + 0.0020*i;

  if (nbins_2v == 3)
    bins_2v[0] = 0, bins_2v[1] = 0.04, bins_2v[2] = 0.07, bins_2v[3] = 0.11;
  else
    for (int i = 0; i <= nbins_2v; ++i)
      bins_2v[i] = 0.01*i;

  jmt::ConfigFromEnv env("sm", true);

                                       //  2017                   2018                  2017+2018
  const double default_n1v[4][3][3] = {{{  14349, 2258,  199 }, { 11600, 2094, 249 }, {  14349+11600, 2258+2094,  199+249 }},  // MC scaled to int. lumi.
                                       {{   6561, 1073,   92 }, {  3427,  642,  75 }, {   6561+ 3427, 1073+ 642,   92+ 75 }},  // MC effective
                                       {{   3203,  786,  142 }, {  3036,  689,  82 }, {   3203+ 3036,  786+ 689,  142+ 82 }},  // data 10%
                                       {{  32152, 7838, 1303 }, { 29666, 6892, 908 }, {  32152+29666, 7838+6892, 1303+908 }}   // data 100%
                                      };
  const double default_n2v[4][3][3] = {{{     55,    1,   1 }, { 14, 1, 1 }, {  55+14,   1, 1 }},
                                       {{     22,    3,   1 }, {  8, 1, 1 }, {  22+ 8, 3+1, 1 }},
                                       {{      7,    3,   1 }, { 13, 1, 1 }, {   7+13, 3+0, 1 }},
                                       {{    113,    9,   1 }, { 72, 3, 1 }, { 113+72, 9+3, 1 }}
                                      };

  const int inst = env.get_int("inst", 0);
  const int seed = env.get_int("seed", 12919135 + inst);
  const int ntoys = env.get_int("ntoys", 10000);
  const std::string out_fn = env.get_string("out_fn", "statmodel");
  const bool save_all_1v_bins = env.get_int("save_all_1v_bins", 0);
  const int samples_index = env.get_int("samples_index", 0);
  assert(samples_index >= 0 && samples_index <= 3);
  sample_is_mc = samples_index < 2;
  year_index = env.get_int("year_index", 0);
  assert(year_index >= 0 && year_index <= 2);
  ntracks = env.get_int("ntracks", 5);
  assert(ntracks >= 3 && ntracks <= 5);
  ntracks_index = ntracks - 3;
  const double n1v = env.get_double("n1v", default_n1v[samples_index][year_index][ntracks_index]);
  const double n2v = env.get_double("n2v", default_n2v[samples_index][year_index][ntracks_index]);
  const std::string true_fn = env.get_string("true_fn", "");
  const bool true_from_file = true_fn != "";
  const long ntrue_1v = env.get_long("ntrue_1v", 10000000L);
  const long ntrue_2v = env.get_long("ntrue_2v", 1000000L);
  const double oversample = env.get_double("oversample", 20);
  const std::string year_str[3] = {"2017","2018","2017p8"};
  const std::string ntuple_version = "V27m";
  const std::string rho_compare_fn = env.get_string("rho_compare_fn", env.get_string("rho_compare_path", "/uscms_data/d2/tucker/crab_dirs/Histos" + ntuple_version) + "/" + std::string(sample_is_mc ? "background_" : "JetHT") + year_str[year_index] + ".root");
  const double rho_compare_xmax = env.get_double("rho_compare_xmax", 2);
  const bool rho_compare_only = env.get_bool("rho_compare_only", false);
  phi_c = env.get_double("phi_c", 1.31);
  phi_e = env.get_double("phi_e", 2);
  phi_a = env.get_double("phi_a", 5.96);
  const std::string eff_fn = env.get_string("eff_fn", "vpeffs_" + std::string(sample_is_mc ? "" : "data_") + year_str[year_index] + "_" + ntuple_version + ".root");
  const std::string eff_path = env.get_string("eff_path", "maxtk3");
  const bool print_toys = env.get_bool("print_toys", false);
  //fr_c[0][2][2][2] = env.get_double("lastrhocoeff", -22.6856);

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

  auto finish = [&]() {
    c->Print(pdf_fn + "]");
    delete h_func_rho;
    delete f_func_rho;
    delete f_func_dphi;
    delete h_eff;
  };

  /////////////////////////////////////////////

  // 1st page of output: show the rho fcn itself lin/log

#ifndef FITTING_DBV
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
#endif

  // 2nd page: compare rho to MC background distributions.

  if (std::experimental::filesystem::exists(rho_compare_fn)) {
#ifdef FITTING_DBV
    const double rho_min = fr_kn[ntracks_index][0];
    const double rho_max = fr_kn[ntracks_index][fr_ic == 0 ? 1 : fr_ic];
    const int npar = fr_ic == 0 ? 2 : 1;
#else
    const int npar = 1;
#endif
    TF1* f_func_rho_norm = new TF1("func_rho_norm", func_rho_norm, rho_min, rho_max, npar);
    f_func_rho_norm->SetNpx(25000);
    for (int ipar = 0; ipar < npar; ++ipar)
      f_func_rho_norm->SetParameter(ipar,10);
    uptr<TFile> fin(TFile::Open(rho_compare_fn.c_str()));
    TH1* h_rho_compare = 0;
    if      (ntracks == 5) h_rho_compare = (TH1*)fin->Get(    "mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist");
    else if (ntracks == 3) h_rho_compare = (TH1*)fin->Get("Ntk3mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist");
    else if (ntracks == 4) h_rho_compare = (TH1*)fin->Get("Ntk4mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist");
    h_rho_compare->SetStats(0);
    h_rho_compare->Fit(f_func_rho_norm, sample_is_mc ? "WL R" : "LR");
    const double rho_compare_ymax = h_rho_compare->GetMaximum() * 1.4;
    double rho_compare_ymin = 1e-4;
    for (int ibin = h_rho_compare->GetNbinsX(); ibin >= 1; --ibin)
      if (h_rho_compare->GetBinLowEdge(ibin) < rho_compare_xmax && h_rho_compare->GetBinContent(ibin) > 0) {
        const double fval = f_func_rho_norm->Eval(h_rho_compare->GetBinLowEdge(ibin));
        if (fval > 1e-10) {
          rho_compare_ymin = fval * 0.1;
          break;
        }
      }
    h_rho_compare->GetXaxis()->SetRangeUser(0, rho_compare_xmax);
    h_rho_compare->GetYaxis()->SetRangeUser(rho_compare_ymin, rho_compare_ymax);
    c->SetLogy();
    uptr<TRatioPlot> rho_compare(new TRatioPlot(h_rho_compare));
    rho_compare->SetGraphDrawOpt("P");
    rho_compare->Draw("noconfint");
    c->Update();
    rho_compare->GetLowerRefYaxis()->SetRangeUser(-3,3);
    p();
#ifdef FITTING_DBV
    printf("fit dbv for ntracks %i in [%f, %f] with fr_ic = %i: %.6g", ntracks, rho_min, rho_max, fr_ic, f_func_rho_norm->GetParameter(0));
    if (fr_ic == 0) printf(", %.6g", f_func_rho_norm->GetParameter(1));
    printf("\n");
#endif
    if (getenv("asdf")) c->SaveAs("$asdf/sm_rho_compare.png");
  }
  else {
    TText tt(0.1, 0.75, TString::Format("no file %s", rho_compare_fn.c_str()));
    tt.Draw();
    p();
  }
  c->Clear();

  if (rho_compare_only) {
    finish();
    return 0;
  }

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

    out_f->cd();
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

  printf("2v bins truth fractions:");
  for (int ibin = 1; ibin <= nbins_2v; ++ibin) {
    const double tru = h_true_2v_dvv_norm->GetBinContent(ibin);
    const double pb = 1.35e-3;
    jmt::interval iv = jmt::garwood_poisson(tru, pb, pb);
    if (iv.lower < 1) iv.lower = 0;
    h_2v_dvvc_bins.emplace_back(new TH1D(TString::Format("h_2v_dvvc_bins_%i", ibin), TString::Format("d_{VV}^{C} bin %i", ibin), 200, iv.lower, iv.upper));
    printf("    %12.4f +- %12.4f", tru/n2v, h_true_2v_dvv_norm->GetBinError(ibin)/n2v);
  }
  printf("\n");

  if (ntoys == 0) {
    finish();
    return 0;
  }

  // Throw the toys and fill the above hists.
  // First throw the one vertex sample, then construct dvvc from it.
  // The toy is saved in the h_1v/2v*bins vectors.

  printf("toys:%s", print_toys ? "\n" : " ");
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
    
    if (print_toys) printf("toy %i:", itoy);
    for (int ibin = 1; ibin <= nbins_2v; ++ibin) {
      const double c = h_2v_dvvc->GetBinContent(ibin);
      h_2v_dvvc_bins[ibin-1]->Fill(c);
      if (print_toys) printf(" %.4f", c/n2v);
    }
    if (print_toys) printf("\n");

    if (!print_toys && ntoys > 10 && itoy % (ntoys/10) == 0) {
      printf("%i", itoy/(ntoys/10));
      fflush(stdout);
    }
  }
  if (!print_toys) printf(" %i\n", ntoys);

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
    bool save = save_all_1v_bins;
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
      const bool twosig = d > 2*de;
      if (twosig || i % (nbins_1v/10) == 0) {
        if (twosig) printf("\x1b[31;1m");
        printf("%3i [%.3f-%.3f) %12.4f +- %12.4f  %12.4f +- %12.4f  %12.4f +- %12.4f\n", i+1, bins_1v[i], bins_1v[i+1], b, be, t, te, d, de);
        if (twosig) printf("\x1b[0m");
      }
      if (twosig) {
        save = true;
        tl.SetTextColor(kRed);
      }
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
    if (save) p();
    c->Clear();
  }

  printf("2v bins means:\n");
  printf("%3s               %28s  %28s  %28s  %28s  %12s\n", "bin", "bin mean", "scaled true", "diff", "rms", "rms/true");
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
      const double statuncert = r / t;
      printf("%3i [%.3f-%.3f) %12.4f +- %12.4f  %12.4f +- %12.4f  %12.4f +- %12.4f  %12.4f +- %12.4f  %12.4f\n", i+1, bins_2v[i], bins_2v[i+1], b, be, t, te, b-t, sqrt(be*be + te*te), r, re, statuncert);
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
    //if (getenv("asdf")) c->SaveAs("$asdf/sm_dvvc_bins.png");
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

  out_f->cd();
  for (auto* h : {h_true_1v_rho.get(), h_true_1v_phi.get(), h_true_2v_rho.get(), h_true_2v_phi.get(), h_true_2v_dvv.get(), h_true_2v_dvv_norm.get(), h_true_2v_dphi.get(), h_2v_dvvc_bins_means.get(), h_2v_dvvc_bins_rmses.get()})
    h->Write();

  finish();
}
