#ifndef JMTucker_MFVNeutralino_One2Two_Templates_h
#define JMTucker_MFVNeutralino_One2Two_Templates_h

#include <string>
#include <vector>

class TH1D;

namespace mfv {
  struct Template {
    int i;
    TH1D* h;
    TH1D* h_final;

    Template(int i_, TH1D* h_) : i(i_), h(h_), h_final(0) {}
    virtual double chi2() const { return 0; }
    virtual std::string name() const { return std::string("NoName"); }
    virtual std::string title() const { return std::string("NoTitle"); }
    virtual size_t npars() const { return 0; }
    virtual double par(size_t) const { return 0.; }

    static const int max_npars;
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
