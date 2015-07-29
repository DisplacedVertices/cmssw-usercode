#include "TH1F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

class MFVNeutralinoPATBTagCounting : public edm::EDAnalyzer {
 public:
  explicit MFVNeutralinoPATBTagCounting(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::InputTag vertex_src;
  const edm::InputTag jet_src;
  const std::string b_discriminator_name;
  const double jet_pt_min;
  const double bdisc_min;
  const edm::InputTag muon_src;
  const edm::InputTag electron_src;
  const bool verbose;

  TH1F* h_nbtags;
};

MFVNeutralinoPATBTagCounting::MFVNeutralinoPATBTagCounting(const edm::ParameterSet& cfg)
  : vertex_src(cfg.getParameter<edm::InputTag>("vertex_src")),
    jet_src(cfg.getParameter<edm::InputTag>("jet_src")),
    b_discriminator_name(cfg.getParameter<std::string>("b_discriminator_name")),
    jet_pt_min(cfg.getParameter<double>("jet_pt_min")),
    bdisc_min(cfg.getParameter<double>("bdisc_min")),
    muon_src(cfg.getParameter<edm::InputTag>("muon_src")),
    electron_src(cfg.getParameter<edm::InputTag>("electron_src")),
    verbose(cfg.getParameter<bool>("verbose"))
{
  if (verbose) std::cout << "MFVNeutralinoPATBTagCounting: b_discriminator_name: " << b_discriminator_name << " jet_pt_min: " << jet_pt_min << " bdisc_min: " << bdisc_min << "\n";

  edm::Service<TFileService> fs;
  h_nbtags = fs->make<TH1F>("h_nbtags", "", 30, 0, 30);
}

void MFVNeutralinoPATBTagCounting::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<reco::VertexCollection> vertices;
  event.getByLabel(vertex_src, vertices);

  edm::Handle<pat::JetCollection> jets;
  event.getByLabel(jet_src, jets);

  int njets = 0;
  int nbtags = 0;
  double jet_ht = 0;
  int nmuons = 0;
  int nelectrons = 0;

  // JMTBAD cuts to be kept in step with
  // JMTucker/Tools/python/PATTupleSelection_cfi.py; also note that
  // the jets/muons/electrons in PAT tuples have a certain base
  // selection on them anyway (see the aforementioned _cfi file).
  // ResolutionsHistogrammer.cc uses a StringCutObjectSelector using
  // the string from teh _cfi to keep the two in sync, but here we
  // explicitly code up the cuts for simplicity.

  for (int i = 0, ie = jets->size(); i < ie; ++i) {
    const pat::Jet& jet = jets->at(i);
    const reco::GenJet* gen_jet = jet.genJet();
    const double bdisc = jet.bDiscriminator(b_discriminator_name);

    if (verbose) {
      std::cout << "#" << i << ": pt eta phi: " << jet.pt() << ", " << jet.eta() << ", "<< jet.phi() << " gen jet (ptr: " << gen_jet;
      if (gen_jet)
	std::cout << ") pt eta phi: " << gen_jet->pt() << ", " << gen_jet->eta() << ", " << gen_jet->phi();
      std::cout << " bdisc: " << bdisc << "\n";
    }

    if (jet.pt() > jet_pt_min) {
      jet_ht += jet.pt();
      ++njets;

      if (bdisc > bdisc_min)
	++nbtags;
    }
  }

  edm::Handle<pat::MuonCollection> muons;
  event.getByLabel(muon_src, muons);

  for (int i = 0, ie = int(muons->size()); i < ie; ++i) {
    const pat::Muon& muon = muons->at(i);

    double iso = muon.chargedHadronIso() + muon.neutralHadronIso() + muon.photonIso() - 0.5*muon.puChargedHadronIso();
    double rel_iso = iso / muon.pt();

    double dxy = -999, dz = -999;
    if (vertices->size() > 0) {
      dxy = muon.innerTrack()->dxy(vertices->at(0).position());
      dz  = muon.innerTrack()->dz (vertices->at(0).position());
    }

    if (muon.isPFMuon() &&
	muon.isGlobalMuon() &&
	muon.pt() > 26 && 
	fabs(muon.eta()) < 2.1 &&
	fabs(dxy) < 0.2 &&
	fabs(dz) < 0.5 &&
	muon.globalTrack()->normalizedChi2() < 10. &&
	muon.track()->hitPattern().trackerLayersWithMeasurement() > 5 &&
	muon.globalTrack()->hitPattern().numberOfValidMuonHits() > 0 &&
	muon.innerTrack()->hitPattern().numberOfValidPixelHits() > 0 &&
	muon.numberOfMatchedStations() > 1 &&
	rel_iso < 0.12
	)
    ++nmuons;
  }

  edm::Handle<pat::ElectronCollection> electrons;
  event.getByLabel(electron_src, electrons);

  for (int i = 0, ie = int(electrons->size()); i < ie; ++i) {
    const pat::Electron& electron = electrons->at(i);

    double iso = electron.chargedHadronIso() + electron.photonIso() - 0.5*electron.puChargedHadronIso();
    if (electron.neutralHadronIso() > 0)
      iso += electron.neutralHadronIso();
    double rel_iso = iso / electron.et();

    double supercluster_aeta = fabs(electron.superCluster()->eta());

    double dxy = -999;
    if (vertices->size() > 0)
      dxy = electron.gsfTrack()->dxy(vertices->at(0).position());

    if (electron.electronID("mvaTrigV0") > 0 &&
	electron.pt() > 30 && 
	fabs(electron.eta()) < 2.5 &&
	fabs(dxy) < 0.02 &&
	(supercluster_aeta < 1.4442 || supercluster_aeta > 1.5660) &&
	electron.passConversionVeto() &&
	rel_iso < 0.1)
      ++nelectrons;
  }
  
  bool event_selected = 
    jet_ht > 750 &&
    nmuons + nelectrons > 0 && 
    njets > 6;

  if (event_selected) {
    h_nbtags->Fill(nbtags);

    // ...
  }
}

DEFINE_FWK_MODULE(MFVNeutralinoPATBTagCounting);
