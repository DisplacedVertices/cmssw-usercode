#include "JMTucker/Tools/interface/AnalysisEras.h"

int jmt::AnalysisEras::current_era_ = jmt::AnalysisEras::e_max;
unsigned jmt::AnalysisEras::current_run_ = -1;
unsigned jmt::AnalysisEras::current_ls_ = -1;
unsigned long long jmt::AnalysisEras::current_event_ = -1;

const double jmt::AnalysisEras::int_lumi_[] = { 4.794, 9.631, 4.248, 9.315, 13.540, 14.028, 7.067, 6.895, 31.747 };
