#ifndef JMTucker_MFVNeutralino_interface_Event_h
#define JMTucker_MFVNeutralino_interface_Event_h

#include "TLorentzVector.h"
#include "JMTucker/MFVNeutralino/interface/EventTools.h"

struct MFVEvent {
  typedef unsigned char uchar;
  typedef unsigned short ushort;
  typedef unsigned int uint;

  static TLorentzVector p4(float pt, float eta, float phi, float mass) {
    TLorentzVector v;
    v.SetPtEtaPhiM(pt, eta, phi, mass);
    return v;
  }

  template <typename T>
  static T min(T x, T y) {
    return x < y ? x : y;
  }

  template <typename T>
  static T mag(T x, T y) {
    return sqrt(x*x + y*y);
  }

  template <typename T>
  static T mag(T x, T y, T z) {
    return sqrt(x*x + y*y + z*z);
  }

  bool gen_valid;
  float gen_lsp_pt[2];
  float gen_lsp_eta[2];
  float gen_lsp_phi[2];
  float gen_lsp_mass[2];
  float gen_lsp_decay[2*3];
  uchar gen_decay_type[2];
  uchar gen_partons_in_acc;

  TLorentzVector gen_lsp_p4(int w) const {
    return p4(gen_lsp_pt[w], gen_lsp_eta[w], gen_lsp_phi[w], gen_lsp_mass[w]);
  }

  float minlspdist2d() const {
    return min(mag(gen_lsp_decay[0*3+0] - bsx, gen_lsp_decay[0*3+1] - bsy),
               mag(gen_lsp_decay[1*3+0] - bsx, gen_lsp_decay[1*3+1] - bsy));
  }

  float lspdist2d() const {
    return mag(gen_lsp_decay[0*3+0] - gen_lsp_decay[1*3+0],
               gen_lsp_decay[0*3+1] - gen_lsp_decay[1*3+1]);
  }

  float lspdist3d() const {
    return mag(gen_lsp_decay[0*3+0] - gen_lsp_decay[1*3+0],
               gen_lsp_decay[0*3+1] - gen_lsp_decay[1*3+1],
               gen_lsp_decay[0*3+2] - gen_lsp_decay[1*3+2]);
  }

  bool pass_trigger[mfv::n_trigger_paths];
  bool pass_clean[mfv::n_clean_paths]; // JMTBAD
  bool passoldskim;

  uchar npfjets;
  float pfjetpt4;
  float pfjetpt5;
  float pfjetpt6;

  float npu;

  float bsx;
  float bsy;
  float bsz;

  uchar npv;
  float pvx;
  float pvy;
  float pvz;
  uchar pv_ntracks;
  float pv_sumpt2;
  float pv_rho() const { return mag(pvx - bsx, pvy - bsy); }

  uchar njets;
  uchar njetsnopu[3]; // loose, medium, tight
  float jetpt4;
  float jetpt5;
  float jetpt6;
  float jet_sum_ht;
  float metx;
  float mety;
  float metsig;
  float met() const { return mag(metx, mety); }
  float metphi() const { return atan2(mety, metx); }
  float metdphimin;

  uchar nbtags[3]; // loose, medium, tight
  uchar nmu[3]; // top pag "veto", "semilep", "dilep" 
  uchar nel[3]; // ditto
  int nlep(int w) const { return int(nmu[w]) + int(nel[w]); }
};

#endif
