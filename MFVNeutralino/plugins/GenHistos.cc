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
#include "JMTucker/Tools/interface/MCInteractionTops.h"
#include "JMTucker/Tools/interface/BasicKinematicHists.h"
#include "JMTucker/Tools/interface/GenUtilities.h"
#include "JMTucker/Tools/interface/Utilities.h"

class MFVGenHistos : public edm::EDAnalyzer {
public:
  explicit MFVGenHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

private:
  const edm::InputTag gen_src;
  const edm::InputTag gen_jet_src;
  const bool check_all_gen_particles;
  bool mci_warned;
  const bool mci_bkg;

  edm::ESHandle<ParticleDataTable> pdt;

  TH1F* NumLeptons;
  TH2F* DecayType;
  TH1F* TopDaughterIds[2];
  TH2F* WDaughterIds[2];

  BasicKinematicHistsFactory* bkh_factory;

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
  TH2F* h_r3d_bhadron_v_bquark;
  TH1F* h_lspbeta;
  TH1F* h_lspbetagamma;
  TH1F* h_max_dR;
  TH1F* h_min_dR;
  TH2F* h_max_dR_vs_lspbeta;
  TH2F* h_min_dR_vs_lspbeta;
  TH2F* h_max_dR_vs_lspbetagamma;
  TH2F* h_min_dR_vs_lspbetagamma;

  TH1F* h_status1origins;

  TH2F* h_nbhadronsvsbquarks;
  TH2F* h_nbhadronsvsbquarks_wcuts;
  TH1F* h_nbquarks;
  TH1F* h_bquarks_pt;
  TH1F* h_bquarks_eta;
  TH1F* h_bquarks_phi;
  TH1F* h_bquarks_energy;

  TH1F* h_bquarks_absdphi[2];
  TH1F* h_bquarks_dphi[2];
  TH1F* h_bquarks_deta[2];
  TH2F* h_bquarks_deta_dphi[2];
  TH1F* h_bquarks_avgeta[2];
  TH2F* h_bquarks_avgeta_dphi[2];
  TH1F* h_bquarks_dR[2];
  TH2F* h_bquarks_dR_dphi[2];

  TH1F* h_npartons_in_acc;

  TH1F* h_npartons_60;
  TH1F* h_njets_60;
  TH1F* h_sumht_20;

  TH1F* NJets;
  BasicKinematicHists* Jets;
  TH1F* JetAuxE;
  TH1F* JetEmE;
  TH1F* JetHadE;
  TH1F* JetInvE;
  TH1F* JetNConstituents;
  TH1F* JetNChargedConst;
  TH1F* JetFChargedConst;

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
  : gen_src(cfg.getParameter<edm::InputTag>("gen_src")),
    gen_jet_src(cfg.getParameter<edm::InputTag>("gen_jet_src")),
    check_all_gen_particles(cfg.getParameter<bool>("check_all_gen_particles")),
    mci_warned(false),
    mci_bkg(cfg.getParameter<bool>("mci_bkg"))
{
  edm::Service<TFileService> fs;

  NumLeptons = fs->make<TH1F>("NumLeptons", "", 3, 0, 3);
  NumLeptons->SetTitle(";number of leptons from top decays;events");
  DecayType = fs->make<TH2F>("DecayType", "", 4, 0, 4, 4, 0, 4);
  DecayType->SetTitle(";W+ decay mode;W- decay mode");

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
    Stranges[i]->BookDz (200, -20, 20, "0.2");
    Stranges[i]->BookQ();

    Bottoms[i] = bkh_factory->make(TString::Format("Bottoms#%i", i), TString::Format("bottom #%i", i));
    Bottoms[i]->BookE (200, 0, 2000, "10");
    Bottoms[i]->BookP (200, 0, 2000, "10");
    Bottoms[i]->BookPt(200, 0, 2000, "10");
    Bottoms[i]->BookPz(200, 0, 2000, "10");
    Bottoms[i]->BookM (200, 0, 2000, "10");
    Bottoms[i]->BookRapEta(200, "0.1");
    Bottoms[i]->BookPhi(50, "0.125");
    Bottoms[i]->BookDxy(200, -2, 20, "0.02");
    Bottoms[i]->BookDz (200, -20, 20, "0.2");
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
    Tops[i]->BookDz (200, -20, 20, "0.2");
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
    Ws[i]->BookDz (200, -20, 20, "0.2");
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
    BottomsFromTops[i]->BookDz (200, -20, 20, "0.2");
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
      WDaughters[i][j]->BookDz (200, -20, 20, "0.2");
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
  Electrons->BookDz (200, -20, 20, "0.2");
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
  Muons->BookDz (200, -20, 20, "0.2");
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
  Taus->BookDz (200, -20, 20, "0.2");
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
  LightLeptons->BookDz (200, -20, 20, "0.2");
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
  Leptons->BookDz (200, -20, 20, "0.2");
  Leptons->BookQ();

  h_lsp_dist2d = fs->make<TH1F>("h_lsp_dist2d", ";2D distance between LSP decay positions (cm);Events/0.0025 cm", 400, 0, 1);
  h_lsp_dist3d = fs->make<TH1F>("h_lsp_dist3d", ";3D distance between LSP decay positions (cm);Events/0.0025 cm", 400, 0, 1);

  h_lsp_angle2 = fs->make<TH1F>("h_lsp_angle2", ";cos(angle in r-#phi plane) between LSP momenta;Events/0.01", 202, -1.01, 1.01);
  h_lsp_angle3 = fs->make<TH1F>("h_lsp_angle3", ";cos(3D angle) between LSP momenta;Events/0.01", 202, -1.01, 1.01);

  const char* names[9] = {"lsp", "strange", "bottom", "bhadron", "from21", "from22", "fromq", "from21only", "from22only"};
  for (int i = 0; i < (check_all_gen_particles ? 9 : 4); ++i) {
    h_vtx[i] = fs->make<TH2F>(TString::Format("h_vtx_%s", names[i]), TString::Format(";%s vx (cm); %s vy (cm)", names[i], names[i]), 200, -1, 1, 200, -1, 1);
    h_r2d[i] = fs->make<TH1F>(TString::Format("h_r2d_%s", names[i]), TString::Format(";%s 2D distance (cm);Events/0.01 cm", names[i]), 500, 0, 5);
    h_r3d[i] = fs->make<TH1F>(TString::Format("h_r3d_%s", names[i]), TString::Format(";%s 3D distance (cm);Events/0.01 cm", names[i]), 500, 0, 5);
  }

  h_t = fs->make<TH1F>("h_t", ";time to LSP decay (ns);Events/0.1 ns", 100, 0, 10);
  h_r3d_bhadron_v_bquark = fs->make<TH2F>("h_r3d_bhadron_v_bquark", ";b quark 3D distance (cm);b hadron 3D distance (cm)", 100, 0, 2, 100, 0, 2);
  h_lspbeta = fs->make<TH1F>("h_lspbeta", ";LSP #beta;Events/0.01", 100, 0, 1);
  h_lspbetagamma = fs->make<TH1F>("h_lspbetagamma", ";LSP #beta#gamma;Events/0.1", 100, 0, 10);

  h_max_dR = fs->make<TH1F>("h_max_dR", ";max #DeltaR between partons;Events/0.05", 100, 0, 5);
  h_min_dR = fs->make<TH1F>("h_min_dR", ";min #DeltaR between partons;Events/0.05", 100, 0, 5);
  h_max_dR_vs_lspbeta = fs->make<TH2F>("h_max_dR_vs_lspbeta", ";LSP #beta;max #DeltaR between partons", 100, 0, 1, 100, 0, 5);
  h_min_dR_vs_lspbeta = fs->make<TH2F>("h_min_dR_vs_lspbeta", ";LSP #beta;min #DeltaR between partons", 100, 0, 1, 100, 0, 5);
  h_max_dR_vs_lspbetagamma = fs->make<TH2F>("h_max_dR_vs_lspbetagamma", ";LSP #beta#gamma;max #DeltaR between partons", 100, 0, 10, 100, 0, 5);
  h_min_dR_vs_lspbetagamma = fs->make<TH2F>("h_min_dR_vs_lspbetagamma", ";LSP #beta#gamma;min #DeltaR between partons", 100, 0, 10, 100, 0, 5);

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

  for (int i = 0; i < 2; ++i) {
    h_bquarks_absdphi[i] = fs->make<TH1F>(TString::Format("h_bquarks_status%d_absdphi", i+2), TString::Format("events with two status%d bquarks;|#Delta#phi|;Events/0.126", i+2), 25, 0, 3.15);
    h_bquarks_dphi[i] = fs->make<TH1F>(TString::Format("h_bquarks_status%d_dphi", i+2), TString::Format("events with two status%d bquarks;#Delta#phi;Events/0.126", i+2), 50, -3.15, 3.15);
    h_bquarks_deta[i] = fs->make<TH1F>(TString::Format("h_bquarks_status%d_deta", i+2), TString::Format("events with two status%d bquarks;#Delta#eta;Events/0.16", i+2), 50, -4, 4);
    h_bquarks_deta_dphi[i] = fs->make<TH2F>(TString::Format("h_bquarks_status%d_deta_dphi", i+2), TString::Format("events with two status%d bquarks;#Delta#phi;#Delta#eta", i+2), 50, -3.15, 3.15, 50, -4, 4);
    h_bquarks_avgeta[i] = fs->make<TH1F>(TString::Format("h_bquarks_status%d_avgeta", i+2), TString::Format("events with two status%d bquarks;avg #eta;Events/0.16", i+2), 50, -4, 4);
    h_bquarks_avgeta_dphi[i] = fs->make<TH2F>(TString::Format("h_bquarks_status%d_avgeta_dphi", i+2), TString::Format("events with two status%d bquarks;#Delta#phi;avg #eta", i+2), 50, -3.15, 3.15, 50, -4, 4);
    h_bquarks_dR[i] = fs->make<TH1F>(TString::Format("h_bquarks_status%d_dR", i+2), TString::Format("events with two status%d bquarks;#Delta R;Events/0.14", i+2), 50, 0, 7);
    h_bquarks_dR_dphi[i] = fs->make<TH2F>(TString::Format("h_bquarks_status%d_dR_dphi", i+2), TString::Format("events with two status%d bquarks;#Delta#phi;#Delta R", i+2), 50, -3.15, 3.15, 50, 0, 7);
  }

  h_npartons_in_acc = fs->make<TH1F>("h_npartons_in_acc", ";number of LSP daughters in acceptance;Events", 11, 0, 11);
  h_npartons_60 = fs->make<TH1F>("h_npartons_60", ";number of partons with E_{T} > 60 GeV;Events", 11, 0, 11);
  h_njets_60 = fs->make<TH1F>("h_njets_60", ";number of jets with E_{T} > 60 GeV;Events", 11, 0, 11);
  h_sumht_20 = fs->make<TH1F>("h_sumht_20", ";#SigmaH_{T} of jets with E_{T} > 20 GeV;Events", 100, 0, 2000);

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
  event.getByLabel(gen_src, gen_particles);

  const reco::GenParticle& for_vtx = gen_particles->at(2);
  const int for_vtx_id = abs(for_vtx.pdgId());
  die_if_not(for_vtx_id == 21 || (for_vtx_id >= 1 && for_vtx_id <= 5), "gen_particles[2] is not a gluon or udscb: id=%i", for_vtx_id);
  float x0 = for_vtx.vx(), y0 = for_vtx.vy(), z0 = for_vtx.vz();
  auto fill = [x0,y0,z0](BasicKinematicHists* bkh, const reco::Candidate* c) {
    bkh->Fill(c);
    bkh->FillEx(signed_mag(c->vx() - x0, c->vy() - y0), c->vz() - z0, c->charge());
  };

  if (!mci_bkg) {
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
	for (int i = 0; i < 4; ++i) {
	  dx [i] = particles[i]->vx() - x0;
	  dy [i] = particles[i]->vy() - y0;
	  dz [i] = particles[i]->vz() - z0;
	  r2d[i] = mag(dx[i], dy[i]);
	  r3d[i] = mag(dx[i], dy[i], dz[i]);
	  h_vtx[i]->Fill(dx[i], dy[i]);
	  h_r2d[i]->Fill(r2d[i]);
	  h_r3d[i]->Fill(r3d[i]);
	}
      
	h_t->Fill(r3d[0]/lspbeta/30);
	h_r3d_bhadron_v_bquark->Fill(r3d[2], r3d[3]);
	if (fabs(r3d[2] - r3d[3]) > 0.001) // 10 micron
	  printf("difference between bquark and bhadron r3ds is %f for run,lumi,event %u, %u, %u\n", fabs(r3d[2] - r3d[3]), event.id().run(), event.luminosityBlock(), event.id().event());
        
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
	      for (int i : tofill) {
		h_vtx[i]->Fill(dx, dy);
		h_r2d[i]->Fill(r2d);
		h_r3d[i]->Fill(r3d);
	      }
	    }
	  }

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
	h_min_dR_vs_lspbeta->Fill(lspbeta, min_dR);
	h_max_dR_vs_lspbeta->Fill(lspbeta, max_dR);
	h_min_dR_vs_lspbetagamma->Fill(lspbetagamma, min_dR);
	h_max_dR_vs_lspbetagamma->Fill(lspbetagamma, max_dR);
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

  if (mci_bkg) {
    MCInteractionTops mci;
    mci.Init(*gen_particles);
    if (!mci.Valid()) {
      if (!mci_warned)
    	edm::LogWarning("GenHistos") << "MCInteractionTops invalid; no further warnings!";
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
	
	if (mci.bottoms[i] != 0)
	  fill(Bottoms      [i], mci.bottoms          [i]);
	fill(Tops           [i], mci.tops             [i]);
	fill(Ws             [i], mci.Ws               [i]);
	
	for (int j = 0; j < 2; ++j) {
	  const reco::Candidate* c = mci.W_daughters[i][j];
	  fill(WDaughters[i][j], c);
	  const int id = abs(c->pdgId());
	  if      (id == 11) { fill(Leptons, c); fill(LightLeptons, c); fill(Electrons, c); }
	  else if (id == 13) { fill(Leptons, c); fill(LightLeptons, c); fill(Muons,     c); }
	  else if (id == 15) { fill(Leptons, c);                        fill(Taus,      c); }
	}
	
	const int ndau = 2;
	if (mci.bottoms[i] != 0) {
	  const reco::GenParticle* daughters[ndau] = { mci.bottoms[i], mci.Ws[i] };
 
	  const reco::Candidate* particles[4] = { 0, 0, mci.bottoms[i], 0};
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
	  for (int i = 2; i < 4; ++i) {
	    dx [i] = particles[i]->vx() - x0;
	    dy [i] = particles[i]->vy() - y0;
	    dz [i] = particles[i]->vz() - z0;
	    r2d[i] = mag(dx[i], dy[i]);
	    r3d[i] = mag(dx[i], dy[i], dz[i]);
	    h_vtx[i]->Fill(dx[i], dy[i]);
	    h_r2d[i]->Fill(r2d[i]);
	    h_r3d[i]->Fill(r3d[i]);
	  }
	

	  h_r3d_bhadron_v_bquark->Fill(r3d[2], r3d[3]);
	
	  if (check_all_gen_particles)
	    for (const auto& gen : *gen_particles) {
	      if (gen.status() == 1 && gen.charge() != 0 && mag(gen.vx(), gen.vy()) < 120 && abs(gen.vz()) < 300) {
		const bool from21 = has_any_ancestor_with_id(&gen, 1000021);
		const bool from22 = has_any_ancestor_with_id(&gen, 1000022);
		const float dx = gen.vx() - x0;
		const float dy = gen.vy() - y0;
		const float dz = gen.vz() - z0;
		const float r2d = mag(dx, dy);
		const float r3d = mag(dx, dy, dz);
		std::vector<int> tofill;
		h_status1origins->Fill((from21*4) | (from22*2));
		if (from21) tofill.push_back(4);
		if (from22) tofill.push_back(5);
		if (from21 && !from22 ) tofill.push_back(7);
		if (from22 && !from21 ) tofill.push_back(8);
		for (int i : tofill) {
		  h_vtx[i]->Fill(dx, dy);
		  h_r2d[i]->Fill(r2d);
		  h_r3d[i]->Fill(r3d);
		}
	      }
	    }	
	
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
	}
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
  std::vector<int> ids[2];
  std::vector<double> eta[2];
  std::vector<double> phi[2];
  int nbquarksstatus3 = 0;
  for (const reco::GenParticle& gen : *gen_particles) {
    if (abs(gen.pdgId()) == 5) {
      bool has_b_mom = false;
      for (size_t i = 0, ie = gen.numberOfMothers(); i < ie; ++i) {
        if (abs(gen.mother(i)->pdgId()) == 5) {
          has_b_mom = true;
          break;
        }
      }
      if (!has_b_mom) {
        ++nbquarks;
        if (gen.pt() > min_b_pt && fabs(gen.eta()) < max_b_eta) {
          ++nbquarks_wcuts;
        }
      }
      for (int i = 0; i < 2; ++i) {
        if (gen.status() == i+2) {
          ids[i].push_back(gen.pdgId());
          eta[i].push_back(gen.eta());
          phi[i].push_back(gen.phi());
        }
      }
      if (gen.status() == 3) {
        ++nbquarksstatus3;
        h_bquarks_pt->Fill(gen.pt());
        h_bquarks_eta->Fill(gen.eta());
        h_bquarks_phi->Fill(gen.phi());
        h_bquarks_energy->Fill(gen.energy());
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
  h_nbquarks->Fill(nbquarksstatus3);
  for (int i = 0; i < 2; ++i) {
    if (ids[i].size() == 2) {
      if (ids[i][0] * ids[i][1] < 0) {
        double dphi = reco::deltaPhi(phi[i][0], phi[i][1]);
        double deta = eta[i][0] - eta[i][1];
        double avgeta = (eta[i][0] + eta[i][1]) / 2;
        double dR = reco::deltaR(eta[i][0], phi[i][0], eta[i][1], phi[i][1]);
        h_bquarks_absdphi[i]->Fill(fabs(dphi));
        h_bquarks_dphi[i]->Fill(dphi);
        h_bquarks_deta[i]->Fill(deta);
        h_bquarks_deta_dphi[i]->Fill(dphi, deta);
        h_bquarks_avgeta[i]->Fill(avgeta);
        h_bquarks_avgeta_dphi[i]->Fill(dphi, avgeta);
        h_bquarks_dR[i]->Fill(dR);
        h_bquarks_dR_dphi[i]->Fill(dphi, dR);
      }
    }
  }


  edm::Handle<reco::GenJetCollection> gen_jets;
  event.getByLabel(gen_jet_src, gen_jets);

  NJets->Fill(gen_jets->size());
  int nbjets = 0;
  int njets60 = 0;
  float sumht = 0.0;
  for (const reco::GenJet& jet : *gen_jets) {
    int nchg = 0;
    int id = gen_jet_id(jet);
    for (const reco::GenParticle* g : jet.getGenConstituents())
      if (g->charge())
        ++nchg;

    float fchg = float(nchg)/jet.nConstituents();

    if (jet.pt() > 60 && fabs(jet.eta()) < 2.5)
      ++njets60;
    if (jet.pt() > 20 && fabs(jet.eta()) < 2.5)
      sumht = sumht + jet.pt();;

    Jets->Fill(&jet);
    JetAuxE->Fill(jet.auxiliaryEnergy());
    JetEmE->Fill(jet.emEnergy());
    JetHadE->Fill(jet.hadEnergy());
    JetInvE->Fill(jet.invisibleEnergy());
    JetNConstituents->Fill(jet.nConstituents());
    JetNChargedConst->Fill(nchg);
    JetFChargedConst->Fill(fchg);

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
  h_sumht_20->Fill(sumht);
}

DEFINE_FWK_MODULE(MFVGenHistos);
