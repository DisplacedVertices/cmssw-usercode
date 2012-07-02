#include "TH1F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/BTauReco/interface/JetTag.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/JetReco/interface/CaloJet.h"
#include "DataFormats/JetReco/interface/CaloJetCollection.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

class MFVNeutralinoBTagCounting : public edm::EDAnalyzer {
 public:
  explicit MFVNeutralinoBTagCounting(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::InputTag btag_src;
  const double jet_pt_min;
  const double bdisc_min;
  
  TH1F* h_ndisc;
};

MFVNeutralinoBTagCounting::MFVNeutralinoBTagCounting(const edm::ParameterSet& cfg)
  : btag_src(cfg.getParameter<edm::InputTag>("btag_src")),
    jet_pt_min(cfg.getParameter<double>("jet_pt_min")),
    bdisc_min(cfg.getParameter<double>("bdisc_min"))
{
  edm::Service<TFileService> fs;
  h_ndisc = fs->make<TH1F>("h_ndisc", "", 30, 0, 30);
}

void MFVNeutralinoBTagCounting::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  //edm::Handle<reco::CaloJetCollection> jets;
  //event.getByLabel("ak5CaloJets", jets);
  //printf("njets: %i\n", int(jets->size()));
  //for (int i = 0, ie = int(jets->size()); i < ie; ++i)
  //  printf("jet #%i: pt eta phi %f %f %f\n", i, jets->at(i).pt(), jets->at(i).eta(), jets->at(i).phi());
    
  edm::Handle<reco::JetTagCollection> btags;
  event.getByLabel(btag_src, btags);

  int ndisc = 0;

  //std::cout << btag_src << "\n";
  for (int i = 0, ie = btags->size(); i < ie; ++i) {
    //std::cout << "#" << i << ": pt eta phi: " << (*btags)[i].first->pt() << ", "<< (*btags)[i].first->eta() << ", "<< (*btags)[i].first->phi() << " bdisc: " << (*btags)[i].second << "\n";
    if ((*btags)[i].first->pt() > jet_pt_min && (*btags)[i].second > bdisc_min)
      ++ndisc;
  }

  h_ndisc->Fill(ndisc);
}

DEFINE_FWK_MODULE(MFVNeutralinoBTagCounting);
