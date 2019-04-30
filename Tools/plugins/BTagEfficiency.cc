#include "TH2.h"
#include "TH3.h"
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
  const edm::EDGetTokenT<double> weight_token;
  const edm::EDGetTokenT<pat::JetCollection> jets_token;
  const double jet_pt_min;
  const std::string b_discriminator;
  const std::vector<double> b_discriminator_min;

  enum { light, charm, bottom, nkinds };
  TH3D* h_nlcb;
  TH2D* h_den[nkinds];
  std::vector<TH2D*> h_num[nkinds];
  std::vector<TH1F*> h_scalefactor[nkinds];
};

JMTBTagEfficiency::JMTBTagEfficiency(const edm::ParameterSet& cfg)
  : weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
    jets_token(consumes<pat::JetCollection>(cfg.getParameter<edm::InputTag>("jets_src"))),
    jet_pt_min(cfg.getParameter<double>("jet_pt_min")),
    b_discriminator(cfg.getParameter<std::string>("b_discriminator")),
    b_discriminator_min(cfg.getParameter<std::vector<double>>("b_discriminator_min"))
{
  edm::Service<TFileService> fs;
  TH1::SetDefaultSumw2();

  const int nptbins = 9;
  const double ptbins[nptbins+1] = { 20, 30, 50, 70, 100, 140, 200, 300, 600, 1000 };
  const char* kind[nkinds] = {"light", "charm", "bottom"};
  const size_t nmins = b_discriminator_min.size();
  for (int i = 0; i < nkinds; ++i) {
    h_den[i] = fs->make<TH2D>(TString::Format("den_%s", kind[i]), ";#eta;p_{T} (GeV)", 10, -2.5, 2.5, nptbins, ptbins);
    h_num[i].resize(nmins);
    h_scalefactor[i].resize(nmins);
    for (size_t j = 0; j < nmins; ++j) {
      h_num[i][j] = fs->make<TH2D>(TString::Format("num_%s_%lu", kind[i], j), TString::Format("bdisc min = %f;#eta;p_{T} (GeV)", b_discriminator_min[j]), 10, -2.5, 2.5, nptbins, ptbins);
      h_scalefactor[i][j] = fs->make<TH1F>(TString::Format("scalefactor_%s_%lu", kind[i], j), TString::Format("bdisc min = %f;2017 data-to-simulation scale factor for CSVv2 btag %s jet identification efficiency;Number of %s jets", b_discriminator_min[j], kind[i], kind[i]), 50, 0.75, 1.25);
    }
  }

  h_nlcb = fs->make<TH3D>("h_nlcb", "n_{l};n_{c};n_{b}", 40, 0, 40, 40, 0, 40, 40, 0, 40);
}

void JMTBTagEfficiency::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<double> w;
  event.getByToken(weight_token, w);

  edm::Handle<pat::JetCollection> jets;
  event.getByToken(jets_token, jets);

  int nlcb[3] = {0};

  for (const pat::Jet& jet : *jets) {
    if (jet.pt() < jet_pt_min)
      continue;

    int kind = jet.hadronFlavour();
    if      (kind == 4) kind = 1;
    else if (kind == 5) kind = 2;
    else assert(kind == 0);

    ++nlcb[kind];

    h_den[kind]->Fill(jet.eta(), jet.pt(), *w);

    for (size_t i = 0, ie = b_discriminator_min.size(); i < ie; ++i)
      if (jet.bDiscriminator(b_discriminator) > b_discriminator_min[i])
        h_num[kind][i]->Fill(jet.eta(), jet.pt(), *w);

    double x = jet.pt(); //scale factors from https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation
    assert(x >= 20); if (x > 1000) x = 1000;
    if (kind == 2) {
      h_scalefactor[kind][0]->Fill(0.986369+(-(4.21155e-05*(log(x+19)*(log(x+18)*(3-(-(6.02128*log(x+18)))))))), *w);
      h_scalefactor[kind][1]->Fill(1.09079*((1.+(0.180764*x))/(1.+(0.216797*x))), *w);
      h_scalefactor[kind][2]->Fill(0.91423*((1.+(0.00958053*x))/(1.+(0.010132*x))), *w);
    } else if (kind == 1) {
      h_scalefactor[kind][0]->Fill(0.986369+(-(4.21155e-05*(log(x+19)*(log(x+18)*(3-(-(6.02128*log(x+18)))))))), *w);
      h_scalefactor[kind][1]->Fill(1.09079*((1.+(0.180764*x))/(1.+(0.216797*x))), *w);
      h_scalefactor[kind][2]->Fill(0.91423*((1.+(0.00958053*x))/(1.+(0.010132*x))), *w);
    } else {
      h_scalefactor[kind][0]->Fill(0.948763+0.000459508*x+-2.36079e-07*x*x+4.13462/x, *w);
      h_scalefactor[kind][1]->Fill(0.949449+0.000516201*x+7.13398e-08*x*x+-3.55644e-10*x*x*x, *w);
      h_scalefactor[kind][2]->Fill(0.943355+8.95816/(x*x)+0.000240703*x, *w);
    }
  }

  h_nlcb->Fill(nlcb[0], nlcb[1], nlcb[2], *w);
}

DEFINE_FWK_MODULE(JMTBTagEfficiency);
