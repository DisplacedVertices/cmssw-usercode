#include "TH2F.h"
#include "TRandom3.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/ExtValue.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralino/interface/EventTools.h"

class MFVEventHistos : public edm::EDAnalyzer {
 public:
  explicit MFVEventHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::EDGetTokenT<MFVEvent> mevent_token;
  const edm::EDGetTokenT<double> weight_token;

  TH1F* h_w;

  TH2F* h_gen_decay;
  TH1F* h_gen_flavor_code;

  TH1F* h_nbquarks;
  TH1F* h_bquark_pt;
  TH1F* h_bquark_eta;
  TH1F* h_bquark_phi;
  TH1F* h_bquark_energy;
  TH1F* h_bquark_pairdphi;
  TH1F* h_bquark_pairdeta;

  TH1F* h_minlspdist2d;
  TH1F* h_lspdist2d;
  TH1F* h_lspdist3d;
  TH1F* h_gen_bs2ddist;
  TH2F* h_gen_bsxdist_bsydist;

  TH1F* h_hlt_bits;
  TH1F* h_l1_bits;
  TH1F* h_filter_bits;

  TH1F* h_npu;

  TH1F* h_bsx;
  TH1F* h_bsy;
  TH1F* h_bsz;
  TH1F* h_bsphi;

  TH1F* h_npv;
  TH1F* h_pvx;
  TH1F* h_pvy;
  TH1F* h_pvxwide;
  TH1F* h_pvywide;
  TH1F* h_pvz;
  TH1F* h_pvcxx;
  TH1F* h_pvcxy;
  TH1F* h_pvcxz;
  TH1F* h_pvcyy;
  TH1F* h_pvcyz;
  TH1F* h_pvczz;
  TH1F* h_pvrho;
  TH1F* h_pvrhowide;
  TH1F* h_pvphi;
  TH1F* h_pvntracks;
  TH1F* h_pvscore;
  TH1F* h_pvsx;
  TH1F* h_pvsy;
  TH1F* h_pvsxwide;
  TH1F* h_pvsywide;
  TH1F* h_pvsz;
  TH1F* h_pvsrho;
  TH1F* h_pvsrhowide;
  TH1F* h_pvsphi;
  TH1F* h_pvsscore;
  TH1F* h_pvsdz;
  TH1F* h_pvsmindz;
  TH1F* h_pvsmaxdz;
  TH1F* h_pvsmindz_minscore;
  TH1F* h_pvsmaxdz_minscore;

  TH1F* h_njets;
  TH1F* h_njets20;
  static const int MAX_NJETS = 10;
  TH1F* h_jet_pt[MAX_NJETS+1];
  TH1F* h_jet_eta[MAX_NJETS+1];
  TH1F* h_jet_phi[MAX_NJETS+1];

  TH1F* h_bsort_jet_pt[MAX_NJETS+1];
  TH1F* h_bsort_jet_eta[MAX_NJETS+1];
  TH1F* h_bsort_jet_phi[MAX_NJETS+1];
  TH1F* h_bsort_jet_csv[MAX_NJETS+1];

  TH1F* h_jet_energy;
  TH1F* h_jet_ht;
  TH1F* h_jet_ht_40;
  TH1F* h_calo_jet_pt[MAX_NJETS+1];
  TH1F* h_calo_jet_eta[MAX_NJETS+1];
  TH1F* h_calo_jet_phi[MAX_NJETS+1];
  TH1F* h_calo_jet_ht;
  TH1F* h_calo_jet_ht40;

  TH1F* h_online_calo_jet_ht;
  TH1F* h_online_pf_jet_ht;
  TH2F* h_online_offline_calo_jet_ht;
  TH2F* h_online_offline_pf_jet_ht;

  TH1F* h_online_calojet_pt;
  TH1F* h_online_pfjet_pt;
  TH1F* h_offline_calojet_pt;
  TH1F* h_offline_pfjet_pt;
  TH2F* h_online_offline_calojet_pt;
  TH2F* h_online_offline_pfjet_pt[MAX_NJETS+1];

  TH2F* h_ncalojet_online_offline;
  TH2F* h_ncalojet_idp_online_offline;
  TH2F* h_calojet_ndiff_htdiff;
  TH2F* h_idp_calojet_ndiff_htdiff;

  TH1F* h_jet_pairdphi;
  TH1F* h_jet_pairdeta;
  TH1F* h_jet_pairdr;

  TH1F* h_met;
  TH1F* h_metphi;

  TH1F* h_nbtags[3];
  TH2F* h_nbtags_v_bquark_code[3];
  TH1F* h_jet_bdisc;
  TH2F* h_jet_bdisc_v_bquark_code;
  TH1F* h_bjet_pt;
  TH1F* h_bjet_eta;
  TH1F* h_bjet_phi;
  TH1F* h_bjet_energy;
  TH1F* h_bjet_pairdphi;
  TH1F* h_bjet_pairdeta;

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
  TH2F* h_vertex_seed_track_phi_v_eta;
  TH1F* h_vertex_seed_track_dxy;
  TH1F* h_vertex_seed_track_dz;
  TH1F* h_vertex_seed_track_err_pt;
  TH1F* h_vertex_seed_track_err_eta;
  TH1F* h_vertex_seed_track_err_phi;
  TH1F* h_vertex_seed_track_err_dxy;
  TH1F* h_vertex_seed_track_err_dz;
  TH1F* h_vertex_seed_track_npxhits;
  TH1F* h_vertex_seed_track_nsthits;
  TH1F* h_vertex_seed_track_nhits;
  TH1F* h_vertex_seed_track_npxlayers;
  TH1F* h_vertex_seed_track_nstlayers;
  TH1F* h_vertex_seed_track_nlayers;
};

MFVEventHistos::MFVEventHistos(const edm::ParameterSet& cfg)
  : mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src")))
{
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
  h_bquark_pairdeta = fs->make<TH1F>("h_bquark_pairdeta", ";bquark pair #Delta#eta (rad);bquark pairs/.1", 100, -5.0, 5.0);

  h_minlspdist2d = fs->make<TH1F>("h_minlspdist2d", ";min dist2d(gen vtx #i) (cm);events/0.1 mm", 200, 0, 2);
  h_lspdist2d = fs->make<TH1F>("h_lspdist2d", ";dist2d(gen vtx #0, #1) (cm);events/0.1 mm", 200, 0, 2);
  h_lspdist3d = fs->make<TH1F>("h_lspdist3d", ";dist3d(gen vtx #0, #1) (cm);events/0.1 mm", 200, 0, 2);
  h_gen_bs2ddist = fs->make<TH1F>("h_gen_bs2ddist", ";dist2d(gen vtx, beamspot) (cm);arb. units", 500, 0, 2.5);
  h_gen_bsxdist_bsydist = fs->make<TH2F>("h_gen_bsxdist_bsydist", "; x-dist(gen vtx, beamspot) (cm); y-dist(gen vtx, beamspot)", 500, -0.5, 0.5, 500, -0.5, 0.5);

  h_hlt_bits = fs->make<TH1F>("h_hlt_bits", ";;events", 2*mfv::n_hlt_paths+1, 0, 2*mfv::n_hlt_paths+1);
  h_l1_bits  = fs->make<TH1F>("h_l1_bits",  ";;events", 2*mfv::n_l1_paths +1, 0, 2*mfv::n_l1_paths +1);
  h_filter_bits  = fs->make<TH1F>("h_filter_bits",  ";;events", 2*mfv::n_filter_paths +1, 0, 2*mfv::n_filter_paths +1);

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

  h_filter_bits->GetXaxis()->SetBinLabel(1, "nevents");
  for (int i = 0; i < mfv::n_filter_paths; ++i) {
    h_filter_bits->GetXaxis()->SetBinLabel(i+2, TString::Format(" pass %s", mfv::filter_paths[i]));
  }

  h_npu = fs->make<TH1F>("h_npu", ";true nPU;events", 120, 0, 120);

  h_bsx = fs->make<TH1F>("h_bsx", ";beamspot x (cm);events/10 #mum", 200, -0.1, 0.1);
  h_bsy = fs->make<TH1F>("h_bsy", ";beamspot y (cm);events/10 #mum", 200, -0.1, 0.1);
  h_bsz = fs->make<TH1F>("h_bsz", ";beamspot z (cm);events/400 #mum", 200, -4, 4);
  h_bsphi = fs->make<TH1F>("h_bsphi", ";beamspot #phi (rad);events/.063", 100, -3.1416, 3.1416);

  h_npv = fs->make<TH1F>("h_npv", ";# of primary vertices;events", 120, 0, 120);
  h_pvx = fs->make<TH1F>("h_pvx", ";primary vertex x (cm);events/2 #mum", 200, -0.02, 0.02);
  h_pvy = fs->make<TH1F>("h_pvy", ";primary vertex y (cm);events/2 #mum", 200, -0.02, 0.02);
  h_pvxwide = fs->make<TH1F>("h_pvxwide", ";primary vertex x (cm);events/40 #mum", 50, -0.1, 0.1);
  h_pvywide = fs->make<TH1F>("h_pvywide", ";primary vertex y (cm);events/40 #mum", 50, -0.1, 0.1);
  h_pvz = fs->make<TH1F>("h_pvz", ";primary vertex z (cm);events/3.6 mm", 100, -18, 18);
  h_pvcxx = fs->make<TH1F>("h_pvcxx", ";primary vertex cxx;events", 100, 0, 5e-6);
  h_pvcyy = fs->make<TH1F>("h_pvcyy", ";primary vertex cyy;events", 100, 0, 5e-6);
  h_pvczz = fs->make<TH1F>("h_pvczz", ";primary vertex czz;events", 100, 0, 1e-5);
  h_pvcxy = fs->make<TH1F>("h_pvcxy", ";primary vertex cxy;events", 100, -1e-6, 1e-6);
  h_pvcxz = fs->make<TH1F>("h_pvcxz", ";primary vertex cxz;events", 100, -1e-6, 1e-6);
  h_pvcyz = fs->make<TH1F>("h_pvcyz", ";primary vertex cyz;events", 100, -1e-6, 1e-6);
  h_pvrho = fs->make<TH1F>("h_pvrho", ";primary vertex rho (cm);events/5 #mum", 40, 0, 0.02);
  h_pvrhowide = fs->make<TH1F>("h_pvrhowide", ";primary vertex rho (cm);events/10 #mum", 100, 0, 0.1);
  h_pvphi = fs->make<TH1F>("h_pvphi", ";primary vertex #phi (rad);events/.063", 100, -3.1416, 3.1416);
  h_pvntracks = fs->make<TH1F>("h_pvntracks", ";# of tracks in primary vertex;events/3", 100, 0, 300);
  h_pvscore = fs->make<TH1F>("h_pvscore", ";primary vertex #Sigma p_{T}^{2} (GeV^{2});events/10000 GeV^{2}", 100, 0, 1e6);
  h_pvsx = fs->make<TH1F>("h_pvsx", ";primary vertices x (cm);events/2 #mum", 200, -0.02, 0.02);
  h_pvsy = fs->make<TH1F>("h_pvsy", ";primary vertices y (cm);events/2 #mum", 200, -0.02, 0.02);
  h_pvsxwide = fs->make<TH1F>("h_pvsxwide", ";primary vertices x (cm);events/40 #mum", 50, -0.1, 0.1);
  h_pvsywide = fs->make<TH1F>("h_pvsywide", ";primary vertices y (cm);events/40 #mum", 50, -0.1, 0.1);
  h_pvsz = fs->make<TH1F>("h_pvsz", ";primary vertices z (cm);events/3.6 mm", 100, -18, 18);
  h_pvsrho = fs->make<TH1F>("h_pvsrho", ";primary vertices rho (cm);events/5 #mum", 40, 0, 0.02);
  h_pvsrhowide = fs->make<TH1F>("h_pvsrhowide", ";primary vertices rho (cm);events/10 #mum", 100, 0, 0.1);
  h_pvsphi = fs->make<TH1F>("h_pvsphi", ";primary vertices #phi (rad);events/.063", 100, -3.1416, 3.1416);
  h_pvsscore = fs->make<TH1F>("h_pvsscore", ";primary vertices #Sigma p_{T}^{2} (GeV^{2});events/10000 GeV^{2}", 100, 0, 1e6);
  h_pvsdz = fs->make<TH1F>("h_pvsdz", ";primary vertices pairs #delta z (cm);events/2 mm", 100, 0, 20);
  h_pvsmindz = fs->make<TH1F>("h_pvsmindz", ";min primary vertices pairs #delta z (cm);events/0.5 mm", 100, 0, 5);
  h_pvsmaxdz = fs->make<TH1F>("h_pvmaxdz", ";max primary vertices pairs #delta z (cm);events/2 mm", 100, 0, 20);
  h_pvsmindz_minscore = fs->make<TH1F>("h_pvmindz_minscore", ";min primary vertices pairs (with score req) #delta z (cm);events/1 mm", 100, 0, 10);
  h_pvsmaxdz_minscore = fs->make<TH1F>("h_pvmaxdz_minscore", ";max primary vertices pairs (with score req) #delta z (cm);events/1 mm", 100, 0, 10);

  h_njets = fs->make<TH1F>("h_njets", ";# of jets;events", 30, 0, 30);
  h_njets20 = fs->make<TH1F>("h_njets20", ";# of jets w. p_{T} > 20 GeV;events", 20, 0, 20);
  for (int i = 0; i < MAX_NJETS+1; ++i) {
    TString ijet = i == MAX_NJETS ? TString("all") : TString::Format("%i", i);
    h_jet_pt[i] = fs->make<TH1F>(TString::Format("h_jet_pt_%s", ijet.Data()), TString::Format(";p_{T} of jet #%s (GeV);events/10 GeV", ijet.Data()), 200, 0, 2000);
    h_jet_eta[i] = fs->make<TH1F>(TString::Format("h_jet_eta_%s", ijet.Data()), TString::Format(";absv#eta of jet #%s;events/bin", ijet.Data()), 120, 0, 6);
    h_jet_phi[i] = fs->make<TH1F>(TString::Format("h_jet_phi_%s", ijet.Data()), TString::Format(";#phi of jet #%s;events/bin", ijet.Data()), 100, -3.1416, 3.1416);

    h_bsort_jet_pt[i] = fs->make<TH1F>(TString::Format("h_bsort_jet_pt_%s", ijet.Data()), TString::Format(";p_{T} of jet w/ #%s highest CSV (GeV);events/10 GeV", ijet.Data()), 200, 0, 2000);
    h_bsort_jet_eta[i] = fs->make<TH1F>(TString::Format("h_bsort_jet_eta_%s", ijet.Data()), TString::Format(";absv#eta of jet w/ #%s highest CSV;events/bin", ijet.Data()), 130, 0, 2.6);
    h_bsort_jet_phi[i] = fs->make<TH1F>(TString::Format("h_bsort_jet_phi_%s", ijet.Data()), TString::Format(";#phi of jet w/ #%s highest CSV;events/bin", ijet.Data()), 100, -3.1416, 3.1416);
    h_bsort_jet_csv[i] = fs->make<TH1F>(TString::Format("h_bsort_jet_csv_%s", ijet.Data()), TString::Format(";CSV of jet w/ #%s highest CSV;events/bin", ijet.Data()), 100, 0, 1.0);
  }

  h_jet_energy = fs->make<TH1F>("h_jet_energy", ";jets energy (GeV);jets/10 GeV", 200, 0, 2000);
  h_jet_ht = fs->make<TH1F>("h_jet_ht", ";H_{T} of jets (GeV);events/25 GeV", 200, 0, 5000);
  h_jet_ht_40 = fs->make<TH1F>("h_jet_ht_40", ";H_{T} of jets with p_{T} > 40 GeV;events/25 GeV", 200, 0, 5000);

  for (int i = 0; i < MAX_NJETS+1; ++i) {
    TString ijet = i == MAX_NJETS ? TString("all") : TString::Format("%i", i);
    h_calo_jet_pt[i] = fs->make<TH1F>(TString::Format("h_calo_jet_pt_%s", ijet.Data()), TString::Format(";p_{T} of calo jet #%s (GeV);events/10 GeV", ijet.Data()), 200, 0, 2000);
    h_calo_jet_eta[i] = fs->make<TH1F>(TString::Format("h_calo_jet_eta_%s", ijet.Data()), TString::Format(";abs #eta of calo jet #%s;events/0.05", ijet.Data()), 120, 0, 6);
    h_calo_jet_phi[i] = fs->make<TH1F>(TString::Format("h_calo_jet_phi_%s", ijet.Data()), TString::Format(";#phi of calo jet #%s;events/0.063", ijet.Data()), 100, -3.1416, 3.1416);
  }

  h_calo_jet_ht    = fs->make<TH1F>("h_calo_jet_ht",      ";H_{T} of all calo jets;events/25 GeV", 200, 0, 5000);
  h_calo_jet_ht40  = fs->make<TH1F>("h_calo_jet_ht40",    ";H_{T} of all calo jets w/ p_{T} > 40GeV;events/25 GeV", 200, 0, 5000);

  h_online_calo_jet_ht    = fs->make<TH1F>("h_online_calo_jet_ht",      ";H_{T} of online calo jets;events/25 GeV", 200, 0, 5000);
  h_online_pf_jet_ht    = fs->make<TH1F>("h_online_pf_jet_ht",      ";H_{T} of online PF jets;events/25 GeV", 200, 0, 5000);
  h_online_offline_calo_jet_ht = fs->make<TH2F>("h_online_offline_calo_jet_ht", ";H_{T} of online calojets; H_{T} of offline calojets", 200, 0, 5000, 200, 0, 5000);
  h_online_offline_pf_jet_ht = fs->make<TH2F>("h_online_offline_pf_jet_ht", ";H_{T} of online PF jets; H_{T} of offline PF jets", 200, 0, 5000, 200, 0, 5000);

  h_online_calojet_pt = fs->make<TH1F>("h_online_calojet_pt", ";p_{T} of matched online calojets (GeV);events/bins", 200, 0, 1000);
  h_online_pfjet_pt   = fs->make<TH1F>("h_online_pfjet_pt", ";p_{T} of matched online PF jets (GeV);events/bins", 200, 0, 1000);

  h_offline_calojet_pt = fs->make<TH1F>("h_offline_calojet_pt", ";p_{T} of matched offline calojets (GeV);events/bins", 200, 0, 1000);
  h_offline_pfjet_pt   = fs->make<TH1F>("h_offline_pfjet_pt", ";p_{T} of matched offline PF jets (GeV);events/bins", 200, 0, 1000);

  h_online_offline_calojet_pt = fs->make<TH2F>("h_online_offline_calojet_pt", ";p_{T} of matched online calojets (GeV); p_{T} of matched offline calojets (GeV)", 200, 0, 1000, 200, 0, 1000);

  for (int i = 0; i < MAX_NJETS+1; ++i) {
    TString ijet = i == MAX_NJETS ? TString("all") : TString::Format("%i", i);
    h_online_offline_pfjet_pt[i] = fs->make<TH2F>(TString::Format("h_online_offline_pfjet_pt_%s", ijet.Data()), TString::Format(";p_{T} of online PF jet #%s (GeV); p_{T} of offline PF jet #%s (GeV)", ijet.Data(), ijet.Data()), 200, 0, 1000, 200, 0, 1000);
  }

  h_ncalojet_online_offline = fs->make<TH2F>("h_ncalojet_online_offline", ";N(ak4CaloJetsCorrected);  N(slimmedCaloJets)", 60, 0, 60, 60, 0, 60);
  h_ncalojet_idp_online_offline = fs->make<TH2F>("h_ncalojet_idp_online_offline", ";N(ak4CaloJetsCorrectedIdPassed); N(slimmedCaloJets)", 60, 0, 60, 60, 0, 60);
  h_calojet_ndiff_htdiff = fs->make<TH2F>("h_calojet_ndiff_htdiff", ";N(ak4CaloJetsCorrected) - N(slimmedCaloJets); HT(Online) - HT(Offline) (GeV)", 100, -50, 50, 300, -300, 300); 
  h_idp_calojet_ndiff_htdiff = fs->make<TH2F>("h_idp_calojet_ndiff_htdiff", ";N(ak4CaloJetsCorrectedIdPassed) - N(slimmedCaloJets); HT(Online) - HT(Offline) (GeV)", 100, -50, 50, 300, -300, 300);


  h_jet_pairdphi = fs->make<TH1F>("h_jet_pairdphi", ";jet pair #Delta#phi (rad);jet pairs/.063", 100, -3.1416, 3.1416);
  h_jet_pairdeta = fs->make<TH1F>("h_jet_pairdeta", ";jet pair #Delta#eta ;jet pairs/.1", 100, -5.0, 5.0);
  h_jet_pairdr = fs->make<TH1F>("h_jet_pairdr", ";jet pair #DeltaR (rad);jet pairs/.063", 100, 0, 6.3);

  h_n_vertex_seed_tracks = fs->make<TH1F>("h_n_vertex_seed_tracks", ";# vertex seed tracks;events", 100, 0, 100);
  h_vertex_seed_track_chi2dof = fs->make<TH1F>("h_vertex_seed_track_chi2dof", ";vertex seed track #chi^{2}/dof;tracks/1", 10, 0, 10);
  h_vertex_seed_track_q = fs->make<TH1F>("h_vertex_seed_track_q", ";vertex seed track charge;tracks", 3, -1, 2);
  h_vertex_seed_track_pt = fs->make<TH1F>("h_vertex_seed_track_pt", ";vertex seed track p_{T} (GeV);tracks/GeV", 300, 0, 300);
  h_vertex_seed_track_eta = fs->make<TH1F>("h_vertex_seed_track_eta", ";vertex seed track #eta;tracks/0.052", 100, -2.6, 2.6);
  h_vertex_seed_track_phi = fs->make<TH1F>("h_vertex_seed_track_phi", ";vertex seed track #phi;tracks/0.063", 100, -3.15, 3.15);
  h_vertex_seed_track_phi_v_eta = fs->make<TH2F>("h_vertex_seed_track_phi_v_eta", ";vertex seed track #eta;vertex seed track #phi", 26, -2.6, 2.6, 24, -M_PI, M_PI);
  h_vertex_seed_track_dxy = fs->make<TH1F>("h_vertex_seed_track_dxy", ";vertex seed track dxy (cm);tracks/10 #mum", 200, -0.1, 0.1);
  h_vertex_seed_track_dz = fs->make<TH1F>("h_vertex_seed_track_dz", ";vertex seed track dz (cm);tracks/10 #mum", 200, -0.1, 0.1);
  h_vertex_seed_track_err_pt = fs->make<TH1F>("h_vertex_seed_track_err_pt", ";vertex seed track #sigma(p_{T})/p_{T} (GeV);tracks/0.005", 100, 0, 0.5);
  h_vertex_seed_track_err_eta = fs->make<TH1F>("h_vertex_seed_track_err_eta", ";vertex seed track #sigma(#eta);tracks/5e-5", 100, 0, 0.005);
  h_vertex_seed_track_err_phi = fs->make<TH1F>("h_vertex_seed_track_err_phi", ";vertex seed track #sigma(#phi);tracks/5e-5", 100, 0, 0.005);
  h_vertex_seed_track_err_dxy = fs->make<TH1F>("h_vertex_seed_track_err_dxy", ";vertex seed track #sigma(dxy) (cm);tracks/3 #mum", 100, 0, 0.03);
  h_vertex_seed_track_err_dz = fs->make<TH1F>("h_vertex_seed_track_err_dz", ";vertex seed track #sigma(dz) (cm);tracks/15 #mum", 100, 0, 0.15);
  h_vertex_seed_track_npxhits = fs->make<TH1F>("h_vertex_seed_track_npxhits", ";vertex seed track # pixel hits;tracks", 10, 0, 10);
  h_vertex_seed_track_nsthits = fs->make<TH1F>("h_vertex_seed_track_nsthits", ";vertex seed track # strip hits;tracks", 50, 0, 50);
  h_vertex_seed_track_nhits = fs->make<TH1F>("h_vertex_seed_track_nhits", ";vertex seed track # hits;tracks", 60, 0, 60);
  h_vertex_seed_track_npxlayers = fs->make<TH1F>("h_vertex_seed_track_npxlayers", ";vertex seed track # pixel layers;tracks", 10, 0, 10);
  h_vertex_seed_track_nstlayers = fs->make<TH1F>("h_vertex_seed_track_nstlayers", ";vertex seed track # strip layers;tracks", 20, 0, 20);
  h_vertex_seed_track_nlayers = fs->make<TH1F>("h_vertex_seed_track_nlayers", ";vertex seed track # layers;tracks", 30, 0, 30);

  h_met = fs->make<TH1F>("h_met", ";MET (GeV);events/5 GeV", 100, 0, 500);
  h_metphi = fs->make<TH1F>("h_metphi", ";MET #phi (rad);events/.063", 100, -3.1416, 3.1416);

  const char* lmt_ex[3] = {"loose", "medium", "tight"};
  const char* lep_kind[2] = {"muon", "electron"};
  for (int i = 0; i < 3; ++i) {
    h_nbtags[i] = fs->make<TH1F>(TString::Format("h_nbtags_%i", i), TString::Format(";# of %s b tags;events", lmt_ex[i]), 10, 0, 10);
    h_nbtags_v_bquark_code[i] = fs->make<TH2F>(TString::Format("h_nbtags_v_bquark_code_%i", i), TString::Format(";bquark code;# of %s b tags", lmt_ex[i]), 3, 0, 3, 3, 0, 3);
  }
  h_jet_bdisc = fs->make<TH1F>("h_jet_bdisc", ";jets' b discriminator;jets/0.02", 51, 0, 1.02);
  h_jet_bdisc_v_bquark_code = fs->make<TH2F>("h_jet_bdisc_v_bquark_code", ";b quark code;jets' b discriminator", 3, 0, 3, 51, 0, 1.02);
  h_bjet_pt = fs->make<TH1F>("h_bjet_pt", ";bjets p_{T} (GeV);bjets/10 GeV", 150, 0, 1500);
  h_bjet_eta = fs->make<TH1F>("h_bjet_eta", ";bjets #eta (rad);bjets/.05", 120, -3, 3);
  h_bjet_phi = fs->make<TH1F>("h_bjet_phi", ";bjets #phi (rad);bjets/.063", 100, -3.1416, 3.1416);
  h_bjet_energy = fs->make<TH1F>("h_bjet_energy", ";bjets E (GeV);bjets/10 GeV", 150, 0, 1500);
  h_bjet_pairdphi = fs->make<TH1F>("h_bjet_pairdphi", ";bjet pair #Delta#phi (rad);bjet pairs/.063", 100, -3.1416, 3.1416);
  h_bjet_pairdeta = fs->make<TH1F>("h_bjet_pairdeta", ";bjet pair #Delta#eta;bjet pairs/.1", 100, -5.0, 5.0);

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
}

struct Jet_BHelper {
    float pt  = 0.0;
    float eta = 0.0;
    float phi = 0.0;
    float csv = 0.0;
};

void MFVEventHistos::analyze(const edm::Event& event, const edm::EventSetup&) {



  edm::Handle<MFVEvent> mevent;
  event.getByToken(mevent_token, mevent);

  edm::Handle<double> weight;
  event.getByToken(weight_token, weight);
  const double w = *weight;

  Jet_BHelper jetHelper[MAX_NJETS];
  for (int i=0; i < MAX_NJETS; i++) {
    jetHelper[i].pt  = mevent->nth_jet_pt(i);
    jetHelper[i].eta = fabs(mevent->nth_jet_eta(i));
    jetHelper[i].phi = mevent->nth_jet_phi(i);
    jetHelper[i].csv = (i < (int)(mevent->jet_bdisc_old.size()) ? mevent->jet_bdisc_old[i] : -9.9);
  }
  std::sort(jetHelper, jetHelper+MAX_NJETS, [](Jet_BHelper const &a, Jet_BHelper &b) -> bool{ return a.csv > b.csv; } );

  // Shaun FIXME  -- Avoid events with poor online CaloHT
  if (not (mevent->pass_filter(4) and mevent->pass_filter(5))) return;

  // Shaun FIXME  -- Only plot events which LOOK like the pass the hltBTagCaloCSV filter (filt #6), but don't
  if ((mevent->pass_filter(6)) or (jetHelper[1].csv < 0.5))
    return;

  // Shaun FIXME  -- Only plot events which LOOK like they pass the hltBTagPFCSV filter (filt #13), but don't
  //if ((mevent->pass_filter(13)) or (jetHelper[2].csv < 0.7))
  //  return;

  // Shaun FIXME  -- Only plot events which LOOK like they pass the hltBTagPFCSV filter (filt #13), AND DO
  //if not ((mevent->pass_filter(13)) and (jetHelper[2].csv > 0.7)) 
  //  return;

  // Shaun FIXME  -- Only plot events which LOOK like they pass the hltBTagCaloCSV filter (filt #6), AND DO
  //if (not ((mevent->pass_filter(6)) and (jetHelper[1].csv > 0.5)))
  //  return;

  h_w->Fill(w);

  //////////////////////////////////////////////////////////////////////////////

  h_gen_decay->Fill(mevent->gen_decay_type[0], mevent->gen_decay_type[1], w);
  h_gen_flavor_code->Fill(mevent->gen_flavor_code, w);

  const size_t nbquarks = mevent->gen_bquarks.size();
  h_nbquarks->Fill(nbquarks, w);
  for (size_t i = 0; i < nbquarks; ++i) {
    h_bquark_pt->Fill(mevent->gen_bquarks[i].Pt(), w);
    h_bquark_eta->Fill(mevent->gen_bquarks[i].Eta(), w);
    h_bquark_phi->Fill(mevent->gen_bquarks[i].Phi(), w);
    h_bquark_energy->Fill(mevent->gen_bquarks[i].E(), w);
    for (size_t j = i+1; j < nbquarks; ++j) {
      h_bquark_pairdphi->Fill(reco::deltaPhi(mevent->gen_bquarks[i].Phi(), mevent->gen_bquarks[j].Phi()), w);
      h_bquark_pairdeta->Fill(std::max(mevent->gen_bquarks[i].Eta(), mevent->gen_bquarks[j].Eta()) - std::min(mevent->gen_bquarks[i].Eta(),  mevent->gen_bquarks[j].Eta()), w);
    }
  }
  for (int igenv = 0; igenv < 2; ++igenv) {
    double genx = mevent->gen_lsp_decay[igenv*3+0];
    double geny = mevent->gen_lsp_decay[igenv*3+1];
    double genz = mevent->gen_lsp_decay[igenv*3+2];
    double genbs2ddist = mevent->mag(genx - mevent->bsx_at_z(genz),
                                     geny - mevent->bsy_at_z(genz) 
        );
    h_gen_bs2ddist->Fill(genbs2ddist, w);
    h_gen_bsxdist_bsydist->Fill(genx - mevent->bsx_at_z(genz), geny - mevent->bsy_at_z(genz), w);
  }
  h_minlspdist2d->Fill(mevent->minlspdist2d(), w);
  h_lspdist2d->Fill(mevent->lspdist2d(), w);
  h_lspdist3d->Fill(mevent->lspdist3d(), w);

  //////////////////////////////////////////////////////////////////////////////

  h_hlt_bits->Fill(0., w);
  h_l1_bits->Fill(0., w);
  h_filter_bits->Fill(0., w);
  for (int i = 0; i < mfv::n_hlt_paths; ++i) {
    if (mevent->found_hlt(i)) h_hlt_bits->Fill(1+2*i,   w);
    if (mevent->pass_hlt (i)) h_hlt_bits->Fill(1+2*i+1, w);
  }
  for (int i = 0; i < mfv::n_l1_paths; ++i) {
    if (mevent->found_l1(i)) h_l1_bits->Fill(1+2*i,   w);
    if (mevent->pass_l1 (i)) h_l1_bits->Fill(1+2*i+1, w);
  }
  for (int i = 0; i < mfv::n_filter_paths; ++i) {
    if (mevent->pass_filter (i)) h_filter_bits->Fill(i+1, w);
  }

  //////////////////////////////////////////////////////////////////////////////

  h_npu->Fill(mevent->npu, w);

  h_bsx->Fill(mevent->bsx, w);
  h_bsy->Fill(mevent->bsy, w);
  h_bsz->Fill(mevent->bsz, w);
  h_bsphi->Fill(atan2(mevent->bsy, mevent->bsx), w);

  h_npv->Fill(mevent->npv, w);
  for (auto h : { h_pvx, h_pvxwide }) h->Fill(mevent->pvx - mevent->bsx_at_z(mevent->pvz), w);
  for (auto h : { h_pvy, h_pvywide }) h->Fill(mevent->pvy - mevent->bsy_at_z(mevent->pvz), w);
  h_pvz->Fill(mevent->pvz - mevent->bsz, w);
  h_pvcxx->Fill(mevent->pvcxx, w);
  h_pvcxy->Fill(mevent->pvcxy, w);
  h_pvcxz->Fill(mevent->pvcxz, w);
  h_pvcyy->Fill(mevent->pvcyy, w);
  h_pvcyz->Fill(mevent->pvcyz, w);
  h_pvczz->Fill(mevent->pvczz, w);
  h_pvphi->Fill(atan2(mevent->pvy - mevent->bsy_at_z(mevent->pvz), mevent->pvx - mevent->bsx_at_z(mevent->pvz)), w);
  h_pvntracks->Fill(mevent->pv_ntracks, w);
  h_pvscore->Fill(mevent->pv_score, w);
  h_pvrho->Fill(mevent->pv_rho(), w);
  for (auto h : { h_pvrho, h_pvrhowide }) h->Fill(mevent->pv_rho(), w);
  for (size_t i = 0; i < mevent->npv; ++i) {
    const float z = mevent->pv_z(i);
    const float x = mevent->pv_x(i) - mevent->bsx_at_z(z);
    const float y = mevent->pv_y(i) - mevent->bsy_at_z(z);
    for (auto h : { h_pvsx, h_pvsxwide }) h->Fill(x, w);
    for (auto h : { h_pvsy, h_pvsywide }) h->Fill(y, w);
    h_pvsz->Fill(z, w);
    for (auto h : { h_pvsrho, h_pvsrhowide }) h->Fill(hypot(x,y), w);
    h_pvsphi->Fill(atan2(y,x), w);
    h_pvsscore->Fill(mevent->pv_score_(i), w);

    jmt::MinValue mindz, mindz_minscore;
    jmt::MaxValue maxdz, maxdz_minscore;
    for (size_t j = i+1; j < mevent->npv; ++j) {
      const float z2 = mevent->pv_z(j);
      //const float x2 = mevent->pv_x(j) - mevent->bsx_at_z(z);
      //const float y2 = mevent->pv_y(j) - mevent->bsy_at_z(z);
      const float dz = fabs(z-z2);
      h_pvsdz->Fill(dz, w);
      mindz(dz), maxdz(dz);
      if (mevent->pv_score_(i) > 50e3 && mevent->pv_score_(j) > 50e3)
        mindz_minscore(dz), maxdz_minscore(dz);
    }
    h_pvsmindz->Fill(mindz, w);
    h_pvsmaxdz->Fill(maxdz, w);
    h_pvsmindz_minscore->Fill(mindz_minscore, w);
    h_pvsmaxdz_minscore->Fill(maxdz_minscore, w);
  }

  h_njets->Fill(mevent->njets(), w);
  h_njets20->Fill(mevent->njets(20), w);

  for (int i = 0; i < MAX_NJETS; ++i) {
    h_jet_pt[i]->Fill(mevent->nth_jet_pt(i), w);
    h_jet_eta[i]->Fill(fabs(mevent->nth_jet_eta(i)), w);
    h_jet_phi[i]->Fill(mevent->nth_jet_phi(i), w);
  }

  for (int i = 0; i < MAX_NJETS; ++i) {
    h_bsort_jet_pt[i]->Fill(jetHelper[i].pt, w);
    h_bsort_jet_eta[i]->Fill(jetHelper[i].eta, w);
    h_bsort_jet_phi[i]->Fill(jetHelper[i].phi, w);
    h_bsort_jet_csv[i]->Fill(jetHelper[i].csv, w);
  }

  h_jet_ht->Fill(mevent->jet_ht(mfv::min_jet_pt), w);
  h_jet_ht_40->Fill(mevent->jet_ht(40), w);

  float alt_pf_ht = 0.0;
  unsigned int n_online_pfjets = mevent->hlt_pf_jet_pt.size();
  for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
    if (mevent->jet_pt[ijet] < mfv::min_jet_pt)
      continue;
    h_jet_pt[MAX_NJETS]->Fill(mevent->jet_pt[ijet], w);
    h_jet_eta[MAX_NJETS]->Fill(fabs(mevent->jet_eta[ijet]), w);
    h_jet_phi[MAX_NJETS]->Fill(mevent->jet_phi[ijet], w);


    h_jet_energy->Fill(mevent->jet_energy[ijet], w);
    for (size_t jjet = ijet+1; jjet < mevent->jet_id.size(); ++jjet) {
      if (mevent->jet_pt[jjet] < mfv::min_jet_pt)
        continue;
      h_jet_pairdphi->Fill(reco::deltaPhi(mevent->jet_phi[ijet], mevent->jet_phi[jjet]), w);
      h_jet_pairdeta->Fill(std::max(mevent->jet_eta[ijet], mevent->jet_eta[jjet]) - std::min(mevent->jet_eta[ijet], mevent->jet_eta[jjet]), w);
      h_jet_pairdr->Fill(reco::deltaR(mevent->jet_eta[ijet], mevent->jet_phi[ijet], mevent->jet_eta[jjet], mevent->jet_phi[jjet]), w);
    }

    if (ijet > n_online_pfjets) {
      continue;
    }
    else {
      h_online_offline_pfjet_pt[ijet]->Fill(mevent->jet_pt[ijet], mevent->hlt_pf_jet_pt[ijet], w);
    }

    // Find closest match between online/offline pfjets
    TLorentzVector offline_vec(mevent->jet_pt[ijet], mevent->jet_eta[ijet], mevent->jet_phi[ijet], mevent->jet_energy[ijet]);
    if (fabs(mevent->jet_eta[ijet]) > 2.5) continue;
    if (mevent->jet_pt[ijet] > 30.0) alt_pf_ht += mevent->jet_pt[ijet];
    float match_dR = 1.0;
    float match_online_pt  = -1.0;
    float match_offline_pt = -1.0;

    for (unsigned int ojet = 0; ojet < n_online_pfjets; ojet++) {
        TLorentzVector online_vec(mevent->hlt_pf_jet_pt[ojet], mevent->hlt_pf_jet_eta[ojet], mevent->hlt_pf_jet_phi[ojet], mevent->hlt_pf_jet_energy[ojet]);
        float temp_dR = offline_vec.DeltaR(online_vec);
        
        if (temp_dR < match_dR) {
          match_dR = temp_dR;
          match_online_pt  = online_vec.Pt();
          match_offline_pt = offline_vec.Pt();
        }
    }
    
    h_online_pfjet_pt->Fill(match_online_pt, w);
    h_offline_pfjet_pt->Fill(match_offline_pt, w);
    h_online_offline_pfjet_pt[MAX_NJETS]->Fill(match_online_pt, match_offline_pt, w);

  }

  // Shaun FIXME - Alternative definition of HT (jets must have |eta| < 2.5)
  float alt_calo_ht = 0.0;
  for (size_t ijet = 0; ijet < mevent->calo_jet_pt.size(); ijet++) {
    if ((mevent->calo_jet_pt[ijet] > 30.0) and ( fabs(mevent->calo_jet_eta[ijet]) < 2.5)) alt_calo_ht += mevent->calo_jet_pt[ijet];
  }

  h_online_calo_jet_ht->Fill(mevent->hlt_caloht, w);
  h_online_pf_jet_ht->Fill(mevent->hlt_ht, w);

  h_online_offline_calo_jet_ht->Fill(mevent->hlt_caloht, alt_calo_ht, w);
  h_online_offline_pf_jet_ht->Fill(mevent->hlt_ht, alt_pf_ht, w);

  h_ncalojet_online_offline->Fill(mevent->hlt_calo_jet_pt.size(), mevent->calo_jet_pt.size(), w);
  h_ncalojet_idp_online_offline->Fill(mevent->hlt_idp_calo_jet_pt.size(), mevent->calo_jet_pt.size(), w);
  h_calojet_ndiff_htdiff->Fill((int)(mevent->hlt_calo_jet_pt.size() - mevent->calo_jet_pt.size()), mevent->hlt_caloht - alt_calo_ht, w);
  h_idp_calojet_ndiff_htdiff->Fill((int)(mevent->hlt_idp_calo_jet_pt.size() - mevent->calo_jet_pt.size()), mevent->hlt_caloht - alt_calo_ht, w);

  for (size_t icjet = 0; icjet < mevent->calo_jet_pt.size(); ++icjet) {
    h_calo_jet_pt[MAX_NJETS]->Fill(mevent->calo_jet_pt[icjet], w);
    h_calo_jet_eta[MAX_NJETS]->Fill(fabs(mevent->calo_jet_eta[icjet]), w);
    h_calo_jet_phi[MAX_NJETS]->Fill(mevent->calo_jet_phi[icjet], w);

    if (icjet >= MAX_NJETS) continue;

    h_calo_jet_pt[icjet]->Fill(mevent->calo_jet_pt[icjet], w);
    h_calo_jet_eta[icjet]->Fill(fabs(mevent->calo_jet_eta[icjet]), w);
    h_calo_jet_phi[icjet]->Fill(mevent->calo_jet_phi[icjet], w);

    // Find closest match between online/offline calojets
    TLorentzVector offline_vec(mevent->calo_jet_pt[icjet], mevent->calo_jet_eta[icjet], mevent->calo_jet_phi[icjet], mevent->calo_jet_energy[icjet]);
    float match_dR = 1.0;
    float match_online_pt  = -1.0;
    float match_offline_pt = -1.0;
    int n_online_calojets = mevent->hlt_calo_jet_pt.size();

    for (int ojet = 0; ojet < n_online_calojets; ojet++) {
        TLorentzVector online_vec(mevent->hlt_calo_jet_pt[ojet], mevent->hlt_calo_jet_eta[ojet], mevent->hlt_calo_jet_phi[ojet], mevent->hlt_calo_jet_energy[ojet]);
        float temp_dR = offline_vec.DeltaR(online_vec);
        
        if (temp_dR < match_dR) {
          match_dR = temp_dR;
          match_online_pt  = online_vec.Pt();
          match_offline_pt = offline_vec.Pt();
        }
    }
    
    h_online_calojet_pt->Fill(match_online_pt, w);
    h_offline_calojet_pt->Fill(match_offline_pt, w);
    h_online_offline_calojet_pt->Fill(match_online_pt, match_offline_pt, w);


  }
  h_calo_jet_ht->Fill(mevent->calo_jet_ht(30), w);
  h_calo_jet_ht40->Fill(mevent->calo_jet_ht(40), w);

  for (int i = 0; i < 2; ++i) {
    h_nmuons[i]->Fill(mevent->nmu(i), w);
    h_nelectrons[i]->Fill(mevent->nel(i), w);
    h_nleptons[i]->Fill(mevent->nlep(i), w);
  }

  for (size_t ilep = 0; ilep < mevent->nlep(); ++ilep) {
    const size_t j = mevent->is_electron(ilep);
    for (size_t i = 0; i < 2; ++i)
      if (i == 0 || mevent->pass_lep_sel(ilep)) {
        h_leptons_pt[j][i]->Fill(mevent->lep_pt(ilep), w);
        h_leptons_eta[j][i]->Fill(mevent->lep_eta[ilep], w);
        h_leptons_phi[j][i]->Fill(mevent->lep_phi[ilep], w);
        h_leptons_dxy[j][i]->Fill(mevent->lep_dxy[ilep], w);
        h_leptons_dxybs[j][i]->Fill(mevent->lep_dxybs[ilep], w);
        h_leptons_dz[j][i]->Fill(mevent->lep_dz[ilep], w);
        h_leptons_iso[j][i]->Fill(mevent->lep_iso[ilep], w);
      }
  }

  h_met->Fill(mevent->met(), w);
  h_metphi->Fill(mevent->metphi(), w);

  for (int i = 0; i < 3; ++i) {
    h_nbtags[i]->Fill(mevent->nbtags(i), w);
    h_nbtags_v_bquark_code[i]->Fill(mevent->gen_flavor_code, mevent->nbtags(i), w);
  }
  const int ibtag = 2; // tight only
  for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
    if (mevent->jet_pt[ijet] < mfv::min_jet_pt)
      continue;
    h_jet_bdisc->Fill(mevent->jet_bdisc[ijet], w);
    h_jet_bdisc_v_bquark_code->Fill(mevent->gen_flavor_code, mevent->jet_bdisc[ijet], w);
    if (mevent->is_btagged(ijet, ibtag)) {
      h_bjet_pt->Fill(mevent->jet_pt[ijet], w);
      h_bjet_eta->Fill(mevent->jet_eta[ijet], w);
      h_bjet_phi->Fill(mevent->jet_phi[ijet], w);
      h_bjet_energy->Fill(mevent->jet_energy[ijet], w);
      for (size_t jjet = ijet+1; jjet < mevent->jet_id.size(); ++jjet) {
        if (mevent->jet_pt[jjet] < mfv::min_jet_pt)
          continue;
        if (mevent->is_btagged(jjet, ibtag)) {
          h_bjet_pairdphi->Fill(reco::deltaPhi(mevent->jet_phi[ijet], mevent->jet_phi[jjet]), w);
          h_bjet_pairdeta->Fill(std::max(mevent->jet_eta[ijet], mevent->jet_eta[jjet]) - std::min(mevent->jet_eta[ijet], mevent->jet_eta[jjet]), w);
        }
      }
    }
  }

  //////////////////////////////////////////////////////////////////////////////

  const size_t n_vertex_seed_tracks = mevent->n_vertex_seed_tracks();
  h_n_vertex_seed_tracks->Fill(n_vertex_seed_tracks, w);
  for (size_t i = 0; i < n_vertex_seed_tracks; ++i) {
    h_vertex_seed_track_chi2dof->Fill(mevent->vertex_seed_track_chi2dof[i], w);
    h_vertex_seed_track_q->Fill(mevent->vertex_seed_track_q(i), w);
    h_vertex_seed_track_pt->Fill(mevent->vertex_seed_track_pt(i), w);
    h_vertex_seed_track_eta->Fill(mevent->vertex_seed_track_eta[i], w);
    h_vertex_seed_track_phi->Fill(mevent->vertex_seed_track_phi[i], w);
    h_vertex_seed_track_phi_v_eta->Fill(mevent->vertex_seed_track_eta[i], mevent->vertex_seed_track_phi[i], w);
    h_vertex_seed_track_dxy->Fill(mevent->vertex_seed_track_dxy[i], w);
    h_vertex_seed_track_dz->Fill(mevent->vertex_seed_track_dz[i], w);
    h_vertex_seed_track_err_pt->Fill(mevent->vertex_seed_track_err_pt[i] / mevent->vertex_seed_track_pt(i), w);
    h_vertex_seed_track_err_eta->Fill(mevent->vertex_seed_track_err_eta[i], w);
    h_vertex_seed_track_err_phi->Fill(mevent->vertex_seed_track_err_phi[i], w);
    h_vertex_seed_track_err_dxy->Fill(mevent->vertex_seed_track_err_dxy[i], w);
    h_vertex_seed_track_err_dz->Fill(mevent->vertex_seed_track_err_dz[i], w);
    h_vertex_seed_track_npxhits->Fill(mevent->vertex_seed_track_npxhits(i), w);
    h_vertex_seed_track_nsthits->Fill(mevent->vertex_seed_track_nsthits(i), w);
    h_vertex_seed_track_nhits->Fill(mevent->vertex_seed_track_nhits(i), w);
    h_vertex_seed_track_npxlayers->Fill(mevent->vertex_seed_track_npxlayers(i), w);
    h_vertex_seed_track_nstlayers->Fill(mevent->vertex_seed_track_nstlayers(i), w);
    h_vertex_seed_track_nlayers->Fill(mevent->vertex_seed_track_nlayers(i), w);
  }
}

DEFINE_FWK_MODULE(MFVEventHistos);
