#include "TH1F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "SimDataFormats/TrackingAnalysis/interface/TrackingParticle.h"
#include "JMTucker/Tools/interface/GenUtilities.h"

class CheckGenParticleBarcodes : public edm::EDAnalyzer {
public:
  explicit CheckGenParticleBarcodes(const edm::ParameterSet&);

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  const edm::InputTag gen_particles_src;
  const edm::InputTag tracking_particles_src;

  TH1F* h_genpbarcodes;
  TH1F* h_tpgenpsize;
  TH1F* h_hepmcgenpminds;
  TH1F* h_hepmcbarcodes;
};

CheckGenParticleBarcodes::CheckGenParticleBarcodes(const edm::ParameterSet& cfg) 
  : gen_particles_src(cfg.getParameter<edm::InputTag>("gen_particles_src")),
    tracking_particles_src(cfg.getParameter<edm::InputTag>("tracking_particles_src"))
{
  edm::Service<TFileService> fs;
  h_genpbarcodes   = fs->make<TH1F>("h_genpbarcodes", "", 10, -1, 1);
  h_tpgenpsize 	   = fs->make<TH1F>("h_tpgenpsize", "", 10, 0, 10);
  h_hepmcgenpminds = fs->make<TH1F>("h_hepmcgenpminds", "", 1000, 0, 0.01);
  h_hepmcbarcodes  = fs->make<TH1F>("h_hepmcbarcodes", "", 10, -1, 1);
}

namespace {
  template <typename T>
  T mag(const T& x, const T& y, const T& z) {
    return sqrt(x*x + y*y + z*z);
  }
}

void CheckGenParticleBarcodes::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<reco::GenParticleCollection> gen_particles;
  edm::Handle<std::vector<int> > gen_particles_barcodes;
  event.getByLabel(gen_particles_src, gen_particles);
  event.getByLabel(gen_particles_src, gen_particles_barcodes);

  edm::Handle<TrackingParticleCollection> tracking_particles;
  event.getByLabel(tracking_particles_src, tracking_particles);

  int ibc = 0;
  for (const auto& bc : *gen_particles_barcodes) {
    h_genpbarcodes->Fill(bc - ibc - 1);
    ++ibc;
  }

  for (const auto& tp : *tracking_particles) {
    h_tpgenpsize->Fill(tp.genParticle().size());
    for (const auto& hepmc : tp.genParticle()) {
      int barcode_minus_1 = hepmc->barcode() - 1;

      int min_igenp = -1;
      float min_d = 1e300;
      int igenp = 0;
      for (const auto& genp : *gen_particles) {
	float d = mag(hepmc->momentum().perp()  - genp.pt(),
		      hepmc->momentum().eta()   - genp.eta(),
		      hepmc->momentum().phi()   - genp.phi());
	if (d < min_d) {
	  min_d = d;
	  min_igenp = igenp;
	}
	++igenp;
      }

      if (min_igenp != barcode_minus_1) {
	const reco::GenParticle* bm1 = &gen_particles->at(barcode_minus_1);
	const reco::GenParticle* mig = &gen_particles->at(min_igenp);
	if ((is_ancestor_of(bm1, mig) || is_ancestor_of(mig, bm1)) && min_d < 1e-4)
	  min_igenp = barcode_minus_1;
      }

      h_hepmcgenpminds->Fill(min_d);
      h_hepmcbarcodes->Fill(min_igenp - barcode_minus_1);
      if (min_igenp != barcode_minus_1) {
	printf("barcode_minus_1 = %i not equal min_igenp = %i for this guy, where gen_particles_barcodes \n", barcode_minus_1, min_igenp);
	hepmc->print();
      }
    }
  }
}

DEFINE_FWK_MODULE(CheckGenParticleBarcodes);
