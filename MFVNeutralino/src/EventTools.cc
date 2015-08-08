#include "JMTucker/MFVNeutralino/interface/EventTools.h"
#include "JMTucker/Tools/interface/TriggerHelper.h"

namespace mfv {
  void trigger_decision(const TriggerHelper& trig, bool* pass_trigger) {
    std::vector<std::string> paths({
        "HLT_PFHT650_v",
        "HLT_PFHT550_4Jet_v",
        "HLT_PFHT450_SixJet40_PFBTagCSV_v",
        "HLT_PFHT400_SixJet30_BTagCSV0p5_2PFBTagCSV_v",
        "HLT_PFHT450_SixJet40_v",
        "HLT_PFHT400_SixJet30_v",
        "HLT_QuadJet45_TripleCSV0p5_v",
        "HLT_QuadJet45_DoubleCSV0p5_v",
        "HLT_DoubleJet90_Double30_TripleCSV0p5_v",
        "HLT_DoubleJet90_Double30_DoubleCSV0p5_v",
        "HLT_HT650_DisplacedDijet80_Inclusive_v",
        "HLT_HT750_DisplacedDijet80_Inclusive_v",
        "HLT_HT500_DisplacedDijet40_Inclusive_v",
        "HLT_HT550_DisplacedDijet40_Inclusive_v",
        "HLT_HT350_DisplacedDijet40_DisplacedTrack_v",
        "HLT_HT350_DisplacedDijet80_DisplacedTrack_v",
        "HLT_HT350_DisplacedDijet80_Tight_DisplacedTrack_v"
        });
    assert(paths.size() == 17);
    for (size_t i = 0; i < 17; ++i)
      pass_trigger[i] = trig.pass_any_version(paths[i]);
  }
}
