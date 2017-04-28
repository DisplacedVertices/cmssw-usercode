#include "TH2.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"

class PileupDist : public edm::EDAnalyzer {
public:
  explicit PileupDist(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  const edm::EDGetTokenT<reco::VertexCollection> primary_vertex_token;
  const edm::EDGetTokenT<std::vector<PileupSummaryInfo> > pileup_info_token;

  TH1D* h_npv;
  TH1D* h_ngoodpv;
  TH1D* h_npu;
  TH2D* h_npv_v_npu;
  TH2D* h_ngoodpv_v_npu;
};

PileupDist::PileupDist(const edm::ParameterSet& cfg)
  : primary_vertex_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("primary_vertices_src"))),
    pileup_info_token(consumes<std::vector<PileupSummaryInfo>>(cfg.getParameter<edm::InputTag>("pileup_info_src")))
{
  edm::Service<TFileService> fs;
  const int nmax = 100;
  h_npv = fs->make<TH1D>("h_npv", "", nmax, 0, nmax);
  h_ngoodpv = fs->make<TH1D>("h_ngoodpv", "", nmax, 0, nmax);
  h_npu = fs->make<TH1D>("h_npu", "", nmax, 0, nmax);
  h_npv_v_npu = fs->make<TH2D>("h_npv_v_npu", "", nmax, 0, nmax, nmax, 0, nmax);
  h_ngoodpv_v_npu = fs->make<TH2D>("h_ngoodpv_v_npu", "", nmax, 0, nmax, nmax, 0, nmax);
}

void PileupDist::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByToken(primary_vertex_token, primary_vertices);

  const int npv = int(primary_vertices->size());
  const int ngoodpv = count_if(primary_vertices->begin(), primary_vertices->end(), [](const reco::Vertex& v) { return !v.isFake() && v.ndof() > 4 && fabs(v.z()) <= 24 && v.position().rho() < 2; });

  h_npv->Fill(npv);
  h_ngoodpv->Fill(ngoodpv);

  if (!event.isRealData()) {
    edm::Handle<std::vector<PileupSummaryInfo> > pileup_info;
    event.getByToken(pileup_info_token, pileup_info);

    double npu = -1;
    for (const PileupSummaryInfo& psi : *pileup_info)
      if (psi.getBunchCrossing() == 0) {
        if (npu >= 0)
          throw cms::Exception("BadAssumption", "two psi with bx = 0?");
        npu = psi.getTrueNumInteractions();
      }

    h_npu->Fill(npu);
    h_npv_v_npu->Fill(npu, npv);
    h_ngoodpv_v_npu->Fill(npu, ngoodpv);
  }
}

DEFINE_FWK_MODULE(PileupDist);
