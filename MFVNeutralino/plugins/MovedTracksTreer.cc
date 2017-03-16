#include "TTree.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralino/interface/MovedTracksNtuple.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"

class MFVMovedTracksTreer : public edm::EDAnalyzer {
public:
  explicit MFVMovedTracksTreer(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

  const edm::EDGetTokenT<MFVEvent> event_token;
  const edm::EDGetTokenT<MFVVertexAuxCollection> vertices_token;
  const edm::EDGetTokenT<double> weight_token;
  const std::string mover_src;
  const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
  const edm::EDGetTokenT<reco::TrackCollection> moved_tracks_token;
  const edm::EDGetTokenT<int> npreseljets_token;
  const edm::EDGetTokenT<int> npreselbjets_token;
  const edm::EDGetTokenT<pat::JetCollection> jets_used_token;
  const edm::EDGetTokenT<pat::JetCollection> bjets_used_token;
  const edm::EDGetTokenT<std::vector<double> > move_vertex_token;
  const double max_dist2move;
  const bool apply_presel;
  const unsigned njets_req;
  const unsigned nbjets_req;
  const bool for_mctruth;

  mfv::MovedTracksNtuple nt;
  TTree* tree;
};

MFVMovedTracksTreer::MFVMovedTracksTreer(const edm::ParameterSet& cfg)
  : event_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("event_src"))),
    vertices_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertices_src"))),
    weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
    mover_src(cfg.getParameter<std::string>("mover_src")),
    tracks_token(consumes<reco::TrackCollection>(edm::InputTag(mover_src))),
    moved_tracks_token(consumes<reco::TrackCollection>(edm::InputTag(mover_src, "moved"))),
    npreseljets_token(consumes<int>(edm::InputTag(mover_src, "npreseljets"))),
    npreselbjets_token(consumes<int>(edm::InputTag(mover_src, "npreselbjets"))),
    jets_used_token(consumes<pat::JetCollection>(edm::InputTag(mover_src, "jetsUsed"))),
    bjets_used_token(consumes<pat::JetCollection>(edm::InputTag(mover_src, "bjetsUsed"))),
    move_vertex_token(consumes<std::vector<double> >(edm::InputTag(mover_src, "moveVertex"))),
    max_dist2move(cfg.getParameter<double>("max_dist2move")),
    apply_presel(cfg.getParameter<bool>("apply_presel")),
    njets_req(cfg.getParameter<unsigned>("njets_req")),
    nbjets_req(cfg.getParameter<unsigned>("nbjets_req")),
    for_mctruth(cfg.getParameter<bool>("for_mctruth"))
{
  edm::Service<TFileService> fs;

  tree = fs->make<TTree>("t", "");
  nt.write_to_tree(tree);
}

void MFVMovedTracksTreer::analyze(const edm::Event& event, const edm::EventSetup&) {
  nt.clear();

  nt.run   = event.id().run();
  nt.lumi  = event.luminosityBlock();
  nt.event = event.id().event();

  edm::Handle<double> weight;
  event.getByToken(weight_token, weight);
  nt.weight = *weight;

  edm::Handle<MFVEvent> mevent;
  event.getByToken(event_token, mevent);

  if (for_mctruth && (nt.gen_valid = mevent->gen_valid)) {
    for (int i = 0; i < 2; ++i) {
      nt.gen_lsp_pt[i] = mevent->gen_lsp_pt[i];
      nt.gen_lsp_eta[i] = mevent->gen_lsp_eta[i];
      nt.gen_lsp_phi[i] = mevent->gen_lsp_phi[i];
      nt.gen_lsp_mass[i] = mevent->gen_lsp_mass[i];
      nt.gen_decay_type[i] = mevent->gen_decay_type[i];

      const double z = nt.gen_lsp_decay[i*3+2] = mevent->gen_lsp_decay[i*3+2];
      nt.gen_lsp_decay[i*3+0] = mevent->gen_lsp_decay[i*3+0] - mevent->bsx_at_z(z);
      nt.gen_lsp_decay[i*3+1] = mevent->gen_lsp_decay[i*3+1] - mevent->bsy_at_z(z);
    }
    nt.gen_partons_in_acc = mevent->gen_partons_in_acc;
  }

  nt.pass_hlt = mevent->pass_ & 0x1F;
  nt.npu = int(mevent->npu);
  nt.npv = mevent->npv;
  nt.pvx = mevent->pvx - mevent->bsx_at_z(mevent->pvz);
  nt.pvy = mevent->pvy - mevent->bsy_at_z(mevent->pvz);
  nt.pvz = mevent->pvz;
  nt.pvntracks = mevent->pv_ntracks;
  nt.pvsumpt2 = mevent->pv_sumpt2;
  nt.jetht = mevent->jet_ht(40);
  nt.jetpt4 = mevent->jetpt4();
  nt.met = mevent->met();
  nt.nlep = mevent->nlep(2);
  nt.nalljets = mevent->njets();

  if (!for_mctruth) {
    edm::Handle<reco::TrackCollection> tracks, moved_tracks;
    edm::Handle<int> npreseljets, npreselbjets;
    edm::Handle<pat::JetCollection> jets_used, bjets_used;
    edm::Handle<std::vector<double> > move_vertex;
    event.getByToken(tracks_token,       tracks);
    event.getByToken(moved_tracks_token, moved_tracks);
    event.getByToken(npreseljets_token,  npreseljets);
    event.getByToken(npreselbjets_token, npreselbjets);
    event.getByToken(jets_used_token,    jets_used);
    event.getByToken(bjets_used_token,   bjets_used);
    event.getByToken(move_vertex_token,  move_vertex);

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
  }

  edm::Handle<MFVVertexAuxCollection> vertices;
  event.getByToken(vertices_token, vertices);

  for (const MFVVertexAux& v : *vertices) {
    const double vx = v.x - mevent->bsx_at_z(v.z);
    const double vy = v.y - mevent->bsy_at_z(v.z);
    const double vz = v.z;

    if (!for_mctruth) {
      const double dist2move = pow(pow(vx - nt.move_x, 2) +
                                   pow(vy - nt.move_y, 2) +
                                   pow(vz - nt.move_z, 2), 0.5);
      if (dist2move > max_dist2move)
        continue;
    }

    nt.vtxs_x.push_back(vx);
    nt.vtxs_y.push_back(vy);
    nt.vtxs_z.push_back(vz);
    nt.vtxs_theta.push_back(2*atan(exp(-v.eta[mfv::PTracksPlusJetsByNtracks])));
    nt.vtxs_phi.push_back(v.phi[mfv::PTracksPlusJetsByNtracks]);
    nt.vtxs_ntracks.push_back(v.ntracks());
    nt.vtxs_ntracksptgt3.push_back(v.ntracksptgt(3));
    nt.vtxs_drmin.push_back(v.drmin());
    nt.vtxs_drmax.push_back(v.drmax());
    nt.vtxs_bs2derr.push_back(v.bs2derr);
  }

  if (apply_presel) {
    if ((!for_mctruth && (nt.npreseljets < njets_req || nt.npreselbjets < nbjets_req)) ||
        nt.jetht < 1000)
    return;
  }

  tree->Fill();
}

DEFINE_FWK_MODULE(MFVMovedTracksTreer);
