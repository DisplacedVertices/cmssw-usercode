#include "TTree.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralino/interface/MCInteractionMFV3j.h"

class MFVGenNtupleDumper : public edm::EDAnalyzer {
 public:
  explicit MFVGenNtupleDumper(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::InputTag gen_src;
  
  struct ntuple_t {
    unsigned run;
    unsigned lumi;
    unsigned event;
    float lsp_pt[2];
    float lsp_eta[2];
    float lsp_phi[2];
    float lsp_mass[2];
    float lsp_decay_vx[2];
    float lsp_decay_vy[2];
    float lsp_decay_vz[2];
  };

  ntuple_t nt;
  TTree* tree;
};

MFVGenNtupleDumper::MFVGenNtupleDumper(const edm::ParameterSet& cfg)
  : gen_src(cfg.getParameter<edm::InputTag>("gen_src"))
{
  edm::Service<TFileService> fs;
  tree = fs->make<TTree>("t", "");
  tree->Branch("run", &nt.run, "run/i");
  tree->Branch("lumi", &nt.lumi, "lumi/i");
  tree->Branch("event", &nt.event, "event/i");
  tree->Branch("lsp_pt", nt.lsp_pt, "lsp_pt[2]/F");
  tree->Branch("lsp_eta", nt.lsp_eta, "lsp_eta[2]/F");
  tree->Branch("lsp_phi", nt.lsp_phi, "lsp_phi[2]/F");
  tree->Branch("lsp_mass", nt.lsp_mass, "lsp_mass[2]/F");
  tree->Branch("lsp_decay_vx", nt.lsp_decay_vx, "lsp_decay_vx[2]/F");
  tree->Branch("lsp_decay_vy", nt.lsp_decay_vy, "lsp_decay_vy[2]/F");
  tree->Branch("lsp_decay_vz", nt.lsp_decay_vz, "lsp_decay_vz[2]/F");
}

void MFVGenNtupleDumper::analyze(const edm::Event& event, const edm::EventSetup&) {
  memset(&nt, 0, sizeof(ntuple_t));
  nt.run  = event.id().run();
  nt.lumi = event.luminosityBlock();
  nt.event = event.id().event();

  edm::Handle<reco::GenParticleCollection> gen_particles;
  event.getByLabel(gen_src, gen_particles);

  MCInteractionMFV3j mci;
  mci.Init(*gen_particles);
  if (!mci.Valid()) {
    edm::LogWarning("GenHistos") << "MCInteractionMFV3j invalid!";
    return;
  }

  for (int i = 0; i < 2; ++i) {
    nt.lsp_pt[i] = mci.lsps[i]->pt();
    nt.lsp_eta[i] = mci.lsps[i]->eta();
    nt.lsp_phi[i] = mci.lsps[i]->phi();
    nt.lsp_mass[i] = mci.lsps[i]->mass();
    nt.lsp_decay_vx[i] = mci.stranges[i]->vx();
    nt.lsp_decay_vy[i] = mci.stranges[i]->vy();
    nt.lsp_decay_vz[i] = mci.stranges[i]->vz();
  }

  tree->Fill();
}

DEFINE_FWK_MODULE(MFVGenNtupleDumper);
