#include "TVector3.h"
#include "CLHEP/Random/RandomEngine.h"
#include "CLHEP/Random/RandExponential.h"
#include "CLHEP/Random/RandGauss.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/RandomNumberGenerator.h"

class MFVTrackMover : public edm::EDFilter {
public:
  explicit MFVTrackMover(const edm::ParameterSet&);

private:
  bool select_track(const reco::TrackRef& tk) const;

  virtual bool filter(edm::Event&, const edm::EventSetup&);

  const edm::InputTag tracks_src;
  const edm::InputTag primary_vertices_src;
  const edm::InputTag jets_src;
  const double min_jet_pt;
  const unsigned min_jet_ntracks;
  const std::string b_discriminator;
  const double b_discriminator_veto;
  const double b_discriminator_tag;

  const unsigned njets;
  const unsigned nbjets;
  const double tau;
  const double sig_theta;
  const double sig_phi;

  edm::Service<edm::RandomNumberGenerator> rng;

  std::vector<int> knuth_select(int n, int N) {
    std::vector<int> ts;
    int t = 0, m = 0;
    while (m < n) {
      if ((N - t) * rng->getEngine().flat() >= n - m)
        ++t;
      else {
        ++m;
        ts.push_back(t++);
      }
    }
    return ts;
  }
};

MFVTrackMover::MFVTrackMover(const edm::ParameterSet& cfg) 
  : tracks_src(cfg.getParameter<edm::InputTag>("tracks_src")),
    primary_vertices_src(cfg.getParameter<edm::InputTag>("primary_vertices_src")),
    jets_src(cfg.getParameter<edm::InputTag>("jets_src")),
    min_jet_pt(cfg.getParameter<double>("min_jet_pt")),
    min_jet_ntracks(cfg.getParameter<unsigned>("min_jet_ntracks")),
    b_discriminator(cfg.getParameter<std::string>("b_discriminator")),
    b_discriminator_veto(cfg.getParameter<double>("b_discriminator_veto")),
    b_discriminator_tag(cfg.getParameter<double>("b_discriminator_tag")),
    njets(cfg.getParameter<unsigned>("njets")),
    nbjets(cfg.getParameter<unsigned>("nbjets")),
    tau(cfg.getParameter<double>("tau")),
    sig_theta(cfg.getParameter<double>("sig_theta")),
    sig_phi(cfg.getParameter<double>("sig_phi"))
{
  if (!rng.isAvailable())
    throw cms::Exception("MFVTrackMover", "RandomNumberGeneratorService not available");

  produces<reco::TrackCollection>();
  produces<reco::TrackCollection>("moved");
  produces<pat::JetCollection>("jetsUsed");
  produces<pat::JetCollection>("bjetsUsed");
  produces<std::vector<double> >("flightAxis");
  produces<std::vector<double> >("moveVertex");
}

bool MFVTrackMover::filter(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<reco::TrackCollection> tracks;
  event.getByLabel(tracks_src, tracks);

  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByLabel(primary_vertices_src, primary_vertices);
  const reco::Vertex& primary_vertex = primary_vertices->at(0);
  const bool primary_vertex_has_tracks = primary_vertex.tracks_end() - primary_vertex.tracks_begin();
  if (!primary_vertex_has_tracks)
    throw cms::Exception("MFVTrackMover", "no trackrefs in primary vertex");

  edm::Handle<pat::JetCollection> jets;
  event.getByLabel(jets_src, jets);

  CLHEP::RandExponential rexp(rng->getEngine());
  CLHEP::RandGauss rgau(rng->getEngine());

  std::auto_ptr<reco::TrackCollection> output_tracks(new reco::TrackCollection);
  std::auto_ptr<reco::TrackCollection> moved_tracks(new reco::TrackCollection);
  std::auto_ptr<pat::JetCollection> jets_used(new pat::JetCollection);
  std::auto_ptr<pat::JetCollection> bjets_used(new pat::JetCollection);
  std::auto_ptr<std::vector<double> > flight_vect(new std::vector<double>(3, 0.));
  std::auto_ptr<std::vector<double> > move_vertex(new std::vector<double>(3, 0.));

  std::vector<const pat::Jet*> presel_jets;
  std::vector<const pat::Jet*> presel_bjets;
  std::vector<const pat::Jet*> selected_jets;

  // Pick the (b-)jets we'll use.

  for (const pat::Jet& jet : *jets) {
    if (jet.pt() < min_jet_pt)
      continue;

    unsigned jet_ntracks = 0;
    for (const reco::PFCandidatePtr& pfcand : jet.getPFConstituents())
      if (pfcand->trackRef().isNonnull())
        ++jet_ntracks;
    if (jet_ntracks < min_jet_ntracks)
      continue;

    const double b_disc = jet.bDiscriminator(b_discriminator);
    if (b_disc < b_discriminator_veto)
      presel_jets.push_back(&jet);
    else if (b_disc > b_discriminator_tag)
      presel_bjets.push_back(&jet);
  }

  if (presel_jets.size() < njets || presel_bjets.size() < nbjets)
    return false;

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
  TVector3 move;
  move.SetMagThetaPhi(dist, theta, phi);
  move_vertex->at(0) = primary_vertex.x() + move.x();
  move_vertex->at(1) = primary_vertex.y() + move.y();
  move_vertex->at(2) = primary_vertex.z() + move.z();
  
  // Copy all the input tracks, except for those corresponding to the
  // above jets; for the latter, clone the tracks but move their
  // reference points to the move vertex.

  for (size_t i = 0, ie = tracks->size(); i < ie; ++i) {
    reco::TrackRef tk(tracks, i);
    bool to_move = false;
    for (const pat::Jet* jet : selected_jets)
      for (const reco::PFCandidatePtr& pfcand : jet->getPFConstituents())
        if (tk == pfcand->trackRef()) {
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
      new_tk.setHitPattern(tk->hitPattern());
      new_tk.setNLoops(tk->nLoops());
      new_tk.setTrackerExpectedHitsInner(tk->trackerExpectedHitsInner());
      new_tk.setTrackerExpectedHitsOuter(tk->trackerExpectedHitsOuter());
      moved_tracks->push_back(new_tk);
    }
    else
      output_tracks->push_back(*tk);
  }

  event.put(output_tracks);
  event.put(moved_tracks, "moved");
  event.put(jets_used, "jetsUsed");
  event.put(bjets_used, "bjetsUsed");
  event.put(flight_vect, "flightAxis");
  event.put(move_vertex, "moveVertex");

  return true;
}

DEFINE_FWK_MODULE(MFVTrackMover);
