#include "CLHEP/Random/RandomEngine.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/RandomNumberGenerator.h"

class MFVTrackMover : public edm::EDProducer {
public:
  explicit MFVTrackMover(const edm::ParameterSet&);

private:
  bool select_track(const reco::TrackRef& tk) const;

  virtual void produce(edm::Event&, const edm::EventSetup&);

  const edm::InputTag tracks_src;
  const edm::InputTag primary_vertices_src;
  const edm::InputTag jets_src;

  const double delta_x;
  const double delta_y;
  const double delta_z;

  edm::Service<edm::RandomNumberGenerator> rng;

  const reco::Vertex* primary_vertex;
  const pat::JetCollection* jets;

  TH1F* h_npv;
  TH1F* h_pvntracks;
  TH1F* h_pvsumpt2;
  TH1F* h_ntracks;
  TH1F* h_nselected;

  TH1F* h_njets;
  TH1F* h_jetntracks[10];
  TH1F* h_jetdrs[10];
};

MFVTrackMover::MFVTrackMover(const edm::ParameterSet& cfg) 
  : tracks_src(cfg.getParameter<edm::InputTag>("tracks_src")),
    primary_vertices_src(cfg.getParameter<edm::InputTag>("primary_vertices_src")),
    jets_src(cfg.getParameter<edm::InputTag>("jets_src")),
    delta_x(cfg.getParameter<double>("delta_x")),
    delta_y(cfg.getParameter<double>("delta_y")),
    delta_z(cfg.getParameter<double>("delta_z"))
{
  if (!rng.isAvailable())
    throw cms::Exception("MFVTrackMover", "RandomNumberGeneratorService not available");

  edm::Service<TFileService> fs;
  h_npv = fs->make<TH1F>("h_npv", ";number of primary vertices;events/2", 50, 0, 100);
  h_pvntracks = fs->make<TH1F>("h_pvntracks", ";number of tracks in primary vertex;events/5", 100, 0, 500);
  h_pvsumpt2 = fs->make<TH1F>("h_pvsumpt2", ";#Sigma p_{T}^{2} (GeV);events/200 GeV^{2}", 100, 0, 20000);
  h_ntracks = fs->make<TH1F>("h_ntracks", ";number of tracks;events/20", 100, 0, 2000);
  h_nselected = fs->make<TH1F>("h_nselected", ";number of selected tracks;events/2", 100, 0, 200);

  h_njets = fs->make<TH1F>("h_njets", ";number of jets;events", 20, 0, 20);
  for (int i = 0; i < 10; ++i) {
    h_jetntracks[i] = fs->make<TH1F>(TString::Format("h_jetntracks_%i", i),
                                     i == 0 ? ";number of tracks in jets;events/2" : TString::Format(";number of tracks in jet %i;events/2", i),
                                     25, 0, 50);
    h_jetdrs[i] = fs->make<TH1F>(TString::Format("h_jetdrs_%i", i),
                                 i == 0 ? ";dR between jets;events/0.25" : TString::Format(";dR between jet 0 and %i;events/0.25", i),
                                 20, 0, 5);
  }

  produces<reco::TrackCollection>();
}

bool MFVTrackMover::select_track(const reco::TrackRef& tk) const {
  //const bool primary_vertex_has_tracks = primary_vertex->refittedTracks().size() == 0;
  const bool primary_vertex_has_tracks = primary_vertex->tracks_end() - primary_vertex->tracks_begin();
  if (!primary_vertex_has_tracks)
    throw cms::Exception("MFVTrackMover", "no trackrefs in primary vertex");

  const bool in_primary_vertex = std::find(primary_vertex->tracks_begin(), primary_vertex->tracks_end(), reco::TrackBaseRef(tk)) != primary_vertex->tracks_end();

  bool in_jet = false;
  for (const pat::Jet& jet : *jets) {
    for (const reco::PFCandidatePtr& pfcand : jet.getPFConstituents()) {
      if (tk == pfcand->trackRef()) {
        in_jet = true;
        break;
      }
    }
    if (in_jet)
      break;
  }

  return
    in_primary_vertex &&
    in_jet;
  //  &&    rng->getEngine().flat() < 0.25;
}

void MFVTrackMover::produce(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<reco::TrackCollection> tracks;
  event.getByLabel(tracks_src, tracks);

  h_ntracks->Fill(tracks->size());

  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByLabel(primary_vertices_src, primary_vertices);
  primary_vertex = &primary_vertices->at(0);

  h_npv->Fill(primary_vertices->size());
  h_pvntracks->Fill(primary_vertex->tracks_end() - primary_vertex->tracks_begin());
  h_pvsumpt2->Fill(std::accumulate(primary_vertex->tracks_begin(), primary_vertex->tracks_end(), 0., 
                                   [](const double sum, const reco::TrackBaseRef& tk) { return sum + pow(tk->pt(), 2); }));

  edm::Handle<pat::JetCollection> jets_h;
  event.getByLabel(jets_src, jets_h);
  jets = &*jets_h;

  h_njets->Fill(jets->size());
  std::vector<double> jetdrs;
  for (size_t i = 0, ie = jets->size(); i < ie; ++i) {
    const pat::Jet& jet = jets->at(i);
    int ntracks = 0;
    for (const reco::PFCandidatePtr& pfcand : jet.getPFConstituents())
      if (pfcand->trackRef().isNonnull())
        ++ntracks;
    h_jetntracks[0]->Fill(ntracks);
    if (i < 9)
      h_jetntracks[i+1]->Fill(ntracks);

    for (size_t j = i+1; j < ie; ++j)
      jetdrs.push_back(reco::deltaR(jet, jets->at(j)));
  }
  std::sort(jetdrs.begin(), jetdrs.end());
  for (size_t i = 0, ie = std::min(int(jetdrs.size()), 9); i < ie; ++i) {
    h_jetdrs[0]->Fill(jetdrs[i]);
    h_jetdrs[i+1]->Fill(jetdrs[i]);
  }
    
  std::auto_ptr<reco::TrackCollection> new_tracks(new reco::TrackCollection);

  for (size_t i = 0, ie = tracks->size(); i < ie; ++i) {
    reco::TrackRef tk(tracks, i);
    if (select_track(tk)) {
      reco::TrackBase::Point new_point(tk->vx() + delta_x,
                                       tk->vy() + delta_y,
                                       tk->vz() + delta_z);

      new_tracks->push_back(reco::Track(tk->chi2(), tk->ndof(), new_point, tk->momentum(), tk->charge(), tk->covariance(), tk->algo()));
      reco::Track& new_tk = new_tracks->back();
      new_tk.setQualityMask(tk->qualityMask());
      new_tk.setHitPattern(tk->hitPattern());
      new_tk.setNLoops(tk->nLoops());
      new_tk.setTrackerExpectedHitsInner(tk->trackerExpectedHitsInner());
      new_tk.setTrackerExpectedHitsOuter(tk->trackerExpectedHitsOuter());
    }
  }

  h_nselected->Fill(new_tracks->size());

  event.put(new_tracks);
}

DEFINE_FWK_MODULE(MFVTrackMover);
