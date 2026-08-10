#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

class JMTJetFilter : public edm::EDFilter {
public:
  explicit JMTJetFilter(const edm::ParameterSet&);
private:
  bool filter(edm::Event&, const edm::EventSetup&) override;

  const edm::EDGetTokenT<pat::JetCollection> jets_token;

  const int min_njets;
  const double min_pt_for_ht;
  const double max_pt_for_ht;
  const double min_ht;
  const bool debug;
  const std::string module_label;
};

JMTJetFilter::JMTJetFilter(const edm::ParameterSet& cfg)
  : jets_token(consumes<pat::JetCollection>(cfg.getParameter<edm::InputTag>("jets_src"))),
    min_njets(cfg.getParameter<int>("min_njets")),
    min_pt_for_ht(cfg.getParameter<double>("min_pt_for_ht")),
    max_pt_for_ht(cfg.getParameter<double>("max_pt_for_ht")),
    min_ht(cfg.getParameter<double>("min_ht")),
    debug(cfg.getUntrackedParameter<bool>("debug", false)),
    module_label(cfg.getParameter<std::string>("@module_label"))
{
}

bool JMTJetFilter::filter(edm::Event& event, const edm::EventSetup&) {
  if (debug) std::cout << "JMTJetFilter=" << module_label << " event " << event.id().run() << "," << event.luminosityBlock() << "," << event.id().event() << "\n";

  edm::Handle<pat::JetCollection> jets;
  event.getByToken(jets_token, jets);

  double ht = 0;
  int ijet = 0;
  for (const pat::Jet& jet : *jets) {
    if (debug) std::cout << "jet #" << ijet++ << ": pt " << jet.pt() << " eta " << jet.eta() << " phi " << jet.phi() << " E " << jet.energy() << " nconst " << jet.nConstituents() << "\n";
    const double pt = jet.pt();
    if (pt > min_pt_for_ht && pt < max_pt_for_ht)
      ht += pt;
  }

  if (debug) std::cout << "JMTJetFilter=" << module_label << " njets: " << jets->size() << " ht: " << ht << "\n";

  return
    int(jets->size()) >= min_njets && 
    ht >= min_ht;
}

DEFINE_FWK_MODULE(JMTJetFilter);
