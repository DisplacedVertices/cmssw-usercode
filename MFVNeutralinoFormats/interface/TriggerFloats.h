#ifndef JMTucker_MFVNeutralinoFormats_interface_TriggerFloats_h
#define JMTucker_MFVNeutralinoFormats_interface_TriggerFloats_h

#include "TLorentzVector.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"

namespace mfv {

  struct TriggerFloats {
    std::vector<TLorentzVector> l1jets;
    int nl1jets() const { return l1jets.size(); }
    float l1htt;
    float myhtt;
    float myhttwbug;
    float hltht;
    std::vector<HLTJet> hltcalojets;
    std::vector<HLTJet> hltpfjets;
    int nhltcalojets() const { return hltcalojets.size(); }
    int nhltpfjets() const { return hltpfjets.size(); }
    std::vector<TLorentzVector> hltelectrons;
    std::vector<TLorentzVector> hltmuons;
    std::vector<int> L1decisions;
    std::vector<int> HLTdecisions;

    // related offline stuff 
    int nalljets;
    std::vector<TLorentzVector> jets;
    std::vector<float> jetmuef;
    int njets() const { return jets.size(); }
    int njets(float min_jet_pt) const { return std::count_if(jets.begin(), jets.end(),
                                                             [min_jet_pt](const auto& p4) { return p4.Pt() > min_jet_pt; }); }
    float jetpt1() const { return njets() >= 1 ? jets[0].Pt() : -1; }
    float jetpt2() const { return njets() >= 2 ? jets[1].Pt() : -1; }
    float htall;
    float ht;
    float htptgt30;

    TriggerFloats()
    : l1htt(-1), myhtt(-1), myhttwbug(-1), hltht(-1),
      L1decisions(n_l1_paths, -1),
      HLTdecisions(n_hlt_paths, -1),
      nalljets(0), htall(0), ht(0), htptgt30(0)
    {}
  };
}

#endif
