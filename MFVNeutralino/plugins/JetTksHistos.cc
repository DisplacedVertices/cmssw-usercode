#include <stdio.h>
#include <math.h>
#include <random>
#include "TH2F.h"
#include "TH3F.h"
#include "TRandom3.h"
#include "TVector2.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
//#include "CondFormats/BTauObjects/interface/BTagCalibration.h"
//#include "CondTools/BTau/interface/BTagCalibrationReader.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/ExtValue.h"
#include "JMTucker/Tools/interface/GenUtilities.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/Tools/interface/UncertTools.h"
#include "JMTucker/Tools/interface/Year.h"
#include "JMTucker/MFVNeutralinoFormats/interface/MCInteractions.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralino/interface/EventTools.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/Tools/interface/Math.h"

class MFVJetTksHistos : public edm::EDAnalyzer {
 public:
  explicit MFVJetTksHistos(const edm::ParameterSet&);
  //bool refactor_survival(const int, const bool, const float);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::EDGetTokenT<MFVEvent> mevent_token;
  const edm::EDGetTokenT<double> weight_token;
  const edm::EDGetTokenT<MFVVertexAuxCollection> vertex_token;

  std::mt19937 rng;
  std::uniform_real_distribution<float> distribution;
  std::normal_distribution<double> gaussian;

  static const int CATEGORIES = 5;
  const int ALL      = 0;
  const int PASS_HLT = 1;
  const int FAIL_HLT = 2;
  //const int PASS_OFF = 3;
  //const int FAIL_OFF = 4;
  const int PASS_HLT_CALO_BJET = 3;
  const int PASS_HLT_CALO_LOW_BJET = 4;

  static const int CALO_CATEGORIES = 4;
  // const int ALL       = 0;
  const int PASS_CALO_PROMPT = 1;
  const int PASS_CALO_DISP   = 2;
  const int PASS_HLT_BTAG    = 3;

  static const int   dxy_nbins = 9;
  Double_t dxy_edges[dxy_nbins+1] = {0.0, 0.025, 0.05, 0.075, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50};

  const double offline_csv;
  const double pt_thresh_shift;
  const double pt_lo_for_tag_probe;
  const double pt_hi_for_tag_probe;
  const double tk_match_shift;
  const double soft_tk_thresh;
  const bool plot_soft_tks;
  const bool plot_hard_tks;
  const bool require_triggers;
  const bool veto_bjet_events;
  const bool require_tk_quality;
  const bool require_gen_sumdbv;
  const bool require_two_good_leptons;
  const bool do_tk_filt_refactor;
  const bool get_hlt_btag_factors_pf;
  const bool get_hlt_btag_factors_calo;
  const bool get_hlt_btag_factors_calo_low;
  const bool force_hlt_btag_study;
  const bool require_match_to_hlt;
  const bool require_early_b_filt;
  const bool apply_hlt_btagging;
  const bool apply_offline_dxy_res;
  const int calojet_category;
  const int trigger_bit;

  TH1F* h_w;
  TH2F* h_calojet_nweird_ngood;
  TH1F* h_calojet_sum_good_weird;

  TH2F* h_pfjet_pt_2d;
  TH2F* h_pfjet_pt_dpt;
  TH2F* h_pfjet_eta_deta;
  TH2F* h_pfjet_phi_dphi;
  TH1F* h_pfjet_frac_dpt;
  TH1F* h_pfjet_match_dR0;
  TH1F* h_pfjet_match_dR1;

  TH2F* h_calojet_pt_2d;
  TH2F* h_calojet_pt_dpt;
  TH1F* h_calojet_pt_pass_pt;
  TH2F* h_calojet_eta_deta;
  TH2F* h_calojet_phi_dphi;
  TH1F* h_calojet_frac_dpt;
  TH1F* h_calojet_match_dR0;
  TH1F* h_calojet_match_dR1;
  TH1F* h_calojet_pfjet_dR;

  TH1F* h_calojet_dxy_den0;
  TH1F* h_calojet_dxy_den1;
  TH1F* h_calojet_dxy_num0;
  TH1F* h_calojet_dxy_num1;

  TH1F* h_jet_pt[CATEGORIES];
  TH1F* h_jet_eta[CATEGORIES];
  TH1F* h_jet_phi[CATEGORIES];
  TH1F* h_jet_dbv[CATEGORIES];
  TH1F* h_jet_ntks[CATEGORIES];
  TH1F* h_jet_bdisc_deepflav[CATEGORIES];
  TH1F* h_jet_bdisc_deepcsv[CATEGORIES];
  TH1F* h_jet_bdisc_csv[CATEGORIES];
  TH1F* h_jet_min_hlt_dR[CATEGORIES];
  TH1F* h_jet_min_hlt_calo_dR[CATEGORIES];
  TH1F* h_jet_hlt_calo_dpt[CATEGORIES];
  TH1F* h_jet_min_hlt_bjet_dR[CATEGORIES];
  TH1F* h_jet_min_hlt_calo_bjet_dR[CATEGORIES];
  TH1F* h_jet_matches_hlt[CATEGORIES];
  TH1F* h_jet_matches_hlt_bjet[CATEGORIES];
  TH1F* h_jet_matches_hlt_calo_bjet[CATEGORIES];

  TH1F* h_calojet_ntagged;
  TH1F* h_calojet_npasshlt;
  TH1F* h_calojet_npassprompt;

  TH1F* h_calo_jettk_dxy;
  TH3F* h_calo_jettk_dxy_ic_mult;  // ugh ... 
  TH1F* h_calo_jettk_dxyerr;
  TH1F* h_calo_jettk_nsigmadxy;
  TH1F* h_calo_jettk_pt;
  TH1F* h_calo_jettk_eta;
  TH1F* h_calo_jettk_phi;
  TH1F* h_calo_jettk_deta;
  TH1F* h_calo_jettk_dphi;
  TH1F* h_calo_jettk_deltaR;
  TH2F* h_calo_jettk_deta_dxy;
  TH2F* h_calo_jettk_dphi_dxy;
  TH2F* h_calo_jettk_deltaR_dxy;
  TH1F* h_calo_jettk_npxhits;
  TH1F* h_calo_jettk_nsthits;

  TH1F* h_calojet_pt[CALO_CATEGORIES];
  TH1F* h_calojet_pt_raw[CALO_CATEGORIES];
  TH1F* h_calojet_eta[CALO_CATEGORIES];
  TH1F* h_calojet_phi[CALO_CATEGORIES];
  TH1F* h_calojet_dbv[CALO_CATEGORIES];
  TH1F* h_calojet_dxy[CALO_CATEGORIES];
  TH1F* h_calojet_pf_dR[CALO_CATEGORIES];
  TH1F* h_calojet_pf_next_dR[CALO_CATEGORIES];
  TH1F* h_calojet_csv[CALO_CATEGORIES];
  TH1F* h_calojet_pudisc[CALO_CATEGORIES];
  TH1F* h_calojet_filtscore[CALO_CATEGORIES];
  TH1F* h_calojet_ntks[CALO_CATEGORIES];
  TH1F* h_calojet_njettks[CALO_CATEGORIES];
  TH1F* h_calojet_nprompttks[CALO_CATEGORIES];
  TH1F* h_calojet_ndisptks[CALO_CATEGORIES];
  TH1F* h_calojet_jettk_dxy[CALO_CATEGORIES];
  TH2F* h_calojet_jettk_iclose_dxy[CALO_CATEGORIES];
  TH2F* h_calojet_jettk_iclose_pt[CALO_CATEGORIES];
  TH2F* h_calojet_jettk_iclose_eta[CALO_CATEGORIES];
  TH2F* h_calojet_jettk_iclose_dR[CALO_CATEGORIES];
  TH2F* h_calojet_jettk_iclose_npxhits[CALO_CATEGORIES];
  TH2F* h_calojet_jettk_iclose_nsthits[CALO_CATEGORIES];
  TH2F* h_calojet_jettk_ifar_dxy[CALO_CATEGORIES];
  TH1F* h_calojet_jettk_nsigmadxy[CALO_CATEGORIES];
  TH2F* h_calojet_jettk_iclose_nsigmadxy[CALO_CATEGORIES];
  TH2F* h_calojet_jettk_ifar_nsigmadxy[CALO_CATEGORIES];

  TH1F* h_jet_tks_pt[CATEGORIES];  
  TH1F* h_jet_tks_pt_rel[CATEGORIES];  
  TH1F* h_jet_tks_eta[CATEGORIES];  
  TH1F* h_jet_tks_eta_rel[CATEGORIES];  
  TH1F* h_jet_tks_dR[CATEGORIES];  
  TH1F* h_jet_tks_dxy[CATEGORIES];
  TH1F* h_jet_tks_dxyz[CATEGORIES];
  TH1F* h_jet_tks_nsigmadxy[CATEGORIES];  
  TH1F* h_jet_tks_nsigmadxyz[CATEGORIES];  
  TH1F* h_jet_sum_nsigmadxy[CATEGORIES];  
  TH1F* h_jet_sum_nsigmadxyz[CATEGORIES];  

  TH1F* h_jet_tk_nsigmadxy_avg[CATEGORIES];
  TH1F* h_jet_tk_nsigmadxy_med[CATEGORIES];
  TH1F* h_jet_tk_nsigmadxy_0[CATEGORIES];
  TH1F* h_jet_tk_nsigmadxy_1[CATEGORIES];

  TH1F* h_jet_tk_nsigmadxyz_avg[CATEGORIES];
  TH1F* h_jet_tk_nsigmadxyz_med[CATEGORIES];
  TH1F* h_jet_tk_nsigmadxyz_0[CATEGORIES];
  TH1F* h_jet_tk_nsigmadxyz_1[CATEGORIES];

  TH1F* h_jet_sumtk_pt_ratio[CATEGORIES];
  TH1F* h_jet_sumtk_dR[CATEGORIES];

  TH1F* h_online_btags;
  TH1F* h_online_calo_btags;
  TH1F* h_satisfies_online_tags;

};

MFVJetTksHistos::MFVJetTksHistos(const edm::ParameterSet& cfg)
  : mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
    vertex_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertex_src"))),
    rng(8675309),
    distribution(0.0f, 1.0f),
    gaussian(0.0, 0.004),
    offline_csv(cfg.getParameter<double>("offline_csv")),
    pt_thresh_shift(cfg.getParameter<double>("pt_thresh_shift")),
    pt_lo_for_tag_probe(cfg.getParameter<double>("pt_lo_for_tag_probe")),
    pt_hi_for_tag_probe(cfg.getParameter<double>("pt_hi_for_tag_probe")),
    tk_match_shift(cfg.getParameter<double>("tk_match_shift")),
    soft_tk_thresh(cfg.getParameter<double>("soft_tk_thresh")),
    plot_soft_tks(cfg.getParameter<bool>("plot_soft_tks")),
    plot_hard_tks(cfg.getParameter<bool>("plot_hard_tks")),
    require_triggers(cfg.getParameter<bool>("require_triggers")),
    veto_bjet_events(cfg.getParameter<bool>("veto_bjet_events")),
    require_tk_quality(cfg.getParameter<bool>("require_tk_quality")),
    require_gen_sumdbv(cfg.getParameter<bool>("require_gen_sumdbv")),
    require_two_good_leptons(cfg.getParameter<bool>("require_two_good_leptons")),
    do_tk_filt_refactor(cfg.getParameter<bool>("do_tk_filt_refactor")),
    get_hlt_btag_factors_pf(cfg.getParameter<bool>("get_hlt_btag_factors_pf")),
    get_hlt_btag_factors_calo(cfg.getParameter<bool>("get_hlt_btag_factors_calo")),
    get_hlt_btag_factors_calo_low(cfg.getParameter<bool>("get_hlt_btag_factors_calo_low")),
    force_hlt_btag_study(cfg.getParameter<bool>("force_hlt_btag_study")),
    require_match_to_hlt(cfg.getParameter<bool>("require_match_to_hlt")),
    require_early_b_filt(cfg.getParameter<bool>("require_early_b_filt")),
    apply_hlt_btagging(cfg.getParameter<bool>("apply_hlt_btagging")),
    apply_offline_dxy_res(cfg.getParameter<bool>("apply_offline_dxy_res")),
    calojet_category(cfg.getParameter<int>("calojet_category")),
    trigger_bit(cfg.getParameter<int>("trigger_bit"))

{
  edm::Service<TFileService> fs;

  h_w = fs->make<TH1F>("h_w", ";event weight;events/0.1", 100, 0, 10);
  h_calojet_nweird_ngood = fs->make<TH2F>("h_calojet_nweird_ngood", ";# of WeirdJets; # of GoodJets", 20, 0, 20, 20, 0, 20);
  h_calojet_sum_good_weird = fs->make<TH1F>("h_calojet_sum_good_weird", ";N(WeirdJets) + N(GoodJets); entries", 20, 0, 20);
 
  h_pfjet_pt_2d      = fs->make<TH2F>("h_pfjet_pt_2d",      ";p_{T} of offline pfjets w/ match @ HLT; p_{T} matching HLT jet", 200, 0, 800, 200, 0, 800);
  h_pfjet_pt_dpt     = fs->make<TH2F>("h_pfjet_pt_dpt",     ";p_{T} of offline pfjets w/ match @ HLT; p_{T}(offline) - p_{T}(online)", 200, 0, 800, 100, -100, 100); 
  h_pfjet_eta_deta   = fs->make<TH2F>("h_pfjet_eta_deta",   ";#eta of offline pfjets w/ match @ HLT; #eta(offline) - #eta(online)", 100, -2.5, 2.5, 40, -0.2, 0.2);
  h_pfjet_phi_dphi   = fs->make<TH2F>("h_pfjet_phi_dphi",   ";#phi of offline pfjets w/ match @ HLT; #phi(offline) - #eta(online)", 63, -M_PI, M_PI, 63, -M_PI, M_PI);
  h_pfjet_frac_dpt   = fs->make<TH1F>("h_pfjet_frac_dpt",   ";(p_{T}(offline) - p_{T}(HLT))/p_{T}(offline); entries", 120, -3.0, 3.0);
  h_pfjet_match_dR0  = fs->make<TH1F>("h_pfjet_match_dR0",  ";#DeltaR between offline pfjet and closest HLT match;entries",     100, 0, 2.0);
  h_pfjet_match_dR1  = fs->make<TH1F>("h_pfjet_match_dR1",  ";#DeltaR between offline pfjet and 2nd-closest HLT match;entries", 100, 0, 2.0);

  h_calojet_pt_2d      = fs->make<TH2F>("h_calojet_pt_2d",    ";p_{T} of offline calojets w/ match @ HLT; p_{T} matching HLT jet", 200, 0, 800, 200, 0, 800);
  h_calojet_pt_dpt     = fs->make<TH2F>("h_calojet_pt_dpt",   ";p_{T} of offline calojets w/ match @ HLT; p_{T}(offline) - p_{T}(online)", 200, 0, 800, 100, -100, 100);
  h_calojet_pt_pass_pt = fs->make<TH1F>("h_calojet_pt_pass_pt", ";p_{T} of offline calojets which pass HLT thresh (GeV); entries", 100, 0, 800);
  h_calojet_eta_deta = fs->make<TH2F>("h_calojet_eta_deta", ";#eta of offline calojets w/ match @ HLT; #eta(offline) - #eta(online)", 100, -2.5, 2.5, 40, -0.2, 0.2);
  h_calojet_phi_dphi = fs->make<TH2F>("h_calojet_phi_dphi", ";#phi of offline calojets w/ match @ HLT; #phi(offline) - #eta(online)", 63, -M_PI, M_PI, 63, -M_PI, M_PI);
  h_calojet_frac_dpt = fs->make<TH1F>("h_calojet_frac_dpt", ";(p_{T}(offline) - p_{T}(HLT))/p_{T}(offline); entries", 120, -3.0, 3.0);
  h_calojet_match_dR0  = fs->make<TH1F>("h_calojet_match_dR0",  ";#DeltaR between offline calojet and closest HLT match;entries",     100, 0, 2.0);
  h_calojet_match_dR1  = fs->make<TH1F>("h_calojet_match_dR1",  ";#DeltaR between offline calojet and 2nd-closest HLT match;entries", 100, 0, 2.0);
  h_calojet_pfjet_dR   = fs->make<TH1F>("h_calojet_pfjet_dR",   ";#DeltaR between offline calojet and closest offline pfjet; entries", 125, -0.5, 2.0);

  h_calojet_dxy_den0   = fs->make<TH1F>("h_calojet_dxy_den0", ";calojet d_{xy}(BS) (cm); entries", 250, 0, 0.5);
  h_calojet_dxy_den1   = fs->make<TH1F>("h_calojet_dxy_den1", ";calojet d_{xy}(BS) (cm); entries", 250, 0, 0.5);
  h_calojet_dxy_num0   = fs->make<TH1F>("h_calojet_dxy_num0", ";calojet d_{xy}(BS) (cm); entries", 250, 0, 0.5);
  h_calojet_dxy_num1   = fs->make<TH1F>("h_calojet_dxy_num1", ";calojet d_{xy}(BS) (cm); entries", 250, 0, 0.5);

  for (int i = 0; i < CATEGORIES; ++i) {
    TString bres = i == 4 ? TString("pass_hlt_lo_calo") : (i == 3 ? TString("pass_hlt_calo") : (i == 2 ? TString("fail_hlt") : (i == 1 ? TString("pass_hlt") : "pass_or_fail")));
    //TString bres = i == 5 ? TString("pass_hlt_calo") : (i == 4 ? TString("fail_off") : (i == 3 ? TString("pass_off") : (i == 2 ? TString("fail_hlt") : (i == 1 ? TString("pass_hlt") : "pass_or_fail"))));
    h_jet_pt[i] = fs->make<TH1F>(TString::Format("h_jet_pt_%s", bres.Data()), TString::Format(";p_{T} of jets that %s b-tag(GeV);events/10 GeV", bres.Data()), 200, 0, 800);
    h_jet_eta[i] = fs->make<TH1F>(TString::Format("h_jet_eta_%s", bres.Data()), TString::Format(";absv#eta of jets that %s b-tag;events/bin", bres.Data()), 120, 0, 2.5);
    h_jet_phi[i] = fs->make<TH1F>(TString::Format("h_jet_phi_%s", bres.Data()), TString::Format(";#phi of jets that %s b-tag;entries/bin", bres.Data()), 100, -3.1416, 3.1416);
    h_jet_dbv[i] = fs->make<TH1F>(TString::Format("h_jet_dbv_%s", bres.Data()), TString::Format(";d_{BV} of jets that %s b-tag;entries/bin", bres.Data()), 100, 0.0, 2.0);
    h_jet_ntks[i] = fs->make<TH1F>(TString::Format("h_jet_ntks_%s", bres.Data()), TString::Format(";#tks in jets that %s b-tag;entries/bin", bres.Data()), 40, 0, 40);
    h_jet_bdisc_deepflav[i] = fs->make<TH1F>(TString::Format("h_jet_bdisc_deepflav_%s", bres.Data()), TString::Format(";DeepJet of jets that %s b-tag;entries/bin", bres.Data()), 100, 0, 1.0);
    h_jet_bdisc_deepcsv[i] = fs->make<TH1F>(TString::Format("h_jet_bdisc_deepcsv_%s", bres.Data()), TString::Format(";DeepCSV of jets that %s b-tag;entries/bin", bres.Data()), 100, 0, 1.0);
    h_jet_bdisc_csv[i] = fs->make<TH1F>(TString::Format("h_jet_bdisc_csv_%s", bres.Data()), TString::Format(";CSV of jets that %s b-tag;entries/bin", bres.Data()), 100, 0, 1.0);

    h_jet_min_hlt_dR[i] = fs->make<TH1F>(TString::Format("h_jet_min_hlt_dR_%s", bres.Data()), TString::Format(";min #DeltaR between PF jets that %s and HLT jets", bres.Data()), 80, 0.0, 0.80);
    h_jet_min_hlt_calo_dR[i] = fs->make<TH1F>(TString::Format("h_jet_min_hlt_calo_dR_%s", bres.Data()), TString::Format(";min #DeltaR between PF jets that %s and HLT calojets;entries/bin", bres.Data()), 80, 0.0, 0.80);
    h_jet_hlt_calo_dpt[i] = fs->make<TH1F>(TString::Format("h_jet_hlt_calo_dpt_%s", bres.Data()), TString::Format(";(PFPT-CaloPT)/(PFPT) - %s ;entries/bin", bres.Data()), 100, -1, 1);
    h_jet_min_hlt_bjet_dR[i] = fs->make<TH1F>(TString::Format("h_jet_min_hlt_bjet_dR_%s", bres.Data()), TString::Format(";min #DeltaR between PF jets that %s and HLT bjets", bres.Data()), 80, 0.0, 0.80);
    h_jet_min_hlt_calo_bjet_dR[i] = fs->make<TH1F>(TString::Format("h_jet_min_hlt_calo_bjet_dR_%s", bres.Data()), TString::Format(";min #DeltaR between PF jets that %s and HLT calo bjets", bres.Data()), 80, 0.0, 0.80);
    h_jet_matches_hlt[i] = fs->make<TH1F>(TString::Format("h_jet_matches_hlt_%s", bres.Data()), TString::Format(";PF jet that %s matches to HLT jet?", bres.Data()), 2, -0.1, 1.1);
    h_jet_matches_hlt_bjet[i] = fs->make<TH1F>(TString::Format("h_jet_matches_hlt_bjet_%s", bres.Data()), TString::Format(";PF jet that %s matches to HLT bjet?", bres.Data()), 2, -0.1, 1.1);
    h_jet_matches_hlt_calo_bjet[i] = fs->make<TH1F>(TString::Format("h_jet_matches_hlt_calo_bjet_%s", bres.Data()), TString::Format(";PF jet that %s matches to HLT calo bjet?", bres.Data()), 2, -0.1, 1.1);

    h_jet_tks_pt[i] = fs->make<TH1F>(TString::Format("h_jet_tks_pt_%s", bres.Data()), TString::Format(";p_{T} of all tks in jets that %s b-tag (GeV);entries/bin", bres.Data()), 200, 0, 40);
    h_jet_tks_pt_rel[i] = fs->make<TH1F>(TString::Format("h_jet_tks_ptrel_%s", bres.Data()), TString::Format(";rel p_{T} of all tks in jets that %s b-tag (GeV);entries/bin", bres.Data()), 200, 0, 20);
    h_jet_tks_eta[i] = fs->make<TH1F>(TString::Format("h_jet_tks_eta_%s", bres.Data()), TString::Format(";abs #eta of all tks in jets that %s b-tag;entries/bin", bres.Data()), 100, 0, 4);
    h_jet_tks_eta_rel[i] = fs->make<TH1F>(TString::Format("h_jet_tks_etarel_%s", bres.Data()), TString::Format(";rel #eta of all tks in jets that %s b-tag;entries/bin", bres.Data()), 300, 0, 10);
    h_jet_tks_dR[i] = fs->make<TH1F>(TString::Format("h_jet_tks_dR_%s", bres.Data()), TString::Format(";dR between jet and all tks in jets - %s b-tag;entries/bin", bres.Data()), 100, 0, 0.6);
    h_jet_tks_dxy[i]  = fs->make<TH1F>(TString::Format("h_jet_tks_dxy_%s",  bres.Data()), TString::Format(";dxy of all tks in jets - %s b-tag (cm); entries/bin", bres.Data()), 250, 0, 0.5);
    h_jet_tks_dxyz[i] = fs->make<TH1F>(TString::Format("h_jet_tks_dxyz_%s", bres.Data()), TString::Format(";dxyz of all tks in jets - %s b-tag (cm); entries/bin", bres.Data()), 250, 0, 2.5);
    h_jet_tks_nsigmadxy[i] = fs->make<TH1F>(TString::Format("h_jet_tks_nsigmadxy_%s", bres.Data()), TString::Format("; n #sigma(dxy) of all tks in jets which %s b-tag;entries/bin", bres.Data()), 150, 0, 15);
    h_jet_tks_nsigmadxyz[i] = fs->make<TH1F>(TString::Format("h_jet_tks_nsigmadxyz_%s", bres.Data()), TString::Format("; n#sigma(dxyz) of tks in jets which %s b-tag;entries/bin", bres.Data()), 150, 0, 15);
    h_jet_sum_nsigmadxy[i] = fs->make<TH1F>(TString::Format("h_jet_sum_nsigmadxy_%s", bres.Data()), TString::Format(";#Sigma n#sigma(dxy) of tks in jets which %s b-tag;entries/bin", bres.Data()), 500, 0, 1500);
    h_jet_sum_nsigmadxyz[i] = fs->make<TH1F>(TString::Format("h_jet_sum_nsigmadxyz_%s", bres.Data()), TString::Format(";#Sigman#sigma(dxyz) of tks in jets which %s b-tag;entries/bin", bres.Data()), 500, 0, 1500);

    h_jet_tk_nsigmadxy_avg[i] = fs->make<TH1F>(TString::Format("h_jet_tk_nsigmadxy_avg_%s", bres.Data()), TString::Format("; avg n#sigma(dxy) of tks in jets which %s b-tag; entries/bin", bres.Data()), 300, 0, 30);
    h_jet_tk_nsigmadxy_med[i] = fs->make<TH1F>(TString::Format("h_jet_tk_nsigmadxy_med_%s", bres.Data()), TString::Format("; median n#sigma(dxy) of tks in jets which %s b-tag; entries/bin", bres.Data()), 300, 0, 30);
    h_jet_tk_nsigmadxy_0[i] = fs->make<TH1F>(TString::Format("h_jet_tk_nsigmadxy_0_%s", bres.Data()), TString::Format("; max n#sigma(dxy) of tks in jets which %s b-tag; entries/bin", bres.Data()), 300, 0, 150);
    h_jet_tk_nsigmadxy_1[i] = fs->make<TH1F>(TString::Format("h_jet_tk_nsigmadxy_1_%s", bres.Data()), TString::Format("; 2nd-leading n#sigma(dxy) of tks in jets which %s b-tag; entries/bin", bres.Data()), 300, 0, 150);

    h_jet_tk_nsigmadxyz_avg[i] = fs->make<TH1F>(TString::Format("h_jet_tk_nsigmadxyz_avg_%s", bres.Data()), TString::Format("; avg n#sigma(dxyz) of tks in jets which %s b-tag; entries/bin", bres.Data()), 300, 0, 30);
    h_jet_tk_nsigmadxyz_med[i] = fs->make<TH1F>(TString::Format("h_jet_tk_nsigmadxyz_med_%s", bres.Data()), TString::Format("; median n#sigma(dxyz) of tks in jets which %s b-tag; entries/bin", bres.Data()), 300, 0, 30);
    h_jet_tk_nsigmadxyz_0[i] = fs->make<TH1F>(TString::Format("h_jet_tk_nsigmadxyz_0_%s", bres.Data()), TString::Format("; max n#sigma(dxyz) of tks in jets which %s b-tag; entries/bin", bres.Data()), 300, 0, 150);
    h_jet_tk_nsigmadxyz_1[i] = fs->make<TH1F>(TString::Format("h_jet_tk_nsigmadxyz_1_%s", bres.Data()), TString::Format("; 2nd-leading n#sigma(dxyz) of tks in jets which %s b-tag; entries/bin", bres.Data()), 300, 0, 150);

    h_jet_sumtk_pt_ratio[i] = fs->make<TH1F>(TString::Format("h_jet_sumtk_pt_ratio_%s", bres.Data()), TString::Format(";pT(jet tracks) / pT(jet) - %s b-tag;entries/bin", bres.Data()), 100, 0, 4);
    h_jet_sumtk_dR[i] = fs->make<TH1F>(TString::Format("h_jet_sumtk_dR_%s", bres.Data()), TString::Format(";dR between jet and tks in jets - %s b-tag;entries/bin", bres.Data()), 100, 0, 0.6);
    
  }

  h_calojet_ntagged = fs->make<TH1F>("h_calojet_ntagged", "; # of tagged offline calojets; entries", 20, 0, 20);
  h_calojet_npasshlt = fs->make<TH1F>("h_calojet_npasshlt", "; # of offline calojets passing HLT; entries", 20, 0, 20);
  h_calojet_npassprompt = fs->make<TH1F>("h_calojet_npassprompt", "; # of offline calojets passing prompt veto; entries", 20, 0, 20);

  h_calo_jettk_dxy = fs->make<TH1F>("h_calo_jettk_dxy", ";dxy of pfjettks in calojets (cm);entries", 500, 0, 0.5);
  h_calo_jettk_dxy_ic_mult = fs->make<TH3F>("h_calo_jettk_dxy_ic_mult", ";nth-promptest track index;d_{xy};# of tracks per jet",
                                              15, 0, 15,
                                             500, 0, 0.5,
                                              15, 0, 15);   
  h_calo_jettk_dxyerr = fs->make<TH1F>("h_calo_jettk_dxyerr", ";#sigmadxy of pfjettks in calojets (cm);entries", 250, 0, 0.5);
  h_calo_jettk_nsigmadxy = fs->make<TH1F>("h_calo_jettk_nsigmadxy", ";n#sigmadxy of pfjettks in calojets;entries", 150, 0, 150);
  h_calo_jettk_pt = fs->make<TH1F>("h_calo_jettk_pt", ";p_{T} of pfjettks in calojets (GeV);entries", 100, 0, 50);
  h_calo_jettk_eta = fs->make<TH1F>("h_calo_jettk_eta", ";|#eta| of pfjettks in calojets;entries", 60, 0, 2.0);
  h_calo_jettk_phi = fs->make<TH1F>("h_calo_jettk_phi", ";#phi of pfjettks in calojets;entries", 63, -M_PI, M_PI);
  h_calo_jettk_deta = fs->make<TH1F>("h_calo_jettk_deta", ";|#Delta#eta| of pfjettks and parent calojet;entries", 50, 0, 0.5);
  h_calo_jettk_dphi = fs->make<TH1F>("h_calo_jettk_dphi", ";|#Delta#phi| of pfjettks and parent calojet;entries", 50, 0, 0.5);
  h_calo_jettk_deltaR = fs->make<TH1F>("h_calo_jettk_deltaR", ";#DeltaR of pfjettks and parent calojet; entries", 50, 0, 0.5);
  h_calo_jettk_deta_dxy = fs->make<TH2F>("h_calo_jettk_deta_dxy", ";|#Delta#eta| of pfjettks and parent calojet; dxy of pfjettks in calojet (cm)", 50, 0, 0.5, 250, 0, 0.5);
  h_calo_jettk_dphi_dxy = fs->make<TH2F>("h_calo_jettk_dphi_dxy", ";|#Delta#phi| of pfjettks and parent calojet; dxy of pfjettks in calojet (cm)", 50, 0, 0.5, 250, 0, 0.5);
  h_calo_jettk_deltaR_dxy = fs->make<TH2F>("h_calo_jettk_deltaR_dxy", ";#DeltaR of pfjettks and parent calojet; dxy of pfjettks in calojet (cm)", 50, 0, 0.5, 250, 0, 0.5);
  h_calo_jettk_npxhits = fs->make<TH1F>("h_calo_jettk_npxhits", ";npxhits of pfjettks in calojets;entries", 20, 0, 20);
  h_calo_jettk_nsthits = fs->make<TH1F>("h_calo_jettk_nsthits", ";nsthits of pfjettks in calojets;entries", 40, 0, 40);

  for (int i = 0; i < CALO_CATEGORIES; ++i) {
    TString bres = (i==3 ? TString("pass_c_btag") : (i == 2 ? TString("pass_disp") : (i == 1 ? TString("pass_prmpt") : "all")));
    h_calojet_pt[i] = fs->make<TH1F>(TString::Format("h_calojet_pt_%s", bres.Data()), TString::Format(";p_{T} of calojets that %s (GeV);entries/bin", bres.Data()), 100, 0, 800);
    h_calojet_pt_raw[i] = fs->make<TH1F>(TString::Format("h_calojet_pt_raw_%s", bres.Data()), TString::Format(";'raw' p_{T} of calojets that %s (GeV);entries/bin", bres.Data()), 100, 0, 800);
    h_calojet_eta[i] = fs->make<TH1F>(TString::Format("h_calojet_eta_%s", bres.Data()), TString::Format(";absv#eta of calojets that %s;entries/bin", bres.Data()), 60, 0, 2.5);
    h_calojet_phi[i] = fs->make<TH1F>(TString::Format("h_calojet_phi_%s", bres.Data()), TString::Format(";#phi of calojets that %s;entries/bin", bres.Data()), 63, -M_PI, M_PI);
    h_calojet_dbv[i] = fs->make<TH1F>(TString::Format("h_calojet_dbv_%s", bres.Data()), TString::Format(";best guess d_{BV} of calojets that %s; entries/bin", bres.Data()), 50, 0, 2.0);
    h_calojet_dxy[i] = fs->make<TH1F>(TString::Format("h_calojet_dxy_%s", bres.Data()), TString::Format(";best guess d_{xy} of calojets that %s; entries/bin", bres.Data()), 50, 0, 2.0);
    h_calojet_pf_dR[i] = fs->make<TH1F>(TString::Format("h_calojet_pf_dR_%s", bres.Data()), TString::Format(";#DeltaR (calojet, pfjet) of calojets that %s; entries/bin", bres.Data()), 40, 0, 0.4);
    h_calojet_pf_next_dR[i] = fs->make<TH1F>(TString::Format("h_calojet_pf_next_dR_%s", bres.Data()), TString::Format(";#DeltaR (calojet, 2nd-closest pfjet) of calojets that %s; entries/bin", bres.Data()), 60, 0, 0.6);
    h_calojet_csv[i] = fs->make<TH1F>(TString::Format("h_calojet_csv_%s", bres.Data()), TString::Format(";CSV of calojets that %s;entries/bin", bres.Data()), 100, 0.0, 1.0);
    h_calojet_pudisc[i] = fs->make<TH1F>(TString::Format("h_calojet_pudisc_%s", bres.Data()), TString::Format(";pudisc of calojets that %s;entries/bin", bres.Data()), 200, -1.0, 1.0);
    h_calojet_filtscore[i] = fs->make<TH1F>(TString::Format("h_calojet_filtscore_%s", bres.Data()), TString::Format(";filtscore of calojets that %s; entries/bin", bres.Data()), 4, 0, 4);
    h_calojet_ntks[i] = fs->make<TH1F>(TString::Format("h_calojet_ntks_%s", bres.Data()), TString::Format(";ntks in calojets that %s ;entries/bin", bres.Data()), 40, 0, 40);
    h_calojet_njettks[i] = fs->make<TH1F>(TString::Format("h_calojet_njettks_%s", bres.Data()), TString::Format(";n(pfjet tks) in calojets that %s ;entries/bin", bres.Data()), 40, 0, 40);
    h_calojet_nprompttks[i] = fs->make<TH1F>(TString::Format("h_calojet_nprompttks_%s", bres.Data()), TString::Format(";n(prompt pfjet tks) in calojets that %s ;entries/bin", bres.Data()), 40, 0, 40);
    h_calojet_ndisptks[i] = fs->make<TH1F>(TString::Format("h_calojet_ndisptks_%s", bres.Data()), TString::Format(";n(disp pfjet tks) in calojets that %s ;entries/bin", bres.Data()), 40, 0, 40);

    h_calojet_jettk_dxy[i] = fs->make<TH1F>(TString::Format("h_calojet_jettk_dxy_%s", bres.Data()), TString::Format(";dxy of pfjettks in calojets that %s (cm); entires/bin", bres.Data()), 250, 0, 0.5);
    h_calojet_jettk_iclose_dxy[i] = fs->make<TH2F>(TString::Format("h_calojet_jettk_iclose_dxy_%s", bres.Data()), TString::Format(";nth-closest tk index;dxy of pfjettks in calojets that %s (cm);", bres.Data()), 15, 0, 15, 250, 0, 0.5);
    h_calojet_jettk_iclose_pt[i] = fs->make<TH2F>(TString::Format("h_calojet_jettk_iclose_pt_%s", bres.Data()), TString::Format(";nth-closest tk index;pt of pfjettks in calojets that %s (GeV);", bres.Data()), 15, 0, 15, 100, 0, 50.0);
    h_calojet_jettk_iclose_eta[i] = fs->make<TH2F>(TString::Format("h_calojet_jettk_iclose_eta_%s", bres.Data()), TString::Format(";nth-closest tk index;|#eta| of pfjettks in calojets that %s;", bres.Data()), 15, 0, 15, 60, 0, 2.0);
    h_calojet_jettk_iclose_dR[i] = fs->make<TH2F>(TString::Format("h_calojet_jettk_iclose_dR_%s", bres.Data()), TString::Format(";nth-closest tk index;#DeltaR(pfjettks, parent calojets) that %s;", bres.Data()), 15, 0, 15, 45, 0, 0.45);
    h_calojet_jettk_iclose_npxhits[i] = fs->make<TH2F>(TString::Format("h_calojet_jettk_iclose_npxhits_%s", bres.Data()), TString::Format(";nth-closest tk index;npxhits of pfjettks in calojets that  %s;", bres.Data()), 15, 0, 15, 20, 0, 20);
    h_calojet_jettk_iclose_nsthits[i] = fs->make<TH2F>(TString::Format("h_calojet_jettk_iclose_nsthits_%s", bres.Data()), TString::Format(";nth-closest tk index;nsthits of pfjettks in calojets that %s;", bres.Data()), 15, 0, 15, 40, 0, 40);
    h_calojet_jettk_ifar_dxy[i] = fs->make<TH2F>(TString::Format("h_calojet_jettk_ifar_dxy_%s", bres.Data()), TString::Format(";nth-farthest tk index;dxy of pfjettks in calojets that %s (cm);", bres.Data()), 15, 0, 15, 250, 0, 0.5);

    h_calojet_jettk_nsigmadxy[i] = fs->make<TH1F>(TString::Format("h_calojet_jettk_nsigmadxy_%s", bres.Data()), TString::Format(";n#sigmadxy of pfjettks in calojets that %s (cm); entries/bin", bres.Data()), 150, 0, 150);
    h_calojet_jettk_iclose_nsigmadxy[i] = fs->make<TH2F>(TString::Format("h_calojet_jettk_iclose_nsigmadxy_%s", bres.Data()), TString::Format(";nth-closest tk index;n#sigmadxy of pfjettks in calojets that %s (cm);", bres.Data()), 15, 0, 15, 150, 0, 150);
    h_calojet_jettk_ifar_nsigmadxy[i] = fs->make<TH2F>(TString::Format("h_calojet_jettk_ifar_nsigmadxy_%s", bres.Data()), TString::Format(";nth-farthest tk index;n#sigmadxy of pfjettks in calojets that %s (cm);", bres.Data()), 15, 0, 15, 150, 0, 150);

  }

  h_online_btags = fs->make<TH1F>("h_online_btags", ";# of offline jets tagged @ HLT; entries", 15, 0, 15);
  h_online_calo_btags = fs->make<TH1F>("h_online_calo_btags", ";# of offline jets tagged @ HLT w/ online p_{T} > 80GeV; entries", 15, 0, 15);
  h_satisfies_online_tags = fs->make<TH1F>("h_satisfies_online_tags", ";Event has enough online btags?; entries", 2, -0.01, 1.01);
}

struct Track_Helper {
    float dr     = -9.9;
    float dz     = -9.9;
    float drerr  = -9.9;
    float drsig  = -9.9;
    float dzerr  = -9.9;
    float drz    = -9.9;
    float drzerr = -9.9;

    float pt     = -9.9;
    float eta    = -9.9;
    float phi    = -9.9;
    float deltaR = -9.9;

    int npxhits = -9;
    int nsthits = -9;
};

void MFVJetTksHistos::analyze(const edm::Event& event, const edm::EventSetup&) {
      
    edm::Handle<MFVEvent> mevent;
    event.getByToken(mevent_token, mevent);
  
    edm::Handle<double> weight;
    event.getByToken(weight_token, weight);

    edm::Handle<MFVVertexAuxCollection> auxes;
    event.getByToken(vertex_token, auxes);

    // Get a shorthand for the current year
    int year = int(MFVNEUTRALINO_YEAR);

    double gen_sumdbv = 0.0;
    for (int igenv = 0; igenv < 2; ++igenv) {
        double genx = mevent->gen_lsp_decay[igenv*3+0];
        double geny = mevent->gen_lsp_decay[igenv*3+1];
        double genz = mevent->gen_lsp_decay[igenv*3+2];
        double genbs2ddist = mevent->mag(genx - mevent->bsx_at_z(genz), geny - mevent->bsy_at_z(genz));
        gen_sumdbv += genbs2ddist;  
    }
    if (require_gen_sumdbv and gen_sumdbv < 0.7) { return; }

  
    const double w = *weight;
    int  calojet_ntagged = 0;
    int  calojet_ngood   = 0;
    int  calojet_nweird  = 0;
    int  calojet_npass_hlt    = 0;
    int  calojet_npass_prompt = 0;
    int n_online_btags      = 0;
    int n_online_calo_btags    = 0;
    int n_online_calo_lo_btags = 0;
    double online_pfht    = 0.0;
    double online_caloht  = 0.0;
    double offline_pfht   = 0.0;
    double offline_caloht = 0.0;
    h_w->Fill(w);
  

    if ((require_triggers) and not (mevent->pass_hlt(trigger_bit))) { return; }

    // Calculate on/off caloht
    for (int i = 0, ie=mevent->calo_jet_pt.size(); i < ie; ++i) {
        if ((mevent->calo_jet_pt[i] > 30.0) and (fabs(mevent->calo_jet_eta[i]) < 2.5)) offline_caloht += mevent->calo_jet_pt[i];
    }

    if (require_two_good_leptons) {
        bool has_nice_muon = false;
        bool has_nice_ele  = false;
        for (size_t ilep = 0; ilep < mevent->nlep(); ++ilep) {
            if (mevent->is_electron(ilep)) {
                float ele_eta = mevent->lep_eta[ilep]; 
                float ele_pt  = mevent->lep_pt(ilep);
                if (fabs(ele_eta) > 2.4 or ele_pt < 30.0) continue;
                else if (fabs(ele_eta) < 1.479) {
                    if (mevent->lep_iso[ilep] < (0.0287+(0.506/ele_pt))) {
                        has_nice_ele = true;
                    }
                }
                else {  
                    if (mevent->lep_iso[ilep] < (0.0445+(0.963/ele_pt))) {
                        has_nice_ele = true;
                    }
                }
            }
            else if (mevent->lep_iso[ilep] < 0.15 and mevent->lep_pt(ilep) > 30.0 and fabs(mevent->lep_eta[ilep]) < 2.4) {
                has_nice_muon = true;
            }
        }

        if ((not has_nice_muon) or (not has_nice_ele)) return;
    }


    std::vector<int> di_kine_filter_bits;
    std::vector<int> tri_kine_filter_bits;
    std::vector<int> tri_symm_kine_filter_bits;
    std::vector<int> tri_skew_kine_filter_bits;

    if (year == 20161 or year == 20162) {
        di_kine_filter_bits = { mfv::b_hltDoubleJetsC100, mfv::b_hltDoublePFJetsC100, mfv::b_hltDoublePFJetsC100MaxDeta1p6 };

        tri_symm_kine_filter_bits = { mfv::b_hltQuadCentralJet45, mfv::b_hltQuadPFCentralJetLooseID45 };
        tri_skew_kine_filter_bits = { mfv::b_hltQuadCentralJet30, mfv::b_hltDoubleCentralJet90, mfv::b_hltQuadPFCentralJetLooseID30, mfv::b_hltDoublePFCentralJetLooseID90 };
    }


    if (year == 2017) {
        di_kine_filter_bits  =     { mfv::b_hltDoubleCaloBJets100eta2p3, mfv::b_hltDoublePFJets100Eta2p3, mfv::b_hltDoublePFJets100Eta2p3MaxDeta1p6 };

        if (require_early_b_filt) {
            tri_kine_filter_bits = { mfv::b_hltQuadCentralJet30, mfv::b_hltCaloQuadJet30HT300, mfv::b_hltBTagCaloCSVp05Double,
                                     mfv::b_hltPFCentralJetLooseIDQuad30, mfv::b_hlt1PFCentralJetLooseID75, mfv::b_hlt2PFCentralJetLooseID60,
                                     mfv::b_hlt3PFCentralJetLooseID45, mfv::b_hlt4PFCentralJetLooseID40,
                                     mfv::b_hltPFCentralJetsLooseIDQuad30HT300 };
        }

        else {
            tri_kine_filter_bits = { mfv::b_hltQuadCentralJet30, mfv::b_hltCaloQuadJet30HT300,
                                     mfv::b_hltPFCentralJetLooseIDQuad30, mfv::b_hlt1PFCentralJetLooseID75, mfv::b_hlt2PFCentralJetLooseID60,
                                     mfv::b_hlt3PFCentralJetLooseID45, mfv::b_hlt4PFCentralJetLooseID40,
                                     mfv::b_hltPFCentralJetsLooseIDQuad30HT300 };
        }
    }

    if (year == 2018) {
        di_kine_filter_bits  = { mfv::b_hltDoubleCaloBJets100eta2p3, mfv::b_hltDoublePFJets116Eta2p3, mfv::b_hltDoublePFJets116Eta2p3MaxDeta1p6 };

        if (require_early_b_filt) {
            tri_kine_filter_bits = { mfv::b_hltQuadCentralJet30, mfv::b_hltCaloQuadJet30HT320,
                                mfv::b_hltBTagCaloDeepCSVp17Double, mfv::b_hltPFCentralJetLooseIDQuad30,
                                mfv::b_hlt1PFCentralJetLooseID75, mfv::b_hlt2PFCentralJetLooseID60,
                                mfv::b_hlt3PFCentralJetLooseID45, mfv::b_hlt4PFCentralJetLooseID40,
                                mfv::b_hltPFCentralJetsLooseIDQuad30HT330 };
        }

        else {
            tri_kine_filter_bits = { mfv::b_hltQuadCentralJet30, mfv::b_hltCaloQuadJet30HT320,
                            mfv::b_hltPFCentralJetLooseIDQuad30,
                            mfv::b_hlt1PFCentralJetLooseID75, mfv::b_hlt2PFCentralJetLooseID60,
                            mfv::b_hlt3PFCentralJetLooseID45, mfv::b_hlt4PFCentralJetLooseID40,
                            mfv::b_hltPFCentralJetsLooseIDQuad30HT330 };
        }
    }


    // Get closest online/offline pfjet match and calculate on/off pfht
    for (int i = 0; i < mevent->njets(); ++i) {
        double closest_dR = 0.2;
        double second_dR  = 11.11;
        int closest_idx = -9;

        if ((mevent->jet_pt[i] > 30.0) and (fabs(mevent->jet_eta[i]) < 2.5)) offline_pfht += mevent->jet_pt[i];

        for (int j=0, je=mevent->hlt_pf_jet_pt.size(); j<je; ++j) {
            if ((i == 0) and (mevent->hlt_pf_jet_pt[j] > 30.0) and (fabs(mevent->hlt_pf_jet_eta[j]) < 2.5)) online_pfht += mevent->hlt_pf_jet_pt[i];
            double temp_dR = reco::deltaR(mevent->jet_eta[i], mevent->jet_phi[i], mevent->hlt_pf_jet_eta[j], mevent->hlt_pf_jet_phi[j]);
            if (temp_dR < closest_dR) {
                second_dR   = closest_dR;
                closest_dR  = temp_dR;
                closest_idx = j;
            }
        }
        if (closest_idx == -9) continue;
        h_pfjet_match_dR0->Fill(closest_dR, w);
        h_pfjet_match_dR1->Fill(second_dR, w);
        h_pfjet_frac_dpt->Fill((mevent->jet_pt[i]-mevent->hlt_pf_jet_pt[closest_idx])/mevent->jet_pt[i], w);
        h_pfjet_pt_2d->Fill(mevent->jet_pt[i], mevent->hlt_pf_jet_pt[closest_idx], w); 
        h_pfjet_pt_dpt->Fill(mevent->jet_pt[i], mevent->jet_pt[i]-mevent->hlt_pf_jet_pt[closest_idx], w); 
        h_pfjet_eta_deta->Fill(mevent->jet_eta[i], mevent->jet_eta[i]-mevent->hlt_pf_jet_eta[closest_idx], w); 
        h_pfjet_phi_dphi->Fill(mevent->jet_phi[i], mevent->jet_phi[i]-mevent->hlt_pf_jet_phi[closest_idx], w); 
    }

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////   END INITIAL PFJET STUFF
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////   START CALOJET STUFF


    float calo_pt_hlt_thresh = (trigger_bit == 19 ? 60.0 : 40.0);
    // Get closest online/offline calojet match and calculate on/off caloht
    for (int i = 0, ie=mevent->calo_jet_pt.size(); i < ie; ++i) {
        double closest_dR = 10.00;
        double second_dR  = 11.11;
        int closest_idx = -9;

        //if ((mevent->calo_jet_pt[i] > 40.0) and (fabs(mevent->calo_jet_eta[i]) < 2.5)) offline_caloht += mevent->calo_jet_pt[i];

        for (int j=0, je=mevent->hlt_calo_jet_pt.size(); j<je; ++j) {
            if ((i == 0) and (mevent->hlt_calo_jet_pt[j] > 40.0) and (fabs(mevent->hlt_calo_jet_eta[j]) < 2.5)) online_caloht += mevent->hlt_calo_jet_pt[i];
            double temp_dR = reco::deltaR(mevent->calo_jet_eta[i], mevent->calo_jet_phi[i], mevent->hlt_calo_jet_eta[j], mevent->hlt_calo_jet_phi[j]);
            if (temp_dR < closest_dR) {
                second_dR   = closest_dR;
                closest_dR  = temp_dR;
                closest_idx = j;
            }
            else if (temp_dR < second_dR) {
                second_dR = temp_dR;
            }
        }
        
        if (closest_dR > 0.2 or closest_idx == -9 or fabs(mevent->calo_jet_eta[i]) > 2.0) continue;
        //if (closest_idx == -9 or fabs(mevent->calo_jet_eta[i]) > 2.0) continue;
        h_calojet_match_dR0->Fill(closest_dR, w);
        h_calojet_match_dR1->Fill(second_dR, w);
        h_calojet_frac_dpt->Fill((mevent->calo_jet_pt[i]-mevent->hlt_calo_jet_pt[closest_idx])/mevent->calo_jet_pt[i], w);
        h_calojet_pt_2d->Fill(mevent->calo_jet_pt[i], mevent->hlt_calo_jet_pt[closest_idx], w); 
        h_calojet_pt_dpt->Fill(mevent->calo_jet_pt[i], mevent->calo_jet_pt[i]-mevent->hlt_calo_jet_pt[closest_idx], w); 
        h_calojet_eta_deta->Fill(mevent->calo_jet_eta[i], mevent->calo_jet_eta[i]-mevent->hlt_calo_jet_eta[closest_idx], w); 
        h_calojet_phi_dphi->Fill(mevent->calo_jet_phi[i], mevent->calo_jet_phi[i]-mevent->hlt_calo_jet_phi[closest_idx], w); 

        if (mevent->hlt_calo_jet_pt[closest_idx] > calo_pt_hlt_thresh) h_calojet_pt_pass_pt->Fill(mevent->calo_jet_pt[i], w); 

    }

    // Start doing some calojet stuff
    for (int i = 0, ie=mevent->calo_jet_pt.size(); i < ie; ++i) {
        std::vector<Track_Helper> calo_trackhelpers;
        std::vector<int> fill_calo_hists;
        std::vector<float> jettk_dxys;
        std::vector<float> jettk_nsigmadxys;
        float closest_pudisc = 0.0;
        float closest_csv = -0.2;
        float closest_jec_factor = 1.0;
        float pt_thresh = trigger_bit==19 ? 60.0 : 40.0;
        float calojet_dxy = -1.0;

        double closest_dR = 9.9;
        double next_dR    = 10.9;
        int    closest_j  = -10;
        int    calojet_njettks = 0;
        int    calojet_njettks_prompt = 0;
        int    calojet_njettks_dispd = 0;
        bool has_match = false;
        bool good_jet  = ((mevent->calo_jet_pt[i] > pt_thresh) and (fabs(mevent->calo_jet_eta[i]) < 2.0));

        if (fabs(mevent->calo_jet_eta[i]) > 2.0) continue;

        // Get closest match between offline calojet and offline pfjet
        for (int j=0, je=mevent->jet_pt.size(); j<je; ++j) {
            double temp_dR = reco::deltaR(mevent->calo_jet_eta[i], mevent->calo_jet_phi[i], mevent->jet_eta[j], mevent->jet_phi[j]);
            if (temp_dR < closest_dR) {
                next_dR    = closest_dR;
                closest_dR = temp_dR;
                closest_j  = j;
                has_match = true;
                closest_pudisc = mevent->jet_pt[j] < 50.0 ? mevent->jet_pudisc[j] : 1.1;
                closest_csv    = mevent->jet_bdisc_csv[j];
                closest_jec_factor = mevent->jet_raw_pt[j] / mevent->jet_pt[j];
            }
            else if (temp_dR < next_dR) {
                next_dR = temp_dR;
            }
        }
        if (good_jet) { h_calojet_pfjet_dR->Fill(has_match ? closest_dR : -0.5, w); }

        // Do some kludge-y filter stuff. First, only run on events/jets that look good enough
        bool   matches_promptpass_cjet = false;
        bool   matches_disp_cjet = false;
        bool   matches_hlt_calo_bjet = false;
        //if (not good_jet) continue;

        // Get the number of decent jet tracks within dR < 0.4
        for (size_t itk = 0; itk < mevent->n_jet_tracks_all(); itk++) {
            if (mevent->jet_track_which_jet[itk] != closest_j) continue;
            double this_tk_nsigmadxy = fabs(mevent->jet_track_dxy[itk]/mevent->jet_track_dxy_err[itk]);
            if (fabs(mevent->jet_track_qpt[itk]) < 1.0 or (require_tk_quality and (mevent->jet_track_npxhits(itk) < 2 or mevent->jet_track_nhits(itk) < 8))) continue;

            // Test bit to vary the matching criteria on the softest/hardest tracks
            bool tk_pt_testbit = fabs(mevent->jet_track_qpt[itk]) < soft_tk_thresh;

            double this_dR = reco::deltaR(mevent->calo_jet_eta[i], mevent->calo_jet_phi[i], mevent->jet_track_eta[itk], mevent->jet_track_phi[itk]);
            if (this_dR < (0.4 - (tk_match_shift * tk_pt_testbit))) {

                calojet_njettks++;
                double abs_dxy = fabs(mevent->jet_track_dxy[itk]);
                jettk_dxys.push_back(abs_dxy);
                jettk_nsigmadxys.push_back(this_tk_nsigmadxy);

                if (apply_offline_dxy_res) abs_dxy += gaussian(rng);
                if (abs_dxy < 0.10) calojet_njettks_prompt++;
                if (abs_dxy > 0.05 and this_tk_nsigmadxy > 5.0) calojet_njettks_dispd++;

                Track_Helper tmp_track_helper;
                tmp_track_helper.dr    = abs_dxy;
                tmp_track_helper.drerr = fabs(mevent->jet_track_dxy_err[itk]);
                tmp_track_helper.drsig = this_tk_nsigmadxy;
                tmp_track_helper.pt    = fabs(mevent->jet_track_qpt[itk]);
                tmp_track_helper.eta   = mevent->jet_track_eta[itk];
                tmp_track_helper.phi   = mevent->jet_track_phi[itk];
                tmp_track_helper.deltaR = this_dR;
                tmp_track_helper.npxhits = mevent->jet_track_npxhits(itk);
                tmp_track_helper.nsthits = mevent->jet_track_nhits(itk);

                calo_trackhelpers.push_back(tmp_track_helper);
            }
        }

        // See if this calojet matches to one which passes the prompt track tag (Low-HT trigger in all three years)
        if (trigger_bit != 19) {
            for (int j=0, je=mevent->hlt_calo_jet_lowpt_fewprompt_pt.size(); j < je; j++) {
                double test_jet_eta = mevent->hlt_calo_jet_lowpt_fewprompt_eta[j];
                double test_jet_phi = mevent->hlt_calo_jet_lowpt_fewprompt_phi[j];
                if (reco::deltaR(mevent->calo_jet_eta[i], mevent->calo_jet_phi[i], test_jet_eta, test_jet_phi) < 0.20) {
                    matches_promptpass_cjet = true;
                    break;
                }
            }
        }

        // See if this calojet matches to one which passes the prompt track tag (High-HT trigger)
        if (trigger_bit == 19) {
            for (int j=0, je=mevent->hlt_calo_jet_midpt_fewprompt_pt.size(); j < je; j++) {
                double test_jet_eta = mevent->hlt_calo_jet_midpt_fewprompt_eta[j];
                double test_jet_phi = mevent->hlt_calo_jet_midpt_fewprompt_phi[j];
                if (reco::deltaR(mevent->calo_jet_eta[i], mevent->calo_jet_phi[i], test_jet_eta, test_jet_phi) < 0.20) {
                    matches_promptpass_cjet = true;
                    break;
                }
            }
        } 

        // See if this calojet matches to one which passes the displaced track tag
        else {
            for (int j=0, je=mevent->hlt_calo_jet_lowpt_wdisptks_pt.size(); j < je; j++) {
                double test_jet_eta = mevent->hlt_calo_jet_lowpt_wdisptks_eta[j];
                double test_jet_phi = mevent->hlt_calo_jet_lowpt_wdisptks_phi[j];
                if (reco::deltaR(mevent->calo_jet_eta[i], mevent->calo_jet_phi[i], test_jet_eta, test_jet_phi) < 0.20) {
                  matches_disp_cjet = true;
                  break;
                }
            }
        }

        // See if this calojet matches to one which satisfies the HLT calo bjet filter
        for (int j=0, je=mevent->hlt_calo_b_jet_pt.size(); j < je; j++) {
            double test_jet_eta = mevent->hlt_calo_b_jet_eta[j];
            double test_jet_phi = mevent->hlt_calo_b_jet_phi[j];
            if (reco::deltaR(mevent->calo_jet_eta[i], mevent->calo_jet_phi[i], test_jet_eta, test_jet_phi) < 0.20) {
              matches_hlt_calo_bjet = true;
              break;
            }
        }

        //Require that there is at least one other jet in the event which passes a med btag
        bool has_tag_jet_buddy = false;
        for (int j=0; j < mevent->njets(); ++j) {
            // Make sure this PF jet isn't the same as the CaloJet we're looking at
            if (reco::deltaR(mevent->calo_jet_eta[i], mevent->calo_jet_phi[i], mevent->nth_jet_eta(j), mevent->nth_jet_phi(j)) < 0.4) continue;

            if (mevent->is_btagged(j, 1) and mevent->nth_jet_pt(j) > 30.0 and fabs(mevent->nth_jet_eta(j)) < 2.4) {  // the "1" in is_btagged stands for med.
                has_tag_jet_buddy = true;
                break;  
            }
        }
        if (not has_tag_jet_buddy) continue;
        
        float rand_x = distribution(rng);
        // Refactor survival >_<
        if (do_tk_filt_refactor) {
          //matches_promptpass_cjet = refactor_survival(calojet_njettks_prompt, matches_promptpass_cjet, rand_x);
          matches_promptpass_cjet = jmt::UncertTools::refactor_prompt_tk_eff(calojet_njettks_prompt, matches_promptpass_cjet, rand_x, year);
        }

        // sort vectors by increasing (nsigma)dxy
        jmt::sortVector(jettk_dxys);
        jmt::sortVector(jettk_nsigmadxys);

        // same here, but it's a bit different
        std::sort(calo_trackhelpers.begin(), calo_trackhelpers.end(), [](Track_Helper const &a, Track_Helper const &b) -> bool{ return a.dr < b.dr; });

        // Helper bools
        bool pass_prompt_req   = jettk_dxys.size() >= 3 ? (jettk_dxys[2] > 0.1) : true;
        bool pass_alt_disp_req = calojet_njettks_dispd >= 1;
        bool pass_pt_req       = fabs(mevent->calo_jet_eta[i]) < 2.0 and mevent->calo_jet_pt[i] > (pt_thresh - pt_thresh_shift);

        // Main jet-tagging bools
        bool pass_offline_tagreqs = ((trigger_bit == 18 and pass_prompt_req and pass_alt_disp_req and pass_pt_req) or (trigger_bit == 19 and pass_prompt_req and pass_pt_req));
        bool pass_online_tagreqs  = ((trigger_bit == 18 and matches_disp_cjet and matches_promptpass_cjet) or (trigger_bit == 19 and matches_promptpass_cjet));
        bool pass_category        = true;
        bool pass_pure_region     = mevent->calo_jet_pt[i] > 50.0 ;

        if (not pass_pure_region) continue;
       
        // 0: passes no offline filter bits      1: passes tk-based bits     2: passes pT-based bits     3: passes all bits
        int calojet_filtscore = 0 + (1 * (trigger_bit == 18 and pass_prompt_req and pass_alt_disp_req)) + (1 * (trigger_bit == 19 and pass_prompt_req)) + (2 * pass_pt_req);

        if (matches_promptpass_cjet)                           calojet_npass_prompt++;
        if (pass_online_tagreqs)                               calojet_npass_hlt++;
        if (pass_offline_tagreqs)                              calojet_ntagged++;
        if (pass_offline_tagreqs and pass_online_tagreqs)      calojet_ngood++;
        if (pass_online_tagreqs  and not pass_offline_tagreqs) calojet_nweird++;

        switch(calojet_category) {
            case 1:   // Good Jets
                if (!pass_online_tagreqs || !pass_offline_tagreqs) pass_category = false;
                break;
            case 2:   // Weird Jets (false negatives)
                if (!pass_online_tagreqs || pass_offline_tagreqs) pass_category = false;
                break;
            case 3:   // Bad Jets
                if (pass_online_tagreqs || pass_offline_tagreqs) pass_category = false;
                break;
            case 4:   // "Other" Weird Jets (false positives)
                if (pass_online_tagreqs || !pass_offline_tagreqs) pass_category = false;
                break;
        }

        if (not pass_category) continue;
        
        fill_calo_hists.push_back(ALL);
        if (matches_hlt_calo_bjet)                         { fill_calo_hists.push_back(PASS_HLT_BTAG); }
        if (matches_promptpass_cjet)                       { fill_calo_hists.push_back(PASS_CALO_PROMPT); }
        if (matches_promptpass_cjet and matches_disp_cjet) { fill_calo_hists.push_back(PASS_CALO_DISP); }

        for (auto n_hist : fill_calo_hists) {
             h_calojet_pt[n_hist]->Fill(mevent->calo_jet_pt[i], w);
             h_calojet_pt_raw[n_hist]->Fill(closest_jec_factor * mevent->calo_jet_pt[i], w);
             h_calojet_eta[n_hist]->Fill(fabs(mevent->calo_jet_eta[i]), w);
             h_calojet_phi[n_hist]->Fill(mevent->calo_jet_phi[i], w);
             h_calojet_dxy[n_hist]->Fill(calojet_dxy, w);
             h_calojet_csv[n_hist]->Fill(closest_csv, w);
             h_calojet_pf_dR[n_hist]->Fill(closest_dR, w);
             h_calojet_pf_next_dR[n_hist]->Fill(next_dR, w);
             h_calojet_ntks[n_hist]->Fill(closest_j >= 0 ? (int)(mevent->n_jet_tracks(closest_j)) : -2, w);
             h_calojet_njettks[n_hist]->Fill(calojet_njettks, w);
             h_calojet_nprompttks[n_hist]->Fill(calojet_njettks_prompt, w);
             h_calojet_ndisptks[n_hist]->Fill(calojet_njettks_dispd, w);

             if (mevent->calo_jet_pt[i] < pt_thresh) h_calojet_pudisc[n_hist]->Fill(closest_pudisc, w);

             h_calojet_filtscore[n_hist]->Fill(calojet_filtscore, w);

             for (int ib=0, ibe=jettk_dxys.size(); ib < ibe; ib++) {
                  h_calojet_jettk_dxy[n_hist]->Fill(jettk_dxys[ib], w);
                  h_calojet_jettk_iclose_dxy[n_hist]->Fill(ib, jettk_dxys[ib], w);
                  h_calojet_jettk_iclose_pt[n_hist]->Fill(ib,  calo_trackhelpers[ib].pt, w);
                  h_calojet_jettk_iclose_eta[n_hist]->Fill(ib, calo_trackhelpers[ib].eta, w);
                  h_calojet_jettk_iclose_dR[n_hist]->Fill(ib, calo_trackhelpers[ib].deltaR, w);
                  h_calojet_jettk_iclose_npxhits[n_hist]->Fill(ib, calo_trackhelpers[ib].npxhits, w);
                  h_calojet_jettk_iclose_nsthits[n_hist]->Fill(ib, calo_trackhelpers[ib].nsthits, w);
             }
             for (int ib=0, ibe=jettk_nsigmadxys.size(); ib < ibe; ib++) {
                  h_calojet_jettk_nsigmadxy[n_hist]->Fill(jettk_nsigmadxys[ib], w);
                  h_calojet_jettk_iclose_nsigmadxy[n_hist]->Fill(ib, jettk_nsigmadxys[ib], w);
             }
        }


        // Fill this TH3F... rip in peace
        for (int ib=0, ibe=jettk_dxys.size(); ib < ibe; ib++) {
            h_calo_jettk_dxy_ic_mult->Fill(ib, jettk_dxys[ib], ibe, w);
        }

        // now, sort jet by descending (nsigma)dxy
        std::sort(jettk_dxys.begin(), jettk_dxys.end(), std::greater<double>());
        std::sort(jettk_nsigmadxys.begin(), jettk_nsigmadxys.end(), std::greater<double>());

        // fill some more hists
        for (auto n_hist : fill_calo_hists) {
             for (int ib=0, ibe=jettk_dxys.size(); ib < ibe; ib++) {
                  h_calojet_jettk_ifar_dxy[n_hist]->Fill(ib, jettk_dxys[ib], w);
             }
             for (int ib=0, ibe=jettk_nsigmadxys.size(); ib < ibe; ib++) {
                  h_calojet_jettk_ifar_nsigmadxy[n_hist]->Fill(ib, jettk_nsigmadxys[ib], w);
             }
        }

        // And fill some more track-based hists
        for (auto helper : calo_trackhelpers) {
            h_calo_jettk_dxy->Fill(helper.dr, w);
            h_calo_jettk_dxyerr->Fill(helper.drerr, w);
            h_calo_jettk_nsigmadxy->Fill(helper.drsig, w);
            h_calo_jettk_pt->Fill(helper.pt, w);
            h_calo_jettk_eta->Fill(fabs(helper.eta), w);
            h_calo_jettk_phi->Fill(helper.phi, w);
            h_calo_jettk_deta->Fill(fabs(helper.eta-mevent->calo_jet_eta[i]), w);
            h_calo_jettk_dphi->Fill(fabs(TVector2::Phi_mpi_pi(helper.phi - mevent->calo_jet_phi[i])), w);
            h_calo_jettk_deltaR->Fill(helper.deltaR, w);
            h_calo_jettk_deta_dxy->Fill(fabs(helper.eta-mevent->calo_jet_eta[i]), helper.dr, w);
            h_calo_jettk_dphi_dxy->Fill(TVector2::Phi_mpi_pi(helper.phi - mevent->calo_jet_phi[i]), helper.dr, w);
            h_calo_jettk_deltaR_dxy->Fill(helper.deltaR, helper.dr, w);
            h_calo_jettk_npxhits->Fill(helper.npxhits, w);
            h_calo_jettk_nsthits->Fill(helper.nsthits, w);
    
        }
    }
    
    h_calojet_npasshlt->Fill(calojet_npass_hlt, w);
    h_calojet_npassprompt->Fill(calojet_npass_prompt, w);
    h_calojet_ntagged->Fill(calojet_ntagged, w);
    h_calojet_nweird_ngood->Fill(calojet_nweird, calojet_ngood, w);
    h_calojet_sum_good_weird->Fill(calojet_nweird + calojet_ngood, w);

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////   END CALOJET STUFF
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////   START PFJET STUFF

    // This might messes up something down around L1150 or so. FIXME!!! at some point
    bool debug = false;
    if (debug) std::cout << "\n\n--------------------------------------\n--------------------------------------\nStarting tag and probe" << std::endl;
    if (debug) std::cout << "# of HLT PF btags      : " << mevent->hlt_pfforbtag_jet_pt.size() << std::endl;
    if (debug) std::cout << "# of HLT Calo btags    : " << mevent->hlt_calo_jet_pt.size() << std::endl;
    if (debug) std::cout << "# of HLT Calo low-btags: " << mevent->hlt_low_calo_b_jet_pt.size() << std::endl;
    // bool pass_di_kine_filters      = true;
    // bool pass_alt_tri_kine_filters = (year == 20161 or year == 20162);
    // bool pass_tri_kine_filters     = (year == 2017  or year == 2018);
    bool pass_di_kine_filters      = get_hlt_btag_factors_calo or force_hlt_btag_study;
    bool pass_tri_kine_filters     = get_hlt_btag_factors_pf   or (force_hlt_btag_study and (year == 2017 or year == 2018)); 
    bool pass_alt_tri_kine_filters = get_hlt_btag_factors_calo_low or (force_hlt_btag_study and (year == 20161 or year == 20162));

    for (auto bit : di_kine_filter_bits) {
        if (not mevent->pass_filter(bit)) {
            pass_di_kine_filters = false;
            break;
        };
    }

    for (auto bit : tri_kine_filter_bits) {
        if (not mevent->pass_filter(bit)) {
            pass_tri_kine_filters = false;
            break;
        };
    }

    // Gotta do something a bit differently for the two 2016 tri-bjet triggers
    if (get_hlt_btag_factors_calo_low) {
        if (debug) std::cout << "In get_hlt_btag_factors_calo_low conditional!" << std::endl;
        bool pass_symm = true;
        bool pass_skew = true;
        if (debug) std::cout << "Before filt check: pass_symm: " << pass_symm << "     pass_skew: " << pass_skew << std::endl;

        for (auto bit : tri_symm_kine_filter_bits) {
            if (not mevent->pass_filter(bit)) {
                pass_symm = false;
                break;
            }
        }
        for (auto bit : tri_skew_kine_filter_bits) {
            if (not mevent->pass_filter(bit)) {
                pass_skew = false;
                break;
            }
        }

        if (debug) std::cout << "After  filt check: pass_symm: " << pass_symm << "     pass_skew: " << pass_skew << std::endl;

        if (not (pass_skew or pass_symm)) {
            pass_alt_tri_kine_filters = false;
        }
    }

    bool satisfies_kine_reqs = (pass_tri_kine_filters or pass_di_kine_filters or pass_alt_tri_kine_filters);
    if (debug) std::cout << "satisfies_kine_reqs = " << satisfies_kine_reqs << "\n" << std::endl;
    
    if (debug) std::cout << "Starting jet loop!" << std::endl;
    for (int i = 0; i < mevent->njets(); ++i) {
        if (debug) std::cout << "\nJet #" << i << "\n----------------------------" << std::endl;
        if (debug) std::cout << "DeepJet score: " << mevent->jet_bdisc_deepflav[i] << std::endl;
        if (debug) std::cout << "|eta|:         " << fabs(mevent->nth_jet_eta(i)) << std::endl;
        bool matches_online_bjet          = false;
        bool matches_online_calo_bjet     = false;
        bool matches_online_calo_low_bjet = false;
        bool matches_online_jet           = false;

        if (mevent->jet_bdisc_deepcsv[i] < offline_csv || mevent->nth_jet_pt(i) < pt_lo_for_tag_probe ||
            mevent->nth_jet_pt(i) > pt_hi_for_tag_probe || fabs(mevent->nth_jet_eta(i)) > 2.4) continue;

        //Require that there is at least one other jet in the event which passes a med btag
        bool has_tag_jet_buddy = false;
        for (int j=0; j < mevent->njets(); ++j) {
            if (i == j) continue;

            if (mevent->is_btagged(j, 1) and mevent->nth_jet_pt(j) > 30.0 and fabs(mevent->nth_jet_eta(j)) < 2.4) {  // the "1" in is_btagged stands for med.
                has_tag_jet_buddy = true;
                break;  
            }
        }

        if ( (get_hlt_btag_factors_pf or get_hlt_btag_factors_calo or get_hlt_btag_factors_calo_low) and ((not has_tag_jet_buddy) or (not satisfies_kine_reqs)) ) continue;
        if (debug) std::cout << "Has buddy AND satisfies basic kinematic reqs" << std::endl;

    
        float sum_nsigmadxy = 0.0;
        float sum_nsigmadxyz = 0.0;
    
        float off_eta = mevent->nth_jet_eta(i);
        float off_phi = mevent->nth_jet_phi(i);
        //float hlt_match_pt = -1.0;

        float jet_dbv = 0.0;
    
        TVector3 jet_vector;
        jet_vector.SetPtEtaPhi(mevent->nth_jet_pt(i), off_eta, off_phi);       
        jet_vector.SetMag(1.0);
    
        // See if this jet matches to an online jet (probably yes)
        float jet_min_hlt_dR = 9.9;
        int n_online_jets = mevent->hlt_pf_jet_pt.size();
        for (int j=0; j < n_online_jets; j++) {
            if (mevent->hlt_pf_jet_pt[j] < 30.0) continue;
            float hlt_eta = mevent->hlt_pf_jet_eta[j];
            float hlt_phi = mevent->hlt_pf_jet_phi[j];
            float this_dR = reco::deltaR(hlt_eta, hlt_phi, off_eta, off_phi);
            if (this_dR < jet_min_hlt_dR) {
                jet_min_hlt_dR = this_dR;
            }
        }
        if (jet_min_hlt_dR < 0.40) { matches_online_jet = true; }
    
        // If for some weird reason, there's no match btwn online/offline jets, skip the remaining portion of the loop
        if (require_match_to_hlt and (not matches_online_jet)) continue;

        // See if this jet matches to some HLT jet which passes the btag filters
        int n_online_bjets = mevent->hlt_pfforbtag_jet_pt.size();
        //int n_hlt_calobjets = mevent->hlt_idp_calo_jet_pt.size();

        float jet_min_hlt_bjet_dR = 9.9;
        if (year == 2017 or year == 2018) {
            for (int j=0; j < n_online_bjets; j++) {
                float hlt_eta = mevent->hlt_pfforbtag_jet_eta[j];
                float hlt_phi = mevent->hlt_pfforbtag_jet_phi[j];
                float this_dR = reco::deltaR(hlt_eta, hlt_phi, off_eta, off_phi);
                if (this_dR < jet_min_hlt_bjet_dR) {
                    jet_min_hlt_bjet_dR = this_dR;
                    //hlt_match_pt = mevent->hlt_pfforbtag_jet_pt[i];
                }
            }
        }
        if(jet_min_hlt_bjet_dR < 0.40) { matches_online_bjet = true; }
        if (debug) std::cout << "matches_online_bjet = " << matches_online_bjet << std::endl;

        //See if this jet matches to an HLT calojet
        float jet_min_hlt_calo_dR = 0.801;
        float jet_min_hlt_calo_pt = -999.9;
        for (int j=0, je=mevent->hlt_calo_jet_pt.size(); j < je; j++) {
            float hlt_eta = mevent->hlt_calo_jet_eta[j];
            float hlt_phi = mevent->hlt_calo_jet_phi[j];

            float this_dR = reco::deltaR(hlt_eta, hlt_phi, off_eta, off_phi);
            if (this_dR < jet_min_hlt_calo_dR) {
                jet_min_hlt_calo_dR = this_dR;
                jet_min_hlt_calo_pt = mevent->hlt_calo_jet_pt[j];
            }
        }

        //See if this jet matches to one which satisfies the HLT calo bjet filter
        float jet_min_hlt_calo_bjet_dR = 9.9;
        for (int j=0, je=mevent->hlt_calo_b_jet_pt.size(); j < je; j++) {
            float hlt_eta = mevent->hlt_calo_b_jet_eta[j];
            float hlt_phi = mevent->hlt_calo_b_jet_phi[j];
            float this_dR = reco::deltaR(hlt_eta, hlt_phi, off_eta, off_phi);
            if (this_dR < jet_min_hlt_calo_bjet_dR) {
                jet_min_hlt_calo_bjet_dR = this_dR;
            }
        }
        if(jet_min_hlt_calo_bjet_dR < 0.40) { matches_online_calo_bjet = true; }
        if (debug) std::cout << "matches_online_calo_bjet = " << matches_online_calo_bjet << std::endl;

        //See if this jet matches to one which satisfies the HLT calo bjet (low-score) filter
        float jet_min_hlt_calo_low_bjet_dR = 9.9;
        if (year == 20161 or year == 20162) {
            for (int j=0, je=mevent->hlt_low_calo_b_jet_pt.size(); j < je; j++) {
                float hlt_eta = mevent->hlt_low_calo_b_jet_eta[j];
                float hlt_phi = mevent->hlt_low_calo_b_jet_phi[j];
                float this_dR = reco::deltaR(hlt_eta, hlt_phi, off_eta, off_phi);
                if (this_dR < jet_min_hlt_calo_low_bjet_dR) {
                    jet_min_hlt_calo_low_bjet_dR = this_dR;
                }
            }
        }
        if(jet_min_hlt_calo_low_bjet_dR < 0.40) { matches_online_calo_low_bjet = true; }
        if (debug) std::cout << "matches_online_calo_low_bjet = " << matches_online_calo_low_bjet << std::endl;

        // Study the effects of online/offline btagging differences by punishing online tags in MC
        if (apply_hlt_btagging) {
            float rand_y = distribution(rng);
            float rand_z = distribution(rng);
            float rand_w = distribution(rng);

            matches_online_bjet          = jmt::UncertTools::refactor_btag_hlt(mevent->jet_bdisc_deepcsv[i], matches_online_bjet, rand_y, year);
            matches_online_calo_bjet     = jmt::UncertTools::refactor_calo_btag_hlt(mevent->jet_bdisc_deepcsv[i], matches_online_calo_bjet, rand_z, year);
            matches_online_calo_low_bjet = jmt::UncertTools::refactor_calo_lo_btag_hlt(mevent->jet_bdisc_deepcsv[i], matches_online_calo_low_bjet, rand_w, year);
        }

        if (matches_online_bjet         ) n_online_btags++;
        if (matches_online_calo_bjet    ) n_online_calo_btags++;
        if (matches_online_calo_low_bjet) n_online_calo_lo_btags++;

        // Which histograms do we need to fill?
        std::vector<int> fill_hists;
        fill_hists.push_back(ALL);     // Always fill histo #0
        fill_hists.push_back(matches_online_bjet ? PASS_HLT : FAIL_HLT);
        //fill_hists.push_back(mevent->jet_bdisc_deepcsv[i] > offline_csv ? PASS_OFF : FAIL_OFF);
        if (matches_online_calo_bjet) fill_hists.push_back(PASS_HLT_CALO_BJET);
        if (matches_online_calo_low_bjet) fill_hists.push_back(PASS_HLT_CALO_LOW_BJET);
        
        // Try and find the point that this jet originates from. Do this by finding the closest instance of jet_loc_helper
        // Fill the pre-determined histograms
        for (auto n_hist : fill_hists) {
             h_jet_pt[n_hist]->Fill(mevent->nth_jet_pt(i), w);
             h_jet_eta[n_hist]->Fill(fabs(mevent->nth_jet_eta(i)), w);
             h_jet_phi[n_hist]->Fill(mevent->nth_jet_phi(i), w);
             h_jet_dbv[n_hist]->Fill(jet_dbv, w);
             h_jet_ntks[n_hist]->Fill((int)(mevent->n_jet_tracks(i)));
             h_jet_bdisc_deepflav[n_hist]->Fill((i < (int)(mevent->jet_bdisc_deepflav.size()) ? mevent->jet_bdisc_deepflav[i] : -9.9), w);
             h_jet_bdisc_deepcsv[n_hist]->Fill((i < (int)(mevent->jet_bdisc_deepcsv.size()) ? mevent->jet_bdisc_deepcsv[i] : -9.9), w);
             h_jet_bdisc_csv[n_hist]->Fill((i < (int)(mevent->jet_bdisc_csv.size()) ? mevent->jet_bdisc_csv[i] : -9.9), w);
             h_jet_min_hlt_dR[n_hist]->Fill(jet_min_hlt_dR, w);
             h_jet_min_hlt_bjet_dR[n_hist]->Fill(jet_min_hlt_bjet_dR,w);
             h_jet_min_hlt_calo_bjet_dR[n_hist]->Fill(jet_min_hlt_calo_bjet_dR,w);
             h_jet_min_hlt_calo_dR[n_hist]->Fill(jet_min_hlt_calo_dR,w);
             if (jet_min_hlt_calo_dR < 0.4) {
                h_jet_hlt_calo_dpt[n_hist]->Fill((mevent->nth_jet_pt(i)-jet_min_hlt_calo_pt)/mevent->nth_jet_pt(i), w);
             }
             h_jet_matches_hlt[n_hist]->Fill(matches_online_jet,w);
             h_jet_matches_hlt_bjet[n_hist]->Fill(matches_online_bjet, w);
             h_jet_matches_hlt_calo_bjet[n_hist] ->Fill(matches_online_calo_bjet, w);
        }

        // Start the track portion of this code
        TVector3 jet_sumtk_vector;
        jet_sumtk_vector.SetPtEtaPhi(0.0, 0.0, 0.0);

        std::vector<Track_Helper> trackhelper;
        for (size_t ntk = 0 ; ntk < mevent->n_jet_tracks_all() ; ntk++) {
            if (mevent->jet_track_which_jet[ntk] == i) {
               
              // Vars needed to get 3D IP dist significance
              float dr = mevent->jet_track_dxy[ntk];
              float dz = mevent->jet_track_dz[ntk];
              float drerr = mevent->jet_track_dxy_err[ntk];
              float dzerr = mevent->jet_track_dz_err[ntk];
      
              // Calculate 3D IP dist significance
              float drz = std::hypot(dr, dz);
              float drzerr = std::hypot(dr*drerr/drz , dz*dzerr/drz);
      
              // Add the above variables to a temporary Track_Helper instance. Then, append it.
              Track_Helper temp_helper;
              temp_helper.dr = dr;
              temp_helper.dz = dz;
              temp_helper.drerr = drerr;
              temp_helper.dzerr = dzerr;
              temp_helper.drz = drz;
              temp_helper.drzerr = drzerr;
              trackhelper.push_back(temp_helper);
      
              TVector3 tk_vector;
              tk_vector.SetPtEtaPhi(fabs(mevent->jet_track_qpt[ntk]), mevent->jet_track_eta[ntk], mevent->jet_track_phi[ntk]);
      
              jet_sumtk_vector += tk_vector;        
              sum_nsigmadxy  += fabs(dr/drerr);
              sum_nsigmadxyz += fabs(drz/drzerr);
             
              float pt_rel = (tk_vector.Cross(jet_vector)).Mag();
              float eta_rel = std::atanh( tk_vector.Dot(jet_vector) / tk_vector.Mag() );
      
              for (auto n_hist : fill_hists) {
                   h_jet_tks_pt[n_hist]->Fill(fabs(mevent->jet_track_qpt[ntk]), w);
                   h_jet_tks_pt_rel[n_hist]->Fill(pt_rel, w);
                   h_jet_tks_eta[n_hist]->Fill(fabs(mevent->jet_track_eta[ntk]), w);
                   h_jet_tks_eta_rel[n_hist]->Fill(eta_rel, w);
                   h_jet_tks_dR[n_hist]->Fill(tk_vector.DeltaR(jet_vector), w);
                   h_jet_tks_dxy[n_hist]->Fill(fabs(dr), w);
                   h_jet_tks_dxyz[n_hist]->Fill(fabs(drz), w);
                   h_jet_tks_nsigmadxy[n_hist]->Fill(fabs(dr/drerr), w);
                   h_jet_tks_nsigmadxyz[n_hist]->Fill(fabs(drz/drzerr), w);
              }
            }
      
            for (auto n_hist : fill_hists) {
                h_jet_sum_nsigmadxy[n_hist]->Fill(sum_nsigmadxy, w);
                h_jet_sum_nsigmadxyz[n_hist]->Fill(sum_nsigmadxyz, w);
            }
    
        }
    
        // Sort the tracks in the jet by nsigma(dxyz)
        std::sort(trackhelper.begin(), trackhelper.end(), [](Track_Helper const &a, Track_Helper &b) -> bool{ return fabs(a.dr/a.drerr) > fabs(b.dr/b.drerr); } );
        //std::sort(trackhelper.begin(), trackhelper.end(), [](Track_Helper const &a, Track_Helper &b) -> bool{ return fabs(a.drz/a.drzerr) > fabs(b.drz/b.drzerr); } );
        
        // Calculate mean and median nsigmadxy
        int njtks = trackhelper.size();
        if (njtks > 0) {
            float med_nsigmadxy = -2.0;
            float avg_nsigmadxy = 0.0;
      
            float med_nsigmadxyz = -2.0;
            float avg_nsigmadxyz = 0.0;
             
            if (njtks % 2 == 0) { 
                med_nsigmadxy = fabs((trackhelper[njtks/2 - 1].dr / trackhelper[njtks/2 - 1].drerr) + (trackhelper[njtks/2].dr / trackhelper[njtks/2].drerr))/2;
                med_nsigmadxyz = fabs((trackhelper[njtks/2 - 1].drz / trackhelper[njtks/2 - 1].drzerr) + (trackhelper[njtks/2].drz / trackhelper[njtks/2].drzerr))/2;
            }
            else {
                med_nsigmadxy = fabs( trackhelper[njtks/2].dr / trackhelper[njtks/2].drerr );
                med_nsigmadxyz = fabs( trackhelper[njtks/2].drz / trackhelper[njtks/2].drzerr );
            }
      
            for (int it=0; it < njtks; it++) {
                avg_nsigmadxy += fabs(trackhelper[it].dr / trackhelper[it].drerr);
                avg_nsigmadxyz += fabs(trackhelper[it].drz / trackhelper[it].drzerr);
            }
            avg_nsigmadxy /= njtks;
            avg_nsigmadxyz /= njtks;
      
      
            for (auto n_hist : fill_hists) {
                // Plot mean and median nsigmadxy
                h_jet_tk_nsigmadxy_avg[n_hist]->Fill(avg_nsigmadxy, w);
                h_jet_tk_nsigmadxy_med[n_hist]->Fill(med_nsigmadxy, w);
            
                h_jet_tk_nsigmadxyz_avg[n_hist]->Fill(avg_nsigmadxyz, w);
                h_jet_tk_nsigmadxyz_med[n_hist]->Fill(med_nsigmadxyz, w);
            
                // While we're at it, plot max nsigmadxy
                h_jet_tk_nsigmadxy_0[n_hist]->Fill(fabs(trackhelper[0].dr / trackhelper[0].drerr), w);
                h_jet_tk_nsigmadxyz_0[n_hist]->Fill(fabs(trackhelper[0].drz / trackhelper[0].drzerr), w);
            }
        }
    
        for (auto n_hist : fill_hists) {
            if (njtks > 1) {
                h_jet_tk_nsigmadxy_1[n_hist]->Fill(fabs(trackhelper[1].dr / trackhelper[1].drerr), w);
                h_jet_tk_nsigmadxyz_1[n_hist]->Fill(fabs(trackhelper[1].drz / trackhelper[1].drzerr), w);
            }
      
            h_jet_sumtk_pt_ratio[n_hist]->Fill(mevent->nth_jet_pt(i) / jet_sumtk_vector.Pt(), w);
            h_jet_sumtk_dR[n_hist]->Fill(jet_vector.DeltaR(jet_sumtk_vector), w);
        }
    }

    bool satisfies_online_tags = false;
    if (year == 2017 or year == 2018) {
        if      (pass_di_kine_filters  and n_online_calo_btags >= 2) satisfies_online_tags = true;
        else if (pass_tri_kine_filters and      n_online_btags >= 3) satisfies_online_tags = true;
    }
    else {
        if (pass_alt_tri_kine_filters and n_online_calo_lo_btags >= 3) satisfies_online_tags = true;
        if (pass_di_kine_filters      and    n_online_calo_btags >= 2) satisfies_online_tags = true;
    }

    h_online_btags->Fill(n_online_btags, w);
    h_online_calo_btags->Fill(n_online_calo_btags, w);
    h_satisfies_online_tags->Fill((int)(satisfies_online_tags), w);
      
    //////////////////////////////////////////////////////////////////////////////
}
DEFINE_FWK_MODULE(MFVJetTksHistos);
