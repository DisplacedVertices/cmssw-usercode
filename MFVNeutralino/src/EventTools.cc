#include "JMTucker/MFVNeutralino/interface/EventTools.h"
#include "JMTucker/Tools/interface/TriggerHelper.h"

namespace mfv {
  void trigger_decision(const TriggerHelper& trig, bool* pass_trigger) {
    pass_trigger[0] = trig.pass_any_version("HLT_QuadJet50_v");
    pass_trigger[1] = trig.pass_any_version("HLT_IsoMu24_v");
    pass_trigger[2] = trig.pass_any_version("HLT_HT750_v");
    pass_trigger[3] = trig.pass_any_version("HLT_IsoMu24_eta2p1_v");
    pass_trigger[4] = 
      trig.pass_any_version("HLT_IsoMu20_eta2p1_TriCentralPFJet30_v", false) ||
      trig.pass_any_version("HLT_IsoMu20_eta2p1_TriCentralPFNoPUJet30_v", false) ||
      trig.pass_any_version("HLT_IsoMu17_eta2p1_TriCentralPFNoPUJet30_v", false) ||
      trig.pass_any_version("HLT_IsoMu17_eta2p1_TriCentralPFNoPUJet30_30_20_v", false);
  }
}
