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
    b_HLT_Ele27_WPTight_Gsf, //2016
    b_HLT_Ele32_WPTight_Gsf, //2018
    b_HLT_Ele35_WPTight_Gsf, //2017
    b_HLT_Ele115_CaloIdVT_GsfTrkIdT,
    b_HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165,
    b_HLT_IsoMu24, //2018
    b_HLT_IsoMu27, 
    b_HLT_Mu50,
    
    // displaced lepton triggers 
    b_HLT_Mu43NoFiltersNoVtx_Photon43_CaloIdL, 
    b_HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90, 
    b_HLT_DoublePhoton70, 
    b_HLT_DoubleMu43NoFiltersNoVtx, 

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
    //b_HLT_HT425, // Low HT trigger to study filters using HLT tracking
    n_hlt_paths, // = 27

    // seeding PFHT1050, the bjet triggers, and the displaced dijet triggers
    b_L1_HTT120er=0, b_L1_HTT160er, b_L1_HTT200er, b_L1_HTT220er, b_L1_HTT240er, b_L1_HTT255er, b_L1_HTT270er, b_L1_HTT280er, b_L1_HTT300er, b_L1_HTT320er, b_L1_HTT340er, b_L1_HTT360er, b_L1_HTT380er, b_L1_HTT400er, b_L1_HTT450er, b_L1_HTT500er, b_L1_HTT250er_QuadJet_70_55_40_35_er2p5, b_L1_HTT280er_QuadJet_70_55_40_35_er2p5, b_L1_HTT300er_QuadJet_70_55_40_35_er2p5, b_L1_HTT320er_QuadJet_70_55_40_40_er2p4, b_L1_DoubleJet100er2p3_dEta_Max1p6, b_L1_DoubleJet112er2p3_dEta_Max1p6,
    // the rest of Ele115+Ele50_PFJet165
    b_L1_SingleJet170, b_L1_SingleJet180, b_L1_SingleJet200, b_L1_SingleTau100er2p1, b_L1_SingleTau120er2p1,
    // IsoMu27 and Mu50
    b_L1_SingleMu22, b_L1_SingleMu25,
    n_l1_paths // = 29
  };

  static_assert(n_l1_paths     <= 32, "too many l1 paths");
  static_assert(n_hlt_paths    <= 32, "too many hlt paths");

  extern const char* hlt_paths[n_hlt_paths];
  extern const char* l1_paths[n_l1_paths];
  extern const char* clean_paths[n_clean_paths];
  

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

 //For Lepton Trigger Studies; the following depends on years 
  // 2016
  // static const std::vector<size_t> LeptonTriggers = {
  //   //lepton triggers
  //   mfv::b_HLT_Ele27_WPTight_Gsf, mfv::b_HLT_IsoMu27, mfv::b_HLT_Mu50,
  //   mfv::b_HLT_Ele115_CaloIdVT_GsfTrkIdT, mfv::b_HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165,
  // };
  // //2017
  //   static const std::vector<size_t> LeptonTriggers = {
  //   //lepton triggers
  //   mfv::b_HLT_Ele35_WPTight_Gsf, mfv::b_HLT_IsoMu27, mfv::b_HLT_Mu50,
  //   mfv::b_HLT_Ele115_CaloIdVT_GsfTrkIdT, mfv::b_HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165,
  // };
  //2018
  static const std::vector<size_t> LeptonTriggers = {
    mfv::b_HLT_Ele32_WPTight_Gsf, mfv::b_HLT_Ele115_CaloIdVT_GsfTrkIdT, mfv::b_HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165,
    mfv::b_HLT_IsoMu24, mfv::b_HLT_Mu50
  };

  //displaced lepton triggers 
  static const std::vector<size_t> DisplacedLeptonTriggers = {
    //displaced dilepton triggers
    mfv::b_HLT_Mu43NoFiltersNoVtx_Photon43_CaloIdL, mfv::b_HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90,
    mfv::b_HLT_DoublePhoton70, mfv::b_HLT_DoubleMu43NoFiltersNoVtx
  };		

}

#endif
