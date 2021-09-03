#include "TH1.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DVCode/MFVNeutralinoFormats/interface/Event.h"
#include "DVCode/MFVNeutralinoFormats/interface/VertexAux.h"

class MFVBQuarkCount : public edm::EDAnalyzer {
 public:
  explicit MFVBQuarkCount(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::EDGetTokenT<MFVEvent> event_token;
  const edm::EDGetTokenT<double> weight_token;
  const edm::EDGetTokenT<MFVVertexAuxCollection> vertex_token;

  TH1F* h;
};

MFVBQuarkCount::MFVBQuarkCount(const edm::ParameterSet& cfg)
  : event_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("event_src"))),
    weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
    vertex_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertex_src")))
{
  edm::Service<TFileService> fs;
  h = fs->make<TH1F>("h", "", 24, 1, 25);
}

void MFVBQuarkCount::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<MFVEvent> mevent;
  event.getByToken(event_token, mevent);

  //edm::Handle<double> weight;
  //event.getByToken(weight_token, weight);
  //const double w = *weight;

  edm::Handle<MFVVertexAuxCollection> vertices;
  event.getByToken(vertex_token, vertices);
  const size_t nsv = vertices->size();

  const size_t n_gen_bquark = mevent->gen_bquarks.size();
  size_t n_gen_bquark_accept = 0;
  for (size_t i = 0; i < n_gen_bquark; ++i)
    if (mevent->gen_bquarks[i].Pt() > 5 && fabs(mevent->gen_bquarks[i].Eta()) < 2.5)
      ++n_gen_bquark_accept;

  if (1)        h->Fill(1);
  if (nsv == 1) h->Fill(2);
  if (nsv >= 2) h->Fill(3);
  if (mevent->gen_flavor_code == 2)             h->Fill(4);
  if (mevent->gen_flavor_code == 2 && nsv == 1) h->Fill(5);
  if (mevent->gen_flavor_code == 2 && nsv >= 2) h->Fill(6);
  if (n_gen_bquark == 1)             h->Fill(7);
  if (n_gen_bquark == 1 && nsv == 1) h->Fill(8);
  if (n_gen_bquark == 1 && nsv >= 2) h->Fill(9);
  if (n_gen_bquark == 2)             h->Fill(10);
  if (n_gen_bquark == 2 && nsv == 1) h->Fill(11);
  if (n_gen_bquark == 2 && nsv >= 2) h->Fill(12);
  if (n_gen_bquark > 2)             h->Fill(13);
  if (n_gen_bquark > 2 && nsv == 1) h->Fill(14);
  if (n_gen_bquark > 2 && nsv >= 2) h->Fill(15);
  if (n_gen_bquark_accept == 1)             h->Fill(16);
  if (n_gen_bquark_accept == 1 && nsv == 1) h->Fill(17);
  if (n_gen_bquark_accept == 1 && nsv >= 2) h->Fill(18);
  if (n_gen_bquark_accept == 2)             h->Fill(19);
  if (n_gen_bquark_accept == 2 && nsv == 1) h->Fill(20);
  if (n_gen_bquark_accept == 2 && nsv >= 2) h->Fill(21);
  if (n_gen_bquark_accept > 2)             h->Fill(22);
  if (n_gen_bquark_accept > 2 && nsv == 1) h->Fill(23);
  if (n_gen_bquark_accept > 2 && nsv >= 2) h->Fill(24);
}

DEFINE_FWK_MODULE(MFVBQuarkCount);
