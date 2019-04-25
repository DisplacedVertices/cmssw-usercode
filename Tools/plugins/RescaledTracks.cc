#include <algorithm>
#include <numeric>
#include "CLHEP/Random/RandomEngine.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/RandomNumberGenerator.h"
#include "JMTucker/Formats/interface/TracksMap.h"

class JMTRescaledTracks : public edm::EDProducer {
public:
  explicit JMTRescaledTracks(const edm::ParameterSet&);

private:
  virtual void produce(edm::Event&, const edm::EventSetup&) override;

  const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
  const bool enable;

  class Scales {
    bool pick_;
    int which_;

    double dxyerr_;
    double dszerr_;
    double dxydszcov_;

    const std::vector<double> intlumis_;
    std::vector<double> rbreaks_;

  public:
    enum { w_JetHT2017B, w_JetHT2017C, w_JetHT2017D, w_JetHT2017E, w_JetHT2017F, w_JetHT2018A, w_JetHT2018B, w_JetHT2018C, w_JetHT2018D, max_which };

    Scales(bool pick, int which)
      : pick_(pick),
        which_(which),
        dxyerr_(1), dszerr_(1), dxydszcov_(1),
        intlumis_{4.794, 9.631, 4.248, 9.314, 13.534, 14.002, 7.092, 6.937, 31.894},
        rbreaks_(max_which)
    {
      assert(intlumis_.size() == max_which);
      const double sum = std::accumulate(intlumis_.begin(), intlumis_.end(), 0.);
      std::transform(intlumis_.begin(), intlumis_.end(), rbreaks_.begin(), [&sum](double x) { return x / sum; });
    }

    bool pick() const { return pick_; }
    int which() const { return which_; }
    double dxyerr() const { return dxyerr_; };
    double dszerr() const { return dszerr_; };
    double dxycov() const { return dxyerr_ * dxyerr_; };
    double dszcov() const { return dszerr_ * dszerr_; };
    double dxydszcov() const { return dxydszcov_; };

    void JetHT2017B(double x, double eta) { // x is pt
      if (fabs(eta) < 1.5) {
        const double p_dxy[8] = {1.003954411196716, 0.04680608038556485, 1.1651640253424076, 0.010686515626581808, 1.2423728669230774, 0.002510211465163767, 1.301491397216935, -0.0005992241020962791};
        const double p_dsz[10] = {1.0245229183638793, 0.06544824469215105, 1.1860096333638355, 0.009315198253046261, 1.2534005803324926, -0.0010188848309496473, 1.2759550243574909, -0.0033600655572815436, 2.0547714269037252e-05, -3.967354320030131e-08};
        const double p_dxydsz[5] = {1.2373808693167834, -0.06306772746156655, 0.9989407561722071, 0.004296811774057659, 1.0281436760070548};

        dxyerr_ = (x<=5)*(p_dxy[0]+p_dxy[1]*x)+(x>5&&x<=10)*(p_dxy[2]+p_dxy[3]*x)+(x>10&&x<=19)*(p_dxy[4]+p_dxy[5]*x)+(x>19&&x<=200)*(p_dxy[6]+p_dxy[7]*x)+(x>200)*(p_dxy[6]+p_dxy[7]*200);
        dszerr_ = (x<=3)*(p_dsz[0]+p_dsz[1]*x)+(x>3&&x<=7)*(p_dsz[2]+p_dsz[3]*x)+(x>7&&x<=11)*(p_dsz[4]+p_dsz[5]*x)+(x>11&&x<=200)*(p_dsz[6]+p_dsz[7]*x+p_dsz[8]*pow(x,2)+p_dsz[9]*pow(x,3))+(x>200)*(p_dsz[6]+p_dsz[7]*200+p_dsz[8]*pow(200,2)+p_dsz[9]*pow(200,3));
        dxydszcov_ = (x<=3.5)*(p_dxydsz[0]+p_dxydsz[1]*x)+(x>3.5&&x<=20)*(p_dxydsz[2]+p_dxydsz[3]*x)+(x>20)*p_dxydsz[4];
      }
      else {
        const double p_dxy[8] = {0.9809194238515303, 0.02988345020861421, 1.0494209346433279, 0.01638247946618149, 1.1747904134913318, 0.004173705981459077, 1.27170013468283, -0.0015234534159011834};
        const double p_dsz[7] = {0.9741157497540216, 0.03454031770932743, 1.1551685052673273, 0.008041427889944022, 1.3366714462830347, -0.0034743381492504328, 1.3448120785319356e-05};
        const double p_dxydsz[5] = {1.1772587629670426, -0.012843798533138594, 1.097301005478153, -0.005013846780833367, 0.952633219303397};

        dxyerr_ = (x<=5)*(p_dxy[0]+p_dxy[1]*x)+(x>5&&x<=10)*(p_dxy[2]+p_dxy[3]*x)+(x>10&&x<=19)*(p_dxy[4]+p_dxy[5]*x)+(x>19&&x<=200)*(p_dxy[6]+p_dxy[7]*x)+(x>200)*(p_dxy[6]+p_dxy[7]*200);
        dszerr_ = (x<=7)*(p_dsz[0]+p_dsz[1]*x)+(x>7&&x<=17)*(p_dsz[2]+p_dsz[3]*x)+(x>17&&x<=200)*(p_dsz[4]+p_dsz[5]*x+p_dsz[6]*pow(x,2))+(x>200)*(p_dsz[4]+p_dsz[5]*200+p_dsz[6]*pow(200,2));
        dxydszcov_ = (x<=5)*(p_dxydsz[0]+p_dxydsz[1]*x)+(x>5&&x<=21)*(p_dxydsz[2]+p_dxydsz[3]*x)+(x>21)*p_dxydsz[4];
      }
    }

    void JetHT2017C(double x, double eta) { assert(0); };
    void JetHT2017D(double x, double eta) { assert(0); };
    void JetHT2017E(double x, double eta) { assert(0); };
    void JetHT2017F(double x, double eta) { assert(0); };
    void JetHT2018A(double x, double eta) { assert(0); };
    void JetHT2018B(double x, double eta) { assert(0); };
    void JetHT2018C(double x, double eta) { assert(0); };
    void JetHT2018D(double x, double eta) { assert(0); };

    void pick_era(double r) {
      if (!pick_) return;
      assert(r >= 0 && r <= 1);
      for (int i = 0; i < max_which; ++i)
        if (r < rbreaks_[i]) {
          which_ = i;
          break;
        }
    }

    void set(double pt, double eta) {
      int w = abs(which_);
      if      (w == w_JetHT2017B) JetHT2017B(pt,eta);
      else if (w == w_JetHT2017C) JetHT2017C(pt,eta);
      else if (w == w_JetHT2017D) JetHT2017D(pt,eta);
      else if (w == w_JetHT2017E) JetHT2017E(pt,eta);
      else if (w == w_JetHT2017F) JetHT2017F(pt,eta);
      else if (w == w_JetHT2018A) JetHT2018A(pt,eta);
      else if (w == w_JetHT2018B) JetHT2018B(pt,eta);
      else if (w == w_JetHT2018C) JetHT2018C(pt,eta);
      else if (w == w_JetHT2018D) JetHT2018D(pt,eta);
      else
        throw cms::Exception("Misconfiguration", "bad which") << which_;
    }
  } scales;
};

JMTRescaledTracks::JMTRescaledTracks(const edm::ParameterSet& cfg) 
  : tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("tracks_src"))),
    enable(cfg.getParameter<bool>("enable")),
    scales(enable && cfg.getParameter<bool>("pick"), cfg.getParameter<int>("which"))
{
  edm::Service<edm::RandomNumberGenerator> rng;
  if (scales.pick() && !rng.isAvailable())
    throw cms::Exception("RescaledTracks", "RandomNumberGeneratorService not available");

  produces<reco::TrackCollection>();
  produces<jmt::TracksMap>();
}

void JMTRescaledTracks::produce(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<reco::TrackCollection> tracks;
  event.getByToken(tracks_token, tracks);

  auto output_tracks = std::make_unique<reco::TrackCollection>();
  auto output_tracks_map = std::make_unique<jmt::TracksMap>();

  reco::TrackRefProd h_output_tracks = event.getRefBeforePut<reco::TrackCollection>();

  if (!event.isRealData() && enable && scales.pick()) {
    edm::Service<edm::RandomNumberGenerator> rng;
    scales.pick_era(rng->getEngine(event.streamID()).flat());
  }

  for (size_t i = 0, ie = tracks->size(); i < ie; ++i) {
    reco::TrackRef tk(tracks, i);
    reco::TrackBase::CovarianceMatrix cov = tk->covariance();

    if (!event.isRealData() && enable) {
      scales.set(tk->pt(), tk->eta());

      const int i_dxy = reco::TrackBase::i_dxy;
      const int i_dsz = reco::TrackBase::i_dsz;

      for (int idim = 0; idim < reco::TrackBase::dimension; ++idim) {
	if (idim == i_dxy) cov(idim, i_dxy) *= scales.dxycov();
	else               cov(idim, i_dxy) *= scales.dxyerr();
      }

      for (int idim = 0; idim < reco::TrackBase::dimension; ++idim) {
	if (idim == i_dsz) cov(idim, i_dsz) *= scales.dszcov();
	else               cov(idim, i_dsz) *= scales.dszerr();
      }

      cov(i_dxy, i_dsz) *= scales.dxydszcov();
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
