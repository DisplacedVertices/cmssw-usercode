#ifndef JMTucker_Tools_TrackingTreer_utils
#define JMTucker_Tools_TrackingTreer_utils

#include "JMTucker/Tools/interface/TrackingTree.h"

class TFile;
class TTree;

void root_setup();

struct file_and_tree {
  TFile* f;
  TTree* t;
  TrackingTree nt;

  file_and_tree(const char* in_fn);
  ~file_and_tree();
};

#endif
