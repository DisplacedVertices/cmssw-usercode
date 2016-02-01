#ifndef JMTucker_MFVNeutralino_interface_MiniNtuple_h
#define JMTucker_MFVNeutralino_interface_MiniNtuple_h

#include "TTree.h"

namespace mfv {
  struct MiniNtuple {
    unsigned run;
    unsigned lumi;
    unsigned long long event;
    unsigned char gen_flavor_code;
    unsigned char npv;
    float pvx;
    float pvy;
    float pvz;
    unsigned char npu;
    float weight;
    unsigned char njets;
    float jet_pt[50];
    float jet_eta[50];
    float jet_phi[50];
    float jet_energy[50];
    unsigned char jet_id[50];

    unsigned char nvtx;
    unsigned char ntk0;
    float x0;
    float y0;
    float z0;
    unsigned char ntracksptgt30;
    float drmin0;
    float drmax0;
    unsigned char njetsntks0;
    float bs2derr0;
    float geo2ddist0;
    unsigned char ntk1;
    float x1;
    float y1;
    float z1;
    unsigned char ntracksptgt31;
    float drmin1;
    float drmax1;
    unsigned char njetsntks1;
    float bs2derr1;
    float geo2ddist1;
  };

  void write_to_tree(TTree* tree, MiniNtuple& nt);
  void read_from_tree(TTree* tree, MiniNtuple& nt);
}

#endif
