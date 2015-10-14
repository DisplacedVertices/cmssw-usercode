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
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "PhysicsTools/SelectorUtils/interface/JetIDSelectionFunctor.h"

class MFVTriggerEfficiency : public edm::EDAnalyzer {
public:
  explicit MFVTriggerEfficiency(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void beginRun(const edm::Run&, const edm::EventSetup&);

  const bool require_trigger;
  const bool require_muon;
  const edm::InputTag muons_src;
  const StringCutObjectSelector<pat::Muon> muon_selector;
  const edm::InputTag jets_src;
  const StringCutObjectSelector<pat::Jet> jet_selector;
  const edm::InputTag genjets_src;
  const bool use_genjets;

  L1GtUtils l1_cfg;
  HLTConfigProvider hlt_cfg;

  TH1F* h_nnoselmuons;
  TH1F* h_nmuons;
  TH1F* h_muon_pt[2];
  TH1F* h_muon_eta[2];
  TH1F* h_muon_phi[2];
  TH1F* h_muon_iso[2];

  TH1F* h_nnoseljets;
  TH1F* h_njets;
  TH1F* h_jet_e[10];
  TH1F* h_jet_pt[10];
  TH1F* h_jet_eta[10];
  TH1F* h_jet_phi[10];
  TH1F* h_jet_ht;
  TH2F* h_njets_v_ht;

  TH1F* h_ngenjets;
  TH1F* h_genjet_e[10];
  TH1F* h_genjet_pt[10];
  TH1F* h_genjet_eta[10];
  TH1F* h_genjet_phi[10];
  TH1F* h_genjet_ht;
};

MFVTriggerEfficiency::MFVTriggerEfficiency(const edm::ParameterSet& cfg)
  : require_trigger(cfg.getParameter<bool>("require_trigger")),
    require_muon(cfg.getParameter<bool>("require_muon")),
    muons_src(cfg.getParameter<edm::InputTag>("muons_src")),
    muon_selector(cfg.getParameter<std::string>("muon_cut")),
    jets_src(cfg.getParameter<edm::InputTag>("jets_src")),
    jet_selector(cfg.getParameter<std::string>("jet_cut")),
    genjets_src(cfg.getParameter<edm::InputTag>("genjets_src")),
    use_genjets(genjets_src.label() != "")
{
  edm::Service<TFileService> fs;
  TH1::SetDefaultSumw2();

  if (require_muon) {
    h_nnoselmuons = fs->make<TH1F>("h_nnoselmuons", "", 5, 0, 5);
    h_nmuons = fs->make<TH1F>("h_nmuons", "", 3, 0, 3);
    for (int i = 0; i < 2; ++i) {
      h_muon_pt [i] = fs->make<TH1F>(TString::Format("h_muon_pt_%i" , i), "", 200, 0, 1000);
      h_muon_eta[i] = fs->make<TH1F>(TString::Format("h_muon_eta_%i", i), "", 100, -3, 3);
      h_muon_phi[i] = fs->make<TH1F>(TString::Format("h_muon_phi_%i", i), "", 100, -M_PI, M_PI);
      h_muon_iso[i] = fs->make<TH1F>(TString::Format("h_muon_iso_%i", i), "", 100, 0, 2);
    }
  }

  h_nnoseljets = fs->make<TH1F>("h_nnoseljets", "", 30, 0, 30);
  h_njets = fs->make<TH1F>("h_njets", "", 30, 0, 30);
  for (int i = 0; i < 10; ++i) {
    h_jet_e[i]   = fs->make<TH1F>(TString::Format("h_jet_e_%i",   i), "", 1000, 0, 1000);
    h_jet_pt[i]  = fs->make<TH1F>(TString::Format("h_jet_pt_%i",  i), "", 1000, 0, 1000);
    h_jet_eta[i] = fs->make<TH1F>(TString::Format("h_jet_eta_%i", i), "", 100, -6, 6);
    h_jet_phi[i] = fs->make<TH1F>(TString::Format("h_jet_phi_%i", i), "", 100, -M_PI, M_PI);
  }
  h_jet_ht = fs->make<TH1F>("h_jet_ht", "", 250, 0, 5000);
  h_njets_v_ht = fs->make<TH2F>("h_njets_v_ht", "", 50, 0, 2000, 25, 0, 25);

  if (use_genjets) {
    h_ngenjets = fs->make<TH1F>("h_ngenjets", "", 30, 0, 30);
    for (int i = 0; i < 10; ++i) {
      h_genjet_e[i]   = fs->make<TH1F>(TString::Format("h_genjet_e_%i",   i), "", 1000, 0, 1000);
      h_genjet_pt[i]  = fs->make<TH1F>(TString::Format("h_genjet_pt_%i",  i), "", 1000, 0, 1000);
      h_genjet_eta[i] = fs->make<TH1F>(TString::Format("h_genjet_eta_%i", i), "", 100, -6, 6);
      h_genjet_phi[i] = fs->make<TH1F>(TString::Format("h_genjet_phi_%i", i), "", 100, -M_PI, M_PI);
    }
    h_genjet_ht = fs->make<TH1F>("h_genjet_ht", "", 250, 0, 5000);
  }
}

void MFVTriggerEfficiency::beginRun(const edm::Run& run, const edm::EventSetup& setup) {
  bool changed = true;
  if (!hlt_cfg.init(run, setup, "HLT", changed))
    throw cms::Exception("CheckPrescale", "HLTConfigProvider::init failed with process name HLT");
}

void MFVTriggerEfficiency::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  l1_cfg.getL1GtRunCache(event, setup, true, false);

  edm::Handle<edm::TriggerResults> hlt_results;
  event.getByLabel(edm::InputTag("TriggerResults", "", "HLT"), hlt_results);
  const edm::TriggerNames& hlt_names = event.triggerNames(*hlt_results);
  const size_t npaths = hlt_names.size();

  bool found = false;
  bool pass = false;

#if 0
  std::vector<std::string> paths({
        "HLT_PFHT650_v",
        "HLT_PFHT550_4Jet_v",
//        "HLT_PFHT450_SixJet40_PFBTagCSV_v",
//        "HLT_PFHT400_SixJet30_BTagCSV0p5_2PFBTagCSV_v",
        "HLT_PFHT450_SixJet40_v",
        "HLT_PFHT400_SixJet30_v",
//        "HLT_QuadJet45_TripleCSV0p5_v",
//        "HLT_QuadJet45_DoubleCSV0p5_v",
//        "HLT_DoubleJet90_Double30_TripleCSV0p5_v",
//        "HLT_DoubleJet90_Double30_DoubleCSV0p5_v",
//        "HLT_HT650_DisplacedDijet80_Inclusive_v",
//        "HLT_HT750_DisplacedDijet80_Inclusive_v",
//        "HLT_HT500_DisplacedDijet40_Inclusive_v",
//        "HLT_HT550_DisplacedDijet40_Inclusive_v",
//        "HLT_HT350_DisplacedDijet40_DisplacedTrack_v",
//        "HLT_HT350_DisplacedDijet80_DisplacedTrack_v",
//        "HLT_HT350_DisplacedDijet80_Tight_DisplacedTrack_v"
        });
#endif

  if (require_trigger) {
    for (int hlt_version : {1, 2, 3, 4, 5, 6, 7, 8, 9} ) {
      char path[1024];
      snprintf(path, 1024, "HLT_PFHT800_v%i", hlt_version);
      if (hlt_cfg.triggerIndex(path) == hlt_cfg.size())
        continue;

      found = true;

      //int l1err;
      //const bool l1_pass = l1_cfg.decision(event, "L1_QuadJetC40", l1err);
      //if (l1err != 0) throw cms::Exception("L1ResultError") << "error code when getting L1 decision for L1_QuadJetC40: " << l1err;

      const size_t ipath = hlt_names.triggerIndex(path);
      if (!(ipath < npaths))
        throw cms::Exception("BadAssumption") << "hlt_cfg and triggerNames don't agree on " << path;
      const bool hlt_pass = hlt_results->accept(ipath);

      //pass = l1_pass && hlt_pass;
      pass = hlt_pass;

      break;
    }

    if (!found)
      throw cms::Exception("BadAssumption", "one of HLT_PFHT800_v{1..9} not found");

    if (!pass)
      return;
  }

  if (require_muon) {
    edm::Handle<pat::MuonCollection> muons;
    event.getByLabel(muons_src, muons);

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
  event.getByLabel(jets_src, jets);

  h_nnoseljets->Fill(jets->size());

  int njet = 0;
  double jet_ht = 0;
  for (const pat::Jet& jet : *jets) {
    if (jet_selector(jet)) {
      ++njet;
      jet_ht += jet.pt();
      if (njet == 10)
        break;
      int is[2] = {0, njet};
      for (int i : is) {
        h_jet_e[i]->Fill(jet.energy());
        h_jet_pt[i]->Fill(jet.pt());
        h_jet_eta[i]->Fill(jet.eta());
        h_jet_phi[i]->Fill(jet.phi());
      }
    }
  }

  h_njets->Fill(njet);
  h_jet_ht->Fill(jet_ht);
  h_njets_v_ht->Fill(jet_ht, njet);

  if (use_genjets) {
    edm::Handle<reco::GenJetCollection> genjets;
    event.getByLabel(genjets_src, genjets);

    int ngenjet = 0;
    double genjet_ht = 0;
    for (const reco::GenJet& genjet : *genjets) {
      if (genjet.pt() > 20 && fabs(genjet.eta()) < 2.5) {
        ++ngenjet;
        genjet_ht += genjet.pt();
        if (ngenjet == 10)
          break;
        int is[2] = {0, ngenjet};
        for (int i : is) {
          h_genjet_e[i]->Fill(genjet.energy());
          h_genjet_pt[i]->Fill(genjet.pt());
          h_genjet_eta[i]->Fill(genjet.eta());
          h_genjet_phi[i]->Fill(genjet.phi());
        }
      }
    }

    h_ngenjets->Fill(ngenjet);
    h_genjet_ht->Fill(genjet_ht);
  }
}

DEFINE_FWK_MODULE(MFVTriggerEfficiency);
