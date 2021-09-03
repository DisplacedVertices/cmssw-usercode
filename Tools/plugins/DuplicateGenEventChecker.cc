#include "TH1.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DVCode/Tools/interface/Utilities.h"

class JMTDuplicateGenEventChecker : public edm::EDAnalyzer {
public:
  explicit JMTDuplicateGenEventChecker(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

private:
  const edm::EDGetTokenT<reco::GenParticleCollection> token;

  TH1D* h_px[4];
  TH1D* h_py[4];
  TH1D* h_pz[4];
  TH1D* h_vx;
  TH1D* h_vy;
  TH1D* h_vz;
};

JMTDuplicateGenEventChecker::JMTDuplicateGenEventChecker(const edm::ParameterSet& cfg)
  : token(consumes<reco::GenParticleCollection>(edm::InputTag("genParticles")))
{
  edm::Service<TFileService> fs;
  TH1::SetDefaultSumw2();

  // skip the protons, just look at the hard scatter in/out, usually 2->2 events (px and py of 0 and 1 should be 0)
  for (int i = 0; i < 4; ++i) {
    h_px[i] = fs->make<TH1D>(TString::Format("h_px_%i", i), "", 10000, -5000, 5000);
    h_py[i] = fs->make<TH1D>(TString::Format("h_py_%i", i), "", 10000, -5000, 5000);
    h_pz[i] = fs->make<TH1D>(TString::Format("h_pz_%i", i), "", 10000, -5000, 5000);
  }

  // the vertex of the first particle displaced by more than 10 um
  h_vx = fs->make<TH1D>("h_vx", "", 10000, -1, 1);
  h_vy = fs->make<TH1D>("h_vy", "", 10000, -1, 1);
  h_vz = fs->make<TH1D>("h_vz", "", 10000, -20, 20);
}

void JMTDuplicateGenEventChecker::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<reco::GenParticleCollection> particles;
  event.getByToken(token, particles);

  if (particles->size() < 6)
    throw cms::Exception("BadAssumption", "genParticles size less than 6");

  for (int i = 0; i < 4; ++i) {
    const auto& g = (*particles)[i+2]; // skip the protons, just look at the hard scatter in/out, usually 2->2 events
    h_px[i]->Fill(g.px());
    h_py[i]->Fill(g.py());
    h_pz[i]->Fill(g.pz());
  }

  const double x = (*particles)[2].vx();
  const double y = (*particles)[2].vy();
  const double z = (*particles)[2].vz();

  for (size_t i = 2, ie = particles->size(); i < ie; ++i) {
    const auto& g = (*particles)[i];
    if (mag(x - g.vx(),
            y - g.vy(),
            z - g.vz()) > 0.001) {
      h_vx->Fill(g.vx());
      h_vy->Fill(g.vy());
      h_vz->Fill(g.vz());
      break;
    }
  }
}

DEFINE_FWK_MODULE(JMTDuplicateGenEventChecker);
