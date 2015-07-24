#include "TH2F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralino/interface/MCInteractionMFV3j.h"

class MFVCorrelationsForGeomEff : public edm::EDAnalyzer {
public:
  explicit MFVCorrelationsForGeomEff(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);
private:

  TH2F* h_phi;
  TH2F* h_costheta;
  TH2F* h_betagamma;
};

MFVCorrelationsForGeomEff::MFVCorrelationsForGeomEff(const edm::ParameterSet& cfg) {
  edm::Service<TFileService> fs;

  h_phi = fs->make<TH2F>("h_phi", "", 40, -M_PI, M_PI, 40, -M_PI, M_PI);
  h_costheta = fs->make<TH2F>("h_costheta", "", 40, -1, 1.001, 40, -1, 1.001);
  h_betagamma = fs->make<TH2F>("h_betagamma", "", 40, 0, 10, 40, 0, 10);
}

namespace {
  float mag(float x, float y, float z) {
    return sqrt(x*x + y*y + z*z);
  }
}

void MFVCorrelationsForGeomEff::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<reco::GenParticleCollection> gen_particles;
  event.getByLabel("genParticles", gen_particles);

  MCInteractionMFV3j mci;
  mci.Init(*gen_particles);

  h_phi->Fill(mci.lsps[0]->phi(), mci.lsps[1]->phi());

  h_costheta->Fill(mci.p4_lsps[0].CosTheta(),
                   mci.p4_lsps[1].CosTheta());
  h_betagamma->Fill(mci.p4_lsps[0].Beta() * mci.p4_lsps[0].Gamma(),
                    mci.p4_lsps[1].Beta() * mci.p4_lsps[1].Gamma());
}

DEFINE_FWK_MODULE(MFVCorrelationsForGeomEff);
