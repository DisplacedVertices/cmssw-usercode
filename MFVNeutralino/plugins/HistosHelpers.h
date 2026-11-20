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



namespace hlt_trig_helpers {

  struct hlt_trig_info { // struct storing HLT trigger information
    int year;
    std::string path;
    std::string display_name;
  };

  static const int hlt_trig_year = MFVNEUTRALINO_YEAR == 20161 || MFVNEUTRALINO_YEAR == 20162 ? 2016 : MFVNEUTRALINO_YEAR; // Which year is stored in Year.h?

  static const int hlt_trig_num = hlt_trig_year == 2016 ? 5 : 4; // #triggers is hard-coded to match AN
  // static const int hlt_trig_num = 11;

  static const int hlt_trig_nentries = hlt_trig_num + 1; // +1 for the "all" entry


  static const vector<hlt_trig_info> hlt_trig_AN_list = { // Store the HLT trigger information: year applicable, path, and display name
    { 2016, "HLT_DoubleJetsC100_DoubleBTagCSV_p014_DoublePFJetsC100MaxDeta1p6_v", "di-bjet" },
    { 2016, "HLT_QuadJet45_TripleBTagCSV_p087_v", "symmetric tri-bjet" },
    { 2016, "HLT_DoubleJet90_Double30_TripleBTagCSV_p087_v", "skewed tri-bjet" },
    { 2016, "HLT_HT350_DisplacedDijet40_DisplacedTrack_v", "default displaced" },
    { 2016, "HLT_HT650_DisplacedDijet80_Inclusive_v", "inclusive displaced" },

    { 2017, "HLT_DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_p33_v", "di-bjet" },
    { 2017, "HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0_v", "tri-bjet" },
    { 2017, "HLT_HT430_DisplacedDijet40_DisplacedTrack_v", "default displaced" },
    { 2017, "HLT_HT650_DisplacedDijet60_Inclusive_v", "inclusive displaced" },

    { 2018, "HLT_DoublePFJets116MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v", "di-bjet" },
    { 2018, "HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5_v", "tri-bjet" },
    { 2018, "HLT_HT430_DisplacedDijet40_DisplacedTrack_v", "default displaced" },
    { 2018, "HLT_HT650_DisplacedDijet60_Inclusive_v", "inclusive displaced" },
  };


  inline vector<hlt_trig_info> get_hlt_trig_list() { // Get the list of HLT triggers for the year specified in Year.h
    vector<hlt_trig_info> result;
    for (const hlt_trig_info& trig : hlt_trig_AN_list) {
      if (trig.year == hlt_trig_year) {
        result.push_back(trig);
      }
    }
    return result;
  }

  static const vector<hlt_trig_info> hlt_trig_list = get_hlt_trig_list();

  inline std::string get_nth_hlt_tag(const int n) { // Obtain nth tag (not display_name), padded with "_". Used for histogram names.
    if (n==0) {return "";} // 0th entry is "all"
    std::string tag = "_" + hlt_trig_list[n-1].display_name;
    std::replace(tag.begin(), tag.end(), ' ', '_');
    return tag;
  }

  inline std::string get_nth_hlt_axislabel(const int n) {
    if (n==0) {return "";}
    return " (" + hlt_trig_list[n-1].display_name + " trig)"; // return the " (___ trig)" label, if applicable
  }

  /*
  inline int which_hlt_trig(const hlt_trig_info& trig) { // Given a trigger object, find the index in hlt_trig_list
    for (int i = 0; i < hlt_trig_num; ++i) {
      if (trig.path == hlt_trig_list[i].path) {
        return i + 1; // 0 represents "all" triggers
      }
    }
    return -1;
  }
  */

  inline vector<int> get_hlt_path_indices() { // Return the indices of the 4-5 HLT paths in mfv::hlt_paths
    vector<int> result;
    for (const hlt_trig_info& trig : hlt_trig_list) {
      int path_i = -1;
      for (int i = 0; i < mfv::n_hlt_paths; ++i) {
        const std::string hlt_path = mfv::hlt_paths[i]; // Array of const char*
        if (hlt_path.find(trig.path) != std::string::npos) {
          path_i = i;
          break;
        }
      }
      if (path_i < 0) { throw ("Error: HLT trigger is not in mfv::hlt_paths."); }
      result.push_back(path_i);
    }
    return result;
  }

  static const vector<int> hlt_path_indices = get_hlt_path_indices();


  template <typename EventT>
  inline void fill_by_hlt(TH1F** hs, const EventT& event, const double val, const double w) {
    hs[0]->Fill(val, w);
    bool found_trig = false;
    for (int i = 0; i < hlt_trig_num; ++i) {
      const int path_i = hlt_path_indices[i];
      if (event->found_hlt(path_i) && event->pass_hlt(path_i)) {
        hs[i+1]->Fill(val, w);
        found_trig = true;
      }
    }
    if (found_trig == false) {
      throw ("Error: event does not fire any specified HLT trigger.");
    }
  }

}


#endif


