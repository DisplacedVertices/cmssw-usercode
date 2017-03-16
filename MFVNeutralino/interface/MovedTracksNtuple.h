#ifndef JMTucker_MFVNeutralino_interface_MovedTracksNtuple_h
#define JMTucker_MFVNeutralino_interface_MovedTracksNtuple_h

#include <vector>

class TTree;

namespace mfv {
  struct MovedTracksNtuple {
    typedef unsigned short uchar;
    typedef unsigned short ushort;

    unsigned run;
    unsigned lumi;
    unsigned long long event;

    float weight;

    bool gen_valid;
    float gen_lsp_pt[2];
    float gen_lsp_eta[2];
    float gen_lsp_phi[2];
    float gen_lsp_mass[2];
    float gen_lsp_decay[2*3];
    uchar gen_decay_type[2];
    uchar gen_partons_in_acc;

    uchar pass_hlt;
    uchar npu;
    uchar npv;
    float pvx;
    float pvy;
    float pvz;
    ushort pvntracks;
    float pvsumpt2;
    float jetht;
    float jetpt4;
    float met;
    uchar nlep;
    ushort ntracks;
    uchar nseltracks;
    uchar nalljets;

    uchar npreseljets;
    uchar npreselbjets;
    uchar nlightjets;
    std::vector<float> jets_pt;
    std::vector<float> jets_eta;
    std::vector<float> jets_phi;
    std::vector<float> jets_energy;
    std::vector<uchar> jets_ntracks;

    float move_x;
    float move_y;
    float move_z;

    std::vector<float> vtxs_x;
    std::vector<float> vtxs_y;
    std::vector<float> vtxs_z;
    std::vector<float> vtxs_theta; // tracksplusjets
    std::vector<float> vtxs_phi;
    std::vector<uchar> vtxs_ntracks;
    std::vector<uchar> vtxs_ntracksptgt3;
    std::vector<float> vtxs_drmin;
    std::vector<float> vtxs_drmax;
    std::vector<float> vtxs_bs2derr;

    MovedTracksNtuple();
    void clear();
    void write_to_tree(TTree* tree);
    void read_from_tree(TTree* tree);

    // ugh
    std::vector<float>* p_jets_pt;
    std::vector<float>* p_jets_eta;
    std::vector<float>* p_jets_phi;
    std::vector<float>* p_jets_energy;
    std::vector<uchar>* p_jets_ntracks;
    std::vector<float>* p_vtxs_x;
    std::vector<float>* p_vtxs_y;
    std::vector<float>* p_vtxs_z;
    std::vector<float>* p_vtxs_theta;
    std::vector<float>* p_vtxs_phi;
    std::vector<uchar>* p_vtxs_ntracks;
    std::vector<uchar>* p_vtxs_ntracksptgt3;
    std::vector<float>* p_vtxs_drmin;
    std::vector<float>* p_vtxs_drmax;
    std::vector<float>* p_vtxs_bs2derr;
  };
}

#endif
