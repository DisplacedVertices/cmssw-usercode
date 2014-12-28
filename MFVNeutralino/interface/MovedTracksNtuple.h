#ifndef JMTucker_MFVNeutralino_interface_MovedTracksNtuple_h
#define JMTucker_MFVNeutralino_interface_MovedTracksNtuple_h

#include <vector>

class TTree;

namespace mfv {
  struct MovedTracksNtuple {
    typedef unsigned short ushort;

    unsigned run;
    unsigned lumi;
    unsigned event;

    float weight;

    ushort npu;
    ushort npv;
    float pvx;
    float pvy;
    float pvz;
    ushort pvntracks;
    ushort pvsumpt2;

    ushort ntracks;
    ushort nseltracks;

    ushort npreseljets;
    ushort npreselbjets;
    ushort nlightjets;
    std::vector<float> jets_pt;
    std::vector<float> jets_eta;
    std::vector<float> jets_phi;
    std::vector<float> jets_energy;
    std::vector<ushort> jets_ntracks;

    float move_x;
    float move_y;
    float move_z;

    std::vector<float> vtxs_x;
    std::vector<float> vtxs_y;
    std::vector<float> vtxs_z;
    std::vector<ushort> vtxs_ntracks;
    std::vector<ushort> vtxs_ntracksptgt3;
    std::vector<float> vtxs_drmin;
    std::vector<float> vtxs_drmax;
    std::vector<float> vtxs_bs2derr;

    void clear();
    void write_to_tree(TTree* tree);
    void read_from_tree(TTree* tree);
  };
}

#endif
