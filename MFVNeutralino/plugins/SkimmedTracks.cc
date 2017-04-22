#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"

class MFVSkimmedTracks : public edm::EDProducer {
public:
  explicit MFVSkimmedTracks(const edm::ParameterSet&);
private:
  virtual void produce(edm::Event&, const edm::EventSetup&);

  const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
  const bool apply_sigmadxybs;
  const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
};

MFVSkimmedTracks::MFVSkimmedTracks(const edm::ParameterSet& cfg)
  : tracks_token(consumes<reco::TrackCollection>(edm::InputTag("generalTracks"))),
    apply_sigmadxybs(cfg.getParameter<bool>("apply_sigmadxybs")),
    beamspot_token(consumes<reco::BeamSpot>(edm::InputTag("offlineBeamSpot")))
{
  produces<reco::TrackCollection>();
}

void MFVSkimmedTracks::produce(edm::Event& event, const edm::EventSetup& setup) {
  static const bool debug = false;

  edm::Handle<reco::TrackCollection> tracks;
  event.getByToken(tracks_token, tracks);

  edm::Handle<reco::BeamSpot> beamspot;
  if (apply_sigmadxybs)
    event.getByToken(beamspot_token, beamspot);
  
  std::auto_ptr<reco::TrackCollection> output_tracks(new reco::TrackCollection);

  if (debug) std::cout << "MFVSkimmedTracks::produce: run " << event.id().run() << " lumi " << event.luminosityBlock() << " event " << event.id().event() << " has " << tracks->size() << " input tracks\n";

  int itk = 0;
  for (const reco::Track& tk : *tracks) {
    const double pt = tk.pt();
    const double abs_eta = fabs(tk.eta());
    const bool min_r = tk.hitPattern().hasValidHitInFirstPixelBarrel();
    const int npxlayers = tk.hitPattern().pixelLayersWithMeasurement();
    const int nstlayers = tk.hitPattern().stripLayersWithMeasurement();
    const bool stlayers_pass = (abs_eta < 2.0 && nstlayers >= 6) || (abs_eta >= 2.0 && nstlayers >= 7);

    bool pass = pt > 1. && min_r && npxlayers >= 2 && stlayers_pass;

    if (debug) std::cout << "track #" << itk++ << " pt " << pt << " |eta| " << abs_eta << " min_r " << min_r << " npxlayers " << npxlayers << " nstlayers " << nstlayers << " stlayerspass? " << stlayers_pass << " pass so far? " << pass;

    if (apply_sigmadxybs) {
      const double dxybs = tk.dxy(*beamspot);
      const double dxyerr = tk.dxyError();
      const double sigmadxybs = dxybs / dxyerr;
      pass = pass && sigmadxybs > 4;
      if (debug) std::cout << " dxybs " << dxybs << " dxyerr " << dxyerr << " sigmadxybs " << sigmadxybs;
    }

    if (pass) {
      output_tracks->push_back(tk);
      if (debug) std::cout << " selected! now " << output_tracks->size() << " output tracks";
    }

    if (debug) std::cout << std::endl;
  }

  event.put(output_tracks);
}

DEFINE_FWK_MODULE(MFVSkimmedTracks);
