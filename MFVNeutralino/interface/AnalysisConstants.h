#ifndef JMTucker_MFVNeutralino_AnalysisConstants_h
#define JMTucker_MFVNeutralino_AnalysisConstants_h

// This file is special, intended to be easily (read: hackily)
// parsable by a dumb python script later. Don't mess with the
// formatting if you don't know what you're doing!

namespace mfv {
  namespace AnalysisConstants {
    const double
    int_lumi_2015 = 2613.;

    const char*
    int_lumi_nice_2015 = "  2.6 fb^{-1} (13 TeV)";

    const double
    scale_factor_2015 = 0.99;

    const double
    scaled_int_lumi_2015 = int_lumi_2015 * scale_factor_2015;

    //

    const double
    int_lumi_2016 = 35916.;

    const char*
    int_lumi_nice_2016 = "35.9 fb^{-1} (13 TeV)";

    const double
    scale_factor_2016 = 0.99;

    const double
    scaled_int_lumi_2016 = int_lumi_2016 * scale_factor_2016;

    //

    const double
    int_lumi_2015p6 = int_lumi_2015 + int_lumi_2016;

    const char*
    int_lumi_nice_2015p6 = "38.5 fb^{-1} (13 TeV)";

    const double
    scale_factor_2015p6 = 0.99;

    const double
    scaled_int_lumi_2015p6 = scaled_int_lumi_2015 + scaled_int_lumi_2016;

    //

    const double
    int_lumi_2017 = 41521.;

    const char*
    int_lumi_nice_2017 = "  41.5 fb^{-1} (13 TeV)";

    const double
    scale_factor_2017 = 0.989;

    const double
    scaled_int_lumi_2017 = int_lumi_2017 * scale_factor_2017;

    //

    const double
    int_lumi_2018 = 59693.;

    const char*
    int_lumi_nice_2018 = "  59.7 fb^{-1} (13 TeV)";

    const double
    scale_factor_2018 = 0.989;

    const double
    scaled_int_lumi_2018 = int_lumi_2018 * scale_factor_2018;

    //

    const double
    int_lumi_2017p8 = int_lumi_2017 + int_lumi_2018;

    const char*
    int_lumi_nice_2017p8 = "  101 fb^{-1} (13 TeV)";

    const double
    scale_factor_2017p8 = 0.989;

    const double
    scaled_int_lumi_2017p8 = scaled_int_lumi_2017 + scaled_int_lumi_2018;
  }
}

#endif
