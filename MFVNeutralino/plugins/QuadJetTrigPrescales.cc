#include "TTree.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"

class QuadJetTrigPrescales : public edm::EDAnalyzer {
public:
  explicit QuadJetTrigPrescales(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void beginRun(const edm::Run&, const edm::EventSetup&);

  L1GtUtils l1_cfg;
  HLTConfigProvider hlt_cfg;

  struct tree_t {
    unsigned run;
    unsigned lumi;
    unsigned event;
    std::vector<bool> l1_was_seed;
    std::vector<int> l1_prescale;
    std::vector<int> l1_mask;
    std::vector<bool> pass_l1_premask;
    std::vector<bool> pass_l1;
    std::vector<bool> hlt_found;
    std::vector<int> hlt_prescale;
    std::vector<bool> pass_hlt;

    tree_t() { clear(); }

    void clear() { 
      run = lumi = event = 0;
      l1_was_seed.assign(9, 0);
      l1_prescale.assign(9, 0);
      l1_mask.assign(9, 0);
      pass_l1_premask.assign(9, 0);
      pass_l1.assign(9, 0);
      hlt_found.assign(4, 0);
      hlt_prescale.assign(4, 0);
      pass_hlt.assign(4, 0);
    }
  };

  TTree* tree;
  tree_t nt;
};

QuadJetTrigPrescales::QuadJetTrigPrescales(const edm::ParameterSet& cfg) {
  edm::Service<TFileService> fs;
  tree = fs->make<TTree>("t", "");
  tree->Branch("run", &nt.run, "run/i");
  tree->Branch("lumi", &nt.lumi, "lumi/i");
  tree->Branch("event", &nt.event, "event/i");
  tree->Branch("l1_was_seed", &nt.l1_was_seed);
  tree->Branch("l1_prescale", &nt.l1_prescale);
  tree->Branch("l1_mask", &nt.l1_mask);
  tree->Branch("pass_l1_premask", &nt.pass_l1_premask);
  tree->Branch("pass_l1", &nt.pass_l1);
  tree->Branch("hlt_found", &nt.hlt_found);
  tree->Branch("hlt_prescale", &nt.hlt_prescale);
  tree->Branch("pass_hlt", &nt.pass_hlt);
}

void QuadJetTrigPrescales::beginRun(const edm::Run& run, const edm::EventSetup& setup) {
  bool changed = true;
  if (!hlt_cfg.init(run, setup, "HLT", changed))
    throw cms::Exception("QuadJetTrigPrescales", "HLTConfigProvider::init failed with process name HLT");
}

void QuadJetTrigPrescales::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  nt.clear();
  nt.run  = event.id().run();
  nt.lumi = event.luminosityBlock();
  nt.event  = event.id().event();

  l1_cfg.getL1GtRunCache(event, setup, true, false);

  edm::Handle<edm::TriggerResults> hlt_results;
  event.getByLabel(edm::InputTag("TriggerResults", "", "HLT"), hlt_results);
  const edm::TriggerNames& hlt_names = event.triggerNames(*hlt_results);
  const size_t npaths = hlt_names.size();

  const std::vector<std::string> all_l1_seeds = { "L1_QuadJetC32", "L1_QuadJetC36", "L1_QuadJetC40", "L1_HTT125", "L1_HTT150", "L1_HTT175", "L1_DoubleJetC52", "L1_DoubleJetC56", "L1_DoubleJetC64" };
  //const size_t nl1 = all_l1_seeds.size();
  const std::vector<int> hlt_versions = {1,2,3,5};
  const size_t nhlt = hlt_versions.size();

  for (size_t ihlt = 0; ihlt < nhlt; ++ihlt) {
    const int hlt_version = hlt_versions[ihlt];
    char path[1024];
    snprintf(path, 1024, "HLT_QuadJet50_v%i", hlt_version);
    bool found = false;
    if ((found = nt.hlt_found[ihlt] = hlt_cfg.triggerIndex(path) != hlt_cfg.size()))
      nt.hlt_prescale[ihlt] = hlt_cfg.prescaleValue(event, setup, path);

    const size_t ipath = hlt_names.triggerIndex(path);
    if ((ipath < npaths) != found)
      throw cms::Exception("BadAssumption") << "hlt_cfg and triggerNames don't agree on " << path;

    nt.pass_hlt[ihlt] = found ? hlt_results->accept(ipath) : false;

    if (!found)
      continue;

    const auto& v = hlt_cfg.hltL1GTSeeds(path);
    if (v.size() != 1)
      throw cms::Exception("BadAssumption") << "more than one seed returned: " << v.size();

    std::string s = v[0].second;
    const std::string delim = " OR ";
    while (s.size()) {
      const size_t pos = s.find(delim);
      const std::string l1_path = s.substr(0, pos);
      const auto& itl1 = std::find(all_l1_seeds.begin(), all_l1_seeds.end(), l1_path);
      if (itl1 == all_l1_seeds.end())
        throw cms::Exception("BadAssumption") << "L1 seed " << l1_path << " not expected";
      const size_t il1 = itl1 - all_l1_seeds.begin();

      nt.l1_was_seed[il1] = true;

      int l1_err;

      nt.l1_prescale[il1] = l1_cfg.prescaleFactor(event, l1_path, l1_err);
      if (l1_err != 0)
        throw cms::Exception("L1Error") << "error code " << l1_err << " for path " << l1_path << " when getting prescale";

      nt.l1_mask[il1] = l1_cfg.triggerMask(event, l1_path, l1_err);
      if (l1_err != 0)
        throw cms::Exception("L1Error") << "error code " << l1_err << " for path " << l1_path << " when getting mask";

      nt.pass_l1_premask[il1] = l1_cfg.decision(event, l1_path, l1_err);
      if (l1_err != 0)
        throw cms::Exception("L1Error") << "error code " << l1_err << " for path " << l1_path << " when getting pre-mask decision";
      
      nt.pass_l1[il1] = l1_cfg.decisionAfterMask(event, l1_path, l1_err);
      if (l1_err != 0)
        throw cms::Exception("L1Error") << "error code " << l1_err << " for path " << l1_path << " when getting decision";
      
      if (pos == std::string::npos)
        break;
      else
        s.erase(0, pos + delim.length());
    }
  }

  int sum = 0;

  if ((sum = std::accumulate(nt.l1_was_seed.begin(), nt.l1_was_seed.end(), 0)) == 0)
    throw cms::Exception("BadAssumption") << "none of the L1 paths were found";

  if ((sum = std::accumulate(nt.hlt_found.begin(), nt.hlt_found.end(), 0)) != 1)
    throw cms::Exception("BadAssumption") << "not exactly one of the HLT path versions were found: " << sum;

  tree->Fill();
}

DEFINE_FWK_MODULE(QuadJetTrigPrescales);
