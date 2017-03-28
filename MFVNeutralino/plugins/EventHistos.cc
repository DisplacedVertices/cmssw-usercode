#include "TH2F.h"
#include "TRandom3.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralino/interface/EventTools.h"

#define NBDISC 2

class MFVEventHistos : public edm::EDAnalyzer {
 public:
  explicit MFVEventHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::EDGetTokenT<MFVEvent> mevent_token;
  const edm::EDGetTokenT<double> weight_token;
  const std::vector<double> force_bs;
  const edm::InputTag primary_vertex_src;
  const edm::InputTag jets_src;

  TH1F* h_w;

  TH2F* h_gen_decay;
  TH1F* h_gen_partons_in_acc;
  TH1F* h_gen_flavor_code;

  TH1F* h_nbquarks;
  TH1F* h_bquark_pt;
  TH1F* h_bquark_eta;
  TH1F* h_bquark_phi;
  TH1F* h_bquark_energy;
  TH1F* h_bquark_pairdphi;
  TH1F* h_bquark_pairdr;
  TH1F* h_bquarks_absdphi;
  TH1F* h_bquarks_dphi;
  TH1F* h_bquarks_deta;
  TH2F* h_bquarks_deta_dphi;
  TH1F* h_bquarks_avgeta;
  TH2F* h_bquarks_avgeta_dphi;
  TH1F* h_bquarks_dR;
  TH2F* h_bquarks_dR_dphi;

  TH1F* h_minlspdist2d;
  TH1F* h_lspdist2d;
  TH1F* h_lspdist3d;

  TH1F* h_hlt_bits;
  TH1F* h_hlt_cross;
  TH1F* h_l1_bits;

  TH1F* h_npu;

  TH1F* h_bsx;
  TH1F* h_bsy;
  TH1F* h_bsz;
  TH1F* h_bsphi;

  TH1F* h_npv;
  TH1F* h_pvx;
  TH1F* h_pvy;
  TH1F* h_pvz;
  TH1F* h_pvcxx;
  TH1F* h_pvcxy;
  TH1F* h_pvcxz;
  TH1F* h_pvcyy;
  TH1F* h_pvcyz;
  TH1F* h_pvczz;
  TH1F* h_pvrho;
  TH1F* h_pvphi;
  TH1F* h_pvntracks;
  TH1F* h_pvsumpt2;

  TH1F* h_njets;
  TH1F* h_njetsnopu[3];
  TH1F* h_jetpt1;
  TH1F* h_jetpt2;
  TH1F* h_jetpt3;
  TH1F* h_jetpt4;
  TH1F* h_jetpt5;
  TH1F* h_jetpt6;
  TH1F* h_jet_ht;
  TH1F* h_jet_ht_40;

  TH1F* h_jet_pt;
  TH1F* h_jet_eta;
  TH1F* h_jet_phi;
  TH1F* h_jet_energy;
  TH1F* h_jet_pairdphi;
  TH1F* h_jet_pairdr;

  TH1F* h_jet_Fox_Wolfram[11];
  TH1F* h_jet_ST;
  TH1F* h_jetlep_ST;

  TH2F* h_jet_ST_njets;
  TH2F* h_jet_ST_ht;
  TH2F* h_jet_ST_ht40;

  TH1F* h_met;
  TH1F* h_metphi;

  TH1F* h_nbtags[3];
  TH1F* h_nmuons[3];
  TH1F* h_nelectrons[3];
  TH1F* h_nleptons[3];

  TH1F* h_bjet_pt[3];
  TH1F* h_bjet_eta[3];
  TH1F* h_bjet_phi[3];
  TH1F* h_bjet_energy[3];
  TH1F* h_bjet_pairdphi[3];
  TH1F* h_bjet_pairdr[3];

  TH1F* h_bjets_absdphi[3][2];
  TH1F* h_bjets_dphi[3][2];
  TH1F* h_bjets_deta[3][2];
  TH2F* h_bjets_deta_dphi[3][2];
  TH1F* h_bjets_avgeta[3][2];
  TH2F* h_bjets_avgeta_dphi[3][2];
  TH1F* h_bjets_dR[3][2];
  TH2F* h_bjets_dR_dphi[3][2];

  TH1F* h_leptons_pt[2][3];
  TH1F* h_leptons_eta[2][3];
  TH1F* h_leptons_phi[2][3];
  TH1F* h_leptons_dxy[2][3];
  TH1F* h_leptons_dxybs[2][3];
  TH1F* h_leptons_dz[2][3];
  TH1F* h_leptons_iso[2][3];
  TH1F* h_leptons_iso_neargenel_hardint[2][3];
  TH1F* h_leptons_iso_neargenmu_hardint[2][3];
  TH1F* h_leptons_iso_neargenb[2][3];
  TH1F* h_leptons_iso_nearnothing[2][3];

  TH1F* h_leptons_iso_0e0mu[2][3];
  TH1F* h_leptons_iso_1e0mu[2][3];
  TH1F* h_leptons_iso_0e1mu[2][3];
  TH1F* h_leptons_iso_1e1mu[2][3];
  TH1F* h_leptons_iso_2e0mu[2][3];
  TH1F* h_leptons_iso_0e2mu[2][3];

  TH1F* h_leptons_iso_0e0mu_neargenel[2][3];
  TH1F* h_leptons_iso_1e0mu_neargenel[2][3];
  TH1F* h_leptons_iso_0e1mu_neargenel[2][3];
  TH1F* h_leptons_iso_1e1mu_neargenel[2][3];
  TH1F* h_leptons_iso_2e0mu_neargenel[2][3];
  TH1F* h_leptons_iso_0e2mu_neargenel[2][3];

  TH1F* h_leptons_iso_0e0mu_neargenel_hardint[2][3];
  TH1F* h_leptons_iso_1e0mu_neargenel_hardint[2][3];
  TH1F* h_leptons_iso_0e1mu_neargenel_hardint[2][3];
  TH1F* h_leptons_iso_1e1mu_neargenel_hardint[2][3];
  TH1F* h_leptons_iso_2e0mu_neargenel_hardint[2][3];
  TH1F* h_leptons_iso_0e2mu_neargenel_hardint[2][3];

  TH1F* h_leptons_iso_0e0mu_neargenmu[2][3];
  TH1F* h_leptons_iso_1e0mu_neargenmu[2][3];
  TH1F* h_leptons_iso_0e1mu_neargenmu[2][3];
  TH1F* h_leptons_iso_1e1mu_neargenmu[2][3];
  TH1F* h_leptons_iso_2e0mu_neargenmu[2][3];
  TH1F* h_leptons_iso_0e2mu_neargenmu[2][3];

  TH1F* h_leptons_iso_0e0mu_neargenmu_hardint[2][3];
  TH1F* h_leptons_iso_1e0mu_neargenmu_hardint[2][3];
  TH1F* h_leptons_iso_0e1mu_neargenmu_hardint[2][3];
  TH1F* h_leptons_iso_1e1mu_neargenmu_hardint[2][3];
  TH1F* h_leptons_iso_2e0mu_neargenmu_hardint[2][3];
  TH1F* h_leptons_iso_0e2mu_neargenmu_hardint[2][3];

  TH1F* h_leptons_iso_0e0mu_neargenb[2][3];
  TH1F* h_leptons_iso_1e0mu_neargenb[2][3];
  TH1F* h_leptons_iso_0e1mu_neargenb[2][3];
  TH1F* h_leptons_iso_1e1mu_neargenb[2][3];
  TH1F* h_leptons_iso_2e0mu_neargenb[2][3];
  TH1F* h_leptons_iso_0e2mu_neargenb[2][3];

  TH1F* h_leptons_iso_0e0mu_nearnothing[2][3];
  TH1F* h_leptons_iso_1e0mu_nearnothing[2][3];
  TH1F* h_leptons_iso_0e1mu_nearnothing[2][3];
  TH1F* h_leptons_iso_1e1mu_nearnothing[2][3];
  TH1F* h_leptons_iso_2e0mu_nearnothing[2][3];
  TH1F* h_leptons_iso_0e2mu_nearnothing[2][3];

  TH1F* h_muons_absdphi[3];
  TH1F* h_muons_dphi[3];
  TH1F* h_muons_deta[3];
  TH2F* h_muons_deta_dphi[3];
  TH1F* h_muons_avgeta[3];
  TH2F* h_muons_avgeta_dphi[3];
  TH1F* h_muons_dR[3];
  TH2F* h_muons_dR_dphi[3];

  TH1F* h_jet_svnvertices;
  TH1F* h_jet_svntracks;
  TH1F* h_jet_svsumpt2;
  TH1F* h_jet_svx;
  TH1F* h_jet_svy;
  TH1F* h_jet_svz;
  TH2F* h_jet_svyx;
  TH2F* h_jet_svzr;
  TH2F* h_jet_momphi_posphi;
  TH1F* h_jet_svcxx;
  TH1F* h_jet_svcxy;
  TH1F* h_jet_svcxz;
  TH1F* h_jet_svcyy;
  TH1F* h_jet_svcyz;
  TH1F* h_jet_svczz;
  TH1F* h_jet_svpv2ddist;
  TH1F* h_jet_svpv2derr;
  TH1F* h_jet_svpv2dsig;

  TH1F* h_jetsv_absdphi;
  TH1F* h_jetsv_dxy;
  TH1F* h_jetsv_dxyerr;
  TH1F* h_jetsv_dxysig;
  TH1F* h_jetsv_dz;
  TH1F* h_jetsv_dzerr;
  TH1F* h_jetsv_dzsig;
  TH1F* h_jetsv_d3d;
  TH1F* h_jetsv_d3derr;
  TH1F* h_jetsv_d3dsig;

  TH1F* h_bjetsv_absdphi;
  TH1F* h_bjetsv_dxy;
  TH1F* h_bjetsv_dxyerr;
  TH1F* h_bjetsv_dxysig;
  TH1F* h_bjetsv_dz;
  TH1F* h_bjetsv_dzerr;
  TH1F* h_bjetsv_dzsig;
  TH1F* h_bjetsv_d3d;
  TH1F* h_bjetsv_d3derr;
  TH1F* h_bjetsv_d3dsig;

  TH1F* h_pv_n;
  TH1F* h_pv_x[4];
  TH1F* h_pv_y[4];
  TH1F* h_pv_z[4];
  TH1F* h_pv_rho[4];
  TH1F* h_pv_phi[4];
  TH1F* h_pv_ntracks[4];
  TH1F* h_pv_sumpt2[4];

  TH1F* h_jets_n;
  TH1F* h_jets_pt;
  TH1F* h_jets_eta;
  TH1F* h_jets_phi;

  TH1F* h_bjets_n[NBDISC][3];
  TH1F* h_bjets_pt[NBDISC][3];
  TH1F* h_bjets_eta[NBDISC][3];
  TH1F* h_bjets_phi[NBDISC][3];

  TH1F* h_n_vertex_seed_tracks;
  TH1F* h_vertex_seed_track_chi2dof;
  TH1F* h_vertex_seed_track_q;
  TH1F* h_vertex_seed_track_pt;
  TH1F* h_vertex_seed_track_eta;
  TH1F* h_vertex_seed_track_phi;
  TH1F* h_vertex_seed_track_dxy;
  TH1F* h_vertex_seed_track_dz;
  TH1F* h_vertex_seed_track_npxhits;
  TH1F* h_vertex_seed_track_nsthits;
  TH1F* h_vertex_seed_track_nhits;
  TH1F* h_vertex_seed_track_npxlayers;
  TH1F* h_vertex_seed_track_nstlayers;
  TH1F* h_vertex_seed_track_nlayers;
};

MFVEventHistos::MFVEventHistos(const edm::ParameterSet& cfg)
  : mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
    force_bs(cfg.getParameter<std::vector<double> >("force_bs")),
    primary_vertex_src(cfg.getParameter<edm::InputTag>("primary_vertex_src")),
    jets_src(cfg.getParameter<edm::InputTag>("jets_src"))
{
  if (force_bs.size() && force_bs.size() != 3)
    throw cms::Exception("Misconfiguration", "force_bs must be empty or size 3");

  edm::Service<TFileService> fs;

  h_w = fs->make<TH1F>("h_w", ";event weight;events/0.1", 100, 0, 10);

  h_gen_decay = fs->make<TH2F>("h_gen_decay", "0-2=e,mu,tau, 3=h;decay code #0;decay code #1", 4, 0, 4, 4, 0, 4);
  h_gen_partons_in_acc = fs->make<TH1F>("h_gen_partons_in_acc", ";# partons from LSP in acceptance;events", 11, 0, 11);
  h_gen_flavor_code = fs->make<TH1F>("h_gen_flavor_code", ";quark flavor composition;events", 3, 0, 3);

  h_nbquarks = fs->make<TH1F>("h_nbquarks", ";# of bquarks;events", 20, 0, 20);
  h_bquark_pt = fs->make<TH1F>("h_bquark_pt", ";bquarks p_{T} (GeV);bquarks/10 GeV", 100, 0, 1000);
  h_bquark_eta = fs->make<TH1F>("h_bquark_eta", ";bquarks #eta (rad);bquarks/.08", 100, -4, 4);
  h_bquark_phi = fs->make<TH1F>("h_bquark_phi", ";bquarks #phi (rad);bquarks/.063", 100, -3.1416, 3.1416);
  h_bquark_energy = fs->make<TH1F>("h_bquark_energy", ";bquarks energy (GeV);bquarks/10 GeV", 100, 0, 1000);
  h_bquark_pairdphi = fs->make<TH1F>("h_bquark_pairdphi", ";bquark pair #Delta#phi (rad);bquark pairs/.063", 100, -3.1416, 3.1416);
  h_bquark_pairdr = fs->make<TH1F>("h_bquark_pairdr", ";bquark pair #DeltaR (rad);bquark pairs/.047", 150, 0, 7);
  h_bquarks_absdphi = fs->make<TH1F>("h_bquarks_absdphi", "events with two bquarks;|#Delta#phi|;Events/0.126", 25, 0, 3.15);
  h_bquarks_dphi = fs->make<TH1F>("h_bquarks_dphi", "events with two bquarks;#Delta#phi;Events/0.126", 50, -3.15, 3.15);
  h_bquarks_deta = fs->make<TH1F>("h_bquarks_deta", "events with two bquarks;#Delta#eta;Events/0.16", 50, -4, 4);
  h_bquarks_deta_dphi = fs->make<TH2F>("h_bquarks_deta_dphi", "events with two bquarks;#Delta#phi;#Delta#eta", 50, -3.15, 3.15, 50, -4, 4);
  h_bquarks_avgeta = fs->make<TH1F>("h_bquarks_avgeta", "events with two bquarks;avg #eta;Events/0.16", 50, -4, 4);
  h_bquarks_avgeta_dphi = fs->make<TH2F>("h_bquarks_avgeta_dphi", "events with two bquarks;#Delta#phi;avg #eta", 50, -3.15, 3.15, 50, -4, 4);
  h_bquarks_dR = fs->make<TH1F>("h_bquarks_dR", "events with two bquarks;#Delta R;Events/0.14", 50, 0, 7);
  h_bquarks_dR_dphi = fs->make<TH2F>("h_bquarks_dR_dphi", "events with two bquarks;#Delta#phi;#Delta R", 50, -3.15, 3.15, 50, 0, 7);

  h_minlspdist2d = fs->make<TH1F>("h_minlspdist2d", ";min dist2d(gen vtx #i) (cm);events/0.1 mm", 200, 0, 2);
  h_lspdist2d = fs->make<TH1F>("h_lspdist2d", ";dist2d(gen vtx #0, #1) (cm);events/0.1 mm", 200, 0, 2);
  h_lspdist3d = fs->make<TH1F>("h_lspdist3d", ";dist3d(gen vtx #0, #1) (cm);events/0.1 mm", 200, 0, 2);

  h_hlt_bits = fs->make<TH1F>("h_hlt_bits", ";;events", 2*mfv::n_hlt_paths+1, 0, 2*mfv::n_hlt_paths+1);
  h_hlt_cross = fs->make<TH1F>("h_hlt_cross", ";;events", 6, 0, 6);
  h_l1_bits  = fs->make<TH1F>("h_l1_bits",  ";;events", 2*mfv::n_l1_paths +1, 0, 2*mfv::n_l1_paths +1);

  h_hlt_bits->GetXaxis()->SetBinLabel(1, "nevents");
  for (int i = 0; i < mfv::n_hlt_paths; ++i) {
    h_hlt_bits->GetXaxis()->SetBinLabel(1+2*i+1, TString::Format("found %s", mfv::hlt_paths[i]));
    h_hlt_bits->GetXaxis()->SetBinLabel(1+2*i+2, TString::Format(" pass %s", mfv::hlt_paths[i]));
  }
  h_l1_bits->GetXaxis()->SetBinLabel(1, "nevents");
  for (int i = 0; i < mfv::n_l1_paths; ++i) {
    h_l1_bits->GetXaxis()->SetBinLabel(1+2*i+1, TString::Format("found %s", mfv::l1_paths[i]));
    h_l1_bits->GetXaxis()->SetBinLabel(1+2*i+2, TString::Format(" pass %s", mfv::l1_paths[i]));
  }

  h_hlt_cross->GetXaxis()->SetBinLabel(1, "nevents");
  h_hlt_cross->GetXaxis()->SetBinLabel(2, "HT800 && !HT900");
  h_hlt_cross->GetXaxis()->SetBinLabel(3, "Jet450 && !HT800");
  h_hlt_cross->GetXaxis()->SetBinLabel(4, "Jet450 && !HT900");
  h_hlt_cross->GetXaxis()->SetBinLabel(5, "AK8Jet450 && !HT800");
  h_hlt_cross->GetXaxis()->SetBinLabel(6, "AK8Jet450 && !HT900");

  h_npu = fs->make<TH1F>("h_npu", ";true nPU;events", 65, 0, 65);

  h_bsx = fs->make<TH1F>("h_bsx", ";beamspot x (cm);events/0.1 mm", 200, -1, 1);
  h_bsy = fs->make<TH1F>("h_bsy", ";beamspot y (cm);events/0.1 mm", 200, -1, 1);
  h_bsz = fs->make<TH1F>("h_bsz", ";beamspot z (cm);events/mm", 200, -10, 10);
  h_bsphi = fs->make<TH1F>("h_bsphi", ";beamspot #phi (rad);events/.063", 100, -3.1416, 3.1416);

  h_npv = fs->make<TH1F>("h_npv", ";# of primary vertices;events", 65, 0, 65);
  h_pvx = fs->make<TH1F>("h_pvx", ";primary vertex x (cm);events/10 #mum", 200, -0.1, 0.1);
  h_pvy = fs->make<TH1F>("h_pvy", ";primary vertex y (cm);events/10 #mum", 200, -0.1, 0.1);
  h_pvz = fs->make<TH1F>("h_pvz", ";primary vertex z (cm);events/1.5 mm", 200, -15, 15);
  h_pvcxx = fs->make<TH1F>("h_pvcxx", ";primary vertex cxx;events", 100, -1e-6, 1e-6);
  h_pvcxy = fs->make<TH1F>("h_pvcxy", ";primary vertex cxy;events", 100, -1e-6, 1e-6);
  h_pvcxz = fs->make<TH1F>("h_pvcxz", ";primary vertex cxz;events", 100, -1e-6, 1e-6);
  h_pvcyy = fs->make<TH1F>("h_pvcyy", ";primary vertex cyy;events", 100, -1e-6, 1e-6);
  h_pvcyz = fs->make<TH1F>("h_pvcyz", ";primary vertex cyz;events", 100, -1e-6, 1e-6);
  h_pvczz = fs->make<TH1F>("h_pvczz", ";primary vertex czz;events", 100, -1e-6, 1e-6);
  h_pvrho = fs->make<TH1F>("h_pv_rho", ";PV rho (cm);events/5 #mum", 200, 0, 0.1);
  h_pvphi = fs->make<TH1F>("h_pv_phi", ";primary vertex #phi (rad);events/.063", 100, -3.1416, 3.1416);
  h_pvntracks = fs->make<TH1F>("h_pv_ntracks", ";# of tracks in primary vertex;events", 200, 0, 200);
  h_pvsumpt2 = fs->make<TH1F>("h_pv_sumpt2", ";PV #Sigma p_{T}^{2} (GeV^{2});events/100 GeV^{2}", 200, 0, 20000);
  const char* lmt_ex[3] = {"loose", "medium", "tight"};

  h_njets = fs->make<TH1F>("h_njets", ";# of jets;events", 20, 0, 20);
  for (int i = 0; i < 3; ++i)
    h_njetsnopu[i] = fs->make<TH1F>(TString::Format("h_njetsnopu_%s", lmt_ex[i]), TString::Format(";# of jets (%s PU id);events", lmt_ex[i]), 20, 0, 20);
  h_jetpt1 = fs->make<TH1F>("h_jetpt1", ";p_{T} of 1st jet (GeV);events/10 GeV", 100, 0, 1000);
  h_jetpt2 = fs->make<TH1F>("h_jetpt2", ";p_{T} of 2nd jet (GeV);events/10 GeV", 100, 0, 1000);
  h_jetpt3 = fs->make<TH1F>("h_jetpt3", ";p_{T} of 3rd jet (GeV);events/5 GeV", 100, 0, 500);
  h_jetpt4 = fs->make<TH1F>("h_jetpt4", ";p_{T} of 4th jet (GeV);events/5 GeV", 100, 0, 500);
  h_jetpt5 = fs->make<TH1F>("h_jetpt5", ";p_{T} of 5th jet (GeV);events/5 GeV", 100, 0, 500);
  h_jetpt6 = fs->make<TH1F>("h_jetpt6", ";p_{T} of 6th jet (GeV);events/5 GeV", 100, 0, 500);
  h_jet_ht = fs->make<TH1F>("h_jet_ht", ";H_{T} of jets (GeV);events/25 GeV", 200, 0, 5000);
  h_jet_ht_40 = fs->make<TH1F>("h_jet_ht_40", ";H_{T} of jets with p_{T} > 40 GeV;events/25 GeV", 200, 0, 5000);

  h_jet_pt = fs->make<TH1F>("h_jet_pt", ";jets p_{T} (GeV);jets/10 GeV", 100, 0, 1000);
  h_jet_eta = fs->make<TH1F>("h_jet_eta", ";jets #eta (rad);jets/.08", 100, -4, 4);
  h_jet_phi = fs->make<TH1F>("h_jet_phi", ";jets #phi (rad);jets/.063", 100, -3.1416, 3.1416);
  h_jet_energy = fs->make<TH1F>("h_jet_energy", ";jets energy (GeV);jets/10 GeV", 100, 0, 1000);
  h_jet_pairdphi = fs->make<TH1F>("h_jet_pairdphi", ";jet pair #Delta#phi (rad);jet pairs/.063", 100, -3.1416, 3.1416);
  h_jet_pairdr = fs->make<TH1F>("h_jet_pairdr", ";jet pair #DeltaR (rad);jet pairs/.047", 150, 0, 7);

  for (int i = 0; i < 11; ++i) {
    h_jet_Fox_Wolfram[i] = fs->make<TH1F>(TString::Format("h_jet_H%dT",i), TString::Format(";jets transverse Fox-Wolfram moment H_{%d}^{T};events",i), 101, 0, 1.01);
  }
  h_jet_ST = fs->make<TH1F>("h_jet_ST", ";jets transverse sphericity S_{T};events", 101, 0, 1.01);
  h_jetlep_ST = fs->make<TH1F>("h_jetlep_ST", ";jets + dilep muons transverse sphericity S_{T};events", 101, 0, 1.01);
  h_jet_ST_njets = fs->make<TH2F>("h_jet_ST_njets", ";number of jets;jets transverse sphericity S_{T}", 20, 0, 20, 101, 0, 1.01);
  h_jet_ST_ht = fs->make<TH2F>("h_jet_ST_ht", ";H_{T} of jets (GeV);jets transverse sphericity S_{T}", 200, 0, 5000, 101, 0, 1.01);
  h_jet_ST_ht40 = fs->make<TH2F>("h_jet_ST_ht40", ";H_{T} of jets with p_{T} > 40 GeV;jets transverse sphericity S_{T}", 200, 0, 5000, 101, 0, 1.01);

  h_met = fs->make<TH1F>("h_met", ";MET (GeV);events/5 GeV", 100, 0, 500);
  h_metphi = fs->make<TH1F>("h_metphi", ";MET #phi (rad);events/.063", 100, -3.1416, 3.1416);

  const char* lep_kind[2] = {"muon", "electron"};
  const char* lep_ex[3] = {"veto", "semilep", "dilep"};
  const char* bjets_pt[2] = {"20", "50"};
  for (int i = 0; i < 3; ++i) {
    h_nbtags[i] = fs->make<TH1F>(TString::Format("h_nbtags_%s", lmt_ex[i]), TString::Format(";# of %s b-tags;events", lmt_ex[i]), 20, 0, 20);
    h_nmuons[i] = fs->make<TH1F>(TString::Format("h_nmuons_%s", lep_ex[i]), TString::Format(";# of %s muons;events", lep_ex[i]), 5, 0, 5);
    h_nelectrons[i] = fs->make<TH1F>(TString::Format("h_nelectrons_%s", lep_ex[i]), TString::Format(";# of %s electrons;events", lep_ex[i]), 5, 0, 5);
    h_nleptons[i] = fs->make<TH1F>(TString::Format("h_nleptons_%s", lep_ex[i]), TString::Format(";# of %s leptons;events", lep_ex[i]), 5, 0, 5);

    h_bjet_pt[i] = fs->make<TH1F>(TString::Format("h_bjet_%s_pt", lmt_ex[i]), TString::Format(";%s bjets p_{T} (GeV);bjets/10 GeV", lmt_ex[i]), 100, 0, 1000);
    h_bjet_eta[i] = fs->make<TH1F>(TString::Format("h_bjet_%s_eta", lmt_ex[i]), TString::Format(";%s bjets #eta (rad);bjets/.08", lmt_ex[i]), 100, -4, 4);
    h_bjet_phi[i] = fs->make<TH1F>(TString::Format("h_bjet_%s_phi", lmt_ex[i]), TString::Format(";%s bjets #phi (rad);bjets/.063", lmt_ex[i]), 100, -3.1416, 3.1416);
    h_bjet_energy[i] = fs->make<TH1F>(TString::Format("h_bjet_%s_energy", lmt_ex[i]), TString::Format(";%s bjets energy (GeV);bjets/10 GeV", lmt_ex[i]), 100, 0, 1000);
    h_bjet_pairdphi[i] = fs->make<TH1F>(TString::Format("h_bjet_%s_pairdphi", lmt_ex[i]), TString::Format(";%s bjet pair #Delta#phi (rad);bjet pairs/.063", lmt_ex[i]), 100, -3.1416, 3.1416);
    h_bjet_pairdr[i] = fs->make<TH1F>(TString::Format("h_bjet_%s_pairdr", lmt_ex[i]), TString::Format(";%s bjet pair #DeltaR (rad);bjet pairs/.047", lmt_ex[i]), 150, 0, 7);

    for (int j = 0; j < 2; ++j) {
      h_bjets_absdphi[i][j] = fs->make<TH1F>(TString::Format("h_bjets_%s_ptgt%s_absdphi", lmt_ex[i], bjets_pt[j]), TString::Format("events with two %s GeV %s bjets;|#Delta#phi| (rad);events/0.126", bjets_pt[j], lmt_ex[i]), 25, 0, 3.15);
      h_bjets_dphi[i][j] = fs->make<TH1F>(TString::Format("h_bjets_%s_ptgt%s_dphi", lmt_ex[i], bjets_pt[j]), TString::Format("events with two %s GeV %s bjets;#Delta#phi (rad);events/0.126", bjets_pt[j], lmt_ex[i]), 50, -3.15, 3.15);
      h_bjets_deta[i][j] = fs->make<TH1F>(TString::Format("h_bjets_%s_ptgt%s_deta", lmt_ex[i], bjets_pt[j]), TString::Format("events with two %s GeV %s bjets;#Delta#eta (rad);events/0.16", bjets_pt[j], lmt_ex[i]), 50, -4, 4);
      h_bjets_deta_dphi[i][j] = fs->make<TH2F>(TString::Format("h_bjets_%s_ptgt%s_deta_dphi", lmt_ex[i], bjets_pt[j]), TString::Format("events with two %s GeV %s bjets;#Delta#phi (rad);#Delta#eta (rad)", bjets_pt[j], lmt_ex[i]), 50, -3.15, 3.15, 50, -4, 4);
      h_bjets_avgeta[i][j] = fs->make<TH1F>(TString::Format("h_bjets_%s_ptgt%s_avgeta", lmt_ex[i], bjets_pt[j]), TString::Format("events with two %s GeV %s bjets;avg #eta (rad);events/0.16", bjets_pt[j], lmt_ex[i]), 50, -4, 4);
      h_bjets_avgeta_dphi[i][j] = fs->make<TH2F>(TString::Format("h_bjets_%s_ptgt%s_avgeta_dphi", lmt_ex[i], bjets_pt[j]), TString::Format("events with two %s GeV %s bjets;#Delta#phi (rad); avg #eta (rad)", bjets_pt[j], lmt_ex[i]), 50, -3.15, 3.15, 50, -4, 4);
      h_bjets_dR[i][j] = fs->make<TH1F>(TString::Format("h_bjets_%s_ptgt%s_dR", lmt_ex[i], bjets_pt[j]), TString::Format("events with two %s GeV %s bjets;#Delta R (rad); events/0.14", bjets_pt[j], lmt_ex[i]), 50, 0, 7);
      h_bjets_dR_dphi[i][j] = fs->make<TH2F>(TString::Format("h_bjets_%s_ptgt%s_dR_dphi", lmt_ex[i], bjets_pt[j]), TString::Format("events with two %s GeV %s bjets;#Delta#phi (rad);#Delta R (rad)", bjets_pt[j], lmt_ex[i]), 50, -3.15, 3.15, 50, 0, 7);
    }

    for (int j = 0; j < 2; ++j) {
      h_leptons_pt   [j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_pt",    lep_kind[j], lep_ex[i]), TString::Format(";%s %s p_{T} (GeV);%ss/5 GeV",     lep_ex[i], lep_kind[j], lep_kind[j]), 40, 0, 200);
      h_leptons_eta  [j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_eta",   lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #eta (rad);%ss/.104",      lep_ex[i], lep_kind[j], lep_kind[j]), 50, -2.6, 2.6);
      h_leptons_phi  [j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_phi",   lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #phi (rad);%ss/.126",      lep_ex[i], lep_kind[j], lep_kind[j]), 50, -3.1416, 3.1416);
      h_leptons_dxy  [j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_dxy",   lep_kind[j], lep_ex[i]), TString::Format(";%s %ss dxy(PV) (cm);%ss/50 #mum", lep_ex[i], lep_kind[j], lep_kind[j]), 200, -0.5, 0.5);
      h_leptons_dxybs[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_dxybs", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss dxy(BS) (cm);%ss/50 #mum", lep_ex[i], lep_kind[j], lep_kind[j]), 200, -0.5, 0.5);
      h_leptons_dz   [j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_dz",   lep_kind[j], lep_ex[i]), TString::Format(";%s %ss dz (cm);%ss/50 #mum",       lep_ex[i], lep_kind[j], lep_kind[j]), 200, -0.5, 0.5);
      h_leptons_iso  [j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso",   lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%ss/.04",       lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
      h_leptons_iso_neargenel_hardint  [j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_neargenel_hardint",   lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%ss/.04",       lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
      h_leptons_iso_neargenmu_hardint  [j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_neargenmu_hardint",   lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%ss/.04",       lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
      h_leptons_iso_neargenb  [j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_neargenb",   lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%ss/.04",       lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
      h_leptons_iso_nearnothing  [j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_nearnothing",   lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%ss/.04",       lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);

    h_leptons_iso_0e0mu[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_0e0mu", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_1e0mu[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_1e0mu", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_0e1mu[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_0e1mu", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_1e1mu[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_1e1mu", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_2e0mu[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_2e0mu", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_0e2mu[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_0e2mu", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);

    h_leptons_iso_0e0mu_neargenel[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_0e0mu_neargenel", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_1e0mu_neargenel[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_1e0mu_neargenel", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_0e1mu_neargenel[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_0e1mu_neargenel", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_1e1mu_neargenel[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_1e1mu_neargenel", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_2e0mu_neargenel[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_2e0mu_neargenel", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_0e2mu_neargenel[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_0e2mu_neargenel", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);


    h_leptons_iso_0e0mu_neargenel_hardint[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_0e0mu_neargenel_hardint", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_1e0mu_neargenel_hardint[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_1e0mu_neargenel_hardint", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_0e1mu_neargenel_hardint[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_0e1mu_neargenel_hardint", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_1e1mu_neargenel_hardint[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_1e1mu_neargenel_hardint", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_2e0mu_neargenel_hardint[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_2e0mu_neargenel_hardint", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_0e2mu_neargenel_hardint[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_0e2mu_neargenel_hardint", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);

    h_leptons_iso_0e0mu_neargenmu[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_0e0mu_neargenmu", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_1e0mu_neargenmu[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_1e0mu_neargenmu", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_0e1mu_neargenmu[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_0e1mu_neargenmu", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_1e1mu_neargenmu[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_1e1mu_neargenmu", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_2e0mu_neargenmu[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_2e0mu_neargenmu", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_0e2mu_neargenmu[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_0e2mu_neargenmu", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);

    h_leptons_iso_0e0mu_neargenmu_hardint[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_0e0mu_neargenmu_hardint", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_1e0mu_neargenmu_hardint[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_1e0mu_neargenmu_hardint", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_0e1mu_neargenmu_hardint[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_0e1mu_neargenmu_hardint", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_1e1mu_neargenmu_hardint[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_1e1mu_neargenmu_hardint", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_2e0mu_neargenmu_hardint[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_2e0mu_neargenmu_hardint", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_0e2mu_neargenmu_hardint[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_0e2mu_neargenmu_hardint", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);

    h_leptons_iso_0e0mu_neargenb[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_0e0mu_neargenb", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_1e0mu_neargenb[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_1e0mu_neargenb", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_0e1mu_neargenb[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_0e1mu_neargenb", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_1e1mu_neargenb[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_1e1mu_neargenb", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_2e0mu_neargenb[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_2e0mu_neargenb", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_0e2mu_neargenb[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_0e2mu_neargenb", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);

    h_leptons_iso_0e0mu_nearnothing[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_0e0mu_nearnothing", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_1e0mu_nearnothing[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_1e0mu_nearnothing", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_0e1mu_nearnothing[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_0e1mu_nearnothing", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_1e1mu_nearnothing[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_1e1mu_nearnothing", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_2e0mu_nearnothing[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_2e0mu_nearnothing", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    h_leptons_iso_0e2mu_nearnothing[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso_0e2mu_nearnothing", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%s/.04", lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
    }

    h_muons_absdphi[i] = fs->make<TH1F>(TString::Format("h_muons_%s_absdphi", lep_ex[i]), TString::Format("events with two %s muons;|#Delta#phi| (rad);events/0.126", lep_ex[i]), 25, 0, 3.15);
    h_muons_dphi[i] = fs->make<TH1F>(TString::Format("h_muons_%s_dphi", lep_ex[i]), TString::Format("events with two %s muons;#Delta#phi (rad);events/0.126", lep_ex[i]), 50, -3.15, 3.15);
    h_muons_deta[i] = fs->make<TH1F>(TString::Format("h_muons_%s_deta", lep_ex[i]), TString::Format("events with two %s muons;#Delta#eta (rad);events/0.16", lep_ex[i]), 50, -4, 4);
    h_muons_deta_dphi[i] = fs->make<TH2F>(TString::Format("h_muons_%s_deta_dphi", lep_ex[i]), TString::Format("events with two %s muons;#Delta#phi (rad);#Delta#eta (rad)", lep_ex[i]), 50, -3.15, 3.15, 50, -4, 4);
    h_muons_avgeta[i] = fs->make<TH1F>(TString::Format("h_muons_%s_avgeta", lep_ex[i]), TString::Format("events with two %s muons;avg #eta (rad);events/0.16", lep_ex[i]), 50, -4, 4);
    h_muons_avgeta_dphi[i] = fs->make<TH2F>(TString::Format("h_muons_%s_avgeta_dphi", lep_ex[i]), TString::Format("events with two %s muons;#Delta#phi (rad);avg #eta (rad)", lep_ex[i]), 50, -3.15, 3.15, 50, -4, 4);
    h_muons_dR[i] = fs->make<TH1F>(TString::Format("h_muons_%s_dR", lep_ex[i]), TString::Format("events with two %s muons;#Delta R (rad);events/0.14", lep_ex[i]), 50, 0, 7);
    h_muons_dR_dphi[i] = fs->make<TH2F>(TString::Format("h_muons_%s_dR_dphi", lep_ex[i]), TString::Format("events with two %s muons;#Delta#phi (rad);#Delta R (rad)", lep_ex[i]), 50, -3.15, 3.15, 50, 0, 7);
  }

  h_jet_svnvertices = fs->make<TH1F>("h_jet_svnvertices", ";number of secondary vertices;number of jets", 10, 0, 10);
  h_jet_svntracks = fs->make<TH1F>("h_jet_svntracks", ";# of tracks/SV;number of jets", 40, 0, 40);
  h_jet_svsumpt2 = fs->make<TH1F>("h_jet_svsumpt2", ";SV #Sigma p_{T}^{2} (GeV^2);number of jets", 300, 0, 6000);
  h_jet_svx = fs->make<TH1F>("h_jet_svx", ";SV x (cm);number of jets", 100, -8, 8);
  h_jet_svy = fs->make<TH1F>("h_jet_svy", ";SV y (cm);number of jets", 100, -8, 8);
  h_jet_svz = fs->make<TH1F>("h_jet_svz", ";SV z (cm);number of jets", 100, -25, 25);
  h_jet_svyx = fs->make<TH2F>("h_jet_svyx", ";SV x (cm);SV y (cm)", 100, -8, 8, 100, -8, 8);
  h_jet_svzr = fs->make<TH2F>("h_jet_svzr", ";SV rho (cm);SV z (cm)", 100, -8, 8, 100, -25, 25);
  h_jet_momphi_posphi = fs->make<TH2F>("h_jet_momphi_posphi", ";SV position phi;jet momentum phi", 50, -3.15, 3.15, 50, -3.15, 3.15);
  h_jet_svcxx = fs->make<TH1F>("h_jet_svcxx", ";SV cxx;number of jets", 100, -0.01, 0.01);
  h_jet_svcxy = fs->make<TH1F>("h_jet_svcxy", ";SV cxy;number of jets", 100, -0.01, 0.01);
  h_jet_svcxz = fs->make<TH1F>("h_jet_svcxz", ";SV cxz;number of jets", 100, -0.01, 0.01);
  h_jet_svcyy = fs->make<TH1F>("h_jet_svcyy", ";SV cyy;number of jets", 100, -0.01, 0.01);
  h_jet_svcyz = fs->make<TH1F>("h_jet_svcyz", ";SV cyz;number of jets", 100, -0.01, 0.01);
  h_jet_svczz = fs->make<TH1F>("h_jet_svczz", ";SV czz;number of jets", 100, -0.01, 0.01);
  h_jet_svpv2ddist = fs->make<TH1F>("h_jet_svpv2ddist", ";dist2d(SV, PV) (cm);number of jets", 100, 0, 5);
  h_jet_svpv2derr = fs->make<TH1F>("h_jet_svpv2derr", ";#sigma(dist2d(SV, PV)) (cm);number of jets", 100, 0, 0.05);
  h_jet_svpv2dsig = fs->make<TH1F>("h_jet_svpv2dsig", ";N#sigma(dist2d(SV, PV));number of jets", 100, 0, 100);

  h_jetsv_absdphi = fs->make<TH1F>("h_jetsv_dphi", "events with two jet vertices;|#Delta#phi| (rad);events/0.126", 25, 0, 3.15);
  h_jetsv_dxy = fs->make<TH1F>("h_jetsv_dxy", "events with two jet vertices;dist2d(sv #0, #1) (cm);arb. units", 500, 0, 5);
  h_jetsv_dxyerr = fs->make<TH1F>("h_jetsv_dxyerr", "events with two jet vertices;#sigma(dist2d(sv #0, #1)) (cm);arb. units", 500, 0, 0.5);
  h_jetsv_dxysig = fs->make<TH1F>("h_jetsv_dxysig", "events with two jet vertices;N#sigma(dist2d(sv #0, #1));arb. units", 100, 0, 100);
  h_jetsv_dz = fs->make<TH1F>("h_jetsv_dz", "events with two jet vertices;|dz(sv #0, #1)| (cm);arb. units", 500, 0, 5);
  h_jetsv_dzerr = fs->make<TH1F>("h_jetsv_dzerr", "events with two jet vertices;#sigma(dz(sv #0, #1)) (cm);arb. units", 500, 0, 0.5);
  h_jetsv_dzsig = fs->make<TH1F>("h_jetsv_dzsig", "events with two jet vertices;N#sigma(dz(sv #0, #1));arb. units", 100, 0, 100);
  h_jetsv_d3d = fs->make<TH1F>("h_jetsv_d3d", "events with two jet vertices;dist3d(sv #0, #1) (cm);arb. units", 500, 0, 5);
  h_jetsv_d3derr = fs->make<TH1F>("h_jetsv_d3derr", "events with two jet vertices;#sigma(dist3d(sv #0, #1)) (cm);arb. units", 500, 0, 0.5);
  h_jetsv_d3dsig = fs->make<TH1F>("h_jetsv_d3dsig", "events with two jet vertices;N#sigma(dist3d(sv #0, #1));arb. units", 100, 0, 100);

  h_bjetsv_absdphi = fs->make<TH1F>("h_bjetsv_dphi", "events with two bjet vertices;|#Delta#phi| (rad);events/0.126", 25, 0, 3.15);
  h_bjetsv_dxy = fs->make<TH1F>("h_bjetsv_dxy", "events with two bjet vertices;dist2d(sv #0, #1) (cm);arb. units", 500, 0, 5);
  h_bjetsv_dxyerr = fs->make<TH1F>("h_bjetsv_dxyerr", "events with two bjet vertices;#sigma(dist2d(sv #0, #1)) (cm);arb. units", 500, 0, 0.5);
  h_bjetsv_dxysig = fs->make<TH1F>("h_bjetsv_dxysig", "events with two bjet vertices;N#sigma(dist2d(sv #0, #1));arb. units", 100, 0, 100);
  h_bjetsv_dz = fs->make<TH1F>("h_bjetsv_dz", "events with two bjet vertices;|dz(sv #0, #1)| (cm);arb. units", 500, 0, 5);
  h_bjetsv_dzerr = fs->make<TH1F>("h_bjetsv_dzerr", "events with two bjet vertices;#sigma(dz(sv #0, #1)) (cm);arb. units", 500, 0, 0.5);
  h_bjetsv_dzsig = fs->make<TH1F>("h_bjetsv_dzsig", "events with two bjet vertices;N#sigma(dz(sv #0, #1));arb. units", 100, 0, 100);
  h_bjetsv_d3d = fs->make<TH1F>("h_bjetsv_d3d", "events with two bjet vertices;dist3d(sv #0, #1) (cm);arb. units", 500, 0, 5);
  h_bjetsv_d3derr = fs->make<TH1F>("h_bjetsv_d3derr", "events with two bjet vertices;#sigma(dist3d(sv #0, #1)) (cm);arb. units", 500, 0, 0.5);
  h_bjetsv_d3dsig = fs->make<TH1F>("h_bjetsv_d3dsig", "events with two bjet vertices;N#sigma(dist3d(sv #0, #1));arb. units", 100, 0, 100);

  if (primary_vertex_src.label() != "") {
    h_pv_n = fs->make<TH1F>("h_pv_n", ";# of primary vertices;events", 65, 0, 65);
    const char* pv_names[4] = {"pv1_sumpt2", "rest_sumpt2", "pv1_absdz", "rest_absdz"};
    for (int i = 0; i < 4; ++i) {
      h_pv_x[i] = fs->make<TH1F>(TString::Format("h_%s_x", pv_names[i]), TString::Format(";%s x (cm);events/10 #mum", pv_names[i]), 200, -0.1, 0.1);
      h_pv_y[i] = fs->make<TH1F>(TString::Format("h_%s_y", pv_names[i]), TString::Format(";%s y (cm);events/10 #mum", pv_names[i]), 200, -0.1, 0.1);
      h_pv_z[i] = fs->make<TH1F>(TString::Format("h_%s_z", pv_names[i]), TString::Format(";%s z (cm);events/1.5 mm", pv_names[i]), 200, -15, 15);
      h_pv_rho[i] = fs->make<TH1F>(TString::Format("h_%s_rho", pv_names[i]), TString::Format(";%s rho (cm);events/5 #mum", pv_names[i]), 200, 0, 0.1);
      h_pv_phi[i] = fs->make<TH1F>(TString::Format("h_%s_phi", pv_names[i]), TString::Format(";%s #phi (rad);events/.063", pv_names[i]), 100, -3.1416, 3.1416);
      h_pv_ntracks[i] = fs->make<TH1F>(TString::Format("h_%s_ntracks", pv_names[i]), TString::Format(";%s # of tracks in primary vertex;events", pv_names[i]), 200, 0, 200);
      h_pv_sumpt2[i] = fs->make<TH1F>(TString::Format("h_%s_sumpt2", pv_names[i]), TString::Format(";%s #Sigma p_{T}^{2} (GeV^{2});events/10 GeV^{2}", pv_names[i]), 200, 0, 2000);
    }
  }

  if (jets_src.label() != "") {
    h_jets_n = fs->make<TH1F>("h_jets_n", ";# of jets;events", 20, 0, 20);
    h_jets_pt = fs->make<TH1F>("h_jets_pt", ";jet pt;number of jets", 100, 0, 500);
    h_jets_eta = fs->make<TH1F>("h_jets_eta", ";jet eta;number of jets", 50, -4, 4);
    h_jets_phi = fs->make<TH1F>("h_jets_phi", ";jet phi;number of jets", 50, -3.15, 3.15);

    const char* b_wpnames[NBDISC] = {"JP", "CSV"};
    for (int i = 0; i < NBDISC; ++i) {
      for (int j = 0; j < 3; ++j) {
        h_bjets_n[i][j] = fs->make<TH1F>(TString::Format("h_bjets_%s%s_n", b_wpnames[i], lmt_ex[j]), TString::Format(";# of %s %s bjets;events", b_wpnames[i], lmt_ex[j]), 20, 0, 20);
        h_bjets_pt[i][j] = fs->make<TH1F>(TString::Format("h_bjets_%s%s_pt", b_wpnames[i], lmt_ex[j]), TString::Format(";%s %s bjet pt;number of bjets", b_wpnames[i], lmt_ex[j]), 100, 0, 500);
        h_bjets_eta[i][j] = fs->make<TH1F>(TString::Format("h_bjets_%s%s_eta", b_wpnames[i], lmt_ex[j]), TString::Format(";%s %s bjet eta;number of bjets", b_wpnames[i], lmt_ex[j]), 50, -4, 4);
        h_bjets_phi[i][j] = fs->make<TH1F>(TString::Format("h_bjets_%s%s_phi", b_wpnames[i], lmt_ex[j]), TString::Format(";%s %s bjet phi;number of bjets", b_wpnames[i], lmt_ex[j]), 50, -3.15, 3.15);
      }
    }
  }

  h_n_vertex_seed_tracks = fs->make<TH1F>("h_n_vertex_seed_tracks", ";# vertex seed tracks;events", 100, 0, 100);
  h_vertex_seed_track_chi2dof = fs->make<TH1F>("h_vertex_seed_track_chi2dof", ";vertex seed track #chi^{2}/dof;tracks/1", 10, 0, 10);
  h_vertex_seed_track_q = fs->make<TH1F>("h_vertex_seed_track_q", ";vertex seed track charge;tracks", 3, -1, 2);
  h_vertex_seed_track_pt = fs->make<TH1F>("h_vertex_seed_track_pt", ";vertex seed track p_{T} (GeV);tracks/GeV", 300, 0, 300);
  h_vertex_seed_track_eta = fs->make<TH1F>("h_vertex_seed_track_eta", ";vertex seed track #eta;tracks/0.052", 100, -2.6, 2.6);
  h_vertex_seed_track_phi = fs->make<TH1F>("h_vertex_seed_track_phi", ";vertex seed track #phi;tracks/0.063", 100, -3.15, 3.15);
  h_vertex_seed_track_dxy = fs->make<TH1F>("h_vertex_seed_track_dxy", ";vertex seed track dxy (cm);tracks/10 #mum", 200, -0.1, 0.1);
  h_vertex_seed_track_dz = fs->make<TH1F>("h_vertex_seed_track_dz", ";vertex seed track dz (cm);tracks/10 #mum", 200, -0.1, 0.1);
  h_vertex_seed_track_npxhits = fs->make<TH1F>("h_vertex_seed_track_npxhits", ";vertex seed track # pixel hits;tracks", 10, 0, 10);
  h_vertex_seed_track_nsthits = fs->make<TH1F>("h_vertex_seed_track_nsthits", ";vertex seed track # strip hits;tracks", 50, 0, 50);
  h_vertex_seed_track_nhits = fs->make<TH1F>("h_vertex_seed_track_nhits", ";vertex seed track # hits;tracks", 60, 0, 60);
  h_vertex_seed_track_npxlayers = fs->make<TH1F>("h_vertex_seed_track_npxlayers", ";vertex seed track # pixel layers;tracks", 10, 0, 10);
  h_vertex_seed_track_nstlayers = fs->make<TH1F>("h_vertex_seed_track_nstlayers", ";vertex seed track # strip layers;tracks", 20, 0, 20);
  h_vertex_seed_track_nlayers = fs->make<TH1F>("h_vertex_seed_track_nlayers", ";vertex seed track # layers;tracks", 30, 0, 30);
}

void MFVEventHistos::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<MFVEvent> mevent;
  event.getByToken(mevent_token, mevent);

  edm::Handle<double> weight;
  event.getByToken(weight_token, weight);
  const double w = *weight;
  h_w->Fill(w);

  const double bsx = force_bs.size() ? force_bs[0] : mevent->bsx;
  const double bsy = force_bs.size() ? force_bs[1] : mevent->bsy;
  const double bsz = force_bs.size() ? force_bs[2] : mevent->bsz;

  //////////////////////////////////////////////////////////////////////////////

  h_gen_decay->Fill(mevent->gen_decay_type[0], mevent->gen_decay_type[1], w);
  h_gen_partons_in_acc->Fill(mevent->gen_partons_in_acc, w);
  h_gen_flavor_code->Fill(mevent->gen_flavor_code, w);

  h_nbquarks->Fill(mevent->gen_bquark_pt.size());
  for (size_t ibquark = 0; ibquark < mevent->gen_bquark_pt.size(); ++ibquark) {
    h_bquark_pt->Fill(mevent->gen_bquark_pt[ibquark]);
    h_bquark_eta->Fill(mevent->gen_bquark_eta[ibquark]);
    h_bquark_phi->Fill(mevent->gen_bquark_phi[ibquark]);
    h_bquark_energy->Fill(mevent->gen_bquark_energy[ibquark]);
    for (size_t jbquark = ibquark+1; jbquark < mevent->gen_bquark_pt.size(); ++jbquark) {
      h_bquark_pairdphi->Fill(reco::deltaPhi(mevent->gen_bquark_phi[ibquark], mevent->gen_bquark_phi[jbquark]));
      h_bquark_pairdr->Fill(reco::deltaR(mevent->gen_bquark_eta[ibquark], mevent->gen_bquark_phi[ibquark], mevent->gen_bquark_eta[jbquark], mevent->gen_bquark_phi[jbquark]));
    }
  }
  if (mevent->gen_bquark_pt.size() == 2) {
    double dphi = reco::deltaPhi(mevent->gen_bquark_phi[0], mevent->gen_bquark_phi[1]);
    double deta = mevent->gen_bquark_eta[0] - mevent->gen_bquark_eta[1];
    double avgeta = (mevent->gen_bquark_eta[0] + mevent->gen_bquark_eta[1]) / 2;
    double dR = reco::deltaR(mevent->gen_bquark_eta[0], mevent->gen_bquark_phi[0], mevent->gen_bquark_eta[1], mevent->gen_bquark_phi[1]);
    h_bquarks_absdphi->Fill(fabs(dphi));
    h_bquarks_dphi->Fill(dphi);
    h_bquarks_deta->Fill(deta);
    h_bquarks_deta_dphi->Fill(dphi, deta);
    h_bquarks_avgeta->Fill(avgeta);
    h_bquarks_avgeta_dphi->Fill(dphi, avgeta);
    h_bquarks_dR->Fill(dR);
    h_bquarks_dR_dphi->Fill(dphi, dR);
  }

  h_minlspdist2d->Fill(mevent->minlspdist2d(), w);
  h_lspdist2d->Fill(mevent->lspdist2d(), w);
  h_lspdist3d->Fill(mevent->lspdist3d(), w);

  //////////////////////////////////////////////////////////////////////////////

  h_hlt_bits->Fill(0., w);
  h_l1_bits->Fill(0., w);
  for (int i = 0; i < mfv::n_hlt_paths; ++i) {
    if (mevent->found_hlt(i)) h_hlt_bits->Fill(1+2*i,   w);
    if (mevent->pass_hlt (i)) h_hlt_bits->Fill(1+2*i+1, w);
  }
  for (int i = 0; i < mfv::n_l1_paths; ++i) {
    if (mevent->found_l1(i)) h_l1_bits->Fill(1+2*i,   w);
    if (mevent->pass_l1 (i)) h_l1_bits->Fill(1+2*i+1, w);
  }

  {
    const bool pass_800  = mevent->pass_hlt(1);
    const bool pass_900  = mevent->pass_hlt(2);
    const bool pass_450  = mevent->pass_hlt(3);
    const bool pass_8450 = mevent->pass_hlt(4);
    h_hlt_cross->Fill(0., w);
    if (pass_800  && !pass_900) h_hlt_cross->Fill(1., w);
    if (pass_450  && !pass_800) h_hlt_cross->Fill(2., w);
    if (pass_450  && !pass_900) h_hlt_cross->Fill(3., w);
    if (pass_8450 && !pass_800) h_hlt_cross->Fill(4., w);
    if (pass_8450 && !pass_900) h_hlt_cross->Fill(5., w);
  }

  //////////////////////////////////////////////////////////////////////////////

  h_npu->Fill(mevent->npu, w);

  h_bsx->Fill(bsx, w);
  h_bsy->Fill(bsy, w);
  h_bsz->Fill(bsz, w);
  h_bsphi->Fill(atan2(bsy, bsx), w);

  h_npv->Fill(mevent->npv, w);
  h_pvx->Fill(mevent->pvx - bsx, w);
  h_pvy->Fill(mevent->pvy - bsy, w);
  h_pvz->Fill(mevent->pvz - bsz, w);
  h_pvcxx->Fill(mevent->pvcxx, w);
  h_pvcxy->Fill(mevent->pvcxy, w);
  h_pvcxz->Fill(mevent->pvcxz, w);
  h_pvcyy->Fill(mevent->pvcyy, w);
  h_pvcyz->Fill(mevent->pvcyz, w);
  h_pvczz->Fill(mevent->pvczz, w);
  h_pvphi->Fill(atan2(mevent->pvy - bsy, mevent->pvx - bsx), w);
  h_pvntracks->Fill(mevent->pv_ntracks, w);
  h_pvsumpt2->Fill(mevent->pv_sumpt2, w);
  h_pvrho->Fill(mevent->pv_rho(), w);

  h_njets->Fill(mevent->njets(), w);
  for (int i = 0; i < 3; ++i)
    h_njetsnopu[i]->Fill(mevent->njetsnopu(i), w);
  h_jetpt1->Fill(mevent->njets() >= 1 ? mevent->jet_pt[0] : 0.f, w);
  h_jetpt2->Fill(mevent->njets() >= 2 ? mevent->jet_pt[1] : 0.f, w);
  h_jetpt3->Fill(mevent->njets() >= 3 ? mevent->jet_pt[2] : 0.f, w);
  h_jetpt4->Fill(mevent->jetpt4(), w);
  h_jetpt5->Fill(mevent->jetpt5(), w);
  h_jetpt6->Fill(mevent->jetpt6(), w);
  h_jet_ht->Fill(mevent->jet_ht(), w);
  h_jet_ht_40->Fill(mevent->jet_ht(40), w);

  for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
    h_jet_pt->Fill(mevent->jet_pt[ijet]);
    h_jet_eta->Fill(mevent->jet_eta[ijet]);
    h_jet_phi->Fill(mevent->jet_phi[ijet]);
    h_jet_energy->Fill(mevent->jet_energy[ijet]);
    for (size_t jjet = ijet+1; jjet < mevent->jet_id.size(); ++jjet) {
      h_jet_pairdphi->Fill(reco::deltaPhi(mevent->jet_phi[ijet], mevent->jet_phi[jjet]));
      h_jet_pairdr->Fill(reco::deltaR(mevent->jet_eta[ijet], mevent->jet_phi[ijet], mevent->jet_eta[jjet], mevent->jet_phi[jjet]));
    }
  }

  uchar lep0 = mevent->gen_decay_type[0];
  uchar lep1 = mevent->gen_decay_type[1];
  for (size_t ilep = 0; ilep < mevent->lep_id.size(); ++ilep) {
    const size_t j = mevent->is_electron(ilep);
    for (size_t i = 0; i < 3; ++i)
      if (mevent->pass_lep_sel_bit(ilep, 1<<i)) {
        h_leptons_pt[j][i]->Fill(mevent->lep_pt[ilep]);
        h_leptons_eta[j][i]->Fill(mevent->lep_eta[ilep]);
        h_leptons_phi[j][i]->Fill(mevent->lep_phi[ilep]);
        h_leptons_dxy[j][i]->Fill(mevent->lep_dxy[ilep]);
        h_leptons_dxybs[j][i]->Fill(mevent->lep_dxybs[ilep]);
        h_leptons_dz[j][i]->Fill(mevent->lep_dz[ilep]);
        h_leptons_iso[j][i]->Fill(mevent->lep_iso[ilep]);

	bool near_b = false;
	bool near_el = false;
	bool near_mu = false;
	bool hard_int = false;
	for (size_t ibquark = 0; ibquark < mevent->gen_bquark_pt.size(); ++ibquark) {
	  double dR = reco::deltaR(mevent->gen_bquark_eta[ibquark], mevent->gen_bquark_phi[ibquark], mevent->lep_eta[ilep], mevent->lep_phi[ilep]);
	  if (dR < 0.5) {
	    near_b = true;
	    break;
	  }
	}
	for (size_t igenlep = 0; igenlep < mevent->gen_lepton_id.size(); ++igenlep) {
	  double dR = reco::deltaR(mevent->gen_lepton_eta[igenlep], mevent->gen_lepton_phi[igenlep], mevent->lep_eta[ilep], mevent->lep_phi[ilep]);
	  if (dR < 0.1) {
	    if (mevent->gen_lepton_id[igenlep] & 0x80) 
	      hard_int = true;
            if (mevent->gen_lepton_id[igenlep] & 1)
              near_el = true;
            else 
              near_mu = true;
	    break;
	  }
	}

	if (near_el && hard_int) h_leptons_iso_neargenel_hardint[j][i]->Fill(mevent->lep_iso[ilep]);
	if (near_mu && hard_int) h_leptons_iso_neargenmu_hardint[j][i]->Fill(mevent->lep_iso[ilep]);
	if (near_b) h_leptons_iso_neargenb[j][i]->Fill(mevent->lep_iso[ilep]);
	if (!near_el && !near_mu && !near_b) h_leptons_iso_nearnothing[j][i]->Fill(mevent->lep_iso[ilep]);

	if (lep0 == 0) {
	  if (lep1 == 0) {
	    h_leptons_iso_2e0mu[j][i]->Fill(mevent->lep_iso[ilep]);
	    if (near_b) h_leptons_iso_2e0mu_neargenb[j][i]->Fill(mevent->lep_iso[ilep]);
	    if (near_el) {
	      h_leptons_iso_2e0mu_neargenel[j][i]->Fill(mevent->lep_iso[ilep]);
	      if (hard_int) 
		h_leptons_iso_2e0mu_neargenel_hardint[j][i]->Fill(mevent->lep_iso[ilep]);
	    }
	    if (near_mu) {
	      h_leptons_iso_2e0mu_neargenmu[j][i]->Fill(mevent->lep_iso[ilep]);
	      if (hard_int) 
		h_leptons_iso_2e0mu_neargenmu_hardint[j][i]->Fill(mevent->lep_iso[ilep]);
	    }
	    if (!near_el && !near_mu && !near_b)
	      h_leptons_iso_2e0mu_nearnothing[j][i]->Fill(mevent->lep_iso[ilep]);
	  }
	  else if (lep1 == 1) {
	    h_leptons_iso_1e1mu[j][i]->Fill(mevent->lep_iso[ilep]);
	    if (near_b) h_leptons_iso_1e1mu_neargenb[j][i]->Fill(mevent->lep_iso[ilep]);
	    if (near_el) {
	      h_leptons_iso_1e1mu_neargenel[j][i]->Fill(mevent->lep_iso[ilep]);
	      if (hard_int) 
		h_leptons_iso_1e1mu_neargenel_hardint[j][i]->Fill(mevent->lep_iso[ilep]);
	    }
	    if (near_mu) {
	      h_leptons_iso_1e1mu_neargenmu[j][i]->Fill(mevent->lep_iso[ilep]);
	      if (hard_int) 
		h_leptons_iso_1e1mu_neargenmu_hardint[j][i]->Fill(mevent->lep_iso[ilep]);
	    }
	    if (!near_el && !near_mu && !near_b)
	      h_leptons_iso_1e1mu_nearnothing[j][i]->Fill(mevent->lep_iso[ilep]);
	  }
	  else {
	    h_leptons_iso_1e0mu[j][i]->Fill(mevent->lep_iso[ilep]);
	    if (near_b) h_leptons_iso_1e0mu_neargenb[j][i]->Fill(mevent->lep_iso[ilep]);
	    if (near_el) {
	      h_leptons_iso_1e0mu_neargenel[j][i]->Fill(mevent->lep_iso[ilep]);
	      if (hard_int) 
		h_leptons_iso_1e0mu_neargenel_hardint[j][i]->Fill(mevent->lep_iso[ilep]);
	    }
	    if (near_mu) {
	      h_leptons_iso_1e0mu_neargenmu[j][i]->Fill(mevent->lep_iso[ilep]);
	      if (hard_int) 
		h_leptons_iso_1e0mu_neargenmu_hardint[j][i]->Fill(mevent->lep_iso[ilep]);
	    }
	    if (!near_el && !near_mu && !near_b)
	      h_leptons_iso_1e0mu_nearnothing[j][i]->Fill(mevent->lep_iso[ilep]);
	  }
	}
	else if (lep0 == 1) {
	  if (lep1 == 0) {
	    h_leptons_iso_1e1mu[j][i]->Fill(mevent->lep_iso[ilep]);
	    if (near_b) h_leptons_iso_1e1mu_neargenb[j][i]->Fill(mevent->lep_iso[ilep]);
	    if (near_el) {
	      h_leptons_iso_1e1mu_neargenel[j][i]->Fill(mevent->lep_iso[ilep]);
	      if (hard_int) 
		h_leptons_iso_1e1mu_neargenel_hardint[j][i]->Fill(mevent->lep_iso[ilep]);
	    }
	    if (near_mu) {
	      h_leptons_iso_1e1mu_neargenmu[j][i]->Fill(mevent->lep_iso[ilep]);
	      if (hard_int) 
		h_leptons_iso_1e1mu_neargenmu_hardint[j][i]->Fill(mevent->lep_iso[ilep]);
	    }
	    if (!near_el && !near_mu && !near_b)
	      h_leptons_iso_1e1mu_nearnothing[j][i]->Fill(mevent->lep_iso[ilep]);
	  }
	  else if (lep1 == 1) {
	    h_leptons_iso_0e2mu[j][i]->Fill(mevent->lep_iso[ilep]);
	    if (near_b) h_leptons_iso_0e2mu_neargenb[j][i]->Fill(mevent->lep_iso[ilep]);
	    if (near_el) {
	      h_leptons_iso_0e2mu_neargenel[j][i]->Fill(mevent->lep_iso[ilep]);
	      if (hard_int) 
		h_leptons_iso_0e2mu_neargenel_hardint[j][i]->Fill(mevent->lep_iso[ilep]);
	    }
	    if (near_mu) {
	      h_leptons_iso_0e2mu_neargenmu[j][i]->Fill(mevent->lep_iso[ilep]);
	      if (hard_int) 
		h_leptons_iso_0e2mu_neargenmu_hardint[j][i]->Fill(mevent->lep_iso[ilep]);
	    }
	    if (!near_el && !near_mu && !near_b)
	      h_leptons_iso_0e2mu_nearnothing[j][i]->Fill(mevent->lep_iso[ilep]);
	  }
	  else {
	    h_leptons_iso_0e1mu[j][i]->Fill(mevent->lep_iso[ilep]);
	    if (near_b) h_leptons_iso_0e1mu_neargenb[j][i]->Fill(mevent->lep_iso[ilep]);
	    if (near_el) {
	      h_leptons_iso_0e1mu_neargenel[j][i]->Fill(mevent->lep_iso[ilep]);
	      if (hard_int) 
		h_leptons_iso_0e1mu_neargenel_hardint[j][i]->Fill(mevent->lep_iso[ilep]);
	    }
	    if (near_mu) {
	      h_leptons_iso_0e1mu_neargenmu[j][i]->Fill(mevent->lep_iso[ilep]);
	      if (hard_int) 
		h_leptons_iso_0e1mu_neargenmu_hardint[j][i]->Fill(mevent->lep_iso[ilep]);
	    }
	    if (!near_el && !near_mu && !near_b)
	      h_leptons_iso_0e1mu_nearnothing[j][i]->Fill(mevent->lep_iso[ilep]);
	  }
	}
	else {
	  if (lep1 == 0) {
	    h_leptons_iso_1e0mu[j][i]->Fill(mevent->lep_iso[ilep]);
	    if (near_b) h_leptons_iso_1e0mu_neargenb[j][i]->Fill(mevent->lep_iso[ilep]);
	    if (near_el) {
	      h_leptons_iso_1e0mu_neargenel[j][i]->Fill(mevent->lep_iso[ilep]);
	      if (hard_int) 
		h_leptons_iso_1e0mu_neargenel_hardint[j][i]->Fill(mevent->lep_iso[ilep]);
	    }
	    if (near_mu) {
	      h_leptons_iso_1e0mu_neargenmu[j][i]->Fill(mevent->lep_iso[ilep]);
	      if (hard_int) 
		h_leptons_iso_1e0mu_neargenmu_hardint[j][i]->Fill(mevent->lep_iso[ilep]);
	    }
	    if (!near_el && !near_mu && !near_b)
	      h_leptons_iso_1e0mu_nearnothing[j][i]->Fill(mevent->lep_iso[ilep]);
	  }
	  else if (lep1 == 1) {
	    h_leptons_iso_0e1mu[j][i]->Fill(mevent->lep_iso[ilep]);
	    if (near_b) h_leptons_iso_0e1mu_neargenb[j][i]->Fill(mevent->lep_iso[ilep]);
	    if (near_el) {
	      h_leptons_iso_0e1mu_neargenel[j][i]->Fill(mevent->lep_iso[ilep]);
	      if (hard_int) 
		h_leptons_iso_0e1mu_neargenel_hardint[j][i]->Fill(mevent->lep_iso[ilep]);
	    }
	    if (near_mu) {
	      h_leptons_iso_0e1mu_neargenmu[j][i]->Fill(mevent->lep_iso[ilep]);
	      if (hard_int) 
		h_leptons_iso_0e1mu_neargenmu_hardint[j][i]->Fill(mevent->lep_iso[ilep]);
	    }
	    if (!near_el && !near_mu && !near_b)
	      h_leptons_iso_0e1mu_nearnothing[j][i]->Fill(mevent->lep_iso[ilep]);
	  } 
	  else {
	    h_leptons_iso_0e0mu[j][i]->Fill(mevent->lep_iso[ilep]);
	    if (near_b) h_leptons_iso_0e0mu_neargenb[j][i]->Fill(mevent->lep_iso[ilep]);
	    if (near_el) {
	      h_leptons_iso_0e0mu_neargenel[j][i]->Fill(mevent->lep_iso[ilep]);
	      if (hard_int) 
		h_leptons_iso_0e0mu_neargenel_hardint[j][i]->Fill(mevent->lep_iso[ilep]);
	    }
	    if (near_mu) {
	      h_leptons_iso_0e0mu_neargenmu[j][i]->Fill(mevent->lep_iso[ilep]);
	      if (hard_int) 
		h_leptons_iso_0e0mu_neargenmu_hardint[j][i]->Fill(mevent->lep_iso[ilep]);
	    }
	    if (!near_el && !near_mu && !near_b)
	      h_leptons_iso_0e0mu_nearnothing[j][i]->Fill(mevent->lep_iso[ilep]);
	  }
	}
      }
  }
  double Fox_Wolfram[11] = {0};
  for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
    double theta_i = 2 * atan(exp(-mevent->jet_eta[ijet]));
    for (size_t jjet = 0; jjet < mevent->jet_id.size(); ++jjet) {
      double theta_j = 2 * atan(exp(-mevent->jet_eta[jjet]));
      double WT_ij = mevent->jet_pt[ijet] * mevent->jet_pt[jjet] / (mevent->jet_ht() * mevent->jet_ht());
      double x = cos(theta_i) * cos(theta_j) + sin(theta_i) * sin(theta_j) * cos(mevent->jet_phi[ijet] - mevent->jet_phi[jjet]);
      Fox_Wolfram[0] += WT_ij * 1;
      Fox_Wolfram[1] += WT_ij * x;
      Fox_Wolfram[2] += WT_ij * 1./2. * (3*pow(x,2) - 1);
      Fox_Wolfram[3] += WT_ij * 1./2. * (5*pow(x,3) - 3*x);
      Fox_Wolfram[4] += WT_ij * 1./8. * (35*pow(x,4) - 30*pow(x,2) + 3);
      Fox_Wolfram[5] += WT_ij * 1./8. * (63*pow(x,5) - 70*pow(x,3) + 15*x);
      Fox_Wolfram[6] += WT_ij * 1./16. * (231*pow(x,6) - 315*pow(x,4) + 105*pow(x,2) - 5);
      Fox_Wolfram[7] += WT_ij * 1./16. * (429*pow(x,7) - 693*pow(x,5) + 315*pow(x,3) - 35*x);
      Fox_Wolfram[8] += WT_ij * 1./128. * (6435*pow(x,8) - 12012*pow(x,6) + 6930*pow(x,4) - 1260*pow(x,2) + 35);
      Fox_Wolfram[9] += WT_ij * 1./128. * (12155*pow(x,9) - 25740*pow(x,7) + 18018*pow(x,5) - 4620*pow(x,3) + 315*x);
      Fox_Wolfram[10] += WT_ij * 1./256. * (46189*pow(x,10) - 109395*pow(x,8) + 90090*pow(x,6) - 30030*pow(x,4) + 3465*pow(x,2) - 63);
    }
  }
  for (int i = 0; i < 11; ++i) {
    h_jet_Fox_Wolfram[i]->Fill(Fox_Wolfram[i]);
  }
  h_jet_ST->Fill(mevent->jet_ST());
  h_jetlep_ST->Fill(mevent->jetlep_ST(0, MFVEvent::mu_dilep));
  h_jet_ST_njets->Fill(mevent->njets(), mevent->jet_ST());
  h_jet_ST_ht->Fill(mevent->jet_ht(), mevent->jet_ST());
  h_jet_ST_ht40->Fill(mevent->jet_ht(40), mevent->jet_ST());

  h_met->Fill(mevent->met());
  h_metphi->Fill(mevent->metphi());

  std::vector<double> bjets_eta[3][2];
  std::vector<double> bjets_phi[3][2];
  for (int i = 0; i < 3; ++i) {
    h_nbtags[i]->Fill(mevent->nbtags(i), w);
    h_nmuons[i]->Fill(mevent->nmu(i), w);
    h_nelectrons[i]->Fill(mevent->nel(i), w);
    h_nleptons[i]->Fill(mevent->nlep(i), w);

    for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
      if (((mevent->jet_id[ijet] >> 2) & 3) >= i + 1) {
        h_bjet_pt[i]->Fill(mevent->jet_pt[ijet]);
        h_bjet_eta[i]->Fill(mevent->jet_eta[ijet]);
        h_bjet_phi[i]->Fill(mevent->jet_phi[ijet]);
        h_bjet_energy[i]->Fill(mevent->jet_energy[ijet]);
        for (size_t jjet = ijet+1; jjet < mevent->jet_id.size(); ++jjet) {
          if (((mevent->jet_id[jjet] >> 2) & 3) >= i + 1) {
            h_bjet_pairdphi[i]->Fill(reco::deltaPhi(mevent->jet_phi[ijet], mevent->jet_phi[jjet]));
            h_bjet_pairdr[i]->Fill(reco::deltaR(mevent->jet_eta[ijet], mevent->jet_phi[ijet], mevent->jet_eta[jjet], mevent->jet_phi[jjet]));
          }
        }

        for (int j = 0; j < 2; ++j) {
          if (j==1 && mevent->jet_pt[ijet] < 50) continue;
          bjets_eta[i][j].push_back(mevent->jet_eta[ijet]);
          bjets_phi[i][j].push_back(mevent->jet_phi[ijet]);
        }
      }
    }

    for (int j = 0; j < 2; ++j) {
      if (bjets_phi[i][j].size() == 2) {
        double dphi = reco::deltaPhi(bjets_phi[i][j][0], bjets_phi[i][j][1]);
        double deta = bjets_eta[i][j][0] - bjets_eta[i][j][1];
        double avgeta = (bjets_eta[i][j][0] + bjets_eta[i][j][1]) / 2;
        double dR = reco::deltaR(bjets_eta[i][j][0], bjets_phi[i][j][0], bjets_eta[i][j][1], bjets_phi[i][j][1]);
        h_bjets_absdphi[i][j]->Fill(fabs(dphi));
        h_bjets_dphi[i][j]->Fill(dphi);
        h_bjets_deta[i][j]->Fill(deta);
        h_bjets_deta_dphi[i][j]->Fill(dphi, deta);
        h_bjets_avgeta[i][j]->Fill(avgeta);
        h_bjets_avgeta_dphi[i][j]->Fill(dphi, avgeta);
        h_bjets_dR[i][j]->Fill(dR);
        h_bjets_dR_dphi[i][j]->Fill(dphi, dR);
      }
    }
  }

  std::vector<double> jetsv_x;
  std::vector<double> jetsv_y;
  std::vector<double> jetsv_z;
  std::vector<double> jetsv_cxx;
  std::vector<double> jetsv_cxy;
  std::vector<double> jetsv_cxz;
  std::vector<double> jetsv_cyy;
  std::vector<double> jetsv_cyz;
  std::vector<double> jetsv_czz;
  for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
    h_jet_svnvertices->Fill(mevent->jet_svnvertices[ijet]);
    if (mevent->jet_svnvertices[ijet] > 0) {
      jetsv_x.push_back(mevent->jet_svx[ijet] - mevent->bsx);
      jetsv_y.push_back(mevent->jet_svy[ijet] - mevent->bsy);
      jetsv_z.push_back(mevent->jet_svz[ijet] - mevent->bsz);
      jetsv_cxx.push_back(mevent->jet_svcxx[ijet]);
      jetsv_cxy.push_back(mevent->jet_svcxy[ijet]);
      jetsv_cxz.push_back(mevent->jet_svcxz[ijet]);
      jetsv_cyy.push_back(mevent->jet_svcyy[ijet]);
      jetsv_cyz.push_back(mevent->jet_svcyz[ijet]);
      jetsv_czz.push_back(mevent->jet_svczz[ijet]);

      h_jet_svntracks->Fill(mevent->jet_svntracks[ijet]);
      h_jet_svsumpt2->Fill(mevent->jet_svsumpt2[ijet]);
      h_jet_svx->Fill(mevent->jet_svx[ijet] - mevent->bsx);
      h_jet_svy->Fill(mevent->jet_svy[ijet] - mevent->bsy);
      h_jet_svz->Fill(mevent->jet_svz[ijet] - mevent->bsz);
      h_jet_svyx->Fill(mevent->jet_svx[ijet] - mevent->bsx, mevent->jet_svy[ijet] - mevent->bsy);
      float svr = sqrt((mevent->jet_svx[ijet] - mevent->bsx) * (mevent->jet_svx[ijet] - mevent->bsx) + (mevent->jet_svy[ijet] - mevent->bsy) * (mevent->jet_svy[ijet] - mevent->bsy));
      h_jet_svzr->Fill(svr * (mevent->jet_svy[ijet] - mevent->bsy >= 0 ? 1 : -1), mevent->jet_svz[ijet] - mevent->bsz);
      h_jet_momphi_posphi->Fill(atan2(mevent->jet_svy[ijet] - mevent->bsy, mevent->jet_svx[ijet] - mevent->bsx), mevent->jet_phi[ijet]);
      h_jet_svcxx->Fill(mevent->jet_svcxx[ijet]);
      h_jet_svcxy->Fill(mevent->jet_svcxy[ijet]);
      h_jet_svcxz->Fill(mevent->jet_svcxz[ijet]);
      h_jet_svcyy->Fill(mevent->jet_svcyy[ijet]);
      h_jet_svcyz->Fill(mevent->jet_svcyz[ijet]);
      h_jet_svczz->Fill(mevent->jet_svczz[ijet]);
      h_jet_svpv2ddist->Fill(mevent->jet_svpv2ddist(ijet));
      h_jet_svpv2derr->Fill(mevent->jet_svpv2derr(ijet));
      h_jet_svpv2dsig->Fill(mevent->jet_svpv2dsig(ijet));
    }
  }
  if (jetsv_x.size() == 2) {
    double dphi = reco::deltaPhi(atan2(jetsv_y[0], jetsv_x[0]), atan2(jetsv_y[1], jetsv_x[1]));
    h_jetsv_absdphi->Fill(fabs(dphi));

    double dxy = sqrt((jetsv_x[0] - jetsv_x[1]) * (jetsv_x[0] - jetsv_x[1]) + (jetsv_y[0] - jetsv_y[1]) * (jetsv_y[0] - jetsv_y[1]));
    double dx = (jetsv_x[0] - jetsv_x[1]) / dxy;
    double dy = (jetsv_y[0] - jetsv_y[1]) / dxy;
    double dxyerr = sqrt((jetsv_cxx[0] + jetsv_cxx[1])*dx*dx + (jetsv_cyy[0] + jetsv_cyy[1])*dy*dy + 2*(jetsv_cxy[0] + jetsv_cxy[1])*dx*dy);
    h_jetsv_dxy->Fill(dxy);
    h_jetsv_dxyerr->Fill(dxyerr);
    h_jetsv_dxysig->Fill(dxy / dxyerr);

    double dz = fabs(jetsv_z[0] - jetsv_z[1]);
    double dzerr = sqrt(jetsv_czz[0] + jetsv_czz[1]);
    h_jetsv_dz->Fill(dz);
    h_jetsv_dzerr->Fill(dzerr);
    h_jetsv_dzsig->Fill(dz / dzerr);

    double dr = sqrt((jetsv_x[0] - jetsv_x[1]) * (jetsv_x[0] - jetsv_x[1]) + (jetsv_y[0] - jetsv_y[1]) * (jetsv_y[0] - jetsv_y[1]) + (jetsv_z[0] - jetsv_z[1]) * (jetsv_z[0] - jetsv_z[1]));
    double dxr = (jetsv_x[0] - jetsv_x[1]) / dr;
    double dyr = (jetsv_y[0] - jetsv_y[1]) / dr;
    double dzr = (jetsv_z[0] - jetsv_z[1]) / dr;
    double drerr = sqrt((jetsv_cxx[0] + jetsv_cxx[1])*dxr*dxr + (jetsv_cyy[0] + jetsv_cyy[1])*dyr*dyr + 2*(jetsv_cxy[0] + jetsv_cxy[1])*dxr*dyr
                    + 2*(jetsv_cxz[0] + jetsv_cxz[1])*dxr*dzr + 2*(jetsv_cyz[0] + jetsv_cyz[1])*dyr*dzr + (jetsv_czz[0] + jetsv_czz[1])*dzr*dzr);
    h_jetsv_d3d->Fill(dr);
    h_jetsv_d3derr->Fill(drerr);
    h_jetsv_d3dsig->Fill(dr / drerr);
  }

  jetsv_x.clear();
  jetsv_y.clear();
  jetsv_z.clear();
  jetsv_cxx.clear();
  jetsv_cxy.clear();
  jetsv_cxz.clear();
  jetsv_cyy.clear();
  jetsv_cyz.clear();
  jetsv_czz.clear();
  for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
    if (((mevent->jet_id[ijet] >> 2) & 3) >= 2 && mevent->jet_svnvertices[ijet] > 0) {
      jetsv_x.push_back(mevent->jet_svx[ijet] - mevent->bsx);
      jetsv_y.push_back(mevent->jet_svy[ijet] - mevent->bsy);
      jetsv_z.push_back(mevent->jet_svz[ijet] - mevent->bsz);
      jetsv_cxx.push_back(mevent->jet_svcxx[ijet]);
      jetsv_cxy.push_back(mevent->jet_svcxy[ijet]);
      jetsv_cxz.push_back(mevent->jet_svcxz[ijet]);
      jetsv_cyy.push_back(mevent->jet_svcyy[ijet]);
      jetsv_cyz.push_back(mevent->jet_svcyz[ijet]);
      jetsv_czz.push_back(mevent->jet_svczz[ijet]);
    }
  }

  if (jetsv_x.size() == 2) {
    double dphi = reco::deltaPhi(atan2(jetsv_y[0], jetsv_x[0]), atan2(jetsv_y[1], jetsv_x[1]));
    h_bjetsv_absdphi->Fill(fabs(dphi));

    double dxy = sqrt((jetsv_x[0] - jetsv_x[1]) * (jetsv_x[0] - jetsv_x[1]) + (jetsv_y[0] - jetsv_y[1]) * (jetsv_y[0] - jetsv_y[1]));
    double dx = (jetsv_x[0] - jetsv_x[1]) / dxy;
    double dy = (jetsv_y[0] - jetsv_y[1]) / dxy;
    double dxyerr = sqrt((jetsv_cxx[0] + jetsv_cxx[1])*dx*dx + (jetsv_cyy[0] + jetsv_cyy[1])*dy*dy + 2*(jetsv_cxy[0] + jetsv_cxy[1])*dx*dy);
    h_bjetsv_dxy->Fill(dxy);
    h_bjetsv_dxyerr->Fill(dxyerr);
    h_bjetsv_dxysig->Fill(dxy / dxyerr);

    double dz = fabs(jetsv_z[0] - jetsv_z[1]);
    double dzerr = sqrt(jetsv_czz[0] + jetsv_czz[1]);
    h_bjetsv_dz->Fill(dz);
    h_bjetsv_dzerr->Fill(dzerr);
    h_bjetsv_dzsig->Fill(dz / dzerr);

    double dr = sqrt((jetsv_x[0] - jetsv_x[1]) * (jetsv_x[0] - jetsv_x[1]) + (jetsv_y[0] - jetsv_y[1]) * (jetsv_y[0] - jetsv_y[1]) + (jetsv_z[0] - jetsv_z[1]) * (jetsv_z[0] - jetsv_z[1]));
    double dxr = (jetsv_x[0] - jetsv_x[1]) / dr;
    double dyr = (jetsv_y[0] - jetsv_y[1]) / dr;
    double dzr = (jetsv_z[0] - jetsv_z[1]) / dr;
    double drerr = sqrt((jetsv_cxx[0] + jetsv_cxx[1])*dxr*dxr + (jetsv_cyy[0] + jetsv_cyy[1])*dyr*dyr + 2*(jetsv_cxy[0] + jetsv_cxy[1])*dxr*dyr
                    + 2*(jetsv_cxz[0] + jetsv_cxz[1])*dxr*dzr + 2*(jetsv_cyz[0] + jetsv_cyz[1])*dyr*dzr + (jetsv_czz[0] + jetsv_czz[1])*dzr*dzr);
    h_bjetsv_d3d->Fill(dr);
    h_bjetsv_d3derr->Fill(drerr);
    h_bjetsv_d3dsig->Fill(dr / drerr);
  }

  //////////////////////////////////////////////////////////////////////////////

  edm::Handle<reco::VertexCollection> primary_vertices;
  if (primary_vertex_src.label() != "") {
    event.getByLabel(primary_vertex_src, primary_vertices);

    const int npv = int(primary_vertices->size());
    h_pv_n->Fill(npv, w);

    const reco::Vertex& pv0 = primary_vertices->at(0);
    double absdz = 100000;
    int ipvdz = 0;
    for (int ipv = 1; ipv < npv; ++ipv) {
      const reco::Vertex& pv = primary_vertices->at(ipv);
      if (fabs(pv.z() - pv0.z()) < absdz) {
        absdz = fabs(pv.z() - pv0.z());
        ipvdz = ipv;
      }
    }

    for (int ipv = 1; ipv < npv; ++ipv) {
      const reco::Vertex& pv = primary_vertices->at(ipv);
      double sumpt2 = 0;
      for (auto trki = pv.tracks_begin(), trke = pv.tracks_end(); trki != trke; ++trki) {
        double trkpt = (*trki)->pt();
        sumpt2 += trkpt * trkpt;
      }

      const int isumpt2 = ipv == 1 ? 0 : 1;
      h_pv_x[isumpt2]->Fill(pv.x() - bsx, w);
      h_pv_y[isumpt2]->Fill(pv.y() - bsy, w);
      h_pv_z[isumpt2]->Fill(pv.z() - bsz, w);
      h_pv_rho[isumpt2]->Fill(sqrt((pv.x() - bsx) * (pv.x() - bsx) + (pv.y() - bsy) * (pv.y() - bsy)), w);
      h_pv_phi[isumpt2]->Fill(atan2(pv.y() - bsy, pv.x() - bsx), w);
      h_pv_ntracks[isumpt2]->Fill(pv.nTracks(), w);
      h_pv_sumpt2[isumpt2]->Fill(sumpt2, w);

      const int iabsdz = ipv == ipvdz ? 2 : 3;
      h_pv_x[iabsdz]->Fill(pv.x() - bsx, w);
      h_pv_y[iabsdz]->Fill(pv.y() - bsy, w);
      h_pv_z[iabsdz]->Fill(pv.z() - bsz, w);
      h_pv_rho[iabsdz]->Fill(sqrt((pv.x() - bsx) * (pv.x() - bsx) + (pv.y() - bsy) * (pv.y() - bsy)), w);
      h_pv_phi[iabsdz]->Fill(atan2(pv.y() - bsy, pv.x() - bsx), w);
      h_pv_ntracks[iabsdz]->Fill(pv.nTracks(), w);
      h_pv_sumpt2[iabsdz]->Fill(sumpt2, w);
    }
  }

  //////////////////////////////////////////////////////////////////////////////

  edm::Handle<pat::JetCollection> jets;
  if (jets_src.label() != "") {
    event.getByLabel(jets_src, jets);

    const int njets = int(jets->size());
    h_jets_n->Fill(njets, w);

    const char* b_discriminators[NBDISC] = {"jetProbabilityBJetTags", "combinedSecondaryVertexBJetTags"};
    const double b_discriminator_mins[NBDISC][3] = {{0.275, 0.545, 0.790}, {0.244, 0.679, 0.898}};
    int nbjets[NBDISC][3] = {{0, 0, 0}, {0, 0, 0}};
    for (int i = 0; i < njets; ++i) {
      const pat::Jet& jet = jets->at(i);
      h_jets_pt->Fill(jet.pt(), w);
      h_jets_eta->Fill(jet.eta(), w);
      h_jets_phi->Fill(jet.phi(), w);
      for (int j = 0; j < NBDISC; ++j) {
        for (int k = 0; k < 3; ++k) {
          if (jet.bDiscriminator(b_discriminators[j]) > b_discriminator_mins[j][k]) {
            nbjets[j][k] += 1;
            h_bjets_pt[j][k]->Fill(jet.pt(), w);
            h_bjets_eta[j][k]->Fill(jet.eta(), w);
            h_bjets_phi[j][k]->Fill(jet.phi(), w);
          }
        }
      }
    }
    for (int j = 0; j < NBDISC; ++j) {
      for (int k = 0; k < 3; ++k) {
        h_bjets_n[j][k]->Fill(nbjets[j][k], w);
      }
    }
  }

  //////////////////////////////////////////////////////////////////////////////

  const size_t n_vertex_seed_tracks = mevent->n_vertex_seed_tracks();
  h_n_vertex_seed_tracks->Fill(n_vertex_seed_tracks);
  for (size_t i = 0; i < n_vertex_seed_tracks; ++i) {
    h_vertex_seed_track_chi2dof->Fill(mevent->vertex_seed_track_chi2dof[i], w);
    h_vertex_seed_track_q->Fill(mevent->vertex_seed_track_q(i), w);
    h_vertex_seed_track_pt->Fill(mevent->vertex_seed_track_pt(i), w);
    h_vertex_seed_track_eta->Fill(mevent->vertex_seed_track_eta[i], w);
    h_vertex_seed_track_phi->Fill(mevent->vertex_seed_track_phi[i], w);
    h_vertex_seed_track_dxy->Fill(mevent->vertex_seed_track_dxy[i], w);
    h_vertex_seed_track_dz->Fill(mevent->vertex_seed_track_dz[i], w);
    h_vertex_seed_track_npxhits->Fill(mevent->vertex_seed_track_npxhits(i), w);
    h_vertex_seed_track_nsthits->Fill(mevent->vertex_seed_track_nsthits(i), w);
    h_vertex_seed_track_nhits->Fill(mevent->vertex_seed_track_nhits(i), w);
    h_vertex_seed_track_npxlayers->Fill(mevent->vertex_seed_track_npxlayers(i), w);
    h_vertex_seed_track_nstlayers->Fill(mevent->vertex_seed_track_nstlayers(i), w);
    h_vertex_seed_track_nlayers->Fill(mevent->vertex_seed_track_nlayers(i), w);
  }
}

DEFINE_FWK_MODULE(MFVEventHistos);
