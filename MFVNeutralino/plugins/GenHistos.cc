#include "TH1F.h"
#include "TH2F.h"
#include "TLorentzVector.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "SimGeneral/HepPDTRecord/interface/ParticleDataTable.h"
#include "JMTucker/MFVNeutralino/interface/MCInteractionMFV3j.h"
#include "JMTucker/MFVNeutralino/interface/MCInteractionXX4j.h"
#include "JMTucker/MFVNeutralino/interface/MCInteractionLQ.h"
#include "JMTucker/Tools/interface/MCInteractionTops.h"
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
  const bool check_all_gen_particles;
  bool mci_warned;
  enum mci_mode_t { mci_invalid, mci_mfv3j, mci_xx4j, mci_lq, mci_ttbar };
  const std::string mci_mode_str;
  mci_mode_t mci_mode;

  edm::ESHandle<ParticleDataTable> pdt;

  TH1F* NumLeptons;
  TH2F* DecayType;
  TH1F* TopDaughterIds[2];
  TH2F* WDaughterIds[2];

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

  TH1F* h_lsp_dist2d;
  TH1F* h_lsp_dist3d;
  TH1F* h_lsp_angle2;
  TH1F* h_lsp_angle3;

  TH2F* h_vtx[9];
  TH1F* h_r2d[9];
  TH1F* h_r3d[9];
  TH1F* h_t;
  TH1F* h_ct;
  TH1F* h_ctau;
  TH2F* h_r3d_bhadron_v_bquark;
  TH1F* h_lspbeta;
  TH1F* h_lspbetagamma;
  TH1F* h_max_dR;
  TH1F* h_min_dR;
  TH2F* h_max_dR_vs_lspbeta;
  TH2F* h_min_dR_vs_lspbeta;
  TH2F* h_max_dR_vs_lspbetagamma;
  TH2F* h_min_dR_vs_lspbetagamma;
  TH1F* h_lsp_daughters_pt;
  TH1F* h_lsp_daughters_eta;
  TH1F* h_lsp_daughters_dxy;
  TH2F* h_lsp_daughters_dxy_dBV;
  TH1F* h_lsp_max_dR;
  TH1F* h_lsp_min_dR;
  TH1F* h_lsp_daughters_jets_dR;
  TH1F* h_lsp_daughters_jets_nmatch;
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

  TH1F* h_npartons_in_acc;

  TH1F* h_npartons_60;
  TH1F* h_njets_60;
  TH1F* h_ht_20;

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
    check_all_gen_particles(cfg.getParameter<bool>("check_all_gen_particles")),
    mci_warned(false),
    mci_mode_str(cfg.getParameter<std::string>("mci_mode"))
{
  if (mci_mode_str == "mfv3j")
    mci_mode = mci_mfv3j;
  else if (mci_mode_str == "xx4j")
    mci_mode = mci_xx4j;
  else if (mci_mode_str == "lq")
    mci_mode = mci_lq;
  else if (mci_mode_str == "ttbar")
    mci_mode = mci_ttbar;
  else
    mci_mode = mci_invalid;

  edm::Service<TFileService> fs;

  NumLeptons = fs->make<TH1F>("NumLeptons", "", 3, 0, 3);
  NumLeptons->SetTitle(";number of leptons from top decays;events");
  DecayType = fs->make<TH2F>("DecayType", "", 6, 0, 6, 6, 0, 6);
  DecayType->SetTitle(";decay mode 0;decay mode 1");

  TopDaughterIds[0] = fs->make<TH1F>("TopDaughterIds",    "top daughter ids",    15, 0, 15);
  TopDaughterIds[1] = fs->make<TH1F>("TopbarDaughterIds", "topbar daughter ids", 15, 0, 15);
  const char* TopDaughterIdLabels[] = { "W+", "W-", "b", "bbar", "g", "u", "ubar", "d", "dbar", "s", "sbar" , "c", "cbar", "gamma", "N/A" };
  for (int i = 0; i < 2; ++i)
    set_bin_labels(TopDaughterIds[i]->GetXaxis(), TopDaughterIdLabels);

  WDaughterIds[0] = fs->make<TH2F>("WplusDaughterIds",  "W+ daughter ids", 25, 0, 25, 25, 0, 25);
  WDaughterIds[1] = fs->make<TH2F>("WminusDaughterIds", "W- daughter ids", 25, 0, 25, 25, 0, 25);
  const char* WDaughterIdLabels[] = { "d", "u", "s", "c", "b", "dbar", "ubar", "sbar", "cbar", "bbar", "e-", "nu_e", "mu-", "nu_mu", "tau-", "nu_tau", "e+", "nu_ebar", "mu+", "nu_mubar", "tau+", "nu_taubar", "W+", "W-", "N/A" };
  for (int i = 0; i < 2; ++i) {
    set_bin_labels(WDaughterIds[i]->GetXaxis(), WDaughterIdLabels);
    set_bin_labels(WDaughterIds[i]->GetYaxis(), WDaughterIdLabels);
  }

  bkh_factory = new BasicKinematicHistsFactory(fs);

  for (int i = 0; i < 2; ++i) {
    Hs[i] = bkh_factory->make(TString::Format("Hs#%i", i), TString::Format("H #%i", i));
    Hs[i]->BookE (200, 0, 2000, "10");
    Hs[i]->BookP (200, 0, 2000, "10");
    Hs[i]->BookPt(200, 0, 2000, "10");
    Hs[i]->BookPz(200, 0, 2000, "10");
    Hs[i]->BookM (200, 0, 2000, "10");
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
    Lsps[i]->BookE (200, 0, 2000, "10");
    Lsps[i]->BookP (200, 0, 2000, "10");
    Lsps[i]->BookPt(200, 0, 2000, "10");
    Lsps[i]->BookPz(200, 0, 2000, "10");
    Lsps[i]->BookM (200, 0, 2000, "10");
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

  h_lsp_dist2d = fs->make<TH1F>("h_lsp_dist2d", ";2D distance between LSP decay positions (cm);Events/0.0025 cm", 4000, 0, 10);
  h_lsp_dist3d = fs->make<TH1F>("h_lsp_dist3d", ";3D distance between LSP decay positions (cm);Events/0.0025 cm", 4000, 0, 10);

  h_lsp_angle2 = fs->make<TH1F>("h_lsp_angle2", ";cos(angle in r-#phi plane) between LSP momenta;Events/0.01", 202, -1.01, 1.01);
  h_lsp_angle3 = fs->make<TH1F>("h_lsp_angle3", ";cos(3D angle) between LSP momenta;Events/0.01", 202, -1.01, 1.01);

  const char* names[9] = {"lsp", "strange", "bottom", "bhadron", "from21", "from22", "fromq", "from21only", "from22only"};
  for (int i = 0; i < (check_all_gen_particles ? 9 : 4); ++i) {
    h_vtx[i] = fs->make<TH2F>(TString::Format("h_vtx_%s", names[i]), TString::Format(";%s vx (cm); %s vy (cm)", names[i], names[i]), 200, -1, 1, 200, -1, 1);
    h_r2d[i] = fs->make<TH1F>(TString::Format("h_r2d_%s", names[i]), TString::Format(";%s 2D distance (cm);Events/0.01 cm", names[i]), 500, 0, 5);
    h_r3d[i] = fs->make<TH1F>(TString::Format("h_r3d_%s", names[i]), TString::Format(";%s 3D distance (cm);Events/0.01 cm", names[i]), 500, 0, 5);
  }

  h_t = fs->make<TH1F>("h_t", ";time to LSP decay (ns);Events/0.1 ns", 100, 0, 10);
  h_ct = fs->make<TH1F>("h_ct", ";ct to LSP decay (#mum);Events/10 #mum", 2000, 0, 20000);
  h_ctau = fs->make<TH1F>("h_ctau", ";c#tau to LSP decay (#mum);Events/10 #mum", 1000, 0, 10000);
  h_r3d_bhadron_v_bquark = fs->make<TH2F>("h_r3d_bhadron_v_bquark", ";b quark 3D distance (cm);b hadron 3D distance (cm)", 100, 0, 2, 100, 0, 2);
  h_lspbeta = fs->make<TH1F>("h_lspbeta", ";LSP #beta;Events/0.01", 100, 0, 1);
  h_lspbetagamma = fs->make<TH1F>("h_lspbetagamma", ";LSP #beta#gamma;Events/0.1", 100, 0, 10);

  h_max_dR = fs->make<TH1F>("h_max_dR", ";max #DeltaR between partons;Events/0.05", 100, 0, 5);
  h_min_dR = fs->make<TH1F>("h_min_dR", ";min #DeltaR between partons;Events/0.05", 100, 0, 5);
  h_max_dR_vs_lspbeta = fs->make<TH2F>("h_max_dR_vs_lspbeta", ";LSP #beta;max #DeltaR between partons", 100, 0, 1, 100, 0, 5);
  h_min_dR_vs_lspbeta = fs->make<TH2F>("h_min_dR_vs_lspbeta", ";LSP #beta;min #DeltaR between partons", 100, 0, 1, 100, 0, 5);
  h_max_dR_vs_lspbetagamma = fs->make<TH2F>("h_max_dR_vs_lspbetagamma", ";LSP #beta#gamma;max #DeltaR between partons", 100, 0, 10, 100, 0, 5);
  h_min_dR_vs_lspbetagamma = fs->make<TH2F>("h_min_dR_vs_lspbetagamma", ";LSP #beta#gamma;min #DeltaR between partons", 100, 0, 10, 100, 0, 5);
  h_lsp_daughters_pt = fs->make<TH1F>("h_lsp_daughters_pt", ";p_{T} of partons (GeV);LSP daughter partons/1 GeV", 500, 0, 500);
  h_lsp_daughters_eta = fs->make<TH1F>("h_lsp_daughters_eta", ";#eta of partons;LSP daughter partons/0.16", 50, -4, 4);
  h_lsp_daughters_dxy = fs->make<TH1F>("h_lsp_daughters_dxy", ";dxy of partons;LSP daughter partons/10 #mum", 400, -0.2, 0.2);
  h_lsp_daughters_dxy_dBV = fs->make<TH2F>("h_lsp_daughters_dxy_dBV", ";LSP 2D distance;dxy of partons", 500, 0, 5, 400, -0.2, 0.2);
  h_lsp_max_dR = fs->make<TH1F>("h_lsp_max_dR", ";max #DeltaR between partons;Events/0.05", 100, 0, 5);
  h_lsp_min_dR = fs->make<TH1F>("h_lsp_min_dR", ";min #DeltaR between partons;Events/0.05", 100, 0, 5);
  h_lsp_daughters_jets_dR = fs->make<TH1F>("h_lsp_daughters_jets_dR", ";#DeltaR between partons and jets;parton-jet pairs/0.05", 100, 0, 5);
  h_lsp_daughters_jets_nmatch = fs->make<TH1F>("h_lsp_daughters_jets_nmatch", ";number of genJets w/ #DeltaR < 0.4;LSP daughter partons", 10, 0, 10);
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
  h_bquarks_pt = fs->make<TH1F>("h_bquarks_pt", ";b quarks p_{T} (GeV);arb. units", 200, 0, 2000);
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

  h_npartons_in_acc = fs->make<TH1F>("h_npartons_in_acc", ";number of LSP daughters in acceptance;Events", 11, 0, 11);
  h_npartons_60 = fs->make<TH1F>("h_npartons_60", ";number of partons with E_{T} > 60 GeV;Events", 11, 0, 11);
  h_njets_60 = fs->make<TH1F>("h_njets_60", ";number of jets with E_{T} > 60 GeV;Events", 11, 0, 11);
  h_ht_20 = fs->make<TH1F>("h_ht_20", ";#SigmaH_{T} of jets with E_{T} > 20 GeV;Events", 100, 0, 2000);

  NJets = fs->make<TH1F>("NJets", ";number of jets;Events", 30, 0, 30);
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

namespace {
  float mag(float x, float y) {
    return sqrt(x*x + y*y);
  }
  
  float mag(float x, float y, float z) {
    return sqrt(x*x + y*y + z*z);
  }
  
  float signed_mag(float x, float y) {
    float m = mag(x,y);
    if (y < 0) return -m;
    return m;
  }
}

void MFVGenHistos::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  setup.getData(pdt);

  edm::Handle<reco::GenParticleCollection> gen_particles;
  event.getByToken(gen_token, gen_particles);

  edm::Handle<reco::GenJetCollection> gen_jets;
  event.getByToken(gen_jet_token, gen_jets);

  const reco::GenParticle& for_vtx = gen_particles->at(2);
  const int for_vtx_id = abs(for_vtx.pdgId());
  die_if_not(for_vtx_id == 21 || (for_vtx_id >= 1 && for_vtx_id <= 5), "gen_particles[2] is not a gluon or udscb: id=%i", for_vtx_id);
  float x0 = for_vtx.vx(), y0 = for_vtx.vy(), z0 = for_vtx.vz();
  auto fill = [x0,y0,z0](BasicKinematicHists* bkh, const reco::Candidate* c) {
    bkh->Fill(c);
    bkh->FillEx(signed_mag(c->vx() - x0, c->vy() - y0), c->vz() - z0, c->charge());
  };

  if (mci_mode == mci_mfv3j) { // JMTBAD mci_ttbar
    MCInteractionMFV3j mci;
    mci.Init(*gen_particles);
    if (!mci.Valid()) {
      if (!mci_warned)
        edm::LogWarning("GenHistos") << "MCInteractionMFV3j invalid; no further warnings!";
      mci_warned = true;
    }
    else {
      NumLeptons->Fill(mci.num_leptonic);
      DecayType->Fill(mci.decay_type[0], mci.decay_type[1]);

      for (int i = 0; i < 2; ++i) {
	// For debugging, record all the daughter ids for tops, stops, Ws.
	for (size_t j = 0, je = mci.last_tops[i]->numberOfDaughters(); j < je; ++j)
	  fill_by_label(TopDaughterIds[i], pdt->particle(mci.last_tops[i]->daughter(j)->pdgId())->name());
	fill_by_label(WDaughterIds[i], pdt->particle(mci.W_daughters[i][0]->pdgId())->name(), pdt->particle(mci.W_daughters[i][1]->pdgId())->name());

	fill(Lsps           [i], mci.lsps             [i]);
	fill(Stranges       [i], mci.stranges         [i]);
	fill(Bottoms        [i], mci.bottoms          [i]);
	fill(Tops           [i], mci.tops             [i]);
	fill(Ws             [i], mci.Ws               [i]);
	fill(BottomsFromTops[i], mci.bottoms_from_tops[i]);

	for (int j = 0; j < 2; ++j) {
	  const reco::Candidate* c = mci.W_daughters[i][j];
	  fill(WDaughters[i][j], c);
	  const int id = abs(c->pdgId());
	  if      (id == 11) { fill(Leptons, c); fill(LightLeptons, c); fill(Electrons, c); }
	  else if (id == 13) { fill(Leptons, c); fill(LightLeptons, c); fill(Muons,     c); }
	  else if (id == 15) { fill(Leptons, c);                        fill(Taus,      c); }
	}

	const reco::GenParticle& lsp = *mci.lsps[i];
	const int ndau = 3;
	const reco::GenParticle* daughters[ndau] = { mci.stranges[i], mci.bottoms[i], mci.tops[i] };

	const double lspbeta  = lsp.p()/lsp.energy();
	const double lspbetagamma = lspbeta/sqrt(1-lspbeta*lspbeta);
	h_lspbeta->Fill(lspbeta);
	h_lspbetagamma->Fill(lspbetagamma);

	// Fill some simple histos: 2D vertex location, and distance to
	// origin, and the min/max deltaR of the daughters (also versus
	// lsp boost).

	const reco::Candidate* particles[4] = { &lsp, mci.stranges[i], mci.bottoms[i], 0};
	// For that last one, find the b hadron for the primary b quark.
	std::vector<const reco::Candidate*> b_quark_descendants;
	const reco::Candidate* last_b_quark = final_candidate(mci.bottoms[i], 3);
	flatten_descendants(last_b_quark, b_quark_descendants);
	for (const reco::Candidate* bdesc : b_quark_descendants) {
	  if (is_bhadron(bdesc)) {
	    particles[3] = bdesc;
	    break;
	  }
	}
	die_if_not(particles[3] != 0, "did not find b hadron");
      
	float dx [4] = {0}; 
	float dy [4] = {0}; 
	float dz [4] = {0}; 
	float r2d[4] = {0};
	float r3d[4] = {0};
	for (int j = 0; j < 4; ++j) {
	  dx [j] = particles[j]->vx() - x0;
	  dy [j] = particles[j]->vy() - y0;
	  dz [j] = particles[j]->vz() - z0;
	  r2d[j] = mag(dx[j], dy[j]);
	  r3d[j] = mag(dx[j], dy[j], dz[j]);
	  h_vtx[j]->Fill(dx[j], dy[j]);
	  h_r2d[j]->Fill(r2d[j]);
	  h_r3d[j]->Fill(r3d[j]);
	}
      
	h_t->Fill(r3d[1]/lspbeta/30);
        h_ct->Fill(r3d[1]/lspbeta*10000);
        h_ctau->Fill(r3d[1]/lspbetagamma*10000);
	h_r3d_bhadron_v_bquark->Fill(r3d[2], r3d[3]);
	if (fabs(r3d[2] - r3d[3]) > 0.001) // 10 micron
          std::cout << "difference between bquark and bhadron r3ds is " << fabs(r3d[2] - r3d[3]) << " for run,lumi,event " << event.id().run() << ", " << event.luminosityBlock() << ", " << event.id().event() << "\n";
        
	if (check_all_gen_particles)
	  for (const auto& gen : *gen_particles) {
	    if (gen.status() == 1 && gen.charge() != 0 && mag(gen.vx(), gen.vy()) < 120 && abs(gen.vz()) < 300) {
	      const bool from21 = has_any_ancestor_with_id(&gen, 1000021);
	      const bool from22 = has_any_ancestor_with_id(&gen, 1000022);
	      const bool fromq = mci.Ancestor(&gen, "quark");
	      const float dx = gen.vx() - x0;
	      const float dy = gen.vy() - y0;
	      const float dz = gen.vz() - z0;
	      const float r2d = mag(dx, dy);
	      const float r3d = mag(dx, dy, dz);
	      std::vector<int> tofill;
	      h_status1origins->Fill((from21*4) | (from22*2) | (fromq*1));
	      if (from21) tofill.push_back(4);
	      if (from22) tofill.push_back(5);
	      if (fromq)  tofill.push_back(6);
	      if (from21 && !from22 && !fromq) tofill.push_back(7);
	      if (from22 && !from21 && !fromq) tofill.push_back(8);
	      for (int j : tofill) {
		h_vtx[j]->Fill(dx, dy);
		h_r2d[j]->Fill(r2d);
		h_r3d[j]->Fill(r3d);
	      }
	    }
	  }

	float min_dR =  1e99;
	float max_dR = -1e99;
	for (int j = 0; j < ndau; ++j) {
	  for (int k = j+1; k < ndau; ++k) {
	    float dR = reco::deltaR(*daughters[j], *daughters[k]);
	    if (dR < min_dR)
	      min_dR = dR;
	    if (dR > max_dR)
	      max_dR = dR;
	  }
	}

	h_min_dR->Fill(min_dR);
	h_max_dR->Fill(max_dR);
	h_min_dR_vs_lspbeta->Fill(lspbeta, min_dR);
	h_max_dR_vs_lspbeta->Fill(lspbeta, max_dR);
	h_min_dR_vs_lspbetagamma->Fill(lspbetagamma, min_dR);
	h_max_dR_vs_lspbetagamma->Fill(lspbetagamma, max_dR);

        const int lsp_ndau = 5;
        const reco::GenParticle* lsp_daughters[lsp_ndau] = { mci.stranges[i], mci.bottoms[i], mci.bottoms_from_tops[i], mci.W_daughters[i][0], mci.W_daughters[i][1] };

        int lsp_ntracks = 0;
        float lsp_min_dR =  1e99;
        float lsp_max_dR = -1e99;
        for (int j = 0; j < lsp_ndau; ++j) {
          h_lsp_daughters_pt->Fill(lsp_daughters[j]->pt());
          h_lsp_daughters_eta->Fill(lsp_daughters[j]->eta());
          h_lsp_daughters_dxy->Fill(mag(mci.stranges[i]->vx() - mci.lsps[i]->vx(), mci.stranges[i]->vy() - mci.lsps[i]->vy()) * sin(lsp_daughters[j]->phi() - atan2(mci.stranges[i]->vy() - mci.lsps[i]->vy(), mci.stranges[i]->vx() - mci.lsps[i]->vx())));
          h_lsp_daughters_dxy_dBV->Fill(mag(mci.stranges[i]->vx() - mci.lsps[i]->vx(), mci.stranges[i]->vy() - mci.lsps[i]->vy()), mag(mci.stranges[i]->vx() - mci.lsps[i]->vx(), mci.stranges[i]->vy() - mci.lsps[i]->vy()) * sin(lsp_daughters[j]->phi() - atan2(mci.stranges[i]->vy() - mci.lsps[i]->vy(), mci.stranges[i]->vx() - mci.lsps[i]->vx())));

          int nmatch = 0;
          for (const reco::GenJet& jet : *gen_jets) {
            h_lsp_daughters_jets_dR->Fill(reco::deltaR(*lsp_daughters[j], jet));
            if (reco::deltaR(*lsp_daughters[j], jet) < 0.4) {
              ++nmatch;
            }
          }
          h_lsp_daughters_jets_nmatch->Fill(nmatch);

          if (is_neutrino(lsp_daughters[j]) || fabs(lsp_daughters[j]->eta()) > 2.5) continue;

          if (is_lepton(lsp_daughters[j])) {
           ++ lsp_ntracks;
          } else {
            for (const reco::GenJet& jet : *gen_jets) {
              if (reco::deltaR(*lsp_daughters[j], jet) < 0.4) {
                for (const reco::GenParticle* g : jet.getGenConstituents())
                  if (g->charge())
                    ++lsp_ntracks;
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

      h_lsp_dist2d->Fill(mag(mci.stranges[0]->vx() - mci.stranges[1]->vx(),
			     mci.stranges[0]->vy() - mci.stranges[1]->vy()));
      h_lsp_dist3d->Fill(mag(mci.stranges[0]->vx() - mci.stranges[1]->vx(),
			     mci.stranges[0]->vy() - mci.stranges[1]->vy(),
			     mci.stranges[0]->vz() - mci.stranges[1]->vz()));

      {
	TVector3 lsp_mom_0 = mci.p4_lsps[0].Vect();
	TVector3 lsp_mom_1 = mci.p4_lsps[1].Vect();
	h_lsp_angle3->Fill(lsp_mom_0.Dot(lsp_mom_1)/lsp_mom_0.Mag()/lsp_mom_1.Mag());
	lsp_mom_0.SetZ(0);
	lsp_mom_1.SetZ(0);
	h_lsp_angle2->Fill(lsp_mom_0.Dot(lsp_mom_1)/lsp_mom_0.Mag()/lsp_mom_1.Mag());
      }

      std::vector<const reco::GenParticle*> lsp_partons;
      for (int i = 0; i < 2; ++i) {
	lsp_partons.push_back(mci.stranges[i]);
	lsp_partons.push_back(mci.bottoms[i]);
	lsp_partons.push_back(mci.bottoms_from_tops[i]);
	if (mci.decay_type[i] == 3) {
	  lsp_partons.push_back(mci.W_daughters[i][0]);
	  lsp_partons.push_back(mci.W_daughters[i][1]);
	}
      } 

      int npartons_in_acc = 0;
      int npartons_60 = 0;
      for (const reco::GenParticle* p : lsp_partons) {
	if (p->pt() > 20 && fabs(p->eta()) < 2.5)
	  ++npartons_in_acc;
	if (p->pt() > 60 && fabs(p->eta()) < 2.5)
	  ++npartons_60;
      }
      h_npartons_in_acc->Fill(npartons_in_acc);
      h_npartons_60->Fill(npartons_60);
    }
  }
  else if (mci_mode == mci_xx4j) {
    MCInteractionXX4j mci;
    mci.Init(*gen_particles);
    if (!mci.Valid()) {
      if (!mci_warned)
        edm::LogWarning("GenHistos") << "MCInteractionXX4j invalid; no further warnings!";
      mci_warned = true;
    }
    else {
      DecayType->Fill(mci.decay_id[0], mci.decay_id[1]);

      for (int i = 0; i < 2; ++i) {
	fill(Hs[i], mci.hs[i]);
	for (int j = 0; j < 2; ++j)
	  fill(Qs[i][j], mci.qs[i][j]);

	const reco::GenParticle& lsp = *mci.hs[i];
	const int ndau = 2;
	const reco::GenParticle* daughters[2] = { mci.qs[i][0], mci.qs[i][1] };

	const double lspbeta  = lsp.p()/lsp.energy();
	const double lspbetagamma = lspbeta/sqrt(1-lspbeta*lspbeta);
	h_lspbeta->Fill(lspbeta);
	h_lspbetagamma->Fill(lspbetagamma);

	// Fill some simple histos: 2D vertex location, and distance to
	// origin, and the min/max deltaR of the daughters (also versus
	// lsp boost).

	const reco::Candidate* particles[3] = { &lsp, daughters[0], daughters[1] };
      
	float dx [3] = {0}; 
	float dy [3] = {0}; 
	float dz [3] = {0}; 
	float r2d[3] = {0};
	float r3d[3] = {0};
	for (int j = 0; j < 3; ++j) {
	  dx [j] = particles[j]->vx() - x0;
	  dy [j] = particles[j]->vy() - y0;
	  dz [j] = particles[j]->vz() - z0;
	  r2d[j] = mag(dx[j], dy[j]);
	  r3d[j] = mag(dx[j], dy[j], dz[j]);
	  h_vtx[j]->Fill(dx[j], dy[j]);
	  h_r2d[j]->Fill(r2d[j]);
	  h_r3d[j]->Fill(r3d[j]);
	}
      
	h_t->Fill(r3d[1]/lspbeta/30);
        h_ct->Fill(r3d[1]/lspbeta*10000);
        h_ctau->Fill(r3d[1]/lspbetagamma*10000);

	float min_dR =  1e99;
	float max_dR = -1e99;
	for (int j = 0; j < ndau; ++j) {
	  for (int k = j+1; k < ndau; ++k) {
	    float dR = reco::deltaR(*daughters[j], *daughters[k]);
	    if (dR < min_dR)
	      min_dR = dR;
	    if (dR > max_dR)
	      max_dR = dR;
	  }
	}

	h_min_dR->Fill(min_dR);
	h_max_dR->Fill(max_dR);
	h_min_dR_vs_lspbeta->Fill(lspbeta, min_dR);
	h_max_dR_vs_lspbeta->Fill(lspbeta, max_dR);
	h_min_dR_vs_lspbetagamma->Fill(lspbetagamma, min_dR);
	h_max_dR_vs_lspbetagamma->Fill(lspbetagamma, max_dR);
      }

      h_lsp_dist2d->Fill(mag(mci.qs[0][0]->vx() - mci.qs[0][1]->vx(),
			     mci.qs[0][0]->vy() - mci.qs[0][1]->vy()));
      h_lsp_dist3d->Fill(mag(mci.qs[0][0]->vx() - mci.qs[0][1]->vx(),
			     mci.qs[0][0]->vy() - mci.qs[0][1]->vy(),
			     mci.qs[0][0]->vz() - mci.qs[0][1]->vz()));

      {
	TVector3 lsp_mom_0 = mci.p4_hs[0].Vect();
	TVector3 lsp_mom_1 = mci.p4_hs[1].Vect();
	h_lsp_angle3->Fill(lsp_mom_0.Dot(lsp_mom_1)/lsp_mom_0.Mag()/lsp_mom_1.Mag());
	lsp_mom_0.SetZ(0);
	lsp_mom_1.SetZ(0);
	h_lsp_angle2->Fill(lsp_mom_0.Dot(lsp_mom_1)/lsp_mom_0.Mag()/lsp_mom_1.Mag());
      }

      std::vector<const reco::GenParticle*> lsp_partons;
      for (int i = 0; i < 2; ++i) {
	lsp_partons.push_back(mci.qs[0][i]);
      } 

      int npartons_in_acc = 0;
      int npartons_60 = 0;
      for (const reco::GenParticle* p : lsp_partons) {
	if (p->pt() > 20 && fabs(p->eta()) < 2.5)
	  ++npartons_in_acc;
	if (p->pt() > 60 && fabs(p->eta()) < 2.5)
	  ++npartons_60;
      }
      h_npartons_in_acc->Fill(npartons_in_acc);
      h_npartons_60->Fill(npartons_60);
    }
  }
  else if (mci_mode == mci_lq) {
    MCInteractionLQ mci;
    mci.Init(*gen_particles);
    if (!mci.Valid()) {
      if (!mci_warned)
        edm::LogWarning("GenHistos") << "MCInteractionLQ invalid; no further warnings!";
      mci_warned = true;
    }
    else {
      DecayType->Fill(mci.decay_id[0], mci.decay_id[1]);

      for (int i = 0; i < 2; ++i) {
	fill(Hs[i], mci.lqs[i]);
	for (int j = 0; j < 2; ++j)
	  fill(Qs[i][j], mci.daus[i][j]);

	const reco::GenParticle& lsp = *mci.lqs[i];
	const int ndau = 2;
	const reco::GenParticle* daughters[2] = { mci.daus[i][0], mci.daus[i][1] };

	const double lspbeta  = lsp.p()/lsp.energy();
	const double lspbetagamma = lspbeta/sqrt(1-lspbeta*lspbeta);
	h_lspbeta->Fill(lspbeta);
	h_lspbetagamma->Fill(lspbetagamma);

	// Fill some simple histos: 2D vertex location, and distance to
	// origin, and the min/max deltaR of the daughters (also versus
	// lsp boost).

	const reco::Candidate* particles[3] = { &lsp, daughters[0], daughters[1] };
      
	float dx [3] = {0}; 
	float dy [3] = {0}; 
	float dz [3] = {0}; 
	float r2d[3] = {0};
	float r3d[3] = {0};
	for (int j = 0; j < 3; ++j) {
	  dx [j] = particles[j]->vx() - x0;
	  dy [j] = particles[j]->vy() - y0;
	  dz [j] = particles[j]->vz() - z0;
	  r2d[j] = mag(dx[j], dy[j]);
	  r3d[j] = mag(dx[j], dy[j], dz[j]);
	  h_vtx[j]->Fill(dx[j], dy[j]);
	  h_r2d[j]->Fill(r2d[j]);
	  h_r3d[j]->Fill(r3d[j]);
	}
      
	h_t->Fill(r3d[1]/lspbeta/30);
	h_t->Fill(r3d[1]/lspbeta/30);
        h_ct->Fill(r3d[1]/lspbeta*10000);
        h_ctau->Fill(r3d[1]/lspbetagamma*10000);

	float min_dR =  1e99;
	float max_dR = -1e99;
	for (int j = 0; j < ndau; ++j) {
	  for (int k = j+1; k < ndau; ++k) {
	    float dR = reco::deltaR(*daughters[j], *daughters[k]);
	    if (dR < min_dR)
	      min_dR = dR;
	    if (dR > max_dR)
	      max_dR = dR;
	  }
	}

	h_min_dR->Fill(min_dR);
	h_max_dR->Fill(max_dR);
	h_min_dR_vs_lspbeta->Fill(lspbeta, min_dR);
	h_max_dR_vs_lspbeta->Fill(lspbeta, max_dR);
	h_min_dR_vs_lspbetagamma->Fill(lspbetagamma, min_dR);
	h_max_dR_vs_lspbetagamma->Fill(lspbetagamma, max_dR);
      }

      h_lsp_dist2d->Fill(mag(mci.daus[0][0]->vx() - mci.daus[1][0]->vx(),
			     mci.daus[0][0]->vy() - mci.daus[1][0]->vy()));
      h_lsp_dist3d->Fill(mag(mci.daus[0][0]->vx() - mci.daus[1][0]->vx(),
			     mci.daus[0][0]->vy() - mci.daus[1][0]->vy(),
			     mci.daus[0][0]->vz() - mci.daus[1][0]->vz()));

      {
	TVector3 lsp_mom_0 = mci.p4_lqs[0].Vect();
	TVector3 lsp_mom_1 = mci.p4_lqs[1].Vect();
	h_lsp_angle3->Fill(lsp_mom_0.Dot(lsp_mom_1)/lsp_mom_0.Mag()/lsp_mom_1.Mag());
	lsp_mom_0.SetZ(0);
	lsp_mom_1.SetZ(0);
	h_lsp_angle2->Fill(lsp_mom_0.Dot(lsp_mom_1)/lsp_mom_0.Mag()/lsp_mom_1.Mag());
      }

      std::vector<const reco::GenParticle*> lsp_partons;
      for (int i = 0; i < 2; ++i) {
	lsp_partons.push_back(mci.daus[0][i]);
      } 

      int npartons_in_acc = 0;
      int npartons_60 = 0;
      for (const reco::GenParticle* p : lsp_partons) {
	if (p->pt() > 20 && fabs(p->eta()) < 2.5)
	  ++npartons_in_acc;
	if (p->pt() > 60 && fabs(p->eta()) < 2.5)
	  ++npartons_60;
      }
      h_npartons_in_acc->Fill(npartons_in_acc);
      h_npartons_60->Fill(npartons_60);
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


  NJets->Fill(gen_jets->size());
  int nbjets = 0;
  int njets60 = 0;
  float ht = 0.0;
  for (const reco::GenJet& jet : *gen_jets) {
    int nchg = 0;
    int id = gen_jet_id(jet);
    int ntracksptgt3 = 0;
    for (const reco::GenParticle* g : jet.getGenConstituents()) {
      if (g->charge())
        ++nchg;
      if (g->charge() && g->pt() > 3)
        ++ntracksptgt3;
    }

    float fchg = float(nchg)/jet.nConstituents();

    if (jet.pt() > 60 && fabs(jet.eta()) < 2.5)
      ++njets60;
    if (jet.pt() > 20 && fabs(jet.eta()) < 2.5)
      ht = ht + jet.pt();;

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
  NBJets->Fill(nbjets);
  h_njets_60->Fill(njets60);
  h_ht_20->Fill(ht);
}

DEFINE_FWK_MODULE(MFVGenHistos);
