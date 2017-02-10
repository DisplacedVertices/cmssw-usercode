#include "TH2.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/Tools/interface/TrackerSpaceExtent.h"

class MFVPackedPFCandidates : public edm::EDAnalyzer {
public:
  explicit MFVPackedPFCandidates(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);
private:
  const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
  const edm::EDGetTokenT<reco::VertexCollection> primary_vertices_token;
  const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
  const edm::EDGetTokenT<pat::PackedCandidateCollection> packed_candidate_token;

  TrackerSpaceExtents tracker_extents;

  TH2F* h_nmatch_v_nseed;
  TH1F* h_matchdist;
  TH1F* h_fracdelta_par[5];
  TH1F* h_fracdelta_cov[5][5]; // only the upper 5*4/2 = 10 are filled
  TH1F* h_fracdelta_sigmadxybs;
  TH1F* h_delta_pxl;
  TH1F* h_delta_stl;
  TH1F* h_delta_minr;
  TH1F* h_nomatch_par[5];
  TH1F* h_nomatch_sigmadxybs;
  TH1F* h_nomatch_pxl;
  TH1F* h_nomatch_stl;
  TH1F* h_nomatch_minr;
};

MFVPackedPFCandidates::MFVPackedPFCandidates(const edm::ParameterSet& cfg)
  : beamspot_token(consumes<reco::BeamSpot>(edm::InputTag("offlineBeamSpot"))),
    tracks_token(consumes<reco::TrackCollection>(edm::InputTag("generalTracks"))),
    packed_candidate_token(consumes<pat::PackedCandidateCollection>(edm::InputTag("packedPFCandidates")))
{
  edm::Service<TFileService> fs;
  h_nmatch_v_nseed = fs->make<TH2F>("h_nmatch_v_nseed", "", 200, 0, 200, 200, 0, 200);
  h_matchdist = fs->make<TH1F>("h_matchdist", "", 1000, 0, 0.01);
  h_nomatch_par[0] = fs->make<TH1F>("h_nomatch_par_0", "", 100, 0, 1000);
  h_nomatch_par[1] = fs->make<TH1F>("h_nomatch_par_1", "", 100, -3, 3);
  h_nomatch_par[2] = fs->make<TH1F>("h_nomatch_par_2", "", 100, -3.15, 3.15);
  h_nomatch_par[3] = fs->make<TH1F>("h_nomatch_par_3", "", 10000, -1, 1);
  h_nomatch_par[4] = fs->make<TH1F>("h_nomatch_par_4", "", 10000, -1, 1);
  h_nomatch_sigmadxybs = fs->make<TH1F>("h_nomatch_sigmadxybs", "", 10000, -1, 1);
  h_nomatch_pxl = fs->make<TH1F>("h_nomatch_pxl", "", 10, 0, 10);
  h_nomatch_stl = fs->make<TH1F>("h_nomatch_stl", "", 20, 0, 20);
  h_nomatch_minr = fs->make<TH1F>("h_nomatch_minr", "", 10, 0, 10);
  for (int i = 0; i < 5; ++i) {
    h_fracdelta_par[i] = fs->make<TH1F>(TString::Format("h_fracdelta_par_%i", i), "", 10000, -1, 1);
    for (int j = i; j < 5; ++j)
      h_fracdelta_cov[i][j] = fs->make<TH1F>(TString::Format("h_fracdelta_cov_%i_%i", i, j), "", 10000, -1e-2, 1e-2);
  }
  h_fracdelta_sigmadxybs = fs->make<TH1F>("h_fracdelta_sigmadxybs", "", 10000, -1, 1);
  h_delta_pxl = fs->make<TH1F>("h_delta_pxl", "", 100, -50, 50);
  h_delta_stl = fs->make<TH1F>("h_delta_stl", "", 100, -50, 50);
  h_delta_minr = fs->make<TH1F>("h_delta_minr", "", 100, -50, 50);
}

void MFVPackedPFCandidates::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  const bool prints = true;

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByToken(beamspot_token, beamspot);
  const double bs_x = beamspot->position().x();
  const double bs_y = beamspot->position().y();
  const double bs_z = beamspot->position().z();
  
  if (!tracker_extents.filled())
    tracker_extents.fill(setup, GlobalPoint(bs_x, bs_y, bs_z));

  //edm::Handle<reco::VertexCollection> primary_vertices;
  //event.getByToken(primary_vertices_token, primary_vertices);
  //const reco::Vertex* primary_vertex = 0;
  //if (primary_vertices->size())
  //  primary_vertex = &primary_vertices->at(0);

  edm::Handle<reco::TrackCollection> tracks;
  event.getByToken(tracks_token, tracks);

  edm::Handle<pat::PackedCandidateCollection> packed_candidates;
  event.getByToken(packed_candidate_token, packed_candidates);

  int npass = 0;
  int nmatch = 0;

  if (prints) printf("generalTracks that pass our cuts (all # = %lu):\n", tracks->size());
  for (size_t itk = 0, itke = tracks->size(); itk < itke; ++itk) {
    const reco::Track& tk = (*tracks)[itk];
    const NumExtents ne = tracker_extents.numExtentInRAndZ(tk.hitPattern(), false);
    const double dxybs = tk.dxy(*beamspot);
    const double sigmadxybs = dxybs / tk.dxyError();
    const bool pass = tk.pt() > 1 && ne.min_r <= 1 && tk.hitPattern().pixelLayersWithMeasurement() >= 2 && tk.hitPattern().stripLayersWithMeasurement() >= 3 && fabs(sigmadxybs) > 4;

    if (pass) {
      ++npass;

      if (prints) {
        printf("tk #%4lu: pt %10.4g +- %10.4g eta %10.4g +- %10.4g phi %10.4g +- %10.4g dxy %10.4g +- %10.4g dz %10.4g +- %10.4g\n",
               itk, tk.pt(), tk.ptError(), tk.eta(), tk.etaError(), tk.phi(), tk.phiError(), tk.dxy(), tk.dxyError(), tk.dz(), tk.dzError());
        printf("  # px hits: %2i layers: %2i st hits: %2i layers: %2i   min_r: %i  dxybs: %10.4g  sigmadxybs: %10.4g\n",
               tk.hitPattern().numberOfValidPixelHits(), tk.hitPattern().pixelLayersWithMeasurement(),
               tk.hitPattern().numberOfValidStripHits(), tk.hitPattern().stripLayersWithMeasurement(),
               ne.min_r, dxybs, sigmadxybs);
      }

      const pat::PackedCandidate* closest_cd = 0;
      double closest_cd_dist = 100;
      for (size_t icd = 0, icde = packed_candidates->size(); icd < icde; ++icd) {
        const pat::PackedCandidate& cd = (*packed_candidates)[icd];
        if (cd.charge()) {
          const reco::Track& cd_tk = cd.pseudoTrack();
          const double dist = reco::deltaR(tk, cd_tk);
          if (dist < 0.111e-3 && dist < closest_cd_dist) {
            closest_cd = &cd;
            closest_cd_dist = dist;
          }
        }
      }

      h_matchdist->Fill(closest_cd_dist);

      if (closest_cd) {
        ++nmatch;
        const reco::Track& cd_tk = closest_cd->pseudoTrack();
        const NumExtents cd_ne = tracker_extents.numExtentInRAndZ(cd_tk.hitPattern(), false);
        const double cd_dxybs = cd_tk.dxy(*beamspot);
        const double cd_sigmadxybs = cd_dxybs / cd_tk.dxyError();
        const bool cd_passes = cd_tk.pt() > 1 && cd_ne.min_r <= 1 && cd_tk.hitPattern().pixelLayersWithMeasurement() >= 2 && cd_tk.hitPattern().stripLayersWithMeasurement() >= 3 && fabs(cd_sigmadxybs) > 4;

        h_fracdelta_par[0]->Fill(cd_tk.pt()  / tk.pt()  - 1);
        h_fracdelta_par[1]->Fill(cd_tk.eta() / tk.eta() - 1);
        h_fracdelta_par[2]->Fill(cd_tk.phi() / tk.phi() - 1);
        h_fracdelta_par[3]->Fill(cd_tk.dxy() / tk.dxy() - 1);
        h_fracdelta_par[4]->Fill(cd_tk.dz()  / tk.dz()  - 1);
        for (int i = 0; i < 5; ++i)
          for (int j = i; j < 5; ++j)
            if (fabs(tk.covariance(i,j)) > 0)
              h_fracdelta_cov[i][j]->Fill(cd_tk.covariance(i,j) / tk.covariance(i,j) - 1);
        h_fracdelta_sigmadxybs->Fill(cd_sigmadxybs / sigmadxybs - 1);
        h_delta_pxl->Fill(cd_tk.hitPattern().pixelLayersWithMeasurement() - tk.hitPattern().pixelLayersWithMeasurement());
        h_delta_stl->Fill(cd_tk.hitPattern().stripLayersWithMeasurement() - tk.hitPattern().stripLayersWithMeasurement());
        h_delta_minr->Fill(cd_ne.min_r - ne.min_r);
        if (prints) {
          printf("  the closest CD with dist %f:\n", closest_cd_dist);
          printf("    pt %10.4g +- %10.4g eta %10.4g +- %10.4g phi %10.4g +- %10.4g dxy %10.4g +- %10.4g dz %10.4g +- %10.4g\n",
                 cd_tk.pt(), cd_tk.ptError(), cd_tk.eta(), cd_tk.etaError(), cd_tk.phi(), cd_tk.phiError(), cd_tk.dxy(), cd_tk.dxyError(), cd_tk.dz(), cd_tk.dzError());
          printf("    # px hits: %2i layers: %2i st hits: %2i layers: %2i   min_r: %i  dxybs: %10.4g  sigmadxybs: %10.4g\n",
                 cd_tk.hitPattern().numberOfValidPixelHits(), cd_tk.hitPattern().pixelLayersWithMeasurement(),
                 cd_tk.hitPattern().numberOfValidStripHits(), cd_tk.hitPattern().stripLayersWithMeasurement(),
                 cd_ne.min_r, cd_dxybs, cd_sigmadxybs);
          printf("  also passes? %i\n", cd_passes);
        }
      }
      else {
        if (prints) printf("  NO CD MATCH\n");
        h_nomatch_par[0]->Fill(tk.pt() );
        h_nomatch_par[1]->Fill(tk.eta());
        h_nomatch_par[2]->Fill(tk.phi());
        h_nomatch_par[3]->Fill(tk.dxy());
        h_nomatch_par[4]->Fill(tk.dz() );
        h_nomatch_sigmadxybs->Fill(sigmadxybs);
        h_nomatch_pxl->Fill(tk.hitPattern().pixelLayersWithMeasurement());
        h_nomatch_stl->Fill(tk.hitPattern().stripLayersWithMeasurement());
        h_nomatch_minr->Fill(ne.min_r);
      }
    }
  }

  h_nmatch_v_nseed->Fill(npass, nmatch);
  if (prints) printf("# general passing: %i  # with match: %i\n", npass, nmatch);
}

DEFINE_FWK_MODULE(MFVPackedPFCandidates);
