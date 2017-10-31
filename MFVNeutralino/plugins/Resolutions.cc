#include "TH2.h"
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
  const edm::EDGetTokenT<MFVVertexAuxCollection> vertices_token;
  const edm::EDGetTokenT<MFVEvent> event_token;
  const int which_mom;
  const double max_dr;
  const double max_dist;
  const double max_dist_2d;
  const double max_dist_2d_square; // half length of side

  TH1F* h_dr;
  TH1F* h_dist;

  TH1F* h_lsp_nmatch[2];
  TH2F* h_lsp0nmatch_lsp1nmatch;
  TH2F* h_vtxmatch_vtxtotal;

  TH1F* h_dx;
  TH1F* h_dy;
  TH1F* h_dz;
  TH1F* h_dist2d;
  TH1F* h_dist3d;
  TH2F* h_s_dx_dy;
  TH2F* h_s_dx_dz;
  TH2F* h_s_dy_dz;

  TH1F* h_pull_dz;
  TH1F* h_pull_dist2d;

  TH1F* h_r_p;
  TH1F* h_r_pt;
  TH1F* h_r_eta;
  TH1F* h_r_phi;
  TH1F* h_r_mass;
  TH1F* h_r_msptm;
  TH1F* h_r_msptm_mass;
  TH1F* h_r_energy;
  TH1F* h_r_px;
  TH1F* h_r_py;
  TH1F* h_r_pz;
  TH1F* h_r_rapidity;
  TH1F* h_r_theta;
  TH1F* h_r_betagamma;
  TH1F* h_r_avgbetagammalab;
  TH1F* h_r_avgbetagammacmz;

  TH1F* h_f_p;
  TH1F* h_f_pt;
  TH1F* h_f_mass;
  TH1F* h_f_msptm;
  TH1F* h_f_msptm_mass;
  TH1F* h_f_energy;

  TH2F* h_rp_rmass;
  TH2F* h_fp_fmass;
  TH2F* h_s_p_mass;

  TH2F* h_rp_renergy;
  TH2F* h_fp_fenergy;
  TH2F* h_s_p_energy;

  TH2F* h_s_p;
  TH2F* h_s_pt;
  TH2F* h_s_eta;
  TH2F* h_s_phi;
  TH2F* h_s_mass;
  TH2F* h_s_msptm;
  TH2F* h_s_msptm_mass;
  TH2F* h_s_energy;
  TH2F* h_s_px;
  TH2F* h_s_py;
  TH2F* h_s_pz;
  TH2F* h_s_rapidity;
  TH2F* h_s_theta;
  TH2F* h_s_betagamma;
  TH2F* h_s_avgbetagammalab;
  TH2F* h_s_avgbetagammacmz;

  TH1F* h_flight_visdaus_theta;
  TH1F* h_flight_visdaus_phi;
  TH1F* h_flight_rec_theta;
  TH1F* h_flight_rec_phi;
};

MFVResolutions::MFVResolutions(const edm::ParameterSet& cfg)
  : vertices_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertex_src"))),
    event_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    which_mom(cfg.getParameter<int>("which_mom")),
    max_dr(cfg.getParameter<double>("max_dr")),
    max_dist(cfg.getParameter<double>("max_dist")),
    max_dist_2d(cfg.getParameter<double>("max_dist_2d")),
    max_dist_2d_square(cfg.getParameter<double>("max_dist_2d_square"))
{
  die_if_not(which_mom >= 0 && which_mom < mfv::NMomenta, "invalid which_mom");

  edm::Service<TFileService> fs;

  h_dr = fs->make<TH1F>("h_dr", ";deltaR to closest lsp;number of vertices", 150, 0, 7);
  h_dist = fs->make<TH1F>("h_dist", ";distance to closest lsp;number of vertices", 100, 0, 0.02);

  for (int i = 0; i < 2; ++i) {
    h_lsp_nmatch[i] = fs->make<TH1F>(TString::Format("h_lsp%d_nmatch", i), TString::Format(";number of vertices that match lsp%d;events", i), 15, 0, 15);
  }
  h_lsp0nmatch_lsp1nmatch = fs->make<TH2F>("h_lsp0nmatch_lsp1nmatch", ";lsp1_nmatch;lsp0_nmatch", 15, 0, 15, 15, 0, 15);
  h_vtxmatch_vtxtotal = fs->make<TH2F>("h_vtxmatch_vtxtotal", ";total number of vertices in the event;number of vertices that match an lsp", 15, 0, 15, 15, 0, 15);

  h_dx = fs->make<TH1F>("h_dx", ";x resolution (cm);number of vertices", 200, -0.02, 0.02);
  h_dy = fs->make<TH1F>("h_dy", ";y resolution (cm);number of vertices", 200, -0.02, 0.02);
  h_dz = fs->make<TH1F>("h_dz", ";z resolution (cm);number of vertices", 200, -0.02, 0.02);
  h_dist2d = fs->make<TH1F>("h_dist2d", ";dist2d(lsp,vtx) (cm);number of vertices", 100, 0, 0.02);
  h_dist3d = fs->make<TH1F>("h_dist3d", ";dist3d(lsp,vtx) (cm);number of vertices", 100, 0, 0.02);
  h_s_dx_dy = fs->make<TH2F>("h_s_dx_dy", ";y resolution (cm);x resolution (cm)", 200, -0.02, 0.02, 200, -0.02, 0.02);
  h_s_dx_dz = fs->make<TH2F>("h_s_dx_dz", ";z resolution (cm);x resolution (cm)", 200, -0.02, 0.02, 200, -0.02, 0.02);
  h_s_dy_dz = fs->make<TH2F>("h_s_dy_dz", ";z resolution (cm);y resolution (cm)", 200, -0.02, 0.02, 200, -0.02, 0.02);

  h_pull_dz = fs->make<TH1F>("h_pull_dz", ";pull on z resolution;number of vertices", 100, -5, 5);
  h_pull_dist2d = fs->make<TH1F>("h_pull_dist2d", ";pull on dist2d resolution;number of vertices", 100, 0, 5);

  h_r_p = fs->make<TH1F>("h_r_p", ";p resolution (GeV);number of vertices", 300, -1500, 1500);
  h_r_pt = fs->make<TH1F>("h_r_pt", ";p_{T} resolution (GeV);number of vertices", 300, -1500, 1500);
  h_r_eta = fs->make<TH1F>("h_r_eta", ";eta resolution;number of vertices", 50, -4, 4);
  h_r_phi = fs->make<TH1F>("h_r_phi", ";phi resolution;number of vertices", 50, -3.15, 3.15);
  h_r_mass = fs->make<TH1F>("h_r_mass", ";mass resolution (GeV);number of vertices", 300, -1500, 1500);
  h_r_msptm = fs->make<TH1F>("h_r_msptm", ";msptm resolution (GeV);number of vertices", 300, -1500, 1500);
  h_r_msptm_mass = fs->make<TH1F>("h_r_msptm_mass", ";msptm resolution w.r.t. mass (GeV);number of vertices", 300, -1500, 1500);
  h_r_energy = fs->make<TH1F>("h_r_energy", ";energy resolution (GeV);number of vertices", 300, -1500, 1500);
  h_r_px = fs->make<TH1F>("h_r_px", ";px resolution (GeV);number of vertices", 300, -1500, 1500);
  h_r_py = fs->make<TH1F>("h_r_py", ";py resolution (GeV);number of vertices", 300, -1500, 1500);
  h_r_pz = fs->make<TH1F>("h_r_pz", ";pz resolution (GeV);number of vertices", 300, -1500, 1500);
  h_r_rapidity = fs->make<TH1F>("h_r_rapidity", ";rapidity resolution;number of vertices", 50, -4, 4);
  h_r_theta = fs->make<TH1F>("h_r_theta", ";theta resolution;number of vertices", 50, -3.15, 3.15);
  h_r_betagamma = fs->make<TH1F>("h_r_betagamma", ";betagamma resolution;number of vertices", 200, -10, 10);
  h_r_avgbetagammalab = fs->make<TH1F>("h_r_avgbetagammalab", ";avgbetagammalab resolution;events", 200, -10, 10);
  h_r_avgbetagammacmz = fs->make<TH1F>("h_r_avgbetagammacmz", ";avgbetagammacmz resolution;events", 200, -10, 10);

  h_f_p = fs->make<TH1F>("h_f_p", ";fractional p resolution;number of vertices", 100, -1, 5);
  h_f_pt = fs->make<TH1F>("h_f_pt", ";fractional p_{T} resolution;number of vertices", 100, -1, 5);
  h_f_mass = fs->make<TH1F>("h_f_mass", ";fractional mass resolution;number of vertices", 100, -1, 5);
  h_f_msptm = fs->make<TH1F>("h_f_msptm", ";fractional msptm resolution;number of vertices", 100, -1, 5);
  h_f_msptm_mass = fs->make<TH1F>("h_f_msptm_mass", ";fractional msptm resolution w.r.t. mass;number of vertices", 100, -1, 5);
  h_f_energy = fs->make<TH1F>("h_f_energy", ";fractional energy resolution;number of vertices", 100, -1, 5);

  h_rp_rmass = fs->make<TH2F>("h_rp_rmass", ";mass resolution;p resolution", 300, -1500, 1500, 300, -1500, 1500);
  h_fp_fmass = fs->make<TH2F>("h_fp_fmass", ";fractional mass resolution;fractional p resolution", 300, -1, 2, 300, -1, 2);
  h_s_p_mass = fs->make<TH2F>("h_s_p_mass", ";reconstructed mass;reconstructed p", 150, 0, 1500, 150, 0, 1500);

  h_rp_renergy = fs->make<TH2F>("h_rp_renergy", ";energy resolution;p resolution", 300, -1500, 1500, 300, -1500, 1500);
  h_fp_fenergy = fs->make<TH2F>("h_fp_fenergy", ";fractional energy resolution;fractional p resolution", 300, -1, 2, 300, -1, 2);
  h_s_p_energy = fs->make<TH2F>("h_s_p_energy", ";reconstructed energy;reconstructed p", 150, 0, 1500, 150, 0, 1500);

  h_s_p = fs->make<TH2F>("h_s_p", ";generated p;reconstructed p", 150, 0, 1500, 150, 0, 1500);
  h_s_pt = fs->make<TH2F>("h_s_pt", ";generated pt;reconstructed pt", 150, 0, 1500, 150, 0, 1500);
  h_s_eta = fs->make<TH2F>("h_s_eta", ";generated eta;reconstructed eta", 50, -4, 4, 50, -4, 4);
  h_s_phi = fs->make<TH2F>("h_s_phi", ";generated phi;reconstructed phi", 50, -3.15, 3.15, 50, -3.15, 3.15);
  h_s_mass = fs->make<TH2F>("h_s_mass", ";generated mass;reconstructed mass", 150, 0, 1500, 150, 0, 1500);
  h_s_msptm = fs->make<TH2F>("h_s_msptm", ";generated msptm;reconstructed msptm", 150, 0, 1500, 150, 0, 1500);
  h_s_msptm_mass = fs->make<TH2F>("h_s_msptm_mass", ";generated mass;reconstructed msptm", 150, 0, 1500, 150, 0, 1500);
  h_s_energy = fs->make<TH2F>("h_s_energy", ";generated energy;reconstructed energy", 150, 0, 1500, 150, 0, 1500);
  h_s_px = fs->make<TH2F>("h_s_px", ";generated px;reconstructed px", 300, -1500, 1500, 300, -1500, 1500);
  h_s_py = fs->make<TH2F>("h_s_py", ";generated py;reconstructed py", 300, -1500, 1500, 300, -1500, 1500);
  h_s_pz = fs->make<TH2F>("h_s_pz", ";generated pz;reconstructed pz", 300, -1500, 1500, 300, -1500, 1500);
  h_s_rapidity = fs->make<TH2F>("h_s_rapidity", ";generated rapidity;reconstructed rapidity", 50, -4, 4, 50, -4, 4);
  h_s_theta = fs->make<TH2F>("h_s_theta", ";generated theta;reconstructed theta", 50, 0, 3.15, 50, 0, 3.15);
  h_s_betagamma = fs->make<TH2F>("h_s_betagamma", ";generated betagamma;reconstructed betagamma", 100, 0, 10, 100, 0, 10);
  h_s_avgbetagammalab = fs->make<TH2F>("h_s_avgbetagammalab", ";generated avgbetagammalab;reconstructed avgbetagammalab", 100, 0, 10, 100, 0, 10);
  h_s_avgbetagammacmz = fs->make<TH2F>("h_s_avgbetagammacmz", ";generated avgbetagammacmz;reconstructed avgbetagammacmz", 100, 0, 10, 100, 0, 10);

  h_flight_visdaus_theta = fs->make<TH1F>("h_flight_visdaus_theta", ";#Delta #theta between true flight dir and generated visible-daughter momentum; events/0.04", 100, -2, 2);
  h_flight_visdaus_phi = fs->make<TH1F>("h_flight_visdaus_phi", ";#Delta #phi between true flight dir and generated visible-daughter momentum; events/0.04", 100, -2, 2);
  h_flight_rec_theta = fs->make<TH1F>("h_flight_rec_theta", ";#Delta #theta between true flight dir and reconstructed momentum;events/0.04", 100, -2, 2);
  h_flight_rec_phi = fs->make<TH1F>("h_flight_rec_phi", ";#Delta #phi between true flight dir and reconstructed momentum;events/0.04", 100, -2, 2);
}

namespace {
  float mag(float x, float y) {
    return sqrt(x*x + y*y);
  }
  
  float mag(float x, float y, float z) {
    return sqrt(x*x + y*y + z*z);
  }
}

void MFVResolutions::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<MFVEvent> mevent;
  event.getByToken(event_token, mevent);

  die_if_not(mevent->gen_valid, "not running on signal sample");

  edm::Handle<MFVVertexAuxCollection> vertices;
  event.getByToken(vertices_token, vertices);

  const TLorentzVector lsp_p4s[2] = { mevent->gen_lsp_p4(0), mevent->gen_lsp_p4(1) };
  const TLorentzVector lsp_p4s_vis[2] = { mevent->gen_lsp_p4_vis(0), mevent->gen_lsp_p4_vis(1) };
  const TVector3 lsp_flights[2] = { mevent->gen_lsp_flight(0), mevent->gen_lsp_flight(1) };
  int lsp_nmatch[2] = {0,0};
  int nvtx_match = 0;

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
    else if (max_dist > 0 && max_dist_2d > 0 && max_dist_2d_square > 0) {
      double dists[2] = {
        mag(mevent->gen_lsp_decay[0*3+0] - vtx.x,
            mevent->gen_lsp_decay[0*3+1] - vtx.y,
            mevent->gen_lsp_decay[0*3+2] - vtx.z),
        mag(mevent->gen_lsp_decay[1*3+0] - vtx.x,
            mevent->gen_lsp_decay[1*3+1] - vtx.y,
            mevent->gen_lsp_decay[1*3+2] - vtx.z),
      };
      
      double dist2d[2] = {
        mag(mevent->gen_lsp_decay[0*3+0] - vtx.x,
            mevent->gen_lsp_decay[0*3+1] - vtx.y),
        mag(mevent->gen_lsp_decay[1*3+0] - vtx.x,
            mevent->gen_lsp_decay[1*3+1] - vtx.y),
      };

      double dist2d_square_x[2] = {
        fabs(mevent->gen_lsp_decay[0*3+0] - vtx.x),
        fabs(mevent->gen_lsp_decay[1*3+0] - vtx.x)
      };

      double dist2d_square_y[2] = {
        fabs(mevent->gen_lsp_decay[0*3+1] - vtx.y),
	fabs(mevent->gen_lsp_decay[1*3+1] - vtx.y)
      };
      

      for (int i = 0; i < 2; ++i) {
        if (dists[i] < max_dist && dist2d[i] < max_dist_2d && dist2d_square_x[i] < max_dist_2d_square && dist2d_square_y[i] < max_dist_2d_square) {
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

    ++nvtx_match;
    const TLorentzVector& lsp_p4 = lsp_p4s[ilsp];
    const TLorentzVector& lsp_p4_vis = lsp_p4s_vis[ilsp];
    const TVector3& lsp_flight = lsp_flights[ilsp];
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
    h_s_dx_dy->Fill(vtx.y - mevent->gen_lsp_decay[ilsp*3+1], vtx.x - mevent->gen_lsp_decay[ilsp*3+0]);
    h_s_dx_dz->Fill(vtx.z - mevent->gen_lsp_decay[ilsp*3+2], vtx.x - mevent->gen_lsp_decay[ilsp*3+0]);
    h_s_dy_dz->Fill(vtx.z - mevent->gen_lsp_decay[ilsp*3+2], vtx.y - mevent->gen_lsp_decay[ilsp*3+1]);

    // histogram space pulls: z, dist2d
    h_pull_dz->Fill((vtx.z - mevent->gen_lsp_decay[ilsp*3+2]) / sqrt(vtx.czz));
    h_pull_dist2d->Fill(mag(mevent->gen_lsp_decay[ilsp*3+0] - vtx.x,
                            mevent->gen_lsp_decay[ilsp*3+1] - vtx.y) / vtx.bs2derr);

    // histogram momentum resolutions: p, pt, eta, phi, mass, energy, px, py, pz, rapidity, theta, betagamma
    double vtx_msptm = sqrt(vtx_p4.M() * vtx_p4.M() + vtx_p4.Pt() * vtx_p4.Pt())+ fabs(vtx_p4.Pt());
    double lsp_msptm = sqrt(lsp_p4.M() * lsp_p4.M() + lsp_p4.Pt() * lsp_p4.Pt())+ fabs(lsp_p4.Pt());

    h_r_p->Fill(vtx_p4.P() - lsp_p4.P());
    h_r_pt->Fill(vtx_p4.Pt() - lsp_p4.Pt());
    h_r_eta->Fill(vtx_p4.Eta() - lsp_p4.Eta());
    h_r_phi->Fill(reco::deltaPhi(vtx_p4.Phi(), lsp_p4.Phi()));
    h_r_mass->Fill(vtx_p4.M() - lsp_p4.M());
    h_r_msptm->Fill(vtx_msptm - lsp_msptm);
    h_r_msptm_mass->Fill(vtx_msptm - lsp_p4.M());
    h_r_energy->Fill(vtx_p4.E() - lsp_p4.E());
    h_r_px->Fill(vtx_p4.Px() - lsp_p4.Px());
    h_r_py->Fill(vtx_p4.Py() - lsp_p4.Py());
    h_r_pz->Fill(vtx_p4.Pz() - lsp_p4.Pz());
    h_r_rapidity->Fill(vtx_p4.Rapidity() - lsp_p4.Rapidity());
    h_r_theta->Fill(vtx_p4.Theta() - lsp_p4.Theta());
    h_r_betagamma->Fill(vtx_p4.Beta()*vtx_p4.Gamma() - lsp_p4.Beta()*lsp_p4.Gamma());

    h_f_p->Fill((vtx_p4.P() - lsp_p4.P()) / lsp_p4.P());
    h_f_pt->Fill((vtx_p4.Pt() - lsp_p4.Pt()) / lsp_p4.Pt());
    h_f_mass->Fill((vtx_p4.M() - lsp_p4.M()) / lsp_p4.M());
    h_f_msptm->Fill((vtx_msptm - lsp_msptm) / lsp_msptm);
    h_f_msptm_mass->Fill((vtx_msptm - lsp_p4.M()) / lsp_p4.M());
    h_f_energy->Fill((vtx_p4.E() - lsp_p4.E()) / lsp_p4.E());

    h_rp_rmass->Fill(vtx_p4.M() - lsp_p4.M(), vtx_p4.P() - lsp_p4.P());
    h_fp_fmass->Fill((vtx_p4.M() - lsp_p4.M()) / lsp_p4.M(), (vtx_p4.P() - lsp_p4.P()) / lsp_p4.P());
    h_s_p_mass->Fill(vtx_p4.M(), vtx_p4.P());

    h_rp_renergy->Fill(vtx_p4.M() - lsp_p4.M(), vtx_p4.E() - lsp_p4.E());
    h_fp_fenergy->Fill((vtx_p4.M() - lsp_p4.M()) / lsp_p4.M(), (vtx_p4.E() - lsp_p4.E()) / lsp_p4.E());
    h_s_p_energy->Fill(vtx_p4.M(), vtx_p4.E());

    h_s_p->Fill(lsp_p4.P(), vtx_p4.P());
    h_s_pt->Fill(lsp_p4.Pt(), vtx_p4.Pt());
    h_s_eta->Fill(lsp_p4.Eta(), vtx_p4.Eta());
    h_s_phi->Fill(lsp_p4.Phi(), vtx_p4.Phi());
    h_s_mass->Fill(lsp_p4.M(), vtx_p4.M());
    h_s_msptm->Fill(lsp_msptm, vtx_msptm);
    h_s_msptm_mass->Fill(lsp_p4.M(), vtx_msptm);
    h_s_energy->Fill(lsp_p4.E(), vtx_p4.E());
    h_s_px->Fill(lsp_p4.Px(), vtx_p4.Px());
    h_s_py->Fill(lsp_p4.Py(), vtx_p4.Py());
    h_s_pz->Fill(lsp_p4.Pz(), vtx_p4.Pz());
    h_s_rapidity->Fill(lsp_p4.Rapidity(), vtx_p4.Rapidity());
    h_s_theta->Fill(lsp_p4.Theta(), vtx_p4.Theta());
    h_s_betagamma->Fill(lsp_p4.Beta()*lsp_p4.Gamma(), vtx_p4.Beta()*vtx_p4.Gamma());

    h_flight_visdaus_theta->Fill(lsp_p4_vis.Vect().Theta() - lsp_flight.Theta());
    h_flight_visdaus_phi->Fill(lsp_p4_vis.Vect().DeltaPhi(lsp_flight));
    h_flight_rec_theta->Fill(vtx_p4.Vect().Theta() - lsp_flight.Theta());
    h_flight_rec_phi->Fill(vtx_p4.Vect().DeltaPhi(lsp_flight));
  }

  // histogram lsp_nmatch
  for (int i = 0; i < 2; ++i) {
    h_lsp_nmatch[i]->Fill(lsp_nmatch[i]);
  }
  h_lsp0nmatch_lsp1nmatch->Fill(lsp_nmatch[1], lsp_nmatch[0]);

  const int nsv = int(vertices->size());
  h_vtxmatch_vtxtotal->Fill(nsv, nvtx_match);

  // histogram average betagamma resolutions
  if (nsv >= 2) {
    const MFVVertexAux& v0 = vertices->at(0);
    const MFVVertexAux& v1 = vertices->at(1);

    TLorentzVector lsp0_p4 = lsp_p4s[0];
    TLorentzVector lsp1_p4 = lsp_p4s[1];
    double lsp_avgbetagammalab = (lsp0_p4.Beta()*lsp0_p4.Gamma() + lsp1_p4.Beta()*lsp1_p4.Gamma()) / 2;
    TVector3 lsp_betacmz = TVector3(0, 0, -(lsp0_p4.Pz() + lsp1_p4.Pz()) / (lsp0_p4.E() + lsp1_p4.E()));
    lsp0_p4.Boost(lsp_betacmz);
    lsp1_p4.Boost(lsp_betacmz);
    double lsp_avgbetagammacmz = (lsp0_p4.Beta()*lsp0_p4.Gamma() + lsp1_p4.Beta()*lsp1_p4.Gamma()) / 2;

    TLorentzVector vtx0_p4 = v0.p4(which_mom);
    TLorentzVector vtx1_p4 = v1.p4(which_mom);
    double vtx_avgbetagammalab = (vtx0_p4.Beta()*vtx0_p4.Gamma() + vtx1_p4.Beta()*vtx1_p4.Gamma()) / 2;
    TVector3 vtx_betacmz = TVector3(0, 0, -(vtx0_p4.Pz() + vtx1_p4.Pz()) / (vtx0_p4.E() + vtx1_p4.E()));
    vtx0_p4.Boost(vtx_betacmz);
    vtx1_p4.Boost(vtx_betacmz);
    double vtx_avgbetagammacmz = (vtx0_p4.Beta()*vtx0_p4.Gamma() + vtx1_p4.Beta()*vtx1_p4.Gamma()) / 2;

    h_r_avgbetagammalab->Fill(vtx_avgbetagammalab - lsp_avgbetagammalab);
    h_r_avgbetagammacmz->Fill(vtx_avgbetagammacmz - lsp_avgbetagammacmz);
    h_s_avgbetagammalab->Fill(lsp_avgbetagammalab, vtx_avgbetagammalab);
    h_s_avgbetagammacmz->Fill(lsp_avgbetagammacmz, vtx_avgbetagammacmz);

  }
}

DEFINE_FWK_MODULE(MFVResolutions);
