#include "TH2.h"
#include "CLHEP/Random/RandBinomial.h"
#include "CLHEP/Random/RandomEngine.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/RandomNumberGenerator.h"
#include "TrackingTools/IPTools/interface/IPTools.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"

class MFVVertexTracks : public edm::EDFilter {
public:
  MFVVertexTracks(const edm::ParameterSet&);
  virtual bool filter(edm::Event&, const edm::EventSetup&);

private:
  const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
  const bool use_primary_vertices;
  const edm::EDGetTokenT<reco::VertexCollection> primary_vertices_token;
  const bool disregard_event;
  const bool use_tracks;
  const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
  const bool use_non_pv_tracks;
  const bool use_non_pvs_tracks;
  const bool use_pf_candidates;
  const edm::EDGetTokenT<reco::PFCandidateCollection> pf_candidate_token;
  const bool use_pf_jets;
  const edm::EDGetTokenT<reco::PFJetCollection> pf_jet_token;
  const bool use_pat_jets;
  const edm::EDGetTokenT<pat::JetCollection> pat_jet_token;
  const bool use_second_tracks;
  const edm::EDGetTokenT<reco::TrackCollection> second_tracks_token;
  const int min_n_seed_tracks;
  const bool no_track_cuts;
  const double min_seed_jet_pt;
  const double min_track_pt;
  const double min_track_dxy;
  const double min_track_sigmadxy;
  const double min_track_sigmadxypv;
  const int min_track_hit_r;
  const int min_track_nhits;
  const int min_track_npxhits;
  const int min_track_npxlayers;
  const int min_track_nstlayers;
  const double max_track_dxyerr;
  const double max_track_dxyipverr;
  const double max_track_d3dipverr;
  const bool jumble_tracks;
  const double remove_tracks_frac;
  const bool histos;
  const bool verbose;
  const std::string module_label;

  TH1F* h_n_all_tracks;
  TH1F* h_all_track_pars[6];
  TH1F* h_all_track_errs[6];
  TH1F* h_all_track_sigmadxybs;
  TH1F* h_all_track_sigmadxypv;
  TH1F* h_all_track_nhits;
  TH1F* h_all_track_npxhits;
  TH1F* h_all_track_nsthits;
  TH1F* h_all_track_npxlayers;
  TH1F* h_all_track_nstlayers;
  TH1F* h_n_seed_tracks;
  TH1F* h_seed_track_pars[6];
  TH1F* h_seed_track_errs[6];
  TH1F* h_seed_track_sigmadxybs;
  TH1F* h_seed_track_sigmadxypv;
  TH1F* h_seed_track_nhits;
  TH1F* h_seed_track_npxhits;
  TH1F* h_seed_track_nsthits;
  TH1F* h_seed_track_npxlayers;
  TH1F* h_seed_track_nstlayers;
  TH1F* h_seed_nm1_pt;
  TH1F* h_seed_nm1_npxlayers;
  TH1F* h_seed_nm1_nstlayers;
  TH1F* h_seed_nm1_sigmadxybs;
};

MFVVertexTracks::MFVVertexTracks(const edm::ParameterSet& cfg)
  : beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot_src"))),
    use_primary_vertices(cfg.getParameter<edm::InputTag>("primary_vertices_src").label() != ""),
    primary_vertices_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("primary_vertices_src"))),
    disregard_event(cfg.getParameter<bool>("disregard_event")),
    use_tracks(cfg.getParameter<bool>("use_tracks")),
    tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("tracks_src"))),
    use_non_pv_tracks(cfg.getParameter<bool>("use_non_pv_tracks")),
    use_non_pvs_tracks(cfg.getParameter<bool>("use_non_pvs_tracks")),
    use_pf_candidates(cfg.getParameter<bool>("use_pf_candidates")),
    pf_candidate_token(use_pf_candidates ? consumes<reco::PFCandidateCollection>(cfg.getParameter<edm::InputTag>("pf_candidate_src")) : edm::EDGetTokenT<reco::PFCandidateCollection>()),
    use_pf_jets(cfg.getParameter<bool>("use_pf_jets")),
    pf_jet_token(use_pf_jets ? consumes<reco::PFJetCollection>(cfg.getParameter<edm::InputTag>("pf_jet_src")) : edm::EDGetTokenT<reco::PFJetCollection>()),
    use_pat_jets(cfg.getParameter<bool>("use_pat_jets")),
    pat_jet_token(use_pat_jets ? consumes<pat::JetCollection>(cfg.getParameter<edm::InputTag>("pat_jet_src")) : edm::EDGetTokenT<pat::JetCollection>()),
    use_second_tracks(cfg.getParameter<bool>("use_second_tracks")),
    second_tracks_token(use_second_tracks ? consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("second_tracks_src")) : edm::EDGetTokenT<reco::TrackCollection>()),
    min_n_seed_tracks(cfg.getParameter<int>("min_n_seed_tracks")),
    no_track_cuts(cfg.getParameter<bool>("no_track_cuts")),
    min_seed_jet_pt(cfg.getParameter<double>("min_seed_jet_pt")),
    min_track_pt(cfg.getParameter<double>("min_track_pt")),
    min_track_dxy(cfg.getParameter<double>("min_track_dxy")),
    min_track_sigmadxy(cfg.getParameter<double>("min_track_sigmadxy")),
    min_track_sigmadxypv(cfg.getParameter<double>("min_track_sigmadxypv")),
    min_track_hit_r(cfg.getParameter<int>("min_track_hit_r")),
    min_track_nhits(cfg.getParameter<int>("min_track_nhits")),
    min_track_npxhits(cfg.getParameter<int>("min_track_npxhits")),
    min_track_npxlayers(cfg.getParameter<int>("min_track_npxlayers")),
    min_track_nstlayers(cfg.getParameter<int>("min_track_nstlayers")),
    max_track_dxyerr(cfg.getParameter<double>("max_track_dxyerr")),
    max_track_dxyipverr(cfg.getParameter<double>("max_track_dxyipverr")),
    max_track_d3dipverr(cfg.getParameter<double>("max_track_d3dipverr")),
    jumble_tracks(cfg.getParameter<bool>("jumble_tracks")),
    remove_tracks_frac(cfg.getParameter<double>("remove_tracks_frac")),
    histos(cfg.getUntrackedParameter<bool>("histos", false)),
    verbose(cfg.getUntrackedParameter<bool>("verbose", false)),
    module_label(cfg.getParameter<std::string>("@module_label"))
{
  if (min_track_hit_r < 1 || min_track_hit_r > 4)
    throw cms::Exception("MFVVertexTracks") << "hit_r cuts may only be 1-4";

  if (use_tracks + use_non_pv_tracks + use_non_pvs_tracks + use_pf_candidates + use_pf_jets + use_pat_jets != 1)
    throw cms::Exception("MFVVertexTracks") << "must enable exactly one of use_tracks/use_non_pv_tracks/use_non_pvs_tracks/pf_candidates/pf_jets/pat_jets";

  if ((use_non_pv_tracks || use_non_pvs_tracks) && !use_primary_vertices)
    throw cms::Exception("MFVVertexTracks", "can't use_non_pv_tracks || use_non_pvs_tracks if !use_primary_vertices");

  edm::Service<edm::RandomNumberGenerator> rng;
  if ((jumble_tracks || remove_tracks_frac > 0) && !rng.isAvailable())
    throw cms::Exception("Vertexer") << "RandomNumberGeneratorService not available for jumbling or removing tracks!\n";

  produces<std::vector<reco::TrackRef>>("all");
  produces<std::vector<reco::TrackRef>>("seed");
  produces<reco::TrackCollection>("seed");

  if (histos) {
    edm::Service<TFileService> fs;

    h_n_all_tracks  = fs->make<TH1F>("h_n_all_tracks",  "", 200, 0, 2000);
    h_n_seed_tracks = fs->make<TH1F>("h_n_seed_tracks", "", 200, 0,  200);

    const char* par_names[6] = {"pt", "eta", "phi", "dxybs", "dxypv", "dz"};
    const int par_nbins[6] = {  50, 50, 50, 100, 100, 80 };
    const double par_lo[6] = {   0, -2.5, -3.15, -0.2, -0.2, -20 };
    const double par_hi[6] = {  10,  2.5,  3.15,  0.2,  0.2,  20 };
    const double err_lo[6] = { 0 };
    const double err_hi[6] = { 0.15, 0.01, 0.01, 0.2, 0.2, 0.4 };
    for (int i = 0; i < 6; ++i) {
      h_all_track_pars[i] = fs->make<TH1F>(TString::Format("h_all_track_%s",    par_names[i]), "", par_nbins[i], par_lo[i], par_hi[i]);
      h_all_track_errs[i] = fs->make<TH1F>(TString::Format("h_all_track_err%s", par_names[i]), "", par_nbins[i], err_lo[i], err_hi[i]);
    }

    h_all_track_sigmadxybs = fs->make<TH1F>("h_all_track_sigmadxybs", "", 40, -10, 10);
    h_all_track_sigmadxypv = fs->make<TH1F>("h_all_track_sigmadxypv", "", 40, -10, 10);
    h_all_track_nhits      = fs->make<TH1F>("h_all_track_nhits",      "", 40,   0, 40);
    h_all_track_npxhits    = fs->make<TH1F>("h_all_track_npxhits",    "", 12,   0, 12);
    h_all_track_nsthits    = fs->make<TH1F>("h_all_track_nsthits",    "", 28,   0, 28);
    h_all_track_npxlayers  = fs->make<TH1F>("h_all_track_npxlayers",  "", 10,   0, 10);
    h_all_track_nstlayers  = fs->make<TH1F>("h_all_track_nstlayers",  "", 30,   0, 30);

    for (int i = 0; i < 6; ++i) {
      h_seed_track_pars[i] = fs->make<TH1F>(TString::Format("h_seed_track_%s",    par_names[i]), "", par_nbins[i], par_lo[i], par_hi[i]);
      h_seed_track_errs[i] = fs->make<TH1F>(TString::Format("h_seed_track_err%s", par_names[i]), "", par_nbins[i], err_lo[i], err_hi[i]);
    }

    h_seed_track_sigmadxybs = fs->make<TH1F>("h_seed_track_sigmadxybs", "", 40, -10, 10);
    h_seed_track_sigmadxypv = fs->make<TH1F>("h_seed_track_sigmadxypv", "", 40, -10, 10);
    h_seed_track_nhits      = fs->make<TH1F>("h_seed_track_nhits",      "", 40,   0, 40);
    h_seed_track_npxhits    = fs->make<TH1F>("h_seed_track_npxhits",    "", 12,   0, 12);
    h_seed_track_nsthits    = fs->make<TH1F>("h_seed_track_nsthits",    "", 28,   0, 28);
    h_seed_track_npxlayers  = fs->make<TH1F>("h_seed_track_npxlayers",  "", 10,   0, 10);
    h_seed_track_nstlayers  = fs->make<TH1F>("h_seed_track_nstlayers",  "", 30,   0, 30);

    h_seed_nm1_pt = fs->make<TH1F>("h_seed_nm1_pt", "", 50, 0, 10);
    h_seed_nm1_npxlayers = fs->make<TH1F>("h_seed_nm1_npxlayers", "", 10, 0, 10);
    h_seed_nm1_nstlayers = fs->make<TH1F>("h_seed_nm1_nstlayers", "", 30, 0, 30);
    h_seed_nm1_sigmadxybs = fs->make<TH1F>("h_seed_nm1_sigmadxybs", "", 40, -10, 10);
  }
}

bool MFVVertexTracks::filter(edm::Event& event, const edm::EventSetup& setup) {
  if (verbose)
    std::cout << "MFVVertexTracks " << module_label << " run " << event.id().run() << " lumi " << event.luminosityBlock() << " event " << event.id().event() << "\n";

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByToken(beamspot_token, beamspot);

  edm::Handle<reco::VertexCollection> primary_vertices;
  const reco::Vertex* primary_vertex = 0;
  if (use_primary_vertices) {
    event.getByToken(primary_vertices_token, primary_vertices);
    if (primary_vertices->size())
      primary_vertex = &primary_vertices->at(0);
  }

  edm::ESHandle<TransientTrackBuilder> tt_builder;
  setup.get<TransientTrackRecord>().get("TransientTrackBuilder", tt_builder);

  std::unique_ptr<std::vector<reco::TrackRef>> all_tracks (new std::vector<reco::TrackRef>);
  std::unique_ptr<std::vector<reco::TrackRef>> seed_tracks(new std::vector<reco::TrackRef>);
  std::unique_ptr<reco::TrackCollection> seed_tracks_copy(new reco::TrackCollection);

  if (!disregard_event) {
    if (use_tracks) {
      edm::Handle<reco::TrackCollection> tracks;
      event.getByToken(tracks_token, tracks);
      for (size_t i = 0, ie = tracks->size(); i < ie; ++i)
        all_tracks->push_back(reco::TrackRef(tracks, i));
    }
    else if (use_non_pv_tracks || use_non_pvs_tracks) {
      std::map<reco::TrackRef, std::vector<std::pair<int, float> > > tracks_in_pvs;
      for (size_t i = 0, ie = primary_vertices->size(); i < ie; ++i) {
        const reco::Vertex& pv = primary_vertices->at(i);
        for (auto it = pv.tracks_begin(), ite = pv.tracks_end(); it != ite; ++it) {
          float w = pv.trackWeight(*it);
          reco::TrackRef tk = it->castTo<reco::TrackRef>();
          tracks_in_pvs[tk].push_back(std::make_pair(i, w));
        }
      }

      edm::Handle<reco::TrackCollection> tracks;
      event.getByToken(tracks_token, tracks);
      for (size_t i = 0, ie = tracks->size(); i < ie; ++i) {
        reco::TrackRef tkref(tracks, i);
        bool ok = true;
        for (const auto& pv_use : tracks_in_pvs[tkref])
          if (use_non_pvs_tracks || (use_non_pv_tracks && pv_use.first == 0)) {
            ok = false;
            break;
          }

        if (ok)
          all_tracks->push_back(tkref);
      }
    }
    else if (use_pf_candidates) {
      edm::Handle<reco::PFCandidateCollection> pf_candidates;
      event.getByToken(pf_candidate_token, pf_candidates);

      for (const reco::PFCandidate& cand : *pf_candidates) {
        reco::TrackRef tkref = cand.trackRef();
        if (tkref.isNonnull())
          all_tracks->push_back(tkref);
      }
    }
    else if (use_pf_jets) {
      edm::Handle<reco::PFJetCollection> jets;
      event.getByToken(pf_jet_token, jets);
      for (const reco::PFJet& jet : *jets) {
        if (jet.pt() > min_seed_jet_pt &&
            fabs(jet.eta()) < 2.5 &&
            jet.numberOfDaughters() > 1 &&
            jet.neutralHadronEnergyFraction() < 0.99 &&
            jet.neutralEmEnergyFraction() < 0.99 &&
            (fabs(jet.eta()) >= 2.4 || (jet.chargedEmEnergyFraction() < 0.99 && jet.chargedHadronEnergyFraction() > 0. && jet.chargedMultiplicity() > 0))) {
          for (const reco::TrackRef& tk : jet.getTrackRefs())
            all_tracks->push_back(tk);
        }
      }
    }
    else if (use_pat_jets) {
      edm::Handle<pat::JetCollection> jets;
      event.getByToken(pat_jet_token, jets);
      for (const pat::Jet& jet : *jets) {
        if (jet.pt() > min_seed_jet_pt) { // assume rest of id above already applied
          for (const reco::PFCandidatePtr& pfcand : jet.getPFConstituents()) {
            const reco::TrackRef& tk = pfcand->trackRef();
            if (tk.isNonnull())
              all_tracks->push_back(tk);
          }
        }
      }
    }
  }

  const size_t second_tracks_start_at = all_tracks->size(); // no cuts are applied to second_tracks since the hits cuts are hard to do without having hit info stored

  if (use_second_tracks) {
    edm::Handle<reco::TrackCollection> tracks;
    event.getByToken(second_tracks_token, tracks);
    if (verbose) printf("second tracks start at %lu and there are %lu of them\n", second_tracks_start_at, tracks->size());
    for (size_t i = 0, ie = tracks->size(); i < ie; ++i)
      all_tracks->push_back(reco::TrackRef(tracks, i));
  }

  if (jumble_tracks) {
    assert(!use_second_tracks); // would break second_tracks_start_at cut skipping logic
    edm::Service<edm::RandomNumberGenerator> rng;
    CLHEP::HepRandomEngine& rng_engine = rng->getEngine(event.streamID());
    auto random_converter = [&](size_t n) { return size_t(rng_engine.flat() * n); };
    std::random_shuffle(all_tracks->begin(), all_tracks->end(), random_converter);
  }

  for (size_t i = 0, ie = all_tracks->size(); i < ie; ++i) {
    const reco::TrackRef& tk = (*all_tracks)[i];
    const bool is_second_track = i >= second_tracks_start_at;

    // copy/calculate cheap things, which may be used later in histos
    const double pt = tk->pt();
    const double dxybs = tk->dxy(*beamspot);
    const double dxypv = primary_vertex ? tk->dxy(primary_vertex->position()) : 1e99;
    const double dxyerr = tk->dxyError();
    const double sigmadxybs = dxybs / dxyerr;
    const double sigmadxypv = dxypv / dxyerr;
    const int nhits = tk->hitPattern().numberOfValidHits();
    const int npxhits = tk->hitPattern().numberOfValidPixelHits();
    const int nsthits = tk->hitPattern().numberOfValidStripHits();
    const int npxlayers = tk->hitPattern().pixelLayersWithMeasurement();
    const int nstlayers = tk->hitPattern().stripLayersWithMeasurement();
    int min_r = 2000000000;
    for (int i = 1; i <= 4; ++i)
      if (tk->hitPattern().hasValidHitInPixelLayer(PixelSubdetector::PixelBarrel,i)) {
        min_r = i;
        break;
      }

    bool use = no_track_cuts || is_second_track || [&]() {

      const bool use_cheap =
        pt > min_track_pt &&
        fabs(dxybs) > min_track_dxy &&
        dxyerr < max_track_dxyerr &&
        fabs(sigmadxybs) > min_track_sigmadxy &&
        fabs(sigmadxypv) > min_track_sigmadxypv &&
        nhits >= min_track_nhits &&
        npxhits >= min_track_npxhits &&
        npxlayers >= min_track_npxlayers &&
        nstlayers >= min_track_nstlayers &&
        (min_track_hit_r == 999 || min_r <= min_track_hit_r);

      if (!use_cheap) return false;

      if (primary_vertex && (max_track_dxyipverr > 0 || max_track_d3dipverr > 0)) {
        reco::TransientTrack ttk = tt_builder->build(tk);
        if (max_track_dxyipverr > 0) {
          auto dxy_ipv = IPTools::absoluteTransverseImpactParameter(ttk, *primary_vertex); if (!dxy_ipv.first || dxy_ipv.second.error() >= max_track_dxyipverr) return false;
        }
        if (max_track_d3dipverr > 0) {
          auto d3d_ipv = IPTools::absoluteImpactParameter3D        (ttk, *primary_vertex); if (!d3d_ipv.first || d3d_ipv.second.error() >= max_track_d3dipverr) return false;
        }
      }

      return true;
    }();

    if (use && remove_tracks_frac > 0) {
      // special values:
      // remove_tracks_frac < 1: throw out that % of tracks
      // 1 <= remove_tracks_frac < 50: throw out tracks according to central values of data/mc in cosmics study in AN-15-206
      // 50 <= remove_tracks_frac < 100: ditto but propagate error bars through and add in quadrature to value (overblown)
      // 100 <= remove_tracks_frac: throw binomials according to those values
      edm::Service<edm::RandomNumberGenerator> rng;
      CLHEP::HepRandomEngine& rng_engine = rng->getEngine(event.streamID());
      double prob = 0;
      int ieta = 0;

      if (1 <= remove_tracks_frac) {
        const double ad = fabs(dxybs);
        if      (0    <= ad && ad < 0.25) ieta = 0;
        else if (0.25 <= ad && ad < 0.50) ieta = 1;
        else if (0.50 <= ad && ad < 0.75) ieta = 2;
        else if (0.75 <= ad && ad < 1.00) ieta = 3;
        else if (1.00 <= ad && ad < 1.50) ieta = 4;
        else if (1.50 <= ad && ad < 2.00) ieta = 5;
        else if (2.00 <= ad)              ieta = 6;
      }

      if (remove_tracks_frac < 1)
        prob = remove_tracks_frac;
      else if (1 <= remove_tracks_frac && remove_tracks_frac < 100) {
        // digitized Fig. 25 of AN-15-206 (pdf retrieved from tdr svn on 7/24/2018), https://apps.automeris.io/wpd/ is awesome
        const double probs[2][7] = {
          { 0.02, 0.04, 0.01, 0.01, 0.07, 0.11, 0.07 }, // without including error bars
          { 0.04, 0.05, 0.03, 0.03, 0.08, 0.12, 0.09 }  // propagate error bars then add in quad shift and unc
        };
        prob = probs[remove_tracks_frac >= 50][ieta];
      }
      else if (100 <= remove_tracks_frac) {
        const double N[2][7] = { { 160, 194, 104, 264, 303, 450, 414 },   // mc
                                 {  55,  69,  80,  59, 157, 131, 142 } }; // data
        const double p[2][7] = { { 0.960, 0.957, 0.977, 0.953, 0.928, 0.854, 0.800 },
                                 { 0.945, 0.922, 0.971, 0.964, 0.861, 0.761, 0.745 } };
        CLHEP::RandBinomial rr(rng_engine);
        const double mc   = rr.shoot(N[0][ieta], p[0][ieta]) / N[0][ieta];
        const double data = rr.shoot(N[1][ieta], p[1][ieta]) / N[1][ieta];
        prob = mc > data ? mc/data - 1 : 0;
      }

      if (rng_engine.flat() < prob)
        use = false;
    }

    /////////////

    if (use) {
      seed_tracks->push_back(tk);
      seed_tracks_copy->push_back(*tk);
    }

    if (verbose) {
      printf("track %5lu: pt: %7.3f dxy: %7.3f nhits %3i ", i, pt, dxybs, nhits);
      if (use)
        printf(" selected for seed! (#%lu)", seed_tracks->size()-1);
      printf("\n");
    }

    if (histos) {
      const double pars[6] = {pt, tk->eta(), tk->phi(), dxybs, dxypv, tk->dz(beamspot->position()) };
      const double errs[6] = { tk->ptError(), tk->etaError(), tk->phiError(), tk->dxyError(), tk->dxyError(), tk->dzError() };

      for (int i = 0; i < 6; ++i) {
        h_all_track_pars[i]->Fill(pars[i]);
        h_all_track_errs[i]->Fill(errs[i]);
      }

      h_all_track_sigmadxybs->Fill(sigmadxybs);
      h_all_track_sigmadxypv->Fill(sigmadxypv);
      h_all_track_nhits->Fill(nhits);
      h_all_track_npxhits->Fill(npxhits);
      h_all_track_nsthits->Fill(nsthits);
      h_all_track_npxlayers->Fill(npxlayers);
      h_all_track_nstlayers->Fill(nstlayers);

      const bool nm1[4] = {
        pt > min_track_pt,
        npxlayers >= min_track_npxlayers,
        nstlayers >= min_track_nstlayers,
        fabs(sigmadxybs) > min_track_sigmadxy
      };

      if (nm1[1] && nm1[2] && nm1[3]) h_seed_nm1_pt->Fill(pt);
      if (nm1[0] && nm1[2] && nm1[3]) h_seed_nm1_npxlayers->Fill(npxlayers);
      if (nm1[0] && nm1[1] && nm1[3]) h_seed_nm1_nstlayers->Fill(nstlayers);
      if (nm1[0] && nm1[1] && nm1[2]) h_seed_nm1_sigmadxybs->Fill(sigmadxybs);

      if (use) {
        for (int i = 0; i < 6; ++i) {
          h_seed_track_pars[i]->Fill(pars[i]);
          h_seed_track_errs[i]->Fill(errs[i]);
        }

	h_seed_track_sigmadxybs->Fill(sigmadxybs);
	h_seed_track_sigmadxypv->Fill(sigmadxypv);
        h_seed_track_nhits->Fill(nhits);
        h_seed_track_npxhits->Fill(npxhits);
        h_seed_track_nsthits->Fill(nsthits);
	h_seed_track_npxlayers->Fill(npxlayers);
	h_seed_track_nstlayers->Fill(nstlayers);
      }
    }
  }

  if (verbose)
    printf("n_all_tracks: %5lu   n_seed_tracks: %5lu\n", all_tracks->size(), seed_tracks->size());
  if (histos) {
    h_n_all_tracks->Fill(all_tracks->size());
    h_n_seed_tracks->Fill(seed_tracks->size());
  }

  const bool pass_min_n_seed_tracks = int(seed_tracks->size()) >= min_n_seed_tracks;

  event.put(std::move(all_tracks), "all");
  event.put(std::move(seed_tracks), "seed");
  event.put(std::move(seed_tracks_copy), "seed");

  return pass_min_n_seed_tracks;
}

DEFINE_FWK_MODULE(MFVVertexTracks);
