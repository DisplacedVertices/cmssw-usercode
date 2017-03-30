#include "TH2.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
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

  const int use_weight;
  const int require_bits[2]; // HLT then L1
  const bool require_muon;
  const bool require_4jets;
  const double require_ht;
  const edm::EDGetTokenT<mfv::TriggerFloats> triggerfloats_token;
  const edm::EDGetTokenT<pat::MuonCollection> muons_token;
  const StringCutObjectSelector<pat::Muon> muon_selector;
  const edm::EDGetTokenT<pat::JetCollection> jets_token;
  const StringCutObjectSelector<pat::Jet> jet_selector;
  const edm::EDGetTokenT<reco::GenJetCollection> genjets_token;
  const bool use_genjets;

  TH1F* h_nnoselmuons;
  TH1F* h_nmuons;
  TH1F* h_muon_pt[2];
  TH1F* h_muon_eta[2];
  TH1F* h_muon_phi[2];
  TH1F* h_muon_iso[2];

  TH1F* h_nnoseljets;
  TH1F* h_njets;
  TH1F* h_jet_e[11];
  TH1F* h_jet_pt[11];
  TH1F* h_jet_eta[11];
  TH1F* h_jet_phi[11];
  TH1F* h_jet_muef[11];
  TH1F* h_jet_ht_all;
  TH1F* h_jet_ht;
  TH1F* h_jet_ht_ptlt200;
  TH1F* h_jet_ht_m_hlt_ht;
  TH2F* h_njets_v_ht;
  TH1F* h_myhtt_m_l1htt;
  TH1F* h_myhttwbug_m_l1htt;
  TH1F* h_l1jet_pt[11];
  TH2F* h_jetpt2v1;

  TH1F* h_ngenjets;
  TH1F* h_genjet_e[11];
  TH1F* h_genjet_pt[11];
  TH1F* h_genjet_eta[11];
  TH1F* h_genjet_phi[11];
  TH1F* h_genjet_ht;
};

MFVTriggerEfficiency::MFVTriggerEfficiency(const edm::ParameterSet& cfg)
  : use_weight(cfg.getParameter<int>("use_weight")),
    require_bits{cfg.getParameter<int>("require_hlt"), cfg.getParameter<int>("require_l1")},
    require_muon(cfg.getParameter<bool>("require_muon")),
    require_4jets(cfg.getParameter<bool>("require_4jets")),
    require_ht(cfg.getParameter<double>("require_ht")),
    triggerfloats_token(consumes<mfv::TriggerFloats>(edm::InputTag("mfvTriggerFloats"))),
    muons_token(consumes<pat::MuonCollection>(cfg.getParameter<edm::InputTag>("muons_src"))),
    muon_selector(cfg.getParameter<std::string>("muon_cut")),
    jets_token(consumes<pat::JetCollection>(cfg.getParameter<edm::InputTag>("jets_src"))),
    jet_selector(cfg.getParameter<std::string>("jet_cut")),
    genjets_token(consumes<reco::GenJetCollection>(cfg.getParameter<edm::InputTag>("genjets_src"))),
    use_genjets(cfg.getParameter<edm::InputTag>("genjets_src").label() != "")
{
  assert(use_weight >= 0 && use_weight <= 2);

  // require_bits:
  // -1 = don't care, ORs or other combinations represented by negative numbers other than -1
  // HLT:
  // -2 = HLT_PFHT800 || PFJet450
  // -3 = HLT_PFHT800 || PFJet450 || AK8PFJet450
  // -4 = HLT_PFHT900 || PFJet450
  // -5 = HLT_PFHT900 || PFJet450 || AK8PFJet450
  // L1:
  // -2 = L1 HTT calculation bugged as in 2016H, threshold 240 GeV
  // -3 = ditto, 255 GeV
  // -4 = ditto, 280 GeV
  // -5 = ditto, 300 GeV
  // -6 = ditto, 320 GeV -- probably don't need to do every single one separately but just in case
  assert(require_bits[0] >= -5 && require_bits[0] < mfv::n_hlt_paths);
  assert(require_bits[1] >= -6 && require_bits[1] < mfv::n_l1_paths);

  edm::Service<TFileService> fs;
  TH1::SetDefaultSumw2();

  if (require_muon) {
    h_nnoselmuons = fs->make<TH1F>("h_nnoselmuons", ";# all muons;events", 5, 0, 5);
    h_nmuons = fs->make<TH1F>("h_nmuons", ";# selected muons;events", 3, 0, 3);
    const char* ex[2] = {"all", "selected"};
    for (int i = 0; i < 2; ++i) {
      h_muon_pt [i] = fs->make<TH1F>(TString::Format("h_muon_pt_%i" , i), TString::Format(";%s muon p_{T} (GeV);events/5 GeV", ex[i]), 200, 0, 1000);
      h_muon_eta[i] = fs->make<TH1F>(TString::Format("h_muon_eta_%i", i), TString::Format(";%s muon #eta;events/0.12", ex[i]), 50, -3, 3);
      h_muon_phi[i] = fs->make<TH1F>(TString::Format("h_muon_phi_%i", i), TString::Format(";%s muon #phi;events/0.125", ex[i]), 50, -M_PI, M_PI);
      h_muon_iso[i] = fs->make<TH1F>(TString::Format("h_muon_iso_%i", i), TString::Format(";%s muon isolation;events/0.04", ex[i]), 50, 0, 2);
    }
  }

  h_nnoseljets = fs->make<TH1F>("h_nnoseljets", ";# all jets;events", 30, 0, 30);
  h_njets = fs->make<TH1F>("h_njets", ";# selected jets;events", 30, 0, 30);
  for (int i = 0; i < 11; ++i) {
    char buf[32];
    if (i == 0)
      snprintf(buf, 32, "all jets");
    else
      snprintf(buf, 32, "jet %i", i);
    h_jet_e[i]    = fs->make<TH1F>(TString::Format("h_jet_e_%i",   i),  TString::Format(";%s energy (GeV);events/5 GeV", buf), 200, 0, 1000);
    h_jet_pt[i]   = fs->make<TH1F>(TString::Format("h_jet_pt_%i",  i),  TString::Format(";%s p_{T} (GeV);events/5 GeV", buf), 200, 0, 1000);
    h_jet_eta[i]  = fs->make<TH1F>(TString::Format("h_jet_eta_%i", i),  TString::Format(";%s #eta;events/0.12", buf), 50, -6, 6);
    h_jet_phi[i]  = fs->make<TH1F>(TString::Format("h_jet_phi_%i", i),  TString::Format(";%s #phi;events/0.125", buf), 50, -M_PI, M_PI);
    h_jet_muef[i] = fs->make<TH1F>(TString::Format("h_jet_muef_%i", i), TString::Format(";%s #mu energy fraction;events/0.1", buf), 11, 0, 1.1);

    if (i == 0)
      snprintf(buf, 32, "all L1 jets");
    else
      snprintf(buf, 32, "L1 jet %i", i);
    h_l1jet_pt[i] = fs->make<TH1F>(TString::Format("h_l1jet_pt_%i",  i),  TString::Format(";%s p_{T} (GeV);events/5 GeV", buf), 200, 0, 1000);
  }
  h_jet_ht_all = fs->make<TH1F>("h_jet_ht_all", ";jet (p_{T} > 20 GeV) H_{T} (GeV);events/20 GeV", 250, 0, 5000);
  h_jet_ht = fs->make<TH1F>("h_jet_ht", ";jet (p_{T} > 40 GeV) H_{T} (GeV);events/20 GeV", 250, 0, 5000);
  h_jet_ht_ptlt200 = fs->make<TH1F>("h_jet_ht_ptlt200", ";jet (40 < p_{T} < 200 GeV) H_{T} (GeV);events/20 GeV", 250, 0, 5000);
  h_jet_ht_m_hlt_ht = fs->make<TH1F>("h_jet_ht_m_hlt_ht", ";offline jet (p_{T} > 40 GeV) H_{T} - HLT H_{T} (GeV);events/10 GeV", 100, -500, 500);
  h_njets_v_ht = fs->make<TH2F>("h_njets_v_ht", ";jet (p_{T} > 40 GeV) H_{T} (GeV);# selected jets", 20, 0, 2000, 15, 0, 15);

  h_myhtt_m_l1htt = fs->make<TH1F>("h_myhtt_m_l1htt", ";my L1 HTT - L1 HTT in event;events/5 GeV", 100, -250, 250);
  h_myhttwbug_m_l1htt = fs->make<TH1F>("h_myhttwbug_m_l1htt", ";my L1 HTT with bug - L1 HTT in event;events/5 GeV", 100, -250, 250);

  {
    const int nx = 5;
    const float xbins[nx+1] = {0, 250, 400, 550, 700, 1000};
    const int ny = 5;
    const float ybins[ny+1] = {0, 150, 250, 400, 600, 1000};
    h_jetpt2v1 = fs->make<TH2F>("h_jetpt2v1", ";jet 1 p_{T} (GeV);jet 2 p_{T} (GeV)", nx, xbins, ny, ybins);
  }

  if (use_genjets) {
    h_ngenjets = fs->make<TH1F>("h_ngenjets", ";# gen jets;events", 30, 0, 30);
    for (int i = 0; i < 11; ++i) {
      char buf[32];
      if (i == 0)
        snprintf(buf, 32, "all gen jets");
      else
        snprintf(buf, 32, "gen jet %i", i);
      h_genjet_e[i]   = fs->make<TH1F>(TString::Format("h_genjet_e_%i",   i), TString::Format(";%s energy (GeV);events/5 GeV", buf), 200, 0, 1000);
      h_genjet_pt[i]  = fs->make<TH1F>(TString::Format("h_genjet_pt_%i",  i), TString::Format(";%s p_{T} (GeV);events/5 GeV", buf), 200, 0, 1000);
      h_genjet_eta[i] = fs->make<TH1F>(TString::Format("h_genjet_eta_%i", i), TString::Format(";%s #eta;events/0.12", buf), 50, -6, 6);
      h_genjet_phi[i] = fs->make<TH1F>(TString::Format("h_genjet_phi_%i", i), TString::Format(";%s #phi;events/0.125", buf), 50, -M_PI, M_PI);
    }
    h_genjet_ht = fs->make<TH1F>("h_genjet_ht", ";gen jet H_{T} (GeV);events/20 GeV", 250, 0, 5000);
  }
}

namespace {
  bool orem(const std::vector<int>& decisions, std::vector<int> which) {
    for (int w : which) {
      const int decision = decisions[w];
      if (decision == -1) throw cms::Exception("TriggerNotFound") << mfv::hlt_paths[w] << " wasn't found";
      else if (decision == 1) return true;
    }
    return false;
  }

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
  edm::Handle<pat::JetCollection> jets;
  event.getByToken(jets_token, jets);

  double w = 1;

  if (use_weight) {
    double jet_pt_1 = -1, jet_pt_2 = -1;
    int njet = 0;
    for (const pat::Jet& jet : *jets) {
      if (jet_selector(jet)) {
        ++njet;
        if (njet == 1)
          jet_pt_1 = jet.pt();
        else if (njet == 2) {
          jet_pt_2 = jet.pt();
          break;
        }
      }
    }
    if      (use_weight == 1) w = jetpt12_weight_mfvM300(jet_pt_1, jet_pt_2);
    else if (use_weight == 2) w = jetpt12_weight_mfvM800(jet_pt_1, jet_pt_2);
  }

  edm::Handle<mfv::TriggerFloats> triggerfloats;
  event.getByToken(triggerfloats_token, triggerfloats);

  for (int i = 0; i < 2; ++i) { // HLT then L1
    const int r = require_bits[i];
    if (r == -1)
      continue;

    const std::vector<int>& decisions = i == 0 ? triggerfloats->HLTdecisions : triggerfloats->L1decisions;

    if (i == 0 && r < 0) {
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
    else {
      const int decision = decisions[r];
      if (decision == -1)
        throw cms::Exception("TriggerNotFound") << (i == 0 ? "HLT" : "L1") << " bit " << r << " wasn't found";
      else if (decision == 0)
        return;
    }
  }

  if (require_muon) {
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
  }

  if (require_4jets || require_ht > 0) {
    int njets = 0;
    double ht = 0;
    for (const pat::Jet& jet : *jets)
      if (jet_selector(jet)) {
        ++njets;
        if (jet.pt() > 40)
          ht += jet.pt();
      }

    if ((require_4jets && njets < 4) || (ht < require_ht))
      return;
  }

  h_nnoseljets->Fill(jets->size(), w);

  int njet = 0;
  double jet_ht_all = 0;
  double jet_ht = 0;
  double jet_ht_ptlt200 = 0;
  double jet_pt_1 = 0, jet_pt_2 = 0;
  for (const pat::Jet& jet : *jets) {
    if (jet_selector(jet)) {
      ++njet;
      if (njet == 1)
        jet_pt_1 = jet.pt();
      else if (njet == 2)
        jet_pt_2 = jet.pt();
      jet_ht_all += jet.pt();
      if (jet.pt() > 40) {
        jet_ht += jet.pt();
        if (jet.pt() < 200)
          jet_ht_ptlt200 += jet.pt();
      }

      for (int i : {0, njet}) {
        if (i == 0 || njet < 11) {
          h_jet_e[i]->Fill(jet.energy(), w);
          h_jet_pt[i]->Fill(jet.pt(), w);
          h_jet_eta[i]->Fill(jet.eta(), w);
          h_jet_phi[i]->Fill(jet.phi(), w);
          h_jet_muef[i]->Fill(jet.muonEnergyFraction(), w);
        }
      }
    }
  }

  h_njets->Fill(njet, w);
  h_jet_ht_all->Fill(jet_ht_all, w);
  h_jet_ht->Fill(jet_ht, w);
  h_jet_ht_ptlt200->Fill(jet_ht_ptlt200, w);
  h_njets_v_ht->Fill(jet_ht, njet, w);
  h_myhtt_m_l1htt->Fill(triggerfloats->myhtt - triggerfloats->l1htt);
  h_myhttwbug_m_l1htt->Fill(triggerfloats->myhttwbug - triggerfloats->l1htt);
  h_jetpt2v1->Fill(jet_pt_1, jet_pt_2, w);
  h_jet_ht_m_hlt_ht->Fill(jet_ht - triggerfloats->hltht, w); 

  int nl1jet = 0;
  for (float pt : triggerfloats->l1jetspts) {
    ++nl1jet;
    for (int i : {0, nl1jet})
      if (i == 0 || nl1jet < 11)
        h_l1jet_pt[i]->Fill(pt, w);
  }

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
