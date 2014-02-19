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

  TH1F* h_lsp_nmatch[2];
  TH1F* h_dr;
  TH1F* h_dist;

  TH1F* h_dx;
  TH1F* h_dy;
  TH1F* h_dz;
  TH1F* h_dist2d;
  TH1F* h_dist3d;

  TH1F* h_r_p;
  TH1F* h_r_pt;
  TH1F* h_r_eta;
  TH1F* h_r_phi;
  TH1F* h_r_mass;
  TH1F* h_r_px;
  TH1F* h_r_py;
  TH1F* h_r_pz;
  TH1F* h_r_rapidity;
  TH1F* h_r_theta;

  TH1F* h_f_p;
  TH1F* h_f_pt;
  TH1F* h_f_mass;
  TH1F* h_f_px;
  TH1F* h_f_py;
  TH1F* h_f_pz;

  TH2F* h_s_p;
  TH2F* h_s_pt;
  TH2F* h_s_eta;
  TH2F* h_s_phi;
  TH2F* h_s_mass;
  TH2F* h_s_px;
  TH2F* h_s_py;
  TH2F* h_s_pz;
  TH2F* h_s_rapidity;
  TH2F* h_s_theta;

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

  for (int i = 0; i < 2; ++i) {
    h_lsp_nmatch[i] = fs->make<TH1F>(TString::Format("h_lsp%d_nmatch", i), TString::Format(";number of vertices that match lsp%d;events", i), 15, 0, 15);
  }
  h_dr = fs->make<TH1F>("h_dr", ";deltaR to closest lsp;number of vertices", 150, 0, 7);
  h_dist = fs->make<TH1F>("h_dist", ";distance to closest lsp;number of vertices", 100, 0, 0.02);

  h_dx = fs->make<TH1F>("h_dx", ";x resolution (cm);number of vertices", 200, -0.02, 0.02);
  h_dy = fs->make<TH1F>("h_dy", ";y resolution (cm);number of vertices", 200, -0.02, 0.02);
  h_dz = fs->make<TH1F>("h_dz", ";z resolution (cm);number of vertices", 200, -0.02, 0.02);
  h_dist2d = fs->make<TH1F>("h_dist2d", ";dist2d(lsp,vtx) (cm);number of vertices", 100, 0, 0.02);
  h_dist3d = fs->make<TH1F>("h_dist3d", ";dist3d(lsp,vtx) (cm);number of vertices", 100, 0, 0.02);

  h_r_p = fs->make<TH1F>("h_r_p", ";p resolution (GeV);number of vertices", 300, -1500, 1500);
  h_r_pt = fs->make<TH1F>("h_r_pt", ";p_{T} resolution (GeV);number of vertices", 300, -1500, 1500);
  h_r_eta = fs->make<TH1F>("h_r_eta", ";eta resolution;number of vertices", 50, -4, 4);
  h_r_phi = fs->make<TH1F>("h_r_phi", ";phi resolution;number of vertices", 50, -3.15, 3.15);
  h_r_mass = fs->make<TH1F>("h_r_mass", ";mass resolution (GeV);number of vertices", 300, -1500, 1500);
  h_r_px = fs->make<TH1F>("h_r_px", ";px resolution (GeV);number of vertices", 300, -1500, 1500);
  h_r_py = fs->make<TH1F>("h_r_py", ";py resolution (GeV);number of vertices", 300, -1500, 1500);
  h_r_pz = fs->make<TH1F>("h_r_pz", ";pz resolution (GeV);number of vertices", 300, -1500, 1500);
  h_r_rapidity = fs->make<TH1F>("h_r_rapidity", ";rapidity resolution;number of vertices", 50, -4, 4);
  h_r_theta = fs->make<TH1F>("h_r_theta", ";theta resolution;number of vertices", 50, -3.15, 3.15);

  h_f_p = fs->make<TH1F>("h_f_p", ";fractional p resolution;number of vertices", 100, -5, 5);
  h_f_pt = fs->make<TH1F>("h_f_pt", ";fractional pt resolution;number of vertices", 100, -5, 5);
  h_f_mass = fs->make<TH1F>("h_f_mass", ";fractional mass resolution;number of vertices", 100, -5, 5);
  h_f_px = fs->make<TH1F>("h_f_px", ";fractional px resolution;number of vertices", 100, -5, 5);
  h_f_py = fs->make<TH1F>("h_f_py", ";fractional py resolution;number of vertices", 100, -5, 5);
  h_f_pz = fs->make<TH1F>("h_f_pz", ";fractional pz resolution;number of vertices", 100, -5, 5);

  h_s_p = fs->make<TH2F>("h_s_p", ";generated p;reconstructed p", 150, 0, 1500, 150, 0, 1500);
  h_s_pt = fs->make<TH2F>("h_s_pt", ";generated pt;reconstructed pt", 150, 0, 1500, 150, 0, 1500);
  h_s_eta = fs->make<TH2F>("h_s_eta", ";generated eta;reconstructed eta", 50, -4, 4, 50, -4, 4);
  h_s_phi = fs->make<TH2F>("h_s_phi", ";generated phi;reconstructed phi", 50, -3.15, 3.15, 50, -3.15, 3.15);
  h_s_mass = fs->make<TH2F>("h_s_mass", ";generated mass;reconstructed mass", 150, 0, 1500, 150, 0, 1500);
  h_s_px = fs->make<TH2F>("h_s_px", ";generated px;reconstructed px", 150, 0, 1500, 150, 0, 1500);
  h_s_py = fs->make<TH2F>("h_s_py", ";generated py;reconstructed py", 150, 0, 1500, 150, 0, 1500);
  h_s_pz = fs->make<TH2F>("h_s_pz", ";generated pz;reconstructed pz", 150, 0, 1500, 150, 0, 1500);
  h_s_rapidity = fs->make<TH2F>("h_s_rapidity", ";generated rapidity;reconstructed rapidity", 50, -4, 4, 50, -4, 4);
  h_s_theta = fs->make<TH2F>("h_s_theta", ";generated theta;reconstructed theta", 50, 0, 3.15, 50, 0, 3.15);
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

    // histogram dr, dist
    h_dr->Fill(dr);
    h_dist->Fill(dist);

    // histogram space resolutions: x, y, z, dist2d, dist3d
    h_dx->Fill(vtx.x - mevent->gen_lsp_decay[ilsp*3+0]);
    h_dy->Fill(vtx.y - mevent->gen_lsp_decay[ilsp*3+1]);
    h_dz->Fill(vtx.z - mevent->gen_lsp_decay[ilsp*3+2]);
    h_dist2d->Fill(mag(mevent->gen_lsp_decay[ilsp*3+0] - vtx.x,
                       mevent->gen_lsp_decay[ilsp*3+1] - vtx.y));
    h_dist3d->Fill(mag(mevent->gen_lsp_decay[ilsp*3+0] - vtx.x,
                       mevent->gen_lsp_decay[ilsp*3+1] - vtx.y,
                       mevent->gen_lsp_decay[ilsp*3+2] - vtx.z));

    // histogram momentum resolutions: p, pt, eta, phi, mass, px, py, pz, rapidity, theta
    h_r_p->Fill(vtx_p4.P() - lsp_p4.P());
    h_r_pt->Fill(vtx_p4.Pt() - lsp_p4.Pt());
    h_r_eta->Fill(vtx_p4.Eta() - lsp_p4.Eta());
    h_r_phi->Fill(reco::deltaPhi(vtx_p4.Phi(), lsp_p4.Phi()));
    h_r_mass->Fill(vtx_p4.M() - lsp_p4.M());
    h_r_px->Fill(vtx_p4.Px() - lsp_p4.Px());
    h_r_py->Fill(vtx_p4.Py() - lsp_p4.Py());
    h_r_pz->Fill(vtx_p4.Pz() - lsp_p4.Pz());
    h_r_rapidity->Fill(vtx_p4.Rapidity() - lsp_p4.Rapidity());
    h_r_theta->Fill(vtx_p4.Theta() - lsp_p4.Theta());

    h_f_p->Fill((vtx_p4.P() - lsp_p4.P()) / lsp_p4.P());
    h_f_pt->Fill((vtx_p4.Pt() - lsp_p4.Pt()) / lsp_p4.Pt());
    h_f_mass->Fill((vtx_p4.M() - lsp_p4.M()) / lsp_p4.M());
    h_f_px->Fill((vtx_p4.Px() - lsp_p4.Px()) / lsp_p4.Px());
    h_f_py->Fill((vtx_p4.Py() - lsp_p4.Py()) / lsp_p4.Py());
    h_f_pz->Fill((vtx_p4.Pz() - lsp_p4.Pz()) / lsp_p4.Pz());

    h_s_p->Fill(lsp_p4.P(), vtx_p4.P());
    h_s_pt->Fill(lsp_p4.Pt(), vtx_p4.Pt());
    h_s_eta->Fill(lsp_p4.Eta(), vtx_p4.Eta());
    h_s_phi->Fill(lsp_p4.Phi(), vtx_p4.Phi());
    h_s_mass->Fill(lsp_p4.M(), vtx_p4.M());
    h_s_px->Fill(lsp_p4.Px(), vtx_p4.Px());
    h_s_py->Fill(lsp_p4.Py(), vtx_p4.Py());
    h_s_pz->Fill(lsp_p4.Pz(), vtx_p4.Pz());
    h_s_rapidity->Fill(lsp_p4.Rapidity(), vtx_p4.Rapidity());
    h_s_theta->Fill(lsp_p4.Theta(), vtx_p4.Theta());
  }

  // histogram lsp_nmatch[i]
  for (int i = 0; i < 2; ++i) {
    h_lsp_nmatch[i]->Fill(lsp_nmatch[i]);
  }
}

DEFINE_FWK_MODULE(MFVResolutions);
