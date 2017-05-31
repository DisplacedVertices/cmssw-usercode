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
  const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
  const edm::EDGetTokenT<reco::VertexCollection> primary_vertex_token;
  const edm::EDGetTokenT<pat::MuonCollection> muons_token;
  const edm::EDGetTokenT<pat::ElectronCollection> electrons_token;
  const edm::EDGetTokenT<std::vector<double> > gen_vertices_token;
  const edm::EDGetTokenT<reco::VertexCollection> vertex_token;
  const std::string sv_to_jets_src;
  edm::EDGetTokenT<mfv::JetVertexAssociation> sv_to_jets_token[mfv::NJetsByUse];
  const MFVVertexAuxSorter sorter;
};

MFVVertexAuxProducer::MFVVertexAuxProducer(const edm::ParameterSet& cfg)
  : beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot_src"))),
    primary_vertex_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("primary_vertex_src"))),
    muons_token(consumes<pat::MuonCollection>(cfg.getParameter<edm::InputTag>("muons_src"))),
    electrons_token(consumes<pat::ElectronCollection>(cfg.getParameter<edm::InputTag>("electrons_src"))),
    gen_vertices_token(consumes<std::vector<double> >(cfg.getParameter<edm::InputTag>("gen_vertices_src"))),
    vertex_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("vertex_src"))),
    sv_to_jets_src(cfg.getParameter<std::string>("sv_to_jets_src")),
    //sv_to_jets_token(consumes<mfv::JetVertexAssociation>(edm::InputTag("sv_to_jets_src"))),
    sorter(cfg.getParameter<std::string>("sort_by"))
{
  for (int i = 0; i < mfv::NJetsByUse; ++i)
    sv_to_jets_token[i] = consumes<mfv::JetVertexAssociation>(edm::InputTag(sv_to_jets_src, mfv::jetsby_names[i])); // JMTBAD yuck, rethink

  produces<std::vector<MFVVertexAux> >();
}

void MFVVertexAuxProducer::produce(edm::Event& event, const edm::EventSetup& setup) {

  //////////////////////////////////////////////////////////////////////

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByToken(beamspot_token, beamspot);
  const float bsx = beamspot->x0();
  const float bsy = beamspot->y0();
  const float bsz = beamspot->z0();
  const GlobalPoint origin(bsx, bsy, bsz);
  const reco::Vertex fake_bs_vtx(beamspot->position(), beamspot->covariance3D());

  //////////////////////////////////////////////////////////////////////

  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByToken(primary_vertex_token, primary_vertices);
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
  event.getByToken(muons_token, muons);

  edm::Handle<pat::ElectronCollection> electrons;
  event.getByToken(electrons_token, electrons);

  //////////////////////////////////////////////////////////////////////

  edm::Handle<std::vector<double> > gen_vertices;
  event.getByToken(gen_vertices_token, gen_vertices);

  //////////////////////////////////////////////////////////////////////

  edm::Handle<reco::VertexCollection> secondary_vertices;
  event.getByToken(vertex_token, secondary_vertices);
  const int nsv = int(secondary_vertices->size());

  const bool use_sv_to_jets = sv_to_jets_src != "dummy";
  edm::Handle<mfv::JetVertexAssociation> sv_to_jets[mfv::NJetsByUse];
  if (use_sv_to_jets)
    for (int i = 0; i < mfv::NJetsByUse; ++i)
      event.getByToken(sv_to_jets_token[i], sv_to_jets[i]);

  //////////////////////////////////////////////////////////////////////

  std::auto_ptr<std::vector<MFVVertexAux> > auxes(new std::vector<MFVVertexAux>(nsv));
  std::set<int> trackicity;

  for (int isv = 0; isv < nsv; ++isv) {
    const reco::Vertex& sv = secondary_vertices->at(isv);
    const reco::VertexRef svref(secondary_vertices, isv);
    MFVVertexAux& aux = auxes->at(isv);
    aux.which = int2uchar(isv);
    aux.which_lep.clear();

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
    aux.ndof_ = int2uchar_clamp(int(sv.ndof()));

    math::XYZVector pv2sv;
    if (primary_vertex != 0)
      pv2sv = sv.position() - primary_vertex->position();

    std::vector<math::XYZTLorentzVector> p4s(mfv::NMomenta);
    p4s[mfv::PTracksOnly] = sv.p4();

    for (int i = 0; i < mfv::NJetsByUse; ++i)
      aux.njets[i] = 0;

    std::vector<double> jetpairdetas[mfv::NJetsByUse];
    std::vector<double> jetpairdrs[mfv::NJetsByUse];
    std::vector<double> costhjetmomvtxdisps[mfv::NJetsByUse];
    std::set<reco::TrackRef> jets_tracks[mfv::NJetsByUse];

    if (use_sv_to_jets) {
      for (int i = 0; i < mfv::NJetsByUse; ++i) {
        int njets = sv_to_jets[i]->numberOfAssociations(svref);
        aux.njets[i] = int2uchar(njets);
      
        if (njets > 0) {
          const edm::RefVector<pat::JetCollection>& jets = (*sv_to_jets[i])[svref];

          for (int ijet = 0; ijet < njets; ++ijet) {
            p4s[1+i] += jets[ijet]->p4();

            for (const reco::PFCandidatePtr& pfcand : jets[ijet]->getPFConstituents()) {
              const reco::TrackRef& tk = pfcand->trackRef();
              if (tk.isNonnull())
                jets_tracks[i].insert(tk);
            }

            if (primary_vertex)
              costhjetmomvtxdisps[i].push_back(costh3(jets[ijet]->p4(), pv2sv));
            else
              costhjetmomvtxdisps[i].push_back(-2);

            for (int jjet = ijet+1; jjet < njets; ++jjet) {
              jetpairdetas[i].push_back(fabs(jets[ijet]->eta() - jets[jjet]->eta()));
              jetpairdrs[i].push_back(reco::deltaR(*jets[ijet], *jets[jjet]));
            }
          }
        
          math::XYZTLorentzVector jpt_p4 = p4s[1+i];

          for (auto it = sv.tracks_begin(), ite = sv.tracks_end(); it != ite; ++it) {
            if (sv.trackWeight(*it) >= mfv::track_vertex_weight_min) {
              reco::TrackRef tk = it->castTo<reco::TrackRef>();
              if (!jets_tracks[i].count(tk))
                jpt_p4 += math::XYZTLorentzVector(tk->px(), tk->py(), tk->pz(), tk->p());
            }
          }

          p4s[1 + i + mfv::NJetsByUse] = jpt_p4;
        }
      }

      distrib_calculator jetpairdeta(jetpairdetas[mfv::JByNtracks], std::vector<double>());
      aux.jetpairdetamin(jetpairdeta.min);
      aux.jetpairdetamax(jetpairdeta.max);
      aux.jetpairdetaavg(jetpairdeta.avg);
      aux.jetpairdetarms(jetpairdeta.rms);

      distrib_calculator jetpairdr(jetpairdrs[mfv::JByNtracks], std::vector<double>());
      aux.jetpairdrmin(jetpairdr.min);
      aux.jetpairdrmax(jetpairdr.max);
      aux.jetpairdravg(jetpairdr.avg);
      aux.jetpairdrrms(jetpairdr.rms);

      if (aux.njets[mfv::JByNtracks] > 0) {
        distrib_calculator costhjetmomvtxdisp(costhjetmomvtxdisps[mfv::JByNtracks], std::vector<double>());
        aux.costhjetmomvtxdispmin(costhjetmomvtxdisp.min);
        aux.costhjetmomvtxdispmax(costhjetmomvtxdisp.max);
        aux.costhjetmomvtxdispavg(costhjetmomvtxdisp.avg);
        aux.costhjetmomvtxdisprms(costhjetmomvtxdisp.rms);
      }
      else {
        aux.costhjetmomvtxdispmin(-2);
        aux.costhjetmomvtxdispmax(-2);
        aux.costhjetmomvtxdispavg(-2);
        aux.costhjetmomvtxdisprms(-2);
      }
    }

    for (int i = 0; i < mfv::NMomenta; ++i) {
      aux.pt[i]   = p4s[i].pt();
      aux.eta[i]  = p4s[i].eta();
      aux.phi[i]  = p4s[i].phi();
      aux.mass[i] = p4s[i].mass();
    }

      
    //const double sv_r = mag(sv.position().x() - bsx, sv.position().y() - bsy);
    //const double sv_z = fabs(sv.position().z() - bsz);

    auto trkb = sv.tracks_begin();
    auto trke = sv.tracks_end();

    std::vector<double> costhtkmomvtxdisps;

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

      assert(muons->size() <= 128);
      assert(electrons->size() <= 128);
      for (size_t i = 0, ie = muons->size(); i < ie; ++i)
        if (muons->at(i).track() == trref)
          aux.which_lep.push_back(i);
      if (aux.which_lep.size() == 0) // if a muon matched, don't check for electrons
        for (size_t i = 0, ie = electrons->size(); i < ie; ++i)
          if (electrons->at(i).closestCtfTrackRef() == trref)
            aux.which_lep.push_back(i | (1<<7));

      costhtkmomvtxdisps.push_back(costh3(tri->momentum(), pv2sv));

      const uchar nhitsbehind = 0; //int2uchar(tracker_extents.numHitsBehind(tri->hitPattern(), sv_r, sv_z));

      const std::vector<std::pair<int, float> >& pv_for_track = tracks_in_pvs[trref];
      if (pv_for_track.size() > 1)
        throw cms::Exception("VertexAuxProducer") << "multiple PV for a track";

      aux.track_weight(-1, sv.trackWeight(tri));
      aux.track_q(-1, tri->charge());
      aux.track_hitpattern(-1,
                           tri->hitPattern().numberOfValidPixelHits(), 
                           tri->hitPattern().pixelLayersWithMeasurement(), 
                           tri->hitPattern().numberOfValidStripHits(),
                           tri->hitPattern().stripLayersWithMeasurement(), 
                           nhitsbehind,
                           tri->hitPattern().numberOfLostHits(reco::HitPattern::TRACK_HITS)); // JMTBAD could add missing inner, outer

      aux.track_injet.push_back(jets_tracks[0].count(trref)); // JMTBAD
      aux.track_inpv.push_back(pv_for_track.size() ? pv_for_track[0].first : -1);
      aux.track_dxy.push_back(fabs(tri->dxy(beamspot->position())));
      aux.track_dz.push_back(primary_vertex ? fabs(tri->dz(primary_vertex->position())) : 0); // JMTBAD not the previous behavior when no PV
      aux.track_vx.push_back(tri->vx());
      aux.track_vy.push_back(tri->vy());
      aux.track_vz.push_back(tri->vz());
      aux.track_px.push_back(tri->px());
      aux.track_py.push_back(tri->py());
      aux.track_pz.push_back(tri->pz());
      aux.track_chi2.push_back(tri->chi2());
      aux.track_ndof.push_back(tri->ndof());
      aux.track_cov.push_back(tri->covariance());
      aux.track_pt_err.push_back(tri->ptError());
      aux.track_eta.push_back(tri->eta());
      aux.track_phi.push_back(tri->phi());
    }

    const mfv::vertex_distances vtx_distances(sv, *gen_vertices, *beamspot, primary_vertex, p4s);

    distrib_calculator costhtkmomvtxdisp(costhtkmomvtxdisps, std::vector<double>());
    aux.costhtkmomvtxdispmin(costhtkmomvtxdisp.min);
    aux.costhtkmomvtxdispmax(costhtkmomvtxdisp.max);
    aux.costhtkmomvtxdispavg(costhtkmomvtxdisp.avg);
    aux.costhtkmomvtxdisprms(costhtkmomvtxdisp.rms);

    aux.gen2ddist       = vtx_distances.gen2ddist.value();
    aux.gen2derr        = vtx_distances.gen2ddist.error();
    aux.gen3ddist       = vtx_distances.gen3ddist.value();
    aux.gen3derr        = vtx_distances.gen3ddist.error();
    aux.bs2ddist        = vtx_distances.bs2ddist.value();
    aux.bs2derr         = vtx_distances.bs2ddist.error();
    aux.pv2ddist        = vtx_distances.pv2ddist_val;
    aux.pv2derr         = vtx_distances.pv2ddist_err;
    aux.pv3ddist        = vtx_distances.pv3ddist_val;
    aux.pv3derr         = vtx_distances.pv3ddist_err;

    for (int i = 0; i < mfv::NMomenta; ++i) {
      aux.costhmombs  (i, vtx_distances.costhmombs  [i]);
      aux.costhmompv2d(i, vtx_distances.costhmompv2d[i]);
      aux.costhmompv3d(i, vtx_distances.costhmompv3d[i]);

      aux.missdistpv   [i] = vtx_distances.missdistpv[i].value();
      aux.missdistpverr[i] = vtx_distances.missdistpv[i].error();
    }

  }

  sorter.sort(*auxes);

  event.put(auxes);
}

DEFINE_FWK_MODULE(MFVVertexAuxProducer);
