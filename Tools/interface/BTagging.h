#ifndef JMTucker_Tools_BTagging_h
#define JMTucker_Tools_BTagging_h

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "JMTucker/Tools/interface/Year.h"

namespace jmt {
  class BTagging {
    static int year_;

  public:
    static void set_year(int y) { year_ = y; }

    static float discriminator(const pat::Jet& jet, bool old=false) {
      if (old)
        return jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags"); // CSVv2
      else
        return jet.bDiscriminator("pfDeepFlavourJetTags:probb") + jet.bDiscriminator("pfDeepFlavourJetTags:probbb") + jet.bDiscriminator("pfDeepFlavourJetTags:problepb"); // DeepFlavour
    }

    enum { loose, medium, tight, nwp };

    static float discriminator_min(int wp, bool old=false) {
      assert(wp >= 0 && wp <= 2);
      assert(year_ == 2017 || year_ == 2018);
      const float old_mins[3] = {0.5803, 0.8838, 0.9693}; // JMTBAD drop
      const float mins[2][3] = { {0.0521, 0.3033, 0.7489}, {0.0494, 0.2770, 0.7264} };
      return (old ? old_mins : mins[year_-2017])[wp];
    }

    static bool is_tagged(const pat::Jet& jet, int wp, bool old=false) {
      return discriminator(jet, old) > discriminator_min(wp, old);
    }
  };
}

#endif
