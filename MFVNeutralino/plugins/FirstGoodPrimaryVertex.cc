#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"

class MFVFirstGoodPrimaryVertex : public edm::EDProducer {
public:
  explicit MFVFirstGoodPrimaryVertex(const edm::ParameterSet&);
private:
  virtual void produce(edm::Event&, const edm::EventSetup&);
  const edm::EDGetTokenT<reco::VertexCollection> vertices_token;
};

MFVFirstGoodPrimaryVertex::MFVFirstGoodPrimaryVertex(const edm::ParameterSet& cfg)
  : vertices_token(consumes<reco::VertexCollection>(edm::InputTag("offlinePrimaryVertices")))
{
  produces<reco::VertexCollection>();
}

void MFVFirstGoodPrimaryVertex::produce(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<reco::VertexCollection> vertices;
  event.getByToken(vertices_token, vertices);
  
  std::unique_ptr<reco::VertexCollection> output(new reco::VertexCollection);

  for (const reco::Vertex& v : *vertices)
    if (!v.isFake() && v.ndof() > 4 && fabs(v.z()) <= 24 && v.position().rho() < 2) {
      output->push_back(v);
      break;
    }

  event.put(std::move(output));
}

DEFINE_FWK_MODULE(MFVFirstGoodPrimaryVertex);
