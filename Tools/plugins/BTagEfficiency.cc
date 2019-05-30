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

  enum { b_2017old, b_2017, b_2018, nbdisc };
  enum { nwp = 3 };
  const std::string b_discriminator_s;
  const int b_discriminator;
  static const double b_discriminator_min[nbdisc][nwp];

  enum { light, charm, bottom, nkinds };
  TH3D* h_nlcb;
  TH2D* h_den[nkinds];
  std::vector<TH2D*> h_num[nkinds];
  std::vector<TH1D*> h_scalefactor[nkinds];
};

const double JMTBTagEfficiency::b_discriminator_min[JMTBTagEfficiency::nbdisc][JMTBTagEfficiency::nwp] = {
  {0.5803, 0.8838, 0.9693},
  {0.0521, 0.3033, 0.7489},
  {0.0494, 0.2770, 0.7264}
};

JMTBTagEfficiency::JMTBTagEfficiency(const edm::ParameterSet& cfg)
  : weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
    jets_token(consumes<pat::JetCollection>(cfg.getParameter<edm::InputTag>("jets_src"))),
    jet_pt_min(cfg.getParameter<double>("jet_pt_min")),
    b_discriminator_s(cfg.getParameter<std::string>("b_discriminator")),
    b_discriminator(b_discriminator_s == "2017old" ? b_2017old :
                    b_discriminator_s == "2017"    ? b_2017 :
                    b_discriminator_s == "2018"    ? b_2018 :
                    -1)
{
  if (b_discriminator == -1)
    throw cms::Exception("Misconfiguration", "bad b_discriminator value") << b_discriminator;

  edm::Service<TFileService> fs;
  TH1::SetDefaultSumw2();

  const int nptbins = 9;
  const double ptbins[nptbins+1] = { 20, 30, 50, 70, 100, 140, 200, 300, 600, 1000 };
  const char* kind[nkinds] = {"light", "charm", "bottom"};
  for (int i = 0; i < nkinds; ++i) {
    h_den[i] = fs->make<TH2D>(TString::Format("den_%s", kind[i]), ";#eta;p_{T} (GeV)", 10, -2.5, 2.5, nptbins, ptbins);
    h_num[i].resize(nwp);
    h_scalefactor[i].resize(nwp);
    for (size_t j = 0; j < nwp; ++j) {
      h_num[i][j] = fs->make<TH2D>(TString::Format("num_%s_%lu", kind[i], j), TString::Format("bdisc min = %f;#eta;p_{T} (GeV)", b_discriminator_min[b_discriminator][j]), 10, -2.5, 2.5, nptbins, ptbins);
      h_scalefactor[i][j] = fs->make<TH1D>(TString::Format("scalefactor_%s_%lu", kind[i], j), TString::Format("bdisc min = %f;2017 data-to-simulation scale factor for btag %s jet identification efficiency;number of %s jets", b_discriminator_min[b_discriminator][j], kind[i], kind[i]), 100, 0., 2.);
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

    for (size_t i = 0; i < nwp; ++i) {
      const double bd = b_discriminator == b_2017old ?
        jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags") :
        jet.bDiscriminator("pfDeepFlavourJetTags:probb") + jet.bDiscriminator("pfDeepFlavourJetTags:probbb") + jet.bDiscriminator("pfDeepFlavourJetTags:problepb");
      if (bd > b_discriminator_min[b_discriminator][i])
        h_num[kind][i]->Fill(jet.eta(), jet.pt(), *w);
    }

    // central value scale factors from https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation
    double x = jet.pt(); 
    assert(x >= 20); if (x > 1000) x = 1000;
    if (b_discriminator == b_2017old) { // https://twiki.cern.ch/twiki/pub/CMS/BtagRecommendation94X/CSVv2_94XSF_WP_V2_B_F.csv
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
    else if (b_discriminator == b_2017) { // https://twiki.cern.ch/twiki/pub/CMS/BtagRecommendation94X/DeepFlavour_94XSF_WP_V2_B_F.csv
      if (kind == 2) {
        h_scalefactor[kind][0]->Fill(1.04891*((1.+(0.0145976*x))/(1.+(0.0165274*x))), *w);
        h_scalefactor[kind][1]->Fill(0.991757*((1.+(0.0209615*x))/(1.+(0.0234962*x))), *w);
        h_scalefactor[kind][2]->Fill(0.908648*((1.+(0.00516407*x))/(1.+(0.00564675*x))), *w);
      } else if (kind == 1) {
        h_scalefactor[kind][0]->Fill(1.04891*((1.+(0.0145976*x))/(1.+(0.0165274*x))), *w);
        h_scalefactor[kind][1]->Fill(0.991757*((1.+(0.0209615*x))/(1.+(0.0234962*x))), *w);
        h_scalefactor[kind][2]->Fill(0.908648*((1.+(0.00516407*x))/(1.+(0.00564675*x))), *w);
      } else {
        h_scalefactor[kind][0]->Fill(1.43763+-0.000337048*x+2.22072e-07*x*x+-4.85489/x, *w);
        h_scalefactor[kind][1]->Fill(1.40779+-0.00094558*x+8.74982e-07*x*x+-4.67814/x, *w);
        h_scalefactor[kind][2]->Fill(0.952956+0.000569069*x+-1.88872e-06*x*x+1.25729e-09*x*x*x, *w);
      }
    }
    else if (b_discriminator == b_2018) { // https://twiki.cern.ch/twiki/pub/CMS/BtagRecommendation102X/DeepJet_102XSF_WP_V1.csv
      if (kind == 2) {
        h_scalefactor[kind][0]->Fill(0.873139+(0.00420739*(log(x+19)*(log(x+18)*(3-(0.380932*log(x+18)))))), *w);
        h_scalefactor[kind][1]->Fill(1.0097+(-(2.89663e-06*(log(x+19)*(log(x+18)*(3-(-(110.381*log(x+18)))))))), *w);
        h_scalefactor[kind][2]->Fill(0.818896+(0.00682971*(log(x+19)*(log(x+18)*(3-(0.440998*log(x+18)))))), *w);
      } else if (kind == 1) {
        h_scalefactor[kind][0]->Fill(0.873139+(0.00420739*(log(x+19)*(log(x+18)*(3-(0.380932*log(x+18)))))), *w);
        h_scalefactor[kind][1]->Fill(1.0097+(-(2.89663e-06*(log(x+19)*(log(x+18)*(3-(-(110.381*log(x+18)))))))), *w);
        h_scalefactor[kind][2]->Fill(0.818896+(0.00682971*(log(x+19)*(log(x+18)*(3-(0.440998*log(x+18)))))), *w);
      } else {
        h_scalefactor[kind][0]->Fill(1.61341+-0.000566321*x+1.99464e-07*x*x+-5.09199/x, *w);
        h_scalefactor[kind][1]->Fill(1.59373+-0.00113028*x+8.66631e-07*x*x+-1.10505/x, *w);
        h_scalefactor[kind][2]->Fill(1.77088+-0.00371551*x+5.86489e-06*x*x+-3.01178e-09*x*x*x, *w);
      }
    }
  }

  h_nlcb->Fill(nlcb[0], nlcb[1], nlcb[2], *w);
}

DEFINE_FWK_MODULE(JMTBTagEfficiency);
