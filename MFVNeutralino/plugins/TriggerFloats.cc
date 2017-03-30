#include "JMTucker/MFVNeutralinoFormats/interface/Year.h"
#if defined(MFVNEUTRALINO_2015)
  #include "L1Trigger/GlobalTriggerAnalyzer/interface/L1GtUtils.h"
  #include "DataFormats/L1Trigger/interface/L1EtMissParticle.h"
  #include "DataFormats/L1Trigger/interface/L1EtMissParticleFwd.h"
#elif defined(MFVNEUTRALINO_2016)
  #include "CondFormats/DataRecord/interface/L1TUtmTriggerMenuRcd.h"
  #include "CondFormats/L1TObjects/interface/L1TUtmTriggerMenu.h"
  #include "DataFormats/L1TGlobal/interface/GlobalAlgBlk.h"
  #include "DataFormats/L1Trigger/interface/EtSum.h"
  #include "DataFormats/L1Trigger/interface/EtSumHelper.h"
  #include "DataFormats/L1Trigger/interface/Jet.h"
#else
  #error what year is it
#endif

#include "TTree.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/TriggerHelper.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/TriggerFloats.h"

#ifdef MFVNEUTRALINO_2016
std::ostream& operator<<(std::ostream& o, const l1t::L1Candidate& c) {
  o << "et: " << c.et() << " eta: " << c.eta() << " phi: " << c.phi()
    << " hwPt: " << c.hwPt() << " hwEta: " << c.hwEta() << " hwPhi: " << c.hwPhi() << " hwQual: " << c.hwQual() << " hwIso: " << c.hwIso();
  return o;
}
#endif

class MFVTriggerFloats : public edm::EDFilter {
public:
  explicit MFVTriggerFloats(const edm::ParameterSet&);

private:
  virtual bool filter(edm::Event&, const edm::EventSetup&) override;

#if defined(MFVNEUTRALINO_2015)
  L1GtUtils l1_cfg;
  const edm::EDGetTokenT<l1extra::L1EtMissParticleCollection> l1_htt_token;
#elif defined(MFVNEUTRALINO_2016)
  const edm::EDGetTokenT<l1t::JetBxCollection> l1_jets_token;
  const edm::EDGetTokenT<l1t::EtSumBxCollection> l1_etsums_token;
  const edm::EDGetTokenT<GlobalAlgBlkBxCollection> l1_results_token;
#endif
  const edm::EDGetTokenT<edm::TriggerResults> trigger_results_token;
  const edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> trigger_objects_token;
  const double ht_cut;

  const bool prints;
};

MFVTriggerFloats::MFVTriggerFloats(const edm::ParameterSet& cfg)
  :
#if defined(MFVNEUTRALINO_2015)
    l1_cfg(cfg, consumesCollector(), false),
    l1_htt_token(consumes<l1extra::L1EtMissParticleCollection>(edm::InputTag("l1extraParticles", "MHT"))),
#elif defined(MFVNEUTRALINO_2016)
    l1_jets_token(consumes<l1t::JetBxCollection>(edm::InputTag("caloStage2Digis", "Jet"))),
    l1_etsums_token(consumes<l1t::EtSumBxCollection>(edm::InputTag("caloStage2Digis", "EtSum"))),
    l1_results_token(consumes<GlobalAlgBlkBxCollection>(cfg.getParameter<edm::InputTag>("l1_results_src"))),
#endif
    trigger_results_token(consumes<edm::TriggerResults>(cfg.getParameter<edm::InputTag>("trigger_results_src"))),
    trigger_objects_token(consumes<pat::TriggerObjectStandAloneCollection>(cfg.getParameter<edm::InputTag>("trigger_objects_src"))),
    ht_cut(cfg.getParameter<double>("ht_cut")),
    prints(cfg.getUntrackedParameter<bool>("prints", false))
{
  produces<mfv::TriggerFloats>();
}

bool MFVTriggerFloats::filter(edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<edm::TriggerResults> trigger_results;
  event.getByToken(trigger_results_token, trigger_results);
  const edm::TriggerNames& trigger_names = event.triggerNames(*trigger_results);
  TriggerHelper helper(*trigger_results, trigger_names);

  edm::Handle<pat::TriggerObjectStandAloneCollection> trigger_objects;
  event.getByToken(trigger_objects_token, trigger_objects);

#ifdef MFVNEUTRALINO_2016
  edm::Handle<l1t::JetBxCollection> l1_jets;
  event.getByToken(l1_jets_token, l1_jets);

  double my_htt = 0;
  double my_htt_wbug = 0;
  double my_htt_pos = 0;
  double my_htt_neg = 0;

  for (size_t i = 0, ie = l1_jets->size(0); i < ie; ++i) {
    const l1t::Jet& jet = l1_jets->at(0, i);
    const double pt = jet.pt();
    const double eta = jet.eta();
    if (fabs(eta) < 3 && pt >= 30) {
      if (eta > 0 && my_htt_pos < 1023) {
        if (pt < 1023)
          my_htt_pos += pt;
        else
          my_htt_pos = 1023;
      }
      if (eta < 0 && my_htt_neg < 1023) {
        if (pt < 1023)
          my_htt_neg += pt;
        else 
          my_htt_neg = 1023;
      }
    }
  }

  my_htt = my_htt_wbug = my_htt_pos + my_htt_neg;
  if ((my_htt_neg == 1023 && my_htt_pos > 0) || (my_htt_pos == 1023 && my_htt_neg > 0))
    my_htt_wbug -= 1024;

  edm::Handle<l1t::EtSumBxCollection> l1_etsums;
  event.getByToken(l1_etsums_token, l1_etsums);
  l1t::EtSumHelper etsumhelper(l1_etsums);
#endif

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

#ifdef MFVNEUTRALINO_2016
    std::cout << " === L1 CaloStage2 digis ===\n";

    for (int bx = l1_jets->getFirstBX(), bxe = l1_jets->getLastBX(); bx < bxe; ++bx) {
      if (l1_jets->isEmpty(bx))
        std::cout << "\t    bx " << bx << " is empty for jets\n";
      else {
        const size_t n = l1_jets->size(bx);
        std::cout << "\t    bx " << bx << " has " << n << " jets:\n";
        for (size_t i = 0; i < n; ++i) {
          const l1t::Jet& jet = l1_jets->at(bx, i);
          std::cout << "\t      jet " << i << ": " << jet << "\n"
                    << "\t             rawEt " << jet.rawEt() << " seedEt " << jet.seedEt() << " PUEt: " << jet.puEt() << " towerIEta: " << jet.towerIEta() << " towerIPhi: " << jet.towerIPhi() << "\n";
        }
      }
    }

    for (int bx = l1_etsums->getFirstBX(), bxe = l1_etsums->getLastBX(); bx < bxe; ++bx) {
      if (l1_etsums->isEmpty(bx))
        std::cout << "\t    bx " << bx << " is empty for etsums\n";
      else {
        const size_t n = l1_etsums->size(bx);
        std::cout << "\t    bx " << bx << " has " << n << " etsums:\n";
        for (size_t i = 0; i < n; ++i) {
          const l1t::EtSum& etsum = l1_etsums->at(bx, i);
          std::cout << "\t      etsum " << i << ": type " << etsum.getType() << " " << etsum << "\n";
        }
      }
    }

    std::cout << "\tEtSumHelper says MET " << etsumhelper.MissingEt() << " phi " << etsumhelper.MissingEtPhi()
              << " MHT " << etsumhelper.MissingHt() << " phi " << etsumhelper.MissingHtPhi()
              << " ETT " << etsumhelper.TotalEt() << " HTT " << etsumhelper.TotalHt() << "  My HTT " << my_htt << " with bug " << my_htt_wbug << "\n";
#endif

    std::cout << std::endl;
  }

  float ht_for_cut = -1;
  std::auto_ptr<mfv::TriggerFloats> floats(new mfv::TriggerFloats);

  for (pat::TriggerObjectStandAlone obj : *trigger_objects) {
    if (obj.filterIds().size() == 1 && obj.filterIds()[0] == 89) {
      if (obj.collection() == "hltPFHT::HLT")
        ht_for_cut = floats->hltht = obj.pt();
      else if (obj.collection() == "hltHtMhtForMC::HLT") {
        floats->hltht4mc = obj.pt();
        if (ht_for_cut < 0)
          ht_for_cut = floats->hltht4mc;
      }
    }
  }

#if defined(MFVNEUTRALINO_2015)
  edm::Handle<l1extra::L1EtMissParticleCollection> l1_htts;
  event.getByToken(l1_htt_token, l1_htts);
  if (l1_htts->size() != 1)
    throw cms::Exception("BadAssumption", "not exactly one L1 MHT object");
  const l1extra::L1EtMissParticle& l1_htt = l1_htts->at(0);
  if (l1_htt.type() != 1)
    throw cms::Exception("BadAssumption", "L1 MHT object in collection not right type");
  floats->l1htt = l1_htt.etTotal();

#elif defined(MFVNEUTRALINO_2016)
  for (size_t i = 0, ie = l1_jets->size(0); i < ie; ++i) {
    const l1t::Jet& jet = l1_jets->at(0, i);
    if (fabs(jet.eta()) < 3)
      floats->l1jetspts.push_back(jet.pt());
  }
  std::sort(std::begin(floats->l1jetspts), std::end(floats->l1jetspts), std::greater<float>());

  floats->l1htt = etsumhelper.TotalHt();
  floats->myhtt = my_htt;
  floats->myhttwbug = my_htt_wbug;
#endif

  if (prints)
    printf("TriggerFloats: ht = %f  ht4mc = %f\n", floats->hltht, floats->hltht4mc);

  for (int i = 0; i < mfv::n_hlt_paths; ++i) {
    const std::pair<bool, bool> paf = helper.pass_and_found_any_version(mfv::hlt_paths[i]);
    if (paf.second)
      floats->HLTdecisions[i] = paf.first;

    if (prints)
      printf("HLT bit %2i %30s: %2i\n", i, mfv::hlt_paths[i], floats->HLTdecisions[i]);
  }

#if defined(MFVNEUTRALINO_2015)
  l1_cfg.getL1GtRunCache(event, setup, true, false);
#elif defined(MFVNEUTRALINO_2016)
  edm::Handle<GlobalAlgBlkBxCollection> l1_results_all;
  event.getByToken(l1_results_token, l1_results_all);
  const std::vector<bool>& l1_results = l1_results_all->at(0, 0).getAlgoDecisionFinal();

  edm::ESHandle<L1TUtmTriggerMenu> l1_menu;
  setup.get<L1TUtmTriggerMenuRcd>().get(l1_menu);
#endif

  for (int i = 0; i < mfv::n_l1_paths; ++i) {
#if defined(MFVNEUTRALINO_2015)
    int l1err = 0;
    const bool pass = l1_cfg.decision(event, mfv::l1_paths[i], l1err);
    const bool found = l1err == 0;
#elif defined(MFVNEUTRALINO_2016)
    const auto& m = l1_menu->getAlgorithmMap();
    const auto& e = m.find(mfv::l1_paths[i]);
    const bool found = e != m.end();
    const bool pass = found ? l1_results[e->second.getIndex()] : false;
#endif

    if (found) floats->L1decisions[i] = pass;

    if (prints)
      printf("L1 bit %2i %30s: %2i\n", i, mfv::l1_paths[i], floats->L1decisions[i]);
  }

  event.put(floats);

  return ht_cut < 0 || ht_for_cut > ht_cut;
}

DEFINE_FWK_MODULE(MFVTriggerFloats);
