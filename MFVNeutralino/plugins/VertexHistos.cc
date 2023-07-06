#include "TH2.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/ExtValue.h"
#include "JMTucker/Tools/interface/PairwiseHistos.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"

class MFVVertexHistos : public edm::EDAnalyzer {
 public:
  explicit MFVVertexHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::EDGetTokenT<MFVEvent> mevent_token;
  const edm::EDGetTokenT<double> weight_token;
  const edm::EDGetTokenT<MFVVertexAuxCollection> vertex_token;
  const int max_ntrackplots;
  const bool do_scatterplots;

  enum sv_index { sv_all, sv_num_indices };
  static const char* sv_index_names[sv_num_indices];

  void fill(TH1F** hs,          const int, const double val,                    const double weight) const { hs[sv_all]->Fill(val, weight); }
  void fill(TH2F** hs,          const int, const double val, const double val2, const double weight) const { hs[sv_all]->Fill(val, val2, weight); }
  void fill(PairwiseHistos* hs, const int, const PairwiseHistos::ValueMap& val, const double weight) const { hs[sv_all].Fill(val, -1, weight); }

  Measurement1D miss_dist(const math::XYZPoint&, const math::XYZPoint&, const math::XYZPoint&, const double [9], const double [9]);

  PairwiseHistos h_sv[sv_num_indices];

  TH1F* h_sv_jets_deltaphi[4][sv_num_indices];

  TH2F* h_sv_bs2derr_bsbs2ddist[sv_num_indices];
  TH2F* h_pvrho_bsbs2ddist[sv_num_indices];

  TH1F* h_w;
  TH1F* h_nsv;
  // assoc. lep in sv
  TH1F* h_nsv_wlep;

  TH1F* h_nsv_eflavor;
  TH1F* h_nsv_mflavor;
  TH1F* h_nsv_emuflavor;
  TH1F* h_nmsv;
  TH1F* h_nesv;
  TH1F* h_nemusv;

  TH1F* h_nsv_genmatched;
  //distance from SV to gen SV 
  TH1F* h_sv_genv_mag;
  TH1F* h_sv_ele_genv_mag;
  TH1F* h_sv_mu_genv_mag;
  TH1F* h_sv_tau_genv_mag;

  TH2F* h_svidx_assoclep;
  TH2F* h_svidx_assocmu;
  TH2F* h_svidx_assocel;

  //lepton specifc 
  TH1F* h_gen_ele_closestdR;
  TH1F* h_gen_mu_closestdR;
  TH1F* h_nmatchele;
  TH1F* h_nmatchmu;

  //gen daughter reconstructed but no vertex
  TH1F* h_lepdau_novtx_[2];
  //gen daughter reconstructed and the vertex is reconstructed 
  TH1F* h_lepdau_wvtx_[2];
  // gen daughter is one of the tracks in the vertex (matching via)
  TH1F* h_lepdau_invtx_[2];

  TH1F* h_matchlep_dxy_[2];
  TH1F* h_matchlep_dxyerr_[2];
  TH1F* h_matchlep_missdist_[2];
  TH1F* h_matchlep_nsigmadxy_[2];
  TH1F* h_matchlep_missdisterr_[2];
  TH1F* h_matchlep_missdistsig_[2];
  TH1F* h_matchlep_pt_[2];

  //track requirements 
  TH1F* h_matchlep_nm1_minr_[2];
  TH1F* h_matchlep_nm1_npxlayers_[2];
  TH1F* h_matchlep_nm1_nstlayers_[2];
  TH1F* h_matchlep_nm1_nsigmadxy_[2];
  TH2F* h_matchlep_genvtx_pos_[2];

  TH1F* h_nomatchlep_dxy_[2];
  TH1F* h_nomatchlep_dxyerr_[2];
  TH1F* h_nomatchlep_missdist_[2];
  TH1F* h_nomatchlep_nsigmadxy_[2];
  TH1F* h_nomatchlep_missdisterr_[2];
  TH1F* h_nomatchlep_missdistsig_[2];
  TH1F* h_nomatchlep_pt_[2];
  TH1F* h_nomatchlep_trkdR_[2];

  //track requirements 
  TH1F* h_nomatchlep_nm1_minr_[2];
  TH1F* h_nomatchlep_nm1_npxlayers_[2];
  TH1F* h_nomatchlep_nm1_nstlayers_[2];
  TH1F* h_nomatchlep_nm1_nsigmadxy_[2];
  TH2F* h_nomatchlep_genvtx_pos_[2];


  TH1F* h_sv_gen2ddist_signed;
  TH2F* h_sv_ntk_genbs2ddist;
  TH2F* h_sv_ntk_bs2ddist;
  TH2F* h_sv_ntk_gen2ddist;
  TH2F* h_sv_ntk_njet;
  TH2F* h_sv_ntk0_ntk1;
  TH2F* h_sv_nsv_nmatchjet;

  TH2F* h_sv_xy;
  TH2F* h_sv_yz;
  TH2F* h_sv_xz;
  TH2F* h_sv_rz;
  TH1F* h_svdist2d;
  TH1F* h_svdist3d;
  TH2F* h_sv0pvdz_v_sv1pvdz;
  TH2F* h_sv0pvdzsig_v_sv1pvdzsig;
  TH1F* h_absdeltaphi01;
  TH2F* h_pvmosttracksshared;
  TH1F* h_fractrackssharedwpv01;
  TH1F* h_fractrackssharedwpvs01;
  TH1F* h_sv_shared_jets;
  TH1F* h_svdist2d_shared_jets;
  TH1F* h_svdist2d_no_shared_jets;
  TH1F* h_absdeltaphi01_shared_jets;
  TH1F* h_absdeltaphi01_no_shared_jets;

  TH1F* h_sv_track_weight[sv_num_indices];
  TH1F* h_sv_track_q[sv_num_indices];
  TH1F* h_sv_track_pt[sv_num_indices];
  TH1F* h_sv_track_eta[sv_num_indices];
  TH1F* h_sv_track_phi[sv_num_indices];
  TH1F* h_sv_track_dxy[sv_num_indices];
  TH1F* h_sv_track_dz[sv_num_indices];
  TH1F* h_sv_track_pt_err[sv_num_indices];
  TH1F* h_sv_track_eta_err[sv_num_indices];
  TH1F* h_sv_track_phi_err[sv_num_indices];
  TH1F* h_sv_track_dxy_err[sv_num_indices];
  TH1F* h_sv_track_dz_err[sv_num_indices];
  TH1F* h_sv_track_nsigmadxy[sv_num_indices];
  TH1F* h_sv_track_chi2dof[sv_num_indices];
  TH1F* h_sv_track_npxhits[sv_num_indices];
  TH1F* h_sv_track_nsthits[sv_num_indices];
  TH1F* h_sv_track_nhitsbehind[sv_num_indices];
  TH1F* h_sv_track_nhitslost[sv_num_indices];
  TH1F* h_sv_track_nhits[sv_num_indices];
  TH1F* h_sv_track_injet[sv_num_indices];
  TH1F* h_sv_track_inpv[sv_num_indices];

  TH1F* h_sv_eletrack_pt[sv_num_indices];
  TH1F* h_sv_eletrack_eta[sv_num_indices];
  TH1F* h_sv_eletrack_phi[sv_num_indices];
  TH1F* h_sv_eletrack_dxy[sv_num_indices];
  TH1F* h_sv_eletrack_iso[sv_num_indices];
  TH1F* h_sv_eletrack_ID[sv_num_indices];
  // TH1F* h_sv_alleletrack_tip[sv_num_indices];
  // TH1F* h_sv_alleletrack_tiperr[sv_num_indices];
  // TH1F* h_sv_alleletrack_tipsig[sv_num_indices];
  // TH1F* h_sv_matchedeletrack_tip[sv_num_indices];
  // TH1F* h_sv_matchedeletrack_tiperr[sv_num_indices];
  // TH1F* h_sv_matchedeletrack_tipsig[sv_num_indices];

  TH1F* h_sv_mutrack_pt[sv_num_indices];
  TH1F* h_sv_mutrack_eta[sv_num_indices];
  TH1F* h_sv_mutrack_phi[sv_num_indices];
  TH1F* h_sv_mutrack_dxy[sv_num_indices];
  TH1F* h_sv_mutrack_iso[sv_num_indices];
  TH1F* h_sv_mutrack_ID[sv_num_indices];
  // TH1F* h_sv_allmutrack_tip[sv_num_indices];
  // TH1F* h_sv_allmutrack_tiperr[sv_num_indices];
  // TH1F* h_sv_allmutrack_tipsig[sv_num_indices];
  // TH1F* h_sv_matchedmutrack_tip[sv_num_indices];
  // TH1F* h_sv_matchedmutrack_tiperr[sv_num_indices];
  // TH1F* h_sv_matchedmutrack_tipsig[sv_num_indices];
};

const char* MFVVertexHistos::sv_index_names[MFVVertexHistos::sv_num_indices] = { "all" };

MFVVertexHistos::MFVVertexHistos(const edm::ParameterSet& cfg)
  : mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
    vertex_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertex_src"))),
    max_ntrackplots(cfg.getParameter<int>("max_ntrackplots")),
    do_scatterplots(cfg.getParameter<bool>("do_scatterplots"))
{
  edm::Service<TFileService> fs;

  h_w = fs->make<TH1F>("h_w", ";event weight;events/0.1", 100, 0, 10);
  h_nsv = fs->make<TH1F>("h_nsv", ";# of secondary vertices;arb. units", 15, 0, 15);
  h_nsv_wlep = fs->make<TH1F>("h_nsv_wlep", ";# of secondary vertices with at least 1 assoc. lep;arb. units", 15, 0, 15);
  h_nsv_eflavor = fs->make<TH1F>("h_nsv_eflavor", "; # of secondary vertices genmatched to ele sv; arb. units", 4, 0, 4);
  h_nsv_mflavor = fs->make<TH1F>("h_nsv_mflavor", "; # of secondary vertices genmatched to mu sv; arb. units", 4, 0, 4);
  h_nsv_emuflavor = fs->make<TH1F>("h_nsv_emuflavor", "; # of secondary vertices genmatched to ele or mu sv; arb. units", 6, 0, 6);
  h_nmsv = fs->make<TH1F>("h_nmsv", "; # of secondary vertices genmatched to mu sv with mu in sv; arb. units", 4, 0, 4);
  h_nesv = fs->make<TH1F>("h_nesv", "; # of secondary vertices genmatched to ele sv with ele in sv; arb. units", 4, 0, 4);
  h_nemusv = fs->make<TH1F>("h_nemusv", "; # of secondary vertices genmatched to ele or mu sv with ele or mu in sv; arb. units", 6, 0, 6);

  h_nsv_genmatched = fs->make<TH1F>("h_nsv_genmatched", ";# of secondary vertices < 0.02 away from gen vertex;arb. units", 15, 0, 15);
  h_sv_genv_mag = fs->make<TH1F>("h_sv_genv_mag", ";Mag(genvtx, closest recovtx);arb. units", 200, 0, 0.2);
  h_sv_ele_genv_mag = fs->make<TH1F>("h_sv_ele_genv_mag", ";Mag(genvtx with ele, closest recovtx);arb. units", 200, 0, 0.2);
  h_sv_mu_genv_mag = fs->make<TH1F>("h_sv_mu_genv_mag", ";Mag(genvtx with mu, closest recovtx);arb. units", 200, 0, 0.2);
  h_sv_tau_genv_mag = fs->make<TH1F>("h_sv_tau_genv_mag", ";Mag(genvtx with tau, closest recovtx);arb. units", 200, 0, 0.2);

  h_svidx_assoclep = fs->make<TH2F>("h_svidx_assoclep", "; N of associated leptons in the SV);SV Index", 10, 0, 10, 10, 0, 10);
  h_svidx_assocmu  = fs->make<TH2F>("h_svidx_assocmu", "; N of associated muons in the SV);SV Index", 10, 0, 10, 10, 0, 10);
  h_svidx_assocel  = fs->make<TH2F>("h_svidx_assocel", "; N of associated electrons in the SV);SV Index", 10, 0, 10, 10, 0, 10);

  h_gen_ele_closestdR = fs->make<TH1F>("h_gen_ele_closestdR", "; dR of best match btwn gen - reco ele", 200, 0, 0.2);
  h_gen_mu_closestdR = fs->make<TH1F>("h_gen_mu_closestdR", "; dR of best match btwn gen - reco mu", 200, 0, 0.2);
  h_nmatchele = fs->make<TH1F>("h_nmatchele", "; # of electrons matched to gen-level electrons;events", 10, 0, 10);
  h_nmatchmu = fs->make<TH1F>("h_nmatchmu", "; # of muons matched to gen-level muons;events", 10, 0, 10);


  const char* lep_tag[2] = {"ele", "mu"};
  for (int i = 0; i< 2; ++i) {
    h_lepdau_novtx_[i] = fs->make<TH1F>(TString::Format("h_lepdau_novtx_%s", lep_tag[i]), TString::Format("; no SV matched - is the reco %s matched?;", lep_tag[i]), 3, 0, 3);
    h_lepdau_wvtx_[i] = fs->make<TH1F>(TString::Format("h_lepdau_wvtx_%s", lep_tag[i]), TString::Format("; SV is matched - is the reco %s matched?;", lep_tag[i]), 3, 0, 3);
    h_lepdau_invtx_[i] = fs->make<TH1F>(TString::Format("h_lepdau_invtx_%s", lep_tag[i]), TString::Format("; SV & %s are matched - is the %s in the SV?;", lep_tag[i], lep_tag[i]), 3, 0, 3);
    h_matchlep_dxy_[i] = fs->make<TH1F>(TString::Format("h_matchlep_dxy_%s", lep_tag[i]), TString::Format("; genmatched %s inSV dxy;", lep_tag[i]), 150, 0, 3.0);
    h_matchlep_dxyerr_[i] = fs->make<TH1F>(TString::Format("h_matchlep_dxyerr_%s", lep_tag[i]), TString::Format("; genmatched %s inSV dxyerr;", lep_tag[i]), 100, 0, 0.05);
    h_matchlep_nsigmadxy_[i] = fs->make<TH1F>(TString::Format("h_matchlep_nsigmadxy_%s", lep_tag[i]), TString::Format("; genmatched %s inSV nsigmadxy;", lep_tag[i]), 200, 0, 200);
    h_matchlep_pt_[i] = fs->make<TH1F>(TString::Format("h_matchlep_pt_%s", lep_tag[i]), TString::Format("; genmatched %s inSV pt;", lep_tag[i]), 200, 0, 1000);
    h_matchlep_nm1_minr_[i] = fs->make<TH1F>(TString::Format("h_matchlep_nm1_minr_%s", lep_tag[i]), TString::Format("; genmatched %s inSV nm1 minr;", lep_tag[i]), 10, 0, 10);
    h_matchlep_nm1_npxlayers_[i] = fs->make<TH1F>(TString::Format("h_matchlep_nm1_npxlayers_%s", lep_tag[i]), TString::Format("; genmatched %s inSV nm1 npxlayers;", lep_tag[i]), 20, 0, 20);
    h_matchlep_nm1_nstlayers_[i] = fs->make<TH1F>(TString::Format("h_matchlep_nm1_nstlayers_%s", lep_tag[i]), TString::Format("; genmatched %s inSV nm1 nstlayers;", lep_tag[i]), 20, 0, 20);
    h_matchlep_nm1_nsigmadxy_[i] = fs->make<TH1F>(TString::Format("h_matchlep_nm1_nsigmadxy_%s", lep_tag[i]), TString::Format("; genmatched %s inSV nm1 nsigmadxy;", lep_tag[i]), 200, 0, 200);
    h_matchlep_genvtx_pos_[i] = fs->make<TH2F>(TString::Format("h_matchlep_genvtx_pos_%s", lep_tag[i]), ";genSV x (cm); genSV y (cm);", 100, -4, 4, 100, -4, 4);

    h_nomatchlep_dxy_[i] = fs->make<TH1F>(TString::Format("h_nomatchlep_dxy_%s", lep_tag[i]), TString::Format("; genmatched %s not inSV dxy;", lep_tag[i]), 150, 0, 3.0);
    h_nomatchlep_dxyerr_[i] = fs->make<TH1F>(TString::Format("h_nomatchlep_dxyerr_%s", lep_tag[i]), TString::Format("; genmatched %s not inSV dxyerr;", lep_tag[i]), 100, 0, 0.05);
    h_nomatchlep_nsigmadxy_[i] = fs->make<TH1F>(TString::Format("h_nomatchlep_nsigmadxy_%s", lep_tag[i]), TString::Format("; genmatched %s not inSV nsigmadxy;", lep_tag[i]), 200, 0, 200);
    h_nomatchlep_pt_[i] = fs->make<TH1F>(TString::Format("h_nomatchlep_pt_%s", lep_tag[i]), TString::Format("; genmatched %s not inSV pt;", lep_tag[i]), 200, 0, 1000);
    h_nomatchlep_nm1_minr_[i] = fs->make<TH1F>(TString::Format("h_nomatchlep_nm1_minr_%s", lep_tag[i]), TString::Format("; genmatched %s not inSV nm1 minr;", lep_tag[i]), 10, 0, 10);
    h_nomatchlep_nm1_npxlayers_[i] = fs->make<TH1F>(TString::Format("h_nomatchlep_nm1_npxlayers_%s", lep_tag[i]), TString::Format("; genmatched %s not inSV nm1 npxlayers;", lep_tag[i]), 20, 0, 20);
    h_nomatchlep_nm1_nstlayers_[i] = fs->make<TH1F>(TString::Format("h_nomatchlep_nm1_nstlayers_%s", lep_tag[i]), TString::Format("; genmatched %s not inSV nm1 nstlayers;", lep_tag[i]), 20, 0, 20);
    h_nomatchlep_nm1_nsigmadxy_[i] = fs->make<TH1F>(TString::Format("h_nomatchlep_nm1_nsigmadxy_%s", lep_tag[i]), TString::Format("; genmatched %s not inSV nm1 nsigmadxy;", lep_tag[i]), 200, 0, 200);
    h_nomatchlep_genvtx_pos_[i] = fs->make<TH2F>(TString::Format("h_nomatchlep_genvtx_pos_%s", lep_tag[i]), ";genSV x (cm); genSV y (cm);", 100, -4, 4, 100, -4, 4);

    h_nomatchlep_trkdR_[i] = fs->make<TH1F>(TString::Format("h_nomatchlep_trkdR_%s", lep_tag[i]), TString::Format("; deltaR between SV tracks and genmatched %s not inSV;", lep_tag[i]), 200, 0, 5.0);
    h_nomatchlep_missdist_[i] = fs->make<TH1F>(TString::Format("h_nomatchlep_missdist_%s", lep_tag[i]), TString::Format(";missdist btwn SV and genmatched %s not inSV;", lep_tag[i]), 150, 0, 3.0);
    h_nomatchlep_missdisterr_[i] = fs->make<TH1F>(TString::Format("h_nomatchlep_missdisterr_%s", lep_tag[i]), TString::Format(";missdisterr btwn SV and reco %s not inSV;", lep_tag[i]), 100, 0, 0.05);
    h_nomatchlep_missdistsig_[i] = fs->make<TH1F>(TString::Format("h_nomatchlep_missdistsig_%s", lep_tag[i]), TString::Format(";missdistsig btwn SV and reco %s not inSV;", lep_tag[i]), 200, 0, 100);
    h_matchlep_missdist_[i] = fs->make<TH1F>(TString::Format("h_matchlep_missdist_%s", lep_tag[i]), TString::Format(";missdist btwn SV and genmatched %s inSV;", lep_tag[i]), 150, 0, 3.0);
    h_matchlep_missdisterr_[i] = fs->make<TH1F>(TString::Format("h_matchlep_missdisterr_%s", lep_tag[i]), TString::Format(";missdisterr btwn SV and reco %s inSV;", lep_tag[i]), 100, 0, 0.05);
    h_matchlep_missdistsig_[i] = fs->make<TH1F>(TString::Format("h_matchlep_missdistsig_%s", lep_tag[i]), TString::Format(";missdistsig btwn SV and reco %s inSV;", lep_tag[i]), 200, 0, 100);
  }

  PairwiseHistos::HistoDefs hs;

  hs.add("x", "SV x (cm)", 100, -4, 4);
  hs.add("y", "SV y (cm)", 100, -4, 4);
  hs.add("z", "SV z (cm)", 100, -25, 25);
  hs.add("phi", "SV phi", 25, -3.15, 3.15);
  hs.add("phi_pv", "SV phi w.r.t. PV", 25, -3.15, 3.15);
  hs.add("cxx", "SV covariance xx (cm^{2})", 100, 0, 1e-5);
  hs.add("cxy", "SV covariance xy (cm^{2})", 100, -1e-5, 1e-5);
  hs.add("cxz", "SV covariance xz (cm^{2})", 100, -1e-5, 1e-5);
  hs.add("cyy", "SV covariance yy (cm^{2})", 100, 0, 1e-5);
  hs.add("cyz", "SV covariance yz (cm^{2})", 100, -1e-5, 1e-5);
  hs.add("czz", "SV covariance zz (cm^{2})", 100, 0, 1e-5);

  hs.add("rescale_chi2", "rescaled-fit SV x (cm)", 40, 0, 10);
  hs.add("rescale_x", "rescaled-fit SV x (cm)", 100, -4, 4);
  hs.add("rescale_y", "rescaled-fit SV y (cm)", 100, -4, 4);
  hs.add("rescale_z", "rescaled-fit SV z (cm)", 100, -25, 25);
  hs.add("rescale_cxx", "rescaled-fit SV covariance xx (cm^{2})", 100, 0, 1e-5);
  hs.add("rescale_cxy", "rescaled-fit SV covariance xy (cm^{2})", 100, -1e-5, 1e-5);
  hs.add("rescale_cxz", "rescaled-fit SV covariance xz (cm^{2})", 100, -1e-5, 1e-5);
  hs.add("rescale_cyy", "rescaled-fit SV covariance yy (cm^{2})", 100, 0, 1e-5);
  hs.add("rescale_cyz", "rescaled-fit SV covariance yz (cm^{2})", 100, -1e-5, 1e-5);
  hs.add("rescale_czz", "rescaled-fit SV covariance zz (cm^{2})", 100, 0, 1e-5);
  hs.add("rescale_dx", "rescaled-fit - nominal SV x (cm)", 100, -5e-4, 5e-4);
  hs.add("rescale_dy", "rescaled-fit - nominal SV y (cm)", 100, -5e-4, 5e-4);
  hs.add("rescale_dz", "rescaled-fit - nominal SV z (cm)", 100, -5e-4, 5e-4);
  hs.add("rescale_dx_big", "rescaled-fit - nominal SV x (cm)", 100, -4, 4);
  hs.add("rescale_dy_big", "rescaled-fit - nominal SV y (cm)", 100, -4, 4);
  hs.add("rescale_dz_big", "rescaled-fit - nominal SV z (cm)", 100, -4, 4);
  hs.add("rescale_d2", "rescaled-fit - nominal SV (2D) (cm)", 100, 0, 8e-4);
  hs.add("rescale_d2_big", "rescaled-fit - nominal SV (2D) (cm)", 100, 0, 4);
  hs.add("rescale_d3", "rescaled-fit - nominal SV (3D) (cm)", 100, 0, 1e-3);
  hs.add("rescale_d3_big", "rescaled-fit - nominal SV (3D) (cm)", 100, 0, 4);
  hs.add("rescale_bsbs2ddist", "rescaled-fit d_{BV} (cm)", 1000, 0, 2.5);
  hs.add("rescale_bs2derr", "rescaled-fit #sigma(dist2d(SV, beamspot)) (cm)", 1000, 0, 0.05);

  hs.add("max_nm1_refit_dist3_wbad", "maximum n-1 refit distance (3D) (cm)", 1001, -0.001, 1);
  hs.add("max_nm1_refit_dist3", "maximum n-1 refit distance (3D) (cm)", 1000, 0, 1);
  hs.add("max_nm1_refit_dist2", "maximum n-1 refit distance (2D) (cm)", 1000, 0, 1);
  hs.add("max_nm1_refit_distz", "maximum n-1 refit z distance (cm)", 1000, 0, 1);

  hs.add("ntracks",                       "# of tracks/SV",                                                               40,    0,      40);
  hs.add("ntracksptgt3",                  "# of tracks/SV w/ p_{T} > 3 GeV",                                              40,    0,      40);
  hs.add("ntracksptgt10",                 "# of tracks/SV w/ p_{T} > 10 GeV",                                             40,    0,      40);
  hs.add("ntracksetagt1p5",               "# of tracks/SV w/ |#eta| > 1.5",                                               40,    0,      40);
  hs.add("trackminnhits",                 "min number of hits on track per SV",                                           40,    0,      40);
  hs.add("trackmaxnhits",                 "max number of hits on track per SV",                                           40,    0,      40);
  hs.add("njetsntks",                     "# of jets assoc. by tracks to SV",                                             10,    0,      10);
  hs.add("nelensv",                       " # of ele assoc. to SV",                                                        5,    0,       5);
  hs.add("nmunsv",                        " # of mu assoc. to SV",                                                        10,    0,      10);
  hs.add("nlepnsv",                       " # of leptons assoc. to SV",                                                   10,    0,      10);
  hs.add("chi2dof",                       "SV #chi^2/dof",                                                                50,    0,       7);
  hs.add("chi2dofprob",                   "SV p(#chi^2, dof)",                                                            50,    0,       1.2);

  hs.add("tkonlyp",                       "SV tracks-only p (GeV)",                                                       50,    0,     500);
  hs.add("tkonlypt",                      "SV tracks-only p_{T} (GeV)",                                                   50,    0,     400);
  hs.add("tkonlyeta",                     "SV tracks-only #eta",                                                          50,   -4,       4);
  hs.add("tkonlyrapidity",                "SV tracks-only rapidity",                                                      50,   -4,       4);
  hs.add("tkonlyphi",                     "SV tracks-only #phi",                                                          50,   -3.15,    3.15);
  hs.add("tkonlymass",                    "SV tracks-only mass (GeV)",                                                   100,    0,    1000);

  hs.add("jetsntkp",                      "SV jets-by-ntracks -only p (GeV)",                                             50,    0,    1000);
  hs.add("jetsntkpt",                     "SV jets-by-ntracks -only p_{T} (GeV)",                                         50,    0,    1000);
  hs.add("jetsntketa",                    "SV jets-by-ntracks -only #eta",                                                50,   -4,       4);
  hs.add("jetsntkrapidity",               "SV jets-by-ntracks -only rapidity",                                            50,   -4,       4);
  hs.add("jetsntkphi",                    "SV jets-by-ntracks -only #phi",                                                50,   -3.15,    3.15);
  hs.add("jetsntkmass",                   "SV jets-by-ntracks -only mass (GeV)",                                          50,    0,    2000);

  hs.add("tksjetsntkp",                   "SV tracks-plus-jets-by-ntracks p (GeV)",                                       50,    0,    1000);
  hs.add("tksjetsntkpt",                  "SV tracks-plus-jets-by-ntracks p_{T} (GeV)",                                   50,    0,    1000);
  hs.add("tksjetsntketa",                 "SV tracks-plus-jets-by-ntracks #eta",                                          50,   -4,       4);
  hs.add("tksjetsntkrapidity",            "SV tracks-plus-jets-by-ntracks rapidity",                                      50,   -4,       4);
  hs.add("tksjetsntkphi",                 "SV tracks-plus-jets-by-ntracks #phi",                                          50,   -3.15,    3.15);
  hs.add("tksjetsntkmass",                "SV tracks-plus-jets-by-ntracks mass (GeV)",                                   100,    0,    5000);
				        
  hs.add("costhtkonlymombs",              "cos(angle(2-momentum (tracks-only), 2-dist to BS))",                           21,   -1,       1.1);
  hs.add("costhtkonlymompv2d",            "cos(angle(2-momentum (tracks-only), 2-dist to PV))",                           21,   -1,       1.1);
  hs.add("costhtkonlymompv3d",            "cos(angle(3-momentum (tracks-only), 3-dist to PV))",                           21,   -1,       1.1);

  hs.add("costhtksjetsntkmombs",          "cos(angle(2-momentum (tracks-plus-jets-by-ntracks), 2-dist to BS))",          21,   -1,       1.1);
  hs.add("costhtksjetsntkmompv2d",        "cos(angle(2-momentum (tracks-plus-jets-by-ntracks), 2-dist to PV))",          21,   -1,       1.1);
  hs.add("costhtksjetsntkmompv3d",        "cos(angle(3-momentum (tracks-plus-jets-by-ntracks), 3-dist to PV))",          21,   -1,       1.1);

  hs.add("missdisttkonlypv",              "miss dist. (tracks-only) of SV to PV (cm)",                                   100,    0,       2);
  hs.add("missdisttkonlypverr",           "#sigma(miss dist. (tracks-only) of SV to PV) (cm)",                           100,    0,       0.05);
  hs.add("missdisttkonlypvsig",           "N#sigma(miss dist. (tracks-only) of SV to PV) (cm)",                          100,    0,     100);

  hs.add("missdisttksjetsntkpv",          "miss dist. (tracks-plus-jets-by-ntracks) of SV to PV (cm)",                   100,    0,       2);
  hs.add("missdisttksjetsntkpverr",       "#sigma(miss dist. (tracks-plus-jets-by-ntracks) of SV to PV) (cm)",           100,    0,       0.05);
  hs.add("missdisttksjetsntkpvsig",       "N#sigma(miss dist. (tracks-plus-jets-by-ntracks) of SV to PV) (cm)",          100,    0,     100);

					  
  hs.add("sumpt2",                        "SV #Sigma p_{T}^{2} (GeV^2)",                                                  50,    0,    10000);

  hs.add("ntrackssharedwpv",  "number of tracks shared with the PV", 30, 0, 30);
  hs.add("ntrackssharedwpvs", "number of tracks shared with any PV", 30, 0, 30);
  hs.add("fractrackssharedwpv",  "fraction of tracks shared with the PV", 41, 0, 1.025);
  hs.add("fractrackssharedwpvs", "fraction of tracks shared with any PV", 41, 0, 1.025);
  hs.add("npvswtracksshared", "number of PVs having tracks shared",  30, 0, 30);
  
  hs.add("trackdxymin", "SV min{trk_{i} dxy(BS)} (cm)", 50, 0, 0.2);
  hs.add("trackdxymax", "SV max{trk_{i} dxy(BS)} (cm)", 50, 0, 2);
  hs.add("trackdxyavg", "SV avg{trk_{i} dxy(BS)} (cm)", 50, 0, 0.5);
  hs.add("trackdxyrms", "SV rms{trk_{i} dxy(BS)} (cm)", 50, 0, 0.5);

  hs.add("trackdzmin", "SV min{trk_{i} dz(PV)} (cm)", 50, 0, 0.5);
  hs.add("trackdzmax", "SV max{trk_{i} dz(PV)} (cm)", 50, 0, 2);
  hs.add("trackdzavg", "SV avg{trk_{i} dz(PV)} (cm)", 50, 0, 1);
  hs.add("trackdzrms", "SV rms{trk_{i} dz(PV)} (cm)", 50, 0, 0.5);

  hs.add("trackpterrmin", "SV min{frac. #sigma trk_{i} p_{T}}", 32, 0, 2);
  hs.add("trackpterrmax", "SV max{frac. #sigma trk_{i} p_{T}}", 32, 0, 2);
  hs.add("trackpterravg", "SV avg{frac. #sigma trk_{i} p_{T}}", 32, 0, 2);
  hs.add("trackpterrrms", "SV rms{frac. #sigma trk_{i} p_{T}}", 32, 0, 2);

  hs.add("tracketaerrmin", "SV min{frac. #sigma trk_{i} #eta}", 32, 0, 0.002);
  hs.add("tracketaerrmax", "SV max{frac. #sigma trk_{i} #eta}", 32, 0, 0.005);
  hs.add("tracketaerravg", "SV avg{frac. #sigma trk_{i} #eta}", 32, 0, 0.002);
  hs.add("tracketaerrrms", "SV rms{frac. #sigma trk_{i} #eta}", 32, 0, 0.002);

  hs.add("trackphierrmin", "SV min{frac. #sigma trk_{i} #phi}", 32, 0, 0.002);
  hs.add("trackphierrmax", "SV max{frac. #sigma trk_{i} #phi}", 32, 0, 0.005);
  hs.add("trackphierravg", "SV avg{frac. #sigma trk_{i} #phi}", 32, 0, 0.002);
  hs.add("trackphierrrms", "SV rms{frac. #sigma trk_{i} #phi}", 32, 0, 0.002);

  hs.add("trackdxynsigmamin", "SV min{N #sigma trk_{i} dxy(BS)} (cm)", 50, 0, 10);
  hs.add("trackdxynsigmamax", "SV max{N #sigma trk_{i} dxy(BS)} (cm)", 50, 0, 10);
  hs.add("trackdxynsigmaavg", "SV avg{N #sigma trk_{i} dxy(BS)} (cm)", 50, 0, 10);
  hs.add("trackdxynsigmarms", "SV rms{N #sigma trk_{i} dxy(BS)} (cm)", 50, 0, 10);

  hs.add("trackdxyerrmin", "SV min{#sigma trk_{i} dxy(BS)} (cm)", 32, 0, 0.004);
  hs.add("trackdxyerrmax", "SV max{#sigma trk_{i} dxy(BS)} (cm)", 32, 0, 0.1);
  hs.add("trackdxyerravg", "SV avg{#sigma trk_{i} dxy(BS)} (cm)", 32, 0, 0.1);
  hs.add("trackdxyerrrms", "SV rms{#sigma trk_{i} dxy(BS)} (cm)", 32, 0, 0.1);

  hs.add("trackdzerrmin", "SV min{#sigma trk_{i} dz(PV)} (cm)", 32, 0, 0.01);
  hs.add("trackdzerrmax", "SV max{#sigma trk_{i} dz(PV)} (cm)", 32, 0, 0.1);
  hs.add("trackdzerravg", "SV avg{#sigma trk_{i} dz(PV)} (cm)", 32, 0, 0.1);
  hs.add("trackdzerrrms", "SV rms{#sigma trk_{i} dz(PV)} (cm)", 32, 0, 0.1);

  hs.add("trackpairdetamin", "SV min{#Delta #eta(i,j)}", 150,    0,       1.5);
  hs.add("trackpairdetamax", "SV max{#Delta #eta(i,j)}", 150,    0,       7);
  hs.add("trackpairdetaavg", "SV avg{#Delta #eta(i,j)}", 150,    0,       5);
  hs.add("trackpairdetarms", "SV rms{#Delta #eta(i,j)}", 150,    0,       3);

  hs.add("trackpairdphimax",   "SV max{|#Delta #phi(i,j)|}",   100, 0, 3.15);
  hs.add("trackpairdphimaxm1", "SV max-1{|#Delta #phi(i,j)|}", 100, 0, 3.15);
  hs.add("trackpairdphimaxm2", "SV max-2{|#Delta #phi(i,j)|}", 100, 0, 3.15);

  hs.add("trackpairdrmin", "SV min{#Delta R(i,j)}", 150, 0, 1.5);
  hs.add("trackpairdrmax", "SV max{#Delta R(i,j)}", 150, 0, 7);
  hs.add("trackpairdravg", "SV avg{#Delta R(i,j)}", 150, 0, 5);
  hs.add("trackpairdrrms", "SV rms{#Delta R(i,j)}", 150, 0, 3);

  hs.add("costhtkmomvtxdispmin", "SV min{cos(angle(trk_{i}, SV-PV))}", 50, -1, 1);
  hs.add("costhtkmomvtxdispmax", "SV max{cos(angle(trk_{i}, SV-PV))}", 50, -1, 1);
  hs.add("costhtkmomvtxdispavg", "SV avg{cos(angle(trk_{i}, SV-PV))}", 50, -1, 1);
  hs.add("costhtkmomvtxdisprms", "SV rms{cos(angle(trk_{i}, SV-PV))}", 50,  0, 1);

  hs.add("costhjetmomvtxdispmin", "SV min{cos(angle(jet_{i}, SV-PV))}", 50, -1, 1);
  hs.add("costhjetmomvtxdispmax", "SV max{cos(angle(jet_{i}, SV-PV))}", 50, -1, 1);
  hs.add("costhjetmomvtxdispavg", "SV avg{cos(angle(jet_{i}, SV-PV))}", 50, -1, 1);
  hs.add("costhjetmomvtxdisprms", "SV rms{cos(angle(jet_{i}, SV-PV))}", 50,  0, 1);

  hs.add("multipv_maxdz",    "max #Delta z of PV w tracks shared (cm)", 100, 0, 10);
  hs.add("multipvbyz_maxdz", "max #Delta z of PV w track-assoc-by-z (cm)", 100, 0, 10);

  hs.add("gen2ddist",                     "dist2d(SV, closest gen vtx) (cm)",                                            200,    0,       0.2);
  hs.add("gen2derr",                      "#sigma(dist2d(SV, closest gen vtx)) (cm)",                                    200,    0,       0.2);
  hs.add("gen2dsig",                      "N#sigma(dist2d(SV, closest gen vtx)) (cm)",                                   200,    0,     100);
  hs.add("gen3ddist",                     "dist3d(SV, closest gen vtx) (cm)",                                            200,    0,       0.2);
  hs.add("gen3derr",                      "#sigma(dist3d(SV, closest gen vtx)) (cm)",                                    200,    0,       0.2);
  hs.add("gen3dsig",                      "N#sigma(dist3d(SV, closest gen vtx)) (cm)",                                   200,    0,     100);
  hs.add("bs2ddist",                      "dist2d(SV, beamspot) (cm)",                                                  1000,    0,      2.5);
  hs.add("bsbs2ddist",                    "dist2d(SV, beamspot) (cm)",                                                  1000,    0,      2.5);
  hs.add("bs2derr",                       "#sigma(dist2d(SV, beamspot)) (cm)",                                           1000,    0,       0.05);
  hs.add("bs2dsig",                       "N#sigma(dist2d(SV, beamspot))",                                               100,    0,     100);
  hs.add("pv2ddist",                      "dist2d(SV, PV) (cm)",                                                         100,    0,       0.5);
  hs.add("pv2derr",                       "#sigma(dist2d(SV, PV)) (cm)",                                                 100,    0,       0.05);
  hs.add("pv2dsig",                       "N#sigma(dist2d(SV, PV))",                                                     100,    0,     100);
  hs.add("pv3ddist",                      "dist3d(SV, PV) (cm)",                                                         100,    0,       0.5);
  hs.add("pv3derr",                       "#sigma(dist3d(SV, PV)) (cm)",                                                 100,    0,       0.1);
  hs.add("pv3dsig",                       "N#sigma(dist3d(SV, PV))",                                                     100,    0,     100);
  hs.add("pvdz",                          "dz(SV, PV) (cm)",                                                             100,    0,       0.5);
  hs.add("pvdzerr",                       "#sigma(dz(SV, PV)) (cm)",                                                     100,    0,       0.1);
  hs.add("pvdzsig",                       "N#sigma(dz(SV, PV))",                                                         100,    0,     100);


  const char* lmt_ex[4] = {"", "loose b-", "medium b-", "tight b-"};
  for (int i = 0; i < 4; ++i) {
    hs.add(TString::Format("jet%d_deltaphi0", i), TString::Format("|#Delta#phi| to closest %sjet", lmt_ex[i]),      25, 0, 3.15);
    hs.add(TString::Format("jet%d_deltaphi1", i), TString::Format("|#Delta#phi| to next closest %sjet", lmt_ex[i]), 25, 0, 3.15);
  }

  for (int i = 0; i < max_ntrackplots; ++i) {
    hs.add(TString::Format("track%i_weight",        i), TString::Format("track%i weight",                      i),  21,  0,      1.05);
    hs.add(TString::Format("track%i_q",             i), TString::Format("track%i charge",                      i),   4, -2,      2);
    hs.add(TString::Format("track%i_pt",            i), TString::Format("track%i p_{T} (GeV)",                 i), 200,  0,    200);
    hs.add(TString::Format("track%i_eta",           i), TString::Format("track%i #eta",                        i),  50, -4,      4);
    hs.add(TString::Format("track%i_phi",           i), TString::Format("track%i #phi",                        i),  50, -3.15,   3.15);
    hs.add(TString::Format("track%i_dxy",           i), TString::Format("track%i dxy (cm)",                    i), 100,  0,      1);
    hs.add(TString::Format("track%i_dz",            i), TString::Format("track%i dz (cm)",                     i), 100,  0,      1);
    hs.add(TString::Format("track%i_pt_err",        i), TString::Format("track%i #sigma(p_{T})/p_{T}",         i), 200,  0,      2);
    hs.add(TString::Format("track%i_eta_err",       i), TString::Format("track%i #sigma(#eta)",                i), 200,  0,      0.02);
    hs.add(TString::Format("track%i_phi_err",       i), TString::Format("track%i #sigma(#phi)",                i), 200,  0,      0.02);
    hs.add(TString::Format("track%i_dxy_err",       i), TString::Format("track%i #sigma(dxy) (cm)",            i), 100,  0,      0.1);
    hs.add(TString::Format("track%i_dz_err",        i), TString::Format("track%i #sigma(dz) (cm)",             i), 100,  0,      0.1);
    hs.add(TString::Format("track%i_nsigmadxy",     i), TString::Format("track%i n#sigma(dxy)",                i), 400,  0,     40);
    hs.add(TString::Format("track%i_chi2dof",       i), TString::Format("track%i #chi^{2}/dof",                i), 100,  0,     10);
    hs.add(TString::Format("track%i_npxhits",       i), TString::Format("track%i number of pixel hits",        i),  12,  0,     12);
    hs.add(TString::Format("track%i_nsthits",       i), TString::Format("track%i number of strip hits",        i),  28,  0,     28);
    hs.add(TString::Format("track%i_nhitsbehind",   i), TString::Format("track%i number of hits behind",       i),  10,  0,     10);
    hs.add(TString::Format("track%i_nhitslost",     i), TString::Format("track%i number of hits lost",         i),  10,  0,     10);
    hs.add(TString::Format("track%i_nhits",         i), TString::Format("track%i number of hits",              i),  40,  0,     40);
    hs.add(TString::Format("track%i_injet",         i), TString::Format("track%i in-jet?",                     i),   2,  0,      2);
    hs.add(TString::Format("track%i_inpv",          i), TString::Format("track%i in-PV?",                      i),  10, -1,      9);
    hs.add(TString::Format("track%i_jet_deltaphi0", i), TString::Format("track%i |#Delta#phi| to closest jet", i),  25,  0,      3.15);

    hs.add(TString::Format("eletrack%i_pt",         i), TString::Format("p_{T} of ele track%i assoc to SV (GeV)", i),   200,      0,     1000);
    hs.add(TString::Format("eletrack%i_eta",        i), TString::Format("eta of ele track%i assoc to SV",         i),    50,     -4,       4);
    hs.add(TString::Format("eletrack%i_phi",        i), TString::Format("phi of ele track%i assoc to SV",         i),    50,  -3.15,    3.15);
    hs.add(TString::Format("eletrack%i_dxy",        i), TString::Format("dxy (cm) of ele track%i assoc to SV",    i),   200,   -2.0,     2.0);
    hs.add(TString::Format("eletrack%i_iso",        i), TString::Format("iso of ele track%i assoc to SV",         i),   100,      0,     2.0);
    hs.add(TString::Format("eletrack%i_ID",         i), TString::Format("ID of ele track%i assoc to SV",          i),     5,      0,       5);
    // hs.add(TString::Format("alleletrack%i_tip",    i), TString::Format("transverse IP of all ele track%i to SV", i), 100,    0,       2.0);
    // hs.add(TString::Format("alleletrack%i_tiperr", i), TString::Format("transverse IP err of all ele track%i to SV", i), 100,    0,       0.05);
    // hs.add(TString::Format("alleletrack%i_tipsig", i), TString::Format("transverse IP sig. of all ele track%i to SV", i),  100,   0,   100);
    // hs.add(TString::Format("matchedeletrack%i_tip",  i), TString::Format("transverse IP of ele track%i assoc to SV", i), 100,    0,       2.0);
    // hs.add(TString::Format("matchedeletrack%i_tiperr", i), TString::Format("transverse IP err of ele track%i assoc to SV", i), 100,    0,       0.05);
    // hs.add(TString::Format("matchedeletrack%i_tipsig", i), TString::Format("transverse IP sig. of ele track%i assoc to SV", i),  100,   0,   100);


    hs.add(TString::Format("mutrack%i_pt",          i), TString::Format("p_{T} of mu track%i assoc to SV (GeV)",  i),  200,      0,    1000);
    hs.add(TString::Format("mutrack%i_eta",         i), TString::Format("eta of mu track%i assoc to SV",          i),   50,     -4,       4);
    hs.add(TString::Format("mutrack%i_phi",         i), TString::Format("phi of mu track%i assoc to SV",          i),   50,  -3.15,    3.15);
    hs.add(TString::Format("mutrack%i_dxy",         i), TString::Format("dxy (cm) of mu track%i assoc to SV",     i),  200,   -2.0,     2.0);
    hs.add(TString::Format("mutrack%i_iso",         i), TString::Format("iso of mu track%i assoc to SV",          i),  100,      0,     2.0);
    hs.add(TString::Format("mutrack%i_ID",          i), TString::Format("ID of mu track%i assoc to SV",           i),    4,      0,      4);
    // hs.add(TString::Format("allmutrack%i_tip",     i), TString::Format("transverse IP of all mu track%i to SV", i),  100,      0,     2.0);
    // hs.add(TString::Format("allmutrack%i_tiperr",  i), TString::Format("transverse IP err of all mu track%i to SV", i),  100,      0,     0.05);
    // hs.add(TString::Format("allmutrack%i_tipsig",  i), TString::Format("transverse IP sig. of all mu track%i to SV", i),  100,   0,     100);
    // hs.add(TString::Format("matchedmutrack%i_tip",   i), TString::Format("transverse IP of mu track%i assoc to SV", i),  100,      0,     2.0);
    // hs.add(TString::Format("matchedmutrack%i_tiperr", i), TString::Format("transverse IP err of mu track%i assoc to SV", i),  100,      0,     0.05);
    // hs.add(TString::Format("matchedmutrack%i_tipsig", i), TString::Format("transverse IP sig. of mu track%i assoc to SV", i),  100,   0,     100);

  }

  for (int j = 0; j < sv_num_indices; ++j) {
    const char* exc = sv_index_names[j];

    h_sv[j].Init("h_sv_" + std::string(exc), hs, true, do_scatterplots);

    for (int i = 0; i < 4; ++i)
      h_sv_jets_deltaphi[i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%sjets_deltaphi", exc, lmt_ex[i]), TString::Format(";%s SV #Delta#phi to %sjets;arb. units", exc, lmt_ex[i]), 50, -3.15, 3.15);

    h_sv_bs2derr_bsbs2ddist[j] = fs->make<TH2F>(TString::Format("h_sv_%s_bs2derr_bsbs2ddist", exc), TString::Format("%s SV;dist2d(SV, beamspot) (cm);#sigma(dist2d(SV, beamspot)) (cm)", exc), 500, 0, 2.5, 100, 0, 0.05);
    h_pvrho_bsbs2ddist[j] = fs->make<TH2F>(TString::Format("h_pvrho_sv_%s_bsbs2ddist", exc), TString::Format("%s SV;dist2d(SV, beamspot) (cm);dist2d(PV, beamspot)) (cm)", exc), 5000, 0, 2.5, 200, 0, 0.1);

    h_sv_track_weight[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_weight", exc), TString::Format(";%s SV tracks weight;arb. units", exc), 21, 0, 1.05);
    h_sv_track_q[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_q", exc), TString::Format(";%s SV tracks charge;arb. units.", exc), 4, -2, 2);
    h_sv_track_pt[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_pt", exc), TString::Format(";%s SV tracks p_{T} (GeV);arb. units", exc), 200, 0, 200);
    h_sv_track_eta[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_eta", exc), TString::Format(";%s SV tracks #eta;arb. units", exc), 50, -4, 4);
    h_sv_track_phi[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_phi", exc), TString::Format(";%s SV tracks #phi;arb. units", exc), 50, -3.15, 3.15);
    h_sv_track_dxy[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_dxy", exc), TString::Format(";%s SV tracks dxy (cm);arb. units", exc), 100, 0, 1);
    h_sv_track_dz[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_dz", exc), TString::Format(";%s SV tracks dz (cm);arb. units", exc), 100, 0, 1);
    h_sv_track_pt_err[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_pt_err", exc), TString::Format(";%s SV tracks #sigma(p_{T})/p_{T};arb. units", exc), 200, 0, 2);
    h_sv_track_eta_err[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_eta_err", exc), TString::Format(";%s SV tracks #sigma(#eta);arb. units", exc), 200, 0, 0.02);
    h_sv_track_phi_err[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_phi_err", exc), TString::Format(";%s SV tracks #sigma(#phi);arb. units", exc), 200, 0, 0.02);
    h_sv_track_dxy_err[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_dxy_err", exc), TString::Format(";%s SV tracks #sigma(dxy) (cm);arb. units", exc), 100, 0, 0.1);
    h_sv_track_dz_err[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_dz_err", exc), TString::Format(";%s SV tracks #sigma(dz) (cm);arb. units", exc), 100, 0, 0.1);
    h_sv_track_nsigmadxy[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_nsigmadxy", exc), TString::Format(";%s SV tracks n#sigma(dxy);arb. units", exc), 400, 0, 40);
    h_sv_track_chi2dof[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_chi2dof", exc), TString::Format(";%s SV tracks #chi^{2}/dof;arb. units", exc), 100, 0, 10);
    h_sv_track_npxhits[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_npxhits", exc), TString::Format(";%s SV tracks number of pixel hits;arb. units", exc), 12, 0, 12);
    h_sv_track_nsthits[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_nsthits", exc), TString::Format(";%s SV tracks number of strip hits;arb. units", exc), 28, 0, 28);
    h_sv_track_nhitsbehind[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_nhitsbehind", exc), TString::Format(";%s SV tracks number of hits behind;arb. units", exc), 10, 0, 10);
    h_sv_track_nhitslost[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_nhitslost", exc), TString::Format(";%s SV tracks number of hits lost;arb. units", exc), 10, 0, 10);
    h_sv_track_nhits[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_nhits", exc), TString::Format(";%s SV tracks number of hits", exc), 40, 0, 40);
    h_sv_track_injet[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_injet", exc), TString::Format(";%s SV tracks in-jet?", exc), 2, 0, 2);
    h_sv_track_inpv[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_inpv", exc), TString::Format(";%s SV tracks in-PV?", exc), 10, -1, 9);
  
    h_sv_eletrack_pt[j] = fs->make<TH1F>(TString::Format("h_sv_%s_eletrack_pt", exc), TString::Format(";%s SV assoc. electron p_{T} (GeV);arb. units", exc), 200, 0, 1000);
    h_sv_eletrack_eta[j] = fs->make<TH1F>(TString::Format("h_sv_%s_eletrack_eta", exc), TString::Format(";%s SV assoc. electron #eta;arb. units", exc), 50, -4, 4);
    h_sv_eletrack_phi[j] = fs->make<TH1F>(TString::Format("h_sv_%s_eletrack_phi", exc), TString::Format(";%s SV assoc. electron #phi;arb. units", exc), 50, -3.15, 3.15);
    h_sv_eletrack_dxy[j] = fs->make<TH1F>(TString::Format("h_sv_%s_eletrack_dxy", exc), TString::Format(";%s SV assoc. electron dxy (cm);arb. units", exc), 200, -2.0, 2.0);
    h_sv_eletrack_iso[j] = fs->make<TH1F>(TString::Format("h_sv_%s_eletrack_iso", exc), TString::Format(";%s SV assoc. electron iso;arb. units", exc), 100, 0, 2.0);
    h_sv_eletrack_ID[j] = fs->make<TH1F>(TString::Format("h_sv_%s_eletrack_ID", exc), TString::Format(";%s SV assoc. electron ID;arb. units", exc), 5, 0, 5);
    // h_sv_matchedeletrack_tip[j] = fs->make<TH1F>(TString::Format("h_sv_%s_matchedeletrack_tip", exc), TString::Format(";%s SV - assoc. electron transverse impact parameter; arb. units", exc), 100, 0, 2.0);
    // h_sv_matchedeletrack_tiperr[j] = fs->make<TH1F>(TString::Format("h_sv_%s_matchedeletrack_tiperr", exc), TString::Format(";%s SV - assoc. electron transverse impact parameter err; arb. units", exc), 100, 0, 0.05);
    // h_sv_matchedeletrack_tipsig[j] = fs->make<TH1F>(TString::Format("h_sv_%s_matcheledetrack_tipsig", exc), TString::Format(";%s SV - assoc. electron transverse impact parameter sig.; arb. units", exc), 100, 0, 100);
    // h_sv_alleletrack_tip[j] = fs->make<TH1F>(TString::Format("h_sv_%s_alleletrack_tip", exc), TString::Format(";%s SV - electron transverse impact parameter; arb. units", exc), 100, 0, 2.0);
    // h_sv_alleletrack_tiperr[j] = fs->make<TH1F>(TString::Format("h_sv_%s_alleletrack_tiperr", exc), TString::Format(";%s SV - electron transverse impact parameter err; arb. units", exc), 100, 0, 0.05);
    // h_sv_alleletrack_tipsig[j] = fs->make<TH1F>(TString::Format("h_sv_%s_alleletrack_tipsig", exc), TString::Format(";%s SV - electron transverse impact parameter sig.; arb. units", exc), 100, 0, 100);

    h_sv_mutrack_pt[j] = fs->make<TH1F>(TString::Format("h_sv_%s_mutrack_pt", exc), TString::Format(";%s SV assoc. muon p_{T} (GeV);arb. units", exc), 200, 0, 1000);
    h_sv_mutrack_eta[j] = fs->make<TH1F>(TString::Format("h_sv_%s_mutrack_eta", exc), TString::Format(";%s SV assoc. muon #eta;arb. units", exc), 50, -4, 4);
    h_sv_mutrack_phi[j] = fs->make<TH1F>(TString::Format("h_sv_%s_mutrack_phi", exc), TString::Format(";%s SV assoc. muon #phi;arb. units", exc), 50, -3.15, 3.15);
    h_sv_mutrack_dxy[j] = fs->make<TH1F>(TString::Format("h_sv_%s_mutrack_dxy", exc), TString::Format(";%s SV assoc. muon dxy (cm);arb. units", exc), 200, -2.0, 2.0);
    h_sv_mutrack_iso[j] = fs->make<TH1F>(TString::Format("h_sv_%s_mutrack_iso", exc), TString::Format(";%s SV assoc. muon iso;arb. units", exc), 1000, 0, 2.0);
    h_sv_mutrack_ID[j] = fs->make<TH1F>(TString::Format("h_sv_%s_mutrack_ID", exc), TString::Format(";%s SV assoc. muon ID;arb. units", exc), 4, 0, 4);
    // h_sv_matchedmutrack_tip[j] = fs->make<TH1F>(TString::Format("h_sv_%s_matchedmutrack_tip", exc), TString::Format(";%s SV - assoc. muon transverse impact parameter; arb. units", exc), 100, 0, 2.0);
    // h_sv_matchedmutrack_tiperr[j] = fs->make<TH1F>(TString::Format("h_sv_%s_matchedmutrack_tiperr", exc), TString::Format(";%s SV - assoc. muon transverse impact parameter err; arb. units", exc), 100, 0, 0.05);
    // h_sv_matchedmutrack_tipsig[j] = fs->make<TH1F>(TString::Format("h_sv_%s_matchedmutrack_tipsig", exc), TString::Format(";%s SV - assoc. muon transverse impact parameter sig.; arb. units", exc), 100, 0, 100);
    // h_sv_allmutrack_tip[j] = fs->make<TH1F>(TString::Format("h_sv_%s_allmutrack_tip", exc), TString::Format(";%s SV - muon transverse impact parameter; arb. units", exc), 100, 0, 2.0);
    // h_sv_allmutrack_tiperr[j] = fs->make<TH1F>(TString::Format("h_sv_%s_allmutrack_tiperr", exc), TString::Format(";%s SV - muon transverse impact parameter err; arb. units", exc), 100, 0, 0.05);
    // h_sv_allmutrack_tipsig[j] = fs->make<TH1F>(TString::Format("h_sv_%s_allmutrack_tipsig", exc), TString::Format(";%s SV - muon transverse impact parameter sig.; arb. units", exc), 100, 0, 100);
  }

  h_sv_gen2ddist_signed = fs->make<TH1F>("h_sv_gen2ddist_signed", ";dist2d(SV, closest gen vtx) (cm);arb. units", 400,-0.2,0.2);
  h_sv_ntk_genbs2ddist = fs->make<TH2F>("h_sv_ntk_genbs2ddist", ";# tracks of SV;dist2d(gen vtx, beamspot) (cm)",40,0,40,500,0,2.5);
  h_sv_ntk_bs2ddist = fs->make<TH2F>("h_sv_ntk_bs2ddist", ";# tracks of SV;dist2d(SV, beamspot) (cm)",40,0,40,500,0,2.5);
  h_sv_ntk_gen2ddist = fs->make<TH2F>("h_sv_ntk_gen2ddist", ";# tracks of SV;dist2d(SV, closest gen vtx) (cm)",40,0,40,200,0,0.2);
  h_sv_nsv_nmatchjet = fs->make<TH2F>("h_sv_nsv_nmatchjet", ";# jets matched with gen quarks;# SV", 10, 0, 10, 10, 0, 10);


  h_sv_ntk_njet = fs->make<TH2F>("h_sv_ntk_njet", "; # tracks of SV; # associated jets of SV", 40,0,40,10,0,10);
  h_sv_ntk0_ntk1 = fs->make<TH2F>("h_sv_ntk0_ntk1", "; # tracks of SV0; # tracks of SV1", 40,0,40,40,0,40);
  h_sv_xy = fs->make<TH2F>("h_sv_xy", ";SV x (cm);SV y (cm)", 100, -4, 4, 100, -4, 4);
  h_sv_xz = fs->make<TH2F>("h_sv_xz", ";SV x (cm);SV z (cm)", 100, -4, 4, 100, -25, 25);
  h_sv_yz = fs->make<TH2F>("h_sv_yz", ";SV y (cm);SV z (cm)", 100, -4, 4, 100, -25, 25);
  h_sv_rz = fs->make<TH2F>("h_sv_rz", ";SV r (cm);SV z (cm)", 100, -4, 4, 100, -25, 25);
  h_svdist2d = fs->make<TH1F>("h_svdist2d", ";dist2d(sv #0, #1) (cm);arb. units", 500, 0, 1);
  h_svdist3d = fs->make<TH1F>("h_svdist3d", ";dist3d(sv #0, #1) (cm);arb. units", 500, 0, 1);
  h_sv0pvdz_v_sv1pvdz = fs->make<TH2F>("h_sv0pvdz_v_sv1pvdz", ";sv #1 dz to PV (cm);sv #0 dz to PV (cm)", 100, 0, 0.5, 100, 0, 0.5);
  h_sv0pvdzsig_v_sv1pvdzsig = fs->make<TH2F>("h_sv0pvdzsig_v_sv1pvdzsig", ";N#sigma(sv #1 dz to PV);sv N#sigma(#0 dz to PV)", 100, 0, 50, 100, 0, 50);
  h_absdeltaphi01 = fs->make<TH1F>("h_absdeltaphi01", ";abs(delta(phi of sv #0, phi of sv #1));arb. units", 315, 0, 3.15);
  h_fractrackssharedwpv01 = fs->make<TH1F>("h_fractrackssharedwpv01", ";fraction of sv #0 and sv #1 tracks shared with the PV;arb. units", 41, 0, 1.025);
  h_fractrackssharedwpvs01 = fs->make<TH1F>("h_fractrackssharedwpvs01", ";fraction of sv #0 and sv #1 tracks shared with any PV;arb. units", 41, 0, 1.025);
  h_pvmosttracksshared = fs->make<TH2F>("h_pvmosttracksshared", ";index of pv most-shared to sv #0; index of pv most-shared to sv #1", 71, -1, 70, 71, -1, 70);
  h_sv_shared_jets  = fs->make<TH1F>("h_sv_shared_jets", ";SV tracks share jet?", 2, 0, 2);
  h_svdist2d_shared_jets = fs->make<TH1F>("h_svdist2d_shared_jets", ";dist2d(sv #0, #1) (cm);arb. units", 500, 0, 1);
  h_svdist2d_no_shared_jets = fs->make<TH1F>("h_svdist2d_no_shared_jets", ";dist2d(sv #0, #1) (cm);arb. units", 500, 0, 1);
  h_absdeltaphi01_shared_jets = fs->make<TH1F>("h_absdeltaphi01_shared_jets", ";abs(delta(phi of sv #0, phi of sv #1));arb. units", 316, 0, 3.16);
  h_absdeltaphi01_no_shared_jets = fs->make<TH1F>("h_absdeltaphi01_no_shared_jets", ";abs(delta(phi of sv #0, phi of sv #1));arb. units", 316, 0, 3.16);
}

Measurement1D MFVVertexHistos::miss_dist(const math::XYZPoint& pv, const math::XYZPoint& sv, const math::XYZPoint& lep, const double pv_arr [9], const double sv_arr [9]) {

  // miss distance is magnitude of (lepton direction (= n) cross (tv - sv) ( = d))
  // to calculate uncertainty, use |n X d|^2 = (|n||d|)^2 - (n . d)^2 
  // returns the unit vector -> to get the direction 
  AlgebraicVector3 n = ROOT::Math::Unit(AlgebraicVector3(lep.x(), lep.y(), lep.z()));
  ROOT::Math::SMatrix<double, 3> svcov(sv_arr,9);
  ROOT::Math::SMatrix<double, 3> pvcov(pv_arr,9);


  AlgebraicVector3 d(sv.x() - pv.x(),
                     sv.y() - pv.y(),
                     sv.z() - pv.z());
  AlgebraicVector3 n_cross_d = ROOT::Math::Cross(n,d);
  double n_dot_d = ROOT::Math::Dot(n,d);
  double val = ROOT::Math::Mag(n_cross_d);

  AlgebraicVector3 jac(2*d(0) - 2*n_dot_d*n(0),
                       2*d(1) - 2*n_dot_d*n(1),
                       2*d(2) - 2*n_dot_d*n(2));
  return Measurement1D(val, sqrt(ROOT::Math::Similarity(jac, svcov + pvcov)) / 2 / val);

}

void MFVVertexHistos::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<MFVEvent> mevent;
  event.getByToken(mevent_token, mevent);

  edm::Handle<double> weight;
  event.getByToken(weight_token, weight);
  const double w = *weight;
  h_w->Fill(w);

  const double bsx = mevent->bsx;
  const double bsy = mevent->bsy;
  const double bsz = mevent->bsz;
  const math::XYZPoint bs(bsx, bsy, bsz);
  const math::XYZPoint pv(mevent->pvx, mevent->pvy, mevent->pvz);

  edm::Handle<MFVVertexAuxCollection> auxes;
  event.getByToken(vertex_token, auxes);

  const int nsv = int(auxes->size());
  h_nsv->Fill(nsv, w);
  // matching jets with gen quarks from LLPs and fill a 2D histogram with nsv vs. # total number of jets matched to LLPs
  // do the same but with gen leptons from LLPs;
  // nmatched 0 refers to the first llp; nmatched 1 refers to the second llp
  double nmatched_0 = 0;
  double nmatched_1 = 0;
  double nelematched_0 = 0;
  double nelematched_1 = 0;
  double nmumatched_0 = 0;
  double nmumatched_1 = 0;

  //vector of important variables : (eta, phi, pt, dxybs, dxyerr, nsigmadxy, minr, npxlayers, nstlayers)
  std::vector<float> elematched_0; 
  std::vector<float> elematched_1;
  std::vector<float> mumatched_0;
  std::vector<float> mumatched_1;


  int ngen_ele = 0;
  int ngen_mu = 0;
  int ngen_tau = 0;

  int genele0 = 0;
  int genele1 = 0;
  int genmu0 = 0;
  int genmu1 = 0;
  
  for (size_t i=0; i<mevent->gen_daughters.size(); ++i){
    // skip stops and only look at leptons and quarks
    // FIXME: this only works for stoplq samples
    if (abs(mevent->gen_daughter_id[i])==1000006) {
      continue;
    }
    else{
      double gd_eta = mevent->gen_daughters[i].Eta();
      double gd_phi = mevent->gen_daughters[i].Phi();
      int n_matched = 0;
      int n_ematched = 0;
      int ngen_e = 0;
      int n_mmatched = 0;
      int ngen_m = 0;
      if (abs(mevent->gen_daughter_id[i]) >= 1 && abs(mevent->gen_daughter_id[i]) <= 5) {
        for (int ij = 0; ij<mevent->njets(); ++ij){
          double dR2 = reco::deltaR2(mevent->nth_jet_eta(ij), mevent->nth_jet_phi(ij), gd_eta, gd_phi);
          if (dR2<0.16){
            n_matched += 1;
          }
        }
      }
      else if (abs(mevent->gen_daughter_id[i]) == 11) { 
        ngen_ele += 1;
        ngen_e +=1;
        std::vector<int> matched_ele_indx; 
        std::vector<double> mindR;

        for (int ie=0; ie<mevent->nelectrons(); ++ie){
          double dR = reco::deltaR(mevent->nth_ele_eta(ie), mevent->nth_ele_phi(ie), gd_eta, gd_phi);
          mindR.push_back(dR);
          matched_ele_indx.push_back(ie);
        }
        if (mindR.size() !=0) {
          h_gen_ele_closestdR->Fill(*min_element(mindR.begin(), mindR.end()), w);
          float best_dR = *min_element(mindR.begin(), mindR.end());
          int best_idx = std::min_element(mindR.begin(), mindR.end()) - mindR.begin();
          //since the electrons are ordered; the best mindR index can be used for all electron variables 
          int bestele_idx = matched_ele_indx[best_idx];

          // if (bestele_idx != best_idx) {
          //   std::cout << bestele_idx << " " << best_idx << std::endl;
          // }
          if (best_dR < 0.2) {
            n_ematched +=1;
            if (i < 2) {
              elematched_0.push_back(mevent->nth_ele_eta(bestele_idx));
              elematched_0.push_back(mevent->nth_ele_phi(bestele_idx));
              elematched_0.push_back(mevent->nth_ele_pt(bestele_idx));
              elematched_0.push_back(mevent->electron_dxybs[bestele_idx]);
              elematched_0.push_back(mevent->electron_dxyerr[bestele_idx]);
              elematched_0.push_back(fabs(mevent->electron_dxybs[bestele_idx]/mevent->electron_dxyerr[bestele_idx]));
              elematched_0.push_back(mevent->electron_minr[bestele_idx]);
              elematched_0.push_back(mevent->electron_npxlayers(bestele_idx));
              elematched_0.push_back(mevent->electron_nstlayers(bestele_idx));
            }
            else if (i>2) {
              elematched_1.push_back(mevent->nth_ele_eta(bestele_idx));
              elematched_1.push_back(mevent->nth_ele_phi(bestele_idx));
              elematched_1.push_back(mevent->nth_ele_pt(bestele_idx));
              elematched_1.push_back(mevent->electron_dxybs[bestele_idx]);
              elematched_1.push_back(mevent->electron_dxyerr[bestele_idx]);
              elematched_1.push_back(fabs(mevent->electron_dxybs[bestele_idx]/mevent->electron_dxyerr[bestele_idx]));
              elematched_1.push_back(mevent->electron_minr[bestele_idx]);
              elematched_1.push_back(mevent->electron_npxlayers(bestele_idx));
              elematched_1.push_back(mevent->electron_nstlayers(bestele_idx));
            }
          }
        }
      }
      else if (abs(mevent->gen_daughter_id[i]) == 13 ) {
        ngen_mu += 1;
        ngen_m +=1;
        std::vector<double> mindR;
        std::vector<double> matched_mu_idx;
        for (int im=0; im<mevent->nmuons(); ++im){
          double dR = reco::deltaR(mevent->nth_mu_eta(im), mevent->nth_mu_phi(im), gd_eta, gd_phi);
          mindR.push_back(dR);
          matched_mu_idx.push_back(im);
        }
        if (mindR.size() !=0) {
          h_gen_mu_closestdR->Fill(*min_element(mindR.begin(), mindR.end()), w);
          float best_dR = *min_element(mindR.begin(), mindR.end());
          int best_idx = std::min_element(mindR.begin(), mindR.end()) - mindR.begin();
          int bestmu_idx = matched_mu_idx[best_idx];

          // if (bestmu_idx != best_idx) {
          //   std::cout << bestmu_idx << " " << best_idx << std::endl;
          // }
          if (best_dR < 0.2) {
            n_mmatched +=1;
            if (i < 2) {
              mumatched_0.push_back(mevent->nth_mu_eta(bestmu_idx));
              mumatched_0.push_back(mevent->nth_mu_phi(bestmu_idx));
              mumatched_0.push_back(mevent->nth_mu_pt(bestmu_idx));
              mumatched_0.push_back(mevent->muon_dxybs[bestmu_idx]);
              mumatched_0.push_back(mevent->muon_dxyerr[bestmu_idx]);
              mumatched_0.push_back(fabs(mevent->muon_dxybs[bestmu_idx]/mevent->muon_dxyerr[bestmu_idx]));
              mumatched_0.push_back(mevent->muon_minr[bestmu_idx]);
              mumatched_0.push_back(mevent->muon_npxlayers(bestmu_idx));
              mumatched_0.push_back(mevent->muon_nstlayers(bestmu_idx));

            }
            else if (i>2) {
              mumatched_1.push_back(mevent->nth_mu_eta(bestmu_idx));
              mumatched_1.push_back(mevent->nth_mu_phi(bestmu_idx));
              mumatched_1.push_back(mevent->nth_mu_pt(bestmu_idx));
              mumatched_1.push_back(mevent->muon_dxybs[bestmu_idx]);
              mumatched_1.push_back(mevent->muon_dxyerr[bestmu_idx]);
              mumatched_1.push_back(fabs(mevent->muon_dxybs[bestmu_idx]/mevent->muon_dxyerr[bestmu_idx]));
              mumatched_1.push_back(mevent->muon_minr[bestmu_idx]);
              mumatched_1.push_back(mevent->muon_npxlayers(bestmu_idx));
              mumatched_1.push_back(mevent->muon_nstlayers(bestmu_idx));
            }
          }
        }
      }
      else if (abs(mevent->gen_daughter_id[i]) == 15 ) {
        ngen_tau +=1;
      }
      //should be 4 gen daughters; i = 0,1 belong to first vertex; i = 2,3 belong to second vertex
      if (i<2){
        nmatched_0 += n_matched;
        nelematched_0 += n_ematched;
        nmumatched_0 += n_mmatched;
        genele0 += ngen_e;
        genmu0 += ngen_m;
        
      }
      else{
        nmatched_1 += n_matched;
        nelematched_1 += n_ematched;
        nmumatched_1 += n_mmatched;
        genele1 += ngen_e;
        genmu1 += ngen_m;
      }
    }
  }
  std::vector<int> genlep_dau{ngen_ele, ngen_mu, ngen_tau};
  h_sv_nsv_nmatchjet->Fill(nmatched_0+nmatched_1, nsv, w);

  if (genele0) h_nmatchele->Fill(nelematched_0, w);
  if (genele1) h_nmatchele->Fill(nelematched_1, w);
  if (genmu0) h_nmatchmu->Fill(nmumatched_0, w);
  if (genmu1) h_nmatchmu->Fill(nmumatched_1, w);

  for (int isv = 0; isv < nsv; ++isv) {
    const MFVVertexAux& aux = auxes->at(isv);
    const int ntracks = aux.ntracks();
    const int nmuons = aux.nmuons;
    const int nelectrons = aux.nelectrons;


    jmt::MinValue d;
    double sv_gen2ddist_sign = 1;
    for (int igenv = 0; igenv < 2; ++igenv) {
      double genx = mevent->gen_lsp_decay[igenv*3+0];
      double geny = mevent->gen_lsp_decay[igenv*3+1];
      d(igenv, mag(aux.x-genx,
                  aux.y-geny));  
    }

    const int genvtx_2d = d.i();

    double genbs2ddist = mevent->mag(mevent->gen_lsp_decay[genvtx_2d*3+0] - mevent->bsx_at_z(mevent->gen_lsp_decay[genvtx_2d*3+2]),
                                     mevent->gen_lsp_decay[genvtx_2d*3+1] - mevent->bsy_at_z(mevent->gen_lsp_decay[genvtx_2d*3+2]) 
          );
    h_sv_ntk_genbs2ddist->Fill(ntracks, genbs2ddist, w);
    if (genbs2ddist<mevent->bs2ddist(aux))
      sv_gen2ddist_sign = -1;

    h_sv_gen2ddist_signed->Fill(sv_gen2ddist_sign*aux.gen2ddist, w);

    h_sv_ntk_bs2ddist->Fill(ntracks, mevent->bs2ddist(aux), w);
    h_sv_ntk_gen2ddist->Fill(ntracks, aux.gen2ddist, w);
    h_sv_xy->Fill(aux.x - mevent->bsx_at_z(aux.z), aux.y - mevent->bsy_at_z(aux.z), w);
    h_sv_xz->Fill(aux.x - mevent->bsx_at_z(aux.z), aux.z - bsz, w);
    h_sv_yz->Fill(aux.y - mevent->bsy_at_z(aux.z), aux.z - bsz, w);
    h_sv_rz->Fill(mevent->bs2ddist(aux) * (aux.y - mevent->bsy_at_z(aux.z) >= 0 ? 1 : -1), aux.z - bsz, w);

    MFVVertexAux::stats trackpairdeta_stats(&aux, aux.trackpairdetas());
    MFVVertexAux::stats   trackpairdr_stats(&aux, aux.trackpairdrs());

    jmt::MaxValue max_nm1_refit_dist3_wbad, max_nm1_refit_dist3, max_nm1_refit_dist2, max_nm1_refit_distz;
    for (size_t i = 0, ie = aux.nnm1(); i < ie; ++i) {
      const double dist3 = mag(aux.nm1_x[i] - aux.x, aux.nm1_y[i] - aux.y, aux.nm1_z[i] - aux.z);
      if (aux.nm1_chi2[i] < 0)
        max_nm1_refit_dist3_wbad(std::numeric_limits<double>::max());
      else {
        max_nm1_refit_dist3_wbad(dist3);
        max_nm1_refit_dist3(dist3);
        max_nm1_refit_dist2(mag(aux.nm1_x[i] - aux.x, aux.nm1_y[i] - aux.y));
        max_nm1_refit_distz(fabs(aux.nm1_z[i] - aux.z));
      }
    }

    if (max_nm1_refit_dist3_wbad == std::numeric_limits<double>::max())
      max_nm1_refit_dist3_wbad.set(-0.0005);

    PairwiseHistos::ValueMap v = {
        {"x", aux.x - mevent->bsx_at_z(aux.z)},
        {"y", aux.y - mevent->bsy_at_z(aux.z)},
        {"z", aux.z - bsz},
        {"phi", atan2(aux.y - mevent->bsy_at_z(aux.z), aux.x - mevent->bsx_at_z(aux.z))},
        {"phi_pv", atan2(aux.y - mevent->pvy, aux.x - mevent->pvx)},
        {"cxx", aux.cxx},
        {"cxy", aux.cxy},
        {"cxz", aux.cxz},
        {"cyy", aux.cyy},
        {"cyz", aux.cyz},
        {"czz", aux.czz},

        {"rescale_chi2", aux.rescale_chi2},
        {"rescale_x", aux.rescale_x - mevent->bsx_at_z(aux.z)},
        {"rescale_y", aux.rescale_y - mevent->bsy_at_z(aux.z)},
        {"rescale_z", aux.rescale_z - bsz},
        {"rescale_cxx", aux.rescale_cxx},
        {"rescale_cxy", aux.rescale_cxy},
        {"rescale_cxz", aux.rescale_cxz},
        {"rescale_cyy", aux.rescale_cyy},
        {"rescale_cyz", aux.rescale_cyz},
        {"rescale_czz", aux.rescale_czz},
        {"rescale_dx", aux.rescale_x - aux.x},
        {"rescale_dy", aux.rescale_y - aux.y},
        {"rescale_dz", aux.rescale_z - aux.z},
        {"rescale_dx_big", aux.rescale_x - aux.x},
        {"rescale_dy_big", aux.rescale_y - aux.y},
        {"rescale_dz_big", aux.rescale_z - aux.z},
        {"rescale_d2",     mag(aux.rescale_x - aux.x, aux.rescale_y - aux.y)},
        {"rescale_d2_big", mag(aux.rescale_x - aux.x, aux.rescale_y - aux.y)},
        {"rescale_d3",     mag(aux.rescale_x - aux.x, aux.rescale_y - aux.y, aux.rescale_z - aux.z)},
        {"rescale_d3_big", mag(aux.rescale_x - aux.x, aux.rescale_y - aux.y, aux.rescale_z - aux.z)},
        {"rescale_bsbs2ddist", mag(aux.x - mevent->bsx_at_z(aux.z), aux.y - mevent->bsy_at_z(aux.z))},
        {"rescale_bs2derr", aux.rescale_bs2derr},

        {"max_nm1_refit_dist3_wbad", max_nm1_refit_dist3_wbad},
        {"max_nm1_refit_dist3", max_nm1_refit_dist3},
        {"max_nm1_refit_dist2", max_nm1_refit_dist2},
        {"max_nm1_refit_distz", max_nm1_refit_distz},

        {"ntracks",                 ntracks},
        {"ntracksptgt3",            aux.ntracksptgt(3)},
        {"ntracksptgt10",           aux.ntracksptgt(10)},
        {"ntracksetagt1p5",         aux.ntracksetagt(1.5)},
        {"trackminnhits",           aux.trackminnhits()},
        {"trackmaxnhits",           aux.trackmaxnhits()},
        {"njetsntks",               aux.njets[mfv::JByNtracks]},
        {"nelensv",                 nelectrons},
        {"nmunsv",                  nmuons},
        {"nlepnsv",                 aux.nleptons},
        {"chi2dof",                 aux.chi2dof()},
        {"chi2dofprob",             TMath::Prob(aux.chi2, aux.ndof())},

        {"tkonlyp",             aux.p4(mfv::PTracksOnly).P()},
        {"tkonlypt",            aux.pt[mfv::PTracksOnly]},
        {"tkonlyeta",           aux.eta[mfv::PTracksOnly]},
        {"tkonlyrapidity",      aux.p4(mfv::PTracksOnly).Rapidity()},
        {"tkonlyphi",           aux.phi[mfv::PTracksOnly]},
        {"tkonlymass",          aux.mass[mfv::PTracksOnly]},

        {"jetsntkp",             aux.p4(mfv::PJetsByNtracks).P()},
        {"jetsntkpt",            aux.pt[mfv::PJetsByNtracks]},
        {"jetsntketa",           aux.eta[mfv::PJetsByNtracks]},
        {"jetsntkrapidity",      aux.p4(mfv::PJetsByNtracks).Rapidity()},
        {"jetsntkphi",           aux.phi[mfv::PJetsByNtracks]},
        {"jetsntkmass",          aux.mass[mfv::PJetsByNtracks]},

        {"tksjetsntkp",             aux.p4(mfv::PTracksPlusJetsByNtracks).P()},
        {"tksjetsntkpt",            aux.pt[mfv::PTracksPlusJetsByNtracks]},
        {"tksjetsntketa",           aux.eta[mfv::PTracksPlusJetsByNtracks]},
        {"tksjetsntkrapidity",      aux.p4(mfv::PTracksPlusJetsByNtracks).Rapidity()},
        {"tksjetsntkphi",           aux.phi[mfv::PTracksPlusJetsByNtracks]},
        {"tksjetsntkmass",          aux.mass[mfv::PTracksPlusJetsByNtracks]},

        {"costhtkonlymombs",         aux.costhmombs  (mfv::PTracksOnly)},
        {"costhtkonlymompv2d",       aux.costhmompv2d(mfv::PTracksOnly)},
        {"costhtkonlymompv3d",       aux.costhmompv3d(mfv::PTracksOnly)},

        {"costhtksjetsntkmombs",     aux.costhmombs  (mfv::PTracksPlusJetsByNtracks)},
        {"costhtksjetsntkmompv2d",   aux.costhmompv2d(mfv::PTracksPlusJetsByNtracks)},
        {"costhtksjetsntkmompv3d",   aux.costhmompv3d(mfv::PTracksPlusJetsByNtracks)},

        {"missdisttkonlypv",        aux.missdistpv   [mfv::PTracksOnly]},
        {"missdisttkonlypverr",     aux.missdistpverr[mfv::PTracksOnly]},
        {"missdisttkonlypvsig",     aux.missdistpvsig(mfv::PTracksOnly)},

        

        {"missdisttksjetsntkpv",        aux.missdistpv   [mfv::PTracksPlusJetsByNtracks]},
        {"missdisttksjetsntkpverr",     aux.missdistpverr[mfv::PTracksPlusJetsByNtracks]},
        {"missdisttksjetsntkpvsig",     aux.missdistpvsig(mfv::PTracksPlusJetsByNtracks)},

        {"sumpt2",                  aux.sumpt2()},

        {"ntrackssharedwpv", aux.ntrackssharedwpv()},
        {"ntrackssharedwpvs", aux.ntrackssharedwpvs()},
        {"fractrackssharedwpv", float(aux.ntrackssharedwpv()) / ntracks},
        {"fractrackssharedwpvs", float(aux.ntrackssharedwpvs()) / ntracks},
        {"npvswtracksshared", aux.npvswtracksshared()},

        {"trackdxymin", aux.trackdxymin()},
        {"trackdxymax", aux.trackdxymax()},
        {"trackdxyavg", aux.trackdxyavg()},
        {"trackdxyrms", aux.trackdxyrms()},

        {"trackdzmin", aux.trackdzmin()},
        {"trackdzmax", aux.trackdzmax()},
        {"trackdzavg", aux.trackdzavg()},
        {"trackdzrms", aux.trackdzrms()},

        {"trackpterrmin", aux.trackpterrmin()},
        {"trackpterrmax", aux.trackpterrmax()},
        {"trackpterravg", aux.trackpterravg()},
        {"trackpterrrms", aux.trackpterrrms()},

        {"tracketaerrmin", aux.tracketaerrmin()},
        {"tracketaerrmax", aux.tracketaerrmax()},
        {"tracketaerravg", aux.tracketaerravg()},
        {"tracketaerrrms", aux.tracketaerrrms()},

        {"trackphierrmin", aux.trackphierrmin()},
        {"trackphierrmax", aux.trackphierrmax()},
        {"trackphierravg", aux.trackphierravg()},
        {"trackphierrrms", aux.trackphierrrms()},

        {"trackdxyerrmin", aux.trackdxyerrmin()},
        {"trackdxyerrmax", aux.trackdxyerrmax()},
        {"trackdxyerravg", aux.trackdxyerravg()},
        {"trackdxyerrrms", aux.trackdxyerrrms()},

        {"trackdxynsigmamin", aux.trackdxynsigmamin()},
        {"trackdxynsigmamax", aux.trackdxynsigmamax()},
        {"trackdxynsigmaavg", aux.trackdxynsigmaavg()},
        {"trackdxynsigmarms", aux.trackdxynsigmarms()},

        {"trackdzerrmin", aux.trackdzerrmin()},
        {"trackdzerrmax", aux.trackdzerrmax()},
        {"trackdzerravg", aux.trackdzerravg()},
        {"trackdzerrrms", aux.trackdzerrrms()},

        {"trackpairdetamin", trackpairdeta_stats.min},
        {"trackpairdetamax", trackpairdeta_stats.max},
        {"trackpairdetaavg", trackpairdeta_stats.avg},
        {"trackpairdetarms", trackpairdeta_stats.rms},

        {"trackpairdrmin",  trackpairdr_stats.min},
        {"trackpairdrmax",  trackpairdr_stats.max},
        {"trackpairdravg",  trackpairdr_stats.avg},
        {"trackpairdrrms",  trackpairdr_stats.rms},

        {"costhtkmomvtxdispmin", aux.costhtkmomvtxdispmin()},
        {"costhtkmomvtxdispmax", aux.costhtkmomvtxdispmax()},
        {"costhtkmomvtxdispavg", aux.costhtkmomvtxdispavg()},
        {"costhtkmomvtxdisprms", aux.costhtkmomvtxdisprms()},

        {"costhjetmomvtxdispmin", aux.costhjetmomvtxdispmin()},
        {"costhjetmomvtxdispmax", aux.costhjetmomvtxdispmax()},
        {"costhjetmomvtxdispavg", aux.costhjetmomvtxdispavg()},
        {"costhjetmomvtxdisprms", aux.costhjetmomvtxdisprms()},

        {"gen2ddist",   aux.gen2ddist},
        {"gen2derr",    aux.gen2derr},
        {"gen2dsig",    aux.gen2dsig()},
        {"gen3ddist",   aux.gen3ddist},
        {"gen3derr",    aux.gen3derr},
        {"gen3dsig",    aux.gen3dsig()},
        {"bs2ddist",    aux.bs2ddist},
        {"bsbs2ddist",  mevent->bs2ddist(aux)},
        {"bs2derr",     aux.bs2derr},
        {"bs2dsig",     aux.bs2dsig()},
        {"pv2ddist",    aux.pv2ddist},
        {"pv2derr",     aux.pv2derr},
        {"pv2dsig",     aux.pv2dsig()},
        {"pv3ddist",    aux.pv3ddist},
        {"pv3derr",     aux.pv3derr},
        {"pv3dsig",     aux.pv3dsig()},
        {"pvdz",        aux.pvdz()},
        {"pvdzerr",     aux.pvdzerr()},
        {"pvdzsig",     aux.pvdzsig()}
    };

    std::map<int,int> multipv = aux.pvswtracksshared();
    std::map<int,int> multipvbyz;
    for (int i = 0; i < ntracks; ++i) {
      jmt::MinValue closest(0.1);
      for (int j = 0; j < mevent->npv; ++j)
        closest(j, fabs(aux.track_vz[i] - mevent->pv_z(j)));
      if (closest.i() >= 0)
        ++multipvbyz[closest.i()];
    }

    auto multipv_maxdz = [&](const std::map<int,int>& m) {
      std::vector<int> mv;
      for (auto c : m)
        if (c.first != -1)
          mv.push_back(c.first);
      jmt::MaxValue v;
      const size_t n = mv.size();
      for (size_t i = 0; i < n; ++i)
        for (size_t j = i+1; j < n; ++j)
          v(fabs(mevent->pv_z(mv[i]) - mevent->pv_z(mv[j])));
      return double(v);
    };
    v["multipv_maxdz"] = multipv_maxdz(multipv);
    v["multipvbyz_maxdz"] = multipv_maxdz(multipvbyz);

    std::vector<float> trackpairdphis = aux.trackpairdphis();
    std::sort(trackpairdphis.begin(), trackpairdphis.end());
    const size_t ntrackpairs = trackpairdphis.size();
    v["trackpairdphimax"]   = ntrackpairs < 1 ? -1 : trackpairdphis[ntrackpairs-1];
    v["trackpairdphimaxm1"] = ntrackpairs < 2 ? -1 : trackpairdphis[ntrackpairs-2];
    v["trackpairdphimaxm2"] = ntrackpairs < 3 ? -1 : trackpairdphis[ntrackpairs-3];

    for (int i = 0; i < 4; ++i) {
      std::vector<double> jetdeltaphis;
      for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
        if (mevent->jet_pt[ijet] < mfv::min_jet_pt)
          continue;
        if (((mevent->jet_id[ijet] >> 2) & 3) >= i) {
          const double dphi = reco::deltaPhi(atan2(aux.y - bsy, aux.x - bsx), mevent->jet_phi[ijet]);
          fill(h_sv_jets_deltaphi[i], isv, dphi, w);
          jetdeltaphis.push_back(fabs(dphi));
        }
      }
      std::sort(jetdeltaphis.begin(), jetdeltaphis.end());
      int njets = jetdeltaphis.size();
      v[TString::Format("jet%d_deltaphi0", i).Data()] = 0 > njets - 1 ? -1 : jetdeltaphis[0];
      v[TString::Format("jet%d_deltaphi1", i).Data()] = 1 > njets - 1 ? -1 : jetdeltaphis[1];
    }

    fill(h_sv_bs2derr_bsbs2ddist, isv, mevent->bs2ddist(aux), aux.bs2derr, w);
    fill(h_pvrho_bsbs2ddist, isv, mevent->bs2ddist(aux), mevent->pv_rho(), w);

    for (int i = 0; i < ntracks; ++i) {
      fill(h_sv_track_weight, isv, aux.track_weight(i), w);
      fill(h_sv_track_q, isv, aux.track_q(i), w);
      fill(h_sv_track_pt, isv, aux.track_pt(i), w);
      fill(h_sv_track_eta, isv, aux.track_eta[i], w);
      fill(h_sv_track_phi, isv, aux.track_phi[i], w);
      fill(h_sv_track_dxy, isv, aux.track_dxy[i], w);
      fill(h_sv_track_dz, isv, aux.track_dz[i], w);
      fill(h_sv_track_pt_err, isv, aux.track_pt_err[i], w);
      fill(h_sv_track_eta_err, isv, aux.track_eta_err(i), w);
      fill(h_sv_track_phi_err, isv, aux.track_phi_err(i), w);
      fill(h_sv_track_dxy_err, isv, aux.track_dxy_err(i), w);
      fill(h_sv_track_dz_err, isv, aux.track_dz_err(i), w);
      fill(h_sv_track_nsigmadxy, isv, aux.track_dxy[i] / aux.track_dxy_err(i), w);
      fill(h_sv_track_chi2dof, isv, aux.track_chi2dof(i), w);
      fill(h_sv_track_npxhits, isv, aux.track_npxhits(i), w);
      fill(h_sv_track_nsthits, isv, aux.track_nsthits(i), w);
      fill(h_sv_track_nhitsbehind, isv, aux.track_nhitsbehind(i), w);
      fill(h_sv_track_nhitslost, isv, aux.track_nhitslost(i), w);
      fill(h_sv_track_nhits, isv, aux.track_nhits(i), w);
      fill(h_sv_track_injet, isv, aux.track_injet[i], w);
      fill(h_sv_track_inpv, isv, aux.track_inpv[i], w);
    }

    for (int i=0; i < nelectrons; ++i) {
      fill(h_sv_eletrack_pt,  isv, aux.electron_pt[i],  w);
      fill(h_sv_eletrack_eta, isv, aux.electron_eta[i], w);
      fill(h_sv_eletrack_phi, isv, aux.electron_phi[i], w);
      fill(h_sv_eletrack_dxy, isv, aux.electron_dxy[i], w);
      fill(h_sv_eletrack_iso, isv, aux.electron_iso[i], w); 
      auto temp = aux.electron_ID[i]; 
      int id = 0;
      if ( temp[0] == 0 ) id = 0; 
      if ( temp[0] == 1 ) id = 1;
      if ( temp[1] == 1 ) id = 2; 
      if ( temp[2] == 1 ) id = 3;
      if ( temp[3] == 1 ) id = 4;
      fill(h_sv_eletrack_ID,  isv, id,  w);
    //   fill(h_sv_matchedeletrack_tip, isv, aux.matchedelevtxtip[i], w);
    //   fill(h_sv_matchedeletrack_tiperr, isv, aux.matchedelevtxtiperr[i], w);
    }
    // for (size_t i = 0, ie = aux.elevtxtip.size(); i < ie; ++i) {
    //   fill(h_sv_alleletrack_tip, isv, aux.elevtxtip[ie], w);
    //   fill(h_sv_alleletrack_tiperr, isv, aux.elevtxtiperr[ie], w);
    //   fill(h_sv_alleletrack_tipsig, isv, aux.elevtxtipsig[ie], w);
    // }

    for (int i=0; i < nmuons; ++i) {
      fill(h_sv_mutrack_pt,  isv, aux.muon_pt[i],  w);
      fill(h_sv_mutrack_eta, isv, aux.muon_eta[i], w);
      fill(h_sv_mutrack_phi, isv, aux.muon_phi[i], w);
      fill(h_sv_mutrack_dxy, isv, aux.muon_dxy[i], w);
      fill(h_sv_mutrack_iso, isv, aux.muon_iso[i], w); 
      auto temp = aux.muon_ID[i]; 
      int id = 0;
      if ( temp[0] == 0 ) id = 0; 
      if ( temp[0] == 1 ) id = 1;
      if ( temp[1] == 1 ) id = 2; 
      if ( temp[2] == 1 ) id = 3;
      fill(h_sv_mutrack_ID,  isv, id,  w);
      // fill(h_sv_matchedmutrack_tip, isv, aux.matchedmuvtxtip[i], w);
      // fill(h_sv_matchedmutrack_tiperr, isv, aux.matchedmuvtxtiperr[i], w);
      // fill(h_sv_matchedmutrack_tipsig, isv, aux.matchedmuvtxtipsig[i], w);
    }
    // for (size_t j =0, im=aux.muvtxtip.size(); j < im; ++j) {
    //   fill(h_sv_allmutrack_tip, isv, aux.muvtxtip[im], w);
    //   fill(h_sv_allmutrack_tiperr, isv, aux.muvtxtiperr[im], w);
    //   fill(h_sv_allmutrack_tipsig, isv, aux.muvtxtipsig[im], w);
      // mu_isv_tip.push_back(aux.muvtxtip[im]);
      // mu_isv_tiperr.push_back(aux.muvtxtiperr[im]);
      // mu_isv_tipsig.push_back(aux.muvtxtipsig[im]);
    //} 

    // muon_sv_tip.push_back(mu_isv_tip);
    // muon_sv_tiperr.push_back(mu_isv_tiperr);
    // muon_sv_tipsig.push_back(mu_isv_tipsig);


    h_svidx_assocel->Fill(nelectrons, isv, w);
    h_svidx_assocmu->Fill(nmuons, isv, w);
    h_svidx_assoclep->Fill(nelectrons+nmuons, isv, w);
   
    if (max_ntrackplots > 0) {
      std::vector<std::pair<int,float>> itk_pt;
      for (int i = 0; i < ntracks; ++i)
        itk_pt.push_back(std::make_pair(i, aux.track_pt(i)));

      std::sort(itk_pt.begin(), itk_pt.end(), [](std::pair<int,float> itk_pt1, std::pair<int,float> itk_pt2) { return itk_pt1.second > itk_pt2.second; } );
      for (int i = 0; i < max_ntrackplots; ++i) {
        if (i < ntracks) {
          v[TString::Format("track%i_weight",        i).Data()] = aux.track_weight(itk_pt[i].first);
          v[TString::Format("track%i_q",             i).Data()] = aux.track_q(itk_pt[i].first);
          v[TString::Format("track%i_pt",            i).Data()] = aux.track_pt(itk_pt[i].first);
          v[TString::Format("track%i_eta",           i).Data()] = aux.track_eta[itk_pt[i].first];
          v[TString::Format("track%i_phi",           i).Data()] = aux.track_phi[itk_pt[i].first];
          v[TString::Format("track%i_dxy",           i).Data()] = aux.track_dxy[itk_pt[i].first];
          v[TString::Format("track%i_dz",            i).Data()] = aux.track_dz[itk_pt[i].first];
          v[TString::Format("track%i_pt_err",        i).Data()] = aux.track_pt_err[itk_pt[i].first];
          v[TString::Format("track%i_eta_err",       i).Data()] = aux.track_eta_err(itk_pt[i].first);
          v[TString::Format("track%i_phi_err",       i).Data()] = aux.track_phi_err(itk_pt[i].first);
          v[TString::Format("track%i_dxy_err",       i).Data()] = aux.track_dxy_err(itk_pt[i].first);
          v[TString::Format("track%i_dz_err",        i).Data()] = aux.track_dz_err(itk_pt[i].first);
          v[TString::Format("track%i_nsigmadxy",     i).Data()] = aux.track_dxy[itk_pt[i].first] / aux.track_dxy_err(itk_pt[i].first);
          v[TString::Format("track%i_chi2dof",       i).Data()] = aux.track_chi2dof(itk_pt[i].first);
          v[TString::Format("track%i_npxhits",       i).Data()] = aux.track_npxhits(itk_pt[i].first);
          v[TString::Format("track%i_nsthits",       i).Data()] = aux.track_nsthits(itk_pt[i].first);
          v[TString::Format("track%i_nhitsbehind",   i).Data()] = aux.track_nhitsbehind(itk_pt[i].first);
          v[TString::Format("track%i_nhitslost",     i).Data()] = aux.track_nhitslost(itk_pt[i].first);
          v[TString::Format("track%i_nhits",         i).Data()] = aux.track_nhits(itk_pt[i].first);
          v[TString::Format("track%i_injet",         i).Data()] = aux.track_injet[itk_pt[i].first];
          v[TString::Format("track%i_inpv",          i).Data()] = aux.track_inpv[itk_pt[i].first];

          std::vector<double> jetdeltaphis;
          for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
            if (mevent->jet_pt[ijet] < mfv::min_jet_pt)
              continue;
            jetdeltaphis.push_back(fabs(reco::deltaPhi(aux.track_phi[itk_pt[i].first], mevent->jet_phi[ijet])));
          }
          std::sort(jetdeltaphis.begin(), jetdeltaphis.end());
          int njets = jetdeltaphis.size();
          v[TString::Format("track%i_jet_deltaphi0", i).Data()] = 0 > njets - 1 ? -1 : jetdeltaphis[0];
        } else {
          v[TString::Format("track%i_weight",        i).Data()] = -1e6;
          v[TString::Format("track%i_q",             i).Data()] = -1e6;
          v[TString::Format("track%i_pt",            i).Data()] = -1e6;
          v[TString::Format("track%i_eta",           i).Data()] = -1e6;
          v[TString::Format("track%i_phi",           i).Data()] = -1e6;
          v[TString::Format("track%i_dxy",           i).Data()] = -1e6;
          v[TString::Format("track%i_dz",            i).Data()] = -1e6;
          v[TString::Format("track%i_pt_err",        i).Data()] = -1e6;
          v[TString::Format("track%i_eta_err",       i).Data()] = -1e6;
          v[TString::Format("track%i_phi_err",       i).Data()] = -1e6;
          v[TString::Format("track%i_dxy_err",       i).Data()] = -1e6;
          v[TString::Format("track%i_dz_err",        i).Data()] = -1e6;
          v[TString::Format("track%i_nsigmadxy",     i).Data()] = -1e6;
          v[TString::Format("track%i_chi2dof",       i).Data()] = -1e6;
          v[TString::Format("track%i_npxhits",       i).Data()] = -1e6;
          v[TString::Format("track%i_nsthits",       i).Data()] = -1e6;
          v[TString::Format("track%i_nhitsbehind",   i).Data()] = -1e6;
          v[TString::Format("track%i_nhitslost",     i).Data()] = -1e6;
          v[TString::Format("track%i_nhits",         i).Data()] = -1e6;
          v[TString::Format("track%i_injet",         i).Data()] = -1e6;
          v[TString::Format("track%i_inpv",          i).Data()] = -1e6;
          v[TString::Format("track%i_jet_deltaphi0", i).Data()] = -1e6;
        }
      }
    }

    fill(h_sv, isv, v, w);
  }

  //////////////////////////////////////////////////////////////////////

  int nsv_wassoclept = 0;
  //just storing nlep assoc. to sv 
  std::vector<int> isv_elinsv;
  std::vector<int> isv_muinsv; 

  // // 2d vector storing : 
  // // (e, mu, tau) 
  // // index is sv 
  std::vector<std::vector<int>> vtx_flavor;

  // the dR between isv and gen vtx; 
  // index is sv
  std::vector<float> genvertex0_dR;
  std::vector<float> genvertex1_dR;

  //index should be sv
  //going to revert to match by track... 
  // std::vector<bool> genmatchedele0_bylep;
  // std::vector<bool> genmatchedmu0_bylep;
  // std::vector<bool> genmatchedele1_bylep;
  // std::vector<bool> genmatchedmu1_bylep;
  // std::vector<bool> genmatchedele_bytrk;
  // std::vector<bool> genmatchedmu_bytrk;
  std::vector<bool> genmatchedele0_bytrk;
  std::vector<bool> genmatchedmu0_bytrk;
  std::vector<bool> genmatchedele1_bytrk;
  std::vector<bool> genmatchedmu1_bytrk;

  //include : ntracks for each sv 
  std::vector<float> ele0_vtx_ntracks;
  std::vector<float> ele1_vtx_ntracks;
  std::vector<float> mu0_vtx_ntracks;
  std::vector<float> mu1_vtx_ntracks;


  // index is sv; 
  //2d vector of : dR between tracks and lepton 
  // if no lepton -> {} 
  std::vector<std::vector<float>> el_vtxtrk_dR;
  std::vector<std::vector<float>> mu_vtxtrk_dR;

  //index is sv; 
  //2d vector of : missdist between lep and sv
  std::vector<float> missdist_ele0;
  std::vector<float> missdist_ele1;
  std::vector<float> missdist_mu0;
  std::vector<float> missdist_mu1;

  std::vector<double> missdisterr_ele0;
  std::vector<double> missdisterr_ele1;
  std::vector<double> missdisterr_mu0;
  std::vector<double> missdisterr_mu1;

  double gensv[4] {mevent->gen_lsp_decay[0*3+0], mevent->gen_lsp_decay[0*3+1], mevent->gen_lsp_decay[1*3+0], mevent->gen_lsp_decay[1*3+1]};

  for (int isv = 0; isv < nsv; ++isv) {
    const MFVVertexAux& aux = auxes->at(isv);
    const int ntracks = aux.ntracks();
    const math::XYZPoint pos_isv(aux.x, aux.y, aux.z);

    double pvarr[9] {mevent->pvcxx, mevent->pvcxy, mevent->pvcxz, mevent->pvcxy, mevent->pvcyy, mevent->pvcyz, mevent->pvcxz, mevent->pvcyz, mevent->pvczz};
    double svarr[9] {aux.cxx, aux.cxy, aux.cxz, aux.cxy, aux.cyy, aux.cyz, aux.cxz, aux.cyz, aux.czz};

    //initializing all those 1d that will be stored in the 2d 
    std::vector<int> elinsv;
    std::vector<int> muinsv;
    // vflavor : (ele, mu, tau, none) the last place is to catch events in which no gen particles present in ntuple
    std::vector<int> vflavor{0,0,0,0};

    std::vector<float> eltk_dr;
    std::vector<float> mutk_dr;

    float ele0_md = -99.;
    float ele1_md = -99.;
    float mu0_md = -99.;
    float mu1_md = -99.;
    double ele0_err = -99.;
    double ele1_err = -99.;
    double mu0_err = -99.;
    double mu1_err = -99.;


    // bool genmatchedele0_lep = false;
    // bool genmatchedmu0_lep = false;
    // bool genmatchedele1_lep = false;
    // bool genmatchedmu1_lep = false;
    bool genmatchedele0_trk = false;
    bool genmatchedmu0_trk = false;
    bool genmatchedele1_trk = false;
    bool genmatchedmu1_trk = false;

    const int nmuons = aux.nmuons;
    const int nelectrons = aux.nelectrons;
    elinsv.push_back(nelectrons);
    muinsv.push_back(nmuons);

    if (nmuons + nelectrons > 0 ) nsv_wassoclept +=1;

    //have to do a work around (currently) to get the daughter id's from the correct decay 
    // ie. indirectly getting lepton flavor of the lsp decay. 
    // from eventproducer : 
      // mci->decay_point[i] 
      // mci->secondaries[i] 
    // these will be in order since index is the same. Thus, 
    // gen daughters are a list of 4 [a, b, c, d] 
    // the quarks are a, c. the leptons are b and d 
    // so since we need index 0 and 2, I do igen*2 + 1 
    std::vector<int> genvtx_flavor;
    jmt::MinValue d;
   
    for (int igenv = 0; igenv < 2; ++igenv) {
      double genx = mevent->gen_lsp_decay[igenv*3+0];
      double geny = mevent->gen_lsp_decay[igenv*3+1];
      //hopefully temporary; possibly something went wrong with ntuple creation 
      if (mevent->gen_daughters.size() != 0) {
        int genvtx_fl = abs(mevent->gen_daughter_id[igenv*2+1]);
        genvtx_flavor.push_back(genvtx_fl);

      }
      else {
        int genvtx_fl = -1;
        genvtx_flavor.push_back(genvtx_fl);
      }
      d(igenv, mag(aux.x-genx,
                   aux.y-geny));
    }

    const int closest_genvtx_flavor = genvtx_flavor[d.i()];
    if (closest_genvtx_flavor == 11 ) vflavor[0] += 1;
    if (closest_genvtx_flavor == 13 ) vflavor[1] += 1;
    if (closest_genvtx_flavor == 15 ) vflavor[2] += 1;
    if (closest_genvtx_flavor == -1 ) vflavor[3] += 1;
 
    vtx_flavor.push_back(vflavor);

    //needed a work-around to keep dR for each of the gen vertices separate. while also keeping nentries at nsv 
    // so : dummy fill a large number : 10 for the gen vertex that isn't the closest to the reco vertex. 
    if (d.i() == 0) {
      genvertex0_dR.push_back(d.v());
      genvertex1_dR.push_back(10.);
      if (elematched_0.size() != 0) {
        const math::XYZPoint elepos_0(elematched_0[3], elematched_0[0], elematched_0[1]);
        ele0_md= miss_dist(pv, pos_isv, elepos_0, pvarr, svarr).value();
        ele0_err= miss_dist(pv, pos_isv, elepos_0, pvarr, svarr).error();
        // for (int i=0; i < nelectrons; ++i) {
        //   if (elematched_0[0] == aux.electron_eta[i]) {
        //     if (elematched_0[1] == aux.electron_phi[i]) {    
        //       genmatchedele0_lep = true;
        //     }
        //   }
        // }
        for (int i = 0; i < ntracks; ++i) {
          eltk_dr.push_back(reco::deltaR(elematched_0[0], elematched_0[1], aux.track_eta[i], aux.track_phi[i]));
          if (reco::deltaR(elematched_0[0], elematched_0[1], aux.track_eta[i], aux.track_phi[i]) < 0.2) {
            genmatchedele0_trk = true;
          }
        }
      }
      if (mumatched_0.size() != 0) {
        const math::XYZPoint mupos_0(mumatched_0[3], mumatched_0[0], mumatched_0[1]);
        mu0_md = (miss_dist(pv, pos_isv, mupos_0, pvarr, svarr).value());
        mu0_err = (miss_dist(pv, pos_isv, mupos_0, pvarr, svarr).error());
        // for (int i=0; i < nmuons; ++i) {
        //   if (mumatched_0[0] == aux.muon_eta[i]) {
        //     if (mumatched_0[1] == aux.muon_phi[i]) {
        //       genmatchedmu0_lep = true;
        //     }
        //   }
        // }
        for (int i = 0; i < ntracks; ++i) {
          mutk_dr.push_back(reco::deltaR(mumatched_0[0], mumatched_0[1], aux.track_eta[i], aux.track_phi[i]));
          if (reco::deltaR(mumatched_0[0], mumatched_0[1], aux.track_eta[i], aux.track_phi[i]) < 0.2) {
           genmatchedmu0_trk = true;
          }
        }
      }
    }
    if (d.i() == 1) {
      genvertex1_dR.push_back(d.v());
      genvertex0_dR.push_back(10.);
      
      if (elematched_1.size() != 0) {
        const math::XYZPoint elepos_1(elematched_1[3], elematched_1[0], elematched_1[1]);
        ele1_md = (miss_dist(pv, pos_isv, elepos_1, pvarr, svarr).value());
        ele1_err = (miss_dist(pv, pos_isv, elepos_1, pvarr, svarr).error());
        // for (int i=0; i < nelectrons; ++i) {
        //   if (elematched_1[0] == aux.electron_eta[i]) {
        //     if (elematched_1[1] == aux.electron_phi[i]) {
        //       genmatchedele1_lep = true;
        //     }
        //   } 
        // }
        for (int i = 0; i < ntracks; ++i) {
          eltk_dr.push_back(reco::deltaR(elematched_1[0], elematched_1[1], aux.track_eta[i], aux.track_phi[i]));
          if (reco::deltaR(elematched_1[0], elematched_1[1], aux.track_eta[i], aux.track_phi[i]) < 0.2) {
            genmatchedele1_trk = true;
          }
        }
      } 
      if (mumatched_1.size() != 0) {
        const math::XYZPoint mupos_1(mumatched_1[3], mumatched_1[0], mumatched_1[1]);
        mu1_md = (miss_dist(pv, pos_isv, mupos_1, pvarr, svarr).value());
        mu1_err = (miss_dist(pv, pos_isv, mupos_1, pvarr, svarr).error());
        // for (int i=0; i < nmuons; ++i) {
        //   if (mumatched_1[0] == aux.muon_eta[i]) {
        //     if (mumatched_1[1] == aux.muon_phi[i]) {
        //       genmatchedmu1_lep = true;
        //     }
        //   }
        // }
        for (int i = 0; i < ntracks; ++i) {
          mutk_dr.push_back(reco::deltaR(mumatched_1[0], mumatched_1[1], aux.track_eta[i], aux.track_phi[i]));
          if (reco::deltaR(mumatched_1[0], mumatched_1[1], aux.track_eta[i], aux.track_phi[i]) < 0.2) {
            genmatchedmu1_trk = true;
          }
        }
        //}
      }
    }

    // genmatchedele0_bylep.push_back(genmatchedele0_lep);
    // genmatchedmu0_bylep.push_back(genmatchedmu0_lep);
    // genmatchedele1_bylep.push_back(genmatchedele1_lep);
    // genmatchedmu1_bylep.push_back(genmatchedmu1_lep);
    genmatchedele0_bytrk.push_back(genmatchedele0_trk);
    genmatchedmu0_bytrk.push_back(genmatchedmu0_trk);
    genmatchedele1_bytrk.push_back(genmatchedele1_trk);
    genmatchedmu1_bytrk.push_back(genmatchedmu1_trk);


    mu_vtxtrk_dR.push_back(mutk_dr);
    el_vtxtrk_dR.push_back(eltk_dr);

    missdist_ele1.push_back(ele1_md);
    missdist_mu0.push_back(mu0_md);
    missdist_ele0.push_back(ele0_md);
    missdist_mu1.push_back(mu1_md);
    missdisterr_ele1.push_back(ele1_err);
    missdisterr_mu0.push_back(mu0_err);
    missdisterr_ele0.push_back(ele0_err);
    missdisterr_mu1.push_back(mu1_err);

    //this will be for all ... 
    h_sv_genv_mag->Fill(d.v(), w);
    if (closest_genvtx_flavor == 11) h_sv_ele_genv_mag->Fill(d.v(), w);
    if (closest_genvtx_flavor == 13) h_sv_mu_genv_mag->Fill(d.v(), w);
    if (closest_genvtx_flavor == 15) h_sv_tau_genv_mag->Fill(d.v(), w);

  }

  int good_match_sv0 = 0;
  int good_match_sv1 = 0;
  int eflavor = 0;
  int mflavor = 0;
  int evtx = 0;
  int mvtx = 0;

  // now its time to find the reconstructed vertices that are the closest to gen vertex 0 and gen vertex 1
  // also getting the index of the min element 
  if (genvertex0_dR.size() !=0) {
    float best_sv_gen0_dR = *min_element(genvertex0_dR.begin(), genvertex0_dR.end());
    int best_sv_gen0_isv = std::min_element(genvertex0_dR.begin(), genvertex0_dR.end()) - genvertex0_dR.begin();

    // these two cases should be filled if we have nsv == 2 or nsv == 1 (matched)
    if (best_sv_gen0_dR < 0.02) {
      // sv matches 
      // get the closest electron / muon to the sv in order to plot the tip/err/sig
      good_match_sv0 += 1;
      if (vtx_flavor[best_sv_gen0_isv][0]) {
        h_lepdau_wvtx_[0]->Fill(nelematched_0, w);
        eflavor +=1;
        if (nelematched_0){
          //minr, npxlayers, nstlayers, nsigmadxy
          const bool nm1[4] = {
            elematched_0[6] <= 1,
            elematched_0[7] >= 2,
            elematched_0[8] >= 6,
            abs(elematched_0[5]) > 4
          };

          const bool nm1_minr = nm1[1] && nm1[2] && nm1[3];
          const bool nm1_npxlayers = nm1[0] && nm1[2] && nm1[3];
          const bool nm1_nstlayers = nm1[0] && nm1[1] && nm1[3];
          const bool nm1_nsigmadxy = nm1[0] && nm1[1] && nm1[2];

          evtx +=1;
          h_lepdau_invtx_[0]->Fill(genmatchedele0_bytrk[best_sv_gen0_isv], w);
          if (genmatchedele0_bytrk[best_sv_gen0_isv]) {
            h_matchlep_pt_[0]->Fill(elematched_0[2], w);
            h_matchlep_dxy_[0]->Fill(abs(elematched_0[3]), w);
            h_matchlep_dxyerr_[0]->Fill(elematched_0[4], w);
            h_matchlep_nsigmadxy_[0]->Fill(abs(elematched_0[5]), w);
            h_matchlep_missdist_[0]->Fill(missdist_ele0[best_sv_gen0_isv], w);
            h_matchlep_missdisterr_[0]->Fill(missdisterr_ele0[best_sv_gen0_isv], w);
            h_matchlep_missdistsig_[0]->Fill(missdist_ele0[best_sv_gen0_isv]/missdisterr_ele0[best_sv_gen0_isv], w);
            h_matchlep_genvtx_pos_[0]->Fill(gensv[0], gensv[1], w);
            if (nm1_minr) h_matchlep_nm1_minr_[0]->Fill(elematched_0[6], w);
            if (nm1_npxlayers) h_matchlep_nm1_npxlayers_[0]->Fill(elematched_0[7], w);
            if (nm1_nstlayers) h_matchlep_nm1_nstlayers_[0]->Fill(elematched_0[8], w);
            if (nm1_nsigmadxy) h_matchlep_nm1_nsigmadxy_[0]->Fill(abs(elematched_0[5]), w);
          }

          else {
            h_nomatchlep_missdist_[0]->Fill(missdist_ele0[best_sv_gen0_isv], w);
            h_nomatchlep_missdisterr_[0]->Fill(missdisterr_ele0[best_sv_gen0_isv], w);
            h_nomatchlep_missdistsig_[0]->Fill(missdist_ele0[best_sv_gen0_isv]/missdisterr_ele0[best_sv_gen0_isv], w);
            h_nomatchlep_pt_[0]->Fill(elematched_0[2], w);
            h_nomatchlep_dxy_[0]->Fill(abs(elematched_0[3]), w);
            h_nomatchlep_dxyerr_[0]->Fill(elematched_0[4], w);
            h_nomatchlep_nsigmadxy_[0]->Fill(abs(elematched_0[5]), w);
            h_nomatchlep_genvtx_pos_[0]->Fill(gensv[0], gensv[1], w);
            if (nm1_minr) h_nomatchlep_nm1_minr_[0]->Fill(elematched_0[6], w);
            if (nm1_npxlayers) h_nomatchlep_nm1_npxlayers_[0]->Fill(elematched_0[7], w);
            if (nm1_nstlayers) h_nomatchlep_nm1_nstlayers_[0]->Fill(elematched_0[8], w);
            if (nm1_nsigmadxy) h_nomatchlep_nm1_nsigmadxy_[0]->Fill(abs(elematched_0[5]), w);
            if (el_vtxtrk_dR[best_sv_gen0_isv].size() != 0) {
              for (float dr : el_vtxtrk_dR[best_sv_gen0_isv]) {
                h_nomatchlep_trkdR_[0]->Fill(dr, w);
              }
            }
          }
        }

      }
      else if (vtx_flavor[best_sv_gen0_isv][1]) {
        h_lepdau_wvtx_[1]->Fill(nmumatched_0, w);
        mflavor +=1;
        if (nmumatched_0){
          mvtx +=1;
          const bool nm1[4] = {
            mumatched_0[6] <= 1,
            mumatched_0[7] >= 2,
            mumatched_0[8] >= 6,
            mumatched_0[5] > 4
          };

          const bool nm1_minr = nm1[1] && nm1[2] && nm1[3];
          const bool nm1_npxlayers = nm1[0] && nm1[2] && nm1[3];
          const bool nm1_nstlayers = nm1[0] && nm1[1] && nm1[3];
          const bool nm1_nsigmadxy = nm1[0] && nm1[1] && nm1[2];

          h_lepdau_invtx_[1]->Fill(genmatchedmu0_bytrk[best_sv_gen0_isv], w);
          if (genmatchedmu0_bytrk[best_sv_gen0_isv]) {
            h_matchlep_pt_[1]->Fill(mumatched_0[2], w);
            h_matchlep_dxy_[1]->Fill(abs(mumatched_0[3]), w);
            h_matchlep_dxyerr_[1]->Fill(mumatched_0[4], w);
            h_matchlep_nsigmadxy_[1]->Fill(abs(mumatched_0[5]), w);
            h_matchlep_missdist_[1]->Fill(missdist_mu0[best_sv_gen0_isv], w);
            h_matchlep_missdisterr_[1]->Fill(missdisterr_mu0[best_sv_gen0_isv], w);
            h_matchlep_missdistsig_[1]->Fill(missdist_mu0[best_sv_gen0_isv]/missdisterr_mu0[best_sv_gen0_isv], w);
            h_matchlep_genvtx_pos_[1]->Fill(gensv[0], gensv[1], w);
            if (nm1_minr) h_matchlep_nm1_minr_[1]->Fill(mumatched_0[6], w);
            if (nm1_npxlayers) h_matchlep_nm1_npxlayers_[1]->Fill(mumatched_0[7], w);
            if (nm1_nstlayers) h_matchlep_nm1_nstlayers_[1]->Fill(mumatched_0[8], w);
            if (nm1_nsigmadxy) h_matchlep_nm1_nsigmadxy_[1]->Fill(abs(mumatched_0[5]), w);
          }
          else {
            h_nomatchlep_missdist_[1]->Fill(missdist_mu0[best_sv_gen0_isv], w);
            h_nomatchlep_missdisterr_[1]->Fill(missdisterr_mu0[best_sv_gen0_isv], w);
            h_nomatchlep_missdistsig_[1]->Fill(missdist_mu0[best_sv_gen0_isv]/missdisterr_mu0[best_sv_gen0_isv], w);
            h_nomatchlep_pt_[1]->Fill(mumatched_0[2], w);
            h_nomatchlep_dxy_[1]->Fill(abs(mumatched_0[3]), w);
            h_matchlep_dxyerr_[1]->Fill(mumatched_0[4], w);
            h_matchlep_nsigmadxy_[1]->Fill(abs(mumatched_0[5]), w);
            h_nomatchlep_genvtx_pos_[1]->Fill(gensv[0], gensv[1], w);
            if (nm1_minr) h_nomatchlep_nm1_minr_[1]->Fill(mumatched_0[6], w);
            if (nm1_npxlayers) h_nomatchlep_nm1_npxlayers_[1]->Fill(mumatched_0[7], w);
            if (nm1_nstlayers) h_nomatchlep_nm1_nstlayers_[1]->Fill(mumatched_0[8], w);
            if (nm1_nsigmadxy) h_nomatchlep_nm1_nsigmadxy_[1]->Fill(abs(mumatched_0[5]), w);
            if (mu_vtxtrk_dR[best_sv_gen0_isv].size() != 0) {
              for (float dr : mu_vtxtrk_dR[best_sv_gen0_isv]) {
                h_nomatchlep_trkdR_[1]->Fill(dr, w);
              }
            }
          }
        }
      }
    }
  }
  if (genvertex1_dR.size() !=0) {
    float best_sv_gen1_dR = *min_element(genvertex1_dR.begin(), genvertex1_dR.end());
    int best_sv_gen1_isv = std::min_element(genvertex1_dR.begin(), genvertex1_dR.end()) - genvertex1_dR.begin();
    if (best_sv_gen1_dR < 0.02) {
      // sv matches 
      good_match_sv1 += 1;
      if (vtx_flavor[best_sv_gen1_isv][0]) {
        eflavor +=1;
        h_lepdau_wvtx_[0]->Fill(nelematched_1, w);
        if (nelematched_1){
          evtx +=1;
          const bool nm1[4] = {
            elematched_1[6] <= 1,
            elematched_1[7] >= 2,
            elematched_1[8] >= 6,
            elematched_1[5] > 4
          };

          const bool nm1_minr = nm1[1] && nm1[2] && nm1[3];
          const bool nm1_npxlayers = nm1[0] && nm1[2] && nm1[3];
          const bool nm1_nstlayers = nm1[0] && nm1[1] && nm1[3];
          const bool nm1_nsigmadxy = nm1[0] && nm1[1] && nm1[2];

          h_lepdau_invtx_[0]->Fill(genmatchedele1_bytrk[best_sv_gen1_isv], w);
          if (genmatchedele1_bytrk[best_sv_gen1_isv]) {
            h_matchlep_pt_[0]->Fill(elematched_1[2], w);
            h_matchlep_dxy_[0]->Fill(abs(elematched_1[3]), w);
            h_matchlep_dxyerr_[0]->Fill(elematched_1[4], w);
            h_matchlep_nsigmadxy_[0]->Fill(abs(elematched_1[5]), w);
            h_matchlep_missdist_[0]->Fill(missdist_ele1[best_sv_gen1_isv], w);
            h_matchlep_missdisterr_[0]->Fill(missdisterr_ele1[best_sv_gen1_isv], w);
            h_matchlep_missdistsig_[0]->Fill(missdist_ele1[best_sv_gen1_isv]/missdisterr_ele1[best_sv_gen1_isv], w);
            h_matchlep_genvtx_pos_[0]->Fill(gensv[2], gensv[3], w);
            if (nm1_minr) h_matchlep_nm1_minr_[0]->Fill(elematched_1[6], w);
            if (nm1_npxlayers) h_matchlep_nm1_npxlayers_[0]->Fill(elematched_1[7], w);
            if (nm1_nstlayers) h_matchlep_nm1_nstlayers_[0]->Fill(elematched_1[8], w);
            if (nm1_nsigmadxy) h_matchlep_nm1_nsigmadxy_[0]->Fill(abs(elematched_1[5]), w);
          }
          else {
            h_nomatchlep_pt_[0]->Fill(elematched_1[2], w);
            h_nomatchlep_dxy_[0]->Fill(abs(elematched_1[3]), w);
            h_nomatchlep_dxyerr_[0]->Fill(elematched_1[4], w);
            h_nomatchlep_nsigmadxy_[0]->Fill(abs(elematched_1[5]), w);
            h_nomatchlep_missdist_[0]->Fill(missdist_ele1[best_sv_gen1_isv], w);
            h_nomatchlep_missdisterr_[0]->Fill(missdisterr_ele1[best_sv_gen1_isv], w);
            h_nomatchlep_missdistsig_[0]->Fill(missdist_ele1[best_sv_gen1_isv]/missdisterr_ele1[best_sv_gen1_isv], w);
            h_nomatchlep_genvtx_pos_[0]->Fill(gensv[2], gensv[3], w);
            if (nm1_minr) h_nomatchlep_nm1_minr_[0]->Fill(elematched_1[6], w);
            if (nm1_npxlayers) h_nomatchlep_nm1_npxlayers_[0]->Fill(elematched_1[7], w);
            if (nm1_nstlayers) h_nomatchlep_nm1_nstlayers_[0]->Fill(elematched_1[8], w);
            if (nm1_nsigmadxy) h_nomatchlep_nm1_nsigmadxy_[0]->Fill(abs(elematched_1[5]), w);
            if (el_vtxtrk_dR[best_sv_gen1_isv].size() != 0) {
              for (float dr : el_vtxtrk_dR[best_sv_gen1_isv]) {
                h_nomatchlep_trkdR_[0]->Fill(dr, w);
              }
            }
          }
        }
      }
      else if (vtx_flavor[best_sv_gen1_isv][1]) {
        h_lepdau_wvtx_[1]->Fill(nmumatched_1, w);
        mflavor +=1;   
        if (nmumatched_1){
          mvtx +=1;
          const bool nm1[4] = {
            mumatched_1[6] <= 1,
            mumatched_1[7] >= 2,
            mumatched_1[8] >= 6,
            mumatched_1[5] > 4
          };

          const bool nm1_minr = nm1[1] && nm1[2] && nm1[3];
          const bool nm1_npxlayers = nm1[0] && nm1[2] && nm1[3];
          const bool nm1_nstlayers = nm1[0] && nm1[1] && nm1[3];
          const bool nm1_nsigmadxy = nm1[0] && nm1[1] && nm1[2];

          h_nmsv->Fill(1,w);
          h_lepdau_invtx_[1]->Fill(genmatchedmu1_bytrk[best_sv_gen1_isv], w);
          if (genmatchedmu1_bytrk[best_sv_gen1_isv]) {
            h_matchlep_pt_[1]->Fill(mumatched_1[2], w);
            h_matchlep_dxy_[1]->Fill(abs(mumatched_1[3]), w);
            h_matchlep_dxyerr_[1]->Fill(mumatched_1[4], w);
            h_matchlep_nsigmadxy_[1]->Fill(abs(mumatched_1[5]), w);
            h_matchlep_missdist_[1]->Fill(missdist_mu1[best_sv_gen1_isv], w);
            h_matchlep_missdisterr_[1]->Fill(missdisterr_mu1[best_sv_gen1_isv], w);
            h_matchlep_missdistsig_[1]->Fill(missdist_mu1[best_sv_gen1_isv]/missdisterr_mu1[best_sv_gen1_isv], w);
            h_matchlep_genvtx_pos_[1]->Fill(gensv[2], gensv[3], w);
            if (nm1_minr) h_matchlep_nm1_minr_[1]->Fill(mumatched_1[6], w);
            if (nm1_npxlayers) h_matchlep_nm1_npxlayers_[1]->Fill(mumatched_1[7], w);
            if (nm1_nstlayers) h_matchlep_nm1_nstlayers_[1]->Fill(mumatched_1[8], w);
            if (nm1_nsigmadxy) h_matchlep_nm1_nsigmadxy_[1]->Fill(abs(mumatched_1[5]), w);
          }
          else {
            h_nomatchlep_pt_[1]->Fill(mumatched_1[2], w);
            h_nomatchlep_missdist_[1]->Fill(missdist_mu1[best_sv_gen1_isv], w);
            h_nomatchlep_missdisterr_[1]->Fill(missdisterr_mu1[best_sv_gen1_isv], w);
            h_nomatchlep_missdistsig_[1]->Fill(missdist_mu1[best_sv_gen1_isv]/missdisterr_mu1[best_sv_gen1_isv], w);
            h_nomatchlep_dxy_[1]->Fill(abs(mumatched_1[3]), w);
            h_nomatchlep_dxyerr_[1]->Fill(mumatched_1[4], w);
            h_nomatchlep_nsigmadxy_[1]->Fill(abs(mumatched_1[5]), w);
            h_nomatchlep_genvtx_pos_[1]->Fill(gensv[2], gensv[3], w);
            if (nm1_minr) h_nomatchlep_nm1_minr_[1]->Fill(mumatched_1[6], w);
            if (nm1_npxlayers) h_nomatchlep_nm1_npxlayers_[1]->Fill(mumatched_1[7], w);
            if (nm1_nstlayers) h_nomatchlep_nm1_nstlayers_[1]->Fill(mumatched_1[8], w);
            if (nm1_nsigmadxy) h_nomatchlep_nm1_nsigmadxy_[1]->Fill(abs(mumatched_1[5]), w);
            if (mu_vtxtrk_dR[best_sv_gen1_isv].size() != 0) {
              for (float dr : mu_vtxtrk_dR[best_sv_gen1_isv]) {
                h_nomatchlep_trkdR_[1]->Fill(dr, w);
              }
            }
          }
        }
      }
    }
  }

  if (!good_match_sv0) {
    if (genele0) h_lepdau_novtx_[0]->Fill(nelematched_0, w);
    if (genmu0) h_lepdau_novtx_[1]->Fill(nmumatched_0, w);
  }
  
  if (!good_match_sv1) {
    if (genele1) h_lepdau_novtx_[0]->Fill(nelematched_1, w);
    if (genmu1) h_lepdau_novtx_[1]->Fill(nmumatched_1, w); 
  }

  // if possible, fill and take care of all lepton associated to vertices information 
  h_nsv_wlep->Fill(nsv_wassoclept, w);
  h_nsv_genmatched->Fill(good_match_sv0+good_match_sv1, w);

  if (genlep_dau[0] > 0 ) {
    h_nsv_eflavor->Fill(eflavor,w);
    h_nesv->Fill(evtx,w);
  }
  if (genlep_dau[1] > 0 ) {
    h_nsv_mflavor->Fill(mflavor,w);
    h_nmsv->Fill(mvtx,w);
  }
  if (genlep_dau[0] > 0 || genlep_dau[1] > 0) {
    h_nsv_emuflavor->Fill(eflavor + mflavor,w);
    h_nemusv->Fill(evtx+mvtx,w);
  }

  if (nsv >= 2) {
    const MFVVertexAux& sv0 = auxes->at(0);
    const MFVVertexAux& sv1 = auxes->at(1);
    h_sv_ntk0_ntk1->Fill(sv0.ntracks(), sv1.ntracks(), w);
    double svdist2d = mag(sv0.x - sv1.x, sv0.y - sv1.y);
    double svdist3d = mag(sv0.x - sv1.x, sv0.y - sv1.y, sv0.z - sv1.z);
    h_svdist2d->Fill(svdist2d, w);
    h_svdist3d->Fill(svdist3d, w);
    h_sv0pvdz_v_sv1pvdz->Fill(sv0.pvdz(), sv1.pvdz(), w);
    h_sv0pvdzsig_v_sv1pvdzsig->Fill(sv0.pvdzsig(), sv1.pvdzsig(), w);
    double phi0 = atan2(sv0.y - bsy, sv0.x - bsx);
    double phi1 = atan2(sv1.y - bsy, sv1.x - bsx);
    h_absdeltaphi01->Fill(fabs(reco::deltaPhi(phi0, phi1)), w);

    h_fractrackssharedwpv01 ->Fill(float(sv0.ntrackssharedwpv () + sv1.ntrackssharedwpv ())/(sv0.ntracks() + sv1.ntracks()), w);
    h_fractrackssharedwpvs01->Fill(float(sv0.ntrackssharedwpvs() + sv1.ntrackssharedwpvs())/(sv0.ntracks() + sv1.ntracks()), w);
    h_pvmosttracksshared->Fill(sv0.ntrackssharedwpvs() ? sv0.pvmosttracksshared() : -1,
                               sv1.ntrackssharedwpvs() ? sv1.pvmosttracksshared() : -1,
                               w);

    std::vector<std::vector<int> > sv_track_which_jet;
    for (int isv = 0; isv < nsv; ++isv) {
      const MFVVertexAux& aux = auxes->at(isv);
      const int ntracks = aux.ntracks();
  
      std::vector<int> track_which_jet;
      for (int i = 0; i < ntracks; ++i) {
        double match_threshold = 1.3;
        int jet_index = 255;
        for (unsigned j = 0; j < mevent->jet_track_which_jet.size(); ++j) {
          double a = fabs(aux.track_pt(i) - fabs(mevent->jet_track_qpt[j])) + 1;
          double b = fabs(aux.track_eta[i] - mevent->jet_track_eta[j]) + 1;
          double c = fabs(aux.track_phi[i] - mevent->jet_track_phi[j]) + 1;
          if (a * b * c < match_threshold) {
            match_threshold = a * b * c;
            jet_index = mevent->jet_track_which_jet[j];
          }
        }
        if (jet_index != 255) {
          track_which_jet.push_back((int) jet_index);
        }
      }
      sv_track_which_jet.push_back(track_which_jet);
    }
  
    bool shared_jet = std::find_first_of (sv_track_which_jet[0].begin(), sv_track_which_jet[0].end(), sv_track_which_jet[1].begin(), sv_track_which_jet[1].end()) != sv_track_which_jet[0].end();
    h_sv_shared_jets->Fill(shared_jet, w);
    if (shared_jet) {
      h_svdist2d_shared_jets->Fill(svdist2d, w);
      h_absdeltaphi01_shared_jets->Fill(fabs(reco::deltaPhi(phi0, phi1)), w);
    } else {
      h_svdist2d_no_shared_jets->Fill(svdist2d, w);
      h_absdeltaphi01_no_shared_jets->Fill(fabs(reco::deltaPhi(phi0, phi1)), w);
    }
  }

  // number of jets associated with SVs
  for (int isv = 0; isv < nsv; ++isv) {
    const MFVVertexAux& aux = auxes->at(isv);
    const int ntracks = aux.ntracks();
    std::set<int> sv_jetasso;
    for (int i = 0; i < ntracks; ++i) {
	    double match_threshold = 1.3;
	    int jet_index = 255;
	    for (unsigned j = 0; j < mevent->jet_track_which_jet.size(); ++j) {
	      double a = fabs(aux.track_pt(i) - fabs(mevent->jet_track_qpt[j])) + 1;
	      double b = fabs(aux.track_eta[i] - mevent->jet_track_eta[j]) + 1;
	      double c = fabs(aux.track_phi[i] - mevent->jet_track_phi[j]) + 1;
	      if (a * b * c < match_threshold) {
	        match_threshold = a * b * c;
	        jet_index = mevent->jet_track_which_jet[j];
	      }
	    }
	    if (jet_index != 255) {
        sv_jetasso.insert((int) jet_index);
	    }
    }
    h_sv_ntk_njet->Fill(ntracks, sv_jetasso.size(), w);
  } 
}

DEFINE_FWK_MODULE(MFVVertexHistos);
