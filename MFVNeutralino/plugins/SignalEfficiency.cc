#include "TH1F.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"
#include "DataFormats/Math/interface/deltaR.h"

class SignalEfficiency : public edm::EDAnalyzer {
 public:
  explicit SignalEfficiency(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);
 
 private:
  const edm::InputTag trigger_results_src;
  const edm::InputTag jet_src;
  const double min_jet_pt;
  const double max_jet_eta;
  const edm::InputTag primary_vertex_src;
  const edm::InputTag muon_src;
  const int min_nmuons;
  const bool muon_dxymax;
  const std::string b_discriminator_name;
  const double bdisc_min;
  const int min_nbtags;

  TH1F* h_njets;
  TH1F* h_6jets;
  TH1F* h_7jets;
  TH1F* h_8jets;
};

SignalEfficiency::SignalEfficiency(const edm::ParameterSet& cfg)
  : trigger_results_src(cfg.getParameter<edm::InputTag>("trigger_results_src")),
    jet_src(cfg.getParameter<edm::InputTag>("jet_src")),
    min_jet_pt(cfg.getParameter<double>("min_jet_pt")),
    max_jet_eta(cfg.getParameter<double>("max_jet_eta")),
    primary_vertex_src(cfg.getParameter<edm::InputTag>("primary_vertex_src")),
    muon_src(cfg.getParameter<edm::InputTag>("muon_src")),
    min_nmuons(cfg.getParameter<int>("min_nmuons")),
    muon_dxymax(cfg.getParameter<bool>("muon_dxymax")),
    b_discriminator_name(cfg.getParameter<std::string>("b_discriminator_name")),
    bdisc_min(cfg.getParameter<double>("bdisc_min")),
    min_nbtags(cfg.getParameter<int>("min_nbtags"))
{
  edm::Service<TFileService> fs;
  h_njets = fs->make<TH1F>("h_njets", ";number of jets before analysis cuts;events", 100, 0, 100);
  h_6jets = fs->make<TH1F>("h_6jets", ";number of btags;events with 6 jets", 4, 1, 5);
  h_7jets = fs->make<TH1F>("h_7jets", ";number of btags;events with 7 jets", 4, 1, 5);
  h_8jets = fs->make<TH1F>("h_8jets", ";number of btags;events with >=8 jets", 4, 1, 5);
}

void SignalEfficiency::analyze(const edm::Event& event, const edm::EventSetup& setup) {

  edm::Handle<edm::TriggerResults> trigger_results;
  event.getByLabel(trigger_results_src, trigger_results);
  const edm::TriggerNames& trigger_names = event.triggerNames(*trigger_results);
  const size_t npaths = trigger_names.size();

  const bool simple_trigger[2] = { true, true };
  const std::string try_trigger[2] = {
    "HLT_IsoMu24_v", "HLT_IsoMu24_eta2p1_v"
  };
  bool pass_trigger[2] = { false, false };

  for (int itry = 0; itry < 2; ++itry) {
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

  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByLabel(primary_vertex_src, primary_vertices);
  const reco::Vertex& pv = primary_vertices->at(0);

  edm::Handle<pat::MuonCollection> muons;
  event.getByLabel(muon_src, muons);
  int nmuons = 0;
  std::vector<pat::Muon> good_muons;
  for (int i = 0; i < int(muons->size()); ++i) {
    const pat::Muon& muon = muons->at(i);
    const reco::Track& tk = *muon.bestTrack();
  
    bool good = 
      muon.isPFMuon() &&
      ((muon::isGoodMuon(muon, muon::GlobalMuonPromptTight) && muon.numberOfMatchedStations() > 1) || muon::isGoodMuon(muon, muon::TMLastStationTight)) &&
      muon.pt() > 35 &&
      fabs(muon.eta()) < 2.1 &&
      tk.hitPattern().numberOfValidTrackerHits() > 5 &&
      tk.hitPattern().numberOfValidPixelHits() > 0 &&
      tk.ptError()/tk.pt() < 0.1 &&
      muon.combinedQuality().trkKink < 20 &&
      (muon.chargedHadronIso() + muon.neutralHadronIso() + muon.photonIso() - 0.5*muon.puChargedHadronIso())/muon.pt() < 0.1;

    if (muon_dxymax) {
      const double dxymax = muon.pt() > 20 ? 0.02 : 0.01;
      good = good && fabs(tk.dxy(pv.position())) < dxymax && fabs(tk.dz(pv.position())) < 0.1;
    }

    if (good) {
      ++nmuons;
      good_muons.push_back(muon);
    }
  }
  bool pass_nmuons = nmuons >= min_nmuons;

  edm::Handle<pat::JetCollection> jets;
  event.getByLabel(jet_src, jets);
  h_njets->Fill(int(jets->size()));
  int njets = 0;
  int nbtags = 0;
  for (int i = 0; i < int(jets->size()); ++i) {
    const pat::Jet& jet = jets->at(i);
    const double bdisc = jet.bDiscriminator(b_discriminator_name);
    if (jet.pt() > min_jet_pt && fabs(jet.eta()) < max_jet_eta) {
      bool jet_deltaR = true;
      for (int j = 0; j < int(good_muons.size()); ++j) {
        const pat::Muon& muon = good_muons[j];
        if (deltaR(jet, muon) < 0.5) {
          jet_deltaR = false;
        }
      }
      if (jet_deltaR) {
        ++njets;
        if (bdisc > bdisc_min) {
          ++nbtags;
        }
      }
    }
  }
  bool pass_nbtags = nbtags >= min_nbtags;

  if ((pass_trigger[0] || pass_trigger[1]) && pass_nbtags && pass_nmuons) {
    if (njets == 6) h_6jets->Fill(nbtags);
    if (njets == 7) h_7jets->Fill(nbtags);
    if (njets >= 8) h_8jets->Fill(nbtags);
  }

}

DEFINE_FWK_MODULE(SignalEfficiency);
