#include "DataFormats/PatCandidates/interface/Jet.h"
#include "JMTucker/Tools/interface/BTagging.h"
#include "JMTucker/Tools/interface/Year.h"

namespace jmt {
  namespace BTagging {
    float discriminator_min(int wp, int tagger) {
      assert(wp >= 0 && wp <= 2);
      const float csv_mins[3]         = { 0.5803, 0.8838, 0.9693 }; // JMTBAD drop
      const float deepcsv_mins[2][3]  = { {0.1355, 0.4506, 0.7738}, {0.1208, 0.4168, 0.7665} };
      const float deepflav_mins[2][3] = { {0.0532, 0.3040, 0.7476}, {0.0490, 0.2783, 0.7100} };
      return (tagger==0 ? csv_mins : tagger==1 ? deepcsv_mins[jmt::Year::get()-2017] : deepflav_mins[jmt::Year::get()-2017])[wp];
    }

    bool is_tagged(double disc, int wp, int tagger) {
      return disc > discriminator_min(wp, tagger);
    }

    float discriminator(const pat::Jet& jet, int tagger) {
      if (tagger==0)
        return jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags"); // CSVv2
      else if (tagger==1)
        return jet.bDiscriminator("pfDeepCSVJetTags:probb") + jet.bDiscriminator("pfDeepCSVJetTags:probbb"); // DeepCSV
      else
        return jet.bDiscriminator("pfDeepFlavourJetTags:probb") + jet.bDiscriminator("pfDeepFlavourJetTags:probbb") + jet.bDiscriminator("pfDeepFlavourJetTags:problepb"); // DeepFlavour
    }

    bool is_tagged(const pat::Jet& jet, int wp, int tagger) {
      return is_tagged(discriminator(jet, tagger), wp, tagger);
    }
  }
}
