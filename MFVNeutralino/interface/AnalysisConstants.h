#ifndef JMTucker_MFVNeutralino_AnalysisConstants_h
#define JMTucker_MFVNeutralino_AnalysisConstants_h

// This file is special, intended to be easily (read: hackily)
// parsable by a dumb python script later. Don't mess with the
// formatting if you don't know what you're doing!

namespace mfv {
  namespace AnalysisConstants {
    const double
    int_lumi = 17600.;

    const char*
    int_lumi_nice = "17.6 fb^{-1}";

    const double
    scale_factor = 0.978;
  }
}

#endif
