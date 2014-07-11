#ifndef JMTucker_MFVNeutralino_One2Two_Phi_h
#define JMTucker_MFVNeutralino_One2Two_Phi_h

class TH1D;

namespace mfv {
  struct Phi {
    static const bool use_abs;
    static const int nbins;
    static const double min;
    static const double max;

    static TH1D* new_1d_hist(const char* name, const char* title);
  };
}

#endif
