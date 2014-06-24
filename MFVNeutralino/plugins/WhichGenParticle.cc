#include "TH2F.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/Tools/interface/Utilities.h"

class MFVWhichGenParticle : public edm::EDAnalyzer {
 public:
  explicit MFVWhichGenParticle(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::InputTag gen_particles_src;
  const edm::InputTag mevent_src;
  const edm::InputTag vertices_src;

  float bsx;
  float bsy;

  TH1F* h_nsv;
  TH1F* h_svdz;

  std::map<std::string, TH1F*> m_h_nxx;
  std::map<std::string, TH2F*> m_h_nsv_v_nxx;
  std::map<std::string, TH1F*> m_h_dphi_sv_xx;
  std::map<std::string, TH1F*> m_h_min_dphi_sv_xx;
  std::map<std::string, TH1F*> m_h_dist_sv_xx;
  std::map<std::string, TH1F*> m_h_min_dist_sv_xx;

  typedef std::vector<const reco::GenParticle*> GenParticlePointers;
  void fill(const std::string name, const MFVVertexAuxCollection&, const GenParticlePointers&);
};

MFVWhichGenParticle::MFVWhichGenParticle(const edm::ParameterSet& cfg)
  : gen_particles_src(cfg.getParameter<edm::InputTag>("gen_particles_src")),
    mevent_src(cfg.getParameter<edm::InputTag>("mevent_src")),
    vertices_src(cfg.getParameter<edm::InputTag>("vertices_src"))
{
  edm::Service<TFileService> fs;
  h_nsv  = fs->make<TH1F>("h_nsv",  ";number of secondary vertices;events", 10, 0, 10);
  h_svdz = fs->make<TH1F>("h_svdz", ";#Delta z(SV, PV) (cm);events/0.1 cm", 100, -5, 5);

  const char* parts[] = { "bquarks", "bmesons", "cmesons", "smesonschg", "smesonsneu", "pions", "bbaryons", "cbaryons", "sbaryons", "taus" };
  for (const char* part : parts) {
    m_h_nxx       [part] = fs->make<TH1F>(TString::Format("h_n%s",         part), TString::Format(";number of %s;events",                                     part), 100, 0, 100);
    m_h_nsv_v_nxx [part] = fs->make<TH2F>(TString::Format("h_nsv_v_n%s",   part), TString::Format(";number of %s;number of vertices",                         part), 100, 0, 100, 10, 0, 10);
    m_h_dphi_sv_xx[part] = fs->make<TH1F>(TString::Format("h_dphi_sv_n%s", part), TString::Format(";#Delta#phi(%s_{i}, each vertex);vertices/0.063", part), 100, -M_PI, M_PI);
    m_h_min_dphi_sv_xx[part] = fs->make<TH1F>(TString::Format("h_min_dphi_sv_n%s", part), TString::Format(";smallest #Delta#phi(%s_{i}, each vertex);vertices/0.063", part), 100, -M_PI, M_PI);
    m_h_dist_sv_xx[part] = fs->make<TH1F>(TString::Format("h_dist_sv_n%s", part), TString::Format(";dist3d(%s_{i}, each vertex);vertices/0.0005 cm", part), 100, 0, 0.05);
    m_h_min_dist_sv_xx[part] = fs->make<TH1F>(TString::Format("h_min_dist_sv_n%s", part), TString::Format(";smallest dist3d(%s_{i}, each vertex);vertices/0.0005 cm", part), 100, 0, 0.05);
  }
}

void MFVWhichGenParticle::fill(const std::string name, const MFVVertexAuxCollection& sv, const MFVWhichGenParticle::GenParticlePointers& xx) {
  TH1F* h_nxx        = m_h_nxx       [name];
  TH2F* h_nsv_v_nxx  = m_h_nsv_v_nxx [name];
  TH1F* h_dphi_sv_xx = m_h_dphi_sv_xx[name];
  TH1F* h_min_dphi_sv_xx = m_h_min_dphi_sv_xx[name];
  TH1F* h_dist_sv_xx = m_h_dist_sv_xx[name];
  TH1F* h_min_dist_sv_xx = m_h_min_dist_sv_xx[name];

  static const bool debug = false;
  if (debug) printf("%s:\n", name.c_str());

  const int nsv = int(sv.size());
  const int nxx = int(xx.size());

  h_nxx->Fill(nxx);
  h_nsv_v_nxx->Fill(nxx, nsv);

  std::vector<double> dphis(nsv*nxx);
  std::vector<double> dists(nsv*nxx);

  for (int ixx = 0; ixx < nxx; ++ixx) {
    const reco::GenParticle* b = xx[ixx];
    for (int isv = 0; isv < nsv; ++isv) {
      const MFVVertexAux& vtx = sv.at(isv);
      const double vtx_phi = atan2(vtx.y - bsy, vtx.x - bsx);
      const double dphi = reco::deltaPhi(vtx_phi, b->phi());
      const double dist = sqrt((vtx.x - b->vx()) * (vtx.x - b->vx()) + (vtx.y - b->vy()) * (vtx.y - b->vy()) + (vtx.z - b->vz()) * (vtx.z - b->vz()));
      if (debug) printf("ixx %i isv %i dphi %f dist %f\n", ixx, isv, dphi, dist);
      dphis[ixx*nsv + isv] = dphi;
      dists[ixx*nsv + isv] = dist;
      h_dphi_sv_xx->Fill(dphi);
      h_dist_sv_xx->Fill(dist);
    }
  }

  std::vector<double> min_dphis(nsv, 1e99);
  std::vector<bool> xx_used(nxx, 0);
  std::vector<bool> sv_used(nsv, 0);
  int used_cnt = 0;
  const int stop = std::min(nsv, nxx);
  while (used_cnt < stop) {
    double min_dphi = 1e99;
    int idphi_min = -1;
    for (int idphi = 0; idphi < nsv*nxx; ++idphi) {
      if (xx_used[idphi / nsv] || sv_used[idphi % nsv])
        continue;
      if (fabs(dphis[idphi]) < fabs(min_dphi)) {
        min_dphi = dphis[idphi];
        idphi_min = idphi;
      }
    }

    const int ixx_min = idphi_min / nsv;
    const int isv_min = idphi_min % nsv;
    min_dphis[isv_min] = min_dphi;
    xx_used[ixx_min] = 1;
    sv_used[isv_min] = 1;
    if (debug) printf("using ixx %i for isv %i with dphi %f\n", ixx_min, isv_min, min_dphi);
    ++used_cnt;
  }

  std::vector<double> min_dists(nsv, 1e99);
  xx_used.assign(nxx, 0);
  sv_used.assign(nsv, 0);
  used_cnt = 0;
  while (used_cnt < stop) {
    double min_dist = 1e99;
    int idist_min = -1;
    for (int idist = 0; idist < nsv*nxx; ++idist) {
      if (xx_used[idist / nsv] || sv_used[idist % nsv])
        continue;
      if (dists[idist] < min_dist) {
        min_dist = dists[idist];
        idist_min = idist;
      }
    }

    const int ixx_min = idist_min / nsv;
    const int isv_min = idist_min % nsv;
    min_dists[isv_min] = min_dist;
    xx_used[ixx_min] = 1;
    sv_used[isv_min] = 1;
    if (debug) printf("using ixx %i for isv %i with dist %f\n", ixx_min, isv_min, min_dist);
    ++used_cnt;
  }

  if (debug) printf("best:\n");
  for (int isv = 0; isv < nsv; ++isv) {
    h_min_dphi_sv_xx->Fill(min_dphis[isv]);
    h_min_dist_sv_xx->Fill(min_dists[isv]);
    if (debug) printf("isv: %i dphi: %f dist: %f\n", isv, min_dphis[isv], min_dists[isv]);
  }
}

void MFVWhichGenParticle::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<reco::GenParticleCollection> gen_particles;
  event.getByLabel(gen_particles_src, gen_particles);

  GenParticlePointers bquarks;
  GenParticlePointers bmesons;
  GenParticlePointers cmesons;
  GenParticlePointers smesonschg;
  GenParticlePointers smesonsneu;
  GenParticlePointers pions;
  GenParticlePointers bbaryons;
  GenParticlePointers cbaryons;
  GenParticlePointers sbaryons;
  GenParticlePointers taus;

  for (const reco::GenParticle& g: *gen_particles) {
    const bool stat1 = g.status() == 1;
    const bool stat2 = g.status() == 2 || (g.status() >= 51 && g.status() <= 59);
    const int id = abs(g.pdgId());

    if (stat2) {
      if (id == 5)
        bquarks.push_back(&g);
      else if (id % 1000 / 500 == 1)
        bmesons.push_back(&g);
      else if (id % 1000 / 400 == 1)
        cmesons.push_back(&g);
      else if ((id % 1000 / 300 == 1 || id == 130) && g.charge() != 0)
        smesonschg.push_back(&g);
      else if ((id % 1000 / 300 == 1 || id == 130) && g.charge() == 0)
        smesonsneu.push_back(&g);
      else if (id % 10000 / 5000 == 1)
        bbaryons.push_back(&g);
      else if (id % 10000 / 4000 == 1)
        cbaryons.push_back(&g);
      else if (id % 10000 / 3000 == 1)
        sbaryons.push_back(&g);
      else if (id == 15)
        taus.push_back(&g);
    }
    else if (stat1 && id == 211) {
      pions.push_back(&g);
    }
  }

  edm::Handle<MFVEvent> mevent;
  event.getByLabel(mevent_src, mevent);
  bsx = mevent->bsx;
  bsy = mevent->bsy;

  edm::Handle<MFVVertexAuxCollection> vertices;
  event.getByLabel(vertices_src, vertices);

  const int nsv = int(vertices->size());
  h_nsv->Fill(nsv);

  for (const MFVVertexAux& v : *vertices)
    h_svdz->Fill(v.z - mevent->pvz);

  fill("bquarks",  *vertices, bquarks );
  fill("bmesons",  *vertices, bmesons );
  fill("cmesons",  *vertices, cmesons );
  fill("smesonschg",  *vertices, smesonschg);
  fill("smesonsneu",  *vertices, smesonsneu);
  fill("pions",    *vertices, pions   );
  fill("bbaryons", *vertices, bbaryons);
  fill("cbaryons", *vertices, cbaryons);
  fill("sbaryons", *vertices, sbaryons);
  fill("taus",     *vertices, taus);
}

DEFINE_FWK_MODULE(MFVWhichGenParticle);
