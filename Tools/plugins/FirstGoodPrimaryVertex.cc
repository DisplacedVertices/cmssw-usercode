#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"

class JMTFirstGoodPrimaryVertex : public edm::EDFilter {
public:
  explicit JMTFirstGoodPrimaryVertex(const edm::ParameterSet&);
private:
  virtual bool filter(edm::Event&, const edm::EventSetup&) override;
  const edm::EDGetTokenT<reco::VertexCollection> vertices_token;
  const bool cut;
};

JMTFirstGoodPrimaryVertex::JMTFirstGoodPrimaryVertex(const edm::ParameterSet& cfg)
  : vertices_token(consumes<reco::VertexCollection>(edm::InputTag("offlinePrimaryVertices"))),
    cut(cfg.getParameter<bool>("cut"))
{
  produces<reco::VertexCollection>();
  produces<int>("nAll");
  produces<int>("nGood");
}

bool JMTFirstGoodPrimaryVertex::filter(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<reco::VertexCollection> vertices;
  event.getByToken(vertices_token, vertices);
  
  std::unique_ptr<reco::VertexCollection> output(new reco::VertexCollection);
  std::unique_ptr<int> nall(new int(vertices->size()));
  std::unique_ptr<int> ngood(new int(0));

  for (const reco::Vertex& v : *vertices) {
    if (!v.isFake() && v.ndof() > 4 && fabs(v.z()) <= 24 && v.position().rho() < 2) {
      if (output->empty()) output->push_back(v);
      ++(*ngood);
    }
  }

  const bool pass = !cut || *ngood > 0;
  event.put(std::move(output));
  event.put(std::move(nall), "nAll");
  event.put(std::move(ngood), "nGood");
  return pass;
}

DEFINE_FWK_MODULE(JMTFirstGoodPrimaryVertex);
