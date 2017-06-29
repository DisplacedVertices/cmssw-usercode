#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/TriggerFloats.h"

class MFVTriggerFloatsFilter : public edm::EDFilter {
public:
  explicit MFVTriggerFloatsFilter(const edm::ParameterSet&);

private:
  virtual bool filter(edm::Event&, const edm::EventSetup&);

  bool orem(const std::vector<int>& decisions, std::vector<int> which) {
    for (int w : which) {
      const int decision = decisions[w];
      if (decision == -1) throw cms::Exception("TriggerNotFound") << mfv::hlt_paths[w] << " wasn't found";
      else if (decision == 1) return true;
    }
    return false;
  }

  const edm::EDGetTokenT<mfv::TriggerFloats> triggerfloats_token;
  const int require_bits[2]; // HLT then L1
  const int min_njets;
  const double hltht_cut;
  const double ht_cut;
  const double myhtt_m_l1htt_cut;
  const double myhttwbug_m_l1htt_cut;
};

MFVTriggerFloatsFilter::MFVTriggerFloatsFilter(const edm::ParameterSet& cfg) 
  : triggerfloats_token(consumes<mfv::TriggerFloats>(edm::InputTag("mfvTriggerFloats"))),
    require_bits{cfg.getParameter<int>("require_hlt"), cfg.getParameter<int>("require_l1")},
    min_njets(cfg.getParameter<int>("min_njets")),
    hltht_cut(cfg.getParameter<double>("hltht_cut")),
    ht_cut(cfg.getParameter<double>("ht_cut")),
    myhtt_m_l1htt_cut(cfg.getParameter<double>("myhtt_m_l1htt_cut")),
    myhttwbug_m_l1htt_cut(cfg.getParameter<double>("myhttwbug_m_l1htt_cut"))
{
  // require_bits:
  // -1 = don't care, ORs or other combinations represented by negative numbers other than -1
  // HLT:
  // -2 = HLT_PFHT800 || PFJet450
  // -3 = HLT_PFHT800 || PFJet450 || AK8PFJet450
  // -4 = HLT_PFHT900 || PFJet450
  // -5 = HLT_PFHT900 || PFJet450 || AK8PFJet450
  // L1:
  // -2 = L1 HTT calculation bugged as in 2016H, threshold 240 GeV
  // -3 = ditto, 255 GeV
  // -4 = ditto, 280 GeV
  // -5 = ditto, 300 GeV
  // -6 = ditto, 320 GeV -- probably don't need to do every single one separately but just in case
  assert(require_bits[0] >= -5 && require_bits[0] < mfv::n_hlt_paths);
  assert(require_bits[1] >= -6 && require_bits[1] < mfv::n_l1_paths);
}

bool MFVTriggerFloatsFilter::filter(edm::Event& event, const edm::EventSetup&) {
  edm::Handle<mfv::TriggerFloats> triggerfloats;
  event.getByToken(triggerfloats_token, triggerfloats);

  for (int i = 0; i < 2; ++i) { // HLT then L1
    const int r = require_bits[i];
    if (r == -1)
      continue;

    const std::vector<int>& decisions = i == 0 ? triggerfloats->HLTdecisions : triggerfloats->L1decisions;

    if (i == 0 && r < 0) {
      if ((r == -2 && !orem(decisions, {mfv::b_HLT_PFHT800, mfv::b_HLT_PFJet450})) ||
          (r == -3 && !orem(decisions, {mfv::b_HLT_PFHT800, mfv::b_HLT_PFJet450, mfv::b_HLT_AK8PFJet450})) ||
          (r == -4 && !orem(decisions, {mfv::b_HLT_PFHT900, mfv::b_HLT_PFJet450})) ||
          (r == -5 && !orem(decisions, {mfv::b_HLT_PFHT900, mfv::b_HLT_PFJet450, mfv::b_HLT_AK8PFJet450})))
        return false;
    }
    else if (i == 1 && r < 0) {
      const double thresholds[5] = {240, 255, 280, 300, 320};
      if (triggerfloats->myhttwbug < thresholds[-r-2])
        return false;
    }
    else {
      const int decision = decisions[r];
      if (decision == -1)
        throw cms::Exception("TriggerNotFound") << (i == 0 ? "HLT" : "L1") << " bit " << r << " wasn't found";
      else if (decision == 0)
        return false;
    }
  }

  if (hltht_cut > 0 && triggerfloats->hltht < hltht_cut)
    return false;

  if (ht_cut > 0 && triggerfloats->ht < ht_cut)
    return false;

  if (min_njets > 0 && triggerfloats->njets() < min_njets)
    return false;

  if (myhtt_m_l1htt_cut > 0 && fabs(triggerfloats->myhtt - triggerfloats->l1htt) < myhtt_m_l1htt_cut)
    return false;

  if (myhttwbug_m_l1htt_cut > 0 && fabs(triggerfloats->myhttwbug - triggerfloats->l1htt) < myhttwbug_m_l1htt_cut)
    return false;

  return true;
}

DEFINE_FWK_MODULE(MFVTriggerFloatsFilter);
