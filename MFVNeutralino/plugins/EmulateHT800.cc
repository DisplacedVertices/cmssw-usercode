#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/TriggerHelper.h"
#include "L1Trigger/GlobalTriggerAnalyzer/interface/L1GtUtils.h"

class MFVEmulateHT800 : public edm::EDFilter {
public:
  explicit MFVEmulateHT800(const edm::ParameterSet&);

private:
  virtual bool filter(edm::Event&, const edm::EventSetup&) override;
  void put_ht(edm::Event&, float) const;

  edm::EDGetTokenT<edm::TriggerResults> trigger_results_token;
  edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> trigger_objects_token;
  const bool throw_not_found;
  const bool return_actual;
  const bool return_ht900;
  const bool prints;
  const bool histos;

  L1GtUtils l1_cfg;

  TH1F* h_not_found_but_pass350;
  TH1F* h_ht;
  TH1F* h_ht4mc;
  TH1F* h_agree[2];
};

MFVEmulateHT800::MFVEmulateHT800(const edm::ParameterSet& cfg)
  : trigger_results_token(consumes<edm::TriggerResults>(cfg.getParameter<edm::InputTag>("trigger_results_src"))),
    trigger_objects_token(consumes<pat::TriggerObjectStandAloneCollection>(cfg.getParameter<edm::InputTag>("trigger_objects_src"))),
    throw_not_found(cfg.getParameter<bool>("throw_not_found")),
    return_actual(cfg.getParameter<bool>("return_actual")),
    return_ht900(cfg.getParameter<bool>("return_ht900")),
    prints(cfg.getUntrackedParameter<bool>("prints", false)),
    histos(cfg.getUntrackedParameter<bool>("histos", false)),
    l1_cfg(cfg, consumesCollector(), false)
{
  if (histos) {
    edm::Service<TFileService> fs;
    h_not_found_but_pass350 = fs->make<TH1F>("h_not_found_but_pass350", "", 2, 0, 2);
    h_ht = fs->make<TH1F>("h_ht", "", 2000, 0, 10000);
    h_ht4mc = fs->make<TH1F>("h_ht4mc", "", 2000, 0, 10000);
    h_agree[0] = fs->make<TH1F>("h_agree_800", "", 2, 0, 2);
    h_agree[1] = fs->make<TH1F>("h_agree_900", "", 2, 0, 2);
  }

  produces<float>();
}

void MFVEmulateHT800::put_ht(edm::Event& event, float ht_) const {
  std::auto_ptr<float> ht(new float(ht_));
  event.put(ht);
}

bool MFVEmulateHT800::filter(edm::Event& event, const edm::EventSetup& setup) {
  l1_cfg.getL1GtRunCache(event, setup, true, false);

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

  const char* paths[2] = {"HLT_PFHT800_v", "HLT_PFHT900_v"};
  const int thresh[2] = {800, 900};
  bool pass [2] = {false, false};
  bool found[2] = {false, false};
  for (int i : {0,1} ) {
    std::pair<bool, bool> pass_and_found = helper.pass_and_found_any_version(paths[i]);
    found[i] = pass_and_found.second;
    if (pass_and_found.second) {
      pass[i] = pass_and_found.first;
    }
  }

  // JMTBAD force it in 2016
  found[0] = false;

  if (int(found[0]) + int(found[1]) != 1)
    throw cms::Exception("EmulateHT800", "didn't find exactly one of HLT_PFHT800 or 900");

  if (prints) printf("found 800? %i pass? %i   found 900? %i pass? %i\n", found[0], pass[0], found[1], pass[1]);

  float ht = -1;
  bool found_ht = false;
  float ht4mc = -1;
  bool found_ht4mc = false;
  for (pat::TriggerObjectStandAlone obj : *trigger_objects) {
    if (obj.filterIds().size() == 1 && obj.filterIds()[0] == 89) {
      if (obj.collection() == "hltPFHT::HLT") {
        ht = obj.pt();
        found_ht = true;
      }
      else if (obj.collection() == "hltHtMhtForMC::HLT") {
        ht4mc = obj.pt();
        found_ht4mc = true;
      }
    }
  }

  if (return_actual && found[return_ht900]) {
    if (prints) printf("return actual = %i\n", pass[return_ht900]);
    put_ht(event, ht);
    return pass[return_ht900];
  }

  // HT800 and 900 seeds are is "L1_HTT150 OR L1_HTT175"
  int l1err = 0;
  const bool l1_pass_150 = l1_cfg.decision(event, "L1_HTT150", l1err);
  if (l1err != 0) throw cms::Exception("L1ResultError") << "error code when getting L1 decision for L1_HTT150: " << l1err;
  const bool l1_pass_175 = l1_cfg.decision(event, "L1_HTT175", l1err);
  if (l1err != 0) throw cms::Exception("L1ResultError") << "error code when getting L1 decision for L1_HTT175: " << l1err;
  const bool l1_pass = l1_pass_150 || l1_pass_175;

  // only objects that pass at least one path are saved. check 350
  std::pair<bool, bool> pass_and_found_350 = helper.pass_and_found_any_version("HLT_PFHT350_v");
  if (!pass_and_found_350.second)
    throw cms::Exception("EmulateHT800", "didn't find HLT_PFHT350");

  if (prints)
    printf("ht? %i %f  ht4mc? %i %f\n", found_ht, ht, found_ht4mc, ht4mc);

  if (histos) {
    h_ht->Fill(ht);
    h_not_found_but_pass350->Fill(!found_ht && pass_and_found_350.first);
  }

  if (!found_ht) {
    if (pass_and_found_350.first) {
      std::cout << "event: (" << event.id().run() << ", " << event.luminosityBlock() << ", " << event.id().event() << "): ";
      printf("DISAGREEMENT in found_ht: %i pass_350: %i\n", found_ht, pass_and_found_350.first);
      if (throw_not_found)
        throw cms::Exception("EmulateHT800", "couldn't find HT in trigger objects");
    }
    put_ht(event, -1);
    if (prints) printf("350 didn't pass, return false\n");
    return false; // 350 didn't pass...
  }

  bool emulated_pass[2] = {false, false};

  for (int i : {0,1} ) {
    emulated_pass[i] = l1_pass && ht >= thresh[i];
    if (prints) printf("emulated pass %i: l1_pass %i  ht %f -> %i\n", i, l1_pass, ht, emulated_pass[i]);
    if (found[i]) {
      const bool agree = emulated_pass[i] == pass[i];
      if (histos) h_agree[i]->Fill(agree);
      if (!agree) {
        std::cout << "event: (" << event.id().run() << ", " << event.luminosityBlock() << ", " << event.id().event() << "): ";
        printf("DISAGREEMENT: ht = %f and HLT_PFHT%i = %i; ht4mc (found? %i) = %f\n", ht, thresh[i], pass[i], found_ht4mc, ht4mc);
        if (histos) h_ht4mc->Fill(ht4mc);
      }
    }
  }

  if (prints) printf("put ht = %f in event and return %i\n", ht, emulated_pass[0]);
  put_ht(event, ht);
  return emulated_pass[return_ht900];
}

DEFINE_FWK_MODULE(MFVEmulateHT800);
