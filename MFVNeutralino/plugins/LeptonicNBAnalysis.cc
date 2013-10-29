#include "TH2F.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "CMGTools/External/interface/PileupJetIdentifier.h"

class LeptonicNBAnalysis : public edm::EDAnalyzer {
 public:
  explicit LeptonicNBAnalysis(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);
 
 private:
  const edm::InputTag trigger_results_src;
  const edm::InputTag primary_vertex_src;
  const edm::InputTag secondary_vertex_src;
  const edm::InputTag muon_src;
  const int min_nmuons;
  const edm::InputTag jet_src;
  const double min_jet_pt;
  const double max_jet_eta;
  const int min_njets;
  const std::string b_discriminator_name;
  const double bdisc_min;
  const int min_nbtags;

  const bool muon_stations_min;
  const bool muon_trackerhits_min;
  const bool muon_pixelhits_min;
  const bool muon_dxy_max;
  const bool muon_dz_max;
  const bool muon_eta_max;
  const bool muon_tkpterror_max;
  const bool muon_trkkink_max;
  const bool muon_pt_min;
  const bool muon_iso_max;

  TH1F* h_nmuons;
  TH1F* h_muon_pt;
  TH1F* h_muon_eta;
  TH1F* h_nmuons_cut;
  TH1F* h_njets;
  TH1F* h_jet_pt;
  TH1F* h_jet_eta;
  TH1F* h_jet_deltaR;
  TH1F* h_njets_puJetId;
  TH1F* h_njets_cut;
  TH1F* h_nbtags;
  TH1F* h_nbtags_cut;
  TH2F* h_ntracks01_v_maxtrackpt01;

  TH1F* h_6jets;
  TH1F* h_7jets;
  TH1F* h_8jets;
};

LeptonicNBAnalysis::LeptonicNBAnalysis(const edm::ParameterSet& cfg)
  : trigger_results_src(cfg.getParameter<edm::InputTag>("trigger_results_src")),
    primary_vertex_src(cfg.getParameter<edm::InputTag>("primary_vertex_src")),
    secondary_vertex_src(cfg.getParameter<edm::InputTag>("secondary_vertex_src")),
    muon_src(cfg.getParameter<edm::InputTag>("muon_src")),
    min_nmuons(cfg.getParameter<int>("min_nmuons")),
    jet_src(cfg.getParameter<edm::InputTag>("jet_src")),
    min_jet_pt(cfg.getParameter<double>("min_jet_pt")),
    max_jet_eta(cfg.getParameter<double>("max_jet_eta")),
    min_njets(cfg.getParameter<int>("min_njets")),
    b_discriminator_name(cfg.getParameter<std::string>("b_discriminator_name")),
    bdisc_min(cfg.getParameter<double>("bdisc_min")),
    min_nbtags(cfg.getParameter<int>("min_nbtags")),
    muon_stations_min(cfg.getParameter<bool>("muon_stations_min")),
    muon_trackerhits_min(cfg.getParameter<bool>("muon_trackerhits_min")),
    muon_pixelhits_min(cfg.getParameter<bool>("muon_pixelhits_min")),
    muon_dxy_max(cfg.getParameter<bool>("muon_dxy_max")),
    muon_dz_max(cfg.getParameter<bool>("muon_dz_max")),
    muon_eta_max(cfg.getParameter<bool>("muon_eta_max")),
    muon_tkpterror_max(cfg.getParameter<bool>("muon_tkpterror_max")),
    muon_trkkink_max(cfg.getParameter<bool>("muon_trkkink_max")),
    muon_pt_min(cfg.getParameter<bool>("muon_pt_min")),
    muon_iso_max(cfg.getParameter<bool>("muon_iso_max"))
{
  edm::Service<TFileService> fs;

  h_nmuons = fs->make<TH1F>("h_nmuons", ";number of muons before cuts;events", 10, 0, 10);
  h_muon_pt = fs->make<TH1F>("h_muon_pt", ";muon pt;number of muons", 100, 0, 1000);
  h_muon_eta = fs->make<TH1F>("h_muon_eta", ";muon eta;number of muons", 40, -3, 3);
  h_nmuons_cut = fs->make<TH1F>("h_nmuons_cut", ";number of muons after cuts;events", 10, 0, 10);
  h_njets = fs->make<TH1F>("h_njets", ";number of jets before cuts;events", 20, 0, 20);
  h_jet_pt = fs->make<TH1F>("h_jet_pt", ";jet pt;number of jets", 100, 0, 1000);
  h_jet_eta = fs->make<TH1F>("h_jet_eta", ";jet eta;number of jets", 40, -3, 3);
  h_jet_deltaR = fs->make<TH1F>("h_jet_deltaR", ";pass_jet_deltaR;number of jets", 2, 0, 2);
  h_njets_puJetId = fs->make<TH1F>("h_njets_puJetId", ";number of jets that pass loose puJetId cut;events", 20, 0, 20);
  h_njets_cut = fs->make<TH1F>("h_njets_cut", ";number of jets after cuts;events", 20, 0, 20);
  h_nbtags = fs->make<TH1F>("h_nbtags", ";number of btags before cuts;events", 20, 0, 20);
  h_nbtags_cut = fs->make<TH1F>("h_nbtags_cut", ";number of btags after cuts;events", 20, 0, 20);
  h_ntracks01_v_maxtrackpt01 = fs->make<TH2F>("h_ntracks01_v_maxtrackpt01", ";sum of maxtrackpt for the two SV's with the highest ntracks;sum of ntracks of the two SV's with the highest ntracks", 300, 0, 300, 80, 0, 80);

  h_6jets = fs->make<TH1F>("h_6jets", ";number of btags;events with 6 jets", 4, 1, 5);
  h_7jets = fs->make<TH1F>("h_7jets", ";number of btags;events with 7 jets", 4, 1, 5);
  h_8jets = fs->make<TH1F>("h_8jets", ";number of btags;events with >=8 jets", 4, 1, 5);
}

void LeptonicNBAnalysis::analyze(const edm::Event& event, const edm::EventSetup& setup) {

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
  h_nmuons->Fill(muons->size());
  int nmuons = 0;
  std::vector<pat::Muon> good_muons;
  for (int i = 0; i < int(muons->size()); ++i) {
    const pat::Muon& muon = muons->at(i);
    h_muon_pt->Fill(muon.pt());
    h_muon_eta->Fill(muon.eta());
    const reco::Track& tk = *muon.bestTrack();

    bool good = muon.isPFMuon();
    if (muon_stations_min)    good = good && ((muon::isGoodMuon(muon, muon::GlobalMuonPromptTight) && muon.numberOfMatchedStations() > 1) || muon::isGoodMuon(muon, muon::TMLastStationTight));
    if (muon_trackerhits_min) good = good && tk.hitPattern().numberOfValidTrackerHits() > 5;
    if (muon_pixelhits_min)   good = good && tk.hitPattern().numberOfValidPixelHits() > 0;
    if (muon_dxy_max) {
      const double dxymax = muon.pt() > 20 ? 0.02 : 0.01;
      good = good && fabs(tk.dxy(pv.position())) < dxymax;
    }
    if (muon_dz_max)          good = good && fabs(tk.dz(pv.position())) < 0.1;
    if (muon_eta_max)         good = good && abs(muon.eta()) < 2.1;
    if (muon_tkpterror_max)   good = good && tk.ptError()/tk.pt() < 0.1;
    if (muon_trkkink_max)     good = good && muon.combinedQuality().trkKink < 20;
    if (muon_pt_min)          good = good && muon.pt() > 35;
    if (muon_iso_max)         good = good && (muon.chargedHadronIso() + muon.neutralHadronIso() + muon.photonIso() - 0.5*muon.puChargedHadronIso())/muon.pt() < 0.1;

    if (good) {
      ++nmuons;
      good_muons.push_back(muon);
    }
  }
  bool pass_nmuons = nmuons >= min_nmuons;

  edm::Handle<pat::JetCollection> jets;
  event.getByLabel(jet_src, jets);

  edm::Handle<edm::ValueMap<float> > puJetIdMva;
  event.getByLabel("puJetMvaChs", "fullDiscriminant", puJetIdMva);

  edm::Handle<edm::ValueMap<int> > puJetIdFlag;
  event.getByLabel("puJetMvaChs", "fullId", puJetIdFlag);

  h_njets->Fill(int(jets->size()));
  int njets = 0;
  int njets_puJetId = 0;
  int nbtags = 0;
  int nbtags_nocuts = 0;
  for (int i = 0; i < int(jets->size()); ++i) {
    pat::JetRef jetref(jets, i);
    float mva   = (*puJetIdMva)[jetref];
    int idflag = (*puJetIdFlag)[jetref];

/*
    std::cout << "jet " << i << " pt " << jetref->pt() << " eta " << jetref->eta() << " PU JetID MVA " << mva;
    if (PileupJetIdentifier::passJetId(idflag, PileupJetIdentifier::kLoose)) {
      std::cout << " pass loose wp";
    }
    if (PileupJetIdentifier::passJetId(idflag, PileupJetIdentifier::kMedium)) {
      std::cout << " pass medium wp";
    }
    if (PileupJetIdentifier::passJetId(idflag, PileupJetIdentifier::kTight)) {
      std::cout << " pass tight wp";
    }
    std::cout << "\n";
*/

    if (PileupJetIdentifier::passJetId(idflag, PileupJetIdentifier::kLoose)) {
      ++njets_puJetId;
    }

    const pat::Jet& jet = jets->at(i);
    h_jet_pt->Fill(jet.pt());
    h_jet_eta->Fill(jet.eta());
    const double bdisc = jet.bDiscriminator(b_discriminator_name);
    if (bdisc > bdisc_min) {
      ++nbtags_nocuts;
    }
    bool jet_deltaR = true;
    for (int j = 0; j < int(good_muons.size()); ++j) {
      const pat::Muon& muon = good_muons[j];
      if (deltaR(jet, muon) < 0.5) {
        jet_deltaR = false;
      }
    }
    h_jet_deltaR->Fill(jet_deltaR);
    if (jet.pt() > min_jet_pt && fabs(jet.eta()) < max_jet_eta && jet_deltaR && PileupJetIdentifier::passJetId(idflag, PileupJetIdentifier::kLoose)) {
      ++njets;
      if (bdisc > bdisc_min) {
        ++nbtags;
      }
    }
  }
  h_njets_puJetId->Fill(njets_puJetId);
  h_nbtags->Fill(nbtags_nocuts);
  bool pass_njets = njets >= min_njets;
  bool pass_nbtags = nbtags >= min_nbtags;

  edm::Handle<reco::VertexCollection> secondary_vertices;
  event.getByLabel(secondary_vertex_src, secondary_vertices);
  int ntracks0 = 0;
  int ntracks1 = 0;
  double maxtrackpt0 = 0;
  double maxtrackpt1 = 0;
  for (int i = 0; i < int(secondary_vertices->size()); ++i) {
    const reco::Vertex& sv = secondary_vertices->at(i);
    auto trkb = sv.tracks_begin();
    auto trke = sv.tracks_end();
    int ntracks = trke - trkb;

    std::vector<double> trackpts;
    for (auto trki = trkb; trki != trke; ++trki) {
      const reco::TrackBaseRef& tri = *trki;
      double pti = tri->pt();
      trackpts.push_back(pti);
    }
    std::sort(trackpts.begin(), trackpts.end());
    const double maxtrackpt = trackpts[trackpts.size()-1];

    if (ntracks > ntracks0) {
      ntracks1 = ntracks0;
      ntracks0 = ntracks;
      maxtrackpt1 = maxtrackpt0;
      maxtrackpt0 = maxtrackpt;
    } else if (ntracks > ntracks1) {
      ntracks1 = ntracks;
      maxtrackpt1 = maxtrackpt;
    }
  }

  if ((pass_trigger[0] || pass_trigger[1]) && pass_nmuons && pass_njets && pass_nbtags) {
    h_nmuons_cut->Fill(nmuons);
    h_njets_cut->Fill(njets);
    h_nbtags_cut->Fill(nbtags);
    h_ntracks01_v_maxtrackpt01->Fill(maxtrackpt0 + maxtrackpt1, ntracks0 + ntracks1);

    if (njets == 6) h_6jets->Fill(nbtags);
    if (njets == 7) h_7jets->Fill(nbtags);
    if (njets >= 8) h_8jets->Fill(nbtags);

  }

}

DEFINE_FWK_MODULE(LeptonicNBAnalysis);
