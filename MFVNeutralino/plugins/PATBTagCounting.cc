#include "TH1F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

class MFVNeutralinoPATBTagCounting : public edm::EDAnalyzer {
 public:
  explicit MFVNeutralinoPATBTagCounting(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::InputTag jet_src;
  const std::string b_discriminator_name;
  const double jet_pt_min;
  const double bdisc_min;
  const bool verbose;
  
  TH1F* h_ndisc;
};

MFVNeutralinoPATBTagCounting::MFVNeutralinoPATBTagCounting(const edm::ParameterSet& cfg)
  : jet_src(cfg.getParameter<edm::InputTag>("jet_src")),
    b_discriminator_name(cfg.getParameter<std::string>("b_discriminator_name")),
    jet_pt_min(cfg.getParameter<double>("jet_pt_min")),
    bdisc_min(cfg.getParameter<double>("bdisc_min")),
    verbose(cfg.getParameter<bool>("verbose"))
{
  edm::Service<TFileService> fs;
  h_ndisc = fs->make<TH1F>("h_ndisc", "", 30, 0, 30);
}

void MFVNeutralinoPATBTagCounting::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<pat::JetCollection> jets;
  event.getByLabel(jet_src, jets);

  int ndisc = 0;

  if (verbose) std::cout << "MFVNeutralinoPATBTagCounting: b_discriminator_name: " << b_discriminator_name << " jet_pt_min: " << jet_pt_min << " bdisc_min: " << bdisc_min << "\n";
  for (int i = 0, ie = jets->size(); i < ie; ++i) {
    const pat::Jet& jet = jets->at(i);
    //const reco::GenJet* gen_jet = jet.genJet();

    const double bdisc = jet.bDiscriminator(b_discriminator_name);
    if (verbose) std::cout << "#" << i << ": pt eta phi: " << jet.pt() << ", "<< jet.eta() << ", "<< jet.phi() << " bdisc: " << bdisc << "\n";
    if (jet.pt() > jet_pt_min && bdisc > bdisc_min)
      ++ndisc;
  }

  h_ndisc->Fill(ndisc);
}

DEFINE_FWK_MODULE(MFVNeutralinoPATBTagCounting);
