#include "TH2.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralinoFormats/interface/MCInteractions.h"
#include "JMTucker/Tools/interface/Utilities.h"

class MFVCorrelationsForGeomEff : public edm::EDAnalyzer {
public:
  explicit MFVCorrelationsForGeomEff(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

private:
  const edm::EDGetTokenT<mfv::MCInteraction> mci_token;

  TH2F* h_phi;
  TH2F* h_costheta;
  TH2F* h_betagamma;
};

MFVCorrelationsForGeomEff::MFVCorrelationsForGeomEff(const edm::ParameterSet& cfg)
  : mci_token(consumes<mfv::MCInteraction>(cfg.getParameter<edm::InputTag>("mci_src")))
{
  edm::Service<TFileService> fs;
  h_phi = fs->make<TH2F>("h_phi", "", 40, -M_PI, M_PI, 40, -M_PI, M_PI);
  h_costheta = fs->make<TH2F>("h_costheta", "", 40, -1, 1.001, 40, -1, 1.001);
  h_betagamma = fs->make<TH2F>("h_betagamma", "", 40, 0, 10, 40, 0, 10);
}

void MFVCorrelationsForGeomEff::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<mfv::MCInteraction> mci;
  event.getByToken(mci_token, mci);

  h_phi->Fill(mci->lsp(0)->phi(), mci->lsp(1)->phi());

  TLorentzVector p0 = make_tlv(mci->lsp(0));
  TLorentzVector p1 = make_tlv(mci->lsp(1));

  h_costheta->Fill(p0.CosTheta(), p1.CosTheta());
  h_betagamma->Fill(p0.Beta() * p0.Gamma(),
                    p1.Beta() * p1.Gamma());
}

DEFINE_FWK_MODULE(MFVCorrelationsForGeomEff);
