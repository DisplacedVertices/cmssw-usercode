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
#include "RecoParticleFlow/PFTracking/interface/PFTrackAlgoTools.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"

class MFVPackedCandidates : public edm::EDAnalyzer {
public:
  explicit MFVPackedCandidates(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);
private:
  bool goodPtResolution(const reco::Track&) const;

  const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
  const edm::EDGetTokenT<reco::VertexCollection> primary_vertices_token;
  const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
  const edm::EDGetTokenT<pat::PackedCandidateCollection> packed_candidate_token;
  const double max_closest_cd_dist;
  const bool prints;

  TH2F* h_nmatch_v_nseed;
  TH2F* h_nmatchpass_v_nseed;
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
  TH1F* h_nomatch_highpurity;
  TH1F* h_nomatch_losthits;
  TH1F* h_nomatch_lostlayers;
  TH1F* h_nomatch_p;
  TH1F* h_nomatch_dptopt;
  TH1F* h_nomatch_goodptrel;

  struct track_ex {
    const reco::BeamSpot& beamspot;
    const reco::Track& track;
    int npxhits;
    int nsthits;
    int npxlayers;
    int nstlayers;
    double aeta;
    double dxybs;
    double sigmadxybs;
    bool pass;

    track_ex(const reco::BeamSpot& bs, const reco::Track& tk)
      : beamspot(bs), track(tk)
    {
      npxhits = tk.hitPattern().numberOfValidPixelHits();
      nsthits = tk.hitPattern().numberOfValidStripHits();
      npxlayers = tk.hitPattern().pixelLayersWithMeasurement();
      nstlayers = tk.hitPattern().stripLayersWithMeasurement();
      aeta = fabs(tk.eta());
      dxybs = tk.dxy(beamspot);
      sigmadxybs = dxybs / tk.dxyError();
      pass =
        tk.pt() > 1 &&
        tk.hitPattern().hasValidHitInFirstPixelBarrel() &&
        npxlayers >= 2 &&
        ((aeta < 2 && nstlayers >= 6) || (aeta >= 2 && nstlayers >= 7)) &&
        fabs(sigmadxybs) > 4;
    }
  };
};

// from RecoParticleFlow/PFProducer/plugins/importers/GeneralTracksImporter.cc
bool MFVPackedCandidates::goodPtResolution(const reco::Track& tk) const {
  //recheck that the track is high purity!
  if (!tk.quality(reco::TrackBase::highPurity))
    return false;
 
  const std::vector<double> _DPtovPtCut = {10.0, 10.0, 10.0, 10.0, 10.0, 5.0};
  const std::vector<unsigned> _NHitCut = { 3, 3, 3, 3, 3, 3 };
  const bool _useIterTracking = true;


  const bool _debug = false;

  const double P = tk.p();
  const double Pt = tk.pt();
  const double DPt = tk.ptError();
  const unsigned int NHit = 
    tk.hitPattern().trackerLayersWithMeasurement();
  const unsigned int NLostHit = 
    tk.hitPattern().trackerLayersWithoutMeasurement(reco::HitPattern::TRACK_HITS);
  const unsigned int LostHits = tk.numberOfLostHits();
  const double sigmaHad = sqrt(1.20*1.20/P+0.06*0.06) / (1.+LostHits);

  // Protection against 0 momentum tracks
  if ( P < 0.05 ) return false;
 
  if (_debug) std::cout << " PFBlockAlgo: PFrecTrack->Track Pt= "
		   << Pt << " DPt = " << DPt << std::endl;


  double dptCut = PFTrackAlgoTools::dPtCut(tk.algo(),_DPtovPtCut,_useIterTracking);
  unsigned int nhitCut    = PFTrackAlgoTools::nHitCut(tk.algo(),_NHitCut,_useIterTracking);

  if ( ( dptCut > 0. && 
	 DPt/Pt > dptCut*sigmaHad ) || 
       NHit < nhitCut ) { 
    if (_debug) std::cout << " PFBlockAlgo: skip badly measured track"
		     << ", P = " << P 
		     << ", Pt = " << Pt 
		     << " DPt = " << DPt 
		     << ", N(hits) = " << NHit << " (Lost : " << LostHits << "/" << NLostHit << ")"
			  << ", Algo = " << tk.algo()
		     << std::endl;
    if (_debug) std::cout << " cut is DPt/Pt < " << dptCut * sigmaHad << std::endl;
    if (_debug) std::cout << " cut is NHit >= " << nhitCut << std::endl;
    return false;
  }

  return true;
}

MFVPackedCandidates::MFVPackedCandidates(const edm::ParameterSet& cfg)
  : beamspot_token(consumes<reco::BeamSpot>(edm::InputTag("offlineBeamSpot"))),
    tracks_token(consumes<reco::TrackCollection>(edm::InputTag("generalTracks"))),
    packed_candidate_token(consumes<pat::PackedCandidateCollection>(edm::InputTag("packedPFCandidates"))),
    max_closest_cd_dist(cfg.getParameter<bool>("max_closest_cd_dist")),
    prints(cfg.getParameter<bool>("prints"))
{
  edm::Service<TFileService> fs;
  h_nmatch_v_nseed = fs->make<TH2F>("h_nmatch_v_nseed", "", 50, 0, 50, 50, 0, 50);
  h_nmatchpass_v_nseed = fs->make<TH2F>("h_nmatchpass_v_nseed", "", 50, 0, 50, 50, 0, 50);
  h_matchdist = fs->make<TH1F>("h_matchdist", "", 1000, 0, 0.01);
  h_nomatch_par[0] = fs->make<TH1F>("h_nomatch_par_0", "", 100, 0, 1000);
  h_nomatch_par[1] = fs->make<TH1F>("h_nomatch_par_1", "", 100, -3, 3);
  h_nomatch_par[2] = fs->make<TH1F>("h_nomatch_par_2", "", 100, -3.15, 3.15);
  h_nomatch_par[3] = fs->make<TH1F>("h_nomatch_par_3", "", 10000, -1, 1);
  h_nomatch_par[4] = fs->make<TH1F>("h_nomatch_par_4", "", 10000, -1, 1);
  h_nomatch_sigmadxybs = fs->make<TH1F>("h_nomatch_sigmadxybs", "", 10000, -1, 1);
  h_nomatch_pxl = fs->make<TH1F>("h_nomatch_pxl", "", 10, 0, 10);
  h_nomatch_stl = fs->make<TH1F>("h_nomatch_stl", "", 20, 0, 20);
  h_nomatch_highpurity = fs->make<TH1F>("h_nomatch_highpurity", "", 2, 0, 2);
  h_nomatch_losthits = fs->make<TH1F>("h_nomatch_losthits", "", 50, 0, 50);
  h_nomatch_lostlayers = fs->make<TH1F>("h_nomatch_lostlayers", "", 50, 0, 50);
  h_nomatch_p = fs->make<TH1F>("h_nomatch_p", "", 20, 0, 1);
  h_nomatch_dptopt = fs->make<TH1F>("h_nomatch_dptopt", "", 100, 0, 5);
  h_nomatch_goodptrel = fs->make<TH1F>("h_nomatch_goodptrel", "", 2, 0, 2);
  for (int i = 0; i < 5; ++i) {
    h_fracdelta_par[i] = fs->make<TH1F>(TString::Format("h_fracdelta_par_%i", i), "", 10000, -1, 1);
    for (int j = i; j < 5; ++j)
      h_fracdelta_cov[i][j] = fs->make<TH1F>(TString::Format("h_fracdelta_cov_%i_%i", i, j), "", 10000, -1e-2, 1e-2);
  }
  h_fracdelta_sigmadxybs = fs->make<TH1F>("h_fracdelta_sigmadxybs", "", 10000, -1, 1);
  h_delta_pxl = fs->make<TH1F>("h_delta_pxl", "", 100, -50, 50);
  h_delta_stl = fs->make<TH1F>("h_delta_stl", "", 100, -50, 50);
}

void MFVPackedCandidates::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<reco::BeamSpot> beamspot;
  event.getByToken(beamspot_token, beamspot);
  
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
  int nmatchpass = 0;

  if (prints) printf("generalTracks that pass our cuts (all # = %lu):\n", tracks->size());
  for (size_t itk = 0, itke = tracks->size(); itk < itke; ++itk) {
    const reco::Track& tk = (*tracks)[itk];
    const track_ex te(*beamspot, tk);

    if (te.pass) {
      ++npass;

      if (prints) {
        printf("tk #%4lu: pt %10.4g +- %10.4g eta %10.4g +- %10.4g phi %10.4g +- %10.4g dxy %10.4g +- %10.4g dz %10.4g +- %10.4g\n",
               itk, tk.pt(), tk.ptError(), tk.eta(), tk.etaError(), tk.phi(), tk.phiError(), tk.dxy(), tk.dxyError(), tk.dz(), tk.dzError());
        printf("  # px hits: %2i layers: %2i st hits: %2i layers: %2i   dxybs: %10.4g  sigmadxybs: %10.4g\n",
               te.npxhits, te.npxlayers, te.nsthits, te.nstlayers, te.dxybs, te.sigmadxybs);
      }

      const pat::PackedCandidate* closest_cd = 0;
      double closest_cd_dist = 100;
      for (size_t icd = 0, icde = packed_candidates->size(); icd < icde; ++icd) {
        const pat::PackedCandidate& cd = (*packed_candidates)[icd];
        if (cd.charge()) {
          const reco::Track& cd_tk = cd.pseudoTrack();
          const double dist = reco::deltaR(tk, cd_tk);
          if (dist < closest_cd_dist) {
            closest_cd = &cd;
            closest_cd_dist = dist;
          }
        }
      }

      h_matchdist->Fill(closest_cd_dist);
      if (closest_cd_dist > max_closest_cd_dist)
        closest_cd = 0;

      if (closest_cd) {
        ++nmatch;
        const reco::Track& cd_tk = closest_cd->pseudoTrack();
        const track_ex cd_te(*beamspot, cd_tk);

        if (cd_te.pass)
          ++nmatchpass;

        h_fracdelta_par[0]->Fill(cd_tk.pt()  / tk.pt()  - 1);
        h_fracdelta_par[1]->Fill(cd_tk.eta() / tk.eta() - 1);
        h_fracdelta_par[2]->Fill(cd_tk.phi() / tk.phi() - 1);
        h_fracdelta_par[3]->Fill(cd_tk.dxy() / tk.dxy() - 1);
        h_fracdelta_par[4]->Fill(cd_tk.dz()  / tk.dz()  - 1);
        for (int i = 0; i < 5; ++i)
          for (int j = i; j < 5; ++j)
            if (fabs(tk.covariance(i,j)) > 0)
              h_fracdelta_cov[i][j]->Fill(cd_tk.covariance(i,j) / tk.covariance(i,j) - 1);
        h_fracdelta_sigmadxybs->Fill(cd_te.sigmadxybs / te.sigmadxybs - 1);
        h_delta_pxl->Fill(cd_te.npxlayers - te.npxlayers);
        h_delta_stl->Fill(cd_te.nstlayers - te.nstlayers);
        if (prints) {
          printf("  the closest CD with dist %f:\n", closest_cd_dist);
          printf("    pt %10.4g +- %10.4g eta %10.4g +- %10.4g phi %10.4g +- %10.4g dxy %10.4g +- %10.4g dz %10.4g +- %10.4g\n",
                 cd_tk.pt(), cd_tk.ptError(), cd_tk.eta(), cd_tk.etaError(), cd_tk.phi(), cd_tk.phiError(), cd_tk.dxy(), cd_tk.dxyError(), cd_tk.dz(), cd_tk.dzError());
          printf("    # px hits: %2i layers: %2i st hits: %2i layers: %2i   dxybs: %10.4g  sigmadxybs: %10.4g\n",
                 cd_te.npxhits, cd_te.npxlayers, cd_te.nsthits, cd_te.nstlayers, cd_te.dxybs, cd_te.sigmadxybs);
          printf("  also passes? %i\n", cd_te.pass);
        }
      }
      else {
        h_nomatch_par[0]->Fill(tk.pt() );
        h_nomatch_par[1]->Fill(tk.eta());
        h_nomatch_par[2]->Fill(tk.phi());
        h_nomatch_par[3]->Fill(tk.dxy());
        h_nomatch_par[4]->Fill(tk.dz() );
        h_nomatch_sigmadxybs->Fill(te.sigmadxybs);
        h_nomatch_pxl->Fill(te.npxlayers);
        h_nomatch_stl->Fill(te.nstlayers);
        const bool highpurity = tk.quality(reco::TrackBase::highPurity);
        const bool goodptrel = goodPtResolution(tk);
        h_nomatch_highpurity->Fill(highpurity);
        if (prints) printf("  NO CD MATCH highpurity %i goodptrel %i\n", highpurity, goodptrel);
        if (highpurity) {
          h_nomatch_losthits->Fill(tk.numberOfLostHits());
          h_nomatch_lostlayers->Fill(tk.hitPattern().trackerLayersWithoutMeasurement(reco::HitPattern::TRACK_HITS));
          h_nomatch_p->Fill(tk.p());
          h_nomatch_dptopt->Fill(tk.pt() > 0 ? tk.ptError()/tk.pt() : 999);
          h_nomatch_goodptrel->Fill(goodptrel);
        }
      }
    }
  }

  h_nmatch_v_nseed->Fill(npass, nmatch);
  h_nmatchpass_v_nseed->Fill(npass, nmatchpass);
  if (prints) printf("# general passing: %i  # with match: %i that pass: %i\n", npass, nmatch, nmatchpass);
}

DEFINE_FWK_MODULE(MFVPackedCandidates);
