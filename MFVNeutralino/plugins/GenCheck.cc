#include "TH2F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/GenUtilities.h"
#include "JMTucker/Tools/interface/Utilities.h"

class MFVGenCheck : public edm::EDAnalyzer {
public:
  explicit MFVGenCheck(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);
  void endJob();

private:
  const bool debug;
  const edm::InputTag gen_src;
  const int lsp_id;
  std::vector<std::vector<int> > allowed_dau_ids;

  TH1F* h_nlsp;
  TH1F* h_ndau;
  TH1F* h_beta;
  TH1F* h_betagamma;
  TH1F* h_betagamma_orig;
  TH1F* h_r3d;
  TH1F* h_tau;

  std::map<int, int> all_dau_ids;
};

MFVGenCheck::MFVGenCheck(const edm::ParameterSet& cfg)
  : debug(cfg.getUntrackedParameter<bool>("debug", false)),
    gen_src(cfg.getParameter<edm::InputTag>("gen_src")),
    lsp_id(cfg.getParameter<int>("lsp_id"))
{
  const edm::ParameterSet& allowed = cfg.getParameter<edm::ParameterSet>("allowed_dau_ids");
  for (const std::string& name : allowed.getParameterNamesForType<std::vector<int>>()) {
    std::vector<int> v = allowed.getParameter<std::vector<int>>(name);
    std::sort(v.begin(), v.end());
    allowed_dau_ids.push_back(v);
  }

  edm::Service<TFileService> fs;

  h_nlsp = fs->make<TH1F>("h_nlsp", "", 5, 0, 5);
  h_ndau = fs->make<TH1F>("h_ndau", "", 5, 0, 5);;
  h_beta = fs->make<TH1F>("h_beta", "", 500, 0, 1);
  h_betagamma = fs->make<TH1F>("h_betagamma", "", 500, 0, 5);
  h_betagamma_orig = fs->make<TH1F>("h_betagamma_orig", "", 500, 0, 5);
  h_r3d = fs->make<TH1F>("h_r3d", "", 500, 0, 5);
  h_tau = fs->make<TH1F>("h_tau", "", 500, 0, 5);
}

namespace {
  float mag(float x, float y, float z) {
    return sqrt(x*x + y*y + z*z);
  }
}

void MFVGenCheck::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  if (debug) printf("\n\nevent %i\n", int(event.id().event()));

  edm::Handle<reco::GenParticleCollection> gen_particles;
  event.getByLabel(gen_src, gen_particles);

  std::vector<const reco::GenParticle*> lsps;

  const reco::GenParticle& for_vtx = gen_particles->at(2);
  const int for_vtx_id = abs(for_vtx.pdgId());
  die_if_not(for_vtx_id == 21 || (for_vtx_id >= 1 && for_vtx_id <= 5), "gen_particles[2] is not a gluon or udscb: id=%i", for_vtx_id);
  float x0 = for_vtx.vx(), y0 = for_vtx.vy(), z0 = for_vtx.vz();

  int igen = -1;
  bool found = false;
  for (const reco::GenParticle& gen : *gen_particles) {
    ++igen;

    if (gen.pdgId() != lsp_id)
      continue;

    if (!found) {
      found = true;
      const double beta = gen.p() / gen.energy();
      const double betagamma = beta / sqrt(1 - beta*beta);
      h_betagamma_orig->Fill(betagamma);
    }      
      
    if (debug) printf("lsp at %i has daus: ", igen);
    std::vector<int> dau_ids;
    for (int idau = 0, idaue = gen.numberOfDaughters(); idau < idaue; ++idau) {
      const reco::Candidate* dau = gen.daughter(idau);
      if (debug) printf("%i ", dau->pdgId());
      dau_ids.push_back(dau->pdgId());
    }

    std::sort(dau_ids.begin(), dau_ids.end());

    bool ok = false;

    for (const std::vector<int>& allowed : allowed_dau_ids)
      if (allowed == dau_ids) {
        ok = true;
        break;
      }

    if (debug) printf("ok? %i\n", ok);

    if (ok)
      lsps.push_back(&gen);
  }

  if (debug) printf("got %i lsps with ok decays\n", int(lsps.size()));
  h_nlsp->Fill(lsps.size());

  if (lsps.size() == 2) {
    std::vector<int> dau_ids[2];

    for (int ilsp = 0; ilsp < 2; ++ilsp) {
      const reco::GenParticle* lsp = lsps[ilsp];

      const double beta = lsp->p() / lsp->energy();
      const double betagamma = beta / sqrt(1 - beta*beta);
      h_beta->Fill(beta);
      h_betagamma->Fill(betagamma);

      for (int idau = 0, idaue = lsp->numberOfDaughters(); idau < idaue; ++idau) {
        const reco::Candidate* dau = lsp->daughter(idau);
        dau_ids[ilsp].push_back(dau->pdgId());
        if (debug) printf("ilsp %i dau id %i\n", ilsp, dau->pdgId());
        if (idau == 0) {
          const double r3d = mag(dau->vx() - x0,
                                 dau->vy() - y0,
                                 dau->vz() - z0);
          const double tau = r3d / betagamma;
          h_r3d->Fill(r3d);
          h_tau->Fill(tau);
        }
      }

      for (int id : dau_ids[ilsp])
        all_dau_ids[id] += 1;
    }

    h_ndau->Fill(dau_ids[0].size());
    h_ndau->Fill(dau_ids[1].size());
  }
}

void MFVGenCheck::endJob() {
  edm::Service<TFileService> fs;

  const size_t n = all_dau_ids.size();
  
  TH1F* h_dauids = fs->make<TH1F>("h_dauids", "", n, 0, n);
  TAxis* ax = h_dauids->GetXaxis();
  int i = 1;
  for (auto p : all_dau_ids) {
    ax->SetBinLabel(i, TString::Format("%i", p.first));
    h_dauids->SetBinContent(i, p.second);
    ++i;
  }
}

DEFINE_FWK_MODULE(MFVGenCheck);
