#include "TH2F.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

class JMTGenParticleHistos : public edm::EDAnalyzer {
public:
  explicit JMTGenParticleHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

private:
  const edm::EDGetTokenT<reco::GenParticleCollection> token;

  TH1F* h_firstparton_vx;
  TH1F* h_firstparton_vy;
  TH1F* h_firstparton_vz;

  TH1F* h_status1_vx;
  TH1F* h_status1_vy;
  TH1F* h_status1_vz;
};

JMTGenParticleHistos::JMTGenParticleHistos(const edm::ParameterSet& cfg)
  : token(consumes<reco::GenParticleCollection>(cfg.getParameter<edm::InputTag>("src")))
{
  edm::Service<TFileService> fs;
  h_firstparton_vx = fs->make<TH1F>("h_firstparton_vx", "", 1000, -1, 1);
  h_firstparton_vy = fs->make<TH1F>("h_firstparton_vy", "", 1000, -1, 1);
  h_firstparton_vz = fs->make<TH1F>("h_firstparton_vz", "", 1000, -20, 20);
  h_status1_vx = fs->make<TH1F>("h_status1_vx", "", 1000, -1, 1);
  h_status1_vy = fs->make<TH1F>("h_status1_vy", "", 1000, -1, 1);
  h_status1_vz = fs->make<TH1F>("h_status1_vz", "", 1000, -20, 20);
}

void JMTGenParticleHistos::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<reco::GenParticleCollection> particles;
  event.getByToken(token, particles);

  const reco::GenParticle& p = particles->at(2);
  h_firstparton_vx->Fill(p.vx());
  h_firstparton_vy->Fill(p.vy());
  h_firstparton_vz->Fill(p.vz());

  for (const reco::GenParticle& p : *particles) {
    if (p.status() == 1) {
      h_status1_vx->Fill(p.vx());
      h_status1_vy->Fill(p.vy());
      h_status1_vz->Fill(p.vz());
    }

  }
}

DEFINE_FWK_MODULE(JMTGenParticleHistos);
