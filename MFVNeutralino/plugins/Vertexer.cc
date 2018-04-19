#include "TH2.h"
#include "TMath.h"
#include "TFitResult.h"
#include "CLHEP/Random/RandomEngine.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/RandomNumberGenerator.h"
#include "RecoVertex/ConfigurableVertexReco/interface/ConfigurableVertexReconstructor.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "TrackingTools/IPTools/interface/IPTools.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "JMTucker/Tools/interface/Bridges.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexerPairEff.h"

namespace {
  template <typename T>
  T mag(T x, T y) {
    return sqrt(x*x + y*y);
  }
  
  template <typename T>
  T mag(T x, T y, T z) {
    return sqrt(x*x + y*y + z*z);
  }
}

class MFVVertexer : public edm::EDProducer {
public:
  MFVVertexer(const edm::ParameterSet&);
  virtual void produce(edm::Event&, const edm::EventSetup&);

private:
  typedef std::set<reco::TrackRef> track_set;

  void finish(edm::Event&, const std::vector<reco::TransientTrack>&, std::unique_ptr<reco::VertexCollection>, std::unique_ptr<VertexerPairEffs>, const std::vector<std::pair<track_set, track_set>>&);

  template <typename T>
  void print_track_set(const T& ts) const {
    for (auto r : ts)
      printf(" %u", r.key());
  }

  template <typename T>
  void print_track_set(const T& ts, const reco::Vertex& v) const {
    for (auto r : ts)
      printf(" %u%s", r.key(), (v.trackWeight(r) < 0.5 ? "!" : ""));
  }

  void print_track_set(const reco::Vertex& v) const {
    for (auto r = v.tracks_begin(), re = v.tracks_end(); r != re; ++r)
      printf(" %lu%s", r->key(), (v.trackWeight(*r) < 0.5 ? "!" : ""));
  }

  bool is_track_subset(const track_set& a, const track_set& b) const {
    bool is_subset = true;
    const track_set& smaller = a.size() <= b.size() ? a : b;
    const track_set& bigger  = a.size() <= b.size() ? b : a;
    
    for (auto t : smaller)
      if (bigger.count(t) < 1) {
        is_subset = false;
        break;
      }

    return is_subset;
  }

  track_set vertex_track_set(const reco::Vertex& v, const double min_weight = 0.5) const {
    std::set<reco::TrackRef> result;

    for (auto it = v.tracks_begin(), ite = v.tracks_end(); it != ite; ++it) {
      const double w = v.trackWeight(*it);
      const bool use = w >= min_weight;
      assert(use);
      //if (verbose) ("trk #%2i pt %6.3f eta %6.3f phi %6.3f dxy %6.3f dz %6.3f w %5.3f  use? %i\n", int(it-v.tracks_begin()), (*it)->pt(), (*it)->eta(), (*it)->phi(), (*it)->dxy(), (*it)->dz(), w, use);
      if (use)
        result.insert(it->castTo<reco::TrackRef>());
    }

    return result;
  }

  Measurement1D vertex_dist(const reco::Vertex& v0, const reco::Vertex& v1) const {
    if (use_2d_vertex_dist)
      return vertex_dist_2d.distance(v0, v1);
    else
      return vertex_dist_3d.distance(v0, v1);
  }

  std::pair<bool, Measurement1D> track_dist(const reco::TransientTrack& t, const reco::Vertex& v) const {
    if (use_2d_track_dist)
      return IPTools::absoluteTransverseImpactParameter(t, v);
    else
      return IPTools::absoluteImpactParameter3D(t, v);
  }

  VertexDistanceXY vertex_dist_2d;
  VertexDistance3D vertex_dist_3d;
  std::unique_ptr<KalmanVertexFitter> kv_reco;
  std::unique_ptr<VertexReconstructor> av_reco;

  std::vector<TransientVertex> kv_reco_dropin(std::vector<reco::TransientTrack>& ttks) {
    if (ttks.size() < 2)
      return std::vector<TransientVertex>();
    std::vector<TransientVertex> v(1, kv_reco->vertex(ttks));
    if (v[0].normalisedChiSquared() > 5)
      return std::vector<TransientVertex>();
    return v;
  }

  const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
  const bool use_primary_vertices;
  const edm::EDGetTokenT<reco::VertexCollection> primary_vertices_token;
  const double min_jet_pt_for_ht;
  const bool disregard_event;
  const bool use_tracks;
  const edm::EDGetTokenT<reco::TrackCollection> track_token;
  const bool use_non_pv_tracks;
  const bool use_non_pvs_tracks;
  const bool use_pf_candidates;
  const edm::EDGetTokenT<reco::PFCandidateCollection> pf_candidate_token;
  const bool use_pf_jets;
  const edm::EDGetTokenT<reco::PFJetCollection> pf_jet_token;
  const bool use_pat_jets;
  const edm::EDGetTokenT<pat::JetCollection> pat_jet_token;
  const bool use_second_tracks;
  const edm::EDGetTokenT<reco::TrackCollection> second_track_token;
  const bool no_track_cuts;
  const double min_seed_jet_pt;
  const bool stlayers_v_eta;
  const double min_all_track_pt;
  const double min_all_track_dxy;
  const double min_all_track_sigmadxy;
  const double min_all_track_sigmadxypv;
  const int min_all_track_hit_r;
  const int min_all_track_nhits;
  const int min_all_track_npxhits;
  const int min_all_track_npxlayers;
  const int min_all_track_nstlayers;
  const double max_all_track_dxyerr;
  const double max_all_track_dxyipverr;
  const double max_all_track_d3dipverr;
  const double min_seed_track_pt;
  const double min_seed_track_dxy;
  const double min_seed_track_sigmadxy;
  const double min_seed_track_sigmadxypv;
  const int min_seed_track_hit_r;
  const int min_seed_track_nhits;
  const int min_seed_track_npxhits;
  const int min_seed_track_npxlayers;
  const int min_seed_track_nstlayers;
  const double max_seed_track_dxyerr;
  const double max_seed_track_dxyipverr;
  const double max_seed_track_d3dipverr;
  const int n_tracks_per_seed_vertex;
  const double max_seed_vertex_chi2;
  const bool use_2d_vertex_dist;
  const bool use_2d_track_dist;
  const double merge_anyway_dist;
  const double merge_anyway_sig;
  const double merge_shared_dist;
  const double merge_shared_sig;
  const double max_track_vertex_dist;
  const double max_track_vertex_sig;
  const double min_track_vertex_sig_to_remove;
  const bool remove_one_track_at_a_time;
  const bool jumble_tracks;
  const double remove_tracks_frac;
  const double remove_seed_tracks_frac;
  const bool histos;
  const bool scatterplots;
  const bool track_histos_only;
  const bool verbose;
  const std::string module_label;

  TH1F* h_n_all_tracks;
  TH1F* h_all_track_pars[6];
  TH1F* h_all_track_errs[6];
  TH2F* h_all_track_pars_v_pars[6][6];
  TH2F* h_all_track_errs_v_pars[6][6];
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
  TH2F* h_seed_track_pars_v_pars[6][6];
  TH2F* h_seed_track_errs_v_pars[6][6];
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
  TH1F* h_n_seed_vertices;
  TH1F* h_seed_vertex_track_weights;
  TH1F* h_seed_vertex_chi2;
  TH1F* h_seed_vertex_ndof;
  TH1F* h_seed_vertex_x;
  TH1F* h_seed_vertex_y;
  TH1F* h_seed_vertex_rho;
  TH1F* h_seed_vertex_phi;
  TH1F* h_seed_vertex_z;
  TH1F* h_seed_vertex_r;
  TH1F* h_seed_vertex_paird2d;
  TH1F* h_seed_vertex_pairdphi;
  TH1F* h_n_resets;
  TH1F* h_n_onetracks;
  TH1F* h_noshare_vertex_tkvtxdist;
  TH1F* h_noshare_vertex_tkvtxdisterr;
  TH1F* h_noshare_vertex_tkvtxdistsig;
  TH1F* h_n_noshare_vertices;
  TH1F* h_noshare_vertex_ntracks;
  TH1F* h_noshare_vertex_track_weights;
  TH1F* h_noshare_vertex_chi2;
  TH1F* h_noshare_vertex_ndof;
  TH1F* h_noshare_vertex_x;
  TH1F* h_noshare_vertex_y;
  TH1F* h_noshare_vertex_rho;
  TH1F* h_noshare_vertex_phi;
  TH1F* h_noshare_vertex_z;
  TH1F* h_noshare_vertex_r;
  TH1F* h_noshare_vertex_paird2d;
  TH1F* h_noshare_vertex_pairdphi;
  TH1F* h_noshare_track_multiplicity;
  TH1F* h_max_noshare_track_multiplicity;
  TH1F* h_n_output_vertices;

  struct track_cuts {
    const MFVVertexer& mv;
    const reco::Track& tk;
    const reco::BeamSpot& bs;
    const reco::Vertex* pv;
    const TransientTrackBuilder& tt_builder;

    double pt;
    double abs_eta;
    double dxybs;
    double dxypv;
    double dxyerr;
    double sigmadxybs;
    double sigmadxypv;
    int nhits;
    int npxhits;
    int npxlayers;
    int nstlayers;
    int min_r;
    
    track_cuts(const MFVVertexer* mv_, const reco::Track& tk_, const reco::BeamSpot& bs_, const reco::Vertex* pv_, const TransientTrackBuilder& tt)
      : mv(*mv_), tk(tk_), bs(bs_), pv(pv_), tt_builder(tt)
    {
      pt = tk.pt();
      abs_eta = fabs(tk.eta());
      dxybs = tk.dxy(bs);
      dxypv = pv ? tk.dxy(pv->position()) : 1e99;
      dxyerr = tk.dxyError();
      sigmadxybs = dxybs / dxyerr;
      sigmadxypv = dxypv / dxyerr;
      nhits = tk.hitPattern().numberOfValidHits(); // JMTBAD this is supposed to be strip hits...
      npxhits = tk.hitPattern().numberOfValidPixelHits();
      npxlayers = tk.hitPattern().pixelLayersWithMeasurement();
      nstlayers = tk.hitPattern().stripLayersWithMeasurement();
      min_r = jmt::hasValidHitInFirstPixelBarrel(tk) ? 1 : 2000000000;
    }

    // these are cheap
    bool use_ex(bool for_seed) const {
      if (mv.stlayers_v_eta) {
        if ((abs_eta < 2.0 && nstlayers < 6) || (abs_eta >= 2.0 && nstlayers < 7))
          return false;
      }

      if (for_seed) {
        return 
          npxlayers >= mv.min_seed_track_npxlayers && 
          nstlayers >= mv.min_seed_track_nstlayers && 
          (mv.min_seed_track_hit_r == 999 || min_r <= mv.min_seed_track_hit_r) &&
          pt > mv.min_seed_track_pt &&
          fabs(sigmadxybs) > mv.min_seed_track_sigmadxy &&
          fabs(dxybs) > mv.min_seed_track_dxy &&
          fabs(sigmadxypv) > mv.min_seed_track_sigmadxypv &&
          nhits >= mv.min_seed_track_nhits && 
          npxhits >= mv.min_seed_track_npxhits && 
          dxyerr < mv.max_seed_track_dxyerr;
      }
      else {
        return 
          npxlayers >= mv.min_all_track_npxlayers && 
          nstlayers >= mv.min_all_track_nstlayers && 
          (mv.min_all_track_hit_r == 999 || min_r <= mv.min_all_track_hit_r) &&
          pt > mv.min_all_track_pt &&
          fabs(sigmadxybs) > mv.min_all_track_sigmadxy &&
          fabs(dxybs) > mv.min_all_track_dxy &&
          fabs(sigmadxypv) > mv.min_all_track_sigmadxypv &&
          nhits >= mv.min_all_track_nhits && 
          npxhits >= mv.min_all_track_npxhits && 
          dxyerr < mv.max_all_track_dxyerr;
      }
    }

    bool use(bool for_seed) const {
      if (!use_ex(for_seed))
        return false;

      if (!pv)
        return true;

      const double max_dxyipverr = for_seed ? mv.max_seed_track_dxyipverr : mv.max_all_track_dxyipverr;
      const double max_d3dipverr = for_seed ? mv.max_seed_track_d3dipverr : mv.max_all_track_d3dipverr;

      if (max_dxyipverr <= 0 && max_d3dipverr <= 0)
        return true;

      reco::TransientTrack ttk = tt_builder.build(tk);

      if (max_dxyipverr > 0) {
        auto dxy_ipv = IPTools::absoluteTransverseImpactParameter(ttk, *pv);
        if (!dxy_ipv.first || dxy_ipv.second.error() >= max_dxyipverr)
          return false;
      }

      if (max_d3dipverr > 0) {
        auto d3d_ipv = IPTools::absoluteImpactParameter3D(ttk, *pv);
        if (!d3d_ipv.first || d3d_ipv.second.error() >= max_d3dipverr)
          return false;
      }
      
      return true;
    }
  };
};

MFVVertexer::MFVVertexer(const edm::ParameterSet& cfg)
  : kv_reco(new KalmanVertexFitter(cfg.getParameter<edm::ParameterSet>("kvr_params"), cfg.getParameter<edm::ParameterSet>("kvr_params").getParameter<bool>("doSmoothing"))),
    av_reco(new ConfigurableVertexReconstructor(cfg.getParameter<edm::ParameterSet>("avr_params"))),
    beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot_src"))),
    use_primary_vertices(cfg.getParameter<edm::InputTag>("primary_vertices_src").label() != ""),
    primary_vertices_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("primary_vertices_src"))),
    min_jet_pt_for_ht(cfg.getParameter<double>("min_jet_pt_for_ht")),
    disregard_event(cfg.getParameter<bool>("disregard_event")),
    use_tracks(cfg.getParameter<bool>("use_tracks")),
    track_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("track_src"))),
    use_non_pv_tracks(cfg.getParameter<bool>("use_non_pv_tracks")),
    use_non_pvs_tracks(cfg.getParameter<bool>("use_non_pvs_tracks")),
    use_pf_candidates(cfg.getParameter<bool>("use_pf_candidates")),
    pf_candidate_token(consumes<reco::PFCandidateCollection>(cfg.getParameter<edm::InputTag>("pf_candidate_src"))),
    use_pf_jets(cfg.getParameter<bool>("use_pf_jets")),
    pf_jet_token(consumes<reco::PFJetCollection>(cfg.getParameter<edm::InputTag>("pf_jet_src"))),
    use_pat_jets(cfg.getParameter<bool>("use_pat_jets")),
    pat_jet_token(consumes<pat::JetCollection>(cfg.getParameter<edm::InputTag>("pat_jet_src"))),
    use_second_tracks(cfg.getParameter<bool>("use_second_tracks")),
    second_track_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("second_track_src"))),
    no_track_cuts(cfg.getParameter<bool>("no_track_cuts")),
    min_seed_jet_pt(cfg.getParameter<double>("min_seed_jet_pt")),
    stlayers_v_eta(cfg.getParameter<bool>("stlayers_v_eta")),
    min_all_track_pt(cfg.getParameter<double>("min_all_track_pt")),
    min_all_track_dxy(cfg.getParameter<double>("min_all_track_dxy")),
    min_all_track_sigmadxy(cfg.getParameter<double>("min_all_track_sigmadxy")),
    min_all_track_sigmadxypv(cfg.getParameter<double>("min_all_track_sigmadxypv")),
    min_all_track_hit_r(cfg.getParameter<int>("min_all_track_hit_r")),
    min_all_track_nhits(cfg.getParameter<int>("min_all_track_nhits")),
    min_all_track_npxhits(cfg.getParameter<int>("min_all_track_npxhits")),
    min_all_track_npxlayers(cfg.getParameter<int>("min_all_track_npxlayers")),
    min_all_track_nstlayers(cfg.getParameter<int>("min_all_track_nstlayers")),
    max_all_track_dxyerr(cfg.getParameter<double>("max_all_track_dxyerr")),
    max_all_track_dxyipverr(cfg.getParameter<double>("max_all_track_dxyipverr")),
    max_all_track_d3dipverr(cfg.getParameter<double>("max_all_track_d3dipverr")),
    min_seed_track_pt(cfg.getParameter<double>("min_seed_track_pt")),
    min_seed_track_dxy(cfg.getParameter<double>("min_seed_track_dxy")),
    min_seed_track_sigmadxy(cfg.getParameter<double>("min_seed_track_sigmadxy")),
    min_seed_track_sigmadxypv(cfg.getParameter<double>("min_seed_track_sigmadxypv")),
    min_seed_track_hit_r(cfg.getParameter<int>("min_seed_track_hit_r")),
    min_seed_track_nhits(cfg.getParameter<int>("min_seed_track_nhits")),
    min_seed_track_npxhits(cfg.getParameter<int>("min_seed_track_npxhits")),
    min_seed_track_npxlayers(cfg.getParameter<int>("min_seed_track_npxlayers")),
    min_seed_track_nstlayers(cfg.getParameter<int>("min_seed_track_nstlayers")),
    max_seed_track_dxyerr(cfg.getParameter<double>("max_seed_track_dxyerr")),
    max_seed_track_dxyipverr(cfg.getParameter<double>("max_seed_track_dxyipverr")),
    max_seed_track_d3dipverr(cfg.getParameter<double>("max_seed_track_d3dipverr")),
    n_tracks_per_seed_vertex(cfg.getParameter<int>("n_tracks_per_seed_vertex")),
    max_seed_vertex_chi2(cfg.getParameter<double>("max_seed_vertex_chi2")),
    use_2d_vertex_dist(cfg.getParameter<bool>("use_2d_vertex_dist")),
    use_2d_track_dist(cfg.getParameter<bool>("use_2d_track_dist")),
    merge_anyway_dist(cfg.getParameter<double>("merge_anyway_dist")),
    merge_anyway_sig(cfg.getParameter<double>("merge_anyway_sig")),
    merge_shared_dist(cfg.getParameter<double>("merge_shared_dist")),
    merge_shared_sig(cfg.getParameter<double>("merge_shared_sig")),
    max_track_vertex_dist(cfg.getParameter<double>("max_track_vertex_dist")),
    max_track_vertex_sig(cfg.getParameter<double>("max_track_vertex_sig")),
    min_track_vertex_sig_to_remove(cfg.getParameter<double>("min_track_vertex_sig_to_remove")),
    remove_one_track_at_a_time(cfg.getParameter<bool>("remove_one_track_at_a_time")),
    jumble_tracks(cfg.getParameter<bool>("jumble_tracks")),
    remove_tracks_frac(cfg.getParameter<double>("remove_tracks_frac")),
    remove_seed_tracks_frac(cfg.getParameter<double>("remove_seed_tracks_frac")),
    histos(cfg.getUntrackedParameter<bool>("histos", false)),
    scatterplots(cfg.getUntrackedParameter<bool>("scatterplots", false)),
    track_histos_only(cfg.getUntrackedParameter<bool>("track_histos_only", false)),
    verbose(cfg.getUntrackedParameter<bool>("verbose", false)),
    module_label(cfg.getParameter<std::string>("@module_label"))
{
  if ((min_all_track_hit_r != 1 && min_all_track_hit_r != 999) || (min_seed_track_hit_r != 1 && min_seed_track_hit_r != 999))
    throw cms::Exception("MFVVertexer") << "hit_r cuts may only be 1";

  if (use_tracks + use_non_pv_tracks + use_non_pvs_tracks + use_pf_candidates + use_pf_jets + use_pat_jets != 1)
    throw cms::Exception("MFVVertexer") << "must enable exactly one of use_tracks/use_non_pv_tracks/use_non_pvs_tracks/pf_candidates/pf_jets/pat_jets";

  if ((use_non_pv_tracks || use_non_pvs_tracks) && !use_primary_vertices)
    throw cms::Exception("MFVVertexer", "can't use_non_pv_tracks || use_non_pvs_tracks if !use_primary_vertices");

  if (n_tracks_per_seed_vertex < 2 || n_tracks_per_seed_vertex > 5)
    throw cms::Exception("MFVVertexer", "n_tracks_per_seed_vertex must be one of 2,3,4,5");

  edm::Service<edm::RandomNumberGenerator> rng;
  if ((jumble_tracks || remove_tracks_frac > 0 || remove_seed_tracks_frac > 0) && !rng.isAvailable())
    throw cms::Exception("Vertexer") << "RandomNumberGeneratorService not available for jumbling or removing tracks!\n";

  produces<reco::VertexCollection>();
  produces<VertexerPairEffs>();
  produces<reco::TrackCollection>("seed");
  produces<reco::TrackCollection>("inVertices");

  if (histos) {
    edm::Service<TFileService> fs;

    h_n_all_tracks  = fs->make<TH1F>("h_n_all_tracks",  "", 40, 0, 2000);
    h_n_seed_tracks = fs->make<TH1F>("h_n_seed_tracks", "", 50, 0,  200);

    const char* par_names[6] = {"pt", "eta", "phi", "dxybs", "dxypv", "dz"};
    const int par_nbins[6] = {  50, 50, 50, 100, 100, 80 };
    const double par_lo[6] = {   0, -2.5, -3.15, -0.2, -0.2, -20 };
    const double par_hi[6] = {  10,  2.5,  3.15,  0.2,  0.2,  20 };
    const double err_lo[6] = { 0 };
    const double err_hi[6] = { 0.15, 0.01, 0.01, 0.2, 0.2, 0.4 };
    for (int i = 0; i < 6; ++i)
      h_all_track_pars[i] = fs->make<TH1F>(TString::Format("h_all_track_%s",    par_names[i]), "", par_nbins[i], par_lo[i], par_hi[i]);
    for (int i = 0; i < 6; ++i)
      h_all_track_errs[i] = fs->make<TH1F>(TString::Format("h_all_track_err%s", par_names[i]), "", par_nbins[i], err_lo[i], err_hi[i]);
    if (scatterplots) {
      for (int i = 0; i < 6; ++i)
        for (int j = i+1; j < 6; ++j)
          h_all_track_pars_v_pars[i][j] = fs->make<TH2F>(TString::Format("h_all_track_%s_v_%s", par_names[j], par_names[i]), "", par_nbins[i], par_lo[i], par_hi[i], par_nbins[j], par_lo[j], par_hi[j]);
      for (int i = 0; i < 6; ++i)
        for (int j = 0; j < 6; ++j)
          h_all_track_errs_v_pars[i][j] = fs->make<TH2F>(TString::Format("h_all_track_err%s_v_%s", par_names[j], par_names[i]), "", par_nbins[i], par_lo[i], par_hi[i], par_nbins[j], err_lo[j], err_hi[j]);
    }

    h_all_track_sigmadxybs           = fs->make<TH1F>("h_all_track_sigmadxybs",           "", 40, -10,     10);
    h_all_track_sigmadxypv           = fs->make<TH1F>("h_all_track_sigmadxypv",           "", 40, -10,     10);
    h_all_track_nhits                = fs->make<TH1F>("h_all_track_nhits",                "",  40,   0,     40);
    h_all_track_npxhits              = fs->make<TH1F>("h_all_track_npxhits",              "",  12,   0,     12);
    h_all_track_nsthits              = fs->make<TH1F>("h_all_track_nsthits",              "",  28,   0,     28);
    h_all_track_npxlayers            = fs->make<TH1F>("h_all_track_npxlayers",            "",  10,   0,     10);
    h_all_track_nstlayers            = fs->make<TH1F>("h_all_track_nstlayers",            "",  30,   0,     30);

    for (int i = 0; i < 6; ++i)
      h_seed_track_pars[i] = fs->make<TH1F>(TString::Format("h_seed_track_%s",    par_names[i]), "", par_nbins[i], par_lo[i], par_hi[i]);
    for (int i = 0; i < 6; ++i)
      h_seed_track_errs[i] = fs->make<TH1F>(TString::Format("h_seed_track_err%s", par_names[i]), "", par_nbins[i], err_lo[i], err_hi[i]);
    if (scatterplots) {
      for (int i = 0; i < 6; ++i)
        for (int j = i+1; j < 6; ++j)
          h_seed_track_pars_v_pars[i][j] = fs->make<TH2F>(TString::Format("h_seed_track_%s_v_%s", par_names[j], par_names[i]), "", par_nbins[i], par_lo[i], par_hi[i], par_nbins[j], par_lo[j], par_hi[j]);
      for (int i = 0; i < 6; ++i)
        for (int j = 0; j < 6; ++j)
          h_seed_track_errs_v_pars[i][j] = fs->make<TH2F>(TString::Format("h_seed_track_err%s_v_%s", par_names[j], par_names[i]), "", par_nbins[i], par_lo[i], par_hi[i], par_nbins[j], err_lo[j], err_hi[j]);
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

    h_n_seed_vertices                = fs->make<TH1F>("h_n_seed_vertices",                "",  50,   0,    200);
    h_seed_vertex_track_weights      = fs->make<TH1F>("h_seed_vertex_track_weights",      "",  21,   0,      1.05);
    h_seed_vertex_chi2               = fs->make<TH1F>("h_seed_vertex_chi2",               "",  20,   0, max_seed_vertex_chi2);
    h_seed_vertex_ndof               = fs->make<TH1F>("h_seed_vertex_ndof",               "",  10,   0,     20);
    h_seed_vertex_x                  = fs->make<TH1F>("h_seed_vertex_x",                  "", 100,  -1,      1);
    h_seed_vertex_y                  = fs->make<TH1F>("h_seed_vertex_y",                  "", 100,  -1,      1);
    h_seed_vertex_rho                = fs->make<TH1F>("h_seed_vertex_rho",                "", 100,   0,      2);
    h_seed_vertex_phi                = fs->make<TH1F>("h_seed_vertex_phi",                "",  50,  -3.15,   3.15);
    h_seed_vertex_z                  = fs->make<TH1F>("h_seed_vertex_z",                  "",  40, -20,     20);
    h_seed_vertex_r                  = fs->make<TH1F>("h_seed_vertex_r",                  "", 100,   0,      2);
    h_seed_vertex_paird2d            = fs->make<TH1F>("h_seed_vertex_paird2d",            "", 100,   0,      0.2);
    h_seed_vertex_pairdphi           = fs->make<TH1F>("h_seed_vertex_pairdphi",           "", 100,  -3.14,   3.14);

    h_n_resets                       = fs->make<TH1F>("h_n_resets",                       "", 50,   0,   500);
    h_n_onetracks                    = fs->make<TH1F>("h_n_onetracks",                    "",  5,   0,     5);

    h_n_noshare_vertices             = fs->make<TH1F>("h_n_noshare_vertices",             "", 50,   0,    50);
    h_noshare_vertex_tkvtxdist       = fs->make<TH1F>("h_noshare_vertex_tkvtxdist",       "", 100,  0,   0.1);
    h_noshare_vertex_tkvtxdisterr    = fs->make<TH1F>("h_noshare_vertex_tkvtxdisterr",    "", 100,  0,   0.1);
    h_noshare_vertex_tkvtxdistsig    = fs->make<TH1F>("h_noshare_vertex_tkvtxdistsig",    "", 100,  0,     6);
    h_noshare_vertex_ntracks         = fs->make<TH1F>("h_noshare_vertex_ntracks",         "",  30,  0, 30);
    h_noshare_vertex_track_weights   = fs->make<TH1F>("h_noshare_vertex_track_weights",   "",  21,   0,      1.05);
    h_noshare_vertex_chi2            = fs->make<TH1F>("h_noshare_vertex_chi2",            "", 20,   0, max_seed_vertex_chi2);
    h_noshare_vertex_ndof            = fs->make<TH1F>("h_noshare_vertex_ndof",            "", 10,   0,     20);
    h_noshare_vertex_x               = fs->make<TH1F>("h_noshare_vertex_x",               "", 100,  -1,      1);
    h_noshare_vertex_y               = fs->make<TH1F>("h_noshare_vertex_y",               "", 100,  -1,      1);
    h_noshare_vertex_rho             = fs->make<TH1F>("h_noshare_vertex_rho",             "", 100,   0,      2);
    h_noshare_vertex_phi             = fs->make<TH1F>("h_noshare_vertex_phi",             "", 50,  -3.15,   3.15);
    h_noshare_vertex_z               = fs->make<TH1F>("h_noshare_vertex_z",               "", 40, -20,     20);
    h_noshare_vertex_r               = fs->make<TH1F>("h_noshare_vertex_r",               "", 100,   0,      2);
    h_noshare_vertex_paird2d         = fs->make<TH1F>("h_noshare_vertex_paird2d",            "", 100,   0,      0.2);
    h_noshare_vertex_pairdphi        = fs->make<TH1F>("h_noshare_vertex_pairdphi",           "", 100,  -3.15,   3.15);
    h_noshare_track_multiplicity     = fs->make<TH1F>("h_noshare_track_multiplicity",     "",  40,   0,     40);
    h_max_noshare_track_multiplicity = fs->make<TH1F>("h_max_noshare_track_multiplicity", "",  40,   0,     40);
    h_n_output_vertices           = fs->make<TH1F>("h_n_output_vertices",           "", 50, 0, 50);
  }
}

void MFVVertexer::finish(edm::Event& event, const std::vector<reco::TransientTrack>& seed_tracks, std::unique_ptr<reco::VertexCollection> vertices, std::unique_ptr<VertexerPairEffs> vpeffs, const std::vector<std::pair<track_set, track_set>>& vpeffs_tracks) {
  std::unique_ptr<reco::TrackCollection> tracks_seed      (new reco::TrackCollection);
  std::unique_ptr<reco::TrackCollection> tracks_inVertices(new reco::TrackCollection);

  if (verbose) printf("finish:\nseed tracks:\n");

  std::map<std::pair<unsigned, unsigned>, unsigned char> seed_track_ref_map;
  assert(seed_tracks.size() <= 255);
  unsigned char itk = 0;
  for (const reco::TransientTrack& ttk : seed_tracks) {
    tracks_seed->push_back(ttk.track());
    const reco::TrackBaseRef& tk(ttk.trackBaseRef());
    seed_track_ref_map[std::make_pair(tk.id().id(), tk.key())] = itk++;

    if (verbose) printf("id: %i key: %lu pt: %f\n", tk.id().id(), tk.key(), tk->pt());
  }

  assert(vpeffs->size() == vpeffs_tracks.size());
  for (size_t i = 0, ie = vpeffs->size(); i < ie; ++i) {
    for (auto tk : vpeffs_tracks[i].first)  (*vpeffs)[i].tracks_push_back(0, seed_track_ref_map[std::make_pair(tk.id().id(), tk.key())]);
    for (auto tk : vpeffs_tracks[i].second) (*vpeffs)[i].tracks_push_back(1, seed_track_ref_map[std::make_pair(tk.id().id(), tk.key())]);
  }

  if (verbose) printf("vertices:\n");

  for (const reco::Vertex& v : *vertices) {
    if (verbose) printf("x: %f y %f z %f\n", v.x(), v.y(), v.z());
    for (auto it = v.tracks_begin(), ite = v.tracks_end(); it != ite; ++it) {
      reco::TrackRef tk = it->castTo<reco::TrackRef>();
      if (verbose) printf("id: %i key: %u pt: %f\n", tk.id().id(), tk.key(), tk->pt());
      tracks_inVertices->push_back(*tk);
    }
  }

  if (verbose)
    printf("n_output_vertices: %lu\n", vertices->size());
  if (histos)
    h_n_output_vertices->Fill(vertices->size());

  event.put(std::move(vertices));
  event.put(std::move(vpeffs));
  event.put(std::move(tracks_seed),       "seed");
  event.put(std::move(tracks_inVertices), "inVertices");
}

void MFVVertexer::produce(edm::Event& event, const edm::EventSetup& setup) {
  if (verbose) {
    printf("------------------------------------------------------------------------\n");
    printf("MFVVertexer %s: run %u, lumi %u, event ", module_label.c_str(), event.id().run(), event.luminosityBlock());
    std::cout << event.id().event() << "\n";
  }

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByToken(beamspot_token, beamspot);
  const double bs_x = beamspot->position().x();
  const double bs_y = beamspot->position().y();
  const double bs_z = beamspot->position().z();

  edm::Handle<reco::VertexCollection> primary_vertices;
  const reco::Vertex* primary_vertex = 0;
  if (use_primary_vertices) {
    event.getByToken(primary_vertices_token, primary_vertices);
    if (primary_vertices->size())
      primary_vertex = &primary_vertices->at(0);
  }

  //////////////////////////////////////////////////////////////////////
  // The tracks to be used. Will be filled from a track collection or
  // from raw-PF/PF2PAT jet constituents with cuts on pt/nhits/dxy.
  //////////////////////////////////////////////////////////////////////

  edm::ESHandle<TransientTrackBuilder> tt_builder;

  setup.get<TransientTrackRecord>().get("TransientTrackBuilder", tt_builder);

  std::vector<reco::TrackRef> all_tracks;
  std::vector<reco::TransientTrack> seed_tracks;
  std::vector<bool> seed_track_is_second;
  std::map<reco::TrackRef, size_t> seed_track_ref_map;

  if (!disregard_event) {
    if (use_tracks) {
      edm::Handle<reco::TrackCollection> tracks;
      event.getByToken(track_token, tracks);
      for (size_t i = 0, ie = tracks->size(); i < ie; ++i)
        all_tracks.push_back(reco::TrackRef(tracks, i));
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
      event.getByToken(track_token, tracks);
      for (size_t i = 0, ie = tracks->size(); i < ie; ++i) {
        reco::TrackRef tkref(tracks, i);
        bool ok = true;
        for (const auto& pv_use : tracks_in_pvs[tkref])
          if (use_non_pvs_tracks || (use_non_pv_tracks && pv_use.first == 0)) {
            ok = false;
            break;
          }

        if (ok)
          all_tracks.push_back(tkref);
      }
    }
    else if (use_pf_candidates) {
      edm::Handle<reco::PFCandidateCollection> pf_candidates;
      event.getByToken(pf_candidate_token, pf_candidates);

      for (const reco::PFCandidate& cand : *pf_candidates) {
        reco::TrackRef tkref = cand.trackRef();
        if (tkref.isNonnull())
          all_tracks.push_back(tkref);
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
            all_tracks.push_back(tk);
        }
      }
    }
    else if (use_pat_jets) {
      edm::Handle<pat::JetCollection> jets;
      event.getByToken(pat_jet_token, jets);
      for (const pat::Jet& jet : *jets) {
        if (jet.pt() > min_seed_jet_pt) { // assume rest of id above already applied at tuple time
          for (const reco::PFCandidatePtr& pfcand : jet.getPFConstituents()) {
            const reco::TrackRef& tk = pfcand->trackRef();
            if (tk.isNonnull())
              all_tracks.push_back(tk);
          }
        }
      }
    }
  }

  const size_t second_tracks_start_at = all_tracks.size(); // no cuts are applied to second_tracks since the hits cuts are hard to do without having hit info stored
  
  if (use_second_tracks) {
    edm::Handle<reco::TrackCollection> tracks;
    event.getByToken(second_track_token, tracks);
    if (verbose) printf("second tracks start at %lu and there are %lu of them\n", second_tracks_start_at, tracks->size());
    for (size_t i = 0, ie = tracks->size(); i < ie; ++i)
      all_tracks.push_back(reco::TrackRef(tracks, i));
  }

  if (jumble_tracks) {
    assert(!use_second_tracks); // would break second_tracks_start_at cut skipping logic
    edm::Service<edm::RandomNumberGenerator> rng;
    CLHEP::HepRandomEngine& rng_engine = rng->getEngine(event.streamID());
    auto random_converter = [&](size_t n) { return size_t(rng_engine.flat() * n); };
    std::random_shuffle(all_tracks.begin(), all_tracks.end(), random_converter);
  }

  for (size_t i = 0, ie = all_tracks.size(); i < ie; ++i) {
    const reco::TrackRef& tk = all_tracks[i];
    const track_cuts tc(this, *tk, *beamspot, primary_vertex, *tt_builder);
    const bool is_second_track = i >= second_tracks_start_at;
    bool use = no_track_cuts || is_second_track || tc.use(false);

    if (use && remove_tracks_frac > 0) {
      edm::Service<edm::RandomNumberGenerator> rng;
      CLHEP::HepRandomEngine& rng_engine = rng->getEngine(event.streamID());
      if (rng_engine.flat() < remove_tracks_frac)
        use = false;
    }

    if (use) {
      seed_tracks.push_back(tt_builder->build(tk));
      seed_track_is_second.push_back(is_second_track);
      seed_track_ref_map[tk] = seed_tracks.size() - 1;
    }

    if (verbose) {
      printf("track %5lu: pt: %7.3f dxy: %7.3f nhits %3i ", i, tc.pt, tc.dxybs, tc.nhits);
      if (use)
        printf(" selected for seed(false)! (#%lu)", seed_tracks.size()-1);
      printf("\n");
    }        

    if (histos) {
      const double pars[6] = {tc.pt, tk->eta(), tk->phi(), tc.dxybs, tc.dxypv, tk->dz(beamspot->position()) };
      const double errs[6] = { tk->ptError(), tk->etaError(), tk->phiError(), tk->dxyError(), tk->dxyError(), tk->dzError() };

      for (int i = 0; i < 6; ++i) {
        h_all_track_pars[i]->Fill(pars[i]);
        h_all_track_errs[i]->Fill(errs[i]);
        if (scatterplots) {
          for (int j = 0; j < 6; ++j) {
            if (j >= i+1)
              h_all_track_pars_v_pars[i][j]->Fill(pars[i], pars[j]);
            h_all_track_errs_v_pars[i][j]->Fill(pars[i], errs[j]);
          }
        }
      }
      
      h_all_track_sigmadxybs->Fill(tc.sigmadxybs);
      h_all_track_sigmadxypv->Fill(tc.sigmadxypv);
      h_all_track_nhits->Fill(tc.nhits);
      h_all_track_npxhits->Fill(tk->hitPattern().numberOfValidPixelHits());
      h_all_track_nsthits->Fill(tk->hitPattern().numberOfValidStripHits());
      h_all_track_npxlayers->Fill(tk->hitPattern().pixelLayersWithMeasurement());
      h_all_track_nstlayers->Fill(tk->hitPattern().stripLayersWithMeasurement());

      const bool nm1[4] = {
        tc.pt > min_all_track_pt,
        tc.npxlayers >= min_all_track_npxlayers,
        tc.nstlayers >= min_all_track_nstlayers,
        fabs(tc.sigmadxybs) > min_seed_track_sigmadxy
      };

      if (nm1[1] && nm1[2] && nm1[3]) h_seed_nm1_pt->Fill(tc.pt);
      if (nm1[0] && nm1[2] && nm1[3]) h_seed_nm1_npxlayers->Fill(tc.npxlayers);
      if (nm1[0] && nm1[1] && nm1[3]) h_seed_nm1_nstlayers->Fill(tc.nstlayers);
      if (nm1[0] && nm1[1] && nm1[2]) h_seed_nm1_sigmadxybs->Fill(tc.sigmadxybs);

      if (use) {
        for (int i = 0; i < 6; ++i) {
          h_seed_track_pars[i]->Fill(pars[i]);
          h_seed_track_errs[i]->Fill(errs[i]);
          if (scatterplots) {
            for (int j = 0; j < 6; ++j) {
              if (j >= i+1)
                h_seed_track_pars_v_pars[i][j]->Fill(pars[i], pars[j]);
              h_seed_track_errs_v_pars[i][j]->Fill(pars[i], errs[j]);
            }
          }
        }

	h_seed_track_sigmadxybs->Fill(tc.sigmadxybs);
	h_seed_track_sigmadxypv->Fill(tc.sigmadxypv);
        h_seed_track_nhits->Fill(tc.nhits);
        h_seed_track_npxhits->Fill(tk->hitPattern().numberOfValidPixelHits());
        h_seed_track_nsthits->Fill(tk->hitPattern().numberOfValidStripHits());
	h_seed_track_npxlayers->Fill(tk->hitPattern().pixelLayersWithMeasurement());
	h_seed_track_nstlayers->Fill(tk->hitPattern().stripLayersWithMeasurement());
      }
    }
  }

  const size_t ntk = seed_tracks.size();

  if (verbose)
    printf("n_all_tracks: %5lu   n_seed_tracks: %5lu\n", all_tracks.size(), ntk);
  if (histos) {
    h_n_all_tracks->Fill(all_tracks.size());
    h_n_seed_tracks->Fill(ntk);
  }

  //////////////////////////////////////////////////////////////////////
  // Form seed vertices from all pairs of tracks whose vertex fit
  // passes cuts.
  //////////////////////////////////////////////////////////////////////

  std::unique_ptr<reco::VertexCollection> vertices(new reco::VertexCollection);
  std::unique_ptr<VertexerPairEffs> vpeffs(new VertexerPairEffs);
  std::vector<std::pair<track_set, track_set>> vpeffs_tracks;

  if (ntk == 0 || track_histos_only) {
    if (verbose) {
      if (ntk == 0)
        printf("no seed tracks");
      else
        printf("track histos only");
      printf(" -> putting empty vertex collection into event\n");
    }
    finish(event, seed_tracks, std::move(vertices), std::move(vpeffs), vpeffs_tracks);
    return;
  }

  std::vector<bool> seed_use(ntk, 0);
  if (verbose) printf("seed_use:");
  for (size_t itk = 0; itk < ntk; ++itk) {
    const track_cuts itk_tc(this, seed_tracks[itk].track(), *beamspot, primary_vertex, *tt_builder);
    seed_use[itk] = no_track_cuts || seed_track_is_second[itk] || itk_tc.use(true);
    if (seed_use[itk] && remove_seed_tracks_frac > 0) {
      edm::Service<edm::RandomNumberGenerator> rng;
      CLHEP::HepRandomEngine& rng_engine = rng->getEngine(event.streamID());
      if (rng_engine.flat() < remove_seed_tracks_frac)
        seed_use[itk] = false;
    }
    if (verbose && seed_use[itk]) printf(" %lu", itk);
  }
  if (verbose) printf("\n");

  std::vector<size_t> itks(n_tracks_per_seed_vertex, 0);

  auto try_seed_vertex = [&]() {
    std::vector<reco::TransientTrack> ttks(n_tracks_per_seed_vertex);
    for (int i = 0; i < n_tracks_per_seed_vertex; ++i)
      ttks[i] = seed_tracks[itks[i]];

    TransientVertex seed_vertex = kv_reco->vertex(ttks);
    if (seed_vertex.isValid() && seed_vertex.normalisedChiSquared() < max_seed_vertex_chi2) {
      vertices->push_back(reco::Vertex(seed_vertex));

      if (verbose || histos) {
        const reco::Vertex& v = vertices->back();
        const double vchi2 = v.normalizedChi2();
        const double vndof = v.ndof();
        const double vx = v.position().x() - bs_x;
        const double vy = v.position().y() - bs_y;
        const double vz = v.position().z() - bs_z;
        const double phi = atan2(vy, vx);
        const double rho = mag(vx, vy);
        const double r = mag(vx, vy, vz);
        if (verbose) {
          printf("from tracks");
          for (auto itk : itks)
            printf(" %lu", itk);
          printf(": vertex #%3lu: chi2/dof: %7.3f dof: %7.3f pos: <%7.3f, %7.3f, %7.3f>  rho: %7.3f  phi: %7.3f  r: %7.3f\n", vertices->size()-1, vchi2, vndof, vx, vy, vz, rho, phi, r);
        }
        if (histos) {
          for (auto it = v.tracks_begin(), ite = v.tracks_end(); it != ite; ++it)
            h_seed_vertex_track_weights->Fill(v.trackWeight(*it));
          h_seed_vertex_chi2->Fill(vchi2);
          h_seed_vertex_ndof->Fill(vndof);
          h_seed_vertex_x->Fill(vx);
          h_seed_vertex_y->Fill(vy);
          h_seed_vertex_rho->Fill(rho);
          h_seed_vertex_phi->Fill(phi);
          h_seed_vertex_z->Fill(vz);
          h_seed_vertex_r->Fill(r);
        }
      }
    }
  };

  // ha
  for (size_t itk = 0; itk < ntk; ++itk) {
    if (!seed_use[itk]) continue;
    itks[0] = itk;
    for (size_t jtk = itk+1; jtk < ntk; ++jtk) {
      if (!seed_use[jtk]) continue;
      itks[1] = jtk;
      if (n_tracks_per_seed_vertex == 2) { try_seed_vertex(); continue; }
      for (size_t ktk = jtk+1; ktk < ntk; ++ktk) {
        if (!seed_use[ktk]) continue;
        itks[2] = ktk;
        if (n_tracks_per_seed_vertex == 3) { try_seed_vertex(); continue; }
        for (size_t ltk = ktk+1; ltk < ntk; ++ltk) {
          if (!seed_use[ltk]) continue;
          itks[3] = ltk;
          if (n_tracks_per_seed_vertex == 4) { try_seed_vertex(); continue; }
          for (size_t mtk = ltk+1; mtk < ntk; ++mtk) {
            if (!seed_use[mtk]) continue;
            itks[4] = mtk;
            try_seed_vertex();
          }
        }
      }
    }
  }

  if (histos) {
    for (std::vector<reco::Vertex>::const_iterator v0 = vertices->begin(); v0 != vertices->end(); ++v0) {
      const double v0x = v0->position().x() - bs_x;
      const double v0y = v0->position().y() - bs_y;
      const double phi0 = atan2(v0y, v0x);
      for (std::vector<reco::Vertex>::const_iterator v1 = v0 + 1; v1 != vertices->end(); ++v1) {
        const double v1x = v1->position().x() - bs_x;
        const double v1y = v1->position().y() - bs_y;
        const double phi1 = atan2(v1y, v1x);
        h_seed_vertex_paird2d ->Fill(mag(v0x - v1x, v0y - v1y));
        h_seed_vertex_pairdphi->Fill(reco::deltaPhi(phi0, phi1));
      }
    }
  }

  if (verbose)
    printf("n_seed_vertices: %lu\n", vertices->size());
  if (histos)
    h_n_seed_vertices->Fill(vertices->size());

  //////////////////////////////////////////////////////////////////////
  // Take care of track sharing. If a track is in two vertices, and
  // the vertices are "close", refit the tracks from the two together
  // as one vertex. If the vertices are not close, keep the track in
  // the vertex to which it is "closer".
  //////////////////////////////////////////////////////////////////////

  if (verbose)
    printf("fun time!\n");

  track_set discarded_tracks;
  int n_resets = 0;
  int n_onetracks = 0;
  std::vector<reco::Vertex>::iterator v[2];
  size_t ivtx[2];
  for (v[0] = vertices->begin(); v[0] != vertices->end(); ++v[0]) {
    track_set tracks[2];
    ivtx[0] = v[0] - vertices->begin();
    tracks[0] = vertex_track_set(*v[0]);

    if (tracks[0].size() < 2) {
      if (verbose)
        printf("track-sharing: vertex-0 #%lu is down to one track, junking it\n", ivtx[0]);
      v[0] = vertices->erase(v[0]) - 1;
      ++n_onetracks;
      continue;
    }

    bool duplicate = false;
    bool merge = false;
    bool refit = false;
    track_set tracks_to_remove_in_refit[2];
    VertexerPairEff* vpeff = 0;
    const size_t max_vpeffs_size = 20000; // enough for 200 vertices to share tracks

    for (v[1] = v[0] + 1; v[1] != vertices->end(); ++v[1]) {
      ivtx[1] = v[1] - vertices->begin();
      tracks[1] = vertex_track_set(*v[1]);

      if (tracks[1].size() < 2) {
        if (verbose)
          printf("track-sharing: vertex-1 #%lu is down to one track, junking it\n", ivtx[1]);
        v[1] = vertices->erase(v[1]) - 1;
        ++n_onetracks;
        continue;
      }

      if (verbose) {
        printf("track-sharing: # vertices = %lu. considering vertices #%lu (chi2/dof %.3f prob %.2e, track set", vertices->size(), ivtx[0], v[0]->chi2()/v[0]->ndof(), TMath::Prob(v[0]->chi2(), int(v[0]->ndof())));
        print_track_set(tracks[0], *v[0]);
        printf(") and #%lu (chi2/dof %.3f prob %.2e, track set", ivtx[1], v[1]->chi2()/v[1]->ndof(), TMath::Prob(v[1]->chi2(), int(v[1]->ndof())));
        print_track_set(tracks[1], *v[1]);
        printf("):\n");
      }

      if (is_track_subset(tracks[0], tracks[1])) {
        if (verbose)
          printf("   subset/duplicate vertices %lu and %lu, erasing second and starting over\n", ivtx[0], ivtx[1]);
        duplicate = true;
        break;
      }

      if (vpeffs->size() < max_vpeffs_size) {
        std::pair<track_set, track_set> vpeff_tracks(tracks[0], tracks[1]);
        auto it = std::find(vpeffs_tracks.begin(), vpeffs_tracks.end(), vpeff_tracks);
        if (it != vpeffs_tracks.end()) {
          vpeffs->at(it - vpeffs_tracks.begin()).inc_weight();
          vpeff = 0;
        }
        else {
          vpeffs->push_back(VertexerPairEff());
          vpeff = &vpeffs->back();
          vpeff->set_vertices(*v[0], *v[1]);
          vpeffs_tracks.push_back(vpeff_tracks);
        }
      }
      else
        vpeff = 0;

      reco::TrackRefVector shared_tracks;
      for (auto tk : tracks[0])
        if (tracks[1].count(tk) > 0)
          shared_tracks.push_back(tk);

      if (verbose) {
        if (shared_tracks.size()) {
          printf("   shared tracks are: ");
          print_track_set(shared_tracks);
          printf("\n");
        }
        else
          printf("   no shared tracks\n");
      }  

      if (shared_tracks.size() > 0) {
        if (vpeff)
          vpeff->kind(VertexerPairEff::share);

        Measurement1D v_dist = vertex_dist(*v[0], *v[1]);
        if (verbose)
          printf("   vertex dist (2d? %i) %7.3f  sig %7.3f\n", use_2d_vertex_dist, v_dist.value(), v_dist.significance());

        if (v_dist.value() < merge_shared_dist || v_dist.significance() < merge_shared_sig) {
          if (verbose) printf("          dist < %7.3f || sig < %7.3f, will try using merge result first before arbitration\n", merge_shared_dist, merge_shared_sig);
          merge = true;
        }
        else
          refit = true;

        if (verbose) printf("   checking for arbitration refit:\n");
        for (auto tk : shared_tracks) {
          const reco::TransientTrack& ttk = seed_tracks[seed_track_ref_map[tk]];
          std::pair<bool, Measurement1D> t_dist_0 = track_dist(ttk, *v[0]);
          std::pair<bool, Measurement1D> t_dist_1 = track_dist(ttk, *v[1]);
          if (verbose) {
            printf("      track-vertex0 dist (2d? %i) calc success? %i  dist %7.3f  sig %7.3f\n", use_2d_track_dist, t_dist_0.first, t_dist_0.second.value(), t_dist_0.second.significance());
            printf("      track-vertex1 dist (2d? %i) calc success? %i  dist %7.3f  sig %7.3f\n", use_2d_track_dist, t_dist_1.first, t_dist_1.second.value(), t_dist_1.second.significance());
          }

          t_dist_0.first = t_dist_0.first && (t_dist_0.second.value() < max_track_vertex_dist || t_dist_0.second.significance() < max_track_vertex_sig);
          t_dist_1.first = t_dist_1.first && (t_dist_1.second.value() < max_track_vertex_dist || t_dist_1.second.significance() < max_track_vertex_sig);
          bool remove_from_0 = !t_dist_0.first;
          bool remove_from_1 = !t_dist_1.first;
          if (t_dist_0.second.significance() < min_track_vertex_sig_to_remove && t_dist_1.second.significance() < min_track_vertex_sig_to_remove) {
            if (tracks[0].size() > tracks[1].size())
              remove_from_1 = true;
            else
              remove_from_0 = true;
          }
          else if (t_dist_0.second.significance() < t_dist_1.second.significance())
            remove_from_1 = true;
          else
            remove_from_0 = true;

          if (verbose) {
            printf("   for tk %u:\n", tk.key());
            printf("      track-vertex0 dist < %7.3f || sig < %7.3f ? %i  remove? %i\n", max_track_vertex_dist, max_track_vertex_sig, t_dist_0.first, remove_from_0);
            printf("      track-vertex1 dist < %7.3f || sig < %7.3f ? %i  remove? %i\n", max_track_vertex_dist, max_track_vertex_sig, t_dist_1.first, remove_from_1);
          }

          if (remove_from_0) tracks_to_remove_in_refit[0].insert(tk);
          if (remove_from_1) tracks_to_remove_in_refit[1].insert(tk);

          if (remove_one_track_at_a_time) {
            if (verbose)
              printf("   arbitrate only one track at a time\n");
            break;
          }
        }

        if (verbose)
          printf("   breaking to refit\n");
        
        break;
      }

      if (verbose) printf("   moving on to next vertex pair.\n");
    }

    if (duplicate) {
      vertices->erase(v[1]);
    }
    else if (merge) {
      if (verbose)
        printf("      before merge, # total vertices = %lu\n", vertices->size());

      track_set tracks_to_fit;
      for (int i = 0; i < 2; ++i)
        for (auto tk : tracks[i])
          tracks_to_fit.insert(tk);

      if (verbose) {
        printf("   merging vertices %lu and %lu with these tracks:", ivtx[0], ivtx[1]);
        print_track_set(tracks_to_fit);
        printf("\n");
      }

      std::vector<reco::TransientTrack> ttks;
      for (auto tk : tracks_to_fit)
        ttks.push_back(seed_tracks[seed_track_ref_map[tk]]);
      
      reco::VertexCollection new_vertices;
      for (const TransientVertex& tv : kv_reco_dropin(ttks))
        new_vertices.push_back(reco::Vertex(tv));
      
      if (verbose) {
        printf("      got %lu new vertices out of the av fit\n", new_vertices.size());
        printf("      these (chi2/dof : prob | track sets):");
        for (const auto& nv : new_vertices) {
          printf(" (%.3f : %.2e | ", nv.chi2()/nv.ndof(), TMath::Prob(nv.chi2(), int(nv.ndof())));
          print_track_set(nv);
          printf(" ),");
        }
        printf("\n");
      }

      // If we got two new vertices, maybe it took A B and A C D and made a better one from B C D, and left a broken one A B! C! D!.
      // If we get one that is truly the merger of the track lists, great. If it is just something like A B , A C -> A B C!, or we get nothing, then default to arbitration.
      if (new_vertices.size() > 1) {
        if (verbose)
          printf("   jiggled again?\n");   
        assert(new_vertices.size() == 2);
        *v[1] = reco::Vertex(new_vertices[1]);
        *v[0] = reco::Vertex(new_vertices[0]);
      }
      else if (new_vertices.size() == 1 && vertex_track_set(new_vertices[0], 0) == tracks_to_fit) {
        if (verbose)
          printf("   merge worked!\n");   

        if (vpeff)
          vpeff->kind(VertexerPairEff::merge);

        vertices->erase(v[1]);
        *v[0] = reco::Vertex(new_vertices[0]); // ok to use v[0] after the erase(v[1]) because v[0] is by construction before v[1]
      }
      else {
        if (verbose)
          printf("   merge didn't work, trying arbitration refits\n");   
        refit = true;
      }

      if (verbose)
        printf("   vertices size is now %lu\n", vertices->size());
    }

    if (refit) {
      bool erase[2] = { false };
      reco::Vertex vsave[2] = { *v[0], *v[1] };

      for (int i = 0; i < 2; ++i) {
        if (tracks_to_remove_in_refit[i].empty())
          continue;

        if (verbose) {
          printf("   refit vertex%i %lu with these tracks:", i, ivtx[i]);
          print_track_set(tracks[i]);
          printf("   but skip these:");
          print_track_set(tracks_to_remove_in_refit[i]);
          printf("\n");
        }

        std::vector<reco::TransientTrack> ttks;
        for (auto tk : tracks[i])
          if (tracks_to_remove_in_refit[i].count(tk) == 0) 
            ttks.push_back(seed_tracks[seed_track_ref_map[tk]]);

        reco::VertexCollection new_vertices;
        for (const TransientVertex& tv : kv_reco_dropin(ttks))
          new_vertices.push_back(reco::Vertex(tv));
        if (verbose) {
          printf("      got %lu new vertices out of the av fit for v%i\n", new_vertices.size(), i);
          printf("      these track sets:");
          for (const auto& nv : new_vertices) {
            printf(" (");
            print_track_set(nv);
            printf(" ),");
          }
          printf("\n");
        }
        if (new_vertices.size() == 1)
          *v[i] = new_vertices[0];
        else
          erase[i] = true;
      }

      if (vpeff && (erase[0] || erase[1]))
        vpeff->kind(VertexerPairEff::erase);

      if (erase[1]) vertices->erase(v[1]);
      if (erase[0]) vertices->erase(v[0]);

      if (verbose)
        printf("      vertices size is now %lu\n", vertices->size());
    }

    // If we changed the vertices at all, start loop over completely.
    if (duplicate || merge || refit) {
      v[0] = vertices->begin() - 1;  // -1 because about to ++sv
      ++n_resets;
      if (verbose) printf("   resetting from vertices %lu and %lu. # of resets: %i\n", ivtx[0], ivtx[1], n_resets);
      
      //if (n_resets == 3000)
      //  throw "I'm dumb";
    }
  }

  if (verbose)
    printf("n_resets: %i  n_onetracks: %i  n_noshare_vertices: %lu\n", n_resets, n_onetracks, vertices->size());
  if (histos) {
    h_n_resets->Fill(n_resets);
    h_n_onetracks->Fill(n_onetracks);
    h_n_noshare_vertices->Fill(vertices->size());
  }

  if (histos || verbose) {
    std::map<reco::TrackRef, int> track_use;
    for (size_t i = 0, ie = vertices->size(); i < ie; ++i) {
      const reco::Vertex& v = vertices->at(i);
      const int ntracks = v.nTracks();
      const double vchi2 = v.normalizedChi2();
      const double vndof = v.ndof();
      const double vx = v.position().x() - bs_x;
      const double vy = v.position().y() - bs_y;
      const double vz = v.position().z() - bs_z;
      const double rho = mag(vx, vy);
      const double phi = atan2(vy, vx);
      const double r = mag(vx, vy, vz);
      for (const auto& r : vertex_track_set(v)) {
        if (track_use.find(r) != track_use.end())
          track_use[r] += 1;
        else
          track_use[r] = 1;
      }

      if (verbose)
        printf("no-share vertex #%3lu: ntracks: %i chi2/dof: %7.3f dof: %7.3f pos: <%7.3f, %7.3f, %7.3f>  rho: %7.3f  phi: %7.3f  r: %7.3f\n", i, ntracks, vchi2, vndof, vx, vy, vz, rho, phi, r);

      if (histos) {
        h_noshare_vertex_ntracks->Fill(ntracks);
        for (auto it = v.tracks_begin(), ite = v.tracks_end(); it != ite; ++it) {
	  h_noshare_vertex_track_weights->Fill(v.trackWeight(*it));

	  reco::TransientTrack seed_track;
	  seed_track = tt_builder->build(*it.operator*());
	  std::pair<bool, Measurement1D> tk_vtx_dist = track_dist(seed_track, v);
	  h_noshare_vertex_tkvtxdist->Fill(tk_vtx_dist.second.value());
	  h_noshare_vertex_tkvtxdisterr->Fill(tk_vtx_dist.second.error());
	  h_noshare_vertex_tkvtxdistsig->Fill(tk_vtx_dist.second.significance());
	}
        h_noshare_vertex_chi2->Fill(vchi2);
        h_noshare_vertex_ndof->Fill(vndof);
        h_noshare_vertex_x->Fill(vx);
        h_noshare_vertex_y->Fill(vy);
        h_noshare_vertex_rho->Fill(rho);
        h_noshare_vertex_phi->Fill(phi);
        h_noshare_vertex_z->Fill(vz);
        h_noshare_vertex_r->Fill(r);

        for (size_t j = i+1, je = vertices->size(); j < je; ++j) {
          const reco::Vertex& vj = vertices->at(j);
          const double vjx = vj.position().x() - bs_x;
          const double vjy = vj.position().y() - bs_y;
          const double phij = atan2(vjy, vjx);
          h_noshare_vertex_paird2d->Fill(mag(vx - vjx, vy - vjy));
          h_noshare_vertex_pairdphi->Fill(reco::deltaPhi(phi, phij));
        }
      }
    }
    
    if (verbose)
      printf("track multiple uses:\n");

    int max_noshare_track_multiplicity = 0;
    for (const auto& p : track_use) {
      if (verbose && p.second > 1)
        printf("track %3u used %3i times\n", p.first.key(), p.second);
      if (histos)
        h_noshare_track_multiplicity->Fill(p.second);
      if (p.second > max_noshare_track_multiplicity)
        max_noshare_track_multiplicity = p.second;
    }
    if (histos)
      h_max_noshare_track_multiplicity->Fill(max_noshare_track_multiplicity);
  }

  //////////////////////////////////////////////////////////////////////
  // Merge vertices that are still "close". JMTBAD this doesn't do anything currently.
  //////////////////////////////////////////////////////////////////////

  if (verbose)
    printf("fun2!\n");

  for (v[0] = vertices->begin(); v[0] != vertices->end(); ++v[0]) {
    ivtx[0] = v[0] - vertices->begin();

    bool merge = false;
    for (v[1] = v[0] + 1; v[1] != vertices->end(); ++v[1]) {
      ivtx[1] = v[1] - vertices->begin();

      if (verbose)
        printf("close-merge: # vertices = %lu. considering vertices #%lu (ntk = %i) and #%lu (ntk = %i):", vertices->size(), ivtx[0], v[0]->nTracks(), ivtx[1], v[1]->nTracks());

      Measurement1D v_dist = vertex_dist(*v[0], *v[1]);
      if (verbose)
        printf("   vertex dist (2d? %i) %7.3f  sig %7.3f\n", use_2d_vertex_dist, v_dist.value(), v_dist.significance());
  
      if (v_dist.value() < merge_anyway_dist || v_dist.significance() < merge_anyway_sig) {
        if (verbose)
          printf("          dist < %7.3f || sig < %7.3f, breaking to merge\n", merge_anyway_dist, merge_anyway_sig);
        merge = true;
        break;
      }
    }

    if (merge) {
      std::vector<reco::TransientTrack> ttks;
      for (int i = 0; i < 2; ++i)
        for (auto tk : vertex_track_set(*v[i]))
          ttks.push_back(tt_builder->build(tk));
      
      reco::VertexCollection new_vertices;
      for (const TransientVertex& tv : kv_reco_dropin(ttks))
        new_vertices.push_back(reco::Vertex(tv));
      
      if (verbose) {
        printf("      got %lu new vertices out of the av fit\n", new_vertices.size());
        printf("      these track sets:");
        for (const auto& nv : new_vertices) {
          printf(" (");
          print_track_set(nv);
          printf(" ),");
        }
        printf("\n");
      }
    }
  }
 
  //////////////////////////////////////////////////////////////////////
  // Put the output.
  //////////////////////////////////////////////////////////////////////

  finish(event, seed_tracks, std::move(vertices), std::move(vpeffs), vpeffs_tracks);
}

DEFINE_FWK_MODULE(MFVVertexer);
