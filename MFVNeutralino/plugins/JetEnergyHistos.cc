#include "TH2F.h"
#include "TRandom3.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralino/interface/EventTools.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"

#define NBDISC 2

class MFVJetEnergyHistos : public edm::EDAnalyzer {
 public:
  explicit MFVJetEnergyHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::EDGetTokenT<MFVEvent> mevent_token;
  const edm::EDGetTokenT<double> weight_token;
  const bool jes;

  TH1F* h_w;

  TH1F* h_njets;
  TH1F* h_jet_ht;
  TH1F* h_jet_ht_40;

  TH1F* h_jet_pt;
  TH1F* h_jet_eta;
  TH1F* h_jet_phi;
  TH1F* h_jet_energy;

  TH1F* h_jet_pt_up;
  TH1F* h_jet_pt_down;
  TH1F* h_jet_ht_up;
  TH1F* h_jet_ht_down;
  TH1F* h_jet_ht_40_up;
  TH1F* h_jet_ht_40_down;

  TH1F* h_jet_ht_40_1000cut;
  TH1F* h_jet_ht_40_up_1000cut;
  TH1F* h_jet_ht_40_down_1000cut;  

  TH1F* h_scale_up;
  TH1F* h_scale_down;
};

MFVJetEnergyHistos::MFVJetEnergyHistos(const edm::ParameterSet& cfg)
  : mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
    jes(cfg.getParameter<bool>("jes")) // true jes, false jer
{
  edm::Service<TFileService> fs;

  h_w = fs->make<TH1F>("h_w", ";event weight;events/0.1", 100, 0, 10);

  h_njets = fs->make<TH1F>("h_njets", ";# of jets;events", 20, 0, 20);
  h_jet_ht = fs->make<TH1F>("h_jet_ht", ";H_{T} of jets (GeV);events/25 GeV", 200, 0, 5000);
  h_jet_ht_40 = fs->make<TH1F>("h_jet_ht_40", ";H_{T} of jets with p_{T} > 40 GeV;events/25 GeV", 200, 0, 5000);

  h_jet_pt = fs->make<TH1F>("h_jet_pt", ";jets p_{T} (GeV);jets/10 GeV", 100, 0, 1000);
  h_jet_eta = fs->make<TH1F>("h_jet_eta", ";jets #eta (rad);jets/.08", 100, -4, 4);
  h_jet_phi = fs->make<TH1F>("h_jet_phi", ";jets #phi (rad);jets/.063", 100, -3.1416, 3.1416);
  h_jet_energy = fs->make<TH1F>("h_jet_energy", ";jets energy (GeV);jets/10 GeV", 100, 0, 1000);

  h_jet_pt_up = fs->make<TH1F>("h_jet_pt_up", ";shifted up jets p_{T} (GeV);jets/10 GeV", 100, 0, 1000);
  h_jet_pt_down = fs->make<TH1F>("h_jet_pt_down", ";shifted down jets p_{T} (GeV);jets/10 GeV", 100, 0, 1000);
  h_jet_ht_up = fs->make<TH1F>("h_jet_ht_up", ";shifted up H_{T} of jets (GeV);events/25 GeV", 200, 0, 5000);
  h_jet_ht_down = fs->make<TH1F>("h_jet_ht_down", ";shifted down H_{T} of jets (GeV);events/25 GeV", 200, 0, 5000);
  h_jet_ht_40_up = fs->make<TH1F>("h_jet_ht_40_up", ";shifted up H_{T} of jets (GeV);events/25 GeV", 200, 0, 5000);
  h_jet_ht_40_down = fs->make<TH1F>("h_jet_ht_40_down", ";shifted down H_{T} of jets (GeV);events/25 GeV", 200, 0, 5000);

  h_jet_ht_40_1000cut = fs->make<TH1F>("h_jet_ht_40_1000cut", ";H_{T} of jets (GeV);events/25 GeV", 200, 0, 5000);
  h_jet_ht_40_up_1000cut = fs->make<TH1F>("h_jet_ht_40_up_1000cut", ";shifted up H_{T} of jets (GeV);events/25 GeV", 200, 0, 5000);
  h_jet_ht_40_down_1000cut = fs->make<TH1F>("h_jet_ht_40_down_1000cut", ";shifted down H_{T} of jets (GeV);events/25 GeV", 200, 0, 5000);

  h_scale_up = fs->make<TH1F>("h_scale_up", ";scale factor;jets/0.004", 50, 0.9, 1.1);
  h_scale_down = fs->make<TH1F>("h_scale_down", ";scale factor;jets/0.004", 50, 0.9, 1.1);
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

  double scale_up = 1e9;
  double scale_down = 1e9;
  
  h_w->Fill(w);

  h_njets->Fill(mevent->njets(), w);
  h_jet_ht->Fill(mevent->jet_ht(), w);
  h_jet_ht_40->Fill(mevent->jet_ht(40), w);
  if (mevent->jet_ht(40) > 1000) h_jet_ht_40_1000cut->Fill(mevent->jet_ht(40), w); 

  double ht_up = 0;
  double ht_down = 0;
  double ht_40_up = 0;
  double ht_40_down = 0;

  for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
    h_jet_pt->Fill(mevent->jet_pt[ijet]);
    h_jet_eta->Fill(mevent->jet_eta[ijet]);
    h_jet_phi->Fill(mevent->jet_phi[ijet]);
    h_jet_energy->Fill(mevent->jet_energy[ijet]);

    jec_unc.setJetEta(mevent->jet_eta[ijet]);
    jec_unc.setJetPt(mevent->jet_pt[ijet]);
    const double unc_up = jec_unc.getUncertainty(true);

    jec_unc.setJetEta(mevent->jet_eta[ijet]);
    jec_unc.setJetPt(mevent->jet_pt[ijet]);
    const double unc_down = jec_unc.getUncertainty(false);

    if (jes) {
      double mult = 1.0;
      scale_up = 1 + mult * unc_up;
      scale_down = 1 - mult * unc_down;
    }
    else {
      double factorup = 1;
      double factordown = 1;
      const float aeta = fabs(mevent->jet_eta[ijet]);
      if      (aeta < 0.5) {
	factorup = 1.117;
	factordown = 1.101;
      }
      else if (aeta < 0.8) {
	factorup = 1.151;
	factordown = 1.125;
      }
      else if (aeta < 1.1) {
	factorup = 1.127;
	factordown = 1.101;
      }
      else if (aeta < 1.3) {
	factorup = 1.147;
	factordown = 1.099;
      }
      else if (aeta < 1.7) {
	factorup = 1.095;
	factordown = 1.073;
      }
      else if (aeta < 1.9) {
	factorup = 1.117;
	factordown = 1.047;
      }
      else if (aeta < 2.1) {
	factorup = 1.187;
	factordown = 1.093;
      }
      else if (aeta < 2.3) {
	factorup = 1.120;
	factordown = 1.014;
      }
      else if (aeta < 2.5) {
	factorup = 1.218;
	factordown = 1.136;
      }
      else if (aeta < 2.8) {
	factorup = 1.403;
	factordown = 1.325;
      }
      else if (aeta < 3.0) {
	factorup = 1.928;
	factordown = 1.786;
      }
      else if (aeta < 3.2) {
	factorup = 1.350;
	factordown = 1.306;
      }
      else if (aeta < 5.0) {
	factorup = 1.189;
	factordown = 1.131;
      }
      else
	throw cms::Exception("BadJet") << "JER jet with pt " << mevent->jet_pt[ijet] << " eta " << mevent->jet_eta[ijet] << " out of range?";

      const float gen_jet_energy = gRandom->Gaus(mevent->jet_energy[ijet], 0.1);
      scale_up = (gen_jet_energy + factorup * (mevent->jet_energy[ijet] - gen_jet_energy))/mevent->jet_energy[ijet];
      scale_down = (gen_jet_energy + factordown * (mevent->jet_energy[ijet] - gen_jet_energy))/mevent->jet_energy[ijet];
    }

    h_scale_up->Fill(scale_up);
    h_scale_down->Fill(scale_down);

    h_jet_pt_up->Fill(mevent->jet_pt[ijet] * scale_up);
    h_jet_pt_down->Fill(mevent->jet_pt[ijet] * scale_down);
    ht_up += mevent->jet_pt[ijet] * scale_up;
    ht_down += mevent->jet_pt[ijet] * scale_down;
    if (mevent->jet_pt[ijet] > 40) {
      ht_40_up += mevent->jet_pt[ijet] * scale_up;
      ht_40_down += mevent->jet_pt[ijet] * scale_down;
    }
  }

  h_jet_ht_up->Fill(ht_up, w);
  h_jet_ht_down->Fill(ht_down, w);
  h_jet_ht_40_up->Fill(ht_40_up, w);
  h_jet_ht_40_down->Fill(ht_40_down, w);

  if (ht_40_up > 1000) h_jet_ht_40_up_1000cut->Fill(ht_40_up, w);
  if (ht_40_down > 1000) h_jet_ht_40_down_1000cut->Fill(ht_40_down, w);
}
DEFINE_FWK_MODULE(MFVJetEnergyHistos);
