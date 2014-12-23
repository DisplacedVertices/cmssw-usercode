#include "TTree.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"

class MFVMovedTracksTreer : public edm::EDAnalyzer {
public:
  explicit MFVMovedTracksTreer(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

  const edm::InputTag event_src;
  const edm::InputTag vertices_src;
  const edm::InputTag weight_src;
  const std::string mover_src;
  const double max_dist2move;

  typedef unsigned short ushort;
  struct ntuple_t {
    unsigned run;
    unsigned lumi;
    unsigned event;

    float weight;

    ushort npu;
    ushort npv;
    float pvx;
    float pvy;
    float pvz;
    ushort pvntracks;
    ushort pvsumpt2;

    ushort ntracks;
    ushort nseltracks;

    ushort npreseljets;
    ushort npreselbjets;
    ushort nlightjets;
    std::vector<float> jets_pt;
    std::vector<float> jets_eta;
    std::vector<float> jets_phi;
    std::vector<float> jets_energy;
    std::vector<ushort> jets_ntracks;

    float move_x;
    float move_y;
    float move_z;

    std::vector<float> vtxs_x;
    std::vector<float> vtxs_y;
    std::vector<float> vtxs_z;
    std::vector<ushort> vtxs_ntracks;
    std::vector<ushort> vtxs_ntracksptgt3;
    std::vector<float> vtxs_drmin;
    std::vector<float> vtxs_drmax;
    std::vector<float> vtxs_bs2derr;

    void clear() {
      run = lumi = event = 0;
      weight = pvx = pvy = pvz = move_x = move_y = move_z = 0;
      npu = npv = pvntracks = pvsumpt2 = ntracks = nseltracks = npreseljets = npreselbjets = nlightjets = 0;
      jets_pt.clear();
      jets_eta.clear();
      jets_phi.clear();
      jets_energy.clear();
      jets_ntracks.clear();
      vtxs_x.clear();
      vtxs_y.clear();
      vtxs_z.clear();
      vtxs_ntracks.clear();
      vtxs_ntracksptgt3.clear();
      vtxs_drmin.clear();
      vtxs_drmax.clear();
      vtxs_bs2derr.clear();
    }
  };

  ntuple_t nt;
  TTree* tree;
};

MFVMovedTracksTreer::MFVMovedTracksTreer(const edm::ParameterSet& cfg)
  : event_src(cfg.getParameter<edm::InputTag>("event_src")),
    vertices_src(cfg.getParameter<edm::InputTag>("vertices_src")),
    weight_src(cfg.getParameter<edm::InputTag>("weight_src")),
    mover_src(cfg.getParameter<std::string>("mover_src")),
    max_dist2move(cfg.getParameter<double>("max_dist2move"))
{
  edm::Service<TFileService> fs;

  tree = fs->make<TTree>("t", "");
  tree->SetAlias("njets", "jets_pt@.size()");
  tree->SetAlias("nvtxs", "vtxs_x@.size()");

  tree->Branch("run", &nt.run);
  tree->Branch("lumi", &nt.lumi);
  tree->Branch("event", &nt.event);
  tree->Branch("weight", &nt.weight);
  tree->Branch("npu", &nt.npu);
  tree->Branch("npv", &nt.npv);
  tree->Branch("pvx", &nt.pvx);
  tree->Branch("pvy", &nt.pvy);
  tree->Branch("pvz", &nt.pvz);
  tree->Branch("pvntracks", &nt.pvntracks);
  tree->Branch("pvsumpt2", &nt.pvsumpt2);
  tree->Branch("ntracks", &nt.ntracks);
  tree->Branch("nseltracks", &nt.nseltracks);
  tree->Branch("npreseljets", &nt.npreseljets);
  tree->Branch("npreselbjets", &nt.npreselbjets);
  tree->Branch("nlightjets", &nt.nlightjets);
  tree->Branch("jets_pt", &nt.jets_pt);
  tree->Branch("jets_eta", &nt.jets_eta);
  tree->Branch("jets_phi", &nt.jets_phi);
  tree->Branch("jets_energy", &nt.jets_energy);
  tree->Branch("jets_ntracks", &nt.jets_ntracks);
  tree->Branch("move_x", &nt.move_x);
  tree->Branch("move_y", &nt.move_y);
  tree->Branch("move_z", &nt.move_z);
  tree->Branch("vtxs_x", &nt.vtxs_x);
  tree->Branch("vtxs_y", &nt.vtxs_y);
  tree->Branch("vtxs_z", &nt.vtxs_z);
  tree->Branch("vtxs_ntracks", &nt.vtxs_ntracks);
  tree->Branch("vtxs_ntracksptgt3", &nt.vtxs_ntracksptgt3);
  tree->Branch("vtxs_drmin", &nt.vtxs_drmin);
  tree->Branch("vtxs_drmax", &nt.vtxs_drmax);
  tree->Branch("vtxs_bs2derr", &nt.vtxs_bs2derr);
}

void MFVMovedTracksTreer::analyze(const edm::Event& event, const edm::EventSetup&) {
  nt.clear();

  nt.run   = event.id().run();
  nt.lumi  = event.luminosityBlock();
  nt.event = event.id().event();

  edm::Handle<double> weight;
  event.getByLabel(weight_src, weight);
  nt.weight = *weight;

  edm::Handle<MFVEvent> mevent;
  event.getByLabel(event_src, mevent);

  nt.npu = int(mevent->npu);
  nt.npv = mevent->npv;
  nt.pvx = mevent->pvx - mevent->bsx_at_z(mevent->pvz);
  nt.pvy = mevent->pvy - mevent->bsy_at_z(mevent->pvz);
  nt.pvz = mevent->pvz - mevent->bsz;
  nt.pvntracks = mevent->pv_ntracks;
  nt.pvsumpt2 = mevent->pv_sumpt2;

  edm::Handle<reco::TrackCollection> tracks, moved_tracks;
  edm::Handle<int> npreseljets, npreselbjets;
  edm::Handle<pat::JetCollection> jets_used, bjets_used;
  edm::Handle<std::vector<double> > move_vertex;
  event.getByLabel(edm::InputTag(mover_src),                 tracks);
  event.getByLabel(edm::InputTag(mover_src, "moved"),        moved_tracks);
  event.getByLabel(edm::InputTag(mover_src, "npreseljets"),  npreseljets); 
  event.getByLabel(edm::InputTag(mover_src, "npreselbjets"), npreselbjets); 
  event.getByLabel(edm::InputTag(mover_src, "jetsUsed"),     jets_used);
  event.getByLabel(edm::InputTag(mover_src, "bjetsUsed"),    bjets_used);
  event.getByLabel(edm::InputTag(mover_src, "moveVertex"),   move_vertex);

  nt.ntracks = tracks->size();
  nt.nseltracks = moved_tracks->size();

  nt.npreseljets  = *npreseljets;
  nt.npreselbjets = *npreselbjets;

  nt.nlightjets = jets_used->size();

  for (const pat::JetCollection* jets : { &*jets_used, &*bjets_used }) {
    for (const pat::Jet& jet : *jets) {
      nt.jets_pt.push_back(jet.pt());
      nt.jets_eta.push_back(jet.eta());
      nt.jets_phi.push_back(jet.phi());
      nt.jets_energy.push_back(jet.energy());

      ushort jet_ntracks = 0;
      for (const reco::PFCandidatePtr& pfcand : jet.getPFConstituents())
        if (pfcand->trackRef().isNonnull())
          ++jet_ntracks;
      nt.jets_ntracks.push_back(jet_ntracks);
    }
  }

  nt.move_z = move_vertex->at(2);
  nt.move_x = move_vertex->at(0) - mevent->bsx_at_z(nt.move_z);
  nt.move_y = move_vertex->at(1) - mevent->bsy_at_z(nt.move_z);

  edm::Handle<MFVVertexAuxCollection> vertices;
  event.getByLabel(vertices_src, vertices);

  for (const MFVVertexAux& v : *vertices) {
    const double vx = v.x - mevent->bsx_at_z(v.z);
    const double vy = v.y - mevent->bsy_at_z(v.z);
    const double vz = v.z;

    const double dist2move = pow(pow(vx - nt.move_x, 2) +
                                 pow(vy - nt.move_y, 2) +
                                 pow(vz - nt.move_z, 2), 0.5);
    if (dist2move > max_dist2move)
      continue;

    nt.vtxs_x.push_back(vx);
    nt.vtxs_y.push_back(vy);
    nt.vtxs_z.push_back(vz);
    nt.vtxs_ntracks.push_back(v.ntracks());
    nt.vtxs_ntracksptgt3.push_back(v.ntracksptgt(3));
    nt.vtxs_drmin.push_back(v.drmin());
    nt.vtxs_drmax.push_back(v.drmax());
    nt.vtxs_bs2derr.push_back(v.bs2derr);
  }

  tree->Fill();
}

DEFINE_FWK_MODULE(MFVMovedTracksTreer);
