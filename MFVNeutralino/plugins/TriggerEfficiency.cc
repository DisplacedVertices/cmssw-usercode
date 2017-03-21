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

class MFVTriggerEfficiency : public edm::EDAnalyzer {
public:
  explicit MFVTriggerEfficiency(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  const int require_bits[2]; // HLT then L1
  const bool require_muon;
  const bool require_4jets;
  const double require_ht;
  const edm::EDGetTokenT<std::vector<int>> decisions_tokens[2];
  const edm::EDGetTokenT<pat::MuonCollection> muons_token;
  const StringCutObjectSelector<pat::Muon> muon_selector;
  const edm::EDGetTokenT<pat::JetCollection> jets_token;
  const StringCutObjectSelector<pat::Jet> jet_selector;
  const edm::EDGetTokenT<float> hlt_ht_token;
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

  TH1F* h_ngenjets;
  TH1F* h_genjet_e[11];
  TH1F* h_genjet_pt[11];
  TH1F* h_genjet_eta[11];
  TH1F* h_genjet_phi[11];
  TH1F* h_genjet_ht;
};

MFVTriggerEfficiency::MFVTriggerEfficiency(const edm::ParameterSet& cfg)
  : require_bits{cfg.getParameter<int>("require_hlt"), cfg.getParameter<int>("require_l1")},
    require_muon(cfg.getParameter<bool>("require_muon")),
    require_4jets(cfg.getParameter<bool>("require_4jets")),
    require_ht(cfg.getParameter<double>("require_ht")),
    decisions_tokens{
      consumes<std::vector<int>>(edm::InputTag("mfvTriggerFloats", "HLTdecisions")),
      consumes<std::vector<int>>(edm::InputTag("mfvTriggerFloats", "L1decisions"))
      },
    muons_token(consumes<pat::MuonCollection>(cfg.getParameter<edm::InputTag>("muons_src"))),
    muon_selector(cfg.getParameter<std::string>("muon_cut")),
    jets_token(consumes<pat::JetCollection>(cfg.getParameter<edm::InputTag>("jets_src"))),
    jet_selector(cfg.getParameter<std::string>("jet_cut")),
    hlt_ht_token(consumes<float>(edm::InputTag("mfvTriggerFloats", "ht"))),
    genjets_token(consumes<reco::GenJetCollection>(cfg.getParameter<edm::InputTag>("genjets_src"))),
    use_genjets(cfg.getParameter<edm::InputTag>("genjets_src").label() != "")
{
  // -1 = don't care, ORs represented by negative numbers other than -1
  // -2 = HLT_PFHT800 || PFJet450
  // -3 = HLT_PFHT800 || PFJet450 || AK8PFJet450
  // -4 = HLT_PFHT900 || PFJet450
  // -5 = HLT_PFHT900 || PFJet450 || AK8PFJet450
  assert(require_bits[0] >= -5 && require_bits[0] < mfv::n_hlt_paths);
  assert(require_bits[1] >= -1 && require_bits[0] < mfv::n_l1_paths);

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
  }
  h_jet_ht_all = fs->make<TH1F>("h_jet_ht_all", ";jet (p_{T} > 20 GeV) H_{T} (GeV);events/20 GeV", 250, 0, 5000);
  h_jet_ht = fs->make<TH1F>("h_jet_ht", ";jet (p_{T} > 40 GeV) H_{T} (GeV);events/20 GeV", 250, 0, 5000);
  h_jet_ht_ptlt200 = fs->make<TH1F>("h_jet_ht_ptlt200", ";jet (40 < p_{T} < 200 GeV) H_{T} (GeV);events/20 GeV", 250, 0, 5000);
  h_jet_ht_m_hlt_ht = fs->make<TH1F>("h_jet_ht_m_hlt_ht", ";offline jet (p_{T} > 40 GeV) H_{T} - HLT H_{T} (GeV);events/10 GeV", 100, -500, 500);
  h_njets_v_ht = fs->make<TH2F>("h_njets_v_ht", ";jet (p_{T} > 40 GeV) H_{T} (GeV);# selected jets", 50, 0, 2000, 15, 0, 15);

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
}

void MFVTriggerEfficiency::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  for (int i = 0; i < 2; ++i) { // HLT then L1
    const int r = require_bits[i];
    if (r == -1)
      continue;

    edm::Handle<std::vector<int>> decisions;
    event.getByToken(decisions_tokens[i], decisions);

    if (i == 0 && r < 0) {
      if ((r == -2 && !orem(*decisions, {1,3})) ||
          (r == -3 && !orem(*decisions, {1,3,4})) ||
          (r == -4 && !orem(*decisions, {2,3})) ||
          (r == -5 && !orem(*decisions, {2,3,4})))
        return;
    }
    else {
      const int decision = (*decisions)[r];
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

          h_muon_pt[i]->Fill(muon.pt());
          h_muon_eta[i]->Fill(muon.eta());
          h_muon_phi[i]->Fill(muon.phi());
          h_muon_iso[i]->Fill((muon.chargedHadronIso() + muon.neutralHadronIso() + muon.photonIso() - 0.5*muon.puChargedHadronIso())/muon.pt());
        }
      }
    }

    h_nnoselmuons->Fill(nmuons[0]);
    h_nmuons->Fill(nmuons[1]);

    if (nmuons[1] < 1)
      return;
  }

  edm::Handle<pat::JetCollection> jets;
  event.getByToken(jets_token, jets);

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

  h_nnoseljets->Fill(jets->size());

  int njet = 0;
  double jet_ht_all = 0;
  double jet_ht = 0;
  double jet_ht_ptlt200 = 0;
  for (const pat::Jet& jet : *jets) {
    if (jet_selector(jet)) {
      ++njet;
      jet_ht_all += jet.pt();
      if (jet.pt() > 40) {
        jet_ht += jet.pt();
        if (jet.pt() < 200)
          jet_ht_ptlt200 += jet.pt();
      }

      for (int i : {0, njet}) {
        if (i == 0 || njet < 11) {
          h_jet_e[i]->Fill(jet.energy());
          h_jet_pt[i]->Fill(jet.pt());
          h_jet_eta[i]->Fill(jet.eta());
          h_jet_phi[i]->Fill(jet.phi());
          h_jet_muef[i]->Fill(jet.muonEnergyFraction());
        }
      }
    }
  }

  h_njets->Fill(njet);
  h_jet_ht_all->Fill(jet_ht_all);
  h_jet_ht->Fill(jet_ht);
  h_jet_ht_ptlt200->Fill(jet_ht_ptlt200);
  h_njets_v_ht->Fill(jet_ht, njet);

  edm::Handle<float> hlt_ht;
  event.getByToken(hlt_ht_token, hlt_ht);
  h_jet_ht_m_hlt_ht->Fill(jet_ht - *hlt_ht); 

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
            h_genjet_e[i]->Fill(genjet.energy());
            h_genjet_pt[i]->Fill(genjet.pt());
            h_genjet_eta[i]->Fill(genjet.eta());
            h_genjet_phi[i]->Fill(genjet.phi());
          }
        }
      }
    }

    h_ngenjets->Fill(ngenjet);
    h_genjet_ht->Fill(genjet_ht);
  }
}

DEFINE_FWK_MODULE(MFVTriggerEfficiency);
