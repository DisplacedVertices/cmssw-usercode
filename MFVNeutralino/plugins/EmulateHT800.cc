#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/TriggerHelper.h"

class MFVEmulateHT800 : public edm::EDAnalyzer {
public:
  explicit MFVEmulateHT800(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override;

  edm::EDGetTokenT<edm::TriggerResults> trigger_results_token;
  edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> trigger_objects_token;
  const bool throw_not_found;
  const bool prints;

  TH1F* h_not_found_but_pass350;
  TH1F* h_ht;
  TH1F* h_agree[2];
};

MFVEmulateHT800::MFVEmulateHT800(const edm::ParameterSet& cfg)
  : trigger_results_token(consumes<edm::TriggerResults>(cfg.getParameter<edm::InputTag>("trigger_results_src"))),
    trigger_objects_token(consumes<pat::TriggerObjectStandAloneCollection>(cfg.getParameter<edm::InputTag>("trigger_objects_src"))),
    throw_not_found(cfg.getParameter<bool>("throw_not_found")),
    prints(cfg.getUntrackedParameter<bool>("prints", false))
{
  edm::Service<TFileService> fs;
  h_not_found_but_pass350 = fs->make<TH1F>("h_not_found_but_pass350", "", 2, 0, 2);
  h_ht = fs->make<TH1F>("h_ht", "", 2000, 0, 10000);
  h_agree[0] = fs->make<TH1F>("h_agree_800", "", 2, 0, 2);
  h_agree[1] = fs->make<TH1F>("h_agree_900", "", 2, 0, 2);
}

void MFVEmulateHT800::analyze(const edm::Event& event, const edm::EventSetup&) {
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

  // only objects that pass at least one path are saved. check 350
  std::pair<bool, bool> pass_and_found_350 = helper.pass_and_found_any_version("HLT_PFHT350_v");
  if (!pass_and_found_350.second)
    throw cms::Exception("EmulateHT800", "didn't find HLT_PFHT350");

  float ht = -1;
  bool found_ht = false;
  for (pat::TriggerObjectStandAlone obj : *trigger_objects)
    if (obj.filterIds().size() == 1 && obj.filterIds()[0] == 89 && obj.collection() == "hltPFHT::HLT") {
      ht = obj.pt();
      found_ht = true;
    }

  h_ht->Fill(ht);
  h_not_found_but_pass350->Fill(!found_ht && pass_and_found_350.first);

  if (!found_ht) {
    if (pass_and_found_350.first) {
      std::cout << "event: (" << event.id().run() << ", " << event.luminosityBlock() << ", " << event.id().event() << "): ";
      printf("DISAGREEMENT in found_ht: %i pass_350: %i\n", found_ht, pass_and_found_350.first);
      if (throw_not_found)
        throw cms::Exception("EmulateHT800", "couldn't find HT in trigger objects");
    }
    return;
  }

  const char* paths[2] = {"HLT_PFHT800_v", "HLT_PFHT900_v"};
  const int thresh[2] = {800, 900};
  bool one_found = false;
  for (int i : {0,1} ) {
    std::pair<bool, bool> pass_and_found = helper.pass_and_found_any_version(paths[i]);
    if (pass_and_found.second) {
      one_found = true;
      const bool agree = (ht > thresh[i]) == pass_and_found.first;
      if (!agree) {
        std::cout << "event: (" << event.id().run() << ", " << event.luminosityBlock() << ", " << event.id().event() << "): ";
        printf("DISAGREEMENT: ht = %f and HLT_PFHT%i = %i\n", ht, thresh[i], pass_and_found.first);
      }
      h_agree[i]->Fill(agree);
    }
  }
  if (!one_found)
    throw cms::Exception("EmulateHT800", "didn't find at least one of HLT_PFHT800 or 900");
}

DEFINE_FWK_MODULE(MFVEmulateHT800);
