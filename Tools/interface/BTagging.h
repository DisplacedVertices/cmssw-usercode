#ifndef JMTucker_Tools_BTagging_h
#define JMTucker_Tools_BTagging_h

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "JMTucker/Tools/interface/BTagging.h"
#include "JMTucker/Tools/interface/Year.h"

namespace jmt {
  class BTagging {
  public:
    static float discriminator(const pat::Jet& jet, bool old=false) {
      if (old)
        return jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags"); // CSVv2
      else
        return jet.bDiscriminator("pfDeepFlavourJetTags:probb") + jet.bDiscriminator("pfDeepFlavourJetTags:probbb") + jet.bDiscriminator("pfDeepFlavourJetTags:problepb"); // DeepFlavour
    }

    enum { loose, medium, tight, nwp };

    static float discriminator_min(int wp, bool old=false) {
      assert(wp >= 0 && wp <= 2);
      if (old) {
        const float mins[3] = {0.5803, 0.8838, 0.9693};
        return mins[wp];
      }
      else {
#ifdef MFVNEUTRALINO_2017
        const float mins[3] = {0.0521, 0.3033, 0.7489};
#elif defined(MFVNEUTRALINO_2018)
        const float mins[3] = {0.0494, 0.2770, 0.7264};
#else
#error bad year
#endif
        return mins[wp];
      }
    }

    static bool is_tagged(const pat::Jet& jet, int wp, bool old=false) {
      return discriminator(jet, old) > discriminator_min(wp, old);
    }
  };
}

#endif
