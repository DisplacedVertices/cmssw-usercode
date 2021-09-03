#include "TH2.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DVCode/MFVNeutralinoFormats/interface/Event.h"
#include "DVCode/MFVNeutralinoFormats/interface/VertexAux.h"

class NmxHistos : public edm::EDAnalyzer {
 public:
  explicit NmxHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::InputTag weight_src;
  const bool use_weight;
  const std::vector<edm::InputTag> vertex_srcs;
  const size_t n;

  TH2F* h_nsv;
};

NmxHistos::NmxHistos(const edm::ParameterSet& cfg)
  : weight_src(cfg.getParameter<edm::InputTag>("weight_src")),
    use_weight(cfg.getParameter<bool>("use_weight")),
    vertex_srcs(cfg.getParameter<std::vector<edm::InputTag> >("vertex_srcs")),
    n(vertex_srcs.size())
{
  edm::Service<TFileService> fs;

  h_nsv = fs->make<TH2F>("h_nsv", "", n, 0, n, 20, 0, 20);
  TAxis* xax = h_nsv->GetXaxis();
  for (size_t i = 0; i < n; ++i) {
    xax->SetBinLabel(i+1, vertex_srcs[i].label().c_str());
  }
}

void NmxHistos::analyze(const edm::Event& event, const edm::EventSetup&) {
  double w = 1;
  if (use_weight) {
    edm::Handle<double> weight;
    event.getByLabel(weight_src, weight);
    w = *weight;
  }

  for (size_t i = 0; i < n; ++i) {
    edm::Handle<MFVVertexAuxCollection> vertices;
    event.getByLabel(vertex_srcs[i], vertices);

    const int nsv = int(vertices->size());
    h_nsv->Fill(i, nsv, w);
  }
}

DEFINE_FWK_MODULE(NmxHistos);
