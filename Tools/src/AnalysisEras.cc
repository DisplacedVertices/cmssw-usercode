#include "JMTucker/Tools/interface/AnalysisEras.h"

int jmt::AnalysisEras::current_era_ = jmt::AnalysisEras::e_max;
unsigned jmt::AnalysisEras::current_run_ = -1;
unsigned jmt::AnalysisEras::current_ls_ = -1;
unsigned long long jmt::AnalysisEras::current_event_ = -1;

const double jmt::AnalysisEras::int_lumi_[] = { 4.803, 9.573, 4.248, 9.315, 12.671, 13.978, 7.064, 6.895, 31.747 };
