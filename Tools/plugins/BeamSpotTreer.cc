#include "TTree.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

class BeamSpotTreer : public edm::EDAnalyzer {
public:
  explicit BeamSpotTreer(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  const edm::InputTag beamspot_src;
  const edm::InputTag primary_vertex_src;

  struct tree_t {
    unsigned run;
    unsigned lumi;
    unsigned event;

    float bs_x;
    float bs_y;
    float bs_z;
    float bs_sigmaz;
    float bs_dxdz;
    float bs_dydz;
    float bs_width;

    float bs_err_x;
    float bs_err_y;
    float bs_err_z;
    float bs_err_sigmaz;
    float bs_err_dxdz;
    float bs_err_dydz;
    float bs_err_width;

    std::vector<float> pv_x;
    std::vector<float> pv_y;
    std::vector<float> pv_z;
    std::vector<float> pv_sumpt2;
    std::vector<float> pv_ntracks;
    std::vector<float> pv_chi2;
    std::vector<float> pv_ndof;
    std::vector<float> pv_cxx;
    std::vector<float> pv_cxy;
    std::vector<float> pv_cxz;
    std::vector<float> pv_cyy;
    std::vector<float> pv_cyz;
    std::vector<float> pv_czz;

    tree_t() { clear(); }

    void clear() {
      run = lumi = event = 0;
      bs_x = bs_y = bs_z = bs_sigmaz = bs_dxdz = bs_dydz = bs_width = 0;
      bs_err_x = bs_err_y = bs_err_z = bs_err_sigmaz = bs_err_dxdz = bs_err_dydz = bs_err_width = 0;

      pv_x.clear();
      pv_y.clear();
      pv_z.clear();
      pv_sumpt2.clear();
      pv_ntracks.clear();
      pv_chi2.clear();
      pv_ndof.clear();
      pv_cxx.clear();
      pv_cxy.clear();
      pv_cxz.clear();
      pv_cyy.clear();
      pv_cyz.clear();
      pv_czz.clear();
    }
  };

  TTree* tree;
  tree_t nt;
};

BeamSpotTreer::BeamSpotTreer(const edm::ParameterSet& cfg)
  : beamspot_src(cfg.getParameter<edm::InputTag>("beamspot_src")),
    primary_vertex_src(cfg.getParameter<edm::InputTag>("primary_vertex_src"))
{
  edm::Service<TFileService> fs;
  tree = fs->make<TTree>("t", "");
  tree->Branch("run", &nt.run, "run/i");
  tree->Branch("lumi", &nt.lumi, "lumi/i");
  tree->Branch("event", &nt.event, "event/i");
  tree->Branch("bs_x", &nt.bs_x, "bs_x/F");
  tree->Branch("bs_y", &nt.bs_y, "bs_y/F");
  tree->Branch("bs_z", &nt.bs_z, "bs_z/F");
  tree->Branch("bs_sigmaz", &nt.bs_sigmaz, "bs_sigmaz/F");
  tree->Branch("bs_dxdz", &nt.bs_dxdz, "bs_dxdz/F");
  tree->Branch("bs_dydz", &nt.bs_dydz, "bs_dydz/F");
  tree->Branch("bs_width", &nt.bs_width, "bs_width/F");
  tree->Branch("bs_err_x", &nt.bs_err_x, "bs_err_x/F");
  tree->Branch("bs_err_y", &nt.bs_err_y, "bs_err_y/F");
  tree->Branch("bs_err_z", &nt.bs_err_z, "bs_err_z/F");
  tree->Branch("bs_err_sigmaz", &nt.bs_err_sigmaz, "bs_err_sigmaz/F");
  tree->Branch("bs_err_dxdz", &nt.bs_err_dxdz, "bs_err_dxdz/F");
  tree->Branch("bs_err_dydz", &nt.bs_err_dydz, "bs_err_dydz/F");
  tree->Branch("bs_err_width", &nt.bs_err_width, "bs_err_width/F");
  tree->Branch("pv_x", &nt.pv_x);
  tree->Branch("pv_y", &nt.pv_y);
  tree->Branch("pv_z", &nt.pv_z);
  tree->Branch("pv_sumpt2", &nt.pv_sumpt2);
  tree->Branch("pv_ntracks", &nt.pv_ntracks);
  tree->Branch("pv_chi2", &nt.pv_chi2);
  tree->Branch("pv_ndof", &nt.pv_ndof);
  tree->Branch("pv_cxx", &nt.pv_cxx);
  tree->Branch("pv_cxy", &nt.pv_cxy);
  tree->Branch("pv_cxz", &nt.pv_cxz);
  tree->Branch("pv_cyy", &nt.pv_cyy);
  tree->Branch("pv_cyz", &nt.pv_cyz);
  tree->Branch("pv_czz", &nt.pv_czz);
}

void BeamSpotTreer::analyze(const edm::Event& event, const edm::EventSetup&) {
  nt.clear();
  nt.run = event.id().run();
  nt.lumi = event.luminosityBlock();
  nt.event = event.id().event();

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByLabel(beamspot_src, beamspot);

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

  for (int i = 0; i < 7; ++i)
    for (int j = i+1; j < 7; ++j)
      assert(beamspot->covariance(i,j) == 0);

  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByLabel(primary_vertex_src, primary_vertices);

  for (const reco::Vertex& pv : *primary_vertices) {
    nt.pv_x.push_back(pv.x());
    nt.pv_y.push_back(pv.y());
    nt.pv_z.push_back(pv.z());

    float sumpt2 = 0;    
    for (auto it = pv.tracks_begin(); it != pv.tracks_end(); ++it)
      sumpt2 += (**it).pt() * (**it).pt();
    nt.pv_sumpt2.push_back(sumpt2);

    nt.pv_ntracks.push_back(pv.nTracks());
    nt.pv_chi2.push_back(pv.chi2());
    nt.pv_ndof.push_back(pv.ndof());
    nt.pv_cxx.push_back(pv.covariance(0,0));
    nt.pv_cxy.push_back(pv.covariance(0,1));
    nt.pv_cxz.push_back(pv.covariance(0,2));
    nt.pv_cyy.push_back(pv.covariance(1,1));
    nt.pv_cyz.push_back(pv.covariance(1,2));
    nt.pv_czz.push_back(pv.covariance(2,2));
  }

  tree->Fill();
}

DEFINE_FWK_MODULE(BeamSpotTreer);
