#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "JMTucker/Tools/interface/TriggerHelper.h"

class MFVEventFilter : public edm::EDFilter {
    public:
        explicit MFVEventFilter(const edm::ParameterSet&);
    private:
        bool filter(edm::Event&, const edm::EventSetup&) override;
        bool trigger_veto(edm::Event& event, const std::vector<std::string> trigger_list);

        struct Mode {
            enum mode_t { either, jets_only, leptons_only, dilepton_only, HT_OR_bjets_OR_displaced_dijet, bjets_OR_displaced_dijet, displaced_dijet_veto_bjets, bjets_OR_displaced_dijet_veto_HT };
            const mode_t mode;
            Mode(const std::string& m) : mode(m == "low HT" ? jets_only : m == "bjets_OR_displaced_dijet_veto_HT" ? bjets_OR_displaced_dijet_veto_HT : m == "bjets OR displaced dijet" ? bjets_OR_displaced_dijet : m == "displaced dijet veto bjets" ? displaced_dijet_veto_bjets : m == "HT OR bjets OR displaced dijet" ? HT_OR_bjets_OR_displaced_dijet : m == "dilepton_only" ? dilepton_only : m == "leptons only" ? leptons_only : m == "jets only" ? jets_only : either) {}
            bool operator==(mode_t m) const { return mode == m; }
        };
        const Mode mode;


        const edm::EDGetTokenT<pat::JetCollection> jets_token;
        const edm::EDGetTokenT<edm::TriggerResults> trigger_results_token;
        const StringCutObjectSelector<pat::Jet> jet_selector;
        const int min_njets;
        const double min_pt_for_ht;
        const double min_ht;
        const edm::EDGetTokenT<pat::MuonCollection> muons_token;
        const StringCutObjectSelector<pat::Muon> muon_selector;
        const double min_muon_pt;
        const edm::EDGetTokenT<pat::ElectronCollection> electrons_token;
        const StringCutObjectSelector<pat::Electron> electron_selector;
        const double min_electron_pt;
        const int min_nleptons;
        const bool veto_bjet_triggers;
        const std::vector<std::string> triggers_to_veto;
        const bool debug;
};

MFVEventFilter::MFVEventFilter(const edm::ParameterSet& cfg)
    : mode(cfg.getParameter<std::string>("mode")),
    jets_token(consumes<pat::JetCollection>(cfg.getParameter<edm::InputTag>("jets_src"))),
    trigger_results_token(consumes<edm::TriggerResults>(cfg.getParameter<edm::InputTag>("trigger_results_src"))),
    jet_selector(cfg.getParameter<std::string>("jet_cut")),
    min_njets(cfg.getParameter<int>("min_njets")),
    min_pt_for_ht(cfg.getParameter<double>("min_pt_for_ht")),
    min_ht(cfg.getParameter<double>("min_ht")),
    muons_token(consumes<pat::MuonCollection>(cfg.getParameter<edm::InputTag>("muons_src"))),
    muon_selector(cfg.getParameter<std::string>("muon_cut")),
    min_muon_pt(cfg.getParameter<double>("min_muon_pt")),
    electrons_token(consumes<pat::ElectronCollection>(cfg.getParameter<edm::InputTag>("electrons_src"))),
    electron_selector(cfg.getParameter<std::string>("electron_cut")),
    min_electron_pt(cfg.getParameter<double>("min_electron_pt")),
    min_nleptons(cfg.getParameter<int>("min_nleptons")),
    veto_bjet_triggers(cfg.getParameter<bool>("veto_bjet_triggers")),
    triggers_to_veto(cfg.getParameter<std::vector<std::string>>("triggers_to_veto")),
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

    if (veto_bjet_triggers) {
        for (auto trigger_to_veto : triggers_to_veto) {
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

    if (debug) printf("MFVEventFilter: njets: %i  ht: %f pass? %i\n", njets, ht, jets_pass);

    if (mode == Mode::jets_only) {
        return jets_pass;
    }
    else if (mode == Mode::either && jets_pass)
        return true;
    else if (mode == Mode::HT_OR_bjets_OR_displaced_dijet || mode == Mode::bjets_OR_displaced_dijet_veto_HT || mode == Mode::bjets_OR_displaced_dijet || mode == Mode::displaced_dijet_veto_bjets)
        return true;


    edm::Handle<pat::MuonCollection> muons;
    edm::Handle<pat::ElectronCollection> electrons;
    event.getByToken(muons_token, muons);
    event.getByToken(electrons_token, electrons);

    int nmuons = 0, nelectrons = 0;

    for (const pat::Muon& muon : *muons)
        if (muon_selector(muon) && muon.pt() > min_muon_pt)
            ++nmuons;

    for (const pat::Electron& electron : *electrons)
        if (electron_selector(electron) && electron.pt() > min_electron_pt)
            ++nelectrons;

    const bool leptons_pass = (nmuons + nelectrons >= min_nleptons);

    if (debug) printf("MFVEventFilter: nmuons: %i nelectrons: %i pass? %i\n", nmuons, nelectrons, leptons_pass);

    return leptons_pass;
}

DEFINE_FWK_MODULE(MFVEventFilter);
