#include "TH1F.h"
#include "TH2F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "RecoVertex/AdaptiveVertexFit/interface/AdaptiveVertexFitter.h"
#include "RecoVertex/ConfigurableVertexReco/interface/ConfigurableVertexReconstructor.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexUpdator.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexTrackCompatibilityEstimator.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexSmoother.h"
#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "TrackingTools/IPTools/interface/IPTools.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"

class MFVTrackVertexArbitrator : public edm::EDProducer {
public:
  MFVTrackVertexArbitrator(const edm::ParameterSet&);

  virtual void produce(edm::Event&, const edm::EventSetup&);

private:
  bool trackFilter(const reco::TrackRef&) const;

  const edm::InputTag primaryVertexCollection;
  const edm::InputTag secondaryVertexCollection;
  const edm::InputTag trackCollection;
  const edm::InputTag beamSpotCollection;
  const double dRCut;
  const double distCut;
  const double sigCut;
  const double dLenFraction;

  VertexDistance3D vdist;

  const bool do_histos;
  TH1F* h_ntracks;
  TH1F* h_dist;
  TH1F* h_sig;
  TH1F* h_w;
  TH1F* h_tkdpvsuccess;
  TH1F* h_tkdpv;
  TH1F* h_tkdpvsig;
  TH1F* h_tkdsvsuccess;
  TH1F* h_tkdsv;
  TH1F* h_tkdsvsig;
  TH2F* h_tkdsv_v_dpv;
  TH2F* h_tkdsvsig_v_dpvsig;
  TH1F* h_dr;
  TH2F* h_tkdsv_v_dR;
  TH2F* h_tkdsvsig_v_dR;
  TH1F* h_nselforsv;
  TH2F* h_nselforsv_v_svalready;
  TH1F* h_nnewvtx;
};

MFVTrackVertexArbitrator::MFVTrackVertexArbitrator(const edm::ParameterSet& cfg)
  : primaryVertexCollection  (cfg.getParameter<edm::InputTag>("primaryVertices")),
    secondaryVertexCollection(cfg.getParameter<edm::InputTag>("secondaryVertices")),
    trackCollection          (cfg.getParameter<edm::InputTag>("tracks")),
    beamSpotCollection       (cfg.getParameter<edm::InputTag>("beamSpot")),
    dRCut       (cfg.getParameter<double>("dRCut")),
    distCut     (cfg.getParameter<double>("distCut")),
    sigCut      (cfg.getParameter<double>("sigCut")),
    dLenFraction(cfg.getParameter<double>("dLenFraction")),
    do_histos(cfg.getParameter<bool>("do_histos"))
{
  produces<reco::VertexCollection>();

  if (do_histos) {
    edm::Service<TFileService> fs;
    h_ntracks = fs->make<TH1F>("h_ntracks", "", 50, 0, 1000);
    h_dist = fs->make<TH1F>("h_dist", "", 100, 0, 1);
    h_sig = fs->make<TH1F>("h_sig", "", 100, 0, 100);
    h_w = fs->make<TH1F>("h_w", "", 51, 0, 1.02);
    h_tkdpvsuccess = fs->make<TH1F>("h_tkdpvsuccess", "", 2, 0, 2);
    h_tkdpv = fs->make<TH1F>("h_tkdpv", "", 100, 0, 1);
    h_tkdpvsig = fs->make<TH1F>("h_tkdpvsig", "", 100, 0, 100);
    h_tkdsvsuccess = fs->make<TH1F>("h_tkdsvsuccess", "", 2, 0, 2);
    h_tkdsv = fs->make<TH1F>("h_tkdsv", "", 100, 0, 1);
    h_tkdsvsig = fs->make<TH1F>("h_tkdsvsig", "", 100, 0, 100);
    h_tkdsv_v_dpv = fs->make<TH2F>("h_tkdsv_v_dpv", "", 50, 0, 1, 50, 0, 1);
    h_tkdsvsig_v_dpvsig = fs->make<TH2F>("h_tkdsvsig_v_dpvsig", "", 50, 0, 100, 50, 0, 100);
    h_dr = fs->make<TH1F>("h_dr", "", 100, 0, 7);
    h_tkdsv_v_dR = fs->make<TH2F>("h_tkdsv_v_dR", "", 50, 0, 7, 50, 0, 1);
    h_tkdsvsig_v_dR = fs->make<TH2F>("h_tkdsvsig_v_dR", "", 50, 0, 7, 50, 0, 100);
    h_nselforsv = fs->make<TH1F>("h_nselforsv", "", 25, 0, 25);
    h_nselforsv_v_svalready = fs->make<TH2F>("h_nselforsv_v_svalready", "", 50, 0, 50, 25, 0, 25);
    h_nnewvtx = fs->make<TH1F>("h_nnewvtx", "", 50, 0, 50);
  }
}

bool MFVTrackVertexArbitrator::trackFilter(const reco::TrackRef& track) const {
  return
    track->hitPattern().trackerLayersWithMeasurement() >= 4 &&
    track->hitPattern().numberOfValidPixelHits() >= 1 &&
    track->pt() > 0.4;
}

void MFVTrackVertexArbitrator::produce(edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<reco::VertexCollection> primaryVertices;
  event.getByLabel(primaryVertexCollection, primaryVertices);

  std::auto_ptr<reco::VertexCollection> recoVertices(new reco::VertexCollection);

  if (primaryVertices->size() > 0) {
    const reco::Vertex& pv = primaryVertices->at(0);

    edm::Handle<reco::BeamSpot> beamSpot;
    event.getByLabel(beamSpotCollection, beamSpot);

    edm::Handle<reco::TrackCollection> tracks;
    event.getByLabel(trackCollection, tracks);

    edm::Handle<reco::VertexCollection> secondaryVertices;
    event.getByLabel(secondaryVertexCollection, secondaryVertices);
    
    edm::ESHandle<TransientTrackBuilder> trackBuilder;
    setup.get<TransientTrackRecord>().get("TransientTrackBuilder", trackBuilder);

    const double annealing_sigmacut = 3.0;
    const double annealing_Tini     = 256.;
    const double annealing_ratio    = 0.25;
    AdaptiveVertexFitter theAdaptiveFitter(GeometricAnnealing(annealing_sigmacut, annealing_Tini, annealing_ratio),
                                           DefaultLinearizationPointFinder(),
                                           KalmanVertexUpdator<5>(),
                                           KalmanVertexTrackCompatibilityEstimator<5>(),
                                           KalmanVertexSmoother());

    reco::TrackRefVector selectedTracks;
    for (size_t i = 0, ie = tracks->size(); i < ie; ++i) {
      reco::TrackRef tk(tracks, i);
      if (trackFilter(tk))
        selectedTracks.push_back(tk);
    }

    if (do_histos) h_ntracks->Fill(selectedTracks.size());
    
    for (std::vector<reco::Vertex>::const_iterator sv = secondaryVertices->begin(); sv != secondaryVertices->end(); ++sv) {
      GlobalPoint ppv(pv .position().x(), pv .position().y(), pv .position().z());
      GlobalPoint ssv(sv->position().x(), sv->position().y(), sv->position().z());
      GlobalVector flightDir = ssv - ppv;

      Measurement1D dlen = vdist.distance(pv, *sv);
      if (do_histos) h_dist->Fill(dlen.value());
      if (do_histos) h_sig->Fill(dlen.significance());
      std::vector<reco::TransientTrack> selTracks;

      for (unsigned int itrack = 0; itrack < selectedTracks.size(); itrack++) {
        reco::TrackRef tkref = selectedTracks[itrack];

        reco::TransientTrack tt = trackBuilder->build(tkref);
        tt.setBeamSpot(*beamSpot);
        float w = sv->trackWeight(tkref);
        if (do_histos) h_w->Fill(w);
        std::pair<bool,Measurement1D> ipv  = IPTools::absoluteImpactParameter3D(tt, pv);
        std::pair<bool,Measurement1D> isv  = IPTools::absoluteImpactParameter3D(tt, *sv);
        //        std::pair<bool,Measurement1D> itpv = IPTools::absoluteTransverseImpactParameter(tt, pv);
        float dR = reco::deltaR(flightDir, tt.track());

        if (do_histos) h_tkdpvsuccess->Fill(ipv.first);
        if (do_histos) h_tkdpv->Fill(ipv.second.value());
        if (do_histos) h_tkdpvsig->Fill(ipv.second.significance());

        if (do_histos) h_tkdsvsuccess->Fill(isv.first);
        if (do_histos) h_tkdsv->Fill(isv.second.value());
        if (do_histos) h_tkdsvsig->Fill(isv.second.significance());

        if (do_histos) h_tkdsv_v_dpv->Fill(ipv.second.value(), isv.second.value());
        if (do_histos) h_tkdsvsig_v_dpvsig->Fill(ipv.second.significance(), isv.second.significance());

        if (do_histos) h_dr->Fill(dR);
        if (do_histos) h_tkdsv_v_dR->Fill(dR, isv.second.value());
        if (do_histos) h_tkdsvsig_v_dR->Fill(dR, isv.second.significance());

        if (w > 0 || (isv.second.significance() < sigCut && isv.second.value() < distCut && isv.second.value() < dlen.value() * dLenFraction)) {
          if (isv.second.value() < ipv.second.value() && isv.second.value() < distCut && isv.second.value() < dlen.value()*dLenFraction && dR < dRCut)
            selTracks.push_back(tt);
          // add also the tracks used in previous fitting that are still closer to Sv than Pv 
          else if (w > 0.5 && isv.second.value() <= ipv.second.value() && dR < dRCut)
            selTracks.push_back(tt);
        }
      }

      if (do_histos) h_nselforsv->Fill(selTracks.size());
      if (do_histos) h_nselforsv_v_svalready->Fill(sv->nTracks(), selTracks.size());
      if (selTracks.size() >= 2) { 
        TransientVertex singleFitVertex = theAdaptiveFitter.vertex(selTracks,ssv);
        if (singleFitVertex.isValid())
          recoVertices->push_back(reco::Vertex(singleFitVertex));
      } 
    }
  }	

  if (do_histos) h_nnewvtx->Fill(recoVertices->size());
  event.put(recoVertices);
}

DEFINE_FWK_MODULE(MFVTrackVertexArbitrator);
