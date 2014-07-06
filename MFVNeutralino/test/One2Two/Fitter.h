#ifndef JMTucker_MFVNeutralino_One2Two_Fitter_h
#define JMTucker_MFVNeutralino_One2Two_Fitter_h

#include "ConfigFromEnv.h"

namespace mfv {
  struct Fitter {
    const std::string name;
    const std::string uname;

    jmt::ConfigFromEnv env;

    TFile* fout;
    TDirectory* dout;
    TDirectory* dtoy;
    TRandom* rand;
    const int seed;

    ////////////////////////////////////////////////////////////////////////////

    // output objs and hists

    ////////////////////////////////////////////////////////////////////////////

    // diag and output trees
    
    ////////////////////////////////////////////////////////////////////////////

    Fitter(const std::string& name_, TFile* f, TRandom* r);
    //    ~Fitter();

    void book_trees();
  };
}

#endif
