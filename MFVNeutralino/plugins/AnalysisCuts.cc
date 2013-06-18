#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"

class MFVAnalysisCuts : public edm::EDFilter {
public:
  explicit MFVAnalysisCuts(const edm::ParameterSet&);

private:
  virtual bool filter(edm::Event&, const edm::EventSetup&);

  const edm::InputTag jet_src;
  const double min_jet_pt;
  const double min_4th_jet_pt;
  const double min_5th_jet_pt;
  const double min_6th_jet_pt;
  const double min_njets;
  const double min_nbtags;
  const double min_sum_ht;

  const std::string b_discriminator_name;
  const double bdisc_min;
  const edm::InputTag muon_src;
  const edm::InputTag electron_src;
};

MFVAnalysisCuts::MFVAnalysisCuts(const edm::ParameterSet& cfg) 
  : jet_src(cfg.getParameter<edm::InputTag>("jet_src")),
    min_jet_pt(cfg.getParameter<double>("min_jet_pt")),
    min_4th_jet_pt(cfg.getParameter<double>("min_4th_jet_pt")),
    min_5th_jet_pt(cfg.getParameter<double>("min_5th_jet_pt")),
    min_6th_jet_pt(cfg.getParameter<double>("min_6th_jet_pt")),
    min_njets(cfg.getParameter<double>("min_njets")),
    min_nbtags(cfg.getParameter<double>("min_nbtags")),
    min_sum_ht(cfg.getParameter<double>("min_sum_ht")),

    b_discriminator_name(cfg.getParameter<std::string>("b_discriminator_name")),
    bdisc_min(cfg.getParameter<double>("bdisc_min")),
    muon_src(cfg.getParameter<edm::InputTag>("muon_src")),
    electron_src(cfg.getParameter<edm::InputTag>("electron_src"))
{
}

bool MFVAnalysisCuts::filter(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<pat::JetCollection> jets;
  event.getByLabel(jet_src, jets);

  int njets = 0;
  int nbtags = 0;
  
  double sum_ht = 0;
  for (int i = 0, ie = jets->size(); i < ie; ++i) {
    const pat::Jet& jet = jets->at(i);
    const double bdisc = jet.bDiscriminator(b_discriminator_name);

    if (jet.pt() > min_jet_pt) {
      sum_ht += jet.pt();
      ++njets;
      if (bdisc > bdisc_min)
        ++nbtags;
    }

    if (i+1==4 && jet.pt() < min_4th_jet_pt) return false; //cut on the pt of the 4th jet
    if (i+1==5 && jet.pt() < min_5th_jet_pt) return false; //cut on the pt of the 5th jet
    if (i+1==6 && jet.pt() < min_6th_jet_pt) return false; //cut on the pt of the 6th jet
  }

  if (njets < min_njets) return false; //cut on the number of jets
  if (nbtags < min_nbtags) return false; //cut on the number of btags
  if (sum_ht < min_sum_ht) return false; //cut on the sum of the pt's of all the jets

  return true;
}

DEFINE_FWK_MODULE(MFVAnalysisCuts);

