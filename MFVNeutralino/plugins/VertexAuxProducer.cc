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
#include "JMTucker/MFVNeutralino/interface/Event.h"
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
};

MFVVertexAuxProducer::MFVVertexAuxProducer(const edm::ParameterSet& cfg)
  : primary_vertex_src(cfg.getParameter<edm::InputTag>("primary_vertex_src")),
    gen_vertices_src(cfg.getParameter<edm::InputTag>("gen_vertices_src")),
    vertex_src(cfg.getParameter<edm::InputTag>("vertex_src")),
    sv_to_jets_src(cfg.getParameter<std::string>("sv_to_jets_src"))
{
  produces<MFVEvent>();
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
    
    if (use_sv_to_jets) {
      reco::Candidate::LorentzVector jets_p4[MFVJetVertexAssociation::NByUse];

      for (int i = 0; i < MFVJetVertexAssociation::NByUse; ++i) {
        int njets = sv_to_jets[i]->numberOfAssociations(svref);
        aux.njets[i] = int2uchar(njets);
      
        if (njets > 0) {
          const edm::RefVector<pat::JetCollection>& jets = (*sv_to_jets[i])[svref];
          for (int ijet = 0; ijet < njets; ++ijet)
            jets_p4[i] += jets[ijet]->p4();
        
          aux.jetspt  [i] = jets_p4[i].pt();
          aux.jetseta [i] = jets_p4[i].eta();
          aux.jetsphi [i] = jets_p4[i].phi();
          aux.jetsmass[i] = jets_p4[i].mass();
        }
      }
    }
    else {
      for (int i = 0; i < MFVJetVertexAssociation::NByUse; ++i) {
        aux.njets[i] = 0;
        aux.jetspt[i] = 0;
        aux.jetseta[i] = 0;
        aux.jetsphi[i] = 0;
        aux.jetsmass[i] = 0;
      }
    }
      
    const double sv_r = mag(sv.position().x() - bsx, sv.position().y() - bsy);
    const double sv_z = fabs(sv.position().z() - bsz);

    auto trkb = sv.tracks_begin();
    auto trke = sv.tracks_end();
    aux.ntracks = int2uchar(trke - trkb); // JMTBAD use ++ntracks in loop

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
      if (sv.trackWeight(tri) < mfv::track_vertex_weight_min)
        continue;

      const double pti = tri->pt();
      trackpts.push_back(pti);

      // inc_uchar(aux.ntracks); // JMTBAD

      if (pti > 3)  inc_uchar(aux.ntracksptgt3);
      if (pti > 5)  inc_uchar(aux.ntracksptgt5);
      if (pti > 10) inc_uchar(aux.ntracksptgt10);

      aux.sumpt2 += pti*pti;

      if (trackicity.count(tri.key()) > 0)
        throw cms::Exception("VertexAuxProducer") << "trackicity > 1";
      else
        trackicity.insert(tri.key());

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
    
    std::sort(trackpts.begin(), trackpts.end());
    aux.mintrackpt = trackpts[0];
    aux.maxtrackpt = trackpts[trackpts.size()-1];
    aux.maxm1trackpt = trackpts[trackpts.size()-2];
    aux.maxm2trackpt = trackpts.size() > 2 ? trackpts[trackpts.size()-3] : -1;

    const mfv::vertex_tracks_distance vtx_tks_dist(sv);
    const mfv::vertex_distances vtx_distances(sv, *gen_vertices, *beamspot, primary_vertex);

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

    aux.costhmombs  [0] = vtx_distances.costhmombs; // JMTBAD other costhmoms
    aux.costhmompv2d[0] = vtx_distances.costhmompv2d;
    aux.costhmompv3d[0] = vtx_distances.costhmompv3d;

    // JMTBAD miss distances
  }

  event.put(auxes);
}

DEFINE_FWK_MODULE(MFVVertexAuxProducer);
