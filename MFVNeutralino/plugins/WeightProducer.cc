#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"

class MFVWeightProducer : public edm::EDProducer {
public:
  explicit MFVWeightProducer(const edm::ParameterSet&);
  void produce(edm::Event&, const edm::EventSetup&);

private:
  const edm::InputTag mevent_src;
  const bool enable;
  const bool prints;

  const bool weight_pileup;
  const std::vector<double> pileup_weights;
  double pileup_weight(int mc_npu) const;

  enum { sum_pileup_weight, sum_weight, n_sums };
  TH1F* h_sums;
};

MFVWeightProducer::MFVWeightProducer(const edm::ParameterSet& cfg)
  : mevent_src(cfg.getParameter<edm::InputTag>("mevent_src")),
    enable(cfg.getParameter<bool>("enable")),
    prints(cfg.getUntrackedParameter<bool>("prints", false)),
    weight_pileup(cfg.getParameter<bool>("weight_pileup")),
    pileup_weights(cfg.getParameter<std::vector<double> >("pileup_weights"))
{
  produces<double>();

  edm::Service<TFileService> fs;
  TH1::SetDefaultSumw2();
  h_sums = fs->make<TH1F>("h_sums", "", n_sums+1, 0, n_sums+1);
}

double MFVWeightProducer::pileup_weight(int mc_npu) const {
  if (mc_npu < 0 || mc_npu > int(pileup_weights.size()))
    return 0;
  else
    return pileup_weights[mc_npu];
}

void MFVWeightProducer::produce(edm::Event& event, const edm::EventSetup&) {
  h_sums->Fill(n_sums);

  edm::Handle<MFVEvent> mevent;
  event.getByLabel(mevent_src, mevent);

  std::auto_ptr<double> weight(new double);
  *weight = 1;

  if (enable) {
    if (!event.isRealData()) {
      if (weight_pileup) {
        const double pu_w = pileup_weight(mevent->npu);
        h_sums->Fill(sum_pileup_weight, pu_w);
        *weight *= pu_w;
      }
    }
  }

  h_sums->Fill(sum_weight, *weight);

  if (prints)
    printf("MFVWeight: r,l,e: %u, %u, %u   weight: %g\n", event.id().run(), event.luminosityBlock(), event.id().event(), *weight);

  event.put(weight);
}

DEFINE_FWK_MODULE(MFVWeightProducer);
