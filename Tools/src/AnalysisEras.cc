#include "JMTucker/Tools/interface/AnalysisEras.h"

int jmt::AnalysisEras::current_era_ = jmt::AnalysisEras::e_max;
unsigned jmt::AnalysisEras::current_run_ = -1;
unsigned jmt::AnalysisEras::current_ls_ = -1;
unsigned long long jmt::AnalysisEras::current_event_ = -1;

// JPR 2/20/2026: I took the numbers from Ang's EXO-22-020 AN. That search admittedly used a different trigger with 
// different availability vs. time, but for our purposes is good enough for this. 
const double jmt::AnalysisEras::int_lumi_[] = { 0, 5.826, 2.621, 4.286, 4.066, 2.865, 0.584, 7.653, 8.740, 4.80, 9.63, 4.25, 9.32, 13.5, 14.0, 7.09, 6.94, 31.9 };
