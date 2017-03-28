#ifndef JMTucker_MFVNeutralinoFormats_interface_TriggerFloats_h
#define JMTucker_MFVNeutralinoFormats_interface_TriggerFloats_h

namespace mfv {
  struct TriggerFloats {
    std::vector<float> l1jetspts;
    float l1htt;
    float myhtt;
    float myhttwbug;
    float ht;
    float ht4mc;
    std::vector<int> L1decisions;
    std::vector<int> HLTdecisions;
  };
}

#endif
