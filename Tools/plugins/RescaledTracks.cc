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
      double dzerr_scale = 1.;

      if (fabs(tk->eta()) < 1.5) {
        const double x = tk->pt();
        const double p_dxy[8] = {1.003954411196716, 0.04680608038556485, 1.1651640253424076, 0.010686515626581808, 1.2423728669230774, 0.002510211465163767, 1.301491397216935, -0.0005992241020962791};
	const double p_dz[10] = {1.007007715615617, 0.07076294166195589, 1.1868108455695654, 0.01124546073198655, 1.2603636901194164, -6.757442837850885e-05, 1.2959118721777048, -0.0036321160334744722, 2.2186635725411445e-05, -4.756429055003546e-08};

        dxyerr_scale = (x<=5)*(p_dxy[0]+p_dxy[1]*x)+(x>5&&x<=10)*(p_dxy[2]+p_dxy[3]*x)+(x>10&&x<=19)*(p_dxy[4]+p_dxy[5]*x)+(x>19&&x<=200)*(p_dxy[6]+p_dxy[7]*x)+(x>200)*(p_dxy[6]+p_dxy[7]*200);
	dzerr_scale = (x<=3)*(p_dz[0]+p_dz[1]*x)+(x>3&&x<=7)*(p_dz[2]+p_dz[3]*x)+(x>7&&x<=11)*(p_dz[4]+p_dz[5]*x)+(x>11&&x<=200)*(p_dz[6]+p_dz[7]*x+p_dz[8]*pow(x,2)+p_dz[9]*pow(x,3))+(x>200)*(p_dz[6]+p_dz[7]*200+p_dz[8]*pow(200,2)+p_dz[9]*pow(200,3));
      } else {
        const double x = tk->pt();
	const double p_dxy[8] = {0.9809194238515303, 0.02988345020861421, 1.0494209346433279, 0.01638247946618149, 1.1747904134913318, 0.004173705981459077, 1.27170013468283, -0.0015234534159011834};
	const double p_dz[8] = {0.9691350243030017, 0.031178536430892512, 1.1955721335524367, 0.004243897802816205, 1.3189428244296684, -0.0026031457703504764, -7.571559366239088e-08, 4.5067664856339936e-08};

	dxyerr_scale = (x<=5)*(p_dxy[0]+p_dxy[1]*x)+(x>5&&x<=10)*(p_dxy[2]+p_dxy[3]*x)+(x>10&&x<=19)*(p_dxy[4]+p_dxy[5]*x)+(x>19&&x<=200)*(p_dxy[6]+p_dxy[7]*x)+(x>200)*(p_dxy[6]+p_dxy[7]*200);
	dzerr_scale = (x<=9)*(p_dz[0]+p_dz[1]*x)+(x>9&&x<=20)*(p_dz[2]+p_dz[3]*x)+(x>20&&x<=200)*(p_dz[4]+p_dz[5]*x+p_dz[6]*pow(x,2)+p_dz[7]*pow(x,3))+(x>200)*(p_dz[4]+p_dz[5]*200+p_dz[6]*pow(200,2)+p_dz[7]*pow(200,3));
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
	if (idim == i_dsz) {
	  const double cov_dz = tk->dzError() * tk->dzError();
	  const double cov_theta = tk->thetaError() * tk->thetaError();
	  cov(idim, i_dsz) = cov_dz * pow(dzerr_scale, 2) * pow(sin(tk->theta()), 2) + cov_theta * pow(tk->dz(), 2) * pow(cos(tk->theta()), 2); // neglecting dz/theta covariance cross term
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

DEFINE_FWK_MODULE(JMTRescaledTracks);
