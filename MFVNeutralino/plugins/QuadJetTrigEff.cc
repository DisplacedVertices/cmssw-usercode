#include "TH2.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
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
  virtual void endJob();

  const edm::InputTag jets_src;
  const int sel;
  JetIDSelectionFunctor calojet_sel;
  HLTConfigProvider hlt_cfg;
  const bool no_prescale;

  std::map<int,int> prescales_seen;
  TH1F* h_jet4_pt;
  TH1F* h_jet4_eta;
};

QuadJetTrigEff::QuadJetTrigEff(const edm::ParameterSet& cfg)
  : jets_src(cfg.getParameter<edm::InputTag>("jets_src")),
    sel(cfg.getParameter<int>("sel")),
    calojet_sel(JetIDSelectionFunctor::PURE09, JetIDSelectionFunctor::Quality_t(sel)),
    no_prescale(cfg.getParameter<bool>("no_prescale"))
{
  edm::Service<TFileService> fs;
  h_jet4_pt  = fs->make<TH1F>("h_jet4_pt",  "", 201, -1, 200);
  h_jet4_eta = fs->make<TH1F>("h_jet4_pta", "", 200, -6, 6);
}

void QuadJetTrigEff::beginRun(const edm::Run& run, const edm::EventSetup& setup) {
  bool changed = true;
  if (!hlt_cfg.init(run, setup, "HLT", changed))
    throw cms::Exception("CheckPrescale", "HLTConfigProvider::init failed with process name HLT");
}

void QuadJetTrigEff::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  int prescale = 0;
  for (int i = 0; i < 100; ++i) {
    char path[1024];
    snprintf(path, 1024, "HLT_QuadJet50_v%i", i);
    if (hlt_cfg.triggerIndex(path) != hlt_cfg.size()) {
      prescale = hlt_cfg.prescaleValue(event, setup, path);
      //      std::pair<int, int> prescales = hlt_cfg.prescaleValues(event, setup, path);
      //      prescale = prescales.first * prescales.second;
      prescales_seen[prescale] += 1;
    }
  }

  if (no_prescale and prescale != 1)
    return;

  edm::Handle<pat::JetCollection> jets;
  event.getByLabel(jets_src, jets);

  pat::strbitset ret = calojet_sel.getBitTemplate();

  int njet = 0;
  double pt = -1, eta = -6;
  for (const pat::Jet& jet : *jets) {
    ret.set(false);
    if (sel < 0 || calojet_sel(jet, ret))
      if (++njet == 4) {
        pt  = jet.pt();
        eta = jet.eta();
      }
  }

  h_jet4_pt ->Fill(pt);
  h_jet4_eta->Fill(eta);
}

void QuadJetTrigEff::endJob() {
  printf("QuadJetTrigEff prescales seen:\n");
  for (const auto& p : prescales_seen)
    printf("%i: %i\n", p.first, p.second);
}

DEFINE_FWK_MODULE(QuadJetTrigEff);
