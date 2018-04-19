#include "JMTucker/Tools/interface/Year.h"
#if defined(MFVNEUTRALINO_2015)
  #include "L1Trigger/GlobalTriggerAnalyzer/interface/L1GtUtils.h"
  #include "DataFormats/L1Trigger/interface/L1EtMissParticle.h"
  #include "DataFormats/L1Trigger/interface/L1EtMissParticleFwd.h"
#elif defined(MFVNEUTRALINO_2016) || defined(MFVNEUTRALINO_2017)
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
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "JMTucker/Tools/interface/TriggerHelper.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/TriggerFloats.h"

class MFVTriggerFloats : public edm::EDProducer {
public:
  explicit MFVTriggerFloats(const edm::ParameterSet&);

private:
  virtual void produce(edm::Event&, const edm::EventSetup&) override;

#if defined(MFVNEUTRALINO_2015)
  L1GtUtils l1_cfg;
  const edm::EDGetTokenT<l1extra::L1EtMissParticleCollection> l1_htt_token;
#elif defined(MFVNEUTRALINO_2016) || defined(MFVNEUTRALINO_2017)
  const edm::EDGetTokenT<l1t::JetBxCollection> l1_jets_token;
  const edm::EDGetTokenT<l1t::EtSumBxCollection> l1_etsums_token;
  const edm::EDGetTokenT<GlobalAlgBlkBxCollection> l1_results_token;
#endif
  const edm::EDGetTokenT<edm::TriggerResults> trigger_results_token;
  const edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> trigger_objects_token;

  const edm::EDGetTokenT<pat::JetCollection> jets_token;
  const StringCutObjectSelector<pat::Jet> jet_selector;

  const int prints;
};

MFVTriggerFloats::MFVTriggerFloats(const edm::ParameterSet& cfg)
  :
#if defined(MFVNEUTRALINO_2015)
    l1_cfg(cfg, consumesCollector(), false),
    l1_htt_token(consumes<l1extra::L1EtMissParticleCollection>(edm::InputTag("l1extraParticles", "MHT"))),
#elif defined(MFVNEUTRALINO_2016) || defined(MFVNEUTRALINO_2017)
    l1_jets_token(consumes<l1t::JetBxCollection>(edm::InputTag("caloStage2Digis", "Jet"))),
    l1_etsums_token(consumes<l1t::EtSumBxCollection>(edm::InputTag("caloStage2Digis", "EtSum"))),
    l1_results_token(consumes<GlobalAlgBlkBxCollection>(cfg.getParameter<edm::InputTag>("l1_results_src"))),
#endif
    trigger_results_token(consumes<edm::TriggerResults>(cfg.getParameter<edm::InputTag>("trigger_results_src"))),
    trigger_objects_token(consumes<pat::TriggerObjectStandAloneCollection>(cfg.getParameter<edm::InputTag>("trigger_objects_src"))),
    jets_token(consumes<pat::JetCollection>(cfg.getParameter<edm::InputTag>("jets_src"))),
    jet_selector(cfg.getParameter<std::string>("jet_cut")),
    prints(cfg.getUntrackedParameter<int>("prints", 0))
{
  produces<mfv::TriggerFloats>();
}

void MFVTriggerFloats::produce(edm::Event& event, const edm::EventSetup& setup) {
  if (prints) std::cout << "TriggerFloats run " << event.id().run() << " lumi " << event.luminosityBlock() << " event " << event.id().event() << "\n";

  edm::Handle<edm::TriggerResults> trigger_results;
  event.getByToken(trigger_results_token, trigger_results);
  const edm::TriggerNames& trigger_names = event.triggerNames(*trigger_results);
  TriggerHelper helper(*trigger_results, trigger_names);

  edm::Handle<pat::TriggerObjectStandAloneCollection> trigger_objects;
  event.getByToken(trigger_objects_token, trigger_objects);

#if defined(MFVNEUTRALINO_2016) || defined(MFVNEUTRALINO_2017)
  edm::Handle<l1t::JetBxCollection> l1_jets;
  event.getByToken(l1_jets_token, l1_jets);

  int i2pt_first[2] = {0};
  int i2htt[2] = {0};
  for (size_t i = 0, ie = l1_jets->size(0); i < ie; ++i) {
    const l1t::Jet& jet = l1_jets->at(0, i);

    const double eta = jet.eta();
    const bool is_pos = eta >= 0; // ?
    const double pt = jet.pt();
    const int i2pt = int(pt*2);
    assert(fabs(pt*2 - double(i2pt)) < 1e-3);

    if (fabs(eta) < 3 && i2pt >= 61) {
      if (i2pt_first[is_pos] == 0)
        i2pt_first[is_pos] = i2pt;

      if (i2pt == 2047)
        i2htt[is_pos] = 2047;
      else if (i2pt_first[is_pos] != 2047) {
        i2htt[is_pos] += i2pt;
        if (i2htt[is_pos] > 4095)
          i2htt[is_pos] = 4095;
      }
    }

    if (prints) printf("after jet #%2lu (pt %7.1f eta %7.2f is pos? %i): i2pt_neg_first: %7i pos %7i i2htt_neg: %7i pos: %7i\n", i, jet.pt(), jet.eta(), is_pos, i2pt_first[0], i2pt_first[1], i2htt[0], i2htt[1]);
  }

  double my_htt = 0;
  double my_htt_wbug = 0;

  if ((i2pt_first[0] == 2047 && i2pt_first[1] ==    0) ||
      (i2pt_first[0] ==    0 && i2pt_first[1] == 2047) ||
      (i2pt_first[0] == 2047 && i2pt_first[1] == 2047))
    my_htt = my_htt_wbug = 2047.5;
  else {
    my_htt = my_htt_wbug = (i2htt[0] + i2htt[1]) / 2.;
    if ((i2htt[0] == 2047 && i2htt[1]) || (i2htt[1] == 2047 && i2htt[0]))
      my_htt_wbug -= 1024;
  }

  if (prints) {
    //    double htt = 0;
    double htt_wbug = 0;
    double htt_pos = 0;
    double htt_neg = 0;

    for (size_t i = 0, ie = l1_jets->size(0); i < ie; ++i) {
      const l1t::Jet& jet = l1_jets->at(0, i);
      const double pt = jet.pt();
      if (fabs(jet.eta()) < 3 && pt >= 30) {
        if(jet.eta() > 0 && htt_pos < 1023){
          if(pt < 1023)
            htt_pos += pt;
          else
            htt_pos = 1023;
        }
        if(jet.eta() < 0 && htt_neg < 1023) {
          if(pt < 1023)
            htt_neg += pt;
          else 
            htt_neg = 1023;
        } 
      }
    }

    //    htt = htt_pos + htt_neg;
    htt_wbug = htt_pos + htt_neg;

    if( ( htt_neg == 1023 && htt_pos > 0 )
        || ( htt_pos == 1023 && htt_neg > 0 ) )
      htt_wbug -= 1024;

    printf("Aaron gets %7.1f\n",  htt_wbug);
  }

  edm::Handle<l1t::EtSumBxCollection> l1_etsums;
  event.getByToken(l1_etsums_token, l1_etsums);
  l1t::EtSumHelper etsumhelper(l1_etsums);
#endif

  if (prints > 1) {
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

#if defined(MFVNEUTRALINO_2016) || defined(MFVNEUTRALINO_2017)
  if (prints) {
    std::cout << "=== L1 CaloStage2 digis ===\n";

    auto intok = [](double x) { assert(x - int(x) < 1e-3); return int(x); };
    std::streamsize p = std::cout.precision();

    for (int bx = l1_jets->getFirstBX(), bxe = l1_jets->getLastBX(); bx < bxe; ++bx) {
      if (prints > 1 || bx == 0) {
        if (l1_jets->isEmpty(bx))
          std::cout << "bx " << bx << " is empty for jets\n";
        else {
          const size_t n = l1_jets->size(bx);
          std::cout << "bx " << bx << " has " << n << " jets:\n";
          for (size_t i = 0; i < n; ++i) {
            const l1t::Jet& jet = l1_jets->at(bx, i);
            assert(fabs(jet.pt() - jet.et()) < 1e-3);
            std::cout << "  jet " << i << " et: " << std::setw(7) << jet.et() << " eta: " << std::setw(7) << std::setprecision(3) << jet.eta() << " phi: " << std::setw(7) << jet.phi() << "        "
                      << " hwPt: " << intok(jet.hwPt()) << " hwEta: " << intok(jet.hwEta()) << " hwPhi: " << intok(jet.hwPhi()) << " hwQual: " << intok(jet.hwQual()) << " hwIso: " << intok(jet.hwIso())
                      << " rawEt " << intok(jet.rawEt()) << " seedEt " << intok(jet.seedEt()) << " PUEt: " << intok(jet.puEt()) << " towerIEta: " << intok(jet.towerIEta()) << " towerIPhi: " << intok(jet.towerIPhi()) << "\n";
          }
        }
      }
    }

    std::cout.precision(p);

    if (prints > 1) {
      for (int bx = l1_etsums->getFirstBX(), bxe = l1_etsums->getLastBX(); bx < bxe; ++bx) {
        if (prints > 1 || bx == 0) {
          if (l1_etsums->isEmpty(bx))
            std::cout << "bx " << bx << " is empty for etsums\n";
          else {
            const size_t n = l1_etsums->size(bx);
            std::cout << "bx " << bx << " has " << n << " etsums:\n";
            for (size_t i = 0; i < n; ++i) {
              const l1t::EtSum& etsum = l1_etsums->at(bx, i);
              std::cout << "  etsum " << i << ": type " << etsum.getType() << " et: " << etsum.et() << " hwPt: " << etsum.hwPt() << "\n";
            }
          }
        }
      }
    }

    if (prints > 1)
      std::cout << "EtSumHelper: MET " << etsumhelper.MissingEt() << " phi " << etsumhelper.MissingEtPhi()
                << " MHT " << etsumhelper.MissingHt() << " phi " << etsumhelper.MissingHtPhi()
                << " ETT " << etsumhelper.TotalEt() << "   HTT " << etsumhelper.TotalHt() << " Mine " << my_htt << " w.bug " << my_htt_wbug << "\n";
    else
      std::cout << "EtSumHelper: HTT " << etsumhelper.TotalHt() << " Mine " << my_htt << " w.bug " << my_htt_wbug;

    if (fabs(my_htt - etsumhelper.TotalHt()) > 0.4 || fabs(my_htt_wbug - etsumhelper.TotalHt()) > 0.4) {
      std::cout << "  DIFFERENT\n";

      size_t n = l1_jets->size(0);
      assert(n < 30);
      for (unsigned x = 1, xe = 1<<n; x < xe; ++x) {
        double sum = 0;
        for (unsigned i = 0; i < n; ++i)
          if (x & (1<<i))
            sum += l1_jets->at(0, i).pt();
        while (sum > 0) {
          if (fabs(sum - etsumhelper.TotalHt()) < 4) {
            printf("to get %7.1f should've used 0x%x =", sum, x);
            for (unsigned i = 0; i < n; ++i)
              if (x & (1<<i))
                printf(" %u", i);
            printf("\n");
          }
          sum -= 1024.;
        }
      }
    }

    std::cout << std::endl;
  }
#endif

  std::unique_ptr<mfv::TriggerFloats> floats(new mfv::TriggerFloats);

  for (pat::TriggerObjectStandAlone obj : *trigger_objects) {
    if (obj.filterIds().size() == 1 && obj.filterIds()[0] == 89) {
      if (obj.collection() == "hltPFHT::HLT")
        floats->hltht = obj.pt();
      else if (obj.collection() == "hltHtMhtForMC::HLT") {
        floats->hltht4mc = obj.pt();
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

#elif defined(MFVNEUTRALINO_2016) || defined(MFVNEUTRALINO_2017)
  for (size_t i = 0, ie = l1_jets->size(0); i < ie; ++i) {
    const l1t::Jet& jet = l1_jets->at(0, i);
    if (i > 0) assert(jet.pt() <= l1_jets->at(0, i-1).pt());
    if (fabs(jet.eta()) < 3) {
      TLorentzVector v;
      v.SetPtEtaPhiE(jet.pt(), jet.eta(), jet.phi(), jet.energy());
      floats->l1jets.push_back(v);
    }
  }

  floats->l1htt = etsumhelper.TotalHt();
  floats->myhtt = my_htt;
  floats->myhttwbug = my_htt_wbug;
#endif

  if (prints)
    printf("TriggerFloats: hltht = %f  hltht4mc = %f\n", floats->hltht, floats->hltht4mc);

  for (int i = 0; i < mfv::n_hlt_paths; ++i) {
    const std::pair<bool, bool> paf = helper.pass_and_found_any_version(mfv::hlt_paths[i]);
    if (paf.second)
      floats->HLTdecisions[i] = paf.first;

    if (prints)
      printf("HLT bit %2i %20s: %2i\n", i, mfv::hlt_paths[i], floats->HLTdecisions[i]);
  }

#if defined(MFVNEUTRALINO_2015)
  l1_cfg.getL1GtRunCache(event, setup, true, false);
#elif defined(MFVNEUTRALINO_2016) || defined(MFVNEUTRALINO_2017)
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
#elif defined(MFVNEUTRALINO_2016) || defined(MFVNEUTRALINO_2017)
    const auto& m = l1_menu->getAlgorithmMap();
    const auto& e = m.find(mfv::l1_paths[i]);
    const bool found = e != m.end();
    const bool pass = found ? l1_results[e->second.getIndex()] : false;
#endif

    if (found) floats->L1decisions[i] = pass;

    if (prints)
      printf("L1  bit %2i %20s: %2i\n", i, mfv::l1_paths[i], floats->L1decisions[i]);
  }

  edm::Handle<pat::JetCollection> jets;
  event.getByToken(jets_token, jets);

  for (const pat::Jet& jet : *jets)
    if (jet_selector(jet)) {
      const double pt = jet.pt();
      TLorentzVector v;
      v.SetPtEtaPhiE(pt, jet.eta(), jet.phi(), jet.energy());
      floats->jets.push_back(v);
      floats->jetmuef.push_back(jet.muonEnergyFraction());

      floats->htall += pt;
      if (pt > 30) floats->htptgt30 += pt;
      if (pt > 40) floats->ht += pt;
    }

  if (prints)
    printf("# all jets: %lu  selected: %i  jetpt1: %f  2: %f  ht: %f\n", jets->size(), floats->njets(), floats->jetpt1(), floats->jetpt2(), floats->ht);

  event.put(std::move(floats));
}

DEFINE_FWK_MODULE(MFVTriggerFloats);
