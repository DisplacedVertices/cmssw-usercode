#include "TH2.h"
#include "TRandom3.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"
#include "DVCode/MFVNeutralinoFormats/interface/Event.h"
#include "DVCode/Tools/interface/Year.h"

class MFVJetEnergyHistos : public edm::EDAnalyzer {
 public:
  explicit MFVJetEnergyHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::EDGetTokenT<MFVEvent> mevent_token;
  const edm::EDGetTokenT<double> weight_token;
  const bool jes;

  TH1D* h_w;

  TH1D* h_njets;
  TH1D* h_njets20;
  TH1D* h_jet_ht;
  TH1D* h_jet_ht_40;

  TH1D* h_jet_pt;
  TH1D* h_jet_eta;
  TH1D* h_jet_phi;
  TH1D* h_jet_energy;

  TH1D* h_njets_notmatched;
  TH1D* h_jet_pt_notmatched;

  TH1D* h_jet_pt_up;
  TH1D* h_jet_pt_down;
  TH1D* h_jet_ht_up;
  TH1D* h_jet_ht_down;
  TH1D* h_jet_ht_40_up;
  TH1D* h_jet_ht_40_down;
  TH1D* h_jet_ht_40_mup;
  TH1D* h_jet_ht_40_mdown;

  TH1D* h_jet_ht_40_1200cut;
  TH1D* h_jet_ht_40_up_1200cut;
  TH1D* h_jet_ht_40_down_1200cut;

  TH1D* h_scale_up;
  TH1D* h_scale_down;
};

MFVJetEnergyHistos::MFVJetEnergyHistos(const edm::ParameterSet& cfg)
  : mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
    jes(cfg.getParameter<bool>("jes")) // true jes, false jer
{
  edm::Service<TFileService> fs;

  h_w = fs->make<TH1D>("h_w", ";event weight;events/0.1", 100, 0, 10);

  h_njets = fs->make<TH1D>("h_njets", ";# of jets;events", 20, 0, 20);
  h_njets20 = fs->make<TH1D>("h_njets20", ";# of jets with p_{T} > 20 GeV;events", 20, 0, 20);
  h_jet_ht = fs->make<TH1D>("h_jet_ht", ";H_{T} of jets (GeV);events/25 GeV", 200, 0, 5000);
  h_jet_ht_40 = fs->make<TH1D>("h_jet_ht_40", ";H_{T} of jets with p_{T} > 40 GeV;events/25 GeV", 200, 0, 5000);

  h_jet_pt = fs->make<TH1D>("h_jet_pt", ";jets p_{T} (GeV);jets/10 GeV", 100, 0, 1000);
  h_jet_eta = fs->make<TH1D>("h_jet_eta", ";jets #eta (rad);jets/.08", 100, -4, 4);
  h_jet_phi = fs->make<TH1D>("h_jet_phi", ";jets #phi (rad);jets/.063", 100, -3.1416, 3.1416);
  h_jet_energy = fs->make<TH1D>("h_jet_energy", ";jets energy (GeV);jets/10 GeV", 100, 0, 1000);

  h_njets_notmatched = fs->make<TH1D>("h_njets_notmatched", ";# of jets without gen jet;events", 20, 0, 20);
  h_jet_pt_notmatched = fs->make<TH1D>("h_jet_pt_notmatched", ";jets without gen jet p_{T} (GeV);jets/10 GeV", 100, 0, 1000);

  h_jet_pt_up = fs->make<TH1D>("h_jet_pt_up", ";shifted up jets p_{T} (GeV);jets/10 GeV", 100, 0, 1000);
  h_jet_pt_down = fs->make<TH1D>("h_jet_pt_down", ";shifted down jets p_{T} (GeV);jets/10 GeV", 100, 0, 1000);
  h_jet_ht_up = fs->make<TH1D>("h_jet_ht_up", ";shifted up H_{T} of jets (GeV);events/25 GeV", 200, 0, 5000);
  h_jet_ht_down = fs->make<TH1D>("h_jet_ht_down", ";shifted down H_{T} of jets (GeV);events/25 GeV", 200, 0, 5000);
  h_jet_ht_40_up = fs->make<TH1D>("h_jet_ht_40_up", ";shifted up H_{T} of jets (GeV);events/25 GeV", 200, 0, 5000);
  h_jet_ht_40_down = fs->make<TH1D>("h_jet_ht_40_down", ";shifted down H_{T} of jets (GeV);events/25 GeV", 200, 0, 5000);
  h_jet_ht_40_mup = fs->make<TH1D>("h_jet_ht_40_mup", ";shifted up H_{T} of jets - nominal (GeV);events/25 GeV", 200, -500, 500);
  h_jet_ht_40_mdown = fs->make<TH1D>("h_jet_ht_40_mdown", ";shifted down H_{T} of jets - nominal (GeV);events/25 GeV", 200, -500, 500);

  h_jet_ht_40_1200cut = fs->make<TH1D>("h_jet_ht_40_1200cut", ";H_{T} of jets (GeV);events/25 GeV", 200, 0, 5000);
  h_jet_ht_40_up_1200cut = fs->make<TH1D>("h_jet_ht_40_up_1200cut", ";shifted up H_{T} of jets (GeV);events/25 GeV", 200, 0, 5000);
  h_jet_ht_40_down_1200cut = fs->make<TH1D>("h_jet_ht_40_down_1200cut", ";shifted down H_{T} of jets (GeV);events/25 GeV", 200, 0, 5000);

  h_scale_up = fs->make<TH1D>("h_scale_up", ";scale factor;jets/0.004", 50, 0.9, 1.1);
  h_scale_down = fs->make<TH1D>("h_scale_down", ";scale factor;jets/0.004", 50, 0.9, 1.1);
}

void MFVJetEnergyHistos::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<MFVEvent> mevent;
  event.getByToken(mevent_token, mevent);

  edm::Handle<double> weight;
  event.getByToken(weight_token, weight);
  const double w = *weight;

  edm::ESHandle<JetCorrectorParametersCollection> jet_corr;
  setup.get<JetCorrectionsRecord>().get("AK4PF", jet_corr);
  JetCorrectionUncertainty jec_unc((*jet_corr)["Uncertainty"]);

  h_w->Fill(w);

  h_njets->Fill(mevent->njets(), w);
  h_njets20->Fill(mevent->njets(20), w);
  h_jet_ht->Fill(mevent->jet_ht(), w);
  const double ht_40 = mevent->jet_ht(40);
  h_jet_ht_40->Fill(ht_40, w);
  if (ht_40 > 1200) h_jet_ht_40_1200cut->Fill(ht_40, w);

  int njets_notmatched = 0;
  double ht_up = 0, ht_down = 0, ht_40_up = 0, ht_40_down = 0;

  for (int i = 0, ie = mevent->njets(); i < ie; ++i) {
    if (mevent->jet_pt[i] < mfv::min_jet_pt)
      continue;

    h_jet_pt->Fill(mevent->jet_pt[i], w);
    h_jet_eta->Fill(mevent->jet_eta[i], w);
    h_jet_phi->Fill(mevent->jet_phi[i], w);
    h_jet_energy->Fill(mevent->jet_energy[i], w);

    double scale_up = 1, scale_down = 1;

    if (jes) {
      jec_unc.setJetEta(mevent->jet_eta[i]);
      jec_unc.setJetPt(mevent->jet_pt[i]);
      scale_up   = 1 + jec_unc.getUncertainty(true);
      jec_unc.setJetEta(mevent->jet_eta[i]); // yes, you have to call the setters again
      jec_unc.setJetPt(mevent->jet_pt[i]);
      scale_down = 1 - jec_unc.getUncertainty(false);
    }
    else {
      int ind = -1;
      const double aeta = fabs(mevent->jet_eta[i]);
      if      (aeta < 0.522) ind = 0;
      else if (aeta < 0.783) ind = 1;
      else if (aeta < 1.131) ind = 2;
      else if (aeta < 1.305) ind = 3;
      else if (aeta < 1.740) ind = 4;
      else if (aeta < 1.930) ind = 5;
      else if (aeta < 2.043) ind = 6;
      else if (aeta < 2.322) ind = 7;
      else if (aeta < 2.500) ind = 8;
      else if (aeta < 2.853) ind = 9;
      else if (aeta < 2.964) ind = 10;
      else if (aeta < 3.139) ind = 11;
      else if (aeta < 5.191) ind = 12;
      else
	throw cms::Exception("BadJet") << "JER jet with pt " << mevent->jet_pt[i] << " eta " << mevent->jet_eta[i] << " out of range?";

      // https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution
#ifdef MFVNEUTRALINO_2017
      const double sf[13] = {1.1432, 1.1815, 1.0989, 1.1137, 1.1307, 1.1600, 1.2393, 1.2604, 1.4085, 1.9909, 2.2923, 1.2696, 1.1542};
      const double un[13] = {0.0222, 0.0484, 0.0456, 0.1397, 0.1470, 0.0976, 0.1909, 0.1501, 0.2020, 0.5684, 0.3743, 0.1089, 0.1524};
#elif defined(MFVNEUTRALINO_2018)
      const double sf[13] = {1.15, 1.134, 1.102, 1.134, 1.104, 1.149, 1.148, 1.114, 1.347, 2.137, 1.65, 1.225, 1.082};
      const double un[13] = {0.043, 0.08, 0.052, 0.112, 0.211, 0.159, 0.209, 0.191, 0.274, 0.524, 0.941, 0.194, 0.198};
#else
#error bad year
#endif

      if (mevent->jet_gen_energy[i] > 0) {
        const double up = sf[ind] + un[ind];
        const double dn = sf[ind] - un[ind];
        scale_up   = (mevent->jet_gen_energy[i] + up * (mevent->jet_energy[i] - mevent->jet_gen_energy[i])) / mevent->jet_energy[i];
        scale_down = (mevent->jet_gen_energy[i] + dn * (mevent->jet_energy[i] - mevent->jet_gen_energy[i])) / mevent->jet_energy[i];
      }
      else { // JMTBAD
        ++njets_notmatched;
        h_jet_pt_notmatched->Fill(mevent->jet_pt[i], w);
      }
    }

    //printf("jet %i pt %f eta %f up %f dn %f\n", i, mevent->jet_pt[i], mevent->jet_eta[i], scale_up, scale_down);

    h_scale_up->Fill(scale_up, w);
    h_scale_down->Fill(scale_down, w);

    h_jet_pt_up->Fill(mevent->jet_pt[i] * scale_up, w);
    h_jet_pt_down->Fill(mevent->jet_pt[i] * scale_down, w);
    ht_up += mevent->jet_pt[i] * scale_up;
    ht_down += mevent->jet_pt[i] * scale_down;
    if (mevent->jet_pt[i] > 40) {
      ht_40_up += mevent->jet_pt[i] * scale_up;
      ht_40_down += mevent->jet_pt[i] * scale_down;
    }
  }

  h_njets_notmatched->Fill(njets_notmatched, w);
  h_jet_ht_up->Fill(ht_up, w);
  h_jet_ht_down->Fill(ht_down, w);
  h_jet_ht_40_up->Fill(ht_40_up, w);
  h_jet_ht_40_down->Fill(ht_40_down, w);
  h_jet_ht_40_mup->Fill(ht_40 - ht_40_up, w);
  h_jet_ht_40_mdown->Fill(ht_40 - ht_40_down, w);

  if (ht_40_up > 1200) h_jet_ht_40_up_1200cut->Fill(ht_40_up, w);
  if (ht_40_down > 1200) h_jet_ht_40_down_1200cut->Fill(ht_40_down, w);
}

DEFINE_FWK_MODULE(MFVJetEnergyHistos);
