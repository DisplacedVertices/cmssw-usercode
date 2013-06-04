#include "TH1F.h"
#include "TH2F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"

class MFVVertexMerger : public edm::EDProducer {
public:
  MFVVertexMerger(const edm::ParameterSet&);

  virtual void produce(edm::Event&, const edm::EventSetup&);

private:
  double computeSharedTracks(const reco::Vertex&, const reco::Vertex&) const;

  const edm::InputTag vertex_src;
  const double max_frac;
  const double min_sig;

  VertexDistance3D dist;

  const bool do_histos;
  TH2F* h_nvtx;
  TH2F* h_frac_v_sig;
};

MFVVertexMerger::MFVVertexMerger(const edm::ParameterSet& params)
  : vertex_src(params.getParameter<edm::InputTag>("secondaryVertices")),
    max_frac(params.getParameter<double>("maxFraction")),
    min_sig(params.getParameter<double>("minSignificance")),
    do_histos(params.getParameter<bool>("do_histos"))
{
  produces<reco::VertexCollection>();
  
  if (do_histos) {
    edm::Service<TFileService> fs;
    h_nvtx = fs->make<TH2F>("h_nvtx", ";# input vertices;# output vertices", 100, 0, 100, 50, 0, 50);
    h_frac_v_sig = fs->make<TH2F>("h_frac_v_sig", ";pairwise significance;fraction shared", 50, 0, 100, 26, 0, 1.04);
  }
}

double MFVVertexMerger::computeSharedTracks(const reco::Vertex& sv, const reco::Vertex& sv2) const {
  std::set<reco::TrackRef> sv_tracks;

  for (auto it = sv.tracks_begin(); it != sv.tracks_end(); ++it)
    if (sv.trackWeight(*it) >= 0.5)
      sv_tracks.insert(it->castTo<reco::TrackRef>());

  unsigned count = 0, total = 0;
  for (auto it = sv2.tracks_begin(), ite = sv2.tracks_end(); it != ite; ++it) {
    if (sv2.trackWeight(*it) >= 0.5) {
      ++total;
      count += sv_tracks.count(it->castTo<reco::TrackRef>());
    }
  }

  return double(count)/total;
}

void MFVVertexMerger::produce(edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<reco::VertexCollection> vertices;
  event.getByLabel(vertex_src, vertices);

  std::auto_ptr<reco::VertexCollection> new_vertices(new reco::VertexCollection);
  for (const reco::Vertex& sv : *vertices)
    new_vertices->push_back(sv);

  for (std::vector<reco::Vertex>::iterator sv = new_vertices->begin(); sv != new_vertices->end(); ++sv) {
    bool shared = false;
    for (std::vector<reco::Vertex>::iterator sv2 = new_vertices->begin(); sv2 != new_vertices->end(); ++sv2) {
      if (sv == sv2)
        continue; 

      const double sig = dist.distance(*sv, *sv2).significance();
      const double fr = computeSharedTracks(*sv2, *sv);
      if (do_histos) h_frac_v_sig->Fill(sig, fr);

      if (sig < min_sig && fr > max_frac && fr >= computeSharedTracks(*sv, *sv2))
        shared = true;
    }

    if (shared)
      sv = new_vertices->erase(sv) - 1;
  }

  if (do_histos) h_nvtx->Fill(vertices->size(), new_vertices->size());
  event.put(new_vertices);
}

DEFINE_FWK_MODULE(MFVVertexMerger);
