#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/MFVNeutralino/interface/TrackerSpaceExtent.h"
#include "JMTucker/MFVNeutralino/interface/VertexTools.h"
#include "JMTucker/Tools/interface/Utilities.h"

namespace {
  template <typename T, typename T2>
  double dot3(const T& a, const T2& b) {
    return a.x() * b.x() + a.y() * b.y() + a.z() * b.z();
  }

  template <typename T, typename T2>
  double costh3(const T& a, const T2& b) {
    return dot3(a,b) / mag(a.x(), a.y(), a.z()) / mag(b.x(), b.y(), b.z());
  }
}

class MFVVertexAuxProducer : public edm::EDProducer {
 public:
  explicit MFVVertexAuxProducer(const edm::ParameterSet&);
  void produce(edm::Event&, const edm::EventSetup&);

 private:
  const edm::InputTag primary_vertex_src;
  const edm::InputTag muons_src;
  const edm::InputTag electrons_src;
  const edm::InputTag gen_vertices_src;
  const edm::InputTag vertex_src;
  const std::string sv_to_jets_src;
  const MFVVertexAuxSorter sorter;
};

MFVVertexAuxProducer::MFVVertexAuxProducer(const edm::ParameterSet& cfg)
  : primary_vertex_src(cfg.getParameter<edm::InputTag>("primary_vertex_src")),
    muons_src(cfg.getParameter<edm::InputTag>("muons_src")),
    electrons_src(cfg.getParameter<edm::InputTag>("electrons_src")),
    gen_vertices_src(cfg.getParameter<edm::InputTag>("gen_vertices_src")),
    vertex_src(cfg.getParameter<edm::InputTag>("vertex_src")),
    sv_to_jets_src(cfg.getParameter<std::string>("sv_to_jets_src")),
    sorter(cfg.getParameter<std::string>("sort_by"))
{
  produces<std::vector<MFVVertexAux> >();
}

void MFVVertexAuxProducer::produce(edm::Event& event, const edm::EventSetup& setup) {

  //////////////////////////////////////////////////////////////////////

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByLabel("offlineBeamSpot", beamspot);
  const float bsx = beamspot->x0();
  const float bsy = beamspot->y0();
  const float bsz = beamspot->z0();

  //////////////////////////////////////////////////////////////////////

  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByLabel(primary_vertex_src, primary_vertices);
  const reco::Vertex* primary_vertex = 0;
  if (primary_vertices->size())
    primary_vertex = &primary_vertices->at(0);

  std::map<reco::TrackRef, std::vector<std::pair<int, float> > > tracks_in_pvs;
  for (size_t i = 0, ie = primary_vertices->size(); i < ie; ++i) {
    const reco::Vertex& pv = primary_vertices->at(i);
    for (auto it = pv.tracks_begin(), ite = pv.tracks_end(); it != ite; ++it) {
      float w = pv.trackWeight(*it);
      reco::TrackRef tk = it->castTo<reco::TrackRef>();
      tracks_in_pvs[tk].push_back(std::make_pair(i, w));
    }
  }

  //////////////////////////////////////////////////////////////////////

  edm::Handle<pat::MuonCollection> muons;
  event.getByLabel(muons_src, muons);

  edm::Handle<pat::ElectronCollection> electrons;
  event.getByLabel(electrons_src, electrons);

  //////////////////////////////////////////////////////////////////////

  TrackerSpaceExtents tracker_extents;
  tracker_extents.fill(setup, GlobalPoint(bsx, bsy, bsz));
  
  //////////////////////////////////////////////////////////////////////

  edm::Handle<std::vector<double> > gen_vertices;
  event.getByLabel(gen_vertices_src, gen_vertices);

  //////////////////////////////////////////////////////////////////////

  edm::Handle<reco::VertexCollection> secondary_vertices;
  event.getByLabel(vertex_src, secondary_vertices);
  const int nsv = int(secondary_vertices->size());

  const bool use_sv_to_jets = sv_to_jets_src != "dummy";
  edm::Handle<mfv::JetVertexAssociation> sv_to_jets[mfv::NJetsByUse];
  std::set<reco::TrackRef> jets_tracks;
  if (use_sv_to_jets)
    for (int i = 0; i < mfv::NJetsByUse; ++i)
      event.getByLabel(edm::InputTag(sv_to_jets_src, mfv::jetsby_names[i]), sv_to_jets[i]);

  //////////////////////////////////////////////////////////////////////

  std::auto_ptr<std::vector<MFVVertexAux> > auxes(new std::vector<MFVVertexAux>(nsv));
  std::set<int> trackicity;

  for (int isv = 0; isv < nsv; ++isv) {
    const reco::Vertex& sv = secondary_vertices->at(isv);
    const reco::VertexRef svref(secondary_vertices, isv);
    MFVVertexAux& aux = auxes->at(isv);
    aux.which = int2uchar(isv);

    aux.x = sv.x();
    aux.y = sv.y();
    aux.z = sv.z();

    aux.cxx = sv.covariance(0,0);
    aux.cxy = sv.covariance(0,1);
    aux.cxz = sv.covariance(0,2);
    aux.cyy = sv.covariance(1,1);
    aux.cyz = sv.covariance(1,2);
    aux.czz = sv.covariance(2,2);

    aux.chi2 = sv.chi2();
    aux.ndof = sv.ndof();

    aux.bs_x = bsx;
    aux.bs_y = bsy;
    aux.bs_z = bsz;

    aux.bs_cxx = beamspot->covariance3D()(0,0);
    aux.bs_cxy = beamspot->covariance3D()(0,1);
    aux.bs_cxz = beamspot->covariance3D()(0,2);
    aux.bs_cyy = beamspot->covariance3D()(1,1);
    aux.bs_cyz = beamspot->covariance3D()(1,2);
    aux.bs_czz = beamspot->covariance3D()(2,2);

    aux.pv_x = primary_vertex->x();
    aux.pv_y = primary_vertex->y();
    aux.pv_z = primary_vertex->z();

    aux.pv_cxx = primary_vertex->covariance(0,0);
    aux.pv_cxy = primary_vertex->covariance(0,1);
    aux.pv_cxz = primary_vertex->covariance(0,2);
    aux.pv_cyy = primary_vertex->covariance(1,1);
    aux.pv_cyz = primary_vertex->covariance(1,2);
    aux.pv_czz = primary_vertex->covariance(2,2);

    if (use_sv_to_jets) {
      assert(mfv::NJetsByUse == 1); // otherwise NMomenta is wrong, and we don't handle jet_assoctype in VertexAux (yet)

      for (int i = 0; i < mfv::NJetsByUse; ++i) {
        int njets = sv_to_jets[i]->numberOfAssociations(svref);
        if (njets) {
          const edm::RefVector<pat::JetCollection>& jets = (*sv_to_jets[i])[svref];

          for (int ijet = 0; ijet < njets; ++ijet) {
            aux.jet_pt.push_back(jets[ijet]->pt());
            aux.jet_eta.push_back(jets[ijet]->eta());
            aux.jet_phi.push_back(jets[ijet]->phi());
            aux.jet_energy.push_back(jets[ijet]->energy());

            for (const reco::PFCandidatePtr& pfcand : jets[ijet]->getPFConstituents()) {
              const reco::TrackRef& tk = pfcand->trackRef();
              if (tk.isNonnull())
                jets_tracks.insert(tk);
            }
          }
        }
      }

      aux.costhjetmomvtxdispmin = aux.costhjetmomvtxdispmax = aux.costhjetmomvtxdispavg = aux.costhjetmomvtxdisprms = -2;
    }

    
    const double sv_r = mag(sv.position().x() - bsx, sv.position().y() - bsy);
    const double sv_z = fabs(sv.position().z() - bsz);

    auto trkb = sv.tracks_begin();
    auto trke = sv.tracks_end();

    for (auto trki = trkb; trki != trke; ++trki) {
      const reco::TrackBaseRef& tri = *trki;
      const reco::TrackRef& trref = tri.castTo<reco::TrackRef>();
      const math::XYZTLorentzVector tri_p4(tri->px(), tri->py(), tri->pz(), tri->p());

      if (trackicity.count(tri.key()) > 0)
        throw cms::Exception("VertexAuxProducer") << "trackicity > 1";
      else
        trackicity.insert(tri.key());

      if (sv.trackWeight(tri) < mfv::track_vertex_weight_min)
        continue;

      if (tri->ptError() / tri->pt() > 0.5) {
        // For really bad tracks, only store the track weight and the
        // pt(error). insert_track makes a placeholder so the vectors
        // don't get out of sync JMTBAD.
        aux.insert_track();
        aux.track_w.back() = sv.trackWeight(tri);
        aux.track_pt_err.back() = tri->ptError();
        aux.track_pt.back() = tri->pt();
        continue;
      }


      assert(muons->size() <= 128);
      assert(electrons->size() <= 128);
      for (size_t i = 0, ie = muons->size(); i < ie; ++i)
        if (muons->at(i).track() == trref)
          aux.which_lep.push_back(i);
      if (aux.which_lep.size() == 0) // if a muon matched, don't check for electrons
        for (size_t i = 0, ie = electrons->size(); i < ie; ++i)
          if (electrons->at(i).closestCtfTrackRef() == trref)
            aux.which_lep.push_back(i | (1<<7));


      aux.track_w.push_back(MFVVertexAux::make_track_weight(sv.trackWeight(tri)));
      aux.track_chg.push_back(MFVVertexAux::make_track_q(tri->charge()));
      aux.track_pt.push_back(tri->pt());
      aux.track_eta.push_back(tri->eta());
      aux.track_phi.push_back(tri->phi());
      aux.track_dxy.push_back(fabs(tri->dxy(beamspot->position())));
      aux.track_dz.push_back(primary_vertex ? fabs(tri->dz(primary_vertex->position())) : 0); // JMTBAD not the previous behavior when no PV
      aux.track_pt_err.push_back(tri->ptError()/tri->pt());
      aux.track_dxy_err.push_back(tri->dxyError());
      aux.track_dz_err.push_back(tri->dzError());
      aux.track_chi2dof.push_back(tri->normalizedChi2());
      aux.track_hitpattern.push_back(MFVVertexAux::make_track_hitpattern(tri->hitPattern().numberOfValidPixelHits(),
                                                                         tri->hitPattern().numberOfValidStripHits(),
                                                                         tracker_extents.numHitsBehind(tri->hitPattern(), sv_r, sv_z)));
      aux.track_injet.push_back(jets_tracks.count(trref));
      
      const std::vector<std::pair<int, float> >& pv_for_track = tracks_in_pvs[trref];
      if (pv_for_track.size() > 1)
        throw cms::Exception("VertexAuxProducer") << "multiple PV for a track";
      aux.track_inpv.push_back(pv_for_track.size() ? pv_for_track[0].first : -1);
    }

    auto g2d = mfv::gen_dist(sv, *gen_vertices, false);
    auto g3d = mfv::gen_dist(sv, *gen_vertices, true);
    aux.gen2ddist       = g2d.value();
    aux.gen2derr        = g2d.error();
    aux.gen3ddist       = g3d.value();
    aux.gen3derr        = g3d.error();

//    for (int i = 0; i < mfv::NMomenta; ++i) {
//      aux.costhmombs  [i] = vtx_distances.costhmombs[i];
//      aux.costhmompv2d[i] = vtx_distances.costhmompv2d[i];
//      aux.costhmompv3d[i] = vtx_distances.costhmompv3d[i];
//
//      aux.missdistpv   [i] = vtx_distances.missdistpv[i].value();
//      aux.missdistpverr[i] = vtx_distances.missdistpv[i].error();
//    }

    assert(aux.tracks_ok() && aux.jets_ok());
  }

  sorter.sort(*auxes);

  event.put(auxes);
}

DEFINE_FWK_MODULE(MFVVertexAuxProducer);
