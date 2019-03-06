#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralinoFormats/interface/TracksMap.h"

class MFVRescaledTracks : public edm::EDProducer {
public:
  explicit MFVRescaledTracks(const edm::ParameterSet&);

private:
  virtual void produce(edm::Event&, const edm::EventSetup&) override;

  const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
  const bool enable;
};

MFVRescaledTracks::MFVRescaledTracks(const edm::ParameterSet& cfg) 
  : tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("tracks_src"))),
    enable(cfg.getParameter<bool>("enable"))
{
  produces<reco::TrackCollection>();
  produces<mfv::TracksMap>();
}

void MFVRescaledTracks::produce(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<reco::TrackCollection> tracks;
  event.getByToken(tracks_token, tracks);

  auto output_tracks = std::make_unique<reco::TrackCollection>();
  auto output_tracks_map = std::make_unique<mfv::TracksMap>();

  reco::TrackRefProd h_output_tracks = event.getRefBeforePut<reco::TrackCollection>();

  for (size_t i = 0, ie = tracks->size(); i < ie; ++i) {
    reco::TrackRef tk(tracks, i);

    reco::TrackBase::CovarianceMatrix cov = tk->covariance();

    if (!event.isRealData() && enable) {
      if (fabs(tk->eta()) < 1.5) {
        const double x = tk->pt();
        const double p[8] = {1.003954411196716, 0.04680608038556485, 1.1651640253424076, 0.010686515626581808, 1.2423728669230774, 0.002510211465163767, 1.301491397216935, -0.0005992241020962791};
        const double dxyerr_scale = (x<=5)*(p[0]+p[1]*x)+(x>5&&x<=10)*(p[2]+p[3]*x)+(x>10&&x<=19)*(p[4]+p[5]*x)+(x>19&&x<=200)*(p[6]+p[7]*x)+(x>200)*(p[6]+p[7]*200);

        const int i_dxy = reco::TrackBase::i_dxy;
        for (int idim = 0; idim < reco::TrackBase::dimension; ++idim) {
          if (idim == i_dxy)
            cov(idim, i_dxy) *= dxyerr_scale * dxyerr_scale;
          else
            cov(idim, i_dxy) *= dxyerr_scale;
        }
      }
    }

    output_tracks->push_back(reco::Track(tk->chi2(), tk->ndof(), tk->referencePoint(), tk->momentum(), tk->charge(), cov, tk->algo()));
    reco::Track& new_tk = output_tracks->back();
    new_tk.setQualityMask(tk->qualityMask());
    new_tk.setNLoops(tk->nLoops());
    reco::HitPattern* hp = const_cast<reco::HitPattern*>(&new_tk.hitPattern());  *hp = tk->hitPattern(); // lmao

    output_tracks_map->insert(tk, reco::TrackRef(h_output_tracks, output_tracks->size() - 1));
  }

  event.put(std::move(output_tracks));
  event.put(std::move(output_tracks_map));
}

DEFINE_FWK_MODULE(MFVRescaledTracks);
