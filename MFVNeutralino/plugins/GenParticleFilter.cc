#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
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
};

MFVGenParticleFilter::MFVGenParticleFilter(const edm::ParameterSet& cfg) 
  : gen_src(cfg.getParameter<edm::InputTag>("gen_src")),
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
    mci_warned(false)
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

  return true;
}

DEFINE_FWK_MODULE(MFVGenParticleFilter);
