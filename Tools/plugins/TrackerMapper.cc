#include "TH2F.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "JMTucker/Tools/interface/TrackerSpaceExtent.h"

class TrackerMapper : public edm::EDAnalyzer {
 public:
  explicit TrackerMapper(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);
 
 private:
  const edm::EDGetTokenT<reco::TrackCollection> track_token;
  const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
  const edm::EDGetTokenT<reco::VertexCollection> primary_vertex_token;
  const edm::EDGetTokenT<std::vector<PileupSummaryInfo> > pileup_token;

  const std::vector<double> pileup_weights;
  double pileup_weight(int mc_npu) const;

  TH1F* h_bsx;
  TH1F* h_bsy;
  TH1F* h_bsz;

  TH1F* h_npv;

  TH1F* h_ntracks[3];
  TH1F* h_tracks_pt[3];
  TH1F* h_tracks_eta[3];
  TH1F* h_tracks_phi[3];
  TH1F* h_tracks_vx[3];
  TH1F* h_tracks_vy[3];
  TH1F* h_tracks_vz[3];
  TH1F* h_tracks_vphi[3];
  TH1F* h_tracks_dxy[3];
  TH1F* h_tracks_dxy_zslices[3][6];
  TH1F* h_tracks_dxyerr[3];
  TH1F* h_tracks_dzerr[3];
  TH1F* h_tracks_nhits[3];
  TH1F* h_tracks_npxhits[3];
  TH1F* h_tracks_nsthits[3];

  TH1F* h_tracks_min_r[3];
  TH1F* h_tracks_npxlayers[3];
  TH1F* h_tracks_nstlayers[3];
  TH1F* h_tracks_sigmadxy[3];
  TH1F* h_tracks_absdxy[3];
  TH1F* h_tracks_sigmadxy_dxyslices[3][6];
  TH1F* h_ntracks_dxyslices[3][6];

  TH2F* h_dxyerr_v_ptcut[2];
  TH2F* h_dxyerr_v_npxlayerscut[2];
  TH2F* h_dxyerr_v_nstlayerscut[2];
};

TrackerMapper::TrackerMapper(const edm::ParameterSet& cfg)
  : track_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("track_src"))),
    beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot_src"))),
    primary_vertex_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("primary_vertex_src"))),
    pileup_token(consumes<std::vector<PileupSummaryInfo> >(edm::InputTag("addPileupInfo"))),
    pileup_weights(cfg.getParameter<std::vector<double> >("pileup_weights"))
{
  edm::Service<TFileService> fs;

  h_bsx = fs->make<TH1F>("h_bsx", ";beamspot x (cm);events", 200, -1, 1);
  h_bsy = fs->make<TH1F>("h_bsy", ";beamspot y (cm);events", 200, -1, 1);
  h_bsz = fs->make<TH1F>("h_bsz", ";beamspot z (cm);events", 200, -1, 1);

  h_npv = fs->make<TH1F>("h_npv", ";number of primary vertices;events", 65, 0, 65);

  const char* ex[3] = {"all", "sel", "seed"};
  for (int i = 0; i < 3; ++i) {
    h_ntracks[i] = fs->make<TH1F>(TString::Format("h_%s_ntracks", ex[i]), TString::Format(";number of %s tracks;events", ex[i]), 2000, 0, 2000);
    h_tracks_pt[i] = fs->make<TH1F>(TString::Format("h_%s_tracks_pt", ex[i]), TString::Format("%s tracks;tracks pt;arb. units", ex[i]), 200, 0, 20);
    h_tracks_phi[i] = fs->make<TH1F>(TString::Format("h_%s_tracks_phi", ex[i]), TString::Format("%s tracks;tracks phi;arb. units", ex[i]), 50, -3.15, 3.15);
    h_tracks_eta[i] = fs->make<TH1F>(TString::Format("h_%s_tracks_eta", ex[i]), TString::Format("%s tracks;tracks eta;arb. units", ex[i]), 50, -4, 4);
    h_tracks_vx[i] = fs->make<TH1F>(TString::Format("h_%s_tracks_vx", ex[i]), TString::Format("%s tracks;tracks vx - beamspot x;arb. units", ex[i]), 400, -0.2, 0.2);
    h_tracks_vy[i] = fs->make<TH1F>(TString::Format("h_%s_tracks_vy", ex[i]), TString::Format("%s tracks;tracks vy - beamspot y;arb. units", ex[i]), 400, -0.2, 0.2);
    h_tracks_vz[i] = fs->make<TH1F>(TString::Format("h_%s_tracks_vz", ex[i]), TString::Format("%s tracks;tracks vz - beamspot z;arb. units", ex[i]), 400, -20, 20);
    h_tracks_vphi[i] = fs->make<TH1F>(TString::Format("h_%s_tracks_vphi", ex[i]), TString::Format("%s tracks;tracks vphi w.r.t. beamspot;arb. units", ex[i]), 50, -3.15, 3.15);
    h_tracks_dxy[i] = fs->make<TH1F>(TString::Format("h_%s_tracks_dxy", ex[i]), TString::Format("%s tracks;tracks dxy to beamspot;arb. units", ex[i]), 400, -0.2, 0.2);
    for (int j = 0; j < 6; ++j) {
      h_tracks_dxy_zslices[i][j] = fs->make<TH1F>(TString::Format("h_%s_tracks_dxy_z%d", ex[i], j), TString::Format("%s tracks z%d;tracks dxy to beamspot;arb. units", ex[i], j), 400, -0.2, 0.2);
    }
    h_tracks_dxyerr[i] = fs->make<TH1F>(TString::Format("h_%s_tracks_dxyerr", ex[i]), TString::Format("%s tracks;tracks dxyerr;arb. units", ex[i]), 200, 0, 0.2);
    h_tracks_dzerr[i] = fs->make<TH1F>(TString::Format("h_%s_tracks_dzerr", ex[i]), TString::Format("%s tracks;tracks dzerr;arb. units", ex[i]), 200, 0, 2);
    h_tracks_nhits[i] = fs->make<TH1F>(TString::Format("h_%s_tracks_nhits", ex[i]), TString::Format("%s tracks;tracks nhits;arb. units", ex[i]), 40, 0, 40);
    h_tracks_npxhits[i] = fs->make<TH1F>(TString::Format("h_%s_tracks_npxhits", ex[i]), TString::Format("%s tracks;tracks npxhits;arb. units", ex[i]), 40, 0, 40);
    h_tracks_nsthits[i] = fs->make<TH1F>(TString::Format("h_%s_tracks_nsthits", ex[i]), TString::Format("%s tracks;tracks nsthits;arb. units", ex[i]), 40, 0, 40);

    h_tracks_min_r[i] = fs->make<TH1F>(TString::Format("h_%s_tracks_min_r", ex[i]), TString::Format("%s tracks;tracks min_r;arb. units", ex[i]), 20, 0, 20);
    h_tracks_npxlayers[i] = fs->make<TH1F>(TString::Format("h_%s_tracks_npxlayers", ex[i]), TString::Format("%s tracks;tracks npxlayers;arb. units", ex[i]), 20, 0, 20);
    h_tracks_nstlayers[i] = fs->make<TH1F>(TString::Format("h_%s_tracks_nstlayers", ex[i]), TString::Format("%s tracks;tracks nstlayers;arb. units", ex[i]), 20, 0, 20);
    h_tracks_sigmadxy[i] = fs->make<TH1F>(TString::Format("h_%s_tracks_sigmadxy", ex[i]), TString::Format("%s tracks;tracks sigmadxy;arb. units", ex[i]), 200, 0, 20);
    h_tracks_absdxy[i] = fs->make<TH1F>(TString::Format("h_%s_tracks_absdxy", ex[i]), TString::Format("%s tracks;tracks |dxy| to beamspot;arb. units", ex[i]), 200, 0, 0.2);
    for (int j = 0; j < 6; ++j) {
      h_tracks_sigmadxy_dxyslices[i][j] = fs->make<TH1F>(TString::Format("h_%s_tracks_sigmadxy_dxy%d", ex[i], j), TString::Format("%s tracks with %.2f <= |dxy| < %.2f;tracks sigmadxy;arb. units", ex[i], 0.01*j, 0.01*(j+1)), 200, 0, 20);
      h_ntracks_dxyslices[i][j] = fs->make<TH1F>(TString::Format("h_%s_ntracks_dxy%d", ex[i], j), TString::Format(";number of %s tracks with %.2f <= |dxy| < %.2f;events", ex[i], 0.01*j, 0.01*(j+1)), 500, 0, 500);
    }
  }

  const char* ex2[2] = {"all", "nm1"};
  for (int i = 0; i < 2; ++i) {
    h_dxyerr_v_ptcut[i] = fs->make<TH2F>(TString::Format("h_%s_dxyerr_v_ptcut", ex2[i]), "", 40, 0, 20, 100, 0, 0.2);
    h_dxyerr_v_npxlayerscut[i] = fs->make<TH2F>(TString::Format("h_%s_dxyerr_v_npxlayerscut", ex2[i]), "", 5, 0, 5, 100, 0, 0.2);
    h_dxyerr_v_nstlayerscut[i] = fs->make<TH2F>(TString::Format("h_%s_dxyerr_v_nstlayerscut", ex2[i]), "", 15, 0, 15, 100, 0, 0.2);
  }
}

double TrackerMapper::pileup_weight(int mc_npu) const {
  if (mc_npu < 0 || mc_npu >= int(pileup_weights.size()))
    return 0;
  else
    return pileup_weights[mc_npu];
}

void TrackerMapper::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  std::auto_ptr<double> weight(new double);
  *weight = 1;

  int npu = -1;
  if (!event.isRealData()) {
    edm::Handle<std::vector<PileupSummaryInfo> > pileup;
    event.getByToken(pileup_token, pileup);

    for (std::vector<PileupSummaryInfo>::const_iterator psi = pileup->begin(), end = pileup->end(); psi != end; ++psi)
      if (psi->getBunchCrossing() == 0)
        npu = psi->getTrueNumInteractions();

    const double pu_w = pileup_weight(npu);
    *weight *= pu_w;
  }

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByToken(beamspot_token, beamspot);

  const float bsx = beamspot->x0();
  const float bsy = beamspot->y0();
  const float bsz = beamspot->z0();

  h_bsx->Fill(bsx);
  h_bsy->Fill(bsy);
  h_bsz->Fill(bsz);

  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByToken(primary_vertex_token, primary_vertices);
  h_npv->Fill(int(primary_vertices->size()), *weight);

  edm::Handle<reco::TrackCollection> tracks;
  event.getByToken(track_token, tracks);

  int ntracks[3] = {0};
  int ntracks_dxyslices[3][6] = {{0}, {0}, {0}};
  for (const reco::Track& tk : *tracks) {
    TrackerSpaceExtents tracker_extents;
    const double pt = tk.pt();
    const double min_r = tracker_extents.numExtentInRAndZ(tk.hitPattern(), false).min_r;
    const double npxlayers = tk.hitPattern().pixelLayersWithMeasurement();
    const double nstlayers = tk.hitPattern().stripLayersWithMeasurement();
    const double sigmadxybs = fabs(tk.dxy(*beamspot) / tk.dxyError());

    const bool sel = pt > 1 && min_r <= 1 && npxlayers >= 2 && nstlayers >= 3;
    const bool seed = sel && sigmadxybs > 4;

    const bool nm1_sel[3] = {
      min_r <= 1 && npxlayers >= 2 && nstlayers >= 3,
      min_r <= 1 && pt > 1 && nstlayers >= 3,
      min_r <= 1 && pt > 1 && npxlayers >= 2
    };
    const double nm1_v[3] = { pt, npxlayers, nstlayers };

    for (int i = 0; i < 2; ++i) {
      TH2F* nm1_h[3] = { h_dxyerr_v_ptcut[i], h_dxyerr_v_npxlayerscut[i], h_dxyerr_v_nstlayerscut[i] };
      for (int j = 0; j < 3; ++j) {
        if (i == 0 || (i == 1 && nm1_sel[j])) {
          for (int ibin = 1; ibin <= nm1_h[j]->GetNbinsX(); ++ibin) {
            const double cut = nm1_h[j]->GetXaxis()->GetBinLowEdge(ibin);
            if (nm1_v[j] >= cut) nm1_h[j]->Fill(cut, tk.dxyError(), *weight);
          }
        }
      }
    }

    for (int i = 0; i < 3; ++i) {
      if (i==1 && !sel) continue;
      if (i==2 && !seed) continue;

      ++ntracks[i];

      h_tracks_pt[i]->Fill(tk.pt(), *weight);
      h_tracks_eta[i]->Fill(tk.eta(), *weight);
      h_tracks_phi[i]->Fill(tk.phi(), *weight);
      h_tracks_vx[i]->Fill(tk.vx() - bsx, *weight);
      h_tracks_vy[i]->Fill(tk.vy() - bsy, *weight);
      h_tracks_vz[i]->Fill(tk.vz() - bsz, *weight);
      h_tracks_vphi[i]->Fill(atan2(tk.vy() - bsy, tk.vx() - bsx), *weight);
      h_tracks_dxy[i]->Fill(tk.dxy(*beamspot), *weight);
      h_tracks_dxyerr[i]->Fill(tk.dxyError(), *weight);
      h_tracks_dzerr[i]->Fill(tk.dzError(), *weight);
      h_tracks_nhits[i]->Fill(tk.hitPattern().numberOfValidHits(), *weight);
      h_tracks_npxhits[i]->Fill(tk.hitPattern().numberOfValidPixelHits(), *weight);
      h_tracks_nsthits[i]->Fill(tk.hitPattern().numberOfValidStripHits(), *weight);

      double z = tk.vz() - bsz;
      double dxy = tk.dxy(*beamspot);
      if (z<-5)         h_tracks_dxy_zslices[i][0]->Fill(dxy, *weight);
      if (z>-5 && z<-2) h_tracks_dxy_zslices[i][1]->Fill(dxy, *weight);
      if (z>-2 && z<0)  h_tracks_dxy_zslices[i][2]->Fill(dxy, *weight);
      if (z>0 && z<2)   h_tracks_dxy_zslices[i][3]->Fill(dxy, *weight);
      if (z>2 && z<5)   h_tracks_dxy_zslices[i][4]->Fill(dxy, *weight);
      if (z>5)          h_tracks_dxy_zslices[i][5]->Fill(dxy, *weight);

      h_tracks_min_r[i]->Fill(min_r, *weight);
      h_tracks_npxlayers[i]->Fill(npxlayers, *weight);
      h_tracks_nstlayers[i]->Fill(nstlayers, *weight);
      h_tracks_sigmadxy[i]->Fill(sigmadxybs, *weight);

      double absdxy = fabs(dxy);
      h_tracks_absdxy[i]->Fill(absdxy, *weight);
      for (int j = 0; j < 6; ++j) {
        if (absdxy >= 0.01*j && absdxy < 0.01*(j+1)) {
          ++ntracks_dxyslices[i][j];
          h_tracks_sigmadxy_dxyslices[i][j]->Fill(sigmadxybs, *weight);
        }
      }
    }
  }

  for (int i = 0; i < 3; ++i) {
    h_ntracks[i]->Fill(ntracks[i], *weight);

    for (int j = 0; j < 6; ++j) {
      h_ntracks_dxyslices[i][j]->Fill(ntracks_dxyslices[i][j], *weight);
    }
  }
}

DEFINE_FWK_MODULE(TrackerMapper);
