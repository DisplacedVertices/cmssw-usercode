#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DVCode/MFVNeutralinoFormats/interface/Event.h"
#include "DVCode/MFVNeutralinoFormats/interface/VertexAux.h"

class MFVSizeof : public edm::EDAnalyzer {
public:
  explicit MFVSizeof(const edm::ParameterSet&) {
    printf("MFVSizeof:\nevent  : %lu\nvtx aux: %lu\n", sizeof(MFVEvent), sizeof(MFVVertexAux));
  }

  void analyze(const edm::Event&, const edm::EventSetup&) {}
};

DEFINE_FWK_MODULE(MFVSizeof);
