#ifndef JMTucker_MFVNeutralino_One2Two_Random_h
#define JMTucker_MFVNeutralino_One2Two_Random_h

#include <vector>

class TRandom;

namespace jmt {
  extern const int seed_base;

  std::vector<int> knuth_choose_wo_replacement(TRandom* rand, int N, int n);
}

#endif
