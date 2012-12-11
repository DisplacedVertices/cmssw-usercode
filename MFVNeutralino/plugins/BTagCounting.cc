#include "TH1F.h"
#include "TH2F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/BTauReco/interface/JetTag.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectronFwd.h"
#include "DataFormats/EgammaCandidates/interface/Conversion.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrack.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/JetReco/interface/CaloJet.h"
#include "DataFormats/JetReco/interface/CaloJetCollection.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/RecoCandidate/interface/IsoDeposit.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "EGamma/EGammaAnalysisTools/interface/EGammaCutBasedEleId.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

class MFVNeutralinoBTagCounting : public edm::EDAnalyzer {
 public:
  explicit MFVNeutralinoBTagCounting(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::InputTag vertex_src;
  const edm::InputTag muon_src;
  const edm::InputTag electron_src;
  const edm::InputTag btag_src;
  const double jet_pt_min;
  const double bdisc_min;
  
  TH1F* h_ndisc;
  TH1F* h_mu_dxy;
  TH1F* h_mu_dz;
  TH1F* h_el_dxy;
  TH1F* h_el_dz;
  TH1F* h_mu_max_dxy;
  TH1F* h_mu_max_dz;
  TH1F* h_el_max_dxy;
  TH1F* h_el_max_dz;
};

MFVNeutralinoBTagCounting::MFVNeutralinoBTagCounting(const edm::ParameterSet& cfg)
  : vertex_src(cfg.getParameter<edm::InputTag>("vertex_src")),
    muon_src(cfg.getParameter<edm::InputTag>("muon_src")),
    electron_src(cfg.getParameter<edm::InputTag>("electron_src")),
    btag_src(cfg.getParameter<edm::InputTag>("btag_src")),
    jet_pt_min(cfg.getParameter<double>("jet_pt_min")),
    bdisc_min(cfg.getParameter<double>("bdisc_min"))
{
  edm::Service<TFileService> fs;

  h_ndisc = fs->make<TH1F>("h_ndisc", "", 30, 0, 30);
  
  h_mu_dxy = fs->make<TH1F>("h_mu_dxy", "", 1000, -10, 10);
  h_mu_dz  = fs->make<TH1F>("h_mu_dz",  "", 1000, -50, 50);
  h_el_dxy = fs->make<TH1F>("h_el_dxy", "", 1000, -10, 10);
  h_el_dz  = fs->make<TH1F>("h_el_dz",  "", 1000, -50, 50);
  h_mu_max_dxy = fs->make<TH1F>("h_mu_max_dxy", "", 1000, -10, 10);
  h_mu_max_dz  = fs->make<TH1F>("h_mu_max_dz",  "", 1000, -50, 50);
  h_el_max_dxy = fs->make<TH1F>("h_el_max_dxy", "", 1000, -10, 10);
  h_el_max_dz  = fs->make<TH1F>("h_el_max_dz",  "", 1000, -50, 50);
}

void MFVNeutralinoBTagCounting::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  //edm::Handle<reco::CaloJetCollection> jets;
  //event.getByLabel("ak5CaloJets", jets);
  //printf("njets: %i\n", int(jets->size()));
  //for (int i = 0, ie = int(jets->size()); i < ie; ++i)
  //  printf("jet #%i: pt eta phi %f %f %f\n", i, jets->at(i).pt(), jets->at(i).eta(), jets->at(i).phi());

  edm::Handle<reco::VertexCollection> vertices;
  event.getByLabel(vertex_src, vertices);

  edm::Handle<reco::MuonCollection> muons;
  event.getByLabel(muon_src, muons);

  double max_dxy, max_dz;
  bool seen;

  max_dxy = max_dz = 0;
  seen = false;
  for (const auto& muon : *muons) {
    if (!muon.isGlobalMuon())
      continue;
    double rel_iso = (muon.isolationR03().sumPt + muon.isolationR03().emEt + muon.isolationR03().hadEt) / muon.pt();

    double dxy = -999, dz = -999;
    if (vertices->size() > 0) {
      dxy = muon.innerTrack()->dxy(vertices->at(0).position());
      dz  = muon.innerTrack()->dz (vertices->at(0).position());
    }

    if (muon.isGlobalMuon() &&
	muon.pt() > 26 && 
	fabs(muon.eta()) < 2.1 &&
	muon.globalTrack()->normalizedChi2() < 10. &&
	muon.track()->hitPattern().trackerLayersWithMeasurement() > 5 &&
	muon.globalTrack()->hitPattern().numberOfValidMuonHits() > 0 &&
	muon.numberOfMatchedStations() > 1 && 
	rel_iso < 0.12
	) {
      h_mu_dxy->Fill(dxy);
      h_mu_dz ->Fill(dz);

      seen = true;
      if (fabs(dxy) > fabs(max_dxy)) max_dxy = dxy;
      if (fabs(dz ) > fabs(max_dz )) max_dz  = dz;
    }
  }

  if (seen) {
    h_mu_max_dxy->Fill(max_dxy);
    h_mu_max_dz ->Fill(max_dz);
  }
    
  edm::Handle<reco::GsfElectronCollection> electrons;
  event.getByLabel(electron_src, electrons);

  edm::Handle<reco::ConversionCollection> conversions;
  event.getByLabel("allConversions", conversions);

  edm::Handle<edm::ValueMap<double> > iso_deposit_charged, iso_deposit_gamma, iso_deposit_neutral;
  event.getByLabel("elPFIsoValueCharged03PFIdPFIso", iso_deposit_charged);
  event.getByLabel("elPFIsoValueGamma03PFIdPFIso",   iso_deposit_gamma);
  event.getByLabel("elPFIsoValueNeutral03PFIdPFIso", iso_deposit_neutral);

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByLabel("offlineBeamSpot", beamspot);

  edm::Handle<double> rho_iso;
  event.getByLabel("kt6PFJetsForIsolation", "rho", rho_iso);

  int iel = 0;
  max_dxy = max_dz = 0;
  seen = false;
  for (const auto& electron : *electrons) {
    double dxy = -999, dz = -999;
    if (vertices->size() > 0) {
      dxy = electron.gsfTrack()->dxy(vertices->at(0).position());
      dz  = electron.gsfTrack()->dz (vertices->at(0).position());
    }

    const reco::GsfElectronRef ele_ref(electrons, iel);
    double iso_ch = (*iso_deposit_charged)[ele_ref];
    double iso_em = (*iso_deposit_gamma  )[ele_ref];
    double iso_nh = (*iso_deposit_neutral)[ele_ref];

    double supercluster_aeta = fabs(electron.superCluster()->eta());

    unsigned mask = EgammaCutBasedEleId::TestWP(EgammaCutBasedEleId::LOOSE,  ele_ref, conversions, *beamspot, vertices, iso_ch, iso_em, iso_nh, *rho_iso);
    unsigned cuts = EgammaCutBasedEleId::DETAIN | EgammaCutBasedEleId::DPHIIN | EgammaCutBasedEleId::SIGMAIETAIETA | EgammaCutBasedEleId::HOE | EgammaCutBasedEleId::OOEMOOP | EgammaCutBasedEleId::ISO | EgammaCutBasedEleId::VTXFIT | EgammaCutBasedEleId::MHITS;
    bool pass_id = (mask & cuts) == cuts;
    if (pass_id && 
	electron.pt() > 30 && 
	fabs(electron.eta()) < 2.5 &&
	(supercluster_aeta < 1.4442 || supercluster_aeta > 1.5660)
	) {
      h_el_dxy->Fill(dxy);
      h_el_dz ->Fill(dz);

      seen = true;
      if (fabs(dxy) > fabs(max_dxy)) max_dxy = dxy;
      if (fabs(dz ) > fabs(max_dz )) max_dz  = dz;
    }

    ++iel;
  }

  if (seen) {
    h_el_max_dxy->Fill(max_dxy);
    h_el_max_dz ->Fill(max_dz);
  }

  edm::Handle<reco::JetTagCollection> btags;
  event.getByLabel(btag_src, btags);

  int ndisc = 0;

  //std::cout << btag_src << "\n";
  for (int i = 0, ie = btags->size(); i < ie; ++i) {
    //std::cout << "#" << i << ": pt eta phi: " << (*btags)[i].first->pt() << ", "<< (*btags)[i].first->eta() << ", "<< (*btags)[i].first->phi() << " bdisc: " << (*btags)[i].second << "\n";
    if ((*btags)[i].first->pt() > jet_pt_min && (*btags)[i].second > bdisc_min)
      ++ndisc;
  }

  h_ndisc->Fill(ndisc);
}

DEFINE_FWK_MODULE(MFVNeutralinoBTagCounting);
