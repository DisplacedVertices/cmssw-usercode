#ifndef JMTucker_Tools_NtupleFiller_h
#define JMTucker_Tools_NtupleFiller_h

#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/HitPattern.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "JMTucker/Tools/interface/Ntuple.h"
#include "JMTucker/Tools/interface/TrackRefGetter.h"


namespace jmt {
  class BaseSubNtupleFiller {
    BaseSubNtuple& nt_;
    const edm::EDGetTokenT<double> weight_token_;
    const edm::EDGetTokenT<std::vector<PileupSummaryInfo>> pileup_token_;
    const edm::EDGetTokenT<reco::VertexCollection> pvs_token_;
    const edm::EDGetTokenT<double> rho_token_;
    
   
  public:
    BaseSubNtupleFiller(BaseSubNtuple& nt, const edm::ParameterSet& cfg, edm::ConsumesCollector&& cc)
      : nt_(nt),
        weight_token_(cc.consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
        pileup_token_(cc.consumes<std::vector<PileupSummaryInfo>>(cfg.getParameter<edm::InputTag>("pileup_info_src"))),
        pvs_token_(cc.consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("primary_vertices_src"))),
        rho_token_(cc.consumes<double>(cfg.getParameter<edm::InputTag>("rho_src")))
	
    {}
    void operator()(const edm::Event&);
  };

  class BeamspotSubNtupleFiller {
    BeamspotSubNtuple& nt_;
    const edm::InputTag tag_;
    const edm::EDGetTokenT<reco::BeamSpot> token_;
    edm::Handle<reco::BeamSpot> bs_;
  public:
    BeamspotSubNtupleFiller(BeamspotSubNtuple& nt, const edm::ParameterSet& cfg, edm::ConsumesCollector&& cc)
      : nt_(nt),
        tag_(cfg.getParameter<edm::InputTag>("beamspot_src")),
        token_(cc.consumes<reco::BeamSpot>(tag_))
    {}
    void operator()(const edm::Event&);
    const reco::BeamSpot& bs() const { return *bs_; }
  };

  class PrimaryVerticesSubNtupleFiller {
    PrimaryVerticesSubNtuple& nt_;
    const bool miniaod_;
    const edm::InputTag tag_;
    const edm::EDGetTokenT<reco::VertexCollection> token_;
    const edm::EDGetTokenT<edm::ValueMap<float>> scores_token_;
    const edm::EDGetTokenT<pat::PackedCandidateCollection> cands_token_;
    const bool filter_;
    const bool first_only_;
    edm::Handle<reco::VertexCollection> pvs_;
    edm::Handle<edm::ValueMap<float>> scores_;
    edm::Handle<pat::PackedCandidateCollection> cands_;
    std::vector<int> i2nti_;
    const reco::Vertex* pv_;
    int ipv_;
  public:
    PrimaryVerticesSubNtupleFiller(PrimaryVerticesSubNtuple& nt, const edm::ParameterSet& cfg, edm::ConsumesCollector&& cc, bool filter, bool first_only)
      : nt_(nt),
        miniaod_(cfg.getParameter<bool>("input_is_miniaod")),
        tag_(cfg.getParameter<edm::InputTag>("primary_vertices_src")),
        token_(cc.consumes<reco::VertexCollection>(tag_)),
        scores_token_(cc.consumes<edm::ValueMap<float>>(tag_)),
        cands_token_(cc.consumes<pat::PackedCandidateCollection>(cfg.getParameter<edm::InputTag>("packed_candidates_src"))),
        filter_(filter),
        first_only_(first_only),
        pv_(nullptr),
        ipv_(-1)
    {}
    bool cut(const reco::Vertex& pv) const { return pv.isFake() || pv.ndof() < 4 || fabs(pv.z()) > 24 || fabs(pv.position().Rho()) > 2; }
    const edm::Handle<reco::VertexCollection>& hpvs(const edm::Event& e) { e.getByToken(token_, pvs_); return pvs_; }
    const reco::VertexCollection& pvs(const edm::Event& e) { return *hpvs(e); }
    const pat::PackedCandidateCollection& cands(const edm::Event& e) { e.getByToken(cands_token_, cands_); return *cands_; }
    void operator()(const edm::Event&, const reco::BeamSpot* =0); // JMTBAD if we keep the beamspot subtraction option, add param in ctor
    int i2nti(size_t i) const { return i2nti_[i]; }
    const reco::Vertex* pv() const { return pv_; }
    int ipv() const { return ipv_; }
  };

  void NtupleAdd(JetsSubNtuple&, const pat::Jet&);
  typedef bool (*jets_cut_fcn)(const pat::Jet&);

  class JetsSubNtupleFiller {
    JetsSubNtuple& nt_;
    const edm::InputTag tag_;
    const edm::EDGetTokenT<pat::JetCollection> token_;
    jets_cut_fcn cut_;
    edm::Handle<pat::JetCollection> jets_;
    std::vector<int> i2nti_;
  public:
    JetsSubNtupleFiller(JetsSubNtuple& nt, const edm::ParameterSet& cfg, edm::ConsumesCollector&& cc, jets_cut_fcn cut=0)
      : nt_(nt),
        tag_(cfg.getParameter<edm::InputTag>("jets_src")),
        token_(cc.consumes<pat::JetCollection>(tag_)),
        cut_(cut)
    {}
    bool cut(const pat::Jet& j) const { return cut_ == 0 ? false : cut_(j); }
    const edm::Handle<pat::JetCollection>& hjets(const edm::Event& e) { e.getByToken(token_, jets_); return jets_; }
    const pat::JetCollection& jets(const edm::Event& e) { return *hjets(e); }
    void operator()(const edm::Event&);
    int i2nti(size_t i) const { return i2nti_[i]; }
  };

  class PFSubNtupleFiller {
    PFSubNtuple& nt_;
    const edm::InputTag tag_;
    const edm::EDGetTokenT<pat::METCollection> token_;
    edm::Handle<pat::METCollection> mets_;
  public:
    PFSubNtupleFiller(PFSubNtuple& nt, const edm::ParameterSet& cfg, edm::ConsumesCollector&& cc)
      : nt_(nt),
        tag_(cfg.getParameter<edm::InputTag>("mets_src")),
        token_(cc.consumes<pat::METCollection>(tag_))
    {}
    void operator()(const edm::Event&);
    const pat::METCollection& mets() const { return *mets_; }
  };
  
  //electrons
  void NtupleAdd(EleTracksSubNtuple&, const reco::Track&);
  typedef bool (*tracks_cut_fcn)(const reco::Track&);

  class EleTracksSubNtupleFiller {
    EleTracksSubNtuple& nt_;
    const edm::InputTag tag_;
    const edm::EDGetTokenT<reco::TrackCollection> token_;
    int cut_level_ ;
    tracks_cut_fcn cut_;
    edm::Handle<reco::TrackCollection> eletracks_;

  public:
    EleTracksSubNtupleFiller(EleTracksSubNtuple& nt, const edm::ParameterSet& cfg, edm::ConsumesCollector&& cc, int cut_level = -1, tracks_cut_fcn cut=0)
      : nt_(nt),
        tag_(cfg.getParameter<edm::InputTag>("electron_tracks_src")),
        token_(cc.consumes<reco::TrackCollection>(tag_)),
        cut_level_(cut_level),
        cut_(cut)
    {}
    bool cut(const reco::Track&, const edm::Event&, BeamspotSubNtupleFiller* =0) const;
    const edm::Handle<reco::TrackCollection>& ehtracks(const edm::Event& e) { e.getByToken(token_, eletracks_); return eletracks_; }
    const reco::TrackCollection& eletracks(const edm::Event& e) { return *ehtracks(e); }
    void operator()(const edm::Event&, BeamspotSubNtupleFiller* =0);
  };

  //muons 
  void NtupleAdd(MuTracksSubNtuple&, const reco::Track&);
  typedef bool (*tracks_cut_fcn)(const reco::Track&);

  class MuTracksSubNtupleFiller {
    MuTracksSubNtuple& nt_;
    const edm::InputTag tag_;
    const edm::EDGetTokenT<reco::TrackCollection> token_;
    int cut_level_ ;
    tracks_cut_fcn cut_;
    edm::Handle<reco::TrackCollection> mutracks_;

  public:
    MuTracksSubNtupleFiller(MuTracksSubNtuple& nt, const edm::ParameterSet& cfg, edm::ConsumesCollector&& cc, int cut_level = -1, tracks_cut_fcn cut=0)
      : nt_(nt),
        tag_(cfg.getParameter<edm::InputTag>("muon_tracks_src")),
        token_(cc.consumes<reco::TrackCollection>(tag_)),
        cut_level_(cut_level),
        cut_(cut)

    {}
    bool cut(const reco::Track&, const edm::Event&, BeamspotSubNtupleFiller* =0) const;
    const edm::Handle<reco::TrackCollection>& mhtracks(const edm::Event& e) { e.getByToken(token_, mutracks_); return mutracks_; }
    const reco::TrackCollection& mutracks(const edm::Event& e) { return *mhtracks(e); }
    void operator()(const edm::Event&, BeamspotSubNtupleFiller* =0);
  };


  void NtupleAdd(TracksSubNtuple&, const reco::Track&, int which_jet=-1, int which_pv=-1, int which_sv=-1, unsigned misc=0);
  typedef bool (*tracks_cut_fcn)(const reco::Track&);

  class TracksSubNtupleFiller {
    TracksSubNtuple& nt_;
    const edm::InputTag tag_;
    const edm::EDGetTokenT<reco::TrackCollection> token_;
    int cut_level_ ;
    tracks_cut_fcn cut_;
    edm::Handle<reco::TrackCollection> tracks_;
    jmt::TrackRefGetter trg_;


    
  public:
    TracksSubNtupleFiller(TracksSubNtuple& nt, const edm::ParameterSet& cfg, edm::ConsumesCollector&& cc, int cut_level = -1, tracks_cut_fcn cut=0)
      : nt_(nt),
        tag_(cfg.getParameter<edm::InputTag>("tracks_src")),
        token_(cc.consumes<reco::TrackCollection>(tag_)),
        cut_level_(cut_level),
        cut_(cut),
        trg_("TracksSubNtupleFiller", cfg.getParameter<edm::ParameterSet>("track_ref_getter"), std::move(cc))

    {}
    bool cut(const reco::Track&, const edm::Event&, BeamspotSubNtupleFiller* =0) const;
    const edm::Handle<reco::TrackCollection>& htracks(const edm::Event& e) { e.getByToken(token_, tracks_); return tracks_; }
    const reco::TrackCollection& tracks(const edm::Event& e) { return *htracks(e); }
    int which_jet(const edm::Event&, JetsSubNtupleFiller*, reco::TrackRef&);
    int which_pv(const edm::Event&, PrimaryVerticesSubNtupleFiller*, reco::TrackRef&);
    void operator()(const edm::Event&, JetsSubNtupleFiller* =0, PrimaryVerticesSubNtupleFiller* =0, BeamspotSubNtupleFiller* =0);
  };

  //////////////////////////////////////////////////////////////////////

  class INtupleFiller {
  public:
    virtual ~INtupleFiller() {}
    INtupleFiller(INtuple& nt)
      : nt_(nt)
    {
      edm::Service<TFileService> fs;
      t_ = fs->make<TTree>("t", "");
      nt_.write_to_tree(t_);
    }

    void fill(const edm::Event& e, bool final=false) {
      nt_.clear();
      (*this)(e);
      if (final) finalize();
    }

    void finalize() {
      t_->Fill();
    }

    virtual void operator()(const edm::Event&) = 0;

  private:
    INtuple& nt_;
    TTree* t_;
  };

  class TrackingAndJetsNtupleFillerParams { // for a bit more verbosity at caller instead of many anonymous params in Filler ctor
    bool pvs_subtract_bs_;
    bool pvs_filter_;
    bool pvs_first_only_;
    jets_cut_fcn jets_cut_;
    bool fill_tracks_;
    int tracks_cut_level_;
    tracks_cut_fcn tracks_cut_;
    bool use_separated_leptons_;

  public:
    TrackingAndJetsNtupleFillerParams()
      : pvs_subtract_bs_(false),
        pvs_filter_(true),
        pvs_first_only_(false),
        jets_cut_(nullptr),
        fill_tracks_(true),
        tracks_cut_level_(-1),
        tracks_cut_(nullptr),
        use_separated_leptons_(false)
    {}

    bool pvs_subtract_bs() const { return pvs_subtract_bs_; }
    bool pvs_filter() const { return pvs_filter_; }
    bool pvs_first_only() const { return pvs_first_only_; }
    jets_cut_fcn jets_cut() const { return jets_cut_; }
    bool fill_tracks() const { return fill_tracks_; }
    int tracks_cut_level() const { return tracks_cut_level_; }
    tracks_cut_fcn tracks_cut() const { return tracks_cut_; }
    bool use_separated_leptons() const { return use_separated_leptons_; }

    TrackingAndJetsNtupleFillerParams pvs_subtract_bs           (bool x) { TrackingAndJetsNtupleFillerParams y(*this); y.pvs_subtract_bs_  = x; return y; }
    TrackingAndJetsNtupleFillerParams pvs_filter                (bool x) { TrackingAndJetsNtupleFillerParams y(*this); y.pvs_filter_       = x; return y; }
    TrackingAndJetsNtupleFillerParams pvs_first_only            (bool x) { TrackingAndJetsNtupleFillerParams y(*this); y.pvs_first_only_   = x; return y; }
    TrackingAndJetsNtupleFillerParams jets_cut          (jets_cut_fcn x) { TrackingAndJetsNtupleFillerParams y(*this); y.jets_cut_         = x; return y; }
    TrackingAndJetsNtupleFillerParams fill_tracks               (bool x) { TrackingAndJetsNtupleFillerParams y(*this); y.fill_tracks_      = x; return y; }
    TrackingAndJetsNtupleFillerParams tracks_cut_level           (int x) { TrackingAndJetsNtupleFillerParams y(*this); y.tracks_cut_level_ = x; return y; }
    TrackingAndJetsNtupleFillerParams tracks_cut      (tracks_cut_fcn x) { TrackingAndJetsNtupleFillerParams y(*this); y.tracks_cut_       = x; return y; }
    TrackingAndJetsNtupleFillerParams use_separated_leptons     (bool x) { TrackingAndJetsNtupleFillerParams y(*this); y.use_separated_leptons_ = x; return y; }
  };
    
    // this is not great but I didn't want to spend time figuring out how to share a single ConsumesCollector instance
#define NF_CC_TrackingAndJets_p edm::ConsumesCollector&& cc0, edm::ConsumesCollector&& cc1, edm::ConsumesCollector&& cc2, edm::ConsumesCollector&& cc3, edm::ConsumesCollector&& cc4, edm::ConsumesCollector&& cc5, edm::ConsumesCollector&& cc6, edm::ConsumesCollector&& cc7
#define NF_CC_TrackingAndJets_v consumesCollector(),          consumesCollector(),          consumesCollector(),          consumesCollector(),          consumesCollector(),          consumesCollector(),          consumesCollector(),          consumesCollector()

  class TrackingAndJetsNtupleFiller : public INtupleFiller {
    TrackingAndJetsNtuple& nt_;
    TrackingAndJetsNtupleFillerParams p_;
    BaseSubNtupleFiller base_filler_;
    BeamspotSubNtupleFiller bs_filler_;
    PrimaryVerticesSubNtupleFiller pvs_filler_;
    JetsSubNtupleFiller jets_filler_;
    PFSubNtupleFiller pf_filler_;
    MuTracksSubNtupleFiller mutracks_filler_;
    EleTracksSubNtupleFiller eletracks_filler_;
    TracksSubNtupleFiller tracks_filler_;
  public:
    TrackingAndJetsNtupleFiller(TrackingAndJetsNtuple& nt, const edm::ParameterSet& cfg, NF_CC_TrackingAndJets_p, TrackingAndJetsNtupleFillerParams p)
      : INtupleFiller(nt),
        nt_(nt),
        p_(p),
        base_filler_(nt.base(), cfg, std::move(cc0)),
        bs_filler_(nt.bs(), cfg, std::move(cc1)),
        pvs_filler_(nt.pvs(), cfg, std::move(cc2), p.pvs_filter(), p.pvs_first_only()),
        jets_filler_(nt.jets(), cfg, std::move(cc3), p.jets_cut()),
        pf_filler_(nt.pf(), cfg, std::move(cc4)),
        mutracks_filler_(nt.mu_tracks(), cfg, std::move(cc5), p.tracks_cut_level(), p.tracks_cut()),
        eletracks_filler_(nt.ele_tracks(), cfg, std::move(cc6), p.tracks_cut_level(), p.tracks_cut()),
	      tracks_filler_(nt.tracks(), cfg, std::move(cc7), p.tracks_cut_level(), p.tracks_cut())
      {}
    
      BaseSubNtupleFiller base_filler() { return base_filler_; }
      BeamspotSubNtupleFiller bs_filler() { return bs_filler_; }
      PrimaryVerticesSubNtupleFiller pvs_filler() { return pvs_filler_; }
      JetsSubNtupleFiller jets_filler() { return jets_filler_; }
      PFSubNtupleFiller pf_filler() { return pf_filler_; }
      MuTracksSubNtupleFiller mutracks_filler() { return mutracks_filler_; }
      EleTracksSubNtupleFiller eletracks_filler() { return eletracks_filler_; }
      TracksSubNtupleFiller tracks_filler() { return tracks_filler_; }


      const reco::BeamSpot& bs() { return bs_filler_.bs(); }
      const reco::Vertex* pv() const { return pvs_filler_.pv(); }

      virtual void operator()(const edm::Event&);
    };
  }

#endif
