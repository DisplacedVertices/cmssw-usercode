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

  const std::vector<double> binning;

  TH1F* h_npu;
};

PileupDist::PileupDist(const edm::ParameterSet& cfg)
  : binning(cfg.getParameter<std::vector<double> >("binning"))
{
  if (binning.size() != 3)
    throw cms::Exception("PileupDist", "binning must have three numbers");

  edm::Service<TFileService> fs;
  h_npu = fs->make<TH1F>("h_npu", "", int(binning[0]), binning[1], binning[2]);
}

void PileupDist::analyze(const edm::Event& event, const edm::EventSetup&) {
  if (event.isRealData())
    return;

  edm::Handle<std::vector<PileupSummaryInfo> > pileup;
  event.getByLabel("addPileupInfo", pileup);

  for (const PileupSummaryInfo& psi : *pileup)
    if (psi.getBunchCrossing() == 0)
      h_npu->Fill(psi.getTrueNumInteractions());
}

DEFINE_FWK_MODULE(PileupDist);
