#ifndef JMTucker_Tools_NtupleFiller_h
#define JMTucker_Tools_NtupleFiller_h

#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "JMTucker/Tools/interface/Ntuple.h"

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
    const reco::VertexCollection& pvs(const edm::Event& e) { e.getByToken(token_, pvs_); return *pvs_; }
    const pat::PackedCandidateCollection& cands(const edm::Event& e) { e.getByToken(cands_token_, cands_); return *cands_; }
    void operator()(const edm::Event&, const reco::BeamSpot* =0);
    const reco::Vertex* pv() const { return pv_; }
    int ipv() const { return ipv_; }
  };

  void NtupleAdd(TracksSubNtuple&, const reco::Track&);

  class TracksSubNtupleFiller {
    TracksSubNtuple& nt_;
    const edm::InputTag tag_;
    const edm::EDGetTokenT<reco::TrackCollection> token_;
    bool (*cut_)(const reco::Track&);
    edm::Handle<reco::TrackCollection> tracks_;
  public:
    TracksSubNtupleFiller(TracksSubNtuple& nt, const edm::ParameterSet& cfg, edm::ConsumesCollector&& cc, bool (*cut)(const reco::Track&) = 0)
      : nt_(nt),
        tag_(cfg.getParameter<edm::InputTag>("tracks_src")),
        token_(cc.consumes<reco::TrackCollection>(tag_)),
        cut_(cut)
    {}
    bool cut(const reco::Track& t) const { return cut_ == 0 ? false : cut_(t); }
    const reco::TrackCollection& tracks(const edm::Event& e) { e.getByToken(token_, tracks_); return *tracks_; }
    void operator()(const edm::Event& e) { for (const auto& tk : tracks(e)) if (!cut(tk)) NtupleAdd(nt_, tk); }
  };

  void NtupleAdd(JetsSubNtuple&, const pat::Jet&);

  class JetsSubNtupleFiller {
    JetsSubNtuple& nt_;
    const edm::InputTag tag_;
    const edm::EDGetTokenT<pat::JetCollection> token_;
    bool (*cut_)(const pat::Jet&);
    edm::Handle<pat::JetCollection> jets_;
  public:
    JetsSubNtupleFiller(JetsSubNtuple& nt, const edm::ParameterSet& cfg, edm::ConsumesCollector&& cc, bool (*cut)(const pat::Jet&) = 0)
      : nt_(nt),
        tag_(cfg.getParameter<edm::InputTag>("jets_src")),
        token_(cc.consumes<pat::JetCollection>(tag_)),
        cut_(cut)
    {}
    bool cut(const pat::Jet& j) const { return cut_ == 0 ? false : cut_(j); }
    const pat::JetCollection& jets(const edm::Event& e) { e.getByToken(token_, jets_); return *jets_; }
    void operator()(const edm::Event& e) { for (const auto& j : jets(e)) if (!cut(j)) NtupleAdd(nt_, j); }
  };
};

#endif
