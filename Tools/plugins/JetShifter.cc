#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/MakerMacros.h"

class JMTJetShifter : public edm::EDProducer {
public:
  explicit JMTJetShifter(const edm::ParameterSet&);
private:
  void produce(edm::Event&, const edm::EventSetup&);

  const edm::InputTag jet_src;
  const bool enable;
  const bool jes;
  const bool up;
};

JMTJetShifter::JMTJetShifter(const edm::ParameterSet& cfg)
  : jet_src(cfg.getParameter<edm::InputTag>("jet_src")),
    enable(cfg.getParameter<bool>("enable")),
    jes(cfg.getParameter<bool>("jes")), // true jes, false jer
    up(cfg.getParameter<bool>("up"))
{
  produces<pat::JetCollection>();

  if (!jes) throw cms::Exception("NotImplemented", "JES");
}

void JMTJetShifter::produce(edm::Event& event, const edm::EventSetup& setup) {
  if (!jes && event.isRealData())
    throw cms::Exception("BadConfiguration", "JER requested but running on data");
    
  edm::Handle<pat::JetCollection> jets;
  event.getByLabel(jet_src, jets);
  
  std::auto_ptr<pat::JetCollection> new_jets(new pat::JetCollection);

  edm::ESHandle<JetCorrectorParametersCollection> jet_corr;
  setup.get<JetCorrectionsRecord>().get("AK4PF", jet_corr);
  JetCorrectionUncertainty jec_unc((*jet_corr)["Uncertainty"]);

  for (auto jet : *jets) {
    pat::Jet new_jet(jet);

    if (enable) {
      double scale = 1e9;

      if (jes) {
        jec_unc.setJetEta(jet.eta());
        jec_unc.setJetPt(jet.pt());
        const double unc = jec_unc.getUncertainty(up);
        if (up) scale = 1 + unc;
        else    scale = 1 - unc;
      }
      else {
        double factor = 1;

        const float aeta = fabs(jet.eta());
        if      (aeta < 0.5) {
          if (up) factor = 1.117;
          else    factor = 1.101;
        }
        else if (aeta < 0.8) {
          if (up) factor = 1.151;
          else    factor = 1.125;
        }
        else if (aeta < 1.1) {
          if (up) factor = 1.127;
          else    factor = 1.101;
        }
        else if (aeta < 1.3) {
          if (up) factor = 1.147;
          else    factor = 1.099;
        }
        else if (aeta < 1.7) {
          if (up) factor = 1.095;
          else    factor = 1.073;
        }
        else if (aeta < 1.9) {
          if (up) factor = 1.117;
          else    factor = 1.047;
        }
        else if (aeta < 2.1) {
          if (up) factor = 1.187;
          else    factor = 1.093;
        }
        else if (aeta < 2.3) {
          if (up) factor = 1.120;
          else    factor = 1.014;
        }
        else if (aeta < 2.5) {
          if (up) factor = 1.218;
          else    factor = 1.136;
        }
        else if (aeta < 2.8) {
          if (up) factor = 1.403;
          else    factor = 1.325;
        }
        else if (aeta < 3.0) {
          if (up) factor = 1.928;
          else    factor = 1.786;
        }
        else if (aeta < 3.2) {
          if (up) factor = 1.350;
          else    factor = 1.306;
        }
        else if (aeta < 5.0) {
          if (up) factor = 1.189;
          else    factor = 1.131;
        }
        else
          throw cms::Exception("BadJet") << "JER jet with pt " << jet.pt() << " eta " << jet.eta() << " out of range?";

        if (!jet.genJet())
          throw cms::Exception("BadJet") << "jet with pt " << jet.pt() << " eta " << jet.eta() << " has no gen jet";


        const float gen_jet_energy = jet.genJet()->energy();
        scale = (gen_jet_energy + factor*(jet.energy() - jet.genJet()->energy()))/jet.energy();
      }

      new_jet.scaleEnergy(scale);
    }


    new_jets->push_back(new_jet);
  }

  event.put(new_jets);
}

DEFINE_FWK_MODULE(JMTJetShifter);
