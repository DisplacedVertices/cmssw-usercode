#include "TH1F.h"
#include "TH2F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "RecoVertex/VertexPrimitives/interface/CachingVertex.h"
#include "RecoVertex/VertexPrimitives/interface/TransientVertex.h"
#include "RecoVertex/VertexTools/interface/VertexDistanceXY.h"
#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "JMTucker/MFVNeutralino/interface/MCInteractionMFV3j.h"
#include "JMTucker/Tools/interface/MCInteractionTops.h"
#include "JMTucker/Tools/interface/Utilities.h"

class VtxRecoPlay : public edm::EDAnalyzer {
 public:
  explicit VtxRecoPlay(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::InputTag primary_vertex_src;
  const edm::InputTag gen_src;
  const edm::InputTag vertex_src;
  const bool print_info;
  const bool is_mfv;
  const int min_njets;
  TH1F* h_njets;
  TH2F* h_gen_vtx;
  TH1F* h_nrecvtx;
  TH2F* h_rec_vtx;
  TH1F* h_recvtxchi2;
  TH1F* h_recvtxchi2prob;
  TH1F* h_dist2d;
  TH1F* h_dist2dfull;
  TH1F* h_dist3d;
  TH1F* h_gendist2d;
  TH1F* h_gendist3d;
  TH1F* h_paircompat2d;
  TH1F* h_paircompat3d;
  TH1F* h_pairdistcompat2dfail;
  TH1F* h_pairdistcompat3dfail;
  TH1F* h_pairerrcompat2dfail;
  TH1F* h_pairerrcompat3dfail;
  TH1F* h_pairdist2d;
  TH1F* h_pairdist3d;
  TH1F* h_pairerr2d;
  TH1F* h_pairerr3d;
  TH1F* h_pairsig2d;
  TH1F* h_pairsig3d;
};

VtxRecoPlay::VtxRecoPlay(const edm::ParameterSet& cfg)
  : primary_vertex_src(cfg.getParameter<edm::InputTag>("primary_vertex_src")),
    gen_src(cfg.getParameter<edm::InputTag>("gen_src")),
    vertex_src(cfg.getParameter<edm::InputTag>("vertex_src")),
    print_info(cfg.getParameter<bool>("print_info")),
    is_mfv(cfg.getParameter<bool>("is_mfv")),
    min_njets(cfg.getParameter<int>("min_njets"))
{
  edm::Service<TFileService> fs;
  
  h_njets                  = fs->make<TH1F>("h_njets",                  "",      50,    0,   50);
  h_gen_vtx                = fs->make<TH2F>("h_gen_vtx",                "",     500,   -1,    1,    500,  -1,   1);
  h_nrecvtx                = fs->make<TH1F>("h_nrecvtx",                "",     100,    0,  100);
  h_rec_vtx                = fs->make<TH2F>("h_rec_vtx",                "",     500,   -1,    1,    500,  -1,   1);
  h_recvtxchi2             = fs->make<TH1F>("h_recvtxchi2",             "",      50,    0,   50);
  h_recvtxchi2prob         = fs->make<TH1F>("h_recvtxchi2prob",         "",      50,    0,    1);
  h_dist2d                 = fs->make<TH1F>("h_dist2d",                 "",    1000,    0,    5);
  h_dist2dfull             = fs->make<TH1F>("h_dist2dfull",             "",    1000,    0,    5);
  h_dist3d                 = fs->make<TH1F>("h_dist3d",                 "",    1000,    0,    5);
  h_gendist2d              = fs->make<TH1F>("h_gendist2d",              "",    1000,    0,    5);
  h_gendist3d              = fs->make<TH1F>("h_gendist3d",              "",    1000,    0,    5);
  h_paircompat2d           = fs->make<TH1F>("h_paircompat2d",           "",    1000,    0,    5);
  h_paircompat3d           = fs->make<TH1F>("h_paircompat3d",           "",    1000,    0,    5);
  h_pairdistcompat2dfail   = fs->make<TH1F>("h_pairdistcompat2dfail",   "",    1000,    0,    5);
  h_pairdistcompat3dfail   = fs->make<TH1F>("h_pairdistcompat3dfail",   "",    1000,    0,    5);
  h_pairerrcompat2dfail    = fs->make<TH1F>("h_pairerrcompat2dfail",    "",    1000,    0,    5);
  h_pairerrcompat3dfail    = fs->make<TH1F>("h_pairerrcompat3dfail",    "",    1000,    0,    5);
  h_pairdist2d             = fs->make<TH1F>("h_pairdist2d",             "",    1000,    0,    5);
  h_pairdist3d             = fs->make<TH1F>("h_pairdist3d",             "",    1000,    0,    5);
  h_pairerr2d              = fs->make<TH1F>("h_pairerr2d",              "",    1000,    0,    5);
  h_pairerr3d              = fs->make<TH1F>("h_pairerr3d",              "",    1000,    0,    5);
  h_pairsig2d              = fs->make<TH1F>("h_pairsig2d",              "",    1000,    0,    5);
  h_pairsig3d              = fs->make<TH1F>("h_pairsig3d",              "",    1000,    0,    5);
}

namespace {
  float mag(float x, float y) {
    return sqrt(x*x + y*y);
  }
  
  float mag(float x, float y, float z) {
    return sqrt(x*x + y*y + z*z);
  }
}

void VtxRecoPlay::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  if (min_njets > 0) {
    edm::Handle<reco::PFJetCollection> jets;
    event.getByLabel("ak5PFJets", jets);

    int njets = 0;
    for (const reco::PFJet& jet : *jets) {
      if (jet.pt() > 20 && 
	  fabs(jet.eta()) < 2.5 && 
	  jet.numberOfDaughters() > 1 &&
	  jet.neutralHadronEnergyFraction() < 0.99 && 
	  jet.neutralEmEnergyFraction() < 0.99 && 
	  (fabs(jet.eta()) >= 2.4 || (jet.chargedEmEnergyFraction() < 0.99 && jet.chargedHadronEnergyFraction() > 0. && jet.chargedMultiplicity() > 0)))
	njets += 1;
    }
    h_njets->Fill(njets);
    if (njets < min_njets)
      return;
  }

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByLabel("offlineBeamSpot", beamspot);

  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByLabel(primary_vertex_src, primary_vertices);

  edm::Handle<reco::GenParticleCollection> gen_particles;
  event.getByLabel(gen_src, gen_particles);
  
  float gen_verts[2][3] = {{0}};
  bool mci_valid = false;

  if (is_mfv) {
    MCInteractionMFV3j mci;
    mci.Init(*gen_particles);
    if ((mci_valid = mci.Valid())) {
      if (print_info)
	mci.Print(std::cout);
      for (int i = 0; i < 2; ++i) {
	const reco::GenParticle* daughter = mci.stranges[i];
	h_gen_vtx->Fill(daughter->vx() - beamspot->x0(), daughter->vy() - beamspot->y0());
	gen_verts[i][0] = daughter->vx();
	gen_verts[i][1] = daughter->vy();
	gen_verts[i][2] = daughter->vz();
      }
    }
  }
  else {
    MCInteractionTops mci;
    mci.Init(*gen_particles);
    if ((mci_valid = mci.Valid())) {
      for (int i = 0; i < 2; ++i) {
	const reco::GenParticle* daughter = mci.tops[i];
	h_gen_vtx->Fill(daughter->vx() - beamspot->x0(), daughter->vy() - beamspot->y0());
	gen_verts[i][0] = daughter->vx();
	gen_verts[i][1] = daughter->vy();
	gen_verts[i][2] = daughter->vz();
      }
    }
  }

  if (!mci_valid)
    edm::LogWarning("VtxRecoPlay") << "warning: neither MCI valid";

  edm::Handle<reco::VertexCollection> rec_vertices;
  event.getByLabel(vertex_src, rec_vertices);

  const int nvtx = rec_vertices->size();
  h_nrecvtx->Fill(nvtx);
  for (const reco::Vertex& vtx : *rec_vertices) {
    h_rec_vtx->Fill(vtx.x() - beamspot->x0(), vtx.y() - beamspot->y0());
    h_recvtxchi2->Fill(vtx.normalizedChi2());
    h_recvtxchi2prob->Fill(TMath::Prob(vtx.chi2(), vtx.ndof()));
    float closest2d = 1e99;
    float closest3d = 1e99;
    for (int i = 0; i < 2; ++i) {
      float dist2d = mag(vtx.x() - gen_verts[i][0], vtx.y() - gen_verts[i][1]);
      float dist3d = mag(vtx.x() - gen_verts[i][0], vtx.y() - gen_verts[i][1], vtx.z() - gen_verts[i][2]);
      if (dist2d < closest2d) closest2d = dist2d;
      if (dist3d < closest3d) closest3d = dist3d;
    }
    assert(closest2d < 1e99); // obviously
    assert(closest3d < 1e99);
    h_gendist2d->Fill(closest2d);
    h_gendist3d->Fill(closest3d);

    h_dist2d    ->Fill(mag(vtx.x() - beamspot->x(vtx.z()), vtx.y() - beamspot->y(vtx.z())));
    h_dist2dfull->Fill(mag(vtx.x() - beamspot->x0(),       vtx.y() - beamspot->y0()));
  }

  VertexDistance3D distcalc_3d;
  VertexDistanceXY distcalc_2d;
  for (int ivtx = 0; ivtx < nvtx - 1; ++ivtx) {
    const reco::Vertex& vtx_i = rec_vertices->at(ivtx);
    for (int jvtx = ivtx + 1; jvtx < nvtx; ++jvtx) {
      const reco::Vertex& vtx_j = rec_vertices->at(jvtx);

      Measurement1D dist_2d = distcalc_2d.distance(vtx_i, vtx_j);
      Measurement1D dist_3d = distcalc_3d.distance(vtx_i, vtx_j);

      h_pairdist2d->Fill(dist_2d.value());
      h_pairerr2d ->Fill(dist_2d.error());
      h_pairsig2d ->Fill(dist_2d.significance());

      h_pairdist3d->Fill(dist_3d.value());
      h_pairerr3d ->Fill(dist_3d.error());
      h_pairsig3d ->Fill(dist_3d.significance());

      try {
	h_paircompat2d->Fill(distcalc_2d.compatibility(vtx_i, vtx_j));
      }
      catch (cms::Exception& e) {
	if (e.category() != "VertexDistanceXY::matrix inversion problem")
	  throw;
	h_pairdistcompat2dfail->Fill(dist_2d.value());
	h_pairerrcompat2dfail ->Fill(dist_2d.error());
      }
      try {
	h_paircompat3d->Fill(distcalc_3d.compatibility(vtx_i, vtx_j));
      }
      catch (cms::Exception& e) {
	if (e.category() != "VertexDistance3D::matrix inversion problem")
	  throw;
	h_pairdistcompat3dfail->Fill(dist_3d.value());
	h_pairerrcompat3dfail ->Fill(dist_3d.error());
      }
    }
  }
}

DEFINE_FWK_MODULE(VtxRecoPlay);
