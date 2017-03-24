#ifndef JMTucker_MFVNeutralino_AnalysisConstants_h
#define JMTucker_MFVNeutralino_AnalysisConstants_h

// This file is special, intended to be easily (read: hackily)
// parsable by a dumb python script later. Don't mess with the
// formatting if you don't know what you're doing!

namespace mfv {
  namespace AnalysisConstants {
    const double
    int_lumi_2015 = 2683.;

    const double
    int_lumi_2016 = 35867.;

    const double
    int_lumi = 38550.;

    const char*
    int_lumi_nice_2015 = "  2.7 fb^{-1} (13 TeV)";

    const char*
    int_lumi_nice_2016 = "35.9 fb^{-1} (13 TeV)";

    const double
    scale_factor_2015 = 1.;

    const double
    scale_factor_2016 = 1.;
  }
}

#endif
