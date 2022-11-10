#include "JMTucker/MFVNeutralinoFormats/interface/TriggerEnum.h"

namespace mfv {
  // be sure these end in _v
  const char* hlt_paths[mfv::n_hlt_paths] = {
    "HLT_PFHT1050_v",
    "HLT_Ele35_WPTight_Gsf_v",
    "HLT_Ele115_CaloIdVT_GsfTrkIdT_v",
    "HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v",
    "HLT_IsoMu27_v",
    "HLT_Mu50_v",
    "HLT_Ele15_IsoVVVL_PFHT450_v",
    "HLT_Mu15_IsoVVVL_PFHT450_v",

    // 2017 bjet triggers
    "HLT_DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_p33_v",
    "HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0_v",
    "HLT_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2_v",
    "HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2_v",
    "HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5_v",

    // 2018 bjet triggers
    "HLT_DoublePFJets116MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v",
    "HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5_v",
    "HLT_PFHT400_FivePFJet_100_100_60_30_30_DoublePFBTagDeepCSV_4p5_v",
    "HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94_v",
    "HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59_v",

    // 2017 + 2018 Displaced Dijet triggers
    "HLT_HT430_DisplacedDijet40_DisplacedTrack_v",
    "HLT_HT650_DisplacedDijet60_Inclusive_v",

    // 2016 Displaced Dijet Triggers
    "HLT_HT350_DisplacedDijet40_DisplacedTrack",
    "HLT_HT650_DisplacedDijet80_Inclusive",

    // 2016 Bjet triggers
    "HLT_QuadJet45_TripleBTagCSV_p087",
    "HLT_DoubleJet90_Double30_TripleBTagCSV_p087",
    "HLT_DoubleJetsC100_DoubleBTagCSV_p014_DoublePFJetsC100MaxDeta1p6",

    // MET trigger
    "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v",

  };

  const char* l1_paths[mfv::n_l1_paths] = {
    "L1_HTT120er",
    "L1_HTT160er",
    "L1_HTT200er",
    "L1_HTT220er",
    "L1_HTT240er",
    "L1_HTT255er",
    "L1_HTT270er",
    "L1_HTT280er",
    "L1_HTT300er",
    "L1_HTT320er",
    "L1_HTT340er",
    "L1_HTT360er",
    "L1_HTT380er",
    "L1_HTT400er",
    "L1_HTT450er",
    "L1_HTT500er",
    "L1_HTT250er_QuadJet_70_55_40_35_er2p5",
    "L1_HTT280er_QuadJet_70_55_40_35_er2p5",
    "L1_HTT300er_QuadJet_70_55_40_35_er2p5",
    "L1_HTT320er_QuadJet_70_55_40_40_er2p4",
    "L1_DoubleJet100er2p3_dEta_Max1p6",
    "L1_DoubleJet112er2p3_dEta_Max1p6",
    "L1_SingleJet170",
    "L1_SingleJet180",
    "L1_SingleJet200",
    "L1_SingleTau100er2p1",
    "L1_SingleTau120er2p1",
    "L1_SingleMu22",
    "L1_SingleMu25"
  };

  const char* clean_paths[mfv::n_clean_paths] = {
    "Flag_HBHENoiseFilter",
    "Flag_HBHENoiseIsoFilter",
    "Flag_EcalDeadCellTriggerPrimitiveFilter",
    "Flag_goodVertices",
    "Flag_eeBadScFilter",
    "Flag_globalTightHalo2016Filter",
    "Flag_CSCTightHalo2015Filter"
  };


  const char* filter_paths[mfv::n_filter_paths] = {

    // 2017 di-bjet filter names
    "hltDoubleCaloBJets100eta2p3", // also in 2018
    "hltBTagCalo80x6CSVp0p92DoubleWithMatching",
    "hltDoublePFJets100Eta2p3",
    "hltDoublePFJets100Eta2p3MaxDeta1p6",

    // 2018 di-bjet filter names
    "hltBTagCaloDeepCSV0p71Double6Jets80",
    "hltDoublePFJets116Eta2p3",
    "hltDoublePFJets116Eta2p3MaxDeta1p6",

    // 2017 tri-bjet filter names
    "hltQuadCentralJet30",          // also in 2018
    "hltCaloQuadJet30HT300",
    "hltBTagCaloCSVp05Double",
    "hltPFCentralJetLooseIDQuad30", // in 2018
    "hlt1PFCentralJetLooseID75",    // in 2018
    "hlt2PFCentralJetLooseID60",    // in 2018
    "hlt3PFCentralJetLooseID45",    // in 2018
    "hlt4PFCentralJetLooseID40",    // in 2018
    "hltPFCentralJetsLooseIDQuad30HT300",
    "hltBTagPFCSVp070Triple",

    // 2018 tri-bjet filter names
    "hltCaloQuadJet30HT320",
    "hltBTagCaloDeepCSVp17Double",
    "hltPFCentralJetsLooseIDQuad30HT330",
    "hltBTagPFDeepCSV4p5Triple",

  };

  const int filter_nreqs[mfv::n_filter_paths] = {

    // 2017 di-bjet trigger
    2,
    2,
    2,
    1,

    // 2018 di-bjet trigger
    2,
    2,
    1,

    // 2017 tri-bjet trigger
    4,
    300, // this is an HT filter
    2,
    4,
    1,
    2,
    3,
    4,
    300, // this is an HT filter
    3,

    // 2018 tri-bjet trigger
    320, // this is an HT filter
    2,
    330, // this is an HT filter
    3,

  };

}
