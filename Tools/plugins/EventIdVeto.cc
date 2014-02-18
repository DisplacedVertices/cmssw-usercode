#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"

class EventIdVeto : public edm::EDFilter {
public:
  explicit EventIdVeto(const edm::ParameterSet&);

private:
  virtual bool filter(edm::Event&, const edm::EventSetup&);

  typedef std::pair<unsigned, unsigned> LE;
  typedef std::tuple<unsigned, unsigned, unsigned> RLE;
  std::set<LE> mle;
  std::set<RLE> mrle;

  const bool use_run;
};

EventIdVeto::EventIdVeto(const edm::ParameterSet& cfg) 
  : use_run(cfg.getParameter<bool>("use_run"))
{
  const std::string& fn(cfg.getParameter<std::string>("list_fn"));
  FILE* f = fopen(fn.c_str(), "rt");
  if (!f)
    throw cms::Exception("EventIdVeto") << "could not read file " << fn;

  char line[1024];
  while (fgets(line, 1024, f) != 0) {
    unsigned r,l,e;
    if (sscanf(line, "(%u,%u,%u),", &r, &l, &e) != 3)
      continue;
    if (use_run)
      mrle.insert(RLE(r,l,e));
    else
      mle.insert(LE(l,e));
  }
  fclose(f);

  printf("EventIdVeto: vetoing %lu events\n", (use_run ? mrle.size() : mle.size()));
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
