#include "Random.h"
#include <vector>
#include "TRandom3.h"
#include "VAException.h"

namespace jmt {
  const int seed_base = 12191982;

  std::vector<int> knuth_choose_wo_replacement(TRandom* rand, int N, int n) {
    std::vector<int> r;
    if (n > N)
      vthrow("cannot choose without replacement %i items from %i items", n, N);

    int t = 0, m = 0;
    while (m < n) {
      if ((N - t) * rand->Rndm() >= n - m)
        ++t;
      else {
        ++m;
        r.push_back(t++);
      }
    }

    return r;
  }
}
