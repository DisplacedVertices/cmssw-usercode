#include "TVector3.h"
#include "CLHEP/Random/RandomEngine.h"
#include "CLHEP/Random/RandExponential.h"
#include "CLHEP/Random/RandGauss.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/RandomNumberGenerator.h"
#include "JMTucker/Formats/interface/TracksMap.h"
#include "JMTucker/Tools/interface/BTagging.h"
#include "JMTucker/Tools/interface/TrackRefGetter.h"

class MFVTrackMover : public edm::EDProducer {
public:
  explicit MFVTrackMover(const edm::ParameterSet&);

private:
  virtual void produce(edm::Event&, const edm::EventSetup&);

  const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
  const edm::EDGetTokenT<reco::VertexCollection> primary_vertices_token;
  const edm::EDGetTokenT<pat::JetCollection> jets_token;
  jmt::TrackRefGetter track_ref_getter;

  const double min_jet_pt;
  const unsigned min_jet_ntracks;

  const unsigned njets;
  const unsigned nbjets;
  const double tau;
  const double sig_theta;
  const double sig_phi;
};

MFVTrackMover::MFVTrackMover(const edm::ParameterSet& cfg) 
  : tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("tracks_src"))),
    primary_vertices_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("primary_vertices_src"))),
    jets_token(consumes<pat::JetCollection>(cfg.getParameter<edm::InputTag>("jets_src"))),
    track_ref_getter(cfg.getParameter<std::string>("@module_label"),
                         cfg.getParameter<edm::ParameterSet>("track_ref_getter"),
                         consumesCollector()),
    min_jet_pt(cfg.getParameter<double>("min_jet_pt")),
    min_jet_ntracks(cfg.getParameter<unsigned>("min_jet_ntracks")),
    njets(cfg.getParameter<unsigned>("njets")),
    nbjets(cfg.getParameter<unsigned>("nbjets")),
    tau(cfg.getParameter<double>("tau")),
    sig_theta(cfg.getParameter<double>("sig_theta")),
    sig_phi(cfg.getParameter<double>("sig_phi"))
{
  edm::Service<edm::RandomNumberGenerator> rng;
  if (!rng.isAvailable())
    throw cms::Exception("MFVTrackMover", "RandomNumberGeneratorService not available");

  produces<reco::TrackCollection>();
  produces<jmt::TracksMap>();
  produces<reco::TrackCollection>("moved");
  produces<int>("npreseljets");
  produces<int>("npreselbjets");
  produces<pat::JetCollection>("jetsUsed");
  produces<pat::JetCollection>("bjetsUsed");
  produces<std::vector<double> >("flightAxis");
  produces<std::vector<double> >("moveVertex");
}

void MFVTrackMover::produce(edm::Event& event, const edm::EventSetup&) {
  edm::Service<edm::RandomNumberGenerator> rng;
  CLHEP::HepRandomEngine& rng_engine = rng->getEngine(event.streamID());

  auto knuth_select = [&rng_engine](int n, int N) -> std::vector<int> {
    std::vector<int> ts;
    int t = 0, m = 0;
    while (m < n) {
      if ((N - t) * rng_engine.flat() >= n - m)
        ++t;
      else {
        ++m;
        ts.push_back(t++);
      }
    }
    return ts;
  };

  auto output_tracks = std::make_unique<reco::TrackCollection>();
  reco::TrackRefProd h_output_tracks = event.getRefBeforePut<reco::TrackCollection>();
  auto output_tracks_map = std::make_unique<jmt::TracksMap>();
  auto moved_tracks = std::make_unique<reco::TrackCollection>(); // JMTBAD just write a vector<bool> and pick it up in MovedTracksTreer
  auto npreseljets = std::make_unique<int>();
  auto npreselbjets = std::make_unique<int>();
  auto jets_used = std::make_unique<pat::JetCollection>();
  auto bjets_used = std::make_unique<pat::JetCollection>();
  auto flight_vect = std::make_unique<std::vector<double>>(3, 0.);
  auto move_vertex = std::make_unique<std::vector<double>>(3, 0.);

  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByToken(primary_vertices_token, primary_vertices);
  const reco::Vertex* pv = primary_vertices->size() ? &(*primary_vertices)[0] : 0;

  if (pv) {
    edm::Handle<pat::JetCollection> jets;
    event.getByToken(jets_token, jets);

    CLHEP::RandExponential rexp(rng_engine);
    CLHEP::RandGauss rgau(rng_engine);

    std::vector<const pat::Jet*> presel_jets;
    std::vector<const pat::Jet*> presel_bjets;
    std::vector<const pat::Jet*> selected_jets;

    TVector3 move;

    // Pick the (b-)jets we'll use.

    for (const pat::Jet& jet : *jets) {
      if (jet.pt() < min_jet_pt || track_ref_getter.tracks(event, jet).size() < min_jet_ntracks)
        continue;

      const double b_disc = jmt::BTagging::discriminator(jet);
      if (b_disc < jmt::BTagging::discriminator_min(jmt::BTagging::loose))
        presel_jets.push_back(&jet);
      else if (b_disc > jmt::BTagging::discriminator_min(jmt::BTagging::tight))
        presel_bjets.push_back(&jet);
    }

    *npreseljets = presel_jets.size();
    *npreselbjets = presel_bjets.size();
    const bool pass_presel = presel_jets.size() >= njets && presel_bjets.size() >= nbjets;

    if (pass_presel) {
      for (int i : knuth_select(njets, presel_jets.size())) {
        selected_jets.push_back(presel_jets[i]);
        jets_used->push_back(*presel_jets[i]);
      }

      for (int i : knuth_select(nbjets, presel_bjets.size())) {
        selected_jets.push_back(presel_bjets[i]);
        bjets_used->push_back(*presel_bjets[i]);
      }

      // Find the energy-weighted average direction of all the (b-)jets to
      // be the flight axis.

      TVector3 flight_axis;
      for (const pat::Jet* jet : selected_jets)
        flight_axis += TVector3(jet->px(), jet->py(), jet->pz());
      flight_axis.SetMag(1.);
      flight_vect->at(0) = flight_axis.x();
      flight_vect->at(1) = flight_axis.y();
      flight_vect->at(2) = flight_axis.z();

      // Find the move vertex: pick a flight distance using Exp(dist|tau)
      // and a direction around the flight axis using
      // Gaus(theta|sig_theta) * Gaus(phi|sig_phi).

      const double dist = rexp.fire(tau);
      const double theta = rgau.fire(flight_axis.Theta(), sig_theta);
      const double phi   = rgau.fire(flight_axis.Phi(),   sig_phi);
      move.SetMagThetaPhi(dist, theta, phi);
      move_vertex->at(0) = primary_vertices->at(0).x() + move.x();
      move_vertex->at(1) = primary_vertices->at(0).y() + move.y();
      move_vertex->at(2) = primary_vertices->at(0).z() + move.z();
    }
  
    // Copy all the input tracks, except for those corresponding to the
    // above jets; for the latter, clone the tracks but move their
    // reference points to the move vertex.

    edm::Handle<reco::TrackCollection> tracks;
    event.getByToken(tracks_token, tracks);

    for (size_t i = 0, ie = tracks->size(); i < ie; ++i) {
      reco::TrackRef tk(tracks, i);
      bool to_move = false;
      for (const pat::Jet* jet : selected_jets)
        for (const reco::TrackRef& jet_tk : track_ref_getter.tracks(event, *jet))
          if (tk == jet_tk) {
            to_move = true;
            goto done_check_to_move;
          }
      done_check_to_move:
    
      if (to_move) {
        reco::TrackBase::Point new_point(tk->vx() + move.x(),
                                         tk->vy() + move.y(),
                                         tk->vz() + move.z());

        output_tracks->push_back(reco::Track(tk->chi2(), tk->ndof(), new_point, tk->momentum(), tk->charge(), tk->covariance(), tk->algo()));
        reco::Track& new_tk = output_tracks->back();
        new_tk.setQualityMask(tk->qualityMask());
        new_tk.setNLoops(tk->nLoops());
        reco::HitPattern* hp = const_cast<reco::HitPattern*>(&new_tk.hitPattern());  *hp = tk->hitPattern(); // lmao
        moved_tracks->push_back(new_tk);
      }
      else
        output_tracks->push_back(*tk);

      output_tracks_map->insert(tk, reco::TrackRef(h_output_tracks, output_tracks->size() - 1));
    }
  }

  event.put(std::move(output_tracks));
  event.put(std::move(output_tracks_map));
  event.put(std::move(moved_tracks), "moved");
  event.put(std::move(npreseljets), "npreseljets");
  event.put(std::move(npreselbjets), "npreselbjets");
  event.put(std::move(jets_used), "jetsUsed");
  event.put(std::move(bjets_used), "bjetsUsed");
  event.put(std::move(flight_vect), "flightAxis");
  event.put(std::move(move_vertex), "moveVertex");
}

DEFINE_FWK_MODULE(MFVTrackMover);
