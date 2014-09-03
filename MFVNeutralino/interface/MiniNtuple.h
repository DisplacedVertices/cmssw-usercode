#ifndef JMTucker_MFVNeutralino_interface_MiniNtuple_h
#define JMTucker_MFVNeutralino_interface_MiniNtuple_h

#include "TTree.h"

namespace mfv {
  struct MiniNtuple {
    unsigned run;
    unsigned lumi;
    unsigned event;
    unsigned short npv;
    float pvx;
    float pvy;
    float pvz;
    unsigned short npu;
    float weight;
    unsigned short njets;
    float jet_pt[50];
    float jet_eta[50];
    float jet_phi[50];
    float jet_energy[50];
    unsigned short nvtx;
    unsigned short ntk0;
    float x0;
    float y0;
    float z0;
    float cxx0;
    float cxy0;
    float cxz0;
    float cyy0;
    float cyz0;
    float czz0;
    unsigned short ntk1;
    float x1;
    float y1;
    float z1;
    float cxx1;
    float cxy1;
    float cxz1;
    float cyy1;
    float cyz1;
    float czz1;
  };

  void write_to_tree(TTree* tree, MiniNtuple& nt);
  void read_from_tree(TTree* tree, MiniNtuple& nt);
}

#endif
