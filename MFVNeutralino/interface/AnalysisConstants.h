#ifndef JMTucker_MFVNeutralino_AnalysisConstants_h
#define JMTucker_MFVNeutralino_AnalysisConstants_h

// This file is special, intended to be easily (read: hackily)
// parsable by a dumb python script later. Don't mess with the
// formatting if you don't know what you're doing!

namespace mfv {
  namespace AnalysisConstants {
    const double
    int_lumi_2015 = 2691.;

    const double
    int_lumi_2016 = 36810.;

    const double
    int_lumi = 39501.;

    const char*
    int_lumi_nice = "39.5 fb^{-1} (13 TeV)";

    const double
    scale_factor = 1.;
  }
}

#endif
