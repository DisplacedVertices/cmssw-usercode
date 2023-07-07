#include "TH2.h"
#include "CLHEP/Random/RandBinomial.h"
#include "CLHEP/Random/RandomEngine.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/TrackReco/interface/TrackBase.h"
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
#include "JMTucker/Tools/interface/AnalysisEras.h"
#include "JMTucker/Tools/interface/TrackRescaler.h"

class MFVVertexTracks : public edm::EDFilter {
public:
  MFVVertexTracks(const edm::ParameterSet&);
  virtual bool filter(edm::Event&, const edm::EventSetup&);

private:
  bool match_track_jet(const reco::Track& tk, const pat::Jet& jet);
  const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
  const bool use_primary_vertices;
  const edm::EDGetTokenT<reco::VertexCollection> primary_vertices_token;
  const bool disregard_event;
  const bool use_tracks;
  const bool use_separated_leptons;
  const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
  const edm::EDGetTokenT<reco::TrackCollection> electron_tracks_token;
  const edm::EDGetTokenT<reco::TrackCollection> muon_tracks_token;
  const bool save_quality_tracks;
  const bool match_jets;
  const edm::EDGetTokenT<pat::JetCollection> match_jet_token;
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
  const double min_track_pt_loose;
  const double min_track_dxy;
  const double min_track_sigmadxy;
  const double min_track_rescaled_sigmadxy;
  const double min_leptrack_rescaled_sigmadxy;
  const double min_track_rescaled_sigmadxy_loose;
  const double min_track_sigmadxypv;
  const int min_track_hit_r;
  const int min_leptrack_hit_r;
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

  jmt::TrackRescaler track_rescaler;

  TH1F* h_n_all_tracks;
  TH1F* h_all_track_pars[7];
  TH1F* h_all_track_errs[7];
  TH1F* h_all_track_p;
  TH1F* h_all_track_pt_barrel;
  TH1F* h_all_track_pt_endcap;
  TH1F* h_all_track_errdxybs;
  TH2F* h_all_track_pt_errdxybs;
  TH2F* h_all_track_pt_dxybs;
  TH1F* h_all_track_sigmadxybs;
  TH1F* h_all_track_sigmadxypv;
  TH1F* h_all_track_nhits;
  TH1F* h_all_track_npxhits;
  TH1F* h_all_track_nsthits;
  TH1F* h_all_track_npxlayers;
  TH1F* h_all_track_nstlayers;
  TH1F* h_n_seed_tracks;
  TH1F* h_seed_track_pars[7];
  TH1F* h_seed_track_errs[7];
  TH1F* h_seed_track_p;
  TH1F* h_seed_track_pt_barrel;
  TH1F* h_seed_track_pt_endcap;
  TH1F* h_seed_track_errdxybs;
  TH2F* h_seed_track_pt_errdxybs;
  TH2F* h_seed_track_pt_dxybs;
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

  TH1F* h_n_all_eletracks;
  TH1F* h_all_eletrack_pars[7];
  TH1F* h_all_eletrack_errs[7];
  TH1F* h_all_eletrack_p;
  TH1F* h_all_eletrack_pt_barrel;
  TH1F* h_all_eletrack_pt_endcap;
  TH1F* h_all_eletrack_errdxybs;
  // TH2F* h_all_eletrack_pt_errdxybs;
  // TH2F* h_all_eletrack_pt_dxybs;
  TH1F* h_all_eletrack_sigmadxybs;
  TH1F* h_all_eletrack_sigmadxypv;
  TH1F* h_all_eletrack_nhits;
  TH1F* h_all_eletrack_npxhits;
  TH1F* h_all_eletrack_nsthits;
  TH1F* h_all_eletrack_npxlayers;
  TH1F* h_all_eletrack_nstlayers;
  TH1F* h_all_eletrack_minr;
  TH1F* h_n_seed_eletracks;
  TH1F* h_seed_eletrack_pars[7];
  TH1F* h_seed_eletrack_errs[7];
  TH1F* h_seed_eletrack_p;
  TH1F* h_seed_eletrack_pt_barrel;
  TH1F* h_seed_eletrack_pt_endcap;
  TH1F* h_seed_eletrack_errdxybs;
  // TH2F* h_seed_eletrack_pt_errdxybs;
  // TH2F* h_seed_eletrack_pt_dxybs;
  TH1F* h_seed_eletrack_sigmadxybs;
  TH1F* h_seed_eletrack_sigmadxypv;
  TH1F* h_seed_eletrack_nhits;
  TH1F* h_seed_eletrack_npxhits;
  TH1F* h_seed_eletrack_nsthits;
  TH1F* h_seed_eletrack_npxlayers;
  TH1F* h_seed_eletrack_nstlayers;
  TH1F* h_seed_nm1_elept;
  TH1F* h_seed_nm1_elenpxlayers;
  TH1F* h_seed_nm1_elenstlayers;
  TH1F* h_seed_nm1_elesigmadxybs;
  TH1F* h_seed_nm1_eledxybs;
  TH1F* h_seed_nm1_eledxyerr;
  TH1F* h_seed_nm1_eleminr;

  TH2F* h_seed_track_sigmadxybs_vs_pt;
  TH2F* h_seed_track_dxybs_vs_pt;
  TH2F* h_seed_track_dxyerr_vs_pt;

  TH2F* h_all_eletrack_sigmadxybs_vs_pt;
  TH2F* h_all_eletrack_dxybs_vs_pt;
  TH2F* h_all_eletrack_dxyerr_vs_pt;
  TH2F* h_all_eletrack_minr_vs_pt;
  TH2F* h_all_eletrack_npxlayers_vs_pt;
  TH2F* h_all_eletrack_nstlayers_vs_pt;

  TH2F* h_seed_eletrack_sigmadxybs_vs_pt;
  TH2F* h_seed_eletrack_dxybs_vs_pt;
  TH2F* h_seed_eletrack_dxyerr_vs_pt;
  TH2F* h_seed_eletrack_minr_vs_pt;
  TH2F* h_seed_eletrack_npxlayers_vs_pt;
  TH2F* h_seed_eletrack_nstlayers_vs_pt; 

  TH2F* h_all_eletrack_sigmadxybs_vs_dxy;
  TH2F* h_all_eletrack_minr_vs_dxy;
  TH2F* h_all_eletrack_npxlayers_vs_dxy;
  TH2F* h_all_eletrack_nstlayers_vs_dxy;
  TH2F* h_all_eletrack_dxyerr_vs_dxy;

  TH2F* h_seed_eletrack_sigmadxybs_vs_dxy;
  TH2F* h_seed_eletrack_minr_vs_dxy;
  TH2F* h_seed_eletrack_npxlayers_vs_dxy;
  TH2F* h_seed_eletrack_nstlayers_vs_dxy; 
  TH2F* h_seed_eletrack_dxyerr_vs_dxy;

  TH1F* h_n_all_mutracks;
  TH1F* h_all_mutrack_pars[7];
  TH1F* h_all_mutrack_errs[7];
  TH1F* h_all_mutrack_p;
  TH1F* h_all_mutrack_pt_barrel;
  TH1F* h_all_mutrack_pt_endcap;
  TH1F* h_all_mutrack_errdxybs;
  // TH2F* h_all_mutrack_pt_errdxybs;
  // TH2F* h_all_mutrack_pt_dxybs;
  TH1F* h_all_mutrack_sigmadxybs;
  TH1F* h_all_mutrack_sigmadxypv;
  TH1F* h_all_mutrack_nhits;
  TH1F* h_all_mutrack_npxhits;
  TH1F* h_all_mutrack_nsthits;
  TH1F* h_all_mutrack_npxlayers;
  TH1F* h_all_mutrack_nstlayers;
  TH1F* h_all_mutrack_minr;
  TH1F* h_n_seed_mutracks;
  TH1F* h_seed_mutrack_pars[7];
  TH1F* h_seed_mutrack_errs[7];
  TH1F* h_seed_mutrack_p;
  TH1F* h_seed_mutrack_pt_barrel;
  TH1F* h_seed_mutrack_pt_endcap;
  TH1F* h_seed_mutrack_errdxybs;
  TH2F* h_seed_mutrack_pt_errdxybs;
  TH2F* h_seed_mutrack_pt_dxybs;
  TH1F* h_seed_mutrack_sigmadxybs;
  TH1F* h_seed_mutrack_sigmadxypv;
  TH1F* h_seed_mutrack_nhits;
  TH1F* h_seed_mutrack_npxhits;
  TH1F* h_seed_mutrack_nsthits;
  TH1F* h_seed_mutrack_npxlayers;
  TH1F* h_seed_mutrack_nstlayers;
  TH1F* h_seed_nm1_mupt;
  TH1F* h_seed_nm1_munpxlayers;
  TH1F* h_seed_nm1_munstlayers;
  TH1F* h_seed_nm1_mudxybs;
  TH1F* h_seed_nm1_mudxyerr;
  TH1F* h_seed_nm1_musigmadxybs;
  TH1F* h_seed_nm1_muminr;

  TH2F* h_all_mutrack_sigmadxybs_vs_pt;
  TH2F* h_all_mutrack_dxybs_vs_pt;
  TH2F* h_all_mutrack_dxyerr_vs_pt;
  TH2F* h_all_mutrack_minr_vs_pt;
  TH2F* h_all_mutrack_npxlayers_vs_pt;
  TH2F* h_all_mutrack_nstlayers_vs_pt;

  TH2F* h_seed_mutrack_sigmadxybs_vs_pt;
  TH2F* h_seed_mutrack_dxybs_vs_pt;
  TH2F* h_seed_mutrack_dxyerr_vs_pt;
  TH2F* h_seed_mutrack_minr_vs_pt;
  TH2F* h_seed_mutrack_npxlayers_vs_pt;
  TH2F* h_seed_mutrack_nstlayers_vs_pt; 

  TH2F* h_all_mutrack_sigmadxybs_vs_dxy;
  TH2F* h_all_mutrack_minr_vs_dxy;
  TH2F* h_all_mutrack_npxlayers_vs_dxy;
  TH2F* h_all_mutrack_nstlayers_vs_dxy;
  TH2F* h_all_mutrack_dxyerr_vs_dxy;

  TH2F* h_seed_mutrack_sigmadxybs_vs_dxy;
  // TH2F* h_seed_mutrack_dxybs_vs_dxy;
  // TH2F* h_seed_mutrack_dxyerr_vs_pt;
  TH2F* h_seed_mutrack_minr_vs_dxy;
  TH2F* h_seed_mutrack_npxlayers_vs_dxy;
  TH2F* h_seed_mutrack_nstlayers_vs_dxy; 
  TH2F* h_seed_mutrack_dxyerr_vs_dxy;

};

MFVVertexTracks::MFVVertexTracks(const edm::ParameterSet& cfg)
  : beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot_src"))),
    use_primary_vertices(cfg.getParameter<edm::InputTag>("primary_vertices_src").label() != ""),
    primary_vertices_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("primary_vertices_src"))),
    disregard_event(cfg.getParameter<bool>("disregard_event")),
    use_tracks(cfg.getParameter<bool>("use_tracks")),
    use_separated_leptons(cfg.getParameter<bool>("use_separated_leptons")),
    tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("tracks_src"))),
    electron_tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("electron_tracks_src"))),
    muon_tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("muon_tracks_src"))),
    save_quality_tracks(cfg.getParameter<bool>("save_quality_tracks")),
    match_jets(cfg.getParameter<bool>("match_jets")),
    match_jet_token(match_jets ? consumes<pat::JetCollection>(cfg.getParameter<edm::InputTag>("match_jet_src")) : edm::EDGetTokenT<pat::JetCollection>()),
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
    min_track_pt_loose(cfg.getParameter<double>("min_track_pt_loose")),
    min_track_dxy(cfg.getParameter<double>("min_track_dxy")),
    min_track_sigmadxy(cfg.getParameter<double>("min_track_sigmadxy")),
    min_track_rescaled_sigmadxy(cfg.getParameter<double>("min_track_rescaled_sigmadxy")),
    min_leptrack_rescaled_sigmadxy(cfg.getParameter<double>("min_leptrack_rescaled_sigmadxy")),
    min_track_rescaled_sigmadxy_loose(cfg.getParameter<double>("min_track_rescaled_sigmadxy_loose")),
    min_track_sigmadxypv(cfg.getParameter<double>("min_track_sigmadxypv")),
    min_track_hit_r(cfg.getParameter<int>("min_track_hit_r")),
    min_leptrack_hit_r(cfg.getParameter<int>("min_leptrack_hit_r")),
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
  produces<std::vector<reco::TrackRef>>("allele");
  produces<std::vector<reco::TrackRef>>("eleseed");
  produces<std::vector<reco::TrackRef>>("allmu");
  produces<std::vector<reco::TrackRef>>("museed");
  produces<reco::TrackCollection>("seed");
  produces<std::vector<reco::TrackRef>>("quality");
  produces<reco::TrackCollection>("quality");

  if (histos) {
    edm::Service<TFileService> fs;

    h_n_all_tracks  = fs->make<TH1F>("h_n_all_tracks",  "", 200, 0, 2000);
    h_n_seed_tracks = fs->make<TH1F>("h_n_seed_tracks", "", 200, 0,  200);
    h_n_all_eletracks  = fs->make<TH1F>("h_n_all_eletracks",  "", 200, 0, 200);
    h_n_seed_eletracks = fs->make<TH1F>("h_n_seed_eletracks", "", 200, 0,  200);    
    h_n_all_mutracks  = fs->make<TH1F>("h_n_all_mutracks",  "", 200, 0, 200);
    h_n_seed_mutracks = fs->make<TH1F>("h_n_seed_mutracks", "", 200, 0,  200);

    const char* par_names[7] = {"pt", "eta", "phi", "dxybs", "rescale_dxybs", "dxypv", "dz"};
    const int par_nbins[7] = {  50, 50, 50, 500, 500, 100, 80 };
    //const double par_lo[7] = {   0, -2.5, -3.15, -0.2, -0.2, -0.2, -20 };
    const double par_lo[7] = {   0, -2.5, -3.15, 0, 0, 0, -20 };
    const double par_hi[7] = {  10,  2.5,  3.15,  1,  1,  1,  20 };
    const double err_lo[7] = { 0 };
    const double err_hi[7] = { 0.15, 0.01, 0.01, 0.2, 0.2, 0.2, 0.4 };
    for (int i = 0; i < 7; ++i) {
      h_all_track_pars[i] = fs->make<TH1F>(TString::Format("h_all_track_%s",    par_names[i]), "", par_nbins[i], par_lo[i], par_hi[i]);
      h_all_track_errs[i] = fs->make<TH1F>(TString::Format("h_all_track_err%s", par_names[i]), "", par_nbins[i], err_lo[i], err_hi[i]);
      h_all_eletrack_pars[i] = fs->make<TH1F>(TString::Format("h_all_eletrack_%s",    par_names[i]), "", par_nbins[i], par_lo[i], par_hi[i]);
      h_all_eletrack_errs[i] = fs->make<TH1F>(TString::Format("h_all_eletrack_err%s", par_names[i]), "", par_nbins[i], err_lo[i], err_hi[i]);      
      h_all_mutrack_pars[i] = fs->make<TH1F>(TString::Format("h_all_mutrack_%s",    par_names[i]), "", par_nbins[i], par_lo[i], par_hi[i]);
      h_all_mutrack_errs[i] = fs->make<TH1F>(TString::Format("h_all_mutrack_err%s", par_names[i]), "", par_nbins[i], err_lo[i], err_hi[i]);
    }

    h_all_track_p = fs->make<TH1F>("h_all_track_p", ";all track's p (GeV)", 50, 0, 10);
    h_all_track_pt_barrel = fs->make<TH1F>("h_all_track_pt_barrel", ";all track's p_{T} in barrel (GeV)", 50, 0, 10);
    h_all_track_pt_endcap = fs->make<TH1F>("h_all_track_pt_endcap", ";all track's p_{T} in endcap (GeV)", 50, 0, 10);
    h_all_track_sigmadxybs = fs->make<TH1F>("h_all_track_sigmadxybs", ";all track's nsigmadxybs", 40, -10, 10);
    h_all_track_pt_dxybs = fs->make<TH2F>("h_all_track_pt_dxybs", ";all track's p_{T} (GeV);all track's dxybs (cm)", 500, 0, 100, 500, -0.2, 0.2);
    h_all_track_pt_errdxybs = fs->make<TH2F>("h_all_track_pt_errdxybs", ";all track's p_{T} (GeV);all track's err_dxybs (cm)", 500, 0, 100, 500, 0, 0.2);
    h_all_track_sigmadxypv = fs->make<TH1F>("h_all_track_sigmadxypv", ";all track's nsigmadxypv", 40, -10, 10);
    h_all_track_nhits      = fs->make<TH1F>("h_all_track_nhits",      ";all track's nhits", 40,   0, 40);
    h_all_track_npxhits    = fs->make<TH1F>("h_all_track_npxhits",    ";all track's npxhits", 12,   0, 12);
    h_all_track_nsthits    = fs->make<TH1F>("h_all_track_nsthits",    ";all track's nsthits", 28,   0, 28);
    h_all_track_npxlayers  = fs->make<TH1F>("h_all_track_npxlayers",  ";all track's npxlayers", 10,   0, 10);
    h_all_track_nstlayers  = fs->make<TH1F>("h_all_track_nstlayers",  ";all track's nstlayers", 30,   0, 30);

    h_all_eletrack_p = fs->make<TH1F>("h_all_eletrack_p", "", 400, 0, 2000);
    h_all_eletrack_pt_barrel = fs->make<TH1F>("h_all_eletrack_pt_barrel", "", 400, 0, 2000);
    h_all_eletrack_pt_endcap = fs->make<TH1F>("h_all_eletrack_pt_endcap", "", 400, 0, 2000);
    h_all_eletrack_sigmadxybs = fs->make<TH1F>("h_all_eletrack_sigmadxybs", "", 40, 0, 20);
    // h_all_eletrack_pt_dxybs = fs->make<TH2F>("h_all_eletrack_pt_dxybs", "", 500, 0, 100, 500, 0, 2);
    // h_all_eletrack_pt_errdxybs = fs->make<TH2F>("h_all_eletrack_pt_errdxybs", "", 500, 0, 100, 500, 0, 0.2);
    h_all_eletrack_sigmadxypv = fs->make<TH1F>("h_all_eletrack_sigmadxypv", "", 40, 0, 20);
    h_all_eletrack_nhits      = fs->make<TH1F>("h_all_eletrack_nhits",      "", 40,   0, 40);
    h_all_eletrack_npxhits    = fs->make<TH1F>("h_all_eletrack_npxhits",    "", 12,   0, 12);
    h_all_eletrack_nsthits    = fs->make<TH1F>("h_all_eletrack_nsthits",    "", 28,   0, 28);
    h_all_eletrack_npxlayers  = fs->make<TH1F>("h_all_eletrack_npxlayers",  "", 10,   0, 10);
    h_all_eletrack_nstlayers  = fs->make<TH1F>("h_all_eletrack_nstlayers",  "", 30,   0, 30);
    h_all_eletrack_minr       = fs->make<TH1F>("h_all_eletrack_minr", "", 6, 0, 6);

    h_all_mutrack_p = fs->make<TH1F>("h_all_mutrack_p", "", 400, 0, 2000);
    h_all_mutrack_pt_barrel = fs->make<TH1F>("h_all_mutrack_pt_barrel", "", 400, 0, 2000);
    h_all_mutrack_pt_endcap = fs->make<TH1F>("h_all_mutrack_pt_endcap", "", 400, 0, 2000);
    h_all_mutrack_sigmadxybs = fs->make<TH1F>("h_all_mutrack_sigmadxybs", "", 40, 0, 20);
    // h_all_mutrack_pt_dxybs = fs->make<TH2F>("h_all_mutrack_pt_dxybs", "", 500, 0, 100, 500, 0, 2);
    // h_all_mutrack_pt_errdxybs = fs->make<TH2F>("h_all_mutrack_pt_errdxybs", "", 500, 0, 100, 500, 0, 0.2);
    h_all_mutrack_sigmadxypv = fs->make<TH1F>("h_all_mutrack_sigmadxypv", "", 40, 0, 20);
    h_all_mutrack_nhits      = fs->make<TH1F>("h_all_mutrack_nhits",      "", 40,   0, 40);
    h_all_mutrack_npxhits    = fs->make<TH1F>("h_all_mutrack_npxhits",    "", 12,   0, 12);
    h_all_mutrack_nsthits    = fs->make<TH1F>("h_all_mutrack_nsthits",    "", 28,   0, 28);
    h_all_mutrack_npxlayers  = fs->make<TH1F>("h_all_mutrack_npxlayers",  "", 10,   0, 10);
    h_all_mutrack_nstlayers  = fs->make<TH1F>("h_all_mutrack_nstlayers",  "", 30,   0, 30);
    h_all_mutrack_minr       = fs->make<TH1F>("h_all_mutrack_minr", "", 6, 0, 6);

    for (int i = 0; i < 7; ++i) {
      h_seed_track_pars[i] = fs->make<TH1F>(TString::Format("h_seed_track_%s",    par_names[i]), "", par_nbins[i], par_lo[i], par_hi[i]);
      h_seed_track_errs[i] = fs->make<TH1F>(TString::Format("h_seed_track_err%s", par_names[i]), "", par_nbins[i], err_lo[i], err_hi[i]);
      h_seed_eletrack_pars[i] = fs->make<TH1F>(TString::Format("h_seed_eletrack_%s",    par_names[i]), "", par_nbins[i], par_lo[i], par_hi[i]);
      h_seed_eletrack_errs[i] = fs->make<TH1F>(TString::Format("h_seed_eletrack_err%s", par_names[i]), "", par_nbins[i], err_lo[i], err_hi[i]);
      h_seed_mutrack_pars[i] = fs->make<TH1F>(TString::Format("h_seed_mutrack_%s",    par_names[i]), "", par_nbins[i], par_lo[i], par_hi[i]);
      h_seed_mutrack_errs[i] = fs->make<TH1F>(TString::Format("h_seed_mutrack_err%s", par_names[i]), "", par_nbins[i], err_lo[i], err_hi[i]);
    }

    h_seed_track_p = fs->make<TH1F>("h_seed_track_p", "", 50, 0, 10);
    h_seed_track_pt_barrel = fs->make<TH1F>("h_seed_track_pt_barrel", "", 50, 0, 10);
    h_seed_track_pt_endcap = fs->make<TH1F>("h_seed_track_pt_endcap", "", 50, 0, 10);
    h_seed_track_sigmadxybs = fs->make<TH1F>("h_seed_track_sigmadxybs", "", 40, -10, 10);
    h_seed_track_sigmadxypv = fs->make<TH1F>("h_seed_track_sigmadxypv", "", 40, -10, 10);
    h_seed_track_pt_dxybs = fs->make<TH2F>("h_seed_track_pt_dxybs", "", 500, 0, 100, 500, -0.2, 0.2);
    h_seed_track_pt_errdxybs = fs->make<TH2F>("h_seed_track_pt_errdxybs", "", 500, 0, 100, 500, 0, 0.2);
    h_seed_track_nhits      = fs->make<TH1F>("h_seed_track_nhits",      "", 40,   0, 40);
    h_seed_track_npxhits    = fs->make<TH1F>("h_seed_track_npxhits",    "", 12,   0, 12);
    h_seed_track_nsthits    = fs->make<TH1F>("h_seed_track_nsthits",    "", 28,   0, 28);
    h_seed_track_npxlayers  = fs->make<TH1F>("h_seed_track_npxlayers",  "", 10,   0, 10);
    h_seed_track_nstlayers  = fs->make<TH1F>("h_seed_track_nstlayers",  "", 30,   0, 30);

    h_seed_nm1_pt = fs->make<TH1F>("h_seed_nm1_pt", "", 50, 0, 10);
    h_seed_nm1_npxlayers = fs->make<TH1F>("h_seed_nm1_npxlayers", "", 10, 0, 10);
    h_seed_nm1_nstlayers = fs->make<TH1F>("h_seed_nm1_nstlayers", "", 30, 0, 30);
    h_seed_nm1_sigmadxybs = fs->make<TH1F>("h_seed_nm1_sigmadxybs", "", 40, -10, 10);

    h_seed_eletrack_p = fs->make<TH1F>("h_seed_eletrack_p", "", 400, 0, 2000);
    h_seed_eletrack_pt_barrel = fs->make<TH1F>("h_seed_eletrack_pt_barrel", "", 400, 0, 2000);
    h_seed_eletrack_pt_endcap = fs->make<TH1F>("h_seed_eletrack_pt_endcap", "", 400, 0, 2000);
    h_seed_eletrack_sigmadxybs = fs->make<TH1F>("h_seed_eletrack_sigmadxybs", "", 40, 0, 20);
    h_seed_eletrack_sigmadxypv = fs->make<TH1F>("h_seed_eletrack_sigmadxypv", "", 40, 0, 20);
    // h_seed_eletrack_pt_dxybs = fs->make<TH2F>("h_seed_eletrack_pt_dxybs", "", 500, 0, 100, 500, 0, 2);
    // h_seed_eletrack_pt_errdxybs = fs->make<TH2F>("h_seed_eletrack_pt_errdxybs", "", 500, 0, 100, 500, 0, 0.2);
    h_seed_eletrack_nhits      = fs->make<TH1F>("h_seed_eletrack_nhits",      "", 40,   0, 40);
    h_seed_eletrack_npxhits    = fs->make<TH1F>("h_seed_eletrack_npxhits",    "", 12,   0, 12);
    h_seed_eletrack_nsthits    = fs->make<TH1F>("h_seed_eletrack_nsthits",    "", 28,   0, 28);
    h_seed_eletrack_npxlayers  = fs->make<TH1F>("h_seed_eletrack_npxlayers",  "", 10,   0, 10);
    h_seed_eletrack_nstlayers  = fs->make<TH1F>("h_seed_eletrack_nstlayers",  "", 30,   0, 30);

    h_seed_nm1_elept = fs->make<TH1F>("h_seed_nm1_elept", "", 400, 0, 2000);
    h_seed_nm1_elenpxlayers = fs->make<TH1F>("h_seed_nm1_elenpxlayers", "", 10, 0, 10);
    h_seed_nm1_elenstlayers = fs->make<TH1F>("h_seed_nm1_elenstlayers", "", 30, 0, 30);
    h_seed_nm1_eledxybs = fs->make<TH1F>("h_seed_nm1_eledxybs", "", 500, 0, 2);
    h_seed_nm1_eledxyerr = fs->make<TH1F>("h_seed_nm1_eledxyerr", "", 500, 0, 0.2);
    h_seed_nm1_elesigmadxybs = fs->make<TH1F>("h_seed_nm1_elesigmadxybs", "", 40, 0, 20);
    h_seed_nm1_eleminr = fs->make<TH1F>("h_seed_nm1_eleminr", "", 6, 0, 6);

    h_all_eletrack_minr_vs_pt = fs->make<TH2F>("h_all_eletrack_minr_vs_pt", "", 100, 0, 2000, 5, 0, 5);
    h_all_eletrack_dxybs_vs_pt = fs->make<TH2F>("h_all_eletrack_dxybs_vs_pt", "", 100, 0, 2000, 500, 0, 2);
    h_all_eletrack_dxyerr_vs_pt = fs->make<TH2F>("h_all_eletrack_dxyerr_vs_pt", "", 100, 0, 2000, 500, 0, 0.2);
    h_all_eletrack_sigmadxybs_vs_pt = fs->make<TH2F>("h_all_eletrack_sigmadxybs_vs_pt", "", 100, 0, 2000, 50, 0, 50);
    h_all_eletrack_npxlayers_vs_pt = fs->make<TH2F>("h_all_eletrack_npxlayers_vs_pt", "", 100, 0, 2000, 10, 0, 10);
    h_all_eletrack_nstlayers_vs_pt = fs->make<TH2F>("h_all_eletrack_nstlayers_vs_pt", "", 100, 0, 2000, 30, 0, 30);

    h_seed_track_dxybs_vs_pt = fs->make<TH2F>("h_seed_track_dxybs_vs_pt", "", 500, 0, 100, 500, 0, 2);
    h_seed_track_dxyerr_vs_pt = fs->make<TH2F>("h_seed_track_dxyerr_vs_pt", "", 500, 0, 100, 500, 0, 0.2);
    h_seed_track_sigmadxybs_vs_pt = fs->make<TH2F>("h_seed_track_sigmadxybs_vs_pt", "", 500, 0, 100, 50, 0, 50);

    h_seed_eletrack_minr_vs_pt = fs->make<TH2F>("h_seed_eletrack_minr_vs_pt", "", 100, 0, 2000, 5, 0, 5);
    h_seed_eletrack_dxybs_vs_pt = fs->make<TH2F>("h_seed_eletrack_dxybs_vs_pt", "", 100, 0, 2000, 500, 0, 2);
    h_seed_eletrack_dxyerr_vs_pt = fs->make<TH2F>("h_seed_eletrack_dxyerr_vs_pt", "", 100, 0, 2000, 500, 0, 0.2);
    h_seed_eletrack_sigmadxybs_vs_pt = fs->make<TH2F>("h_seed_eletrack_sigmadxybs_vs_pt", "", 100, 0, 2000, 50, 0, 50);
    h_seed_eletrack_npxlayers_vs_pt = fs->make<TH2F>("h_seed_eletrack_npxlayers_vs_pt", "", 100, 0, 2000, 10, 0, 10);
    h_seed_eletrack_nstlayers_vs_pt = fs->make<TH2F>("h_seed_eletrack_nstlayers_vs_pt", "", 100, 0, 2000, 30, 0, 30);

    h_all_eletrack_minr_vs_dxy = fs->make<TH2F>("h_all_eletrack_minr_vs_dxy", "", 100, 0, 5, 5, 0, 5);
    h_all_eletrack_sigmadxybs_vs_dxy = fs->make<TH2F>("h_all_eletrack_sigmadxybs_vs_dxy", "", 100, 0, 5, 50, 0, 50);
    h_all_eletrack_npxlayers_vs_dxy = fs->make<TH2F>("h_all_eletrack_npxlayers_vs_dxy", "", 100, 0, 5, 10, 0, 10);
    h_all_eletrack_nstlayers_vs_dxy = fs->make<TH2F>("h_all_eletrack_nstlayers_vs_dxy", "", 100, 0, 5, 30, 0, 30);
    h_all_eletrack_dxyerr_vs_dxy = fs->make<TH2F>("h_all_eletrack_dxyerr_vs_dxy", "", 100, 0, 5, 500, 0, 0.2);

    h_seed_eletrack_minr_vs_dxy = fs->make<TH2F>("h_seed_eletrack_minr_vs_dxy", "", 100, 0, 5, 5, 0, 5);
    h_seed_eletrack_sigmadxybs_vs_dxy = fs->make<TH2F>("h_seed_eletrack_sigmadxybs_vs_dxy", "", 100, 0, 5, 50, 0, 50);
    h_seed_eletrack_npxlayers_vs_dxy = fs->make<TH2F>("h_seed_eletrack_npxlayers_vs_dxy", "", 100, 0, 5, 10, 0, 10);
    h_seed_eletrack_nstlayers_vs_dxy = fs->make<TH2F>("h_seed_eletrack_nstlayers_vs_dxy", "", 100, 0, 5, 30, 0, 30);
    h_seed_eletrack_dxyerr_vs_dxy = fs->make<TH2F>("h_seed_eletrack_dxyerr_vs_dxy", "", 500, 0, 0.5, 20, 0, 0.02);

    h_seed_mutrack_p = fs->make<TH1F>("h_seed_mutrack_p", "", 400, 0, 2000);
    h_seed_mutrack_pt_barrel = fs->make<TH1F>("h_seed_mutrack_pt_barrel", "", 400, 0, 2000);
    h_seed_mutrack_pt_endcap = fs->make<TH1F>("h_seed_mutrack_pt_endcap", "", 400, 0, 2000);
    h_seed_mutrack_sigmadxybs = fs->make<TH1F>("h_seed_mutrack_sigmadxybs", "", 40, 0, 20);
    h_seed_mutrack_sigmadxypv = fs->make<TH1F>("h_seed_mutrack_sigmadxypv", "", 40, 0, 20);
    // h_seed_mutrack_pt_dxybs = fs->make<TH2F>("h_seed_mutrack_pt_dxybs", "", 500, 0, 100, 500, 0, 2);
    // h_seed_mutrack_pt_errdxybs = fs->make<TH2F>("h_seed_mutrack_pt_errdxybs", "", 500, 0, 100, 500, 0, 0.2);
    h_seed_mutrack_nhits      = fs->make<TH1F>("h_seed_mutrack_nhits",      "", 40,   0, 40);
    h_seed_mutrack_npxhits    = fs->make<TH1F>("h_seed_mutrack_npxhits",    "", 12,   0, 12);
    h_seed_mutrack_nsthits    = fs->make<TH1F>("h_seed_mutrack_nsthits",    "", 28,   0, 28);
    h_seed_mutrack_npxlayers  = fs->make<TH1F>("h_seed_mutrack_npxlayers",  "", 10,   0, 10);
    h_seed_mutrack_nstlayers  = fs->make<TH1F>("h_seed_mutrack_nstlayers",  "", 30,   0, 30);

    h_seed_nm1_mupt = fs->make<TH1F>("h_seed_nm1_mupt", "", 400, 0, 2000);
    h_seed_nm1_munpxlayers = fs->make<TH1F>("h_seed_nm1_munpxlayers", "", 10, 0, 10);
    h_seed_nm1_munstlayers = fs->make<TH1F>("h_seed_nm1_munstlayers", "", 30, 0, 30);
    h_seed_nm1_mudxybs = fs->make<TH1F>("h_seed_nm1_mudxybs", "", 500, 0, 2);
    h_seed_nm1_mudxyerr = fs->make<TH1F>("h_seed_nm1_mudxyerr", "", 500, 0, 0.2);
    h_seed_nm1_musigmadxybs = fs->make<TH1F>("h_seed_nm1_musigmadxybs", "", 40, 0, 20);
    h_seed_nm1_muminr = fs->make<TH1F>("h_seed_nm1_minr", "", 6, 0, 6);

    h_all_mutrack_minr_vs_pt = fs->make<TH2F>("h_all_mutrack_minr_vs_pt", "", 100, 0, 2000, 5, 0, 5);
    h_all_mutrack_dxybs_vs_pt = fs->make<TH2F>("h_all_mutrack_dxybs_vs_pt", "", 100, 0, 2000, 500, 0, 2);
    h_all_mutrack_dxyerr_vs_pt = fs->make<TH2F>("h_all_mutrack_dxyerr_vs_pt", "", 100, 0, 2000, 500, 0, 0.2);
    h_all_mutrack_sigmadxybs_vs_pt = fs->make<TH2F>("h_all_mutrack_sigmadxybs_vs_pt", "", 100, 0, 2000, 50, 0, 50);
    h_all_mutrack_npxlayers_vs_pt = fs->make<TH2F>("h_all_mutrack_npxlayers_vs_pt", "", 100, 0, 2000, 10, 0, 10);
    h_all_mutrack_nstlayers_vs_pt = fs->make<TH2F>("h_all_mutrack_nstlayers_vs_pt", "", 100, 0, 2000, 30, 0, 30);

    h_seed_mutrack_minr_vs_pt = fs->make<TH2F>("h_seed_mutrack_minr_vs_pt", "", 100, 0, 2000, 5, 0, 5);
    h_seed_mutrack_dxybs_vs_pt = fs->make<TH2F>("h_seed_mutrack_dxybs_vs_pt", "", 100, 0, 2000, 500, 0, 2);
    h_seed_mutrack_dxyerr_vs_pt = fs->make<TH2F>("h_seed_mutrack_dxyerr_vs_pt", "", 100, 0, 2000, 500, 0, 0.2);
    h_seed_mutrack_sigmadxybs_vs_pt = fs->make<TH2F>("h_seed_mutrack_sigmadxybs_vs_pt", "", 100, 0, 2000, 50, 0, 50);
    h_seed_mutrack_npxlayers_vs_pt = fs->make<TH2F>("h_seed_mutrack_npxlayers_vs_pt", "", 100, 0, 2000, 10, 0, 10);
    h_seed_mutrack_nstlayers_vs_pt = fs->make<TH2F>("h_seed_mutrack_nstlayers_vs_pt", "", 100, 0, 2000, 30, 0, 30);

    h_all_mutrack_minr_vs_dxy = fs->make<TH2F>("h_all_mutrack_minr_vs_dxy", "", 100, 0, 5, 5, 0, 5);
    h_all_mutrack_sigmadxybs_vs_dxy = fs->make<TH2F>("h_all_mutrack_sigmadxybs_vs_dxy", "", 100, 0, 5, 50, 0, 50);
    h_all_mutrack_npxlayers_vs_dxy = fs->make<TH2F>("h_all_mutrack_npxlayers_vs_dxy", "", 100, 0, 5, 10, 0, 10);
    h_all_mutrack_nstlayers_vs_dxy = fs->make<TH2F>("h_all_mutrack_nstlayers_vs_dxy", "", 100, 0, 5, 30, 0, 30);
    h_all_mutrack_dxyerr_vs_dxy = fs->make<TH2F>("h_all_mutrack_dxyerr_vs_dxy", "", 100, 0, 5, 500, 0, 0.2);

    h_seed_mutrack_minr_vs_dxy = fs->make<TH2F>("h_seed_mutrack_minr_vs_dxy", "", 100, 0, 5, 5, 0, 5);
    h_seed_mutrack_sigmadxybs_vs_dxy = fs->make<TH2F>("h_seed_mutrack_sigmadxybs_vs_dxy", "", 100, 0, 5, 50, 0, 50);
    h_seed_mutrack_npxlayers_vs_dxy = fs->make<TH2F>("h_seed_mutrack_npxlayers_vs_dxy", "", 100, 0, 5, 10, 0, 10);
    h_seed_mutrack_nstlayers_vs_dxy = fs->make<TH2F>("h_seed_mutrack_nstlayers_vs_dxy", "", 100, 0, 5, 30, 0, 30);
    h_seed_mutrack_dxyerr_vs_dxy = fs->make<TH2F>("h_seed_mutrack_dxyerr_vs_dxy", "", 500, 0, 0.5, 20, 0, 0.02);
  }
}

bool MFVVertexTracks::filter(edm::Event& event, const edm::EventSetup& setup) {
  if (verbose)
    std::cout << "MFVVertexTracks " << module_label << " run " << event.id().run() << " lumi " << event.luminosityBlock() << " event " << event.id().event() << "\n";

  const int track_rescaler_which = jmt::TrackRescaler::w_JetHT; // JMTBAD which rescaling if ever a different one
  track_rescaler.setup(!event.isRealData() && track_rescaler_which != -1 && min_track_rescaled_sigmadxy > 0,
                       jmt::AnalysisEras::pick(event, this),
                       track_rescaler_which);

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
  std::unique_ptr<std::vector<reco::TrackRef>> all_electron_tracks (new std::vector<reco::TrackRef>);
  std::unique_ptr<std::vector<reco::TrackRef>> all_muon_tracks (new std::vector<reco::TrackRef>);
  std::unique_ptr<std::vector<reco::TrackRef>> electron_seed_tracks(new std::vector<reco::TrackRef>);
  std::unique_ptr<std::vector<reco::TrackRef>> muon_seed_tracks(new std::vector<reco::TrackRef>);
  std::unique_ptr<reco::TrackCollection> seed_tracks_copy(new reco::TrackCollection);
  std::unique_ptr<std::vector<reco::TrackRef>> quality_tracks(new std::vector<reco::TrackRef>);
  std::unique_ptr<reco::TrackCollection> quality_tracks_copy(new reco::TrackCollection);

  std::vector<reco::TrackRef> seed_track_loose;

  if (!disregard_event) {
    if (use_tracks) {
      edm::Handle<reco::TrackCollection> tracks;
      event.getByToken(tracks_token, tracks);
      for (size_t i = 0, ie = tracks->size(); i < ie; ++i)
        all_tracks->push_back(reco::TrackRef(tracks, i));
    }
    if (use_separated_leptons) { 
      edm::Handle<reco::TrackCollection> muon_tracks;
      event.getByToken(muon_tracks_token, muon_tracks);
      for (size_t i = 0, im = muon_tracks->size(); i < im; ++i) 
        all_muon_tracks->push_back(reco::TrackRef(muon_tracks, i));

      edm::Handle<reco::TrackCollection> electron_tracks;
      event.getByToken(electron_tracks_token, electron_tracks);
      for (size_t i = 0, ie = electron_tracks->size(); i < ie; ++i) 
        all_electron_tracks->push_back(reco::TrackRef(electron_tracks, i));
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
    const auto rs = track_rescaler.scale(*tk);
    const bool is_second_track = i >= second_tracks_start_at;

    // copy/calculate cheap things, which may be used later in histos
    const double p = tk->p();
    const double pt = tk->pt();
    const double eta = tk->eta();
    const double phi = tk->phi();
    const double dxybs = tk->dxy(*beamspot);
    const double dxypv = primary_vertex ? tk->dxy(primary_vertex->position()) : 1e99;
    const double dxyerr = tk->dxyError();
    const double rescaled_dxyerr = rs.rescaled_tk.dxyError();
    const double sigmadxybs = dxybs / dxyerr;
    const double rescaled_sigmadxybs = dxybs / rescaled_dxyerr;
    const double sigmadxypv = dxypv / dxyerr;
    const int nhits = tk->hitPattern().numberOfValidHits();
    const int npxhits = tk->hitPattern().numberOfValidPixelHits();
    const int nsthits = tk->hitPattern().numberOfValidStripHits();
    const int npxlayers = tk->hitPattern().pixelLayersWithMeasurement();
    const int nstlayers = tk->hitPattern().stripLayersWithMeasurement();
    const auto trackLostInnerHits = tk->hitPattern().numberOfLostHits(reco::HitPattern::MISSING_INNER_HITS);
    int min_r = 2000000000;
    for (int i = 1; i <= 4; ++i)
      if (tk->hitPattern().hasValidHitInPixelLayer(PixelSubdetector::PixelBarrel,i)) {
        min_r = i;
        break;
      }

    bool use = no_track_cuts || is_second_track || [&]() {

      //this is for low pt leptons & general tracks 
      const bool use_cheap =
        pt > min_track_pt &&
        fabs(dxybs) > min_track_dxy &&
        dxyerr < max_track_dxyerr &&
        fabs(sigmadxybs) > min_track_sigmadxy &&
        fabs(rescaled_sigmadxybs) > min_track_rescaled_sigmadxy &&
        fabs(sigmadxypv) > min_track_sigmadxypv &&
        nhits >= min_track_nhits &&
        npxhits >= min_track_npxhits &&
        npxlayers >= min_track_npxlayers &&
        nstlayers >= min_track_nstlayers &&
        (min_track_hit_r == 999 || min_r <= min_track_hit_r || (min_r == 2.0 && trackLostInnerHits == 0 ));
      
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
    else if (match_jets){
      const bool use_loose =
        pt > min_track_pt_loose &&
        fabs(dxybs) > min_track_dxy &&
        dxyerr < max_track_dxyerr &&
        fabs(sigmadxybs) > min_track_sigmadxy &&
        fabs(rescaled_sigmadxybs) > min_track_rescaled_sigmadxy_loose &&
        fabs(sigmadxypv) > min_track_sigmadxypv &&
        nhits >= min_track_nhits &&
        npxhits >= min_track_npxhits &&
        npxlayers >= min_track_npxlayers &&
        nstlayers >= min_track_nstlayers &&
        (min_track_hit_r == 999 || min_r <= min_track_hit_r || (min_r == 2.0 && trackLostInnerHits == 0));
      if (use_loose){
        seed_track_loose.push_back(tk);
      }
    }
    else if (save_quality_tracks){
      const bool use_loose =
        pt > min_track_pt &&
        fabs(dxybs) > min_track_dxy &&
        dxyerr < max_track_dxyerr &&
        fabs(sigmadxybs) > min_track_sigmadxy &&
        fabs(rescaled_sigmadxybs) > min_track_rescaled_sigmadxy_loose &&
        fabs(sigmadxypv) > min_track_sigmadxypv &&
        nhits >= min_track_nhits &&
        npxhits >= min_track_npxhits &&
        npxlayers >= min_track_npxlayers &&
        nstlayers >= min_track_nstlayers &&
        (min_track_hit_r == 999 || min_r <= min_track_hit_r || (min_r == 2.0 && trackLostInnerHits == 0));
      if (use_loose){
        quality_tracks->push_back(tk);
        quality_tracks_copy->push_back(*tk);
      }
    }

    if (verbose) {
      printf("track %5lu: pt: %10.3f +- %10.3f eta: %10.3f +- %10.3f phi: %10.3f +- %10.3f dxy: %10.5f +- %10.5f (-> nsig %5.3f, rescaled: %10.5f +- %10.5f -> nsig %10.3f) dz: %10.3f +- %10.3f nhits: %3i/%3i/%3i nlayers: %3i/%3i/%3i ", i, pt, tk->ptError(), tk->eta(), tk->etaError(), tk->phi(), tk->phiError(), dxybs, dxyerr, fabs(sigmadxybs), dxybs, rescaled_dxyerr, fabs(rescaled_sigmadxybs), tk->dz(), tk->dzError(), npxhits, nsthits, nhits, npxlayers, nstlayers, npxlayers + nstlayers);
      if (use)
        printf(" selected for seed! (#%lu)", seed_tracks->size()-1);
      printf("\n");
    }

    if (histos) {
      const double pars[7] = {pt, tk->eta(), tk->phi(), dxybs, dxybs, dxypv, tk->dz(beamspot->position()) };
      const double errs[7] = { tk->ptError(), tk->etaError(), tk->phiError(), tk->dxyError(), rescaled_dxyerr, tk->dxyError(), tk->dzError() };

      for (int i = 0; i < 7; ++i) {
        h_all_track_pars[i]->Fill(pars[i]);
        h_all_track_errs[i]->Fill(errs[i]);
      }

      h_all_track_p->Fill(p);
      if (abs(tk->eta())<1.4){
        h_all_track_pt_barrel->Fill(pt);
      }
      else{
        h_all_track_pt_endcap->Fill(pt);
      }
      h_all_track_sigmadxybs->Fill(sigmadxybs);
      h_all_track_sigmadxypv->Fill(sigmadxypv);
      h_all_track_pt_dxybs->Fill(pt, dxybs);
      h_all_track_pt_errdxybs->Fill(pt, tk->dxyError());
      h_all_track_nhits->Fill(nhits);
      h_all_track_npxhits->Fill(npxhits);
      h_all_track_nsthits->Fill(nsthits);
      h_all_track_npxlayers->Fill(npxlayers);
      h_all_track_nstlayers->Fill(nstlayers);

      const bool nm1[5] = {
        pt > min_track_pt,
        npxlayers >= min_track_npxlayers,
        nstlayers >= min_track_nstlayers,
        fabs(rescaled_sigmadxybs) > min_track_rescaled_sigmadxy, // JMTBAD rescaled_sigmadxybs
      };
      if (min_track_hit_r == 999 || min_r <= min_track_hit_r || (min_r == 2.0 && trackLostInnerHits == 0)){
          if (nm1[1] && nm1[2] && nm1[3]) h_seed_nm1_pt->Fill(pt);
          if (nm1[0] && nm1[2] && nm1[3]) h_seed_nm1_npxlayers->Fill(npxlayers);
          if (nm1[0] && nm1[1] && nm1[3]) h_seed_nm1_nstlayers->Fill(nstlayers);
          if (nm1[0] && nm1[1] && nm1[2]) h_seed_nm1_sigmadxybs->Fill(rescaled_sigmadxybs);
          if (nm1[1] && nm1[2]) {
             h_seed_track_dxybs_vs_pt->Fill(pt, fabs(dxybs));
             h_seed_track_dxyerr_vs_pt->Fill(pt, dxyerr);
             h_seed_track_sigmadxybs_vs_pt->Fill(pt, fabs(sigmadxybs));
          }
      }

      if (use) {
        for (int i = 0; i < 7; ++i) {
          h_seed_track_pars[i]->Fill(pars[i]);
          h_seed_track_errs[i]->Fill(errs[i]);
        }

        h_seed_track_p->Fill(p);
        if (abs(tk->eta())<1.4){
          h_seed_track_pt_barrel->Fill(pt);
        }
        else{
          h_seed_track_pt_endcap->Fill(pt);
        }
        h_seed_track_sigmadxybs->Fill(rescaled_sigmadxybs);
        h_seed_track_sigmadxypv->Fill(sigmadxypv);
        h_seed_track_pt_dxybs->Fill(pt, dxybs);
        h_seed_track_pt_errdxybs->Fill(pt, tk->dxyError());
        h_seed_track_nhits->Fill(nhits);
        h_seed_track_npxhits->Fill(npxhits);
        h_seed_track_nsthits->Fill(nsthits);
        h_seed_track_npxlayers->Fill(npxlayers);
        h_seed_track_nstlayers->Fill(nstlayers);
        
      }
    }
  }
  if (match_jets){
    if(verbose){
      std::cout << "seed tracks before matching with jets: ";
      for (const auto& tk:*seed_tracks){
        std::cout << " " << tk.key();
      }
      std::cout << std::endl;
    }
    edm::Handle<pat::JetCollection> jets;
    event.getByToken(match_jet_token, jets);
    std::set<size_t> decay_jets;
    for (size_t itk=0; itk<seed_tracks->size(); ++itk){
      for (size_t j=0; j<jets->size(); ++j){
        if (match_track_jet(*(*seed_tracks)[itk], (*jets)[j])){
          decay_jets.insert(j);
          if(verbose)
            std::cout << "track " << (*seed_tracks)[itk].key() << " matched with jet " << j << std::endl;
        }
      }
    }
    if(verbose){
      std::cout << "matched jets: ";
      for (const auto& j:decay_jets){
        std::cout << " " << j;
      }
      std::cout << std::endl;
    }
    for (const reco::TrackRef& itk:seed_track_loose){
      for (size_t j:decay_jets){
        if(verbose)
          std::cout << "trying to match track " << itk.key() << " with jet " << j << std::endl;
        if (match_track_jet(*itk, (*jets)[j])){
          if(verbose)
            std::cout << "  track matched, adding to seed tracks: " << itk.key() << std::endl;
          seed_tracks->push_back(itk);
          seed_tracks_copy->push_back(*itk);
          break;
        }
      }
    }
  }
  // now we get to do this all over for lepton tracks ... (with electrons and muons separate) 
  if (use_separated_leptons) {
    for (size_t i = 0, im = all_muon_tracks->size(); i < im; ++i) {
      const reco::TrackRef& mtk = (*all_muon_tracks)[i];
      //this will need to be changed once we have a different(?) track rescaler for leptons ... 
      const auto rs = track_rescaler.scale(*mtk);
      //copy/calculate the cheap things but now for muons ... 
      const double p = mtk->p(); //don't need it yet 
      const double pt = mtk->pt();
      const double dxybs = mtk->dxy(*beamspot);
      const double dxypv = primary_vertex ? mtk->dxy(primary_vertex->position()) : 1e99;
      const double dxyerr = mtk->dxyError();
      const double rescaled_dxyerr = rs.rescaled_tk.dxyError();
      const double sigmadxybs = dxybs / dxyerr;
      const double rescaled_sigmadxybs = dxybs / rescaled_dxyerr;
      const double sigmadxypv = dxypv / dxyerr;
      const int nhits = mtk->hitPattern().numberOfValidHits();
      const int npxhits = mtk->hitPattern().numberOfValidPixelHits();
      const int nsthits = mtk->hitPattern().numberOfValidStripHits(); 
      const int npxlayers = mtk->hitPattern().pixelLayersWithMeasurement();
      const int nstlayers = mtk->hitPattern().stripLayersWithMeasurement();
      int min_r = 2000000000;
      for (int i = 1; i <= 4; ++i)
        if (mtk->hitPattern().hasValidHitInPixelLayer(PixelSubdetector::PixelBarrel,i)) {
          min_r = i;
          break;
        }
      int losthits = mtk->hitPattern().numberOfLostHits(reco::HitPattern::MISSING_INNER_HITS);
      bool use_mu = no_track_cuts || [&]() {

        //this min lep pt is hard coded during the split -- hence hard coded here
        const bool use_cheap =
          pt >= 20.0 &&
          fabs(dxybs) > min_track_dxy &&
          dxyerr < max_track_dxyerr &&
          fabs(sigmadxybs) > min_track_sigmadxy &&
          fabs(rescaled_sigmadxybs) > min_leptrack_rescaled_sigmadxy &&
          fabs(sigmadxypv) > min_track_sigmadxypv &&
          nhits >= min_track_nhits &&
          npxhits >= min_track_npxhits &&
          npxlayers >= min_track_npxlayers &&
          nstlayers >= min_track_nstlayers &&
          (min_track_hit_r == 999 || (min_r <= min_leptrack_hit_r && losthits == 0) || min_r <= min_track_hit_r);
          
        if (!use_cheap) return false;

        if (primary_vertex && (max_track_dxyipverr > 0 || max_track_d3dipverr > 0)) {
          reco::TransientTrack ttk = tt_builder->build(mtk);
          if (max_track_dxyipverr > 0) {
            auto dxy_ipv = IPTools::absoluteTransverseImpactParameter(ttk, *primary_vertex); if (!dxy_ipv.first || dxy_ipv.second.error() >= max_track_dxyipverr) return false;
          }
          if (max_track_d3dipverr > 0) {
            auto d3d_ipv = IPTools::absoluteImpactParameter3D        (ttk, *primary_vertex); if (!d3d_ipv.first || d3d_ipv.second.error() >= max_track_d3dipverr) return false;
          }
        }

        return true;
      }();

      if (use_mu) {
        seed_tracks->push_back(mtk);
        muon_seed_tracks->push_back(mtk);
        seed_tracks_copy->push_back(*mtk);
        
      }  

      if (verbose) {
        printf("track %5lu: pt: %10.3f +- %10.3f eta: %10.3f +- %10.3f phi: %10.3f +- %10.3f dxy: %10.5f +- %10.5f (-> nsig %5.3f, rescaled: %10.5f +- %10.5f -> nsig %10.3f) dz: %10.3f +- %10.3f nhits: %3i/%3i/%3i nlayers: %3i/%3i/%3i ", i, pt, mtk->ptError(), mtk->eta(), mtk->etaError(), mtk->phi(), mtk->phiError(), dxybs, dxyerr, fabs(sigmadxybs), dxybs, rescaled_dxyerr, fabs(rescaled_sigmadxybs), mtk->dz(), mtk->dzError(), npxhits, nsthits, nhits, npxlayers, nstlayers, npxlayers + nstlayers);
        if (use_mu)
          printf(" muon selected for seed! (#%lu)", seed_tracks->size()-1);
        printf("\n");
      }

      if (histos) {
        const double pars[7] = {pt, mtk->eta(), mtk->phi(), fabs(dxybs), fabs(dxybs), fabs(dxypv), mtk->dz(beamspot->position()) };
        const double errs[7] = { mtk->ptError(), mtk->etaError(), mtk->phiError(), mtk->dxyError(), rescaled_dxyerr, mtk->dxyError(), mtk->dzError() };

        for (int i = 0; i < 7; ++i) {
          h_all_mutrack_pars[i]->Fill(pars[i]);
          h_all_mutrack_errs[i]->Fill(errs[i]);
        }

        h_all_mutrack_p->Fill(p);
        if (abs(mtk->eta())<1.4){
          h_all_mutrack_pt_barrel->Fill(pt);
        }
        else{
          h_all_mutrack_pt_endcap->Fill(pt);
        }
        h_all_mutrack_sigmadxybs->Fill(fabs(sigmadxybs));
        h_all_mutrack_sigmadxypv->Fill(fabs(sigmadxypv));
        // h_all_mutrack_pt_dxybs->Fill(pt, dxybs);
        // h_all_mutrack_pt_errdxybs->Fill(pt, mtk->dxyError());
        h_all_mutrack_nhits->Fill(nhits);
        h_all_mutrack_npxhits->Fill(npxhits);
        h_all_mutrack_nsthits->Fill(nsthits);
        h_all_mutrack_npxlayers->Fill(npxlayers);
        h_all_mutrack_nstlayers->Fill(nstlayers);
        h_all_mutrack_minr->Fill(min_r);
        h_all_mutrack_minr_vs_pt->Fill(pt, min_r); 
        h_all_mutrack_dxybs_vs_pt->Fill(pt, fabs(dxybs));
        h_all_mutrack_dxyerr_vs_pt->Fill(pt, dxyerr);
        h_all_mutrack_sigmadxybs_vs_pt->Fill(pt, fabs(sigmadxybs));
        h_all_mutrack_npxlayers_vs_pt->Fill(pt, npxlayers);
        h_all_mutrack_nstlayers_vs_pt->Fill(pt, nstlayers);
        h_all_mutrack_minr_vs_dxy->Fill(fabs(dxybs), min_r); 
        h_all_mutrack_sigmadxybs_vs_dxy->Fill(fabs(dxybs), fabs(sigmadxybs));
        h_all_mutrack_npxlayers_vs_dxy->Fill(fabs(dxybs), npxlayers);
        h_all_mutrack_nstlayers_vs_dxy->Fill(fabs(dxybs), nstlayers);
        h_all_mutrack_dxyerr_vs_dxy->Fill(fabs(dxybs), dxyerr);

        const bool nm1[5] = {
          pt > min_track_pt,
          npxlayers >= min_track_npxlayers,
          nstlayers >= min_track_nstlayers,
          fabs(sigmadxybs) > 3, // JMTBAD rescaled_sigmadxybs
          (min_r <= min_leptrack_hit_r && losthits == 0) || min_r <= min_track_hit_r
        };

        if (nm1[1] && nm1[2] && nm1[3] && nm1[4]) h_seed_nm1_mupt->Fill(pt);
        if (nm1[0] && nm1[2] && nm1[3] && nm1[4]) h_seed_nm1_munpxlayers->Fill(npxlayers);
        if (nm1[0] && nm1[1] && nm1[3] && nm1[4]) h_seed_nm1_munstlayers->Fill(nstlayers);
        if (nm1[0] && nm1[1] && nm1[2] && nm1[4]) {
          h_seed_nm1_mudxybs->Fill(fabs(dxybs));
          h_seed_nm1_mudxyerr->Fill(dxyerr);
          h_seed_nm1_musigmadxybs->Fill(fabs(sigmadxybs));
        }
        if (nm1[0] && nm1[1] && nm1[2] && nm1[3]) h_seed_nm1_muminr->Fill(min_r);

        if (nm1[1] && nm1[2] && nm1[4]) {
          h_seed_mutrack_dxybs_vs_pt->Fill(pt, fabs(dxybs));
          h_seed_mutrack_dxyerr_vs_pt->Fill(pt, dxyerr);
          h_seed_mutrack_sigmadxybs_vs_pt->Fill(pt, fabs(sigmadxybs));
          h_seed_mutrack_sigmadxybs_vs_dxy->Fill(fabs(dxybs), fabs(sigmadxybs));
          h_seed_mutrack_dxyerr_vs_dxy->Fill(fabs(dxybs), dxyerr);
        }
        if (nm1[2] && nm1[3] && nm1[4]) {
          h_seed_mutrack_npxlayers_vs_pt->Fill(pt, npxlayers);
          h_seed_mutrack_npxlayers_vs_dxy->Fill(fabs(dxybs), npxlayers);
        }
        if (nm1[1] && nm1[3] && nm1[4]) {
          h_seed_mutrack_nstlayers_vs_pt->Fill(pt, nstlayers);
          h_seed_mutrack_nstlayers_vs_dxy->Fill(fabs(dxybs), nstlayers);
        } 
        if (nm1[1] && nm1[2] && nm1[3]) {
          h_seed_mutrack_minr_vs_pt->Fill(pt, min_r);
          h_seed_mutrack_minr_vs_dxy->Fill(fabs(dxybs), min_r);
        }
        if (use_mu) {
          for (int i = 0; i < 7; ++i) {
            h_seed_mutrack_pars[i]->Fill(pars[i]);
            h_seed_mutrack_errs[i]->Fill(errs[i]);
          }

          h_seed_mutrack_p->Fill(p);
          if (abs(mtk->eta())<1.4){
            h_seed_mutrack_pt_barrel->Fill(pt);
          }
          else{
            h_seed_mutrack_pt_endcap->Fill(pt);
          }
          h_seed_mutrack_sigmadxybs->Fill(fabs(sigmadxybs));
          h_seed_mutrack_sigmadxypv->Fill(fabs(sigmadxypv));
          // h_seed_mutrack_pt_dxybs->Fill(pt, fabs(dxybs));
          // h_seed_mutrack_pt_errdxybs->Fill(pt, mtk->dxyError());
          h_seed_mutrack_nhits->Fill(nhits);
          h_seed_mutrack_npxhits->Fill(npxhits);
          h_seed_mutrack_nsthits->Fill(nsthits);
          h_seed_mutrack_npxlayers->Fill(npxlayers);
          h_seed_mutrack_nstlayers->Fill(nstlayers);
        }
      }
      
    }
    for (size_t i = 0, ie = all_electron_tracks->size(); i < ie; ++i) {
      const reco::TrackRef& etk = (*all_electron_tracks)[i];
      //this will need to be changed once we have a different(?) track rescaler for leptons ... ?
      const auto rs = track_rescaler.scale(*etk);

      //copy/calculate the cheap things but now for electrons ... 
      const double p = etk->p(); //don't need it yet
      const double pt = etk->pt();
      const double dxybs = etk->dxy(*beamspot);
      const double dxypv = primary_vertex ? etk->dxy(primary_vertex->position()) : 1e99;
      const double dxyerr = etk->dxyError();
      const double rescaled_dxyerr = rs.rescaled_tk.dxyError();
      const double sigmadxybs = dxybs / dxyerr;
      const double rescaled_sigmadxybs = dxybs / rescaled_dxyerr;
      const double sigmadxypv = dxypv / dxyerr;
      const int nhits = etk->hitPattern().numberOfValidHits();
      const int npxhits = etk->hitPattern().numberOfValidPixelHits();
      const int nsthits = etk->hitPattern().numberOfValidStripHits(); 
      const int npxlayers = etk->hitPattern().pixelLayersWithMeasurement();
      const int nstlayers = etk->hitPattern().stripLayersWithMeasurement();

      int min_r = 2000000000;
      for (int i = 1; i <= 4; ++i)
        if (etk->hitPattern().hasValidHitInPixelLayer(PixelSubdetector::PixelBarrel,i)) {
          min_r = i;
          break;
        }
      int losthits = etk->hitPattern().numberOfLostHits(reco::HitPattern::MISSING_INNER_HITS);
      bool use_ele = no_track_cuts || [&]() {

        //this min lep pt is hard coded during the split -- hence hard coded here
        const bool use_cheap =
          pt >= 20.0 &&
          fabs(dxybs) > min_track_dxy &&
          dxyerr < max_track_dxyerr &&
          fabs(sigmadxybs) > min_track_sigmadxy &&
          fabs(rescaled_sigmadxybs) > 3 &&
          //fabs(rescaled_sigmadxybs) > min_leptrack_rescaled_sigmadxy &&
          fabs(sigmadxypv) > min_track_sigmadxypv &&
          nhits >= min_track_nhits &&
          npxhits >= min_track_npxhits &&
          npxlayers >= min_track_npxlayers &&
          nstlayers >= min_track_nstlayers &&
          (min_track_hit_r == 999 || (min_r <= min_leptrack_hit_r && losthits == 0) || min_r <= min_track_hit_r);
          //(min_track_hit_r == 999 || (min_r <= 3));

        if (!use_cheap) return false;

        if (primary_vertex && (max_track_dxyipverr > 0 || max_track_d3dipverr > 0)) {
          reco::TransientTrack ttk = tt_builder->build(etk);
          if (max_track_dxyipverr > 0) {
            auto dxy_ipv = IPTools::absoluteTransverseImpactParameter(ttk, *primary_vertex); if (!dxy_ipv.first || dxy_ipv.second.error() >= max_track_dxyipverr) return false;
          }
          if (max_track_d3dipverr > 0) {
            auto d3d_ipv = IPTools::absoluteImpactParameter3D        (ttk, *primary_vertex); if (!d3d_ipv.first || d3d_ipv.second.error() >= max_track_d3dipverr) return false;
          }
        }

        return true;
      }();
      if (use_ele) {
        seed_tracks->push_back(etk);
        electron_seed_tracks->push_back(etk);
        seed_tracks_copy->push_back(*etk);
      }
      if (verbose) {
        printf("track %5lu: pt: %10.3f +- %10.3f eta: %10.3f +- %10.3f phi: %10.3f +- %10.3f dxy: %10.5f +- %10.5f (-> nsig %5.3f, rescaled: %10.5f +- %10.5f -> nsig %10.3f) dz: %10.3f +- %10.3f nhits: %3i/%3i/%3i nlayers: %3i/%3i/%3i ", i, pt, etk->ptError(), etk->eta(), etk->etaError(), etk->phi(), etk->phiError(), dxybs, dxyerr, fabs(sigmadxybs), dxybs, rescaled_dxyerr, fabs(rescaled_sigmadxybs), etk->dz(), etk->dzError(), npxhits, nsthits, nhits, npxlayers, nstlayers, npxlayers + nstlayers);
        std::cout << "min_r : " << min_r << "lost hits : " << losthits << std::endl;
        if (use_ele)
          printf(" ele selected for seed! (#%lu)", seed_tracks->size()-1);
        printf("\n");
      }
      if (histos) {
        const double pars[7] = {pt, etk->eta(), etk->phi(), fabs(dxybs), fabs(dxybs), fabs(dxypv), etk->dz(beamspot->position()) };
        const double errs[7] = { etk->ptError(), etk->etaError(), etk->phiError(), etk->dxyError(), rescaled_dxyerr, etk->dxyError(), etk->dzError() };

        for (int i = 0; i < 7; ++i) {
          h_all_eletrack_pars[i]->Fill(pars[i]);
          h_all_eletrack_errs[i]->Fill(errs[i]);
        }

        h_all_eletrack_p->Fill(p);
        if (abs(etk->eta())<1.4){
          h_all_eletrack_pt_barrel->Fill(pt);
        }
        else{
          h_all_eletrack_pt_endcap->Fill(pt);
        }
        h_all_eletrack_sigmadxybs->Fill(fabs(sigmadxybs));
        h_all_eletrack_sigmadxypv->Fill(fabs(sigmadxypv));
        // h_all_eletrack_pt_dxybs->Fill(pt, fabs(dxybs));
        // h_all_eletrack_pt_errdxybs->Fill(pt, etk->dxyError());
        h_all_eletrack_nhits->Fill(nhits);
        h_all_eletrack_npxhits->Fill(npxhits);
        h_all_eletrack_nsthits->Fill(nsthits);
        h_all_eletrack_npxlayers->Fill(npxlayers);
        h_all_eletrack_nstlayers->Fill(nstlayers);
        h_all_eletrack_minr->Fill(min_r);

        h_all_eletrack_minr_vs_pt->Fill(pt, min_r); 
        h_all_eletrack_dxybs_vs_pt->Fill(pt, fabs(dxybs));
        h_all_eletrack_dxyerr_vs_pt->Fill(pt, dxyerr);
        h_all_eletrack_sigmadxybs_vs_pt->Fill(pt, fabs(sigmadxybs));
        h_all_eletrack_npxlayers_vs_pt->Fill(pt, npxlayers);
        h_all_eletrack_nstlayers_vs_pt->Fill(pt, nstlayers);

        h_all_eletrack_minr_vs_dxy->Fill(fabs(dxybs), min_r); 
        h_all_eletrack_sigmadxybs_vs_dxy->Fill(fabs(dxybs), fabs(sigmadxybs));
        h_all_eletrack_npxlayers_vs_dxy->Fill(fabs(dxybs), npxlayers);
        h_all_eletrack_nstlayers_vs_dxy->Fill(fabs(dxybs), nstlayers);
        h_all_eletrack_dxyerr_vs_dxy->Fill(fabs(dxybs), dxyerr);

        const bool nm1[5] = {
          pt > min_track_pt,
          npxlayers >= min_track_npxlayers,
          nstlayers >= min_track_nstlayers,
          fabs(sigmadxybs) > 3, // JMTBAD rescaled_sigmadxybs
          (min_r <= min_leptrack_hit_r && losthits == 0) || min_r <= min_track_hit_r
        };

        if (nm1[1] && nm1[2] && nm1[3] && nm1[4]) h_seed_nm1_elept->Fill(pt);
        if (nm1[0] && nm1[2] && nm1[3] && nm1[4]) h_seed_nm1_elenpxlayers->Fill(npxlayers);
        if (nm1[0] && nm1[1] && nm1[3] && nm1[4]) h_seed_nm1_elenstlayers->Fill(nstlayers);
        if (nm1[0] && nm1[1] && nm1[2] && nm1[4]) {
          h_seed_nm1_eledxybs->Fill(fabs(dxybs));
          h_seed_nm1_eledxyerr->Fill(dxyerr);
          h_seed_nm1_elesigmadxybs->Fill(fabs(sigmadxybs));
        }
        if (nm1[0] && nm1[1] && nm1[2] && nm1[3]) h_seed_nm1_eleminr->Fill(min_r);

        if (nm1[1] && nm1[2] && nm1[4]) {
          h_seed_eletrack_dxybs_vs_pt->Fill(pt, fabs(dxybs));
          h_seed_eletrack_dxyerr_vs_pt->Fill(pt, dxyerr);
          h_seed_eletrack_sigmadxybs_vs_pt->Fill(pt, fabs(sigmadxybs));
          h_seed_eletrack_sigmadxybs_vs_dxy->Fill(fabs(dxybs), fabs(sigmadxybs));
          h_seed_eletrack_dxyerr_vs_dxy->Fill(fabs(dxybs), dxyerr);
        }
        if (nm1[2] && nm1[3] && nm1[4]) {
          h_seed_eletrack_npxlayers_vs_pt->Fill(pt, npxlayers);
          h_seed_eletrack_npxlayers_vs_dxy->Fill(fabs(dxybs), npxlayers);
        }
        if (nm1[1] && nm1[3] && nm1[4]) {
          h_seed_eletrack_nstlayers_vs_pt->Fill(pt, nstlayers);
          h_seed_eletrack_nstlayers_vs_dxy->Fill(fabs(dxybs), nstlayers);
        }
        if (nm1[1] && nm1[2] && nm1[3]) {
          h_seed_mutrack_minr_vs_pt->Fill(pt, min_r);
          h_seed_mutrack_minr_vs_dxy->Fill(fabs(dxybs), min_r);
        }

        if (use_ele) {
          for (int i = 0; i < 7; ++i) {
            h_seed_eletrack_pars[i]->Fill(pars[i]);
            h_seed_eletrack_errs[i]->Fill(errs[i]);
          }

          h_seed_eletrack_p->Fill(p);
          if (abs(etk->eta())<1.4){
            h_seed_eletrack_pt_barrel->Fill(pt);
          }
          else{
            h_seed_eletrack_pt_endcap->Fill(pt);
          }
          h_seed_eletrack_sigmadxybs->Fill(fabs(sigmadxybs));
          h_seed_eletrack_sigmadxypv->Fill(fabs(sigmadxypv));
          // h_seed_eletrack_pt_dxybs->Fill(pt, fabs(dxybs));
          // h_seed_eletrack_pt_errdxybs->Fill(pt, etk->dxyError());
          h_seed_eletrack_nhits->Fill(nhits);
          h_seed_eletrack_npxhits->Fill(npxhits);
          h_seed_eletrack_nsthits->Fill(nsthits);
          h_seed_eletrack_npxlayers->Fill(npxlayers);
          h_seed_eletrack_nstlayers->Fill(nstlayers);
        }
      }
    }
  }

  if (verbose) {
    printf("n_all_tracks: %5lu   n_seed_tracks: %5lu\n", all_tracks->size(), seed_tracks->size());
    printf("n_all_muon_tracks: %5lu   n_muon_seed_tracks: %5lu\n", all_muon_tracks->size(), muon_seed_tracks->size());
    printf("n_all_electron_tracks: %5lu   n_electron_seed_tracks: %5lu\n", all_electron_tracks->size(), electron_seed_tracks->size());

  }
  if (histos) {
    h_n_all_tracks->Fill(all_tracks->size());
    h_n_seed_tracks->Fill(seed_tracks->size());
    h_n_all_mutracks->Fill(all_muon_tracks->size());
    h_n_all_eletracks->Fill(all_electron_tracks->size());
    h_n_seed_eletracks->Fill(electron_seed_tracks->size());
    h_n_seed_mutracks->Fill(muon_seed_tracks->size());

    
  }

  const bool pass_min_n_seed_tracks = int(seed_tracks->size()) >= min_n_seed_tracks;

  event.put(std::move(all_tracks), "all");
  event.put(std::move(seed_tracks), "seed");
  event.put(std::move(seed_tracks_copy), "seed");
  event.put(std::move(quality_tracks), "quality");
  event.put(std::move(quality_tracks_copy), "quality");

  if (use_separated_leptons) {
    event.put(std::move(all_electron_tracks), "allele");
    event.put(std::move(all_muon_tracks), "allmu");
    event.put(std::move(electron_seed_tracks), "eleseed");
    event.put(std::move(muon_seed_tracks), "museed");
  }

  return pass_min_n_seed_tracks;
}

bool MFVVertexTracks::match_track_jet(const reco::Track& tk, const pat::Jet& jet){
  //if (reco::deltaR2(tk, jet)>0.16) return false;
  if (verbose){
    std::cout << "jet track matching..." << std::endl;
    std::cout << "  target track pt " << tk.pt() << " eta " << tk.eta() << " phi " << tk.phi() << std::endl;
  }
  double match_thres = 1.3;
  for (size_t idau = 0, idaue = jet.numberOfDaughters(); idau < idaue; ++idau) {
    const reco::Candidate* dau = jet.daughter(idau);
    if (dau->charge() == 0)
      continue;
    const reco::Track* jtk = 0;
    const reco::PFCandidate* pf = dynamic_cast<const reco::PFCandidate*>(dau);
    if (pf) {
      const reco::TrackRef& r = pf->trackRef();
      if (r.isNonnull())
        jtk = &*r;
    }
    else {
      const pat::PackedCandidate* pk = dynamic_cast<const pat::PackedCandidate*>(dau);
      if (pk && pk->charge() && pk->hasTrackDetails())
        jtk = &pk->pseudoTrack();
    }
    if (jtk){
      double a = fabs(tk.pt()-jtk->pt())+1;
      double b = fabs(tk.eta()-jtk->eta())+1;
      double c = fabs(tk.phi()-jtk->phi())+1;
      if (verbose)
        std::cout << "  jet track pt " << jtk->pt() << " eta " << jtk->eta() << " phi " << jtk->phi() << " match abc " << a*b*c << std::endl;
      if (a*b*c < match_thres){
        return true;
      }
    }
  }
  return false;
}

DEFINE_FWK_MODULE(MFVVertexTracks);
