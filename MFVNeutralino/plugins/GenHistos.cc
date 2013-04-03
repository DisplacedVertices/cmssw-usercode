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
#include "JMTucker/Tools/interface/BasicKinematicHists.h"
#include "JMTucker/Tools/interface/Utilities.h"

class MFVNeutralinoGenHistos : public edm::EDAnalyzer {
 public:
  explicit MFVNeutralinoGenHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::InputTag gen_src;
  const int required_num_leptonic;
  const std::vector<int> allowed_decay_types;
  const bool print_info;

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

  TH2F* h_vtx_2d;
  TH1F* h_rho;
  TH1F* h_lspbeta;
  TH1F* h_lspbetagamma;
  TH1F* h_max_dR;
  TH1F* h_min_dR;
  TH2F* h_max_dR_vs_lspbeta;
  TH2F* h_min_dR_vs_lspbeta;
  TH2F* h_max_dR_vs_lspbetagamma;
  TH2F* h_min_dR_vs_lspbetagamma;
};

MFVNeutralinoGenHistos::MFVNeutralinoGenHistos(const edm::ParameterSet& cfg)
  : gen_src(cfg.getParameter<edm::InputTag>("gen_src")),
    required_num_leptonic(cfg.getParameter<int>("required_num_leptonic")),
    allowed_decay_types(cfg.getParameter<std::vector<int> >("allowed_decay_types")),
    print_info(cfg.getParameter<bool>("print_info"))
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
    Stranges[i]->BookDxy(200, -50, 50, "0.5");
    Stranges[i]->BookDz (200, -50, 50, "0.5");
    Stranges[i]->BookQ();

    Bottoms[i] = bkh_factory->make(TString::Format("Bottoms#%i", i), TString::Format("bottom #%i", i));
    Bottoms[i]->BookE (200, 0, 2000, "10");
    Bottoms[i]->BookP (200, 0, 2000, "10");
    Bottoms[i]->BookPt(200, 0, 2000, "10");
    Bottoms[i]->BookPz(200, 0, 2000, "10");
    Bottoms[i]->BookM (200, 0, 2000, "10");
    Bottoms[i]->BookRapEta(200, "0.1");
    Bottoms[i]->BookPhi(50, "0.125");
    Bottoms[i]->BookDxy(200, -50, 50, "0.5");
    Bottoms[i]->BookDz (200, -50, 50, "0.5");
    Bottoms[i]->BookQ();
    
    Tops[i] = bkh_factory->make(TString::Format("Tops#%i", i), TString::Format("top #%i", i));
    Tops[i]->BookE (200, 0, 2000, "10");
    Tops[i]->BookP (200, 0, 2000, "10");
    Tops[i]->BookPt(200, 0, 2000, "10");
    Tops[i]->BookPz(200, 0, 2000, "10");
    Tops[i]->BookM (200, 0, 2000, "10");
    Tops[i]->BookRapEta(200, "0.1");
    Tops[i]->BookPhi(50, "0.125");
    Tops[i]->BookDxy(200, -50, 50, "0.5");
    Tops[i]->BookDz (200, -50, 50, "0.5");
    Tops[i]->BookQ();
    
    Ws[i] = bkh_factory->make(TString::Format("Ws#%i", i), TString::Format("w #%i", i));
    Ws[i]->BookE (200, 0, 2000, "10");
    Ws[i]->BookP (200, 0, 2000, "10");
    Ws[i]->BookPt(200, 0, 2000, "10");
    Ws[i]->BookPz(200, 0, 2000, "10");
    Ws[i]->BookM (200, 0, 2000, "10");
    Ws[i]->BookRapEta(200, "0.1");
    Ws[i]->BookPhi(50, "0.125");
    Ws[i]->BookDxy(200, -50, 50, "0.5");
    Ws[i]->BookDz (200, -50, 50, "0.5");
    Ws[i]->BookQ();

    BottomsFromTops[i] = bkh_factory->make(TString::Format("BottomsFromTops#%i", i), TString::Format("bottom from top #%i", i));
    BottomsFromTops[i]->BookE (200, 0, 2000, "10");
    BottomsFromTops[i]->BookP (200, 0, 2000, "10");
    BottomsFromTops[i]->BookPt(200, 0, 2000, "10");
    BottomsFromTops[i]->BookPz(200, 0, 2000, "10");
    BottomsFromTops[i]->BookM (200, 0, 2000, "10");
    BottomsFromTops[i]->BookRapEta(200, "0.1");
    BottomsFromTops[i]->BookPhi(50, "0.125");
    BottomsFromTops[i]->BookDxy(200, -50, 50, "0.5");
    BottomsFromTops[i]->BookDz (200, -50, 50, "0.5");
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
      WDaughters[i][j]->BookDxy(200, -50, 50, "0.5");
      WDaughters[i][j]->BookDz (200, -50, 50, "0.5");
      WDaughters[i][j]->BookQ();
    }
  }

  h_vtx_2d = fs->make<TH2F>("h_vtx_2d", "", 500, -1, 1, 500, -1, 1);
  h_rho = fs->make<TH1F>("h_rho", "", 100, 0, 2);
  h_lspbeta = fs->make<TH1F>("h_lspbeta", "", 100, 0, 1);
  h_lspbetagamma = fs->make<TH1F>("h_lspbetagamma", "", 100, 0, 10);
  h_max_dR = fs->make<TH1F>("h_max_dR", "", 100, 0, 5);
  h_min_dR = fs->make<TH1F>("h_min_dR", "", 100, 0, 5);
  h_max_dR_vs_lspbeta = fs->make<TH2F>("h_max_dR_vs_lspbeta", "", 100, 0, 1, 100, 0, 5);
  h_min_dR_vs_lspbeta = fs->make<TH2F>("h_min_dR_vs_lspbeta", "", 100, 0, 1, 100, 0, 5);
  h_max_dR_vs_lspbetagamma = fs->make<TH2F>("h_max_dR_vs_lspbetagamma", "", 100, 0, 10, 100, 0, 5);
  h_min_dR_vs_lspbetagamma = fs->make<TH2F>("h_min_dR_vs_lspbetagamma", "", 100, 0, 10, 100, 0, 5);
}

float mag(float x, float y) {
  return sqrt(x*x + y*y);
}

void MFVNeutralinoGenHistos::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  setup.getData(pdt);

  edm::Handle<reco::GenParticleCollection> gen_particles;
  event.getByLabel(gen_src, gen_particles);

  MCInteractionMFV3j mci;
  mci.Init(*gen_particles);
  if (!mci.Valid()) {
    edm::LogWarning("GenHistos") << "MCInteractionMFV3j invalid!";
    return;
  }

  if (print_info)
    mci.Print(std::cout);

  if (required_num_leptonic >= 0 && mci.num_leptonic != required_num_leptonic) 
    return;

  if (allowed_decay_types.size())
    for (int i = 0; i < 2; ++i)
      if (std::find(allowed_decay_types.begin(), allowed_decay_types.end(), mci.decay_type[i]) == allowed_decay_types.end())
	return;

  NumLeptons->Fill(mci.num_leptonic);
  DecayType->Fill(mci.decay_type[0], mci.decay_type[1]);

  // Assume pythia line 2 (probably a gluon) has the "right"
  // production vertex. (The protons are just at 0,0,0.)
  const reco::GenParticle& for_vtx = gen_particles->at(2);
  const float vx = for_vtx.vx();
  const float vy = for_vtx.vy();
  if (print_info) printf("gluon x,y: %f, %f\n", vx, vy);

  for (int i = 0; i < 2; ++i) {
    // For debugging, record all the daughter ids for tops, stops, Ws.
    for (size_t j = 0; j < mci.tops[i]->numberOfDaughters(); ++j)
      fill_by_label(TopDaughterIds[i], pdt->particle(mci.tops[i]->daughter(j)->pdgId())->name());
    fill_by_label(WDaughterIds[i], pdt->particle(mci.W_daughters[i][0]->pdgId())->name(), pdt->particle(mci.W_daughters[i][1]->pdgId())->name());

    Lsps    [i]->Fill(mci.lsps[i]);
    Stranges[i]->Fill(mci.stranges[i]);
    Bottoms [i]->Fill(mci.bottoms[i]);
    Tops    [i]->Fill(mci.tops[i]);

    Stranges[i]->FillEx(mag(mci.stranges[i]->vx(), mci.stranges[i]->vy()), mci.stranges[i]->vz(), mci.stranges[i]->charge());
    Bottoms [i]->FillEx(mag(mci.bottoms [i]->vx(), mci.bottoms [i]->vy()), mci.bottoms [i]->vz(), mci.bottoms [i]->charge());
    Tops    [i]->FillEx(mag(mci.tops    [i]->vx(), mci.tops    [i]->vy()), mci.tops    [i]->vz(), mci.tops    [i]->charge());

    Ws[i]->Fill(mci.Ws[i]);
    if (mci.bottoms_from_tops[i])
      BottomsFromTops[i]->Fill(mci.bottoms_from_tops[i]);
    for (int j = 0; j < 2; ++j)
      WDaughters[i][j]->Fill(mci.W_daughters[i][j]);


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
    h_min_dR_vs_lspbeta->Fill(lspbeta, min_dR);
    h_max_dR_vs_lspbeta->Fill(lspbeta, max_dR);
    h_min_dR_vs_lspbetagamma->Fill(lspbetagamma, min_dR);
    h_max_dR_vs_lspbetagamma->Fill(lspbetagamma, max_dR);
  }
}

DEFINE_FWK_MODULE(MFVNeutralinoGenHistos);
