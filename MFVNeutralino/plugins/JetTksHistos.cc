#include <stdio.h>
#include <math.h>
#include "TH2F.h"
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

class MFVJetTksHistos : public edm::EDAnalyzer {
 public:
  explicit MFVJetTksHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::EDGetTokenT<MFVEvent> mevent_token;
  const edm::EDGetTokenT<double> weight_token;
  const edm::EDGetTokenT<MFVVertexAuxCollection> vertex_token;
  const edm::EDGetTokenT<reco::GenParticleCollection> gen_token;

  static const int CATEGORIES = 5;
  const int ALL      = 0;
  const int PASS_HLT = 1;
  const int FAIL_HLT = 2;
  const int PASS_OFF = 3;
  const int FAIL_OFF = 4;

  static const int CALO_CATEGORIES = 5;
  // const int ALL       = 0;
  const int MATCH_PROMPT = 1;
  const int MISS_PROMPT  = 2;
  const int MATCH_DISP   = 3;
  const int MISS_DISP    = 4;

  const double offline_csv;

  TH1F* h_w;

  TH2F* h_pfjet_pt_2d;
  TH2F* h_pfjet_pt_dpt;
  TH2F* h_pfjet_eta_deta;
  TH2F* h_pfjet_phi_dphi;
  TH1F* h_pfjet_frac_dpt;
  TH1F* h_pfjet_match_dR0;
  TH1F* h_pfjet_match_dR1;
  TH2F* h_off_on_pfht;
  TH2F* h_calojet_pt_2d;
  TH2F* h_calojet_pt_dpt;
  TH2F* h_calojet_pt_n;
  TH2F* h_calojet_eta_deta;
  TH2F* h_calojet_phi_dphi;
  TH1F* h_calojet_frac_dpt;
  TH1F* h_calojet_match_dR0;
  TH1F* h_calojet_match_dR1;
  TH1F* h_calojet_pfjet_dR;
  TH2F* h_off_on_caloht;

  TH1F* h_calojet_dxy_den0;
  TH1F* h_calojet_dxy_den1;
  TH1F* h_calojet_dxy_num0;
  TH1F* h_calojet_dxy_num1;

  TH1F* h_jet_pt[CATEGORIES];
  TH1F* h_jet_eta[CATEGORIES];
  TH1F* h_jet_phi[CATEGORIES];
  TH1F* h_jet_dbv[CATEGORIES];
  TH1F* h_jet_skeweta[CATEGORIES];
  TH1F* h_jet_skewphi[CATEGORIES];
  TH1F* h_jet_skew_dR[CATEGORIES];
  TH1F* h_jet_ntks[CATEGORIES];
  TH1F* h_jet_bdisc_deepflav[CATEGORIES];
  TH1F* h_jet_bdisc_deepcsv[CATEGORIES];

  TH1F* h_calojet_ngood;
  TH1F* h_calojet_pt[CALO_CATEGORIES];
  TH1F* h_calojet_eta[CALO_CATEGORIES];
  TH1F* h_calojet_phi[CALO_CATEGORIES];
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
    gen_token(consumes<reco::GenParticleCollection>(cfg.getParameter<edm::InputTag>("gen_src"))),
    offline_csv(cfg.getParameter<double>("offline_csv"))

{
  edm::Service<TFileService> fs;

  h_w = fs->make<TH1F>("h_w", ";event weight;events/0.1", 100, 0, 10);
 
  h_pfjet_pt_2d      = fs->make<TH2F>("h_pfjet_pt_2d",      ";p_{T} of offline pfjets w/ match @ HLT; p_{T} matching HLT jet", 200, 0, 800, 200, 0, 800);
  h_pfjet_pt_dpt     = fs->make<TH2F>("h_pfjet_pt_dpt",     ";p_{T} of offline pfjets w/ match @ HLT; p_{T}(offline) - p_{T}(online)", 200, 0, 800, 100, -100, 100); 
  h_pfjet_eta_deta   = fs->make<TH2F>("h_pfjet_eta_deta",   ";#eta of offline pfjets w/ match @ HLT; #eta(offline) - #eta(online)", 100, -2.5, 2.5, 40, -0.2, 0.2);
  h_pfjet_phi_dphi   = fs->make<TH2F>("h_pfjet_phi_dphi",   ";#phi of offline pfjets w/ match @ HLT; #phi(offline) - #eta(online)", 63, -M_PI, M_PI, 63, -M_PI, M_PI);
  h_pfjet_frac_dpt   = fs->make<TH1F>("h_pfjet_frac_dpt",   ";(p_{T}(offline) - p_{T}(HLT))/p_{T}(offline); entries", 120, -3.0, 3.0);
  h_pfjet_match_dR0  = fs->make<TH1F>("h_pfjet_match_dR0",  ";#DeltaR between offline pfjet and closest HLT match;entries",     100, 0, 2.0);
  h_pfjet_match_dR1  = fs->make<TH1F>("h_pfjet_match_dR1",  ";#DeltaR between offline pfjet and 2nd-closest HLT match;entries", 100, 0, 2.0);
  h_off_on_pfht      = fs->make<TH2F>("h_off_on_pfht",      ";Offline PFHT(30); Offline PFHT(30) - Online PFHT(30)", 300, 0, 1500, 300, -750, 750);
  h_calojet_pt_2d    = fs->make<TH2F>("h_calojet_pt_2d",    ";p_{T} of offline calojets w/ match @ HLT; p_{T} matching HLT jet", 200, 0, 800, 200, 0, 800);
  h_calojet_pt_dpt   = fs->make<TH2F>("h_calojet_pt_dpt",   ";p_{T} of offline calojets w/ match @ HLT; p_{T}(offline) - p_{T}(online)", 200, 0, 800, 100, -100, 100);
  h_calojet_pt_n     = fs->make<TH2F>("h_calojet_pt_n",     ";p_{T} of offline calojets; # of calojets in event within p_{T} range", 7, 50, 750, 15, -0.5, 14.5);
  h_calojet_eta_deta = fs->make<TH2F>("h_calojet_eta_deta", ";#eta of offline calojets w/ match @ HLT; #eta(offline) - #eta(online)", 100, -2.5, 2.5, 40, -0.2, 0.2);
  h_calojet_phi_dphi = fs->make<TH2F>("h_calojet_phi_dphi", ";#phi of offline calojets w/ match @ HLT; #phi(offline) - #eta(online)", 63, -M_PI, M_PI, 63, -M_PI, M_PI);
  h_calojet_frac_dpt = fs->make<TH1F>("h_calojet_frac_dpt", ";(p_{T}(offline) - p_{T}(HLT))/p_{T}(offline); entries", 120, -3.0, 3.0);
  h_calojet_match_dR0  = fs->make<TH1F>("h_calojet_match_dR0",  ";#DeltaR between offline calojet and closest HLT match;entries",     100, 0, 2.0);
  h_calojet_match_dR1  = fs->make<TH1F>("h_calojet_match_dR1",  ";#DeltaR between offline calojet and 2nd-closest HLT match;entries", 100, 0, 2.0);
  h_calojet_pfjet_dR   = fs->make<TH1F>("h_calojet_pfjet_dR",   ";#DeltaR between offline calojet and closest offline pfjet; entries", 125, -0.5, 2.0);
  h_off_on_caloht      = fs->make<TH2F>("h_off_on_caloht",      ";Offline CaloHT(30); Offline CaloHT(30) - Online CaloHT(30)", 300, 0, 1500, 300, -750, 750);

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
    h_jet_skeweta[i] = fs->make<TH1F>(TString::Format("h_jet_skeweta_%s", bres.Data()), TString::Format(";#Delta#eta(jet, disp) for jets that %s b-tag;events/bin", bres.Data()), 120, 0, 3.0); // Original nBins = 120
    h_jet_skewphi[i] = fs->make<TH1F>(TString::Format("h_jet_skewphi_%s", bres.Data()), TString::Format(";#Delta#phi(jet, disp) for jets that %s b-tag;events/bin", bres.Data()), 100, -3.1416, 3.1416);
    h_jet_skew_dR[i] = fs->make<TH1F>(TString::Format("h_jet_skew_dR_%s", bres.Data()), TString::Format(";#DeltaR(jet, disp) for jets that %s b-tag;events/bin", bres.Data()), 100, 0, 1.6); // Original nBins = 100
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

  h_calojet_ngood = fs->make<TH1F>("h_calojet_ngood", "; # of good offline calojets; entries", 20, 0, 20);
  for (int i = 0; i < CALO_CATEGORIES; ++i) {
    TString bres = i == 4 ? TString("miss_disp") : (i == 3 ? TString("match_disp") : (i == 2 ? TString("miss_prompt") : (i == 1 ? TString("match_prompt") : "all")));
    h_calojet_pt[i] = fs->make<TH1F>(TString::Format("h_calojet_pt_%s", bres.Data()), TString::Format(";p_{T} of calojets that %s (GeV);events/10 GeV", bres.Data()), 200, 0, 800);
    h_calojet_eta[i] = fs->make<TH1F>(TString::Format("h_calojet_eta_%s", bres.Data()), TString::Format(";absv#eta of calojets that %s;events/bin", bres.Data()), 120, 0, 2.5);
    h_calojet_phi[i] = fs->make<TH1F>(TString::Format("h_calojet_phi_%s", bres.Data()), TString::Format(";#phi of calojets that %s;events/bin", bres.Data()), 100, -3.1416, 3.1416);
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
    float dzerr  = -9.9;
    float drz    = -9.9;
    float drzerr = -9.9;
};

struct Jet_Loc_Helper {
    float vtx_jet_pt  = -9.9;
    float vtx_jet_eta = -9.9;
    float vtx_jet_phi = -9.9;
    float vtx_pt   = -9.9;
    float vtx_eta  = -9.9;
    float vtx_phi  = -9.9;
    float vtx_dx  = -9.9;
    float vtx_dy  = -9.9;
    float vtx_dz  = -9.9;
};

void MFVJetTksHistos::analyze(const edm::Event& event, const edm::EventSetup&) {
      
    edm::Handle<MFVEvent> mevent;
    event.getByToken(mevent_token, mevent);
  
    edm::Handle<reco::GenParticleCollection> gen_particles;
    event.getByToken(gen_token, gen_particles);
  
    edm::Handle<double> weight;
    event.getByToken(weight_token, weight);

    edm::Handle<MFVVertexAuxCollection> auxes;
    event.getByToken(vertex_token, auxes);
    const int nsv = int(auxes->size());
  
    const double w = *weight;
    int    calojet_ngood  = 0;
    double online_pfht    = 0.0;
    double online_caloht  = 0.0;
    double offline_pfht   = 0.0;
    double offline_caloht = 0.0;
    h_w->Fill(w);
  
    const size_t n_vertex_seed_tracks = mevent->n_vertex_seed_tracks();
    std::vector<int>    jet_pt_bin_counts{  0  ,  0  ,  0  ,  0  ,  0  ,  0  ,  0  };
    std::vector<double> jet_pt_bin_holders{100., 200., 300., 400., 500., 600., 700.};

    std::vector<Jet_Loc_Helper> jet_loc_helper;
    for (int isv = 0; isv < nsv; isv++) {
        const MFVVertexAux& aux = auxes->at(isv);

        // The index [0] indicates that we're using ntracks to assoc.
        // a jet to a vertex. No need to worry about this right now.
        const std::vector<float> my_pts  = aux.jet_pt[0];
        const std::vector<float> my_etas = aux.jet_eta[0];
        const std::vector<float> my_phis = aux.jet_phi[0];
        int npt = int(my_pts.size());

        for (int ij=0; ij < npt; ij++) {
            Jet_Loc_Helper tmp_loc_helper;
            tmp_loc_helper.vtx_jet_pt  = my_pts[ij];
            tmp_loc_helper.vtx_jet_eta = my_etas[ij];
            tmp_loc_helper.vtx_jet_phi = my_phis[ij];

            // The index [2] indicates use tracks+jet to get pt/eta/phi
            tmp_loc_helper.vtx_pt  = aux.pt[2];
            tmp_loc_helper.vtx_eta = aux.eta[2];
            tmp_loc_helper.vtx_phi = aux.phi[2];

            tmp_loc_helper.vtx_dx  = aux.x - mevent->bsx_at_z(aux.z);
            tmp_loc_helper.vtx_dy  = aux.y - mevent->bsy_at_z(aux.z);
            tmp_loc_helper.vtx_dz  = aux.z - mevent->bsz;
            
            jet_loc_helper.push_back(tmp_loc_helper);
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


    // Get closest online/offline calojet match and calculate on/off caloht
    for (int i = 0, ie=mevent->calo_jet_pt.size(); i < ie; ++i) {
        double closest_dR = 0.2;
        double second_dR  = 11.11;
        int closest_idx = -9;

        if ((mevent->calo_jet_pt[i] > 40.0) and (fabs(mevent->calo_jet_eta[i]) < 2.5)) offline_caloht += mevent->calo_jet_pt[i];

        for (int j=0, je=mevent->hlt_calo_jet_pt.size(); j<je; ++j) {
            if ((i == 0) and (mevent->hlt_calo_jet_pt[j] > 40.0) and (fabs(mevent->hlt_calo_jet_eta[j]) < 2.5)) online_caloht += mevent->hlt_calo_jet_pt[i];
            double temp_dR = reco::deltaR(mevent->calo_jet_eta[i], mevent->calo_jet_phi[i], mevent->hlt_calo_jet_eta[j], mevent->hlt_calo_jet_phi[j]);
            if (temp_dR < closest_dR) {
                second_dR   = closest_dR;
                closest_dR  = temp_dR;
                closest_idx = j;
            }
        }
        if (closest_idx == -9) continue;
        h_calojet_match_dR0->Fill(closest_dR, w);
        h_calojet_match_dR1->Fill(second_dR, w);
        h_calojet_frac_dpt->Fill((mevent->calo_jet_pt[i]-mevent->hlt_calo_jet_pt[closest_idx])/mevent->calo_jet_pt[i], w);
        h_calojet_pt_2d->Fill(mevent->calo_jet_pt[i], mevent->hlt_calo_jet_pt[closest_idx], w); 
        h_calojet_pt_dpt->Fill(mevent->calo_jet_pt[i], mevent->calo_jet_pt[i]-mevent->hlt_calo_jet_pt[closest_idx], w); 
        h_calojet_eta_deta->Fill(mevent->calo_jet_eta[i], mevent->calo_jet_eta[i]-mevent->hlt_calo_jet_eta[closest_idx], w); 
        h_calojet_phi_dphi->Fill(mevent->calo_jet_phi[i], mevent->calo_jet_phi[i]-mevent->hlt_calo_jet_phi[closest_idx], w); 

       if (fabs(mevent->calo_jet_eta[i]) < 2.0) {
         int bin = (int)(mevent->calo_jet_pt[i]/100.0);
         if (bin < 0 || bin > (int) (jet_pt_bin_counts.size())) continue;
         jet_pt_bin_counts[bin]++;
       }
    }

    for (int n=0, ne=jet_pt_bin_counts.size(); n<ne; n++) {
      h_calojet_pt_n->Fill(jet_pt_bin_holders[n], jet_pt_bin_counts[n], w);
    }
    
    if (offline_pfht > 10.0 and online_pfht > 10.0) h_off_on_pfht->Fill(offline_pfht, offline_pfht-online_pfht, w);
    if (offline_caloht > 10.0 and online_caloht > 10.0) h_off_on_caloht->Fill(offline_caloht, offline_caloht-online_caloht, w);

    // Start doing some calojet stuff
    for (int i = 0, ie=mevent->calo_jet_pt.size(); i < ie; ++i) {
        std::vector<Track_Helper> calo_trackhelper;
        std::vector<Track_Helper> calo_seedtrackhelper;
        std::vector<int> fill_calo_hists;
        std::vector<float> jettk_dxys;
        std::vector<float> jettk_nsigmadxys;
        std::vector<float> seedtk_dxys;
        std::vector<float> seedtk_nsigmadxys;
        float med_jettk_dxy;
        float med_seedtk_dxy;
        float med_jettk_nsigmadxy;
        float med_seedtk_nsigmadxy;

        fill_calo_hists.push_back(ALL);
        double closest_dR = 9.9;
        int    closest_j  = -10;
        int    calojet_nseedtks = 0;
        int    calojet_njettks = 0;
        bool has_match = false;
        bool good_jet  = ((mevent->calo_jet_pt[i] > 50.0) and (fabs(mevent->calo_jet_eta[i]) < 2.0));

        // Get closest match between online calojet and offline calojet
        for (int j=0, je=mevent->jet_pt.size(); j<je; ++j) {
            double temp_dR = reco::deltaR(mevent->calo_jet_eta[i], mevent->calo_jet_phi[i], mevent->jet_eta[j], mevent->jet_phi[j]);
            if (temp_dR < closest_dR) {
                closest_dR = temp_dR;
                closest_j  = j;
                has_match = true;
            }
        }
        if (good_jet) { h_calojet_pfjet_dR->Fill(has_match ? closest_dR : -0.5, w); }

        // Do some kludge-y filter stuff. First, only run on events/jets that look good enough
        bool   matches_prompt_cjet = false;
        bool   matches_disp_cjet   = false;
        if ( (not good_jet) or offline_caloht < 500.0) continue;

        // Get the number of seed tracks within dR < 0.4
        for (size_t itk = 0; itk < n_vertex_seed_tracks; ++itk) {
            double this_dR = reco::deltaR(mevent->calo_jet_eta[i], mevent->calo_jet_phi[i], mevent->vertex_seed_track_eta[itk], mevent->vertex_seed_track_phi[itk]);
            if (this_dR < 0.5) {
                calojet_nseedtks++;
                seedtk_dxys.push_back(fabs(mevent->vertex_seed_track_dxy[itk]));
                seedtk_nsigmadxys.push_back(fabs(mevent->vertex_seed_track_dxy[itk]/mevent->vertex_seed_track_err_dxy[itk]));
            }
        }

        // Get the number of decent jet tracks within dR < 0.4
        for (size_t itk = 0; itk < mevent->n_jet_tracks_all(); itk++) {
            if (mevent->jet_track_which_jet[itk] != closest_j) continue;
            double this_tk_nsigmadxy = fabs(mevent->jet_track_dxy[itk]/mevent->jet_track_dxy_err[itk]);
            if (fabs(mevent->jet_track_qpt[itk]) < 1.0 or mevent->jet_track_npxhits(itk) < 2 or mevent->jet_track_nhits(itk) < 8) continue;

            double this_dR = reco::deltaR(mevent->calo_jet_eta[i], mevent->calo_jet_phi[i], mevent->jet_track_eta[itk], mevent->jet_track_phi[itk]);
            if (this_dR < 0.5) {
                calojet_njettks++;
                jettk_dxys.push_back(fabs(mevent->jet_track_dxy[itk]));
                jettk_nsigmadxys.push_back(this_tk_nsigmadxy);
            }
        }

        // See if this calojet matches to one which passes the prompt track tag
        for (int j=0, je=mevent->hlt_calo_jet_lowpt_fewprompt_pt.size(); j < je; j++) {
            double test_jet_eta = mevent->hlt_calo_jet_lowpt_fewprompt_eta[j];
            double test_jet_phi = mevent->hlt_calo_jet_lowpt_fewprompt_phi[j];
            if (reco::deltaR(mevent->calo_jet_eta[i], mevent->calo_jet_phi[i], test_jet_eta, test_jet_phi) < 0.14) {
                matches_prompt_cjet = true;
                break;
            }
        }
        
        // See if this calojet matches to one which passes the prompt track tag
        for (int j=0, je=mevent->hlt_calo_jet_lowpt_wdisptks_pt.size(); j < je; j++) {
            double test_jet_eta = mevent->hlt_calo_jet_lowpt_wdisptks_eta[j];
            double test_jet_phi = mevent->hlt_calo_jet_lowpt_wdisptks_phi[j];
            if (reco::deltaR(mevent->calo_jet_eta[i], mevent->calo_jet_phi[i], test_jet_eta, test_jet_phi) < 0.14) {
              matches_disp_cjet = true;
              break;
            }
        }

        fill_calo_hists.push_back(matches_prompt_cjet ? MATCH_PROMPT : MISS_PROMPT);
        fill_calo_hists.push_back(matches_disp_cjet   ? MATCH_DISP   : MISS_DISP);

        // sort vectors by increasing (nsigma)dxy
        std::sort(jettk_dxys.begin(), jettk_dxys.end());
        std::sort(jettk_nsigmadxys.begin(), jettk_nsigmadxys.end());
        std::sort(seedtk_dxys.begin(), seedtk_dxys.end());
        std::sort(seedtk_nsigmadxys.begin(), seedtk_nsigmadxys.end());

        med_jettk_dxy  = (calojet_njettks == 0 ? -0.001 : calojet_njettks % 2 == 1 ? jettk_dxys[calojet_njettks/2] : (jettk_dxys[calojet_njettks/2] + jettk_dxys[calojet_njettks/2] - 1)/2);
        med_seedtk_dxy = (calojet_nseedtks == 0 ? -0.001 : calojet_nseedtks % 2 == 1 ? seedtk_dxys[calojet_nseedtks/2] : (seedtk_dxys[calojet_nseedtks/2] + seedtk_dxys[calojet_nseedtks/2] - 1)/2);
        med_jettk_nsigmadxy  = (calojet_njettks == 0 ? -0.001 : calojet_njettks % 2 == 1 ? jettk_nsigmadxys[calojet_njettks/2] : (jettk_nsigmadxys[calojet_njettks/2] + jettk_nsigmadxys[calojet_njettks/2] - 1)/2);
        med_seedtk_nsigmadxy = (calojet_nseedtks == 0 ? -0.001 : calojet_nseedtks % 2 == 1 ? seedtk_nsigmadxys[calojet_nseedtks/2] : (seedtk_nsigmadxys[calojet_nseedtks/2] + seedtk_nsigmadxys[calojet_nseedtks/2] - 1)/2);

        bool pass_prompt_req   = jettk_dxys.size() >= 3 ? (jettk_dxys[2] > 0.1) : true;
        bool pass_disp_dxy_req = jettk_dxys.size() >= 1 ? (*max_element(std::begin(jettk_dxys), std::end(jettk_dxys)) > 0.05) : false;
        bool pass_disp_sig_req = jettk_nsigmadxys.size() >= 1 ? (*max_element(std::begin(jettk_nsigmadxys), std::end(jettk_nsigmadxys)) > 5.0) : false;
        //bool pass_alt_disp_req = calojet_njettks_dispd >= 1;
        bool pass_low_pt_req       = mevent->calo_jet_pt[i] > 50.0;
        bool pass_big_pt_req       = mevent->calo_jet_pt[i] > 70.0;

        if ((pass_prompt_req and pass_disp_sig_req and pass_disp_dxy_req and pass_low_pt_req) or (pass_prompt_req and pass_big_pt_req and offline_caloht > 700)) calojet_ngood++;

        if (not pass_prompt_req) continue; //FIXME

        for (auto n_hist : fill_calo_hists) {
             h_calojet_pt[n_hist]->Fill(mevent->calo_jet_pt[i], w);
             h_calojet_eta[n_hist]->Fill(fabs(mevent->calo_jet_eta[i]), w);
             h_calojet_phi[n_hist]->Fill(mevent->calo_jet_phi[i], w);
             h_calojet_ntks[n_hist]->Fill(closest_j >= 0 ? (int)(mevent->n_jet_tracks(closest_j)) : -2, w);
             h_calojet_njettks[n_hist]->Fill(calojet_njettks, w);
             h_calojet_nseedtks[n_hist]->Fill(calojet_nseedtks, w);

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
    }
    
    if (offline_caloht > 400) { h_calojet_ngood->Fill(calojet_ngood, w); }

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
        float closest_helper_dR  = 4.0;
        float closest_vtx_eta = -9.0;
        float closest_vtx_phi = -9.0;
        for (auto helper : jet_loc_helper) {
            float temp_dR = reco::deltaR(helper.vtx_jet_eta, helper.vtx_jet_phi, off_eta, off_phi);
            if (temp_dR < closest_helper_dR) {
                closest_helper_dR = temp_dR;
                jet_dbv = std::hypot(helper.vtx_dx, helper.vtx_dy);

                closest_vtx_eta = helper.vtx_eta;
                closest_vtx_phi = helper.vtx_phi;
            }
        }
        float closest_vtx_dR = reco::deltaR(closest_vtx_eta, closest_vtx_phi, off_eta, off_phi);

        // Fill the pre-determined histograms
        for (auto n_hist : fill_hists) {
             h_jet_pt[n_hist]->Fill(mevent->nth_jet_pt(i), w);
             h_jet_eta[n_hist]->Fill(fabs(mevent->nth_jet_eta(i)), w);
             h_jet_phi[n_hist]->Fill(mevent->nth_jet_phi(i), w);
             h_jet_dbv[n_hist]->Fill(jet_dbv, w);
             h_jet_skeweta[n_hist]->Fill(fabs(closest_vtx_eta - off_eta), w);
             h_jet_skewphi[n_hist]->Fill(TVector2::Phi_mpi_pi(closest_vtx_phi - off_phi), w);
             h_jet_skew_dR[n_hist]->Fill(closest_vtx_dR, w);
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
