#include "Templates.h"

#include <cmath>
#include "TH1D.h"

namespace mfv {
  const int Template::nbins = 20000;
  const double Template::min_val = 0;
  const double Template::max_val = 10;

  const int Template::max_npars = 3;

  std::vector<double> Template::binning() {
    std::vector<double> bins;
    for (int i = 0; i < 20; ++i)
      bins.push_back(i * 0.01);
    bins.push_back(0.2);
    bins.push_back(0.4);
    bins.push_back(0.6);
    bins.push_back(1);
    bins.push_back(3);
    return bins;
  }

  TH1D* Template::hist_with_binning(const char* name, const char* title) {
    std::vector<double> bins = binning();
    return new TH1D(name, title, bins.size()-1, &bins[0]);
  }

  TH1D* Template::finalize_binning(TH1D* h) {
    std::vector<double> bins = binning();
    TH1D* hh = (TH1D*)h->Rebin(bins.size()-1, TString::Format("%s_rebinned", h->GetName()), &bins[0]);
    const int nb = hh->GetNbinsX();
    const double l  = hh->GetBinContent(nb);
    const double le = hh->GetBinError  (nb);
    const double o  = hh->GetBinContent(nb+1);
    const double oe = hh->GetBinError  (nb+1);
    hh->SetBinContent(nb, l + o);
    hh->SetBinError  (nb, sqrt(le*le + oe*oe));
    hh->SetBinContent(nb+1, 0);
    hh->SetBinError  (nb+1, 0);
    return hh;
  }

  TH1D* Template::finalize_template(TH1D* h) {
    TH1D* hh = finalize_binning(h);
    hh->Scale(1./hh->Integral());
    return hh;
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

  ClearedJetsTemplate::ClearedJetsTemplate(int i_, TH1D* h_)
    : Template(i_, h_)
  {
  }
}
