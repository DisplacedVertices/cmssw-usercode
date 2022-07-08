#include "TH2.h"
#include "TMath.h"
#include <math.h>  
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "RecoVertex/VertexTools/interface/VertexDistanceXY.h"
#include "TrackingTools/IPTools/interface/IPTools.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexerPairEff.h"
#include "JMTucker/MFVNeutralino/interface/VertexerParams.h"
#include "JMTucker/Tools/interface/Utilities.h"

class MFVVertexer : public edm::EDProducer {
  public:
    MFVVertexer(const edm::ParameterSet&);
    virtual void produce(edm::Event&, const edm::EventSetup&);

  private:
    typedef std::set<reco::TrackRef> track_set;
    typedef std::vector<reco::TrackRef> track_vec;

    std::pair<bool, std::vector<std::vector<size_t>>> sharedjets(const size_t vtx0idx, const size_t vtx1idx, const std::vector < std::vector<size_t>>& sv_match_jetidx, const std::vector < std::vector<size_t>>& sv_match_trkidx);
    bool hasCommonElement(std::vector<size_t> vec0, std::vector<size_t> vec1);
    std::vector<size_t>::iterator getFirstCommonElement(std::vector<size_t>& vec0, std::vector<size_t>& vec1);
    template <typename T> void eraseElement(std::vector<T>& vec, size_t idx);
    void createSetofSharedJetTracks(std::vector<std::vector<size_t>>& vec_sharedjet_track_idx, std::vector<size_t>& vec_special_sharedjet_track_idx, std::vector<size_t>& vec_all_track_idx, std::vector<size_t>& vec_sharedjet_idx, size_t sharedjet_idx); 
    bool match_track_jet(const reco::Track& tk, const pat::Jet& jet, const pat::JetCollection& jets, const size_t& idx);

    void finish(edm::Event&, const std::vector<reco::TransientTrack>&, std::unique_ptr<reco::VertexCollection>, std::unique_ptr<VertexerPairEffs>, const std::vector<std::pair<track_set, track_set>>&);

    enum stepEnum{afterdzfit, aftermerge, aftersharedjets, N_STEPS};
    std::vector<TString> stepStrs = {"afterdzfit", "aftermerge", "aftersharedjets", "N_STEPS"};
    void fillCommonOutputHists(std::unique_ptr<reco::VertexCollection>& vertices, const reco::Vertex& fake_bs_vtx, edm::ESHandle<TransientTrackBuilder>& tt_builder, size_t step);

    template <typename T>
      void print_track_set(const T& ts) const {
        for (auto r : ts)
          printf(" %u", r.key());
      }

    template <typename T>
      void print_track_set(const T & ts, const reco::Vertex & v) const {
        for (auto r : ts)
          printf(" %u%s", r.key(), (v.trackWeight(r) < mfv::track_vertex_weight_min ? "!" : ""));
      }

    void print_track_set(const reco::Vertex & v) const {
      for (auto r = v.tracks_begin(), re = v.tracks_end(); r != re; ++r)
        printf(" %lu%s", r->key(), (v.trackWeight(*r) < mfv::track_vertex_weight_min ? "!" : ""));
    }

    bool is_track_subset(const track_set & a, const track_set & b) const {
      bool is_subset = true;
      const track_set& smaller = a.size() <= b.size() ? a : b;
      const track_set& bigger = a.size() <= b.size() ? b : a;

      for (auto t : smaller)
        if (bigger.count(t) < 1) {
          is_subset = false;
          break;
        }

      return is_subset;
    }

    track_set vertex_track_set(const reco::Vertex & v, const double min_weight = mfv::track_vertex_weight_min) const {
      track_set result;

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

    track_vec vertex_track_vec(const reco::Vertex & v, const double min_weight = mfv::track_vertex_weight_min) const {
      track_set s = vertex_track_set(v, min_weight);
      return track_vec(s.begin(), s.end());
    }

    Measurement1D vertex_dist(const reco::Vertex & v0, const reco::Vertex & v1) const {
      if (use_2d_vertex_dist)
        return vertex_dist_2d.distance(v0, v1);
      else
        return vertex_dist_3d.distance(v0, v1);
    }

    std::pair<bool, Measurement1D> track_dist(const reco::TransientTrack & t, const reco::Vertex & v) const {
      if (use_2d_track_dist)
        return IPTools::absoluteTransverseImpactParameter(t, v);
      else
        return IPTools::absoluteImpactParameter3D(t, v);
    }

    VertexDistanceXY vertex_dist_2d;
    VertexDistance3D vertex_dist_3d;
    std::unique_ptr<KalmanVertexFitter> kv_reco;

    std::vector<TransientVertex> kv_reco_dropin(std::vector<reco::TransientTrack> & ttks) {
      if (ttks.size() < 2)
        return std::vector<TransientVertex>();
      std::vector<TransientVertex> v(1, kv_reco->vertex(ttks));
      if (v[0].normalisedChiSquared() > 5)
        return std::vector<TransientVertex>();
      return v;
    }

    std::vector<TransientVertex> kv_reco_dropin_nocut(std::vector<reco::TransientTrack> & ttks) {
      if (ttks.size() < 2)
        return std::vector<TransientVertex>();
      std::vector<TransientVertex> v(1, kv_reco->vertex(ttks));
      return v;
    }
    const bool do_track_refinement;
    const bool resolve_split_vertices_loose;
    const bool resolve_split_vertices_tight;
    const bool investigate_merged_vertices;
    const bool resolve_shared_jets;
    const edm::EDGetTokenT<pat::JetCollection> shared_jet_token;
    const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
    const edm::EDGetTokenT<std::vector<reco::TrackRef>> seed_tracks_token;
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
    const double max_nm1_refit_dist3;
    const double max_nm1_refit_distz;
    const int max_nm1_refit_count;
    const double trackrefine_sigmacut;
    const double trackrefine_trimmax;
    const bool histos;
    const bool histos_noshare;
    const bool histos_output_afterdzfit;
    const bool histos_output_aftermerge;
    const bool histos_output_aftersharedjets;
    const bool verbose;
    const std::string module_label;


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

    TH1F* h_n_noshare_vertices;
    TH1F* h_noshare_vertex_ntracks;
    TH1F* h_noshare_vertex_mass;
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

    TH1F* h_noshare_vertex_tkvtxdist;
    TH1F* h_noshare_vertex_tkvtxdisterr;
    TH1F* h_noshare_vertex_tkvtxdistsig;

    TH1F* h_noshare_vertex_tkvtxdist_before_do_track_refinement;
    TH1F* h_noshare_vertex_tkvtxdisterr_before_do_track_refinement;
    TH1F* h_noshare_vertex_tkvtxdistsig_before_do_track_refinement;

    TH1F* h_noshare_trackrefine_sigmacut_vertex_chi2;
    TH1F* h_noshare_trackrefine_sigmacut_vertex_tkvtxdistsig;
    TH1F* h_noshare_trackrefine_sigmacut_vertex_distr_shift;

    TH1F* h_noshare_trackrefine_trimmax_vertex_chi2;
    TH1F* h_noshare_trackrefine_trimmax_vertex_tkvtxdistsig;
    TH1F* h_noshare_trackrefine_trimmax_vertex_distr_shift;

    TH1F* h_n_output_vertices;
    TH1F* h_n_at_least_5trk_output_vertices;

    TH1F* hs_output_vertex_tkvtxdist[stepEnum::N_STEPS];
    TH1F* hs_output_vertex_tkvtxdisterr[stepEnum::N_STEPS];
    TH1F* hs_output_vertex_tkvtxdistsig[stepEnum::N_STEPS];
    TH1F* hs_n_at_least_5trk_output_vertices[stepEnum::N_STEPS];
    TH1F* hs_output_vertex_nm1_bsbs2ddist[stepEnum::N_STEPS];
    TH1F* hs_output_vertex_nm1_bs2derr[stepEnum::N_STEPS];
    TH1F* hs_output_vertex_ntracks[stepEnum::N_STEPS];
    TH1F* hs_output_vertex_mass[stepEnum::N_STEPS];
    TH1F* hs_output_vertex_track_weights[stepEnum::N_STEPS];
    TH1F* hs_output_vertex_chi2[stepEnum::N_STEPS];
    TH1F* hs_output_vertex_ndof[stepEnum::N_STEPS];
    TH1F* hs_output_vertex_x[stepEnum::N_STEPS];
    TH1F* hs_output_vertex_y[stepEnum::N_STEPS];
    TH1F* hs_output_vertex_rho[stepEnum::N_STEPS];
    TH1F* hs_output_vertex_phi[stepEnum::N_STEPS];
    TH1F* hs_output_vertex_z[stepEnum::N_STEPS];
    TH1F* hs_output_vertex_r[stepEnum::N_STEPS];
    TH1F* hs_output_vertex_paird2d[stepEnum::N_STEPS];
    TH1F* hs_output_vertex_paird2dsig[stepEnum::N_STEPS];
    TH1F* hs_output_vertex_pairdphi[stepEnum::N_STEPS];

    TH1F* h_output_aftermerge_potential_merged_vertex_nm1_chi2;
    TH1F* h_output_aftermerge_potential_merged_vertex_nm1_ntracks;
    TH1F* h_output_aftermerge_potential_merged_vertex_nm1_bs2derr;
    TH1F* h_output_aftermerge_potential_merged_vertex_nm1_bsbs2ddist;

    TH1F* h_resolve_shared_jets_lonetrkvtx_dphi;

    TH1F* h_output_aftersharedjets_n_onetracks;

};

MFVVertexer::MFVVertexer(const edm::ParameterSet& cfg)
  : 
    kv_reco(new KalmanVertexFitter(cfg.getParameter<edm::ParameterSet>("kvr_params"), cfg.getParameter<edm::ParameterSet>("kvr_params").getParameter<bool>("doSmoothing"))),
    do_track_refinement(cfg.getParameter<bool>("do_track_refinement")),
    resolve_split_vertices_loose(cfg.getParameter<bool>("resolve_split_vertices_loose")),
    resolve_split_vertices_tight(cfg.getParameter<bool>("resolve_split_vertices_tight")),
    investigate_merged_vertices(cfg.getParameter<bool>("investigate_merged_vertices")),
    resolve_shared_jets(cfg.getParameter<bool>("resolve_shared_jets")),
    shared_jet_token(resolve_shared_jets ? consumes<pat::JetCollection>(cfg.getParameter<edm::InputTag>("resolve_shared_jets_src")) : edm::EDGetTokenT<pat::JetCollection>()),
    beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot_src"))),
    seed_tracks_token(consumes<std::vector<reco::TrackRef>>(cfg.getParameter<edm::InputTag>("seed_tracks_src"))),
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
    max_nm1_refit_dist3(cfg.getParameter<double>("max_nm1_refit_dist3")),
    max_nm1_refit_distz(cfg.getParameter<double>("max_nm1_refit_distz")),
    max_nm1_refit_count(cfg.getParameter<int>("max_nm1_refit_count")),
    trackrefine_sigmacut(cfg.getParameter<double>("trackrefine_sigmacut")),
    trackrefine_trimmax(cfg.getParameter<double>("trackrefine_trimmax")),
    histos(cfg.getUntrackedParameter<bool>("histos", false)),
    histos_noshare(cfg.getUntrackedParameter<bool>("histos_noshare", false)),
    histos_output_afterdzfit(cfg.getUntrackedParameter<bool>("histos_output_afterdzfit", false)),
    histos_output_aftermerge(cfg.getUntrackedParameter<bool>("histos_output_aftermerge", false)),
    histos_output_aftersharedjets(cfg.getUntrackedParameter<bool>("histos_output_aftersharedjets", false)),
    verbose(cfg.getUntrackedParameter<bool>("verbose", false)),
    module_label(cfg.getParameter<std::string>("@module_label"))
{
  if (n_tracks_per_seed_vertex < 2 || n_tracks_per_seed_vertex > 5)
    throw cms::Exception("MFVVertexer", "n_tracks_per_seed_vertex must be one of 2,3,4,5");

  produces<reco::VertexCollection>();
  produces<VertexerPairEffs>();
  produces<reco::TrackCollection>("seed"); // JMTBAD remove me
  produces<reco::TrackCollection>("inVertices");

  if (histos) {
    edm::Service<TFileService> fs;

    h_n_seed_vertices                = fs->make<TH1F>("h_n_seed_vertices",                ";# of seed vertices",  50,   0,    200);
    h_seed_vertex_track_weights      = fs->make<TH1F>("h_seed_vertex_track_weights",      ";seed vertex's track weights",  21,   0,      1.05);
    h_seed_vertex_chi2               = fs->make<TH1F>("h_seed_vertex_chi2",               ";normalized chi2",  40,   0, 10);
    h_seed_vertex_ndof               = fs->make<TH1F>("h_seed_vertex_ndof",               ";ndof",  10,   0,     20);
    h_seed_vertex_x                  = fs->make<TH1F>("h_seed_vertex_x",                  ";vtxbsdist_x (cm.)", 20,  -1,      1);
    h_seed_vertex_y                  = fs->make<TH1F>("h_seed_vertex_y",                  ";vtxbsdist_y (cm.)", 20,  -1,      1);
    h_seed_vertex_rho                = fs->make<TH1F>("h_seed_vertex_rho",                ";vtx rho", 20,   0,      2);
    h_seed_vertex_phi                = fs->make<TH1F>("h_seed_vertex_phi",                ";vtx phi",  20,  -3.15,   3.15);
    h_seed_vertex_z                  = fs->make<TH1F>("h_seed_vertex_z",                  ";vtxbsdist_z (cm.)",  20, -20,     20);
    h_seed_vertex_r                  = fs->make<TH1F>("h_seed_vertex_r",                  ";vtxbsdist_r (cm.)", 20,   0,      2);
    h_seed_vertex_paird2d            = fs->make<TH1F>("h_seed_vertex_paird2d",            ";svdist2d (cm.) every pair", 100,   0,      0.2);
    h_seed_vertex_pairdphi           = fs->make<TH1F>("h_seed_vertex_pairdphi",           ";dPhi(vtx0,vtx1) every pair", 100,  -3.14,   3.14);

    h_n_resets                       = fs->make<TH1F>("h_n_resets",                       "", 50,   0,   500);
    h_n_onetracks                    = fs->make<TH1F>("h_n_onetracks",                    "",  5,   0,     5);

    h_n_noshare_vertices             = fs->make<TH1F>("h_n_noshare_vertices",             ";# of noshare vertices", 20,   0,    50);

    if (histos_noshare) {
      h_noshare_vertex_ntracks = fs->make<TH1F>("h_noshare_vertex_ntracks", ";ntracks/vtx", 30, 0, 30);
      h_noshare_vertex_mass = fs->make<TH1F>("h_noshare_vertex_mass", ";mass/vtx (GeV)", 20, 0, 1000);
      h_noshare_vertex_track_weights = fs->make<TH1F>("h_noshare_vertex_track_weights", ";vertex track weights", 21, 0, 1.05);
      h_noshare_vertex_chi2 = fs->make<TH1F>("h_noshare_vertex_chi2", ";normalized chi2", 40, 0, 10);
      h_noshare_vertex_ndof = fs->make<TH1F>("h_noshare_vertex_ndof", ";ndof", 10, 0, 20);
      h_noshare_vertex_x = fs->make<TH1F>("h_noshare_vertex_x", ";vtxbsdist_x (cm.)", 20, -1, 1);
      h_noshare_vertex_y = fs->make<TH1F>("h_noshare_vertex_y", ";vtxbsdist_y (cm.)", 20, -1, 1);
      h_noshare_vertex_rho = fs->make<TH1F>("h_noshare_vertex_rho", ";vtx rho", 20, 0, 2);
      h_noshare_vertex_phi = fs->make<TH1F>("h_noshare_vertex_phi", ";vtx phi", 20, -3.15, 3.15);
      h_noshare_vertex_z = fs->make<TH1F>("h_noshare_vertex_z", ";vtxbsdist_z (cm.)", 20, -20, 20);
      h_noshare_vertex_r = fs->make<TH1F>("h_noshare_vertex_r", ";vtxbsdist_r (cm.)", 20, 0, 2);
      h_noshare_vertex_paird2d = fs->make<TH1F>("h_noshare_vertex_paird2d", ";svdist2d (cm.) every pair", 100, 0, 0.2);
      h_noshare_vertex_pairdphi = fs->make<TH1F>("h_noshare_vertex_pairdphi", ";dPhi(vtx0,vtx1) every pair", 100, -3.14, 3.14);
      h_noshare_track_multiplicity = fs->make<TH1F>("h_noshare_track_multiplicity", "", 20, 0, 40);
      h_max_noshare_track_multiplicity = fs->make<TH1F>("h_max_noshare_track_multiplicity", "", 20, 0, 40);
      h_noshare_vertex_tkvtxdist = fs->make<TH1F>("h_noshare_vertex_tkvtxdist", ";tkvtxdist (cm.)", 20, 0, 0.1);
      h_noshare_vertex_tkvtxdisterr = fs->make<TH1F>("h_noshare_vertex_tkvtxdisterr", ";tkvtxdisterr (cm.)", 20, 0, 0.1);
      h_noshare_vertex_tkvtxdistsig = fs->make<TH1F>("h_noshare_vertex_tkvtxdistsig", ";tkvtxdistsig", 20, 0, 6);
    }

    if (do_track_refinement) {
      h_noshare_vertex_tkvtxdist_before_do_track_refinement = fs->make<TH1F>("h_noshare_vertex_tkvtxdist_before_do_track_refinement", ";tkvtxdist (cm.)", 20, 0, 0.1);
      h_noshare_vertex_tkvtxdisterr_before_do_track_refinement = fs->make<TH1F>("h_noshare_vertex_tkvtxdisterr_before_do_track_refinement", ";tkvtxdisterr (cm.)", 20, 0, 0.1);
      h_noshare_vertex_tkvtxdistsig_before_do_track_refinement = fs->make<TH1F>("h_noshare_vertex_tkvtxdistsig_before_do_track_refinement", ";tkvtxdistsig", 20, 0, 6);
      h_noshare_trackrefine_sigmacut_vertex_chi2 = fs->make<TH1F>("h_noshare_trackrefine_sigmacut_vertex_chi2", ";chi2/dof", 10, 0, 10);
      h_noshare_trackrefine_sigmacut_vertex_tkvtxdistsig = fs->make<TH1F>("h_noshare_trackrefine_sigmacut_vertex_tkvtxdistsig", ";missdist sig", 20, 0, 6);
      h_noshare_trackrefine_sigmacut_vertex_distr_shift = fs->make<TH1F>("h_noshare_trackrefine_sigmacut_vertex_distr_shift", ";vtx after sigmacut'r - vtx before sigmacut'r (cm)", 20, -0.08, 0.08);

      h_noshare_trackrefine_trimmax_vertex_chi2 = fs->make<TH1F>("h_noshare_trackrefine_trimmax_vertex_chi2", ";chi2/dof", 10, 0, 10);
      h_noshare_trackrefine_trimmax_vertex_tkvtxdistsig = fs->make<TH1F>("h_noshare_trackrefine_trimmax_vertex_tkvtxdistsig", ";missdist sig", 20, 0, 6);
      h_noshare_trackrefine_trimmax_vertex_distr_shift = fs->make<TH1F>("h_noshare_trackrefine_trimmax_vertex_distr_shift", ";vtx after trimmax'r - vtx before trimmax'r (cm)", 20, -0.08, 0.08);
    }

    h_n_output_vertices = fs->make<TH1F>("h_n_output_vertices", ";# of output vertices", 50, 0, 50);
    h_n_at_least_5trk_output_vertices = fs->make<TH1F>("h_n_at_least_5trk_output_vertices", ";# of output vertices w/ >=5trk/vtx", 20, 0, 20);

    for(size_t step = 0; step < stepEnum::N_STEPS; ++step) {

      if (step == stepEnum::afterdzfit      && !histos_output_afterdzfit)      continue;
      if (step == stepEnum::aftermerge      && !histos_output_aftermerge)      continue;
      if (step == stepEnum::aftersharedjets && !histos_output_aftersharedjets) continue;

      hs_n_at_least_5trk_output_vertices[step] = fs->make<TH1F>("h_n_at_least_5trk_output_"+stepStrs[step]+"_vertices", ";# of >=5trk-vertices", 20, 0, 20);
      hs_output_vertex_nm1_bsbs2ddist[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_nm1_bsbs2ddist", ";dBV (cm.) w/ n-1 cuts applied", 100, 0, 1.0);
      hs_output_vertex_nm1_bs2derr[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_nm1_bs2derr", ";bs2derr (cm.) w/ n-1 cuts applied", 20, 0, 0.05);
      hs_output_vertex_tkvtxdist[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_tkvtxdist", ";tkvtxdist (cm.)", 20, 0, 0.1);
      hs_output_vertex_tkvtxdisterr[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_tkvtxdisterr", ";tkvtxdisterr (cm.)", 20, 0, 0.1);
      hs_output_vertex_tkvtxdistsig[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_tkvtxdistsig", ";tkvtxdistsig", 20, 0, 6);
      hs_output_vertex_ntracks[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_ntracks", ";ntracks/vtx", 30, 0, 30);
      hs_output_vertex_mass[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_mass", ";mass/vtx (GeV)", 20, 0, 1000);
      hs_output_vertex_track_weights[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_track_weights", ";vertex track weights", 21, 0, 1.05);
      hs_output_vertex_chi2[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_chi2", ";normalized chi2", 40, 0, 10);
      hs_output_vertex_ndof[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_ndof", ";ndof", 10, 0, 20);
      hs_output_vertex_x[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_x", ";vtxbsdist_x (cm.)", 20, -1, 1);
      hs_output_vertex_y[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_y", ";vtxbsdist_y (cm.)", 20, -1, 1);
      hs_output_vertex_rho[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_rho", ";vtx rho", 20, 0, 2);
      hs_output_vertex_phi[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_phi", ";vtx phi", 20, -3.15, 3.15);
      hs_output_vertex_z[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_z", ";vtxbsdist_z (cm.)", 20, -20, 20);
      hs_output_vertex_r[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_r", ";vtxbsdist_r (cm.)", 20, 0, 2);
      hs_output_vertex_paird2d[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_paird2d", ";svdist2d (cm.) every pair", 100, 0, 0.2);
      hs_output_vertex_paird2dsig[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_paird2dsig", ";svdist2d significance every pair", 100, 0, 20);
      hs_output_vertex_pairdphi[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_pairdphi", ";dPhi(vtx0,vtx1) every pair", 100, -3.14, 3.14);
    }

    if (investigate_merged_vertices) {
      h_output_aftermerge_potential_merged_vertex_nm1_chi2 = fs->make<TH1F>("h_output_aftermerge_potential_merged_vertex_nm1_chi2", ";normalized chi2 w/ n-1 cuts applied", 80, 0, 20);
      h_output_aftermerge_potential_merged_vertex_nm1_ntracks = fs->make<TH1F>("h_output_aftermerge_potential_merged_vertex_nm1_ntracks", ";ntracks/vtx w/ n-1 cuts applied", 30, 0, 30);
      h_output_aftermerge_potential_merged_vertex_nm1_bs2derr = fs->make<TH1F>("h_output_aftermerge_potential_merged_vertex_nm1_bs2derr", ";bs2derr (cm.) w/ n-1 cuts applied", 20, 0, 0.05);
      h_output_aftermerge_potential_merged_vertex_nm1_bsbs2ddist = fs->make<TH1F>("h_output_aftermerge_potential_merged_vertex_nm1_bsbs2ddist", ";dBV (cm.) w/ n-1 cuts applied", 100, 0, 1.0);
    }

    if (resolve_shared_jets) {
      h_resolve_shared_jets_lonetrkvtx_dphi = fs->make<TH1F>("h_resolve_shared_jets_lonetrkvtx_dphi", ";|dPhi(vtx,a lone track)|", 20, 0, 3.15);
    }

    if (histos_output_aftersharedjets) {
      h_output_aftersharedjets_n_onetracks = fs->make<TH1F>("h_output_aftersharedjets_n_onetracks", "", 5, 0, 5);
    }
  }
}

void MFVVertexer::finish(edm::Event& event, const std::vector<reco::TransientTrack>& seed_tracks, std::unique_ptr<reco::VertexCollection> vertices, std::unique_ptr<VertexerPairEffs> vpeffs, const std::vector<std::pair<track_set, track_set>>& vpeffs_tracks) {
  std::unique_ptr<reco::TrackCollection> tracks_seed      (new reco::TrackCollection);
  std::unique_ptr<reco::TrackCollection> tracks_inVertices(new reco::TrackCollection);

  if (verbose) printf("finish:\nseed tracks:\n");

  std::map<std::pair<unsigned, unsigned>, unsigned char> seed_track_ref_map;
  unsigned char itk = 0;
  for (const reco::TransientTrack& ttk : seed_tracks) {
    tracks_seed->push_back(ttk.track());
    const reco::TrackBaseRef& tk(ttk.trackBaseRef());
    seed_track_ref_map[std::make_pair(tk.id().id(), tk.key())] = uint2uchar_clamp(itk++);

    if (verbose) printf("id: %i key: %lu pt: %f\n", tk.id().id(), tk.key(), tk->pt());
  }

  assert(vpeffs->size() == vpeffs_tracks.size());
  for (size_t i = 0, ie = vpeffs->size(); i < ie; ++i) {
    for (auto tk : vpeffs_tracks[i].first)  (*vpeffs)[i].tracks_push_back(0, seed_track_ref_map[std::make_pair(tk.id().id(), tk.key())]);
    for (auto tk : vpeffs_tracks[i].second) (*vpeffs)[i].tracks_push_back(1, seed_track_ref_map[std::make_pair(tk.id().id(), tk.key())]);
  }

  if (verbose) printf("vertices:\n");
  int count_5trk_vertices = 0;
  for (const reco::Vertex& v : *vertices) {
    if (verbose) printf("x: %f y %f z %f\n", v.x(), v.y(), v.z());
    for (auto it = v.tracks_begin(), ite = v.tracks_end(); it != ite; ++it) {
      reco::TrackRef tk = it->castTo<reco::TrackRef>();
      if (verbose) printf("id: %i key: %u <%f,%f,%f,%f,%f>\n", tk.id().id(), tk.key(), tk->charge()*tk->pt(), tk->eta(), tk->phi(), tk->dxy(), tk->dz());
      tracks_inVertices->push_back(*tk);
    }
    if (v.nTracks() >= 5)
      ++count_5trk_vertices;
  }

  if (verbose)
    printf("n_output_vertices: %lu\n", vertices->size());
  if (histos) {
    h_n_output_vertices->Fill(vertices->size());
    h_n_at_least_5trk_output_vertices->Fill(count_5trk_vertices);
  }

  event.put(std::move(vertices));
  event.put(std::move(vpeffs));
  event.put(std::move(tracks_seed),       "seed");
  event.put(std::move(tracks_inVertices), "inVertices");
}

void MFVVertexer::produce(edm::Event& event, const edm::EventSetup& setup) {
  if (verbose)
    std::cout << "MFVVertexer " << module_label << " run " << event.id().run() << " lumi " << event.luminosityBlock() << " event " << event.id().event() << "\n";

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByToken(beamspot_token, beamspot);
  const double bsx = beamspot->position().x();
  const double bsy = beamspot->position().y();
  const double bsz = beamspot->position().z();
  const reco::Vertex fake_bs_vtx(beamspot->position(), beamspot->covariance3D());

  edm::ESHandle<TransientTrackBuilder> tt_builder;
  setup.get<TransientTrackRecord>().get("TransientTrackBuilder", tt_builder);

  edm::Handle<std::vector<reco::TrackRef>> seed_track_refs;
  event.getByToken(seed_tracks_token, seed_track_refs);

  std::vector<reco::TransientTrack> seed_tracks;
  std::map<reco::TrackRef, size_t> seed_track_ref_map;

  for (const reco::TrackRef& tk : *seed_track_refs) {
    seed_tracks.push_back(tt_builder->build(tk));
    seed_track_ref_map[tk] = seed_tracks.size() - 1;
  }

  const size_t ntk = seed_tracks.size();
  if (verbose)
    printf("n_seed_tracks: %5lu\n", ntk);

  //////////////////////////////////////////////////////////////////////
  // Form seed vertices from all pairs of tracks whose vertex fit
  // passes cuts.
  //////////////////////////////////////////////////////////////////////

  std::unique_ptr<reco::VertexCollection> vertices(new reco::VertexCollection);
  std::unique_ptr<VertexerPairEffs> vpeffs(new VertexerPairEffs);
  std::vector<std::pair<track_set, track_set>> vpeffs_tracks;

  if (ntk == 0) {
    if (verbose)
      printf("no seed tracks -> putting empty vertex collection into event\n");
    finish(event, seed_tracks, std::move(vertices), std::move(vpeffs), vpeffs_tracks);
    return;
  }

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
        const double vx = v.position().x() - bsx;
        const double vy = v.position().y() - bsy;
        const double vz = v.position().z() - bsz;
        const double phi = atan2(vy, vx);
        const double rho = mag(vx, vy);
        const double r = mag(vx, vy, vz);
        if (verbose) {
          printf("from tracks");
          for (auto itk : itks)
            printf(" %lu", itk);
          printf(": vertex #%3lu: chi2/dof: %7.3f dof: %7.3f pos: <%7.3f, %7.3f, %7.3f>  rho: %7.3f  phi: %7.3f  r: %7.3f\n", vertices->size() - 1, vchi2, vndof, vx, vy, vz, rho, phi, r);
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
    itks[0] = itk;
    for (size_t jtk = itk + 1; jtk < ntk; ++jtk) {
      itks[1] = jtk;
      if (n_tracks_per_seed_vertex == 2) { try_seed_vertex(); continue; }
      for (size_t ktk = jtk + 1; ktk < ntk; ++ktk) {
        itks[2] = ktk;
        if (n_tracks_per_seed_vertex == 3) { try_seed_vertex(); continue; }
        for (size_t ltk = ktk + 1; ltk < ntk; ++ltk) {
          itks[3] = ltk;
          if (n_tracks_per_seed_vertex == 4) { try_seed_vertex(); continue; }
          for (size_t mtk = ltk + 1; mtk < ntk; ++mtk) {
            itks[4] = mtk;
            try_seed_vertex();
          }
        }
      }
    }
  }

  if (histos) {
    for (std::vector<reco::Vertex>::const_iterator v0 = vertices->begin(); v0 != vertices->end(); ++v0) {
      const double v0x = v0->position().x() - bsx;
      const double v0y = v0->position().y() - bsy;
      const double phi0 = atan2(v0y, v0x);
      for (std::vector<reco::Vertex>::const_iterator v1 = v0 + 1; v1 != vertices->end(); ++v1) {
        const double v1x = v1->position().x() - bsx;
        const double v1y = v1->position().y() - bsy;
        const double phi1 = atan2(v1y, v1x);
        h_seed_vertex_paird2d->Fill(mag(v0x - v1x, v0y - v1y));
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
        printf("track-sharing: # vertices = %lu. considering vertices #%lu (chi2/dof %.3f prob %.2e, track set", vertices->size(), ivtx[0], v[0]->chi2() / v[0]->ndof(), TMath::Prob(v[0]->chi2(), int(v[0]->ndof())));
        print_track_set(tracks[0], *v[0]);
        printf(") and #%lu (chi2/dof %.3f prob %.2e, track set", ivtx[1], v[1]->chi2() / v[1]->ndof(), TMath::Prob(v[1]->chi2(), int(v[1]->ndof())));
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
          printf(" (%.3f : %.2e | ", nv.chi2() / nv.ndof(), TMath::Prob(nv.chi2(), int(nv.ndof())));
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
          * v[i] = new_vertices[0];
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


  // Debugging plots for track refinement and noshare histos: 
  // These steps are sequential within the loop, but nested in their own `if` statements below.
  // (useful e.g. if one wants to look at the noshare plots during the track refinement)
  if (do_track_refinement || histos_noshare) {
    std::map<reco::TrackRef, int> track_use;
    for (size_t i = 0, ie = vertices->size(); i < ie; ++i) {
      reco::Vertex& v_trf = vertices->at(i);
      const int ntracks = v_trf.nTracks();
      const double vmass = v_trf.p4().mass();
      const double vchi2 = v_trf.normalizedChi2();
      const double vndof = v_trf.ndof();
      const double vx = v_trf.position().x() - bsx;
      const double vy = v_trf.position().y() - bsy;
      const double vz = v_trf.position().z() - bsz;
      const double rho = mag(vx, vy);
      const double phi = atan2(vy, vx);
      const double r = mag(vx, vy, vz);
      for (const auto& tk : vertex_track_set(v_trf)) {
        if (track_use.find(tk) != track_use.end())
          track_use[tk] += 1;
        else
          track_use[tk] = 1;
      }

      if (verbose)
        printf("no-share vertex #%3lu: ntracks: %i chi2/dof: %7.3f dof: %7.3f pos: <%7.3f, %7.3f, %7.3f>  rho: %7.3f  phi: %7.3f  r: %7.3f\n", i, ntracks, vchi2, vndof, vx, vy, vz, rho, phi, r);

      if (do_track_refinement) {

        track_set set_trackrefine_sigmacut_tks;
        std::vector<reco::TransientTrack> trackrefine_sigmacut_ttks;
        track_set set_trackrefine_trimmax_tks;
        std::vector<reco::TransientTrack> trackrefine_trimmax_ttks;
        std::vector<double> trackrefine_trim_ttks_missdist_sig;
        for (auto it = v_trf.tracks_begin(), ite = v_trf.tracks_end(); it != ite; ++it) {

          reco::TransientTrack seed_track;
          seed_track = tt_builder->build(*it.operator*());
          std::pair<bool, Measurement1D> tk_vtx_dist = track_dist(seed_track, v_trf);

          h_noshare_vertex_tkvtxdist_before_do_track_refinement->Fill(tk_vtx_dist.second.value());
          h_noshare_vertex_tkvtxdisterr_before_do_track_refinement->Fill(tk_vtx_dist.second.error());
          h_noshare_vertex_tkvtxdistsig_before_do_track_refinement->Fill(tk_vtx_dist.second.significance());

          if (tk_vtx_dist.second.significance() < trackrefine_sigmacut) {
            set_trackrefine_sigmacut_tks.insert(it->castTo<reco::TrackRef>());
          }
        }

        for (auto tk : set_trackrefine_sigmacut_tks) {
          trackrefine_sigmacut_ttks.push_back(tt_builder->build(tk));
        }

        // if tracks's miss distance significance is larger than trackrefine_sigmacut, we first remove all those tracks and refit a new vertex
        double trackrefine_sigmacut_v0x = v_trf.position().x() - bsx;
        double trackrefine_sigmacut_v0y = v_trf.position().y() - bsy;
        double trackrefine_sigmacut_v0r = mag(trackrefine_sigmacut_v0x, trackrefine_sigmacut_v0y);

        reco::Vertex trackrefine_sigmacut_v;
        for (const TransientVertex& tv : kv_reco_dropin(trackrefine_sigmacut_ttks))
          trackrefine_sigmacut_v = reco::Vertex(tv);
        double trackrefine_sigmacut_vchi2 = trackrefine_sigmacut_v.normalizedChi2();
        h_noshare_trackrefine_sigmacut_vertex_chi2->Fill(trackrefine_sigmacut_vchi2);

        double trackrefine_sigmacut_v1x = trackrefine_sigmacut_v.position().x() - bsx;
        double trackrefine_sigmacut_v1y = trackrefine_sigmacut_v.position().y() - bsy;
        double trackrefine_sigmacut_v1r = mag(trackrefine_sigmacut_v1x, trackrefine_sigmacut_v1y);

        // just to check how the new vertex is shifted by removing tracks by trackrefine_sigmacut
        double sigmacut_vertex_distr = trackrefine_sigmacut_v1r - trackrefine_sigmacut_v0r;
        h_noshare_trackrefine_sigmacut_vertex_distr_shift->Fill(sigmacut_vertex_distr);

        for (auto it = trackrefine_sigmacut_v.tracks_begin(), ite = trackrefine_sigmacut_v.tracks_end(); it != ite; ++it) {
          reco::TransientTrack trackrefine_sigmacut_track;
          trackrefine_sigmacut_track = tt_builder->build(*it.operator*());
          std::pair<bool, Measurement1D> tk_vtx_dist = track_dist(trackrefine_sigmacut_track, trackrefine_sigmacut_v);
          h_noshare_trackrefine_sigmacut_vertex_tkvtxdistsig->Fill(tk_vtx_dist.second.significance());
          trackrefine_trim_ttks_missdist_sig.push_back(tk_vtx_dist.second.significance());
          set_trackrefine_trimmax_tks.insert(it->castTo<reco::TrackRef>());
        }

        int n_trackrefine_trimmax = 0;
        reco::Vertex trackrefine_trimmax_v = trackrefine_sigmacut_v;

        for (auto tk : set_trackrefine_trimmax_tks) {
          trackrefine_trimmax_ttks.push_back(tt_builder->build(tk));
        }

        while (trackrefine_trimmax_ttks.size() > 2 && *std::max_element(trackrefine_trim_ttks_missdist_sig.begin(), trackrefine_trim_ttks_missdist_sig.end()) > trackrefine_trimmax) {
          ++n_trackrefine_trimmax;

          int max_missdist_sig_idx = std::max_element(trackrefine_trim_ttks_missdist_sig.begin(), trackrefine_trim_ttks_missdist_sig.end()) - trackrefine_trim_ttks_missdist_sig.begin();
          // trimmax only one track with the largest miss distance significance at a time
          trackrefine_trimmax_ttks.erase(trackrefine_trimmax_ttks.begin() + max_missdist_sig_idx);
          double trackrefine_trimmax_v0x = trackrefine_trimmax_v.position().x() - bsx;
          double trackrefine_trimmax_v0y = trackrefine_trimmax_v.position().y() - bsy;
          double trackrefine_trimmax_v0r = mag(trackrefine_trimmax_v0x, trackrefine_trimmax_v0y);

          // while we still find a track with max miss distance significance larger than trackrefine_trimmax, we trim it out, namely trimmax, and refit a new vertex until the max miss distance significance is under trackrefine_trimmax
          for (const TransientVertex& tv : kv_reco_dropin(trackrefine_trimmax_ttks))
            trackrefine_trimmax_v = reco::Vertex(tv);

          double trackrefine_trimmax_v1x = trackrefine_trimmax_v.position().x() - bsx;
          double trackrefine_trimmax_v1y = trackrefine_trimmax_v.position().y() - bsy;
          double trackrefine_trimmax_v1r = mag(trackrefine_trimmax_v1x, trackrefine_trimmax_v1y);

          // just to check how the new vertex is shifted by removing a trimmax track
          double trimmax_vertex_distr = trackrefine_trimmax_v1r - trackrefine_trimmax_v0r;
          h_noshare_trackrefine_trimmax_vertex_distr_shift->Fill(trimmax_vertex_distr);

          trackrefine_trim_ttks_missdist_sig.clear();

          for (auto it = trackrefine_trimmax_v.tracks_begin(), ite = trackrefine_trimmax_v.tracks_end(); it != ite; ++it) {
            reco::TransientTrack trackrefine_trimmax_track;
            trackrefine_trimmax_track = tt_builder->build(*it.operator*());
            std::pair<bool, Measurement1D> tk_vtx_dist = track_dist(trackrefine_trimmax_track, trackrefine_trimmax_v);
            trackrefine_trim_ttks_missdist_sig.push_back(tk_vtx_dist.second.significance());
          }

        }

        if (verbose) printf("   trimming the trimmax track from a vertex w/ # of trimming: %i\n", n_trackrefine_trimmax);

        double trackrefine_trimmax_vchi2 = trackrefine_trimmax_v.normalizedChi2();
        h_noshare_trackrefine_trimmax_vertex_chi2->Fill(trackrefine_trimmax_vchi2);

        for (unsigned int j = 0, je = trackrefine_trim_ttks_missdist_sig.size(); j < je; ++j) {
          h_noshare_trackrefine_trimmax_vertex_tkvtxdistsig->Fill(trackrefine_trim_ttks_missdist_sig[j]);
        }

        // the end of track refinement in two steps -- (1) sigmacut and (2) trimmax
        // we replace the noshare vertex by the vertex after the track refinement
        v_trf = trackrefine_trimmax_v;
      }


      if (histos_noshare) {
        h_noshare_vertex_ntracks->Fill(ntracks);

        for (auto it = v_trf.tracks_begin(), ite = v_trf.tracks_end(); it != ite; ++it) {
          h_noshare_vertex_track_weights->Fill(v_trf.trackWeight(*it));

          reco::TransientTrack seed_track;
          seed_track = tt_builder->build(*it.operator*());
          std::pair<bool, Measurement1D> tk_vtx_dist = track_dist(seed_track, v_trf);
          h_noshare_vertex_tkvtxdist->Fill(tk_vtx_dist.second.value());
          h_noshare_vertex_tkvtxdisterr->Fill(tk_vtx_dist.second.error());
          h_noshare_vertex_tkvtxdistsig->Fill(tk_vtx_dist.second.significance());
        }

		h_noshare_vertex_mass->Fill(vmass);
        h_noshare_vertex_chi2->Fill(vchi2);
        h_noshare_vertex_ndof->Fill(vndof);
        h_noshare_vertex_x->Fill(vx);
        h_noshare_vertex_y->Fill(vy);
        h_noshare_vertex_rho->Fill(rho);
        h_noshare_vertex_phi->Fill(phi);
        h_noshare_vertex_z->Fill(vz);
        h_noshare_vertex_r->Fill(r);

        for (size_t j = i + 1, je = vertices->size(); j < je; ++j) {
          const reco::Vertex& vj = vertices->at(j);
          const double vjx = vj.position().x() - bsx;
          const double vjy = vj.position().y() - bsy;
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


  //////////////////////////////////////////////////////////////////////////////////////////////
  // Merge vertices that are still "close" in 2D, aka "loose" merging (typically off by default)
  //////////////////////////////////////////////////////////////////////////////////////////////
  if (verbose)
    printf("fun2! before 'loose' merging loop, # vertices = %lu\n", vertices->size());

  if (resolve_split_vertices_loose) {

    if (merge_anyway_sig > 0 || merge_anyway_dist > 0) {
      double v0x;
      double v0y;
      double phi0;

      for (v[0] = vertices->begin(); v[0] != vertices->end(); ++v[0]) {
        ivtx[0] = v[0] - vertices->begin();

        double v1x;
        double v1y;
        double phi1;

        for (v[1] = v[0] + 1; v[1] != vertices->end(); ++v[1]) {

          ivtx[1] = v[1] - vertices->begin();

          if (verbose)
            printf("close-merge: # vertices = %lu. considering vertices #%lu (ntk = %i) and #%lu (ntk = %i):", vertices->size(), ivtx[0], v[0]->nTracks(), ivtx[1], v[1]->nTracks());

          Measurement1D v_dist = vertex_dist(*v[0], *v[1]);
          if (verbose)
            printf("   vertex dist (2d? %i) %7.3f  sig %7.3f\n", use_2d_vertex_dist, v_dist.value(), v_dist.significance());

          v0x = v[0]->x() - bsx;
          v0y = v[0]->y() - bsy;
          phi0 = atan2(v0y, v0x);
          v1x = v[1]->x() - bsx;
          v1y = v[1]->y() - bsy;
          phi1 = atan2(v1y, v1x);

          if (v_dist.value() < merge_anyway_dist || v_dist.significance() < merge_anyway_sig) {
            if (verbose)
              printf("          dist < %7.3f || sig < %7.3f, breaking to merge\n", merge_anyway_dist, merge_anyway_sig);

            std::vector<reco::TransientTrack> ttks;

            for (int i = 0; i < 2; ++i) {
              for (auto tk : vertex_track_set(*v[i])) {
                ttks.push_back(tt_builder->build(tk));
              }
            }

            reco::VertexCollection merged_vertices;
            for (const TransientVertex& tv : kv_reco_dropin(ttks)) {
              merged_vertices.push_back(reco::Vertex(tv));

              for (auto it = merged_vertices[0].tracks_begin(), ite = merged_vertices[0].tracks_end(); it != ite; ++it) {
                reco::TransientTrack seed_track;
                seed_track = tt_builder->build(*it.operator*());
                std::pair<bool, Measurement1D> tk_vtx_dist = track_dist(seed_track, merged_vertices[0]);
              }
            }

            if (verbose) {
              printf("      got %lu new vertices out of the av fit\n", merged_vertices.size());
              printf("      these track sets:");
              for (const auto& nv : merged_vertices) {
                printf(" (");
                print_track_set(nv);
                printf(" ),");
              }
              printf("\n");
            }

            if (merged_vertices.size() == 1) {
              if (verbose) {
                printf(" sv2ddist between a merging pair is %7.3f \n", v_dist.value());
                printf(" |dPhi(vtx0,vtx1) between a merging pair is %4.3f \n", fabs(reco::deltaPhi(phi0, phi1)));
                printf(" # of tracks per vtx0 is %u \n", v[0]->nTracks());
                printf(" # of tracks per vtx1 is %u \n", v[1]->nTracks());
                printf(" ---------------- merge the two vertices if chi2/dof < 5 ----------------- \n");
                printf(" # of tracks per a new merged vertex is %u \n", merged_vertices[0].nTracks());
              }

              //std::cout << "check no mem out of ranges (before) : " << v[1] - vertices->begin() << std::endl;
              *v[0] = merged_vertices[0];
              //std::cout << "check no mem out of ranges (after) : " << v[1] - vertices->begin() << std::endl;

              v[1] = vertices->erase(v[1]) - 1;
            }
          }
        }
      }

      // Printouts of new vertex distance when using verbose mode
      if (verbose) {
        std::vector<reco::Vertex>::iterator nv[2];
        for (nv[0] = vertices->begin(); nv[0] != vertices->end(); ++nv[0]) {
          for (nv[1] = nv[0] + 1; nv[1] != vertices->end(); ++nv[1]) {

            Measurement1D nv_dist = vertex_dist(*nv[0], *nv[1]);
            printf("  new vertex dist (2d? %i) %7.3f  sig %7.3f\n", use_2d_vertex_dist, nv_dist.value(), nv_dist.significance());
          }
        }
      }
    }
  }


  //////////////////////////////////////////////////////////////////////
  // Drop tracks that "move" the vertex too much by refitting without each track.
  //////////////////////////////////////////////////////////////////////
  if (max_nm1_refit_dist3 > 0 || max_nm1_refit_distz > 0) {
    std::vector<int> refit_count(vertices->size(), 0);

    int iv = 0;
    for (v[0] = vertices->begin(); v[0] != vertices->end(); ++v[0], ++iv) {
      if (max_nm1_refit_count > 0 && refit_count[iv] >= max_nm1_refit_count)
        continue;

      const track_vec tks = vertex_track_vec(*v[0]);
      const size_t ntks = tks.size();
      if (ntks < 3)
        continue;

      if (verbose) {
        printf("doing n-%i refit on vertex at %7.4f %7.4f %7.4f with %lu tracks\n", refit_count[iv] + 1, v[0]->x(), v[0]->y(), v[0]->z(), ntks);
        for (size_t i = 0; i < ntks; ++i)
          printf("  refit %lu will drop tk pt %7.4f +- %7.4f eta %7.4f +- %7.4f phi %7.4f +- %7.4f dxy %7.4f +- %7.4f dz %7.4f +- %7.4f\n", i, tks[i]->pt(), tks[i]->ptError(), tks[i]->eta(), tks[i]->etaError(), tks[i]->phi(), tks[i]->phiError(), tks[i]->dxy(), tks[i]->dxyError(), tks[i]->dz(), tks[i]->dzError());
      }

      std::vector<reco::TransientTrack> ttks(ntks - 1);
      for (size_t i = 0; i < ntks; ++i) {
        for (size_t j = 0; j < ntks; ++j)
          if (j != i)
            ttks[j - (j >= i)] = tt_builder->build(tks[j]);
        reco::Vertex vnm1(TransientVertex(kv_reco->vertex(ttks)));
        const double dist3_2 = mag2(vnm1.x() - v[0]->x(), vnm1.y() - v[0]->y(), vnm1.z() - v[0]->z());
        const double distz = mag(vnm1.z() - v[0]->z());
        if (verbose) printf("  refit %lu chi2 %7.4f vtx %7.4f %7.4f %7.4f dist3 %7.4f distz %7.4f\n", i, vnm1.chi2(), vnm1.x(), vnm1.y(), vnm1.z(), sqrt(dist3_2), distz);

        if (vnm1.chi2() < 0 ||
            (max_nm1_refit_dist3 > 0 && mag2(vnm1.x() - v[0]->x(), vnm1.y() - v[0]->y(), vnm1.z() - v[0]->z()) > pow(max_nm1_refit_dist3, 2)) ||
            (max_nm1_refit_distz > 0 && distz > max_nm1_refit_distz)) {
          if (verbose) {
            printf("    replacing");
            if (refit_count[iv] < max_nm1_refit_count - 1)
              printf(" and reconsidering");
            printf("\n");
          }

          *v[0] = vnm1;
          ++refit_count[iv];
          --v[0], --iv;
          break;
        }
      }
    }
    iv = 0; //some vertices after dz refiting have normalized chi2 > 5
    for (v[0] = vertices->begin(); v[0] != vertices->end(); ++v[0], ++iv) {
       if ((*v[0]).chi2() > 5) {
         v[0] = vertices->erase(v[0]) - 1;
         continue;
       }
    }
  }
  if (histos_output_afterdzfit){
    fillCommonOutputHists(vertices, fake_bs_vtx, tt_builder, stepEnum::afterdzfit);
  }


  /////////////////////////////////////////////////////////////////////////////////////////////////////
  // Merge every pair of output vertices that satisfy the following criteria to resolve split-vertices:
  //   - >=2trk/vtx
  //   - dBV > 100 um
  //   - |dPhi(vtx0,vtx1)| < 0.5 
  //   - svdist2d < 300 um
  // Note that the merged vertex must pass chi2/dof < 5
  ////////////////////////////////////////////////////////////////////////////////////////////////////
  if (resolve_split_vertices_tight) {
    reco::VertexCollection potential_merged_vertices;

    for (v[0] = vertices->begin(); v[0] != vertices->end(); ++v[0]) {

      track_set tracks[2];
      tracks[0] = vertex_track_set(*v[0]);

      bool merge = false;
      for (v[1] = v[0] + 1; v[1] != vertices->end(); ++v[1]) {
        if (vertices->size() >= 2 && v[0]->nTracks() >= 2 && v[1]->nTracks() >= 2) {

          tracks[1] = vertex_track_set(*v[1]);

          Measurement1D v_dist = vertex_dist_2d.distance(*v[0], *v[1]);

          Measurement1D dBV0_Meas1D = vertex_dist_2d.distance(*v[0], fake_bs_vtx);
          double dBV0 = dBV0_Meas1D.value();

          Measurement1D dBV1_Meas1D = vertex_dist_2d.distance(*v[1], fake_bs_vtx);
          double dBV1 = dBV1_Meas1D.value();

          double v0x = v[0]->x() - bsx;
          double v0y = v[0]->y() - bsy;

          double phi0 = atan2(v0y, v0x);

          double v1x = v[1]->x() - bsx;
          double v1y = v[1]->y() - bsy;

          double phi1 = atan2(v1y, v1x);

          if (fabs(reco::deltaPhi(phi0, phi1)) < 0.5 && v_dist.value() < 0.0300 && dBV0 > 0.0100 && dBV1 > 0.0100) {
            track_set tracks_to_fit;
            for (int i = 0; i < 2; ++i)
              for (auto tk : tracks[i])
                tracks_to_fit.insert(tk);
            std::vector<reco::TransientTrack> ttks;
            for (auto tk : tracks_to_fit)
              ttks.push_back(seed_tracks[seed_track_ref_map[tk]]);

            if (investigate_merged_vertices) {
              std::vector<TransientVertex> tv(1, kv_reco->vertex(ttks));
              potential_merged_vertices.push_back(reco::Vertex(tv[0]));
              //std::cout << "ntrack in potental merged: " << potential_merged_vertices.back().nTracks() << std::endl;
            }

            reco::VertexCollection merged_vertices;
            for (const TransientVertex& tv : kv_reco_dropin(ttks)) {
              merged_vertices.push_back(reco::Vertex(tv));
            }

            if (merged_vertices.size() == 1 && vertex_track_set(merged_vertices[0], 0) == tracks_to_fit) {

              merge = true;

              if (verbose) {
                printf(" sv2ddist between a merging pair is %7.3f \n", v_dist.value());
                printf(" |dPhi(vtx0,vtx1) between a merging pair is %4.3f \n", fabs(reco::deltaPhi(phi0, phi1)));
                printf(" # of tracks per vtx0 is %u \n", v[0]->nTracks());
                printf(" # of tracks per vtx1 is %u \n", v[1]->nTracks());
                printf(" ---------------- merge the two vertices if chi2/dof < 5 ----------------- \n");
                printf(" # of tracks per a new merged vertex is %u \n", merged_vertices[0].nTracks());
              }

              v[1] = vertices->erase(v[1]) - 1; // (1) erase and point the iterator at the previous entry
              *v[0] = reco::Vertex(merged_vertices[0]); // (2) updated v[0] (ok to use v[0] after the erase(v[1]) because v[0] is by construction before v[1])
            }
          }
        }
      }
	  // going through all the pairs of of v[1] and a fixed v[0] for merging, if merge happens (1) each v[1] is erased (2) v[0] is updated (recurring until exit loop) (3) reset the combination again
	  if (merge)
		  v[0] = vertices->begin() - 1; // (3) reset the combination if a valid merge happens 
    }

    if (investigate_merged_vertices) {
      for (size_t i = 0, ie = potential_merged_vertices.size(); i < ie; ++i) {
        reco::Vertex vpm = potential_merged_vertices[i];
        const int ntracks = vpm.nTracks();
        const double vchi2 = vpm.normalizedChi2();
        Measurement1D dBV_Meas1D = vertex_dist_2d.distance(vpm, fake_bs_vtx);
        double dBV = dBV_Meas1D.value();
        double bs2derr = dBV_Meas1D.error();

        // n-1 plots of the various cuts used (ntk, dBV, bs2derr, chi2)
        if (ntracks >= 5 && dBV > 0.01 && bs2derr < 0.0025) {
          h_output_aftermerge_potential_merged_vertex_nm1_chi2->Fill(vchi2);
        }
        if (vchi2 < 5 && dBV > 0.01 && bs2derr < 0.0025) {
          h_output_aftermerge_potential_merged_vertex_nm1_ntracks->Fill(ntracks);
        }
        if (vchi2 < 5 && ntracks >= 5 && bs2derr < 0.0025) {
          h_output_aftermerge_potential_merged_vertex_nm1_bsbs2ddist->Fill(dBV);
        }
        if (vchi2 < 5 && ntracks >= 5 && dBV > 0.01) {
          h_output_aftermerge_potential_merged_vertex_nm1_bs2derr->Fill(bs2derr);
        }
      }
    }
  }

  if (histos_output_aftermerge) {
    fillCommonOutputHists(vertices, fake_bs_vtx, tt_builder, stepEnum::aftermerge);
  }

  //////////////////////////////////////////////////////////////////////
  // Shared-jet mitigation with the following procedure:
  //   -   make a set of vertices that have been sorted by ascending number of tracks per vertex
  //   - 	 loop thru a pair of >=3trk vertices and check whether they share {1,1} and {1,n} shared jets or not 
  //   -   In the double loop: check one vertex at a time (sv0) and remove a lone track to the jet if it is pointing backward from its vertex (apply dphi < pi/2)
  //   -   In the double loop: assign a new fitted vertex to the one resolving shared jets
  //   -   loop thru a set of vertices after the mitigation to clean up a vertex with just one track
  // Note that:
  //   - {1,1} shared jets have exactly one track to the jet from both vertices
  //   - {1,n} shared jets have one of the two vertices contributing exactly one track to the jet
  //////////////////////////////////////////////////////////////////////
  if (resolve_shared_jets) {
    edm::Handle<pat::JetCollection> jets;
    event.getByToken(shared_jet_token, jets);

    std::vector<std::vector<size_t> > sv_total_track_which_trkidx; // a vector of each sv's track indx
    // we need ascending vectors of vertices based on their total tracks in order to speed up the shared-jet algorithm because the less-track vertex is more likely to be removed first after a single shared-jet track is removed, reducing the size of vertices to loop thru.  
    std::vector<unsigned int> sv_ascending_total_ntrack; // a vector of ascending number of total tracks per vertex 
    std::vector<size_t> sv_ascending_vtxidx; // a vector of vertex index corresponding to the order of ascending total tracks in sv_ascending_total_ntrack 


    std::vector<std::vector<size_t> > sv_match_trkidx; // a vector of each sv's track indx to keep a record of a track matching with a jet  
    std::vector<std::vector<size_t> > sv_match_jetidx; // a vector of each sv's jet indx to keep a record of a jet that matches with a track at the same iterator  

    std::vector<track_vec> sv_total_track_which_trk_vec; // a vector of each sv's track_vec object 

    int n_output_aftersharedjets_onetracks = 0;

    size_t vtxidx = 0;
    for (v[0] = vertices->begin(); v[0] != vertices->end(); ++v[0]) {
      std::vector<size_t> track_idx;
      std::vector<size_t> tracktojet_which_trkidx;
      std::vector<size_t> tracktojet_which_jetidx;
      track_vec tks = vertex_track_vec(*v[0]);
      sv_total_track_which_trk_vec.push_back(tks);
      for (size_t i = 0; i < tks.size(); ++i) {
        const reco::TrackRef& itk = tks[i];
        track_idx.push_back(i);
        for (size_t j = 0; j < jets->size(); ++j) {
          if (match_track_jet(*itk, (*jets)[j], *jets, j)) {
            tracktojet_which_trkidx.push_back(i);
            tracktojet_which_jetidx.push_back(j);
            if (verbose)
              printf(" track %u matched with a jet %lu \n", tks[i].key(), j);
          }
        }
      }

      unsigned int ntracks = track_idx.size();

      if (vtxidx == 0) { // start creating the ascening vector of sorted number of total tracks and its corresponding vertex index
        sv_ascending_total_ntrack.push_back(ntracks);
        sv_ascending_vtxidx.push_back(vtxidx);
      }
      else { // the algorithm continues after the first vertex is added to the vector 

        std::vector<unsigned int>::iterator it_ntracks = sv_ascending_total_ntrack.end();
        std::vector<size_t>::iterator it_vtx = sv_ascending_vtxidx.end();
        // finding an iterator that points to a position that ntrack is just less than or equal to itself from the back to the front
        while (it_ntracks != sv_ascending_total_ntrack.begin() && ntracks <= sv_ascending_total_ntrack[std::distance(sv_ascending_total_ntrack.begin(), it_ntracks)-1])
        {
          --it_ntracks;
          --it_vtx;
        }
        // adding a vertex at the end if it has higher ntrack. otherwise, insert it before an iterator pointing to a position that this ntrack is smaller than itself 
        if (it_ntracks == sv_ascending_total_ntrack.end() && ntracks > sv_ascending_total_ntrack[std::distance(sv_ascending_total_ntrack.begin(), it_ntracks)]) {
          sv_ascending_total_ntrack.push_back(ntracks);
          sv_ascending_vtxidx.push_back(vtxidx);
        }

        else {
          sv_ascending_total_ntrack.insert(it_ntracks, ntracks);
          sv_ascending_vtxidx.insert(it_vtx, vtxidx);
        }
      }

      sv_total_track_which_trkidx.push_back(track_idx);
      sv_match_trkidx.push_back(tracktojet_which_trkidx);
      sv_match_jetidx.push_back(tracktojet_which_jetidx);
      vtxidx++;
    }


    if (vertices->size() >= 2) {
      // double for loops to double counts the sv0 and sv1 pairing. The code always remove 'lone shared tracks' from (multiple) special shared jets to sv0 in each round as long as they are not compatible to sv0. Otherwise, the sv1 from the earlier round will be considered again (double count) to have the tracks being removed or not. 
      for (size_t vtxi = 0; vtxi < sv_ascending_vtxidx.size(); vtxi++) {
        const size_t vtxidx0 = sv_ascending_vtxidx[vtxi];
        reco::Vertex& sv0 = vertices->at(vtxidx0);
        double sv0x = sv0.x() - bsx;
        double sv0y = sv0.y() - bsy;
        double phi0 = atan2(sv0y, sv0x);
        if (verbose){
          printf("-----loop # %lu ----- \n", vtxi);
          printf(" sv0'idx: %lu \n", vtxidx0);
          printf(" sv0'ntrack: %u \n", sv0.nTracks());
        }
        for (size_t vtxj = 0; vtxj < sv_ascending_vtxidx.size(); vtxj++) {
          if (vtxi == vtxj) continue;
          const size_t vtxidx1 = sv_ascending_vtxidx[vtxj];
          reco::Vertex& sv1 = vertices->at(vtxidx1);
          if (verbose){
            printf(" sv1'idx: %lu \n", vtxidx1);
            printf(" sv1'ntrack: %u \n", sv1.nTracks());
          }

          // only consider a pair with at least 3 tracks per vertex
          if (sv0.nTracks() > 2 && sv1.nTracks() > 2) {

            std::pair<bool, std::vector<std::vector<size_t>>> sharedjet_tool = sharedjets(vtxidx0, vtxidx1, sv_match_jetidx, sv_match_trkidx);

            // loop thru {1,1}+{1,n} nsharedjets and remove just one shared track from v0 if a |dPhi(v0,one shared track)| > pi/2
            if (sharedjet_tool.first) {
              if (verbose)
                printf("start shj implementation to {1,1} and {1,n} \n");
              std::vector<std::vector<size_t>> sv_lonesharedtrack_trkidx = sharedjet_tool.second;
              std::vector<size_t> sv0_lonesharedtrack_trkidx = sv_lonesharedtrack_trkidx[0];
              std::vector<size_t> sv1_lonesharedtrack_trkidx = sv_lonesharedtrack_trkidx[1];
              if (verbose) {
                printf("size of set of lone shared tracks per sv0: %lu \n", sv0_lonesharedtrack_trkidx.size());
                printf("size of set of lone shared tracks per sv1: %lu \n", sv1_lonesharedtrack_trkidx.size());
              }
              for (size_t k = 0; k < sv0_lonesharedtrack_trkidx.size(); k++) {
                track_vec tks_sv0 = sv_total_track_which_trk_vec[vtxidx0];
                size_t idx = sv0_lonesharedtrack_trkidx[k];
                h_resolve_shared_jets_lonetrkvtx_dphi->Fill(fabs(reco::deltaPhi(tks_sv0[idx]->phi(), phi0)));

                // drop the lone track pointing backwards from the vertex direction!
                if (fabs(reco::deltaPhi(tks_sv0[idx]->phi(), phi0)) > M_PI / 2) {
                  eraseElement(sv_total_track_which_trkidx[vtxidx0], idx);
                }
              }
              if (verbose) {
                printf("sv0'idx: %lu with ntrack before: %u",vtxidx0, sv0.nTracks());
                printf("sv1'idx: %lu with ntrack before: %u",vtxidx1, sv1.nTracks());
              }

              track_set  sv0_resolved_sharedtracks_trkset;
              for (unsigned int trk0_i = 0; trk0_i < sv_total_track_which_trkidx[vtxidx0].size(); ++trk0_i) {
                size_t idx = sv_total_track_which_trkidx[vtxidx0][trk0_i];
                track_vec tks_sv0 = sv_total_track_which_trk_vec[vtxidx0];
                sv0_resolved_sharedtracks_trkset.insert(tks_sv0[idx]);

              }
              std::vector<reco::TransientTrack> sv0_resolved_sharedtracks_ttks;
              for (auto tk : sv0_resolved_sharedtracks_trkset)
                sv0_resolved_sharedtracks_ttks.push_back(tt_builder->build(tk));

              reco::Vertex sv0_resolved_sharedtracks;

              for (const TransientVertex& tv : kv_reco_dropin(sv0_resolved_sharedtracks_ttks))
                sv0_resolved_sharedtracks = reco::Vertex(tv);

              sv0 = sv0_resolved_sharedtracks; // update sv0 after non-compatible 'lone shared tracks' from some special shared jets are removed 
              if (verbose) {
                printf("sv0'idx: %lu with ntrack after: %u",vtxidx0, sv0.nTracks());
                printf("sv1'idx: %lu with ntrack after: %u",vtxidx1, sv1.nTracks());
              }
            }
          }
        }
      }
    }

    for (v[0] = vertices->begin(); v[0] != vertices->end(); ++v[0]) {
      track_set tracks[2];
      ivtx[0] = v[0] - vertices->begin();
      tracks[0] = vertex_track_set(*v[0]);

      if (tracks[0].size() < 2) {
        if (verbose)
          throw cms::Exception("1-trk vtx in Vertexer") << "at vertex index: " << ivtx[0];
        v[0] = vertices->erase(v[0]) - 1;
        ++n_output_aftersharedjets_onetracks;
        continue;
      }

      if (tracks[0].size() < v[0]->nTracks()) {
        throw cms::Exception("inconsistent total tracks per vertex in Vertexer") << "please check for duplicated tracks ";
        std::vector<reco::TransientTrack> sv_nonduplicate_ttks;
        for (const reco::TrackRef& itk : vertex_track_set(*v[0])) {
          if (itk.isNonnull())
            sv_nonduplicate_ttks.push_back(tt_builder->build(itk));
        }

        for (const TransientVertex& tv : kv_reco_dropin(sv_nonduplicate_ttks))
          *v[0] = reco::Vertex(tv);
      }
    }

    if (histos_output_aftersharedjets) {
      fillCommonOutputHists(vertices, fake_bs_vtx, tt_builder, stepEnum::aftersharedjets);
      h_output_aftersharedjets_n_onetracks->Fill(n_output_aftersharedjets_onetracks);
    }
  }


  //////////////////////////////////////////////////////////////////////
  // Put the output.
  //////////////////////////////////////////////////////////////////////

  finish(event, seed_tracks, std::move(vertices), std::move(vpeffs), vpeffs_tracks);
}

// this function will only return false only if shared jets between the given vertex pair contribute multiple shared-jet tracks to 'both' vertices (not a special case we consider).   
std::pair<bool, std::vector<std::vector<size_t>>> MFVVertexer::sharedjets(const size_t vtx0idx, const size_t vtx1idx, const std::vector < std::vector<size_t>>& sv_match_jetidx, const std::vector < std::vector<size_t>>& sv_match_trkidx) {

  bool shared_jet = hasCommonElement(sv_match_jetidx[vtx0idx], sv_match_jetidx[vtx1idx]);

  std::vector<std::vector<size_t>> sv_match_special_sharedjet_trkidx;
  std::vector<size_t> sv0_match_special_sharedjet_trkidx;
  std::vector<size_t> sv1_match_special_sharedjet_trkidx;

  if (shared_jet) {

    size_t nsharedjets = 0;

    std::vector<std::vector<size_t>> sv_match_temp_jetidx = sv_match_jetidx;
    std::vector<std::vector<size_t>> sv0_match_sharedjet_trkidx;
    std::vector<std::vector<size_t>> sv1_match_sharedjet_trkidx;

    std::vector<size_t> sv0_match_jetidx = sv_match_jetidx[vtx0idx];
    std::vector<size_t> sv0_match_trkidx = sv_match_trkidx[vtx0idx];

    std::vector<size_t> sv1_match_jetidx = sv_match_jetidx[vtx1idx];
    std::vector<size_t> sv1_match_trkidx = sv_match_trkidx[vtx1idx];

    while (hasCommonElement(sv_match_temp_jetidx[vtx0idx], sv_match_temp_jetidx[vtx1idx])) {
      nsharedjets++;
      std::vector<size_t>::iterator sharedjet_it = getFirstCommonElement(sv_match_temp_jetidx[vtx0idx], sv_match_temp_jetidx[vtx1idx]);
      size_t sharedjet_it_idx = std::distance(sv_match_temp_jetidx[vtx0idx].begin(), sharedjet_it);
      size_t jet_index = sv_match_temp_jetidx[vtx0idx].at(sharedjet_it_idx);

      eraseElement(sv_match_temp_jetidx[vtx0idx], jet_index);
      eraseElement(sv_match_temp_jetidx[vtx1idx], jet_index);

      // start collecting shared tracks of sv0 for each shared jet
      createSetofSharedJetTracks(sv0_match_sharedjet_trkidx, sv0_match_special_sharedjet_trkidx, sv0_match_trkidx, sv0_match_jetidx, jet_index);

      // start collecting shared tracks of sv1 for each shared jet
      createSetofSharedJetTracks(sv1_match_sharedjet_trkidx, sv1_match_special_sharedjet_trkidx, sv1_match_trkidx, sv1_match_jetidx, jet_index);

    }
    sv_match_special_sharedjet_trkidx.push_back(sv0_match_special_sharedjet_trkidx);
    sv_match_special_sharedjet_trkidx.push_back(sv1_match_special_sharedjet_trkidx);
  }
  //boolean below is a selector for mitigating only 1:1 and 1:n shared-jet cases. Feel free to set it to true for considering all shared-jet cases including the n:m case
  bool shared_jet_specialcase = (sv0_match_special_sharedjet_trkidx.size() != 0 || sv1_match_special_sharedjet_trkidx.size() != 0);
  return std::pair<bool, std::vector<std::vector<size_t>>>(
      shared_jet_specialcase,
      sv_match_special_sharedjet_trkidx);
}

bool MFVVertexer::hasCommonElement(std::vector<size_t> vec0, std::vector<size_t> vec1) {
  return getFirstCommonElement(vec0, vec1) != vec0.end();
}

std::vector<size_t>::iterator MFVVertexer::getFirstCommonElement(std::vector<size_t>& vec0, std::vector<size_t>& vec1) {
  return std::find_first_of(vec0.begin(), vec0.end(), vec1.begin(), vec1.end());
}

template <typename T>
void MFVVertexer::eraseElement(std::vector<T>& vec, size_t idx) {
  vec.erase(std::remove(vec.begin(), vec.end(), idx), vec.end());
  return;
}


void MFVVertexer::createSetofSharedJetTracks(std::vector<std::vector<size_t>>& vec_sharedjet_track_idx, std::vector<size_t>& vec_special_sharedjet_track_idx, std::vector<size_t>& vec_all_track_idx, std::vector<size_t>& vec_sharedjet_idx, size_t sharedjet_idx){
  std::vector<size_t> temp_match_trkidx_per_sharedjet_idx = {};
  for (size_t k = 0; k < vec_sharedjet_idx.size(); k++) // since sharedjet_idx and all_track_idx vectors correspond one-to-one, for each shared jet index we can create a temporary set of track idx matching to it 
    if (vec_sharedjet_idx[k] == sharedjet_idx) {temp_match_trkidx_per_sharedjet_idx.push_back(vec_all_track_idx[k]);}
  vec_sharedjet_track_idx.push_back(temp_match_trkidx_per_sharedjet_idx);
  if (temp_match_trkidx_per_sharedjet_idx.size() == 1) { // this is a condition of a lone shared-jet track per jet per vertex 
    vec_special_sharedjet_track_idx.push_back(temp_match_trkidx_per_sharedjet_idx[0]);
  }
  return;
}

bool MFVVertexer::match_track_jet(const reco::Track& tk, const pat::Jet& matchjet, const pat::JetCollection& jets, const size_t& idx) {

  if (verbose) {
    std::cout << "jet track matching..." << std::endl;
    std::cout << "  target track pt " << tk.pt() << " eta " << tk.eta() << " phi " << tk.phi() << std::endl;
  }

  // Arbitrary threshold, but idea is to minimize [1+delta(pT)] * [1+delta(eta)] * [1+delta(phi)] in order to match the track to the jet
  double match_thres = 1.3;
  size_t jet_index = 255;
  for (size_t j = 0; j < jets.size(); ++j) {
    for (size_t idau = 0, idaue = jets[j].numberOfDaughters(); idau < idaue; ++idau) {

      // Note that the usage of both PFCandidates and PackedCandidates is copied from EventProducer.cc; see comments there for subtleties related to this (largely AOD vs. MiniAOD)
      const reco::Candidate* dau = jets[j].daughter(idau);
      if (dau->charge() == 0)
        continue;
      const reco::Track * jtk = 0;
      const reco::PFCandidate * pf = dynamic_cast<const reco::PFCandidate*>(dau);
      if (pf) {
        const reco::TrackRef& r = pf->trackRef();
        if (r.isNonnull())
          jtk = &*r;
      }
      else {
        const pat::PackedCandidate* pk = dynamic_cast<const pat::PackedCandidate*>(dau);
        if (pk && pk->charge() != 0 && pk->hasTrackDetails())
          jtk = &pk->pseudoTrack();
      }
      if (jtk) {
        double a = fabs(tk.pt() - fabs(jtk->charge() * jtk->pt())) + 1;
        double b = fabs(tk.eta() - jtk->eta()) + 1;
        double c = fabs(tk.phi() - jtk->phi()) + 1;
        if (verbose)
          std::cout << "  jet track pt " << jtk->pt() << " eta " << jtk->eta() << " phi " << jtk->phi() << " match abc " << a * b * c << std::endl;
        if (a * b * c < match_thres) {
          match_thres = a * b * c;
          jet_index = j;
        }
      }
    }
  }
  if (jet_index == idx){
    return true;
  }

  return false;
}

void MFVVertexer::fillCommonOutputHists(std::unique_ptr<reco::VertexCollection>& vertices, const reco::Vertex& fake_bs_vtx, edm::ESHandle<TransientTrackBuilder>& tt_builder, size_t step) {

  std::map<reco::TrackRef, int> track_use;
  int count_5trk_vertices = 0;

  const double bsx = fake_bs_vtx.position().x();
  const double bsy = fake_bs_vtx.position().y();
  const double bsz = fake_bs_vtx.position().z();

  for (size_t i = 0, ie = vertices->size(); i < ie; ++i) {
    const reco::Vertex& v = vertices->at(i);
    const int ntracks = v.nTracks();
    const double vmass = v.p4().mass();
    const double vchi2 = v.normalizedChi2();
    const double vndof = v.ndof();
    const double vx = v.position().x() - bsx;
    const double vy = v.position().y() - bsy;
    const double vz = v.position().z() - bsz;
    const double rho = mag(vx, vy);
    const double phi = atan2(vy, vx);
    const double r = mag(vx, vy, vz);
    for (const auto& tk : vertex_track_set(v)) {
      if (track_use.find(tk) != track_use.end())
        track_use[tk] += 1;
      else
        track_use[tk] = 1;
    }

    hs_output_vertex_ntracks[step]->Fill(ntracks);
    if (ntracks >= 5) {
      count_5trk_vertices++;
      Measurement1D dBV_Meas1D = vertex_dist_2d.distance(v, fake_bs_vtx);
      double dBV = dBV_Meas1D.value();
      double bs2derr = dBV_Meas1D.error();

      if (vchi2 < 5 && ntracks >= 5 && bs2derr < 0.0025) {
        hs_output_vertex_nm1_bsbs2ddist[step]->Fill(dBV);
      }
      if (vchi2 < 5 && ntracks >= 5 && dBV > 0.01) {
        hs_output_vertex_nm1_bs2derr[step]->Fill(bs2derr);
      }
    }

    for (auto it = v.tracks_begin(), ite = v.tracks_end(); it != ite; ++it) {
      hs_output_vertex_track_weights[step]->Fill(v.trackWeight(*it));

      reco::TransientTrack seed_track;
      seed_track = tt_builder->build(*it.operator*());
      std::pair<bool, Measurement1D> tk_vtx_dist = track_dist(seed_track, v);
      hs_output_vertex_tkvtxdist[step]->Fill(tk_vtx_dist.second.value());
      hs_output_vertex_tkvtxdisterr[step]->Fill(tk_vtx_dist.second.error());
      hs_output_vertex_tkvtxdistsig[step]->Fill(tk_vtx_dist.second.significance());
    }

	hs_output_vertex_mass[step]->Fill(vmass);
    hs_output_vertex_chi2[step]->Fill(vchi2);
    hs_output_vertex_ndof[step]->Fill(vndof);
    hs_output_vertex_x[step]->Fill(vx);
    hs_output_vertex_y[step]->Fill(vy);
    hs_output_vertex_rho[step]->Fill(rho);
    hs_output_vertex_phi[step]->Fill(phi);
    hs_output_vertex_z[step]->Fill(vz);
    hs_output_vertex_r[step]->Fill(r);

    for (size_t j = i + 1, je = vertices->size(); j < je; ++j) {
      const reco::Vertex& vj = vertices->at(j);
      const double vjx = vj.position().x() - bsx;
      const double vjy = vj.position().y() - bsy;
      const double phij = atan2(vjy, vjx);
      Measurement1D v_dist = vertex_dist(vj, v);
      hs_output_vertex_paird2d[step]->Fill(mag(vx - vjx, vy - vjy));
      hs_output_vertex_paird2dsig[step]->Fill(v_dist.significance());
      hs_output_vertex_pairdphi[step]->Fill(reco::deltaPhi(phi, phij));
    }
  }

  hs_n_at_least_5trk_output_vertices[step]->Fill(count_5trk_vertices);
}

DEFINE_FWK_MODULE(MFVVertexer);
