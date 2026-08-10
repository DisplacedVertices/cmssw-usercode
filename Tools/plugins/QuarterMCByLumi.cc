#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"

class QuarterMCByLumi : public edm::EDFilter {
public:
  explicit QuarterMCByLumi(const edm::ParameterSet&);

private:
  virtual bool filter(edm::Event&, const edm::EventSetup&);
  const unsigned n;
  const bool first;
  const bool second;
  const bool third;
  const bool fourth;
};

QuarterMCByLumi::QuarterMCByLumi(const edm::ParameterSet& cfg) 
  : n(cfg.getParameter<unsigned>("n")),
    first(cfg.getParameter<bool>("first")),
    second(cfg.getParameter<bool>("second")),
    third(cfg.getParameter<bool>("third")),
    fourth(cfg.getParameter<bool>("fourth"))
{
  if (n % 4 != 0) throw cms::Exception("n must be divisible by 4");
  printf("QuarterMCByLumi: n: %i first? %i second? %i third? %i fourth? %i \n", n, first, second, third, fourth);
}

bool QuarterMCByLumi::filter(edm::Event& event, const edm::EventSetup&) {

  int quarter_lumi_mod_n = (event.luminosityBlock() % n) / 4;

  if (first  && quarter_lumi_mod_n == 0) return true;
  if (second && quarter_lumi_mod_n == 1) return true;
  if (third  && quarter_lumi_mod_n == 2) return true;
  if (fourth && quarter_lumi_mod_n == 3) return true;

  return false;
}

DEFINE_FWK_MODULE(QuarterMCByLumi);
