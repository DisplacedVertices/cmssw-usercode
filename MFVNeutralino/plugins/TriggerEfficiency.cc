#include "TH2.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "PhysicsTools/SelectorUtils/interface/JetIDSelectionFunctor.h"

class MFVTriggerEfficiency : public edm::EDProducer {
public:
  explicit MFVTriggerEfficiency(const edm::ParameterSet&);

private:
  virtual void produce(edm::Event&, const edm::EventSetup&);

  const int require_bits[2]; // HLT then L1
  const bool require_muon;
  const bool require_4jets;
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
  TH1F* h_jet_e[6];
  TH1F* h_jet_pt[6];
  TH1F* h_jet_eta[6];
  TH1F* h_jet_phi[6];
  TH1F* h_jet_frac_mu[6];
  TH1F* h_jet_muef[6];
  TH1F* h_jet_ht_all;
  TH1F* h_jet_ht;
  TH1F* h_jet_ht_ptlt200;
  TH1F* h_jet_ht_no_mu_fromcand;
  TH1F* h_jet_ht_no_mu;
  TH1F* h_jet_ht_m_hlt_ht;
  TH1F* h_jet_ht_no_mu_m_hlt_ht;
  TH2F* h_njets_v_ht;

  TH1F* h_ngenjets;
  TH1F* h_genjet_e[6];
  TH1F* h_genjet_pt[6];
  TH1F* h_genjet_eta[6];
  TH1F* h_genjet_phi[6];
  TH1F* h_genjet_ht;
};

MFVTriggerEfficiency::MFVTriggerEfficiency(const edm::ParameterSet& cfg)
  : require_bits{cfg.getParameter<int>("require_hlt"), cfg.getParameter<int>("require_l1")},
    require_muon(cfg.getParameter<bool>("require_muon")),
    require_4jets(cfg.getParameter<bool>("require_4jets")),
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
  assert(require_bits[0] >= -1); // ORs will be represented by other negative numbers, not implemented yet
  assert(require_bits[1] >= -1);

  edm::Service<TFileService> fs;
  TH1::SetDefaultSumw2();

  if (require_muon) {
    h_nnoselmuons = fs->make<TH1F>("h_nnoselmuons", "", 5, 0, 5);
    h_nmuons = fs->make<TH1F>("h_nmuons", "", 3, 0, 3);
    for (int i = 0; i < 2; ++i) {
      h_muon_pt [i] = fs->make<TH1F>(TString::Format("h_muon_pt_%i" , i), "", 200, 0, 1000);
      h_muon_eta[i] = fs->make<TH1F>(TString::Format("h_muon_eta_%i", i), "", 50, -3, 3);
      h_muon_phi[i] = fs->make<TH1F>(TString::Format("h_muon_phi_%i", i), "", 50, -M_PI, M_PI);
      h_muon_iso[i] = fs->make<TH1F>(TString::Format("h_muon_iso_%i", i), "", 50, 0, 2);
    }
  }

  h_nnoseljets = fs->make<TH1F>("h_nnoseljets", "", 30, 0, 30);
  h_njets = fs->make<TH1F>("h_njets", "", 30, 0, 30);
  for (int i = 0; i < 6; ++i) {
    h_jet_e[i]   = fs->make<TH1F>(TString::Format("h_jet_e_%i",   i), "", 200, 0, 1000);
    h_jet_pt[i]  = fs->make<TH1F>(TString::Format("h_jet_pt_%i",  i), "", 200, 0, 1000);
    h_jet_eta[i] = fs->make<TH1F>(TString::Format("h_jet_eta_%i", i), "", 50, -6, 6);
    h_jet_phi[i] = fs->make<TH1F>(TString::Format("h_jet_phi_%i", i), "", 50, -M_PI, M_PI);
    h_jet_frac_mu[i] = fs->make<TH1F>(TString::Format("h_jet_frac_mu_%i", i), "", 11, 0, 1.1);
    h_jet_muef[i] = fs->make<TH1F>(TString::Format("h_jet_muef_%i", i), "", 11, 0, 1.1);
  }
  h_jet_ht_all = fs->make<TH1F>("h_jet_ht_all", "", 250, 0, 5000);
  h_jet_ht = fs->make<TH1F>("h_jet_ht", "", 250, 0, 5000);
  h_jet_ht_ptlt200 = fs->make<TH1F>("h_jet_ht_ptlt200", "", 250, 0, 5000);
  h_jet_ht_no_mu_fromcand = fs->make<TH1F>("h_jet_ht_no_mu_fromcand", "", 250, 0, 5000);
  h_jet_ht_no_mu = fs->make<TH1F>("h_jet_ht_no_mu", "", 250, 0, 5000);
  h_jet_ht_m_hlt_ht = fs->make<TH1F>("h_jet_ht_m_hlt_ht", "", 100, -500, 500);
  h_jet_ht_no_mu_m_hlt_ht = fs->make<TH1F>("h_jet_ht_no_mu_m_hlt_ht", "", 100, -500, 500);
  h_njets_v_ht = fs->make<TH2F>("h_njets_v_ht", "", 50, 0, 2000, 15, 0, 15);

  if (use_genjets) {
    h_ngenjets = fs->make<TH1F>("h_ngenjets", "", 30, 0, 30);
    for (int i = 0; i < 6; ++i) {
      h_genjet_e[i]   = fs->make<TH1F>(TString::Format("h_genjet_e_%i",   i), "", 200, 0, 1000);
      h_genjet_pt[i]  = fs->make<TH1F>(TString::Format("h_genjet_pt_%i",  i), "", 200, 0, 1000);
      h_genjet_eta[i] = fs->make<TH1F>(TString::Format("h_genjet_eta_%i", i), "", 50, -6, 6);
      h_genjet_phi[i] = fs->make<TH1F>(TString::Format("h_genjet_phi_%i", i), "", 50, -M_PI, M_PI);
    }
    h_genjet_ht = fs->make<TH1F>("h_genjet_ht", "", 250, 0, 5000);
  }
}

void MFVTriggerEfficiency::produce(edm::Event& event, const edm::EventSetup& setup) {
  for (int i = 0; i < 2; ++i) { // HLT then L1
    if (require_bits[i] != -1) {
      edm::Handle<std::vector<int>> decisions;
      event.getByToken(decisions_tokens[i], decisions);
      const int decision = (*decisions)[require_bits[i]];
      if (decision == -1)
        throw cms::Exception("TriggerNotFound") << (i == 0 ? "HLT" : "L1") << " bit " << require_bits[i] << " wasn't found";
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

  if (require_4jets) {
    int njets = 0;
    for (const pat::Jet& jet : *jets)
      if (jet_selector(jet))
        ++njets;
    if (njets < 4)
      return;
  }

  h_nnoseljets->Fill(jets->size());

  int njet = 0;
  double jet_ht_all = 0;
  double jet_ht = 0;
  double jet_ht_ptlt200 = 0;
  double jet_ht_no_mu = 0;
  double jet_ht_no_mu_fromcand = 0;
  for (const pat::Jet& jet : *jets) {
    if (jet_selector(jet)) {
      ++njet;
      jet_ht_all += jet.pt();
      if (jet.pt() > 40) {
        jet_ht += jet.pt();
        if (jet.pt() < 200)
          jet_ht_ptlt200 += jet.pt();
      }
      if (jet.muonEnergyFraction() < 0.8)
        jet_ht_no_mu += jet.pt();

      double tot_frac_mu = 0;
      for (size_t idau = 0, idaue = jet.numberOfDaughters(); idau < idaue; ++idau) {
        const reco::Candidate* dau = jet.daughter(idau);
        if (abs(dau->pdgId()) == 13) {
          const double frac_mu = dau->energy() / jet.energy();
          tot_frac_mu += frac_mu;
        }
      }
      if (tot_frac_mu < 0.8)
        jet_ht_no_mu_fromcand += jet.pt();

      for (int i : {0, njet}) {
        if (i == 0 || njet < 6) {
          h_jet_e[i]->Fill(jet.energy());
          h_jet_pt[i]->Fill(jet.pt());
          h_jet_eta[i]->Fill(jet.eta());
          h_jet_phi[i]->Fill(jet.phi());
          h_jet_frac_mu[i]->Fill(tot_frac_mu);
          h_jet_muef[i]->Fill(jet.muonEnergyFraction());
        }
      }
    }
  }

  h_njets->Fill(njet);
  h_jet_ht_all->Fill(jet_ht_all);
  h_jet_ht->Fill(jet_ht);
  h_jet_ht_ptlt200->Fill(jet_ht_ptlt200);
  h_jet_ht_no_mu_fromcand->Fill(jet_ht_no_mu_fromcand);
  h_jet_ht_no_mu->Fill(jet_ht_no_mu);
  h_njets_v_ht->Fill(jet_ht, njet);

  edm::Handle<float> hlt_ht;
  event.getByToken(hlt_ht_token, hlt_ht);
  h_jet_ht_m_hlt_ht->Fill(jet_ht - *hlt_ht); 
  h_jet_ht_no_mu_m_hlt_ht->Fill(jet_ht_no_mu - *hlt_ht); 

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
          if (i == 0 || ngenjet < 6) {
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
