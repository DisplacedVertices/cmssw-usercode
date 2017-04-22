#include "Phi.h"
#include "ROOTTools.h"
#include "Templates.h"

#include <cmath>
#include "TString.h"
#include "TH1D.h"
#include "VAException.h"

namespace mfv {
  const bool Template::fine_binning = false;
  const int Template::nbins = 20000;
  const double Template::min_val = 0;
  const double Template::max_val = 10;
  const double Template::bin_width = (Template::max_val - Template::min_val) / Template::nbins;
  const int Template::max_npars = 3;

  void Template::set_h_phi() {
    h_phi = Phi::new_1d_hist(TString::Format("%s_phi", h->GetName()), h->GetTitle());
  }

  std::vector<double> Template::binning(const bool shorten_last) {
    std::vector<double> bins = {0, 0.04, 0.07};
    bins.push_back(shorten_last ? 0.15 : 4);
    return bins;
  }

  TH1D* Template::shorten_hist(TH1D* h, bool save) {
    const std::vector<double> bins = binning(true);
    TH1D* h_short = (TH1D*)h->Rebin(bins.size()-1, TString::Format("%s_shortened", h->GetName()), &bins[0]);
    // Splitting the last bin puts its contents in the overflow -- move back into last bin.
    const int n = h_short->GetNbinsX();
    const double v = h_short->GetBinContent(n+1);
    const double e = h_short->GetBinError(n+1);
    h_short->SetBinContent(n+1, 0);
    h_short->SetBinError  (n+1, 0);
    h_short->SetBinContent(n, v);
    h_short->SetBinError  (n, e);
    if (!save)
      h_short->SetDirectory(0);
    return h_short;
  }

  TH1D* Template::hist_with_binning(const char* name, const char* title) {
    std::vector<double> bins = binning();
    return new TH1D(name, title, bins.size()-1, &bins[0]);
  }

  TH1D* Template::finalize_binning(TH1D* h) {
    std::vector<double> bins = binning();
    TH1D* hh = (TH1D*)h->Rebin(bins.size()-1, TString::Format("%s_rebinned", h->GetName()), &bins[0]);
    jmt::deoverflow(hh);
    return hh;
  }

  TH1D* Template::finalize_template(TH1D* h) {
    TH1D* hh = finalize_binning(h);
    hh->Scale(1./hh->Integral());
    return hh;
  }

  void Template::finalize_template_in_place(TH1D* h) {
    jmt::deoverflow(h);
    h->Scale(1./h->Integral());
  }

  //////////////////////////////////////////////////////////////////////////////

  PhiShiftTemplate::PhiShiftTemplate(int i_, TH1D* h_, const double phi_exp_, const double shift_)
    : Template(i_, h_),
      phi_exp(phi_exp_),
      shift(shift_)
  {
    pars.push_back(phi_exp);
    pars.push_back(shift);
  }

  double PhiShiftTemplate::chi2() const {
    return 0; // pow(phi_exp - 1.7, 2)/0.7
  }

  std::string PhiShiftTemplate::name() const {
    char buf[128];
    snprintf(buf, 128, "phishift%04i", i);
    return std::string(buf);
  }

  std::string PhiShiftTemplate::title() const {
    char buf[128];
    snprintf(buf, 128, "phi_exp = %f, shift = %g", phi_exp, shift);
    return std::string(buf);
  }

  double PhiShiftTemplate::par(size_t w) const {
    if (w == 0)
      return phi_exp;
    else if (w == 1)
      return shift;
    else
      return 0.;
  }

  //////////////////////////////////////////////////////////////////////////////

  ClearedJetsTemplate::ClearedJetsTemplate(int i_, TH1D* h_, const double mu, const double sigma)
    : Template(i_, h_),
      clearing_mu(mu),
      clearing_sigma(sigma)
  {
    pars.push_back(mu);
    pars.push_back(sigma);
  }

  std::string ClearedJetsTemplate::name() const {
    char buf[128];
    snprintf(buf, 128, "clearedjets%04i", i);
    return std::string(buf);
  }

  std::string ClearedJetsTemplate::title() const {
    char buf[128];
    snprintf(buf, 128, "clearing_mu = %f, clearing_sigma = %g", clearing_mu, clearing_sigma);
    return std::string(buf);
  }

  double ClearedJetsTemplate::par(size_t w) const {
    if (w == 0)
      return clearing_mu;
    else if (w == 1)
      return clearing_sigma;
    else
      return 0.;
  }

  //////////////////////////////////////////////////////////////////////////////

  SimpleClearingTemplate::SimpleClearingTemplate(int i_, TH1D* h_, const double sigma)
    : Template(i_, h_),
      clearing_sigma(sigma)
  {
    pars.push_back(sigma);
    pars.push_back(0);
  }

  std::string SimpleClearingTemplate::name() const {
    char buf[128];
    snprintf(buf, 128, "simpleclear%04i", i);
    return std::string(buf);
  }

  std::string SimpleClearingTemplate::title() const {
    char buf[128];
    snprintf(buf, 128, "clearing_sigma = %g", clearing_sigma);
    return std::string(buf);
  }

  double SimpleClearingTemplate::par(size_t w) const {
    if (w == 0)
      return clearing_sigma;
    else
      return 0.;
  }

  //////////////////////////////////////////////////////////////////////////////

  Run2Template::Run2Template(int i_, TH1D* h_)
    : Template(i_, h_)
  {
  }

  //////////////////////////////////////////////////////////////////////////////

  int TemplateInterpolator::extra_prints = 0;

  TemplateInterpolator::TemplateInterpolator(Templates* templates_, int n_bins_,
                                             const std::vector<TemplatePar>& par_infos_,
                                             std::vector<double>& a_)
    : templates(templates_),
      n_bins(n_bins_),
      n_pars(templates->at(0)->npars()),
      par_infos(par_infos_),
      a(a_)
  {
    if (n_pars > 2)
      jmt::vthrow("only n_pars = 2 implemented in TemplateInterpolator"); // JMTBAD

    if (int(par_infos.size()) != n_pars)
      jmt::vthrow("TemplateInterpolator:: par_infos size %lu != n_pars %i", par_infos.size(), n_pars);

    for (Template* t : *templates)
      if (int(t->npars()) != n_pars)
        jmt::vthrow("template mismatch in TemplateInterpolator");

    if (int(a.size()) != n_bins+2)
      jmt::vthrow("TemplateInterpolator:: wrong n_bins in a");

    if (n_pars > 0) {
      int nR = 0;
      int nQ = 1;
      for (int i = 0; i < n_pars; ++i) {
        nR += 2*nQ;
        nQ *= 2;
      }

      R.resize(nR);
      for (std::vector<double>& v : R)
        v.resize(n_bins+2);
      Q.resize(nQ);
    }
    else {
      if (templates->size() != 1)
        jmt::vthrow("npars == 1 and more than one template");
    }
  }

  int TemplateInterpolator::i_par(int i, double par) const {
    if (n_pars == 0)
      return 0;

    double dret = (par - par_infos[i].start) / par_infos[i].step;
    if (dret >= par_infos[i].nsteps)
      return par_infos[i].nsteps - 1;
    int ret(dret);
    if (ret <= 0)
      return 0;
    else if (ret >= par_infos[i].nsteps)
      return par_infos[i].nsteps - 1;
    else
      return ret;
  }

  int TemplateInterpolator::i_Q(const std::vector<double>& pars) const {
    if (n_pars == 0)
      return 0;

    std::vector<int> ipars;
    int ret = 0;
    int mult = 1;
    //if (extra_prints) printf("\niq %f %f\n", pars[0], pars[1]);
    for (int i = n_pars-1; i >= 0; --i) {
      int ip = i_par(i, pars[i]);
      ret += ip * mult;
      mult *= par_infos[i].nsteps;
      //if (extra_prints) printf("i %i ip %i ret %i mult %i\n", i, ip, ret, mult);
    }
    return ret;
  }

  Template* TemplateInterpolator::get_Q(const std::vector<double>& pars) const {
    return (*templates)[i_Q(pars)];
  }

  void TemplateInterpolator::interpolate(const std::vector<double>& pars, std::vector<double>* a_p) {
    if (int(pars.size()) != n_pars)
      jmt::vthrow("TemplateInterpolator::interpolate: pars size %lu != n_pars %i", pars.size(), n_pars);

    if (a_p == 0)
      a_p = &a;

    if (n_pars == 0) {
      for (int ibin = 1; ibin <= n_bins; ++ibin)
        (*a_p)[ibin] = (*templates)[0]->h->GetBinContent(ibin);
      return;
    }

    if (n_pars == 1) {
      const int i_par0 = i_par(0, pars[0]);
      const int i_par0_p1 = i_par0 == par_infos[0].nsteps - 1 ? i_par0 : i_par0 + 1;
      Q[0] = (*templates)[i_par0   ];
      Q[1] = (*templates)[i_par0_p1];
      const double d = Q[1]->par(0) - Q[0]->par(0);
      const double f = (Q[1]->par(0) - pars[0])/d;
      for (int ibin = 1; ibin <= n_bins; ++ibin)
        (*a_p)[ibin] = f * Q[0]->h->GetBinContent(ibin) + (1-f) * Q[1]->h->GetBinContent(ibin);
      return;
    }

    const int i_par0 = i_par(0, pars[0]);
    const int i_par1 = i_par(1, pars[1]);
    const int i_par0_p1 = i_par0 == par_infos[0].nsteps - 1 ? i_par0 : i_par0 + 1;
    const int i_par1_p1 = i_par1 == par_infos[1].nsteps - 1 ? i_par1 : i_par1 + 1;
    const int n_par1 = par_infos[1].nsteps;

    Q[0] = (*templates)[n_par1 * i_par0    + i_par1   ];
    Q[1] = (*templates)[n_par1 * i_par0    + i_par1_p1];
    Q[2] = (*templates)[n_par1 * i_par0_p1 + i_par1   ];
    Q[3] = (*templates)[n_par1 * i_par0_p1 + i_par1_p1];

    if (extra_prints) {
      printf("interpolate: %f %f\n", pars[0], pars[1]);
      printf("ntemplates: %i  i_par0: %i  p1: %i  i_par1: %i  p1: %i  n_par1: %i\n", int(templates->size()), i_par0, i_par0_p1, i_par1, i_par1_p1, n_par1);
      for (int i = 0; i < 4; ++i) {
        printf("Q%i: %s\n", i, Q[i]->title().c_str());
        for (int ibin = 1; ibin <= n_bins; ++ibin)
          printf("   %i %f\n", ibin, Q[i]->h->GetBinContent(ibin));
      }
    }

    if (i_par0 == i_par0_p1 && i_par1 == i_par1_p1) {
      for (int ibin = 1; ibin <= n_bins; ++ibin)
        (*a_p)[ibin] = Q[0]->h->GetBinContent(ibin);
    }
    else if (i_par0 == i_par0_p1) {
      const double d = Q[1]->par(1) - Q[0]->par(1);
      const double f = (Q[1]->par(1) - pars[1])/d;
      for (int ibin = 1; ibin <= n_bins; ++ibin)
        (*a_p)[ibin] = f * Q[0]->h->GetBinContent(ibin) + (1-f) * Q[1]->h->GetBinContent(ibin);
    }
    else if (i_par1 == i_par1_p1) {
      const double d = Q[2]->par(0) - Q[0]->par(0);
      const double f = (Q[2]->par(0) - pars[0])/d;
      for (int ibin = 1; ibin <= n_bins; ++ibin)
        (*a_p)[ibin] = f * Q[0]->h->GetBinContent(ibin) + (1-f) * Q[2]->h->GetBinContent(ibin);
    }
    else {
      for (int i = 0; i < 2; ++i) {
        const double d = Q[2+i]->par(0) - Q[i]->par(0);
        const double f = (Q[2+i]->par(0) - pars[0])/d;
        if (extra_prints) printf("R[%i] d %f f %f\n", i, d, f);
        for (int ibin = 1; ibin <= n_bins; ++ibin) {
          R[i][ibin] = f * Q[i]->h->GetBinContent(ibin) + (1-f) * Q[2+i]->h->GetBinContent(ibin);
          if (extra_prints) printf("   Q[%i][%i] %f  Q[%i][%i] %f  R[%i][%i] %f\n", ibin, i, Q[i]->h->GetBinContent(ibin), 2+i, ibin, Q[2+i]->h->GetBinContent(ibin), i, ibin, R[i][ibin]);
        }
      }

      const double d = Q[1]->par(1) - Q[0]->par(1);
      const double f = (Q[1]->par(1) - pars[1])/d;
      if (extra_prints) printf("a d %f f %f\n", d, f);
      for (int ibin = 1; ibin <= n_bins; ++ibin) {
        (*a_p)[ibin] = f * R[0][ibin] + (1-f) * R[1][ibin];
        if (extra_prints) printf("   R[0][%i] %f R[1][%i] %f  a[%i] %f\n", ibin, R[0][ibin], ibin, R[1][ibin], ibin, (*a_p)[ibin]);
      }
    }
  }
}
