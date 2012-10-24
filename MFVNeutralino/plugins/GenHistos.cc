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
  
  TH1F* h_num_ninos;
  TH2F* h_vtx_2d;
  TH1F* h_rho;
  TH1F* h_ninobeta;
  TH1F* h_ninobetagamma;
  TH1F* h_max_dR;
  TH1F* h_min_dR;
  TH2F* h_max_dR_vs_ninobeta;
  TH2F* h_min_dR_vs_ninobeta;
  TH2F* h_max_dR_vs_ninobetagamma;
  TH2F* h_min_dR_vs_ninobetagamma;

  edm::ESHandle<ParticleDataTable> pdt;
};

MFVNeutralinoGenHistos::MFVNeutralinoGenHistos(const edm::ParameterSet& cfg)
  : gen_src(cfg.getParameter<edm::InputTag>("gen_src")),
    gen_jet_src(cfg.getParameter<edm::InputTag>("gen_jet_src")),
    gen_met_src(cfg.getParameter<edm::InputTag>("gen_met_src"))
{
  edm::Service<TFileService> fs;

  h_num_ninos = fs->make<TH1F>("h_num_ninos", "", 5, 0, 5);
  h_vtx_2d = fs->make<TH2F>("h_vtx_2d", "", 500, -1, 1, 500, -1, 1);
  h_rho = fs->make<TH1F>("h_rho", "", 100, 0, 2);
  h_ninobeta = fs->make<TH1F>("h_ninobeta", "", 100, 0, 1);
  h_ninobetagamma = fs->make<TH1F>("h_ninobetagamma", "", 100, 0, 10);
  h_max_dR = fs->make<TH1F>("h_max_dR", "", 100, 0, 5);
  h_min_dR = fs->make<TH1F>("h_min_dR", "", 100, 0, 5);
  h_max_dR_vs_ninobeta = fs->make<TH2F>("h_max_dR_vs_ninobeta", "", 100, 0, 1, 100, 0, 5);
  h_min_dR_vs_ninobeta = fs->make<TH2F>("h_min_dR_vs_ninobeta", "", 100, 0, 1, 100, 0, 5);
  h_max_dR_vs_ninobetagamma = fs->make<TH2F>("h_max_dR_vs_ninobetagamma", "", 100, 0, 10, 100, 0, 5);
  h_min_dR_vs_ninobetagamma = fs->make<TH2F>("h_min_dR_vs_ninobetagamma", "", 100, 0, 10, 100, 0, 5);
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
  const float vx = for_vtx.vx();
  const float vy = for_vtx.vy();
  printf("gluon x,y: %f, %f\n", vx, vy);

  int num_ninos = 0;
  const int ndau = 3;
  const int dau_id_order[ndau] = { 3, 5, 6 };

  BOOST_FOREACH(const reco::GenParticle& gen, *gens) {
    if (!(gen.pdgId() == 1000022 && gen.status() == 52 && gen.numberOfDaughters() == 3))
      continue;
    const reco::GenParticle& nino = gen;

    ++num_ninos;
    const double ninobeta  = nino.p()/nino.energy();
    const double ninobetagamma = ninobeta/sqrt(1-ninobeta*ninobeta);
    h_ninobeta->Fill(ninobeta);
    h_ninobetagamma->Fill(ninobetagamma);
    
    // Get the immediate daughters, in order by the ids specified in
    // dau_id_order.
    const reco::Candidate* daughters[ndau] = {0};
    for (int i = 0; i < ndau; ++i) {
      int id = nino.daughter(i)->pdgId();
      for (int j = 0; j < ndau; ++j) {
	if (abs(id) == dau_id_order[j])
	  daughters[j] = nino.daughter(i);
      }
    }

    // Make sure we found all three daughters, and then get the
    // "final" state daughters (having status 22 or 23 depending on
    // quark type).
    for (int i = 0; i < ndau; ++i) {
      const reco::Candidate* dau = daughters[i];
      if (dau == 0)
	throw cms::Exception("DaughterNotFound") << "did not find daughter for neutralino with id " << dau_id_order[i];
      
      while (daughters[i]->status() != 22 && daughters[i]->status() != 23) {
	for (int j = 0, je = int(dau->numberOfDaughters()); j < je; ++j)
	  if (dau->pdgId() == dau->daughter(j)->pdgId())
	    daughters[i] = dau->daughter(j);
	if (daughters[i] == dau)
	  throw cms::Exception("FinalDaughterNotFound") << "for id " << dau_id_order[i] << ", final state (22 or 23) daughter descendant not found";
      }
    }

    // Fill some simple histos: 2D vertex location, and distance to
    // origin, and the min/max deltaR of the daughters (also versus
    // nino boost).
    float dx = daughters[0]->vx() - vx;
    float dy = daughters[0]->vy() - vy;
    h_vtx_2d->Fill(dx, dy);
    h_rho->Fill(sqrt(dx*dx + dy*dy));

    float min_dR =  1e99;
    float max_dR = -1e99;
    for (int i = 0; i < ndau; ++i) {
      for (int j = i+1; j < ndau; ++j) {
	float dR = reco::deltaR(*daughters[i], *daughters[j]);
	if (dR < min_dR)
	  min_dR = dR;
	if (dR > max_dR)
	  max_dR = dR;
      }
    }

    h_min_dR->Fill(min_dR);
    h_max_dR->Fill(max_dR);
    h_min_dR_vs_ninobeta->Fill(ninobeta, min_dR);
    h_max_dR_vs_ninobeta->Fill(ninobeta, max_dR);
    h_min_dR_vs_ninobetagamma->Fill(ninobetagamma, min_dR);
    h_max_dR_vs_ninobetagamma->Fill(ninobetagamma, max_dR);
  }

  h_num_ninos->Fill(num_ninos);
}

DEFINE_FWK_MODULE(MFVNeutralinoGenHistos);
