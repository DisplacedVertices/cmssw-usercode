#include <boost/foreach.hpp>
#include "TH1F.h"
#include "TH2F.h"
#include "TLorentzVector.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
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
};

MFVNeutralinoGenHistos::MFVNeutralinoGenHistos(const edm::ParameterSet& cfg)
  : gen_src(cfg.getParameter<edm::InputTag>("gen_src")),
    gen_jet_src(cfg.getParameter<edm::InputTag>("gen_jet_src")),
    gen_met_src(cfg.getParameter<edm::InputTag>("gen_met_src"))
{
  edm::Service<TFileService> fs;

  h_vtx_2d = fs->make<TH2F>("h_vtx_2d", "", 100, -10, 10, 100, -10, 10);
}

void MFVNeutralinoGenHistos::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  setup.getData(pdt);

  edm::Handle<reco::GenParticleCollection> gens;
  event.getByLabel(gen_src, gens);
  edm::Handle<reco::GenJetCollection> gen_jets;
  event.getByLabel(gen_jet_src, gen_jets);
  edm::Handle<reco::GenMETCollection> gen_mets;
  event.getByLabel(gen_met_src, gen_mets);
  const reco::GenMET& gen_met = gen_mets->at(0);

  BOOST_FOREACH(const reco::GenParticle& gen, *gens) {
    if (gen.pdgId() == 1000022 && gen.status() == 52) {
      h_vtx_2d->Fill(gen.vx(), gen.vy());
    }
  }
}

DEFINE_FWK_MODULE(MFVNeutralinoGenHistos);
