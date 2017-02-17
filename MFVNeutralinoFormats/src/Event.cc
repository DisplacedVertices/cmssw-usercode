#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"

namespace mfv {
  const char* hlt_paths[mfv::n_hlt_paths] = {
    "HLT_PFHT350_v",
    "HLT_PFHT800_v",
    "HLT_PFHT900_v",
    "HLT_PFJet450_v",
    "HLT_AK8PFJet450_v"
  };

  const char* l1_paths[mfv::n_l1_paths] = {
    "L1_HTT100",
    "L1_HTT125",
    "L1_HTT150",
    "L1_HTT175",
    "L1_HTT160",
    "L1_HTT200",
    "L1_HTT220",
    "L1_HTT240",
    "L1_HTT255",
    "L1_HTT270",
    "L1_HTT280",
    "L1_HTT300",
    "L1_HTT320",
    "L1_SingleJet128",
    "L1_SingleJet170",
    "L1_SingleJet180",
    "L1_SingleJet200"
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
}
