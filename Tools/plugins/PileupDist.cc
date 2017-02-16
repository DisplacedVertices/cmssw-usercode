#include "TH1F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"

class PileupDist : public edm::EDAnalyzer {
public:
  explicit PileupDist(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  const edm::EDGetTokenT<std::vector<PileupSummaryInfo> > pileup_info_token;
  const std::vector<double> binning;

  TH1F* h_npu;
};

PileupDist::PileupDist(const edm::ParameterSet& cfg)
  : pileup_info_token(consumes<std::vector<PileupSummaryInfo>>(cfg.getParameter<edm::InputTag>("pileup_info_src"))),
    binning(cfg.getParameter<std::vector<double>>("binning"))
{
  if (binning.size() != 3)
    throw cms::Exception("PileupDist", "binning must have three numbers");

  edm::Service<TFileService> fs;
  h_npu = fs->make<TH1F>("h_npu", "", int(binning[0]), binning[1], binning[2]);
}

void PileupDist::analyze(const edm::Event& event, const edm::EventSetup&) {
  if (event.isRealData())
    return;

  edm::Handle<std::vector<PileupSummaryInfo> > pileup_info;
  event.getByToken(pileup_info_token, pileup_info);

  for (const PileupSummaryInfo& psi : *pileup_info)
    if (psi.getBunchCrossing() == 0)
      h_npu->Fill(psi.getTrueNumInteractions());
}

DEFINE_FWK_MODULE(PileupDist);
