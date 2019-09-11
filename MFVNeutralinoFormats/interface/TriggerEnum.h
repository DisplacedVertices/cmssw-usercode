#ifndef JMTucker_MFVNeutralinoFormats_interface_TriggerEnum_h
#define JMTucker_MFVNeutralinoFormats_interface_TriggerEnum_h

#include <cassert>
#include <numeric>
#include <vector>
#include <cstddef>

namespace mfv {
  // JMTBAD hope you keep these in sync with TriggerEnum.cc
  static const int n_clean_paths = 7;
  enum {
    b_HLT_PFHT1050, b_HLT_Ele35_WPTight_Gsf, b_HLT_Ele115_CaloIdVT_GsfTrkIdT, b_HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165, b_HLT_IsoMu27, b_HLT_Mu50, b_HLT_Ele15_IsoVVVL_PFHT450, b_HLT_Mu15_IsoVVVL_PFHT450, 
    b_HLT_DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_p33, b_HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0, b_HLT_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2, b_HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2, b_HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5, // 2017 bjet triggers
    b_HLT_DoublePFJets116MaxDeta1p6_DoubleCaloBTagDeepCSV_p71, b_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5, b_HLT_PFHT400_FivePFJet_100_100_60_30_30_DoublePFBTagDeepCSV_4p5, b_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94, b_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59, // 2018 bjet triggers
    b_HLT_HT430_DisplacedDijet40_DisplacedTrack, b_HLT_HT650_DisplacedDijet60_Inclusive, // displaced dijet triggers
    n_hlt_paths, // = 20

    // FIXME have to figure out which L1s to delete, and which new ones might be useful to add (to find HLT w.r.t. L1 efficiencies)

    // seeding PFHT1050 (and the cross triggers by 320er and 380er)
    b_L1_HTT120er=0, b_L1_HTT160er, b_L1_HTT200er, b_L1_HTT220er, b_L1_HTT240er, b_L1_HTT255er, b_L1_HTT270er, b_L1_HTT280er, b_L1_HTT300er, b_L1_HTT320er, b_L1_HTT340er, b_L1_HTT380er, b_L1_HTT400er, b_L1_HTT450er, b_L1_HTT500er, b_L1_HTT250er_QuadJet_70_55_40_35_er2p5, b_L1_HTT280er_QuadJet_70_55_40_35_er2p5, b_L1_HTT300er_QuadJet_70_55_40_35_er2p5,
    // the rest of Ele115+Ele50_PFJet165
    b_L1_SingleJet170, b_L1_SingleJet180, b_L1_SingleJet200, b_L1_SingleTau100er2p1, b_L1_SingleTau120er2p1,
    // IsoMu27 and Mu50
    b_L1_SingleMu22, b_L1_SingleMu25,
    n_l1_paths // = 25
  };

  static_assert(n_hlt_paths + n_l1_paths <= 64, "too many paths");

  extern const char* hlt_paths[n_hlt_paths];
  extern const char* l1_paths[n_l1_paths];
  extern const char* clean_paths[n_clean_paths];

  // For use in the HT or Bjet or DisplacedDijet trigger studies
  static const std::vector<size_t> HTOrBjetOrDisplacedDijetTriggers = {
    // HT trigger
    mfv::b_HLT_PFHT1050,
    // bjet triggers 2017
    mfv::b_HLT_DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_p33, mfv::b_HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0, mfv::b_HLT_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2, mfv::b_HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2, mfv::b_HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5,
    // bjet triggers 2018
    mfv::b_HLT_DoublePFJets116MaxDeta1p6_DoubleCaloBTagDeepCSV_p71, mfv::b_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5, mfv::b_HLT_PFHT400_FivePFJet_100_100_60_30_30_DoublePFBTagDeepCSV_4p5, mfv::b_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94, mfv::b_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59,
    // displaced dijet triggers
    mfv::b_HLT_HT430_DisplacedDijet40_DisplacedTrack, mfv::b_HLT_HT650_DisplacedDijet60_Inclusive
  };
}

#endif
