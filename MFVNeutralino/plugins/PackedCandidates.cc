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
#include "JMTucker/Tools/interface/TrackHistos.h"

class MFVPackedCandidates : public edm::EDAnalyzer {
public:
  explicit MFVPackedCandidates(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);
private:
  const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
  const edm::EDGetTokenT<reco::VertexCollection> primary_vertices_token;
  const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
  const edm::EDGetTokenT<pat::PackedCandidateCollection> packed_candidate_token;
  const double max_closest_cd_dist;
  const bool prints;

  TH1F* h_nseed;
  TH1F* h_nmatch;
  TH1F* h_nmatchpass;
  TH2F* h_nmatch_v_nseed;
  TH2F* h_nmatchpass_v_nseed;
  TH1F* h_matchdist;
  TH1F* h_matchdist_notk;

  jmt::TrackHistos h_all;
  jmt::TrackHistos h_highpurity;
  jmt::TrackHistos h_seed;
  jmt::TrackHistos h_seed_highpurity;
  jmt::TrackHistos h_match;
  jmt::TrackHistos h_match_pass;
  jmt::TrackHistos h_nomatch;
  jmt::TrackHistos h_nomatch_highpurity;
  jmt::TrackHistos h_nomatch_highpurity_goodptres;

  TH1F* h_delta_pt;
  TH1F* h_delta_eta;
  TH1F* h_delta_phi;
  TH1F* h_delta_dxy;
  TH1F* h_delta_dz;
  TH1F* h_delta_dxybs;
  TH1F* h_delta_dxypv;
  TH1F* h_delta_dzbs;
  TH1F* h_delta_dzpv;
  TH1F* h_delta_sigmadxybs;
  TH1F* h_delta_pxh;
  TH1F* h_delta_pxl;
  TH1F* h_delta_sth;
  TH1F* h_delta_stl;

  struct track_ex {
    const reco::BeamSpot& bs;
    const reco::Vertex* pv;
    const reco::Track& tk;

    const bool highpurity;
    const bool goodptres;
    const int npxhits;
    const int nsthits;
    const int npxlayers;
    const int nstlayers;
    const int nlosthits;
    const int nlostlayers;
    const double aeta;
    const double dxybs;
    const double dxypv;
    const double dzbs;
    const double dzpv;
    const double sigmadxybs;
    const double dptopt;
    const bool pass;

    track_ex(const reco::BeamSpot& bs_, const reco::Vertex* pv_, const reco::Track& tk_);
  };
};

namespace {
  // from RecoParticleFlow/PFProducer/plugins/importers/GeneralTracksImporter.cc
  bool goodPtResolution(const reco::Track& tk) {
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
}

MFVPackedCandidates::track_ex::track_ex(const reco::BeamSpot& bs_, const reco::Vertex* pv_, const reco::Track& tk_)
  : bs(bs_), pv(pv_), tk(tk_),

    highpurity(tk.quality(reco::TrackBase::highPurity)),
    goodptres(goodPtResolution(tk)),
    npxhits(tk.hitPattern().numberOfValidPixelHits()),
    nsthits(tk.hitPattern().numberOfValidStripHits()),
    npxlayers(tk.hitPattern().pixelLayersWithMeasurement()),
    nstlayers(tk.hitPattern().stripLayersWithMeasurement()),
    nlosthits(tk.numberOfLostHits()),
    nlostlayers(tk.hitPattern().trackerLayersWithoutMeasurement(reco::HitPattern::TRACK_HITS)),
    aeta(fabs(tk.eta())),
    dxybs(tk.dxy(bs)),
    dxypv(pv ? tk.dxy(pv->position()) : 1e99),
    dzbs(tk.dz(bs.position())),
    dzpv(pv ? tk.dz(pv->position()) : 1e99),
    sigmadxybs(dxybs / tk.dxyError()),
    dptopt(tk.pt() > 0 ? tk.ptError() / tk.pt() : -999),

    pass(tk.pt() > 1 &&
         tk.hitPattern().hasValidHitInFirstPixelBarrel() &&
         npxlayers >= 2 &&
         ((aeta < 2 && nstlayers >= 6) || (aeta >= 2 && nstlayers >= 7)) &&
         fabs(sigmadxybs) > 4)
{}

MFVPackedCandidates::MFVPackedCandidates(const edm::ParameterSet& cfg)
  : beamspot_token(consumes<reco::BeamSpot>(edm::InputTag("offlineBeamSpot"))),
    primary_vertices_token(consumes<reco::VertexCollection>(edm::InputTag("goodOfflinePrimaryVertices"))),
    tracks_token(consumes<reco::TrackCollection>(edm::InputTag("generalTracks"))),
    packed_candidate_token(consumes<pat::PackedCandidateCollection>(edm::InputTag("packedPFCandidates"))),
    max_closest_cd_dist(cfg.getParameter<double>("max_closest_cd_dist")),
    prints(cfg.getParameter<bool>("prints")),
    h_all("all"),
    h_highpurity("highpurity"),
    h_seed("seed"),
    h_seed_highpurity("seed_highpurity"),
    h_match("match"),
    h_match_pass("match_pass"),
    h_nomatch("nomatch"),
    h_nomatch_highpurity("nomatch_highpurity"),
    h_nomatch_highpurity_goodptres("nomatch_highpurity_goodptres")
{
  edm::Service<TFileService> fs;
  h_nseed = fs->make<TH1F>("h_nseed", "", 50, 0, 50);
  h_nmatch = fs->make<TH1F>("h_nmatch", "", 50, 0, 50);
  h_nmatchpass = fs->make<TH1F>("h_nmatchpass", "", 50, 0, 50);
  h_nmatch_v_nseed = fs->make<TH2F>("h_nmatch_v_nseed", "", 50, 0, 50, 50, 0, 50);
  h_nmatchpass_v_nseed = fs->make<TH2F>("h_nmatchpass_v_nseed", "", 50, 0, 50, 50, 0, 50);
  h_matchdist = fs->make<TH1F>("h_matchdist", "", 10000, 0, 0.1);
  h_matchdist_notk = fs->make<TH1F>("h_matchdist_notk", "", 10000, 0, 0.1);

  h_delta_pt = fs->make<TH1F>("h_delta_par_pt", "", 1000, -50, 50);
  h_delta_eta = fs->make<TH1F>("h_delta_par_eta", "", 1000, -3, 3);
  h_delta_phi = fs->make<TH1F>("h_delta_par_phi", "", 1000, -3.15, 3.15);
  h_delta_dxy = fs->make<TH1F>("h_delta_par_dxy", "", 1000, -1, 1);
  h_delta_dz = fs->make<TH1F>("h_delta_par_dz", "", 1000, -1, 1);
  h_delta_dxybs = fs->make<TH1F>("h_delta_par_dxybs", "", 1000, -1, 1);
  h_delta_dxypv = fs->make<TH1F>("h_delta_par_dxypv", "", 1000, -1, 1);
  h_delta_dzbs = fs->make<TH1F>("h_delta_par_dzbs", "", 1000, -1, 1);
  h_delta_dzpv = fs->make<TH1F>("h_delta_par_dzpv", "", 1000, -1, 1);
  h_delta_sigmadxybs = fs->make<TH1F>("h_delta_sigmadxybs", "", 1000, -1, 1);
  h_delta_pxh = fs->make<TH1F>("h_delta_pxh", "", 40, -20, 20);
  h_delta_pxl = fs->make<TH1F>("h_delta_pxl", "", 40, -20, 20);
  h_delta_sth = fs->make<TH1F>("h_delta_sth", "", 100, -50, 50);
  h_delta_stl = fs->make<TH1F>("h_delta_stl", "", 100, -50, 50);
}

void MFVPackedCandidates::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<reco::BeamSpot> beamspot;
  event.getByToken(beamspot_token, beamspot);
  
  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByToken(primary_vertices_token, primary_vertices);
  const reco::Vertex* pv = 0;
  if (primary_vertices->size())
    pv = &primary_vertices->at(0);

  edm::Handle<reco::TrackCollection> tracks;
  event.getByToken(tracks_token, tracks);

  edm::Handle<pat::PackedCandidateCollection> packed_candidates;
  event.getByToken(packed_candidate_token, packed_candidates);

  int nseed = 0;
  int nmatch = 0;
  int nmatchpass = 0;

  if (prints) printf("generalTracks that pass our cuts (all # = %lu):\n", tracks->size());
  for (size_t itk = 0, itke = tracks->size(); itk < itke; ++itk) {
    const reco::Track& tk = (*tracks)[itk];
    const track_ex te(*beamspot, pv, tk);

    h_all.Fill(tk, &*beamspot, pv);
    if (te.highpurity)
      h_highpurity.Fill(tk, &*beamspot, pv);

    if (te.pass) {
      ++nseed;

      h_seed.Fill(tk, &*beamspot, pv);
      if (te.highpurity)
        h_seed_highpurity.Fill(tk, &*beamspot, pv);

      if (prints) {
        printf("tk #%4lu: pt %10.4g +- %10.4g eta %10.4g +- %10.4g phi %10.4g +- %10.4g dxy %10.4g +- %10.4g dz %10.4g +- %10.4g\n",
               itk, tk.pt(), tk.ptError(), tk.eta(), tk.etaError(), tk.phi(), tk.phiError(), tk.dxy(), tk.dxyError(), tk.dz(), tk.dzError());
        printf("  # px hits: %2i layers: %2i st hits: %2i layers: %2i   dxybs: %10.4g  sigmadxybs: %10.4g\n",
               te.npxhits, te.npxlayers, te.nsthits, te.nstlayers, te.dxybs, te.sigmadxybs);
      }

      const pat::PackedCandidate* closest_cd = 0;
      //const pat::PackedCandidate* closest_cd_notk = 0;
      double closest_cd_dist = 100;
      double closest_cd_notk_dist = 100;
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
        else {
          const double dist = reco::deltaR(tk, cd);
          if (dist < closest_cd_notk_dist) {
            //closest_cd_notk = &cd;
            closest_cd_notk_dist = dist;
          }
        }
      }

      h_matchdist->Fill(closest_cd_dist);
      h_matchdist_notk->Fill(closest_cd_notk_dist);

      if (closest_cd_dist > max_closest_cd_dist)
        closest_cd = 0;

      if (closest_cd) {
        ++nmatch;
        const reco::Track& cd_tk = closest_cd->pseudoTrack();
        const track_ex cd_te(*beamspot, pv, cd_tk);

        h_match.Fill(tk, &*beamspot, pv);

        if (cd_te.pass) {
          h_match_pass.Fill(tk, &*beamspot, pv);
          ++nmatchpass;
        }

        h_delta_pt->Fill(cd_tk.pt() - tk.pt());
        h_delta_eta->Fill(cd_tk.eta() - tk.eta());
        h_delta_phi->Fill(cd_tk.phi() - tk.phi());
        h_delta_dxy->Fill(cd_tk.dxy() - tk.dxy());
        h_delta_dz->Fill(cd_tk.dz() - tk.dz());
        h_delta_dxybs->Fill(cd_te.dxybs - te.dxybs);
        h_delta_dxypv->Fill(cd_te.dxypv - te.dxypv);
        h_delta_dzbs->Fill(cd_te.dzbs - te.dzbs);
        h_delta_dzpv->Fill(cd_te.dzpv - te.dzpv);
        h_delta_sigmadxybs->Fill(cd_te.sigmadxybs / te.sigmadxybs - 1);
        h_delta_pxh->Fill(cd_te.npxhits - te.npxhits);
        h_delta_pxl->Fill(cd_te.npxlayers - te.npxlayers);
        h_delta_sth->Fill(cd_te.nsthits - te.nsthits);
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
        if (prints) printf("  NO CD MATCH highpurity %i goodptres %i\n", te.highpurity, te.goodptres);

        h_nomatch.Fill(tk, &*beamspot, pv);
        if (te.highpurity) {
          h_nomatch_highpurity.Fill(tk, &*beamspot, pv);
          if (te.goodptres)
            h_nomatch_highpurity_goodptres.Fill(tk, &*beamspot, pv);
        }
      }
    }
  }

  h_nseed->Fill(nseed);
  h_nmatch->Fill(nmatch);
  h_nmatchpass->Fill(nmatchpass);
  h_nmatch_v_nseed->Fill(nseed, nmatch);
  h_nmatchpass_v_nseed->Fill(nseed, nmatchpass);
  if (prints) printf("# general passing: %i  # with match: %i that pass: %i\n", nseed, nmatch, nmatchpass);
}

DEFINE_FWK_MODULE(MFVPackedCandidates);
