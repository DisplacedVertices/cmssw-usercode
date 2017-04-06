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
  const double min_ht;
  const bool debug;
};

MFVJetFilter::MFVJetFilter(const edm::ParameterSet& cfg)
  : jets_token(consumes<pat::JetCollection>(cfg.getParameter<edm::InputTag>("jets_src"))),
    min_njets(cfg.getParameter<int>("min_njets")),
    min_ht(cfg.getParameter<double>("min_ht")),
    debug(cfg.getUntrackedParameter<bool>("debug", false))
{
}

bool MFVJetFilter::filter(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<pat::JetCollection> jets;
  event.getByToken(jets_token, jets);

  double ht_20 = 0;
  double ht_40 = 0;
  double ht_gt30lt200 = 0;
  for (const pat::Jet& jet : *jets) {
    const double pt = jet.pt();
    ht_20 += pt;
    if (pt > 40)
      ht_40 += pt;
    if (pt > 30 && pt < 200)
      ht_gt30lt200 += pt;
  }

  if (debug) printf("JetFilter: njets: %lu gt20: %f  gt40: %f  gt30lt200: %f\n", jets->size(), ht_20, ht_40, ht_gt30lt200);

  return
    int(jets->size()) >= min_njets && 
    ht_40 >= min_ht;
}

DEFINE_FWK_MODULE(MFVJetFilter);
