#include "TH2.h"
#include "TTree.h"
#include "CLHEP/Random/RandBinomial.h"
#include "CLHEP/Random/RandomEngine.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
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
#include "JMTucker/MFVNeutralinoFormats/interface/MCInteractions.h"

struct eventInfo
{
  std::vector <double> gen_vtx_x;
  std::vector <double> gen_vtx_y;
  std::vector <double> gen_vtx_z;
  std::vector <double> tk_p;
  std::vector <double> tk_pt;
  std::vector <double> tk_eta;
  std::vector <double> tk_phi;
  std::vector <double> tk_dxybs;
  std::vector <double> tk_dxybserr;
  std::vector <double> tk_sigmadxybs;
  std::vector <double> tk_nhits;
  std::vector <double> tk_npxhits;
  std::vector <double> tk_nsthits;
  std::vector <double> tk_npxlayers;
  std::vector <double> tk_nstlayers;
  std::vector <double> tk_min_r;
  std::vector <double> tk_ip3D_genvtx_0;
  std::vector <double> tk_ip3D_genvtx_1;
  std::vector <double> tk_ip2D_genvtx_0;
  std::vector <double> tk_ip2D_genvtx_1;
  std::vector <double> tk_ip3D_err_genvtx_0;
  std::vector <double> tk_ip3D_err_genvtx_1;
  std::vector <double> tk_ip2D_err_genvtx_0;
  std::vector <double> tk_ip2D_err_genvtx_1;
  std::vector <double> tk_is_seed;
  std::vector <int> tk_whichLLP;

};

class MFVTrackTree : public edm::EDAnalyzer {
  public:
    explicit MFVTrackTree(const edm::ParameterSet&);
    void analyze(const edm::Event&, const edm::EventSetup&);

  private:
    void visitdaughters(const reco::Candidate* dau, int whichLLP, int rank=0){
      if(verbose)
        std::cout << "  rank "<<rank<<"  id " << dau->pdgId() << " status " << dau->status() << " isjet " << dau->isJet() << " pt " << dau->pt() << " eta " << dau->eta() << " phi " << dau->phi() << std::endl;
      if (dau->numberOfDaughters()){
        if(verbose)
          std::cout << "daughter of " << dau->pdgId() << std::endl;
        for (size_t i=0; i<dau->numberOfDaughters(); ++i){
          visitdaughters(dau->daughter(i), whichLLP, rank+1);
        }
      }
      else{
        if (verbose)
          std::cout << "final particle" << std::endl;
        if ( (dau->status()<=3) || ( (dau->status()>=21) && (dau->status()<=29) ) || ( (dau->status()>=11) && (dau->status()<=19) ) )
          LLP_daus[whichLLP].insert(dau);
      }
    }


    virtual void beginJob() override;
    virtual void endJob() override;
    void initEventStructure();

    TTree *eventTree;
    eventInfo *evInfo;

    const edm::EDGetTokenT<std::vector<double>> genvtx_token;
    const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
    const bool use_primary_vertices;
    const edm::EDGetTokenT<reco::VertexCollection> primary_vertices_token;
    const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
    const edm::EDGetTokenT<mfv::MCInteraction> mci_token;
    const bool no_track_cuts;
    const double min_track_pt;
    const double min_track_dxy;
    const double min_track_sigmadxy;
    const double min_track_rescaled_sigmadxy;
    const double min_track_sigmadxypv;
    const int min_track_hit_r;
    const int min_track_nhits;
    const int min_track_npxhits;
    const int min_track_npxlayers;
    const int min_track_nstlayers;
    const double max_track_dxyerr;
    const double max_track_dxyipverr;
    const double max_track_d3dipverr;
    std::set<const reco::Candidate*> LLP_daus[2];

    jmt::TrackRescaler track_rescaler;
    bool verbose;

};

MFVTrackTree::MFVTrackTree(const edm::ParameterSet& cfg)
  : genvtx_token(consumes<std::vector<double>>(cfg.getParameter<edm::InputTag>("genvtx_src"))),
    beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot_src"))),
    use_primary_vertices(cfg.getParameter<edm::InputTag>("primary_vertices_src").label() != ""),
    primary_vertices_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("primary_vertices_src"))),
    tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("tracks_src"))),
    mci_token(consumes<mfv::MCInteraction>(cfg.getParameter<edm::InputTag>("mci_src"))),
    no_track_cuts(cfg.getParameter<bool>("no_track_cuts")),
    min_track_pt(cfg.getParameter<double>("min_track_pt")),
    min_track_dxy(cfg.getParameter<double>("min_track_dxy")),
    min_track_sigmadxy(cfg.getParameter<double>("min_track_sigmadxy")),
    min_track_rescaled_sigmadxy(cfg.getParameter<double>("min_track_rescaled_sigmadxy")),
    min_track_sigmadxypv(cfg.getParameter<double>("min_track_sigmadxypv")),
    min_track_hit_r(cfg.getParameter<int>("min_track_hit_r")),
    min_track_nhits(cfg.getParameter<int>("min_track_nhits")),
    min_track_npxhits(cfg.getParameter<int>("min_track_npxhits")),
    min_track_npxlayers(cfg.getParameter<int>("min_track_npxlayers")),
    min_track_nstlayers(cfg.getParameter<int>("min_track_nstlayers")),
    max_track_dxyerr(cfg.getParameter<double>("max_track_dxyerr")),
    max_track_dxyipverr(cfg.getParameter<double>("max_track_dxyipverr")),
    max_track_d3dipverr(cfg.getParameter<double>("max_track_d3dipverr")),
    verbose(cfg.getParameter<bool>("verbose"))
{
  evInfo = new eventInfo;
}

void MFVTrackTree::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  if (verbose)
    std::cout << "MFVTrackTree:: event id: " << event.id().event() << std::endl;
  
  initEventStructure();
  LLP_daus[0].clear();
  LLP_daus[1].clear();

  const int track_rescaler_which = jmt::TrackRescaler::w_JetHT; // JMTBAD which rescaling if ever a different one
  track_rescaler.setup(!event.isRealData() && track_rescaler_which != -1 && min_track_rescaled_sigmadxy > 0,
                       jmt::AnalysisEras::pick(event, this),
                       track_rescaler_which);

  edm::Handle<std::vector<double>> gen_vertex;
  event.getByToken(genvtx_token, gen_vertex);
  std::vector<reco::Vertex> genv;
  for (size_t i=0; i<2; ++i){
    const double x = (*gen_vertex)[i*3+0];
    const double y = (*gen_vertex)[i*3+1];
    const double z = (*gen_vertex)[i*3+2];
    math::Error<3>::type e;
    math::XYZPoint p(x, y, z);
    reco::Vertex vg(p,e);
    genv.push_back(vg);
    evInfo->gen_vtx_x.push_back(x);
    evInfo->gen_vtx_y.push_back(y);
    evInfo->gen_vtx_z.push_back(z);
  }

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

  edm::Handle<mfv::MCInteraction> mci;
  event.getByToken(mci_token, mci);
  if (mci->valid()){
    assert(mci->primaries().size() == 2);
    for (int i=0; i<2; ++i){
      auto secondaries = mci->secondaries(i);
      if(verbose)
        std::cout << "LLP" << i << std::endl;
      for (unsigned int i_secondary = 0; i_secondary < secondaries.size(); ++i_secondary){
        const reco::GenParticleRef& s = secondaries[i_secondary];
        if (s->pdgId()!=1000022)
          LLP_daus[i].insert(&*s);
        if (verbose)
          std::cout << "LLP secondary " << s->pdgId() << " status " << s->status() << " isJet " << s->isJet() << " pt " << s->pt() << " eta " << s->eta() << " phi " << s->phi() << std::endl;
        //if(abs(s->pdgId()) != 5 && abs(s->pdgId()) != 24){
        if (1){
          for(unsigned int i_dau = 0; i_dau < s->numberOfDaughters(); ++i_dau){
            auto dau = s->daughter(i_dau);
            visitdaughters(dau,i);
          }
        }
      }
    }
  }
  if(1){
    std::cout << "LLP0 final daughter:" << LLP_daus[0].size()<<std::endl;
    for (const auto&dau:LLP_daus[0]){
      std::cout << " pdgid " << dau->pdgId() << " pt " << dau->pt() << " eta " << dau->eta() << " phi " << dau->phi() << std::endl;
    }
    std::cout << "LLP final daughter:" << LLP_daus[1].size()<<std::endl;
    for (const auto&dau:LLP_daus[1]){
      std::cout << " pdgid " << dau->pdgId() << " pt " << dau->pt() << " eta " << dau->eta() << " phi " << dau->phi() << std::endl;
    }
  }

  edm::Handle<reco::TrackCollection> tracks;
  event.getByToken(tracks_token, tracks);
  for (size_t i = 0, ie = tracks->size(); i < ie; ++i){
    const reco::TrackRef& tk = reco::TrackRef(tracks, i);
    const auto rs = track_rescaler.scale(*tk);

    const double p = tk->p();
    const double pt = tk->pt();
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
    int min_r = 2000000000;
    for (int i = 1; i <= 4; ++i)
      if (tk->hitPattern().hasValidHitInPixelLayer(PixelSubdetector::PixelBarrel,i)) {
        min_r = i;
        break;
      }

    reco::TransientTrack ttk = tt_builder->build(tk);
    auto dxy_gen0 = IPTools::absoluteTransverseImpactParameter(ttk, genv[0]);
    auto d3d_gen0 = IPTools::absoluteImpactParameter3D(ttk, genv[0]);
    auto dxy_gen1 = IPTools::absoluteTransverseImpactParameter(ttk, genv[1]);
    auto d3d_gen1 = IPTools::absoluteImpactParameter3D(ttk, genv[1]);

    bool use = no_track_cuts || [&]() {

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
        (min_track_hit_r == 999 || min_r <= min_track_hit_r);

      if (!use_cheap) return false;

      if (primary_vertex && (max_track_dxyipverr > 0 || max_track_d3dipverr > 0)) {
        //reco::TransientTrack ttk = tt_builder->build(tk);
        if (max_track_dxyipverr > 0) {
          auto dxy_ipv = IPTools::absoluteTransverseImpactParameter(ttk, *primary_vertex); if (!dxy_ipv.first || dxy_ipv.second.error() >= max_track_dxyipverr) return false;
        }
        if (max_track_d3dipverr > 0) {
          auto d3d_ipv = IPTools::absoluteImpactParameter3D        (ttk, *primary_vertex); if (!d3d_ipv.first || d3d_ipv.second.error() >= max_track_d3dipverr) return false;
        }
      }

      return true;
    }();

    if (use) {
      evInfo->tk_is_seed.push_back(1);
      double mindr = 999;
      for (int illp=0; illp<2; ++illp){
        for(const auto& dau:LLP_daus[illp]){
          double dr2 = reco::deltaR2(tk->eta(), tk->phi(), dau->eta(), dau->phi());
          if (dr2<mindr){
            mindr = dr2;
            
          }
        }
      }
      std::cout << "seed tracks matched with dr2 " << mindr <<" eta " << tk->eta() << " phi " << tk->phi()<< std::endl;
    }
    else
      evInfo->tk_is_seed.push_back(0);

    double match_thres = 0.16;
    bool match[2] = {false, false};
    for (int illp=0; illp<2; ++illp){
      for(const auto& dau:LLP_daus[illp]){
        if ((dau->pdgId()!=21)&&(dau->pdgId()>=10))
          continue;
        double dr2 = reco::deltaR2(tk->eta(), tk->phi(), dau->eta(), dau->phi());
        if (dr2<match_thres){
          match[illp] = true;
          break;
        }
      }
    }
    if (match[0]&match[1]){
      evInfo->tk_whichLLP.push_back(2);
    }
    else if (match[0]){
      evInfo->tk_whichLLP.push_back(0);
    }
    else if (match[1]){
      evInfo->tk_whichLLP.push_back(1);
    }
    else{
      evInfo->tk_whichLLP.push_back(-1);
      if (use)
        std::cout << "  track not matched " << std::endl;
    }

    evInfo->tk_p.push_back(p);
    evInfo->tk_pt.push_back(pt);
    evInfo->tk_eta.push_back(tk->eta());
    evInfo->tk_phi.push_back(tk->phi());
    evInfo->tk_dxybs.push_back(dxybs);
    evInfo->tk_dxybserr.push_back(rescaled_dxyerr);
    evInfo->tk_sigmadxybs.push_back(rescaled_sigmadxybs);
    evInfo->tk_nhits.push_back(nhits);
    evInfo->tk_npxhits.push_back(npxhits);
    evInfo->tk_nsthits.push_back(nsthits);
    evInfo->tk_npxlayers.push_back(npxlayers);
    evInfo->tk_nstlayers.push_back(nstlayers);
    evInfo->tk_min_r.push_back(min_r);
    if (d3d_gen0.first){
      evInfo->tk_ip3D_genvtx_0.push_back(d3d_gen0.second.value());
      evInfo->tk_ip3D_err_genvtx_0.push_back(d3d_gen0.second.error());
    }
    else {
      evInfo->tk_ip3D_genvtx_0.push_back(-1);
      evInfo->tk_ip3D_err_genvtx_0.push_back(-1);
    }
    if (d3d_gen1.first){
      evInfo->tk_ip3D_genvtx_1.push_back(d3d_gen1.second.value());
      evInfo->tk_ip3D_err_genvtx_1.push_back(d3d_gen1.second.error());
    }
    else {
      evInfo->tk_ip3D_genvtx_1.push_back(-1);
      evInfo->tk_ip3D_err_genvtx_1.push_back(-1);
    }
    if (dxy_gen0.first){
      evInfo->tk_ip2D_genvtx_0.push_back(dxy_gen0.second.value());
      evInfo->tk_ip2D_err_genvtx_0.push_back(dxy_gen0.second.error());
    }
    else {
      evInfo->tk_ip2D_genvtx_0.push_back(-1);
      evInfo->tk_ip2D_err_genvtx_0.push_back(-1);
    }
    if (dxy_gen1.first){
      evInfo->tk_ip2D_genvtx_1.push_back(dxy_gen1.second.value());
      evInfo->tk_ip2D_err_genvtx_1.push_back(dxy_gen1.second.error());
    }
    else {
      evInfo->tk_ip2D_genvtx_1.push_back(-1);
      evInfo->tk_ip2D_err_genvtx_1.push_back(-1);
    }
  }
  eventTree->Fill(); 
}

void MFVTrackTree::beginJob()
{
  edm::Service<TFileService> fs;
  if(!fs) throw edm::Exception(edm::errors::Configuration, "TFileService is not registered in cfg file");
  eventTree = fs->make<TTree>("track_tree", "track_tree");
  eventTree->Branch("gen_vtx_x",        &evInfo->gen_vtx_x);
  eventTree->Branch("gen_vtx_y",        &evInfo->gen_vtx_y);
  eventTree->Branch("gen_vtx_z",        &evInfo->gen_vtx_z);
  eventTree->Branch("tk_p",             &evInfo->tk_p);
  eventTree->Branch("tk_pt",            &evInfo->tk_pt);
  eventTree->Branch("tk_eta",           &evInfo->tk_eta);
  eventTree->Branch("tk_phi",           &evInfo->tk_phi);
  eventTree->Branch("tk_dxybs",         &evInfo->tk_dxybs);
  eventTree->Branch("tk_dxybserr",      &evInfo->tk_dxybserr);
  eventTree->Branch("tk_sigmadxybs",    &evInfo->tk_sigmadxybs);
  eventTree->Branch("tk_nhits",         &evInfo->tk_nhits);
  eventTree->Branch("tk_npxhits",       &evInfo->tk_npxhits);
  eventTree->Branch("tk_nsthits",       &evInfo->tk_nsthits);
  eventTree->Branch("tk_npxlayers",     &evInfo->tk_npxlayers);
  eventTree->Branch("tk_nstlayers",     &evInfo->tk_nstlayers);
  eventTree->Branch("tk_min_r",         &evInfo->tk_min_r);
  eventTree->Branch("tk_ip3D_genvtx_0", &evInfo->tk_ip3D_genvtx_0);
  eventTree->Branch("tk_ip3D_genvtx_1", &evInfo->tk_ip3D_genvtx_1);
  eventTree->Branch("tk_ip2D_genvtx_0", &evInfo->tk_ip2D_genvtx_0);
  eventTree->Branch("tk_ip2D_genvtx_1", &evInfo->tk_ip2D_genvtx_1);
  eventTree->Branch("tk_ip3D_err_genvtx_0", &evInfo->tk_ip3D_err_genvtx_0);
  eventTree->Branch("tk_ip3D_err_genvtx_1", &evInfo->tk_ip3D_err_genvtx_1);
  eventTree->Branch("tk_ip2D_err_genvtx_0", &evInfo->tk_ip2D_err_genvtx_0);
  eventTree->Branch("tk_ip2D_err_genvtx_1", &evInfo->tk_ip2D_err_genvtx_1);
  eventTree->Branch("tk_is_seed",       &evInfo->tk_is_seed);
  eventTree->Branch("tk_whichLLP",      &evInfo->tk_whichLLP);
  
}

void MFVTrackTree::endJob()
{}

void MFVTrackTree::initEventStructure()
{
  evInfo->gen_vtx_x.clear();
  evInfo->gen_vtx_y.clear();
  evInfo->gen_vtx_z.clear();
  evInfo->tk_p.clear();
  evInfo->tk_pt.clear();
  evInfo->tk_eta.clear();
  evInfo->tk_phi.clear();
  evInfo->tk_dxybs.clear();
  evInfo->tk_dxybserr.clear();
  evInfo->tk_sigmadxybs.clear();
  evInfo->tk_nhits.clear();
  evInfo->tk_npxhits.clear();
  evInfo->tk_nsthits.clear();
  evInfo->tk_npxlayers.clear();
  evInfo->tk_nstlayers.clear();
  evInfo->tk_min_r.clear();
  evInfo->tk_ip3D_genvtx_0.clear();
  evInfo->tk_ip3D_genvtx_1.clear();
  evInfo->tk_ip2D_genvtx_0.clear();
  evInfo->tk_ip2D_genvtx_1.clear();
  evInfo->tk_ip3D_err_genvtx_0.clear();
  evInfo->tk_ip3D_err_genvtx_1.clear();
  evInfo->tk_ip2D_err_genvtx_0.clear();
  evInfo->tk_ip2D_err_genvtx_1.clear();
  evInfo->tk_is_seed.clear();
  evInfo->tk_whichLLP.clear();
}
DEFINE_FWK_MODULE(MFVTrackTree);
