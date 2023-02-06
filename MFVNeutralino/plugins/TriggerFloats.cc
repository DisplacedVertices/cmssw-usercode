#include "TTree.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "CondFormats/DataRecord/interface/L1TUtmTriggerMenuRcd.h"
#include "CondFormats/L1TObjects/interface/L1TUtmTriggerMenu.h"
#include "DataFormats/L1TGlobal/interface/GlobalAlgBlk.h"
#include "DataFormats/L1Trigger/interface/EtSum.h"
#include "DataFormats/L1Trigger/interface/EtSumHelper.h"
#include "DataFormats/L1Trigger/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "JMTucker/Tools/interface/TriggerHelper.h"
#include "JMTucker/Tools/interface/METxyCorrection.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/TriggerFloats.h"
#include <cmath>

class MFVTriggerFloats : public edm::EDProducer {
public:
  explicit MFVTriggerFloats(const edm::ParameterSet&);

private:
  virtual void produce(edm::Event&, const edm::EventSetup&) override;

  const edm::EDGetTokenT<l1t::JetBxCollection> l1_jets_token;
  const edm::EDGetTokenT<l1t::EtSumBxCollection> l1_etsums_token;
  const edm::EDGetTokenT<GlobalAlgBlkBxCollection> l1_results_token;
  const edm::EDGetTokenT<edm::TriggerResults> trigger_results_token;
  const edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> trigger_objects_token;
  //const edm::EDGetTokenT<edm::TriggerResults> met_filters_token;
  const edm::EDGetTokenT<bool> badPFMuonFilterUpdateDz_token;

  const edm::EDGetTokenT<pat::JetCollection> jets_token;
  const StringCutObjectSelector<pat::Jet> jet_selector;

  //const edm::EDGetTokenT<pat::METCollection> met_token;
  const edm::EDGetTokenT<pat::MuonCollection> muons_token;
  const StringCutObjectSelector<pat::Muon> muon_selector;
  const edm::EDGetTokenT<reco::VertexCollection> primary_vertex_token;
  const bool isMC;
  const int year;

  const int prints;
};

MFVTriggerFloats::MFVTriggerFloats(const edm::ParameterSet& cfg)
  : l1_jets_token(consumes<l1t::JetBxCollection>(edm::InputTag("caloStage2Digis", "Jet"))),
    l1_etsums_token(consumes<l1t::EtSumBxCollection>(edm::InputTag("caloStage2Digis", "EtSum"))),
    l1_results_token(consumes<GlobalAlgBlkBxCollection>(cfg.getParameter<edm::InputTag>("l1_results_src"))),
    trigger_results_token(consumes<edm::TriggerResults>(cfg.getParameter<edm::InputTag>("trigger_results_src"))),
    trigger_objects_token(consumes<pat::TriggerObjectStandAloneCollection>(cfg.getParameter<edm::InputTag>("trigger_objects_src"))),
    //met_filters_token(consumes<edm::TriggerResults>(cfg.getParameter<edm::InputTag>("met_filters_src"))),
    badPFMuonFilterUpdateDz_token(consumes<bool>(edm::InputTag("BadPFMuonFilterUpdateDz"))),
    jets_token(consumes<pat::JetCollection>(cfg.getParameter<edm::InputTag>("jets_src"))),
    jet_selector(cfg.getParameter<std::string>("jet_cut")),
    //met_token(consumes<pat::METCollection>(cfg.getParameter<edm::InputTag>("met_src"))),
    muons_token(consumes<pat::MuonCollection>(cfg.getParameter<edm::InputTag>("muons_src"))),
    muon_selector(cfg.getParameter<std::string>("muon_cut")),
    primary_vertex_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("primary_vertex_src"))),
    isMC(cfg.getParameter<bool>("isMC")),
    year(cfg.getParameter<int>("year")),
    prints(cfg.getUntrackedParameter<int>("prints", 0))
{
  produces<mfv::TriggerFloats>();
}

namespace {
  TLorentzVector p4(double pt, double eta, double phi, double energy) {
    TLorentzVector v;
    v.SetPtEtaPhiE(pt, eta, phi, energy);
    return v;
  }
}

void MFVTriggerFloats::produce(edm::Event& event, const edm::EventSetup& setup) {
  if (prints) std::cout << "TriggerFloats run " << event.id().run() << " lumi " << event.luminosityBlock() << " event " << event.id().event() << "\n";

  //std::vector<std::string> metfilternames = {"Flag_goodVertices", "Flag_globalSuperTightHalo2016Filter", "Flag_HBHENoiseFilter", "Flag_HBHENoiseIsoFilter", "Flag_EcalDeadCellTriggerPrimitiveFilter", "Flag_BadPFMuonFilter", "Flag_eeBadScFilter", "Flag_ecalBadCalibFilter"};
  //edm::Handle<edm::TriggerResults> metFilters;
  //event.getByToken(met_filters_token, metFilters);
  //const edm::TriggerNames &names = event.triggerNames(*metFilters);

  edm::Handle<edm::TriggerResults> trigger_results;
  event.getByToken(trigger_results_token, trigger_results);
  const edm::TriggerNames& trigger_names = event.triggerNames(*trigger_results);
  TriggerHelper helper(*trigger_results, trigger_names);

  edm::Handle<pat::TriggerObjectStandAloneCollection> trigger_objects;
  event.getByToken(trigger_objects_token, trigger_objects);

  edm::Handle<l1t::JetBxCollection> l1_jets;
  event.getByToken(l1_jets_token, l1_jets);


  //edm::Handle<pat::METCollection> mets;
  //event.getByToken(met_token, mets);


  edm::Handle<pat::MuonCollection> muons;
  event.getByToken(muons_token, muons);

  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByToken(primary_vertex_token, primary_vertices);

  short int npass_filter[mfv::n_filter_paths] = {0};

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

  if (prints > 1) {
    std::cout << "event: (" << event.id().run() << ", " << event.luminosityBlock() << ", " << event.id().event() << ")\n";
    std::cout << " === TRIGGER PATHS === " << "\n";
    for (unsigned int i = 0, n = trigger_results->size(); i < n; ++i)
      std::cout << "Trigger " << trigger_names.triggerName(i) << ": " << (trigger_results->accept(i) ? "PASS" : "fail (or not run)") << "\n";
    std::cout << "\n === TRIGGER OBJECTS === " << "\n";
    for (pat::TriggerObjectStandAlone obj : *trigger_objects) {
      obj.unpackNamesAndLabels(event, *trigger_results);
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
      std::cout << "\t   Paths (" << pathNamesAll.size()<<"/"<<pathNamesLast.size();
      if (pathNamesAll.size() != pathNamesLast.size())
        std::cout << " paths different";
      std::cout << "):    ";
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

  std::unique_ptr<mfv::TriggerFloats> floats(new mfv::TriggerFloats);

  for (pat::TriggerObjectStandAlone obj : *trigger_objects) {
    const size_t nids = obj.filterIds().size();
    bool is_l1 = false;
    bool is_ht = false;
    bool is_cluster = false;
    bool is_photon = false;
    bool is_muon = false;
    bool is_jet = false;

    if (prints) printf("obj pt %f eta %f phi %f coll %s ids (#=%lu)", obj.pt(), obj.eta(), obj.phi(), obj.collection().c_str(), nids);

    for (int id : obj.filterIds()) {
      if (is_l1)
        assert(id < 0);

      if (prints) printf(" %i", id);

      if (id < 0)
        is_l1 = true;
      else if (id == trigger::TriggerTHT)
        is_ht = true;
      else if (id == trigger::TriggerCluster)
        is_cluster = true;
      else if (id == trigger::TriggerPhoton)
        is_photon = true;
      else if (id == trigger::TriggerMuon)
        is_muon = true;
      else if (id == trigger::TriggerBJet || id == trigger::TriggerJet)
        is_jet = true;
    }

    obj.unpackNamesAndLabels(event, *trigger_results);
    for (unsigned h = 0; h < obj.filterLabels().size(); ++h){
      for (unsigned j = 0; j < mfv::n_filter_paths; ++j) {
        // If we see a filter we're looking for and it's NOT an HT/MHT filter, then just tally it
        if ((mfv::filter_paths[j] == obj.filterLabels()[h]) and (obj.filterIds()[0] != 90) and (obj.filterIds()[0] != 89)) {
            npass_filter[j]++;
        }
         // If we see a filter we're looking for and it is an HT filter (id = 89), then we'll check the HT
        else if ((mfv::filter_paths[j] == obj.filterLabels()[h]) and (obj.filterIds()[0] == 89)) {
            npass_filter[j] += obj.pt();
        }
      }
    }

    if (prints) printf(" is_l1 %i is_ht %i is_cluster %i is_photon %i is_muon %i is_jet %i\n", is_l1, is_ht, is_cluster, is_photon, is_muon, is_jet);

    if (is_l1) assert(nids == 1 && !is_ht && !is_cluster && !is_photon && !is_muon && !is_jet);
    if (is_ht) {
      if      (nids == 1) assert(!is_cluster && !is_photon && !is_muon && !is_jet);
      else if (nids == 2) assert(!is_cluster && !is_photon);
      else assert(0);
    }
    const bool is_electron = is_cluster;

    if (is_ht) {
      if (obj.collection() == "hltPFHTJet30::HLT")
        floats->hltht = obj.pt();
      else if (obj.collection() == "hltHtMhtCaloJetsQuadC30::HLT")
        floats->hltcaloht = obj.pt();
    }

    else if (is_electron || is_muon) {
      // for HT above we didn't check the path, there's always only one
      // HT object. there can be many trigger electrons/muons, only store
      // those that were used in the decision, i.e. those that were used
      // in a path we care about.
      obj.unpackNamesAndLabels(event, *trigger_results);
      const std::vector<std::string>& pathNamesAll  = obj.pathNames(false);
      int ipath = -1;
      for (const std::string& p : pathNamesAll) {
        for (int i = 0; i < mfv::n_hlt_paths; ++i)
          if (helper.path_same_without_version(p, mfv::hlt_paths[i])) {
            ipath = i;
            break;
          }
        if (ipath != -1) break;
      }

      if (ipath != -1) {

        if (is_electron) {
          if (obj.collection() == "hltEgammaCandidates::HLT")
            floats->hltelectrons.push_back(p4(obj.pt(), obj.eta(), obj.phi(), obj.energy()));
        }
        else if (is_muon) {
          if (obj.collection() == "hltIterL3MuonCandidates::HLT")
            floats->hltmuons.push_back(p4(obj.pt(), obj.eta(), obj.phi(), obj.energy()));
        }

        if (prints) {
          std::cout << "TriggerFloats lepton object for path " << mfv::hlt_paths[ipath]
                    << " pt " << obj.pt() << " eta " << obj.eta() << " phi " << obj.phi()
                    << " collection: " << obj.collection() << " ids (# = " << obj.filterIds().size() << "):";
          for (auto id : obj.filterIds())
            std::cout << " " << id;
          std::cout << "\n";
        }
      }
    }
    else if (is_jet) {
      obj.unpackNamesAndLabels(event, *trigger_results);
      const std::vector<std::string>& pathNamesAll  = obj.pathNames(false);
      int ipath = -1;
      for (const std::string& p : pathNamesAll) {
        for (int i = 0; i < mfv::n_hlt_paths; ++i){
          if (helper.path_same_without_version(p, mfv::hlt_paths[i])) {
            ipath = i;
            break;
          }
        }
        if (ipath != -1) break;
      }

      // FIXME - keep all hlt CaloJetsCorrected objects for now. Move this into the following conditional when done
      if(obj.collection() == "hltAK4CaloJetsCorrected::HLT"){
        floats->hltcalojets.push_back(p4(obj.pt(), obj.eta(), obj.phi(), obj.energy()));
      }

      // Low(er)-momentum calo jets with not very many prompt tracks
      if(obj.collection() == "hltDisplacedHLTCaloJetCollectionProducerLowPt::HLT") {
        floats->hltcalojets_lowpt_fewprompt.push_back(p4(obj.pt(), obj.eta(), obj.phi(), obj.energy()));
      }

      // Low(er)-momentum calo jets with at least one displaced track
      if(obj.collection() == "hltIter02DisplacedHLTCaloJetCollectionProducerLowPt::HLT") {
        floats->hltcalojets_lowpt_wdisptks.push_back(p4(obj.pt(), obj.eta(), obj.phi(), obj.energy()));
      }

      // Mid-momentum calo hets with not very many prompt tracks (Kinda redundant, can delete. But I'll keep for now) 
      if(obj.collection() == "hltDisplacedHLTCaloJetCollectionProducerMidPt::HLT") {
        floats->hltcalojets_midpt_fewprompt.push_back(p4(obj.pt(), obj.eta(), obj.phi(), obj.energy()));
      }

      if (ipath != -1) {

        // Note that all of the bjet triggers use PF jets for the kinematics, and the
        // b-tagging discriminants aren't currently available in AODs, so this is
        // sufficient for the trigger matching for now
        if(obj.collection() == "hltAK4PFJetsCorrected::HLT"){
          floats->hltpfjets.push_back(p4(obj.pt(), obj.eta(), obj.phi(), obj.energy()));
        }
        else if(obj.collection() == "hltDisplacedHLTCaloJetCollectionProducerLowPt::HLT" || obj.collection() == "hltDisplacedHLTCaloJetCollectionProducerMidPt::HLT"){
          floats->hltdisplacedcalojets.push_back(p4(obj.pt(), obj.eta(), obj.phi(), obj.energy()));
        }
        else if(obj.collection() == "hltAK4CaloJetsCorrectedIDPassed::HLT") {
          floats->hltidpassedcalojets.push_back(p4(obj.pt(), obj.eta(), obj.phi(), obj.energy()));
        }
        else if(obj.collection() == "hltPFJetForBtag::HLT") {
          bool save_this_jet = false;
          for (auto label : obj.filterLabels()) {
            if (label == "hltBTagPFCSVp070Triple") { save_this_jet = true; }
          }
          if (save_this_jet) {
            floats->hltpfjetsforbtag.push_back(p4(obj.pt(), obj.eta(), obj.phi(), obj.energy()));
          }
        }

        if (prints) {
          std::cout << "TriggerFloats jet object for path " << mfv::hlt_paths[ipath]
                    << " pt " << obj.pt() << " eta " << obj.eta() << " phi " << obj.phi()
                    << " collection: " << obj.collection() << " ids (# = " << obj.filterIds().size() << "):";
          for (auto id : obj.filterIds())
            std::cout << " " << id;
          std::cout << "\n";
        }
      }
    }
  }

  for (size_t i = 0, ie = l1_jets->size(0); i < ie; ++i) {
    const l1t::Jet& jet = l1_jets->at(0, i);
    if (i > 0) assert(jet.pt() <= l1_jets->at(0, i-1).pt());
    if (fabs(jet.eta()) < 3)
      floats->l1jets.push_back(p4(jet.pt(), jet.eta(), jet.phi(), jet.energy()));
  }

  floats->l1htt = etsumhelper.TotalHt();
  floats->myhtt = my_htt;
  floats->myhttwbug = my_htt_wbug;
//  floats->met_pt = met_pt;
//  floats->met_phi = met_phi;
//  floats->met_pt_calo = met.caloMETPt();
//  floats->met_pt_nomu = met_nomu_pt;
//  floats->met_phi_nomu = met_nomu_phi;
//  floats->pass_metfilters = pass_all_metfilters;

  if (prints)
    printf("TriggerFloats: hltht = %f\n", floats->hltht);

  for (int i = 0; i < mfv::n_hlt_paths; ++i) {
    const std::pair<bool, bool> paf = helper.pass_and_found_any_version(mfv::hlt_paths[i]);
    if (paf.second)
      floats->HLTdecisions[i] = paf.first;

    if (prints)
      printf("HLT bit %2i %20s: %2i\n", i, mfv::hlt_paths[i], floats->HLTdecisions[i]);
  }

  if (prints) {
    printf("TriggerFloats: event passed HLT for");
    for (int i = 0; i < mfv::n_hlt_paths; ++i)
      if (floats->HLTdecisions[i])
        printf(" %s", mfv::hlt_paths[i]);
    printf("\n");
  }

  edm::Handle<GlobalAlgBlkBxCollection> l1_results_all;
  event.getByToken(l1_results_token, l1_results_all);
  const std::vector<bool>& l1_results = l1_results_all->at(0, 0).getAlgoDecisionFinal();

  edm::ESHandle<L1TUtmTriggerMenu> l1_menu;
  setup.get<L1TUtmTriggerMenuRcd>().get(l1_menu);

  for (int i = 0; i < mfv::n_l1_paths; ++i) {
    const auto& m = l1_menu->getAlgorithmMap();
    const auto& e = m.find(mfv::l1_paths[i]);
    const bool found = e != m.end();
    const bool pass = found ? l1_results[e->second.getIndex()] : false;

    if (found) floats->L1decisions[i] = pass;

    if (prints)
      printf("L1  bit %2i %20s: %2i\n", i, mfv::l1_paths[i], floats->L1decisions[i]);
  }

  for (int i = 0; i < mfv::n_filter_paths; ++i) { 
    if (npass_filter[i] >= mfv::filter_nreqs[i])
      floats->FLTdecisions[i] = true;
    else
      floats->FLTdecisions[i] = false;
  }

  edm::Handle<pat::JetCollection> jets;
  event.getByToken(jets_token, jets);

  floats->nalljets = jets->size();

  for (const pat::Jet& jet : *jets)
    if (jet_selector(jet)) {
      const double pt = jet.pt();
      floats->jets.push_back(p4(pt, jet.eta(), jet.phi(), jet.energy()));
      floats->jetmuef.push_back(jet.muonEnergyFraction());

      floats->htall += pt;
      if (pt > 30) floats->htptgt30 += pt;
      if (pt > 40) floats->ht += pt;
    }

  if (prints) {
    printf("# all jets: %lu  selected: %i (>30GeV: %i) jetpt1: %f  2: %f  ht(30): %f\n", jets->size(), floats->njets(), floats->njets(30), floats->jetpt1(), floats->jetpt2(), floats->htptgt30);
    for (int i = 0; i < mfv::n_filter_paths; ++i)
      printf("%s,  npass: %i   Filter Passed: %i \n", mfv::filter_paths[i], npass_filter[i], floats->FLTdecisions[i]);
  }

  event.put(std::move(floats));
}

DEFINE_FWK_MODULE(MFVTriggerFloats);
