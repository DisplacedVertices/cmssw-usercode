#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

class MFVJECPATProducer : public edm::EDProducer {
public:
  explicit MFVJECPATProducer(const edm::ParameterSet&);
private:
  void produce(edm::Event&, const edm::EventSetup&);

  const edm::InputTag jet_src;
  const bool enable;
  const bool jes;
  const bool up;
};

MFVJECPATProducer::MFVJECPATProducer(const edm::ParameterSet& cfg)
  : jet_src(cfg.getParameter<edm::InputTag>("jet_src")),
    enable(cfg.getParameter<bool>("enable")),
    jes(cfg.getParameter<bool>("jes")),
    up(cfg.getParameter<bool>("up"))
{
  produces<pat::JetCollection>();
}

void MFVJECPATProducer::produce(edm::Event& event, const edm::EventSetup&) {
  throw cms::Exception("NotImplemented");

  edm::Handle<pat::JetCollection> jets;
  event.getByLabel(jet_src, jets);
  
  std::auto_ptr<pat::JetCollection> new_jets(new pat::JetCollection);

  JetCorrectionUncertainty jec_unc("Summer13_V4_MC_Uncertainty_AK5PF.txt");

  for (std::vector<pat::Jet>::const_iterator jet = jets->begin(), jete = jets->end(); jet != jete; ++jet) {
    if (!jet->genJet())
      throw cms::Exception("BadJet") << "jet with pt " << jet->pt() << " eta " << jet->eta() << " has no gen jet";

    float scale = 1e9;
    pat::Jet new_jet(*jet);

    if (jes) {
      jec_unc.setJetEta(jet->eta());
      jec_unc.setJetPt(jet->pt());
      const float uncertainty = jec_unc.getUncertainty(up);
      if (up) scale = 1 + uncertainty;
      else    scale = 1 - uncertainty;
    }
    else {
      float factor;

      const float aeta = fabs(jet->eta());
      if (aeta < 0.5) {
        if (up) factor = 1.115;
        else    factor = 0.990;
      }
      else if (aeta < 1.1 && aeta > 0.5) {
        if (up) factor = 1.114;
        else    factor = 1.001;
      }
      else if (aeta < 1.7 && aeta > 1.1) {
	if (up) factor = 1.161;
	else    factor = 1.032;
      }
      else if (aeta < 2.3 && aeta > 1.7) {
	if (up) factor = 1.228;
	else    factor = 1.042;
      }
      else if (aeta < 5.0 && aeta > 2.3) {
	if (up) factor = 1.488;
	else    factor = 1.089;
      }
      else
        throw cms::Exception("BadJet") << "jet with pt " << jet->pt() << " eta " << jet->eta();

      const float gen_jet_energy = jet->genJet()->energy();
      scale = (gen_jet_energy + factor*(jet->energy() - jet->genJet()->energy()))/jet->energy();
    }
    
    if (enable)
      new_jet.scaleEnergy(scale);

    new_jets->push_back(new_jet);
  }

  event.put(new_jets);
}

DEFINE_FWK_MODULE(MFVJECPATProducer);
