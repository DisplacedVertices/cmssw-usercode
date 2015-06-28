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
  h_all_pv_track_pt  = fs->make<TH1F>("h_all_pv_track_pt", ";p_{T} of all tracks in all primary vertices (GeV); arb. units", 150, 0, 150);
  h_all_pv_track_eta = fs->make<TH1F>("h_all_pv_track_eta", ";eta; arb. units", 50, -4, 4);
  h_all_pv_track_phi = fs->make<TH1F>("h_all_pv_track_phi", ";phi; arb. units", 50, -3.15, 3.15);
  h_all_pv_track_dxy = fs->make<TH1F>("h_all_pv_track_dxy", ";dxy (cm); arb. units", 50, -2, 2);
  h_all_pv_track_dz  = fs->make<TH1F>("h_all_pv_track_dz", ";dz (cm); arb. units", 100, -20, 20);
  h_all_pv_track_pterr  = fs->make<TH1F>("h_all_pv_track_pterr", ";error in p_{T} of all tracks in all primary vertices (GeV); arb. units", 50, 0, 0.25);
  h_all_pv_track_etaerr = fs->make<TH1F>("h_all_pv_track_etaerr", ";eta error; arb. units", 50, 0, 0.1);
  h_all_pv_track_phierr = fs->make<TH1F>("h_all_pv_track_phierr", ";phi error; arb. units", 50, 0, 0.1);
  h_all_pv_track_dxyerr = fs->make<TH1F>("h_all_pv_track_dxyerr", ";dxy error; arb. units", 50, 0, 0.5);
  h_all_pv_track_dzerr  = fs->make<TH1F>("h_all_pv_track_dzerr", ";dz error; arb. units", 50, 0, 1);
  h_all_pv_track_ptoversigma  = fs->make<TH1F>("h_all_pv_track_ptoversigma", ";pt/ptError; arb. units", 200, 0, 200);
  h_all_pv_track_etaoversigma = fs->make<TH1F>("h_all_pv_track_etaoversigma", ";eta/etaError; arb. units", 300, -150, 150);
  h_all_pv_track_phioversigma = fs->make<TH1F>("h_all_pv_track_phioversigma", ";phi/phiError; arb. units", 300, -150, 150);
  h_all_pv_track_dxyoversigma = fs->make<TH1F>("h_all_pv_track_dxyoversigma", ";dxy/dxyError; arb. units", 100, -15, 15);
  h_all_pv_track_dzoversigma  = fs->make<TH1F>("h_all_pv_track_dzoversigma", ";dz/dzError; arb. units", 200, -120, 120);
  h_all_pv_track_chi2dof = fs->make<TH1F>("h_all_pv_track_chi2dof", ";#chi^2/dof; arb. units", 50, 0, 7);
  h_all_pv_track_npxhits = fs->make<TH1F>("h_all_pv_track_npxhits", ";# of pixel hits for all PV tracks; arb. units", 15, 0, 15);
  h_all_pv_track_nsthits = fs->make<TH1F>("h_all_pv_track_nsthits", ";# of strip hits for all PV tracks; arb. units", 45, 0, 45);
  h_all_pv_track_npxlayers = fs->make<TH1F>("h_all_pv_track_npxlayers", ";# pixel layer hits; arb. units", 6, 0, 6);
  h_all_pv_track_nstlayers = fs->make<TH1F>("h_all_pv_track_nstlayers", ";# strip layer hits; arb. untis", 20, 0, 20);
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

   std::map<reco::TrackRef, std::vector<std::pair<int, float> > > tracks_in_pvs;
   for (size_t i = 0, ie = primary_vertices->size(); i < ie; ++i) {
     const reco::Vertex& pv = primary_vertices->at(i);
     for (auto it = pv.tracks_begin(), ite = pv.tracks_end(); it != ite; ++it) {
       float w = pv.trackWeight(*it);
       reco::TrackRef tk = it->castTo<reco::TrackRef>();
       tracks_in_pvs[tk].push_back(std::make_pair(i, w));
     }
   }

   for (size_t i = 0, ie = tracks->size(); i < ie; ++i) {
      reco::TrackRef tkref(tracks, i);
      bool ok = false;
      for (const auto& pv_use : tracks_in_pvs[tkref])
        if (use_only_pvs_tracks || (use_only_pv_tracks && pv_use.first == 0)) {
          ok = true;
          break;
        }
      
      if (ok)
        all_tracks.push_back(tkref);
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
   LogInfo("Stuff0") << "# of PVs " << primary_vertices->size();
   LogInfo("Stuff1") << "total # tracks in a PV " << all_tracks.size();
   LogInfo("Stuff2") << "total # tracks in event " << tracks->size();

   const int npv = int(primary_vertices->size());
   h_npv->Fill(npv);   
}

DEFINE_FWK_MODULE(PVAnalyzer);
