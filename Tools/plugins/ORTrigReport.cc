#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DVCode/Tools/interface/TriggerHelper.h"

// The normal TrigReport doesn't state how many events are written
// total to the file in case of OutputModule's SelectEvents having
// multiple paths (i.e. when you are writing an event depending on the
// OR of the paths). Add a summary block to stdout that so that it is
// easy to see what the total number of events should be, useful for
// sanity check on tupling batch jobs.

class ORTrigReport : public edm::EDAnalyzer {
public:
  explicit ORTrigReport(const edm::ParameterSet&);

private:
  const edm::InputTag results_src;
  const std::vector<std::string> paths;

  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob();

  int run, passed, not_found;
};

ORTrigReport::ORTrigReport(const edm::ParameterSet& cfg) 
  : results_src(cfg.getParameter<edm::InputTag>("results_src")),
    paths(cfg.getParameter<std::vector<std::string> >("paths"))
{
  run = passed = not_found = 0;
}

void ORTrigReport::analyze(const edm::Event& event, const edm::EventSetup&) {
  run += 1;

  edm::Handle<edm::TriggerResults> trigger_results;
  event.getByLabel(results_src, trigger_results);
  TriggerHelper h(*trigger_results, event.triggerNames(*trigger_results));
 
  bool pass = false, found = false, one_found = false;

  for (size_t i = 0, ie = paths.size(); i < ie; ++i) {
    pass = pass || h.pass(paths[i], found);
    if (found)
      one_found = true;
    found = false;
  }

  if (!one_found) {
    assert(!pass);
    not_found += 1;
  }
  else if (pass)
    passed += 1;
}

void ORTrigReport::endJob() {
  printf("\n");
  printf("TrigReport ---------- MyOR   Summary ------------\n");
  printf("TrigReport  Trig Bit#        Run     Passed     Failed      Error Name\n");
  printf("TrigReport     0 9999 %10i %10i %10i %10i pMyOR\n", run, passed, run - passed - not_found, not_found);
  printf("\n");
  fflush(stdout);
}

DEFINE_FWK_MODULE(ORTrigReport);
