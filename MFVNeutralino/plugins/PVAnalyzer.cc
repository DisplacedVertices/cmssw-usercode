#include <memory>
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH1.h"
#include <iostream>
class PVAnalyzer : public edm::EDAnalyzer {
   public:
      explicit PVAnalyzer(const edm::ParameterSet&);
      ~PVAnalyzer();

   private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  TH1F* h_npv;

  TH1F* h_ntracks[4];
  TH1F* h_track_pt[4];
  TH1F* h_track_eta[4];
  TH1F* h_track_phi[4];
  TH1F* h_track_dxybs[4];
  TH1F* h_track_dxypv[4];
  TH1F* h_track_dzbs[4];
  TH1F* h_track_dzpv[4];

  TH1F* h_track_pterr[4];
  TH1F* h_track_etaerr[4];
  TH1F* h_track_phierr[4];
  TH1F* h_track_dxyerr[4];
  TH1F* h_track_dzerr[4];
  
  TH1F* h_track_sigmapt[4];
  TH1F* h_track_sigmaeta[4];
  TH1F* h_track_sigmaphi[4];
  TH1F* h_track_sigmadxybs[4];
  TH1F* h_track_sigmadxypv[4];
  TH1F* h_track_sigmadzbs[4];
  TH1F* h_track_sigmadzpv[4];

  TH1F* h_track_chi2dof[4];
  TH1F* h_track_npxhits[4];
  TH1F* h_track_nsthits[4];
  TH1F* h_track_npxlayers[4];
  TH1F* h_track_nstlayers[4];

  const edm::InputTag primary_vertices_src;
  const edm::InputTag track_src;
  const edm::InputTag beamspot_src;

  const bool use_only_pv_tracks;
  const bool use_only_pvs_tracks;
  const double maxNormChi2;
  const int minPxLayer;
  const int minSilLayer;
};

PVAnalyzer::PVAnalyzer(const edm::ParameterSet& iConfig)
  : primary_vertices_src(iConfig.getParameter<edm::InputTag>("primary_vertices_src")),
    track_src(iConfig.getParameter<edm::InputTag>("track_src")),
    beamspot_src(iConfig.getParameter<edm::InputTag>("beamspot_src")),
    use_only_pv_tracks(iConfig.getParameter<bool>("use_only_pv_tracks")),
    use_only_pvs_tracks(iConfig.getParameter<bool>("use_only_pvs_tracks")),
    maxNormChi2(iConfig.getParameter<double>("maxNormChi2")),
    minPxLayer(iConfig.getParameter<int>("minPxLayer")),
    minSilLayer(iConfig.getParameter<int>("minSilLayer"))
{
  edm::Service<TFileService> fs;
  const char* categories[4] = {"all_pv", "pv0", "other_pvs", "non_pv"};

  h_npv = fs->make<TH1F>("h_npv", ";# of primary vertices; arb. units", 50, 0, 50);

  for (int i = 0; i < 4; ++i) {
    h_ntracks[i] = fs->make<TH1F>(TString::Format("h_%s_ntracks", categories[i]), "ntracks; arb. units", 200, 0, 200);
    h_track_pt[i]  = fs->make<TH1F>(TString::Format("h_%s_track_pt", categories[i]), ";p_{T} (GeV); arb. units", 300, 0, 150);
    h_track_eta[i] = fs->make<TH1F>(TString::Format("h_%s_track_eta", categories[i]), ";eta; arb. units", 50, -4, 4);
    h_track_phi[i] = fs->make<TH1F>(TString::Format("h_%s_track_phi", categories[i]), ";phi; arb. units", 50, -3.15, 3.15);
    h_track_dxybs[i] = fs->make<TH1F>(TString::Format("h_%s_track_dxybs", categories[i]), ";dxy w.r.t. bs (cm); arb. units", 1000, -2, 2);
    h_track_dxypv[i] = fs->make<TH1F>(TString::Format("h_%s_track_dxypv", categories[i]), ";dxy w.r.t. pv (cm); arb. units", 1000, -2, 2);
    h_track_dzbs[i]  = fs->make<TH1F>(TString::Format("h_%s_track_dzbs", categories[i]), ";dz w.r.t. bs (cm); arb. units", 1000, -25, 25);
    h_track_dzpv[i] = fs->make<TH1F>(TString::Format("h_%s_track_dzpv", categories[i]), ";dz w.r.t. pv (cm); arb. units", 1000, -25, 25);

    h_track_pterr[i]  = fs->make<TH1F>(TString::Format("h_%s_track_pterr", categories[i]), ";error in p_{T} (GeV); arb. units", 50, 0, 0.25);
    h_track_etaerr[i] = fs->make<TH1F>(TString::Format("h_%s_track_etaerr", categories[i]), ";eta error; arb. units", 50, 0, 0.1);
    h_track_phierr[i] = fs->make<TH1F>(TString::Format("h_%s_track_phierr", categories[i]), ";phi error; arb. units", 50, 0, 0.1);
    h_track_dxyerr[i] = fs->make<TH1F>(TString::Format("h_%s_track_dxyerr", categories[i]), ";dxy error; arb. units", 300, 0, 0.5);
    h_track_dzerr[i]  = fs->make<TH1F>(TString::Format("h_%s_track_dzerr", categories[i]), ";dz error; arb. units", 300, 0, 1);

    h_track_sigmapt[i]  = fs->make<TH1F>(TString::Format("h_%s_track_sigmapt", categories[i]), ";pt/ptError; arb. units", 400, 0, 250);
    h_track_sigmaeta[i] = fs->make<TH1F>(TString::Format("h_%s_track_sigmaeta", categories[i]), ";eta/etaError; arb. units", 1600, -800, 800);
    h_track_sigmaphi[i] = fs->make<TH1F>(TString::Format("h_%s_track_sigmaphi", categories[i]), ";phi/phiError; arb. units", 1600, -800, 800);
    h_track_sigmadxybs[i] = fs->make<TH1F>(TString::Format("h_%s_track_sigmadxybs", categories[i]), ";dxy/dxyError; arb. units", 300, -15, 15);
    h_track_sigmadxypv[i] = fs->make<TH1F>(TString::Format("h_%s_track_sigmadxypv", categories[i]), ";dxy/dxyError; arb. units", 300, -15, 15);
    h_track_sigmadzbs[i]  = fs->make<TH1F>(TString::Format("h_%s_track_sigmadzbs", categories[i]), ";dz/dzError; arb. units", 1600, -800, 800);
    h_track_sigmadzpv[i] = fs->make<TH1F>(TString::Format("h_%s_track_sigmadzpv", categories[i]), ";dz/dzError; arb. units", 1600, -800, 800);

    h_track_chi2dof[i] = fs->make<TH1F>(TString::Format("h_%s_track_chi2dof", categories[i]), ";#chi^2/dof; arb. units", 50, 0, 7);
    h_track_npxhits[i] = fs->make<TH1F>(TString::Format("h_%s_track_npxhits", categories[i]), ";# of pixel hits; arb. units", 15, 0, 15);
    h_track_nsthits[i] = fs->make<TH1F>(TString::Format("h_%s_track_nsthits", categories[i]), ";# of strip hits; arb. units", 45, 0, 45);
    h_track_npxlayers[i] = fs->make<TH1F>(TString::Format("h_%s_track_npxlayers", categories[i]), ";# pixel layer hits; arb. units", 6, 0, 6);
    h_track_nstlayers[i] = fs->make<TH1F>(TString::Format("h_%s_track_nstlayers", categories[i]), ";# strip layer hits; arb. units", 20, 0, 20);
  }
}


PVAnalyzer::~PVAnalyzer()
{
}


void PVAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;

   Handle<reco::VertexCollection> primary_vertices;
   iEvent.getByLabel(primary_vertices_src, primary_vertices);

   Handle<reco::TrackCollection> tracks;
   iEvent.getByLabel(track_src, tracks);
  
   Handle<reco::BeamSpot> beamspot;
   iEvent.getByLabel(beamspot_src, beamspot);

   std::vector<reco::TrackRef> all_tracks;
   std::vector<reco::TrackRef> main_pv_tracks;
   std::vector<reco::TrackRef> other_pvs_tracks;
   std::vector<reco::TrackRef> non_pv_tracks;

   std::map<reco::TrackRef, std::vector<std::pair<int, float> > > tracks_in_pvs;
   std::map<reco::TrackRef, std::vector<std::pair<int, float> > > tracks_in_main_pv;
   std::map<reco::TrackRef, std::vector<std::pair<int, float> > > tracks_in_other_pvs;
   std::map<reco::TrackRef, math::XYZPoint> positions;

   for (size_t i = 0, ie = primary_vertices->size(); i < ie; ++i) {
     const reco::Vertex& pv = primary_vertices->at(i);
     for (auto it = pv.tracks_begin(), ite = pv.tracks_end(); it != ite; ++it) {
       float w = pv.trackWeight(*it);
       reco::TrackRef tk = it->castTo<reco::TrackRef>();
       tracks_in_pvs[tk].push_back(std::make_pair(i, w));
       positions[tk] = pv.position();
       h_ntracks[0]->Fill(pv.tracksSize());
     }

     if(i == 0) {
       for (auto it = pv.tracks_begin(), ite = pv.tracks_end(); it != ite; ++it) {
	 float w = pv.trackWeight(*it);
	 reco::TrackRef tk = it->castTo<reco::TrackRef>();
	 tracks_in_main_pv[tk].push_back(std::make_pair(i, w));
       }
       h_ntracks[1]->Fill(pv.tracksSize());
     } else {
       for (auto it = pv.tracks_begin(), ite = pv.tracks_end(); it != ite; ++it) {
         float w = pv.trackWeight(*it);
	 reco::TrackRef tk = it->castTo<reco::TrackRef>();
         tracks_in_other_pvs[tk].push_back(std::make_pair(i, w));
       }
       h_ntracks[2]->Fill(pv.tracksSize());
     }
   }
   for (size_t i = 0, ie = tracks->size(); i < ie; ++i) {
      reco::TrackRef tkref(tracks, i);
     
      bool ok_all = false;
      bool ok_main = false;
      bool ok_other = false;

      for (const auto& pv_use : tracks_in_pvs[tkref])
        if (use_only_pvs_tracks || (use_only_pv_tracks && pv_use.first == 0)) {
          ok_all = true;
          break;
        }

      for (const auto& pv_use : tracks_in_main_pv[tkref])
        if (use_only_pvs_tracks || (use_only_pv_tracks && pv_use.first == 0)) {
          ok_main = true;
          break;
        }

      for (const auto& pv_use : tracks_in_other_pvs[tkref])
        if (use_only_pvs_tracks || (use_only_pv_tracks && pv_use.first == 0)) {
          ok_other = true;
          break;
        }
      if (ok_all)
        all_tracks.push_back(tkref);
      else 
	non_pv_tracks.push_back(tkref);

      if (ok_main)
        main_pv_tracks.push_back(tkref);

      if (ok_other)
        other_pvs_tracks.push_back(tkref);
    }
   for (size_t i = 0, ie = all_tracks.size(); i < ie; ++i) {
     const reco::TrackRef& tk = all_tracks[i];

     const double pt = tk->pt();
     const double eta = tk->eta();
     const double phi = tk->phi();
     const double dxybs = tk->dxy(*beamspot);
     const double dxypv = tk->dxy(positions[tk]);
     const double dzbs = tk->dz(beamspot->position());
     const double dzpv = tk->dz(positions[tk]);
     const double ptErr = tk->ptError();
     const double etaErr = tk->etaError();
     const double phiErr = tk->phiError();
     const double dxyErr = tk->dxyError();
     const double dzErr = tk->dzError();
     const double chi2dof = tk->normalizedChi2();
     const int npxhits = tk->hitPattern().numberOfValidPixelHits();
     const int nsthits = tk->hitPattern().numberOfValidStripHits();
     const int npxlayers = tk->hitPattern().pixelLayersWithMeasurement();
     const int nstlayers = tk->hitPattern().stripLayersWithMeasurement();

     bool use = maxNormChi2 > chi2dof && npxlayers >= minPxLayer && nstlayers >= minSilLayer; 
     
     if(use) {
       h_track_pt[0]->Fill(pt);
       h_track_eta[0]->Fill(eta);
       h_track_phi[0]->Fill(phi);
       h_track_dxybs[0]->Fill(dxybs);
       h_track_dxypv[0]->Fill(dxypv);
       h_track_dzbs[0]->Fill(dzbs);
       h_track_dzpv[0]->Fill(dzpv);
       h_track_pterr[0]->Fill(ptErr);
       h_track_etaerr[0]->Fill(etaErr);
       h_track_phierr[0]->Fill(phiErr);
       h_track_dxyerr[0]->Fill(dxyErr);
       h_track_dzerr[0]->Fill(dzErr);
       h_track_sigmapt[0]->Fill(pt/ptErr);
       h_track_sigmaeta[0]->Fill(eta/etaErr);
       h_track_sigmaphi[0]->Fill(phi/phiErr);
       h_track_sigmadxybs[0]->Fill(dxybs/dxyErr);
       h_track_sigmadxypv[0]->Fill(dxypv/dxyErr);
       h_track_sigmadzbs[0]->Fill(dzbs/dzErr);
       h_track_sigmadzpv[0]->Fill(dzpv/dzErr);
       h_track_chi2dof[0]->Fill(chi2dof);
       h_track_npxhits[0]->Fill(npxhits);
       h_track_nsthits[0]->Fill(nsthits);
       h_track_npxlayers[0]->Fill(npxlayers);
       h_track_nstlayers[0]->Fill(nstlayers);
     }
   }

   for (size_t i = 0, ie = main_pv_tracks.size(); i < ie; ++i) {
     const reco::TrackRef& tk = main_pv_tracks[i];
     const double pt = tk->pt();
     const double eta = tk->eta();
     const double phi = tk->phi();
     const double dxybs = tk->dxy(*beamspot);
     const double dxypv = tk->dxy(positions[tk]);
     const double dzbs = tk->dz(beamspot->position());
     const double dzpv = tk->dz(positions[tk]);
     const double ptErr = tk->ptError();
     const double etaErr = tk->etaError();
     const double phiErr = tk->phiError();
     const double dxyErr = tk->dxyError();
     const double dzErr = tk->dzError();
     const double chi2dof = tk->normalizedChi2();
     const int npxhits = tk->hitPattern().numberOfValidPixelHits();
     const int nsthits = tk->hitPattern().numberOfValidStripHits();
     const int npxlayers = tk->hitPattern().pixelLayersWithMeasurement();
     const int nstlayers = tk->hitPattern().stripLayersWithMeasurement();
  
     bool use = maxNormChi2 > chi2dof && npxlayers >= minPxLayer && nstlayers >= minSilLayer;

     if(use) {
       h_track_pt[1]->Fill(pt);  
       h_track_eta[1]->Fill(eta);
       h_track_phi[1]->Fill(phi);
       h_track_dxybs[1]->Fill(dxybs);
       h_track_dxypv[1]->Fill(dxypv);
       h_track_dzbs[1]->Fill(dzbs);
       h_track_dzpv[1]->Fill(dzpv);
       h_track_pterr[1]->Fill(ptErr);
       h_track_etaerr[1]->Fill(etaErr);
       h_track_phierr[1]->Fill(phiErr);
       h_track_dxyerr[1]->Fill(dxyErr);
       h_track_dzerr[1]->Fill(dzErr);
       h_track_sigmapt[1]->Fill(pt/ptErr);
       h_track_sigmaeta[1]->Fill(eta/etaErr);
       h_track_sigmaphi[1]->Fill(phi/phiErr);
       h_track_sigmadxybs[1]->Fill(dxybs/dxyErr);
       h_track_sigmadxypv[1]->Fill(dxypv/dxyErr);
       h_track_sigmadzbs[1]->Fill(dzbs/dzErr);
       h_track_sigmadzpv[1]->Fill(dzpv/dzErr);
       h_track_chi2dof[1]->Fill(chi2dof);
       h_track_npxhits[1]->Fill(npxhits);
       h_track_nsthits[1]->Fill(nsthits);
       h_track_npxlayers[1]->Fill(npxlayers);
       h_track_nstlayers[1]->Fill(nstlayers);
     }
   }

   for (size_t i = 0, ie = other_pvs_tracks.size(); i < ie; ++i) {
     const reco::TrackRef& tk = other_pvs_tracks[i];
     const double pt = tk->pt();
     const double eta = tk->eta();
     const double phi = tk->phi();
     const double dxybs = tk->dxy(*beamspot);
     const double dxypv = tk->dxy(positions[tk]);
     const double dzbs = tk->dz(beamspot->position());
     const double dzpv = tk->dz(positions[tk]);
     const double ptErr = tk->ptError();
     const double etaErr = tk->etaError();
     const double phiErr = tk->phiError();
     const double dxyErr = tk->dxyError();
     const double dzErr = tk->dzError();
     const double chi2dof = tk->chi2() / tk->ndof();
     const int npxhits = tk->hitPattern().numberOfValidPixelHits();
     const int nsthits = tk->hitPattern().numberOfValidStripHits();
     const int npxlayers = tk->hitPattern().pixelLayersWithMeasurement();
     const int nstlayers = tk->hitPattern().stripLayersWithMeasurement();

     bool use = maxNormChi2 > chi2dof && npxlayers >= minPxLayer && nstlayers >= minSilLayer;
     
     if(use) {
       h_track_pt[2]->Fill(pt);
       h_track_eta[2]->Fill(eta);
       h_track_phi[2]->Fill(phi);
       h_track_dxybs[2]->Fill(dxybs);
       h_track_dxypv[2]->Fill(dxypv);
       h_track_dzbs[2]->Fill(dzbs);
       h_track_dzpv[2]->Fill(dzpv);
       h_track_pterr[2]->Fill(ptErr);
       h_track_etaerr[2]->Fill(etaErr);
       h_track_phierr[2]->Fill(phiErr);
       h_track_dxyerr[2]->Fill(dxyErr);
       h_track_dzerr[2]->Fill(dzErr);
       h_track_sigmapt[2]->Fill(pt/ptErr);
       h_track_sigmaeta[2]->Fill(eta/etaErr);
       h_track_sigmaphi[2]->Fill(phi/phiErr);
       h_track_sigmadxybs[2]->Fill(dxybs/dxyErr);
       h_track_sigmadxypv[2]->Fill(dxypv/dxyErr);
       h_track_sigmadzbs[2]->Fill(dzbs/dzErr);
       h_track_sigmadzpv[2]->Fill(dzpv/dzErr);
       h_track_chi2dof[2]->Fill(chi2dof);
       h_track_npxhits[2]->Fill(npxhits);
       h_track_nsthits[2]->Fill(nsthits);
       h_track_npxlayers[2]->Fill(npxlayers);
       h_track_nstlayers[2]->Fill(nstlayers);
     }
   }

   for (size_t i = 0, ie = non_pv_tracks.size(); i < ie; ++i) {
     const reco::TrackRef& tk = non_pv_tracks[i];
     const double pt = tk->pt();
     const double eta = tk->eta();
     const double phi = tk->phi();
     const double dxybs = tk->dxy(*beamspot);
     const double dxypv = tk->dxy(positions[tk]);
     const double dzbs = tk->dz(beamspot->position());
     double dzpv = tk->dz(beamspot->position());
     if(primary_vertices->size() != 0)
       dzpv = tk->dz(primary_vertices->at(0).position());
     const double ptErr = tk->ptError();
     const double etaErr = tk->etaError();
     const double phiErr = tk->phiError();
     const double dxyErr = tk->dxyError();
     const double dzErr = tk->dzError();
     const double chi2dof = tk->chi2() / tk->ndof();
     const int npxhits = tk->hitPattern().numberOfValidPixelHits();
     const int nsthits = tk->hitPattern().numberOfValidStripHits();
     const int npxlayers = tk->hitPattern().pixelLayersWithMeasurement();
     const int nstlayers = tk->hitPattern().stripLayersWithMeasurement();

     bool use = maxNormChi2 > chi2dof && npxlayers >= minPxLayer && nstlayers >= minSilLayer;
     
     if(use) {
       h_track_pt[3]->Fill(pt);
       h_track_eta[3]->Fill(eta);
       h_track_phi[3]->Fill(phi);
       h_track_dxybs[3]->Fill(dxybs);
       h_track_dxypv[3]->Fill(dxypv);
       h_track_dzbs[3]->Fill(dzbs);
       h_track_dzpv[3]->Fill(dzpv);
       h_track_pterr[3]->Fill(ptErr);
       h_track_etaerr[3]->Fill(etaErr);
       h_track_phierr[3]->Fill(phiErr);
       h_track_dxyerr[3]->Fill(dxyErr);
       h_track_dzerr[3]->Fill(dzErr);
       h_track_sigmapt[3]->Fill(pt/ptErr);
       h_track_sigmaeta[3]->Fill(eta/etaErr);
       h_track_sigmaphi[3]->Fill(phi/phiErr);
       h_track_sigmadxybs[3]->Fill(dxybs/dxyErr);
       h_track_sigmadxypv[3]->Fill(dxypv/dxyErr);
       h_track_sigmadzbs[3]->Fill(dzbs/dzErr);
       h_track_sigmadzpv[3]->Fill(dzpv/dzErr);
       h_track_chi2dof[3]->Fill(chi2dof);
       h_track_npxhits[3]->Fill(npxhits);
       h_track_nsthits[3]->Fill(nsthits);
       h_track_npxlayers[3]->Fill(npxlayers);
       h_track_nstlayers[3]->Fill(nstlayers);
     }
   }

   /*
   LogInfo("Stuff0") << "# of PVs " << primary_vertices->size();
   LogInfo("Stuff3") << "# of tracks in main PV " << main_pv_tracks.size();
   LogInfo("Stuff5") << "# of tracks not in a PV at all " << non_pv_tracks.size();
   LogInfo("Stuff4") << "# of tracks in other PVs " << other_pvs_tracks.size();
   LogInfo("Stuff1") << "total # tracks in a PV " << all_tracks.size();
   LogInfo("Stuff2") << "total # tracks in event " << tracks->size();
   */

   const int npv = int(primary_vertices->size());
   h_npv->Fill(npv);   
}

DEFINE_FWK_MODULE(PVAnalyzer);
