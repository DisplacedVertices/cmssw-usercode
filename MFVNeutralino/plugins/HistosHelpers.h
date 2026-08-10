#ifndef JMTucker_MFVNeutralino_HistosHelpers_h
#define JMTucker_MFVNeutralino_HistosHelpers_h

#include <cmath>

#include "TH1F.h"
#include "TH2F.h"

using std::vector;

/*
Helper file written by Yuqing
*/

namespace pt_helpers {
  // Throw out low-pT events

  enum pt_region {
    pt_none = -1,
    pt_all,
    pt_keep
  };

  static const bool filter_seed_tracks_w_low_pt = false; // Flag for filtering all low-pT seed tracks. Turn on to filter tracks.

  static const float pt_cut = 4.0; // GeV

  static const int pt_num_regions = 2;

  // Convert pt_cut to something like "2" or "2p5"
  static const int int_ptcut = int(pt_cut);
  static const int dp_ptcut = int(pt_cut * 10) % 10;
  static const std::string pt_tag = std::to_string(int_ptcut) + (dp_ptcut > 0 ? "p" + std::to_string(dp_ptcut) : "");
  static const std::string pt_dp_tag = std::to_string(int_ptcut) + (dp_ptcut > 0 ? "." + std::to_string(dp_ptcut) : "");

  static const std::string pt_region_tags[pt_num_regions] = {
    "",
    "_ptgt" + pt_tag
  };

  static const std::string pt_region_names[pt_num_regions] = {
    "",
    "pT > " + pt_dp_tag + " GeV"
  };
  

  inline pt_region get_general_pt_region(const double pt) {
    if (pt > pt_cut) {
      return pt_keep;
    }
    return pt_none;
  }


  static const bool remove_vertex_w_low_pt_track = false;

  template <typename VertexAuxT>
  inline bool remove_vertex(const VertexAuxT& aux) {
    if (!remove_vertex_w_low_pt_track) {
      return false;
    }

    for (int i = 0; i < aux.ntracks(); ++i) {
      if (get_general_pt_region(aux.track_pt(i)) == pt_none) {
        return true;
      }
    }

    return false;
  }

}



namespace eta_helpers {
  
  enum eta_region {
    eta_none = -1,
    eta_all,
    eta_barrel,
    eta_endcap
  };

  static const int eta_num_regions = 3;
  
  static const char* eta_region_tags[eta_num_regions] = {
    "",
    "_barrel",
    "_endcap"
  };

  static const char* eta_region_names[eta_num_regions] = {
    "",
    "barrel",
    "endcap"
  };


  // General eta region finder - later I might add ele, mu etas
  inline eta_region get_general_eta_region(const double eta) {
    if (abs(eta) < 1.4) {
      return eta_barrel;
    }
    return eta_endcap;
  }


  // Eta region fillers
  inline void fill_general_eta(TH1F** hs, const double eta, const double val, const double w) {
    hs[int(eta_all)]->Fill(val, w);
    const int region = int(get_general_eta_region(eta));
    if (region >= 0) {
      hs[int(region)]->Fill(val, w);
    };
  }

  // Later, might want TH2F filler too
  
}



namespace corr_2d_helpers {

  enum corr_2d_axes {
    dxy_ax,
    dxy_err_ax,
    pt_ax,
    pt_err_ax,
    eta_ax,
    phi_ax,
    nlayers_ax,
    npxlayers_ax,
    nstlayers_ax,
    dz_ax,
    dz_err_ax,
  };

  static const int corr_2d_num_axes = 11;

  static const char* corr_2d_tags[corr_2d_num_axes] = {
    "_dxy",
    "_dxy_err",
    "_pt",
    "_pt_err",
    "_eta",
    "_phi",
    "_nlayers",
    "_npxlayers",
    "_nstlayers",
    "_dz",
    "_dz_err"
  };

  static const char* corr_2d_ax_labels[corr_2d_num_axes] = {
    "dxy (cm)",
    "#sigma(dxy) (cm)",
    "p_{T} (GeV)",
    "#sigma(p_{T})/p_{T} (GeV)",
    "#eta",
    "#phi",
    "# layers",
    "# pixel layers",
    "# strip layers",
    "dz (cm)",
    "#sigma(dz) (cm)"
  };

  static const vector<vector<double>> corr_2d_bins = {
    {100, -0.5, 0.5}, // dxy
    {30, 0, 0.03}, // dxy_err
    {300, 0, 300}, // pt
    {50, 0, 0.5}, // pt_err
    {40, -2.6, 2.6}, // eta
    {40, -3.15, 3.15}, // phi
    {30, 0, 30}, // nlayers
    {10, 0, 10}, // npxlayers
    {20, 0, 20}, // nstlayers
    {80, -0.2, 0.2}, // dz
    {60, 0, 0.15} // dz_err
  };

}


#endif


