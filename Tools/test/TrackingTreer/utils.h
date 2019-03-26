#ifndef JMTucker_Tools_TrackingTreer_utils
#define JMTucker_Tools_TrackingTreer_utils

#include "JMTucker/Tools/interface/Ntuple.h"

class TFile;
class TTree;

// JMTBAD common library with e.g. TrackMover

void root_setup();

struct file_and_tree {
  TFile* f;
  TTree* t;
  jmt::TrackingNtuple nt;
  TFile* f_out;

  file_and_tree(const char* in_fn, const char* out_fn);
  ~file_and_tree();
};

#endif
