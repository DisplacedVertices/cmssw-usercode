#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "JMTucker/MFVNeutralino/interface/TrackerSpaceExtent.h"
#include "JMTucker/MFVNeutralino/interface/VertexAux.h"
#include "JMTucker/MFVNeutralino/interface/VertexTools.h"
#include "JMTucker/Tools/interface/Utilities.h"

class MFVVertexAuxProducer : public edm::EDProducer {
 public:
  explicit MFVVertexAuxProducer(const edm::ParameterSet&);
  void produce(edm::Event&, const edm::EventSetup&);

 private:
  const edm::InputTag primary_vertex_src;
  const edm::InputTag gen_vertices_src;
  const edm::InputTag vertex_src;
  const std::string sv_to_jets_src;
  const MFVVertexAuxSorter sorter;
};

MFVVertexAuxProducer::MFVVertexAuxProducer(const edm::ParameterSet& cfg)
  : primary_vertex_src(cfg.getParameter<edm::InputTag>("primary_vertex_src")),
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
  const GlobalPoint origin(bsx, bsy, bsz);
  const reco::Vertex fake_bs_vtx(beamspot->position(), beamspot->covariance3D());

  //////////////////////////////////////////////////////////////////////

  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByLabel(primary_vertex_src, primary_vertices);
  const reco::Vertex* primary_vertex = 0;
  if (primary_vertices->size())
    primary_vertex = &primary_vertices->at(0);

  //////////////////////////////////////////////////////////////////////

  TrackerSpaceExtents tracker_extents;
  tracker_extents.fill(setup, origin);
  
  //////////////////////////////////////////////////////////////////////

  edm::Handle<std::vector<double> > gen_vertices;
  event.getByLabel(gen_vertices_src, gen_vertices);

  //////////////////////////////////////////////////////////////////////

  edm::Handle<reco::VertexCollection> secondary_vertices;
  event.getByLabel(vertex_src, secondary_vertices);
  const int nsv = int(secondary_vertices->size());

  const bool use_sv_to_jets = sv_to_jets_src != "dummy";
  edm::Handle<MFVJetVertexAssociation::type> sv_to_jets[MFVJetVertexAssociation::NByUse];
  if (use_sv_to_jets)
    for (int i = 0; i < MFVJetVertexAssociation::NByUse; ++i)
      event.getByLabel(edm::InputTag(sv_to_jets_src, MFVJetVertexAssociation::names[i]), sv_to_jets[i]);

  //////////////////////////////////////////////////////////////////////

  std::auto_ptr<std::vector<MFVVertexAux> > auxes(new std::vector<MFVVertexAux>(nsv));
  std::set<int> trackicity;

  for (int isv = 0; isv < nsv; ++isv) {
    const reco::Vertex& sv = secondary_vertices->at(isv);
    const reco::VertexRef svref(secondary_vertices, isv);
    MFVVertexAux& aux = auxes->at(isv);
    aux.ref = svref;
    aux.selected = false; // to be finalized in VertexSelector

    aux.x = sv.x();
    aux.y = sv.y();
    aux.z = sv.z();

    aux.chi2 = sv.chi2();
    aux.ndof = sv.ndof();


    std::vector<math::XYZTLorentzVector> p4s(mfv::NMomenta);
    p4s[mfv::PTracksOnly] = sv.p4();

    for (int i = 0; i < MFVJetVertexAssociation::NByUse; ++i)
      aux.njets[i] = 0;

    if (use_sv_to_jets) {
      for (int i = 0; i < MFVJetVertexAssociation::NByUse; ++i) {
        int njets = sv_to_jets[i]->numberOfAssociations(svref);
        aux.njets[i] = int2uchar(njets);
      
        if (njets > 0) {
          const edm::RefVector<pat::JetCollection>& jets = (*sv_to_jets[i])[svref];
          std::set<reco::TrackRef> jets_tracks;

          for (int ijet = 0; ijet < njets; ++ijet) {
            p4s[1+i] += jets[ijet]->p4();

            for (const reco::PFCandidatePtr& pfcand : jets[ijet]->getPFConstituents()) {
              const reco::TrackRef& tk = pfcand->trackRef();
              if (tk.isNonnull())
                jets_tracks.insert(tk);
            }
          }
        
          math::XYZTLorentzVector jpt_p4 = p4s[1+i];

          for (auto it = sv.tracks_begin(), ite = sv.tracks_end(); it != ite; ++it) {
            if (sv.trackWeight(*it) >= mfv::track_vertex_weight_min) {
              reco::TrackRef tk = it->castTo<reco::TrackRef>();
              if (!jets_tracks.count(tk))
                jpt_p4 += math::XYZTLorentzVector(tk->px(), tk->py(), tk->pz(), tk->p());
            }
          }

          p4s[1 + i + MFVJetVertexAssociation::NByUse] = jpt_p4;
        }
      }
    }

    for (int i = 0; i < mfv::NMomenta; ++i) {
      aux.pt[i]   = p4s[i].pt();
      aux.eta[i]  = p4s[i].eta();
      aux.phi[i]  = p4s[i].phi();
      aux.mass[i] = p4s[i].mass();
    }

      
    const double sv_r = mag(sv.position().x() - bsx, sv.position().y() - bsy);
    const double sv_z = fabs(sv.position().z() - bsz);

    auto trkb = sv.tracks_begin();
    auto trke = sv.tracks_end();

    aux.ntracks = 0;
    aux.nbadtracks = 0;
    aux.ntracksptgt3 = 0;
    aux.ntracksptgt5 = 0;
    aux.ntracksptgt10 = 0;
    aux.trackminnhits = 255;
    aux.trackmaxnhits = 0;
    aux.sumpt2 = 0;
    std::vector<double> trackpts;
    aux.maxnhitsbehind = 0;
    aux.sumnhitsbehind = 0;

    for (auto trki = trkb; trki != trke; ++trki) {
      const reco::TrackBaseRef& tri = *trki;

      if (trackicity.count(tri.key()) > 0)
        throw cms::Exception("VertexAuxProducer") << "trackicity > 1";
      else
        trackicity.insert(tri.key());

      if (sv.trackWeight(tri) < mfv::track_vertex_weight_min)
        continue;

      inc_uchar(aux.ntracks);

      if (tri->ptError() / tri->pt() > 0.5) {
        inc_uchar(aux.nbadtracks);
        continue;
      }

      const double pti = tri->pt();
      trackpts.push_back(pti);

      if (pti > 3)  inc_uchar(aux.ntracksptgt3);
      if (pti > 5)  inc_uchar(aux.ntracksptgt5);
      if (pti > 10) inc_uchar(aux.ntracksptgt10);

      aux.sumpt2 += pti*pti;

      const uchar nhits = int2uchar(tri->numberOfValidHits());
      if (nhits < aux.trackminnhits)
        aux.trackminnhits = nhits;
      if (nhits > aux.trackmaxnhits)
        aux.trackmaxnhits = nhits;

      const uchar nhitsbehind = int2uchar(tracker_extents.numHitsBehind(tri->hitPattern(), sv_r, sv_z));
      if (nhitsbehind > aux.maxnhitsbehind)
        aux.maxnhitsbehind = nhitsbehind;
      if (int(aux.sumnhitsbehind) + int(nhitsbehind) > 255)
        aux.sumnhitsbehind = 255;
      else
        aux.sumnhitsbehind += nhitsbehind;
    }

    if (trackpts.size()) {
      std::sort(trackpts.begin(), trackpts.end());
      aux.mintrackpt = trackpts[0];
      aux.maxtrackpt = trackpts[trackpts.size()-1];
      aux.maxm1trackpt = trackpts[trackpts.size()-2];
      aux.maxm2trackpt = trackpts.size() > 2 ? trackpts[trackpts.size()-3] : -1;
    }
    else
      aux.mintrackpt = aux.maxtrackpt = aux.maxm1trackpt = aux.maxm2trackpt = -1;
      
    const mfv::vertex_tracks_distance vtx_tks_dist(sv);
    const mfv::vertex_distances vtx_distances(sv, *gen_vertices, *beamspot, primary_vertex, p4s);

    aux.drmin  = vtx_tks_dist.drmin;
    aux.drmax  = vtx_tks_dist.drmax;
    aux.dravg  = vtx_tks_dist.dravg;
    aux.drrms  = vtx_tks_dist.drrms;
    aux.dravgw = vtx_tks_dist.dravgw;
    aux.drrmsw = vtx_tks_dist.drrmsw;
    
    aux.gen2ddist       = vtx_distances.gen2ddist.value();
    aux.gen2derr        = vtx_distances.gen2ddist.error();
    aux.gen3ddist       = vtx_distances.gen3ddist.value();
    aux.gen3derr        = vtx_distances.gen3ddist.error();
    aux.bs2dcompatscss  = vtx_distances.bs2dcompat.first;
    aux.bs2dcompat      = vtx_distances.bs2dcompat.second;
    aux.bs2ddist        = vtx_distances.bs2ddist.value();
    aux.bs2derr         = vtx_distances.bs2ddist.error();
    aux.bs3ddist        = vtx_distances.bs3ddist;
    aux.pv2dcompatscss  = vtx_distances.pv2dcompat.first;
    aux.pv2dcompat      = vtx_distances.pv2dcompat.second;
    aux.pv2ddist        = vtx_distances.pv2ddist_val;
    aux.pv2derr         = vtx_distances.pv2ddist_err;
    aux.pv3dcompatscss  = vtx_distances.pv3dcompat.first;
    aux.pv3dcompat      = vtx_distances.pv3dcompat.second;
    aux.pv3ddist        = vtx_distances.pv3ddist_val;
    aux.pv3derr         = vtx_distances.pv3ddist_err;

    for (int i = 0; i < mfv::NMomenta; ++i) {
      aux.costhmombs  [i] = vtx_distances.costhmombs[i];
      aux.costhmompv2d[i] = vtx_distances.costhmompv2d[i];
      aux.costhmompv3d[i] = vtx_distances.costhmompv3d[i];

      aux.missdistpv   [i] = vtx_distances.missdistpv[i].value();
      aux.missdistpverr[i] = vtx_distances.missdistpv[i].error();
    }

  }

  sorter.sort(*auxes);

  event.put(auxes);
}

DEFINE_FWK_MODULE(MFVVertexAuxProducer);
