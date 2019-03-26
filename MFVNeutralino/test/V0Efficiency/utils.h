#ifndef v0efficiency_utils_h
#define v0efficiency_utils_h

#include <cmath>
#include <map>
#include <string>
#include "JMTucker/MFVNeutralino/interface/Ntuple.h"

class TFile;
class TTree;

void root_setup();

struct file_and_tree {
  TFile* f;
  TTree* t;
  mfv::K0Ntuple nt;
  TFile* f_out;

  file_and_tree(const char* in_fn, const char* out_fn);
  ~file_and_tree();
};

#endif
