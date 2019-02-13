#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

class MFVRescaledTracks : public edm::EDProducer {
public:
  explicit MFVRescaledTracks(const edm::ParameterSet&);

private:
  virtual void produce(edm::Event&, const edm::EventSetup&) override;

  const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
};

MFVRescaledTracks::MFVRescaledTracks(const edm::ParameterSet& cfg) 
  : tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("tracks_src")))
{
  produces<reco::TrackCollection>();
}

void MFVRescaledTracks::produce(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<reco::TrackCollection> tracks;
  event.getByToken(tracks_token, tracks);

  std::unique_ptr<reco::TrackCollection> output_tracks(new reco::TrackCollection);

  
  for (const reco::Track& tk : *tracks) {
    const double pt = tk.pt();

    reco::TrackBase::CovarianceMatrix cov = tk.covariance();

    double dxyerr_scale = 1.2;
    if (pt < 6)
      dxyerr_scale =  0.0375 * pt + 1.025;
    else if (6 <= pt && pt < 10)
      dxyerr_scale = -0.0125 * pt + 1.325;

    const int i_dxy = reco::TrackBase::i_dxy;
    for (int idim = 0; idim < reco::TrackBase::dimension; ++idim) {
      if (idim == i_dxy)
        cov(idim, i_dxy) *= dxyerr_scale * dxyerr_scale;
      else
        cov(idim, i_dxy) *= dxyerr_scale;
    }

    output_tracks->push_back(reco::Track(tk.chi2(), tk.ndof(), tk.referencePoint(), tk.momentum(), tk.charge(), cov, tk.algo()));
    reco::Track& new_tk = output_tracks->back();
    new_tk.setQualityMask(tk.qualityMask());
    new_tk.setNLoops(tk.nLoops());
    reco::HitPattern* hp = const_cast<reco::HitPattern*>(&new_tk.hitPattern());  *hp = tk.hitPattern(); // lmao
  }

  event.put(std::move(output_tracks));
}

DEFINE_FWK_MODULE(MFVRescaledTracks);
