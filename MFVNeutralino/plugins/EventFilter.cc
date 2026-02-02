#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "RecoEgamma/EgammaTools/interface/EffectiveAreas.h"
#include "SimDataFormats/GeneratorProducts/interface/GenLumiInfoHeader.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "JMTucker/Tools/interface/TriggerHelper.h"

class MFVEventFilter : public edm::EDFilter {
public:
  explicit MFVEventFilter(const edm::ParameterSet&);
private:
  bool filter(edm::Event&, const edm::EventSetup&) override;
  bool trigger_veto(edm::Event& event, const std::vector<std::string> trigger_list);
  struct Mode {
    enum mode_t { either, jets_only, muons_only, electrons_only_veto_muons, leptons_only, HT_OR_bjets_OR_displaced_dijet, bjets_OR_displaced_dijet_veto_leptons_and_HT, bjets_OR_displaced_dijet_veto_HT, MET_only, lep_OR_displaced_lep};
    const mode_t mode;
    Mode(const std::string& m) : mode(m == "MET only" ? MET_only : m == "bjets OR displaced dijet veto leptons and HT" ? bjets_OR_displaced_dijet_veto_leptons_and_HT : m == "bjets OR displaced dijet veto HT" ? bjets_OR_displaced_dijet_veto_HT : m == "HT OR bjets OR displaced dijet" ? HT_OR_bjets_OR_displaced_dijet : m == "muons only" ? muons_only : m == "electrons only veto muons" ? electrons_only_veto_muons : m == "leptons only" ? leptons_only : m == "lep or displaced lep" ? lep_OR_displaced_lep : m == "jets only" ? jets_only : either) {}
    bool operator==(mode_t m) const { return mode == m; }
  };
  const Mode mode;

  const edm::EDGetTokenT<GenLumiInfoHeader> gen_lumi_header_token; // for randpar parsing
  const edm::EDGetTokenT<pat::JetCollection> jets_token;
  const edm::EDGetTokenT<edm::TriggerResults> trigger_results_token;
  const StringCutObjectSelector<pat::Jet> jet_selector;
  const int min_njets;
  const double min_pt_for_ht;
  const double min_ht;
  const edm::EDGetTokenT<pat::MuonCollection> muons_token;
  const double min_muon_pt;
  const edm::EDGetTokenT<pat::ElectronCollection> electrons_token;
  const double min_electron_pt;
  const int min_nleptons;
  const bool veto_bjet_triggers;
  const std::vector<std::string> bjet_triggers_to_veto;
  const bool veto_lepton_triggers;
  const std::vector<std::string> lepton_triggers_to_veto;
  EffectiveAreas electron_effective_areas;
  const edm::EDGetTokenT<double> rho_token;
  const bool parse_randpars;
  const int randpar_mass;
  const std::string randpar_ctau;
  const std::string randpar_dcay;
  const bool debug;
};


MFVEventFilter::MFVEventFilter(const edm::ParameterSet& cfg)
  : mode(cfg.getParameter<std::string>("mode")),
    gen_lumi_header_token(consumes<GenLumiInfoHeader, edm::InLumi>(edm::InputTag("generator"))),
    jets_token(consumes<pat::JetCollection>(cfg.getParameter<edm::InputTag>("jets_src"))),
    trigger_results_token(consumes<edm::TriggerResults>(cfg.getParameter<edm::InputTag>("trigger_results_src"))),
    jet_selector(cfg.getParameter<std::string>("jet_cut")),
    min_njets(cfg.getParameter<int>("min_njets")),
    min_pt_for_ht(cfg.getParameter<double>("min_pt_for_ht")),
    min_ht(cfg.getParameter<double>("min_ht")),
    muons_token(consumes<pat::MuonCollection>(cfg.getParameter<edm::InputTag>("muons_src"))),
    min_muon_pt(cfg.getParameter<double>("min_muon_pt")),
    electrons_token(consumes<pat::ElectronCollection>(cfg.getParameter<edm::InputTag>("electrons_src"))),
    min_electron_pt(cfg.getParameter<double>("min_electron_pt")),
    min_nleptons(cfg.getParameter<int>("min_nleptons")),
    veto_bjet_triggers(cfg.getParameter<bool>("veto_bjet_triggers")),
    bjet_triggers_to_veto(cfg.getParameter<std::vector<std::string>>("bjet_triggers_to_veto")),
    veto_lepton_triggers(cfg.getParameter<bool>("veto_lepton_triggers")),
    lepton_triggers_to_veto(cfg.getParameter<std::vector<std::string>>("lepton_triggers_to_veto")),
    electron_effective_areas(cfg.getParameter<edm::FileInPath>("electron_effective_areas").fullPath()),
    rho_token(consumes<double>(cfg.getParameter<edm::InputTag>("rho_src"))),
    parse_randpars(cfg.getParameter<bool>("parse_randpars")),
    randpar_mass(cfg.getParameter<int>("randpar_mass")),
    randpar_ctau(cfg.getParameter<std::string>("randpar_ctau")),
    randpar_dcay(cfg.getParameter<std::string>("randpar_dcay")),
    debug(cfg.getUntrackedParameter<bool>("debug", false))
{
}
bool MFVEventFilter::filter(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<pat::JetCollection> jets;
  event.getByToken(jets_token, jets);
  
  edm::Handle<edm::TriggerResults> trigger_results;
  event.getByToken(trigger_results_token, trigger_results);
  const edm::TriggerNames& trigger_names = event.triggerNames(*trigger_results);
  TriggerHelper helper(*trigger_results, trigger_names);
  const edm::LuminosityBlock& lumi = event.getLuminosityBlock();
  
  // If pertinent, parse randpar configuration
  if (parse_randpars) {
    
    edm::Handle<GenLumiInfoHeader> gen_header;
    lumi.getByToken(gen_lumi_header_token, gen_header);
    
    std::string rp_config_desc = gen_header->configDescription();
    std::string str_mass = "MS-" + std::to_string(randpar_mass);
    std::string str_ctau = "ctauS-" + randpar_ctau;
    std::string str_dcay = randpar_dcay;
    std::string comp_string_Zn = "ZH_" + str_dcay + "_ZToLL_MH-125_" + str_mass + "_" + str_ctau + "_TuneCP5_13TeV-powheg-pythia8";
    std::string comp_string_Wp = "WplusH_HToSSTodddd_WToLNu_MH-125_" + str_mass + "_" + str_ctau + "_TuneCP5_13TeV-powheg-pythia8";
    if (not ((comp_string_Wp == rp_config_desc) or (comp_string_Zn == rp_config_desc))) {
      return false;
    }
    else {
      return true;
    }
  }

  if (veto_bjet_triggers) {
    for (auto trigger_to_veto : bjet_triggers_to_veto) {
        if (helper.pass_any_version(trigger_to_veto)) return false;
    }
  }

  int njets = 0;
  double ht = 0;
  for (const pat::Jet& jet : *jets)
    if (jet_selector(jet)) {
        ++njets;
        if (jet.pt() > min_pt_for_ht)
            ht += jet.pt();
    }

  const bool jets_pass = njets >= min_njets && ht >= min_ht;

  //leptons 
  edm::Handle<pat::MuonCollection> muons;
  edm::Handle<pat::ElectronCollection> electrons;
  event.getByToken(muons_token, muons);
  event.getByToken(electrons_token, electrons);
  
  edm::Handle<double> rho;
  event.getByToken(rho_token, rho);

  int nmuons = 0, nelectrons = 0;
  bool leptons_pass = nmuons + nelectrons >= min_nleptons;
  bool muons_pass = false; //to safeguard against double counting of events that fires both muon trigger and electron trigger 

  for (const pat::Muon& muon : *muons) {
    reco::TrackRef mtk = muon.track();
    if (mtk.isNull()) continue;
 
    if (muon.pt() > min_muon_pt && abs(muon.eta()) < 2.4) {
      bool isMedMuon = muon.passed(reco::Muon::CutBasedIdMedium);
      const float iso = (muon.pfIsolationR04().sumChargedHadronPt + std::max(0., muon.pfIsolationR04().sumNeutralHadronEt + muon.pfIsolationR04().sumPhotonEt -0.5*muon.pfIsolationR04().sumPUPt))/muon.pt();
      if (isMedMuon && iso < 0.15) {
  	    ++nmuons;
      } 
    } 
    leptons_pass = nmuons + nelectrons >= min_nleptons;
    if (leptons_pass) {
      muons_pass = true;
      break;
    }
  } 

  if (debug) printf("MFVEventFilter: nmuons: %i nelectrons: %i pass? %i\n", nmuons, nelectrons, leptons_pass);
   
  for (const pat::Electron& electron : *electrons) {
    reco::GsfTrackRef etk = electron.gsfTrack();
    if (etk.isNull()) continue;

    if (electron.pt() > min_electron_pt && abs(electron.eta()) < 2.4) {
      bool isTightEl = electron.electronID("cutBasedElectronID-Fall17-94X-V1-tight");
      //const auto pfIso = electron.pfIsolationVariables();
      //const float eA = electron_effective_areas.getEffectiveArea(fabs(electron.superCluster()->eta()));
      //const float iso = (pfIso.sumChargedHadronPt + std::max(0., pfIso.sumNeutralHadronEt + pfIso.sumPhotonEt - *rho*eA)) / electron.pt();
      const bool passveto = electron.passConversionVeto();

      if (isTightEl && passveto) {
  	    ++nelectrons;
      } 
    } 
    leptons_pass = nmuons + nelectrons >= min_nleptons;
    if (leptons_pass) {
      break;
    }
  } 

  if (debug) printf("MFVEventFilter: nmuons: %i nelectrons: %i pass? %i electron veto mu pass? %i \n", nmuons, nelectrons, leptons_pass, (leptons_pass && !(muons_pass)));

  
  if (mode == Mode::jets_only)
    return jets_pass;
  else if (mode == Mode::either && jets_pass)
    return true;
  else if (mode == Mode::HT_OR_bjets_OR_displaced_dijet || mode == Mode::bjets_OR_displaced_dijet_veto_HT)
    return true;
  else if (mode == Mode::bjets_OR_displaced_dijet_veto_leptons_and_HT)
    return true;
  else if (mode == Mode::MET_only)
    return true;
  //these two else if's must be in this order 
  else if (mode == Mode::muons_only || mode == Mode::leptons_only)  //avoid double counting an event that fires both lepton triggers and keep it in muon selection 
    return leptons_pass && jets_pass;
  else if (mode == Mode::electrons_only_veto_muons || mode == Mode::leptons_only) 
    return leptons_pass && jets_pass && !(muons_pass);
  else return true; // catch-all
} 
DEFINE_FWK_MODULE(MFVEventFilter);
