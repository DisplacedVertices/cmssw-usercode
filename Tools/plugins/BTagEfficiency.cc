#include "TH2.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"

class JMTBTagEfficiency : public edm::EDAnalyzer {
public:
  explicit JMTBTagEfficiency(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&) override;

private:
  const edm::EDGetTokenT<std::vector<PileupSummaryInfo> > pileup_summary_token;
  const std::vector<double> pileup_weights;
  const edm::EDGetTokenT<pat::JetCollection> jets_token;
  const double jet_pt_min;
  const double jet_ht_min;
  const int njets_min;
  const std::string b_discriminator;
  const std::vector<double> b_discriminator_min;

  enum { light, charm, bottom, nkinds };
  TH2D* h_den[nkinds];
  std::vector<TH2D*> h_num[nkinds];
};

JMTBTagEfficiency::JMTBTagEfficiency(const edm::ParameterSet& cfg)
  : pileup_summary_token(consumes<std::vector<PileupSummaryInfo> >(cfg.getParameter<edm::InputTag>("pileup_info_src"))),
    pileup_weights(cfg.getParameter<std::vector<double>>("pileup_weights")),
    jets_token(consumes<pat::JetCollection>(cfg.getParameter<edm::InputTag>("jets_src"))),
    jet_pt_min(cfg.getParameter<double>("jet_pt_min")),
    jet_ht_min(cfg.getParameter<double>("jet_ht_min")),
    njets_min(cfg.getParameter<int>("njets_min")),
    b_discriminator(cfg.getParameter<std::string>("b_discriminator")),
    b_discriminator_min(cfg.getParameter<std::vector<double>>("b_discriminator_min"))
{
  edm::Service<TFileService> fs;
  TH1::SetDefaultSumw2();

  const int nptbins = 11;
  const double ptbins[nptbins+1] = { 20, 30, 40, 50, 75, 100, 150, 200, 350, 500, 750, 1000 };
  const char* kind[nkinds] = {"light", "charm", "bottom"};
  const size_t nmins = b_discriminator_min.size();
  for (int i = 0; i < nkinds; ++i) {
    h_den[i] = fs->make<TH2D>(TString::Format("den_%s", kind[i]), ";#eta;p_{T} (GeV)", 10, -2.5, 2.5, nptbins, ptbins);
    h_num[i].resize(nmins);
    for (size_t j = 0; j < nmins; ++j)
      h_num[i][j] = fs->make<TH2D>(TString::Format("num_%s_%lu", kind[i], j), TString::Format("bdisc min = %f;#eta;p_{T} (GeV)", b_discriminator_min[j]), 10, -2.5, 2.5, nptbins, ptbins);
  }
}

void JMTBTagEfficiency::analyze(const edm::Event& event, const edm::EventSetup&) {
  double w = 1; 

  int npu = -1;
  edm::Handle<std::vector<PileupSummaryInfo> > pileup;
  event.getByToken(pileup_summary_token, pileup);

  for (std::vector<PileupSummaryInfo>::const_iterator psi = pileup->begin(), end = pileup->end(); psi != end; ++psi)
    if (psi->getBunchCrossing() == 0)
      npu = psi->getTrueNumInteractions();

  if (npu >= 0 && npu < int(pileup_weights.size()))
    w *= pileup_weights[npu];

  ////

  edm::Handle<pat::JetCollection> jets;
  event.getByToken(jets_token, jets);

  int njets = 0;
  double jet_ht = 0;
  for (const pat::Jet& jet : *jets) {
    if (jet.pt() < jet_pt_min) continue;
    ++njets;
    jet_ht += jet.pt();
  }

  if (njets < njets_min || jet_ht < jet_ht_min)
    return;

  for (const pat::Jet& jet : *jets) {
    if (jet.pt() < jet_pt_min) continue;

    int kind = jet.hadronFlavour();
    if      (kind == 4) kind = 1;
    else if (kind == 5) kind = 2;
    else assert(kind == 0);

    h_den[kind]->Fill(jet.eta(), jet.pt());

    for (size_t i = 0, ie = b_discriminator_min.size(); i < ie; ++i)
      if (jet.bDiscriminator(b_discriminator) > b_discriminator_min[i])
        h_num[kind][i]->Fill(jet.eta(), jet.pt());
  }
}

DEFINE_FWK_MODULE(JMTBTagEfficiency);
