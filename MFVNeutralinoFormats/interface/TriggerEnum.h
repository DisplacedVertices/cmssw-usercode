#ifndef JMTucker_MFVNeutralinoFormats_interface_TriggerEnum_h
#define JMTucker_MFVNeutralinoFormats_interface_TriggerEnum_h

#include <cassert>
#include <numeric>
#include <vector>
#include <cstddef>
#include "TLorentzVector.h"

namespace mfv {

  // JMTBAD hope you keep these in sync with TriggerEnum.cc
  static const int n_clean_paths = 7;
  enum {

    // HT-triggered analysis trigger
    b_HLT_PFHT1050,

    // Lepton triggers
    b_HLT_Ele35_WPTight_Gsf,
    b_HLT_Ele115_CaloIdVT_GsfTrkIdT,
    b_HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165,
    b_HLT_IsoMu27,
    b_HLT_Mu50,
    b_HLT_Ele15_IsoVVVL_PFHT450,
    b_HLT_Mu15_IsoVVVL_PFHT450, 
    
    // 2017 bjet triggers
    b_HLT_DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_p33,
    b_HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0,
    b_HLT_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2,
    b_HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2,
    b_HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5,

    // 2018 bjet triggers
    b_HLT_DoublePFJets116MaxDeta1p6_DoubleCaloBTagDeepCSV_p71,
    b_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5,
    b_HLT_PFHT400_FivePFJet_100_100_60_30_30_DoublePFBTagDeepCSV_4p5,
    b_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94,
    b_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59,

    // 2017 + 2018 Displaced Dijet triggers
    b_HLT_HT430_DisplacedDijet40_DisplacedTrack,
    b_HLT_HT650_DisplacedDijet60_Inclusive,

    // 2016 Displaced Dijet triggers
    b_HLT_HT350_DisplacedDijet40_DisplacedTrack,
    b_HLT_HT650_DisplacedDijet80_Inclusive,

    // 2016 bjet triggers
    b_HLT_QuadJet45_TripleBTagCSV_p087,
    b_HLT_DoubleJet90_Double30_TripleBTagCSV_p087,
    b_HLT_DoubleJetsC100_DoubleBTagCSV_p014_DoublePFJetsC100MaxDeta1p6,

    // MET Trigger
    b_HLT_PFMET120_PFMHT120_IDTight,

    // // Low HT trigger to study filters using HLT tracking
    b_HLT_HT425, // Low HT trigger to study filters using HLT tracking
    n_hlt_paths, // = 27

    // seeding PFHT1050, the bjet triggers, and the displaced dijet triggers
    b_L1_HTT120er=0, b_L1_HTT160er, b_L1_HTT200er, b_L1_HTT220er, b_L1_HTT240er, b_L1_HTT255er, b_L1_HTT270er, b_L1_HTT280er, b_L1_HTT300er, b_L1_HTT320er, b_L1_HTT340er, b_L1_HTT360er, b_L1_HTT380er, b_L1_HTT400er, b_L1_HTT450er, b_L1_HTT500er, b_L1_HTT250er_QuadJet_70_55_40_35_er2p5, b_L1_HTT280er_QuadJet_70_55_40_35_er2p5, b_L1_HTT300er_QuadJet_70_55_40_35_er2p5, b_L1_HTT320er_QuadJet_70_55_40_40_er2p4, b_L1_DoubleJet100er2p3_dEta_Max1p6, b_L1_DoubleJet112er2p3_dEta_Max1p6,
    // the rest of Ele115+Ele50_PFJet165
    b_L1_SingleJet170, b_L1_SingleJet180, b_L1_SingleJet200, b_L1_SingleTau100er2p1, b_L1_SingleTau120er2p1,
    // IsoMu27 and Mu50
    b_L1_SingleMu22, b_L1_SingleMu25,
    n_l1_paths // = 29
  };

  enum {
    // Filters for 2017 di-bjet trigger (some are shared with 2018) (0,1,2,3  n=4)
    b_hltDoubleCaloBJets100eta2p3, b_hltBTagCalo80x6CSVp0p92DoubleWithMatching, b_hltDoublePFJets100Eta2p3, b_hltDoublePFJets100Eta2p3MaxDeta1p6,

    // Filters unique to 2018 di-bjet trigger (4, 5, 6  n=3)
    b_hltBTagCaloDeepCSV0p71Double6Jets80, b_hltDoublePFJets116Eta2p3, b_hltDoublePFJets116Eta2p3MaxDeta1p6, 

    // Filters for 2017 tri-bjet trigger (some are shared with 2018) (7-16, n=10)
    b_hltQuadCentralJet30, b_hltCaloQuadJet30HT300, b_hltBTagCaloCSVp05Double, b_hltPFCentralJetLooseIDQuad30, b_hlt1PFCentralJetLooseID75, b_hlt2PFCentralJetLooseID60,
    b_hlt3PFCentralJetLooseID45, b_hlt4PFCentralJetLooseID40, b_hltPFCentralJetsLooseIDQuad30HT300, b_hltBTagPFCSVp070Triple,
    
    // Filters unique to 2018 tri-bjet trigger (17-20, n=4)
    b_hltCaloQuadJet30HT320, b_hltBTagCaloDeepCSVp17Double, hltPFCentralJetsLooseIDQuad30HT330, hltBTagPFDeepCSV4p5Triple,

    // Filters for 2017/8 Displaced Dijet + Displaced Track trigger (21-25, n=5)
    b_hltHT430, b_hltDoubleCentralCaloJetpt40, b_hltTwoPromptHLTL3DisplacedDijetFullTracksHLTCaloJetTagFilterLowPt, b_hltL4PromptDisplacedDijetFullTracksHLTCaloJetTagFilterLowPt, b_hltL4DisplacedDijetFullTracksHLTCaloJetTagFilterLowPt,

    // Filters for 2017/8 Inclusive Displaced Dijet trigger (26-29, n=4)
    b_hltHT650, b_hltDoubleCentralCaloJetpt60, b_hltTwoPromptHLTL3DisplacedDijetFullTracksHLTCaloJetTagFilterMidPt, b_hltL4PromptDisplacedDijetFullTracksHLTCaloJetTagFilterMidPt,

    // Filters for 2016 Displaced Dijet + Displaced Track trigger (30, n=1)
    // only the HT filter is different from the 2017/18 trigger
    b_hltHT350, 
    
    // Filters for 2016 Inclsuive Displaced Dijet trigger (31-33, n=3)
    // The HT filter is the same as in 2017/18
    b_hltDoubleCentralCaloJetpt80, b_hltTwoPromptHLTL3DisplacedDijetFullTracksHLTCaloJetTagFilter, b_hltL4PromptDisplacedDijetFullTracksHLTCaloJetTagFilter,

    // Filters for 2016 first tri-bjet trigger (34-36, n=3)
    b_hltQuadCentralJet45, b_hltBTagCaloCSVp087Triple, b_hltQuadPFCentralJetLooseID45,

    // Filters for 2016 second tri-bjet trigger (37-39, n=3)
    // Some filters shared with the other tri-bjet triggers
    b_hltDoubleCentralJet90, b_hltQuadPFCentralJetLooseID30, b_hltDoublePFCentralJetLooseID90,

    // Filters for 2016 di-bjet trigger (40-43, n=4)
    b_hltDoubleJetsC100, b_hltBTagCaloCSVp014DoubleWithMatching, b_hltDoublePFJetsC100, b_hltDoublePFJetsC100MaxDeta1p6,

    // bookkeeping
    n_filter_paths // = 44
  };

  static_assert(n_l1_paths     <= 32, "too many l1 paths");
  static_assert(n_hlt_paths    <= 32, "too many hlt paths");
  static_assert(n_filter_paths <= 64, "too many filter paths");

  extern const char* hlt_paths[n_hlt_paths];
  extern const char* l1_paths[n_l1_paths];
  extern const char* clean_paths[n_clean_paths];
  extern const char* filter_paths[n_filter_paths];
  extern const int   filter_nreqs[n_filter_paths];

  // For use in the Bjet/DisplacedDijet trigger studies
  static const std::vector<size_t> HTOrBjetOrDisplacedDijetTriggers = {
    // HT trigger
    mfv::b_HLT_PFHT1050,
    // bjet triggers 2017 - only use the first two, since they contribute most of the efficiency
    mfv::b_HLT_DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_p33, mfv::b_HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0, 
    // bjet triggers 2018 - only use the first two, since they contribute most of the efficiency
    mfv::b_HLT_DoublePFJets116MaxDeta1p6_DoubleCaloBTagDeepCSV_p71, mfv::b_HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5, 
    // displaced dijet triggers 2017/18
    mfv::b_HLT_HT430_DisplacedDijet40_DisplacedTrack, mfv::b_HLT_HT650_DisplacedDijet60_Inclusive,
    //bjet triggers 2016
    mfv::b_HLT_QuadJet45_TripleBTagCSV_p087, mfv::b_HLT_DoubleJet90_Double30_TripleBTagCSV_p087, mfv::b_HLT_DoubleJetsC100_DoubleBTagCSV_p014_DoublePFJetsC100MaxDeta1p6,
    //displaced dijet triggers 2016
    mfv::b_HLT_HT350_DisplacedDijet40_DisplacedTrack, mfv::b_HLT_HT650_DisplacedDijet80_Inclusive
  };
}

#endif
