#include <stdio.h>
#include <math.h>
#include "TH2F.h"
#include "TH3F.h"
#include "TRandom3.h"
#include "TVector2.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/ExtValue.h"
#include "JMTucker/Tools/interface/GenUtilities.h"
#include "JMTucker/Tools/interface/Utilities.h"
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
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::EDGetTokenT<MFVEvent> mevent_token;
  const edm::EDGetTokenT<double> weight_token;
  const edm::EDGetTokenT<MFVVertexAuxCollection> vertex_token;

  static const int CATEGORIES = 5;
  const int ALL      = 0;
  const int PASS_HLT = 1;
  const int FAIL_HLT = 2;
  const int PASS_OFF = 3;
  const int FAIL_OFF = 4;

  static const int CALO_CATEGORIES = 3;
  // const int ALL       = 0;
  const int PASS_CALO_HLT = 1;
  const int FAIL_CALO_HLT = 2;

  static const int   dxy_nbins = 9;
  Double_t dxy_edges[dxy_nbins+1] = {0.0, 0.025, 0.05, 0.075, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50};

  const double offline_csv;
  const double pt_thresh_shift;
  const double tk_match_shift;
  const double soft_tk_thresh;
  const bool plot_soft_tks;
  const bool plot_hard_tks;
  const bool require_triggers;
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

  TH1F* h_calojet_ntagged;

  TH1F* h_calo_jettk_dxy;
  TH2F* h_calo_jettk_dxy_mult;
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
  TH1F* h_calojet_pudisc[CALO_CATEGORIES];
  TH1F* h_calojet_filtscore[CALO_CATEGORIES];
  TH1F* h_calojet_ntks[CALO_CATEGORIES];
  TH1F* h_calojet_njettks[CALO_CATEGORIES];
  TH1F* h_calojet_nseedtks[CALO_CATEGORIES];
  TH1F* h_calojet_jettk_dxy[CALO_CATEGORIES];
  TH2F* h_calojet_jettk_iclose_dxy[CALO_CATEGORIES];
  TH2F* h_calojet_jettk_ifar_dxy[CALO_CATEGORIES];
  TH1F* h_calojet_jettk_nsigmadxy[CALO_CATEGORIES];
  TH2F* h_calojet_jettk_iclose_nsigmadxy[CALO_CATEGORIES];
  TH2F* h_calojet_jettk_ifar_nsigmadxy[CALO_CATEGORIES];
  TH1F* h_calojet_seedtk_dxy[CALO_CATEGORIES];
  TH2F* h_calojet_seedtk_iclose_dxy[CALO_CATEGORIES];
  TH2F* h_calojet_seedtk_ifar_dxy[CALO_CATEGORIES];
  TH1F* h_calojet_seedtk_nsigmadxy[CALO_CATEGORIES];
  TH2F* h_calojet_seedtk_iclose_nsigmadxy[CALO_CATEGORIES];
  TH2F* h_calojet_seedtk_ifar_nsigmadxy[CALO_CATEGORIES];
  TH1F* h_calojet_med_jettk_dxy[CALO_CATEGORIES];
  TH1F* h_calojet_med_jettk_nsigmadxy[CALO_CATEGORIES];
  TH1F* h_calojet_med_seedtk_dxy[CALO_CATEGORIES];
  TH1F* h_calojet_med_seedtk_nsigmadxy[CALO_CATEGORIES];

  TH1F* h_jet_tks_pt[CATEGORIES];  
  TH1F* h_jet_tks_pt_rel[CATEGORIES];  
  TH1F* h_jet_tks_eta[CATEGORIES];  
  TH1F* h_jet_tks_eta_rel[CATEGORIES];  
  TH1F* h_jet_tks_dR[CATEGORIES];  
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

  TH2F* h_proxy_grid[CATEGORIES];
};

MFVJetTksHistos::MFVJetTksHistos(const edm::ParameterSet& cfg)
  : mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
    vertex_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertex_src"))),
    offline_csv(cfg.getParameter<double>("offline_csv")),
    pt_thresh_shift(cfg.getParameter<double>("pt_thresh_shift")),
    tk_match_shift(cfg.getParameter<double>("tk_match_shift")),
    soft_tk_thresh(cfg.getParameter<double>("soft_tk_thresh")),
    plot_soft_tks(cfg.getParameter<bool>("plot_soft_tks")),
    plot_hard_tks(cfg.getParameter<bool>("plot_hard_tks")),
    require_triggers(cfg.getParameter<bool>("require_triggers")),
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
    TString bres = i == 4 ? TString("fail_off") : (i == 3 ? TString("pass_off") : (i == 2 ? TString("fail_hlt") : (i == 1 ? TString("pass_hlt") : "pass_or_fail")));
    h_jet_pt[i] = fs->make<TH1F>(TString::Format("h_jet_pt_%s", bres.Data()), TString::Format(";p_{T} of jets that %s b-tag(GeV);events/10 GeV", bres.Data()), 200, 0, 800);
    h_jet_eta[i] = fs->make<TH1F>(TString::Format("h_jet_eta_%s", bres.Data()), TString::Format(";absv#eta of jets that %s b-tag;events/bin", bres.Data()), 120, 0, 2.5);
    h_jet_phi[i] = fs->make<TH1F>(TString::Format("h_jet_phi_%s", bres.Data()), TString::Format(";#phi of jets that %s b-tag;events/bin", bres.Data()), 100, -3.1416, 3.1416);
    h_jet_dbv[i] = fs->make<TH1F>(TString::Format("h_jet_dbv_%s", bres.Data()), TString::Format(";d_{BV} of jets that %s b-tag;events/bin", bres.Data()), 100, 0.0, 2.0);
    h_jet_ntks[i] = fs->make<TH1F>(TString::Format("h_jet_ntks_%s", bres.Data()), TString::Format(";#tks in jets that %s b-tag;events/bin", bres.Data()), 40, 0, 40);
    h_jet_bdisc_deepflav[i] = fs->make<TH1F>(TString::Format("h_jet_bdisc_deepflav_%s", bres.Data()), TString::Format(";DeepJet of jets that %s b-tag;events/bin", bres.Data()), 100, 0, 1.0);
    h_jet_bdisc_deepcsv[i] = fs->make<TH1F>(TString::Format("h_jet_bdisc_deepcsv_%s", bres.Data()), TString::Format(";CSV of jets that %s b-tag;events/bin", bres.Data()), 100, 0, 1.0);

    h_jet_tks_pt[i] = fs->make<TH1F>(TString::Format("h_jet_tks_pt_%s", bres.Data()), TString::Format(";p_{T} of all tks in jets that %s b-tag (GeV);events/bin", bres.Data()), 200, 0, 40);
    h_jet_tks_pt_rel[i] = fs->make<TH1F>(TString::Format("h_jet_tks_ptrel_%s", bres.Data()), TString::Format(";rel p_{T} of all tks in jets that %s b-tag (GeV);events/bin", bres.Data()), 200, 0, 20);
    h_jet_tks_eta[i] = fs->make<TH1F>(TString::Format("h_jet_tks_eta_%s", bres.Data()), TString::Format(";abs #eta of all tks in jets that %s b-tag;events/bin", bres.Data()), 100, 0, 4);
    h_jet_tks_eta_rel[i] = fs->make<TH1F>(TString::Format("h_jet_tks_etarel_%s", bres.Data()), TString::Format(";rel #eta of all tks in jets that %s b-tag;events/bin", bres.Data()), 300, 0, 10);
    h_jet_tks_dR[i] = fs->make<TH1F>(TString::Format("h_jet_tks_dR_%s", bres.Data()), TString::Format(";dR between jet and all tks in jets - %s b-tag;events/bin", bres.Data()), 100, 0, 0.6);
    h_jet_tks_nsigmadxy[i] = fs->make<TH1F>(TString::Format("h_jet_tks_nsigmadxy_%s", bres.Data()), TString::Format("; n #sigma(dxy) of all tks in jets which %s b-tag;events/bin", bres.Data()), 150, 0, 15);
    h_jet_tks_nsigmadxyz[i] = fs->make<TH1F>(TString::Format("h_jet_tks_nsigmadxyz_%s", bres.Data()), TString::Format("; n#sigma(dxyz) of tks in jets which %s b-tag;events/bin", bres.Data()), 150, 0, 15);
    h_jet_sum_nsigmadxy[i] = fs->make<TH1F>(TString::Format("h_jet_sum_nsigmadxy_%s", bres.Data()), TString::Format(";#Sigma n#sigma(dxy) of tks in jets which %s b-tag;events/bin", bres.Data()), 500, 0, 1500);
    h_jet_sum_nsigmadxyz[i] = fs->make<TH1F>(TString::Format("h_jet_sum_nsigmadxyz_%s", bres.Data()), TString::Format(";#Sigman#sigma(dxyz) of tks in jets which %s b-tag;events/bin", bres.Data()), 500, 0, 1500);

    h_jet_tk_nsigmadxy_avg[i] = fs->make<TH1F>(TString::Format("h_jet_tk_nsigmadxy_avg_%s", bres.Data()), TString::Format("; avg n#sigma(dxy) of tks in jets which %s b-tag; events/bin", bres.Data()), 300, 0, 30);
    h_jet_tk_nsigmadxy_med[i] = fs->make<TH1F>(TString::Format("h_jet_tk_nsigmadxy_med_%s", bres.Data()), TString::Format("; median n#sigma(dxy) of tks in jets which %s b-tag; events/bin", bres.Data()), 300, 0, 30);
    h_jet_tk_nsigmadxy_0[i] = fs->make<TH1F>(TString::Format("h_jet_tk_nsigmadxy_0_%s", bres.Data()), TString::Format("; max n#sigma(dxy) of tks in jets which %s b-tag; events/bin", bres.Data()), 300, 0, 150);
    h_jet_tk_nsigmadxy_1[i] = fs->make<TH1F>(TString::Format("h_jet_tk_nsigmadxy_1_%s", bres.Data()), TString::Format("; 2nd-leading n#sigma(dxy) of tks in jets which %s b-tag; events/bin", bres.Data()), 300, 0, 150);

    h_jet_tk_nsigmadxyz_avg[i] = fs->make<TH1F>(TString::Format("h_jet_tk_nsigmadxyz_avg_%s", bres.Data()), TString::Format("; avg n#sigma(dxyz) of tks in jets which %s b-tag; events/bin", bres.Data()), 300, 0, 30);
    h_jet_tk_nsigmadxyz_med[i] = fs->make<TH1F>(TString::Format("h_jet_tk_nsigmadxyz_med_%s", bres.Data()), TString::Format("; median n#sigma(dxyz) of tks in jets which %s b-tag; events/bin", bres.Data()), 300, 0, 30);
    h_jet_tk_nsigmadxyz_0[i] = fs->make<TH1F>(TString::Format("h_jet_tk_nsigmadxyz_0_%s", bres.Data()), TString::Format("; max n#sigma(dxyz) of tks in jets which %s b-tag; events/bin", bres.Data()), 300, 0, 150);
    h_jet_tk_nsigmadxyz_1[i] = fs->make<TH1F>(TString::Format("h_jet_tk_nsigmadxyz_1_%s", bres.Data()), TString::Format("; 2nd-leading n#sigma(dxyz) of tks in jets which %s b-tag; events/bin", bres.Data()), 300, 0, 150);

    h_jet_sumtk_pt_ratio[i] = fs->make<TH1F>(TString::Format("h_jet_sumtk_pt_ratio_%s", bres.Data()), TString::Format(";pT(jet tracks) / pT(jet) - %s b-tag;events/bin", bres.Data()), 100, 0, 4);
    h_jet_sumtk_dR[i] = fs->make<TH1F>(TString::Format("h_jet_sumtk_dR_%s", bres.Data()), TString::Format(";dR between jet and tks in jets - %s b-tag;events/bin", bres.Data()), 100, 0, 0.6);
    
    h_proxy_grid[i] = fs->make<TH2F>(TString::Format("h_proxy_grid_%s", bres.Data()), ";b-score cut value; >=3 offline proxies?", 100, 0, 1, 2, 0, 1.2);
  }

  h_calojet_ntagged = fs->make<TH1F>("h_calojet_ntagged", "; # of tagged offline calojets; entries", 20, 0, 20);

  h_calo_jettk_dxy = fs->make<TH1F>("h_calo_jettk_dxy", ";dxy of pfjettks in calojets (cm);entries", 250, 0, 0.5);
  h_calo_jettk_dxy_mult = fs->make<TH2F>("h_calo_jettk_dxy_mult", ";dxy of pfjettks in calojets (cm); ntks per jet with dxy", dxy_nbins, dxy_edges, 20, -0.5, 19.5);
  h_calo_jettk_dxy_ic_mult = fs->make<TH3F>("h_calo_jettk_dxy_ic_mult", ";nth-promptest track index;d_{xy};# of tracks per jet",
                                              15, 0, 15,
                                             250, 0, 0.5,
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
    TString bres = (i == 2 ? TString("fail_hlt") : (i == 1 ? TString("pass_hlt") : "all"));
    h_calojet_pt[i] = fs->make<TH1F>(TString::Format("h_calojet_pt_%s", bres.Data()), TString::Format(";p_{T} of calojets that %s (GeV);events/10 GeV", bres.Data()), 100, 0, 800);
    h_calojet_pt_raw[i] = fs->make<TH1F>(TString::Format("h_calojet_pt_raw_%s", bres.Data()), TString::Format(";'raw' p_{T} of calojets that %s (GeV);events/10 GeV", bres.Data()), 100, 0, 800);
    h_calojet_eta[i] = fs->make<TH1F>(TString::Format("h_calojet_eta_%s", bres.Data()), TString::Format(";absv#eta of calojets that %s;events/bin", bres.Data()), 60, 0, 2.5);
    h_calojet_phi[i] = fs->make<TH1F>(TString::Format("h_calojet_phi_%s", bres.Data()), TString::Format(";#phi of calojets that %s;events/bin", bres.Data()), 63, -M_PI, M_PI);
    h_calojet_dbv[i] = fs->make<TH1F>(TString::Format("h_calojet_dbv_%s", bres.Data()), TString::Format(";best guess d_{BV} of calojets that %s; events/bin", bres.Data()), 50, 0, 2.0);
    h_calojet_dxy[i] = fs->make<TH1F>(TString::Format("h_calojet_dxy_%s", bres.Data()), TString::Format(";best guess d_{xy} of calojets that %s; events/bin", bres.Data()), 50, 0, 2.0);
    h_calojet_pf_dR[i] = fs->make<TH1F>(TString::Format("h_calojet_pf_dR_%s", bres.Data()), TString::Format(";#DeltaR (calojet, pfjet) of calojets that %s; events/bin", bres.Data()), 40, 0, 0.4);
    h_calojet_pf_next_dR[i] = fs->make<TH1F>(TString::Format("h_calojet_pf_next_dR_%s", bres.Data()), TString::Format(";#DeltaR (calojet, 2nd-closest pfjet) of calojets that %s; events/bin", bres.Data()), 60, 0, 0.6);
    h_calojet_pudisc[i] = fs->make<TH1F>(TString::Format("h_calojet_pudisc_%s", bres.Data()), TString::Format(";pudisc of calojets that %s;events/bin", bres.Data()), 200, -1.0, 1.0);
    h_calojet_filtscore[i] = fs->make<TH1F>(TString::Format("h_calojet_filtscore_%s", bres.Data()), TString::Format(";filtscore of calojets that %s; events/bin", bres.Data()), 4, 0, 4);
    h_calojet_ntks[i] = fs->make<TH1F>(TString::Format("h_calojet_ntks_%s", bres.Data()), TString::Format(";ntks in calojets that %s ;events/bin", bres.Data()), 40, 0, 40);
    h_calojet_njettks[i] = fs->make<TH1F>(TString::Format("h_calojet_njettks_%s", bres.Data()), TString::Format(";n(pfjet tks) in calojets that %s ;events/bin", bres.Data()), 40, 0, 40);
    h_calojet_nseedtks[i] = fs->make<TH1F>(TString::Format("h_calojet_nseedtks_%s", bres.Data()), TString::Format(";nseedtks in calojets that %s ;events/bin", bres.Data()), 40, 0, 40);

    h_calojet_jettk_dxy[i] = fs->make<TH1F>(TString::Format("h_calojet_jettk_dxy_%s", bres.Data()), TString::Format(";dxy of pfjettks in calojets that %s (cm); events/bin", bres.Data()), 250, 0, 0.5);
    h_calojet_jettk_iclose_dxy[i] = fs->make<TH2F>(TString::Format("h_calojet_jettk_iclose_dxy_%s", bres.Data()), TString::Format(";nth-closest tk index;dxy of pfjettks in calojets that %s (cm);", bres.Data()), 15, 0, 15, 250, 0, 0.5);
    h_calojet_jettk_ifar_dxy[i] = fs->make<TH2F>(TString::Format("h_calojet_jettk_ifar_dxy_%s", bres.Data()), TString::Format(";nth-farthest tk index;dxy of pfjettks in calojets that %s (cm);", bres.Data()), 15, 0, 15, 250, 0, 0.5);

    h_calojet_jettk_nsigmadxy[i] = fs->make<TH1F>(TString::Format("h_calojet_jettk_nsigmadxy_%s", bres.Data()), TString::Format(";n#sigmadxy of pfjettks in calojets that %s (cm); events/bin", bres.Data()), 150, 0, 150);
    h_calojet_jettk_iclose_nsigmadxy[i] = fs->make<TH2F>(TString::Format("h_calojet_jettk_iclose_nsigmadxy_%s", bres.Data()), TString::Format(";nth-closest tk index;n#sigmadxy of pfjettks in calojets that %s (cm);", bres.Data()), 15, 0, 15, 150, 0, 150);
    h_calojet_jettk_ifar_nsigmadxy[i] = fs->make<TH2F>(TString::Format("h_calojet_jettk_ifar_nsigmadxy_%s", bres.Data()), TString::Format(";nth-farthest tk index;n#sigmadxy of pfjettks in calojets that %s (cm);", bres.Data()), 15, 0, 15, 150, 0, 150);

    h_calojet_seedtk_dxy[i] = fs->make<TH1F>(TString::Format("h_calojet_seedtk_dxy_%s", bres.Data()), TString::Format(";dxy of seedtks in calojets that %s (cm); events/bin", bres.Data()), 250, 0, 0.5);
    h_calojet_seedtk_iclose_dxy[i] = fs->make<TH2F>(TString::Format("h_calojet_seedtk_iclose_dxy_%s", bres.Data()), TString::Format(";nth-closest tk index;dxy of seedtks in calojets that %s (cm);", bres.Data()), 15, 0, 15, 250, 0, 0.5);
    h_calojet_seedtk_ifar_dxy[i] = fs->make<TH2F>(TString::Format("h_calojet_seedtk_ifar_dxy_%s", bres.Data()), TString::Format(";nth-farthest tk index;dxy of seedtks in calojets that %s (cm);", bres.Data()), 15, 0, 15, 250, 0, 0.5);

    h_calojet_seedtk_nsigmadxy[i] = fs->make<TH1F>(TString::Format("h_calojet_seedtk_nsigmadxy_%s", bres.Data()), TString::Format(";n#sigmadxy of seedtks in calojets that %s; events/bin", bres.Data()), 150, 0, 150);
    h_calojet_seedtk_iclose_nsigmadxy[i] = fs->make<TH2F>(TString::Format("h_calojet_seedtk_iclose_nsigmadxy_%s", bres.Data()), TString::Format(";nth-closest tk index;n#sigmadxy of seedtks in calojets that %s (cm);", bres.Data()), 15, 0, 15, 150, 0, 150);
    h_calojet_seedtk_ifar_nsigmadxy[i] = fs->make<TH2F>(TString::Format("h_calojet_seedtk_ifar_nsigmadxy_%s", bres.Data()), TString::Format(";nth-farthest tk index;n#sigmadxy of seedtks in calojets that %s (cm);", bres.Data()), 15, 0, 15, 150, 0, 150);

    h_calojet_med_jettk_dxy[i] = fs->make<TH1F>(TString::Format("h_calojet_med_jettk_dxy_%s", bres.Data()), TString::Format(";med pfjettk dxy in calojets that %s (cm);", bres.Data()), 250, -.002, 0.498);
    h_calojet_med_jettk_nsigmadxy[i] = fs->make<TH1F>(TString::Format("h_calojet_med_jettk_nsigmadxy_%s", bres.Data()), TString::Format(";med jettk n#sigmadxy in calojets that %s (cm);", bres.Data()), 150, -1, 149);
    h_calojet_med_seedtk_dxy[i] = fs->make<TH1F>(TString::Format("h_calojet_med_seedtk_dxy_%s", bres.Data()), TString::Format(";med seedtk dxy in calojets that %s (cm);", bres.Data()), 250, -.002, 0.498);
    h_calojet_med_seedtk_nsigmadxy[i] = fs->make<TH1F>(TString::Format("h_calojet_med_seedtk_nsigmadxy_%s", bres.Data()), TString::Format(";med seedtk n#sigmadxy in calojets that %s (cm);", bres.Data()), 150, -1, 149);
  }

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
  
    const double w = *weight;
    int    calojet_ntagged = 0;
    int    calojet_ngood   = 0;
    int    calojet_nweird  = 0;
    double online_pfht    = 0.0;
    double online_caloht  = 0.0;
    double offline_pfht   = 0.0;
    double offline_caloht = 0.0;
    h_w->Fill(w);
  
    const size_t n_vertex_seed_tracks = mevent->n_vertex_seed_tracks();

    if ((require_triggers) and not (mevent->pass_hlt(trigger_bit))) return;

    // Calculate on/off caloht
    for (int i = 0, ie=mevent->calo_jet_pt.size(); i < ie; ++i) {
        if ((mevent->calo_jet_pt[i] > 30.0) and (fabs(mevent->calo_jet_eta[i]) < 2.5)) offline_caloht += mevent->calo_jet_pt[i];
    }

    if (offline_caloht < 400.0 or (trigger_bit==19 and offline_caloht < 600.0) or (not mevent->pass_l1(mfv::b_L1_HTT380er))) return;

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
        std::vector<float> seedtk_dxys;
        std::vector<float> seedtk_nsigmadxys;
        float med_jettk_dxy;
        float med_seedtk_dxy;
        float med_jettk_nsigmadxy;
        float med_seedtk_nsigmadxy;
        float closest_pudisc = 0.0;
        float closest_jec_factor = 1.0;
        float pt_thresh = trigger_bit==19 ? 70.0 : 50.0;
        float calojet_dxy = -1.0;

        //                             {0.0, 0.025, 0.05, 0.075, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50};
        std::vector<int> dxy_content = {    0,     0,    0,     0,    0,    0,    0,    0,    0};

        double closest_dR = 9.9;
        double next_dR    = 10.9;
        int    closest_j  = -10;
        int    calojet_nseedtks = 0;
        int    calojet_njettks = 0;
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
                closest_jec_factor = mevent->jet_raw_pt[j] / mevent->jet_pt[j];
            }
            else if (temp_dR < next_dR) {
                next_dR = temp_dR;
            }
        }
        if (good_jet) { h_calojet_pfjet_dR->Fill(has_match ? closest_dR : -0.5, w); }

        // Do some kludge-y filter stuff. First, only run on events/jets that look good enough
        bool   matches_prompt_cjet = false;
        bool   matches_disp_cjet = false;
        //if (not good_jet) continue;
        // Get the number of seed tracks within dR < 0.5
        for (size_t itk = 0; itk < n_vertex_seed_tracks; ++itk) {
            double this_dR = reco::deltaR(mevent->calo_jet_eta[i], mevent->calo_jet_phi[i], mevent->vertex_seed_track_eta[itk], mevent->vertex_seed_track_phi[itk]);
            if (this_dR < 0.5) {
                calojet_nseedtks++;
                seedtk_dxys.push_back(fabs(mevent->vertex_seed_track_dxy[itk]));
                seedtk_nsigmadxys.push_back(fabs(mevent->vertex_seed_track_dxy[itk]/mevent->vertex_seed_track_err_dxy[itk]));
            }
        }

        // Get the number of decent jet tracks within dR < 0.5
        for (size_t itk = 0; itk < mevent->n_jet_tracks_all(); itk++) {
            if (mevent->jet_track_which_jet[itk] != closest_j) continue;
            double this_tk_nsigmadxy = fabs(mevent->jet_track_dxy[itk]/mevent->jet_track_dxy_err[itk]);
            //if (fabs(mevent->jet_track_qpt[itk]) < 1.0 or mevent->jet_track_npxhits(itk) < 2 or mevent->jet_track_nhits(itk) < 8) continue;
            if (fabs(mevent->jet_track_qpt[itk]) < 1.0) continue;

            // Test bit to vary the matching criteria on the softest/hardest tracks
            bool tk_pt_testbit = fabs(mevent->jet_track_qpt[itk]) < soft_tk_thresh;

            double this_dR = reco::deltaR(mevent->calo_jet_eta[i], mevent->calo_jet_phi[i], mevent->jet_track_eta[itk], mevent->jet_track_phi[itk]);
            if (this_dR < (0.4 - (tk_match_shift * tk_pt_testbit))) {

                float abs_dxy = fabs(mevent->jet_track_dxy[itk]);
                for (int iedge=0, iedgee=dxy_nbins+1; iedge<iedgee; iedge++) {
                    if ((abs_dxy > dxy_edges[iedge]) and (abs_dxy < dxy_edges[iedge+1])) {
                        dxy_content[iedge]++;
                    }
                    else {
                        continue;
                    }
                }

                calojet_njettks++;
                jettk_dxys.push_back(fabs(mevent->jet_track_dxy[itk]));
                jettk_nsigmadxys.push_back(this_tk_nsigmadxy);

                if (fabs(mevent->jet_track_dxy[itk]) > 0.05 and this_tk_nsigmadxy > 5.0) calojet_njettks_dispd++;

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

        // See if this calojet matches to one which passes the prompt track tag (Low-HT trigger)
        if (trigger_bit != 19) {
            for (int j=0, je=mevent->hlt_calo_jet_lowpt_fewprompt_pt.size(); j < je; j++) {
                double test_jet_eta = mevent->hlt_calo_jet_lowpt_fewprompt_eta[j];
                double test_jet_phi = mevent->hlt_calo_jet_lowpt_fewprompt_phi[j];
                if (reco::deltaR(mevent->calo_jet_eta[i], mevent->calo_jet_phi[i], test_jet_eta, test_jet_phi) < 0.14) {
                    matches_prompt_cjet = true;
                    break;
                }
            }
        }

        // See if this calojet matches to one which passes the prompt track tag (High-HT trigger)
        if (trigger_bit == 19) {
            for (int j=0, je=mevent->hlt_calo_jet_midpt_fewprompt_pt.size(); j < je; j++) {
                double test_jet_eta = mevent->hlt_calo_jet_midpt_fewprompt_eta[j];
                double test_jet_phi = mevent->hlt_calo_jet_midpt_fewprompt_phi[j];
                if (reco::deltaR(mevent->calo_jet_eta[i], mevent->calo_jet_phi[i], test_jet_eta, test_jet_phi) < 0.14) {
                    matches_prompt_cjet = true;
                    break;
                }
            }
        } 

        // See if this calojet matches to one which passes the displaced track tag
        else {
            for (int j=0, je=mevent->hlt_calo_jet_lowpt_wdisptks_pt.size(); j < je; j++) {
                double test_jet_eta = mevent->hlt_calo_jet_lowpt_wdisptks_eta[j];
                double test_jet_phi = mevent->hlt_calo_jet_lowpt_wdisptks_phi[j];
                if (reco::deltaR(mevent->calo_jet_eta[i], mevent->calo_jet_phi[i], test_jet_eta, test_jet_phi) < 0.14) {
                  matches_disp_cjet = true;
                  break;
                }
            }
        }

        // sort vectors by increasing (nsigma)dxy
        jmt::sortVector(jettk_dxys);
        jmt::sortVector(jettk_nsigmadxys);
        jmt::sortVector(seedtk_dxys);
        jmt::sortVector(seedtk_nsigmadxys);

        // Find median (nsigma)dxys. Return -0.001 if no elements
        med_jettk_dxy  = (calojet_njettks  == 0 ? -0.001 : jmt::computeMedian(jettk_dxys));
        med_seedtk_dxy = (calojet_nseedtks == 0 ? -0.001 : jmt::computeMedian(seedtk_dxys));
        med_jettk_nsigmadxy  = (calojet_njettks  == 0 ? -0.001 : jmt::computeMedian(jettk_nsigmadxys));
        med_seedtk_nsigmadxy = (calojet_nseedtks == 0 ? -0.001 : jmt::computeMedian(seedtk_nsigmadxys));

        // Helper bools
        bool pass_prompt_req   = jettk_dxys.size() >= 3 ? (jettk_dxys[2] > 0.1) : true;
        bool pass_alt_disp_req = calojet_njettks_dispd >= 1;
        bool pass_pt_req       = fabs(mevent->calo_jet_eta[i]) < 2.0 and mevent->calo_jet_pt[i] > (pt_thresh - pt_thresh_shift);

        // Main jet-tagging bools
        bool pass_offline_tagreqs = ((trigger_bit == 18 and pass_prompt_req and pass_alt_disp_req and pass_pt_req) or (trigger_bit == 19 and pass_prompt_req and pass_pt_req));
        bool pass_online_tagreqs  = ((trigger_bit == 18 and matches_disp_cjet and matches_prompt_cjet) or (trigger_bit == 19 and matches_prompt_cjet));
        bool pass_category        = true;
        bool pass_pure_region     = mevent->calo_jet_pt[i] > 50.0;
       
        // 0: passes no offline filter bits      1: passes tk-based bits     2: passes pT-based bits     3: passes all bits
        int calojet_filtscore = 0 + (1 * (trigger_bit == 18 and pass_prompt_req and pass_alt_disp_req)) + (1 * (trigger_bit == 19 and pass_prompt_req)) + (2 * pass_pt_req);

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
            case 3:   // Bad Jets -- also lots of "bad jets" are high eta. Dont care abt 'em
                if (pass_online_tagreqs || pass_offline_tagreqs || fabs(mevent->calo_jet_eta[i]) > 2.0) pass_category = false;
                break;
            case 4:   // "Other" Weird Jets (false positives)
                if (pass_online_tagreqs || !pass_offline_tagreqs) pass_category = false;
                break;
        }

        if ((not pass_category) or (not pass_pure_region)) continue;
        //if (not pass_category) continue;
        
        fill_calo_hists.push_back(ALL);
        fill_calo_hists.push_back(pass_online_tagreqs ? PASS_CALO_HLT : FAIL_CALO_HLT);

        for (auto n_hist : fill_calo_hists) {
             h_calojet_pt[n_hist]->Fill(mevent->calo_jet_pt[i], w);
             h_calojet_pt_raw[n_hist]->Fill(closest_jec_factor * mevent->calo_jet_pt[i], w);
             h_calojet_eta[n_hist]->Fill(fabs(mevent->calo_jet_eta[i]), w);
             h_calojet_phi[n_hist]->Fill(mevent->calo_jet_phi[i], w);
             h_calojet_dxy[n_hist]->Fill(calojet_dxy, w);
             h_calojet_pf_dR[n_hist]->Fill(closest_dR, w);
             h_calojet_pf_next_dR[n_hist]->Fill(next_dR, w);
             h_calojet_ntks[n_hist]->Fill(closest_j >= 0 ? (int)(mevent->n_jet_tracks(closest_j)) : -2, w);
             h_calojet_njettks[n_hist]->Fill(calojet_njettks, w);
             h_calojet_nseedtks[n_hist]->Fill(calojet_nseedtks, w);

             if (mevent->calo_jet_pt[i] < pt_thresh) h_calojet_pudisc[n_hist]->Fill(closest_pudisc, w);

             h_calojet_filtscore[n_hist]->Fill(calojet_filtscore, w);
             h_calojet_med_jettk_dxy[n_hist]->Fill(med_jettk_dxy, w);
             h_calojet_med_seedtk_dxy[n_hist]->Fill(med_seedtk_dxy, w);
             h_calojet_med_jettk_nsigmadxy[n_hist]->Fill(med_jettk_nsigmadxy, w);
             h_calojet_med_seedtk_nsigmadxy[n_hist]->Fill(med_seedtk_nsigmadxy, w);

             for (int ib=0, ibe=jettk_dxys.size(); ib < ibe; ib++) {
                  h_calojet_jettk_dxy[n_hist]->Fill(jettk_dxys[ib], w);
                  h_calojet_jettk_iclose_dxy[n_hist]->Fill(ib, jettk_dxys[ib], w);
             }
             for (int ib=0, ibe=jettk_nsigmadxys.size(); ib < ibe; ib++) {
                  h_calojet_jettk_nsigmadxy[n_hist]->Fill(jettk_nsigmadxys[ib], w);
                  h_calojet_jettk_iclose_nsigmadxy[n_hist]->Fill(ib, jettk_nsigmadxys[ib], w);
             }
             for (int ib=0, ibe=seedtk_dxys.size(); ib < ibe; ib++) {
                  h_calojet_seedtk_dxy[n_hist]->Fill(seedtk_dxys[ib], w);
                  h_calojet_seedtk_iclose_dxy[n_hist]->Fill(ib, seedtk_dxys[ib], w);
             }
             for (int ib=0, ibe=seedtk_nsigmadxys.size(); ib < ibe; ib++) {
                  h_calojet_seedtk_dxy[n_hist]->Fill(seedtk_nsigmadxys[ib], w);
                  h_calojet_seedtk_iclose_nsigmadxy[n_hist]->Fill(ib, seedtk_nsigmadxys[ib], w);
             }
        }


        // Fill this TH3F... rip in peace
        for (int ib=0, ibe=jettk_dxys.size(); ib < ibe; ib++) {
            h_calo_jettk_dxy_ic_mult->Fill(ib, jettk_dxys[ib], ibe, w);
        }

        // now, sort jet by descending (nsigma)dxy
        std::sort(jettk_dxys.begin(), jettk_dxys.end(), std::greater<double>());
        std::sort(jettk_nsigmadxys.begin(), jettk_nsigmadxys.end(), std::greater<double>());
        std::sort(seedtk_dxys.begin(), seedtk_dxys.end(), std::greater<double>());
        std::sort(seedtk_nsigmadxys.begin(), seedtk_nsigmadxys.end(), std::greater<double>());

        // fill some more hists
        for (auto n_hist : fill_calo_hists) {
             for (int ib=0, ibe=jettk_dxys.size(); ib < ibe; ib++) {
                  h_calojet_jettk_ifar_dxy[n_hist]->Fill(ib, jettk_dxys[ib], w);
             }
             for (int ib=0, ibe=jettk_nsigmadxys.size(); ib < ibe; ib++) {
                  h_calojet_jettk_ifar_nsigmadxy[n_hist]->Fill(ib, jettk_nsigmadxys[ib], w);
             }
             for (int ib=0, ibe=seedtk_dxys.size(); ib < ibe; ib++) {
                  h_calojet_seedtk_ifar_dxy[n_hist]->Fill(ib, seedtk_dxys[ib], w);
             }
             for (int ib=0, ibe=seedtk_nsigmadxys.size(); ib < ibe; ib++) {
                  h_calojet_seedtk_ifar_nsigmadxy[n_hist]->Fill(ib, seedtk_nsigmadxys[ib], w);
             }
        }

        // Fill the track multiplicity vs. dxy plot
        for (int iedge=0, iedgee=dxy_nbins+1; iedge<iedgee; iedge++) {
            h_calo_jettk_dxy_mult->Fill(dxy_edges[iedge]+0.0005, dxy_content[iedge], w);           
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
    
    h_calojet_ntagged->Fill(calojet_ntagged, w);
    h_calojet_nweird_ngood->Fill(calojet_nweird, calojet_ngood, w);
    h_calojet_sum_good_weird->Fill(calojet_nweird + calojet_ngood, w);

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////   END CALOJET STUFF
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////   START PFJET STUFF

    for (int i = 0; i < mevent->njets(); ++i) {
        bool matches_online_bjet = false;
        bool matches_online_calo = false;

        if (mevent->jet_bdisc_deepcsv[i] < offline_csv || mevent->nth_jet_pt(i) < 30.0) continue;
    
        std::vector<int> fill_hists;
        fill_hists.push_back(ALL);     // Always fill histo #0
    
        float sum_nsigmadxy = 0.0;
        float sum_nsigmadxyz = 0.0;
    
        //float off_pt  = mevent->nth_jet_pt(i);
        float off_eta = mevent->nth_jet_eta(i);
        float off_phi = mevent->nth_jet_phi(i);

        float jet_dbv = 0.0;
    
        TVector3 jet_vector;
        jet_vector.SetPtEtaPhi(mevent->nth_jet_pt(i), off_eta, off_phi);       
        jet_vector.SetMag(1.0);
    
        // See if this jet matches to an online calojet (probably yes)
        int n_online_calojets = mevent->hlt_pf_jet_pt.size();
        for (int j=0; j < n_online_calojets; j++) {
            float hlt_eta = mevent->hlt_pf_jet_eta[j];
            float hlt_phi = mevent->hlt_pf_jet_phi[j];
    
            if(reco::deltaR(hlt_eta, hlt_phi, off_eta, off_phi) < 0.14) { matches_online_calo = true; break;}
        }
                      
        // If for some weird reason, there's no match btwn online/offline jets, skip this jet
        if (not matches_online_calo) continue;
    
        // See if this jet matches to some HLT jet which passes the btag filters
        //int n_online_bjets = mevent->hlt_pfforbtag_jet_pt.size();
        int n_hlt_calobjets = mevent->hlt_idp_calo_jet_pt.size();
        for (int j=0; j < n_hlt_calobjets; j++) {
            float hlt_eta = mevent->hlt_idp_calo_jet_eta[j];
            float hlt_phi = mevent->hlt_idp_calo_jet_phi[j];
    
            if(reco::deltaR(hlt_eta, hlt_phi, off_eta, off_phi) < 0.14) { matches_online_bjet = true; }
        }
    
        // Which histograms do we need to fill?
        fill_hists.push_back(matches_online_bjet ? PASS_HLT : FAIL_HLT);
        fill_hists.push_back(mevent->jet_bdisc_deepcsv[i] > offline_csv ? PASS_OFF : FAIL_OFF);
        
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
      
    //////////////////////////////////////////////////////////////////////////////
      
    for (int b = 0; b < 100; b++) {
        float b_cut = (b * 0.01)+0.00001;
        int   n_proxies = 0; // Number of jets passing whatever the proxy is
        int   n_passes  = 0; // Number of jets matching to an HLT bjet
        int n_online_bjets = mevent->hlt_pfforbtag_jet_pt.size();
    
        for (int i = 0; i < mevent->njets(); i++) {
            float b_disc = (i < (int)(mevent->jet_bdisc_deepcsv.size()) ? mevent->jet_bdisc_deepcsv[i] : -9.9);
            if (b_disc < 0.0 or mevent->nth_jet_pt(i) < 30.0) continue;
            if (b_disc > b_cut) n_proxies++;
      
            float off_eta = mevent->nth_jet_eta(i);
            float off_phi = mevent->nth_jet_phi(i);
      
            for (int j=0; j < n_online_bjets; j++) {
                float hlt_eta = mevent->hlt_pfforbtag_jet_eta[j];
                float hlt_phi = mevent->hlt_pfforbtag_jet_phi[j];
                if(reco::deltaR(hlt_eta, hlt_phi, off_eta, off_phi) < 0.14) n_passes++;
            }
        }
    
        float y_bin  = n_proxies >= 3 ? 1.0 : 0.0;
        int n_hist = n_online_bjets >= 3 ? 0 : 1;   // If this collection has at least three members, then there's enough HLT bjets to pass
        h_proxy_grid[n_hist]->Fill(b_cut, y_bin, w);
      
    }
}
DEFINE_FWK_MODULE(MFVJetTksHistos);
