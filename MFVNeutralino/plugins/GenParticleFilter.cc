#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "JMTucker/MFVNeutralino/interface/MCInteractionMFV3j.h"
#include "JMTucker/Tools/interface/GenUtilities.h"

class MFVGenParticleFilter : public edm::EDFilter {
public:
  explicit MFVGenParticleFilter(const edm::ParameterSet&);

private:
  virtual bool filter(edm::Event&, const edm::EventSetup&);

  const edm::InputTag gen_jet_src;
  const int min_njets;
  const double min_jet_pt;
  const double min_jet_sumht;

  const edm::InputTag gen_src;
  const bool print_info;
  const bool cut_invalid;
  const int required_num_leptonic;
  const std::vector<int> allowed_decay_types;
  const double min_lepton_pt;
  const double max_lepton_eta;
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
  bool mci_warned;

  bool cut_lepton(const reco::Candidate* lep) const {
    return lep->pt() < min_lepton_pt || fabs(lep->eta()) > max_lepton_eta;
  }

  const int min_npartons;
  const double min_parton_pt;
  const double min_parton_sumht;
  const double max_drmin;
  const double min_drmax;
  const double max_drmax;
};

MFVGenParticleFilter::MFVGenParticleFilter(const edm::ParameterSet& cfg) 
  : gen_jet_src(cfg.getParameter<edm::InputTag>("gen_jet_src")),
    min_njets(cfg.getParameter<int>("min_njets")),
    min_jet_pt(cfg.getParameter<double>("min_jet_pt")),
    min_jet_sumht(cfg.getParameter<double>("min_jet_sumht")),
    gen_src(cfg.getParameter<edm::InputTag>("gen_src")),
    print_info(cfg.getParameter<bool>("print_info")),
    cut_invalid(cfg.getParameter<bool>("cut_invalid")),
    required_num_leptonic(cfg.getParameter<int>("required_num_leptonic")),
    allowed_decay_types(cfg.getParameter<std::vector<int> >("allowed_decay_types")),
    min_lepton_pt(cfg.getParameter<double>("min_lepton_pt")),
    max_lepton_eta(cfg.getParameter<double>("max_lepton_eta")),
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
    mci_warned(false),
    min_npartons(cfg.getParameter<int>("min_npartons")),
    min_parton_pt(cfg.getParameter<double>("min_parton_pt")),
    min_parton_sumht(cfg.getParameter<double>("min_parton_sumht")),
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
  edm::Handle<reco::GenJetCollection> gen_jets;
  event.getByLabel(gen_jet_src, gen_jets);

  int njets_min_pt = 0;
  double jet_sumht = 0;
  for (const reco::GenJet& jet : *gen_jets) {
    if (jet.pt() > min_jet_pt && fabs(jet.eta()) < 2.5)
      ++njets_min_pt;
    if (jet.pt() > 20 && fabs(jet.eta()) < 2.5)
      jet_sumht += jet.pt();
  }
  if (njets_min_pt < min_njets)
    return false;
  if (jet_sumht < min_jet_sumht)
    return false;

  edm::Handle<reco::GenParticleCollection> gen_particles;
  event.getByLabel(gen_src, gen_particles);

  MCInteractionMFV3j mci;
  mci.Init(*gen_particles);

  if (print_info)
    mci.Print(std::cout);

  if (!mci.Valid()) {
    if (!mci_warned)
      edm::LogWarning("GenHistos") << "MCInteractionMFV3j invalid; no further warnings!";
    mci_warned = true;
    return !cut_invalid;
  }

  if (required_num_leptonic >= 0 && mci.num_leptonic != required_num_leptonic) 
    return false;

  if (mci.num_leptonic == 1) {
    if (cut_lepton(mci.W_daughters[mci.which_is_lepton][0]))
      return false;
  }
  else if (mci.num_leptonic == 2) {
    for (int i = 0; i < 2; ++i)
      if (cut_lepton(mci.W_daughters[i][0]))
        return false;
  }

  if (allowed_decay_types.size())
    for (int i = 0; i < 2; ++i)
      if (std::find(allowed_decay_types.begin(), allowed_decay_types.end(), mci.decay_type[i]) == allowed_decay_types.end())
        return false;

  const double rho0 = mag(mci.stranges[0]->vx() - mci.lsps[0]->vx(), mci.stranges[0]->vy() - mci.lsps[0]->vy());
  const double rho1 = mag(mci.stranges[1]->vx() - mci.lsps[1]->vx(), mci.stranges[1]->vy() - mci.lsps[1]->vy());

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

  const double r0 = mag(mci.stranges[0]->vx() - mci.lsps[0]->vx(), mci.stranges[0]->vy() - mci.lsps[0]->vy(), mci.stranges[0]->vz() - mci.lsps[0]->vz());
  const double r1 = mag(mci.stranges[1]->vx() - mci.lsps[1]->vx(), mci.stranges[1]->vy() - mci.lsps[1]->vy(), mci.stranges[1]->vz() - mci.lsps[1]->vz());

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

  std::vector<const reco::GenParticle*> partons;
  for (int i = 0; i < 2; ++i) {
    partons.push_back(mci.stranges[i]);
    partons.push_back(mci.bottoms[i]);
    partons.push_back(mci.bottoms_from_tops[i]);
    if (mci.decay_type[i] == 3) {
      partons.push_back(mci.W_daughters[i][0]);
      partons.push_back(mci.W_daughters[i][1]);
    }
  }

  std::vector<std::vector<float> > parton_pt_eta_phi;
  float parton_sumht = 0;
  for (const reco::GenParticle* p : partons) {
    if (p->pt() > 20 && fabs(p->eta()) < 2.5) {
      std::vector<float> pt_eta_phi;
      pt_eta_phi.push_back(p->pt());
      pt_eta_phi.push_back(p->eta());
      pt_eta_phi.push_back(p->phi());
      parton_pt_eta_phi.push_back(pt_eta_phi);
      parton_sumht += p->pt();
    }
  }
  std::sort(parton_pt_eta_phi.begin(), parton_pt_eta_phi.end(), [](std::vector<float> p1, std::vector<float> p2) { return p1.at(0) > p2.at(0); } );

  bool unmerged = true;
  while (unmerged) {
    bool merged = false;
    for (int i = 0; i < int(parton_pt_eta_phi.size()); ++i) {
      std::vector<float> p1 = parton_pt_eta_phi.at(i);
      for (int j = i+1; j < int(parton_pt_eta_phi.size()); ++j) {
        std::vector<float> p2 = parton_pt_eta_phi.at(j);
        if (reco::deltaR(p1.at(1), p1.at(2), p2.at(1), p2.at(2)) < 0.6) {
          std::vector<float> pt_eta_phi;
          pt_eta_phi.push_back(p1.at(0) + p2.at(0));
          pt_eta_phi.push_back((p1.at(0) * p1.at(1) + p2.at(0) * p2.at(1)) / (p1.at(0) + p2.at(0)));
          pt_eta_phi.push_back((p1.at(0) * p1.at(2) + p2.at(0) * p2.at(2)) / (p1.at(0) + p2.at(0)));
          parton_pt_eta_phi.erase(parton_pt_eta_phi.begin() + j);
          parton_pt_eta_phi.erase(parton_pt_eta_phi.begin() + i);
          parton_pt_eta_phi.push_back(pt_eta_phi);
          std::sort(parton_pt_eta_phi.begin(), parton_pt_eta_phi.end(), [](std::vector<float> p1, std::vector<float> p2) { return p1.at(0) > p2.at(0); } );
          merged = true;
          break;
        }
      }
      if (merged) {
        break;
      }
    }
    if (merged) {
      continue;
    }
    unmerged = false;
  }

  if (min_npartons > 0 && (int(parton_pt_eta_phi.size()) >= min_npartons ? parton_pt_eta_phi.at(min_npartons-1).at(0) : 0.f) < min_parton_pt)
    return false;
  if (parton_sumht < min_parton_sumht)
    return false;

  for (int i = 0; i < 2; ++i) {
    const int ndau = 5;
    const reco::GenParticle* daughters[ndau] = { mci.stranges[i], mci.bottoms[i], mci.bottoms_from_tops[i], mci.W_daughters[i][0], mci.W_daughters[i][1] };

    float drmin =  1e99;
    float drmax = -1e99;
    for (int j = 0; j < ndau; ++j) {
      if (is_neutrino(daughters[j]) || fabs(daughters[j]->eta()) > 2.5) continue;
      for (int k = j+1; k < ndau; ++k) {
        if (is_neutrino(daughters[k]) || fabs(daughters[k]->eta()) > 2.5) continue;
        float dr = reco::deltaR(*daughters[j], *daughters[k]);
        if (dr < drmin)
          drmin = dr;
        if (dr > drmax)
          drmax = dr;
      }
    }

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
