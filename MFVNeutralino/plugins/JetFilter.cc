#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/MakerMacros.h"

class MFVJetFilter : public edm::EDFilter {
public:
  explicit MFVJetFilter(const edm::ParameterSet&);
private:
  bool filter(edm::Event&, const edm::EventSetup&) override;

  const edm::EDGetTokenT<pat::JetCollection> jets_token;

  const int min_njets;
  const double min_pt_for_ht;
  const double max_pt_for_ht;
  const double min_ht;
  const bool debug;
};

MFVJetFilter::MFVJetFilter(const edm::ParameterSet& cfg)
  : jets_token(consumes<pat::JetCollection>(cfg.getParameter<edm::InputTag>("jets_src"))),
    min_njets(cfg.getParameter<int>("min_njets")),
    min_pt_for_ht(cfg.getParameter<double>("min_pt_for_ht")),
    max_pt_for_ht(cfg.getParameter<double>("max_pt_for_ht")),
    min_ht(cfg.getParameter<double>("min_ht")),
    debug(cfg.getUntrackedParameter<bool>("debug", false))
{
}

bool MFVJetFilter::filter(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<pat::JetCollection> jets;
  event.getByToken(jets_token, jets);

  double ht = 0;
  for (const pat::Jet& jet : *jets) {
    const double pt = jet.pt();
    if (pt > min_pt_for_ht && pt < max_pt_for_ht)
      ht += pt;
  }

  if (debug) printf("JetFilter: njets: %lu  ht: %f\n", jets->size(), ht);

  return
    int(jets->size()) >= min_njets && 
    ht >= min_ht;
}

DEFINE_FWK_MODULE(MFVJetFilter);
