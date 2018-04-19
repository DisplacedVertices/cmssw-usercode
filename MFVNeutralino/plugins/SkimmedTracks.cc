#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "JMTucker/Tools/interface/Bridges.h"

class MFVSkimmedTracks : public edm::EDFilter {
public:
  explicit MFVSkimmedTracks(const edm::ParameterSet&);
private:
  virtual bool filter(edm::Event&, const edm::EventSetup&) override;

  const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
  const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
  const edm::EDGetTokenT<reco::VertexCollection> primary_vertices_token;
  const double min_pt;
  const double min_dxybs;
  const double min_nsigmadxybs;
  const bool cut;
  const bool debug;
};

MFVSkimmedTracks::MFVSkimmedTracks(const edm::ParameterSet& cfg)
  : tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("tracks_src"))),
    beamspot_token(consumes<reco::BeamSpot>(edm::InputTag("offlineBeamSpot"))),
    primary_vertices_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("primary_vertices_src"))),
    min_pt(cfg.getParameter<double>("min_pt")),
    min_dxybs(cfg.getParameter<double>("min_dxybs")),
    min_nsigmadxybs(cfg.getParameter<double>("min_nsigmadxybs")),
    cut(cfg.getParameter<bool>("cut")),
    debug(cfg.getUntrackedParameter<bool>("debug", false))
{
  produces<reco::TrackCollection>();
  produces<std::vector<int>>(); // which PV if any, -1 if none
}

bool MFVSkimmedTracks::filter(edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<reco::TrackCollection> tracks;
  event.getByToken(tracks_token, tracks);

  edm::Handle<reco::BeamSpot> beamspot;
  if (min_dxybs > 0 || min_nsigmadxybs > 0)
    event.getByToken(beamspot_token, beamspot);

  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByToken(primary_vertices_token, primary_vertices);

  if (debug) std::cout << "MFVSkimmedTracks::filter: run " << event.id().run() << " lumi " << event.luminosityBlock() << " event " << event.id().event() << " has " << tracks->size() << " input tracks, " << primary_vertices->size() << " primary vertices\n";

  std::map<reco::TrackRef, std::vector<int>> tracks_in_pvs;
  for (size_t i = 0, ie = primary_vertices->size(); i < ie; ++i) {
    const reco::Vertex& pv = (*primary_vertices)[i];
    for (auto it = pv.tracks_begin(), ite = pv.tracks_end(); it != ite; ++it)
      tracks_in_pvs[it->castTo<reco::TrackRef>()].push_back(i);
  }
  
  std::unique_ptr<reco::TrackCollection> output_tracks(new reco::TrackCollection);
  std::unique_ptr<std::vector<int>> output_pvindex(new std::vector<int>);

  int itk = -1;
  for (const reco::Track& tk : *tracks) {
    ++itk;
    const double pt = tk.pt();
    const double abs_eta = fabs(tk.eta());
    const bool min_r = jmt::hasValidHitInFirstPixelBarrel(tk);
    const int npxlayers = tk.hitPattern().pixelLayersWithMeasurement();
    const int nstlayers = tk.hitPattern().stripLayersWithMeasurement();
    const bool stlayers_pass = (abs_eta < 2.0 && nstlayers >= 6) || (abs_eta >= 2.0 && nstlayers >= 7);

    bool pass = pt > min_pt && min_r && npxlayers >= 2 && stlayers_pass;

    if (debug) std::cout << "track #" << itk << " pt " << pt << " |eta| " << abs_eta << " min_r " << min_r << " npxlayers " << npxlayers << " nstlayers " << nstlayers << " stlayerspass? " << stlayers_pass << " pass so far? " << pass;

    if (pass && (min_dxybs > 0 || min_nsigmadxybs > 0)) {
      const double dxybs = tk.dxy(*beamspot);
      const double dxyerr = tk.dxyError();
      const double nsigmadxybs = dxybs / dxyerr;
      if (fabs(dxybs) < min_dxybs || fabs(nsigmadxybs) < min_nsigmadxybs)
        pass = false;
      if (debug) std::cout << " dxybs " << dxybs << " dxyerr " << dxyerr << " sigmadxybs " << nsigmadxybs;
    }

    if (pass) {
      output_tracks->push_back(tk);

      reco::TrackRef ref(tracks, itk);
      const std::vector<int>& pv_for_track = tracks_in_pvs[ref];
      if (pv_for_track.size() > 1)
        throw cms::Exception("BadAssumption", "multiple PV for a track");
      output_pvindex->push_back(pv_for_track.size() ? pv_for_track[0] : -1);

      if (debug) std::cout << " selected! now " << output_tracks->size() << " output tracks";
    }

    if (debug) std::cout << std::endl;
  }

  const size_t n_out = output_tracks->size();
  event.put(std::move(output_tracks));
  event.put(std::move(output_pvindex));

  return !cut || n_out;
}

DEFINE_FWK_MODULE(MFVSkimmedTracks);
