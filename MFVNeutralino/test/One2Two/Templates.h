#ifndef JMTucker_MFVNeutralino_One2Two_Templates_h
#define JMTucker_MFVNeutralino_One2Two_Templates_h

class TH1D;

namespace mfv {
  struct Template {
    int i;
    const TH1D* h;
    Template(int i_, const TH1D* h_) : i(i_), h(h_) {}
  };

  struct PhiShiftTemplate : public Template {
    double phi_exp;
    double shift;

    PhiShiftTemplate(int i_, const TH1D* h_, const double phi_exp_, const double shift_)
      : Template(i_, h_),
        phi_exp(phi_exp_),
        shift(shift_)
    {
    }
  };

  struct ClearedJetsTemplate : public Template {
    ClearedJetsTemplate(int i_, const TH1D* h_)
      : Template(i_, h_)
    {
    }
  };

  //////////////////////////////////////////////////////////////////////////////

  typedef std::vector<Template*> Templates;
}

#endif
