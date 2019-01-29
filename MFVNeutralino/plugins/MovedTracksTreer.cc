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

private:
  const edm::EDGetTokenT<MFVEvent> event_token;
  const edm::EDGetTokenT<MFVVertexAuxCollection> vertices_token;
  const edm::EDGetTokenT<double> weight_token;
  const edm::EDGetTokenT<std::vector<reco::TrackRef>> sel_tracks_token;
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
    sel_tracks_token(consumes<std::vector<reco::TrackRef>>(cfg.getParameter<edm::InputTag>("sel_tracks_src"))),
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

namespace {
  double mag2(double x, double y, double z)           { return x*x + y*y + z*z; }
  double mag2(double x, double y, double z, double w) { return x*x + y*y + z*z + w*w; }
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
    for (auto p : mevent->gen_daughters) {
      nt.gen_daughter_pt.push_back(p.Pt());
      nt.gen_daughter_eta.push_back(p.Eta());
      nt.gen_daughter_phi.push_back(p.Phi());
      nt.gen_daughter_mass.push_back(p.M());
    }
    nt.gen_daughter_id = mevent->gen_daughter_id;
  }

  static_assert(mfv::n_hlt_paths <= 8);
  nt.pass_hlt = mevent->pass_hlt_bits();
  nt.bsx = mevent->bsx;
  nt.bsy = mevent->bsy;
  nt.bsz = mevent->bsz;
  nt.bsdxdz = mevent->bsdxdz;
  nt.bsdydz = mevent->bsdydz;
  nt.npu = int(mevent->npu);
  nt.npv = mevent->npv;
  nt.pvx = mevent->pvx - mevent->bsx_at_z(mevent->pvz);
  nt.pvy = mevent->pvy - mevent->bsy_at_z(mevent->pvz);
  nt.pvz = mevent->pvz;
  nt.pvntracks = mevent->pv_ntracks;
  nt.pvsumpt2 = mevent->pv_sumpt2;
  nt.jetht = mevent->jet_ht(40);

  for (size_t i = 0, ie = mevent->njets(); i < ie; ++i) {
    if (mevent->jet_pt[i] < mfv::min_jet_pt)
      continue;
    nt.alljets_pt.push_back(mevent->jet_pt[i]);
    nt.alljets_eta.push_back(mevent->jet_eta[i]);
    nt.alljets_phi.push_back(mevent->jet_phi[i]);
    nt.alljets_energy.push_back(mevent->jet_energy[i]);
    nt.alljets_ntracks.push_back(mevent->n_jet_tracks(i));
    nt.alljets_bdisc.push_back(mevent->jet_bdisc[i]);
    nt.alljets_hadronflavor.push_back(mevent->jet_hadron_flavor(i));
    nt.alljets_moved.push_back(false); // set below
  }

  TVector3 move_vector;

  if (!for_mctruth) {
    edm::Handle<reco::TrackCollection> tracks, moved_tracks;
    edm::Handle<std::vector<reco::TrackRef>> sel_tracks;
    edm::Handle<int> npreseljets, npreselbjets;
    edm::Handle<pat::JetCollection> jets_used, bjets_used;
    edm::Handle<std::vector<double> > move_vertex;
    event.getByToken(tracks_token,       tracks);
    event.getByToken(sel_tracks_token,   sel_tracks);
    event.getByToken(moved_tracks_token, moved_tracks);
    event.getByToken(npreseljets_token,  npreseljets);
    event.getByToken(npreselbjets_token, npreselbjets);
    event.getByToken(jets_used_token,    jets_used);
    event.getByToken(bjets_used_token,   bjets_used);
    event.getByToken(move_vertex_token,  move_vertex);

    nt.ntracks = tracks->size();
    nt.nmovedtracks = moved_tracks->size();

    auto tks_push_back = [&](const reco::Track& tk) {
      nt.tks_qpt.push_back(tk.charge() * tk.pt());
      nt.tks_eta.push_back(tk.eta());
      nt.tks_phi.push_back(tk.phi());
      nt.tks_dxy.push_back(tk.dxy(reco::TrackBase::Point(mevent->bsx_at_z(tk.vz()), mevent->bsy_at_z(tk.vz()), 0)));
      nt.tks_dz.push_back(tk.dxy(reco::TrackBase::Point(mevent->pvx, mevent->pvy, mevent->pvz)));
      nt.tks_err_pt.push_back(tk.ptError());
      nt.tks_err_eta.push_back(tk.etaError());
      nt.tks_err_phi.push_back(tk.phiError());
      nt.tks_err_dxy.push_back(tk.dxyError());
      nt.tks_err_dz.push_back(tk.dzError());
      nt.tks_hp_.push_back(mfv::HitPattern(tk.hitPattern().numberOfValidPixelHits(), tk.hitPattern().numberOfValidStripHits(), tk.hitPattern().pixelLayersWithMeasurement(), tk.hitPattern().stripLayersWithMeasurement()).value);
      nt.tks_moved.push_back(0);
      nt.tks_vtx.push_back(255);
    };

    for (const reco::TrackRef& tk : *sel_tracks)
      tks_push_back(*tk);

    for (const reco::Track& tk : *moved_tracks) {
      double dist2min = 0.1;
      int which = -1;
      for (size_t i = 0, ie = nt.ntks(); i < ie; ++i) {
        const double dist2 = mag2(tk.charge() * tk.pt() - nt.tks_qpt[i],
                                  tk.eta() - nt.tks_eta[i],
                                  tk.phi() - nt.tks_phi[i]);
        if (dist2 < dist2min) {
          dist2min = dist2;
          which = i;
        }
      }

      if (which == -1) { // moved tracks don't have to be selected
        tks_push_back(tk);
        nt.tks_moved.back() = true;
      }
      else
        nt.tks_moved[which] = true;
    }

    nt.npreseljets  = *npreseljets;
    nt.npreselbjets = *npreselbjets;

    const size_t nalljets = nt.alljets_pt.size();
    const size_t nmovedjets = jets_used->size() + bjets_used->size();
    std::vector<int> whichs(nmovedjets, -1);

    int ijet = -1;
    for (const pat::JetCollection* jets : { &*jets_used, &*bjets_used }) {
      for (const pat::Jet& jet : *jets) {
        ++ijet;
        double dist2min = 0.1;
        int which = -1;

        for (size_t j = 0; j < nalljets; ++j) {
          const double dist2 = mag2(jet.pt()     - nt.alljets_pt[j],
                                    jet.eta()    - nt.alljets_eta[j],
                                    jet.phi()    - nt.alljets_phi[j],
                                    jet.energy() - nt.alljets_energy[j]);
          if (dist2 < dist2min) {
            dist2min = dist2;
            which = j;
          }
        }

        assert(which != -1);
        whichs[ijet] = which;
        nt.alljets_moved[which] = true;
      }
    }

    for (size_t i = 0; i < nmovedjets; ++i)
      for (size_t j = i+1; j < nmovedjets; ++j)
        assert(whichs[i] != whichs[j]);

    nt.move_z = move_vertex->at(2);
    nt.move_x = move_vertex->at(0) - mevent->bsx_at_z(nt.move_z);
    nt.move_y = move_vertex->at(1) - mevent->bsy_at_z(nt.move_z);

    move_vector.SetXYZ(move_vertex->at(0) - mevent->pvx,
                       move_vertex->at(1) - mevent->pvy,
                       move_vertex->at(2) - mevent->pvz);
  }

  edm::Handle<MFVVertexAuxCollection> vertices;
  event.getByToken(vertices_token, vertices);

  for (const MFVVertexAux& v : *vertices) {
    const double vx = v.x - mevent->bsx_at_z(v.z);
    const double vy = v.y - mevent->bsy_at_z(v.z);
    const double vz = v.z;

    if (!for_mctruth) {
      const double dist2move = sqrt(mag2(vx - nt.move_x,
                                         vy - nt.move_y,
                                         vz - nt.move_z));
      if (dist2move > max_dist2move)
        continue;
    }

    nt.vtxs_x.push_back(vx);
    nt.vtxs_y.push_back(vy);
    nt.vtxs_z.push_back(vz);
    nt.vtxs_pt.push_back(v.pt[mfv::PTracksPlusJetsByNtracks]);
    nt.vtxs_theta.push_back(2*atan(exp(-v.eta[mfv::PTracksPlusJetsByNtracks])));
    nt.vtxs_phi.push_back(v.phi[mfv::PTracksPlusJetsByNtracks]);
    nt.vtxs_mass.push_back(v.mass[mfv::PTracksPlusJetsByNtracks]);
    nt.vtxs_tkonlymass.push_back(v.mass[mfv::PTracksOnly]);
    nt.vtxs_ntracks.push_back(v.ntracks());
    nt.vtxs_bs2derr.push_back(v.bs2derr);

    if (!for_mctruth)
      for (size_t i = 0, ie = v.ntracks(); i < ie; ++i) {
        double dist2min = 0.1;
        int which = -1;
        for (size_t j = 0, je = nt.ntks(); j < je; ++j) {
          const double dist2 = mag2(v.track_qpt(i) - nt.tks_qpt[j],
                                    v.track_eta[i] - nt.tks_eta[j],
                                    v.track_phi[i] - nt.tks_phi[j]);
          if (dist2 < dist2min) {
            dist2min = dist2;
            which = j;
          }
        }

        assert(which != -1);
        assert(nt.tks_vtx[which] == 255);
        const size_t iv = nt.nvtxs() - 1;
        assert(iv < 255);
        nt.tks_vtx[which] = iv;
      }
  }

  if (apply_presel) {
    if ((!for_mctruth && (nt.npreseljets < njets_req || nt.npreselbjets < nbjets_req)) ||
        nt.jetht < 1000)
    return;
  }

  tree->Fill();
}

DEFINE_FWK_MODULE(MFVMovedTracksTreer);
