#include "TTree.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "CondFormats/DataRecord/interface/L1TUtmTriggerMenuRcd.h"
#include "CondFormats/L1TObjects/interface/L1TUtmTriggerMenu.h"
#include "DataFormats/L1TGlobal/interface/GlobalAlgBlk.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/TriggerHelper.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"

class MFVTriggerFloats : public edm::EDProducer {
public:
  explicit MFVTriggerFloats(const edm::ParameterSet&);

private:
  virtual void produce(edm::Event&, const edm::EventSetup&) override;

  const bool prints;

  const edm::EDGetTokenT<GlobalAlgBlkBxCollection> l1_results_token;
  const edm::EDGetTokenT<edm::TriggerResults> trigger_results_token;
  const edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> trigger_objects_token;

  TTree* tree;
  struct tree_t {
    unsigned run;
    unsigned lumi;
    unsigned long long evt;
    float ht;
    float ht4mc;
    unsigned found;
    unsigned pass;
  };
  tree_t t;
};

MFVTriggerFloats::MFVTriggerFloats(const edm::ParameterSet& cfg)
  : prints(cfg.getUntrackedParameter<bool>("prints", false)),
    l1_results_token(consumes<GlobalAlgBlkBxCollection>(cfg.getParameter<edm::InputTag>("l1_results_src"))),
    trigger_results_token(consumes<edm::TriggerResults>(cfg.getParameter<edm::InputTag>("trigger_results_src"))),
    trigger_objects_token(consumes<pat::TriggerObjectStandAloneCollection>(cfg.getParameter<edm::InputTag>("trigger_objects_src"))),
    tree((TTree*)cfg.getUntrackedParameter<bool>("tree", false))
{
  produces<float>("ht");
  produces<float>("ht4mc");
  produces<std::vector<int>>("L1decisions");
  produces<std::vector<int>>("HLTdecisions");

  if (tree) {
    edm::Service<TFileService> fs;
    tree = fs->make<TTree>("t", "");
    tree->Branch("run",   &t.run,   "run/i");
    tree->Branch("lumi",  &t.lumi,  "lumi/i");
    tree->Branch("event", &t.evt,   "event/l");
    tree->Branch("ht",    &t.ht,    "ht/F");
    tree->Branch("ht4mc", &t.ht4mc, "ht4mc/F");
    tree->Branch("found", &t.found, "found/i");
    tree->Branch("pass",  &t.pass,  "pass/i");
  }
}

void MFVTriggerFloats::produce(edm::Event& event, const edm::EventSetup& setup) {
  if (tree) {
    t.run   = event.id().run();
    t.lumi  = event.luminosityBlock();
    t.evt   = event.id().event();
    t.ht    = -1;
    t.ht4mc = -1;
    t.found = 0;
    t.pass  = 0;
  }

  edm::Handle<GlobalAlgBlkBxCollection> l1_results_all;
  event.getByToken(l1_results_token, l1_results_all);
  const std::vector<bool>& l1_results = l1_results_all->at(0, 0).getAlgoDecisionFinal();

  edm::ESHandle<L1TUtmTriggerMenu> l1_menu;
  setup.get<L1TUtmTriggerMenuRcd>().get(l1_menu);

  edm::Handle<edm::TriggerResults> trigger_results;
  event.getByToken(trigger_results_token, trigger_results);
  const edm::TriggerNames& trigger_names = event.triggerNames(*trigger_results);
  TriggerHelper helper(*trigger_results, trigger_names);

  edm::Handle<pat::TriggerObjectStandAloneCollection> trigger_objects;
  event.getByToken(trigger_objects_token, trigger_objects);

  if (prints) {
    std::cout << "event: (" << event.id().run() << ", " << event.luminosityBlock() << ", " << event.id().event() << ")\n";
    std::cout << " === TRIGGER PATHS === " << "\n";
    for (unsigned int i = 0, n = trigger_results->size(); i < n; ++i)
      std::cout << "Trigger " << trigger_names.triggerName(i) << ": " << (trigger_results->accept(i) ? "PASS" : "fail (or not run)") << "\n";
    std::cout << "\n === TRIGGER OBJECTS === " << "\n";
    for (pat::TriggerObjectStandAlone obj : *trigger_objects) {
      obj.unpackPathNames(trigger_names); // needs above to be non-const
      std::cout << "\tTrigger object:  pt " << obj.pt() << ", eta " << obj.eta() << ", phi " << obj.phi() << "\n";
      std::cout << "\t   Collection: " << obj.collection() << "\n";
      std::cout << "\t   Type IDs:   ";
      for (unsigned h = 0; h < obj.filterIds().size(); ++h)
        std::cout << " " << obj.filterIds()[h] ;
      std::cout << "\n";
      std::cout << "\t   Filters:    ";
      for (unsigned h = 0; h < obj.filterLabels().size(); ++h)
        std::cout << " " << obj.filterLabels()[h];
      std::cout << "\n";
      const std::vector<std::string>& pathNamesAll  = obj.pathNames(false);
      const std::vector<std::string>& pathNamesLast = obj.pathNames(true);
      std::cout << "\t   Paths (" << pathNamesAll.size()<<"/"<<pathNamesLast.size()<<"):    ";
      for (unsigned h = 0, n = pathNamesAll.size(); h < n; ++h) {
        const bool isBoth = obj.hasPathName(pathNamesAll[h], true, true);
        const bool isL3   = obj.hasPathName(pathNamesAll[h], false, true);
        const bool isLF   = obj.hasPathName(pathNamesAll[h], true, false);
        const bool isNone = obj.hasPathName(pathNamesAll[h], false, false);
        std::cout << "   " << pathNamesAll[h];
        if (isBoth) std::cout << "(L,3)";
        if (isL3 && !isBoth) std::cout << "(*,3)";
        if (isLF && !isBoth) std::cout << "(L,*)";
        if (isNone && !isBoth && !isL3 && !isLF) std::cout << "(*,*)";
      }
      std::cout << "\n";
    }
    std::cout << std::endl;
  }

  std::auto_ptr<float> ht(new float(-1));
  std::auto_ptr<float> ht4mc(new float(-1));
  std::auto_ptr<std::vector<int>> L1decisions(new std::vector<int>(mfv::n_l1_paths, -1));
  std::auto_ptr<std::vector<int>> HLTdecisions(new std::vector<int>(mfv::n_hlt_paths, -1));

  for (pat::TriggerObjectStandAlone obj : *trigger_objects) {
    if (obj.filterIds().size() == 1 && obj.filterIds()[0] == 89) {
      if (obj.collection() == "hltPFHT::HLT")
        t.ht = *ht = obj.pt();
      else if (obj.collection() == "hltHtMhtForMC::HLT")
        t.ht4mc = *ht4mc = obj.pt();
    }
  }

  if (prints)
    printf("TriggerFloats: ht = %f  ht4mc = %f\n", *ht, *ht4mc);

  for (int i = 0; i < mfv::n_l1_paths; ++i) {
    const auto& m = l1_menu->getAlgorithmMap();
    const auto& e = m.find(mfv::l1_paths[i]);
    const bool found = e != m.end();
    const bool pass = found ? l1_results[e->second.getIndex()] : false;

    if (found) (*L1decisions)[i] = pass;

    if (prints)
      printf("L1 bit %2i %30s: %2i\n", i, mfv::l1_paths[i], (*L1decisions)[i]);

    if (tree) {
      if (found) {
        const unsigned bit = 1 << i;
        t.found |= bit;
        if (pass) t.pass |= bit;
      }
    }
  }

  for (int i = 0; i < mfv::n_hlt_paths; ++i) {
    const std::pair<bool, bool> paf = helper.pass_and_found_any_version(hlt_paths[i]);
    if (paf.second)
      (*HLTdecisions)[i] = paf.first;

    if (prints)
      printf("HLT bit %2i %30s: %2i\n", i, mfv::hlt_paths[i], (*HLTdecisions)[i]);

    if (tree) {
      if (paf.second) {
        const unsigned bit = 1 << (31 - i);
        t.found |= bit;
        if (paf.first) t.pass |= bit;
      }
    }
  }

  if (tree)
    tree->Fill();

  event.put(ht, "ht");
  event.put(ht4mc, "ht4mc");
  event.put(L1decisions, "L1decisions");
  event.put(HLTdecisions, "HLTdecisions");
}

DEFINE_FWK_MODULE(MFVTriggerFloats);
