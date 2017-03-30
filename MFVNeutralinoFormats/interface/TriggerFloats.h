#ifndef JMTucker_MFVNeutralinoFormats_interface_TriggerFloats_h
#define JMTucker_MFVNeutralinoFormats_interface_TriggerFloats_h

#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"

namespace mfv {
  struct TriggerFloats {
    std::vector<float> l1jetspts;
    float l1htt;
    float myhtt;
    float myhttwbug;
    float hltht;
    float hltht4mc;
    std::vector<int> L1decisions;
    std::vector<int> HLTdecisions;

    TriggerFloats()
      : l1htt(-1), myhtt(-1), myhttwbug(-1), hltht(-1), hltht4mc(-1),
        L1decisions(n_l1_paths, -1),
        HLTdecisions(n_hlt_paths, -1)
    {}
  };
}

#endif
