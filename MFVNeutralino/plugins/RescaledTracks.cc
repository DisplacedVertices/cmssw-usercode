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
      const double x = tk->pt();
      const double p[12] = {1.0173011869120834, 0.044533302581799744, 1.3195634354617685, -0.009976304901909844, 1.1850626163736517, 0.0012770778723076347, 1.0049535896045954, 0.011293826864722332, 1.3791408353275811, 0.00163492657307045, 1.5557569970128258, -0.0014711711689202145};
      const double dxyerr_scale = (x<=5)*(p[0]+p[1]*x)+(x>5&&x<=10)*(p[2]+p[3]*x)+(x>10&&x<=18)*(p[4]+p[5]*x)+(x>18&&x<=40)*(p[6]+p[7]*x)+(x>40&&x<=60)*(p[8]+p[9]*x)+(x>60&&x<=200)*(p[10]+p[11]*x) + (x>200)*(p[10]+p[11]*200);

      const int i_dxy = reco::TrackBase::i_dxy;
      for (int idim = 0; idim < reco::TrackBase::dimension; ++idim) {
        if (idim == i_dxy)
          cov(idim, i_dxy) *= dxyerr_scale * dxyerr_scale;
        else
          cov(idim, i_dxy) *= dxyerr_scale;
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
