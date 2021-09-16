#include "DataFormats/PatCandidates/interface/Jet.h"
#include "JMTucker/Tools/interface/BTagging.h"
#include "JMTucker/Tools/interface/Year.h"

namespace jmt {
  namespace BTagging {
    float discriminator_min(int wp, bool old) {
      assert(wp >= 0 && wp <= 2);
      const float old_mins[3] = {0.1355, 0.4506, 0.7738}; // JMTBAD drop
      const float mins[2][3] = { {0.0532, 0.3040, 0.7476}, {0.0490, 0.2783, 0.7100} };
      return (old ? old_mins : mins[jmt::Year::get()-2017])[wp];
    }

    bool is_tagged(double disc, int wp, bool old) {
      return disc > discriminator_min(wp, old);
    }

    float discriminator(const pat::Jet& jet, bool old) {
      if (old)
        return jet.bDiscriminator("pfDeepCSVJetTags:probb") + jet.bDiscriminator("pfDeepCSVJetTags:probbb"); // DeepCSV
      else
        return jet.bDiscriminator("pfDeepFlavourJetTags:probb") + jet.bDiscriminator("pfDeepFlavourJetTags:probbb") + jet.bDiscriminator("pfDeepFlavourJetTags:problepb"); // DeepFlavour
    }

    bool is_tagged(const pat::Jet& jet, int wp, bool old) {
      return is_tagged(discriminator(jet, old), wp, old);
    }
  }
}
