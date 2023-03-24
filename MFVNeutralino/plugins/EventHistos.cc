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
  TH1F* h_eventid;

  TH2F* h_gen_decay;
  TH1F* h_gen_flavor_code;
  TH1F* h_gen_leptons;
  TH1F* h_gen_jets;
  TH1F* h_gen_daughters;
  TH1F* h_gen_daughter_id;
  // closest dR between reco lepton & gen lepton
  TH1F* h_gen_ele_closestdR;
  TH1F* h_gen_mu_closestdR;

  TH1F* h_nbquarks;
  TH1F* h_bquark_pt;
  TH1F* h_bquark_eta;
  TH1F* h_bquark_phi;
  TH1F* h_bquark_energy;
  TH1F* h_bquark_pairdphi;

  TH1F* h_minlspdist2d;
  TH1F* h_lspdist2d;
  TH1F* h_lspdist3d;
  TH1F* h_gen_bs2ddist;
  TH1F* h_llp_dphi;
  TH1F* h_nmatchjet_llp;
  TH1F* h_llp_pt_vecsum;

  TH2F* h_llp0pt_llp1pt;
  TH2F* h_decay_lsp0pt_lsp1pt;
  TH2F* h_decay_llp0_llp1_quark_sumpt;
  TH2F* h_sum_matched_jetpt_llp;

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
  TH1F* h_jet_nseedtrack[MAX_NJETS+1];
  TH1F* h_jet_energy;
  TH1F* h_jet_ht;
  TH1F* h_jet_ht_40;

  TH1F* h_jet_pairdphi;
  TH1F* h_jet_pairdr;
  TH1F* h_jetel_pairdphi;
  TH1F* h_jetel_pairdr;
  TH1F* h_jetmu_pairdphi;
  TH1F* h_jetmu_pairdr;
  
  TH1F* h_met;
  TH1F* h_metphi;
  TH1F* h_metnomu;
  TH1F* h_metnomuphi;

  TH1F* h_nbtags[3];
  TH2F* h_nbtags_v_bquark_code[3];
  TH1F* h_jet_bdisc;
  TH2F* h_jet_bdisc_v_bquark_code;
  TH1F* h_bjet_pt;
  TH1F* h_bjet_eta;
  TH1F* h_bjet_phi;
  TH1F* h_bjet_energy;
  TH1F* h_bjet_pairdphi;

  TH1F* h_nmuons;
  TH1F* h_nelectrons;
  TH1F* h_nleptons;

  TH1F* h_nmuons_[3];
  TH1F* h_nelectrons_[4];
  //this is a bit uneven due to considering different el/mu working points (not much focus on tight mu or loose el) 
  // 0: loose el,mu //  1: med el,mu // 2: tight el,mu // 3: tight el, med. mu // 4: tight el, loose mu // 5: med el, loose mu 
  TH1F* h_nleptons_pass_[6];

  TH1F* h_muon_pt_[3];
  TH1F* h_muon_eta_[3];
  TH1F* h_muon_iso_[3];
  TH1F* h_muon_phi_[3];
  TH1F* h_muon_dxybs_[3];
  TH1F* h_muon_nsigmadxy_[3];
  TH1F* h_muon_dz_[3];
  TH1F* h_muon_npxhits_[3];
  TH1F* h_muon_nsthits_[3];
  TH1F* h_muon_nhits_[3];
  TH1F* h_muon_npxlayers_[3];
  TH1F* h_muon_nstlayers_[3];
  TH1F* h_muon_nlayers_[3];
  TH1F* h_electron_pt_[4];
  TH1F* h_electron_eta_[4];
  TH1F* h_electron_phi_[4];
  TH1F* h_electron_iso_[4];
  TH1F* h_electron_dxybs_[4];
  TH1F* h_electron_nsigmadxy_[4];
  TH1F* h_electron_dz_[4];
  TH1F* h_electron_dz_EB_[4];
  TH1F* h_electron_dz_EE_[4];
  TH1F* h_electron_npxhits_[4];
  TH1F* h_electron_nsthits_[4];
  TH1F* h_electron_nhits_[4];
  TH1F* h_electron_npxlayers_[4];
  TH1F* h_electron_nstlayers_[4];
  TH1F* h_electron_nlayers_[4];
  
  
  TH1F* h_n_vertex_seed_tracks;
  TH1F* h_vertex_seed_track_chi2dof;
  TH1F* h_vertex_seed_track_q;
  TH1F* h_vertex_seed_track_pt;
  TH1F* h_vertex_seed_track_pt_barrel;
  TH1F* h_vertex_seed_track_pt_endcap;
  TH1F* h_vertex_seed_track_p;
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

  //TH1F* h_nvtx_seedtracks_near_genvtx;
  
};

MFVEventHistos::MFVEventHistos(const edm::ParameterSet& cfg)
  : mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src")))
{
  edm::Service<TFileService> fs;

  h_w = fs->make<TH1F>("h_w", ";event weight;events/0.1", 100, 0, 10);
  h_eventid = fs->make<TH1F>("h_eventid", ";eventid", 10000, 0, 10000);

  h_gen_decay = fs->make<TH2F>("h_gen_decay", "0-2=e,mu,tau, 3=h;decay code #0;decay code #1", 4, 0, 4, 4, 0, 4);
  h_gen_flavor_code = fs->make<TH1F>("h_gen_flavor_code", ";quark flavor composition;events", 3, 0, 3);
  h_gen_leptons = fs->make<TH1F>("h_gen_leptons", ";gen level leptons; events", 10, 0, 10);
  h_gen_jets = fs->make<TH1F>("h_gen_jets", ";gen level jets; events", 10, 0, 10);
  h_gen_daughters = fs->make<TH1F>("h_gen_daughters", ";gen daughters; events", 10, 0, 10);
  h_gen_daughter_id = fs->make<TH1F>("h_gen_daughter_id", ";gen daughter id; events", 40, -20, 20);
  h_gen_ele_closestdR = fs->make<TH1F>("h_gen_ele_closestdR", ";dR between closest reco ele and gen ele; events", 200, 0, 0.2);
  h_gen_mu_closestdR = fs->make<TH1F>("h_gen_mu_closestdR", ";dR between closest reco mu and gen mu; events", 200, 0, 0.2);

  h_nbquarks = fs->make<TH1F>("h_nbquarks", ";# of bquarks;events", 20, 0, 20);
  h_bquark_pt = fs->make<TH1F>("h_bquark_pt", ";bquarks p_{T} (GeV);bquarks/10 GeV", 100, 0, 1000);
  h_bquark_eta = fs->make<TH1F>("h_bquark_eta", ";bquarks #eta (rad);bquarks/.08", 100, -4, 4);
  h_bquark_phi = fs->make<TH1F>("h_bquark_phi", ";bquarks #phi (rad);bquarks/.063", 100, -3.1416, 3.1416);
  h_bquark_energy = fs->make<TH1F>("h_bquark_energy", ";bquarks energy (GeV);bquarks/10 GeV", 100, 0, 1000);
  h_bquark_pairdphi = fs->make<TH1F>("h_bquark_pairdphi", ";bquark pair #Delta#phi (rad);bquark pairs/.063", 100, -3.1416, 3.1416);

  h_minlspdist2d = fs->make<TH1F>("h_minlspdist2d", ";min dist2d(gen vtx #i) (cm);events/0.1 mm", 200, 0, 2);
  h_lspdist2d = fs->make<TH1F>("h_lspdist2d", ";dist2d(gen vtx #0, #1) (cm);events/0.1 mm", 200, 0, 2);
  h_lspdist3d = fs->make<TH1F>("h_lspdist3d", ";dist3d(gen vtx #0, #1) (cm);events/0.1 mm", 200, 0, 2);
  h_gen_bs2ddist = fs->make<TH1F>("h_gen_bs2ddist", ";dist2d(gen vtx, beamspot) (cm);arb. units", 500, 0, 2.5);
  h_llp_dphi = fs->make<TH1F>("h_llp_dphi", ";delta #phi (rad); arb. unit", 100, -3.1416, 3.1416);
  h_nmatchjet_llp = fs->make<TH1F>("h_nmatchjet_llp", ";# matched jet/LLP; arb. unit", 10,0,10);
  h_llp_pt_vecsum = fs->make<TH1F>("h_llp_pt_vecsum", ";vector sum of LLP p_{T}; arb. unit", 100, 0, 1000);

  h_llp0pt_llp1pt = fs->make<TH2F>("h_llp0pt_llp1pt", ";max llp p_{T} (GeV);min llp p_{T} (GeV)", 300, 0, 3000, 300, 0, 3000);
  h_decay_lsp0pt_lsp1pt = fs->make<TH2F>("h_decay_lsp0pt_lsp1pt", ";max Neutralino p_{T} (GeV);min Neutralino p_{T} (GeV)", 300, 0, 3000, 300, 0, 3000);
  h_decay_llp0_llp1_quark_sumpt = fs->make<TH2F>("h_decay_llp0_llp1_quark_sumpt", ";max sum p_{T} of quarks from LLP (GeV);min sum p_{T} of quarks from LLP (GeV)", 100, 0, 1000, 100, 0, 1000);
  h_sum_matched_jetpt_llp = fs->make<TH2F>("h_sum_matched_jetpt_llp", ";max sum p_{T} of LLP-matched jets (GeV);min sum p_{T} of LLP-matched jets (GeV)", 100, 0, 1000, 100, 0, 1000);


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
    h_jet_eta[i] = fs->make<TH1F>(TString::Format("h_jet_eta_%s", ijet.Data()), TString::Format(";#eta of jet #%s (GeV);events/0.05", ijet.Data()), 120, -3, 3);
    h_jet_phi[i] = fs->make<TH1F>(TString::Format("h_jet_phi_%s", ijet.Data()), TString::Format(";#phi of jet #%s (GeV);events/0.063", ijet.Data()), 100, -3.1416, 3.1416);
    h_jet_nseedtrack[i] = fs->make<TH1F>(TString::Format("h_jet_nseedtrack_%s", ijet.Data()), TString::Format(";jet #%s number of seed tracks;arb. units", ijet.Data()), 50, 0, 50);
  }
  h_jet_energy = fs->make<TH1F>("h_jet_energy", ";jets energy (GeV);jets/10 GeV", 200, 0, 2000);
  h_jet_ht = fs->make<TH1F>("h_jet_ht", ";H_{T} of jets (GeV);events/25 GeV", 200, 0, 5000);
  h_jet_ht_40 = fs->make<TH1F>("h_jet_ht_40", ";H_{T} of jets with p_{T} > 40 GeV;events/25 GeV", 200, 0, 5000);

  h_jet_pairdphi = fs->make<TH1F>("h_jet_pairdphi", ";jet pair #Delta#phi (rad);jet pairs/.063", 100, -3.1416, 3.1416);
  h_jet_pairdr = fs->make<TH1F>("h_jet_pairdr", ";jet pair #DeltaR (rad);jet pairs/.063", 100, 0, 6.3);
  h_jetel_pairdphi = fs->make<TH1F>("h_jetel_pairdphi", ";jet electron pair #Delta#phi (rad);jetel pairs/.063", 100, -3.1416, 3.1416);
  h_jetel_pairdr = fs->make<TH1F>("h_jetel_pairdr", ";jet electron pair #DeltaR (rad);jetel pairs/.063", 100, 0, 6.3);
  h_jetmu_pairdphi = fs->make<TH1F>("h_jetmu_pairdphi", ";jet muon pair #Delta#phi (rad);jetmu pairs/.063", 100, -3.1416, 3.1416);
  h_jetmu_pairdr = fs->make<TH1F>("h_jetmu_pairdr", ";jet muon pair #DeltaR (rad);jetmu pairs/.063", 100, 0, 6.3);
   
  h_n_vertex_seed_tracks = fs->make<TH1F>("h_n_vertex_seed_tracks", ";# vertex seed tracks;events", 100, 0, 100);
  h_vertex_seed_track_chi2dof = fs->make<TH1F>("h_vertex_seed_track_chi2dof", ";vertex seed track #chi^{2}/dof;tracks/1", 10, 0, 10);
  h_vertex_seed_track_q = fs->make<TH1F>("h_vertex_seed_track_q", ";vertex seed track charge;tracks", 3, -1, 2);
  h_vertex_seed_track_pt = fs->make<TH1F>("h_vertex_seed_track_pt", ";vertex seed track p_{T} (GeV);tracks/GeV", 300, 0, 300);
  h_vertex_seed_track_pt_barrel = fs->make<TH1F>("h_vertex_seed_track_pt_barrel", ";vertex seed track p_{T} (GeV) barrel;tracks/GeV", 300, 0, 300);
  h_vertex_seed_track_pt_endcap = fs->make<TH1F>("h_vertex_seed_track_pt_endcap", ";vertex seed track p_{T} (GeV) endcap;tracks/GeV", 300, 0, 300);
  h_vertex_seed_track_p = fs->make<TH1F>("h_vertex_seed_track_p", ";vertex seed track p (GeV);tracks/GeV", 300, 0, 300);
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

  //h_nvtx_seedtracks_near_genvtx = fs->make<TH1F>("h_nvtx_seedtracks_near_genvtx", "; nvertex seed tracks near genvtx;tracks", 100, 0, 100);
  
  h_met = fs->make<TH1F>("h_met", ";MET (GeV);events/5 GeV", 500, 0, 2500);
  h_metphi = fs->make<TH1F>("h_metphi", ";MET #phi (rad);events/.063", 100, -3.1416, 3.1416);
  h_metnomu = fs->make<TH1F>("h_metnomu", ";METNoMu (GeV);events/5 GeV", 500, 0, 2500);
  h_metnomuphi = fs->make<TH1F>("h_metnomuphi", ";METNoMu #phi (rad);events/.063", 100, -3.1416, 3.1416);

  const char* lmt_ex[3] = {"loose", "medium", "tight"};
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

  //lepton histos
  h_nmuons = fs->make<TH1F>("h_nmuons", ";# of muons;events", 10, 0, 10);
  h_nelectrons = fs->make<TH1F>("h_nelectrons", ";# of electrons;events", 10, 0, 10);
  h_nleptons = fs->make<TH1F>("h_nleptons", ";# of leptons;events", 10, 0, 10);


  const char* ele_ex[4] = {"veto", "loose", "medium", "tight"};
  for (int i = 0; i< 4; ++i) {
    h_nelectrons_[i] = fs->make<TH1F>(TString::Format("h_nelectrons_%s", ele_ex[i]), TString::Format(";# of %s electrons;events", ele_ex[i]), 10, 0, 10);
    h_electron_pt_[i] = fs->make<TH1F>(TString::Format("h_electron_pt_%s", ele_ex[i]), TString::Format(";pt of %s electrons;electron/5 GeV", ele_ex[i]), 200, 0, 1000);
    h_electron_eta_[i] = fs->make<TH1F>(TString::Format("h_electron_eta_%s", ele_ex[i]), TString::Format(";%s electron #eta (rad);electron/.104", ele_ex[i]), 50, -2.6, 2.6);
    h_electron_phi_[i] = fs->make<TH1F>(TString::Format("h_electron_phi_%s", ele_ex[i]), TString::Format( ";%s electron #phi (rad);electron/.126", ele_ex[i]),  50, -3.1416, 3.1416);
    h_electron_iso_[i] = fs->make<TH1F>(TString::Format("h_electron_iso_%s", ele_ex[i]), TString::Format(";%s electron iso;electron/.04", ele_ex[i]), 50, 0, 2.0);
    h_electron_dxybs_[i] = fs->make<TH1F>(TString::Format("h_electron_dxybs_%s", ele_ex[i]), TString::Format(";dxybs of %s electrons;electron/50 #mum", ele_ex[i]), 400, -2.0, 2.0);
    h_electron_nsigmadxy_[i] = fs->make<TH1F>(TString::Format("h_electron_nsigmadxy_%s", ele_ex[i]), TString::Format(";%s muon n#sigma(dxy);arb. units", ele_ex[i]), 400, -60, 60);
    h_electron_dz_[i] = fs->make<TH1F>(TString::Format("h_electron_dz_%s", ele_ex[i]), TString::Format(";dz of %s electrons;electron/50 #mum", ele_ex[i]), 400, -2.0, 2.0);
    h_electron_dz_EB_[i] = fs->make<TH1F>(TString::Format("h_electron_dz_EB_%s", ele_ex[i]), TString::Format(";dz of %s EB electrons;electron/50 #mum", ele_ex[i]), 400, -2.0, 2.0);
    h_electron_dz_EE_[i] = fs->make<TH1F>(TString::Format("h_electron_dz_EE_%s", ele_ex[i]), TString::Format(";dz of %s EE electrons;electron/50 #mum", ele_ex[i]), 400, -2.0, 2.0);
    h_electron_npxhits_[i] = fs->make<TH1F>(TString::Format("h_electron_npxhits_%s", ele_ex[i]), TString::Format("; %s electron # pixel hits;tracks", ele_ex[i]), 10, 0, 10);
    h_electron_nsthits_[i] = fs->make<TH1F>(TString::Format("h_electron_nsthits_%s", ele_ex[i]), TString::Format("; %s electron # strip hits;tracks", ele_ex[i]), 50, 0, 50);
    h_electron_nhits_[i] = fs->make<TH1F>(TString::Format("h_electron_nhits_%s", ele_ex[i]), TString::Format("; %s electron # hits;tracks", ele_ex[i]), 60, 0, 60);
    h_electron_npxlayers_[i] = fs->make<TH1F>(TString::Format("h_electron_npxlayers_%s", ele_ex[i]), TString::Format(";%s electron # pixel layers;tracks", ele_ex[i]), 10, 0, 10);
    h_electron_nstlayers_[i] = fs->make<TH1F>(TString::Format("h_electron_nstlayers_%s", ele_ex[i]), TString::Format(";%s electron # strip layers;tracks", ele_ex[i]), 20, 0, 20);
    h_electron_nlayers_[i] = fs->make<TH1F>(TString::Format("h_electron_nlayers_%s", ele_ex[i]), TString::Format("; %s electron # layers;tracks", ele_ex[i]), 30, 0, 30);
  }
    
  const char* mu_ex[3] = {"loose", "medium", "tight"};
  for (int i = 0; i < 3; ++i) {
    h_nmuons_[i] = fs->make<TH1F>(TString::Format("h_nmuons_%s", mu_ex[i]), TString::Format(";# of %s muons;events", mu_ex[i]), 10, 0, 10);
    h_muon_pt_[i] = fs->make<TH1F>(TString::Format("h_muon_pt_%s", mu_ex[i]), TString::Format(";pt of %s muons;muon/5 GeV", mu_ex[i]), 200, 0, 1000);
    h_muon_eta_[i] = fs->make<TH1F>(TString::Format("h_muon_eta_%s", mu_ex[i]), TString::Format("; %s muon #eta (rad);muon/.104", mu_ex[i]), 50, -2.6, 2.6);
    h_muon_phi_[i] = fs->make<TH1F>(TString::Format("h_muon_phi_%s", mu_ex[i]), TString::Format("; %s muon #phi (rad);muon/.126", mu_ex[i]), 50, -3.1416, 3.1416);
    h_muon_iso_[i] = fs->make<TH1F>(TString::Format("h_muon_iso_%s", mu_ex[i]), TString::Format(";%s muon iso;muon/.04", mu_ex[i]), 50, 0, 2.0);
    h_muon_dxybs_[i] = fs->make<TH1F>(TString::Format("h_muon_dxybs_%s", mu_ex[i]), TString::Format(";dxybs of %s muons;muon/50 #mum", mu_ex[i]), 400, -2.0, 2.0);
    h_muon_nsigmadxy_[i] = fs->make<TH1F>(TString::Format("h_muon_nsigmadxy_%s", mu_ex[i]), TString::Format(";%s muon n#sigma(dxy);arb. units", mu_ex[i]), 400, -60, 60);
    h_muon_dz_[i] = fs->make<TH1F>(TString::Format("h_muon_dz_%s", mu_ex[i]), TString::Format(";dz of %s muons;muon/50 #mum", mu_ex[i]), 400, -2.0, 2.0);
    h_muon_npxhits_[i] = fs->make<TH1F>(TString::Format("h_muon_npxhits_%s", mu_ex[i]), TString::Format("; %s muon # pixel hits;tracks", mu_ex[i]), 10, 0, 10);
    h_muon_nsthits_[i] = fs->make<TH1F>(TString::Format("h_muon_nsthits_%s", mu_ex[i]), TString::Format("; %s muon # strip hits;tracks", mu_ex[i]), 50, 0, 50);
    h_muon_nhits_[i] = fs->make<TH1F>(TString::Format("h_muon_nhits_%s", mu_ex[i]), TString::Format("; %s muon # hits;tracks", mu_ex[i]),  60, 0, 60);
    h_muon_npxlayers_[i] = fs->make<TH1F>(TString::Format("h_muon_npxlayers_%s", mu_ex[i]), TString::Format("; %s muon # pixel layers;tracks", mu_ex[i]), 10, 0, 10);
    h_muon_nstlayers_[i] = fs->make<TH1F>(TString::Format("h_muon_nstlayers_%s", mu_ex[i]), TString::Format("; %s muon # strip layers;tracks", mu_ex[i]), 20, 0, 20);
    h_muon_nlayers_[i] = fs->make<TH1F>(TString::Format("h_muon_nlayers_%s", mu_ex[i]), TString::Format("; %s muon # layers;tracks", mu_ex[i]), 30, 0, 30);
  }

    
  //  for nsel leptons; as stated above 
  const char* sel_ex[6] = {"loose_emu", "med_emu", "tight_emu", "tight_e_med_mu", "tight_e_loose_mu", "med_e_loose_mu"};
  for (int i = 0; i < 6; ++i) {
    h_nleptons_pass_[i] = fs->make<TH1F>(TString::Format("h_nleptons_pass_%s", sel_ex[i]), TString::Format(";# of %s;events", sel_ex[i]), 10, 0, 10);
  }
}

void MFVEventHistos::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<MFVEvent> mevent;
  event.getByToken(mevent_token, mevent);

  edm::Handle<double> weight;
  event.getByToken(weight_token, weight);
  const double w = *weight;
  h_w->Fill(w);
  h_eventid->Fill(event.id().event());

  //////////////////////////////////////////////////////////////////////////////

  h_gen_decay->Fill(mevent->gen_decay_type[0], mevent->gen_decay_type[1], w);

  h_gen_flavor_code->Fill(mevent->gen_flavor_code, w);

  const size_t ngenlep = mevent->gen_leptons.size();
  h_gen_leptons->Fill(ngenlep, w);
    
  const size_t ngenjet = mevent->gen_jets.size();
  h_gen_jets->Fill(ngenjet, w);

  const size_t ngendaughter = mevent->gen_daughters.size();
  h_gen_daughters->Fill(ngendaughter, w);
  for (size_t i = 0; i < ngendaughter; ++i) {
    h_gen_daughter_id->Fill(mevent->gen_daughter_id[i], w);

    if (abs(mevent->gen_daughter_id[i]) == 11) {
      double gd_eta = mevent->gen_daughters[i].Eta();
      double gd_phi = mevent->gen_daughters[i].Phi();
      //double mindR2 = 999.0;
      std::vector<double> mindR2;
      for (int ie=0; ie<mevent->nelectrons(); ++ie){
        double dR2 = reco::deltaR2(mevent->nth_ele_eta(ie), mevent->nth_ele_phi(ie), gd_eta, gd_phi);
        // if (dR2 < mindR2) {
        //   dR2 = mindR2;
        // }
        mindR2.push_back(dR2);
      }
      if (mevent->nelectrons() !=0)
        h_gen_ele_closestdR->Fill(*min_element(mindR2.begin(), mindR2.end()), w);
    }
    else if (abs(mevent->gen_daughter_id[i]) == 13 ) {
      double gd_eta = mevent->gen_daughters[i].Eta();
      double gd_phi = mevent->gen_daughters[i].Phi();
      //double mindR2 = 999.0;
      std::vector<double> mindR2;
      for (int im=0; im<mevent->nmuons(); ++im){
        double dR2 = reco::deltaR2(mevent->nth_mu_eta(im), mevent->nth_mu_phi(im), gd_eta, gd_phi);
        mindR2.push_back(dR2);
      }
      if (mevent->nmuons() !=0)
        h_gen_mu_closestdR->Fill(*min_element(mindR2.begin(), mindR2.end()), w);
    }
  }


  const size_t nbquarks = mevent->gen_bquarks.size();
  h_nbquarks->Fill(nbquarks, w);
  for (size_t i = 0; i < nbquarks; ++i) {
    h_bquark_pt->Fill(mevent->gen_bquarks[i].Pt(), w);
    h_bquark_eta->Fill(mevent->gen_bquarks[i].Eta(), w);
    h_bquark_phi->Fill(mevent->gen_bquarks[i].Phi(), w);
    h_bquark_energy->Fill(mevent->gen_bquarks[i].E(), w);
    for (size_t j = i+1; j < nbquarks; ++j)
      h_bquark_pairdphi->Fill(reco::deltaPhi(mevent->gen_bquarks[i].Phi(), mevent->gen_bquarks[j].Phi()), w);
  }

  for (int igenv = 0; igenv < 2; ++igenv) {
    double genx = mevent->gen_lsp_decay[igenv*3+0];
    double geny = mevent->gen_lsp_decay[igenv*3+1];
    double genz = mevent->gen_lsp_decay[igenv*3+2];
    double genbs2ddist = mevent->mag(genx - mevent->bsx_at_z(genz),
                                     geny - mevent->bsy_at_z(genz) 
        );
    h_gen_bs2ddist->Fill(genbs2ddist, w);
  }

  h_minlspdist2d->Fill(mevent->minlspdist2d(), w);
  h_lspdist2d->Fill(mevent->lspdist2d(), w);
  h_lspdist3d->Fill(mevent->lspdist3d(), w);
  h_llp_dphi->Fill(mevent->gen_lsp_phi[0]-mevent->gen_lsp_phi[1], w);

  h_llp_pt_vecsum->Fill((mevent->gen_lsp_p4(0)+mevent->gen_lsp_p4(1)).Pt(), w);
  h_llp0pt_llp1pt->Fill(std::max(mevent->gen_lsp_pt[0], mevent->gen_lsp_pt[1]), std::min(mevent->gen_lsp_pt[0], mevent->gen_lsp_pt[1]), w);
  double decay_quarks0_pt[2] = {-1,-1};
  double decay_quarks1_pt[2] = {-1,-1};
  double decaylsp0_pt = -1;
  double decaylsp1_pt = -1;
  double decay_jets0_pt[2] = {-1,-1};
  double decay_jets1_pt[2] = {-1,-1};
  double nmatched_0 = 0;
  double nmatched_1 = 0;
  for (size_t i=0; i<mevent->gen_daughters.size(); ++i){
    if (abs(mevent->gen_daughter_id[i])==1000006){
      // FIXME: this part only works for DispSUSY because of the pdgID and the number of daughters from each LLP
      // get pT for neutralinos from the decay of gluino --ignoring for now
      // this only works for splitSUSY samples because it's looking for stop(1000006) as gen_daughter
      // see vertex histos for the lepton distributions
      if (decaylsp0_pt>0){
        decaylsp1_pt = mevent->gen_daughters[i].Pt();
      }
      else{
        decaylsp0_pt = mevent->gen_daughters[i].Pt();
      }
    }
    else{
      // match jets to gen quarks from LLP decay
      double gd_eta = mevent->gen_daughters[i].Eta();
      double gd_phi = mevent->gen_daughters[i].Phi();
      int n_matched = 0;
      double pt_sum = 0;
      for (int ij = 0; ij<MAX_NJETS; ++ij){
        double dR2 = (mevent->nth_jet_eta(ij)-gd_eta)*(mevent->nth_jet_eta(ij)-gd_eta)+(mevent->nth_jet_phi(ij)-gd_phi)*(mevent->nth_jet_phi(ij)-gd_phi);
        if (dR2<0.16){
          n_matched += 1;
          pt_sum += mevent->nth_jet_pt(ij);
        }
      }
      if (i<2){
        // daughter from the first LLP
        nmatched_0 += n_matched;
        if (decay_quarks0_pt[0]>=0){
          decay_quarks0_pt[1] = mevent->gen_daughters[i].Pt();
          decay_jets0_pt[1] = pt_sum;
        }
        else{
          decay_quarks0_pt[0] = mevent->gen_daughters[i].Pt();
          decay_jets0_pt[0] = pt_sum;
        }
      }
      else{
        // daughters from the second LLP
        nmatched_1 += n_matched;
        if (decay_quarks1_pt[0]>=0){
          decay_quarks1_pt[1] = mevent->gen_daughters[i].Pt();
          decay_jets1_pt[1] = pt_sum;
        }
        else{
          decay_quarks1_pt[0] = mevent->gen_daughters[i].Pt();
          decay_jets1_pt[0] = pt_sum;
        }
      }
    }
  }
  h_decay_lsp0pt_lsp1pt->Fill(std::max(decaylsp0_pt, decaylsp1_pt), std::min(decaylsp0_pt, decaylsp1_pt), w);
  h_decay_llp0_llp1_quark_sumpt->Fill(std::max(decay_quarks0_pt[0]+decay_quarks0_pt[1], decay_quarks1_pt[0]+decay_quarks1_pt[1]), std::min(decay_quarks0_pt[0]+decay_quarks0_pt[1], decay_quarks1_pt[0]+decay_quarks1_pt[1]), w);
  h_nmatchjet_llp->Fill(nmatched_0, w);
  h_nmatchjet_llp->Fill(nmatched_1, w);
  h_sum_matched_jetpt_llp->Fill(std::max(decay_jets0_pt[0]+decay_jets0_pt[1], decay_jets1_pt[0]+decay_jets1_pt[1]), std::min(decay_jets0_pt[0]+decay_jets0_pt[1], decay_jets1_pt[0]+decay_jets1_pt[1]), w);

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
    h_jet_eta[i]->Fill(mevent->nth_jet_eta(i), w);
    h_jet_phi[i]->Fill(mevent->nth_jet_phi(i), w);
  }
  h_jet_ht->Fill(mevent->jet_ht(mfv::min_jet_pt), w);
  h_jet_ht_40->Fill(mevent->jet_ht(40), w);

  for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
    if (mevent->jet_pt[ijet] < mfv::min_jet_pt)
      continue;
    h_jet_pt[MAX_NJETS]->Fill(mevent->jet_pt[ijet], w);
    h_jet_eta[MAX_NJETS]->Fill(mevent->jet_eta[ijet], w);
    h_jet_phi[MAX_NJETS]->Fill(mevent->jet_phi[ijet], w);
    h_jet_energy->Fill(mevent->jet_energy[ijet], w);
    for (size_t jjet = ijet+1; jjet < mevent->jet_id.size(); ++jjet) {
      if (mevent->jet_pt[jjet] < mfv::min_jet_pt)
        continue;
      h_jet_pairdphi->Fill(reco::deltaPhi(mevent->jet_phi[ijet], mevent->jet_phi[jjet]), w);
      h_jet_pairdr->Fill(reco::deltaR(mevent->jet_eta[ijet], mevent->jet_phi[ijet], mevent->jet_eta[jjet], mevent->jet_phi[jjet]), w);
    }
  }


  h_nmuons->Fill(mevent->nmuons(), w);
  h_nelectrons->Fill(mevent->nelectrons(), w);
  h_nleptons->Fill(mevent->nlep(), w);
  //initialize number of muons that pass : loose, medium, tight (similar for electrons, but add veto)
  std::vector<int> nmuons{ 0, 0, 0 };
  std::vector<int> nelectrons{ 0, 0, 0, 0 };

  //placeholder 2d vector to be able to fill nsellepton histo for all the different cases; 1st is el, 2nd is mu
  std::vector<std::vector<int>> nlept_idx{
  					  { 0, 1 },
  					  { 1, 2 },
  					  { 2, 3 },
  					  { 1, 3 },
  					  { 0, 3 },
  					  { 0, 2 } };

  //muons
  for (int imu = 0; imu < mevent->nmuons(); ++imu) {
    for (int j = 0; j < 3; ++j) {

      if (mevent->muon_ID[imu][j] == 1) {
  	nmuons[j] += 1;
      }
   	
      h_muon_pt_[j]->Fill(mevent->muon_pt[imu], w);
      h_muon_eta_[j]->Fill(mevent->muon_eta[imu], w);
      h_muon_phi_[j]->Fill(mevent->muon_phi[imu], w);
      h_muon_iso_[j]->Fill(mevent->muon_iso[imu], w);
      h_muon_dxybs_[j]->Fill(mevent->muon_dxybs[imu], w);
      h_muon_nsigmadxy_[j]->Fill(mevent->muon_dxybs[imu] / mevent->muon_dxyerr[imu], w);
      h_muon_dz_[j]->Fill(mevent->muon_dz[imu], w);
      h_muon_npxhits_[j]->Fill(mevent->muon_npxhits(imu), w);
      h_muon_nsthits_[j]->Fill(mevent->muon_nsthits(imu), w);
      h_muon_nhits_[j]->Fill(mevent->muon_nhits(imu) , w);
      h_muon_nstlayers_[j]->Fill(mevent->muon_nstlayers(imu), w);
      h_muon_npxlayers_[j]->Fill(mevent->muon_npxlayers(imu), w);
      h_muon_nlayers_[j]->Fill(mevent->muon_nlayers(imu), w);
      
    }
  }

  for (int j = 0; j < 3; ++j) {
    h_nmuons_[j]->Fill(nmuons[j], w);
  }

  //electrons
  for (int iel = 0; iel < mevent->nelectrons(); ++iel) {
    for (int j = 0; j < 4; ++j) {

      if (mevent->electron_ID[iel][j] == 1) {
      	nelectrons[j] +=1;
      }
      h_electron_pt_[j]->Fill(mevent->electron_pt[iel], w);
      h_electron_eta_[j]->Fill(mevent->electron_eta[iel], w);
      h_electron_phi_[j]->Fill(mevent->electron_phi[iel], w);
      h_electron_iso_[j]->Fill(mevent->electron_iso[iel], w);	
      h_electron_dxybs_[j]->Fill(mevent->electron_dxybs[iel], w);
      h_electron_nsigmadxy_[j]->Fill(mevent->electron_dxybs[iel] / mevent->electron_dxyerr[iel], w);
      h_electron_dz_[j]->Fill(mevent->electron_dz[iel], w);
      h_electron_npxhits_[j]->Fill(mevent->electron_npxhits(iel), w);
      h_electron_nsthits_[j]->Fill(mevent->electron_nsthits(iel), w);
      h_electron_nhits_[j]->Fill(mevent->electron_nhits(iel), w);
      h_electron_nstlayers_[j]->Fill(mevent->electron_nstlayers(iel), w);
      h_electron_npxlayers_[j]->Fill(mevent->electron_npxlayers(iel), w);
      h_electron_nlayers_[j]->Fill(mevent->electron_nlayers(iel), w);
	
      if (mevent->electron_isEB[iel] == 1) {
    	h_electron_dz_EB_[j]->Fill(mevent->electron_dz[iel], w);
      }

      else if (mevent->electron_isEE[iel] == 1) {
    	h_electron_dz_EE_[j]->Fill(mevent->electron_dz[iel], w);
      }
    }
  }

  for (int j = 0; j < 4; ++j) {
    h_nelectrons_[j]->Fill(nelectrons[j], w);
  }

  // to get the correct muon, electron -- have to reference the lepton index
  for (int l = 0; l < 6; ++l) {
      h_nleptons_pass_[l]->Fill((nmuons[nlept_idx[l][0]] + nelectrons[nlept_idx[l][1]]), w);
  }

  // // now to check the relation between jets and electrons/muons
  // // only considering selected leptons (pt, eta, iso) 
  int highjet = 0;
  for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
    if (mevent->jet_pt[ijet] < mfv::min_jet_pt)
      continue;
    highjet +=1;
    int highel = 0;
    for (int iselel = 0; iselel < mevent->nelectrons(); ++iselel) {
      if (mevent->electron_ID[iselel][3] == 1) {
  	if (mevent->electron_pt[iselel] > 35) {
  	  if (abs(mevent->electron_eta[iselel]) < 2.5) {
  	    if (mevent->electron_iso[iselel] < 0.1) {
  	      highel +=1;
	      if (highjet < 3 && highel < 2) {
  		h_jetel_pairdphi->Fill(reco::deltaPhi(mevent->jet_phi[ijet], mevent->electron_phi[iselel]), w);
  		h_jetel_pairdr->Fill(reco::deltaR(mevent->jet_eta[ijet], mevent->jet_phi[ijet], mevent->electron_eta[iselel], mevent->electron_phi[iselel]), w);
  	      }
  	    }
  	  }
  	}
      }
    }
    int highmu = 0;
    for (int iselmu = 0; iselmu < mevent->nmuons(); ++iselmu) {
      if (mevent->muon_ID[iselmu][1] == 1) {
  	if (mevent->muon_pt[iselmu] > 26) {
  	  if (abs(mevent->muon_eta[iselmu]) < 2.4) {
  	    if (mevent->muon_iso[iselmu] < 0.15) {
  	      highmu +=1;
	      if (highjet < 3 && highmu < 2) {
  		h_jetmu_pairdphi->Fill(reco::deltaPhi(mevent->jet_phi[ijet], mevent->muon_phi[iselmu]), w);
  		h_jetmu_pairdr->Fill(reco::deltaR(mevent->jet_eta[ijet], mevent->jet_phi[ijet], mevent->muon_eta[iselmu], mevent->muon_phi[iselmu]), w);
  	      }
  	    }
  	  }
  	}
      }
    }
  }

  
  h_met->Fill(mevent->met(), w);
  h_metphi->Fill(mevent->metphi(), w);
  h_metnomu->Fill(mevent->metNoMu(), w);
  h_metnomuphi->Fill(mevent->metNoMuphi(), w);

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
        }
      }
    }
  }

  //////////////////////////////////////////////////////////////////////////////

  const size_t n_vertex_seed_tracks = mevent->n_vertex_seed_tracks();
  std::vector<int> track_which_jet;
  //const int nvtx_seedtracks_near_genvtx = 0;
  
  h_n_vertex_seed_tracks->Fill(n_vertex_seed_tracks, w);
  for (size_t i = 0; i < n_vertex_seed_tracks; ++i) {
    h_vertex_seed_track_chi2dof->Fill(mevent->vertex_seed_track_chi2dof[i], w);
    h_vertex_seed_track_q->Fill(mevent->vertex_seed_track_q(i), w);
    h_vertex_seed_track_pt->Fill(mevent->vertex_seed_track_pt(i), w);
    if (abs(mevent->vertex_seed_track_eta[i])<1.4){
      h_vertex_seed_track_pt_barrel->Fill(mevent->vertex_seed_track_pt(i), w);
    }
    else{
      h_vertex_seed_track_pt_endcap->Fill(mevent->vertex_seed_track_pt(i), w);
    }
    TVector3 v;
    v.SetPtEtaPhi(mevent->vertex_seed_track_pt(i),mevent->vertex_seed_track_eta[i],mevent->vertex_seed_track_phi[i]);
    h_vertex_seed_track_p->Fill(v.Mag(), w);

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

    double match_threshold = 1.3;
    int jet_index = 255;
    for (unsigned j = 0; j < mevent->jet_track_which_jet.size(); ++j) {
      double a = fabs(mevent->vertex_seed_track_pt(i) - fabs(mevent->jet_track_qpt[j])) + 1;
      double b = fabs(mevent->vertex_seed_track_eta[i] - mevent->jet_track_eta[j]) + 1;
      double c = fabs(mevent->vertex_seed_track_phi[i] - mevent->jet_track_phi[j]) + 1;
      if (a * b * c < match_threshold) {
        match_threshold = a * b * c;
        jet_index = mevent->jet_track_which_jet[j];
      }
    }
    if (jet_index != 255) {
      track_which_jet.push_back((int) jet_index);
    }
  }
  int njet_seedtrack = 0;
  for (size_t i = 0; i<mevent->jet_id.size(); ++i){
    int n_seedtrack = std::count(track_which_jet.begin(), track_which_jet.end(), i);
    njet_seedtrack += n_seedtrack;
    if (i<MAX_NJETS)
      h_jet_nseedtrack[i]->Fill(n_seedtrack, w);
  }
  h_jet_nseedtrack[MAX_NJETS]->Fill(njet_seedtrack, w);
}

DEFINE_FWK_MODULE(MFVEventHistos);
