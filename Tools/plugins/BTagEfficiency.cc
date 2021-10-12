#include "TH2.h"
#include "TH3.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "JMTucker/Tools/interface/BTagging.h"
#include "JMTucker/Tools/interface/Year.h"

class JMTBTagEfficiency : public edm::EDAnalyzer {
public:
  explicit JMTBTagEfficiency(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&) override;

private:
  const edm::EDGetTokenT<double> weight_token;
  const edm::EDGetTokenT<pat::JetCollection> jets_token;
  const double jet_pt_min;
  const bool old;

  enum { light, charm, bottom, nkinds };
  TH3D* h_nlcb;
  TH2D* h_den[nkinds];
  std::vector<TH2D*> h_num[nkinds];
  std::vector<TH1D*> h_scalefactor[nkinds];
};

JMTBTagEfficiency::JMTBTagEfficiency(const edm::ParameterSet& cfg)
  : weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
    jets_token(consumes<pat::JetCollection>(cfg.getParameter<edm::InputTag>("jets_src"))),
    jet_pt_min(cfg.getParameter<double>("jet_pt_min")),
    old(cfg.getParameter<bool>("old"))
{
  edm::Service<TFileService> fs;
  TH1::SetDefaultSumw2();

  const int nptbins = 9;
  const double ptbins[nptbins+1] = { 20, 30, 50, 70, 100, 140, 200, 300, 600, 1000 };
  const char* kind[nkinds] = {"light", "charm", "bottom"};
  for (int i = 0; i < nkinds; ++i) {
    h_den[i] = fs->make<TH2D>(TString::Format("den_%s", kind[i]), ";#eta;p_{T} (GeV)", 10, -2.5, 2.5, nptbins, ptbins);
    h_num[i].resize(jmt::BTagging::nwp);
    h_scalefactor[i].resize(jmt::BTagging::nwp);
    for (size_t j = 0; j < jmt::BTagging::nwp; ++j) {
      const float dmin = jmt::BTagging::discriminator_min(j, old);
      h_num[i][j] = fs->make<TH2D>(TString::Format("num_%s_%lu", kind[i], j), TString::Format("bdisc min = %f;#eta;p_{T} (GeV)", dmin), 10, -2.5, 2.5, nptbins, ptbins);
      h_scalefactor[i][j] = fs->make<TH1D>(TString::Format("scalefactor_%s_%lu", kind[i], j), TString::Format("bdisc min = %f;2017 data-to-simulation scale factor for btag %s jet identification efficiency;number of %s jets", dmin, kind[i], kind[i]), 100, 0., 2.);
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

    for (size_t i = 0; i < jmt::BTagging::nwp; ++i)
      if (jmt::BTagging::is_tagged(jet, i, old))
        h_num[kind][i]->Fill(jet.eta(), jet.pt(), *w);

    // central value scale factors from https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation
    // JMTBAD move to BTagging class?
    double x = jet.pt(); 
    assert(x >= 20); if (x > 1000) x = 1000;
#ifdef MFVNEUTRALINO_2017
    if (old) { // https://twiki.cern.ch/twiki/pub/CMS/BtagRecommendation106XUL17/DeepCSV_106XUL17SF_WPonly_V2p1.csv
      if (kind == 2) {
        h_scalefactor[kind][0]->Fill(0.947762+(0.000950836*(log(x+19)*(log(x+18)*(3-(0.26089*log(x+18)))))), *w);
        h_scalefactor[kind][1]->Fill(0.92801+(6.63609e-05*(log(x+19)*(log(x+18)*(3-(-(4.49722*log(x+18))))))), *w);
        h_scalefactor[kind][2]->Fill(0.698099+(0.00876337*(log(x+19)*(log(x+18)*(3-(0.371033*log(x+18)))))), *w);
      } else if (kind == 1) {
        h_scalefactor[kind][0]->Fill(0.947762+(0.000950836*(log(x+19)*(log(x+18)*(3-(0.26089*log(x+18)))))), *w);
        h_scalefactor[kind][1]->Fill(0.92801+(6.63609e-05*(log(x+19)*(log(x+18)*(3-(-(4.49722*log(x+18))))))), *w);
        h_scalefactor[kind][2]->Fill(0.698099+(0.00876337*(log(x+19)*(log(x+18)*(3-(0.371033*log(x+18)))))), *w);
      } else {
        h_scalefactor[kind][0]->Fill(1.02103+0.00020673*x+-1.37579e-07*x*x+5.45282/x, *w);
        h_scalefactor[kind][1]->Fill(1.09411+-0.000277731*x+2.47948e-07*x*x+-0.65943/x, *w);
        h_scalefactor[kind][2]->Fill(0.817821+1.44089/sqrt(x), *w);
      }
    }
    else { // https://twiki.cern.ch/twiki/pub/CMS/BtagRecommendation106XUL17/DeepJet_106XUL17SF_WPonly_V2p1.csv
      if (kind == 2) {
        h_scalefactor[kind][0]->Fill(0.932707+(0.00201163*(log(x+19)*(log(x+18)*(3-(0.36597*log(x+18)))))), *w);
        h_scalefactor[kind][1]->Fill(0.921599+(0.000862106*(log(x+19)*(log(x+18)*(3-(0.139754*log(x+18)))))), *w);
        h_scalefactor[kind][2]->Fill(0.868894+(0.00108176*(log(x+19)*(log(x+18)*(3-(-(0.00273954*log(x+18))))))), *w);
      } else if (kind == 1) {
        h_scalefactor[kind][0]->Fill(0.932707+(0.00201163*(log(x+19)*(log(x+18)*(3-(0.36597*log(x+18)))))), *w);
        h_scalefactor[kind][1]->Fill(0.921599+(0.000862106*(log(x+19)*(log(x+18)*(3-(0.139754*log(x+18)))))), *w);
        h_scalefactor[kind][2]->Fill(0.868894+(0.00108176*(log(x+19)*(log(x+18)*(3-(-(0.00273954*log(x+18))))))), *w);
      } else {
        h_scalefactor[kind][0]->Fill(1.34198+-0.000555031*x+3.20633e-07*x*x+0.888495/x, *w);
        h_scalefactor[kind][1]->Fill(1.35875+-0.000916722*x+6.33425e-07*x*x+-2.07301/x, *w);
        h_scalefactor[kind][2]->Fill(0.850069+1.99726/sqrt(x), *w);
      }
    }
#elif defined(MFVNEUTRALINO_2018)
    { // https://twiki.cern.ch/twiki/pub/CMS/BtagRecommendation106XUL18/DeepJet_106XUL18SF_WPonly_V1p1.csv
      if (kind == 2) {
        h_scalefactor[kind][0]->Fill(0.882297+0.00426142*log(x+19)*log(x+18)*(3-0.411195*log(x+18)), *w);
        h_scalefactor[kind][1]->Fill(0.763354+0.0081767*log(x+19)*log(x+18)*(3-0.399925*log(x+18)), *w);
        h_scalefactor[kind][2]->Fill(0.716648+0.00833545*log(x+19)*log(x+18)*(3-0.370069*log(x+18)), *w);
      } else if (kind == 1) {
        h_scalefactor[kind][0]->Fill(0.882297+0.00426142*log(x+19)*log(x+18)*(3-0.411195*log(x+18)), *w);
        h_scalefactor[kind][1]->Fill(0.763354+0.0081767*log(x+19)*log(x+18)*(3-0.399925*log(x+18)), *w);
        h_scalefactor[kind][2]->Fill(0.716648+0.00833545*log(x+19)*log(x+18)*(3-0.370069*log(x+18)), *w);
      } else {
        h_scalefactor[kind][0]->Fill(1.46193+-0.000605595*x+3.30224e-07*x*x+-0.367873/x, *w);
        h_scalefactor[kind][1]->Fill(1.46818+-0.00104385*x+8.01998e-07*x*x+-2.02643/x, *w);
        h_scalefactor[kind][2]->Fill(0.864506+2.79354/sqrt(x), *w);
      }
    }
#else
#error bad year
#endif
  }

  h_nlcb->Fill(nlcb[0], nlcb[1], nlcb[2], *w);
}

DEFINE_FWK_MODULE(JMTBTagEfficiency);
