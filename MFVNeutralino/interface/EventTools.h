#ifndef JMTucker_MFVNeutralino_interface_EventTools_h
#define JMTucker_MFVNeutralino_interface_EventTools_h

class TriggerHelper;

namespace mfv {
  void trigger_decision(const TriggerHelper& trig, bool* pass_trigger);
}

#endif
