#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/Math/interface/Point3D.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/ExtValue.h"
#include "JMTucker/Tools/interface/PairwiseHistos.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/Tools/interface/TrackRescaler.h"
#include "JMTucker/Tools/interface/AnalysisEras.h"
#include "JMTucker/MFVNeutralinoFormats/interface/JetVertexAssociation.h"
#include "TLorentzVector.h"

class MFVTrackHistos : public edm::EDAnalyzer {
  public:
    explicit MFVTrackHistos(const edm::ParameterSet&);
    void analyze(const edm::Event&, const edm::EventSetup&);
  private:
    const edm::EDGetTokenT<MFVEvent> mevent_token;
    const edm::EDGetTokenT<double> weight_token;
    const edm::EDGetTokenT<reco::TrackCollection> track_token;
    const int max_ntrack;

    jmt::TrackRescaler track_rescaler;

    TH1F* h_w;
    TH1F* h_all_track_n;
    TH1F* h_all_track_pt;
    TH1F* h_all_track_eta;
    TH1F* h_all_track_phi;
    TH1F* h_all_track_dxybs;
    TH1F* h_all_track_dxybe_sig;
    TH1F* h_all_track_dz;
    TH1F* h_all_track_dz_sig;
    TH1F* h_leading_track_n;
    TH1F* h_leading_track_pt;
    TH1F* h_leading_track_eta;
    TH1F* h_leading_track_phi;
    TH1F* h_leading_track_dxybs;
    TH1F* h_leading_track_dxybe_sig;
    TH1F* h_leading_track_dz;
    TH1F* h_leading_track_dz_sig;

};


MFVTrackHistos::MFVTrackHistos(const edm::ParameterSet& cfg)
    : mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
      weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
      track_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("track_src"))),
      max_ntrack(cfg.getParameter<int>("max_ntrack"))
{
  edm::Service<TFileService> fs;

  h_w = fs->make<TH1F>("h_w", ";event weight;events/0.1", 100, 0, 10);

  h_all_track_n = fs->make<TH1F>("h_all_track_n", ";# tracks;events",200,0,200);
  h_all_track_pt = fs->make<TH1F>("h_all_track_pt", ";all track p_{T} (GeV); events",2000,0,2000);
  h_all_track_eta = fs->make<TH1F>("h_all_track_eta", ";all track #eta; events",50,-4,4);
  h_all_track_phi = fs->make<TH1F>("h_all_track_phi", ";all track #phi; events", 50, -3.15, 3.15);
  h_all_track_dxybs = fs->make<TH1F>("h_all_track_dxybs", ";all track dxybs (cm)", 100, -1, 1);
  h_all_track_dxybe_sig = fs->make<TH1F>("h_all_track_dxybe_sig", "; all track #sigma(dxybs); events", 400, -40, 40);
  h_all_track_dz = fs->make<TH1F>("h_all_track_dz", ";all track dz (cm); events", 500, -35, 35);
  h_all_track_dz_sig = fs->make<TH1F>("h_all_track_dz_sig", ";all track #sigma(dz);events",200,-20000,20000);

  h_leading_track_n = fs->make<TH1F>("h_leading_track_n", ";# tracks;events",200,0,200);
  h_leading_track_pt = fs->make<TH1F>("h_leading_track_pt", ";all track p_{T} (GeV); events",2000,0,2000);
  h_leading_track_eta = fs->make<TH1F>("h_leading_track_eta", ";all track #eta; events",50,-4,4);
  h_leading_track_phi = fs->make<TH1F>("h_leading_track_phi", ";all track #phi; events", 50, -3.15, 3.15);
  h_leading_track_dxybs = fs->make<TH1F>("h_leading_track_dxybs", ";all track dxybs (cm)", 100, -1, 1);
  h_leading_track_dxybe_sig = fs->make<TH1F>("h_leading_track_dxybe_sig", "; all track #sigma(dxybs); events", 400, -40, 40);
  h_leading_track_dz = fs->make<TH1F>("h_leading_track_dz", ";all track dz (cm); events", 500, -35, 35);
  h_leading_track_dz_sig = fs->make<TH1F>("h_leading_track_dz_sig", ";all track #sigma(dz);events",200,-20000,20000);
}

void MFVTrackHistos::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<MFVEvent> mevent;
  event.getByToken(mevent_token, mevent);

  edm::Handle<double> weight;
  event.getByToken(weight_token, weight);
  const double w = *weight;
  h_w->Fill(w);

  edm::Handle<reco::TrackCollection> tracks;
  event.getByToken(track_token, tracks);

  double bsx = mevent->bsx;
  double bsy = mevent->bsy;
  double bsz = mevent->bsz;
  const math::XYZPoint bs(bsx, bsy, bsz);

  const int track_rescaler_which = jmt::TrackRescaler::w_JetHT; // JMTBAD which rescaling if ever a different one
  track_rescaler.setup(!event.isRealData() && track_rescaler_which != -1,
                       jmt::AnalysisEras::pick(event.id().event()),
                       //jmt::AnalysisEras::pick(event, this),
                       track_rescaler_which);

  double min_track_pt = 1.0;
  double min_track_nhits = 0;
  double min_track_npxhits = 0;
  double min_track_npxlayers = 2;
  double min_track_nstlayers = 6;
  double min_track_hit_r = 1;
  int ntracks = 0;

  for (size_t i = 0, ie = tracks->size(); i < ie; ++i){
    const reco::TrackRef& tk = reco::TrackRef(tracks, i);
    const auto rs = track_rescaler.scale(*tk);

    const double pt = tk->pt();
    const double dxybs = tk->dxy(bs);
    const double rescaled_dxyerr = rs.rescaled_tk.dxyError();
    const double rescaled_sigmadxybs = dxybs / rescaled_dxyerr;
    const double dzbs = tk->dz(bs);
    const double rescaled_dzerr = rs.rescaled_tk.dzError();
    const double rescaled_sigmadzbs = dzbs / rescaled_dzerr;
    const int nhits = tk->hitPattern().numberOfValidHits();
    const int npxhits = tk->hitPattern().numberOfValidPixelHits();
    //const int nsthits = tk->hitPattern().numberOfValidStripHits();
    const int npxlayers = tk->hitPattern().pixelLayersWithMeasurement();
    const int nstlayers = tk->hitPattern().stripLayersWithMeasurement();
    int min_r = 2000000000;
    for (int i = 1; i <= 4; ++i)
      if (tk->hitPattern().hasValidHitInPixelLayer(PixelSubdetector::PixelBarrel,i)) {
        min_r = i;
        break;
      }

    const bool use =
      pt > min_track_pt &&
      nhits >= min_track_nhits &&
      npxhits >= min_track_npxhits &&
      npxlayers >= min_track_npxlayers &&
      nstlayers >= min_track_nstlayers &&
      (min_track_hit_r == 999 || min_r <= min_track_hit_r);

    if (use) {
      ++ntracks;
      h_all_track_pt->Fill(pt, w);
      h_all_track_eta->Fill(tk->eta(), w);
      h_all_track_phi->Fill(tk->phi(), w);
      h_all_track_dxybs->Fill(dxybs, w);
      h_all_track_dxybe_sig->Fill(rescaled_sigmadxybs, w);
      h_all_track_dz->Fill(dzbs, w);
      h_all_track_dz_sig->Fill(rescaled_sigmadzbs, w);
      if (ntracks<max_ntrack){
        h_leading_track_pt->Fill(pt, w);
        h_leading_track_eta->Fill(tk->eta(), w);
        h_leading_track_phi->Fill(tk->phi(), w);
        h_leading_track_dxybs->Fill(dxybs, w);
        h_leading_track_dxybe_sig->Fill(rescaled_sigmadxybs, w);
        h_leading_track_dz->Fill(dzbs, w);
        h_leading_track_dz_sig->Fill(rescaled_sigmadzbs, w);
      }
    }
  }
  h_all_track_n->Fill(ntracks, w);
  h_leading_track_n->Fill(ntracks>=max_ntrack?max_ntrack:ntracks, w);

}
DEFINE_FWK_MODULE(MFVTrackHistos);
