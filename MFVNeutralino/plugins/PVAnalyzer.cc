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


class PVAnalyzer : public edm::EDAnalyzer {
   public:
      explicit PVAnalyzer(const edm::ParameterSet&);
      ~PVAnalyzer();

   private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  TH1F* h_npv;

  TH1F* h_all_pv_track_pt;
  TH1F* h_all_pv_track_eta;
  TH1F* h_all_pv_track_phi;
  TH1F* h_all_pv_track_dxy;
  TH1F* h_all_pv_track_dz;

  TH1F* h_all_pv_track_pterr;
  TH1F* h_all_pv_track_etaerr;
  TH1F* h_all_pv_track_phierr;
  TH1F* h_all_pv_track_dxyerr;
  TH1F* h_all_pv_track_dzerr;
  
  TH1F* h_all_pv_track_ptoversigma;
  TH1F* h_all_pv_track_etaoversigma;
  TH1F* h_all_pv_track_phioversigma;
  TH1F* h_all_pv_track_dxyoversigma;
  TH1F* h_all_pv_track_dzoversigma;

  TH1F* h_all_pv_track_chi2dof;
  TH1F* h_all_pv_track_npxhits;
  TH1F* h_all_pv_track_nsthits;
  TH1F* h_all_pv_track_npxlayers;
  TH1F* h_all_pv_track_nstlayers;

  TH1F* h_pv0_track_pt;
  TH1F* h_pv0_track_eta;
  TH1F* h_pv0_track_phi;
  TH1F* h_pv0_track_dxy;
  TH1F* h_pv0_track_dz;

  TH1F* h_pv0_track_pterr;
  TH1F* h_pv0_track_etaerr;
  TH1F* h_pv0_track_phierr;
  TH1F* h_pv0_track_dxyerr;
  TH1F* h_pv0_track_dzerr;

  TH1F* h_pv0_track_ptoversigma;
  TH1F* h_pv0_track_etaoversigma;
  TH1F* h_pv0_track_phioversigma;
  TH1F* h_pv0_track_dxyoversigma;
  TH1F* h_pv0_track_dzoversigma;

  TH1F* h_pv0_track_chi2dof;
  TH1F* h_pv0_track_npxhits;
  TH1F* h_pv0_track_nsthits;
  TH1F* h_pv0_track_npxlayers;
  TH1F* h_pv0_track_nstlayers;

  TH1F* h_other_pvs_track_pt;
  TH1F* h_other_pvs_track_eta;
  TH1F* h_other_pvs_track_phi;
  TH1F* h_other_pvs_track_dxy;
  TH1F* h_other_pvs_track_dz;

  TH1F* h_other_pvs_track_pterr;
  TH1F* h_other_pvs_track_etaerr;
  TH1F* h_other_pvs_track_phierr;
  TH1F* h_other_pvs_track_dxyerr;
  TH1F* h_other_pvs_track_dzerr;

  TH1F* h_other_pvs_track_ptoversigma;
  TH1F* h_other_pvs_track_etaoversigma;
  TH1F* h_other_pvs_track_phioversigma;
  TH1F* h_other_pvs_track_dxyoversigma;
  TH1F* h_other_pvs_track_dzoversigma;

  TH1F* h_other_pvs_track_chi2dof;
  TH1F* h_other_pvs_track_npxhits;
  TH1F* h_other_pvs_track_nsthits;
  TH1F* h_other_pvs_track_npxlayers;
  TH1F* h_other_pvs_track_nstlayers;

  const edm::InputTag primary_vertices_src;
  const edm::InputTag track_src;
  const edm::InputTag beamspot_src;

  const bool use_only_pv_tracks;
  const bool use_only_pvs_tracks;
};

PVAnalyzer::PVAnalyzer(const edm::ParameterSet& iConfig)
  : primary_vertices_src(iConfig.getParameter<edm::InputTag>("primary_vertices_src")),
    track_src(iConfig.getParameter<edm::InputTag>("track_src")),
    beamspot_src(iConfig.getParameter<edm::InputTag>("beamspot_src")),
    use_only_pv_tracks(iConfig.getParameter<bool>("use_only_pv_tracks")),
    use_only_pvs_tracks(iConfig.getParameter<bool>("use_only_pvs_tracks"))
{
  edm::Service<TFileService> fs;

  h_npv = fs->make<TH1F>("h_npv", ";# of primary vertices; arb. units", 50, 0, 50);
  h_all_pv_track_pt  = fs->make<TH1F>("h_all_pv_track_pt", ";p_{T} of all tracks in all primary vertices (GeV); arb. units", 300, 0, 150);
  h_all_pv_track_eta = fs->make<TH1F>("h_all_pv_track_eta", ";eta of all PV tracks; arb. units", 50, -4, 4);
  h_all_pv_track_phi = fs->make<TH1F>("h_all_pv_track_phi", ";phi of all PV tracks; arb. units", 50, -3.15, 3.15);
  h_all_pv_track_dxy = fs->make<TH1F>("h_all_pv_track_dxy", ";dxy of all PV tracks (cm); arb. units", 1000, -2, 2);
  h_all_pv_track_dz  = fs->make<TH1F>("h_all_pv_track_dz", ";dz of all PV tracks (cm); arb. units", 200, -25, 25);

  h_all_pv_track_pterr  = fs->make<TH1F>("h_all_pv_track_pterr", ";error in p_{T} of all tracks in all primary vertices (GeV); arb. units", 50, 0, 0.25);
  h_all_pv_track_etaerr = fs->make<TH1F>("h_all_pv_track_etaerr", ";eta error; arb. units", 50, 0, 0.1);
  h_all_pv_track_phierr = fs->make<TH1F>("h_all_pv_track_phierr", ";phi error; arb. units", 50, 0, 0.1);
  h_all_pv_track_dxyerr = fs->make<TH1F>("h_all_pv_track_dxyerr", ";dxy error; arb. units", 300, 0, 0.5);
  h_all_pv_track_dzerr  = fs->make<TH1F>("h_all_pv_track_dzerr", ";dz error; arb. units", 300, 0, 1);

  h_all_pv_track_ptoversigma  = fs->make<TH1F>("h_all_pv_track_ptoversigma", ";pt/ptError; arb. units", 400, 0, 250);
  h_all_pv_track_etaoversigma = fs->make<TH1F>("h_all_pv_track_etaoversigma", ";eta/etaError; arb. units", 400, -200, 200);
  h_all_pv_track_phioversigma = fs->make<TH1F>("h_all_pv_track_phioversigma", ";phi/phiError; arb. units", 400, -200, 200);
  h_all_pv_track_dxyoversigma = fs->make<TH1F>("h_all_pv_track_dxyoversigma", ";dxy/dxyError; arb. units", 300, -15, 15);
  h_all_pv_track_dzoversigma  = fs->make<TH1F>("h_all_pv_track_dzoversigma", ";dz/dzError; arb. units", 400, -200, 200);

  h_all_pv_track_chi2dof = fs->make<TH1F>("h_all_pv_track_chi2dof", ";#chi^2/dof; arb. units", 50, 0, 7);
  h_all_pv_track_npxhits = fs->make<TH1F>("h_all_pv_track_npxhits", ";# of pixel hits for all PV tracks; arb. units", 15, 0, 15);
  h_all_pv_track_nsthits = fs->make<TH1F>("h_all_pv_track_nsthits", ";# of strip hits for all PV tracks; arb. units", 45, 0, 45);
  h_all_pv_track_npxlayers = fs->make<TH1F>("h_all_pv_track_npxlayers", ";# pixel layer hits; arb. units", 6, 0, 6);
  h_all_pv_track_nstlayers = fs->make<TH1F>("h_all_pv_track_nstlayers", ";# strip layer hits; arb. units", 20, 0, 20);

  h_pv0_track_pt  = fs->make<TH1F>("h_pv0_track_pt", ";p_{T} of tracks in main PV (GeV); arb. units", 300, 0, 150);
  h_pv0_track_eta = fs->make<TH1F>("h_pv0_track_eta", ";eta of tracks in main PV; arb. units", 50, -4, 4);
  h_pv0_track_phi = fs->make<TH1F>("h_pv0_track_phi", ";phi of tracks in main PV; arb. units", 50, -3.15, 3.15);
  h_pv0_track_dxy = fs->make<TH1F>("h_pv0_track_dxy", ";dxy of tracks in main PV (cm); arb. units", 1000, -2, 2);
  h_pv0_track_dz  = fs->make<TH1F>("h_pv0_track_dz", ";dz of tracks in main PV (cm); arb. units", 200, -25, 25);

  h_pv0_track_pterr  = fs->make<TH1F>("h_pv0_track_pterr", ";error in p_{T} of tracks in main PV (GeV); arb. units", 50, 0, 0.25);
  h_pv0_track_etaerr = fs->make<TH1F>("h_pv0_track_etaerr", ";eta error of tracks in main PV; arb. units", 50, 0, 0.1);
  h_pv0_track_phierr = fs->make<TH1F>("h_pv0_track_phierr", ";phi error of tracks in main PV; arb. units", 50, 0, 0.1);
  h_pv0_track_dxyerr = fs->make<TH1F>("h_pv0_track_dxyerr", ";dxy error of tracks in main PV; arb. units", 300, 0, 0.5);
  h_pv0_track_dzerr  = fs->make<TH1F>("h_pv0_track_dzerr", ";dz error of tracks in main PV; arb. units", 300, 0, 1);

  h_pv0_track_ptoversigma  = fs->make<TH1F>("h_pv0_track_ptoversigma", ";pt/ptError of tracks in main PV; arb. units", 400, 0, 250);
  h_pv0_track_etaoversigma = fs->make<TH1F>("h_pv0_track_etaoversigma", ";eta/etaError of tracks in main PV; arb. units", 400, -200, 200);
  h_pv0_track_phioversigma = fs->make<TH1F>("h_pv0_track_phioversigma", ";phi/phiError of tracks in main PV; arb. units", 400, -200, 200);
  h_pv0_track_dxyoversigma = fs->make<TH1F>("h_pv0_track_dxyoversigma", ";dxy/dxyError of tracks in main PV; arb. units", 300, -15, 15);
  h_pv0_track_dzoversigma  = fs->make<TH1F>("h_pv0_track_dzoversigma", ";dz/dzError of tracks in main PV; arb. units", 400, -200, 200);

  h_pv0_track_chi2dof = fs->make<TH1F>("h_pv0_track_chi2dof", ";#chi^2/dof of tracks in main PV; arb. units", 50, 0, 7);
  h_pv0_track_npxhits = fs->make<TH1F>("h_pv0_track_npxhits", ";# of pixel hits for tracks in main PV; arb. units", 15, 0, 15);
  h_pv0_track_nsthits = fs->make<TH1F>("h_pv0_track_nsthits", ";# of strip hits for tracks in main PV; arb. units", 45, 0, 45);
  h_pv0_track_npxlayers = fs->make<TH1F>("h_pv0_track_npxlayers", ";# pixel layer hits of tracks in main PV; arb. units", 6, 0, 6);
  h_pv0_track_nstlayers = fs->make<TH1F>("h_pv0_track_nstlayers", ";# strip layer hits of tracks in main PV; arb. untis", 20, 0, 20);

  h_other_pvs_track_pt  = fs->make<TH1F>("h_other_pvs_track_pt", ";p_{T} of tracks in other primary vertices (GeV); arb. units", 300, 0, 150);
  h_other_pvs_track_eta = fs->make<TH1F>("h_other_pvs_track_eta", ";eta of tracks in other primary vertices; arb. units", 50, -4, 4);
  h_other_pvs_track_phi = fs->make<TH1F>("h_other_pvs_track_phi", ";phi of tracks in other primary vertices; arb. units", 50, -3.15, 3.15);
  h_other_pvs_track_dxy = fs->make<TH1F>("h_other_pvs_track_dxy", ";dxy of tracks in other primary vertices (cm); arb. units", 1000, -2, 2);
  h_other_pvs_track_dz  = fs->make<TH1F>("h_other_pvs_track_dz", ";dz of tracks in other primary vertices (cm); arb. units", 200, -25, 25);

  h_other_pvs_track_pterr  = fs->make<TH1F>("h_other_pvs_track_pterr", ";error in p_{T} of tracks in other primary vertices (GeV); arb. units", 50, 0, 0.25);
  h_other_pvs_track_etaerr = fs->make<TH1F>("h_other_pvs_track_etaerr", ";eta error; arb. units", 50, 0, 0.1);
  h_other_pvs_track_phierr = fs->make<TH1F>("h_other_pvs_track_phierr", ";phi error; arb. units", 50, 0, 0.1);
  h_other_pvs_track_dxyerr = fs->make<TH1F>("h_other_pvs_track_dxyerr", ";dxy error; arb. units", 300, 0, 0.5);
  h_other_pvs_track_dzerr  = fs->make<TH1F>("h_other_pvs_track_dzerr", ";dz error; arb. units", 300, 0, 1);

  h_other_pvs_track_ptoversigma  = fs->make<TH1F>("h_other_pvs_track_ptoversigma", ";pt/ptError; arb. units", 400, 0, 250);
  h_other_pvs_track_etaoversigma = fs->make<TH1F>("h_other_pvs_track_etaoversigma", ";eta/etaError; arb. units", 400, -200, 200);
  h_other_pvs_track_phioversigma = fs->make<TH1F>("h_other_pvs_track_phioversigma", ";phi/phiError; arb. units", 400, -200, 200);
  h_other_pvs_track_dxyoversigma = fs->make<TH1F>("h_other_pvs_track_dxyoversigma", ";dxy/dxyError; arb. units", 300, -15, 15);
  h_other_pvs_track_dzoversigma  = fs->make<TH1F>("h_other_pvs_track_dzoversigma", ";dz/dzError; arb. units", 400, -200, 200);

  h_other_pvs_track_chi2dof = fs->make<TH1F>("h_other_pvs_track_chi2dof", ";#chi^2/dof; arb. units", 50, 0, 7);
  h_other_pvs_track_npxhits = fs->make<TH1F>("h_other_pvs_track_npxhits", ";# of pixel hits of tracks in other PVs; arb. units", 15, 0, 15);
  h_other_pvs_track_nsthits = fs->make<TH1F>("h_other_pvs_track_nsthits", ";# of strip hits of tracks in other PVs; arb. units", 45, 0, 45);
  h_other_pvs_track_npxlayers = fs->make<TH1F>("h_other_pvs_track_npxlayers", ";# pixel layer hits of tracks in other PVs; arb. units", 6, 0, 6);
  h_other_pvs_track_nstlayers = fs->make<TH1F>("h_other_pvs_track_nstlayers", ";# strip layer hits of tracks in other PVs; arb. untis", 20, 0, 20);

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

   std::map<reco::TrackRef, std::vector<std::pair<int, float> > > tracks_in_pvs;
   std::map<reco::TrackRef, std::vector<std::pair<int, float> > > tracks_in_main_pv;
   std::map<reco::TrackRef, std::vector<std::pair<int, float> > > tracks_in_other_pvs;

   for (size_t i = 0, ie = primary_vertices->size(); i < ie; ++i) {
     const reco::Vertex& pv = primary_vertices->at(i);
     for (auto it = pv.tracks_begin(), ite = pv.tracks_end(); it != ite; ++it) {
       float w = pv.trackWeight(*it);
       reco::TrackRef tk = it->castTo<reco::TrackRef>();
       tracks_in_pvs[tk].push_back(std::make_pair(i, w));
     }

     if(i == 0) {
       for (auto it = pv.tracks_begin(), ite = pv.tracks_end(); it != ite; ++it) {
	 float w = pv.trackWeight(*it);
	 reco::TrackRef tk = it->castTo<reco::TrackRef>();
	 tracks_in_main_pv[tk].push_back(std::make_pair(i, w));
       }
     } else {
       for (auto it = pv.tracks_begin(), ite = pv.tracks_end(); it != ite; ++it) {
         float w = pv.trackWeight(*it);
	 reco::TrackRef tk = it->castTo<reco::TrackRef>();
         tracks_in_other_pvs[tk].push_back(std::make_pair(i, w));
       }
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
     const double dxy = tk->dxy(*beamspot);
     const double dz = tk->dz(beamspot->position());
     const double ptErr = tk->ptError();
     const double etaErr = tk->etaError();
     const double phiErr = tk->phiError();
     const double dxyErr = tk->dxyError();
     const double dzErr = tk->dzError();
     const double chi2dof = tk->chi2() / tk->ndof();
     const int npxhits = tk->hitPattern().numberOfValidPixelHits();
     const int nsthits = tk->hitPattern().numberOfValidStripHits();
     
     h_all_pv_track_pt->Fill(pt);
     h_all_pv_track_eta->Fill(eta);
     h_all_pv_track_phi->Fill(phi);
     h_all_pv_track_dxy->Fill(dxy);
     h_all_pv_track_dz->Fill(dz); 
     h_all_pv_track_pterr->Fill(ptErr);
     h_all_pv_track_etaerr->Fill(etaErr);
     h_all_pv_track_phierr->Fill(phiErr);
     h_all_pv_track_dxyerr->Fill(dxyErr);
     h_all_pv_track_dzerr->Fill(dzErr);
     h_all_pv_track_ptoversigma->Fill(pt/ptErr);
     h_all_pv_track_etaoversigma->Fill(eta/etaErr);
     h_all_pv_track_phioversigma->Fill(phi/phiErr);
     h_all_pv_track_dxyoversigma->Fill(dxy/dxyErr);
     h_all_pv_track_dzoversigma->Fill(dz/dzErr);

     h_all_pv_track_chi2dof->Fill(chi2dof);

     h_all_pv_track_npxhits->Fill(npxhits);
     h_all_pv_track_nsthits->Fill(nsthits);
     h_all_pv_track_npxlayers->Fill(tk->hitPattern().pixelLayersWithMeasurement());
     h_all_pv_track_nstlayers->Fill(tk->hitPattern().stripLayersWithMeasurement());
   }

   for (size_t i = 0, ie = main_pv_tracks.size(); i < ie; ++i) {
     const reco::TrackRef& tk = main_pv_tracks[i];
     const double pt = tk->pt();
     const double eta = tk->eta();
     const double phi = tk->phi();
     const double dxy = tk->dxy(*beamspot);
     const double dz = tk->dz(beamspot->position());
     const double ptErr = tk->ptError();
     const double etaErr = tk->etaError();
     const double phiErr = tk->phiError();
     const double dxyErr = tk->dxyError();
     const double dzErr = tk->dzError();
     const double chi2dof = tk->chi2() / tk->ndof();
     const int npxhits = tk->hitPattern().numberOfValidPixelHits();
     const int nsthits = tk->hitPattern().numberOfValidStripHits();

     h_pv0_track_pt->Fill(pt);
     h_pv0_track_eta->Fill(eta);
     h_pv0_track_phi->Fill(phi);
     h_pv0_track_dxy->Fill(dxy);
     h_pv0_track_dz->Fill(dz);
     h_pv0_track_pterr->Fill(ptErr);
     h_pv0_track_etaerr->Fill(etaErr);
     h_pv0_track_phierr->Fill(phiErr);
     h_pv0_track_dxyerr->Fill(dxyErr);
     h_pv0_track_dzerr->Fill(dzErr);
     h_pv0_track_ptoversigma->Fill(pt/ptErr);
     h_pv0_track_etaoversigma->Fill(eta/etaErr);
     h_pv0_track_phioversigma->Fill(phi/phiErr);
     h_pv0_track_dxyoversigma->Fill(dxy/dxyErr);
     h_pv0_track_dzoversigma->Fill(dz/dzErr);
  
     h_pv0_track_chi2dof->Fill(chi2dof);

     h_pv0_track_npxhits->Fill(npxhits);
     h_pv0_track_nsthits->Fill(nsthits);
     h_pv0_track_npxlayers->Fill(tk->hitPattern().pixelLayersWithMeasurement());
     h_pv0_track_nstlayers->Fill(tk->hitPattern().stripLayersWithMeasurement());
   }

   for (size_t i = 0, ie = other_pvs_tracks.size(); i < ie; ++i) {
     const reco::TrackRef& tk = other_pvs_tracks[i];
     const double pt = tk->pt();
     const double eta = tk->eta();
     const double phi = tk->phi();
     const double dxy = tk->dxy(*beamspot);
     const double dz = tk->dz(beamspot->position());
     const double ptErr = tk->ptError();
     const double etaErr = tk->etaError();
     const double phiErr = tk->phiError();
     const double dxyErr = tk->dxyError();
     const double dzErr = tk->dzError();
     const double chi2dof = tk->chi2() / tk->ndof();
     const int npxhits = tk->hitPattern().numberOfValidPixelHits();
     const int nsthits = tk->hitPattern().numberOfValidStripHits();

     h_other_pvs_track_pt->Fill(pt);
     h_other_pvs_track_eta->Fill(eta);
     h_other_pvs_track_phi->Fill(phi);
     h_other_pvs_track_dxy->Fill(dxy);
     h_other_pvs_track_dz->Fill(dz);
     h_other_pvs_track_pterr->Fill(ptErr);
     h_other_pvs_track_etaerr->Fill(etaErr);
     h_other_pvs_track_phierr->Fill(phiErr);
     h_other_pvs_track_dxyerr->Fill(dxyErr);
     h_other_pvs_track_dzerr->Fill(dzErr);
     h_other_pvs_track_ptoversigma->Fill(pt/ptErr);
     h_other_pvs_track_etaoversigma->Fill(eta/etaErr);
     h_other_pvs_track_phioversigma->Fill(phi/phiErr);
     h_other_pvs_track_dxyoversigma->Fill(dxy/dxyErr);
     h_other_pvs_track_dzoversigma->Fill(dz/dzErr);
  
     h_other_pvs_track_chi2dof->Fill(chi2dof);

     h_other_pvs_track_npxhits->Fill(npxhits);
     h_other_pvs_track_nsthits->Fill(nsthits);
     h_other_pvs_track_npxlayers->Fill(tk->hitPattern().pixelLayersWithMeasurement());
     h_other_pvs_track_nstlayers->Fill(tk->hitPattern().stripLayersWithMeasurement());
   }


   /*
   LogInfo("Stuff0") << "# of PVs " << primary_vertices->size();
   LogInfo("Stuff3") << "# of tracks in main PV " << main_pv_tracks.size();
   LogInfo("Stuff4") << "# of tracks in other PVs " << other_pvs_tracks.size();
   LogInfo("Stuff1") << "total # tracks in a PV " << all_tracks.size();
   LogInfo("Stuff2") << "total # tracks in event " << tracks->size();
   */

   const int npv = int(primary_vertices->size());
   h_npv->Fill(npv);   
}

DEFINE_FWK_MODULE(PVAnalyzer);
