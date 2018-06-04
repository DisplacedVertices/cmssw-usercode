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

  TH1F* h_w;

  TH2F* h_gen_decay;
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

  TH1F* h_met;
  TH1F* h_metphi;

  TH1F* h_nbtags[3];

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

  TH1F* h_nmuons[2];
  TH1F* h_nelectrons[2];
  TH1F* h_nleptons[2];

  TH1F* h_leptons_pt[2][2];
  TH1F* h_leptons_eta[2][2];
  TH1F* h_leptons_phi[2][2];
  TH1F* h_leptons_dxy[2][2];
  TH1F* h_leptons_dxybs[2][2];
  TH1F* h_leptons_dz[2][2];
  TH1F* h_leptons_iso[2][2];

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
    force_bs(cfg.getParameter<std::vector<double> >("force_bs"))
{
  if (force_bs.size() && force_bs.size() != 3)
    throw cms::Exception("Misconfiguration", "force_bs must be empty or size 3");

  edm::Service<TFileService> fs;

  h_w = fs->make<TH1F>("h_w", ";event weight;events/0.1", 100, 0, 10);

  h_gen_decay = fs->make<TH2F>("h_gen_decay", "0-2=e,mu,tau, 3=h;decay code #0;decay code #1", 4, 0, 4, 4, 0, 4);
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

  h_met = fs->make<TH1F>("h_met", ";MET (GeV);events/5 GeV", 100, 0, 500);
  h_metphi = fs->make<TH1F>("h_metphi", ";MET #phi (rad);events/.063", 100, -3.1416, 3.1416);

  const char* lep_kind[2] = {"muon", "electron"};
  const char* bjets_pt[2] = {"20", "50"};
  for (int i = 0; i < 3; ++i) {
    h_nbtags[i] = fs->make<TH1F>(TString::Format("h_nbtags_%s", lmt_ex[i]), TString::Format(";# of %s b-tags;events", lmt_ex[i]), 20, 0, 20);
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
  }

  const char* lep_ex[2] = {"any", "selected"};
  for (int i = 0; i < 2; ++i) {
    h_nmuons[i] = fs->make<TH1F>(TString::Format("h_nmuons_%s", lep_ex[i]), TString::Format(";# of %s muons;events", lep_ex[i]), 5, 0, 5);
    h_nelectrons[i] = fs->make<TH1F>(TString::Format("h_nelectrons_%s", lep_ex[i]), TString::Format(";# of %s electrons;events", lep_ex[i]), 5, 0, 5);
    h_nleptons[i] = fs->make<TH1F>(TString::Format("h_nleptons_%s", lep_ex[i]), TString::Format(";# of %s leptons;events", lep_ex[i]), 5, 0, 5);
    for (int j = 0; j < 2; ++j) {
      h_leptons_pt   [j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_pt",    lep_kind[j], lep_ex[i]), TString::Format(";%s %s p_{T} (GeV);%ss/5 GeV",     lep_ex[i], lep_kind[j], lep_kind[j]), 40, 0, 200);
      h_leptons_eta  [j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_eta",   lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #eta (rad);%ss/.104",      lep_ex[i], lep_kind[j], lep_kind[j]), 50, -2.6, 2.6);
      h_leptons_phi  [j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_phi",   lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #phi (rad);%ss/.126",      lep_ex[i], lep_kind[j], lep_kind[j]), 50, -3.1416, 3.1416);
      h_leptons_dxy  [j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_dxy",   lep_kind[j], lep_ex[i]), TString::Format(";%s %ss dxy(PV) (cm);%ss/50 #mum", lep_ex[i], lep_kind[j], lep_kind[j]), 200, -0.5, 0.5);
      h_leptons_dxybs[j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_dxybs", lep_kind[j], lep_ex[i]), TString::Format(";%s %ss dxy(BS) (cm);%ss/50 #mum", lep_ex[i], lep_kind[j], lep_kind[j]), 200, -0.5, 0.5);
      h_leptons_dz   [j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_dz",   lep_kind[j], lep_ex[i]), TString::Format(";%s %ss dz (cm);%ss/50 #mum",       lep_ex[i], lep_kind[j], lep_kind[j]), 200, -0.5, 0.5);
      h_leptons_iso  [j][i] = fs->make<TH1F>(TString::Format("h_%s_%s_iso",   lep_kind[j], lep_ex[i]), TString::Format(";%s %ss #iso (rad);%ss/.04",       lep_ex[i], lep_kind[j], lep_kind[j]), 50, 0, 2);
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
  h_gen_flavor_code->Fill(mevent->gen_flavor_code, w);

  const size_t nbquarks = mevent->gen_bquarks.size();
  h_nbquarks->Fill(nbquarks);
  for (size_t i = 0; i < nbquarks; ++i) {
    h_bquark_pt->Fill(mevent->gen_bquarks[i].Pt());
    h_bquark_eta->Fill(mevent->gen_bquarks[i].Eta());
    h_bquark_phi->Fill(mevent->gen_bquarks[i].Phi());
    h_bquark_energy->Fill(mevent->gen_bquarks[i].E());
    for (size_t j = i+1; j < nbquarks; ++j) {
      const double dphi = reco::deltaPhi(mevent->gen_bquarks[i].Phi(), mevent->gen_bquarks[j].Phi());
      const double deta = mevent->gen_bquarks[i].Eta() - mevent->gen_bquarks[j].Eta(); // JMTBAD why not fabs
      const double avgeta = (mevent->gen_bquarks[i].Eta() + mevent->gen_bquarks[j].Eta()) / 2;
      const double dR = reco::deltaR(mevent->gen_bquarks[i].Eta(), mevent->gen_bquarks[i].Phi(), mevent->gen_bquarks[j].Eta(), mevent->gen_bquarks[j].Phi());
      h_bquark_pairdphi->Fill(dphi);
      h_bquark_pairdr->Fill(dR);
      if (nbquarks == 2) {
        h_bquarks_absdphi->Fill(fabs(dphi));
        h_bquarks_dphi->Fill(dphi);
        h_bquarks_deta->Fill(deta);
        h_bquarks_deta_dphi->Fill(dphi, deta);
        h_bquarks_avgeta->Fill(avgeta);
        h_bquarks_avgeta_dphi->Fill(dphi, avgeta);
        h_bquarks_dR->Fill(dR);
        h_bquarks_dR_dphi->Fill(dphi, dR);
      }
    }
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

  for (int i = 0; i < 2; ++i) {
    h_nmuons[i]->Fill(mevent->nmu(i), w);
    h_nelectrons[i]->Fill(mevent->nel(i), w);
    h_nleptons[i]->Fill(mevent->nlep(i), w);
  }

  for (size_t ilep = 0; ilep < mevent->lep_id.size(); ++ilep) {
    const size_t j = mevent->is_electron(ilep);
    for (size_t i = 0; i < 2; ++i)
      if (i == 0 || mevent->pass_lep_sel(ilep)) {
        h_leptons_pt[j][i]->Fill(mevent->lep_pt[ilep]);
        h_leptons_eta[j][i]->Fill(mevent->lep_eta[ilep]);
        h_leptons_phi[j][i]->Fill(mevent->lep_phi[ilep]);
        h_leptons_dxy[j][i]->Fill(mevent->lep_dxy[ilep]);
        h_leptons_dxybs[j][i]->Fill(mevent->lep_dxybs[ilep]);
        h_leptons_dz[j][i]->Fill(mevent->lep_dz[ilep]);
        h_leptons_iso[j][i]->Fill(mevent->lep_iso[ilep]);
      }
  }

  h_met->Fill(mevent->met());
  h_metphi->Fill(mevent->metphi());

  std::vector<double> bjets_eta[3][2];
  std::vector<double> bjets_phi[3][2];
  for (int i = 0; i < 3; ++i) {
    h_nbtags[i]->Fill(mevent->nbtags(i), w);

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
