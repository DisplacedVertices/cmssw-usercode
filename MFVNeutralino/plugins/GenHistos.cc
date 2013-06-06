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
#include "JMTucker/Tools/interface/GenUtilities.h"
#include "JMTucker/Tools/interface/Utilities.h"

class MFVGenHistos : public edm::EDAnalyzer {
 public:
  explicit MFVGenHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::InputTag gen_src;
  const bool check_all_gen_particles;

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

  TH2F* h_vtx[9];
  TH1F* h_r2d[9];
  TH1F* h_r3d[9];
  TH1F* h_t;
  TH1F* h_lspbeta;
  TH1F* h_lspbetagamma;
  TH1F* h_max_dR;
  TH1F* h_min_dR;
  TH2F* h_max_dR_vs_lspbeta;
  TH2F* h_min_dR_vs_lspbeta;
  TH2F* h_max_dR_vs_lspbetagamma;
  TH2F* h_min_dR_vs_lspbetagamma;

  TH1F* h_status1origins;
};

MFVGenHistos::MFVGenHistos(const edm::ParameterSet& cfg)
  : gen_src(cfg.getParameter<edm::InputTag>("gen_src")),
    check_all_gen_particles(cfg.getParameter<bool>("check_all_gen_particles"))
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

  const char* names[9] = {"lsp", "strange", "bottom", "bhadron", "from21", "from22", "fromq", "from21only", "from22only"};
  for (int i = 0; i < 9; ++i) {
    h_vtx[i] = fs->make<TH2F>(TString::Format("h_vtx_%s", names[i]), TString::Format(";%s vx (cm); %s vy (cm)", names[i], names[i]), 201, -1, 1, 201, -1, 1);
    h_r2d[i] = fs->make<TH1F>(TString::Format("h_r2d_%s", names[i]), TString::Format(";%s 2D distance (cm);Events/0.05 cm", names[i]), 100, 0, 5);
    h_r3d[i] = fs->make<TH1F>(TString::Format("h_r3d_%s", names[i]), TString::Format(";%s 3D distance (cm);Events/0.05 cm", names[i]), 100, 0, 5);
  }

  h_t = fs->make<TH1F>("h_t", ";time to LSP decay (ns);Events/0.1 ns", 100, 0, 10);
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
  die_if_not(for_vtx_id == 21 || (for_vtx_id >= 1 && for_vtx_id <= 4), "gen_particles[2] is not a gluon or light quark: id=%i", for_vtx_id);
  float x0 = for_vtx.vx(), y0 = for_vtx.vy(), z0 = for_vtx.vz();

  MCInteractionMFV3j mci;
  mci.Init(*gen_particles);
  if (!mci.Valid()) {
    edm::LogWarning("GenHistos") << "MCInteractionMFV3j invalid!";
    return;
  }

  NumLeptons->Fill(mci.num_leptonic);
  DecayType->Fill(mci.decay_type[0], mci.decay_type[1]);

  for (int i = 0; i < 2; ++i) {
    // For debugging, record all the daughter ids for tops, stops, Ws.
    for (size_t j = 0, je = mci.last_tops[i]->numberOfDaughters(); j < je; ++j)
      fill_by_label(TopDaughterIds[i], pdt->particle(mci.last_tops[i]->daughter(j)->pdgId())->name());
    fill_by_label(WDaughterIds[i], pdt->particle(mci.W_daughters[i][0]->pdgId())->name(), pdt->particle(mci.W_daughters[i][1]->pdgId())->name());

    Lsps    [i]->Fill(mci.lsps[i]);
    Stranges[i]->Fill(mci.stranges[i]);
    Bottoms [i]->Fill(mci.bottoms[i]);
    Tops    [i]->Fill(mci.tops[i]);

    Stranges[i]->FillEx(signed_mag(mci.stranges[i]->vx(), mci.stranges[i]->vy()), mci.stranges[i]->vz(), mci.stranges[i]->charge());
    Bottoms [i]->FillEx(signed_mag(mci.bottoms [i]->vx(), mci.bottoms [i]->vy()), mci.bottoms [i]->vz(), mci.bottoms [i]->charge());
    Tops    [i]->FillEx(signed_mag(mci.tops    [i]->vx(), mci.tops    [i]->vy()), mci.tops    [i]->vz(), mci.tops    [i]->charge());

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

    const reco::Candidate* particles[4] = { &lsp, mci.stranges[i], mci.bottoms[i], 0};
    // For that last one, find the b hadron for the primary b quark.
    std::vector<const reco::Candidate*> b_quark_descendants;
    const reco::Candidate* last_b_quark = final_candidate(mci.bottoms[i], 3);
    flatten_descendants(last_b_quark, b_quark_descendants);
    for (const reco::Candidate* bdesc : b_quark_descendants) {
      int zid = abs(bdesc->pdgId()) % 10000;
      if (zid / 100 == 5 || zid / 1000 == 5) {
        particles[3] = bdesc;
        break;
      }
    }
    die_if_not(particles[3] != 0, "did not find b hadron");

    for (int i = 0; i < 4; ++i) {
      const float dx = particles[i]->vx() - x0;
      const float dy = particles[i]->vy() - y0;
      const float dz = particles[i]->vz() - z0;
      const float r2d = mag(dx, dy);
      const float r3d = mag(dx, dy, dz);
      h_vtx[i]->Fill(dx, dy);
      h_r2d[i]->Fill(r2d);
      h_r3d[i]->Fill(r3d);
      if (i == 0)
        h_t->Fill(r3d/lspbeta/30);
    }

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
}

DEFINE_FWK_MODULE(MFVGenHistos);
