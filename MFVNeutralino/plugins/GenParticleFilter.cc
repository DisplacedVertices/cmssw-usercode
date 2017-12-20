#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "JMTucker/MFVNeutralinoFormats/interface/MCInteractions.h"
#include "JMTucker/Tools/interface/GenUtilities.h"

class MFVGenParticleFilter : public edm::EDFilter {
public:
  explicit MFVGenParticleFilter(const edm::ParameterSet&);

private:
  virtual bool filter(edm::Event&, const edm::EventSetup&);

  const edm::EDGetTokenT<reco::GenJetCollection> gen_jets_token;
  const edm::EDGetTokenT<std::vector<double>> gen_vertex_token;
  const edm::EDGetTokenT<mfv::MCInteraction> mci_token;

  const int min_njets;
  const double min_jet_pt;
  const double min_jet_ht;

  const int required_num_leptonic;
  const std::vector<int> allowed_decay_types;
  const double min_lepton_pt;
  const double max_lepton_eta;
  const double min_dvv;
  const double min_rho0;
  const double max_rho0;
  const double min_rho1;
  const double max_rho1;
  const double min_r0;
  const double max_r0;
  const double min_r1;
  const double max_r1;
  const double min_rhobigger;
  const double max_rhobigger;
  const double min_rhosmaller;
  const double max_rhosmaller;
  const double min_rbigger;
  const double max_rbigger;
  const double min_rsmaller;
  const double max_rsmaller;

  bool pass_lepton(const reco::Candidate* lep) const {
    return lep->pt() >= min_lepton_pt || fabs(lep->eta()) < max_lepton_eta;
  }

  const int min_npartons;
  const double min_parton_pt;
  const double min_parton_ht;
  const double min_parton_ht40;
  const int min_ntracks;
  const int min_nquarks;
  const double min_sumpt;
  const double max_drmin;
  const double min_drmax;
  const double max_drmax;
};

MFVGenParticleFilter::MFVGenParticleFilter(const edm::ParameterSet& cfg) 
  : gen_jets_token(consumes<reco::GenJetCollection>(cfg.getParameter<edm::InputTag>("gen_jets_src"))),
    gen_vertex_token(consumes<std::vector<double>>(cfg.getParameter<edm::InputTag>("gen_vertex_src"))),
    mci_token(consumes<mfv::MCInteraction>(cfg.getParameter<edm::InputTag>("mci_src"))),
    min_njets(cfg.getParameter<int>("min_njets")),
    min_jet_pt(cfg.getParameter<double>("min_jet_pt")),
    min_jet_ht(cfg.getParameter<double>("min_jet_ht")),
    required_num_leptonic(cfg.getParameter<int>("required_num_leptonic")),
    allowed_decay_types(cfg.getParameter<std::vector<int> >("allowed_decay_types")),
    min_lepton_pt(cfg.getParameter<double>("min_lepton_pt")),
    max_lepton_eta(cfg.getParameter<double>("max_lepton_eta")),
    min_dvv(cfg.getParameter<double>("min_dvv")),
    min_rho0(cfg.getParameter<double>("min_rho0")),
    max_rho0(cfg.getParameter<double>("max_rho0")),
    min_rho1(cfg.getParameter<double>("min_rho1")),
    max_rho1(cfg.getParameter<double>("max_rho1")),
    min_r0(cfg.getParameter<double>("min_r0")),
    max_r0(cfg.getParameter<double>("max_r0")),
    min_r1(cfg.getParameter<double>("min_r1")),
    max_r1(cfg.getParameter<double>("max_r1")),
    min_rhobigger(cfg.getParameter<double>("min_rhobigger")),
    max_rhobigger(cfg.getParameter<double>("max_rhobigger")),
    min_rhosmaller(cfg.getParameter<double>("min_rhosmaller")),
    max_rhosmaller(cfg.getParameter<double>("max_rhosmaller")),
    min_rbigger(cfg.getParameter<double>("min_rbigger")),
    max_rbigger(cfg.getParameter<double>("max_rbigger")),
    min_rsmaller(cfg.getParameter<double>("min_rsmaller")),
    max_rsmaller(cfg.getParameter<double>("max_rsmaller")),
    min_npartons(cfg.getParameter<int>("min_npartons")),
    min_parton_pt(cfg.getParameter<double>("min_parton_pt")),
    min_parton_ht(cfg.getParameter<double>("min_parton_ht")),
    min_parton_ht40(cfg.getParameter<double>("min_parton_ht40")),
    min_ntracks(cfg.getParameter<int>("min_ntracks")),
    min_nquarks(cfg.getParameter<int>("min_nquarks")),
    min_sumpt(cfg.getParameter<double>("min_sumpt")),
    max_drmin(cfg.getParameter<double>("max_drmin")),
    min_drmax(cfg.getParameter<double>("min_drmax")),
    max_drmax(cfg.getParameter<double>("max_drmax"))
{
}

namespace {
  template <typename T>
  T mag(T x, T y) {
    return sqrt(x*x + y*y);
  }

  template <typename T>
  T mag(T x, T y, T z) {
    return sqrt(x*x + y*y + z*z);
  }
}

bool MFVGenParticleFilter::filter(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<std::vector<double>> gen_vertex;
  event.getByToken(gen_vertex_token, gen_vertex);
    
  const double x0 = (*gen_vertex)[0];
  const double y0 = (*gen_vertex)[1];
  const double z0 = (*gen_vertex)[2];

  std::vector<const reco::GenParticle*> partons[2];
  double v[2][3] = {{0}};

  edm::Handle<mfv::MCInteraction> mci;
  event.getByToken(mci_token, mci);

  if (!mci->valid()) {
    std::cout << "MFVGenParticleFilter: MCInteraction not valid--model not implemented? skipping event" << std::endl;
    return false;
  }

  for (int i : {0,1}) {
    for (auto ref : mci->visible(i))
      partons[i].push_back((reco::GenParticle*)first_candidate(&*ref));
    auto x = mci->decay_point(i);
    v[i][0] = x.x - x0;
    v[i][1] = x.y - y0;
    v[i][2] = x.z - z0;
  }

  const double dbv[2] = { mag(v[0][0], v[0][1]), mag(v[1][0], v[1][1]) };
  const double dvv = mci->dvv();

  edm::Handle<reco::GenJetCollection> gen_jets;
  event.getByToken(gen_jets_token, gen_jets);

  int njets_min_pt = 0;
  double jet_ht = 0;
  for (const reco::GenJet& jet : *gen_jets) {
    if (jet.pt() > min_jet_pt && fabs(jet.eta()) < 2.5)
      ++njets_min_pt;
    if (jet.pt() > 20 && fabs(jet.eta()) < 2.5)
      jet_ht += jet.pt();
  }
  if (njets_min_pt < min_njets)
    return false;
  if (jet_ht < min_jet_ht)
    return false;

  if (required_num_leptonic >= 0) {
    int nlep = 0;
    for (const auto& r : mci->light_leptons())
      if (pass_lepton(&*r))
        ++nlep;
    if (nlep < required_num_leptonic)
      return false;
  }

  if (allowed_decay_types.size())
    for (int i = 0; i < 2; ++i)
      if (std::find(allowed_decay_types.begin(), allowed_decay_types.end(), mci->decay_type()[i]) == allowed_decay_types.end())
        return false;

  const double rho0 = dbv[0];
  const double rho1 = dbv[1];

  if (min_dvv > 0 && dvv < min_dvv)
    return false;

  if ((min_rho0 > 0 && rho0 < min_rho0) ||
      (max_rho0 > 0 && rho0 > max_rho0) ||
      (min_rho1 > 0 && rho1 < min_rho1) ||
      (max_rho1 > 0 && rho1 > max_rho1))
    return false;

  const double rhobigger  = rho0 < rho1 ? rho1 : rho0;
  const double rhosmaller = rho0 < rho1 ? rho0 : rho1;

  if ((min_rhobigger > 0 && rhobigger < min_rhobigger)    ||
      (max_rhobigger > 0 && rhobigger > max_rhobigger)    ||
      (min_rhosmaller > 0 && rhosmaller < min_rhosmaller) ||
      (max_rhosmaller > 0 && rhosmaller > max_rhosmaller))
    return false;

  const double r0 = mag(v[0][0], v[0][1], v[0][2]);
  const double r1 = mag(v[1][0], v[1][1], v[1][2]);

  if ((min_r0 > 0 && r0 < min_r0) ||
      (max_r0 > 0 && r0 > max_r0) ||
      (min_r1 > 0 && r1 < min_r1) ||
      (max_r1 > 0 && r1 > max_r1))
    return false;

  const double rbigger  = r0 < r1 ? r1 : r0;
  const double rsmaller = r0 < r1 ? r0 : r1;

  if ((min_rbigger > 0 && rbigger < min_rbigger)    ||
      (max_rbigger > 0 && rbigger > max_rbigger)    ||
      (min_rsmaller > 0 && rsmaller < min_rsmaller) ||
      (max_rsmaller > 0 && rsmaller > max_rsmaller))
    return false;

  std::vector<float> parton_pt;
  for (int i = 0; i < 2; ++i) {
    for (const reco::GenParticle* p : partons[i]) {
      if (p->pt() > 20 && fabs(p->eta()) < 2.5 && is_quark(p)) {
        parton_pt.push_back(p->pt());
      }
    }
  }
  std::sort(parton_pt.begin(), parton_pt.end(), [](float p1, float p2) { return p1 > p2; } );

  if (int(parton_pt.size()) < min_npartons)
    return false;
  if (min_npartons > 0 && parton_pt.at(min_npartons-1) < min_parton_pt)
    return false;
  if (std::accumulate(parton_pt.begin(), parton_pt.end(), 0.f) < min_parton_ht)
    return false;
  if (std::accumulate(parton_pt.begin(), parton_pt.end(), 0.f, [](float init, float b) { if (b > 40) init += b; return init; }) < min_parton_ht40)
    return false;

  for (int i = 0; i < 2; ++i) {
    const int ndau = int(partons[i].size());

    int ntracks = 0;
    int nquarks = 0;
    float sumpt = 0;
    float drmin = 1e6;
    float drmax = 0;
    for (int j = 0; j < ndau; ++j) {
      const reco::GenParticle* p1 = partons[i][j];
      if (is_neutrino(p1) || p1->pt() < 20 || fabs(p1->eta()) > 2.5 || fabs(dbv[i] * sin(p1->phi() - atan2(v[i][1], v[i][0]))) < 0.01) continue;
      ++ntracks;
      if (!is_lepton(p1)) ++nquarks;
      sumpt += p1->pt();
      for (int k = j+1; k < ndau; ++k) {
        const reco::GenParticle* p2 = partons[i][k];
        if (is_neutrino(p2) || p2->pt() < 20 || fabs(p2->eta()) > 2.5 || fabs(dbv[i] * sin(p2->phi() - atan2(v[i][1], v[i][0]))) < 0.01) continue;
        float dr = reco::deltaR(*p1, *p2);
        if (dr < drmin)
          drmin = dr;
        if (dr > drmax)
          drmax = dr;
      }
    }

    if (ntracks < min_ntracks)
      return false;
    if (nquarks < min_nquarks)
      return false;
    if (sumpt < min_sumpt)
      return false;
    if (drmin > max_drmin)
      return false;
    if (drmax < min_drmax)
      return false;
    if (drmax > max_drmax)
      return false;
  }

  return true;
}

DEFINE_FWK_MODULE(MFVGenParticleFilter);
