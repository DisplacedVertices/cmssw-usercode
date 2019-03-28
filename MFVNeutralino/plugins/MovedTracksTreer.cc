#include "TTree.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralino/interface/Ntuple.h"
#include "JMTucker/MFVNeutralino/interface/NtupleFiller.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/Tools/interface/Utilities.h"

class MFVMovedTracksTreer : public edm::EDAnalyzer {
public:
  explicit MFVMovedTracksTreer(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

private:
  jmt::BaseSubNtupleFiller base_filler;
  jmt::BeamspotSubNtupleFiller bs_filler;
  jmt::PrimaryVerticesSubNtupleFiller pvs_filler;
  jmt::JetsSubNtupleFiller jets_filler;
  mfv::GenTruthSubNtupleFiller gentruth_filler;
  const edm::EDGetTokenT<MFVVertexAuxCollection> vertices_token;
  const edm::EDGetTokenT<double> weight_token;
  const edm::EDGetTokenT<std::vector<reco::TrackRef>> sel_tracks_token;
  const std::string mover_src;
  const edm::EDGetTokenT<reco::TrackCollection> all_tracks_token;
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
  : base_filler(nt.base(), cfg, consumesCollector()),
    bs_filler(nt.bs(), cfg, consumesCollector()),
    pvs_filler(nt.pvs(), cfg, consumesCollector(), true, false),
    jets_filler(nt.jets(), cfg, consumesCollector()),
    gentruth_filler(nt.gentruth(), cfg, consumesCollector()),
    vertices_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertices_src"))),
    sel_tracks_token(consumes<std::vector<reco::TrackRef>>(cfg.getParameter<edm::InputTag>("sel_tracks_src"))),
    mover_src(cfg.getParameter<std::string>("mover_src")),
    all_tracks_token(consumes<reco::TrackCollection>(edm::InputTag(mover_src))),
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

namespace {
  double mag2(double x, double y, double z)           { return x*x + y*y + z*z; }
  double mag2(double x, double y, double z, double w) { return x*x + y*y + z*z + w*w; }
}

void MFVMovedTracksTreer::analyze(const edm::Event& event, const edm::EventSetup&) {
  nt.clear();

  base_filler(event);
  bs_filler(event);
  pvs_filler(event, &bs_filler.bs());
  jets_filler(event);
  gentruth_filler(event);

  if (!for_mctruth) {
    edm::Handle<reco::TrackCollection> all_tracks, moved_tracks;
    edm::Handle<std::vector<reco::TrackRef>> sel_tracks;
    edm::Handle<int> npreseljets, npreselbjets;
    edm::Handle<pat::JetCollection> jets_used, bjets_used;
    edm::Handle<std::vector<double> > move_vertex;
    event.getByToken(all_tracks_token,   all_tracks);
    event.getByToken(sel_tracks_token,   sel_tracks);
    event.getByToken(moved_tracks_token, moved_tracks);
    event.getByToken(npreseljets_token,  npreseljets);
    event.getByToken(npreselbjets_token, npreselbjets);
    event.getByToken(jets_used_token,    jets_used);
    event.getByToken(bjets_used_token,   bjets_used);
    event.getByToken(move_vertex_token,  move_vertex);

    nt.tm().set(all_tracks->size(), moved_tracks->size(), *npreseljets, *npreselbjets,
                (*move_vertex)[0] - bs_filler.bs().x((*move_vertex)[2]),
                (*move_vertex)[1] - bs_filler.bs().y((*move_vertex)[2]),
                (*move_vertex)[2]);

    auto tks_push_back = [&](const reco::Track& tk) { NtupleAdd(nt.tracks(), tk); };

    for (const reco::TrackRef& tk : *sel_tracks)
      tks_push_back(*tk);

    for (const reco::Track& tk : *moved_tracks) {
      double dist2min = 0.1;
      int which = -1;
      for (int i = 0, ie = nt.tracks().n(); i < ie; ++i) {
        const double dist2 = mag2(tk.charge() * tk.pt() - nt.tracks().qpt(i),
                                  tk.eta()              - nt.tracks().eta(i),
                                  tk.phi()              - nt.tracks().phi(i));
        if (dist2 < dist2min) {
          dist2min = dist2;
          which = i;
        }
      }

      if (which == -1) {
        which = nt.tracks().n();
        tks_push_back(tk);
      }

      nt.set_tk_moved(which);
    }

    for (const pat::Jet& jet : jets_filler.jets(event)) {
      double dist2min = 0.1;
      int whichjet = -1;

      for (int j = 0, je = nt.jets().n(); j < je; ++j) {
        const double dist2 = mag2(jet.pt()     - nt.jets().pt(j),
                                  jet.eta()    - nt.jets().eta(j),
                                  jet.phi()    - nt.jets().phi(j),
                                  jet.energy() - nt.jets().energy(j));
        if (dist2 < dist2min) {
          dist2min = dist2;
          whichjet = j;
        }
      }

      assert(whichjet != -1);

      for (size_t idau = 0, idaue = jet.numberOfDaughters(); idau < idaue; ++idau) {
        const reco::Track* tk = jetDaughterTrack(jet, idau);
        if (tk) {
          double dist2min = 0.1;
          int whichtk = -1;
          for (size_t i = 0, ie = nt.tracks().n(); i < ie; ++i) {
            const double dist2 = mag2(tk->charge() * tk->pt() - nt.tracks().qpt(i),
                                      tk->eta()               - nt.tracks().eta(i),
                                      tk->phi()               - nt.tracks().phi(i));
            if (dist2 < dist2min) {
              dist2min = dist2;
              whichtk = i;
            }
          }
          if (whichtk != -1)
            nt.tracks().set_which_jet(whichtk, whichjet);
        }
      }
    }

    const size_t nmovedjets = jets_used->size() + bjets_used->size();
    std::vector<int> whichs(nmovedjets, -1);

    int i = -1;
    for (const pat::JetCollection* jets : { &*jets_used, &*bjets_used }) {
      for (const pat::Jet& jet : *jets) {
        ++i;
        double dist2min = 0.1;
        int which = -1;

        for (size_t j = 0, je = nt.jets().n(); j < je; ++j) {
          const double dist2 = mag2(jet.pt()     - nt.jets().pt(j),
                                    jet.eta()    - nt.jets().eta(j),
                                    jet.phi()    - nt.jets().phi(j),
                                    jet.energy() - nt.jets().energy(j));
          if (dist2 < dist2min) {
            dist2min = dist2;
            which = j;
          }
        }

        assert(which != -1);
        whichs[i] = which;
        nt.set_jet_moved(which);
      }
    }

    for (size_t i = 0; i < nmovedjets; ++i)
      for (size_t j = i+1; j < nmovedjets; ++j)
        assert(whichs[i] != whichs[j]);
  }

  edm::Handle<MFVVertexAuxCollection> vertices;
  event.getByToken(vertices_token, vertices);

  for (const MFVVertexAux& v : *vertices) {
    const double vx = v.x - bs_filler.bs().x(v.z);
    const double vy = v.y - bs_filler.bs().y(v.z);
    const double vz = v.z;

    if (!for_mctruth) {
      const double dist2move = sqrt(mag2(vx - nt.tm().move_x(),
                                         vy - nt.tm().move_y(),
                                         vz - nt.tm().move_z()));
      if (dist2move > max_dist2move)
        continue;
    }

    nt.vertices().add(vx, vy, vz,
                      v.cxx, v.cxy, v.cxz, v.cyy, v.cyz, v.czz,
                      v.ntracks(), v.bs2derr, v.geo2ddist(), false,
                      v.pt[mfv::PTracksPlusJetsByNtracks], v.eta[mfv::PTracksPlusJetsByNtracks], v.phi[mfv::PTracksPlusJetsByNtracks], v.mass[mfv::PTracksPlusJetsByNtracks],
                      v.mass[mfv::PTracksOnly]);

    if (!for_mctruth)
      for (size_t i = 0, ie = v.ntracks(); i < ie; ++i) {
        double dist2min = 0.1;
        int which = -1;
        for (size_t j = 0, je = nt.tracks().n(); j < je; ++j) {
          const double dist2 = mag2(v.track_qpt(i) - nt.tracks().qpt(j),
                                    v.track_eta[i] - nt.tracks().eta(j),
                                    v.track_phi[i] - nt.tracks().phi(j));
          if (dist2 < dist2min) {
            dist2min = dist2;
            which = j;
          }
        }

        assert(which != -1);
        assert(nt.tracks().which_sv(which) == 255);
        const size_t iv = nt.vertices().n() - 1;
        assert(iv < 255);
        nt.tracks().set_which_sv(which, iv);
      }
  }

  if (apply_presel) {
    if ((!for_mctruth && (nt.tm().npreseljets() < njets_req || nt.tm().npreselbjets() < nbjets_req)) ||
        nt.jets().ht() < 1000)
    return;
  }

  tree->Fill();
}

DEFINE_FWK_MODULE(MFVMovedTracksTreer);
