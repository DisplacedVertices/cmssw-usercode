#ifndef JMTucker_Tools_TriggerHelper_h
#define JMTucker_Tools_TriggerHelper_h

#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Common/interface/TriggerNames.h"

struct TriggerHelper {
  const edm::TriggerResults& trigger_results;
  const edm::TriggerNames& trigger_names;

  TriggerHelper(const edm::TriggerResults& trigger_results_, const edm::TriggerNames& trigger_names_) : trigger_results(trigger_results_), trigger_names(trigger_names_) {}

  bool pass(const char* name, bool& found, const bool debug=false) const {
    const unsigned ndx = trigger_names.triggerIndex(name);
    found = ndx < trigger_results.size();
    if (debug) {
      printf("TriggerHelper debug\nname: %s\n", name);
      printf("names size: %lu\n", trigger_names.size());
      for (size_t i = 0, ie= trigger_names.size(); i < ie; ++i)
	printf("name %lu: %s\n", i, trigger_names.triggerName(i).c_str());
      printf("ndx: %u => name %s found? %i\n", ndx, name, found);
      if (found)
	printf("trigger fired? %i\n", trigger_results.accept(ndx));
      printf("done.\n");
    }
    return found ? trigger_results.accept(ndx) : false;
  }

  bool pass(const char* name) const {
    bool found = false;
    bool result = pass(name, found);
    if (!found)
      throw cms::Exception("TriggerHelper") << "no trigger with name " << name << " found\n";
    return result;
  }
   
  bool pass(const char* fmt, int range_lo, int range_hi) const {
    char name[512];
    for (int i = range_lo; i <= range_hi; ++i) {
      snprintf(name, 512, fmt, i);
      bool found = false;
      bool result = pass(name, found);
      if (found)
	return result;
    }
    throw cms::Exception("TriggerHelper") << "no trigger for fmt " << fmt << " range " << range_lo << "-" << range_hi << " found";
  }
};

#endif
