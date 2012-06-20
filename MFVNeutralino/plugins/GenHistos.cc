#include <boost/foreach.hpp>
#include "TH1F.h"
#include "TH2F.h"
#include "TLorentzVector.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/METReco/interface/GenMET.h"
#include "DataFormats/METReco/interface/GenMETCollection.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "SimGeneral/HepPDTRecord/interface/ParticleDataTable.h"

class MFVNeutralinoGenHistos : public edm::EDAnalyzer {
 public:
  explicit MFVNeutralinoGenHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::InputTag gen_src;
  const edm::InputTag gen_jet_src;
  const edm::InputTag gen_met_src;
  
  TH2F* h_vtx_2d;
  TH1F* h_rho;

  edm::ESHandle<ParticleDataTable> pdt;
};

MFVNeutralinoGenHistos::MFVNeutralinoGenHistos(const edm::ParameterSet& cfg)
  : gen_src(cfg.getParameter<edm::InputTag>("gen_src")),
    gen_jet_src(cfg.getParameter<edm::InputTag>("gen_jet_src")),
    gen_met_src(cfg.getParameter<edm::InputTag>("gen_met_src"))
{
  edm::Service<TFileService> fs;

  h_vtx_2d = fs->make<TH2F>("h_vtx_2d", "", 100, -10, 10, 100, -10, 10);
  h_rho = fs->make<TH1F>("h_rho", "", 100, 0, 10);
}

void MFVNeutralinoGenHistos::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  setup.getData(pdt);

  edm::Handle<reco::GenParticleCollection> gens;
  event.getByLabel(gen_src, gens);
  edm::Handle<reco::GenJetCollection> gen_jets;
  event.getByLabel(gen_jet_src, gen_jets);
  edm::Handle<reco::GenMETCollection> gen_mets;
  event.getByLabel(gen_met_src, gen_mets);
  //const reco::GenMET& gen_met = gen_mets->at(0);

  edm::Handle<reco::BeamSpot> bs;
  event.getByLabel("offlineBeamSpot", bs);
  printf("beamspot x,y: %f, %f\n", bs->x0(), bs->y0());

  // Assume pythia line 2 (probably a gluon) has the "right"
  // production vertex. (The protons are just at 0,0,0.)
  const reco::GenParticle& for_vtx = gens->at(2);
  float vx = for_vtx.vx(), vy = for_vtx.vy(), vz = for_vtx.vz();
  printf("gluon x,y: %f, %f\n", vx, vy);
  
  BOOST_FOREACH(const reco::GenParticle& gen, *gens) {
    if (gen.pdgId() == 1000022 && gen.status() == 52 && gen.numberOfDaughters() == 3) {
      printf("neutralino vertex: %f, %f, %f\n", gen.vx() - vx, gen.vy() - vy, gen.vz() - vz);
      float dx, dy, dz;
      dx = dy = dz = 1e99;
      for (int i = 0, ie = int(gen.numberOfDaughters()); i < ie; ++i) {
	dx =  gen.daughter(i)->vx() - vx;
	dy =  gen.daughter(i)->vy() - vy;
	dz =  gen.daughter(i)->vz() - vz;
	printf("neutralino daughter %i: id %i pt %f eta %f phi %f vertex: %f, %f, %f (rho: %f)\n", i, gen.daughter(i)->pdgId(), gen.daughter(i)->pt(), gen.daughter(i)->eta(), gen.daughter(i)->phi(), dx, dy, dz, sqrt(dx*dx + dy*dy));
      }
      h_vtx_2d->Fill(dx, dy);
      h_rho->Fill(sqrt(dx*dx + dy*dy));
    }
  }
}

DEFINE_FWK_MODULE(MFVNeutralinoGenHistos);
