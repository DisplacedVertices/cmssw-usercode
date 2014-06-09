#ifndef JMTucker_MFVNeutralino_interface_MiniNtuple_h
#define JMTucker_MFVNeutralino_interface_MiniNtuple_h

#include "TTree.h"

namespace mfv {
  struct MiniNtuple {
    unsigned run;
    unsigned lumi;
    unsigned event;
    unsigned short nvtx;
    unsigned short ntk0;
    float x0;
    float y0;
    float z0;
    unsigned short ntk1;
    float x1;
    float y1;
    float z1;
  };

  void write_to_tree(TTree* tree, MiniNtuple& nt);
  void read_from_tree(TTree* tree, MiniNtuple& nt);
}

#endif
