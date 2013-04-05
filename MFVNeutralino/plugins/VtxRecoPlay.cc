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
  TH1F* h_njets;
  TH2F* h_gen_vtx;
  TH1F* h_nrecvtx;
  TH2F* h_rec_vtx;
  TH1F* h_recvtxchi2;
  TH1F* h_recvtxchi2prob;
  TH1F* h_dist;
  TH1F* h_dist2d;
  TH1F* h_pairvtxsuccess;
  TH1F* h_pairvtxchi2;
  TH1F* h_pairvtxchi2prob;
  TH2F* h_pairvtx;
  TH1F* h_pairvtxdist2d;
  TH1F* h_pairvtxdist;
};

VtxRecoPlay::VtxRecoPlay(const edm::ParameterSet& cfg)
  : primary_vertex_src(cfg.getParameter<edm::InputTag>("primary_vertex_src")),
    gen_src(cfg.getParameter<edm::InputTag>("gen_src")),
    vertex_src(cfg.getParameter<edm::InputTag>("vertex_src")),
    print_info(cfg.getParameter<bool>("print_info")),
    is_mfv(cfg.getParameter<bool>("is_mfv"))
{
  edm::Service<TFileService> fs;
  
  h_njets = fs->make<TH1F>("h_njets", "", 50, 0, 50);
  h_gen_vtx = fs->make<TH2F>("h_gen_vtx", "", 500, -1, 1, 500, -1, 1);
  h_nrecvtx = fs->make<TH1F>("h_nrecvtx", "", 100, 0, 100);
  h_rec_vtx = fs->make<TH2F>("h_rec_vtx", "", 500, -1, 1, 500, -1, 1);
  h_recvtxchi2 = fs->make<TH1F>("h_recvtxchi2", "", 50,0,50);
  h_recvtxchi2prob = fs->make<TH1F>("h_recvtxchi2prob", "", 50,0,1);
  h_dist2d = fs->make<TH1F>("h_dist2d", "", 1000, 0, 5);
  h_dist = fs->make<TH1F>("h_dist", "", 1000, 0, 5);
  h_pairvtxsuccess = fs->make<TH1F>("h_pairvtxsuccess", "", 2,0,2);
  h_pairvtxchi2 = fs->make<TH1F>("h_pairvtxchi2", "", 50,0,50);
  h_pairvtxchi2prob = fs->make<TH1F>("h_pairvtxchi2prob", "", 50,0,1);
  h_pairvtx = fs->make<TH2F>("h_pairvtx", "", 500, -1, 1, 500, -1, 1);
  h_pairvtxdist2d = fs->make<TH1F>("h_pairvtxdist2d", "", 1000, 0, 5);
  h_pairvtxdist = fs->make<TH1F>("h_pairvtxdist", "", 1000, 0, 5);
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
  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByLabel(primary_vertex_src, primary_vertices);
  
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
  if (njets < 6)
    return;

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
	h_gen_vtx->Fill(daughter->vx(), daughter->vy());
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
	h_gen_vtx->Fill(daughter->vx(), daughter->vy());
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
    h_rec_vtx->Fill(vtx.x(), vtx.y());
    h_recvtxchi2->Fill(vtx.normalizedChi2());
    h_recvtxchi2prob->Fill(TMath::Prob(vtx.chi2(), vtx.ndof()));
    for (int i = 0; i < 2; ++i) {
      h_dist2d->Fill(mag(vtx.x() - gen_verts[i][0], vtx.y() - gen_verts[i][1]));
      h_dist  ->Fill(mag(vtx.x() - gen_verts[i][0], vtx.y() - gen_verts[i][1], vtx.z() - gen_verts[i][2]));
    }
  }

  edm::ESHandle<TransientTrackBuilder> trackBuilder;
  setup.get<TransientTrackRecord>().get("TransientTrackBuilder", trackBuilder);

  edm::Handle<reco::TrackCollection> tracks;
  event.getByLabel("generalTracks", tracks);

  for (int ivtx = 0; ivtx < nvtx; ++ivtx) {
    const reco::Vertex& vtxi = rec_vertices->at(ivtx);

    std::vector<reco::TransientTrack> ttvi;
    for (reco::Vertex::trackRef_iterator it = vtxi.tracks_begin(), ite = vtxi.tracks_end(); it != ite; ++it)
      ttvi.push_back(trackBuilder->build(**it));

    for (int jvtx = ivtx+1; jvtx < nvtx; ++jvtx) {
      const reco::Vertex& vtxj = rec_vertices->at(jvtx);
      
      std::vector<reco::TransientTrack> ttvj(ttvi);
      for (reco::Vertex::trackRef_iterator it = vtxj.tracks_begin(), ite = vtxj.tracks_end(); it != ite; ++it)
	ttvj.push_back(trackBuilder->build(**it));

      KalmanVertexFitter kvf(true);
      CachingVertex<5> cv = kvf.vertex(ttvj);
      TransientVertex tv = cv;
      reco::Vertex vtx = tv;
      
      h_pairvtxsuccess->Fill(tv.isValid());
      if (tv.isValid()) {
	h_pairvtxchi2->Fill(vtx.normalizedChi2());
	h_pairvtxchi2prob->Fill(TMath::Prob(vtx.chi2(), vtx.ndof()));
	h_pairvtx->Fill(vtx.x(), vtx.y());
	for (int igen = 0; igen < 2; ++igen) {
	  h_pairvtxdist2d->Fill(mag(vtx.x() - gen_verts[igen][0], vtx.y() - gen_verts[igen][1]));
	  h_pairvtxdist  ->Fill(mag(vtx.x() - gen_verts[igen][0], vtx.y() - gen_verts[igen][1], vtx.z() - gen_verts[igen][2]));
	}
      }
    }
  }

}

DEFINE_FWK_MODULE(VtxRecoPlay);
