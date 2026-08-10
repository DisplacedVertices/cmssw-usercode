#include <iostream>
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Run.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/LHERunInfoProduct.h"

class JMTLHEGenInfo : public edm::EDAnalyzer {
public:
  explicit JMTLHEGenInfo(const edm::ParameterSet&);
private:
  virtual void endRun(const edm::Run&, const edm::EventSetup&) override;
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override;

  const bool use_lhe;
  const edm::EDGetTokenT<LHERunInfoProduct> lhe_run_token;
  const edm::EDGetTokenT<LHEEventProduct> lhe_event_token;
  const edm::EDGetTokenT<GenEventInfoProduct> gen_event_token;
  const std::string sep;
};

JMTLHEGenInfo::JMTLHEGenInfo(const edm::ParameterSet& cfg)
  : use_lhe(cfg.getParameter<bool>("use_lhe")),
    lhe_run_token(mayConsume<LHERunInfoProduct, edm::InRun>(edm::InputTag("externalLHEProducer"))),
    lhe_event_token(mayConsume<LHEEventProduct>(edm::InputTag("externalLHEProducer"))),
    gen_event_token(consumes<GenEventInfoProduct>(edm::InputTag("generator"))),
    sep("\n================================================================================\n")
{}

void JMTLHEGenInfo::endRun(const edm::Run& run, edm::EventSetup const&) {
  std::cout << sep << "JMTLHEGenInfo::endRun run " << run.id().run() << "\n";

  if (use_lhe) {
    edm::Handle<LHERunInfoProduct> lhe;
    run.getByToken(lhe_run_token, lhe);

    int count = 0;
    for (LHERunInfoProduct::headers_const_iterator it = lhe->headers_begin(); it != lhe->headers_end(); ++it, ++count) {
      std::cout << sep << "LHE run header #" << count << " tag " << it->tag() << " lines:\n";
      for (auto line : it->lines())
        std::cout << line;
    }

    if (lhe->comments_size()) {
      count = 0;
      for (LHERunInfoProduct::comments_const_iterator it = lhe->comments_begin(); it != lhe->comments_end(); ++it, ++count)
        std::cout << sep << "LHE run comment #" << count << " " << *it;
    }
    else
      std::cout << sep << "LHE run comments empty\n";
  }

  std::cout << sep << "JMTLHEGenInfo::endRun done\n";
}

void JMTLHEGenInfo::analyze(const edm::Event& event, const edm::EventSetup&) {
  std::cout << sep << "JMTLHEGenInfo::analyze run " << event.id().run() << " lumi " << event.luminosityBlock() << " event " << event.id().event() << "\n";

  int count = 0;

  if (use_lhe) {
    edm::Handle<LHEEventProduct> lhe;
    event.getByToken(lhe_event_token, lhe);

    if (lhe->comments_size())
      for (LHERunInfoProduct::comments_const_iterator it = lhe->comments_begin(); it != lhe->comments_end(); ++it, ++count)
        std::cout << sep << "LHE event comment #" << count << " " << *it;
    else
      std::cout << sep << "LHE event comments empty\n";

    std::cout << sep << "LHE event stuff:\nnpLO = " << lhe->npLO() << " npNLO = " << lhe->npNLO() << " originalXWGTUP = " << lhe->originalXWGTUP() << "\n";

    if (lhe->pdf())
      std::cout << "PDF info: id = " << lhe->pdf()->id.first << "," << lhe->pdf()->id.second
                << " x = " << lhe->pdf()->x.first << "," << lhe->pdf()->x.second
                << " xPDF = " << lhe->pdf()->xPDF.first << "," << lhe->pdf()->xPDF.second
                << " scalePDF = " << lhe->pdf()->scalePDF << "\n";
    else
      std::cout << "PDF info empty\n";

    std::cout << "scales (#=" << lhe->scales().size() << "):\n";
    count = 0;
    for (auto s : lhe->scales())
      std::cout << "  s #" << std::setw(4) << count++ << ": " << s << "\n";

    std::cout << "weights (#=" << lhe->weights().size() << "):\n";
    count = 0;
    for (auto w : lhe->weights())
      std::cout << "  w #" << std::setw(4) << count++ << ": '" << w.id << "' = " << w.wgt << " (" << w.wgt / lhe->originalXWGTUP() << ")\n";
  }

  edm::Handle<GenEventInfoProduct> gen;
  event.getByToken(gen_event_token, gen);

  std::cout << sep << "GenEventInfo stuff:\nqScale = " << gen->qScale() << " alphaQCD = " << gen->alphaQCD() << " alphaQED = " << gen->alphaQED() << " nMEPartons = " << gen->nMEPartons() << " nMEPartonsFiltered = " << gen->nMEPartonsFiltered() << "\n";

  if (gen->pdf())
    std::cout << "PDF info: id = " << gen->pdf()->id.first << "," << gen->pdf()->id.second
              << " x = " << gen->pdf()->x.first << "," << gen->pdf()->x.second
              << " xPDF = " << gen->pdf()->xPDF.first << "," << gen->pdf()->xPDF.second
              << " scalePDF = " << gen->pdf()->scalePDF << "\n";
  else
    std::cout << "PDF info empty\n";

  std::cout << "weights (#=" << gen->weights().size() << "):\n";
  count = 0;
  for (auto w : gen->weights())
    std::cout << "  w #" << std::setw(4) << count++ << ": " << w << "\n";

  std::cout << sep << "JMTLHEGenInfo::analyze done\n";
}

DEFINE_FWK_MODULE(JMTLHEGenInfo);
