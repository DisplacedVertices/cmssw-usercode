#include "TH1F.h"
#include "TH2F.h"
#include "TLorentzVector.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"

class MFVResolutions : public edm::EDAnalyzer {
 public:
  explicit MFVResolutions(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::InputTag vertex_src;
  const edm::InputTag mevent_src;
  const int which_mom;
  const double max_dr;
  const double max_dist;
};

MFVResolutions::MFVResolutions(const edm::ParameterSet& cfg)
  : vertex_src(cfg.getParameter<edm::InputTag>("vertex_src")),
    mevent_src(cfg.getParameter<edm::InputTag>("mevent_src")),
    which_mom(cfg.getParameter<int>("which_mom")),
    max_dr(cfg.getParameter<double>("max_dr")),
    max_dist(cfg.getParameter<double>("max_dist"))
{
  die_if_not(which_mom >= 0 && which_mom < mfv::NMomenta, "invalid which_mom");

  edm::Service<TFileService> fs;
}

namespace {
  float mag(float x, float y) {
    return sqrt(x*x + y*y);
  }
  
  float mag(float x, float y, float z) {
    return sqrt(x*x + y*y + z*z);
  }
  
  float signed_mag(float x, float y) {
    float m = mag(x,y);
    if (y < 0) return -m;
    return m;
  }
}

void MFVResolutions::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<MFVEvent> mevent;
  event.getByLabel(mevent_src, mevent);

  die_if_not(mevent->gen_valid, "not running on signal sample");

  edm::Handle<MFVVertexAuxCollection> vertices;
  event.getByLabel(vertex_src, vertices);

  TLorentzVector lsp_p4s[2] = { mevent->gen_lsp_p4(0), mevent->gen_lsp_p4(1) };
  int lsp_nmatch[2] = {0,0};

  for (const MFVVertexAux& vtx : *vertices) {
    double dr = 1e99, dist = 1e99;

    int ilsp = -1;
    if (max_dr > 0) {
      double drs[2] = {
        reco::deltaR(lsp_p4s[0].Eta(), lsp_p4s[0].Phi(), vtx.eta[which_mom], vtx.phi[which_mom]),
        reco::deltaR(lsp_p4s[1].Eta(), lsp_p4s[1].Phi(), vtx.eta[which_mom], vtx.phi[which_mom])
      };
      
      for (int i = 0; i < 2; ++i) {
        if (drs[i] < max_dr) {
          ++lsp_nmatch[i];
          if (drs[i] < dr) {
            dr = drs[i];
            ilsp = i;
          }
        }
      }
    }
    else if (max_dist > 0) {
      double dists[2] = {
        mag(mevent->gen_lsp_decay[0*3+0] - vtx.x,
            mevent->gen_lsp_decay[0*3+1] - vtx.y,
            mevent->gen_lsp_decay[0*3+2] - vtx.z),
        mag(mevent->gen_lsp_decay[1*3+0] - vtx.x,
            mevent->gen_lsp_decay[1*3+1] - vtx.y,
            mevent->gen_lsp_decay[1*3+2] - vtx.z),
      };

      for (int i = 0; i < 2; ++i) {
        if (dists[i] < max_dist) {
          ++lsp_nmatch[i];
          if (dists[i] < dist) {
            dist = dists[i];
            ilsp = i;
          }
        }
      }
    }

    if (ilsp < 0)
      continue;


    const TLorentzVector& lsp_p4 = lsp_p4s[ilsp];
    const TLorentzVector& vtx_p4 = vtx.p4(which_mom);

    // histogram dr, dist, lsp_nmatch[i]
    // histogram space resolutions: x, y, z, dist2d, dist3d
    // histogram momentum: p, pt, eta, phi, mass, px, py, pz
  }
}

DEFINE_FWK_MODULE(MFVResolutions);
