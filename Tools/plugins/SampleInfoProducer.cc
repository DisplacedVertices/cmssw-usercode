#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"

class SampleInfoProducer : public edm::EDProducer {
public:
  explicit SampleInfoProducer(const edm::ParameterSet&);

private:
  virtual void produce(edm::Event&, const edm::EventSetup&);

  int sample2number(const std::string& sample) const {
    const std::vector<std::string> samples = {
      "qcdht0100", "qcdht0250", "qcdht0500", "qcdht1000", "ttbarhadronic", "ttbarsemilep", "ttbardilep"
    };
    int num = -1;
    const auto it = std::find(samples.begin(), samples.end(), sample);
    if (it != samples.end())
      num = int(it - samples.begin());
    return num;
  }

  const int sample;
  const int numEvents;
  const double crossSection;
  const double partialWeight;
  const double intLumi;
  const double weight;
};

SampleInfoProducer::SampleInfoProducer(const edm::ParameterSet& cfg)
  : sample(sample2number(cfg.getParameter<std::string>("sample"))),
    numEvents(cfg.getParameter<int>("numEvents")),
    crossSection(cfg.getParameter<double>("crossSection")),
    partialWeight(float(crossSection) / numEvents),
    intLumi(cfg.getParameter<double>("intLumi")),
    weight(partialWeight * intLumi)
{
  produces<int>("sample");
  produces<int>("numEvents");
  produces<double>("crossSection");
  produces<double>("weight");
}

void SampleInfoProducer::produce(edm::Event& event, const edm::EventSetup&) {
  std::auto_ptr<int> p_sample(new int(sample));
  std::auto_ptr<int> p_numEvents(new int(numEvents));
  std::auto_ptr<double> p_crossSection(new double(crossSection));
  std::auto_ptr<double> p_weight(new double(weight));

  event.put(p_sample, "sample");
  event.put(p_numEvents, "numEvents");
  event.put(p_crossSection, "crossSection");
  event.put(p_weight, "weight");
}

DEFINE_FWK_MODULE(SampleInfoProducer);
