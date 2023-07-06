#include "TH2.h"
#include "TMath.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaPhi.h"
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

  void finish(edm::Event&, const std::vector<reco::TransientTrack>&, std::unique_ptr<reco::VertexCollection>, std::unique_ptr<VertexerPairEffs>, const std::vector<std::pair<track_set, track_set>>&);

  enum stepEnum{beforedzfit, afterdzfit, N_STEPS};
  std::vector<TString> stepStrs = {"beforedzfit", "afterdzfit", "N_STEPS"};
  void fillCommonOutputHists(std::unique_ptr<reco::VertexCollection>& vertices, const reco::Vertex& fake_bs_vtx, edm::ESHandle<TransientTrackBuilder>& tt_builder, size_t step);
  
  template <typename T>
  void print_track_set(const T& ts) const {
    for (auto r : ts)
      printf(" %u", r.key());
  }

  template <typename T>
  void print_track_set(const T& ts, const reco::Vertex& v) const {
    for (auto r : ts)
      printf(" %u%s", r.key(), (v.trackWeight(r) < mfv::track_vertex_weight_min ? "!" : ""));
  }

  void print_track_set(const reco::Vertex& v) const {
    for (auto r = v.tracks_begin(), re = v.tracks_end(); r != re; ++r)
      printf(" %lu%s", r->key(), (v.trackWeight(*r) < mfv::track_vertex_weight_min ? "!" : ""));
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
  
  track_set vertex_track_set(const reco::Vertex& v, const double min_weight = mfv::track_vertex_weight_min) const {
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

  track_vec vertex_track_vec(const reco::Vertex& v, const double min_weight = mfv::track_vertex_weight_min) const {
    track_set s = vertex_track_set(v, min_weight);
    return track_vec(s.begin(), s.end());
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

  std::vector<TransientVertex> kv_reco_dropin(std::vector<reco::TransientTrack>& ttks, double chi2=5) {
    if (ttks.size() < 2)
      return std::vector<TransientVertex>();
    std::vector<TransientVertex> v(1, kv_reco->vertex(ttks));
    //std::cout << "fitted vertex chi2/dof: " << v[0].normalisedChiSquared() << std::endl;
    if (v[0].normalisedChiSquared() > chi2) //15
      return std::vector<TransientVertex>();
    return v;
  }

  const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
  const edm::EDGetTokenT<std::vector<reco::TrackRef>> seed_tracks_token;
  const edm::EDGetTokenT<std::vector<reco::TrackRef>> museed_tracks_token;
  const edm::EDGetTokenT<std::vector<reco::TrackRef>> eleseed_tracks_token;
  const int n_tracks_per_seed_vertex;
  const double max_seed_vertex_chi2;
  const bool use_2d_vertex_dist;
  const bool use_2d_track_dist;
  const bool track_attachment;
  const edm::EDGetTokenT<std::vector<reco::TrackRef>> quality_tracks_token;
  const double track_attachment_chi2;
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
  const bool ignore_lep_in_refit_distz;
  const double max_nm1_refit_distz_error;
  const double max_nm1_refit_distz_sig;
  const int max_nm1_refit_count;
  const bool histos;
  const bool histos_output_beforedzfit;
  const bool histos_output_afterdzfit;
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
  TH1F* h_noshare_nm1refit_dz;
  TH1F* h_noshare_nm1refit_dz_err;
  TH1F* h_noshare_nm1refit_dz_sig;
  TH2F* h_noshare_nm1refit_dz_dzerr;
  TH1F* h_max_noshare_track_multiplicity;
  TH1F* h_n_output_vertices;
  TH1F* h_output_vertex_ntracks;
  TH1F* h_output_vertex_chi2;
  TH1F* h_output_vertex_ndof;
  TH1F* h_output_vertex_normchi2;
  TH1F* h_output_vertex_x;
  TH1F* h_output_vertex_y;
  TH1F* h_output_vertex_z;

  TH1F* h_n_at_least_3trk_output_vertices;
  TH1F* h_n_at_least_4trk_output_vertices;

  TH1F* hs_output_vertex_tkvtxdist[stepEnum::N_STEPS];
  TH1F* hs_output_vertex_tkvtxdisterr[stepEnum::N_STEPS];
  TH1F* hs_output_vertex_tkvtxdistsig[stepEnum::N_STEPS];
  TH1F* hs_n_at_least_3trk_output_vertices[stepEnum::N_STEPS];
  TH1F* hs_n_at_least_4trk_output_vertices[stepEnum::N_STEPS];
  TH1F* hs_output_vertex_nm1_bsbs2ddist[stepEnum::N_STEPS];
  TH1F* hs_output_vertex_nm1_bs2derr[stepEnum::N_STEPS];
  TH1F* hs_output_vertex_ntracks[stepEnum::N_STEPS];
  TH1F* hs_output_vertex_neletracks[stepEnum::N_STEPS];
  TH1F* hs_output_vertex_nmutracks[stepEnum::N_STEPS];
  TH1F* hs_output_vertex_hasele[stepEnum::N_STEPS];
  TH1F* hs_output_vertex_hasmu[stepEnum::N_STEPS];
  TH1F* hs_output_vertex_nleptracks_ptgt20[stepEnum::N_STEPS];
  TH1F* hs_output_vertex_mass[stepEnum::N_STEPS];
  TH1F* hs_output_vertex_track_weights[stepEnum::N_STEPS];
  TH1F* hs_output_vertex_chi2[stepEnum::N_STEPS];
  TH1F* hs_output_vertex_ndof[stepEnum::N_STEPS];
  TH1F* hs_output_vertex_x[stepEnum::N_STEPS];
  TH1F* hs_output_vertex_y[stepEnum::N_STEPS];
  TH1F* hs_output_vertex_rho[stepEnum::N_STEPS];
  TH1F* hs_output_vertex_phi[stepEnum::N_STEPS];
  TH1F* hs_output_vertex_z[stepEnum::N_STEPS];
  TH1F* hs_output_vertex_zerr[stepEnum::N_STEPS];
  TH1F* hs_output_vertex_r[stepEnum::N_STEPS];
  TH1F* hs_output_vertex_paird2d[stepEnum::N_STEPS];
  TH1F* hs_output_vertex_paird2dsig[stepEnum::N_STEPS];
  TH1F* hs_output_vertex_pairdphi[stepEnum::N_STEPS];

  TH1F* h_deltaz_justfromlep;
  TH1F* h_deltax_justfromlep;
  TH1F* h_deltay_justfromlep;

};

MFVVertexer::MFVVertexer(const edm::ParameterSet& cfg)
  : kv_reco(new KalmanVertexFitter(cfg.getParameter<edm::ParameterSet>("kvr_params"), cfg.getParameter<edm::ParameterSet>("kvr_params").getParameter<bool>("doSmoothing"))),
    beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot_src"))),
    seed_tracks_token(consumes<std::vector<reco::TrackRef>>(cfg.getParameter<edm::InputTag>("seed_tracks_src"))),
    museed_tracks_token(consumes<std::vector<reco::TrackRef>>(cfg.getParameter<edm::InputTag>("muon_seed_tracks_src"))),
    eleseed_tracks_token(consumes<std::vector<reco::TrackRef>>(cfg.getParameter<edm::InputTag>("electron_seed_tracks_src"))),
    n_tracks_per_seed_vertex(cfg.getParameter<int>("n_tracks_per_seed_vertex")),
    max_seed_vertex_chi2(cfg.getParameter<double>("max_seed_vertex_chi2")),
    use_2d_vertex_dist(cfg.getParameter<bool>("use_2d_vertex_dist")),
    use_2d_track_dist(cfg.getParameter<bool>("use_2d_track_dist")),
    track_attachment(cfg.getParameter<bool>("track_attachment")),
    quality_tracks_token(track_attachment ? consumes<std::vector<reco::TrackRef>>(cfg.getParameter<edm::InputTag>("quality_tracks_src")) : edm::EDGetTokenT<std::vector<reco::TrackRef>>()),
    track_attachment_chi2(cfg.getParameter<double>("track_attachment_chi2")),
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
    ignore_lep_in_refit_distz(cfg.getParameter<bool>("ignore_lep_in_refit_distz")),
    max_nm1_refit_distz_error(cfg.getParameter<double>("max_nm1_refit_distz_error")),
    max_nm1_refit_distz_sig(cfg.getParameter<double>("max_nm1_refit_distz_sig")),
    max_nm1_refit_count(cfg.getParameter<int>("max_nm1_refit_count")),
    histos(cfg.getUntrackedParameter<bool>("histos", false)),
    histos_output_beforedzfit(cfg.getUntrackedParameter<bool>("histos_output_beforedzfit", true)),
    histos_output_afterdzfit(cfg.getUntrackedParameter<bool>("histos_output_afterdzfit", true)),
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
    h_noshare_nm1refit_dz            = fs->make<TH1F>("h_noshare_nm1refit_dz",            "", 100, 0, 0.1);
    h_noshare_nm1refit_dz_err        = fs->make<TH1F>("h_noshare_nm1refit_dz_err",        "", 100, 0, 0.1);
    h_noshare_nm1refit_dz_sig        = fs->make<TH1F>("h_noshare_nm1refit_dz_sig",        "", 50, 0, 10);
    h_noshare_nm1refit_dz_dzerr      = fs->make<TH2F>("h_noshare_nm1refit_dz_dzerr",      "", 100, 0, 0.1, 100, 0, 0.1);
    h_max_noshare_track_multiplicity = fs->make<TH1F>("h_max_noshare_track_multiplicity", "",  40,   0,     40);
    h_n_output_vertices              = fs->make<TH1F>("h_n_output_vertices",              "", 50, 0, 50);
    h_n_at_least_3trk_output_vertices = fs->make<TH1F>("h_n_at_least_3trk_output_vertices", ";# of output vertices w/ >=3trk/vtx", 20, 0, 20);
    h_n_at_least_4trk_output_vertices = fs->make<TH1F>("h_n_at_least_4trk_output_vertices", ";# of output vertices w/ >=4trk/vtx", 20, 0, 20);
    h_output_vertex_ntracks          = fs->make<TH1F>("h_output_vertex_ntracks",          "",  30,  0, 30);
    h_output_vertex_chi2             = fs->make<TH1F>("h_output_vertex_chi2",             "", 20,   0, max_seed_vertex_chi2);
    h_output_vertex_ndof             = fs->make<TH1F>("h_output_vertex_ndof",             "", 10,   0,     20);
    h_output_vertex_normchi2         = fs->make<TH1F>("h_output_vertex_normchi2",         "", 50,   0, max_seed_vertex_chi2);
    h_output_vertex_x                = fs->make<TH1F>("h_output_vertex_x",                "", 200,  -1,      1);
    h_output_vertex_y                = fs->make<TH1F>("h_output_vertex_y",                "", 200,  -1,      1);
    h_output_vertex_z                = fs->make<TH1F>("h_output_vertex_z",                "", 500,  0,     50);
    h_deltaz_justfromlep             = fs->make<TH1F>("h_deltaz_justfromlep",             "", 400,  0,      2);
    h_deltax_justfromlep             = fs->make<TH1F>("h_deltax_justfromlep",             "", 400,  0,      2);
    h_deltay_justfromlep             = fs->make<TH1F>("h_deltay_justfromlep",             "", 400,  0,      2);
  
    for(size_t step = 0; step < stepEnum::N_STEPS; ++step) {

      if (step == stepEnum::beforedzfit      && !histos_output_beforedzfit)      continue;
      if ( step == stepEnum::afterdzfit  && !histos_output_afterdzfit)      continue;

      hs_n_at_least_3trk_output_vertices[step] = fs->make<TH1F>("h_n_at_least_3trk_output_"+stepStrs[step]+"_vertices", ";# of >=3trk-vertices", 20, 0, 20);
      hs_n_at_least_4trk_output_vertices[step] = fs->make<TH1F>("h_n_at_least_4trk_output_"+stepStrs[step]+"_vertices", ";# of >=4trk-vertices", 20, 0, 20);
      hs_output_vertex_nm1_bsbs2ddist[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_nm1_bsbs2ddist", ";dBV (cm.) w/ n-1 cuts applied", 100, 0, 1.0);
      hs_output_vertex_nm1_bs2derr[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_nm1_bs2derr", ";bs2derr (cm.) w/ n-1 cuts applied", 20, 0, 0.05);
      hs_output_vertex_tkvtxdist[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_tkvtxdist", ";tkvtxdist (cm.)", 20, 0, 0.1);
      hs_output_vertex_tkvtxdisterr[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_tkvtxdisterr", ";tkvtxdisterr (cm.)", 20, 0, 0.1);
      hs_output_vertex_tkvtxdistsig[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_tkvtxdistsig", ";tkvtxdistsig", 20, 0, 6);
      hs_output_vertex_ntracks[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_ntracks", ";ntracks/vtx", 30, 0, 30);
      hs_output_vertex_neletracks[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_neletracks", ";neletracks/vtx", 30, 0, 30);
      hs_output_vertex_nmutracks[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_nmutracks", ";nmutracks/vtx", 30, 0, 30);
      hs_output_vertex_hasmu[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_hasmu", ";Does the SV have a mu?", 2, 0, 2);
      hs_output_vertex_hasele[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_hasele", ";Does the SV have an ele?", 2, 0, 2);
      hs_output_vertex_nleptracks_ptgt20[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_nleptracks_ptgt20", ";nleptracks/vtx w/ pt >= 20GeV", 5, 0, 5);
      hs_output_vertex_mass[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_mass", ";mass/vtx (GeV)", 20, 0, 1000);
      hs_output_vertex_track_weights[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_track_weights", ";vertex track weights", 21, 0, 1.05);
      hs_output_vertex_chi2[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_chi2", ";normalized chi2", 40, 0, 10);
      hs_output_vertex_ndof[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_ndof", ";ndof", 10, 0, 20);
      hs_output_vertex_x[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_x", ";vtxbsdist_x (cm.)", 20, -1, 1);
      hs_output_vertex_y[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_y", ";vtxbsdist_y (cm.)", 20, -1, 1);
      hs_output_vertex_rho[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_rho", ";vtx rho", 20, 0, 2);
      hs_output_vertex_phi[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_phi", ";vtx phi", 20, -3.15, 3.15);
      hs_output_vertex_z[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_z", ";vtxbsdist_z (cm.)", 400, -20, 20);
      hs_output_vertex_zerr[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_zerr", ";vtx_dist_zerr (cm.)", 40, 0, 1);
      hs_output_vertex_r[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_r", ";vtxbsdist_r (cm.)", 20, 0, 2);
      hs_output_vertex_paird2d[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_paird2d", ";svdist2d (cm.) every pair", 100, 0, 0.2);
      hs_output_vertex_paird2dsig[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_paird2dsig", ";svdist2d significance every pair", 100, 0, 20);
      hs_output_vertex_pairdphi[step] = fs->make<TH1F>("h_output_"+stepStrs[step]+"_vertex_pairdphi", ";dPhi(vtx0,vtx1) every pair", 100, -3.14, 3.14);
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

  for (const reco::Vertex& v : *vertices) {
    if (verbose) printf("x: %f y %f z %f\n", v.x(), v.y(), v.z());
    for (auto it = v.tracks_begin(), ite = v.tracks_end(); it != ite; ++it) {
      reco::TrackRef tk = it->castTo<reco::TrackRef>();
      if (verbose) printf("id: %i key: %u <%f,%f,%f,%f,%f>\n", tk.id().id(), tk.key(), tk->charge()*tk->pt(), tk->eta(), tk->phi(), tk->dxy(), tk->dz());
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

  edm::Handle<std::vector<reco::TrackRef>> muon_seed_track_refs;
  event.getByToken(museed_tracks_token, muon_seed_track_refs);

  edm::Handle<std::vector<reco::TrackRef>> electron_seed_track_refs;
  event.getByToken(eleseed_tracks_token, electron_seed_track_refs);

  edm::Handle<std::vector<reco::TrackRef>> quality_track_refs;
  if (track_attachment)
    event.getByToken(quality_tracks_token, quality_track_refs);

  std::vector<reco::TransientTrack> seed_tracks;
  std::map<reco::TrackRef, size_t> seed_track_ref_map;
  track_set all_seed_tracks;

  for (const reco::TrackRef& tk : *seed_track_refs) {
    all_seed_tracks.insert(tk);
    seed_tracks.push_back(tt_builder->build(tk));
    seed_track_ref_map[tk] = seed_tracks.size() - 1;
  }

  const size_t ntk = seed_tracks.size();
  if (verbose){
    printf("n_seed_tracks: %5lu\n", ntk);
    if (track_attachment)
      printf("n_quality_tracks: %5lu\n", quality_track_refs->size());
  }

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
    itks[0] = itk;
    for (size_t jtk = itk+1; jtk < ntk; ++jtk) {
      itks[1] = jtk;
      if (n_tracks_per_seed_vertex == 2) { try_seed_vertex(); continue; }
      for (size_t ktk = jtk+1; ktk < ntk; ++ktk) {
        itks[2] = ktk;
        if (n_tracks_per_seed_vertex == 3) { try_seed_vertex(); continue; }
        for (size_t ltk = ktk+1; ltk < ntk; ++ltk) {
          itks[3] = ltk;
          if (n_tracks_per_seed_vertex == 4) { try_seed_vertex(); continue; }
          for (size_t mtk = ltk+1; mtk < ntk; ++mtk) {
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

  // try to recycle discarded seed track during fitting
  if (false){
    track_set track_discard;
    for (const reco::TrackRef& itk:all_seed_tracks){
      bool used = false;
      for (size_t i=0; i<vertices->size(); ++i){
        const reco::Vertex& v = vertices->at(i);
        const track_set vtk = vertex_track_set(v);
        if (vtk.find(itk)!=vtk.end()){
          used = true;
          break;
        }
      }
      if (!used){
        track_discard.insert(itk);
      }
    }
    bool useful_tracks = true;
    while (useful_tracks){
      if (verbose){
        std::cout << "discarded tracks: ";
        print_track_set(track_discard);
        std::cout << std::endl;
      }
      useful_tracks = false;
      for (const reco::TrackRef& itk:track_discard){
        const reco::TransientTrack& ttk = seed_tracks[seed_track_ref_map[itk]];
        int v_assign = -1;
        double v_assign_dist_sig = 999;
        unsigned int v_assign_ntk = 0;
        if (verbose){
          std::cout << "For track " << itk.key() << std::endl;
        }
        for (size_t i=0; i<vertices->size(); ++i){
          const reco::Vertex& v = vertices->at(i);
          std::pair<bool, Measurement1D> t_dist = track_dist(ttk, v);
          t_dist.first = t_dist.first && (t_dist.second.value() < max_track_vertex_dist || t_dist.second.significance() < max_track_vertex_sig); // whether it is too far away from the vtx
          if (t_dist.first) {
            if (t_dist.second.significance()<min_track_vertex_sig_to_remove){
              if (v_assign_ntk<v.nTracks()){
                v_assign = i;
                v_assign_dist_sig = t_dist.second.significance();
                v_assign_ntk = v.nTracks();
              }
            }
            else if (t_dist.second.significance()<v_assign_dist_sig){
              v_assign = i;
              v_assign_dist_sig = t_dist.second.significance();
              v_assign_ntk = v.nTracks();
            }
          }
          
          if (verbose){
            std::cout << "  Track-vertex " << i << " " << t_dist.first << " dist: " << t_dist.second.value() << " sig: " << t_dist.second.significance() << std::endl;
          }
        }
        if (verbose)
          std::cout << "Track " << itk.key() << " assigned to " << v_assign << std::endl;
        if (v_assign>=0){
          useful_tracks = true;
          track_discard.erase(itk);
          if (verbose){
            std::cout << "Fitting vertex " << v_assign << " with tracks: ";
            print_track_set((*vertices)[v_assign]);
            std::cout << " with added track " << itk.key() << std::endl;
          }
          std::vector<reco::TransientTrack> ttks;
          for (auto tk:vertex_track_set((*vertices)[v_assign])){
            ttks.push_back(seed_tracks[seed_track_ref_map[tk]]);
          }
          ttks.push_back(ttk);
          reco::VertexCollection new_vertices;
          for (const TransientVertex& tv : kv_reco_dropin(ttks))
            new_vertices.push_back(reco::Vertex(tv));
          if (verbose) {
            printf("      got %lu new vertices out of the av fit for v%i\n", new_vertices.size(), v_assign);
            printf("      these track sets:");
            for (const auto& nv : new_vertices) {
              printf(" (");
              print_track_set(nv);
              printf(" ),");
            }
            printf("\n");
          }
          if (new_vertices.size() == 1)
            (*vertices)[v_assign] = new_vertices[0];
          break;
        }
      }
    }
  }

  // track attachment : https://cds.cern.ch/record/2669425 (chapter 4.5)
  if (track_attachment){
    // build transient tracks from quality tracks (not included in seed tracks)
    std::vector<reco::TransientTrack> quality_tracks;
    std::map<reco::TrackRef, size_t> quality_track_ref_map;
    track_set all_quality_tracks;
    for (const reco::TrackRef& tk : *quality_track_refs) {
      all_quality_tracks.insert(tk);
      quality_tracks.push_back(tt_builder->build(tk));
      quality_track_ref_map[tk] = quality_tracks.size() - 1;
    }
    //start track attachment, attach tracks to vertices if dist(track, vertex)<5 sigma, if a track is close to more than one vertices, attach to the closer one, if a tracks has distance with more than one vertices <=1.5 sigma, attach it to the vertex with more tracks
    bool refit = true;
    while (refit){
      refit = false;
      if (verbose){
        std::cout << "now trying attaching tracks: ";
        print_track_set(all_quality_tracks);
        std::cout << std::endl;
      }
      for (const reco::TrackRef& itk:all_quality_tracks) {
        const reco::TransientTrack& ttk = quality_tracks[quality_track_ref_map[itk]];
        int v_assign = -1;
        double v_assign_dist_sig = 999;
        unsigned int v_assign_ntk = 0;

        if (verbose){
          std::cout << "For track " << itk.key() << std::endl;
        }
        for (size_t i=0; i<vertices->size(); ++i){
          const reco::Vertex& v = vertices->at(i);
          std::pair<bool, Measurement1D> t_dist = track_dist(ttk, v);
          t_dist.first = t_dist.first && (t_dist.second.value() < max_track_vertex_dist || t_dist.second.significance() < max_track_vertex_sig); // whether it is too far away from the vtx
          if (t_dist.first) {
            if ( (t_dist.second.significance()<min_track_vertex_sig_to_remove) && (v_assign_dist_sig<min_track_vertex_sig_to_remove) ){
              if (v_assign_ntk<v.nTracks()){
                v_assign = i;
                v_assign_dist_sig = t_dist.second.significance();
                v_assign_ntk = v.nTracks();
              }
            }
            else if (t_dist.second.significance()<v_assign_dist_sig){
              v_assign = i;
              v_assign_dist_sig = t_dist.second.significance();
              v_assign_ntk = v.nTracks();
            }
          }
          
          if (verbose){
            std::cout << "  Track-vertex " << i << " " << t_dist.first << " dist: " << t_dist.second.value() << " sig: " << t_dist.second.significance() << std::endl;
          }
        }
        if (verbose)
          std::cout << "Track " << itk.key() << " assigned to " << v_assign << std::endl;
        if (v_assign>=0){
          refit = true;
          all_quality_tracks.erase(itk);
          if (verbose){
            std::cout << "Fitting vertex " << v_assign << " with tracks: ";
            print_track_set((*vertices)[v_assign]);
            std::cout << " with added track " << itk.key() << std::endl;
          }
          std::vector<reco::TransientTrack> ttks;
          for (auto tk:vertex_track_set((*vertices)[v_assign])){
            ttks.push_back(tt_builder->build(tk));
          }
          ttks.push_back(ttk);
          if (verbose)
            std::cout << " fitting vertex with " << ttks.size() << " tracks " << std::endl;
          reco::VertexCollection new_vertices;
          for (const TransientVertex& tv : kv_reco_dropin(ttks, track_attachment_chi2))
            new_vertices.push_back(reco::Vertex(tv));
          if (verbose) {
            printf("      got %lu new vertices out of the av fit for v%i\n", new_vertices.size(), v_assign);
            printf("      these track sets:");
            for (const auto& nv : new_vertices) {
              printf(" (");
              print_track_set(nv);
              printf(" ),");
            }
            printf("\n");
          }
          if (new_vertices.size() == 1)
            (*vertices)[v_assign] = new_vertices[0];
          break;
        }
      }
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
      const double vx = v.position().x() - bsx;
      const double vy = v.position().y() - bsy;
      const double vz = v.position().z() - bsz;
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

  //////////////////////////////////////////////////////////////////////
  // Merge vertices that are still "close". JMTBAD this doesn't do anything currently, only run in verbose mode
  //////////////////////////////////////////////////////////////////////

  if (verbose)
    printf("fun2! before merge loop, # vertices = %lu\n", vertices->size());

  if (verbose) {
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
  }

  if (verbose){
    // investigate how tracks are dropped during nm1 process
    for (v[0] = vertices->begin(); v[0] != vertices->end(); ++v[0]) {
      const track_vec tks = vertex_track_vec(*v[0]);
      const size_t ntks = tks.size();
      if (ntks < 3)
        continue;
      printf("doing refit on vertex at %7.4f %7.4f %7.4f with %lu tracks\n", v[0]->x(), v[0]->y(), v[0]->z(), ntks);
      for (size_t i = 0; i < ntks; ++i){
        printf("  refit %lu will drop tk  pt %7.4f +- %7.4f eta %7.4f +- %7.4f phi %7.4f +- %7.4f dxy %7.4f +- %7.4f dz %7.4f +- %7.4f\n", i, tks[i]->pt(), tks[i]->ptError(), tks[i]->eta(), tks[i]->etaError(), tks[i]->phi(), tks[i]->phiError(), tks[i]->dxy(), tks[i]->dxyError(), tks[i]->dz(), tks[i]->dzError());
        std::vector<reco::TransientTrack> ttks(ntks-1);
        for (size_t j = 0; j < ntks; ++j)
          if (j != i)
            ttks[j-(j>=i)] = tt_builder->build(tks[j]);

        reco::Vertex vnm1(TransientVertex(kv_reco->vertex(ttks)));
        printf("    refitted vertex chi2/dof %7.4f with track ", vnm1.normalizedChi2());
        print_track_set(vnm1);
      }
    }
  }
  if (histos_output_beforedzfit){
    fillCommonOutputHists(vertices, fake_bs_vtx, tt_builder, stepEnum::beforedzfit);
  }

  //////////////////////////////////////////////////////////////////////
  // Drop tracks that "move" the vertex too much by refitting without each track.
  //////////////////////////////////////////////////////////////////////
  //if the track is a lepton (key == 154 or 155) don't do the refitting. 
  //I believe specificially, 154 are electrons. 155 are muons 

  if (max_nm1_refit_dist3 > 0 || max_nm1_refit_distz > 0) {
  //if (max_nm1_refit_dist3 > 0 || max_nm1_refit_distz > 0 || max_nm1_refit_distz_sig > 0) {
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
        printf("doing n-%i refit on vertex at %7.4f %7.4f %7.4f with %lu tracks\n", refit_count[iv]+1, v[0]->x(), v[0]->y(), v[0]->z(), ntks);
        for (size_t i = 0; i < ntks; ++i) {
          printf("  refit %lu will drop tk pt %7.4f +- %7.4f eta %7.4f +- %7.4f phi %7.4f +- %7.4f dxy %7.4f +- %7.4f dz %7.4f +- %7.4f\n", i, tks[i]->pt(), tks[i]->ptError(), tks[i]->eta(), tks[i]->etaError(), tks[i]->phi(), tks[i]->phiError(), tks[i]->dxy(), tks[i]->dxyError(), tks[i]->dz(), tks[i]->dzError());
          if (ignore_lep_in_refit_distz) {
            if ( (tks[i].id().id() == 155 || tks[i].id().id() == 154) && abs(tks[i]->pt()) >= 20.0 ) 
              printf("  refit %lu will SKIP tk pt %7.4f +- %7.4f eta %7.4f +- %7.4f phi %7.4f +- %7.4f dxy %7.4f +- %7.4f dz %7.4f +- %7.4f\n", i, tks[i]->pt(), tks[i]->ptError(), tks[i]->eta(), tks[i]->etaError(), tks[i]->phi(), tks[i]->phiError(), tks[i]->dxy(), tks[i]->dxyError(), tks[i]->dz(), tks[i]->dzError());
          }
        }
      }

      std::vector<reco::TransientTrack> ttks(ntks - 1);
      //loops over all tracks 
      for (size_t i = 0; i < ntks; ++i) {
        // we want to : NOT DROP leptons 
        if ( ! ((tks[i].id().id() == 155 || tks[i].id().id() == 154) && abs(tks[i]->pt()) >= 20.0 ) ) {
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
    }
    iv = 0; //some vertices after dz refiting have normalized chi2 > 5
    for (v[0] = vertices->begin(); v[0] != vertices->end(); ++v[0], ++iv) {
       if ((*v[0]).normalizedChi2() > 5) {
         v[0] = vertices->erase(v[0]) - 1;
         continue;
       }
    }
  }
  if (histos_output_afterdzfit){
    fillCommonOutputHists(vertices, fake_bs_vtx, tt_builder, stepEnum::afterdzfit);
  }

  //////////////////////////////////////////////////////////////////////
  // Put the output.
  //////////////////////////////////////////////////////////////////////

  if (histos) {
    for (const reco::Vertex& v : *vertices) { 
      h_output_vertex_ntracks->Fill(v.tracksSize());
      h_output_vertex_chi2->Fill(v.chi2());
      h_output_vertex_ndof->Fill(v.ndof());
      h_output_vertex_normchi2->Fill(v.normalizedChi2());
      h_output_vertex_x->Fill(v.x());
      h_output_vertex_y->Fill(v.y());
      h_output_vertex_z->Fill(v.z());
    }
  }
  finish(event, seed_tracks, std::move(vertices), std::move(vpeffs), vpeffs_tracks);
}

void MFVVertexer::fillCommonOutputHists(std::unique_ptr<reco::VertexCollection>& vertices, const reco::Vertex& fake_bs_vtx, edm::ESHandle<TransientTrackBuilder>& tt_builder, size_t step) {

  std::map<reco::TrackRef, int> track_use;
  int count_3trk_vertices = 0;
  int count_4trk_vertices = 0;
  int count_vertex_wele = 0;
  int count_vertex_wmu = 0;

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
    int nleptracks = 0;
    int nele_tks = 0;
    int nmu_tks = 0;

    for (const auto& tk : vertex_track_set(v)) {
      if (tk.id().id() == 154 && tk->pt() >= 20.0)
        nele_tks += 1;
      if (tk.id().id() == 155 && tk->pt() >= 20.0) 
        nmu_tks += 1;

      if (tk.id().id() == 155 || tk.id().id() == 154) {
        if (tk->pt() >= 20.0)
          nleptracks += 1;
      }
      if (track_use.find(tk) != track_use.end())
        track_use[tk] += 1;
      else
        track_use[tk] = 1;
    }

    hs_output_vertex_neletracks[step]->Fill(nele_tks);
    hs_output_vertex_nmutracks[step]->Fill(nmu_tks);
    hs_output_vertex_nleptracks_ptgt20[step]->Fill(nleptracks);
    hs_output_vertex_ntracks[step]->Fill(ntracks);
    if (nele_tks > 0 ) count_vertex_wele++;
    if (nmu_tks > 0 ) count_vertex_wmu++;
    if (ntracks >= 3) {
      count_3trk_vertices++;
      if (ntracks >= 4) 
        count_4trk_vertices++;
      Measurement1D dBV_Meas1D = vertex_dist_2d.distance(v, fake_bs_vtx);
      double dBV = dBV_Meas1D.value();
      double bs2derr = dBV_Meas1D.error();

      if (vchi2 < 5 && ntracks >= 3 && bs2derr < 0.05) {
        hs_output_vertex_nm1_bsbs2ddist[step]->Fill(dBV);
      }
      if (vchi2 < 5 && ntracks >= 3 && dBV > 0.01) {
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
    hs_output_vertex_zerr[step]->Fill(v.zError());
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

  hs_n_at_least_3trk_output_vertices[step]->Fill(count_3trk_vertices);
  hs_n_at_least_4trk_output_vertices[step]->Fill(count_4trk_vertices);
  hs_output_vertex_hasele[step]->Fill(count_vertex_wele);
  hs_output_vertex_hasmu[step]->Fill(count_vertex_wmu);
}


DEFINE_FWK_MODULE(MFVVertexer);
