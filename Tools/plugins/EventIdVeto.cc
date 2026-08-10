#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"

class EventIdVeto : public edm::EDFilter {
public:
  explicit EventIdVeto(const edm::ParameterSet&);

private:
  virtual bool filter(edm::Event&, const edm::EventSetup&);

  typedef std::pair<unsigned, unsigned long long> LE;
  typedef std::tuple<unsigned, unsigned, unsigned long long> RLE;
  std::set<LE> mle;
  std::set<RLE> mrle;

  const bool use_run;
  const bool debug;
};

EventIdVeto::EventIdVeto(const edm::ParameterSet& cfg) 
  : use_run(cfg.getParameter<bool>("use_run")),
    debug(cfg.getUntrackedParameter<bool>("debug", false))
{
  std::string fn(cfg.getParameter<std::string>("list_fn"));

  if (fn.size()) {
    printf("EventIdVeto: fn is %s\n", fn.c_str());
    if (fn.length() > 3 && fn.compare(fn.length() - 3, 3, ".gz") == 0) {
      printf("EventIdVeto: gunzipping\n");
      if (system(("gunzip " + fn).c_str()) != 0)
        throw cms::Exception("EventIdVeto") << "could not unzip file " << fn;
      fn.erase(fn.length() - 3, 3);
    }

    FILE* f = fopen(fn.c_str(), "rt");
    if (!f)
      throw cms::Exception("EventIdVeto") << "could not read file " << fn;

    char line[1024];
    while (fgets(line, 1024, f) != 0) {
      if (debug) printf("EventIdVeto debug: file line read: %s", line);
      unsigned r,l;
      unsigned long long e;
      int res;
      if (use_run)
        res = sscanf(line, "(%u,%u,%llu),", &r, &l, &e);
      else
        res = sscanf(line, "(%u,%llu),", &l, &e);
      if (debug) printf("    sscanf returned %i, r,l,e = %u, %u, %llu\n", res, r,l,e);
      if (res != (use_run ? 3 : 2))
        continue;
      if (use_run)
        mrle.insert(RLE(r,l,e));
      else
        mle.insert(LE(l,e));
    }
    fclose(f);
  }
  else {
    const std::vector<unsigned> lumis = cfg.getParameter<std::vector<unsigned>>("lumis");
    const size_t n = lumis.size();
    const std::vector<unsigned long long> events = cfg.getParameter<std::vector<unsigned long long>>("events");
    const std::vector<unsigned> runs = use_run ? cfg.getParameter<std::vector<unsigned>>("runs") : std::vector<unsigned>();

    if ((use_run && runs.size() != n) || events.size() != n)
      throw cms::Exception("EventIdVeto", "mismatched sizes");

    for (size_t i = 0; i < n; ++i)
      if (use_run)
        mrle.insert(RLE(runs[i], lumis[i], events[i]));
      else
        mle.insert(LE(lumis[i], events[i]));
  }

  const size_t nveto = use_run ? mrle.size() : mle.size();
  if (nveto == 0)
    throw cms::Exception("EventIdVeto") << "found zero events to veto in file " << fn;
  printf("EventIdVeto: vetoing %lu events\n", nveto);
}

bool EventIdVeto::filter(edm::Event& event, const edm::EventSetup&) {
  if (use_run)
    return mrle.find(RLE(event.id().run(),
                         event.luminosityBlock(),
                         event.id().event())) == mrle.end();
  else
    return mle.find(LE(event.luminosityBlock(),
                       event.id().event())) == mle.end();
}

DEFINE_FWK_MODULE(EventIdVeto);
