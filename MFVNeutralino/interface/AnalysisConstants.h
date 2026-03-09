
#ifndef JMTucker_MFVNeutralino_AnalysisConstants_h
#define JMTucker_MFVNeutralino_AnalysisConstants_h

// This file is special, intended to be easily (read: hackily)
// parsable by a dumb python script later. Don't mess with the
// formatting if you don't know what you're doing!

namespace mfv {
  namespace AnalysisConstants {

    // JPR 2/5/2026: turning off old preUL stuff, that in principle is no longer used
    /*
    const double
    int_lumi_2015 = 2613.;

    const char*
    int_lumi_nice_2015 = "  2.6 fb^{-1} (13 TeV)";

    const double
    scale_factor_2015 = 1.0;

    const double
    scaled_int_lumi_2015 = int_lumi_2015 * scale_factor_2015;

    //

    const double
    int_lumi_2016 = 35916.;
    // This is for preUL

    const char*
    int_lumi_nice_2016 = "35.9 fb^{-1} (13 TeV)";

    const double
    scale_factor_2016 = 1.00;

    const double
    scaled_int_lumi_2016 = int_lumi_2016 * scale_factor_2016;

    //

    const double
    int_lumi_2015p6 = int_lumi_2015 + int_lumi_2016;

    const char*
    int_lumi_nice_2015p6 = "38.5 fb^{-1} (13 TeV)";

    const double
    scale_factor_2015p6 = 1.00;

    const double
    scaled_int_lumi_2015p6 = scaled_int_lumi_2015 + scaled_int_lumi_2016;
    */

    //

    const double
    int_lumi_20161 = 19502.;

    const char*
    int_lumi_nice_20161 = "19.5 fb^{-1} (13 TeV)";

    const double
    scale_factor_20161 = 1.00;

    const double
    scaled_int_lumi_20161 = int_lumi_20161 * scale_factor_20161;

    //

    const double
    int_lumi_20162 = 16812.;

    const char*
    int_lumi_nice_20162 = "16.8 fb^{-1} (13 TeV)";

    const double
    scale_factor_20162 = 1.00;

    const double
    scaled_int_lumi_20162 = int_lumi_20162 * scale_factor_20162;

    //

    const double
    int_lumi_2016 = int_lumi_20161 + int_lumi_20162;

    const char*
    int_lumi_nice_2016 = "36.3 fb^{-1} (13 TeV)";

    const double
    scale_factor_2016 = 1.00;

    const double
    scaled_int_lumi_2016 = int_lumi_2016 * scale_factor_2016;

    //

    const double
    int_lumi_2017 = 42068.;

    const char*
    int_lumi_nice_2017 = "  42.1 fb^{-1} (13 TeV)";

    const double
    scale_factor_2017 = 1.00;

    const double
    scaled_int_lumi_2017 = int_lumi_2017 * scale_factor_2017;

    //

    const double
    int_lumi_2018 = 59561.;

    const char*
    int_lumi_nice_2018 = "  59.6 fb^{-1} (13 TeV)";

    const double
    scale_factor_2018 = 1.00;

    const double
    scaled_int_lumi_2018 = int_lumi_2018 * scale_factor_2018;

    //

    const double
    int_lumi_2017p8 = int_lumi_2017 + int_lumi_2018;

    const char*
    int_lumi_nice_2017p8 = "  101.6 fb^{-1} (13 TeV)";

    const double
    scale_factor_2017p8 = 1.00;

    const double
    scaled_int_lumi_2017p8 = scaled_int_lumi_2017 + scaled_int_lumi_2018;

    //

    const double
    int_lumi_run2 = int_lumi_20161 + int_lumi_20162 + int_lumi_2017 + int_lumi_2018;

    const char*
    int_lumi_nice_run2 = "  137.9 fb^{-1} (13 TeV)";

    const double
    scale_factor_run2 = 1.00;

    const double
    scaled_int_lumi_run2 = scaled_int_lumi_20161 + scaled_int_lumi_20162 + scaled_int_lumi_2017 + scaled_int_lumi_2018;

    //

    const double
    int_lumi_bjet_trig_2017 = 37187.;

    const char*
    int_lumi_nice_bjet_trig_2017 = "  37.2 fb^{-1} (13 TeV)";

    const double
    scale_factor_bjet_trig_2017 = 1.00;

    const double
    scaled_int_lumi_bjet_trig_2017 = int_lumi_bjet_trig_2017 * scale_factor_bjet_trig_2017;

    //

    const double
    int_lumi_bjet_trig_2018 = 54286.;

    const char*
    int_lumi_nice_bjet_trig_2018 = "  54.3 fb^{-1} (13 TeV)";

    const double
    scale_factor_bjet_trig_2018 = 1.00;

    const double
    scaled_int_lumi_bjet_trig_2018 = int_lumi_bjet_trig_2018 * scale_factor_bjet_trig_2018;

    //

    const double
    int_lumi_bjet_trig_2017p8 = int_lumi_bjet_trig_2017 + int_lumi_bjet_trig_2018;

    const char*
    int_lumi_nice_bjet_trig_2017p8 = "  91.5 fb^{-1} (13 TeV)";

    const double
    scale_factor_bjet_trig_2017p8 = 1.00;

    const double
    scaled_int_lumi_bjet_trig_2017p8 = scaled_int_lumi_bjet_trig_2017 + scaled_int_lumi_bjet_trig_2018;

    //

    const double
    int_lumi_bjet_trig_run2 = int_lumi_20161 + int_lumi_20162 + int_lumi_bjet_trig_2017 + int_lumi_bjet_trig_2018;

    const char*
    int_lumi_bjet_trig_nice_run2 = "  127.8 fb^{-1} (13 TeV)";

    const double
    scale_factor_bjet_trig_run2 = 1.00;

    const double
    scaled_int_lumi_bjet_trig_run2 = scaled_int_lumi_20161 + scaled_int_lumi_20162 + scaled_int_lumi_bjet_trig_2017 + scaled_int_lumi_bjet_trig_2018;
  
  }
}

#endif
