#include "TH2F.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "CMGTools/External/interface/PileupJetIdentifier.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"

class HadronicNBAnalysis : public edm::EDAnalyzer {
 public:
  explicit HadronicNBAnalysis(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);
 
 private:
  const edm::InputTag trigger_results_src;
  const edm::InputTag jet_src;
  const int min_njets;
  const double min_jet_pt;
  const double min_1st_jet_pt;
  const std::string b_discriminator_name;
  const int min_nbtags;
  const double bdisc_min;
  const edm::InputTag muon_src;
  const edm::InputTag electron_src;

  TH1F* h_njets;
  TH1F* h_jet_pt;
  TH1F* h_jet_eta;
  TH1F* h_njets_cut;
  TH1F* h_nbtags;
  TH1F* h_nbtags_cut;

  TH1F* h_6jets;
  TH1F* h_7jets;
  TH1F* h_8jets;
};

HadronicNBAnalysis::HadronicNBAnalysis(const edm::ParameterSet& cfg)
  : trigger_results_src(cfg.getParameter<edm::InputTag>("trigger_results_src")),
    jet_src(cfg.getParameter<edm::InputTag>("jet_src")),
    min_njets(cfg.getParameter<int>("min_njets")),
    min_jet_pt(cfg.getParameter<double>("min_jet_pt")),
    min_1st_jet_pt(cfg.getParameter<double>("min_1st_jet_pt")),
    b_discriminator_name(cfg.getParameter<std::string>("b_discriminator_name")),
    min_nbtags(cfg.getParameter<int>("min_nbtags")),
    bdisc_min(cfg.getParameter<double>("bdisc_min")),
    muon_src(cfg.getParameter<edm::InputTag>("muon_src")),
    electron_src(cfg.getParameter<edm::InputTag>("electron_src"))
{
  edm::Service<TFileService> fs;

  h_njets = fs->make<TH1F>("h_njets", ";number of jets before cuts;events", 20, 0, 20);
  h_jet_pt = fs->make<TH1F>("h_jet_pt", ";jet pt;number of jets", 100, 0, 1000);
  h_jet_eta = fs->make<TH1F>("h_jet_eta", ";jet eta;number of jets", 40, -3, 3);
  h_njets_cut = fs->make<TH1F>("h_njets_cut", ";number of jets after cuts;events", 20, 0, 20);
  h_nbtags = fs->make<TH1F>("h_nbtags", ";number of btags before cuts;events", 20, 0, 20);
  h_nbtags_cut = fs->make<TH1F>("h_nbtags_cut", ";number of btags after cuts;events", 20, 0, 20);

  h_6jets = fs->make<TH1F>("h_6jets", ";number of btags;events with 6 jets", 4, 1, 5);
  h_7jets = fs->make<TH1F>("h_7jets", ";number of btags;events with 7 jets", 4, 1, 5);
  h_8jets = fs->make<TH1F>("h_8jets", ";number of btags;events with >=8 jets", 4, 1, 5);
}

void HadronicNBAnalysis::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<edm::TriggerResults> trigger_results;
  event.getByLabel(trigger_results_src, trigger_results);
  const edm::TriggerNames& trigger_names = event.triggerNames(*trigger_results);
  const size_t npaths = trigger_names.size();

  const bool simple_trigger[1] = { true };
  const std::string try_trigger[1] = {
    "HLT_HT750_v"
  };
  bool pass_trigger[1] = { false };

  for (int itry = 0; itry < 1; ++itry) {
    if (simple_trigger[itry]) {
      const std::string& trigger = try_trigger[itry];

      for (size_t ipath = 0; ipath < npaths; ++ipath) {
        const std::string path = trigger_names.triggerName(ipath);
        if (path.substr(0, trigger.size()) == trigger) {
          pass_trigger[itry] = trigger_results->accept(ipath);
          break;
        }
      }
    }
    else {
      assert(0);
    }
  }

  edm::Handle<pat::JetCollection> jets;
  event.getByLabel(jet_src, jets);

  h_njets->Fill(int(jets->size()));
  int njets = 0;
  int nbtags = 0;
  int nbtags_nocuts = 0;
  bool pass_njets = false;
  double sum_ht = 0;
  for (int i = 0; i < int(jets->size()); ++i) {
    const pat::Jet& jet = jets->at(i);
    h_jet_pt->Fill(jet.pt());
    h_jet_eta->Fill(jet.eta());
    const double bdisc = jet.bDiscriminator(b_discriminator_name);
    if (bdisc > bdisc_min) {
      ++nbtags_nocuts;
    }

    if (i == 0 && jet.pt() > min_1st_jet_pt) pass_njets = true;
    if (jet.pt() > min_jet_pt) {
      ++njets;
      sum_ht += jet.pt();
      if (bdisc > bdisc_min) {
        ++nbtags;
      }
    }
  }
  h_nbtags->Fill(nbtags_nocuts);
  pass_njets = pass_njets && njets >= min_njets;
  bool pass_nbtags = nbtags >= min_nbtags;

  edm::Handle<pat::MuonCollection> muons;
  event.getByLabel(muon_src, muons);

  edm::Handle<pat::ElectronCollection> electrons;
  event.getByLabel(electron_src, electrons);

  if (pass_trigger[0] && pass_njets && pass_nbtags && int(muons->size()) == 0 && int(electrons->size()) == 0) {
    h_njets_cut->Fill(njets);
    h_nbtags_cut->Fill(nbtags);

    if (sum_ht > 1750) { 
    if (njets == 6) h_6jets->Fill(nbtags);
    if (njets == 7) h_7jets->Fill(nbtags);
    if (njets >= 8) h_8jets->Fill(nbtags);
    }
  }
}

DEFINE_FWK_MODULE(HadronicNBAnalysis);
