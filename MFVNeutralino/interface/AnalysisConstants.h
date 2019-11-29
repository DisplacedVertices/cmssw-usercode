#ifndef JMTucker_MFVNeutralino_AnalysisConstants_h
#define JMTucker_MFVNeutralino_AnalysisConstants_h

// This file is special, intended to be easily (read: hackily)
// parsable by a dumb python script later. Don't mess with the
// formatting if you don't know what you're doing!

namespace mfv {
  namespace AnalysisConstants {
    const double
    int_lumi_2017 = 41521.;

    const char*
    int_lumi_nice_2017 = "  41.5 fb^{-1} (13 TeV)";

    const double
    scale_factor_2017 = 0.989;

    const double
    scaled_int_lumi_2017 = int_lumi_2017 * scale_factor_2017;

    const double
    int_lumi_2018 = 59693.;

    const char*
    int_lumi_nice_2018 = "  59.7 fb^{-1} (13 TeV)";

    const double
    scale_factor_2018 = 0.989;

    const double
    scaled_int_lumi_2018 = int_lumi_2018 * scale_factor_2018;

    const double
    int_lumi_2017p8 = int_lumi_2017 + int_lumi_2018;

    const char*
    int_lumi_nice_2017p8 = "  101 fb^{-1} (13 TeV)";

    const double
    scale_factor_2017p8 = 0.989;

    const double
    scaled_int_lumi_2017p8 = int_lumi_2017p8 * scale_factor_2017p8;
  }
}

#endif
