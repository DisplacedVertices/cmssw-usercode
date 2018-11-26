#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"

class JMTNpuFilter : public edm::EDFilter {
public:
  explicit JMTNpuFilter(const edm::ParameterSet&);
private:
  bool filter(edm::Event&, const edm::EventSetup&) override;

  const edm::EDGetTokenT<std::vector<PileupSummaryInfo> > pileup_info_token;

  const double min_npu;
  const double max_npu;
};

JMTNpuFilter::JMTNpuFilter(const edm::ParameterSet& cfg)
  : pileup_info_token(consumes<std::vector<PileupSummaryInfo>>(cfg.getParameter<edm::InputTag>("pileup_info_src"))),
    min_npu(cfg.getParameter<double>("min_npu")),
    max_npu(cfg.getParameter<double>("max_npu"))
{
}

bool JMTNpuFilter::filter(edm::Event& event, const edm::EventSetup&) {
  if (event.isRealData())
    return true;

  edm::Handle<std::vector<PileupSummaryInfo> > pileup_info;
  event.getByToken(pileup_info_token, pileup_info);

  double npu = -1;
  for (const PileupSummaryInfo& psi : *pileup_info)
    if (psi.getBunchCrossing() == 0) {
      if (npu >= 0)
        throw cms::Exception("BadAssumption", "two psi with bx = 0?");
      npu = psi.getTrueNumInteractions();
    }

  return npu >= min_npu && npu < max_npu;
}

DEFINE_FWK_MODULE(JMTNpuFilter);
