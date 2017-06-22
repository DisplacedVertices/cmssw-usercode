#include "TTree.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "JMTucker/Tools/interface/TrackingTree.h"
#include "JMTucker/Tools/interface/TrackerSpaceExtent.h"

class TrackingTreer : public edm::EDAnalyzer {
public:
  explicit TrackingTreer(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  const edm::EDGetTokenT<std::vector<PileupSummaryInfo>> pileup_token;
  const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
  const edm::EDGetTokenT<reco::VertexCollection> primary_vertices_token;
  const edm::EDGetTokenT<reco::TrackCollection> tracks_token;

  const bool assert_diag_cov;

  TTree* tree;
  TrackingTree nt;
};

TrackingTreer::TrackingTreer(const edm::ParameterSet& cfg)
  : pileup_token(consumes<std::vector<PileupSummaryInfo>>(edm::InputTag("addPileupInfo"))),
    beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot_src"))),
    primary_vertices_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("primary_vertices_src"))),
    tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("tracks_src"))),
    assert_diag_cov(cfg.getParameter<bool>("assert_diag_cov"))
{
  edm::Service<TFileService> fs;
  tree = fs->make<TTree>("t", "");
  nt.write_to_tree(tree);
}

void TrackingTreer::analyze(const edm::Event& event, const edm::EventSetup&) {
  nt.clear();
  nt.run = event.id().run();
  nt.lumi = event.luminosityBlock();
  nt.event = event.id().event();

  if (!event.isRealData()) {
    edm::Handle<std::vector<PileupSummaryInfo> > pileup;
    event.getByToken(pileup_token, pileup);

    for (std::vector<PileupSummaryInfo>::const_iterator psi = pileup->begin(), end = pileup->end(); psi != end; ++psi)
      if (psi->getBunchCrossing() == 0)
        nt.npu = psi->getTrueNumInteractions();
  }

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByToken(beamspot_token, beamspot);

  nt.bs_x = beamspot->x0();
  nt.bs_y = beamspot->y0();
  nt.bs_z = beamspot->z0();
  nt.bs_sigmaz = beamspot->sigmaZ();
  nt.bs_dxdz = beamspot->dxdz();
  nt.bs_dydz = beamspot->dydz();
  nt.bs_width = beamspot->BeamWidthX(); // set equal to Y

  nt.bs_err_x = beamspot->x0Error();
  nt.bs_err_y = beamspot->y0Error();
  nt.bs_err_z = beamspot->z0Error();
  nt.bs_err_sigmaz = beamspot->sigmaZ0Error();
  nt.bs_err_dxdz = beamspot->dxdzError();
  nt.bs_err_dydz = beamspot->dydzError();
  nt.bs_err_width = beamspot->BeamWidthXError();

  if (assert_diag_cov) {
    bool ok = true;
    for (int i = 0; i < 7; ++i)
      for (int j = i+1; j < 7; ++j)
        if (beamspot->covariance(i,j) > 1e-8)
          ok = false;
    if (!ok) {
      for (int i = 0; i < 7; ++i)
        for (int j = i+1; j < 7; ++j)
          std::cout << "beamspot cov(" << i << "," << j << ") = " << beamspot->covariance(i,j) << std::endl;
      throw cms::Exception("BadAssumption", "non-zero cov matrix");
    }
  }

  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByToken(primary_vertices_token, primary_vertices);
  const reco::Vertex* the_pv = primary_vertices->size() ? &(*primary_vertices)[0] : 0;

  for (const reco::Vertex& pv : *primary_vertices) {
    nt.pv_x.push_back(pv.x());
    nt.pv_y.push_back(pv.y());
    nt.pv_z.push_back(pv.z());

    float sumpt2 = 0;    
    for (auto it = pv.tracks_begin(); it != pv.tracks_end(); ++it)
      sumpt2 += (**it).pt() * (**it).pt();
    nt.pv_sumpt2.push_back(sumpt2);

    nt.pv_ntracks.push_back(pv.nTracks());
    nt.pv_chi2dof.push_back(pv.normalizedChi2());
    nt.pv_cxx.push_back(pv.covariance(0,0));
    nt.pv_cxy.push_back(pv.covariance(0,1));
    nt.pv_cxz.push_back(pv.covariance(0,2));
    nt.pv_cyy.push_back(pv.covariance(1,1));
    nt.pv_cyz.push_back(pv.covariance(1,2));
    nt.pv_czz.push_back(pv.covariance(2,2));
  }

  edm::Handle<reco::TrackCollection> tracks;
  event.getByToken(tracks_token, tracks);

  TrackerSpaceExtents tracker_extents;

  for (const reco::Track& tk : *tracks) {
    nt.tk_chi2dof.push_back(tk.normalizedChi2());
    nt.tk_qpt.push_back(tk.charge() * tk.pt());
    nt.tk_eta.push_back(tk.eta());
    nt.tk_phi.push_back(tk.phi());
    nt.tk_dxybs.push_back(tk.dxy(*beamspot));
    nt.tk_dzbs.push_back(tk.dz(beamspot->position()));
    if (the_pv) {
      nt.tk_dxypv.push_back(tk.dxy(the_pv->position()));
      nt.tk_dzpv.push_back(tk.dz(the_pv->position()));
    }
    else {
      nt.tk_dxypv.push_back(1e99);
      nt.tk_dzpv.push_back(1e99);
    }
    nt.tk_vx.push_back(tk.vx());
    nt.tk_vy.push_back(tk.vy());
    nt.tk_vz.push_back(tk.vz());
    nt.tk_err_qpt.push_back(tk.ptError());
    nt.tk_err_eta.push_back(tk.etaError());
    nt.tk_err_phi.push_back(tk.phiError());
    nt.tk_err_dxy.push_back(tk.dxyError());
    nt.tk_err_dz.push_back(tk.dzError());
    nt.tk_nsthit.push_back(tk.hitPattern().numberOfValidStripHits());
    nt.tk_npxhit.push_back(tk.hitPattern().numberOfValidPixelHits());
    nt.tk_nstlay.push_back(tk.hitPattern().stripLayersWithMeasurement());
    nt.tk_npxlay.push_back(tk.hitPattern().pixelLayersWithMeasurement());

    NumExtents ex    = tracker_extents.numExtentInRAndZ(tk.hitPattern(), false);
    NumExtents ex_px = tracker_extents.numExtentInRAndZ(tk.hitPattern(), true);
    nt.tk_minhit(ex.min_r < 2e9 ? ex.min_r : 0,
                 ex.min_z < 2e9 ? ex.min_z : 0);
    nt.tk_maxhit(ex.max_r > -2e9 ? ex.max_r : 0,
                 ex.max_z > -2e9 ? ex.max_z : 0);
    nt.tk_maxpxhit(ex_px.max_r > -2e9 ? ex_px.max_r : 0,
                   ex_px.max_z > -2e9 ? ex_px.max_z : 0);
  }

  tree->Fill();
}

DEFINE_FWK_MODULE(TrackingTreer);
