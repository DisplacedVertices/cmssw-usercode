#include "Fitter.h"

#include <cassert>
#include <cmath>
#include <limits>

#include "TCanvas.h"
#include "TF1.h"
#include "TFile.h"
#include "TFitResult.h"
#include "TGraphAsymmErrors.h"
#include "TGraphErrors.h"
#include "TH2.h"
#include "TLegend.h"
#include "TMath.h"
#include "TMinuit.h"
#include "TRandom3.h"
#include "TStopwatch.h"
#include "TTree.h"

#include "Prob.h"
#include "ProgressBar.h"
#include "ROOTTools.h"
#include "Random.h"
#include "Templater.h"

namespace mfv {
  namespace fit {
    int extra_prints = 0;
    int n_calls = 0;

    int n_bins = -1;

    bool barlow_beeston = false;
    bool bend_bkg = false;
    std::vector<double> eta_bkg;
    std::vector<double> a_bkg;
    std::vector<double> A_bkg;
    TemplateInterpolator* interp;

    double n_sig_orig = -1;
    TH1D* h_sig = 0;
    std::vector<double> a_sig;
    std::vector<double> A_sig;

    TH1D* h_data_real = 0;
    TH1D* h_data_toy_sig = 0;
    TH1D* h_data_toy_bkg = 0;
    TH1D* h_data_toy = 0;
    TH1D* h_data = 0;
    const double* a_data = 0;
    double a_data_integ = 0;

    void set_n_bins(int n) {
      if (n_bins >= 0)
        jmt::vthrow("set_n_bins called twice");

      n_bins = n;
      eta_bkg.resize(n+2, -1);
      a_bkg.resize(n+2, -1);
      A_bkg.resize(n+2, -1);
      a_sig.resize(n+2, -1);
      A_sig.resize(n+2, -1);
    }

    void check_n_bins(TH1D* h) {
      if (h->GetNbinsX() != n_bins)
        jmt::vthrow("%s binning bad: n_bins = %i, h # bins: %i", h->GetName(), n_bins, h->GetNbinsX());
    }

    void set_sig(TH1D* h) {
      check_n_bins(h);
      h_sig = h;
      for (int i = 1; i <= n_bins; ++i)
        a_sig[i] = h->GetBinContent(i);
    }

    void set_data_no_check(TH1D* h) {
      h_data = h;
      a_data = h->GetArray();
      a_data_integ = h->Integral();
    }

    void set_data_real() {
      set_data_no_check(h_data_real);
    }

    void globals_ok() {
      if (n_bins < 0 || h_data == 0 || h_sig == 0 || h_data_real == 0 || interp == 0)
        jmt::vthrow("fit globals not set up properly: n_bins: %i  h_data: %p  h_sig: %p  h_data_real: %p  interp: %p", n_bins, h_data, h_sig, h_data_real, interp);
    }

    double lnL_offset = 0;

    void calc_lnL_offset() {
      lnL_offset = 0;
      for (int i = 1; i <= n_bins; ++i)
        lnL_offset -= n_sig_orig * a_sig[i] * log(n_sig_orig * a_sig[i]) - n_sig_orig * a_sig[i]; 
    }

    int RootsQuad(const long double* coef, long double& x0, long double& x1) {
      long double a = coef[2];
      long double b = coef[1];
      long double c = coef[0];
      long double det = b*b - 4*a*c;
      int nrealroots = 2;
      if (det < 0.L) {
        nrealroots = 0;
        x0 = -b/a/2.L;
        x1 = sqrtl(-det)/a/2.L;
      }
      else if (det == 0.L) {
        nrealroots = 1;
        x0 = x1 = -b/a/2.L;
      }
      else {
        x0 =(-b-sqrtl(det))/a/2.L;
        x1 =(-b+sqrtl(det))/a/2.L;
      }
      return nrealroots;
    }

    Bool_t RootsCubic(const long double* coef, long double &a, long double &b, long double &c)
    {
      // Calculates roots of polynomial of 3rd order a*x^3 + b*x^2 + c*x + d, where
      // a == coef[3], b == coef[2], c == coef[1], d == coef[0]
      //coef[3] must be different from 0
      // If the boolean returned by the method is false:
      //    ==> there are 3 real roots a,b,c
      // If the boolean returned by the method is true:
      //    ==> there is one real root a and 2 complex conjugates roots (b+i*c,b-i*c)
      // Author: Francois-Xavier Gentit

      Bool_t complex = kFALSE;
      long double r,s,t,p,q,d,ps3,ps33,qs2,u,v,tmp,lnu,lnv,su,sv,y1,y2,y3;
      a    = 0.L;
      b    = 0.L;
      c    = 0.L;
      if (coef[3] == 0.L) return complex;
      r    = coef[2]/coef[3];
      s    = coef[1]/coef[3];
      t    = coef[0]/coef[3];
      p    = s - (r*r)/3.L;
      ps3  = p/3.L;
      q    = (2.L*r*r*r)/27.L - (r*s)/3.L + t;
      qs2  = q/2.L;
      ps33 = ps3*ps3*ps3;
      d    = ps33 + qs2*qs2;
      if (d>=0.L) {
        complex = kTRUE;
        d   = sqrtl(d);
        u   = -qs2 + d;
        v   = -qs2 - d;
        tmp = 1.L/3.L;
        lnu = logl(fabsl(u));
        lnv = logl(fabsl(v));
        su  = u < 0 ? -1.L : 1.L;
        sv  = v < 0 ? -1.L : 1.L;
        u   = su*expl(tmp*lnu);
        v   = sv*expl(tmp*lnv);
        y1  = u + v;
        y2  = -y1/2.L;
        y3  = ((u-v)*sqrtl(3.L))/2.L;
        tmp = r/3.L;
        a   = y1 - tmp;
        b   = y2 - tmp;
        c   = y3;
      } else {
        long double phi,cphi,phis3,c1,c2,c3,pis3;
        ps3   = -ps3;
        ps33  = -ps33;
        cphi  = -qs2/sqrtl(ps33);
        phi   = acosl(cphi);
        phis3 = phi/3.L;
        pis3  = M_PI/3.L;
        c1    = cosl(phis3);
        c2    = cosl(pis3 + phis3);
        c3    = cosl(pis3 - phis3);
        tmp   = sqrtl(ps3);
        y1    = 2.L*tmp*c1;
        y2    = -2.L*tmp*c2;
        y3    = -2.L*tmp*c3;
        tmp = r/3.L;
        a   = y1 - tmp;
        b   = y2 - tmp;
        c   = y3 - tmp;
      }
      return complex;
    }

    double twolnL(double mu_sig, double mu_bkg, double par0, double par1) {
      if (TMath::IsNaN(mu_sig) || TMath::IsNaN(mu_bkg) || TMath::IsNaN(par0) || TMath::IsNaN(par1))
        //jmt::vthrow("NaN in twolnL(%f, %f, %f, %f)", mu_sig, mu_bkg, par0, par1);
        return std::numeric_limits<double>::quiet_NaN();

      //return -pow(mu_sig - 0, 2) -pow(mu_bkg - 234, 2) - pow(par0 - 0.03, 2) - pow(par1 - 0.01, 2);

      //static int local_ncalls = 0;
      //printf("call %i\n", ++local_ncalls);
      //if (local_ncalls == 5075000) {
      //  extra_prints=1;
      //  TemplateInterpolator::extra_prints=1;
      //}

      if (mu_sig < 1e-12)
        mu_sig = 1e-12;
      if (mu_bkg < 1e-12)
        mu_bkg = 1e-12;
      if (par0 < 0)
        par0 = 0;
      if (par1 < 0.0005)
        par1 = 0.0005;

      interp->interpolate(par0, par1);

      for (int i = 1; i < n_bins; ++i) {
        if (TMath::IsNaN(a_bkg[i]))
          jmt::vthrow("NaN in interpolation (%f, %f) in bin %i", par0, par1, i);
        else if (a_bkg[i] < 0)
          jmt::vthrow("negative in interpolation (%f, %f) in bin %i", par0, par1, i);
      }

      if (extra_prints)
        printf("\n--- twolnL call ---\nmu_sig: %f  mu_bkg: %f\npar0: %f  par1: %f\n", mu_sig, mu_bkg, par0, par1);

      A_sig.assign(n_bins+2, 0.);
      A_bkg.assign(n_bins+2, 0.);
      double A_sig_sum = 0, A_bkg_sum = 0;

      for (int i = 1; i <= n_bins; ++i) {
        const double sig_bkg = eta_bkg[i] / mu_bkg;
        const double sig_bkg_2 = sig_bkg * sig_bkg;

        if (!barlow_beeston) {
          A_sig_sum += (A_sig[i] = a_sig[i]);
          A_bkg_sum += (A_bkg[i] = a_bkg[i]*(1. + (bend_bkg ? sig_bkg : 0.)));
          continue;
        }

        double t = 0.;

        if (a_data[i] > 1e-6) {
          const double t_lo = -n_sig_orig/mu_sig;
          const double t_hi = 1.; //std::min(a_bkg[i] / mu_bkg / sig_bkg_2, 1.);

          const long double coeff[4] = {
            a_data[i] - mu_sig * a_sig[i] - mu_bkg * a_bkg[i],
            a_data[i] * mu_sig / n_sig_orig + mu_sig * a_sig[i] - (mu_sig / n_sig_orig - 1) * mu_bkg * a_bkg[i] + eta_bkg[i] * eta_bkg[i],
            mu_bkg * a_bkg[i] * mu_sig / n_sig_orig + eta_bkg[i] * eta_bkg[i] * (mu_sig / n_sig_orig - 1),
            - eta_bkg[i] * eta_bkg[i] * mu_sig / n_sig_orig
          };

          std::vector<long double> ts(3, 1e99);
          int nr;
          if (fabs(coeff[3]/coeff[2]) > 1e-3)
            nr = RootsCubic(coeff, ts[0], ts[1], ts[2]) ? 1 : 3;
          else
            nr = RootsQuad(coeff, ts[0], ts[1]);
          std::sort(ts.begin(), ts.end(), [](long double x, long double y) { return fabs(x) < fabs(y); });

          int nok = 0;
          bool found = false;
          for (int ir = 0; ir < nr; ++ir)
            if (ts[ir] > t_lo && ts[ir] < t_hi) {
              ++nok;
              if (!found) {
                found = true;
                t = ts[ir];
              }
            }

          if (extra_prints) {
            printf("find t: bin %i  d: %5.1f  eta_bkg: %10.3e  sig_bkg: %10.3e  a_bkg: %10.3e  a_sig: %10.3e -> t in [%e, %e]\n", i, a_data[i], eta_bkg[i], sig_bkg, a_bkg[i], a_sig[i], t_lo, t_hi);
            printf("f:=d/(1-t)-mb*(ab-t*mb*sigb*sigb)-ms*as/(1+t*ms/N);\n");
            printf("Z:=ms/N; g:=(-(mb*sigb)^2*Z)*t^3 + (mb*ab*Z+(mb*sigb)^2*(Z-1))*t^2 + (d*Z+ms*as-(Z-1)*mb*ab+(mb*sigb)^2)*t + (d-ms*as-mb*ab);\n");
            printf("solve(eval(f,{d=%.1f,mb=%.6e,ab=%.6e,sigb=%.6e,ms=%.6e,as=%.6e,N=%.1f}),t);\n", a_data[i], mu_bkg, a_bkg[i], sig_bkg, mu_sig, a_sig[i], n_sig_orig);
            printf("solve(eval(g,{d=%.1f,mb=%.6e,ab=%.6e,sigb=%.6e,ms=%.6e,as=%.6e,N=%.1f}),t);\n", a_data[i], mu_bkg, a_bkg[i], sig_bkg, mu_sig, a_sig[i], n_sig_orig);
            printf("solve((%.6Le) + (%.6Le) * t + (%.6Le) * t^2 + (%.6Le) * t^3, t);\n", coeff[0], coeff[1], coeff[2], coeff[3]);
            //printf("coeffs:  %.6Le  %.6Le  %.6Le  %.6Le\n", coeff[0], coeff[1], coeff[2], coeff[3]);
            //fflush(stdout);
            //for (int jmt = 0; jmt < 4; ++jmt)
            //  printf("coeff%i: %.6Le\n", jmt, coeff[jmt]);
            //fflush(stdout);
            printf("num roots = %i : a = %.6Le  b = %.6Le  c = %.6Le -> num ok = %i\n", nr, ts[0], ts[1], ts[2], nok);
          }

          if (nok > 1)
            jmt::vthrow("more than one solution for t");
          else if (nok != 1)
            jmt::vthrow("no solution for t");
        }
        else {
          t = 1.;
          if (extra_prints)
            printf("find t: bin %i  d: 0 -> t = 1\n", i);
        }

        A_sig[i] = a_sig[i] / (t * mu_sig / n_sig_orig + 1);
        A_bkg[i] = a_bkg[i] - t * mu_bkg * sig_bkg_2;
        if (A_bkg[i] < 0)
          A_bkg[i] = 0;

        if (A_sig[i] < 0 || A_bkg[i] < 0)
          jmt::vthrow("negative A_sig");

        A_sig_sum += A_sig[i];
        A_bkg_sum += A_bkg[i];
      }

      if (extra_prints) {
        for (int times = 0; times < 2; ++times) {
          if (times)
            printf("mu*a -> mu*A:\n");
          else
            printf("a -> A (i.e. not times mu_sig/bkg):\n");
          double a_sig_sum = 0, a_bkg_sum = 0;
          const double m_sig = times ? mu_sig : 1;
          const double m_bkg = times ? mu_bkg : 1;
          printf("   %10s %10s %10s %10s %10s %10s\n", "a_bkg", "A_bkg", "dlt_bkg", "a_sig", "A_sig", "dlt_sig");
          for (int i = 1; i <= n_bins; ++i) {
            a_bkg_sum += a_bkg[i];
            a_sig_sum += a_sig[i];
            printf("%2i %10.3e %10.3e %10.3e %10.3e %10.3e %10.3e\n", i, m_bkg * a_bkg[i], m_bkg * A_bkg[i], m_bkg * (A_bkg[i] - a_bkg[i]), m_sig * a_sig[i], m_sig * A_sig[i], m_sig * (A_sig[i] - a_sig[i]));
          }
          printf("sums:\n");
          printf("   %10.3e %10.3e %10.3e %10.3e %10.3e %10.3e\n", m_bkg * a_bkg_sum, m_bkg * A_bkg_sum, m_bkg * (A_bkg_sum - a_bkg_sum), m_sig * a_sig_sum, m_sig * A_sig_sum, m_sig * (A_sig_sum - a_sig_sum));
        }
      }

      double lnL_bb_bkg = 0;
      double lnL_bb_sig = 0;
      double lnL_fit = 0;

      for (int i = 1; i <= n_bins; ++i) {
        const double sig_bkg = eta_bkg[i] / mu_bkg;
        const double dlnL_bb_bkg = barlow_beeston ? (a_bkg[i] == 0. ? 0. : -0.5 * pow((a_bkg[i] - A_bkg[i])/sig_bkg, 2)) : 0;
        const double dlnL_bb_sig = barlow_beeston ? (n_sig_orig * a_sig[i] * log(n_sig_orig * A_sig[i]) - n_sig_orig * A_sig[i]) : 0;

        const double nu_sig = mu_sig * A_sig[i];
        const double nu_bkg = mu_bkg * A_bkg[i];
        const double nu_sum = nu_sig + nu_bkg;
        const double dlnL_fit = -nu_sum + a_data[i] * log(nu_sum);

        lnL_fit += dlnL_fit;
        lnL_bb_bkg += dlnL_bb_bkg;
        lnL_bb_sig += dlnL_bb_sig;

        if (extra_prints)
          printf("i: %2i  nu_bkg: %7.3f  nu_sig: %7.3f  nu: %7.3f  n: %6.1f    dlnL: %10.6f + %10.6f + %10.6f  lnL: %10.6f + %10.6f + %10.6f\n", i, nu_bkg, nu_sig, nu_sum, a_data[i], dlnL_fit, dlnL_bb_bkg, dlnL_bb_sig, lnL_fit, lnL_bb_bkg, lnL_bb_sig);
      }

      double lnL = lnL_fit; 
      if (barlow_beeston) {
        lnL += lnL_bb_bkg;
        lnL += lnL_offset + lnL_bb_sig;
      }

      //lnL += -0.5*pow((par0 - 0.03)/0.01, 2) - 0.5*pow((par1 - 0.01)/0.01, 2);

      ++n_calls;

      if (TMath::IsNaN(lnL))
        jmt::vthrow("lnL is NaN");
      return 2*lnL;
    }

    void minfcn(int&, double*, double& f, double* par, int) {
      f = -twolnL(par[0], par[1], par[2], par[3]);
    }
  }

  //////////////////////////////////////////////////////////////////////////////

  std::string Fitter::min_lik_t::nuis_title() const {
    char buf[128];
    snprintf(buf, 128, "nuis 0:  %f #pm %f  nuis1: %f #pm %f", nuis0, err_nuis0, nuis1, err_nuis1);
    return std::string(buf);
  }

  std::string Fitter::min_lik_t::mu_title() const {
    char buf[256];
    snprintf(buf, 128, "#mu_{sig} = %f #pm %f, #mu_{bkg} = %f #pm %f", mu_sig, err_mu_sig, mu_bkg, err_mu_bkg);
    return std::string(buf);
  }

  std::string Fitter::min_lik_t::title() const {
    return mu_title() + "  " + nuis_title();
  }


  void Fitter::min_lik_t::print(const char* header, const char* indent) const {
    printf("%s%s  istat = %i  maxtwolnL = %10.4e  mu_sig = %7.3f +- %7.3f    mu_bkg = %7.3f +- %7.3f  nuis0 = %7.3f +- %7.3f [%7.3f, %7.3f]  nuis1 = %7.3f +- %7.3f [%7.3f, %7.3f]  corr %7.3f\n", indent, header, istat, maxtwolnL, mu_sig, err_mu_sig, mu_bkg, err_mu_bkg, nuis0, err_nuis0, nuis0 + eminus_nuis0, nuis0 + eplus_nuis0, nuis1, err_nuis1, nuis1 + eminus_nuis1, nuis1 + eplus_nuis1, correlation_nuis);
    printf("%s    A_sig ", indent);
    const int ie = fit::n_bins; // JMTBAD
    for (int i = 1; i <= ie; ++i) printf("%6.4f (%4.2f) ", A_sig[i], A_sig_rel[i]);
    printf("  sum: %5.3f\n", A_sig_sum);
    printf("%s    A_bkg ", indent);
    for (int i = 1; i <= ie; ++i) printf("%6.4f (%4.2f) ", A_bkg[i], A_bkg_rel[i]);
    printf("  sum: %5.3f\n", A_bkg_sum);
    double sum = 0;
    printf("%s    yield: ", indent);
    for (int i = 1; i <= ie; ++i) {
      const double y = yield_in_bin(i);
      sum += y;
      printf("%6.2f ", y);
    }
    printf("  sum: %.2f\n", sum);
  }

  void Fitter::test_stat_t::print(const char* header, const int i, const char* indent) const {
    if (i < 0)
      printf("%s:", header);
    else
      printf("%s #%i:", header, i);
    printf("  ok? %i  t = %f\n", ok(), t);
    h1.print("h1", indent);
    h0.print("h0", indent);
  }

  //////////////////////////////////////////////////////////////////////////////

  Fitter::Fitter(const std::string& name_, TFile* f, TRandom* r)
    : name (name_.size() ? " " + name_ : ""),
      uname(name_.size() ? "_" + name_ : ""),

      env("mfvo2t_fitter" + uname),
      print_level(env.get_int("print_level", -1)),
      save_plots(env.get_bool("save_plots", true)),
      inject_in_last_bin(env.get_int("inject_in_last_bin", 0)),
      bkg_gaussians(env.get_bool("bkg_gaussians", true)),
      bkg_gaussians_all(env.get_bool("bkg_gaussians_all", false)),
      barlow_beeston(env.get_bool("barlow_beeston", true)),
      bend_bkg(env.get_bool("bend_bkg", false)),
      allow_negative_mu_sig(env.get_bool("allow_negative_mu_sig", false)),
      run_mnseek(env.get_bool("run_mnseek", false)),
      run_minos(env.get_bool("run_minos", true)),
      draw_bkg_templates(env.get_bool("draw_bkg_templates", 0)),
      fix_nuis0(env.get_bool("fix_nuis0", 0)),
      fix_nuis1(env.get_bool("fix_nuis1", 0)),
      start_nuis0(env.get_double("start_nuis0", 0.025)),
      start_nuis1(env.get_double("start_nuis1", 0.008)),
      fluctuate_toys_shapes(env.get_bool("fluctuate_toys_shapes", true)),
      n_toy_signif(env.get_int("n_toy_signif", 10000)),
      print_toys(env.get_bool("print_toys", false)),
      print_subtoys(env.get_bool("print_subtoys", false)),
      save_toys(env.get_bool("save_toys", false)),
      do_signif(env.get_bool("do_signif", true)),
      do_limit(env.get_bool("do_limit", true)),
      only_fit(env.get_bool("only_fit", false)),
      n_toy_cls(env.get_int("n_toy_cls", 10000)),
      do_cls(env.get_bool("do_cls", true)),
      i_limit_job(env.get_int("i_limit_job", -1)),
      n_toy_limit(env.get_int("n_toy_limit", 10000)),
      sig_limit_start(env.get_double("sig_limit_start", 0.01)),
      sig_limit_stop(env.get_double("sig_limit_stop", 250)),
      sig_limit_step(env.get_double("sig_limit_step", 0.25)),
      sig_eff(env.get_double("sig_eff", 1.)),
      sig_eff_uncert(env.get_double("sig_eff_uncert", 0.2)),
      bracket_limit(env.get_bool("bracket_limit", false)),

      fout(f),
      dout(f->mkdir(TString::Format("Fitter%s", uname.c_str()))),
      dtoy(0),
      rand(r),
      seed(r->GetSeed() - jmt::seed_base)
  {
    printf("Fitter%s config:\n", name.c_str());
    printf("print_level: %i\n", print_level);
    printf("bkg_gaussians: %i\n", bkg_gaussians);
    printf("bkg_gaussians_all: %i\n", bkg_gaussians_all);
    printf("barlow_beeston: %i\n", barlow_beeston);
    printf("bend_bkg: %i\n", bend_bkg);
    printf("allow_negative_mu_sig: %i\n", allow_negative_mu_sig);
    printf("run_mnseek: %i\n", run_mnseek);
    printf("run_minos: %i\n", run_minos);
    printf("draw_bkg_templates: %i\n", draw_bkg_templates);
    printf("fix_nuis 0: %i  1: %i\n", fix_nuis0, fix_nuis1);
    printf("start_nuis: %f, %f\n", start_nuis0, start_nuis1);
    printf("fluctuate_toys_shapes: %i\n", fluctuate_toys_shapes);
    printf("n_toy_signif: %i\n", n_toy_signif);
    printf("print_toys? %i (sub? %i)\n", print_toys, print_subtoys);
    printf("save_toys? %i\n", save_toys);
    printf("do_signif? %i\n", do_signif);
    printf("do_limit? %i\n", do_limit);
    printf("only_fit? %i\n", only_fit);
    printf("do_cls? %i  n_toy_cls: %i\n", do_cls, n_toy_cls);
    printf("i_limit_job: %i\n", i_limit_job);
    printf("n_toy_limit: %i (~%f uncert @ 0.05)\n", n_toy_limit, sqrt(0.05*0.95/n_toy_limit));
    printf("sig_limit_scan: %f-%f in %f steps\n", sig_limit_start, sig_limit_stop, sig_limit_step);
    printf("sig_eff: %f +- %f\n", sig_eff, sig_eff_uncert);
    printf("bracket_limit: %i\n", bracket_limit);

    fflush(stdout);

    fit::set_n_bins(Template::binning().size()-1);

    book_trees();
  }

  void Fitter::book_trees() {
    dout->cd();

    TTree* t_config = new TTree("t_config", "");
    t_config->Branch("seed", const_cast<int*>(&seed), "seed/I");
    t_config->Branch("bkg_gaussians", const_cast<bool*>(&bkg_gaussians));
    t_config->Branch("bkg_gaussians_all", const_cast<bool*>(&bkg_gaussians_all));
    t_config->Branch("barlow_beeston", const_cast<bool*>(&barlow_beeston));
    t_config->Branch("bend_bkg", const_cast<bool*>(&bend_bkg));
    t_config->Branch("allow_negative_mu_sig", const_cast<bool*>(&allow_negative_mu_sig));
    t_config->Branch("run_mnseek", const_cast<bool*>(&run_mnseek));
    t_config->Branch("run_minos", const_cast<bool*>(&run_minos));
    t_config->Branch("fix_nuis0", const_cast<bool*>(&fix_nuis0));
    t_config->Branch("fix_nuis1", const_cast<bool*>(&fix_nuis1));
    t_config->Branch("start_nuis0", const_cast<double*>(&start_nuis0));
    t_config->Branch("start_nuis1", const_cast<double*>(&start_nuis1));
    t_config->Branch("fluctuate_toys_shapes", const_cast<bool*>(&fluctuate_toys_shapes));
    t_config->Branch("n_toy_signif", const_cast<int*>(&n_toy_signif));
    t_config->Branch("n_toy_limit", const_cast<int*>(&n_toy_limit));
    t_config->Branch("n_toy_cls", const_cast<int*>(&n_toy_cls));
    t_config->Branch("do_cls", const_cast<bool*>(&do_cls));
    t_config->Branch("sig_limit_start", const_cast<double*>(&sig_limit_start));
    t_config->Branch("sig_limit_step", const_cast<double*>(&sig_limit_step));
    t_config->Branch("sig_eff", const_cast<double*>(&sig_eff));
    t_config->Branch("sig_eff_uncert", const_cast<double*>(&sig_eff_uncert));
    t_config->Fill();


    t_fit_info = new TTree("t_fit_info", "");
    t_fit_info->Branch("seed", const_cast<int*>(&seed), "seed/I");
    t_fit_info->Branch("toy", &toy, "toy/I");
    t_fit_info->Branch("true_pars", &true_pars);
    t_fit_info->Branch("t_obs_0__h1_istat", &t_obs_0.h1.istat, "t_obs_0__h1_istat/I");
    t_fit_info->Branch("t_obs_0__h1_maxtwolnL", &t_obs_0.h1.maxtwolnL, "t_obs_0__h1_maxtwolnL/D");
    t_fit_info->Branch("t_obs_0__h1_mu_sig", &t_obs_0.h1.mu_sig, "t_obs_0__h1_mu_sig/D");
    t_fit_info->Branch("t_obs_0__h1_err_mu_sig", &t_obs_0.h1.err_mu_sig, "t_obs_0__h1_err_mu_sig/D");
    t_fit_info->Branch("t_obs_0__h1_eplus_mu_sig", &t_obs_0.h1.eplus_mu_sig, "t_obs_0__h1_eplus_mu_sig/D");
    t_fit_info->Branch("t_obs_0__h1_eminus_mu_sig", &t_obs_0.h1.eminus_mu_sig, "t_obs_0__h1_eminus_mu_sig/D");
    t_fit_info->Branch("t_obs_0__h1_A_sig_sum", &t_obs_0.h1.A_sig_sum);
    t_fit_info->Branch("t_obs_0__h1_mu_bkg", &t_obs_0.h1.mu_bkg, "t_obs_0__h1_mu_bkg/D");
    t_fit_info->Branch("t_obs_0__h1_err_mu_bkg", &t_obs_0.h1.err_mu_bkg, "t_obs_0__h1_err_mu_bkg/D");
    t_fit_info->Branch("t_obs_0__h1_eplus_mu_bkg", &t_obs_0.h1.eplus_mu_bkg, "t_obs_0__h1_eplus_mu_bkg/D");
    t_fit_info->Branch("t_obs_0__h1_eminus_mu_bkg", &t_obs_0.h1.eminus_mu_bkg, "t_obs_0__h1_eminus_mu_bkg/D");
    t_fit_info->Branch("t_obs_0__h1_A_bkg_sum", &t_obs_0.h1.A_bkg_sum);
    t_fit_info->Branch("t_obs_0__h1_nuis0", &t_obs_0.h1.nuis0, "t_obs_0__h1_nuis0/D");
    t_fit_info->Branch("t_obs_0__h1_err_nuis0", &t_obs_0.h1.err_nuis0, "t_obs_0__h1_err_nuis0/D");
    t_fit_info->Branch("t_obs_0__h1_eplus_nuis0", &t_obs_0.h1.eplus_nuis0, "t_obs_0__h1_eplus_nuis0/D");
    t_fit_info->Branch("t_obs_0__h1_eminus_nuis0", &t_obs_0.h1.eminus_nuis0, "t_obs_0__h1_eminus_nuis0/D");
    t_fit_info->Branch("t_obs_0__h1_nuis1", &t_obs_0.h1.nuis1, "t_obs_0__h1_nuis1/D");
    t_fit_info->Branch("t_obs_0__h1_err_nuis1", &t_obs_0.h1.err_nuis1, "t_obs_0__h1_err_nuis1/D");
    t_fit_info->Branch("t_obs_0__h1_eplus_nuis1", &t_obs_0.h1.eplus_nuis1, "t_obs_0__h1_eplus_nuis1/D");
    t_fit_info->Branch("t_obs_0__h1_eminus_nuis1", &t_obs_0.h1.eminus_nuis1, "t_obs_0__h1_eminus_nuis1/D");
    t_fit_info->Branch("t_obs_0__h1_correlation_nuis", &t_obs_0.h1.correlation_nuis, "t_obs_0__h1_correlation_nuis/D");
    t_fit_info->Branch("t_obs_0__h0_istat", &t_obs_0.h0.istat, "t_obs_0__h0_istat/I");
    t_fit_info->Branch("t_obs_0__h0_maxtwolnL", &t_obs_0.h0.maxtwolnL, "t_obs_0__h0_maxtwolnL/D");
    t_fit_info->Branch("t_obs_0__h0_mu_sig", &t_obs_0.h0.mu_sig, "t_obs_0__h0_mu_sig/D");
    t_fit_info->Branch("t_obs_0__h0_err_mu_sig", &t_obs_0.h0.err_mu_sig, "t_obs_0__h0_err_mu_sig/D");
    t_fit_info->Branch("t_obs_0__h0_eplus_mu_sig", &t_obs_0.h0.eplus_mu_sig, "t_obs_0__h0_eplus_mu_sig/D");
    t_fit_info->Branch("t_obs_0__h0_eminus_mu_sig", &t_obs_0.h0.eminus_mu_sig, "t_obs_0__h0_eminus_mu_sig/D");
    t_fit_info->Branch("t_obs_0__h0_A_sig_sum", &t_obs_0.h0.A_sig_sum);
    t_fit_info->Branch("t_obs_0__h0_mu_bkg", &t_obs_0.h0.mu_bkg, "t_obs_0__h0_mu_bkg/D");
    t_fit_info->Branch("t_obs_0__h0_err_mu_bkg", &t_obs_0.h0.err_mu_bkg, "t_obs_0__h0_err_mu_bkg/D");
    t_fit_info->Branch("t_obs_0__h0_eplus_mu_bkg", &t_obs_0.h0.eplus_mu_bkg, "t_obs_0__h0_eplus_mu_bkg/D");
    t_fit_info->Branch("t_obs_0__h0_eminus_mu_bkg", &t_obs_0.h0.eminus_mu_bkg, "t_obs_0__h0_eminus_mu_bkg/D");
    t_fit_info->Branch("t_obs_0__h0_A_bkg_sum", &t_obs_0.h0.A_bkg_sum);
    t_fit_info->Branch("t_obs_0__h0_nuis0", &t_obs_0.h0.nuis0, "t_obs_0__h0_nuis0/D");
    t_fit_info->Branch("t_obs_0__h0_err_nuis0", &t_obs_0.h0.err_nuis0, "t_obs_0__h0_err_nuis0/D");
    t_fit_info->Branch("t_obs_0__h0_eplus_nuis0", &t_obs_0.h0.eplus_nuis0, "t_obs_0__h0_eplus_nuis0/D");
    t_fit_info->Branch("t_obs_0__h0_eminus_nuis0", &t_obs_0.h0.eminus_nuis0, "t_obs_0__h0_eminus_nuis0/D");
    t_fit_info->Branch("t_obs_0__h0_nuis1", &t_obs_0.h0.nuis1, "t_obs_0__h0_nuis1/D");
    t_fit_info->Branch("t_obs_0__h0_err_nuis1", &t_obs_0.h0.err_nuis1, "t_obs_0__h0_err_nuis1/D");
    t_fit_info->Branch("t_obs_0__h0_eplus_nuis1", &t_obs_0.h0.eplus_nuis1, "t_obs_0__h0_eplus_nuis1/D");
    t_fit_info->Branch("t_obs_0__h0_eminus_nuis1", &t_obs_0.h0.eminus_nuis1, "t_obs_0__h0_eminus_nuis1/D");
    t_fit_info->Branch("t_obs_0__h0_correlation_nuis", &t_obs_0.h0.correlation_nuis, "t_obs_0__h0_correlation_nuis/D");
    t_fit_info->Branch("t_obs_0__t", &t_obs_0.t, "t_obs_0__t/D");
    t_fit_info->Branch("fs_chi2", &fit_stat.chi2);
    t_fit_info->Branch("fs_ndof", &fit_stat.ndof);
    t_fit_info->Branch("fs_prob", &fit_stat.prob);
    t_fit_info->Branch("fs_ks", &fit_stat.ks);
    t_fit_info->Branch("pval_signif", &pval_signif);
    t_fit_info->Branch("pval_cls", &pval_signif);
    t_fit_info->Branch("sig_limits", &sig_limits);
    t_fit_info->Branch("pval_limits", &pval_limits);
    t_fit_info->Branch("pval_limit_errs", &pval_limit_errs);
    t_fit_info->Branch("sig_limit", &sig_limit);
    t_fit_info->Branch("sig_limit_err", &sig_limit_err);
    t_fit_info->Branch("sig_limit_fit_n", &sig_limit_fit_n);
    t_fit_info->Branch("sig_limit_fit_a", &sig_limit_fit_a);
    t_fit_info->Branch("sig_limit_fit_b", &sig_limit_fit_b);
    t_fit_info->Branch("sig_limit_fit_a_err", &sig_limit_fit_a_err);
    t_fit_info->Branch("sig_limit_fit_b_err", &sig_limit_fit_b_err);
    t_fit_info->Branch("sig_limit_fit_prob", &sig_limit_fit_prob);

    t_fit_info->SetAlias("s_true", "true_pars[0]");
    t_fit_info->SetAlias("b_true", "true_pars[1]");
  }    

  void Fitter::draw_likelihood(const test_stat_t& t, const char* ex) {
    //printf("draw_likelihood: ");

    struct scan_t {
      int n;
      double min;
      double max;
      double d() const { return (max - min)/n; }
      double v(int i) const { return min + d() * i; }
    };

    scan_t mu_scan[2] = {
      { 200, 0, 200 },
      { 400, 0, 400 }
    };

    const size_t npars = bkg_templates->at(0)->npars();
    std::vector<double> mins(npars,  1e99);
    std::vector<double> maxs(npars, -1e99);
    for (Template* tp : *bkg_templates)
      for (size_t ipar = 0; ipar < npars; ++ipar) {
        double t_par = tp->par(ipar);
        if (t_par > maxs[ipar])
          maxs[ipar] = t_par;
        if (t_par < mins[ipar])
          mins[ipar] = t_par;
      }
    int n_nuis[2] = {200, 200};
    if (maxs[1] <= mins[1]) {
      maxs[1] = mins[1] + 1;
      n_nuis[1] = 3;
    }

    scan_t nuis_scan[2] = {
      { n_nuis[0], mins[0], maxs[0] },
      { n_nuis[1], mins[1], maxs[1] }
    };

    TDirectory* cwd = gDirectory;

    TString ex_(ex);
    if (ex)
      ex_ += "_";

    for (int sb = 1; sb >= 0; --sb) {
      const char* sb_or_b = sb ? "sb" : "b";
      //printf("%s: ", sb_or_b); fflush(stdout);
      const char* sb_or_b_nice = sb ? "sig + bkg" : "b only";
      const min_lik_t& ml = sb ? t.h1 : t.h0;

      TDirectory* subdir = 0;
      if (draw_bkg_templates)
        subdir = cwd->mkdir(TString::Format("bkg_template_scan_nuis_%s", sb_or_b));

      if (draw_bkg_templates)
        cwd->cd();

      TH2F* h1 = new TH2F(TString::Format("h_likelihood_%s%s_scannuis", ex_.Data(), sb_or_b),
                          TString::Format("Best %s fit: %s;nuis. par 0;nuis. par 1", sb_or_b_nice, ml.title().c_str()),
                          nuis_scan[0].n, nuis_scan[0].min, nuis_scan[0].max,
                          nuis_scan[1].n, nuis_scan[1].min, nuis_scan[1].max
                          );

      for (int i0 = 1; i0 <= nuis_scan[0].n; ++i0) {
        const double nuispar0 = nuis_scan[0].v(i0);

        if (draw_bkg_templates)
          subdir->mkdir(TString::Format("nuis0_%03i", i0))->cd();

        for (int i1 = 1; i1 <= nuis_scan[1].n; ++i1) {
          //fit::extra_prints = i0 == 186 && i1 == 1;
          //fit::interp->extra_prints = i0 == 186 && i1 == 1;

          const double nuispar1 = nuis_scan[1].v(i1);
          const double twolnL = fit::twolnL(ml.mu_sig, ml.mu_bkg, nuispar0, nuispar1);

          if (draw_bkg_templates)
            make_h_bkg(TString::Format("h_bkg_template_scan_%s_nuis0_%03i_nuis1_%03i", sb_or_b, i0, i1), std::vector<double>({nuispar0, nuispar1}), std::vector<double>());

          //printf("i0: %i %f  i1: %i %f  %f\n", i0, nuispar0, i1, nuispar1, twolnL);
          h1->SetBinContent(i0, i1, twolnL);
        }
      }

      if (draw_bkg_templates)
        cwd->cd();

      TH2F* h2 = new TH2F(TString::Format("h_likelihood_%s%s_scanmus", ex_.Data(), sb_or_b),
                          TString::Format("Best %s fit: %s;#mu_{sig};#mu_{bkg}", sb_or_b_nice, ml.title().c_str()),
                          mu_scan[0].n, mu_scan[0].min, mu_scan[0].max,
                          mu_scan[1].n, mu_scan[1].min, mu_scan[1].max
                          );

      for (int i0 = 1; i0 <= mu_scan[0].n; ++i0) {
        const double mu_sig = mu_scan[0].v(i0);
        for (int i1 = 1; i1 <= mu_scan[1].n; ++i1) {
          const double mu_bkg = mu_scan[1].v(i1);
          h2->SetBinContent(i0, i1, fit::twolnL(mu_sig, mu_bkg, ml.nuis0, ml.nuis1));
        }
      }

      TH2F* h3 = new TH2F(TString::Format("h_likelihood_%s%s_scan_mubkg_nuis0", ex_.Data(), sb_or_b),
                          TString::Format("Best %s fit: %s;nuis. par 0;#mu_{bkg}", sb_or_b_nice, ml.title().c_str()),
                          nuis_scan[0].n, nuis_scan[0].min, nuis_scan[0].max,
                          mu_scan[1].n, mu_scan[1].min, mu_scan[1].max
                          );

      for (int i0 = 1; i0 <= nuis_scan[0].n; ++i0) {
        const double nuispar0 = nuis_scan[0].v(i0);
        for (int i1 = 1; i1 <= mu_scan[1].n; ++i1) {
          const double mu_bkg = mu_scan[1].v(i1);
          h3->SetBinContent(i0, i1, fit::twolnL(ml.mu_sig, mu_bkg, nuispar0, ml.nuis1));
        }
      }

      TH2F* h4 = new TH2F(TString::Format("h_likelihood_%s%s_scan_mubkg_nuis1", ex_.Data(), sb_or_b),
                          TString::Format("Best %s fit: %s;nuis. par 1;#mu_{bkg}", sb_or_b_nice, ml.title().c_str()),
                          nuis_scan[1].n, nuis_scan[1].min, nuis_scan[1].max,
                          mu_scan[1].n, mu_scan[1].min, mu_scan[1].max
                          );

      for (int i0 = 1; i0 <= nuis_scan[1].n; ++i0) {
        const double nuispar1 = nuis_scan[1].v(i0);
        for (int i1 = 1; i1 <= mu_scan[1].n; ++i1) {
          const double mu_bkg = mu_scan[1].v(i1);
          h4->SetBinContent(i0, i1, fit::twolnL(ml.mu_sig, mu_bkg, ml.nuis0, nuispar1));
        }
      }

      TH2F* h5 = new TH2F(TString::Format("h_likelihood_%s%s_scan_musig_nuis0", ex_.Data(), sb_or_b),
                          TString::Format("Best %s fit: %s;nuis. par 0;#mu_{sig}", sb_or_b_nice, ml.title().c_str()),
                          nuis_scan[0].n, nuis_scan[0].min, nuis_scan[0].max,
                          mu_scan[0].n, mu_scan[0].min, mu_scan[0].max
                          );

      for (int i0 = 1; i0 <= nuis_scan[0].n; ++i0) {
        const double nuispar0 = nuis_scan[0].v(i0);
        for (int i1 = 1; i1 <= mu_scan[0].n; ++i1) {
          const double mu_sig = mu_scan[0].v(i1);
          h5->SetBinContent(i0, i1, fit::twolnL(mu_sig, ml.mu_bkg, nuispar0, ml.nuis1));
        }
      }

      TH2F* h6 = new TH2F(TString::Format("h_likelihood_%s%s_scan_musig_nuis1", ex_.Data(), sb_or_b),
                          TString::Format("Best %s fit: %s;nuis. par 1;#mu_{sig}", sb_or_b_nice, ml.title().c_str()),
                          nuis_scan[1].n, nuis_scan[1].min, nuis_scan[1].max,
                          mu_scan[0].n, mu_scan[0].min, mu_scan[0].max
                          );

      for (int i0 = 1; i0 <= nuis_scan[1].n; ++i0) {
        const double nuispar1 = nuis_scan[1].v(i0);
        for (int i1 = 1; i1 <= mu_scan[0].n; ++i1) {
          const double mu_sig = mu_scan[0].v(i1);
          h6->SetBinContent(i0, i1, fit::twolnL(mu_sig, ml.mu_bkg, ml.nuis0, nuispar1));
        }
      }

      TH1F* h7 = new TH1F(TString::Format("h_likelihood_%s%s_scan_mubkg", ex_.Data(), sb_or_b),
                          TString::Format("Best %s fit: %s;#mu_{bkg};twolnL", sb_or_b_nice, ml.title().c_str()),
                          mu_scan[1].n, mu_scan[1].min, mu_scan[1].max
                          );

      for (int i0 = 1; i0 <= mu_scan[1].n; ++i0) {
        const double mu_bkg = mu_scan[1].v(i0);
        h7->SetBinContent(i0, fit::twolnL(ml.mu_sig, mu_bkg, ml.nuis0, ml.nuis1));
      }

      TH1F* h8 = new TH1F(TString::Format("h_likelihood_%s%s_scan_musig", ex_.Data(), sb_or_b),
                          TString::Format("Best %s fit: %s;#mu_{sig};twolnL", sb_or_b_nice, ml.title().c_str()),
                          mu_scan[0].n, mu_scan[0].min, mu_scan[0].max
                          );

      for (int i0 = 1; i0 <= mu_scan[0].n; ++i0) {
        const double mu_sig = mu_scan[0].v(i0);
        h8->SetBinContent(i0, fit::twolnL(mu_sig, ml.mu_bkg, ml.nuis0, ml.nuis1));
      }

      TH1F* h9 = new TH1F(TString::Format("h_likelihood_%s%s_scan_nuis0", ex_.Data(), sb_or_b),
                          TString::Format("Best %s fit: %s;nuis. par 0;twolnL", sb_or_b_nice, ml.title().c_str()),
                          nuis_scan[0].n, nuis_scan[0].min, nuis_scan[0].max
                          );

      for (int i0 = 1; i0 <= nuis_scan[0].n; ++i0) {
        const double nuispar0 = nuis_scan[0].v(i0);
        h9->SetBinContent(i0, fit::twolnL(ml.mu_sig, ml.mu_bkg, nuispar0, ml.nuis1));
      }

      TH1F* h10 = new TH1F(TString::Format("h_likelihood_%s%s_scan_nuis1", ex_.Data(), sb_or_b),
                          TString::Format("Best %s fit: %s;nuis. par 1;twolnL", sb_or_b_nice, ml.title().c_str()),
                          nuis_scan[1].n, nuis_scan[1].min, nuis_scan[1].max
                          );

      for (int i0 = 1; i0 <= nuis_scan[1].n; ++i0) {
        const double nuispar1 = nuis_scan[1].v(i0);
        h10->SetBinContent(i0, fit::twolnL(ml.mu_sig, ml.mu_bkg, ml.nuis0, nuispar1));
      }

      printf("\n");
    }
  }

  TH1D* Fitter::make_h_bkg(const char* n, const std::vector<double>& nuis_pars, const std::vector<double>& A_bkg) {
    if (print_level > 0) printf("make_h_bkg: %s  nuispars %f %f  A_bkg size %lu\n", n, nuis_pars[0], nuis_pars[1], A_bkg.size());
    TH1D* h = (TH1D*)fit::interp->get_Q(nuis_pars)->h->Clone(n);
    if (A_bkg.size()) {
      if (print_level > 0) printf("read A_bkg directly\n");
      for (int ibin = 1; ibin <= fit::n_bins; ++ibin) {
        if (print_level > 0) printf("%i %f\n", ibin, A_bkg[ibin]);
        h->SetBinContent(ibin, A_bkg[ibin]);
      }
    }
    else {
      std::vector<double> a(fit::n_bins+2, 0.);
      fit::interp->interpolate(std::vector<double>(), &a);
      if (print_level > 0) printf("interpolate from nuispars\n");
      for (int ibin = 0; ibin <= fit::n_bins+1; ++ibin) {
        if (print_level > 0) printf("%i %f\n", ibin, a[ibin]);
        h->SetBinContent(ibin, a[ibin]);
      }
    }
    return h;
  }

  void Fitter::scan_template_chi2(const test_stat_t& t) {
    TCanvas* c_scan_templates = new TCanvas("c_scan_templates");

    std::vector<TH1D*> hs;

    const int n_data = fit::h_data_real->Integral();
    TH1D* h_data_shortened = Template::shorten_hist(fit::h_data_real, false);
    hs.push_back(h_data_shortened);

    TGraphAsymmErrors* tgae_data_shortened = jmt::poisson_intervalize(h_data_shortened);
    tgae_data_shortened->SetTitle(";d_{VV} (cm);events");
    tgae_data_shortened->GetYaxis()->SetTitleOffset(1.2);
    tgae_data_shortened->SetLineWidth(2);
    tgae_data_shortened->SetMarkerStyle(20);
    tgae_data_shortened->SetMarkerSize(1);
    tgae_data_shortened->Draw("AP");

    TH1D* h_bkg_fit = make_h_bkg("h_bkg_fit", t.h0.nuis_pars(), std::vector<double>());
    h_bkg_fit->SetDirectory(0);
    TH1D* h_bkg_fit_shortened = Template::shorten_hist(h_bkg_fit, false);
    hs.push_back(h_bkg_fit);
    hs.push_back(h_bkg_fit_shortened);
    h_bkg_fit_shortened->Scale(n_data / h_bkg_fit_shortened->Integral());
    h_bkg_fit_shortened->SetLineWidth(2);
    h_bkg_fit_shortened->SetLineColor(kBlue);
    h_bkg_fit_shortened->Draw("same e");

    TH1D* h_bkg_fit_bb = make_h_bkg("h_bkg_fit", t.h0.nuis_pars(), t.h0.A_bkg);
    h_bkg_fit_bb->SetDirectory(0);
    TH1D* h_bkg_fit_bb_shortened = Template::shorten_hist(h_bkg_fit_bb, false);
    hs.push_back(h_bkg_fit_bb);
    hs.push_back(h_bkg_fit_bb_shortened);
    h_bkg_fit_bb_shortened->Scale(n_data / h_bkg_fit_bb_shortened->Integral());
    h_bkg_fit_bb_shortened->SetLineWidth(2);
    h_bkg_fit_bb_shortened->SetLineColor(9);
    h_bkg_fit_bb_shortened->Draw("same e");

    printf("bin contents:\n");
    printf("%6s | %6s | prediction from nu0 = %.4f, nu1 = %.4f\n", "ibin", "n_i", t.h0.nuis_pars()[0], t.h0.nuis_pars()[1]);
    for (int ibin = 1; ibin <= fit::n_bins; ++ibin) {
      const double estat = h_bkg_fit_shortened->GetBinError(ibin);
      const double esyst = fit::eta_bkg[ibin];
      printf("%6i | %6.1f | %7.3f +- %7.3f (stat) +- %7.3f (syst) (+- %7.3f tot)\n", ibin, fit::h_data_real->GetBinContent(ibin), h_bkg_fit_shortened->GetBinContent(ibin), estat, esyst, sqrt(estat*estat + esyst*esyst));
    }

    const int Nbest = 3;
    std::vector<double> best_chi2(Nbest, 1e99);
    std::vector<Template*> best_template(Nbest, (Template*)0);

    for (Template* tmp : *bkg_templates) {
      assert(fabs(tmp->h->Integral() - 1) < 1e-4);

      std::vector<double> chi2(Nbest, 0.);

      bool in_last_3 = true;

      for (int ibin = 4; ibin <= fit::n_bins; ++ibin) {
        const double cd = h_data_shortened->GetBinContent(ibin);
        const double c = tmp->h->GetBinContent(ibin);
        const int c_orig = int(pow(c / tmp->h->GetBinError(ibin), 2));
        const double w = c / c_orig * n_data;
        const double alphao2 = 2.7e-3; // 3sig
        jmt::interval i = jmt::garwood_poisson(c_orig, alphao2, alphao2);
        i.lower *= w;
        i.upper *= w;

        if (!i.in(cd))
          in_last_3 = false;
      }

      for (int ibin = 1; ibin <= fit::n_bins; ++ibin) {
        const double cd = h_data_shortened->GetBinContent(ibin);
        const double c  = tmp->h->GetBinContent(ibin);
        const double dchi2 = c > 0 ? pow(cd - c * n_data, 2) / (c * n_data) : 0.;

        for (int ibest = 0; ibest < Nbest; ++ibest) {
          bool use = true;
          if (ibest == 1)
            use = ibin >= 4;
          else if (ibest == 2)
            use = ibin <= 3;

          if (use)
            chi2[ibest] += dchi2;
        }
      }

      for (int ibest = 0; ibest < Nbest; ++ibest) {
        if (ibest == 2 && !in_last_3)
          continue;
        if (chi2[ibest] < best_chi2[ibest]) {
          best_chi2[ibest] = chi2[ibest];
          best_template[ibest] = tmp;
        }
      }
    }

    for (int ibest = 0; ibest < Nbest; ++ibest)
      printf("best scan: chi2=%f template=%s\n", best_chi2[ibest], best_template[ibest]->title().c_str());

    const int colors[Nbest] = { 2, 8, 6 };
    const char* legs[Nbest] = { "all bins", "last three bins", "1st three, touching last three" };
    TLegend* leg = new TLegend(0.384,0.606,0.856,0.853);
    leg->SetFillColor(kWhite);

    leg->AddEntry(tgae_data_shortened, "data", "LPE");
    leg->AddEntry(h_bkg_fit_shortened, "best b-only fit", "LPE");
    leg->AddEntry(h_bkg_fit_bb_shortened, "best b-only fit w/BB", "LPE");

    for (int ibest = 0; ibest < Nbest; ++ibest) {
      Template* tmp = best_template[ibest];
      TH1D* h = Template::shorten_hist(tmp->h, false);
      hs.push_back(h);
      h->Scale(n_data / h->Integral());
      h->SetLineWidth(2);
      h->SetLineColor(colors[ibest]);
      leg->AddEntry(h, TString::Format("#nu = (%i #mum, %i #mum): best #chi^{2}(%s)", int(tmp->par(0)*10000), int(tmp->par(1)*10000), legs[ibest]), "LPE");
      h->Draw("same e");
    }

    leg->Draw();

    c_scan_templates->Write();
    delete c_scan_templates;
    delete tgae_data_shortened;
    delete leg;
    for (TH1D* h : hs)
      delete h;
    hs.clear();
  }

  Fitter::fit_stat_t Fitter::draw_fit(const test_stat_t& t) {
    fit_stat_t ret;

    for (int div = 0; div <= 1; ++div) {
      for (int bb = 1; bb >= 0; --bb) {
        for (int sb = 1; sb >= 0; --sb) {
          const char* bb_or_no = bb ? "bb" : "nobb";
          const char* bb_or_no_nice = bb ? "w/ BB" : "w/o BB";
          const char* div_or_no = div ? "div" : "nodiv";
          const char* div_or_no_nice = div ? "/bin width" : "";
          const char* sb_or_b = sb ? "sb" : "b";
          const char* sb_or_b_nice = sb ? "sig + bkg" : "b only";
          const min_lik_t& ml = sb ? t.h1 : t.h0;
          TCanvas* c = new TCanvas(TString::Format("c_%s_fit_%s_%s", sb_or_b, bb_or_no, div_or_no));

          if (div == 0) {
            TH1D* h_phi = (TH1D*)fit::interp->get_Q(ml.nuis_pars())->h_phi->Clone(TString::Format("h_phi_%s_fit_%s_%s", sb_or_b, bb_or_no, div_or_no));
            h_phi->SetLineWidth(2);
          }

          TH1D* h_bkg_fit = make_h_bkg(TString::Format("h_bkg_%s_fit_%s_%s", sb_or_b, bb_or_no, div_or_no), ml.nuis_pars(), bb ? ml.A_bkg : std::vector<double>());
          TH1D* h_sig_fit  = (TH1D*)fit::h_sig ->Clone(TString::Format("h_sig_%s_fit_%s_%s",  sb_or_b, bb_or_no, div_or_no));
          TH1D* h_data_fit = (TH1D*)fit::h_data->Clone(TString::Format("h_data_%s_fit_%s_%s", sb_or_b, bb_or_no, div_or_no));

          for (TH1D** ph : {&h_bkg_fit, &h_sig_fit, &h_data_fit})
            *ph = Template::shorten_hist(*ph, true);

          for (TH1D* h : {h_bkg_fit, h_sig_fit, h_data_fit}) {
            if (!save_plots) h->SetDirectory(0);
            h->SetLineWidth(2);
            if (div)
              jmt::divide_by_bin_width(h);
          }

          h_sig_fit->SetLineColor(kRed);
          h_sig_fit->SetFillColor(kRed);
          h_sig_fit->SetFillStyle(3004);
          h_bkg_fit->SetLineColor(kBlue);
          h_bkg_fit->SetFillColor(kBlue);
          h_bkg_fit->SetFillStyle(3005);

          h_sig_fit->Scale(ml.mu_sig);
          h_bkg_fit->Scale(ml.mu_bkg);

          TH1D* h_sum_fit = (TH1D*)h_sig_fit->Clone(TString::Format("h_sum_%s_fit_%s_%s_shortened", sb_or_b, bb_or_no, div_or_no));
          if (!save_plots) h_sum_fit->SetDirectory(0);
          h_sum_fit->SetLineColor(kMagenta);
          h_sum_fit->Add(h_bkg_fit);
          for (TH1D* h : {h_sum_fit, h_data_fit})
            h->SetTitle(TString::Format("best %s fit %s: %s;svdist2d (cm);events%s", sb_or_b_nice, bb_or_no_nice, ml.title().c_str(), div_or_no_nice));

          for (TH1D* h : {h_sum_fit, h_data_fit, h_sig_fit, h_bkg_fit})
            h->SetStats(0);

          if (h_data_fit->GetMaximum() > h_sum_fit->GetMaximum()) {
            h_data_fit->Draw("e");
            h_sum_fit->Draw("hist same");
          }
          else {
            h_sum_fit->Draw("hist");
            h_data_fit->Draw("same e");
          }
          h_sig_fit->Draw("same hist");
          h_bkg_fit->Draw("same hist");
          if (save_plots) c->Write();
          delete c;

          for (TH1D* h : {h_sum_fit, h_data_fit, h_sig_fit, h_bkg_fit})
            h->SetStats(1);

          if (!div) {
            TH1D* h_sum_cumul  = (TH1D*)h_sum_fit ->Clone(TString::Format("h_sum_%s_cumul_%s_%s",  sb_or_b, bb_or_no, div_or_no));
            TH1D* h_data_cumul = (TH1D*)h_data_fit->Clone(TString::Format("h_data_%s_cumul_%s_%s", sb_or_b, bb_or_no, div_or_no));
            h_sum_cumul->Scale(1/h_sum_cumul->Integral());
            h_data_cumul->Scale(1/h_data_cumul->Integral());

            for (TH1D* h : {h_sum_cumul, h_data_cumul}) {
              if (!save_plots) h->SetDirectory(0);
              jmt::cumulate(h, false);
            }

            TCanvas* c2 = new TCanvas(TString::Format("c_%s_cumul_%s_%s", sb_or_b, bb_or_no, div_or_no));
            for (TH1D* h : {h_sum_cumul, h_data_cumul})
              h->SetStats(0);
            h_sum_cumul->Draw();
            h_data_cumul->Draw("same e");
            if (save_plots) c2->Write();
            delete c2;
            for (TH1D* h : {h_sum_cumul, h_data_cumul})
              h->SetStats(1);

            ret.chi2 = 0;
            ret.ndof = h_data_fit->GetNbinsX() - (sb ? 2 : 1);
            if (!fix_nuis0)
              ret.ndof -= 1;
            if (!fix_nuis1)
              ret.ndof -= 1;
            ret.ks = 0;
            for (int ibin = 1; ibin <= h_data_fit->GetNbinsX(); ++ibin) {
              if (h_sum_fit->GetBinContent(ibin) > 0)
                ret.chi2 += pow(h_data_fit->GetBinContent(ibin) - h_sum_fit->GetBinContent(ibin), 2) / h_sum_fit->GetBinContent(ibin);

              double ksd = fabs(h_sum_cumul->GetBinContent(ibin) - h_data_cumul->GetBinContent(ibin));
              if (ksd > ret.ks)
                ret.ks = ksd;
            }
            ret.prob = TMath::Prob(ret.chi2, ret.ndof);

            if (!save_plots) {
              delete h_sum_cumul;
              delete h_data_cumul;
            }
          }

          if (!save_plots) {
            delete h_bkg_fit;
            delete h_sig_fit;
            delete h_data_fit;
            delete h_sum_fit;
          }
        }
      }
    }

    return ret;
  }

  Fitter::min_lik_t Fitter::min_likelihood(double mu_sig_start, bool fix_mu_sig) {
    fit::globals_ok();

    min_lik_t ret;

    TMinuit* m = new TMinuit(4);
    m->SetPrintLevel(print_level);
    m->SetFCN(fit::minfcn);
    double three = 3;
    int thisseed = 20000 + seed + toy;
    m->mnrn15(three, thisseed);
    int ierr;
    double mu_sig_lo = 0, mu_sig_hi = 500;
    if (mu_sig_start > 0)
      mu_sig_hi = mu_sig_start;
    if (allow_negative_mu_sig)
      mu_sig_lo = -500;
    m->mnparm(0, "mu_sig", (mu_sig_start > 0 ? mu_sig_start : 0), 0.5, mu_sig_lo, mu_sig_hi, ierr);
    m->mnparm(1, "mu_bkg", fit::a_data_integ, 0.5, 0, 500, ierr);

    const size_t npars = bkg_templates->at(0)->npars();
    std::vector<double> mins(npars,  1e99);
    std::vector<double> maxs(npars, -1e99);
    for (Template* t : *bkg_templates)
      for (size_t ipar = 0; ipar < npars; ++ipar) {
        double t_par = t->par(ipar);
        if (t_par > maxs[ipar])
          maxs[ipar] = t_par;
        if (t_par < mins[ipar])
          mins[ipar] = t_par;
      }

    static const char* nuis_par_names[2] = { "nuis0", "nuis1" };
    for (size_t ipar = 0; ipar < npars; ++ipar) {
      //printf("ipar %lu min %f max %f\n", ipar, mins[ipar],maxs[ipar]);
      const double start = ipar == 0 ? start_nuis0 : start_nuis1;
      m->mnparm(2+ipar, nuis_par_names[ipar], start, 0.001, mins[ipar], maxs[ipar], ierr);
    }

    if (fix_mu_sig)
      m->FixParameter(0);

    if (fix_nuis0)
      m->FixParameter(2);

    if (fix_nuis1)
      m->FixParameter(3);

    m->Command("SET STRATEGY 2");
    if (print_level > 0)
      m->Command("SET DEBUG -1");

    if (run_mnseek) {
      if (print_level > 0)
        printf("call mnseek\n");
      double seek_arg[2] = {100, 100};
      m->mnexcm("SEE", seek_arg, 2, ierr);
    }

    if (print_level > 0)
      printf("call migrad\n");
    m->Migrad();

    m->GetParameter(0, ret.mu_sig, ret.err_mu_sig);
    m->GetParameter(1, ret.mu_bkg, ret.err_mu_bkg);
    m->GetParameter(2, ret.nuis0, ret.err_nuis0);
    m->GetParameter(3, ret.nuis1, ret.err_nuis1);

    if (run_minos) {
      if (print_level > 0)
        printf("call minos\n");
      m->mnmnos();
    }

    double eparab, gcc;
    m->mnerrs(0, ret.eplus_mu_sig, ret.eminus_mu_sig, eparab, gcc);
    m->mnerrs(1, ret.eplus_mu_bkg, ret.eminus_mu_bkg, eparab, gcc);
    m->mnerrs(2, ret.eplus_nuis0, ret.eminus_nuis0, eparab, gcc);
    m->mnerrs(3, ret.eplus_nuis1, ret.eminus_nuis1, eparab, gcc);

    // remove limits before redoing covariance matrix calculation and minos below
    m->mnparm(0, "mu_sig", ret.mu_sig, ret.err_mu_sig, 0,0, ierr);
    m->mnparm(1, "mu_bkg", ret.mu_bkg, ret.err_mu_bkg, 0,0, ierr);
    double nuis[2] = {ret.nuis0, ret.nuis1};
    double err_nuis[2] = {ret.err_nuis0, ret.err_nuis1};
    for (size_t ipar = 0; ipar < npars; ++ipar)
      m->mnparm(2+ipar, nuis_par_names[ipar], nuis[ipar], err_nuis[ipar], 0,0, ierr);

    m->mnhess();

    TMatrixDSym cov(npars+2);
    m->mnemat(cov.GetMatrixArray(), npars+2);
    if (fix_nuis0 || fix_nuis1)
      ret.correlation_nuis = -999;
    else {
      if (fix_mu_sig)
        ret.correlation_nuis = cov(1,2)/sqrt(cov(1,1) * cov(2,2));
      else
        ret.correlation_nuis = cov(2,3)/sqrt(cov(2,2) * cov(3,3));
    }

    if (print_level > 0) {
      printf("external covariance matrix:\n");
      for (int ipar = 0; ipar < int(npars+2); ++ipar) {
        for (int jpar = 0; jpar < int(npars+2); ++jpar) {
          if (jpar < ipar)
            printf("%12s", "");
          else
            printf("%12.4e ", cov(ipar,jpar));
        }
        printf("\n");
      }
      if (fix_mu_sig) printf("nuis correlation coeff: %f\n", ret.correlation_nuis);
    }

    double fmin, fedm, errdef;
    int npari, nparx, istat;
    m->mnstat(fmin, fedm, errdef, npari, nparx, istat);
    ret.maxtwolnL = -fmin;
    m->GetParameter(0, ret.mu_sig, ret.err_mu_sig);
    m->GetParameter(1, ret.mu_bkg, ret.err_mu_bkg);
    m->GetParameter(2, ret.nuis0, ret.err_nuis0);
    m->GetParameter(3, ret.nuis1, ret.err_nuis1);
    ret.ok = istat == 3;
    ret.istat = istat;

    if (print_level > 0)
      printf("calling twolnL at last minimum so A_sig/bkg are updated\n");
    fit::twolnL(ret.mu_sig, ret.mu_bkg, ret.nuis0, ret.nuis1);

    ret.A_sig.assign(fit::n_bins+2, -1);
    ret.A_bkg.assign(fit::n_bins+2, -1);
    ret.A_sig_rel.assign(fit::n_bins+2, -1);
    ret.A_bkg_rel.assign(fit::n_bins+2, -1);
    ret.A_sig_sum = 0.;
    ret.A_bkg_sum = 0.;
    for (int i = 1; i <= fit::n_bins; ++i) {
      ret.A_sig_sum += (ret.A_sig[i] = fit::A_sig[i]);
      ret.A_bkg_sum += (ret.A_bkg[i] = fit::A_bkg[i]);
      ret.A_sig_rel[i] = fit::A_sig[i] / fit::a_sig[i];
      ret.A_bkg_rel[i] = fit::A_bkg[i] / fit::a_bkg[i];
    }

    //printf("min_likelihood: %s  istat: %i   maxtwolnL: %e   mu_sig: %f +- %f  mu_bkg: %f +- %f\n", bkg_template->title().c_str(), istat, maxtwolnL, mu_sig, err_mu_sig, mu_bkg, err_mu_bkg);
    delete m;
    return ret;
  }

  Fitter::test_stat_t Fitter::calc_test_stat(double fix_mu_sig_val) {
    test_stat_t t;
    if (print_level > 0)
      printf("calc_test_stat: H1\n");
    t.h1 = min_likelihood(fix_mu_sig_val, false);
    if (print_level > 0)
      printf("calc_test_stat: H0 (mu_sig fixed to %f)\n", fix_mu_sig_val);
    t.h0 = min_likelihood(fix_mu_sig_val, true);
    t.t = t.h1.maxtwolnL - t.h0.maxtwolnL;
    return t;
  }

  void Fitter::make_toy_data(int i_toy_signif, int i_toy_limit, int i_toy_expect, int n_sig, int n_bkg, TH1D* h_bkg) {
    delete fit::h_data_toy_sig;
    delete fit::h_data_toy_bkg;
    delete fit::h_data_toy;

    char s[128], s2[128];
    if (i_toy_signif < 0 && i_toy_limit < 0 && i_toy_expect < 0)
      snprintf(s, 128, "h_%%s_seed%02i_toy%02i", seed, toy);
    else if (i_toy_signif >= 0)
      snprintf(s, 128, "h_%%s_seed%02i_toy%02i_signif%02i", seed, toy, i_toy_signif);
    else if (i_toy_limit >= 0)
      snprintf(s, 128, "h_%%s_seed%02i_toy%02i_limit%02i", seed, toy, i_toy_limit);
    else if (i_toy_expect >= 0)
      snprintf(s, 128, "h_%%s_seed%02i_toy%02i_expect%02i", seed, toy, i_toy_expect);

    snprintf(s2, 128, s, "data_toy_sig"); fit::h_data_toy_sig = Template::hist_with_binning(s2, "");
    snprintf(s2, 128, s, "data_toy_bkg"); fit::h_data_toy_bkg = Template::hist_with_binning(s2, "");
    snprintf(s2, 128, s, "data_toy");     fit::h_data_toy     = Template::hist_with_binning(s2, "");

    for (TH1D* h : {fit::h_data_toy_sig, fit::h_data_toy_bkg, fit::h_data_toy}) {
      h->SetLineWidth(2);
      h->SetDirectory(0);
    }

    TH1D* h_sig_use = fit::h_sig;
    TH1D* h_bkg_use = h_bkg;

    if (fluctuate_toys_shapes) {
      h_sig_use = (TH1D*)fit::h_sig->Clone("h_sig_use");
      h_bkg_use = (TH1D*)h_bkg->Clone("h_bkg_use");
      h_sig_use->SetDirectory(0);
      h_bkg_use->SetDirectory(0);

      double ss_sum = 0;
      double bs_sum = 0;
      std::vector<double> ss(fit::n_bins+2, 0.);
      std::vector<double> bs(fit::n_bins+2, 0.);
      for (int i = 1; i <= fit::n_bins; ++i) {
        const double sc = fit::h_sig->GetBinContent(i);
        const double sn = rand->Poisson(sc * fit::n_sig_orig);
        ss_sum += sn;
        ss[i] = sn;

        const double bc  = h_bkg->GetBinContent(i);
        const double bce = fit::eta_bkg[i] / n_bkg;
        double bn = rand->Gaus(bc, bce);
        if (bn < 0)
          bn = 0;
        bs_sum += bn;
        bs[i] = bn;
      }

      for (int i = 1; i <= fit::n_bins; ++i) {
        h_sig_use->SetBinContent(i, ss[i]/ss_sum);
        h_bkg_use->SetBinContent(i, bs[i]/bs_sum);
      }
    }

    fit::h_data_toy_sig->FillRandom(h_sig_use, n_sig);
    fit::h_data_toy_bkg->FillRandom(h_bkg_use, n_bkg);

    if (fluctuate_toys_shapes) {
      delete h_sig_use;
      delete h_bkg_use;
    }

    fit::h_data_toy->Add(fit::h_data_toy_sig);
    fit::h_data_toy->Add(fit::h_data_toy_bkg);
    fit::set_data_no_check(fit::h_data_toy);

    if (print_level > 1) {
      printf("make_toy_data: i_signif: %i i_limit: %i n_sig: %i n_bkg: %i\n", i_toy_signif, i_toy_limit, n_sig, n_bkg);
      printf("h_sig: ");
      for (int i = 0; i <= fit::n_bins+1; ++i)
        printf("%10.6f ", fit::h_sig->GetBinContent(i));
      printf("\nh_bkg: ");
      for (int i = 0; i <= fit::n_bins+1; ++i)
        printf("%10.6f ", h_bkg->GetBinContent(i));
      printf("\ntoy_sig: ");
      for (int i = 0; i <= fit::n_bins+1; ++i)
        printf("%10.6f ", fit::h_data_toy_sig->GetBinContent(i));
      printf("\ntoy_bkg: ");
      for (int i = 0; i <= fit::n_bins+1; ++i)
        printf("%10.6f ", fit::h_data_toy_bkg->GetBinContent(i));
      printf("\ntoy: ");
      for (int i = 0; i <= fit::n_bins+1; ++i)
        printf("%10.6f ", fit::h_data_toy->GetBinContent(i));
      printf("\n");
    }
  }

  void Fitter::fit(int toy_, Templater* bkg_templater, TH1D* sig_template, const VertexPairs& v2v, const std::vector<double>& true_pars_) {
    toy = toy_;
    true_pars = true_pars_;

    dtoy = dout->mkdir(TString::Format("seed%02i_toy%02i", seed, toy));

    ////

    dtoy->mkdir("finalized_templates")->cd();

    if (!fit::extra_prints && print_level > 1)
      fit::extra_prints = 1;

    fit::n_sig_orig = sig_template->Integral(1,100000);
    printf("n_sig_orig: %.1f\n", fit::n_sig_orig);
    fit::set_sig(Template::finalize_template(sig_template));
    fit::calc_lnL_offset();

    if (bkg_gaussians_all)
      fit::eta_bkg = { -1, 0.09, 0.15, 0.19, -1 };
    else if (bkg_gaussians) 
      fit::eta_bkg = { -1, 0.09, 0.15, 0.19, -1 };
      //fit::eta_bkg = { -1, 1, 3.9, 3.8, 1.4, 0.1, 0.1, -1 };
      //fit::eta_bkg = { -1, 1, 1, 1, 3, 1, 1, -1 };
    else {
      fit::eta_bkg.assign(fit::n_bins+2, 1e-3);
      fit::eta_bkg.front() = -1;
      fit::eta_bkg.back() = -1;
    }

    //fit::eta_bkg = { -1, 1, 1, 1, 3, 1, 1, -1 };

    if (int(fit::eta_bkg.size()) != fit::n_bins+2)
      jmt::vthrow("eta_bkg wrong size");

    fit::barlow_beeston = barlow_beeston;
    fit::bend_bkg = bend_bkg;

    bkg_templates = bkg_templater->get_templates();
    fit::interp = new TemplateInterpolator(bkg_templates, fit::n_bins, bkg_templater->par_info(), fit::a_bkg);

    //fit::a_bkg = {0.000000,0.020406,0.747983,0.218452,0.010790,0.002105,0.000263,0.000000};
    //fit::interp->interpolate(0.03, 0.01);
    //printf("a_bkg after one interp\n");
    //for (double a : fit::a_bkg)
    //  printf("%f ", a);
    //printf("\n");

    std::map<int, int> template_index_deltas;
    bool any_nan = false;
    for (int i = 0, ie = bkg_templates->size(); i < ie; ++i) {
      //printf("bkg template #%5i: %s\n", i, bkg_templates->at(i)->title().c_str());
      const TH1D* ht = bkg_templates->at(i)->h;
      for (int ibin = 0; ibin <= ht->GetNbinsX()+1; ++ibin)
        if (TMath::IsNaN(ht->GetBinContent(ibin)) || TMath::IsNaN(ht->GetBinError(ibin))) {
          printf("NaN in template %i (%s) bin %i\n", i, bkg_templates->at(i)->title().c_str(), ibin);
          any_nan = true;
        }
      const int delta = abs(i - fit::interp->i_Q(bkg_templates->at(i)->pars));
      template_index_deltas[delta] += 1;
    }
    if (any_nan)
      jmt::vthrow("something wrong with templates");

    TH1D* h_data_temp = Template::hist_with_binning("h_data", TString::Format("toy %i", toy));
    for (const VertexPair& p : v2v)
      h_data_temp->Fill(p.d2d());
    for (int i = 0; i < inject_in_last_bin; ++i)
      h_data_temp->Fill(2);
    fit::h_data_real = Template::finalize_binning(h_data_temp);
    if (0) {
      printf("duhing\n");
      std::vector<double> duh = { 7, 215, 49, 0, 0, 0 };
      assert(int(duh.size()) == fit::n_bins);
      for (int i = 0; i < fit::n_bins; ++i)
        fit::h_data_real->SetBinContent(i+1, duh[i]);
    }
    fit::set_data_real();
    const int n_data = fit::h_data_real->Integral();
    printf("Fitter: data histogram: ");
    for (int i = 1; i <= fit::n_bins; ++i)
      printf("%.1f ", fit::h_data_real->GetBinContent(i));
    printf("  sum: %.1f  n_data: %i\n", fit::h_data_real->Integral(), n_data);
    delete h_data_temp;

    ////

    dtoy->mkdir("fit_results")->cd();

    if (save_plots) {
      for (int i = 1; i <= fit::n_bins; ++i) {
        const int nn(0.8*(n_data + sqrt(n_data) * 3));
        h_signif_toy.push_back(new TH1F(TString::Format("h_signif_toys_bin_%i", i), "", nn, 0, nn));
        h_limit_toy.push_back(new TH1F(TString::Format("h_limit_toys_bin_%i", i), "", nn, 0, nn));
      }
    }

    printf("Fitter: toy: %i  n_sig_true: %.1f  n_bkg_true: %.1f  true_pars:", toy, true_pars[0], true_pars[1]);
    for (double tp : true_pars)
      printf(" %f", tp);
    printf("\n");
    printf("  # bkg templates: %lu  template_index_deltas seen:\n", bkg_templates->size());
    for (const auto& p : template_index_deltas)
      printf("%i: %i times\n", p.first, p.second);

    TStopwatch tsw;
    t_obs_0 = calc_test_stat(0);
    printf("n_calls: %i time to fit: ", fit::n_calls); tsw.Print();
    t_obs_0.print("t_obs_0");

    if (print_level > 0) {
      const int save_extra_prints = fit::extra_prints;
      fit::extra_prints = 1;
      printf("twolnL_h1:\n");
      const double twolnL_h1 = fit::twolnL(t_obs_0.h1.mu_sig, t_obs_0.h1.mu_bkg, t_obs_0.h1.nuis_pars()[0], t_obs_0.h1.nuis_pars()[1]);
      printf("twolnL_h1 = %f\n", twolnL_h1);
      printf("twolnL_h0:\n");
      const double twolnL_h0 = fit::twolnL(t_obs_0.h0.mu_sig, t_obs_0.h0.mu_bkg, t_obs_0.h0.nuis_pars()[0], t_obs_0.h0.nuis_pars()[1]);
      printf("twolnL_h0 = %f\n", twolnL_h0);
      if (toy >= 0) {
        printf("twolnL_true(mu_sig=%f, mu_bkg=%f, nuis0=%f, nuis1=%f:\n", true_pars[0], true_pars[1], 0.028, 0.01);
        const double twolnL_true = fit::twolnL(true_pars[0], true_pars[1], 0.028, 0.01);
        printf("twolnL_true = %f\n", twolnL_true);
      }
      fit::extra_prints = save_extra_prints;
    }

    TH1D* h_bkg_obs_0 = make_h_bkg("h_bkg_obs_0", t_obs_0.h0.nuis_pars(), t_obs_0.h0.A_bkg);

    pval_signif = 1;
    pval_cls = 1;
    double pval_cls_err = 0;

    const int save_print_level = print_level;
    const int save_extra_prints = fit::extra_prints;
    print_level = -1;
    fit::extra_prints = 0;

    //    if (save_plots) draw_likelihood(t_obs_0);
    //scan_template_chi2(t_obs_0);
    fit_stat = draw_fit(t_obs_0);

    print_level = save_print_level;
    fit::extra_prints = save_extra_prints;

    if (!only_fit && do_signif) {
      fit::n_calls = 0;
      TStopwatch tsw_signif;

      printf("throwing %i significance toys:\n", n_toy_signif);
      jmt::ProgressBar pb_signif(50, n_toy_signif);
      if (!print_toys)
        pb_signif.start();

      int n_toy_signif_t_ge_obs = 0;

      for (int i_toy_signif = 0; i_toy_signif < n_toy_signif; ++i_toy_signif) {
        //fit::extra_prints = TemplateInterpolator::extra_prints = i_toy_signif == 91 || i_toy_signif == 90;
        
        const int n_sig_signif = 0;
        const int n_bkg_signif = rand->Poisson(n_data);
        make_toy_data(i_toy_signif, -1, -1, n_sig_signif, n_bkg_signif, h_bkg_obs_0);
        if (save_plots)
          for (int i = 1; i <= fit::n_bins; ++i)
            h_signif_toy[i-1]->Fill(fit::h_data->GetBinContent(i));
      
        const test_stat_t t = calc_test_stat(0);
        if (t.t >= t_obs_0.t)
          ++n_toy_signif_t_ge_obs;

        if (print_toys) {
          t.print("t_signif toy", i_toy_signif);
        }
        else
          ++pb_signif;

        if (save_toys) {
          jmt::vthrow("save signif toys not implemented");
        }
      }

      pval_signif = double(n_toy_signif_t_ge_obs) / n_toy_signif;
      printf("\npval_signif: %e\n", pval_signif); fflush(stdout);
      printf("n_calls: %i time for signif: ", fit::n_calls); tsw_signif.Print();
    }

    if (!only_fit && do_limit) {
      fit::n_calls = 0;
      TStopwatch tsw_limit;

      const double limit_alpha = 0.05;

      const double sig_limit_lo = sig_limit_start;
      const double sig_limit_hi = sig_limit_stop;
      const int n_sigma_away_lo = 6;
      const int n_sigma_away_hi = 5;
      double sig_limit_scan = sig_limit_lo;

      printf("scanning for %.1f%% upper limit, ", 100*(1-limit_alpha));
      if (i_limit_job < 0)
        printf("observed\n");
      else
        printf("expected (toy #%i)\n", i_limit_job);

      jmt::ProgressBar pb_limit(50, (sig_limit_hi - sig_limit_lo)/sig_limit_step);
      if (!print_toys)
        pb_limit.start();

      std::vector<double> bracket_sig_limit;
      std::vector<double> bracket_pval_limit;
      std::vector<double> bracket_pval_limit_err;
      int n_below = 0;

      TH1D* h_toy_expected = 0;
      if (i_limit_job >= 0) {
        for (int i_toy_expected = 0; i_toy_expected <= i_limit_job; ++i_toy_expected) {
          delete h_toy_expected;
          make_toy_data(-1, -1, i_limit_job, 0, rand->Poisson(n_data), h_bkg_obs_0);
          h_toy_expected = (TH1D*)fit::h_data_toy->Clone("h_toy_expected");
          h_toy_expected->SetDirectory(0);
          if (save_plots)
            for (int i = 1; i <= fit::n_bins; ++i)
              h_limit_toy[i-1]->Fill(fit::h_data_toy->GetBinContent(i));
          if (print_subtoys && i_toy_expected < i_limit_job) {
            printf("burning toy [ ");
            for (int i = 1; i <= fit::n_bins; ++i)
              printf("%i ", int(h_toy_expected->GetBinContent(i)));
            printf("]\n");
          }
        }

        printf("toy_expected [ ");
        for (int i = 1; i <= fit::n_bins; ++i)
          printf("%i ", int(h_toy_expected->GetBinContent(i)));
        printf("]\n");
      }

      if (0) {
        fit::set_data_no_check(h_toy_expected);
        printf("start t076\n");
        test_stat_t t076 = calc_test_stat(0.76);
        t076.print("0.76");
        printf("start t101\n");
        test_stat_t t101 = calc_test_stat(1.01);
        t101.print("1.01");

        fit::extra_prints=0;
        print_level=0;
        draw_likelihood(t076, "0p76");
        draw_likelihood(t101, "1p01");

        sig_limit_scan = 1e99;
      }

      if (do_cls) {
        fit::n_calls = 0;
        TStopwatch tsw_cls;

        if (i_limit_job < 0)
          fit::set_data_real(); 
        else
          fit::set_data_no_check(h_toy_expected);

        const test_stat_t t_obs_cls = calc_test_stat(0);
        t_obs_cls.print("t_obs_cls");

        printf("throwing %i toys for p_b for CLs:\n", n_toy_cls);
        jmt::ProgressBar pb_cls(50, n_toy_cls);
        if (!print_toys)
          pb_cls.start();

        int n_toy_cls_t_ge_obs = 0;
        for (int i_toy_cls = 0; i_toy_cls < n_toy_cls; ++i_toy_cls) {
          const int n_sig_cls = 0;
          const int n_bkg_cls = rand->Poisson(n_data);
          make_toy_data(i_toy_cls, -1, -1, n_sig_cls, n_bkg_cls, h_bkg_obs_0);

          const test_stat_t t = calc_test_stat(0);
          if (t.t >= t_obs_cls.t)
            ++n_toy_cls_t_ge_obs;

          if (print_toys) {
            if (print_subtoys) {
              printf("  cls toy %i nsig 0 nbkg %i n'data' %i [ ", i_toy_cls, n_bkg_cls, n_data);
              for (int i = 1; i <= fit::n_bins; ++i)
                printf("%i ", int(fit::h_data->GetBinContent(i)));
              printf("] ");
              t.print("t_cls", -1, "    ");
            }
            //t.print("t_cls toy", i_toy_cls);
          }
          else
            ++pb_cls;

          if (save_toys) {
            jmt::vthrow("save cls toys not implemented");
          }
        }

        assert(n_toy_cls_t_ge_obs > 5);

        const double T = 1./n_toy_cls;
        const double p_hat = 1 - double(n_toy_cls_t_ge_obs) / n_toy_cls;
        pval_cls = (p_hat + T/2)/(1 + T);
        pval_cls_err = sqrt(p_hat * (1 - p_hat) * T + T*T/4)/(1 + T);
        
        printf("\npval_cls: %e +- %e\n", pval_cls, pval_cls_err); fflush(stdout);
        printf("n_calls: %i time for cls: ", fit::n_calls); tsw_cls.Print();
        printf("\n");
      }

      while (sig_limit_scan < sig_limit_hi) {
        const double mu_sig_limit = sig_eff * sig_limit_scan;

        if (i_limit_job < 0)
          fit::set_data_real(); 
        else
          fit::set_data_no_check(h_toy_expected);

        const test_stat_t t_obs_limit_ = calc_test_stat(mu_sig_limit);

        if (print_toys) {
          printf("sig_limit: %f  mu_sig_limit: %f data: [ ", sig_limit_scan, mu_sig_limit);
          for (int i = 1; i <= fit::n_bins; ++i)
            printf("%i ", int(fit::h_data->GetBinContent(i)));
          printf("] ");
          t_obs_limit_.print("t_obs_limit");
        }
        else
          ++pb_limit;

        if (save_toys) {
          jmt::vthrow("save limit toys not implemented");
        }

        int n_toy_limit_t_ge_obs = 0;

        jmt::ProgressBar pb_limit_toys(50, n_toy_limit);
        if (print_toys && !print_subtoys)
          pb_limit_toys.start();

        for (int i_toy_limit = 0; i_toy_limit < n_toy_limit; ++i_toy_limit) {
          const double mu_sig_limit_toy = mu_sig_limit * (sig_eff_uncert > 0 ? jmt::lognormal(rand, 0, sig_eff_uncert) : 1);
          if (mu_sig_limit_toy >= n_data) {
            --i_toy_limit;
            continue;
          }
          const int n_sig_limit = rand->Poisson(mu_sig_limit_toy);
          const int n_bkg_limit = rand->Poisson(n_data - mu_sig_limit_toy);

          make_toy_data(-1, i_toy_limit, -1, n_sig_limit, n_bkg_limit, h_bkg_obs_0);
      
          const test_stat_t t = calc_test_stat(mu_sig_limit);
          if (t.t > t_obs_limit_.t)
            ++n_toy_limit_t_ge_obs;

          if (print_toys) {
            if (print_subtoys) {
              printf("  limit toy %i nsig %i nbkg %i n'data' %i [ ", i_toy_limit, n_sig_limit, n_bkg_limit, n_data);
              for (int i = 1; i <= fit::n_bins; ++i)
                printf("%i ", int(fit::h_data->GetBinContent(i)));
              printf("] ");
              t.print("t_limit", -1, "    ");
            }
            else
              ++pb_limit_toys;
          }

          if (save_toys) {
            jmt::vthrow("save toys for limits not implemented");
          }
        }
        if (print_toys)
          printf("\n");

        const double T = 1./n_toy_limit;
        const double p_hat = double(n_toy_limit_t_ge_obs) / n_toy_limit;
        const double pval_limit = (p_hat + T/2)/(1 + T) / pval_cls;
        const double pval_limit_err = sqrt((p_hat * (1 - p_hat) * T + T*T/4)/(1 + T) / pow(pval_cls, 2) + pow(pval_cls_err, 2));
        const double pval_limit_sglo = pval_limit - n_sigma_away_lo * pval_limit_err;
        const double pval_limit_sghi = pval_limit + n_sigma_away_hi * pval_limit_err;

        sig_limits.push_back(sig_limit_scan);
        pval_limits.push_back(pval_limit);
        pval_limit_errs.push_back(pval_limit_err);

        if (print_toys) {
          printf("  p_hat = %f -> %f +- %f  (%i,%i)s: [%f, %f]\n", p_hat, pval_limit, pval_limit_err, n_sigma_away_lo, n_sigma_away_hi, pval_limit_sglo, pval_limit_sghi);
          fflush(stdout);
        }

        if (pval_limit_sglo <= limit_alpha) {
          if (print_toys)
            printf("  ** include in bracket\n");

          bracket_sig_limit.push_back(sig_limit_scan);
          bracket_pval_limit.push_back(pval_limit);
          bracket_pval_limit_err.push_back(pval_limit_err);
        }

        if (pval_limit_sghi <= limit_alpha) {
          if (bracket_limit || ++n_below > 10)
            break;
        }

        sig_limit_scan += sig_limit_step;
      }

      printf("n_calls: %i time for limit: ", fit::n_calls); tsw_limit.Print();

      if (sig_limits.size()) {
        std::vector<double> sig_limit_errs(pval_limits.size(), 0.);
        TGraphErrors* g = new TGraphErrors(sig_limits.size(), &sig_limits[0], &pval_limits[0], &sig_limit_errs[0], &pval_limit_errs[0]);
        g->SetMarkerStyle(5);
        TF1* interp_fcn = new TF1("interp_fcn", "[0]*exp(-[1]*x)", bracket_sig_limit.front(), bracket_sig_limit.back());
        interp_fcn->SetParameters(0.5, 0.3);
        TFitResultPtr res = g->Fit(interp_fcn, "RS");
        const double a  = res->Parameter(0);
        const double b  = res->Parameter(1);
        const double ea = res->ParError(0);
        const double eb = res->ParError(1);
        const double cov = res->CovMatrix(0,1);
        const double dfda = 1/a/b;
        sig_limit = -log(limit_alpha/a)/b;
        const double dfdb = -sig_limit/b;
        sig_limit_err = sqrt(dfda*dfda * ea*ea + dfdb*dfdb * eb*eb + 2 * dfda * dfdb * cov);
        sig_limit_fit_n = bracket_sig_limit.size();
        sig_limit_fit_a     = a;
        sig_limit_fit_b     = b;
        sig_limit_fit_a_err = ea;
        sig_limit_fit_b_err = eb;
        sig_limit_fit_prob = res->Prob();
        g->SetName("g_limit_bracket_fit");
        if (save_plots)
          g->Write();
        else
          delete g;

        printf("  *** done bracketing (%lu points), y = %.2f at %f +- %f (prob: %f)\n", bracket_sig_limit.size(), limit_alpha, sig_limit, sig_limit_err, sig_limit_fit_prob);
      }

      delete h_toy_expected;
      h_toy_expected = 0;
    }

    t_fit_info->Fill();

    delete fit::interp;
  }
}
