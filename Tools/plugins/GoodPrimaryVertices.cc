#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"

class JMTGoodPrimaryVertices : public edm::EDFilter {
public:
  explicit JMTGoodPrimaryVertices(const edm::ParameterSet&);
private:
  virtual bool filter(edm::Event&, const edm::EventSetup&) override;

  const bool input_is_miniaod;
  const edm::EDGetTokenT<reco::VertexCollection> vertices_token;
  const edm::EDGetTokenT<edm::ValueMap<float>> scores_token;
  const unsigned nfirst;
  const bool cut;
};

JMTGoodPrimaryVertices::JMTGoodPrimaryVertices(const edm::ParameterSet& cfg)
  : input_is_miniaod(cfg.getParameter<bool>("input_is_miniaod")),
    vertices_token(consumes<reco::VertexCollection>(edm::InputTag(input_is_miniaod ? "offlineSlimmedPrimaryVertices" : "offlinePrimaryVertices"))),
    scores_token(consumes<edm::ValueMap<float>>(input_is_miniaod ? edm::InputTag("offlineSlimmedPrimaryVertices") : edm::InputTag("primaryVertexAssociation", "original"))),
    nfirst(cfg.getParameter<unsigned>("nfirst")),
    cut(cfg.getParameter<bool>("cut"))
{
  produces<int>("nAll");
  produces<int>("nGood");
  produces<reco::VertexCollection>();
  produces<edm::ValueMap<float>>();
}

bool JMTGoodPrimaryVertices::filter(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<reco::VertexCollection> vertices;
  event.getByToken(vertices_token, vertices);

  edm::Handle<edm::ValueMap<float>> scores;
  event.getByToken(scores_token, scores);

  auto output_vertices = std::make_unique<reco::VertexCollection>();
  std::vector<float> output_scores_;
  auto nall = std::make_unique<int>(vertices->size());
  auto ngood = std::make_unique<int>(0);

  for (size_t i = 0 , ie = vertices->size(); i < ie; ++i) {
    reco::VertexRef v(vertices, i);
    if (!v->isFake() && v->ndof() > 4 && fabs(v->z()) <= 24 && v->position().rho() < 2) {
      if (nfirst == 0 || output_vertices->size() < nfirst) {
        output_vertices->push_back(*v);
        output_scores_.push_back((*scores)[v]);
      }
      ++(*ngood);
    }
  }

  const bool pass = !cut || *ngood > 0;

  event.put(std::move(nall), "nAll");
  event.put(std::move(ngood), "nGood");
  auto h_output_vertices = event.put(std::move(output_vertices));

  auto output_scores = std::make_unique<edm::ValueMap<float>>();
  edm::ValueMap<float>::Filler filler(*output_scores);
  filler.insert(h_output_vertices, output_scores_.begin(), output_scores_.end());
  filler.fill();
  event.put(std::move(output_scores));

  return pass;
}

DEFINE_FWK_MODULE(JMTGoodPrimaryVertices);
