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
  const int num_events;
  const double cross_section;
  const double partial_weight;
  const double lumi_weight;
  const edm::InputTag extra_weight_src;
};

SampleInfoProducer::SampleInfoProducer(const edm::ParameterSet& cfg)
  : sample(sample2number(cfg.getParameter<std::string>("sample"))),
    num_events(cfg.getParameter<int>("num_events")),
    cross_section(cfg.getParameter<double>("cross_section")),
    partial_weight(float(cross_section) / num_events),
    lumi_weight(partial_weight * cfg.getParameter<double>("int_lumi")),
    extra_weight_src(cfg.getParameter<edm::InputTag>("extra_weight_src"))
{
  produces<int>("sample");
  produces<int>("numEvents");
  produces<double>("crossSection");
  produces<double>("partialWeight");
  produces<double>("lumiWeight");
  produces<double>("extraWeight");
  produces<double>("weight");
}

void SampleInfoProducer::produce(edm::Event& event, const edm::EventSetup&) {
  std::auto_ptr<int> p_sample(new int(sample));
  std::auto_ptr<int> p_num_events(new int(num_events));
  std::auto_ptr<double> p_cross_section(new double(cross_section));
  std::auto_ptr<double> p_partial_weight(new double(partial_weight));
  std::auto_ptr<double> p_lumi_weight(new double(lumi_weight));
  std::auto_ptr<double> p_extra_weight(new double(1));
  std::auto_ptr<double> p_weight(new double(lumi_weight));

  if (extra_weight_src.label() != "") {
    edm::Handle<double> extra_weight;
    event.getByLabel(extra_weight_src, extra_weight);
    *p_extra_weight = *extra_weight;
    *p_weight *= *extra_weight;
  }

  event.put(p_sample, "sample");
  event.put(p_num_events, "numEvents");
  event.put(p_cross_section, "crossSection");
  event.put(p_partial_weight, "partialWeight");
  event.put(p_lumi_weight, "lumiWeight");
  event.put(p_extra_weight, "extraWeight");
  event.put(p_weight, "weight");
}

DEFINE_FWK_MODULE(SampleInfoProducer);
