#include "DataFormats/PatCandidates/interface/Jet.h"
#include "JMTucker/Tools/interface/BTagging.h"
#include "JMTucker/Tools/interface/Year.h"

namespace jmt {
  namespace BTagging {
    float discriminator_min(int wp, bool old) {
      assert(wp >= 0 && wp <= 2);
      // FIXME: check whether this need to be changed for UL
      const float old_mins[3] = {0.5803, 0.8838, 0.9693}; // JMTBAD drop
      const float mins[2][3] = { {0.0521, 0.3033, 0.7489}, {0.0494, 0.2770, 0.7264} };
      return (old ? old_mins : mins[jmt::Year::get()-2017])[wp];
    }

    bool is_tagged(double disc, int wp, bool old) {
      return disc > discriminator_min(wp, old);
    }

    float discriminator(const pat::Jet& jet, bool old) {
      if (old)
        return jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags"); // CSVv2
      else
        return jet.bDiscriminator("pfDeepFlavourJetTags:probb") + jet.bDiscriminator("pfDeepFlavourJetTags:probbb") + jet.bDiscriminator("pfDeepFlavourJetTags:problepb"); // DeepFlavour
    }

    bool is_tagged(const pat::Jet& jet, int wp, bool old) {
      return is_tagged(discriminator(jet, old), wp, old);
    }
  }
}
