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
  L1GtUtils l1_cfg;
  const bool no_prescale;
  const bool apply_prescale;
  const std::string prints;

  std::map<int,int> prescales_seen;
  std::map<std::string, std::map<int,int> > l1_prescales_seen;

  TH1F* h_jet4_pt;
  TH1F* h_jet4_eta;
};

QuadJetTrigEff::QuadJetTrigEff(const edm::ParameterSet& cfg)
  : jets_src(cfg.getParameter<edm::InputTag>("jets_src")),
    sel(cfg.getParameter<int>("sel")),
    calojet_sel(JetIDSelectionFunctor::PURE09, JetIDSelectionFunctor::Quality_t(sel)),
    no_prescale(cfg.getParameter<bool>("no_prescale")),
    apply_prescale(cfg.getParameter<bool>("apply_prescale")),
    prints(cfg.getParameter<std::string>("prints"))
{
  if (apply_prescale && no_prescale)
    throw cms::Exception("Misconfiguration", "can't apply_prescale and no_prescale");

  edm::Service<TFileService> fs;
  TH1::SetDefaultSumw2();
  h_jet4_pt  = fs->make<TH1F>("h_jet4_pt",  "", 201, -1, 200);
  h_jet4_eta = fs->make<TH1F>("h_jet4_pta", "", 200, -6, 6);
}

void QuadJetTrigEff::beginRun(const edm::Run& run, const edm::EventSetup& setup) {
  bool changed = true;
  if (!hlt_cfg.init(run, setup, "HLT", changed))
    throw cms::Exception("CheckPrescale", "HLTConfigProvider::init failed with process name HLT");
}

void QuadJetTrigEff::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  l1_cfg.getL1GtRunCache(event, setup, true, false);
  int prescale = 1;

  for (int i = 0; i < 100; ++i) {
    char path[1024];
    snprintf(path, 1024, "HLT_QuadJet50_v%i", i);
    if (hlt_cfg.triggerIndex(path) != hlt_cfg.size()) {
      prescale = hlt_cfg.prescaleValue(event, setup, path);

      const auto& v = hlt_cfg.hltL1GTSeeds(path);
      if (v.size() != 1)
        throw cms::Exception("BadAssumption") << "more than one seed returned for quadjet50: " << v.size();

      std::string s = v[0].second;
      size_t pos = 0;
      const std::string delim = " OR ";
      int min_l1prescale = (1<<17)-1;
      while ((pos = s.find(delim)) != std::string::npos) {
        const std::string l1path = s.substr(0, pos);
        int l1err;
        const int l1prescale = l1_cfg.prescaleFactor(event, l1path, l1err);
        if (l1err != 0)
          throw cms::Exception("L1PrescaleError") << "error code " << l1err << " for path " << l1path;
        if (l1prescale < min_l1prescale)
          min_l1prescale = l1prescale;
        l1_prescales_seen[l1path][l1prescale] += 1;
        s.erase(0, pos + delim.length());
      }

      if (min_l1prescale > 1 && min_l1prescale < (1<<17))
        throw cms::Exception("L1PrescaleError") << "l1 prescale " << min_l1prescale;

      prescales_seen[prescale] += 1;
    }
  }

  if (no_prescale && prescale != 1)
    return;

  if (!apply_prescale)
    prescale = 1;

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

  h_jet4_pt ->Fill(pt, prescale);
  h_jet4_eta->Fill(eta, prescale);
}

void QuadJetTrigEff::endJob() {
  if (prints != "") {
    printf("QuadJetTrigEff:%s BEGIN prints\nprescales seen:\n", prints.c_str());
    for (const auto& p : prescales_seen)
      printf("%i: %i\n", p.first, p.second);
    printf("l1 prescales seen:\n");
    for (const auto& p : l1_prescales_seen) {
      printf("path: %s:\n", p.first.c_str());
      for (const auto& p2 : p.second) {
        printf("%i: %i\n", p2.first, p2.second);
      }
    }
    printf("QuadJetTrigEff:%s END prints\n", prints.c_str());
  }
}

DEFINE_FWK_MODULE(QuadJetTrigEff);
