#include "JMTucker/MFVNeutralino/interface/MovedTracksNtuple.h"

#include "TTree.h"

namespace mfv {
  void MovedTracksNtuple::clear() {
    run = lumi = event = 0;
    weight = pvx = pvy = pvz = move_x = move_y = move_z = 0;
    npu = npv = pvntracks = pvsumpt2 = ntracks = nseltracks = npreseljets = npreselbjets = nlightjets = 0;
    jets_pt.clear();
    jets_eta.clear();
    jets_phi.clear();
    jets_energy.clear();
    jets_ntracks.clear();
    vtxs_x.clear();
    vtxs_y.clear();
    vtxs_z.clear();
    vtxs_ntracks.clear();
    vtxs_ntracksptgt3.clear();
    vtxs_drmin.clear();
    vtxs_drmax.clear();
    vtxs_bs2derr.clear();
  }

  void MovedTracksNtuple::write_to_tree(TTree* tree) {
    tree->SetAlias("njets", "jets_pt@.size()");
    tree->SetAlias("nvtxs", "vtxs_x@.size()");

    tree->Branch("run", &run);
    tree->Branch("lumi", &lumi);
    tree->Branch("event", &event);
    tree->Branch("weight", &weight);
    tree->Branch("npu", &npu);
    tree->Branch("npv", &npv);
    tree->Branch("pvx", &pvx);
    tree->Branch("pvy", &pvy);
    tree->Branch("pvz", &pvz);
    tree->Branch("pvntracks", &pvntracks);
    tree->Branch("pvsumpt2", &pvsumpt2);
    tree->Branch("ntracks", &ntracks);
    tree->Branch("nseltracks", &nseltracks);
    tree->Branch("npreseljets", &npreseljets);
    tree->Branch("npreselbjets", &npreselbjets);
    tree->Branch("nlightjets", &nlightjets);
    tree->Branch("jets_pt", &jets_pt);
    tree->Branch("jets_eta", &jets_eta);
    tree->Branch("jets_phi", &jets_phi);
    tree->Branch("jets_energy", &jets_energy);
    tree->Branch("jets_ntracks", &jets_ntracks);
    tree->Branch("move_x", &move_x);
    tree->Branch("move_y", &move_y);
    tree->Branch("move_z", &move_z);
    tree->Branch("vtxs_x", &vtxs_x);
    tree->Branch("vtxs_y", &vtxs_y);
    tree->Branch("vtxs_z", &vtxs_z);
    tree->Branch("vtxs_ntracks", &vtxs_ntracks);
    tree->Branch("vtxs_ntracksptgt3", &vtxs_ntracksptgt3);
    tree->Branch("vtxs_drmin", &vtxs_drmin);
    tree->Branch("vtxs_drmax", &vtxs_drmax);
    tree->Branch("vtxs_bs2derr", &vtxs_bs2derr);
  }

  void MovedTracksNtuple::read_from_tree(TTree* tree) {
    tree->SetBranchAddress("run", &run);
    tree->SetBranchAddress("lumi", &lumi);
    tree->SetBranchAddress("event", &event);
    tree->SetBranchAddress("weight", &weight);
    tree->SetBranchAddress("npu", &npu);
    tree->SetBranchAddress("npv", &npv);
    tree->SetBranchAddress("pvx", &pvx);
    tree->SetBranchAddress("pvy", &pvy);
    tree->SetBranchAddress("pvz", &pvz);
    tree->SetBranchAddress("pvntracks", &pvntracks);
    tree->SetBranchAddress("pvsumpt2", &pvsumpt2);
    tree->SetBranchAddress("ntracks", &ntracks);
    tree->SetBranchAddress("nseltracks", &nseltracks);
    tree->SetBranchAddress("npreseljets", &npreseljets);
    tree->SetBranchAddress("npreselbjets", &npreselbjets);
    tree->SetBranchAddress("nlightjets", &nlightjets);
    tree->SetBranchAddress("jets_pt", &jets_pt);
    tree->SetBranchAddress("jets_eta", &jets_eta);
    tree->SetBranchAddress("jets_phi", &jets_phi);
    tree->SetBranchAddress("jets_energy", &jets_energy);
    tree->SetBranchAddress("jets_ntracks", &jets_ntracks);
    tree->SetBranchAddress("move_x", &move_x);
    tree->SetBranchAddress("move_y", &move_y);
    tree->SetBranchAddress("move_z", &move_z);
    tree->SetBranchAddress("vtxs_x", &vtxs_x);
    tree->SetBranchAddress("vtxs_y", &vtxs_y);
    tree->SetBranchAddress("vtxs_z", &vtxs_z);
    tree->SetBranchAddress("vtxs_ntracks", &vtxs_ntracks);
    tree->SetBranchAddress("vtxs_ntracksptgt3", &vtxs_ntracksptgt3);
    tree->SetBranchAddress("vtxs_drmin", &vtxs_drmin);
    tree->SetBranchAddress("vtxs_drmax", &vtxs_drmax);
    tree->SetBranchAddress("vtxs_bs2derr", &vtxs_bs2derr);
  }
}
