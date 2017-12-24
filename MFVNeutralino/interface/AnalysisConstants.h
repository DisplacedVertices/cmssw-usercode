#ifndef JMTucker_MFVNeutralino_AnalysisConstants_h
#define JMTucker_MFVNeutralino_AnalysisConstants_h

// This file is special, intended to be easily (read: hackily)
// parsable by a dumb python script later. Don't mess with the
// formatting if you don't know what you're doing!

namespace mfv {
  namespace AnalysisConstants {
    const double
    int_lumi_2015 = 2613.;

    const double
    int_lumi_2016 = 35916.;

    const double
    int_lumi_2015p6 = 38529.;

    const char*
    int_lumi_nice_2015 = "  2.6 fb^{-1} (13 TeV)";

    const char*
    int_lumi_nice_2016 = "35.9 fb^{-1} (13 TeV)";

    const char*
    int_lumi_nice_2015p6 = "38.5 fb^{-1} (13 TeV)";

    const double
    scale_factor_2015 = 1.;

    const double
    scale_factor_2016 = 1.;

    const double
    scale_factor_2015p6 = 1.;
  }
}

#endif
