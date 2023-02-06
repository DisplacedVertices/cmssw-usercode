#include "DataFormats/PatCandidates/interface/Jet.h"
#include "JMTucker/Tools/interface/BTagging.h"
#include "JMTucker/Tools/interface/Year.h"

// Pre-VFP numbers
// DeepCSV:  0.2027, 0.6001, 0.8819
// DeepFlav: 0.0508, 0.2598, 0.6502
//
// Post-VFP numbers
// DeepCSV:  0.1918, 0.5847, 0.8767
// DeepFlav: 0.0480, 0.2489, 0.6377

namespace jmt {
  namespace BTagging {
    float discriminator_min(int wp, int tagger) {
      assert(wp >= 0 && wp <= 2);
      int idx = jmt::Year::get() == 20161 ? 0 : jmt::Year::get() == 20162 ? 1 : jmt::Year::get() == 2017 ? 2 : 3;
      const float csv_mins[4][3]      = { {0.4600, 0.8000, 0.9350}, {0.4600, 0.8000, 0.9350}, {0.5803, 0.8838, 0.9693}, {0.5803, 0.8838, 0.9693} }; // JMTBAD drop
      const float deepcsv_mins[4][3]  = { {0.2027, 0.6001, 0.8819}, {0.1918, 0.5847, 0.8767}, {0.1355, 0.4506, 0.7738}, {0.1208, 0.4168, 0.7665} };
      const float deepflav_mins[4][3] = { {0.0508, 0.2598, 0.6502}, {0.0480, 0.2489, 0.6377}, {0.0532, 0.3040, 0.7476}, {0.0490, 0.2783, 0.7100} };
      
      // if we get an invalid tagger options (e.g. not 0 or 1) default to use deepflav, since it's the recommendation
      return (tagger==0 ? csv_mins[idx] : tagger==1 ? deepcsv_mins[idx] : deepflav_mins[idx])[wp];
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
