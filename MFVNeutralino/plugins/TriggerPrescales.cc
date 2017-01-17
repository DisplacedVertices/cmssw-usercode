#include "TTree.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "L1Trigger/GlobalTriggerAnalyzer/interface/L1GtUtils.h"
#include "HLTrigger/HLTcore/interface/HLTPrescaleProvider.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"

class MFVTriggerPrescales : public edm::EDAnalyzer {
public:
  explicit MFVTriggerPrescales(const edm::ParameterSet&);
  static const int NL1;
  static const int NHLT;

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void beginRun(const edm::Run&, const edm::EventSetup&);

  const edm::EDGetTokenT<edm::TriggerResults> hlt_token;
  const bool prints;
  std::map<std::pair<unsigned, unsigned>, bool> ls_seen;

  HLTPrescaleProvider trig_cfg;

  struct tree_t {
    unsigned run;
    unsigned lumi;
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
      run = lumi = 0;
      l1_was_seed.assign(NL1, 0);
      l1_prescale.assign(NL1, 0);
      l1_mask.assign(NL1, 0);
      pass_l1_premask.assign(NL1, 0);
      pass_l1.assign(NL1, 0);
      hlt_found.assign(NHLT, 0);
      hlt_prescale.assign(NHLT, 0);
      pass_hlt.assign(NHLT, 0);
    }
  };

  TTree* tree;
  tree_t nt;
};

const int MFVTriggerPrescales::NL1 = 4;
const int MFVTriggerPrescales::NHLT = 2;

MFVTriggerPrescales::MFVTriggerPrescales(const edm::ParameterSet& cfg)
  : hlt_token(consumes<edm::TriggerResults>(edm::InputTag("TriggerResults", "", "HLT"))),
    prints(cfg.getUntrackedParameter<bool>("prints", false)),
    trig_cfg(cfg, consumesCollector(), *this)
{
  edm::Service<TFileService> fs;
  tree = fs->make<TTree>("t", "");
  tree->Branch("run", &nt.run, "run/i");
  tree->Branch("lumi", &nt.lumi, "lumi/i");
  tree->Branch("l1_was_seed", &nt.l1_was_seed);
  tree->Branch("l1_prescale", &nt.l1_prescale);
  tree->Branch("l1_mask", &nt.l1_mask);
  tree->Branch("pass_l1_premask", &nt.pass_l1_premask);
  tree->Branch("pass_l1", &nt.pass_l1);
  tree->Branch("hlt_found", &nt.hlt_found);
  tree->Branch("hlt_prescale", &nt.hlt_prescale);
  tree->Branch("pass_hlt", &nt.pass_hlt);
}

void MFVTriggerPrescales::beginRun(const edm::Run& run, const edm::EventSetup& setup) {
  bool changed = true;
  if (!trig_cfg.init(run, setup, "HLT", changed))
    throw cms::Exception("MFVTriggerPrescales", "HLTConfigProvider::init failed with process name HLT");

  if (prints) {
    const HLTConfigProvider& hlt_cfg = trig_cfg.hltConfigProvider();
    hlt_cfg.dump("ProcessPSet");
    hlt_cfg.dump("ProcessName");
    hlt_cfg.dump("GlobalTag");
    hlt_cfg.dump("TableName");
    hlt_cfg.dump("Triggers");
    hlt_cfg.dump("TriggerSeeds");
    hlt_cfg.dump("Modules");
    hlt_cfg.dump("StreamNames");
    hlt_cfg.dump("Streams");
    hlt_cfg.dump("DatasetNames");
    hlt_cfg.dump("Datasets");
    hlt_cfg.dump("PrescaleTable");
  }
}

void MFVTriggerPrescales::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  if (prints) printf("MFVTriggerPrescales r %u l %u e %llu\n", event.id().run(), event.luminosityBlock(), event.id().event());

  // Not clear how to use L1GtUtils in beginLumi so just do the below once per lumisec
  auto ls = std::make_pair(event.id().run(), event.luminosityBlock());
  if (ls_seen[ls]) {
    if (prints) printf("already seen, skipping\n");
    return;
  }
  ls_seen[ls] = true;

  nt.clear();
  nt.run  = event.id().run();
  nt.lumi = event.luminosityBlock();

  const L1GtUtils& l1_cfg = trig_cfg.l1GtUtils();
  const HLTConfigProvider& hlt_cfg = trig_cfg.hltConfigProvider();

  edm::Handle<edm::TriggerResults> hlt_results;
  event.getByToken(hlt_token, hlt_results);
  const edm::TriggerNames& hlt_names = event.triggerNames(*hlt_results);
  const size_t npaths = hlt_names.size();

  const std::vector<std::string> all_l1_seeds = { "L1_HTT100", "L1_HTT125", "L1_HTT150", "L1_HTT175" };
  const std::vector<int> hlt_versions = {1,2};
  assert(all_l1_seeds.size() == NL1);
  assert(hlt_versions.size() == NHLT);

  for (size_t ihlt = 0; ihlt < NHLT; ++ihlt) {
    const int hlt_version = hlt_versions[ihlt];
    char path[1024];
    snprintf(path, 1024, "HLT_PFHT800_v%i", hlt_version);
    bool found = false;
    if ((found = nt.hlt_found[ihlt] = hlt_cfg.triggerIndex(path) != hlt_cfg.size()))
      nt.hlt_prescale[ihlt] = trig_cfg.prescaleValue(event, setup, path);

    const size_t ipath = hlt_names.triggerIndex(path);
    if ((ipath < npaths) != found)
      throw cms::Exception("BadAssumption") << "hlt_cfg and triggerNames don't agree on " << path;

    nt.pass_hlt[ihlt] = found ? hlt_results->accept(ipath) : false;

    if (prints) printf("ihlt %lu path %s found? %i pass? %i prescale %i\n", ihlt, path, int(found), int(nt.pass_hlt[ihlt]), nt.hlt_prescale[ihlt]);

    if (!found)
      continue;

    const auto& v = hlt_cfg.hltL1GTSeeds(path);
    if (v.size() != 1)
      throw cms::Exception("BadAssumption") << "more than one seed returned: " << v.size();

    std::string s = v[0].second;
    if (prints) printf("L1 seed %s\n", s.c_str());
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

      if (prints) printf("%s: prescale %i mask %i pass premask? %i pass? %i\n", l1_path.c_str(), nt.l1_prescale[il1], nt.l1_mask[il1], int(nt.pass_l1_premask[il1]), int(nt.pass_l1[il1]));

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

DEFINE_FWK_MODULE(MFVTriggerPrescales);
