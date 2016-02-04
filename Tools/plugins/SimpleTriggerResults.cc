#include "TTree.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

class SimpleTriggerResults : public edm::EDAnalyzer {
public:
  explicit SimpleTriggerResults(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  std::string branch_name(const std::string& path_name) const;

  const edm::EDGetTokenT<edm::TriggerResults> trigger_results_token;
  const edm::EDGetTokenT<double> weight_token;
  const bool use_weight;
  const bool deversion;

  TTree* tree;

  static const size_t max_npaths;
  std::map<std::string, size_t> paths;
#define MAX_NPATHS 1024
  bool buf[MAX_NPATHS];
  unsigned run;
  unsigned lumi;
  unsigned long long evt;
  double weight;
};

SimpleTriggerResults::SimpleTriggerResults(const edm::ParameterSet& cfg) 
  : trigger_results_token(consumes<edm::TriggerResults>(cfg.getParameter<edm::InputTag>("trigger_results_src"))),
    weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
    use_weight(cfg.getParameter<edm::InputTag>("weight_src").label() != ""),
    deversion(cfg.getParameter<bool>("deversion"))
{
  edm::Service<TFileService> fs;
  tree = fs->make<TTree>("t", "");
  tree->Branch("run",    &run,    "run/i");
  tree->Branch("lumi",   &lumi,   "lumi/i");
  tree->Branch("event",  &evt);
  if (use_weight)
    tree->Branch("weight", &weight, "weight/D");
}

std::string SimpleTriggerResults::branch_name(const std::string& path_name) const {
  std::string b_name = path_name;
  if (deversion) {
    size_t pos = b_name.rfind("_v");
    if (pos != std::string::npos)
      b_name.erase(pos);
  }
  return b_name;
}

void SimpleTriggerResults::analyze(const edm::Event& event, const edm::EventSetup&) {
  run  = event.id().run();
  lumi = event.luminosityBlock();
  evt  = event.id().event();

  if (use_weight) {
    edm::Handle<double> weight_h;
    event.getByToken(weight_token, weight_h);
    weight = *weight_h;
  }

  edm::Handle<edm::TriggerResults> trigger_results;
  event.getByToken(trigger_results_token, trigger_results);
  const edm::TriggerNames& trigger_names = event.triggerNames(*trigger_results);
  const size_t npaths = trigger_names.size();
  assert(npaths <= MAX_NPATHS);

  if (paths.size() == 0) {
    // Initialize the tree branches now that we have the information
    // on the paths. The branch name is the path name, unless
    // deversion is true, in which case e.g. HLT_QuadJet50_v2 becomes
    // HLT_QuadJet50. The version number is not stripped in the paths
    // map for checking for the same menu below, and for indexing into
    // buf.
    for (size_t ipath = 0; ipath < npaths; ++ipath) {
      const std::string& path_name = trigger_names.triggerName(ipath);
      std::string b_name = branch_name(path_name);
      tree->Branch(b_name.c_str(), &buf[ipath], (b_name + "/O").c_str());
      paths[path_name] = ipath;
    }
  }
  else {
    // Throw an exception if we're not using the exact same paths.
    bool ok = paths.size() == npaths;
    size_t ipath = 0;
    std::string path_name;
    for (size_t ipath = 0; ok && ipath < npaths; ++ipath) {
      path_name = trigger_names.triggerName(ipath);
      if (paths.find(path_name) == paths.end())
        ok = false;
    }
    if (!ok)
      throw cms::Exception("SimpleTriggerResults") << "different trigger menu? paths.size(): " << paths.size() << " npaths: " << npaths << " or path " << ipath << " had name " << path_name << " not found in list of paths";
  }

  for (size_t ipath = 0; ipath < npaths; ++ipath)
    buf[ipath] = trigger_results->accept(ipath);

  tree->Fill();
}

DEFINE_FWK_MODULE(SimpleTriggerResults);
