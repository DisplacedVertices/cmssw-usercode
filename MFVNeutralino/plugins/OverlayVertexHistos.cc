#include "TH2F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

class MFVOverlayVertexHistos : public edm::EDAnalyzer {
 public:
  explicit MFVOverlayVertexHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::EDGetTokenT<std::vector<double>> truth_token;
  const edm::EDGetTokenT<reco::VertexCollection> vertices_token;

  const int min_ntracks;

  TH1F* h_dvv_true;
  TH1F* h_dvv_pass_anytwo;
  TH1F* h_dvv_pass_twominntk;
  TH1F* h_dvv_pass_foundv0;
  TH1F* h_dvv_pass_foundv0samentk;
  TH1F* h_dvv_pass_foundv0andv1;
  TH1F* h_dvv_pass_foundv0andv1samentk;
};

MFVOverlayVertexHistos::MFVOverlayVertexHistos(const edm::ParameterSet& cfg)
  : truth_token(consumes<std::vector<double>>(cfg.getParameter<edm::InputTag>("truth_src"))),
    vertices_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("vertices_src"))),
    min_ntracks(cfg.getParameter<int>("min_ntracks"))
{
  edm::Service<TFileService> fs;

  h_dvv_true                     = fs->make<TH1F>("h_dvv_true",                     "", 100, 0, 0.1);
  h_dvv_pass_anytwo              = fs->make<TH1F>("h_dvv_pass_anytwo",              "", 100, 0, 0.1);
  h_dvv_pass_twominntk           = fs->make<TH1F>("h_dvv_pass_twominntk",           "", 100, 0, 0.1);
  h_dvv_pass_foundv0             = fs->make<TH1F>("h_dvv_pass_foundv0",             "", 100, 0, 0.1);
  h_dvv_pass_foundv0samentk      = fs->make<TH1F>("h_dvv_pass_foundv0samentk",      "", 100, 0, 0.1);
  h_dvv_pass_foundv0andv1        = fs->make<TH1F>("h_dvv_pass_foundv0andv1",        "", 100, 0, 0.1);
  h_dvv_pass_foundv0andv1samentk = fs->make<TH1F>("h_dvv_pass_foundv0andv1samentk", "", 100, 0, 0.1);
}

namespace {
  template <typename T> T mag(T x, T y)      { return sqrt(x*x + y*y);       }
  template <typename T> T mag(T x, T y, T z) { return sqrt(x*x + y*y + z*z); }
}

void MFVOverlayVertexHistos::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<std::vector<double>> truth;
  event.getByToken(truth_token, truth);

  const int ntk0 = int(truth->at(0));
  const double x0 = truth->at(1);
  const double y0 = truth->at(2);
  const double z0 = truth->at(3);
  const int ntk1 = int(truth->at(4));
  //const double x1 = truth->at(5);
  //const double y1 = truth->at(6);
  //const double z1 = truth->at(7);
  const double x1_0 = truth->at(8);
  const double y1_0 = truth->at(9);
  const double z1_0 = truth->at(10);

  const double dvv_true = mag(x0 - x1_0, y0 - y1_0);

  edm::Handle<reco::VertexCollection> vertices;
  event.getByToken(vertices_token, vertices);

  h_dvv_true->Fill(dvv_true);

  int nvtx = int(vertices->size());
  int nvtx_minntk = 0;
  bool found[2] = {0};
  int found_ntk[2] = {0};
  const double found_dist = 0.012;

  for (const reco::Vertex& v : *vertices) {
    const int ntk = v.nTracks(0.);

    if (ntk >= min_ntracks)
      ++nvtx_minntk;

    if (mag(v.x() - x0, v.y() - y0, v.z() - z0) < found_dist) {
      found[0] = true;
      found_ntk[0] = ntk;
    }

    if (mag(v.x() - x1_0, v.y() - y1_0, v.z() - z1_0) < found_dist) {
      found[1] = true;
      found_ntk[1] = ntk;
    }
  } 

  auto fillit = [&dvv_true](TH1F* h, bool cond) { if (cond) h->Fill(dvv_true); };

  fillit(h_dvv_pass_anytwo,              nvtx >= 2);                                                            
  fillit(h_dvv_pass_twominntk,           nvtx_minntk >= 2);                                                     
  fillit(h_dvv_pass_foundv0,             found[0]);                                                             
  fillit(h_dvv_pass_foundv0samentk,      found[0] && found_ntk[0] == ntk0);                                     
  fillit(h_dvv_pass_foundv0andv1,        found[0] && found[1]);                                                 
  fillit(h_dvv_pass_foundv0andv1samentk, found[0] && found[1] && found_ntk[0] == ntk0 && found_ntk[1] == ntk1); 
}

DEFINE_FWK_MODULE(MFVOverlayVertexHistos);
