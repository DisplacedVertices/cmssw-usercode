#include "TH2.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "PhysicsTools/SelectorUtils/interface/JetIDSelectionFunctor.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/TriggerFloats.h"

class MFVTriggerEfficiency : public edm::EDAnalyzer {
public:
  explicit MFVTriggerEfficiency(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  const int use_jetpt_weights;
  const int require_bits[2]; // HLT then L1
  const bool require_muon;
  const bool require_electron;
  const bool do_ttbar_selection;
  const bool require_2jets;
  const bool require_4jets;
  const bool require_6jets;
  const double require_1stjetpt;
  const double require_2ndjetpt;
  const double require_3rdjetpt;
  const double require_4thjetpt;
  const double require_6thjetpt;
  const double require_maxdeta1p6pt;
  const double require_maxdeta1p6maxeta;
  const double min_bjet_pt;
  const double max_bjet_eta;
  const bool require_2btags;
  const bool require_3btags;
  const double require_ht;
  const double require_ht30;
  const bool require_trig_match_all;
  const int require_trig_match_nm1_idx;
  const edm::EDGetTokenT<double> weight_token;
  const edm::EDGetTokenT<mfv::TriggerFloats> triggerfloats_token;
  const edm::EDGetTokenT<pat::MuonCollection> muons_token;
  const StringCutObjectSelector<pat::Muon> muon_selector;
  const edm::EDGetTokenT<pat::ElectronCollection> electrons_token;
  const StringCutObjectSelector<pat::Electron> electron_selector;
  const edm::EDGetTokenT<reco::GenJetCollection> genjets_token;
  const bool use_genjets;


  TH1D* h_w;

  TH1D* h_nnoselmuons;
  TH1D* h_nmuons;
  TH1D* h_muon_pt[2];
  TH1D* h_muon_eta[2];
  TH1D* h_muon_phi[2];
  TH1D* h_muon_iso[2];

  TH1D* h_nnoselelectrons;
  TH1D* h_nelectrons;
  TH1D* h_electron_pt[2];
  TH1D* h_electron_eta[2];
  TH1D* h_electron_phi[2];
  TH1D* h_electron_iso[2];

  TH1D* h_mue_mass_nosel;
  TH1D* h_mue_mass_OS_only;
  TH1D* h_mue_mass_gt_90;
  TH1D* h_mue_mass_post_sel;

  // FIXME add a plot of mindeta_pt100 (and pt140 or w/e the other trig is?) to verify that the cut is done right?
  TH1D* h_nnoseljets;
  TH1D* h_njets;
  TH1D* h_jet_e[11];
  TH1D* h_jet_pt[11];
  TH1D* h_jet_eta[11];
  TH1D* h_jet_phi[11];
  TH1D* h_jet_muef[11];
  TH1D* h_jet_ht_all;
  TH1D* h_jet_ht;
  TH1D* h_jet_ht30;
  TH1D* h_jet_ht_m_hlt_ht;
  TH2F* h_njets_v_ht;
  TH1D* h_myhtt_m_l1htt;
  TH1D* h_myhttwbug_m_l1htt;
  TH1D* h_l1jet_pt[11];
  TH2F* h_jetpt2v1;

  TH1D* h_nbjets;
  TH1D* h_bjet_e[11];
  TH1D* h_bjet_pt[11];
  TH1D* h_bjet_eta[11];
  TH1D* h_bjet_phi[11];

  TH1D* h_bjet_leg_e;
  TH1D* h_bjet_leg_pt;
  TH1D* h_bjet_leg_eta;
  TH1D* h_bjet_leg_phi;
  TH2D* h_bjet_leg_pt_eta;
  TH2D* h_bjet_leg_phi_eta;

  TH1D* h_ngenjets;
  TH1D* h_genjet_e[11];
  TH1D* h_genjet_pt[11];
  TH1D* h_genjet_eta[11];
  TH1D* h_genjet_phi[11];
  TH1D* h_genjet_ht;
};

MFVTriggerEfficiency::MFVTriggerEfficiency(const edm::ParameterSet& cfg)
  : use_jetpt_weights(cfg.getParameter<int>("use_jetpt_weights")),
    require_bits{cfg.getParameter<int>("require_hlt"), cfg.getParameter<int>("require_l1")},
    require_muon(cfg.getParameter<bool>("require_muon")),
    require_electron(cfg.getParameter<bool>("require_electron")),
    do_ttbar_selection(cfg.getParameter<bool>("do_ttbar_selection")),
    require_2jets(cfg.getParameter<bool>("require_2jets")),
    require_4jets(cfg.getParameter<bool>("require_4jets")),
    require_6jets(cfg.getParameter<bool>("require_6jets")),
    require_1stjetpt(cfg.getParameter<double>("require_1stjetpt")),
    require_2ndjetpt(cfg.getParameter<double>("require_2ndjetpt")),
    require_3rdjetpt(cfg.getParameter<double>("require_3rdjetpt")),
    require_4thjetpt(cfg.getParameter<double>("require_4thjetpt")),
    require_6thjetpt(cfg.getParameter<double>("require_6thjetpt")),
    require_maxdeta1p6pt(cfg.getParameter<double>("require_maxdeta1p6pt")),
    require_maxdeta1p6maxeta(cfg.getParameter<double>("require_maxdeta1p6maxeta")),
    min_bjet_pt(cfg.getParameter<double>("min_bjet_pt")),
    max_bjet_eta(cfg.getParameter<double>("max_bjet_eta")),
    require_2btags(cfg.getParameter<bool>("require_2btags")),
    require_3btags(cfg.getParameter<bool>("require_3btags")),
    require_ht(cfg.getParameter<double>("require_ht")),
    require_ht30(cfg.getParameter<double>("require_ht30")),
    require_trig_match_all(cfg.getParameter<bool>("require_trig_match_all")),
    require_trig_match_nm1_idx(cfg.getParameter<int>("require_trig_match_nm1_idx")),
    weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
    triggerfloats_token(consumes<mfv::TriggerFloats>(edm::InputTag("mfvTriggerFloats"))),
    muons_token(consumes<pat::MuonCollection>(cfg.getParameter<edm::InputTag>("muons_src"))),
    muon_selector(cfg.getParameter<std::string>("muon_cut")),
    electrons_token(consumes<pat::ElectronCollection>(cfg.getParameter<edm::InputTag>("electrons_src"))),
    electron_selector(cfg.getParameter<std::string>("electron_cut")),
    genjets_token(consumes<reco::GenJetCollection>(cfg.getParameter<edm::InputTag>("genjets_src"))),
    use_genjets(cfg.getParameter<edm::InputTag>("genjets_src").label() != "")
{
  assert(use_jetpt_weights >= 0 && use_jetpt_weights <= 2);

  // JMTBAD the bits checking is now duplicated in TriggerFloatsFilter, should understand how to clean that up
  // require_bits:
  // -1 = don't care, ORs or other combinations represented by negative numbers other than -1
  assert(require_bits[0] >= -1 && require_bits[0] < mfv::n_hlt_paths);
  assert(require_bits[1] >= -1 && require_bits[1] < mfv::n_l1_paths);

  edm::Service<TFileService> fs;
  TH1::SetDefaultSumw2();

  h_w = fs->make<TH1D>("h_w", ";event weight;events", 20, 0, 10);

  if (require_muon || do_ttbar_selection) {
    h_nnoselmuons = fs->make<TH1D>("h_nnoselmuons", ";# all muons;events", 5, 0, 5);
    h_nmuons = fs->make<TH1D>("h_nmuons", ";# selected muons;events", 3, 0, 3);
    const char* ex[2] = {"all", "selected"};
    for (int i = 0; i < 2; ++i) {
      h_muon_pt [i] = fs->make<TH1D>(TString::Format("h_muon_pt_%i" , i), TString::Format(";%s muon p_{T} (GeV);events/5 GeV", ex[i]), 200, 0, 1000);
      h_muon_eta[i] = fs->make<TH1D>(TString::Format("h_muon_eta_%i", i), TString::Format(";%s muon #eta;events/0.12", ex[i]), 50, -3, 3);
      h_muon_phi[i] = fs->make<TH1D>(TString::Format("h_muon_phi_%i", i), TString::Format(";%s muon #phi;events/0.125", ex[i]), 50, -M_PI, M_PI);
      h_muon_iso[i] = fs->make<TH1D>(TString::Format("h_muon_iso_%i", i), TString::Format(";%s muon isolation;events/0.04", ex[i]), 50, 0, 2);
    }
  }

  if (require_electron || do_ttbar_selection) {
    h_nnoselelectrons = fs->make<TH1D>("h_nnoselelectrons", ";# all electrons;events", 5, 0, 5);
    h_nelectrons = fs->make<TH1D>("h_nelectrons", ";# selected electrons;events", 3, 0, 3);
    const char* ex[2] = {"all", "selected"};
    for (int i = 0; i < 2; ++i) {
      h_electron_pt [i] = fs->make<TH1D>(TString::Format("h_electron_pt_%i" , i), TString::Format(";%s electron p_{T} (GeV);events/5 GeV", ex[i]), 200, 0, 1000);
      h_electron_eta[i] = fs->make<TH1D>(TString::Format("h_electron_eta_%i", i), TString::Format(";%s electron #eta;events/0.12", ex[i]), 50, -3, 3);
      h_electron_phi[i] = fs->make<TH1D>(TString::Format("h_electron_phi_%i", i), TString::Format(";%s electron #phi;events/0.125", ex[i]), 50, -M_PI, M_PI);
      h_electron_iso[i] = fs->make<TH1D>(TString::Format("h_electron_iso_%i", i), TString::Format(";%s electron isolation;events/0.04", ex[i]), 50, 0, 2);
    }
  }

  h_mue_mass_nosel    = fs->make<TH1D>("h_mue_mass_nosel", "m_{#mue}", 200, 0, 200);
  h_mue_mass_OS_only  = fs->make<TH1D>("h_mue_mass_OS_only", "m_{#mue}", 200, 0, 200);
  h_mue_mass_gt_90    = fs->make<TH1D>("h_mue_mass_gt_90", "m_{#mue}", 200, 0, 200);
  h_mue_mass_post_sel = fs->make<TH1D>("h_mue_mass_post_sel", "m_{#mue}", 200, 0, 200);

  h_nnoseljets = fs->make<TH1D>("h_nnoseljets", ";# all jets;events", 30, 0, 30);
  h_njets = fs->make<TH1D>("h_njets", ";# selected jets;events", 30, 0, 30);
  h_nbjets = fs->make<TH1D>("h_nbjets", ";# selected bjets;events", 30, 0, 30);
  for (int i = 0; i < 11; ++i) {
    char buf[32];
    char buf_bjet[32];
    if (i == 0) {
      snprintf(buf, 32, "all jets");
      snprintf(buf_bjet, 32, "all bjets");
    }
    else {
      snprintf(buf, 32, "jet %i", i);
      snprintf(buf_bjet, 32, "bjet %i", i);
    }
    h_jet_e[i]    = fs->make<TH1D>(TString::Format("h_jet_e_%i",   i),  TString::Format(";%s energy (GeV);events/5 GeV", buf), 200, 0, 1000);
    h_jet_pt[i]   = fs->make<TH1D>(TString::Format("h_jet_pt_%i",  i),  TString::Format(";%s p_{T} (GeV);events/5 GeV", buf), 200, 0, 1000);
    h_jet_eta[i]  = fs->make<TH1D>(TString::Format("h_jet_eta_%i", i),  TString::Format(";%s #eta;events/0.12", buf), 50, -6, 6);
    h_jet_phi[i]  = fs->make<TH1D>(TString::Format("h_jet_phi_%i", i),  TString::Format(";%s #phi;events/0.125", buf), 50, -M_PI, M_PI);
    h_jet_muef[i] = fs->make<TH1D>(TString::Format("h_jet_muef_%i", i), TString::Format(";%s #mu energy fraction;events/0.1", buf), 11, 0, 1.1);

    h_bjet_e[i]    = fs->make<TH1D>(TString::Format("h_bjet_e_%i",   i),  TString::Format(";%s energy (GeV);events/5 GeV", buf_bjet), 200, 0, 1000);
    h_bjet_pt[i]   = fs->make<TH1D>(TString::Format("h_bjet_pt_%i",  i),  TString::Format(";%s p_{T} (GeV);events/5 GeV", buf_bjet), 200, 0, 1000);
    h_bjet_eta[i]  = fs->make<TH1D>(TString::Format("h_bjet_eta_%i", i),  TString::Format(";%s #eta;events/0.12", buf_bjet), 50, -6, 6);
    h_bjet_phi[i]  = fs->make<TH1D>(TString::Format("h_bjet_phi_%i", i),  TString::Format(";%s #phi;events/0.125", buf_bjet), 50, -M_PI, M_PI);

    if (i == 0)
      snprintf(buf, 32, "all L1 jets");
    else
      snprintf(buf, 32, "L1 jet %i", i);
    h_l1jet_pt[i] = fs->make<TH1D>(TString::Format("h_l1jet_pt_%i",  i),  TString::Format(";%s p_{T} (GeV);events/5 GeV", buf), 200, 0, 1000);
  }
  h_bjet_leg_e   = fs->make<TH1D>("h_bjet_leg_e",   ";bjet leg energy (GeV);events/5 GeV", 200, 0, 1000);
  h_bjet_leg_pt  = fs->make<TH1D>("h_bjet_leg_pt",  ";bjet leg p_{T} (GeV);events/5 GeV", 200, 0, 1000);
  h_bjet_leg_eta = fs->make<TH1D>("h_bjet_leg_eta", ";bjet leg #eta;events/0.12", 50, -6, 6);
  h_bjet_leg_phi = fs->make<TH1D>("h_bjet_leg_phi", ";bjet leg #phi;events/0.125",50, -M_PI, M_PI);

  h_bjet_leg_pt_eta  = fs->make<TH2D>("h_bjet_leg_pt_eta",";bjet leg p_{T} (GeV);bjet leg #eta", 200, 0, 1000, 50, -6, 6);
  h_bjet_leg_phi_eta = fs->make<TH2D>("h_bjet_leg_phi_eta",";bjet leg #phi;bjet leg #eta", 50, -M_PI, M_PI, 50, -6, 6);

  h_jet_ht_all = fs->make<TH1D>("h_jet_ht_all", ";jet (p_{T} > 20 GeV) H_{T} (GeV);events/20 GeV", 250, 0, 5000);
  h_jet_ht = fs->make<TH1D>("h_jet_ht", ";jet (p_{T} > 40 GeV) H_{T} (GeV);events/20 GeV", 250, 0, 5000);
  h_jet_ht30 = fs->make<TH1D>("h_jet_ht30", ";jet (p_{T} > 30 GeV) H_{T} (GeV);events/20 GeV", 250, 0, 5000);
  h_jet_ht_m_hlt_ht = fs->make<TH1D>("h_jet_ht_m_hlt_ht", ";offline jet (p_{T} > 40 GeV) H_{T} - HLT H_{T} (GeV);events/10 GeV", 100, -500, 500);
  h_njets_v_ht = fs->make<TH2F>("h_njets_v_ht", ";jet (p_{T} > 40 GeV) H_{T} (GeV);# selected jets", 20, 0, 2000, 15, 0, 15);

  h_myhtt_m_l1htt = fs->make<TH1D>("h_myhtt_m_l1htt", ";my L1 HTT - L1 HTT in event;events/5 GeV", 100, -250, 250);
  h_myhttwbug_m_l1htt = fs->make<TH1D>("h_myhttwbug_m_l1htt", ";my L1 HTT with bug - L1 HTT in event;events/5 GeV", 100, -250, 250);

  {
    const int nx = 5;
    const float xbins[nx+1] = {0, 250, 400, 550, 700, 1000};
    const int ny = 5;
    const float ybins[ny+1] = {0, 150, 250, 400, 600, 1000};
    h_jetpt2v1 = fs->make<TH2F>("h_jetpt2v1", ";jet 1 p_{T} (GeV);jet 2 p_{T} (GeV)", nx, xbins, ny, ybins);
  }

  if (use_genjets) {
    h_ngenjets = fs->make<TH1D>("h_ngenjets", ";# gen jets;events", 30, 0, 30);
    for (int i = 0; i < 11; ++i) {
      char buf[32];
      if (i == 0)
        snprintf(buf, 32, "all gen jets");
      else
        snprintf(buf, 32, "gen jet %i", i);
      h_genjet_e[i]   = fs->make<TH1D>(TString::Format("h_genjet_e_%i",   i), TString::Format(";%s energy (GeV);events/5 GeV", buf), 200, 0, 1000);
      h_genjet_pt[i]  = fs->make<TH1D>(TString::Format("h_genjet_pt_%i",  i), TString::Format(";%s p_{T} (GeV);events/5 GeV", buf), 200, 0, 1000);
      h_genjet_eta[i] = fs->make<TH1D>(TString::Format("h_genjet_eta_%i", i), TString::Format(";%s #eta;events/0.12", buf), 50, -6, 6);
      h_genjet_phi[i] = fs->make<TH1D>(TString::Format("h_genjet_phi_%i", i), TString::Format(";%s #phi;events/0.125", buf), 50, -M_PI, M_PI);
    }
    h_genjet_ht = fs->make<TH1D>("h_genjet_ht", ";gen jet H_{T} (GeV);events/20 GeV", 250, 0, 5000);
  }
}

namespace {
//  bool orem(const std::vector<int>& decisions, std::vector<int> which) {
//    for (int w : which) {
//      const int decision = decisions[w];
//      if (decision == -1) throw cms::Exception("TriggerNotFound") << mfv::hlt_paths[w] << " wasn't found";
//      else if (decision == 1) return true;
//    }
//    return false;
//  }

  double jetpt12_weight_mfvM300(double jetpt1, double jetpt2) {
    if      (jetpt1 >=   0 && jetpt1 < 250 && jetpt2 >=   0 && jetpt2 < 150) return 2.969734e+01;
    else if (jetpt1 >=   0 && jetpt1 < 250 && jetpt2 >= 150 && jetpt2 < 250) return 1.134604e+01;
    else if (jetpt1 >=   0 && jetpt1 < 250 && jetpt2 >= 250 && jetpt2 < 400) return 1.000000e-06;
    else if (jetpt1 >=   0 && jetpt1 < 250 && jetpt2 >= 400 && jetpt2 < 600) return 1.000000e-06;
    else if (jetpt1 >=   0 && jetpt1 < 250 && jetpt2 >= 600                ) return 1.000000e-06;
    else if (jetpt1 >= 250 && jetpt1 < 400 && jetpt2 >=   0 && jetpt2 < 150) return 1.411194e+01;
    else if (jetpt1 >= 250 && jetpt1 < 400 && jetpt2 >= 150 && jetpt2 < 250) return 4.387227e+00;
    else if (jetpt1 >= 250 && jetpt1 < 400 && jetpt2 >= 250 && jetpt2 < 400) return 1.734888e+00;
    else if (jetpt1 >= 250 && jetpt1 < 400 && jetpt2 >= 400 && jetpt2 < 600) return 1.000000e-06;
    else if (jetpt1 >= 250 && jetpt1 < 400 && jetpt2 >= 600                ) return 1.000000e-06;
    else if (jetpt1 >= 400 && jetpt1 < 550 && jetpt2 >=   0 && jetpt2 < 150) return 3.492948e+00;
    else if (jetpt1 >= 400 && jetpt1 < 550 && jetpt2 >= 150 && jetpt2 < 250) return 1.596243e+00;
    else if (jetpt1 >= 400 && jetpt1 < 550 && jetpt2 >= 250 && jetpt2 < 400) return 7.278219e-01;
    else if (jetpt1 >= 400 && jetpt1 < 550 && jetpt2 >= 400 && jetpt2 < 600) return 3.255670e-01;
    else if (jetpt1 >= 400 && jetpt1 < 550 && jetpt2 >= 600                ) return 1.000000e-06;
    else if (jetpt1 >= 550 && jetpt1 < 700 && jetpt2 >=   0 && jetpt2 < 150) return 5.541697e-01;
    else if (jetpt1 >= 550 && jetpt1 < 700 && jetpt2 >= 150 && jetpt2 < 250) return 7.320858e-01;
    else if (jetpt1 >= 550 && jetpt1 < 700 && jetpt2 >= 250 && jetpt2 < 400) return 4.656565e-01;
    else if (jetpt1 >= 550 && jetpt1 < 700 && jetpt2 >= 400 && jetpt2 < 600) return 2.752871e-01;
    else if (jetpt1 >= 550 && jetpt1 < 700 && jetpt2 >= 600                ) return 1.926626e-01;
    else if (jetpt1 >= 700 &&                 jetpt2 >=   0 && jetpt2 < 150) return 3.220271e-02;
    else if (jetpt1 >= 700 &&                 jetpt2 >= 150 && jetpt2 < 250) return 2.955854e-01;
    else if (jetpt1 >= 700 &&                 jetpt2 >= 250 && jetpt2 < 400) return 4.815754e-01;
    else if (jetpt1 >= 700 &&                 jetpt2 >= 400 && jetpt2 < 600) return 4.056667e-01;
    else if (jetpt1 >= 700 &&                 jetpt2 >= 600                ) return 2.262678e-01;
    else
      return -1;
  }

  double jetpt12_weight_mfvM800(double jetpt1, double jetpt2) {
    if      (jetpt1 >=   0 && jetpt1 < 250 && jetpt2 >=   0 && jetpt2 < 150) return 4.665087e+00;
    else if (jetpt1 >=   0 && jetpt1 < 250 && jetpt2 >= 150 && jetpt2 < 250) return 6.253220e+00;
    else if (jetpt1 >=   0 && jetpt1 < 250 && jetpt2 >= 250 && jetpt2 < 400) return 1.000000e-06;
    else if (jetpt1 >=   0 && jetpt1 < 250 && jetpt2 >= 400 && jetpt2 < 600) return 1.000000e-06;
    else if (jetpt1 >=   0 && jetpt1 < 250 && jetpt2 >= 600                ) return 1.000000e-06;
    else if (jetpt1 >= 250 && jetpt1 < 400 && jetpt2 >=   0 && jetpt2 < 150) return 3.818711e+00;
    else if (jetpt1 >= 250 && jetpt1 < 400 && jetpt2 >= 150 && jetpt2 < 250) return 3.262763e+00;
    else if (jetpt1 >= 250 && jetpt1 < 400 && jetpt2 >= 250 && jetpt2 < 400) return 2.321000e+00;
    else if (jetpt1 >= 250 && jetpt1 < 400 && jetpt2 >= 400 && jetpt2 < 600) return 1.000000e-06;
    else if (jetpt1 >= 250 && jetpt1 < 400 && jetpt2 >= 600                ) return 1.000000e-06;
    else if (jetpt1 >= 400 && jetpt1 < 550 && jetpt2 >=   0 && jetpt2 < 150) return 9.482955e-01;
    else if (jetpt1 >= 400 && jetpt1 < 550 && jetpt2 >= 150 && jetpt2 < 250) return 1.022670e+00;
    else if (jetpt1 >= 400 && jetpt1 < 550 && jetpt2 >= 250 && jetpt2 < 400) return 9.130405e-01;
    else if (jetpt1 >= 400 && jetpt1 < 550 && jetpt2 >= 400 && jetpt2 < 600) return 5.669553e-01;
    else if (jetpt1 >= 400 && jetpt1 < 550 && jetpt2 >= 600                ) return 1.000000e-06;
    else if (jetpt1 >= 550 && jetpt1 < 700 && jetpt2 >=   0 && jetpt2 < 150) return 1.783120e-01;
    else if (jetpt1 >= 550 && jetpt1 < 700 && jetpt2 >= 150 && jetpt2 < 250) return 3.696464e-01;
    else if (jetpt1 >= 550 && jetpt1 < 700 && jetpt2 >= 250 && jetpt2 < 400) return 5.048690e-01;
    else if (jetpt1 >= 550 && jetpt1 < 700 && jetpt2 >= 400 && jetpt2 < 600) return 4.840129e-01;
    else if (jetpt1 >= 550 && jetpt1 < 700 && jetpt2 >= 600                ) return 4.077907e-01;
    else if (jetpt1 >= 700 &&                 jetpt2 >=   0 && jetpt2 < 150) return 1.748533e-02;
    else if (jetpt1 >= 700 &&                 jetpt2 >= 150 && jetpt2 < 250) return 1.395618e-01;
    else if (jetpt1 >= 700 &&                 jetpt2 >= 250 && jetpt2 < 400) return 4.457198e-01;
    else if (jetpt1 >= 700 &&                 jetpt2 >= 400 && jetpt2 < 600) return 5.939362e-01;
    else if (jetpt1 >= 700 &&                 jetpt2 >= 600                ) return 4.430860e-01;
    else
      return -1;
  }
}

void MFVTriggerEfficiency::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<double> weight;
  event.getByToken(weight_token, weight);
  double w = *weight;

  edm::Handle<mfv::TriggerFloats> triggerfloats;
  event.getByToken(triggerfloats_token, triggerfloats);

  if (use_jetpt_weights) {
    if      (use_jetpt_weights == 1) w *= jetpt12_weight_mfvM300(triggerfloats->jetpt1(), triggerfloats->jetpt2());
    else if (use_jetpt_weights == 2) w *= jetpt12_weight_mfvM800(triggerfloats->jetpt1(), triggerfloats->jetpt2());
  }

  h_w->Fill(w);

  for (int i = 0; i < 2; ++i) { // HLT then L1
    const int r = require_bits[i];
    if (r == -1)
      continue;

    const std::vector<int>& decisions = i == 0 ? triggerfloats->HLTdecisions : triggerfloats->L1decisions;

/*  if (i == 0 && r < 0) {
      if ((r == -2 && !orem(decisions, {mfv::b_HLT_PFHT800, mfv::b_HLT_PFJet450})) ||
          (r == -3 && !orem(decisions, {mfv::b_HLT_PFHT800, mfv::b_HLT_PFJet450, mfv::b_HLT_AK8PFJet450})) ||
          (r == -4 && !orem(decisions, {mfv::b_HLT_PFHT900, mfv::b_HLT_PFJet450})) ||
          (r == -5 && !orem(decisions, {mfv::b_HLT_PFHT900, mfv::b_HLT_PFJet450, mfv::b_HLT_AK8PFJet450})))
        return;
    }
    else if (i == 1 && r < 0) {
      const double thresholds[5] = {240, 255, 280, 300, 320};
      if (triggerfloats->myhttwbug < thresholds[-r-2])
        return;
    }
    else */ {
      const int decision = decisions[r];
      if (decision == -1)
        throw cms::Exception("TriggerNotFound") << (i == 0 ? "HLT" : "L1") << " bit " << r << " wasn't found";
      else if (decision == 0)
        return;
    }
  }

  // ttbar selection requires exactly e+mu events
  bool require_exactly_one_muon = do_ttbar_selection;
  bool require_exactly_one_electron = do_ttbar_selection;

  if (require_muon || do_ttbar_selection) {
    edm::Handle<pat::MuonCollection> muons;
    event.getByToken(muons_token, muons);

    int nmuons[2] = {0};
    for (const pat::Muon& muon : *muons) {
      for (int i = 0; i < 2; ++i) {
        if (i == 0 || muon_selector(muon)) {
          ++nmuons[i];
          h_muon_pt[i]->Fill(muon.pt(), w);
          h_muon_eta[i]->Fill(muon.eta(), w);
          h_muon_phi[i]->Fill(muon.phi(), w);
          h_muon_iso[i]->Fill((muon.chargedHadronIso() + muon.neutralHadronIso() + muon.photonIso() - 0.5*muon.puChargedHadronIso())/muon.pt(), w);
        }
      }
    }

    h_nnoselmuons->Fill(nmuons[0], w);
    h_nmuons->Fill(nmuons[1], w);

    if (nmuons[1] < 1)
      return;
    if (require_exactly_one_muon && nmuons[1] != 1)
      return;
  }

  if (require_electron || do_ttbar_selection) {
    edm::Handle<pat::ElectronCollection> electrons;
    event.getByToken(electrons_token, electrons);

    int nelectrons[2] = {0};
    for (const pat::Electron& electron : *electrons) {
      for (int i = 0; i < 2; ++i) {
        if (i == 0 || electron_selector(electron)) {
          ++nelectrons[i];
          h_electron_pt[i]->Fill(electron.pt(), w);
          h_electron_eta[i]->Fill(electron.eta(), w);
          h_electron_phi[i]->Fill(electron.phi(), w);
          h_electron_iso[i]->Fill((electron.chargedHadronIso() + electron.neutralHadronIso() + electron.photonIso() - 0.5*electron.puChargedHadronIso())/electron.pt(), w);
        }
      }
    }

    h_nnoselelectrons->Fill(nelectrons[0], w);
    h_nelectrons->Fill(nelectrons[1], w);

    if (nelectrons[1] < 1)
      return;
    if (require_exactly_one_electron && nelectrons[1] != 1)
      return;
  }

  bool passed_ttbar_selection = false;

  edm::Handle<pat::MuonCollection> muons;
  event.getByToken(muons_token, muons);

  edm::Handle<pat::ElectronCollection> electrons;
  event.getByToken(electrons_token, electrons);

  for (const pat::Muon& muon : *muons) {
    if (!muon_selector(muon)) continue;

    for( const pat::Electron& electron : *electrons) {
      if (!electron_selector(electron)) continue;

      double mue_mass = (muon.p4() + electron.p4()).M();
      h_mue_mass_nosel->Fill(mue_mass);

      // only use opposite sign events
      if (muon.charge() == electron.charge()) continue;
      h_mue_mass_OS_only->Fill(mue_mass);

      // avoid Z->bb background
      if(mue_mass < 90) continue;
      h_mue_mass_gt_90->Fill(mue_mass);

      passed_ttbar_selection = true;
    }
  }
    
    if (do_ttbar_selection && !passed_ttbar_selection) return;

  if (
      (require_2jets && triggerfloats->njets(20) < 2) ||
      (require_4jets && triggerfloats->njets(20) < 4) ||
      (require_6jets && triggerfloats->njets(20) < 6) ||
      (require_1stjetpt > 0 && (triggerfloats->njets(20) < 1 || triggerfloats->jets[0].Pt() < require_1stjetpt)) || 
      (require_2ndjetpt > 0 && (triggerfloats->njets(20) < 2 || triggerfloats->jets[1].Pt() < require_2ndjetpt)) || 
      (require_3rdjetpt > 0 && (triggerfloats->njets(20) < 3 || triggerfloats->jets[2].Pt() < require_3rdjetpt)) || 
      (require_4thjetpt > 0 && (triggerfloats->njets(20) < 4 || triggerfloats->jets[3].Pt() < require_4thjetpt)) || 
      (require_6thjetpt > 0 && (triggerfloats->njets(20) < 6 || triggerfloats->jets[5].Pt() < require_6thjetpt)) ||
      (require_ht > 0 && triggerfloats->ht < require_ht) ||
      (require_ht30 > 0 && triggerfloats->htptgt30 < require_ht30)
    )
    return;

  int nbtags = triggerfloats->nbjets(min_bjet_pt, max_bjet_eta);
  int min_nbtags = 0;
  if      (require_3btags) min_nbtags = 3;
  else if (require_2btags) min_nbtags = 2;
  if (nbtags < min_nbtags) return;

  std::vector<int> bjet_indices = {};
  if (require_trig_match_all || require_trig_match_nm1_idx != -1) {

    int nbtags_trigmatched = 0;
    int min_nbtags_trigmatched = 0;
    if      (require_trig_match_all)           min_nbtags_trigmatched = min_nbtags;
    else if (require_trig_match_nm1_idx != -1) min_nbtags_trigmatched = min_nbtags-1;

    for (int ijet = 0; ijet < triggerfloats->njets(); ++ijet) {

      if (triggerfloats->jets[ijet].Pt() > min_bjet_pt && triggerfloats->tight_btag[ijet]) {
        if (max_bjet_eta > 0 && fabs(triggerfloats->jets[ijet].Eta()) > max_bjet_eta) continue;
        bjet_indices.push_back(ijet);
      }
    }

    // careful! ibjet here is the bjet indexing, while ijet is the index from before
    for (unsigned int ibjet = 0; ibjet < bjet_indices.size(); ++ibjet) {

      // skip our n-1 index
      if ( (int) ibjet == require_trig_match_nm1_idx) continue;

      // stop once we have enough trigmatched bjets
      if (nbtags_trigmatched >= min_nbtags_trigmatched) continue;

      int ijet = bjet_indices.at(ibjet);
      if (!triggerfloats->isTrigMatched[ijet]) return;

      ++nbtags_trigmatched;
    }
  }

  if (require_maxdeta1p6pt > 0) {

    bool satisfies_maxdeta1p6 = false;

    for (int ijet = 0; ijet < triggerfloats->njets(); ++ijet) {
      if (triggerfloats->jets[ijet].Pt() < require_maxdeta1p6pt) continue;
      if (require_maxdeta1p6maxeta > 0 && fabs(triggerfloats->jets[ijet].Eta()) > require_maxdeta1p6maxeta) continue;

      for (int jjet = 0; jjet < triggerfloats->njets(); ++jjet) {
        if (triggerfloats->jets[jjet].Pt() < require_maxdeta1p6pt) continue;
        if (require_maxdeta1p6maxeta > 0 && fabs(triggerfloats->jets[jjet].Eta()) > require_maxdeta1p6maxeta) continue;

        if (fabs(triggerfloats->jets[ijet].Eta() - triggerfloats->jets[jjet].Eta()) < 1.6) 
          satisfies_maxdeta1p6 = true;
      }
    }

    if (!satisfies_maxdeta1p6) return;
  }

  // Post-selection m_mue plots
  for (const pat::Muon& muon : *muons) {
    if (!muon_selector(muon)) continue;

    for( const pat::Electron& electron : *electrons) {
      if (!electron_selector(electron)) continue;

      double mue_mass = (muon.p4() + electron.p4()).M();
      h_mue_mass_post_sel->Fill(mue_mass);
    }
  }

  h_nnoseljets->Fill(triggerfloats->nalljets, w);

  int ibjet = 0; 
  for (int ijet = 0; ijet < triggerfloats->njets(); ++ijet) {

    for (int i : {0, ijet+1}) {
      if (i == 0 || ijet < 10) {
        h_jet_e[i]->Fill(triggerfloats->jets[ijet].E(), w);
        h_jet_pt[i]->Fill(triggerfloats->jets[ijet].Pt(), w);
        h_jet_eta[i]->Fill(triggerfloats->jets[ijet].Eta(), w);
        h_jet_phi[i]->Fill(triggerfloats->jets[ijet].Phi(), w);
        h_jet_muef[i]->Fill(triggerfloats->jetmuef[ijet], w);
      }
    }

    if (triggerfloats->jets[ijet].Pt() > min_bjet_pt && triggerfloats->tight_btag[ijet]) {
      if (max_bjet_eta > 0 && fabs(triggerfloats->jets[ijet].Eta()) > max_bjet_eta) continue;

      for (int i : {0, ibjet+1}) {
        if (i == 0 || ibjet < 10) {
          h_bjet_e[i]->Fill(triggerfloats->jets[ijet].E(), w);
          h_bjet_pt[i]->Fill(triggerfloats->jets[ijet].Pt(), w);
          h_bjet_eta[i]->Fill(triggerfloats->jets[ijet].Eta(), w);
          h_bjet_phi[i]->Fill(triggerfloats->jets[ijet].Phi(), w);
        }
      }
      ++ibjet;
    }
  }

  // plots for the bjet nm1 index (aka the leg we're measuring)
  if (require_trig_match_nm1_idx != -1) {
    int ijet = bjet_indices.at(require_trig_match_nm1_idx);
    h_bjet_leg_e->Fill(triggerfloats->jets[ijet].E(), w);
    h_bjet_leg_pt->Fill(triggerfloats->jets[ijet].Pt(), w);
    h_bjet_leg_eta->Fill(triggerfloats->jets[ijet].Eta(), w);
    h_bjet_leg_phi->Fill(triggerfloats->jets[ijet].Phi(), w);

    h_bjet_leg_pt_eta->Fill(triggerfloats->jets[ijet].Pt(), triggerfloats->jets[ijet].Eta(), w);
    h_bjet_leg_phi_eta->Fill(triggerfloats->jets[ijet].Phi(), triggerfloats->jets[ijet].Eta(), w);
  }

  h_njets->Fill(triggerfloats->njets(20), w);
  h_nbjets->Fill(triggerfloats->nbjets(min_bjet_pt, max_bjet_eta), w);
  h_jet_ht_all->Fill(triggerfloats->htall, w);
  h_jet_ht->Fill(triggerfloats->ht, w);
  h_jet_ht30->Fill(triggerfloats->htptgt30, w);
  h_njets_v_ht->Fill(triggerfloats->ht, triggerfloats->njets(20), w);
  h_myhtt_m_l1htt->Fill(triggerfloats->myhtt - triggerfloats->l1htt, w);
  h_myhttwbug_m_l1htt->Fill(triggerfloats->myhttwbug - triggerfloats->l1htt, w);
  h_jetpt2v1->Fill(triggerfloats->jetpt1(), triggerfloats->jetpt2(), w);
  h_jet_ht_m_hlt_ht->Fill(triggerfloats->ht - triggerfloats->hltht, w); 

  for (int il1jet = 0; il1jet < triggerfloats->nl1jets(); ++il1jet)
    for (int i : {0, il1jet+1})
      if (i == 0 || il1jet < 10)
        h_l1jet_pt[i]->Fill(triggerfloats->l1jets[il1jet].Pt(), w);


  if (use_genjets) {
    edm::Handle<reco::GenJetCollection> genjets;
    event.getByToken(genjets_token, genjets);

    int ngenjet = 0;
    double genjet_ht = 0;
    for (const reco::GenJet& genjet : *genjets) {
      if (genjet.pt() > 20 && fabs(genjet.eta()) < 2.5) {
        ++ngenjet;
        genjet_ht += genjet.pt();

        for (int i : {0, ngenjet}) {
          if (i == 0 || ngenjet < 11) {
            h_genjet_e[i]->Fill(genjet.energy(), w);
            h_genjet_pt[i]->Fill(genjet.pt(), w);
            h_genjet_eta[i]->Fill(genjet.eta(), w);
            h_genjet_phi[i]->Fill(genjet.phi(), w);
          }
        }
      }
    }

    h_ngenjets->Fill(ngenjet, w);
    h_genjet_ht->Fill(genjet_ht, w);
  }
}

DEFINE_FWK_MODULE(MFVTriggerEfficiency);
