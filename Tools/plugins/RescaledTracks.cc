#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Formats/interface/TracksMap.h"

class JMTRescaledTracks : public edm::EDProducer {
public:
  explicit JMTRescaledTracks(const edm::ParameterSet&);

private:
  virtual void produce(edm::Event&, const edm::EventSetup&) override;

  const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
  const bool enable;
};

JMTRescaledTracks::JMTRescaledTracks(const edm::ParameterSet& cfg) 
  : tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("tracks_src"))),
    enable(cfg.getParameter<bool>("enable"))
{
  produces<reco::TrackCollection>();
  produces<jmt::TracksMap>();
}

void JMTRescaledTracks::produce(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<reco::TrackCollection> tracks;
  event.getByToken(tracks_token, tracks);

  auto output_tracks = std::make_unique<reco::TrackCollection>();
  auto output_tracks_map = std::make_unique<jmt::TracksMap>();

  reco::TrackRefProd h_output_tracks = event.getRefBeforePut<reco::TrackCollection>();

  for (size_t i = 0, ie = tracks->size(); i < ie; ++i) {
    reco::TrackRef tk(tracks, i);

    reco::TrackBase::CovarianceMatrix cov = tk->covariance();

    if (!event.isRealData() && enable) {
      double dxyerr_scale = 1.;
      double dszerr_scale = 1.;

      if (fabs(tk->eta()) < 1.5) {
        const double x = tk->pt();
        const double p_dxy[8] = {1.003954411196716, 0.04680608038556485, 1.1651640253424076, 0.010686515626581808, 1.2423728669230774, 0.002510211465163767, 1.301491397216935, -0.0005992241020962791};
	const double p_dsz[10] = {1.0245229183638793, 0.06544824469215105, 1.1860096333638355, 0.009315198253046261, 1.2534005803324926, -0.0010188848309496473, 1.2759550243574909, -0.0033600655572815436, 2.0547714269037252e-05, -3.967354320030131e-08};

        dxyerr_scale = (x<=5)*(p_dxy[0]+p_dxy[1]*x)+(x>5&&x<=10)*(p_dxy[2]+p_dxy[3]*x)+(x>10&&x<=19)*(p_dxy[4]+p_dxy[5]*x)+(x>19&&x<=200)*(p_dxy[6]+p_dxy[7]*x)+(x>200)*(p_dxy[6]+p_dxy[7]*200);
	dszerr_scale = (x<=3)*(p_dsz[0]+p_dsz[1]*x)+(x>3&&x<=7)*(p_dsz[2]+p_dsz[3]*x)+(x>7&&x<=11)*(p_dsz[4]+p_dsz[5]*x)+(x>11&&x<=200)*(p_dsz[6]+p_dsz[7]*x+p_dsz[8]*pow(x,2)+p_dsz[9]*pow(x,3))+(x>200)*(p_dsz[6]+p_dsz[7]*200+p_dsz[8]*pow(200,2)+p_dsz[9]*pow(200,3));
      } else {
        const double x = tk->pt();
	const double p_dxy[8] = {0.9809194238515303, 0.02988345020861421, 1.0494209346433279, 0.01638247946618149, 1.1747904134913318, 0.004173705981459077, 1.27170013468283, -0.0015234534159011834};
	const double p_dsz[7] = {0.9741157497540216, 0.03454031770932743, 1.1551685052673273, 0.008041427889944022, 1.3366714462830347, -0.0034743381492504328, 1.3448120785319356e-05};

	dxyerr_scale = (x<=5)*(p_dxy[0]+p_dxy[1]*x)+(x>5&&x<=10)*(p_dxy[2]+p_dxy[3]*x)+(x>10&&x<=19)*(p_dxy[4]+p_dxy[5]*x)+(x>19&&x<=200)*(p_dxy[6]+p_dxy[7]*x)+(x>200)*(p_dxy[6]+p_dxy[7]*200);
	dszerr_scale = (x<=7)*(p_dsz[0]+p_dsz[1]*x)+(x>7&&x<=17)*(p_dsz[2]+p_dsz[3]*x)+(x>17&&x<=200)*(p_dsz[4]+p_dsz[5]*x+p_dsz[6]*pow(x,2))+(x>200)*(p_dsz[4]+p_dsz[5]*200+p_dsz[6]*pow(200,2));
      }

      const int i_dxy = reco::TrackBase::i_dxy;
      const int i_dsz = reco::TrackBase::i_dsz;
      for (int idim = 0; idim < reco::TrackBase::dimension; ++idim) {
	if (idim == i_dxy)
	  cov(idim, i_dxy) *= dxyerr_scale * dxyerr_scale;
	else
	  cov(idim, i_dxy) *= dxyerr_scale;
      }
      for (int idim = 0; idim < reco::TrackBase::dimension; ++idim) {
	if (idim == i_dsz)
	  cov(idim, i_dsz) *= dszerr_scale * dszerr_scale;
	else
	  cov(idim, i_dsz) *= dszerr_scale;
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

DEFINE_FWK_MODULE(JMTRescaledTracks);
