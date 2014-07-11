#ifndef JMTucker_MFVNeutralino_One2Two_Templates_h
#define JMTucker_MFVNeutralino_One2Two_Templates_h

#include <string>
#include <vector>

class TH1D;

namespace mfv {
  struct Template {
    int i;
    TH1D* h;

    Template(int i_, TH1D* h_) : i(i_), h(h_) {}
    virtual double chi2() const { return 0; }
    virtual std::string name() const { return std::string("NoName"); }
    virtual std::string title() const { return std::string("NoTitle"); }
    virtual size_t npars() const { return 0; }
    virtual double par(size_t) const { return 0.; }

    static const int nbins;
    static const double min_val;
    static const double max_val;

    static std::vector<double> binning();
    static TH1D* hist_with_binning(const char* name, const char* title);
    static TH1D* finalize_binning(TH1D* h);
    static TH1D* finalize_template(TH1D* h);

    static const int max_npars;
    std::vector<double> pars;
  };

  //////////////////////////////////////////////////////////////////////////////

  struct PhiShiftTemplate : public Template {
    double phi_exp;
    double shift;

    PhiShiftTemplate(int i_, TH1D* h_, const double phi_exp_, const double shift_);

    virtual double chi2() const;
    virtual std::string name() const;
    virtual std::string title() const;
    virtual double par(size_t w) const;
  };

  //////////////////////////////////////////////////////////////////////////////

  struct ClearedJetsTemplate : public Template {
    ClearedJetsTemplate(int i_, TH1D* h_);
  };

  //////////////////////////////////////////////////////////////////////////////

  typedef std::vector<Template*> Templates;
}

#endif
