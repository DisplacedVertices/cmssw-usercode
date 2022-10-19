#include "TH1F.h"
#include "TH2F.h"
#include "DataFormats/Math/interface/Point3D.h"
#include "DataFormats/Math/interface/PtEtaPhiMass.h"
#include "TLorentzVector.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "SimGeneral/HepPDTRecord/interface/ParticleDataTable.h"
#include "JMTucker/MFVNeutralinoFormats/interface/MCInteractions.h"
#include "JMTucker/Tools/interface/BasicKinematicHists.h"
#include "JMTucker/Tools/interface/GenUtilities.h"
#include "JMTucker/Tools/interface/Utilities.h"

class MFVGenHistos : public edm::EDAnalyzer {
public:
  explicit MFVGenHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

private:
  const edm::EDGetTokenT<reco::GenParticleCollection> gen_token;
  const edm::EDGetTokenT<reco::GenJetCollection> gen_jet_token;
  const edm::EDGetTokenT<std::vector<double>> gen_vertex_token;
  const edm::EDGetTokenT<mfv::MCInteraction> mci_token;
  bool mci_warned;

  bool isBhadron(int pdgID);
  bool isKaon(int pdgID);
  bool isChadron(int pdgID);
  bool isBquark(int pdgID);
  bool isValidLeptonic(const reco::GenParticle* parent, int pdgID);
  bool isBvtx(const reco::GenParticle* parent, int pdgID, double dist3d, std::vector<int> vec_pdgID);
  size_t mindR_dau(int &nth_chain, const reco::GenParticle* parent, std::vector<double>& vec_first_dR, std::vector<double>& vec_second_dR, std::vector<size_t>& excl_idx_first_dRmin, std::vector<size_t>& excl_idx_second_dRmin);
  bool Is_bdecay_done(int &nth_chain, const reco::GenParticle* bquark, const reco::GenParticle* parent, std::vector<const reco::GenParticle*>& vec_gen_particle, std::vector<const reco::GenParticle*>& vec_bhad_gen_particle, std::vector<int>& vec_pdgID, std::vector<double>& vec_first_dR, std::vector<double>& vec_second_dR, std::vector<double>& vec_decay, std::vector<size_t>& excl_idx_first_dRmin, std::vector<size_t>& excl_idx_second_dRmin);
 
  edm::ESHandle<ParticleDataTable> pdt;

  TH1F* h_valid;

  TH1F* NumLeptons;
  TH2F* DecayType;

  BasicKinematicHistsFactory* bkh_factory;

  BasicKinematicHists* Hs[2];
  BasicKinematicHists* Qs[2][2];

  BasicKinematicHists* Lsps[2];
  BasicKinematicHists* Stranges[2];
  BasicKinematicHists* Bottoms[2];
  BasicKinematicHists* Tops[2];
  BasicKinematicHists* Ws[2];
  BasicKinematicHists* BottomsFromTops[2];
  BasicKinematicHists* WDaughters[2][2];
  BasicKinematicHists* Muons;
  BasicKinematicHists* Electrons;
  BasicKinematicHists* Taus;
  BasicKinematicHists* LightLeptons;
  BasicKinematicHists* Leptons;

  BasicKinematicHists* Ups[2];
  BasicKinematicHists* Downs[2];

  TH1F* h_lsp_dist2d;
  TH1F* h_lsp_dist3d;
  TH1F* h_lsp_angle2;
  TH1F* h_lsp_angle3;

  TH2F* h_vtx[5];
  TH1F* h_r2d[5];
  TH1F* h_r3d[5];
  TH1F* h_ctau;
  TH1F* h_ctaubig;
  TH2F* h_r3d_bhadron_v_bquark;
  TH1F* h_lspbeta;
  TH1F* h_lspbetagamma;
  TH1F* h_max_deta;
  TH1F* h_min_deta;
  TH1F* h_max_dphi;
  TH1F* h_min_dphi;
  TH1F* h_max_dR;
  TH1F* h_min_dR;
  TH2F* h_max_dR_vs_lspbeta;
  TH2F* h_min_dR_vs_lspbeta;
  TH2F* h_max_dR_vs_lspbetagamma;
  TH2F* h_min_dR_vs_lspbetagamma;
  TH1F* h_neutralino_daughters_pt;
  TH1F* h_llp_daughters_pt;
  TH1F* h_neutralino_daughters_eta;
  TH1F* h_llp_daughters_eta;
  TH1F* h_neutralino_daughters_dxy;
  TH2F* h_neutralino_daughters_dxy_dBV;
  TH1F* h_llp_daughters_phi;
  TH1F* h_llp_daughters_mass;
  TH1F* h_lsp_max_dR;
  TH1F* h_lsp_min_dR;
  TH1F* h_neutralino_daughters_jets_dR;
  TH1F* h_neutralino_daughters_jets_nmatch;
  TH1F* h_lsp_ntracks;

  TH1F* h_status1origins;

  TH2F* h_nbhadronsvsbquarks;
  TH2F* h_nbhadronsvsbquarks_wcuts;
  TH1F* h_nbquarks;
  TH1F* h_bquarks_pt;
  TH1F* h_bquarks_eta;
  TH1F* h_bquarks_phi;
  TH1F* h_bquarks_energy;

  TH1F* h_bquarks_absdphi;
  TH1F* h_bquarks_dphi;
  TH1F* h_bquarks_deta;
  TH2F* h_bquarks_deta_dphi;
  TH1F* h_bquarks_avgeta;
  TH2F* h_bquarks_avgeta_dphi;
  TH1F* h_bquarks_dR;
  TH2F* h_bquarks_dR_dphi;

  TH1I* h_n_gen_bvtx;	// # of b-vertices per event
  TH1F* h_dau_to_gdau_mindR;   // a set of four minimum dR saved within the recursive function at the chain of b-quark to daus 
  TH1F* h_gdau_to_ggdau_mindR;	// a set of four minimum dR saved within the recursive function at the chain of b-quark's daus to gdaus
  TH1F* h_dau_select_edge_b_decay_dist3d_from_llp; //  b-vtx (from b hadrons) decay lengths 
  TH1F* h_dau_select_b_decay_dist3d_from_llp;  	// b-vtx (from non-b hadrons) decay lengths 
  TH1F* h_dau_select_b_had_dist3d_from_llp;  	// b-hadron's decay length
  TH1F* h_dau_select_b_had_diff_pT_b_quark;  	// difference in pT between b-hadron and b-quark
  TH1F* h_dau_select_b_had_ctau;  	// b-hadron's gammabeta
  TH1I* h_dau_select_b_had_pdgid;  	// b-hadron's pdgid
  TH1I* h_dau_select_nonb_had_pdgid;  	// non-b hadron's pdgid
  TH1F* h_dau_select_b_had_gammabeta;  	// b-hadron's gammabeta
  TH1F* h_dau_select_b_had_pT;  	// b-hadron's pT
  TH1F* h_dau_select_b_decay_dR_by_vec_nonb_had_to_b_had; // dR between non-b hadrons and its b-hadron
  TH1F* h_dau_select_b_decay_dphi_by_vec_nonb_had_to_b_had;	  // dphi between non-b hadrons and its b-hadron
  TH1F* h_dau_select_b_had_absdphi_by_vec_two_b_had_per_llp;	  // |dphi| between two b hadrons per llp 
  TH1F* h_dau_select_b_had_absdphi_by_vec_its_llp;	  // |dphi| between a b hadron and its llp
  TH1F* h_dau_select_b_quark_absdphi_by_vec_its_llp;   // |dphi| between a b-quark and its llp
  TH1F* h_dau_select_b_had_absdphi_by_vec_its_b_quark;	 // |dphi| between a b hadron and its b-quark
  TH1F* h_dau_select_b_decay_absdphi_by_vec_two_nonb_had_per_llp;	  // |dphi| between two non-b hadrons per llp
  TH1F* h_dau_select_b_decay_absdphi_by_pt_two_nonb_had_per_llp;	  // |dphi| between two non-b hadrons per llp by decay points
  TH1F* h_dau_select_b_decay_absdeta_by_pt_two_nonb_had_per_llp;	  // |deta| between two non-b hadrons per llp by decay points


  TH1F* h_npartons_in_acc;

  TH1F* h_npartons_60;
  TH1F* h_njets_60;
  TH1F* h_njets_40;
  TH1F* h_njets_30;
  TH1F* h_njets_20;
  TH1F* h_ht;
  TH1F* h_ht40;

  TH1F* NJets;
  BasicKinematicHists* Jets;
  TH1F* JetAuxE;
  TH1F* JetEmE;
  TH1F* JetHadE;
  TH1F* JetInvE;
  TH1F* JetNConstituents;
  TH1F* JetNChargedConst;
  TH1F* JetFChargedConst;
  TH2F* JetNtracksPt;
  TH2F* JetNtracksptgt3Pt;

  TH1F* JetIds;

  TH1F* NBJets;
  BasicKinematicHists* BJets;
  TH1F* BJetAuxE;
  TH1F* BJetEmE;
  TH1F* BJetHadE;
  TH1F* BJetInvE;
  TH1F* BJetNConstituents;
  TH1F* BJetNChargedConst;
  TH1F* BJetFChargedConst;
};

MFVGenHistos::MFVGenHistos(const edm::ParameterSet& cfg)
  : gen_token(consumes<reco::GenParticleCollection>(cfg.getParameter<edm::InputTag>("gen_src"))),
    gen_jet_token(consumes<reco::GenJetCollection>(cfg.getParameter<edm::InputTag>("gen_jet_src"))),
    gen_vertex_token(consumes<std::vector<double>>(cfg.getParameter<edm::InputTag>("gen_vertex_src"))),
    mci_token(consumes<mfv::MCInteraction>(cfg.getParameter<edm::InputTag>("mci_src"))),

    mci_warned(false)
{
  edm::Service<TFileService> fs;

  h_valid = fs->make<TH1F>("h_valid", "", 2, 0, 2);

  NumLeptons = fs->make<TH1F>("NumLeptons", "", 3, 0, 3);
  NumLeptons->SetTitle(";number of leptons from top decays;events");
  DecayType = fs->make<TH2F>("DecayType", "", 6, 0, 6, 6, 0, 6);
  DecayType->SetTitle(";decay mode 0;decay mode 1");

  bkh_factory = new BasicKinematicHistsFactory(fs);

  for (int i = 0; i < 2; ++i) {
    Hs[i] = bkh_factory->make(TString::Format("Hs#%i", i), TString::Format("H #%i", i));
    Hs[i]->BookE (300, 0, 6000, "20");
    Hs[i]->BookP (300, 0, 6000, "20");
    Hs[i]->BookPt(300, 0, 6000, "20");
    Hs[i]->BookPz(300, 0, 6000, "20");
    Hs[i]->BookM (300, 0, 6000, "20");
    Hs[i]->BookRapEta(200, "0.1");
    Hs[i]->BookPhi(50, "0.125");

    for (int j = 0; j < 2; ++j) {
      Qs[i][j] = bkh_factory->make(TString::Format("Qs#%i#%i", i,j), TString::Format("H#%i daughter #%i", i, j));
      Qs[i][j]->BookE (200, 0, 2000, "10");
      Qs[i][j]->BookP (200, 0, 2000, "10");
      Qs[i][j]->BookPt(200, 0, 2000, "10");
      Qs[i][j]->BookPz(200, 0, 2000, "10");
      Qs[i][j]->BookM (200, 0, 2000, "10");
      Qs[i][j]->BookRapEta(200, "0.1");
      Qs[i][j]->BookPhi(50, "0.125");
      Qs[i][j]->BookDxy(200, -2, 2, "0.02");
      Qs[i][j]->BookDz (200, -2, 2, "0.02");
      Qs[i][j]->BookQ();
    }

    Lsps[i] = bkh_factory->make(TString::Format("Lsps#%i", i), TString::Format("lsp #%i", i));
    Lsps[i]->BookE (300, 0, 6000, "20");
    Lsps[i]->BookP (300, 0, 6000, "20");
    Lsps[i]->BookPt(300, 0, 6000, "20");
    Lsps[i]->BookPz(300, 0, 6000, "20");
    Lsps[i]->BookM (300, 0, 6000, "20");
    Lsps[i]->BookRapEta(200, "0.1");
    Lsps[i]->BookPhi(50, "0.125");

    Stranges[i] = bkh_factory->make(TString::Format("Stranges#%i", i), TString::Format("strange #%i", i));
    Stranges[i]->BookE (200, 0, 2000, "10");
    Stranges[i]->BookP (200, 0, 2000, "10");
    Stranges[i]->BookPt(200, 0, 2000, "10");
    Stranges[i]->BookM (200, 0, 2000, "10");
    Stranges[i]->BookRapEta(200, "0.1");
    Stranges[i]->BookPhi(50, "0.125");
    Stranges[i]->BookDxy(200, -2, 2, "0.02");
    Stranges[i]->BookDz (200, -2, 2, "0.02");
    Stranges[i]->BookQ();

    Ups[i] = bkh_factory->make(TString::Format("Ups#%i", i), TString::Format("up #%i", i));
    Ups[i]->BookE (200, 0, 2000, "10");
    Ups[i]->BookP (200, 0, 2000, "10");
    Ups[i]->BookPt(200, 0, 2000, "10");
    Ups[i]->BookM (200, 0, 2000, "10");
    Ups[i]->BookRapEta(200, "0.1");
    Ups[i]->BookPhi(50, "0.125");
    Ups[i]->BookDxy(200, -2, 2, "0.02");
    Ups[i]->BookDz (200, -2, 2, "0.02");
    Ups[i]->BookQ();

    Downs[i] = bkh_factory->make(TString::Format("Downs#%i", i), TString::Format("down #%i", i));
    Downs[i]->BookE (200, 0, 2000, "10");
    Downs[i]->BookP (200, 0, 2000, "10");
    Downs[i]->BookPt(200, 0, 2000, "10");
    Downs[i]->BookM (200, 0, 2000, "10");
    Downs[i]->BookRapEta(200, "0.1");
    Downs[i]->BookPhi(50, "0.125");
    Downs[i]->BookDxy(200, -2, 2, "0.02");
    Downs[i]->BookDz (200, -2, 2, "0.02");
    Downs[i]->BookQ();

    Bottoms[i] = bkh_factory->make(TString::Format("Bottoms#%i", i), TString::Format("bottom #%i", i));
    Bottoms[i]->BookE (200, 0, 2000, "10");
    Bottoms[i]->BookP (200, 0, 2000, "10");
    Bottoms[i]->BookPt(200, 0, 2000, "10");
    Bottoms[i]->BookPz(200, 0, 2000, "10");
    Bottoms[i]->BookM (200, 0, 2000, "10");
    Bottoms[i]->BookRapEta(200, "0.1");
    Bottoms[i]->BookPhi(50, "0.125");
    Bottoms[i]->BookDxy(200, -2, 2, "0.02");
    Bottoms[i]->BookDz (200, -2, 2, "0.02");
    Bottoms[i]->BookQ();
    
    Tops[i] = bkh_factory->make(TString::Format("Tops#%i", i), TString::Format("top #%i", i));
    Tops[i]->BookE (200, 0, 2000, "10");
    Tops[i]->BookP (200, 0, 2000, "10");
    Tops[i]->BookPt(200, 0, 2000, "10");
    Tops[i]->BookPz(200, 0, 2000, "10");
    Tops[i]->BookM (200, 0, 2000, "10");
    Tops[i]->BookRapEta(200, "0.1");
    Tops[i]->BookPhi(50, "0.125");
    Tops[i]->BookDxy(200, -2, 2, "0.02");
    Tops[i]->BookDz (200, -2, 2, "0.02");
    Tops[i]->BookQ();
    
    Ws[i] = bkh_factory->make(TString::Format("Ws#%i", i), TString::Format("w #%i", i));
    Ws[i]->BookE (200, 0, 2000, "10");
    Ws[i]->BookP (200, 0, 2000, "10");
    Ws[i]->BookPt(200, 0, 2000, "10");
    Ws[i]->BookPz(200, 0, 2000, "10");
    Ws[i]->BookM (200, 0, 2000, "10");
    Ws[i]->BookRapEta(200, "0.1");
    Ws[i]->BookPhi(50, "0.125");
    Ws[i]->BookDxy(200, -2, 2, "0.02");
    Ws[i]->BookDz (200, -2, 2, "0.02");
    Ws[i]->BookQ();

    BottomsFromTops[i] = bkh_factory->make(TString::Format("BottomsFromTops#%i", i), TString::Format("bottom from top #%i", i));
    BottomsFromTops[i]->BookE (200, 0, 2000, "10");
    BottomsFromTops[i]->BookP (200, 0, 2000, "10");
    BottomsFromTops[i]->BookPt(200, 0, 2000, "10");
    BottomsFromTops[i]->BookPz(200, 0, 2000, "10");
    BottomsFromTops[i]->BookM (200, 0, 2000, "10");
    BottomsFromTops[i]->BookRapEta(200, "0.1");
    BottomsFromTops[i]->BookPhi(50, "0.125");
    BottomsFromTops[i]->BookDxy(200, -2, 2, "0.02");
    BottomsFromTops[i]->BookDz (200, -2, 2, "0.02");
    BottomsFromTops[i]->BookQ();

    for (int j = 0; j < 2; ++j) {
      WDaughters[i][j] = bkh_factory->make(TString::Format("WDaughters#%i#%i", i,j), TString::Format("W#%i daughter #%i", i, j));
      WDaughters[i][j]->BookE (200, 0, 2000, "10");
      WDaughters[i][j]->BookP (200, 0, 2000, "10");
      WDaughters[i][j]->BookPt(200, 0, 2000, "10");
      WDaughters[i][j]->BookPz(200, 0, 2000, "10");
      WDaughters[i][j]->BookM (200, 0, 2000, "10");
      WDaughters[i][j]->BookRapEta(200, "0.1");
      WDaughters[i][j]->BookPhi(50, "0.125");
      WDaughters[i][j]->BookDxy(200, -2, 2, "0.02");
      WDaughters[i][j]->BookDz (200, -2, 2, "0.02");
      WDaughters[i][j]->BookQ();
    }
  }

  Electrons = bkh_factory->make("Electrons", "electrons");
  Electrons->BookE (200, 0, 2000, "10");
  Electrons->BookP (200, 0, 2000, "10");
  Electrons->BookPt(200, 0, 2000, "10");
  Electrons->BookPz(200, 0, 2000, "10");
  Electrons->BookM (200, 0, 2000, "10");
  Electrons->BookRapEta(200, "0.1");
  Electrons->BookPhi(50, "0.125");
  Electrons->BookDxy(200, -2, 2, "0.02");
  Electrons->BookDz (200, -2, 2, "0.02");
  Electrons->BookQ();

  Muons = bkh_factory->make("Muons", "muons");
  Muons->BookE (200, 0, 2000, "10");
  Muons->BookP (200, 0, 2000, "10");
  Muons->BookPt(200, 0, 2000, "10");
  Muons->BookPz(200, 0, 2000, "10");
  Muons->BookM (200, 0, 2000, "10");
  Muons->BookRapEta(200, "0.1");
  Muons->BookPhi(50, "0.125");
  Muons->BookDxy(200, -2, 2, "0.02");
  Muons->BookDz (200, -2, 2, "0.02");
  Muons->BookQ();

  Taus = bkh_factory->make("Taus", "taus");
  Taus->BookE (200, 0, 2000, "10");
  Taus->BookP (200, 0, 2000, "10");
  Taus->BookPt(200, 0, 2000, "10");
  Taus->BookPz(200, 0, 2000, "10");
  Taus->BookM (200, 0, 2000, "10");
  Taus->BookRapEta(200, "0.1");
  Taus->BookPhi(50, "0.125");
  Taus->BookDxy(200, -2, 2, "0.02");
  Taus->BookDz (200, -2, 2, "0.02");
  Taus->BookQ();

  LightLeptons= bkh_factory->make("LightLeptons", "light leptons");
  LightLeptons->BookE (200, 0, 2000, "10");
  LightLeptons->BookP (200, 0, 2000, "10");
  LightLeptons->BookPt(200, 0, 2000, "10");
  LightLeptons->BookPz(200, 0, 2000, "10");
  LightLeptons->BookM (200, 0, 2000, "10");
  LightLeptons->BookRapEta(200, "0.1");
  LightLeptons->BookPhi(50, "0.125");
  LightLeptons->BookDxy(200, -2, 2, "0.02");
  LightLeptons->BookDz (200, -2, 2, "0.02");
  LightLeptons->BookQ();

  Leptons = bkh_factory->make("Leptons", "leptons");
  Leptons->BookE (200, 0, 2000, "10");
  Leptons->BookP (200, 0, 2000, "10");
  Leptons->BookPt(200, 0, 2000, "10");
  Leptons->BookPz(200, 0, 2000, "10");
  Leptons->BookM (200, 0, 2000, "10");
  Leptons->BookRapEta(200, "0.1");
  Leptons->BookPhi(50, "0.125");
  Leptons->BookDxy(200, -2, 2, "0.02");
  Leptons->BookDz (200, -2, 2, "0.02");
  Leptons->BookQ();

  h_lsp_dist2d = fs->make<TH1F>("h_lsp_dist2d", ";2D distance between LSP decay positions (cm);Events/0.0025 cm", 500, 0, 1);
  h_lsp_dist3d = fs->make<TH1F>("h_lsp_dist3d", ";3D distance between LSP decay positions (cm);Events/0.0025 cm", 500, 0, 1);

  h_lsp_angle2 = fs->make<TH1F>("h_lsp_angle2", ";cos(angle in r-#phi plane) between LSP momenta;Events/0.01", 202, -1.01, 1.01);
  h_lsp_angle3 = fs->make<TH1F>("h_lsp_angle3", ";cos(3D angle) between LSP momenta;Events/0.01", 202, -1.01, 1.01);

  const char* names[9] = {"lsp", "strange", "bottom", "bhadron", "from21", "from22", "fromq", "from21only", "from22only"};
  for (int i = 0; i < 5; ++i) {
    h_vtx[i] = fs->make<TH2F>(TString::Format("h_vtx_%s", names[i]), TString::Format(";%s vx (cm); %s vy (cm)", names[i], names[i]), 200, -1, 1, 200, -1, 1);
    h_r2d[i] = fs->make<TH1F>(TString::Format("h_r2d_%s", names[i]), TString::Format(";%s 2D distance (cm);Events/0.01 cm", names[i]), 500, 0, 5);
    h_r3d[i] = fs->make<TH1F>(TString::Format("h_r3d_%s", names[i]), TString::Format(";%s 3D distance (cm);Events/0.01 cm", names[i]), 500, 0, 5);
  }

  h_ctau = fs->make<TH1F>("h_ctau", ";c#tau to LSP decay (cm);Events/50 #mum", 200, 0, 1);
  h_ctaubig = fs->make<TH1F>("h_ctaubig", ";c#tau to LSP decay (cm);Events/500 #mum", 200, 0, 10);
  h_r3d_bhadron_v_bquark = fs->make<TH2F>("h_r3d_bhadron_v_bquark", ";b quark 3D distance (cm);b hadron 3D distance (cm)", 100, 0, 2, 100, 0, 2);
  h_lspbeta = fs->make<TH1F>("h_lspbeta", ";LSP #beta;Events/0.01", 100, 0, 1);
  h_lspbetagamma = fs->make<TH1F>("h_lspbetagamma", ";LSP #beta#gamma;Events/0.1", 100, 0, 10);

  h_max_dphi = fs->make<TH1F>("h_max_dphi", ";max |#Delta#phi| between partons;Events/0.05", 100, 0, 5);
  h_min_dphi = fs->make<TH1F>("h_min_dphi", ";min |#Delta#phi| between partons;Events/0.05", 100, 0, 5);
  h_max_deta = fs->make<TH1F>("h_max_deta", ";max |#Delta#eta| between partons;Events/0.05", 100, 0, 5);
  h_min_deta = fs->make<TH1F>("h_min_deta", ";min |#Delta#eta| between partons;Events/0.05", 100, 0, 5);
  h_max_dR = fs->make<TH1F>("h_max_dR", ";max #DeltaR between partons;Events/0.05", 100, 0, 5);
  h_min_dR = fs->make<TH1F>("h_min_dR", ";min #DeltaR between partons;Events/0.05", 100, 0, 5);
  h_max_dR_vs_lspbeta = fs->make<TH2F>("h_max_dR_vs_lspbeta", ";LSP #beta;max #DeltaR between partons", 100, 0, 1, 100, 0, 5);
  h_min_dR_vs_lspbeta = fs->make<TH2F>("h_min_dR_vs_lspbeta", ";LSP #beta;min #DeltaR between partons", 100, 0, 1, 100, 0, 5);
  h_max_dR_vs_lspbetagamma = fs->make<TH2F>("h_max_dR_vs_lspbetagamma", ";LSP #beta#gamma;max #DeltaR between partons", 100, 0, 10, 100, 0, 5);
  h_min_dR_vs_lspbetagamma = fs->make<TH2F>("h_min_dR_vs_lspbetagamma", ";LSP #beta#gamma;min #DeltaR between partons", 100, 0, 10, 100, 0, 5);
  h_neutralino_daughters_pt = fs->make<TH1F>("h_neutralino_daughters_pt", ";p_{T} of partons (GeV);LSP daughter partons/1 GeV", 100, 0, 500);
  h_llp_daughters_pt = fs->make<TH1F>("h_llp_daughters_pt", ";p_{T} of partons (GeV);fraction of LLP daughter partons", 100, 0, 500);
  h_neutralino_daughters_eta = fs->make<TH1F>("h_neutralino_daughters_eta", ";#eta of partons;LSP daughter partons/0.16", 50, -4, 4);
  h_llp_daughters_eta = fs->make<TH1F>("h_llp_daughters_eta", ";#eta of partons;fraction of LLP daughter partons", 50, -4, 4);
  h_neutralino_daughters_dxy = fs->make<TH1F>("h_neutralino_daughters_dxy", ";dxy of partons;LSP daughter partons/10 #mum", 400, -0.2, 0.2);
  h_neutralino_daughters_dxy_dBV = fs->make<TH2F>("h_neutralino_daughters_dxy_dBV", ";LSP 2D distance;dxy of partons", 500, 0, 5, 400, -0.2, 0.2);
  h_llp_daughters_phi = fs->make<TH1F>("h_llp_daughters_phi", ";#phi of partons;fraction of LLP daughter partons", 50, -4, 4);
  h_llp_daughters_mass = fs->make<TH1F>("h_llp_daughters_mass", ";#mass of partons;fraction of LLP daughter partons", 50, 0, 100);
  h_lsp_max_dR = fs->make<TH1F>("h_lsp_max_dR", ";max #DeltaR between partons;Events/0.05", 100, 0, 5);
  h_lsp_min_dR = fs->make<TH1F>("h_lsp_min_dR", ";min #DeltaR between partons;Events/0.05", 100, 0, 5);
  h_neutralino_daughters_jets_dR = fs->make<TH1F>("h_neutralino_daughters_jets_dR", ";#DeltaR between partons and jets;parton-jet pairs/0.05", 100, 0, 5);
  h_neutralino_daughters_jets_nmatch = fs->make<TH1F>("h_neutralino_daughters_jets_nmatch", ";number of genJets w/ #DeltaR < 0.4;LSP daughter partons", 10, 0, 10);
  h_lsp_ntracks = fs->make<TH1F>("h_lsp_ntracks", ";total number of constituents in genJets w/ #DeltaR < 0.4;LSPs", 300, 0, 300);

  h_status1origins = fs->make<TH1F>("status1origins", "", 8, 0, 8);
  TAxis* xax = h_status1origins->GetXaxis();
  xax->SetBinLabel(1, "nowhere");
  xax->SetBinLabel(2, "q only");
  xax->SetBinLabel(3, "22 only");
  xax->SetBinLabel(4, "q & 22");
  xax->SetBinLabel(5, "21 only");
  xax->SetBinLabel(6, "21 & q");
  xax->SetBinLabel(7, "21 & 22");
  xax->SetBinLabel(8, "21 & 22 & q");

  h_nbhadronsvsbquarks = fs->make<TH2F>("h_nbhadronsvsbquarks", ";number of b quarks;number of b hadrons", 20, 0, 20, 20, 0, 20);
  h_nbhadronsvsbquarks_wcuts = fs->make<TH2F>("h_nbhadronsvsbquarks_wcuts", "", 20, 0, 20, 20, 0, 20);
  h_nbquarks = fs->make<TH1F>("h_nbquarks", ";number of b quarks;Events", 20, 0, 20);
  h_bquarks_pt = fs->make<TH1F>("h_bquarks_pt", ";b quarks p_{T} (GeV);arb. units", 100, 0, 500);
  h_bquarks_eta = fs->make<TH1F>("h_bquarks_eta", ";b quarks #eta;arb. units", 50, -4, 4);
  h_bquarks_phi = fs->make<TH1F>("h_bquarks_phi", ";b quarks #phi;arb. units", 50, -3.15, 3.15);
  h_bquarks_energy = fs->make<TH1F>("h_bquarks_energy", ";b quarks energy (GeV);arb. units", 200, 0, 2000);

  h_bquarks_absdphi = fs->make<TH1F>("h_bquarks_absdphi", "events with two bquarks;|#Delta#phi|;Events/0.126", 25, 0, 3.15);
  h_bquarks_dphi = fs->make<TH1F>("h_bquarks_dphi", "events with two bquarks;#Delta#phi;Events/0.126", 50, -3.15, 3.15);
  h_bquarks_deta = fs->make<TH1F>("h_bquarks_deta", "events with two bquarks;#Delta#eta;Events/0.16", 50, -4, 4);
  h_bquarks_deta_dphi = fs->make<TH2F>("h_bquarks_deta_dphi", "events with two bquarks;#Delta#phi;#Delta#eta", 50, -3.15, 3.15, 50, -4, 4);
  h_bquarks_avgeta = fs->make<TH1F>("h_bquarks_avgeta", "events with two bquarks;avg #eta;Events/0.16", 50, -4, 4);
  h_bquarks_avgeta_dphi = fs->make<TH2F>("h_bquarks_avgeta_dphi", "events with two bquarks;#Delta#phi;avg #eta", 50, -3.15, 3.15, 50, -4, 4);
  h_bquarks_dR = fs->make<TH1F>("h_bquarks_dR", "events with two bquarks;#Delta R;Events/0.14", 50, 0, 7);
  h_bquarks_dR_dphi = fs->make<TH2F>("h_bquarks_dR_dphi", "events with two bquarks;#Delta#phi;#Delta R", 50, -3.15, 3.15, 50, 0, 7);

  h_n_gen_bvtx = fs->make<TH1I>("h_n_gen_bvtx", ";# of GEN b-vertices (from non-b hadrons); events/1", 40, 0, 40);
  h_dau_to_gdau_mindR = fs->make<TH1F>("h_dau_to_gdau_mindR", ";minimum dR of a b-had and its daughter; arb. units", 140, 0, 2.0);
  h_gdau_to_ggdau_mindR = fs->make<TH1F>("h_gdau_to_ggdau_mindR", ";minimum dR of b-had's daughter and its granddaughter; arb. units", 140, 0, 2.0);
  h_dau_select_edge_b_decay_dist3d_from_llp = fs->make<TH1F>("h_dau_select_edge_b_decay_dist3d_from_llp", "multiple dau stage w.r.t LLP (final product still a b-hadron); displaced b-had vtx from an LLP decay position (cm);b-vtx/0.01 cm", 100, 0, 1);
  h_dau_select_b_decay_dist3d_from_llp = fs->make<TH1F>("h_dau_select_b_decay_dist3d_from_llp", "; displaced b-had vtx from an LLP decay position (cm);b-vtx/0.01 cm", 400, 0, 4.0);
  h_dau_select_b_had_dist3d_from_llp = fs->make<TH1F>("h_dau_select_b_had_dist3d_from_llp", "; b-hadron position from an LLP decay position (cm);b-hadron/0.01 cm", 100, 0, 1);
  h_dau_select_b_had_diff_pT_b_quark = fs->make<TH1F>("h_dau_select_b_had_diff_pT_b_quark", "; p_{T} b-hadron - p_{T} b-quark (GeV) ;b-hadron/1 GeV", 100, -50, 50);
  h_dau_select_b_had_gammabeta = fs->make<TH1F>("h_dau_select_b_had_gammabeta", "; b-hadron #beta#gamma; 4 x events / 1", 100, 0, 100);
  h_dau_select_b_had_ctau = fs->make<TH1F>("h_dau_select_b_had_ctau", "; b-hadron's ctau (cm);b-hadron/0.01 cm", 100, 0, 1);
  h_dau_select_b_had_pdgid = fs->make<TH1I>("h_dau_select_b_had_pdgid", "; b-hadron's pdg ID ;b-hadron/1", 120000, -6000, 6000);
  h_dau_select_nonb_had_pdgid = fs->make<TH1I>("h_dau_select_nonb_had_pdgid", "; non-b hadron's pdg ID ;non-b hadron/1", 120000, -6000, 6000);
  h_dau_select_b_had_pT = fs->make<TH1F>("h_dau_select_b_had_pT", "; b-hadron pT; 4 x events / 5 GeV", 100, 0, 500);
  h_dau_select_b_decay_dR_by_vec_nonb_had_to_b_had = fs->make<TH1F>("h_dau_select_b_decay_dR_by_vec_nonb_had_to_b_had", ";#Delta R between a non-b hadron and b-had; arb. units", 140, 0, 7.0);
  h_dau_select_b_decay_dphi_by_vec_nonb_had_to_b_had = fs->make<TH1F>("h_dau_select_b_decay_dphi_by_vec_nonb_had_to_b_had", ";#phi a non-b hadron - #phi b-had; arb. units", 50, -3.15, 3.15);
  h_dau_select_b_had_absdphi_by_vec_two_b_had_per_llp = fs->make<TH1F>("h_dau_select_b_had_absdphi_by_vec_two_b_had_per_llp", ";|#Delta #phi| of a pair of b hadrons; arb. units", 100, 0, 3.15);
  h_dau_select_b_had_absdphi_by_vec_its_llp = fs->make<TH1F>(" h_dau_select_b_had_absdphi_by_vec_its_llp", ";|#Delta #phi| of b-had and its LLP; arb. units", 100, 0, 3.15);
  h_dau_select_b_quark_absdphi_by_vec_its_llp = fs->make<TH1F>(" h_dau_select_b_quark_absdphi_by_vec_its_llp", ";|#Delta #phi| of b-quark and its LLP; arb. units", 100, 0, 3.15);
  h_dau_select_b_had_absdphi_by_vec_its_b_quark = fs->make<TH1F>(" h_dau_select_b_had_absdphi_by_vec_its_b_quark", ";|#Delta #phi| of b-had and its b-quark; arb. units", 100, 0, 3.15);
  h_dau_select_b_decay_absdphi_by_vec_two_nonb_had_per_llp = fs->make<TH1F>("h_dau_select_b_decay_absdphi_by_vec_two_nonb_had_per_llp", ";|#Delta #phi| of a pair of non-b hadrons; arb. units", 100, 0, 3.15);
  h_dau_select_b_decay_absdphi_by_pt_two_nonb_had_per_llp = fs->make<TH1F>("h_dau_select_b_decay_absdphi_by_pt_two_nonb_had_per_llp", ";|#Delta #phi| of vertices by a pair of non-b hadrons; arb. units", 100, 0, 3.15);
  h_dau_select_b_decay_absdeta_by_pt_two_nonb_had_per_llp = fs->make<TH1F>("h_dau_select_b_decay_absdeta_by_pt_two_nonb_had_per_llp", ";|#Delta #eta| of vertices by a pair of non-b hadrons; arb. units", 100, 0, 3.15);

  
  h_npartons_in_acc = fs->make<TH1F>("h_npartons_in_acc", ";number of LSP daughters in acceptance;Events", 40, 0, 40);
  h_npartons_60 = fs->make<TH1F>("h_npartons_60", ";number of partons with E_{T} > 60 GeV;Events", 40, 0, 40);
  h_njets_60 = fs->make<TH1F>("h_njets_60", ";number of jets with E_{T} > 60 GeV;Events", 20, 0, 20);
  h_njets_40 = fs->make<TH1F>("h_njets_40", ";number of jets with E_{T} > 40 GeV;Events", 20, 0, 20); 
  h_njets_30 = fs->make<TH1F>("h_njets_30", ";number of jets with E_{T} > 30 GeV;Events", 20, 0, 20);
  h_njets_20 = fs->make<TH1F>("h_njets_20", ";number of jets with E_{T} > 20 GeV;Events", 20, 0, 20);
  h_ht = fs->make<TH1F>("h_ht", ";#SigmaH_{T} of jets with E_{T} > 20 GeV;Events/100 GeV", 100, 0, 2000);
  h_ht40 = fs->make<TH1F>("h_ht40", ";#SigmaH_{T} of jets with E_{T} > 40 GeV;Events/100 GeV", 100, 0, 2000);

  NJets = fs->make<TH1F>("NJets", ";number of jets;Events", 20, 0, 20);
  Jets = bkh_factory->make("Jets", "gen jets");
  Jets->BookE (200, 0, 2000, "10");
  Jets->BookP (200, 0, 2000, "10");
  Jets->BookPt(200, 0, 2000, "10");
  Jets->BookPz(200, 0, 2000, "10");
  Jets->BookM (200, 0, 2000, "10");
  Jets->BookRapEta(200, "0.1");
  Jets->BookPhi(50, "0.125");
  
  JetAuxE = fs->make<TH1F>("JetAuxE", ";auxiliary energy of jet;jets/5 GeV", 200, 0, 1000);
  JetEmE = fs->make<TH1F>("JetEmE", ";EM energy of jet;jets/5 GeV", 200, 0, 1000);
  JetHadE = fs->make<TH1F>("JetEmE", ";hadronic energy of jet;jets/5 GeV", 200, 0, 1000);
  JetInvE = fs->make<TH1F>("JetEmE", ";invisible energy of jet;jets/5 GeV", 200, 0, 1000);
  JetNConstituents = fs->make<TH1F>("JetNConstituents", ";# of constituents of jet;jets", 200, 0, 200);
  JetNChargedConst = fs->make<TH1F>("JetNChargedConst", ";# of charged constituents of jet;jets", 200, 0, 200);
  JetFChargedConst = fs->make<TH1F>("JetFChargedConst", ";fraction of charged constituents of jet;jets", 200, 0, 1);
  JetNtracksPt = fs->make<TH2F>("JetNtracksPt", ";jet p_{T} (GeV);# of charged constituents of jet", 40, 0, 400, 40, 0, 40);
  JetNtracksptgt3Pt = fs->make<TH2F>("JetNtracksptgt3Pt", ";jet p_{T} (GeV);# of charged constituents of jet with p_{T} > 3 GeV", 40, 0, 400, 40, 0, 40);

  JetIds = fs->make<TH1F>("JetIds", ";pdg id of jet;jets", 11, 0, 11);
  const char* JetIdLabels[] = { "d", "u", "s", "c", "b", "dbar", "ubar", "sbar", "cbar", "bbar", "N/A" };
  set_bin_labels(JetIds->GetXaxis(), JetIdLabels);

  NBJets = fs->make<TH1F>("NBJets", ";number of b jets;Events", 30, 0, 30);
  BJets = bkh_factory->make("BJets", "gen jets with b id");
  BJets->BookE (200, 0, 2000, "10");
  BJets->BookP (200, 0, 2000, "10");
  BJets->BookPt(200, 0, 2000, "10");
  BJets->BookPz(200, 0, 2000, "10");
  BJets->BookM (200, 0, 2000, "10");
  BJets->BookRapEta(200, "0.1");
  BJets->BookPhi(50, "0.125");

  BJetAuxE = fs->make<TH1F>("BJetAuxE", ";auxiliary energy of b jet;jets/5 GeV", 200, 0, 1000);
  BJetEmE = fs->make<TH1F>("BJetEmE", ";EM energy of b jet;jets/5 GeV", 200, 0, 1000);
  BJetHadE = fs->make<TH1F>("BJetEmE", ";hadronic energy of b jet;jets/5 GeV", 200, 0, 1000);
  BJetInvE = fs->make<TH1F>("BJetEmE", ";invisible energy of b jet;jets/5 GeV", 200, 0, 1000);
  BJetNConstituents = fs->make<TH1F>("BJetNConstituents", ";# of constituents of b jet;jets", 200, 0, 200);
  BJetNChargedConst = fs->make<TH1F>("BJetNChargedConst", ";# of charged constituents of b jet;jets", 200, 0, 200);
  BJetFChargedConst = fs->make<TH1F>("BJetFChargedConst", ";fraction of charged constituents of b jet;jets", 200, 0, 1);
}

void MFVGenHistos::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  setup.getData(pdt);

  edm::Handle<reco::GenParticleCollection> gen_particles;
  event.getByToken(gen_token, gen_particles);

  edm::Handle<reco::GenJetCollection> gen_jets;
  event.getByToken(gen_jet_token, gen_jets);

  edm::Handle<mfv::MCInteraction> mci;
  event.getByToken(mci_token, mci);

  edm::Handle<std::vector<double>> gen_vertex;
  event.getByToken(gen_vertex_token, gen_vertex);
  const double x0 = (*gen_vertex)[0];
  const double y0 = (*gen_vertex)[1];
  const double z0 = (*gen_vertex)[2];

  auto fill = [x0,y0,z0](BasicKinematicHists* bkh, const reco::Candidate* c) {
    bkh->Fill(c);
    bkh->FillEx(signed_mag(c->vx() - x0, c->vy() - y0), c->vz() - z0, c->charge());
  };

  h_valid->Fill(mci->valid());

  if (!mci->valid()) {
    if (!mci_warned)
      edm::LogWarning("GenHistos") << "MCInteraction invalid; no further warnings!";
    mci_warned = true;
  }
  else {
    NumLeptons->Fill(mci->num_leptonic());
    DecayType->Fill(mci->decay_type()[0], mci->decay_type()[1]);

    for (int i = 0; i < 2; ++i) {
      reco::GenParticleRef lsp = mci->primaries()[i];
      const double lspbeta  = lsp->p()/lsp->energy();
      const double lspbetagamma = lspbeta/sqrt(1-lspbeta*lspbeta);
      h_lspbeta->Fill(lspbeta);
      h_lspbetagamma->Fill(lspbetagamma);

      const std::vector<reco::GenParticleRef> particles = mci->visible(i);
      const int npar = particles.size();
      std::vector<float> dx (npar, 0); 
      std::vector<float> dy (npar, 0); 
      std::vector<float> dz (npar, 0); 
      std::vector<float> r2d(npar, 0);
      std::vector<float> r3d(npar, 0);
      for (int j = 0; j < npar; ++j) {
        if (j == 5)
          break;
        dx [j] = particles[j]->vx() - x0;
        dy [j] = particles[j]->vy() - y0;
        dz [j] = particles[j]->vz() - z0;
        r2d[j] = mag(dx[j], dy[j]);
        r3d[j] = mag(dx[j], dy[j], dz[j]);

        // don't fill most of the plots for cases w/ two visible particles; the plots assume the visible particles are ordered according to names[9] above.
        // certainly not true for e.g. H->LLPs, LLP->b bbar. The LLP decay positions are correct, so only fill for j == 0
        // FIXME consider improving!
        if (j > 0 && npar == 2) continue;
        h_vtx[j]->Fill(dx[j], dy[j]);
        h_r2d[j]->Fill(r2d[j]);
        h_r3d[j]->Fill(r3d[j]);
      }
      
      const double ctau = r3d[0]/lspbetagamma;
      h_ctau->Fill(ctau);
      h_ctaubig->Fill(ctau);

      float min_deta =  1e99;
      float max_deta = -1e99;
      float min_dphi =  1e99;
      float max_dphi = -1e99;
      float min_dR =  1e99;
      float max_dR = -1e99;
      for (int j = 0; j < npar; ++j) {
        float pT = particles[j]->pt();
        float mass = particles[j]->mass();
        float phi = particles[j]->phi();
        float eta = particles[j]->eta();
        for (int k = j+1; k < npar; ++k) {
          float deta = fabs(particles[j]->eta() - particles[k]->eta());
          float dphi = fabs(reco::deltaPhi(particles[j]->phi(), particles[k]->phi()));
          float dR = reco::deltaR(*particles[j], *particles[k]);
          if (deta < min_deta)
            min_deta = deta;
          if (deta > max_deta)
            max_deta = deta;
          if (dphi < min_dphi)
            min_dphi = dphi;
          if (dphi > max_dphi)
            max_dphi = dphi;
          if (dR < min_dR)
            min_dR = dR;
          if (dR > max_dR)
            max_dR = dR;
        }
        h_llp_daughters_pt->Fill(pT);
        h_llp_daughters_mass->Fill(mass);
        h_llp_daughters_phi->Fill(phi);
        h_llp_daughters_eta->Fill(eta);
      }

      h_min_deta->Fill(min_deta);
      h_max_deta->Fill(max_deta);
      h_min_dphi->Fill(min_dphi);
      h_max_dphi->Fill(max_dphi);
      h_min_dR->Fill(min_dR);
      h_max_dR->Fill(max_dR);
      h_min_dR_vs_lspbeta->Fill(lspbeta, min_dR);
      h_max_dR_vs_lspbeta->Fill(lspbeta, max_dR);
      h_min_dR_vs_lspbetagamma->Fill(lspbetagamma, min_dR);
      h_max_dR_vs_lspbetagamma->Fill(lspbetagamma, max_dR);
    }
    
	h_lsp_dist2d->Fill(mci->dvv());
    h_lsp_dist3d->Fill(mci->d3d());

    TVector3 lsp_mom_0 = make_tlv(*mci->primaries()[0]).Vect();
    TVector3 lsp_mom_1 = make_tlv(*mci->primaries()[1]).Vect();
    h_lsp_angle3->Fill(lsp_mom_0.Dot(lsp_mom_1)/lsp_mom_0.Mag()/lsp_mom_1.Mag());
    lsp_mom_0.SetZ(0);
    lsp_mom_1.SetZ(0);
    h_lsp_angle2->Fill(lsp_mom_0.Dot(lsp_mom_1)/lsp_mom_0.Mag()/lsp_mom_1.Mag());


	// BEGIN: Hunt for b-quark decay points 
	if ( true ) {
		std::vector<double> vec_c_nonb_decay = {};
		std::vector<double> vec_c_nonb_dR_dau = {};
		std::vector<double> vec_c_nonb_dR_gdau = {};
		std::vector<double> vec_c_dR_b_to_llp = {0.0,0.0,0.0,0.0};
		std::vector<double> vec_c_llppT_b_to_llp = { 0.0,0.0,0.0,0.0 };
		std::vector<const reco::GenParticle*> vec_c_nonb_gen_particle = {};
		std::vector<const reco::GenParticle*> vec_c_b_gen_particle = {};
		// an effort to sort a set of b-quarks by their number of daughters 
		//std::vector<size_t> vec_ascending_total_bdaus; // a vector of ascending number of total daughters per b-quark  
		//std::vector<size_t> vec_ascending_total_bdaus_idx; // a vector of vertex index corresponding to the order of ascending total daughters in vec_ascending_total_bdaus

		
		//bool nonb_chain = false;
		if (mci->primaries().size() == 2 and mci->secondaries().size() == 4) {
			size_t nth_bquark = 0;
			
			// an effort to sort a set of b-quarks by their number of daughters before running a b-vertex finding algorithm 
			/*
			size_t idx = 0;
			for (auto p : mci->secondaries()) {
				if (idx == 0) {
					vec_ascending_total_bdaus.push_back(p->numberOfDaughters());
					vec_ascending_total_bdaus_idx.push_back(idx);
				}
				else {
					std::vector<size_t>::iterator it_bdaus = vec_ascending_total_bdaus.end();
					std::vector<size_t>::iterator it_idx = vec_ascending_total_bdaus_idx.end();
					// finding an iterator that points to a position that bdaus is just less than or equal to itself from the back to the front
					while (it_bdaus != vec_ascending_total_bdaus.begin() && p->numberOfDaughters() <= vec_ascending_total_bdaus[std::distance(vec_ascending_total_bdaus.begin(), it_bdaus) - 1])
					{
						--it_bdaus;
						--it_idx;
					}
					// adding a b-quark at the end if it has higher daus. otherwise, insert it before an iterator pointing to a position that this daus is smaller than itself 
					if (it_bdaus == vec_ascending_total_bdaus.end() && p->numberOfDaughters() > vec_ascending_total_bdaus[std::distance(vec_ascending_total_bdaus.begin(), it_bdaus)]) {
						vec_ascending_total_bdaus.push_back(p->numberOfDaughters());
						vec_ascending_total_bdaus_idx.push_back(idx);
					}

					else {
						vec_ascending_total_bdaus.insert(it_bdaus, p->numberOfDaughters());
						vec_ascending_total_bdaus_idx.insert(it_idx, idx);
					}
				}
				idx++;

			}
			*/

			for (reco::GenParticleRef genref_p : mci->secondaries()) {
			//for( size_t ib = 0, ibe = vec_ascending_total_bdaus_idx.size(); ib < ibe; ++ib){
			//	auto p = mci->secondaries()[vec_ascending_total_bdaus_idx[ib]];
				
				nth_bquark += 1;
				bool catch_b_vtx = false;
				std::vector<int> vec_dau_pdgID = {};
				std::vector<size_t> excl_idx_first_dRmin = {};
				std::vector<size_t> excl_idx_second_dRmin = {};
				int nth_chain = 1;
				
				
				const reco::GenParticle* p = genref_p.get();
				TVector3 llp_flight = TVector3(p->vx(), p->vy(), p->vz());
				if (p->numberOfDaughters() == 0)
					continue;
                int count_while_1 = 0;
				int count_while_2 = 0;
				while (!catch_b_vtx || (vec_c_nonb_decay.size() != nth_bquark || (vec_c_nonb_decay.size() == nth_bquark && std::count(vec_c_nonb_decay.begin(), vec_c_nonb_decay.end(), vec_c_nonb_decay[nth_bquark - 1]) > 1))) {
					
					
					
					size_t num_daus = p->numberOfDaughters();
					
					if (excl_idx_first_dRmin.size() == num_daus ) {
						break;
					}
					
					if (vec_c_nonb_decay.size() == nth_bquark && std::count(vec_c_nonb_decay.begin(), vec_c_nonb_decay.end(), vec_c_nonb_decay[nth_bquark - 1]) > 1) {
						vec_c_nonb_decay.pop_back();
						vec_c_nonb_gen_particle.pop_back();
						vec_c_b_gen_particle.pop_back();
					}
					if (vec_c_nonb_dR_dau.size() > vec_c_nonb_decay.size())
						vec_c_nonb_dR_dau.pop_back();
					while (vec_c_nonb_dR_gdau.size() != 0 && vec_c_nonb_dR_gdau.size() == vec_c_nonb_dR_dau.size())
						vec_c_nonb_dR_gdau.pop_back();

					
					if (nth_chain == 1 || (excl_idx_first_dRmin.size() > 0 && excl_idx_second_dRmin.size() == p->daughter(excl_idx_first_dRmin[excl_idx_first_dRmin.size() - 1])->numberOfDaughters())) {
						count_while_1 += 1;
						
						vec_dau_pdgID = {};
						nth_chain = 1;

						catch_b_vtx = Is_bdecay_done(nth_chain, p, p, vec_c_nonb_gen_particle, vec_c_b_gen_particle, vec_dau_pdgID, vec_c_nonb_dR_dau, vec_c_nonb_dR_gdau, vec_c_nonb_decay, excl_idx_first_dRmin, excl_idx_second_dRmin);
					}
					else {
						count_while_2 += 1;
						size_t idx_first_chain = excl_idx_first_dRmin[excl_idx_first_dRmin.size() - 1];
						while (vec_dau_pdgID.size() != 1)
							vec_dau_pdgID.pop_back();
						nth_chain = 2;
						
						catch_b_vtx = Is_bdecay_done(nth_chain, p, (const reco::GenParticle*)p->daughter(idx_first_chain), vec_c_nonb_gen_particle, vec_c_b_gen_particle, vec_dau_pdgID, vec_c_nonb_dR_dau, vec_c_nonb_dR_gdau, vec_c_nonb_decay, excl_idx_first_dRmin, excl_idx_second_dRmin);
						
					}
					
					if (count_while_1 == 10 || count_while_2 == 10) {

						std::cout << "STUCK:" << " 2 " << count_while_2 << " 1 " << count_while_1 << std::endl;
						std::cout << "nth b-quark : " << nth_bquark << " b-vertices : " << vec_c_nonb_decay.size() << std::endl;
						int n = int(vec_c_nonb_decay.size()) - 1;
						std::cout << "so far we have..." << std::endl;
						while (!(n < 0)) {
							std::cout << n << "th b-quark displ (cm) " << vec_c_nonb_decay[n] << std::endl;
							n--;
						}
						std::cout << "1th chain exclusion size : " << excl_idx_first_dRmin.size() << " is equal to # of b-quark's daus ?" << num_daus << std::endl;
						std::cout << "the current chain is down to " << nth_chain << std::endl;
						std::cout << "so as its history size " << vec_dau_pdgID.size() << std::endl;
						std::cout << "with its 2th chain exclusion size : " << excl_idx_second_dRmin.size() << std::endl;
						if (excl_idx_first_dRmin.size() != 0)
							std::cout << "hopefully the 2nd is not yet equal to # of b-quark's gdaus" << p->daughter(excl_idx_first_dRmin[excl_idx_first_dRmin.size() - 1])->numberOfDaughters() << std::endl;
															  
						break;
					}
					
				}

				if (vec_c_nonb_decay.size() == nth_bquark) {
					h_dau_to_gdau_mindR->Fill(vec_c_nonb_dR_dau[nth_bquark - 1]);
					h_gdau_to_ggdau_mindR->Fill(vec_c_nonb_dR_gdau[nth_bquark - 1]);

					size_t idx_llp = 0;
					if (!isBhadron(vec_dau_pdgID[vec_dau_pdgID.size() - 1])) {
						h_dau_select_b_decay_dist3d_from_llp->Fill(vec_c_nonb_decay[nth_bquark - 1]);
						h_dau_select_b_decay_dR_by_vec_nonb_had_to_b_had->Fill(reco::deltaR(vec_c_nonb_gen_particle[nth_bquark - 1]->eta(), vec_c_nonb_gen_particle[nth_bquark - 1]->phi(), vec_c_b_gen_particle[nth_bquark - 1]->eta(), vec_c_b_gen_particle[nth_bquark - 1]->phi()));
						if (nth_bquark-1 < 2) {
							vec_c_dR_b_to_llp[nth_bquark - 1] = fabs(reco::deltaPhi(mci->primaries()[0]->phi(), p->phi()));
							vec_c_llppT_b_to_llp[nth_bquark - 1] = mci->primaries()[0]->pt();

						}
						else {
							vec_c_dR_b_to_llp[nth_bquark - 1] = fabs(reco::deltaPhi(mci->primaries()[1]->phi(), p->phi()));
							vec_c_llppT_b_to_llp[nth_bquark - 1] = mci->primaries()[1]->pt();

						}
						h_dau_select_b_decay_dphi_by_vec_nonb_had_to_b_had->Fill(reco::deltaPhi(vec_c_nonb_gen_particle[nth_bquark - 1]->phi(), vec_c_b_gen_particle[nth_bquark - 1]->phi())); // non - b hadrons and its b - quark
						TVector3 nonb_flight = TVector3(vec_c_nonb_gen_particle[nth_bquark - 1]->vx() - p->vx(), vec_c_nonb_gen_particle[nth_bquark - 1]->vy() - p->vy(), vec_c_nonb_gen_particle[nth_bquark - 1]->vz() - p->vz());
						double bhad_dist3d = sqrt(pow(vec_c_b_gen_particle[nth_bquark - 1]->vx() - p->vx(), 2) + pow(vec_c_b_gen_particle[nth_bquark - 1]->vy() - p->vy(), 2) + pow(vec_c_b_gen_particle[nth_bquark - 1]->vz() - p->vz(), 2));
						h_dau_select_b_had_dist3d_from_llp->Fill(bhad_dist3d);
						h_dau_select_b_had_diff_pT_b_quark->Fill(vec_c_b_gen_particle[nth_bquark - 1]->pt() - p->pt());
						double bhad_beta = vec_c_b_gen_particle[nth_bquark - 1]->p() / vec_c_b_gen_particle[nth_bquark - 1]->energy();
						double bhad_betagamma = bhad_beta / sqrt(1 - bhad_beta * bhad_beta);
						h_dau_select_b_had_ctau->Fill(vec_c_nonb_decay[nth_bquark - 1] / bhad_betagamma);
						h_dau_select_b_had_pdgid->Fill(vec_c_b_gen_particle[nth_bquark - 1]->pdgId());
						h_dau_select_nonb_had_pdgid->Fill(vec_c_nonb_gen_particle[nth_bquark - 1]->pdgId());
						h_dau_select_b_had_gammabeta->Fill(bhad_betagamma);
						h_dau_select_b_had_pT->Fill(vec_c_b_gen_particle[nth_bquark - 1]->pt());

						if (nth_bquark == 2 || nth_bquark == 4) {
							double eta_nob0 = etaFromXYZ(vec_c_nonb_gen_particle[nth_bquark - 1]->vx(), vec_c_nonb_gen_particle[nth_bquark - 1]->vy(), vec_c_nonb_gen_particle[nth_bquark - 1]->vz());
							double eta_nob1 = etaFromXYZ(vec_c_nonb_gen_particle[nth_bquark - 2]->vx(), vec_c_nonb_gen_particle[nth_bquark - 2]->vy(), vec_c_nonb_gen_particle[nth_bquark - 2]->vz());
							h_dau_select_b_decay_absdphi_by_vec_two_nonb_had_per_llp->Fill(fabs(reco::deltaPhi(vec_c_nonb_gen_particle[nth_bquark - 1]->phi(), vec_c_nonb_gen_particle[nth_bquark - 2]->phi())));	  // |dphi| between two non-b hadrons per llp
							TVector3 another_nonb_flight = TVector3(vec_c_nonb_gen_particle[nth_bquark - 2]->vx() - p->vx(), vec_c_nonb_gen_particle[nth_bquark - 2]->vy() - p->vy(), vec_c_nonb_gen_particle[nth_bquark - 2]->vz() - p->vz());
							h_dau_select_b_decay_absdphi_by_pt_two_nonb_had_per_llp->Fill(fabs(reco::deltaPhi(nonb_flight.Phi(), another_nonb_flight.Phi())));	  // |dphi| between two non-b hadrons per llp by decay points
							h_dau_select_b_decay_absdeta_by_pt_two_nonb_had_per_llp->Fill(fabs(eta_nob0 - eta_nob1));	  // |deta| between two non-b hadrons per llp by decay points
							
							h_dau_select_b_had_absdphi_by_vec_two_b_had_per_llp->Fill(fabs(reco::deltaPhi(vec_c_b_gen_particle[nth_bquark - 1]->phi(), vec_c_b_gen_particle[nth_bquark - 2]->phi())));	  // |dphi| between two non-b hadrons per llp
							
							if (!isBhadron(vec_c_b_gen_particle[nth_bquark - 1]->pdgId())) {
								std::cout << "WARNING! this event has a nonb-hadron decaying to a displaced nonb-hadron at nth b-quark = " << nth_bquark << std::endl;
								std::cout << " run " << event.id().run() << " lumi " << event.luminosityBlock() << " event " << event.id().event() << "\n";
								//nonb_chain = true;
							}



						}
						if (nth_bquark == 1 || nth_bquark == 2) {
							idx_llp = 0;
						}
						else {
							idx_llp = 1;
						}

						h_dau_select_b_had_absdphi_by_vec_its_llp->Fill(fabs(reco::deltaPhi(vec_c_b_gen_particle[nth_bquark - 1]->phi(), mci->primaries()[idx_llp]->phi())));
						h_dau_select_b_quark_absdphi_by_vec_its_llp->Fill(fabs(reco::deltaPhi(p->phi(), mci->primaries()[idx_llp]->phi())));
						h_dau_select_b_had_absdphi_by_vec_its_b_quark->Fill(fabs(reco::deltaPhi(vec_c_b_gen_particle[nth_bquark - 1]->phi(), p->phi())));

					}
					else {
						h_dau_select_edge_b_decay_dist3d_from_llp->Fill(vec_c_nonb_decay[nth_bquark - 1]);
					}
				}
				


				
			}
		}

		bool weird_decay = false;
		for (size_t n = 0, ne = vec_c_b_gen_particle.size(); n < ne; ++n) {
			if (reco::deltaR(vec_c_nonb_gen_particle[n]->eta(), vec_c_nonb_gen_particle[n]->phi(), vec_c_b_gen_particle[n]->eta(), vec_c_b_gen_particle[n]->phi()) > 2) {
				weird_decay = true;
				std::cout << "investigating events w/ # of GEN b-vertices of " << vec_c_nonb_decay.size() << std::endl;
				std::cout << " run " << event.id().run() << " lumi " << event.luminosityBlock() << " event " << event.id().event() << "\n";
				std::cout << " id " << vec_c_b_gen_particle[n]->pdgId() << " #its daus " << vec_c_b_gen_particle[n]->numberOfDaughters() << " pt " << vec_c_b_gen_particle[n]->pt() << " eta " << vec_c_b_gen_particle[n]->eta() << " phi " << vec_c_b_gen_particle[n]->phi() << " mass " << vec_c_b_gen_particle[n]->mass() << std::endl;
				std::cout << "this large dR is : " << reco::deltaR(vec_c_nonb_gen_particle[n]->eta(), vec_c_nonb_gen_particle[n]->phi(), vec_c_b_gen_particle[n]->eta(), vec_c_b_gen_particle[n]->phi()) << std::endl;
				std::cout << "the following are other daus (that could have matched) dR " << std::endl;
				for (size_t i = 0, ie = vec_c_b_gen_particle[n]->numberOfDaughters(); i < ie; ++i) {
					const reco::GenParticle* dau = (const reco::GenParticle*) vec_c_b_gen_particle[n]->daughter(i);
					std::cout << "this dau dR is : " << reco::deltaR(dau->eta(), dau->phi(), vec_c_b_gen_particle[n]->eta(), vec_c_b_gen_particle[n]->phi()) << std::endl;
					std::cout <<" id " << dau->pdgId() << " #its daus " << dau->numberOfDaughters() << " pt " << dau->pt() << " eta " << dau->eta() << " phi " << dau->phi() << " mass " << dau->mass() << std::endl;

				}

			}
		}

		bool check_issue = true;
		if (weird_decay) {
			
           //std::cout << "WARNING!: # of b-vertices = " << vec_c_nonb_decay.size()  << "w/ repeated count = " << issue_count << std::endl;
		   /*
		   std::cout << "sorted number of b-daus in a vec of size "<< vec_ascending_total_bdaus_idx.size() << "is the following... " << std::endl;
		   for (size_t ib = 0, ibe = vec_ascending_total_bdaus_idx.size(); ib < ibe; ++ib) {
			   //auto p = mci->secondaries(vec_ascending_total_bdaus_idx[ib]);
			   //size_t num_daus = p->numberOfDaughters(); 
			   std::cout << vec_ascending_total_bdaus[ib] << std::endl;
			   
		   }
		   */
           if (check_issue) {

				for (size_t n = 0, ne = vec_c_nonb_decay.size(); n < ne; ++n) {
					std::cout << " displ (cm) " << vec_c_nonb_decay[n] << std::endl;
				}
				std::cout << "min dR from b-quark to its daus" << std::endl;
				for (size_t n = 0, ne = vec_c_nonb_dR_dau.size(); n < ne; ++n) {
					std::cout << " dau dR " << vec_c_nonb_dR_dau[n] << std::endl;
				}
				std::cout << "min dR from b-quark daus to its gdaus" << std::endl;
				for (size_t n = 0, ne = vec_c_nonb_dR_gdau.size(); n < ne; ++n) {
					std::cout << " gdau dR " << vec_c_nonb_dR_gdau[n] << std::endl;
				}

				size_t count_b = 0;
				for (auto p : mci->secondaries()) {
					
					std::cout << "the b-quark #" << count_b<< std::endl;
					count_b += 1;
					std::cout << "the delta R between b-quark and LLP is " << vec_c_dR_b_to_llp[count_b - 1] << " it's LLP pT is " << vec_c_llppT_b_to_llp[count_b - 1] << std::endl;
					std::cout << " # of daus " << p->numberOfDaughters() << std::endl;
					std::cout << "dau " << " id " << p->pdgId() << " #gdaus " << p->numberOfDaughters() << " pt " << p->pt() << " eta " << p->eta() << " phi " << p->phi() << " mass " << p->mass() << std::endl;
					for (size_t i = 0, ie = p->numberOfDaughters(); i < ie; ++i) {

						const reco::GenParticle* gdau = (reco::GenParticle*) p->daughter(i);
						double dau_dR = reco::deltaR(gdau->eta(), gdau->phi(), p->eta(), p->phi());

						double gdau_dist3d = sqrt(pow(gdau->vx() - p->vx(), 2) + pow(gdau->vy() - p->vy(), 2) + pow(gdau->vz() - p->vz(), 2));
						std::cout << "    gdau " << " displ (cm) " << gdau_dist3d << " id " << gdau->pdgId() << " #ggdaus " << gdau->numberOfDaughters() << " pt " << gdau->pt() << " eta " << gdau->eta() << " phi " << gdau->phi() << " mass " << gdau->mass() << std::endl;
						std::cout << "    gdau dR " << dau_dR << std::endl;
						for (size_t j = 0, je = gdau->numberOfDaughters(); j < je; ++j) {
							const reco::GenParticle* ggdau = (reco::GenParticle*) gdau->daughter(j);
							double gdau_dR = reco::deltaR(ggdau->eta(), ggdau->phi(), gdau->eta(), gdau->phi());

							double ggdau_dist3d = sqrt(pow(ggdau->vx() - p->vx(), 2) + pow(ggdau->vy() - p->vy(), 2) + pow(ggdau->vz() - p->vz(), 2));
							std::cout << "        ggdau " << " displ (cm) " << ggdau_dist3d << " id " << ggdau->pdgId() << " #gggdaus " << ggdau->numberOfDaughters() << " pt " << ggdau->pt() << " eta " << ggdau->eta() << " phi " << ggdau->phi() << " mass " << ggdau->mass() << std::endl;
							std::cout << "        ggdau dR " << gdau_dR << std::endl;
							for (size_t k = 0, ke = ggdau->numberOfDaughters(); k < ke; ++k) {
								const reco::GenParticle* gggdau = (reco::GenParticle*) ggdau->daughter(k);
								double gggdau_dist3d = sqrt(pow(gggdau->vx() - p->vx(), 2) + pow(gggdau->vy() - p->vy(), 2) + pow(gggdau->vz() - p->vz(), 2));
								std::cout << "           gggdau " << " displ (cm) " << gggdau_dist3d << " id " << gggdau->pdgId() << " #ggggdaus " << gggdau->numberOfDaughters() << " pt " << gggdau->pt() << " eta " << gggdau->eta() << " phi " << gggdau->phi() << " mass " << gggdau->mass() << std::endl;
								for (size_t l = 0, le = gggdau->numberOfDaughters(); l < le; ++l) {
									const reco::GenParticle* ggggdau = (reco::GenParticle*) gggdau->daughter(l);
									double ggggdau_dist3d = sqrt(pow(ggggdau->vx() - p->vx(), 2) + pow(ggggdau->vy() - p->vy(), 2) + pow(ggggdau->vz() - p->vz(), 2));
									std::cout << "                ggggdau " << " displ (cm) " << ggggdau_dist3d << " id " << ggggdau->pdgId() << " #gggggdaus " << ggggdau->numberOfDaughters() << " pt " << ggggdau->pt() << " eta " << ggggdau->eta() << " phi " << ggggdau->phi() << " mass " << ggggdau->mass() << std::endl;
									for (size_t m = 0, me = ggggdau->numberOfDaughters(); m < me; ++m) {
										const reco::GenParticle* gggggdau = (reco::GenParticle*) ggggdau->daughter(m);
										double gggggdau_dist3d = sqrt(pow(gggggdau->vx() - p->vx(), 2) + pow(gggggdau->vy() - p->vy(), 2) + pow(gggggdau->vz() - p->vz(), 2));
										std::cout << "                   gggggdau " << " displ (cm) " << gggggdau_dist3d << " id " << gggggdau->pdgId() << " ggggggdaus " << gggggdau->numberOfDaughters() << " pt " << gggggdau->pt() << " eta " << gggggdau->eta() << " phi " << gggggdau->phi() << " mass " << gggggdau->mass() << std::endl;
										for (size_t n = 0, ne = gggggdau->numberOfDaughters(); n < ne; ++n) {
											const reco::GenParticle* ggggggdau = (reco::GenParticle*) gggggdau->daughter(n);
											double ggggggdau_dist3d = sqrt(pow(ggggggdau->vx() - p->vx(), 2) + pow(ggggggdau->vy() - p->vy(), 2) + pow(ggggggdau->vz() - p->vz(), 2));
											std::cout << "                        ggggggdau " << " displ (cm) " << ggggggdau_dist3d << " id " << ggggggdau->pdgId() << " gggggggdaus " << ggggggdau->numberOfDaughters() << " pt " << ggggggdau->pt() << " eta " << ggggggdau->eta() << " phi " << ggggggdau->phi() << " mass " << ggggggdau->mass() << std::endl;

										}
									}
								}
							}
						}
					}

				}
			}
			

		}
		
		h_n_gen_bvtx->Fill(vec_c_nonb_decay.size());
		
	}
	// END: Hunt for b-quark decay points 
	

    int npartons_in_acc = 0;
    int npartons_60 = 0;
    for (auto p : mci->visible()) {
      if (p->pt() > 20 && fabs(p->eta()) < 2.5)
        ++npartons_in_acc;
      if (p->pt() > 60 && fabs(p->eta()) < 2.5)
        ++npartons_60;
    }
    h_npartons_in_acc->Fill(npartons_in_acc);
    h_npartons_60->Fill(npartons_60);
    
    if (mci->type() == mfv::mci_MFVtbs) { // || mci->type() == mci_Ttbar) {
      for (int i = 0; i < 2; ++i) {
        fill(Lsps           [i], &*mci->lsp(i));
        fill(Stranges       [i], &*mci->strange(i));
        fill(Bottoms        [i], &*mci->primary_bottom(i));
        fill(Tops           [i], &*mci->top(i));
        fill(Ws             [i], &*mci->W(i));
        fill(BottomsFromTops[i], &*mci->bottom(i));

        for (int j = 0; j < 2; ++j) {
          const reco::Candidate* c = &*mci->W_daughter(i,j);
          fill(WDaughters[i][j], c);
          const int id = abs(c->pdgId());
          if      (id == 11) { fill(Leptons, c); fill(LightLeptons, c); fill(Electrons, c); }
          else if (id == 13) { fill(Leptons, c); fill(LightLeptons, c); fill(Muons,     c); }
          else if (id == 15) { fill(Leptons, c);                        fill(Taus,      c); }
        }


        const int lsp_ndau = 5;
        const reco::GenParticleRef lsp_daughters[lsp_ndau] = { mci->strange(i), mci->primary_bottom(i), mci->bottom(i), mci->W_daughter(i, 0), mci->W_daughter(i, 1) };

        int lsp_ntracks = 0;
        float lsp_min_dR =  1e99;
        float lsp_max_dR = -1e99;
        for (int j = 0; j < lsp_ndau; ++j) {
          h_neutralino_daughters_pt->Fill(lsp_daughters[j]->pt());
          h_neutralino_daughters_eta->Fill(lsp_daughters[j]->eta());
          h_neutralino_daughters_dxy->Fill(mag(mci->strange(i)->vx() - mci->lsp(i)->vx(), mci->strange(i)->vy() - mci->lsp(i)->vy()) * sin(lsp_daughters[j]->phi() - atan2(mci->strange(i)->vy() - mci->lsp(i)->vy(), mci->strange(i)->vx() - mci->lsp(i)->vx())));
          h_neutralino_daughters_dxy_dBV->Fill(mag(mci->strange(i)->vx() - mci->lsp(i)->vx(), mci->strange(i)->vy() - mci->lsp(i)->vy()), mag(mci->strange(i)->vx() - mci->lsp(i)->vx(), mci->strange(i)->vy() - mci->lsp(i)->vy()) * sin(lsp_daughters[j]->phi() - atan2(mci->strange(i)->vy() - mci->lsp(i)->vy(), mci->strange(i)->vx() - mci->lsp(i)->vx())));

          int nmatch = 0;
          for (const reco::GenJet& jet : *gen_jets) {
            h_neutralino_daughters_jets_dR->Fill(reco::deltaR(*lsp_daughters[j], jet));
            if (reco::deltaR(*lsp_daughters[j], jet) < 0.4) {
              ++nmatch;
            }
          }
          h_neutralino_daughters_jets_nmatch->Fill(nmatch);

          if (is_neutrino(lsp_daughters[j]) || fabs(lsp_daughters[j]->eta()) > 2.5) continue;

          if (is_lepton(lsp_daughters[j]))
            ++lsp_ntracks;
          else {
            for (const reco::GenJet& jet : *gen_jets) {
              if (reco::deltaR(*lsp_daughters[j], jet) < 0.4) {
                for (unsigned int idx = 0; idx < jet.numberOfDaughters(); ++idx) {
                  const pat::PackedGenParticle* g = dynamic_cast<const pat::PackedGenParticle*>(jet.daughter(idx));
                  if (g->charge())
                    ++lsp_ntracks;
                }
              }
            }
          }
          
          for (int k = j+1; k < lsp_ndau; ++k) {
            if (is_neutrino(lsp_daughters[k]) || fabs(lsp_daughters[k]->eta()) > 2.5) continue;
            float dR = reco::deltaR(*lsp_daughters[j], *lsp_daughters[k]);
            if (dR < lsp_min_dR)
              lsp_min_dR = dR;
            if (dR > lsp_max_dR)
              lsp_max_dR = dR;
          }
        }

        h_lsp_ntracks->Fill(lsp_ntracks);
        h_lsp_min_dR->Fill(lsp_min_dR);
        h_lsp_max_dR->Fill(lsp_max_dR);
      }


    }
    if (mci->type() == mfv::mci_MFVuds) {
      for (int i = 0; i < 2; ++i) {
        fill(Lsps           [i], &*mci->lsp(i));
        fill(Stranges       [i], &*mci->strange(i));
        fill(Ups            [i], &*mci->up(i));
        fill(Downs          [i], &*mci->down(i));
      }
    }
    else if (mci->type() == mfv::mci_XX4j || mci->type() == mfv::mci_MFVddbar || mci->type() == mfv::mci_MFVbbbar || mci->type() == mfv::mci_MFVlq || mci->type() == mfv::mci_stopdbardbar) {
      for (int i = 0; i < 2; ++i) {
        fill(Hs[i], &*mci->primaries()[i]);
        for (int j = 0; j < 2; ++j)
          fill(Qs[i][j], &*mci->secondaries()[i*2+j]);
      }
    }
  }

  // Now look at b quarks separately. Count the number of status-3 b
  // quarks, those with tops, vector bosons, or LSPs as mothers so
  // that we only get each one once. Also as cross check count the
  // number of b hadrons (should be status 2), those with b quarks as
  // mothers.
  const double min_b_pt = 20;
  const double max_b_eta = 2.5;
  int nbquarks = 0;
  int nbhadrons = 0;
  int nbquarks_wcuts = 0;
  int nbhadrons_wcuts = 0;
  std::vector<int> bquarks_ids;
  std::vector<double> bquarks_eta;
  std::vector<double> bquarks_phi;
  for (const reco::GenParticle& gen : *gen_particles) {
    if (abs(gen.pdgId()) == 5) {
      bool has_b_dau = false;
      for (size_t i = 0, ie = gen.numberOfDaughters(); i < ie; ++i) {
        if (abs(gen.daughter(i)->pdgId()) == 5) {
          has_b_dau = true;
          break;
        }
      }
      if (!has_b_dau) {
        ++nbquarks;
        h_bquarks_pt->Fill(gen.pt());
        h_bquarks_eta->Fill(gen.eta());
        h_bquarks_phi->Fill(gen.phi());
        h_bquarks_energy->Fill(gen.energy());
        bquarks_ids.push_back(gen.pdgId());
        bquarks_eta.push_back(gen.eta());
        bquarks_phi.push_back(gen.phi());
        if (gen.pt() > min_b_pt && fabs(gen.eta()) < max_b_eta) {
          ++nbquarks_wcuts;
        }
      }
    }

    if (is_bhadron(&gen)) {
      bool has_b_mom = false;
      for (size_t i = 0, ie = gen.numberOfMothers(); i < ie; ++i) {
        if (is_bhadron(gen.mother(i))) {
          has_b_mom = true;
          break;
        }
      }
      if (!has_b_mom) {
        ++nbhadrons;
        if (gen.pt() > min_b_pt && fabs(gen.eta()) < max_b_eta) {
          ++nbhadrons_wcuts;
        }
      }
    }
  }

  h_nbhadronsvsbquarks->Fill(nbquarks, nbhadrons);
  h_nbhadronsvsbquarks_wcuts->Fill(nbquarks_wcuts, nbhadrons_wcuts);
  h_nbquarks->Fill(nbquarks);
  if (bquarks_ids.size() == 2) {
    double dphi = reco::deltaPhi(bquarks_phi[0], bquarks_phi[1]);
    double deta = bquarks_eta[0] - bquarks_eta[1];
    double avgeta = (bquarks_eta[0] + bquarks_eta[1]) / 2;
    double dR = reco::deltaR(bquarks_eta[0], bquarks_phi[0], bquarks_eta[1], bquarks_phi[1]);
    h_bquarks_absdphi->Fill(fabs(dphi));
    h_bquarks_dphi->Fill(dphi);
    h_bquarks_deta->Fill(deta);
    h_bquarks_deta_dphi->Fill(dphi, deta);
    h_bquarks_avgeta->Fill(avgeta);
    h_bquarks_avgeta_dphi->Fill(dphi, avgeta);
    h_bquarks_dR->Fill(dR);
    h_bquarks_dR_dphi->Fill(dphi, dR);
  }

  int njets = 0;
  int nbjets = 0;
  int njets60 = 0;
  int njets40 = 0;
  int njets30 = 0;
  int njets20 = 0; 
  float ht = 0, ht40 = 0;
  for (const reco::GenJet& jet : *gen_jets) {
    if (jet.pt() < 20 || fabs(jet.eta()) > 2.5)
      continue;

    ++njets;
    ht += jet.pt();
    if (jet.pt() > 20)
      ++njets20;
    if (jet.pt() > 30)
      ++njets30;
    if (jet.pt() > 40){
      ht40 += jet.pt();
      ++njets40;
    }
    if (jet.pt() > 60)
      ++njets60;

    int nchg = 0;
    int id = gen_jet_id(jet);
    int ntracksptgt3 = 0;
    for (unsigned int idx = 0; idx < jet.numberOfDaughters(); ++idx) {
      const pat::PackedGenParticle* g = dynamic_cast<const pat::PackedGenParticle*>(jet.daughter(idx));
      if (g && g->charge())
        ++nchg;
      if (g && g->charge() && g->pt() > 3)
        ++ntracksptgt3;
    }

    float fchg = float(nchg)/jet.nConstituents();

    Jets->Fill(&jet);
    JetAuxE->Fill(jet.auxiliaryEnergy());
    JetEmE->Fill(jet.emEnergy());
    JetHadE->Fill(jet.hadEnergy());
    JetInvE->Fill(jet.invisibleEnergy());
    JetNConstituents->Fill(jet.nConstituents());
    JetNChargedConst->Fill(nchg);
    JetFChargedConst->Fill(fchg);
    JetNtracksPt->Fill(jet.pt(), nchg);
    JetNtracksptgt3Pt->Fill(jet.pt(), ntracksptgt3);

    fill_by_label(JetIds, id != 0 ? pdt->particle(id)->name() : "N/A");

    if (id == 5) {
      ++nbjets;

      BJets->Fill(&jet);
      BJetAuxE->Fill(jet.auxiliaryEnergy());
      BJetEmE->Fill(jet.emEnergy());
      BJetHadE->Fill(jet.hadEnergy());
      BJetInvE->Fill(jet.invisibleEnergy());
      BJetNConstituents->Fill(jet.nConstituents());
      BJetNChargedConst->Fill(nchg);
      BJetFChargedConst->Fill(fchg);
    }      
  }
  NJets->Fill(njets);
  NBJets->Fill(nbjets);
  h_njets_60->Fill(njets60);
  h_njets_40->Fill(njets40); 
  h_njets_30->Fill(njets30);
  h_njets_20->Fill(njets20); 
  h_ht->Fill(ht);
  h_ht40->Fill(ht40);
}

bool MFVGenHistos::isBhadron(int pdgID) {
	return (int(abs(pdgID)/100) % 10) == 5 || (int(abs(pdgID) / 1000) % 10) == 5 ;
}

bool MFVGenHistos::isBquark(int pdgID) {
	return fabs(pdgID) == 5;
}

bool MFVGenHistos::isValidLeptonic(const reco::GenParticle* parent, int pdgID) {
	bool found_lepton_pair = false;			// this is a photon radiated from a b-quark to l-l+ and two neutrinos 
	for (size_t i = 0, ie = parent->numberOfDaughters(); i < ie; ++i) {
		const reco::GenParticle* dau = (const reco::GenParticle*) parent->daughter(i);
		if (pdgID == -1* dau->pdgId() && (abs(pdgID) == 11|| abs(pdgID) == 13 || abs(pdgID) == 15) )
			found_lepton_pair = true;
	}
	return !found_lepton_pair;
}

bool MFVGenHistos::isBvtx(const reco::GenParticle* parent, int pdgID, double dist3d, std::vector<int> vec_pdgID) {
	
	for (size_t i = 1, ie = vec_pdgID.size() - 1; i < ie; ++i) {
		if (!(isBhadron(abs(vec_pdgID[i])) == true  	  // the chain of b-hadrons
			|| isBquark(abs(vec_pdgID[i])) == true
			|| ( i < vec_pdgID.size() - 2 && vec_pdgID[i] == 21 && isBhadron(abs(vec_pdgID[i+1])) == true)))			  // allow gluons to b-mesons 
			return false;
		
	}
		
	return dist3d > 0 && isValidLeptonic(parent, pdgID);
}



size_t MFVGenHistos::mindR_dau(int &nth_chain, const reco::GenParticle* parent, std::vector<double>& vec_first_dR, std::vector<double>& vec_second_dR, std::vector<size_t>& excl_idx_first_dRmin, std::vector<size_t>& excl_idx_second_dRmin) {

	double mindR = 200;
	size_t idx_mindR = 0;
	
	for (size_t i = 0, ie = parent->numberOfDaughters(); i < ie; ++i) {

		    
			if (nth_chain == 1 && std::count(excl_idx_first_dRmin.begin(), excl_idx_first_dRmin.end(), i) == 1)
				continue;

			if (nth_chain == 2 && std::count(excl_idx_second_dRmin.begin(), excl_idx_second_dRmin.end(), i) == 1)
				continue;
			

			const reco::GenParticle* dau = (const reco::GenParticle*) parent->daughter(i);
			double dau_dR = reco::deltaR(dau->eta(), dau->phi(), parent->eta(), parent->phi());
			if (dau_dR < mindR) {
				mindR = dau_dR;
				idx_mindR = i;
			}
	}
    

	//ONLY for printouts
	if (nth_chain == 1 && std::count(vec_first_dR.begin(), vec_first_dR.end(), mindR) == 0) {
		vec_first_dR.push_back(mindR);
	}
	
	if (nth_chain == 2 && std::count(vec_second_dR.begin(), vec_second_dR.end(), mindR) == 0) {
		vec_second_dR.push_back(mindR);
	}
	
	return idx_mindR;
}


bool MFVGenHistos::Is_bdecay_done(int &nth_chain, const reco::GenParticle* bquark, const reco::GenParticle* parent, std::vector<const reco::GenParticle*>& vec_gen_particle, std::vector<const reco::GenParticle*>& vec_bhad_gen_particle, std::vector<int>& vec_pdgID, std::vector<double>& vec_first_dR, std::vector<double>& vec_second_dR, std::vector<double>& vec_decay, std::vector<size_t>& excl_idx_first_dRmin, std::vector<size_t>& excl_idx_second_dRmin) {

	
	for (size_t i = 0, ie = parent->numberOfDaughters(); i < ie; ++i) {
			// gdau stage
		    if (nth_chain == 2 && excl_idx_second_dRmin.size() == parent->numberOfDaughters())
			    break;

			if (nth_chain == 1 || nth_chain == 2) {
				if (i != mindR_dau(nth_chain, parent, vec_first_dR, vec_second_dR, excl_idx_first_dRmin, excl_idx_second_dRmin))
					continue;
		    }
			if (nth_chain == 1 && std::count(excl_idx_first_dRmin.begin(), excl_idx_first_dRmin.end(), i) == 0)	{
				excl_idx_first_dRmin.push_back(i);
				excl_idx_second_dRmin = {};
			}
			if (nth_chain == 2 && std::count(excl_idx_second_dRmin.begin(), excl_idx_second_dRmin.end(), i) == 0) {
				excl_idx_second_dRmin.push_back(i);
			}
			
			const reco::GenParticle* dau = (const reco::GenParticle*) parent->daughter(i);
			
			int dau_pdgID = dau->pdgId();
			double dau_dist3d = sqrt(pow(dau->vx() - bquark->vx(), 2) + pow(dau->vy() - bquark->vy(), 2) + pow(dau->vz() - bquark->vz(), 2));
			vec_pdgID.push_back(dau_pdgID);
			if (isBhadron(dau_pdgID)) {
				if (isBvtx(parent, dau_pdgID, dau_dist3d, vec_pdgID)) {
					vec_decay.push_back(dau_dist3d);
					break;
				}
			}
			else {
				if (!isBquark(dau_pdgID)) {
					if (isBvtx(parent, dau_pdgID, dau_dist3d, vec_pdgID)) {
						vec_decay.push_back(dau_dist3d);
						vec_gen_particle.push_back(dau);
						vec_bhad_gen_particle.push_back(parent);
						break;
					}
				}
			}
			
			nth_chain += 1;
			return Is_bdecay_done(nth_chain, bquark, dau, vec_gen_particle, vec_bhad_gen_particle, vec_pdgID, vec_first_dR, vec_second_dR, vec_decay, excl_idx_first_dRmin, excl_idx_second_dRmin);
	}

	return true;
}

DEFINE_FWK_MODULE(MFVGenHistos);
