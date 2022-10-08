#include "TH1F.h"
#include "TH2F.h"
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
  bool isBquark(int pdgID);
  bool isBvtx(int pdgID, double dist3d, std::vector<int> vec_btag);
  reco::GenParticle* valid_dau(auto parent, reco::GenParticle* dau, double thes_dR);
  size_t mindR_dau(int nth_chain, auto parent, std::vector<double>& vec_first_dR, std::vector<double>& vec_second_dR);
  bool Is_bdecay_done(int nth_chain, const reco::GenParticleRef& bquark, auto parent, std::vector<int>& vec_btag, std::vector<double>& vec_first_dR, std::vector<double>& vec_second_dR, std::vector<double>& vec_decay);
  void print_bchain(int num, auto init_p);

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

  TH1I* h_n_gen_bvtx;
  TH1F* h_missing_dau_to_gdau_mindR;
  TH1F* h_missing_gdau_to_ggdau_mindR;
  TH1F* h_dau_to_gdau_mindR;
  TH1F* h_gdau_to_ggdau_mindR;
  TH1F* h_dau_select_edge_b_decay_dist3d_from_llp;
  TH1F* h_dau_select_b_decay_dist3d_from_llp;

  TH1I* h_gdau_bhadrons_pdgID; 
  TH1I* h_gdau_nonbhadrons_pdgID;
  TH1F* h_gdau_bhadrons_dist3d_from_llp;
  TH1F* h_gdau_nonbhadrons_dist3d_from_llp;
  TH1F* h_gdau_n_b_decay_points;
  TH1F* h_gdau_n_non_b_decay_points;
  TH1F* h_gdau_select_edge_b_decay_dist3d_from_llp;
  TH1F* h_gdau_select_b_decay_dist3d_from_llp;

  TH1I* h_ggdau_bhadrons_pdgID;
  TH1I* h_ggdau_nonbhadrons_pdgID;
  TH1F* h_ggdau_bhadrons_dist3d_from_llp;
  TH1F* h_ggdau_nonbhadrons_dist3d_from_llp;
  TH1F* h_ggdau_n_b_decay_points;
  TH1F* h_ggdau_n_non_b_decay_points;
  TH1F* h_ggdau_select_edge_b_decay_dist3d_from_llp;
  TH1F* h_ggdau_select_b_decay_dist3d_from_llp;

  TH1I* h_gggdau_bhadrons_pdgID;
  TH1I* h_gggdau_for_ggggdau_bhadrons_pdgID;
  TH1I* h_gggdau_nonbhadrons_pdgID;
  TH1F* h_gggdau_bhadrons_dist3d_from_llp;
  TH1F* h_gggdau_nonbhadrons_dist3d_from_llp;
  TH1F* h_gggdau_n_b_decay_points;
  TH1F* h_gggdau_n_non_b_decay_points;
  TH1F* h_gggdau_select_edge_b_decay_dist3d_from_llp;
  TH1F* h_gggdau_select_b_decay_dist3d_from_llp;
  

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
  h_missing_dau_to_gdau_mindR = fs->make<TH1F>("h_missing_dau_to_gdau_mindR", "found < 4 b-vertices;minimum dR of a b-quark and its daughter; arb. units", 140, 0, 7.0);
  h_missing_gdau_to_ggdau_mindR = fs->make<TH1F>("h_missing_gdau_to_ggdau_mindR", "found < 4 b-vertices;minimum dR of b-quark's daughter and its granddaughter; arb. units", 140, 0, 7.0);
  h_dau_to_gdau_mindR = fs->make<TH1F>("h_dau_to_gdau_mindR", ";minimum dR of a b-quark and its daughter; arb. units", 140, 0, 7.0);
  h_gdau_to_ggdau_mindR = fs->make<TH1F>("h_gdau_to_ggdau_mindR", ";minimum dR of b-quark's daughter and its granddaughter; arb. units", 140, 0, 7.0);
  h_dau_select_edge_b_decay_dist3d_from_llp = fs->make<TH1F>("h_dau_select_edge_b_decay_dist3d_from_llp", "multiple dau stage w.r.t LLP (final product still a b-hadron); displaced b-quark vtx from an LLP decay position (cm);b-vtx/0.0025 cm", 500, 0, 1);
  h_dau_select_b_decay_dist3d_from_llp = fs->make<TH1F>("h_dau_select_b_decay_dist3d_from_llp", "multiple dau stage w.r.t LLP; displaced b-quark vtx from an LLP decay position (cm);b-vtx/0.0025 cm", 500, 0, 1);


  h_gdau_bhadrons_pdgID = fs->make<TH1I>("h_gdau_bhadrons_pdgID", "gdau stage w.r.t LLP;pdg id of b-hadron;jets", 10000, -5000, 5000);
  h_gdau_nonbhadrons_pdgID = fs->make<TH1I>("h_gdau_nonbhadrons_pdgID", "gdau stage w.r.t LLP;pdg id of non b-hadron;jets", 10000, -5000, 5000);
  h_gdau_bhadrons_dist3d_from_llp = fs->make<TH1F>("h_gdau_bhadrons_dist3d_from_llp", "gdau stage w.r.t LLP;3D distance of b-hadrom from LLP decay positions (cm);b-hadron/0.0025 cm", 500, 0, 1);
  h_gdau_nonbhadrons_dist3d_from_llp = fs->make<TH1F>("h_gdau_nonbhadrons_dist3d_from_llp", "gdau stage w.r.t LLP;3D distance of non b-hadrom from LLP decay positions (cm);non b-hadron/0.0025 cm", 500, 0, 1);
  h_gdau_n_b_decay_points = fs->make<TH1F>("h_gdau_n_b_decay_points", "gdau stage w.r.t LLP; # of non-zero b-decay points at this stage;events", 10, 0, 10);
  h_gdau_n_non_b_decay_points = fs->make<TH1F>("h_gdau_n_non_b_decay_points", "gdau stage w.r.t LLP; # of non-zero non b-decay points at this stage;events", 10, 0, 10);
  h_gdau_select_edge_b_decay_dist3d_from_llp = fs->make<TH1F>("h_gdau_select_edge_b_decay_dist3d_from_llp", "gdau stage w.r.t LLP (final product still a b-hadron); displaced b-quark vtx from an LLP decay position (cm);b-vtx/0.0025 cm", 500, 0, 1);
  h_gdau_select_b_decay_dist3d_from_llp = fs->make<TH1F>("h_gdau_select_b_decay_dist3d_from_llp", "gdau stage w.r.t LLP; displaced b-quark vtx from an LLP decay position (cm);b-vtx/0.0025 cm", 500, 0, 1);


  h_ggdau_bhadrons_pdgID = fs->make<TH1I>("h_ggdau_bhadrons_pdgID", "ggdau stage w.r.t LLP;pdg id of b-hadron;jets", 10000, -5000, 5000);
  h_ggdau_nonbhadrons_pdgID = fs->make<TH1I>("h_ggdau_nonbhadrons_pdgID", "ggdau stage w.r.t LLP;pdg id of non b-hadron;jets", 10000, -5000, 5000);
  h_ggdau_bhadrons_dist3d_from_llp = fs->make<TH1F>("h_ggdau_bhadrons_dist3d_from_llp", "ggdau stage w.r.t LLP;3D distance of b-hadrom from LLP decay positions (cm);b-hadron/0.0025 cm", 500, 0, 1);
  h_ggdau_nonbhadrons_dist3d_from_llp = fs->make<TH1F>("h_ggdau_nonbhadrons_dist3d_from_llp", "ggdau stage w.r.t LLP;3D distance of non b-hadrom from LLP decay positions (cm);non b-hadron/0.0025 cm", 500, 0, 1);
  h_ggdau_n_b_decay_points = fs->make<TH1F>("h_ggdau_n_b_decay_points", "ggdau stage w.r.t LLP; # of non-zero b-decay points at this stage;events", 10, 0, 10);
  h_ggdau_n_non_b_decay_points = fs->make<TH1F>("h_ggdau_n_non_b_decay_points", "ggdau stage w.r.t LLP; # of non-zero non b-decay points at this stage;events", 10, 0, 10);
  h_ggdau_select_edge_b_decay_dist3d_from_llp = fs->make<TH1F>("h_ggdau_select_edge_b_decay_dist3d_from_llp", "ggdau stage w.r.t LLP (final product still a b-hadron); displaced b-quark vtx from an LLP decay position (cm);b-vtx/0.0025 cm", 500, 0, 1);
  h_ggdau_select_b_decay_dist3d_from_llp = fs->make<TH1F>("h_ggdau_select_b_decay_dist3d_from_llp", "ggdau stage w.r.t LLP; displaced b-quark vtx from an LLP decay positions (cm);b-vtx/0.0025 cm", 500, 0, 1);

  h_gggdau_bhadrons_pdgID = fs->make<TH1I>("h_gggdau_bhadrons_pdgID", "gggdau stage w.r.t LLP;pdg id of b-hadron;jets", 10000, -5000, 5000);
  h_gggdau_for_ggggdau_bhadrons_pdgID = fs->make<TH1I>("h_gggdau_for_ggggdau_bhadrons_pdgID", "gggdau stage w.r.t LLP;pdg id of b-hadron stisfying b-decays;jets", 10000, -5000, 5000);
  h_gggdau_nonbhadrons_pdgID = fs->make<TH1I>("h_gggdau_nonbhadrons_pdgID", "gggdau stage w.r.t LLP;pdg id of non b-hadron;jets", 10000, -5000, 5000);
  h_gggdau_bhadrons_dist3d_from_llp = fs->make<TH1F>("h_gggdau_bhadrons_dist3d_from_llp", "gggdau stage w.r.t LLP;3D distance of b-hadrom from LLP decay positions (cm);b-hadron/0.0025 cm", 500, 0, 1);
  h_gggdau_nonbhadrons_dist3d_from_llp = fs->make<TH1F>("h_gggdau_nonbhadrons_dist3d_from_llp", "gggdau stage w.r.t LLP;3D distance of non b-hadrom from LLP decay positions (cm);non b-hadron/0.0025 cm", 500, 0, 1);
  h_gggdau_n_b_decay_points = fs->make<TH1F>("h_gggdau_n_b_decay_points", "gggdau stage w.r.t LLP; # of non-zero b-decay points at this stage;events", 10, 0, 10);
  h_gggdau_n_non_b_decay_points = fs->make<TH1F>("h_gggdau_n_non_b_decay_points", "gggdau stage w.r.t LLP; # of non-zero non b-decay points at this stage;events", 10, 0, 10);
  h_gggdau_select_edge_b_decay_dist3d_from_llp = fs->make<TH1F>("h_gggdau_select_edge_b_decay_dist3d_from_llp", "gggdau stage w.r.t LLP (final product still a b-hadron); displaced b-quark vtx from an LLP decay position (cm);b-vtx/0.0025 cm", 500, 0, 1);
  h_gggdau_select_b_decay_dist3d_from_llp = fs->make<TH1F>("h_gggdau_select_b_decay_dist3d_from_llp", "gggdau stage w.r.t LLP; displaced b-quark vtx from LLP decay positions (cm);b-vtx/0.0025 cm", 500, 0, 1);


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
	if (mci->valid()) {
		
		/*
		std::vector<double> vec_c_gdau_b_decay = {};
		std::vector<double> vec_c_gdau_nonb_decay = {};
		std::vector<double> vec_c_ggdau_b_decay = {};
		std::vector<double> vec_c_ggdau_nonb_decay = {};
		std::vector<double> vec_c_gggdau_b_decay = {};
		std::vector<double> vec_c_gggdau_nonb_decay = {};
		std::vector<double> vec_c_b_decay = {};
		*/
		std::vector<double> vec_c_nonb_decay = {};
		std::vector<double> vec_c_nonb_dR_dau = {};
		std::vector<double> vec_c_nonb_dR_gdau = {};
		/*
		std::vector<int> vec_c_nonb_pdgID = {};
		std::vector<int> vec_c_nonb_ndaus = {};
		std::vector<int> vec_c_nonb_parent_pdgID = {};
		*/
		//bool has_weird_b = false;

		if (mci->primaries().size() == 2 and mci->secondaries().size() == 4) {
			
			for (auto p : mci->secondaries()) {
				
				//bool has_one_match_bvtx = false;
				std::vector<int> vec_dau_btag = {};
				if (p->numberOfDaughters() == 0)
					continue;

				//std::cout << __LINE__ << std::endl;
				Is_bdecay_done(1, p, p, vec_dau_btag, vec_c_nonb_dR_dau, vec_c_nonb_dR_gdau, vec_c_nonb_decay);
				/*
				if (std::count(vec_dau_btag.begin(), vec_dau_btag.end(), 5.0) > 3)
					has_weird_b = true;
				
					std::cout << "investigating a b-chain w/ all b-quarks in the chain " << std::endl;
					for (size_t n = 0, ne = vec_c_nonb_decay.size(); n < ne; ++n) {
						std::cout << " displ (cm) " << vec_c_nonb_decay[n] << std::endl;
					}
					for (size_t n = 0, ne = vec_c_nonb_dR_dau.size(); n < ne; ++n) {
						h_dR_valid_dau->Fill(vec_c_nonb_dR_dau[n]);
						std::cout << " dau dR " << vec_c_nonb_dR_dau[n] << std::endl;
					}
					print_bchain(1, p);
				}
				*/
			
				//std::cout << __LINE__ << std::endl;
				//auto can_dau = p;
				/*
				for (size_t i = 0, ie = p->numberOfDaughters(); i < ie; ++i) {
					// gdau stage
					auto gdau = p->daughter(i);   
					double dau_dR = reco::deltaR(gdau->eta(), gdau->phi(), p->eta(), p->phi());
					if (valid_dau(p, (reco::GenParticle*)gdau, 100.0) == nullptr)
						continue;
					int gdau_pdgID = gdau->pdgId();
					double gdau_dist3d = sqrt(pow(gdau->vx() - p->vx(), 2) + pow(gdau->vy() - p->vy(), 2) + pow(gdau->vz() - p->vz(), 2));
					int gdau_btag = 0;
					if (isBhadron(gdau_pdgID)) {
						h_gdau_bhadrons_pdgID->Fill(gdau_pdgID);
						h_gdau_bhadrons_dist3d_from_llp->Fill(gdau_dist3d);
						gdau_btag = 5;
						if (isBvtx(gdau_pdgID, gdau_dist3d)) {
							vec_c_gdau_b_decay.push_back(gdau_dist3d);
							vec_c_b_decay.push_back(gdau_dist3d);
							h_gdau_select_edge_b_decay_dist3d_from_llp->Fill(gdau_dist3d);
						}
					}
					else {
						h_gdau_nonbhadrons_pdgID->Fill(gdau_pdgID);
						h_gdau_nonbhadrons_dist3d_from_llp->Fill(gdau_dist3d);
						gdau_btag = 999;
						if (isBvtx(gdau_pdgID, gdau_dist3d) && has_one_match_bvtx == false) {
							has_one_match_bvtx = true;
							vec_c_gdau_nonb_decay.push_back(gdau_dist3d);
							vec_c_nonb_dR_dau.push_back(dau_dR);
							vec_c_nonb_decay.push_back(gdau_dist3d);
							vec_c_nonb_pdgID.push_back(gdau_pdgID);
							vec_c_nonb_ndaus.push_back(gdau->numberOfDaughters());
							vec_c_nonb_parent_pdgID.push_back(p->pdgId());
							h_gdau_select_b_decay_dist3d_from_llp->Fill(gdau_dist3d);
							
						}
					}

					for (size_t j = 0, je = p->daughter(i)->numberOfDaughters(); j < je; ++j) {
						// ggdau stage
						auto ggdau = p->daughter(i)->daughter(j);
						if (valid_dau(gdau, (reco::GenParticle*)ggdau, 100.0) == nullptr)
							continue;
						int ggdau_pdgID = ggdau->pdgId();
						int ggdau_btag = 0;
						double ggdau_dist3d = sqrt(pow(ggdau->vx() - p->vx(), 2) + pow(ggdau->vy() - p->vy(), 2) + pow(ggdau->vz() - p->vz(), 2));
						if (isBhadron(ggdau_pdgID)) {
							h_ggdau_bhadrons_pdgID->Fill(ggdau_pdgID);
							h_ggdau_bhadrons_dist3d_from_llp->Fill(ggdau_dist3d);
							ggdau_btag = 5;
							if (isBvtx(ggdau_pdgID, ggdau_dist3d)) {
								if (gdau_btag == 5) {
									vec_c_b_decay.push_back(ggdau_dist3d);
									vec_c_ggdau_b_decay.push_back(ggdau_dist3d);
									h_ggdau_select_edge_b_decay_dist3d_from_llp->Fill(ggdau_dist3d);
								}
							}
						}
						else {
							h_ggdau_nonbhadrons_pdgID->Fill(ggdau_pdgID);
							h_ggdau_nonbhadrons_dist3d_from_llp->Fill(ggdau_dist3d);
							ggdau_btag = 999;
							if (isBvtx(ggdau_pdgID, ggdau_dist3d) && has_one_match_bvtx == false) {
								if (gdau_btag == 5) {
									has_one_match_bvtx = true;
									vec_c_nonb_decay.push_back(ggdau_dist3d);
									vec_c_nonb_dR_dau.push_back(dau_dR);
									vec_c_nonb_pdgID.push_back(ggdau_pdgID);
									vec_c_nonb_ndaus.push_back(ggdau->numberOfDaughters());
									vec_c_nonb_parent_pdgID.push_back(gdau_pdgID);
									vec_c_ggdau_nonb_decay.push_back(ggdau_dist3d);
									h_ggdau_select_b_decay_dist3d_from_llp->Fill(ggdau_dist3d);
									
								}
							}
						}

						for (size_t k = 0, ke = p->daughter(i)->daughter(j)->numberOfDaughters(); k < ke; ++k) {
							// gggdau stage
							auto gggdau = p->daughter(i)->daughter(j)->daughter(k);
							if (valid_dau(ggdau, (reco::GenParticle*)gggdau, 100.0) == nullptr)
								continue;
							int gggdau_pdgID = gggdau->pdgId();
							double gggdau_dist3d = sqrt(pow(gggdau->vx() - p->vx(), 2) + pow(gggdau->vy() - p->vy(), 2) + pow(gggdau->vz() - p->vz(), 2));
							if (isBhadron(gggdau_pdgID)) {
								h_gggdau_bhadrons_pdgID->Fill(gggdau_pdgID);
								h_gggdau_bhadrons_dist3d_from_llp->Fill(gggdau_dist3d);
								if (isBvtx(gggdau_pdgID, gggdau_dist3d)) {
									if (ggdau_btag == 5 && gdau_btag == 5) {
										vec_c_b_decay.push_back(gggdau_dist3d);
										vec_c_gggdau_b_decay.push_back(gggdau_dist3d);
										h_gggdau_select_edge_b_decay_dist3d_from_llp->Fill(gggdau_dist3d);
									}
								}

								if (ggdau_btag == 5 && gdau_btag == 5)
									h_gggdau_for_ggggdau_bhadrons_pdgID->Fill(gggdau->pdgId());
							}
							else {
								h_gggdau_nonbhadrons_pdgID->Fill(gggdau_pdgID);
								h_gggdau_nonbhadrons_dist3d_from_llp->Fill(gggdau_dist3d);
								if (isBvtx(gggdau_pdgID, gggdau_dist3d) && has_one_match_bvtx == false) {
									if (ggdau_btag == 5 && gdau_btag == 5) {
										has_one_match_bvtx = true;
										vec_c_nonb_decay.push_back(gggdau_dist3d);
										vec_c_nonb_dR_dau.push_back(dau_dR);
										vec_c_nonb_pdgID.push_back(gggdau_pdgID);
										vec_c_nonb_ndaus.push_back(gggdau->numberOfDaughters());
										vec_c_nonb_parent_pdgID.push_back(ggdau_pdgID);
										vec_c_gggdau_nonb_decay.push_back(gggdau_dist3d);
										h_gggdau_select_b_decay_dist3d_from_llp->Fill(gggdau_dist3d);
										
									}
                                                              
								}
								    
							}
							
						}
					}
				}
				*/
			}
		}

		
		if (vec_c_nonb_decay.size() != 4) {
			std::cout << "investigating events w/ # of GEN b-vertices of " << vec_c_nonb_decay.size() << std::endl;
			for (size_t n = 0, ne = vec_c_nonb_decay.size(); n < ne; ++n) {
				std::cout << " displ (cm) " << vec_c_nonb_decay[n] << std::endl;
			}
			std::cout << "min dR from b-quark to its daus" << std::endl;
			for (size_t n = 0, ne = vec_c_nonb_dR_dau.size(); n < ne; ++n) {
				h_missing_dau_to_gdau_mindR->Fill(vec_c_nonb_dR_dau[n]);
				std::cout << " dau dR " << vec_c_nonb_dR_dau[n] << std::endl;
			}
			std::cout << "min dR from b-quark daus to its gdaus" << std::endl;
			for (size_t n = 0, ne = vec_c_nonb_dR_gdau.size(); n < ne; ++n) {
				h_missing_gdau_to_ggdau_mindR->Fill(vec_c_nonb_dR_dau[n]);
				std::cout << " gdau dR " << vec_c_nonb_dR_gdau[n] << std::endl;
			}
			for (auto p : mci->secondaries()) {
				std::cout << "dau " << " id " << p->pdgId() << " #gdaus " << p->numberOfDaughters() << " pt " << p->pt() << " eta " << p->eta() << " phi " << p->phi() << " mass " << p->mass() << std::endl;
				for (size_t i = 0, ie = p->numberOfDaughters(); i < ie; ++i) {
					
					auto gdau = p->daughter(i);
					double dau_dR = reco::deltaR(gdau->eta(), gdau->phi(), p->eta(), p->phi());

					double gdau_dist3d = sqrt(pow(gdau->vx() - p->vx(), 2) + pow(gdau->vy() - p->vy(), 2) + pow(gdau->vz() - p->vz(), 2));
					std::cout << "    gdau " << " displ (cm) " << gdau_dist3d << " id " << gdau->pdgId() << " #ggdaus " << gdau->numberOfDaughters() <<  " pt " << gdau->pt() << " eta " << gdau->eta() << " phi " << gdau->phi() << " mass " << gdau->mass() << std::endl;
					std::cout << "    gdau dR " << dau_dR << std::endl;
					for (size_t j = 0, je = gdau->numberOfDaughters(); j < je; ++j) {
						auto ggdau = gdau->daughter(j);
						double gdau_dR = reco::deltaR(ggdau->eta(), ggdau->phi(), gdau->eta(), gdau->phi());

						double ggdau_dist3d = sqrt(pow(ggdau->vx() - p->vx(), 2) + pow(ggdau->vy() - p->vy(), 2) + pow(ggdau->vz() - p->vz(), 2));
						std::cout << "        ggdau " << " displ (cm) " << ggdau_dist3d << " id " << ggdau->pdgId() << " #gggdaus " << ggdau->numberOfDaughters() << " pt " << ggdau->pt() << " eta " << ggdau->eta() << " phi " << ggdau->phi() << " mass " << ggdau->mass() << std::endl;
						std::cout << "        ggdau dR " << gdau_dR << std::endl;
						for (size_t k = 0, ke = ggdau->numberOfDaughters(); k < ke; ++k) {
							auto gggdau = ggdau->daughter(k);
							double gggdau_dist3d = sqrt(pow(gggdau->vx() - p->vx(), 2) + pow(gggdau->vy() - p->vy(), 2) + pow(gggdau->vz() - p->vz(), 2));
							std::cout << "           gggdau " << " displ (cm) " << gggdau_dist3d << " id " << gggdau->pdgId() << " #ggggdaus " << gggdau->numberOfDaughters() << " pt " << gggdau->pt() << " eta " << gggdau->eta() << " phi " << gggdau->phi() << " mass " << gggdau->mass() << std::endl;
							for (size_t l = 0, le = gggdau->numberOfDaughters(); l < le; ++l) {
								auto ggggdau = gggdau->daughter(l);
								double ggggdau_dist3d = sqrt(pow(ggggdau->vx() - p->vx(), 2) + pow(ggggdau->vy() - p->vy(), 2) + pow(ggggdau->vz() - p->vz(), 2));
								std::cout << "                ggggdau " << " displ (cm) " << ggggdau_dist3d << " id " << gggdau->pdgId() << " #gggggdaus " << ggggdau->numberOfDaughters() << " pt " << ggggdau->pt() << " eta " << ggggdau->eta() << " phi " << ggggdau->phi() << " mass " << ggggdau->mass() << std::endl;
								for (size_t m = 0, me = ggggdau->numberOfDaughters(); m < me; ++m) {
									auto gggggdau = ggggdau->daughter(m);
									double gggggdau_dist3d = sqrt(pow(gggggdau->vx() - p->vx(), 2) + pow(gggggdau->vy() - p->vy(), 2) + pow(gggggdau->vz() - p->vz(), 2));
									std::cout << "                   gggggdau " << " displ (cm) " << gggggdau_dist3d << " id " << gggggdau->pdgId() << " ggggggdaus " << gggggdau->numberOfDaughters() << " pt " << gggggdau->pt() << " eta " << gggggdau->eta() << " phi " << gggggdau->phi() << " mass " << gggggdau->mass() << std::endl;
									for (size_t n = 0, ne = gggggdau->numberOfDaughters(); n < ne; ++n) {
										auto ggggggdau = gggggdau->daughter(n);
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
		
		h_n_gen_bvtx->Fill(vec_c_nonb_decay.size());
		/*
		h_gdau_n_b_decay_points->Fill(vec_c_gdau_b_decay.size());
		h_gdau_n_non_b_decay_points->Fill(vec_c_gdau_nonb_decay.size());
		h_ggdau_n_b_decay_points->Fill(vec_c_ggdau_b_decay.size());
		h_ggdau_n_non_b_decay_points->Fill(vec_c_ggdau_nonb_decay.size());
		h_gggdau_n_b_decay_points->Fill(vec_c_gggdau_b_decay.size());
		h_gggdau_n_non_b_decay_points->Fill(vec_c_gggdau_nonb_decay.size());
		*/
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
	return (int(fabs(pdgID)/100) % 10) == 5 || (int(fabs(pdgID) / 1000) % 10) == 5;
}

bool MFVGenHistos::isBquark(int pdgID) {
	return fabs(pdgID) == 5;
}

bool MFVGenHistos::isBvtx(int pdgID, double dist3d, std::vector<int> vec_btag) {
	
    for (size_t i = 0, ie = vec_btag.size() - 1; i < ie; ++i) {
		if (!(abs(vec_btag[i]) == 5 || (vec_btag[i] == 21 && vec_btag[i+1] == -5)))
			return false;
	}
	
		
	return dist3d > 0 && fabs(pdgID) != 11;
}

reco::GenParticle* MFVGenHistos::valid_dau(auto parent, reco::GenParticle* dau, double thes_dR) {
	double dau_dR = reco::deltaR(dau->eta(), dau->phi(), parent->eta(), parent->phi());
	//h_dR_valid_dau->Fill(dau_dR);
	if (dau_dR < thes_dR)
		return dau;
	else
		return nullptr;
}

size_t MFVGenHistos::mindR_dau(int nth_chain, auto parent, std::vector<double>& vec_first_dR, std::vector<double>& vec_second_dR) {
	double mindR = 200;
	size_t idx_mindR = 0;
	for (size_t i = 0, ie = parent->numberOfDaughters(); i < ie; ++i) {
		auto dau = parent->daughter(i);
	    double dau_dR = reco::deltaR(dau->eta(), dau->phi(), parent->eta(), parent->phi());
		if (dau_dR < mindR) {
			mindR = dau_dR;
			idx_mindR = i;
		}
	}
	if (nth_chain == 1) {
		vec_first_dR.push_back(mindR);
		h_dau_to_gdau_mindR->Fill(mindR);
	}
	if (nth_chain == 2) {
		vec_second_dR.push_back(mindR);
		h_gdau_to_ggdau_mindR->Fill(mindR);
	}
	return idx_mindR;
}

void MFVGenHistos::print_bchain(int num, auto init_p) {

		for (size_t i = 0, ie = init_p->numberOfDaughters(); i < ie; ++i) {
			auto dau = init_p->daughter(i);
			double dau_dist3d = sqrt(pow(dau->vx() - init_p->vx(), 2) + pow(dau->vy() - init_p->vy(), 2) + pow(dau->vz() - init_p->vz(), 2));
			std::cout << "g x " << num << " dau " << " displ (cm) " << dau_dist3d << " id " << dau->pdgId() << " #daus " << dau->numberOfDaughters() << " pt " << dau->pt() << " eta " << dau->eta() << " phi " << dau->phi() << " mass " << dau->mass() << std::endl;
			if (dau_dist3d == 0.0)
				print_bchain(num + 1, dau);
		}
		return;
}


bool MFVGenHistos::Is_bdecay_done(int nth_chain, const reco::GenParticleRef& bquark, auto parent, std::vector<int>& vec_btag, std::vector<double>& vec_first_dR, std::vector<double>& vec_second_dR, std::vector<double>& vec_decay) {

	for (size_t i = 0, ie = parent->numberOfDaughters(); i < ie; ++i) {
		// gdau stage
		if ((nth_chain == 1  && (i != mindR_dau(nth_chain, parent, vec_first_dR, vec_second_dR))) || (nth_chain == 2 && (i != mindR_dau(nth_chain, parent, vec_first_dR, vec_second_dR))))
			 continue;
		auto dau = parent->daughter(i);
		//double dau_dR = reco::deltaR(dau->eta(), dau->phi(), bquark->eta(), bquark->phi());
		//if (valid_dau(parent, (reco::GenParticle*)dau, 100.0) == nullptr)
		//	continue;
		int dau_pdgID = dau->pdgId();
		double dau_dist3d = sqrt(pow(dau->vx() - bquark->vx(), 2) + pow(dau->vy() - bquark->vy(), 2) + pow(dau->vz() - bquark->vz(), 2));
		
		if (isBhadron(dau_pdgID)) {
			vec_btag.push_back(-5);
			if (isBvtx(dau_pdgID, dau_dist3d, vec_btag)) {
				vec_decay.push_back(dau_dist3d);
				h_dau_select_edge_b_decay_dist3d_from_llp->Fill(dau_dist3d);
				break;
			}
		}
		else if (isBquark(dau_pdgID)) {
			vec_btag.push_back(5);
			/*
			if (isBvtx(dau_pdgID, dau_dist3d, vec_btag)) {
				h_dau_select_edge_b_decay_dist3d_from_llp->Fill(dau_dist3d);
			}
			*/
		}
		else if (dau_pdgID == 21) {
			vec_btag.push_back(21);
		}
		else {
			vec_btag.push_back(999);
			if (isBvtx(dau_pdgID, dau_dist3d, vec_btag)) {
				vec_decay.push_back(dau_dist3d);
				h_dau_select_b_decay_dist3d_from_llp->Fill(dau_dist3d);
				break;
			}
			
		}
		
		return Is_bdecay_done(nth_chain+1,bquark, dau, vec_btag, vec_first_dR, vec_second_dR, vec_decay);
	}
	
	return true;
}

DEFINE_FWK_MODULE(MFVGenHistos);
