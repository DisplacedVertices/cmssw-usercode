#include "TH2.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "PhysicsTools/SelectorUtils/interface/JetIDSelectionFunctor.h"

class QuadJetTrigEff : public edm::EDAnalyzer {
public:
  explicit QuadJetTrigEff(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void beginRun(const edm::Run&, const edm::EventSetup&);

  const std::string l1_path;
  const edm::InputTag jets_src;
  const int sel;
  JetIDSelectionFunctor calojet_sel;
  HLTConfigProvider hlt_cfg;
  L1GtUtils l1_cfg;
  const bool no_prescale;
  const bool apply_prescale;
  const bool require_trigger;

  TH1F* h_nnoseljets;
  TH1F* h_njets;
  TH1F* h_jet_e[20];
  TH1F* h_jet_pt[20];
  TH1F* h_jet_eta[20];
  TH1F* h_jet_phi[20];
};

QuadJetTrigEff::QuadJetTrigEff(const edm::ParameterSet& cfg)
  : l1_path(cfg.getParameter<std::string>("l1_path")),
    jets_src(cfg.getParameter<edm::InputTag>("jets_src")),
    sel(cfg.getParameter<int>("sel")),
    calojet_sel(JetIDSelectionFunctor::PURE09, JetIDSelectionFunctor::Quality_t(sel)),
    no_prescale(cfg.getParameter<bool>("no_prescale")),
    apply_prescale(cfg.getParameter<bool>("apply_prescale")),
    require_trigger(cfg.getParameter<bool>("require_trigger"))
{
  if (apply_prescale && no_prescale)
    throw cms::Exception("Misconfiguration", "can't apply_prescale and no_prescale");

  edm::Service<TFileService> fs;
  TH1::SetDefaultSumw2();
  h_nnoseljets = fs->make<TH1F>("h_nnoseljets", "", 200, 0, 200);
  h_njets = fs->make<TH1F>("h_njets", "", 20, 0, 20);
  for (int i = 0; i < 20; ++i) {
    h_jet_e[i]   = fs->make<TH1F>(TString::Format("h_jet_e_%i",   i), "", 2000, 0, 2000);
    h_jet_pt[i]  = fs->make<TH1F>(TString::Format("h_jet_pt_%i",  i), "", 2000, 0, 2000);
    h_jet_eta[i] = fs->make<TH1F>(TString::Format("h_jet_eta_%i", i), "", 200, -6, 6);
    h_jet_phi[i] = fs->make<TH1F>(TString::Format("h_jet_phi_%i", i), "", 200, -M_PI, M_PI);
  }
}

void QuadJetTrigEff::beginRun(const edm::Run& run, const edm::EventSetup& setup) {
  bool changed = true;
  if (!hlt_cfg.init(run, setup, "HLT", changed))
    throw cms::Exception("CheckPrescale", "HLTConfigProvider::init failed with process name HLT");
}

void QuadJetTrigEff::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  l1_cfg.getL1GtRunCache(event, setup, true, false);

  edm::Handle<edm::TriggerResults> hlt_results;
  event.getByLabel(edm::InputTag("TriggerResults", "", "HLT"), hlt_results);
  const edm::TriggerNames& hlt_names = event.triggerNames(*hlt_results);
  const size_t npaths = hlt_names.size();

  int prescale = 1;
  bool pass = false;

  for (int i = 0; i < 100; ++i) {
    char path[1024];
    snprintf(path, 1024, "HLT_QuadJet50_v%i", i);
    if (hlt_cfg.triggerIndex(path) == hlt_cfg.size())
      continue;

    int l1err;
    const bool l1_pass = l1_cfg.decision(event, l1_path, l1err);
    if (l1err != 0) throw cms::Exception("L1PrescaleError") << "error code when getting L1 decision: " << l1err;
    const int l1_prescale = l1_cfg.prescaleFactor(event, l1_path, l1err);
    if (l1err != 0) throw cms::Exception("L1PrescaleError") << "error code when getting L1 prescale: " << l1err;

    const int hlt_prescale = hlt_cfg.prescaleValue(event, setup, path);

    const size_t ipath = hlt_names.triggerIndex(path);
    if (!(ipath < npaths))
      throw cms::Exception("BadAssumption") << "hlt_cfg and triggerNames don't agree on " << path;
    const bool hlt_pass = hlt_results->accept(ipath);

    prescale = l1_prescale * hlt_prescale;
    pass = l1_pass && hlt_pass;

    break;
  }

  if (require_trigger && !pass)
    return;

  if (no_prescale && prescale != 1)
    return;

  if (!apply_prescale)
    prescale = 1;

  edm::Handle<pat::JetCollection> jets;
  event.getByLabel(jets_src, jets);

  h_nnoseljets->Fill(jets->size());

  pat::strbitset ret = calojet_sel.getBitTemplate();

  int njet = 0;
  for (const pat::Jet& jet : *jets) {
    ret.set(false);
    if (jet.pt() > 20 && fabs(jet.eta()) < 2.5 && (sel < 0 || calojet_sel(jet, ret))) {
      ++njet;
      if (njet == 20)
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
}

DEFINE_FWK_MODULE(QuadJetTrigEff);
